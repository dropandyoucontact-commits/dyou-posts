"""MQ-M01 « Zara ne devine pas » — vidéo explicative MONARQUE (centrale d'achat textile française basée en Chine).

Charte reprise du site monarqueprod.com et de la plaquette : blanc cassé #F5F4F2, noir #0E0E0E, Archivo Black pour les
titres, reliefs blancs sculptés (cartes du monde, d'Europe et de Chine du site), logo officiel. Rushes : vidéo d'atelier
fournie par le client (media/rushes/). Voix Tomy à 3,6 mots/s, sous-titres fins (sans surlignage).
Aucun chiffre inventé : barres, curseurs et cartes seulement.
"""
import math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import SousTitresFins, texte_flou, lueur
import moteur

# polices : Archivo Black (titres du site) et PingFang (chinois)
moteur._prov.registerTypeface(skia.Typeface.MakeFromFile(str(P / "media" / "ArchivoBlack.ttf")), "ArchivoBlack")
moteur._prov.registerTypeface(skia.Typeface.MakeFromFile("/System/Library/Fonts/PingFang.ttc", 0), "PingFangCJK")
moteur._FAM["archivo"] = "ArchivoBlack"
moteur._FAM["cjk"] = "PingFangCJK"

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.5, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

FOND, INK, GR, BL = "#F5F4F2", "#0E0E0E", "#8C8985", "#FFFFFF"
MINT, VERT, ROUGE, ROSE, PIERRE = "#B8E6C5", "#17A05D", "#FF3B30", "#FFB7B7", "#DAD7D2"
OMBRE = (30, 70, 0.16)
SOUS = SousTitresFins(K, fusions={(135, 136, 137, 138): "monarqueprod.com."}, y=290, taille=62, fam="gras")


def ent(t, t0, d=0.42, s=1.6): return prog(t, t0, d, lambda v: rebond(v, s))
def sor(t, t0, d=0.28): return prog(t, t0, d, entree)
def titre(c, s, cx, cy, taille, col=INK, alpha=1.0, track=0.0): return texte_centre(c, s, cx, cy, taille, col, "archivo", alpha, track)
def bez(p0, p1, p2, u): return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])


def courbe(c, p0, p1, p2, u0, u1, col, ep, alpha=1.0, pointille=None):
    if u1 <= u0: return
    pa = peinture(col, alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=ep); pa.setStrokeCap(skia.Paint.kRound_Cap)
    if pointille: pa.setPathEffect(skia.DashPathEffect.Make(pointille, 0))
    path = skia.Path()
    for k in range(41):
        x, y = bez(p0, p1, p2, mix(u0, u1, k / 40))
        (path.moveTo if k == 0 else path.lineTo)(x, y)
    c.drawPath(path, pa)


# ─────────────────────────────────────────── fond : blanc cassé, plans sculptés qui dérivent
def fond_mq(c, t):
    c.clear(hexa(FOND))
    for x0, ph, a in [(-260, 0.0, 0.9), (330, 1.4, 0.7), (900, 2.7, 0.8)]:
        c.save(); c.translate(x0 + 70 * math.sin(t * 0.22 + ph), 960); c.rotate(-32)
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeLinear([skia.Point(-230, 0), skia.Point(230, 0)],
                                                   [hexa("#FFFFFF", 0.0), hexa("#FFFFFF", a), hexa("#E4E1DC", 0.55 * a), hexa("#E4E1DC", 0.0)], [0, 0.45, 0.55, 1]))
        c.drawRect(skia.Rect.MakeXYWH(-230, -1700, 460, 3400), g)
        c.restore()
    p = peinture("#D9D6D1", 0.55)
    dy = (t * 14) % 60
    for y in range(-60, H + 60, 60):
        for x in range(30, W, 60):
            c.drawCircle(x, y + 30 - dy, 1.7, p)


# ─────────────────────────────────────────── briques
def carte_blanche(c, x, y, w, h, r=40, alpha=1.0, col=BL, ombre=OMBRE):
    carte(c, x, y, w, h, r, col, alpha, ombre)


def photo(c, nom, cx, cy, w, h, r=36, zoom=1.0, fx=0.5, fy=0.5, cadre=12):
    carte_blanche(c, cx - w / 2, cy - h / 2, w, h, r)
    image_cover(c, nom, cx - w / 2 + cadre, cy - h / 2 + cadre, w - 2 * cadre, h - 2 * cadre, zoom, fx, fy, r - cadre / 2)


def clip(c, nom, cx, cy, w, h, tl, vitesse=1.0, r=36, cadre=12):
    """rush dans une carte ; w, h entiers et constants (le cache des images est fait à cette taille)"""
    carte_blanche(c, cx - w / 2, cy - h / 2, w, h, r)
    video(c, nom, cx - w / 2 + cadre, cy - h / 2 + cadre, w - 2 * cadre, h - 2 * cadre, tl, vitesse, True, r - cadre / 2)


def pilule(c, label, cx, cy, u, taille=34, fond_=INK, col=BL, ic=None, rot=0.0, ombre=(12, 30, 0.2)):
    if u <= 0.01: return
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.35, 1, u), mix(0.35, 1, u))
    pastille(c, label, 0, 0, taille, fond_, col, ic, borne(u * 2), ombre)
    c.restore()


def coche(c, label, cx, cy, u, taille=34):
    """pastille blanche, disque vert coché"""
    if u <= 0.01: return
    tw = largeur(label, taille, "noir"); h = taille * 2.2; w = tw + h + taille
    c.save(); c.translate(cx, cy); c.scale(mix(0.35, 1, u), mix(0.35, 1, u))
    with Calque(c, borne(u * 2)):
        rrect(c, -w / 2, -h / 2, w, h, h / 2, BL, 1, (14, 34, 0.2))
        disque(c, -w / 2 + h / 2, 0, h / 2 - 9, VERT)
        icone(c, "check", -w / 2 + h / 2, 0, h * 0.42, BL, 3.2)
        texte_centre(c, label, -w / 2 + h + tw / 2 - 4, 0, taille, INK, "noir")
    c.restore()


def epingle(c, x, y, label, u, col=INK, drapeau_=None, haut=80, taille=30):
    if u <= 0.01: return
    with Calque(c, borne(u * 2)):
        disque(c, x, y, 10, col); anneau(c, x, y, 18 * u, col, 3, 0.4)
        trait(c, x, y, x, y - haut * u, col, 4)
        c.save(); c.translate(x, y - haut * u); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
        w, h = pastille(c, label, 0, -34, taille, col, BL, None, 1.0, (10, 26, 0.2))
        if drapeau_: drapeau(c, drapeau_, -w / 2 - 58, -52, 48, 34, 6)
        c.restore()


def bulle_cjk(c, txt, x, y, u, droite=False):
    if u <= 0.01: return
    T = 36; tw = largeur(txt, T, "cjk", 0); bw, bh = tw + 56, T * 1.9
    ax = x + (bw if droite else 0)
    c.save(); c.translate(ax, y + bh); c.scale(mix(0.3, 1, u), mix(0.3, 1, u)); c.translate(-ax, -(y + bh))
    with Calque(c, borne(u * 2)):
        rrect(c, x, y, bw, bh, 30, BL, 1, (14, 36, 0.2))
        texte(c, txt, x + 28, y + bh / 2 - hauteurLigne(T, "cjk") / 2, T, INK, "cjk", track=0)
    c.restore()


# carte du monde du site (relief blanc) : fenêtre Europe → Chine
MSRC = (620.0, 200.0, 640.0, 420.0)
PARIS_I, CANTON_I = (705.0, 365.0), (1145.0, 500.0)


def carte_monde(c, cx, cy, w):
    """dessine la carte ; renvoie la fonction image → écran"""
    sx, sy, sw, sh = MSRC
    k = w / sw; h = sh * k
    x0, y0 = cx - w / 2, cy - h / 2
    carte_blanche(c, x0 - 14, y0 - 14, w + 28, h + 28, 44, 1.0, BL)
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0, w, h), 32, 32), True)
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x0 + w, y0 + h)], [hexa("#CFCBC5"), hexa("#E2DFDA")]))
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), g)
    c.drawImageRect(moteur._img("carte-monde"), skia.Rect.MakeXYWH(sx, sy, sw, sh), skia.Rect.MakeXYWH(x0, y0, w, h), moteur._ECH, skia.Paint(AntiAlias=True))
    c.restore()
    return lambda p: (x0 + (p[0] - sx) * k, y0 + (p[1] - sy) * k)


