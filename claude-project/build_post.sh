#!/bin/bash
# Usage: ./build_post.sh <overlay.png> <background_loop.mp4> <audio.mp3> <out.mp4>
# Current recipe (23 Nov 2026): 10s, no blur, 9.54s logo loop retimed to 10s so it stays seamless,
# first 10s of the track, 1s fade-out, -14 LUFS.
set -e
OV=$1; BG=$2; AU=$3; OUT=$4
ffmpeg -v error -y -i "$BG" -loop 1 -i "$OV" -i "$AU" -filter_complex \
"[0:v]setpts=PTS*10/9.541667,fps=24[b];[b][1:v]overlay=shortest=1,format=yuv420p[v];\
[2:a]atrim=0:10,asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st=9:d=1.0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]" \
-map "[v]" -map "[a]" -t 10 -c:v libx264 -preset veryfast -crf 20 -r 24 -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "built $OUT"
