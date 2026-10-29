# Trouver et découper des archives — format ARCHIVES de @recto_cerveau (30/10/2026)

Youssef, 30/10 : « moins de motion, plus de vidéo et photo brut, donc le gros du travail tu dois
le faire sur récupérer les bons passages de vidéo — car ce format qu'on propose ne fonctionne pas
jusqu'à preuve du contraire. » Le motion design (bonhomme, pièce 3D) n'est plus la base.

## Où sont les archives

**archive.org est la source principale.** YouTube est bloqué sur ce Mac (« The page needs to be
reloaded » sur tous les clients yt-dlp, vérifié le 30/10) — ne pas perdre de temps dessus.

Chercher un sujet :

    curl -s -G "https://archive.org/advancedsearch.php" \
      --data-urlencode 'q=(mon sujet) AND mediatype:movies' \
      --data-urlencode 'fl[]=identifier' --data-urlencode 'fl[]=title' \
      --data-urlencode 'fl[]=downloads' --data-urlencode 'rows=20' \
      --data-urlencode 'sort[]=downloads desc' --data-urlencode 'output=json'

Puis `https://archive.org/metadata/<identifier>` donne la liste des fichiers, leur taille, leur
durée et leurs dimensions. **Attention** : `and[]=mediatype:movies` est refusé par l'API, il faut
mettre le filtre dans `q`. Et l'identifiant complet se trouve par `identifier:debut*`.

Trouvé le 30/10 et à garder : **`OJ_Simpson_Trial_Compilation`** — le procès O.J. Simpson en
entier, jour par jour, **492 fichiers, 195 Go, 480p**, verdict du 3 octobre compris. Et
**`abc-2020-and-special-report-coverage-of-oj-simpson-bronco-chase-6171994`** pour la
course-poursuite du 17 juin 1994 (320×240, c'est de la télé de 1994).

## Ne jamais télécharger le fichier entier

Un fichier d'archive fait 500 à 800 Mo et le disque du Mac est plein à 97 %. ffmpeg sait **chercher
dans un fichier distant** par requêtes de plage HTTP : `-ss` AVANT `-i` sur l'URL. Une image prise
à 1 h 40 dans un fichier de 510 Mo coûte ~10 s et quelques centaines de Ko.

`moteur/outils/scan_archive.sh` balaye un fichier distant et sort une planche-contact :

    bash ../moteur/outils/scan_archive.sh "<URL>" planche 0 7000 500    # large
    bash ../moteur/outils/scan_archive.sh "<URL>" planche 5900 7000 90  # resserré

On balaye large, on repère le moment, on resserre deux fois. C'est **ça**, le gros du travail.

## Découper un passage en vertical

Deux traitements, et le choix se fait au plan :

- **Plein cadre** quand le sujet est un GROS PLAN (un visage, un objet tenu en main). On prend une
  tranche verticale de la source 4:3 : `crop=205:362:<x>:0` puis `scale=1080:1920`. C'est ~5× de
  grossissement, c'est doux — @darkearth fait exactement ça et c'est passé à 2,7 M de vues.
- **Pleine largeur nette + fond flou** quand le plan est LARGE (une salle, une autoroute). L'image
  reste nette sur toute sa largeur, le reste du cadre est le même plan flouté et assombri.

**Toujours couper l'incrustation.** Les archives du procès portent un timecode « conus video
#356857 » à **76-82 % de hauteur** : `crop=640:362:0:0` l'enlève (et pas un rognage par le bas,
l'incrustation n'est pas tout en bas). Les archives de télé portent des bandeaux de chaîne.

## Monter

L'ffmpeg de ce Mac **n'a ni `drawtext` ni `subtitles`** (pas de libass) : aucun texte ne peut être
écrit par ffmpeg. Les sous-titres se rendent avec Skia en PNG transparents puis se superposent :

    /usr/bin/python3 ../moteur/outils/soustitres_png.py --duree 70 --fps 20 --y 1330 \
        --censure "34:m*rt"
    ffmpeg -i renders/fond.mp4 -framerate 20 -i texte/t%05d.png -ss 0 -t 70 -i media/voix.mp3 \
      -filter_complex "[1:v]fps=30,format=rgba[txt];[0:v][txt]overlay=0:0,format=yuv420p[v]" \
      -map "[v]" -map 2:a -c:v libx264 -crf 19 -c:a aac -b:a 192k -shortest -y video/X.mp4

Ne PAS faire passer l'archive dans le moteur Skia : `prepare_video` extrait chaque image en JPEG,
soit ~1 Go de cache pour 70 s. Le disque ne le supporte pas.

Style repris de la référence : **un seul mot à l'écran à la fois**, capitales blanches, ombre
portée, et rien d'autre. Les mots sensibles se censurent à l'affichage (`--censure`), pas à la voix.
