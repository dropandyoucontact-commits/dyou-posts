"""CB-M15 « Ce sac existe en trois qualités » — story Snapchat DROP&YOU (15/10/2026), voix Tomy au débit validé
(4,2 mots/s demandés, pauses 0,18 s). Même sujet que CB-M14, refait sans aucun prix : trois qualités (standard /
1:1 / qualité originale ; v2 du 15/10 : ni « vrais matériaux » ni « vite fait », Youssef ne veut pas mentir ni descendre la première), ça vaut pour tout (montres, baskets, vêtements), puis le crocodile cousu main.
Story Snap : aucun appel à enregistrer, partager ou commenter ; interface Snap en haut (≈ 0-250) et en bas (≈ 1700+)
laissée libre. Fond « cobalt » (moteur/cobalt.py) à la place du noir et or.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence
from studio import lettres, Groupe, eclats, rayons, entre, SousTitresEncre
from noir import *
from cobalt import *

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.8, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresEncre(K, fusions={(52,): "1:1.", (152, 153, 154): "DROP&YOU."}, y=1440, larg=900, taille=54, fam="gras", max_mots=5)

PHOTO_DESSUS = "photos/sacs/sacoches-3-qualites-dessus"
PHOTO_3 = "photos/sacs/sacoches-3-qualites-face"
SANGLES = "videos/sacs/sacoches-3-qualites-sangles"
CROCO_PHOTO = "photos/croco/croco-deux-sacs-finis"
CROCO_BOITE = "videos/croco/croco-sac-fini-boite"
CROCO_PEAUX = "videos/croco/croco-peaux-telephone-defile"
CROCO_TYPES = "videos/croco/croco-types-de-peaux-comparatif"
CROCO_PORTEF = "videos/croco/croco-portefeuille-violet"
AVIS = [("photos/avis/avis-sac-beige-matelasse", 0.42), ("photos/avis/avis-pochette-noire-matelassee", 0.45),
        ("photos/avis/avis-sacoche-nylon-noire", 0.45), ("photos/avis/avis-claquettes-noires", 0.55)]
# du standard (sac du bas de la photo, le plus lisse) à la qualité originale (sac du haut, le grain)
QUAL = [("Standard", 0.645, "Le modèle", "heart", TW(35)), ("1:1", 0.462, "Les détails", "copy", TW(60)),
        ("Qualité originale", 0.305, "Le plus proche", "gem", TW(70))]
BANDES = [560, 835, 1110]
BLEU_CASE = "#0A1650"

T_UNE, T_DEVINE, T_FIN1 = TW(6), TW(13), TW(15) - 0.1
T_Q = [TW(25), TW(44), TW(61)]
T_GRAIN, T_FERR, T_MILLI = TW(75), TW(77), TW(79)
T_TOUT, T_MONT, T_BASK, T_VET, T_MARCH, T_BUDG = TW(83), TW(89), TW(91), TW(93), TW(94), TW(102)
T_FOU, T_COUSU, T_CROCO, T_MAISONS, T_PEAU, T_MOIS = TW(106), TW(113), TW(116), TW(123), TW(128), TW(132)
T_FIN, T_DY = TW(145) - 0.1, TW(152) - 0.1


def titre(c, t, txt, t0, t1, y=440, cols=None, taille=96):
    """titre lettre par lettre ; parti avant que le suivant n'entre"""
    if t < t0 - 0.1 or t > t1 + 0.1: return
    ts = ajuste(txt, 960, taille, "noir", -0.03)
    a = 1 - prog(t, t1 - 0.2, 0.15, entree)
    lettres(c, txt, 540, y - ts * 0.62, ts, t, t0 - 0.05, "masque", decal=0.022, duree=0.4, grad=True,
            cols=cols or [BLANC, "#DCE6FF"], alpha=a)


OR_C = [ORANGE, ORANGE2]


def interro(c, cx, cy, t, a, k):
    """pastille orange « ? » qui palpite"""
    if a <= 0.01: return
    b = mix(0.3, 1, a) * (1 + 0.07 * math.sin(t * 7 + k * 2))
    c.save(); c.translate(cx, cy); c.scale(b, b)
    lueur(c, 0, 0, 120, ORANGE, 0.35)
    disque(c, 0, 0, 62, ORANGE, borne(a * 3)); texte(c, "?", 0, -hauteurLigne(84) / 2, 84, BLEU_CASE, "noir", "centre", 0, borne(a * 3))
    c.restore()


