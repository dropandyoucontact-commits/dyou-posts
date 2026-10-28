"""MQ-M09 « Vous lui avez envoyé une photo. Il vous a renvoyé son interprétation. » — hook écrit par nous (20/10/2026).
Levier : confusion / révélation (l'idée contre le produit reçu) + l'étape manquante. Persona : créateur de marque qui
envoie une photo d'inspiration à un fabricant et reçoit « à peu près ». Message Monarque : le développement produit
(dossier technique, patronage, matière au nuancier, prototype validé), culture produit française + équipe en Chine.
Charte MQ-M05 + cartes 3D + signature 3D MONARQUE (mq.signature_mq). Aucun chiffre. Zone sûre : x 130-860."""
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
from mq import flash_noir, logo_monarque, signature_mq, sons_signature_mq

polices(P)
K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 2.3, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = SousTitresEncre(K, y=1440, larg=640, taille=50, fam="gras", max_mots=5, cx=500)
CX = 510

# repères (mots)
T_ENVOYE, T_PHOTO, T_IL, T_RENVOYE, T_INTERP = TW(3), TW(5), TW(6), TW(9), TW(11)
T_MATIERE, T_PRES, T_COUPE, T_APPROX, T_TAILLES, T_VOTRES = TW(13), TW(16), TW(18), TW(19), TW(21), TW(24)
T_ET, T_DEMANDEZ, T_POURQUOI, T_PRODUIT, T_RESS, T_IDEE = TW(25), TW(28), TW(29), TW(31), TW(33), TW(37)
T_PARCE, T_PHOTO2, T_PRODUIT2 = TW(38), TW(40), TW(44)
T_ENTRE, T_MANQUE, T_ETAPE, T_MARQUES, T_SAUTENT, T_JAMAIS, T_DEVEL = TW(45), TW(49), TW(51), TW(54), TW(57), TW(58), TW(60)
T_UN, T_DOSSIER, T_PRECIS, T_UN2, T_PATRON, T_MESURES = TW(61), TW(62), TW(64), TW(65), TW(66), TW(69)
T_UNE, T_CHOISIE, T_NUANCIER, T_PASE, T_ECRAN, T_UN3, T_PROTO, T_VALIDE, T_LANCER, T_SOIT = TW(70), TW(72), TW(75), TW(76), TW(79), TW(80), TW(81), TW(82), TW(85), TW(89)
T_CEST, T_METIER, T_MQ = TW(90), TW(93), TW(95)
T_UNEC, T_CULTURE, T_FRANC, T_ETEQ, T_EQUIPE, T_CHINE, T_POUR, T_DESSINE, T_FRANCE, T_FABRIQUE, T_PREVU = \
    TW(96), TW(97), TW(99), TW(100), TW(102), TW(105), TW(106), TW(111), TW(113), TW(115), TW(117)
T_VOUS, T_GARDEZ, T_LIDEE, T_NOUS, T_FAISONS, T_PRODUITF = TW(118), TW(119), TW(120), TW(121), TW(123), TW(125)
T_FIN, T_L1, T_L2 = TW(126), TW(127), TW(131)
T_BOUTON = TW(134) + 0.7

MEDIAS = [("fiche-technique", False), ("rushes/couture", True), ("produits/veste-zip-marine", False),
          ("rushes/nuancier", True), ("produits/blouse-satin-kaki-dos", False), ("rushes/atelier", True)]


# ─────────────────────────────────────────── briques locales
def titre2(c, t, l1, l2, t0, t1, c2=ENCRE, t2=None):
    if l1: titre(c, t, l1, t0, t1, y=330, taille=84, larg=780)
    if l2: titre(c, t, l2, (t2 if t2 is not None else t0 + 0.12), t1, y=440, couleur=c2, taille=84, larg=780)


