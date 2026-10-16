"""MQ-M07 « Vouloir économiser sur tout vous coûte plus cher » — script du client (hook 4), 16/10/2026.
Recette validée MQ-M05 (reference/monarque.md) : fond clair, Archivo Black, voix Tomy 4,2 mots/s, −13 LUFS,
graphique à modèles différents, carton à la signature du client. Aucun montant à l'écran : les coûts sont des barres et des €."""
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

T_PARF, T_MAIS, T_OU, T_MAUV, T_RENT = TW(5), TW(6), TW(10), TW(18), TW(23)
T_COLL, T_LANC, T_BUDG, T_MARG0, T_MARG = TW(27), TW(31), TW(32), TW(35), TW(39)
T_ALORS, T_CHERES, T_TOUT, T_CHAQ = TW(40), TW(47), TW(48), TW(54)
T_QUOI, T_DEVL, T_FABR = TW(59), TW(63), TW(67)
T_SIZ, T_MAT, T_DOS, T_ECH, T_REC, T_RET, T_COUTS = TW(74), TW(78), TW(82), TW(86), TW(90), TW(93), TW(98)
T_VMARGE, T_FOND, T_MARCHE = TW(101), TW(104), TW(114)
T_STRAT, T_NE, T_PRIX, T_CHERCH, T_PERT = TW(115), TW(123), TW(128), TW(132), TW(137)
T_PRD, T_BDG, T_AMB = TW(140), TW(142), TW(145)
T_EXACT, T_MQ, T_ACC = TW(146), TW(150), TW(155)
T_PISTE = [TW(156), TW(159), TW(161), TW(164)]
T_LIM, T_EURO, T_DECI, T_VAL, T_PERF, T_DEPM, T_TIRER = TW(165), TW(169), TW(176), TW(179), TW(183), TW(188), TW(197)
T_FIN, T_DEVM, T_PRODM, T_CH1, T_CH2 = TW(204), TW(205), TW(207), TW(210), TW(213)


def coupe(c, x, y, a, rot=0.0):
    """les ciseaux qui coupent dans les coûts"""
    if a <= 0.01: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(a, a)
    disque(c, 0, 0, 54, ENCRE, 1, (10, 26, 0.3)); icone(c, "scissors", 0, 0, 58, BLANC, 2.6)
    c.restore()


# ─────────────────────────────────────────── 1 · hook : réduire vos coûts ? parfait. mais où ?
POSTES = [("Tissu", 0.78), ("Façon", 0.62), ("Patronage", 0.5), ("Échantillon", 0.44), ("Contrôle qualité", 0.56)]


def hook(c, t):
    if t > T_COLL + 0.4: return
    g = Groupe(c, t, -1, T_COLL, ent="aucune", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "RÉDUIRE VOS COÛTS ?", -0.55, T_PARF - 0.1, taille=90)
        titre(c, t, "PARFAIT !", T_PARF - 0.05, T_MAIS - 0.1, couleur=VERT, taille=120)
        titre(c, t, "OÙ ÉCONOMISER ?", T_MAIS, T_MAUV - 0.1)
        titre(c, t, "LES MAUVAIS CHOIX", T_MAUV - 0.05, T_RENT - 0.1, couleur=ROUGE, taille=88)
        titre(c, t, "VOTRE RENTABILITÉ", T_RENT - 0.05, T_COLL - 0.1, couleur=ROUGE, taille=88)
        a = entre(t, -0.35, 0.5, 1.5)
        r = prog(t, T_RENT - 0.15, 0.45, entreeSortie)                 # la fiche remonte pour laisser la courbe
        reduit = mix(1.0, 0.7, prog(t, 0.2, 0.7, entreeSortie))
        mauvais = prog(t, T_MAUV + 0.1, 0.5, entreeSortie)
        lignes = []
        for k, (lab, v) in enumerate(POSTES):
            vv = v * reduit
            if k in (0, 4): vv = mix(vv, 0.08, mauvais)
            lignes.append((lab, vv))
        cx, cy = 540, mix(960, 800, r)
        s = mix(0.7, 1, a) * mix(1, 0.78, r)
        c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-540, -960)
        with Calque(c, borne(a * 3)):
            cadre(c, 120, 590, 840, 740, 44)
            fiche_couts(c, t, 120, 590, 840, 740, -1.0, lignes, "VOS COÛTS", (0, 4) if t > T_MAUV + 0.1 else ())
        c.restore()
        # les ciseaux qui cherchent où couper
        sx = cles(t, [(0, 860), (0.9, 700, entreeSortie), (T_OU, 860), (T_OU + 0.35, 330, entreeSortie), (T_OU + 0.7, 700, entreeSortie),
                      (T_MAUV - 0.1, 760), (T_MAUV + 0.1, 600, entreeSortie)])
        sy = cles(t, [(0, 700), (0.9, 900, entreeSortie), (T_OU, 900), (T_OU + 0.35, 1080, entreeSortie), (T_OU + 0.7, 820, entreeSortie),
                      (T_MAUV - 0.1, 760), (T_MAUV + 0.1, 760, entreeSortie)])
        coupe(c, sx, sy - 160 * r, entre(t, -0.3, 0.4, 2.0) * (1 - r), 10 * math.sin(t * 9))
        coche(c, 900, 600, 46, entre(t, T_PARF, 0.35, 2.4) * (1 - prog(t, T_MAIS, 0.2)))
        if t > T_MAUV + 0.2:
            for k, yy in enumerate((750, 1246)):
                croix(c, 880, (yy - 960) * s + cy, 30 * s, entre(t, T_MAUV + 0.3 + 0.12 * k, 0.35, 2.4) * (1 - r))
        # la rentabilité qui plonge
        if r > 0:
            with Calque(c, r):
                cadre(c, 140, 1060, 800, 300, 36)
                texte(c, "RENTABILITÉ", 190, 1095, 30, ENCRE, "noir", track=0.06)
                icone(c, "trending-down", 880, 1115, 46, ROUGE, 2.6)
                u = prog(t, T_RENT, 0.9, entreeSortie)
                path = skia.Path(); path.moveTo(190, 1200)
                n = int(60 * u) + 1
                for i in range(1, n):
                    v = i / 60
                    path.lineTo(190 + v * 700, 1200 - 30 * math.sin(v * 6) + 110 * v ** 2)
                pe = peinture(ROUGE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=9); pe.setStrokeCap(skia.Paint.kRound_Cap)
                c.drawPath(path, pe)