# ─────────────────────────────────────────── S0 · hook : Zara lit les données, votre boutique joue au bandit manchot
REELS = ["ROBE", "TRENCH", "JEAN", "PULL", "VESTE", "JUPE", "CHEMISE", "BLAZER"]
T_STOP = [TW(10) - 0.08, TW(10) + 0.2, TW(11) - 0.02]
T_LEV = TW(9) - 0.06
T1 = TW(12) - 0.12
COURBE_Z = [(0, 0.15), (0.12, 0.22), (0.22, 0.18), (0.34, 0.38), (0.46, 0.33), (0.58, 0.55), (0.7, 0.5), (0.82, 0.74), (1.0, 0.9)]


def s0(c, t):
    if t > T1 + 0.5: return
    o = prog(t, T1, 0.42, entree)
    # la carte ZARA : ventes en direct
    zo = prog(t, T_LEV - 0.12, 0.32, entree)
    if zo < 1:
        with Espace(c, 540, 600, rx=5, ry=-7 + 3 * math.sin(t * 2.1), ty=-520 * zo, s=1 + 0.02 * math.sin(t * 3)):
            with Calque(c, 1 - zo):
                carte_blanche(c, 130, 490, 820, 220, 44)
                texte(c, "ZARA", 180, 540, 92, INK, "archivo", track=0.06)
                texte(c, "Ventes en direct", 182, 652, 24, GR, "demi", track=0)
                pr = prog(t, 0.0, TW(8) + 0.15, lin)
                x0, y0, ww, hh = 540, 530, 370, 140
                pts = [(x0 + a * ww, y0 + hh - b * hh) for a, b in COURBE_Z]
                path = skia.Path(); n = 60
                for k in range(n + 1):
                    u = 0.12 + 0.88 * pr * k / n
                    j = min(len(pts) - 2, int(u * (len(pts) - 1)))
                    f = u * (len(pts) - 1) - j
                    x = mix(pts[j][0], pts[j + 1][0], f); y = mix(pts[j][1], pts[j + 1][1], f)
                    (path.moveTo if k == 0 else path.lineTo)(x, y)
                pa = peinture(VERT, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=8); pa.setStrokeCap(skia.Paint.kRound_Cap)
                c.drawPath(path, pa)
                lx, ly = path.getPoint(path.countPoints() - 1)
                disque(c, lx, ly, 13, VERT); anneau(c, lx, ly, 13 + 14 * ((t * 1.6) % 1), VERT, 3, 1 - (t * 1.6) % 1)
    # la machine
    m = prog(t, T_LEV, 0.5, sortie)
    cy = mix(1080, 960, m)
    sx = secousse(t, T_STOP[2], 20, 0.4)[0] + secousse(t, T_LEV + 0.08, 9, 0.3)[0]
    with Espace(c, 540 + sx, cy, rx=6, ry=4 * math.sin(t * 1.3), s=mix(1.0, 1.1, m) * mix(1, 0.7, o), tx=-1150 * o, rz=-6 * o):
        x0, y0, w, h = 110, cy - 300, 860, 600
        carte_blanche(c, x0, y0, w, h, 66, 1.0, BL, (44, 96, 0.24))
        rrect(c, x0 + 40, y0 + 34, w - 80, 84, 42, INK)
        titre(c, "COLLECTION", 540, y0 + 76, 40, BL, track=0.12)
        for k in range(9):                                              # ampoules
            on = (int(t * 9) + k) % 3 == 0 if t < T_STOP[2] else (int(t * 4) % 2 == 0)
            disque(c, x0 + 90 + k * 85, y0 + h - 40, 9, ROUGE if t >= T_STOP[2] else "#F2C14E", 1.0 if on else 0.3)
        for k in range(3):
            rx_, ry_, rw, rh = 540 + (k - 1) * 262 - 116, cy - 140, 232, 300
            rrect(c, rx_ - 6, ry_ - 6, rw + 12, rh + 12, 30, "#1C1C1C")
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(rx_, ry_, rw, rh), 26, 26), True)
            c.drawRect(skia.Rect.MakeXYWH(rx_, ry_, rw, rh), peinture("#FBFAF8"))
            mx, my = rx_ + rw / 2, ry_ + rh / 2
            if t < T_STOP[k]:
                pos = t * 12.5 + k * 2.7
                fl = math.floor(pos)
                for j in range(-2, 3):
                    mot = REELS[(fl + j) % len(REELS)]
                    yy = my + (j - (pos - fl)) * 128
                    T = ajuste(mot, 200, 50, "archivo")
                    for dy, a in ((-16, 0.25), (0, 0.9), (16, 0.25)):
                        titre(c, mot, mx, yy + dy, T, INK, a)
            else:
                u = prog(t, T_STOP[k], 0.4, lambda v: rebond(v, 2.4))
                yy = my + mix(-90, 0, u)
                titre(c, "?", mx, yy, mix(120, 190, u), ROUGE)
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, ry_), skia.Point(0, ry_ + rh)],
                                                       [hexa("#000000", 0.55), hexa("#000000", 0.0), hexa("#000000", 0.0), hexa("#000000", 0.55)], [0, 0.3, 0.7, 1]))
            c.drawRect(skia.Rect.MakeXYWH(rx_, ry_, rw, rh), g)
            c.restore()
            trait(c, rx_ - 10, my, rx_ + 4, my, ROUGE, 6); trait(c, rx_ + rw - 4, my, rx_ + rw + 10, my, ROUGE, 6)
        # le levier
        ang = cles(t, [(T_LEV - 0.01, 0), (T_LEV + 0.12, 75, sortie), (T_LEV + 0.55, 0, sortie)])
        c.save(); c.translate(x0 + w + 6, cy + 20); c.rotate(ang)
        trait(c, 0, 0, 0, -220, "#BDB8B1", 18); disque(c, 0, -230, 38, ROUGE, 1, (8, 20, 0.25)); disque(c, -10, -242, 12, BL, 0.5)
        c.restore()
        rrect(c, x0 + w - 10, cy - 10, 44, 70, 16, "#BDB8B1")
        tampon(c, "AU HASARD", 540, cy + 330, t, TW(11) + 0.08, 58, ROUGE, -8)


# ─────────────────────────────────────────── S1 · le bon de commande, des mois à l'avance
T2 = TW(20) - 0.1
MOIS = ["MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPT."]
T_MOIS = [TW(16) + k * (TW(19) + 0.12 - TW(16)) / 6 for k in range(7)]
SW = ["#C9B79C", "#222222", "#EFE8DA", "#B5523B", "#7A8B6F"]


def s1(c, t):
    if t < T1 - 0.05 or t > T2 + 0.5: return
    u = ent(t, T1 + 0.02, 0.5, 1.3); o = prog(t, T2, 0.42, entree)
    with Espace(c, 540, 1020, rx=mix(32, 4, u), ry=-5 + 2 * math.sin(t * 1.6), s=mix(0.5, 1, u) * mix(1, 0.75, o), ty=mix(500, 0, u), tx=-1150 * o):
        with Calque(c, borne(u * 3)):
            carte_blanche(c, 150, 700, 720, 660, 46)
            texte(c, "BON DE COMMANDE", 205, 748, 42, INK, "archivo", track=0.02)
            texte(c, "Collection · saison prochaine", 207, 808, 26, GR, "demi", track=0)
            for k in range(5):
                a = ent(t, TW(13) + 0.07 * k, 0.32, 1.8)
                if a <= 0: continue
                y = 870 + k * 68
                with Calque(c, borne(a * 2)):
                    c.save(); c.translate(mix(-60, 0, a), 0)
                    rrect(c, 205, y, 52, 52, 12, SW[k])
                    rrect(c, 278, y + 8, [300, 240, 330, 210, 280][k], 14, 7, "#E3E0DB")
                    rrect(c, 278, y + 32, 150, 10, 5, "#EEECE8")
                    rrect(c, 700, y + 10, 110, 32, 16, INK, 0.9)
                    c.restore()
            texte(c, "Budget engagé", 205, 1225, 26, INK, "gras", track=0)
            f = prog(t, TW(15), TW(19) - TW(15), entreeSortie)
            rrect(c, 205, 1270, 610, 22, 11, "#E8E6E2"); rrect(c, 205, 1270, 610 * f, 22, 11, INK if f < 1 else ROUGE)
            tampon(c, "COMMANDÉ", 640, 1130, t, TW(19) + 0.02, 48, INK, -10, "check")
    # le calendrier qui file
    a = ent(t, TW(15) - 0.12, 0.45, 2.0) * (1 - o)
    if a > 0:
        with Espace(c, 800, 620, ry=mix(-60, -12, a), rz=6, s=mix(0.4, 1, a), tx=-1150 * o):
            with Calque(c, borne(a * 2)):
                carte_blanche(c, 660, 470, 280, 300, 34, 1, BL, (24, 60, 0.22))
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(660, 470, 280, 300), 34, 34), True)
                c.drawRect(skia.Rect.MakeXYWH(660, 470, 280, 76), peinture(ROUGE)); c.restore()
                texte_centre(c, "LIVRAISON", 800, 508, 24, BL, "noir", 1, 0.08)
                k = sum(1 for tt in T_MOIS if t >= tt) - 1
                k = max(0, k)
                uf = prog(t, T_MOIS[k], 0.14, sortie) if k > 0 else 1
                c.save(); c.translate(800, 660); c.scale(1, mix(0.2, 1, uf))
                titre(c, MOIS[k], 0, 0, ajuste(MOIS[k], 240, 62, "archivo"), INK)
                c.restore()
                for j in range(2):
                    disque(c, 730 + j * 140, 470, 12, "#BDB8B1")


