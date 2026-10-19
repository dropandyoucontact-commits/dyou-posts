"""GSX-M04 « Vous connaissez votre prix d'achat. Mais maîtrisez-vous réellement votre rentabilité ? » — hook 4 du client
(19/10/2026), pédagogie. Même forme que GSX-M01 (moteur/gsx.py). Aucun montant : la tour des coûts, des barres sans chiffres.
Fil visuel : globe et activité → la marge sur le papier → la tour des coûts qui s'empile sur le prix usine → TVA, fiscalité,
CA / marge / bénéfice → le prix de vente → le partenaire stratégique → les fondations d'une stratégie d'achat → GSX."""
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

T_DEV, T_TROUVE, T_FOURN, T_NEGO, T_DEFINI = TW(7), TW(10), TW(14), TW(15), TW(19)
T_MAIS, T_MARGE, T_PAPIER, T_GAR, T_RENT = TW(24), TW(27), TW(31), TW(32), TW(37)
T_POUR, T_ALLER, T_USINE = TW(38), TW(44), TW(47)
T_CHAQUE, T_ANTI, T_COUT, T_PROJET = TW(75), TW(79), TW(83), TW(87)
T_MAISC, T_TVA, T_ANTIC, T_DIST, T_MARGEC, T_RESU = TW(88), TW(96), TW(102), TW(107), TW(109), TW(112)
T_FAIRE, T_CA, T_DEGA, T_GEN, T_BENEF, T_TROIS = TW(117), TW(119), TW(121), TW(125), TW(127), TW(129)
T_CEST, T_VISION, T_FIXER, T_PVENTE, T_COH, T_OBJ = TW(132), TW(134), TW(140), TW(142), TW(145), TW(148)
T_ET, T_CHOIX, T_PART, T_STRAT = TW(149), TW(154), TW(157), TW(161)
T_IDENT, T_NEGO2, T_EVAL, T_ANTI2 = TW(162), TW(166), TW(170), TW(177)
T_LOBJ, T_CONSTR, T_MARCHE, T_BUDGET, T_AMB = TW(181), TW(184), TW(191), TW(194), TW(198)
T_LA, T_TOUT, T_CHER, T_ELLE, T_OU, T_QUOI, T_COMMENT = TW(200), TW(206), TW(209), TW(210), TW(214), TW(216), TW(219)
T_FIN = TW(223)

RUSHES = ["rushes/entrepot-bleu", "rushes/cartons-ouvrieres", "rushes/chaine-electronique", "rushes/atelier-valises",
          "rushes/entrepot-colis", "rushes/presses-jaunes"]


# ─────────────────────────────────────────── 1 · hook : importer, développer ; fournisseur trouvé, prix négocié, prix de vente
ACQUIS = [(T_FOURN, "factory", "Fournisseur trouvé", "TROUVÉ VOTRE FOURNISSEUR"), (T_NEGO, "scale", "Prix négocié", "NÉGOCIÉ VOTRE PRIX"),
          (T_DEFINI, "euro", "Prix de vente défini", "DÉFINI VOTRE PRIX DE VENTE")]


