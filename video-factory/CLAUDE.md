# Point d'entrée pour Claude — vidéos DYOU et ChinaBook

Ce dépôt contient une bibliothèque de 50 vidéos à produire. Commencer par `video-factory/manifest.json` : chaque ID pointe vers un dossier `videos/ID/` qui associe sans ambiguïté la voix off (`script.txt`), les scènes et prompts (`brief.json`), les images numérotées, le futur MP3 et le futur MP4.

## Contrat de montage

1. Choisir un ID du manifeste. Lire le script et le brief du même dossier. Ne jamais mélanger des images de deux IDs.
2. Lire `availability.json` pour savoir quelles images sont réellement déposées. Un chemin du manifeste ou du brief peut être prévu mais encore absent.
3. Les voix se génèrent ici, **une par une et à la demande** : `outils/voix.py --un ID`. Ne pas lancer `--tout` : un script peut encore changer, et une voix regénérée est du crédit perdu (clé dans `~/.config/dyou/elevenlabs.json`, voix Tomy, modèle `eleven_v4`, offre Starter : 30 000 crédits par mois et licence commerciale). Garder la prise brute en `ID-brut.mp3`, accélérer à `atempo=1.12`, puis ranger le résultat sous `videos/ID/audio/ID.mp3`. Mesurer les respirations (`silencedetect=noise=-30dB:d=0.12`, sans `-v error` qui les masque) et donner à chaque plan la phrase qu'il porte. Dans `montage_CB02.py`, `PLANS` porte la durée réelle **et** la durée d'écriture de chaque plan : le temps est étiré entre les deux, donc une nouvelle prise de voix se recale sans réécrire les animations, et `mixer_sons.py` lit ces bornes au lieu de les recopier. Exporter `videos/ID/video/ID.mp4` en 1080 × 1920.
4. Varier le fond d'une vidéo à l'autre et à l'intérieur d'une même vidéo : `outils/theme.py` donne cinq thèmes (nuit, encre, sable, acier, braise) avec leur palette et leur texture. Ne jamais écrire une couleur en dur. Typographie sans large espacement, preuves réelles en mockup et photos distinctes. Contrôler les marges et le cadrage 9:16, en particulier le dernier CTA. Bruitages courts sur les apparitions et transitions, sans musique de fond.
5. Les images générées n'ont ni texte ni marque. Ajouter le logo DYOU original et les vraies captures en montage. La navigation POLYRA est disponible dans `videos/RES-01/captures/POLYRA-navigation-reference-720p.mp4` (copie légère de la capture réelle). Ne pas inventer des prix, témoignages, captures WeChat ou preuves commerciales.

## Prix à l'écran

Le prix cher affiché est celui de dropandyou, relu dans `full11_source.json`. Le prix fournisseur ne s'écrit que s'il figure dans `donnees/prix-chinabook.csv`, rempli à la main ; sinon le montage affiche la case « RÉSERVÉ » et renvoie au commentaire. Ne pas parler des produits bon marché (sous 60 €) : l'écart de prix ne se voit pas.

## Produits à l'image

Les 150 images générées servent au décor et à la scène. **Dès qu'un produit est montré, il vient de la banque DROP&YOU**, détouré par `outils/detourer.py` — plus jamais une photo de produit générique qui n'a rien à voir avec ce qui est réellement vendu. Le détoureur rejette de lui-même une photo au fond non uni ou dont le détourage mange de la matière : il y a 2 035 produits, on en prend un autre plutôt que de rafistoler.

## Angles ChinaBook

Les vingt scripts se répartissent en cinq familles, marquées par `famille` dans chaque `brief.json` : `prix` (le même objet, deux prix), `voyage` (pas besoin d'aller en Chine), `intermediaire` (la marge du revendeur français), `rentable` (ce que ça te rapporte), `reseau` (le carnet, la confiance, le tri). Varier les familles dans le calendrier de publication.

## Répartition du travail

ChatGPT fournit les scripts de départ et les images de scène. **Le motion et les voix sont faits ici** : scripts réécrits quand l'angle ne porte pas, montage, bruitages, encodage.

Statut au 4 octobre 2026 : 50 scripts et prompts complets, 143 images de scène disponibles ; les sept `01.webp` de CB-01, CB-02, CB-03, CB-05, CB-07, CB-09 et CB-10 ont été retirées (personnage cagoulé non demandé) et restent à régénérer, logo DYOU et capture POLYRA de référence. `availability.json` expose le statut par ID et doit refléter le disque, pas l'intention : un `status: ready` sur un fichier absent fait planter un montage. Vidéos montées : RES-01, CB-02, CB-08.

## Motion design

Depuis le 5 octobre 2026 : moteur Python + Skia dans `motion/CB-M01/` (premier projet complet, voir son `LISEZ-MOI.md` et `DECOUPAGE.md`). Ressources GitHub vérifiées (licences, maintenance) et pièges de Higgsedit dans `motion-ressources/README.md`. Avant de livrer, vérifier des images extraites **du MP4 final**, pas seulement les aperçus : le rendu Higgsedit a déjà changé de police entre les deux.
