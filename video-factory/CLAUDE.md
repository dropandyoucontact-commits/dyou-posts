# Point d'entrée pour Claude — vidéos DYOU et ChinaBook

## Conformité DROP&YOU et ChinaBook — prioritaire sur tout le reste (17/10/2026)

Deux pubs TikTok refusées le 17/10 sur DELICIAE : CB-M08 (« Misleading Opportunity » : « 50 paires de Saucony ×50 », achat de
50 unités pour revendre) et la vidéo IA à 21,6 K (contrefaçon de marques + audio 0:21-0:29 qui renvoie vers WhatsApp).
Les mêmes fautes bridaient la portée organique. Valable pour **toutes** les vidéos CB- et DY-, organique comme pub :

1. **Aucune marque nommée** : ni à l'oral, ni à l'écran, ni en hashtag, ni en description, ni dans le nom de fichier.
   Les visuels suffisent.
2. **Aucun renvoi hors plateforme** : plus de WhatsApp ni de Snap en fin de vidéo (ni Telegram, ni Instagram) — ni numéro,
   ni logo, ni dit, ni suggéré. Le message privé de la plateforme reste permis. `cta_whatsapp` (kit.py) et la scène
   « écris-nous : Snap / WhatsApp » de `dy3d.py` ne s'utilisent plus.
3. **Aucune promesse de gain ni ticket d'entrée** : pas de quantité minimum en condition, pas de prix d'accès, pas de
   promesse de revente ou de bénéfice.
4. **Jamais « contrefaçon »**, ni copie, réplique, faux, dupe, AAA. Discours : produits de très haute qualité, plusieurs
   qualités possibles selon les produits (grille standard / 1:1 / originale : sacs seulement).

**CTA** — organique : « écris-moi en message privé », « commente », « enregistre la vidéo », rien d'autre.
Pub : pas d'appel à commenter ; « contacte-moi via le lien autour de cette vidéo » (le bouton de l'annonce porte l'action).

La modération lit le texte à l'écran (OCR) et transcrit l'audio, horodatage à l'appui : une seule image fautive
(un logo dans un mockup) fait tomber la vidéo. Permis : produits, entrepôts, lieux, sourcing, fournisseurs validés,
délais, douane, transitaire, différences de qualité en restant général.

**Avant chaque rendu** : `python3 ../moteur/outils/conformite.py` depuis le dossier de la vidéo (`rendu.py video` le lance
seul et s'arrête pour un projet CB-/DY- fautif). Il contrôle script.txt et scenes.py ; les mockups et images se vérifient
à l'œil sur les aperçus. Les pubs DYOU Agency (DA-) ne sont pas visées.

**Marque et produits (17/10/2026)** : le logo DROP&YOU se met **en haut de l'écran du téléphone** (en-tête d'appli), en plus du
filigrane. Les cartes produits en verre clair (`banque/glace/carte_*.png`) servent quand un produit doit être présenté, pas
partout ; elles portent des logos de marques lisibles → à signaler avant une vidéo TikTok. Les consignes de ChatGPT ne
s'appliquent que si elles montent le niveau (référence : DA-M14/M16-EN v2, DY-M12).

**Vrais produits et zone sûre (17/10/2026, retour sur DY-M12).** Jamais un produit dessiné ou une icône à la place d'un
produit : les vraies paires détourées et les vraies vidéos de la banque et des projets (« les gens veulent voir ce qu'ils
ont envie d'acheter »). Hook fort (vrais produits dès l'image 0) et une intention de commentaire par vidéo. Contrôler
chaque vidéo de stock image par image : des cartons portent des marques. **Zone sûre unique TikTok + Snap** : sur un
téléphone 19,5:9 l'appli rogne ~96 px de chaque côté et la colonne de boutons couvre x > 860 de y 816 à 1555 → titres
≤ 760-840 px, contenu sous y 816 entre x 130 et 860, sous-titres de `studio.sous_titres` (y 1410, x 180-820). Vérifier
avec `motion/moteur/outils/zone_tiktok.py apercus/t*.png -o planche.jpg`.

**Jamais de ralenti (18/10/2026).** Une vidéo ou un rush ralenti « fait comme si la vidéo laguait » et casse le motion.
Vitesse ×1, ou accélérée quand le geste dure plus longtemps que la phrase (geste de 6 s, voix de 2-3 s → ×2). Si le plan est
trop court pour la phrase : enchaîner un deuxième plan, jamais l'étirer. `moteur.video()` refuse tout `vitesse < 1`.

**Produits et signature (18/10/2026, retour sur DY-M13).** Youssef choisit les baskets et articles qui jaillissent (mes choix
« pourris » : paires à virgule, montantes connues) → lui demander la liste, sinon `PAIRES` isolée en tête de scenes.py.
Ne pas centrer une vidéo DROP&YOU sur les baskets : « un article — une paire, une montre, une sape », catégories mélangées.
Fin : `moteur/signature.py` (produits aspirés → explosion → DROP&YOU recomposé en 3D), plus jamais le logo dans un cadre.
**DY-M15 = référence DROP&YOU validée (18/10/2026)** : police, disposition, rythme, signature → partir de là.
Toute correction validée par Youssef devient la base des vidéos suivantes (moteur ou règle ici), sans qu'il la redemande.
Pubs DYOU Agency : garder les dernières, mais leur fin passe à une signature du même genre, aux couleurs de l'agence.