# ─────────────────────────────────────────── S2-S3 · rupture d'un côté, stock qui dort de l'autre
T3 = TW(34) - 0.1
CARTONS = [(700, 1250, -3, TW(26) - 0.05), (898, 1252, 2, TW(28) - 0.05), (800, 1092, -2, TW(29) + 0.02), (790, 934, 4, TW(30) + 0.05)]


def s2(c, t):
    if t < T2 - 0.05 or t > T3 + 0.5: return
    u = ent(t, T2 + 0.02, 0.5, 1.3); o = prog(t, T3, 0.42, entree)
    d = prog(t, TW(26) - 0.15, 0.45, entreeSortie)               # la carte se range à gauche quand le stock arrive
    cx = mix(540, 290, d)
    rup = prog(t, TW(25) - 0.02, 0.2)
    with Espace(c, cx, 1010, ry=mix(-55, 6, u) + 2 * math.sin(t * 1.7), s=mix(0.5, 1, u) * mix(1.12, 0.92, d) * mix(1, 0.7, o), tx=-1150 * o):
        with Calque(c, borne(u * 3)):
            carte_blanche(c, cx - 210, 690, 420, 640, 40)
            image_cover(c, "f_33", cx - 198, 702, 396, 440, 1.15 + 0.05 * math.sin(t), 0.45, 0.5, 30)
            if rup > 0: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 198, 702, 396, 440), 30, 30), peinture("#FFFFFF", 0.55 * rup))
            texte(c, "Trench beige", cx - 186, 1160, 34, INK, "archivo", track=0)
            texte(c, "Stock", cx - 186, 1222, 24, GR, "gras", track=0)
            f = 1 - prog(t, TW(22), TW(25) - TW(22) + 0.05, entreeSortie)
            rrect(c, cx - 186, 1262, 372, 20, 10, "#E8E6E2")
            if f > 0.01: rrect(c, cx - 186, 1262, 372 * f, 20, 10, VERT if f > 0.3 else ROUGE)
            tampon(c, "RUPTURE", cx, 940, t, TW(25), 60, ROUGE, -12, "x")
    pilule(c, "Top ventes", cx, 650, ent(t, TW(22) - 0.08, 0.4, 2.4) * (1 - sor(t, TW(26) - 0.15)), 32, VERT, BL, "trending-up", -4)
    # les cartons qui s'empilent
    for k, (x, y, rot, t0) in enumerate(CARTONS):
        if t < t0: continue
        ch = prog(t, t0, 0.3, entree)
        yy = mix(y - 900, y, ch) - 900 * o
        sh = secousse(t, t0 + 0.3, 8, 0.25)
        c.save(); c.translate(sh[0], sh[1])
        carton(c, x - 1150 * o * 0 + 0, yy, 200, 0, 1 - o, rot + mix(-25, 0, ch))
        c.restore()
        poussiere = prog(t, TW(31) - 0.1, 0.8, lin)
        if poussiere > 0 and ch >= 1:
            h_ = 156
            rrect(c, x - 100, yy - h_ / 2, 200, h_, 12, "#9C958C", 0.28 * poussiere * (1 - o))
    # zZz
    for j, (dx, tt, T) in enumerate([(0, 0.0, 44), (50, 0.22, 60), (110, 0.44, 78)]):
        a = prog(t, TW(31) - 0.05 + tt, 0.5, sortie) * (1 - o)
        if a > 0:
            fl = 30 * math.sin((t - TW(31)) * 3 + j)
            titre(c, "Z", 860 + dx + fl, mix(860, 760 - j * 70, a), T, GR, borne(a * 2) * (1 - sor(t, T3 - 0.1)))
    pilule(c, "Capital bloqué", 800, 1430, ent(t, TW(33) - 0.08, 0.42, 2.4) * (1 - o), 34, ROUGE, BL, "lock", 3)


# ─────────────────────────────────────────── S4 · produire en Chine seul : la langue, les intermédiaires
T4 = TW(43) - 0.1
CANTON_C = (650, 660)
CHAINE = [("Vous", "user"), ("Agent", "message-circle"), ("Grossiste", "building-2"), ("Usine", "factory")]


def s4(c, t):
    if t < T3 - 0.05 or t > T4 + 0.5: return
    u = ent(t, T3 + 0.02, 0.55, 1.2); o = prog(t, T4, 0.42, entree)
    m = prog(t, TW(41) - 0.2, 0.45, entreeSortie)
    w = mix(940, 640, m); cy = mix(960, 700, m)
    k = w / 1040; h = 833 * k; x0, y0 = 540 - w / 2, cy - h / 2
    with Espace(c, 540, cy, rx=mix(40, 8, u), s=mix(0.6, 1, u) * mix(1, 0.7, o), ty=-900 * o):
        with Calque(c, borne(u * 3) * (1 - o)):
            carte_blanche(c, x0 - 16, y0 - 16, w + 32, h + 32, 44)
            image(c, "chine", x0, y0, w)
            px, py = x0 + CANTON_C[0] * k, y0 + CANTON_C[1] * k
            onde(c, px, py, t, TW(37), 20, 160, ROUGE, 6, 0.7)
            epingle(c, px, py, "Usines", ent(t, TW(37) - 0.08, 0.42, 2.0), ROUGE, "CN", mix(90, 60, m))
            # vous, seul, loin
            a = ent(t, TW(38) - 0.08, 0.4, 2.2)
            if a > 0:
                vx, vy = x0 + 170 * k, y0 + 250 * k
                courbe(c, (vx, vy), ((vx + px) / 2, vy - 60), (px, py - 20), 0, a, GR, 4, 0.8, [14, 12])
                c.save(); c.translate(vx, vy); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
                disque(c, 0, 0, 56 * mix(1, 0.8, m), BL, 1, (12, 30, 0.22)); icone(c, "user", 0, 0, 56 * mix(1, 0.8, m), INK, 2.6)
                q = 1 + 0.12 * math.sin(t * 9)
                c.save(); c.translate(48, -52); c.scale(q, q); disque(c, 0, 0, 26, ROUGE); titre(c, "?", 0, 0, 32, BL); c.restore()
                c.restore()
    # la langue
    b1 = ent(t, TW(39) - 0.08, 0.36, 1.8) * (1 - prog(t, TW(41) - 0.25, 0.25, entree))
    b2 = ent(t, TW(40) - 0.02, 0.36, 1.8) * (1 - prog(t, TW(41) - 0.25, 0.25, entree))
    bulle_cjk(c, "最低起订量是多少？", 470, 1180, b1, True)
    bulle_cjk(c, "请先付定金。", 210, 1300, b2)
    texte_centre(c, "Échange illustratif", 540, 1440, 22, GR, "demi", max(b1, b2) * 0.9, 0)
    # les intermédiaires
    for i, (lab, ic) in enumerate(CHAINE):
        a = ent(t, TW(41) - 0.06 + 0.08 * i, 0.36, 2.0) * (1 - o)
        if a <= 0: continue
        x = 160 + i * 253; y = 1170
        if i > 0:
            ua = prog(t, TW(41) + 0.08 * i, 0.25, sortie) * (1 - o)
            trait(c, x - 253 + 74, y, x - 253 + 74 + (253 - 148) * ua, y, INK, 5, ua)
            pilule(c, "+ marge", x - 126, y - 112, ent(t, TW(42) - 0.05 + 0.12 * (i - 1), 0.36, 2.6) * (1 - o), 26, ROUGE, BL, None, [-6, 4, -3][i - 1])
        c.save(); c.translate(x, y); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
        with Calque(c, borne(a * 2)):
            disque(c, 0, 0, 68, INK if i == 0 else BL, 1, (12, 30, 0.2))
            icone(c, ic, 0, 0, 62, BL if i == 0 else INK, 2.6)
            texte_centre(c, lab, 0, 108, 28, INK, "noir")
        c.restore()


