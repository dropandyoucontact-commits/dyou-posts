"""DA-M11-EN « Pause » — pub US DYOU motion (16/10/2026), sans prix. Hook en 3D : un énorme symbole PAUSE en volume
s'écrase devant un téléphone figé (« You just stopped scrolling ») ; le cerveau rassure (« that's normal ») ; la vidéo
repart et le téléphone fait un tour complet (« It's motion design ») ; recul : un mur de téléphones qui regardent tous
la même pub (« it works on everyone »). Corps commun et fin « take off » : moteur/studio3d.py."""
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
T_STOP, T_WORRY, T_NORMAL, T_ITS, T_MOTION, T_WORKS, T_EVERY, T_B1 = TW(2), TW(4), TW(7), TW(8), TW(9), TW(13), TW(15), M["b2"]
PW, PH = 470, 960
T_FIGE = 0.9


def ecran(t):
    """contenu de l'écran : figé jusqu'à « It's », puis il repart"""
    tt = T_FIGE if t < T_ITS else T_FIGE + (t - T_ITS)
    return post_motion(tt, "STOP", "SCROLLING", "IT MOVES", "Watch")


def ecran_fige(t):
    base = ecran(t)
    def f(c, w, h):
        base(c, w, h)
        if t < T_ITS + 0.2:
            o = 1 - prog(t, T_ITS, 0.25)
            c.drawRect(skia.Rect.MakeWH(w, h), peinture("#2A2436", 0.42 * o))
            rrect(c, w * 0.08, h - 60, w * 0.84, 10, 5, "#FFFFFF", 0.35 * o)
            rrect(c, w * 0.08, h - 60, w * 0.84 * 0.38, 10, 5, S["rouge"], o)
            disque(c, w * 0.08 + w * 0.84 * 0.38, h - 55, 14, S["rouge"], o)
    return f


def barres_pause(t):
    a = prog(t, -0.05, 0.3, sortieExpo)
    part = prog(t, T_WORRY - 0.1, 0.55, entree)
    plans = []
    face = aplat(None, 26, GRAD_VIF)
    cote = aplat("#4B2BA8", 0)
    dessus = aplat("#9B7BFF", 0)
    for k, dx in enumerate((-115, 115)):
        cz = mix(-1300, -420, a) + 2600 * part
        cy_ = -40 - 900 * part * (1 if k else 0.7)
        plans += boite((dx - 170 + (300 if k else -300) * part, cy_, cz), 120, 440, 130,
                       dict(avant=face, gauche=cote, droite=cote, haut=dessus, bas=cote),
                       ax=mix(-35, 8, a) + 120 * part, ay=mix(40, -14, a) + (90 if k else -90) * part, az=mix(-20, 0, a))
    return plans


