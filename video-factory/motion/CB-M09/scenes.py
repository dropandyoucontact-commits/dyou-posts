"""CB-M09 « Surron » — vidéo ORGANIQUE (≈ 40 s), même format que CB-M06 / CB-M08.

Chiffres de Youssef (13/10/2026) : en Chine la plus petite 1 500 €, la plus grosse 3 600 € ; transport 400-600 € ;
revente en France 3 000 € et 6 000 € ; Surron = marque chinoise, produits officiels ; distribuer en France, Belgique, Europe.
Médias : rush 16:9 de Youssef (Surron + fille cagoulée) en cadre dans le hook, photo du showroom Surron (logo découpé
du mur), Surron détourée de la banque. Voix : « Sur-Ronne » dans la prise pour la prononciation, « Surron » à l'écran.
"""
import math, pathlib, re, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import moteur

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 2.0, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
ROUGE, VERT, INK, BL = C["rouge"], C["vert"], C["ink"], C["blanc"]
MARQUES.update({"tiktok": "#000000", "instagram": "#E4405F", "klarna": "#FFB3C7"})
VINTED, ORANGE = "#09B1BA", "#F28C28"

# ─────────────────────────────────────────── sous-titres
AFFICHE = {1: "Surron", 92: "Surron,", 20: "1 500 €.", 27: "3 600 €.", 37: "400", 40: "600 €.", 53: "1 500,", 58: "3 000 €.",
           64: "3 600,", 71: "6 000 €.", 133: "ChinaBook."}
CACHES = {21, 22, 23, 28, 29, 30, 38, 41, 42, 54, 55, 59, 60, 65, 66, 67, 72}
VERTS = {1, 20, 27, 58, 71, 80, 92, 101, 105, 109, 116, 118, 123, 133, 134, 140}
ROUGES = {37, 40, 91}
COUPES = {3, 10, 17, 24, 31, 35, 43, 50, 56, 61, 68, 73, 77, 86, 92, 97, 106, 115, 119, 124, 134, 137}


def _blocs():
    blocs, cour = [], []
    for m in K.mots:
        i = m["i"]
        if i in CACHES: continue
        mot = AFFICHE.get(i, m["w"]).replace("'", "’")
        prec = cour[-1][1] if cour else ""
        if cour and (i in COUPES or len(cour) >= 6 or re.search(r"[.?]$", prec) or (re.search(r"[,:]$", prec) and len(cour) >= 3)):
            blocs.append(cour); cour = []
        cour.append((i, mot, "g" if i in VERTS else ("r" if i in ROUGES else "")))
    blocs.append(cour)
    net = []
    for bl in blocs:
        if net and len(bl) == 1 and bl[0][0] not in COUPES and len(net[-1]) <= 6: net[-1] = net[-1] + bl
        else: net.append(bl)
    return net


SOUS = SousTitres(K, _blocs())


def fen(i0, i1, a=0.14, b=0.02):
    return (TW(i0) - a if i0 else 0.0, TW(i1) - b)


H, S1, S2, S3 = fen(0, 17), fen(17, 31), fen(31, 43), fen(43, 73)
S4, S5, S6 = fen(73, 86), fen(86, 106), fen(106, 124)
S7 = (TW(124) - 0.14, TW(133) + 0.3)


class _Sc:
    def __init__(self, c, tr):
        self.c, self.tr = c, tr
    def __enter__(self):
        dx, dy, s, al = self.tr
        if al < 0.999: self.c.saveLayerAlpha(None, int(255 * borne(al)))
        else: self.c.save()
        self.c.translate(540 + dx, 1080 + dy); self.c.scale(s, s); self.c.translate(-540, -1080)
        return self.c
    def __exit__(self, *a):
        self.c.restore()


def scene(c, t, S, ek="gauche", sk="gauche", de=0.28, ds=0.22):
    a, b = S
    if not (a <= t <= b): return None
    ue = prog(t, a, de, sortie) if ek else 1.0
    us = prog(t, b - ds, ds, entree) if sk else 0.0
    dx = dy = 0.0; s = 1.0; al = 1.0
    if ek == "gauche": dx += 1300 * (1 - ue)
    elif ek == "bas": dy += 1500 * (1 - ue)
    elif ek == "zoom": s *= mix(0.55, 1, ue); al *= ue
    if sk == "gauche": dx -= 1300 * us
    elif sk == "haut": dy -= 1500 * us
    elif sk == "zoom": s *= mix(1, 1.9, us); al *= (1 - us)
    return _Sc(c, (dx, dy, s, al))


def tel(c, cx, cy, ecran, w=480, h=960, alpha=1.0, **espace):
    with Espace(c, cx, cy, **espace):
        telephone(c, cx - w / 2, cy - h / 2, w, h, ecran, alpha)


def apparait(t, t0, s=1.9, d=0.34):
    return prog(t, t0, d, lambda v: rebond(v, s))