# ─────────────────────────────────────────── S5 · échantillon ≠ production
T5 = TW(52) - 0.12
DEFAUTS = [(-90, -120), (70, 30), (-40, 150)]


def s5(c, t):
    if t < T4 - 0.05 or t > T5 + 0.4: return
    o = prog(t, T5 - 0.05, 0.3, entree)
    for j, (cx, lab, t0) in enumerate([(290, "ÉCHANTILLON", T4 + 0.02), (790, "PRODUCTION", TW(45) - 0.12)]):
        u = ent(t, t0, 0.5, 1.3)
        if u <= 0: continue
        sx = mix(cx, 540, o)
        with Espace(c, sx, 1000, ry=mix(-70 if j else 70, 10 if j == 0 else -10, u), s=mix(0.5, 1, u) * mix(1, 0.1, o), rz=mix(0, 20 if j else -20, o)):
            with Calque(c, borne(u * 3) * (1 - o)):
                carte_blanche(c, sx - 215, 680, 430, 640, 40)
                texte_centre(c, lab, sx, 730, 30, INK, "archivo", 1, 0.06)
                if j == 0:
                    image_cover(c, "f_33", sx - 200, 772, 400, 430, 1.2, 0.45, 0.5, 26)
                    a = ent(t, TW(44) - 0.05, 0.4, 2.6)
                    if a > 0:
                        c.save(); c.translate(sx + 160, 790); c.scale(a, a); disque(c, 0, 0, 44, VERT, 1, (8, 20, 0.25)); icone(c, "check", 0, 0, 48, BL, 3.4); c.restore()
                else:
                    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx - 200, 772, 400, 430), 26, 26), True)
                    c.translate(sx, 987); c.rotate(5); c.translate(-sx, -987)
                    image_cover(c, "f_33", sx - 230, 750, 460, 480, 1.5, 0.62, 0.35)
                    c.restore()
                    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx - 200, 772, 400, 430), 26, 26), peinture("#5A3B1E", 0.28))
                    trait(c, sx - 170, 1080, sx + 160, 1010, "#2A1B0E", 4, 0.8, [10, 18])
                    for k, (dx, dy) in enumerate(DEFAUTS):
                        a = prog(t, TW(51) - 0.05 + 0.1 * k, 0.3, lambda v: rebond(v, 2))
                        if a > 0: anneau(c, sx + dx, 987 + dy, 52 * a, ROUGE, 7, borne(a * 2))
                texte_centre(c, "Validé" if j == 0 else "Reçu", sx, 1262, 30, VERT if j == 0 else ROUGE, "noir")
    a = ent(t, TW(48) - 0.08, 0.36, 2.8) * (1 - o)
    if a > 0:
        sh = secousse(t, TW(48), 12, 0.3)
        c.save(); c.translate(540 + sh[0], 1000 + sh[1]); c.scale(a, a)
        disque(c, 0, 0, 74, ROUGE, 1, (12, 30, 0.3)); texte_centre(c, "≠", 0, 2, 120, BL, "noir")
        c.restore()
    if t < T5 - 0.05:
        tampon(c, "NON CONFORME", 790, 1180, t, TW(51) + 0.12, 40, ROUGE, -9)


# ─────────────────────────────────────────── S6 · MONARQUE : disque noir, logo, puis Paris → Chine
T_M = TW(52) - 0.06
T_MR = TW(55) - 0.22              # le disque se retire, le logo va se poser en haut de la carte
T6 = TW(62) - 0.1
LOGO_W = 860


def logo(c, cx, cy, w, blanc=False, alpha=1.0):
    nom = "logo-blanc" if blanc else "logo-noir"
    iw, ih = taille_img(nom); image(c, nom, cx - w / 2, cy - w * ih / iw / 2, w, alpha)


def disque_noir(c, t, t0, t1, cx=540, cy=1000):
    r = cles(t, [(t0, 0), (t0 + 0.28, 2000, entree), (t1, 2000), (t1 + 0.34, 0, entreeSortie)])
    if r > 1: disque(c, cx, cy, r, INK)
    return r


def s6(c, t):
    if t < T_M - 0.05 or t > T6 + 0.5: return
    r = disque_noir(c, t, T_M, T_MR)
    u = prog(t, T_M + 0.16, 0.36, lambda v: rebond(v, 1.6))
    v = prog(t, T_MR, 0.42, entreeSortie)                # le logo descend se poser sur la carte
    o = prog(t, T6, 0.42, entree)
    # la carte
    a = ent(t, T_MR + 0.05, 0.6, 1.1)
    if a > 0:
        with Espace(c, 540, 980, rx=mix(30, 8, a) + 2 * math.sin(t * 1.2), s=mix(1.3, 1, a) * mix(1, 0.8, o), ty=-1000 * o):
            with Calque(c, borne(a * 2) * (1 - o)):
                vers = carte_monde(c, 540, 1000, 980)
                pa, pc = vers(PARIS_I), vers(CANTON_I)
                ctrl = ((pa[0] + pc[0]) / 2, min(pa[1], pc[1]) - 260)
                ua = prog(t, TW(58) + 0.05, TW(61) - TW(58), entreeSortie)
                courbe(c, pa, ctrl, pc, 0, ua, INK, 7)
                if 0 < ua < 1:
                    hx, hy = bez(pa, ctrl, pc, ua); disque(c, hx, hy, 14, INK); anneau(c, hx, hy, 24, INK, 3, 0.4)
                epingle(c, pa[0], pa[1], "Paris", ent(t, TW(58) - 0.08, 0.42, 2.0), INK, "FR", 90)
                onde(c, pc[0], pc[1], t, TW(61), 20, 180, INK, 6, 0.7)
                epingle(c, pc[0], pc[1], "Chine", ent(t, TW(61) - 0.06, 0.42, 2.0), INK, "CN", 90)
    # le rush de l'atelier, sur place
    b = ent(t, TW(59) - 0.08, 0.5, 1.4) * (1 - o)
    if b > 0:
        with Espace(c, 820, 1330, ry=mix(-50, -10, b), rz=4, s=mix(0.3, 1, b), ty=-1000 * o):
            with Calque(c, borne(b * 2)):
                clip(c, "rushes/atelier", 820, 1330, 300, 400, t - TW(59) + 0.5, 1.2, 30, 10)
                pilule(c, "Bureau sur place", 820, 1530, 1.0, 26, INK, BL, "map-pin")
    # le logo : blanc sur le disque, puis noir en haut de la carte
    if t >= T_M + 0.14:
        lw = mix(1.5, 1, u) * mix(LOGO_W, 420, v)
        ly = mix(1000, 545, v) - 1000 * o
        if v < 1: logo(c, 540, ly, lw, True, borne(u * 3) * (1 - v))
        if v > 0: logo(c, 540, ly, lw, False, v * (1 - o))
    return r


# ─────────────────────────────────────────── S7 · on part de votre marché
T7 = TW(67) - 0.1


def s7(c, t):
    if t < T6 - 0.05 or t > T7 + 0.5: return
    u = ent(t, T6 + 0.02, 0.5, 1.3); o = prog(t, T7, 0.42, entree)
    with Espace(c, 540, 1000, ry=mix(50, -6, u) + 3 * math.sin(t * 1.4), rx=4, s=mix(0.5, 1, u) * mix(1, 0.8, o), tx=-1150 * o):
        with Calque(c, borne(u * 3)):
            photo(c, "shop", 540, 1010, 640, 820, 40, 1.05 + 0.05 * prog(t, T6, 1.2, lin), 0.5, 0.42)
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 612), skia.Point(0, 1408)], [hexa("#8F8A83", 0.35), hexa("#3B3834", 0.55)]))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(232, 612, 616, 796), 34, 34), g)
            titre(c, "VOTRE MARCHÉ", 540, 1330, 40, BL, 1, 0.06)
    onde(c, 540, 1000, t, TW(66) - 0.05, 120, 520, INK, 6, 0.8)
    for lab, ic, x, y, t0, rot in [("Votre clientèle", "users", 300, 660, TW(63) - 0.08, -5), ("Vos prix", "receipt", 820, 920, TW(64) - 0.02, 4),
                                   ("Les tendances", "trending-up", 330, 1180, TW(66) - 0.08, -3)]:
        pilule(c, lab, x - 1150 * o, y, ent(t, t0, 0.42, 2.4), 32, BL, INK, ic, rot)


# ─────────────────────────────────────────── S8 · développement : matières, patronages, prototypes
T8 = TW(74) - 0.12
DEV = [(200, "MATIÈRES", TW(71) - 0.06), (540, "PATRONAGES", TW(72) - 0.06), (880, "PROTOTYPES", TW(73) - 0.06)]
TISSUS = [("#C9B79C", -20), ("#2B2B2B", -7), ("#EFE8DA", 6), ("#B5523B", 19)]


