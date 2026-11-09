"""VX-M02-pub — le montage de VX-M02 remonté sur les mots de Tomy (30/10/2026).

Même image, mais chaque coupe tombe sur un mot de la prise complète de Tomy (voix-ads), d'un seul tenant :
poser la voix B sur le montage fait pour la voix A laissait soit des trous, soit la voix en avance sur l'image.
Seuls les repères changent (mots du script pub), les scènes sont celles de VX-M02/scenes.py.


v6 (31/10/2026, Youssef : « pas besoin de 3D, t'as déjà le mixeur propre ») : le produit = les clips Flow sur NOIR PUR
(clip-rotation, clip-vortex, clip-dessus — vrai couvercle, vrai bec), la montagne de la bannière seulement sur le résultat
(c2), le démontage (c3) et la fin (c1 puis c7). Zéro main IA (c4/c5/c6 écartés). Textes posés ici, voix seule.
v4 (31/10/2026) : UN SEUL PLAN CONTINU en vraie 3D (~/vorix-3d, Three.js, export d'images → videos/scene3d.mp4) : le shaker
sur fond noir qui tourne, se remplit, mélange, se démonte et se remonte, calé sur la voix ; les textes sont posés ici.
v3 (31/10/2026) : Mikail ne veut PLUS ses rushes (« faits à l'arrache, ça fait pas pub »). Chaque plan réel est
remplacé par un clip Grok Imagine (images clés ChatGPT, VX-M03/media/images/k1..k7) : c1 héros montagne, c2 vortex,
c3 éclaté, c4 l'eau, c5 le bouton, c6 le rinçage, c7 plan large. Les explications restent en motion sur noir.
Hook plein cadre sur son plan le plus fort (le vortex, couvercle ouvert, pas une goutte dehors), puis
le reste en cartes de verre fumé (moteur/glace.py), une idée par seconde, pills pour les caractéristiques,
signature VORIX à la fin. Voix A (montage) : le gars cagoulé, ton vlog. Voix B : Tomy, version pub —
mixée ensuite sur la même image.

Chaque coupe tombe sur un mot de timing.json (TW).
"""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
from kit import *
from studio import *
from glace import *
appliquer()
from agence import SousTitresFins

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 2.1, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

# repères : un mot par coupe, cherchés par leur texte (le script peut changer, pas le montage)
import unicodedata
def _n(x): return "".join(ch for ch in unicodedata.normalize("NFD", x.lower()) if ch.isalnum())
def trouve(mot, apres=-1.0):
    for m in K.mots:
        if m["t0"] > apres and _n(m["w"]) == _n(mot): return m["t0"]
    raise KeyError(mot)
T_GOUTTE, T_SORT, T_CEST, T_VORIX = trouve("pas"), trouve("dehors"), trouve("voilà"), trouve("vorix")
T_MOTEUR, T_BASE = trouve("moteur", T_CEST), trouve("base", T_CEST)
T_EAU, T_POUDRE, T_APPUIE, T_MELANGE = trouve("eau"), trouve("poudre"), trouve("bouton"), trouve("mélange")
T_ZERO = trouve("pas", T_MELANGE); T_CINQ, T_BATT, T_MAIN = trouve("cinq"), trouve("recharge"), trouve("tient")
T_LAVER, T_DEMONTE = trouve("pour"), trouve("démonte"); T_EAU2 = trouve("l'eau", T_DEMONTE)
T_DEPUIS = trouve("le", T_EAU2); T_REGLE = T_DEPUIS - 0.4          # « Le shaker qui bosse à ta place. »
FIN_VOIX = K.mots[-1]["t1"]
T_SIGN = trouve("vorix", T_DEPUIS) - 0.15                          # le logo tombe sur le « VORIX » final
T_A2, T_A3 = T_CEST * 2.9 / 4.33, T_CEST * 3.6 / 4.33                # les trois angles du hook, à l'échelle de la phrase