def carte_media(nom, vid, t0, label=None, ic=None, accent=None, voile=None, zoom=1.0, fy=0.5, fond_=ENCRE, col=BLANC):
    def f(c, w, h):
        t = agence.T_COURANT[0]
        cadre(c, 0, 0, w, h, w * 0.09, accent=accent)
        m = w * 0.04
        if vid: video(c, nom, m, m, int(w - 2 * m), int(h - 2 * m), t - t0, 1.0, rayon=w * 0.07)
        else: image_cover(c, nom, m, m, w - 2 * m, h - 2 * m, zoom, 0.5, fy, rayon=w * 0.07)
        if voile: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(m, m, w - 2 * m, h - 2 * m), w * 0.07, w * 0.07), peinture(voile[0], voile[1]))
        if label: pilule(c, label, w / 2, h - m - w * 0.12, 1.0, ic, fond_, col, max(20, w * 0.075))
    return f


def interpretation(cc, w, h, t):
    """le produit « interprété » : la photo tordue, délavée, avec un « ? » rouge"""
    cadre(cc, 0, 0, w, h, w * 0.09, accent=ROUGE)
    m = w * 0.04
    cc.save(); cc.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(m, m, w - 2 * m, h - 2 * m), w * 0.07, w * 0.07), True)
    cc.save(); cc.translate(w / 2, h / 2); cc.skew(0.08, 0.0); cc.scale(1.08, 0.94); cc.translate(-w / 2, -h / 2)
    image_cover(cc, "trench-court", m, m, w - 2 * m, h - 2 * m, 1.0, 0.5, 0.4)
    cc.restore()
    cc.drawRect(skia.Rect.MakeWH(w, h), peinture("#8C8985", 0.35))
    cc.restore()
    cc.save(); cc.translate(w * 0.8, h * 0.14); cc.rotate(8 * math.sin(t * 2.4))
    disque(cc, 0, 0, w * 0.1, ROUGE); texte(cc, "?", 0, -hauteurLigne(w * 0.13, "archivo") / 2, w * 0.13, BLANC, "archivo", "centre", 0)
    cc.restore()
    pilule(cc, "Son interprétation", w / 2, h - m - w * 0.12, 1.0, "triangle-alert", ROUGE, BLANC, w * 0.07)


# ─────────────────────────────────────────── 1 · hook : vous lui avez envoyé une photo, il vous a renvoyé son interprétation
def scene_hook(c, t):
    t1 = T_MATIERE - 0.12
    g = Groupe(c, t, -1, t1, ent="aucune", sor="zoom", d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        o = prog(t, -0.3, 1.4, douce)
        rep = prog(t, T_RENVOYE - 0.1, 0.6, entreeSortie)          # la réponse arrive : la photo se pousse à gauche
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.9), ay=mix(-18, 6, o) + 4 * math.sin(t * 0.7), tz=mix(200, 0, prog(t, -0.3, 0.8, sortie)), cx=CX, cy=1000)
        CW, CH = 380, 540
        sx, sy = secousse(t, T_INTERP, 12, 0.3)
        plans = [Plan(coins((mix(0, -190, rep), mix(0, -30, rep), mix(0, 120, rep)), CW, CH, ay=mix(0, 14, rep)), CW, CH,
                      carte_media("after-hours-trench-olive-veste-bleue", False, -0.3, "Votre photo", "image", fy=0.35), 1.0)]
        if rep > 0:
            plans.append(Plan(coins((mix(700, 190, rep) + sx, 30 + sy, mix(900, 0, rep)), CW, CH, ay=-14), CW, CH, lambda cc, w, h: interpretation(cc, w, h, t), borne(rep * 2)))
        scene3d(c, cam, plans)
        # la flèche d'envoi, puis la flèche de retour
        e = prog(t, T_ENVOYE - 0.05, 0.4, entreeSortie)
        if e > 0 and rep < 1:
            with Calque(c, 1 - rep):
                pilule(c, "Envoyé", CX + 250, 700, entre(t, T_ENVOYE - 0.05, 0.4, 2.2), "send", ENCRE, BLANC, 28, 3)
        if rep > 0.8:
            onde(c, CX + 190, 1000, t, T_INTERP, 80, 520, ROUGE, 8, 0.6)
            eclats(c, CX + 190, 1000, t, T_INTERP, 14, 400, cols=[ROUGE, ENCRE, "#C9C4BC"], graine=12)
        titre2(c, t, "VOUS LUI AVEZ ENVOYÉ", "UNE PHOTO.", -0.6, T_IL - 0.08, ENCRE, -0.45)
        titre2(c, t, "IL VOUS A RENVOYÉ", "SON INTERPRÉTATION.", T_IL - 0.08, t1, ROUGE, T_RENVOYE - 0.08)


