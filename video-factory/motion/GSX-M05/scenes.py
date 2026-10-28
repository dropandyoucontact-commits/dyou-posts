"""GSX-M05 « Votre fournisseur en Chine vous a dit oui. » — hook écrit par nous (20/10/2026), pas par le client.
Levier : prémisse à contre-pied (le « oui » qui devrait inquiéter) + lecture active (les bulles « Oui ✓ » qui s'empilent).
Persona : dirigeant francophone qui importe ou veut importer, loin du terrain, qui a déjà vécu l'échantillon parfait
et la production différente, l'acompte versé et le silence. Même forme que GSX-M01 → M04 (moteur/gsx.py), plus :
bulles de conversation en 3D, carte qui se retourne (oui → non), échantillon / production côte à côte, points de
frappe qui n'aboutissent jamais, cadenas de vérification, « OUI » vérifié par GSX, signature explosive.
Aucun chiffre, aucune promesse de gain. Zone sûre TikTok / Snap : x 130-860, axe CX = 510."""
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

# repères (mots)
T_DIT, T_OUI0, T_OUI1, T_OUI2, T_OUI3 = TW(6), TW(7), TW(8), TW(12), TW(16)
T_ET, T_LA, T_INQ = TW(20), TW(23), TW(29)
T_CAR, T_UNOUI, T_NEST, T_ENGAG = TW(30), TW(33), TW(35), TW(39)
T_CEST1, T_FACON, T_POLIE, T_NON = TW(40), TW(43), TW(44), TW(50)
T_ECH, T_PARFAIT, T_PROD, T_ARRIVE, T_DIFF = TW(51), TW(53), TW(54), TW(57), TW(58)
T_ACOMPTE, T_VERSE, T_ETR, T_REP, T_ATTENDRE = TW(59), TW(61), TW(62), TW(64), TW(67)
T_A, T_MILLIERS, T_KM, T_AUCUN, T_VERIF = TW(68), TW(70), TW(72), TW(75), TW(78)
T_ALORS, T_QUI, T_VERITE, T_TERRAIN = TW(79), TW(80), TW(84), TW(87)
T_CEST, T_GSX, T_INTERV = TW(88), TW(91), TW(92)
T_NOUS, T_SELECT, T_VERIFIONS, T_FOURN, T_AVANT, T_ENGAGIEZ = TW(93), TW(94), TW(96), TW(98), TW(99), TW(104)
T_NEGO, T_NOM = TW(106), TW(109)
T_SUIV, T_OPER, T_PLACE, T_EXIG, T_COMPR, T_RESP = TW(112), TW(114), TW(116), TW(120), TW(122), TW(124)
T_PARCE, T_VRAI, T_OUIV, T_VERIFIE = TW(125), TW(127), TW(131), TW(135)
T_FIN, T_L1, T_L2 = TW(136), TW(137), TW(143)

RUSHES = ["rushes/presses-jaunes", "rushes/chaine-electronique", "rushes/atelier-valises", "rushes/entrepot-bleu",
          "rushes/cartons-ouvrieres", "rushes/entrepot-colis"]


# ─────────────────────────────────────────── briques locales
def bulle_v(c, txt, cx, cy, a, droite=True, fond_=None, col=None, taille=34, ic=None, ic_col=None, w_min=0):
    """bulle de conversation en verre clair (gauche) ou pleine encre (droite) qui naît de son coin ; renvoie (w, h)"""
    if a <= 0.01: return 0, 0
    tw = largeur(txt, taille, "titre", -0.01)
    ic_w = taille * 1.15 if ic else 0
    w, h = max(w_min, tw + ic_w + (taille * 0.4 if ic else 0) + taille * 1.3), taille * 2.1
    ax = cx + w / 2 if droite else cx - w / 2
    c.save(); c.translate(ax, cy + h / 2); s = mix(0.3, 1, a); c.scale(s, s); c.translate(-ax, -(cy + h / 2))
    with Calque(c, borne(a * 2.5)):
        if fond_:
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), h * 0.42, h * 0.42)
            p = skia.Paint(AntiAlias=True, Color=hexa(fond_, 0.3), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
            c.save(); c.translate(0, 10); c.drawRRect(rr, p); c.restore()
            c.drawRRect(rr, peinture(fond_))
        else:
            verre_clair(c, cx - w / 2, cy - h / 2, w, h, h * 0.42, 1.0, 0.7)
        # la petite queue vers le coin
        qx = cx + w / 2 - 16 if droite else cx - w / 2 + 16
        pth = skia.Path(); pth.moveTo(qx, cy + h / 2 - 4); pth.lineTo(qx + (10 if droite else -10), cy + h / 2 + 18); pth.lineTo(qx + (-18 if droite else 18), cy + h / 2 - 4); pth.close()
        c.drawPath(pth, peinture(fond_ or "#F4F6FA"))
        x = cx - w / 2 + taille * 0.65
        texte(c, txt, x, cy - hauteurLigne(taille, "titre") / 2, taille, col or (BLANC if fond_ else ENCRE), "titre", track=-0.01)
        if ic: icone(c, ic, cx + w / 2 - taille * 0.65 - ic_w / 2, cy, ic_w * 0.9, ic_col or VERT, 2.8)
    c.restore()
    return w, h


def points_frappe(c, cx, cy, t, a):
    """« … » en train d'écrire, qui n'aboutit jamais"""
    if a <= 0.01: return
    w, h = 150, 74
    with Calque(c, borne(a * 3)):
        verre_clair(c, cx - w / 2, cy - h / 2, w, h, 37, 1.0, 0.5)
        for j in range(3):
            y = cy + 8 * math.sin(t * 7 + j * 1.1)
            disque(c, cx - 36 + j * 36, y, 11, GRIS, 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 7 + j * 1.1)))


