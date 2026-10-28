"""GSX-M06 « Vous pensez acheter à une usine. Vous achetez à quelqu'un qui achète à l'usine. » — hook écrit par nous
(20/10/2026). Levier : confusion volontaire + révélation (la carte « usine » se retourne : c'est un bureau), puis la chaîne
Vous → intermédiaire → vraie usine, la marge cachée, le contact impossible, personne de responsable, « à qui parlez-vous ? ».
Persona : importateur francophone qui croit traiter « en direct » avec un fabricant trouvé en ligne.
Même forme que GSX-M01 → M04 (moteur/gsx.py) + carte recto/verso en 3D, chaîne animée avec flèches et étiquette
« + marge », faux tampon « FABRICANT », lien direct rétabli par GSX dans la langue et les codes, signature explosive.
Aucun chiffre, aucune promesse. Zone sûre TikTok / Snap : x 130-860, axe CX = 510."""
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
T_PENSEZ, T_USINE0, T_VOUS2, T_QUELQUN, T_ACHETE, T_LUSINE = TW(1), TW(5), TW(6), TW(9), TW(11), TW(13)
T_DERR, T_PHOTO, T_ATELIER, T_ILYA, T_BUREAU = TW(14), TW(17), TW(19), TW(20), TW(25)
T_UN, T_INTERM, T_COMMANDE, T_VRAIE, T_USINE2, T_PREND, T_MARGE = TW(26), TW(27), TW(29), TW(32), TW(33), TW(34), TW(36)
T_REVEND, T_SOUS, T_NOM, T_FABRICANT = TW(39), TW(42), TW(44), TW(46)
T_PAYEZ, T_CHER, T_SANS, T_SAVOIR = TW(47), TW(50), TW(51), TW(53)
T_PARLEZ, T_JAMAIS, T_CEUX, T_PRODUISENT = TW(54), TW(57), TW(59), TW(61)
T_ET, T_QUALITE, T_PASLA, T_PERSONNE, T_RESP = TW(62), TW(67), TW(70), TW(71), TW(73)
T_ALORS, T_POSEZ, T_QUESTION, T_SAVEZ, T_VRAIMENT, T_QUI, T_PARLEZ2 = TW(74), TW(75), TW(78), TW(79), TW(80), TW(82), TW(84)
T_CEST, T_GSX, T_INTERV = TW(85), TW(88), TW(89)
T_NOUS, T_IDENT, T_VERIT, T_FAB2 = TW(90), TW(91), TW(93), TW(94)
T_EVAL, T_CAPA = TW(96), TW(98)
T_NEGO, T_DIRECT, T_EUX, T_LANGUE, T_CODES = TW(101), TW(102), TW(104), TW(107), TW(111)
T_SAVEZ2, T_ENFIN, T_QUIP, T_OU, T_COND = TW(113), TW(114), TW(115), TW(117), TW(121)
T_FIN, T_L1, T_L2 = TW(122), TW(123), TW(129)

RUSHES = ["rushes/chaine-electronique", "rushes/atelier-valises", "rushes/cartons-ouvrieres", "rushes/presses-jaunes",
          "rushes/entrepot-bleu", "rushes/tissu-machine"]
HANZI = ["关", "系", "面", "子", "谈", "判", "信", "任", "价", "格"]


# ─────────────────────────────────────────── briques locales
def face_bureau(c, w, h):
    """le dos de la carte « usine » : un bureau commercial, pas d'atelier"""
    verre_clair(c, 0, 0, w, h, w * 0.08, 1.0, 1.0, ROUGE)
    rrect(c, w * 0.08, h * 0.1, w * 0.84, h * 0.5, w * 0.05, "#EEF1F6")
    # une table, un écran, une chaise : le bureau
    rrect(c, w * 0.2, h * 0.42, w * 0.6, h * 0.04, 6, "#C4CAD4")
    rrect(c, w * 0.3, h * 0.22, w * 0.4, h * 0.18, 10, ENCRE); rrect(c, w * 0.32, h * 0.24, w * 0.36, h * 0.14, 6, "#9AA8BF")
    rrect(c, w * 0.47, h * 0.4, w * 0.06, h * 0.03, 3, ENCRE)
    icone(c, "briefcase", w * 0.17, h * 0.32, w * 0.12, ROUGE, 2.4)
    icone(c, "phone", w * 0.83, h * 0.32, w * 0.1, ROUGE, 2.4)
    texte(c, "BUREAU", w / 2, h * 0.66, ajuste("BUREAU", w * 0.8, w * 0.16, "archivo", -0.02), ROUGE, "archivo", "centre", -0.02)
    texte(c, "commercial", w / 2, h * 0.66 + w * 0.18, w * 0.08, GRIS, "demi", "centre", 0)
    balayage(c, 0, 0, w, h, T_COURANT[0], w * 0.08, 0.4, 0.35)


