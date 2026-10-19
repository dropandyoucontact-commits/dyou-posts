"""GSX-M01 « Tout le monde parle de la Chine. Mais qui en maîtrise vraiment les codes ? » — hook 1 du client (19/10/2026).
GSX (Global SINO Export) = deuxième société du client MONARQUE : même grammaire claire (fond blanc cassé, Archivo Black,
Tomy, sous-titres encre) + les éléments de DY-M15 passés en clair (cartes en verre givré qui sortent en 3D, plans qui
jaillissent, signature explosive). Accent rouge du logo. Script du client mot pour mot ; attaque du hook rapide
(outils/hook_rapide.py). Rushes d'usines du client, plans entiers (cartes 9:16 ou 16:9, jamais une bande rognée).
Zone sûre TikTok / Snap : contenu entre x 130 et 860, axe CX = 510."""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import Groupe, eclats, entre, curseur, clic, lueur_s, lettres, sous_titres
from studio3d import Cam, Plan, coins, scene3d, Balance
from gsx import *

polices(P)
DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 1.9, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = sous_titres(K)
CX = 510
_T = [0.0]

# repères (mots)
T_ON, T_PRIX, T_OPP, T_FAB, T_GRANDE = TW(9), TW(13), TW(15), TW(19), TW(24)
T_MAIS, T_PROM, T_QUEST, T_QUI, T_CODES, T_CHINOIS = TW(26), TW(30), TW(31), TW(34), TW(38), TW(41)
T_CAR, T_SIMPLE, T_TROUVER, T_USINE, T_INTERNET = TW(42), TW(50), TW(52), TW(54), TW(56)
T_IL, T_COMPR, T_LOC, T_NEGO, T_IDENT, T_INTERL, T_DIST, T_OPPV, T_MAUV = TW(57), TW(59), TW(63), TW(64), TW(66), TW(69), TW(74), TW(77), TW(79)
T_SURTOUT, T_DEFEND, T_INTER, T_MILLIERS, T_KM, T_FOURN = TW(81), TW(87), TW(89), TW(95), TW(97), TW(100)
T_CEST, T_GSX, T_INTERV = TW(101), TW(105), TW(106)
T_ROLE, T_ACC, T_SOURC, T_AIDER, T_PART, T_EXIG, T_LIEN, T_OBJ, T_TERRAIN = TW(107), TW(112), TW(117), TW(118), TW(124), TW(128), TW(131), TW(136), TW(141)
T_PARCE, T_PRIX2, T_COMPTE, T_QUAL, T_PARTN, T_CHOIS = TW(143), TW(146), TW(149), TW(152), TW(154), TW(158)
T_AVEC, T_CHERCHEZ, T_FOURN2 = TW(161), TW(165), TW(169)
T_VOUS, T_ENTOUR, T_PARTN2, T_ENJEUX, T_DECIS, T_VEILLE, T_INTER2, T_COEUR, T_ETAPE = TW(170), TW(172), TW(174), TW(178), TW(183), TW(185), TW(190), TW(193), TW(196)
T_FIN, T_LA, T_ENCORE = TW(197), TW(198), TW(203)

RUSHES = ["rushes/chaine-electronique", "rushes/presses-jaunes", "rushes/valises-moulage", "rushes/tissu-machine",
          "rushes/cartons-ouvrieres", "rushes/entrepot-colis", "rushes/entrepot-bleu"]


# ─────────────────────────────────────────── cartes
def carte_rush(nom, t0, vitesse=1.0, label=None, ic=None):
    """une vraie vidéo du client dans une carte de verre clair (plan entier, jamais ralenti)"""
    def f(c, w, h):
        verre_clair(c, 0, 0, w, h, w * 0.08)
        m = w * 0.045
        video(c, nom, m, m, w - 2 * m, h - 2 * m, _T[0] - t0, vitesse, True, rayon=w * 0.055)
        balayage(c, 0, 0, w, h, _T[0], w * 0.08, 0.4, 0.35)
        if label:
            pill_v(c, label, w / 2, h - m - 52, 1.0, ic, taille=max(20, w * 0.07))
    return f


def carte_ic(ic, lab, sous=None, accent=ROUGE, gris=0.0):
    def f(c, w, h):
        verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 1 - gris, accent)
        tuile_v(c, ic, w / 2, h * 0.36, w * 0.42, accent if not gris else "#A9AFBA")
        lab_w = ajuste(lab, w * 0.84, w * 0.12, "archivo", -0.02)
        texte(c, lab, w / 2, h * 0.62, lab_w, ENCRE if not gris else "#9AA0AA", "archivo", "centre", -0.02)
        if sous: texte(c, sous, w / 2, h * 0.62 + lab_w * 1.3, w * 0.065, GRIS, "demi", "centre", 0)
        balayage(c, 0, 0, w, h, _T[0], w * 0.1, 0.4, 0.4)
    return f


def tuile_v(c, ic, cx, cy, taille, accent=ROUGE):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - taille / 2, cy - taille / 2, taille, taille), taille * 0.28, taille * 0.28)
    p = skia.Paint(AntiAlias=True, Color=hexa(accent, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, taille * 0.12))
    c.save(); c.translate(0, taille * 0.08); c.drawRRect(rr, p); c.restore()
    c.drawRRect(rr, pgrad_(cx - taille / 2, cy - taille / 2, cx + taille / 2, cy + taille / 2, [accent, _fonce(accent)]))
    icone(c, ic, cx, cy, taille * 0.52, BLANC, 2.6)


def _fonce(col):
    return {ROUGE: "#A80020", VERT: "#0E7A44"}.get(col, "#6D7380")


