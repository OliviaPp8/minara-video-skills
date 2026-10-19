#!/usr/bin/env python3
"""Cut a recorded narration into script lines and place them on the film's voiceover track.

  vo.py lines  <script.md>  -o vo-lines.json            # read voiceover lines + times from the script doc
  vo.py align  <narration>  vo-lines.json -o vo-clips.json   # find each line in the recording
  vo.py build  vo-clips.json -o assets/vo.wav --duration 71   # place clips on a film-length track
  vo.py mux    <video.mp4> assets/vo.wav [--bgm bgm-duck.wav] -o out.mp4
  vo.py check  <video_or_wav> vo-clips.json             # find every clip in the result, confirm it lands on time

Deterministic, local only (ffmpeg + whisper-cli + numpy). 48 kHz mono for the voiceover track.
"""
import argparse, difflib, json, os, re, subprocess, sys, tempfile
import numpy as np

SR = 48000
MODEL_CANDIDATES = [
    os.environ.get("WHISPER_MODEL", ""),
    os.path.expanduser("~/.cache/whisper/ggml-small.en.bin"),
    os.path.expanduser("~/.cache/whisper/ggml-base.en.bin"),
]
LEAD = 0.25   # default gap between a keyframe range start and the line start
PRE, POST = 0.03, 0.08   # padding kept around detected speech
FADE = 0.015


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, check=True, **kw)


def load(path, sr=SR):
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def save_wav(path, x, sr=SR):
    import wave
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def words(text):
    return [w for w in re.sub(r"[^a-z0-9'$%.]+", " ", text.lower().replace("’", "'")).split() if w.strip(".")]


def norm(w):
    return w.strip(".'").replace("'", "")


