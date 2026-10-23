---
name: video-cover
description: Make a cover / thumbnail for a finished video. Reads the video's script doc (or storyboard / plan), pulls out the key message, writes one main title, picks one key visual, then designs a three-element cover (brand logo + title + key visual, no small text) in the brand system the operator points to — a local brand kit (folder of logos, fonts, colour/token files, guideline .md/.pdf), a saved website (.mhtml), a design.md, or the video's own composition — and exports 2560×1440 + 1280×720 PNGs (or portrait / square sizes) with an automatic overlap and overflow check, then can put the cover on the film's first frames (0.1s) so first-frame thumbnails show it. Local HTML + headless Chrome, no image generation. Use for /video-cover, "做封面", "视频封面", "缩略图", "封面图", "thumbnail", "cover image", "给这个视频做个封面", "封面合并到第一帧", "封面放进视频开头".
---

# /video-cover — Video cover from the script, in the brand's own system

A cover is one still that says what the film is about in under two seconds. It has **three elements only: the brand logo, one main title and one key visual.** No label, subtitle, proof number, date or any other small text ; small text is unreadable at thumbnail size and only adds clutter. It is built in HTML from the same assets as the film (fonts, logo, key image), so type and colour match the brand exactly, then shot with headless Chrome.

`<skill>` below means this skill's installed directory (for example `~/.claude/skills/video-cover`, `~/.agents/skills/video-cover` or `~/.codex/skills/video-cover`).

## Inputs (find them before asking)

| Input | Where to look | Required |
|---|---|---|
| Script | project `docs/*script*.md`, `PLAN*.md`, `STORYBOARD.md`, or the composition's on-screen text | yes |
| Brand source | what the operator named, in this order of preference: a **local brand kit** (folder or single file), a saved website `.mhtml`, a `design.md`, or the video's own composition | yes |
| Key image | the film's hero asset (product shot, sculpture, logo mark) in the project `assets/` | usually |
| Platform / size | ask only if unknown; default 16:9 2560×1440 + 1280×720 | default ok |

If no brand source is given, ask once. Don't fall back to the Minara palette for a non-Minara brand.

### Brand sources the extractor reads

| Source | What it is | What gets pulled |
|---|---|---|
| Brand-kit folder | e.g. `Brand/`, `Media Kit/`, `Brand Kit/`: logos, fonts, banners, a guideline doc | logo files (light / dark, SVG / PNG), font files, hex colours and named tokens from any `.css` `.scss` `.json` `.yaml` `.md` `.txt` `.pdf` inside, font names from guideline tables, guideline docs to read |
| Single brand file | `tokens.json`, `brand.css`, `design.md`, `Brand Guidelines.pdf` | named colour tokens, hex colours, font families |
| Saved website | `.mhtml` ("Save as → Webpage, Single File") | CSS custom properties, font families, letter-spacing, logo SVG, images, plus an offline `page.html` for a reference screenshot; lists images the page uses that the archive didn't save |
| HyperFrames composition | the film's `index.html` | reuse its `:root` tokens, `@font-face` and `assets/` directly (no script needed) |

## Workflow

1. **Read the script and extract the message.** Write down, in one line each:
   - What it is (product / model / feature name, and who makes it)
   - What it's for (the one or two use cases the film stresses)
2. **Write the main title** (English unless the film is in another language).
   - 2–4 words, on one or two lines. Reuse the brand's own launch phrasing when it exists (website hero, launch post), e.g. `Introducing Acme.`
   - Accent colour on the product name only.
   - It's the only text on the cover. Everything from step 1 that doesn't fit in the title (maker, use case, any number) stays off the cover; the film and the post copy carry it.
   - Copy rules: same voice rules as `minara-videoscript` (calm, no hype words, no exclamation marks, sentence case). Nothing the film or the brand's own copy doesn't say.
   - **Pick one key visual**: the film's hero asset (product shot, sculpture, the product's key screen or object). One focal point; no collage, no extra badges or chips.
3. **Extract the brand system.**
   ```bash
   python3 -I <skill>/scripts/extract_brand.py "<brand-kit folder | brand file | site.mhtml>" <project>/cover/brand
   ```
   It prints colour tokens, the most used hex colours, font families and font files, logos, other images, and guideline documents, and saves `brand/tokens.json`. For an `.mhtml` it also splits the archive into `brand/parts/` with an offline `page.html`. Then:
   - **Read the guideline docs it lists** (`.md` directly, `.pdf` with page ranges). They decide what the extractor can't: which colour is the accent vs. a status colour, which logo version goes on a light or dark background, clear space, minimum size, banned uses. Brand rules beat the counts the script prints.
   - Pick: paper / background, ink / title text, accent; the display font; the logo version for the cover's background (light / dark, from the brand kit); the key image. Label font, muted and hairline colours aren't needed.
   - Fonts: use font files from the kit if it has them; otherwise download woff2 (Google Fonts CSS2 with a desktop User-Agent, `latin` subset) into `<project>/assets/fonts/`. A variable font needs one file with `font-weight: 100 900`.
   - Website source: screenshot `parts/page.html` once with headless Chrome and look at header, hero layout, accent use, button shape. Ask the operator for any image listed as "NOT in the archive".