def hook(c, t):
    # caméra : se tourne vers le téléphone, puis recule pour le mur de téléphones
    recul = prog(t, T_WORKS - 0.25, 0.8, entreeSortie)
    cam = Cam(ax=mix(10, 0, prog(t, T_WORRY, 0.8, entreeSortie)) + 18 * recul, ay=mix(-24, 4 * math.sin(t * 1.4), prog(t, T_WORRY, 0.8, entreeSortie)) - 16 * recul,
              tz=mix(80, 0, prog(t, 0, 0.6, sortie)) + 2600 * recul, cy=900 - 120 * recul)
    lueur_s(c, 540, 900, 760, S["violetVif"], 0.16 + 0.12 * prog(t, T_ITS, 0.4))
    # « It's motion design » : la vidéo repart et le téléphone fait un tour complet
    tour = prog(t, T_MOTION - 0.15, 0.95, lambda v: ressort(v, 1.2, 5.0)) * 360 if t >= T_MOTION - 0.15 else 0.0
    plans = [Plan(coins((0, 0, 0), PW, PH, ay=tour), PW, PH, tel(ecran_fige(t))),
             Plan(coins((0, 0, 0), PW, PH, ay=tour + 180), PW, PH, dos_tel)]
    # le mur de téléphones (« it works on everyone »)
    if recul > 0:
        for i in range(-3, 4):
            for j in range(-2, 3):
                if i == 0 and j == 0: continue
                d = math.hypot(i, j)
                ap = entre(t, T_WORKS - 0.2 + 0.05 * d, 0.5, 1.6)
                if ap <= 0: continue
                cen = (i * 600, j * 1080, 600 * mix(1.6, 0, ap) + 40 * d)
                plans.append(Plan(coins(cen, PW, PH, ay=mix(60, 0, ap) * (1 if i > 0 else -1)), PW, PH,
                                  tel(post_motion(t + 0.37 * (i + 3 * j), "STOP", "SCROLLING", "IT MOVES", "Watch")), borne(ap * 2) * 0.55))
    if t < T_WORRY + 0.7: plans += barres_pause(t)
    scene3d(c, cam, plans)
    sx, sy = secousse(t, 0.25, 22)
    # coches « vue » sur le mur
    if recul > 0.5:
        for i in range(-3, 4):
            for j in range(-2, 3):
                if (i + j) % 2: continue
                X, Y, Z = cam.proj((i * 600 + 180, j * 1080 - 420, 40 * math.hypot(i, j)))
                ck = entre(t, T_EVERY - 0.1 + 0.04 * abs(i + j), 0.35, 2.4)
                if ck > 0:
                    disque(c, X, Y, 30 * ck * FOC / (FOC + Z), S["vert"]); icone(c, "check", X, Y, 34 * ck * FOC / (FOC + Z), "#FFFFFF", 3)
    # textes
    a0 = entre(t, 0.0, 0.35, 2.4)
    if t < T_WORRY + 0.3:
        with Calque(c, 1 - prog(t, T_WORRY, 0.25)):
            lettres(c, "PAUSED.", 540 + sx, 230 + sy, 150, t, -0.2, "ressort", decal=0.04)
            pill(c, "You stopped scrolling", 540, 1230, 32, "encre", "pause", borne(a0 * 3), mix(0.4, 1, a0), rot=-3)
    b = entre(t, T_WORRY + 0.05, 0.45, 2.0)
    if b > 0 and t < T_ITS + 0.2:
        with Calque(c, borne(b * 3) * (1 - prog(t, T_ITS, 0.25))):
            c.save(); c.translate(240, 560); c.rotate(-6); c.scale(mix(0.5, 1, b), mix(0.5, 1, b))
            carte_s(c, -150, -110, 300, 220, 36, ombre=0.18)
            tuile(c, "brain", 0, -26, 96)
            texte(c, "Your brain", 0, 40, 30, S["encre"], "titre", "centre", -0.02)
            c.restore()
        n = entre(t, T_NORMAL - 0.1, 0.4, 2.4)
        if n > 0: pill(c, "100% normal", 790, 1220, 34, "vert", "circle-check", borne(n * 3), mix(0.4, 1, n), rot=5)
    if T_MOTION - 0.3 < t < T_WORKS + 0.2:
        with Calque(c, 1 - prog(t, T_WORKS - 0.1, 0.3)):
            p_ = entre(t, T_ITS - 0.05, 0.4, 2.2)
            pill(c, "Playing again", 540, 240, 38, "grad", "play", borne(p_ * 3), mix(0.4, 1, p_), rot=-3)
    if t > T_WORKS - 0.1:
        cb = entre(t, T_WORKS - 0.15, 0.45, 1.6)
        carte_s(c, 540 - 430 * mix(0.6, 1, cb), 150, 860 * mix(0.6, 1, cb), 330, 46, "#FFFFFF", None, 0.18, borne(cb * 3) * 0.94)
        lettres(c, "IT WORKS ON", 540, 200, 92, t, T_WORKS - 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
        lettres(c, "EVERYONE.", 540, 300, 150, t, T_EVERY - 0.1, "ressort", decal=0.04)


# ─────────────────────────────────────────── sons du hook
son(0.0, "whoosh_bas", -8); son(0.22, "impact", -4); son(0.25, "tampon", -8); son(0.3, "verre", -11)
son(T_STOP, "pop", -12)
son(T_WORRY - 0.1, "whoosh", -9); son(T_WORRY + 0.05, "pop", -11); son(T_NORMAL - 0.1, "check", -10); son(T_NORMAL, "ding", -14)
son(T_ITS - 0.05, "clic", -7); son(T_MOTION - 0.15, "whoosh_long", -7); son(T_MOTION + 0.6, "impact_doux", -9); son(T_MOTION + 0.62, "ching", -12)
for i in range(10): son(T_MOTION - 0.2 + 0.05 * i, "blip", -19)
son(T_WORKS - 0.25, "whoosh_bas", -9)
for i in range(12): son(T_WORKS - 0.2 + 0.05 * i, "pop", -19)
son(T_EVERY - 0.1, "impact", -6); son(T_EVERY, "ching", -11)
for i in range(8): son(T_EVERY - 0.1 + 0.04 * i, "check", -21)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps3d(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.3), (T_WORRY - 0.1, T_WORRY + 0.5), (T_MOTION - 0.15, T_MOTION + 0.6), (T_WORKS - 0.25, T_WORKS + 0.5), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(0.22, "#FFFFFF", 0.35), (T_EVERY - 0.08, "#FFFFFF", 0.2), (M["captive"] + 0.35, S["violetVif"], 0.08), (M["take"], "#FFFFFF", 0.22),
                    (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    compose(c, t, M, hook, T_B1, SOUS, K, battement(t, 0.22, 1, 0.5) - 1)
