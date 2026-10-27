"""MQ-M08 « Regardez vos cartons. C'est là que dort votre argent. » — hook écrit par nous (20/10/2026).
Levier : perte (l'argent immobilisé dans le stock) + contraste rupture / invendus. Persona : fondateur d'une marque ou
d'une boutique qui achète sa collection des mois à l'avance et solde en fin de saison. Message de la plaquette Monarque :
passer d'une collection figée à une offre vivante (tester, mesurer, réassortir).
Charte MQ-M05 (fond clair, Archivo Black, cases blanches, Tomy, −13 LUFS, globe à points, graphique « vos ventes »)
+ cartes en vraie 3D (studio3d) + signature 3D MONARQUE (mq.signature_mq). Aucun chiffre. Zone sûre : x 130-860."""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import agence
from studio import lettres, Groupe, eclats, entre, SousTitresEncre, curseur, lueur_s
from studio3d import Cam, Plan, coins, scene3d, Balance
from monarque import *
from monarque import VERT, ROUGE
from mq import graphique, flash_noir, logo_monarque, signature_mq, sons_signature_mq, MODELES

polices(P)
K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 2.3, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = SousTitresEncre(K, y=1440, larg=640, taille=50, fam="gras", max_mots=5, cx=500)
CX = 510

# repères (mots)
T_CARTONS, T_LA, T_DORT, T_ARGENT = TW(2), TW(3), TW(6), TW(8)
T_VOUS, T_COMMANDE, T_COLL, T_MOIS, T_AVANCE, T_INTUIT = TW(9), TW(11), TW(14), TW(16), TW(18), TW(21)
T_LES, T_MARCHENT, T_RUPTURE, T_CELLES, T_PASM, T_ENTASSENT = TW(22), TW(25), TW(27), TW(28), TW(32), TW(34)
T_ET, T_SAISON, T_BRADEZ, T_PAYE, T_TARIF = TW(35), TW(39), TW(41), TW(46), TW(48)
T_CE, T_GOUT, T_CEST, T_METHODE = TW(49), TW(55), TW(56), TW(60)
T_GRANDES, T_DEVINENT, T_PAS = TW(61), TW(65), TW(66)
T_ELLES, T_TESTENT, T_SERIES, T_MESURENT, T_REASS, T_VEND = TW(67), TW(68), TW(71), TW(73), TW(76), TW(80)
T_EXACT, T_MQ, T_FAIRE = TW(81), TW(85), TW(89)
T_NOUS, T_DEV, T_PRODUITS, T_SUIVONS, T_PROD, T_CHINE, T_SOURC, T_CONTR, T_ORGA, T_REASS2, T_VENTES = \
    TW(90), TW(91), TW(93), TW(95), TW(97), TW(99), TW(101), TW(103), TW(106), TW(108), TW(112)
T_ARRET, T_PARIER, T_SAISON2, T_ENTIERE, T_INVEST, T_MARCHE = TW(113), TW(116), TW(119), TW(120), TW(122), TW(126)
T_FIN, T_L1, T_L2 = TW(127), TW(128), TW(132)
T_BOUTON = TW(133) + 0.7

MEDIAS = [("produits/veste-ceinturee-prune", False), ("rushes/machines", True), ("produits/blouson-cuir-noir", False),
          ("rushes/controle", True), ("produits/chemise-rayee-bordeaux", False), ("rushes/atelier", True)]


# ─────────────────────────────────────────── briques locales
def titre2(c, t, l1, l2, t0, t1, c2=ENCRE, t2=None):
    """deux lignes Archivo : la première encre, la seconde colorée, dans la zone sûre"""
    if l1: titre(c, t, l1, t0, t1, y=330, taille=84, larg=780)
    if l2: titre(c, t, l2, (t2 if t2 is not None else t0 + 0.12), t1, y=440, couleur=c2, taille=84, larg=780)


def carte_media(nom, vid, t0, label=None, ic=None, accent=None, voile=None, zoom=1.0, fy=0.5):
    """case blanche Monarque à plaquer sur un Plan 3D"""
    def f(c, w, h):
        t = agence.T_COURANT[0]
        cadre(c, 0, 0, w, h, w * 0.09, accent=accent)
        m = w * 0.04
        if vid: video(c, nom, m, m, int(w - 2 * m), int(h - 2 * m), t - t0, 1.0, rayon=w * 0.07)
        else: image_cover(c, nom, m, m, w - 2 * m, h - 2 * m, zoom, 0.5, fy, rayon=w * 0.07)
        if voile: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(m, m, w - 2 * m, h - 2 * m), w * 0.07, w * 0.07), peinture(voile[0], voile[1]))
        if label: pilule(c, label, w / 2, h - m - w * 0.12, 1.0, ic, accent or ENCRE, BLANC, max(20, w * 0.075))
    return f