def bande(c, t, k, y, u, actif, dim=1.0):
    nom, fy = QUAL[k][0], QUAL[k][1]
    c.save(); c.translate((1 - u) * 300, 0)
    case_media(c, t, PHOTO_3, 90, y, 900, 250, borne(u * 3) * dim, 1.0, zoom=1.08 + 0.03 * actif * t % 1 * 0, fx=0.52, fy=fy,
               accent=ORANGE if actif else None)
    c.restore()


# ─────────────────────────────────────────── HOOK : trois qualités, une seule vraiment proche de l'original, devine laquelle
def hook(c, t):
    if t > T_Q[0] + 0.3: return
    fin = prog(t, T_Q[0] - 0.3, 0.3, entree)
    with Calque(c, 1 - fin):
        a1 = 1 - prog(t, T_UNE - 0.2, 0.15, entree)
        if a1 > 0:
            lettres(c, "CE SAC EXISTE", 540, 330, 92, t, -0.7, "ressort", grad=False, couleur=BLANC, decal=0.03, alpha=a1)
            lettres(c, "EN 3 QUALITÉS", 540, 440, 108, t, -0.55, "ressort", cols=OR_C, decal=0.03, alpha=a1)
        a2 = 1 - prog(t, T_DEVINE - 0.2, 0.15, entree)
        if t > T_UNE - 0.1 and a2 > 0:
            lettres(c, "UNE SEULE", 540, 330, 92, t, T_UNE - 0.05, "ressort", grad=False, couleur=BLANC, decal=0.03, alpha=a2)
            lettres(c, "LA PLUS PROCHE", 540, 440, 100, t, TW(9) - 0.1, "ressort", cols=OR_C, decal=0.025, alpha=a2)
        if t > T_DEVINE - 0.1:
            lettres(c, "DEVINE LAQUELLE", 540, 400, 100, t, T_DEVINE - 0.05, "ressort", cols=OR_C, decal=0.03)
        sp = prog(t, T_DEVINE - 0.2, 0.45, entreeSortie)
        if sp < 1:
            case_media(c, t, PHOTO_DESSUS, 140, 590, 800, 760, 1 - sp, mix(1, 0.9, sp), zoom=1.08 + 0.025 * t, fy=0.5,
                       accent=ORANGE if t > T_UNE else None)
            with Calque(c, 1 - sp):
                for k, (lab, ic, t0) in enumerate([("Même modèle", "copy", 0.15), ("3 qualités", "layers", 0.6)]):
                    puce(c, lab, 140 + 40 + largeur(lab, 34, "gras") / 2 + 50, 660 + k * 95, entre(t, t0, 0.4, 2.2), ic, ORANGE, 34)
                puce(c, "Proche de l'original", 540, 1280, entre(t, TW(11), 0.4, 2.2), "gem", ORANGE, 36)
        if sp > 0:
            for k in range(3):
                u = entre(t, T_DEVINE - 0.2 + 0.08 * k, 0.45, 1.6)
                if u <= 0: continue
                bande(c, t, k, BANDES[k], u, False)
                etiquette_case(c, str(k + 1), 150, BANDES[k] + 60, u, BLANC, 40, "noir", BLEU_CASE)
                interro(c, 900, BANDES[k] + 125, t, entre(t, T_DEVINE + 0.1 + 0.12 * k, 0.4, 2.2), k)
    # « je te montre le plus fou » : le cadenas, garé en haut à droite jusqu'au crocodile
    if T_FIN1 <= t < T_FOU + 1.0:
        a = entre(t, T_FIN1, 0.5, 1.6)
        gare = prog(t, T_Q[0] - 0.5, 0.5, entreeSortie)
        ouvre = prog(t, T_FOU + 0.2, 0.3, sortie)
        cx, cy = mix(540, 880, gare), mix(960, 300, gare)
        cadenas(c, cx, cy, mix(0.4, 1.25, a) * mix(1, 0.29, gare), t, "LE PLUS FOU", ouvre, 1 - prog(t, T_FOU + 0.55, 0.3))
        eclats(c, cx, cy, t, T_FOU + 0.2, 14, 260, [ORANGE, BLANC, ORANGE2], graine=8)


