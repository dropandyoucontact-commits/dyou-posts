# Point d'entrée pour Claude — vidéos DYOU et ChinaBook

## Qui décide du motion

Décision de Youssef, 5 octobre 2026 : **tout le motion design est décidé et réglé par
Claude, et ses règles vivent dans ce dépôt** (ce fichier, `reference/A-LIRE.md`,
`motion/LISEZ-MOI.md`). Les consignes de motion venues de ChatGPT ne s'appliquent plus :
briefs Higgsedit, champs `motion_direction` et `images` des `brief.json`, thèmes sombres,
`A-REGENERER.md`. Si une règle de motion doit changer, c'est Claude qui la change ici.

## Le standard : CB-M04 et CB-M05 (06/10/2026)

**Le niveau de référence est celui de `motion/CB-M04/` (« T'as tout faux ») et de `motion/CB-M05/`
(« Reste ici », v2)**, validés par Youssef le 6 octobre 2026 : « c'est parfait », « c'est très bien
ce que tu me fais ». Toute nouvelle vidéo part du `scenes.py` de CB-M05 et suit la recette de
`reference/A-LIRE.md` (section « La méthode validée », corrections comprises). CB-M01 (05/10) reste
la première vidéo validée, plus le modèle. Les anciennes méthodes (montages PIL de
`outils/ancien-montage/`, thèmes sombres, exemple RES-01) ne sont pas des modèles.

**Volume : `mixer.py --lufs -9 renders/image.mp4`** (depuis DY-M02, 09/10/2026) : la voix est montée seule
(≈ −10 LUFS), les bruitages posés à côté d'elle puis effacés sous chaque mot. Retour de Youssef sur DY-M02 :
voix bien forte = bon ; bruitages « encore un peu trop bas » → réglage par défaut relevé de 2 dB (`ecart = -1`).
Jamais d'écart de 15 LU (« on n'entend plus rien »), jamais un seul gain de sortie qui remonte les bruitages
au-dessus de la voix. Ancien réglage −11 LUFS : trop faible, Youssef remontait le son dans CapCut.
Ce qu'il faut savoir est dans `reference/A-LIRE.md` ; comment faire une nouvelle vidéo est dans
`motion/LISEZ-MOI.md`.

Le moteur est `motion/moteur/` (Python + Skia : texte crénagé, perspective 3D, flou de
mouvement, confettis, encodage H.264). Chaque vidéo est un dossier `motion/<ID>/` qui ne
contient que son script, sa voix, son minutage, ses médias et son `scenes.py`.

## Chaîne de production

