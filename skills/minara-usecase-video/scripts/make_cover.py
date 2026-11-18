#!/usr/bin/env python3
"""Make a cover image for a Minara use case video.

Pulls one real UI frame from the rendered video (or uses a given image),
lays it out with the title in the brand cover style, and screenshots it
with headless Chrome.

  make_cover.py --video output/x-v3.mp4 --at 62 --title "Turn your trading idea into a live strategy." \
      --sub "Strategy Studio · Desktop" -o output/cover
  make_cover.py --shot frame.png --title "..." --layouts landscape -o output/cover

Outputs <out>/cover-landscape.png (1920x1080) and cover-portrait.png (1080x1920),
plus the extracted shot.png and the cover-*.html sources for manual tweaks.
"""
import argparse, html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets", "cover")
LOGO = os.environ.get("MINARA_LOGO_PATH") or os.path.join(ASSETS, "minara-logo-dark.png")
if not os.path.isfile(LOGO):
    raise SystemExit("Set MINARA_LOGO_PATH to your logo (PNG for a dark background); the logo is not shipped")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SIZES = {"landscape": (1920, 1080), "portrait": (1080, 1920)}

# Screen crops per display mode, in 1080p frame coordinates (W:H:X:Y). See SKILL.md §3 "Device display".
CROPS = {
    "phone": "780:1688:150:116",          # phone body (assets/phone-frame.html), screen only
    "monitor": "1656:931:132:74",         # PC monitor on desktop background, no stand (assets/pc-monitor-frame.html)
    "legacy-phone": "972:1728:54:96",     # before 2026-11-13: 90% phone screen, no body
    "legacy-monitor": "1656:931:132:38",  # before 2026-11-13: monitor with stand
    "none": None,                         # full screen, or PC + phone in one frame: use the whole frame
}


def probe(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-of", "json", video],
                         capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    return s["width"], s["height"]


def grab(video, t, dst, frame="auto"):
    w, h = probe(video)
    if frame == "auto":
        frame = "phone" if h > w else "monitor"
    crop = CROPS[frame]
    if crop:  # crops are in 1080p coordinates; 2K/4K exports scale them up
        k = min(w, h) / 1080
        crop = ":".join(str(round(int(v) * k)) for v in crop.split(":"))
    vf = ["-vf", f"crop={crop}"] if crop else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video,
                    "-frames:v", "1", *vf, dst], check=True)
    return "phone" if h > w else "desktop"


CSS = """
@font-face { font-family: 'Geist'; src: url('{font}') format('woff2'); font-weight: 100 900; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: {W}px; height: {H}px; overflow: hidden; background: #0E0F11; }
body { font-family: 'Geist', system-ui, -apple-system, sans-serif; color: #FFFFFF; position: relative;
  -webkit-font-smoothing: antialiased; }
.glow { position: absolute; inset: 0;
  background: radial-gradient(1100px 760px at {gx} {gy}, rgba(255,255,255,0.075), rgba(255,255,255,0) 70%); }
.logo { position: absolute; height: {logoH}px; left: {pad}px; top: {pad}px; }
.copy { position: absolute; }
.tt { font-weight: 650; letter-spacing: -0.025em; line-height: 1.06; text-wrap: balance; }
.ts { margin-top: 30px; color: #8A8A8A; font-weight: 500; letter-spacing: -0.005em; }
.shot { position: absolute; overflow: hidden; border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0 40px 120px rgba(0,0,0,0.55), 0 0 0 10px rgba(255,255,255,0.03); background: #15171A; }
.shot img { display: block; width: 100%; height: 100%; object-fit: cover; object-position: {objpos}; }
"""

# Per layout × shot kind: copy block box, shot box, type sizes. Shots bleed off the edge on purpose.
LAYOUT = {
    ("landscape", "desktop"): dict(copy="left:96px; top:0; bottom:0; width:720px; display:flex; flex-direction:column; justify-content:center;",
                                   shot="left:900px; top:200px; width:1180px; height:664px; border-radius:22px;",
                                   tt=88, ts=30, gx="72%", gy="55%", objpos="left top"),
    ("landscape", "phone"):   dict(copy="left:96px; top:0; bottom:0; width:900px; display:flex; flex-direction:column; justify-content:center;",
                                   shot="left:1200px; top:150px; width:540px; height:960px; border-radius:44px;",
                                   tt=92, ts=30, gx="76%", gy="60%", objpos="center top"),
    ("portrait", "desktop"):  dict(copy="left:80px; right:80px; top:230px;",
                                   shot="left:80px; top:760px; width:1560px; height:878px; border-radius:24px;",
                                   tt=96, ts=34, gx="60%", gy="72%", objpos="left top"),
    ("portrait", "phone"):    dict(copy="left:80px; right:80px; top:230px;",
                                   shot="left:160px; top:680px; width:760px; height:1351px; border-radius:56px;",
                                   tt=96, ts=34, gx="50%", gy="75%", objpos="center top"),
}


def page(layout, kind, title, sub, shot):
    W, H = SIZES[layout]
    L = LAYOUT[(layout, kind)]
    css = CSS
    for k, v in dict(font="file://" + os.path.join(ASSETS, "geist-latin-wght-normal.woff2"),
                     W=W, H=H, gx=L["gx"], gy=L["gy"], logoH=60 if layout == "landscape" else 64,
                     pad=80 if layout == "landscape" else 80, objpos=L["objpos"]).items():
        css = css.replace("{" + k + "}", str(v))
    sub_html = f'<div class="ts" style="font-size:{L["ts"]}px">{html.escape(sub)}</div>' if sub else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="glow"></div>
<img class="logo" src="file://{LOGO}">
<div class="copy" style="{L['copy']}"><div class="tt" style="font-size:{L['tt']}px">{html.escape(title)}</div>{sub_html}</div>
<div class="shot" style="{L['shot']}"><img src="file://{shot}"></div>
</body></html>"""


def shoot(src, dst, W, H):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}", "--virtual-time-budget=1500",
                    f"--screenshot={dst}", "file://" + src], check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--video", help="rendered use case mp4; the frame at --at becomes the shot")
    g.add_argument("--shot", help="use this image as the shot instead")
    ap.add_argument("--at", type=float, default=0, help="seconds into --video")
    ap.add_argument("--frame", default="auto", choices=["auto", *CROPS],
                    help="display mode of the video; auto = phone for portrait, monitor for landscape. "
                         "Use none for full-screen films and PC + phone films")
    ap.add_argument("--monitor", action="store_true", help="alias for --frame monitor")
    ap.add_argument("--kind", choices=["desktop", "phone"], help="shot kind (auto from --video)")
    ap.add_argument("--title", required=True)
    ap.add_argument("--sub", default="")
    ap.add_argument("--layouts", default="landscape,portrait")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    if a.video:
        shot = os.path.join(out, "shot.png")
        kind = grab(a.video, a.at, shot, "monitor" if a.monitor else a.frame)
    else:
        shot = os.path.abspath(a.shot)
        kind = a.kind or "desktop"
    kind = a.kind or kind

    for layout in a.layouts.split(","):
        W, H = SIZES[layout]
        src = os.path.join(out, f"cover-{layout}.html")
        with open(src, "w") as f:
            f.write(page(layout, kind, a.title, a.sub, shot))
        dst = os.path.join(out, f"cover-{layout}.png")
        shoot(src, dst, W, H)
        print(dst)


if __name__ == "__main__":
    main()