def fenetre(t, a, b, d=0.25):
    """opacité d'un sous-plan visible de a à b"""
    return prog(t, a, d, sortie) * (1 - prog(t, b - d, d, entree))


# ─────────────────────────────────────────── petits éléments
def basket(c, nom, cx, cy, w, alpha=1.0, rot=0.0, ombre=True):
    if alpha <= 0.01: return
    iw, ih = taille_img(f"saucony/{nom}"); h = w * ih / iw
    c.save(); c.translate(cx, cy); c.rotate(rot)
    if ombre: ombre_sol(c, 0, h * 0.45, w * 0.42, h * 0.08, 0.2 * alpha)
    image(c, f"saucony/{nom}", -w / 2, -h / 2, w, alpha)
    c.restore()


def etiquette(c, cx, cy, w, txt, u, coul=INK, rot=0.0, verrou=0.0, sous=None, fond_=BL):
    """étiquette de prix : carte trouée + ficelle ; verrou > 0 : cadenas posé dessus"""
    if u <= 0.01: return
    h = w * 0.56
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
    with Calque(c, borne(u * 2)):
        pq = skia.Path()
        pq.moveTo(-w / 2 + h * 0.32, -h / 2); pq.lineTo(w / 2 - 22, -h / 2); pq.quadTo(w / 2, -h / 2, w / 2, -h / 2 + 22)
        pq.lineTo(w / 2, h / 2 - 22); pq.quadTo(w / 2, h / 2, w / 2 - 22, h / 2); pq.lineTo(-w / 2 + h * 0.32, h / 2)
        pq.lineTo(-w / 2, 0); pq.close()
        p = peinture(fond_); p.setImageFilter(skia.ImageFilters.DropShadow(0, 22, 26, 26, hexa(INK, 0.22))); c.drawPath(pq, p)
        c.drawPath(pq, peinture(coul, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        disque(c, -w / 2 + h * 0.3, 0, h * 0.08, "#E6EBE8"); anneau(c, -w / 2 + h * 0.3, 0, h * 0.08, coul, 4)
        T = ajuste(txt, w * 0.62, h * 0.5)
        texte_centre(c, txt, w * 0.1, -h * 0.04 if sous else 0, T, coul, "noir")
        if sous: texte_centre(c, sous, w * 0.1, h * 0.28, h * 0.13, C["gris"], "fort", 1, 0.02)
        if verrou > 0:
            c.save(); c.translate(w * 0.36, -h * 0.42); c.rotate(12); c.scale(verrou, verrou)
            disque(c, 0, 0, h * 0.2, ROUGE, 1, (8, 20, 0.25)); icone(c, "lock", 0, 0, h * 0.22, BL, 2.8)
            c.restore()
    c.restore()


def tuile(c, nom, cx, cy, taille, u=1.0, rot=0.0):
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
    with Calque(c, borne(u * 2)):
        r = taille * 0.24
        if nom == "vinted":
            rrect(c, -taille / 2, -taille / 2, taille, taille, r, VINTED, 1, (10, 26, 0.18))
            texte_centre(c, "Vinted", 0, 0, ajuste("Vinted", taille * 0.82, taille * 0.3), BL, "noir", 1, -0.02)
        elif nom == "ebay":
            rrect(c, -taille / 2, -taille / 2, taille, taille, r, BL, 1, (10, 26, 0.18), "#E7EBE9", 3)
            T = taille * 0.34; x = -largeur("ebay", T, "noir", -0.06) / 2
            for l, col in zip("ebay", ["#E53238", "#0064D2", "#F5AF02", "#86B817"]):
                texte(c, l, x, -hauteurLigne(T) / 2, T, col, "noir", track=-0.06); x += largeur(l, T, "noir", -0.06)
        elif nom == "klarna":
            rrect(c, -taille / 2, -taille / 2, taille, taille, r, MARQUES["klarna"], 1, (10, 26, 0.18))
            logo_glyphe(c, "klarna", 0, 0, taille * 0.5, INK)
        else:
            logo_app(c, nom, 0, 0, taille)
    c.restore()


def billet(c, cx, cy, w, rot, alpha=1.0):
    h = w * 0.52
    c.save(); c.translate(cx, cy); c.rotate(rot)
    rrect(c, -w / 2, -h / 2, w, h, 12, ORANGE, alpha, (8, 20, 0.15))
    rrect(c, -w / 2 + 10, -h / 2 + 10, w - 20, h - 20, 8, "#F7A85A", alpha)
    texte_centre(c, "€", -w * 0.22, 0, h * 0.55, "#7A3B06", "noir", alpha)
    disque(c, w * 0.22, 0, h * 0.26, "#E07A14", alpha)
    c.restore()


def compteur(t, t0, t1, v):
    return int(round(v * prog(t, t0, max(0.05, t1 - t0), sortie)))


def euros(n):
    return f"{n:,}".replace(",", " ") + " €"


def coche(c, cx, cy, r, u, couleur=None):
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.scale(u, u)
    disque(c, 0, 0, r, couleur or VERT, 1.0, (8, 20, 0.2)); icone(c, "check", 0, 0, r * 1.1, BL, 3.6)
    c.restore()


def signet(c, cx, cy, taille, rempli, alpha=1.0):
    w, h = taille * 0.62, taille * 0.8
    pq = skia.Path()
    pq.moveTo(cx - w / 2, cy - h / 2); pq.lineTo(cx + w / 2, cy - h / 2); pq.lineTo(cx + w / 2, cy + h / 2)
    pq.lineTo(cx, cy + h / 2 - w * 0.42); pq.lineTo(cx - w / 2, cy + h / 2); pq.close()
    if rempli: c.drawPath(pq, peinture("#FACE15", alpha))
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=taille * 0.08, StrokeJoin=skia.Paint.kRound_Join,
                   Color=hexa(INK if rempli else BL, alpha))
    c.drawPath(pq, p)


def pil(c, label, cx, cy, taille, fond_, texte_c, t0, t, rot=0.0, ic=None, fin=None):
    u = apparait(t, t0)
    if fin is not None: u *= 1 - prog(t, fin, 0.2, entree)
    if u > 0: pastille_rot(c, label, cx, cy, taille, fond_, texte_c, rot, mix(0.3, 1, u), borne(u * 2), ic, (14, 32, 0.25))



# ─────────────────────────────────────────── la Surron
YEL = "#F2B705"
GZ, PAR, BRU = (113.26, 23.13), (2.35, 48.86), (4.35, 50.85)
EUROPE = [(13.4, 52.5), (12.5, 41.9), (-3.7, 40.4), (4.9, 52.4), (16.4, 48.2), (21.0, 52.2), (-9.1, 38.7), (10.0, 53.6), (8.5, 47.4), (14.4, 50.1)]
G = Globe()


def moto(c, cx, cy, w, alpha=1.0, rot=0.0, ombre=True):
    if alpha <= 0.01: return
    nom = "produits/mobilite/moto-electrique"
    iw, ih = taille_img(nom); h = w * ih / iw
    c.save(); c.translate(cx, cy); c.rotate(rot)
    if ombre: ombre_sol(c, 0, h * 0.47, w * 0.44, h * 0.06, 0.22 * alpha)
    image(c, nom, -w / 2, -h / 2, w, alpha)
    c.restore()


def plaque(c, cx, cy, w, u, rot=0.0):
    """le vrai logo Surron, découpé du mur du showroom"""
    if u <= 0: return
    iw, ih = taille_img("logo-surron"); h = w * ih / iw
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
    with Calque(c, borne(u * 2)):
        carte(c, -w / 2 - 10, -h / 2 - 10, w + 20, h + 20, 22, "#3C3E42", 1, (14, 34, 0.3))
        image_cover(c, "logo-surron", -w / 2, -h / 2, w, h, 1.0, 0.5, 0.5, 14)
    c.restore()


def drapeau_carte(c, pays, cx, cy, w, u, rot=0.0):
    if u <= 0: return
    h = w * 0.66
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(u, u)
    rrect(c, -w / 2 - 12, -h / 2 - 12, w + 24, h + 24, 18, BL, 1, (12, 30, 0.25)); drapeau(c, pays, -w / 2, -h / 2, w, h, 10)
    c.restore()


# ─────────────────────────────────────────── H · une Surron neuve, combien en Chine ? (rush 16:9 en cadre)
def h(c, t):
    sc = scene(c, t, H, None, "gauche")
    if sc is None: return
    with sc:
        ue = prog(t, 0, 0.5, sortie)
        sx, sy = secousse(t, TW(5) - 0.05, 10, 0.3)
        cx, cy, w, hh = 540 + sx, 920 + sy, 960, 540
        with Espace(c, cx, cy, ry=mix(-14, -6, ue) + 2 * math.sin(t * 1.8), rx=4, s=mix(1.08, 1, ue)):
            carte(c, cx - w / 2 - 14, cy - hh / 2 - 14, w + 28, hh + 28, 40, BL, 1, (30, 70, 0.25))
            video(c, "surron-hook", cx - w / 2, cy - hh / 2, w, hh, t * 0.9, 1.0, True, 28)
            yb = cy + hh / 2 - 74
            rrect(c, cx - w / 2 + 24, yb, 150, 50, 25, ROUGE, 0.95)
            disque(c, cx - w / 2 + 50, yb + 25, 8, BL, 0.4 + 0.6 * (int(t * 3) % 2))
            texte_centre(c, "CHINE", cx - w / 2 + 112, yb + 25, 22, BL, "noir", 1, 0.06)
        plaque(c, 290, 575, 330, 1.0 if t < 0.05 else apparait(t, TW(1) - 0.1, 1.8, 0.36), -6)
        pil(c, "NEUVE", 850, 580, 44, VERT, BL, TW(2) - 0.08, t, 6, "sparkles")
        etiquette(c, 560, 1400, 560, "? €", apparait(t, TW(5) - 0.08, 1.8, 0.4), INK, -5)
        drapeau_carte(c, "CN", 230, 1290, 120, apparait(t, TW(9) - 0.08), -10)
        if t >= TW(10) - 0.1:
            u = apparait(t, TW(10) - 0.1, 2.0, 0.34)
            c.save(); c.translate(860, 1300); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
            disque(c, 0, 0, 96, INK, borne(u * 2), (16, 40, 0.3)); icone(c, "hand", 0, 0, 100, BL, 2.6, borne(u * 2))
            c.restore()
            pastille_rot(c, "RESTE LÀ", 860, 1450, 40, INK, BL, -4, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))