def ecran_chat(c, w, h, t):
    """l'écran de conversation du hook : « Le prix ? » « Oui ✓ », « Le délai ? » « Oui ✓ », « La qualité ? » « Oui ✓ »"""
    verre_clair(c, 0, 0, w, h, 44)
    rrect(c, 0, 0, w, 110, 44, "#FFFFFF", 0.9); trait(c, 24, 110, w - 24, 110, "#E3E7EE", 2)
    disque(c, 64, 55, 32, ENCRE); icone(c, "factory", 64, 55, 32, BLANC, 2.4)
    texte(c, "Fournisseur", 112, 30, 30, ENCRE, "titre", track=-0.01)
    disque(c, 122, 76, 7, VERT); texte(c, "en ligne", 136, 64, 22, GRIS, "demi", track=0)
    QA = [("Le prix ?", -0.5, T_OUI1), ("Le délai ?", -0.38, T_OUI2), ("La qualité ?", -0.26, T_OUI3)]   # les 3 questions déjà posées à l'image 0
    y = 150
    for k, (q, tq, to) in enumerate(QA):
        a = entre(t, tq, 0.35, 2.0)
        if a <= 0:
            continue
        bulle_v(c, q, 40, y + 36, a, droite=False, fond_=ENCRE)
        y += 100
        b = entre(t, to - 0.04, 0.4, 2.2)
        if b > 0:
            inq = prog(t, T_LA + 0.12 * k, 0.3, sortie)        # « là que vous auriez dû vous inquiéter » : la coche devient « ? »
            bulle_v(c, "Oui", w - 40, y + 36, b, droite=True, ic="check" if inq < 0.5 else "circle-help",
                    ic_col=VERT if inq < 0.5 else ROUGE, w_min=190)
            if inq > 0 and inq < 1: eclats(c, w - 70, y + 36, t, T_LA + 0.12 * k, 6, 120, cols=[ROUGE, GRIS], graine=40 + k, duree=0.5)
        y += 100
    balayage(c, 0, 0, w, h, t, 44, 0.35, 0.3)


# ─────────────────────────────────────────── 1 · hook : il vous a dit oui, oui, oui — et c'est là qu'il fallait s'inquiéter
def scene_hook(c, t):
    t1 = T_CAR - 0.12
    g = Groupe(c, t, -1, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        o = prog(t, -0.3, 1.6, douce)
        sx, sy = secousse(t, T_INQ, 16, 0.35)
        cam = Cam(ax=-12 + 3 * math.sin(t * 0.9), ay=mix(-26, 8, o) + 5 * math.sin(t * 0.7), tz=mix(260, 0, prog(t, -0.3, 0.9, sortie)), cx=CX + sx, cy=1010 + sy)
        W_, H_ = 620, 760
        scene3d(c, cam, [Plan(coins((0, 0, 0), W_, H_, ay=0), W_, H_, lambda cc, w, h: ecran_chat(cc, w, h, t))])
        for k, tk in enumerate((T_OUI1, T_OUI2, T_OUI3)):
            if t > tk:
                onde(c, CX + 200, 760 + k * 200, t, tk + 0.05, 40, 260, VERT, 6, 0.45)
                eclats(c, CX + 200, 760 + k * 200, t, tk + 0.05, 8, 220, cols=[VERT, ENCRE, "#9AA8BF"], graine=10 + k, duree=0.6)
        if t > T_LA - 0.05:
            lueur_s(c, CX, 1000, 560, ROUGE, 0.12 * prog(t, T_LA, 0.4))
            pill_v(c, "Vous auriez dû vous inquiéter", CX, 1330, entre(t, T_INQ - 0.35, 0.4, 2.2), "triangle-alert", plein=True, rot=-2)
        titre2(c, t, "VOTRE FOURNISSEUR EN CHINE", "VOUS A DIT OUI.", -0.6, T_OUI1 - 0.1, t2=-0.45)
        for k, (tk, l2) in enumerate(((T_OUI1, "OUI POUR LE PRIX"), (T_OUI2, "OUI POUR LE DÉLAI"), (T_OUI3, "OUI POUR LA QUALITÉ"))):
            fin = (T_OUI2, T_OUI3, T_ET)[k] - 0.08
            titre2(c, t, None, l2, tk - 0.08, fin, t2=tk - 0.08, e2="ressort", c2=VERT if k < 2 else ENCRE)
        titre2(c, t, "C'EST PRÉCISÉMENT LÀ", "QU'IL FALLAIT S'INQUIÉTER", T_ET - 0.08, t1, t2=T_LA - 0.08, c2=ROUGE)


# ─────────────────────────────────────────── 2 · en Chine, un oui n'est pas toujours un engagement (le lien se casse)
def carte_mot(mot, col=ENCRE, ic=None, accent=ROUGE):
    def f(c, w, h):
        verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 1.0, accent)
        if ic: tuile_v(c, ic, w / 2, h * 0.34, w * 0.38, accent)
        texte(c, mot, w / 2, h * (0.6 if ic else 0.5) - hauteurLigne(ajuste(mot, w * 0.84, w * 0.2, "archivo", -0.02), "archivo") / 2,
              ajuste(mot, w * 0.84, w * 0.2, "archivo", -0.02), col, "archivo", "centre", -0.02)
        balayage(c, 0, 0, w, h, T_COURANT[0], w * 0.1, 0.4, 0.4)
    return f