# ---------- lines: script doc -> vo-lines.json ----------
def parse_time(cell):
    m = re.search(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*s", cell)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"(\d+(?:\.\d+)?)\s*s", cell)
    return (float(m.group(1)), None) if m else (None, None)


def cmd_lines(a):
    md = open(a.script, encoding="utf-8").read().splitlines()
    out, hdr = [], None
    for ln in md:
        if not ln.strip().startswith("|"):
            hdr = None if not ln.strip() else hdr
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        low = [c.lower() for c in cells]
        if "voiceover" in low and "time" in low and "key" in " ".join(low):
            hdr = {n: i for i, n in enumerate(low)}
            continue
        if not hdr or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        vo = cells[hdr["voiceover"]].strip()
        if vo in ("", "—", "-"):
            continue
        t0, t1 = parse_time(cells[hdr["time"]])
        out.append({"key": cells[0], "text": vo.strip('"“”'), "range": [t0, t1],
                    "at": round(t0 + LEAD, 2) if t0 is not None else None})
    if not out:
        sys.exit("No keyframe sheet with Key / Time / Voiceover columns found. Write vo-lines.json by hand: "
                 '[{"key":"K1","text":"…","range":[0,2.4],"at":0.25}]')
    json.dump(out, open(a.o, "w"), indent=1, ensure_ascii=False)
    for l in out:
        print(f'{l["key"]:>5}  at {l["at"]:6.2f}s  range {l["range"]}  "{l["text"]}"')
    print(f"{len(out)} lines -> {a.o}")


# ---------- align: recording + lines -> vo-clips.json ----------
def whisper_words(audio, model):
    model = model or next((m for m in MODEL_CANDIDATES if os.path.exists(m)), None)
    if not model:
        sys.exit("No whisper model. Download one:\n  mkdir -p ~/.cache/whisper && curl -L -o "
                 "~/.cache/whisper/ggml-small.en.bin "
                 "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin")
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", audio, "-ar", "16000", "-ac", "1", wav])
        run(["whisper-cli", "-m", model, "-f", wav, "-l", "en", "-ml", "1", "-sow", "-oj", "-of",
             os.path.join(d, "a"), "-np"])
        segs = json.load(open(os.path.join(d, "a.json")))["transcription"]
    out = []
    for s in segs:
        for w in words(s["text"]):
            out.append((norm(w), s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000))
    return out


def envelope(x, hop=0.01):
    n = int(hop * SR)
    fr = x[: len(x) // n * n].reshape(-1, n)
    return 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9), hop


def refine(env, hop, a, b, lo, hi, floor):
    """Tighten [a,b] to where speech energy actually is, without crossing [lo,hi]."""
    i0, i1 = int(max(lo, a - 0.25) / hop), int(min(hi, b + 0.25) / hop)
    seg = env[i0:i1]
    on = np.where(seg > floor)[0]
    if len(on) == 0:
        return a, b
    s, e = (i0 + on[0]) * hop, (i0 + on[-1] + 1) * hop
    return max(lo, s - PRE), min(hi, e + POST)


def cmd_align(a):
    lines = json.load(open(a.lines))
    tw = whisper_words(a.narration, a.model)
    script = [(norm(w), li) for li, l in enumerate(lines) for w in words(l["text"])]
    sm = difflib.SequenceMatcher(None, [w for w, _ in script], [w for w, _, _ in tw], autojunk=False)
    hit = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            hit[blk.a + k] = blk.b + k
    x = load(a.narration)
    env, hop = envelope(x)
    floor = env.max() - a.floor_db
    rough, last_j = [], -1
    for li, l in enumerate(lines):
        idx = [i for i, (_, L) in enumerate(script) if L == li]
        pos = [k for k, i in enumerate(idx) if i in hit]
        if not pos:
            rough.append(None); continue
        # words heard differently at the edges ("agent" heard as "AI") still belong to this line
        j0 = max(last_j + 1, hit[idx[pos[0]]] - pos[0])
        j1 = min(len(tw) - 1, hit[idx[pos[-1]]] + (len(idx) - 1 - pos[-1]))
        last_j = j1
        rough.append((tw[j0][1], tw[j1][2], len(pos) / len(idx)))
    clips, prev_end = [], 0.0
    for li, l in enumerate(lines):
        r = rough[li]
        if r is None:
            clips.append({**l, "src": None, "status": "MISSING"}); continue
        nxt = next((q[0] for q in rough[li + 1:] if q), len(x) / SR)
        s, e = refine(env, hop, r[0], r[1], prev_end, max(r[1], nxt - 0.02), floor)
        prev_end = e
        clips.append({**l, "file": os.path.abspath(a.narration), "src": [round(s, 3), round(e, 3)], "len": round(e - s, 3),
                      "match": round(r[2], 2), "status": "OK" if r[2] >= 0.8 else "CHECK"})
    used = set(hit.values())
    extra = [w for i, (w, _, _) in enumerate(tw) if i not in used]
    json.dump(clips, open(a.o, "w"), indent=1, ensure_ascii=False)
    report(clips)
    if extra:
        print(f"\nHeard but not in script ({len(extra)} words): {' '.join(extra[:40])}")
    print(f"-> {a.o}")


def report(clips):
    print(f'{"key":>5} {"status":7} {"source":>15} {"len":>5} {"at":>7} {"room":>6}  text')
    for i, c in enumerate(clips):
        nxt = next((d["at"] for d in clips[i + 1:] if d.get("at") is not None), None)
        end = c["range"][1] if c["range"][1] is not None else nxt
        room = (end - c["at"]) if (end is not None and c["at"] is not None) else None
        src = f'{c["src"][0]:6.2f}-{c["src"][1]:6.2f}' if c.get("src") else "—"
        flag = c["status"]
        if room is not None and c.get("len") and c["len"] > room:
            flag = "LONG"
        print(f'{c["key"]:>5} {flag:7} {src:>15} {c.get("len", 0):5.2f} {c["at"] or 0:7.2f} '
              f'{"—" if room is None else f"{room:6.2f}":>6}  "{c["text"]}"')


# ---------- build: vo-clips.json -> film-length vo.wav ----------
def cmd_build(a):
    clips = json.load(open(a.clips))
    src = {}
    out = np.zeros(int(a.duration * SR))
    f = int(FADE * SR)
    last = -1.0
    for c in clips:
        if not c.get("src") or c.get("at") is None:
            print(f'skip {c["key"]}: {c["status"]}'); continue
        path = c.get("file", a.narration or clips[0].get("file"))
        if not path:
            sys.exit("Pass --narration (or put \"file\" on each clip).")
        if path not in src:
            src[path] = load(path)
        s, e = c["src"]
        seg = src[path][int(s * SR): int(e * SR)].copy()
        r = np.ones(len(seg)); r[:f] = np.linspace(0, 1, f); r[-f:] = np.linspace(1, 0, f)
        seg *= r * (10 ** (c.get("gain_db", 0) / 20))
        i = int(c["at"] * SR)
        if c["at"] < last:
            print(f'WARNING {c["key"]} starts at {c["at"]:.2f}s, before the previous line ends ({last:.2f}s)')
        if i + len(seg) > len(out):
            sys.exit(f'{c["key"]} runs past the end of the film ({c["at"] + len(seg) / SR:.2f}s > {a.duration}s)')
        out[i:i + len(seg)] += seg
        last = c["at"] + len(seg) / SR
        print(f'{c["at"]:6.2f}-{last:6.2f}  {c["text"]}')
    tmp = a.o + ".raw.wav"
    save_wav(tmp, out)
    # loudness: speech at -16 LUFS integrated, true peak -1.5 dBTP
    run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", str(SR), "-ac", "1", a.o])
    os.remove(tmp)
    if a.split_dir:
        os.makedirs(a.split_dir, exist_ok=True)
        for c in clips:
            if c.get("src"):
                run(["ffmpeg", "-v", "error", "-y", "-i", c.get("file", a.narration), "-ss", str(c["src"][0]),
                     "-to", str(c["src"][1]), "-ar", str(SR), "-ac", "1",
                     os.path.join(a.split_dir, f'{c["key"]}.wav')])
    print(f"-> {a.o} ({a.duration}s, 48 kHz mono, -16 LUFS)")


# ---------- mux: put vo (+bgm) into a rendered video without re-encoding picture ----------
def cmd_mux(a):
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                     a.video]).stdout)
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", a.vo]
    if a.bgm:
        cmd += ["-i", a.bgm]
        fc = (f"[1:a]volume={a.vo_db}dB,aresample={SR},pan=stereo|c0=c0|c1=c0[v];"
              f"[2:a]volume={a.bgm_db}dB,aresample={SR}[b];"
              f"[v][b]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.89[a]")
    else:
        fc = f"[1:a]volume={a.vo_db}dB,aresample={SR},pan=stereo|c0=c0|c1=c0,alimiter=limit=0.89[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v:0", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
            "-b:a", "256k", "-ar", str(SR), "-t", f"{dur:.3f}", "-movflags", "+faststart", a.o]
    run(cmd)
    info = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,sample_rate",
                "-of", "csv=p=0", a.o]).stdout.decode().split()
    print(" | ".join(info), f"| {dur:.3f}s -> {a.o}")