# ─────────────────────────────────────────── 2 · la matière à peu près, la coupe approximative, les tailles pas les vôtres
ECARTS = [(T_MATIERE, T_PRES, "layers", "La matière", "à peu près", "LA MATIÈRE", "À PEU PRÈS"),
          (T_COUPE, T_APPROX, "scissors", "La coupe", "approximative", "LA COUPE", "APPROXIMATIVE"),
          (T_TAILLES, T_VOTRES, "scan-line", "Les tailles", "pas les vôtres", "LES TAILLES", "PAS LES VÔTRES")]


def scene_ecarts(c, t):
    t0, t1 = T_MATIERE - 0.12, T_ET - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="gauche", d_in=0.32, d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        media(c, t, "trench-court", CX - 390, 620, 340, 480, borne(a * 3), mix(0.6, 1, a), zoom=1.05, fy=0.4, accent=ROUGE, voile=("#8C8985", 0.25))
        for k, (tk, tv, ic, lab, sous, _, _) in enumerate(ECARTS):
            u = entre(t, tk - 0.12, 0.45, 1.8)
            if u <= 0: continue
            x, y, w, h = CX - 10, 640 + k * 160, 500, 136
            c.save(); c.translate(380 * (1 - min(u, 1)), 0)
            with Calque(c, borne(u * 3)):
                cadre(c, x, y, w, h, 36, accent=ROUGE if t > tv else None)
                disque(c, x + 68, y + h / 2, 42, ENCRE); icone(c, ic, x + 68, y + h / 2, 42, BLANC, 2.6)
                texte(c, lab, x + 130, y + 26, 34, ENCRE, "archivo", track=-0.01)
                v = entre(t, tv - 0.05, 0.4, 2.2)
                if v > 0: texte(c, sous, x + 130, y + 76, 30, ROUGE, "gras", track=-0.01, alpha=borne(v * 3))
                croix(c, x + w - 50, y + h / 2, 28, v)
            c.restore()
            if t > tv and t < tv + 0.5: eclats(c, x + w - 50, y + h / 2, t, tv, 8, 200, cols=[ROUGE, ENCRE], graine=20 + k, duree=0.6)
        for k, (tk, tv, _, _, _, l1, l2) in enumerate(ECARTS):
            fin = ECARTS[k + 1][0] - 0.1 if k < 2 else t1
            titre2(c, t, l1, l2, tk - 0.08, fin, ROUGE, tv - 0.08)