# ─────────────────────────────────────────── les trois qualités, sans prix
def qualites(c, t):
    if t < T_Q[0] - 0.3 or t > T_GRAIN + 0.4: return
    sortie_ = prog(t, T_GRAIN - 0.15, 0.35, entree)
    titre(c, t, "STANDARD", T_Q[0], T_Q[1] - 0.1)
    titre(c, t, "LE 1:1", T_Q[1], T_Q[2] - 0.1)
    titre(c, t, "QUALITÉ ORIGINALE", T_Q[2], T_GRAIN - 0.1, cols=OR_C)
    with Calque(c, 1 - sortie_):
        actif = max([k for k in range(3) if t >= T_Q[k] - 0.15] or [-1])
        for k in range(3):
            y = BANDES[k]; on = k == actif
            dim = 1.0 if (on or k < actif) else 0.4
            bande(c, t, k, y, 1.0, on, dim)
            puce(c, QUAL[k][0], 90 + 40 + largeur(QUAL[k][0], 32, "gras") / 2 + 30, y + 52, entre(t, T_Q[k] - 0.1, 0.4, 2.2), None, ORANGE, 32)
            tag = QUAL[k][2]
            etiquette_case(c, tag, 990 - 40 - largeur(tag, 36, "noir") / 2 - 20, y + 250 - 48, entre(t, QUAL[k][4] - 0.05, 0.35, 2.4),
                           ORANGE if k < 2 else VERT, 36, "noir", BLEU_CASE if k < 2 else BLANC, )
        # détail parlé : le 1:1, un cran au-dessus
        puce(c, "Un cran au-dessus", 700, BANDES[1] + 60, entre(t, TW(54) - 0.1, 0.4, 2.2), "trending-up", ORANGE, 30)
        if t > T_Q[2]:
            lueur(c, 540, BANDES[2] + 125, 520, ORANGE, 0.12 * entre(t, T_Q[2], 0.5, 1.2))


# ─────────────────────────────────────────── le grain, les ferrures, au millimètre
def details(c, t):
    g = Groupe(c, t, T_GRAIN - 0.12, T_TOUT, ent="zoom", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "LE GRAIN", T_GRAIN, T_FERR - 0.1, cols=OR_C)
        titre(c, t, "LES FERRURES", T_FERR, T_MILLI - 0.1)
        titre(c, t, "AU MILLIMÈTRE", T_MILLI, T_TOUT - 0.1, cols=OR_C)
        sf = prog(t, T_FERR - 0.15, 0.4, entreeSortie)
        if sf < 1:
            a = entre(t, T_GRAIN - 0.1, 0.5, 1.5)
            case_media(c, t, PHOTO_3, 90, 560, 900, 780, borne(a * 3) * (1 - sf), mix(0.6, 1, a), zoom=3.2 + 0.18 * max(0, t - T_GRAIN),
                       fx=0.42, fy=QUAL[2][1] + 0.01, accent=ORANGE)
            puce(c, "Le grain", 300, 640, entre(t, TW(76) - 0.1, 0.4, 2.2) * (1 - sf), "scan-line", ORANGE, 34)
            coche(c, 930, 620, 38, entre(t, TW(76) + 0.2, 0.35, 2.4) * (1 - sf))
        if sf > 0:
            case_media(c, t, SANGLES, 190, 560, 700, 780, borne(sf * 3), mix(0.7, 1, sf), video_t0=T_FERR - 0.15, vitesse=1.6, accent=ORANGE)
            puce(c, "Ferrures", 340, 1280, entre(t, T_FERR + 0.1, 0.4, 2.2), "check", VERT, 34)
            # la règle du millimètre
            m = prog(t, T_MILLI + 0.05, 0.6, entreeSortie)
            if m > 0:
                x0, y0 = 230, 1180
                trait(c, x0, y0, x0 + 620 * m, y0, ORANGE, 5)
                for j in range(int(31 * m) + 1):
                    hh = 34 if j % 5 == 0 else 18
                    trait(c, x0 + j * 20, y0, x0 + j * 20, y0 - hh, ORANGE, 3)
                puce(c, "Au mm", 760, 1280, entre(t, T_MILLI + 0.4, 0.4, 2.2), "target", ORANGE, 34)


