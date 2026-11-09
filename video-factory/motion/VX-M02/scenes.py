"""VX-M02 — VORIX, shaker électrique (client Mikail) — montage unique, deux voix (30/10/2026).

Uniquement la matière du client : ses cinq rushes et ses photos. Aucune 3D, aucune image générée.
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
T_GOUTTE, T_SORT, T_CEST, T_VORIX = trouve("pas"), trouve("sort"), trouve("c'est"), trouve("vorix")
T_MOTEUR, T_BASE = trouve("moteur"), trouve("base")
T_EAU, T_POUDRE, T_APPUIE, T_MELANGE = trouve("eau"), trouve("poudre"), trouve("t'appuies"), trouve("mélange")
T_ZERO = trouve("pas", T_MELANGE); T_CINQ, T_BATT, T_MAIN = trouve("cinq"), trouve("recharge"), trouve("tient")
T_LAVER, T_DEMONTE = trouve("pour"), trouve("démonte"); T_EAU2 = trouve("l'eau", T_DEMONTE)
T_DEPUIS = trouve("depuis"); T_REGLE = T_DEPUIS - 0.4
FIN_VOIX = K.mots[-1]["t1"]
T_SIGN = FIN_VOIX - 0.25

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
for t0 in (T_CEST, T_MOTEUR, T_EAU, T_POUDRE, T_APPUIE, T_ZERO, T_CINQ, T_LAVER, T_EAU2, T_DEPUIS):
    rapide(t0 - 0.06, t0 + 0.10); eclair(t0, GLACE, 0.09)           # plus de bruit de transition (règle du 30/10/2026)
rapide(2.84, 2.99); rapide(3.54, 3.69); son(T_APPUIE + 0.1, "clic", -8)
for t0 in (T_CINQ, T_BATT, T_MAIN): son(t0, "pop", -8)   # le petit bruit discret sur chaque bénéfice, rien d'autre
son(T_SIGN + 0.5, "ding", -8)


# ─────────────────────────────────────────── briques
def rush(c, nom, t_local, z=1.0, dx=0.0, dy=0.0, alpha=1.0):
    """un rush plein cadre, zoomé par le canevas (le cache reste en 1080×1920, une seule extraction)"""
    c.save(); c.translate(W / 2 + dx, H / 2 + dy); c.scale(z, z); c.translate(-W / 2, -H / 2)
    video(c, nom, 0, 0, W, H, t_local, alpha=alpha)
    c.restore()


def carte_rush(c, nom, t_local, cx, cy, w, h, t, alpha=1.0, s=1.0, z=1.0, dx=0.0, dy=0.0, r=42):
    """un rush dans un cadre de verre fumé, cadré en « cover », avec son reflet qui passe"""
    if alpha <= 0.01 or s <= 0.01: return
    w2, h2 = w * s, h * s
    x, y = cx - w2 / 2, cy - h2 / 2
    with Calque(c, alpha):
        verre(c, x, y, w2, h2, r, 1.0, lueur=1.1)
        m = 10 * s
        iw, ih = w2 - 2 * m, h2 - 2 * m
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + m, y + m, iw, ih), r - 8, r - 8), doAntiAlias=True)
        k = max(iw / W, ih / H) * z
        c.translate(x + m + iw / 2 + dx * k, y + m + ih / 2 + dy * k); c.scale(k, k); c.translate(-W / 2, -H / 2)
        video(c, nom, 0, 0, W, H, t_local)
        c.restore()
        balayage(c, x, y, w2, h2, t, r, 0.35, 0.12)


def titre(c, s, t, t0, y, taille=118, couleur=BLANC, fin=None, track=-0.02):
    taille = ajuste(s, 640, taille, "noir", track)
    a = 1.0 if fin is None else 1 - prog(t, fin, 0.25, entree)
    lettres(c, s, 500, y, taille, t, t0, "masque", fam="noir", couleur=couleur, grad=False,
            decal=0.028, duree=0.42, track=track, alpha=a)


def ligne_sous(c, s, t, t0, y, taille=118, fin=None, track=-0.02):
    """filet qui se tire sous un titre"""
    a = prog(t, t0 + 0.25, 0.45) * (1.0 if fin is None else 1 - prog(t, fin, 0.25, entree))
    taille = ajuste(s, 640, taille, "noir", track)
    l = largeur(s, taille, "noir", track)
    trait(c, 500 - l / 2, y + taille * 1.18, 500 - l / 2 + l * a, y + taille * 1.18, GLACE, 3.0, min(1.0, a * 1.5))


def entre_s(t, t0, d=0.5):
    return prog(t, t0, d, lambda u: ressort(u, 1.2, 5.0))


def sort_s(t, t1, d=0.25):
    return 1 - prog(t, t1, d, entree)


# ─────────────────────────────────────────── scènes
def hook(c, t):
    """0 → « C'est » : le vortex, couvercle ouvert, plein cadre — rien d'autre"""
    if t >= T_CEST + 0.15: return
    # trois angles : le vortex de face, la plongée dans le vortex, puis le shake fini en plan héros
    T_A2, T_A3 = 2.9, 3.6
    if t < T_A2:
        rush(c, "videos/IMG_3413-d", t + 1.5, z=mix(1.06, 1.14, prog(t, 0.0, T_A2, lin)), dy=-20)
    elif t < T_A3:
        rush(c, "videos/IMG_3413-d", t - T_A2 + 4.3, z=1.12, dy=-60)
    else:
        rush(c, "videos/IMG_3413-d", t - T_A3 + 16.6, z=mix(1.08, 1.16, prog(t, T_A3, T_CEST - T_A3, lin)), dy=-40)
    # voile léger en bas pour le titre
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, H * 0.62), skia.Point(0, H)], [hexa("#000000", 0.0), hexa("#000000", 0.62)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    titre(c, "PAS UNE GOUTTE.", t, T_GOUTTE, 1300, 112, BLANC, fin=T_CEST - 0.05)
    ligne_sous(c, "PAS UNE GOUTTE.", t, T_GOUTTE, 1300, 112, fin=T_CEST - 0.05)
    # fondu au noir glace sur la coupe
    v = prog(t, T_CEST - 0.1, 0.12)
    if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000", v))


def presentation(c, t):
    """« C'est le VORIX. Y a un moteur dans la base. »"""
    if t < T_CEST - 0.1 or t > T_EAU + 0.2: return
    fond_neutre(c, t)
    a1 = entre_s(t, T_CEST, 0.55) * sort_s(t, T_MOTEUR - 0.05)
    # le produit en main, de face, logo
    carte_rush(c, "videos/IMG_3412-d", t - T_CEST + 20.2, 500, 760 + 40 * (1 - a1), 700, 1000, t, alpha=a1, s=mix(0.92, 1.0, a1))
    titre(c, "VORIX", t, T_VORIX, 1300, 124, BLANC, fin=T_MOTEUR - 0.05, track=0.26)
    # la base et l'hélice : le moteur
    a2 = entre_s(t, T_MOTEUR, 0.55) * sort_s(t, T_EAU - 0.05)
    zoom = mix(1.0, 1.22, prog(t, T_MOTEUR, T_EAU - T_MOTEUR, lin))
    carte_rush(c, "videos/IMG_3412-d", t - T_MOTEUR + 5.3, 500, 780, 700, 1000, t, alpha=a2, s=mix(0.92, 1.0, a2), z=zoom * 1.25, dy=-470)
    if t >= T_BASE - 0.05:
        pill_g(c, "UN MOTEUR DANS LA BASE", 500, 1290, 34, "doux", alpha=a2 * prog(t, T_BASE - 0.05, 0.3), s=mix(0.8, 1.0, entre_s(t, T_BASE - 0.05, 0.5)))


