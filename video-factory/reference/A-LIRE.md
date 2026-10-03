# Le standard minimum

`EXEMPLE-RES-01.mp4` est la référence à égaler ou dépasser pour les 49 autres
vidéos. `montage-exemple.py` est le moteur qui l'a produite.
Validé par Youssef le 03/10/2026 — en dessous de ce niveau, on ne livre pas.

## La règle du mockup : élargir le téléphone, jamais rogner le site

C'est le point qui a demandé trois essais.

Les enregistrements d'écran n'ont pas tous le même rapport — de 0,515 pour ATHLA
à 0,598 pour POLYRA. Avec un cadre de largeur fixe, le site est rogné sur les
côtés : sur RES-01, « On ne pose pas un motif » s'affichait « n ne pose as un
motif », et le prix du simulateur était coupé.

**Le cadre du téléphone s'adapte à la capture, pas l'inverse.** On extrait en
`scale=-2:<hauteur>` **sans `crop`**, le montage lit la taille réelle des images
et dessine le cadre autour. Un mockup large se lit très bien ; un site rogné, non.

```python
ECR = sorted((TRAV/"phone").glob("p*.png"))
_e = Image.open(ECR[0]); ECR_W, ECR_H = _e.size; _e.close()
...
pw, phh = ECR_W, ECR_H          # jamais de valeur en dur
px, py = (W-pw)//2, 520
```

## Les autres règles tenues par cet exemple

**Zone de sécurité.** Marges latérales à 10 % (`MARGE = 108`), rien d'important
sous 75 % de hauteur (`BAS_SUR = 1440`). Un fichier 9:16 n'est pas affiché en
9:16 : les téléphones sont en 19,5:9, et Facebook agrandit de 22 % pour remplir
la hauteur, donc il rogne 9 % de chaque côté.

**Durées en nombre d'images, jamais en secondes.** `-frames:v 82`, pas `-t 2.73`.
La somme des plans égale la durée du MP3 à l'image près.

**Calage sur les respirations réelles du MP3.**
`ffmpeg -hide_banner -i voix.mp3 -af "silencedetect=noise=-30dB:d=0.12" -f null -`
(avec `-v error` les filtres n'affichent rien). Les frontières de phrase se
choisissent parmi ces pauses, pondérées par le nombre de syllabes.

**Le mockup montre le site dont parle la voix**, et la queue d'enregistrement est
retirée — voir `captures-communes/A-LIRE.md`.

**Police** : Helvetica Neue index 9 (Condensed Black) pour les titres, index 10
(Medium) pour le texte. L'index 2 est l'italique : piège déjà payé.

**Logo** : `brand-DYOU-sigle.png`, le sigle seul détouré. Pas la vignette carrée.

**Voix** : « D-YOU Agency » dans les scripts, sinon ElevenLabs le lit comme un mot.

**Son** : voix à −16 LUFS, bruitages de `sons/` posés par `outils/mixer_sons.py`,
limiteur à 0,95, pas de musique de fond.

## Ce qui reste perfectible

L'animation est sobre : fondus et translations. Il y a de la marge sans changer
d'outil — typographie révélée mot à mot, courbes d'accélération plutôt que des
fondus linéaires, flou de mouvement sur les entrées, masques qui suivent une
forme, transitions qui portent le sens au lieu d'un simple whoosh.