# ─────────────────────────────────────────── S1 · prix en Chine : la petite, la grosse
def s1(c, t):
    sc = scene(c, t, S1, "gauche", "gauche")
    if sc is None: return
    with sc:
        pil(c, "PRIX EN CHINE", 540, 640, 42, INK, BL, S1[0] + 0.1, t, -3)
        drapeau_carte(c, "CN", 820, 600, 90, apparait(t, S1[0] + 0.2), 8)
        for k, (x, y, w, t0, tp, prix, lab) in enumerate([(320, 880, 460, TW(17) - 0.05, TW(20) - 0.06, "1 500 €", "La petite"),
                                                         (640, 1220, 600, TW(24) - 0.05, TW(27) - 0.06, "3 600 €", "La grosse")]):
            u = apparait(t, t0, 1.5, 0.45)
            if u <= 0: continue
            moto(c, x, y + 8 * math.sin(t * 2 + k), w * mix(0.4, 1, u), borne(u * 2), [-3, 3][k])
            pastille_rot(c, lab, x - w * 0.28, y - w * 0.36, 34, BL, INK, -6, mix(0.3, 1, u), borne(u * 2), None, (12, 28, 0.2))
            etiquette(c, [770, 250][k], [860, 1180][k], [360, 400][k], prix, apparait(t, tp, 2.0, 0.36), VERT, [6, -5][k])


