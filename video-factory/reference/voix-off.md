# Vidéos voix off sur rushes — format validé (DY-M08, 16/10/2026)

Youssef : « C'était parfait. » Il enverra d'autres rushes (POV, marchandise, personnages qui font quelque chose sans parler) :
on écrit une voix off qui raconte, plutôt que de faire parler une IA. **Toute nouvelle vidéo de ce type part de `motion/DY-M08/`.**

## Ce qu'il envoie, ce qu'on fait

1. **Recoller** si la vidéo arrive en plusieurs morceaux (limite 30 Mo) : `ffmpeg -f concat`, puis 1080×1920, 30 i/s → `media/source.mp4`.
2. **Découper en plans** : repérer chaque changement de plan et ce qu'on y voit (planche d'images toutes les 0,5 s). Noter
   `COUPES` et les 3-4 changements de chapitre (`FLASH`).
3. **Écrire le texte plan par plan** : une phrase = un plan, elle parle de ce qu'on voit à ce moment-là.
   - Hook dans les 3 premières secondes sur l'image la plus forte (argent, produit, lieu), puis la promesse « reste / enregistre, je t'explique ».
   - Récit à la première personne, tutoiement, ton vlog entraînant, phrases courtes.
   - Offre concrète sur les plans marchandise (à l'unité / en lot, les fournisseurs).
   - Fin : appel au commentaire (« Dis-moi en commentaire ce que tu cherches »), puis logo + « Enregistre la vidéo ».
   - Vocabulaire maison : jamais « usine » (voir `A-LIRE.md`) ; « Drop and You » à l'oral, DROP&YOU à l'écran.
4. **`segments.json`** : `[début, fin visée, texte]` par phrase, calé sur les coupes (petit blanc de 0,1-0,3 s avant chaque coupe).
5. **Voix** : `voix_segments.py` (Léo `jsScnYkNNda9Q1NES5nn`, une prise par phrase, horodatée, jamais régénérée sans `--forcer`)
   puis `assembler_voix.py` (pose chaque phrase à son début, accélère au plus ×1,2 si elle déborde) → `voix/voix.wav` + `mots.json`.
   **Débit naturel, pas le 4,2 mots/s du motion** : c'est l'image qui donne le rythme. Si une phrase dépasse encore, on la raccourcit.
6. **Habillage** (`montage.py`, base `moteur/edit.py`) :
   - sous-titres fins centrés, mot dit en jaune ;
   - pastilles sur les mots forts, **jamais sur un visage** (sous le menton, y ≈ 1090) ;
   - logo au moment où la marque est prononcée ;
   - flash blanc + coup de zoom **seulement** aux changements de chapitre, petits zooms sur les mots forts, bruitages discrets.
   Pas plus : la vidéo tournée reste la star.
7. **Son** : `montage.py son` → −13 LUFS / −1 dB. **Pas de musique générée** (il la met dans CapCut) : `--sans-musique`.
   Une musique déjà payée peut être reprise de `motion/banque/musiques/`.
8. **Vérifier** le MP4 final (planche d'images + mesure du son), envoyer une copie allégée si > 30 Mo, l'original reste dans `video/`.

## Pièges rencontrés

- Échantillons numpy en float64 écrits comme du f32 → bruit ; toujours `astype(np.float32)` avant `tobytes()`.
- whisper peut « entendre » une phrase dans une musique instrumentale : réécouter avant de conclure qu'elle chante.
