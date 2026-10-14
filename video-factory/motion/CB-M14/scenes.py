"""CB-M14 « Arrête de dire que la Chine, c'est de la mauvaise qualité » — organique DROP&YOU (14/10/2026), voix You,
4 mots/s, style noir à cases fines. Même sujet que CB-M13, autre hook : on ouvre sur les trois sacoches (même modèle,
trois prix, trois qualités), le crocodile devient la boucle ouverte (« le plus fou »), fin sur les avis clients DROP&YOU.
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
DUREE = round(K.timing["duree_voix"] + 1.8, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresEncre(K, fusions={(52, 53): "120", (55, 56): "150", (66, 67, 68, 69): "1:1,", (71, 72): "200",
                                  (74, 75, 76): "250", (83, 84): "300", (193, 194, 195): "DROP&YOU."},
                       y=1440, larg=900, taille=54, fam="gras", max_mots=5)

PHOTO_DESSUS = "photos/sacs/sacoches-3-qualites-dessus"
CROCO_PHOTO = "photos/croco/croco-deux-sacs-finis"
CROCO_BOITE = "videos/croco/croco-sac-fini-boite"
CROCO_PEAUX = "videos/croco/croco-peaux-telephone-defile"
CROCO_TYPES = "videos/croco/croco-types-de-peaux-comparatif"
CROCO_PORTEF = "videos/croco/croco-portefeuille-violet"
AVIS = [("photos/avis/avis-sac-beige-matelasse", 0.42), ("photos/avis/avis-pochette-noire-matelassee", 0.45),
        ("photos/avis/avis-sacoche-nylon-noire", 0.45), ("photos/avis/avis-claquettes-noires", 0.55)]

T_ENR, T_RESTE = TW(21), TW(28) - 0.1
T_Q, T_PRIX = [TW(43), TW(61), TW(78)], [TW(52), TW(71), TW(83)]
T_GRAIN, T_LISSE, T_FERR = TW(94), TW(97), TW(109)
T_PARTAGE, T_BUDGET, T_FOU = TW(116), TW(125), TW(132)
T_CROCO, T_PRIXC, T_PEAU, T_MOIS = TW(136), TW(149), TW(154), TW(158)
T_COM, T_FIN, T_CLIENTS, T_DY = TW(170) - 0.1, TW(177) - 0.1, TW(188), TW(193) - 0.1


def entete_marque(c, t):
    iw, ih = taille_img("logo-dy-blanc"); lw = 210
    image(c, "logo-dy-blanc", 70, 250 - lw * ih / iw / 2, lw, 0.9 * (1 - prog(t, T_DY - 0.1, 0.3)))


def titre(c, t, txt, t0, t1, y=440, cols=None, taille=96):
    if t < t0 - 0.1 or t > t1 + 0.3: return
    ts = ajuste(txt, 940, taille, "noir", -0.03)
    a = 1 - prog(t, t1 - 0.05, 0.25, entree)
    lettres(c, txt, 540, y - ts * 0.62, ts, t, t0 - 0.05, "masque", decal=0.022, duree=0.4, grad=True,
            cols=cols or [BLANC, "#E9E4F5"], alpha=a)


# ─────────────────────────────────────────── HOOK
def hook(c, t):
    if t > T_Q[0] + 0.3: return
    fin = prog(t, T_Q[0] - 0.35, 0.35, entree)
    with Calque(c, 1 - fin):
        part = prog(t, T_RESTE, 0.4, entreeSortie)
        lettres(c, "ARRÊTE DE DIRE", 540, 330, 92, t, -0.7, "ressort", grad=False, couleur=BLANC, decal=0.03, alpha=1 - part)
        lettres(c, "CHINE = CHEAP", 540, 440, 108, t, -0.55, "ressort", cols=[OR, OR2], decal=0.03, alpha=1 - part)
        barre(c, 150, 520, 930, 450, prog(t, TW(9), 0.22, sortie) * (1 - part), ROUGE, 12)
        y0 = 590
        case_media(c, t, PHOTO_DESSUS, 140, y0, 800, 760, 1 - 0.7 * part, 1.0, zoom=1.08 + 0.025 * t, fy=0.5,
                   accent=OR if t > TW(15) else None)
        if part < 0.99:
            with Calque(c, 1 - part):
                for k, (lab, ic, t0) in enumerate([("Même modèle", "copy", TW(15)), ("3 prix", "euro", TW(17)), ("3 qualités", "layers", TW(19))]):
                    puce(c, lab, 140 + 40 + largeur(lab, 34, "gras") / 2 + 50, y0 + 70 + k * 95, entre(t, t0 - 0.1, 0.4, 2.2), ic, OR, 34)
                tampon_n(c, "FAUX", 760, 1000, t, TW(10) + 0.2, ROUGE, 10, 72)
        bouton_enregistre(c, t, T_ENR, 860, 1230 + 300 * part, 1 - part)
    # « je te montre le plus fou » : sous cadenas, garé en haut à droite jusqu'à « Et le plus fou »
    if T_RESTE <= t < T_FOU + 1.0:
        a = entre(t, T_RESTE, 0.5, 1.6)
        gare = prog(t, T_Q[0] - 0.5, 0.5, entreeSortie)
        ouvre = prog(t, T_FOU + 0.2, 0.3, sortie)
        cx, cy = mix(540, 880, gare), mix(900, 250, gare)
        cadenas(c, cx, cy, mix(0.4, 1.25, a) * mix(1, 0.29, gare), t, "LE PLUS FOU", ouvre, 1 - prog(t, T_FOU + 0.55, 0.3))
        eclats(c, cx, cy, t, T_FOU + 0.2, 14, 260, [OR, BLANC, OR2], graine=8)


# ─────────────────────────────────────────── trois qualités, grain, ferrures
def sacoches(c, t):
    titre(c, t, "3 QUALITÉS", T_Q[0], T_GRAIN, cols=[BLANC, "#E9E4F5"])
    trois_sacoches(c, t, T_Q[0] - 0.4, T_Q[0], T_Q, T_PRIX, T_GRAIN)
    titre(c, t, "LE GRAIN", T_GRAIN, T_FERR, cols=[OR, OR2])
    titre(c, t, "TOUT EST PARFAIT", T_FERR, T_PARTAGE, cols=[VERT, "#9FF5C4"])
    grain(c, t, T_GRAIN, T_LISSE, T_FERR, T_PARTAGE)
    if T_LISSE < t < T_FERR:
        with Calque(c, 1 - prog(t, T_FERR - 0.2, 0.2, entree)):
            tampon_n(c, "ÇA FAIT FAUX", 540, 1190, t, TW(103) + 0.1, ROUGE, -6, 46)


def partage_s(c, t):
    g = Groupe(c, t, T_PARTAGE - 0.12, T_BUDGET, ent="zoom", sor="zoom")
    if not g.visible: return
    with g:
        partage(c, t, T_PARTAGE, TW(120) - 0.05, "Revendeur")


def budget(c, t):
    g = Groupe(c, t, T_BUDGET - 0.12, T_FOU, ent="bas", sor="recul")
    if not g.visible: return
    with g:
        titre(c, t, "EN CHINE", T_BUDGET, T_FOU + 1)
        for k, (lab, x) in enumerate([("€", 260), ("€€", 540), ("€€€", 820)]):
            u = entre(t, T_BUDGET + 0.15 + 0.1 * k, 0.4, 2.2)
            if u <= 0: continue
            c.save(); c.translate(x, 760); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            case(c, -120, -100, 240, 200, 34, borne(u * 3), accent=OR if k == 2 else None)
            texte(c, lab, 0, -hauteurLigne(76) / 2, 76, OR, "noir", "centre", 0, borne(u * 3))
            c.restore()
            coche(c, x + 100, 680, 32, entre(t, T_BUDGET + 0.5 + 0.1 * k, 0.35, 2.4))
        etiquette_case(c, "TOI + TON BUDGET", 540, 1040, entre(t, TW(127) - 0.1, 0.45, 2.0), OR, 54)


# ─────────────────────────────────────────── le plus fou : le crocodile
def croco(c, t):
    if t < T_FOU - 0.2: return
    g = Groupe(c, t, T_FOU - 0.2, T_COM, ent="grand", sor="gauche")
    if not g.visible: return
    with g:
        titre(c, t, "LE PLUS FOU", T_FOU, T_CROCO, cols=[OR, OR2])
        titre(c, t, "VRAIE PEAU DE CROCODILE", T_CROCO, T_PRIXC, cols=[BLANC, "#E9E4F5"])
        titre(c, t, "DES DIZAINES DE MILLIERS D'€", T_PRIXC, T_PEAU, cols=[OR, OR2])
        titre(c, t, "CHOISIS TA PEAU", T_PEAU, T_MOIS, cols=[BLANC, "#E9E4F5"])
        titre(c, t, "1 MOIS, COUSU MAIN", T_MOIS, T_COM + 1, cols=[OR, OR2])
        sp = prog(t, T_PEAU - 0.15, 0.4, entreeSortie)
        a = entre(t, T_FOU + 0.1, 0.5, 1.5)
        if sp < 1:
            with Calque(c, 1 - sp):
                sw = prog(t, T_CROCO - 0.1, 0.35, entreeSortie)
                case_media(c, t, CROCO_BOITE, 140, 560, 800, 780, borne(a * 3) * (1 - sw), mix(0.6, 1, a), video_t0=T_FOU, vitesse=1.3)
                case_media(c, t, CROCO_PHOTO, 140, 560, 800, 780, sw, mix(0.92, 1, sw), zoom=1.05 + 0.04 * max(0, t - T_CROCO), fy=0.55,
                           accent=OR)
                etiquette_case(c, "€€€€€", 800, 620, entre(t, T_PRIXC - 0.05, 0.35, 2.4), OR, 50)
                puce(c, "100 % crocodile", 540, 1290, entre(t, TW(142) - 0.1, 0.4, 2.2), "badge-check", OR, 36)
        if sp > 0:
            sw2 = prog(t, T_MOIS - 0.1, 0.4, entreeSortie)
            case_media(c, t, CROCO_PEAUX if sw2 < 0.5 else CROCO_PORTEF, 90, 540, 440, 800, sp, mix(0.85, 1, sp),
                       video_t0=(T_PEAU - 0.15) if sw2 < 0.5 else T_MOIS, vitesse=0.9 if sw2 < 0.5 else 1.6)
            case_media(c, t, CROCO_TYPES if sw2 < 0.5 else CROCO_BOITE, 550, 540, 440, 800, sp, mix(0.85, 1, sp),
                       video_t0=(T_PEAU - 0.15) if sw2 < 0.5 else T_MOIS - 3.0, vitesse=1.3, accent=OR)
            if sw2 > 0:
                with Calque(c, sw2):
                    puce(c, "1 mois", 310, 1290, entre(t, TW(160) - 0.1, 0.4, 2.2), "calendar", OR, 34)
                    puce(c, "Cousu main", 770, 1290, entre(t, TW(166) - 0.1, 0.4, 2.2), "hand", OR, 34)


# ─────────────────────────────────────────── commentaire, avis clients, DROP&YOU
def fin(c, t):
    if t < T_COM - 0.05: return
    sc = prog(t, T_FIN - 0.1, 0.35, entreeSortie)
    if sc < 1:
        with Calque(c, 1 - sc):
            lettres(c, "DIS-MOI", 540, 560, 120, t, T_COM, "ressort", cols=[OR, OR2], decal=0.035)
            commentaire(c, t, T_COM, "Tu y crois ?", ["Oui !", "Grave", "Je veux le même"], 900, 0.4)
    if t < T_FIN - 0.1: return
    titre(c, t, "SANS TE PRENDRE LA TÊTE", T_FIN, T_CLIENTS - 0.1, cols=[BLANC, "#E9E4F5"])
    titre(c, t, "NOS CLIENTS", T_CLIENTS - 0.1, T_DY, cols=[OR, OR2])
    logo_t = prog(t, T_DY - 0.1, 0.4, entreeSortie)
    # les captures des clients, en éventail
    for k, (nom, fy) in enumerate(AVIS):
        u = entre(t, T_FIN + 0.25 + 0.32 * k, 0.5, 1.6)
        if u <= 0: continue
        rot = (-14, -5, 5, 14)[k]
        x = 540 + (k - 1.5) * 190
        y = 900 + abs(k - 1.5) * 40 - 300 * logo_t
        c.save(); c.translate(x, y + 260 * (1 - u)); c.rotate(rot * u); c.scale(mix(0.6, 1, u) * mix(1, 0.62, logo_t), mix(0.6, 1, u) * mix(1, 0.62, logo_t))
        case_media(c, t, nom, -170, -300, 340, 600, borne(u * 3), 1.0, zoom=1.0, fy=fy, accent=OR if t > T_CLIENTS else None, pad=8, r=24)
        c.restore()
    for k in range(5):
        u = entre(t, T_CLIENTS + 0.06 * k, 0.35, 2.4)
        if u > 0 and logo_t < 1:
            icone(c, "star", 540 + (k - 2) * 70, 1290, 56 * u, OR, 2.4, 1 - logo_t)
    if logo_t > 0:
        ul = entre(t, T_DY + 0.1, 0.5, 1.5)
        lueur(c, 540, 1120, 600 * logo_t, OR, 0.22)
        rayons(c, 540, 1120, t, 900, 0.07 * logo_t, 14, OR2)
        iw, ih = taille_img("logo-dy-blanc"); lw = 720 * mix(0.6, 1, ul)
        image(c, "logo-dy-blanc", 540 - lw / 2, 1110 - lw * ih / iw / 2, lw, borne(ul * 3))


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(0.05, "verre", -10)
son(TW(9), "croc", -7); son(TW(10) + 0.13, "tampon", -5)
for t0 in [TW(15), TW(17), TW(19)]: son(t0 - 0.1, "pop", -10)
son(T_ENR - 0.15, "pop", -9); son(T_ENR + 0.35, "clic", -5); son(T_ENR + 0.38, "ching", -8); son(T_ENR + 0.4, "check", -9)
son(T_RESTE, "impact_doux", -6); son(T_RESTE + 0.05, "montee", -12)
son(T_Q[0] - 0.5, "whoosh_long", -9)
for k in range(3): son(T_Q[0] - 0.15 + 0.08 * k, "whoosh_court", -12)
for t0 in T_Q: son(t0 - 0.1, "pop", -10)
for t0 in T_PRIX: son(t0 - 0.05, "ching", -9)
son(T_GRAIN - 0.2, "whoosh", -8); son(T_GRAIN + 0.4, "check", -10)
son(T_LISSE - 0.15, "pop", -10); son(T_LISSE + 0.25, "croc", -10); son(T_LISSE + 0.35, "croc", -11); son(TW(103) + 0.13, "tampon", -6)
son(T_FERR - 0.15, "whoosh_bas", -8); son(T_FERR + 0.1, "check", -9); son(T_FERR + 0.6, "check", -9)
son(T_PARTAGE - 0.1, "whoosh_bas", -7); son(T_PARTAGE + 0.5, "impact_doux", -9); son(TW(120) - 0.05, "whoosh_court", -9)
son(TW(120) + 0.5, "message_in", -8)
son(T_BUDGET - 0.15, "whoosh", -8)
for k in range(3): son(T_BUDGET + 0.15 + 0.1 * k, "pop", -11); son(T_BUDGET + 0.5 + 0.1 * k, "check", -13)
son(TW(127) - 0.1, "ching", -8)
son(T_FOU - 0.2, "whoosh_long", -8); son(T_FOU + 0.2, "clic", -5); son(T_FOU + 0.22, "impact", -5); son(T_FOU + 0.25, "ching", -8)
son(T_CROCO - 0.1, "whoosh", -9); son(TW(142) - 0.1, "check", -10); son(T_PRIXC - 0.05, "ching", -7); son(T_PRIXC, "impact_doux", -9)
son(T_PEAU - 0.15, "whoosh_bas", -8); son(T_MOIS - 0.1, "whoosh", -9); son(TW(160) - 0.1, "pop", -10); son(TW(166) - 0.1, "pop", -10)
son(T_COM, "message", -9)
for k in range(1, 4):
    for j in range(3): son(T_COM + 0.5 + 0.4 * k + 0.05 * j, "frappe", -17)
son(T_FIN - 0.1, "whoosh", -9)
for k in range(4): son(T_FIN + 0.25 + 0.32 * k, "swipe", -11)
for k in range(5): son(T_CLIENTS + 0.06 * k, "blip", -14)
son(T_DY - 0.1, "montee", -11); son(T_DY + 0.1, "impact", -5); son(T_DY + 0.12, "ching", -9)

for a, b in [(0.0, 0.25), (T_Q[0] - 0.5, T_Q[0] + 0.3), (T_PARTAGE - 0.2, T_PARTAGE + 0.3), (T_BUDGET - 0.2, T_BUDGET + 0.3),
             (T_FOU - 0.2, T_FOU + 0.4), (T_PEAU - 0.2, T_PEAU + 0.3), (T_FIN - 0.1, T_FIN + 0.3), (T_DY - 0.1, T_DY + 0.4)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(9), ROUGE, 0.08), (T_ENR + 0.38, OR, 0.08), (T_FOU + 0.22, OR, 0.12), (T_DY + 0.1, "#FFFFFF", 0.14)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_noir(c, t, battement(t, T_DY + 0.1, 1, 0.6) - 1)
    entete_marque(c, t)
    hook(c, t); sacoches(c, t); partage_s(c, t); budget(c, t); croco(c, t); fin(c, t)
    K.dessine_eclairs(c, t)
    if not (T_COM - 0.05 < t < T_FIN - 0.1) and t < T_DY: SOUS.dessine(c, t, BLANC)