def scene_hook(c, t):
    t1 = T_MAIS - 0.12
    g = Groupe(c, t, -1, t1, ent="aucune", sor="haut", d_out=0.3)
    if not g.visible: return
    with g:
        part = prog(t, T_TROUVE - 0.25, 0.5, entreeSortie)
        if part < 1:
            with Calque(c, 1 - part):
                o = prog(t, -0.3, 1.8, douce)
                sx, sy = secousse(t, 0.0, 14, 0.3)
                lon = mix(60, 80, o) + 3 * t
                R = 330 * mix(1, 0.6, part)
                cx, cy = CX - 60 + sx, 930 + sy
                G = globe(c, lon, 34, cx, cy, R, 1.0)
                u = prog(t, -0.4, 1.4, entreeSortie)
                for j in range(3):                       # des colis qui partent de Chine vers la France
                    uj = (t * 0.7 + j / 3) % 1
                    tete = G.arc(c, CN, FR, cx, cy, R, lon, 34, u, ROUGE, 6, 0.4, [14, 12]) if j == 0 else None
                    pts = G.trace(CN, FR, uj * u, 0.4)
                    if len(pts):
                        q = pts[-1] @ G.rot(lon, 34).T
                        if q[2] > -0.1 and uj * u > 0.05:
                            px, py = cx + R * q[0], cy - R * q[1]
                            disque(c, px, py, 30, BLANC, 0.95, (6, 16, 0.25)); icone(c, "package", px, py, 34, ROUGE, 2.4)
                # l'activité qui grandit
                a = entre(t, T_DEV - 0.15, 0.45, 1.8)
                if a > 0:
                    c.save(); c.translate(CX + 230, 1180); c.rotate(-4); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
                    verre_clair(c, -150, -110, 300, 220, 40, borne(a * 3))
                    b = prog(t, T_DEV, 0.9, entreeSortie)
                    for k in range(4):
                        hb = (30 + 34 * k) * b
                        rrect(c, -110 + k * 58, 60 - hb, 44, hb, 8, ROUGE if k == 3 else "#D5DAE3")
                    icone(c, "trending-up", 100, -66, 40, ROUGE, 2.6)
                    texte(c, "Votre activité", -126, -96, 26, ENCRE, "titre", track=-0.01)
                    c.restore()
        for k, (tk, ic, lab, _) in enumerate(ACQUIS):
            rangee(c, t, CX, 760 + k * 170, 720, ic, lab, tk - 0.05, "ok", tk + 0.3, VERT)
    titre2(c, t, "IMPORTER DEPUIS LA CHINE", "DÉVELOPPER VOTRE ACTIVITÉ ?", -0.6, T_TROUVE - 0.1, t2=-0.5)
    for k, (tk, _, _, l2) in enumerate(ACQUIS):
        a_ = T_TROUVE - 0.1 if k == 0 else tk - 0.1
        fin = ACQUIS[k + 1][0] - 0.1 if k < 2 else t1
        titre2(c, t, "VOUS AVEZ" if k == 0 else None, l2, a_, fin, t2=tk - 0.1, e2="ressort")


# ─────────────────────────────────────────── 2 · une marge sur le papier ne garantit pas un projet rentable
def scene_papier(c, t):
    t0, t1 = T_MAIS - 0.12, T_POUR - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.55, 1.5)
        sx, sy = secousse(t, T_RENT, 12, 0.3)
        c.save(); c.translate(CX + sx, 980 + sy); c.rotate(-3 + 2 * math.sin(t * 1.5)); s = mix(0.4, 1, a); c.scale(s, s)
        with Calque(c, borne(a * 3)):
            verre_clair(c, -260, -330, 520, 660, 30, 1.0, 0.6)
            rrect(c, -260, -330, 520, 70, 30, "#EEF1F6")
            icone(c, "file-text", -210, -295, 36, GRIS, 2.4); texte(c, "Votre projet", -180, -312, 30, GRIS, "titre", track=-0.01)
            for j in range(4):
                rrect(c, -210, -220 + j * 44, [380, 300, 340, 220][j], 16, 8, "#E3E7EE")
            m = prog(t, T_MARGE - 0.1, 0.7, lambda v: ressort(v, 1.2, 4.0))
            texte(c, "MARGE", -210, 0, 34, ENCRE, "archivo", track=0.04)
            rrect(c, -210, 60, 420, 40, 20, "#E3E7EE")
            if m > 0: rrect(c, -210, 60, max(40, 420 * 0.85 * m), 40, 20, VERT)
            pill_v(c, "Intéressante", 90, 150, entre(t, TW(28) - 0.1, 0.4, 2.2), "trending-up", VERT, taille=28)
        c.restore()
        if t > T_RENT - 0.1:
            tampon(c, "RENTABLE ?", CX, 1200, t, T_RENT - 0.05, 64, ROUGE, -8)
            eclats(c, CX, 1200, t, T_RENT, 12, 340, cols=[ROUGE, ENCRE], graine=4)
        titre2(c, t, "MAIS ATTENTION", "UNE MARGE SUR LE PAPIER", T_MAIS - 0.05, T_GAR - 0.1, t2=T_MARGE - 0.1)
        titre2(c, t, "NE GARANTIT PAS", "UN PROJET RENTABLE", T_GAR - 0.1, t1, t2=TW(35) - 0.05, c2=ROUGE)


# ─────────────────────────────────────────── 3 · la tour des coûts sur le prix usine
POSTES = [(TW(49), "plane", "Transport international", "TRANSPORT"), (TW(51), "landmark", "Droits de douane", "DOUANE"),
          (TW(54), "file-text", "Dédouanement", "DÉDOUANEMENT"), (TW(55), "warehouse", "Stockage", "STOCKAGE"),
          (TW(56), "package", "Préparation des commandes", "PRÉPARATION"), (TW(60), "truck", "Distribution", "DISTRIBUTION"),
          (TW(63), "badge-percent", "Commissions commerciales", "COMMISSIONS"), (TW(66), "building", "Frais de fonctionnement", "FONCTIONNEMENT"),
          (TW(71), "wallet", "Charges de l'entreprise", "CHARGES")]