# ─────────────────────────────────────────── ça marche pour tout : montres, baskets, vêtements ; tous les budgets
COLS = [("Montres", "watch", "montres-serties", 1.3, T_MONT), ("Baskets", "footprints", "videos/chaussures/baskets-stock-1", 1.3, T_BASK),
        ("Vêtements", "shirt", "originaux/veste-racing-noire", None, T_VET)]


def pour_tout(c, t):
    g = Groupe(c, t, T_TOUT - 0.12, T_FOU, ent="droite", sor="zoom", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "ÇA MARCHE POUR TOUT", T_TOUT, T_MARCH - 0.1, taille=88)
        titre(c, t, "TOUS LES MARCHÉS", T_MARCH, T_BUDG - 0.1, cols=OR_C)
        titre(c, t, "TOUS LES BUDGETS", T_BUDG, T_FOU - 0.1, cols=OR_C)
        mo = prog(t, T_MARCH - 0.1, 0.45, entreeSortie)
        for k, (lab, ic, nom, vit, t0) in enumerate(COLS):
            u = entre(t, (T_TOUT + 0.1 + 0.1 * k) if k else T_TOUT, 0.5, 1.5)
            u = max(u * 0.0, u)
            if u <= 0: continue
            on = t >= t0 - 0.1
            x = 60 + k * 330
            y = mix(580, 560, mo)
            c.save(); c.translate(x + 150, y + 330); s = mix(0.5, 1, u) * mix(1, 0.86, mo); c.scale(s, s); c.translate(-(x + 150), -(y + 330))
            if vit:
                case_media(c, t, nom, x, y, 300, 600, borne(u * 3) * (1.0 if on else 0.45), 1.0, video_t0=T_TOUT, vitesse=vit,
                           accent=ORANGE if (on and t < T_MARCH) else None, r=30, pad=8)
            else:
                case_media(c, t, nom, x, y, 300, 600, borne(u * 3) * (1.0 if on else 0.45), 1.0, zoom=1.15, fy=0.45,
                           accent=ORANGE if (on and t < T_MARCH) else None, r=30, pad=8)
            c.restore()
            puce(c, lab, x + 150, mix(1250, 1150, mo), entre(t, t0 - 0.1, 0.4, 2.2), None, ORANGE, 32)
        # tous les budgets : trois niveaux, tous cochés
        if t > T_BUDG - 0.2:
            for k, lab in enumerate(["€", "€€", "€€€"]):
                u = entre(t, T_BUDG + 0.05 + 0.1 * k, 0.4, 2.2)
                if u <= 0: continue
                x = 210 + k * 330
                c.save(); c.translate(x, 1280); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
                case(c, -110, -62, 220, 124, 30, borne(u * 3), accent=ORANGE if k == 2 else None)
                texte(c, lab, 0, -hauteurLigne(60) / 2, 60, ORANGE, "noir", "centre", 0, borne(u * 3))
                c.restore()
                coche(c, x + 95, 1230, 26, entre(t, T_BUDG + 0.4 + 0.1 * k, 0.35, 2.4))
        elif t > T_MARCH:
            for k, (lab, ic) in enumerate([("Standard", "heart"), ("1:1", "copy"), ("Originale", "gem")]):
                puce(c, lab, 210 + k * 330, 1280, entre(t, T_MARCH + 0.1 + 0.1 * k, 0.4, 2.2) * (1 - prog(t, T_BUDG - 0.25, 0.15)),
                     ic, ORANGE, 32)