def tissu(c, x, y, w, h, col):
    rrect(c, x, y, w, h, 16, col, 1, (8, 20, 0.2))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 16, 16), True)
    clair = col in ("#EFE8DA", "#C9B79C")
    for k in range(0, int(w + h), 9):
        trait(c, x + k, y, x + k - h, y + h, "#000000" if clair else "#FFFFFF", 1.5, 0.08, rond=False)
    c.restore()


def contenu_dev(c, j, cx, cy, t):
    if j == 0:
        for col, rot in TISSUS:
            c.save(); c.translate(cx, cy + 150); c.rotate(rot); tissu(c, -70, -300, 140, 230, col); c.restore()
    elif j == 1:
        rrect(c, cx - 130, cy - 190, 260, 380, 18, "#F1E7D6")
        pa = peinture(INK, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=4)
        pa.setPathEffect(skia.DashPathEffect.Make([14, 9], 0))
        c.drawPath(chemin_svg(f"M{cx-100} {cy-150} L{cx-30} {cy-170} Q{cx} {cy-140} {cx+30} {cy-170} L{cx+100} {cy-150} L{cx+80} {cy-60} "
                              f"L{cx+70} {cy+40} L{cx-70} {cy+40} L{cx-80} {cy-60} Z"), pa)
        c.drawPath(chemin_svg(f"M{cx-95} {cy+80} L{cx+95} {cy+80} L{cx+70} {cy+165} L{cx-70} {cy+165} Z"), pa)
        trait(c, cx, cy - 140, cx, cy + 30, ROUGE, 3, 0.8, [6, 8])
        icone(c, "scissors", cx + 92, cy + 120, 52, INK, 2.4)
    else:
        video(c, "rushes/couture", cx - 138, cy - 208, 276, 416, t - TW(73) + 0.6, 1.0, True, 26)


def s8(c, t):
    if t < T7 - 0.05 or t > T8 + 0.5: return
    o = prog(t, T8, 0.42, entree)
    pilule(c, "Développement produit", 540 - 1150 * o, 560, ent(t, TW(68) - 0.1, 0.42, 2.0), 32, INK, BL, "wand-sparkles")
    for j, (cx, lab, tf) in enumerate(DEV):
        u = ent(t, T7 + 0.03 + 0.08 * j, 0.5, 1.4)
        if u <= 0: continue
        f = prog(t, tf, 0.42, lambda v: rebond(v, 1.8))
        with Espace(c, cx, 1010, ry=(1 - j) * 10 + 2 * math.sin(t * 1.5 + j), rx=mix(40, 5, u), s=mix(0.4, 1, u) * mix(1, 1.04, battement(t, tf, 1, 0.3) - 1 + 0) * mix(1, 0.8, o),
                    ty=mix(400, 0, u), tx=-1150 * o):
            with Calque(c, borne(u * 3)):
                carte_blanche(c, cx - 155, 780, 310, 460, 34)
                if f < 1:
                    rrect(c, cx - 135, 800, 270, 420, 26, "#F1EFEC", 1 - f, None, "#CFCBC5", 3)
                    titre(c, "?", cx, 1010, 110, "#CFCBC5", 1 - f)
                if f > 0:
                    with Calque(c, borne(f * 2)):
                        c.save(); c.translate(cx, 1010); c.scale(mix(0.6, 1, f), mix(0.6, 1, f)); c.translate(-cx, -1010)
                        contenu_dev(c, j, cx, 1010, t)
                        c.restore()
            titre(c, lab, cx, 1300, 30, INK, borne(f * 2) * (1 - o), 0.04)


# ─────────────────────────────────────────── S9 · on compare les usines
T9 = TW(78) - 0.1
USINES = [("Usine A", (0.5, 0.8, 0.55)), ("Usine B", (0.92, 0.78, 0.86)), ("Usine C", (0.68, 0.42, 0.5))]
CRIT = ["Qualité", "Prix", "Délai"]


def s9(c, t):
    if t < T8 - 0.05 or t > T9 + 0.5: return
    o = prog(t, T9, 0.4, entree)
    choix = prog(t, TW(77) - 0.04, 0.4, lambda v: rebond(v, 1.6))
    for i, (nom, vals) in enumerate(USINES):
        u = ent(t, T8 + 0.03 + 0.08 * i, 0.45, 1.4)
        if u <= 0: continue
        y = 730 + i * 230
        sel = i == 1
        al = 1 - 0.6 * choix * (0 if sel else 1)
        s = mix(0.5, 1, u) * (mix(1, 1.05, choix) if sel else 1) * mix(1, 0.8, o)
        with Espace(c, 540, y, rx=mix(60, 0, u), s=s, tx=mix(-900 if i % 2 else 900, 0, u) + (1150 if i % 2 else -1150) * o):
            with Calque(c, borne(u * 3) * al):
                carte_blanche(c, 120, y - 95, 840, 190, 38, 1, BL)
                if sel and choix > 0: rrect(c, 120, y - 95, 840, 190, 38, None, 1, None, INK, 6 * choix)
                disque(c, 205, y, 52, INK); icone(c, "factory", 205, y, 52, BL, 2.4)
                texte(c, nom, 280, y - 34, 40, INK, "archivo", track=0)
                for k, cr in enumerate(CRIT):
                    xx = 560 + k * 130
                    texte(c, cr, xx, y - 52, 20, GR, "gras", track=0)
                    f = vals[k] * prog(t, TW(75) - 0.1 + 0.05 * i + 0.05 * k, 0.5, sortie)
                    rrect(c, xx, y - 14, 18, 70, 9, "#ECEAE6"); rrect(c, xx, y - 14 + 70 * (1 - f), 18, 70 * f, 9, VERT if sel and choix > 0 else INK)
                    rrect(c, xx + 30, y - 14, 70, 70, 14, "#F4F2EF")
                    icone(c, ["gem", "banknote", "timer"][k], xx + 65, y + 21, 38, INK, 2.2)
    # le scan qui passe
    sc = prog(t, TW(75) - 0.1, TW(77) - TW(75), lin)
    if 0 < sc < 1:
        ys = mix(640, 1260, sc)
        lueur(c, 540, ys, 260, MINT, 0.5)
        trait(c, 110, ys, 970, ys, VERT, 5, 0.9)
    coche(c, "Retenue", 790, 860, choix * (1 - o), 30)


# ─────────────────────────────────────────── S10 · on négocie les prix, les volumes, les délais
T10 = TW(86) - 0.1
NEGO = [("PRIX", "banknote", TW(81), 0.86, 0.42), ("VOLUMES", "package", TW(83), 0.3, 0.72), ("DÉLAIS", "timer", TW(85), 0.84, 0.38)]


def s10(c, t):
    if t < T9 - 0.05 or t > T10 + 0.5: return
    u = ent(t, T9 + 0.02, 0.5, 1.3); o = prog(t, T10, 0.42, entree)
    with Espace(c, 540, 1010, rx=mix(-35, 4, u), ry=2 * math.sin(t * 1.3), s=mix(0.5, 1, u) * mix(1, 0.8, o), tx=1150 * o):
        with Calque(c, borne(u * 3)):
            carte_blanche(c, 120, 690, 840, 640, 44)
            disque(c, 200, 770, 44, INK); icone(c, "heart-handshake", 200, 770, 46, BL, 2.4)
            texte(c, "NÉGOCIATION", 268, 744, 42, INK, "archivo", track=0.04)
            for k, (lab, ic, tm, v0, v1) in enumerate(NEGO):
                y = 900 + k * 150
                v = cles(t, [(tm - 0.18, v0), (tm + 0.38, v1, entreeSortie)])
                fini = prog(t, tm + 0.35, 0.3, lambda w_: rebond(w_, 2.2))
                actif = 1 if tm - 0.2 <= t <= tm + 0.6 else 0
                icone(c, ic, 190, y + 8, 40, INK, 2.4)
                texte(c, lab, 230, y - 12, 30, INK, "archivo", track=0.03)
                x0, ww = 230, 600
                rrect(c, x0, y + 40, ww, 16, 8, "#E8E6E2"); rrect(c, x0, y + 40, ww * v, 16, 8, VERT if fini > 0 else INK)
                kx = x0 + ww * v
                if actif: lueur(c, kx, y + 48, 80, MINT, 0.6)
                disque(c, kx, y + 48, 24, BL, 1, (6, 14, 0.25)); anneau(c, kx, y + 48, 24, INK, 4)
                if fini > 0:
                    c.save(); c.translate(880, y + 20); c.scale(fini, fini); disque(c, 0, 0, 30, VERT); icone(c, "check", 0, 0, 34, BL, 3.4); c.restore()
                if actif and k != 1:
                    icone(c, "trending-down", kx, y - 6, 34, VERT, 3)


