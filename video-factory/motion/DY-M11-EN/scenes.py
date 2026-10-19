"""DY-M11-EN — VERSION ANGLAISE de DY-M11 « Pas besoin de l'avion » (v2 du 17/10 : « plusieurs qualités, selon les produits », plus de standard / 1:1 / originale) — DROP&YOU, sujet de DY-M02 au style CB-M15 (cobalt, débit validé), en 3D (17/10/2026).
Hook : une carte d'embarquement Paris → Guangzhou arrive en tournant, tampon PAS BESOIN, elle se déchire en deux ;
« On y est déjà » : épingle DROP&YOU plantée à Guangzhou sur un sol en perspective. Fin : le China Book (livre en volume,
« par DROP&YOU »). Corps commun : moteur/dy3d.py. Logo DROP&YOU en filigrane tout du long."""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from dy3d import *
import agence

K = Kit(P, 1.0)
DUREE = round(K.timing["mots"][-1]["t1"] + 1.8, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
I = lambda mot, apres=0: trouve(K, mot, apres)

import dy3d
dy3d.TR.update({"Sur place, en Chine": "On the ground, in China", "8 à 12 jours": "8 to 12 days", "Chine": "China", "Chez toi": "Your door",
                "Pour toi": "For you", "Pour revendre": "To resell", "On gère les deux": "We do both", "Virement": "Transfer", "Carte": "Card",
                "France": "France", "Belgique": "Belgium", "Partout": "Anywhere", "LIVRAISON": "DELIVERY", "COMPRISE": "INCLUDED",
                "À L'UNITÉ": "ONE PIECE", "OU EN QUANTITÉ": "OR IN BULK", "ÉCRIS-NOUS": "MESSAGE US"})

M = dict(dy=TW(I("drop")), place=TW(I("ground")), cat0=TW(I("a", 19)),
         items=[("veste", TW(I("jacket"))), ("casque", TW(I("headphones"))), ("moto", TW(I("motorbike")))],
         titre_cat=("SHOW US", "THE MODEL"), catalogue=TW(I("show")), tel=TW(I("model")),
         qual0=TW(I("and", 35)), q=[TW(I("several")), TW(I("quality")), TW(I("options"))],
         quals=[("Jacket", "", "veste"), ("Headphones", "", "casque"), ("Motorbike", "", "moto")],
         titre_qual=("DEPENDS ON THE PRODUCT", "SEVERAL QUALITIES"), t_titre2=TW(I("several")),
         livr=TW(I("delivery")), jours=TW(I("eight")),
         fr=TW(I("france")), be=TW(I("belgium")), partout=TW(I("anywhere")), unite=TW(I("one", 60)), quant=TW(I("bulk")),
         revendre=TW(I("resell")), paie=TW(I("paypal")), vir=TW(I("bank")), carte=TW(I("card")),
         ecris=TW(I("message")), snap=TW(I("snap")), dy1=TW(I("drop", 76)), wa=TW(I("whatsapp")), cb0=TW(I("and", 83)))
SOUS = SousTitresEncre(K, fusions={(I("drop", 76), I("drop", 76) + 1, I("drop", 76) + 2, I("drop", 76) + 3): "DropandYou1,",
                                   (I("china", 90), I("china", 90) + 1): "China Book."},
                       y=1440, larg=900, taille=54, fam="gras", max_mots=5)
T_AVION, T_CHINE, T_ON, T_DEJA, T_TOI, T_B1 = TW(3), TW(5), TW(6), TW(7), TW(9), M["dy"]
T_TRAITER, T_CB = TW(I("deal")), TW(I("china", 90))


def billet(moitie=None):
    """carte d'embarquement ; moitie = 'g' ou 'd' pour une moitié déchirée"""
    def f(c, w, h):
        W_ = w * (2 if moitie else 1)
        dx = -w if moitie == "d" else 0
        c.save(); c.clipRect(skia.Rect.MakeWH(w, h)); c.translate(dx, 0)
        rrect(c, 0, 0, W_, h, 30, "#FFFFFF")
        c.drawRoundRect(skia.Rect.MakeXYWH(0, 0, W_, 70), 30, 30, pgrad(0, 0, W_, 0, [ORANGE, "#E0560A"])); c.drawRect(skia.Rect.MakeXYWH(0, 40, W_, 30), pgrad(0, 0, W_, 0, [ORANGE, "#E0560A"]))
        texte(c, "BOARDING PASS", 30, 18, 30, BLANC, "noir", track=0.06)
        icone(c, "plane", W_ - 60, 35, 40, BLANC, 2.4)
        texte(c, "PARIS", 30, 100, 26, "#6B7280", "fort", track=0.04); texte(c, "CDG", 30, 128, 90, BLEU_CASE, "noir", track=-0.02)
        texte(c, "GUANGZHOU", W_ - 30, 100, 26, "#6B7280", "fort", "droite", 0.04); texte(c, "CAN", W_ - 30, 128, 90, BLEU_CASE, "noir", "droite", -0.02)
        icone(c, "plane-takeoff", W_ / 2, 175, 60, ORANGE, 2.4)
        for j, (lab, val) in enumerate([("FLIGHT", "DY 001"), ("GATE", "K12"), ("SEAT", "32A")]):
            texte(c, lab, 30 + j * W_ / 3, 245, 20, "#6B7280", "fort", track=0.06); texte(c, val, 30 + j * W_ / 3, 270, 34, BLEU_CASE, "noir", track=0)
        for j in range(26): rrect(c, W_ - 260 + j * 9, h - 20 - 0, 4 + 3 * (j % 3), -1, 0, BLEU_CASE)
        c.restore()
    return f


def hook(c, t):
    a = prog(t, -0.05, 0.55, lambda v: ressort(v, 1.3, 4.8))
    dech = prog(t, T_CHINE - 0.1, 0.6, entree)
    on = prog(t, T_ON - 0.15, 0.5, sortieExpo)
    cam = Cam(ax=mix(-8, -28, on) + 3 * math.sin(t), ay=mix(-60, -8, min(a, 1.1)) + 5 * math.sin(t * 0.8), tz=mix(600, 120, min(a, 1.1)) + 300 * on, cy=mix(980, 1060, on))
    W_, H_ = 840, 385
    plans = []
    if dech < 1:
        if t < T_CHINE - 0.1:
            plans.append(Plan(coins((0, -40, 0), W_, H_, ay=mix(-55, 0, min(a, 1.0)) + 6 * math.sin(t * 1.5), az=-4), W_, H_, billet()))
        else:
            for k, m in enumerate(("g", "d")):
                sgn = -1 if k == 0 else 1
                plans.append(Plan(coins((sgn * (W_ / 4 + 260 * dech), -40 + 900 * dech ** 1.6, 500 * dech), W_ / 2, H_, az=sgn * 40 * dech, ay=sgn * 50 * dech), W_ / 2, H_, billet(m), 1 - dech))
    if on > 0:
        sol(c, cam, t, y=300, alpha=0.45 * on, couleur="#5F7BFF")
    scene3d(c, cam, plans)
    st = entre(t, T_AVION - 0.12, 0.35, 2.6) * (1 - dech)
    if st > 0:
        tampon_n(c, "NO NEED", 560, 1000, t, T_AVION - 0.12, ROUGE, -12, 64)
    if on > 0:
        X, Y, Z = cam.proj((0, 300, 200))
        e = prog(t, T_ON - 0.1, 0.55, lambda v: ressort(v, 1.6, 5.0))
        yy = Y - 700 * (1 - min(e, 1.0))
        c.drawOval(skia.Rect.MakeXYWH(X - 110, Y - 22, 220, 44), peinture("#000000", 0.3 * on))
        for k in range(3):
            u = ((t - T_ON) * 0.9 + k / 3) % 1
            c.drawOval(skia.Rect.MakeXYWH(X - 110 - 300 * u, Y - 22 - 60 * u, 220 + 600 * u, 44 + 120 * u), peinture(ORANGE, 0.5 * (1 - u) * on, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        disque(c, X, yy - 150, 90, ORANGE); disque(c, X, yy - 150, 64, BLEU_CASE)
        iw, ih = taille_img(LOGO); lw = 100; image(c, LOGO, X - lw / 2, yy - 150 - lw * ih / iw / 2, lw)
        pth = skia.Path(); pth.moveTo(X - 78, yy - 110); pth.lineTo(X, yy); pth.lineTo(X + 78, yy - 110); pth.close(); c.drawPath(pth, peinture(ORANGE))
        puce(c, "Guangzhou", X - 250, yy - 150, entre(t, T_ON + 0.2, 0.4, 2.2), "map-pin", ORANGE, 38)
        p = entre(t, T_TOI - 0.1, 0.4, 2.2)
        if p > 0: etiquette_case(c, "For you", 780, 900, p, ORANGE, 48, "noir", BLEU_CASE)
    titre(c, t, "NO NEED", "TO FLY TO CHINA", -0.25, T_ON - 0.1, y=400, t2=TW(2))
    titre(c, t, "WE'RE ALREADY", "THERE", T_ON, T_B1 + 0.2, y=400, t2=TW(8))


def china_book(c, t):
    t0 = M["cb0"] - 0.15
    if t < t0 or t > DUREE - 1.3: return
    s = prog(t, DUREE - 1.6, 0.3, entree)
    a = prog(t, t0, 0.6, lambda v: ressort(v, 1.3, 4.6))
    with Calque(c, 1 - s):
        titre(c, t, "DEAL WITH THEM", "YOURSELF?", M["cb0"], DUREE - 1.4, y=400, t2=T_TRAITER + 0.2)
        cam = Cam(ax=-14 + 3 * math.sin(t), ay=mix(-120, -24, min(a, 1.05)) + 12 * math.sin(t * 0.9), tz=mix(1400, 220, min(a, 1.05)), cy=980)
        def couv(cc, w, h):
            cc.drawRoundRect(skia.Rect.MakeWH(w, h), 22, 22, pgrad(0, 0, w, h, ["#8A6BFF", "#6E48F0", "#4B2BA8"]))
            rrect(cc, 24, 24, w - 48, h - 48, 16, None, 1.0, None, "#FFFFFF", 3)
            texte(cc, "CHINA", w / 2, h * 0.32, 90, BLANC, "noir", "centre", -0.02)
            texte(cc, "BOOK", w / 2, h * 0.32 + 92, 90, ORANGE2, "noir", "centre", -0.02)
            texte(cc, "by DROP&YOU", w / 2, h * 0.78, 30, BLANC, "fort", "centre", 0.04)
        pages = aplat("#F5F1E8"); dos = aplat("#4B2BA8")
        plans = boite((0, 0, 0), 440, 600, 90, dict(avant=couv, arriere=dos, gauche=dos, droite=pages, haut=pages, bas=pages))
        scene3d(c, cam, plans)
        if t > T_CB - 0.1:
            eclats(c, 540, 980, t, T_CB, 16, 520, [ORANGE, BLANC, "#8A6BFF"], graine=7)
            puce(c, "Suppliers, direct", 540, 1310, entre(t, T_CB, 0.4, 2.2), "users", ORANGE, 36)


son(0.0, "whoosh_bas", -8); son(0.3, "impact_doux", -7); son(0.05, "pop", -11); son(TW(2) - 0.05, "pop", -11)
son(T_AVION - 0.12, "tampon", -5); son(T_AVION - 0.1, "impact", -6)
son(T_CHINE - 0.1, "croc", -7); son(T_CHINE, "whoosh", -9)
son(T_ON - 0.15, "whoosh_bas", -8); son(T_ON + 0.35, "impact", -5); son(T_ON + 0.4, "ching", -9); son(T_ON + 0.2, "pop", -11)
son(T_DEJA - 0.1, "pop", -10); son(T_TOI - 0.1, "check", -9)
sons_corps(K, M, DUREE)
son(M["cb0"] - 0.15, "whoosh_long", -8); son(M["cb0"] + 0.3, "impact_doux", -8); son(T_CB - 0.1, "montee", -11); son(T_CB, "ching", -9); son(T_CB + 0.2, "pop", -10)
for a, b in [(0.12, 0.4), (T_CHINE - 0.1, T_CHINE + 0.4), (T_ON - 0.15, T_ON + 0.4), (T_B1 - 0.35, T_B1 + 0.1), (M["cb0"] - 0.15, M["cb0"] + 0.4)]: rapide(a, b)
for tt, cc_, a_ in [(T_AVION - 0.1, "#FFFFFF", 0.14), (T_ON + 0.35, ORANGE, 0.1), (T_CB, ORANGE, 0.1), (DUREE - 1.3, "#FFFFFF", 0.14)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    agence.T_COURANT[0] = t
    compose(c, t, M, hook, T_B1, SOUS, K, DUREE, extra=china_book, pulse=battement(t, T_ON + 0.35, 1, 0.6) - 1)
