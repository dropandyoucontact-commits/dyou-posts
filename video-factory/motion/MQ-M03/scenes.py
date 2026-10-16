"""MQ-M03 « Votre usine vous dit oui à tout » — MONARQUE, version fond noir (15/10/2026).

Même thème que MQ-M02 (produire en Chine sans personne sur place), autre accroche et autres paroles : le fournisseur
qui dit oui à tout, la réception qui ne ressemble pas à la commande (trench long commandé / court reçu), puis Monarque
présent dans l'atelier pendant la production. Style noir de CB-M14 (cases fines, titres lettre par lettre), accent
beige trench, logo blanc du client, globe blanc sculpté sur fond noir. Voix Tomy 4,35 mots/s, pauses resserrées.
Aucun chiffre inventé ; l'échange fournisseur porte la mention « Échange illustratif ».
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
import monarque


def titre(c, t, txt, t0, t1, couleur=BLANC, **k):
    monarque.titre(c, t, txt, t0, t1, couleur=couleur, **k)

polices(P)
K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.6, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresEncre(K, fusions={(113, 114, 115, 116): "monarqueprod.com."}, y=1440, larg=900, taille=54, fam="gras", max_mots=5)

LONG, COURT = "trench-long", "trench-court"
T_PB = TW(9)
T_OUI = [TW(13), TW(17), TW(21)]
T_RECEP, T_COUPE, T_FINI, T_CLI = TW(25), TW(29), TW(33), TW(36)
T_PASCN, T_DIST, T_PERS = TW(40), TW(47), TW(52)
T_MQ, T_BUR, T_CN = TW(56), TW(62), TW(66)
T_SEL, T_DEV, T_NEG = TW(67), TW(71), TW(75)
T_PEND, T_ATEL, T_APRES = TW(79), TW(83), TW(87)
T_CTRL, T_CORR, T_EXP = TW(89), TW(91), TW(96)
T_MAIN, T_AVION = TW(98), TW(105)
T_FIN, T_URL = TW(108), TW(113)


# ─────────────────────────────────────────── 1 · hook : oui à tout
BULLES = [("没问题！", "cjk", -0.9), ("OK, no problem", "gras", -0.5), ("可以可以", "cjk", 0.3), ("Yes, sure!", "gras", 0.65),
          ("没问题", "cjk", 1.0)]


def hook(c, t):
    g = Groupe(c, t, -1, T_OUI[0], ent="aucune", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        lettres(c, "OUI À TOUT", 540, 330, 120, t, -0.6, "ressort", fam="archivo", grad=False, couleur=BLANC, decal=0.035, track=-0.01)
        barre_u = prog(t, T_PB + 0.1, 0.22, sortie)
        if barre_u > 0:
            trait(c, 190, 405, 190 + 700 * barre_u, 405, ROUGE, 12)
        rouge = prog(t, T_PB, 0.3)
        a = entre(t, -0.4, 0.5, 1.4)
        cadre(c, 140, 560, 800, 760, 40, True, ROUGE if rouge > 0.5 else None, borne(a * 3))
        with Calque(c, borne(a * 3)):
            disque(c, 210, 630, 34, "#1E1D24"); icone(c, "factory", 210, 630, 36, BEIGE, 2.4)
            texte(c, "Votre usine", 262, 630 - hauteurLigne(34, "gras") / 2, 34, BLANC, "gras", track=-0.01)
            texte(c, "en ligne", 262 + largeur("Votre usine", 34, "gras", -0.01) + 18, 630 - hauteurLigne(26, "gras") / 2 + 3, 26, VERT, "gras", track=-0.01)
            trait(c, 170, 690, 910, 690, "#FFFFFF", 2, 0.12)
            for k, (txt, fam, dt) in enumerate(BULLES):
                u = entre(t, 0.05 + dt, 0.35, 2.0)
                if u <= 0: continue
                T = 44
                tw = largeur(txt, T, fam, -0.01); bw, bh = tw + 64, T * 2.0
                x, y = 180, 730 + k * 112
                c.save(); c.translate(x, y + bh); c.scale(mix(0.3, 1, u), mix(0.3, 1, u)); c.translate(-x, -(y + bh))
                with Calque(c, borne(u * 3)):
                    rrect(c, x, y, bw, bh, 34, mix_col(rouge), 1.0)
                    texte(c, txt, x + 32, y + bh / 2 - hauteurLigne(T, fam) / 2, T, BLANC, fam, track=-0.01)
                    coche(c, x + bw + 40, y + bh / 2, 22, 1.0, VERT if rouge < 0.5 else ROUGE)
                c.restore()
            texte_centre(c, "Échange illustratif", 540, 1290, 22, GRIS, "demi", 0.8, 0)
        tampon_n(c, "LE PROBLÈME", 620, 1010, t, TW(12) + 0.05, ROUGE, -8, 70)


def mix_col(u):
    """bulle grise qui rougit quand « c'est exactement le problème »"""
    if u <= 0: return "#24232B"
    return "#24232B" if u < 0.5 else "#5A1F25"


