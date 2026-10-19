---
name: minara-guide-video
description: Create Minara product guide/tutorial videos from screen recordings supplied by the operator. Use for /minara-guide-video, “给录屏加字幕配音”, retiming a new recording cut, building a timeline approval player, or correcting caption/product meaning. Drives caption-recording from source analysis through pre-render approval, final verification, and local delivery. Not for synthetic HyperFrames marketing videos.
---

# minara-guide-video

Use this for real Minara screen recordings. the operator records the product; add a detailed but concise
English voiceover and captions. Load and follow the `caption-recording` skill for all mechanics.

## Required sequence

1. Probe the new source. Rebuild its timeline even if an older walkthrough looks similar.
2. Extract frames every 3–5 seconds; use 0.5–1 second spacing around every transition. Repeat until
   each screen/panel boundary has a defensible timestamp.
3. Write short sentences in screen order. Explain the visible task and verified product meaning.
   Do not infer relationships between nearby controls.
4. Use explicit `start` anchors for every flat cue. Run:

   ```bash
   python ~/.claude/skills/caption-recording/scripts/caption_footage.py <video_dir> --prepare-only
   python ~/.claude/skills/caption-recording/scripts/make_review_page.py <video_dir> --open
   ```

5. **Stop at the player review page and wait for the operator's confirmation.** Do not encode the MP4
   merely because the timeline looks plausible.
6. Apply every cue/time/product-copy correction and refresh the prepared timing.
7. Only after approval, run `caption_footage.py <video_dir>` to render.
8. Extract an output frame at every cue midpoint. For every adjusted cue, also inspect near its
   start and end. Correct and repeat the render/check loop if any screen, caption, or voice drifts.
9. Deliver the MP4 locally and highlight it in Finder when requested.

The player page is a hard approval gate, not an optional post-render accessory. It defaults to the
raw source, overlays the planned cue live, exposes narration gaps, supports fine seeking and speed,
and copies cue-specific feedback back into chat.

## Copy rules

- Use practitioner language and short TTS-safe sentences.
- Name what is actually visible at that moment.
- Verify product semantics. For example, profit-share rate changes the creator's share, not the
  settlement schedule; Subscriber Overview reports creator subscribers, AUM, and profit share,
  independent of live-run controls.
- A user-specified voice speed overrides the normal default.

## Delivery rule

Do **not** send videos to any chat, channel or group by default. Send only when the operator
explicitly requests it in the current task. If they say not to send, treat that as absolute.