# ─────────────────────────────────────────── 3 · pourquoi votre produit ne ressemble pas à votre idée
def scene_pourquoi(c, t):
    t0, t1 = T_ET - 0.12, T_PARCE - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="aucune", d_in=0.35, cy=960)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), cx=CX, cy=1000)
        CW, CH = 320, 460
        u1 = entre(t, T_ET, 0.5, 1.6)
        u2 = prog(t, T_PRODUIT - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_PRODUIT - 0.1 else 0.0
        plans = []
        if u1 > 0: plans.append(Plan(coins((-185, 0, 0), CW, CH, ay=12), CW, CH, carte_media("fiche-technique", False, t0, "Votre idée", "lightbulb", BEIGE, fy=0.3, fond_=BEIGE, col=ENCRE), borne(u1 * 3)))
        if u2 > 0: plans.append(Plan(coins((185, 0, mix(1400, 0, min(u2, 1.05))), CW, CH, ay=-12), CW, CH, carte_media("trench-court", False, t0, "Votre produit", "shirt", ROUGE, ("#8C8985", 0.3), fy=0.4, fond_=ROUGE), borne(u2 * 3)))
        scene3d(c, cam, plans)
        signe(c, "≠", CX, 1000, entre(t, T_RESS - 0.05, 0.35, 2.6), ROUGE, 60, t, T_RESS)
        q = entre(t, T_POURQUOI - 0.05, 0.4, 2.4)
        if q > 0:
            c.save(); c.translate(CX, 1330); c.scale(q, q); c.rotate(6 * math.sin(t * 2.4))
            disque(c, 0, 0, 70, ENCRE, 1, (12, 30, 0.3)); texte(c, "?", 0, -hauteurLigne(90, "archivo") / 2, 90, BLANC, "archivo", "centre", 0)
            c.restore()
        titre2(c, t, "VOUS VOUS DEMANDEZ POURQUOI", "VOTRE PRODUIT", T_ET - 0.05, T_RESS - 0.1, ENCRE, T_PRODUIT - 0.1)
        titre2(c, t, "NE RESSEMBLE PAS", "À VOTRE IDÉE.", T_RESS - 0.1, t1, ROUGE, T_IDEE - 0.1)


# ─────────────────────────────────────────── 5 · il manque une étape : le développement
def scene_etape(c, t):
    t0, t1 = T_ENTRE - 0.1, T_UN - 0.12
    g = Groupe(c, t, t0, t1, ent="grand", sor="haut", d_in=0.35, d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        y = 980
        with Calque(c, borne(a * 3)):
            media(c, t, "fiche-technique", CX - 420, y - 160, 240, 320, 1.0, 1.0, zoom=1.0, fy=0.3, r=28, pad=8)
            pilule(c, "L'idée", CX - 300, y + 210, 1.0, "lightbulb", ENCRE, BLANC, 26)
            media(c, t, "produits/veste-zip-marine", CX + 180, y - 160, 240, 320, 1.0, 1.0, zoom=1.0, fy=0.4, r=28, pad=8)
            pilule(c, "Le produit", CX + 300, y + 210, 1.0, "shirt", ENCRE, BLANC, 26)
            trait(c, CX - 170, y, CX - 80, y, "#DCD8D2", 8, 1, [12, 12]); trait(c, CX + 80, y, CX + 170, y, "#DCD8D2", 8, 1, [12, 12])
        # la case manquante, en pointillés, qui clignote ; puis « DÉVELOPPEMENT » la remplit
        m = entre(t, T_MANQUE - 0.1, 0.45, 2.0)
        d = prog(t, T_DEVEL - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.6)) if t > T_DEVEL - 0.1 else 0.0
        if m > 0:
            c.save(); c.translate(CX, y); c.scale(m, m)
            if d < 1:
                pe = peinture(ROUGE if t > T_SAUTENT else GRIS, 0.9 * (1 - d), Style=skia.Paint.kStroke_Style, StrokeWidth=4); pe.setPathEffect(skia.DashPathEffect.Make([14, 10], t * 40))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -160, 160, 320), 28, 28), pe)
                texte(c, "?", 0, -hauteurLigne(90, "archivo") / 2, 90, "#C9C4BC", "archivo", "centre", 0, 0.6 + 0.4 * math.sin(t * 7))
            if d > 0:
                s = min(d, 1.08); c.scale(s, s)
                rrect(c, -80, -160, 160, 320, 28, BEIGE, 1, (14, 34, 0.3))
                icone(c, "scissors", 0, -70, 60, ENCRE, 2.6)
                c.save(); c.translate(0, 60); c.rotate(-90)
                texte(c, "DÉVELOPPEMENT", 0, -hauteurLigne(30, "archivo") / 2, 30, ENCRE, "archivo", "centre", 0.02)
                c.restore()
            c.restore()
            if d > 0: eclats(c, CX, y, t, T_DEVEL, 14, 380, cols=[BEIGE, BEIGE2, ENCRE], graine=9)
        if t > T_SAUTENT - 0.1: pilule(c, "Jamais sautée", CX, 1340, entre(t, T_SAUTENT - 0.1, 0.4, 2.2) * (1 - prog(t, T_DEVEL - 0.1, 0.3)), "ban", ROUGE, BLANC, 28, -2)
        titre2(c, t, "ENTRE LES DEUX,", "IL MANQUE UNE ÉTAPE", T_ENTRE - 0.05, T_MARQUES - 0.1, ENCRE, T_MANQUE - 0.1)
        titre2(c, t, "LES MARQUES SÉRIEUSES", "NE LA SAUTENT JAMAIS", T_MARQUES - 0.1, T_DEVEL - 0.15, ROUGE, T_SAUTENT - 0.1)
        titre2(c, t, None, "LE DÉVELOPPEMENT", T_DEVEL - 0.15, t1, BEIGE, T_DEVEL - 0.1)


