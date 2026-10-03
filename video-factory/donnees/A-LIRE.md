# Prix à remplir

`prix-chinabook.csv` sert aux vidéos qui affichent une comparaison de prix.

- `prix_site_eur` est **déjà rempli** : c'est le prix réellement affiché sur dropandyou.
  Il ne s'invente pas, il se relit dans `full11_source.json`.
- `prix_chinabook_eur` est **à remplir par Youssef**. Tant qu'une ligne est vide,
  le montage n'écrit aucun chiffre fournisseur à l'écran : il affiche la case
  « RÉSERVÉ » et renvoie au commentaire. C'est la règle, pas un provisoire.
- Le Surron est la seule ligne déjà remplie : les fourchettes viennent de Youssef
  (3 000 – 7 000 € en France, 1 500 – 3 600 € en Chine, 04/10/2026).

Ne jamais compléter une ligne par estimation ou par règle de trois.