# ---------- check: find every clip in the finished track by cross-correlation ----------
def cmd_check(a):
    clips = [c for c in json.load(open(a.clips)) if c.get("src") and c.get("at") is not None]
    sr = 16000
    mix = load(a.media, sr)
    srcs, bad = {}, 0
    for c in clips:
        f = c.get("file")
        if f not in srcs:
            srcs[f] = load(f, sr)
        s, e = c["src"]
        clip = srcs[f][int(s * sr): int(e * sr)]
        w0 = max(0, int((c["at"] - 1.0) * sr))
        win = mix[w0: int((c["at"] + 1.0) * sr) + len(clip)]
        if len(win) < len(clip):
            print(f'OFF {c["key"]:>5} outside the track'); bad += 1; continue
        n = 1 << (len(win) + len(clip)).bit_length()
        xc = np.fft.irfft(np.fft.rfft(win, n) * np.conj(np.fft.rfft(clip, n)), n)[: len(win) - len(clip) + 1]
        energy = np.sqrt(np.convolve(win ** 2, np.ones(len(clip)), "valid")) * np.linalg.norm(clip) + 1e-12
        score = xc / energy
        k = int(score.argmax())
        got, conf = (w0 + k) / sr, float(score[k])
        ok = abs(got - c["at"]) <= a.tol and conf >= 0.5
        bad += not ok
        print(f'{"ok " if ok else "OFF"} {c["key"]:>5} planned {c["at"]:6.2f}s found {got:6.2f}s '
              f'match {conf:.2f}  "{c["text"]}"')
    print("All lines on time." if not bad else f"{bad} line(s) off by more than {a.tol}s or not found.")
    sys.exit(1 if bad else 0)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("lines"); s.add_argument("script"); s.add_argument("-o", default="vo-lines.json")
    s = sp.add_parser("align"); s.add_argument("narration"); s.add_argument("lines")
    s.add_argument("-o", default="vo-clips.json"); s.add_argument("--model")
    s.add_argument("--floor-db", type=float, default=42, help="speech threshold below the loudest frame")
    s = sp.add_parser("build"); s.add_argument("clips"); s.add_argument("-o", required=True)
    s.add_argument("--duration", type=float, required=True); s.add_argument("--narration")
    s.add_argument("--split-dir", help="also write one wav per line here, for review")
    s = sp.add_parser("mux"); s.add_argument("video"); s.add_argument("vo"); s.add_argument("--bgm")
    s.add_argument("-o", required=True); s.add_argument("--vo-db", type=float, default=0)
    s.add_argument("--bgm-db", type=float, default=0)
    s = sp.add_parser("check"); s.add_argument("media"); s.add_argument("clips")
    s.add_argument("--tol", type=float, default=0.05)
    a = p.parse_args()
    {"lines": cmd_lines, "align": cmd_align, "build": cmd_build, "mux": cmd_mux, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    main()