# ─────────────────────────────────────────── S2 · le transport Chine → France
def s2(c, t):
    sc = scene(c, t, S2, "zoom", "gauche", de=0.3)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1060, 410
        lon0, lat0 = cles(t, [(S2[0], 95), (TW(34), 58, entreeSortie)]), 38
        G.disque(c, cx, cy, R); G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2, 3: 1.3})
        G.repere(c, *GZ, cx, cy, R, lon0, lat0, "CHINE", INK, "CN", apparait(t, S2[0] + 0.15, 1.8, 0.4), 1.0, 70)
        G.repere(c, *PAR, cx, cy, R, lon0, lat0, "FRANCE", VERT, "FR", apparait(t, TW(34) - 0.08, 1.8, 0.4), 1.0, 80)
        pv = prog(t, TW(32) - 0.1, TW(35) - TW(32), entreeSortie)
        if pv > 0:
            G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, 1.0, "#CBD5CF", 5, 0.32, [2, 16])
            x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, pv, INK, 7, 0.32)
            if pv < 1:
                c.save(); c.translate(x_, y_); c.rotate(-15); disque(c, 0, 0, 44, INK, 1.0, (8, 20, 0.2)); icone(c, "ship", 0, 0, 48, BL, 2.4); c.restore()
        if t >= TW(37) - 0.1:
            u = apparait(t, TW(37) - 0.1, 1.8, 0.4)
            c.save(); c.translate(540, 1560); c.rotate(-3); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
            rrect(c, -330, -80, 660, 160, 80, ORANGE, borne(u * 2), (14, 34, 0.3))
            icone(c, "truck", -240, 0, 70, BL, 2.6, borne(u * 2))
            n6 = apparait(t, TW(40) - 0.06, 2.2, 0.3)
            texte_centre(c, "400 – 600 €" if n6 > 0.3 else "400 € …", 40, 0, 64, BL, "noir", borne(u * 2))
            c.restore()


# ─────────────────────────────────────────── S3 · en France : 3 000 € et 6 000 €
def ligne_revente(c, t, y, w_moto, achat, revente, t_achat, t_rev, v_rev, lab):
    u = apparait(t, t_achat - 0.12, 1.5, 0.45)
    if u <= 0: return
    with Calque(c, borne(u * 2)):
        c.save(); c.translate(mix(-400, 0, u), 0)
        carte(c, 70, y - 150, 940, 300, 50, BL, 1, (24, 56, 0.15))
        moto(c, 230, y + 10, w_moto, 1, -3, False)
        texte(c, lab, 110, y - 130, 28, C["gris"], "noir", track=0)
        texte_centre(c, achat, 520, y - 40, 50, C["grisClair"], "noir")
        drapeau(c, "CN", 490, y + 10, 60, 40, 6)
        trait(c, 600, y - 10, 690, y - 10, INK, 6); icone(c, "arrow-right", 700, y - 10, 46, INK, 3)
        r = apparait(t, t_rev - 0.06, 2.0, 0.4)
        c.save(); c.translate(850, y - 30); c.scale(mix(0.3, 1, r), mix(0.3, 1, r))
        n = int(v_rev * prog(t, t_rev - 0.06, 0.45, sortie)) if r > 0 else 0
        texte_centre(c, euros(n), 0, 0, 74, VERT, "noir", borne(r * 2))
        drapeau(c, "FR", -30, 50, 60, 40, 6)
        c.restore()
        c.restore()