# ─────────────────────────────────────────── 2 · lancer une collection, maîtriser le budget, garder la marge
def jauge(c, t, x, y, w, lab, ic, v, couleur):
    disque(c, x + 30, y + 30, 30, "#EFEDEA"); icone(c, ic, x + 30, y + 30, 32, ENCRE, 2.4)
    texte(c, lab, x + 80, y + 30 - hauteurLigne(34) / 2, 34, ENCRE, "noir", track=0.04)
    rrect(c, x, y + 80, w, 26, 13, "#E8E5E0"); rrect(c, x, y + 80, max(26, w * v), 26, 13, couleur)


def collection(c, t):
    g = Groupe(c, t, T_COLL - 0.1, T_ALORS, ent="bas", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "LANCER UNE COLLECTION", T_COLL, T_BUDG - 0.1, taille=84)
        titre(c, t, "MAÎTRISER LE BUDGET", T_BUDG - 0.05, T_MARG0 - 0.1, taille=88)
        titre(c, t, "UN MAXIMUM DE MARGE", T_MARG0 - 0.05, T_ALORS - 0.1, taille=84)
        for k, nom in enumerate(MODELES):
            u = entre(t, T_COLL + 0.1 + 0.1 * k, 0.45, 1.8)
            if u <= 0: continue
            x = 70 + k * 240
            media(c, t, nom, x, 580, 220, 300, borne(u * 3), mix(0.5, 1, u), zoom=1.0, r=26, pad=8, rot=(-4, 2, -2, 4)[k] * (1 - u))
        pilule(c, "Votre collection", 540, 920, entre(t, T_LANC - 0.05, 0.4, 2.2), "shirt", ENCRE, BLANC, 30)
        b = entre(t, T_BUDG - 0.1, 0.5, 1.5)
        if b > 0:
            c.save(); c.translate(0, 200 * (1 - b))
            with Calque(c, borne(b * 3)):
                cadre(c, 110, 1000, 860, 360, 40)
                jauge(c, t, 170, 1040, 740, "BUDGET", "wallet", mix(0.9, 0.55, prog(t, T_BUDG + 0.2, 0.6, entreeSortie)), ENCRE)
                jauge(c, t, 170, 1200, 740, "MARGE", "badge-percent", mix(0.0, 0.85, prog(t, TW(37) - 0.1, 0.8, entreeSortie)), BEIGE)
            c.restore()


# ─────────────────────────────────────────── 3 · le moins cher, tout vous-même, chaque dépense rognée
OFFRES = [("rushes/machines", "€€€"), ("rushes/atelier", "€€"), ("rushes/bureau", "€")]
TACHES = ["wrench", "phone", "truck", "file-text", "package", "mail"]


