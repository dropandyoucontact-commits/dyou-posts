# MONARQUE — la recette validée (16/10/2026)

Le client a **adoré MQ-M05 et MQ-M04 v2** : c'est le niveau de référence pour toutes ses vidéos (pub, contenu éducatif,
réseaux). Nouvelle vidéo = copier `motion/MQ-M05/` (scenes.py, médias), changer le script et les scènes, garder tout le reste.

## Ce qui ne change pas
- **Fond blanc cassé** `fond_clair()` (sa préférence), noir encre, Archivo Black, accent beige trench ; rouge = problème,
  vert = validé, beige = ce qui gagne. Briques : `moteur/monarque.py`.
- **Voix Tomy**, débit validé (4,2 mots/s, pauses 0,18 s, défaut de `voix.py`), vouvoiement. Son : `mixer.py --lufs -13`
  (−13 LUFS, crête ≤ −1 dB). Avant le mix : écrire `sfx.json` depuis `scenes.SFX` (voir plus bas).
- **Script du client lu mot pour mot** quand il en fournit un ; aucun chiffre inventé.
- **Plans dézoomés** : cartes verticales qui montrent le plan entier, jamais une bande large qui coupe un rush.
- **Image 0 pleine** : titre + éléments déjà présents à t = 0 (MQ-M05 : « Vous » au centre et ses 4 cases), puis chaque
  élément s'allume au mot qui le nomme (`TW(i)`).
- **Globe EN POINTS**, pays allumé (Chine en noir + halo beige, France en noir, avion sur l'arc) : `globe_points()`.
  Jamais le globe blanc sculpté.
- **Graphique « vos ventes »** : barres + vignettes, **un modèle différent sous chaque barre** (ses photos produits).
- Disque noir + logo blanc sur « Monarque », puis logo noir en tête ; sous-titres `SousTitresEncre` masqués pendant
  les disques noirs et le carton final ; fin = logo, sa signature, bouton monarqueprod.com cliqué.
- Grammaire de scène : titres lettre par lettre, cases à médias, pastilles, coches/croix, tampons, courbe (prix d'une
  erreur), pistes d'étapes, une idée par phrase, suspense → réponse (graphique à plat, puis qui monte).

## Médias
`motion/banque/monarque/` (hors git, dépôt public) : `produits/` (fond clair), `fiches/` (fiches techniques MONARQUE ;
pas le « Nike techpack »), `references/`. Rushes atelier, nuancier, studio, SHOP, trenchs : `motion/MQ-M05/media/`.

## Chaîne
```
cd motion/MQ-Mxx && python3 ../moteur/outils/voix.py
/usr/bin/python3 ../moteur/rendu.py apercu …     # planches, corriger
/usr/bin/python3 ../moteur/rendu.py video
/usr/bin/python3 -c "import sys,json;sys.path.insert(0,'.');import scenes;json.dump(sorted(scenes.SFX),open('sfx.json','w'))"
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 renders/image.mp4
/usr/bin/python3 ../moteur/outils/verifier.py video/MQ-Mxx.mp4 0 …   # toujours vérifier le MP4 final
```
Piège : une fonction de dessin qui sort tôt (`alpha ≤ 0`) doit quand même renvoyer ce que l'appelant déballe.
