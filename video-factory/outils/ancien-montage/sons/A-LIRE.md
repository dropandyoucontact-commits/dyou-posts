# Bruitages

Cinq sons **synthétisés** par `outils/faire_sons.py` — rien n'est téléchargé,
donc rien à créditer ni à vérifier côté licence. Relancer le script les refait
à l'identique (graine fixe).

| Son | Durée | Quand |
|---|---|---|
| `tick.wav` | 45 ms | chaque ligne de titre qui apparaît |
| `pop.wav` | 110 ms | une carte, un libellé, un bouton |
| `whoosh.wav` | 380 ms | changement de plan |
| `swipe.wav` | 220 ms | défilement dans le mockup |
| `impact.wav` | 420 ms | le carton final |

`outils/mixer_sons.py` les pose sur la voix aux timecodes des plans, normalise la
voix à −16 LUFS et passe le tout dans un limiteur à 0,95. Gains typiques : −9 dB
pour l'impact final, −11 à −13 pour les pop et les tick, −15 pour le whoosh,
−20 pour les swipe. Assez pour s'entendre, assez bas pour ne pas manger la voix.

**Pas de musique de fond** : le contrat de montage l'exclut, et sous une voix off
de 20 secondes une nappe ne fait que brouiller le message.
