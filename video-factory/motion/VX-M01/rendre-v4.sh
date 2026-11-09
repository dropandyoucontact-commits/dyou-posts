#!/bin/sh
cd "$(dirname "$0")"
pkill -f "rendu.py video"; sleep 2; pkill -9 -f "rendu.py video"; sleep 1
echo "processus restants : $(pgrep -f 'rendu.py video' | wc -l | tr -d ' ')"
rm -f renders/seg*.mp4 renders/segments.txt
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1 || { echo "RENDU KO"; exit 1; }
/usr/bin/python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -2
echo "VX-M01 OK $(date +%H:%M)"
