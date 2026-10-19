"""GSX-M03 « Et si le fournisseur le moins cher était celui qui vous coûtait le plus cher ? » — hook 3 du client (19/10/2026).
Même forme que GSX-M01 (moteur/gsx.py). Aucun montant : les prix sont des « € » empilés, les risques des barres et des tampons.
Fil visuel : trois offres, la moins chère se retourne (face cachée rouge) → les risques claquent → acheter mieux → GSX."""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import Groupe, eclats, entre, curseur, clic, lueur_s, lettres, sous_titres, rayons
from studio3d import Cam, Plan, coins, scene3d, Balance
from gsx import *
import gsx

polices(P)
DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 1.9, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = sous_titres(K)
CX = 510

T_MEILL, T_MAIS, T_MOINS, T_ETAIT, T_COUTAIT, T_PLUS = TW(9), TW(11), TW(16), TW(18), TW(23), TW(25)
T_UN, T_GAR, T_QUAL, T_RESP, T_FIAB = TW(27), TW(31), TW(34), TW(37), TW(42)
T_PROD, T_NONC, T_LIVR, T_RET, T_FRAIS, T_IMPR, T_COMPR, T_RENT = TW(45), TW(47), TW(49), TW(51), TW(53), TW(55), TW(58), TW(60)
T_ET, T_PROB, T_APP, T_TROP, T_TARD = TW(64), TW(67), TW(68), TW(72), TW(73)
T_UNS, T_EFF, T_PAYER, T_MOINS2 = TW(77), TW(79), TW(85), TW(86)
T_IL, T_COMP, T_EVAL, T_NEGO, T_COND, T_CONC, T_QUAL2, T_COUTS, T_RENT2 = TW(88), TW(91), TW(94), TW(99), TW(102), TW(104), TW(105), TW(106), TW(108)
T_LE, T_DEP, T_MOINS3, T_MAIS3, T_ACH, T_MIEUX = TW(109), TW(115), TW(116), TW(117), TW(118), TW(119)
T_CEST, T_GSX, T_NOUS = TW(120), TW(123), TW(125)
T_RECH, T_ANAL, T_NEGO2, T_FABS, T_OBJ, T_BONS, T_SECU, T_DECIS = TW(130), TW(133), TW(138), TW(141), TW(144), TW(153), TW(157), TW(159)
T_FIN = TW(161)

RUSHES = ["rushes/presses-jaunes", "rushes/tissu-machine", "rushes/valises-moulage", "rushes/chaine-electronique",
          "rushes/entrepot-bleu", "rushes/atelier-valises"]


def euros(c, cx, cy, n, taille, couleur, alpha=1.0, total=None):
    """« € » empilés : le niveau de prix sans montant"""
    total = total or n
    w = largeur("€", taille, "archivo", 0) * 1.05
    x0 = cx - w * total / 2
    for j in range(total):
        texte(c, "€", x0 + j * w + w / 2, cy - hauteurLigne(taille, "archivo") / 2, taille, couleur if j < n else "#D5DAE3", "archivo", "centre", 0, alpha)