def carte_acteur(ic, lab, sous=None, accent=ENCRE, rush=None, t0=0.0):
    """carte d'un acteur de la chaîne : tuile ou rush en haut, nom en bas"""
    def f(c, w, h):
        verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 0.8, accent)
        if rush:
            m = w * 0.06
            video(c, rush, m, m, w - 2 * m, h * 0.56, T_COURANT[0] - t0, 1.0, True, rayon=w * 0.06)
        else:
            tuile_v(c, ic, w / 2, h * 0.3, w * 0.4, accent)
        lw = ajuste(lab, w * 0.86, w * 0.13, "archivo", -0.02)
        texte(c, lab, w / 2, h * 0.68, lw, ENCRE, "archivo", "centre", -0.02)
        if sous: texte(c, sous, w / 2, h * 0.68 + lw * 1.3, ajuste(sous, w * 0.86, w * 0.075, "demi", 0), GRIS, "demi", "centre", 0)
        balayage(c, 0, 0, w, h, T_COURANT[0], w * 0.1, 0.4, 0.4)
    return f


def fleche(c, xa, xb, y, u, couleur=ROUGE, label=None, t=0.0, haut=True):
    """flèche en pointillés qui avance de xa vers xb ; étiquette au milieu"""
    if u <= 0.01: return
    pe = peinture(couleur, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=7); pe.setStrokeCap(skia.Paint.kRound_Cap)
    pe.setPathEffect(skia.DashPathEffect.Make([16, 12], -t * 90 * (1 if xb > xa else -1)))
    xe = mix(xa, xb, min(u, 1))
    c.drawLine(xa, y, xe, y, pe)
    d = 1 if xb > xa else -1
    pth = skia.Path(); pth.moveTo(xe + 16 * d, y); pth.lineTo(xe - 10 * d, y - 16); pth.lineTo(xe - 10 * d, y + 16); pth.close()
    c.drawPath(pth, peinture(couleur))
    if label and u > 0.6:
        pill_v(c, label, (xa + xb) / 2, y + (-54 if haut else 54), borne((u - 0.6) * 3), None, couleur, taille=24, plein=True)


# ─────────────────────────────────────────── 1 · hook : vous pensez acheter à une usine… (la carte se retourne)
def scene_hook(c, t):
    t1 = T_DERR - 0.12
    g = Groupe(c, t, -1, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        o = prog(t, -0.3, 1.4, douce)
        flip = prog(t, T_QUELQUN - 0.25, 0.65, entreeSortie)
        ay = mix(0, 180, flip) + 8 * math.sin(t * 1.2) * (1 - flip)
        sx, sy = secousse(t, T_QUELQUN + 0.4, 14, 0.3)
        cam = Cam(ax=-12 + 3 * math.sin(t * 0.9), ay=mix(-20, 6, o) + 4 * math.sin(t * 0.7), tz=mix(200, 0, prog(t, -0.3, 0.8, sortie)), cx=CX + sx, cy=1000 + sy)
        CW, CH = 440, 640
        rec = prog(t, T_ACHETE - 0.15, 0.6, entreeSortie)          # « qui achète à l'usine » : la vraie usine apparaît derrière, plus loin
        plans = [Plan(coins((mix(0, -120, rec), 0, 0), CW, CH, ay=ay + mix(0, 14, rec)), CW, CH,
                      carte_rush("rushes/chaine-electronique", -0.3, label="Prix direct usine", ic="factory"), 1.0),
                 Plan(coins((mix(0, -120, rec), 0, 0), CW, CH, ay=ay + 180 + mix(0, 14, rec)), CW, CH, face_bureau, 1.0)]
        if rec > 0:
            plans.append(Plan(coins((mix(600, 300, rec), -60, mix(1800, 700, rec)), CW, CH, ay=-22), CW, CH,
                              carte_rush("rushes/presses-jaunes", T_ACHETE - 0.4, label="La vraie usine", ic="factory", accent=ENCRE), borne(rec * 2)))
        scene3d(c, cam, plans)
        if rec > 0.2:
            fleche(c, CX + 110, CX + 300, 1120, prog(t, T_ACHETE, 0.5, entreeSortie), ROUGE, None, t)
        if t > T_QUELQUN + 0.35:
            onde(c, CX, 1000, t, T_QUELQUN + 0.4, 80, 560, ROUGE, 8, 0.6)
            eclats(c, CX, 1000, t, T_QUELQUN + 0.4, 14, 420, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=12)
        pill_v(c, "Quelqu'un", CX - 120, 1330, entre(t, T_QUELQUN + 0.3, 0.4, 2.2), "user", plein=True, rot=-2)
        titre2(c, t, "VOUS PENSEZ ACHETER", "À UNE USINE", -0.6, T_VOUS2 - 0.08, t2=-0.45)
        titre2(c, t, "VOUS ACHETEZ À QUELQU'UN", "QUI ACHÈTE À L'USINE", T_VOUS2 - 0.08, t1, t2=T_QUELQUN - 0.08, c2=ROUGE, e1="ressort")


# ─────────────────────────────────────────── 2 · derrière la belle photo de l'atelier, souvent un bureau
def scene_photo(c, t):
    t0, t1 = T_DERR - 0.12, T_UN - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        ouv = prog(t, T_ILYA - 0.1, 0.6, entreeSortie)             # la photo glisse, le bureau est derrière
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-14, 10, ouv) + 4 * math.sin(t * 0.8), cx=CX, cy=1000)
        CW, CH = 400, 560
        plans = [Plan(coins((mix(0, -230, ouv), mix(0, -40, ouv), mix(0, -120, ouv)), CW, CH, ay=mix(0, 26, ouv), az=mix(0, -5, ouv)), CW, CH,
                      carte_rush("rushes/atelier-valises", T_DERR - 0.3, label="La belle photo", ic="image"), borne(a * 3)),
                 Plan(coins((mix(0, 190, ouv), mix(0, 30, ouv), mix(420, 160, ouv)), CW, CH, ay=mix(0, -16, ouv)), CW, CH, face_bureau, borne(a * 3) * mix(0.35, 1, ouv))]
        scene3d(c, cam, plans)
        b = entre(t, T_BUREAU - 0.1, 0.4, 2.4)
        if b > 0:
            onde(c, CX + 190, 1000, t, T_BUREAU - 0.05, 60, 420, ROUGE, 7, 0.55)
            eclats(c, CX + 190, 1000, t, T_BUREAU - 0.05, 10, 320, cols=[ROUGE, ENCRE], graine=7)
        pill_v(c, "Souvent", CX + 190, 1330, entre(t, TW(23) - 0.1, 0.4, 2.2), "eye", taille=28)
        titre2(c, t, "DERRIÈRE LA BELLE PHOTO", "DE L'ATELIER", T_DERR - 0.05, T_ILYA - 0.1, t2=T_PHOTO - 0.1)
        titre2(c, t, "IL Y A SOUVENT", "UN BUREAU", T_ILYA - 0.1, t1, t2=T_BUREAU - 0.1, c2=ROUGE, e1="ressort")