def moins_cher(c, t):
    g = Groupe(c, t, T_ALORS - 0.1, T_QUOI, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "LE MOINS CHER", T_ALORS, T_TOUT - 0.1)
        titre(c, t, "TOUT VOUS-MÊME", T_TOUT - 0.05, T_CHAQ - 0.1)
        titre(c, t, "CHAQUE DÉPENSE", T_CHAQ - 0.05, T_QUOI - 0.1)
        sw = prog(t, T_TOUT - 0.15, 0.45, entreeSortie)
        if sw < 1:
            for k, (nom, prix) in enumerate(OFFRES):
                u = entre(t, T_ALORS + 0.08 * k, 0.45, 1.6)
                if u <= 0: continue
                x = 70 + k * 320
                elu = k == 2 and t > T_CHERES + 0.2
                c.save(); c.translate(0, -900 * sw + (1 - u) * 400)
                media(c, t, nom, x, 600, 300, 440, borne(u * 3), 1.0, video_t0=T_ALORS, vitesse=1.2, r=30, pad=10,
                      accent=VERT if elu else None)
                pilule(c, prix, x + 150, 1100, entre(t, TW(44) + 0.1 * k, 0.4, 2.2), "euro", VERT if elu else ENCRE, BLANC, 32)
                c.restore()
            pc = prog(t, TW(46) - 0.1, 0.45, sortie)
            clic = prog(t, T_CHERES + 0.1, 0.1) * (1 - prog(t, T_CHERES + 0.2, 0.15))
            if t > TW(46) - 0.1:
                curseur(c, mix(1000, 870, pc), mix(1560, 1120, pc) - 900 * sw, 1.3, 1 - sw, clic)
        if sw > 0:
            with Calque(c, sw):
                X, Y = 540, 900
                for k, ic in enumerate(TACHES):
                    an = t * 2.6 + k * math.tau / len(TACHES)
                    px, py = X + 290 * math.cos(an), Y + 220 * math.sin(an)
                    disque(c, px, py, 58, BLANC, 1, (10, 26, 0.2)); icone(c, ic, px, py, 56, ENCRE, 2.4)
                sh = secousse(t, T_TOUT + 0.2, 10, 0.6)
                disque(c, X + sh[0], Y + sh[1], 100, ENCRE, 1, (14, 34, 0.3))
                icone(c, "user", X + sh[0], Y - 22 + sh[1], 56, BLANC, 2.8); texte_centre(c, "VOUS", X + sh[0], Y + 40 + sh[1], 34, BLANC, "noir")
                pilule(c, "Tout vous-même", 540, 640, entre(t, TW(51) - 0.1, 0.4, 2.2) * (1 - prog(t, T_CHAQ - 0.1, 0.2)), "triangle-alert", ROUGE, BLANC, 30)
                # chaque dépense rognée
                for k in range(5):
                    e = entre(t, T_CHAQ + 0.08 * k, 0.4, 2.0)
                    if e <= 0: continue
                    rr = 50 * mix(1, 0.55, prog(t, TW(56) + 0.12 * k, 0.3, entree))
                    x = 220 + k * 160
                    c.save(); c.translate(x, 1250); c.scale(e, e)
                    disque(c, 0, 0, rr, ENCRE, 1, (6, 16, 0.25)); icone(c, "euro", 0, 0, rr, BLANC, 2.6)
                    c.restore()
                    if t > TW(56) + 0.12 * k: coupe(c, x + 46, 1205, entre(t, TW(56) + 0.12 * k - 0.1, 0.3, 2.0) * 0.6, -20)


# ─────────────────────────────────────────── 4 · à quoi sert d'économiser si c'est mal fabriqué ?
def quoi(c, t):
    g = Groupe(c, t, T_QUOI - 0.1, T_SIZ, ent="bas", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "À QUOI ÇA SERT ?", T_QUOI, T_FABR - 0.1)
        titre(c, t, "SI C'EST MAL FABRIQUÉ", T_FABR - 0.05, T_SIZ - 0.1, couleur=ROUGE, taille=84)
        u = entre(t, T_QUOI, 0.45, 1.6)
        media(c, t, "ensemble-sweat-jupe", 70, 620, 420, 640, borne(u * 3), mix(0.6, 1, u), zoom=1.0, fy=0.3, rot=mix(-8, 0, u))
        pilule(c, "Développement", 280, 1310, entre(t, T_DEVL - 0.05, 0.4, 2.2), "scissors", ENCRE, BLANC, 28)
        coupe(c, 450, 660, entre(t, T_DEVL, 0.35, 2.4), -15)
        pilule(c, "Économisé", 280, 1180, entre(t, T_DEVL + 0.25, 0.4, 2.2), "euro", VERT, BLANC, 28, -3)
        v = entre(t, T_FABR - 0.25, 0.45, 1.6)
        if v > 0:
            media(c, t, "trench-court", 590, 620, 420, 640, borne(v * 3), mix(0.6, 1, v), zoom=1.05, rot=mix(8, 0, v), accent=ROUGE)
            pilule(c, "Votre produit", 800, 1310, entre(t, TW(69) - 0.05, 0.4, 2.2), "shirt", ENCRE, BLANC, 28)
            tampon(c, "MAL FABRIQUÉ", 800, 900, t, TW(72), 44, ROUGE, -9)
        f = entre(t, TW(67) - 0.1, 0.35, 2.6)
        if f > 0:
            disque(c, 540, 940, 52 * f, ENCRE, 1, (12, 30, 0.3)); icone(c, "arrow-right", 540, 940, 60 * f, BLANC, 3)


