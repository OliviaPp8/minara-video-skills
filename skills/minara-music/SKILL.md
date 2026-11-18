---
name: minara-music
description: Generate background music and synced sound effects for Minara videos from the per-second script. Default style is minimal electronic / minimal tech (dry kick, short hats, rim clicks, syncopated sub, sparse sine sequence, low drone) with every scene cut hit-synced (卡点): a half-beat drop before the cut, a reverse swell into it, a hit and a stab on it. Translates each scene's mood and on-screen actions (taps, typing, reveals, success, notifications) into a cue sheet, then renders BGM + SFX locally (numpy synth, no external service), with optional ducking under the voiceover. Use for /minara-music, "配乐", "生成音乐", "BGM", "背景音乐", "卡点", "极简电子", "minimal tech", "按脚本生成音乐", "加音效", or when a minara-video / minara-guide-video project needs a music bed.
---

# /minara-music — Minimal tech music + sound effects from the script

Turn the video's **per-second script** into a cue sheet, `cues.json`, then synthesize the BGM and picture-synced sound effects locally. Synthesis is pure local numpy and deterministic (the same cues + seed always give the same audio). No external service, no cost.

**Default style: minimal electronic / minimal tech** (the operator, 2026-10-21). Few sounds, all short and dry, on a strict grid: a tight kick, short hats, rim clicks, a syncopated sub bass, a sparse 16th-note sine sequence and a low drone. Energy comes from adding and removing layers, not from chords or melody. The music is cut to the picture: every scene cut gets a hit.

`<skill>` below is this skill's installed directory (for example `~/.claude/skills/minara-music` or `~/.agents/skills/minara-music`).

Source: a launch film (2026-10-21), `examples/minimal-tech.json`. The earlier warm style from the Minara V2 launch film is still available as `"style": "soft"` (`examples/v2-launch.json`) and renders exactly as before.

## Workflow (in order)

1. **Read the script**: the per-second script from minara-video, or the keyframe sheet from minara-videoscript (Music column + sound cues). Collect two lists: the **cut times** (every scene change and any hard picture change) and the **visible actions** (word or card pops, taps, typing, reveals of a key number).
2. **Pick the tempo so the cuts land on the beat.** Default 120 BPM (beat = 0.5s), so cuts on whole or half seconds are on the grid. The script prints a warning for any cut more than 20 ms off the 16th-note grid, with the nearest grid time; move the cut in the picture, or change `bpm` when it suggests one that fits every cut. Hits that miss the grid by more than ~30 ms sound late.
3. **Write the cue sheet** in the project's `audio-src/cues.json`:
   - `duration` (= final video length), `bpm`, `key` (default `A minor`; `C major` for brighter pieces), `seed`. `style` defaults to `minimal`.
   - `sections`: one per scene, with `energy` and a `note` naming the picture. Section starts are the cuts by default.
   - `cuts` (optional): list them only to add cuts inside a section, drop one, or set `big` / `gain`. Default = every section start after 0; a cut is `big` when it opens a `full`, `climax` or `outro` section. Write `"cuts": []` for no cut hits.
   - `sfx`: one per visible action, at the second the script gives. Reveals of a key number or a card use `stab`; small pops and taps use `tap`.
4. **Show the operator the sheet first; don't render yet.** Markdown tables: "time / energy / layers / picture", "cut / big", "sfx time / type / action". Wait for OK. They edit the sheet, not the code.
5. **Render**:
   ```bash
   python3 <skill>/scripts/make_music.py <project>/audio-src/cues.json -o <project>/assets [--vo <project>/assets/vo.wav]
   ```
   About a second per minute of film.
