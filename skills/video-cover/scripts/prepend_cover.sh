#!/usr/bin/env bash
# Put the cover on the first frames of a video so platforms that take the first frame as the
# thumbnail (X, Telegram, Discord, many players) show the cover.
#
# Usage: prepend_cover.sh <video> <cover.png> <out.mp4> [seconds=0.1] [WxH]
#   seconds  how long the cover holds; default 0.1s (6 frames at 60fps): visible to a thumbnail
#            grabber, barely noticeable when watching. Keep it ≤ 0.2s.
#   WxH      output size; default = the input video's size. Pass e.g. 2560x1440 when the input is a
#            4K master, so the film is scaled once (lanczos) instead of re-encoding the delivered file.
# The audio is delayed by the same amount (silence in front), so picture and sound stay in sync.
# Output: H.264 yuv420p, CRF 16 (CRF=14 in the environment to override), AAC 192k, +faststart, same fps as the input.
set -euo pipefail
[ $# -ge 3 ] || { sed -n '2,12p' "$0"; exit 2; }
IN="$1"; COVER="$2"; OUT="$3"; DUR="${4:-0.1}"; SIZE="${5:-}"; CRF="${CRF:-16}"

IFS=, read -r W H FPS < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$IN")
if [ -n "$SIZE" ]; then W="${SIZE%x*}"; H="${SIZE#*x}"; fi
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | head -1)

V="[0:v]scale=${W}:${H}:force_original_aspect_ratio=decrease:flags=lanczos,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${FPS},format=yuv420p,trim=duration=${DUR},setpts=PTS-STARTPTS[c];[1:v]scale=${W}:${H}:flags=lanczos,setsar=1,fps=${FPS},format=yuv420p[m];[c][m]concat=n=2:v=1:a=0[v]"
if [ -n "$HAS_AUDIO" ]; then
  MS=$(python3 -c "print(int(round(float('$DUR')*1000)))")
  ffmpeg -v error -y -loop 1 -framerate "$FPS" -i "$COVER" -i "$IN" \
    -filter_complex "$V;[1:a]adelay=${MS}:all=1[a]" -map "[v]" -map "[a]" \
    -c:v libx264 -preset slow -crf "$CRF" -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  ffmpeg -v error -y -loop 1 -framerate "$FPS" -i "$COVER" -i "$IN" \
    -filter_complex "$V" -map "[v]" -c:v libx264 -preset slow -crf "$CRF" -pix_fmt yuv420p -movflags +faststart "$OUT"
fi
echo "Wrote $OUT"
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact=p=0 "$OUT"
