#!/bin/sh
# attend la fin du rendu VX-M01-sombre, détoure les rushes, remplace les clips dans les deux projets, re-rend les deux
cd "$(dirname "$0")"
while pgrep -f "VX-M01-sombre/rendre.sh" >/dev/null || pgrep -f "rendu.py video" >/dev/null; do sleep 30; done
echo "détourage $(date +%H:%M)"
/usr/bin/python3 outils/detourer_rushes.py plages-detourage.json 2>&1 | grep -v Warning || { echo "DETOURAGE KO"; exit 1; }
for p in . ../VX-M02-pub; do
  sed -i.bak-sans-detourage -e 's#"videos/IMG_3413"#"videos/IMG_3413-d"#g; s#"videos/IMG_3412"#"videos/IMG_3412-d"#g; s#"videos/IMG_3416"#"videos/IMG_3416-d"#g' $p/scenes.py
done
echo "rendu VX-M02 $(date +%H:%M)"
rm -rf renders/cache-videos renders/seg*.mp4
/usr/bin/python3 ../moteur/rendu.py video > renders-log.txt 2>&1 || { echo "RENDU VX-M02 KO"; exit 1; }
/usr/bin/python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 --ecart 9 renders/image.mp4 | tail -1
echo "VX-M02 OK $(date +%H:%M)"
sh ../VX-M02-pub/rendre.sh
