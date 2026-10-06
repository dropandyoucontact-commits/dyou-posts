"""CB-M04 « T'as tout faux » — ChinaBook pour revendeur (achat-revente, Vinted, Snap), 27,75 s.

Accroche de Youssef (06/10/2026) : tu passes par un fournisseur en Europe ou par des plateformes
(Hipobuy, Oopbuy) ? T'as tout faux. Ceux qui sont partis en Chine ont leur propre fournisseur et
leur propre transitaire. Ces plateformes sont pour ceux qui ne sont jamais venus. Moi j'ai cherché
sur place (Kinbo à Guangzhou, SEG à Shenzhen, photos à l'écran une seconde), j'ai trié, les
validés sont dans le ChinaBook.

Voix : moteur/outils/voix.py (Tomy, 3,8 mots/s). Chaque élément cite le mot qu'il illustre.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import kit as KM

DUREE = 27.75
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a
G = Globe()

GZ, SZ, PAR = (113.26, 23.13), (114.06, 22.54), (2.35, 48.86)

# ─────────────────────────────────────────── sous-titres
SOUS = SousTitres(K, [
    [(0, "Stop.", "r", -0.45)],
    [(1, "Tu"), (2, "fais"), (3, "de"), (4, "l’achat-revente,", "g")],
    [(5, "du"), (6, "Vinted,", "g"), (7, "ou"), (8, "tu"), (9, "vends"), (10, "sur"), (11, "ton"), (12, "Snap ?", "g")],
    [(13, "Et"), (14, "tu"), (15, "passes"), (16, "par"), (17, "un"), (18, "fournisseur"), (19, "en"), (20, "Europe,", "r")],
    [(21, "ou"), (22, "par"), (23, "Hipobuy,", "r"), (24, "Oopbuy ?", "r")],
    [(25, "T’as"), (26, "tout", "r"), (27, "faux.", "r")],
    [(28, "Ceux"), (29, "qui"), (30, "sont"), (31, "partis"), (32, "en"), (33, "Chine", "g")],
    [(34, "ont"), (35, "leur"), (36, "propre"), (37, "fournisseur", "g"), (38, "et"), (39, "leur"), (40, "propre"), (41, "transitaire.", "g")],
    [(42, "C’est"), (43, "moins", "g"), (44, "cher,", "g")],
    [(45, "et"), (46, "c’est"), (47, "comme"), (48, "ça"), (49, "que"), (50, "ça"), (51, "marche"), (52, "vraiment.", "g")],
    [(53, "Ces"), (54, "plateformes,"), (55, "c’est"), (56, "pour"), (57, "ceux"), (58, "qui")],
    [(59, "ne"), (60, "sont"), (61, "jamais", "r"), (62, "venus"), (63, "en"), (64, "Chine.")],
    [(65, "Moi,"), (66, "j’ai"), (67, "cherché"), (68, "sur"), (69, "place :", "g")],
    [(70, "à"), (71, "Kinbo,", "g"), (72, "à"), (73, "Guangzhou,")],
    [(74, "et"), (75, "au"), (76, "SEG,", "g"), (77, "à"), (78, "Shenzhen.")],
    [(79, "J’en"), (80, "ai"), (81, "testé"), (82, "plusieurs,", "g")],
    [(83, "j’ai"), (84, "fait"), (85, "le"), (86, "tri.", "g")],
    [(87, "Ceux"), (88, "que"), (89, "j’ai"), (90, "validés", "g"), (91, "sont"), (92, "dans"), (93, "le"), (94, "ChinaBook.", "g")],
    [(96, "Envoie-moi"), (97, "« CHINA »", "g"), (98, "sur"), (99, "WhatsApp.")],
    [(None, "Ton", "", 26.37), (None, "accès", "", 26.44), (None, "direct", "g", 26.53), (None, "à", "", 26.63), (None, "la", "", 26.68), (None, "Chine.", "", 26.74)],
])

# ─────────────────────────────────────────── fenêtres de scène
S1, S2, S3, S5 = (0.0, 1.0), (0.80, 3.80), (3.60, 8.25), (8.05, 11.78)
S6, S7, S8, S9, S10 = (11.55, 14.05), (13.85, 16.62), (16.42, 21.10), (20.88, 23.05), (22.85, 24.90)
T_CTA, T_FIN = 24.85, 26.30
TL = [TW(97) - 0.16 + k * 0.07 for k in range(5)]
T_ENVOI = TW(98)
T_KINBO, T_SEG = TW(71) - 0.06, TW(76) - 0.06
T_LOGO = TW(94) - 0.12


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
    """fenêtre de scène avec entrée et sortie : gauche, droite, haut, bas, zoom, ou None"""
    a, b = S
    if not (a <= t <= b): return None
    ue = prog(t, a, de, sortie) if ek else 1.0
    us = prog(t, b - ds, ds, entree) if sk else 0.0
    dx = dy = 0.0; s = 1.0; al = 1.0
    if ek == "gauche": dx += 1300 * (1 - ue)
    elif ek == "droite": dx -= 1300 * (1 - ue)
    elif ek == "bas": dy += 1500 * (1 - ue)
    elif ek == "haut": dy -= 1500 * (1 - ue)
    elif ek == "zoom": s *= mix(0.55, 1, ue); al *= ue
    if sk == "gauche": dx -= 1300 * us
    elif sk == "droite": dx += 1300 * us
    elif sk == "haut": dy -= 1500 * us
    elif sk == "bas": dy += 1500 * us
    elif sk == "zoom": s *= mix(1, 1.9, us); al *= (1 - us)
    return _Sc(c, (dx, dy, s, al))


def tel(c, cx, cy, ecran, w=480, h=960, alpha=1.0, **espace):
    with Espace(c, cx, cy, **espace):
        telephone(c, cx - w / 2, cy - h / 2, w, h, ecran, alpha)


def octogone(cx, cy, r):
    p = skia.Path()
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        (p.moveTo if k == 0 else p.lineTo)(cx + r * math.cos(a), cy + r * math.sin(a))
    p.close()
    return p


def drapeau_eu(c, x, y, w, h, r=7):
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#003399"))
    for k in range(12):
        a = 2 * math.pi * k / 12
        c.drawPath(etoile(x + w / 2 + h * 0.32 * math.cos(a), y + h / 2 + h * 0.32 * math.sin(a), h * 0.065), peinture("#FFCC00"))
    c.restore()


# ─────────────────────────────────────────── S1 · STOP
def s1(c, t):
    sc = scene(c, t, S1, None, "zoom", ds=0.2)
    if sc is None: return
    with sc:
        punch = 1.0 + 0.16 * (1 - prog(t, 0, 0.3, sortie))
        sx, sy = secousse(t, 0.0, 16, 0.4)
        c.save(); c.translate(540 + sx, 1060 + sy); c.rotate(-4 + 2 * math.sin(t * 6)); c.scale(punch, punch)
        ombre_sol(c, 0, 360, 260, 26, 0.16)
        pa = peinture(C["rouge"]); pa.setImageFilter(skia.ImageFilters.DropShadow(0, 24, 40, 40, hexa("#000000", 0.25)))
        c.drawPath(octogone(0, 0, 330), pa)
        c.drawPath(octogone(0, 0, 300), peinture(C["blanc"], Style=skia.Paint.kStroke_Style, StrokeWidth=14))
        icone(c, "hand", 0, -92, 150, C["blanc"], 2.4)
        texte_centre(c, "STOP", 0, 92, 150, C["blanc"])
        c.restore()


# ─────────────────────────────────────────── S2 · achat-revente, Vinted, Snap
STORIES = [("photos/chaussures/baskets-portees-marine", "Baskets", 1.05), ("photos/chaussures/baskets-portees-violettes", "Nouveau", 1.15),
           ("photos/chaussures/planche-baskets-12-modeles", "Dispo", 1.25), ("photos/mobilite/casque-moto-plateau", "Casques", 1.35)]
CHATS = [dict(nom="Inès", texte="Tu fais quelle taille ?", t=1.10, couleur="#10B981"),
         dict(nom="Sofiane", texte="T’as encore la bleue ?", t=TW(6), couleur="#3B82F6", badge=2),
         dict(nom="Léa", texte="Je les prends !", t=TW(9), couleur="#EC4899"),
         dict(nom="Yanis", texte="Dispo en gros ?", t=TW(12) - 0.05, couleur="#F59E0B", badge=1)]


def s2(c, t):
    sc = scene(c, t, S2, "zoom", "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        tel(c, 540, 1150, lambda cc, a, b, d, e: ecran_snap(cc, a, b, d, e, t, STORIES, CHATS), ry=-6 + 3 * math.sin(t * 2.0), rz=1.5 * math.sin(t * 2.6))
        for lab, t0, x, y, rot, coul, ic in (("ACHAT-REVENTE", TW(4) - 0.05, 300, 690, -6, C["vert"], "banknote"),
                                             ("VINTED", TW(6) - 0.05, 830, 760, 6, C["ink"], "shirt")):
            if t >= t0:
                u = prog(t, t0, 0.32, lambda v: rebond(v, 1.9))
                pastille_rot(c, lab, x, y, 36, coul, C["blanc"], rot, mix(0.3, 1, u), borne(u * 2), ic, (14, 32, 0.22))
        if t >= TW(12) - 0.08:
            u = prog(t, TW(12) - 0.08, 0.34, lambda v: rebond(v, 2.0))
            c.save(); c.translate(860, 1360); c.rotate(10); c.scale(u, u); logo_app(c, "snapchat", 0, 0, 150); c.restore()


# ─────────────────────────────────────────── S3 · Europe, Hipobuy, Oopbuy… t'as tout faux
CARTES3 = [("Fournisseur en Europe", "Revendeur", "eu", TW(13) + 0.05, 780),
           ("Hipobuy", "Plateforme d’achat", "globe", TW(23) - 0.05, 1010),
           ("Oopbuy", "Plateforme d’achat", "globe", TW(24) - 0.05, 1240)]


def s3(c, t):
    sc = scene(c, t, S3, "bas", "haut")
    if sc is None: return
    with sc:
        sx, sy = secousse(t, TW(27), 18, 0.4)
        c.save(); c.translate(sx, sy)
        for k, (titre, sous, ic, t0, cy) in enumerate(CARTES3):
            ug = prog(t, S3[0] + 0.2 + 0.1 * k, 0.35, lambda v: rebond(v, 1.7)) * (1 - prog(t, t0 - 0.05, 0.15))
            if k > 0 and ug > 0:
                c.save(); c.translate(540, cy); c.scale(mix(0.6, 1, ug), mix(0.6, 1, ug))
                with Calque(c, borne(ug * 2)):
                    rrect(c, -430, -95, 860, 190, 40, C["fondDoux"], 1.0, None, "#D5DBD8", 4)
                    disque(c, -334, 0, 50, "#E3E8E5"); icone(c, "circle-help", -334, 0, 60, C["grisClair"], 2.2)
                    rrect(c, -248, -40, 360, 34, 17, "#E3E8E5"); rrect(c, -248, 14, 220, 24, 12, "#E3E8E5")
                c.restore()
            if t < t0: continue
            u = prog(t, t0, 0.4, lambda v: rebond(v, 1.6))
            tx = TW(25) + 0.08 * k
            x_ = prog(t, tx, 0.22, lambda v: rebond(v, 2.2))
            with Espace(c, 540, cy, rx=mix(70, 0, u)):
                c.save(); c.translate(540 + 900 * (1 - u), cy)
                with Calque(c, borne(u * 2) * mix(1, 0.6, x_)):
                    carte(c, -430, -95, 860, 190, 40, C["blanc"], 1.0, (20, 44, 0.14))
                    rrect(c, -394, -60, 120, 120, 30, C["rougeDoux"])
                    if ic == "eu": drapeau_eu(c, -374, -36, 80, 54)
                    else: icone(c, ic, -334, 0, 74, C["rouge"], 2.3)
                    texte(c, titre, -248, -62, ajuste(titre, 450, 46), C["ink"], "noir")
                    texte(c, sous, -248, 2, 28, C["gris"], "demi", track=0)
                    if x_ > 0: trait(c, -250, 0, -250 + 470 * prog(t, tx, 0.18, sortie), 0, C["rouge"], 10)
                c.restore()
                um = prog(t, t0 + 0.22, 0.3, lambda v: rebond(v, 2.0))
                if um > 0 and x_ <= 0:
                    pastille_rot(c, "+ MARGE", 840, cy - 52, 30, C["rouge"], C["blanc"], 7, mix(0.3, 1, um), borne(um * 2))
                if x_ > 0:
                    c.save(); c.translate(870, cy); c.scale(x_, x_)
                    disque(c, 0, 0, 62, C["rouge"], 1.0, (10, 26, 0.25)); icone(c, "x", 0, 0, 70, C["blanc"], 3.8)
                    c.restore()
        c.restore()
        tampon(c, "TOUT FAUX", 540, 1440, t, TW(27), 84, C["rouge"], -7, "octagon-x")


# ─────────────────────────────────────────── S5 · partis en Chine : leur fournisseur, leur transitaire
def s5(c, t):
    sc = scene(c, t, S5, "zoom", "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1110, 410
        lon0 = cles(t, [(S5[0], 30), (TW(33), 78, entreeSortie)]); lat0 = 34
        G.disque(c, cx, cy, R); G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2})
        pv = prog(t, TW(28), TW(33) - TW(28) + 0.1, entreeSortie)
        G.arc(c, PAR, GZ, cx, cy, R, lon0, lat0, 1.0, "#CBD5CF", 5, 0.3, [2, 16], borne(pv * 4))
        x_, y_, z_ = G.arc(c, PAR, GZ, cx, cy, R, lon0, lat0, pv, C["ink"], 6, 0.3, [2, 16])
        if 0 < pv < 1 and z_ > 0:
            c.save(); c.translate(x_, y_); c.rotate(-20); disque(c, 0, 0, 40, C["ink"], 1.0, (8, 20, 0.2)); icone(c, "plane", 0, 0, 46, C["blanc"], 2.4); c.restore()
        G.repere(c, *PAR, cx, cy, R, lon0, lat0, "EUROPE", C["ink"], None, prog(t, S5[0] + 0.15, 0.4, lambda v: rebond(v, 1.8)), 1.0, 70)
        G.repere(c, *GZ, cx, cy, R, lon0, lat0, "CHINE", C["vert"], "CN", prog(t, TW(33) - 0.05, 0.4, lambda v: rebond(v, 1.8)), 1.0, 80)
        pr = prog(t, TW(41) - 0.1, 0.8, entreeSortie)
        if pr > 0:
            G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, 1.0, "#CDEFDC", 6, 0.36)
            x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, pr, C["vert"], 8, 0.36)
            if pr < 1 and z_ > 0: carton(c, x_, y_ - 20, 96, 0, 1.0, 8 * math.sin(t * 9))
            if pr >= 1: onde(c, *G.pos(*PAR, lon0, lat0, R, cx, cy)[:2], t, TW(41) + 0.7, 20, 110, C["vert"], 5)
        for lab, ic, t0, x, y, rot in (("SON FOURNISSEUR", "store", TW(37) - 0.08, 330, 700, -6), ("SON TRANSITAIRE", "truck", TW(41) - 0.08, 740, 1420, 5)):
            if t >= t0:
                u = prog(t, t0, 0.34, lambda v: rebond(v, 1.9))
                pastille_rot(c, lab, x, y, 34, C["vert"], C["blanc"], rot, mix(0.3, 1, u), borne(u * 2), ic, (14, 32, 0.22))


# ─────────────────────────────────────────── S6 · moins cher : plateforme contre direct
def s6(c, t):
    sc = scene(c, t, S6, "droite", "haut", de=0.28, ds=0.22)
    if sc is None: return
    with sc:
        base, wb = 1400, 270
        for k, (cx, lab, marges) in enumerate(((320, "Plateforme", 2), (760, "En direct", 0))):
            u = prog(t, S6[0] + 0.1 + 0.1 * k, 0.45, lambda v: rebond(v, 1.5))
            h0 = 300 * u
            rrect(c, cx - wb / 2, base - h0, wb, h0, 26, C["vert"], borne(u * 2))
            for m in range(marges):
                um = prog(t, S6[0] + 0.35 + 0.16 * m, 0.34, lambda v: rebond(v, 1.7))
                if um <= 0: continue
                hm = 200 * um; y0 = base - 300 - 12 - m * 212
                rrect(c, cx - wb / 2, y0 - hm, wb, hm, 26, C["rouge"], borne(um * 2))
                texte_centre(c, "+ marge", cx, y0 - hm / 2, 44, C["blanc"], alpha=borne(um * 2))
            texte_centre(c, "Prix Chine", cx, base - 150 * u, 40, C["blanc"], "fort", borne(u * 2) * borne((u - 0.6) * 3), 0)
            texte_centre(c, lab, cx, base + 60, 44, C["ink"], "noir", borne(u * 2))
        if t >= TW(44) - 0.1:
            c.save(); c.translate(760, base - 380); c.scale(battement(t, TW(44), 0.12, 0.3), battement(t, TW(44), 0.12, 0.3))
            disque(c, 0, 0, 56, C["ink"], 1.0, (10, 26, 0.25)); icone(c, "check", 0, 0, 62, C["blanc"], 3.6)
            c.restore()
        if t < TW(51) - 0.1: tampon(c, "MOINS CHER", 760, 850, t, TW(44), 58, C["vert"], 8, "banknote")
        if t >= TW(51) - 0.1:
            u = prog(t, TW(51) - 0.1, 0.34, lambda v: rebond(v, 1.9))
            pastille_rot(c, "LA VRAIE MÉTHODE", 760, 850, 34, C["ink"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "badge-check", (14, 32, 0.22))
            confettis(c, 760, 850, t, TW(52), 18, 260, 4)


# ─────────────────────────────────────────── S7 · les plateformes : pour ceux qui ne sont jamais venus
def passeport(c, cx, cy, s, rot):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    carte(c, -230, -320, 460, 640, 34, "#173A2F", 1.0, (26, 60, 0.3))
    rrect(c, -206, -296, 412, 592, 24, "#173A2F", 1.0, None, "#C9A646", 3)
    texte_centre(c, "PASSEPORT", 0, -190, 50, "#C9A646", "noir", track=0.12)
    icone(c, "globe", 0, 10, 190, "#C9A646", 1.6)
    rrect(c, -60, 190, 120, 70, 12, "#173A2F", 1.0, None, "#C9A646", 3)
    c.restore()


def s7(c, t):
    sc = scene(c, t, S7, "gauche", "zoom", de=0.28, ds=0.2)
    if sc is None: return
    with sc:
        u = prog(t, S7[0] + 0.05, 0.45, lambda v: rebond(v, 1.5))
        passeport(c, 540, 1080 + 10 * math.sin(t * 3), mix(0.6, 1, u), -5 + 2 * math.sin(t * 2.4))
        for k, (lab, x, y, rot) in enumerate((("Hipobuy", 250, 700, -8), ("Oopbuy", 830, 760, 7))):
            ul = prog(t, TW(54) - 0.05 + 0.1 * k, 0.32, lambda v: rebond(v, 1.9))
            if ul > 0:
                bob = 10 * math.sin(t * 3 + k * 2)
                pastille_rot(c, lab, x, y + bob, 36, C["blanc"], C["ink"], rot, mix(0.3, 1, ul), borne(ul * 2), "globe", (14, 32, 0.18))
        tampon(c, "JAMAIS VENU", 560, 1160, t, TW(61), 70, C["rouge"], -12, "x")
        if t >= TW(64) - 0.1:
            ue = prog(t, TW(64) - 0.1, 0.34, lambda v: rebond(v, 1.9))
            c.save(); c.translate(770, 1420); c.rotate(5); c.scale(mix(0.4, 1, ue), mix(0.4, 1, ue))
            w, h = pastille(c, "EN CHINE", 28, 0, 36, C["ink"], C["blanc"], None, borne(ue * 2), (14, 32, 0.22))
            drapeau(c, "CN", -w / 2 - 60, -26, 60, 40, 6)
            c.restore()


# ─────────────────────────────────────────── S8 · sur place : Kinbo (Guangzhou), SEG (Shenzhen)
def photo_lieu(c, t, nom, t0, t1, cx, cy, w, h, rot, label, ville):
    if not (t0 - 0.12 <= t <= t1 + 0.26): return
    u = prog(t, t0 - 0.12, 0.3, lambda v: rebond(v, 1.5))
    out = prog(t, t1, 0.24, entree)
    c.save(); c.translate(cx + 1300 * out * (1 if rot > 0 else -1), cy - 200 * out); c.rotate(rot * mix(2.5, 1, u)); s = mix(1.6, 1, u); c.scale(s, s)
    with Calque(c, borne(u * 3)):
        carte(c, -w / 2 - 18, -h / 2 - 18, w + 36, h + 36, 30, C["blanc"], 1.0, (26, 64, 0.28))
        z = 1.04 + 0.14 * prog(t, t0, t1 - t0 + 0.3, lin)
        image_cover(c, nom, -w / 2, -h / 2, w, h, z, 0.5, 0.45, rayon=18)
        f = 1 - (t - t0) / 0.12
        if 0 < f <= 1: c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), peinture("#FFFFFF", 0.75 * f))
        ul = prog(t, t0 + 0.1, 0.3, lambda v: rebond(v, 2.0))
        c.save(); c.translate(0, h / 2 + 30); c.rotate(-rot * 1.5); c.scale(mix(0.4, 1, ul), mix(0.4, 1, ul))
        pw, ph = pastille(c, label + " · " + ville, 30, 0, 38, C["ink"], C["blanc"], None, borne(ul * 2), (14, 32, 0.25))
        drapeau(c, "CN", -pw / 2 - 64, -27, 62, 42, 6)
        c.restore()
    c.restore()


def s8(c, t):
    sc = scene(c, t, S8, "droite", "zoom", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        tel(c, 540, 1144, lambda cc, a, b, d, e: video(cc, "videos/guangzhou/guangzhou-cartons-baskets-gros", a, b, d, e, t - S8[0], 1.0),
            ry=-8 + 3 * math.sin(t * 2.0), rz=-2 * math.sin(t * 2.7), s=mix(1.0, 0.92, prog(t, T_KINBO - 0.1, 0.3)))
        if TW(69) - 0.08 <= t < T_KINBO + 0.1:
            u = prog(t, TW(69) - 0.08, 0.34, lambda v: rebond(v, 1.9))
            pastille_rot(c, "SUR PLACE", 300, 720, 38, C["vert"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "map-pin", (14, 32, 0.22))
        photo_lieu(c, t, "lieux/kinbo-devanture-guangzhou", T_KINBO, T_KINBO + 1.0, 540, 1090, 560, 746, -4, "KINBO", "GUANGZHOU")
        photo_lieu(c, t, "lieux/seg-electronics-market-shenzhen", T_SEG, T_SEG + 1.0, 540, 1060, 840, 630, 4, "SEG", "SHENZHEN")


# ─────────────────────────────────────────── S9 · testé plusieurs, fait le tri
FOURN = [("photos/chaussures/baskets-portees-grises", "Guangzhou"), ("photos/chaussures/etagere-baskets-running-6-modeles", "Guangzhou"),
         ("photos/fabrication/couture-semelle", "Guangzhou"), ("photos/mobilite/casque-moto-plateau", "Shenzhen"),
         ("photos/chaussures/planche-baskets-12-modeles", "Guangzhou"), ("photos/chaussures/baskets-portees-violettes", "Guangzhou")]
GARDES = {1, 4}
POS9 = [(305, 780), (775, 780), (305, 1030), (775, 1030), (305, 1280), (775, 1280)]
T_TRI = [TW(83) - 0.05 + 0.08 * j for j in range(4)]


def s9(c, t):
    sc = scene(c, t, S9, "bas", None, de=0.28)
    if sc is None: return
    with sc:
        rejets = [k for k in range(6) if k not in GARDES]
        vol = prog(t, S9[1] - 0.25, 0.25, entree)
        for k, ((img, ville), (cx, cy)) in enumerate(zip(FOURN, POS9)):
            t0 = TW(79) + 0.06 * k
            u = prog(t, t0, 0.36, lambda v: rebond(v, 1.7))
            if u <= 0: continue
            dy = rot = 0.0; al = 1.0; x_ = 0.0; f = 0.0
            if k in rejets:
                tr = T_TRI[rejets.index(k)]
                x_ = prog(t, tr, 0.2, lambda v: rebond(v, 2.2))
                f = prog(t, tr + 0.3, 0.45, entree)
                dy, rot, al = 60 * f, (10 if k % 2 else -10) * f, 1 - f
            else:
                cx, cy = mix(cx, 540, vol), mix(cy, 1144, vol)
            if al <= 0: continue
            c.save(); c.translate(cx, cy + dy); c.rotate(rot); s = mix(0.4, 1, u) * mix(1, 0.6, vol if k in GARDES else 0) * (mix(1, 0.7, f) if k in rejets else 1); c.scale(s, s)
            with Calque(c, borne(u * 2) * al):
                ok = k in GARDES and t >= TW(86) - 0.05
                carte(c, -215, -105, 430, 210, 34, C["blanc"], 1.0, (16, 36, 0.14), C["vert"] if ok else None, 6 if ok else 0)
                KM._cercle_image(c, img, -135, 0, 62, 1.3)
                texte(c, "Fournisseur", -55, -52, 34, C["ink"], "noir", track=0)
                texte(c, ville, -55, -8, 24, C["gris"], "demi", track=0)
                rrect(c, -55, 38, 200, 16, 8, C["ligne"])
                if x_ > 0:
                    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-215, -105, 430, 210), 34, 34), peinture(C["rouge"], 0.18 * x_))
            c.restore()
            if x_ > 0 and al > 0:
                c.save(); c.translate(cx + 170, cy - 70 + dy); c.scale(x_, x_)
                disque(c, 0, 0, 44, C["rouge"], 1.0, (10, 26, 0.25)); icone(c, "x", 0, 0, 50, C["blanc"], 3.8)
                c.restore()
            if k in GARDES and t >= TW(86) - 0.05:
                uv = prog(t, TW(86) - 0.05, 0.3, lambda v: rebond(v, 2.0))
                c.save(); c.translate(cx + 170 * mix(1, 0.6, vol), cy - 70 * mix(1, 0.6, vol)); c.scale(uv, uv)
                disque(c, 0, 0, 44, C["vert"], 1.0, (10, 26, 0.25)); icone(c, "check", 0, 0, 50, C["blanc"], 3.8)
                c.restore()
        tampon(c, "TRIÉS", 540, 1430, t, TW(86), 64, C["ink"], -6, "list-filter")


# ─────────────────────────────────────────── S10 · les validés dans le ChinaBook
def s10(c, t):
    sc = scene(c, t, S10, None, None)
    if sc is None: return
    with sc:
        e = prog(t, S10[0] + 0.1, 0.4, sortie)
        lignes = [dict(t=TW(88), image="photos/chaussures/etagere-baskets-running-6-modeles", nom="Baskets", ville="Guangzhou", zoom=1.7, fx=0.5, fy=0.28),
                  dict(t=TW(90) - 0.05, image="photos/chaussures/planche-baskets-12-modeles", nom="Sneakers", ville="Guangzhou"),
                  dict(t=TW(91), image="photos/mobilite/casque-moto-plateau", nom="Électronique", ville="Shenzhen", fy=0.55)]
        tel(c, 540, 1144, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-30, -4, e) + 2 * math.sin(t * 2.2), s=mix(0.6, 1, e), alpha=borne(e * 2))
        tampon(c, "VALIDÉS", 790, 760, t, TW(90), 58, C["vert"], -8, "badge-check")
        confettis(c, 790, 760, t, TW(90) + 0.04, 22, 320, 9)


def disque_logo(c, t):
    """disque vert plein écran, logo blanc qui claque sur « ChinaBook », puis ouverture sur l'appel à l'action"""
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (T_CTA - 0.12, 1750), (T_CTA + 0.3, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, C["ink"])
        if T_LOGO + 0.2 <= t <= T_CTA + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, T_CTA - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * so)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2, lw, borne(u * 3) * (1 - so))
    return r


# ─────────────────────────────────────────── sons, flou, éclairs
son(0.0, "impact", -5); son(0.0, "tampon", -8); son(0.02, "whoosh_court", -12); son(0.3, "ding", -14); son(0.80, "whoosh", -13)
for k in range(4): son(1.05 + k * 0.1, "pop", -16)
son(1.10, "message_in", -12); son(TW(4) - 0.05, "pop", -11); son(TW(6) - 0.05, "pop", -11); son(TW(6), "message_in", -12)
son(TW(9), "message_in", -12); son(TW(12) - 0.08, "pop", -10); son(TW(12) - 0.05, "message_in", -12); son(3.58, "whoosh", -13)
for k, (_, _, _, t0, _) in enumerate(CARTES3):
    son(t0, "whoosh_court", -14); son(t0 + 0.05, "pop", -13); son(t0 + 0.22, "tampon", -13)
for k in range(3): son(TW(25) + 0.08 * k, "impact_doux", -10)
son(TW(27) - 0.1, "tampon", -6); son(TW(27) - 0.08, "impact", -7); son(8.03, "whoosh_long", -13)
son(TW(28), "whoosh_long", -15); son(TW(33), "pop", -11); son(TW(37) - 0.08, "pop", -11); son(TW(37), "check", -13)
son(TW(41) - 0.1, "whoosh_long", -14); son(TW(41) - 0.08, "pop", -11); son(TW(41) + 0.7, "ding", -13); son(11.53, "whoosh", -13)
for k in range(2): son(S6[0] + 0.1 + 0.1 * k, "pop", -14)
for m in range(2): son(S6[0] + 0.35 + 0.16 * m, "croc", -12)
son(TW(44) - 0.1, "tampon", -8); son(TW(44), "ching", -10); son(TW(51) - 0.1, "pop", -11); son(TW(52), "ding", -13); son(13.83, "whoosh", -13)
son(S7[0] + 0.05, "swipe", -14); son(TW(54) - 0.05, "pop", -13); son(TW(54) + 0.05, "pop", -13)
son(TW(61) - 0.1, "tampon", -7); son(TW(61) - 0.08, "impact_doux", -9); son(TW(64) - 0.1, "pop", -11); son(16.40, "whoosh", -13)
son(S8[0] + 0.05, "swipe", -15); son(TW(69) - 0.08, "pop", -11)
for tt in (T_KINBO, T_SEG):
    son(tt - 0.12, "whoosh_court", -12); son(tt, "clic", -9); son(tt + 0.1, "pop", -12); son(tt + 1.0, "whoosh_court", -14)
son(20.86, "whoosh", -13)
for k in range(6): son(TW(79) + 0.06 * k, "pop", -15)
for tr in T_TRI: son(tr, "impact_doux", -10); son(tr + 0.3, "whoosh_court", -17)
son(TW(86) - 0.05, "check", -11); son(TW(86) - 0.1, "tampon", -9); son(S9[1] - 0.25, "whoosh", -14)
son(TW(88), "pop", -12); son(TW(90) - 0.05, "pop", -12); son(TW(91), "pop", -12); son(TW(90) - 0.1, "tampon", -9); son(TW(90) + 0.04, "ching", -11)
son(T_LOGO - 0.1, "montee", -15); son(T_LOGO + 0.24, "impact", -7); son(T_LOGO + 0.26, "verre", -9); son(T_CTA - 0.1, "whoosh_long", -14)
for tl in TL: son(tl, "frappe", -13)
son(T_ENVOI, "clic", -10); son(T_ENVOI + 0.04, "whoosh_court", -13); son(T_ENVOI + 0.16, "message", -10)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.14, "impact_doux", -8); son(T_FIN + 0.16, "verre", -8); son(T_FIN + 0.36, "pop", -11)

for a, b in [(0.78, 1.1), (3.58, 3.9), (TW(25), TW(25) + 0.3), (TW(27) - 0.12, TW(27) + 0.1), (8.03, 8.4), (11.53, 11.85),
             (13.83, 14.15), (16.40, 16.75), (T_KINBO - 0.14, T_KINBO + 0.12), (T_KINBO + 0.98, T_KINBO + 1.26), (T_SEG - 0.14, T_SEG + 0.12),
             (T_SEG + 0.98, T_SEG + 1.26), (20.86, 21.2), (T_TRI[0] + 0.3, T_TRI[-1] + 0.75), (S9[1] - 0.25, S9[1] + 0.3),
             (T_LOGO, T_LOGO + 0.4), (T_CTA - 0.12, T_CTA + 0.32), (T_ENVOI, T_ENVOI + 0.32), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, C["rouge"], 0.14), (TW(25), C["rouge"], 0.10), (TW(27) - 0.08, C["rouge"], 0.12), (TW(37), C["vert"], 0.08),
                    (TW(44), C["vert"], 0.10), (TW(61) - 0.08, C["rouge"], 0.10), (T_KINBO, "#FFFFFF", 0.25), (T_SEG, "#FFFFFF", 0.25),
                    (TW(86), C["vert"], 0.10), (TW(90), C["vert"], 0.08), (T_LOGO + 0.24, C["blanc"], 0.15), (T_FIN + 0.14, C["vert"], 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def alpha_bandeau(t, r):
    return borne(prog(t, 0.95, 0.3) * (1 - prog(t, T_FIN - 0.05, 0.25)) * (1 - borne(r / 400)))


def dessine(c, t):
    fond(c, t)
    for s in (s1, s2, s3, s5, s6, s7, s8, s9, s10):
        s(c, t)
    r = disque_logo(c, t)
    bandeau(c, t, alpha_bandeau(t, r))
    cta_whatsapp(c, t, T_CTA, TL, T_ENVOI, T_FIN, DUREE)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if r > 900 else C["ink"])