BH, BG, BW = 66, 8, 560


def bloc(c, x, y, w, h, ic, lab, plein=False):
    if plein:
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 18, 18)
        p = skia.Paint(AntiAlias=True, Color=hexa(ENCRE, 0.3), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
        c.save(); c.translate(0, 10); c.drawRRect(rr, p); c.restore()
        c.drawRRect(rr, peinture(ENCRE))
        col = BLANC
    else:
        verre_clair(c, x, y, w, h, 18, 1.0, 0.6, ROUGE, 0.7)
        col = ENCRE
    icone(c, ic, x + 44, y + h / 2, 34, BLANC if plein else ROUGE, 2.4)
    texte(c, lab, x + 82, y + h / 2 - hauteurLigne(32, "titre") / 2, ajuste(lab, w - 100, 32, "titre", -0.01), col, "titre", track=-0.01)


def scene_tour(c, t):
    t0, t1 = T_POUR - 0.12, T_MAISC - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        base_y = 1310
        x = CX - BW / 2
        u0 = entre(t, T_ALLER - 0.15, 0.45, 1.8)
        if u0 > 0:
            c.save(); c.translate(CX, base_y - BH / 2); c.scale(mix(0.4, 1, u0), mix(0.4, 1, u0)); c.translate(-CX, -(base_y - BH / 2))
            with Calque(c, borne(u0 * 3)): bloc(c, x, base_y - BH, BW, BH, "factory", "Prix usine", True)
            c.restore()
        n_on = 0
        for k, (tk, ic, lab, _) in enumerate(POSTES):
            d = prog(t, tk - 0.12, 0.42, lambda v: ressort(v, 1.3, 5.0)) if t > tk - 0.12 else 0.0
            if d <= 0: continue
            n_on = k + 1
            y = base_y - BH - (k + 1) * (BH + BG)
            yy = y - 700 * (1 - min(d, 1.0))
            c.save(); c.translate(CX, yy + BH / 2); c.rotate(((-1) ** k) * 6 * (1 - min(d, 1))); c.translate(-CX, -(yy + BH / 2))
            with Calque(c, borne(d * 4)): bloc(c, x, yy, BW, BH, ic, lab)
            c.restore()
            if t < tk + 0.4: eclats(c, CX, y + BH, t, tk + 0.18, 8, 220, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=20 + k)
        # coût réel : accolade rouge sur toute la tour
        r = prog(t, T_COUT - 0.15, 0.5, entreeSortie)
        if r > 0:
            haut = base_y - BH - len(POSTES) * (BH + BG)
            xb = x + BW + 26
            yb = mix(base_y, haut, r)
            trait(c, xb, base_y, xb, yb, ROUGE, 6); trait(c, xb - 14, base_y, xb, base_y, ROUGE, 6); trait(c, xb - 14, yb, xb, yb, ROUGE, 6)
            c.save(); c.translate(xb + 34, (base_y + haut) / 2); c.rotate(-90)
            texte(c, "COÛT RÉEL", 0, -hauteurLigne(40, "archivo") / 2, 40, ROUGE, "archivo", "centre", 0.04, r)
            c.restore()
            trait(c, x - 26, base_y, x - 26, base_y - BH, ENCRE, 6, r)
        titre2(c, t, "POUR STRUCTURER VOS ACHATS", "AU-DELÀ DU PRIX USINE", T_POUR - 0.05, POSTES[0][0] - 0.1, t2=T_ALLER - 0.1)
        for k, (tk, _, _, l2) in enumerate(POSTES):
            fin = POSTES[k + 1][0] - 0.06 if k < len(POSTES) - 1 else T_CHAQUE - 0.1
            titre2(c, t, "AJOUTEZ" if k >= 6 else None, l2, tk - 0.08, fin, t2=tk - 0.08, e2="masque", grand=96)
        titre2(c, t, "CHAQUE POSTE ANTICIPÉ", "LE COÛT RÉEL", T_CHAQUE - 0.1, t1, t2=T_COUT - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 4 · TVA, fiscalité, marge ≠ résultat ; CA, marge, bénéfice
def barre_lab(c, x, y, w, v, lab, col, a=1.0):
    if a <= 0.01: return
    with Calque(c, borne(a * 3)):
        texte(c, lab, x, y - 44, 30, ENCRE, "titre", track=-0.01)
        rrect(c, x, y, w, 46, 23, "#E3E7EE")
        if v > 0: rrect(c, x, y, max(46, w * v), 46, 23, col)


def scene_fiscal(c, t):
    t0, t1 = T_MAISC - 0.12, T_CEST - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        dist = prog(t, T_DIST - 0.15, 0.5, entreeSortie)
        ent3 = prog(t, T_FAIRE - 0.15, 0.5, entreeSortie)
        if dist < 1:
            cam = Cam(ax=-10 + 2 * math.sin(t), ay=6 * math.sin(t * 0.8), tz=mix(0, 900, dist), cx=CX, cy=980)
            CW, CH = 300, 420
            plans = []
            for k, (tk, ic, lab, sous) in enumerate([(T_TVA, "receipt", "TVA", "son traitement"), (T_ANTIC, "landmark", "Fiscalité", "vos obligations")]):
                u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > tk - 0.15 else 0.0
                if u <= 0: continue
                plans.append(Plan(coins(((k - 0.5) * 330, 0, mix(1500, 0, min(u, 1.05))), CW, CH, ay=(k - 0.5) * -20), CW, CH, carte_ic(ic, lab, sous), borne(u * 3) * (1 - dist)))
            scene3d(c, cam, plans)
            if t < T_TVA: pill_v(c, "Ce n'est pas tout", CX, 980, entre(t, T_MAISC, 0.4, 2.2), "triangle-alert", plein=True)
        if dist > 0 and ent3 < 1:
            with Calque(c, dist * (1 - ent3)):
                verre_clair(c, 150, 760, 720, 420, 44)
                barre_lab(c, 210, 880, 600, prog(t, T_MARGEC - 0.1, 0.7, entreeSortie) * 0.9, "Marge commerciale", ENCRE, entre(t, T_MARGEC - 0.15, 0.4, 2.0))
                barre_lab(c, 210, 1060, 600, prog(t, T_RESU - 0.1, 0.7, entreeSortie) * 0.45, "Résultat réel", ROUGE, entre(t, T_RESU - 0.15, 0.4, 2.0))
        if ent3 > 0:
            # entonnoir : chiffre d'affaires > marge > bénéfice (largeurs seulement, aucun chiffre)
            for k, (tk, lab, w, col) in enumerate([(T_CA, "Chiffre d'affaires", 720, "#9AA0AA"), (T_DEGA, "Marge", 520, ENCRE), (T_GEN, "Bénéfice", 320, ROUGE)]):
                u = entre(t, tk - 0.12, 0.45, 1.8)
                if u <= 0: continue
                y = 780 + k * 150
                c.save(); c.translate(CX, y); c.scale(mix(0.3, 1, u), 1)
                with Calque(c, borne(u * 3)):
                    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -55, w, 110), 34, 34)
                    p = skia.Paint(AntiAlias=True, Color=hexa(col, 0.3), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
                    c.save(); c.translate(0, 12); c.drawRRect(rr, p); c.restore()
                    c.drawRRect(rr, peinture(col))
                    texte(c, lab, 0, -hauteurLigne(36, "archivo") / 2, ajuste(lab, w - 40, 36, "archivo", -0.02), BLANC, "archivo", "centre", -0.02)
                c.restore()
            pill_v(c, "Trois choses différentes", CX, 1290, entre(t, T_TROIS - 0.1, 0.4, 2.2), "split", plein=True)
        titre2(c, t, None, "MAIS CE N'EST PAS TOUT", T_MAISC - 0.05, T_TVA - 0.1, t2=T_MAISC)
        titre2(c, t, "MAÎTRISER", "LA TVA", T_TVA - 0.1, T_ANTIC - 0.1, t2=TW(101) - 0.1)
        titre2(c, t, "ANTICIPER", "VOS OBLIGATIONS FISCALES", T_ANTIC - 0.1, T_DIST - 0.15, t2=T_ANTIC)
        titre2(c, t, "DISTINGUER LA MARGE", "DU RÉSULTAT RÉEL", T_DIST - 0.15, T_FAIRE - 0.15, t2=T_RESU - 0.1, c2=ROUGE)
        titre2(c, t, "CHIFFRE D'AFFAIRES, MARGE, BÉNÉFICE", "TROIS CHOSES DIFFÉRENTES", T_FAIRE - 0.15, t1, t2=T_TROIS - 0.1)


# ─────────────────────────────────────────── 5 · la vision globale fixe un prix de vente cohérent
ORBITE = [("factory", "Prix usine"), ("plane", "Transport"), ("landmark", "Douane"), ("receipt", "TVA"), ("wallet", "Charges"), ("trending-up", "Marge")]


def scene_prix(c, t):
    t0, t1 = T_CEST - 0.12, T_ET - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="zoom", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        fixe = prog(t, T_FIXER - 0.1, 0.5, entreeSortie)
        cy = 980
        for k, (ic, lab) in enumerate(ORBITE):
            e = entre(t, T_VISION - 0.2 + 0.06 * k, 0.4, 1.8)
            if e <= 0: continue
            an = k * 2 * math.pi / len(ORBITE) + t * 0.6
            R = mix(320, 270, fixe)
            px, py = CX + R * math.cos(an), cy + R * 0.8 * math.sin(an)
            c.save(); c.translate(px, py); s = mix(0.3, 1, e) * mix(1, 0.85, fixe); c.scale(s, s)
            tw = largeur(lab, 26, "titre", -0.01); w = tw + 86
            verre_clair(c, -w / 2, -34, w, 68, 34, borne(e * 3), 0.6)
            icone(c, ic, -w / 2 + 34, 0, 28, ROUGE, 2.4)
            texte(c, lab, -w / 2 + 60, -hauteurLigne(26, "titre") / 2, 26, ENCRE, "titre", track=-0.01)
            c.restore()
            trait(c, CX, cy, px, py, "#D5DAE3", 3, 0.6 * borne(e * 2), [8, 10])
        # l'étiquette « prix de vente »
        c.save(); c.translate(CX, cy - 300 * (1 - min(fixe * 1.2, 1)) * (t > T_FIXER - 0.1)); c.rotate(mix(-12, -4, fixe) + 3 * math.sin(t * 2))
        s = mix(0.4, 1, a) * mix(0.85, 1.05, fixe); c.scale(s, s)
        with Calque(c, borne(a * 3)):
            pth = skia.Path(); pth.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -100, 340, 200), 30, 30))
            p = skia.Paint(AntiAlias=True, Color=hexa(ROUGE, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
            c.save(); c.translate(0, 18); c.drawPath(pth, p); c.restore()
            c.drawPath(pth, pgrad_(-170, -100, 170, 100, [ROUGE, "#A80020"]))
            disque(c, -128, -58, 14, BLANC)
            texte(c, "PRIX", 0, -60, 44, BLANC, "archivo", "centre", 0.02)
            texte(c, "DE VENTE", 0, -6, 44, BLANC, "archivo", "centre", 0.02)
        c.restore()
        coche_v(c, CX + 170, cy - 110, 40, entre(t, T_COH, 0.35, 2.4))
        pill_v(c, "Cohérent avec vos objectifs", CX, 1300, entre(t, T_OBJ - 0.1, 0.4, 2.2), "target", plein=True)
        if t > T_COH: eclats(c, CX, cy, t, T_COH, 14, 380, cols=[ROUGE, VERT, ENCRE], graine=9)
        titre2(c, t, "C'EST CETTE", "VISION GLOBALE", T_CEST - 0.05, T_FIXER - 0.1, t2=T_VISION - 0.1)
        titre2(c, t, "QUI PERMET DE FIXER", "UN PRIX DE VENTE COHÉRENT", T_FIXER - 0.1, t1, t2=T_PVENTE - 0.1)


# ─────────────────────────────────────────── 6 · le choix du partenaire en Chine devient stratégique
def scene_strategique(c, t):
    t0, t1 = T_ET - 0.12, T_IDENT - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="haut", d_in=0.4, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.3)
        cx, cy = CX, 1000
        R = 360 * mix(0.6, 1, a)
        G = globe(c, 108, 26, cx, cy, R, prog(t, T_CHOIX - 0.1, 0.5, sortie), borne(a * 3))
        kx, ky, _ = G.pos(*CN, 108, 26, R, cx, cy)
        p = entre(t, T_PART - 0.15, 0.5, 1.8)
        if p > 0:
            onde(c, kx, ky, t, T_PART, 40, 260, ROUGE, 6, 0.6)
            c.save(); c.translate(kx + 20, ky - 150); c.scale(mix(0.3, 1, p), mix(0.3, 1, p))
            with Calque(c, borne(p * 3)):
                verre_clair(c, -190, -70, 380, 140, 44, 1.0, 1.2)
                image(c, "sigle-gsx", -165, -40, 66)
                texte(c, "Votre partenaire", -70, -48, 30, ENCRE, "titre", track=-0.01)
                texte(c, "en Chine", -70, -6, 30, ROUGE, "titre", track=-0.01)
            c.restore()
            trait(c, kx, ky, kx + 20, ky - 80, ROUGE, 4, borne(p * 3))
        if t > T_STRAT - 0.05: tampon(c, "STRATÉGIQUE", CX, 1290, t, T_STRAT, 60, ROUGE, -7)
        titre2(c, t, "LE CHOIX DE VOTRE PARTENAIRE", "DEVIENT STRATÉGIQUE", T_ET - 0.05, t1, t2=T_STRAT - 0.15, c2=ROUGE)


# ─────────────────────────────────────────── 7 · identifier, négocier, évaluer les MOQ, anticiper l'approvisionnement
LEVIERS = [(T_IDENT, "rushes/entrepot-bleu", "Fournisseurs", "search", "IDENTIFIER", "LES BONS FOURNISSEURS"),
           (T_NEGO2, "rushes/atelier-valises", "Conditions d'achat", "scale", "NÉGOCIER", "LES CONDITIONS D'ACHAT"),
           (T_EVAL, "rushes/cartons-ouvrieres", "Quantités minimales", "boxes", "ÉVALUER", "LES QUANTITÉS MINIMALES"),
           (T_ANTI2, "rushes/entrepot-colis", "Approvisionnement", "truck", "ANTICIPER", "L'APPROVISIONNEMENT")]


def scene_leviers(c, t):
    t0, t1 = T_IDENT - 0.12, T_LOBJ - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="recul", d_out=0.3)
    if not g.visible: return
    with g:
        cam = Cam(ax=-12 + 3 * math.sin(t), ay=8 * math.sin(t * 0.7), tz=60, cx=CX, cy=990)
        CW, CH = 270, 370
        plans = []
        for k, (tk, nom, lab, ic, _, _) in enumerate(LEVIERS):
            u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            x, y = (-150 if k % 2 == 0 else 150), (-200 if k < 2 else 200)
            plans.append(Plan(coins((x, y, mix(1300, 0, min(u, 1.05))), CW, CH, ay=(k % 2 - 0.5) * -14), CW, CH,
                              carte_rush(nom, t0, label=lab, ic=ic), borne(u * 3)))
        scene3d(c, cam, plans)
        for k, (tk, _, _, _, l1, l2) in enumerate(LEVIERS):
            fin = LEVIERS[k + 1][0] - 0.1 if k < 3 else t1
            titre2(c, t, l1, l2, tk - 0.1, fin, t2=tk, e1="ressort")