# ─────────────────────────────────────────── 5 · la pression : chaque erreur claque sur la précédente
def table_tailles(c, x, y, w, h, t, t0):
    texte(c, "SIZING", x + 30, y + 34, 34, ENCRE, "archivo", track=0.02)
    cols, rows = ["", "S", "M", "L", "XL"], ["Poitrine", "Épaules", "Manches", "Longueur"]
    cw, rh = (w - 60) / 5, (h - 150) / 5
    for j, lab in enumerate(cols):
        texte_centre(c, lab, x + 30 + cw * (j + 0.5), y + 130, 26, GRIS, "noir")
    for i, lab in enumerate(rows):
        yy = y + 120 + rh * (i + 1)
        trait(c, x + 30, yy - rh * 0.45, x + w - 30, yy - rh * 0.45, "#E3E0DB", 2)
        texte(c, lab, x + 30, yy - hauteurLigne(22, "gras") / 2, 22, ENCRE, "gras")
        for j in range(1, 5):
            faux = (i, j) in ((1, 2), (3, 4), (2, 1))
            cx_, cy_ = x + 30 + cw * (j + 0.5), yy
            if faux and t > t0 + 0.3:
                rrect(c, cx_ - cw * 0.4, cy_ - 20, cw * 0.8, 40, 10, ROUGE, 0.15, None, ROUGE, 3)
                texte_centre(c, "?", cx_, cy_, 28, ROUGE, "noir")
            else:
                rrect(c, cx_ - cw * 0.3, cy_ - 6, cw * 0.6, 12, 6, "#DCD8D2")


def recommencer(c, x, y, w, h, t, t0):
    rrect(c, x, y, w, h, 24, "#FDECEB")
    an = 360 * 1.4 * max(0, t - t0)
    c.save(); c.translate(x + w / 2, y + h / 2 - 40); c.rotate(an)
    icone(c, "refresh-cw", 0, 0, 260, ROUGE, 2.4)
    c.restore()
    texte_centre(c, "ÉCHANTILLON 2", x + w / 2, y + h - 110, 40, ROUGE, "archivo")


ERREURS = [("UN SIZING MAL DÉFINI", T_SIZ, "sizing", "ruler"), ("MATIÈRE MAL CHOISIE", T_MAT, "rushes/nuancier", "layers"),
           ("DOSSIER INCOMPLET", T_DOS, "eln-078-tailleur-prune-2pages", "file-text"), ("ÉCHANTILLON REFUSÉ", T_ECH, "trench-court", "x"),
           ("ON RECOMMENCE", T_REC, "recommencer", "refresh-cw"), ("PRODUCTION EN RETARD", T_RET, "rushes/machines", "calendar-clock"),
           ("LES COÛTS AUGMENTENT", T_COUTS, "couts", "trending-up")]


def pression(c, t):
    g = Groupe(c, t, T_SIZ - 0.1, T_VMARGE, ent="aucune", sor="haut", cy=960)
    if not g.visible: return
    with g:
        for k, (txt, t0, quoi_, ic) in enumerate(ERREURS):
            t1 = ERREURS[k + 1][1] if k + 1 < len(ERREURS) else T_VMARGE
            titre(c, t, txt, t0 - 0.05, t1 - 0.1, couleur=ROUGE if k % 2 else ENCRE, taille=86)
            if t < t0 - 0.15 or (k + 2 < len(ERREURS) and t > ERREURS[k + 2][1]): continue
            u = prog(t, t0 - 0.15, 0.22, entree)
            s = mix(1.6, 1, u)
            rot = (-4, 3, -3, 4, -2, 3, -4)[k]
            c.save(); c.translate(540, 960); c.rotate(rot); c.scale(s, s); c.translate(-540, -960)
            x, y, w, h = 210, 570, 660, 780
            with Calque(c, borne(u * 2)):
                if quoi_.startswith("rushes"):
                    media(c, t, quoi_, x, y, w, h, 1.0, 1.0, video_t0=t0, vitesse=1.2, r=34)
                elif quoi_ in ("trench-court", "eln-078-tailleur-prune-2pages"):
                    media(c, t, quoi_, x, y, w, h, 1.0, 1.0, zoom=1.0, fy=0.35, r=34)
                    if quoi_.startswith("eln"):                        # des cases du dossier restent vides
                        for (bx, by, bw, bh) in [(250, 690, 260, 60), (560, 760, 260, 60), (300, 1140, 500, 120)]:
                            rrect(c, bx, by, bw, bh, 12, "#EFEDEA", 1, None, ROUGE, 3)
                            texte_centre(c, "?", bx + bw / 2, by + bh / 2, 34, ROUGE, "noir")
                else:
                    cadre(c, x, y, w, h, 34)
                    if quoi_ == "sizing": table_tailles(c, x, y, w, h, t, t0)
                    elif quoi_ == "recommencer": recommencer(c, x + 12, y + 12, w - 24, h - 24, t, t0)
                    else:
                        v = prog(t, t0, 0.6, entreeSortie)
                        fiche_couts(c, t, x, y, w, h, -1.0, [(lab, mix(vv, min(1.0, vv * 1.6), v)) for lab, vv in POSTES], "VOS COÛTS",
                                    tuple(range(5)) if v > 0.3 else ())
            c.restore()
            if t > t0 - 0.05:
                sh = secousse(t, t0 + 0.07, 10, 0.25)
                croix(c, 820 + sh[0], 620 + sh[1], 44, entre(t, t0 + 0.25, 0.35, 2.4))
            # le compteur des erreurs
        n = sum(1 for e in ERREURS if t > e[1] - 0.05)
        for k in range(len(ERREURS)):
            on = k < n
            disque(c, 540 + (k - 3) * 54, 1395, 16 if on else 10, ROUGE if on else "#DCD8D2")


