# Captures réelles communes à toutes les vidéos

`DYOU-site-navigation.mp4` — navigation réelle sur **dyou-agency.com**, 13,66 s,
30 i/s, H.264 (source : enregistrement d'écran du 03/10/2026, ré-encodé depuis
888×1714 HEVC 60 i/s pour alléger le dépôt).

**C'est cette capture qui va dans le mockup téléphone dès qu'une voix off parle
de D-YOU Agency**, et non la navigation POLYRA — celle-ci reste réservée aux
vidéos qui parlent du site d'un client résine (RES-01 et suivantes le citent
nommément dans leur `real_asset_requirement`).

Pour la poser dans un plan plus court que 13,66 s : accélérer avec
`setpts=PTS/<facteur>` plutôt que couper, afin de montrer tout le parcours.