# ─────────────────────────────────────────── 8 · construire une stratégie d'achat : marché, budget, ambitions
PILIERS = [(T_MARCHE, "store", "Marché"), (T_BUDGET, "wallet", "Budget"), (T_AMB, "rocket", "Ambitions")]


def scene_construire(c, t):
    t0, t1 = T_LOBJ - 0.12, T_LA - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="haut", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        sol = 1300
        rrect(c, CX - 360, sol, 720, 18, 9, "#D5DAE3", entre(t, t0, 0.4, 1.4))
        pos = prog(t, T_AMB + 0.25, 0.45, lambda v: ressort(v, 1.4, 5.0))
        for k in range(3):                               # emplacements des piliers, en pointillés, dès le début
            e = entre(t, t0 + 0.1 * k, 0.4, 1.6) * (1 - prog(t, PILIERS[k][0] - 0.1, 0.3))
            if e > 0:
                x = CX + (k - 1) * 230 - 85
                pe = peinture(GRIS, 0.7 * borne(e * 2), Style=skia.Paint.kStroke_Style, StrokeWidth=3); pe.setPathEffect(skia.DashPathEffect.Make([12, 10], t * 30))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, sol - 360, 170, 360), 30, 30), pe)
                texte(c, "?", x + 85, sol - 180 - hauteurLigne(70, "archivo") / 2, 70, "#C4CAD4", "archivo", "centre", 0, borne(e * 2))
        for k, (tk, ic, lab) in enumerate(PILIERS):
            u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.2, 4.6)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            h = 360 * min(u, 1.06); x = CX + (k - 1) * 230 - 85
            verre_clair(c, x, sol - h, 170, h, 30, 1.0, 0.8)
            if u > 0.6:
                tuile_v(c, ic, x + 85, sol - h + 70, 84)
                texte(c, lab, x + 85, sol - h + 130, ajuste(lab, 150, 30, "archivo", -0.02), ENCRE, "archivo", "centre", -0.02)
            eclats(c, x + 85, sol, t, tk, 8, 200, cols=[ROUGE, ENCRE], graine=30 + k)
        # le toit « stratégie d'achat » : flotte, puis se pose sur les trois piliers
        r = entre(t, T_CONSTR - 0.1, 0.45, 1.8)
        if r > 0:
            y = mix(700, sol - 360 - 110, pos) + (8 * math.sin(t * 3) * (1 - pos))
            sx, sy = secousse(t, T_AMB + 0.45, 14, 0.3)
            c.save(); c.translate(CX + sx, y + 55 + sy); c.rotate(mix(-4, 0, pos)); c.scale(mix(0.4, 1, r), mix(0.4, 1, r))
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-330, -55, 660, 110), 30, 30)
            p = skia.Paint(AntiAlias=True, Color=hexa(ROUGE, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 24))
            c.save(); c.translate(0, 16); c.drawRRect(rr, p); c.restore()
            c.drawRRect(rr, pgrad_(-330, -55, 330, 55, [ROUGE, "#A80020"]))
            texte(c, "STRATÉGIE D'ACHAT", 0, -hauteurLigne(48, "archivo") / 2, 48, BLANC, "archivo", "centre", 0)
            c.restore()
            if t > T_AMB + 0.45: eclats(c, CX, sol - 360 - 55, t, T_AMB + 0.45, 14, 400, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=12)
        titre2(c, t, "L'OBJECTIF : CONSTRUIRE", "UNE STRATÉGIE D'ACHAT", T_LOBJ - 0.05, T_MARCHE - 0.1, t2=T_CONSTR - 0.05)
        for k, (tk, _, lab) in enumerate(PILIERS):
            fin = PILIERS[k + 1][0] - 0.1 if k < 2 else t1
            titre2(c, t, "ADAPTÉE À" if k == 0 else None, ["VOTRE MARCHÉ", "VOTRE BUDGET", "VOS AMBITIONS"][k], tk - 0.1, fin, t2=tk - 0.05)


