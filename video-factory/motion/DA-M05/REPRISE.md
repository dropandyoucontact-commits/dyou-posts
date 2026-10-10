# Prompt de reprise — vidéos DYOU Agency « artisan + rushes + mockups »

À coller tel quel dans Claude (cloud ou Claude Code sur une autre machine) ou dans ChatGPT.

---

Tu reprends la production de pubs vidéo verticales pour **DYOU Agency** (dyou-agency.com), une agence qui crée des
sites internet à l'image de la marque d'artisans et d'indépendants. Objectif de chaque vidéo : faire commenter un
mot-clé à la cible (artisans résine, coachs sportifs…) pour leur vendre un site.

## Le dépôt

GitHub `dropandyoucontact-commits/dyou-posts`, dossier `video-factory/`. Lis d'abord, dans l'ordre :
1. `video-factory/CLAUDE.md` (règles, chaîne de production, section « DA-M04 — référence de montage hybride ») ;
2. `video-factory/motion/DA-M04/scenes.py` : **le modèle validé** (« la vidéo est parfaite, ça c'est du montage ») ;
3. `video-factory/motion/DA-M05/` : la même chose pour les artisans de la résine époxy (le dossier où tu es).

Les médias (rushes, voix, rendus) ne sont PAS sur GitHub (dépôt public) : Youssef te les renvoie.

## La forme validée (DA-M04 « Stop, coach »)

- Format 1080×1920, 60 i/s, 23-27 s de voix + ~1,5 s de carton final.
- **Un seul rush en plein écran : le hook** (le personnage filmé en selfie, 3 s). Tout le reste est du motion.
- **Les autres rushes vont dans des mockups** : un téléphone 3D sombre légèrement incliné qui flotte, et les rushes à
  **écran vert** (téléphone, ordinateur) passent dans un grand cadre de verre dépoli, avec du contenu incrusté dans le vert
  (détourage du vert + suivi des 4 coins de l'écran, image par image, en suivant les doigts qui passent devant).
- Des blocs découpés dans la capture du site **sortent de l'écran** en panneaux de verre fumé (3D, rebond), et sont
  surlignés au mot qui les nomme.
- Style agence : fond sombre vivant, verre dépoli, particules, liseré clair. Couleur d'accent = celle du site montré
  (ATHLA : #C8FF2E ; POLYRA résine : cuivre / or rosé #E0A070 → #B8683C sur noir).
- **Sous-titres fins** : la phrase en cours en blanc, chaque mot qui se pose flou → net à son temps. **Aucun surlignage,
  aucun mot coloré, pas de karaoké.** Sous-titres masqués pendant le logo de fin.
- Chaque animation tombe **sur le mot** qui la nomme (minutage mot à mot de la voix), jamais à une seconde écrite à la main.
- Pastilles de verre courtes (« Ton site », « Payé en ligne »…), notifications, icônes Lucide.
- Fin : champ de commentaire où le mot-clé se tape lettre par lettre puis s'envoie (cœur), « Je t'explique en privé »,
  disque logo DYOU, carton « Commente « MOT » sous la vidéo » + dyou-agency.com. Pas de numéro WhatsApp pour l'agence.
- Bruitages sur chaque apparition (whoosh, pop, verre, clic, ding, frappe clavier), pas de musique.

## Voix et son

- Voix off française ElevenLabs « Tomy » (voice_id `Lt0unAbeM6JystrA2RTv`, modèle eleven_v4, `language_code: "fr"`,
  sinon l'accent part en québécois), endpoint *with-timestamps* pour avoir le temps de chaque mot.
- Accélérée à ~3,8 mots/s sans changer la hauteur. Script de 95-105 mots, tutoiement, phrases courtes, oral.
- Mix : voix compressée seule autour de −10 LUFS, bruitages ~1 LU dessous et baissés sous chaque mot, mix final
  −9 à −10,5 LUFS, crête ≤ −1 dB. Jamais de bruitages plus forts que la voix.

## Structure du script (psychologie)

Accroche ciblée (« Si tu fais X, reste ici, c'est pour toi ») → le quotidien / le travail de la cible → le problème
(un vieux site qui ne représente pas son travail, le client part ailleurs) → « Nous, on te crée un site à l'image de
ta marque » + 3-4 bénéfices concrets montrés sur le site de démo → « Tu veux le même pour ton entreprise ? Commente
« MOT », et je t'explique tout. » Aucun prix, aucun chiffre ni témoignage inventé. Texte différent à chaque vidéo
(les algorithmes repèrent les doublons).

## DA-M05 « Résine » (en cours le 10/10/2026)

Script : `DA-M05/script.txt`. Rushes (720×1280, 24 i/s, muets, personnage blond moustachu, maison de luxe, sol en résine marbrée) :
- `r1` 3,2 s **selfie** qui montre le sol → plein écran, le hook (« Si tu fais des sols en résine comme celui-ci… ») ;
- `r2` 3,9 s ponçage à la ponceuse, `r3` 4,3 s coulée de la résine à la raclette → dans le téléphone (« poncer, préparer, couler ») ;
- `r4` 6 s assis, ordinateur portable à écran **vert**, il s'énerve et le jette → on incruste un **vieux site moche**
  (fabriqué, nom fictif) sur « un vieux site, trois photos floues… », il le jette sur « Résultat » ;
- `r5` 6 s il tient un téléphone à écran **vert** et le pointe → on incruste **POLYRA**, notre site de démo résine
  (dyou-agency.com/realisations/polyra/, capture mobile 520 px ×2), blocs qui sortent : hero « Le sol devient signature »,
  finitions (Perle, Obsidienne, Sur mesure), méthode (Écouter, Préparer, Composer, Couler), bouton « Imaginer mon sol » = devis ;
- `r6` 6 s il marche vers la caméra puis selfie → dans le téléphone sur « Tu veux le même ? », avant le champ « RÉSINE ».

## Si tu n'as pas le moteur (ChatGPT, ou sans le dépôt)

Reproduis la même chose dans CapCut / After Effects : hook plein écran 3 s, puis fond sombre, téléphone 3D, cadre de verre,
incrustation sur écran vert (incrustation chroma + suivi de plan), panneaux en verre dépoli, sous-titres blancs fins,
champ de commentaire animé, voix Tomy. Donne à Youssef le découpage plan par plan avec le mot de la voix qui déclenche
chaque élément.
