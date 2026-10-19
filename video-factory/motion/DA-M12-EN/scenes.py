"""DA-M12-EN « Cube » — pub US DYOU motion (16/10/2026), sans prix. Hook en 3D : un cube qui tourne d'un quart de tour
par idée — SAME BUSINESS, SAME OFFER, la photo grise, puis la face motion qui s'allume ; « Guess who gets the calls » :
les appels entrants arrivent du fond et s'empilent du côté motion. Corps commun et fin « take off » : moteur/studio3d.py."""
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

N_HOOK = 16
M = reperes(TW, N_HOOK)
SOUS = sous_titres(K)
T_R1, T_PHOTO, T_R2, T_THIS, T_GUESS, T_CALLS, T_B1 = TW(2), TW(4), TW(8), TW(10), TW(11), TW(15), M["b2"]
T_P = TW(7)
C_ = 580


def face_mot(mot1, mot2, ic):
    def f(c, w, h):
        rrect(c, 0, 0, w, h, 40, "#FFFFFF", 1.0, None, S["ligne"], 4)
        c.drawRoundRect(skia.Rect.MakeXYWH(14, 14, w - 28, h - 28), 30, 30, pgrad(0, 0, w, h, ["#FBF9FF", "#EEF2FF"]))
        tuile(c, ic, w / 2, h * 0.3, 130)
        texte(c, mot1, w / 2, h * 0.5, 54, S["gris"], "titre", "centre", 0.14)
        texte_grad(c, mot2, w / 2, h * 0.6, 108 if len(mot2) < 7 else 92, "noir", "centre", -0.035)
    return f


def face_haut(c, w, h):
    c.drawRoundRect(skia.Rect.MakeWH(w, h), 40, 40, pgrad(0, 0, w, h, GRAD_VIF))
    image(c, "dyou-icon-512", w / 2 - 90, h / 2 - 90, 180)


def angle_cube(t):
    a = 0.0
    for t0 in (T_R1, T_PHOTO, T_R2):
        if t >= t0 - 0.12: a += 90 * ressort(prog(t, t0 - 0.12, 0.7, lin), 1.6, 4.4)
    return a


def appel(k):
    def f(c, w, h):
        rrect(c, 0, 0, w, h, h / 2, "#FFFFFF", 1.0, None, S["ligne"], 3)
        disque(c, h / 2, h / 2, h * 0.36, S["vert"]); icone(c, "phone", h / 2, h / 2, h * 0.36, "#FFFFFF", 2.6)
        texte(c, ["Incoming call", "New customer", "Incoming call", "Booking request"][k], h + 4, h * 0.2, 40, S["encre"], "titre", track=-0.02)
        texte(c, "just now", h + 4, h * 0.56, 28, S["gris"], "demi", track=0)
    return f


def hook(c, t):
    ang = angle_cube(t)
    a = prog(t, -0.05, 0.55, sortieExpo)
    g = prog(t, T_GUESS - 0.15, 0.6, entreeSortie)
    sx, sy = secousse(t, T_CALLS, 16)
    cam = Cam(ax=-16 + 4 * math.sin(t * 0.9), ay=-22 * g + 5 * math.sin(t * 0.7), tz=mix(1400, -60, a) + 700 * g, cy=880, tx=sx - 330 * g, ty=sy)
    lueur_s(c, 540, 860, 720, S["violetVif"], 0.14 + 0.2 * prog(t, T_THIS - 0.1, 0.4))
    sol(c, cam, t, y=C_ / 2 + 80, alpha=0.35)
    vivant = post_motion(t, "YOUR", "BUSINESS", "IN MOTION", "Call now")
    def photo(cc, w, h):
        post_gris(4)(cc, w, h)
    faces = dict(avant=face_mot("SAME", "BUSINESS", "store"), droite=face_mot("SAME", "OFFER", "badge-percent"),
                 arriere=photo, gauche=vivant, haut=face_haut)
    plans = boite((0, 0, 0), C_, C_, C_, faces, ax=0, ay=ang + mix(-60, 0, a), az=0)
    # appels qui arrivent du fond et s'empilent à droite du cube
    for k in range(4):
        tk = TW(12 + k) - 0.25
        u = prog(t, tk, 0.55, sortieExpo)
        if u <= 0: continue
        cen = (mix(1100, 600, u), -330 + k * 200, mix(3200, -160, u))
        plans.append(Plan(coins(cen, 520, 150, ay=mix(-50, -6, u), ax=mix(20, 0, u)), 520, 150, appel(k), borne(u * 3)))
    scene3d(c, cam, plans)
    # étiquettes
    if T_P - 0.2 < t < T_R2 + 0.2:
        b = entre(t, T_P - 0.12, 0.4, 2.4) * (1 - prog(t, T_R2 - 0.1, 0.2))
        pill(c, "A photo", 540, 330, 36, "blanc", "image", borne(b * 3), mix(0.4, 1, b), rot=-4)
    if t > T_THIS - 0.2:
        b = entre(t, T_THIS - 0.1, 0.4, 2.4) * (1 - g)
        if b > 0:
            pill(c, "Motion design", 540, 300, 40, "grad", "sparkles", borne(b * 3), mix(0.4, 1, b), rot=3)
            eclats(c, 540, 880, t, T_THIS, 16, 600, graine=3)
            onde(c, 540, 880, t, T_THIS, 220, 800, S["violetVif"], 10, 0.6)
    if t > T_GUESS - 0.2:
        lettres(c, "WHO GETS", 540, 170, 100, t, TW(12) - 0.1, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
        lettres(c, "THE CALLS?", 540, 280, 120, t, TW(14) - 0.1, "ressort", decal=0.04)
        ph = entre(t, T_CALLS - 0.1, 0.4, 2.4)
        if ph > 0:
            c.save(); c.translate(250, 1240); c.rotate(14 * math.sin(t * 40) * (1 - prog(t, T_CALLS + 0.2, 0.6))); c.scale(ph, ph)
            lueur_s(c, 0, 0, 120, S["vert"], 0.3); disque(c, 0, 0, 70, S["vert"]); icone(c, "phone", 0, 0, 66, "#FFFFFF", 2.6)
            c.restore()


# ─────────────────────────────────────────── sons du hook
son(0.0, "whoosh_bas", -8); son(0.25, "impact", -5); son(0.28, "pop", -12)
for t0 in (T_R1, T_PHOTO, T_R2): son(t0 - 0.12, "whoosh_court", -9); son(t0 + 0.15, "impact_doux", -9)
son(T_P - 0.12, "pop", -11); son(T_R2 + 0.15, "verre", -10)
son(T_THIS - 0.1, "impact", -5); son(T_THIS, "ching", -9)
for i in range(8): son(T_THIS + 0.04 * i, "pop", -19)
son(T_GUESS - 0.15, "whoosh", -10)
for k in range(4): son(TW(12 + k) - 0.25, "whoosh_court", -13); son(TW(12 + k) + 0.1, "message_in", -10)
son(T_CALLS - 0.1, "ding", -9); son(T_CALLS, "impact_doux", -9)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps3d(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.4)] + [(t0 - 0.12, t0 + 0.3) for t0 in (T_R1, T_PHOTO, T_R2)] + [(T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_THIS - 0.05, "#FFFFFF", 0.3), (M["captive"] + 0.35, S["violetVif"], 0.08), (M["take"], "#FFFFFF", 0.22),
                    (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    compose(c, t, M, hook, T_B1, SOUS, K, battement(t, T_THIS, 1, 0.5) - 1)
