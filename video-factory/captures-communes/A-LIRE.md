# Captures réelles — une par métier

Le mockup téléphone montre **le site dont parle la voix off**, jamais un autre.
C'est le point qui a fait rater la première version de RES-01 : elle parlait de
résine et le téléphone affichait l'accueil de l'agence puis un site de coaching.

| Fichier | Site | Pour les vidéos |
|---|---|---|
| `site-POLYRA-resine.mp4` | POLYRA | **RES-01 → RES-10** (résine au sol) |
| `site-ATHLA-coach.mp4` | ATHLA | **COA-01 → COA-10** (coach sportif) |
| `site-VELOR-location.mp4` | VELOR | **LOC-01 → LOC-10** (location de voiture) |
| `site-DYOU-accueil.mp4` | dyou-agency.com | quand la voix parle de **l'agence elle-même**, en général vers la fin |

Toutes en 1280 de haut, 30 i/s, H.264, sans son (sources : enregistrements
d'écran du 03/10/2026 en 60 i/s HEVC, ré-encodés pour alléger le dépôt).

## Deux règles apprises le 03/10/2026

**Ne jamais recadrer la capture.** Les quatre sources n'ont pas le même rapport
(0,515 à 0,598 : les enregistrements iPhone ne sont pas cadrés pareil). Un crop à
largeur fixe mange le texte du site sur les côtés — c'est arrivé sur RES-01, où
« On ne pose pas un motif » s'affichait « n ne pose as un motif ». Le cadre du
téléphone doit **épouser la source** : on extrait en `scale=-2:<hauteur>` sans
`crop`, et le montage lit la taille réelle des images pour dessiner le cadre.

**Couper la queue de l'enregistrement.** Un enregistrement iPhone finit souvent
sur le Centre de contrôle. `outils/nettoyer_captures.py` le repère — l'arrière-plan
devient flou, ce qui le distingue d'un simple changement de page — et écrit la
durée exploitable dans `utiles.json`. Le montage lit ce fichier, jamais la durée
brute. Relevé actuel : seul POLYRA est concerné, 0,80 s à retirer.

**Pour tenir dans un plan plus court, accélérer plutôt que couper :**
`setpts=PTS/<durée utile ÷ durée du plan>` — le parcours reste entier.
Exemple RES-01, plan de 7,33 s sur 11,50 s utiles : `setpts=PTS/1.5682`.

Les 20 vidéos ChinaBook n'ont pas de site à montrer : pas de mockup pour elles,
ou alors une capture WeChat autorisée, jamais une fausse image générée.
