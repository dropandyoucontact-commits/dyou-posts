# Ligne éditoriale — vidéos Chine et import-export

But : construire une audience autour de la Chine et de l'import-export, **pas vendre à
chaque vidéo**. Youssef, le 5 octobre 2026 : « Il ne faut pas que je vende tout le temps
mon China Book, toutes les vidéos. Sinon, les gens ne vont pas s'abonner. »

## Le discours ChinaBook — la façon de vendre de Youssef

Donné par Youssef le 5 octobre 2026 ; il prime sur tout le reste.

- **Jamais « usine » ni « fabricant ».** Ce n'est pas vrai : ChinaBook ne branche pas les
  gens avec des usines. Ce sont des **fournisseurs à Guangzhou ou à Shenzhen, validés,
  vérifiés, avec qui Youssef travaille lui-même**. Pas de « demande-lui des photos de
  l'usine », pas de « signes que ce n'est pas une usine ».
- **Taper dans le cœur du problème.** « Tu es revendeur, tu vends des sneakers par
  exemple. Tu passes par un Français installé en Chine. Lui prend sa marge : il va voir
  le fournisseur chinois, il prend sa marge, et il t'envoie. Avec le ChinaBook, tu passes
  directement par les fournisseurs chinois : tu leur parles sur WeChat et tu paies sur
  Alipay. »
- **Le process, qu'on peut expliquer en vidéo :**
  1. sur WeChat, tu écris au fournisseur : « je veux deux paires de B30 » ;
  2. il te donne le prix et t'envoie un QR code Alipay ; tu paies ;
  3. il envoie la marchandise **à ton nom** (ou au surnom que tu lui as donné) **chez ton
     transitaire** ;
  4. le transitaire regroupe les colis de tes différents fournisseurs, et tu lui dis sur
     WeChat où part chaque chose : « cette paire et les lunettes, ça va là ; les AirPods
     Max, là ; la montre connectée, ici ».
- **À l'écran** : les conversations se montrent en style WeChat (le site ChinaBook en a
  de vraies captures), avec les logos WeChat et Alipay quand on parle de ces applis ; le
  produit montré correspond à ce que dit la voix (textile → vestes, électronique →
  casque, baskets → vidéos du fournisseur dans un téléphone, accélérées ×2 à ×2,5).
  Lieux à venir dans la banque : la devanture de Kimbo à Guangzhou (où l'on va trouver
  des fournisseurs), la tour SEG Electronics à Shenzhen.

## Sujets

1. **Partir en Chine** : ce qu'il faut faire en arrivant (applications de paiement, de
   transport, de réservation comme Trip.com, carte SIM ou eSIM, accès internet…),
   formalités, où loger quand on vient sourcer.
2. **Les marchés** : quelle ville pour quoi, comment s'y prendre sur place.
3. **Acheter en Chine** : échantillons, quantités minimales, négociation, contrôle
   qualité, paiement, transitaire, douane, délais.
4. **Les erreurs et les arnaques** à éviter.
5. **ChinaBook** : le réseau testé, le contact direct (modèle : `motion/CB-M01`).

Formats qui marchent pour ces sujets : « les 5 / 10 choses à faire », « les erreurs »,
« un marché en 60 secondes », « ce que personne ne te dit ».

## Partir d'un contenu de référence

Quand Youssef envoie une vidéo ou un carrousel TikTok :
1. le décortiquer (texte à l'écran, voix, ordre des idées, accroche) ;
2. lister les affirmations et **vérifier celles qui changent** (visa, applications,
   règles de paiement, douane) à la source officielle, le jour même ;
3. écrire **notre** script : notre accroche, notre ordre, nos mots. On reprend des faits,
   jamais le texte ni les visuels de quelqu'un d'autre.

## Le script

- 45 à 60 s ; à 3,5 mots par seconde, c'est 150 à 210 mots.
- La première phrase accroche (une promesse, une question, un chiffre vérifié).
- Une idée par phrase ; un point de la liste = un plan du motion.
- Aucun prix, délai ou résultat chiffré sans source.
- Voix Tomy, accélérée par `motion/moteur/outils/voix.py`.

## L'appel à l'action — en rotation

Règle de départ, à ajuster selon les chiffres :
- **La plupart des vidéos** : un appel d'audience (« abonne-toi pour la partie 2 »,
  « enregistre-la pour ton voyage », une question en commentaire).
