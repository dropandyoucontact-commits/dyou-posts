"""DA-M16-EN « Losing » — pub US DYOU pour vendre des sites (17/10/2026), sans prix. Hook en 3D : ton vieux site charge
dans un téléphone ; des clients arrivent du fond par vagues et ricochent dessus, croix rouge, ils repartent (« losing you
customers ») ; un calendrier en volume tourne ses pages (« Every single day ») ; la loupe plonge dans l'écran (« Here's why »).
Corps commun « sites » : moteur/sites3d.py."""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio3d import *
from sites3d import *
config_sites()

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 1.6, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

N_HOOK = 11
M = reperes(TW, N_HOOK)
SOUS = sous_titres(K)
T_LOSING, T_CUST, T_EVERY, T_SINGLE, T_DAY, T_WHY, T_B1 = TW(3), TW(5), TW(6), TW(7), TW(8), TW(9), M["g0"]
PW_, PH_ = 470, 960
JOURS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN", "MON"]


def jeton(perdu):
    def f(c, w, h):
        disque(c, w / 2, h / 2, w / 2 - 4, "#FFFFFF", 1.0, None)
        anneau(c, w / 2, h / 2, w / 2 - 6, S["lilas"] if not perdu else S["rouge"], 6)
        icone(c, "user-round", w / 2, h / 2, w * 0.5, S["violet"] if not perdu else S["rouge"], 2.4)
    return f


def page_cal(jour):
    def f(c, w, h):
        rrect(c, 0, 0, w, h, 28, "#FFFFFF", 1.0, None, S["ligne"], 3)
        c.drawRoundRect(skia.Rect.MakeWH(w, h * 0.28), 28, 28, pgrad(0, 0, w, 0, GRAD_VIF)); c.drawRect(skia.Rect.MakeXYWH(0, h * 0.14, w, h * 0.14), pgrad(0, 0, w, 0, GRAD_VIF))
        texte(c, jour, w / 2, h * 0.42, h * 0.32, S["encre"], "noir", "centre", -0.03)
        for j in range(2): disque(c, w * (0.3 + 0.4 * j), h * 0.06, 9, "#FFFFFF")
    return f


def page_pivot(cx, ytop, cz, w, h, ang):
    """page fixée par son bord haut ; ang = 0 à plat face caméra, 90 = retournée vers l'arrière"""
    a = math.radians(ang)
    return [(cx - w / 2, ytop, cz), (cx + w / 2, ytop, cz), (cx + w / 2, ytop + h * math.cos(a), cz + h * math.sin(a)), (cx - w / 2, ytop + h * math.cos(a), cz + h * math.sin(a))]