def carte_offre(nom, lab, n, t0, choisi_t=None):
    def f(c, w, h):
        t = gsx.T_COURANT[0]
        on = choisi_t is not None and t > choisi_t
        verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 1.0, VERT if on else ROUGE)
        m = w * 0.06
        video(c, nom, m, m, w - 2 * m, int(h * 0.56), t - t0, 1.0, True, rayon=w * 0.07)
        texte(c, lab, w / 2, h * 0.64, w * 0.09, GRIS, "titre", "centre", -0.01)
        euros(c, w / 2, h * 0.82, n, w * 0.16, VERT if on else ENCRE, total=3)
        if on:
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, 0, w, h), w * 0.1, w * 0.1)
            c.drawRRect(rr, peinture(VERT, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        balayage(c, 0, 0, w, h, t, w * 0.1, 0.4, 0.4)
    return f


def dos_rouge(c, w, h):
    """la face cachée de l'offre la moins chère"""
    t = gsx.T_COURANT[0]
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeWH(w, h), w * 0.1, w * 0.1)
    c.drawRRect(rr, pgrad_(0, 0, w, h, [ROUGE, "#A80020"]))
    c.drawRRect(rr, peinture("#FFFFFF", 0.4, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
    icone(c, "trending-up", w / 2, h * 0.26, w * 0.36, BLANC, 2.8)
    texte(c, "LE PLUS", w / 2, h * 0.46, w * 0.13, BLANC, "archivo", "centre", -0.02)
    texte(c, "CHER", w / 2, h * 0.46 + w * 0.15, w * 0.13, BLANC, "archivo", "centre", -0.02)
    euros(c, w / 2, h * 0.84, 5, w * 0.12, BLANC, 0.9 + 0.1 * math.sin(t * 8))


# ─────────────────────────────────────────── 1 · hook : le meilleur prix… et si le moins cher coûtait le plus cher ?
OFFRES = [("rushes/tissu-machine", "Fournisseur A", 3), ("rushes/presses-jaunes", "Fournisseur B", 2), ("rushes/valises-moulage", "Fournisseur C", 1)]


def scene_offres(c, t):
    t1 = T_UN - 0.12
    g = Groupe(c, t, -1, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        flip = prog(t, T_ETAIT - 0.1, 0.55, entreeSortie)
        cam = Cam(ax=-10 + 2 * math.sin(t * 1.1), ay=5 * math.sin(t * 0.8), tz=0, cx=CX, cy=1000)
        CW, CH = 260, 420
        plans = []
        for k, (nom, lab, n) in enumerate(OFFRES):
            u = prog(t, -0.5 + 0.1 * k, 0.6, lambda v: ressort(v, 1.3, 4.6))
            elu = k == 2
            avant = prog(t, T_MOINS - 0.1, 0.4, sortie) if elu else 0.0
            x = mix(280, 0, avant) if elu else (k - 1) * 280
            z = mix(1300, 0, min(u, 1.05)) - 260 * avant
            al = borne(u * 3) * (1 - 0.6 * prog(t, T_MOINS, 0.3) * (not elu))
            ay = (k - 1) * -10
            if elu and flip > 0:
                ang = 180 * flip
                if ang < 90:
                    plans.append(Plan(coins((x, 0, z), CW, CH, ay=ang), CW, CH, carte_offre(nom, lab, n, -0.5, T_MOINS), al))
                else:
                    plans.append(Plan(coins((x, 0, z), CW, CH, ay=ang - 180), CW, CH, dos_rouge, al))
            else:
                plans.append(Plan(coins((x, 0, z), CW, CH, ay=ay), CW, CH, carte_offre(nom, lab, n, -0.5, T_MOINS if elu else None), al))
        scene3d(c, cam, plans)
        # le curseur qui va chercher la moins chère
        tap = T_MOINS + 0.05
        cu = prog(t, 0.3, tap - 0.3, entreeSortie)
        if t < T_ETAIT:
            ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
            curseur(c, mix(860, 820, cu) - 300 * prog(t, T_MOINS - 0.1, 0.4, sortie), mix(1420, 1120, cu), 1.3, 1 - prog(t, T_ETAIT - 0.2, 0.2), ap)
            if t > tap: clic(c, CX - 10, 1100, t, tap, VERT)
        pill_v(c, "Le moins cher", CX, 1300, entre(t, T_MOINS, 0.4, 2.2) * (1 - flip), "badge-check", VERT, plein=True)
        if flip > 0.5:
            onde(c, CX, 1000, t, T_ETAIT + 0.2, 90, 520, ROUGE, 10, 0.6)
            eclats(c, CX, 1000, t, T_ETAIT + 0.2, 14, 420, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=3)
            pill_v(c, "Vous coûte le plus cher", CX, 1300, entre(t, T_COUTAIT - 0.1, 0.4, 2.2), "trending-up", plein=True)
    titre2(c, t, "EN SOURCING, TOUT LE MONDE", "CHERCHE LE MEILLEUR PRIX", -0.6, T_MAIS - 0.1, t2=-0.5)
    titre2(c, t, "ET SI LE MOINS CHER", "VOUS COÛTAIT LE PLUS CHER ?", T_MAIS - 0.1, t1, t2=T_COUTAIT - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 2 · un prix attractif ne garantit ni la qualité, ni les délais, ni la fiabilité
GARANTIES = [(T_QUAL, "badge-check", "La qualité", "LA QUALITÉ"), (T_RESP, "clock", "Le respect des délais", "LES DÉLAIS"),
             (T_FIAB, "shield-check", "La fiabilité du fabricant", "LA FIABILITÉ")]


def scene_garanties(c, t):
    t0, t1 = T_UN - 0.12, T_PROD - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.6)
        c.save(); c.translate(CX, 680); c.rotate(-3 + 2 * math.sin(t * 2)); s = mix(0.4, 1, a); c.scale(s, s)
        with Calque(c, borne(a * 3)):
            verre_clair(c, -300, -80, 600, 160, 50, 1.0, 1.0, VERT)
            tuile_v(c, "euro", -220, 0, 100, VERT)
            texte(c, "Un prix attractif", -150, -hauteurLigne(46, "archivo") / 2, 46, ENCRE, "archivo", track=-0.02)
        c.restore()
        for k, (tk, ic, lab, _) in enumerate(GARANTIES):
            rangee(c, t, CX, 870 + k * 160, 720, ic, lab, tk, "ko", tk + 0.4)
        titre2(c, t, "UN PRIX ATTRACTIF", "NE GARANTIT NI…", T_UN - 0.05, T_QUAL - 0.1, t2=T_GAR - 0.05)
        for k, (tk, _, _, l2) in enumerate(GARANTIES):
            fin = GARANTIES[k + 1][0] - 0.1 if k < 2 else t1
            titre2(c, t, "NI" if k else "NE GARANTIT NI", l2, tk - 0.1, fin, t2=tk - 0.05, e2="ressort", c2=ROUGE)


# ─────────────────────────────────────────── 3 · non conforme, retard, frais imprévus → la rentabilité plonge
def carte_tampon(dessin, label, t0):
    def f(c, w, h):
        dessin(c, w, h)
        tampon(c, label, w / 2, h * 0.5, gsx.T_COURANT[0], t0, w * 0.1, ROUGE, -9)
    return f


RISQUES = [(T_PROD, "NON CONFORME", T_NONC), (T_LIVR, "RETARDÉE", T_RET), (T_FRAIS, "IMPRÉVUS", T_IMPR)]


def scene_risques(c, t):
    t0, t1 = T_PROD - 0.12, T_ET - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="gauche", d_out=0.3)
    if not g.visible: return
    with g:
        chute = prog(t, T_COMPR - 0.15, 0.5, entreeSortie)
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.9), ay=6 * math.sin(t * 0.7), tz=mix(0, 700, chute), cx=CX, cy=mix(1000, 760, chute))
        CW, CH = 270, 420
        dess = [carte_tampon(carte_rush("rushes/valises-moulage", t0), "NON CONFORME", T_NONC + 0.05),
                carte_tampon(carte_ic("truck", "Livraison", "retardée"), "RETARD", T_RET + 0.05),
                carte_tampon(carte_ic("receipt", "Frais", "imprévus"), "IMPRÉVUS", T_IMPR + 0.05)]
        plans = []
        for k, (tk, _, _) in enumerate(RISQUES):
            u = prog(t, tk - 0.12, 0.45, lambda v: ressort(v, 1.3, 4.8)) if t > tk - 0.12 else 0.0
            if u <= 0: continue
            plans.append(Plan(coins(((k - 1) * 290, 20, mix(1800, 0, min(u, 1.05))), CW, CH, ay=mix(50 * (-1) ** k, (k - 1) * -10, min(u, 1)), az=(k - 1) * 2),
                              CW, CH, dess[k], borne(u * 3)))
        scene3d(c, cam, plans)
        for k, (tk, _, _) in enumerate(RISQUES):
            if t > tk and chute < 0.5:
                eclats(c, CX + (k - 1) * 290, 1020, t, tk + 0.1, 10, 280, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=11 + k)
        if chute > 0:
            # la rentabilité qui plonge
            c.save(); c.translate(0, 220 * (1 - chute))
            with Calque(c, chute):
                verre_clair(c, 150, 960, 720, 340, 44, 1.0, 1.0)
                texte(c, "RENTABILITÉ", 200, 995, 32, ENCRE, "archivo", track=0.04)
                icone(c, "trending-down", 820, 1015, 46, ROUGE, 2.6)
                u = prog(t, T_RENT - 0.05, 0.9, entreeSortie)
                path = skia.Path(); path.moveTo(200, 1110)
                for i in range(1, int(60 * u) + 1):
                    v = i / 60
                    path.lineTo(200 + v * 620, 1110 - 30 * math.sin(v * 6) + 140 * v ** 2)
                pe = peinture(ROUGE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=9); pe.setStrokeCap(skia.Paint.kRound_Cap)
                c.drawPath(path, pe)
            c.restore()
        titre2(c, t, "UN PRODUIT", "NON CONFORME", T_PROD - 0.1, T_LIVR - 0.1, t2=T_NONC - 0.1, c2=ROUGE)
        titre2(c, t, "UNE LIVRAISON", "RETARDÉE", T_LIVR - 0.1, T_FRAIS - 0.1, t2=T_RET - 0.1, c2=ROUGE)
        titre2(c, t, "DES FRAIS", "IMPRÉVUS", T_FRAIS - 0.1, T_COMPR - 0.15, t2=T_IMPR - 0.1, c2=ROUGE)
        titre2(c, t, "ET VOTRE COMMANDE", "N'EST PLUS RENTABLE", T_COMPR - 0.15, t1, t2=T_RENT - 0.1)


# ─────────────────────────────────────────── 4 · quand les problèmes apparaissent, il est trop tard
JALONS = [("Commande", "file-text"), ("Production", "factory"), ("Livraison", "truck")]


def scene_tard(c, t):
    t0, t1 = T_ET - 0.12, T_UNS - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="zoom", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        y = 900; x0, x1 = CX - 300, CX + 300
        p = prog(t, t0, T_APP - t0 + 0.2, lin)
        rrect(c, x0, y - 6, x1 - x0, 12, 6, "#D5DAE3")
        rrect(c, x0, y - 6, (x1 - x0) * p, 12, 6, ENCRE)
        for i, (lab, ic) in enumerate(JALONS):
            x = x0 + i * (x1 - x0) / 2
            on = p >= i / 2 - 0.01
            c.save(); c.translate(x, y)
            verre_clair(c, -70, -70, 140, 140, 40, 1.0, 0.6 if on else 0.0)
            icone(c, ic, 0, 0, 64, ENCRE if on else "#B8BEC8", 2.6)
            c.restore()
            texte(c, lab, x, y + 90, 30, ENCRE if on else GRIS, "titre", "centre", -0.01)
        pb = entre(t, T_APP - 0.05, 0.4, 2.2)
        if pb > 0:
            c.save(); c.translate(x1, y - 150); c.scale(mix(0.3, 1, pb), mix(0.3, 1, pb))
            disque(c, 0, 0, 52, ROUGE, borne(pb * 3), (10, 26, 0.3)); icone(c, "triangle-alert", 0, -2, 56, BLANC, 2.6, borne(pb * 3))
            c.restore()
            onde(c, x1, y - 150, t, T_APP, 60, 260, ROUGE, 6, 0.5)
        h = entre(t, T_TROP - 0.15, 0.45, 2.0)
        if h > 0:
            c.save(); c.translate(CX, 1170); c.rotate(10 * math.sin(t * 3)); c.scale(mix(0.3, 1, h), mix(0.3, 1, h))
            verre_clair(c, -80, -80, 160, 160, 46, borne(h * 3)); icone(c, "hourglass", 0, 0, 84, ENCRE, 2.6, borne(h * 3))
            c.restore()
        if t > T_TARD: tampon(c, "TROP TARD", CX, 1170, t, T_TARD + 0.05, 64, ROUGE, -8)
        titre2(c, t, "QUAND LES PROBLÈMES", "APPARAISSENT", T_ET - 0.05, T_TROP - 0.15, t2=T_APP - 0.1)
        titre2(c, t, "IL EST SOUVENT", "TROP TARD", T_TROP - 0.15, t1, t2=T_TARD - 0.05, c2=ROUGE)


# ─────────────────────────────────────────── 5 · un sourcing efficace : comparer, évaluer, négocier, concilier
CRITERES = ["Qualité", "Délais", "Prix"]


def carte_eval(nom, t0, notes):
    def f(c, w, h):
        t = gsx.T_COURANT[0]
        verre_clair(c, 0, 0, w, h, w * 0.1)
        m = w * 0.06
        video(c, nom, m, m, w - 2 * m, int(h * 0.48), t - t0, 1.0, True, rayon=w * 0.07)
        e = prog(t, T_EVAL - 0.1, 0.8, entreeSortie)
        for j, (lab, v) in enumerate(zip(CRITERES, notes)):
            y = h * 0.6 + j * h * 0.12
            texte(c, lab, m + 4, y, w * 0.07, GRIS, "titre", track=-0.01)
            bx = w * 0.42; bw = w - bx - m
            rrect(c, bx, y + w * 0.02, bw, w * 0.05, w * 0.025, "#E3E7EE")
            if e > 0: rrect(c, bx, y + w * 0.02, max(w * 0.05, bw * v * e), w * 0.05, w * 0.025, ROUGE if v > 0.7 else "#9AA0AA")
        balayage(c, 0, 0, w, h, t, w * 0.1, 0.4, 0.4)
    return f


def scene_efficace(c, t):
    t0, t1 = T_UNS - 0.12, T_LE - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        comp = prog(t, T_IL - 0.15, 0.5, entreeSortie)
        venn = prog(t, T_CONC - 0.15, 0.55, entreeSortie)
        if comp < 1:
            with Calque(c, 1 - comp):
                a = entre(t, t0, 0.5, 1.6)
                c.save(); c.translate(CX, 900); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
                verre_clair(c, -320, -90, 640, 180, 60, borne(a * 3), 0.3)
                icone(c, "euro", -230, 0, 70, GRIS, 2.6)
                texte(c, "Payer moins cher", -170, -hauteurLigne(52, "archivo") / 2, 52, GRIS, "archivo", track=-0.02)
                b = prog(t, T_MOINS2 + 0.1, 0.3, sortie)
                if b > 0: trait(c, -260, 0, -260 + 540 * b, 0, ROUGE, 8)
                c.restore()
                croix_v(c, CX + 300, 820, 46, entre(t, T_MOINS2 + 0.3, 0.35, 2.4))
        if comp > 0 and venn < 1:
            cam = Cam(ax=-10 + 2 * math.sin(t), ay=6 * math.sin(t * 0.7), tz=mix(600, 40, comp) + 900 * venn, cx=CX, cy=980)
            CW, CH = 270, 470
            notes = [(0.9, 0.6, 0.5), (0.5, 0.8, 0.8), (0.4, 0.4, 0.95)]
            plans = []
            for k, nom in enumerate(["rushes/presses-jaunes", "rushes/tissu-machine", "rushes/cartons-ouvrieres"]):
                u = prog(t, T_COMP - 0.15 + 0.08 * k, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_COMP - 0.15 + 0.08 * k else 0.0
                if u <= 0: continue
                plans.append(Plan(coins(((k - 1) * 290, 0, mix(900, 0, min(u, 1.05))), CW, CH, ay=(k - 1) * -10), CW, CH,
                                  carte_eval(nom, t0, notes[k]), borne(u * 3) * (1 - venn)))
            scene3d(c, cam, plans)
            pill_v(c, "Négocier les bonnes conditions", CX, 1300, entre(t, T_NEGO - 0.1, 0.4, 2.2) * (1 - venn), "scale", plein=True)
        if venn > 0:
            cy = 960
            for k, (lab, tk, ang) in enumerate([("Qualité", T_QUAL2, -90), ("Coûts", T_COUTS, 30), ("Rentabilité", T_RENT2, 150)]):
                e = entre(t, tk - 0.12, 0.45, 1.8)
                if e <= 0: continue
                rr = mix(260, 110, prog(t, T_RENT2 + 0.2, 0.5, entreeSortie))
                x, y = CX + rr * math.cos(math.radians(ang)), cy + rr * math.sin(math.radians(ang))
                p = skia.Paint(AntiAlias=True)
                p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), 190, [hexa([ROUGE, ENCRE, VERT][k], 0.16 * borne(e * 2)), hexa([ROUGE, ENCRE, VERT][k], 0.04 * borne(e * 2))]))
                c.drawCircle(x, y, 190 * min(e, 1.1), p)
                anneau(c, x, y, 190 * min(e, 1.1), [ROUGE, ENCRE, VERT][k], 4, 0.8 * borne(e * 2))
                lx, ly = CX + 300 * math.cos(math.radians(ang)), cy + 300 * math.sin(math.radians(ang))
                pill_v(c, lab, lx, ly, e, None, [ROUGE, ENCRE, VERT][k], taille=30, plein=True)
            coche_v(c, CX, cy, 50, entre(t, T_RENT2 + 0.6, 0.35, 2.4))
            if t > T_RENT2 + 0.6: eclats(c, CX, cy, t, T_RENT2 + 0.6, 14, 360, cols=[ROUGE, VERT, ENCRE], graine=6)
        titre2(c, t, "UN SOURCING EFFICACE", "CE N'EST PAS PAYER MOINS", T_UNS - 0.05, T_IL - 0.1, t2=T_PAYER - 0.15)
        for (a_, b_, l1, l2) in [(T_IL - 0.1, T_EVAL - 0.1, "IL S'AGIT DE", "COMPARER LES OFFRES"), (T_EVAL - 0.1, T_NEGO - 0.1, None, "ÉVALUER LES FOURNISSEURS"),
                                 (T_NEGO - 0.1, T_CONC - 0.15, None, "NÉGOCIER"), (T_CONC - 0.15, t1, "POUR CONCILIER", "QUALITÉ, COÛTS, RENTABILITÉ")]:
            titre2(c, t, l1, l2, a_, b_, t2=a_ + 0.05)