6. **Self-check** (measure, then ask the operator to listen; don't claim you heard it):
   - Loudness per section: busiest sections (`full`, `climax`) loudest; `intro`, `breakdown`, `outro` 6–10 dB lower.
   - Each cut hit 5–15 dB above the half beat before it (the drop makes the hit land).
   - With a voiceover, ducking works: music sits ~8 dB lower under speech, hits and SFX are not ducked.
   Fix by editing the sheet (`level`, `layers`, a cut's `gain`, an sfx `gain`) and re-rendering.
7. **Deliver**: the path to `bgm.wav` (or `bgm-duck.wav`), and `open -R` on `preview-mix.wav` so they can listen. In HyperFrames add it as its own audio element; the voiceover stays on a separate track. For a film that already has the cover on its first frames (`video-cover`, 0.1s), delay the music by the same 0.1s before muxing.

## Output

| File | Contents |
|---|---|
| `bgm.wav` | Music + cut hits + sound effects, 48 kHz stereo, -1 dBFS peak, 0.4 s fade-in, 3.2 s fade-out |
| `bgm-duck.wav` | With a voiceover: music lowered by `duck_db` (default -8 dB) under speech; cut hits and sound effects are not ducked |
| `preview-mix.wav` | With a voiceover: bed + voice, for listening only |

## Energy → layers (minimal style)

Layers: `k` kick (quarter notes) · `h` hats (off-beat 8ths; 16ths too when `b` is on) · `r` rim clicks (the off-beat after beats 2 and 4) · `b` syncopated sub bass (i i VI VII per bar; I I IV V in major) · `s` sparse 16th sine sequence on the tonic 7th chord · `p` low drone (root + fifth).

| energy | layers | Use for |
|---|---|---|
| `silent` | — | Full silence |
| `intro` | `p` | Opening, first words on screen |
| `light` | `khp` | Product name or a simple reveal; light pulse |
| `build` | `khrsp` | Explaining how it works; adds a short riser when the next section is `full` / `climax` |
| `full` | `khrbsp` | The main proof: results, backtest, live demo |
| `breakdown` | `rsp` | Kick and bass out; a pause, a list of cards, security / privacy |
| `climax` | `khrbsp` | Strongest kick, stabs move up a third; product name or launch claim |
| `outro` | `p` | End card: drone + high shimmer, fades with the mix |

Each section takes `"level": 0.5–1.3` to adjust its volume, and `"layers": "khrsp"` to override the set (e.g. keep the groove going in a table scene without the bass).

**Per-bar variation** (`"variation": true` at the top of the sheet, opt-in): when the operator says the loop is too repetitive (“太单调”, “每小节加点变化”), every bar of a 4-bar phrase changes — the sequence follows the bar's chord and cycles four patterns (bar 4 is a busier fill), ghost kicks on bars 2 and 4, an open hat on bar 2, a rim / hat roll into each new phrase, a moving bass on odd bars, and a soft crash + short reverse swell marking each phrase in `full` / `climax`. Still the same few sounds. Without the flag the render is unchanged.

**Cut hits (卡点)**, on every cut: kick, rim and bass drop for the half beat before it, a 0.5 s reverse noise swell rises into it, and a low hit plus a minor-7th stab (major-7th in a major key) land on it. Big cuts get a louder hit.

## Sound effect types (sfx)

| type | minimal sound | Typical action | Optional parameters |
|---|---|---|---|
| `stab` | Short filtered 7th-chord stab | A key number, card or headline appears | `high` (default: true inside a climax), `gain` |
| `tap` | Rim click | Button tap, word pop, small card pop | `gain` |
| `typing` | Hat ticks | Typing in an input or URL | `chars`, `cps` (match the on-screen typing speed) |
| `hit` | Low hit | Extra hard accent off a cut | `gain` |
| `success` | Two rising sine blips | Order filled, strategy running | `gain` |
| `notify` | Three sine blips | Notification pops up | `gain` |
| `bell` | Long sine ping | Logo or avatar appears | `note` (MIDI) |
| `blips` | Blips stepping up the scale | Backtest progress, loading | `count`, `step` (seconds), `note` |
| `sparkle` | Scattered high blips | Particles converging | `dur` |
| `riser` | Rising noise | Extra build-up | `dur` |
| `whoosh` | Falling noise | Window collapse, push transition | `dur` |
| `thud` | Heavy hit | Lock, confirmation | `gain` |
| `crash` | Short noise burst | Extra accent | `gain` |

In `"style": "soft"`, the same types use the V2 sounds (bells, plucks, cymbal); `stab` and `hit` are minimal-only.

## Rules

- **Minimal means few sounds.** Don't add pads, chord progressions, melodies, risers on every cut, or effects on every element. When a section feels thin, add one layer, not a new instrument.
- **Cuts are the grid.** Every scene cut gets a hit; nothing else gets a hit-sized sound. Reveals get a `stab`; small pops get a `tap`.
- **Sound effects follow visible actions only.** No matching action on screen, no sound effect.
- **Copy timings from the script; don't estimate.** Cut and sfx times come from the per-second script or the composition's timeline; typing `cps` matches the animation.
- When the operator asks to remove a sound ("50s 的咚咚咚删掉"), find which cue it is (cut hit, stab, kick in the section) and say which one was removed; if two candidates are close, name the other one too.
- If the script's length or order changes, **update cues.json and re-render**; don't stretch or cut the audio by hand.
- Don't use external AI music services or tracks downloaded from the web; licensed music comes only from the operator.
