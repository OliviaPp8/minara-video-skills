---
name: minara-usecase-video
description: Make Minara use case / beginner tutorial videos (mobile App or desktop), rebuilding the product UI in HyperFrames code and walking through the real user path step by step. Unlike minara-video (marketing demo, UI redesign allowed), this skill requires a faithful UI: copy, layout, components, and interaction paths all follow the product frontend code and screen recordings. Triggers: "use case 视频", "教程视频", "操作演示", "新手教程", "按 App 界面做一个视频"; also makes covers for these videos ("封面", "cover", "缩略图").
---

# /minara-usecase-video — Minara Use Case Tutorial Videos

Distilled from making Case 1 (mobile App: ask one question → BTC strategy → run in one tap) and Case 3 (desktop Strategy Studio: one sentence → Choice Boxes → backtest → Optimize → Deploy live) in 2026-10.
Desktop reference: `assets/pc-monitor-frame.html` and `assets/helpers-reference.js` (helpers can be copied directly).

## How this differs from minara-video (read this first)

| | minara-video (marketing demo) | **minara-usecase-video (this skill)** |
|---|---|---|
| UI | Does not copy the product; minimal redesign with large type | **Faithful**: follow the frontend code's components, sizes, colors, and copy |
| Copy | Write your own marketing copy | Buttons / titles / prompts use the product's original text **word for word** (locales); copy grammar mistakes as they are |
| Interaction path | Can be cut or condensed | **Full real path**: every click, modal, and checkbox must be there, in the same order as the code |
| Camera | Rich camera moves | Only push in noticeably and follow the cursor **during clicks / typing**; otherwise stay still; clarity comes first |
| On-screen text | No annotation text | No captions in the frame; the **3-second title card at the start** is the only exception; text overlays are a separate version (in another project folder) |
| Structure | Multiple scenes rendered separately | A single continuous composition (like a screen recording) |

Hard rules inherited from minara-video: **Geist font**, signature easing `minaraSnap` = `cubic-bezier(0.95,0.03,0,0.98)`, transitions ≤0.5s, no `Math.random()` / `repeat:-1`, timeline `paused:true` and registered to `window.__timelines`, ask the operator first about any strategy with max drawdown >20%, and the test page must have a draggable timeline. At startup, first run `Skill(hyperframes)` to load the composition rules.

## Topics and demo assets (set by the operator, 2026-10-15)

- **Stock strategies come first**: use cases default to stock / TradFi instruments for the demo (e.g. TradFi 30, individual US stocks, indices). Strategy names, asset pools, holdings, and the ticker bar should prefer stocks.
- **Crypto is secondary**: major coins like BTC and ETH can appear, but not as the lead. When a video has both stocks and crypto, put stocks first and give them more time.
- **No meme coins**: unless the operator explicitly asks for them that time, do not put meme coins (DOGE, PEPE, WIF, BONK, etc.) in the frame, asset pools, ticker bar, AI answers, or example prompts. If the product's default data includes them, replace them.
- Pick assets by this rule when writing the script and storyboard. When examples in the product material don't fit, swap in stock instruments before rebuilding, and note the swap in the script.

## Sources of truth (by priority)