def scene_engagement(c, t):
    t0, t1 = T_CAR - 0.12, T_CEST1 - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.55, 1.5)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=6 * math.sin(t * 0.8), cx=CX, cy=1000)
        CW, CH = 300, 360
        plans = []
        u1 = prog(t, T_UNOUI - 0.12, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_UNOUI - 0.12 else 0.0
        u2 = prog(t, T_ENGAG - 0.35, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_ENGAG - 0.35 else 0.0
        casse = prog(t, T_NEST + 0.1, 0.4, sortie)
        if u1 > 0:
            plans.append(Plan(coins((-190 - 60 * casse, 20 * casse, mix(1400, 0, min(u1, 1.05))), CW, CH, ay=12, az=-6 * casse), CW, CH,
                              carte_mot("OUI", ENCRE, "message-circle", ENCRE), borne(u1 * 3)))
        if u2 > 0:
            plans.append(Plan(coins((190 + 60 * casse, -20 * casse, mix(1400, 0, min(u2, 1.05))), CW, CH, ay=-12, az=6 * casse), CW, CH,
                              carte_mot("ENGAGEMENT", ENCRE, "file-text", ENCRE), borne(u2 * 3)))
        scene3d(c, cam, plans)
        if u2 > 0: lien(c, t, CX - 60, CX + 60, 1000, T_ENGAG - 0.2, casse=T_NEST + 0.1)
        if t > T_NEST + 0.1:
            croix_v(c, CX, 1000, 44, entre(t, T_NEST + 0.15, 0.35, 2.4))
            eclats(c, CX, 1000, t, T_NEST + 0.15, 10, 300, cols=[ROUGE, ENCRE], graine=8)
        # la Chine en rouge sur un petit globe au-dessus
        with Calque(c, borne(a * 3)):
            globe(c, 100 + 6 * t, 24, CX, 680, 150 * mix(0.6, 1, a), 1.0, 1.0, france=False)
        titre2(c, t, "CAR EN CHINE", "UN OUI N'EST PAS TOUJOURS", T_CAR - 0.05, T_ENGAG - 0.12, t2=T_UNOUI - 0.1)
        titre2(c, t, None, "UN ENGAGEMENT", T_ENGAG - 0.12, t1, t2=T_ENGAG - 0.1, c2=ROUGE, e2="ressort")


# ─────────────────────────────────────────── 3 · une façon polie de ne pas vous dire non (la carte se retourne)
def face_oui(c, w, h):
    verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 0.8, VERT)
    tuile_v(c, "smile", w / 2, h * 0.3, w * 0.34, VERT)
    texte(c, "OUI", w / 2, h * 0.56, w * 0.26, ENCRE, "archivo", "centre", -0.02)
    texte(c, "bien sûr, pas de problème", w / 2, h * 0.82, ajuste("bien sûr, pas de problème", w * 0.86, w * 0.07, "demi", 0), GRIS, "demi", "centre", 0)
    balayage(c, 0, 0, w, h, T_COURANT[0], w * 0.1, 0.4, 0.4)


def face_non(c, w, h):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, 0, w, h), w * 0.1, w * 0.1)
    c.drawRRect(rr, pgrad_(0, 0, w, h, [ROUGE, "#A80020"]))
    c.drawRRect(rr, peinture("#FFFFFF", 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
    disque(c, w / 2, h * 0.3, w * 0.17, BLANC); icone(c, "x", w / 2, h * 0.3, w * 0.2, ROUGE, 3.2)
    texte(c, "NON", w / 2, h * 0.56, w * 0.26, BLANC, "archivo", "centre", -0.02)
    texte(c, "ce qu'il ne vous dit pas", w / 2, h * 0.82, ajuste("ce qu'il ne vous dit pas", w * 0.86, w * 0.07, "demi", 0), "#FFD5DA", "demi", "centre", 0)


def scene_poli(c, t):
    t0, t1 = T_CEST1 - 0.12, T_ECH - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        flip = prog(t, T_NON - 0.3, 0.6, entreeSortie)
        ay = mix(0, 180, flip) + 6 * math.sin(t * 1.4) * (1 - flip)
        cam = Cam(ax=-8 + 2 * math.sin(t), ay=4 * math.sin(t * 0.8), tz=mix(300, 0, a), cx=CX, cy=1000)
        CW, CH = 420, 520
        sx, sy = secousse(t, T_NON + 0.3, 12, 0.3)
        plans = [Plan(coins((sx, sy, 0), CW, CH, ay=ay), CW, CH, face_oui, borne(a * 3)),
                 Plan(coins((sx, sy, 0), CW, CH, ay=ay + 180), CW, CH, face_non, borne(a * 3))]
        scene3d(c, cam, plans)
        if t > T_NON + 0.25:
            onde(c, CX, 1000, t, T_NON + 0.3, 80, 520, ROUGE, 8, 0.6)
            eclats(c, CX, 1000, t, T_NON + 0.3, 14, 420, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=12)
        pill_v(c, "Une façon polie", CX, 690, entre(t, T_FACON - 0.1, 0.4, 2.2), "heart-handshake", taille=30)
        titre2(c, t, "C'EST PARFOIS", "UNE FAÇON POLIE", T_CEST1 - 0.05, T_NON - 0.3, t2=T_FACON - 0.08)
        titre2(c, t, "DE NE PAS", "VOUS DIRE NON", T_NON - 0.3, t1, t2=T_NON - 0.2, c2=ROUGE, e1="ressort")


# ─────────────────────────────────────────── 4 · l'échantillon est parfait, la production arrive différente
def scene_echantillon(c, t):
    t0, t1 = T_ECH - 0.12, T_ACOMPTE - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=6 * math.sin(t * 0.8), cx=CX, cy=1000)
        CW, CH = 320, 500
        u1 = prog(t, T_ECH - 0.05, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_ECH - 0.05 else 0.0
        u2 = prog(t, T_PROD - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_PROD - 0.1 else 0.0
        dec = prog(t, T_PROD - 0.1, 0.5, entreeSortie)              # l'échantillon se pousse à gauche
        plans = []
        if u1 > 0:
            plans.append(Plan(coins((mix(0, -185, dec), 0, mix(1400, 0, min(u1, 1.05))), CW, CH, ay=mix(0, 12, dec)), CW, CH,
                              carte_rush("rushes/presses-jaunes", T_ECH - 0.3, label="Échantillon", ic="badge-check", accent=VERT), borne(u1 * 3)))
        if u2 > 0:
            def prod(cc, w, h):
                carte_rush("rushes/presses-jaunes", T_ECH - 0.3 + 2.4, label="Production", ic="triangle-alert", accent=ROUGE)(cc, w, h)
                d = prog(t, T_DIFF - 0.05, 0.4, sortie)
                if d > 0:                                           # un voile gris-rouge : « différente »
                    cc.save(); cc.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(w * 0.045, w * 0.045, w * 0.91, h - w * 0.09), w * 0.055, w * 0.055), True)
                    cc.drawRect(skia.Rect.MakeWH(w, h), peinture("#6B7280", 0.45 * d))
                    for j in range(6):
                        yy = h * (0.18 + 0.12 * j)
                        trait(cc, w * 0.1, yy, w * 0.9, yy + 14 * ((-1) ** j), ROUGE, 3, 0.5 * d, [10, 12])
                    cc.restore()
            plans.append(Plan(coins((185, 0, mix(1400, 0, min(u2, 1.05))), CW, CH, ay=-12), CW, CH, prod, borne(u2 * 3)))
        scene3d(c, cam, plans)
        coche_v(c, CX - 185 * dec, 740, 50, entre(t, T_PARFAIT - 0.05, 0.35, 2.4))
        d = entre(t, T_DIFF - 0.05, 0.4, 2.4)
        if d > 0:
            croix_v(c, CX + 185, 740, 50, d)
            eclats(c, CX + 185, 740, t, T_DIFF, 12, 320, cols=[ROUGE, GRIS, ENCRE], graine=14)
            pill_v(c, "Différente", CX + 180, 1300, d, "triangle-alert", plein=True, rot=-3)
        pill_v(c, "Parfait", CX - 180 * dec, 1300, entre(t, T_PARFAIT - 0.05, 0.4, 2.2), "badge-check", accent=VERT)
        titre2(c, t, "L'ÉCHANTILLON", "EST PARFAIT", T_ECH - 0.05, T_PROD - 0.1, t2=T_PARFAIT - 0.1, c2=VERT)
        titre2(c, t, "LA PRODUCTION, ELLE,", "ARRIVE DIFFÉRENTE", T_PROD - 0.1, t1, t2=T_DIFF - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 5 · l'acompte est versé, et les réponses se font attendre
def scene_acompte(c, t):
    t0, t1 = T_ACOMPTE - 0.12, T_A - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="zoom", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        sil = prog(t, T_ETR - 0.1, 0.5, entreeSortie)
        # le virement
        c.save(); c.translate(CX, mix(960, 760, sil)); c.rotate(-3 + 2 * math.sin(t * 1.3)); s = mix(0.4, 1, a) * mix(1, 0.78, sil); c.scale(s, s)
        with Calque(c, borne(a * 3)):
            verre_clair(c, -330, -130, 660, 260, 44, 1.0, 0.8)
            tuile_v(c, "banknote", -240, -20, 110, ENCRE)
            texte(c, "Acompte", -160, -66, 44, ENCRE, "archivo", track=-0.02)
            texte(c, "virement international", -160, 0, 28, GRIS, "demi", track=0)
            v = prog(t, T_VERSE - 0.1, 0.45, entreeSortie)
            rrect(c, -160, 56, 440, 26, 13, "#E3E7EE"); rrect(c, -160, 56, 440 * v, 26, 13, VERT if v >= 0.99 else ENCRE)
            e = entre(t, T_VERSE + 0.3, 0.35, 2.4)
            if e > 0:
                pill_v(c, "Envoyé", 220, -60, e, "check", VERT, taille=26, plein=True)
        c.restore()
        if t > T_VERSE + 0.3: eclats(c, CX + 220, 900, t, T_VERSE + 0.3, 8, 220, cols=[VERT, ENCRE], graine=15, duree=0.6)
        # puis le silence : vos messages, « vu », les points qui n'aboutissent pas, l'horloge
        if sil > 0:
            with Calque(c, sil):
                y = 960
                bulle_v(c, "Où en est la production ?", CX + 300, y, entre(t, T_ETR, 0.35, 2.0), droite=True, fond_=ENCRE, taille=30)
                texte(c, "Vu", CX + 300, y + 44, 22, GRIS, "demi", "droite", 0, entre(t, T_REP - 0.2, 0.3, 2.0))
                bulle_v(c, "Une date de livraison ?", CX + 300, y + 110, entre(t, T_REP, 0.35, 2.0), droite=True, fond_=ENCRE, taille=30)
                texte(c, "Vu", CX + 300, y + 154, 22, GRIS, "demi", "droite", 0, entre(t, T_REP + 0.3, 0.3, 2.0))
                points_frappe(c, CX - 220, y + 230, t, entre(t, T_REP + 0.25, 0.4, 2.0))
                h = entre(t, T_ATTENDRE - 0.1, 0.45, 2.0)
                if h > 0:
                    c.save(); c.translate(CX + 250, y + 240); c.scale(h, h)
                    disque(c, 0, 0, 54, BLANC, 1, (8, 20, 0.22)); anneau(c, 0, 0, 54, "#D5DAE3", 3)
                    for k in range(12): trait(c, 44 * math.cos(k * math.pi / 6), 44 * math.sin(k * math.pi / 6), 48 * math.cos(k * math.pi / 6), 48 * math.sin(k * math.pi / 6), GRIS, 2)
                    ag = (t - T_ATTENDRE) * 9
                    trait(c, 0, 0, 34 * math.cos(ag), 34 * math.sin(ag), ROUGE, 5); trait(c, 0, 0, 22 * math.cos(ag / 12), 22 * math.sin(ag / 12), ENCRE, 6)
                    c.restore()
        titre2(c, t, "L'ACOMPTE", "EST VERSÉ", T_ACOMPTE - 0.05, T_ETR - 0.1, t2=T_VERSE - 0.1)
        titre2(c, t, "ET LES RÉPONSES", "SE FONT ATTENDRE", T_ETR - 0.1, t1, t2=T_REP - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 6 · à des milliers de kilomètres, aucun moyen de vérifier ; qui dit la vérité ?
def scene_distance(c, t):
    t0, t1 = T_A - 0.12, T_CEST - 0.05
    g = Groupe(c, t, t0, t1, ent="zoom", sor="aucune", d_in=0.4)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.3)
        lon = mix(30, 64, prog(t, t0, t1 - t0, douce))
        R = 360 * mix(0.7, 1, a)
        cx, cy = CX, 1000
        G = globe(c, lon, 30, cx, cy, R, prog(t, T_MILLIERS - 0.2, 0.6, sortie), borne(a * 3))
        u = prog(t, T_MILLIERS - 0.2, 1.0, entreeSortie)
        if u > 0:
            G.arc(c, FR, CN, cx, cy, R, lon, 30, u, ROUGE, 7, 0.35, [16, 12])
        G.repere(c, *FR, cx, cy, R, lon, 30, "Vous", ENCRE, "FR", entre(t, T_A + 0.1, 0.4, 2.0), haut=60)
        G.repere(c, *CN, cx, cy, R, lon, 30, "Votre fournisseur", ROUGE, "CN", entre(t, T_KM - 0.1, 0.4, 2.0), haut=70)
        oe = entre(t, T_AUCUN - 0.1, 0.45, 2.0)
        if oe > 0:
            c.save(); c.translate(CX + 250, 690); c.rotate(6 * math.sin(t * 2)); s = mix(0.3, 1, oe); c.scale(s, s)
            verre_clair(c, -110, -110, 220, 220, 60, borne(oe * 3), 1.0, ROUGE)
            icone(c, "eye-off", 0, -10, 110, ROUGE, 2.6, borne(oe * 3))
            disque(c, 74, 70, 34, ENCRE, borne(oe * 3)); texte(c, "?", 74, 70 - hauteurLigne(46, "archivo") / 2, 46, BLANC, "archivo", "centre", 0, borne(oe * 3))
            c.restore()
        pill_v(c, "Aucun moyen de vérifier", CX, 1300, entre(t, T_VERIF - 0.25, 0.4, 2.2) * (1 - prog(t, T_ALORS, 0.3)), "eye-off", plein=True)
        q = entre(t, T_QUI - 0.1, 0.5, 2.0)
        if q > 0:
            kx, ky, _ = G.pos(*CN, lon, 30, R, cx, cy)
            onde(c, kx, ky, t, T_QUI, 40, 300, ROUGE, 6, 0.6)
            c.save(); c.translate(CX, 1300); c.scale(mix(0.3, 1, q), mix(0.3, 1, q)); c.rotate(6 * math.sin(t * 2.4))
            disque(c, 0, 0, 86, ENCRE, borne(q * 3), (14, 36, 0.3)); icone(c, "circle-help", 0, 0, 110, BLANC, 2.4, borne(q * 3))
            c.restore()
        titre2(c, t, "À DES MILLIERS DE KILOMÈTRES", "AUCUN MOYEN DE VÉRIFIER", T_A - 0.05, T_ALORS - 0.1, t2=T_AUCUN - 0.1, c2=ROUGE)
        titre2(c, t, "ALORS, QUI VOUS DIT LA VÉRITÉ", "SUR LE TERRAIN ?", T_ALORS - 0.1, t1, t2=T_VERITE - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 7 · ce que fait GSX : sélection / vérification, négociation, suivi sur place
ETAPES = [(T_NOUS, "rushes/chaine-electronique", "search", "Sélection et vérification", "NOUS SÉLECTIONNONS", "ET VÉRIFIONS VOS FOURNISSEURS"),
          (T_NEGO, "rushes/atelier-valises", "scale", "Négociation en votre nom", "NOUS NÉGOCIONS", "EN VOTRE NOM"),
          (T_SUIV, "rushes/entrepot-colis", "map-pin", "Suivi sur place", "NOUS SUIVONS VOS OPÉRATIONS", "SUR PLACE")]


def scene_gsx_actions(c, t):
    t0, t1 = T_NOUS - 0.1, T_PARCE - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.8), ay=6 * math.sin(t * 0.7), cx=CX, cy=840)
        CW, CH = 300, 400
        plans = []
        for k, (tk, nom, ic, lab, _, _) in enumerate(ETAPES):
            u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.6)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            suiv = ETAPES[k + 1][0] if k < 2 else None
            rec = prog(t, suiv - 0.15, 0.5, entreeSortie) if suiv else 0.0
            x = mix(0, -330 + 110 * k, rec); z = mix(1400, 0, min(u, 1.05)) + 500 * rec; y = -120 * rec
            plans.append(Plan(coins((x, y, z), CW, CH, ay=mix(0, 18, rec)), CW, CH, carte_rush(nom, tk - 0.3, label=lab if rec < 0.5 else None, ic=ic), borne(u * 3) * (1 - 0.5 * rec)))
        scene3d(c, cam, plans)
        # vérification : le cadenas qui se ferme et le bouclier GSX sur le fournisseur choisi
        v = entre(t, T_VERIFIONS - 0.05, 0.45, 2.2) * (1 - prog(t, T_NEGO - 0.15, 0.3))
        if v > 0:
            bouclier(c, t, CX + 190, 690, T_VERIFIONS - 0.05, VERT, marque=None, taille=0.8)
            pill_v(c, "Vérifié avant engagement", CX, 1120, entre(t, T_AVANT - 0.1, 0.4, 2.2) * v, "shield-check", accent=VERT)
        n = entre(t, T_NOM - 0.1, 0.4, 2.2) * (1 - prog(t, T_SUIV - 0.15, 0.3))
        pill_v(c, "En votre nom", CX, 1120, n, "user", plein=True)
        # suivi : exigences comprises ✓ respectées ✓
        for k, (tk, lab) in enumerate(((T_COMPR, "Comprises"), (T_RESP, "Respectées"))):
            pill_v(c, lab, CX - 160 + 320 * k, 1200, entre(t, tk - 0.1, 0.4, 2.2), "check", VERT, taille=30, plein=True)
            if t > tk: eclats(c, CX - 160 + 320 * k, 1200, t, tk, 8, 200, cols=[VERT, ENCRE], graine=50 + k, duree=0.6)
        pill_v(c, "Vos exigences", CX, 1320, entre(t, T_EXIG - 0.1, 0.4, 2.2), "file-text", taille=28)
        for k, (tk, _, _, _, l1, l2) in enumerate(ETAPES):
            fin = ETAPES[k + 1][0] - 0.12 if k < 2 else T_EXIG - 0.1
            t2 = (T_SELECT, T_NEGO, T_OPER)[k]
            titre2(c, t, l1, l2, tk - 0.08, fin, t2=t2 - 0.05, e1="ressort" if k else "masque")
        titre2(c, t, "POUR QUE VOS EXIGENCES SOIENT", "COMPRISES ET RESPECTÉES", T_EXIG - 0.1, t1, t2=T_COMPR - 0.1, c2=VERT)


