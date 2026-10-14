"""DA-M06 « Laquelle ? » — pub DYOU Agency pour vendre des vidéos motion design (style clair du site, 14/10/2026).

Hook (comparaison, le spectateur choisit) : deux téléphones, le même message ; à gauche une pub fixe, grise,
à droite la même en motion. « Laquelle tu regardes jusqu'au bout ? » — la barre de visionnage de la pub fixe
s'arrête, l'autre va au bout. « Évidemment, celle qui bouge » : la fixe tombe, on plonge dans l'écran de l'autre.
Corps commun avec DA-M07 (moteur/studio.py) : être à la page → motion design → captivé, comprend, agit →
croissance → vidéo explicative sur le site → script, animation, 3 ou 4 accroches → 290 € TTC → devis.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *

DUREE = 30.2
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

M = dict(b1=TW(13), produit=TW(17), service=TW(19), message=TW(24), oblige=TW(26), page=TW(30), b2=TW(31), motion=TW(35),
         captive=TW(40), regarde=TW(42), comprend=TW(44), action=TW(47), b3=TW(50), titre_b3="RÉSULTAT", attention=TW(52),
         demandes=TW(55), clients=TW(58), b4=TW(59), site=TW(66), expliquer=TW(68), facon=TW(70), simple=TW(73), b5=TW(74),
         script=TW(77), anime=TW(79), accroches=TW(84), tester=TW(89), prix=TW(90), deux=TW(93), qvd=TW(95), euros=TW(96),
         devis=TW(97), url=TW(101))
SOUS = sous_titres(K, fusions={(93, 94, 95, 96): "290 €.", (101, 102, 103, 104, 105): "dyou-agency.com."})

T_LAQ, T_BOUT, T_EVID, T_BOUGE, T_B1 = TW(4), TW(8), TW(9), TW(12), TW(13)


# ─────────────────────────────────────────── les deux écrans du hook
def ecran_fixe(c, x, y, w, h, t):
    """la pub « classique » : grise, plate, rien ne bouge"""
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#ECEAF0"))
    rrect(c, x + 30, y + 120, w - 60, w - 60, 18, "#D8D5DE")
    icone(c, "image", x + w / 2, y + 120 + (w - 60) / 2, 90, "#B2AEBB", 1.6)
    yy = y + 120 + w - 30
    texte(c, "Cuisines Morel", x + 34, yy, 34, "#5E5968", "fort", track=0)
    texte(c, "Cuisine sur mesure", x + 34, yy + 52, 25, "#8A8594", "demi", track=0)
    texte(c, "Devis gratuit", x + 34, yy + 88, 25, "#8A8594", "demi", track=0)
    texte(c, "Tél. 06 •• •• •• ••", x + 34, yy + 124, 23, "#A09BAA", "demi", track=0)


def ecran_motion(c, x, y, w, h, t):
    """la même pub en motion design : tout vit"""
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pgrad(x, y, x + w, y + h, GRAD_VIF))
    cx, cy = x + w / 2, y + h * 0.42
    for k in range(3):
        r = 120 + 60 * k + 10 * math.sin(t * 3 + k)
        c.save(); c.translate(cx, cy); c.rotate(t * (40 + 25 * k) * (-1) ** k)
        rrect(c, -r, -r, 2 * r, 2 * r, r * 0.45, None, 1.0, None, "#FFFFFF", 3)
        c.restore()
    for k in range(5):
        a = t * 1.3 + k * 1.26
        etoile4(c, cx + 150 * math.cos(a), cy + 190 * math.sin(a), 16 + 6 * math.sin(t * 5 + k), "#FFFFFF", 0.85, t * 2)
    tl = (t + 0.4) % 1.8
    lettres(c, "TA", cx, cy - 110, 70, tl, 0.0, "ressort", grad=False, couleur="#FFFFFF", decal=0.05)
    lettres(c, "CUISINE", cx, cy - 40, 70, tl, 0.1, "ressort", grad=False, couleur="#FFFFFF", decal=0.04)
    lettres(c, "SUR MESURE", cx, cy + 40, 40, tl, 0.35, "masque", grad=False, couleur="#E3D6FF", decal=0.03)
    pu = 1 + 0.06 * math.sin(t * 7)
    pill(c, "Devis offert", cx, y + h * 0.74, 26, "blanc", "sparkles", 1.0, pu)
    barre_progression(c, x + 40, y + h - 60, w - 80, (t * 0.45) % 1, 8, ["#FFFFFF", "#FFFFFF"], "#FFFFFF40", tete=False)


# ─────────────────────────────────────────── hook
def hook(c, t):
    so = prog(t, T_EVID - 0.1, 0.35, entreeSortie)
    lettres(c, "MÊME MESSAGE.", 540, 190 - 80 * so, 86, t, -0.3, "ressort", grad=False, decal=0.025, alpha=1 - so)
    lettres(c, "2 VIDÉOS.", 540, 290 - 80 * so, 86, t, TW(2) - 0.12, "masque", decal=0.04, alpha=1 - so)
    chute = prog(t, T_EVID - 0.02, 0.75, entree)
    gris = prog(t, T_EVID - 0.05, 0.25, sortie)
    cen = prog(t, T_EVID + 0.05, 0.65, entreeSortie)
    zoom = prog(t, T_B1 - 0.42, 0.45, entree)
    PW, PH, PY = 400, 800, 880
    # A : la pub fixe
    ax = 290 - 120 * chute; ay = PY + 1500 * chute ** 1.6
    if chute < 1:
        with Espace(c, ax, ay, ry=10, rz=-24 * chute):
            telephone_s(c, ax, ay, PW, PH, lambda cc, x, y, w, h: ecran_fixe(cc, x, y, w, h, t), gris=gris)
        with Calque(c, 1 - prog(t, T_EVID, 0.2)):
            pill(c, "A", 290, PY - PH / 2 - 44, 30, "blanc", None, 1.0, entre(t, -0.1, 0.4, 2))
            u = 0.12 * prog(t, TW(6), T_BOUT - TW(6), sortie)
            barre_progression(c, 140, PY + PH / 2 + 46, 300, u, 14, [S["grisClair"], S["gris"]])
            z = entre(t, T_BOUT + 0.02, 0.4, 2.4)
            if z > 0: pill(c, "Zappée", 290, PY + PH / 2 + 100, 26, "rouge", "x", borne(z * 3), mix(0.4, 1, z), rot=-4)
    # B : la pub en motion
    bx = mix(790, 540, cen); by = mix(PY, 900, cen)
    sx, sy = secousse(t, T_BOUGE + 0.05, 16)
    sc = mix(1, 1.32, cen) * mix(1, 4.6, zoom) * battement(t, T_BOUGE + 0.05, 0.06, 0.3)
    with Espace(c, bx + sx, by + sy, ry=mix(-10, 0, cen), s=sc):
        telephone_s(c, bx + sx, by + sy, PW, PH, lambda cc, x, y, w, h: ecran_motion(cc, x, y, w, h, t))
    with Calque(c, 1 - prog(t, T_EVID, 0.2)):
        pill(c, "B", 790, PY - PH / 2 - 44, 30, "grad", None, 1.0, entre(t, 0.0, 0.4, 2))
        u = prog(t, TW(6), T_BOUT + 0.35 - TW(6), sortie)
        barre_progression(c, 640, PY + PH / 2 + 46, 300, u, 14)
        z = entre(t, T_BOUT + 0.3, 0.4, 2.4)
        if z > 0: pill(c, "Vue en entier", 790, PY + PH / 2 + 100, 26, "vert", "check", borne(z * 3), mix(0.4, 1, z), rot=3)
    # « Laquelle ? » : un point d'interrogation entre les deux, et le curseur qui hésite
    q = entre(t, T_LAQ - 0.1, 0.45, 2.2) * (1 - prog(t, T_EVID - 0.05, 0.2, entree))
    if q > 0:
        c.save(); c.translate(540, 760 + 14 * math.sin(t * 5)); c.rotate(10 * math.sin(t * 3)); c.scale(q, q)
        lueur_s(c, 0, 0, 160, S["violetVif"], 0.3)
        texte_grad(c, "?", 0, -110, 220, "noir", "centre")
        c.restore()
        hx = 540 + 230 * math.sin((t - T_LAQ) * 5.5)
        curseur(c, hx, 1020 + 30 * math.cos((t - T_LAQ) * 5.5), 1.1, borne(q * 2))
    eclats(c, bx, by, t, T_BOUGE + 0.05, 14, 520, graine=2)
    onde(c, bx, by, t, T_BOUGE + 0.05, 200, 700, S["violetVif"], 10, 0.6)


# ─────────────────────────────────────────── sons du hook
son(0.0, "impact", -7); son(0.02, "whoosh_court", -12); son(0.0, "pop", -13); son(0.1, "pop", -15)
son(TW(2) - 0.12, "whoosh_court", -12)
son(T_LAQ - 0.1, "pop", -9); son(T_LAQ, "montee", -16)
for k in range(5): son(T_LAQ + 0.15 + 0.2 * k, "clic", -21)
son(TW(6), "tick", -16); son(T_BOUT + 0.02, "croc", -9); son(T_BOUT + 0.3, "check", -11)
son(T_EVID - 0.02, "whoosh_bas", -9); son(T_EVID + 0.4, "impact_doux", -12)
son(T_BOUGE + 0.05, "impact", -6); son(T_BOUGE + 0.08, "ching", -12)
son(T_B1 - 0.42, "whoosh_long", -8)
sons_corps(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.2), (T_EVID - 0.05, T_EVID + 0.55), (T_B1 - 0.45, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_BOUGE + 0.05, S["violetVif"], 0.10), (M["page"] + 0.12, "#FFFFFF", 0.25), (M["captive"] + 0.35, S["violetVif"], 0.08),
                    (M["euros"] - 0.06, "#FFFFFF", 0.22), (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    fond_studio(c, t, battement(t, M["captive"] + 0.35, 1, 0.5) - 1)
    scene_b1(c, t, M); scene_b2(c, t, M); scene_b3(c, t, M); scene_b4(c, t, M); scene_b5(c, t, M)
    scene_cta(c, t, M, DUREE)
    scene_prix(c, t, M)
    if t < T_B1 + 0.35:
        r = prog(t, T_B1 - 0.1, 0.42, sortie) * 1500
        c.save()
        if r > 1:
            pth = skia.Path(); pth.addCircle(540, 900, r); c.clipPath(pth, skia.ClipOp.kDifference, True)
        hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    if t < M["prix"] - 0.25:
        with Calque(c, 1 - prog(t, T_B1 - 0.55, 0.15) if t < T_B1 - 0.1 else 1.0):      # pas de sous-titre sur l'écran qui plonge
            SOUS.dessine(c, t, S["encre"])