# ─────────────────────────────────────────── 3 · la chaîne : vous → intermédiaire → vraie usine ; la marge ; « fabricant »
def scene_chaine(c, t):
    t0, t1 = T_UN - 0.12, T_PAYEZ - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        cam = Cam(ax=-8 + 2 * math.sin(t), ay=4 * math.sin(t * 0.8), tz=mix(200, 0, a), cx=CX, cy=980)
        CW, CH = 230, 330
        ui = prog(t, T_INTERM - 0.12, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_INTERM - 0.12 else 0.0
        uu = prog(t, T_VRAIE - 0.12, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_VRAIE - 0.12 else 0.0
        plans = [Plan(coins((-300, 0, 0), CW, CH, ay=14), CW, CH, carte_acteur("user", "Vous", "l'acheteur", ENCRE), borne(a * 3))]
        if ui > 0:
            sx, sy = secousse(t, T_FABRICANT, 10, 0.3)
            plans.append(Plan(coins((sx, sy, mix(1200, 0, min(ui, 1.05))), CW, CH), CW, CH, carte_acteur("briefcase", "Intermédiaire", "le bureau", ROUGE), borne(ui * 3)))
        if uu > 0:
            plans.append(Plan(coins((300, 0, mix(1200, 0, min(uu, 1.05))), CW, CH, ay=-14), CW, CH,
                              carte_acteur(None, "Vraie usine", "ceux qui produisent", ENCRE, "rushes/presses-jaunes", T_VRAIE - 0.4), borne(uu * 3)))
        scene3d(c, cam, plans)
        y = 980
        fleche(c, CX + 120, CX + 180, y, prog(t, T_COMMANDE - 0.05, 0.45, entreeSortie), ROUGE, "Commande", t, haut=True)
        fleche(c, CX - 120, CX - 180, y + 40, prog(t, T_REVEND - 0.05, 0.45, entreeSortie), ROUGE, "Revend", t, haut=False)
        m = entre(t, T_PREND - 0.1, 0.45, 2.2)
        if m > 0:                                                    # « prend sa marge » : l'étiquette rouge qui grossit sur l'intermédiaire
            c.save(); c.translate(CX + 90, 760); c.rotate(-10 + 3 * math.sin(t * 2)); s = mix(0.3, 1, m) * (1 + 0.25 * prog(t, T_MARGE - 0.05, 0.4, sortie)); c.scale(s, s)
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-96, -48, 192, 96), 24, 24)
            p = skia.Paint(AntiAlias=True, Color=hexa(ROUGE, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
            c.save(); c.translate(0, 12); c.drawRRect(rr, p); c.restore()
            c.drawRRect(rr, pgrad_(-96, -48, 96, 48, [ROUGE, "#A80020"]))
            texte(c, "+ MARGE", 0, -hauteurLigne(38, "archivo") / 2, 38, BLANC, "archivo", "centre", 0)
            c.restore()
            if t > T_MARGE - 0.05: eclats(c, CX + 90, 760, t, T_MARGE - 0.05, 10, 260, cols=[ROUGE, ENCRE], graine=9, duree=0.6)
        if t > T_FABRICANT - 0.12:                                   # « sous le nom de fabricant » : le faux tampon claque sur l'intermédiaire
            tampon(c, "FABRICANT", CX, 1210, t, T_FABRICANT - 0.08, 54, ROUGE, -8, "factory")
            eclats(c, CX, 1210, t, T_FABRICANT, 12, 320, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=11)
        titre2(c, t, "UN INTERMÉDIAIRE", "QUI COMMANDE À LA VRAIE USINE", T_UN - 0.05, T_PREND - 0.1, t2=T_INTERM - 0.08)
        titre2(c, t, "PREND SA MARGE", "ET VOUS REVEND LE TOUT", T_PREND - 0.1, T_SOUS - 0.1, t2=T_MARGE - 0.1, c2=ROUGE, e1="ressort")
        titre2(c, t, "SOUS LE NOM", "DE FABRICANT", T_SOUS - 0.1, t1, t2=T_FABRICANT - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 4 · vous payez plus cher sans le savoir
def scene_cher(c, t):
    t0, t1 = T_PAYEZ - 0.12, T_PARLEZ - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        c.save(); c.translate(CX, 980); c.rotate(-2 + 2 * math.sin(t * 1.3)); s = mix(0.4, 1, a); c.scale(s, s)
        with Calque(c, borne(a * 3)):
            verre_clair(c, -330, -290, 660, 580, 48, 1.0, 0.8)
            texte(c, "Ce que vous payez", -270, -250, 30, GRIS, "titre", track=-0.01)
            base, x, w = 230, -150, 300
            h1 = 300
            rrect(c, x, base - h1, w, h1, 18, ENCRE)
            texte(c, "Prix usine", x + w / 2, base - h1 / 2 - hauteurLigne(32, "archivo") / 2, 32, BLANC, "archivo", "centre", -0.02)
            m = prog(t, T_CHER - 0.1, 0.6, lambda v: ressort(v, 1.3, 4.6)) if t > T_CHER - 0.1 else 0.0
            if m > 0:
                h2 = 150 * min(m, 1.08)
                rrect(c, x, base - h1 - h2, w, h2, 18, ROUGE)
                texte(c, "Marge cachée", x + w / 2, base - h1 - h2 / 2 - hauteurLigne(28, "archivo") / 2, 28, BLANC, "archivo", "centre", -0.02, borne(m * 2))
                trait(c, x + w + 30, base - h1, x + w + 30, base - h1 - h2, ROUGE, 6)
                icone(c, "trending-up", x + w + 70, base - h1 - h2 / 2, 48, ROUGE, 2.8)
            so = entre(t, T_SANS - 0.1, 0.45, 2.2)
            if so > 0:
                c.save(); c.translate(230, -180); c.scale(so, so)
                disque(c, 0, 0, 60, BLANC, 1, (8, 20, 0.22)); anneau(c, 0, 0, 60, "#D5DAE3", 3); icone(c, "eye-off", 0, 0, 62, ROUGE, 2.6)
                c.restore()
        c.restore()
        if t > T_CHER + 0.3: eclats(c, CX, 760, t, T_CHER + 0.3, 10, 300, cols=[ROUGE, ENCRE], graine=13, duree=0.6)
        pill_v(c, "Sans le savoir", CX, 1330, entre(t, T_SAVOIR - 0.25, 0.4, 2.2), "eye-off", plein=True, rot=-2)
        titre2(c, t, "VOUS PAYEZ", "PLUS CHER", T_PAYEZ - 0.05, T_SANS - 0.1, t2=T_CHER - 0.1, c2=ROUGE)
        titre2(c, t, None, "SANS LE SAVOIR", T_SANS - 0.1, t1, t2=T_SANS - 0.08, e2="ressort")


# ─────────────────────────────────────────── 5 · vous ne parlez jamais à ceux qui produisent (le lien direct, barré)
def scene_contact(c, t):
    t0, t1 = T_PARLEZ - 0.12, T_ET - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="zoom", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), cx=CX, cy=1000)
        CW, CH = 300, 460
        u2 = prog(t, T_CEUX - 0.12, 0.5, lambda v: ressort(v, 1.3, 4.8)) if t > T_CEUX - 0.12 else 0.0
        plans = [Plan(coins((-200, 0, 0), CW, CH, ay=14), CW, CH, carte_acteur("user", "Vous", None, ENCRE), borne(a * 3))]
        if u2 > 0:
            plans.append(Plan(coins((200, 0, mix(1300, 0, min(u2, 1.05))), CW, CH, ay=-14), CW, CH,
                              carte_rush("rushes/cartons-ouvrieres", T_CEUX - 0.3, label="Ceux qui produisent", ic="users"), borne(u2 * 3)))
        scene3d(c, cam, plans)
        j = entre(t, T_JAMAIS - 0.1, 0.45, 2.2)
        if j > 0:
            lien(c, t, CX - 60, CX + 60, 1000, T_JAMAIS - 0.1, casse=T_JAMAIS + 0.25)
            c.save(); c.translate(CX, 1000); c.scale(min(j, 1.1), min(j, 1.1))
            disque(c, 0, 0, 62, ROUGE, 1, (10, 26, 0.25)); icone(c, "message-circle-x", 0, 0, 66, BLANC, 2.6)
            c.restore()
            if t > T_JAMAIS + 0.25: eclats(c, CX, 1000, t, T_JAMAIS + 0.25, 10, 300, cols=[ROUGE, ENCRE], graine=8, duree=0.6)
        pill_v(c, "Jamais", CX, 1330, entre(t, T_JAMAIS - 0.05, 0.4, 2.2), "ban", plein=True, rot=-3)
        titre2(c, t, "VOUS NE PARLEZ JAMAIS", "À CEUX QUI PRODUISENT", T_PARLEZ - 0.05, t1, t2=T_CEUX - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── 6 · le jour où la qualité n'est pas là, personne n'est responsable
def scene_personne(c, t):
    t0, t1 = T_ET - 0.12, T_ALORS - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="haut", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), cx=CX, cy=1000)
        CW, CH = 280, 400
        def colis(cc, w, h):
            carte_rush("rushes/entrepot-colis", T_ET - 0.3, label="Votre commande", ic="package")(cc, w, h)
            d = prog(t, T_PASLA - 0.05, 0.4, sortie)
            if d > 0:
                cc.save(); cc.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(w * 0.045, w * 0.045, w * 0.91, h - w * 0.09), w * 0.055, w * 0.055), True)
                cc.drawRect(skia.Rect.MakeWH(w, h), peinture("#6B7280", 0.45 * d))
                cc.restore()
        plans = [Plan(coins((0, -60, 0), CW, CH), CW, CH, colis, borne(a * 3))]
        scene3d(c, cam, plans)
        q = entre(t, T_PASLA - 0.05, 0.4, 2.4)
        if q > 0:
            croix_v(c, CX + 130, 760, 48, q)
            eclats(c, CX + 130, 760, t, T_PASLA, 10, 280, cols=[ROUGE, GRIS, ENCRE], graine=14)
        # les deux acteurs se renvoient la balle : « pas moi »
        p = entre(t, T_PERSONNE - 0.1, 0.45, 2.0)
        if p > 0:
            for k, (x, lab, ic) in enumerate(((-250, "Intermédiaire", "briefcase"), (250, "Usine", "factory"))):
                c.save(); c.translate(CX + x, 1250); s = mix(0.3, 1, p); c.scale(s, s); c.rotate((-1) ** k * 4 * math.sin(t * 2.5))
                with Calque(c, borne(p * 3)):
                    verre_clair(c, -130, -70, 260, 140, 40, 1.0, 0.8, ROUGE)
                    tuile_v(c, ic, -75, 0, 70, "#A9AFBA")
                    texte(c, lab, -22, -hauteurLigne(26, "archivo") / 2, ajuste(lab, 150, 26, "archivo", -0.02), ENCRE, "archivo", track=-0.02)
                c.restore()
                bulle = entre(t, T_PERSONNE + 0.1 + 0.15 * k, 0.35, 2.2)
                if bulle > 0:
                    c.save(); c.translate(CX + x + (60 if k == 0 else -60), 1140); c.scale(bulle, bulle)
                    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -36, 160, 72), 30, 30); c.drawRRect(rr, peinture(ENCRE))
                    texte(c, "Pas moi", 0, -hauteurLigne(28, "titre") / 2, 28, BLANC, "titre", "centre", -0.01)
                    c.restore()
            fleche(c, CX - 110, CX + 110, 1250, prog(t, T_PERSONNE + 0.1, 0.4, entreeSortie), "#9AA0AA", None, t)
            fleche(c, CX + 110, CX - 110, 1290, prog(t, T_PERSONNE + 0.25, 0.4, entreeSortie), "#9AA0AA", None, t)
        if t > T_RESP - 0.1: tampon(c, "PERSONNE", CX, 1000, t, T_RESP - 0.08, 64, ROUGE, -8, "x")
        titre2(c, t, "LE JOUR OÙ LA QUALITÉ", "N'EST PAS LÀ", T_ET - 0.05, T_PERSONNE - 0.1, t2=T_QUALITE - 0.1)
        titre2(c, t, "PERSONNE", "N'EST RESPONSABLE", T_PERSONNE - 0.1, t1, t2=T_PERSONNE - 0.08, c2=ROUGE, e1="ressort")