def hook(c, t):
    a = prog(t, -0.05, 0.55, lambda v: ressort(v, 1.3, 4.8))
    plonge = prog(t, T_WHY - 0.05, 0.7, entree)
    cam = Cam(ax=-6 + 3 * math.sin(t * 0.9), ay=mix(-40, -14, min(a, 1.1)) + 4 * math.sin(t * 0.7) + 14 * plonge, tz=mix(1400, 260, min(a, 1.1)) - 1500 * plonge, cy=980)
    lueur_s(c, 540, 980, 700, S["rouge"], 0.08 * prog(t, T_LOSING, 0.4) * (1 - plonge))
    plans = [Plan(coins((0, 60, 0), PW_, PH_), PW_, PH_, tel(site_vieux(t)))]
    # le flot de clients qui ricochent
    for i in range(16):
        ts = T_LOSING - 0.45 + 0.17 * i
        u = (t - ts) / 1.1
        if u <= 0 or u >= 1 or ts > T_WHY: continue
        cote = 1 if i % 2 else -1
        x0, y0 = cote * (160 + 90 * ((i * 7) % 5)), -360 + 140 * ((i * 3) % 6)
        if u < 0.55:
            v = sortie(u / 0.55)
            p = (mix(x0 * 2.2, x0 * 0.55, v), mix(y0 * 1.6, y0 * 0.7, v), mix(3200, -180, v))
            perdu = False
        else:
            v = entree((u - 0.55) / 0.45)
            p = (mix(x0 * 0.55, cote * 1300, v), mix(y0 * 0.7, y0 * 0.7 - 500 * v, v), mix(-180, -500, v))
            perdu = True
        plans.append(Plan(coins(p, 130, 130), 130, 130, jeton(perdu), borne((1 - u) * 4) * borne(u * 6)))
    # le calendrier dont les pages tournent
    cal = entre(t, T_EVERY - 0.15, 0.45, 1.8) * (1 - plonge)
    if cal > 0:
        cx_, ytop, cz = -330, -640, -140
        nb = len(JOURS) - 1
        dt = (T_DAY + 0.35 - T_EVERY) / nb
        for k in range(nb, -1, -1):
            tf = T_EVERY + k * dt
            ang = 0 if t < tf else 100 * prog(t, tf, 0.16, entree)
            if ang >= 99: continue
            plans.append(Plan(page_pivot(cx_, ytop, cz + 2.0 * k, 300, 300, ang), 300, 300, page_cal(JOURS[k]), borne(cal * 3), recto=False))
    scene3d(c, cam, plans)
    # croix rouges aux ricochets
    for i in range(16):
        ts = T_LOSING - 0.45 + 0.17 * i + 0.55 * 1.1
        if 0 < t - ts < 0.35 and ts < T_WHY + 0.5:
            cote = 1 if i % 2 else -1
            x0, y0 = cote * (160 + 90 * ((i * 7) % 5)), -360 + 140 * ((i * 3) % 6)
            X, Y, Z = cam.proj((x0 * 0.55, y0 * 0.7, -180))
            e = entre(t, ts, 0.25, 2.4) * (1 - prog(t, ts + 0.2, 0.15))
            disque(c, X + 40, Y - 40, 26 * e, S["rouge"]); icone(c, "x", X + 40, Y - 40, 30 * e, "#FFFFFF", 3.2)
    # la loupe
    if t > T_WHY - 0.3:
        lo = prog(t, T_WHY - 0.3, 0.4, sortie)
        x, y = mix(950, 600, lo), mix(1500, 900, lo)
        s_ = 1 + 1.6 * plonge
        c.save(); c.translate(x, y); c.scale(s_, s_)
        lueur_s(c, 0, 0, 160, S["violetVif"], 0.3)
        anneau(c, 0, 0, 110, S["encre"], 16); trait(c, 78, 78, 170, 170, S["encre"], 24)
        disque(c, 0, 0, 96, "#FFFFFF", 0.25)
        c.restore()
    # textes
    if t < T_EVERY + 0.1:
        with Calque(c, 1 - prog(t, T_EVERY - 0.1, 0.2)):
            lettres(c, "YOUR WEBSITE", 540, 170, 104, t, -0.25, "ressort", decal=0.03, grad=False, couleur=S["encre"])
            lettres(c, "IS LOSING", 540, 285, 120, t, T_LOSING - 0.12, "masque", grad=False, couleur=S["rouge"], decal=0.03, duree=0.35)
            lettres(c, "CUSTOMERS.", 540, 405, 120, t, T_CUST - 0.15, "ressort", decal=0.035)
    if T_EVERY - 0.15 < t < T_WHY + 0.05:
        with Calque(c, 1 - prog(t, T_WHY - 0.1, 0.2)):
            for k, (mot, tt) in enumerate([("EVERY.", T_EVERY), ("SINGLE.", T_SINGLE), ("DAY.", T_DAY)]):
                lettres(c, mot, 720, 180 + k * 120, 112, t, tt - 0.1, "ressort", decal=0.035, grad=k == 2, couleur=S["encre"])
    if t > T_WHY - 0.1:
        lettres(c, "HERE'S WHY.", 540, 230, 140, t, T_WHY - 0.08, "ressort", decal=0.04)


son(0.0, "whoosh_bas", -8); son(0.3, "impact", -6); son(0.33, "verre", -12); son(0.05, "pop", -12)
son(T_LOSING - 0.12, "whoosh_court", -10)
for i in range(16):
    ts = T_LOSING - 0.45 + 0.17 * i
    if ts < T_WHY: son(ts + 0.6, "croc" if i % 3 == 0 else "blip", -17)
son(T_CUST - 0.15, "impact_doux", -9)
son(T_EVERY - 0.15, "pop", -10)
for k in range(len(JOURS) - 1): son(T_EVERY + k * (T_DAY + 0.35 - T_EVERY) / (len(JOURS) - 1), "swipe", -14)
for tt in (T_EVERY, T_SINGLE, T_DAY): son(tt - 0.1, "tampon", -10)
son(T_WHY - 0.3, "whoosh", -9); son(T_WHY - 0.05, "montee", -10); son(T_WHY + 0.3, "whoosh_bas", -8)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_sites(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.5), (T_WHY - 0.05, T_WHY + 0.7), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_CUST, S["rouge"], 0.08), (M["take"], "#FFFFFF", 0.22), (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    compose_sites(c, t, M, hook, T_B1, SOUS, K, 0.0)
