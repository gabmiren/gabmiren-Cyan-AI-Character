#!/bin/bash
# $1 = audio source (video or audio file with the ref-timeline track), $2 = output
set -e
A=g1.mp4; B=g2.mp4; C=/home/claude/refs8/tv_cockpit.mp4
ffmpeg -v error -y -i $A -i $C -i $B -i cap.png -i "$1" -filter_complex "\
[0:v]scale=720:1280:flags=lanczos,fps=30,trim=0:4.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.39[a];\
[1:v]scale=720:1280,fps=30,setpts=PTS-STARTPTS[c];\
[2:v]scale=720:1280:flags=lanczos,fps=30,trim=0:2.12,setpts=PTS-STARTPTS[b];\
[a][c][b]concat=n=3:v=1:a=0,format=yuva420p[v];[v][3:v]overlay=0:0,format=yuv420p[o]" \
-map "[o]" -map 4:a -c:v libx264 -crf 17 -c:a aac -b:a 192k -shortest "$2"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$2"