def s3(c, t):
    sc = scene(c, t, S3, "gauche", "gauche")
    if sc is None: return
    with sc:
        pil(c, "REVENTE EN FRANCE", 540, 640, 42, VERT, BL, S3[0] + 0.1, t, -3, "trending-up")
        drapeau_carte(c, "FR", 900, 600, 90, apparait(t, TW(45) - 0.08), 8)
        if t < TW(50) - 0.05:
            u = apparait(t, TW(49) - 0.1, 2.0, 0.4)
            c.save(); c.translate(540, 1050); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
            disque(c, 0, 0, 150, INK, borne(u * 2), (16, 40, 0.3)); texte_centre(c, "? €", 0, 0, 120, BL, "noir", borne(u * 2))
            c.restore()
        ligne_revente(c, t, 950, 300, "1 500 €", "3 000 €", TW(51), TW(58), 3000, "LA PETITE")
        ligne_revente(c, t, 1300, 330, "3 600 €", "6 000 €", TW(62), TW(71), 6000, "LA GROSSE")
        confettis(c, 850, 920, t, TW(58) + 0.3, 20, 300, 3)
        confettis(c, 850, 1270, t, TW(71) + 0.3, 26, 360, 5)


# ─────────────────────────────────────────── S4 · même avec le transport, la marge
def barre_empilee(c, t, x, base, k_px, achat, total, lab, t0):
    u = prog(t, t0, 0.5, sortie)
    ha = achat * k_px * u
    ht = 500 * k_px * prog(t, t0 + 0.25, 0.4, sortie)
    hm = (total - achat - 500) * k_px * prog(t, TW(80) - 0.1, 0.5, lambda v: rebond(v, 1.3))
    w = 230
    rrect(c, x - w / 2, base - ha, w, ha, 14, "#C9D0CC")
    if ha > 60: texte_centre(c, "Chine", x, base - ha / 2, 30, INK, "noir")
    if ht > 2:
        rrect(c, x - w / 2, base - ha - ht, w, ht, 10, ORANGE)
        if ht > 30: texte_centre(c, "Transport", x, base - ha - ht / 2, 22, BL, "noir")
    if hm > 2:
        rrect(c, x - w / 2, base - ha - ht - hm, w, hm, 18, VERT)
        if hm > 80: texte_centre(c, "MARGE", x, base - ha - ht - hm / 2, 40, BL, "noir")
    texte_centre(c, lab, x, base + 46, 32, C["gris"], "noir")
    if hm > 2: texte_centre(c, euros(total), x, base - ha - ht - hm - 40, 40, VERT, "noir", prog(t, TW(80), 0.3))


def s4(c, t):
    sc = scene(c, t, S4, "gauche", "gauche")
    if sc is None: return
    with sc:
        carte(c, 110, 600, 860, 900, 56, BL, 1, (26, 60, 0.14))
        barre_empilee(c, t, 330, 1400, 0.095, 1500, 3000, "La petite", S4[0] + 0.1)
        barre_empilee(c, t, 750, 1400, 0.095, 3600, 6000, "La grosse", S4[0] + 0.25)
        tampon(c, "VRAIE MARGE", 400, 700, t, TW(80) + 0.05, 52, VERT, -5, "trending-up")
        etincelles(c, 750, 750, t, TW(80) + 0.3, 12, 260)