# ─────────────────────────────────────────── 6 · et votre marge ? elle fond avant le marché
def marge(c, t):
    g = Groupe(c, t, T_VMARGE - 0.1, T_STRAT, ent="bas", sor="zoom", cy=960)
    if not g.visible or t > T_STRAT + 0.3: return
    with g:
        titre(c, t, "VOTRE MARGE ?", T_VMARGE, T_FOND - 0.1)
        titre(c, t, "ELLE FOND", T_FOND - 0.05, T_STRAT - 0.1, couleur=ROUGE, taille=120)
        a = entre(t, T_VMARGE - 0.05, 0.5, 1.4)
        v = mix(0.88, 0.06, prog(t, T_FOND - 0.1, T_MARCHE - T_FOND, lambda x: x ** 0.8))
        with Calque(c, borne(a * 3)):
            cadre(c, 110, 590, 860, 360, 40)
            disque(c, 180, 660, 34, "#EFEDEA"); icone(c, "badge-percent", 180, 660, 36, ENCRE, 2.4)
            texte(c, "VOTRE MARGE", 236, 660 - hauteurLigne(38) / 2, 38, ENCRE, "noir", track=0.04)
            col = melange(BEIGE, ROUGE, prog(t, T_FOND, 1.2))
            rrect(c, 170, 750, 740, 110, 55, "#E8E5E0"); rrect(c, 170, 750, max(110, 740 * v), 110, 55, col)
            # les gouttes qui tombent du bout de la barre
            if t > T_FOND:
                ex = 170 + max(60, 740 * v) - 20
                for k in range(8):
                    d = (t - T_FOND - 0.18 * k)
                    if d <= 0: continue
                    d = d % 1.0
                    disque(c, ex - 30 * (k % 3), 870 + 260 * d * d, 16 * (1 - d), ROUGE, 0.8 * (1 - d))
        # le produit qui n'est pas encore arrivé au marché
        b = entre(t, TW(110) - 0.1, 0.45, 1.6)
        if b > 0:
            with Calque(c, borne(b * 3)):
                trait(c, 200, 1180, 860, 1180, "#DCD8D2", 8, 1, [16, 16])
                disque(c, 880, 1180, 100, ENCRE, 1, (10, 26, 0.25)); icone(c, "store", 880, 1180, 96, BLANC, 2.4)
                texte_centre(c, "Le marché", 880, 1325, 32, ENCRE, "noir")
                px = mix(220, 560, prog(t, TW(110), T_MARCHE - TW(110) + 0.4, sortie))
                media(c, t, "produits/veste-zip-marine", px - 120, 1020, 240, 320, 1.0, 1.0, zoom=1.0, r=28, pad=8)


# ─────────────────────────────────────────── 7 · changez de stratégie
def strategie(c, t):
    return flash_noir(c, t, T_STRAT, T_NE, "CHANGEZ", "DE STRATÉGIE", BEIGE, 140)


# ─────────────────────────────────────────── 8 · pas le prix le plus bas : la solution la plus pertinente
def pertinent(c, t):
    g = Groupe(c, t, T_NE - 0.1, T_EXACT, ent="aucune", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "PAS LE PRIX LE PLUS BAS", T_NE, T_CHERCH - 0.1, taille=80)
        titre(c, t, "LE PLUS PERTINENT", T_CHERCH - 0.05, T_EXACT - 0.1, couleur=ENCRE, taille=88)
        for k in range(2):
            t0 = (T_NE - 0.05, T_CHERCH - 0.1)[k]
            u = entre(t, t0, 0.45, 1.6)
            if u <= 0: continue
            x = 70 + k * 520
            on = k == 1 and t > T_PERT
            dim = 0.5 if (k == 0 and t > T_CHERCH) else 1.0
            c.save(); c.translate(x + 210, 880); c.rotate(mix((-8, 8)[k], 0, u)); c.scale(mix(0.6, 1, u), mix(0.6, 1, u)); c.translate(-(x + 210), -880)
            with Calque(c, borne(u * 3) * dim):
                cadre(c, x, 600, 420, 560, 36, accent=BEIGE if on else None)
                if k == 0:
                    disque(c, x + 210, 820, 120, "#9A968F"); icone(c, "euro", x + 210, 820, 120, BLANC, 2.4)
                    texte_centre(c, "LE MOINS", x + 210, 1020, 46, ENCRE, "archivo"); texte_centre(c, "CHER", x + 210, 1080, 46, ENCRE, "archivo")
                else:
                    for rr, col in [(130, BEIGE), (92, BLANC), (56, BEIGE), (20, BLANC)]: disque(c, x + 210, 820, rr, col)
                    texte_centre(c, "LE PLUS", x + 210, 1020, 46, ENCRE, "archivo"); texte_centre(c, "PERTINENT", x + 210, 1080, 46, ENCRE, "archivo")
            c.restore()
        croix(c, 450, 630, 36, entre(t, TW(131), 0.35, 2.4))
        coche(c, 970, 630, 36, entre(t, T_PERT, 0.35, 2.4))
        for k, (lab, ic, t0, x) in enumerate([("Votre produit", "shirt", T_PRD, 250), ("Votre budget", "wallet", T_BDG, 540), ("Vos ambitions", "rocket", T_AMB, 830)]):
            pilule(c, lab, x, 1260, entre(t, t0 - 0.05, 0.4, 2.2), ic, BEIGE if k == 2 else ENCRE, BLANC, 26, (-3, 2, -2)[k])


