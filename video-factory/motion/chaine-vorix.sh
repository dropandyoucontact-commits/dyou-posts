#!/bin/sh
# VX-M02 : rendu puis deux voix ; VX-M01 : rendu puis voix. Journal : chaine-vorix.log
set -e
cd ~/Desktop/dyou-posts/video-factory/motion/VX-M02
rm -f renders/image.mp4 renders/seg*.mp4 renders/segments.txt
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1
./mixer-deux-voix.sh > mix-log.txt 2>&1
echo "VX-M02 OK $(date +%H:%M)"
cd ../VX-M01
rm -f renders/image.mp4 renders/seg*.mp4 renders/segments.txt
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 renders/image.mp4 > mix-log.txt 2>&1
echo "VX-M01 OK $(date +%H:%M)"