# ─────────────────────────────────────────── 6 · dépenser moins → acheter mieux
def scene_mieux(c, t):
    t0, t1 = T_LE - 0.12, T_CEST + 0.2
    g = Groupe(c, t, t0, t1, ent="bas", sor="aucune", d_in=0.35)
    if not g.visible: return
    with g:
        a = entre(t, T_DEP - 0.15, 0.45, 1.8)
        if a > 0:
            c.save(); c.translate(CX, 820); c.rotate(-3); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
            verre_clair(c, -330, -90, 660, 180, 56, borne(a * 3), 0.3)
            texte(c, "DÉPENSER MOINS", 0, -hauteurLigne(56, "archivo") / 2, 56, GRIS, "archivo", "centre", -0.02, borne(a * 3))
            b = prog(t, T_MOINS3 + 0.15, 0.3, sortie)
            if b > 0: trait(c, -290, 0, -290 + 580 * b, 0, ROUGE, 9)
            c.restore()
        m = entre(t, T_ACH - 0.1, 0.5, 2.0)
        if m > 0:
            sx, sy = secousse(t, T_MIEUX, 12, 0.3)
            c.save(); c.translate(CX + sx, 1080 + sy); c.rotate(2); c.scale(mix(0.3, 1.0, m), mix(0.3, 1.0, m))
            tw = largeur("ACHETER MIEUX", 56, "archivo", -0.02); W2 = tw + 190
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-W2 / 2, -95, W2, 190), 60, 60)
            p = skia.Paint(AntiAlias=True, Color=hexa(ROUGE, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
            c.save(); c.translate(0, 20); c.drawRRect(rr, p); c.restore()
            c.drawRRect(rr, pgrad_(-W2 / 2, -95, W2 / 2, 95, [ROUGE, "#A80020"]))
            texte(c, "ACHETER MIEUX", -W2 / 2 + 46, -hauteurLigne(56, "archivo") / 2, 56, BLANC, "archivo", track=-0.02)
            disque(c, W2 / 2 - 80, 0, 44, BLANC); icone(c, "check", W2 / 2 - 80, 0, 52, ROUGE, 3.4)
            c.restore()
            onde(c, CX, 1080, t, T_MIEUX, 100, 520, ROUGE, 8, 0.5)
            eclats(c, CX, 1080, t, T_MIEUX, 14, 420, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=8)
        titre2(c, t, "LE VÉRITABLE OBJECTIF", None, T_LE - 0.05, t1 - 0.2)


# ─────────────────────────────────────────── 7 · disque GSX, puis l'accompagnement
def scene_gsx(c, t):
    return disque_gsx(c, t, T_CEST, T_GSX, T_NOUS, CX, 1000, "C'EST LÀ QUE")


AIDES = [(T_RECH, "rushes/entrepot-bleu", "Recherche", "search"), (T_ANAL, "rushes/tissu-machine", "Analyse", "eye"),
         (T_NEGO2, "rushes/atelier-valises", "Négociation", "scale")]


def scene_aide(c, t):
    t0, t1 = T_NOUS - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="aucune", sor="recul", d_out=0.4)
    if not g.visible: return
    with g:
        choix = prog(t, T_OBJ - 0.15, 0.6, entreeSortie)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-10, 6, prog(t, t0, 2, douce)) + 4 * math.sin(t * 0.8), tz=mix(0, -80, choix), cx=CX, cy=980)
        CW, CH = 270, 440
        plans = []
        for k, (tk, nom, lab, ic) in enumerate(AIDES):
            u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            x = (k - 1) * 285 * (1 - 0.15 * choix)
            z = mix(1500, 0, min(u, 1.05)) + (300 * choix if k != 1 else -200 * choix)
            plans.append(Plan(coins((x, 0, z), CW, CH, ay=(k - 1) * -10), CW, CH,
                              carte_rush(nom, t0, label=lab, ic=ic, accent=VERT if (k == 1 and t > T_BONS) else ROUGE),
                              borne(u * 3) * (1 - 0.6 * choix * (k != 1))))
        scene3d(c, cam, plans)
        pill_v(c, "Avec les fabricants en Chine", CX, 1300, entre(t, T_FABS - 0.1, 0.4, 2.2) * (1 - choix), "factory", plein=True)
        coche_v(c, CX + 120, 760, 48, entre(t, T_BONS, 0.35, 2.4))
        if t > T_BONS: eclats(c, CX, 980, t, T_BONS + 0.05, 12, 340, cols=[VERT, ROUGE, ENCRE], graine=4)
        s = entre(t, T_SECU - 0.1, 0.45, 2.0)
        if s > 0:
            c.save(); c.translate(CX, 1290); c.scale(mix(0.3, 1, s), mix(0.3, 1, s))
            w = largeur("Décisions d'achat sécurisées", 32, "titre", -0.01) + 140
            verre_clair(c, -w / 2, -48, w, 96, 48, borne(s * 3), 1.0)
            ferme = prog(t, T_DECIS, 0.25, sortie)
            icone(c, "lock" if ferme > 0.5 else "lock-open", -w / 2 + 56, 0, 44, ROUGE, 2.6, borne(s * 3))
            texte(c, "Décisions d'achat sécurisées", -w / 2 + 96, -hauteurLigne(32, "titre") / 2, 32, ENCRE, "titre", track=-0.01, alpha=borne(s * 3))
            c.restore()
        for (a_, b_, l1, l2) in [(T_NOUS - 0.05, T_ANAL - 0.1, "NOUS VOUS ACCOMPAGNONS", "RECHERCHE DE FOURNISSEURS"),
                                 (T_ANAL - 0.1, T_NEGO2 - 0.1, None, "ANALYSE DES OFFRES"), (T_NEGO2 - 0.1, T_OBJ - 0.15, None, "NÉGOCIATION"),
                                 (T_OBJ - 0.15, T_SECU - 0.1, "NOTRE OBJECTIF", "LES BONS PARTENAIRES"), (T_SECU - 0.1, T_FIN - 0.05, "SÉCURISER", "VOS DÉCISIONS D'ACHAT")]:
            titre2(c, t, l1, l2, a_, b_, t2=a_ + 0.05, c2=ROUGE if l2 == "LES BONS PARTENAIRES" else ENCRE)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8)
