# VX-M03 — refonte VORIX après retour client du 30/10 23 h (vocaux transcrits)

Mikail : ses rushes étaient « faits à l'arrache, juste pour aider » → il ne veut PLUS ses vidéos dans le montage.
IA acceptée si « bien fait, réaliste », pas étiqueté IA par Instagram.
Il veut : 1) une bande-annonce sombre, dans la montagne de sa bannière, le shaker qui passe « comme les pubs », sans voix ;
2) une présentation : caractéristiques + mode d'emploi (voix Tomy conservée).
Référence envoyée par Youssef : « Pub IA cinématique pour produit | BOGA AI STUDIO » (YouTube short).

## Chaîne
photos/packshots → ChatGPT (images clés, ambiance bannière) → Seedance 2.5 image-to-video (API Higgsfield,
`bytedance/seedance-2.5/image-to-video` : prompt, image_url, duration 4-30, resolution 480p/720p/1080p,
end_image_url, generate_audio) → montage Skia (titres blancs + accent jaune, zéro bruitage).

## Images clés (ChatGPT, 2:3)
K1 héros montagne : shaker fermé sur rocher humide, crête + brume, faisceau blanc, tiers haut vide.
K2 vortex macro : gros plan, shake chocolat en tourbillon, gouttes sur la paroi, montagne floue.
K3 éclaté : couvercle / gobelet / base posés sur le rocher, gouttes.
K4 geste 1 : main qui verse de l'eau dans le gobelet ouvert, plan de travail sombre (présentation).
K5 geste 2 : pouce sur le bouton de la base, LED, vortex qui démarre.
K6 rinçage : pièces sous le filet d'eau du robinet.
K7 signature : plan large montagne, shaker petit au centre, beaucoup de noir en haut pour « VORIX ».

## Clips Seedance (8 s, 720p, sans audio)
C1 K1 : caméra orbite lente autour du produit, brume qui glisse, gouttes qui tombent. (bande-annonce ouverture)
C2 K2 : vortex qui tourne, caméra fixe légère poussée.
C3 K3 : caméra glisse latéralement sur les pièces, lumière qui balaie.
C4 K4 : l'eau coule, puis une dosette de poudre tombe (présentation « tu verses »).
C5 K5 : le pouce appuie, LED s'allume, le liquide se met à tourner (« tu appuies »).
C6 K6 : l'eau coule sur les pièces, éclaboussures (« passe sous l'eau »).
C7 K7 : push-in lent, brume. (signature)
