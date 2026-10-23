#!/usr/bin/env python3
"""Read a brand system from a saved website or a local brand kit and print it.

Usage: python3 -I extract_brand.py <source> <outDir>

<source> can be:
  site.mhtml            a saved web page ("Webpage, Single File")
  brandkit/             a local brand-kit folder (logos, fonts, colour/token files, guideline PDF)
  tokens.json / .css / .scss / .md / .txt / .ase-less text file with colours
  guideline.pdf         a brand-guideline PDF (listed for reading; colours are pulled from its text if possible)

Writes:
  <outDir>/parts/       (mhtml only) every MIME part; page.html renders offline for a reference screenshot
  <outDir>/tokens.json  colours (CSS vars and hex counts), font families, font files, logos, images
Prints the same, ranked, so the colour and type choices can be read straight off it.
"""
import email
import json
import os
import re
import subprocess
import sys
from collections import Counter

EXT = {"text/html": "html", "text/css": "css", "image/svg+xml": "svg", "image/png": "png",
       "image/jpeg": "jpg", "image/webp": "webp", "image/gif": "gif", "font/woff2": "woff2"}
FONT_EXT = {".woff2", ".woff", ".ttf", ".otf"}
IMG_EXT = {".svg", ".png", ".jpg", ".jpeg", ".webp"}
TEXT_EXT = {".css", ".scss", ".less", ".json", ".md", ".txt", ".html", ".yaml", ".yml", ".js", ".ts", ".xml"}
HEX = r"#[0-9a-fA-F]{6}\b"


def scan_text(text):
    """Colour vars, hex usage, font families, sizes and tracking found in any CSS-like or prose text."""
    var_vals = {}
    for k, v in re.findall(r"(--[a-zA-Z0-9-]+)\s*:\s*([^;}{\n]{1,80})", text):
        if not k.startswith("--tw-"):
            var_vals.setdefault(k, v.strip())
    # JSON / YAML style tokens: "primary": "#264cf1"
    for k, v in re.findall(r"(?<![\w-])[\"']?([A-Za-z][\w .-]{1,40})[\"']?\s*[:=]\s*[\"']?(#[0-9a-fA-F]{3,8})\b", text):
        var_vals.setdefault(k.strip(), v)
    colours = {k: v for k, v in var_vals.items() if re.match(r"#[0-9a-fA-F]{3,8}\b|rgb|hsl|oklch", v)}
    fonts = Counter(f.strip() for f in re.findall(r"font-family\s*:\s*([^;}{\n]+)", text))
    for f in re.findall(r"(?:[Tt]ypeface|[Ff]ont|字体)\s*[:：]\s*`?([A-Z][\w ]{2,40})", text):
        if f.strip().split()[0] not in {"Family", "Size", "Weight", "Font"}:
            fonts[f.strip()] += 1
    # markdown tables in guideline docs: | Geist | Regular 400 | / | Geist | 12px | 400 |
    for f in re.findall(r"(?m)^\|\s*([A-Z][\w ]{2,30}?)\s*\|\s*(?:(?:Regular|Medium|Bold|Semi ?Bold|Light|Thin|Black)\b|\d{3}\s*\||\d+px\s*\|\s*\d{3}\b)", text):
        if f.strip() not in {"Font", "Size", "Weight"}:
            fonts[f.strip()] += 1
    return {
        "colours": colours,
        "other_vars": {k: v for k, v in var_vals.items() if k not in colours},
        "fonts": fonts,
        "hex": Counter(h.lower() for h in re.findall(HEX, text)),
        "sizes": Counter(re.findall(r"font-size\s*:\s*([^;}{\n]+)", text)),
        "tracking": Counter(re.findall(r"letter-spacing\s*:\s*([^;}{\n]+)", text)),
    }