# ─────────────────────────────────────────── 1 · hook : le globe, et tout le monde vous parle de la Chine
BULLES = [("Usine directe", "factory"), ("Prix imbattables", "euro"), ("Le bon plan", "sparkles"), ("Fabricant", "factory"),
          ("Import Chine", "ship"), ("Petits prix", "euro"), ("Sourcing", "search"), ("Opportunité", "trending-up"),
          ("Fournisseur", "package"), ("Production", "factory")]
# (départ, direction, sens) : 4 bulles déjà en vol à l'image 0
VOLS = [(-0.55 + 0.17 * j, d, (-1) ** j) for j, d in enumerate(
    [(-0.6, -0.2), (0.62, -0.38), (-0.5, 0.5), (0.58, 0.42), (-0.72, -0.55), (0.4, -0.72), (-0.25, 0.72), (0.76, 0.05), (-0.68, 0.12), (0.3, 0.62)])]


def bulle_volante(c, t, j, t0, direc, sens, X0, Y0):
    lab, ic = BULLES[j % len(BULLES)]
    u = (t - t0) / 1.05
    if not (0 <= u <= 1): return
    v = sortie(u) * 0.4 + u ** 1.6 * 0.6
    Z = -1500 * u ** 1.1; f = 1800 / (1800 + Z)
    x = X0 + direc[0] * 600 * v * f; y = Y0 + (direc[1] * (760 if direc[1] > 0 else 420) * v - 160 * math.sin(math.pi * min(1, u * 1.2))) * f
    s = 0.82 * f
    c.save(); c.translate(x, y); c.rotate(sens * (-8 + 26 * u)); c.scale(s, s)
    with Calque(c, borne(u / 0.06) * borne((1 - u) / 0.12 + 0.3)):
        tw = largeur(lab, 34, "titre", -0.01); w, h = tw + 120, 84
        verre_clair(c, -w / 2, -h / 2, w, h, 30, 1.0, 0.8)
        pth = skia.Path(); pth.moveTo(-w / 2 + 34, h / 2 - 2); pth.lineTo(-w / 2 + 26, h / 2 + 22); pth.lineTo(-w / 2 + 58, h / 2 - 2); pth.close()
        c.drawPath(pth, peinture("#EEF1F6"))
        icone(c, ic, -w / 2 + 44, 0, 36, ROUGE, 2.6)
        texte(c, lab, -w / 2 + 76, -hauteurLigne(34, "titre") / 2, 34, ENCRE, "titre", track=-0.01)
    c.restore()


def scene_hook(c, t):
    if t > T_ON + 0.35: return
    part = prog(t, T_ON - 0.15, 0.4, entree)
    with Calque(c, 1 - part):
        o = prog(t, -0.3, 1.6, douce)
        sx, sy = secousse(t, 0.0, 14, 0.3)
        a, b = secousse(t, TW(8), 10, 0.25); sx += a; sy += b
        R = mix(330, 360, o) * (1 + 0.6 * part)
        lon = mix(40, 104, o) + 4 * t
        X0, Y0 = CX + sx, 1010 + sy
        lueur_s(c, X0, Y0, 520, ROUGE, 0.10 + 0.08 * prog(t, TW(8) - 0.1, 0.3))
        globe(c, lon, 18, X0, Y0, R, mix(0.55, 1, prog(t, 0.0, 0.6, sortie)) * (1 + 0.15 * battement(t, TW(8), 1, 0.4) - 0.15))
        for j, (t0, d, s) in enumerate(VOLS):
            onde(c, X0, Y0, t, t0, 80, 420, ROUGE, 5, 0.5)
        for j, (t0, d, s) in enumerate(VOLS):
            bulle_volante(c, t, j, t0, d, s, X0, Y0)
        if t > TW(8) - 0.1:
            onde(c, X0, Y0, t, TW(8), 100, 640, ROUGE, 10, 0.6)
            eclats(c, X0, Y0, t, TW(8), 14, 460, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=2)
    titre2(c, t, "AUJOURD'HUI, TOUT LE MONDE", "VOUS PARLE DE LA CHINE", -0.6, T_ON - 0.05, t2=-0.45)


# ─────────────────────────────────────────── 2 · prix compétitifs, opportunités, fabricants à grande échelle
def opp_dessin(c, w, h):
    """carte « opportunités » : courbe qui monte pour de vrai"""
    verre_clair(c, 0, 0, w, h, w * 0.1)
    tuile_v(c, "trending-up", w / 2, h * 0.2, w * 0.3)
    u = prog(_T[0], T_OPP, 0.9, entreeSortie)
    x0, y0, x1, y1 = w * 0.12, h * 0.78, w * 0.88, h * 0.38
    for k in range(5):
        hb = (y0 - y1) * (0.25 + 0.17 * k) * u
        rrect(c, x0 + k * (x1 - x0) / 5 + 6, y0 - hb, (x1 - x0) / 5 - 12, hb, 8, ROUGE if k == 4 else "#D5DAE3")
    texte(c, "Opportunités", w / 2, h * 0.84, w * 0.1, ENCRE, "archivo", "centre", -0.02)
    balayage(c, 0, 0, w, h, _T[0], w * 0.1, 0.4, 0.4)


ARRIVEES = [(T_PRIX - 0.08, "PRIX COMPÉTITIFS"), (T_OPP - 0.08, "OPPORTUNITÉS"), (T_FAB - 0.08, "DES FABRICANTS")]


