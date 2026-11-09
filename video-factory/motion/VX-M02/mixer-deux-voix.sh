#!/bin/sh
# Même image, deux voix : A (cagoulé, media/voix.mp3) → video/VX-M02.mp4 ; B (Tomy pub, calée) → video/VX-M02-pub.mp4
set -e
cd "$(dirname "$0")"
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -2
cp media/voix.mp3 media/voix-A-cagoule.mp3; cp timing.json timing-A.json
cp voix-ads/media/voix-calee.mp3 media/voix.mp3
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -2
mv video/VX-M02.mp4 video/VX-M02-pub.mp4
cp media/voix-A-cagoule.mp3 media/voix.mp3
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -1
ls -la video/*.mp4 | awk '{print $9, $5}'