# ─────────────────────────────────────────── 7 · savez-vous vraiment à qui vous parlez ?
def scene_question(c, t):
    t0, t1 = T_ALORS - 0.12, T_CEST - 0.05
    g = Groupe(c, t, t0, t1, ent="bas", sor="aucune", d_in=0.4)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.55, 1.5)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-24, 8, prog(t, t0, t1 - t0, douce)) + 4 * math.sin(t * 0.8), tz=mix(300, 0, a), cx=CX, cy=1000)
        CW, CH = 380, 520
        def inconnu(cc, w, h):
            verre_clair(cc, 0, 0, w, h, w * 0.1, 1.0, 1.0, ROUGE)
            disque(cc, w / 2, h * 0.32, w * 0.2, "#E3E7EE"); icone(cc, "user", w / 2, h * 0.32, w * 0.22, GRIS, 2.4)
            q = entre(t, T_QUI - 0.05, 0.4, 2.4)
            if q > 0:
                cc.save(); cc.translate(w * 0.68, h * 0.2); cc.scale(q, q)
                disque(cc, 0, 0, w * 0.1, ROUGE); texte(cc, "?", 0, -hauteurLigne(w * 0.13, "archivo") / 2, w * 0.13, BLANC, "archivo", "centre", 0)
                cc.restore()
            for j in range(3):
                rrect(cc, w * 0.18, h * 0.6 + j * h * 0.08, w * [0.64, 0.5, 0.56][j], h * 0.035, 8, "#E3E7EE")
            balayage(cc, 0, 0, w, h, T_COURANT[0], w * 0.1, 0.4, 0.4)
        scene3d(c, cam, [Plan(coins((0, 0, 0), CW, CH, ay=6 * math.sin(t * 1.2)), CW, CH, inconnu, borne(a * 3))])
        if t > T_QUI - 0.05:
            onde(c, CX + 70, 820, t, T_QUI, 40, 300, ROUGE, 6, 0.6)
        pill_v(c, "Une seule question", CX, 1330, entre(t, T_QUESTION - 0.1, 0.4, 2.2) * (1 - prog(t, T_SAVEZ, 0.3)), "circle-help", taille=30)
        pill_v(c, "À qui parlez-vous ?", CX, 1330, entre(t, T_PARLEZ2 - 0.15, 0.4, 2.2), "message-circle", plein=True)
        titre2(c, t, "ALORS, POSEZ-VOUS", "UNE SEULE QUESTION", T_ALORS - 0.05, T_SAVEZ - 0.1, t2=T_POSEZ - 0.08)
        titre2(c, t, "SAVEZ-VOUS VRAIMENT", "À QUI VOUS PARLEZ ?", T_SAVEZ - 0.1, t1, t2=T_VRAIMENT - 0.08, c2=ROUGE, e1="ressort")