# ─────────────────────────────────────────── 8 · un vrai oui, c'est un oui vérifié (la bulle du hook revient, sous le bouclier GSX)
def scene_vrai_oui(c, t):
    t0, t1 = T_PARCE - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="bas", sor="recul", d_in=0.35, d_out=0.4)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.55, 1.5)
        ver = prog(t, T_VERIFIE - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.6)) if t > T_VERIFIE - 0.1 else 0.0
        sx, sy = secousse(t, T_VERIFIE, 14, 0.3)
        c.save(); c.translate(CX + sx, 980 + sy); c.rotate(-3 + 2 * math.sin(t * 1.4)); s = mix(0.4, 1, a); c.scale(s, s)
        with Calque(c, borne(a * 3)):
            verre_clair(c, -300, -170, 600, 340, 60, 1.0, 1.2, VERT if ver > 0 else ROUGE)
            texte(c, "OUI", 0, -hauteurLigne(150, "archivo") / 2 - 20, 150, ENCRE, "archivo", "centre", -0.03)
            b = prog(t, T_OUIV - 0.05, 0.4, sortie)
            if b > 0: rrect(c, -140 * b, 100, 280 * b, 8, 4, VERT if ver > 0 else ROUGE)
        c.restore()
        if ver > 0:
            c.save(); c.translate(CX + 250 + sx, 800 + sy); c.rotate(-8); c.scale(min(ver, 1.1), min(ver, 1.1))
            disque(c, 0, 0, 92, BLANC, 1, (12, 30, 0.25)); anneau(c, 0, 0, 92, VERT, 6)
            icone(c, "shield-check", 0, -8, 86, VERT, 2.8)
            iw, ih = taille_img("sigle-gsx"); image(c, "sigle-gsx", -30, 34, 60)
            c.restore()
            onde(c, CX + 250, 800, t, T_VERIFIE, 60, 460, VERT, 8, 0.6)
            eclats(c, CX, 980, t, T_VERIFIE, 16, 480, cols=[VERT, ROUGE, ENCRE], graine=17)
            tampon(c, "VÉRIFIÉ", CX, 1250, t, T_VERIFIE, 64, VERT, -7, "check")
        titre2(c, t, "PARCE QU'UN VRAI OUI", "C'EST UN OUI", T_PARCE - 0.05, T_VERIFIE - 0.1, t2=T_VRAI - 0.08)
        titre2(c, t, None, "QUE L'ON A VÉRIFIÉ", T_VERIFIE - 0.1, T_FIN - 0.05, t2=T_VERIFIE - 0.08, c2=VERT, e2="ressort")


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8); son(0.2, "whoosh_long", -12)
for k, tk in enumerate((T_OUI1, T_OUI2, T_OUI3)):
    son(tk - 0.04, "pop", -9); son(tk + 0.05, "check", -8); son(tk + 0.07, "ching", -13)
