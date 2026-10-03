# Images retirées le 03/10/2026 — à regénérer

Sept premières images ChinaBook ont été supprimées : **CB-01, CB-02, CB-03,
CB-05, CB-07, CB-09, CB-10** (`images/01.webp` et son `01.json`).

**Pourquoi.** Elles montraient toutes le même homme en cagoule noire et lunettes
rouges emballant des colis dans un entrepôt. Aucun prompt ne le demandait — celui
de CB-01 dit « Revendeur français préparant des colis dans son petit local ».
C'est une dérive du générateur sur un lot entier.

Pour une marque qui vend l'accès à des fournisseurs vérifiés, cette image raconte
l'inverse du message, et c'est le type de visuel que la modération publicitaire
Meta refuse.

`availability.json` a été mis à jour : ces sept entrées déclarent maintenant une
seule image disponible.

**À regénérer** : la première image de ces sept scripts, en respectant le prompt
du `brief.json`, sans personnage masqué ni cagoulé.

**Au passage, deux demandes pour les prochaines générations :**
- sortir en **1080 × 1920**, pas en 941 × 1672 — l'agrandissement atteint 30 %
  quand un plan a un zoom, et ça se voit ;
- **regarder les images produites avant de les pousser** : le prompt ne garantit
  pas le résultat, c'est ce lot qui le prouve.