def scene_promesses(c, t):
    t0, t1 = T_ON - 0.15, T_CAR - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        derr = prog(t, T_MAIS - 0.1, 0.6, entreeSortie)        # « mais derrière » : les cartes reculent et pâlissent
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.9), ay=6 * math.sin(t * 0.7), tz=mix(0, 900, derr), cx=CX, cy=mix(1000, 900, derr))
        CW, CH = 270, 440
        dess = [carte_ic("euro", "Prix", "compétitifs"), opp_dessin, carte_rush("rushes/chaine-electronique", T_FAB - 1.5, 1.0)]
        plans = []
        for k, (tk, _) in enumerate(ARRIVEES):
            u = prog(t, tk - 0.1, 0.45, lambda v: ressort(v, 1.3, 4.8)) if t > tk - 0.1 else 0.0
            if u <= 0: continue
            x = (k - 1) * 290; z = mix(1800, 0, min(u, 1.05))
            ay = mix(60 * (1 if k % 2 else -1), (k - 1) * -10, min(u, 1))
            z -= 260 * prog(t, T_GRANDE - 0.1, 0.4, sortie) * (k == 2) * (1 - derr)
            plans.append(Plan(coins((x, 40, z), CW, CH, ay=ay, az=(k - 1) * 2), CW, CH, dess[k],
                              borne(u * 3) * (1 - 0.6 * derr)))
        scene3d(c, cam, plans)
        for k, (tk, _) in enumerate(ARRIVEES):
            if t > tk:
                px = CX + (k - 1) * 290 * (1 - 0.5 * derr)
                onde(c, px, 1040, t, tk + 0.1, 80, 380, ROUGE, 6, 0.45)
                eclats(c, px, 1040, t, tk + 0.1, 10, 300, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=11 + k)
        pill_v(c, "À grande échelle", CX, 1300, entre(t, T_GRANDE - 0.1, 0.4, 2.2) * (1 - derr), "factory", plein=True)
        # « derrière toutes ces promesses » : le voile de verre, puis la question
        if derr > 0:
            verre_clair(c, 150, 600, 720, 640, 56, 0.55 * derr, 0.5, ROUGE, 0.4)
            q = entre(t, T_QUEST - 0.1, 0.5, 2.0)
            if q > 0:
                c.save(); c.translate(CX, 880); c.scale(mix(0.3, 1, q), mix(0.3, 1, q)); c.rotate(8 * math.sin(t * 2.4))
                disque(c, 0, 0, 120, ENCRE, borne(q * 3), (16, 40, 0.3)); icone(c, "circle-help", 0, 0, 150, BLANC, 2.4, borne(q * 3))
                c.restore()
            cod = entre(t, T_CODES - 0.1, 0.45, 1.8)
            if cod > 0: codes(c, t, CX, 1120, cod)
        for k, (tk, lab) in enumerate(ARRIVEES):
            fin = ARRIVEES[k + 1][0] if k < 2 else T_GRANDE - 0.1
            titre2(c, t, "ON VOUS PARLE DE" if k == 0 else None, lab, tk, fin, t2=tk, e2="ressort")
        titre2(c, t, None, "À GRANDE ÉCHELLE", T_GRANDE - 0.08, T_MAIS - 0.1, e2="ressort")
        titre2(c, t, "MAIS DERRIÈRE CES PROMESSES", "QUI MAÎTRISE LES CODES ?", T_MAIS - 0.05, t1, t2=T_QUI - 0.05, c2=ROUGE)


HANZI = ["关", "系", "面", "子", "谈", "判", "信", "任", "价", "格"]


def codes(c, t, cx, cy, a):
    """cadenas à molettes : les « codes du marché chinois » qui tournent sans se caler"""
    w, h = 520, 150
    c.save(); c.translate(cx, cy); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
    with Calque(c, borne(a * 3)):
        verre_clair(c, -w / 2, -h / 2, w, h, 40, 1.0, 1.0)
        tuile_v(c, "lock", -w / 2 + 75, 0, 86, ENCRE)
        for j in range(4):
            x = -w / 2 + 160 + j * 86
            rrect(c, x, -52, 72, 104, 18, "#EEF1F6", 1, None, "#D5DAE3", 2)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, -52, 72, 104), 18, 18), True)
            ph = t * (5 + 1.7 * j) + j * 1.3
            for d in (-1, 0, 1):
                ch = HANZI[int(math.floor(ph) + d + j * 3) % len(HANZI)]
                yy = -26 + (d - (ph % 1)) * 70
                texte(c, ch, x + 36, yy, 48, ENCRE if d == 0 else GRIS, "cjk", "centre", 0)
            c.restore()
    c.restore()


# ─────────────────────────────────────────── 3 · pas simplement trouver une usine sur Internet
RESULTATS = ["Usine — prix direct usine", "Fabricant — tous produits", "Usine — livraison rapide", "Fabricant — meilleur prix"]


