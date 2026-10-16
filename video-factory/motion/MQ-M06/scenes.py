"""MQ-M06 « Vous n'avez pas besoin d'aller en Chine » — script du client (hook 3), 16/10/2026.
Recette validée MQ-M05 (reference/monarque.md) : fond clair, Archivo Black, voix Tomy 4,2 mots/s, −13 LUFS,
globe en points (Chine allumée), graphique à modèles différents, carton à la signature du client."""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import agence
from studio import lettres, Groupe, eclats, entre, SousTitresEncre, curseur
from monarque import *
from monarque import VERT, ROUGE
from mq import *

polices(P)
K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.7, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresEncre(K, y=1440, larg=900, taille=54, fam="gras", max_mots=5)

T_ATT, T_DEP, T_MIL, T_FRA = TW(11), TW(18), TW(20), TW(28)
T_VOY, T_TEMPS, T_SURT, T_CHER = TW(32), TW(51), TW(57), TW(60)
T_APRES, T_CERT, T_PART = TW(61), TW(65), TW(70)
T_AVEC, T_MQ, T_ACC = TW(75), TW(76), TW(85)
T_FAB, T_DEVP, T_PREP = TW(92), TW(94), TW(100)
T_PRES, T_ECO, T_SANS, T_KM = TW(109), TW(111), TW(119), TW(126)
T_VOUS, T_COLL, T_ECH, T_DEVS, T_PROD, T_FR2 = TW(129), TW(133), TW(137), TW(141), TW(145), TW(146)
T_TPS, T_BUDG, T_GRAND, T_MULT, T_COMM = TW(149), TW(153), TW(158), TW(161), TW(167)
T_ALORS, T_RES, T_QUEST, T_PARTIR, T_OU, T_BONS = TW(171), TW(174), TW(177), TW(181), TW(186), TW(191)
T_FIN, T_DEVM, T_PRODM, T_CONT = TW(193), TW(194), TW(196), TW(199)


# ─────────────────────────────────────────── 1 · hook : aller en Chine ? Attendez !
def piece(c, x, y, r, a=1.0):
    disque(c, x, y, r, ENCRE, a, (6, 16, 0.25)); anneau(c, x, y, r * 0.78, BEIGE, 3, a); icone(c, "euro", x, y, r * 1.0, BLANC, 2.6, a)


