# CB-M01 « Le réseau en direct » — projet source

Vidéo ChinaBook verticale 1080 × 1920, 60 i/s, 59,4 s, fond blanc, noir et vert.
Composée en Python avec Skia (pas de navigateur, pas de capture d'écran) :
chaque image est une fonction pure du temps, donc l'aperçu et la vidéo finale
sortent du même code.

## Fichiers

| Fichier | Rôle |
|---|---|
| `scenes.py` | Les 13 scènes, les sous-titres karaoké, les sons et les fenêtres de flou. C'est ici qu'on modifie la vidéo. |
| `moteur.py` | Briques communes : texte mesuré (HarfBuzz), cartes, ombres, images, icônes SVG, perspective 3D, confettis, encodage. |
| `rendu.py` | `apercu` (planche d'images) et `video` (rendu complet sur 3 processus). |
| `timing.json` | Temps de chaque mot de la voix (whisper.cpp recalé sur les respirations). |
| `chine.json` | Contour de la Chine (Natural Earth, domaine public). |
| `media/` | Voix, produits détourés (PNG transparents), logos recolorés. |
| `fontes/`, `icones/` | Inter (OFL) et icônes Lucide (ISC). |
| `outils/` | `sons.py` (bruitages synthétisés), `mixer.py` (mixage FFmpeg), `minutage.py`, `detourer.py`, `decoupage.py`. |
| `DECOUPAGE.md` | Le découpage final : plans et sous-titres avec leurs temps réels. |

## Refaire la vidéo

```sh
pip3 install --user skia-python numpy pillow scipy
python3 rendu.py apercu 1.0 6.5 17.9 36.6 52.4   # aperçus/planche.jpg
python3 rendu.py video                            # renders/image.mp4 (~20 min sur le Mac de 2015)
python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
python3 outils/sons.py                            # sons/*.wav
python3 outils/mixer.py renders/image.mp4         # video/CB-M01.mp4, voix à -16 LUFS
```

## Changer de voix ou de texte

1. Nouvelle voix dans `media/voix.mp3`, puis transcription mot à mot :
   `whisper-cli -m ~/.local/share/whisper-models/ggml-small.bin -l fr -f voix16.wav -ml 1 -sow -oj -ojf -of mots`
2. `python3 outils/minutage.py` régénère `timing.json`.
3. Dans `scenes.py`, `SOUS` liste les sous-titres par indice de mot. Les scènes
   citent aussi des indices (`TW(60)` = le mot « mois ») : tout se recale seul
   tant que l'ordre des phrases ne change pas.

## Règles tenues

- Aucun prix, marge ou résultat chiffré inventé : les barres et tickets n'ont
  pas de nombres. « 14 jours » vient de la voix (« deux semaines »).
- L'échange avec le fournisseur est marqué « Échange illustratif ».
- Marques visibles sur les produits non citées.
- Rien d'important sous 1 440 px ni à moins de 70 px des bords.