def scene_internet(c, t):
    t0, t1 = T_CAR - 0.12, T_IL - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="gauche", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        cam = Cam(ax=-8 + 2 * math.sin(t), ay=mix(-22, 8, prog(t, t0, t1 - t0, douce)), tz=mix(500, 60, a), cx=CX, cy=1000)
        W_, H_ = 680, 620

        def nav(cc, w, h):
            verre_clair(cc, 0, 0, w, h, 40)
            for k, col in enumerate(["#FF6159", "#FFBD2E", "#28C941"]): disque(cc, 40 + 28 * k, 40, 9, col)
            rrect(cc, 30, 74, w - 60, 76, 38, "#FFFFFF", 1, None, "#D5DAE3", 2)
            icone(cc, "search", 76, 112, 34, ROUGE, 2.6)
            s = "usine Chine"
            n = int(borne((t - (T_CAR + 0.1)) / 0.5) * len(s) + 0.999) if t > T_CAR + 0.1 else 0
            texte(cc, s[:n], 112, 112 - hauteurLigne(36, "titre") / 2, 36, ENCRE, "titre", track=-0.01)
            if n < len(s) and int(t * 3) % 2 == 0: rrect(cc, 116 + largeur(s[:n], 36, "titre", -0.01), 92, 4, 40, 2, ROUGE)
            for k, r_ in enumerate(RESULTATS):
                u = prog(t, T_TROUVER - 0.3 + 0.08 * k, 0.35, sortieExpo)
                if u <= 0: continue
                y = 180 + k * 104 + 20 * (1 - u)
                with Calque(cc, u):
                    rrect(cc, 30, y, w - 60, 90, 22, "#FFFFFF", 1, (6, 16, 0.08), "#E3E7EE", 2)
                    disque(cc, 82, y + 45, 28, "#EEF1F6"); icone(cc, "factory", 82, y + 45, 32, GRIS, 2.4)
                    texte(cc, r_, 128, y + 45 - hauteurLigne(28, "titre") / 2, 28, ENCRE, "titre", track=-0.01)
            balayage(cc, 0, 0, w, h, _T[0], 40, 0.4, 0.35)
        scene3d(c, cam, [Plan(coins((0, 0, 0), W_, H_), W_, H_, nav)])
        tap = T_USINE + 0.05
        cu = prog(t, tap - 0.45, 0.4, sortie)
        if cu > 0:
            ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
            curseur(c, mix(860, 560, cu), mix(1400, 900, cu), 1.3, 1 - prog(t, T_INTERNET + 0.3, 0.3), ap)
            clic(c, 550, 890, t, tap, ROUGE)
        x = entre(t, T_INTERNET - 0.05, 0.4, 2.4)
        if x > 0:
            croix_v(c, CX + 250, 760, 66, x)
            pill_v(c, "Pas si simple", CX, 1300, x, "triangle-alert", plein=True, rot=-3)
        titre2(c, t, "TRAVAILLER AVEC LA CHINE", "PAS SIMPLEMENT", T_CAR - 0.05, T_TROUVER - 0.1, t2=T_SIMPLE - 0.05)
        titre2(c, t, "TROUVER", "UNE USINE SUR INTERNET", T_TROUVER - 0.1, t1, t2=T_USINE - 0.05, e1="ressort")


# ─────────────────────────────────────────── 4 · ce qu'il faut savoir faire
SAVOIRS = [(T_COMPR, "landmark", "Les pratiques locales", "COMPRENDRE"), (T_NEGO, "scale", "Savoir négocier", "NÉGOCIER"),
           (T_IDENT, "users", "Les bons interlocuteurs", "IDENTIFIER"), (T_DIST, "eye", "Le bon choix", "DISTINGUER")]


def scene_savoirs(c, t):
    t0, t1 = T_IL - 0.12, T_SURTOUT - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="haut", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        choix = prog(t, T_DIST - 0.15, 0.55, entreeSortie)
        if choix < 1:
            with Calque(c, 1 - choix):
                for k, (tk, ic, lab, _) in enumerate(SAVOIRS[:3]):
                    u = entre(t, tk - 0.12, 0.45, 1.8)
                    if u <= 0: continue
                    y = 640 + k * 190
                    c.save(); c.translate(CX + 400 * (1 - min(u, 1)), y); c.rotate(-4 * (1 - min(u, 1)))
                    with Calque(c, borne(u * 3)):
                        verre_clair(c, -360, -76, 720, 152, 44)
                        tuile_v(c, ic, -280, 0, 104)
                        texte(c, lab, -205, -hauteurLigne(40, "archivo") / 2, ajuste(lab, 470, 40, "archivo", -0.02), ENCRE, "archivo", track=-0.02)
                        coche_v(c, 300, 0, 32, entre(t, tk + 0.35, 0.35, 2.4))
                        balayage(c, -360, -76, 720, 152, t + k, 44, 0.5, 0.4)
                    c.restore()
        if choix > 0:
            cam = Cam(ax=-8 + 2 * math.sin(t), ay=mix(-30, 6, choix) + 4 * math.sin(t * 0.8), tz=mix(700, 40, choix), cx=CX, cy=1000)
            CW, CH = 330, 520
            bon = carte_rush("rushes/presses-jaunes", T_DIST - 0.2, 1.0)
            mauvais = carte_ic("factory", "Mauvais", "choix", gris=1.0)
            scene3d(c, cam, [Plan(coins((-185, 0, 0), CW, CH, ay=12), CW, CH, bon, borne(choix * 2)),
                             Plan(coins((185, 0, 0), CW, CH, ay=-12), CW, CH, mauvais, borne(choix * 2))])
            v = entre(t, T_OPPV - 0.05, 0.4, 2.4)
            coche_v(c, CX - 185, 760, 56, v)
            pill_v(c, "Vraie opportunité", CX - 175, 1300, v, "badge-check", accent=VERT)
            m = entre(t, T_MAUV - 0.05, 0.4, 2.4)
            croix_v(c, CX + 185, 760, 56, m)
            if m > 0: eclats(c, CX + 185, 760, t, T_MAUV, 10, 260, cols=[ROUGE, GRIS], graine=5)
        for k, (tk, _, _, l2) in enumerate(SAVOIRS):
            fin = SAVOIRS[k + 1][0] - 0.1 if k < 3 else t1
            titre2(c, t, "IL FAUT" if k == 0 else None, l2, tk - 0.1, fin, t2=tk - 0.08, e2="ressort",
                   c2=ROUGE if k == 3 else ENCRE)