# ─────────────────────────────────────────── 2 · oui pour la matière, le délai, le prix
OUIS = [("LA MATIÈRE", "layers", LONG, None), ("LE DÉLAI", "calendar-clock", "rushes/machines", 1.2), ("LE PRIX", "euro", "rushes/bureau", 1.1)]


def ouis(c, t):
    g = Groupe(c, t, T_OUI[0] - 0.1, T_RECEP, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        for k, (lab, ic, nom, vit) in enumerate(OUIS):
            t1 = T_OUI[k + 1] - 0.1 if k < 2 else T_RECEP - 0.1
            titre(c, t, "OUI · " + lab, T_OUI[k], t1, couleur=BLANC if k % 2 == 0 else BEIGE2, taille=92)
        actif = max([k for k in range(3) if t >= T_OUI[k] - 0.12] or [-1])
        for k, (lab, ic, nom, vit) in enumerate(OUIS):
            u = entre(t, T_OUI[0] - 0.1 + 0.08 * k, 0.45, 1.6)
            if u <= 0: continue
            y = 560 + k * 270; on = k == actif
            dim = 1.0 if k <= actif else 0.4
            c.save(); c.translate((1 - u) * 400, 0)
            if vit is None:
                media(c, t, nom, 90, y, 900, 250, borne(u * 3) * dim, 1.0, zoom=4.0, fx=0.4, fy=0.62, sombre=True, accent=BEIGE if on else None)
            else:
                media(c, t, nom, 90, y, 900, 250, borne(u * 3) * dim, 1.0, video_t0=T_OUI[0], vitesse=vit, sombre=True, accent=BEIGE if on else None)
            c.restore()
            puce_n(c, lab.split(" ", 1)[1].capitalize(), 90 + 40 + largeur(lab, 32, "gras") / 2 + 30, y + 52, entre(t, T_OUI[k] - 0.1, 0.4, 2.2), ic, BEIGE, 32)
            tampon_n(c, "OUI", 880, y + 175, t, T_OUI[k] + 0.12, VERT, -8, 46)


# ─────────────────────────────────────────── 3 · à la réception : la coupe, les finitions, vos clients qui attendent
def reception(c, t):
    g = Groupe(c, t, T_RECEP - 0.1, T_PASCN, ent="bas", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "À LA RÉCEPTION", T_RECEP, T_CLI - 0.1)
        titre(c, t, "VOS CLIENTS ATTENDENT", T_CLI - 0.05, T_PASCN - 0.1, couleur=BEIGE2, taille=84)
        sw = prog(t, T_CLI - 0.15, 0.4, entreeSortie)
        if sw < 1:
            with Calque(c, 1 - sw):
                a = entre(t, T_RECEP - 0.1, 0.5, 1.5)
                media(c, t, LONG, 70, 600, 440, 720, borne(a * 3), mix(0.6, 1, a), zoom=1.14, sombre=True, accent=VERT)
                puce_n(c, "Commandé", 290, 1385, entre(t, T_RECEP + 0.2, 0.4, 2.2), "check", VERT, 32)
                if t >= TW(28) - 0.1:
                    u = prog(t, TW(28) - 0.1, 0.28, entree)
                    sh = secousse(t, TW(28) + 0.18, 14, 0.32)
                    c.save(); c.translate(sh[0], sh[1] + mix(-1500, 0, u))
                    media(c, t, COURT, 570, 600, 440, 720, 1.0, 1.0, zoom=1.12, sombre=True, accent=ROUGE, rot=mix(-10, 2, u))
                    c.restore()
                    puce_n(c, "Reçu", 790, 1385, entre(t, TW(28) + 0.3, 0.4, 2.2), "x", ROUGE, 32)
                # la coupe : la ligne de l'ourlet commandé, qui ne tombe plus au même endroit
                lc = prog(t, T_COUPE + 0.05, 0.4, entreeSortie)
                if lc > 0:
                    trait(c, 110, 1200, 110 + 880 * lc, 1200, ROUGE, 5, 1.0, [16, 12])
                    puce_n(c, "Coupe", 790, 1130, entre(t, TW(31), 0.4, 2.2), "scissors", ROUGE, 30)
                for k, (dx, dy) in enumerate([(-50, -20), (60, 20), (-45, 90)]):
                    q = prog(t, T_FINI + 0.05 + 0.1 * k, 0.3, lambda v: rebond(v, 2))
                    if q > 0: anneau(c, 790 + dx, 900 + dy, 42 * q, ROUGE, 6, borne(q * 2))
                puce_n(c, "Finitions", 790, 760, entre(t, TW(34) + 0.05, 0.4, 2.2), "search", ROUGE, 30)
        if sw > 0:
            b = entre(t, T_CLI - 0.1, 0.5, 1.4)
            media(c, t, "shop", 190, 580, 700, 780, borne(b * 3), mix(0.7, 1, b), zoom=1.05 + 0.04 * max(0, t - T_CLI), fy=0.4, sombre=True,
                  voile=("#000000", 0.25))
            hb = entre(t, TW(39) - 0.1, 0.45, 2.0)
            if hb > 0:
                c.save(); c.translate(540, 960); c.rotate(180 * prog(t, TW(39) + 0.3, 0.6, entreeSortie)); c.scale(hb, hb)
                disque(c, 0, 0, 90, "#0B0A0F", 0.9); anneau(c, 0, 0, 90, BEIGE, 3, 0.9); icone(c, "hourglass", 0, 0, 90, BEIGE, 2.6)
                c.restore()
            puce_n(c, "En attente", 540, 1240, entre(t, TW(39), 0.4, 2.2), "clock", BEIGE, 34)


# ─────────────────────────────────────────── 4 · pas la Chine : la distance, personne sur place (globe)
def globe_distance(c, t):
    if t < T_PASCN or t > T_MQ + 0.3: return
    o = prog(t, T_MQ - 0.15, 0.3, entree)
    titre(c, t, "PAS LA CHINE", T_PASCN, T_DIST - 0.1, couleur=BLANC)
    titre(c, t, "LA DISTANCE", T_DIST - 0.05, T_PERS - 0.1, couleur=BEIGE2)
    titre(c, t, "PERSONNE SUR PLACE", T_PERS - 0.05, T_MQ, couleur=ROUGE, taille=86)
    a = entre(t, T_PASCN + 0.08, 0.7, 1.2)
    rot = prog(t, T_DIST - 0.1, 1.0, entreeSortie)
    lon0 = mix(98, 55, rot) + 3 * (t - T_PASCN); lat0 = mix(28, 38, rot)
    R = 400 * mix(0.7, 1, a) * mix(1, 0.5, o)
    cx, cy = 540, 990
    with Calque(c, borne(a * 3) * (1 - o)):
        lueur(c, cx, cy, R * 1.5, "#6F8CFF", 0.12)
        GL.dessine_globe(c, lon0, lat0, cx, cy, R, sombre=True)
        kx, ky, kz = GL.projette(*CANTON, lon0, lat0, R, cx, cy)
        if kz > 0.05:
            epingle(c, kx, ky, "Usine", entre(t, T_PASCN + 0.2, 0.42, 2.0) * borne(kz * 4), BLANC, "CN", 80, 30, "#FFFFFF", ENCRE)
        ua = prog(t, T_DIST, 1.0, entreeSortie)
        if ua > 0:
            pa = arc_globe(c, lon0, lat0, cx, cy, R, CANTON, PARIS, ua, BEIGE, 6, 0.3)
            fx, fy, fz = GL.projette(*PARIS, lon0, lat0, R, cx, cy)
            if fz > 0.05:
                epingle(c, fx, fy, "Vous", entre(t, T_DIST + 0.8, 0.42, 2.0), BEIGE, "FR", 80, 30, BEIGE, ENCRE)
        b = entre(t, T_PERS - 0.05, 0.5, 1.5)
        if b > 0:
            media(c, t, "rushes/atelier", 600, 1040, 380, 300, borne(b * 3), mix(0.5, 1, b), video_t0=T_PERS, vitesse=1.1, sombre=True,
                  accent=ROUGE, voile=("#000000", 0.3), rot=3)
            croix(c, 950, 1060, 34, entre(t, TW(54), 0.35, 2.4))


# ─────────────────────────────────────────── 5 · MONARQUE, bureau en Chine
def monarque_s(c, t):
    if t < T_MQ - 0.2 or t > T_SEL + 0.4: return
    u = entre(t, T_MQ - 0.05, 0.5, 1.3)
    v = prog(t, T_BUR - 0.2, 0.45, entreeSortie)
    o = prog(t, T_SEL - 0.15, 0.4, entree)
    if v < 1:
        lueur(c, 540, 960, 700 * u * (1 - v), BEIGE, 0.2)
        rayons(c, 540, 960, t, 1000, 0.08 * u * (1 - v), 16, BEIGE2)
        eclats(c, 540, 960, t, T_MQ + 0.1, 16, 380, [BEIGE, BEIGE2, BLANC], graine=5)
        pt = puce_n(c, "Centrale d'achat française", 540, 1170, entre(t, TW(59), 0.4, 2.0) * (1 - v), "badge-check", BEIGE, 36)
    lw = mix(1.6, 1, u) * mix(860, 440, v)
    logo(c, 540, mix(940, 430, v) - 900 * o, lw, True, borne(u * 3) * (1 - o))
    a = entre(t, T_BUR - 0.1, 0.7, 1.2)
    if a > 0:
        lon0, lat0 = 108 + 2.5 * (t - T_BUR), 27
        R = 400 * mix(0.75, 1, a) * mix(1, 0.7, o)
        cx, cy = 540, 1000 + 900 * o
        with Calque(c, borne(a * 3) * (1 - o)):
            lueur(c, cx, cy, R * 1.5, "#6F8CFF", 0.12)
            GL.dessine_globe(c, lon0, lat0, cx, cy, R, sombre=True)
            kx, ky, kz = GL.projette(*CANTON, lon0, lat0, R, cx, cy)
            onde(c, kx, ky, t, T_CN, 20, 190, BEIGE, 6, 0.7)
            epingle(c, kx, ky, "Bureau Monarque", entre(t, T_CN - 0.05, 0.42, 2.0), BEIGE, "CN", 90, 30, BEIGE, ENCRE)
            b = entre(t, T_CN + 0.1, 0.5, 1.4)
            media(c, t, "rushes/bureau", 90, 1080, 330, 300, borne(b * 3), mix(0.5, 1, b), video_t0=T_CN, vitesse=1.0, sombre=True,
                  accent=BEIGE, rot=-3)


# ─────────────────────────────────────────── 6 · on sélectionne, on développe, on négocie
ETAPES = [("ON SÉLECTIONNE", "Usines", "factory", "rushes/machines", T_SEL), ("ON DÉVELOPPE", "Prototypes", "shirt", "rushes/couture", T_DEV),
          ("ON NÉGOCIE", "Pour vous", "heart-handshake", "rushes/trench", T_NEG)]


def etapes(c, t):
    g = Groupe(c, t, T_SEL - 0.1, T_PEND, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        for k, (tit, lab, ic, nom, t0) in enumerate(ETAPES):
            t1 = ETAPES[k + 1][4] - 0.1 if k < 2 else T_PEND - 0.1
            titre(c, t, tit, t0, t1, couleur=BLANC if k != 1 else BEIGE2)
        actif = max([k for k, e in enumerate(ETAPES) if t >= e[4] - 0.12] or [-1])
        for k, (tit, lab, ic, nom, t0) in enumerate(ETAPES):
            u = entre(t, T_SEL - 0.05 + 0.08 * k, 0.45, 1.6)
            if u <= 0: continue
            y = 560 + k * 270; on = k == actif
            c.save(); c.translate((1 - u) * 400, 0)
            media(c, t, nom, 90, y, 900, 250, borne(u * 3) * (1.0 if k <= actif else 0.4), 1.0, video_t0=T_SEL, vitesse=1.2, sombre=True,
                  accent=BEIGE if on else None)
            c.restore()
            puce_n(c, lab, 90 + 40 + largeur(lab, 32, "gras") / 2 + 50, y + 52, entre(t, t0 - 0.1, 0.4, 2.2), ic, BEIGE, 32)
            coche(c, 940, y + 200, 30, entre(t, t0 + 0.3, 0.35, 2.4))


# ─────────────────────────────────────────── 7 · pendant la production, dans l'atelier, pas après
def pendant(c, t):
    g = Groupe(c, t, T_PEND - 0.1, T_CTRL, ent="bas", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "PENDANT", T_PEND, T_APRES - 0.1, couleur=BEIGE2, taille=120)
        titre(c, t, "PAS APRÈS", T_APRES - 0.05, T_CTRL - 0.1, couleur=ROUGE, taille=120)
        a = entre(t, T_PEND - 0.05, 0.5, 1.4)
        media(c, t, "rushes/atelier", 140, 560, 800, 600, borne(a * 3), mix(0.7, 1, a), video_t0=T_PEND, vitesse=1.0, sombre=True,
              accent=BEIGE if t > T_ATEL else None)
        puce_n(c, "Dans l'atelier", 330, 640, entre(t, T_ATEL, 0.4, 2.2), "map-pin", BEIGE, 32)
        # la barre de production : Monarque est dedans, pas à la fin
        b = entre(t, T_PEND + 0.1, 0.45, 1.6)
        if b > 0:
            with Calque(c, borne(b * 3)):
                texte(c, "PRODUCTION", 140, 1210, 28, GRIS, "noir", track=0.08)
                rrect(c, 140, 1260, 800, 18, 9, "#FFFFFF", 0.12)
                f = prog(t, T_PEND + 0.1, T_APRES - T_PEND + 0.4, lin)
                rrect(c, 140, 1260, 800 * f, 18, 9, BEIGE)
                mx = 140 + 800 * min(f, 0.55)
                disque(c, mx, 1269, 26, BEIGE, 1, (6, 16, 0.4)); icone(c, "user-round", mx, 1269, 28, ENCRE, 2.4)
                texte(c, "MONARQUE", mx, 1300, 24, BEIGE, "noir", "centre", 0.06)
                disque(c, 940, 1269, 14, "#FFFFFF", 0.4)
                texte(c, "Après", 940, 1300, 24, GRIS, "gras", "centre", -0.01)
            croix(c, 940, 1269, 30, entre(t, T_APRES + 0.15, 0.35, 2.4))


# ─────────────────────────────────────────── 8 · on contrôle, on corrige, on expédie
PAS3 = [("CONTRÔLÉ", "scan-line", T_CTRL), ("CORRIGÉ", "wrench", T_CORR), ("EXPÉDIÉ", "truck", T_EXP)]


def expedition(c, t):
    g = Groupe(c, t, T_CTRL - 0.1, T_MAIN, ent="grand", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ON CONTRÔLE", T_CTRL, TW(93) - 0.1, couleur=BLANC, taille=110)
        titre(c, t, "ET SEULEMENT LÀ", TW(93) - 0.05, T_MAIN - 0.1, couleur=BEIGE2, taille=96)
        a = entre(t, T_CTRL - 0.05, 0.5, 1.4)
        media(c, t, "rushes/controle", 140, 560, 800, 560, borne(a * 3), mix(0.7, 1, a), video_t0=T_CTRL, vitesse=1.2, sombre=True,
              accent=VERT if t > T_EXP else None)
        for k, (lab, ic, t0) in enumerate(PAS3):
            u = entre(t, t0 - 0.1, 0.45, 1.8)
            if u <= 0: continue
            x = 200 + k * 340
            c.save(); c.translate(x, 1250); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            with Calque(c, borne(u * 3)):
                cadre(c, -150, -80, 300, 160, 30, True, VERT if k == 2 else BEIGE)
                icone(c, ic, 0, -26, 54, VERT if k == 2 else BEIGE, 2.6)
                texte(c, lab, 0, 22, 30, BLANC, "noir", "centre", 0.02)
            c.restore()
            if k < 2:
                ua = prog(t, PAS3[k + 1][2] - 0.2, 0.25, sortie)
                if ua > 0: trait(c, x + 155, 1250, x + 155 + 30 * ua, 1250, BEIGE, 4)
        tampon_n(c, "CONFORME", 540, 840, t, T_EXP + 0.25, VERT, -8, 66)


# ─────────────────────────────────────────── 9 · vous gardez la main, sans prendre l'avion
def main_(c, t):
    g = Groupe(c, t, T_MAIN - 0.1, T_FIN, ent="droite", sor="recul", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VOUS GARDEZ LA MAIN", T_MAIN, T_AVION - 0.1, taille=90)
        titre(c, t, "SANS PRENDRE L'AVION", T_AVION - 0.05, T_FIN - 0.1, couleur=BEIGE2, taille=86)
        a = entre(t, T_MAIN - 0.05, 0.5, 1.4)
        media(c, t, LONG, 250, 560, 580, 760, borne(a * 3), mix(0.6, 1, a), zoom=1.12 + 0.02 * max(0, t - T_MAIN), sombre=True, accent=VERT)
        puce_n(c, "Votre collection", 540, 640, entre(t, TW(103), 0.4, 2.2), "check", VERT, 34)
        b = entre(t, T_AVION, 0.45, 2.0)
        if b > 0:
            x = mix(1200, 860, prog(t, T_AVION, 0.5, sortie))
            c.save(); c.translate(x, 1250); c.scale(mix(0.4, 1, b), mix(0.4, 1, b))
            disque(c, 0, 0, 96, "#0B0A0F", 0.92); anneau(c, 0, 0, 96, ROUGE, 3, 0.9)
            icone(c, "plane", 0, 0, 96, BLANC, 2.4)
            c.restore()
            u = prog(t, T_AVION + 0.35, 0.2, sortie)
            if u > 0: trait(c, x - 70, 1250 - 70, x - 70 + 140 * u, 1250 - 70 + 140 * u, ROUGE, 10)


# ─────────────────────────────────────────── 10 · fin
def fin(c, t):
    if t < T_FIN - 0.1: return
    carton_fin(c, t, T_FIN, T_URL, sombre=True)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9)
for txt, fam, dt in BULLES:
    if dt > 0: son(0.05 + dt, "message_in", -11)
son(T_PB + 0.1, "croc", -7); son(TW(12) + 0.05, "tampon", -5)
son(T_OUI[0] - 0.15, "whoosh", -8)
for t0 in T_OUI: son(t0 - 0.1, "pop", -10); son(t0 + 0.12, "tampon", -8)
son(T_RECEP - 0.1, "whoosh_bas", -8); son(T_RECEP + 0.2, "check", -11)
son(TW(28) - 0.1, "whoosh_court", -9); son(TW(28) + 0.18, "impact", -5); son(TW(28) + 0.3, "pop", -10)
son(T_COUPE + 0.05, "swipe", -10); son(TW(31), "pop", -10)
for k in range(3): son(T_FINI + 0.05 + 0.1 * k, "pop", -12)
son(T_CLI - 0.15, "whoosh", -8); son(TW(39) - 0.1, "impact_doux", -8); son(TW(39), "pop", -10)
son(T_PASCN - 0.1, "whoosh_long", -8); son(T_PASCN + 0.2, "pop", -10); son(T_DIST, "whoosh_long", -9); son(T_DIST + 0.8, "pop", -10)
son(T_PERS - 0.05, "whoosh_court", -9); son(TW(54), "croc", -8)
son(T_MQ - 0.15, "montee", -10); son(T_MQ + 0.05, "impact", -4); son(T_MQ + 0.1, "ching", -8); son(TW(59), "pop", -10)
son(T_BUR - 0.2, "whoosh_bas", -8); son(T_CN - 0.05, "impact_doux", -7); son(T_CN + 0.1, "pop", -10)
son(T_SEL - 0.15, "whoosh", -8)
for e in ETAPES: son(e[4] - 0.1, "pop", -10); son(e[4] + 0.3, "check", -12)
son(T_PEND - 0.1, "whoosh_bas", -8); son(T_ATEL, "pop", -10); son(T_APRES - 0.05, "impact_doux", -7); son(T_APRES + 0.15, "croc", -8)
son(T_CTRL - 0.1, "whoosh", -8)
for lab, ic, t0 in PAS3: son(t0 - 0.1, "pop", -9); son(t0 + 0.1, "check", -12)
son(T_EXP + 0.25, "tampon", -5)
son(T_MAIN - 0.1, "whoosh_court", -8); son(TW(103), "check", -10); son(T_AVION, "whoosh", -9); son(T_AVION + 0.35, "croc", -8)
son(T_FIN - 0.1, "montee", -11); son(T_FIN + 0.05, "impact", -5); son(T_URL - 0.15, "pop", -9); son(T_URL + 0.45, "clic", -5)
son(T_URL + 0.5, "ching", -8)

for a, b in [(T_OUI[0] - 0.15, T_OUI[0] + 0.3), (T_RECEP - 0.15, T_RECEP + 0.3), (TW(28) - 0.1, TW(28) + 0.2), (T_CLI - 0.15, T_CLI + 0.3),
             (T_MQ - 0.15, T_MQ + 0.3), (T_SEL - 0.15, T_SEL + 0.3), (T_PEND - 0.15, T_PEND + 0.3), (T_CTRL - 0.15, T_CTRL + 0.3),
             (T_MAIN - 0.15, T_MAIN + 0.3), (T_FIN - 0.1, T_FIN + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(12) + 0.05, ROUGE, 0.08), (TW(28) + 0.18, ROUGE, 0.07), (T_MQ + 0.05, BEIGE, 0.12), (T_EXP + 0.25, VERT, 0.07)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_sombre(c, t, battement(t, T_MQ + 0.05, 1, 0.6) - 1)
    hook(c, t); ouis(c, t); reception(c, t); globe_distance(c, t); monarque_s(c, t)
    etapes(c, t); pendant(c, t); expedition(c, t); main_(c, t); fin(c, t)
    K.dessine_eclairs(c, t)
    if not (T_MQ - 0.1 < t < TW(57) - 0.05) and t < T_FIN - 0.1:
        SOUS.dessine(c, t, BLANC)