def from_mhtml(src, out):
    parts_dir = os.path.join(out, "parts")
    os.makedirs(parts_dir, exist_ok=True)
    msg = email.message_from_binary_file(open(src, "rb"))
    parts, html, css_all, loc_map = [], None, "", {}
    for i, p in enumerate(x for x in msg.walk() if not x.is_multipart()):
        ct, loc = p.get_content_type(), p.get("Content-Location", "")
        data = p.get_payload(decode=True) or b""
        fn = f"part{i:02d}.{EXT.get(ct, 'bin')}"
        open(os.path.join(parts_dir, fn), "wb").write(data)
        parts.append({"file": os.path.join(parts_dir, fn), "type": ct, "bytes": len(data), "location": loc})
        loc_map[loc] = fn
        if ct == "text/html" and html is None:
            html = data.decode("utf8", "ignore")
        if ct == "text/css":
            css_all += data.decode("utf8", "ignore") + "\n"
    if html:
        page = re.sub(r"<script.*?</script>", "", html, flags=re.S)
        for loc, fn in loc_map.items():
            if loc:
                page = page.replace(loc, fn)
        open(os.path.join(parts_dir, "page.html"), "w").write(page)
    text = css_all + "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html or "", flags=re.S)) + (html or "")
    refs = sorted(set(re.findall(r'(?:src|href)="([^"]+\.(?:png|jpg|jpeg|webp|svg))"', html or "")))
    return {
        "kind": "mhtml", "scan": scan_text(text),
        "logos": [p for p in parts if p["type"] == "image/svg+xml" or "logo" in p["location"].lower()],
        "images": sorted((p for p in parts if p["type"].startswith("image/")), key=lambda p: -p["bytes"]),
        "font_files": [p for p in parts if p["type"].startswith("font/")],
        "docs": [], "missing": [r for r in refs if r not in loc_map],
        "notes": [f"{parts_dir}/page.html renders offline; screenshot it once for the layout"],
    }


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def from_paths(paths, root):
    text, logos, images, fonts, docs, notes = "", [], [], [], [], []
    for f in paths:
        ext = os.path.splitext(f)[1].lower()
        rel = os.path.relpath(f, root) if os.path.isdir(root) else os.path.basename(f)
        size = os.path.getsize(f)
        item = {"file": f, "type": ext.lstrip("."), "bytes": size, "location": rel}
        if ext in FONT_EXT:
            fonts.append(item)
        elif ext in IMG_EXT:
            (logos if re.search(r"(?i)logo|mark|wordmark|icon|symbol", rel) else images).append(item)
        elif ext == ".pdf":
            docs.append(item)
            t = pdf_text(f)
            if t:
                text += "\n" + t
            else:
                notes.append(f"Read {rel} with the Read tool (pages=...) — no text layer extracted")
        elif ext in TEXT_EXT and size < 3_000_000:
            text += "\n" + open(f, encoding="utf8", errors="ignore").read()
            if ext in {".md", ".txt"}:
                docs.append(item)
    images.sort(key=lambda p: -p["bytes"])
    return {"kind": "brandkit", "scan": scan_text(text), "logos": logos, "images": images,
            "font_files": fonts, "docs": docs, "missing": [], "notes": notes}


def from_source(src, out):
    if src.lower().endswith((".mhtml", ".mht")):
        return from_mhtml(src, out)
    if os.path.isdir(src):
        paths = []
        for dp, dn, fn in os.walk(src):
            dn[:] = [d for d in dn if not d.startswith(".") and d not in {"node_modules", "__MACOSX"}]
            paths += [os.path.join(dp, f) for f in fn if not f.startswith(".")]
        return from_paths(sorted(paths), src)
    return from_paths([src], src)


def main(src, out):
    if not os.path.exists(src):
        sys.exit(f"Not found: {src}\nPass a .mhtml file, a brand-kit folder, or a token / guideline file.")
    os.makedirs(out, exist_ok=True)
    r = from_source(src, out)
    s = r["scan"]
    tokens = {"source": src, "kind": r["kind"], "colour_vars": s["colours"], "other_vars": s["other_vars"],
              "font_families": s["fonts"].most_common(), "hex_usage": s["hex"].most_common(20),
              "font_sizes": s["sizes"].most_common(15), "letter_spacing": s["tracking"].most_common(10),
              "font_files": r["font_files"], "logos": r["logos"], "images": r["images"][:20],
              "docs": r["docs"], "missing_images": r["missing"], "notes": r["notes"]}
    json.dump(tokens, open(os.path.join(out, "tokens.json"), "w"), indent=1)

    print(f"Source: {src} ({r['kind']})\n")
    print("Colour tokens:")
    for k, v in list(s["colours"].items())[:30]:
        print(f"  {k:<28} {v}")
    if not s["colours"]:
        print("  (none named)")
    print("\nMost used hex colours:")
    print("  " + ("  ".join(f"{h}({n})" for h, n in s["hex"].most_common(12)) or "(none)"))
    print("\nFont families:")
    for f, n in s["fonts"].most_common(8):
        print(f"  {n:>3}× {f}")
    print("\nFont files:")
    for p in r["font_files"][:12]:
        print(f"  {p['location']}")
    if s["tracking"]:
        print("\nLetter-spacing in use:", ", ".join(t for t, _ in s["tracking"].most_common(6)))
    print("\nLogos:")
    for p in r["logos"][:12]:
        print(f"  {p['location']}  ({p['bytes']} B)")
    print("\nOther images (largest first):")
    for p in r["images"][:8]:
        print(f"  {p['location']}  ({p['bytes']} B)")
    if r["docs"]:
        print("\nGuideline documents (read these for usage rules: clear space, logo colour, do/don't):")
        for p in r["docs"][:8]:
            print(f"  {p['location']}")
    if r["missing"]:
        print("\nImages referenced but NOT in the archive (ask the operator for these):")
        for m in r["missing"][:10]:
            print("  " + m)
    for n in r["notes"]:
        print("\nNote: " + n)
    print(f"\nWrote {out}/tokens.json")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
