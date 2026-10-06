# Point d'entrée pour Claude — vidéos DYOU et ChinaBook

## Qui décide du motion

Décision de Youssef, 5 octobre 2026 : **tout le motion design est décidé et réglé par
Claude, et ses règles vivent dans ce dépôt** (ce fichier, `reference/A-LIRE.md`,
`motion/LISEZ-MOI.md`). Les consignes de motion venues de ChatGPT ne s'appliquent plus :
briefs Higgsedit, champs `motion_direction` et `images` des `brief.json`, thèmes sombres,
`A-REGENERER.md`. Si une règle de motion doit changer, c'est Claude qui la change ici.

## Le standard : CB-M01

**Toute vidéo motion se fait au niveau de `motion/CB-M01/video/CB-M01.mp4`**, validé par
Youssef le 5 octobre 2026 (« c'est le niveau que j'accepte »). Les anciennes méthodes
(montages PIL de `outils/ancien-montage/`, thèmes sombres, exemple RES-01) ne sont plus
des modèles. **Depuis le 06/10/2026, la méthode de CB-M04 et CB-M05 est validée (« c'est parfait ») :
partir de leur `scenes.py` pour toute nouvelle vidéo ChinaBook courte.** Ce qu'il faut savoir est dans `reference/A-LIRE.md` ; comment faire une
nouvelle vidéo est dans `motion/LISEZ-MOI.md`.

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
