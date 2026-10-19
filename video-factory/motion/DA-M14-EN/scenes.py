"""DA-M14-EN « Layers » — pub US DYOU motion (16/10/2026), sans prix. Hook en 3D : une photo grise prend un tampon X
(« Big brands don't post photos ») et bascule au fond ; la pub animée arrive en tournant (« They post this ») ; vue éclatée :
ses calques (fond, formes, produit, texte, bouton) s'écartent en profondeur pendant que la caméra tourne autour, chacun
étiqueté (« Built layer by layer ») ; ils se recollent d'un coup et la pub devient la tienne (« Now it's your turn »).
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

N_HOOK = 16
M = reperes(TW, N_HOOK)
SOUS = sous_titres(K)
T_PHOTOS, T_THEY, T_THIS, T_BUILT, T_L1, T_BY, T_L2, T_NOW, T_YOUR, T_TURN, T_B1 = (TW(4), TW(5), TW(7), TW(8), TW(9), TW(10), TW(11),
                                                                                  TW(12), TW(14), TW(15), M["b2"])
LW, LH = 560, 780
NOMS = ["Background", "Shapes", "Product", "Text", "Button"]


def calque(k, t, a_lab, tienne):
    def f(c, w, h):
        if k == 0:
            c.drawRoundRect(skia.Rect.MakeWH(w, h), 44, 44, pgrad(0, 0, w, h, GRAD_VIF))
            lueur_s(c, w / 2, h * 0.4, 300, "#FFFFFF", 0.18)
        elif k == 1:
            for j in range(3):
                r = 110 + 55 * j + 8 * math.sin(t * 3 + j)
                c.save(); c.translate(w / 2, h * 0.4); c.rotate(t * (40 + 25 * j) * (-1) ** j)
                rrect(c, -r, -r, 2 * r, 2 * r, r * 0.45, None, 1.0, None, "#FFFFFF", 4)
                c.restore()
            for j in range(6):
                a = t * 1.3 + j * 1.05
                etoile4(c, w / 2 + 200 * math.cos(a), h * 0.4 + 250 * math.sin(a), 18 + 6 * math.sin(t * 5 + j), "#FFFFFF", 0.9, t * 2)
        elif k == 2:
            y = h * 0.3 + 14 * math.sin(t * 2.4)
            c.save(); c.translate(w / 2, y); c.rotate(8 * math.sin(t * 1.7))
            carte_s(c, -110, -110, 220, 220, 60, "#FFFFFF", None, 0.25)
            icone(c, "store" if tienne else "gem", 0, 0, 120, S["violet"], 2.4)
            c.restore()
        elif k == 3:
            l1, l2 = ("YOUR", "BUSINESS") if tienne else ("NEW", "DROP")
            tl = (t + 0.3) % 2.2
            lettres(c, l1, w / 2, h * 0.5, 84, tl, 0.0, "ressort", grad=False, couleur="#FFFFFF", decal=0.05)
            lettres(c, l2, w / 2, h * 0.6, 84 if len(l2) < 6 else 74, tl, 0.1, "ressort", grad=False, couleur="#FFFFFF", decal=0.04)
        else:
            c.save(); c.translate(w / 2, h * 0.84); s_ = 1 + 0.06 * math.sin(t * 7); c.scale(s_, s_)
            pill(c, "Book now" if tienne else "Shop now", 0, 0, 34, "blanc", "sparkles")
            c.restore()
            barre_progression(c, 40, h - 34, w - 80, (t * 0.45) % 1, 8, ["#FFFFFF", "#FFFFFF"], "#FFFFFF40", tete=False)
        if a_lab > 0:
            c.save(); c.translate(w - 20, 40)
            pill(c, NOMS[k], -largeur(NOMS[k], 38, "fort", 0) / 2 - 60, 10, 38, "encre" if k != 4 else "blanc", "layers", borne(a_lab * 3), mix(0.4, 1, a_lab))
            c.restore()
    return f


def hook(c, t):
    # la photo grise qui prend le X et bascule
    tombe = prog(t, T_THEY - 0.1, 0.6, entree)
    a0 = prog(t, -0.05, 0.5, sortieExpo)
    cam = Cam(ax=-8, ay=0, tz=0)
    lueur_s(c, 540, 900, 720, S["violetVif"], 0.12 + 0.18 * prog(t, T_THEY, 0.5))
    if tombe < 1:
        cen = (0, mix(-60, 300, tombe), mix(500, 0, a0) + 2200 * tombe)
        scene3d(c, cam, [Plan(coins(cen, LW, LH, ax=mix(30, 0, a0) + 80 * tombe, ay=mix(-40, 8, a0), az=-6 * tombe), LW, LH, post_gris(5), 1 - tombe)])
        x_ = entre(t, T_PHOTOS - 0.1, 0.35, 2.6) * (1 - tombe)
        if x_ > 0:
            c.save(); c.translate(540, 860); c.rotate(-12); c.scale(mix(2.4, 1, prog(t, T_PHOTOS - 0.1, 0.18, entree)), mix(2.4, 1, prog(t, T_PHOTOS - 0.1, 0.18, entree)))
            with Calque(c, borne(x_ * 3)):
                disque(c, 0, 0, 150, S["rouge"], 1.0, (10, 30, 0.25)); icone(c, "x", 0, 0, 170, "#FFFFFF", 4.2)
            c.restore()
    # la pub en calques
    arr = prog(t, T_THEY - 0.05, 0.7, lambda v: ressort(v, 1.4, 4.6)) if t >= T_THEY - 0.05 else 0.0
    if arr > 0:
        ecl = prog(t, T_BUILT - 0.1, 0.8, entreeSortie) * (1 - prog(t, T_NOW - 0.05, 0.28, entree))
        orb = prog(t, T_BUILT - 0.1, T_NOW - T_BUILT + 0.1, douce)
        tienne = t > T_NOW + 0.1
        cam2 = Cam(ax=mix(-6, -9, ecl) + 3 * math.sin(t), ay=mix(70, -16, min(arr, 1.2)) + 50 * orb * (1 - prog(t, T_NOW - 0.05, 0.4, entreeSortie)) + 6 * math.sin(t * 0.8),
                   tz=mix(1600, 60, min(arr, 1.1)) + 260 * ecl, cy=900, tx=-110 * ecl)
        plans = []
        for k in range(5):
            lab = entre(t, T_L1 - 0.1 + 0.16 * k, 0.4, 2.2) * (1 - prog(t, T_NOW - 0.1, 0.2))
            z = (2 - k) * 260 * ecl + (2 - k) * 4
            plans.append(Plan(coins((0, -20, z), LW, LH), LW, LH, calque(k, t, lab, tienne), recto=False))
        scene3d(c, cam2, plans)
        sx, sy = secousse(t, T_NOW + 0.2, 20)
        if t > T_NOW + 0.15:
            eclats(c, 540 + sx, 880 + sy, t, T_NOW + 0.22, 18, 620, graine=9)
            onde(c, 540, 880, t, T_NOW + 0.2, 200, 820, S["violetVif"], 10, 0.6)
    # titres
    if t < T_THEY + 0.25:
        with Calque(c, 1 - prog(t, T_THEY - 0.05, 0.25)):
            lettres(c, "BIG BRANDS", 540, 200, 132, t, -0.25, "ressort", decal=0.035)
            b = entre(t, TW(2) - 0.1, 0.4, 2.2)
            pill(c, "don't post photos", 540, 400, 36, "encre", "image-off", borne(b * 3), mix(0.4, 1, b), rot=-3)
    if T_THEY - 0.2 < t < T_BUILT + 0.2:
        with Calque(c, 1 - prog(t, T_BUILT - 0.05, 0.25)):
            lettres(c, "THEY POST", 540, 170, 100, t, T_THEY - 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
            lettres(c, "THIS.", 540, 280, 150, t, T_THIS - 0.1, "ressort", decal=0.05)
    if T_BUILT - 0.2 < t < T_NOW + 0.1:
        with Calque(c, 1 - prog(t, T_NOW - 0.1, 0.2)):
            lettres(c, "LAYER", 540, 170, 140, t, T_L1 - 0.1, "chemin", decal=0.045, duree=0.5, graine=4)
            lettres(c, "BY LAYER", 540, 310, 110, t, T_BY - 0.1, "masque", decal=0.03, duree=0.35, grad=False, couleur=S["encre"])
    if t > T_NOW - 0.1:
        lettres(c, "NOW IT'S", 540, 170, 100, t, T_NOW - 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
        lettres(c, "YOUR TURN.", 540, 280, 140, t, T_YOUR - 0.1, "ressort", decal=0.04)


# ─────────────────────────────────────────── sons du hook
son(0.0, "whoosh_bas", -8); son(0.3, "impact_doux", -8); son(0.05, "pop", -12)
son(TW(2) - 0.1, "pop", -11)
son(T_PHOTOS - 0.1, "tampon", -6); son(T_PHOTOS - 0.05, "croc", -11)
son(T_THEY - 0.1, "whoosh_bas", -9)
son(T_THEY - 0.05, "whoosh_long", -8); son(T_THIS - 0.1, "impact", -6); son(T_THIS, "ching", -10)
son(T_BUILT - 0.1, "montee", -10)
for k in range(5): son(T_L1 - 0.1 + 0.16 * k, "pop", -12); son(T_L1 - 0.05 + 0.16 * k, "clic", -18)
for i in range(10): son(T_BUILT + 0.05 * i, "blip", -20)
son(T_NOW - 0.05, "whoosh_court", -9); son(T_NOW + 0.2, "impact", -4); son(T_NOW + 0.22, "verre", -10); son(T_NOW + 0.25, "ching", -11)
son(T_YOUR - 0.1, "pop", -11)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps3d(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.4), (T_THEY - 0.1, T_THEY + 0.5), (T_NOW - 0.05, T_NOW + 0.3), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_PHOTOS - 0.08, "#FFFFFF", 0.2), (T_NOW + 0.2, "#FFFFFF", 0.3), (M["captive"] + 0.35, S["violetVif"], 0.08), (M["take"], "#FFFFFF", 0.22),
                    (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    compose(c, t, M, hook, T_B1, SOUS, K, battement(t, T_NOW + 0.2, 1, 0.5) - 1)
