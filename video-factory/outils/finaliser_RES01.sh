#!/bin/bash
set -e
cd "$(dirname "$0")"
T=_travail/RES-01
mkdir -p ../videos/RES-01/video
ffmpeg -v error -y -framerate 30 -i $T/frames/f%04d.png \
  -c:v libx264 -profile:v high -preset slow -crf 18 -pix_fmt yuv420p -r 30 -an $T/muet.mp4
# la piste porte deja la voix normalisee + les bruitages
ffmpeg -v error -y -i $T/muet.mp4 -i $T/piste.wav \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -movflags +faststart -shortest ../videos/RES-01/video/RES-01.mp4
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height -of default=noprint_wrappers=1 ../videos/RES-01/video/RES-01.mp4