- **Environ une sur trois** : une passerelle douce en dernière phrase, du type « Pas le
  temps ou pas les moyens d'aller en Chine ? Les fournisseurs que j'ai testés sont
  regroupés dans le ChinaBook. Écris-moi CHINA. »
- **De temps en temps** : une vidéo entièrement ChinaBook, comme CB-M01.

## Deux familles de vidéos : organique ou pub (Youssef, 08/10/2026)

Avant d'écrire un script, savoir pour quoi il est fait. Youssef le dit en le demandant.

**Vidéo organique** (pour publier sur le compte, gagner des abonnés) :
- **Appel à l'enregistrement ou au partage dans les 3 premières secondes**, dit par la voix :
  « Enregistre cette vidéo », « Envoie-la à celui qui part avec toi ». Ça fait monter l'algorithme.
- **Une question au public quand on explique quelque chose** : « Dis-moi en commentaire… ».
  Les commentaires comptent autant que les enregistrements.
- **Une boucle ouverte annoncée tôt** (« reste jusqu'au 9… ») pour tenir jusqu'au bout.
- La pub ChinaBook se place **à la fin**, en passerelle : « tu n'as même pas besoin d'y aller,
  on a déjà fait le travail, nos fournisseurs validés sont dans le ChinaBook ».
- Un sujet qui n'a rien à voir avec les produits (voyage, applis, VPN…) se fait en **motion pur**
  (logos, écrans, icônes), sans aller chercher dans la banque de produits. Même voix, même débit.

**Vidéo pub** (motion type CB-M04 / CB-M05 / DY-M01, pour Meta Ads) :
- **Aucun appel aux commentaires, à l'enregistrement ni à l'abonnement** : ça ne sert à rien en pub.
- Seul appel à l'action : WhatsApp (ou le site, qui porte déjà le WhatsApp).

**Signature (Youssef, 08/10/2026)** : toute vidéo ChinaBook, organique ou pub, finit sur le carton
final avec **« proposé par » + le logo DROP&YOU** (`moteur/media/logo-dropandyou.png`), comme DY-M01 v1.

**Remix d'un TikTok d'arnaques ou de conseils** : le discours ChinaBook prime sur la source. Jamais
« usine », jamais « paie seulement sur un compte d'entreprise » (chez nous on paie le fournisseur sur
Alipay) : on reformule en « vrai fournisseur », « moyen de paiement traçable », « il te montre la
marchandise en direct ».

**Remasteriser un TikTok de référence** : on reprend les idées et les faits (vérifiés le jour même),
jamais le texte, la voix ni les visuels. On retire tout ce qui appartient à l'auteur (son nom, son
compte, ses appels à l'action vers lui). Notre accroche, notre ordre, plus dense, plus rapide.

## Le persona et l'accroche (décision de Youssef, 05/10/2026)

Youssef connaît son persona et ne le redéfinit plus : un **revendeur** (sneakers, textile, électronique…)
qui trouve que sa marge est trop faible, qui passe par un intermédiaire (un Français installé en Chine),
et qui craint de perdre du temps et des milliers d'euros à aller sourcer lui-même. Claude sait ce que ce
revendeur veut entendre : ne pas redemander.

**Accroche agressive, une idée, une phrase, dans les 3 premières secondes :**
- le problème dit sans détour (« Tu ne marges pas assez sur tes sneakers ? Normal. Tu bosses pour un
  Français installé en Chine ») ;
- une première image réelle ou choquante (un rush de Youssef, une barre de marge qu'on mange) ;
- la réponse en 2 phrases (ChinaBook = les numéros directs), puis le process, puis l'appel à l'action.

Modèle : `motion/CB-M03` (27,5 s). La structure qui marche : accroche → cause → preuve (« j'y étais »)
→ solution → process (WeChat, Alipay, transitaire) → liberté (détail, unité, gros, à la commande, depuis
la Thaïlande) → « sans y aller, sans perdre des milliers d'euros ni du temps » → « Envoie-moi CHINA ».