# ─────────────────────────────────────────── 9 · la rentabilité : où investir, quoi anticiper, comment structurer
SAVOIRS = [(T_OU, "target", "Où investir"), (T_QUOI, "eye", "Quoi anticiper"), (T_COMMENT, "layers", "Comment structurer")]


def scene_lecon(c, t):
    t0, t1 = T_LA - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="droite", sor="recul", d_in=0.32, d_out=0.4)
    if not g.visible: return
    with g:
        sav = prog(t, T_ELLE - 0.15, 0.45, entreeSortie)
        if sav < 1:
            with Calque(c, 1 - sav):
                a = entre(t, T_LA, 0.45, 1.8)
                c.save(); c.translate(CX, 940); c.rotate(-3); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
                verre_clair(c, -350, -90, 700, 180, 56, borne(a * 3), 0.3)
                texte(c, "Tout acheter moins cher", 0, -hauteurLigne(50, "archivo") / 2, 50, GRIS, "archivo", "centre", -0.02, borne(a * 3))
                b = prog(t, T_CHER + 0.05, 0.3, sortie)
                if b > 0: trait(c, -320, 0, -320 + 640 * b, 0, ROUGE, 9)
                c.restore()
        for k, (tk, ic, lab) in enumerate(SAVOIRS):
            rangee(c, t, CX, 760 + k * 175, 720, ic, lab, tk, "ok", tk + 0.35, ROUGE)
        titre2(c, t, "LA RENTABILITÉ, CE N'EST PAS", "TOUT ACHETER MOINS CHER", T_LA - 0.05, T_ELLE - 0.1, t2=T_TOUT - 0.1)
        titre2(c, t, "C'EST SAVOIR", "OÙ INVESTIR", T_ELLE - 0.1, T_QUOI - 0.1, t2=T_OU - 0.05, c2=ROUGE)
        titre2(c, t, None, "QUOI ANTICIPER", T_QUOI - 0.1, T_COMMENT - 0.1, t2=T_QUOI - 0.05, c2=ROUGE)
        titre2(c, t, None, "COMMENT STRUCTURER", T_COMMENT - 0.1, T_FIN - 0.05, t2=T_COMMENT - 0.05, c2=ROUGE)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8); son(0.2, "whoosh_long", -12)
