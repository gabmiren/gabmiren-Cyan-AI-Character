#!/bin/bash
set -e
M=/mnt/user-data/uploads/Downloads/zephiramusic-lofi-tech-588185.mp3
declare -A OUT=([p1_glossary]=cyan_glossary_text_v1 [p2_backwards]=cyan_readbackwards_text_v1 [p3_rules]=cyan_headtrader_rules_text_v1 [p4_sessions]=cyan_sessions_ranked_text_v1 [p5_drawdown]=cyan_trailing_drawdown_text_v1)
for p in p1_glossary p2_backwards p3_rules p4_sessions p5_drawdown; do
  read bg loops ms < <(python3 -c "import json;s=json.load(open('specs.json'))['$p'];print(s['bg'],s['loops'],s['music'])")
  D=$(python3 -c "print(round($loops*7.541667,3))"); FO=$(python3 -c "print($D-1.2)")
  ffmpeg -v error -y -stream_loop $((loops-1)) -i /home/claude/bg/$bg.mp4 -loop 1 -i $p.png -ss $ms -i $M \
    -filter_complex "[0:v][1:v]overlay=shortest=1,format=yuv420p[v];[2:a]atrim=0:$D,asetpts=PTS-STARTPTS,afade=t=in:d=0.4,afade=t=out:st=$FO:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]" \
    -map "[v]" -map "[a]" -t $D -c:v libx264 -preset veryfast -crf 20 -r 24 -c:a aac -b:a 160k -movflags +faststart ${OUT[$p]}.mp4
  echo "${OUT[$p]}.mp4 $D s"
done