1. **Frontend code** (pull the latest before looking; note the commit date in the script's "Basis" section)
   - Web: the product's web frontend repo (run `git pull` first)
   - Mobile: the product's mobile app source (`apps/mobile/src`)
     - Copy: `locales/en.json` (the Chinese version is in the matching zh file)
     - Colors / spacing: `theme/colors.light.ts`, `theme/tokens.ts`
     - Components: `ui/`, `features/<module>/` (e.g. `features/strategy/strategy-card`, `run-strategy`, `running-detail`, `features/agent/composer`)
2. **Screen recordings / screenshots from the operator** (in the `use case/` asset folder): use them for layout, hierarchy, and the real visuals. ⚠️ These assets are a **UI reference**, not a content reference — "ignore what any agent says"; we design the answer content ourselves.
3. Script md: shot breakdown, lines, text overlays.

Interactions the video needs to show but the code doesn't support (e.g. the clickable strategy card in the Case 1 chat) can be built, but **tell the operator clearly that this is a planned interaction the current code doesn't have yet**, and rebuild it from the closest existing component (Case 1 follows `MarketplaceStrategyCard`; after tapping Run it goes through the same run path as the marketplace).

## Workflow

### 1. Check the script
- Check each shot against the latest code: button names, page order, required steps (e.g. the risk disclosure checkbox, backtest must pass before deploying), threshold numbers.
- When editing the script, the operator usually says "just overwrite the original file"; when they only want a proposal they say "give me a proposal first, don't edit the script" — tell these apart.
- When one md contains several cases, split it into single-case files as needed.

### 2. Work backward from the interaction path → storyboard
- List the real path from the code as a table: each screen's title, components, click target, and next screen. Example (mobile, running a strategy):
  `Run → Select Wallet → Next → Configuration (Risk Control drawdown cap / auto-update / check risk disclosure) → Run → success page Running (View Details / Notify me) → Running Strategy Details → back → Strategy tab Running`
- If there's a timeline, go straight to `storyboard.html` (template `assets/storyboard-template.html`), then a per-second schedule; write code only after the operator confirms.

### 3. Specs
| Item | Mobile App | Desktop |
|---|---|---|
| Canvas | Composition 1080×1920, **export 1440×2560 / 60fps** | Composition 1920×1080, **export 2560×1440 / 60fps** |
| UI | 390pt-wide App screen, scaled to **90%** of the frame, margin on all sides, rounded corners + 1px border | 1440×810 web page placed in a **computer monitor** (dark bezel + stand, scale 1.15), font sizes 10–15% larger than the product's original sizes |
| Theme / language | Set by the operator; default **English + the App's default light theme** | Same as left |
| Demo data | 3–4 digit PnL, drawdown <20%, marked as demo | Same as left |
| Opening | 0–3s title card, then the walkthrough | Same as left |

Mobile coordinate system: `K = 1080*0.9/390`, `#app` placed at `left:54px; top:96px`, `transform: scale(K)`. Write all element CSS in **in-App pt coordinates**, rebuilt from the sizes in the code.

Desktop coordinate system: `K = 1.15`, `OX = 132`, `OY = 38` (px position of the screen's top-left corner in the frame), 1440×810 pt. Layout: left sidebar 264 / center column 766 / right Assistant 410, bottom ticker bar 26.

**Desktop must use a computer monitor (set by the operator, 2026-10-15)**: the product UI no longer fills the frame; it sits inside the screen of a computer monitor, with the monitor bezel and stand behind it. Use `assets/pc-monitor-frame.html` directly:
- Structure: `#cam` > `#stand-neck` + `#stand-base` + `#monitor` > `#screen` > `#app`. Monitor outer frame 1684×959.5 at left 118 / top 24, 14px bezel, 26 corner radius; screen 1656×931.5, 12 corner radius; stand centered below the monitor. Background keeps the dark radial gradient.
- The monitor and stand are both inside `#cam`, so they scale up with the UI when pushing in; the cursor and click ripple are also inside `#cam`, positioned with `OX + x*K`, `OY + y*K`. The `camTo` formula doesn't change; only swap the three values `K / OX / OY`.
- The UI is about 14% smaller than when it filled the frame (1.333 → 1.15), so text is a bit smaller in wide shots; the push-ins during clicks and typing make up for it. If the operator finds wide-shot text too small, raise everything one step per the font size spec; do not remove the monitor.
- After the opening title card fades out, the whole monitor (including the stand) fades in from 1.04×.
- Mobile does not get a monitor; keep the current 90% screen with rounded corners and border.

**Font size spec (desktop; the operator, 2026-10-15: "make the font across the whole UI a bit bigger so users can read it on their phones")** — the final video will be watched on phones, so these sizes are the minimum:

| Element | pt |
|---|---|
| Page title (strategy name) | 21 |
| Sidebar nav / tabs / toolbar / buttons / sub-tabs | 16–16.5 |
| Assistant body / user bubble / Choice Box option description | 15 / 15 / 14 |
| Choice Box question / option name | 17.5 / 16 |
| Metric card label / value | 14 / 22 |
| Table / code | 15 / 14.5 (line height 24) |
| Modal title / field label / input, chip, button | 20 / 14.5 / 15.5–16 |

If larger text no longer fits, remove minor small text (e.g. "1,264 Trades" and "684W 580L" in the metric cards); do not shrink font sizes. When placing the mobile screen in a desktop video, use scale 1.2, centered.

**Opening title card (spec of 2026-10-15)**: 0–3s dark background, one large centered headline (Geist 76px / 650, `text-wrap: balance`), words rise in one by one (0.09s apart); at 2.55s the headline scales up and fades out; at 2.75s the product UI fades in from 1.04× back to 1×. The headline copy comes from the operator, e.g. Case 3 "Turn your trading idea into a live strategy.". Implementation: write the walkthrough in `tl` (not paused), use an outer `master = gsap.timeline({paused:true})` for the title, `master.add(tl, 3)`, and register `master`; add 3 to both `data-duration` and the test page's `DUR`.

### 4. Write the composition
Put the project in `$VIDEO_WORKSPACE/hyperframes/<slug>/`:
```
index.html        single composition (data-composition-id="main")
_test.html        test page (copy assets/test-wrapper.html, change DUR and timeline id)
assets/           local gsap, CustomEase, Geist woff2, minara-avatar.png (no CDN dependency)
references/       copies of source assets
audio/            lines.tsv (voiceover copy), vo-placement.tsv (timing)
storyboard.html / _backups/ / output/
```
Core helpers are in `assets/helpers-reference.js` (real code from Case 1):
- `R(el)`: measure the element's in-App pt coordinates **before any movement animation** and store them in `MAP`. All later clicks use these predicted coordinates — measuring after the screen has been pushed out of frame is off by 390pt, and the cursor misses.
- `camTo(t, px, py, s, d)` / `camReset`: camera push-in. When `s>1`, pull the focus point a bit toward the center (desktop: `720+(px-720)*0.75`, same for y) so whole rows aren't cropped; clamp the position inside the frame so nothing outside shows. Use the variable `curS` to track the current scale (`camTo` sets it, `camReset` returns it to 1).
- `curShow / curMove / tap / moveTap`: mobile uses a semi-transparent soft touch point, desktop uses a white arrow cursor; clicks press down + ripple. **When `curS>1`, `moveTap` runs `camTo` to the click target in sync** (duration = move duration + 0.15s), so the frame follows the cursor automatically while zoomed in.
- `pushIn / pushBack`: horizontal page push, 0.45s.
- `splitWords + stream`: AI answers stream in word by word.

### 5. Camera and pacing (rules set from the operator's own words)
- "When the mouse clicks or when typing, zoom in to the area of that specific action, and the frame can follow the mouse; **when it isn't clicking, no need to zoom in**."
- "Make the zoom where the cursor moves more noticeable" (2026-10-15, replaces the old ≤1.25 cap). Desktop scales:
  | Action | Scale |
  |---|---|
  | Typing (input box) | 1.7 |
  | Clicking a button / tab / sidebar | 1.6 |
  | Reading the Assistant chat, Choice Box | 1.5 |
  | Consecutive actions inside a modal | 1.45, following the cursor |
  Mobile Case 1 used 1.25; new mobile videos should also be "noticeable" — confirm the scale with the operator.
- For consecutive clicks (Choice Box options, the Deploy step modals), stay in close-up and follow the whole time; don't pull out and push back in each time.
- When a click leads to a result the viewer needs to see (switching tabs, By symbol / Fills, backtest results appearing, metrics refreshing, toolbar values filled after AI generation), pull back to the wide shot 0.5–0.6s after the click.
- When zoomed in, it's acceptable for a modal's top and bottom edges to leave the frame briefly, but the cursor and the target being clicked must stay in frame, and text must not touch the frame edge.
- "No fancy camera moves needed; the main goal is to show each step clearly"; switch at a normal voiceover pace, with no stuttering.
- No captions in the frame.

### 6. Fidelity checklist (pitfalls from Case 1)
- **Typing effect**: one `<span>` per character, revealed one by one with `tl.set(span,{display:'inline'})`. **Do not** rewrite the whole `textContent` every frame — seeking backward leaves wrong intermediate values (v2 had an extra "C" stacked on the placeholder text).
- Input box line wrap: during setup, reveal characters one by one to measure which character wraps to two lines and how much the height grows; at that moment move the quick-question cards above it up in sync.
- Layering: the quick-question cards must sit above the input box's white background mask; the detail page must cover the tab bar (detail page z-index > tabbar).
- Avoid class name collisions: the text overlay layer uses the `hz-` prefix (`hz-main / hz-note / hz-cta`); it once collided with the run panel's `.cta` and produced a black bar.
- Content after a page switch must not slide under the status bar / top bar; tables must not carry a gray background.
- Always use `immediateRender:false` on `fromTo`, otherwise the first frame is wrong when seeking.
- Frame grabs must cover: before and after every click, mid-typing, the moment of a line wrap, and after every page switch.

**Desktop additions (pitfalls from Case 3)**
- Avoid class name collisions: the model picker in the composer once used `.md`, which collided with the modal's `.md`, and the whole block ended up outside the input box. Modals, text overlays, and components each get their own prefix.
- Give buttons enough width for the enlarged font size (e.g. "Run Backtest" ≥160pt), otherwise the label wraps to two lines.
- In the Assistant, stack bubbles, Choice Boxes, and replies **dynamically** by their real height (during setup, read `offsetTop/offsetHeight`, lay them out in order, and compute the chat scroll y values); do not hard-code top — after a font size change they overlap.
- Elements that follow a toolbar (e.g. the invert score checkbox) are positioned by the previous element's actual width.
- For fields whose value changes via `.flip` (Untitled → V1, 1 → 2, 8 → 3 symbols), stack the old and new values and crossfade with autoAlpha + a small offset; don't rewrite textContent. Same for number refreshes (V1 → V2 metrics).
- Elements that start hidden and appear one by one later (metric cards, treemap tiles, table rows, component chips) must be set to `autoAlpha:0` in setup first, otherwise they flash the moment their container appears.
- Most "content_overlap / text_occluded / contrast" warnings from `hyperframes check` are triggered by modal masks, initial stacked layers, and the product's original colors, and are intentional; structural errors must be 0.

### 7. Test → iterate
- Test page on port 4097 (text overlay version 4098), `python3 -m http.server`; kill the old port before starting a new one.
- The operator marks issues on screenshots → fix them yourself with Edit → confirm with frame grabs → then ask them to look again.
- Frame grabs: `npx -y hyperframes@latest snapshot --at 1.5,4.6,... --no-end --describe false -o <scratchpad>`.

### 8. Text overlay version
- Copy the whole project to `<slug>-huazi/` and leave the original project untouched; share `audio` via a symlink.
- Take the text overlays from the script md, keep only the entries that match the current footage, and match the UI language (English UI → English overlays). In the delivery notes, list a "time / overlay / original script text" mapping table.
- Put the text overlays outside the camera layer (`#cam`) so they don't scale up during push-ins; the main overlay goes in the top margin, small disclaimer text in the bottom margin.

### 9. Voiceover
- Use `minara-voiceover`: cut the recorded narration into the script's lines and place them on the voiceover track. **Do not substitute a TTS voice** for a missing line; ask for a re-record. A temporary local TTS may be used only to measure durations for laying out the visuals; it does not go in the final video.
- After generating, adjust the visuals to the actual durations and add `<audio data-start data-duration data-track-index>`.

### 10. Render and deliver
- **Export 2K 60fps** (see "Video export requirements" at the end): a subagent first renders a 4K 60fps master, then ffmpeg scales it to 2K → `output/<slug>-vN.mp4`, with an incrementing version number and no overwriting.
- After rendering, grab key frames with ffmpeg and check them before delivering; for any version with problems, write "do not use" in the delivery notes.
- Delivery: a table with file path, size, and specs; state whether it has audio and what is still missing. Do not post to the group automatically.

### 11. Cover
Make one when the operator says "封面 / cover / 缩略图"; you can also ask whether they want one when delivering the final video.

- **One command**:
  ```bash
  python3 ~/.claude/skills/minara-usecase-video/scripts/make_cover.py \
    --video output/<slug>-vN.mp4 --at <seconds> \
    --title "<same line as the title card>" --sub "<product location, e.g. Strategy Studio · Desktop / Minara App>" \
    -o output/cover
  ```
  By default it produces `cover-landscape.png` (1920×1080) and `cover-portrait.png` (1080×1920); add `--layouts landscape` when only one is needed. The same folder keeps `shot.png` and `cover-*.html`; for fine-tuning, edit the html directly and rerun.
- **The image comes from the final video itself**: the script grabs a frame from the mp4 as the product screenshot. For mobile videos (portrait), it crops out the App screen automatically; for desktop videos with the monitor, add `--monitor` to crop only the UI inside the screen (the cover adds its own rounded corners and border to the screenshot, so don't include the monitor); older full-frame desktop videos use the whole frame. You can also pass an existing screenshot with `--shot <image> --kind desktop|phone`.
- **Picking the frame**: choose a moment where **the camera is not pushed in** and the result is most complete, e.g. backtest results shown, the strategy already running, the returns card refreshed. First grab 3–4 candidate frames with ffmpeg for the operator to choose from; don't decide yourself. Don't use frames where the cursor covers key numbers.
- **Layout** (fixed; don't redesign it each time): dark background `#0E0F11` with a very faint white radial glow, official logo in the top left (not shipped in this repo: put your dark-mode wordmark at `assets/cover/logo.png` or set `COVER_LOGO`; without it the cover renders without a logo). Title in Geist 650, `text-wrap: balance`, with one line of gray subtitle below. The product screenshot has rounded corners and a border, and deliberately bleeds off the right or bottom edge of the frame. Landscape is text left, image right; portrait is text on top, image below.
- **Copy**: the title defaults to **exactly the same words** as the video's opening title card; the subtitle only states the product location, with no selling points. Only these two lines of text and the logo appear on the cover; no extra badges, buttons, arrows, or "NEW" tags.
- **Data**: returns and drawdown shown in the screenshot must also pass the max drawdown >20% check; don't put return numbers in the title.
- **Delivery**: after generating, look at both images yourself with Read, confirm the title doesn't break into an orphan word and the screenshot isn't covered by the logo or title, then deliver with the paths listed. Do not post to the group or upload automatically.

## 📦 Video export requirements: 2K 60fps (set by the operator, 2026-10-16; applies to all final mp4s)

- **All final videos are 2K 60fps**: landscape **2560×1440**, portrait **1440×2560**; H.264 + AAC, `yuv420p`, `+faststart`. Put this in the "Specs" column of the delivery table.
- **Keep writing the composition at 1920×1080 / 1080×1920**; don't change coordinates or font sizes. Resolution is raised only at export.
- HyperFrames `--resolution` only supports integer multiples (1080p / 4K) and **has no 2K preset**, so do it in two steps:
  ```bash
  # 1) 4K 60fps master (use portrait-4k for portrait)
  npx -y hyperframes@latest render -c index.html -q high --fps 60 --resolution landscape-4k -o output/<slug>-vN-4k.mp4
  # 2) lanczos downscale to 2K (portrait: scale=1440:2560)
  ffmpeg -y -i output/<slug>-vN-4k.mp4 -vf "scale=2560:1440:flags=lanczos" \
    -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart output/<slug>-vN.mp4
  ```
  Do not upscale 1080p directly to 2K (it looks soft).
- **Check with ffprobe before delivery**: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 <mp4>` must return `2560,1440,60/1` (or `1440,2560,60/1`). The `-4k` master is an intermediate file and is not delivered.
- The test page scrubber and timecode still read at 30fps (for communication); this does not affect the export frame rate.
