#!/bin/sh
cd "$(dirname "$0")"
pkill -f "rendu\.py vid[e]o"; sleep 2; pkill -9 -f "rendu\.py vid[e]o"; sleep 1
echo "processus restants : $(pgrep -f 'rendu\.py vid[e]o' | wc -l | tr -d ' ')"
rm -f renders/seg*.mp4 renders/segments.txt
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1 || { echo "RENDU KO"; exit 1; }
/usr/bin/python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -2
# plus de musique de la banque (Youssef, 31/10 : « générique », silence ou trailer sérieux) — voix seule
echo "VX-M02-pub OK $(date +%H:%M)"
