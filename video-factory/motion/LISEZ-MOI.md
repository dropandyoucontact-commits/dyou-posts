# Faire une nouvelle vidéo motion

Le niveau à tenir : `CB-M01/video/CB-M01.mp4` (voir `../reference/A-LIRE.md`).
Toutes les commandes se lancent **depuis le dossier de la vidéo**.

```sh
# 0. une fois par machine
pip3 install --user skia-python numpy pillow scipy
python3 moteur/outils/sons.py                 # 18 bruitages synthétisés dans moteur/sons/

# 1. le dossier de la vidéo
mkdir -p MON-ID/media && cd MON-ID
cp ../CB-M02/scenes.py .                       # point de départ : il s'appuie sur moteur/kit.py
#    écrire script.txt (la voix exacte), déposer les produits détourés dans media/

# 2. la voix (ElevenLabs, Tomy) et le temps de chaque mot
python3 ../moteur/outils/voix.py --etat        # coût et crédits restants
python3 ../moteur/outils/voix.py               # media/voix.mp3 + timing.json, 3,5 mots/s
python3 ../moteur/outils/voix.py --debit 3.8   # plus vite, sans regénérer (gratuit)

# 3. les scènes : écrire scenes.py (SOUS = sous-titres par indice de mot, une fonction par scène)
python3 ../moteur/rendu.py apercu 0.5 3 8 15   # apercus/planche.jpg

# 4. la vidéo
python3 ../moteur/rendu.py video               # renders/image.mp4, ≈ 5 min pour 60 s
python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
python3 ../moteur/outils/mixer.py renders/image.mp4      # video/MON-ID.mp4, −16 LUFS

# 5. vérifier LE FICHIER FINAL
python3 ../moteur/outils/verifier.py video/MON-ID.mp4 0.0 2 5 10 20 30 40 50
```

`moteur/kit.py` fournit les briques au standard : sous-titres karaoké (`SousTitres`), fond,
bandeau, pastilles, tampons, téléphone, bulles, éclairs, registres de sons et de flou.
Les logos et produits ChinaBook sont dans `moteur/media/` (un `media/` de projet passe devant).

Dans `scenes.py` : `DUREE` = durée de la voix + 1,5 s de carton final ; chaque animation
cite le mot qu'elle illustre (`TW(i)`) ; chaque son est déclaré à côté de son animation
(`son(t, "pop", -14)`) ; les mouvements rapides sont signalés (`rapide(t0, t1)`) pour le
flou de mouvement.

Voix fournie au lieu d'être générée : la déposer en `media/voix.mp3`, la transcrire avec
whisper.cpp (`whisper-cli -ml 1 -sow -oj …`, voir `CB-M01/LISEZ-MOI.md`), puis
`python3 ../moteur/outils/minutage.py`.