# ─────────────────────────────────────────── 5 · qui défend vos intérêts, à des milliers de kilomètres
def scene_distance(c, t):
    t0, t1 = T_SURTOUT - 0.12, T_CEST - 0.05
    g = Groupe(c, t, t0, t1, ent="zoom", sor="aucune", d_in=0.4)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.3)
        lon = mix(30, 62, prog(t, t0, t1 - t0, douce))
        R = 360 * mix(0.7, 1, a)
        cx, cy = CX, 1000
        G = globe(c, lon, 30, cx, cy, R, prog(t, T_MILLIERS - 0.2, 0.6, sortie), borne(a * 3))
        u = prog(t, T_MILLIERS - 0.2, 1.0, entreeSortie)
        if u > 0:
            tete = G.arc(c, FR, CN, cx, cy, R, lon, 30, u, ROUGE, 7, 0.35, [16, 12])
            if u < 1 and tete: icone(c, "plane", tete[0], tete[1], 46, ENCRE, 2.6)
        G.repere(c, *FR, cx, cy, R, lon, 30, "Vous", ENCRE, "FR", entre(t, T_SURTOUT + 0.1, 0.4, 2.0), haut=60)
        G.repere(c, *CN, cx, cy, R, lon, 30, "Vos fournisseurs", ROUGE, "CN", entre(t, T_FOURN - 0.15, 0.4, 2.0), haut=70)
        bouclier = entre(t, T_DEFEND - 0.1, 0.45, 2.0)
        if bouclier > 0:
            c.save(); c.translate(CX + 250, 690); c.rotate(6 * math.sin(t * 2)); s = mix(0.3, 1, bouclier); c.scale(s, s)
            verre_clair(c, -110, -110, 220, 220, 60, borne(bouclier * 3))
            icone(c, "shield-check", 0, -10, 110, ROUGE, 2.6, borne(bouclier * 3))
            disque(c, 74, 70, 34, ENCRE, borne(bouclier * 3)); texte(c, "?", 74, 70 - hauteurLigne(46, "archivo") / 2, 46, BLANC, "archivo", "centre", 0, borne(bouclier * 3))
            c.restore()
        pill_v(c, "Des milliers de kilomètres", CX, 1300, entre(t, T_KM - 0.1, 0.4, 2.2), "plane", plein=True)
        titre2(c, t, "ET SURTOUT", "QUI DÉFEND VOS INTÉRÊTS ?", T_SURTOUT - 0.05, t1, t2=T_DEFEND - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 6 · c'est là que GSX intervient (disque noir, logo)
def scene_gsx(c, t):
    r = cles(t, [(T_CEST - 0.1, 0), (T_CEST + 0.25, 2200, entree), (T_ROLE - 0.15, 2200), (T_ROLE + 0.2, 0, entreeSortie)])
    if r <= 1: return 0
    disque(c, CX, 1000, r, ENCRE)
    u = entre(t, T_GSX - 0.12, 0.55, 1.8)
    if u > 0:
        sx, sy = secousse(t, T_GSX, 16, 0.3)
        sortie_ = prog(t, T_ROLE - 0.2, 0.3, entree)
        lueur_s(c, CX, 960, 520, ROUGE, 0.25 * borne(u * 2) * (1 - sortie_))
        w = 720 * mix(0.4, 1, u) * mix(1, 0.4, sortie_)
        logo_gsx(c, CX + sx, mix(960, 300, sortie_) + sy, w, borne(u * 3), blanc=True)
        onde(c, CX, 960, t, T_GSX + 0.05, 100, 760, ROUGE, 12, 0.6)
        eclats(c, CX, 960, t, T_GSX + 0.05, 16, 560, cols=[ROUGE, BLANC, "#9AA8BF"], graine=9)
    titre2(c, t, "C'EST PRÉCISÉMENT LÀ", None, T_CEST, T_GSX - 0.1, y=860)
    return r


def entete(c, t):
    a = prog(t, T_ROLE - 0.05, 0.3, sortie) * (1 - prog(t, T_FIN - 0.15, 0.25))
    if a > 0: logo_gsx(c, 540, 240, 210, a)


# ─────────────────────────────────────────── 7 · notre rôle : sourcing, partenaires adaptés, faire le lien
def scene_role(c, t):
    t0, t1 = T_ROLE - 0.1, T_PARCE - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        lien = prog(t, T_LIEN - 0.2, 0.6, entreeSortie)
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.8), ay=mix(-16, 10, prog(t, t0, T_LIEN - t0, douce)) * (1 - lien) + 4 * math.sin(t * 0.7),
                  tz=mix(0, -40, lien), cx=CX, cy=1000)
        plans = []
        etapes = [(T_ACC, carte_rush("rushes/entrepot-colis", T_ACC - 0.5, 1.0), -175, 330, 540),
                  (T_AIDER, carte_rush("rushes/atelier-valises", T_AIDER - 2.0, 1.0), 175, 330, 540)]
        for k, (tk, dess, x, CW, CH) in enumerate(etapes):
            u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.6)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            if k == 1: CW, CH = 330, 540
            pos = (mix(x, x * 2.8, lien), mix(-20, -500, lien), mix(1500, 0, min(u, 1.05)) + 400 * lien)
            plans.append(Plan(coins(pos, CW, CH, ay=mix(50 * (-1) ** k, (-1) ** k * -8, min(u, 1))), CW, CH, dess, borne(u * 3) * (1 - lien)))
        if lien > 0:
            CW, CH = 360, 560
            plans.append(Plan(coins((mix(-900, -205, lien), 0, 0), CW, CH, ay=14), CW, CH, carte_ic("target", "Vos", "objectifs"), borne(lien * 2)))
            plans.append(Plan(coins((mix(900, 205, lien), 0, 0), CW, CH, ay=-14), CW, CH,
                              carte_rush("rushes/tissu-machine", T_LIEN, 1.0), borne(lien * 2)))
        scene3d(c, cam, plans)
        if t < T_LIEN:
            pill_v(c, "Sourcing", CX - 175, 1300, entre(t, T_SOURC - 0.1, 0.4, 2.2) * (1 - lien), "search", plein=True)
            p = entre(t, T_PART - 0.1, 0.4, 2.2) * (1 - lien)
            pill_v(c, "Partenaires adaptés", CX + 175, 1300, p, "badge-check", accent=VERT)
            coche_v(c, CX + 300, 770, 40, entre(t, T_EXIG - 0.05, 0.35, 2.4) * (1 - lien))
        if lien > 0:
            # le lien : trait rouge tendu entre les deux cartes, le sigle GSX au milieu
            v = prog(t, T_LIEN + 0.1, 0.7, entreeSortie)
            xa, xb, y = CX - 150, CX + 150, 1000
            pe = peinture(ROUGE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=8); pe.setStrokeCap(skia.Paint.kRound_Cap)
            pe.setPathEffect(skia.DashPathEffect.Make([18, 12], -t * 80))
            c.drawLine(xa, y, mix(xa, xb, v), y, pe)
            s = entre(t, T_LIEN + 0.45, 0.45, 2.2)
            if s > 0:
                disque(c, CX, y, 70 * s, BLANC, 1, (10, 26, 0.25)); anneau(c, CX, y, 70 * s, ROUGE, 4)
                iw, ih = taille_img("sigle-gsx"); image(c, "sigle-gsx", CX - 46 * s, y - 46 * s * ih / iw, 92 * s)
                eclats(c, CX, y, t, T_LIEN + 0.5, 12, 300, cols=[ROUGE, ENCRE], graine=3)
            pill_v(c, "Vos objectifs", CX - 200, 1300, entre(t, T_OBJ - 0.1, 0.4, 2.2), "target", taille=28)
            pill_v(c, "Le terrain chinois", CX + 200, 1300, entre(t, T_TERRAIN - 0.1, 0.4, 2.2), "map-pin", taille=28, plein=True)
        titre2(c, t, "NOTRE RÔLE", "VOUS ACCOMPAGNER", T_ROLE, T_SOURC - 0.1, t2=T_ACC - 0.05)
        titre2(c, t, "DANS VOS OPÉRATIONS DE", "SOURCING", T_SOURC - 0.1, T_AIDER - 0.1, t2=T_SOURC - 0.05, e1="ressort")
        titre2(c, t, "IDENTIFIER", "LES BONS PARTENAIRES", T_AIDER - 0.1, T_LIEN - 0.15, t2=T_PART - 0.05)
        titre2(c, t, "FAIRE LE LIEN", "OBJECTIFS ↔ TERRAIN", T_LIEN - 0.15, t1, t2=T_OBJ - 0.05, c2=ROUGE)


