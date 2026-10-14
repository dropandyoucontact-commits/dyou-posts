"""CB-M08 « 50 paires de Saucony » — vidéo ORGANIQUE (53,5 s), dans la lignée de CB-M06 (la plus vue du TikTok).

Texte dicté par Youssef le 13/10/2026 (seul changement : 1 600 € pour 50 paires à 32 €, 800 € chacun — il avait écrit
1 500 / 750). Prix de Youssef : 32 € la paire par 50, revente 80-85 €, ≈ 50 € de bénéfice ; paiement en 3 fois Klarna.
Boucle ouverte : « je te donne le prix à la fin » → barre « prix verrouillé » en haut jusqu'au 32 €.
Médias : Saucony Omni 9 du catalogue DROP&YOU détourées (rembg), photos de cartons et de billets de Youssef,
vidéos de la banque (On en stock, cartons Saucony à Guangzhou).
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
AFFICHE = {0: "50", 6: "On.", 29: "2 500 €", 40: "50 €", 57: "50", 63: "2 500 €.", 74: "50,", 80: "32 €", 87: "85 €,", 89: "80 €",
           100: "50 €", 108: "50", 136: "48 h.", 141: "1 600 €,", 149: "800 €", 158: "3", 161: "Klarna :", 195: "ChinaBook."}
CACHES = {30, 31, 32, 33, 41, 64, 65, 66, 67, 81, 101, 137, 142, 143, 144, 150}
VERTS = {0, 3, 6, 29, 34, 40, 45, 47, 50, 63, 80, 87, 89, 100, 103, 113, 121, 125, 136, 141, 149, 158, 161, 167, 179, 180, 186, 195}
ROUGES = {18, 21}
COUPES = {7, 14, 24, 37, 44, 53, 61, 68, 75, 84, 88, 95, 106, 110, 118, 122, 126, 133, 138, 145, 152, 160, 162, 169, 173, 181, 190}


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


# ─────────────────────────────────────────── fenêtres et transitions (comme CB-M06)
def fen(i0, i1, a=0.14, b=0.02):
    return (TW(i0) - a if i0 else 0.0, TW(i1) - b)


H, S1, S2, S3 = fen(0, 24), fen(24, 37), fen(37, 68), fen(68, 106)
S4, S5, S6, S7 = fen(106, 138), fen(138, 169), fen(169, 181), (TW(181) - 0.14, TW(195) + 0.3)
T_LOGO = TW(195) - 0.12
T_FIN = T_LOGO + 0.85


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


# ─────────────────────────────────────────── la barre « prix verrouillé » (boucle ouverte jusqu'au 32 €)
T_BARRE0 = TW(22) + 0.25
T_REVELE = TW(80) - 0.06


def barre_prix(c, t):
    if t < T_BARRE0 or t > T_REVELE + 0.9: return
    u = prog(t, T_BARRE0, 0.35, sortie)
    o = prog(t, T_REVELE + 0.5, 0.35, entree)
    f = prog(t, T_BARRE0, T_REVELE - T_BARRE0, lin)
    y = 236
    with Calque(c, u * (1 - o)):
        rrect(c, 90, y - 7, 820, 14, 7, "#E6EBE8")
        rrect(c, 90, y - 7, 820 * f, 14, 7, VERT)
        disque(c, 90 + 820 * f, y, 11, VERT); anneau(c, 90 + 820 * f, y, 11 + 8 * ((t * 2) % 1), VERT, 3, 1 - (t * 2) % 1)
        ouvert = t >= T_REVELE
        s = battement(t, T_REVELE, 0.5, 0.4)
        c.save(); c.translate(965, y); c.scale(s, s); c.rotate(8)
        rrect(c, -50, -30, 100, 60, 16, VERT if ouvert else BL, 1, (8, 20, 0.2), INK if not ouvert else VERT, 4)
        if ouvert: texte_centre(c, "32 €", 0, 0, 28, BL, "noir")
        else:
            icone(c, "lock", -20, 0, 28, ROUGE, 2.8); texte_centre(c, "€", 20, 0, 30, INK, "noir")
        c.restore()


# ─────────────────────────────────────────── H · 50 paires, combien en Chine ? le prix à la fin
SORTIES = [("s15", (300, 820), -14, 0.0, 380), ("s10", (800, 760), 12, TW(3) - 0.05, 360), ("s14", (790, 1540), -8, TW(3) + 0.12, 340),
           ("s16", (270, 1500), 9, TW(3) + 0.28, 320)]


def ecran_cartons(cc, a, b, d, e, t):
    sw = prog(t, TW(6) - 0.12, 0.3, entreeSortie)
    if sw < 1: image_cover(cc, "carton-saucony", a - d * sw, b, d, e, 1.12 + 0.04 * math.sin(t), 0.55, 0.55)
    if sw > 0: image_cover(cc, "carton-on", a + d * (1 - sw), b, d, e, 1.1, 0.5, 0.55)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(a, b), skia.Point(a, b + 220)], [hexa("#000000", 0.45), hexa("#000000", 0)]))
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, 220), p)
    texte(cc, "9:41", a + 40, b + 24, 24, BL, "fort", track=0)


def h(c, t):
    sc = scene(c, t, H, None, "gauche")
    if sc is None: return
    with sc:
        ue = prog(t, 0, 0.5, sortie)
        part = prog(t, TW(9) - 0.15, 0.4, entreeSortie)          # les baskets s'écartent pour l'étiquette
        sx, sy = secousse(t, TW(6) - 0.1, 10, 0.3)
        tel(c, 540 + sx, mix(1180, 1260, part) + sy, lambda cc, a, b, d, e: ecran_cartons(cc, a, b, d, e, t),
            ry=mix(-20, -8, ue) + 3 * math.sin(t * 2.2), rz=mix(-5, 2, ue), s=mix(1.06, 1, ue) * mix(1, 0.82, part))
        # les Saucony jaillissent de l'écran
        for nom, (x, y), rot, t0, w in SORTIES:
            u = 1.0 if t0 <= 0 else prog(t, t0, 0.45, lambda v: rebond(v, 1.3))
            if u <= 0: continue
            px, py = mix(540, x, u), mix(1180, y, u)
            px += mix(0, (-500 if x < 540 else 500), part); py += mix(0, -120, part)
            fl = 10 * math.sin(t * 3 + x)
            basket(c, nom, px, py + fl, w * mix(0.3, 1, u), borne(u * 2) * (1 - part), rot + 5 * math.sin(t * 2 + y))
        # ×50 dès l'image 0
        u50 = 1.0 if t < 0.05 else apparait(t, 0.0, 1.6, 0.3)
        b50 = battement(t, TW(0) + 0.05, 0.12, 0.3)
        c.save(); c.translate(mix(830, 860, part), mix(1180, 640, part)); c.rotate(8); c.scale(u50 * b50 * mix(1, 0.6, part), u50 * b50 * mix(1, 0.6, part))
        rrect(c, -150, -90, 300, 180, 44, VERT, 1, (16, 40, 0.3)); texte_centre(c, "×50", 0, -4, 120, BL, "noir")
        c.restore()
        # combien ça coûte en Chine ? l'étiquette, puis le cadenas
        ue_ = apparait(t, TW(9) - 0.08, 1.8, 0.4) * (1 - prog(t, TW(22) + 0.05, 0.3, entree))
        if ue_ > 0:
            tremble = 6 * math.sin(t * 30) * (1 - prog(t, TW(18) - 0.1, 0.2))
            v = prog(t, TW(18) - 0.06, 0.3, lambda w_: rebond(w_, 2.4))
            vers_barre = prog(t, TW(22) + 0.05, 0.3, entree)
            etiquette(c, mix(540, 965, vers_barre), mix(830, 236, vers_barre), 640, "? €", ue_ + (1 - ue_) * 0, INK, -6 + tremble * 0.3, v)
            if t >= TW(13) - 0.08:
                uf = apparait(t, TW(13) - 0.08) * (1 - vers_barre)
                c.save(); c.translate(250, 640); c.rotate(-10); c.scale(uf, uf)
                rrect(c, -80, -54, 160, 108, 20, BL, 1, (12, 30, 0.25)); drapeau(c, "CN", -66, -40, 132, 80, 10)
                c.restore()
        pil(c, "À LA FIN", 330, 1010, 44, ROUGE, BL, TW(20) - 0.05, t, -6, "timer", TW(22) + 0.05)
        if t >= TW(22) - 0.1:
            u = apparait(t, TW(22) - 0.1, 2.0, 0.34) * (1 - prog(t, H[1] - 0.25, 0.2, entree))
            c.save(); c.translate(540, 980); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
            disque(c, 0, 0, 120, INK, borne(u * 2), (16, 40, 0.3)); icone(c, "hand", 0, 0, 120, BL, 2.6, borne(u * 2))
            c.restore()
            pastille_rot(c, "RESTE LÀ", 540, 1170, 46, INK, BL, -4, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))


# ─────────────────────────────────────────── S1 · 2 500 € ce mois-ci
PLUIE = [(130 + k * 92, (k * 37) % 5 * 0.07, (k * 53) % 40 - 20) for k in range(10)]


def s1(c, t):
    sc = scene(c, t, S1, "gauche", "gauche")
    if sc is None: return
    with sc:
        t0 = TW(29) - 0.1
        for x, d, rot in PLUIE:
            u = prog(t, t0 + d, 1.4, lin)
            if 0 < u < 1:
                billet(c, x, mix(500, 1650, u), 130, rot + 200 * u, borne((1 - u) * 4))
        u = apparait(t, S1[0] + 0.1, 1.6, 0.4)
        c.save(); c.translate(540, 1040); c.scale(mix(0.4, 1, u) * battement(t, TW(33) + 0.2, 0.08, 0.35), mix(0.4, 1, u) * battement(t, TW(33) + 0.2, 0.08, 0.35))
        carte(c, -420, -200, 840, 400, 60, BL, borne(u * 2), (26, 60, 0.16))
        n = compteur(t, t0, TW(33) + 0.2, 2500)
        texte_centre(c, euros(n), 0, -30, 170, VERT, "noir", borne(u * 2))
        texte_centre(c, "de bénéfice", 0, 110, 44, C["gris"], "fort", borne(u * 2), 0)
        c.restore()
        confettis(c, 540, 1000, t, TW(33) + 0.2, 26, 420, 4)
        tampon(c, "FACILE", 300, 1350, t, TW(34), 60, VERT, -8, "check")
        if t >= TW(35) - 0.1:
            uc = apparait(t, TW(35) - 0.1)
            c.save(); c.translate(790, 1380); c.rotate(6); c.scale(mix(0.3, 1, uc), mix(0.3, 1, uc))
            carte(c, -150, -130, 300, 260, 40, BL, borne(uc * 2), (16, 40, 0.2))
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150, -130, 300, 260), 40, 40), True)
            c.drawRect(skia.Rect.MakeXYWH(-150, -130, 300, 70), peinture(ROUGE, borne(uc * 2))); c.restore()
            texte_centre(c, "CE MOIS", 0, -95, 30, BL, "noir", borne(uc * 2), 0.06)
            icone(c, "calendar", 0, 40, 110, INK, 2.4, borne(uc * 2))
            c.restore()


# ─────────────────────────────────────────── S2 · 50 € par paire × 50 paires = 2 500 €
def s2(c, t):
    sc = scene(c, t, S2, "gauche", "gauche")
    if sc is None: return
    with sc:
        # a) une paire, + 50 €
        a = fenetre(t, S2[0], TW(53) - 0.1)
        mv = prog(t, TW(44) - 0.15, 0.4, entreeSortie)
        if a > 0:
            with Calque(c, a):
                ub = apparait(t, S2[0] + 0.08, 1.5, 0.4)
                basket(c, "s15", mix(540, 300, mv), mix(980, 760, mv), mix(560, 300, mv) * mix(0.4, 1, ub), 1, -6 + 3 * math.sin(t * 2))
                ue = apparait(t, TW(40) - 0.08, 2.0, 0.36)
                etiquette(c, mix(720, 720, mv), mix(1250, 720, mv), mix(420, 300, mv), "+50 €", ue, VERT, 6, 0, "par paire" if t >= TW(43) - 0.1 else None)
                for k, (nom, x, tk) in enumerate([("vinted", 230, TW(45)), ("ebay", 540, TW(47)), ("snapchat", 850, TW(50))]):
                    tuile(c, nom, x, 1150, 220, apparait(t, tk - 0.08, 1.9, 0.36), [-6, 3, 7][k])
                for k, (nom, x, y) in enumerate([("tiktok", 300, 1420), ("whatsapp", 540, 1460), ("instagram", 780, 1420)]):
                    tuile(c, nom, x, y, 130, apparait(t, TW(52) - 0.12 + 0.07 * k, 2.2, 0.3), [-8, 0, 8][k])
                if t >= TW(52) - 0.1:
                    uq = apparait(t, TW(52) - 0.1)
                    pastille_rot(c, "PEU IMPORTE", 820, 900, 40, INK, BL, 5, mix(0.3, 1, uq), borne(uq * 2), None, (14, 32, 0.25))
        # b) la grille des 50 paires vendues
        g = fenetre(t, TW(53) - 0.12, TW(61) + 0.1)
        if g > 0:
            with Calque(c, g):
                carte(c, 70, 640, 940, 700, 50, BL, 1, (26, 60, 0.14))
                tn = prog(t, TW(56) - 0.05, TW(60) + 0.1 - TW(56), lin)
                n = int(50 * tn)
                for k in range(50):
                    r_, q = divmod(k, 10)
                    x, y = 132 + q * 91, 760 + r_ * 108
                    ok = k < n
                    uk = prog(t, TW(56) - 0.05 + (TW(60) + 0.1 - TW(56)) * k / 50, 0.18, lambda v: rebond(v, 2.2))
                    basket(c, ["s15", "s10", "s14", "s16", "s9"][k % 5], x, y, 80 * mix(1, 1.15, uk if ok else 0), 1.0 if ok else 0.18, 0, False)
                    if ok and uk > 0.5: coche(c, x + 30, y - 24, 14, borne((uk - 0.5) * 2))
                texte_centre(c, f"{n}/50 vendues", 540, 1290, 48, VERT if n == 50 else INK, "noir")
        # c) l'équation
        e = prog(t, TW(61) - 0.12, 0.3, sortie)
        if e > 0:
            with Calque(c, e):
                ue = apparait(t, TW(61) - 0.05, 1.6, 0.4)
                c.save(); c.translate(540, 1030); c.scale(mix(0.5, 1, ue), mix(0.5, 1, ue))
                carte(c, -440, -260, 880, 520, 60, BL, 1, (26, 60, 0.16))
                texte_centre(c, "50 € × 50", 0, -110, 100, INK, "noir")
                trait(c, -340, 0, 340, 0, "#E6EBE8", 6)
                u2 = apparait(t, TW(63) - 0.06, 2.2, 0.36)
                c.save(); c.translate(0, 120); c.scale(mix(0.3, 1, u2), mix(0.3, 1, u2))
                texte_centre(c, "= 2 500 €", 0, 0, 130, VERT, "noir", borne(u2 * 2))
                c.restore()
                c.restore()
                confettis(c, 540, 1100, t, TW(63), 28, 460, 9)


# ─────────────────────────────────────────── S3 · 32 € la paire, revendue 80-85 €, + 50 €
def ecran_video(nom, t0, vitesse=1.0, rogne=(0, 0, 0, 0)):
    return lambda cc, a, b, d, e, t: video(cc, nom, a, b, d, e, t - t0, vitesse, True, 0, 1.0, rogne)


def s3(c, t):
    sc = scene(c, t, S3, "gauche", "gauche")
    if sc is None: return
    with sc:
        # a) les Saucony en gros à Guangzhou, chez DROP&YOU
        rv = prog(t, T_REVELE - 0.15, 0.35, entreeSortie)
        a = 1 - prog(t, TW(84) - 0.3, 0.25, entree)
        if a > 0:
            with Calque(c, a):
                tel(c, mix(330, -300, rv), 1180, lambda cc, x, y, d, e: video(cc, "videos/guangzhou/guangzhou-cartons-baskets-gros", x, y, d, e, (t - S3[0]) * 0.9, 1.0, True),
                    ry=12 + 3 * math.sin(t * 2), rz=-3)
                if t >= TW(69) - 0.1:
                    ul = apparait(t, TW(69) - 0.1) * (1 - rv)
                    c.save(); c.translate(560, 720); c.rotate(-5); c.scale(mix(0.3, 1, ul), mix(0.3, 1, ul))
                    rrect(c, -230, -50, 460, 100, 50, BL, borne(ul * 2), (12, 30, 0.22)); drapeau(c, "CN", -205, -24, 72, 48, 8)
                    texte_centre(c, "Guangzhou", 40, 0, 44, INK, "noir", borne(ul * 2))
                    c.restore()
                if t >= TW(72) - 0.1:
                    ud = apparait(t, TW(72) - 0.1) * (1 - rv)
                    c.save(); c.translate(770, 1000); c.rotate(4); c.scale(mix(0.3, 1, ud), mix(0.3, 1, ud))
                    carte(c, -220, -80, 440, 160, 40, BL, borne(ud * 2), (14, 34, 0.2))
                    image(c, "logo-dropandyou", -180, -36, 360, borne(ud * 2))
                    c.restore()
                if t >= TW(74) - 0.1:
                    uc = apparait(t, TW(74) - 0.1) * (1 - rv)
                    carton(c, 780, 1330, 230, 0, borne(uc * 2), 4 + 3 * math.sin(t * 5))
                    c.save(); c.translate(880, 1240); c.rotate(10); c.scale(uc, uc)
                    rrect(c, -80, -48, 160, 96, 30, VERT, 1, (10, 24, 0.25)); texte_centre(c, "×50", 0, 0, 56, BL, "noir")
                    c.restore()
                # b) la révélation : 32 €
                if t >= T_REVELE - 0.12:
                    u = apparait(t, T_REVELE - 0.1, 2.0, 0.4)
                    v = prog(t, T_REVELE, 0.25, sortie)                   # le cadenas saute
                    sx, sy = secousse(t, T_REVELE, 18, 0.35)
                    etiquette(c, 540 + sx, 1060 + sy, 760, "32 €", u, VERT, -5, 0, "la paire" if t >= TW(82) - 0.1 else None)
                    if v < 1:
                        c.save(); c.translate(mix(780, 980, v), mix(870, 600, v) + 400 * v * v); c.rotate(12 + 300 * v)
                        disque(c, 0, 0, 80, ROUGE, 1 - v); icone(c, "lock-open", 0, 0, 86, BL, 2.8, 1 - v)
                        c.restore()
                    confettis(c, 540, 1000, t, T_REVELE + 0.05, 34, 520, 2)
                    etincelles(c, 540, 1060, t, T_REVELE, 14, 520)
                    if t >= TW(80) + 0.15:
                        up = apparait(t, TW(80) + 0.15) * a
                        pastille_rot(c, "PRIX DÉVOILÉ", 540, 1420, 44, INK, BL, -3, mix(0.3, 1, up), borne(up * 2), "lock-open", (14, 32, 0.25))
        # c) l'annonce revendue 85 €, parfois 80 €
        b = fenetre(t, TW(84) - 0.3, TW(95) - 0.05)
        if b > 0:
            with Calque(c, b):
                ua = apparait(t, TW(84) - 0.25, 1.5, 0.45)
                c.save(); c.translate(540, 1080); c.rotate(-3); c.scale(mix(0.5, 1, ua), mix(0.5, 1, ua)); c.translate(-540, -1080)
                carte(c, 190, 640, 700, 860, 48, BL, 1, (26, 60, 0.18))
                rrect(c, 220, 670, 640, 480, 30, "#F3F6F4")
                basket(c, "s10", 540, 920, 520, 1, -4 + 2 * math.sin(t * 2))
                tuile(c, "vinted", 790, 720, 90, 1.0, 6)
                texte(c, "Saucony Omni 9", 230, 1180, 44, INK, "noir", track=0)
                texte(c, "Neuve · toutes tailles", 232, 1240, 28, C["gris"], "demi", track=0)
                p85 = apparait(t, TW(87) - 0.06, 2.0, 0.34)
                barre_ = prog(t, TW(89) - 0.1, 0.22, sortie)
                if p85 > 0:
                    texte(c, "85 €", 232, 1300, 84, INK if barre_ <= 0 else C["grisClair"], "noir", track=0, alpha=borne(p85 * 2))
                    if barre_ > 0: trait(c, 226, 1352, 226 + 200 * barre_, 1352, ROUGE, 8)
                if barre_ > 0:
                    u80 = apparait(t, TW(89) - 0.02, 2.2, 0.34)
                    c.save(); c.translate(600, 1345); c.scale(u80, u80); texte_centre(c, "80 €", 0, 0, 92, VERT, "noir"); c.restore()
                c.restore()
                pil(c, "ARRANGÉ", 800, 1460, 42, VERT, BL, TW(92) - 0.08, t, 5, "heart-handshake")
        # d) la marge : 32 € → 80-85 €, ≈ + 50 €
        d_ = prog(t, TW(95) - 0.15, 0.3, sortie)
        if d_ > 0:
            with Calque(c, d_):
                carte(c, 110, 620, 860, 860, 56, BL, 1, (26, 60, 0.14))
                base = 1330
                ha = 300 * apparait(t, TW(95) - 0.05, 1.4, 0.45)
                hv = 780 * apparait(t, TW(97) - 0.05, 1.4, 0.5)
                rrect(c, 230, base - ha * 32 / 85 * 2.2, 220, ha * 32 / 85 * 2.2, 26, "#C9D0CC")
                texte_centre(c, "Achat", 340, base + 50, 36, C["gris"], "noir")
                texte_centre(c, "32 €", 340, base - ha * 32 / 85 * 2.2 - 50, 52, INK, "noir", borne(ha / 100))
                hvv = hv * 0.85
                rrect(c, 630, base - hvv, 220, hvv, 26, VERT)
                texte_centre(c, "Revente", 740, base + 50, 36, C["gris"], "noir")
                texte_centre(c, "80-85 €", 740, base - hvv - 50, 52, VERT, "noir", borne(hv / 200))
                ub = apparait(t, TW(100) - 0.08, 2.0, 0.4)
                if ub > 0:
                    y0, y1 = base - 300 * 32 / 85 * 2.2, base - 780 * 0.85
                    trait(c, 540, y0, 540, mix(y0, y1, ub), INK, 6, 1, [14, 10])
                    c.save(); c.translate(540, (y0 + y1) / 2); c.rotate(-6); c.scale(ub, ub)
                    rrect(c, -170, -60, 340, 120, 60, INK, 1, (12, 30, 0.3)); texte_centre(c, "≈ +50 €", 0, 0, 64, BL, "noir")
                    c.restore()
                tampon(c, "BÉNÉFICE", 340, 760, t, TW(103), 50, VERT, -6, "trending-up")


# ─────────────────────────────────────────── S4 · ça va plus vite que tu penses : TikTok, stock en France, 48 h
COEURS = [(k * 0.31 % 1.0, 60 + (k * 47) % 120, k) for k in range(9)]


def ecran_tiktok(cc, a, b, d, e, t):
    video(cc, "videos/chaussures/baskets-stock-1", a, b, d, e, (t - TW(118)) * 1.3, 1.0, True, 0, 1.0, (0.0, 0.0, 0.0, 0.24))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(a, b + e - 380), skia.Point(a, b + e)], [hexa("#000000", 0), hexa("#000000", 0.7)]))
    cc.drawRect(skia.Rect.MakeXYWH(a, b + e - 380, d, 380), p)
    texte(cc, "Pour toi", a + d / 2 - 50, b + 40, 26, BL, "noir", track=0)
    for k, (ic, y) in enumerate([("heart", 500), ("message-circle", 610), ("send", 720)]):
        icone(cc, ic, a + d - 52, b + y, 50, BL if not (k == 0 and t > TW(121)) else "#FE2C55", 2.6)
    icone(cc, "heart", a + d - 52, b + 500, 50, "#FE2C55", 2.6, prog(t, TW(121), 0.2))
    for ph, dx, k in COEURS:
        u = ((t - TW(121)) * 0.8 + ph) % 1.0
        if t > TW(121):
            icone(cc, "heart", a + d - 70 - dx * u * 0.6, b + 480 - 380 * u, 34 + 10 * math.sin(k), "#FE2C55", 2.4, borne((1 - u) * 2))
    texte(cc, "@ton.stock", a + 28, b + e - 210, 28, BL, "noir", track=0)
    lignes = [("Stock dispo en France", TW(122) - 0.1), ("Livré dans ta ville", TW(126) - 0.1), ("Envoi en 48 h", TW(134) - 0.1)]
    for k, (l, tl) in enumerate(lignes):
        n = int(len(l) * prog(t, tl, 0.45, lin))
        if n > 0: texte(cc, l[:n], a + 28, b + e - 166 + k * 44, 30, BL, "fort", track=0)


def s4(c, t):
    sc = scene(c, t, S4, "gauche", "gauche")
    if sc is None: return
    with sc:
        # a) 50 paires, plus vite que tu penses
        a = 1 - prog(t, TW(118) - 0.3, 0.25, entree)
        if a > 0:
            with Calque(c, a):
                u = apparait(t, S4[0] + 0.08, 1.5, 0.4)
                n = compteur(t, TW(112) - 0.1, TW(117), 50)
                c.save(); c.translate(540, 1000); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
                carte(c, -380, -300, 760, 600, 60, BL, 1, (26, 60, 0.16))
                icone(c, "timer", 0, -150, 130, INK, 2.4)
                ang = (t - S4[0]) * (900 if t > TW(112) - 0.1 else 120)
                trait(c, 0, -140, 46 * math.sin(math.radians(ang)), -140 - 46 * math.cos(math.radians(ang)), ROUGE, 6)
                texte_centre(c, f"{n}", 0, 70, 200, VERT if n == 50 else INK, "noir")
                texte_centre(c, "paires vendues", 0, 215, 40, C["gris"], "fort", 1, 0)
                c.restore()
                if t > TW(112) - 0.1:
                    for k in range(7):
                        y = 760 + k * 80; ph = ((t * 3) + k * 0.37) % 1
                        trait(c, 60 + 900 * ph, y, 60 + 900 * ph + 140, y, INK, 5, 0.25 * (1 - ph) * a)
                tampon(c, "PLUS VITE", 540, 1420, t, TW(113), 60, VERT, -5, "zap")
        # b) le post TikTok
        b = prog(t, TW(118) - 0.3, 0.3, sortie)
        if b > 0:
            tel(c, mix(1500, 560, b), 1170, lambda cc, x, y, d, e: ecran_tiktok(cc, x, y, d, e, t), ry=-8 + 3 * math.sin(t * 2), rz=2)
            tuile(c, "tiktok", 220, 760, 170, apparait(t, TW(121) - 0.08, 1.9, 0.36), -8)
            if t >= TW(122) - 0.1:
                u = apparait(t, TW(122) - 0.1)
                pastille_rot(c, "STOCK DISPO", 830, 760, 40, INK, BL, 6, mix(0.3, 1, u), borne(u * 2), "package", (14, 32, 0.25))
                c.save(); c.translate(940, 690); c.scale(u, u); drapeau(c, "FR", -42, -28, 84, 56, 8); c.restore()
            pil(c, "DANS TA VILLE", 260, 1120, 40, VERT, BL, TW(126) - 0.08, t, -6, "map-pin")
            if t >= TW(134) - 0.1:
                uc = apparait(t, TW(134) - 0.1)
                carton(c, 850, 1330, 200, 0, borne(uc * 2), 6 + 3 * math.sin(t * 5))
            tampon(c, "48 H", 830, 1180, t, TW(136), 62, ROUGE, 8, "truck")


# ─────────────────────────────────────────── S5 · 1 600 € à deux, 800 € chacun, Klarna en 3 fois
def s5(c, t):
    sc = scene(c, t, S5, "gauche", "gauche")
    if sc is None: return
    with sc:
        a = 1 - prog(t, TW(152) - 0.3, 0.25, entree)
        if a > 0:
            with Calque(c, a):
                u = apparait(t, TW(141) - 0.1, 1.7, 0.4)
                sp = prog(t, TW(145) - 0.1, 0.45, entreeSortie)
                if sp < 1:
                    c.save(); c.translate(540, 900); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
                    with Calque(c, 1 - sp):
                        carte(c, -360, -150, 720, 300, 56, BL, 1, (26, 60, 0.16))
                        texte_centre(c, "1 600 €", 0, -20, 140, INK, "noir")
                        texte_centre(c, "50 paires", 0, 90, 38, C["gris"], "fort", 1, 0)
                    c.restore()
                for k, (lab, ic, tk) in enumerate([("Toi", "user", TW(145) - 0.05), ("Ton pote", "users", TW(147) - 0.05)]):
                    if sp <= 0: continue
                    x = mix(540, 290 + 500 * k, sp)
                    uk = apparait(t, tk, 1.8, 0.4)
                    c.save(); c.translate(x, 1000); c.rotate([-4, 4][k]); c.scale(mix(0.5, 1, sp), mix(0.5, 1, sp))
                    carte(c, -220, -260, 440, 520, 50, BL, 1, (22, 50, 0.16))
                    disque(c, 0, -120, 80, INK, borne(uk * 2)); icone(c, ic, 0, -120, 80, BL, 2.6, borne(uk * 2))
                    texte_centre(c, lab, 0, 0, 40, C["gris"], "noir", borne(uk * 2))
                    u8 = apparait(t, TW(149) - 0.06, 2.2, 0.36)
                    c.save(); c.translate(0, 130); c.scale(mix(0.3, 1, u8), mix(0.3, 1, u8))
                    texte_centre(c, "800 €", 0, 0, 100, VERT, "noir", borne(u8 * 2))
                    c.restore()
                    c.restore()
                if sp > 0.5:
                    disque(c, 540, 1000, 50, VERT, 1, (10, 24, 0.25)); texte_centre(c, "+", 540, 996, 70, BL, "noir")
        # Klarna
        b = prog(t, TW(152) - 0.3, 0.3, sortie)
        if b > 0:
            with Calque(c, b):
                c.save(); c.translate(540, 1080); c.scale(mix(0.6, 1, b), mix(0.6, 1, b)); c.translate(-540, -1080)
                carte(c, 120, 650, 840, 780, 54, BL, 1, (26, 60, 0.16))
                image(c, "logo-dropandyou", 180, 700, 300)
                texte(c, "Commande · 50 paires", 182, 790, 36, INK, "noir", track=0)
                trait(c, 170, 860, 910, 860, "#E6EBE8", 3)
                uk = apparait(t, TW(156) - 0.1, 1.6, 0.4)
                c.save(); c.translate(540, 960); c.scale(mix(0.4, 1, uk), mix(0.4, 1, uk))
                rrect(c, -360, -64, 720, 128, 64, MARQUES["klarna"], borne(uk * 2), (10, 26, 0.2))
                logo_glyphe(c, "klarna", -270, 0, 56, INK, borne(uk * 2))
                texte_centre(c, "Payer en 3 fois", 40, 0, 46, INK, "noir", borne(uk * 2))
                c.restore()
                for k, lab in enumerate(["Aujourd’hui", "Dans 30 j", "Dans 60 j"]):
                    x = 250 + k * 290
                    uu = apparait(t, TW(158) - 0.05 + 0.18 * k, 2.0, 0.34)
                    c.save(); c.translate(x, 1150); c.scale(mix(0.3, 1, uu), mix(0.3, 1, uu))
                    disque(c, 0, 0, 74, VERT if k == 0 else "#F3F6F4", borne(uu * 2))
                    anneau(c, 0, 0, 74, VERT, 6, borne(uu * 2))
                    texte_centre(c, "1/3", 0, 0, 48, BL if k == 0 else VERT, "noir", borne(uu * 2))
                    texte_centre(c, lab, 0, 120, 30, C["gris"], "fort", borne(uu * 2), 0)
                    c.restore()
                    if k < 2 and uu > 0.6: trait(c, x + 84, 1150, x + 206, 1150, VERT, 5, 1, [12, 10])
                c.restore()
                tuile(c, "klarna", 860, 660, 150, apparait(t, TW(161) - 0.08, 1.9, 0.36), 8)
                pil(c, "PETIT BUDGET", 330, 1490, 44, INK, BL, TW(167) - 0.08, t, -5, "wallet")


# ─────────────────────────────────────────── S6 · ta commande arrive, les ventes tombent, des vrais sous
VENTES = [(TW(175) - 0.1, "Vendu · 85 €"), (TW(176) + 0.05, "Vendu · 80 €"), (TW(177) + 0.1, "Vendu · 85 €")]


def s6(c, t):
    sc = scene(c, t, S6, "gauche", "zoom")
    if sc is None: return
    with sc:
        u = apparait(t, S6[0] + 0.05, 1.5, 0.45)
        vs = prog(t, TW(179) - 0.15, 0.35, entreeSortie)
        c.save(); c.translate(mix(540, 330, vs), 1100); c.rotate(mix(-4, -9, vs)); c.scale(mix(0.4, 1, u) * mix(1, 0.75, vs), mix(0.4, 1, u) * mix(1, 0.75, vs))
        carte(c, -300, -420, 600, 840, 46, BL, 1, (26, 60, 0.2))
        image_cover(c, "carton-on", -282, -402, 564, 804, 1.1 + 0.05 * prog(t, S6[0], 2.5, lin), 0.5, 0.55, 32)
        c.restore()
        pil(c, "COMMANDE REÇUE", 540, 700, 42, VERT, BL, TW(172) - 0.1, t, -4, "package", TW(179) - 0.2)
        for k, (tk, lab) in enumerate(VENTES):
            uv = apparait(t, tk, 1.8, 0.34) * (1 - prog(t, TW(179) - 0.15, 0.2, entree))
            if uv <= 0: continue
            c.save(); c.translate(mix(1100, 690, uv), 860 + k * 150); c.scale(mix(0.6, 1, uv), mix(0.6, 1, uv))
            rrect(c, -230, -56, 460, 112, 30, BL, borne(uv * 2), (12, 30, 0.22))
            disque(c, -170, 0, 36, VERT, borne(uv * 2)); icone(c, "check", -170, 0, 40, BL, 3.4, borne(uv * 2))
            texte(c, lab, -118, -hauteurLigne(38) / 2, 38, INK, "noir", track=0, alpha=borne(uv * 2))
            c.restore()
        if vs > 0:
            ub = apparait(t, TW(179) - 0.1, 1.6, 0.45)
            c.save(); c.translate(720, 1120); c.rotate(5); c.scale(mix(0.4, 1, ub), mix(0.4, 1, ub))
            carte(c, -260, -460, 520, 920, 44, BL, borne(ub * 2), (26, 60, 0.25))
            image_cover(c, "billets", -244, -444, 488, 888, 1.15, 0.72, 0.68, 30, borne(ub * 2))
            c.restore()
            confettis(c, 720, 1000, t, TW(180), 30, 460, 6, cols=[VERT, ORANGE, INK, C["vertMoyen"], C["ambre"]])


# ─────────────────────────────────────────── S7 · les fournisseurs en direct dans le ChinaBook
def s7(c, t):
    sc = scene(c, t, S7, "gauche", None, de=0.3)
    if sc is None: return
    with sc:
        e = prog(t, S7[0] + 0.05, 0.45, sortie)
        lignes = [dict(t=TW(186) - 0.05, image="photos/chaussures/etagere-baskets-running-6-modeles", nom="Running", ville="Guangzhou"),
                  dict(t=TW(189) - 0.1, image="photos/chaussures/planche-baskets-12-modeles", nom="Sneakers", ville="Guangzhou"),
                  dict(t=TW(191) - 0.1, image="produits/textile/veste-racing-noire", nom="Textile", ville="Guangzhou")]
        tel(c, 540, 1150, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-30, -4, e) + 2 * math.sin(t * 2.2),
            s=mix(0.6, 1, e), alpha=borne(e * 2))
        tampon(c, "EN DIRECT", 800, 760, t, TW(186), 56, VERT, -8, "badge-check")


def disque_logo(c, t):
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (T_FIN - 0.05, 1750), (T_FIN + 0.35, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, INK)
        if T_LOGO + 0.2 <= t <= T_FIN + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, T_FIN - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * so)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2, lw, borne(u * 3) * (1 - so))
    return r


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
son(0.0, "impact", -6); son(0.0, "whoosh_court", -10); son(0.1, "pop", -11)
for _, _, _, t0, _ in SORTIES[1:]: son(t0, "whoosh_court", -10); son(t0 + 0.2, "pop", -12)
son(TW(6) - 0.12, "swipe", -10); son(TW(9) - 0.15, "whoosh", -11); son(TW(9) - 0.08, "impact_doux", -8)
son(TW(13) - 0.08, "pop", -10); son(TW(18) - 0.06, "tampon", -7); son(TW(18), "croc", -9); son(TW(20) - 0.05, "pop", -10)
son(TW(22) - 0.1, "impact", -8); son(TW(22) + 0.05, "whoosh_court", -11); son(T_BARRE0, "blip", -12)
son(S1[0], "whoosh", -10)
for k in range(12): son(TW(29) - 0.1 + k * (TW(33) + 0.3 - TW(29)) / 12, "tick", -12)
son(TW(33) + 0.2, "ching", -7); son(TW(33) + 0.22, "impact_doux", -9); son(TW(34) - 0.12, "tampon", -7); son(TW(35) - 0.1, "pop", -10)
son(S2[0], "whoosh", -10); son(S2[0] + 0.1, "pop", -11); son(TW(40) - 0.08, "ching", -9); son(TW(44) - 0.15, "swipe", -12)
for tk in (TW(45), TW(47), TW(50)): son(tk - 0.08, "pop", -8)
for k in range(3): son(TW(52) - 0.12 + 0.07 * k, "pop", -12)
son(TW(53) - 0.12, "whoosh_court", -10)
for k in range(10): son(TW(56) - 0.05 + (TW(60) + 0.1 - TW(56)) * k / 10, "blip", -12)
son(TW(60) + 0.12, "check", -8); son(TW(61) - 0.1, "whoosh", -10); son(TW(63) - 0.06, "impact", -6); son(TW(63), "ching", -7)
son(S3[0], "whoosh", -10); son(TW(69) - 0.1, "pop", -10); son(TW(72) - 0.1, "pop", -9); son(TW(74) - 0.1, "impact_doux", -9)
son(T_REVELE - 0.4, "montee", -9); son(T_REVELE, "impact", -4); son(T_REVELE + 0.02, "ching", -6); son(T_REVELE + 0.05, "verre", -9)
son(TW(80) + 0.15, "pop", -10)
son(TW(84) - 0.3, "whoosh", -10); son(TW(87) - 0.06, "ching", -8); son(TW(89) - 0.1, "swipe", -9); son(TW(89) - 0.02, "pop", -8)
son(TW(92) - 0.08, "check", -9); son(TW(95) - 0.15, "whoosh", -10); son(TW(95) - 0.05, "montee", -14); son(TW(97) - 0.05, "montee", -11)
son(TW(100) - 0.08, "ching", -7); son(TW(103) - 0.12, "tampon", -6)
son(S4[0], "whoosh", -10)
for k in range(10): son(TW(112) - 0.1 + k * (TW(117) - TW(112) + 0.1) / 10, "tick", -11)
son(TW(113) - 0.12, "tampon", -7); son(TW(117), "ding", -9)
son(TW(118) - 0.3, "whoosh_long", -9); son(TW(121) - 0.08, "pop", -9); son(TW(121), "message_in", -10)
son(TW(122) - 0.1, "pop", -10); son(TW(126) - 0.08, "pop", -10); son(TW(134) - 0.1, "impact_doux", -9); son(TW(136) - 0.12, "tampon", -6)
son(S5[0], "whoosh", -10); son(TW(141) - 0.1, "impact_doux", -8); son(TW(145) - 0.1, "swipe", -9)
son(TW(145) - 0.05, "pop", -10); son(TW(147) - 0.05, "pop", -10); son(TW(149) - 0.06, "ching", -8)
son(TW(152) - 0.3, "whoosh", -10); son(TW(156) - 0.1, "pop", -9)
for k in range(3): son(TW(158) - 0.05 + 0.18 * k, "blip", -9)
son(TW(161) - 0.08, "pop", -9); son(TW(167) - 0.08, "pop", -10)
son(S6[0], "whoosh", -10); son(S6[0] + 0.05, "impact_doux", -8); son(TW(172) - 0.1, "check", -9)
for tk, _ in VENTES: son(tk, "ching", -8); son(tk + 0.02, "message_in", -12)
son(TW(179) - 0.15, "whoosh", -9); son(TW(179) - 0.1, "impact", -7); son(TW(180), "ching", -6)
son(S7[0], "whoosh_long", -10); son(TW(186) - 0.12, "tampon", -7)
for tk in (TW(186), TW(189), TW(191)): son(tk - 0.05, "ching", -11)
son(T_LOGO - 0.1, "montee", -12); son(T_LOGO + 0.24, "impact", -5); son(T_LOGO + 0.26, "verre", -8)
son(T_FIN, "whoosh", -10); son(T_FIN + 0.1, "impact_doux", -7); son(T_FIN + 0.12, "verre", -8); son(T_FIN + 0.3, "pop", -9); son(T_FIN + 0.55, "pop", -11)

for a, b in [(TW(6) - 0.12, TW(6) + 0.2), (TW(9) - 0.15, TW(9) + 0.25), (TW(22) + 0.05, TW(22) + 0.35), (S1[0], S1[0] + 0.3), (S2[0], S2[0] + 0.3),
             (TW(44) - 0.15, TW(44) + 0.25), (TW(53) - 0.12, TW(53) + 0.15), (TW(61) - 0.12, TW(61) + 0.2), (S3[0], S3[0] + 0.3),
             (T_REVELE - 0.15, T_REVELE + 0.3), (TW(84) - 0.3, TW(84) + 0.05), (TW(95) - 0.15, TW(95) + 0.15), (S4[0], S4[0] + 0.3),
             (TW(118) - 0.3, TW(118) + 0.05), (S5[0], S5[0] + 0.3), (TW(145) - 0.1, TW(145) + 0.35), (TW(152) - 0.3, TW(152) + 0.05),
             (S6[0], S6[0] + 0.3), (TW(179) - 0.15, TW(179) + 0.2), (S7[0], S7[0] + 0.35), (T_LOGO, T_LOGO + 0.4), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, "#FFFFFF", 0.2), (TW(18) - 0.06, ROUGE, 0.1), (TW(33) + 0.2, VERT, 0.1), (TW(63), VERT, 0.12),
                    (T_REVELE, VERT, 0.18), (TW(100) - 0.08, VERT, 0.1), (TW(136), ROUGE, 0.08), (TW(149), VERT, 0.1),
                    (TW(180), ORANGE, 0.12), (T_LOGO + 0.24, BL, 0.15), (T_FIN + 0.1, VERT, 0.1)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def alpha_bandeau(t, r):
    return borne(prog(t, 0.45, 0.3) * (1 - prog(t, T_FIN - 0.05, 0.25)) * (1 - borne(r / 400)))


def dessine(c, t):
    fond(c, t)
    for s in (h, s1, s2, s3, s4, s5, s6, s7):
        s(c, t)
    barre_prix(c, t)
    r = disque_logo(c, t)
    bandeau(c, t, alpha_bandeau(t, r))
    carton_final(c, t)
    K.dessine_eclairs(c, t)
    if t < T_FIN: SOUS.dessine(c, t, BL if r > 900 else INK)
