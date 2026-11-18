---
name: minara-video
description: The operator's standard workflow for making Minara marketing / launch / demo videos. Built on the hyperframes skill, with a stricter process - confirm style → high-level storyboard → copy → build each scene separately → confirm a per-second script → iterate on a local test page → render only once the user is satisfied. Product screens are rebuilt in HTML, with screen recordings / screenshots used only as reference; recording frames never go into the film.
---

# /minara-video

> ## 🅖 Font rule: every Minara video uses **Geist** for all text
> Titles / body / numbers / buttons / tables - **all of it** uses `font-family: 'Geist', system-ui, -apple-system, sans-serif`.
> **No Inter, no serif of any kind, and no system default font that falls back to serif.**
> Loading: `@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&display=swap')`; pair numbers with `font-variant-numeric: tabular-nums`.
> Write both CSS selectors, `#root, [data-composition-id="root"] {}`, or font-family will not apply and the page inherits the browser's default serif (see item 1 of "Composition structure pitfalls").
> Not negotiable and not optional, unless the operator **explicitly says "换字体" (change the font) for that job**. (Set by the operator 2026-06-24; promoted to the top rule 2026-06-26.)

This is the operator's standard operating procedure for Minara videos, distilled from the problems hit while making the Strategy Studio public release video on 2026-05-26 ~ 27.

> **⚠️ Route first: this is the workflow for HyperFrames composited motion videos (marketing / launch / demo, where every frame is built in code).**
> If the task is a **product guide / tutorial video** - the operator **records the screen themselves** and you only add voiceover + captions and deliver - use the **`minara-guide-video`** sub-skill, not this one. How to tell: is there an existing screen recording / is the ask "add voiceover and captions to this recording"? The two differ in voice, captions, and delivery.

## Compliance: never say "invest"

Do not use **invest / investing / investor(s) / investment(s)** (or **投资 / 投资者** in Chinese copy) anywhere in the copy this skill produces: scripts, voiceover, on-screen text, titles, subtitles, descriptions, tags, posts, replies, emails, CTAs, alt text. The word can read as investment advice and creates compliance risk. Say what the user actually does instead:

- "Ask Minara how to trade NVDA after earnings", not "invest in NVDA"
- "Ask which stocks look undervalued", not "find stocks to invest in"
- "traders" / "users", not "investors"; "trading ideas" / "market analysis", not "investment ideas"
- Risk lines say "Not financial advice", not "not investment advice"