# ─────────────────────────────────────────── 8 · GSX : les vrais fabricants, leurs capacités, la négociation directe
def codes(c, t, cx, cy, a):
    """cadenas à molettes : les codes, cette fois ils se calent (GSX les connaît)"""
    w, h = 520, 150
    c.save(); c.translate(cx, cy); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
    with Calque(c, borne(a * 3)):
        verre_clair(c, -w / 2, -h / 2, w, h, 40, 1.0, 1.0, VERT)
        tuile_v(c, "lock-open", -w / 2 + 75, 0, 86, VERT)
        for j in range(4):
            x = -w / 2 + 160 + j * 86
            rrect(c, x, -52, 72, 104, 18, "#EEF1F6", 1, None, "#D5DAE3", 2)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, -52, 72, 104), 18, 18), True)
            cal = prog(t, T_CODES + 0.1 + 0.12 * j, 0.3, sortie)
            ph = (t * (5 + 1.7 * j) + j * 1.3) * (1 - cal)
            for d in (-1, 0, 1):
                ch = HANZI[(int(math.floor(ph)) + d + j * 3) % len(HANZI)] if cal < 1 else HANZI[(j * 3 + d) % len(HANZI)]
                yy = -26 + (d - (ph % 1)) * 70
                texte(c, ch, x + 36, yy, 48, (VERT if cal >= 1 else ENCRE) if d == 0 else GRIS, "cjk", "centre", 0)
            c.restore()
    c.restore()


