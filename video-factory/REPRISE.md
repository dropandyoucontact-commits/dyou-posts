# Prompt de reprise — vidéos motion DYOU / ChinaBook / DROP&YOU

À coller tel quel dans Claude (claude.ai, Claude Code cloud ou une autre machine) ou dans ChatGPT, quand la session
habituelle n'est pas disponible. Tout le savoir-faire est dans deux dépôts GitHub du compte `dropandyoucontact-commits` :

| Dépôt | Visibilité | Contenu |
|---|---|---|
| `dyou-posts` | **public** | le moteur de montage, le code de chaque vidéo, les règles et les techniques — **jamais de média dedans** |
| `dyou-assets` | privé | `motion-videos/` = toutes les vidéos finies (les exemples) ; `motion-medias/<ID>/` = rushes, voix, captures de chaque vidéo ; `motion-banque/` = banque produits |

Pour refaire une vidéo avec le moteur : cloner les deux, copier `dyou-assets/motion-medias/<ID>/` dans
`dyou-posts/video-factory/motion/<ID>/media/`, puis suivre la chaîne ci-dessous.

## Niveau actuel (19/10/2026) — commence ici, le reste du fichier est plus ancien

Le niveau à atteindre, ce sont les dernières vidéos. Regarde d'abord le MP4 fini dans `dyou-assets/motion-videos/`,
puis lis son `scenes.py` dans `dyou-posts/video-factory/motion/<ID>/`, puis les modules du moteur qu'il importe.

| Vidéo de référence | Ce qu'elle montre | Modules (`video-factory/motion/moteur/`) |
|---|---|---|
| **DA-M17-EN** (pub motion) et **DA-M18-EN** (pub sites) | les plus récentes : fond clair studio, cartes en verre clair, **signature 3D DYOU** à la fin | `verre_studio.py` + `studio3d.py` / `sites3d.py` + `studio.py` |
| DA-M14-EN-v2, DA-M16-EN-v2 | les mêmes en verre fumé sombre (cartes UI animées, vitrine de sites, rendu qui avance) | `glace.py` |
| DA-M10-EN à DA-M16-EN | studio clair en vraie perspective 3D (caméra, plans, décollage) | `studio3d.py`, `sites3d.py` |
| DY-M15 | signature explosive DROP&YOU (médias aspirés, explosion, logo extrudé) | `signature.py` |
| GSX-M01 à GSX-M04 | client GSX : fond blanc, verre clair, signature 3D à la couleur du client | `gsx.py` |
| DY-M10, DY-M11, CB-M15 | style cobalt (bleu nuit / orange) en 3D | `cobalt.py`, `dy3d.py` |
| MQ-M05 | client MONARQUE, niveau validé par le client | `monarque.py`, `mq.py` |

Ce qui fait le niveau, dans le code :
- **3D sans moteur 3D** : `studio3d.py` (`Cam`, `Plan`, `rot3`, `compose`) projette des plans en perspective dans Skia.
- **Verre** : `verre()` dans `verre_studio.py` (clair) et `glace.py` (sombre) : flou d'arrière-plan, halo, liseré dégradé.
  Les deux thèmes s'appliquent en remplaçant `rrect` / `carte_s` dans les modules (`appliquer()` / `_installe`).
- **Signature 3D** : `verre_studio.signature()` (et `signature.py`, `gsx.py`) : médias aspirés au centre → explosion
  (flash, ondes, éclats de verre, étincelles) → anneau de cartes → sigle extrudé en couches qui tourne et claque →
  nom en tranches qui volent → bouton cliqué, adresse tapée. Calée sur le mot de la voix (`T_BOUM`).
- **Tout tombe sur un mot** : `TW(i)` / `M["mot"]` lus dans `timing.json`, jamais une seconde écrite à la main.
- **Hook rapide** : `outils/hook_rapide.py` (lancé par `voix.py`) accélère et renforce la 1re phrase. Jamais de ralenti sur un clip.
- **Zone sûre TikTok/Snap** : `outils/zone_tiktok.py` (~96 px rognés de chaque côté, boutons à droite x > 860).
- **Son** : `outils/mixer.py --lufs -13` (−13 LUFS, crête ≤ −1 dB) ; un bruitage sur chaque apparition, pas de musique.
- **Conformité** : `outils/conformite.py` avant chaque rendu DROP&YOU/ChinaBook (pas de marque, de WhatsApp/Snap, de promesse de gain).

### Installer le moteur ailleurs que sur le Mac (tablette → Claude Code dans le cloud, ou toute machine Linux)

```
git clone git@github.com:dropandyoucontact-commits/dyou-posts.git
git clone git@github.com:dropandyoucontact-commits/dyou-assets.git      # privé
pip install skia-python numpy pillow scipy
apt install ffmpeg                                                        # ou brew install ffmpeg
cd dyou-posts/video-factory/motion
cp -r ../../../dyou-assets/motion-medias/moteur/. moteur/media/            # logos, images du moteur
mkdir -p banque && cp -r ../../../dyou-assets/motion-banque/. banque/      # banque (dont banque/glace)
cp -r ../../../dyou-assets/motion-medias/DA-M17-EN DA-M17-EN/media         # médias d'une vidéo (voix, logo…)
python3 moteur/outils/sons.py                                              # régénère les bruitages (synthétisés, non suivis)
cd DA-M17-EN && python3 ../moteur/rendu.py apercu 2 8 14 20                # planche d'images, puis :
python3 ../moteur/rendu.py video && python3 ../moteur/outils/mixer.py --lufs -13 renders/image.mp4
python3 ../moteur/outils/verifier.py video/DA-M17-EN.mp4 2 8 14 20
```

Une vidéo existante se refait sans clé : `voix.mp3` est dans ses médias, `timing.json` dans son dossier de code. Pour une **nouvelle voix**, il
faut la clé ElevenLabs (`~/.config/dyou/elevenlabs.json`, jamais dans GitHub) : la demander à Youssef, ou générer la voix
Tomy ailleurs et poser `media/voix.mp3` + l'horodatage des mots. Une tablette seule ne fait pas tourner Python + Skia :
il faut une machine (Claude Code dans le cloud, VPS) ; la tablette ne sert qu'à piloter et regarder.

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
