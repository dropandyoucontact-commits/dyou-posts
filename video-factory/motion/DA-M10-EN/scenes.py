"""DA-M10-EN « Feed » — pub US DYOU motion (16/10/2026), sans prix. Hook en 3D : le fil d'actualité couché en perspective
défile à toute vitesse (posts gris), compteur 1,000 posts a day ; GRAY. FLAT. FORGOTTEN. ; « Then one moves » : un post
se décolle du fil, se redresse face caméra et prend vie ; « and they stop » : le fil s'arrête, le doigt tape.
Corps commun et fin « take off » : moteur/studio3d.py."""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio3d import *
config_us()

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 1.6, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

N_HOOK = 18
M = reperes(TW, N_HOOK)
SOUS = sous_titres(K, fusions={(4, 5, 6, 7, 8): "a thousand posts a day."})
T_THOU, T_GRAY, T_FLAT, T_FORG, T_THEN, T_MOVES, T_STOP, T_B1 = TW(5), TW(9), TW(10), TW(11), TW(12), TW(14), TW(17), M["b2"]

PAS, CW, CH = 800, 560, 720
V0 = 2600.0


def defil(t):
    return cles(t, [(0, 0), (T_GRAY, V0 * T_GRAY, lin), (T_THEN + 0.2, V0 * T_GRAY + 1400, sortie)])


S_FIN = defil(T_THEN + 0.3)
K_HERO = round((S_FIN - 500) / PAS)


def cam_fil(t, ax=-58.0):
    return Cam(ax=ax, ay=6 * math.sin(t * 0.8), az=-4 + 2 * math.sin(t * 0.6), tz=520, cy=1040)


