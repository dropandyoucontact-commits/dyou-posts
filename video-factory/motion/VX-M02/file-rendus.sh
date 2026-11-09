#!/bin/sh
# file d'attente : VX-M01-sombre (v3), puis VX-M02 détouré, puis VX-M02-pub détouré
cd "$(dirname "$0")/../VX-M01-sombre" && ./rendre.sh > rendre.log 2>&1; tail -1 rendre.log
cd ../VX-M02 && rm -rf renders/cache-videos renders/seg*.mp4
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1 || { echo "RENDU VX-M02 KO"; exit 1; }
/usr/bin/python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -1
echo "VX-M02 OK $(date +%H:%M)"
rm -rf ../VX-M02-pub/renders/cache-videos
sh ../VX-M02-pub/rendre.sh
echo "FILE TERMINEE $(date +%H:%M)"
