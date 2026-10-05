# CB-M01 « Le réseau en direct » — la vidéo de référence

Vidéo ChinaBook verticale 1080 × 1920, 60 i/s, 59,4 s, fond blanc, noir et vert.
C'est le standard de toutes les vidéos motion (voir `../../reference/A-LIRE.md`).
Composée en Python avec Skia, sans navigateur ni capture d'écran : chaque image est une
fonction pure du temps, donc l'aperçu et la vidéo finale sortent du même code.

## Fichiers

| Fichier | Rôle |
|---|---|
| `scenes.py` | Les 13 scènes, les sous-titres karaoké, les sons et les fenêtres de flou. C'est ici qu'on modifie la vidéo. |
| `timing.json` | Temps de chaque mot de la voix (whisper.cpp recalé sur les respirations : la voix a été fournie, pas générée). |
| `chine.json` | Contour de la Chine (Natural Earth, domaine public). |
| `media/` | Voix, produits détourés (PNG transparents), logos recolorés. |
| `outils/decoupage.py` | Régénère `DECOUPAGE.md`, le découpage final avec les temps réels. |
| `sfx.json` | Les 180 bruitages (temps, son, gain) émis par `scenes.py`. |
| `video/CB-M01.mp4` | La vidéo livrée. |

Le moteur, les polices, les icônes et les outils communs sont dans `../moteur/`.

## Refaire la vidéo

```sh
cd video-factory/motion/CB-M01
python3 ../moteur/rendu.py apercu 1.0 6.5 17.9 36.6 52.4   # apercus/planche.jpg
python3 ../moteur/rendu.py video                            # renders/image.mp4 (~5 min)
python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
python3 ../moteur/outils/sons.py                            # une fois : ../moteur/sons/*.wav
python3 ../moteur/outils/mixer.py renders/image.mp4         # video/CB-M01.mp4, voix à -16 LUFS
python3 ../moteur/outils/verifier.py video/CB-M01.mp4 0 5 10 20 30 40 50 59
```

La voix de CB-M01 a été fournie par Youssef ; son minutage vient de whisper.cpp :
`whisper-cli -m ~/.local/share/whisper-models/ggml-small.bin -l fr -f voix16.wav -ml 1 -sow -oj -ojf -of mots`,
puis `python3 ../moteur/outils/minutage.py`. Pour une voix générée par nous, utiliser
`../moteur/outils/voix.py`, qui donne le minutage directement.

## Règles tenues

- Aucun prix, marge ou résultat chiffré inventé : les barres et tickets n'ont pas de
  nombres. « 14 jours » vient de la voix (« deux semaines »).
- L'échange avec le fournisseur est marqué « Échange illustratif ».
- Marques visibles sur les produits non citées.
- Rien d'important sous 1 440 px ni à moins de 70 px des bords.
