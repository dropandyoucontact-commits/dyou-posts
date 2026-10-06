"""CB-M05 « Reste ici » — ChinaBook pour qui veut partir sourcer à Kinbo (25,1 s).

Accroche de Youssef (06/10/2026) : tu comptes aller en Chine, à Kinbo, trouver tes fournisseurs ?
Reste ici. Le voyage coûte cher ; moi je l'ai déjà fait, les fournisseurs validés sont dans ton
téléphone avec le ChinaBook ; tu bosses dès demain depuis la France, ou tu prends ton billet si tu
as déjà ta clientèle, et tu gères tes commandes à distance, à l'unité ou en lot.

Voix : moteur/outils/voix.py (Tomy, 3,8 mots/s). Chaque élément cite le mot qu'il illustre.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *

DUREE = 25.15
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a
G = Globe()

GZ, PAR = (113.26, 23.13), (2.35, 48.86)

# ─────────────────────────────────────────── sous-titres
SOUS = SousTitres(K, [
    [(0, "Tu", "", -0.45), (1, "comptes", "", -0.3), (2, "aller"), (3, "en"), (4, "Chine,", "r")],
    [(5, "à"), (6, "Kinbo,", "g"), (7, "pour"), (8, "trouver"), (9, "tes"), (10, "fournisseurs ?", "g")],
    [(11, "Attends.", "r")],
    [(12, "Reste", "g"), (13, "ici.", "g")],
    [(14, "T’as"), (15, "pas"), (16, "besoin"), (17, "d’aller"), (18, "jusque-là.", "r")],
    [(19, "Le"), (20, "billet,"), (21, "l’hôtel,")],
    [(22, "les"), (23, "semaines"), (24, "sur"), (25, "place"), (26, "à"), (27, "tester"), (28, "des"), (29, "fournisseurs :")],
    [(30, "ça"), (31, "te"), (32, "coûte"), (33, "des"), (34, "milliers", "r"), (35, "d’euros.", "r")],
    [(36, "Moi,"), (37, "je"), (38, "l’ai"), (39, "déjà", "g"), (40, "fait.", "g")],
    [(41, "Les"), (42, "fournisseurs"), (43, "que"), (44, "j’ai"), (45, "validés,", "g")],
    [(46, "je"), (47, "te"), (48, "les"), (49, "mets"), (50, "dans"), (51, "ton"), (52, "téléphone,", "g")],
    [(53, "avec"), (54, "le"), (55, "ChinaBook.", "g")],
    [(57, "Tu"), (58, "bosses"), (59, "dès"), (60, "demain,", "g"), (61, "depuis"), (62, "la"), (63, "France.", "g")],
    [(64, "Et"), (65, "si"), (66, "t’as"), (67, "déjà"), (68, "ta"), (69, "clientèle,", "g")],
    [(70, "tu"), (71, "prends"), (72, "ton"), (73, "billet,")],
    [(74, "et"), (75, "tu"), (76, "gères"), (77, "tes"), (78, "commandes"), (79, "à"), (80, "distance,", "g")],
    [(81, "à"), (82, "l’unité", "g"), (83, "ou"), (84, "en"), (85, "lot.", "g")],
    [(86, "Envoie-moi"), (87, "« CHINA »", "g"), (88, "sur"), (89, "WhatsApp.")],
    [(None, "Ton", "", 23.75), (None, "accès", "", 23.82), (None, "direct", "g", 23.91), (None, "à", "", 24.01), (None, "la", "", 24.06), (None, "Chine.", "", 24.12)],
])

# ─────────────────────────────────────────── fenêtres de scène
S1, S2, S3, S4, S5 = (0.0, 2.88), (2.76, 5.68), (5.55, 10.62), (10.45, 12.02), (11.85, 15.45)
S6, S7, S8, S9 = (15.30, 17.32), (17.18, 19.56), (19.42, 21.02), (20.86, 22.40)
T_CTA, T_FIN = 22.25, 23.68
TL = [TW(87) - 0.16 + k * 0.07 for k in range(5)]
T_ENVOI = TW(88)
T_KINBO = TW(6) - 0.06
T_LOGO = TW(55) - 0.12


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


def billet(c, cx, cy, s=1.0, rot=0.0, alpha=1.0, coche=0.0):
    """carte d'embarquement Paris → Guangzhou (sans compagnie, sans numéro)"""
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        carte(c, -420, -200, 840, 400, 40, C["blanc"], 1.0, (26, 60, 0.22))
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-420, -200, 840, 400), 40, 40), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(-420, -200, 840, 96), peinture(C["ink"]))
        c.restore()
        icone(c, "plane-takeoff", -364, -152, 46, C["blanc"], 2.4)
        texte(c, "CARTE D’EMBARQUEMENT", -320, -172, 34, C["blanc"], "noir", track=0.06)
        for x, pays, ville in ((-370, "FR", "PARIS"), (95, "CN", "GUANGZHOU")):
            drapeau(c, pays, x, -76, 66, 44, 7)
            texte(c, ville, x, -18, ajuste(ville, 290, 54), C["ink"], "noir")
        icone(c, "plane", -10, -30, 64, C["vert"], 2.4)
        trait(c, -400, 92, 230, 92, C["ligne"], 4, 1.0, (2, 14))
        for k, (lab, val) in enumerate((("PORTE", "—"), ("SIÈGE", "—"))):
            texte(c, lab, -370 + k * 220, 116, 22, C["gris"], "fort", track=0.06)
            texte(c, val, -370 + k * 220, 142, 34, C["ink"], "noir")
        qr_code(c, 262, 96, 120)
        if coche > 0:
            c.save(); c.translate(360, -150); c.scale(coche, coche)
            disque(c, 0, 0, 52, C["vert"], 1.0, (10, 26, 0.25)); icone(c, "check", 0, 0, 58, C["blanc"], 3.6)
            c.restore()
    c.restore()


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


