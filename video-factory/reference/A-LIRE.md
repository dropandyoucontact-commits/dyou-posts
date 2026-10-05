# Le standard : CB-M01 « Le réseau en direct »

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
occupe au moins la moitié de cette zone. On le vérifie sur des images **tirées du MP4
final**, une toutes les 0,4 s, en cherchant les plans trop blancs.

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

## Ce qu'on vérifie avant de livrer

1. Des images extraites **du MP4 final** sur toute la durée (`outils/verifier.py`) :
   espaces entre les mots, rien qui déborde d'un cadre, rien qui se chevauche, aucun mot
   illisible pendant un glissement de surlignage.
2. Volume intégré à −16 LUFS, crête sous −1 dBFS, durée = voix + carton final.
3. Aucun chiffre inventé à l'écran.
