# Exemple de montage à reproduire

`EXEMPLE-montage-resine.mp4` — 1080 × 1920, 25,80 s, 774 images, 4,3 Mo.
`render-exemple.py` est le moteur qui l'a produit : c'est le squelette à reprendre
pour les 50 vidéos de la bibliothèque.

Cette vidéo n'appartient à aucun ID du manifeste : son texte vient d'un script
antérieur à la factory. Elle sert de **référence de charte**, pas de livrable.

## Les huit plans

| # | Images | Durée | Contenu | Fond |
|---|--------|-------|---------|------|
| 1 | 82 | 2,73 s | « Tu poses des sols en résine / qui transforment une pièce. » | photo |
| 2 | 50 | 1,67 s | « Mais pour décrocher un chantier… » + carte | violet |
| 3 | 120 | 4,00 s | « Tes soirées dans les messages. » + conversation | photo |
| 4 | 98 | 3,27 s | « Les mêmes questions. » + trois cartes | violet |
| 5 | 49 | 1,63 s | signature DYOU Agency | violet |
| 6 | 177 | 5,90 s | « Un site pour montrer ton travail. » + mockup | violet |
| 7 | 117 | 3,90 s | « Ton savoir-faire mérite mieux. » + carte | photo |
| 8 | 81 | 2,70 s | CTA « Écris résine » + bouton | violet |

L'alternance fond photo / fond violet du point 4 du contrat est tenue : 1 photo,
2 violet, 3 photo, 4 violet, 5 violet, 6 violet, 7 photo, 8 violet.

## Les règles que ce montage applique

**Durées posées en nombre d'images, jamais en secondes.** `-frames:v 82`, pas
`-t 2.73`. Sinon les arrondis s'accumulent : 0,12 s de dérive sur sept plans au
premier essai. Somme des plans = durée exacte du MP3.

**Calage sur les respirations réelles du MP3**, pas sur une durée estimée :
`ffmpeg -hide_banner -i voix.mp3 -af "silencedetect=noise=-35dB:d=0.20" -f null -`
Attention : avec `-v error` les filtres n'affichent rien, il faut `-hide_banner`.

**Zone de sécurité 9:16.** Un fichier 9:16 n'est pas affiché en 9:16 : les écrans
de téléphone sont en 19,5:9, et Facebook agrandit la vidéo de 22 % pour remplir la
hauteur — il rogne **9 % à gauche et 9 % à droite**. D'où, dans `render-exemple.py` :
- `MARGE = 108` px, soit 10 % — jamais moins ;
- `BAS_SUR = 1440` px, soit 75 % — rien d'important en dessous, c'est là que se
  posent la légende, le nom de la Page et les boutons.
Mesuré le 03/10/2026 sur un cas réel : un texte s'arrêtant à 5 % du bord perdait
une lettre de chaque côté à la publication.

**Police** : Helvetica Neue, index 9 (Condensed Black) pour les titres,
index 10 (Medium) pour le texte courant. **L'index 2 est l'italique** — piège déjà
payé, les puces sortaient penchées.

**Preuves réelles en mockup, pas en image générée.** Le plan 6 affiche la vraie
navigation POLYRA en vidéo dans le cadre du téléphone (177 images extraites de la
capture), pas une suite de captures fixes.

**Son** : voix normalisée à −16 LUFS, crête à −1,5 dBTP. Pas de musique de fond.

## Ce qu'il reste à faire pour les 50

Relevé sur le disque au 03/10/2026 : **39 dossiers ont 1 image sur les 3 prévues**,
11 n'en ont aucune, **aucun MP3 n'est déposé**, et une seule capture vidéo existe
(la navigation POLYRA dans RES-01). Les briefs annoncent trois images par vidéo :
c'est un objectif, pas un état. Lire `availability.json` avant chaque montage.