def apparait(t, t0, s=1.9, d=0.34):
    return prog(t, t0, d, lambda v: rebond(v, s))


# ─────────────────────────────────────────── S1 · tu comptes aller à Kinbo ?
def s1(c, t):
    sc = scene(c, t, S1, None, "zoom", ds=0.2)
    if sc is None: return
    with sc:
        punch = 1.0 + 0.14 * (1 - prog(t, 0, 0.3, sortie))
        bob = 10 * math.sin(t * 3.2)
        billet(c, 540, 1060 + bob, punch * mix(1, 0.86, prog(t, T_KINBO - 0.1, 0.3)), -4 + 2 * math.sin(t * 2.6))
        photo_lieu(c, t, "lieux/kinbo-devanture-guangzhou", T_KINBO, T_KINBO + 1.0, 540, 1090, 520, 693, -5, "KINBO", "GUANGZHOU")
        if t >= TW(10) - 0.08:
            u = apparait(t, TW(10) - 0.08)
            pastille_rot(c, "TES FOURNISSEURS ?", 540, 1390, 40, C["vert"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "search", (14, 32, 0.22))


# ─────────────────────────────────────────── S2 · attends, reste ici, pas besoin d'aller jusque-là
def s2(c, t):
    sc = scene(c, t, S2, "zoom", "gauche", de=0.3, ds=0.22)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1130, 400
        lon0, lat0 = cles(t, [(S2[0], 30), (TW(18), 62, entreeSortie)]), 38
        G.disque(c, cx, cy, R); G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2})
        G.repere(c, *GZ, cx, cy, R, lon0, lat0, "KINBO", C["vert"], "CN", apparait(t, S2[0] + 0.2, 1.8, 0.4), 1.0, 70)
        G.repere(c, *PAR, cx, cy, R, lon0, lat0, "TOI · ICI", C["ink"], "FR", apparait(t, TW(12) - 0.05, 1.8, 0.4), 1.0, 80)
        if t >= TW(12):
            px, py = G.pos(*PAR, lon0, lat0, R, cx, cy)[:2]
            onde(c, px, py, t, TW(12), 20, 120, C["ink"], 5); onde(c, px, py, t, TW(13), 20, 120, C["ink"], 5)
        pv = prog(t, TW(14), TW(18) - TW(14) + 0.05, lin)
        if pv > 0:
            G.arc(c, PAR, GZ, cx, cy, R, lon0, lat0, 1.0, "#CBD5CF", 5, 0.3, [2, 16])
            x_, y_, z_ = G.arc(c, PAR, GZ, cx, cy, R, lon0, lat0, min(pv, 0.62), C["ink"], 6, 0.3, [2, 16])
            c.save(); c.translate(x_, y_); c.rotate(-20); disque(c, 0, 0, 42, C["ink"], 1.0, (8, 20, 0.2)); icone(c, "plane", 0, 0, 48, C["blanc"], 2.4); c.restore()
            if t >= TW(18) - 0.05:
                ux = apparait(t, TW(18) - 0.05, 2.2, 0.22)
                c.save(); c.translate(x_ + 48, y_ - 48); c.scale(ux, ux)
                disque(c, 0, 0, 50, C["rouge"], 1.0, (10, 26, 0.25)); icone(c, "x", 0, 0, 58, C["blanc"], 3.8)
                c.restore()
        # « Attends. » : la main qui claque, puis s'efface sur « Reste »
        if TW(11) - 0.1 <= t < TW(12) + 0.2:
            u = prog(t, TW(11) - 0.1, 0.18, entree); o = prog(t, TW(12) - 0.05, 0.22, entree)
            sx, sy = secousse(t, TW(11) + 0.05, 14, 0.35)
            c.save(); c.translate(540 + sx, 1100 + sy - 300 * o); s = mix(2.4, 1, u) * mix(1, 0.3, o); c.scale(s, s)
            with Calque(c, u * (1 - o)):
                disque(c, 0, 0, 230, C["rouge"], 1.0, (20, 50, 0.3)); icone(c, "hand", 0, 0, 230, C["blanc"], 2.2)
            c.restore()
        tampon(c, "PAS BESOIN", 540, 1420, t, TW(18), 70, C["rouge"], -6, "x")


