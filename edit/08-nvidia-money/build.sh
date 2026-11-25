#!/bin/bash
# Usage: ./build.sh <raw genjutsu clip> <out.mp4>
# Upscale the 480p Genjutsu clip to 720x1280, burn the caption, keep the clip's own audio at -14 LUFS.
set -e
cd "$(dirname "$0")"
python3 cap.py cap.png
ffmpeg -v error -y -i "$1" -i cap.png -filter_complex \
"[0:v]scale=720:1280:flags=lanczos,setsar=1[b];[b][1:v]overlay=0:0,format=yuv420p[v];[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]" \
-map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 160k -movflags +faststart "$2"
echo "built $2"
