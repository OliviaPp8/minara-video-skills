---
name: minara-voiceover
description: Cut an existing narration recording into the script's voiceover lines and place each line on the film's voiceover track at the time the script gives, then put that track into the video. Reads the lines and times from the minara-videoscript keyframe sheet, finds each line in the recording (local whisper-cli word timings + energy trim), builds a film-length vo.wav at -16 LUFS, mixes it with the BGM into the rendered mp4 without re-encoding the picture (or wires it into the HyperFrames composition), and verifies every line lands on time. Local only, no TTS, no external service. Use for /minara-voiceover, "旁白", "配音", "切旁白", "旁白对轨", "把旁白放进视频", "语音合成", "voiceover", "VO track".
---

# /minara-voiceover — Cut the narration and lay it on the film

Input: one narration recording (the voice actor or the operator reading the script, lines in order) and an approved script. Output: a voiceover track where every line starts at the second the script says, and a video with that track in it.

This skill does **not** generate a voice. If a line is missing or wrong in the recording, it gets re-recorded; nothing is synthesized to fill the gap, so the film never mixes two voices.

Where it sits:

| Step | Skill |
|---|---|
| Script with voiceover lines and keyframe times | `minara-videoscript` |
| Picture | `minara-video` / `minara-usecase-video` |
| **Voiceover track, cut and placed** | **`minara-voiceover`** |
| BGM ducked under the voiceover | `minara-music` (`--vo assets/vo.wav`) |

Precedent: `V2 UI宣发/minara-v2-ui-promo/audio-src/make_vo.py` cut `narration-full.mp3` by hand into 20 lines. This skill's `align` reproduces those cuts within 0.1s automatically.

## Tool

`scripts/vo.py` (ffmpeg + whisper-cli + numpy, deterministic):

```bash
VO=~/.claude/skills/minara-voiceover/scripts/vo.py
python3 $VO lines  docs/NN-script-<slug>.md -o audio-src/vo-lines.json
python3 $VO align  audio-src/narration.mp3 audio-src/vo-lines.json -o audio-src/vo-clips.json
python3 $VO build  audio-src/vo-clips.json -o assets/vo.wav --duration <film seconds> --split-dir audio-src/vo-lines
python3 $VO mux    renders/<film>-2K-60fps.mp4 assets/vo.wav --bgm assets/bgm-duck.wav -o renders/<film>-2K-60fps-vo.mp4
python3 $VO check  renders/<film>-2K-60fps-vo.mp4 audio-src/vo-clips.json
```

Whisper model: the script uses the first one it finds of `~/.cache/whisper/ggml-small.en.bin` or `ggml-base.en.bin` (or `$WHISPER_MODEL`). If none exists it prints the download command; run it (through a proxy if Hugging Face is blocked).

## Workflow

### 1. Lines and times from the script
`vo.py lines` reads the keyframe sheet in the `minara-videoscript` doc (the table with `Key`, `Time`, `Voiceover` columns). Each row with a voiceover line becomes one entry: key, text, keyframe range, and `at` = range start + 0.25s.

- `at` is the default. Where the script or the operator gives an exact start ("line starts as the card lands at 12.4s"), edit `at` in `vo-lines.json`.
- An older script without a keyframe sheet: write `vo-lines.json` by hand, one entry per line: `{"key": "L1", "text": "…", "range": [0, 2.4], "at": 0.25}`.
- The text must be the approved script text; that's what the recording is matched against.

### 2. Find each line in the recording
`vo.py align` transcribes the recording with word timings, matches the script words to the heard words, then trims each line to where the speech energy actually starts and stops (30 ms kept before, 80 ms after), without crossing into the neighbouring line.

It prints one row per line:

| Column | Meaning |
|---|---|
| `status` | `OK` (≥80% of words matched), `CHECK` (fewer matched; listen to it), `MISSING` (not found), `LONG` (clip is longer than the room it has) |
| `source` | start–end in the recording |
| `len` | clip length |
| `at` / `room` | where it goes in the film, and how long until its keyframe range ends |