# ─────────────────────────────────────────── 8 · au-delà du prix : la qualité du partenaire (balance)
def scene_balance(c, t):
    t0, t1 = T_PARCE - 0.12, T_AVEC - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        pese = prog(t, T_QUAL - 0.1, 0.8, lambda v: ressort(v, 1.6, 4.0))
        ang = mix(-6, 16, min(pese, 1.15)) + 2 * math.sin(t * 2.2) * (1 - borne(pese))
        cx, cy = CX, 860
        with Calque(c, borne(a * 3)):
            trait(c, cx, cy, cx, cy + 420, "#B8BEC8", 14); rrect(c, cx - 120, cy + 410, 240, 26, 13, "#B8BEC8")
            disque(c, cx, cy, 22, ENCRE)
            ra = math.radians(ang); L = 300
            ends = [(cx - L * math.cos(ra), cy - L * math.sin(ra)), (cx + L * math.cos(ra), cy + L * math.sin(ra))]
            trait(c, ends[0][0], ends[0][1], ends[1][0], ends[1][1], ENCRE, 12)
            for k, (ex, ey) in enumerate(ends):
                trait(c, ex, ey, ex, ey + 110, "#9AA0AA", 4)
                if k == 0:
                    w, h = 220, 200
                    verre_clair(c, ex - w / 2, ey + 110, w, h, 36, 1.0, 0.3)
                    tuile_v(c, "euro", ex, ey + 185, 88, "#9AA0AA" if pese > 0.3 else ROUGE)
                    texte(c, "Le prix", ex, ey + 245, 32, ENCRE, "archivo", "centre", -0.02)
                else:
                    w, h = 260, 330
                    c.save(); c.translate(ex - w / 2, ey + 110); carte_rush("rushes/chaine-electronique", T_PARCE, 1.0)(c, w, h); c.restore()
                    if pese > 0:
                        pill_v(c, "Qualité", ex, ey + 110 + h - 20, entre(t, T_QUAL - 0.05, 0.4, 2.2), "badge-check", accent=VERT, taille=28)
            if pese > 0:
                eclats(c, ends[1][0], ends[1][1] + 200, t, T_QUAL + 0.25, 12, 320, cols=[VERT, ROUGE, ENCRE], graine=6)
        titre2(c, t, "AU-DELÀ DU PRIX", "CE QUI COMPTE", T_PARCE - 0.05, T_QUAL - 0.15, t2=T_COMPTE - 0.05)
        titre2(c, t, "C'EST LA QUALITÉ", "DU PARTENAIRE", T_QUAL - 0.15, t1, t2=T_PARTN - 0.05, c2=ROUGE, e1="ressort")


