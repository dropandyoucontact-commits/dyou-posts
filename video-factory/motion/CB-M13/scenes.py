"""CB-M13 « Sac en crocodile » — organique ChinaBook (14/10/2026), voix You (clonée), 4 mots/s, style noir à cases fines.

Brief de Youssef : hook sur les sacs en vraie peau de crocodile des grandes marques (plusieurs dizaines de milliers d'euros),
possibles en Chine pour moins cher, confection un mois, cousus main ; la Chine ne rime pas avec « cheap » : pas cher, moyen,
top, originale — « c'est toi et ton budget » ; trois sacoches du même modèle : 120–150 € (revendeurs), 1:1 200–250 €,
originale + 300 € (le grain ; les autres trop lisses ; ferrures et sangle parfaites). Aucune marque dite.
Médias : banque/videos/croco, banque/photos/croco, banque/photos/sacs, banque/videos/sacs.
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

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.6, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresEncre(K, fusions={(117, 118): "120", (120, 121): "150", (129, 130, 131): "1:1,", (133, 134): "200",
                                  (136, 137, 138): "250.", (144, 145): "300", (198, 199): "ChinaBook,", (201, 202, 203): "DROP&YOU."},
                       y=1440, larg=900, taille=54, fam="gras", max_mots=5)

CROCO_PHOTO = "photos/croco/croco-deux-sacs-finis"
CROCO_BOITE = "videos/croco/croco-sac-fini-boite"
CROCO_PEAUX = "videos/croco/croco-peaux-telephone-defile"
CROCO_TYPES = "videos/croco/croco-types-de-peaux-comparatif"
CROCO_PORTEF = "videos/croco/croco-portefeuille-violet"

T_MARQUES, T_CHINE, T_ENR, T_RESTE = TW(10), TW(21), TW(31), TW(34) - 0.1
T_PEAUX, T_TEL, T_CONF = TW(38), TW(43), TW(49)
T_MYTHE, T_TOUT, T_BUDGET = TW(59), TW(76), TW(101)
T_SAC, T_Q = TW(106), [TW(114), TW(126), TW(139)]
T_PRIX = [TW(117), TW(133), TW(142)]
T_GRAIN, T_LISSE, T_FERR = TW(150), TW(153), TW(159)
T_PARTAGE, T_COM, T_FIN, T_CB = TW(167), TW(180) - 0.1, TW(187) - 0.1, TW(198) - 0.1


def entete_marque(c, t):
    iw, ih = taille_img("logo-dy-blanc"); lw = 210
    image(c, "logo-dy-blanc", 70, 250 - lw * ih / iw / 2, lw, 0.9 * (1 - prog(t, T_CB - 0.1, 0.3)))


def titre(c, t, txt, t0, t1, y=440, cols=None, taille=96):
    if t < t0 - 0.1 or t > t1 + 0.3: return
    ts = ajuste(txt, 940, taille, "noir", -0.03)
    a = 1 - prog(t, t1 - 0.05, 0.25, entree)
    lettres(c, txt, 540, y - ts * 0.62, ts, t, t0 - 0.05, "masque", decal=0.022, duree=0.4, grad=True,
            cols=cols or [BLANC, "#E9E4F5"], alpha=a)


# ─────────────────────────────────────────── HOOK : le sac à plusieurs dizaines de milliers d'euros
def hook(c, t):
    if t > T_PEAUX + 0.3: return
    fin = prog(t, T_PEAUX - 0.3, 0.35, entree)
    with Calque(c, 1 - fin):
        part = prog(t, T_RESTE, 0.4, entreeSortie)
        a1 = 1 - prog(t, T_CHINE - 0.15, 0.25, entree)
        if a1 > 0:
            lettres(c, "DES DIZAINES DE", 540, 330, 92, t, -0.7, "ressort", grad=False, couleur=BLANC, decal=0.03, alpha=a1)
            lettres(c, "MILLIERS D'EUROS", 540, 440, 104, t, -0.55, "ressort", cols=[OR, OR2], decal=0.03, alpha=a1)
        if t > T_CHINE - 0.2:
            lettres(c, "EN CHINE :", 540, 330, 92, t, T_CHINE - 0.05, "masque", grad=False, couleur=BLANC, decal=0.03, alpha=1 - part)
            lettres(c, "BIEN MOINS CHER", 540, 440, 104, t, T_CHINE + 0.1, "masque", cols=[VERT, "#9FF5C4"], decal=0.03, alpha=1 - part)
        # la case : la photo des sacs finis, puis la vidéo du sac dans sa boîte
        y0 = 590
        sw = prog(t, T_MARQUES - 0.1, 0.35, entreeSortie)
        if sw < 1:
            case_media(c, t, CROCO_PHOTO, 140, y0, 800, 760, 1 - 0.7 * part, 1.0, zoom=1.05 + 0.03 * t, fy=0.55)
        if sw > 0:
            case_media(c, t, CROCO_BOITE, 140, y0, 800, 760, sw * (1 - 0.7 * part), mix(0.9, 1, sw), video_t0=T_MARQUES - 0.1, vitesse=1.3,
                       accent=OR if t > TW(17) else None)
        if part < 0.99:
            # le prix qui claque, puis barré quand on passe en Chine
            pa = entre(t, TW(5) - 0.1, 0.35, 2.4)
            etiquette_case(c, "€€€€€", 800, y0 + 60, pa * (1 - part), OR, 50)
            barre(c, 700, y0 + 80, 900, y0 + 40, prog(t, TW(28) - 0.05, 0.22, sortie) * (1 - part), ROUGE, 10)
            puce(c, "100 % crocodile", 540, y0 + 700, entre(t, TW(17) - 0.1, 0.4, 2.2) * (1 - part), "badge-check", OR, 36)
            puce(c, "Beaucoup moins cher", 540, y0 + 700, 0, None)
            bm = entre(t, TW(28) - 0.05, 0.4, 2.2)
            if bm > 0:
                with Calque(c, 1 - part):
                    etiquette_case(c, "− €€€", 800, y0 + 150, bm, VERT, 46)
        bouton_enregistre(c, t, T_ENR, 860, 1230 + 300 * part, 1 - part)
        # « reste jusqu'au bout » : la qualité originale sous cadenas, garée en haut à droite
    if t >= T_RESTE and t < T_Q[2] + 1.0:
        a = entre(t, T_RESTE, 0.5, 1.6)
        gare = prog(t, T_PEAUX - 0.5, 0.5, entreeSortie)
        ouvre = prog(t, TW(147), 0.3, sortie)
        cx, cy = mix(540, 880, gare), mix(900, 250, gare)
        cadenas(c, cx, cy, mix(0.4, 1.25, a) * mix(1, 0.29, gare), t, "L'ORIGINALE", ouvre, 1 - prog(t, TW(147) + 0.35, 0.3))
        eclats(c, cx, cy, t, TW(147), 14, 260, [OR, BLANC, OR2], graine=8)


# ─────────────────────────────────────────── les peaux, la confection
def peaux(c, t):
    g = Groupe(c, t, T_PEAUX - 0.3, T_MYTHE, ent="bas", sor="gauche")
    if not g.visible: return
    with g:
        titre(c, t, "CHOISIS TA PEAU", T_PEAUX, T_CONF)
        titre(c, t, "1 MOIS, COUSU MAIN", T_CONF, T_MYTHE + 1)
        sw = prog(t, T_CONF - 0.1, 0.4, entreeSortie)
        a = entre(t, T_PEAUX - 0.2, 0.45, 1.6)
        b = entre(t, T_TEL - 0.2, 0.45, 1.6)
        if sw < 1:
            with Calque(c, 1 - sw):
                case_media(c, t, CROCO_PEAUX, 90, 540, 440, 800, borne(a * 3), mix(0.6, 1, a), video_t0=T_PEAUX - 0.2, vitesse=0.8)
                case_media(c, t, CROCO_TYPES, 550, 540, 440, 800, borne(b * 3), mix(0.6, 1, b), video_t0=T_TEL - 0.2, vitesse=1.3,
                           accent=OR)
                puce(c, "Sur son téléphone", 760, 1290, entre(t, TW(46) - 0.1, 0.4, 2.2), "smartphone", OR, 32)
        if sw > 0:
            case_media(c, t, CROCO_PORTEF, 90, 540, 440, 800, sw, mix(0.85, 1, sw), video_t0=T_CONF - 0.1, vitesse=1.6)
            case_media(c, t, CROCO_BOITE, 550, 540, 440, 800, sw, mix(0.85, 1, sw), video_t0=T_CONF - 2.5, vitesse=1.2, accent=OR)
            puce(c, "1 mois", 310, 1290, entre(t, TW(52) - 0.1, 0.4, 2.2), "calendar", OR, 34)
            puce(c, "Cousu main", 770, 1290, entre(t, TW(55) - 0.1, 0.4, 2.2), "hand", OR, 34)


# ─────────────────────────────────────────── le mythe : Chine = pas cher, mauvaise qualité
def mythe(c, t):
    g = Groupe(c, t, T_MYTHE - 0.12, T_TOUT, ent="droite", sor="zoom")
    if not g.visible: return
    with g:
        titre(c, t, "ARRÊTE DE CROIRE", T_MYTHE, T_TOUT + 1)
        a = entre(t, TW(65) - 0.1, 0.45, 1.8)
        if a > 0:
            c.save(); c.translate(540, 700); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
            texte(c, "CHINE =", 0, -hauteurLigne(110) / 2, 110, BLANC, "noir", "centre", -0.03, borne(a * 3))
            c.restore()
        for k, (lab, t0) in enumerate([("PAS CHER", TW(71)), ("MAUVAISE QUALITÉ", TW(74))]):
            u = entre(t, t0 - 0.1, 0.45, 1.8)
            if u <= 0: continue
            y = 880 + k * 200
            c.save(); c.translate(540, y); c.scale(mix(0.5, 1, u), mix(0.5, 1, u))
            case(c, -430, -80, 860, 160, 30, borne(u * 3))
            ts = ajuste(lab, 760, 72, "noir")
            texte(c, lab, 0, -hauteurLigne(ts) / 2, ts, BLANC, "noir", "centre", -0.02, borne(u * 3))
            c.restore()
            barre(c, 140, y + 30, 940, y - 30, prog(t, t0 + 0.35, 0.22, sortie), ROUGE, 12)
        tampon_n(c, "FAUX", 800, 640, t, TW(75) + 0.15, ROUGE, 10, 64)


# ─────────────────────────────────────────── ils ont tout : c'est toi et ton budget
def tout(c, t):
    g = Groupe(c, t, T_TOUT - 0.12, T_SAC, ent="bas", sor="haut")
    if not g.visible: return
    with g:
        titre(c, t, "ILS ONT TOUT", T_TOUT, T_SAC + 1, cols=[OR, OR2])
        lignes = [("Pas cher", "€", TW(84), TW(86)), ("Moyen", "€€", TW(88), TW(90)), ("Top", "€€€", TW(92), TW(94)),
                  ("Originale", "€€€€", TW(97), TW(99))]
        for k, (lab, eur, t0, t_ok) in enumerate(lignes):
            u = entre(t, t0 - 0.15, 0.4, 1.8)
            if u <= 0: continue
            y = 560 + k * 165
            c.save(); c.translate((1 - u) * 260, 0)
            with Calque(c, borne(u * 3)):
                case(c, 90, y, 900, 140, 28, 1.0, accent=OR if k == 3 else None)
                texte(c, lab, 140, y + 70 - hauteurLigne(56) / 2, 56, BLANC, "noir", track=-0.02)
                texte(c, eur, 800, y + 70 - hauteurLigne(50) / 2, 50, OR, "noir", "droite", 0)
            c.restore()
            coche(c, 900, y + 70, 36, entre(t, t_ok - 0.05, 0.35, 2.4))
        b = entre(t, T_BUDGET - 0.1, 0.45, 2.0)
        if b > 0:
            etiquette_case(c, "TOI + TON BUDGET", 540, 1300, b, OR, 50)


# ─────────────────────────────────────────── sacoches, grain, ferrures
def sacoches(c, t):
    titre(c, t, "MÊME MODÈLE", T_SAC, T_Q[0] - 0.1, cols=[OR, OR2])
    titre(c, t, "3 QUALITÉS", T_Q[0], T_GRAIN, cols=[BLANC, "#E9E4F5"])
    trois_sacoches(c, t, T_SAC, T_Q[0], T_Q, T_PRIX, T_GRAIN)
    titre(c, t, "LE GRAIN", T_GRAIN, T_FERR, cols=[OR, OR2])
    titre(c, t, "TOUT EST PARFAIT", T_FERR, T_PARTAGE, cols=[VERT, "#9FF5C4"])
    grain(c, t, T_GRAIN, T_LISSE, T_FERR, T_PARTAGE)


def partage_s(c, t):
    g = Groupe(c, t, T_PARTAGE - 0.12, T_COM, ent="zoom", sor="zoom")
    if not g.visible: return
    with g:
        partage(c, t, T_PARTAGE, TW(171) - 0.05)


# ─────────────────────────────────────────── commentaire, puis ChinaBook par DROP&YOU
def fin(c, t):
    if t < T_COM - 0.05: return
    sc = prog(t, T_FIN - 0.1, 0.35, entreeSortie)
    if sc < 1:
        with Calque(c, 1 - sc):
            lettres(c, "DIS-MOI", 540, 560, 120, t, T_COM, "ressort", cols=[OR, OR2], decal=0.035)
            commentaire(c, t, T_COM, "Quelle qualité tu prends ?", ["La 1:1", "L'originale !", "Standard"], 900, 0.45)
    if t < T_FIN - 0.1: return
    logo_t = prog(t, T_CB - 0.1, 0.4, entreeSortie)
    # pour chaque budget
    for k, (lab, x) in enumerate([("€", 300), ("€€", 540), ("€€€", 780)]):
        u = entre(t, TW(192) + 0.1 * k, 0.4, 2.2)
        if u <= 0: continue
        c.save(); c.translate(x, mix(820, 560, logo_t)); c.scale(mix(0.4, 1, u) * mix(1, 0.7, logo_t), mix(0.4, 1, u) * mix(1, 0.7, logo_t))
        case(c, -100, -70, 200, 140, 30, borne(u * 3), accent=OR)
        texte(c, lab, 0, -hauteurLigne(60) / 2, 60, OR, "noir", "centre", 0, borne(u * 3))
        c.restore()
    pf = entre(t, TW(188) - 0.1, 0.4, 2.2)
    if pf > 0 and logo_t < 1:
        with Calque(c, 1 - logo_t):
            puce(c, "Fournisseurs validés", 540, 1040, pf, "badge-check", VERT, 40)
    if logo_t > 0:
        ul = entre(t, T_CB + 0.1, 0.5, 1.5)
        lueur(c, 540, 900, 600 * logo_t, "#6E48F0", 0.4)
        rayons(c, 540, 900, t, 900, 0.08 * logo_t, 14, "#9B83FF")
        iw, ih = taille_img("logo-chinabook-blanc"); lw = 800 * mix(0.6, 1, ul)
        image(c, "logo-chinabook-blanc", 540 - lw / 2, 870 - lw * ih / iw / 2, lw, borne(ul * 3))
        up = entre(t, TW(200) - 0.1, 0.45, 1.8)
        if up > 0:
            texte(c, "par", 540, 1030, 36, GRIS, "gras", "centre", 0, borne(up * 3))
            iw, ih = taille_img("logo-dy-blanc"); lw2 = 440 * mix(0.6, 1, up)
            image(c, "logo-dy-blanc", 540 - lw2 / 2, 1100, lw2, borne(up * 3))


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(0.05, "verre", -10)
son(TW(5) - 0.1, "ching", -7); son(TW(5), "impact_doux", -9)
son(T_MARQUES - 0.1, "whoosh", -10); son(TW(17) - 0.1, "check", -10)
son(T_CHINE - 0.15, "whoosh_bas", -8); son(TW(28) - 0.05, "croc", -8); son(TW(28), "ching", -9)
son(T_ENR - 0.15, "pop", -9); son(T_ENR + 0.35, "clic", -5); son(T_ENR + 0.38, "ching", -8); son(T_ENR + 0.4, "check", -9)
son(T_RESTE, "impact_doux", -6); son(T_RESTE + 0.05, "montee", -12)
son(T_PEAUX - 0.5, "whoosh_long", -9); son(T_PEAUX - 0.2, "verre", -9); son(T_TEL - 0.2, "verre", -10); son(TW(46) - 0.1, "pop", -10)
son(T_CONF - 0.1, "whoosh", -9); son(TW(52) - 0.1, "pop", -10); son(TW(55) - 0.1, "pop", -10)
son(T_MYTHE - 0.15, "whoosh_bas", -7); son(TW(65) - 0.1, "impact_doux", -8)
for t0 in [TW(71), TW(74)]: son(t0 - 0.1, "pop", -10); son(t0 + 0.35, "croc", -8)
son(TW(75) + 0.05, "tampon", -5)
son(T_TOUT - 0.15, "whoosh", -7)
for t0, tok in [(TW(84), TW(86)), (TW(88), TW(90)), (TW(92), TW(94)), (TW(97), TW(99))]:
    son(t0 - 0.15, "swipe", -11); son(tok - 0.05, "check", -9)
son(T_BUDGET - 0.1, "ching", -8)
son(T_SAC - 0.2, "whoosh_long", -9); son(T_SAC, "impact_doux", -8)
for k in range(3): son(T_Q[0] - 0.15 + 0.08 * k, "whoosh_court", -12)
for t0 in T_Q: son(t0 - 0.1, "pop", -10)
for t0 in T_PRIX: son(t0 - 0.05, "ching", -9)
son(TW(147), "clic", -6); son(TW(147) + 0.02, "impact", -6)
son(T_GRAIN - 0.2, "whoosh", -8); son(T_GRAIN + 0.4, "check", -10)
son(T_LISSE - 0.15, "pop", -10); son(T_LISSE + 0.25, "croc", -10); son(T_LISSE + 0.35, "croc", -11)
son(T_FERR - 0.15, "whoosh_bas", -8); son(T_FERR + 0.1, "check", -9); son(T_FERR + 0.6, "check", -9)
son(T_PARTAGE - 0.1, "whoosh_bas", -7); son(T_PARTAGE + 0.5, "impact_doux", -9); son(TW(171) - 0.05, "whoosh_court", -9)
son(TW(171) + 0.5, "message_in", -8)
son(T_COM, "message", -9)
for k in range(1, 4):
    for j in range(3): son(T_COM + 0.5 + 0.45 * k + 0.05 * j, "frappe", -17)
son(T_FIN - 0.1, "whoosh", -9); son(TW(188) - 0.1, "check", -10)
for k in range(3): son(TW(192) + 0.1 * k, "pop", -12)
son(T_CB - 0.1, "montee", -11); son(T_CB + 0.1, "impact", -5); son(T_CB + 0.12, "verre", -9); son(TW(200) - 0.1, "pop", -9)

for a, b in [(0.0, 0.25), (T_CHINE - 0.15, T_CHINE + 0.2), (T_PEAUX - 0.6, T_PEAUX + 0.2), (T_MYTHE - 0.2, T_MYTHE + 0.3),
             (T_TOUT - 0.2, T_TOUT + 0.3), (T_PARTAGE - 0.2, T_PARTAGE + 0.3), (T_CB - 0.1, T_CB + 0.4)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(5) - 0.1, OR, 0.08), (T_ENR + 0.38, OR, 0.08), (TW(147), OR, 0.12), (T_CB + 0.1, "#FFFFFF", 0.14)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_noir(c, t, battement(t, T_CB + 0.1, 1, 0.6) - 1)
    entete_marque(c, t)
    hook(c, t); peaux(c, t); mythe(c, t); tout(c, t); sacoches(c, t); partage_s(c, t); fin(c, t)
    K.dessine_eclairs(c, t)
    if not (T_COM - 0.05 < t < T_FIN - 0.1) and t < T_CB: SOUS.dessine(c, t, BLANC)
