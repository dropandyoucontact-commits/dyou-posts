"""DY-M01 « Ton agent en Chine » — présentation de DROP&YOU (31,6 s), en violet.

Brief de Youssef (06/10/2026) : bienvenue chez DROP&YOU, ton agent en Chine ; baskets, vêtements,
électronique, montres, large catalogue ; envoie la photo de l'article, on te donne le prix selon les
qualités, livraison incluse, 8 à 12 jours jusqu'en France, en Belgique ou partout ; acheteur ou
revendeur en gros ; PayPal, virement, carte ; Snap (dropandyou1) ou WhatsApp ; dernier appel vers
le ChinaBook pour acheter aux fournisseurs. DROP&YOU = violet ; la partie ChinaBook repasse au vert.

Voix : moteur/outils/voix.py (Tomy, 3,8 mots/s). Chaque élément cite le mot qu'il illustre.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import kit as KM

DUREE = 31.65
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a

VIOLET = dict(vert="#7C3AED", vertFonce="#5B21B6", vertDoux="#EDE9FE", vertMoyen="#C4B5FD")
VERT = dict(vert="#00B862", vertFonce="#00804A", vertDoux="#E2F7EB", vertMoyen="#9BE3BD")
C.update(VIOLET)
T_CB = TW(96) - 0.08            # « Et si tu veux faire comme moi… » : on passe au ChinaBook, donc au vert


class GlobeV(Globe):
    COUL = {0: "#CFC4EE", 1: "#7C3AED", 2: "#0B0F0D", 3: "#9A93AE", 4: "#C2B6E8"}

    def disque(self, c, cx, cy, R, alpha=1.0):
        with Calque(c, alpha):
            ombre_sol(c, cx, cy + R * 1.06, R * 0.78, R * 0.09, 0.14)
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx - R * 0.3, cy - R * 0.35), R * 1.5,
                                                       [hexa("#FFFFFF"), hexa("#F1ECFC")], [0.0, 1.0]))
            c.drawCircle(cx, cy, R, p)
            anneau(c, cx, cy, R, "#DDD3F5", 3)


G = GlobeV()
GZ, PAR, BRU = (113.26, 23.13), (2.35, 48.86), (4.35, 50.85)
MONDE = [(-17.4, 14.7), (28.0, -26.2), (55.3, 25.2), (37.6, 55.75), (103.8, 1.35)]

# ─────────────────────────────────────────── sous-titres
SOUS = SousTitres(K, [
    [(0, "Bienvenue", "", -0.45), (1, "chez", "", -0.3), (2, "DROP&YOU,", "g")],
    [(5, "ton"), (6, "agent", "g"), (7, "en"), (8, "Chine.")],
    [(9, "Baskets,", "g"), (10, "vêtements,", "g")],
    [(11, "électronique,", "g"), (12, "montres :", "g")],
    [(13, "on"), (14, "a"), (15, "un"), (16, "large", "g"), (17, "catalogue.", "g")],
    [(18, "Tu"), (19, "peux"), (20, "aussi"), (21, "nous"), (22, "envoyer"), (23, "la"), (24, "photo", "g"), (25, "de"), (26, "l’article"), (27, "que"), (28, "tu"), (29, "veux.")],
    [(30, "Selon"), (31, "les"), (32, "qualités,", "g"), (33, "on"), (34, "te"), (35, "donne"), (36, "le"), (37, "prix,", "g")],
    [(38, "livraison", "g"), (39, "incluse :", "g")],
    [(40, "8"), (41, "à"), (42, "12", "g"), (43, "jours", "g"), (44, "jusqu’à"), (45, "chez"), (46, "toi,")],
    [(47, "en"), (48, "France,", "g"), (49, "en"), (50, "Belgique,", "g")],
    [(51, "ou"), (52, "n’importe"), (53, "où"), (54, "dans"), (55, "le"), (56, "monde.", "g")],
    [(57, "Que"), (58, "tu"), (59, "achètes"), (60, "juste"), (61, "pour"), (62, "t’habiller,", "g")],
    [(63, "ou"), (64, "que"), (65, "tu"), (66, "sois"), (67, "revendeur", "g"), (68, "et"), (69, "que"), (70, "tu"), (71, "prennes"), (72, "en"), (73, "gros.", "g")],
    [(74, "Tu"), (75, "paies"), (76, "par"), (77, "PayPal,", "g"), (78, "par"), (79, "virement", "g")],
    [(80, "ou"), (81, "par"), (82, "carte"), (83, "bancaire.", "g")],
    [(84, "Envoie-moi"), (85, "un"), (86, "message"), (87, "sur"), (88, "Snap,", "g"), (89, "dropandyou1,", "g")],
    [(93, "ou"), (94, "sur"), (95, "WhatsApp.", "g")],
    [(96, "Et"), (97, "si"), (98, "tu"), (99, "veux"), (100, "faire"), (101, "comme"), (102, "moi,")],
    [(103, "et"), (104, "acheter"), (105, "directement", "g"), (106, "aux"), (107, "fournisseurs,", "g")],
    [(108, "c’est"), (109, "possible"), (110, "avec"), (111, "le"), (112, "ChinaBook.", "g")],
    [(None, "Les", "", 30.12), (None, "fournisseurs", "", 30.2), (None, "en", "", 30.36), (None, "direct.", "g", 30.42)],
])

# ─────────────────────────────────────────── fenêtres de scène
S1, S2, S3, S4 = (0.0, 2.32), (2.20, 6.42), (6.30, 11.62), (11.50, 15.92)
S5, S6, S7, S8 = (15.80, 19.70), (19.58, 22.24), (22.12, 25.48), (25.36, 29.40)
T_LOGO = TW(112) - 0.15
T_FIN = 29.95


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


def apparait(t, t0, s=1.9, d=0.34):
    return prog(t, t0, d, lambda v: rebond(v, s))


def image_contenue(cc, nom, a, b, d, e, zoom=1.0, fond="#FFFFFF"):
    """photo produit sur fond blanc : affichée entière (« contain »), jamais recadrée"""
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture(fond))
    iw, ih = taille_img(nom)
    s_ = min(d / iw, e / ih) * 0.94 * zoom
    w_, h_ = iw * s_, ih * s_
    cc.save(); cc.clipRect(skia.Rect.MakeXYWH(a, b, d, e))
    image(cc, nom, a + (d - w_) / 2, b + (e - h_) / 2, w_)
    cc.restore()


def flash(cc, a, b, d, e, t, coupes):
    for ct in coupes:
        f = 1 - (t - ct) / 0.09
        if 0 < f <= 1: cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#FFFFFF", 0.7 * f))


# ─────────────────────────────────────────── S1 · le téléphone en 3D d'où jaillissent les baskets
# Hook (retour de Youssef, 08/10/2026) : plus de grand logo qui répète le sous-titre. Dès l'image 0,
# un téléphone en perspective sur fond violet, des baskets du catalogue qui sortent de l'écran vers
# la caméra ; puis le violet rentre dans le téléphone, qui se redresse dans la pose exacte de S2.
D3 = 1800.0
JAILLIT = [("hook/c22", -0.36, (-0.34, 0.12), 1), ("hook/c05", 0.12, (0.6, -0.3), -1), ("hook/c08", 0.38, (-0.6, 0.35), 1),
           ("hook/c11", 0.64, (0.5, 0.5), -1), ("hook/c09", 0.90, (-0.2, -0.7), 1), ("hook/c22", 1.12, (0.45, -0.2), -1)]
VIE = 0.72


def pose_s1(t):
    """pose du téléphone : orbite en 3D, puis arrivée sur la pose de S2 à S2[0]"""
    rx = cles(t, [(0.0, 48), (1.25, 30, douce), (S2[0], 0, entreeSortie)])
    ry = cles(t, [(0.0, -30), (1.25, 22, douce), (S2[0], -6 + 3 * math.sin(S2[0] * 2.2), entreeSortie)])
    rz = cles(t, [(0.0, -10), (1.25, 9, douce), (S2[0], 1.5 * math.sin(S2[0] * 2.7), entreeSortie)])
    cy_ = cles(t, [(0.0, 1260), (1.25, 1160, douce), (S2[0], 1100, entreeSortie)])
    w = cles(t, [(0.0, 640), (1.25, 560, douce), (S2[0], 480, entreeSortie)])
    return rx, ry, rz, cy_, w


def ecran_hook(cc, a, b, d, e, t):
    ecran_catalogue(cc, a, b, d, e, t, -0.6)
    # lueur de l'écran à chaque basket qui sort
    for nom, t0, _, _ in JAILLIT:
        f = 1 - (t - t0) / 0.22
        if 0 < f <= 1: cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#FFFFFF", 0.55 * f))


def basket_volante(c, nom, t, t0, direc, sens, cx, cy):
    u = (t - t0) / VIE
    if not (0 <= u <= 1): return None
    v = sortie(u) * 0.35 + u ** 1.7 * 0.65
    X = direc[0] * 620 * v
    Y = direc[1] * 720 * v - 200 * math.sin(math.pi * min(1, u * 1.2))
    Z = -1560 * u ** 1.1
    f = D3 / (D3 + Z)
    x, y = cx + X * f, cy + Y * f
    w = 330 * f
    rot = sens * (-18 + 70 * u)
    al = borne(u / 0.06)
    iw, ih = taille_img(nom)
    c.save(); c.translate(x, y); c.rotate(rot)
    h_ = w * ih / iw
    om = skia.Paint(AntiAlias=True, ImageFilter=skia.ImageFilters.DropShadowOnly(0, 0.08 * w, 0.06 * w, 0.06 * w, skia.Color4f(0.1, 0.0, 0.25, 0.45 * al)))
    c.saveLayer(None, om); image(c, nom, -w / 2, -h_ / 2, w, al); c.restore()
    image(c, nom, -w / 2, -h_ / 2, w, al)
    c.restore()
    return Z


def s1(c, t):
    if t > S1[1]: return
    rx, ry, rz, cy_, w = pose_s1(t)
    # fond violet plein écran, qui rentre dans le téléphone sur « ton »
    r = cles(t, [(0.0, 1750), (TW(5) - 0.25, 1750), (TW(5) + 0.15, 0, entree)])
    if r > 1:
        disque(c, 540, cy_, r, C["vert"])
        # rayons de vitesse qui partent de l'écran
        with Calque(c, 0.16):
            for k in range(18):
                ang = k / 18 * 2 * math.pi + t * 0.6
                l0 = 260 + ((t * 2400 + k * 137) % 900)
                trait(c, 540 + math.cos(ang) * l0, cy_ + math.sin(ang) * l0, 540 + math.cos(ang) * (l0 + 220), cy_ + math.sin(ang) * (l0 + 220), "#FFFFFF", 10)
    if t < S2[0]:
        sx, sy = secousse(t, 0.0, 16, 0.3)
        for nom, t0, _, _ in JAILLIT: sx, sy = sx + secousse(t, t0, 7, 0.18)[0], sy + secousse(t, t0, 7, 0.18)[1]
        tel(c, 540 + sx, cy_ + sy, lambda cc, a, b, d, e: ecran_hook(cc, a, b, d, e, t), w=w, h=w * 2, rx=rx, ry=ry, rz=rz)
        for nom, t0, _, _ in JAILLIT:
            onde(c, 540, cy_, t, t0, 80, 420, "#FFFFFF", 7, 0.45)
    # les baskets volent devant tout, les plus proches dessinées en dernier
    vols = sorted(JAILLIT, key=lambda j: j[1])
    for nom, t0, direc, sens in vols:
        basket_volante(c, nom, t, t0, direc, sens, 540, cy_)
    # drapeau chinois en autocollant 3D sur « Chine »
    if t >= TW(8) - 0.1:
        u = apparait(t, TW(8) - 0.1, 2.0, 0.32)
        with Espace(c, 860, 760, ry=-28 + 10 * math.sin(t * 3), rx=12, rz=8):
            c.save(); c.translate(860, 760); c.scale(mix(0.2, 1, u), mix(0.2, 1, u))
            rrect(c, -98, -66, 196, 132, 24, "#FFFFFF", borne(u * 2), (14, 36, 0.25))
            drapeau(c, "CN", -82, -50, 164, 100, 14)
            c.restore()


# ─────────────────────────────────────────── S2 · catégories qui défilent dans le téléphone, puis le catalogue
CATALOGUE = [f"catalogue/c{k:02d}" for k in range(33)]
T_MONTRES, T_CATA = TW(12) - 0.08, TW(16) - 0.12


def ecran_catalogue(c, x, y, w, h, t, t0):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#FFFFFF"))
    gap, col = 16, (w - 3 * 16) / 2
    defil = (t - t0) * 1500
    hh = col + 70
    for k in range(40):
        r_, q = divmod(k, 2)
        yy = y + 190 + r_ * (hh + gap) - defil
        if yy > y + h or yy + hh < y + 150: continue
        xx = x + gap + q * (col + gap)
        rrect(c, xx, yy, col, hh, 22, "#F6F4FB")
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xx + 8, yy + 8, col - 16, col - 16), 16, 16), doAntiAlias=True)
        image_contenue(c, CATALOGUE[(k * 7) % len(CATALOGUE)], xx + 8, yy + 8, col - 16, col - 16)
        c.restore()
        rrect(c, xx + 14, yy + col + 6, col * 0.62, 14, 7, "#DCD6EA"); rrect(c, xx + 14, yy + col + 30, col * 0.36, 14, 7, C["vertMoyen"])
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 170), peinture(C["vert"]))
    texte(c, "9:41", x + 40, y + 24, 24, C["blanc"], "fort", track=0)
    iw, ih = taille_img("logo-dy-blanc"); image(c, "logo-dy-blanc", x + 34, y + 84, 250)
    rrect(c, x + w - 120, y + 78, 84, 64, 32, "#FFFFFF", 0.18); icone(c, "search", x + w - 78, y + 110, 30, C["blanc"], 2.6)


def ecran_s2(cc, a, b, d, e, t):
    coupes = []
    if t < TW(10) - 0.05:
        seq = [("chanel-noire", 0.5, 0.42), ("lv-noire", 0.5, 0.72), ("catalogue/c12", 0.5, 0.5), ("catalogue/c14", 0.5, 0.5)]
        t0 = TW(9) - 0.08; k = min(3, max(0, int((t - t0) / 0.17)))
        coupes = [t0 + 0.17 * j for j in range(1, 4)]
        nom, fx, fy = seq[k]
        z = 1.05 + 0.25 * ((t - t0) % 0.17) / 0.17
        if nom.startswith("catalogue/"): image_contenue(cc, nom, a, b, d, e, z)
        else: image_cover(cc, nom, a, b, d, e, z, fx, fy)
    elif t < TW(11) - 0.05:
        t0 = TW(10) - 0.05; k = 0 if t < t0 + 0.3 else 1
        coupes = [t0, t0 + 0.3]
        image_contenue(cc, ["catalogue/c02", "catalogue/c26"][k], a, b, d, e, 1.0 + 0.15 * (t - t0))
    elif t < T_MONTRES:
        t0 = TW(11) - 0.05; k = min(2, int((t - t0) / 0.24))
        coupes = [t0, t0 + 0.24, t0 + 0.48]
        nom, fx, fy = [("dyson-airwrap", 0.45, 0.5), ("dyson-supersonic", 0.55, 0.45), ("dyson-airstrait", 0.4, 0.55)][k]
        image_cover(cc, nom, a, b, d, e, 1.05 + 0.3 * ((t - t0) % 0.24) / 0.24, fx, fy)
    elif t < T_CATA:
        coupes = [T_MONTRES, T_MONTRES + 0.75]
        if t < T_MONTRES + 0.75:
            video(cc, "montres-bleues", a, b, d, e, t - T_MONTRES + 1.0, 1.4)
        else:
            video(cc, "montres-serties", a, b, d, e, t - T_MONTRES + 5.0, 1.8)
    else:
        coupes = [T_CATA]
        ecran_catalogue(cc, a, b, d, e, t, T_CATA)
    flash(cc, a, b, d, e, t, coupes)


CATS = [("BASKETS", TW(9), 270, 700, -6), ("VÊTEMENTS", TW(10), 820, 760, 6), ("ÉLECTRONIQUE", TW(11), 290, 1390, -5), ("MONTRES", TW(12), 800, 1420, 5)]


def s2(c, t):
    sc = scene(c, t, S2, None, "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        sx, sy = secousse(t, T_CATA, 10, 0.3)
        tel(c, 540 + sx, 1100 + sy, lambda cc, a, b, d, e: ecran_s2(cc, a, b, d, e, t), ry=-6 + 3 * math.sin(t * 2.2), rz=1.5 * math.sin(t * 2.7))
        for lab, t0, x, y, rot in CATS:
            if t0 - 0.08 <= t < T_CATA + 0.15:
                u = apparait(t, t0 - 0.08) * (1 - prog(t, T_CATA - 0.05, 0.2, entree))
                pastille_rot(c, lab, x, y, 38, C["vert"] if lab != "MONTRES" else C["ink"], C["blanc"], rot, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.22))
        tampon(c, "LARGE CATALOGUE", 540, 1420, t, TW(16), 60, C["vert"], -5, "store")
        confettis(c, 540, 1420, t, TW(17), 24, 360, 3, [C["vert"], C["vertMoyen"], C["ink"]])


# ─────────────────────────────────────────── S3 · envoie la photo, on te donne le prix selon les qualités
WA_FOND, WA_TETE, WA_MOI = "#EFEAE2", "#008069", "#D9FDD3"


def etoiles(c, x, y, n, taille=20, couleur="#F5B301"):
    for k in range(n):
        c.drawPath(etoile(x + k * taille * 1.15, y, taille / 2), peinture(couleur))


def ecran_whatsapp(c, x, y, w, h, t, msgs):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(WA_FOND))
    ys = y + 186
    hauteurs = []
    for m in msgs:
        if m["type"] == "image": hauteurs.append(300)
        elif m["type"] == "qualites": hauteurs.append(214)
        else: hauteurs.append(76)
    vis = [k for k, m in enumerate(msgs) if t >= m["t"] - 0.02]
    total = sum(hauteurs[k] + 16 for k in vis)
    decal = max(0, total - (h - 186 - 110))
    yy = ys - decal
    for k in vis:
        m = msgs[k]; hb = hauteurs[k]
        u = prog(t, m["t"], 0.3, lambda v: rebond(v, 1.6))
        moi = m["moi"]; wb = w * 0.72 if m["type"] != "texte" else min(w * 0.78, largeur(m["texte"], 26, "demi", 0) + 46)
        xb = x + w - 20 - wb if moi else x + 20
        c.save(); c.translate(xb + (wb if moi else 0), yy + hb); c.scale(mix(0.5, 1, u), mix(0.5, 1, u)); c.translate(-(xb + (wb if moi else 0)), -(yy + hb))
        with Calque(c, borne(u * 2)):
            rrect(c, xb, yy, wb, hb, 20, WA_MOI if moi else "#FFFFFF", 1.0, (2, 4, 0.12))
            if m["type"] == "image":
                image_cover(c, m["image"], xb + 8, yy + 8, wb - 16, hb - 16, 1.0, 0.5, 0.74, rayon=14)
            elif m["type"] == "qualites":
                for j, (lab, n) in enumerate(m["lignes"]):
                    ul = prog(t, m["t"] + 0.12 * j, 0.25)
                    yl = yy + 16 + j * 64
                    with Calque(c, ul):
                        rrect(c, xb + 12, yl, wb - 24, 54, 14, "#F4F1FB")
                        texte(c, lab, xb + 28, yl + 13, 24, C["ink"], "fort", track=0)
                        etoiles(c, xb + wb - 40 - (n - 1) * 23, yl + 27, n)
            else:
                texte(c, m["texte"], xb + 22, yy + 22, 26, C["ink"], "demi", track=0)
        c.restore()
        yy += hb + 16
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 170), peinture(WA_TETE))
    texte(c, "9:41", x + 40, y + 24, 24, C["blanc"], "fort", track=0)
    icone(c, "chevron-left", x + 34, y + 116, 34, C["blanc"], 2.6)
    disque(c, x + 96, y + 116, 34, "#FFFFFF"); image(c, "logo-dy", x + 96 - 26, y + 116 - 6, 52)
    texte(c, "DROP&YOU", x + 146, y + 88, 30, C["blanc"], "noir", track=0)
    texte(c, "en ligne", x + 146, y + 124, 21, "#CDEFE6", "demi", track=0)
    rrect(c, x + 16, y + h - 92, w - 110, 70, 35, "#FFFFFF")
    texte(c, "Message", x + 46, y + h - 74, 26, C["grisClair"], "moyen", track=0)
    disque(c, x + w - 54, y + h - 57, 35, WA_TETE); icone(c, "mic", x + w - 54, y + h - 57, 32, C["blanc"], 2.4)


MSGS3 = [dict(t=TW(22) - 0.05, moi=True, type="image", image="lv-noire"),
         dict(t=TW(27), moi=True, type="texte", texte="Tu as celle-ci ?"),
         dict(t=TW(31) - 0.05, moi=False, type="qualites", lignes=[("Qualité 1", 1), ("Qualité 2", 2), ("Qualité 3", 3)]),
         dict(t=TW(37) - 0.05, moi=False, type="texte", texte="Prix livraison incluse !")]


def s3(c, t):
    sc = scene(c, t, S3, "gauche", "gauche")
    if sc is None: return
    with sc:
        tel(c, 540, 1110, lambda cc, a, b, d, e: ecran_whatsapp(cc, a, b, d, e, t, MSGS3), ry=-5 + 2 * math.sin(t * 2))
        texte_centre(c, "Échange illustratif", 540, 1606, 22, C["grisClair"], "fort", 1.0, 0.04)
        if t >= TW(24) - 0.08:
            u = apparait(t, TW(24) - 0.08)
            pastille_rot(c, "ENVOIE LA PHOTO", 290, 690, 36, C["vert"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "camera", (14, 32, 0.22))
        if t >= TW(32) - 0.08:
            u = apparait(t, TW(32) - 0.08)
            pastille_rot(c, "SELON LA QUALITÉ", 830, 760, 34, C["ink"], C["blanc"], 6, mix(0.3, 1, u), borne(u * 2), "sparkles", (14, 32, 0.22))
        tampon(c, "LIVRAISON INCLUSE", 560, 1700, t, TW(38), 54, C["vert"], -5, "truck")


# ─────────────────────────────────────────── S4 · 8 à 12 jours, France, Belgique, partout
def s4(c, t):
    sc = scene(c, t, S4, "zoom", "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1110, 410
        lon0 = cles(t, [(S4[0], 95), (TW(46), 30, entreeSortie), (TW(52), 42, entreeSortie)]); lat0 = cles(t, [(S4[0], 30), (TW(46), 34, entreeSortie)])
        G.disque(c, cx, cy, R); G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2, 3: 1.3})
        G.repere(c, *GZ, cx, cy, R, lon0, lat0, "CHINE", C["vert"], "CN", apparait(t, S4[0] + 0.15, 1.8, 0.4), 1.0, 70)
        pr = prog(t, TW(40) - 0.1, TW(46) - TW(40) + 0.1, entreeSortie)
        if pr > 0:
            G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, 1.0, C["vertMoyen"], 6, 0.38)
            x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, pr, C["vert"], 8, 0.38)
            if pr < 1 and z_ > 0: carton(c, x_, y_ - 20, 96, 0, 1.0, 8 * math.sin(t * 9))
        G.repere(c, *PAR, cx, cy, R, lon0, lat0, "FRANCE", C["ink"], "FR", apparait(t, TW(48) - 0.05, 1.8, 0.4), 1.0, 120)
        G.repere(c, *BRU, cx, cy, R, lon0, lat0, "BELGIQUE", C["ink"], "BE", apparait(t, TW(50) - 0.05, 1.8, 0.4), 1.0, 50)
        for k, lieu in enumerate(MONDE):
            pm = prog(t, TW(52) + 0.1 * k, 0.55, entreeSortie)
            if pm > 0:
                x_, y_, z_ = G.arc(c, GZ, lieu, cx, cy, R, lon0, lat0, pm, C["vert"], 6, 0.3)
                if pm >= 1:
                    x2, y2, z2 = G.pos(*lieu, lon0, lat0, R, cx, cy)
                    if z2 > 0: disque(c, x2, y2, 10, C["vert"]); onde(c, x2, y2, t, TW(52) + 0.1 * k + 0.55, 10, 70, C["vert"], 4)
        if t >= TW(40) - 0.1:
            u = apparait(t, TW(40) - 0.1)
            pastille_rot(c, "8 À 12 JOURS", 300, 630, 44, C["ink"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "calendar", (14, 32, 0.25))
        if t >= TW(56) - 0.1:
            u = apparait(t, TW(56) - 0.1)
            pastille_rot(c, "PARTOUT DANS LE MONDE", 600, 1420, 38, C["vert"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "globe", (14, 32, 0.25))


# ─────────────────────────────────────────── S5 · pour t'habiller, ou revendeur en gros
T_GROS = TW(71) - 0.12


def s5(c, t):
    sc = scene(c, t, S5, "droite", "gauche", de=0.28, ds=0.22)
    if sc is None: return
    with sc:
        part = prog(t, T_GROS - 0.05, 0.35, entreeSortie)
        for k, (titre, sous, ic, img, t0, cy) in enumerate((("Pour t’habiller", "Acheteur", "shirt", "catalogue/c02", TW(57) - 0.1, 800),
                                                            ("Revendeur", "Prix de gros", "store", "carton-gros", TW(67) - 0.1, 1080))):
            u = apparait(t, t0, 1.5, 0.4)
            if u <= 0: continue
            c.save(); c.translate(540 + 900 * (1 - u), cy - 900 * part); c.rotate((-2 if k == 0 else 2) * (1 - part))
            carte(c, -440, -120, 880, 240, 44, C["blanc"], 1.0, (22, 50, 0.14))
            KM._cercle_image(c, img, -330, 0, 86, 1.2)
            texte(c, titre, -210, -58, ajuste(titre, 520, 54), C["ink"], "noir")
            rrect(c, -210, 18, largeur(sous, 28, "fort", 0) + 80, 52, 26, C["vertDoux"])
            icone(c, ic, -180, 44, 30, C["vertFonce"], 2.4)
            texte(c, sous, -152, 28, 28, C["vertFonce"], "fort", track=0)
            uc = apparait(t, [TW(62), TW(67) + 0.2][k], 2.0, 0.3)
            if uc > 0:
                c.save(); c.translate(380, -80); c.scale(uc, uc); disque(c, 0, 0, 44, C["vert"], 1.0, (8, 20, 0.2)); icone(c, "check", 0, 0, 50, C["blanc"], 3.6); c.restore()
            c.restore()
        # « pour t'habiller » : trois pièces du catalogue sous la carte, sorties avant « revendeur »
        for j, nom in enumerate(("catalogue/c26", "catalogue/c09", "catalogue/c22")):
            uj = apparait(t, TW(57) + 0.1 + 0.08 * j, 1.6, 0.35) * (1 - prog(t, TW(67) - 0.3, 0.22, entree))
            if uj <= 0: continue
            c.save(); c.translate(540 + (j - 1) * 300, 1170 + 80 * (1 - uj)); c.rotate((j - 1) * 4); c.scale(mix(0.5, 1, uj), mix(0.5, 1, uj))
            with Calque(c, borne(uj * 2)):
                carte(c, -130, -150, 260, 300, 32, C["blanc"], 1.0, (16, 40, 0.14))
                image_contenue(c, nom, -112, -132, 224, 264)
            c.restore()
        if t >= T_GROS - 0.05:
            sx, sy = secousse(t, TW(73), 12, 0.35)
            def ecran_gros(cc, a, b, d, e):
                if t < T_GROS + 0.55:
                    image_cover(cc, "carton-gros", a, b, d, e, 1.1 + 0.3 * (t - T_GROS), 0.5, 0.5)
                else:
                    video(cc, "entrepot-cartons", a, b, d, e, t - T_GROS, 1.0)
                flash(cc, a, b, d, e, t, [T_GROS, T_GROS + 0.55])
            tel(c, 540 + sx, mix(2300, 1110, part) + sy, ecran_gros, ry=-4 + 2 * math.sin(t * 2))
        tampon(c, "EN GROS", 760, 1400, t, TW(73), 70, C["rouge"], 7, "package")


# ─────────────────────────────────────────── S6 · PayPal, virement, carte
def logo_paypal(c, x, y, taille):
    w1 = largeur("Pay", taille, "noir", -0.02)
    texte(c, "Pay", x, y, taille, "#003087", "noir", track=-0.02)
    texte(c, "Pal", x + w1, y, taille, "#009CDE", "noir", track=-0.02)


CARTES6 = [("PayPal", None, TW(77) - 0.08, 780), ("Virement bancaire", "landmark", TW(79) - 0.08, 1010), ("Carte bancaire", "credit-card", TW(82) - 0.08, 1240)]


def s6(c, t):
    sc = scene(c, t, S6, "bas", "haut", de=0.25, ds=0.22)
    if sc is None: return
    with sc:
        for k, (lab, ic, t0, cy) in enumerate(CARTES6):
            ug = prog(t, S6[0] + 0.12 + 0.08 * k, 0.32, lambda v: rebond(v, 1.7)) * (1 - prog(t, t0 - 0.05, 0.15))
            if ug > 0:
                c.save(); c.translate(540, cy); c.scale(mix(0.6, 1, ug), mix(0.6, 1, ug))
                with Calque(c, borne(ug * 2)):
                    rrect(c, -430, -95, 860, 190, 40, "#F6F4FB", 1.0, None, "#DDD7EC", 4)
                    disque(c, -334, 0, 50, "#E8E3F3"); icone(c, "circle-help", -334, 0, 60, C["grisClair"], 2.2)
                    rrect(c, -248, -26, 340, 34, 17, "#E8E3F3")
                c.restore()
            if t < t0: continue
            u = prog(t, t0, 0.4, lambda v: rebond(v, 1.6))
            with Espace(c, 540, cy, rx=mix(70, 0, u)):
                c.save(); c.translate(540 + 900 * (1 - u), cy)
                carte(c, -430, -95, 860, 190, 40, C["blanc"], 1.0, (20, 44, 0.14))
                rrect(c, -394, -60, 120, 120, 30, C["vertDoux"])
                if ic is None:
                    texte_centre(c, "P", -334, 0, 74, "#003087", "noir")
                    logo_paypal(c, -248, -hauteurLigne(54) / 2, 54)
                else:
                    icone(c, ic, -334, 0, 70, C["vert"], 2.3)
                    texte(c, lab, -248, -hauteurLigne(48) / 2, ajuste(lab, 520, 48), C["ink"], "noir")
                uc = apparait(t, t0 + 0.2, 2.0, 0.3)
                if uc > 0:
                    c.save(); c.translate(350, 0); c.scale(uc, uc); disque(c, 0, 0, 46, C["vert"], 1.0, (8, 20, 0.2)); icone(c, "check", 0, 0, 52, C["blanc"], 3.6); c.restore()
                c.restore()
        if t >= TW(83) - 0.05:
            u = apparait(t, TW(83) - 0.05)
            pastille_rot(c, "AU CHOIX", 540, 1440, 44, C["ink"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "wallet", (14, 32, 0.25))


# ─────────────────────────────────────────── S7 · Snap dropandyou1, ou WhatsApp
PSEUDO = "dropandyou1"
T_PSEUDO = [TW(89) + k * (TW(92) + 0.2 - TW(89)) / len(PSEUDO) for k in range(len(PSEUDO))]


def s7(c, t):
    sc = scene(c, t, S7, "zoom", "gauche", de=0.28, ds=0.22)
    if sc is None: return
    with sc:
        u = prog(t, S7[0] + 0.05, 0.4, lambda v: rebond(v, 1.5))
        if u > 0:
            bob = 8 * math.sin(t * 3)
            c.save(); c.translate(540, 900 + bob); c.rotate(-3); c.scale(mix(0.5, 1, u), mix(0.5, 1, u))
            with Calque(c, borne(u * 2)):
                carte(c, -440, -190, 880, 380, 54, MARQUES["snapchat"], 1.0, (26, 60, 0.25))
                logo_app(c, "snapchat", -300, -40, 170, 1.0, None)
                texte(c, "Snapchat", -180, -118, 34, "#3A3A00", "fort", track=0)
                xl = -180
                for k, l in enumerate(PSEUDO):
                    if t >= T_PSEUDO[k]:
                        ul = prog(t, T_PSEUDO[k], 0.1, sortie)
                        texte(c, l, xl, -66 - 10 * (1 - ul), 66, C["ink"], "noir", alpha=ul, track=-0.01)
                        xl += largeur(l, 66, "noir", -0.01)
                if TW(89) - 0.1 <= t < TW(92) + 0.4 and int(t * 4) % 2 == 0: rrect(c, xl + 4, -60, 5, 70, 2, C["ink"])
                ub = apparait(t, TW(92) + 0.3, 2.0, 0.3)
                if ub > 0:
                    c.save(); c.translate(0, 110); c.scale(ub, ub)
                    rrect(c, -230, -40, 460, 80, 40, C["ink"]); icone(c, "circle-plus", -172, 0, 38, MARQUES["snapchat"], 2.6)
                    texte_centre(c, "Ajouter", 30, 0, 36, C["blanc"])
                    c.restore()
            c.restore()
        uw = apparait(t, TW(95) - 0.12, 1.6, 0.4)
        if uw > 0:
            s = mix(0.4, 1, uw) * (1 + 0.035 * max(0, math.sin((t - TW(95)) * 6)) if t > TW(95) + 0.4 else 1)
            lab = "Écris-nous sur WhatsApp"
            tw = largeur(lab, 44); wb, hb = tw + 170, 130
            c.save(); c.translate(540, 1300); c.scale(s, s)
            with Calque(c, borne(uw * 2)):
                rrect(c, -wb / 2, -hb / 2, wb, hb, hb / 2, MARQUES["whatsapp"], 1.0, (18, 46, 0.3))
                logo_glyphe(c, "whatsapp", -wb / 2 + 78, 0, 62, C["blanc"])
                texte_centre(c, lab, -wb / 2 + 134 + tw / 2, 0, 44, C["blanc"])
            c.restore()


# ─────────────────────────────────────────── S8 · et si tu veux faire comme moi : le ChinaBook
def s8(c, t):
    sc = scene(c, t, S8, "gauche", None, de=0.3)
    if sc is None: return
    with sc:
        e = prog(t, S8[0] + 0.05, 0.45, sortie)
        lignes = [dict(t=TW(98), image="catalogue/c12", nom="Baskets", ville="Guangzhou"),
                  dict(t=TW(101) - 0.05, image="dyson-supersonic", nom="Électronique", ville="Shenzhen", zoom=1.6, fy=0.4),
                  dict(t=TW(104), image="chanel-noire", nom="Luxe", ville="Guangzhou", fy=0.55)]
        tel(c, 540, 1144, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-30, -4, e) + 2 * math.sin(t * 2.2), s=mix(0.6, 1, e), alpha=borne(e * 2))
        if t >= TW(101) - 0.1:
            u = apparait(t, TW(101) - 0.1)
            pastille_rot(c, "COMME MOI", 300, 700, 38, C["ink"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "user", (14, 32, 0.22))
        tampon(c, "EN DIRECT", 790, 760, t, TW(105), 58, C["vert"], -8, "zap")
        confettis(c, 790, 760, t, TW(105) + 0.04, 22, 320, 9)


def disque_logo(c, t):
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (T_FIN - 0.1, 1750), (T_FIN + 0.3, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, C["vert"])
        if T_LOGO + 0.2 <= t <= T_FIN + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, T_FIN - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * so)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2, lw, borne(u * 3) * (1 - so))
    return r


def carton_final(c, t):
    if t < T_FIN + 0.05: return
    u = prog(t, T_FIN + 0.05, 0.4, sortie)
    disque(c, 540, 1060, 420 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
    ul = prog(t, T_FIN + 0.12, 0.36, lambda v: rebond(v, 1.6))
    lw = 760 * mix(0.6, 1, ul)
    iw_, ih_ = taille_img("logo"); lh = lw * ih_ / iw_
    image(c, "logo", 540 - lw / 2, 960 - lh / 2, lw, borne(ul * 2))
    ub = prog(t, T_FIN + 0.36, 0.36, lambda v: rebond(v, 1.8))
    etincelles(c, 540, 1170, t, T_FIN + 0.5, 12, 380)
    if ub > 0:
        s = mix(0.4, 1, ub) * (1 + 0.035 * max(0, math.sin((t - T_FIN - 0.8) * 5)) if t > T_FIN + 0.8 else 1)
        lab = "Envoie « CHINA » sur WhatsApp"
        tw = largeur(lab, 40); wb, hb = tw + 150, 116
        c.save(); c.translate(540, 1170); c.scale(s, s)
        with Calque(c, borne(ub * 2)):
            rrect(c, -wb / 2, -hb / 2, wb, hb, hb / 2, MARQUES["whatsapp"], 1.0, (18, 46, 0.3))
            logo_glyphe(c, "whatsapp", -wb / 2 + 70, 0, 56, C["blanc"])
            texte_centre(c, lab, -wb / 2 + 118 + tw / 2, 0, 40, C["blanc"])
        c.restore()
    ud = prog(t, T_FIN + 0.6, 0.4, sortie)
    if ud > 0:
        texte_centre(c, "proposé par", 540, 1380, 26, C["gris"], "fort", ud, 0.04)
        iw, ih = taille_img("logo-dy"); image(c, "logo-dy", 540 - 160, 1410, 320, ud)


# ─────────────────────────────────────────── bandeau DROP&YOU
def bandeau_dy(c, t, alpha):
    if alpha <= 0: return
    with Calque(c, alpha):
        image(c, "logo-dy", 86, 150, 200)
        lab = "TON AGENT EN CHINE"
        w = largeur(lab, 20, "fort", 0.12)
        texte(c, lab, 990, 158, 20, C["gris"], "fort", "droite", 0.12)
        disque(c, 990 - w - 20, 170, 6, C["vert"], 0.35 + 0.65 * (0.5 + 0.5 * math.cos(t * 4)))


# ─────────────────────────────────────────── sons, flou, éclairs
son(0.0, "impact", -5); son(0.0, "whoosh_court", -12)
for _n, _t0, _d, _s in JAILLIT:
    if _t0 > 0: son(_t0, "whoosh_court", -12); son(_t0 + 0.02, "pop", -14)
son(TW(5) - 0.25, "whoosh", -13); son(TW(8) - 0.1, "pop", -11); son(S2[0] - 0.3, "whoosh_long", -15)
for t0 in (TW(9) - 0.08, TW(9) + 0.09, TW(9) + 0.26, TW(9) + 0.43, TW(10) - 0.05, TW(10) + 0.25, TW(11) - 0.05, TW(11) + 0.19, TW(11) + 0.43, T_MONTRES, T_MONTRES + 0.75):
    son(t0, "clic", -11); son(t0 + 0.01, "swipe", -18)
for lab, t0, x, y, rot in CATS: son(t0 - 0.08, "pop", -12)
son(T_CATA, "whoosh_court", -12); son(TW(16) - 0.1, "tampon", -8); son(TW(17), "ching", -11); son(6.28, "whoosh", -13)
for m in MSGS3: son(m["t"], "message" if m["moi"] else "message_in", -11)
son(TW(24) - 0.08, "pop", -11); son(TW(32) - 0.08, "pop", -11); son(TW(38) - 0.1, "tampon", -8); son(11.48, "whoosh", -13)
son(S4[0] + 0.15, "pop", -12); son(TW(40) - 0.1, "pop", -10); son(TW(40) - 0.1, "whoosh_long", -15); son(TW(46), "ding", -12)
son(TW(48) - 0.05, "pop", -11); son(TW(50) - 0.05, "pop", -11)
for k in range(5): son(TW(52) + 0.1 * k, "blip", -15)
son(TW(56) - 0.1, "pop", -11); son(15.78, "whoosh", -13)
son(TW(57) - 0.1, "whoosh_court", -13); son(TW(57) + 0.1, "pop", -14); son(TW(62), "check", -12); son(TW(67) - 0.1, "whoosh_court", -13); son(TW(67) + 0.2, "check", -12)
son(T_GROS - 0.05, "whoosh", -12); son(T_GROS + 0.55, "clic", -11); son(TW(73) - 0.1, "tampon", -7); son(TW(73) - 0.08, "impact", -8); son(19.56, "whoosh", -13)
for k, (_, _, t0, _) in enumerate(CARTES6): son(t0, "whoosh_court", -14); son(t0 + 0.2, "check", -12)
son(TW(83) - 0.05, "pop", -11); son(22.10, "whoosh", -13)
son(S7[0] + 0.05, "pop", -10)
for tl in T_PSEUDO: son(tl, "frappe", -15)
son(TW(92) + 0.3, "pop", -12); son(TW(95) - 0.12, "pop", -10); son(TW(95), "message", -12); son(25.34, "whoosh", -13)
son(TW(101) - 0.1, "pop", -11); son(TW(98), "pop", -12); son(TW(101) - 0.05, "pop", -12); son(TW(104), "pop", -12); son(TW(105) - 0.1, "tampon", -9); son(TW(105) + 0.04, "ching", -11)
son(T_LOGO - 0.1, "montee", -15); son(T_LOGO + 0.24, "impact", -7); son(T_LOGO + 0.26, "verre", -9)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.14, "impact_doux", -8); son(T_FIN + 0.16, "verre", -8); son(T_FIN + 0.36, "pop", -11)

for a, b in [(0.06, 1.75), (S2[0] - 0.3, S2[0] + 0.1), (T_CATA - 0.05, T_CATA + 0.15), (6.28, 6.6), (11.48, 11.8), (TW(40) - 0.1, TW(40) + 0.2),
             (15.78, 16.1), (T_GROS - 0.05, T_GROS + 0.35), (19.56, 19.85), (22.10, 22.42), (25.34, 25.7), (T_LOGO, T_LOGO + 0.4), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, "#7C3AED", 0.14), (TW(16), "#7C3AED", 0.10), (TW(38), "#7C3AED", 0.08), (TW(46), "#7C3AED", 0.08), (TW(73) - 0.08, C["rouge"], 0.12),
                    (TW(83), "#7C3AED", 0.08), (TW(95), "#25D366", 0.08), (TW(105), "#00B862", 0.10), (T_LOGO + 0.24, C["blanc"], 0.15), (T_FIN + 0.14, "#00B862", 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    C.update(VERT if t >= T_CB else VIOLET)
    fond(c, t)
    for s in (s1, s2, s3, s4, s5, s6, s7, s8):
        s(c, t)
    r = disque_logo(c, t)
    r1 = 1750 if t < TW(5) - 0.1 else 0
    a = borne(prog(t, TW(5) + 0.1, 0.3) * (1 - prog(t, T_LOGO, 0.2)))
    if t < T_CB: bandeau_dy(c, t, a)
    else: bandeau(c, t, a)
    carton_final(c, t)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if (r > 900 or r1 > 900) else C["ink"])
