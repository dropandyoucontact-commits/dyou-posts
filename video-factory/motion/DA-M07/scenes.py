"""DA-M07 « 3 secondes » — pub DYOU Agency pour vendre des vidéos motion design (style clair du site, 14/10/2026).

Hook (fil qui casse) : un compte à rebours 3-2-1 dans un anneau qui se vide, « Ton client te donne trois
secondes. Après, il scrolle. » — et la vidéo elle-même part vers le haut comme si on la faisait défiler, une pub
grise arrive dessous. « Sauf si ça bouge » : elle revient en force, ÇA BOUGE explose à l'écran.
Corps commun avec DA-M06 (moteur/studio.py), texte légèrement différent (les algorithmes repèrent les doublons).
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *

DUREE = 30.7
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

M = dict(b1=TW(13), produit=TW(17), service=TW(19), message=TW(24), oblige=TW(26), page=TW(30), b2=TW(31), motion=TW(34),
         captive=TW(37), regarde=TW(40), comprend=TW(42), action=TW(48), b3=TW(51), titre_b3="LA DIFFÉRENCE", attention=TW(56),
         demandes=TW(59), clients=TW(62), b4=TW(63), site=TW(66), expliquer=TW(68), facon=TW(70), simple=TW(73),
         long_texte=TW(74), b5=TW(78), script=TW(81), anime=TW(83), accroches=TW(87), tester=TW(91), prix=TW(92),
         deux=TW(95), qvd=TW(97), euros=TW(98), devis=TW(99), url=TW(103))
SOUS = sous_titres(K, fusions={(4, 5): "3 secondes.", (95, 96, 97, 98): "290 €.", (103, 104, 105, 106, 107): "dyou-agency.com."})

T_2, T_1 = TW(6) - 0.05, TW(7) - 0.05          # « Après » → 2, « il » → 1
T_SW = TW(8) - 0.1                               # « scrolle » : la vidéo part vers le haut
T_SNAP = TW(9) - 0.1                             # « Sauf » : elle revient
T_B1 = TW(13)


# ─────────────────────────────────────────── le contenu « défilable »
def compte(c, t):
    """compte à rebours dans un anneau qui se vide"""
    cx, cy = 540, 860
    a = entre(t, -0.35, 0.5, 1.4)
    R = 300
    lueur_s(c, cx, cy, 520, S["violetVif"], 0.18)
    anneau(c, cx, cy, R, S["lavande"], 34)
    rest = 1 - borne(t / (T_SW + 0.1))
    arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), -90, -360 * rest)
    cols = GRAD_VIF if t < T_1 else [S["rouge"], "#FF7A59", S["rouge"]]
    pa = pgrad(cx - R, cy - R, cx + R, cy + R, cols); pa.setStyle(skia.Paint.kStroke_Style); pa.setStrokeWidth(34); pa.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawPath(arc, pa)
    ang = math.radians(-90 - 360 * rest)
    disque(c, cx + R * math.cos(ang), cy + R * math.sin(ang), 24, "#FFFFFF", 1.0, (6, 16, 0.2))
    for j in range(12):
        aa = j * math.pi / 6
        trait(c, cx + (R - 54) * math.cos(aa), cy + (R - 54) * math.sin(aa), cx + (R - 70) * math.cos(aa), cy + (R - 70) * math.sin(aa), S["grisClair"], 4)
    # le chiffre : l'ancien part vers le haut, le nouveau monte de dessous
    taille = 380
    for (n, t_on, t_off) in [("3", -9, T_2), ("2", T_2, T_1), ("1", T_1, 99)]:
        if t < t_on - 0.01 or t > t_off + 0.25: continue
        u = prog(t, t_on, 0.3, sortieExpo) if t_on > 0 else a
        o = prog(t, t_off, 0.22, entree)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(cx - 240, cy - 230, 480, 460))
        flou_calque(c, 10 * o + 8 * (1 - min(1, u * 1.5)), (1 - o))
        texte_grad(c, n, cx, cy - hauteurLigne(taille) / 2 + 300 * (1 - u) - 300 * o, taille, "noir", "centre", -0.04,
                   cols=GRAD if n != "1" else [S["rouge"], "#FF7A59"])
        c.restore(); c.restore()
    b = entre(t, TW(1) - 0.1, 0.4, 2.2)
    pill(c, "Ton client", 540, 390, 34, "blanc", "eye", borne(b * 3), mix(0.4, 1, b), rot=-3)
    lettres(c, "SECONDES", 540, 1200, 110, t, TW(5) - 0.2, "masque", decal=0.03, duree=0.4)


FORMES = [(0, "rond"), (1, "carre"), (2, "etoile"), (3, "anneau"), (4, "rond"), (5, "carre"), (6, "etoile"), (7, "anneau")]


def ca_bouge(c, t):
    t0 = T_SNAP + 0.05
    cx, cy = 540, 860
    rayons(c, cx, cy, t, 1100, 0.10 * prog(t, t0, 0.4), 14, S["violetVif"])
    lueur_s(c, cx, cy, 560, S["violetVif"], 0.25 * prog(t, t0, 0.4))
    for k, forme in FORMES:
        a = entre(t, t0 + 0.04 * k, 0.5, 1.8)
        if a <= 0: continue
        ang = t * (1.6 + 0.15 * k) + k * math.pi / 4
        R = mix(60, 420 + 30 * (k % 3), sortie(min(1, a)))
        x, y = cx + R * math.cos(ang), cy + R * 0.72 * math.sin(ang)
        col = [S["violetVif"], S["bleuVif"], S["or_"], S["violet"]][k % 4]
        c.save(); c.translate(x, y); c.rotate(t * 120 * (-1) ** k)
        if forme == "rond": c.drawCircle(0, 0, 30, pgrad(-30, -30, 30, 30, GRAD_VIF))
        elif forme == "carre": rrect(c, -28, -28, 56, 56, 14, col)
        elif forme == "etoile": etoile4(c, 0, 0, 40, col)
        else: anneau(c, 0, 0, 30, col, 10)
        c.restore()
    o = t0 + max(0.0, math.floor((t - t0 - 0.5) / 0.45)) * 0.45 + 0.5
    lettres(c, "ÇA", 540, 620, 200, t, t0, "ressort", decal=0.05, onde_t=o)
    lettres(c, "BOUGE", 540, 820, 236, t, t0 + 0.12, "ressort", decal=0.05, onde_t=o + 0.1)
    # lignes de vitesse
    for k in range(6):
        u = prog(t, t0 + 0.05 * k, 0.4, sortie)
        if 0 < u < 1:
            yy = 700 + 80 * k
            trait(c, mix(80, 40, u), yy, mix(80, 40, u) + 140 * (1 - u), yy, S["violetVif"], 6, 1 - u)
            trait(c, mix(1000, 1040, u), yy + 40, mix(1000, 1040, u) - 140 * (1 - u), yy + 40, S["bleuVif"], 6, 1 - u)
    eclats(c, cx, cy, t, t0, 18, 600, graine=6, duree=0.9)
    onde(c, cx, cy, t, t0, 150, 760, S["violetVif"], 12, 0.6)


def pub_grise(c, t, y0):
    """le post suivant du fil : une pub grise, plate"""
    c.save(); c.translate(0, y0)
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), peinture("#E7E5EB"))
    disque(c, 110, 260, 44, "#C9C5D0"); rrect(c, 172, 232, 220, 22, 11, "#C9C5D0"); texte(c, "Sponsorisé", 172, 266, 24, "#9B96A5", "demi", track=0)
    rrect(c, 70, 340, 840, 840, 26, "#D3D0D9"); icone(c, "image", 490, 760, 160, "#B3AFBB", 1.4)
    texte(c, "PROMO -10 %", 70, 1220, 64, "#8A8594", "noir", track=0)
    rrect(c, 70, 1310, 600, 22, 11, "#CFCBD6"); rrect(c, 70, 1350, 420, 22, 11, "#CFCBD6")
    for k, ic in enumerate(["heart", "message-circle", "send"]):
        disque(c, 1000, 900 + 130 * k, 46, "#D3D0D9"); icone(c, ic, 1000, 900 + 130 * k, 46, "#8A8594", 2.2)
    c.restore()


def hook(c, t):
    sw = prog(t, T_SW, 0.34, sortieExpo)
    back = prog(t, T_SNAP, 0.7, lambda v: ressort(v, 1.4, 4.2)) if t >= T_SNAP else 0.0
    dy = -1500 * sw * (1 - back)
    sx, sy = secousse(t, T_SNAP + 0.05, 22)
    c.save(); c.translate(sx, dy + sy)
    if t < T_SNAP: compte(c, t)
    else: ca_bouge(c, t)
    c.restore()
    # la pub grise arrive par en dessous, puis se fait chasser
    if T_SW <= t < T_SNAP + 0.5:
        gy = H + dy if t < T_SNAP else H * prog(t, T_SNAP, 0.32, entree) + (-1500 * sw + H) * (1 - prog(t, T_SNAP, 0.32, entree))
        pub_grise(c, t, gy)
    # le doigt qui fait défiler
    f = prog(t, T_SW - 0.22, 0.5, entreeSortie)
    if 0 < f < 1:
        hy = mix(1500, 700, f); al = math.sin(math.pi * f)
        carte_s(c, 640 - 64, hy - 64, 128, 128, 64, "#FFFFFF", None, 0.2, al)
        icone(c, "hand", 640, hy, 66, S["encre"], 2.2, al)
        for k in range(3): trait(c, 640, hy + 90 + 40 * k, 640, hy + 120 + 40 * k, S["violetVif"], 5, 0.5 * al * (1 - k / 3))


# ─────────────────────────────────────────── sons du hook
son(0.0, "impact", -7); son(0.0, "tick", -10); son(0.05, "pop", -13)
for tt in (0.5, 1.0): son(tt, "tick", -14)
son(TW(1) - 0.1, "pop", -12); son(TW(5) - 0.2, "whoosh_court", -12)
son(T_2, "tick", -9); son(T_2, "whoosh_court", -15); son(T_1, "tick", -8); son(T_1, "whoosh_court", -15)
son(T_SW - 0.22, "swipe", -9); son(T_SW, "whoosh", -8)
son(T_SNAP - 0.05, "whoosh_bas", -8); son(T_SNAP + 0.05, "impact", -5); son(T_SNAP + 0.08, "verre", -10); son(T_SNAP + 0.1, "ching", -13)
for k in range(8): son(T_SNAP + 0.1 + 0.05 * k, "pop", -18)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.2), (T_SW - 0.05, T_SW + 0.35), (T_SNAP - 0.05, T_SNAP + 0.4), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_SNAP + 0.05, "#FFFFFF", 0.35), (M["page"] + 0.12, "#FFFFFF", 0.25), (M["captive"] + 0.35, S["violetVif"], 0.08),
                    (M["euros"] - 0.06, "#FFFFFF", 0.22), (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    fond_studio(c, t, battement(t, T_SNAP + 0.05, 1, 0.5) + battement(t, M["captive"] + 0.35, 1, 0.5) - 2)
    scene_b1(c, t, M); scene_b2(c, t, M); scene_b3(c, t, M); scene_b4(c, t, M); scene_b5(c, t, M)
    scene_cta(c, t, M, DUREE)
    scene_prix(c, t, M)
    if t < T_B1 + 0.3:
        o = prog(t, T_B1 - 0.3, 0.35, entree)
        c.save(); c.translate(540, 900); c.scale(mix(1, 2.2, o), mix(1, 2.2, o)); c.translate(-540, -900)
        with Calque(c, 1 - o):
            hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    if t < M["prix"] - 0.25: SOUS.dessine(c, t, S["encre"])
