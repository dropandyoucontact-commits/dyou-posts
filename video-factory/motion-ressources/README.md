# Ressources motion design — ce qu'on peut vraiment utiliser

Dossier commun à Claude et ChatGPT pour les vidéos motion DYOU et ChinaBook.
Chaque ressource a été vérifiée **le 5 octobre 2026** sur GitHub (licence lue
dans le fichier LICENSE du dépôt, date du dernier commit, nombre d'étoiles).
« Utilisé » = employé dans CB-M01 ; « compatible » = utilisable sans changer
d'outil ; « référence » = à lire ou copier à la main, pas à brancher.

## 1. Les deux chaînes de rendu possibles

| Chaîne | Où elle tourne | Quand la prendre |
|---|---|---|
| **Moteur Python + Skia** (`video-factory/motion/CB-M01/moteur.py`) | Sur le Mac, ou n'importe quelle machine avec Python 3.9+ | Par défaut. Ce qu'on voit en aperçu est exactement ce qui sort : même code, même police, même mesure du texte. |
| **Higgsedit** (CLI Higgsfield v0.14.0, build `f39e3bc5882b`) | Dans le bac à sable Higgsfield (connecteur MCP), jamais en local | Si l'on veut un projet éditable dans l'outil Higgsfield. Lire d'abord la section 4 : le rendu final peut différer des aperçus. |

## 2. Dépôts retenus

| Ressource | Rôle | Licence | Dernier commit | ★ | Statut |
|---|---|---|---|---|---|
| [skia-python/skia-python](https://github.com/skia-python/skia-python) | Moteur de dessin 2D (texte HarfBuzz, ombres, perspective, SVG) | BSD-3-Clause | 2026-09-10 | 326 | **Utilisé** — `pip3 install --user skia-python` |
| [rsms/inter](https://github.com/rsms/inter) | Police Inter et Inter Display (titres) | OFL-1.1 | 2024-11-19 | 19 937 | **Utilisé** — fichiers TTF dans `fontes/`, licence jointe |
| [lucide-icons/lucide](https://github.com/lucide-icons/lucide) | Icônes au trait (usine, colis, ciseaux…) | ISC | 2026-10-04 | 24 860 | **Utilisé** — SVG de `lucide-static` 0.544.0 dans `icones/` |
| [nvkelso/natural-earth-vector](https://github.com/nvkelso/natural-earth-vector) | Contours de pays (carte de Chine) | Domaine public | 2024-04-22 | 2 230 | **Utilisé** — `chine.json` extrait du 1:110m |
| [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Transcription locale, temps de chaque mot | MIT | 2026-10-02 | 54 140 | **Utilisé** — `whisper-cli`, modèle `ggml-small.bin`, gratuit |
| [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) | Encodage H.264, mixage, mesure du volume | LGPL-2.1+ / GPL selon la compilation | 2026-10-04 | 64 766 | **Utilisé** |
| [tabler/tabler-icons](https://github.com/tabler/tabler-icons) | 5 000+ icônes au trait, même style que Lucide | MIT | 2026-10-04 | 21 901 | Compatible — même code d'affichage SVG |
| [gl-transitions/gl-transitions](https://github.com/gl-transitions/gl-transitions) | Transitions GLSL entre deux plans | MIT | 2026-06-22 | 2 145 | Référence — en FFmpeg, utiliser plutôt le filtre intégré `xfade` |
| [ai/easings.net](https://github.com/ai/easings.net) | Courbes d'accélération illustrées | GPL-3.0 | 2026-04-07 | 8 698 | Référence — recopier les valeurs de Bézier, pas le code |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | Motion design en TypeScript (générateurs) | MIT | 2026-07-02 | 19 232 | Alternative si on passe à Node |
| [midrender/revideo](https://github.com/midrender/revideo) | Fork de Motion Canvas avec rendu sans interface | MIT | 2026-07-15 | 4 082 | Alternative si on passe à Node |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Vidéo en React | Licence Remotion : gratuite pour un indépendant ou une société de 3 personnes au plus, payante au-delà | 2026-10-05 | 61 922 | À éviter tant que la licence n'est pas tranchée |
| [airbnb/lottie-web](https://github.com/airbnb/lottie-web) + [Samsung/rlottie](https://github.com/Samsung/rlottie) | Animations Lottie (web) et leur rendu en images | MIT (rlottie : MIT pour l'essentiel, quelques parties sous autre licence) | 2025-09-01 / 2026-09-30 | 32 143 / 1 441 | Compatible via rlottie → images → vidéo |
| [greensock/GSAP](https://github.com/greensock/GSAP) | Animation web (nos sites) | Licence GSAP « no charge » (pas une licence libre standard) | 2026-04-13 | 28 810 | Référence pour les noms de courbes |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Vidéo à partir de pages HTML | Apache-2.0 | 2026-10-05 | 56 944 | Écarté : capture de page web |
| [ManimCommunity/manim](https://github.com/ManimCommunity/manim) | Animation mathématique | MIT | 2026-10-05 | 41 268 | Hors sujet pour nos formats |

Recherche « higgsedit » sur GitHub : aucun dépôt de l'outil lui-même (il est
fermé, livré dans le bac à sable Higgsfield). Seules des mentions dans des
collections de prompts.

## 3. Utiliser le moteur Python + Skia

```sh
pip3 install --user skia-python numpy pillow scipy
cd video-factory/motion/CB-M01
python3 rendu.py apercu 0.5 4.2 12.0      # planche d'aperçus dans apercus/
python3 rendu.py video                    # renders/image.mp4, 3 processus
python3 outils/sons.py                    # 18 bruitages synthétisés (aucune licence)
python3 outils/mixer.py renders/image.mp4 # mixage FFmpeg → video/CB-M01.mp4
```

Ce qui fait la qualité, à reprendre d'une vidéo à l'autre :

- **Texte** : toujours `texte()` / `largeur()` du moteur, qui mesurent et dessinent
  avec la même mise en page HarfBuzz. Jamais de position de mot calculée avec une
  autre police que celle qui dessine.
- **Minutage** : `whisper-cli -ml 1 -sow -oj` donne un mot par segment ;
  `outils/minutage.py` recale chaque phrase sur la fin du silence qui la précède
  (whisper avance de 0,1 à 0,15 s en début de phrase).
- **Perspective** : `Espace(c, cx, cy, rx=, ry=, rz=, s=)` projette vraiment les
  quatre coins (pas un simple cisaillement).
- **Flou de mouvement** : déclarer les fenêtres rapides avec `rapide(t0, t1)` ;
  le moteur y moyenne 5 sous-images.
- **Sons** : déclarés avec `son(t, nom, gain)` à côté de l'animation qu'ils
  accompagnent ; `mixer.py` atténue les bruitages sous la voix (sidechain) et
  vise −16 LUFS.
- **Vérification** : extraire des images **du MP4 final** (`ffmpeg -ss T -i
  video/CB-M01.mp4 -frames:v 1`), pas seulement des aperçus.

## 4. Higgsedit : pièges constatés le 5 octobre 2026

1. **Police différente au rendu final.** Les aperçus `p.frame()` utilisaient
   Inter ; l'export `p.render()` sur 8 processus a basculé sur une police de
   secours plus large : mots collés, libellés passés à la ligne et sortis des
   cadres. Toujours vérifier des images extraites du MP4 exporté.
2. **Les masques grandissent depuis leur centre.** Animer `maskWidth` de 1 à W
   ne dévoile que la moitié gauche. Poser le masque à `x: -0.5` et animer
   jusqu'à `2 × W`.
3. **Plusieurs `p.compose` qui se chevauchent** peuvent tomber sur la même
   piste et se refuser (« overlaps clip … on track 3 »). Faire une seule
   composition dont chaque scène est un enfant `frame` avec `at` et `duration`.
4. **Pivots** : un `group` tourne et grandit autour du coin haut-gauche de
   l'écran ; un `frame` autour de son propre coin, sauf avec `origin: "center"`.
   Un très grand cercle posé hors champ ne pivote pas sur son centre.
5. Toutes les clés d'animation doivent tenir dans la durée de vie du nœud,
   sinon la construction échoue.
6. Le bac à sable est effacé ~10 s après chaque appel : envoyer les fichiers
   par `media_upload`, pas par des poussées successives sur ce dépôt public.
