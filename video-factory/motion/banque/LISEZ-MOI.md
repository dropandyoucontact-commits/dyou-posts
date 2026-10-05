# Banque de médias commune

Tout ce que Youssef envoie pour les vidéos motion se range ici, une fois pour toutes
les vidéos. Le moteur cherche un média dans le projet (`media/`), puis dans
`moteur/media/`, puis ici : `image(c, "produits/textile/gilet-maille-creme", …)`.

| Dossier | Contenu | Format |
|---|---|---|
| `produits/<catégorie>/` | Produits détourés : `textile`, `chaussures`, `electronique`, `mobilite`, `accessoires` | PNG transparent, 1 400 px max |
| `videos/<catégorie>/` | Vidéos de fournisseurs (montrées dans un téléphone, accélérées ×2 à ×2,5) | MP4 d'origine |
| `lieux/` | Lieux réels : devanture de Kimbo (Guangzhou), tour SEG Electronics (Shenzhen)… | JPG / PNG |
| `logos/` | Logos d'applications (Simple Icons, CC0) : `wechat`, `alipay` | SVG |
| `originaux/` | Photos d'origine avant détourage | JPG |

## Inventaire au 5 octobre 2026

| Fichier | Ce que c'est |
|---|---|
| `produits/textile/veste-doudoune-bleue.png` | Veste doudoune bleu ciel, manches maille |
| `produits/textile/veste-capuche-grise.png` | Veste à capuche grise réversible, doublure à motif |
| `produits/textile/gilet-maille-creme.png` | Gilet zippé en maille crème |
| `produits/textile/gilet-maille-marine.png` | Gilet zippé en maille marine |
| `produits/electronique/casque-audio.png` | Casque audio, plusieurs coloris |
| `produits/mobilite/moto-electrique.png` | Moto électrique tout-terrain |
| `videos/chaussures/baskets-stock-1.mp4` | Baskets présentées à la main sur le stock (10,2 s) |
| `videos/chaussures/baskets-stock-2.mp4` | Idem, autre modèle (9,6 s) |

## Ajouter un média

```sh
cd video-factory/motion
# photo produit sur fond blanc → PNG transparent
python3 moteur/outils/banque_detourer.py banque/originaux/NOM.jpg banque/produits/CATEGORIE/NOM.png
```

Le détourage retire le fond blanc relié aux bords, le halo clair du studio et les
ombres grises ajoutées par les outils des vendeurs (gris parfaitement neutres). Un
vêtement gris clair peut demander `--halo 255` pour garder ses bords. Toujours
vérifier le résultat sur un fond foncé avant de l'utiliser.

Les noms disent ce qu'on voit, sans marque. Les marques visibles sur les produits ne
se citent ni à l'écran ni dans la voix.