def scene_gsx_direct(c, t):
    t0, t1 = T_NOUS - 0.1, T_SAVEZ2 - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        dir_ = prog(t, T_DIRECT - 0.15, 0.6, entreeSortie)         # « directement » : les fabricants reculent, Vous ↔ Usine se tendent
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.8), ay=mix(-10, 6, prog(t, t0, T_DIRECT - t0, douce)) * (1 - dir_) + 4 * math.sin(t * 0.7), cx=CX, cy=mix(980, 900, dir_))
        CW, CH = 240, 340
        plans = []
        FABS = [(T_IDENT, "rushes/chaine-electronique", -250, -40), (T_VERIT, "rushes/presses-jaunes", 0, 20), (T_FAB2, "rushes/tissu-machine", 250, -40)]
        for k, (tk, nom, x, y) in enumerate(FABS):
            u = prog(t, tk - 0.15, 0.5, lambda v: ressort(v, 1.3, 4.6)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            pos = (mix(x, x * 0.6, dir_), mix(y, -520, dir_), mix(1400, 0, min(u, 1.05)) + 700 * dir_)
            lab = "Véritable fabricant" if k == 1 else None
            plans.append(Plan(coins(pos, CW, CH, ay=(1 - k) * 14), CW, CH, carte_rush(nom, tk - 0.3, label=lab if dir_ < 0.5 else None, ic="badge-check", accent=VERT), borne(u * 3) * (1 - 0.5 * dir_)))
        if dir_ > 0:
            CW2, CH2 = 300, 440
            plans.append(Plan(coins((mix(-900, -210, dir_), 0, 0), CW2, CH2, ay=14), CW2, CH2, carte_acteur("user", "Vous", None, ENCRE), borne(dir_ * 2)))
            plans.append(Plan(coins((mix(900, 210, dir_), 0, 0), CW2, CH2, ay=-14), CW2, CH2,
                              carte_rush("rushes/cartons-ouvrieres", T_DIRECT, label="La vraie usine", ic="factory", accent=ENCRE), borne(dir_ * 2)))
        scene3d(c, cam, plans)
        # évaluer leurs capacités : trois coches sur la carte du milieu
        ev = entre(t, T_EVAL - 0.1, 0.45, 2.0) * (1 - dir_)
        if ev > 0:
            for k, lab in enumerate(("Capacité", "Délais", "Qualité")):
                e = entre(t, T_EVAL - 0.1 + 0.15 * k, 0.4, 2.2) * ev
                pill_v(c, lab, CX - 220 + 220 * k, 1240, e, "check", VERT, taille=26, plein=True)
        bouclier(c, t, CX + 210, 690, T_VERIT - 0.05, VERT, marque=None, taille=0.75) if dir_ < 0.5 else None
        if dir_ > 0:
            lien(c, t, CX - 60, CX + 60, 900, T_DIRECT + 0.1, t_sigle=T_EUX - 0.1)
            la = entre(t, T_LANGUE - 0.1, 0.4, 2.2)
            if la > 0:
                c.save(); c.translate(CX + 150, 700); c.rotate(4 * math.sin(t * 2)); c.scale(la, la)
                verre_clair(c, -110, -48, 220, 96, 40, 1.0, 0.8, VERT)
                texte(c, "你好，谈判", 0, -hauteurLigne(36, "cjk") / 2, 36, ENCRE, "cjk", "centre", 0)
                c.restore()
            codes(c, t, CX, 1250, entre(t, T_CODES - 0.1, 0.45, 1.8))
        titre2(c, t, "NOUS IDENTIFIONS", "LES VÉRITABLES FABRICANTS", T_NOUS - 0.05, T_EVAL - 0.1, t2=T_VERIT - 0.08)
        titre2(c, t, "NOUS ÉVALUONS", "LEURS CAPACITÉS", T_EVAL - 0.1, T_NEGO - 0.1, t2=T_CAPA - 0.08, e1="ressort")
        titre2(c, t, "NOUS NÉGOCIONS", "DIRECTEMENT AVEC EUX", T_NEGO - 0.1, T_LANGUE - 0.12, t2=T_DIRECT - 0.08, c2=VERT)
        titre2(c, t, "DANS LEUR LANGUE", "SELON LEURS CODES", T_LANGUE - 0.12, t1, t2=T_LANGUE - 0.08, e1="ressort")


# ─────────────────────────────────────────── 9 · vous savez enfin qui produit, où, et à quelles conditions
SAVOIRS = [(T_QUIP, "factory", "Qui produit"), (T_OU, "map-pin", "Où"), (T_COND, "file-text", "À quelles conditions")]


def scene_enfin(c, t):
    t0, t1 = T_SAVEZ2 - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="droite", sor="recul", d_in=0.32, d_out=0.4)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.5)
        with Calque(c, borne(a * 3)):
            globe(c, 100 + 5 * t, 24, CX, 730, 105 * mix(0.6, 1, a), 1.0, 1.0, france=False)
        for k, (tk, ic, lab) in enumerate(SAVOIRS):
            rangee(c, t, CX, 900 + k * 170, 720, ic, lab, tk - 0.05, "ok", tk + 0.3, VERT)
        titre2(c, t, "VOUS SAVEZ ENFIN", "QUI PRODUIT", T_SAVEZ2 - 0.05, T_OU - 0.1, t2=T_QUIP - 0.1, c2=VERT)
        titre2(c, t, None, "OÙ", T_OU - 0.1, T_COND - 0.12, t2=T_OU - 0.08, c2=VERT, e2="ressort")
        titre2(c, t, "ET", "À QUELLES CONDITIONS", T_COND - 0.12, T_FIN - 0.05, t2=T_COND - 0.08, c2=VERT)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8); son(0.2, "whoosh_long", -12)
