# Point d'entrée pour Claude — vidéos DYOU et ChinaBook

Ce dépôt contient une bibliothèque de 50 vidéos à produire. Commencer par `video-factory/manifest.json` : chaque ID pointe vers un dossier `videos/ID/` qui associe sans ambiguïté la voix off (`script.txt`), les scènes et prompts (`brief.json`), les images numérotées, le futur MP3 et le futur MP4.

## Contrat de montage

1. Choisir un ID du manifeste. Lire le script et le brief du même dossier. Ne jamais mélanger des images de deux IDs.
2. Lire `availability.json` pour savoir quelles images sont réellement déposées. Un chemin du manifeste ou du brief peut être prévu mais encore absent.
3. Quand l'audio ElevenLabs est disponible, le ranger sous `videos/ID/audio/ID.mp3`. Mesurer sa durée réelle et caler les animations sur les phrases et les accents de cette voix. Exporter `videos/ID/video/ID.mp4` en 1080 × 1920.
4. Varier le fond d'une vidéo à l'autre et à l'intérieur d'une même vidéo : `outils/theme.py` donne cinq thèmes (nuit, encre, sable, acier, braise) avec leur palette et leur texture. Ne jamais écrire une couleur en dur. Typographie sans large espacement, preuves réelles en mockup et photos distinctes. Contrôler les marges et le cadrage 9:16, en particulier le dernier CTA. Bruitages courts sur les apparitions et transitions, sans musique de fond.
5. Les images générées n'ont ni texte ni marque. Ajouter le logo DYOU original et les vraies captures en montage. La navigation POLYRA est disponible dans `videos/RES-01/captures/POLYRA-navigation-reference-720p.mp4` (copie légère de la capture réelle). Ne pas inventer des prix, témoignages, captures WeChat ou preuves commerciales.

## Prix à l'écran

Le prix cher affiché est celui de dropandyou, relu dans `full11_source.json`. Le prix fournisseur ne s'écrit que s'il figure dans `donnees/prix-chinabook.csv`, rempli à la main ; sinon le montage affiche la case « RÉSERVÉ » et renvoie au commentaire. Ne pas parler des produits bon marché (sous 60 €) : l'écart de prix ne se voit pas.

## Produits à l'image

Les produits viennent de la banque DROP&YOU, détourés par `outils/detourer.py`. Celui-ci rejette de lui-même une photo au fond non uni ou dont le détourage mange de la matière — il y a 2 035 produits, on en prend un autre plutôt que de rafistoler.

## Angles ChinaBook

Les vingt scripts se répartissent en cinq familles, marquées par `famille` dans chaque `brief.json` : `prix` (le même objet, deux prix), `voyage` (pas besoin d'aller en Chine), `intermediaire` (la marge du revendeur français), `rentable` (ce que ça te rapporte), `reseau` (le carnet, la confiance, le tri). Varier les familles dans le calendrier de publication.

Statut au 3 octobre 2026 : 50 scripts et prompts complets, 39 premières images de scènes disponibles ; images restantes en cours de génération ; MP3 des nouveaux scripts et MP4 finals non fournis. Ne pas considérer les trois chemins `images/` prévus comme trois images déjà disponibles.