# ─────────────────────────────────────────── S3 · billet, hôtel, semaines : des milliers d'euros
CARTES3 = [("Le billet d’avion", "plane", S3[0] + 0.05, 760), ("L’hôtel", "bed-double", TW(21) - 0.05, 1000),
           ("Des semaines à tester", "calendar", TW(23) - 0.05, 1240)]


def s3(c, t):
    sc = scene(c, t, S3, "bas", "haut", de=0.25, ds=0.22)
    if sc is None: return
    with sc:
        T_M = TW(34) - 0.05
        serre = prog(t, T_M, 0.3, lambda v: rebond(v, 1.6))
        sx, sy = secousse(t, T_M, 16, 0.4)
        for k, (lab, ic, t0, cy) in enumerate(CARTES3):
            ug = prog(t, S3[0] + 0.15 + 0.1 * k, 0.35, lambda v: rebond(v, 1.7)) * (1 - prog(t, t0 - 0.05, 0.15))
            if k > 0 and ug > 0:
                c.save(); c.translate(540, cy); c.scale(mix(0.6, 1, ug), mix(0.6, 1, ug))
                with Calque(c, borne(ug * 2)):
                    rrect(c, -430, -100, 860, 200, 40, C["fondDoux"], 1.0, None, "#D5DBD8", 4)
                    disque(c, -330, 0, 54, "#E3E8E5"); icone(c, "circle-help", -330, 0, 62, C["grisClair"], 2.2)
                    rrect(c, -240, -36, 340, 34, 17, "#E3E8E5"); rrect(c, -240, 16, 200, 24, 12, "#E3E8E5")
                c.restore()
            if t < t0: continue
            u = prog(t, t0, 0.4, lambda v: rebond(v, 1.5))
            y_ = mix(cy, 1000 + (k - 1) * 120, serre)
            with Espace(c, 540 + sx, y_ + sy, rx=mix(80, 0, u)):
                c.save(); c.translate(540 + sx + 900 * (1 - u), y_ + sy); c.scale(mix(1, 0.86, serre), mix(1, 0.86, serre))
                carte(c, -430, -100, 860, 200, 40, C["blanc"], 1.0, (20, 44, 0.14))
                rrect(c, -392, -62, 124, 124, 30, C["vertDoux"]); icone(c, ic, -330, 0, 78, C["vert"], 2.3)
                texte(c, lab, -240, -hauteurLigne(48) / 2, ajuste(lab, 440, 48), C["ink"], "noir")
                ue = apparait(t, t0 + 0.2, 2.0, 0.3)
                c.save(); c.translate(350, 0); c.scale(ue, ue)
                disque(c, 0, 0, 56, C["rougeDoux"]); icone(c, "banknote", 0, 0, 62, C["rouge"], 2.4)
                c.restore()
                c.restore()
        if t >= T_M:
            u = apparait(t, T_M, 2.0, 0.3)
            c.save(); c.translate(540, 1420); c.rotate(-4); c.scale(mix(2.4, 1, prog(t, T_M, 0.18, entree)) * mix(0.6, 1, u), mix(2.4, 1, prog(t, T_M, 0.18, entree)) * mix(0.6, 1, u))
            pastille(c, "DES MILLIERS D’EUROS", 0, 0, 48, C["rouge"], C["blanc"], "banknote", borne(u * 2), (16, 40, 0.3))
            c.restore()
            etincelles(c, 540, 1420, t, T_M + 0.05, 10, 300, C["rouge"])