def hook(c, t):
    if t > T_VOY + 0.4: return
    g = Groupe(c, t, -1, T_VOY, ent="aucune", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ALLER EN CHINE ?", -0.55, T_ATT - 0.1)
        titre(c, t, "ATTENDEZ !", T_ATT - 0.05, T_DEP - 0.1, couleur=ROUGE, taille=120)
        titre(c, t, "DES MILLIERS D'EUROS", T_DEP, T_FRA - 0.1, couleur=ROUGE, taille=84)
        titre(c, t, "DEPUIS LA FRANCE", T_FRA - 0.05, T_VOY - 0.1)
        # la carte d'embarquement, déjà là à l'image 0 ; elle se fige sur « Attendez ! », puis s'efface devant la France
        sh = secousse(t, T_ATT, 22, 0.45)
        mon = prog(t, T_DEP - 0.15, 0.45, entreeSortie)
        part = prog(t, T_FRA - 0.2, 0.4, entree)
        flot = 10 * math.sin(t * 2.4) if t < T_ATT else 0
        a0 = entre(t, -0.35, 0.5, 1.5)
        billet(c, 540 + sh[0] - 900 * part, mix(880, 700, mon) + flot + sh[1], 900 * mix(1, 0.8, mon), borne(a0 * 3),
               mix(-5, -2, mon), mix(0.8, 1, a0))
        if t < T_ATT + 0.1:
            # les fournisseurs à trouver, déjà là à l'image 0
            for k in range(3):
                u = entre(t, -0.3 + 0.08 * k, 0.4, 2.0) * (1 - prog(t, T_ATT - 0.1, 0.2))
                if u <= 0: continue
                x = 300 + k * 240
                c.save(); c.translate(x, 1215); c.scale(u, u)
                disque(c, 0, 0, 76, BLANC, 1, (10, 26, 0.18)); icone(c, "factory", 0, 0, 70, ENCRE, 2.4)
                q = entre(t, TW(10) - 0.1 + 0.08 * k, 0.35, 2.6)
                if q > 0: disque(c, 52, -52, 26 * q, ROUGE); texte_centre(c, "?", 52, -50, 34 * q, BLANC, "noir")
                c.restore()
            pilule(c, "Les bons fournisseurs ?", 540, 1345, entre(t, TW(7) - 0.1, 0.4, 2.2) * (1 - prog(t, T_ATT - 0.1, 0.2)), "search", ENCRE, BLANC, 30)
        # la main qui arrête tout
        h = entre(t, T_ATT - 0.05, 0.35, 2.6) * (1 - mon)
        if h > 0:
            c.save(); c.translate(540 + sh[0], 1230); c.scale(h, h)
            disque(c, 0, 0, 120, ROUGE, 1, (14, 34, 0.3)); icone(c, "hand", 0, 0, 120, BLANC, 2.6)
            c.restore()
        # les pièces qui tombent
        if T_MIL - 0.3 < t < T_FRA + 0.3:
            for k in range(14):
                t0 = T_MIL - 0.2 + 0.07 * k
                if t < t0: continue
                d = t - t0
                x = 160 + (k * 263) % 760 + 30 * math.sin(k)
                y = 820 + 900 * d * d + 200 * d
                if y > 1400: y = 1400 - (k % 3) * 40
                piece(c, x, y, 46, borne((T_FRA + 0.1 - t) * 4))
        # la France : son studio
        b = entre(t, T_FRA - 0.1, 0.5, 1.5)
        if b > 0:
            media(c, t, "studio", 140 + 900 * (1 - b), 580, 800, 760, borne(b * 3), 1.0, zoom=1.0, fy=0.5, accent=ENCRE)
            c.save(); c.translate(900 * (1 - b), 0)
            rrect(c, 200, 640, 330, 84, 42, ENCRE, 1, (10, 26, 0.25)); drapeau(c, "FR", 228, 662, 58, 40, 6)
            texte(c, "En France", 300, 682 - hauteurLigne(32) / 2, 32, BLANC, "noir")
            c.restore()
            coche(c, 880, 640, 40, entre(t, TW(31) - 0.05, 0.35, 2.4))


# ─────────────────────────────────────────── 2 · le voyage : tout ce que ça coûte
LIGNES = [("plane", "Billet d'avion", TW(33)), ("hotel", "Hôtel", TW(35)), ("car-taxi-front", "Déplacements", TW(37)),
          ("calendar", "Semaines sur place", TW(39)), ("factory", "Rencontrer des usines", TW(45)), ("package", "Tester des fournisseurs", TW(48))]


def voyage(c, t):
    g = Groupe(c, t, T_VOY - 0.1, T_APRES, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "LE VOYAGE", T_VOY, T_TEMPS - 0.1)
        titre(c, t, "DU TEMPS", T_TEMPS - 0.05, T_SURT - 0.1)
        titre(c, t, "ET ÇA COÛTE CHER", T_SURT - 0.05, T_APRES - 0.1, couleur=ROUGE)
        a = entre(t, T_VOY - 0.05, 0.5, 1.4)
        c.save(); c.translate(540, 960); c.scale(mix(0.6, 1, a), mix(0.6, 1, a)); c.translate(-540, -960)
        with Calque(c, borne(a * 3)):
            cadre(c, 100, 560, 880, 800, 44)
            texte(c, "VOTRE VOYAGE EN CHINE", 150, 610, 32, ENCRE, "noir", track=0.06)
            trait(c, 150, 670, 930, 670, "#E3E0DB", 3)
            for k, (ic, lab, t0) in enumerate(LIGNES):
                u = entre(t, t0 - 0.1, 0.35, 1.8)
                if u <= 0: continue
                y = 700 + k * 86
                with Calque(c, borne(u * 3)):
                    c.save(); c.translate(-60 * (1 - u), 0)
                    disque(c, 185, y + 34, 30, "#EFEDEA"); icone(c, ic, 185, y + 34, 32, ENCRE, 2.4)
                    texte(c, lab, 235, y + 34 - hauteurLigne(32, "gras") / 2, 32, ENCRE, "gras", track=-0.01)
                    texte(c, "€€€", 920 - largeur("€€€", 34, "noir"), y + 34 - hauteurLigne(34) / 2, 34, ROUGE, "noir")
                    c.restore()
            # total
            tt = entre(t, T_SURT - 0.05, 0.4, 1.8)
            if tt > 0:
                trait(c, 150, 1228, 930, 1228, ENCRE, 4, borne(tt * 3))
                texte(c, "TOTAL", 150, 1262, 40, ENCRE, "archivo", alpha=borne(tt * 3))
                n = int(mix(1, 7, prog(t, T_SURT, T_CHER - T_SURT + 0.2, lin)))
                s_ = "€" * n
                texte(c, s_, 930 - largeur(s_, 46, "noir"), 1258, 46, ROUGE, "noir", alpha=borne(tt * 3))
        c.restore()
        # le temps qui file
        h = entre(t, T_TEMPS - 0.1, 0.4, 2.0)
        if h > 0:
            horloge(c, 860, 620, 96, 2 * math.pi * 2.2 * max(0, t - T_TEMPS), h)
        tampon(c, "CHER", 760, 1100, t, T_CHER + 0.05, 70, ROUGE, -9)


# ─────────────────────────────────────────── 3 · et après ça, les bons partenaires ?
DW, DH, DG = 316, 562, 12


def partenaires(c, t):
    g = Groupe(c, t, T_APRES - 0.1, T_MQ, ent="bas", sor="zoom", cy=960)
    if not g.visible or t > T_MQ + 0.3: return
    with g:
        titre(c, t, "ET APRÈS ÇA ?", T_APRES, T_CERT - 0.1)
        titre(c, t, "LES BONS PARTENAIRES ?", T_CERT - 0.05, T_MQ - 0.1, taille=80)
        x0 = (1080 - 3 * DW - 2 * DG) / 2
        sh = secousse(t, TW(74), 14, 0.4)
        for k, nom in enumerate(["rushes/machines", "rushes/atelier", "rushes/bureau"]):
            u = entre(t, T_APRES + 0.08 * k, 0.45, 1.6)
            if u <= 0: continue
            x = x0 + k * (DW + DG)
            c.save(); c.translate(sh[0] * (1 if k != 1 else -1), (1 - u) * 400)
            media(c, t, nom, x, 590, DW, DH, borne(u * 3), 1.0, video_t0=T_APRES, vitesse=1.2, r=30, pad=10, voile=("#FFFFFF", 0.2))
            q = entre(t, T_PART - 0.15 + 0.1 * k, 0.35, 2.6)
            if q > 0:
                c.save(); c.translate(x + DW / 2, 590 + DH / 2); c.scale(q, q)
                disque(c, 0, 0, 70, ROUGE, 1, (10, 26, 0.3)); texte_centre(c, "?", 0, 3, 96, BLANC, "noir")
                c.restore()
            c.restore()
            pilule(c, f"Partenaire {'ABC'[k]}", x + DW / 2, 590 + DH + 50, entre(t, T_APRES + 0.3 + 0.1 * k, 0.4, 2.2), "factory", ENCRE, BLANC, 26)


# ─────────────────────────────────────────── 4 · avec MONARQUE, pas besoin de partir de zéro
T_POSE = T_ACC - 0.3


def avec_monarque(c, t):
    r = logo_monarque(c, t, T_MQ, T_POSE, T_VOUS)
    a = entre(t, TW(77) - 0.05, 0.4, 1.6) * (1 - prog(t, T_POSE - 0.1, 0.2))
    if a > 0:
        texte_centre(c, "Pas besoin de partir de zéro.", 540, 1110 + 30 * (1 - a), 46, BEIGE2, "gras", borne(a * 3), -0.01)
    return r


# ─────────────────────────────────────────── 5 · on vous accompagne : fabricants, développement, production
def accompagne(c, t):
    g = Groupe(c, t, T_ACC - 0.25, T_PRES, ent="bas", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ON VOUS ACCOMPAGNE", T_ACC, T_PRES - 0.1, taille=80)
        x0 = (1080 - 3 * DW - 2 * DG) / 2
        cartes = [("Fabricants", "search", "rushes/machines", 1.2, T_FAB), ("Développement", "scissors", "ensemble-sweat-jupe", None, T_DEVP),
                  ("Production", "factory", "rushes/atelier", 1.1, T_PREP)]
        actif = max([k for k, d in enumerate(cartes) if t >= d[4] - 0.12] or [-1])
        for k, (lab, ic, nom, vit, t0) in enumerate(cartes):
            u = entre(t, T_ACC - 0.1 + 0.08 * k, 0.45, 1.6)
            if u <= 0: continue
            x, y = x0 + k * (DW + DG), 590
            on = k == actif
            dim = 1.0 if (actif < 0 or k <= actif) else 0.5
            s = mix(1.0, 1.04, prog(t, t0 - 0.12, 0.3, entreeSortie)) if on else 1.0
            c.save(); c.translate((1 - u) * 500, 80 * (1 - u))
            if vit: media(c, t, nom, x, y, DW, DH, borne(u * 3) * dim, s, video_t0=T_ACC, vitesse=vit, accent=ENCRE if on else None, pad=10, r=30)
            else: media(c, t, nom, x, y, DW, DH, borne(u * 3) * dim, s, zoom=1.0, fy=0.4, accent=ENCRE if on else None, pad=10, r=30)
            c.restore()
            pilule(c, lab, x + DW / 2, y + DH + 50, entre(t, t0 - 0.1, 0.4, 2.2), ic, ENCRE, BLANC, 28)
            coche(c, x + DW - 36, y + 36, 28, entre(t, t0 + 0.25, 0.35, 2.4))


# ─────────────────────────────────────────── 6 · présence dans l'écosystème chinois : le globe en points
def globe(c, t):
    g = Groupe(c, t, T_PRES - 0.15, T_VOUS, ent="zoom", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "AU CŒUR DE LA CHINE", T_PRES + 0.05, T_SANS - 0.1, taille=88)
        titre(c, t, "SANS VOUS DÉPLACER", T_SANS - 0.05, T_VOUS - 0.1, taille=88)
        a = entre(t, T_PRES - 0.1, 0.6, 1.3)
        rot = prog(t, T_PRES, T_ECO - T_PRES + 0.4, entreeSortie)
        lon0 = mix(30, 70, rot) + 1.5 * (t - T_PRES); lat0 = mix(42, 34, rot)
        R = 390 * mix(0.7, 1, a)
        cx, cy = 540, 990
        lum = prog(t, T_ECO - 0.1, 0.6, sortie)
        with Calque(c, borne(a * 3)):
            G = globe_points(c, lon0, lat0, cx, cy, R, lum)
            u = prog(t, T_PRES + 0.1, T_ECO - T_PRES + 0.3, entreeSortie)
            G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, 1.0, "#D5D1CB", 5, 0.32, [2, 16])
            stop = prog(t, T_SANS - 0.1, 0.3)                         # l'avion ne part plus : on ne se déplace pas
            hx, hy, hz = G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, u, ENCRE, 7, 0.32)
            G.repere(c, *PARIS, cx, cy, R, lon0, lat0, "Vous, en France", ENCRE, "FR", entre(t, T_PRES + 0.05, 0.42, 2.0), 1.0, 80)
            kx, ky, kz = G.pos(*CANTON, lon0, lat0, R, cx, cy)
            if kz > 0.05 and t > T_ECO - 0.2:
                onde(c, kx, ky, t, T_ECO, 20, 190, ENCRE, 6, 0.7)
            G.repere(c, *CANTON, cx, cy, R, lon0, lat0, "Monarque · Chine", ENCRE, "CN", entre(t, T_ECO + 0.05, 0.42, 2.0), 1.0, 70)
            px, py, pz = G.pos(*PARIS, lon0, lat0, R, cx, cy)
            if stop > 0:
                disque(c, px + 70, py + 40, 40 * stop, ENCRE, 1, (6, 16, 0.25)); icone(c, "plane", px + 70, py + 40, 42 * stop, BLANC, 2.4)
                croix(c, px + 104, py + 8, 24, entre(t, T_SANS + 0.2, 0.35, 2.4))
        pilule(c, "Des milliers de km", 560, 1420 - 60, entre(t, T_KM - 0.05, 0.4, 2.2), "plane", ROUGE, BLANC, 30)


