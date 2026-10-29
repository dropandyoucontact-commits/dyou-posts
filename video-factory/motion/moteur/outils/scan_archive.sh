#!/bin/bash
# balaye un fichier distant : 1 image toutes les N secondes, en parallèle, sans le télécharger
U="$1"; SORTIE="$2"; DEBUT="$3"; FIN="$4"; PAS="$5"
mkdir -p "$SORTIE"; rm -f "$SORTIE"/*.jpg
n=0
for (( s=DEBUT; s<FIN; s+=PAS )); do
  ffmpeg -v error -ss "$s" -i "$U" -frames:v 1 -vf "scale=300:-1,drawtext=text='%{eif\\:$s/60\\:d}min':x=6:y=6:fontsize=22:fontcolor=red:box=1:boxcolor=black" -y "$SORTIE/$(printf %04d $n)_${s}s.jpg" 2>/dev/null || \
  ffmpeg -v error -ss "$s" -i "$U" -frames:v 1 -vf "scale=300:-1" -y "$SORTIE/$(printf %04d $n)_${s}s.jpg" 2>/dev/null &
  n=$((n+1))
  if (( n % 4 == 0 )); then wait; fi
done
wait
ls "$SORTIE"/*.jpg | wc -l