# ─────────────────────────────────────────── S5 · pas de la copie : marque chinoise, de l'officiel
def s5(c, t):
    sc = scene(c, t, S5, "gauche", "gauche")
    if sc is None: return
    with sc:
        # la copie barrée
        a = 1 - prog(t, TW(92) - 0.2, 0.25, entree)
        if a > 0:
            with Calque(c, a):
                u = apparait(t, S5[0] + 0.1, 1.6, 0.4)
                c.save(); c.translate(540, 1060); c.rotate(-4); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
                carte(c, -300, -300, 600, 600, 50, BL, 1, (24, 56, 0.18))
                moto(c, 0, -10, 420, 0.35, 0, False)
                texte_centre(c, "COPIE ?", 0, 210, 60, C["gris"], "noir")
                c.restore()
                tampon(c, "PAS DE COPIE", 540, 1060, t, TW(91) - 0.02, 60, ROUGE, -10, "x-circle")
        # le showroom officiel
        b = prog(t, TW(92) - 0.2, 0.35, sortie)
        if b > 0:
            tel(c, mix(1400, 600, b), 1180, lambda cc, x, y, d, e: image_cover(cc, "showroom-surron", x, y, d, e, 1.08 + 0.06 * prog(t, TW(92), 5, lin), 0.6, 0.45),
                ry=-8 + 2 * math.sin(t * 2), rz=2)
            plaque(c, 330, 690, 360, apparait(t, TW(92) - 0.05, 1.8, 0.36), -6)
            drapeau_carte(c, "CN", 230, 860, 110, apparait(t, TW(96) - 0.08), -8)
            pil(c, "MARQUE CHINOISE", 300, 1020, 34, INK, BL, TW(95) - 0.08, t, -5)
            tampon(c, "OFFICIEL", 300, 1300, t, TW(101), 58, VERT, -8, "badge-check")
            pil(c, "À LA SOURCE", 850, 1560, 40, VERT, BL, TW(104) - 0.05, t, 4, "map-pin")


# ─────────────────────────────────────────── S6 · distributeur : France, Belgique, toute l'Europe
def s6(c, t):
    sc = scene(c, t, S6, "zoom", "gauche", de=0.3)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1120, 430
        lon0, lat0 = cles(t, [(S6[0], 30), (TW(115), 8, entreeSortie)]), cles(t, [(S6[0], 40), (TW(115), 46, entreeSortie)])
        eu = prog(t, TW(122) - 0.1, 0.4, sortie)
        G.disque(c, cx, cy, R)
        G.terres(c, cx, cy, R, lon0, lat0, couleurs={3: VERT, 4: mix_hex("#A6CDB5", VERT, eu)}, grossir={3: 1.4, 4: 1 + 0.3 * eu})
        G.repere(c, *PAR, cx, cy, R, lon0, lat0, "FRANCE", INK, "FR", apparait(t, TW(116) - 0.08, 1.8, 0.4), 1.0, 90)
        G.repere(c, *BRU, cx, cy, R, lon0, lat0, "BELGIQUE", INK, "BE", apparait(t, TW(118) - 0.08, 1.8, 0.4), 1.0, 190)
        for k, p in enumerate(EUROPE):
            uk = apparait(t, TW(120) + 0.06 * k, 2.2, 0.3)
            if uk <= 0: continue
            x, y, z = G.pos(*p, lon0, lat0, R, cx, cy)
            if z > 0.05:
                disque(c, x, y, 13 * uk, VERT, 1, (4, 10, 0.2)); onde(c, x, y, t, TW(120) + 0.06 * k, 10, 60, VERT, 4, 0.5)
        pil(c, "TON SECTEUR", 290, 640, 40, INK, BL, TW(113) - 0.08, t, -5, "map-pin")
        pil(c, "DISTRIBUTEUR", 800, 660, 40, VERT, BL, TW(111) - 0.08, t, 5, "store")
        if t >= TW(123) - 0.1:
            u = apparait(t, TW(123) - 0.1)
            pastille_rot(c, "TOUTE L’EUROPE", 540, 1640, 46, VERT, BL, -3, mix(0.3, 1, u), borne(u * 2), "globe", (14, 32, 0.25))


def mix_hex(a, b, u):
    a, b = a.lstrip("#"), b.lstrip("#")
    return "#" + "".join(f"{int(round(mix(int(a[i:i + 2], 16), int(b[i:i + 2], 16), borne(u)))):02X}" for i in (0, 2, 4))


# ─────────────────────────────────────────── S7 · les contacts dans le ChinaBook, puis enregistre / commente
def s7(c, t):
    sc = scene(c, t, S7, "gauche", None, de=0.3)
    if sc is None: return
    with sc:
        e = prog(t, S7[0] + 0.05, 0.45, sortie)
        lignes = [dict(t=TW(125) - 0.05, image="produits/mobilite/moto-electrique", zoom=1.6, nom="Motos électriques", ville="Guangzhou"),
                  dict(t=TW(127) - 0.05, image="showroom-surron", zoom=1.4, nom="Pièces et équipement", ville="Guangzhou"),
                  dict(t=TW(129) - 0.05, image="photos/chaussures/etagere-baskets-running-6-modeles", nom="Sneakers", ville="Guangzhou")]
        tel(c, 540, 1150, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-30, -4, e) + 2 * math.sin(t * 2.2),
            s=mix(0.6, 1, e), alpha=borne(e * 2))
        tampon(c, "EN DIRECT", 800, 760, t, TW(129), 56, VERT, -8, "badge-check")


T_LOGO = TW(133) - 0.12
SC = (T_LOGO + 0.85, DUREE)
T_FIN = TW(144) + 0.45
REPONSE = "La grosse"
T_TAPE = [TW(141) + k * 0.07 for k in range(len(REPONSE))]