def carton_mq(c, cx, cy, w, alpha=1.0, rot=0.0, etiquette=True):
    """carton kraft aux tons Monarque"""
    if alpha <= 0.01: return
    h = w * 0.72
    c.save(); c.translate(cx, cy); c.rotate(rot)
    with Calque(c, alpha):
        rrect(c, -w / 2, -h / 2, w, h, w * 0.05, "#D9C5A6", 1.0, (w * 0.08, w * 0.2, 0.2), "#B8A082", max(2, w * 0.016))
        rrect(c, -w * 0.06, -h / 2, w * 0.12, h, 0, "#E8DAC2")
        trait(c, -w / 2 + 6, -h / 2 + h * 0.22, w / 2 - 6, -h / 2 + h * 0.22, "#B8A082", max(2, w * 0.012), rond=False)
        if etiquette:
            rrect(c, w * 0.14, 0, w * 0.26, h * 0.3, w * 0.02, BLANC)
            icone(c, "shirt", w * 0.27, h * 0.15, w * 0.14, ENCRE, 2.2)
    c.restore()


def piece(c, cx, cy, r, a, t):
    """pièce d'euro qui dort"""
    if a <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(a, a); c.rotate(8 * math.sin(t * 1.5))
    disque(c, 0, 0, r, BEIGE, 1, (6, 16, 0.25)); anneau(c, 0, 0, r * 0.78, "#A98A5E", 3)
    icone(c, "euro", 0, 0, r * 1.1, ENCRE, 2.8)
    c.restore()


# ─────────────────────────────────────────── 1 · hook : vos cartons, c'est là que dort votre argent
PILE = [(-120, 1180, 300, -3), (160, 1150, 280, 2), (20, 960, 290, -1), (-170, 780, 240, 3), (130, 790, 230, -2)]


