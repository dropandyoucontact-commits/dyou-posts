"""CB-M03 « Tu bosses pour un Français » — ChinaBook pour revendeur de sneakers (27,5 s).

Discours de Youssef (05/10/2026) : jamais « usine » ; fournisseurs validés à Guangzhou et
Shenzhen ; la marge du Français installé en Chine ; WeChat → Alipay → transitaire ; vendre au
détail, à l'unité ou en gros ; gérer à la commande depuis la Thaïlande ; sans y aller.

Voix : moteur/outils/voix.py (Tomy, 3,8 mots/s). Chaque élément cite le mot qu'il illustre.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *

DUREE = 27.5
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a
G = Globe()

GZ, BKK, PAR = (113.26, 23.13), (100.5, 13.75), (2.35, 48.86)      # Guangzhou, Bangkok, Paris
PH = (300, 664, 480, 960)

# ─────────────────────────────────────────── sous-titres
SOUS = SousTitres(K, [
    [(0, "Tu", "", -0.30), (1, "ne", "", -0.18), (2, "marges", "", -0.06), (3, "pas", "r"), (4, "assez", "r"), (5, "sur"), (6, "tes"), (7, "sneakers ?")],
    [(8, "Normal."), (9, "Tu"), (10, "bosses"), (11, "pour"), (12, "un"), (13, "Français", "r"), (14, "installé"), (15, "en"), (16, "Chine.", "r")],
    [(17, "Il"), (18, "achète"), (19, "au"), (20, "fournisseur"), (21, "chinois,"), (22, "prend"), (23, "sa"), (24, "marge,", "r"), (25, "et"), (26, "te"), (27, "revend.", "r")],
    [(28, "Moi,"), (29, "j’ai"), (30, "été"), (31, "à"), (32, "Guangzhou,", "g"), (33, "pour"), (34, "les"), (35, "marques.")],
    [(36, "Avec"), (37, "le"), (38, "ChinaBook,", "g"), (40, "tu"), (41, "as"), (42, "directement", "g"), (43, "les"), (44, "numéros", "g"), (45, "des"), (46, "Chinois.")],
    [(47, "Tu"), (48, "écris"), (49, "sur"), (50, "WeChat,", "g"), (51, "tu"), (52, "paies"), (53, "sur"), (54, "Alipay,", "g"), (55, "ton"), (56, "transitaire", "g"), (57, "t’envoie"), (58, "le"), (59, "colis.")],
    [(60, "Au"), (61, "détail,"), (62, "à"), (63, "l’unité"), (64, "ou"), (65, "en"), (66, "gros :", "g")],
    [(67, "tu"), (68, "vends"), (69, "n’importe"), (70, "quel"), (71, "produit"), (72, "de"), (73, "Chine.", "g")],
    [(74, "Moi,"), (75, "je"), (76, "gère"), (77, "ça"), (78, "à"), (79, "la"), (80, "commande,", "g"), (81, "depuis"), (82, "la"), (83, "Thaïlande.", "g")],
    [(84, "Sans"), (85, "y"), (86, "aller.", "r")],
    [(87, "Sans"), (88, "perdre"), (89, "des"), (90, "milliers"), (91, "d’euros,", "r"), (92, "ni"), (93, "du"), (94, "temps.", "r")],
    [(95, "Envoie-moi"), (96, "« CHINA »", "g"), (97, "sur"), (98, "WhatsApp.")],
    [(None, "Ton", "", 26.12), (None, "accès", "", 26.19), (None, "direct", "g", 26.28), (None, "à", "", 26.38), (None, "la", "", 26.43), (None, "Chine.", "", 26.49)],
])

# ─────────────────────────────────────────── fenêtres de scène
S1, S2, S3, S4, S5 = (0.0, 1.85), (1.62, 4.40), (4.18, 7.30), (7.08, 9.45), (9.22, 12.18)
S6, S7, S8, S9 = (11.95, 15.78), (15.55, 19.52), (19.30, 21.90), (21.66, 24.80)
T_CTA, T_FIN = 24.55, 26.05
TL = [TW(96) - 0.16 + k * 0.07 for k in range(5)]
T_ENVOI = TW(97)


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
    """téléphone en 3D centré sur (cx, cy)"""
    with Espace(c, cx, cy, **espace):
        telephone(c, cx - w / 2, cy - h / 2, w, h, ecran, alpha)


# ─────────────────────────────────────────── S1 · accroche : le vrai cliché de Guangzhou
def s1(c, t):
    sc = scene(c, t, S1, None, "gauche", ds=0.2)
    if sc is None: return
    with sc:
        tx = 7 * math.sin(t * 13.0) + 4 * math.sin(t * 29.0)
        ty = 6 * math.sin(t * 11.0 + 1) + 3 * math.sin(t * 23.0)
        punch = 1.0 + 0.2 * (1 - prog(t, 0, 0.35, sortie))
        tel(c, 540 + tx, 1190 + ty, lambda cc, a, b, d, e: video(cc, "videos/guangzhou/guangzhou-cartons-baskets-gros", a, b, d, e, t),
            w=560, h=1120, ry=-9 + 3 * math.sin(t * 2.2), rz=2.5 * math.sin(t * 3.1), s=punch)
        tampon(c, "MARGE ?", 300, 760, t, 0.20, 64, C["rouge"], -9, "circle-help")
        if True:
            u = prog(t, -0.25, 0.3, lambda v: rebond(v, 1.8))
            sx, sy = secousse(t, 0.85, 12, 0.5)
            c.save(); c.translate(540 + sx, 1330 + sy); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            with Calque(c, borne(u * 2)):
                rrect(c, -290, -70, 580, 140, 34, C["blanc"], 1.0, (16, 36, 0.18))
                texte(c, "TA MARGE", -250, -52, 30, C["gris"], "fort", track=0.08)
                rrect(c, -250, 6, 500, 34, 17, C["ligne"]); rrect(c, -250, 6, 44, 34, 17, C["vert"])
                if t > 0.85: icone(c, "triangle-alert", 238, -34, 46, C["rouge"], 2.6)
            c.restore()


# ─────────────────────────────────────────── S2 · la marge mangée
NSEG, SEG_W, SEG_G, SEG_Y, SEG_H = 12, 70, 6, 1090, 170
SEG_X0 = (1080 - (NSEG * SEG_W + (NSEG - 1) * SEG_G)) / 2
T_MANGE0, T_MANGE1, AV_X0, AV_X1 = TW(13), TW(13) + 0.98, 1040, 205
def t_mange(k):
    cx = SEG_X0 + k * (SEG_W + SEG_G) + SEG_W / 2
    return T_MANGE0 + (AV_X0 - (cx + 34)) / (AV_X0 - AV_X1) * (T_MANGE1 - T_MANGE0)


def s2(c, t):
    sc = scene(c, t, S2, "zoom", "haut", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        u0 = prog(t, S2[0] + 0.05, 0.4, lambda v: rebond(v, 1.7))
        bob = 8 * math.sin(t * 5)
        sneaker(c, 540, 810 + bob, 560 * mix(0.6, 1, u0), alpha=borne(u0 * 2), rot=-3)
        ombre_sol(c, 540, 965, 260, 20, 0.15 * u0)
        rrect(c, SEG_X0 - 10, SEG_Y - 10, NSEG * SEG_W + (NSEG - 1) * SEG_G + 20, SEG_H + 20, 30, C["fondDoux"], borne(u0 * 2))
        pastille(c, "TA MARGE", SEG_X0 + 770, SEG_Y - 62, 28, C["ink"], C["blanc"], "banknote", borne(u0 * 2) * (1 - prog(t, T_MANGE0 - 0.15, 0.2)))
        ax = cles(t, [(TW(9), 1330), (TW(9) + 0.5, AV_X0, sortie), (T_MANGE0, AV_X0), (T_MANGE1, AV_X1, lin)])
        for k in range(NSEG):
            x = SEG_X0 + k * (SEG_W + SEG_G)
            ts = S2[0] + 0.12 + k * 0.035
            us = prog(t, ts, 0.25, lambda v: rebond(v, 1.8))
            mange = k >= 2 and t >= t_mange(k) - 0.02
            if not mange:
                shake = secousse(t, T_MANGE1 + 0.05, 8, 0.4)[0] if k < 2 else 0
                c.save(); c.translate(x + SEG_W / 2 + shake, SEG_Y + SEG_H / 2); c.scale(us, us)
                rrect(c, -SEG_W / 2, -SEG_H / 2, SEG_W, SEG_H, 18, C["vert"], borne(us * 2))
                c.restore()
            elif t < t_mange(k) + 0.16:
                v = prog(t, t_mange(k), 0.16, entree)
                cx_, cy_ = x + SEG_W / 2, SEG_Y + SEG_H / 2
                c.save(); c.translate(mix(cx_, ax, v), mix(cy_, SEG_Y + SEG_H / 2 + 20, v)); c.scale(1 - 0.8 * v, 1 - 0.8 * v)
                rrect(c, -SEG_W / 2, -SEG_H / 2, SEG_W, SEG_H, 18, C["rouge"])
                c.restore()
        # le Français : une bouche qui croque
        if t >= TW(9) - 0.05:
            ay = SEG_Y + SEG_H / 2 + 20
            ouv = 42 * abs(math.sin((t - T_MANGE0) * 24)) if T_MANGE0 <= t <= T_MANGE1 + 0.05 else 12
            pa = peinture(C["rouge"])
            ombre_sol(c, ax, ay + 118, 120, 14, 0.16)
            c.drawArc(skia.Rect.MakeXYWH(ax - 112, ay - 112, 224, 224), 180 + ouv / 2, 360 - ouv, True, pa)
            disque(c, ax + 18, ay - 52, 11, C["blanc"]); disque(c, ax + 20, ay - 50, 5, C["ink"])
            drapeau(c, "FR", ax - 42, ay - 190, 84, 56, 9)
        if t >= TW(14) - 0.05:
            u = prog(t, TW(14) - 0.05, 0.34, lambda v: rebond(v, 1.8))
            c.save(); c.translate(540, 1400); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            w, h = pastille(c, "FRANÇAIS EN CHINE", 8, 0, 32, C["blanc"], C["ink"], None, borne(u * 2), (12, 30, 0.18), C["ink"], 4)
            drapeau(c, "CN", -w / 2 - 58, -22, 52, 36, 5)
            c.restore()
        tampon(c, "POUR LUI", 815, 735, t, TW(13) + 0.25, 56, C["rouge"], 8)


# ─────────────────────────────────────────── S3 · la chaîne : fournisseur → Français → toi
NX = [190, 540, 890]
def s3(c, t):
    sc = scene(c, t, S3, "bas", "haut")
    if sc is None: return
    with sc:
        noeuds = [(C["vert"], "store", "CN", "Fournisseur"), (C["rouge"], "user", "FR", "Le Français"), (C["ink"], "user", None, "Toi")]
        for k, (coul, ic, dr, lab) in enumerate(noeuds):
            u = prog(t, S3[0] + 0.1 + k * 0.1, 0.4, lambda v: rebond(v, 1.8))
            pulse = battement(t, [TW(20), TW(22), TW(26)][k] - 0.05, 0.1, 0.3)
            c.save(); c.translate(NX[k], 860); c.scale(u * pulse, u * pulse)
            disque(c, 0, 0, 120, coul, 1.0, (16, 36, 0.2)); icone(c, ic, 0, 0, 108, C["blanc"], 2.2)
            if dr: drapeau(c, dr, -100, -140, 72, 48, 7)
            c.restore()
            texte_centre(c, lab, NX[k], 1030, 38, C["ink"], "noir", borne(u * 2))
            trait(c, NX[k], 1070, NX[k], 1200, C["ligne"], 5, borne(u * 2), (2, 14))
        # rail et colis
        for a_, b_ in ((0, 1), (1, 2)):
            u = prog(t, S3[0] + 0.3 + a_ * 0.1, 0.4, sortie)
            trait(c, NX[a_] + 40, 1250, mix(NX[a_] + 40, NX[b_] - 40, u), 1250, C["ligne"], 12, 1)
        p1 = prog(t, 5.05, 0.45, entreeSortie); p2 = prog(t, 6.32, 0.55, entreeSortie)
        px = NX[0] + (NX[1] - NX[0]) * p1 + (NX[2] - NX[1]) * p2
        marge = prog(t, TW(22), 0.3, lambda v: rebond(v, 1.6))
        if t >= TW(17) - 0.05:
            u = prog(t, TW(17) - 0.05, 0.32, lambda v: rebond(v, 1.9))
            bond = 22 * math.sin(math.pi * min(1, (t - 5.05) / 0.45)) if 5.05 <= t <= 5.5 else (22 * math.sin(math.pi * min(1, (t - 6.32) / 0.55)) if 6.32 <= t <= 6.87 else 0)
            carton(c, px, 1250 - bond, 260 * mix(0.3, 1, u), marge, borne(u * 2), 4 * math.sin(t * 6))
        if t >= TW(22):
            u = prog(t, TW(22), 0.3, lambda v: rebond(v, 2.0))
            pastille_rot(c, "+ SA MARGE", 540, 1115, 34, C["rouge"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2))
        if t >= 6.88:
            u = prog(t, 6.88, 0.3, lambda v: rebond(v, 2.0))
            pastille_rot(c, "PRIX GONFLÉ", 880, 1400, 34, C["rouge"], C["blanc"], 5, mix(0.3, 1, u), borne(u * 2), "triangle-alert", (12, 28, 0.2))
        etincelles(c, 540, 1250, t, TW(22), 8, 150, C["rouge"])


# ─────────────────────────────────────────── S4 · « j'ai été à Guangzhou » : mes rushs
CUTS4 = [8.05, 8.55, 9.0]
def ecran_s4(cc, a, b, d, e, t):
    if t < CUTS4[0]:
        video(cc, "videos/chaussures/baskets-stock-1", a, b, d, e, t - S4[0], 2.2, rogne=(0, 0, 0, 0.23))
    elif t < CUTS4[1]:
        u = (t - CUTS4[0]) / 0.5
        image_cover(cc, "photos/fabrication/couture-semelle", a, b, d, e, zoom=1.12 + 0.22 * u, fx=0.5 - 0.05 * u, fy=0.52 + 0.08 * u)
    elif t < CUTS4[2]:
        u = (t - CUTS4[1]) / 0.45
        image_cover(cc, "photos/fabrication/assemblage-semelle", a, b, d, e, zoom=1.1 + 0.25 * u, fx=0.5, fy=0.58 - 0.08 * u)
    else:
        video(cc, "videos/chaussures/baskets-stock-2", a, b, d, e, t - CUTS4[2], 2.2, rogne=(0, 0, 0, 0.23))
    for ct in CUTS4:
        f = 1 - (t - ct) / 0.09
        if 0 < f <= 1: cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#FFFFFF", 0.7 * f))


def s4(c, t):
    sc = scene(c, t, S4, "droite", "zoom", de=0.3, ds=0.2)
    if sc is None: return
    with sc:
        sx, sy = 0, 0
        for ct in CUTS4:
            a_, b_ = secousse(t, ct, 10, 0.25); sx += a_; sy += b_
        tel(c, 540 + sx, 1144 + sy, lambda cc, a, b, d, e: ecran_s4(cc, a, b, d, e, t), ry=-8 + 3 * math.sin(t * 2.0), rz=-2 * math.sin(t * 2.7))
        if t >= TW(32) - 0.05:
            u = prog(t, TW(32) - 0.05, 0.34, lambda v: rebond(v, 1.8))
            c.save(); c.translate(330, 700); c.rotate(-6); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            w, h = pastille(c, "GUANGZHOU", 20, 0, 34, C["ink"], C["blanc"], None, borne(u * 2), (14, 32, 0.22))
            drapeau(c, "CN", -w / 2 - 44, -24, 56, 38, 6)
            c.restore()
        tampon(c, "J’Y ÉTAIS", 770, 1360, t, TW(33), 60, C["vert"], 8, "map-pin")


# ─────────────────────────────────────────── S5 · ChinaBook : les numéros directs
def s5(c, t):
    sc = scene(c, t, S5, None, "gauche", ds=0.22)
    if sc is None: return
    with sc:
        e = prog(t, 10.0, 0.45, sortie)
        if e > 0:
            lignes = [dict(t=TW(40) + 0.0, image="photos/chaussures/baskets-portees-marine", nom="Baskets", ville="Guangzhou", fx=0.62),
                      dict(t=TW(42) + 0.0, image="photos/chaussures/etagere-baskets-running-6-modeles", nom="Running", ville="Guangzhou", zoom=1.7, fx=0.5, fy=0.28),
                      dict(t=TW(44) - 0.2, image="photos/mobilite/casque-moto-plateau", nom="Casques", ville="Shenzhen", fy=0.55)]
            tel(c, 540, 1144, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-34, -4, e) + 2 * math.sin(t * 2.2), s=mix(0.8, 1, e), alpha=borne(e * 2))
        if t >= TW(44) - 0.05:
            u = prog(t, TW(44) - 0.05, 0.4, lambda v: rebond(v, 2.0))
            c.save(); c.translate(150, 1020); c.rotate(-10); c.scale(u, u); logo_app(c, "wechat", 0, 0, 150); c.restore()
            u2 = prog(t, TW(44) + 0.2, 0.3, lambda v: rebond(v, 2.2))
            c.save(); c.translate(205, 940); c.scale(u2, u2); disque(c, 0, 0, 24, "#EF4444"); texte_centre(c, "3", 0, 0, 26, C["blanc"], "noir", track=0); c.restore()
        tampon(c, "EN DIRECT", 760, 760, t, TW(42), 58, C["vert"], -9, "zap")
        confettis(c, 760, 760, t, TW(42) + 0.04, 22, 320, 9)


# ─────────────────────────────────────────── disque vert (S4 → S5) et logo qui claque
def disque_transition(c, t):
    r = cles(t, [(9.05, 0), (9.40, 1750, entree), (9.78, 1750), (10.32, 0, entreeSortie)])
    cy_ = cles(t, [(9.78, 1140), (10.32, 720, entreeSortie)])
    if r > 1:
        disque(c, 540, cy_, r, C["vert"])
        if 9.40 <= t <= 10.34:
            u = prog(t, 9.50, 0.3, lambda v: rebond(v, 1.5)); sortie_u = prog(t, 10.05, 0.3, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * sortie_u)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2 - 150 * sortie_u, lw, borne(u * 3) * (1 - sortie_u))
    return r


# ─────────────────────────────────────────── S6 · WeChat → Alipay → transitaire
T6A, T6B, T6C = 11.95, 13.02, 13.96
MSGS = [dict(t=11.98, moi=False, type="texte", texte="Hello !"),
        dict(t=12.10, moi=True, type="texte", texte="Salut ! 2 paires\\nde celles-ci ?"),
        dict(t=12.30, moi=True, type="image", image="photos/chaussures/baskets-portees-violettes"),
        dict(t=12.72, moi=False, type="texte", texte="OK ! Voici\\nle QR code")]
MSGS = [dict(m, texte=m["texte"].replace("\\n", "\n")) if "texte" in m else m for m in MSGS]


def tracker(c, t):
    etapes = [("wechat", "WeChat", TW(50)), ("alipay", "Alipay", TW(54) + 0.1), (None, "Transitaire", TW(59) - 0.35)]
    for k, (logo, lab, ta) in enumerate(etapes):
        cx = 240 + k * 300
        u = prog(t, S6[0] + 0.1 + k * 0.08, 0.35, lambda v: rebond(v, 1.8))
        on = prog(t, ta, 0.25, lambda v: rebond(v, 1.8))
        if u <= 0: continue
        c.save(); c.translate(cx, 640); c.scale(mix(0.5, 1, u) * battement(t, ta, 0.1, 0.25), mix(0.5, 1, u) * battement(t, ta, 0.1, 0.25))
        with Calque(c, borne(u * 2)):
            rrect(c, -138, -42, 276, 84, 42, C["vert"] if on > 0.5 else C["blanc"], 1.0, (10, 24, 0.14), C["ligne"], 3)
            if logo: logo_app(c, logo, -92, 0, 54, 1.0, None)
            else:
                disque(c, -92, 0, 27, C["ink"]); icone(c, "truck", -92, 0, 32, C["blanc"], 2.4)
            texte_centre(c, lab, 22, 0, ajuste(lab, 150, 30), C["blanc"] if on > 0.5 else C["ink"], "noir")
            if on > 0:
                c.save(); c.translate(116, -34); c.scale(on, on); disque(c, 0, 0, 20, C["ink"]); icone(c, "check", 0, 0, 24, C["blanc"], 3.4); c.restore()
        c.restore()


def s6(c, t):
    sc = scene(c, t, S6, "gauche", "gauche")
    if sc is None: return
    with sc:
        tracker(c, t)
        if t < T6B:
            tel(c, 540, 1200, lambda cc, a, b, d, e: ecran_wechat(cc, a, b, d, e, t, "Fournisseur Baskets", MSGS), w=480, h=960, ry=-6 + 2 * math.sin(t * 2))
        elif t < T6C:
            pop = prog(t, T6B, 0.3, lambda v: rebond(v, 1.6))
            tel(c, 540, 1200, lambda cc, a, b, d, e: ecran_alipay(cc, a, b, d, e, t, T6B + 0.15, TW(54) + 0.55, "Fournisseur"), w=480, h=960, s=mix(0.9, 1, pop), ry=-4 * (1 - pop))
        else:
            u = prog(t, T6C, 0.4, lambda v: rebond(v, 1.4))
            cx, cy, R = 540, 1120, 380 * mix(0.6, 1, u)
            lon0, lat0 = cles(t, [(T6C, 75), (15.6, 55)]), 32
            with Calque(c, borne(u * 2)):
                G.disque(c, cx, cy, R); G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2})
                pr = prog(t, TW(56) + 0.05, 1.0, entreeSortie)
                x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, 1.0, "#CDEFDC", 6, 0.34)
                x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, pr, C["vert"], 8, 0.34)
                G.repere(c, *GZ, cx, cy, R, lon0, lat0, "CHINE", C["vert"], "CN", u)
                G.repere(c, *PAR, cx, cy, R, lon0, lat0, "TOI", C["ink"], None, u)
                if pr > 0 and z_ > 0: carton(c, x_, y_ - 20, 96, 0, 1.0, 8 * math.sin(t * 9))
                if pr >= 1: onde(c, *G.pos(*PAR, lon0, lat0, R, cx, cy)[:2], t, TW(59) - 0.35 + 0.15, 20, 110, C["vert"], 5)
        tampon(c, "REÇU", 790, 1370, t, 15.12, 56, C["vert"], 8, "check")


# ─────────────────────────────────────────── S7 · compte Snapchat : détail, unité, gros, tout
PRODUITS = [("produits/textile/veste-racing-noire", 235, 130, 735), ("produits/textile/veste-racing-bleue", 235, 950, 760), ("produits/electronique/casque-audio", 205, 120, 960),
            ("produits/textile/veste-pluie-marine", 215, 960, 985), ("produits/mobilite/moto-electrique", 250, 130, 1170), ("produits/textile/gilet-maille-creme", 215, 950, 1215),
            ("produits/textile/veste-doudoune-bleue", 190, 175, 1350), ("produits/textile/veste-racing-blanche", 215, 905, 1385)]
T_GROS = TW(65) - 0.08
STORIES = [("photos/chaussures/baskets-portees-marine", "Baskets", 15.62), ("photos/chaussures/baskets-portees-violettes", "Nouveau", 15.72),
           ("photos/chaussures/planche-baskets-12-modeles", "Dispo", 15.82), ("photos/mobilite/casque-moto-plateau", "Casques", 15.92)]
CHATS = [dict(nom="Inès", texte="Tu fais quelle taille ?", t=15.55, couleur="#10B981"),
         dict(nom="Sofiane", texte="T’as encore la bleue ?", t=15.78, couleur="#3B82F6", badge=2),
         dict(nom="Léa", texte="Je les prends !", t=TW(63) + 0.05, couleur="#EC4899"),
         dict(nom="Yanis", texte="Dispo en gros ?", t=TW(67) - 0.1, couleur="#F59E0B", badge=1)]


def ecran_s7(cc, a, b, d, e, t):
    if T_GROS <= t < T_GROS + 0.78:
        video(cc, "videos/guangzhou/guangzhou-cartons-baskets-gros", a, b, d, e, t - T_GROS, 0.9)
        f = 1 - (t - T_GROS) / 0.1
        if f > 0: cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#FFFFFF", 0.8 * f))
    else:
        ecran_snap(cc, a, b, d, e, t, STORIES, CHATS)


def s7(c, t):
    sc = scene(c, t, S7, "gauche", "zoom", de=0.28, ds=0.2)
    if sc is None: return
    with sc:
        for k, (nom, w, x, y) in enumerate(PRODUITS):
            t0 = TW(69) + 0.04 * k
            if t < t0: continue
            u = prog(t, t0, 0.5, lambda v: rebond(v, 1.7))
            bob = 12 * math.sin(t * 2.4 + k)
            c.save(); c.translate(mix(540, x, u), mix(1144, y + bob, u)); c.rotate((-8 if k % 2 else 8) * u); c.scale(u, u)
            produit(c, nom, 0, 0, w, 1.0, True)
            c.restore()
        sx, sy = secousse(t, T_GROS + 0.1, 12, 0.35)
        tel(c, 540 + sx, 1144 + sy, lambda cc, a, b, d, e: ecran_s7(cc, a, b, d, e, t), ry=-5 + 3 * math.sin(t * 1.8), rz=1.5 * math.sin(t * 2.3))
        c.save(); c.translate(130, 745); c.rotate(-12); u = prog(t, TW(60), 0.3, lambda v: rebond(v, 1.9)); c.scale(u, u); logo_app(c, "snapchat", 0, 0, 130); c.restore()
        for lab, t0, x, y, rot, coul in (("AU DÉTAIL", TW(61) - 0.1, 250, 700, -6, C["vert"]), ("À L’UNITÉ", TW(63) - 0.1, 840, 700, 6, C["ink"])):
            if t0 <= t < T_GROS + 0.2:
                u = prog(t, t0, 0.32, lambda v: rebond(v, 1.9))
                pastille_rot(c, lab, x, y, 34, coul, C["blanc"], rot, mix(0.3, 1, u), borne(u * 2))
        if t < T_GROS + 0.95:
            tampon(c, "EN GROS", 540, 1010, t, T_GROS + 0.1, 92, C["rouge"], -7)
        if t >= TW(72) - 0.1:
            u = prog(t, TW(72) - 0.1, 0.34, lambda v: rebond(v, 1.9))
            c.save(); c.translate(790, 720); c.rotate(5); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            w, h = pastille(c, "DE CHINE", 28, 0, 36, C["rouge"], C["blanc"], None, borne(u * 2), (14, 32, 0.22))
            drapeau(c, "CN", -w / 2 - 60, -26, 60, 40, 6)
            c.restore()


# ─────────────────────────────────────────── S8 · le globe : je gère depuis la Thaïlande
def s8(c, t):
    sc = scene(c, t, S8, "zoom", "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1060, 420
        lon0 = cles(t, [(S8[0], 15), (S8[0] + 1.15, 101, entreeSortie)]); lat0 = cles(t, [(S8[0], 32), (S8[0] + 1.15, 15, entreeSortie)])
        G.disque(c, cx, cy, R)
        G.terres(c, cx, cy, R, lon0, lat0, grossir={2: 1.7, 1: 1.1})
        pa = prog(t, TW(80) - 0.3, 0.7, entreeSortie)
        if pa > 0:
            G.arc(c, BKK, GZ, cx, cy, R, lon0, lat0, 1.0, "#CBD5CF", 5, 0.25, [2, 16])
            x_, y_, z_ = G.arc(c, BKK, GZ, cx, cy, R, lon0, lat0, pa, C["ink"], 6, 0.25, [2, 16])
            if z_ > 0: c.save(); c.translate(x_, y_ - 22); logo_app(c, "wechat", 0, 0, 62); c.restore()
        G.repere(c, *BKK, cx, cy, R, lon0, lat0, "MOI", C["ink"], "TH", prog(t, S8[0] + 1.0, 0.4, lambda v: rebond(v, 1.8)), 1.0, 90)
        G.repere(c, *GZ, cx, cy, R, lon0, lat0, "FOURNISSEURS", C["vert"], "CN", prog(t, S8[0] + 1.3, 0.4, lambda v: rebond(v, 1.8)), 1.0, 70)
        if t >= TW(78) - 0.1:
            u = prog(t, TW(78) - 0.1, 0.34, lambda v: rebond(v, 1.9))
            pastille_rot(c, "À LA COMMANDE", 300, 700, 34, C["vert"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "package", (14, 32, 0.22))
        if t >= TW(83) - 0.12:
            u = prog(t, TW(83) - 0.12, 0.16, entree)
            c.save(); c.translate(540, 1390); c.rotate(-4); c.scale(mix(2.6, 1, u), mix(2.6, 1, u))
            with Calque(c, u):
                rrect(c, -330, -62, 660, 124, 24, C["blanc"], 0.94, None, C["ink"], 8)
                drapeau(c, "TH", -296, -22, 62, 42, 6)
                texte_centre(c, "DEPUIS LA THAÏLANDE", 36, 0, 42, C["ink"])
            c.restore()


# ─────────────────────────────────────────── S9 · sans y aller, sans perdre
CARTES9 = [("Le billet d’avion", "plane", TW(86), 790), ("Les milliers d’euros", "banknote", TW(91) - 0.05, 1040), ("Ton temps", "clock", TW(94) - 0.1, 1290)]


def s9(c, t):
    sc = scene(c, t, S9, "bas", "haut", de=0.25, ds=0.2)
    if sc is None: return
    with sc:
        for k, (lab, ic, tx, cy) in enumerate(CARTES9):
            ta = S9[0] + 0.02 + k * 0.1
            u = prog(t, ta, 0.4, lambda v: rebond(v, 1.5))
            x_ = prog(t, tx, 0.22, lambda v: rebond(v, 2.2))
            sx, sy = secousse(t, tx + 0.05, 14, 0.3)
            with Espace(c, 540 + sx, cy + sy, rx=mix(80, 0, u)):
                c.save(); c.translate(540, cy); c.scale(1, 1)
                with Calque(c, borne(u * 2) * mix(1, 0.55, x_)):
                    carte(c, -430, -100, 860, 200, 40, C["blanc"], 1.0, (20, 44, 0.14))
                    rrect(c, -392, -62, 124, 124, 30, C["vertDoux"]); icone(c, ic, -330, 0, 78, C["vert"], 2.3)
                    texte(c, lab, -240, -hauteurLigne(48) / 2, ajuste(lab, 520, 48), C["ink"], "noir")
                    if x_ > 0:
                        lw = 560 * prog(t, tx, 0.18, sortie)
                        trait(c, -250, 4, -250 + lw, 4, C["rouge"], 10)
                c.restore()
                if x_ > 0:
                    c.save(); c.translate(540 + 350, cy); c.scale(x_, x_)
                    disque(c, 0, 0, 62, C["rouge"], 1.0, (10, 26, 0.25)); icone(c, "x", 0, 0, 70, C["blanc"], 3.8)
                    c.restore()


# ─────────────────────────────────────────── sons, flou, éclairs
for k in range(3): son(0.2 + k * 0.06, "pop", -17 - k)
son(0.0, "impact", -6); son(0.0, "whoosh_court", -13); son(0.20, "tampon", -9); son(0.42, "ding", -13); son(0.88, "blip", -11); son(1.60, "whoosh", -13)
for k in range(NSEG): son(S2[0] + 0.12 + k * 0.035, "tick", -19)
son(1.74, "pop", -13); son(TW(9), "whoosh_court", -14)
for k in range(2, NSEG): son(t_mange(k), "croc", -9)
son(T_MANGE0 - 0.03, "impact_doux", -9); son(T_MANGE1 + 0.02, "ching", -10); son(TW(14), "pop", -12); son(TW(13) + 0.25, "tampon", -10); son(4.16, "whoosh", -13)
for k in range(3): son(S3[0] + 0.1 + k * 0.1, "pop", -15)
son(TW(17), "pop", -12); son(5.05, "whoosh_court", -15); son(TW(22), "ching", -9); son(TW(22) + 0.02, "tampon", -11); son(6.32, "whoosh_court", -15); son(6.88, "tampon", -9); son(7.06, "whoosh", -13)
son(S4[0], "swipe", -15)
for ct in CUTS4: son(ct - 0.02, "clic", -9); son(ct, "swipe", -16)
son(TW(32), "pop", -12); son(TW(33), "tampon", -10); son(9.20, "whoosh", -13); son(9.05, "montee", -15)
son(9.50, "impact", -7); son(9.52, "verre", -9); son(10.00, "whoosh_long", -14)
for k, tt in enumerate([TW(40), TW(42), TW(44) - 0.2]): son(tt, "pop", -12); son(tt + 0.3, "clic", -12)
son(TW(42), "tampon", -9); son(TW(44) - 0.05, "pop", -11); son(TW(44) + 0.2, "ding", -12); son(12.0, "whoosh", -13)
son(12.10, "message", -11); son(12.30, "message", -13); son(12.72, "message_in", -11); son(TW(50), "check", -12)
son(T6B - 0.02, "whoosh_court", -14); son(T6B + 0.15, "blip", -13); son(T6B + 0.4, "blip", -14); son(TW(54) + 0.55, "ching", -10); son(TW(54) + 0.1, "check", -12)
son(T6C - 0.02, "whoosh", -13); son(TW(56) + 0.05, "whoosh_long", -15); son(TW(59) - 0.35, "check", -12); son(15.12, "tampon", -10); son(15.50, "whoosh", -13)
son(S7[0], "swipe", -15)
for k in range(4): son(15.62 + k * 0.1, "pop", -16)
son(TW(60), "pop", -12); son(TW(61) - 0.1, "pop", -12); son(15.78, "message_in", -11); son(TW(63) - 0.1, "pop", -12); son(TW(63) + 0.05, "message_in", -11)
son(T_GROS - 0.02, "whoosh_court", -12); son(T_GROS + 0.1, "tampon", -7); son(T_GROS + 0.12, "impact", -9); son(TW(67) - 0.1, "message_in", -11)
for k in range(8): son(TW(69) + 0.04 * k, "pop", -14)
son(TW(69), "whoosh", -13); son(TW(72) - 0.1, "pop", -11); son(19.28, "whoosh", -13)
son(S8[0], "whoosh_long", -13); son(S8[0] + 1.0, "pop", -12); son(S8[0] + 1.3, "pop", -12); son(TW(78) - 0.1, "pop", -12)
for k in range(5): son(TW(80) - 0.3 + k * 0.13, "tick", -17)
son(TW(83) - 0.12, "tampon", -8); son(TW(83) - 0.08, "impact_doux", -10); son(21.86, "whoosh", -13)
son(S9[0], "swipe", -14)
for k, (_, _, tx, _) in enumerate(CARTES9): son(S9[0] + 0.02 + k * 0.1, "pop", -14); son(tx, "tampon", -8); son(tx + 0.02, "impact_doux", -11)
son(24.78, "whoosh", -13)
for tl in TL: son(tl, "frappe", -13)
son(T_ENVOI, "clic", -10); son(T_ENVOI + 0.04, "whoosh_court", -13); son(T_ENVOI + 0.16, "message", -10); son(T_CTA, "pop", -14)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.14, "impact_doux", -8); son(T_FIN + 0.16, "verre", -8); son(T_FIN + 0.36, "pop", -11)

for a, b in [(0.0, 0.28), (1.60, 1.9), (S2[0] + 2.4, S2[0] + 2.6), (4.16, 4.5), (5.05, 5.5), (6.32, 6.87), (7.06, 7.4), (CUTS4[0] - 0.05, CUTS4[0] + 0.12),
             (CUTS4[1] - 0.05, CUTS4[1] + 0.12), (CUTS4[2] - 0.05, CUTS4[2] + 0.12), (9.05, 10.5), (11.95, 12.25), (T6B - 0.05, T6B + 0.2), (T6C - 0.05, T6C + 0.3),
             (15.5, 15.85), (T_GROS - 0.05, T_GROS + 0.2), (TW(69) - 0.05, TW(69) + 0.4), (19.28, 19.6), (21.66, 22.0), (24.55, 24.85), (T_ENVOI, T_ENVOI + 0.32), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, C["rouge"], 0.12), (1.74, C["rouge"], 0.10), (T_MANGE0, C["rouge"], 0.10), (TW(22), C["rouge"], 0.10), (6.88, C["rouge"], 0.08), (9.50, C["vert"], 0.12),
                    (TW(42), C["vert"], 0.10), (TW(54) + 0.55, C["vert"], 0.10), (15.12, C["vert"], 0.08), (T_GROS + 0.1, C["rouge"], 0.12),
                    (TW(83) - 0.1, C["vert"], 0.10), (TW(94) - 0.1, C["rouge"], 0.10), (T_FIN + 0.14, C["vert"], 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def alpha_bandeau(t, r):
    return borne(prog(t, 0.45, 0.3) * (1 - prog(t, T_FIN - 0.05, 0.25)) * (1 - borne(r / 400)))


def dessine(c, t):
    fond(c, t)
    for s in (s1, s2, s3, s4, s5, s6, s7, s8, s9):
        s(c, t)
    r = disque_transition(c, t)
    bandeau(c, t, alpha_bandeau(t, r))
    cta_whatsapp(c, t, T_CTA, TL, T_ENVOI, T_FIN, DUREE)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["ink"])