# ─────────────────────────────────────────── S11 · contrôle qualité sur place, dans l'atelier
T11 = TW(94) - 0.1
CTRL = [("Coutures", 330, 790, TW(89) - 0.05), ("Mesures", 760, 1020, TW(91) - 0.05), ("Finitions", 340, 1260, TW(93) - 0.05)]


def s11(c, t):
    if t < T10 - 0.05 or t > T11 + 0.5: return
    u = ent(t, T10 + 0.02, 0.55, 1.2); o = prog(t, T11, 0.42, entree)
    cy = 1000
    with Espace(c, 540, cy, rx=mix(35, 3, u), ry=mix(-30, 0, u) + 4 * math.sin(t * 1.1), s=mix(0.55, 1, u) * mix(1, 0.75, o), tx=-1150 * o):
        with Calque(c, borne(u * 3)):
            clip(c, "rushes/controle", 540, cy, 560, 980, t - T10, 1.0, 44, 12)
            x0, y0, w, h = 552 - 280, cy - 478, 536, 956
            sc = ((t - T10) / 1.2) % 1
            ys = y0 + 40 + sc * (h - 80)
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, ys - 120), skia.Point(0, ys)], [hexa(MINT, 0.0), hexa(MINT, 0.45)]))
            c.drawRect(skia.Rect.MakeXYWH(x0 - 12, ys - 120, w, 120), g)
            trait(c, x0 + 10, ys, x0 + w - 30, ys, MINT, 5)
            for (bx, by, sx, sy) in [(x0 + 10, y0 + 10, 1, 1), (x0 + w - 34, y0 + 10, -1, 1), (x0 + 10, y0 + h - 34, 1, -1), (x0 + w - 34, y0 + h - 34, -1, -1)]:
                trait(c, bx, by, bx + 60 * sx, by, BL, 7); trait(c, bx, by, bx, by + 60 * sy, BL, 7)
            rrect(c, 540 - 170, y0 + 30, 340, 64, 32, INK, 0.85)
            disque(c, 540 - 130, y0 + 62, 10, ROUGE, 0.4 + 0.6 * (int(t * 3) % 2))
            texte_centre(c, "ATELIER · CHINE", 548, y0 + 62, 24, BL, "noir", 1, 0.08)
    for lab, x, y, t0 in CTRL:
        coche(c, lab, x - 1150 * o, y, ent(t, t0, 0.4, 2.4), 36)
        etincelles(c, x - 120, y, t, t0 + 0.1, 8, 90, VERT)


# ─────────────────────────────────────────── S12 · on livre jusqu'à vous
T12 = TW(99) - 0.1


def s12(c, t):
    if t < T11 - 0.05 or t > T12 + 0.5: return
    u = ent(t, T11 + 0.02, 0.5, 1.2); o = prog(t, T12, 0.4, entree)
    with Espace(c, 540, 1000, rx=mix(-30, 8, u), s=mix(1.25, 1, u) * mix(1, 0.8, o), tx=1150 * o):
        with Calque(c, borne(u * 3)):
            vers = carte_monde(c, 540, 1000, 980)
            pa, pc = vers(PARIS_I), vers(CANTON_I)
            ctrl = ((pa[0] + pc[0]) / 2, min(pa[1], pc[1]) - 280)
            ua = prog(t, TW(95) - 0.1, TW(98) - TW(95) + 0.15, entreeSortie)
            courbe(c, pc, ctrl, pa, 0, 1, INK, 4, 0.25, [12, 12])
            courbe(c, pc, ctrl, pa, 0, ua, INK, 7)
            epingle(c, pc[0], pc[1], "Chine", 1.0, INK, "CN", 70, 26)
            if 0 < ua < 1:
                hx, hy = bez(pc, ctrl, pa, ua)
                carton(c, hx, hy - 10, 110, 0, 1, 12 * math.sin(t * 8))
            f = ent(t, TW(98) - 0.06, 0.42, 2.0)
            onde(c, pa[0], pa[1], t, TW(98), 20, 200, VERT, 7, 0.7)
            epingle(c, pa[0], pa[1], "Votre boutique", f, VERT, "FR", 100, 30)
    confettis(c, 300, 760, t, TW(98) + 0.02, 22, 330, 3, cols=[INK, VERT, MINT, ROSE, "#C9B79C"])
    pilule(c, "Livré", 540 + 1150 * o, 1440, ent(t, TW(96) - 0.05, 0.4, 2.4), 32, INK, BL, "truck", -3)


# ─────────────────────────────────────────── S13 · tester, mesurer, relancer ce qui se vend
T13 = TW(113) - 0.12
BARRES = [(270, "#C9B79C", 170), (450, "#2B2B2B", 110), (630, "#B5523B", 250), (810, "#7A8B6F", 80)]
T_CLIC = TW(110) + 0.02


def s13(c, t):
    if t < T12 - 0.05 or t > T13 + 0.5: return
    u = ent(t, T12 + 0.02, 0.5, 1.3); o = prog(t, T13, 0.42, entree)
    best = prog(t, TW(107) - 0.08, 0.5, lambda v: rebond(v, 1.3))
    relance = prog(t, T_CLIC + 0.1, 0.6, lambda v: rebond(v, 1.4))
    base = 1180
    with Espace(c, 540, 900, rx=mix(35, 5, u), ry=2 * math.sin(t * 1.2), s=mix(0.5, 1, u) * mix(1, 0.8, o), tx=-1150 * o):
        with Calque(c, borne(u * 3)):
            carte_blanche(c, 120, 560, 840, 700, 44)
            texte(c, "VOS VENTES", 170, 600, 34, INK, "archivo", track=0.04)
            pilule(c, "Test", 820, 624, ent(t, TW(100) - 0.08, 0.4, 2.4) * (1 - best), 24, "#F1EFEC", INK, "flask-conical" if False else "eye")
            for k in range(1, 4): trait(c, 170, base - k * 130, 910, base - k * 130, "#ECEAE6", 2)
            for k, (x, col, hm) in enumerate(BARRES):
                a = ent(t, TW(100) - 0.06 + 0.06 * k, 0.36, 2.0)
                if a <= 0: continue
                m = prog(t, TW(102) - 0.05 + 0.1 * k, 0.45, lambda v: rebond(v, 1.6))
                h = mix(50, hm, m) * a
                if k == 2: h = mix(h, 470, best) + 30 * relance * (0.5 + 0.5 * math.sin((t - T_CLIC) * 8)) * (1 - prog(t, T_CLIC + 0.8, 0.5))
                al = 1 - 0.65 * best * (0 if k == 2 else 1)
                with Calque(c, al):
                    if k == 2 and best > 0: lueur(c, x, base - h / 2, 200, MINT, 0.6 * best)
                    rrect(c, x - 55, base - h, 110, h, 18, VERT if (k == 2 and best > 0.5) else col)
                    disque(c, x, base + 40, 22, col)
    pilule(c, "Best-seller", 630 - 1150 * o, mix(1180, 640, borne(best)) - 40, best * (1 - o), 30, VERT, BL, "flame", -4)
    # le bouton « relancer la production »
    b = ent(t, TW(108) - 0.1, 0.42, 1.8) * (1 - o)
    if b > 0:
        p = 1 - 0.07 * math.sin(math.pi * borne((t - T_CLIC) / 0.18)) if T_CLIC <= t <= T_CLIC + 0.18 else 1
        c.save(); c.translate(540 - 1150 * o, 1380); c.scale(mix(0.4, 1, b) * p, mix(0.4, 1, b) * p)
        with Calque(c, borne(b * 2)):
            if relance > 0: lueur(c, 0, 0, 420, MINT, 0.5 * relance)
            rrect(c, -330, -64, 660, 128, 64, INK, 1, (16, 40, 0.28))
            icone(c, "factory", -252, 0, 56, BL, 2.4)
            texte_centre(c, "Relancer la production", 30, 0, 38, BL, "noir")
        c.restore()
    # le curseur
    cu = prog(t, TW(108) + 0.1, T_CLIC - TW(108) - 0.1, entreeSortie)
    if cu > 0 and t < T13:
        cx, cy = mix(980, 850, cu), mix(1650, 1420, cu)
        icone(c, "mouse-pointer-click", cx, cy, 80, INK, 2.4)
        onde(c, 820, 1385, t, T_CLIC, 20, 130, INK, 5, 0.5)
    # les colis repartent vers la barre
    for k in range(3):
        tk = T_CLIC + 0.12 + 0.1 * k
        a = prog(t, tk, 0.45, sortie)
        if 0 < a < 1:
            x, y = bez((540, 1380), (300 + 200 * k, 1000), (630, mix(1180, 640, borne(best)) + 40), a)
            carton(c, x, y, 90, 0, 1 - a ** 4, 20 * a)
    confettis(c, 630, 640, t, TW(112), 26, 380, 7, cols=[INK, VERT, MINT, ROSE, "#C9B79C"])