The only exception is a third-party proper noun cited as a source (for example a company's "Investor Relations" page in a citation link). Never use the word in Minara's own voice. Check the final copy for these words before handing it over.

## ⛔️ Startup prerequisite: load HyperFrames + video-shotcraft (mandatory)

**As soon as this skill starts, use the Skill tool to invoke the `hyperframes` skill so all of its composition rules are in context, then read the local `video-shotcraft` shot library entry point in full, and only then continue with the workflow below.**

- This is a hard prerequisite, not optional - `minara-video` is only a stricter workflow wrapper; the actual composition syntax / timeline / render rules all live in `hyperframes`. Writing scene HTML without loading it will hit known problems (timeline paused, `window.__timelines` registration, no `Math.random()` / `repeat:-1`, etc.).
- Even if hyperframes was already used earlier in this session, invoke it again when starting `/minara-video` so the rules are in the current context.
- Load order: `Skill(hyperframes)` first → **then read `$VIDEO_WORKSPACE/video-shotcraft/SKILL.md` in full** → **then `Read $BRAND_DIR/design.md` (Minara v2 visual system)** → then read the fixed style rules → then follow the workflow below.
- **You must read `$BRAND_DIR/design.md` (mandatory; lesson from 2026-06-24)**: this is the official Minara v2 visual system and the **source of truth for color values, type scale, spacing, corner radius, cards, and layout**. This skill's fixed style rules are the "video mood layer"; design.md is the "design token source of truth" - both must be in context. ⚠️ The brand gradient listed in design.md, `#EB53FF/#FF538E/#FF9A32`, **is not used in videos** (removed by the operator 2026-09-02; see the fixed style rules below). Take only its black/white/gray tokens, semantic colors, typography scale, and 4pt spacing.
- **Load the brand asset folder `$BRAND_DIR/logo/` by default (set by the operator, 2026-06-24)**: when you need a logo / avatar / wordmark, **use the official assets here first; do not draw your own SVG as a substitute**. Current inventory (run `ls` first to check; it may change):
  - `Minara Avatar.png` - **Minara black-and-white pixel avatar** (girl with glasses, halftone); the default for the round logo in endings.
  - `Minara Logo.png` - Minara primary logo mark.
  - `MInara Text Logo Light.png` / `MInara Text Logo Light Dark.png` - text wordmark (light / light-and-dark versions).
  - `Minara Avatar Japan.png` - avatar variant for the Japan market.
  - `128_128.png` - small square icon.
  - `minara X banner.jpeg` - X banner.
  - Usage: `cp` the assets you need into the project's `assets/` and reference them in HTML with `<img src="assets/xxx.png">`; HyperFrames inlines local images at render time. When self-verifying with screenshots, also `cp` a copy into `/tmp/<test-dir>/assets/` (relative paths only resolve that way).

### 🎬 video-shotcraft local shot library loading rules (2026-07-21)

- **Fixed local library path**: `$VIDEO_WORKSPACE/video-shotcraft/`. Every time `/minara-video` starts, read its `SKILL.md` in full. Do not use it based only on card names or memory.
- **The fixed method for translating cards** is in "Client 'growing / self-writing' shot lessons § B" below (card frames × TEMPO, clip-path instead of paper-color masks, PageCam2D baked into keyframes, zoom ≥ 1, focus clamped to the canvas).
- **Its default role is a reference library; it does not switch the tech stack automatically**: `minara-video` still centers on HyperFrames' seek-safe compositions, per-scene previews, and render flow; `video-shotcraft` supplies shot language, camera-move recipes, pacing structures, sound design, approved demos, and assets. When adopting one of its Remotion implementations, first translate the method into a deterministic, seekable HyperFrames timeline. Do not copy `Date.now()`, `Math.random()`, or non-seek-safe animation directly.
- **Do not trigger the standalone skill's template prompts**: when loading this library inside `/minara-video`, do not ask each time whether to use Ink Press, and do not interrupt the locked Minara workflow above because of it. Only when the operator explicitly names `Ink Press` or `Remotion`, or asks to replicate that template, read `template/TEMPLATE.md` in full and switch to the template route.
- **Read the source of truth for any shot card you use**: once you decide to use a shot card, read `references/shots/<card-name>.md` and the matching `demos/<card-name>/` implementation source in full; read `references/sequences/` when you need whole-film structure, and `references/sound-design.md` and `assets/audio/ATTRIBUTION.md` when you need sound. Do not load all 106 cards into context at once.
- **Copy only the assets you need**: copy from `assets/lib/`, `assets/audio/`, or `demos/` into the current video project; do not let the project depend on this library's relative paths at runtime. When using audio, keep and check the license attribution.

### 🧰 Remocn local Remotion component library rules (2026-08-13)

- **Fixed local library path**: `$VIDEO_WORKSPACE/remocn/`. It is a shadcn-style copy-paste component library for Remotion, not a HyperFrames plugin and not a runtime dependency of video projects.
- **Load on demand; not part of every startup**: only when the storyboard needs a ready-made Remocn motion / transition / UI simulation, or the operator explicitly names `Remocn` / `Remotion`, read the local `skills/remocn/SKILL.md` in full. For a full film, then read `skills/remocn/references/anatomy.md` and the matching `references/archetypes/<type>.md`; do not load every archetype at once.
- **HyperFrames remains the default stack**: in ordinary `/minara-video` jobs, treat Remocn only as a shot / motion reference, and translate the chosen component's motion logic into a seekable, deterministic HyperFrames GSAP/DOM timeline. Do not put React/Remotion TSX directly into scene HTML, and do not switch stacks just because a ready-made component exists.
- **Use it directly only when Remotion is explicitly chosen**: in an existing Remotion project, if `components.json` is missing, run `npx shadcn@latest init` first; then install only the components the storyboard selected: `npx shadcn@latest add @remocn/<name>`. shadcn resolves dependencies recursively; modify the code after it is copied into the current project. Do not install-all, and do not let the final film reference the local Remocn repo path.
- **Component parameters follow the live docs**: first read `https://remocn.dev/llms-components.txt` to filter, then read the specific `.../<component>.md` page the table points to; do not guess props, defaults, or durations. To investigate an implementation, go back to the local library's `registry/` source and `content/docs/`.
- **Adapt to Minara rules; do not copy the default look**: Remocn's shot structure, motion, and timing can be reused, but the font must be changed to Geist, and color, type size, information density, the signature ease, and ≤0.5s transitions still follow this skill's rules. `Length` in the Remocn docs is the frame where the component's own action ends, not the total scene duration; add hold time per the per-second script. Its default `1280×720 @ 30fps` also does not override the current Minara project's output spec.
- **Distinguish the two API types**: the animation tier is frame-driven and accepts `speed`; `remocn-ui` primitives are timeline state-driven and have no `speed` prop. Both must be reproducible frame by frame, and `Math.random()` / `Date.now()` / interval-driven animation is still forbidden.

### 📸 snapcn local Remotion product-demo component library rules (2026-09-04)

- **Fixed local library path**: `$VIDEO_WORKSPACE/snapcn/` (GitHub `snapcndev/snapcn`, MIT). Same kind of thing as Remocn - a shadcn-style copy-paste component library for Remotion - but **focused on software product demo shots**: AI chat flows, prompt input, terminals, device frames, captions. It is not a HyperFrames plugin and not a runtime dependency of video projects.
- **Division of labor with Remocn**: Remocn leans toward general motion / transitions / archetypes; snapcn leans toward "**putting product UI in the shot**". Minara is an AI trading copilot, so snapcn's **AI Chat Input** group (`search-typing` / `prompt-zoom` / `answer-stream` / `prompt-send` / `answer-highlight` / `agent-steps`) and **Screens & Devices** group (`phone-frame` / `laptop-frame` / `terminal-simulator` / `screen-recording` / `cursor-track`) are the preferred references. For scenes like "Prompt Your Strategy", Copilot answers, or Autopilot execution steps, **look here first**.
- **Load on demand; not part of every startup**: only when the storyboard needs the product demo shots above, or the operator explicitly names `snapcn` / `Remotion`, read the local `skills/snapcn/SKILL.md`. Pick components via the routing table at `skills/snapcn/references/components/index.md` (with Use for / Avoid for / Length / Vibe), and **open only the selected `references/components/<name>.md`**; do not read them all. For film structure, refer to `references/anatomy.md` (Hook → Positioning → Product reveal → Features → Proof → CTA) and `references/archetypes/`.
- **HyperFrames remains the default stack**: in ordinary `/minara-video` jobs, treat snapcn only as a shot / motion / timing reference, and translate the chosen component's motion logic into a seekable, deterministic HyperFrames GSAP/DOM timeline; for implementation details look at the `registry/snap-cn/<name>/` source. Do not put React/Remotion TSX directly into scene HTML, and do not switch stacks just because a ready-made component exists.
- **Use it directly only when Remotion is explicitly chosen**: `npx shadcn@latest add @snapcn/<name>` (`@snapcn` is already in the shadcn registry directory, so no registries config is needed). The Remotion project needs a `components.json` first, and the `@/` alias configured in both `tsconfig.json` **and** `remotion.config.ts` - the Remotion bundler does not read tsconfig paths. Install only the components the storyboard selected; do not install-all; the final film must not reference the local snapcn repo path.
- **Component parameters follow the docs**: live docs at `https://snapcn.dev/llms.txt` (full version `llms-full.txt`); do not guess props / defaults / durations. `Length` is the natural frame length of the component's own action (e.g. `answer-stream` 150f, `search-typing` 420f), not the total scene duration; add hold per the per-second script. Under budget gets truncated; over budget is dead air.
- **Three rules worth adopting directly** (they already point the same way as this skill's rules): ① the **camera model** in `MOTION.md` - shots are not cuts but one virtual camera dollying / craning through the same world: outbound move fast 8–14f + landing spring settle 10–16f + text hold 30–45f, the same origin as this skill's "camera push-in follow" recipe; ② the **anti-AI-slop defaults** in `skills/snapcn/references/design.md` - no decorative letter-spacing, no all caps, no gradient text, no glow shadows, consistent with the 2026-09-02 gradient removal; ③ **scale text with the baseline as pivot + `text-rendering: geometricPrecision`**, which cut jitter from 0.284px to 0.014px (the `motion-quality` rule); use it for large-text scaling animations.
- **Adapt to Minara rules; do not copy the default look**: the font must be changed to Geist; color, type size (large UI readable on phones), information density, the signature elastic ease, and ≤0.5s transitions still follow this skill's rules. Its default `1280×720 @ 30fps` does not override the current Minara project's output spec.
- **Distinguish the two API types**: the `snapcn` animation tier is frame-driven and has `speed`; `snap-cn-ui` primitives (`input` / `caret`) are timeline state-driven and have no `speed`. Both must be reproducible frame by frame; cursor blink uses `Math.floor(frame/15) % 2`, terminal scrolling steps rather than eases, and `Math.random()` / `Date.now()` / interval are still forbidden.

## 🎵 All music and sound effects go through `/minara-music` (2026-10-14)

After the per-second script is confirmed, use the `minara-music` skill to write each section's mood and on-screen actions into `cues.json`. Show the operator the cue sheet first; after it is confirmed, render BGM + SFX locally (when there is a voiceover, also output a ducked version). Do not download music from the web on a whim.

## 📱 UI scene rule - large UI, minimal, do not copy the product (set by the operator, 2026-07-03; global)

When a "product interface" appears in a video, **do not copy the product UI pixel for pixel**. Product screenshots and screen recordings are only a **content reference** (what data and features exist); redo all of the visuals in HTML (see the 🎞️ rule below - no recording frames or screenshots in the film):

- **Large UI**: design for **watching the video on a phone** - viewers watch on a small screen, where small text and dense grids are unreadable. Body ≥28px, titles ≥48px, key numbers huge (80-140px), at most 3-5 elements per screen.
- **Simple, spacious, minimal, clean**: cut secondary details from the product (small labels, dense columns, helper rows, clusters of small icons). One card says one thing; leave plenty of whitespace.
- **Font is always Geist** - whatever font the product interface uses (even if the product hero is serif), the video uses Geist throughout. This echoes the font rule at the top.
- Source: the 2026-07-03 SS2.0 copy-trading video, where I copied the Studio web UI (small text, dense tables + PT Serif hero) and they threw it all out and had it redone.

## 🎞️ Screen recordings are reference only - rebuild every product screen in HTML (set by the operator, 2026-11-13; global)

Use the operator's screen recordings and screenshots to learn **what the product does** - the real flow, layout, UI copy, states, data and timing. **Never put a recording, a frame grabbed from it, or a screenshot into the final film.** Recording frames are not sharp enough for a 2K / 4K export (compression blur, small text, scaling artefacts) and they break the Minara film look. Every product screen in the film is rebuilt in HTML / CSS in the composition.

**What the recording is used for**

| Take from the recording | How it goes into the film |
|---|---|
| Steps and their order, what is clicked / typed | The scene order and the actions in the per-second script |
| UI copy (buttons, labels, messages) | Typed into the HTML word for word (check against the frontend code / i18n when available) |
| Layout and components (where things sit, what appears after what) | Rebuilt as DOM in Geist, then simplified per the 📱 UI scene rule (large UI, 3-5 elements per screen) |
| States and data (loading, streaming answer, filled form, result numbers) | Real values rebuilt as text / SVG / CSS; charts redrawn as SVG paths |
| Rough timing (how long the agent thinks, when the result shows) | A starting point for the per-second script; compress or stretch for pacing |
| Icons, logos | Use the real SVG / PNG asset files (brand folder, product repo, FMP stock logos), never a crop from the recording |

**How**

1. **Collect.** Ask for the recording(s) at the start if the film shows product UI. Keep them in `<project>/references/recordings/`, never in `assets/`.
2. **Extract reference stills.** Use the frame extractor from `minara-usecase-points`:
   ```bash
   python3 -I <minara-usecase-points skill>/scripts/extract_frames.py <recording.mp4> <project>/references/frames
   ```
   It writes one still per scene change plus `contact.png` and `index.tsv` (time of each still). Read the contact sheet, then the stills you need.
3. **Write down what each screen shows** (copy, components, states, numbers) next to the storyboard row / per-second script it belongs to. Note anything unreadable in the recording and check it in the code or ask - do not guess blurry text.
4. **Rebuild in HTML** in Step 5. Sharp vector type and shapes at any zoom, so camera push-ins stay crisp.
5. **Check side by side** on the test page: rebuilt frame next to the reference still at the same moment - same flow, same copy, same states; the look follows the Minara film style, not the recording's pixels.

**Not allowed in the final composition**

- `<video>` / `<img>` / CSS `background-image` pointing at a recording, a frame from it, or a product screenshot (including blurred or dimmed "background" use, picture-in-picture and device-frame fills).
- Tracing text or numbers you could not read in the recording.
- Exception: only when the operator explicitly asks for real footage in that job (e.g. "这段用录屏"). Say in the plan which shot uses it and why.

**Before render**, search the project for media references and make sure none point at `references/`, a recording or a screenshot:
```bash
grep -rnoE '(src|href)="[^"]+\.(mp4|mov|webm|png|jpe?g|webp)"|url\([^)]+\)' <project>/*.html | grep -vE '["(]\.?/?assets/'
grep -rn 'references/' <project>/*.html
```
Anything left must be an asset made for the film (logo, avatar, icon, generated texture), not product footage.

## 🚫 Visual storytelling rule - no stray text (set by the operator, 2026-07-03; global)

**These are videos that tell the story through images. Apart from lines / titles the operator explicitly asked for, no words, labels, or explanatory text should pop up anywhere in the film.** To explain a concept, use imagery (objects, actions, metaphors, color, motion), not on-screen text.

- Allowed text: ① lines that match the voiceover / captions; ② titles / CTAs / numbers the operator explicitly asked for (e.g. "Introducing Strategy Studio 2.0", the closing CTA).
- **Not allowed**: "annotation words" added to the picture, turning every noun mentioned in the voiceover into floating text (e.g. alpha / craft / capital - show "craft" with ore being carved into a diamond and "capital" with money flying in, rather than putting three words on screen), decorative keywords, feature-label walls.
- How to judge: is this word "a line / copy they asked for", or "an explanation I wanted to add"? Delete all of the latter and express it visually instead.
- Source: set on 2026-07-03 when they cut the `alpha · craft · capital` three words I had added on my own in scene2.

## 🔒 Fixed style rules (load every time; not optional, not negotiable)

> Explicitly set by the operator on 2026-06-22 as the default style baseline for every Minara video. Unless they **explicitly say "换风格" (change the style) for that job**, always follow this, and **do not ask about style each time**.

**Font is always Geist (not negotiable). Minara brand colors, clean, modern, lively, top-tier Silicon Valley motion; all motion has physical acceleration and deceleration, easing in and out.**

> The original 2026-06-22 wording also included "warm". **On 2026-09-02 the operator explicitly removed the cream warm background + the brand purple-pink-orange gradient**, and "warm" was removed from the execution items along with them.

In practice:

- **Font = Geist (rule; set by the operator, 2026-06-24)** - all text (titles / body / numbers / buttons) uses `font-family: 'Geist', system-ui, -apple-system, sans-serif`. **No Inter / no serif of any kind.** Load Geist via Google Fonts: `@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&display=swap')`, and still pair numbers with `font-variant-numeric: tabular-nums`. Do not use anything else unless they explicitly say to change the font for that job.
- **Minara brand colors** - green `#07B56A` (up / **success semantics**), red `#F75D5F` (down), dark gray `#222222`/`#15171A`, white `#FFFFFF`, light gray `#B0B0B0` (secondary text). Use semantic colors (green/red/blue/orange) only when they carry meaning, not as decorative emphasis.
- **No cream warm background, no brand purple-pink-orange gradient (removed by the operator, 2026-09-02)** - backgrounds no longer default to cream / warm light gradients; CTAs, emphasized title words, shine sweeps, and frosted overlays **do not use** the `#EB53FF → #FF538E → #FF9A32` gradient. For emphasis, use font weight, type size, whitespace, and lightness contrast. Do not add either of these back unless the operator explicitly specifies it for that job.
- **Clean** - one focal point per screen, plenty of whitespace, no piling up of elements; short text, large type.
- **Modern** - Geist (numbers with `tabular-nums`); rounded corners, soft shadows, restrained strokes.
- **Lively** - elements breathe, have slight overshoot/rebound (`back.out`), and enter staggered; no stiff linear translation.
- **Top-tier Silicon Valley motion** - transitions have layers (push/parallax/masks), details have micro-interactions (touch ripple, button press-down, glow sweep).
- **🌀 Signature elastic ease (the hardest rule; set by the operator, 2026-07-03; applies to all animation)** - in Minara videos, **all** translation / scaling / fades / drawing / count-ups / camera push-pull use the default easing curve **`cubic-bezier(0.95, 0.03, 0, 0.98)`** (a Custom bezier the operator set in Figma; see the dedicated section below). This is an **extreme ease-in-out**: a long stretch at the start with almost no movement (building up) → a sudden high-speed rush through the middle → a gentle settle at the end. It gives a "taut, crisp, springy" feel (they call it "弹性动效" (elastic motion), but it is **not** rebound/bounce - both Y control points are within [0,1], no overshoot). **No `linear`/constant speed.** Unless they explicitly say to change it for that job, all motion defaults to this curve; do not use `power2/power3` anymore.
  - Elements that need a "pop" feel (logo entrance, success check, chips) may layer a bit of `back.out` overshoot on top of this base, but **the base rhythm must be the signature curve**; do not revert the whole film to power3.
  - Accelerating exits / quick-cut endings may still use `power2.in`; special cases like infinitely looping glow sweeps may use `linear`.
- **All transitions ≤ 0.5s (rule; set by the operator 2026-06-25; fixed, not negotiable)** - any transition between sections / acts (previous section out + next section in, push-pull cut, fade cut, mask wipe) has a **total duration ≤ 0.5 seconds**, clean and quick. ⚠️ Distinction: continuous camera motion within a single scene (slow push / slow pull / pan / dolly follow) **is not a transition** and can be as long as it needs; only the switch "to the next piece of content" is bound by the 0.5s cap.

## 🌀 Signature elastic ease - implementation details (required in every film)

> The Custom bezier the operator fixed in Figma on 2026-07-03: **`0.95, 0.03, 0, 0.98`** (the "Curve" tab, not "Spring"). Source: the `跟单milestone视频` (Strategy Studio 2.0) project. This is the **default motion curve** for Minara videos and applies to all animation.

**Curve shape**: long flat start (P1=`0.95,0.03` pulls the handle to the bottom right → slow, building start) → steep middle (instant high speed) → flat end (P2=`0,0.98` pulls the handle to the top left → gentle settle). Extreme ease-in-out, **no overshoot** (both Y values within 0–1). Feel: "tense for a beat, whoosh across, settle firmly". Typical duration **0.8–1.1s** (in their demo video, a vertical bar grows into place in about 1.0s).

**GSAP usage** (the default animation engine in HyperFrames) - register once with `CustomEase` and reuse it across the film:
```js
gsap.registerPlugin(CustomEase);
CustomEase.create("minaraSnap", "M0,0 C0.95,0.03 0,0.98 1,1"); // = cubic-bezier(0.95,0.03,0,0.98)
// After this, every tween uses it by default:
gsap.defaults({ ease: "minaraSnap", duration: 0.9 });
// Or per tween: tl.to(el, { y:0, opacity:1, ease:"minaraSnap", duration:1.0 }, T)
```
- CustomEase CDN: `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/CustomEase.min.js` (the compiler inlines it at render time; include it together with gsap.min.js).
- For groups of entering elements, use `gsap.set(...opacity:0,y:24)` + one `tl.to(...ease:"minaraSnap")` per element (**do not use a staggered `from`**; under seek rendering it gets the first element stuck - see "Composition structure pitfalls").

**CSS usage** (test pages / pure CSS transitions):
```css
transition: all 1s cubic-bezier(0.95, 0.03, 0, 0.98);
```

**Verification page**: `scratchpad/_ease-verify/index.html` (draws the curve + a vertical bar growing along it, for visual comparison against their `弹性动效示范.mp4`).

## ⚠️ Business constraints (must check whenever strategies are shown)

> Any time strategy-related content appears in a video - backtest curves, return cards, metric numbers, Strategy Trades tables, anything showing "how this strategy performs" - it must pass this business check, not just look good.

- **If max drawdown > 20%, you must flag it to the operator.** When preparing to show a strategy's data in a video, check its max drawdown first: if it exceeds 20%, **stop and tell the operator clearly**: "This strategy's max drawdown is X%, above 20%. Confirm you want to show it / or should we use a different one?" Continue only after they confirm. Do not quietly put a high-drawdown strategy in the video.
- Reason: showing high-drawdown strategies in external marketing / launch / demo videos misleads LPs and damages trust and compliance (per Minara's trust positioning with high-net-worth LPs). Drawdown is one of the metrics LPs are most sensitive to.
- How to flag: state the number + risk directly in the conversation and give them the choice (change strategy / adjust the time period / keep showing it); do not decide for them.

## Core principles (unchanged)

1. **Always build scene by scene; never one 50s composition**. Each scene is one `.html` file rendered to its own mp4, and the operator cuts them in a video editor. Even if the final video plays as one continuous piece, the project is still N separate scene files.
2. **Generate a storyboard board first for any video project**. If a timeline already exists, generate it directly without asking; if there is no timeline, first ask the operator: "This video doesn't have a timeline yet. Do you want me to generate a storyboard board first?" Skip the HTML board only if they explicitly say no.
3. **Always confirm the per-second script before writing code**. Changing durations / adding sections / removing sections / reordering → the first response is a timeline markdown table, **not** HTML or a subagent call.
4. **Always start a local test page for the operator to review**. Do not render an mp4 directly for them to review - it wastes time; each render takes at least 20-60s. The test page uses a python http server + a wrapper with Play / Reset buttons.
5. **Keep revising the local page until they explicitly say "渲染 / OK / 满意" (render / OK / satisfied)**. They may change CSS / copy / timing 5 times; do all of it on the test page.
6. **Make small changes yourself with Edit; do not use a subagent**. Only `npx hyperframes render` uses a subagent.
7. **After every element edit you must kill the server + reload Chrome + restart the server** (Studio caching is severe).
8. **Run only one dev server at a time; kill the old port before starting a new one**. The operator's laptop overheats.

## Workflow (follow in order; do not skip steps)

### Step 0 - Project directory

Video projects all live in `$VIDEO_WORKSPACE/hyperframes/<video-slug>/`.

- Slugs use hyphens (`minara-strategy-studio-public`, `silver-launch`), no spaces
- No need for `npx hyperframes init` - just `mkdir + write scene html`
- One html per scene: `scene1-preview.html`, `scene2-preview.html`, `opening.html`, etc.

### Step 0.5 - Storyboard board (first, for every video)

First decide whether the project already has a usable timeline (timecodes from the user, script sections, an existing storyboard / shot list all count):

- **Timeline exists**: do not ask; immediately copy `assets/storyboard-template.html` to the project root as `storyboard.html`, replace the template placeholders with the real project name, total duration, scene count, and slug, and fill each section into the `scenes` array.
- **No timeline**: ask only one question: "This video doesn't have a timeline yet. Do you want me to generate a storyboard board first?" If they say yes, generate it right after the high-level storyboard is set in Step 2; skip the HTML board only if they explicitly say no.

Fixed requirements for the board:

- Table layout, one row per scene; list scene number, time / duration, rough visuals, and AIGC / MG type.
- On the right of MG rows, place, in order, a large "开始" (Start) button, `✅`, `🙅`, and an "打开本地文件" (Open local file) button. Clicking "开始" once turns the whole row blue and changes the label to "取消" (Cancel); clicking again restores pending review. `✅` can override the in-production state and turn the whole row green.
- AIGC rows are grayed out by default, and the production button becomes a non-clickable "同事制作" (made by a colleague), meaning another colleague is responsible for that segment; `✅` / `🙅` remain for review.
- Review decisions are saved to the browser's `localStorage`, and a "复制审阅结果" (Copy review results) summary button is kept.
- Pure HTML; no embedded player and no images / audio / video or other media.
- The storyboard only confirms the high-level shots; it does not replace the per-second timeline confirmation in Step 4.
- Before delivery, check it once with a 1600×1000 headless browser screenshot; return only the local file path and do not open Finder automatically.

### Step 1 - Style (locked by default; do not ask again)

The style baseline is the **🔒 Fixed style rules** above, applied by default every time - **do not ask the operator "what style do you want"** again unless they explicitly say "换风格" (change the style) for that job. Reading design.md (if it exists) is only to check for project-level overrides. Minara default palette:

| Use | Value |
|---|---|
| Background (primary) | `#000` or `#222222` (dark gray, commonly used by the operator) |
| Background (secondary / cards) | `#222222` |
| Primary text | `#FFFFFF` |
| Secondary text | `#B0B0B0` |
| Minara green (up / positive PnL / brand) | `#07B56A` |
| Red (down / negative PnL) | `#F75D5F` |
| Font | **Geist** (weights 500/700/800) - rule; no Inter / serif |
| Number font | Geist + `font-variant-numeric: tabular-nums` |

**Do not proactively suggest or change this palette** unless the operator explicitly says "换风格" (change the style). If you see them using pure black `#000` on a hero card / panel / card but wanting it "a bit grayer", change it to `#222222` by default. **Do not add a cream warm background or the brand purple-pink-orange gradient** (removed 2026-09-02).

### Step 2 - High-level storyboard

Ask the operator for the total video length + roughly how many sections. They may give you the sections directly, or ask you to propose them.

If Step 0.5 already generated the board from an existing timeline, this step only revises it based on their `✅` / `🙅` feedback; do not ask again about known sections. If the project had no timeline and they chose to have a storyboard, generate `storyboard.html` right after the high-level storyboard is confirmed in this step, then move on to copy.

Output a markdown table in this format:

```markdown
## <video-slug> high-level storyboard

| Scene | Duration | Content summary | File name |
|---|---|---|---|
| 1. Opening | 3s | Minara logo + tagline entrance | opening.html |
| 2. Prompt input | 9s | User types prompt + assets scroll | scene1-preview.html |
| 3. UI demo | 15s | Strategy Studio main interface, four-phase showcase | scene2-preview.html |
| 4. Asset grid | 21s | 8 asset cards + Optimize button | scene-asset-grid-optimize.html |
| 5. Backtest | 15s | Code stream → Backtest → 3 time-period cards | scene-backtest-preview.html |
| 6. Trades | 3s | Strategy Trades table | scene-trades-preview.html |
| 7. Deploy | 13s | Hero wallet → wallet wall | scene6-preview.html |

**Total ~79s**; the operator edits the pacing themselves.
```

Have them confirm. They may adjust durations or add / remove scenes.

### Step 3 - Copy

For each scene, collect / confirm the exact copy: titles, subtitles, button text, numbers in tables, card names, etc. Collect it all at once before starting to write code.

**Common Minara copy principles** (from the operator's repeated revisions):
- PnL / return numbers: three or four digits, `+$345` / `+$574` / `+$1,250`; no five digits (layout breaks)
- LONG / SHORT must be color-coded (green / red)
- Asset card text 32-46px, symbols at 800 weight
- Wallet account balances mostly four digits ($1500-$9500); avoid five digits

### Step 4 - Per-second script (per scene)

**This step is the key one**; skipping it wastes 5-10 minutes on repeated renders.

For each scene, first output a markdown timeline that states what happens in each segment + its duration. Example:

```markdown
## scene-backtest timeline

| Time | Content |
|---|---|
| 0–0.4s | Title "Codes" enters |
| 0.4–6.0s | Code streams in character by character (Pine script style) |
| 6.0–7.5s | Backtest button appears + mouse click |
| 7.5–8.0s | Phase 1 fade out |
| 8.0–9.5s | Three time-period cards (30D/90D/1Y) enter + curve stroke reveal |
| 9.5–15s  | Metric text fades in + static hold |

**Total 15s**. Confirm OK and I'll start writing the HTML.
```

Do not touch the keyboard until they explicitly say "OK / 开始 / 写" (OK / start / write). If they question a segment → revise that segment and post it again.

### Step 5 - Write the scene HTML

The template goes in `references/scene-template.html` (to be added; for now refer directly to existing scene files).

Key HyperFrames composition rules (see the `hyperframes` skill for details):

- product screens are rebuilt as DOM / SVG from the reference stills in `references/frames/`; never `<img>` / `<video>` a recording or screenshot (see the 🎞️ rule)
- `<div data-composition-id="root" data-width="1920" data-height="1080" data-start="0" data-duration="<seconds>">`
- timeline `paused: true`
- register `window.__timelines["root"] = tl`
- do not use `Math.random()`; use mulberry32 + a fixed seed
- no `repeat: -1`
- do not use `<br>`; rely on max-width for natural wrapping (except short titles)
- use `font-variant-numeric: tabular-nums` to lock number widths
- load scripts with `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js">`; the compiler inlines it at render time

### Step 6 - Local test page

After each scene is written, **immediately** start a test page for the operator to review; do not render directly.

**Mandatory flow**:

```bash
# 1. Kill the old port (avoids laptop overheating / port conflicts)
lsof -ti:4097 | xargs kill -9 2>/dev/null; true

# 2. Copy to /tmp and add the test wrapper
mkdir -p /tmp/hf-<scene-name>-test
cp "<scene-html-path>" /tmp/hf-<scene-name>-test/index.html

# 3. Add the test wrapper in the /tmp copy:
#    - a 40px control-bar at the top with ▶ Play / ↺ Reset buttons
#    - a .stage-frame container + transform: scale() to fit the window
#    - tl.play() at the end of the script to auto-play once
#    See references/test-wrapper.md for the detailed wrapper template

# 4. Start the server
cd /tmp/hf-<scene-name>-test && python3 -m http.server 4097 &>/tmp/hf-test.log &
sleep 1 && open "http://localhost:4097/"
```

**Why the wrapper is required**: the timeline of a HyperFrames composition html is `paused: true`, so opening it directly in a browser shows a pure black screen. A test page must:
- transform-scale to fit the window (1920×1080 has to shrink on a small screen)
- auto-play once
- have Play / Reset buttons for repeated viewing

**Port allocation habit**: pick anything between 4091-4099, one per scene, to avoid conflicts. Always kill before starting a new one.

**🎚️ The test page must have a timeline scrubber (set by the operator, 2026-07-03; rule)**: Play/Reset alone is not enough - the operator needs to **drag to a specific frame**, stop on any frame, and screenshot it to mark "this frame is the problem". So every test wrapper gets a draggable timeline + timecode/frame-number readout (30fps). This is **essential for communication**, not optional.

Implementation (the wrapper is an iframe pointing at scene.html, and gets the GSAP timeline via `iframe.contentWindow.__timelines.root`):

```html
<!-- control bar + timeline -->
<button onclick="play()">▶</button><button onclick="pause()">⏸</button><button onclick="reset()">↺</button>
<span id="stat">--</span>
<button onclick="step(-1)">◀帧</button>
<input type="range" id="seek" min="0" max="1000" value="0">
<button onclick="step(1)">帧▶</button>
<script>
var FPS=30, DUR=10.5, dragging=false;               // DUR is overwritten by tl.duration() once ready
function tl(){ try{return frames.fr.__timelines.root;}catch(e){return null;} } // or iframe.contentWindow
function fmt(t){var f=Math.round(t*FPS);return (''+Math.floor(t/60)).padStart(2,'0')+':'+(''+Math.floor(t%60)).padStart(2,'0')+':'+(''+(f%FPS)).padStart(2,'0')+' · '+t.toFixed(2)+'s · f'+f;}
function loop(){var r=tl();if(r){if(!dragging)seek.value=Math.round(r.time()/DUR*1000);stat.textContent=fmt(r.time());}requestAnimationFrame(loop);}
function play(){var r=tl();if(r){if(r.time()>=DUR-0.01)r.time(0);r.play();}}
function pause(){var r=tl();if(r)r.pause();}
function reset(){var r=tl();if(r)r.pause(0);seek.value=0;}
function step(d){var r=tl();if(!r)return;r.pause();var n=Math.min(DUR,Math.max(0,r.time()+d/FPS));r.time(n);seek.value=Math.round(n/DUR*1000);}
seek.oninput=function(){var r=tl();if(!r)return;r.pause();r.time(seek.value/1000*DUR);};   // drag = pause + tl.time(seconds)
seek.onmousedown=function(){dragging=true;};window.onmouseup=function(){dragging=false;};
// Before playing, poll until the timeline is ready; once ready, set DUR=r.duration() and call loop()
</script>
```

The core is three things: ① dragging the `range` → `tl.pause()` + `tl.time(seconds)` seek; ② in `requestAnimationFrame`, read `tl.time()` to refresh the timecode/frame number live (do not write back to the range while dragging, to avoid jitter); ③ `◀帧/帧▶` step by `±1/FPS`. **The finished wrapper for this project is `hyperframes/minara-search-trade-demo/_test.html`; copy and adapt it** (iframe mode, easier to maintain than inlining the scene).

### Step 7 - Iterate

After viewing the test page, the operator gives feedback:
- "make the text bigger" → Edit CSS
- "change the color to #222" → Edit CSS
- "make the PnL three digits" → change values
- "change the title to Strategy Trades" → change copy
- "reduce the card spacing" → Edit padding/gap
- "too much empty space on the right" → Edit width / grid

**Make all of these yourself with the Edit tool**; do not spawn a subagent. After the change, the operator just presses ⌘R to reload and see the new version.

**Studio cache / Chrome cache is severe**: if after a change the operator says "I'm still seeing the old version":

```bash
# All three steps are required
lsof -ti:4097 | xargs kill -9 2>/dev/null
cd /tmp/hf-<scene-name>-test && python3 -m http.server 4097 &>/tmp/hf-test.log &
sleep 1
osascript -e 'tell application "Google Chrome" to reload active tab of front window'
# Or just open the URL so Chrome switches to this tab
```

**Element edit request schema (structured edit requests)**: if the operator gives you an element edit in the v1 schema format, **first start an isolated test page in /tmp** (do not touch the main project HTML), and backport to the scene html only after it passes.

### Step 8 - Render the mp4

**Render only when the operator explicitly says "渲染 / 生成视频 / OK render / commit" (render / generate the video / OK render / commit)**.

```bash
# Kill the test server
lsof -ti:4097 | xargs kill -9 2>/dev/null; true
```

Then run the render with a **subagent** (a render takes at least 20-60s; a background subagent does not block):

```
Agent({
  description: "Render <scene> mp4",
  subagent_type: "general-purpose",
  prompt: "Run:
    cd \"$VIDEO_WORKSPACE/hyperframes/<slug>\" && \\
      npx hyperframes render -c <scene-name>.html -q high --fps 60 --resolution landscape-4k --output <scene-name>-<version>-4k.mp4
      Then, per \"Video export requirements\", use ffmpeg to downscale to 2560×1440 → <scene-name>-<version>.mp4, and check with ffprobe that it is 2560,1440,60/1

    Then: open -R <output-path>

    Report just: filename, size, duration, errors. Under 100 words."
})
```

## 📦 Video export requirements: 2K 60fps (set by the operator, 2026-10-16; all final mp4s)

- **All final videos are 2K 60fps**: landscape **2560×1440**, portrait **1440×2560**; H.264 + AAC, `yuv420p`, `+faststart`. Put this in the "spec" column of the delivery table.
- **Compositions are still written at 1920×1080 / 1080×1920**; coordinates and type sizes do not change. Resolution is raised only at export.
- HyperFrames `--resolution` only supports integer multiples (1080p / 4K) and **has no 2K preset**, so it takes two steps:
  ```bash
  # 1) 4K 60fps master (use portrait-4k for portrait)
  npx -y hyperframes@latest render -c index.html -q high --fps 60 --resolution landscape-4k -o output/<slug>-vN-4k.mp4
  # 2) lanczos downscale to 2K (portrait: scale=1440:2560)
  ffmpeg -y -i output/<slug>-vN-4k.mp4 -vf "scale=2560:1440:flags=lanczos" \
    -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart output/<slug>-vN.mp4
  ```
  Do not upscale 1080p directly to 2K (it looks soft).
- **Check with ffprobe before delivery**: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 <mp4>` must return `2560,1440,60/1` (or `1440,2560,60/1`). The `-4k` master is an intermediate file and is not delivered.
- **Keep one video per deliverable, to save disk (the operator, 2026-10-27)**: once the 2K file passes the ffprobe check, delete the `-4k` master (`rm output/<slug>-vN-4k.mp4`). Scene mp4s for editing stay clean (no cover). For the delivered film, the cover version is the only file kept; see the cover section below.
- The test page scrubber and timecode still read at 30fps (for communication); this does not affect the export frame rate.

**Version number habit**: mp4 output file names carry a version number (`-2`, `-3`, `-4` suffix), so the operator's video editor sees a new file instead of a cached one. Example: `scene-backtest-preview-4.mp4`.

**Final videos all go into `output/` (set by the operator, 2026-07-03)**: for multi-scene projects, after each render, `cp` **the latest mp4 of each scene** into the `output/` folder at the project root (old versions stay in each scene's directory). At delivery, `open -R` to highlight `output/`; do not make them dig through a dozen scene subdirectories.

After rendering, use `open -R` to highlight the file in Finder so the operator can drag it straight into the video editor.

## 🖼️ Cover on the first frame (set by the operator, 2026-10-21; every delivered film)

After the final render, make a cover with **`/video-cover`** (title from the script, brand from the brand kit / site the operator names) and put it on the film's first frames, so X / Telegram / Discord / players that use the first frame as the thumbnail show the cover:

```bash
<video-cover skill>/scripts/prepend_cover.sh output/<slug>-vN.mp4 output/<slug>-cover-2560x1440.png output/<slug>-vN-cover.mp4 0.1
# from a 4K master that still exists: ... <slug>-vN-4k.mp4 ... 0.1 2560x1440
# after the checks below pass: keep only the cover version
rm -f output/<slug>-vN-4k.mp4 output/<slug>-vN.mp4
```

- **Very short hold: 0.1s** (6 frames at 60fps); never more than 0.2s. The audio is delayed by the same 0.1s, so BGM and SFX stay on their beats; nothing in the composition is retimed.
- The cover is a separate still, not a scene: don't add it to the composition or the per-second script, and don't change `data-duration`.
- Verify before delivery: frames 0–5 = cover, frame 6 = the film's frame 0, duration = film + 0.1s, `ffprobe` still `2560,1440,60/1`, audio onset moved by 0.1s (`silencedetect`).
- **Deliver only `<slug>-vN-cover.mp4`** (the operator, 2026-10-27, to save disk): once it passes the checks, delete the 4K master and the clean `<slug>-vN.mp4`. Put it in `output/` with the cover PNGs. Do any voiceover / music mux on the clean file *before* prepending the cover; the clean file is deleted only after the final cover version is made. If a clean copy is needed later (YouTube custom thumbnail, re-edit), cut the first 0.1s off the cover version or re-render.
- First used on a launch film (2026-10-21).

## The operator's firm habits

These are hard rules learned from past problems; do not try to talk them out of them:

1. **Each scene is its own mp4**, and they edit it themselves. Do not cram a 60s composition together and hand them a complete film.
2. **Strong deadline mindset**: "this video has to go out at 8pm" = every step you take must be precise; do not waste time. If they say "you're wasting my time" = stop the current approach immediately and ask what they want.
3. **Little patience for repeated revisions**: if you get a change wrong during test page iteration, admit it immediately + redo it. Do not explain.
4. **They do not read long markdown**: use tables for script timelines, not prose.
5. **When they send a screenshot + say "this is the style I mean" = match the image pixel for pixel**. Not "close enough".
6. **"放大特写" (zoom-in close-up) means a very large close-up by default**: make the specified subject the sole compositional center, push the camera in a long way so the subject takes up most of the frame, and let all other elements, components, and device bezels run off the canvas and get cropped. Do not shrink the close-up to keep the full UI, full card, or all four phone edges in frame, and do not read it as a slight zoom where "everything stays in frame". Choose the zoom factor by how much of the frame the subject should finally fill; use 2.5×–4× or more if needed.

## Reusable motion recipes (from crypto-subscription-back, 2026-06-24)

Signature effects used again and again in "product UI demo" shorts (simulated tap → modal → success → ending); copy them directly:

### 1. Camera push-in follow
The operator often says "camera follows the mouse and zooms in to the X button". How:
- Wrap the `.ui-layer` in another `.camera` layer (`position:absolute; inset:0; will-change:transform`); **keep the glow outside the camera** as background, and **keep the ending text outside the camera too** (so it is sharp at the end).
- Use `center('.target-btn')` to get the button's stage center, `gsap.set('.camera',{transformOrigin: x+'px '+y+'px'})`, then `tl.to('.camera',{scale:1.42, ...power2.inOut})` = "push in, centered on the button".
- Put the touch point `.touch` **inside the camera** (it scales with the button, staying visually aligned); before the next act, `tl.to('.camera',{scale:1, ...power3.inOut})` to pull back (at scale=1 the origin doesn't matter, so it returns to place automatically).

### 2. Touch interaction (better than an arrow cursor)
A soft touch dot + ripple ring instead of an SVG arrow: `.touch` (semi-transparent gray circle, 72px) + `.touch-ripple` (white/light gray ring, **not brand pink**). Helpers: `moveTouch(t,x,y,dur)` to move + `tap(t,x,y)` (press down 0.78→1 + ring expands from scale .3 to 1.7 and fades out). Compute coordinates with `center()`; do not hard-code them.

### 3. Success toast (instead of a full-screen success modal)
"Pop a success toast": a white pill centered at the top (`top:80px; left:50%; xPercent:-50`), a green check circle on the left (**green = success semantics, no gradient**) + two lines on the right (bold title + gray subtitle), popping in with `back.out(1.6)` from `y:-30 scale:.9`; the check is drawn with stroke-dash. Put the toast inside `.ui-layer` so it gets blurred along with the UI at the end.

### 4. Autopilot-style ending (the closing pattern the operator keeps asking for)
From `hyperframes/minara-autopilot-mobile`. Structure: **the completed state gets a 60px Gaussian blur + a frosted overlay fades in → round logo pops in with `back.out(1.7)` → two title lines (large bold main title + gray subtitle, rising staggered) → a row of chips rises at the bottom**. ⚠️ The original used a cream frost + gradient emphasis word; **both have been removed (2026-09-02)**: the frosted overlay now uses semi-transparent dark gray/black (e.g. `rgba(34,34,34,.46)`), and emphasis comes from weight/size, not gradient text.
- Blur: `tl.to('.ui-layer',{filter:'blur(60px)', scale:.97, ...power2.inOut})` + `.end-frost` opacity 0→1.
- The round logo **defaults to the official `Minara Avatar.png`** (black-and-white pixel avatar, cp from the brand asset folder into `assets/`): `.end-logo` white circle + 6px white border + shadow, with an inner `<img object-fit:cover>`. (Alternative: Minara chevron mark, dark green background `#0B2A22` + mint green `#6FE3B0`, path `M5 6l4 6-4 6M19 6l-4 6 4 6`.)
- The chips row = the equivalent of autopilot's app-store badge slot; for a payment theme, switch to **USDC/ETH/SOL/USDT coin chips** (colored coin circle + ticker), rising with `back.out(1.4)` stagger.

## Local preview / screenshot self-verification pitfalls (2026-06-24, must read)

> A scene html is a `paused` composition; opened directly in a browser it is a black screen, so it must be wrapped. Pitfalls hit while self-verifying with playwright on this machine:

1. **Where the playwright module is**: it isn't installed globally on this machine; it's hidden in `~/.npm/_npx/<hash>/node_modules/playwright`. **ESM does not read NODE_PATH**, so write a `.cjs` and use an absolute path: `require('$HOME/.npm/_npx/<hash>/node_modules/playwright/index.js')` (the hash may change; run `ls -d ~/.npm/_npx/*/node_modules/playwright` first).
2. **`waitUntil:'networkidle'` hangs forever**: because the composition loads the `gsap.min.js` CDN, the connection is never idle → networkidle never fires → `waitForFunction` times out. **Use `waitUntil:'load'` + polling** for `window.__timelines.root` (`for(i<40){await waitTimeout(500); if(evaluate(()=>!!root))break;}`).
3. **Native-resolution screenshots**: inject the scene into a standalone document (wrapped in `<div class="stage">1920×1080 relative overflow:hidden</div>`), set the viewport to 1920×1080, seek with `tl.pause(); tl.time(t)`, then screenshot; shrink large images with `sips -Z 1280` before Reading them.
4. **Interactive preview page**: an iframe pointing at the standalone scene + `.scaler transform:scale()` to fit the window + Play/Reset buttons + polling on onload to get `iframe.contentWindow.__timelines.root` and call `.restart()`. Port 4093; before starting a new one, `lsof -ti:4093|xargs kill -9`. After changes, reload with `?v=N` added to the iframe `src` as a cache-bust (python http.server returns 304 from cache, and the operator would see the old version).
5. **`<script src="gsap.min.js">` is unreliable under file://** (headless sometimes doesn't execute it → `window.gsap` undefined → timeline not registered). **Most reliable: inline the full gsap source into the standalone's `<script>…</script>`** (`curl` a copy of gsap.min.js through proxy 7890, save it locally, read it with python and inline it). This makes screenshots fully independent of the CDN.
6. **Measure centering/alignment programmatically; don't rely on your eyes**: after seeking to the target frame, compute the element center with `getBoundingClientRect()` and compare it to the frame center (960/540). The operator spots offsets of a few dozen px at a glance ("crooked" / "not centered"); visual re-checks are unreliable - confirm `centerX≈960` with numbers.

## Composition structure pitfalls (apply to every film)

1. **Give the root div both `id="root"` + `data-composition-id="root"`, and write both CSS selectors `#root, [data-composition-id="root"] {}`**. With only the data attribute while CSS selects `#root` → `font-family` doesn't apply → the whole page inherits the browser's default **serif**.
2. **content-box centering trap (the real cause of "crooked" on 2026-06-24)**: CSS defaults to `box-sizing: content-box`, so an element's actual width = `width + left and right padding`. A card/modal written as `width:W; padding:P` has a total width of `W+2P`; positioning it with `left:(1920-W)/2` puts it **P px too far right**. Fix: compute from the real total width, `left=(1920-(W+2P))/2`, or give the element `box-sizing:border-box`. **When the size is scaled up, this offset scales proportionally** and becomes more obvious.
3. **Modal content must be vertically symmetric**: do not pin the button with `position:absolute; bottom:0` at the very bottom of a tall min-height modal - the content piles at the top with a big empty block below → "unequal top and bottom margins". Instead use `.pay-content { display:flex; flex-direction:column; justify-content:center }` + a button in normal flow with `margin-top`, so the whole content group is vertically centered with equal space above and below (measured topGap==botGap). (The old magic negative value `bottom:-396px` is even more forbidden.)
4. **When the camera pushes in across acts, reset it before the next entrance**: after a push-in in the previous act, before the next act, bring `.camera` `scale` back to 1 **and reset `transformOrigin` to the center**, and have the next act's elements enter **after the camera has reset**. Otherwise elements scale in around the previous act's off-center origin → looks "crooked".
5. Gradient backgrounds are hard to tween with GSAP; **animate only scale/opacity, not the gradient itself**.

## ⛔️ Beige bar at the bottom of renders = missing chrome-headless-shell (hard lesson from 2026-06-24, must read)

**Symptom**: the rendered mp4 has **a bar of the body background color about 85px tall at the bottom** (cream `#FAF9F5`), glaring in dark/dim scenes; **the web preview is completely normal**.

**Root cause**: HyperFrames render uses `Page.captureScreenshot` (fixed region 1920×1080, `captureBeyondViewport:false`). When this machine doesn't have the dedicated `chrome-headless-shell` installed (`~/.cache/puppeteer` empty), it **falls back to full Google Chrome headless**, whose compositing surface is ~85px shorter than 1080; the bottom falls outside the surface → Chrome fills it with the `<body>` background color = the bar. **It has nothing to do with the HTML/CSS.**

**Key lesson**: **if the preview is fine but the render is wrong → suspect the renderer/environment first; do not change the composition CSS**. On 2026-06-24 I misdiagnosed it as a CSS problem and changed the dim position / will-change / box-sizing / #root position / position:fixed and more, re-rendering a dozen times with no effect; the real cause was the rendering browser. Diagnostic experiments: render a minimal composition with a pure-black full-screen `.fill` → bottom edge perfectly black (proves the engine itself is fine and it's the browser fallback); change the body background to red → the bar turns red (proves it's the body color showing through).

**Fix (one-time, permanent)**:
```bash
npx -y @puppeteer/browsers install chrome-headless-shell@stable --path ~/.cache/puppeteer
```
Once installed in the default cache directory it is found automatically; run `npx hyperframes render` as usual. The bar is produced at render time, so **re-encoding can't fix it; you must re-render**. See memory `hyperframes_render_headless_shell` for details.

## Hard prerequisites for rendering mp4 (hit on 2026-06-24)

- **render needs a full-document `index.html` in the project**; passing only `-c <scene.html>` fails with `No index.html file found` (CLI v0.7.5 requires the scaffold even with `-c`).
- If the scene file is only a composition fragment (directly `<div data-composition-id="root">…</div>`, no `<html>/<head>/<body>`), **first wrap it as a full document and save it as `index.html`**: `<!doctype html><html><head><style>html,body{margin:0;background:<bg>}</style></head><body>{scene}</body></html>`.
- Then `cd project && HTTPS_PROXY=http://127.0.0.1:7890 HTTP_PROXY=... npx hyperframes render --output name-vN.mp4` (**don't pass `-c`; render index.html directly**; render needs network access to pull the GSAP CDN, so the proxy is required).
- Multiple files with `data-composition-id` in the directory produce a `multiple_root_compositions` warning, which is non-blocking; lint warnings like transform conflicts / Google Fonts import are also non-blocking.
- Run render in a subagent (30-150s); in the main thread, first `lsof -ti:4093|xargs kill` to stop the test server. When done, `open -R` to highlight.

## 🎬 Full-film production lessons (from the 9-scene Cross-Sectional Factors film, 2026-06-26, must read)

Made a complete ~37s marketing film (opening + factor card wall + natural-language strategy generation + logo asset wall + results panel + deposit and deploy + ending), 9 separate scenes, plus a full Chinese version. Below are the new lessons from this whole production line, **more systematic than the scattered items above**.

### A. Self-verification: playwright hangs; the render engine is the reliable path (most important)
- On this machine **playwright headless kept hanging this time** (`chromium.launch()` occasionally hangs until a 2-minute timeout, probably zombie processes/resource contention). **Stop relying on playwright screenshots for self-verification.**
- **Reliable path = render directly + extract frames with ffmpeg**: `npx hyperframes render` had 0 failures throughout. To check a frame: `ffmpeg -y -ss <t> -i scene.mp4 -frames:v 1 _f.png` → `sips -Z 1100` → Read. This was the real workhorse for every self-verification step in this film; screenshot scripts are only a fallback.
- playwright's `page.evaluate(fn, arg)` **takes only one argument**; wrap multiple into an object, `evaluate(({a,b})=>…,{a,b})`; passing two throws "Too many arguments".

### B. Standalone preview collapses: #root needs explicit width and height
- When a scene html is opened alone in a browser/headless, `#root` with no explicit size → height collapses to 0 → absolutely positioned `inset:0` elements inside (text/video) all become 0 tall = **blank screen** (rendering is fine because the framework forces 1920×1080, but preview/screenshots collapse).
- **Fix: `#root,[data-composition-id="root"]{ width:1920px; height:1080px; }`** - harmless for rendering (it's that size anyway) and makes preview work. Add it to every new scene.

### C. gsap.from with stagger gets the first element stuck in seek rendering (hard-learned bug)
- **`tl.from(selector, {opacity:0,…, stagger})` on a paused/seeked HyperFrames timeline leaves the lowest-index element stuck at opacity:0** (the wallet card's "title + large balance" block was invisible while the gain/subtitle were fine). The root cause is that from's immediateRender behaves unreliably under seek rendering.
- **Fix: use `gsap.set(els,{opacity:0,y:24})` + one `tl.to(el,{opacity:1,y:0},T)` per element**. Reliable and seekable. Write every "group of elements appearing in stages" this way; do not use staggered from.

### D. The key to real-looking financial charts = a continuous OHLC walk (the root cause of "fake")
- When candlesticks/return curves look fake, **the root cause is structure, not color**: each candle sitting symmetrically on its own "center line" and candles not connecting = obviously fake.
- **Real approach: a continuous random walk, `open[i] = close[i-1]`**; body height comes naturally from volatility (small move = doji, big move = long body); segmented drift creates the "chop → pullback → breakout surge → continued rise" rhythm.
- Jaggedness: increase per-step noise (`v += drift + (rnd()-0.45)*0.085`); **fade in the green area fill only after the PnL line stroke finishes drawing** (line first, then area; not simultaneously); the line must be thick enough (8-10px) to feel strong.
- Everything uses mulberry32 with a fixed seed, deterministic and renderable.

### E. Stock logos: Clearbit is dead; use FMP, and always check for blank images
- **The Clearbit logo API is down** (returns empty). Working source: **`https://financialmodelingprep.com/image-stock/<TICKER>.png`** (fetch by ticker, no key needed, through proxy 7890).
- **FMP returns a white/blank placeholder PNG for some tickers** (BB/HIMS/MRVL in this film). After downloading you **must scan them**: compute the non-white ratio with PIL; <2% means blank, drop it.
- Non-standard-US tickers (SK Hynix/Samsung/DRAM/CBRS/RKLB) can't be fetched from FMP → ask the operator for the image, or fall back to a gray letter monogram.
- **Uniform round logos**: `.logo{width:Npx;height:Npx;border-radius:50%;object-fit:cover;background:#fff;border:1px solid #EEE}` - transparent logos sit on a white circle, square-background logos fill out into a colored round badge, all tidy.

### F. Chinese (CJK) version production
- **Font stack: `'Geist','PingFang SC','Hiragino Sans GB','Noto Sans SC',system-ui,…`** - the browser falls back per character: Latin/numbers/tickers/Minara/code use Geist, Chinese uses PingFang (a macOS system font, available in headless rendering, no network needed). Geist has no CJK glyphs, so a CJK fallback is required or Chinese won't display.
- **CJK renders about 10× slower** (~70s/scene vs ~8s for English) → batch-render multiple scenes in the background with `run_in_background`, not in the foreground (it will hit the bash timeout).
- **Chinese is squarer and uses fewer characters** → titles need to be ~1.5× larger than the English version (a 132px English title becomes ~210-236px in Chinese to fill 50%+ of the frame), and tight negative `letter-spacing` changes to 0~+0.04em.
- Flow: create a new `<slug>-zh/` folder → copy the 9 final html files + assets → sed to add the CJK font stack globally → translate text file by file (including title/desc/labels in JS data arrays, BUY→买入/SELL→卖出, code comments; do not translate the code itself/tickers/$ values) → batch-render in the background → extract frames with ffmpeg and check each one.

### G. The operator's timecode & annotation conventions
- **Timecode = `HH:MM:SS:FF` @ 30fps**: `00:00:05:05` = 5+5/30 = 5.167s; they have also written `1s25`/`2s07` (= 1s25f/2s07f; the one with a leading zero is a frame number) = 1.833s/2.233s. Conversion = `seconds + frames/30`. Confirm the fps when ambiguous.
- **Red box annotation = target fill boundary**: a red box they draw on a screenshot = "scale the element up to fill this area". **Make sure I can read red boxes**; they shouldn't have to convert it to "scale up 20%"; they can just draw the box.

### H. Copy: financial-English traps + recovering copy across sessions
- **"Finance Equity" is a trap**: in finance, equity means ownership stake, not "fairness". The idiomatic ways to say "financial equality" are **democratize / for everyone / plays fair**. This film's ending was set as **"Where finance plays fair."** (Chinese "让金融更公平").
- **They remember "copy that some Claude window gave" but forgot it** → parse `~/.claude/projects/-Users-lowesyang/*.jsonl` with python, grep message.content for keywords, and you can recover all the options given at the time. That's how the full set of ending copy was recovered that day.

### I. Reusable scene recipes from this film
- **Candle-by-candle growing loop** (deterministic, first and last frames identical for a seamless loop): driven by integer-period sine + an overall fade-out to zero at the end = first frame == last frame.
- **Single card → card wall** (scene2): `.camera` uses gsap x/y/scale; Phase A zooms in on the hero card (other cards opacity:0), Phase B pulls the camera back + surrounding cards fade in, "receding into the wall", Phase C slow scroll.
- **Horizontal pan across an asset wall** (logo wall): wider than the frame, `.camera` translateX slowly; can serve as a title-section background (layer a soft center glow `radial-gradient(...rgba(background color))` to keep text readable).
- **Typewriter**: `tl.to({n:0},{n:len,ease:'none',onUpdate:()=>el.textContent=PROMPT.slice(0,n)})`, deterministic and seekable.
- **Auto tab tour panel** (scene4-demo): 4 views stacked, switching tab highlight + crossfading views over time. **Don't use a slider that measures offsetLeft for the tab highlight** (misaligned if the font hasn't loaded); use an auto-width `.act{background:#fff;box-shadow}` + animate backgroundColor/color.
- **Deposit → deploy → wallet growth** (scene5): success toast (green check; copy says only "arrived", not "arrived in 2 seconds" - it isn't actually that fast), Deploy→Live green pill, balance count-up (`tl.to({v:start},{v:end,onUpdate})`) + rising sparkline.
- **Ending bookend**: the same green dot-matrix mp4 background + avatar as the opening; three lines (brand name in regular weight / slogan in bold / minara.ai) appearing in stages per timecode; the operator prefers **an all-black, no-gradient, no-background, no-arrow minimal CTA**.

## 🧩 UI micro-interaction demo promo lessons (max-mode-promo, 2026-07-08, must read)

When making "product UI micro-interaction → brand CTA" short promos (this film: mode menu pops out a third Max tab + shine sweep → light Gaussian-blur CTA), these **reusable hard lessons** came up:

### A. Default `<h1>/<h2>` margin is the top cause of "mysterious large gaps" (hard-learned, kept getting stuck)
- If the composition's reset only has `* { box-sizing: border-box }` and **no `margin:0`**, `<h1>` and other headings carry the browser default `margin-block: 0.67em` - **≈ 80px top and bottom margin at 120px type**. Symptom: a big unexplained gap between the title and the element below, and changing `margin-top`/`line-height` **barely has any effect** (the 80px h1 margin dominates; your 8px is swamped).
- **Diagnosis**: seek to a frame, measure the gap between the two elements' boxes with `getBoundingClientRect`; if it doesn't match the `margin-top` you set → suspect UA default margin immediately. In this film the measured box gap was 90px but the margin was only 10px; the missing 80px was the h1 margin.
- **Fix**: set `margin: 0` explicitly on heading elements (or globally `*{margin:0;padding:0}`). **Reset heading margins at the start of every new composition; don't wait to hit it.**

### B. The iframe test page must cache-bust the iframe src
- With `_test.html` (iframe pointing at index.html), ⌘R alone **still shows the cached old composition** - the operator gets frustrated after "refreshing many times with no change".
- **Fix**: in JS, `fr.src = 'index.html?v=' + Date.now();` (timestamp on every load). ⚠️ Remind them to refresh the `_test.html` tab.

### C. Bringing React Bits components (SplitText / GlareHover etc.) into HyperFrames
- The React versions don't fit (paused/seek, no React, no scroll, `repeat:-1` forbidden). **Replicating the visuals** is enough:
  - **SplitText per-character pop**: at setup, split the text into `<span class="ch">` (`display:inline-block; white-space:pre`), `gsap.set(chars,{opacity:0,y:40})` + `tl.to(chars,{opacity:1,y:0,ease:'power3.out',stagger:0.045})`. Seek-safe.
  - **Per-character split + continuous gradient together**: after splitting, each char's own `background-clip:text` cuts the gradient separately. To make the whole word share one gradient = give each char `background-size: whole-word-width px 100%` + `background-position-x = -(charLeft - wordLeft)` (measure offsets with rect once at setup). Transform movement doesn't affect x.
  - **GlareHover diagonal glare**: a `linear-gradient(115deg,...white...)` light band sweeps with `translateX`, 1-2 passes during the hover segment. On a light background the white band is faint; you can add `mix-blend-mode: overlay` + raise the white opacity.

### D. Shine/stroke border "partly missing" = clipped by overflow
- Adding `overflow:hidden` to a row to clip shine/glare also clips **the mask stroke border's rounded corners + the `drop-shadow` outer glow**.
- **Fix**: move shine/glare into a separate clipping layer `.fx{position:absolute;inset:0;border-radius:inherit;overflow:hidden}`; the element carrying the border itself is `overflow:visible`; switch the outer pop-up container's `overflow:hidden` back with `tl.set(wrap,{overflow:'visible'})` after the pop-up finishes (one set at 0 and one at the end, so scrubbing works in both directions).

### E. A "stuck" feeling = only subtle motion in a segment, macro-level stillness
- If a segment has only a subtle shine and the camera/elements are all still → it reads as "stuck", even though the timeline is running. **Keep one macro motion in every hold segment** (a very slow camera push-in through the tail is the easiest).

### F. Placing a sub-group precisely "in the red box"
- The operator draws a red box = "put this group here". When the end-card is flex vertically centered, **don't use `transform: translateY`** (it also moves the `inset:0` full-screen frosted background and exposes the edge). **Use container `padding-bottom` to move the content up as a whole** (+`padding-bottom:N` → content center moves up N/2), while the background stays put.
- **Align by measurement**: compute the pairCenter from "main title top ~ subtitle bottom" with `getBoundingClientRect`, and align it to the estimated y of the red box center (red box pixels ÷ screenshot height × 1080). In this film, adjusting pairCenter to 556 hit the red box.

### G. Self-verification workhorse = `__timelines.root.pause(t)` + playwright
- `playwright-cli goto 'http://127.0.0.1:PORT/index.html?v=timestamp'` → `eval "()=>{__timelines.root.pause(t); ...}"` to freeze a frame + measure rects + screenshot → `sips -Z 1500` then Read. For pixel-level requirements, always use eval to measure rects and get numbers. ⚠️ The first eval after `goto` occasionally returns empty; send it again.
- `file://` is blocked by playwright; start `python3 -m http.server`; when verifying with curl, add `--noproxy '*'` (the local 7890 proxy proxies localhost and causes 502).

### H. This film's final form (reusable reference)
- A single 9s composition; `index.html` = the whole film (5s menu demo + 4s light frosted CTA); short promos are not split into scenes.
- **Seamless shine technique** (reusable) = one linear gradient with a **symmetric tile** (`background-size:50% 100%` repeat + animate `--shift`), a seamless loop that replaces the forbidden `repeat:-1`. ⚠️ At the time it used the brand purple-pink-orange band; **that gradient has been removed (2026-09-02)**; reuse only the tile/shift technique, with the color changed to a grayscale white→transparent band.
- Gaussian-blur ending = menu `filter:blur(46px)` + `.landing` frosted overlay + `backdrop-filter:blur(10px)` fade-in + round avatar popping in with `back.out(1.7)` + per-character title. ⚠️ The original frost used cream `rgba(250,249,245,0.55)`, **removed**; use semi-transparent dark gray/black instead.

## 🧿 Metaphorical product scene lessons (Harness S30 Proactive Mode redo, 2026-09-05, must read)

**Background**: the first version of S30 was a "component walkthrough" - template card → suggestion modal → mandate card → pending approval list, small-text dark panels on a light background. The operator rejected it in one sentence: "There's a local s30 output - don't use that, I don't like it." The new direction they gave was three phrases: **make the core components metaphorical · express the core interaction simply · soft easing with elasticity**. The redo went through storyboard → test page → three renders in one day, all approved on the first pass. Below is the method settled in this round; apply it directly to future MG scenes that "explain a product mode/concept".

### A. Produce a storyboard collage before writing a line of code
- What they wanted was **to see a storyboard collage of 8 key frames first**, not the motion first. How: one HTML page, each frame a real CSS-drawn 1920×1080 stage scaled to 0.38, with timecode / voiceover line / action notes (easing, elasticity, what comes first and what comes next), and 4 design principles listed at the top of the page. Take one full-page PNG with Playwright and highlight it with `open -R`; **do not open the web page automatically**.
- After viewing, they only said "you can generate the test page for me to look at" and it went straight to compositing - a frame-accurate storyboard means no starting over later. Template from this round: `harness-launch-video/scenes/s30-proactive-mode-v2/storyboard-v2.html` (cream paper feel, Figtree, card style; it's a review tool, not a video, so the video palette doesn't apply).

### B. How to "make it metaphorical" = four progressive layers, no client pages
1. **Capability tiles**: make the capabilities being combined (Research / Strategies / Automation / Memory) into square cards; each card = the client's Lucide icon + a 40px large label + **one typical UI component representing that feature** (search box + result bar / return curve / connected nodes / memory row + check). Their reference was a bento grid (2×2 squares, large radius 32, gap 28, cards 400×400). The components' micro-animations run during the hold, so the hold isn't dead.
2. **Converge → core object**: the cards shrink to 0.6 along the signature curve into the center; at the moment of collapse a `target` tile pops out + two pulse rings, and the title uses the already-approved BlurText per-letter syntax.
3. **The core object becomes part of a real component**: the `target` tile shrinks via transform into the real AgentCore (ring + dot) inside the MandateCard, then the mandate fields grow out one by one - **this is "object identity": the viewer sees the big metaphor become a small part in the product**.
4. **Boundary = card border**: when explaining "hard boundaries", a 3px white line draws the group's outer frame in one stroke clockwise from the top left (`stroke-dasharray/dashoffset` + `pathLength=1000`), and the card background emerges with the line - **components arrive first, background last** (the operator already set this in S08). Then the whole group collapses via transform into the client's real MandateCard geometry, the state flips to Active, and a green pulse **is clipped at the card edge** = "proactive, but only within the authorized scope", with no words needed.

### C. "Minimal interaction" = zero mouse pointers in the whole film, one gesture per field
- The selected state is a white pill that pops from one option to another with `x + scaleX`; the amount drops into place from 24px below; the risk bar is CSS variable `--k` dragged from 0.5→0.7 with `back.out(1.7)` (overshooting to 0.72 then back), and the legend number 50%→70% crossfades between two span layers; the autonomy level pill pops out and limit chips drop in one by one. **You understand the operation without watching the operation happen.**
- Depth of field: the group currently growing is sharp; completed groups get `autoAlpha .5 + blur 1.4px`; once the boundary is drawn, everything returns to sharp = "the mandate becomes a whole".

### D. "Soft easing with elasticity" = three curves, each with one job
- Elements landing/popping: `back.out(1.4)` (one light overshoot); emphasis gestures (risk knob, end point, check): `back.out(1.7~2)`.
- Translation/convergence/collapse: the project signature curve `CustomEase M0,0 C0.95,0.03 0,0.98 1,1` (slow start → fast → slow finish).
- blur→sharp, area/background emerging, camera: `sine.inOut`. The camera only does a very light 1.0→1.06→1.09→1.0 push-pull, one `.camera` scale channel, `transform-origin` at frame center.
- Transitions ≤0.5s; the final hold keeps one macro motion (a slow pulse ring) to avoid the "stuck" feeling.

### E. They set the pacing; revise by these two rules
- **"After these four things appear, hold for two seconds, then go into the rest of the animation"** - once the key metaphor lands, hold a full 2s so people can see it; shift everything after it later, and **win the time back from the tail** ("the final card hold can be compressed"). Total length must stay within the timeline slot (14.833s); compression methods: cut repeated pings/pulses, tighten 0.7→0.5s, content stagger 0.07→0.06.
- Before changing pacing, list every time literal in a replacement table and replace each one with an assert (Python); after the change, update `window.__scene.beats` to match, and extract frames to check that all three frames of the hold segment are complete.

### F. Engineering rules (verified again this round; don't hit these again)
- **`gsap_non_transform_motion` from `hyperframes check` is a real problem**: tweens on `left/top/width/height/fontSize` jump by whole pixels under frame-by-frame extraction. Fix: use `x/y/scale`; for font size changes use `scale` + `transform-origin: 0 0`; for card box deformation use `x/y/scaleX/scaleY` (slight corner radius distortion is acceptable); when the hub shrinks into a small core, **pre-enlarge the children by the scale factor** (write the 26px ring as 97.5px; after scale 64/240 it comes out exactly 26px).
- **Displayed values must not come from `onUpdate`** (frames extracted with `pause(t)` all show the initial value). For the typewriter, use `tl.set(el,{textContent:...})` discrete per-character states; for number changes, crossfade spans; for progress, tween a CSS variable.
- **Don't measure; give fixed widths**: give explicit widths to the targets the selected pill slides to (260/300/250); do not call `getBoundingClientRect` before fonts load.
- **Overlapping tweens get overridden by the later one**: the title's per-character entrance (to 3.64s) and exit (from 3.5s) overlapped → the exit didn't take effect. The exit must start only after the entrance has fully finished.
- **The tail stretches the total duration**: one ping with an extra 1.2s stretched 14.833 to 15.45. After changes, re-check with `tl.duration()` or the duration printed by the frame extraction tool.
- **Self-contained + two entry points**: `source.html` with placeholders → `build.cjs` inlines GSAP/CustomEase/Geist (data URI) to generate `index.html`; `_test.html` is generated by `tools/make-test-page.cjs`, not hand-edited; `filecheck.cjs` proves both entry points auto-play with zero errors under `file://`, and that the 1920×1080 render viewport has no fit/review bar. The root node of `source.html` uses a `data-comp-root` placeholder that the build replaces with `data-composition-id`; otherwise check reports multiple_root.
- **Move `_test.html` out before rendering and back afterward** (it has its own `data-composition-id` and would be treated as a second root). Render command: `hyperframes render -c index.html -q high --fps 60 --resolution landscape-4k --skill product-launch-video -o output/<id>-4k.mp4`, then downscale to 2K (see "Video export requirements").
- **Trust only the MP4 itself for verification**: extract 13–18 frames with ffmpeg into a contact sheet; check frame count with `ffprobe -count_frames`; stddev of the bottom 100px band (>5 = live gradient, ≈0 = black edge from missing chrome-headless-shell); enlarge dark areas 3× nearest-neighbor to look for banding.
- **Image bytes often don't land on disk**: screenshots/reference images they paste in Claude Desktop repeatedly can't be retrieved as bytes and can't be saved to `references/user-images/`; each time, mention in the report "please send it again as a file".

### G. Copy discipline
- Every word in a component must be an original client i18n string (`en/proactive.json`: goal.* / wizard.q1-3 / expectation.steady / card.* / autonomyControl.* / settingsForm.* / status.*), or an original voiceover line. When the client has no short label, take **the first half** of the original sentence (`Every action here runs in simulation`) and flag it in the report for them to decide; words from the narrative doc ("risk boundaries, watchlists, decision style") may be used but must also be flagged.

## 🖥️ Client "growing / self-writing" shot lessons (harness-launch-video S08 v1→v6, 2026-09-04, must read)

S08 (the Minara client growing out of an empty field) went through 6 versions in one day: diagonal growth wave → components before background → openscreen elastic follow camera → four fixed camera positions → camera removed → compact UI + large text + 2× speed + mouse segment cut → **finally approved only after redoing it with the video-shotcraft `document-typewriter-reveal` card**. Below is what's actually reusable from this line. The project is in `~/Documents/harness-launch-video/` (scene `scenes/s08-product-montage/`, fully logged in its `change-log.md`).

### A. The operator's settled views on "UI growing" shots (apply directly; stop trial and error)
- **Components appear first, one at a time; the background and large frame appear last.** An empty blurred window appearing first = loading; they reject it at first sight.
- **Growing components must not have their own dark background/stroke/shadow** - input boxes and cards are "transparent like the sidebar next to them", and their background **appears together with the client background**. I tried a dark plate, then rim + shadow; both were rejected.
- **The sequence needs names and an order** (sidebar → input box → title → cards → chrome → large background frame), not "sweep everything diagonally".
- **Camera**: they asked for "zoom in and follow the growing component", then immediately found it "too much movement", then narrowed it to four fixed camera positions, then "remove it entirely". Lesson: **for product UI shots, the camera does only one pull from close-up to full page + subtle breathing** (exactly what the card does); no following, no zoom on every click.
- **Compact UI + large text**: shrink the whole client by 20% (later they asked for +20% screen share, i.e. 0.96), **all fonts ×1.5** - what they want is "dense window, large text", not scaling everything up.
- **Duration requirements carry across versions**: a duration they gave (e.g. 6.77s after "shorten accordingly") still holds after switching templates; the template's own 110f beat would be judged "not long enough". **When switching shot cards, keep the duration approved in the previous version and scale the card clock with TEMPO**; do not let the card length override their requirement.
- **When they name a shot card, read the card before doing anything.** This time the first 5 versions were my hand-built growth logic; their final line, "redo it with this template", passed in one go. For future UI entrance requests, first pick cards from `video-shotcraft/references/shots/ui-entrance/` for them to choose, then implement.
- One beat and done - they cut the entire mouse-click tour after the growth. **A growth shot = ends when assembly completes**, with no interaction after it.

### B. The fixed method for translating video-shotcraft cards into HyperFrames
- **Read three things**: the card md (semantics + parameter table + known pitfalls), `demos/<group>/<card>/*.tsx` (tuned true values: easing, timing ratios, mask timing), and any fixture used (e.g. `demos/_fixtures/PageCam2D.tsx`). **Do not downgrade** the parameters marked as "critical / known pitfalls" on the card; only reskin (font/color/material).
- **Write the timeline in card frames**: `const F = TEMPO / FPS` (one "card frame" = TEMPO real frames); multiply all cues/durations by `F`, and use a separate `RF = 1/FPS` for real frames (duration pins, camera sampling). To lengthen or shorten, change only `TEMPO`; all of the card's ratios stay intact. S08 used TEMPO=2 to stretch the 110f card to 6.77s.
- **Remotion Easing → GSAP CustomEase**: `Easing.bezier(a,b,c,d)` = `CustomEase.create(name, "M0,0 C" + a + "," + b + " " + c + "," + d + " 1,1")`.
- **A "paper-color mask" doesn't work in a scene with a background** - the card narrows a mask in the page background color anchored right; our background is a shine sweep, so the mask shows its color. Instead use **`clip-path: inset(0 100% 0 0) → inset(0 0 0 0)` on the block itself**, which never gives itself away on any background.
- **Only one pen tip**: one caret element; for each pair of blocks it follows only the second block, `tl.set` position + `tl.to` x following the reveal front + 2f fade-out; when a new pair starts it naturally jumps over.
- **Highlight comes after landing** (the card's @-mention rule): the active-state background grows 4f after the item lands, using `--veil` to drive a `background-size` gradient, `linear-gradient(...) left / calc(var(--veil)*100%) 100% no-repeat`.
- **Members "baked into the rail" appear with the patch front**: the rail uses a top→bottom patch (`clip-path` or a vertical `--rail` mask); the title bar / card background / ticker appear only when the front passes their y. **Solve the crossing time by bisection on the easing curve**; do not estimate linearly.
- **Camera = PageCam2D math** `translate(960−cx·z, 540−cy·z) scale(z)`, `transform-origin:0 0`, interpolated between keys with `bezier(0.33,0,0.15,1)`, **sampled at every real frame and baked into one GSAP keyframes tween** (`ease:"none"`, `force3D:false`), seek-accurate. Two required changes: ① the card breathes to 0.995 because paper fills the edges; when the background is also in shot, **zoom always ≥ 1.0** (use 1.002/1.008/1.000 to keep the amplitude); ② **clamp the focus to the canvas** (`cx∈[W/2z, W−W/2z]`); the original close-up went 16px above the top edge.
- **Close-up focus = the combined center of everything that will be written out** (from the logo to the bottom hint line), not just the title line - focusing on the title pushes the whole block down and leaves the upper half empty (why v5 was rejected).
- Swap accent colors per the project palette: Minara videos are grayscale; caret / inner rim line use white `#efefef`, green is reserved for semantic states.

### C. Recipe for a compact client + large text (used since v4)
- The client keeps its original layout (1560×896 CSS px), `transform: scale(K)` around the center (0.8 → 0.96), `left/top` unchanged so it centers naturally; use transform, not `zoom` (zoom scales coordinates too, and centering has to be recomputed).
- **Multiply fonts ×1.5 at build time with a batch regex** (`font-size:\s*(\d+)px`), and **assert the rule count is the same before and after**, so the regex doesn't miss one.
- Then make room for the large text: increase fixed row heights (nav 36→44, tile 52→64, titlebar 44→52, ticker 26→36 with the view-stack inset adjusted to match), widen text containers (input box/cards 880→1040), icons ×1.25 so they don't become dots, and write hairlines as `1/K px` so they're exactly 1px after scaling.
- **Prove overflow with numbers, not by eye**: write a walker that traverses every element in the client and reports `scrollWidth>clientWidth`, overflow beyond the nearest overflow-hidden ancestor, and nowrap text exceeding its box; explicitly exclude the marquee (ticker). `tools/verify-compact.cjs` can be taken and adapted.
- When measuring rects, remember the client is already scaled: anything written into the client coordinate system (caret, inner rim line) must be divided by `K = rect.width / offsetWidth`.

### D. Seek-accuracy / determinism pitfalls (supplementing the existing items)
- **GSAP suppresses `onUpdate` on seek** (`pause(t)` defaults to `suppressEvents`), so anything driven by onUpdate freezes in the renderer/scrubber.
- **`gsap.ticker` sleeps while the timeline is paused** - a cold `pause(t)` + screenshot captures the previous frame's camera (measured: 4 of 9 probes lagged a full frame). Do not apply anything from the ticker.
- **`hyperframes check` greps the text**: the name `requestAnimationFrame` triggers an error even if it only appears in a comment. Bake the camera and similar into GSAP tweens, and leave that word out of the source.
- **No `will-change`/3D translate on the camera layer**: Chrome scales a cached raster and UI text goes soft. Keep it 2D with `force3D:false`.
- Normalize diagonal ordering by the single quantity `(x+y)`; **do not normalize x and y separately** - the sidebar differs by only 8px horizontally, and separate normalization stretches that 8px to a full 0..1 range that decides half the order (a hidden bug caught in v3).
- `data-duration` is a build constant; the timeline computes `expectedDuration` in JS and calls `console.error` if it's too short, and the verification script reads `window.__beats`, so forgetting to update the duration gets caught. The renderer rounds 203f up to 204f (6.767→6.800s); document this clearly.
- Verify both before and after rendering: headless frame extraction (`tools/scene-frames.cjs`) to check the composition, **then decode frames from the final MP4 with ffmpeg** (`-ss` must not exceed the last frame's time; for a 4.0s clip take 3.9, not 3.97).

### E. Engineering habits (that bit repeatedly this time)
- **Generator script + single self-contained index.html**: GSAP / CustomEase / Geist / images all as data URIs; `_test.html` generated by `tools/make-test-page.cjs`, not hand-edited.
- **Python replacements must `assert count==1`** and raise on failure - three times an anchor didn't match and nothing was written silently, so every later test ran against the old file; the only sign was "the test results didn't change".
- **After `cd` elsewhere in one Bash call, all paths change**: in the scratchpad, `node build.cjs && node tools/xxx.cjs` - the second one always fails with MODULE_NOT_FOUND; always use absolute paths for tools.
- **In zsh, `echo ====` triggers `=cmd` expansion and errors with `=== not found`**; use `echo "----"` as a separator.
- Screenshots they paste in the desktop app **don't land on disk as bytes**; record a placeholder row in `references/user-images/INDEX.md` and ask them to resend as a file; do not pretend it was saved.
- Delivery always includes: file path + numeric verification + frames decoded from the final video, highlighted with `open -R`; put the version number in the file name (`-v5-typewriter.mp4`).

## Related memory (read as needed)

- [[feedback-hyperframes-confirm-timeline]] - send a timeline for confirmation before changing durations
- [[feedback-hyperframes-element-edit-workflow]] - structured element edits go through an isolated test page
- [[feedback-hyperframes-studio-reload]] - studio caching is severe; must kill + reload + restart
- [[feedback-hyperframes-no-agent-for-small-edits]] - small changes via Edit yourself; only render uses an agent
- [[feedback-localhost-cleanup]] - kill the old port before starting a new one; the laptop overheats

## Source

Distilled while making the `minara-strategy-studio-public` video on 2026-05-26 / 27. It had 7 scenes (opening, scene1-prompt, scene2-ui, scene-asset-grid, scene-backtest, scene-trades, scene6-deploy), and multiple rounds of iteration hit every pitfall listed above. The operator explicitly asked: "Write this up as a skill so this workflow runs automatically next time."

## Revision history

- **2026-11-13** - Added **Screen recordings are reference only**: recordings / screenshots are used to learn the flow, copy, layout, states and timing (stills via `minara-usecase-points/scripts/extract_frames.py` into `references/frames/`), and every product screen is rebuilt in HTML; no recording frames or screenshots in the final film (not sharp enough), with a pre-render grep check. Exception only when the operator asks for real footage in that job.

- **2026-10-21** - Added **Cover on the first frame**: cover made with `/video-cover`, put on the film's first 0.1s with `prepend_cover.sh` (audio delayed to match); deliver a clean and a `-cover` mp4.

- **2026-09-05** - Added **Client "growing / self-writing" shot lessons** (harness-launch-video S08 v1→v6): the operator's settled views on UI growth shots (components before background, no own background while growing, camera pulls only once, compact UI + large text, durations carry across versions, read a named shot card first), the fixed method for translating video-shotcraft cards to HyperFrames (TEMPO card frames, clip-path, PageCam2D baked into keyframes, zoom ≥ 1, focus clamped to the canvas, focus on the combined center), the compact client + 1.5× font recipe and overflow walker, additional seek-accuracy pitfalls, engineering habits.
- **2026-09-05** - Added "🧿 Metaphorical product scene lessons" (Harness S30 Proactive Mode redo): storyboard collage first, four progressive metaphor layers (capability bento cards → converging object → becomes a part of a real component → boundary is the card frame), zero pointers with one gesture per field, three-curve division of easing, the 2s hold + tail compression pacing rule, engineering rules like `gsap_non_transform_motion`, i18n original-string copy discipline.
- **2026-09-04** - Added a reference section for the **snapcn** local Remotion product-demo component library (cloned to `claude playground/snapcn/`), positioned as an on-demand reference for AI chat flow / prompt input / terminal / device frame shots, alongside Remocn; HyperFrames remains the default stack.
- **2026-09-02** - The operator instructed removing the **cream warm background** and the **brand purple-pink-orange gradient** (`#EB53FF/#FF538E/#FF9A32`) from this skill. Effects: the fixed style rules dropped the "warm" execution item and these two color rules; the default palette's primary text changed to pure white + a secondary gray was added; the touch ripple dropped brand pink; the Autopilot ending frost changed to dark gray; the seamless shine keeps only the tile/shift technique, not the brand color band; the design.md reading note marks that gradient as not used in videos. Historical pitfall records (the cream body color in the render bar symptom, the technical note that gradients can't be tweened) are kept as factual records. **Do not add these two back** unless the operator explicitly specifies it for that job.