# ─────────────────────────────────────────── S4 · moi, je l'ai déjà fait
def s4(c, t):
    sc = scene(c, t, S4, "droite", "zoom", de=0.28, ds=0.2)
    if sc is None: return
    with sc:
        tel(c, 540, 1144, lambda cc, a, b, d, e: video(cc, "videos/chaussures/baskets-stock-1", a, b, d, e, t - S4[0], 2.2, rogne=(0, 0, 0, 0.23)),
            ry=-8 + 3 * math.sin(t * 2.0), rz=-2 * math.sin(t * 2.7))
        if t >= TW(36) - 0.05:
            u = apparait(t, TW(36) - 0.05)
            c.save(); c.translate(330, 700); c.rotate(-6); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            w, h = pastille(c, "GUANGZHOU", 20, 0, 34, C["ink"], C["blanc"], None, borne(u * 2), (14, 32, 0.22))
            drapeau(c, "CN", -w / 2 - 44, -24, 56, 38, 6)
            c.restore()
        tampon(c, "DÉJÀ FAIT", 760, 1360, t, TW(39), 62, C["vert"], 8, "check")


# ─────────────────────────────────────────── S5 · les validés dans ton téléphone, avec le ChinaBook
def s5(c, t):
    sc = scene(c, t, S5, "gauche", None, de=0.28)
    if sc is None: return
    with sc:
        lignes = [dict(t=TW(42), image="photos/chaussures/etagere-baskets-running-6-modeles", nom="Baskets", ville="Guangzhou", zoom=1.7, fx=0.5, fy=0.28),
                  dict(t=TW(45) - 0.05, image="photos/chaussures/planche-baskets-12-modeles", nom="Sneakers", ville="Guangzhou"),
                  dict(t=TW(49), image="photos/mobilite/casque-moto-plateau", nom="Électronique", ville="Shenzhen", fy=0.55)]
        pulse = battement(t, TW(52), 0.08, 0.35)
        tel(c, 540, 1144, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=-5 + 2 * math.sin(t * 2.2), s=pulse)
        tampon(c, "VALIDÉS", 790, 760, t, TW(45), 58, C["vert"], -8, "badge-check")
        confettis(c, 790, 760, t, TW(45) + 0.04, 22, 320, 9)
        if t >= TW(52) - 0.08:
            u = apparait(t, TW(52) - 0.08)
            pastille_rot(c, "DANS TON TÉLÉPHONE", 540, 1420, 38, C["ink"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "phone", (14, 32, 0.25))


def disque_logo(c, t):
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (S6[0] - 0.05, 1750), (S6[0] + 0.35, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, C["ink"])
        if T_LOGO + 0.2 <= t <= S6[0] + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, S6[0] - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * so)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2, lw, borne(u * 3) * (1 - so))
    return r