Then `Heard but not in script`: words in the recording the script doesn't have. That's usually a misheard word (V2: "finance AI" for "financial agent", which is fine), an ad-lib, or a retake.

Handling:
- **Retakes**: the matcher takes one take per line. If the operator says a later take is better, set that clip's `src` by hand (listen in `--split-dir` output first).
- **CHECK**: listen to the clip. If it's a mishearing, keep it. If the actor said different words, the line needs a re-record or a script change; ask.
- **MISSING**: stop and tell the operator which line has no audio.
- **LONG**: the clip runs past its keyframe range. Options: start it earlier (`at`), let it run into the next range if that range has no line, or ask for a faster read. Never time-stretch the voice.
- Lines joined without a pause (V2 L14 → L15, "…in the background, watching prices…") are cut at the same point on both sides; keep them consecutive in the film or the cut will sound abrupt.

### 3. Show the operator the cue table, don't build yet
Paste the align table into the chat (key, line, film start, length, room, status), plus anything heard-but-not-in-script and every CHECK / MISSING / LONG with the proposed fix. Wait for OK. They edit `at` values, not code.

### 4. Build the track
`vo.py build` places every clip at its `at` on a silent track of the film's length, 15 ms fades on each clip, then normalizes to **-16 LUFS integrated, -1.5 dBTP** (48 kHz mono). It refuses a clip that runs past the end of the film and warns when two lines overlap.

`--split-dir` also writes one wav per line (`K1.wav`, …) for listening.

Per-clip `gain_db` in `vo-clips.json` evens out a line that was read quieter; set it only after listening.

### 5. Put it in the video

**HyperFrames project (the picture is still built in code)** — preferred, so audio and picture render together:
- The composition already has (or gets) an audio element:
  `<audio id="vo" src="assets/vo.wav" data-start="0" data-duration="<film s>" data-track-index="3" data-volume="1"></audio>`
- Write the new track to the file it points at (or point it at the new file); keep the `data-hf-id` that Studio added.
- Rebuild the ducked BGM against the new voiceover: `minara-music` `make_music.py … --vo assets/vo.wav`, and point the BGM element at `bgm-duck.wav`.
- Re-render only when the operator asks (2K60 delivery per the video skills: 4K60 master, then downscale).

**A rendered mp4 (no re-render wanted)** — `vo.py mux`:
- Copies the picture stream untouched (2560×1440 / 60fps stays as is), mixes `vo.wav` (+ `--bgm` ducked music) to stereo AAC 256k 48 kHz, cuts audio to the video length, limiter at -1 dBFS.
- `--vo-db` / `--bgm-db` adjust the balance (start at 0 / 0 with `bgm-duck.wav`; voice should sit clearly above the music).
- Writes a new file next to the original (`…-vo.mp4`); never overwrite the delivered render.

### 6. Check
`vo.py check <result> vo-clips.json` finds every clip in the finished track by cross-correlation (works with music underneath) and prints planned vs found start and a match score. Pass: every line within 0.05s and match ≥0.5. Then:
- `ffprobe` the result: video stream unchanged, one audio stream 48 kHz, duration equals the video.
- Listen to the start, one busy section and the end card in the result (`open -R` the file only if the operator asks).

### 7. Deliver
File path(s) and 3–5 lines: number of lines placed, any CHECK / LONG fixes made, loudness, result path. Don't post the video anywhere; don't send it to groups.

## Rules

- **Timing comes from the script.** Don't move a line to fit the audio without telling the operator; if the picture should move instead, that's a `minara-video` change.
- **Never time-stretch or pitch-shift the voice**, and never synthesize a missing line. Re-record.
- **The recording is the source of truth for words**; the script is the source of truth for timing. If they disagree on words, ask which one changes.
- Keep `vo-lines.json`, `vo-clips.json` and the narration file in `audio-src/` so the track can be rebuilt after any timing change. When the script's timings change, update `at` and run `build` again; don't edit the wav.
- Voiceover sits above music: build the ducked BGM from the final `vo.wav`, not an older one.
- Narration and rendered videos are not committed to git unless the project already tracks them.