# ─────────────────────────────────────────── 6 · dossier technique, patronage, matière au nuancier, prototype validé
TUILES = [(T_UN, T_PRECIS, "fiche-technique", False, "Dossier technique", "file-text", "UN DOSSIER TECHNIQUE", "PRÉCIS"),
          (T_UN2, T_MESURES, "techpack-veste-guide-tailles", False, "Patronage", "scissors", "UN PATRONAGE", "À VOS MESURES"),
          (T_UNE, T_NUANCIER, "rushes/nuancier", True, "Matière", "layers", "UNE MATIÈRE CHOISIE", "DANS UN NUANCIER"),
          (T_UN3, T_VALIDE, "rushes/controle", True, "Prototype", "badge-check", "UN PROTOTYPE VALIDÉ", "AVANT DE LANCER")]


def scene_tuiles(c, t):
    t0, t1 = T_UN - 0.12, T_MQ + 0.1
    g = Groupe(c, t, t0, t1, ent="droite", sor="aucune", d_in=0.32, cy=960)
    if not g.visible: return
    with g:
        for k, (tk, tv, nom, vid, lab, ic, _, _) in enumerate(TUILES):
            u = entre(t, tk - 0.15, 0.42, 1.8)
            if u <= 0: continue
            x, y = 130 + (k % 2) * 380, 580 + (k // 2) * 400
            w, h = 350, 380
            c.save(); c.translate(x + w / 2, y + h / 2); c.scale(mix(0.4, 1, u), mix(0.4, 1, u)); c.translate(-(x + w / 2), -(y + h / 2))
            if vid: media(c, t, nom, x, y, w, h, borne(u * 3), 1.0, video_t0=tk - 0.2, vitesse=1.0, r=30, pad=10, accent=BEIGE if t > tv else None)
            else: media(c, t, nom, x, y, w, h, borne(u * 3), 1.0, zoom=1.0, fy=0.3, r=30, pad=10, accent=BEIGE if t > tv else None)
            c.restore()
            pilule(c, lab, x + w / 2, y + h - 44, entre(t, tk, 0.4, 2.2), ic, ENCRE, BLANC, 26)
            coche(c, x + w - 34, y + 34, 26, entre(t, tv + 0.05, 0.35, 2.4), BEIGE)
        # « pas sur un écran » : un petit écran barré
        e = entre(t, T_PASE - 0.05, 0.4, 2.2) * (1 - prog(t, T_UN3 - 0.1, 0.3))
        if e > 0:
            c.save(); c.translate(CX + 300, 1000); c.rotate(-8); c.scale(e, e)
            disque(c, 0, 0, 62, ENCRE, 1, (10, 26, 0.3)); icone(c, "smartphone", 0, 0, 56, BLANC, 2.6)
            c.restore()
            croix(c, CX + 345, 955, 26, entre(t, T_ECRAN - 0.05, 0.35, 2.4))
        for k, (tk, tv, _, _, _, _, l1, l2) in enumerate(TUILES):
            fin = TUILES[k + 1][0] - 0.1 if k < 3 else T_CEST - 0.1
            titre2(c, t, l1, l2, tk - 0.08, fin, BEIGE, tv - 0.1)
        titre2(c, t, "C'EST EXACTEMENT", "LE MÉTIER DE", T_CEST - 0.1, t1, ENCRE, T_METIER - 0.1)


# ─────────────────────────────────────────── 8 · culture produit française, équipe en Chine : dessiné en France, fabriqué comme prévu
def scene_france_chine(c, t):
    t0, t1 = T_UNEC - 0.25, T_VOUS - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="zoom", d_out=0.3, cy=960)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.3)
        rot = prog(t, T_UNEC, T_CHINE - T_UNEC + 0.2, entreeSortie)
        lon0 = mix(14, 96, rot) + 2.0 * (t - T_UNEC); lat0 = mix(42, 28, rot)
        R = 330 * mix(0.7, 1, a)
        cx, cy = CX, 1020
        lum = prog(t, T_CHINE - 0.15, 0.6, sortie)
        with Calque(c, borne(a * 3)):
            G = globe_points(c, lon0, lat0, cx, cy, R, lum)
            u = prog(t, T_ETEQ - 0.1, T_CHINE - T_ETEQ + 0.3, entreeSortie)
            G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, 1.0, "#D5D1CB", 5, 0.3, [2, 16])
            hx, hy, hz = G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, u, ENCRE, 7, 0.3)
            if 0 < u < 1: disque(c, hx, hy, 24, ENCRE, 1, (6, 16, 0.25)); icone(c, "plane", hx, hy, 28, BLANC, 2.4)
            G.repere(c, *PARIS, cx, cy, R, lon0, lat0, "Culture produit", ENCRE, "FR", entre(t, T_CULTURE - 0.05, 0.42, 2.0), 1.0, 70)
            kx, ky, kz = G.pos(*CANTON, lon0, lat0, R, cx, cy)
            if kz > 0.05 and t > T_CHINE - 0.2: onde(c, kx, ky, t, T_CHINE, 20, 190, ENCRE, 6, 0.7)
            G.repere(c, *CANTON, cx, cy, R, lon0, lat0, "Équipe Monarque", ENCRE, "CN", entre(t, T_CHINE - 0.05, 0.42, 2.0), 1.0, 70)
        # dessiné en France → fabriqué comme prévu : deux petites cartes qui se répondent
        d = entre(t, T_DESSINE - 0.1, 0.45, 2.0)
        if d > 0:
            c.save(); c.translate(CX - 250, 700); c.rotate(-6); c.scale(d, d)
            cadre(c, -110, -140, 220, 280, 28); image_cover(c, "fiche-technique", -100, -130, 200, 200, 1.0, 0.5, 0.3, 20)
            pilule(c, "Dessiné en France", 0, 108, 1.0, "pencil", ENCRE, BLANC, 20)
            c.restore()
        f = entre(t, T_FABRIQUE - 0.1, 0.45, 2.0)
        if f > 0:
            c.save(); c.translate(CX + 250, 700); c.rotate(6); c.scale(f, f)
            cadre(c, -110, -140, 220, 280, 28, accent=BEIGE if t > T_PREVU else None); image_cover(c, "produits/veste-zip-marine", -100, -130, 200, 200, 1.0, 0.5, 0.4, 20)
            pilule(c, "Fabriqué comme prévu", 0, 108, 1.0, "badge-check", BEIGE, ENCRE, 20)
            c.restore()
            coche(c, CX + 340, 580, 34, entre(t, T_PREVU - 0.05, 0.35, 2.4), BEIGE)
            if t > T_PREVU: eclats(c, CX + 250, 700, t, T_PREVU, 12, 300, cols=[BEIGE, BEIGE2, ENCRE], graine=13)
        titre2(c, t, "UNE CULTURE PRODUIT", "FRANÇAISE", T_UNEC - 0.05, T_ETEQ - 0.1, ENCRE, T_FRANC - 0.1)
        titre2(c, t, "ET UNE ÉQUIPE", "PRÉSENTE EN CHINE", T_ETEQ - 0.1, T_POUR - 0.1, ENCRE, T_EQUIPE - 0.05)
        titre2(c, t, "DESSINÉ EN FRANCE,", "FABRIQUÉ COMME PRÉVU.", T_POUR - 0.1, t1, BEIGE, T_FABRIQUE - 0.1)