# ─────────────────────────────────────────── S6 · dès demain, depuis la France
def s6(c, t):
    sc = scene(c, t, S6, None, "gauche", ds=0.22)
    if sc is None: return
    with sc:
        u = prog(t, S6[0] + 0.1, 0.45, lambda v: rebond(v, 1.5))
        bob = 8 * math.sin(t * 3)
        with Espace(c, 540, 1060 + bob, ry=mix(-50, -6, u), rz=-3):
            c.save(); c.translate(540, 1060 + bob); c.scale(mix(0.5, 1, u), mix(0.5, 1, u))
            with Calque(c, borne(u * 2)):
                carte(c, -260, -300, 520, 600, 46, C["blanc"], 1.0, (26, 60, 0.18))
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-260, -300, 520, 600), 46, 46), doAntiAlias=True)
                c.drawRect(skia.Rect.MakeXYWH(-260, -300, 520, 170), peinture(C["vert"]))
                c.restore()
                for x in (-150, 150): disque(c, x, -300, 22, C["ink"])
                texte_centre(c, "DEMAIN", 0, -215, 84, C["blanc"])
                ud = apparait(t, TW(60) - 0.05, 2.0, 0.34)
                c.save(); c.translate(0, 70); c.scale(ud, ud)
                disque(c, 0, 0, 120, C["vertDoux"]); icone(c, "laptop", 0, 0, 140, C["vert"], 2.2)
                c.restore()
                texte_centre(c, "Tu commences", 0, 230, 38, C["gris"], "fort", borne(ud * 2), 0)
            c.restore()
        if t >= TW(63) - 0.08:
            ue = apparait(t, TW(63) - 0.08)
            c.save(); c.translate(560, 1440); c.rotate(-4); c.scale(mix(0.4, 1, ue), mix(0.4, 1, ue))
            w, h = pastille(c, "DEPUIS LA FRANCE", 34, 0, 40, C["ink"], C["blanc"], None, borne(ue * 2), (14, 32, 0.25))
            drapeau(c, "FR", -w / 2 - 66, -27, 66, 44, 6)
            c.restore()
        confettis(c, 540, 820, t, TW(60), 20, 300, 5)


# ─────────────────────────────────────────── S7 · ta clientèle, puis ton billet
STORIES = [("photos/chaussures/baskets-portees-marine", "Baskets", 17.25), ("photos/chaussures/baskets-portees-violettes", "Nouveau", 17.32),
           ("photos/chaussures/planche-baskets-12-modeles", "Dispo", 17.39), ("photos/mobilite/casque-moto-plateau", "Casques", 17.46)]
CHATS = [dict(nom="Inès", texte="Tu fais quelle taille ?", t=17.3, couleur="#10B981"),
         dict(nom="Sofiane", texte="T’as encore la bleue ?", t=TW(66), couleur="#3B82F6", badge=2),
         dict(nom="Léa", texte="Je les prends !", t=TW(68), couleur="#EC4899"),
         dict(nom="Yanis", texte="Dispo en gros ?", t=TW(69) + 0.1, couleur="#F59E0B", badge=1)]


