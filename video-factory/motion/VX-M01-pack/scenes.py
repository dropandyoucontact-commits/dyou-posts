"""VX-M01-pack — VORIX, bande-annonce « montagne », SANS voix (31/10/2026, v5 « Grok »).

Mikail (30/10, 23 h) : « une bande-annonce, que ça fasse un peu sombre, dans une montagne comme ma bannière ».
Plus de rushes du client, plus de 3D : 7 images clés ChatGPT dans l'ambiance de sa bannière (VX-M03/media/images/k1..k7)
animées par Grok Imagine (720p, 10 s, 2:3 → recadrage « cover » plein cadre). Clips c1 héros, c2 vortex, c3 éclaté,
c7 plan large. Typo blanche, derniers mots en italique jaune, pastilles verre blanc, aucun bruitage, musique seule.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
moteur.PROJET = P
from moteur import *
from studio import lettres
from glace import pill_g, appliquer
appliquer()

DUREE = 25.0
NB_IMAGES = round(DUREE * FPS)
SFX, RAPIDE = [], []


def son(t, nom, gain=0.0): SFX.append((round(t, 3), nom, gain))
def rapide(t0, t1): RAPIDE.append((t0, t1))
def flou_a(t): return 3 if any(a <= t <= b for a, b in RAPIDE) else 1


# ─────────────────────────────────────────── repères (secondes)
T_ROT, T_VORTEX, T_TQ, T_ECL, T_FIN_IMG, FIN = 0.0, 8.0, 15.9, 19.4, 22.6, DUREE
NOIR, BLANC, GLACE = "#000000", "#FFFFFF", "#DCE6F0"
JAUNE = "#FFD400"          # l'accent sport (Youssef, 30/10) : une seule couleur, les derniers mots en italique jaune

for t0 in (T_VORTEX, T_TQ, T_ECL, T_FIN_IMG): rapide(t0 - 0.04, t0 + 0.10)


# ─────────────────────────────────────────── briques
def titre(c, s, t, t0, y, taille=100, fin=None, couleur=BLANC, duree=0.38, larg=780, accent=0):
    """un bloc de titre centré ; `accent` = nombre de mots de la fin en italique jaune"""
    taille = ajuste(s, larg, taille, "noir", -0.02)
    a = 1.0 if fin is None else 1 - prog(t, fin, 0.25, entree)
    if a <= 0.01: return
    mots = s.split(" ")
    if accent <= 0 or accent >= len(mots):
        lettres(c, s, 500, y, taille, t, t0, "masque", fam="noir", couleur=couleur, grad=False, decal=0.0, duree=duree, track=-0.02, alpha=a)
        return
    A, B = " ".join(mots[:-accent]), " ".join(mots[-accent:])
    esp = largeur("N N", taille, "noir", -0.02) - largeur("NN", taille, "noir", -0.02)
    wa, wb = largeur(A, taille, "noir", -0.02) + esp, largeur(B, taille, "noir", -0.02)
    x0 = 500 - (wa + wb) / 2
    lettres(c, A, x0, y, taille, t, t0, "masque", fam="noir", couleur=couleur, grad=False, decal=0.0, duree=duree, track=-0.02, alpha=a, align="gauche")
    hl = hauteurLigne(taille, "noir")
    c.save(); c.translate(x0 + wa, y + hl * 0.78); c.skew(-0.2, 0); c.translate(-(x0 + wa), -(y + hl * 0.78))
    lettres(c, B, x0 + wa, y, taille, t, t0, "masque", fam="noir", couleur=JAUNE, grad=False, decal=0.0, duree=duree, track=-0.02, alpha=a, align="gauche")
    c.restore()


def plan(c, nom, t_local, z=1.0, dx=0.0, dy=0.0, alpha=1.0):
    """un clip Grok 2:3 recadré « cover » plein cadre 9:16 ; zoom par la matrice (un seul cache 1080×1920 par clip)"""
    c.save(); c.translate(W / 2 + dx, H / 2 + dy); c.scale(z, z); c.translate(-W / 2, -H / 2)
    video(c, nom, 0, 0, W, H, t_local, boucle=False, alpha=alpha)
    c.restore()


def voile(c, a):
    if a > 0.004: c.drawRect(skia.Rect.MakeWH(W, H), peinture(NOIR, borne(a)))


def voile_bas(c, a=0.62, y0=0.6):
    """dégradé noir sous les titres, pour les lire sur la montagne"""
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, H * y0), skia.Point(0, H)], [hexa("#000000", 0.0), hexa("#000000", a)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


def pill(c, lab, t, t0, x, y, fin=None):
    if t < t0 - 0.05: return
    a = prog(t, t0, 0.5, lambda u: ressort(u, 1.2, 5.0)) * (1.0 if fin is None else 1 - prog(t, fin, 0.25, entree))
    if a <= 0.01: return
    w = largeur(lab, 34, "fort", -0.01) + 51
    pill_g(c, lab, x + w / 2 + 120 * (1 - a), y, 34, "doux", alpha=a, s=mix(0.85, 1.0, a))


def zoom(t, t0, t1, z0, z1): return mix(z0, z1, borne((t - t0) / max(0.01, t1 - t0)))


# ─────────────────────────────────────────── montage
def dessine(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), peinture(NOIR))

    # 1. HÉROS (0 → 8) : le shaker sur son rocher, la caméra tourne autour. Un bloc de titre à la fois.
    if t < T_VORTEX + 0.1:
        a = 1 - prog(t, T_VORTEX - 0.2, 0.25, entree)
        plan(c, "videos/c1", t - T_ROT, z=zoom(t, 0, T_VORTEX, 1.0, 1.05), alpha=a)
        with Calque(c, a):
            voile_bas(c, 0.66)
            titre(c, "VORIX.", t, 0.6, 1440, 140, fin=3.5)
            titre(c, "LE SHAKER ÉLECTRIQUE.", t, 0.6, 1625, 80, fin=3.5, accent=1)
            titre(c, "UN MOTEUR DANS LA BASE.", t, 3.9, 1480, 92, fin=7.5, accent=2)
            titre(c, "IL MÉLANGE TOUT SEUL.", t, 3.9, 1600, 82, fin=7.5, accent=2)
        voile(c, 1 - borne(t / 0.5))

    # 2. VORTEX (8 → 15,9) : macro, le shake qui tourne
    if T_VORTEX <= t < T_TQ + 0.1:
        a = 1 - prog(t, T_TQ - 0.2, 0.25, entree)
        plan(c, "videos/c2", t - T_VORTEX, z=zoom(t, T_VORTEX, T_TQ, 1.0, 1.06), alpha=a)
        with Calque(c, a):
            voile_bas(c, 0.6, 0.66)
            titre(c, "TU APPUIES.", t, T_VORTEX + 0.5, 1540, 110, fin=11.6, accent=1)
            titre(c, "ZÉRO GRUMEAU.", t, 12.0, 1540, 116, fin=T_TQ - 0.2, accent=1)

    # 3. LA FICHE (15,9 → 19,4) : le héros plus serré, décalé à gauche, trois pastilles à droite
    if T_TQ <= t < T_ECL + 0.1:
        a = 1 - prog(t, T_ECL - 0.2, 0.25, entree)
        plan(c, "videos/c1", t - T_TQ + 6.3, z=zoom(t, T_TQ, T_ECL, 1.18, 1.22), dx=-100, dy=30, alpha=a)
        with Calque(c, a):
            pill(c, "500 ML", t, 16.3, 690, 620)
            pill(c, "CORPS TRITAN", t, 17.0, 690, 740)
            pill(c, "RECHARGEABLE", t, 17.7, 690, 860)

    # 4. ÉCLATÉ (19,4 → 22,6) : les trois pièces sur le rocher
    if T_ECL <= t < T_FIN_IMG + 0.1:
        a = 1 - prog(t, T_FIN_IMG - 0.2, 0.25, entree)
        plan(c, "videos/c3", t - T_ECL, z=zoom(t, T_ECL, T_FIN_IMG, 1.0, 1.04), alpha=a)
        with Calque(c, a):
            voile_bas(c, 0.72, 0.64)
            titre(c, "TOUT SE DÉMONTE.", t, T_ECL + 0.4, 1500, 92, fin=T_FIN_IMG - 0.2, accent=1)
            titre(c, "PASSE SOUS L'EAU.", t, T_ECL + 0.4, 1620, 92, fin=T_FIN_IMG - 0.2, accent=1)

    # 5. FIN (22,6 → 25) : plan large, la marque dans le ciel noir
    if t >= T_FIN_IMG:
        plan(c, "videos/c7", t - T_FIN_IMG, z=zoom(t, T_FIN_IMG, FIN, 1.0, 1.03))
        titre(c, "VORIX", t, T_FIN_IMG + 0.5, 560, 150, couleur=BLANC)
        a = prog(t, T_FIN_IMG + 0.5, 0.38)
        if a > 0:
            texte(c, "TRAIN.  FUEL.  PERFORM.", 500 + 0.34 * 30 / 2, 770, 30, GLACE, "noir", align="centre", track=0.34, alpha=a * 0.9)
        voile(c, prog(t, FIN - 0.6, 0.6))
