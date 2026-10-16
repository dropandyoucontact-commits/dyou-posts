"""MQ-M05 « Vous ne pouvez pas être partout » — script du client (hook 2), 16/10/2026.

Charte et briques de MQ-M04 (fond clair, Archivo Black, cases à médias, voix Tomy 4,2 mots/s, −13 LUFS).
Retours du client sur MQ-M04 appliqués :
- globe : le globe EN POINTS (comme ChinaBook), pays allumé, au lieu du globe blanc sculpté ;
- graphique « vos ventes » : même style de barres, mais sous chaque barre un modèle DIFFÉRENT (photos du client).
Nouveaux médias du client (banque/monarque) : produits sur fond clair, fiches techniques.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import agence
from studio import lettres, Groupe, eclats, entre, SousTitresEncre, curseur
from monarque import *
from monarque import VERT, ROUGE

polices(P)
K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.7, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresEncre(K, y=1440, larg=900, taille=54, fam="gras", max_mots=5)
G = Globe()
TERRE = "#BDB8B1"

# repères (index des mots de timing.json)
T_QUI, T_JOUR, T_ERR, T_HEURE, T_PRIO = TW(20), TW(29), TW(43), TW(53), TW(63)
T_VENDRE, T_FIDEL, T_DEVEL, T_BUSI = TW(66), TW(67), TW(69), TW(71)
T_SOY, T_DEVP, T_PAS, T_IDEE, T_USINE = TW(72), TW(74), TW(78), TW(84), TW(87)
T_MAIT, T_MAT, T_COUT, T_QUAL, T_PROD = TW(90), TW(93), TW(95), TW(97), TW(100)
T_SURT, T_BONNES, T_AVANT, T_CHER = TW(101), TW(106), TW(108), TW(112)
T_LA, T_MQ, T_ACC = TW(114), TW(118), TW(122)
T_DEVPROD, T_JUSQ, T_PRODF = TW(126), TW(128), TW(130)
T_COMP, T_PRES, T_COEUR, T_CHN = TW(131), TW(136), TW(140), TW(144)
T_ROLE, T_NOTRE, T_METH, T_MAIT2, T_COMPET = TW(145), TW(153), TW(164), TW(165), TW(167)
T_FIN, T_VDEV, T_NOUS, T_URL = TW(168), TW(169), TW(173), TW(179) + 0.5

MODELES = ["produits/veste-ceinturee-prune", "produits/blouson-cuir-noir", "produits/veste-zip-marine", "produits/chemise-rayee-bordeaux"]


def melange(c1, c2, u):
    a, b = hexa(c1), hexa(c2)
    u = borne(u)
    f = lambda s: int(round(((a >> s) & 255) * (1 - u) + ((b >> s) & 255) * u))
    return "#%02X%02X%02X" % (f(16), f(8), f(0))


# ─────────────────────────────────────────── le graphique « vos ventes » (style validé, un modèle différent par barre)
def graphique(c, t, cx, cy, hb, best, best_on, alpha=1.0, s=1.0, label="VOS VENTES"):
    x0, y0, w, h = cx - 420, cy - 330, 840, 660
    if alpha <= 0.01: return x0, y0, y0 + 470
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, alpha):
        cadre(c, x0, y0, w, h, 44)
        texte(c, label, x0 + 60, y0 + 50, 34, ENCRE, "noir", track=0.06)
        base = y0 + 470
        for k in range(4):
            x = x0 + 90 + k * 180
            col = BEIGE if (k == best and best_on) else "#DCD8D2"
            hh = max(14, 330 * hb[k])
            rrect(c, x, base - hh, 120, hh, 18, col)
            # le modèle sous la barre, entier (photo du client, fond clair)
            rrect(c, x - 5, base + 18, 130, 150, 22, "#EFEDEA")
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 5, base + 18, 130, 150), 22, 22), True)
            image_cover(c, MODELES[k], x - 5, base + 18, 130, 150, 1.0, 0.5, 0.5); c.restore()
            if k == best and best_on:
                rrect(c, x - 5, base + 18, 130, 150, 22, BEIGE, 1, None, BEIGE, 5)
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 5, base + 18, 130, 150), 22, 22), True)
                image_cover(c, MODELES[k], x + 0, base + 23, 120, 140, 1.0, 0.5, 0.5); c.restore()
    c.restore()
    return x0, y0, base


# ─────────────────────────────────────────── 1 · hook : vous voulez être partout
COINS = [("Collections", "shirt", "produits/veste-ceinturee-prune", None, 70, 590, TW(9)),
         ("Fournisseurs", "phone", "rushes/bureau", 1.2, 730, 590, TW(11)),
         ("Production", "factory", "rushes/machines", 1.2, 70, 1000, TW(13)),
         ("Développement", "scissors", "ensemble-sweat-jupe", None, 730, 1000, TW(15))]
CW, CH = 280, 340


def hook(c, t):
    if t > T_QUI + 0.4: return
    g = Groupe(c, t, -1, T_QUI, ent="aucune", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VOUS VOULEZ", -0.55, T_QUI - 0.1, y=340)
        titre(c, t, "ÊTRE PARTOUT", -0.45, TW(16) - 0.1, y=455, couleur=ENCRE)
        titre(c, t, "TOUT GÉRER", TW(16) - 0.05, T_QUI - 0.1, y=455, couleur=ROUGE)
        # le centre, tiré vers chaque nouvelle case
        sh = [0, 0]
        for (_, _, _, _, x, y, t0) in COINS:
            d = secousse(t, t0 + 0.05, 10, 0.3)
            sh[0] += d[0]; sh[1] += d[1]
        alerte = t > TW(18)
        sa = secousse(t, TW(18), 18, 0.5)
        X, Y = 540 + sh[0] + sa[0], 960 + sh[1] + sa[1]
        for k, (lab, ic, nom, vit, x, y, t0) in enumerate(COINS):
            u = entre(t, -0.4 + 0.08 * k, 0.42, 1.8)          # image 0 pleine : les quatre cases sont déjà là
            if u <= 0: continue
            on = prog(t, t0 - 0.12, 0.3, entreeSortie)            # puis chacune s'allume à son mot
            ccx, ccy = x + CW / 2, y + CH / 2
            trait(c, X, Y, mix(X, ccx, u), mix(Y, ccy, u), ROUGE if alerte else GRIS, 4, 1, [10, 12])
            c.save(); c.translate(mix(X, ccx, u) - ccx, mix(Y, ccy, u) - ccy)
            acc = ROUGE if alerte else (ENCRE if on > 0.5 else None)
            s_ = mix(0.3, 1, u) * mix(0.9, 1.0, on) * (1 + 0.06 * math.sin(math.pi * on))
            if vit: media(c, t, nom, x, y, CW, CH, borne(u * 3) * mix(0.55, 1, on), s_, video_t0=0, vitesse=vit, r=30, pad=10, accent=acc)
            else: media(c, t, nom, x, y, CW, CH, borne(u * 3) * mix(0.55, 1, on), s_, zoom=1.0, fy=0.45, r=30, pad=10, accent=acc)
            pilule(c, lab, ccx, y + CH - 40, entre(t, t0, 0.4, 2.2), ic, ENCRE, BLANC, 26)
            c.restore()
            if alerte:
                a = entre(t, TW(18) + 0.06 * k, 0.35, 2.4)
                if a > 0:
                    disque(c, x + CW - 22, y + 22, 34 * a, ROUGE, 1, (6, 16, 0.25))
                    icone(c, "triangle-alert", x + CW - 22, y + 20, 36 * a, BLANC, 2.6)
        # VOUS au milieu
        r = 92 * (1 + 0.04 * math.sin(t * 7))
        onde(c, X, Y, t, 0.0 if t < 2 else 2.0 * int(t / 2.0), 90, 200, ROUGE if alerte else ENCRE, 5, 0.9)
        disque(c, X, Y, r, ROUGE if alerte else ENCRE, 1, (14, 34, 0.3))
        icone(c, "user", X, Y - 22, 54, BLANC, 2.8)
        texte_centre(c, "VOUS", X, Y + 38, 34, BLANC, "noir")


# ─────────────────────────────────────────── 2 · qui fait grandir votre marque ?
def marque(c, t):
    g = Groupe(c, t, T_QUI - 0.1, T_JOUR, ent="bas", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "QUI FAIT GRANDIR", T_QUI, T_JOUR - 0.1, y=340)
        titre(c, t, "VOTRE MARQUE ?", TW(25), T_JOUR - 0.1, y=455, couleur=ROUGE)
        a = entre(t, T_QUI, 0.5, 1.4)
        hb = [0.12 + 0.03 * math.sin(t * 5 + k) for k in range(4)]        # tout reste à plat
        graphique(c, t, 540, 940, hb, None, False, borne(a * 3), mix(0.6, 1, a), "VOTRE MARQUE")
        q = entre(t, TW(24) - 0.05, 0.4, 2.6)
        if q > 0:
            sh = secousse(t, TW(28), 14, 0.35)
            c.save(); c.translate(760 + sh[0], 820 + sh[1]); c.scale(q, q)
            disque(c, 0, 0, 96, ROUGE, 1, (12, 30, 0.3)); texte_centre(c, "?", 0, 4, 130, BLANC, "noir")
            c.restore()


# ─────────────────────────────────────────── 3 · vos journées : problèmes, fournisseurs, erreurs
DW, DH, DG = 316, 562, 12


def chat(c, t, x, y, w, h, t0):
    """la conversation fournisseur qui ne répond pas"""
    rrect(c, x, y, w, h, 22, "#EFEDEA")
    rrect(c, x, y, w, 70, 22, ENCRE)
    disque(c, x + 40, y + 35, 20, "#3A3A3A"); icone(c, "factory", x + 40, y + 35, 22, BLANC, 2.2)
    texte(c, "Fournisseur", x + 70, y + 35 - hauteurLigne(24, "gras") / 2, 24, BLANC, "gras", track=-0.01)
    msgs = ["Des nouvelles ?", "Le tissu ?", "Allô ?", "??"]
    for k, m in enumerate(msgs):
        a = entre(t, t0 + 0.22 * k, 0.35, 2.2)
        if a <= 0: continue
        tw = largeur(m, 24, "gras", -0.01); bw = tw + 36
        bx, by = x + w - 16 - bw, y + 100 + k * 74
        c.save(); c.translate(bx + bw, by + 26); c.scale(a, a); c.translate(-(bx + bw), -(by + 26))
        rrect(c, bx, by, bw, 52, 20, ENCRE)
        texte(c, m, bx + 18, by + 26 - hauteurLigne(24, "gras") / 2, 24, BLANC, "gras", track=-0.01)
        c.restore()
    if t > t0 + 0.9:
        texte(c, "Vu ✓✓", x + w - 110, y + 100 + 4 * 74, 22, GRIS, "gras", alpha=entre(t, t0 + 0.9, 0.3, 1.5))
    a = entre(t, t0 + 1.0, 0.35, 2.2)
    if a > 0:
        rrect(c, x + 16, y + h - 80, 150 * a, 52, 20, BLANC)
        for k in range(3):
            disque(c, x + 50 + k * 30, y + h - 54, 7, GRIS, 0.4 + 0.6 * abs(math.sin(t * 6 + k)))


def journees(c, t):
    g = Groupe(c, t, T_JOUR - 0.1, T_HEURE, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VOS JOURNÉES", T_JOUR, T_ERR - 0.1)
        titre(c, t, "DES ERREURS ÉVITABLES", T_ERR - 0.05, T_HEURE - 0.1, couleur=ROUGE, taille=80)
        x0 = (1080 - 3 * DW - 2 * DG) / 2
        cartes = [("Technique", "wrench", TW(36)), ("Fournisseurs", "phone", TW(39)), ("Erreurs", "x", TW(47))]
        for k, (lab, ic, t0) in enumerate(cartes):
            u = entre(t, T_JOUR + 0.08 * k, 0.45, 1.6)
            if u <= 0: continue
            x, y = x0 + k * (DW + DG), 590
            on = t0 - 0.12 <= t < (cartes[k + 1][2] - 0.12 if k < 2 else 99)
            s = mix(1.0, 1.04, prog(t, t0 - 0.12, 0.3, entreeSortie)) if on else 1.0
            c.save(); c.translate((1 - u) * 500, 80 * (1 - u))
            cxk, cyk = x + DW / 2, y + DH / 2
            c.save(); c.translate(cxk, cyk); c.scale(s, s); c.translate(-cxk, -cyk)
            if k == 0:
                media(c, t, "rushes/couture", x, y, DW, DH, borne(u * 3), 1.0, video_t0=T_JOUR, vitesse=1.3, r=30, pad=10,
                      accent=ROUGE if on else None)
            elif k == 1:
                with Calque(c, borne(u * 3)):
                    cadre(c, x, y, DW, DH, 30, accent=ROUGE if on else None)
                    chat(c, t, x + 10, y + 10, DW - 20, DH - 20, t0 - 0.1)
            else:
                media(c, t, "trench-court", x, y, DW, DH, borne(u * 3), 1.0, zoom=1.05, fy=0.5, r=30, pad=10,
                      accent=ROUGE if on else None)
            c.restore(); c.restore()
            pilule(c, lab, x + DW / 2, y + DH + 50, entre(t, t0 - 0.1, 0.4, 2.2), ic, ROUGE if t > t0 else ENCRE, BLANC, 28)
            croix(c, x + DW - 36, y + 36, 28, entre(t, t0 + 0.3, 0.35, 2.4))
        tampon(c, "À REFAIRE", x0 + 2 * (DW + DG) + DW / 2, 900, t, TW(50), 40, ROUGE, -10)


# ─────────────────────────────────────────── 4 · chaque heure vous éloigne de votre priorité → vendre, fidéliser, développer
def horloge(c, cx, cy, r, ang, a):
    if a <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(a, a)
    disque(c, 0, 0, r, BLANC, 1, (16, 40, 0.18)); anneau(c, 0, 0, r - 4, ENCRE, 8)
    for k in range(12):
        an = k * math.pi / 6
        trait(c, (r - 26) * math.sin(an), -(r - 26) * math.cos(an), (r - 14) * math.sin(an), -(r - 14) * math.cos(an), ENCRE, 6)
    trait(c, 0, 0, r * 0.45 * math.sin(ang / 12), -r * 0.45 * math.cos(ang / 12), ENCRE, 12)
    trait(c, 0, 0, r * 0.72 * math.sin(ang), -r * 0.72 * math.cos(ang), ROUGE, 7)
    disque(c, 0, 0, 14, ENCRE)
    c.restore()


def priorite(c, t):
    g = Groupe(c, t, T_HEURE - 0.1, T_SOY, ent="bas", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "CHAQUE HEURE", T_HEURE, T_PRIO - 0.1)
        titre(c, t, "VOTRE PRIORITÉ", T_PRIO - 0.05, T_SOY - 0.1, taille=90)
        sw = prog(t, TW(65) - 0.1, 0.45, entreeSortie)        # « priorité : » → le graphique prend la place
        if sw < 1:
            with Calque(c, 1 - sw):
                a = entre(t, T_HEURE, 0.5, 1.6)
                ang = 2 * math.pi * 1.6 * max(0, t - T_HEURE)
                horloge(c, 540, 760, 190, ang, a)
                # VOUS s'éloigne de la cible
                d = prog(t, TW(60) - 0.1, 1.0, entreeSortie)
                vx = mix(660, 200, d)
                b = entre(t, T_HEURE + 0.2, 0.45, 1.8)
                if b > 0:
                    trait(c, vx + 70, 1180, 810, 1180, ROUGE if d > 0.1 else GRIS, 5, borne(b * 3), [12, 12])
                    for k, (rr, col) in enumerate([(92, ROUGE), (64, BLANC), (38, ROUGE), (14, BLANC)]):
                        disque(c, 880, 1180, rr * b, col, 1, (10, 26, 0.2) if k == 0 else None)
                    pilule(c, "Priorité", 880, 1310, b, "target", ENCRE, BLANC, 28)
                    disque(c, vx, 1180, 70 * b, ENCRE, 1, (10, 26, 0.25))
                    texte_centre(c, "VOUS", vx, 1180, 30, BLANC, "noir", borne(b * 3))
                    if d > 0.2:
                        pilule(c, "Vous éloigne", (vx + 810) / 2 + 40, 1090, entre(t, TW(61), 0.4, 2.2), "arrow-right", ROUGE, BLANC, 26)
        if sw > 0:
            hb = [mix(0.15, h1, prog(t, t0 - 0.1, 0.6, entreeSortie)) for h1, t0 in
                  [(0.42, T_VENDRE), (0.55, T_FIDEL), (0.95, T_DEVEL), (0.35, T_DEVEL + 0.15)]]
            gx0, gy0, base = graphique(c, t, 540, 930, hb, 2, t > T_DEVEL + 0.2, sw, mix(0.7, 1, sw))
            for k, (lab, ic, t0, x, y) in enumerate([("Vendre", "euro", T_VENDRE, 280, 1340), ("Fidéliser", "heart", T_FIDEL, 540, 1340),
                                                      ("Développer", "trending-up", T_DEVEL, 800, 1340)]):
                pilule(c, lab, x, y, entre(t, t0 - 0.05, 0.4, 2.2), ic, ENCRE, BLANC, 28)
            bx = gx0 + 90 + 2 * 180 + 60
            pilule(c, "Best-seller", bx, base - 330 * 0.95 - 50, entre(t, T_DEVEL + 0.3, 0.4, 2.4), "flame", BEIGE, BLANC, 26)


# ─────────────────────────────────────────── 5 · soyons clairs : idée + usine ≠ produit
def soyons(c, t):
    if t < T_SOY - 0.15 or t > T_DEVP + 0.3: return
    r = disque_noir(c, t, T_SOY - 0.12, T_DEVP - 0.12)
    a = entre(t, T_SOY - 0.02, 0.4, 2.0) * (1 - prog(t, T_DEVP - 0.14, 0.14))
    if a > 0:
        lettres(c, "SOYONS", 540, 820, 150, t, T_SOY - 0.02, "ressort", fam="archivo", grad=False, couleur=BLANC, decal=0.03, alpha=borne(a * 3))
        lettres(c, "CLAIRS.", 540, 990, 150, t, TW(73) - 0.05, "ressort", fam="archivo", grad=False, couleur=BEIGE, decal=0.03, alpha=borne(a * 3))
    return r


def simple(c, t):
    g = Groupe(c, t, T_DEVP - 0.1, T_MAIT, ent="grand", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "UN PRODUIT TEXTILE", T_DEVP - 0.1, T_PAS - 0.1, taille=88)
        titre(c, t, "PAS SI SIMPLE", T_PAS - 0.05, T_MAIT - 0.1, couleur=ROUGE)
        sw = prog(t, T_PAS + 0.1, 0.45, entreeSortie)
        if sw < 1:
            a = entre(t, T_DEVP - 0.15, 0.5, 1.4)
            media(c, t, "produits/veste-zip-marine", 240 - 300 * sw, 580, 600, 760, borne(a * 3) * (1 - sw), mix(0.7, 1, a) * mix(1, 0.6, sw),
                  zoom=1.0, accent=ENCRE)
            pilule(c, "Votre produit", 540, 1350, entre(t, TW(76), 0.4, 2.2) * (1 - sw), "shirt", ENCRE, BLANC, 30)
        for k, (nom, vit, lab, ic, t0) in enumerate([("ensemble-sweat-jupe", None, "Une bonne idée", "lightbulb", T_IDEE - 0.25),
                                                       ("rushes/machines", 1.2, "Une usine", "factory", T_USINE - 0.1)]):
            u = entre(t, t0, 0.45, 1.6)
            if u <= 0: continue
            x = 70 + k * 520
            if vit: media(c, t, nom, x, 620, 420, 640, borne(u * 3), mix(0.6, 1, u), video_t0=t0, vitesse=vit, rot=mix(8, 0, u))
            else: media(c, t, nom, x, 620, 420, 640, borne(u * 3), mix(0.6, 1, u), zoom=1.0, fy=0.4, rot=mix(-8, 0, u))
            pilule(c, lab, x + 210, 1310, entre(t, t0 + 0.15, 0.4, 2.2), ic, ENCRE, BLANC, 28)
        signe(c, "+", 540, 940, entre(t, T_USINE - 0.15, 0.35, 2.6), ENCRE, 60, t, T_USINE)
        tampon(c, "PAS SUFFISANT", 540, 760, t, TW(89) + 0.25, 46, ROUGE, -8)


# ─────────────────────────────────────────── 6 · maîtriser les matières, les coûts, la qualité, la production
def costing(c, t, x, y, w, h, t0):
    texte(c, "COSTING", x + 30, y + 34, 34, ENCRE, "archivo", track=0.02)
    disque(c, x + w - 54, y + 56, 30, ENCRE); icone(c, "euro", x + w - 54, y + 56, 32, BLANC, 2.6)
    for k, (lab, v) in enumerate([("Tissu", 0.72), ("Façon", 0.5), ("Accessoires", 0.28), ("Transport", 0.44)]):
        yy = y + 130 + k * 58
        texte(c, lab, x + 30, yy, 24, ENCRE, "gras", track=-0.01)
        rrect(c, x + 30, yy + 34, w - 60, 10, 5, "#E8E5E0")
        rrect(c, x + 30, yy + 34, (w - 60) * v * prog(t, t0 + 0.08 * k, 0.5, sortie), 10, 5, ENCRE)


def maitriser(c, t):
    g = Groupe(c, t, T_MAIT - 0.1, T_SURT, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "MAÎTRISER", T_MAIT, T_SURT - 0.1)
        tuiles = [("Matières", "layers", "rushes/nuancier", 1.0, T_MAT), ("Coûts", "euro", None, None, T_COUT),
                  ("Qualité", "shield-check", "rushes/controle", 1.15, T_QUAL), ("Production", "factory", "rushes/machines", 1.2, T_PROD)]
        for k, (lab, ic, nom, vit, t0) in enumerate(tuiles):
            u = entre(t, t0 - 0.2, 0.42, 1.8)
            if u <= 0: continue
            x, y = 85 + (k % 2) * 465, 570 + (k // 2) * 410
            w, h = 445, 390
            c.save(); c.translate(x + w / 2, y + h / 2); c.scale(mix(0.4, 1, u), mix(0.4, 1, u)); c.translate(-(x + w / 2), -(y + h / 2))
            if nom: media(c, t, nom, x, y, w, h, borne(u * 3), 1.0, video_t0=t0 - 0.2, vitesse=vit, r=30, pad=10)
            else:
                with Calque(c, borne(u * 3)):
                    cadre(c, x, y, w, h, 30); costing(c, t, x, y, w, h, t0)
            c.restore()
            pilule(c, lab, x + w / 2, y + h - 44, entre(t, t0, 0.4, 2.2), ic, ENCRE, BLANC, 26)
            coche(c, x + w - 34, y + 34, 26, entre(t, t0 + 0.3, 0.35, 2.4))


# ─────────────────────────────────────────── 7 · les bonnes décisions avant qu'elles ne coûtent cher (courbe)
ETAPES = [("Idée", "lightbulb"), ("Développement", "scissors"), ("Production", "factory"), ("Livraison", "truck")]


def decisions(c, t):
    g = Groupe(c, t, T_SURT - 0.1, T_LA, ent="bas", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ET SURTOUT", T_SURT, T_BONNES - 0.1)
        titre(c, t, "LES BONNES DÉCISIONS", T_BONNES - 0.05, T_LA - 0.1, taille=82)
        a = entre(t, T_SURT, 0.5, 1.4)
        c.save(); c.translate(540, 960); c.scale(mix(0.6, 1, a), mix(0.6, 1, a)); c.translate(-540, -960)
        with Calque(c, borne(a * 3)):
            cadre(c, 80, 580, 920, 780, 44)
            texte(c, "LE PRIX D'UNE ERREUR", 140, 630, 32, ENCRE, "noir", track=0.06)
            ax0, ax1, ay = 190, 900, 1180
            trait(c, ax0, ay, ax1, ay, "#DCD8D2", 6)
            for k, (lab, ic) in enumerate(ETAPES):
                x = ax0 + k * (ax1 - ax0) / 3
                disque(c, x, ay, 16, ENCRE)
                texte_centre(c, lab, x, ay + 60, 24, ENCRE, "gras", 1.0, -0.01)
                icone(c, ic, x, ay + 108, 34, GRIS, 2.2)
            # la courbe : plate au début, qui s'envole à la fin
            u = prog(t, T_SURT + 0.2, T_CHER - T_SURT, lin)
            if u > 0:
                pts = []
                for i in range(int(90 * u) + 1):
                    v = i / 90
                    pts.append((ax0 + v * (ax1 - ax0), ay - 30 - 470 * v ** 3.2))
                tard = [p for p in pts if p[0] > 560]
                if len(tard) > 1:
                    pa = skia.Path(); pa.moveTo(tard[0][0], ay)
                    for p in tard: pa.lineTo(*p)
                    pa.lineTo(tard[-1][0], ay); pa.close()
                    c.drawPath(pa, peinture(ROUGE, 0.12))
                path = skia.Path(); path.moveTo(*pts[0])
                for p in pts[1:]: path.lineTo(*p)
                pe = peinture(ENCRE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=9); pe.setStrokeCap(skia.Paint.kRound_Cap)
                c.drawPath(path, pe)
                tx, ty = pts[-1]
                disque(c, tx, ty, 16, ROUGE if tx > 560 else ENCRE)
            # décider ici
            xd = ax0 + (ax1 - ax0) / 3
            b = entre(t, T_AVANT - 0.05, 0.42, 2.0)
            if b > 0:
                onde(c, xd, ay - 34, t, T_AVANT, 20, 120, VERT, 5, 0.7)
                epingle(c, xd, ay - 34, "Décider ici", b, VERT, None, 130, 28)
            for k, (ex, ey) in enumerate([(700, 900), (790, 820), (870, 720)]):
                e = entre(t, T_CHER - 0.05 + 0.1 * k, 0.35, 2.6)
                if e > 0:
                    disque(c, ex, ey, 34 * e, ROUGE, 1, (6, 16, 0.25)); icone(c, "euro", ex, ey, 36 * e, BLANC, 2.6)
            pilule(c, "Trop tard = cher", 690, 1040, entre(t, TW(113), 0.4, 2.2), "triangle-alert", ROUGE, BLANC, 28, 3)
        c.restore()


# ─────────────────────────────────────────── 8 · « exactement là » → MONARQUE : disque noir, logo qui se pose en tête
T_DQ = T_ACC - 0.3
LOGO_Y, LOGO_W = 250, 340


def la(c, t):
    if t < T_LA - 0.1 or t > T_MQ + 0.2: return
    titre(c, t, "C'EST LÀ", T_LA, T_MQ + 0.2, y=900, taille=150)
    a = entre(t, TW(116) - 0.05, 0.4, 2.0)
    if a > 0:
        c.save(); c.translate(540, 1150); c.scale(a, a)
        for rr, col in [(110, ENCRE), (76, BLANC), (44, ENCRE), (14, BLANC)]: disque(c, 0, 0, rr, col)
        c.restore()


def monarque_logo(c, t):
    if t < T_MQ - 0.15 or t > T_ROLE + 0.4: return
    r = disque_noir(c, t, T_MQ - 0.12, T_DQ)
    u = prog(t, T_MQ + 0.05, 0.36, lambda v: rebond(v, 1.6))
    v = prog(t, T_DQ, 0.42, entreeSortie)
    o = prog(t, T_ROLE - 0.15, 0.3, entree)
    if t >= T_MQ + 0.03:
        lw = mix(1.5, 1, u) * mix(860, LOGO_W, v)
        ly = mix(960, LOGO_Y, v)
        if v < 1: logo(c, 540, ly, lw, True, borne(u * 3) * (1 - v))
        if v > 0: logo(c, 540, ly - 300 * o, lw, False, v * (1 - o))
    return r


# ─────────────────────────────────────────── 9 · du développement à la production, les bonnes compétences
PISTE = [("Développement", T_DEVPROD), ("Prototype", T_JUSQ), ("Contrôle", TW(129)), ("Production", T_PRODF)]


def accompagne(c, t):
    g = Groupe(c, t, T_ACC - 0.25, T_PRES, ent="bas", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ON VOUS ACCOMPAGNE", T_ACC, T_COMP - 0.1, y=430, taille=80)
        titre(c, t, "LES BONNES COMPÉTENCES", T_COMP - 0.05, T_PRES - 0.1, y=430, taille=78)
        a = entre(t, T_ACC - 0.1, 0.5, 1.4)
        # la case : fiche technique, puis l'atelier, puis la production
        sw = prog(t, T_COMP - 0.15, 0.4, entreeSortie)
        etape = "eln-078-tailleur-prune" if t < T_JUSQ else ("rushes/couture" if t < T_PRODF - 0.1 else "rushes/machines")
        y = mix(560, 540, sw)
        if etape.startswith("rushes"):
            media(c, t, etape, 120, y, 840, 520, borne(a * 3), mix(0.6, 1, a), video_t0=T_JUSQ, vitesse=1.2, accent=ENCRE)
        else:
            media(c, t, etape, 120, y, 840, 520, borne(a * 3), mix(0.6, 1, a), zoom=1.0, fy=0.5, accent=ENCRE)
        # la piste développement → production
        if sw < 1:
            with Calque(c, borne(a * 3) * (1 - sw)):
                x0, x1, py = 180, 900, 1200
                trait(c, x0, py, x1, py, "#DCD8D2", 8)
                p = prog(t, T_DEVPROD - 0.1, T_PRODF - T_DEVPROD + 0.1, entreeSortie)
                trait(c, x0, py, mix(x0, x1, p), py, ENCRE, 8)
                for k, (lab, t0) in enumerate(PISTE):
                    x = x0 + k * (x1 - x0) / 3
                    on = t > t0 - 0.1
                    disque(c, x, py, 22 if on else 16, ENCRE if on else "#DCD8D2")
                    if on: icone(c, "check", x, py, 24, BLANC, 3)
                    texte_centre(c, lab, x, py + 64, 26, ENCRE if on else GRIS, "gras", 1.0, -0.01)
                disque(c, mix(x0, x1, p), py, 30, BEIGE, 1, (8, 20, 0.3))
        # les compétences
        for k, (lab, ic, x, yy) in enumerate([("Stylistes", "paintbrush", 300, 1170), ("Modélistes", "scissors", 780, 1170),
                                               ("Façonniers", "hammer", 300, 1290), ("Contrôleurs", "shield-check", 780, 1290)]):
            pilule(c, lab, x, yy, entre(t, T_COMP + 0.1 + 0.13 * k, 0.4, 2.2), ic, ENCRE, BLANC, 30, (-2, 2, 2, -2)[k])


# ─────────────────────────────────────────── 10 · au cœur de l'écosystème textile chinois : le globe en points, Chine allumée
def globe(c, t):
    g = Groupe(c, t, T_PRES - 0.15, T_ROLE, ent="zoom", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "AU CŒUR DE LA CHINE", T_PRES + 0.1, T_ROLE - 0.1, taille=88)
        a = entre(t, T_PRES - 0.1, 0.6, 1.3)
        rot = prog(t, T_PRES, T_COEUR - T_PRES + 0.2, entreeSortie)
        lon0 = mix(30, 106, rot) + 2.0 * (t - T_PRES); lat0 = mix(40, 28, rot)
        R = 380 * mix(0.7, 1, a)
        cx, cy = 540, 960
        lum = prog(t, T_COEUR - 0.1, 0.6, sortie)
        with Calque(c, borne(a * 3)):
            ombre_sol(c, cx, cy + R * 1.06, R * 0.78, R * 0.09, 0.14)
            if lum > 0:
                p = skia.Paint(AntiAlias=True)
                kx, ky, kz = G.pos(*CANTON, lon0, lat0, R, cx, cy)
                p.setShader(skia.GradientShader.MakeRadial(skia.Point(kx, ky), R * 0.9, [hexa(BEIGE, 0.35 * lum), hexa(BEIGE, 0.0)]))
                c.drawCircle(kx, ky, R * 0.9, p)
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx - R * 0.3, cy - R * 0.35), R * 1.5, [hexa("#FFFFFF"), hexa("#ECEAE6")], [0.0, 1.0]))
            c.drawCircle(cx, cy, R, p); anneau(c, cx, cy, R, "#DAD6D0", 3)
            G.terres(c, cx, cy, R, lon0, lat0, couleurs={0: TERRE, 1: melange(TERRE, ENCRE, lum), 2: TERRE, 3: ENCRE, 4: TERRE},
                     grossir={1: mix(1.0, 1.35, lum), 2: 0.6, 3: 1.0})
            u = prog(t, T_PRES + 0.1, T_COEUR - T_PRES + 0.2, entreeSortie)
            G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, 1.0, "#D5D1CB", 5, 0.3, [2, 16])
            hx, hy, hz = G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, u, ENCRE, 7, 0.3)
            if 0 < u < 1:
                disque(c, hx, hy, 24, ENCRE, 1, (6, 16, 0.25)); icone(c, "plane", hx, hy, 28, BLANC, 2.4)
            G.repere(c, *PARIS, cx, cy, R, lon0, lat0, "France", ENCRE, "FR", entre(t, T_PRES + 0.05, 0.42, 2.0), 1.0, 70)
            kx, ky, kz = G.pos(*CANTON, lon0, lat0, R, cx, cy)
            if kz > 0.05 and t > T_COEUR - 0.2:
                onde(c, kx, ky, t, T_COEUR, 20, 190, ENCRE, 6, 0.7)
                onde(c, kx, ky, t, T_CHN - 0.1, 20, 190, ENCRE, 6, 0.7)
            G.repere(c, *CANTON, cx, cy, R, lon0, lat0, "Monarque · Chine", ENCRE, "CN", entre(t, T_COEUR + 0.05, 0.42, 2.0), 1.0, 70)


# ─────────────────────────────────────────── 11 · votre rôle / le nôtre
def roles(c, t):
    g = Groupe(c, t, T_ROLE - 0.15, T_FIN, ent="bas", sor="recul", cy=960)
    if not g.visible: return
    with g:
        for k, (nom, vid, lab1, lab2, t0, t2) in enumerate([("shop", None, "VOTRE RÔLE", "Faire grandir votre marque", T_ROLE, TW(149)),
                                                            ("rushes/atelier", 1.1, "LE NÔTRE", "Développer vos produits", T_NOTRE, T_NOTRE + 0.9)]):
            u = entre(t, t0 - 0.05, 0.5, 1.5)
            if u <= 0: continue
            y = 330 + k * 460
            c.save(); c.translate((1 - u) * (-700 if k == 0 else 700), 0)
            if vid: media(c, t, nom, 90, y, 900, 430, borne(u * 3), 1.0, video_t0=t0, vitesse=vid, voile=("#000000", 0.4))
            else: media(c, t, nom, 90, y, 900, 430, borne(u * 3), 1.0, zoom=1.0, fy=0.45, voile=("#000000", 0.4))
            if k == 1: logo(c, 840, y + 70, 200, True, borne(u * 3))
            texte(c, lab1, 150, y + 220, ajuste(lab1, 780, 84, "archivo"), BLANC, "archivo", track=-0.01)
            b = entre(t, t2, 0.4, 1.6)
            if b > 0: texte(c, lab2, 152, y + 320 + 20 * (1 - b), 42, BLANC, "gras", track=-0.01, alpha=borne(b * 3))
            c.restore()
        if t > TW(150): coche(c, 930, 390, 34, entre(t, TW(150), 0.35, 2.4))
        for k, (lab, ic, t0, x) in enumerate([("Méthode", "list-filter", T_METH, 240), ("Maîtrise", "target", T_MAIT2, 520),
                                              ("Compétitivité", "trending-up", T_COMPET, 820)]):
            pilule(c, lab, x, 1290, entre(t, t0 - 0.05, 0.4, 2.2), ic, BEIGE if k == 2 else ENCRE, BLANC, 28, (-3, 2, -2)[k])


# ─────────────────────────────────────────── 12 · fin : la signature du client
def fin(c, t):
    if t < T_FIN - 0.1: return
    u = entre(t, T_FIN - 0.05, 0.55, 1.4)
    logo(c, 540, 700, 820 * mix(0.7, 1, u), False, borne(u * 3))
    a = entre(t, T_VDEV - 0.05, 0.45, 1.6)
    if a > 0:
        texte_centre(c, "Vous développez votre marque.", 540, 900 + 30 * (1 - a), 46, GRIS, "gras", borne(a * 3), -0.01)
    b = entre(t, T_NOUS - 0.05, 0.45, 1.6)
    if b > 0:
        texte_centre(c, "Nous vous aidons à concrétiser", 540, 990 + 30 * (1 - b), 46, ENCRE, "noir", borne(b * 3), -0.01)
        texte_centre(c, "vos produits.", 540, 1052 + 30 * (1 - b), 46, ENCRE, "noir", borne(b * 3), -0.01)
    d = entre(t, T_URL - 0.15, 0.45, 2.0)
    if d > 0:
        clic = prog(t, T_URL + 0.45, 0.12) * (1 - prog(t, T_URL + 0.6, 0.15))
        s = mix(0.4, 1, d) * (1 - 0.06 * clic)
        c.save(); c.translate(540, 1230); c.scale(s, s)
        tw = largeur("monarqueprod.com", 50, "noir", -0.01); w, h = tw + 190, 116
        rrect(c, -w / 2, -h / 2, w, h, h / 2, ENCRE, borne(d * 3), (16, 40, 0.3))
        icone(c, "arrow-right", w / 2 - 66, 0, 46, BLANC, 3.0, borne(d * 3))
        texte(c, "monarqueprod.com", -w / 2 + 56, -hauteurLigne(50) / 2, 50, BLANC, "noir", track=-0.01, alpha=borne(d * 3))
        c.restore()
        pc = prog(t, T_URL + 0.05, 0.4, sortie)
        curseur(c, mix(980, 700, pc), mix(1600, 1250, pc), 1.3, 1 - prog(t, T_URL + 0.9, 0.3), clic)
        eclats(c, 540, 1230, t, T_URL + 0.5, 12, 300, [BEIGE, BEIGE2, ENCRE], graine=4)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9)
for (_, _, _, _, x, y, t0) in COINS: son(t0 - 0.12, "whoosh_court", -10); son(t0, "pop", -10)
son(TW(18), "croc", -7); son(TW(18) + 0.05, "impact", -5)
for k in range(4): son(TW(18) + 0.06 * k, "blip", -13)
son(T_QUI - 0.1, "whoosh_bas", -7); son(TW(24) - 0.05, "pop", -8); son(TW(28), "croc", -8)
son(T_JOUR - 0.1, "whoosh", -8); son(TW(36) - 0.1, "pop", -10); son(TW(36) + 0.3, "croc", -10)
for k in range(4): son(TW(39) - 0.1 + 0.22 * k, "blip", -12)
son(TW(47) - 0.1, "pop", -10); son(TW(47) + 0.3, "croc", -9); son(TW(50), "tampon", -5); son(T_ERR - 0.05, "impact_doux", -7)
son(T_HEURE - 0.1, "whoosh_bas", -8)
for k in range(6): son(T_HEURE + 0.3 + 0.32 * k, "clic", -14)
son(TW(60) - 0.1, "swipe", -10); son(TW(61), "pop", -10)
son(TW(65) - 0.1, "whoosh", -8)
for t0 in (T_VENDRE, T_FIDEL, T_DEVEL): son(t0 - 0.05, "pop", -10)
son(T_DEVEL + 0.3, "ching", -8)
son(T_SOY - 0.12, "whoosh_long", -7); son(T_SOY, "impact", -3); son(TW(73) - 0.05, "impact", -5)
son(T_DEVP - 0.12, "whoosh_bas", -8); son(TW(76), "pop", -10); son(T_PAS + 0.1, "whoosh", -9)
son(T_IDEE - 0.25, "pop", -10); son(T_USINE - 0.1, "pop", -10); son(T_USINE - 0.15, "croc", -10); son(TW(89) + 0.25, "tampon", -5)
son(T_MAIT - 0.1, "whoosh_court", -8)
for t0 in (T_MAT, T_COUT, T_QUAL, T_PROD): son(t0 - 0.2, "whoosh_court", -11); son(t0 + 0.3, "check", -11)
son(T_SURT - 0.1, "whoosh_bas", -8); son(T_AVANT - 0.05, "check", -8); son(T_AVANT, "ching", -10)
son(T_CHER - 0.3, "montee", -11)
for k in range(3): son(T_CHER - 0.05 + 0.1 * k, "croc", -9)
son(T_LA - 0.1, "whoosh", -8); son(TW(116) - 0.05, "impact_doux", -6)
son(T_MQ - 0.12, "whoosh_long", -7); son(T_MQ + 0.05, "impact", -4); son(T_MQ + 0.08, "ching", -9)
son(T_DQ, "whoosh_bas", -8)
for lab, t0 in PISTE: son(t0 - 0.1, "check", -12)
son(T_JUSQ, "swipe", -12); son(T_PRODF - 0.1, "swipe", -12)
for k in range(4): son(T_COMP + 0.1 + 0.13 * k, "pop", -10)
son(T_PRES - 0.15, "whoosh_long", -8); son(T_COEUR - 0.1, "impact_doux", -6); son(T_COEUR, "ching", -9)
son(T_CHN - 0.1, "check", -10)
son(T_ROLE - 0.15, "whoosh", -8); son(TW(150), "check", -9); son(T_NOTRE - 0.1, "whoosh", -8)
for t0 in (T_METH, T_MAIT2, T_COMPET): son(t0 - 0.05, "pop", -9)
son(T_COMPET + 0.1, "ching", -9)
son(T_FIN - 0.1, "montee", -11); son(T_FIN + 0.05, "impact", -5); son(T_NOUS, "pop", -10)
son(T_URL - 0.15, "pop", -9); son(T_URL + 0.45, "clic", -5); son(T_URL + 0.5, "ching", -8)

for a, b in [(T_QUI - 0.1, T_QUI + 0.3), (T_JOUR - 0.15, T_JOUR + 0.3), (T_HEURE - 0.15, T_HEURE + 0.3), (TW(65) - 0.1, TW(65) + 0.3),
             (T_SOY - 0.1, T_SOY + 0.3), (T_DEVP - 0.15, T_DEVP + 0.15), (T_MAIT - 0.15, T_MAIT + 0.3), (T_SURT - 0.15, T_SURT + 0.3),
             (T_LA - 0.1, T_LA + 0.3), (T_MQ - 0.1, T_MQ + 0.3), (T_PRES - 0.2, T_PRES + 0.3), (T_ROLE - 0.2, T_ROLE + 0.3),
             (T_FIN - 0.1, T_FIN + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(18), ROUGE, 0.08), (T_SOY, "#FFFFFF", 0.08), (T_MQ + 0.05, "#FFFFFF", 0.1), (T_COEUR, BEIGE, 0.08),
                    (T_DEVEL + 0.3, BEIGE, 0.07)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_clair(c, t)
    hook(c, t); marque(c, t); journees(c, t); priorite(c, t)
    simple(c, t)
    r1 = soyons(c, t)                      # le disque noir se retire et découvre la scène suivante
    maitriser(c, t); decisions(c, t); la(c, t)
    accompagne(c, t); globe(c, t); roles(c, t)
    r2 = monarque_logo(c, t)
    fin(c, t)
    K.dessine_eclairs(c, t)
    cache = (T_SOY - 0.1 < t < T_DEVP - 0.05) or (T_MQ - 0.1 < t < T_ACC - 0.05) or t > T_FIN - 0.1
    if not cache:
        SOUS.dessine(c, t, BLANC if max(r1 or 0, r2 or 0) > 1200 else ENCRE)