# ─────────────────────────────────────────── 9 · pas un simple fournisseur : un partenaire qui vous entoure
SATELLITES = [(T_PARTN2, "Partenaire", "heart-handshake"), (T_ENJEUX, "Vos enjeux", "target"), (T_DECIS, "Vos décisions", "lightbulb"),
              (T_INTER2, "Vos intérêts", "shield-check")]
ETAPES = [("Sourcing", "search"), ("Négociation", "scale"), ("Production", "factory"), ("Contrôle", "eye"), ("Expédition", "ship")]


def scene_partenaire(c, t):
    t0, t1 = T_AVEC - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="droite", sor="recul", d_in=0.32, d_out=0.4)
    if not g.visible: return
    with g:
        rech = 1 - prog(t, T_VOUS - 0.2, 0.4, entreeSortie)
        if rech > 0:
            with Calque(c, rech):
                y = 820
                verre_clair(c, CX - 340, y - 60, 680, 120, 60)
                icone(c, "search", CX - 270, y, 44, ROUGE, 2.8)
                s = "un fournisseur"
                n = int(borne((t - (T_CHERCHEZ - 0.05)) / 0.45) * len(s) + 0.999) if t > T_CHERCHEZ - 0.05 else 0
                texte(c, s[:n], CX - 220, y - hauteurLigne(44, "titre") / 2, 44, ENCRE, "titre", track=-0.01)
                b = prog(t, T_FOURN2 + 0.15, 0.25, sortie)
                if b > 0: trait(c, CX - 225, y, CX - 225 + largeur(s, 44, "titre", -0.01) * b, y, ROUGE, 7)
                croix_v(c, CX + 260, y, 40, entre(t, T_FOURN2 + 0.3, 0.35, 2.4))
        if t > T_VOUS - 0.25:
            u = entre(t, T_VOUS - 0.2, 0.5, 1.8)
            etape = prog(t, T_VEILLE - 0.15, 0.6, entreeSortie)
            cy = mix(960, 905, etape)
            for k, (tk, lab, ic) in enumerate(SATELLITES):
                e = entre(t, tk - 0.12, 0.45, 2.0)
                if e <= 0: continue
                an = -math.pi / 2 + k * math.pi / 2 + t * 0.35
                rx, ry = 270 * mix(0.3, 1, min(e, 1)), 270 * mix(0.3, 1, min(e, 1)) * mix(1, 0.6, etape)
                px, py = CX + rx * math.cos(an), cy + ry * math.sin(an)
                trait(c, CX, cy, px, py, "#D5DAE3", 3, borne(e * 2), [8, 10])
                c.save(); c.translate(px, py); s = mix(0.3, 1.25, e) * mix(1, 0.8, etape); c.scale(s, s)
                tw = largeur(lab, 30, "titre", -0.01); w, h = max(200, tw + 60), 150
                verre_clair(c, -w / 2, -h / 2, w, h, 36, borne(e * 3))
                if k == 0:
                    iw, ih = taille_img("sigle-gsx"); image(c, "sigle-gsx", -30, -60, 60, borne(e * 3))
                else:
                    icone(c, ic, 0, -28, 54, ROUGE, 2.6, borne(e * 3))
                texte(c, lab, 0, 14, 30, ENCRE, "titre", "centre", -0.01, borne(e * 3))
                c.restore()
            c.save(); c.translate(CX, cy); s = mix(0.3, 1, u) * (1 + 0.06 * battement(t, T_ENTOUR, 1, 0.4) - 0.06) * mix(1, 0.85, etape); c.scale(s, s)
            lueur_s(c, 0, 0, 260, ROUGE, 0.14 * borne(u * 2))
            disque(c, 0, 0, 108, ENCRE, borne(u * 3), (14, 36, 0.3)); icone(c, "user", 0, -22, 60, BLANC, 2.8, borne(u * 3))
            texte(c, "VOUS", 0, 18, 36, BLANC, "archivo", "centre", 0, borne(u * 3))
            c.restore()
            if etape > 0:      # « au cœur de chaque étape » : la piste, le point rouge qui avance, les coches
                y = 1240; x0, x1 = CX - 320, CX + 320
                with Calque(c, etape):
                    rrect(c, x0, y - 5, x1 - x0, 10, 5, "#D5DAE3")
                    p = prog(t, T_COEUR - 0.2, T_ETAPE + 0.3 - T_COEUR, lin)
                    rrect(c, x0, y - 5, (x1 - x0) * p, 10, 5, ROUGE)
                    for i, (lab, ic) in enumerate(ETAPES):
                        x = x0 + i * (x1 - x0) / 4
                        on = p >= i / 4 - 0.01
                        disque(c, x, y, 34 if on else 28, ROUGE if on else BLANC, 1, (6, 16, 0.2))
                        icone(c, ic if not on else "check", x, y, 32, BLANC if on else GRIS, 2.6)
                        texte(c, lab, x, y + 46, 22, ENCRE if on else GRIS, "titre", "centre", -0.01)
                    disque(c, mix(x0, x1, p), y, 12, BLANC)
        titre2(c, t, "AVEC GSX", "PAS UN SIMPLE FOURNISSEUR", T_AVEC - 0.05, T_VOUS - 0.15, t2=T_CHERCHEZ - 0.1)
        titre2(c, t, "VOUS VOUS ENTOUREZ", "D'UN PARTENAIRE", T_VOUS - 0.15, T_VEILLE - 0.15, t2=T_PARTN2 - 0.1, c2=ROUGE, e1="ressort")
        titre2(c, t, "VOS INTÉRÊTS AU CŒUR", "DE CHAQUE ÉTAPE", T_VEILLE - 0.15, T_FIN - 0.05, t2=T_COEUR - 0.1)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8)