BLANC = "#FFFFFF"
def fond_neutre(c, t, pulse=0.0):
    """fond noir neutre à nappe grise (Youssef, 30/10 : aucun bleu ni violet sur un projet client) — remplace fond_glace"""
    c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000"))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.42), W * 0.95 * (1 + 0.06 * pulse),
                                               [hexa("#262B32", 0.95 + 0.05 * pulse), hexa("#101316", 0.6), hexa("#000000", 0.0)], [0.0, 0.45, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


import glace as _gl; _gl.BLEU = "#C9D3DC"   # lueur des cadres en verre : blanche, plus bleue
GLACE = "#DCE6F0"   # plus de bleu ni de violet (Youssef, 30/10) : blanc glace
ST = SousTitresFins(K, y=1410, larg=640, taille=46, fam="gras", max_mots=4, cx=500)

# sons et bascules
# aucun bruitage (Youssef, 30/10 : « supprime tous les bruits des animations ») ; les coupes se font en silence
for t0 in (T_CEST, T_EAU, T_POUDRE, T_APPUIE, T_MELANGE, T_ZERO, T_CINQ, T_LAVER, T_EAU2, T_DEPUIS, T_SIGN):
    rapide(t0 - 0.05, t0 + 0.08)
rapide(T_A2 - 0.05, T_A2 + 0.08); rapide(T_A3 - 0.05, T_A3 + 0.08)
JAUNE, IW, IH = "#FFD400", 1024, 1536


# ─────────────────────────────────────────── briques
def rush(c, nom, t_local, z=1.0, dx=0.0, dy=0.0, alpha=1.0):
    """un rush BRUT plein cadre (Youssef, 30/10 : plus de détourage, plus de cadre — la vraie vidéo, tout l'écran)"""
    c.save(); c.translate(W / 2 + dx, H / 2 + dy); c.scale(z, z); c.translate(-W / 2, -H / 2)
    video(c, nom, 0, 0, W, H, t_local, alpha=alpha)
    c.restore()


def plan(c, nom, t_local, z=1.0, dx=0.0, dy=0.0, alpha=1.0):
    """un clip Grok 2:3 recadré « cover » plein cadre 9:16 ; zoom par la matrice (un seul cache 1080×1920 par clip)"""
    c.save(); c.translate(W / 2 + dx, H / 2 + dy); c.scale(z, z); c.translate(-W / 2, -H / 2)
    video(c, nom, 0, 0, W, H, t_local, boucle=False, alpha=alpha)
    c.restore()


def zoom(t, t0, t1, z0, z1): return mix(z0, z1, borne((t - t0) / max(0.01, t1 - t0)))


def clip(c, nom, t, t0, s=0.74, dy=-228, alpha=1.0):
    """un clip Flow 9:16 (fond noir) posé sur le noir, réduit pour laisser la place aux textes"""
    w, h = W * s, H * s
    video(c, nom, W / 2 - w / 2, H / 2 - h / 2 + dy, w, h, t - t0, boucle=False, alpha=alpha)


def packshot(c, nom, t, t0, t1, s0, s1, dy0=0.0, dy1=0.0, dx=0.0, alpha=1.0):
    u = borne((t - t0) / max(0.01, t1 - t0))
    sc, dy = mix(s0, s1, u), mix(dy0, dy1, u)
    w, h = IW * sc, IH * sc
    image(c, nom, W / 2 - w / 2 + dx, H / 2 - h / 2 + dy, w, alpha=alpha)


def voile_bas(c, a=0.62):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, H * 0.62), skia.Point(0, H)], [hexa("#000000", 0.0), hexa("#000000", a)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


def titre(c, s, t, t0, y, taille=112, fin=None, accent=1, larg=760):
    """un bloc de titre centré qui monte d'un bloc ; `accent` derniers mots en italique jaune"""
    taille = ajuste(s, larg, taille, "noir", -0.02)
    a = 1.0 if fin is None else 1 - prog(t, fin, 0.25, entree)
    if a <= 0.01: return
    mots = s.split(" ")
    if accent <= 0 or accent >= len(mots):
        lettres(c, s, 500, y, taille, t, t0, "masque", fam="noir", couleur=BLANC, grad=False, decal=0.0, duree=0.38, track=-0.02, alpha=a); return
    A, B = " ".join(mots[:-accent]), " ".join(mots[-accent:])
    esp = largeur("N N", taille, "noir", -0.02) - largeur("NN", taille, "noir", -0.02)
    wa, wb = largeur(A, taille, "noir", -0.02) + esp, largeur(B, taille, "noir", -0.02)
    x0 = 500 - (wa + wb) / 2
    lettres(c, A, x0, y, taille, t, t0, "masque", fam="noir", couleur=BLANC, grad=False, decal=0.0, duree=0.38, track=-0.02, alpha=a, align="gauche")
    hl = hauteurLigne(taille, "noir")
    c.save(); c.translate(x0 + wa, y + hl * 0.78); c.skew(-0.2, 0); c.translate(-(x0 + wa), -(y + hl * 0.78))
    lettres(c, B, x0 + wa, y, taille, t, t0, "masque", fam="noir", couleur=JAUNE, grad=False, decal=0.0, duree=0.38, track=-0.02, alpha=a, align="gauche")
    c.restore()


def pill(c, lab, t, t0, x, y, fin=None):
    if t < t0 - 0.05: return
    a = prog(t, t0, 0.5, lambda u: ressort(u, 1.2, 5.0)) * (1.0 if fin is None else 1 - prog(t, fin, 0.25, entree))
    if a <= 0.01: return
    w = largeur(lab, 34, "fort", -0.01) + 51
    pill_g(c, lab, x + w / 2 + 120 * (1 - a), y, 34, "doux", alpha=a, s=mix(0.85, 1.0, a))


def noir(c, t, t0, d=0.12):
    """un passage au noir sur la coupe : noir à t0, puis l'image suivante revient en d secondes"""
    v = prog(t, t0 - d, d) * (1 - prog(t, t0, d))
    if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000", v))


# ─────────────────────────────────────────── scènes : produit sur noir (Flow) ↔ montagne (Grok)
ZP, DYP = 0.80, -170          # cadrage du produit plein pied : la base finit vers y 1525, les titres passent dessous (y 1560)


def hook(c, t):
    """« Couvercle ouvert, moteur à fond, et pas une goutte dehors. » — le vortex vu de dessus, puis fermé de face"""
    if t >= T_CEST + 0.15: return
    if t < T_GOUTTE: plan(c, "videos/clip-dessus", t + 0.3, z=zoom(t, 0.0, T_GOUTTE, 1.0, 1.07))
    else: plan(c, "videos/clip-vortex", t - T_GOUTTE + 2.0, z=zoom(t, T_GOUTTE, T_CEST, 0.92, 0.96), dy=-70)
    titre(c, "PAS UNE GOUTTE.", t, T_GOUTTE, 1560, 112, fin=T_CEST - 0.05, accent=2)
    noir(c, t, T_CEST)


def presentation(c, t):
    """« Voilà le VORIX : un vrai moteur dans la base. » — le produit fait un tour sur lui-même, sur noir"""
    if t < T_CEST - 0.05 or t > T_EAU + 0.05: return
    plan(c, "videos/clip-rotation", t - T_CEST, z=ZP, dy=DYP)
    titre(c, "VORIX.", t, T_VORIX, 1560, 140, fin=T_MOTEUR + 0.3, accent=0)
    pill(c, "UN MOTEUR DANS LA BASE", t, T_BASE, 500 - (largeur("UN MOTEUR DANS LA BASE", 34, "fort", -0.01) + 51) / 2, 1560, fin=T_EAU - 0.1)


def demo(c, t):
    """« Ton eau, ta poudre, un bouton, et il mélange tout ça tout seul. » — le vortex de face ; au mot « bouton », gros plan sur le bouton"""
    if t < T_EAU - 0.05 or t > T_ZERO + 0.1: return
    if t < T_APPUIE: plan(c, "videos/clip-vortex", t - T_EAU + 0.2, z=ZP, dy=DYP)
    elif t < T_MELANGE: plan(c, "videos/clip-vortex", t - T_EAU + 0.2, z=1.5, dy=-1250)          # le bouton et sa LED
    else: plan(c, "videos/clip-vortex", t - T_EAU + 0.2, z=zoom(t, T_MELANGE, T_ZERO, ZP, ZP + 0.04), dy=DYP)
    titre(c, "TON EAU.", t, T_EAU, 1560, 112, fin=T_POUDRE - 0.28, accent=0)
    titre(c, "TA POUDRE.", t, T_POUDRE, 1560, 112, fin=T_APPUIE - 0.28, accent=0)
    titre(c, "UN BOUTON.", t, T_APPUIE, 1560, 112, fin=T_MELANGE - 0.03, accent=1)
    noir(c, t, T_ZERO)


def resultat(c, t):
    """« Pas un grumeau, et fini de secouer ton shaker dans tous les sens. » — la montagne : le vortex en macro"""
    if t < T_ZERO - 0.05 or t > T_CINQ + 0.05: return
    plan(c, "videos/c2", t - T_ZERO + 2.0, z=zoom(t, T_ZERO, T_CINQ, 1.0, 1.08))
    voile_bas(c)
    titre(c, "PAS UN GRUMEAU.", t, T_ZERO + 0.05, 1600, 112, fin=T_CINQ - 0.05)
    noir(c, t, T_CINQ)


def specs(c, t):
    """« Il fait cinq cents millilitres, il se recharge, et il tient dans la main. » — trois quarts sur noir, pastilles à droite"""
    if t < T_CINQ - 0.05 or t > T_LAVER + 0.05: return
    a = 1 - prog(t, T_LAVER - 0.12, 0.12, entree)
    plan(c, "videos/clip-rotation", t - T_CINQ + 5.1, z=ZP, dx=-175, dy=DYP, alpha=a)   # 5,1 → 7,9 s : du trois-quarts dos à la face, le clip finit pile sur la coupe
    with Calque(c, a):
        pill(c, "500 ML", t, T_CINQ, 640, 700)
        pill(c, "RECHARGEABLE", t, T_BATT, 640, 820)
        pill(c, "TIENT DANS LA MAIN", t, T_MAIN, 640, 940)


def lavage(c, t):
    """« Pour le laver, tout se démonte et ça passe sous l'eau. » — la montagne : les trois pièces sur le rocher"""
    if t < T_LAVER - 0.05 or t > T_DEPUIS + 0.05: return
    plan(c, "videos/c3", t - T_LAVER + 0.4, z=zoom(t, T_LAVER, T_DEPUIS, 1.0, 1.06))
    voile_bas(c, 0.66)
    titre(c, "TOUT SE DÉMONTE.", t, T_DEMONTE, 1600, 100, fin=T_DEPUIS - 0.05, accent=1)
    noir(c, t, T_DEPUIS)


def signature(c, t):
    """« Le shaker qui bosse à ta place. VORIX. » — le héros dans la montagne, puis le plan large et la marque dans le ciel"""
    if t < T_DEPUIS - 0.05: return
    if t < T_SIGN: plan(c, "videos/c1", t - T_DEPUIS + 1.0, z=zoom(t, T_DEPUIS, T_SIGN, 1.0, 1.05))
    else:
        plan(c, "videos/c7", t - T_SIGN, z=zoom(t, T_SIGN, DUREE, 1.0, 1.03))
        titre(c, "VORIX", t, T_SIGN + 0.3, 560, 150, accent=0)
        a2 = prog(t, T_SIGN + 0.3, 0.38)
        if a2 > 0: texte(c, "TRAIN.  FUEL.  PERFORM.", 500 + 0.34 * 30 / 2, 770, 30, GLACE, "noir", align="centre", track=0.34, alpha=a2 * 0.9)
    v = prog(t, DUREE - 0.5, 0.5)
    if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000", v))


def dessine(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000"))
    hook(c, t); presentation(c, t); demo(c, t); resultat(c, t); specs(c, t); lavage(c, t); signature(c, t)
    if (T_MELANGE + 0.1 <= t < T_ZERO - 0.1) or (T_LAVER + 0.1 <= t < T_DEMONTE - 0.05) or (T_DEPUIS + 0.1 <= t < T_SIGN - 0.1):
        ST.dessine(c, t)