4. **Lay out the cover** from `<skill>/assets/cover-template.html`. Copy it to `<project>/cover/cover.html`, fill the tokens, fonts, copy and image paths. Defaults that worked:
   - Canvas 1920×1080 CSS px, exported at device scale 4/3 → 2560×1440.
   - Three blocks only: `logo`, `title` and `image`. Don't add a header hairline, label, subtitle or proof block.
   - Logo top-left (~112px in, ~84px down, 56–72px tall), at its own aspect ratio, respecting the kit's clear space. Use the mark or the wordmark the brand kit gives for that background; Minara covers use the current official media-kit logo.
   - Title in the left column (x≈112–990), vertically centred, 170–210px (the longest line must fit 880px; the check flags overflow), line-height ~0.94, tracking −0.05em; key image on the right (x≈1010 onward, never behind the title), bleeding off the right edge if it has a transparent background.
   - The title should stay readable at 320px wide (the smallest thumbnail size); if it doesn't, shorten it before shrinking it.
   - Keep the bottom-right and bottom-left 120px clear of key text (YouTube timestamp, X play button).
5. **Shoot and check.**
   ```bash
   node <skill>/scripts/shoot_cover.cjs <project>/cover/cover.html <project>/cover landscape
   ```
   It renders `cover-2560x1440.png` and `cover-1280x720.png` (`portrait` → 1440×2560 + 720×1280, `square` → 2160×2160 + 1080×1080), and prints a check:
   - every element marked `data-block` with its box
   - **overlaps** between blocks (e.g. the title running into the key image)
   - **overflow**: text wider than its box, e.g. a nowrap context line running past the rule above it
   - blocks outside the canvas
   The template is laid out for landscape. For `portrait` / `square`, re-stack it first (logo top, image in the middle, title below) and size the title to the narrower column; the check reports anything left off-canvas.
   Fix anything it reports, re-shoot, then open the 1280×720 PNG and look at it at thumbnail size: title readable, one focal point, nothing touching an edge it shouldn't, and no text on the canvas besides the title and the logo.
   Needs Node with Playwright available (`npx playwright --version` once caches it) and Google Chrome or Playwright's Chromium; `sips` (macOS) makes the thumbnail.
6. **Put the cover on the film's first frames** (when the film is rendered, or when the operator asks). Many places take the first frame as the thumbnail (X, Telegram, Discord, most players), so the cover goes in front of the film for a very short hold:
   ```bash
   <skill>/scripts/prepend_cover.sh <film>.mp4 <cover-2560x1440>.png <film>-cover.mp4 0.1 [2560x1440]
   ```
   - Default hold 0.1s = 6 frames at 60fps: a thumbnail grabber gets the cover, a viewer barely sees it. Don't go above 0.2s.
   - The audio is delayed by the same amount, so the music and sound cues stay on their beats. The film itself is not retimed.
   - Pass the 4K master with `2560x1440` when it still exists (one lanczos scale); otherwise the delivered 2K file is fine (one CRF 16 re-encode).
   - Verify: frames 0–5 match the cover PNG, frame 6 matches the film's frame 0, total length = film + hold, and the audio onset moved by the hold:
     ```bash
     ffmpeg -v error -i <film>-cover.mp4 -vf "select='lte(n,7)'" -vsync 0 /tmp/n%02d.png   # look at n06 / n07
     ffmpeg -i <film>-cover.mp4 -af silencedetect=n=-60dB:d=0.02 -vn -f null - 2>&1 | grep -m1 silence_end
     ```
   - Keep both files: `<film>.mp4` (no cover) for editors and platforms with a custom-thumbnail upload, `<film>-cover.mp4` for platforms that use the first frame.
7. **Deliver.** Copy the PNGs (and `-cover.mp4`) into the project `output/` next to the film, `open -R` the large one, and report: the title and where it came from (script or brand source), the logo file and key visual used, and the brand tokens used.

## Don't

- Add small text: label, subtitle, proof number, date, caption, badge. Logo, title and key visual only, unless the operator asks for one more element on that cover.
- Use image generation for the cover. The title must be real type, set in the brand's font, and the logo the real logo file.
- Invent a tagline the film doesn't say, or a number that isn't in the source data.
- Recolour, stretch or redraw a logo. Use the kit's version for the background (light / dark) at its own aspect ratio.
- Use the Minara palette or Geist on another brand's cover, or another brand's look on a Minara cover. Minara covers follow `minara-video`'s fixed style (Geist, Minara colours, no gradient).
- Measure layout by eye. Use the check output.

## Files

| File | What it is |
|---|---|
| `assets/cover-template.html` | Landscape cover template, logo + title + key visual only, with `{{TOKENS}}`; blocks carry `data-block` for the check |
| `scripts/extract_brand.py` | Reads a brand-kit folder, a single token / guideline file, or an `.mhtml`; prints colours, fonts, font files, logos, images, guideline docs; writes `tokens.json` |
| `scripts/shoot_cover.cjs` | Headless Chrome export at full + thumbnail size, with overlap / overflow / bounds check |
| `scripts/prepend_cover.sh` | Puts the cover on the film's first frames (default 0.1s) and delays the audio to match |