# ─────────────────────────────────────────── le plus fou : cousu main, crocodile
def croco(c, t):
    if t < T_FOU - 0.2: return
    g = Groupe(c, t, T_FOU - 0.2, T_FIN, ent="grand", sor="gauche", cy=960)
    if not g.visible: return
    with g:
        titre(c, t, "LE PLUS FOU", T_FOU, T_COUSU - 0.1, cols=OR_C)
        titre(c, t, "COUSU MAIN", T_COUSU, T_CROCO - 0.1)
        titre(c, t, "VRAIE PEAU DE CROCODILE", T_CROCO, T_MAISONS - 0.1, cols=OR_C)
        titre(c, t, "COMME LES GRANDES MAISONS", T_MAISONS, T_PEAU - 0.1, taille=84)
        titre(c, t, "CHOISIS TA PEAU", T_PEAU, T_MOIS - 0.1, cols=OR_C)
        titre(c, t, "1 MOIS, COUSU MAIN", T_MOIS, T_FIN - 0.1)
        sp = prog(t, T_PEAU - 0.15, 0.4, entreeSortie)
        a = entre(t, T_FOU + 0.1, 0.5, 1.5)
        if sp < 1:
            with Calque(c, 1 - sp):
                s1 = prog(t, T_COUSU - 0.1, 0.35, entreeSortie)
                s2 = prog(t, T_CROCO - 0.1, 0.35, entreeSortie)
                if s1 < 1:
                    case_media(c, t, CROCO_BOITE, 140, 560, 800, 780, borne(a * 3) * (1 - s1), mix(0.6, 1, a), video_t0=T_FOU, vitesse=1.3)
                if s1 > 0 and s2 < 1:
                    case_media(c, t, CROCO_PORTEF, 140, 560, 800, 780, s1 * (1 - s2), mix(0.92, 1, s1), video_t0=T_COUSU - 0.1, vitesse=1.5,
                               accent=ORANGE)
                    puce(c, "Fait main", 540, 1290, entre(t, T_COUSU + 0.1, 0.4, 2.2) * (1 - s2), "hand", ORANGE, 36)
                if s2 > 0:
                    case_media(c, t, CROCO_PHOTO, 140, 560, 800, 780, s2, mix(0.92, 1, s2), zoom=1.05 + 0.04 * max(0, t - T_CROCO), fy=0.55,
                               accent=ORANGE)
                    puce(c, "100 % crocodile", 540, 1290, entre(t, TW(122) - 0.1, 0.4, 2.2), "badge-check", ORANGE, 36)
                    etiquette_case(c, "Grandes maisons", 700, 630, entre(t, T_MAISONS + 0.1, 0.35, 2.4), ORANGE, 38, "noir", BLEU_CASE)
        if sp > 0:
            sw2 = prog(t, T_MOIS - 0.1, 0.4, entreeSortie)
            case_media(c, t, CROCO_PEAUX if sw2 < 0.5 else CROCO_PORTEF, 90, 540, 440, 800, sp, mix(0.85, 1, sp),
                       video_t0=(T_PEAU - 0.15) if sw2 < 0.5 else T_MOIS, vitesse=0.9 if sw2 < 0.5 else 1.6)
            case_media(c, t, CROCO_TYPES if sw2 < 0.5 else CROCO_BOITE, 550, 540, 440, 800, sp, mix(0.85, 1, sp),
                       video_t0=(T_PEAU - 0.15) if sw2 < 0.5 else T_MOIS - 3.0, vitesse=1.3, accent=ORANGE)
            if sw2 > 0:
                with Calque(c, sw2):
                    puce(c, "1 mois", 310, 1290, entre(t, TW(134) - 0.1, 0.4, 2.2), "calendar", ORANGE, 34)
                    puce(c, "Cousu main", 770, 1290, entre(t, TW(141) - 0.1, 0.4, 2.2), "hand", ORANGE, 34)


