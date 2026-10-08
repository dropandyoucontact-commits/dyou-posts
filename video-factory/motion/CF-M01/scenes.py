"""CF-M01 « Bienvenue chez China Factory » — présentation de CHINA FACTORY (client de Youssef).

Copie de DY-M01 v1 (ancien hook : disque + logo), brief du 08/10/2026 : fond blanc, accent noir, un peu de
rouge ; logo CHINA FACTORY ; vidéos fournies par Youssef dans recus/ (conteneur, baskets en main, AirPods,
avion cargo, livraison à la maison, carton de bracelets) ; Snap china.factory1, WhatsApp +33 7 59 48 51 82 ;
pas de partie ChinaBook. Même voix (Tomy, 3,8 mots/s), même volume (−11 LUFS).
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import kit as KM

DUREE = 27.6
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a

NOIR = dict(vert="#111113", vertFonce="#000000", vertDoux="#F1F1F3", vertMoyen="#C9C9CF")
C.update(NOIR)
ROUGE = "#E11D2E"
C["rouge"] = ROUGE
WA_NUM = "+33 7 59 48 51 82"


class GlobeV(Globe):
    COUL = {0: "#D6D6DB", 1: ROUGE, 2: "#0B0B0D", 3: "#9A9AA2", 4: "#C4C4CA"}

    def disque(self, c, cx, cy, R, alpha=1.0):
        with Calque(c, alpha):
            ombre_sol(c, cx, cy + R * 1.06, R * 0.78, R * 0.09, 0.14)
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx - R * 0.3, cy - R * 0.35), R * 1.5,
                                                       [hexa("#FFFFFF"), hexa("#F0F0F2")], [0.0, 1.0]))
            c.drawCircle(cx, cy, R, p)
            anneau(c, cx, cy, R, "#DCDCE0", 3)


G = GlobeV()
GZ, PAR, BRU = (113.26, 23.13), (2.35, 48.86), (4.35, 50.85)
MONDE = [(-17.4, 14.7), (28.0, -26.2), (55.3, 25.2), (37.6, 55.75), (103.8, 1.35)]

# ─────────────────────────────────────────── sous-titres
SOUS = SousTitres(K, [
    [(0, "Bienvenue", "", -0.45), (1, "chez", "", -0.3), (2, "CHINA"), (3, "FACTORY,", "g")],
    [(4, "ton"), (5, "agent", "g"), (6, "en"), (7, "Chine.", "r")],
    [(8, "Baskets,", "g"), (9, "vêtements,", "g")],
    [(10, "électronique,", "g"), (11, "montres :", "r")],
    [(12, "on"), (13, "a"), (14, "un"), (15, "large", "g"), (16, "catalogue.", "g")],
    [(17, "Tu"), (18, "peux"), (19, "aussi"), (20, "nous"), (21, "envoyer"), (22, "la"), (23, "photo", "g"), (24, "de"), (25, "l’article"), (26, "que"), (27, "tu"), (28, "veux.")],
    [(29, "Selon"), (30, "les"), (31, "qualités,", "g"), (32, "on"), (33, "te"), (34, "donne"), (35, "le"), (36, "prix,", "g")],
    [(37, "livraison", "r"), (38, "incluse :", "r")],
    [(39, "8"), (40, "à"), (41, "12", "g"), (42, "jours", "g")],
    [(43, "jusqu’à"), (44, "chez"), (45, "toi,", "g")],
    [(46, "en"), (47, "France,", "g"), (48, "en"), (49, "Belgique,", "g")],
    [(50, "ou"), (51, "n’importe"), (52, "où"), (53, "dans"), (54, "le"), (55, "monde.", "g")],
    [(56, "Que"), (57, "tu"), (58, "achètes"), (59, "juste"), (60, "pour"), (61, "t’habiller,", "g")],
    [(62, "ou"), (63, "que"), (64, "tu"), (65, "sois"), (66, "revendeur", "g"), (67, "et"), (68, "que"), (69, "tu"), (70, "prennes"), (71, "en"), (72, "gros.", "r")],
    [(73, "Tu"), (74, "paies"), (75, "par"), (76, "PayPal,", "g"), (77, "par"), (78, "virement", "g")],
    [(79, "ou"), (80, "par"), (81, "carte"), (82, "bancaire.", "g")],
    [(83, "Envoie-moi"), (84, "un"), (85, "message"), (86, "sur"), (87, "Snap,", "g"), (88, "china.factory1,", "g")],
    [(91, "ou"), (92, "sur"), (93, "WhatsApp.", "g")],
])

# ─────────────────────────────────────────── fenêtres de scène
S1, S2, S3 = (0.0, TW(8) - 0.02), (TW(8) - 0.14, TW(17) - 0.02), (TW(17) - 0.14, TW(39) - 0.06)
S4V, S4 = (TW(39) - 0.18, TW(46) - 0.02), (TW(46) - 0.14, TW(56) - 0.02)
S5, S6, S7 = (TW(56) - 0.14, TW(73) - 0.02), (TW(73) - 0.14, TW(83) - 0.02), (TW(83) - 0.14, 24.95)
T_LOGO = 24.78
T_FIN = 25.45


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


# ─────────────────────────────────────────── S1 · bienvenue chez CHINA FACTORY, ton agent en Chine
LOGO_R = 311 / 2095


def s1(c, t):
    sc = scene(c, t, S1, None, None)
    if sc is None: return
    with sc:
        # disque noir plein écran dès l'image 0, logo blanc qui claque, puis le disque rentre dans le téléphone
        r = cles(t, [(0.0, 1750), (TW(4) - 0.25, 1750), (TW(4) + 0.15, 0, entree)])
        puls = 1 + 0.02 * math.sin(t * 5)
        if r > 1: disque(c, 540, 1080, r * puls, C["vert"])
        u = 1.0 + 0.18 * (1 - prog(t, 0, 0.35, sortie))
        so = prog(t, TW(4) - 0.25, 0.3, entree)
        if so < 1:
            lw = 760 * u * mix(1, 0.4, so)
            image(c, "logo-cf-blanc", 540 - lw / 2, 1020 - lw * LOGO_R / 2, lw, 1 - so)
            # filet rouge sous le logo
            rrect(c, 540 - 70 * u, 1020 + lw * LOGO_R / 2 + 40, 140 * u, 10, 5, ROUGE, 1 - so)
        # sur « ton agent en Chine » : le téléphone montre le conteneur qu'on charge
        if t >= TW(4) - 0.15:
            ut = prog(t, TW(4) - 0.15, 0.4, lambda v: rebond(v, 1.5))
            def ecran(cc, a, b, d, e):
                video(cc, "conteneur", a, b, d, e, t - TW(4) + 0.15, 1.7)
                flash(cc, a, b, d, e, t, [TW(4) - 0.15])
            tel(c, 540, 1110, ecran, ry=mix(-35, -6, ut) + 3 * math.sin(t * 2.2), rz=1.5 * math.sin(t * 2.7), s=mix(0.6, 1, ut), alpha=borne(ut * 2))
        if t >= TW(7) - 0.1:
            ua = apparait(t, TW(7) - 0.1, 2.0, 0.32)
            c.save(); c.translate(820, 680); c.rotate(8); c.scale(mix(0.2, 1, ua), mix(0.2, 1, ua))
            rrect(c, -98, -66, 196, 132, 24, "#FFFFFF", borne(ua * 2), (14, 36, 0.25))
            drapeau(c, "CN", -82, -50, 164, 100, 14)
            c.restore()
        etincelles(c, 540, 1100, t, TW(4) + 0.15, 12, 420, ROUGE)


# ─────────────────────────────────────────── S2 · catégories qui défilent dans le téléphone, puis le catalogue
CATALOGUE = [f"cat/p{k:02d}" for k in range(18)]
T_MONTRES, T_CATA = TW(11) - 0.08, TW(15) - 0.12


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
        rrect(c, xx, yy, col, hh, 22, "#F4F4F6")
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xx + 8, yy + 8, col - 16, col - 16), 16, 16), doAntiAlias=True)
        image_contenue(c, CATALOGUE[(k * 5) % len(CATALOGUE)], xx + 8, yy + 8, col - 16, col - 16)
        c.restore()
        rrect(c, xx + 14, yy + col + 6, col * 0.62, 14, 7, "#DCDCE1"); rrect(c, xx + 14, yy + col + 30, col * 0.36, 14, 7, C["vertMoyen"])
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 170), peinture(C["vert"]))
    texte(c, "9:41", x + 40, y + 24, 24, C["blanc"], "fort", track=0)
    image(c, "logo-cf-blanc", x + 34, y + 96, 300)
    rrect(c, x + w - 120, y + 78, 84, 64, 32, "#FFFFFF", 0.18); icone(c, "search", x + w - 78, y + 110, 30, C["blanc"], 2.6)


def ecran_s2(cc, a, b, d, e, t):
    coupes = []
    if t < TW(9) - 0.05:
        t0 = TW(8) - 0.08; coupes = [t0]
        video(cc, "baskets-mains", a, b, d, e, t - t0 + 0.3, 2.2)
    elif t < TW(10) - 0.05:
        t0 = TW(9) - 0.05; k = min(2, int((t - t0) / 0.19))
        coupes = [t0 + 0.19 * j for j in range(3)]
        image_contenue(cc, ["cat/p14", "cat/p16", "cat/p17"][k], a, b, d, e, 1.0 + 0.4 * ((t - t0) % 0.19))
    elif t < T_MONTRES:
        t0 = TW(10) - 0.05; coupes = [t0]
        video(cc, "airpods", a, b, d, e, t - t0 + 0.2, 2.2)
    elif t < T_CATA:
        coupes = [T_MONTRES]
        video(cc, "carton-montres", a, b, d, e, t - T_MONTRES, 1.0)
    else:
        coupes = [T_CATA]
        ecran_catalogue(cc, a, b, d, e, t, T_CATA)
    flash(cc, a, b, d, e, t, coupes)


CATS = [("BASKETS", TW(8), 270, 700, -6), ("VÊTEMENTS", TW(9), 820, 760, 6), ("ÉLECTRONIQUE", TW(10), 290, 1390, -5), ("MONTRES", TW(11), 800, 1420, 5)]


def s2(c, t):
    sc = scene(c, t, S2, None, "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        sx, sy = secousse(t, T_CATA, 10, 0.3)
        tel(c, 540 + sx, 1100 + sy, lambda cc, a, b, d, e: ecran_s2(cc, a, b, d, e, t), ry=-6 + 3 * math.sin(t * 2.2), rz=1.5 * math.sin(t * 2.7))
        for lab, t0, x, y, rot in CATS:
            if t0 - 0.08 <= t < T_CATA + 0.15:
                u = apparait(t, t0 - 0.08) * (1 - prog(t, T_CATA - 0.05, 0.2, entree))
                pastille_rot(c, lab, x, y, 38, C["vert"] if lab != "MONTRES" else ROUGE, C["blanc"], rot, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.22))
        tampon(c, "LARGE CATALOGUE", 540, 1420, t, TW(15), 60, ROUGE, -5, "store")
        confettis(c, 540, 1420, t, TW(16), 24, 360, 3, [C["vert"], ROUGE, C["vertMoyen"]])


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
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xb + 8, yy + 8, wb - 16, hb - 16), 14, 14), peinture("#FFFFFF")); image_contenue(c, m["image"], xb + 8, yy + 8, wb - 16, hb - 16)
            elif m["type"] == "qualites":
                for j, (lab, n) in enumerate(m["lignes"]):
                    ul = prog(t, m["t"] + 0.12 * j, 0.25)
                    yl = yy + 16 + j * 64
                    with Calque(c, ul):
                        rrect(c, xb + 12, yl, wb - 24, 54, 14, "#F3F3F5")
                        texte(c, lab, xb + 28, yl + 13, 24, C["ink"], "fort", track=0)
                        etoiles(c, xb + wb - 40 - (n - 1) * 23, yl + 27, n)
            else:
                texte(c, m["texte"], xb + 22, yy + 22, 26, C["ink"], "demi", track=0)
        c.restore()
        yy += hb + 16
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 170), peinture(WA_TETE))
    texte(c, "9:41", x + 40, y + 24, 24, C["blanc"], "fort", track=0)
    icone(c, "chevron-left", x + 34, y + 116, 34, C["blanc"], 2.6)
    disque(c, x + 96, y + 116, 34, "#FFFFFF"); image(c, "logo-cf-sigle", x + 96 - 22, y + 116 - 18, 44)
    texte(c, "CHINA FACTORY", x + 146, y + 88, 28, C["blanc"], "noir", track=0)
    texte(c, "en ligne", x + 146, y + 124, 21, "#CDEFE6", "demi", track=0)
    rrect(c, x + 16, y + h - 92, w - 110, 70, 35, "#FFFFFF")
    texte(c, "Message", x + 46, y + h - 74, 26, C["grisClair"], "moyen", track=0)
    disque(c, x + w - 54, y + h - 57, 35, WA_TETE); icone(c, "mic", x + w - 54, y + h - 57, 32, C["blanc"], 2.4)


MSGS3 = [dict(t=TW(21) - 0.05, moi=True, type="image", image="cat/p12"),
         dict(t=TW(26), moi=True, type="texte", texte="Tu as celle-ci ?"),
         dict(t=TW(30) - 0.05, moi=False, type="qualites", lignes=[("Qualité 1", 1), ("Qualité 2", 2), ("Qualité 3", 3)]),
         dict(t=TW(36) - 0.05, moi=False, type="texte", texte="Prix livraison incluse !")]


def s3(c, t):
    sc = scene(c, t, S3, "gauche", "gauche")
    if sc is None: return
    with sc:
        tel(c, 540, 1110, lambda cc, a, b, d, e: ecran_whatsapp(cc, a, b, d, e, t, MSGS3), ry=-5 + 2 * math.sin(t * 2))
        texte_centre(c, "Échange illustratif", 540, 1606, 22, C["grisClair"], "fort", 1.0, 0.04)
        if t >= TW(23) - 0.08:
            u = apparait(t, TW(23) - 0.08)
            pastille_rot(c, "ENVOIE LA PHOTO", 290, 690, 36, C["vert"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "camera", (14, 32, 0.22))
        if t >= TW(31) - 0.08:
            u = apparait(t, TW(31) - 0.08)
            pastille_rot(c, "SELON LA QUALITÉ", 830, 760, 34, C["ink"], C["blanc"], 6, mix(0.3, 1, u), borne(u * 2), "sparkles", (14, 32, 0.22))
        tampon(c, "LIVRAISON INCLUSE", 560, 1700, t, TW(37), 54, ROUGE, -5, "truck")


# ─────────────────────────────────────────── S4V · l'avion cargo (8 à 12 jours), puis livré chez toi
T_MAISON = TW(43) - 0.06


def s4v(c, t):
    sc = scene(c, t, S4V, "droite", "zoom", de=0.28, ds=0.2)
    if sc is None: return
    with sc:
        def ecran(cc, a, b, d, e):
            if t < T_MAISON: video(cc, "avion", a, b, d, e, t - S4V[0] + 0.2, 2.0)
            else: video(cc, "livraison-maison", a, b, d, e, t - T_MAISON + 0.6, 1.8)
            flash(cc, a, b, d, e, t, [T_MAISON])
        tel(c, 540, 1110, ecran, ry=-5 + 3 * math.sin(t * 2.2), rz=1.2 * math.sin(t * 2.7))
        if t >= TW(39) - 0.1:
            u = apparait(t, TW(39) - 0.1) * (1 - prog(t, T_MAISON - 0.1, 0.18, entree))
            pastille_rot(c, "8 À 12 JOURS", 290, 660, 44, ROUGE, C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "calendar", (14, 32, 0.25))
            ua = apparait(t, TW(41) - 0.05) * (1 - prog(t, T_MAISON - 0.1, 0.18, entree))
            pastille_rot(c, "PAR AVION", 820, 1500, 38, C["vert"], C["blanc"], 5, mix(0.3, 1, ua), borne(ua * 2), "plane", (14, 32, 0.25))
        tampon(c, "CHEZ TOI", 780, 720, t, TW(45) - 0.05, 60, C["vert"], 7, "map-pin")


# ─────────────────────────────────────────── S4 · 8 à 12 jours, France, Belgique, partout
def s4(c, t):
    sc = scene(c, t, S4, "zoom", "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1110, 410
        lon0 = cles(t, [(S4[0], 95), (TW(47) - 0.1, 30, entreeSortie), (TW(51), 42, entreeSortie)]); lat0 = cles(t, [(S4[0], 30), (TW(47) - 0.1, 34, entreeSortie)])
        G.disque(c, cx, cy, R); G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2, 3: 1.3})
        G.repere(c, *GZ, cx, cy, R, lon0, lat0, "CHINE", ROUGE, "CN", apparait(t, S4[0] + 0.15, 1.8, 0.4), 1.0, 70)
        pr = prog(t, S4[0] + 0.05, TW(47) - S4[0] - 0.05, entreeSortie)
        if pr > 0:
            G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, 1.0, C["vertMoyen"], 6, 0.38)
            x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, pr, C["vert"], 8, 0.38)
            if pr < 1 and z_ > 0: carton(c, x_, y_ - 20, 96, 0, 1.0, 8 * math.sin(t * 9))
        G.repere(c, *PAR, cx, cy, R, lon0, lat0, "FRANCE", C["ink"], "FR", apparait(t, TW(47) - 0.05, 1.8, 0.4), 1.0, 120)
        G.repere(c, *BRU, cx, cy, R, lon0, lat0, "BELGIQUE", C["ink"], "BE", apparait(t, TW(49) - 0.05, 1.8, 0.4), 1.0, 50)
        for k, lieu in enumerate(MONDE):
            pm = prog(t, TW(51) + 0.1 * k, 0.55, entreeSortie)
            if pm > 0:
                x_, y_, z_ = G.arc(c, GZ, lieu, cx, cy, R, lon0, lat0, pm, C["vert"], 6, 0.3)
                if pm >= 1:
                    x2, y2, z2 = G.pos(*lieu, lon0, lat0, R, cx, cy)
                    if z2 > 0: disque(c, x2, y2, 10, C["vert"]); onde(c, x2, y2, t, TW(51) + 0.1 * k + 0.55, 10, 70, C["vert"], 4)
        if t >= TW(55) - 0.1:
            u = apparait(t, TW(55) - 0.1)
            pastille_rot(c, "PARTOUT DANS LE MONDE", 600, 1420, 38, C["vert"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "globe", (14, 32, 0.25))


# ─────────────────────────────────────────── S5 · pour t'habiller, ou revendeur en gros
T_GROS = TW(70) - 0.12


def s5(c, t):
    sc = scene(c, t, S5, "droite", "gauche", de=0.28, ds=0.22)
    if sc is None: return
    with sc:
        part = prog(t, T_GROS - 0.05, 0.35, entreeSortie)
        for k, (titre, sous, ic, img, t0, cy) in enumerate((("Pour t’habiller", "Acheteur", "shirt", "cat/p13", TW(56) - 0.1, 800),
                                                            ("Revendeur", "Prix de gros", "store", "planche-baskets-12-modeles", TW(66) - 0.1, 1080))):
            u = apparait(t, t0, 1.5, 0.4)
            if u <= 0: continue
            c.save(); c.translate(540 + 900 * (1 - u), cy - 900 * part); c.rotate((-2 if k == 0 else 2) * (1 - part))
            carte(c, -440, -120, 880, 240, 44, C["blanc"], 1.0, (22, 50, 0.14))
            KM._cercle_image(c, img, -330, 0, 86, 1.2)
            texte(c, titre, -210, -58, ajuste(titre, 520, 54), C["ink"], "noir")
            rrect(c, -210, 18, largeur(sous, 28, "fort", 0) + 80, 52, 26, C["vertDoux"])
            icone(c, ic, -180, 44, 30, C["vertFonce"], 2.4)
            texte(c, sous, -152, 28, 28, C["vertFonce"], "fort", track=0)
            uc = apparait(t, [TW(61), TW(66) + 0.2][k], 2.0, 0.3)
            if uc > 0:
                c.save(); c.translate(380, -80); c.scale(uc, uc); disque(c, 0, 0, 44, C["vert"], 1.0, (8, 20, 0.2)); icone(c, "check", 0, 0, 50, C["blanc"], 3.6); c.restore()
            c.restore()
        # « pour t'habiller » : trois pièces du catalogue sous la carte, sorties avant « revendeur »
        for j, nom in enumerate(("cat/p15", "cat/p09", "cat/p11")):
            uj = apparait(t, TW(56) + 0.1 + 0.08 * j, 1.6, 0.35) * (1 - prog(t, TW(66) - 0.3, 0.22, entree))
            if uj <= 0: continue
            c.save(); c.translate(540 + (j - 1) * 300, 1170 + 80 * (1 - uj)); c.rotate((j - 1) * 4); c.scale(mix(0.5, 1, uj), mix(0.5, 1, uj))
            with Calque(c, borne(uj * 2)):
                carte(c, -130, -150, 260, 300, 32, C["blanc"], 1.0, (16, 40, 0.14))
                image_contenue(c, nom, -112, -132, 224, 264)
            c.restore()
        if t >= T_GROS - 0.05:
            sx, sy = secousse(t, TW(72), 12, 0.35)
            def ecran_gros(cc, a, b, d, e):
                if t < T_GROS + 0.55:
                    image_cover(cc, "planche-baskets-12-modeles", a, b, d, e, 1.1 + 0.3 * (t - T_GROS), 0.5, 0.5)
                else:
                    video(cc, "videos/guangzhou/guangzhou-cartons-baskets-gros", a, b, d, e, t - T_GROS, 1.6)
                flash(cc, a, b, d, e, t, [T_GROS, T_GROS + 0.55])
            tel(c, 540 + sx, mix(2300, 1110, part) + sy, ecran_gros, ry=-4 + 2 * math.sin(t * 2))
        tampon(c, "EN GROS", 760, 1400, t, TW(72), 70, C["rouge"], 7, "package")


# ─────────────────────────────────────────── S6 · PayPal, virement, carte
def logo_paypal(c, x, y, taille):
    w1 = largeur("Pay", taille, "noir", -0.02)
    texte(c, "Pay", x, y, taille, "#003087", "noir", track=-0.02)
    texte(c, "Pal", x + w1, y, taille, "#009CDE", "noir", track=-0.02)


CARTES6 = [("PayPal", None, TW(76) - 0.08, 780), ("Virement bancaire", "landmark", TW(78) - 0.08, 1010), ("Carte bancaire", "credit-card", TW(81) - 0.08, 1240)]


def s6(c, t):
    sc = scene(c, t, S6, "bas", "haut", de=0.25, ds=0.22)
    if sc is None: return
    with sc:
        for k, (lab, ic, t0, cy) in enumerate(CARTES6):
            ug = prog(t, S6[0] + 0.12 + 0.08 * k, 0.32, lambda v: rebond(v, 1.7)) * (1 - prog(t, t0 - 0.05, 0.15))
            if ug > 0:
                c.save(); c.translate(540, cy); c.scale(mix(0.6, 1, ug), mix(0.6, 1, ug))
                with Calque(c, borne(ug * 2)):
                    rrect(c, -430, -95, 860, 190, 40, "#F4F4F6", 1.0, None, "#DCDCE1", 4)
                    disque(c, -334, 0, 50, "#E9E9EC"); icone(c, "circle-help", -334, 0, 60, C["grisClair"], 2.2)
                    rrect(c, -248, -26, 340, 34, 17, "#E9E9EC")
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
        if t >= TW(82) - 0.05:
            u = apparait(t, TW(82) - 0.05)
            pastille_rot(c, "AU CHOIX", 540, 1440, 44, C["ink"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "wallet", (14, 32, 0.25))


# ─────────────────────────────────────────── S7 · Snap dropandyou1, ou WhatsApp
PSEUDO = "china.factory1"
T_PSEUDO = [TW(88) + k * (TW(90) + 0.2 - TW(88)) / len(PSEUDO) for k in range(len(PSEUDO))]


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
                if TW(88) - 0.1 <= t < TW(90) + 0.4 and int(t * 4) % 2 == 0: rrect(c, xl + 4, -60, 5, 70, 2, C["ink"])
                ub = apparait(t, TW(90) + 0.3, 2.0, 0.3)
                if ub > 0:
                    c.save(); c.translate(0, 110); c.scale(ub, ub)
                    rrect(c, -230, -40, 460, 80, 40, C["ink"]); icone(c, "circle-plus", -172, 0, 38, MARQUES["snapchat"], 2.6)
                    texte_centre(c, "Ajouter", 30, 0, 36, C["blanc"])
                    c.restore()
            c.restore()
        uw = apparait(t, TW(93) - 0.12, 1.6, 0.4)
        if uw > 0:
            s = mix(0.4, 1, uw) * (1 + 0.035 * max(0, math.sin((t - TW(93)) * 6)) if t > TW(93) + 0.4 else 1)
            lab = WA_NUM
            tw = largeur(lab, 44, "noir", 0.03); wb, hb = tw + 170, 130
            c.save(); c.translate(540, 1300); c.scale(s, s)
            with Calque(c, borne(uw * 2)):
                rrect(c, -wb / 2, -hb / 2, wb, hb, hb / 2, MARQUES["whatsapp"], 1.0, (18, 46, 0.3))
                logo_glyphe(c, "whatsapp", -wb / 2 + 78, 0, 62, C["blanc"])
                texte_centre(c, lab, -wb / 2 + 134 + tw / 2, 0, 44, C["blanc"], "noir", 1.0, 0.03)
            c.restore()


def disque_logo(c, t):
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (T_FIN - 0.1, 1750), (T_FIN + 0.3, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, C["vert"])
        if T_LOGO + 0.2 <= t <= T_FIN + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, T_FIN - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 860 * (1 - 0.3 * so)
            image(c, "logo-cf-blanc", 540 - lw / 2, 1020 - lw * LOGO_R / 2, lw, borne(u * 3) * (1 - so))
            rrect(c, 540 - 70, 1020 + lw * LOGO_R / 2 + 40, 140, 10, 5, ROUGE, borne(u * 3) * (1 - so))
    return r


def pilule(c, cx, cy, lab, fond_, coul, glyphe, taille, s, alpha):
    tw = largeur(lab, taille, "noir", 0.03); wb, hb = tw + 3.6 * taille, 2.8 * taille
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        rrect(c, -wb / 2, -hb / 2, wb, hb, hb / 2, fond_, 1.0, (18, 46, 0.3))
        logo_glyphe(c, glyphe, -wb / 2 + 1.75 * taille, 0, 1.4 * taille, coul)
        texte_centre(c, lab, -wb / 2 + 2.9 * taille + tw / 2, 0, taille, coul, "noir", 1.0, 0.03)
    c.restore()


def carton_final(c, t):
    if t < T_FIN + 0.05: return
    u = prog(t, T_FIN + 0.05, 0.4, sortie)
    disque(c, 540, 1060, 440 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
    ul = prog(t, T_FIN + 0.12, 0.36, lambda v: rebond(v, 1.6))
    lw = 820 * mix(0.6, 1, ul)
    image(c, "logo-cf", 540 - lw / 2, 900 - lw * LOGO_R / 2, lw, borne(ul * 2))
    rrect(c, 540 - 60, 900 + lw * LOGO_R / 2 + 30, 120, 9, 4.5, ROUGE, borne(ul * 2))
    etincelles(c, 540, 1130, t, T_FIN + 0.5, 12, 380, ROUGE)
    ub = prog(t, T_FIN + 0.36, 0.36, lambda v: rebond(v, 1.8))
    if ub > 0:
        s = mix(0.4, 1, ub) * (1 + 0.035 * max(0, math.sin((t - T_FIN - 0.8) * 5)) if t > T_FIN + 0.8 else 1)
        pilule(c, 540, 1120, WA_NUM, MARQUES["whatsapp"], C["blanc"], "whatsapp", 42, s, borne(ub * 2))
    us = prog(t, T_FIN + 0.52, 0.36, lambda v: rebond(v, 1.8))
    if us > 0:
        pilule(c, 540, 1270, PSEUDO, MARQUES["snapchat"], C["ink"], "snapchat", 38, mix(0.4, 1, us), borne(us * 2))


# ─────────────────────────────────────────── bandeau CHINA FACTORY
def bandeau_cf(c, t, alpha):
    if alpha <= 0: return
    with Calque(c, alpha):
        image(c, "logo-cf", 86, 156, 250)
        lab = "TON AGENT EN CHINE"
        w = largeur(lab, 20, "fort", 0.12)
        texte(c, lab, 990, 158, 20, C["gris"], "fort", "droite", 0.12)
        disque(c, 990 - w - 20, 170, 6, ROUGE, 0.35 + 0.65 * (0.5 + 0.5 * math.cos(t * 4)))


# ─────────────────────────────────────────── sons, flou, éclairs
son(0.0, "impact", -5); son(0.0, "whoosh_court", -12); son(0.12, "verre", -10); son(TW(4) - 0.25, "whoosh", -13); son(TW(4) - 0.15, "pop", -11); son(TW(7) - 0.1, "pop", -12)
for t0 in (TW(8) - 0.08, TW(8) + 0.09, TW(8) + 0.26, TW(8) + 0.43, TW(9) - 0.05, TW(9) + 0.25, TW(10) - 0.05, TW(10) + 0.19, TW(10) + 0.43, T_MONTRES, T_MONTRES + 0.75):
    son(t0, "clic", -11); son(t0 + 0.01, "swipe", -18)
for lab, t0, x, y, rot in CATS: son(t0 - 0.08, "pop", -12)
son(T_CATA, "whoosh_court", -12); son(TW(15) - 0.1, "tampon", -8); son(TW(16), "ching", -11); son(S3[0] - 0.02, "whoosh", -13)
for m in MSGS3: son(m["t"], "message" if m["moi"] else "message_in", -11)
son(TW(23) - 0.08, "pop", -11); son(TW(31) - 0.08, "pop", -11); son(TW(37) - 0.1, "tampon", -8); son(S4V[0] - 0.02, "whoosh", -13)
son(S4[0] + 0.15, "pop", -12); son(TW(39) - 0.1, "pop", -10); son(S4[0] + 0.05, "whoosh_long", -15); son(TW(47) - 0.12, "ding", -12)
son(TW(47) - 0.05, "pop", -11); son(TW(49) - 0.05, "pop", -11)
for k in range(5): son(TW(51) + 0.1 * k, "blip", -15)
son(TW(55) - 0.1, "pop", -11); son(S5[0] - 0.02, "whoosh", -13)
son(TW(56) - 0.1, "whoosh_court", -13); son(TW(56) + 0.1, "pop", -14); son(TW(61), "check", -12); son(TW(66) - 0.1, "whoosh_court", -13); son(TW(66) + 0.2, "check", -12)
son(T_GROS - 0.05, "whoosh", -12); son(T_GROS + 0.55, "clic", -11); son(TW(72) - 0.1, "tampon", -7); son(TW(72) - 0.08, "impact", -8); son(S6[0] - 0.02, "whoosh", -13)
for k, (_, _, t0, _) in enumerate(CARTES6): son(t0, "whoosh_court", -14); son(t0 + 0.2, "check", -12)
son(TW(82) - 0.05, "pop", -11); son(S7[0] - 0.02, "whoosh", -13)
son(S7[0] + 0.05, "pop", -10)
for tl in T_PSEUDO: son(tl, "frappe", -15)
son(TW(90) + 0.3, "pop", -12); son(TW(93) - 0.12, "pop", -10); son(TW(93), "message", -12); son(T_LOGO - 0.3, "whoosh", -13)
son(S4V[0], "whoosh", -13); son(T_MAISON, "clic", -11); son(TW(41) - 0.05, "pop", -11); son(TW(45) - 0.1, "tampon", -8); son(S4[0] - 0.02, "whoosh", -13)
son(T_LOGO - 0.1, "montee", -15); son(T_LOGO + 0.24, "impact", -7); son(T_LOGO + 0.26, "verre", -9)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.14, "impact_doux", -8); son(T_FIN + 0.16, "verre", -8); son(T_FIN + 0.36, "pop", -11); son(T_FIN + 0.52, "pop", -12)

for a, b in [(TW(4) - 0.25, TW(4) + 0.2), (T_CATA - 0.05, T_CATA + 0.15), (S3[0] - 0.02, S3[0] + 0.3), (S4V[0] - 0.02, S4V[0] + 0.3), (S4[0] - 0.02, S4[0] + 0.3),
             (S5[0] - 0.02, S5[0] + 0.3), (T_GROS - 0.05, T_GROS + 0.35), (S6[0] - 0.02, S6[0] + 0.3), (S7[0] - 0.02, S7[0] + 0.3), (T_LOGO, T_LOGO + 0.4), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, "#FFFFFF", 0.14), (TW(15), ROUGE, 0.10), (TW(37), ROUGE, 0.08), (TW(45) - 0.05, "#111113", 0.08), (TW(72) - 0.08, ROUGE, 0.12),
                    (TW(82), "#111113", 0.08), (TW(93), "#25D366", 0.08), (T_LOGO + 0.24, C["blanc"], 0.15), (T_FIN + 0.14, ROUGE, 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    fond(c, t)
    for s in (s1, s2, s3, s4v, s4, s5, s6, s7):
        s(c, t)
    r = disque_logo(c, t)
    r1 = 1750 if t < TW(4) - 0.1 else 0
    a = borne(prog(t, TW(4) + 0.1, 0.3) * (1 - prog(t, T_LOGO, 0.2)))
    bandeau_cf(c, t, a)
    carton_final(c, t)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if (r > 900 or r1 > 900) else C["ink"])