def disque_logo(c, t):
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (SC[0] - 0.05, 1750), (SC[0] + 0.35, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, INK)
        if T_LOGO + 0.2 <= t <= SC[0] + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, SC[0] - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * so)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2, lw, borne(u * 3) * (1 - so))
    return r


def sc_cta(c, t):
    """enregistre la vidéo, puis la réponse tapée en commentaire"""
    if t < SC[0] or t > T_FIN + 0.4: return
    o = prog(t, T_FIN, 0.32, entree)
    u = prog(t, SC[0], 0.4, sortie)
    c.save(); c.translate(0, mix(900, 0, u) + 900 * o)
    # le signet qui se remplit
    us = apparait(t, TW(134) - 0.08, 1.8, 0.34)
    rempli = t >= TW(134) + 0.15
    b = 1 + 0.25 * (1 - prog(t, TW(134) + 0.15, 0.25)) if rempli else 1
    c.save(); c.translate(250, 760); c.scale(mix(0.3, 1, us) * b, mix(0.3, 1, us) * b)
    disque(c, 0, 0, 100, INK, borne(us * 2), (14, 36, 0.3)); signet(c, 0, 0, 110, rempli, borne(us * 2))
    c.restore()
    if rempli: etincelles(c, 250, 760, t, TW(134) + 0.15, 10, 190, "#FACE15")
    pastille_rot(c, "ENREGISTRE", 560, 740, 44, "#FACE15", INK, -5, mix(0.3, 1, us), borne(us * 2), None, (12, 28, 0.2))
    # la zone de commentaires
    y0 = 920
    carte(c, 60, y0, 960, 600, 54, BL, 1.0, (26, 60, 0.2))
    icone(c, "message-circle", 140, y0 + 80, 52, INK, 2.4)
    texte(c, "Commentaires", 190, y0 + 56, 38, INK, "noir", track=0)
    for k in range(2):
        yy = y0 + 160 + k * 130
        disque(c, 140, yy + 30, 40, "#E6EBE8"); rrect(c, 200, yy + 4, 260 - 40 * k, 20, 10, "#E6EBE8"); rrect(c, 200, yy + 40, 520 - 60 * k, 20, 10, "#EEF1EF")
    rrect(c, 100, y0 + 460, 880, 100, 50, "#F2F4F3", 1.0, None, VERT if t >= TW(137) else "#E1E5E3", 4)
    tx = "".join(l for l, tl in zip(REPONSE, T_TAPE) if t >= tl)
    texte(c, tx or "Ajoute un commentaire…", 150, y0 + 484, 38, INK if tx else C["grisClair"], "noir" if tx else "moyen", track=0)
    if TW(137) <= t < T_TAPE[-1] + 0.6 and int(t * 4) % 2 == 0:
        rrect(c, 150 + largeur(tx, 38, "noir", 0) + 4, y0 + 482, 5, 50, 2, INK)
    c.restore()
    moto(c, 820, 880 + mix(900, 0, u) + 900 * o, 300, apparait(t, TW(142) - 0.1, 1.6, 0.4), 4)


def carton_final(c, t):
    if t < T_FIN: return
    u = prog(t, T_FIN, 0.4, sortie)
    disque(c, 540, 1060, 440 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
    ul = prog(t, T_FIN + 0.08, 0.36, lambda v: rebond(v, 1.6))
    lw = 760 * mix(0.6, 1, ul)
    iw_, ih_ = taille_img("logo"); lh = lw * ih_ / iw_
    image(c, "logo", 540 - lw / 2, 1000 - lh / 2, lw, borne(ul * 2))
    ub = prog(t, T_FIN + 0.3, 0.36, lambda v: rebond(v, 1.8))
    if ub > 0:
        c.save(); c.translate(540, 1180); c.scale(mix(0.4, 1, ub), mix(0.4, 1, ub))
        with Calque(c, borne(ub * 2)):
            rrect(c, -250, -54, 500, 108, 54, INK, 1.0, (16, 40, 0.25))
            signet(c, -170, 0, 56, True); texte_centre(c, "Enregistre-la", 40, 0, 40, BL, "noir")
        c.restore()
    etincelles(c, 540, 1180, t, T_FIN + 0.45, 12, 360)
    ud = prog(t, T_FIN + 0.55, 0.4, sortie)
    if ud > 0:
        texte_centre(c, "proposé par", 540, 1320, 26, C["gris"], "fort", ud, 0.04)
        image(c, "logo-dropandyou", 540 - 160, 1350, 320, ud)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -6); son(0.0, "whoosh_court", -10); son(TW(1) - 0.1, "pop", -9); son(TW(2) - 0.08, "pop", -11)
