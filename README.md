# DYOU Posts

Exports publics des contenus DYOU Agency destinés aux API Meta.

## Arborescence

Les carrousels Instagram sont classés par date et numéro de série sous `instagram/`.
Chaque dossier contient les 7 visuels JPG, la légende, les consignes de publication et un manifeste avec les URL publiques.

## Hashtags : la règle, par réseau

La légende de `caption.txt` sert les deux réseaux, mais ils ne reçoivent pas la
même chose. `carrousel.py` applique la coupe au moment de publier :

- **Facebook : aucun hashtag.** Ils n'y portent pas la découverte et au-delà de
  deux ils se lisent comme du spam. Tous les hashtags sont retirés, où qu'ils
  soient placés dans le texte.
- **Instagram : cinq au maximum**, plafond imposé par la plateforme depuis le
  18/12/2025. Trois hashtags vraiment descriptifs valent mieux que cinq
  génériques : ils ne servent plus à la distribution, seulement à la recherche.

**Pour le producteur de la légende :** viser trois hashtags, et les poser sur la
**dernière ligne**. Jusqu'au 05/10/2026 la coupe ne regardait que cette dernière
ligne ; le carrousel J16 portait ses cinq hashtags au milieu du texte, suivis
d'une phrase de clôture, et les cinq sont partis sur la Page Facebook sans
qu'aucune erreur ne le signale. La coupe est désormais indifférente à la
position, mais la dernière ligne reste la convention lisible.

## Contenu généré par IA : le déclarer

Un visuel ou une vidéo produit par IA doit être publié **avec** la mention
« contenu IA ». Le label de Meta n'est pas une pénalité de classement. C'est
l'inverse qui coûte : un contenu IA **non déclaré** que les classifieurs
repèrent ensuite voit sa distribution réduite. Retirer les métadonnées de
provenance d'un fichier ne protège donc de rien, et fait basculer le post du
bon côté vers le mauvais.