for k in range(3): son(T_LA + 0.12 * k, "croc", -10)
son(T_INQ - 0.35, "tampon", -6); son(T_INQ, "impact_doux", -8)
son(T_CAR - 0.12, "whoosh", -9); son(T_UNOUI - 0.12, "whoosh_court", -10); son(T_UNOUI, "impact_doux", -9)
son(T_ENGAG - 0.35, "whoosh_court", -10); son(T_ENGAG - 0.2, "montee", -14); son(T_NEST + 0.1, "croc", -6); son(T_NEST + 0.15, "impact", -8)
son(T_CEST1 - 0.12, "swipe", -9); son(T_FACON - 0.1, "pop", -10); son(T_NON - 0.3, "whoosh_long", -9); son(T_NON + 0.3, "impact", -5); son(T_NON + 0.32, "verre", -10)
son(T_ECH - 0.12, "whoosh_bas", -8); son(T_ECH - 0.05, "impact_doux", -9); son(T_PARFAIT - 0.05, "check", -8); son(T_PARFAIT, "ching", -11)
son(T_PROD - 0.1, "whoosh_court", -9); son(T_PROD, "impact_doux", -9); son(T_DIFF - 0.05, "croc", -7); son(T_DIFF, "tampon", -8)
son(T_ACOMPTE - 0.12, "whoosh", -9); son(T_VERSE - 0.1, "montee", -13); son(T_VERSE + 0.3, "check", -8); son(T_VERSE + 0.32, "ching", -11)
son(T_ETR - 0.1, "whoosh_bas", -9); son(T_ETR, "message", -12); son(T_REP, "message", -12)
for i in range(8): son(T_REP + 0.25 + i * 0.18, "tick", -18)
son(T_ATTENDRE - 0.1, "pop", -11)
son(T_A - 0.12, "whoosh_long", -8); son(T_MILLIERS - 0.2, "montee", -12); son(T_KM - 0.1, "ding", -12); son(T_AUCUN - 0.1, "pop", -9); son(T_VERIF - 0.25, "tampon", -9)
son(T_ALORS - 0.1, "whoosh_court", -10); son(T_QUI - 0.1, "impact_doux", -8)
son(T_CEST - 0.1, "whoosh_bas", -7); son(T_GSX - 0.1, "montee", -11); son(T_GSX, "impact", -4); son(T_GSX + 0.05, "ching", -9)
son(T_NOUS - 0.15, "whoosh", -8)
for tk, _, _, _, _, _ in ETAPES: son(tk - 0.15, "whoosh_court", -9); son(tk, "impact_doux", -9)
son(T_VERIFIONS - 0.05, "pop", -9); son(T_VERIFIONS + 0.3, "check", -9); son(T_AVANT - 0.1, "pop", -11)
son(T_NOM - 0.1, "pop", -10)
for tk in (T_COMPR, T_RESP): son(tk - 0.1, "pop", -10); son(tk, "check", -9)
son(T_EXIG - 0.1, "pop", -11)
son(T_PARCE - 0.12, "swipe", -9); son(T_PARCE, "impact_doux", -9); son(T_OUIV - 0.05, "swipe", -11)
son(T_VERIFIE - 0.1, "whoosh_court", -9); son(T_VERIFIE, "impact", -5); son(T_VERIFIE + 0.03, "ching", -9); son(T_VERIFIE, "tampon", -7)
sons_signature(son, T_FIN)
for tl in (T_L1, T_L2): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_LA - 0.1, T_LA + 0.3), (T_CAR - 0.15, T_CAR + 0.25), (T_NEST + 0.05, T_NEST + 0.4), (T_CEST1 - 0.15, T_CEST1 + 0.25),
             (T_NON - 0.3, T_NON + 0.45), (T_ECH - 0.15, T_ECH + 0.25), (T_PROD - 0.15, T_PROD + 0.25), (T_ACOMPTE - 0.15, T_ACOMPTE + 0.25),
             (T_ETR - 0.15, T_ETR + 0.25), (T_A - 0.15, T_A + 0.25), (T_NOUS - 0.15, T_NOUS + 0.25), (T_NEGO - 0.15, T_NEGO + 0.25),
             (T_SUIV - 0.15, T_SUIV + 0.25), (T_PARCE - 0.15, T_PARCE + 0.25), (T_VERIFIE - 0.1, T_VERIFIE + 0.3), (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_INQ - 0.35, ROUGE, 0.06), (T_NEST + 0.15, ROUGE, 0.06), (T_NON + 0.3, ROUGE, 0.08), (T_DIFF, ROUGE, 0.06),
                    (T_GSX, "#FFFFFF", 0.12), (T_VERIFIE, VERT, 0.07)]:
    eclair(tt, cc_, a_)


SIGN_MEDIAS = [(n, True) for n in RUSHES]


def dessine(c, t):
    gsx.T_COURANT[0] = t
    fond_clair(c, t)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_engagement(c, t); scene_poli(c, t); scene_echantillon(c, t); scene_acompte(c, t); scene_distance(c, t)
    r = disque_gsx(c, t, T_CEST, T_GSX, T_NOUS, avant="C'EST LÀ QUE")
    with Balance(c, t, 0.8):
        if r < 2100:
            scene_gsx_actions(c, t); scene_vrai_oui(c, t)
    entete(c, t, T_NOUS - 0.05, T_FIN)
    signature_gsx(c, t, T_FIN, SIGN_MEDIAS, [("Ne vous contentez pas d'un oui.", T_L1, 50, ENCRE),
                                               ("Exigez un partenaire.", T_L2, 50, ROUGE)], cy=860)
    K.dessine_eclairs(c, t)
    cache = (T_CEST - 0.1 < t < T_NOUS - 0.05) or t > T_FIN - 0.1
    if not cache: SOUS.dessine(c, t, ENCRE)