## Hook toujours rapide et fort (19/10/2026) — toutes les vidéos voix off

Youssef : « dans le hook, tout le temps faut parler rapide… les premiers mots qui vont sortir, faut jamais que ce soit en lent ;
au début il faut que ça soit fort et rapide, toujours ». L'intonation peut varier ensuite dans la phrase, pas l'attaque.
`voix.py` lance `outils/hook_rapide.py` après `resserrer.py` : sur la première phrase, silences internes ramenés à 0,05 s
(la virgule d'« Aujourd'hui, » ne fait plus de trou), débit relevé à 5,2 mots/s minimum, +1,5 dB. `--sans-hook` pour l'éviter.

**Piège vu sur MQ-M08 (27/10/2026) : `hook_rapide.py` mesure le débit HORS SILENCES.** Sur une attaque
courte — « Regardez vos cartons. », 3 mots — il trouve 5,40 mots/s, se croit déjà au-dessus de la cible
et n'accélère rien, alors que le temps réel donne 4,63 mots/s et que l'attaque sonne molle. Ce qui traîne,
ce sont les blancs entre les mots, pas la diction de Tomy ; et la règle ne serre que la PREMIÈRE PHRASE,
qui peut ne faire que trois mots.

Quand une attaque sonne lente alors que la sortie de `hook_rapide` annonce 5,2 mots/s, refaire depuis la
prise brute (gratuit, aucune regénération ElevenLabs) :

```
python3 ../moteur/outils/voix.py --debit 4.2 --sans-hook
python3 ../moteur/outils/hook_rapide.py --mots 9 --debit 6.5
```

`--mots 9` couvre les deux premières phrases, c'est-à-dire le hook entier ; `--debit 6.5` force
l'accélération jusqu'au plafond ×1,25. Sur MQ-M08 : attaque 4,63 → 5,15 mots/s, hook 5,01 → 6,16 mots/s,
0,48 s gagnées. **Ne jamais relancer `hook_rapide.py` sur une voix.mp3 qui l'a déjà subi** : il s'applique
deux fois. Toujours repartir de `media/voix-brut.mp3`.

Après toute reprise de la voix, le minutage change : **régénérer `sfx.json` avant `mixer.py`**, sinon les
bruitages restent calés sur l'ancien timing (121 sons décalés de 0,5 s sur MQ-M08) :

```
python3 -c "import json, scenes; json.dump(sorted(scenes.SFX), open('sfx.json', 'w'))"
```

Mesurer plutôt que croire la sortie du script — le débit réel du hook, blancs compris :

```
python3 -c "import json; m=json.load(open('timing.json'))['mots']; print(round(9/m[8]['t1'],2),'mots/s')"
```

## Client GSX — Global SINO Export (19/10/2026)