def s7(c, t):
    sc = scene(c, t, S7, "gauche", "gauche", de=0.28, ds=0.22)
    if sc is None: return
    with sc:
        recul = prog(t, TW(71) - 0.15, 0.35, sortie)
        tel(c, 540 - 120 * recul, 1144 - 60 * recul, lambda cc, a, b, d, e: ecran_snap(cc, a, b, d, e, t, STORIES, CHATS), ry=-6 + 3 * math.sin(t * 2.0), s=mix(1, 0.85, recul))
        if t >= TW(69) - 0.08:
            u = apparait(t, TW(69) - 0.08)
            pastille_rot(c, "TA CLIENTÈLE", 300, 700, 38, C["vert"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "users", (14, 32, 0.22))
        if t >= TW(71) - 0.15:
            ub = prog(t, TW(71) - 0.15, 0.4, lambda v: rebond(v, 1.4))
            billet(c, mix(1500, 560, ub), 1280, 0.82, mix(14, -5, ub), 1.0, apparait(t, TW(73), 2.0, 0.3))


# ─────────────────────────────────────────── S8 · tes commandes à distance
def s8(c, t):
    sc = scene(c, t, S8, "zoom", "gauche", de=0.28, ds=0.2)
    if sc is None: return
    with sc:
        cx, cy, R = 540, 1100, 400
        lon0, lat0 = 58, 38
        G.disque(c, cx, cy, R); G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2})
        G.repere(c, *PAR, cx, cy, R, lon0, lat0, "TOI", C["ink"], "FR", apparait(t, S8[0] + 0.15, 1.8, 0.4), 1.0, 80)
        G.repere(c, *GZ, cx, cy, R, lon0, lat0, "FOURNISSEURS", C["vert"], "CN", apparait(t, S8[0] + 0.3, 1.8, 0.4), 1.0, 70)
        pm = prog(t, TW(76) - 0.05, 0.6, entreeSortie)
        if pm > 0:
            G.arc(c, PAR, GZ, cx, cy, R, lon0, lat0, 1.0, "#CBD5CF", 5, 0.3, [2, 16])
            x_, y_, z_ = G.arc(c, PAR, GZ, cx, cy, R, lon0, lat0, pm, C["ink"], 6, 0.3, [2, 16])
            if pm < 1: c.save(); c.translate(x_, y_ - 22); logo_app(c, "wechat", 0, 0, 62); c.restore()
        pc = prog(t, TW(78) + 0.05, 0.75, entreeSortie)
        if pc > 0:
            G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, 1.0, "#CDEFDC", 6, 0.42)
            x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, pc, C["vert"], 8, 0.42)
            if pc < 1: carton(c, x_, y_ - 20, 96, 0, 1.0, 8 * math.sin(t * 9))
            else: onde(c, *G.pos(*PAR, lon0, lat0, R, cx, cy)[:2], t, TW(78) + 0.8, 20, 110, C["vert"], 5)
        if t >= TW(80) - 0.1:
            u = apparait(t, TW(80) - 0.1)
            pastille_rot(c, "À DISTANCE", 760, 1420, 40, C["ink"], C["blanc"], 5, mix(0.3, 1, u), borne(u * 2), "laptop", (14, 32, 0.25))


# ─────────────────────────────────────────── S9 · à l'unité ou en lot
def s9(c, t):
    sc = scene(c, t, S9, "gauche", None, de=0.28)
    if sc is None: return
    with sc:
        u1 = apparait(t, TW(82) - 0.08, 1.7, 0.4)
        if u1 > 0:
            bob = 10 * math.sin(t * 4)
            sneaker(c, 290, 1000 + bob, 400 * mix(0.5, 1, u1), alpha=borne(u1 * 2), rot=-6)
            ombre_sol(c, 290, 1120, 160, 16, 0.15 * u1)
            pastille_rot(c, "À L’UNITÉ", 290, 1290, 40, C["vert"], C["blanc"], -5, mix(0.3, 1, u1), borne(u1 * 2))
        for k, (dx, dy) in enumerate(((-90, 70), (90, 70), (0, -70), (-90, -210), (90, -210))):
            uk = apparait(t, TW(85) - 0.12 + 0.06 * k, 2.0, 0.32)
            if uk > 0:
                carton(c, 790 + dx, 1050 + dy - 200 * (1 - uk), 170, 0, borne(uk * 2), 3 * math.sin(t * 5 + k))
        if t >= TW(85) - 0.05:
            u = apparait(t, TW(85) - 0.05)
            pastille_rot(c, "EN LOT", 790, 1290, 40, C["ink"], C["blanc"], 5, mix(0.3, 1, u), borne(u * 2), "package")