# ─────────────────────────────────────────── S14 · l'agilité des géants, à la taille de votre boutique
T14 = TW(122) - 0.12
T_RED = TW(117) - 0.05


def tour(c, cx, base, w, h, t):
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(cx - w / 2, 0), skia.Point(cx + w / 2, 0)], [hexa("#3A3A3A"), hexa("#0E0E0E"), hexa("#262626")], [0, 0.6, 1]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, base - h, w, h), 18, 18), g)
    rrect(c, cx - w * 0.3, base - h - 60, w * 0.6, 70, 12, "#1A1A1A")
    trait(c, cx, base - h - 60, cx, base - h - 170, "#1A1A1A", 8)
    disque(c, cx, base - h - 175, 10, ROUGE, 0.5 + 0.5 * (int(t * 3) % 2))
    nx, ny = 5, int(h / 70)
    for j in range(ny):
        for i in range(nx):
            on = (i * 7 + j * 13 + int(t * 5)) % 9 < 6
            rrect(c, cx - w / 2 + 26 + i * (w - 52) / nx, base - h + 30 + j * 70, (w - 52) / nx - 16, 36, 6, MINT if on else "#3C3C3C", 0.9)


def s14(c, t):
    if t < T13 - 0.05 or t > T14 + 0.5: return
    u = ent(t, T13 + 0.02, 0.6, 1.2); o = prog(t, T14, 0.42, entree)
    red = prog(t, T_RED, 0.5, entreeSortie)
    s = mix(1, 0.3, red)
    base = 1460
    if red < 1:
        with Espace(c, 540, base, rx=mix(-25, -6, u), s=s * mix(0.6, 1, u), ty=mix(900, 0, u)):
            with Calque(c, borne(u * 3) * (1 - prog(t, T_RED + 0.3, 0.2))):
                ombre_sol(c, 540, base, 320, 40, 0.2)
                tour(c, 540, base, 420, 900, t)
    etincelles(c, 540, 1020, t, TW(121) - 0.05, 12, 420, INK)
    # la boutique
    b = prog(t, T_RED + 0.3, 0.45, lambda v: rebond(v, 1.8))
    if b > 0:
        with Espace(c, 540, 1020, ry=-8 + 3 * math.sin(t * 1.4), s=mix(0.3, 1, b) * mix(1, 0.8, o), tx=-1150 * o):
            with Calque(c, borne(b * 2)):
                carte_blanche(c, 330, 800, 420, 460, 48)
                icone(c, "store", 540, 980, 190, INK, 1.8)
                titre(c, "VOTRE BOUTIQUE", 540, 1170, 34, INK, 1, 0.04)
    # l'éclair (l'agilité), qui passe de la tour à la boutique
    z = ent(t, TW(113) - 0.06, 0.4, 2.6) * (1 - o)
    if z > 0:
        zx = mix(760, 720, red); zy = mix(560, 840, red) if red > 0 else 560
        zx -= 1150 * o
        c.save(); c.translate(zx, zy); c.scale(z * battement(t, TW(121), 0.25, 0.4), z * battement(t, TW(121), 0.25, 0.4)); c.rotate(-8)
        lueur(c, 0, 0, 180, MINT, 0.7)
        disque(c, 0, 0, 74, MINT, 1, (10, 26, 0.22)); icone(c, "zap", 0, 0, 80, INK, 2.8)
        c.restore()


# ─────────────────────────────────────────── S15 · culture produit française + puissance industrielle chinoise
T15 = TW(130) - 0.08
T_FUS = T15 - 0.3


def s15(c, t):
    if t < T14 - 0.05 or t > T15 + 0.3: return
    f = prog(t, T_FUS, 0.3, entree)
    for j, (cx, t0, lab, pays) in enumerate([(285, T14 + 0.02, "CULTURE PRODUIT", "FR"), (795, TW(126) - 0.1, "PUISSANCE INDUSTRIELLE", "CN")]):
        u = ent(t, t0, 0.5, 1.3)
        if u <= 0: continue
        x = mix(cx, 540, f)
        with Espace(c, x, 990, ry=mix(60 if j == 0 else -60, 8 if j == 0 else -8, u) + 2 * math.sin(t * 1.3 + j), s=mix(0.5, 1, u) * mix(1, 0.6, f),
                    tx=mix(-500 if j == 0 else 500, 0, u)):
            with Calque(c, borne(u * 3)):
                carte_blanche(c, x - 235, 690, 470, 620, 40)
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 222, 703, 444, 470), 30, 30), True)
                g = skia.Paint(AntiAlias=True)
                g.setShader(skia.GradientShader.MakeLinear([skia.Point(x - 222, 703), skia.Point(x + 222, 1173)], [hexa("#CFCBC5"), hexa("#E6E3DE")]))
                c.drawRect(skia.Rect.MakeXYWH(x - 222, 703, 444, 470), g)
                if j == 0:
                    image_cover(c, "europe", x - 222, 703, 444, 470, 1.35, 0.32, 0.62)
                else:
                    image_cover(c, "chine", x - 222, 703, 444, 470, 1.0, 0.62, 0.5)
                c.restore()
                if j == 0:
                    epingle(c, x - 10, 1000, "Paris", ent(t, TW(124) - 0.05, 0.4, 2.0), INK, None, 60, 26)
                else:
                    v = ent(t, TW(128) - 0.1, 0.42, 2.0)
                    if v > 0:
                        c.save(); c.translate(x + 110, 1070); c.scale(v, v)
                        disque(c, 0, 0, 98, BL, 1, (10, 26, 0.25))
                        video(c, "rushes/machines", -90, -90, 180, 180, t - TW(128) + 1, 1.2, True, 90)
                        c.restore()
                drapeau(c, pays, x - 200, 1200, 66, 44, 8)
                T = ajuste(lab, 330, 30, "archivo")
                texte(c, lab, x - 120, 1222 - hauteurLigne(T, "archivo") / 2 + 2, T, INK, "archivo", track=0.02)
    a = ent(t, TW(126) - 0.08, 0.4, 2.6) * (1 - f)
    if a > 0:
        c.save(); c.translate(540, 990); c.scale(a, a); c.rotate(90 * (1 - a))
        disque(c, 0, 0, 52, INK, 1, (10, 26, 0.3)); titre(c, "+", 0, 2, 80, BL)
        c.restore()
    if f > 0.6: onde(c, 540, 990, t, T_FUS + 0.28, 60, 600, INK, 10, 0.5)


# ─────────────────────────────────────────── S16 · MONARQUE, carton final
T_L2 = TW(130) - 0.08
T_L2R = TW(131) - 0.12
MOT = "monarqueprod.com"
T_TAPE = [TW(135) - 0.05 + k * (TW(138) + 0.25 - TW(135)) / len(MOT) for k in range(len(MOT))]


def s16(c, t):
    if t < T_L2 - 0.05: return
    r = disque_noir(c, t, T_L2, T_L2R)
    u = prog(t, T_L2 + 0.16, 0.36, lambda v: rebond(v, 1.6))
    v = prog(t, T_L2R, 0.42, entreeSortie)
    lw = mix(1.5, 1, u) * mix(LOGO_W, 780, v)
    ly = mix(1000, 760, v)
    if v < 1: logo(c, 540, ly, lw, True, borne(u * 3) * (1 - v))
    if v > 0: logo(c, 540, ly, lw, False, v)
    if t < T_L2R: return
    a = prog(t, T_L2R + 0.25, 0.4, sortie)
    texte_centre(c, "Centrale d'achat textile française basée en Chine", 540, 880 + mix(16, 0, a), 30, GR, "fort", a, 0)
    b = ent(t, TW(131) - 0.02, 0.45, 1.8)
    if b > 0:
        T_C = TW(132) + 0.1
        p = 1 - 0.06 * math.sin(math.pi * borne((t - T_C) / 0.18)) if T_C <= t <= T_C + 0.18 else 1 + 0.025 * max(0, math.sin((t - T_C) * 5)) * (t > T_C + 0.3)
        c.save(); c.translate(540, 1040); c.scale(mix(0.4, 1, b) * p, mix(0.4, 1, b) * p)
        with Calque(c, borne(b * 2)):
            rrect(c, -340, -66, 680, 132, 66, INK, 1, (18, 44, 0.3))
            texte_centre(c, "Présenter mon projet", -30, 0, 40, BL, "noir")
            disque(c, 270, 0, 44, BL); icone(c, "arrow-right", 270, 0, 46, INK, 3)
        c.restore()
        cu = prog(t, TW(131) + 0.2, T_C - TW(131) - 0.2, entreeSortie)
        if t < T_C + 0.7:
            icone(c, "mouse-pointer-click", mix(920, 820, cu), mix(1400, 1090, cu), 76, INK, 2.4, borne(cu * 3) * (1 - prog(t, T_C + 0.4, 0.3)))
    n = sum(1 for tt in T_TAPE if t >= tt)
    if n > 0:
        txt = MOT[:n]
        w = largeur(MOT, 56, "archivo", 0)
        texte(c, txt, 540 - w / 2, 1190, 56, INK, "archivo", track=0)
        if n < len(MOT) and (t * 3) % 1 < 0.6:
            rrect(c, 540 - w / 2 + largeur(txt, 56, "archivo", 0) + 4, 1196, 5, 60, 2, INK)
    e = prog(t, T_TAPE[-1] + 0.15, 0.4, sortie)
    texte_centre(c, "contact@monarqueprod.fr", 540, 1310 + mix(14, 0, e), 30, GR, "demi", e, 0)
    return r