Deuxième société du client MONARQUE (sourcing / accompagnement en Chine). Même grammaire claire que MONARQUE + les éléments
de DY-M15 passés en clair : `moteur/gsx.py` (verre givré blanc `verre_clair`, accent rouge du logo #E8072D, globe à points
Chine rouge, `titre2`, `signature_gsx` = plans aspirés → explosion → sigle-globe extrudé → « Global SINO Export » en 3D).
Premier film : `motion/GSX-M01/` (hook 1 du client, script mot pour mot, rushes d'usines du client en cartes 9:16 entières).

## Qui décide du motion

Décision de Youssef, 5 octobre 2026 : **tout le motion design est décidé et réglé par
Claude, et ses règles vivent dans ce dépôt** (ce fichier, `reference/A-LIRE.md`,
`motion/LISEZ-MOI.md`). Les consignes de motion venues de ChatGPT ne s'appliquent plus :
briefs Higgsedit, champs `motion_direction` et `images` des `brief.json`, thèmes sombres,
`A-REGENERER.md`. Si une règle de motion doit changer, c'est Claude qui la change ici.

## Client MONARQUE — niveau validé (16/10/2026)

« Le client a adoré » **MQ-M05** et **MQ-M04 v2** : c'est le standard de toutes ses vidéos (pub, éducatif, réseaux).
Recette complète : `reference/monarque.md`. Toute nouvelle vidéo Monarque part de `motion/MQ-M05/`.

## Voix off sur rushes — format validé (16/10/2026)

DY-M08 « c'était parfait » : rush muet de Youssef (POV, marchandise, personnage qui agit) + voix off Léo écrite plan par plan,
débit naturel calé sur l'image. Recette : `reference/voix-off.md`. Toute nouvelle vidéo de ce type part de `motion/DY-M08/`.

## Mise à jour du 15/10/2026 (prioritaire sur tout ce qui suit)

- **Débit de voix validé pour toutes les vidéos, toutes marques** (MQ-M02 / MQ-M03, « il est parfait, enregistre-le toujours ») :
  4,2 mots/s et pauses ramenées à 0,18 s. C'est le défaut de `voix.py`, qui lance `outils/resserrer.py` tout seul.

- **Volume de toutes les vidéos : −13 LUFS intégrés, crête vraie −1 dB.** TikTok rebaisse les vidéos trop fortes (nos −7/−8
  du 14/10) ; Youssef veut la norme (−14) avec un poil de marge au-dessus, et un fichier prêt à poster sans CapCut.
  Motion : `mixer.py --lufs -13` ; edits : `Edit.son()` de `moteur/edit.py` règle le gain par mesure.
- **Edits** (rush tourné, voix d'origine) : voix remplacée par **Léo** (`jsScnYkNNda9Q1NES5nn`) au changeur de voix ElevenLabs
  (même rythme) ; **Tomy est réservé au motion design**. Montage par `moteur/edit.py` : sous-titres petits (Inter Display
  ExtraBold 60 px, une ligne, centrés à y ≈ 1250, hors zones de l'interface TikTok), pastilles sur les mots, coups de zoom,
  logo DROP&YOU + « Enregistre la vidéo » à la fin. Modèles : `motion/DY-M06`, `motion/DY-M07`.

## Mise à jour du 14/10/2026

- **Son fort (CB-M10, 14/10)** : `mixer.py --lufs -8 --ecart -3 renders/image.mp4`, puis poser le son avec
  `aresample=192000,volume=5dB,alimiter=limit=0.86:attack=0.5:release=40:level=false,alimiter=limit=0.86:attack=0.1:release=20:level=false,aresample=48000`
  (AAC 256k) → −6,8 LUFS, crête vraie −1,0 dB. Sans le suréchantillonnage à 192 kHz, l'AAC fait dépasser 0 dB.
- **Plus de fonds blancs** pour l'organique DROP&YOU / ChinaBook : fond sombre violet nuit ou image réelle, accents saturés.
- **Après CB-M10 (14/10)** : fond coloré obligatoire (jamais blanc), Tomy ~4 mots/s (relever le plafond ×1,3 de `voix.py`), nouveaux sujets, fin ChinaBook OU DROP&YOU. Détail dans `LIGNE-EDITORIALE.md`.
- **ChinaBook en violet** (logo du site #6E48F0), plus en vert ; logo DROP&YOU plus présent ; ChinaBook en fin, « par DROP&YOU ».
- Règles d'animation tirées des meilleurs kits GitHub : `reference/grammaire-motion.md`.
- Organique / pub : voir `LIGNE-EDITORIALE.md`, mise à jour du 14/10.

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
   offre Creator : 131 000 crédits sur le compte au 27/10, ~1 crédit par caractère) renvoie le temps de
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

### DA-M05 « Résine » (10/10/2026)

Même montage que DA-M04 pour les artisans des sols en résine époxy, thème `theme_polyra()` (cuivre sur noir), site de démo
POLYRA (`dyou-netlify-ready/dist/realisations/polyra/`, capturé depuis une copie dans le scratchpad : ne jamais écrire dans
`dist/`, il est déployé). Six rushes : selfie en hook, ponçage et coulée dans le téléphone, ordinateur à écran vert avec un
vieux site fictif qu'il referme et jette, téléphone à écran vert avec POLYRA dont les blocs sortent, marche vers la caméra
sur « Tu veux le même ? ». `cadre_vert()` de `DA-M05/scenes.py` recadre le rush pour grossir un petit écran vert.

### DA-M06 / DA-M07 — style « studio clair » du site refondu (14/10/2026)

Pour vendre le motion design DYOU (offre du site : dès 290 € TTC, 30-45 s, 3 ou 4 accroches ; jamais de délai ni de
retouches illimitées promis) : `motion/moteur/studio.py`, aux couleurs du site clair (papier #FCFBFE, encre #211B33,
dégradé #6533BF → #7C43CC → #4665AD, Inter). Niveau visé : au-dessus des meilleurs studios concurrents — titres construits
lettre par lettre, interfaces vivantes, une idée par seconde, transitions variées. Le corps est commun (repères `M`),
seul le hook change. Sous-titres `SousTitresEncre` : encre, fins, sans surlignage, masqués pendant le prix et la fin.

### Pubs DYOU : verre clair + signature 3D (19/10/2026)

Demande de Youssef : garder tout de DA-M14-EN-v2 / DA-M16-EN-v2 (texte, voix, cartes en verre, vitrine, rendu, outils)
sauf les couleurs → fond clair du studio (DA-M06-EN, DA-M09-EN), et fin en signature 3D comme DY-M15 / GSX.
`moteur/verre_studio.py` : `vs.appliquer()` (cartes blanches → verre clair à halo violet, faux sites intacts), cartes de
Youssef redessinées en clair (`carte_rendu`, `carte_outils`, `carte_onde`, `carte_fichier`, `dock_outils`, `vitrine`),
`vs.signature(c, t, M["devis"] - vs.T_BOUM, MEDIAS, lignes, cta)` : explosion sur « Tap », sigle DYOU extrudé, DYOU AGENCY
en tranches 3D, « Tap the link. », bouton cliqué, adresse tapée. Mettre `studio3d.scene_cta` / `sites3d.scene_cta` à vide.
Réf. : DA-M17-EN (motion), DA-M18-EN (sites). Partir de là pour les prochaines pubs DYOU.


## Chaîne d'actu people / cinéma / séries / sport — identité posée le 27/10/2026

Nouvelle chaîne TikTok (projets **AC-M##**), distincte de tout le reste du portefeuille.
Concurrents étudiés : **@tactik77** (TacMedia, 713 K abonnés, sommets à 7,3 M),
**@red.hac** (RedHac, 290 K, « Films - Series - People »). Référence de motion : **@Phyzolof**.

**Ce qui a été refusé (AC-M01 v1)** : l'habillage cobalt + orange de ChinaBook.
Youssef : « t'as utilisé l'identité de DROP&YOU, fallait pas… pour les célébrités faut trouver
un format visuel et rester dedans ». Et : « pas de fonds sombres : quadrillés, en perspective,
qu'on voie de la profondeur, et que tu joues avec ça ».

**L'identité, à tenir d'une vidéo à l'autre — `moteur/people.py` :**

- **le décor est une pièce, pas un fond** : sol quadrillé qui fuit vers un point de fuite
  (`HORIZON` 700, `SOL` 1180), quadrillage de plafond, le tout qui avance lentement vers nous
  (`fond_grille(c, t, vitesse=…)`, accéléré sur les bascules) ;
- **la profondeur raconte** : ce qui arrive vient du point de fuite et grandit, ce qui disparaît
  y repart (`carte_photo(..., u, z0)`, `echelle_z`, `pose_sol` pour la lueur rouge qui ancre) ;
- **noir `#08080A`, blanc `#FFFFFF`, un seul rouge `#E8252D`.** Aucun dégradé de couleur, aucun verre,
  aucun violet : le reste du portefeuille est sombre et VIOLET, cette chaîne est noire et ROUGE ;
  le sol quadrillé est rouge, le plafond blanc, et le point de fuite porte un halo rouge qui bat ;
- **sur noir, une ombre ne dit rien** : ce qui ancre un objet au sol, c'est une LUEUR rouge
  (`pose_sol`), et les cartes portent un halo rouge au lieu d'une ombre portée (`_halo`) ;
- **pavé BLANC → texte noir, pavé ROUGE → texte blanc** (`bloc` choisit seul) ; les coupures de
  presse (`document`) restent du vrai papier blanc, c'est ce qui crève l'écran sur le noir ;
- **typo énorme en capitales** (`titre`), un seul mot surligné en rouge par écran (`surlignage`),
  mots barrés quand on corrige une idée reçue (`barre_rouge`) ;
- briques éditoriales : `rubrique` (DÉCODER / …), `bloc`, `document` (coupure de presse en 3D),
  `donut` + `compteur` + `legende` (la data animée de @Phyzolof), `bandes` (split-screen) ;
- **signature de fin maison** (`signature_people`) : le logo arrive du fond de la pièce, filet rouge,
  baseline, ondes rouges au sol. Celle de DROP&YOU (`signature.py`) ne s'utilise pas ici :
  elle raconte une autre marque, et le logo de la chaîne est blanc et rouge (`logo_people.py`).

**La chaîne est @recto_cerveau** (37,7 K abonnés, « Films 🎥 Séries 📺 Actu people 🍿 »).
Youssef produit, son associé publie. `people.NOM_CHAINE = "RECTO CERVEAU"` ;
`/usr/bin/python3 moteur/outils/logo_people.py "AUTRE NOM"` refabrique logo et signature.

**Habillage FIGÉ le 28/10/2026 — fond noir (AC-M01 v4).** La v3 sur papier crème a été validée sur
tout le reste (« c'est parfait, la dernière vidéo, la voix, tout ») : script, voix, montage et repères
temporels n'ont pas bougé d'un centième. Son associé, qui tient @recto_cerveau, a tranché l'habillage :
« fond noir, la grille qui bouge, accent en rouge et blanc, le texte et les médias plus grands,
juste en changeant la signature visuelle, comme ça on la fige ». C'est désormais LE format de la chaîne :
on part de `AC-M01/scenes.py` et on ne rediscute plus les couleurs. La version papier reste en
`moteur/people-papier.py.bak` et `AC-M01/scenes-v3-papier.py.bak` si jamais.

**« Plus grand » : où ça se gagne vraiment.** Les titres hauts sont déjà bornés par `LARG_T = 950`
(au-delà, les bords partent dans le rognage ~96 px de TikTok) : augmenter leur `taille` ne change
rien, `ajuste` les rabote. Le gain réel est ailleurs — plafond des pavés `bloc` porté de 470 à 630 px
(WOODY WOODPECKER 42 → 57, SUPER MARIO BROS 49 → 66, DIS-LE EN COMMENTAIRE 38 → 51), sous-titres
propres à la chaîne à 60 px (`people.sous_titres_people`, et non `studio.sous_titres` à 50),
médias élargis (extraits 880×495 → 900×506, portraits +15 %), et les punchlines remontées
AU-DESSUS de y 775 pour qu'elles prennent `LARG_T` au lieu de `LARG_BAS` (« T'A ÉLEVÉ, TOI ? »
86 → 126 px rien qu'en la passant de y 770 à y 700).
**Mesurer avant de rendre**, jamais à l'œil sur la planche :
`ajuste(txt, larg, taille, "noir", -0.022)` puis `largeur(...)` → vérifier x ∈ [96, 984] en haut,
et x ∈ [140, 858] sous y 816 (colonne de boutons).

**Livraison : canal Telegram « Tiktok » (28/10/2026).** Youssef produit, son associé publie.
Une vidéo finie et vérifiée part dans le canal privé où ils sont tous les deux (le bot média y est
administrateur), **toujours en FICHIER** :

    cd video-factory/motion/AC-M01
    /usr/bin/python3 ../moteur/outils/livrer.py video/AC-M01.mp4 --legende "…"

`sendDocument`, jamais `sendVideo` : Telegram ré-encode tout ce qui part en vidéo. En document
l'octet envoyé est l'octet reçu, et le fichier se range quand même dans la galerie du téléphone.
Le jeton reste sur le VPS ; `livrer.py` copie, envoie, efface, et compare ce qui est reçu à ce qui
est envoyé. **Au-dessus de 49 Mo** (plafond de 50 Mo de l'API des bots) il bascule seul sur un
**lien** : le master va dans `/srv/livraisons/<jeton>/` sur le VPS, servi par
`https://videos.108-61-187-118.sslip.io` sans index, et le bot poste l'adresse. Empreintes SHA-256
comparées des deux côtés. **Jamais de recompression automatique** : une vidéo livrée l'est en
qualité maximale, sans exception. L'hôte s'installe une fois avec
`moteur/outils/installer-livraisons.sh` — à faire lancer par Youssef, les écritures dans `/etc/`
du VPS sont refusées côté Claude Code. Détail : mémoire `canal-livraison-recto`.

**AC-M02 EST LA RÉFÉRENCE DE LA CHAÎNE** — « parfait la vidéo », Youssef, 28/10/2026.
Toute nouvelle AC- part de `motion/AC-M02/scenes.py`, pas d'AC-M01. Ce qui y est acquis :
hook visuel sans texte, deux cartes empilées pour poser un face-à-face, briques `podium`
(un classement dont la 1re marche est VIDE), `puce` (réactions de réseau), `camp`
(le débat en deux colonnes séparées d'un filet rouge), `ondes_sol`, et la structure
« on montre la preuve, puis on arme les deux camps, puis on fait trancher ».

**Trois règles de plus, posées le 28/10/2026 (AC-M02) — valables pour toute la chaîne :**

1. **Le hook est un VISUEL, pas du texte.** L'image 0 est un plan choc, plein cadre ; aucun titre
   avant le 4e mot. Sur AC-M02 : le visage de Kane qui fonce sur nous, puis il monte et celui de
   Henry arrive du fond en dessous — le face-à-face est à l'écran avant qu'un mot ne soit écrit.
   « Plutôt qu'avoir du texte, direct avoir un visuel choc. »
2. **L'attaque de la voix doit être impactante**, pas seulement rapide :
   `voix.py --debit 4.0 --sans-hook` puis `hook_rapide.py --mots 11 --debit 6.0`
   (`--mots 11` couvre la première phrase entière ; ici 5,68 mots/s sur l'attaque).
3. **Débit général légèrement relevé : 4,66 mots/s** (AC-M01 était à 4,33). `--debit 4.0` y mène ;
   `--debit 4.6` monte à 5,02, c'est trop. Le paramètre n'est pas le résultat : `resserrer.py`
   enlève encore ~10 s de blancs derrière, **mesurer timing.json** avant de valider.

**Deux pièges de production vus sur AC-M02 :**
- **`renders/cache-videos` n'est pas invalidé quand on recoupe un plan.** Un extrait remplacé
  continue de sortir en ancienne version dans les aperçus comme dans le rendu. `rm -rf
  renders/cache-videos` après toute retouche de `media/videos/`.
- **Un extrait de plateau alterne les visages.** Avant de caler `t0`, sortir une planche fine
  (`ffmpeg -ss X -t Y -vf "fps=1/1.5,scale=160:-1,tile=9x2"`) et choisir un segment où la bonne
  personne est à l'image tout du long — au besoin concaténer deux segments.

**Trois contraintes de format (27/10/2026)** :
- **1 minute 02 minimum** par vidéo — seuil de monétisation. Viser 63-70 s de voix (≈ 270 mots).
- **Phrases complètes, courtes et simples** : 8-9 mots. Quelqu'un qui ne connaît pas le sujet
  doit comprendre. Les titres à l'écran restent télégraphiques, pas la voix off.
- **De vraies vidéos de la personne**, récentes, sans texte incrusté. `people.carte_video()` les pose
  en cadre 16:9 large. YouTube ne sort plus que du 360p via
  `yt-dlp --extractor-args "youtube:player_client=android"` : d'où le cadre large, pas de portrait.
  Vérifier les vignettes avant de monter — une bande-démo contient des plans sans la personne.

**Voix : TOUF** (`2AU180IkVdtYRbAj8egD`) — VALIDÉE le 28/10/2026 au soir, prise C.
Touf est l'ami de Youssef : il a cloné sa propre voix et envoyé un fichier ElevenLabs de 76 s
(`…Voix_2_eleven_v4…`). On l'a recloné depuis cet audio. Ce qui a marché, et qui est LA technique
à réutiliser pour toute voix qu'il enverra (« je vais t'envoyer d'autres voix à cloner en utilisant
la même technique ») :

    clone-voix --nom "Touf" --propre fichier.mp3      # ni isolation, ni débruitage
    voix.py --voix 2AU180IkVdtYRbAj8egD --modele eleven_v4 --stabilite 0.65 --style 0.0 \
            --similarite 1.0 --sans-boost --debit 3.3 --sans-hook --sans-resserrer

- **Générer avec le MÊME modèle que la source** (le nom du fichier le dit : `eleven_v4`) : v4 divise
  l'écart par deux par rapport à multilingual_v2 (0,75 dB contre 1,51).
- **Jamais de `remove_background_noise` sur une source propre** : le débruiteur lisse le timbre
  quand il n'a rien à nettoyer. (Sur une vraie prise bruitée, la règle kyks — brut + débruitage — tient.)
- Tester sur le MÊME texte que l'original, mesurer F0 + 40 bandes mel (`~/recto-voix/outils/compare.py`),
  envoyer deux prises calées au niveau de l'original. Au-delà de 1 dB d'écart, demander plus d'audio.
- Débit naturel 3,19 mots/s = déjà le rythme du format lettre. Sur un format d'info, `--debit 4.0`.
L'ancien clone des vieilles vidéos (`x5uzA0wWgLQFZXEL4MbL`, « Touf ancien ») ne sert plus. Kael non plus.
`--modele`, `--similarite` et `--sans-boost` existent dans `voix.py` pour ça.

**Le canal Telegram « Tiktok » ne reçoit QUE les AC-** (Youssef, 28/10 : « les autres vidéos, publie
pas dans le canal quand c'est DROP&YOU ou autre »). `livrer.py` a l'identifiant du canal en dur :
ne jamais l'appeler sur une DY-, CB-, DA-, MQ-, GSX- ou vidéo client.

**FORMAT « LETTRE » (@darkearth) — demandé le 28/10/2026, référence : `motion/AC-M04/scenes.py`.**
Youssef a envoyé une vidéo de @darkearth sur LE SUJET D'AC-M02 (le Ballon d'Or de Kane), traité
autrement : « je te parle pas du design du montage, je te parle du FOND, comment il parle, comment
il a réussi à entraîner les gens ». Ce qu'il fait, mesuré sur sa transcription :
- **on parle AU sujet, pas DU sujet** : « Cher Harry, toi qu'on a si longtemps sous-estimé… ».
  Les titres à l'écran passent au **tutoiement** eux aussi, sinon l'illusion casse ;
- **3,25 mots/s** (nous étions à 4,47) : `voix.py --debit 3.45 --sans-hook --sans-resserrer`.
  **La règle « attaque toujours rapide » est suspendue sur ce format**, l'attaque d'une lettre est lente ;
- anaphore (« toi qu'on… toi qu'on… ») puis renversement ; le « on » collectif rend le spectateur complice ;
- **zéro chiffre jeté pour le chiffre**, une phrase à capturer par vidéo, **pas de CTA ni de question
  finale** : ça se termine sur une image ;
- chez lui il y a de la musique douce du début à la fin — on n'en met pas, c'est la pièce qui nous manque.

**Référence qui a percé sur le même sujet — @scarfoott, « Cher Kylian », 27/10/2026, 700 K vues
(29/10, Youssef : « c'est une vidéo comme ça que je t'aurais dû faire… entraîne-toi »).** Même lettre,
mais : sujet UNIVERSEL (le favori éternel qui perd, pas la polémique en Chine), sortie en 24 h, et
surtout **100 % archives réelles plein cadre** (lui enfant, la cérémonie, ses buts), une coupe
toutes les 2 s, musique douce, UNE ligne de sous-titre — **aucun titre, aucun pavé, aucun graphisme**.
AC-M04 posait la lettre dans la pièce noire avec titres et coupures : un habillage d'info sur un
texte d'émotion. La lettre appelle un **second format visuel** (archives + musique + sous-titre), à
faire valider avant de le coder. Détail : mémoire `reference-scarfoott-cher-kylian`.

**FORMAT « ARCHIVES » — LA BASE DE LA CHAÎNE DEPUIS LE 30/10/2026. Il annule le format bonhomme.**
Youssef : « **moins de motion + de vidéo et photo brut**, donc le gros du travail tu dois le faire
sur **récupérer les bons passages de vidéo**, et voilà, car ce format qu'on propose **ne fonctionne
pas jusqu'à preuve du contraire**. » C'est ce que montrait déjà le décorticage de la vidéo à 2,7 M :
100 % d'archives réelles plein cadre, zéro graphisme. **Mode d'emploi complet :
`motion/outils-archives.md`.** En résumé :

- **La source est archive.org, pas YouTube** (YouTube refuse tous les clients yt-dlp sur ce Mac,
  revérifié le 30/10). archive.org donne des fonds entiers : le procès O.J. Simpson complet
  (`OJ_Simpson_Trial_Compilation`, 492 fichiers, 195 Go, 480p), la couverture ABC du 17/06/1994…
- **Ne jamais télécharger un fichier entier** : `-ss` AVANT `-i` sur l'URL = requête de plage HTTP.
  Une image prise à 1 h 40 dans un fichier de 510 Mo coûte 10 s. **Le disque est plein à 97 %.**
- **Trouver le passage** : `moteur/outils/scan_archive.sh "<URL>" dossier debut fin pas` — balayage
  large, puis resserré deux fois. C'est là qu'est le travail.
- **Découpe verticale, deux traitements choisis au plan** : *plein cadre* pour un gros plan (tranche
  verticale `crop=205:362:<x>:0` puis `scale=1080:1920`, ~5× de grossissement, doux mais c'est ce
  que fait la référence) ; *pleine largeur nette + fond flou de la même image* pour un plan large.
- **Toujours couper l'incrustation** : le timecode des archives du procès est à **76-82 % de
  hauteur**, pas en bas — `crop=640:362:0:0`.
- **L'ffmpeg de ce Mac n'a ni `drawtext` ni `subtitles`** (pas de libass). Les sous-titres se rendent
  en PNG transparents avec Skia — `moteur/outils/soustitres_png.py`, **un seul mot à l'écran à la
  fois** — puis se superposent. **Ne pas faire passer l'archive dans le moteur Skia** :
  `prepare_video` ferait ~1 Go de cache pour 70 s.
- Démo : `motion/AC-M08/video/AC-M08-demo.mp4` (17 s d'AC-M07 refaites en archives, voix TOUF).
- **À trancher par Youssef** : la musique (la référence en a du début à la fin, notre règle dit non)
  et la signature de fin (la référence n'a aucune marque ; la démo garde un filigrane discret).

**FORMAT « BONHOMME » — ÉCARTÉ LE 30/10/2026, gardé au cas où (29/10/2026).** Youssef, après AC-M01→M04 :
« notre format visuel n'accroche pas et en plus il met trop de temps à produire, faut aller plus
simple… un bonhomme animé 2D, quand tu parles de quelqu'un tu peux animer un bonhomme ».
`moteur/bonhomme.py` (skill `~/.claude/skills/bonhomme-2d/`) : fond noir, une ligne de sol, des
bonhommes en bâtons blancs dont la tête est **la vraie photo du visage** dans un disque cerclé de
rouge, bulles, étiquettes, chiffres géants, accessoires dessinés (casque, flammes, billets, livre,
barreaux…), sous-titres de la chaîne. Rig articulé porté de GitHub (`stick-motion` : bras en
cinématique directe, jambes en cinématique inverse, marche sans glissement ; `stickman-story-reels` :
poses et playbook). **Plus de pièce 3D, plus de grille, plus de pavés** sur les AC- : rendu flat en
quelques minutes. Références : `motion/AC-M05/scenes.py` (deux bonhommes, Hanouna/Obispo) et
`motion/AC-M06/scenes.py` (une vie, le bonhomme grandit avec `taille`, fin sur le cercle rouge vide).
Règles : un bonhomme de gauche parle vers la gauche (`cote=-1`), celui de droite vers la droite ;
chiffres et titres en haut (y 300-420), têtes à y 475-725, étiquettes à y 1338 ; têtes recadrées
carré sur le visage dans `media/<nom>.jpg`, `B.SENS_PHOTO[nom]` = sens du regard. Voix Touf
`--debit 3.5` (≈ 3,8 mots/s réels) + `hook_rapide --mots 11 --debit 6.0` : 60 s de voix → 1:03.

**RÉFÉRENCE @darkearth À 2,7 M — « le gant d'O.J. Simpson » (envoyée le 29/10/2026 : « fais-moi la
même mais à une autre façon »).** C'est le carton de la chaîne de référence : 2 700 000 vues,
219 900 j'aime, 82 s, postée le 14/07/2026. Décorticage dans `~/darkearth/ref3/`. Mesuré :
- **les 10 premières secondes n'ont AUCUNE voix** : archives plein cadre, musique, et UNE phrase
  écrite tenue à l'écran (« Ils étaient certains de le condamner… jusqu'à ce qu'il enfile ce gant ») ;
- 229 mots à **3,23 mots/s**, 24 plans, **0,28 coupe/s**, le plan du gant tient 13 s d'affilée ;
- **sous-titres UN MOT à la fois**, capitales blanches ; zéro titre, zéro pavé, zéro graphisme,
  zéro logo, zéro CTA ; fin sur une image ;
- **les mots sensibles sont censurés à l'écran** (« M*RTS. ») : la modération lit par OCR. Chez nous
  ça se fait sans toucher à la voix — `sous_titres_bonhomme(K, fusions={(34,): "m*rt"})`.

**La leçon de fond, plus importante que la forme : ce n'est pas de l'actu.** C'est une histoire de
1995 que tout le monde connaît à moitié, avec un retournement. AC-M01→M06 sont toutes des news du
jour ; le plus gros succès de la référence est un RÉCIT. À tester régulièrement sur la chaîne.

**Notre réponse = `motion/AC-M07/scenes.py`** : même affaire, angle inverse. Lui raconte « un gant a
fait basculer le procès » ; nous racontons **comment le procureur s'est fait pousser à la faute**,
avec le détail qu'il a raté (le fabricant rapporte la même paire, neuve : elle va parfaitement).
Nouvelles briques dans `bonhomme.py` : `gant`, `banc` (le jury), `voiture`, `coche`.
⚠ @darkearth date l'essai du gant du 3 octobre 1995 : c'est la date du verdict, l'essai est du
**15 juin 1995**. Vérifier les dates d'une vidéo de référence avant de la reprendre.

**MONTAGE MOINS DYNAMIQUE — règle du 28/10/2026, après l'échec d'AC-M01 et AC-M02.**
« Faut être moins dynamique. Pour notre format faut plus un truc où les gens soient immersés
totalement, où ils peuvent suivre, où t'as calculé chaque mouvement et animation de façon à
captiver le cerveau. » Référence de mise en œuvre : **`motion/AC-M03/scenes.py`**.
- 9 scènes pour 68 s (AC-M02 en avait 12) : un plan tient 8 à 10 s ;
- **un seul élément à la fois** : un pavé n'arrive qu'une fois le précédent sorti (alpha `av`) ;
- `effet="masque"` partout, plus de `"ressort"` ; **un seul `surlignage` dans toute la vidéo**,
  posé sur la phrase qui fait mal ;
- grille à vitesse constante (0,42) avec 3 respirations douces (×1,1) au lieu de 6 à ×2,6 ;
- 2 éclairs au lieu de 11, ~28 bruitages au lieu de 51, aucun confetti ni éclat sur un sujet grave ;
- les blocs de `rapide()` (flou de mouvement) se limitent aux vraies bascules.

`conformite.py` ne vise que les projets CB- et DY- : sur cette chaîne on **nomme** les films, les
studios et les marques, c'est de l'information. En revanche la **vérification à la source** est
obligatoire avant d'écrire un script (voir `~/dyou-veille-people/README.md`).

## Reprendre ailleurs

`REPRISE.md` (dans ce dossier, section « Niveau actuel » en tête) est le prompt à donner à un autre Claude ou à ChatGPT. Les vidéos finies et les médias
de chaque vidéo (rushes, voix, captures) sont dans le dépôt **privé** `dyou-assets` (`motion-videos/`, `motion-medias/<ID>/`),
jamais dans ce dépôt public.

## Compte ElevenLabs et rendu — à jour au 27/10/2026

**Les voix ont changé de compte.** Le Starter `dropandyou` est abandonné au profit de
**youssef@dyou-agency.com (Creator)**. ElevenLabs n'autorise aucun transfert de compte à compte pour les
clones instantanés et les voix dessinées (seuls les clones professionnels se partagent) : toutes les voix
ont été recréées, donc **tous les voice_id ont changé**.

| Voix | Ancien id | Nouvel id |
|---|---|---|
| Tomy (motion) | `Lt0unAbeM6JystrA2RTv` | `BBiN2YrSqm8dBdXxsFlJ` |
| Léo (aigu, accent espagnol) | `haslyGsX7Yvfg11C5acm` | `WlCMkszs6Oz7vBhdUzrd` |

**Réglage fixe de Léo — validé le 29/10/2026** : `eleven_turbo_v2_5` + `language_code: "es"`, stabilité 0,45,
style 0,15, similarité 1,0, sans speaker boost, speed 1,0, **aucun atempo** (il parle tranquillement, un peu
timide), et **les R triplés dans le texte** (« trrravaille », « prrroblème »). Le réglage énergique
(0,30 / 0,50 + ×1,15) est abandonné. Scribe sur chaque prise, une sur trois sort écorchée.
| Léo (premier clone) | `aL1wJJpipWiIPjPi1jzZ` | `nkNOioEZLcZVKhVdB4sk` |
| Seedance cagoule moto | `IbgOdhbKXd3uBjUO8aHA` | `NBH3DyOfYwDIjZZRj2Og` |
| Seedance boucle moto | `fDOPUqPwDA8tr9PAy2xw` | `9IXe47HGvRNshQI7nJT0` |
| Avital | `ceEUAp9GlR900XIwMTq2` | `jXVZY30NbecT0ooKH1Ba` |
| Avital vlog | `zchjMHCgSyHNevwHbPa9` | `24zyhi85Y3hHyfTkAtE2` |
| Bernard | `pRnWjjXVgCRKGXWLMSks` | `HUFukTz6xld4M8wkzhzE` |

Tomy et les trois autres voix dessinées n'avaient aucun échantillon : elles ont été **reclonées depuis leur
propre audio d'historique**. Comparé sur le script de DY-M19 passé deux fois dans le moteur : ancien 24,57 s,
nouveau 25,04 s, débit naturel 3,46 contre 3,39 mots/s — l'atempo de `voix.py` recale, l'écart ne s'entend pas.
`~/.config/dyou/elevenlabs.json` porte déjà la nouvelle clé et le nouveau Tomy ; sauvegarde complète des
échantillons et de l'audio source dans `~/elevenlabs-backup/` (hors dépôt).

**Comparer deux voix se fait avec le moteur, jamais à la main** : une prise brute ElevenLabs sort à
~3,4 mots/s et sonne molle. Copier le `script.txt` et le `media/voix-brut.mp3` d'un projet rendu dans deux
dossiers, puis `voix.py --debit 4.2` d'un côté (gratuit, il réutilise la prise) et
`voix.py --forcer --voix <id>` de l'autre.

**Le rendu se lance avec `/usr/bin/python3`.** Le `python3` du PATH est passé à Homebrew 3.15 et n'a ni
numpy ni skia ; les paquets du moteur sont installés pour le Python 3.9 d'Apple
(`~/Library/Python/3.9/lib/python/site-packages`).

```
cd video-factory/motion/MON-ID
/usr/bin/python3 ../moteur/rendu.py video
/usr/bin/python3 ../moteur/outils/mixer.py --lufs -13 renders/image.mp4
```

Les outils qui ne font que du réseau ou du FFmpeg (`voix.py`, `hook_rapide.py`) tournent avec n'importe
quelle version.