def hook(c, t):
    s = defil(t)
    cam = cam_fil(t)
    lift = prog(t, T_THEN - 0.05, 0.75, lambda v: ressort(v, 1.5, 4.4)) if t >= T_THEN - 0.05 else 0.0
    oubli = prog(t, T_FORG - 0.05, 0.5, entreeSortie)
    plans = []
    for col, dx in enumerate([-640, 0, 640]):
        dec = 0 if col == 1 else PAS / 2
        for k in range(-2, K_HERO + 12):
            y = k * PAS - s + 500 + dec
            if y < -5600 or y > 1500: continue
            if col == 1 and k == K_HERO and lift > 0: continue
            z = cam.vue((dx, y, 0))[2]
            a = borne(1.25 - (z - 200) / 4600) * (1 if col == 1 else 0.8) * mix(1, 0.45, oubli)
            plans.append(Plan(coins((dx, y, 0), CW, CH), CW, CH, post_gris(k * 3 + col, 0.35 * oubli), a))
    lueur_s(c, 540, 700, 700, S["lilas"], 0.25)
    scene3d(c, cam, plans)
    # le post qui bouge : se décolle du fil et se redresse face caméra
    if lift > 0:
        y0 = K_HERO * PAS - s + 500
        ch = Cam(ax=mix(-58, 0, lift), ay=mix(6 * math.sin(t * 0.8), -8 * math.sin((t - T_THEN) * 2.2), lift), az=mix(-4, 0, lift),
                 tz=mix(520, 0, lift), cy=mix(1040, 860, lift))
        rayons(c, 540, 860, t, 1100, 0.12 * borne(lift), 16, S["violetVif"])
        lueur_s(c, 540, 860, 560, S["violetVif"], 0.32 * borne(lift))
        cen = (0, mix(y0, 0, borne(lift)), mix(0, -260, lift))
        scene3d(c, ch, [Plan(coins(cen, CW, CH), CW, CH, post_motion(t))])
        eclats(c, 540, 860, t, T_MOVES, 16, 560, graine=4)
        onde(c, 540, 860, t, T_THEN + 0.1, 200, 760, S["violetVif"], 10, 0.6)
    # le doigt qui arrête tout
    f = prog(t, T_STOP - 0.35, 0.35, sortie)
    if f > 0:
        ap = prog(t, T_STOP - 0.04, 0.06, sortie) * (1 - prog(t, T_STOP + 0.08, 0.15, sortie))
        hx, hy = mix(860, 640, f), mix(1500, 1060, f)
        carte_s(c, hx - 66, hy - 66 + 10 * ap, 132, 132, 66, "#FFFFFF", None, 0.2)
        icone(c, "hand", hx, hy + 10 * ap, 68, S["encre"], 2.2)
        onde(c, 640, 1040, t, T_STOP, 40, 260, S["violetVif"], 8, 0.5)
    # textes au premier plan
    so = prog(t, T_GRAY - 0.15, 0.25, entree)
    a0 = entre(t, -0.2, 0.4, 2)
    with Calque(c, 1 - so):
        pill(c, "Your customers", 540, 230, 32, "blanc", "users", borne(a0 * 3), mix(0.5, 1, a0), rot=-2)
        u = prog(t, T_THOU - 0.25, 0.6, sortie)
        if u > 0:
            n = int(round(1000 * u))
            txt = f"{n // 1000},{n % 1000:03d}" if n >= 1000 else str(n)
            c.save(); c.translate(540, 400); sc = battement(t, T_THOU + 0.35, 0.12, 0.3); c.scale(sc, sc)
            texte_grad(c, txt, 0, -hauteurLigne(170) / 2, 170, "noir", "centre", -0.04)
            c.restore()
            b = entre(t, TW(6) - 0.1, 0.4, 2.2)
            pill(c, "posts a day", 540, 540, 32, "encre", "layers", borne(b * 3), mix(0.4, 1, b), rot=3)
    for mot, t0, t1 in [("GRAY.", T_GRAY, T_FLAT), ("FLAT.", T_FLAT, T_FORG), ("FORGOTTEN.", T_FORG, T_THEN)]:
        if t0 - 0.2 < t < t1 + 0.3:
            lettres(c, mot, 540, 250, 150 if len(mot) < 8 else 120, t, t0 - 0.08, "masque", grad=False, couleur="#8A8594",
                    decal=0.03, duree=0.3, sortie_t=t1 - 0.05)
    if t > T_THEN - 0.1:
        lettres(c, "ONE MOVES.", 540, 230, 128, t, T_MOVES - 0.12, "ressort", decal=0.035, sortie_t=T_B1 - 0.3)


# ─────────────────────────────────────────── sons du hook
son(0.0, "impact", -7); son(0.0, "whoosh_long", -8); son(0.05, "pop", -13)
for i in range(16): son(0.05 + i * 0.13, "swipe", -20)
son(T_THOU - 0.25, "montee", -12)
for i in range(10): son(T_THOU - 0.2 + i * 0.05, "tick", -17)
son(T_THOU + 0.35, "ching", -10); son(TW(6) - 0.1, "pop", -12)
for tt in (T_GRAY, T_FLAT, T_FORG): son(tt - 0.08, "tampon", -10)
son(T_FORG + 0.1, "whoosh_bas", -12)
son(T_THEN - 0.1, "montee", -10); son(T_THEN + 0.05, "whoosh", -8); son(T_MOVES - 0.05, "impact", -5); son(T_MOVES, "verre", -10); son(T_MOVES + 0.05, "ching", -12)
son(T_STOP - 0.35, "swipe", -12); son(T_STOP, "clic", -6); son(T_STOP + 0.05, "check", -11)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps3d(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, T_GRAY), (T_THEN - 0.05, T_THEN + 0.4), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_MOVES - 0.05, "#FFFFFF", 0.3), (M["captive"] + 0.35, S["violetVif"], 0.08), (M["take"], "#FFFFFF", 0.22),
                    (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    compose(c, t, M, hook, T_B1, SOUS, K, battement(t, T_MOVES, 1, 0.5) - 1)