def demo(c, t):
    """« Tu mets l'eau, la poudre, t'appuies, et c'est mélangé. » — trois cartes, une par mot"""
    if t < T_EAU - 0.35 or t > T_ZERO + 0.2: return
    fond_neutre(c, t)
    etapes = [("videos/IMG_3413-d", 0.35, T_EAU - 0.25, "L'EAU"),
              ("videos/IMG_3413-d", 5.05, T_POUDRE, "LA POUDRE"),
              ("videos/IMG_3413-d", 6.05, T_APPUIE, "UN BOUTON")]
    n = len(etapes)
    for i, (nom, off, t0, lab) in enumerate(etapes):
        if t < t0 - 0.05: continue
        a = entre_s(t, t0, 0.5)
        # la carte active est grande au centre ; les précédentes glissent en haut, petites
        actif = all(t < etapes[j][2] for j in range(i + 1, n))
        if actif:
            cx, cy, w, h, s = 500, 780, 700, 1000, 1.0
            if i == 2:  # « c'est mélangé » : la carte grossit un peu
                g = prog(t, T_MELANGE, 0.6)
                w, h = 700 + 60 * g, 1000 + 80 * g
        else:
            k = prog(t, etapes[i + 1][2], 0.45)
            cx = mix(500, 190 + i * 300, k); cy = mix(780, 260, k); s = mix(1.0, 0.26, k)
            w, h = 700, 1000
        carte_rush(c, nom, t - t0 + off, cx, cy, w, h, t, alpha=a, s=s * mix(0.9, 1.0, a), z=1.12, dy=-300)
        if actif:
            pill_g(c, lab, 500, 1300, 36, "doux", alpha=a, s=mix(0.8, 1.0, a))
    v = prog(t, T_ZERO - 0.1, 0.12)
    if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000", v))


