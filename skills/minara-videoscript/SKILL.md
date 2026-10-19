---
name: minara-videoscript
description: Write Minara video scripts before any animation work — launch / promo films, single-scene supplements, use case tutorials. Turns a brief, product screenshots, frontend code, Figma frames or a feature note into an English-only script doc built around a keyframe sheet; each keyframe has a still image (rendered from UI code, exported from Figma, or AIGC-generated from screenshots), a picture description, the voiceover line, on-screen text (花字) with style, timing and duration, and the BGM style / sound cues. Also covers what each scene must land, user flow + UI copy, voiceover word budget and open questions, in a calm, neutral, natural voice. Then hands off to minara-video, minara-usecase-video and minara-music. Use for /minara-videoscript, "写视频脚本", "视频脚本", "分镜脚本", "关键帧", "关键帧脚本", "花字", "补充脚本", "旁白稿", "video script", "voiceover script", "keyframes".
---

# /minara-videoscript — Minara video scripts

Script only, no animation. The output is one markdown script doc plus a folder of still keyframe images. After the operator approves it, it goes downstream:

| Video type | Downstream skill |
|---|---|
| Marketing / launch / demo film (picture built in code, UI may be redrawn) | `minara-video` |
| Use case / beginner tutorial (UI rebuilt faithfully) | `minara-usecase-video` |
| Captions + voiceover over the operator's own screen recording | `minara-guide-video` |
| Cut the recorded narration and place it on the voiceover track | `minara-voiceover` (reads the keyframe sheet's Voiceover and Time columns) |
| Music / sound effects | `minara-music` (reads the music section and sound cues from this doc) |

Structure: a single-scene supplement has 5–8 keyframes drawn from one `source.html`; a full film is usually 6–10 scenes. Write new scripts in English only.

## The core unit: the keyframe

A script is a sequence of **keyframes**. A keyframe is one still image of a moment the viewer must see, with everything that happens around it written next to it. Every keyframe carries the same seven fields:

| Field | What goes in it |
|---|---|
| **Image** | `![K3](keyframes/<topic>/K3.png)`. Source tag: `UI code` / `Figma` / `AIGC`. |
| **Time** | Timecode the still represents (`40.5s`) and the range it covers (`39.8–41.6s`). |
| **Duration** | Length of that range in seconds (hold + the motion into it). |
| **Picture** | What is on screen and what moves, in order. Camera move if any (push in to the workflow card). |
| **Voiceover** | The line spoken over this range, or `—`. |
| **On-screen text (花字)** | Exact text, style, position, in/out time. Or `—`. Rules below. |
| **Music** | BGM energy for this range + any sound cue with its exact time. |

Rough count: one keyframe per 2–4 seconds of film, at least one per scene. Pick the frames where something has landed (the prompt is typed, the chart is drawn, the notification arrived), not mid-motion blur.

## Language: English only (the operator, 2026-10-19)

- **Everything in the script doc is English**: title, notes, flow table, keyframe fields, voiceover, on-screen text, UI copy, music notes, open questions. No Chinese translation lines, no "中文对照" columns, no other languages. The same goes for any text inside keyframe images.
- UI copy is quoted exactly as it appears in the English product UI.
- The operator may brief in Chinese; translate the meaning into the English script. Talk to them in Chinese in chat if they write in Chinese. Only the doc is English.

## Voice: calm, neutral, natural

The script should read like a person wrote it, not a model. Calm and neutral: state what happens, let the product carry it.

- **Read every voiceover line out loud.** If it sounds like an ad, a slogan generator, or a press release, rewrite it. If you wouldn't say it to a colleague, cut it.
- Plain verbs, short sentences, present tense. Contractions are fine (`it's`, `you'll`). Example of the register: `Just ask.` / `Backtest it.` / `Minara builds the workflow.` / `Then it keeps watching.`
- Neutral, not excited: no hype adjectives, no exclamation marks, no all caps, no emoji.
- **Banned words**: exciting, powerful, seamless(ly), effortless(ly), revolutionary, game-changing, unlock, unleash, elevate, supercharge, empower, cutting-edge, next-level, robust, leverage, harness, journey, landscape, delve, transform(ative), "at your fingertips".
- **Banned AI patterns**:
  - "Not just X, but Y" / "It's not X. It's Y."
  - Lists of three for rhythm ("faster, smarter, safer")
  - "Imagine…", "What if…", "In a world where…", "Say goodbye to…", "Meet your new…"
  - Rhetorical questions as hooks
  - Colon or dash reveals ("One thing changed: everything.")
  - Trailing -ing clauses that add fake depth ("…, giving you full control.")
  - Significance padding ("a pivotal moment", "redefines how…")
- Full pattern list: the AI-writing pattern list (e.g. Wikipedia: "Signs of AI writing"). Run every voiceover line and every piece of on-screen text against it before handing over.
- No profit promises ("guaranteed", "risk-free"). If backtests or returns appear, note where the risk line goes (e.g. `Past performance does not guarantee future results.`).
- Facts not in the source material get ⚠️ and go to "Open questions". Don't invent.

## Workflow

1. **Collect inputs**: brief, screenshots, frontend code path, Figma link, feature notes, existing cut, music reference if any. Ask once, in one combined question, only for what can't be inferred: length, landscape/portrait, platform (X / Discord / website), voiceover or not, where it sits in the film, music mood if the operator has one in mind.
2. **Lock the presentation choices** at the top of the doc so they don't drift: the example case, which surface (Desktop / App / Web), time zone, what is not shown. Pick the case by the topic rules below.
3. **Draft the text first**: section 1 (what to land), the user flow and UI copy, the scene list with timings, and the keyframe list (IDs, times, picture, voiceover, on-screen text, music). No images yet. This keeps image work from steering the story.
4. **Make the keyframe images** by the routes below, into `docs/keyframes/<topic>/K1.png …`. UI frames go first (they're free and exact); ask before any AIGC frame that costs credits.
5. **Write the doc** into the project's `docs/` (`NN-script-scene-N-<topic>.md` for a single scene; `NN-script-<slug>.md` for a full film). Project root if there's no `docs/`. Open every keyframe PNG and check it against its Picture field before linking it.
6. **Self-check** with the checklist below. Compute voiceover word counts and timing; don't estimate.
7. **Send to the operator**: file path plus 3–5 lines (length, scene count, keyframe count by source, voiceover words / share of runtime, music direction in one line, number of open questions). They edit the script and mark keyframes, not code. **No animation before approval.** Still images are allowed before approval; motion is not.
8. **After approval**: hand off. The downstream per-second script expands from this doc's keyframe times; nothing gets rewritten. `minara-music` builds `cues.json` from the Music section. For a review board, generate `storyboard.html` from `minara-video`'s `assets/storyboard-template.html`; AIGC keyframes map to its AIGC rows.

## Making keyframe images

Three routes. Use the first one that fits; a script can mix them, and every keyframe says which one it used.

### Route A — UI code (default for anything that is product UI)

The frame is drawn in HTML, so the copy is exact and the frame can be reused by the animation later.

1. Copy `assets/keyframes-source-template.html` to `docs/keyframes/<topic>/source.html`. One `<section class="k" id="K1">` per keyframe; `?k=K1` shows that frame.
2. Fill each frame from the real UI: take copy, data and structure from the frontend code (components, i18n strings) or the existing HyperFrames composition. **Redraw large**, per the video rules: body ≥28px, titles ≥48px, key numbers 80–140px, 3–5 elements per screen, Geist only, Minara palette (`#F2F2F2` stage, `#15171A` / `#222222` / `#FFFFFF` UI, `#B0B0B0` secondary, green `#07B56A` up/success only, red `#F75D5F` down only), no gradients, "Illustrative data" bottom right.
3. Draw the on-screen text (花字) into the frame where it will sit, so the operator reviews the real layout.
4. Shoot:
   ```bash
   ~/.claude/skills/minara-videoscript/scripts/shoot_keyframes.sh \
     docs/keyframes/<topic>/source.html docs/keyframes/<topic> landscape K1 K2 K3
   ```
   Output is 2560×1440 (`portrait`: 1440×2560), matching the 2K delivery. The script also passes `#k1`, so older V2 source pages (hash-selected) work too.
5. **If the animation already exists** and a keyframe is a moment in it: seek the composition instead of redrawing. Use the project's test page with `?t=<seconds>` or `npm run snapshot -- <t1>,<t2>`, then copy the PNG in as `K<n>.png`.

### Route B — Figma

When design has the frame in Figma (new screens not yet in code, campaign layouts).

1. Get `fileKey` and `nodeId` from the link (`node-id=1-2` → `1:2`). Load the Figma design-to-code guidance before `get_design_context`.
2. `get_screenshot` with `maxDimension: 2560`, then download the URL with curl into `docs/keyframes/<topic>/K<n>.png`.
3. Use `get_design_context` / `get_variable_defs` to take the exact copy and tokens for the UI copy table.
4. If the Figma frame is a dense desktop screen, it is reference only: rebuild it large through Route A and note `Figma → UI code` as the source.

### Route C — AIGC from screenshots

For frames that are not product UI: an opening image, a metaphor, a person using the phone, an environment, a mood shot. Never for product UI or anything with real copy or numbers; those go through A or B.

1. **Ask first.** Image generation spends credits (Figma `generate_image` uses Figma AI credits; Weave models need a quoted cost and an explicit approve). Say which frames, which model, and the cost, then wait.
2. Give the model the screenshot or a Route A frame as reference where the tool accepts one; otherwise describe the reference in the prompt.
3. Prompt rules: 16:9 (or 9:16), the Minara palette in words (light grey stage, near-black UI, white, green only for success), clean and minimal, soft daylight, no gradients, no purple-pink-orange, **no text, letters, numbers or logos in the image** (models garble them; text is added in code), no meme imagery, no real people's likeness or other brands.
4. Save as `K<n>.png`, and write the exact prompt, model, reference image and date to `docs/keyframes/<topic>/prompts.md` so the frame can be regenerated or handed to the colleague who makes AIGC shots.
5. Open the result. Reject anything with stray text, wrong hands, wrong colors, or that looks like stock AI art; regenerate or fall back to a Route A layout.

## On-screen text (花字)

On-screen text is any text placed over the picture that is not part of the UI itself: caption lines, a title, a key number, the end CTA.

- **Allowed**: (1) the voiceover line or part of it, as a caption or emphasis; (2) real UI copy pulled out and enlarged; (3) a title, key number or CTA the operator asked for. Nothing else. No annotation words, label walls, floating keywords or feature tags. If a concept needs explaining, show it with picture and motion.
- The voiceover rules apply: calm, plain, no banned words, no exclamation marks, sentence case.
- Write each item as: `"Just ask."` · 64px / 700 · `#15171A` · top-left over the window · in 12.4s, out 14.0s · rises 24px with minaraSnap.
- Styles to pick from (keep one film consistent):

  | Style | Use | Spec |
  |---|---|---|
  | Caption | Voiceover line shown as text | 40–48px / 500, bottom centre, white on dark or `#15171A` on light, no box |
  | Headline | Title or the scene's one claim | 64–96px / 700, tracking −0.02em, left aligned |
  | Key number | A number that is the point of the shot | 120–200px / 700, tabular nums; green/red only if it is a gain/loss |
  | CTA | End card | 56–72px / 700 + product name or URL |

- Motion: in with minaraSnap (0.6–0.9s, small rise or scale from 0.96), out with a ≤0.3s fade. Each item stays at least as long as it takes to read aloud (0.4s/word, minimum 1.2s).
- No emoji, no gradient fills, no glow, no outlined or 3D text, no all caps.

## Music (BGM style and sound cues)

The doc gives `minara-music` everything it needs, so music is decided with the script, not after.

- **Film-level brief** (one block): tempo (BPM, default 120), key (default A minor; C major for bright pieces), feel in 1–2 plain lines (`Soft electronic, warm pads, light plucked arpeggio, no vocals.`), what to avoid (no EDM drops, no trailer hits, no lo-fi crackle, no vocal chops), and a reference track if the operator gave one. Licensed tracks come only from the operator.
- **Per-keyframe energy**: one of `silent / intro / light / build / full / breakdown / climax / outro` (the `minara-music` vocabulary), plus a few words of mood. Energy follows the story: the product name or launch claim gets `climax`; a privacy or security beat gets `breakdown`; the end card gets `outro`.
- **Sound cues**: only for visible actions, each with its exact time: `tap 35.0s`, `typing 32.1–34.6s (cps 18)`, `success 45.0s`, `notify 45.2s`, `whoosh 47.3s`, `thud 43.2s`, `bell 0.4s`. Types are the `minara-music` sfx list.
- Voiceover ducks the music; say `duck under VO` in the brief when there is voiceover.

## Script doc template

````markdown
# Script | <Topic>: <one-line summary>            ← full film: "Script | <Film name>"

> The single current script for <scene N / the full film>.
> Purpose: <replaces scene N, XX–XXs / new film>. The existing cut is unchanged until this is approved.
> Sources: <frontend code path / Figma link / screenshot paths / product doc>. Items marked ⚠️ aren't in the source and need product confirmation.
> **Presentation (locked)**: <case; surface; time zone; what is not shown; whether there's a follow-up question step>.
> **Output**: <2560×1440 or 1440×2560>, 60fps. Keyframes: `docs/keyframes/<topic>/` (source: `source.html`, AIGC prompts: `prompts.md`).

## 1. What this has to land
1. <the first thing a viewer should remember>
2. … (max 4; each maps to at least one keyframe)

## 2. User flow and UI copy
| Step | User action | UI copy (exact) | Source |
(Source = code path / Figma node / screenshot; demo prompts are marked "(demo)")

## 3. Keyframe sheet (<total>s<, replaces XX–XXs>)
| Key | Time | Dur | Scene | Picture (short) | Voiceover | On-screen text | Music | Image source |
|---|---|---|---|---|---|---|---|---|
| K1 | 0.0–2.4s | 2.4s | S1 | Avatar lands centre | — | — | intro · bell 0.4s | UI code |
(One row per keyframe; ranges contiguous and summing to the total. This is the table downstream skills read.)

## 4. Scenes and keyframes
### <Scene id> | <start>–<end>s (<length>s) <short title>
<one line on what this scene does>

#### K3 · 40.5s (39.8–41.6s, 1.8s) <short title>
![K3](keyframes/<topic>/K3.png)
- **Source**: UI code (`source.html#K3`, copy from `<path>`)
- **Picture**: <what is on screen; what moves, in order; camera>
- **Voiceover**: "<line>" or —
- **On-screen text**: "<text>" · <size/weight> · <colour> · <position> · in <t>, out <t> · <motion>; or —
- **Music**: <energy> · <mood words>; cues: <type t>, …

### Voiceover summary
| Scene | Voiceover | Words | Seconds @150 wpm | Scene length | Share |
- **Total**: X words, ~Ys of Zs (N%, must be ≤80% per scene).

## 5. Music
- **Brief**: <BPM> · <key> · <feel in 1–2 lines> · avoid: <…> · <duck under VO> · reference: <track or none>
| Section | Time | Energy | Mood | Keyframes |
| Cue | Time | Matching action |

## 6. Notes
- **Surface / transitions**: …
- **Demo data**: … (max drawdown if a strategy appears)

## 7. Effect on total runtime        ← only when changing an existing film
| Option | What changes | Result |   (recommend one)

## 8. Open questions
1. ⚠️ …
````

A full film adds a **scene overview table** (scene / time / content / voiceover) before section 3. The rest is the same.

## Writing rules

### Voiceover
- 150 wpm (2.5 words/s). Each scene's voiceover ≤80% of the scene's length, to leave room for the action.
- One line per keyframe range at most; one or two per scene.
- Voiceover says what the user gets; the picture shows how. Don't narrate text that's already being typed on screen.
- Hook within the first 3 seconds (a result or a plain promise, not a question). The last scene lands on the product name and one action.

### Picture
- Demo prompts say everything in one sentence (no follow-up question step unless the presentation choices say otherwise).
- Large UI: 3–5 elements per screen; key numbers get their own keyframe.
- Scene-to-scene switches are ≤0.5s; don't describe long transitions.
- Be concrete: "Cursor clicks "Build automation"", not "the user creates an automation".

### Topic rules (the operator, 2026-10-15)
- **Stocks / TradFi first**, major crypto (BTC, ETH) second. When both appear, stocks come first and get more time.
- **No meme coins unless the operator asks** (picture, asset pools, tickers, AI answers, sample prompts, AIGC images). If product material has them, swap in stocks and note the swap.
- Demo data: PnL in 3–4 digits, balances in 4 digits; keep "Illustrative data" bottom right.
- **Strategy max drawdown >20%: stop and tell the operator** before it goes in the script.

### Timing
- Timecodes to 0.1s. Keyframe ranges and scene ranges are contiguous, don't overlap, and sum to the total. Each keyframe's Dur equals its range.
- If a change lengthens the film, write the runtime section with a shift option and a compress option, recommend one, and note that voiceover and BGM timelines move with it.

## Pre-handoff checklist

- [ ] The whole doc is English, including text inside keyframe images; no Chinese or other-language lines
- [ ] Every voiceover line and on-screen text read aloud: sounds like a calm person, not an ad or a model
- [ ] No banned words or AI patterns (checked against the AI-writing pattern list (e.g. Wikipedia: "Signs of AI writing"))
- [ ] Every point in section 1 has a keyframe
- [ ] Every keyframe has all seven fields; `—` where empty, never blank
- [ ] Every keyframe image exists, is 2560×1440 (or 1440×2560), and was opened and matches its Picture field
- [ ] Product UI frames come from UI code or Figma, never AIGC; AIGC frames have no text and their prompts are in `prompts.md`
- [ ] On-screen text is only voiceover lines, real UI copy, or operator-requested titles / numbers / CTA
- [ ] Music: film brief written; every keyframe has an energy; every cue sits on a visible action with an exact time
- [ ] Word count × 0.4s ≤ 80% of each scene; totals in the summary
- [ ] Keyframe and scene ranges contiguous and sum to the total
- [ ] UI copy traceable to code, Figma or screenshots; anything else marked ⚠️
- [ ] No profit promises; risk line placed if backtests/returns appear
- [ ] Topics: stocks first, no meme coins, drawdown ≤20% (or flagged)
- [ ] All ⚠️ items collected in Open questions

## Don't
- Write animation, render video, generate voiceover or render music before the script is approved. Still keyframes are fine.
- Spend image-generation credits without the operator's go-ahead.
- Use AIGC for product UI, real copy, numbers or logos.
- Pick the runtime option for the operator (recommend, then wait).
- Post the script or keyframes to any group or channel; delivery is the local file path.