son(T_DEV - 0.15, "pop", -9); son(T_DEV, "montee", -14)
son(T_TROUVE - 0.25, "swipe", -9)
for tk, _, _, _ in ACQUIS: son(tk - 0.17, "whoosh_court", -10); son(tk + 0.3, "check", -9)
son(T_MAIS - 0.12, "whoosh", -9); son(T_MARGE - 0.1, "montee", -13); son(TW(28) - 0.1, "pop", -10); son(T_RENT - 0.05, "tampon", -5)
son(T_POUR - 0.12, "swipe", -9); son(T_ALLER - 0.15, "impact_doux", -8)
for tk, _, _, _ in POSTES: son(tk - 0.12, "whoosh_court", -12); son(tk + 0.18, "tampon", -11)
son(T_COUT - 0.15, "montee", -11); son(T_COUT + 0.3, "impact", -6)
son(T_MAISC - 0.12, "whoosh_bas", -8); son(T_MAISC, "pop", -10)
for tk in (T_TVA, T_ANTIC): son(tk - 0.15, "whoosh", -9); son(tk, "impact_doux", -9)
son(T_DIST - 0.15, "swipe", -9); son(T_MARGEC - 0.1, "montee", -14); son(T_RESU - 0.1, "montee", -14)
son(T_FAIRE - 0.15, "whoosh_court", -9)
for tk in (T_CA, T_DEGA, T_GEN): son(tk - 0.12, "pop", -9)
son(T_TROIS - 0.1, "ding", -11)
son(T_CEST - 0.12, "whoosh", -9)
for k in range(6): son(T_VISION - 0.2 + 0.06 * k, "pop", -14)
son(T_FIXER - 0.1, "whoosh_court", -9); son(T_COH, "check", -8); son(T_COH + 0.02, "ching", -10); son(T_OBJ - 0.1, "pop", -10)
son(T_ET - 0.12, "whoosh_long", -8); son(T_PART - 0.15, "pop", -9); son(T_STRAT, "tampon", -5)
for tk, _, _, _, _, _ in LEVIERS: son(tk - 0.15, "whoosh_court", -9); son(tk, "impact_doux", -10)
son(T_LOBJ - 0.12, "swipe", -9); son(T_CONSTR - 0.1, "pop", -9)
for tk, _, _ in PILIERS: son(tk - 0.15, "whoosh_bas", -10); son(tk + 0.2, "impact_doux", -9)
son(T_AMB + 0.45, "impact", -5); son(T_AMB + 0.5, "ching", -9)
son(T_LA - 0.12, "whoosh", -9); son(T_CHER + 0.05, "swipe", -9)
for tk, _, _ in SAVOIRS: son(tk - 0.12, "whoosh_court", -10); son(tk + 0.35, "check", -9)
sons_signature(son, T_FIN)
for tl in (TW(224), TW(230)): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_TROUVE - 0.25, T_TROUVE + 0.2), (T_MAIS - 0.15, T_MAIS + 0.25), (T_POUR - 0.15, T_POUR + 0.25), (T_MAISC - 0.15, T_MAISC + 0.25),
             (T_DIST - 0.15, T_DIST + 0.25), (T_FAIRE - 0.15, T_FAIRE + 0.25), (T_CEST - 0.15, T_CEST + 0.25), (T_ET - 0.15, T_ET + 0.25),
             (T_IDENT - 0.15, T_IDENT + 0.25), (T_LOBJ - 0.15, T_LOBJ + 0.25), (T_LA - 0.15, T_LA + 0.25), (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_RENT, ROUGE, 0.06), (T_COUT + 0.3, ROUGE, 0.06), (T_COH, VERT, 0.05), (T_STRAT, ROUGE, 0.06), (T_AMB + 0.45, "#FFFFFF", 0.1)]:
    eclair(tt, cc_, a_)


SIGN_MEDIAS = [(n, True) for n in RUSHES]


def dessine(c, t):
    gsx.T_COURANT[0] = t
    fond_clair(c, t)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_papier(c, t); scene_tour(c, t); scene_fiscal(c, t); scene_prix(c, t); scene_strategique(c, t)
        scene_leviers(c, t); scene_construire(c, t); scene_lecon(c, t)
    entete(c, t, T_ET - 0.05, T_FIN)
    signature_gsx(c, t, T_FIN, SIGN_MEDIAS, [("Trouvez le bon partenaire en Chine", TW(224), 46, ENCRE),
                                               ("et donnez à votre projet les bases d'une rentabilité durable.", TW(230), 42, ROUGE)], cy=820)
    K.dessine_eclairs(c, t)
    if t < T_FIN - 0.1: SOUS.dessine(c, t, ENCRE)
