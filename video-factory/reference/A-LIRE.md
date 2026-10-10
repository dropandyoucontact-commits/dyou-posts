# Le standard : CB-M04 et CB-M05 (validés le 06/10/2026)

Première vidéo validée : CB-M01 « Le réseau en direct » (05/10/2026), décrite ci-dessous. Niveau de
référence actuel : CB-M04 et CB-M05 v2, voir « La méthode validée ».

## CB-M01 « Le réseau en direct »

Référence : `../motion/CB-M01/video/CB-M01.mp4` (59,4 s), source dans `../motion/CB-M01/`.
Validée par Youssef le 5 octobre 2026 : « c'est le niveau que j'accepte ». Ces règles
sont fixées par Claude, seul responsable du motion ; aucune autre consigne ne les remplace. Une vidéo en
dessous de ce niveau ne se livre pas. L'ancien exemple RES-01 et son script ont été
retirés de ce dossier (ils restent dans l'historique git).

## Ce qui fait le niveau

**Le texte, d'abord.** Sous-titres en Inter Display Black, 96 à 104 px, centrés en haut
(à partir de y = 292), deux ou trois lignes. Chaque mot apparaît au moment exact où il
est prononcé (petit rebond), et un fond vert glisse sous le mot en cours (rouge pour les
mots qui parlent de la marge de l'intermédiaire). Le mot que le fond quitte ne reprend sa
couleur qu'une fois découvert : jamais de vert sur vert. Les mots-clés gardent leur
couleur après coup. Le texte est toujours mesuré et dessiné par le même moteur : aucune
position calculée avec une autre police.

**Une idée = une image qui bouge.** Pas de fiches empilées : des métaphores physiques.
Dans CB-M01 : la marge du revendeur qui écrase la tienne dans une barre de prix ; un colis
qui prend une étiquette « + marge » ; des ciseaux qui coupent l'intermédiaire ; un
calendrier qui défile jusqu'à 14 ; des contacts éliminés un à un ; un interrupteur
« Intermédiaire → Direct » ; « CHINA » tapé lettre par lettre au rythme de la voix.

**Jamais de vide.** Remarque de Youssef le 5 octobre 2026 sur CB-M01 : à plusieurs
moments (début de scène, sortie d'une carte) la moitié de l'écran était blanche et seul
le sous-titre bougeait. Règle : chaque phrase a son visuel **dès son premier mot** ; une
scène entre avant que la précédente ne sorte (chevauchement de 0,2 s) ; la zone entre les
sous-titres et y = 1 440 ne reste jamais sans objet plus de 0,3 s ; le visuel d'une phrase
occupe au moins la moitié de cette zone. On le vérifie avec `motion/moteur/outils/vide.py` (rend une image tous les 0,1 s et cherche la plus grande
bande vide de la zone centrale ; seuil 300 px) et sur des images **tirées du MP4 final**.

**Le rythme.** Un changement visible au moins toutes les secondes. Chaque mot important
déclenche quelque chose : apparition avec rebond, tampon, secousse, éclair de couleur
léger (10 %), confettis sur les moments de victoire. Transitions franches (coup de fouet
avec flou de mouvement, zoom traversant, disque vert qui remplit l'écran), jamais de
fondu mou.

**Le relief.** Cartes blanches arrondies avec ombre douce, produits détourés avec ombre au
sol, vraie perspective 3D sur les entrées (`Espace`), flou de mouvement par sous-images
sur les mouvements rapides (`rapide(t0, t1)`).

**La charte.** Fond blanc à points discrets qui montent. Noir `#0B0F0D`, vert `#00B862`,
rouge `#FF3B30` réservé à l'intermédiaire et à sa marge. Logo ChinaBook recoloré vert et
noir (blanc sur fond vert). Un seul bandeau de marque discret en haut.

**Le son.** Voix à −16 LUFS ; ~180 bruitages synthétisés (whoosh, impact, pop, clic,
verre, frappe…) posés dans `scenes.py` à côté de l'animation qu'ils accompagnent, et
atténués automatiquement sous chaque mot. Pas de musique.

**Le cadre.** Rien d'important sous 1 440 px, ni à moins de 70 px des bords. La première
image est déjà forte (produit + premier mot visibles) : c'est la miniature. Le carton
final tient 1,5 s après la voix (logo + bouton d'appel).

## La méthode validée : CB-M04 et CB-M05 (06/10/2026)

Youssef, après CB-M04 « T'as tout faux » et CB-M05 « Reste ici » : « c'est parfait ».
**Toute vidéo ChinaBook courte se fait désormais comme ces deux-là** (`motion/CB-M04/`,
`motion/CB-M05/`, leurs `DECOUPAGE.md`). La recette :

1. **Une accroche = une cible = une vidéo.** On teste plusieurs accroches sur la même offre
   (plateformes / voyage / Français installé en Chine…) plutôt que de tout dire dans une vidéo.
   L'accroche nomme la cible dès le premier mot (« Stop. Tu fais de l'achat-revente… »,
   « Tu comptes aller à Kinbo… »).
2. **Script de 90 à 105 mots (≈ 520-570 caractères), voix Tomy à 3,8 mots/s** :
   `voix.py --debit 3.8` → 23 à 27 s de voix, + 1,5 s de carton final.
   Structure : accroche → la vérité qui dérange → preuve (« j'y suis allé », rushs, lieux) →
   ChinaBook = contacts validés dans ton téléphone → ce que tu y gagnes → « Envoie-moi CHINA sur WhatsApp ».
3. **Image 0 = la vignette** : un objet fort déjà en place et net (panneau STOP, carte
   d'embarquement), jamais de flou de mouvement sur les 0,25 premières secondes.
4. **Un plan par phrase, chaque élément au mot qui le nomme** (`TW(i)`) : cartes qui se
   barrent, tampons, pastilles, globe avec arcs (avion, message WeChat, colis), téléphone
   avec Snapchat / contacts ChinaBook, rushs de Youssef dans le téléphone.
5. **Photos de lieux (Kinbo, SEG…) : 1 seconde maximum**, au mot qui les nomme, en
   carte photo qui claque puis repart (`photo_lieu` dans CB-M04/CB-M05).
6. **Jamais de vide** : quand une liste se construit mot après mot, des emplacements
   « ? » gris occupent déjà la place et se remplissent au mot. `outils/vide.py` ne doit
   plus signaler que les glissements entre scènes (≤ 0,3 s).
7. **Sur « ChinaBook »** : disque noir plein écran, logo blanc qui claque ; les sous-titres
   passent en blanc pendant le disque (`SOUS.dessine(c, t, C["blanc"] if r > 900 else C["ink"])`).
8. **Aucun chiffre inventé** : coûts, marges et prix sont des barres, des cartes ou
   « des milliers d'euros » si Youssef l'a dit — jamais un montant.
9. **Son : `mixer.py --lufs -9`** (depuis DY-M02, 09/10/2026 : voix montée seule ≈ −10 LUFS, bruitages bien audibles, relevés de 2 dB après DY-M02). Avant : −11 LUFS / −1 dB crête, voix compressée. Plus
   jamais −16 : trop faible sur téléphone.
10. **Vérifier le MP4 final** (`verifier.py` sur toute la durée + `vide.py`), corriger,
   re-rendre, puis seulement livrer. Code dans `dyou-posts`, vidéo finie dans le dépôt privé.

11. **Corrections de Youssef (06/10/2026), à ne plus refaire :**
   - **Une plateforme nommée n'est qu'un exemple.** Dire « Hipobuy, Oopbuy, ou ce genre de
     plateforme », jamais comme si c'étaient les seules.
   - **Le billet d'avion du client ne va pas en Chine.** Quand on parle de quelqu'un qui a déjà sa
     clientèle et qui prend un billet, l'idée est « tu peux travailler de n'importe où » (Thaïlande,
     Maroc…) et gérer ses commandes à distance — pas « tu pars en Chine ». La Chine n'apparaît que
     pour les fournisseurs. Le message ChinaBook : on n'a plus besoin d'aller en Chine.

12. **Le hook de DY-M01 (08/10/2026, validé « c'est parfait, garde ce niveau ») :**
   - **Jamais un grand logo + un sous-titre qui disent la même chose.** Un fond uni avec « Bienvenue
     chez… » n'arrête pas le scroll : l'attention naît quand les articles apparaissent.
   - **Dès l'image 0 : le produit en action, en 3D.** Téléphone en perspective (`Espace`, `matrice3d`),
     produits détourés qui jaillissent vers la caméra (profondeur Z, flou de mouvement, secousse + lueur
     d'écran à chaque sortie), puis le téléphone se pose exactement dans la pose de la scène suivante
     (raccord sans coupure). Référence : `motion/DY-M01/scenes.py`, scène S1.
   - Produits clairs détourés avec **rembg** (le détourage par composantes connexes mange les baskets blanches).

## Ce qu'on vérifie avant de livrer

1. Des images extraites **du MP4 final** sur toute la durée (`outils/verifier.py`) :
   espaces entre les mots, rien qui déborde d'un cadre, rien qui se chevauche, aucun mot
   illisible pendant un glissement de surlignage.
2. Volume intégré à −11 LUFS, crête sous −1 dBFS, durée = voix + carton final.
3. Aucun chiffre inventé à l'écran.
