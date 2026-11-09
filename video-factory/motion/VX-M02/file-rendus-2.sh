#!/bin/sh
# VX-M02 puis VX-M02-pub, fond neutre + rushes détourés + pastilles blanches
cd "$(dirname "$0")"
rm -f renders/seg*.mp4
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1 || { echo "RENDU VX-M02 KO"; exit 1; }
/usr/bin/python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -1
echo "VX-M02 OK $(date +%H:%M)"
sh ../VX-M02-pub/rendre.sh
echo "FILE TERMINEE $(date +%H:%M)"