# ─────────────────────────────────────────── 9 · vous gardez l'idée, nous en faisons un produit
def scene_idee_produit(c, t):
    t0, t1 = T_VOUS - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="bas", sor="recul", d_in=0.35, d_out=0.4, cy=960)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), cx=CX, cy=1000)
        CW, CH = 320, 460
        u1 = entre(t, T_VOUS, 0.5, 1.6)
        u2 = prog(t, T_NOUS - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_NOUS - 0.1 else 0.0
        plans = []
        if u1 > 0: plans.append(Plan(coins((-185, 0, 0), CW, CH, ay=12), CW, CH, carte_media("fiche-technique", False, t0, "Votre idée", "lightbulb", None, fy=0.3), borne(u1 * 3)))
        if u2 > 0: plans.append(Plan(coins((185, 0, mix(1400, 0, min(u2, 1.05))), CW, CH, ay=-12), CW, CH, carte_media("rushes/trench", True, T_NOUS - 0.3, "Votre produit", "shirt", BEIGE, fond_=BEIGE, col=ENCRE), borne(u2 * 3)))
        scene3d(c, cam, plans)
        f = prog(t, T_FAISONS - 0.1, 0.5, entreeSortie)
        if f > 0:
            pe = peinture(BEIGE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=8); pe.setStrokeCap(skia.Paint.kRound_Cap); pe.setPathEffect(skia.DashPathEffect.Make([16, 12], -t * 90))
            c.drawLine(CX - 60, 1000, mix(CX - 60, CX + 60, f), 1000, pe)
            s = entre(t, T_FAISONS + 0.2, 0.4, 2.2)
            if s > 0:
                c.save(); c.translate(CX, 1000); c.scale(s, s)
                disque(c, 0, 0, 54, BLANC, 1, (10, 26, 0.25)); anneau(c, 0, 0, 54, BEIGE, 4); logo(c, 0, 0, 84, False)
                c.restore()
        if t > T_PRODUITF - 0.05: eclats(c, CX + 185, 1000, t, T_PRODUITF, 14, 360, cols=[BEIGE, BEIGE2, ENCRE], graine=14)
        titre2(c, t, "VOUS GARDEZ", "L'IDÉE.", T_VOUS - 0.05, T_NOUS - 0.1, ENCRE, T_LIDEE - 0.1)
        titre2(c, t, "NOUS EN FAISONS", "UN PRODUIT.", T_NOUS - 0.1, T_FIN - 0.05, BEIGE, T_FAISONS - 0.05)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8); son(T_ENVOYE - 0.05, "swipe", -10); son(T_ENVOYE, "pop", -10)
