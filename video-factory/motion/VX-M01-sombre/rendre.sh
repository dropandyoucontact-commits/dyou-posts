#!/bin/sh
cd "$(dirname "$0")"
rm -f renders/seg*.mp4 renders/segments.txt
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1 || { echo "RENDU KO"; exit 1; }
/usr/bin/python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
/usr/bin/python3 mix-sans-voix.py | tail -2
echo "VX-M01-sombre OK $(date +%H:%M)"
