"""DA-M13-EN « Invisible » — pub US DYOU motion (16/10/2026), sans prix. Hook en 3D : la carte « Your business »
arrive en tournoyant, cinq étoiles (« great ») ; recul : elle n'est qu'une case d'un mur de posts en perspective, et
elle s'efface en pointillés (« invisible »), le viseur passe sans la voir ; tout se fige (« doesn't move ») ; « Let's change
that » : la case se remplit de motion et jaillit du mur vers nous. Corps commun et fin « take off » : moteur/studio3d.py."""
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

N_HOOK = 15
M = reperes(TW, N_HOOK)
SOUS = sous_titres(K)
T_GREAT, T_ONLINE, T_INVIS, T_BEC, T_MOVE, T_CHANGE, T_THAT, T_B1 = TW(3), TW(5), TW(7), TW(8), TW(11), TW(12), TW(14), M["b2"]
CW, CH, PX, PY = 420, 540, 470, 600


def carte_pro(fantome=0.0):
    def f(c, w, h):
        if fantome < 1:
            with Calque(c, 1 - fantome):
                rrect(c, 0, 0, w, h, 34, "#FFFFFF", 1.0, None, S["ligne"], 4)
                c.drawRoundRect(skia.Rect.MakeXYWH(22, 22, w - 44, h * 0.46), 24, 24, pgrad(0, 0, w, h, ["#F1EAFF", "#E6EEFF"]))
                tuile(c, "store", w / 2, 22 + h * 0.23, 110)
                texte(c, "Your business", 30, h * 0.55, 40, S["encre"], "titre", track=-0.02)
                for j in range(5): icone(c, "star", 46 + j * 44, h * 0.68, 34, S["or_"], 2.4)
                pill(c, "Open now", 110, h * 0.85, 24, "vert", "clock")
        if fantome > 0:
            pa = peinture(S["grisClair"], fantome, Style=skia.Paint.kStroke_Style, StrokeWidth=5)
            pa.setPathEffect(skia.DashPathEffect.Make([18, 14], 0))
            c.drawRoundRect(skia.Rect.MakeXYWH(4, 4, w - 8, h - 8), 34, 34, pa)
            icone(c, "eye-off", w / 2, h / 2, 90, S["grisClair"], 2.2, fantome)
    return f