son(T_RENVOYE - 0.1, "whoosh_long", -9); son(T_INTERP, "impact", -5); son(T_INTERP + 0.03, "croc", -8)
son(T_MATIERE - 0.12, "whoosh", -9)
for tk, tv, _, _, _, _, _ in ECARTS: son(tk - 0.12, "whoosh_court", -10); son(tv - 0.05, "croc", -8)
son(T_ET - 0.12, "whoosh_bas", -8); son(T_ET, "impact_doux", -9); son(T_POURQUOI - 0.05, "pop", -9)
son(T_PRODUIT - 0.1, "whoosh_court", -10); son(T_PRODUIT, "impact_doux", -9); son(T_RESS - 0.05, "croc", -8); son(T_RESS, "impact", -8)
son(T_PARCE - 0.12, "whoosh_long", -7); son(T_PARCE, "impact", -3); son(T_PHOTO2 + 0.2, "impact", -5)
son(T_ENTRE - 0.1, "whoosh_bas", -8); son(T_MANQUE - 0.1, "pop", -9)
for i in range(6): son(T_MANQUE + 0.2 + i * 0.25, "tick", -16)
son(T_SAUTENT - 0.1, "pop", -10); son(T_DEVEL - 0.1, "whoosh_court", -9); son(T_DEVEL, "impact", -5); son(T_DEVEL + 0.03, "ching", -9)
son(T_UN - 0.12, "whoosh", -9)
for tk, tv, _, _, _, _, _, _ in TUILES: son(tk - 0.15, "whoosh_court", -11); son(tk, "pop", -11); son(tv + 0.05, "check", -10)
son(T_PASE - 0.05, "pop", -10); son(T_ECRAN - 0.05, "croc", -9)
son(T_CEST - 0.05, "whoosh_bas", -8); son(T_MQ - 0.12, "whoosh_long", -7); son(T_MQ + 0.05, "impact", -4); son(T_MQ + 0.08, "ching", -9); son(T_UNEC - 0.3, "whoosh_bas", -8)
son(T_CULTURE - 0.05, "pop", -10); son(T_ETEQ - 0.1, "montee", -12); son(T_CHINE - 0.15, "impact_doux", -6); son(T_CHINE, "ching", -9)
son(T_DESSINE - 0.1, "pop", -9); son(T_FABRIQUE - 0.1, "pop", -9); son(T_PREVU - 0.05, "check", -8); son(T_PREVU, "ching", -10)
son(T_VOUS - 0.12, "whoosh", -9); son(T_VOUS, "impact_doux", -9); son(T_NOUS - 0.1, "whoosh_court", -10); son(T_NOUS, "impact_doux", -9)
son(T_FAISONS - 0.1, "montee", -13); son(T_FAISONS + 0.2, "impact_doux", -8); son(T_FAISONS + 0.25, "ching", -10); son(T_PRODUITF, "check", -9)
sons_signature_mq(son, T_FIN, T_BOUTON)
for tl in (T_L1, T_L2): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_RENVOYE - 0.1, T_RENVOYE + 0.4), (T_MATIERE - 0.15, T_MATIERE + 0.25), (T_ET - 0.15, T_ET + 0.25), (T_PARCE - 0.1, T_PARCE + 0.3),
             (T_ENTRE - 0.15, T_ENTRE + 0.3), (T_DEVEL - 0.1, T_DEVEL + 0.3), (T_UN - 0.15, T_UN + 0.25), (T_MQ - 0.1, T_MQ + 0.3),
             (T_UNEC - 0.3, T_UNEC + 0.2), (T_VOUS - 0.15, T_VOUS + 0.25), (T_NOUS - 0.15, T_NOUS + 0.25), (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_INTERP, ROUGE, 0.07), (T_RESS, ROUGE, 0.06), (T_PARCE, "#FFFFFF", 0.08), (T_DEVEL, BEIGE, 0.08), (T_MQ + 0.05, "#FFFFFF", 0.1),
                    (T_CHINE - 0.15, BEIGE, 0.07), (T_PREVU, BEIGE, 0.06)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_clair(c, t)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_ecarts(c, t); scene_pourquoi(c, t)
    r1 = flash_noir(c, t, T_PARCE, T_ENTRE, "UNE PHOTO", "N'EST PAS UN PRODUIT.")
    with Balance(c, t, 0.8):
        if r1 < 2100: scene_etape(c, t); scene_tuiles(c, t)
    r2 = logo_monarque(c, t, T_MQ, T_UNEC - 0.3, T_FIN)
    with Balance(c, t, 0.8):
        if r2 < 2100: scene_france_chine(c, t); scene_idee_produit(c, t)
    signature_mq(c, t, T_FIN, MEDIAS, [("Une idée se dessine.", T_L1, 46, ENCRE), ("Un produit se développe.", T_L2, 46, BEIGE)], T_BOUTON, cy=800)
    K.dessine_eclairs(c, t)
    cache = (T_PARCE - 0.1 < t < T_ENTRE - 0.05) or (T_MQ - 0.1 < t < T_UNEC - 0.05) or t > T_FIN - 0.1
    if not cache: SOUS.dessine(c, t, BLANC if max(r1 or 0, r2 or 0) > 1200 else ENCRE)
