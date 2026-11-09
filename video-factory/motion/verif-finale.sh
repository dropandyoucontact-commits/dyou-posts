#!/bin/sh
# Planche zone sûre tirée des MP4 FINAUX (pas des aperçus) : 8 images par film, passées dans zone_tiktok.py
set -e
cd ~/Desktop/dyou-posts/video-factory/motion
S=/private/tmp/claude-501/-Users-mohamedelhadad/b5e2408f-df1b-43ec-af59-68f07524612a/scratchpad
for V in VX-M02/video/VX-M02.mp4 VX-M01/video/VX-M01.mp4; do
  n=$(basename "$V" .mp4); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
  rm -rf "$S/zf-$n"; mkdir -p "$S/zf-$n"
  ffmpeg -v error -y -i "$V" -vf "fps=8/$d" "$S/zf-$n/f%02d.png"
  /usr/bin/python3 moteur/outils/zone_tiktok.py "$S"/zf-$n/f*.png -o "$S/zone-finale-$n.jpg"
  echo "$n : $(ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$V" | tr '\n' '+') $(printf '%.2f' "$d") s"
done