# ─────────────────────────────────────────── fin : sans te prendre la tête, DROP&YOU (pas d'appel à l'action Snap)
def fin(c, t):
    if t < T_FIN - 0.1: return
    titre(c, t, "SANS TE PRENDRE LA TÊTE", T_FIN, T_DY - 0.1)
    logo_t = prog(t, T_DY - 0.1, 0.4, entreeSortie)
    for k, (nom, fy) in enumerate(AVIS):
        u = entre(t, T_FIN + 0.2 + 0.25 * k, 0.5, 1.6)
        if u <= 0: continue
        rot = (-14, -5, 5, 14)[k]
        x = 540 + (k - 1.5) * 190
        y = 900 + abs(k - 1.5) * 40 - 300 * logo_t
        c.save(); c.translate(x, y + 260 * (1 - u)); c.rotate(rot * u); c.scale(mix(0.6, 1, u) * mix(1, 0.62, logo_t), mix(0.6, 1, u) * mix(1, 0.62, logo_t))
        case_media(c, t, nom, -170, -300, 340, 600, borne(u * 3), 1.0, zoom=1.0, fy=fy, pad=8, r=24)
        c.restore()
    if logo_t > 0:
        ul = entre(t, T_DY + 0.1, 0.5, 1.5)
        lueur(c, 540, 1120, 620 * logo_t, ORANGE, 0.25)
        rayons(c, 540, 1120, t, 900, 0.08 * logo_t, 14, ORANGE2)
        iw, ih = taille_img("logo-dy-blanc"); lw = 720 * mix(0.6, 1, ul)
        image(c, "logo-dy-blanc", 540 - lw / 2, 1110 - lw * ih / iw / 2, lw, borne(ul * 3))


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(0.15, "pop", -10); son(0.6, "pop", -10)
son(T_UNE - 0.1, "whoosh_court", -9); son(TW(9), "ching", -9); son(TW(11), "pop", -11)
son(T_DEVINE - 0.2, "whoosh_long", -9)
for k in range(3): son(T_DEVINE + 0.1 + 0.12 * k, "pop", -10)
son(T_FIN1, "impact_doux", -6); son(T_FIN1 + 0.05, "montee", -12)
son(T_Q[0] - 0.5, "whoosh", -9)
for k, t0 in enumerate(T_Q): son(t0 - 0.1, "pop", -9)
for q in QUAL: son(q[4] - 0.05, "ching", -10)
son(TW(54) - 0.1, "pop", -11)
son(T_GRAIN - 0.15, "whoosh_long", -8); son(TW(76) - 0.1, "pop", -10); son(TW(76) + 0.2, "check", -10)
son(T_FERR - 0.15, "whoosh_bas", -8); son(T_FERR + 0.1, "check", -9); son(T_MILLI + 0.05, "swipe", -10); son(T_MILLI + 0.4, "pop", -10)
son(T_TOUT - 0.15, "whoosh", -8)
for k, col in enumerate(COLS): son(col[4] - 0.1, "pop", -9)
son(T_MARCH - 0.1, "whoosh_court", -9)
for k in range(3): son(T_MARCH + 0.1 + 0.1 * k, "blip", -13)
for k in range(3): son(T_BUDG + 0.05 + 0.1 * k, "pop", -11); son(T_BUDG + 0.4 + 0.1 * k, "check", -13)
son(T_FOU - 0.2, "whoosh_long", -8); son(T_FOU + 0.2, "clic", -5); son(T_FOU + 0.22, "impact", -5); son(T_FOU + 0.25, "ching", -8)
son(T_COUSU - 0.1, "whoosh", -9); son(T_COUSU + 0.1, "pop", -10)
son(T_CROCO - 0.1, "whoosh", -9); son(TW(122) - 0.1, "check", -10); son(T_MAISONS + 0.1, "ching", -8)
son(T_PEAU - 0.15, "whoosh_bas", -8); son(T_MOIS - 0.1, "whoosh", -9); son(TW(134) - 0.1, "pop", -10); son(TW(141) - 0.1, "pop", -10)
son(T_FIN - 0.1, "whoosh", -9)
for k in range(4): son(T_FIN + 0.2 + 0.25 * k, "swipe", -11)
son(T_DY - 0.1, "montee", -11); son(T_DY + 0.1, "impact", -5); son(T_DY + 0.12, "ching", -9)

for a, b in [(0.0, 0.25), (T_DEVINE - 0.2, T_DEVINE + 0.3), (T_Q[0] - 0.5, T_Q[0] + 0.3), (T_GRAIN - 0.15, T_GRAIN + 0.3),
             (T_TOUT - 0.15, T_TOUT + 0.3), (T_FOU - 0.2, T_FOU + 0.4), (T_PEAU - 0.2, T_PEAU + 0.3), (T_FIN - 0.1, T_FIN + 0.3),
             (T_DY - 0.1, T_DY + 0.4)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_DEVINE + 0.1, ORANGE, 0.08), (T_FOU + 0.22, ORANGE, 0.12), (T_DY + 0.1, "#FFFFFF", 0.14)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_cobalt(c, t, battement(t, T_DY + 0.1, 1, 0.6) - 1)
    hook(c, t); qualites(c, t); details(c, t); pour_tout(c, t); croco(c, t); fin(c, t)
    K.dessine_eclairs(c, t)
    if t < T_DY: SOUS.dessine(c, t, BLANC)
