"""MQ-M04 = MQ-M02 (fond clair, préférée du client) avec ses retours du 16/10/2026 : développement en cartes verticales
(nuancier, fiche technique, prototypes), photo du studio pour « culture produit française ». Voix, rythme, son : ceux de MQ-M02.

MQ-M02 « Vous espérez ça. Vous recevez ça. » — MQ-M01 corrigée pour MONARQUE (15/10/2026).

Retours du client sur MQ-M01 : photo SHOP nette (fournie), un globe blanc sculpté à la place de la carte du monde
(photo de référence → globe_relief.py, vraie 3D), le manteau long en « vous espérez ça » et le court en « vous recevez
ça », un hook plus fort qui parle aux professionnels qui produisent déjà en Chine, débit de DA-M07-169-EN (voix Tomy
à 4,2 mots/s, pauses resserrées à 0,18 s). Niveau de motion : CB-M14 (titres lettre par lettre, médias en cases).
Charte du client : blanc cassé, noir, Archivo Black. Aucun chiffre inventé.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import agence
from studio import lettres, Groupe, eclats, entre, SousTitresEncre, curseur
from monarque import *
from monarque import VERT, ROUGE           # (kit exporte aussi des noms de couleurs)

polices(P)
K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.6, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresEncre(K, fusions={(120, 121, 122, 123): "monarqueprod.com."}, y=1440, larg=900, taille=54, fam="gras", max_mots=5)

LONG, COURT = "trench-long", "trench-court"
T_RECU = TW(3)
T_SCEN, T_ECH, T_PROD = TW(6), TW(15), TW(18)
T_INT, T_PERS = TW(26), TW(31)
T_MQ, T_FR, T_INST, T_CHINE = TW(38), TW(44), TW(45), TW(47)
T_BOUT, T_MARCHE = TW(48), TW(56)
T_DEV, T_MAT, T_PAT, T_PROTO = TW(57), TW(61), TW(62), TW(63)
T_USI, T_NEG = TW(64), TW(68)
T_PRIX, T_VOL, T_DEL = TW(71), TW(73), TW(75)
T_CTRL, T_ATEL, T_DEP = TW(76), TW(82), TW(83)
T_VAL, T_REC2 = TW(86), TW(90)
T_TEST, T_VEND, T_RELANCE = TW(95), TW(99), TW(104)
T_FRCN, T_PUIS = TW(107), TW(111)
T_FIN, T_URL = TW(115), TW(120)


# ─────────────────────────────────────────── 1 · hook : vous espérez ça / vous recevez ça
def hook(c, t):
    if t > T_SCEN + 0.4: return
    g = Groupe(c, t, -1, T_SCEN, ent="aucune", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        a1 = 1 - prog(t, T_RECU - 0.12, 0.2, entree)
        if a1 > 0:
            lettres(c, "VOUS ESPÉREZ ÇA", 540, 330, 96, t, -0.6, "ressort", fam="archivo", grad=False, couleur=ENCRE,
                    decal=0.03, track=-0.01, alpha=a1)
        lettres(c, "VOUS RECEVEZ ÇA", 540, 330, 96, t, T_RECU - 0.05, "ressort", fam="archivo", grad=False, couleur=ROUGE,
                decal=0.025, track=-0.01)
        # le long : grand au centre, puis rangé à gauche quand le court tombe
        d = prog(t, T_RECU - 0.15, 0.4, entreeSortie)
        cx = mix(540, 290, d); s = mix(1.32, 1.0, d)
        media(c, t, LONG, cx - 220, 600, 440, 720, 1.0, s, zoom=1.14 + 0.02 * t, fy=0.5, accent=VERT if d > 0.5 else None)
        pilule(c, "Espéré", cx, 1385, entre(t, T_RECU + 0.25, 0.4, 2.2), "check", VERT)
        # le court : tombe du haut et secoue
        if t >= T_RECU - 0.05:
            u = prog(t, T_RECU - 0.05, 0.3, entree)
            sh = secousse(t, T_RECU + 0.25, 16, 0.35)
            c.save(); c.translate(sh[0], sh[1] + mix(-1500, 0, u))
            media(c, t, COURT, 570, 600, 440, 720, 1.0, 1.0, zoom=1.12, fy=0.5, rot=mix(-12, 3, u), accent=ROUGE)
            c.restore()
            pilule(c, "Reçu", 790, 1385, entre(t, T_RECU + 0.4, 0.4, 2.2), "x", ROUGE)
            signe(c, "≠", 540, 960, entre(t, TW(5) - 0.05, 0.35, 2.6), ROUGE, 70, t, TW(5))
            tampon(c, "NON CONFORME", 790, 1120, t, TW(5) + 0.18, 44, ROUGE, -9)


# ─────────────────────────────────────────── 2 · le scénario : échantillon parfait, production qui ne lui ressemble plus
def scenario(c, t):
    g = Groupe(c, t, T_SCEN - 0.1, T_INT, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "PRODUIRE EN CHINE", T_SCEN, T_ECH - 0.1)
        titre(c, t, "PAS LA MÊME PIÈCE", T_ECH - 0.05, T_INT - 0.1, couleur=ROUGE)
        sw = prog(t, T_ECH - 0.2, 0.4, entreeSortie)
        # la carte de Chine du site, une usine qui pulse
        if sw < 1:
            with Calque(c, 1 - sw):
                a = entre(t, T_SCEN, 0.5, 1.4)
                c.save(); c.translate(540, 960); c.scale(mix(0.8, 1, a) * mix(1, 0.8, sw), mix(0.8, 1, a) * mix(1, 0.8, sw)); c.translate(-540, -960)
                cadre(c, 90, 600, 900, 720, 44)
                k = 860 / 1040; y0 = 600 + (720 - 833 * k) / 2
                image(c, "chine", 110, y0, 860)
                px, py = 110 + 650 * k, y0 + 660 * k
                onde(c, px, py, t, T_SCEN + 0.4, 20, 170, ROUGE, 6, 0.7)
                epingle(c, px, py, "Votre usine", entre(t, TW(10) - 0.1, 0.42, 2.0), ROUGE, "CN", 80)
                pilule(c, "Vous connaissez", 330, 1250, entre(t, TW(12) - 0.1, 0.4, 2.2), "user", ENCRE, BLANC, 32, -3)
                c.restore()
        if sw > 0:
            a = entre(t, T_ECH - 0.1, 0.5, 1.5)
            media(c, t, LONG, 80, 620, 420, 640, borne(a * 3), mix(0.6, 1, a), zoom=2.4, fx=0.52, fy=0.36, accent=VERT)
            pilule(c, "Échantillon", 290, 1300, entre(t, T_ECH + 0.1, 0.4, 2.2), None, ENCRE)
            coche(c, 460, 650, 40, entre(t, TW(17) - 0.05, 0.35, 2.4))
            b = entre(t, T_PROD - 0.1, 0.5, 1.5)
            if b > 0:
                media(c, t, "rushes/trench", 580, 620, 420, 640, borne(b * 3), mix(0.6, 1, b), video_t0=T_PROD - 0.1, vitesse=1.2,
                      accent=ROUGE)
                pilule(c, "Production", 790, 1300, entre(t, T_PROD + 0.1, 0.4, 2.2), None, ENCRE)
                for k, (dx, dy) in enumerate([(-70, -120), (60, 40), (-30, 190)]):
                    q = prog(t, TW(24) - 0.05 + 0.1 * k, 0.3, lambda v: rebond(v, 2))
                    if q > 0: anneau(c, 790 + dx, 940 + dy, 50 * q, ROUGE, 7, borne(q * 2))
            signe(c, "≠", 540, 940, entre(t, TW(22) - 0.05, 0.35, 2.6), ROUGE, 66, t, TW(22))


# ─────────────────────────────────────────── 3 · intermédiaires, et personne sur place
CHAINE = [("Vous", "user"), ("Agent", "message-circle"), ("Grossiste", "building-2"), ("Usine", "factory")]


def intermediaires(c, t):
    g = Groupe(c, t, T_INT - 0.1, T_MQ, ent="bas", sor="aucune", cy=960)
    if not g.visible or t > T_MQ + 0.3: return
    with g:
        titre(c, t, "INTERMÉDIAIRES", T_INT, T_PERS - 0.1)
        titre(c, t, "PERSONNE SUR PLACE", T_PERS - 0.05, T_MQ - 0.1, couleur=ROUGE, taille=86)
        m = prog(t, T_PERS - 0.2, 0.45, entreeSortie)           # la chaîne se tasse, le rush arrive dessous
        for i, (lab, ic) in enumerate(CHAINE):
            a = entre(t, T_INT + 0.05 + 0.14 * i, 0.4, 1.8)
            if a <= 0: continue
            y = mix(600 + i * 175, 560 + i * 112, m); hh = mix(140, 96, m)
            x0 = 140 + (1 - a) * 300
            with Calque(c, borne(a * 3)):
                cadre(c, x0, y, 560, hh, hh / 2)
                disque(c, x0 + hh / 2, y + hh / 2, hh / 2 - 14, ENCRE if i in (0, 3) else "#E8E5E0")
                icone(c, ic, x0 + hh / 2, y + hh / 2, hh * 0.42, BLANC if i in (0, 3) else ENCRE, 2.6)
                texte(c, lab, x0 + hh + 14, y + hh / 2 - hauteurLigne(mix(44, 34, m), "noir") / 2, mix(44, 34, m), ENCRE, "noir", track=-0.01)
            if i in (1, 2):
                pilule(c, "+ marge", 860, y + hh / 2, entre(t, TW(28) + 0.12 * i, 0.4, 2.4), "trending-up", ROUGE, BLANC, 30, 4)
            if i < 3:
                u = prog(t, T_INT + 0.25 + 0.14 * i, 0.25, sortie)
                trait(c, x0 + hh / 2, y + hh + 4, x0 + hh / 2, y + hh + 4 + mix(32, 14, m) * u, GRIS, 4, borne(a * 3), [6, 8])
        if m > 0:
            b = entre(t, T_PERS - 0.05, 0.5, 1.4)
            media(c, t, "rushes/atelier", 140, 1035, 800, 300, borne(b * 3), mix(0.6, 1, b), video_t0=T_PERS - 0.1, vitesse=1.1,
                  voile=("#FFFFFF", 0.25), accent=ROUGE)
            croix(c, 900, 1060, 40, entre(t, TW(36) - 0.05, 0.35, 2.4))
            pilule(c, "Pour dire non ?", 540, 1185, entre(t, TW(35) - 0.1, 0.4, 2.2), "circle-help", ENCRE, BLANC, 34)


# ─────────────────────────────────────────── 4 · MONARQUE : disque noir et logo, puis le globe France → Chine
T_DQ = T_FR - 0.3


def monarque_globe(c, t):
    if t < T_MQ - 0.15 or t > T_BOUT + 0.6: return
    r = disque_noir(c, t, T_MQ - 0.12, T_DQ)
    u = prog(t, T_MQ + 0.05, 0.36, lambda v: rebond(v, 1.6))
    v = prog(t, T_DQ, 0.42, entreeSortie)                       # le logo monte se poser au-dessus du globe
    o = prog(t, T_BOUT + 0.15, 0.4, entree)
    a = entre(t, T_DQ + 0.05, 0.7, 1.2)
    if a > 0:
        rot = prog(t, T_FR + 0.1, T_CHINE - T_FR - 0.05, entreeSortie)
        lon0 = mix(14, 104, rot) + 2.5 * (t - T_DQ); lat0 = mix(38, 30, rot)
        R = 410 * mix(0.75, 1, a) * mix(1, 0.75, o)
        cx, cy = 540, 1000 - 900 * o
        with Calque(c, borne(a * 3) * (1 - o)):
            # retour du client (16/10) : le globe EN POINTS, la Chine qui s'allume, au lieu du globe blanc sculpté
            lum = prog(t, T_CHINE - 0.3, 0.5, sortie)
            G = globe_points(c, lon0, lat0, cx, cy, R, lum)
            ua = prog(t, T_FR + 0.15, T_CHINE - T_FR, entreeSortie)
            G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, 1.0, "#D5D1CB", 5, 0.3, [2, 16])
            hx, hy, hz = G.arc(c, PARIS, CANTON, cx, cy, R, lon0, lat0, ua, ENCRE, 7, 0.3)
            if 0 < ua < 1:
                disque(c, hx, hy, 24, ENCRE, 1, (6, 16, 0.25)); icone(c, "plane", hx, hy, 28, BLANC, 2.4)
            G.repere(c, *PARIS, cx, cy, R, lon0, lat0, "France", ENCRE, "FR", entre(t, T_FR - 0.05, 0.42, 2.0), 1.0, 70)
            kx, ky, kz = G.pos(*CANTON, lon0, lat0, R, cx, cy)
            if kz > 0.05 and t > T_CHINE - 0.2:
                onde(c, kx, ky, t, T_CHINE, 20, 180, ENCRE, 6, 0.7)
            G.repere(c, *CANTON, cx, cy, R, lon0, lat0, "Bureau en Chine", ENCRE, "CN", entre(t, T_CHINE - 0.05, 0.42, 2.0), 1.0, 90)
    if t >= T_MQ + 0.03:
        lw = mix(1.5, 1, u) * mix(860, 440, v)
        ly = mix(960, 430, v) - 900 * o
        if v < 1: logo(c, 540, ly, lw, True, borne(u * 3) * (1 - v))
        if v > 0: logo(c, 540, ly, lw, False, v * (1 - o))
    return r


# ─────────────────────────────────────────── 5 · votre boutique, votre marché
def boutique(c, t):
    g = Groupe(c, t, T_BOUT + 0.15, T_DEV, ent="bas", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VOTRE BOUTIQUE", TW(52) - 0.1, T_MARCHE - 0.1)
        titre(c, t, "VOTRE MARCHÉ", T_MARCHE - 0.05, T_DEV - 0.1)
        a = entre(t, T_BOUT + 0.2, 0.55, 1.4)
        media(c, t, "shop", 190, 580, 700, 780, borne(a * 3), mix(0.7, 1, a), zoom=1.04 + 0.05 * max(0, t - T_BOUT), fx=0.5, fy=0.4,
              accent=ENCRE if t > T_MARCHE else None)
        pilule(c, "Votre clientèle", 270, 820, entre(t, TW(52) + 0.15, 0.4, 2.2), "users", ENCRE, BLANC, 32, -4)
        pilule(c, "Vos prix", 830, 1000, entre(t, TW(54), 0.4, 2.2), "euro", ENCRE, BLANC, 32, 3)
        pilule(c, "Les tendances", 300, 1220, entre(t, T_MARCHE + 0.05, 0.4, 2.2), "trending-up", VERT, BLANC, 32, -2)


# ─────────────────────────────────────────── 6 · développement : matières, patronages, prototypes
# retour du client (16/10) : plans trop serrés dans des bandes larges → trois cartes verticales au format des rushes
# (plan entier, « vue d'ensemble ») ; matières = son nuancier, patronages = sa fiche technique, prototypes inchangé
DEV = [("Matières", "layers", "rushes/nuancier", 1.0, T_MAT), ("Patronages", "scissors", "fiche-technique", None, T_PAT),
       ("Prototypes", "shirt", "rushes/couture", 1.2, T_PROTO)]
DW, DH, DG = 316, 562, 12


def developpement(c, t):
    g = Groupe(c, t, T_DEV - 0.1, T_USI, ent="droite", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "DÉVELOPPEMENT", T_DEV, T_USI - 0.1)
        actif = max([k for k, d in enumerate(DEV) if t >= d[4] - 0.12] or [-1])
        x0 = (1080 - 3 * DW - 2 * DG) / 2
        for k, (lab, ic, nom, vit, t0) in enumerate(DEV):
            u = entre(t, T_DEV + 0.08 * k, 0.45, 1.6)
            if u <= 0: continue
            x, y = x0 + k * (DW + DG), 590
            on = k == actif
            dim = 1.0 if (actif < 0 or k <= actif) else 0.5
            s = mix(1.0, 1.04, prog(t, t0 - 0.12, 0.3, entreeSortie)) if on else 1.0
            c.save(); c.translate((1 - u) * 500, 80 * (1 - u))
            if vit is None:
                media(c, t, nom, x, y, DW, DH, borne(u * 3) * dim, s, zoom=1.0, fx=0.5, fy=0.5,
                      accent=ENCRE if on else None, pad=10, r=30)
            else:
                media(c, t, nom, x, y, DW, DH, borne(u * 3) * dim, s, video_t0=T_DEV, vitesse=vit, accent=ENCRE if on else None,
                      pad=10, r=30)
            c.restore()
            pilule(c, lab, x + DW / 2, y + DH + 50, entre(t, t0 - 0.1, 0.4, 2.2), ic, ENCRE, BLANC, 30)
            coche(c, x + DW - 36, y + 36, 28, entre(t, t0 + 0.25, 0.35, 2.4))


# ─────────────────────────────────────────── 7 · les usines comparées, la négociation
def slider(c, lab, ic, y, v, actif):
    texte(c, lab, 230, y - 70, 34, ENCRE, "noir", track=0.02)
    icone(c, ic, 190, y - 70 + hauteurLigne(34) / 2, 34, ENCRE, 2.4)
    rrect(c, 180, y, 720, 14, 7, "#E8E5E0")
    rrect(c, 180, y, 720 * v, 14, 7, ENCRE)
    disque(c, 180 + 720 * v, y + 7, 28 if actif else 22, BLANC, 1, (8, 20, 0.3)); anneau(c, 180 + 720 * v, y + 7, 28 if actif else 22, ENCRE, 4)


def usines(c, t):
    g = Groupe(c, t, T_USI - 0.1, T_CTRL, ent="bas", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ON COMPARE", T_USI, T_NEG - 0.1)
        titre(c, t, "ON NÉGOCIE", T_NEG - 0.05, T_CTRL - 0.1)
        sw = prog(t, T_NEG - 0.15, 0.4, entreeSortie)
        noms = ["rushes/machines", "rushes/atelier", "rushes/bureau"]
        for k in range(3):
            u = entre(t, T_USI + 0.06 + 0.1 * k, 0.45, 1.6)
            if u <= 0: continue
            elu = k == 1 and t > TW(67) + 0.1
            x = 70 + k * 320
            y = mix(620, 560, sw)
            s = mix(0.6, 1, u) * mix(1, 0.62, sw)
            dim = 0.45 if (t > TW(67) + 0.1 and not elu) else 1.0
            c.save(); c.translate(540 + (x + 150 - 540) * mix(1, 0.62, sw), y); c.scale(s, s); c.translate(-(x + 150), -y)
            media(c, t, noms[k], x, y, 300, 420, borne(u * 3) * dim, 1.0, video_t0=T_USI, vitesse=1.2, accent=VERT if elu else None, r=30, pad=10)
            pilule(c, f"Usine {'ABC'[k]}", x + 150, y + 470, 1.0 * borne(u * 3), "factory", ENCRE, BLANC, 28)
            if elu: coche(c, x + 270, y + 30, 36, entre(t, TW(67) + 0.1, 0.35, 2.4))
            c.restore()
        # la loupe qui passe d'une usine à l'autre
        if t < TW(67) + 0.2:
            lx = cles(t, [(T_USI + 0.3, 220), (TW(66), 860, entreeSortie), (TW(67), 540, entreeSortie)])
            with Calque(c, entre(t, T_USI + 0.3, 0.3, 1.5) * (1 - prog(t, TW(67) + 0.05, 0.15))):
                disque(c, lx, 830, 70, BLANC, 0.9, (10, 26, 0.25)); icone(c, "search", lx, 830, 70, ENCRE, 2.8)
        if sw > 0:
            b = entre(t, T_NEG - 0.05, 0.5, 1.4)
            c.save(); c.translate(540, 1150); c.scale(mix(0.6, 1, b), mix(0.6, 1, b)); c.translate(-540, -1150)
            with Calque(c, borne(b * 3)):
                cadre(c, 120, 900, 840, 520, 44)
                for k, (lab, ic, t0, v0, v1) in enumerate([("PRIX", "euro", T_PRIX, 0.82, 0.48), ("VOLUMES", "boxes", T_VOL, 0.3, 0.7),
                                                           ("DÉLAIS", "calendar-clock", T_DEL, 0.85, 0.5)]):
                    v = mix(v0, v1, prog(t, t0 - 0.05, 0.5, entreeSortie))
                    slider(c, lab, ic, 1050 + k * 140, v, t0 - 0.05 < t < t0 + 0.6)
            c.restore()


# ─────────────────────────────────────────── 8 · contrôle qualité dans l'atelier, avant le départ
def controle(c, t):
    g = Groupe(c, t, T_CTRL - 0.1, T_VAL, ent="droite", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "CONTRÔLE QUALITÉ", T_CTRL, T_VAL - 0.1, taille=90)
        a = entre(t, T_CTRL, 0.5, 1.4)
        media(c, t, "rushes/controle", 140, 570, 800, 780, borne(a * 3), mix(0.7, 1, a), video_t0=T_CTRL, vitesse=1.15,
              accent=VERT if t > TW(85) else None)
        pilule(c, "Dans l'atelier", 330, 690, entre(t, T_ATEL - 0.1, 0.4, 2.2), "map-pin", ENCRE, BLANC, 32, -3)
        pilule(c, "Avant le départ", 740, 1240, entre(t, T_DEP, 0.4, 2.2), "truck", ENCRE, BLANC, 32, 3)
        tampon(c, "CONTRÔLÉ", 540, 980, t, TW(85) + 0.05, 64, VERT, -8, "check")


# ─────────────────────────────────────────── 9 · ce que vous validez = ce que vous recevez
def valide(c, t):
    g = Groupe(c, t, T_VAL - 0.1, T_TEST, ent="grand", sor="haut", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VALIDÉ = REÇU", T_VAL, T_TEST - 0.1, couleur=VERT)
        for k, (lab, t0) in enumerate([("Validé", T_VAL), ("Reçu", T_REC2 + 0.1)]):
            u = entre(t, t0, 0.5, 1.5)
            if u <= 0: continue
            x = 70 + k * 500
            media(c, t, LONG, x, 600, 440, 720, borne(u * 3), mix(0.6, 1, u), zoom=1.14, accent=VERT, rot=mix(8 if k else -8, 0, u))
            pilule(c, lab, x + 220, 1385, entre(t, t0 + 0.2, 0.4, 2.2), "check", VERT)
        signe(c, "=", 540, 960, entre(t, TW(94) - 0.05, 0.35, 2.6), VERT, 70, t, TW(94))
        eclats(c, 540, 960, t, TW(94), 14, 320, [VERT, ENCRE, BEIGE], graine=6)


# ─────────────────────────────────────────── 10 · vous testez, ce qui se vend, on le relance
def relance(c, t):
    g = Groupe(c, t, T_TEST - 0.1, T_FRCN, ent="bas", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "VOUS TESTEZ", T_TEST, T_RELANCE - 0.1)
        titre(c, t, "ON RELANCE", T_RELANCE - 0.05, T_FRCN - 0.1, couleur=VERT)
        a = entre(t, T_TEST, 0.5, 1.4)
        c.save(); c.translate(540, 960); c.scale(mix(0.6, 1, a), mix(0.6, 1, a)); c.translate(-540, -960)
        with Calque(c, borne(a * 3)):
            cadre(c, 120, 580, 840, 600, 44)
            texte(c, "VOS VENTES", 180, 630, 34, ENCRE, "noir", track=0.06)
            # retour du client (16/10) : un modèle DIFFÉRENT sous chaque barre, en entier (ses photos produits)
            for k, (h0, h1, nom, fy) in enumerate([(0.3, 0.38, "produits/veste-ceinturee-prune", 0.5), (0.35, 0.3, "produits/blouson-cuir-noir", 0.5),
                                                   (0.3, 0.95, "produits/veste-zip-marine", 0.5), (0.25, 0.22, "produits/chemise-rayee-bordeaux", 0.5)]):
                hb = mix(h0, h1, prog(t, T_VEND - 0.1 + 0.05 * k, 0.6, entreeSortie)) * prog(t, T_TEST + 0.15 + 0.06 * k, 0.4, sortie)
                x = 200 + k * 190; base = 1050
                col = VERT if (k == 2 and t > T_VEND) else "#DCD8D2"
                rrect(c, x, base - 340 * hb, 120, 340 * hb, 18, col)
                rrect(c, x + 6, base + 16, 108, 108, 22, "#EFEDEA")
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 6, base + 16, 108, 108), 22, 22), True)
                image_cover(c, nom, x + 6, base + 16, 108, 108, 1.0, 0.5, fy); c.restore()
                if k == 2 and t > T_VEND: rrect(c, x + 6, base + 16, 108, 108, 22, None, 1, None, VERT, 4)
            pilule(c, "Best-seller", 580, 1050 - 340 * 0.95 - 50, entre(t, T_VEND + 0.3, 0.4, 2.4), "flame", VERT, BLANC, 28)
        c.restore()
        b = entre(t, T_RELANCE - 0.25, 0.45, 2.0)
        if b > 0:
            clic = prog(t, T_RELANCE + 0.2, 0.1) * (1 - prog(t, T_RELANCE + 0.32, 0.15))
            s = mix(0.4, 1, b) * (1 - 0.06 * clic)
            c.save(); c.translate(540, 1280); c.scale(s, s)
            pastille(c, "Relancer la production", 0, 0, 40, VERT if t > T_RELANCE + 0.25 else ENCRE, BLANC, "refresh-cw", borne(b * 3), (14, 34, 0.3))
            c.restore()
            pc = prog(t, T_RELANCE - 0.2, 0.4, sortie)
            if t < T_RELANCE + 1.0:
                curseur(c, mix(980, 640, pc), mix(1650, 1300, pc), 1.3, 1 - prog(t, T_RELANCE + 0.7, 0.3), clic)
            confettis(c, 540, 1100, t, T_RELANCE + 0.25, 24, 380, 3, [VERT, ENCRE, BEIGE, "#FFB7B7"])


# ─────────────────────────────────────────── 11 · culture produit française, puissance industrielle chinoise
def deux_mondes(c, t):
    g = Groupe(c, t, T_FRCN - 0.1, T_FIN, ent="zoom", sor="recul", cy=960)
    if not g.visible: return
    with g:
        for k, (nom, vid, lab1, lab2, pays, t0) in enumerate([("studio", None, "CULTURE PRODUIT", "française", "FR", T_FRCN),
                                                              ("rushes/machines", 1.2, "PUISSANCE", "industrielle chinoise", "CN", T_PUIS)]):
            u = entre(t, t0 - 0.05, 0.5, 1.5)
            if u <= 0: continue
            y = 470 + k * 470
            c.save(); c.translate((1 - u) * (-700 if k == 0 else 700), 0)
            if vid: media(c, t, nom, 90, y, 900, 430, borne(u * 3), 1.0, video_t0=t0, vitesse=vid, voile=("#000000", 0.35))
            else: media(c, t, nom, 90, y, 900, 430, borne(u * 3), 1.0, zoom=1.0, fy=0.52, voile=("#000000", 0.35))
            drapeau(c, pays, 150, y + 60, 72, 50, 8)
            texte(c, lab1, 150, y + 260, ajuste(lab1, 780, 76, "archivo"), BLANC, "archivo", track=-0.01)
            texte(c, lab2, 152, y + 350, 40, BLANC, "gras", track=-0.01, alpha=0.9)
            c.restore()


# ─────────────────────────────────────────── 12 · fin
def fin(c, t):
    if t < T_FIN - 0.1: return
    carton_fin(c, t, T_FIN, T_URL)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9)
son(T_RECU - 0.2, "whoosh_bas", -6); son(T_RECU + 0.25, "impact", -4); son(T_RECU + 0.3, "verre", -10)
son(T_RECU + 0.25, "check", -12); son(T_RECU + 0.4, "pop", -10); son(TW(5) - 0.05, "croc", -8); son(TW(5) + 0.18, "tampon", -5)
son(T_SCEN - 0.1, "whoosh", -8); son(TW(10) - 0.1, "pop", -10); son(TW(12) - 0.1, "pop", -11)
son(T_ECH - 0.15, "whoosh", -8); son(TW(17) - 0.05, "check", -9); son(T_PROD - 0.1, "whoosh_court", -9)
son(TW(22) - 0.05, "croc", -8)
for k in range(3): son(TW(24) - 0.05 + 0.1 * k, "pop", -12)
son(T_INT - 0.1, "whoosh_bas", -8)
for i in range(4): son(T_INT + 0.05 + 0.14 * i, "pop", -11)
for i in (1, 2): son(TW(28) + 0.12 * i, "ching", -11)
son(T_PERS - 0.1, "whoosh", -8); son(TW(35) - 0.1, "pop", -10); son(TW(36) - 0.05, "croc", -8)
son(T_MQ - 0.12, "whoosh_long", -7); son(T_MQ + 0.05, "impact", -4); son(T_MQ + 0.08, "ching", -9)
son(T_DQ, "whoosh_bas", -8); son(T_FR - 0.05, "pop", -10); son(T_INST, "whoosh_long", -9); son(T_CHINE - 0.05, "impact_doux", -7)
son(T_CHINE, "check", -11)
son(T_BOUT + 0.15, "whoosh", -8); son(TW(52) + 0.15, "pop", -10); son(TW(54), "pop", -10); son(T_MARCHE + 0.05, "pop", -10)
son(T_DEV - 0.1, "whoosh_court", -8)
for d in DEV: son(d[4] - 0.1, "pop", -10); son(d[4] + 0.25, "check", -12)
son(T_USI - 0.1, "whoosh_bas", -8); son(TW(66), "swipe", -12); son(TW(67) + 0.1, "check", -9)
son(T_NEG - 0.1, "whoosh", -8)
for t0 in (T_PRIX, T_VOL, T_DEL): son(t0 - 0.05, "clic", -9); son(t0 + 0.1, "swipe", -13)
son(T_CTRL - 0.1, "whoosh_court", -8); son(T_ATEL - 0.1, "pop", -10); son(T_DEP, "pop", -10); son(TW(85) + 0.05, "tampon", -5)
son(T_VAL - 0.1, "whoosh_long", -8); son(T_VAL + 0.2, "check", -10); son(T_REC2 + 0.3, "check", -10)
son(TW(94) - 0.05, "impact_doux", -6); son(TW(94), "ching", -8)
son(T_TEST - 0.1, "whoosh", -8)
for k in range(4): son(T_TEST + 0.15 + 0.06 * k, "blip", -14)
son(T_VEND + 0.3, "ching", -9); son(T_RELANCE - 0.25, "pop", -10); son(T_RELANCE + 0.2, "clic", -5); son(T_RELANCE + 0.25, "check", -8)
son(T_FRCN - 0.1, "whoosh_bas", -8); son(T_PUIS - 0.1, "whoosh_bas", -8)
son(T_FIN - 0.1, "montee", -11); son(T_FIN + 0.05, "impact", -5); son(T_URL - 0.15, "pop", -9); son(T_URL + 0.45, "clic", -5)
son(T_URL + 0.5, "ching", -8)

for a, b in [(T_RECU - 0.1, T_RECU + 0.3), (T_SCEN - 0.15, T_SCEN + 0.3), (T_INT - 0.1, T_INT + 0.3), (T_MQ - 0.1, T_MQ + 0.3),
             (T_BOUT + 0.1, T_BOUT + 0.5), (T_DEV - 0.15, T_DEV + 0.3), (T_USI - 0.15, T_USI + 0.3), (T_CTRL - 0.15, T_CTRL + 0.3),
             (T_VAL - 0.15, T_VAL + 0.3), (T_TEST - 0.15, T_TEST + 0.3), (T_FRCN - 0.15, T_FRCN + 0.3), (T_FIN - 0.1, T_FIN + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_RECU + 0.25, ROUGE, 0.08), (T_MQ + 0.05, "#FFFFFF", 0.1), (TW(94), VERT, 0.08), (T_RELANCE + 0.25, VERT, 0.07)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_clair(c, t)
    hook(c, t); scenario(c, t); intermediaires(c, t)
    r = monarque_globe(c, t)
    boutique(c, t); developpement(c, t); usines(c, t); controle(c, t); valide(c, t); relance(c, t); deux_mondes(c, t); fin(c, t)
    K.dessine_eclairs(c, t)
    if not (T_MQ - 0.1 < t < TW(39) - 0.05) and t < T_FIN - 0.1:
        SOUS.dessine(c, t, BLANC if (r or 0) > 1200 else ENCRE)