# ─────────────────────────────────────────── 7 · tout depuis la France
CONV = [("Le prototype est prêt.", False), ("Photos envoyées", False), ("Validé ✓", True)]


def depuis_france(c, t):
    g = Groupe(c, t, T_VOUS - 0.1, T_TPS, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VOUS PRÉPAREZ", T_VOUS, T_FR2 - 0.1)
        titre(c, t, "DEPUIS LA FRANCE", T_FR2 - 0.05, T_TPS - 0.1)
        tuiles = [("Collections", "shirt", "produits/veste-ceinturee-prune", None, T_COLL), ("Échanges", "message-circle", None, None, T_ECH),
                  ("Développements", "scissors", "after-hours-bombers-marron-rose", None, T_DEVS), ("Production", "factory", "rushes/machines", 1.2, T_PROD)]
        for k, (lab, ic, nom, vit, t0) in enumerate(tuiles):
            u = entre(t, t0 - 0.25, 0.42, 1.8)
            if u <= 0: continue
            x, y, w, h = 85 + (k % 2) * 465, 570 + (k // 2) * 410, 445, 390
            c.save(); c.translate(x + w / 2, y + h / 2); c.scale(mix(0.4, 1, u), mix(0.4, 1, u)); c.translate(-(x + w / 2), -(y + h / 2))
            if vit: media(c, t, nom, x, y, w, h, borne(u * 3), 1.0, video_t0=t0 - 0.25, vitesse=vit, r=30, pad=10)
            elif nom: media(c, t, nom, x, y, w, h, borne(u * 3), 1.0, zoom=1.0 if k == 0 else 1.6, fx=0.62, fy=0.22 if k == 2 else 0.45, r=30, pad=10)
            else:
                with Calque(c, borne(u * 3)):
                    cadre(c, x, y, w, h, 30); conversation(c, t, x + 10, y + 10, w - 20, h - 20, t0 - 0.1, "Monarque · Chine", CONV, "message-circle", 0.22)
            c.restore()
            pilule(c, lab, x + w / 2, y + h - 40, entre(t, t0 - 0.05, 0.4, 2.2) * (1 - prog(t, T_FR2 - 0.1, 0.2)), ic, ENCRE, BLANC, 26)
            coche(c, x + w - 34, y + 34, 26, entre(t, T_FR2 + 0.06 * k, 0.35, 2.4))
        # l'étiquette France qui se pose au centre
        f = entre(t, T_FR2 - 0.05, 0.4, 2.2)
        if f > 0:
            c.save(); c.translate(540, 975); c.scale(mix(0.4, 1, f), mix(0.4, 1, f))
            w = largeur("Depuis la France", 40, "noir") + 150
            rrect(c, -w / 2, -52, w, 104, 52, ENCRE, borne(f * 3), (14, 34, 0.3))
            drapeau(c, "FR", -w / 2 + 34, -22, 64, 44, 6)
            texte(c, "Depuis la France", -w / 2 + 118, -hauteurLigne(40) / 2, 40, BLANC, "noir", alpha=borne(f * 3))
            c.restore()


# ─────────────────────────────────────────── 8 · votre temps et votre budget pour faire grandir la marque, pas pour voyager
def budget(c, t):
    g = Groupe(c, t, T_TPS - 0.1, T_ALORS, ent="bas", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VOTRE TEMPS, VOTRE BUDGET", T_TPS, T_MULT - 0.1, taille=78)
        titre(c, t, "PAS EN DÉPLACEMENTS", T_MULT - 0.05, T_ALORS - 0.1, couleur=ROUGE, taille=84)
        a = entre(t, T_TPS - 0.05, 0.5, 1.4)
        d = prog(t, T_MULT - 0.1, 0.4, entreeSortie)
        hb = [mix(0.12, h1, prog(t, T_GRAND - 0.15 + 0.06 * k, 0.6, entreeSortie)) for k, h1 in enumerate([0.4, 0.55, 0.95, 0.35])]
        gx0, gy0, base = graphique(c, t, 540, 900, hb, 2, t > T_GRAND + 0.3, borne(a * 3) * mix(1, 0.45, d), mix(0.6, 1, a), "VOTRE MARQUE")
        pilule(c, "Votre temps", 300, 1310, entre(t, TW(150) - 0.05, 0.4, 2.2), "clock", ENCRE, BLANC, 30, -2)
        pilule(c, "Votre budget", 780, 1310, entre(t, T_BUDG - 0.05, 0.4, 2.2), "wallet", ENCRE, BLANC, 30, 2)
        pilule(c, "Grandir", gx0 + 90 + 360 + 60, base - 330 * 0.95 - 50, entre(t, T_GRAND + 0.3, 0.4, 2.4) * (1 - d), "trending-up", BEIGE, BLANC, 26)
        # les billets qui s'empilent, barrés
        for k in range(3):
            b = entre(t, TW(163) + 0.12 * k, 0.4, 1.8)
            if b > 0:
                billet(c, 540 + (k - 1) * 70 + 600 * (1 - b), 880 + (k - 1) * 70, 640, borne(b * 3), (-8, 3, 10)[k], 1.0)
        x = entre(t, TW(165) + 0.1, 0.35, 2.6)
        if x > 0:
            c.save(); c.translate(540, 900); c.scale(x, x)
            disque(c, 0, 0, 110, ROUGE, 1, (12, 30, 0.3)); icone(c, "x", 0, 0, 130, BLANC, 3.4)
            c.restore()
        pilule(c, "Par où commencer ?", 540, 1180, entre(t, T_COMM - 0.05, 0.4, 2.2), "circle-help", ENCRE, BLANC, 32)


# ─────────────────────────────────────────── 9 · avant de réserver : partir, ou les bons partenaires ?
def question(c, t):
    g = Groupe(c, t, T_ALORS - 0.1, T_FIN, ent="droite", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "AVANT DE RÉSERVER", T_ALORS, T_QUEST - 0.1, taille=88)
        titre(c, t, "LA BONNE QUESTION", T_QUEST - 0.05, T_PARTIR - 0.1, taille=88)
        titre(c, t, "PARTIR ?", T_PARTIR - 0.05, T_OU - 0.1, taille=110)
        titre(c, t, "OU LES BONS PARTENAIRES ?", T_OU - 0.05, T_FIN - 0.1, taille=80)
        sw = prog(t, T_PARTIR - 0.2, 0.45, entreeSortie)
        if sw < 1:
            a = entre(t, T_ALORS - 0.05, 0.5, 1.4)
            billet(c, 540 - 700 * sw, 820, 860, borne(a * 3) * (1 - sw), -3, mix(0.6, 1, a))
            b = entre(t, T_RES - 0.1, 0.4, 2.0) * (1 - sw)
            if b > 0:
                c.save(); c.translate(540 - 700 * sw, 1180); c.scale(mix(0.4, 1, b), mix(0.4, 1, b))
                pastille(c, "Réserver", 0, 0, 40, ENCRE, BLANC, "plane", borne(b * 3), (14, 34, 0.3))
                c.restore()
                # le curseur s'approche… et s'arrête
                pc = cles(t, [(T_RES, 0), (T_QUEST - 0.1, 1, sortie), (T_QUEST + 0.4, 0.55, entreeSortie)])
                curseur(c, mix(980, 600, pc) - 700 * sw, mix(1560, 1205, pc), 1.3, borne(b * 3))
                q = entre(t, T_QUEST + 0.1, 0.35, 2.6)
                if q > 0:
                    c.save(); c.translate(820 - 700 * sw, 1120); c.scale(q, q)
                    disque(c, 0, 0, 60, ROUGE, 1, (10, 26, 0.3)); texte_centre(c, "?", 0, 3, 84, BLANC, "noir")
                    c.restore()
        if sw > 0:
            for k in range(2):
                u = entre(t, (T_PARTIR - 0.1, T_OU - 0.1)[k], 0.45, 1.6)
                if u <= 0: continue
                x = 70 + k * 500
                if k == 0:
                    with Calque(c, borne(u * 3)):
                        c.save(); c.translate(x + 220, 960); c.rotate(mix(-8, 0, u)); c.scale(mix(0.6, 1, u), mix(0.6, 1, u)); c.translate(-(x + 220), -960)
                        cadre(c, x, 600, 440, 720, 36, accent=ROUGE if t > T_OU else None)
                        col = "#9A968F" if t > T_OU else ENCRE
                        disque(c, x + 220, 860, 130, col, 1, (12, 30, 0.25)); icone(c, "plane", x + 220, 860, 130, BLANC, 2.4)
                        texte_centre(c, "PARIS", x + 220, 1080, 64, col, "archivo")
                        icone(c, "arrow-down", x + 220, 1150, 50, col, 3)
                        texte_centre(c, "CHINE", x + 220, 1225, 64, col, "archivo")
                        c.restore()
                    pilule(c, "Partir", x + 220, 1385, entre(t, T_PARTIR + 0.1, 0.4, 2.2), "plane", ENCRE, BLANC, 30)
                    croix(c, x + 400, 640, 36, entre(t, T_OU + 0.1, 0.35, 2.4))
                else:
                    media(c, t, "rushes/atelier", x, 600, 440, 720, borne(u * 3), mix(0.6, 1, u), video_t0=T_OU, vitesse=1.1, rot=mix(8, 0, u),
                          accent=VERT if t > T_BONS else None)
                    logo(c, x + 220, 680, 260, True, borne(u * 3))
                    pilule(c, "Les bons partenaires", x + 220, 1385, entre(t, T_BONS - 0.05, 0.4, 2.2), "users", VERT, BLANC, 28)
                    coche(c, x + 400, 640, 36, entre(t, T_BONS + 0.2, 0.35, 2.4))


# ─────────────────────────────────────────── 10 · fin
def fin(c, t):
    signature(c, t, T_FIN, [("Développez mieux.", T_DEVM, "noir", ENCRE), ("Produisez plus intelligemment.", T_PRODM, "noir", ENCRE),
                           ("Contactez-nous", T_CONT, "gras", GRIS)], T_CONT + 0.4)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(TW(9) - 0.1, "pop", -10)
son(T_ATT - 0.05, "impact", -3); son(T_ATT, "croc", -7)
son(T_DEP - 0.15, "whoosh", -8)
for k in range(14): son(T_MIL - 0.2 + 0.07 * k + 0.35, "ching", -15 if k % 2 else -12)
son(T_FRA - 0.1, "whoosh_bas", -8); son(TW(31) - 0.05, "check", -9)
son(T_VOY - 0.1, "whoosh", -8)
for ic, lab, t0 in LIGNES: son(t0 - 0.1, "pop", -10); son(t0 + 0.05, "ching", -15)
son(T_TEMPS - 0.1, "pop", -9)
for k in range(5): son(T_TEMPS + 0.2 + 0.25 * k, "clic", -14)
son(T_SURT - 0.05, "montee", -11); son(T_CHER + 0.05, "tampon", -5)
son(T_APRES - 0.1, "whoosh_bas", -8)
for k in range(3): son(T_APRES + 0.3 + 0.1 * k, "pop", -11); son(T_PART - 0.15 + 0.1 * k, "pop", -9)
son(TW(74), "croc", -8)
son(T_MQ - 0.12, "whoosh_long", -7); son(T_MQ + 0.05, "impact", -4); son(T_MQ + 0.08, "ching", -9); son(T_POSE, "whoosh_bas", -8)
for t0 in (T_FAB, T_DEVP, T_PREP): son(t0 - 0.1, "pop", -10); son(t0 + 0.25, "check", -12)
son(T_PRES - 0.15, "whoosh_long", -8); son(T_ECO - 0.1, "impact_doux", -6); son(T_ECO, "ching", -9)
son(T_SANS - 0.05, "whoosh_court", -9); son(T_SANS + 0.2, "croc", -9); son(T_KM - 0.05, "pop", -9)
son(T_VOUS - 0.1, "whoosh", -8)
for t0 in (T_COLL, T_ECH, T_DEVS, T_PROD): son(t0 - 0.25, "whoosh_court", -11); son(t0 - 0.05, "pop", -10)
for k in range(3): son(T_ECH - 0.1 + 0.22 * k, "blip", -13)
son(T_FR2 - 0.05, "impact_doux", -6); son(T_FR2 + 0.1, "ching", -9)
son(T_TPS - 0.1, "whoosh_bas", -8); son(TW(150) - 0.05, "pop", -10); son(T_BUDG - 0.05, "pop", -10)
for k in range(4): son(T_GRAND - 0.15 + 0.06 * k, "blip", -14)
son(T_GRAND + 0.3, "ching", -9)
for k in range(3): son(TW(163) + 0.12 * k, "whoosh_court", -10)
son(TW(165) + 0.1, "croc", -6); son(T_COMM - 0.05, "pop", -9)
son(T_ALORS - 0.1, "whoosh", -8); son(T_RES - 0.1, "pop", -10); son(T_QUEST + 0.1, "pop", -8)
son(T_PARTIR - 0.2, "whoosh_bas", -8); son(T_OU - 0.1, "whoosh", -9); son(T_OU + 0.1, "croc", -9)
son(T_BONS - 0.05, "pop", -9); son(T_BONS + 0.2, "check", -8)
son(T_FIN - 0.1, "montee", -11); son(T_FIN + 0.05, "impact", -5); son(T_DEVM, "pop", -11); son(T_PRODM, "pop", -11)
son(T_CONT + 0.25, "pop", -9); son(T_CONT + 0.85, "clic", -5); son(T_CONT + 0.9, "ching", -8)

for a, b in [(T_ATT - 0.1, T_ATT + 0.2), (T_FRA - 0.15, T_FRA + 0.3), (T_VOY - 0.15, T_VOY + 0.3), (T_APRES - 0.15, T_APRES + 0.3),
             (T_MQ - 0.1, T_MQ + 0.3), (T_ACC - 0.3, T_ACC + 0.1), (T_PRES - 0.2, T_PRES + 0.3), (T_VOUS - 0.15, T_VOUS + 0.3),
             (T_TPS - 0.15, T_TPS + 0.3), (T_ALORS - 0.15, T_ALORS + 0.3), (T_PARTIR - 0.2, T_PARTIR + 0.25), (T_FIN - 0.1, T_FIN + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_ATT, ROUGE, 0.08), (T_MQ + 0.05, "#FFFFFF", 0.1), (T_ECO, BEIGE, 0.08), (T_FR2, BEIGE, 0.07), (T_BONS + 0.2, VERT, 0.06)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_clair(c, t)
    hook(c, t); voyage(c, t); partenaires(c, t)
    accompagne(c, t); globe(c, t); depuis_france(c, t); budget(c, t); question(c, t)
    r = avec_monarque(c, t)
    fin(c, t)
    K.dessine_eclairs(c, t)
    cache = (T_MQ - 0.1 < t < T_ACC - 0.05) or t > T_FIN - 0.1
    if not cache:
        SOUS.dessine(c, t, BLANC if (r or 0) > 1200 else ENCRE)
