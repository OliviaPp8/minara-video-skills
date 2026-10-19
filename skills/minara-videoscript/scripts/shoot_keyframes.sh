#!/bin/bash
# Screenshot keyframes from a keyframe source page (one .k frame per keyframe, toggled by ?k=K1;
# older V2 source pages use #k1, which is passed too).
# Usage: shoot_keyframes.sh <source.html> <out_dir> [landscape|portrait] K1 K2 ...
# Output: <out_dir>/K1.png ... at 2560x1440 (landscape) or 1440x2560 (portrait).
set -e
SRC="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; OUT="$2"; ORI="${3:-landscape}"; shift 3
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ "$ORI" = portrait ]; then W=1080; H=1920; else W=1920; H=1080; fi
mkdir -p "$OUT"
for K in "$@"; do
  "$CHROME" --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --force-device-scale-factor=1.3333333 --window-size=$W,$H \
    --virtual-time-budget=3000 --screenshot="$OUT/$K.png" "file://$SRC?k=$K#$(echo $K | tr A-Z a-z)" 2>/dev/null
  sips -g pixelWidth -g pixelHeight "$OUT/$K.png" | awk -v k="$K" '/pixel/{d=d" "$2} END{print k":"d}'
done