def scene_hook(c, t):
    t1 = T_VOUS - 0.12
    g = Groupe(c, t, -1, t1, ent="aucune", sor="zoom", d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        o = prog(t, -0.3, 1.2, douce)
        sx, sy = secousse(t, T_CARTONS, 12, 0.3)
        c.save(); c.translate(sx, sy)
        for k, (dx, y, w, rot) in enumerate(PILE):
            u = entre(t, -0.45 + 0.07 * k, 0.4, 1.7)
            if u <= 0: continue
            carton_mq(c, CX + dx + (1 - u) * 60 * (1 if k % 2 else -1), y - 260 * (1 - u), w, borne(u * 3), rot)
        # l'argent qui dort : pièces posées sur les cartons, « z z z »
        for k, (px, py, r) in enumerate(((CX - 30, 700, 46), (CX + 190, 690, 40), (CX - 200, 880, 38), (CX + 60, 1050, 44))):
            piece(c, px, py - 10 * math.sin(t * 2 + k), r, entre(t, T_DORT - 0.1 + 0.08 * k, 0.4, 2.2), t)
        z = entre(t, T_DORT, 0.4, 2.0)
        if z > 0:
            for k in range(3):
                ph = (t * 0.9 + k * 0.33) % 1
                texte(c, "z", CX + 250 + 40 * ph + 14 * k, 640 - 120 * ph - 30 * k, 40 + 14 * k, GRIS, "archivo", "centre", 0, z * (1 - ph))
        c.restore()
        if t > T_ARGENT - 0.1:
            lueur_s(c, CX, 950, 560, BEIGE, 0.12 * prog(t, T_ARGENT - 0.1, 0.4))
            pilule(c, "Votre argent dort ici", CX, 1330, entre(t, T_ARGENT - 0.05, 0.4, 2.2), "banknote", BEIGE, ENCRE, 30, -2)
        titre2(c, t, "REGARDEZ", "VOS CARTONS.", -0.6, T_LA - 0.1, ENCRE, -0.45)
        titre2(c, t, "C'EST LÀ QUE DORT", "VOTRE ARGENT.", T_LA - 0.1, t1, ROUGE, T_DORT - 0.1)


# ─────────────────────────────────────────── 2 · commandé des mois à l'avance, sur une intuition
MOIS = ["JANV.", "FÉVR.", "MARS", "AVRIL", "MAI", "JUIN", "JUIL.", "AOÛT"]


def scene_commande(c, t):
    t0, t1 = T_VOUS - 0.12, T_LES - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="gauche", d_in=0.32, d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-16, 8, prog(t, t0, t1 - t0, douce)) + 4 * math.sin(t * 0.8), cx=CX, cy=980)
        CW, CH = 330, 470
        # la collection commandée (photo) + tampon COMMANDÉ
        plans = [Plan(coins((-180, 0, 0), CW, CH, ay=12), CW, CH, carte_media("after-hours-trench-olive-veste-bleue", False, t0, "Votre collection", "shirt", fy=0.35), borne(a * 3))]
        # le calendrier qui défile : des mois
        u2 = prog(t, T_MOIS - 0.3, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_MOIS - 0.3 else 0.0
        if u2 > 0:
            def cal(cc, w, h):
                cadre(cc, 0, 0, w, h, w * 0.09)
                rrect(cc, w * 0.04, w * 0.04, w * 0.92, h * 0.18, w * 0.07, ENCRE)
                icone(cc, "calendar", w * 0.16, w * 0.04 + h * 0.09, w * 0.1, BLANC, 2.4)
                texte(cc, "COMMANDE", w * 0.27, w * 0.04 + h * 0.09 - hauteurLigne(w * 0.08, "noir") / 2, w * 0.08, BLANC, "noir", track=0.04)
                n = prog(t, T_MOIS - 0.1, T_INTUIT - T_MOIS + 0.3, lin) * 6
                cc.save(); cc.clipRect(skia.Rect.MakeXYWH(0, h * 0.26, w, h * 0.66))
                for k in range(8):
                    yy = h * 0.3 + (k - n) * h * 0.16
                    on = k == int(n)
                    texte(cc, MOIS[k], w / 2, yy, w * 0.16 if on else w * 0.11, ENCRE if on else "#C9C4BC", "archivo", "centre", -0.01)
                cc.restore()
                pilule(cc, "Des mois à l'avance", w / 2, h - w * 0.14, entre(t, T_AVANCE - 0.1, 0.4, 2.2), "hourglass", ROUGE, BLANC, w * 0.07)
            plans.append(Plan(coins((180, 0, mix(1400, 0, min(u2, 1.05))), CW, CH, ay=-12), CW, CH, cal, borne(u2 * 3)))
        scene3d(c, cam, plans)
        if t > T_COMMANDE - 0.05: tampon(c, "COMMANDÉ", CX - 180, 1020, t, T_COMMANDE, 44, ENCRE, -10)
        i = entre(t, T_INTUIT - 0.15, 0.45, 2.2)
        if i > 0:
            c.save(); c.translate(CX + 250, 700); c.rotate(6 * math.sin(t * 2.4)); c.scale(i, i)
            disque(c, 0, 0, 70, ENCRE, 1, (10, 26, 0.3)); icone(c, "lightbulb", 0, -6, 64, BEIGE, 2.6)
            texte(c, "?", 48, -70 - hauteurLigne(56, "archivo") / 2, 56, ROUGE, "archivo", "centre", 0)
            c.restore()
            pilule(c, "Sur une intuition", CX, 1330, i, "circle-help", ROUGE, BLANC, 30, 2)
        titre2(c, t, "VOUS AVEZ COMMANDÉ", "TOUTE VOTRE COLLECTION", T_VOUS - 0.05, T_MOIS - 0.1, ENCRE, T_COLL - 0.1)
        titre2(c, t, "DES MOIS À L'AVANCE", "SUR UNE INTUITION", T_MOIS - 0.1, t1, ROUGE, T_INTUIT - 0.1)


# ─────────────────────────────────────────── 3 · les pièces qui marchent : rupture ; les autres : elles s'entassent
def scene_rupture(c, t):
    t0, t1 = T_LES - 0.12, T_ET - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="haut", d_in=0.35, d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), cx=CX, cy=980)
        CW, CH = 320, 440
        u1 = prog(t, T_LES - 0.05, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_LES - 0.05 else 0.0
        u2 = prog(t, T_CELLES - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_CELLES - 0.1 else 0.0
        plans = []
        if u1 > 0:
            vide = prog(t, T_RUPTURE - 0.05, 0.4, sortie)        # la pièce qui marche disparaît de l'étagère
            def ok(cc, w, h):
                cadre(cc, 0, 0, w, h, w * 0.09, accent=VERT if vide < 0.5 else ROUGE)
                m = w * 0.04
                rrect(cc, m, m, w - 2 * m, h - 2 * m, w * 0.07, "#EFEDEA")
                if vide < 1:
                    cc.save(); cc.translate(w / 2, h / 2); s = mix(1, 0.2, vide); cc.scale(s, s); cc.translate(-w / 2, -h / 2)
                    with Calque(cc, 1 - vide): image_cover(cc, "produits/veste-ceinturee-prune", m, m, w - 2 * m, h - 2 * m, 1.0, 0.5, 0.5, w * 0.07)
                    cc.restore()
                if vide > 0.5:
                    texte(cc, "RUPTURE", w / 2, h * 0.42, ajuste("RUPTURE", w * 0.8, w * 0.16, "archivo", -0.01), ROUGE, "archivo", "centre", -0.01, borne((vide - 0.5) * 4))
                pilule(cc, "Ça marche", w / 2, h - m - w * 0.12, 1.0, "flame", BEIGE, ENCRE, w * 0.075)
            plans.append(Plan(coins((-185, 0, mix(1400, 0, min(u1, 1.05))), CW, CH, ay=12), CW, CH, ok, borne(u1 * 3)))
        if u2 > 0:
            # la pile d'invendus : la même pièce empilée, de plus en plus haut
            for k in range(4):
                e = entre(t, T_PASM + 0.1 * k, 0.4, 2.0) if t > T_PASM else (1.0 if k == 0 else 0.0)
                if e <= 0: continue
                z = mix(1400, 0, min(u2, 1.05)) - 70 * k
                plans.append(Plan(coins((185 + 26 * k, -52 * k, z), CW, CH, ay=-12, az=3 * k), CW, CH,
                                  carte_media("produits/blouson-cuir-noir", False, t0, "Ça ne marche pas" if k == 0 else None, "trending-down", GRIS), borne(u2 * 3) * borne(e * 3)))
        scene3d(c, cam, plans)
        r = entre(t, T_RUPTURE - 0.05, 0.4, 2.4)
        if r > 0:
            croix(c, CX - 185, 760, 48, r)
            eclats(c, CX - 185, 760, t, T_RUPTURE, 10, 280, cols=[ROUGE, ENCRE], graine=5)
        e = entre(t, T_ENTASSENT - 0.05, 0.4, 2.2)
        if e > 0:
            pilule(c, "Elles s'entassent", CX + 180, 1330, e, "boxes", ROUGE, BLANC, 28, -2)
            eclats(c, CX + 220, 760, t, T_ENTASSENT, 10, 280, cols=[ROUGE, GRIS], graine=6)
        titre2(c, t, "LES PIÈCES QUI MARCHENT ?", "EN RUPTURE.", T_LES - 0.05, T_CELLES - 0.1, ROUGE, T_RUPTURE - 0.1)
        titre2(c, t, "CELLES QUI NE MARCHENT PAS ?", "ELLES S'ENTASSENT.", T_CELLES - 0.1, t1, ROUGE, T_ENTASSENT - 0.1)


# ─────────────────────────────────────────── 4 · en fin de saison, vous bradez ce que vous avez payé plein tarif
def scene_bradez(c, t):
    t0, t1 = T_ET - 0.12, T_CE - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="gauche", d_in=0.35, d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        media(c, t, "produits/chemise-rayee-bordeaux", CX - 230, 620, 460, 600, borne(a * 3), mix(0.6, 1, a), zoom=1.0, fy=0.4, accent=ENCRE)
        # l'étiquette de prix : plein tarif barré, « bradé » qui claque
        e = entre(t, T_PAYE - 0.1, 0.45, 2.0)
        if e > 0:
            c.save(); c.translate(CX + 230, 760); c.rotate(-10 + 3 * math.sin(t * 1.8)); c.scale(e, e)
            rrect(c, -130, -90, 260, 180, 24, BLANC, 1, (12, 30, 0.22), "#DCD8D2", 3)
            disque(c, -100, -62, 12, "#DCD8D2")
            texte(c, "PLEIN TARIF", 0, -58, 26, GRIS, "noir", "centre", 0.04)
            texte(c, "€€€", 0, -14, 56, ENCRE, "archivo", "centre", 0)
            b = prog(t, T_BRADEZ - 0.05, 0.3, sortie)
            if b > 0: trait(c, -90, 10, -90 + 180 * b, 10, ROUGE, 9)
            c.restore()
        if t > T_BRADEZ - 0.12:
            tampon(c, "BRADÉ", CX + 160, 1060, t, T_BRADEZ - 0.08, 64, ROUGE, -12)
            eclats(c, CX + 160, 1060, t, T_BRADEZ, 12, 320, cols=[ROUGE, ENCRE], graine=7)
        pilule(c, "Fin de saison", CX, 1330, entre(t, T_SAISON - 0.1, 0.4, 2.2), "calendar-clock", ENCRE, BLANC, 30, -2)
        titre2(c, t, "EN FIN DE SAISON", "VOUS BRADEZ", T_ET - 0.05, T_PAYE - 0.1, ROUGE, T_BRADEZ - 0.12)
        titre2(c, t, "CE QUE VOUS AVEZ PAYÉ", "PLEIN TARIF.", T_PAYE - 0.1, t1, ROUGE, T_TARIF - 0.1)


# ─────────────────────────────────────────── 5 · pas un problème de goût, un problème de méthode
def scene_methode(c, t):
    t0, t1 = T_CE - 0.12, T_GRANDES - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="zoom", d_in=0.32, d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), cx=CX, cy=980)
        CW, CH = 320, 400
        def carte_ic(ic, lab, accent):
            def f(cc, w, h):
                cadre(cc, 0, 0, w, h, w * 0.1, accent=accent)
                disque(cc, w / 2, h * 0.36, w * 0.2, accent or ENCRE); icone(cc, ic, w / 2, h * 0.36, w * 0.2, BLANC, 2.6)
                texte(cc, lab, w / 2, h * 0.64, ajuste(lab, w * 0.8, w * 0.14, "archivo", -0.01), ENCRE, "archivo", "centre", -0.01)
            return f
        u1 = entre(t, T_CE, 0.5, 1.6)
        u2 = prog(t, T_CEST - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_CEST - 0.1 else 0.0
        plans = []
        if u1 > 0: plans.append(Plan(coins((-185, 0, 0), CW, CH, ay=12), CW, CH, carte_ic("paintbrush", "Le goût", VERT if t > T_GOUT else None), borne(u1 * 3)))
        if u2 > 0: plans.append(Plan(coins((185, 0, mix(1400, 0, min(u2, 1.05))), CW, CH, ay=-12), CW, CH, carte_ic("list-filter", "La méthode", ROUGE if t > T_METHODE else None), borne(u2 * 3)))
        scene3d(c, cam, plans)
        coche(c, CX - 185, 760, 44, entre(t, T_GOUT - 0.05, 0.35, 2.4))
        m = entre(t, T_METHODE - 0.05, 0.4, 2.4)
        if m > 0:
            croix(c, CX + 185, 760, 44, m)
            eclats(c, CX + 185, 760, t, T_METHODE, 10, 280, cols=[ROUGE, ENCRE], graine=8)
        titre2(c, t, "CE N'EST PAS", "UN PROBLÈME DE GOÛT", T_CE - 0.05, T_CEST - 0.1, ENCRE, T_CE + 0.15)
        titre2(c, t, "C'EST UN PROBLÈME", "DE MÉTHODE.", T_CEST - 0.1, t1, ROUGE, T_METHODE - 0.1)


# ─────────────────────────────────────────── 7 · tester, mesurer, réassortir : le graphique « vos ventes »
def scene_tester(c, t):
    t0, t1 = T_ELLES - 0.1, T_MQ + 0.1
    g = Groupe(c, t, t0, t1, ent="grand", sor="aucune", d_in=0.35, cy=960)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        pet = prog(t, T_SERIES - 0.1, 0.6, entreeSortie)            # petites séries : quatre petites barres
        mes = prog(t, T_MESURENT - 0.1, 0.6, entreeSortie)          # mesurer : elles prennent leurs vraies hauteurs
        rea = prog(t, T_REASS - 0.1, 0.7, lambda v: ressort(v, 1.3, 4.6)) if t > T_REASS - 0.1 else 0.0   # réassortir : la meilleure monte
        hb = [mix(mix(0.05, 0.2, pet), h1, mes) for h1 in (0.35, 0.52, 0.3, 0.28)]
        hb[1] = mix(hb[1], 0.95, min(rea, 1.1))
        gx0, gy0, base = graphique(c, t, CX, 960, hb, 1, t > T_REASS, borne(a * 3), mix(0.7, 1, a), "VOS VENTES")
        if mes > 0 and rea < 0.2:
            m = entre(t, T_MESURENT - 0.1, 0.4, 2.2)
            c.save(); c.translate(CX + 300, 700); c.rotate(-8); c.scale(m, m)
            disque(c, 0, 0, 56, ENCRE, 1, (10, 26, 0.3)); icone(c, "chart-line", 0, 0, 56, BEIGE, 2.6)
            c.restore()
        if rea > 0:
            bx = gx0 + 90 + 180 + 60
            r = entre(t, T_REASS - 0.05, 0.4, 2.4)
            c.save(); c.translate(bx, base - 330 * 0.95 - 60); c.scale(r, r); c.rotate(-8)
            disque(c, 0, 0, 48, BEIGE, 1, (10, 26, 0.3)); icone(c, "refresh-cw", 0, 0, 50, ENCRE, 2.8)
            c.restore()
            eclats(c, bx, base - 300, t, T_REASS + 0.2, 12, 320, cols=[BEIGE, BEIGE2, ENCRE], graine=9)
            pilule(c, "Réassort", bx, base - 330 * 0.95 - 130, entre(t, T_VEND - 0.1, 0.4, 2.2), "flame", BEIGE, ENCRE, 26)
        for k, (lab, ic, tk, x) in enumerate((("Tester", "sparkles", T_TESTENT, CX - 240), ("Mesurer", "chart-line", T_MESURENT, CX), ("Réassortir", "refresh-cw", T_REASS, CX + 240))):
            pilule(c, lab, x, 1340, entre(t, tk - 0.05, 0.4, 2.2), ic, BEIGE if k == 2 else ENCRE, ENCRE if k == 2 else BLANC, 28, (-2, 2, -2)[k])
        titre2(c, t, "ELLES TESTENT", "EN PETITES SÉRIES", T_ELLES - 0.05, T_MESURENT - 0.1, ENCRE, T_SERIES - 0.15)
        titre2(c, t, "ELLES MESURENT", "ET RÉASSORTISSENT", T_MESURENT - 0.1, T_VEND - 0.1, ENCRE, T_REASS - 0.1)
        titre2(c, t, None, "CE QUI SE VEND.", T_VEND - 0.1, T_EXACT - 0.1, BEIGE, T_VEND - 0.1)
        titre2(c, t, "C'EST EXACTEMENT", "CE QUE VOUS PERMET", T_EXACT - 0.1, t1, ENCRE, T_EXACT + 0.15)


# ─────────────────────────────────────────── 9 · ce que fait Monarque : développer, suivre la production, réassortir
ETAPES = [(T_NOUS, "fiche-technique", False, "Développement", "file-text", "NOUS DÉVELOPPONS", "VOS PRODUITS"),
          (T_SUIVONS, "rushes/machines", True, "Production en Chine", "factory", "NOUS SUIVONS", "VOTRE PRODUCTION EN CHINE"),
          (T_SOURC, "rushes/nuancier", True, "Sourcing", "layers", "DU SOURCING", None),
          (T_CONTR, "rushes/controle", True, "Contrôle", "shield-check", None, "AU CONTRÔLE"),
          (T_ORGA, "shop", False, "Réassorts", "refresh-cw", "NOUS ORGANISONS", "VOS RÉASSORTS")]


def scene_monarque_fait(c, t):
    t0, t1 = T_NOUS - 0.1, T_ARRET - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="zoom", d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.8), ay=6 * math.sin(t * 0.7), cx=CX, cy=900)
        CW, CH = 310, 420
        plans = []
        for k, (tk, nom, vid, lab, ic, _, _) in enumerate(ETAPES):
            u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.6)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            suiv = ETAPES[k + 1][0] if k < 4 else None
            rec = prog(t, suiv - 0.15, 0.5, entreeSortie) if suiv else 0.0
            x = mix(0, -340 + 90 * k, rec); z = mix(1400, 0, min(u, 1.05)) + 500 * rec; y = -140 * rec
            plans.append(Plan(coins((x, y, z), CW, CH, ay=mix(0, 18, rec)), CW, CH,
                              carte_media(nom, vid, tk - 0.3, lab if rec < 0.5 else None, ic, zoom=1.0, fy=0.4), borne(u * 3) * (1 - 0.5 * rec)))
        scene3d(c, cam, plans)
        # la piste développement → production → contrôle → réassort
        x0, x1, py = CX - 320, CX + 320, 1240
        trait(c, x0, py, x1, py, "#DCD8D2", 8, entre(t, t0, 0.4, 1.4))
        p = prog(t, T_DEV - 0.1, T_REASS2 - T_DEV + 0.1, entreeSortie)
        trait(c, x0, py, mix(x0, x1, p), py, ENCRE, 8)
        for k, (lab, tk) in enumerate((("Développement", T_DEV), ("Production", T_PROD), ("Contrôle", T_CONTR), ("Réassort", T_REASS2))):
            x = x0 + k * (x1 - x0) / 3
            on = t > tk - 0.1
            disque(c, x, py, 22 if on else 16, ENCRE if on else "#DCD8D2")
            if on: icone(c, "check", x, py, 24, BLANC, 3)
            texte(c, lab, x, py + 40, 24, ENCRE if on else GRIS, "gras", "centre", -0.01)
        disque(c, mix(x0, x1, p), py, 30, BEIGE, 1, (8, 20, 0.3))
        v = entre(t, T_VENTES - 0.15, 0.4, 2.2)
        pilule(c, "Vos meilleures ventes", CX, 1340, v, "flame", BEIGE, ENCRE, 28)
        for k, (tk, _, _, _, _, l1, l2) in enumerate(ETAPES):
            fin = ETAPES[k + 1][0] - 0.12 if k < 4 else T_VENTES - 0.1
            titre2(c, t, l1, l2, tk - 0.08, fin, ENCRE, tk - 0.05)
        titre2(c, t, "SUR VOS", "MEILLEURES VENTES", T_VENTES - 0.1, t1, BEIGE, T_VENTES - 0.05)


