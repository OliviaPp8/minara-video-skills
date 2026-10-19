---
name: minara-music
description: Generate background music and synced sound effects for Minara videos from the per-second script. Translates each scene's mood and on-screen actions (taps, typing, success, notifications, transitions) into a cue sheet, then renders BGM + SFX locally (numpy synth, no external service), with optional ducking under the voiceover. Use for /minara-music, "配乐", "生成音乐", "BGM", "按脚本生成音乐", "加音效", or when a minara-video / minara-guide-video project needs a music bed.
---

# /minara-music — Generate music + sound effects from the script

Turn the video's **per-second script** into a music cue sheet, `cues.json`, then synthesize the BGM and picture-synced sound effects locally. Synthesis is pure local numpy and the output is deterministic (the same cues + seed always produce the same audio). It calls no external service and costs nothing.

Source: the scoring approach from the Minara V2 launch film, generalized into a reusable script; `examples/v2-launch.json` is that film's cue sheet.

## Workflow (in order)

1. **Read the script**: get the per-second script from minara-video (or the storyboard / voiceover timing sheet). If the script has "sound atmosphere" or "music" columns, follow them; if not, judge from the mood of the picture.
2. **Write the cue sheet**: in the project's `audio-src/cues.json`, write:
   - `duration` (= final video length), `bpm` (default 120), `key` (default `A minor`; for bright/celebratory pieces you can use `C major`), `seed`.
   - `sections`: cut the script into music sections, pick one `energy` per section, and use `note` to describe the matching picture (for easy cross-reference).
   - `sfx`: each visible action in the script (tap, typing, order filled, notification popping up, transition, lock landing) gets one sound effect, timed to the second given in the script.
3. **Show the operator the sheet first; don't render yet**: in markdown tables, list "time range / energy / matching picture" and "sfx time / type / matching action", and wait for them to say OK before rendering. They edit the sheet, not the code.
4. **Render**:
   ```bash
   python3 ~/.claude/skills/minara-music/scripts/make_music.py <project>/audio-src/cues.json -o <project>/assets [--vo <project>/assets/vo.wav]
   ```
5. **Self-check**: the script prints each section; then measure loudness per section to confirm climax is loudest, breakdown/outro clearly drop back, and ducking is working. For listening issues (too busy, a sound effect stealing focus), adjust `level` / `gain` and re-render; each render takes a few seconds.
6. **Deliver**: give the path to `bgm.wav` (or `bgm-duck.wav`), and use `open -R` to highlight `preview-mix.wav` so they can listen. In HyperFrames, add it as an audio track, with the voiceover on a separate track.

## Output

| File | Contents |
|---|---|
| `bgm.wav` | Music + sound effects, 48 kHz stereo, -1 dBFS peak, 0.4 s fade-in at the start and 3.2 s fade-out at the end |
| `bgm-duck.wav` | Generated when there is a voiceover: music is lowered by `duck_db` (default -8 dB) where speech occurs; sound effects are not ducked |
| `preview-mix.wav` | Generated when there is a voiceover: music + voiceover mixed together, for listening only, not for the final video |

## energy section types

| energy | Sound | Used for |
|---|---|---|
| `silent` | No music | Pauses that need complete silence |
| `intro` | Low drone + soft pad | Opening, logo, data converging |
| `light` | Pad + light arpeggio + sparse beat | Mobile interactions, lightweight feature demos |
| `build` | Adds bass and a kick on every beat, automatic riser at the end of the section | Gradual build-up leading to a key moment |
| `full` | Full drum kit + clap + bass + arpeggio | Continuous showcase of core features (backtesting, going live, automation) |
| `breakdown` | Drops drums and bass, leaving only pad and a soft arpeggio; the kick returns in the last bar | Scene changes, sections about security/privacy that need to "breathe" |
| `climax` | Fullest: full drum kit + lead melody + crash at the section start; automatically adds a riser if the previous section is not build | Product name / launch claim appears |
| `outro` | Resolves on the tonic chord + brand bell, fading out with the whole mix | End card, CTA |

Each section can take `"level": 0.5–1.3` to fine-tune its volume. Chords follow global bars (minor i–VI–III–VII, major I–V–vi–IV), so they don't break across sections.

## Sound effect types (sfx)

| type | Sound | Typical action | Optional parameters |
|---|---|---|---|
| `tap` | Short click | Button tap, selection | `gain` |
| `typing` | Continuous typing ticks | Typing in an input field | `chars`, `cps` (characters/second, matching the on-screen typing speed) |
| `success` | Two rising bell tones | Order filled, strategy running | `gain` |
| `notify` | Three-note alert | Notification or reminder popping up | `gain` |
| `bell` | Single bell tone | Avatar/logo appears | `note` (MIDI, default 81) |
| `blips` | Short tones stepping upward | Backtest progress, data loading | `count`, `step` (seconds), `note` |
| `sparkle` | Shimmering grains + breathy noise | Particles converging, opening | `dur` |
| `riser` | Rising noise | Manually added transition build-up | `dur` |
| `whoosh` | Reverse sweep | Window collapsing, push/pull transition | `dur` |
| `thud` | Low lock-in thud | Lock, confirmation, heavy landing | `gain` |
| `crash` | Cymbal | Extra accent | `gain` |

Every sound effect can take `gain` to adjust its volume.

## Rules

- **Sound effects follow visible actions only**: if there is no matching action on screen, add no sound effect, the same as "don't add text casually".
- **Copy timings from the script; don't estimate**: the sfx `t` uses the actual seconds from the per-second script / animation timeline; `cps` for typing uses the typing speed in the animation.
- If the script's length or order changes, **update cues.json first and re-render**; don't stretch the audio by hand.
- Don't use external AI music services or tracks downloaded from the web; when commercially licensed music is needed, the operator provides the file.