for t0, _, _ in VOLS:
    if 0 <= t0: son(t0, "whoosh_court", -13); son(t0 + 0.03, "message_in", -15)
son(TW(8), "impact_doux", -7); son(TW(8) + 0.02, "ching", -12)
for tk, _ in ARRIVEES: son(tk - 0.15, "whoosh", -9); son(tk + 0.08, "impact", -7)
son(T_GRANDE - 0.1, "pop", -10)
son(T_MAIS - 0.1, "whoosh_bas", -8); son(T_QUEST - 0.1, "impact_doux", -8); son(T_CODES - 0.1, "pop", -10)
for i in range(8): son(T_CODES + 0.05 + i * 0.12, "tick", -16)
son(T_CAR - 0.12, "whoosh_long", -9)
for i in range(11): son(T_CAR + 0.1 + i * 0.045, "frappe", -18)
for k in range(4): son(T_TROUVER - 0.3 + 0.08 * k, "pop", -14)
son(T_USINE + 0.05, "clic", -6); son(T_INTERNET - 0.05, "croc", -7); son(T_INTERNET, "tampon", -8)
son(T_IL - 0.12, "swipe", -9)
for tk, _, _, _ in SAVOIRS[:3]: son(tk - 0.12, "whoosh_court", -10); son(tk + 0.35, "check", -10)
son(T_DIST - 0.15, "whoosh", -8); son(T_OPPV - 0.05, "check", -8); son(T_OPPV, "ching", -11); son(T_MAUV - 0.05, "croc", -7)
son(T_SURTOUT - 0.12, "whoosh_long", -8); son(T_DEFEND - 0.1, "pop", -9); son(T_MILLIERS - 0.2, "montee", -12); son(T_KM - 0.1, "pop", -10)
son(T_FOURN - 0.15, "ding", -12)
son(T_CEST - 0.1, "whoosh_bas", -7); son(T_GSX - 0.1, "montee", -11); son(T_GSX, "impact", -4); son(T_GSX + 0.05, "ching", -9)
son(T_ROLE - 0.15, "whoosh", -8)
for tk in (T_ACC, T_AIDER): son(tk - 0.15, "whoosh_court", -9); son(tk, "impact_doux", -9)
son(T_SOURC - 0.1, "pop", -10); son(T_PART - 0.1, "pop", -10); son(T_EXIG - 0.05, "check", -9)
son(T_LIEN - 0.2, "whoosh_long", -8); son(T_LIEN + 0.45, "impact_doux", -7); son(T_LIEN + 0.5, "ching", -10)
son(T_OBJ - 0.1, "pop", -11); son(T_TERRAIN - 0.1, "pop", -11)
son(T_PARCE - 0.12, "swipe", -9); son(T_QUAL - 0.1, "whoosh_bas", -8); son(T_QUAL + 0.2, "impact", -6); son(T_QUAL + 0.25, "ching", -10)
son(T_AVEC - 0.12, "whoosh", -9)
for i in range(13): son(T_CHERCHEZ - 0.05 + i * 0.035, "frappe", -18)
son(T_FOURN2 + 0.15, "swipe", -10); son(T_FOURN2 + 0.3, "croc", -8)
son(T_VOUS - 0.2, "whoosh_bas", -8); son(T_VOUS, "impact_doux", -8)
for tk, _, _ in SATELLITES: son(tk - 0.12, "pop", -10)
son(T_VEILLE - 0.15, "whoosh_court", -10)
for i in range(5): son(T_COEUR - 0.2 + i * (T_ETAPE + 0.3 - T_COEUR) / 4, "check", -12)
sons_signature(son, T_FIN)
for i, tl in enumerate((T_LA, T_ENCORE)): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_ON - 0.15, T_ON + 0.2), (T_MAIS - 0.1, T_MAIS + 0.25), (T_CAR - 0.15, T_CAR + 0.25), (T_IL - 0.15, T_IL + 0.25),
             (T_DIST - 0.15, T_DIST + 0.25), (T_SURTOUT - 0.15, T_SURTOUT + 0.25), (T_ROLE - 0.15, T_ROLE + 0.25), (T_LIEN - 0.2, T_LIEN + 0.25),
             (T_PARCE - 0.15, T_PARCE + 0.25), (T_AVEC - 0.15, T_AVEC + 0.25), (T_VOUS - 0.2, T_VOUS + 0.2), (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(8), ROUGE, 0.06), (T_INTERNET, ROUGE, 0.06), (T_OPPV, VERT, 0.05), (T_GSX, "#FFFFFF", 0.12), (T_QUAL + 0.2, "#FFFFFF", 0.1)]:
    eclair(tt, cc_, a_)


SIGN_MEDIAS = [(n, True) for n in RUSHES[:6]]


def dessine(c, t):
    _T[0] = t
    fond_clair(c, t)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_promesses(c, t); scene_internet(c, t); scene_savoirs(c, t); scene_distance(c, t)
    r = scene_gsx(c, t)
    with Balance(c, t, 0.8):
        if r < 2100:
            scene_role(c, t); scene_balance(c, t); scene_partenaire(c, t)
    entete(c, t)
    signature_gsx(c, t, T_FIN, SIGN_MEDIAS, [("La Chine est une opportunité.", T_LA, 50, ENCRE),
                                               ("Encore faut-il savoir avec qui la saisir.", T_ENCORE, 44, ROUGE)], cy=860)
    K.dessine_eclairs(c, t)
    cache = (T_CEST - 0.1 < t < T_ROLE - 0.05) or t > T_FIN - 0.1
    if not cache: SOUS.dessine(c, t, ENCRE)
