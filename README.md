# Minara video skills

Six [Claude Code](https://claude.com/claude-code) skills for making product videos end to end: script, picture, voiceover, music. They were built for Minara's launch, promo and tutorial films, and they encode one team's rules (brand palette, Geist type, a signature ease, 2K 60fps delivery). Fork them and swap in your own rules.

| Skill | What it does |
|---|---|
| [`minara-videoscript`](skills/minara-videoscript/SKILL.md) | Writes the script before any animation: a keyframe sheet where every still keyframe (rendered from UI code, exported from Figma, or AIGC-generated) carries its picture, voiceover, on-screen text, timing and music. Calm, natural English voice. |
| [`minara-video`](skills/minara-video/SKILL.md) | Marketing / launch / demo films built in HTML with [HyperFrames](https://hyperframes.heygen.com): storyboard board, per-second timeline, local test page with a frame scrubber, render. |
| [`minara-usecase-video`](skills/minara-usecase-video/SKILL.md) | Use case and beginner tutorial videos that rebuild the product UI faithfully (mobile or desktop), plus cover images. |
| [`minara-guide-video`](skills/minara-guide-video/SKILL.md) | Adds voiceover and captions to a screen recording you supply (uses a separate `caption-recording` skill for the mechanics, not included). |
| [`minara-voiceover`](skills/minara-voiceover/SKILL.md) | Cuts a narration recording into the script's lines, places each one at its scripted time, mixes it into the video and checks every line lands on time. |
| [`minara-music`](skills/minara-music/SKILL.md) | Generates BGM and synced sound effects locally from the script's cue sheet (numpy synth, deterministic), ducked under the voiceover. |

Typical order: `minara-videoscript` → `minara-video` or `minara-usecase-video` → `minara-voiceover` → `minara-music`.

## Install

```bash
git clone https://github.com/OliviaPp8/minara-video-skills.git
mkdir -p ~/.claude/skills
for d in minara-video-skills/skills/*/; do ln -s "$PWD/$d" ~/.claude/skills/; done
```

Then call them in Claude Code, e.g. `/minara-videoscript`.

## Requirements

- `ffmpeg` / `ffprobe`, Python 3 with `numpy`, Google Chrome (headless screenshots)
- Node.js for HyperFrames (`npx hyperframes`)
- `whisper-cli` ([whisper.cpp](https://github.com/ggerganov/whisper.cpp)) and a model in `~/.cache/whisper/` for `minara-voiceover`

## Paths the skills expect

| Variable | Meaning |
|---|---|
| `$VIDEO_WORKSPACE` | Where video projects and reference libraries live (e.g. `~/video-workspace`). `minara-video` reads [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft), and optionally [remocn](https://remocn.dev) and [snapcn](https://snapcn.dev), from here. |
| `$BRAND_DIR` | Your brand's `design.md` (colour, type, spacing tokens) and `logo/` folder. |

## Notes

- Brand assets are not included. The Minara name and logo are trademarks of their owner; bring your own logo.
- The Geist font file in `minara-usecase-video/assets/cover/` is © The Geist Project Authors, licensed under the SIL Open Font License 1.1 (`OFL-Geist.txt`).
- The skills are written in English. A few Chinese phrases remain on purpose: they are trigger words the operator types and UI labels in the HTML templates.

## License

MIT, see [LICENSE](LICENSE).
