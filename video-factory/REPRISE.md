# Prompt de reprise — vidéos motion DYOU / ChinaBook / DROP&YOU

À coller tel quel dans Claude (claude.ai, Claude Code cloud ou une autre machine) ou dans ChatGPT, quand la session
habituelle n'est pas disponible. Tout le savoir-faire est dans deux dépôts GitHub du compte `dropandyoucontact-commits` :

| Dépôt | Visibilité | Contenu |
|---|---|---|
| `dyou-posts` | **public** | le moteur de montage, le code de chaque vidéo, les règles et les techniques — **jamais de média dedans** |
| `dyou-assets` | privé | `motion-videos/` = toutes les vidéos finies (les exemples) ; `motion-medias/<ID>/` = rushes, voix, captures de chaque vidéo ; `motion-banque/` = banque produits |

Pour refaire une vidéo avec le moteur : cloner les deux, copier `dyou-assets/motion-medias/<ID>/` dans
`dyou-posts/video-factory/motion/<ID>/media/`, puis suivre la chaîne ci-dessous.

---

Tu reprends la production de vidéos verticales (1080×1920, 60 i/s) pour Youssef : pubs **DYOU Agency** (agence qui crée
des sites à l'image de la marque d'artisans et d'indépendants), vidéos **ChinaBook** (guide pour acheter en Chine) et
**DROP&YOU** / **China Factory** (boutiques). Réponses en français, pas de jargon anglais.

## À lire d'abord, dans l'ordre (dépôt `dyou-posts`)

1. `video-factory/CLAUDE.md` — qui décide, chaîne de production, règles de contenu, **les trois façons de monter**,
   le style agence, la référence DA-M04.
2. `video-factory/reference/A-LIRE.md` — ce qui fait le niveau, la méthode validée (CB-M04/CB-M05), les vérifications.
3. `video-factory/motion/LISEZ-MOI.md` — comment démarrer une nouvelle vidéo.
4. `video-factory/LIGNE-EDITORIALE.md` — sujets, organique vs pub, appels à l'action.
5. Le `scenes.py` de la vidéo modèle la plus proche (liste ci-dessous), et regarder la vidéo finie correspondante
   dans `dyou-assets/motion-videos/`.

## Les vidéos validées qui servent de modèles

| ID | Ce que c'est | Retour de Youssef |
|---|---|---|
| CB-M04, CB-M05 | motion pur fond blanc, ChinaBook — la recette de base | « c'est parfait » |
| DY-M01 v2 | hook 3D : téléphone en perspective, produits qui jaillissent | « garde ce niveau » |
| DY-M02 v2 | rushes mains + téléphone à **écran vert**, site incrusté, panneaux en verre fumé | « celle-ci est la bonne » |
| DY-M03 | habillage d'une vidéo déjà montée, sans voix, repères suivis par flux optique | « c'est parfait » |
| DA-M04 | **montage hybride** : hook selfie plein écran, rushes dans des mockups, écran vert dans un cadre de verre | « la vidéo est parfaite, ça c'est du montage » |
| DA-M05 | même chose que DA-M04 pour les artisans des sols en résine (site POLYRA) | livrée le 10/10/2026 |

## La chaîne (moteur Python + Skia, `video-factory/motion/moteur/`)

1. `motion/<ID>/script.txt` (95-105 mots, tutoiement, oral, une cible par vidéo).
2. Voix : `python3 ../moteur/outils/voix.py --debit 3.8` — ElevenLabs, voix **Tomy** (`Lt0unAbeM6JystrA2RTv`,
   eleven_v4, `language_code: "fr"`), horodatage de chaque mot → `timing.json`. Clé dans `~/.config/dyou/elevenlabs.json`.
3. Rushes à écran vert : `suivi_vert.py` (détourage G − max(R,B) + suivi des 4 coins, voir DA-M05).
4. `scenes.py` : chaque élément tombe sur le mot qui le nomme (`TW(i)`), jamais une seconde écrite à la main.
5. `python3 ../moteur/rendu.py apercu t1 t2 …` (planche), puis `python3 ../moteur/rendu.py video` (~17 min sur le Mac).
6. Bruitages : écrire `sfx.json` depuis `scenes.SFX`, puis `python3 ../moteur/outils/mixer.py --lufs -9 renders/image.mp4`
   → `video/<ID>.mp4` (voix ≈ −10 LUFS, bruitages 1 LU dessous et baissés sous chaque mot, crête ≤ −1 dB).
7. **Vérifier le MP4 final** : `outils/verifier.py video/<ID>.mp4 t1 t2 …` et `outils/vide.py`. Jamais livrer sur la foi des aperçus.
8. Code dans `dyou-posts` (public, sans médias), vidéo finie et médias dans `dyou-assets` (privé).

## La forme validée des pubs DYOU Agency (DA-M04 / DA-M05)

- **Un seul rush en plein écran : le hook** (le personnage en selfie, ~3 s). Tout le reste est du motion.
- Les autres rushes vont dans un **téléphone 3D sombre** qui flotte ; les rushes à **écran vert** (téléphone, ordinateur)
  passent dans un **grand cadre de verre dépoli**, contenu incrusté dans le vert, sous les doigts.
- Des blocs découpés dans la capture du site (Chrome headless, 520 px ×2) **sortent de l'écran** en panneaux de verre,
  surlignés au mot qui les nomme. Ne jamais cacher le visage du personnage avec un panneau.
- Fond sombre vivant, verre dépoli, particules. Accent = couleur du site montré (`theme_athla()`, `theme_polyra()` dans `agence.py`).
- **Sous-titres fins** blancs, mot flou → net à son temps. **Aucun surlignage, aucun mot coloré.**
- Pastilles de verre courtes, notifications, icônes Lucide ; bruitage sur chaque apparition, pas de musique.
- Fin : champ de commentaire où le mot-clé se tape puis s'envoie, « Je t'explique en privé », logo DYOU, carton
  « Commente « MOT » sous la vidéo » + dyou-agency.com. Pas de WhatsApp public pour l'agence.
- Script : accroche ciblée (« Si tu fais X, reste ici, c'est pour toi ») → le travail de la cible → le problème → « Nous, on te
  crée… » + bénéfices montrés sur le site → « Tu veux le même ? Commente « MOT » ». Texte différent à chaque vidéo.
- Ne jamais inventer de prix, de chiffre, de témoignage. Un faux « vieux site » porte un nom fictif.

## Rushes de Youssef

Il les génère lui-même (Grok, Higgsfield…) : personnage muet, 720×1280, 3-10 s. Pour un écran à incruster : **vert
chroma uni mat, 4 coins visibles, mouvement lent, haute résolution**. Il dit lui-même quel rush va où ; sinon : le selfie
en hook, le reste dans les mockups.

## Si tu n'as pas le moteur (ChatGPT sans exécution de code)

Reproduis la même chose dans CapCut / After Effects : hook plein écran 3 s, fond sombre, téléphone 3D, cadre de verre,
incrustation sur écran vert (incrustation chroma + suivi de plan), panneaux en verre dépoli, sous-titres blancs fins,
champ de commentaire animé, voix Tomy. Donne à Youssef le découpage plan par plan, avec le mot de la voix qui déclenche
chaque élément, en t'appuyant sur le `scenes.py` du modèle le plus proche (les temps y sont écrits en `TW(numéro du mot)`).