son(T_QUELQUN - 0.25, "whoosh_long", -9); son(T_QUELQUN + 0.4, "impact", -5); son(T_QUELQUN + 0.42, "verre", -10); son(T_QUELQUN + 0.3, "tampon", -9)
son(T_ACHETE - 0.15, "whoosh_court", -10); son(T_ACHETE, "impact_doux", -9); son(T_ACHETE + 0.2, "montee", -14)
son(T_DERR - 0.12, "whoosh", -9); son(T_DERR, "impact_doux", -9); son(T_ILYA - 0.1, "swipe", -9); son(T_BUREAU - 0.05, "impact", -7); son(T_BUREAU, "croc", -9)
son(T_UN - 0.12, "swipe", -9); son(T_INTERM - 0.12, "whoosh_court", -10); son(T_INTERM, "impact_doux", -9)
son(T_COMMANDE - 0.05, "montee", -14); son(T_VRAIE - 0.12, "whoosh_court", -10); son(T_VRAIE, "impact_doux", -9)
son(T_PREND - 0.1, "pop", -9); son(T_MARGE - 0.05, "impact_doux", -8); son(T_MARGE, "ching", -11)
son(T_REVEND - 0.05, "montee", -14); son(T_FABRICANT - 0.08, "tampon", -5); son(T_FABRICANT, "impact", -7)
son(T_PAYEZ - 0.12, "whoosh_bas", -8); son(T_CHER - 0.1, "montee", -12); son(T_CHER + 0.3, "impact", -7); son(T_SANS - 0.1, "pop", -10); son(T_SAVOIR - 0.25, "tampon", -9)
son(T_PARLEZ - 0.12, "whoosh", -9); son(T_CEUX - 0.12, "whoosh_court", -10); son(T_CEUX, "impact_doux", -9)
son(T_JAMAIS - 0.1, "montee", -14); son(T_JAMAIS + 0.25, "croc", -6); son(T_JAMAIS + 0.28, "impact", -8); son(T_JAMAIS - 0.05, "tampon", -9)
son(T_ET - 0.12, "whoosh_bas", -8); son(T_PASLA - 0.05, "croc", -7); son(T_PASLA, "tampon", -9)
son(T_PERSONNE - 0.1, "whoosh_court", -10); son(T_PERSONNE + 0.1, "pop", -10); son(T_PERSONNE + 0.25, "pop", -10); son(T_RESP - 0.08, "tampon", -5)
son(T_ALORS - 0.12, "whoosh", -9); son(T_QUESTION - 0.1, "pop", -10); son(T_QUI - 0.05, "impact_doux", -8); son(T_PARLEZ2 - 0.15, "pop", -9)
son(T_CEST - 0.1, "whoosh_bas", -7); son(T_GSX - 0.1, "montee", -11); son(T_GSX, "impact", -4); son(T_GSX + 0.05, "ching", -9)
son(T_NOUS - 0.15, "whoosh", -8)
for tk in (T_IDENT, T_VERIT, T_FAB2): son(tk - 0.15, "whoosh_court", -10); son(tk, "impact_doux", -10)
son(T_VERIT - 0.05, "pop", -9); son(T_VERIT + 0.3, "check", -9)
for k in range(3): son(T_EVAL - 0.1 + 0.15 * k, "pop", -11); son(T_EVAL + 0.15 * k, "check", -10)
son(T_DIRECT - 0.15, "whoosh_long", -8); son(T_DIRECT + 0.1, "montee", -13); son(T_EUX - 0.1, "impact_doux", -7); son(T_EUX - 0.05, "ching", -10)
son(T_LANGUE - 0.1, "pop", -9); son(T_CODES - 0.1, "pop", -10)
for j in range(4): son(T_CODES + 0.1 + 0.12 * j, "tick", -14); son(T_CODES + 0.4 + 0.12 * j, "check", -13)
son(T_SAVEZ2 - 0.12, "swipe", -9)
for tk, _, _ in SAVOIRS: son(tk - 0.17, "whoosh_court", -10); son(tk + 0.3, "check", -9)
sons_signature(son, T_FIN)
for tl in (T_L1, T_L2): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_QUELQUN - 0.25, T_QUELQUN + 0.5), (T_DERR - 0.15, T_DERR + 0.25), (T_ILYA - 0.1, T_ILYA + 0.3), (T_UN - 0.15, T_UN + 0.25),
             (T_FABRICANT - 0.1, T_FABRICANT + 0.3), (T_PAYEZ - 0.15, T_PAYEZ + 0.25), (T_PARLEZ - 0.15, T_PARLEZ + 0.25), (T_ET - 0.15, T_ET + 0.25),
             (T_ALORS - 0.15, T_ALORS + 0.25), (T_NOUS - 0.15, T_NOUS + 0.25), (T_DIRECT - 0.15, T_DIRECT + 0.3), (T_SAVEZ2 - 0.15, T_SAVEZ2 + 0.25),
             (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_QUELQUN + 0.4, ROUGE, 0.08), (T_BUREAU - 0.05, ROUGE, 0.06), (T_FABRICANT, ROUGE, 0.06), (T_JAMAIS + 0.25, ROUGE, 0.06),
                    (T_RESP - 0.08, ROUGE, 0.06), (T_GSX, "#FFFFFF", 0.12), (T_EUX - 0.1, VERT, 0.06)]:
    eclair(tt, cc_, a_)


SIGN_MEDIAS = [(n, True) for n in RUSHES]


def dessine(c, t):
    gsx.T_COURANT[0] = t
    fond_clair(c, t)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_photo(c, t); scene_chaine(c, t); scene_cher(c, t); scene_contact(c, t); scene_personne(c, t); scene_question(c, t)
    r = disque_gsx(c, t, T_CEST, T_GSX, T_NOUS, avant="C'EST LÀ QUE")
    with Balance(c, t, 0.8):
        if r < 2100:
            scene_gsx_direct(c, t); scene_enfin(c, t)
    entete(c, t, T_NOUS - 0.05, T_FIN)
    signature_gsx(c, t, T_FIN, SIGN_MEDIAS, [("Avant de chercher le bon prix,", T_L1, 48, ENCRE),
                                               ("trouvez la bonne porte.", T_L2, 50, ROUGE)], cy=860)
    K.dessine_eclairs(c, t)
    cache = (T_CEST - 0.1 < t < T_NOUS - 0.05) or t > T_FIN - 0.1
    if not cache: SOUS.dessine(c, t, ENCRE)