# ─────────────────────────────────────────── sons
son(0.0, "whoosh_long", -10)
for k in range(10): son(0.05 + k * 0.17, "tick", -17)
son(T_LEV, "croc", -8); son(T_LEV + 0.05, "whoosh_court", -11)
for k in range(10): son(T_LEV + 0.1 + k * 0.08, "tick", -15)
for k, ts in enumerate(T_STOP): son(ts, "impact_doux" if k < 2 else "impact", -8); son(ts + 0.02, "clic", -10)
son(TW(11) + 0.08, "tampon", -7)
son(T1, "whoosh", -9); son(T1 + 0.1, "pop", -12)
for k in range(5): son(TW(13) + 0.07 * k, "blip", -16)
son(TW(15) - 0.12, "swipe", -12)
for tt in T_MOIS[1:]: son(tt, "tick", -11)
son(TW(19) + 0.02, "tampon", -7)
son(T2, "whoosh", -9); son(TW(22) - 0.08, "ding", -12); son(TW(25), "tampon", -6); son(TW(25) + 0.02, "impact", -10)
son(TW(26) - 0.15, "swipe", -12)
for (_, _, _, t0) in CARTONS: son(t0 + 0.28, "impact_doux", -7)
son(TW(31) - 0.05, "montee", -15); son(TW(33) - 0.08, "pop", -10); son(TW(33), "croc", -11)
son(T3, "whoosh_long", -9); son(TW(37) - 0.06, "pop", -10); son(TW(38) - 0.08, "blip", -11)
son(TW(39) - 0.08, "message_in", -8); son(TW(40) - 0.02, "message_in", -8)
son(TW(41) - 0.2, "whoosh_court", -11)
for i in range(4): son(TW(41) - 0.06 + 0.08 * i, "pop", -13)
for i in range(3): son(TW(42) - 0.05 + 0.12 * i, "ching", -12)
son(T4, "whoosh", -10); son(TW(44) - 0.05, "check", -10); son(TW(45) - 0.12, "whoosh_court", -11)
son(TW(48) - 0.08, "impact", -8)
for k in range(3): son(TW(51) - 0.05 + 0.1 * k, "blip", -12)
son(TW(51) + 0.12, "tampon", -7)
son(T_M - 0.25, "montee", -12); son(T_M + 0.16, "impact", -4); son(T_M + 0.18, "verre", -8)
son(T_MR, "whoosh_long", -9); son(TW(58) - 0.08, "pop", -10); son(TW(58) + 0.05, "whoosh_bas", -12)
son(TW(59) - 0.08, "pop", -11); son(TW(61) - 0.06, "ding", -10)
son(T6, "whoosh", -9)
for t0 in (TW(63) - 0.08, TW(64) - 0.02, TW(66) - 0.08): son(t0, "pop", -10)
son(TW(66) - 0.05, "whoosh_bas", -13)
son(T7, "whoosh", -10); son(TW(68) - 0.1, "pop", -11)
for (_, _, tf) in DEV: son(tf, "impact_doux", -9); son(tf + 0.02, "verre", -13)
son(T8, "whoosh", -10)
for i in range(3): son(T8 + 0.03 + 0.08 * i, "swipe", -15)
son(TW(75) - 0.1, "montee", -16); son(TW(77) - 0.04, "check", -8); son(TW(77), "impact_doux", -10)
son(T9, "whoosh", -10)
for (_, _, tm, _, _) in NEGO: son(tm - 0.18, "swipe", -11); son(tm + 0.38, "check", -10)
son(T10, "whoosh_long", -9)
for (_, _, _, t0) in CTRL: son(t0, "check", -8); son(t0 + 0.1, "blip", -13)
son(T11, "whoosh", -10); son(TW(95) - 0.1, "whoosh_bas", -11); son(TW(98) - 0.06, "ding", -9); son(TW(98), "ching", -11)
son(T12, "whoosh", -10)
for k in range(4): son(TW(100) - 0.06 + 0.06 * k, "pop", -13)
for k in range(4): son(TW(102) - 0.05 + 0.1 * k, "tick", -10)
son(TW(107) - 0.08, "montee", -12); son(TW(107) + 0.25, "ching", -9)
son(TW(108) - 0.1, "pop", -11); son(T_CLIC, "clic", -6)
for k in range(3): son(T_CLIC + 0.12 + 0.1 * k, "whoosh_court", -13)
son(TW(112), "ding", -10)
son(T13, "whoosh_bas", -9); son(T13 + 0.4, "impact", -10); son(TW(113) - 0.06, "pop", -9)
son(T_RED, "whoosh_long", -10); son(T_RED + 0.3, "impact_doux", -8); son(TW(121) - 0.05, "ching", -10)
son(T14, "whoosh", -10); son(TW(124) - 0.05, "pop", -12); son(TW(126) - 0.1, "whoosh", -11); son(TW(126) - 0.08, "pop", -10)
son(TW(128) - 0.1, "blip", -11); son(T_FUS, "whoosh_court", -9); son(T_FUS + 0.28, "impact", -6)
son(T_L2 + 0.16, "impact", -4); son(T_L2 + 0.18, "verre", -8)
son(T_L2R, "whoosh_long", -10); son(TW(131) - 0.02, "pop", -9); son(TW(132) + 0.1, "clic", -6)
for tt in T_TAPE: son(tt, "frappe", -13)
son(T_TAPE[-1] + 0.15, "ding", -10)

for a, b in [(T_LEV, T_LEV + 0.3), (T1, T1 + 0.45), (T2, T2 + 0.45), (TW(26) - 0.15, TW(26) + 0.3), (T3, T3 + 0.5), (TW(41) - 0.2, TW(41) + 0.3),
             (T4, T4 + 0.45), (T5 - 0.05, T5 + 0.25), (T_MR, T_MR + 0.45), (T6, T6 + 0.45), (T7, T7 + 0.45), (T8, T8 + 0.45), (T9, T9 + 0.45),
             (T10, T10 + 0.5), (T11, T11 + 0.45), (T12, T12 + 0.45), (T13, T13 + 0.5), (T_RED, T_RED + 0.5), (T14, T14 + 0.45),
             (T_FUS, T_FUS + 0.3), (T_L2R, T_L2R + 0.45)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_STOP[2], ROUGE, 0.12), (TW(25), ROUGE, 0.1), (TW(48), ROUGE, 0.1), (T_M + 0.16, "#FFFFFF", 0.12), (TW(77), MINT, 0.18),
                    (TW(98), MINT, 0.15), (TW(107), MINT, 0.2), (T_FUS + 0.28, "#FFFFFF", 0.5), (T_L2 + 0.16, "#FFFFFF", 0.12)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    fond_mq(c, t)
    r1 = r2 = 0
    if t < T_L2 + 0.35:
        s1(c, t); s2(c, t); s4(c, t); s5(c, t); s7(c, t); s8(c, t); s9(c, t); s10(c, t); s11(c, t); s12(c, t); s13(c, t)
        s14(c, t); s15(c, t)
        s0(c, t)
        r1 = s6(c, t) or 0
    r2 = s16(c, t) or 0
    K.dessine_eclairs(c, t)
    if t < T_L2 + 0.1:
        sombre = (T_M + 0.25 <= t <= T_MR + 0.15) or (t >= T_L2 + 0.25)
        SOUS.dessine(c, t, BL if sombre else INK)
