#!/usr/bin/env python3
"""Minara BGM + SFX generator driven by a cue sheet (cues.json) written from the per-second script.

Usage:
  make_music.py cues.json -o out_dir [--vo narration.wav]

Writes out_dir/bgm.wav (music + SFX, 48 kHz stereo). With a voiceover (--vo or "vo" in the
cue sheet) it also writes bgm-duck.wav (music ducked under speech, SFX untouched) and
preview-mix.wav (ducked bed + voice) for listening. Fully local and deterministic (numpy only).

Cue sheet (see examples/v2-launch.json):
{
  "duration": 60, "bpm": 120, "key": "A minor", "seed": 7,
  "sections": [{"start": 0, "end": 5, "energy": "intro"}, ...],
  "sfx": [{"t": 7.3, "type": "tap"}, {"t": 5.9, "type": "typing", "chars": 28, "cps": 22}, ...],
  "duck_db": -8, "vo": "assets/vo.wav"
}
energy: silent | intro | light | build | full | breakdown | climax | outro   (optional "level": 0.5-1.3)
sfx type: tap | typing | success | notify | bell | blips | sparkle | riser | whoosh | thud | crash
"""
import argparse, json, sys, wave, subprocess
from pathlib import Path
import numpy as np

SR = 48000
NOTES = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, "F": 5, "F#": 6, "GB": 6,
         "G": 7, "G#": 8, "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
