# Grammaire du mouvement — ce qu'on prend aux meilleurs (14/10/2026)

Youssef : « va voir sur GitHub s'il n'y a pas de meilleurs skills d'animation motion design ». Sources lues :
- `echris6/motion-video-kit` (MIT, 1,1 k étoiles) — règles tirées de 28 films de lancement pros (81 647 images analysées)
  et de vrais refus de clients ;
- `Vincentwei1021/video-talkcraft` (1,6 k étoiles) — catalogue de ~110 figures d'animation (HTML/GSAP) ;
- les skills Remotion officiels (`remotion-dev/skills`, 5 k étoiles).
Aucun n'est installé : ils supposent React/Remotion ou HTML + navigateur, notre moteur est Python + Skia (plus léger sur
le Mac de Youssef). On en garde les règles, qu'on applique dans `moteur/`.

## Les six règles

1. **Le premier plan devient la transition.** Un titre, un logo ou une forme traverse la caméra (zoom, flou directionnel)
   pendant que la scène suivante est déjà en place dessous. Jamais de trou entre deux scènes.
2. **Un acteur persistant.** Un même objet (téléphone, carte, curseur, colis) garde son identité d'un plan à l'autre.
   Des apparitions sans lien, même belles, font diaporama.
3. **La densité vient de la hiérarchie.** Un mouvement principal, des décalages secondaires (cartes, étiquettes), des
   détails tertiaires (reflets, coches) qui se chevauchent. On n'arrête pas tout l'écran à chaque temps.
4. **Changer de vitesse.** Arrivée qui ralentit (on lit) → sortie rapide. Pas de dérive à vitesse constante.
5. **Les coupes franches marchent** si sujet, échelle, direction et matière se répondent et que le mouvement continue.
6. **Cause → effet.** Chaque action produit un résultat visible : un scan sort un résultat, un bouton change d'état,
   un prix tombe.

## Composition

- Le sujet principal occupe **60 à 85 %** de la zone utile. Le vide fait « pas cher ».
- 1 à 2 choses à lire à la fois.
- Varier les compositions : gros plan objet, vue large, vue de dessus, interface en gros plan, typo d'impact.
  Jamais deux fois « titre au-dessus de trois cartes ».
- Le texte fait partie de la chorégraphie : gros mots qui entrent sur des axes opposés, qui masquent ou révèlent la
  scène suivante ; jamais posé sur une image chargée sans fond.
- **Image 0 = composition finie**, pas un mot à moitié entré.

## Rythme (30 s)

- 12 à 15 compositions, temps de 1,4 à 3,5 s, **aucun arrêt de plus de 0,6 s** (sauf le carton final, 1,5-2 s, qui dérive
  doucement). Contrôle chiffré à faire sur chaque rendu : temps cumulé d'images quasi identiques ≤ 1 s par 30 s.

## Figures à ajouter au moteur (catalogue talkcraft, adaptées)

crash-zoom-punch (coup de zoom sur le mot fort) · whip-pan (filé) · black-slam (claque noire entre deux temps) ·
behind-text-title (le titre passe derrière le sujet) · highlighter-sweep (surligneur qui passe) · strike-and-replace
(mot barré remplacé) · number-counter / number-slab-pop (chiffres) · map-route-pin (trajet sur carte) ·
split-compare-slider (avant/après au curseur) · stack-fan-out (cartes en éventail) · countdown-arc (compte à rebours) ·
focus-dim-spotlight (tout s'assombrit sauf le sujet) · reticle-lock-on (viseur qui se verrouille) ·
word-slot-cycle (mot qui défile comme une machine à sous).

## Son (leçons des refus clients)

- Bruitages **courts et propres**, sans grave qui bourdonne (moins de 50 % d'énergie sous 150 Hz), seulement sur de
  vraies actions (clic sur clic, pop sur badge, check quand ça se pose). Deux sons à moins de 0,15 s : baisser le second.
- Pas de « tic » qui pique dans les 2-8 kHz (+4 dB maximum dans sa bande).
- Une musique avec une pulsation aide les coupes à tomber sur le temps (Youssef peut ajouter un son tendance dans
  TikTok : on livre alors une version voix + bruitages seuls).
- Pour TikTok, Youssef veut **fort** : −7 à −8 LUFS, crête ≤ −1 dB.