son(TW(5) - 0.08, "impact_doux", -8); son(TW(5), "croc", -10); son(TW(9) - 0.08, "pop", -10); son(TW(10) - 0.1, "impact", -8)
son(S1[0], "whoosh", -10); son(S1[0] + 0.1, "pop", -11)
son(TW(17) - 0.05, "whoosh_court", -10); son(TW(20) - 0.06, "ching", -7)
son(TW(24) - 0.05, "whoosh_court", -10); son(TW(27) - 0.06, "ching", -7)
son(S2[0], "whoosh_long", -10); son(S2[0] + 0.15, "pop", -11); son(TW(32) - 0.1, "whoosh_bas", -9); son(TW(34) - 0.08, "pop", -10)
son(TW(37) - 0.1, "impact_doux", -8); son(TW(40) - 0.06, "ching", -9)
son(S3[0], "whoosh", -10); son(S3[0] + 0.1, "pop", -11); son(TW(45) - 0.08, "pop", -11); son(TW(49) - 0.1, "blip", -10)
son(TW(51) - 0.12, "whoosh_court", -10); son(TW(58) - 0.06, "ching", -6); son(TW(58) + 0.3, "impact_doux", -9)
son(TW(62) - 0.12, "whoosh_court", -10); son(TW(71) - 0.06, "ching", -6); son(TW(71) + 0.3, "impact", -8)
son(S4[0], "whoosh", -10); son(S4[0] + 0.1, "montee", -14); son(TW(80) - 0.1, "montee", -10); son(TW(80) + 0.05, "tampon", -6); son(TW(80) + 0.3, "ching", -8)
son(S5[0], "whoosh", -10); son(TW(91) - 0.14, "tampon", -6); son(TW(91) - 0.1, "impact", -8)
son(TW(92) - 0.2, "whoosh_long", -10); son(TW(92) - 0.05, "pop", -9); son(TW(95) - 0.08, "pop", -11); son(TW(96) - 0.08, "pop", -11)
son(TW(101) - 0.12, "tampon", -6); son(TW(101), "check", -9); son(TW(104) - 0.05, "pop", -10)
son(S6[0], "whoosh", -10); son(TW(111) - 0.08, "pop", -10); son(TW(113) - 0.08, "pop", -10)
son(TW(116) - 0.08, "ding", -9); son(TW(118) - 0.08, "ding", -9)
for k in range(len(EUROPE)): son(TW(120) + 0.06 * k, "blip", -14)
son(TW(123) - 0.1, "ching", -8)
son(S7[0], "whoosh_long", -10); son(TW(129) - 0.12, "tampon", -7)
for tk in (TW(125), TW(127), TW(129)): son(tk - 0.05, "ching", -11)
son(T_LOGO - 0.1, "montee", -12); son(T_LOGO + 0.24, "impact", -5); son(T_LOGO + 0.26, "verre", -8)
son(SC[0], "whoosh", -10); son(TW(134) - 0.08, "pop", -10); son(TW(134) + 0.15, "ching", -8)
for tl in T_TAPE: son(tl, "frappe", -12)
son(T_TAPE[-1] + 0.15, "message", -9); son(TW(142) - 0.1, "pop", -10)
son(T_FIN, "whoosh", -10); son(T_FIN + 0.1, "impact_doux", -7); son(T_FIN + 0.12, "verre", -8); son(T_FIN + 0.3, "pop", -9); son(T_FIN + 0.55, "pop", -11)

for a, b in [(S1[0], S1[0] + 0.3), (S2[0], S2[0] + 0.3), (S3[0], S3[0] + 0.3), (S4[0], S4[0] + 0.3), (S5[0], S5[0] + 0.3),
             (TW(92) - 0.2, TW(92) + 0.15), (S6[0], S6[0] + 0.3), (S7[0], S7[0] + 0.35), (T_LOGO, T_LOGO + 0.4), (SC[0], SC[0] + 0.4),
             (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, "#FFFFFF", 0.2), (TW(20) - 0.06, VERT, 0.08), (TW(27) - 0.06, VERT, 0.08), (TW(58), VERT, 0.1), (TW(71), VERT, 0.14),
                    (TW(80) + 0.05, VERT, 0.12), (TW(91), ROUGE, 0.12), (TW(101), VERT, 0.1), (TW(123), VERT, 0.1),
                    (T_LOGO + 0.24, BL, 0.15), (T_FIN + 0.1, VERT, 0.1)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def alpha_bandeau(t, r):
    return borne(prog(t, 0.45, 0.3) * (1 - prog(t, SC[0] - 0.05, 0.25)) * (1 - borne(r / 400)))


def dessine(c, t):
    fond(c, t)
    for s in (h, s1, s2, s3, s4, s5, s6, s7):
        s(c, t)
    r = disque_logo(c, t)
    bandeau(c, t, alpha_bandeau(t, r))
    sc_cta(c, t)
    carton_final(c, t)
    K.dessine_eclairs(c, t)
    if t < T_FIN: SOUS.dessine(c, t, BL if r > 900 else INK)