# ─────────────────────────────────────────── 9 · c'est exactement ce que MONARQUE vous aide à faire
T_POSE = T_ACC - 0.3
PISTE = [("Développement", "ensemble-sweat-jupe"), ("Sourcing", "rushes/bureau"), ("Contrôle", "rushes/controle"), ("Production", "rushes/machines")]


def exactement(c, t):
    if T_EXACT - 0.1 < t < T_MQ + 0.2:
        titre(c, t, "C'EST EXACTEMENT ÇA", T_EXACT, T_MQ + 0.2, y=960, taille=96)


def aide(c, t):
    g = Groupe(c, t, T_ACC - 0.25, T_LIM, ent="bas", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ON VOUS AIDE", T_ACC, T_LIM - 0.1, taille=96)
        a = entre(t, T_ACC - 0.1, 0.5, 1.4)
        k = max([i for i, t0 in enumerate(T_PISTE) if t >= t0 - 0.15] or [0])
        nom = PISTE[k][1]
        if nom.startswith("rushes"):
            media(c, t, nom, 120, 560, 840, 560, borne(a * 3), mix(0.6, 1, a), video_t0=T_PISTE[k] - 0.15, vitesse=1.2, accent=ENCRE)
        else:
            media(c, t, nom, 120, 560, 840, 560, borne(a * 3), mix(0.6, 1, a), zoom=1.0, fy=0.3, accent=ENCRE)
        with Calque(c, borne(a * 3)):
            x0, x1, py = 180, 900, 1240
            trait(c, x0, py, x1, py, "#DCD8D2", 8)
            p = prog(t, T_PISTE[0] - 0.1, T_PISTE[-1] - T_PISTE[0] + 0.1, entreeSortie)
            trait(c, x0, py, mix(x0, x1, p), py, ENCRE, 8)
            for i, (lab, _) in enumerate(PISTE):
                x = x0 + i * (x1 - x0) / 3
                on = t > T_PISTE[i] - 0.1
                disque(c, x, py, 22 if on else 16, ENCRE if on else "#DCD8D2")
                if on: icone(c, "check", x, py, 24, BLANC, 3)
                texte_centre(c, lab, x, py + 64, 26, ENCRE if on else GRIS, "gras", 1.0, -0.01)
            disque(c, mix(x0, x1, p), py, 30, BEIGE, 1, (8, 20, 0.3))


# ─────────────────────────────────────────── 10 · budget limité : chaque euro a un objectif
CIBLES = [("Matière", "layers", 220), ("Développement", "scissors", 540), ("Contrôle", "shield-check", 860)]


def objectif(c, t):
    g = Groupe(c, t, T_LIM - 0.1, T_DECI, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "BUDGET LIMITÉ ?", T_LIM, T_EURO - 0.1)
        titre(c, t, "CHAQUE EURO A UN BUT", T_EURO - 0.05, T_DECI - 0.1, taille=86)
        a = entre(t, T_LIM - 0.05, 0.5, 1.5)
        with Calque(c, borne(a * 3)):
            c.save(); c.translate(540, 790); c.scale(mix(0.7, 1.45, a), mix(0.7, 1.45, a))
            rrect(c, -170, -120, 340, 240, 40, ENCRE, 1, (16, 40, 0.3))
            rrect(c, 60, -40, 130, 80, 30, "#2A2A2A"); disque(c, 110, 0, 14, BEIGE)
            icone(c, "wallet", -60, 0, 110, BLANC, 2.4)
            c.restore()
        for k, (lab, ic, x) in enumerate(CIBLES):
            u = entre(t, T_EURO + 0.1 * k, 0.4, 1.8)
            if u <= 0: continue
            c.save(); c.translate(x, 1180); c.scale(u, u)
            disque(c, 0, 0, 110, BLANC, 1, (12, 30, 0.18)); anneau(c, 0, 0, 110, BEIGE if t > TW(171) + 0.35 + 0.3 * k else "#E3E0DB", 6)
            icone(c, ic, 0, -8, 76, ENCRE, 2.4)
            c.restore()
            pilule(c, lab, x, 1340, u, None, ENCRE, BLANC, 26)
            # la pièce part du porte-monnaie vers sa cible
            t0 = TW(171) + 0.3 * k
            if t > t0:
                v = prog(t, t0, 0.4, entreeSortie)
                px, py = mix(540, x, v), mix(800, 1180, v) - 160 * math.sin(math.pi * v)
                if v < 1: piece(c, px, py, 40)
                coche(c, x + 80, 1100, 26, entre(t, t0 + 0.35, 0.35, 2.4))


def piece(c, x, y, r, a=1.0):
    disque(c, x, y, r, ENCRE, a, (6, 16, 0.25)); anneau(c, x, y, r * 0.78, BEIGE, 3, a); icone(c, "euro", x, y, r, BLANC, 2.6, a)


# ─────────────────────────────────────────── 11 · chaque décision crée de la valeur : le graphique
def valeur(c, t):
    g = Groupe(c, t, T_DECI - 0.1, T_FIN, ent="bas", sor="recul", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "CHAQUE DÉCISION", T_DECI, T_PERF - 0.1)
        titre(c, t, "LA VRAIE PERFORMANCE", T_PERF - 0.05, T_TIRER - 0.1, taille=86)
        titre(c, t, "TIRER DAVANTAGE", T_TIRER - 0.05, T_FIN - 0.1, couleur=ENCRE)
        a = entre(t, T_DECI - 0.05, 0.5, 1.4)
        hb = []
        for k, (h1, h2) in enumerate([(0.35, 0.42), (0.5, 0.6), (0.72, 1.0), (0.3, 0.38)]):
            v = mix(0.12, h1, prog(t, T_VAL - 0.1 + 0.06 * k, 0.6, entreeSortie))
            hb.append(mix(v, h2, prog(t, T_TIRER + 0.1, 0.6, entreeSortie)))
        gx0, gy0, base = graphique(c, t, 540, 900, hb, 2, t > T_VAL + 0.3, borne(a * 3), mix(0.6, 1, a), "LA VALEUR CRÉÉE")
        pilule(c, "Rentabilité", gx0 + 90 + 360 + 60, base - 330 * hb[2] - 50, entre(t, T_TIRER + 0.3, 0.4, 2.4), "trending-up", BEIGE, BLANC, 26)
        d = entre(t, TW(192) - 0.05, 0.4, 2.2)
        if d > 0:
            pilule(c, "Dépenser moins à tout prix", 540, 1320, d, "scissors", "#9A968F", BLANC, 36)
            if t > TW(195): trait(c, 540 - 330 * entre(t, TW(195), 0.3, 1.5), 1320, 540 + 330 * entre(t, TW(195), 0.3, 1.5), 1320, ROUGE, 5)
        eclats(c, gx0 + 90 + 420, base - 330, t, T_TIRER + 0.5, 14, 300, [BEIGE, BEIGE2, ENCRE], graine=7)


# ─────────────────────────────────────────── 12 · fin
def fin(c, t):
    signature(c, t, T_FIN, [("Développez mieux.", T_DEVM, "noir", ENCRE), ("Produisez plus intelligemment.", T_PRODM, "noir", ENCRE),
                           ("Chaque décision compte.", T_CH1, "gras", GRIS), ("Chaque investissement aussi.", T_CH2, "gras", GRIS)],
              TW(215) + 0.1, logo_y=600)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(0.3, "swipe", -11)
son(T_PARF, "check", -7); son(T_PARF + 0.05, "ching", -10)
son(T_MAIS - 0.05, "whoosh_court", -9); son(T_OU + 0.35, "swipe", -11)
son(T_MAUV + 0.1, "swipe", -8)
for k in range(2): son(T_MAUV + 0.3 + 0.12 * k, "croc", -9)
son(T_RENT - 0.15, "whoosh_bas", -8); son(T_RENT + 0.3, "impact_doux", -7)
son(T_COLL - 0.1, "whoosh", -8)
for k in range(4): son(T_COLL + 0.1 + 0.1 * k, "pop", -11)
son(T_LANC - 0.05, "pop", -10); son(T_BUDG - 0.1, "whoosh_court", -10); son(TW(37) - 0.1, "montee", -13)
son(T_ALORS - 0.1, "whoosh_bas", -8)
for k in range(3): son(TW(44) + 0.1 * k, "pop", -11)
son(T_CHERES + 0.1, "clic", -5); son(T_CHERES + 0.2, "check", -10)
son(T_TOUT - 0.15, "whoosh", -8); son(T_TOUT + 0.2, "croc", -9); son(TW(51) - 0.1, "pop", -9)
for k in range(5): son(T_CHAQ + 0.08 * k, "pop", -12); son(TW(56) + 0.12 * k, "swipe", -13)
son(T_QUOI - 0.1, "whoosh_bas", -8); son(T_DEVL, "swipe", -9); son(T_DEVL + 0.25, "ching", -10)
son(T_FABR - 0.25, "whoosh", -8); son(TW(72), "tampon", -5)
for txt, t0, q, ic in ERREURS:
    son(t0 - 0.15, "whoosh_court", -10); son(t0 + 0.07, "impact", -6); son(t0 + 0.25, "croc", -10)
son(T_VMARGE - 0.1, "whoosh_bas", -8); son(T_FOND - 0.1, "montee", -12)
for k in range(5): son(T_FOND + 0.3 + 0.18 * k, "blip", -15)
son(TW(110) - 0.1, "pop", -10)
son(T_STRAT - 0.12, "whoosh_long", -7); son(T_STRAT, "impact", -3); son(T_STRAT + 0.2, "impact", -6)
son(T_NE - 0.05, "whoosh", -8); son(TW(131), "croc", -9); son(T_CHERCH - 0.1, "whoosh", -9); son(T_PERT, "check", -8); son(T_PERT + 0.05, "ching", -10)
for t0 in (T_PRD, T_BDG, T_AMB): son(t0 - 0.05, "pop", -10)
son(T_EXACT - 0.1, "whoosh_court", -9)
son(T_MQ - 0.12, "whoosh_long", -7); son(T_MQ + 0.05, "impact", -4); son(T_MQ + 0.08, "ching", -9); son(T_POSE, "whoosh_bas", -8)
for t0 in T_PISTE: son(t0 - 0.1, "check", -11); son(t0 - 0.15, "swipe", -13)
son(T_LIM - 0.1, "whoosh", -8)
for k in range(3): son(T_EURO + 0.1 * k, "pop", -11); son(TW(171) + 0.3 * k, "whoosh_court", -11); son(TW(171) + 0.3 * k + 0.38, "ching", -10)
son(T_DECI - 0.1, "whoosh_bas", -8)
for k in range(4): son(T_VAL - 0.1 + 0.06 * k, "blip", -14)
son(T_VAL + 0.3, "ching", -9); son(TW(192) - 0.05, "pop", -10); son(TW(195), "croc", -9)
son(T_TIRER + 0.1, "montee", -11); son(T_TIRER + 0.5, "ching", -7)
son(T_FIN - 0.1, "montee", -11); son(T_FIN + 0.05, "impact", -5)
for t0 in (T_DEVM, T_PRODM, T_CH1, T_CH2): son(t0, "pop", -11)
son(TW(215) - 0.05, "pop", -9); son(TW(215) + 0.55, "clic", -5); son(TW(215) + 0.6, "ching", -8)

for a, b in [(T_PARF - 0.1, T_PARF + 0.2), (T_MAUV, T_MAUV + 0.3), (T_COLL - 0.15, T_COLL + 0.3), (T_ALORS - 0.15, T_ALORS + 0.3),
             (T_TOUT - 0.15, T_TOUT + 0.3), (T_QUOI - 0.15, T_QUOI + 0.3), (T_SIZ - 0.15, T_SIZ + 0.2), (T_VMARGE - 0.15, T_VMARGE + 0.3),
             (T_STRAT - 0.1, T_STRAT + 0.3), (T_NE - 0.15, T_NE + 0.2), (T_MQ - 0.1, T_MQ + 0.3), (T_LIM - 0.15, T_LIM + 0.3),
             (T_DECI - 0.15, T_DECI + 0.3), (T_FIN - 0.1, T_FIN + 0.3)] + [(e[1] - 0.15, e[1] + 0.1) for e in ERREURS[1:]]:
    rapide(a, b)
for tt, cc_, a_ in [(T_PARF, VERT, 0.06), (T_MAUV + 0.1, ROUGE, 0.07), (T_STRAT, "#FFFFFF", 0.08), (T_MQ + 0.05, "#FFFFFF", 0.1),
                    (T_PERT, BEIGE, 0.07), (T_TIRER + 0.5, BEIGE, 0.08)] + [(e[1] + 0.07, ROUGE, 0.05) for e in ERREURS]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_clair(c, t)
    hook(c, t); collection(c, t); moins_cher(c, t); quoi(c, t); pression(c, t); marge(c, t)
    pertinent(c, t)
    r1 = strategie(c, t)
    exactement(c, t); aide(c, t); objectif(c, t); valeur(c, t)
    r2 = logo_monarque(c, t, T_MQ, T_POSE, T_LIM)
    fin(c, t)
    K.dessine_eclairs(c, t)
    cache = (T_STRAT - 0.1 < t < T_NE - 0.05) or (T_MQ - 0.1 < t < T_ACC - 0.05) or t > T_FIN - 0.1
    if not cache:
        SOUS.dessine(c, t, BLANC if max(r1 or 0, r2 or 0) > 1200 else ENCRE)
