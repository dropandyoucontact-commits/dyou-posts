#!/bin/bash
set -e
cd "$(dirname "$0")"
T=_travail/RES-01
A=../videos/RES-01/audio/RES-01.mp3
mkdir -p ../videos/RES-01/video
ffmpeg -v error -y -framerate 30 -i $T/frames/f%04d.png \
  -c:v libx264 -profile:v high -preset slow -crf 18 -pix_fmt yuv420p -r 30 -an $T/muet.mp4
ffmpeg -v error -y -i $T/muet.mp4 -i "$A" \
  -filter_complex "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -ar 44100 -ac 2 \
  -movflags +faststart -shortest ../videos/RES-01/video/RES-01.mp4
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height -of default=noprint_wrappers=1 ../videos/RES-01/video/RES-01.mp4