# ─────────────────────────────────────────── sons, flou, éclairs
son(0.0, "impact", -6); son(0.0, "whoosh_court", -12); son(0.3, "ding", -14)
son(T_KINBO - 0.12, "whoosh_court", -12); son(T_KINBO, "clic", -9); son(T_KINBO + 0.1, "pop", -12); son(T_KINBO + 1.0, "whoosh_court", -14)
son(TW(10) - 0.08, "pop", -11); son(2.74, "whoosh", -13); son(S2[0] + 0.2, "pop", -13)
son(TW(11) - 0.1, "tampon", -6); son(TW(11) - 0.08, "impact", -7); son(TW(12) - 0.05, "pop", -11); son(TW(12), "blip", -12); son(TW(13), "blip", -14)
son(TW(14), "whoosh_long", -15); son(TW(18) - 0.05, "impact_doux", -9); son(TW(18) - 0.1, "tampon", -8); son(5.53, "whoosh", -13)
for lab, ic, t0, cy in CARTES3: son(t0, "pop", -12); son(t0 + 0.2, "ching", -15)
son(TW(34) - 0.05, "impact", -7); son(TW(34) - 0.03, "tampon", -9); son(10.43, "whoosh", -13)
son(S4[0], "swipe", -15); son(TW(36) - 0.05, "pop", -12); son(TW(39) - 0.1, "tampon", -9); son(TW(39), "check", -12); son(11.83, "whoosh", -13)
son(TW(42), "pop", -12); son(TW(45) - 0.05, "pop", -12); son(TW(49), "pop", -12); son(TW(45) - 0.1, "tampon", -9); son(TW(45) + 0.04, "ching", -11)
son(TW(52) - 0.08, "pop", -11); son(TW(52), "message_in", -12)
son(T_LOGO - 0.1, "montee", -15); son(T_LOGO + 0.24, "impact", -7); son(T_LOGO + 0.26, "verre", -9); son(S6[0] - 0.05, "whoosh_long", -14)
son(TW(60) - 0.05, "pop", -11); son(TW(60), "ding", -12); son(TW(63) - 0.08, "pop", -11); son(17.16, "whoosh", -13)
for k in range(4): son(17.25 + k * 0.07, "pop", -16)
son(17.3, "message_in", -12); son(TW(66), "message_in", -12); son(TW(68), "message_in", -12); son(TW(69) - 0.08, "pop", -11)
son(TW(71) - 0.15, "whoosh_court", -12); son(TW(73), "check", -11); son(19.40, "whoosh", -13)
son(S8[0] + 0.15, "pop", -13); son(S8[0] + 0.3, "pop", -13); son(TW(76) - 0.05, "message", -11); son(TW(78) + 0.05, "whoosh_long", -14); son(TW(80) - 0.1, "pop", -11)
son(20.84, "swipe", -14); son(TW(82) - 0.08, "pop", -11)
for k in range(5): son(TW(85) - 0.12 + 0.06 * k, "impact_doux", -13)
son(T_CTA - 0.1, "whoosh", -13)
for tl in TL: son(tl, "frappe", -13)
son(T_ENVOI, "clic", -10); son(T_ENVOI + 0.04, "whoosh_court", -13); son(T_ENVOI + 0.16, "message", -10)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.14, "impact_doux", -8); son(T_FIN + 0.16, "verre", -8); son(T_FIN + 0.36, "pop", -11)

for a, b in [(T_KINBO - 0.14, T_KINBO + 0.12), (T_KINBO + 0.98, T_KINBO + 1.26), (2.74, 3.06), (TW(11) - 0.1, TW(11) + 0.1), (TW(12) - 0.05, TW(12) + 0.2),
             (5.53, 5.85), (TW(34) - 0.05, TW(34) + 0.2), (10.43, 10.75), (11.83, 12.15), (T_LOGO, T_LOGO + 0.4), (S6[0] - 0.05, S6[0] + 0.4),
             (17.16, 17.48), (TW(71) - 0.15, TW(71) + 0.25), (19.40, 19.72), (20.84, 21.16), (T_CTA - 0.1, T_CTA + 0.3), (T_ENVOI, T_ENVOI + 0.32), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_KINBO, "#FFFFFF", 0.25), (TW(11) - 0.08, C["rouge"], 0.14), (TW(18) - 0.05, C["rouge"], 0.10), (TW(34) - 0.05, C["rouge"], 0.12),
                    (TW(39), C["vert"], 0.08), (TW(45), C["vert"], 0.08), (T_LOGO + 0.24, C["blanc"], 0.15), (TW(60), C["vert"], 0.08), (T_FIN + 0.14, C["vert"], 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def alpha_bandeau(t, r):
    return borne(prog(t, 0.45, 0.3) * (1 - prog(t, T_FIN - 0.05, 0.25)) * (1 - borne(r / 400)))


def dessine(c, t):
    fond(c, t)
    for s in (s1, s2, s3, s4, s5, s6, s7, s8, s9):
        s(c, t)
    r = disque_logo(c, t)
    bandeau(c, t, alpha_bandeau(t, r))
    cta_whatsapp(c, t, T_CTA, TL, T_ENVOI, T_FIN, DUREE)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if r > 900 else C["ink"])
