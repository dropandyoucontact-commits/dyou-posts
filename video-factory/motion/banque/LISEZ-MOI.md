# Banque de médias commune

Tout ce que Youssef envoie pour les vidéos motion se range ici, une fois pour toutes les
vidéos. Le moteur cherche un média dans le projet (`media/`), puis `moteur/media/`, puis ici.

> **Où sont les médias.** Sur le Mac de Youssef, dans ce dossier, et sauvegardés sur
> GitHub dans le dépôt **privé** `dyou-assets`, sous `motion-banque/` (jamais dans
> `dyou-posts`, qui est public : il sert les visuels à l'API Instagram). `.gitignore` ici
> ne suit que cette page et les logos. Pour sauvegarder après un ajout :
> `git clone git@github.com:dropandyoucontact-commits/dyou-assets.git`, copier ce dossier
> dans `motion-banque/`, commit, push.

## La règle fond blanc / situation (Youssef, 05/10/2026)

| La photo montre… | On en fait quoi |
|---|---|
| Un produit **sur fond blanc** (studio) | **Détouré** (PNG) et posé directement sur le fond blanc de la vidéo, avec ombre au sol : `produit()` du kit. |
| Un produit **en situation** : porté, posé sur un tapis, en étagère, sur un plateau, planche de plusieurs modèles, personnage | **Jamais détouré** : montré **dans un téléphone** — `image_cover()` pour une photo (zoom et travelling lents), `video()` pour une vidéo (accélérée ×2 à ×2,5 pour tenir dans la phrase). |

## Dossiers

| Dossier | Contenu |
|---|---|
| `produits/<catégorie>/` | Produits détourés : `textile`, `chaussures`, `electronique`, `mobilite`, `accessoires` |
| `photos/<catégorie>/` | Photos en situation (téléphone) |
| `videos/<catégorie>/` | Vidéos de fournisseurs (téléphone, accélérées) |
| `lieux/` | Lieux réels : devanture de Kimbo (Guangzhou), tour SEG Electronics (Shenzhen)… |
| `logos/` | Logos d'applications (Simple Icons, CC0) : `wechat`, `alipay`, `snapchat`, `whatsapp` |
| `originaux/` | Photos d'origine avant détourage |

## Inventaire au 5 octobre 2026

Produits détourés (`produits/textile/`) : veste doudoune bleu ciel · veste à capuche grise
réversible · gilet zippé en maille crème · gilet zippé en maille marine · veste de pluie
marine · veste racing noire · veste racing bleue · veste racing blanche. Autres :
`electronique/casque-audio`, `mobilite/moto-electrique`.

Photos en situation (`photos/`) : baskets portées marine / grises / violettes ·
étagère de 6 baskets de running · planche de 12 baskets · casque de moto sur plateau.

Vidéos : `videos/chaussures/` 2 vidéos de baskets en main sur le stock (10,2 s et 9,6 s) ·
`videos/guangzhou/guangzhou-cartons-baskets-gros.mp4` (2,1 s : des cartons pleins de baskets, filtre
« GUANGZHOU » à la fin — sert pour « j'étais à Guangzhou » **et** pour « en gros »).

Photos de fabrication (`photos/fabrication/`) : couture d'une semelle, assemblage d'une semelle
(en téléphone, sans jamais dire « usine » dans la voix).

## Ajouter un média

```sh
cd video-factory/motion
# photo produit sur fond blanc → PNG transparent
python3 moteur/outils/banque_detourer.py banque/originaux/NOM.jpg banque/produits/CATEGORIE/NOM.png
```

Le détourage retire le fond blanc relié aux bords, le halo clair du studio et les ombres
grises ajoutées par les outils des vendeurs. Un vêtement gris clair peut demander
`--halo 255`. Toujours vérifier le résultat sur un fond foncé. Les noms disent ce qu'on
voit, sans marque : les marques visibles sur les produits ne se citent ni à l'écran ni
dans la voix.
