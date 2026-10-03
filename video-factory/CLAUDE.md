# Point d'entrée pour Claude — vidéos DYOU et ChinaBook

Ce dépôt contient une bibliothèque de 50 vidéos à produire. Commencer par `video-factory/manifest.json` : chaque ID pointe vers un dossier `videos/ID/` qui associe sans ambiguïté la voix off (`script.txt`), les scènes et prompts (`brief.json`), les images numérotées, le futur MP3 et le futur MP4.

## Contrat de montage

1. Choisir un ID du manifeste. Lire le script et le brief du même dossier. Ne jamais mélanger des images de deux IDs.
2. Lire `availability.json` pour savoir quelles images sont réellement déposées. Un chemin du manifeste ou du brief peut être prévu mais encore absent.
3. Quand l'audio ElevenLabs est disponible, le ranger sous `videos/ID/audio/ID.mp3`. Mesurer sa durée réelle et caler les animations sur les phrases et les accents de cette voix. Exporter `videos/ID/video/ID.mp4` en 1080 × 1920.
4. Alterner cartes graphiques noir/violet, typographie sans large espacement, preuves réelles en mockup et photos distinctes. Contrôler les marges et le cadrage 9:16, en particulier le dernier CTA. Bruitages courts sur les apparitions et transitions, sans musique de fond.
5. Les images générées n'ont ni texte ni marque. Ajouter le logo DYOU original et les vraies captures en montage. Ne pas inventer des prix, témoignages, captures WeChat ou preuves commerciales.

Statut au 3 octobre 2026 : scripts et prompts complets ; images en cours de génération ; MP3 des nouveaux scripts et MP4 finals non fournis. Ne pas considérer les trois chemins `images/` prévus comme trois images déjà disponibles.