def resultat(c, t):
    """« Zéro grumeau au fond. » — plein cadre, la surface lisse"""
    if t < T_ZERO - 0.1 or t > T_CINQ + 0.05: return
    c.saveLayerAlpha(None, int(255 * (1 - prog(t, T_CINQ - 0.14, 0.16, entree))))
    rush(c, "videos/IMG_3413-d", t - T_ZERO + 13.6, z=mix(1.04, 1.12, prog(t, T_ZERO, 1.4, lin)))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, H * 0.6), skia.Point(0, H)], [hexa("#000000", 0.0), hexa("#000000", 0.6)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    titre(c, "PAS UN GRUMEAU.", t, T_ZERO + 0.05, 1270, 112, BLANC, fin=T_CINQ - 0.05)
    ligne_sous(c, "PAS UN GRUMEAU.", t, T_ZERO + 0.05, 1270, 112, fin=T_CINQ - 0.05)
    c.restore()


def specs(c, t):
    """« Cinq cents millilitres, batterie rechargeable, ça tient dans la main. » — pills empilées"""
    if t < T_CINQ - 0.5 or t > T_LAVER + 0.2: return
    fond_neutre(c, t)
    a = entre_s(t, T_CINQ - 0.42, 0.55) * sort_s(t, T_LAVER - 0.05)
    carte_rush(c, "videos/IMG_3413-d", t - T_CINQ + 15.2, 380, 760, 520, 860, t, alpha=a, s=mix(0.92, 1.0, a), z=1.10, dy=-80)
    for k, (lab, t0) in enumerate((("500 ML", T_CINQ), ("BATTERIE RECHARGEABLE", T_BATT), ("TIENT DANS LA MAIN", T_MAIN))):
        if t < t0 - 0.05: continue
        e = entre_s(t, t0, 0.5)
        pill_g(c, lab, 680 + 140 * (1 - e), 500 + k * 125, 32, "doux" if k else "doux", alpha=a * e, s=mix(0.8, 1.0, e))


def lavage(c, t):
    """« Et pour le laver, tout se démonte, tu passes ça sous l'eau, c'est réglé. »"""
    if t < T_LAVER - 0.1 or t > T_DEPUIS + 0.15: return
    if t < T_EAU2:
        rush(c, "videos/IMG_3412-d", t - T_LAVER + 10.1, z=mix(1.30, 1.40, prog(t, T_LAVER, 1.8, lin)), dy=-330)
    else:
        rush(c, "videos/IMG_3416", t - T_EAU2 + 2.6, z=mix(1.42, 1.52, prog(t, T_EAU2, 1.7, lin)), dx=130, dy=-330)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, H * 0.6), skia.Point(0, H)], [hexa("#000000", 0.0), hexa("#000000", 0.6)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    if t >= T_DEMONTE - 0.05:
        e = entre_s(t, T_DEMONTE, 0.5) * sort_s(t, T_DEPUIS - 0.05)
        pill_g(c, "SE DÉMONTE ENTIÈREMENT", 500, 1150, 36, "doux", alpha=e, s=mix(0.8, 1.0, e))
    v = prog(t, T_DEPUIS - 0.1, 0.12)
    if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000", v))


def signature(c, t):
    """« Depuis que je l'ai, je secoue plus rien. » puis la marque"""
    if t < T_DEPUIS - 0.1: return
    if t < T_SIGN + 0.3:
        rush(c, "videos/IMG_3412-d", t - T_DEPUIS + 22.2, z=mix(1.06, 1.14, prog(t, T_DEPUIS, 1.8, lin)))
    a = prog(t, T_SIGN, 0.45)
    if a > 0:
        with Calque(c, a):
            fond_neutre(c, t, pulse=0.4)
        i = moteur._img("vorix-symbole")
        lw = 320 * mix(0.9, 1.0, entre_s(t, T_SIGN + 0.1, 0.6))
        pp = skia.Paint(AntiAlias=True)
        pp.setColorFilter(skia.ColorFilters.Blend(hexa(BLANC, 1.0), skia.BlendMode.kSrcIn))
        pp.setAlphaf(borne(a * prog(t, T_SIGN + 0.05, 0.4)))
        lh = lw * i.height() / i.width()
        c.drawImageRect(i, skia.Rect.MakeXYWH(W / 2 - lw / 2, 700 - lh / 2, lw, lh), moteur._ECH, pp)
        lettres(c, "VORIX", W / 2, 905, 150, t, T_SIGN + 0.25, "masque", fam="noir", couleur=BLANC, grad=False, decal=0.04, track=0.26, alpha=a)
        lettres(c, "TRAIN.  FUEL.  PERFORM.", W / 2, 1105, 44, t, T_SIGN + 0.75, "masque", fam="noir", couleur=GLACE, grad=False, decal=0.02, track=0.30, alpha=a)
    v = prog(t, DUREE - 0.4, 0.4)
    if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000", v))


def dessine(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000"))
    hook(c, t); demo(c, t); presentation(c, t); specs(c, t); resultat(c, t); lavage(c, t); signature(c, t)
    if T_CEST + 0.1 <= t < T_SIGN - 0.1 and not (T_ZERO <= t < T_CINQ) and not (T_VORIX - 0.05 <= t < T_MOTEUR):
        ST.dessine(c, t)
    K.dessine_eclairs(c, t)