def hook(c, t):
    a = prog(t, -0.05, 0.7, sortieExpo)
    recul = prog(t, T_ONLINE - 0.2, 0.8, entreeSortie)
    sortie_ = prog(t, T_CHANGE + 0.05, 0.75, lambda v: ressort(v, 1.3, 4.6)) if t >= T_CHANGE + 0.05 else 0.0
    fige = prog(t, T_MOVE - 0.1, 0.3)
    cam = Cam(ax=mix(-4, -10, recul) + 3 * math.sin(t * 0.8) * (1 - fige), ay=mix(0, 26, recul) - 18 * sortie_,
              tz=mix(-380, 1500, recul) - 900 * sortie_, cy=900)
    fant = prog(t, T_INVIS - 0.25, 0.5, entreeSortie) * (1 - prog(t, T_CHANGE, 0.25))
    lueur_s(c, 540, 900, 700, S["violetVif"], 0.12 + 0.25 * borne(sortie_))
    plans = []
    if recul > 0:
        for i in range(-3, 4):
            for j in range(-3, 4):
                if i == 0 and j == 0: continue
                d = math.hypot(i, j)
                ap = prog(t, T_ONLINE - 0.25 + 0.03 * d, 0.5, sortie)
                if ap <= 0: continue
                plans.append(Plan(coins((i * PX, j * PY, 0), CW, CH), CW, CH, post_gris(i * 7 + j * 3 + 20), borne(ap * 2) * mix(1, 0.5, borne(sortie_))))
    # la carte : spin d'arrivée, puis case du mur, puis elle jaillit
    spin = mix(-75, 0, a) + 6 * math.sin(t * 1.6) * (1 - recul)
    if sortie_ > 0: spin = 360 * sortie_
    cen = (0, 0, mix(0, -700, borne(sortie_)))
    if sortie_ > 0.02 or t >= T_CHANGE:
        contenu = post_motion(t, "YOUR", "BUSINESS", "IN MOTION", "Visit us")
        plans.append(Plan(coins(cen, CW, CH, ay=spin), CW, CH, contenu, 1.0))
        plans.append(Plan(coins(cen, CW, CH, ay=spin + 180), CW, CH, carte_pro(0)))
    else:
        plans.append(Plan(coins(cen, CW, CH, ay=spin), CW, CH, carte_pro(fant)))
        plans.append(Plan(coins(cen, CW, CH, ay=spin + 180), CW, CH, aplat(None, 34, GRAD_VIF)))
    scene3d(c, cam, plans)
    # étoiles « great »
    g = entre(t, T_GREAT - 0.15, 0.45, 2.2) * (1 - recul)
    if g > 0:
        for k in range(5):
            ang = -math.pi / 2 + (k - 2) * 0.42
            x, y = 540 + 430 * math.cos(ang), 900 + 520 * math.sin(ang) - 30
            c.save(); c.translate(x, y); c.rotate(20 * math.sin(t * 3 + k)); s_ = entre(t, T_GREAT - 0.15 + 0.05 * k, 0.4, 2.6)
            c.scale(s_, s_); lueur_s(c, 0, 0, 70, S["or_"], 0.35); icone(c, "star", 0, 0, 74, S["or_"], 3.0); c.restore()
        pill(c, "Great", 540, 1260, 38, "grad", "heart", borne(g * 3), mix(0.4, 1, g), rot=-3)
    # barre de recherche « online »
    if T_ONLINE - 0.2 < t < T_CHANGE + 0.2:
        b = entre(t, T_ONLINE - 0.15, 0.45, 1.8) * (1 - prog(t, T_CHANGE - 0.1, 0.25))
        with Calque(c, borne(b * 3)):
            carte_s(c, 140, 200, 800, 100, 50, "#FFFFFF", None, 0.16)
            icone(c, "search", 200, 250, 40, S["violet"], 2.6)
            q = "best near me"; n = int(borne((t - T_ONLINE) / 0.6) * len(q) + 0.999) if t > T_ONLINE else 0
            texte(c, q[:n], 240, 250 - hauteurLigne(40, "titre") / 2, 40, S["encre"], "titre", track=-0.01)
            if int(t * 3) % 2 == 0: rrect(c, 244 + largeur(q[:n], 40, "titre", -0.01), 228, 4, 44, 2, S["violet"])
    # le viseur qui balaie le mur et saute la carte
    if T_INVIS - 0.3 < t < T_MOVE:
        u = prog(t, T_INVIS - 0.3, T_MOVE - T_INVIS + 0.2, lin)
        vx = mix(180, 900, u); vy = 900 + 220 * math.sin(u * 7)
        if abs(vx - 540) < 120: vy -= 260
        anneau(c, vx, vy, 70, S["rouge"], 6, 0.8); trait(c, vx - 100, vy, vx - 80, vy, S["rouge"], 6); trait(c, vx + 80, vy, vx + 100, vy, S["rouge"], 6)
        trait(c, vx, vy - 100, vx, vy - 80, S["rouge"], 6); trait(c, vx, vy + 80, vx, vy + 100, S["rouge"], 6)
        iv = entre(t, T_INVIS - 0.1, 0.4, 2.4)
        pill(c, "Invisible", 540, 1220, 40, "rouge", "eye-off", borne(iv * 3), mix(0.4, 1, iv), rot=4)
    if T_BEC - 0.2 < t < T_CHANGE + 0.1:
        cb = entre(t, TW(10) - 0.2, 0.4, 1.6) * (1 - prog(t, T_CHANGE - 0.1, 0.2))
        carte_s(c, 540 - 400 * mix(0.6, 1, cb), 350, 800 * mix(0.6, 1, cb), 300, 46, "#FFFFFF", None, 0.18, borne(cb * 3) * 0.95)
        lettres(c, "IT DOESN'T", 540, 380, 96, t, TW(10) - 0.12, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.3, sortie_t=T_CHANGE - 0.1)
        lettres(c, "MOVE.", 540, 480, 150, t, T_MOVE - 0.08, "masque", grad=False, couleur="#6E6878", decal=0.04, duree=0.3, sortie_t=T_CHANGE - 0.1)
    if t > T_CHANGE - 0.1:
        rayons(c, 540, 900, t, 1200, 0.12 * borne(sortie_), 16, S["violetVif"])
        lettres(c, "LET'S CHANGE", 540, 200, 100, t, T_CHANGE - 0.05, "ressort", decal=0.03, grad=False, couleur=S["encre"])
        lettres(c, "THAT.", 540, 310, 150, t, T_THAT - 0.1, "ressort", decal=0.04)
        eclats(c, 540, 900, t, T_CHANGE + 0.3, 18, 640, graine=8)
        onde(c, 540, 900, t, T_CHANGE + 0.25, 200, 820, S["violetVif"], 10, 0.6)


# ─────────────────────────────────────────── sons du hook
son(0.0, "whoosh_long", -8); son(0.45, "impact_doux", -8); son(0.5, "pop", -12)
for k in range(5): son(T_GREAT - 0.15 + 0.05 * k, "pop", -14)
son(T_GREAT, "ching", -11)
son(T_ONLINE - 0.2, "whoosh_bas", -8)
for i in range(12): son(T_ONLINE + i * 0.05, "frappe", -18)
son(T_INVIS - 0.25, "swipe", -11); son(T_INVIS, "croc", -9)
for i in range(4): son(T_INVIS + 0.2 + 0.25 * i, "tick", -14)
son(T_MOVE - 0.08, "tampon", -8)
son(T_CHANGE - 0.1, "montee", -9); son(T_CHANGE + 0.05, "whoosh", -7); son(T_CHANGE + 0.3, "impact", -5); son(T_CHANGE + 0.33, "verre", -10); son(T_CHANGE + 0.35, "ching", -11)
son(T_THAT - 0.1, "pop", -11)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps3d(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.6), (T_ONLINE - 0.2, T_ONLINE + 0.5), (T_CHANGE + 0.05, T_CHANGE + 0.6), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_CHANGE + 0.3, "#FFFFFF", 0.3), (M["captive"] + 0.35, S["violetVif"], 0.08), (M["take"], "#FFFFFF", 0.22),
                    (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    compose(c, t, M, hook, T_B1, SOUS, K, battement(t, T_CHANGE + 0.3, 1, 0.5) - 1)