1. **Contenu** : quand Youssef envoie des vidéos ou carrousels TikTok de référence, les
   décortiquer (texte à l'écran, voix, structure), puis écrire un script **à nous** —
   jamais une copie. Suivre `LIGNE-EDITORIALE.md` (sujets, appel à l'action qui ne vend
   pas ChinaBook à chaque vidéo).
2. **Voix** : `motion/<ID>/script.txt`, puis `python3 ../moteur/outils/voix.py` depuis ce
   dossier. ElevenLabs (voix Tomy, `eleven_v4`, clé dans `~/.config/dyou/elevenlabs.json`,
   offre Starter : 30 000 crédits par mois, ~1 crédit par caractère) renvoie le temps de
   chaque caractère : `timing.json` sort directement, sans transcription. L'outil accélère
   ensuite la prise à **3,5 mots par seconde** (débit TikTok rapide). Une prise n'est
   jamais regénérée sans `--forcer` : c'est du crédit. Vérifier avec `--etat` avant.
3. **Scènes** : écrire `scenes.py` en partant de celui de CB-M01. Chaque élément cite le
   mot qu'il illustre (`TW(i)`), jamais une seconde écrite en dur.
4. **Aperçus**, puis **rendu** : `python3 ../moteur/rendu.py apercu …` et
   `python3 ../moteur/rendu.py video` (≈ 5 min pour 60 s sur le Mac de Youssef, 2 cœurs /
   4 Go — le VPS de Tokyo, 1 vCPU / 2 Go déjà chargé par les bots, serait 3 fois plus lent).
5. **Son** : `outils/sons.py` (une fois) puis `outils/mixer.py renders/image.mp4` — voix compressée,
   mix final à −11 LUFS / −1 dB crête (assez fort pour le téléphone, plus besoin de CapCut), bruitages atténués sous la voix, pas de musique.
6. **Vérifier le MP4 final** : `outils/verifier.py video/<ID>.mp4 t1 t2 …` extrait des
   images du fichier exporté lui-même. Ne jamais livrer sur la foi des aperçus.

## Règles de contenu

- **Organique ou pub** : voir `LIGNE-EDITORIALE.md`, « Deux familles de vidéos » — appels à enregistrer, partager et commenter en organique seulement.
- Ne pas inventer de prix, de marge, de résultat chiffré, de témoignage, de capture WeChat
  ni de preuve commerciale. Les barres et tickets du motion n'ont pas de nombres.
- Prix à l'écran : le prix cher est celui de dropandyou (`full11_source.json`) ; le prix
  fournisseur seulement s'il figure dans `donnees/prix-chinabook.csv`, rempli à la main —
  sinon la case « RÉSERVÉ ». Pas de produits sous 60 € (l'écart ne se voit pas).
- Un échange avec un fournisseur montré à l'écran porte la mention « Échange illustratif ».
- Les marques visibles sur les produits ne sont pas citées.
- Les faits qui changent (visa, applications, règles de paiement, douane) se vérifient le
  jour du script, à la source officielle.

## Produits à l'image

Dès qu'un produit est montré, il vient de la banque DROP&YOU ou des photos fournies par
Youssef, détouré (`outils/detourer.py` pour la banque, `motion/moteur/outils/detourer.py`
pour une photo isolée sur fond blanc). Jamais une photo de produit générique.

## Bibliothèque des 50 scripts

`manifest.json` indexe 50 dossiers `videos/ID/` (`script.txt`, `brief.json`, images) écrits
avant le standard CB-M01. Leurs scripts restent utilisables : pour en produire un, créer
`motion/<ID>/` et y copier `videos/<ID>/script.txt`. `availability.json` dit quelles images
existent vraiment. Familles ChinaBook : `prix`, `voyage`, `intermediaire`, `rentable`,
`reseau` — varier les familles dans le calendrier.

## Répartition du travail

**Le motion, les voix, les bruitages et l'encodage se font ici, par Claude**, au standard
CB-M01. ChatGPT ne fixe plus de règle de motion ; une idée de sujet ou de script venue de
lui se traite comme un contenu de référence : Claude la réécrit selon `LIGNE-EDITORIALE.md`. Ressources GitHub
vérifiées et pièges connus de Higgsedit : `motion-ressources/README.md`.

## Trois façons de monter (Youssef, 10/10/2026)

1. **Motion pur** : fond blanc ou noir, mockups, téléphones et objets en 3D, voix. Modèle : CB-M04 / CB-M05, `scenes.py` + `moteur/rendu.py`.
2. **Rushes à écran vert** : Youssef génère une vidéo où un élément est vert chroma uni (écran de téléphone, panneau publicitaire,
   écran de télé, vitrine…) ; on détoure le vert, on y incruste du contenu et on fait sortir des panneaux en verre fumé.
   Modèle : DY-M02 (`suivi_vert.py`). Consignes de génération : vert uni mat, 4 coins visibles, mouvement lent, haute résolution.
3. **Habillage d'une vidéo finie** : Youssef envoie une vidéo déjà montée (musique, texte incrusté) ; on n'y touche pas et on pose
   par-dessus, en verre fumé, marque, cartes de chapitre, repères accrochés aux objets (suivi par flux optique) et carton de fin.
   Pas de voix. Modèle : DY-M03 (`montage.py`, `suivi.py`, rendu autonome au format de la source) — « c'est parfait ».

## Vidéos DYOU Agency (vendre du motion) — 10/10/2026

Style à part : `motion/moteur/agence.py` (fond sombre vivant, verre dépoli, violet du logo #7439FC, particules).
**Sous-titres fins** (`SousTitresFins`) : la phrase en cours en blanc, chaque mot qui se pose flou → net à son
temps, **aucun surlignage ni mot coloré** — Youssef n'aime plus les sous-titres karaoké vert/violet pour l'agence.
Les cartes en verre, écrans de chat, mockups 3D : c'est le niveau « moderne » attendu. Pas de logo + sous-titre
qui disent la même chose (sous-titres masqués pendant le disque logo). Modèles : `motion/DA-M01`, `motion/DA-M02`.

### DA-M04 « Stop, coach » — référence de montage hybride (10/10/2026, « la vidéo est parfaite, ça c'est du montage »)

Rushes humoristiques fournis par Youssef (personnages muets, seule la voix off parle) + motion du style agence :
- **un seul rush en plein écran, le hook** (r1 : « Stop ! » et la main qui frappe l'écran) — on garde son vrai son,
  la voix off démarre juste après (voix décalée de 0,95 s, timing.json recalé), vitre fendue + secousse à l'impact ;
- **les autres rushes vont dans des mockups** : téléphone 3D (`video()` dans `telephone_sombre`), et le rush à écran
  vert dans un grand cadre de verre avec le site incrusté sous les doigts (`DA-M04/suivi_vert.py`, fonctions de DY-M02) ;
- les blocs du site sortent du téléphone en verre (découpes d'une capture Chrome headless de la page), surlignés au mot ;
- le texte change à chaque vidéo (les algorithmes repèrent les doublons) ; CTA organique « Commente COACH » tapé à l'écran.

**Voix** : toujours Tomy (`Lt0unAbeM6JystrA2RTv`). eleven_v4 a sorti une prise à l'accent québécois sur DA-M04 :
`voix.py` envoie désormais `language_code: "fr"`. Si une prise sonne autrement, la refaire (`--forcer`) : les animations
suivent les mots (`TW`), rien d'autre à reprendre.