# ─────────────────────────────────────────── 10 · arrêtez de parier sur une saison ; investissez sur ce qui marche
def scene_parier(c, t):
    t0, t1 = T_ARRET - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="bas", sor="recul", d_in=0.35, d_out=0.4, cy=960)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), cx=CX, cy=980)
        CW, CH = 320, 440
        u1 = entre(t, T_ARRET, 0.5, 1.6)
        u2 = prog(t, T_INVEST - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_INVEST - 0.15 else 0.0
        plans = []
        if u1 > 0:
            def parier(cc, w, h):
                cadre(cc, 0, 0, w, h, w * 0.09, accent=ROUGE if t > T_SAISON2 else None)
                rrect(cc, w * 0.08, h * 0.1, w * 0.84, h * 0.5, w * 0.05, "#EFEDEA")
                for i in range(12):                                   # une saison entière : 12 cases
                    xx, yy = w * 0.12 + (i % 4) * w * 0.2, h * 0.14 + (i // 4) * h * 0.15
                    rrect(cc, xx, yy, w * 0.16, h * 0.11, w * 0.02, "#DCD8D2")
                    if t > T_SAISON2 + 0.04 * i: icone(cc, "circle-help", xx + w * 0.08, yy + h * 0.055, w * 0.07, ROUGE, 2.4)
                texte(cc, "PARIER", w / 2, h * 0.68, ajuste("PARIER", w * 0.8, w * 0.15, "archivo", -0.01), ENCRE, "archivo", "centre", -0.01)
                pilule(cc, "Une saison entière", w / 2, h - w * 0.14, entre(t, T_ENTIERE - 0.1, 0.4, 2.2), "hourglass", ROUGE, BLANC, w * 0.07)
            plans.append(Plan(coins((-185, 0, 0), CW, CH, ay=12), CW, CH, parier, borne(u1 * 3)))
        if u2 > 0:
            def investir(cc, w, h):
                cadre(cc, 0, 0, w, h, w * 0.09, accent=BEIGE if t > T_MARCHE - 0.1 else None)
                m = w * 0.04
                image_cover(cc, "produits/veste-ceinturee-prune", m, m, w - 2 * m, h * 0.58, 1.0, 0.5, 0.45, w * 0.07)
                texte(cc, "INVESTIR", w / 2, h * 0.68, ajuste("INVESTIR", w * 0.8, w * 0.15, "archivo", -0.01), ENCRE, "archivo", "centre", -0.01)
                pilule(cc, "Ce qui marche", w / 2, h - w * 0.14, entre(t, T_MARCHE - 0.1, 0.4, 2.2), "flame", BEIGE, ENCRE, w * 0.07)
            plans.append(Plan(coins((185, 0, mix(1400, 0, min(u2, 1.05))), CW, CH, ay=-12), CW, CH, investir, borne(u2 * 3)))
        scene3d(c, cam, plans)
        x = entre(t, T_SAISON2 - 0.05, 0.4, 2.4)
        if x > 0:
            croix(c, CX - 185, 760, 44, x)
            eclats(c, CX - 185, 760, t, T_SAISON2, 10, 280, cols=[ROUGE, ENCRE], graine=10)
        v = entre(t, T_MARCHE - 0.05, 0.4, 2.4)
        if v > 0:
            coche(c, CX + 185, 760, 44, v, BEIGE)
            eclats(c, CX + 185, 760, t, T_MARCHE, 14, 340, cols=[BEIGE, BEIGE2, ENCRE], graine=11)
        titre2(c, t, "ARRÊTEZ DE PARIER", "SUR UNE SAISON ENTIÈRE", T_ARRET - 0.05, T_INVEST - 0.15, ROUGE, T_PARIER - 0.05)
        titre2(c, t, "INVESTISSEZ", "SUR CE QUI MARCHE.", T_INVEST - 0.15, T_FIN - 0.05, BEIGE, T_INVEST - 0.1)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8)
for k in range(5): son(max(0.0, -0.45 + 0.07 * k), "impact_doux", -12)
son(T_CARTONS, "impact_doux", -8)
for k in range(4): son(T_DORT - 0.1 + 0.08 * k, "ching", -14)
son(T_ARGENT - 0.05, "pop", -10)
son(T_VOUS - 0.12, "whoosh", -9); son(T_COMMANDE, "tampon", -7); son(T_MOIS - 0.3, "whoosh_court", -10); son(T_MOIS - 0.2, "impact_doux", -9)
for k in range(6): son(T_MOIS + k * (T_INTUIT - T_MOIS + 0.3) / 6, "tick", -15)
son(T_AVANCE - 0.1, "pop", -10); son(T_INTUIT - 0.15, "pop", -9)
son(T_LES - 0.12, "whoosh_bas", -8); son(T_LES - 0.05, "impact_doux", -9); son(T_RUPTURE - 0.05, "croc", -7); son(T_RUPTURE, "tampon", -9)
son(T_CELLES - 0.1, "whoosh_court", -10); son(T_CELLES, "impact_doux", -9)
for k in range(4): son(T_PASM + 0.1 * k, "impact_doux", -12)
son(T_ENTASSENT - 0.05, "pop", -9); son(T_ENTASSENT, "croc", -9)
son(T_ET - 0.12, "whoosh", -9); son(T_SAISON - 0.1, "pop", -10); son(T_PAYE - 0.1, "pop", -9); son(T_BRADEZ - 0.05, "swipe", -9); son(T_BRADEZ - 0.08, "tampon", -5)
son(T_CE - 0.12, "swipe", -9); son(T_GOUT - 0.05, "check", -9); son(T_CEST - 0.1, "whoosh_court", -10); son(T_CEST, "impact_doux", -9); son(T_METHODE - 0.05, "croc", -7)
son(T_GRANDES - 0.12, "whoosh_long", -7); son(T_GRANDES, "impact", -3); son(T_DEVINENT, "impact", -5)
son(T_ELLES - 0.1, "whoosh_bas", -8); son(T_SERIES - 0.1, "montee", -14)
for k in range(3): son(T_TESTENT - 0.05 + [0, T_MESURENT - T_TESTENT, T_REASS - T_TESTENT][k], "pop", -10)
son(T_MESURENT - 0.1, "montee", -13); son(T_REASS - 0.05, "whoosh_court", -9); son(T_REASS + 0.2, "impact", -6); son(T_REASS + 0.22, "ching", -9)
son(T_VEND - 0.1, "pop", -10)
son(T_MQ - 0.12, "whoosh_long", -7); son(T_MQ + 0.05, "impact", -4); son(T_MQ + 0.08, "ching", -9); son(T_NOUS - 0.3, "whoosh_bas", -8)
for tk, _, _, _, _, _, _ in ETAPES: son(tk - 0.15, "whoosh_court", -10); son(tk, "impact_doux", -10)
for tk in (T_DEV, T_PROD, T_CONTR, T_REASS2): son(tk - 0.1, "check", -12)
son(T_VENTES - 0.15, "pop", -9); son(T_VENTES, "ching", -11)
son(T_ARRET - 0.12, "whoosh", -9); son(T_ARRET, "impact_doux", -9)
for i in range(12): son(T_SAISON2 + 0.04 * i, "tick", -16)
son(T_SAISON2 - 0.05, "croc", -7); son(T_ENTIERE - 0.1, "pop", -10)
son(T_INVEST - 0.15, "whoosh_court", -9); son(T_INVEST, "impact_doux", -8); son(T_MARCHE - 0.05, "check", -8); son(T_MARCHE, "ching", -9)
sons_signature_mq(son, T_FIN, T_BOUTON)
for tl in (T_L1, T_L2): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_LA - 0.1, T_LA + 0.3), (T_VOUS - 0.15, T_VOUS + 0.25), (T_LES - 0.15, T_LES + 0.25), (T_CELLES - 0.15, T_CELLES + 0.25),
             (T_ET - 0.15, T_ET + 0.25), (T_CE - 0.15, T_CE + 0.25), (T_GRANDES - 0.1, T_GRANDES + 0.3), (T_ELLES - 0.15, T_ELLES + 0.3),
             (T_MQ - 0.1, T_MQ + 0.3), (T_NOUS - 0.15, T_NOUS + 0.25), (T_ARRET - 0.15, T_ARRET + 0.25), (T_INVEST - 0.15, T_INVEST + 0.25),
             (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_ARGENT - 0.05, BEIGE, 0.06), (T_RUPTURE, ROUGE, 0.06), (T_BRADEZ - 0.08, ROUGE, 0.07), (T_GRANDES, "#FFFFFF", 0.08),
                    (T_REASS + 0.2, BEIGE, 0.07), (T_MQ + 0.05, "#FFFFFF", 0.1), (T_MARCHE, BEIGE, 0.07)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_clair(c, t)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_commande(c, t); scene_rupture(c, t); scene_bradez(c, t); scene_methode(c, t)
    r1 = flash_noir(c, t, T_GRANDES, T_ELLES, "LES GRANDES MARQUES", "NE DEVINENT PAS.")
    with Balance(c, t, 0.8):
        if r1 < 2100: scene_tester(c, t)
    r2 = logo_monarque(c, t, T_MQ, T_NOUS - 0.3, T_FIN)
    with Balance(c, t, 0.8):
        if r2 < 2100: scene_monarque_fait(c, t); scene_parier(c, t)
    signature_mq(c, t, T_FIN, MEDIAS, [("Votre argent doit tourner.", T_L1, 46, ENCRE), ("Pas dormir.", T_L2, 46, BEIGE)], T_BOUTON, cy=800)
    K.dessine_eclairs(c, t)
    cache = (T_GRANDES - 0.1 < t < T_ELLES - 0.05) or (T_MQ - 0.1 < t < T_NOUS - 0.05) or t > T_FIN - 0.1
    if not cache: SOUS.dessine(c, t, BLANC if max(r1 or 0, r2 or 0) > 1200 else ENCRE)