SCALES = {"minor": [0, 2, 3, 5, 7, 8, 10], "major": [0, 2, 4, 5, 7, 9, 11]}
PROGS = {"minor": [0, 5, 2, 6], "major": [0, 4, 5, 3]}      # i-VI-III-VII  /  I-V-vi-IV
ENERGIES = {"silent", "intro", "light", "build", "full", "breakdown", "climax", "outro"}
SFX_TYPES = {"tap", "typing", "success", "notify", "bell", "blips", "sparkle", "riser", "whoosh", "thud", "crash"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cues")
    ap.add_argument("-o", "--out", default=".")
    ap.add_argument("--vo", help="voiceover wav/mp3 to duck under (overrides cue sheet 'vo')")
    a = ap.parse_args()
    cue_path = Path(a.cues)
    cues = json.loads(cue_path.read_text())
    validate(cues)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    music, sfx = render(cues)
    dur = cues["duration"]
    write(out / "bgm.wav", master(music + sfx, dur))
    print_plan(cues)
    vo_path = a.vo or cues.get("vo")
    if vo_path:
        vp = Path(vo_path)
        if not vp.is_absolute() and not vp.exists():
            vp = cue_path.parent / vp
        vo = load_audio(vp, len(music))
        g = duck_gain(vo, cues.get("duck_db", -8))
        bed = master(music * g + sfx, dur)
        write(out / "bgm-duck.wav", bed)
        mix = bed * 0.85 + np.stack([vo, vo], 1) * 0.9
        write(out / "preview-mix.wav", mix / max(1.0, np.max(np.abs(mix)) / 0.95))
        print(f"→ {out/'bgm-duck.wav'}  (ducked {cues.get('duck_db', -8)} dB under {vp.name})")
        print(f"→ {out/'preview-mix.wav'}  (listen-only: bed + voice)")
    print(f"→ {out/'bgm.wav'}  ({dur:.2f}s, {cues.get('bpm', 120)} BPM, {cues.get('key', 'A minor')})")


def validate(c):
    errs = []
    if not c.get("duration"):
        errs.append("duration is required")
    for i, s in enumerate(c.get("sections", [])):
        if s.get("energy") not in ENERGIES:
            errs.append(f"sections[{i}].energy '{s.get('energy')}' not in {sorted(ENERGIES)}")
        if not (0 <= s["start"] < s["end"] <= c["duration"] + 1e-6):
            errs.append(f"sections[{i}] start/end out of range")
    for i, x in enumerate(c.get("sfx", [])):
        if x.get("type") not in SFX_TYPES:
            errs.append(f"sfx[{i}].type '{x.get('type')}' not in {sorted(SFX_TYPES)}")
    if errs:
        sys.exit("Cue sheet errors:\n  " + "\n  ".join(errs))


def print_plan(c):
    print("Sections:")
    for s in c["sections"]:
        print(f"  {s['start']:6.2f}–{s['end']:6.2f}  {s['energy']:<9} {s.get('note', '')}")
    if c.get("sfx"):
        print(f"SFX: {len(c['sfx'])} cues")


# ---------------- synthesis ----------------
def render(c):
    dur = float(c["duration"]); N = int(SR * dur)
    rng = np.random.default_rng(c.get("seed", 7))
    bpm = float(c.get("bpm", 120)); BEAT = 60 / bpm; BAR = 4 * BEAT
    tonic, mode = parse_key(c.get("key", "A minor"))
    scale = SCALES[mode]; prog = PROGS[mode]
    mus = np.zeros(N); sfx = np.zeros(N)

    def tt(d): return np.arange(int(d * SR)) / SR

    def env(d, a=0.005, r=None, dec=None):
        t = tt(d); e = np.minimum(1, t / max(a, 1e-4))
        if dec: e = e * np.exp(-t / dec)
        if r: e = e * np.clip((d - t) / r, 0, 1)
        return e

    def put(buf, t, x, g=1.0):
        i = int(t * SR); j = min(N, i + len(x))
        if 0 <= i < N and j > i: buf[i:j] += g * x[:j - i]

    def mtof(m): return 440 * 2 ** ((m - 69) / 12)

    def deg(d, base):  # scale degree -> midi
        o, k = divmod(d, 7); return base + scale[k] + 12 * o

    base = 48 + tonic                      # tonic in octave 3 (E3..D#4)
    if base < 52: base += 12

    def chord(bar):
        d = prog[bar % len(prog)]
        return [deg(d + k, base) for k in (0, 2, 4, 6, 8)], deg(d, base) - 12

    pad_ph = rng.random((64, 3, 4)) * 6.28

    def pad_note(f, d, k=0):
        t = tt(d); x = np.zeros_like(t)
        for i, det in enumerate((-0.004, 0, 0.0037)):
            for j, (h, a) in enumerate(((1, 1), (2, .35), (3, .15), (4, .07))):
                x += a * np.sin(2 * np.pi * f * (1 + det) * h * t + pad_ph[k % 64, i, j])
        return x * env(d, a=0.7, r=0.9)

    def pluck(f, d=0.45):
        t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) for h, a in ((1, 1), (2, .45), (3, .2), (5, .08))) * env(d, a=0.003, dec=0.16)

    def bass(f, d=None):
        d = d or BEAT * 0.85; t = tt(d)
        return (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * env(d, a=0.006, dec=0.22, r=0.05)

    def kick():
        d = 0.42; t = tt(d); f = 45 + 80 * np.exp(-t / 0.035); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, a=0.001, dec=0.13)

    def hat(d=0.05):
        n = np.diff(np.concatenate([[0], rng.standard_normal(int(d * SR))])); return n * env(d, a=0.0005, dec=d / 4)

    def clap():
        d = 0.25; t = tt(d); n = rng.standard_normal(len(t))
        e = sum(np.exp(-np.maximum(t - o, 0) / 0.012) * (t >= o) for o in (0, .011, .022)) + 0.6 * np.exp(-t / 0.08)
        return band(n * e, 900, 4500)

    def bell(f, d=1.6):
        t = tt(d); return sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / dk) for r, a, dk in ((1, 1, .9), (2.76, .35, .35), (5.4, .15, .15))) * env(d, a=0.002)

    def click():
        d = 0.03; t = tt(d); return (np.sin(2 * np.pi * 2600 * t) + .5 * rng.standard_normal(len(t))) * np.exp(-t / 0.004)

    def tick():
        d = 0.012; n = rng.standard_normal(int(d * SR)); return np.diff(np.concatenate([[0], n])) * np.exp(-tt(d) / 0.002)

    def swell(d, lo=300, hi=6000, shape=2.0):
        x = band(rng.standard_normal(int(d * SR)), lo, hi); t = tt(d); return x * (t / d) ** shape

    def thud():
        d = 1.0; t = tt(d); f = 34 + 40 * np.exp(-t / 0.06)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, a=0.002, dec=0.35) + 0.25 * band(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.01)

    def crash(d=2.5):
        return band(rng.standard_normal(int(d * SR)), 3000, 12000) * env(d, a=0.002, dec=0.7)

    # ---- music, section by section ----
    sections = sorted(c.get("sections", []), key=lambda s: s["start"])
    tonic_note = deg(0, base)
    for si, s in enumerate(sections):
        a, b, e = float(s["start"]), float(s["end"]), s["energy"]
        lv = float(s.get("level", 1.0))
        if e == "silent":
            continue
        # pad: one chord per bar, bars counted on the global grid so harmony stays continuous
        if e != "outro":
            bar0 = int(a // BAR); t0 = bar0 * BAR
            while t0 < b:
                st = max(t0, a); d = min(t0 + BAR, b) - st + 0.9
                ch, _ = chord(bar0)
                pg = {"intro": .045, "breakdown": .05, "climax": .068}.get(e, .05)
                for k, m in enumerate(ch[:4]):
                    put(mus, st, pad_note(mtof(m), d, bar0 * 4 + k), pg * lv)
                bar0 += 1; t0 = bar0 * BAR
        if e == "intro":
            d = b - a + 0.6; put(mus, a, np.sin(2 * np.pi * mtof(tonic_note - 24) * tt(d)) * env(d, a=min(1.5, d / 3), r=0.8), 0.14 * lv)
        if e == "outro":
            d = b - a + 0.4
            for m in (tonic_note - 12, tonic_note, tonic_note + scale[4], tonic_note + 12, tonic_note + 12 + scale[2], tonic_note + 12 + scale[4]):
                put(mus, a, pad_note(mtof(m), d, 7), 0.05 * lv)
            for i, m in enumerate((tonic_note + 12, tonic_note + 12 + scale[4], tonic_note + 24)):
                put(mus, a + 0.2 + i * 0.18, bell(mtof(m), 2.6), 0.16 * lv)
            continue
        # sub under everything from light upward
        if e in ("light", "build", "full", "climax"):
            bar0 = int(a // BAR); t0 = bar0 * BAR
            while t0 < b:
                st = max(t0, a); d = min(t0 + BAR, b) - st
                _, r = chord(bar0); put(mus, st, np.sin(2 * np.pi * mtof(r - 12) * tt(d)) * env(d, a=0.05, r=0.2), 0.10 * lv)
                bar0 += 1; t0 = bar0 * BAR
        # 8th-note grid
        step = BEAT / 2; s0 = int(np.ceil(a / step - 1e-9))
        k = s0
        while k * step < b - 1e-9:
            t0 = k * step; bar = int(t0 // BAR); off = k % 2; ch, r = chord(bar)
            last_bar = t0 >= b - BAR
            drums = e in ("full", "climax") or (e == "build") or (e == "light") or (e == "breakdown" and last_bar)
            if drums:
                if e == "light":
                    if k % 4 == 0: put(mus, t0, kick(), 0.55 * lv)
                    if off: put(mus, t0, hat(), 0.05 * lv)
                else:
                    if k % 2 == 0: put(mus, t0, kick(), (0.7 if e == "climax" else 0.55) * lv)
                    if e != "breakdown" and (off or e in ("full", "climax")): put(mus, t0, hat(), (0.05 if off else 0.03) * lv)
                    if e in ("full", "climax") and k % 4 == 2: put(mus, t0, clap(), 0.18 * lv)
            if e in ("build", "full", "climax"):
                put(mus, t0, bass(mtof(r)), (0.22 if not off else 0.14) * lv)
            if e in ("light", "build", "full", "climax", "breakdown"):
                m = ch[[0, 2, 1, 3, 4, 2, 1, 3][k % 8]] + 12
                ag = {"light": .045, "breakdown": .035}.get(e, .06)
                put(mus, t0, pluck(mtof(m)), ag * lv)
            k += 1
        if e == "build":
            d = min(2.0, b - a); put(mus, b - d, swell(d, 800, 7000), 0.05 * lv)
        if e == "climax":
            put(mus, a, crash(), 0.05 * lv)
            # lead: chord-tone motif, quarter notes with eighth pickups, one phrase per 2 bars
            pat = [(0, 2, 1.0), (1, 4, .5), (1.5, 2, .5), (2, 1, 1.0), (3, 0, 1.0), (4, 1, .5), (4.5, 2, .5), (5, 4, 1.0), (6, 2 + 7, 1.5), (7.5, 4, .5)]
            t_phrase = a
            while t_phrase < b - BEAT:
                bar = int(t_phrase // BAR)
                for bt, dg, dl in pat:
                    t0 = t_phrase + bt * BEAT
                    if t0 >= b - 0.1: break
                    m = deg(prog[(bar + int(bt // 4)) % len(prog)] + dg, base) + 12 if dg < 7 else deg(dg - 7 + 2, base) + 24
                    d = dl * BEAT * 2 + 0.5; t = tt(d); f = mtof(m)
                    x = (np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t) + .08 * np.sin(6 * np.pi * f * t)) * env(d, a=0.02, dec=0.6, r=0.3)
                    put(mus, t0, x, 0.09 * lv)
                t_phrase += 2 * BAR
        # transition riser into a louder next section
        nxt = sections[si + 1]["energy"] if si + 1 < len(sections) else None
        if nxt == "climax" and e != "build":
            d = min(2.0, b - a); put(mus, b - d, swell(d, 600, 8000, 2.5), 0.07)

    # ---- SFX ----
    for x in c.get("sfx", []):
        t0 = float(x["t"]); ty = x["type"]; g = float(x.get("gain", 1.0))
        if ty == "tap": put(sfx, t0, click(), 0.16 * g)
        elif ty == "typing":
            cps = float(x.get("cps", 22)); n = int(x.get("chars", 20))
            for i in range(n): put(sfx, t0 + i / cps, tick(), 0.10 * g * (0.7 + 0.6 * rng.random()))
        elif ty == "success":
            put(sfx, t0, bell(mtof(84), 1.0), 0.09 * g); put(sfx, t0 + 0.12, bell(mtof(91), 1.2), 0.09 * g)
        elif ty == "notify":
            for i, m in enumerate((88, 84, 88)): put(sfx, t0 + i * 0.11, bell(mtof(m), 0.7), 0.07 * g)
        elif ty == "bell": put(sfx, t0, bell(mtof(int(x.get("note", 81))), 1.6), 0.06 * g)
        elif ty == "blips":
            n = int(x.get("count", 10)); st = float(x.get("step", 0.13)); m0 = int(x.get("note", 64))
            for i in range(n): put(sfx, t0 + i * st, pluck(mtof(m0 + i), 0.15), 0.05 * g)
        elif ty == "sparkle":
            d = float(x.get("dur", 1.2))
            for i in range(int(d * 22)): put(sfx, t0 + d * (i / (d * 22)) ** 0.8, pluck(mtof(84 + int(rng.integers(0, 12))), 0.2), 0.025 * g)
            put(sfx, t0, swell(d, 2000, 9000, 1.6), 0.03 * g)
        elif ty == "riser":
            d = float(x.get("dur", 2.0)); put(sfx, t0, swell(d, 800, 7000), 0.05 * g)
        elif ty == "whoosh":
            d = float(x.get("dur", 0.6)); put(sfx, t0, swell(d, 400, 4000, 1.2)[::-1], 0.06 * g)
        elif ty == "thud": put(sfx, t0, thud(), 0.5 * g)
        elif ty == "crash": put(sfx, t0, crash(), 0.05 * g)

    mus = reverb(mus, rng, 1.8, .28); sfx = reverb(sfx, rng, 1.0, .12)
    return mus, sfx


def parse_key(k):
    k = k.strip()
    if " " not in k and k.endswith("m"): k = k[:-1] + " minor"
    parts = k.split(); note = parts[0].upper(); mode = parts[1].lower() if len(parts) > 1 else "minor"
    if note not in NOTES or mode not in SCALES:
        sys.exit(f"Bad key '{k}'. Use e.g. 'A minor', 'C major', 'F# minor', 'Am'.")
    return NOTES[note], mode


def band(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); m = np.ones_like(f)
    if hi: m *= 1 / np.sqrt(1 + (f / hi) ** 4)
    if lo: m *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** 4)
    return np.fft.irfft(X * m, len(x))


def reverb(x, rng, dur, wet):
    n = int(dur * SR); t = np.arange(n) / SR
    ir = band(rng.standard_normal(n) * np.exp(-t / 0.45), hi=5000); ir /= np.sqrt(np.sum(ir ** 2))
    L = len(x) + n; y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[:len(x)]
    return x + wet * y


def master(x, dur):
    if x.ndim == 2: x = x[:, 0]
    x = band(x, 28, 16000); N = len(x); t = np.arange(N) / SR
    x = x * np.clip(t / 0.4, 0, 1) * np.clip((dur - 0.1 - t) / 3.2, 0, 1)
    x = np.tanh(x * 1.4) / np.tanh(1.4)
    pk = np.max(np.abs(x)) or 1; x = x * 10 ** (-1 / 20) / pk
    st = np.stack([x, x], 1); st[:, 1] = np.roll(st[:, 1], int(0.0007 * SR))
    return st


def load_audio(path, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).astype(np.float64)
    return np.pad(v, (0, max(0, n - len(v))))[:n]


def duck_gain(vo, db):
    w = int(0.01 * SR); n = len(vo) // w
    rms = np.sqrt(np.mean(vo[:n * w].reshape(n, w) ** 2, 1))
    on = (rms > max(1e-4, 0.08 * np.max(rms))).astype(float)
    env = np.zeros(n); a, r = 1 - np.exp(-1 / 5), 1 - np.exp(-1 / 30)   # ~50 ms attack, ~300 ms release
    for i in range(n):
        env[i] = env[i - 1] + (a if on[i] > env[i - 1] else r) * (on[i] - env[i - 1]) if i else on[0] * a
    g = 1 - (1 - 10 ** (db / 20)) * env
    full = np.repeat(g, w); full = np.pad(full, (0, len(vo) - len(full)), mode="edge")
    return full


def write(path, st):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    main()