for k in range(3): son(-0.5 + 0.1 * k + 0.55, "pop", -12)
son(T_MOINS + 0.05, "clic", -6); son(T_MOINS + 0.1, "check", -10)
son(T_ETAIT - 0.1, "whoosh", -8); son(T_ETAIT + 0.2, "impact", -5); son(T_COUTAIT - 0.1, "pop", -9)
son(T_UN - 0.12, "swipe", -9)
for tk, _, _, _ in GARANTIES: son(tk - 0.12, "whoosh_court", -10); son(tk + 0.4, "croc", -10)
for tk, _, t_t in RISQUES: son(tk - 0.15, "whoosh", -9); son(tk + 0.05, "impact", -7); son(t_t + 0.05, "tampon", -7)
son(T_COMPR - 0.15, "whoosh_bas", -8); son(T_RENT, "montee", -14)
son(T_ET - 0.12, "whoosh_court", -9); son(T_APP - 0.05, "impact_doux", -7); son(T_TROP - 0.15, "pop", -10); son(T_TARD + 0.05, "tampon", -5)
son(T_UNS - 0.12, "swipe", -9); son(T_MOINS2 + 0.1, "swipe", -10); son(T_MOINS2 + 0.3, "croc", -9)
son(T_IL - 0.15, "whoosh", -9)
for k in range(3): son(T_COMP - 0.15 + 0.08 * k, "pop", -12)
son(T_EVAL - 0.1, "montee", -14); son(T_NEGO - 0.1, "pop", -10)
son(T_CONC - 0.15, "whoosh_bas", -8)
for tk in (T_QUAL2, T_COUTS, T_RENT2): son(tk - 0.12, "pop", -9)
son(T_RENT2 + 0.6, "check", -8); son(T_RENT2 + 0.62, "ching", -10)
son(T_DEP - 0.15, "pop", -10); son(T_MOINS3 + 0.15, "swipe", -9); son(T_ACH - 0.1, "whoosh", -8); son(T_MIEUX, "impact", -5); son(T_MIEUX + 0.05, "ching", -9)
son(T_CEST - 0.1, "whoosh_bas", -7); son(T_GSX - 0.1, "montee", -11); son(T_GSX, "impact", -4); son(T_GSX + 0.05, "ching", -9)
for tk, _, _, _ in AIDES: son(tk - 0.15, "whoosh_court", -9); son(tk, "impact_doux", -10)
son(T_FABS - 0.1, "pop", -10); son(T_OBJ - 0.15, "whoosh", -9); son(T_BONS, "check", -8); son(T_SECU - 0.1, "pop", -9); son(T_DECIS, "clic", -6)
sons_signature(son, T_FIN)
for tl in (TW(162), TW(169)): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_ETAIT - 0.1, T_ETAIT + 0.4), (T_UN - 0.15, T_UN + 0.25), (T_PROD - 0.15, T_PROD + 0.2), (T_COMPR - 0.15, T_COMPR + 0.3),
             (T_ET - 0.15, T_ET + 0.25), (T_UNS - 0.15, T_UNS + 0.25), (T_IL - 0.15, T_IL + 0.3), (T_CONC - 0.15, T_CONC + 0.3),
             (T_LE - 0.15, T_LE + 0.25), (T_NOUS - 0.15, T_NOUS + 0.25), (T_OBJ - 0.15, T_OBJ + 0.3), (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_ETAIT + 0.2, ROUGE, 0.07), (T_TARD + 0.05, ROUGE, 0.06), (T_MIEUX, "#FFFFFF", 0.1), (T_GSX, "#FFFFFF", 0.12), (T_BONS, VERT, 0.05)]:
    eclair(tt, cc_, a_)


SIGN_MEDIAS = [(n, True) for n in RUSHES]


def dessine(c, t):
    gsx.T_COURANT[0] = t
    fond_clair(c, t)
    scene_offres(c, t)
    with Balance(c, t, 0.8):
        scene_garanties(c, t); scene_risques(c, t); scene_tard(c, t); scene_efficace(c, t); scene_mieux(c, t)
    r = scene_gsx(c, t)
    with Balance(c, t, 0.8):
        if r < 2100: scene_aide(c, t)
    entete(c, t, T_NOUS - 0.05, T_FIN)
    signature_gsx(c, t, T_FIN, SIGN_MEDIAS, [("Ne cherchez pas seulement le meilleur prix.", TW(162), 44, ENCRE),
                                               ("Cherchez le meilleur partenaire pour votre business.", TW(169), 44, ROUGE)], cy=840)
    K.dessine_eclairs(c, t)
    cache = (T_CEST - 0.1 < t < T_NOUS - 0.05) or t > T_FIN - 0.1
    if not cache: SOUS.dessine(c, t, ENCRE)
