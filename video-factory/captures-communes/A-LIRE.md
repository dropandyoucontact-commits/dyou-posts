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

**Pour tenir dans un plan plus court, accélérer plutôt que couper :**
`setpts=PTS/<durée source ÷ durée du plan>` — le parcours reste entier.
Exemple RES-01, plan de 7,33 s sur 12,30 s de source : `setpts=PTS/1.677`.

Les 20 vidéos ChinaBook n'ont pas de site à montrer : pas de mockup pour elles,
ou alors une capture WeChat autorisée, jamais une fausse image générée.
