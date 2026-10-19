"""DA-M15-EN « Competitor » — pub US DYOU pour vendre des sites (17/10/2026), sans prix. Hook en 3D : deux vitrines
identiques posées sur un sol en perspective, toi et ton concurrent ; un grand signe = (« isn't better than you ») ; derrière
chaque vitrine monte un téléphone : le tien gris, le sien vivant, la caméra tourne vers lui (« a better website »).
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

N_HOOK = 12
M = reperes(TW, N_HOOK)
SOUS = sous_titres(K)
T_BETTER, T_YOU, T_THEY, T_BW, T_WEB, T_B1 = TW(3), TW(5), TW(6), TW(10), TW(11), M["g0"]
BX, BY = 290, 250


def vitrine(auvent, nom, gris=False):
    def f(c, w, h):
        rrect(c, 0, 0, w, h, 24, "#FFFFFF" if not gris else "#F3F2F5", 1.0, None, S["ligne"], 4)
        n = 7
        for j in range(n):
            col = auvent[j % 2]
            pth = skia.Path(); x0 = j * w / n
            pth.moveTo(x0, 0); pth.lineTo(x0 + w / n, 0); pth.lineTo(x0 + w / n, 70); pth.quadTo(x0 + w / n / 2, 100, x0, 70); pth.close()
            c.drawPath(pth, peinture(col))
        texte(c, nom, w / 2, 112, 36, S["encre"], "titre", "centre", -0.02)
        rrect(c, 30, 175, w * 0.5, h - 205, 14, "#E8EEFF" if not gris else "#E2E0E6")
        trait(c, 50, 195, 110, 255, "#FFFFFF", 6, 0.7)
        rrect(c, w * 0.62, 175, w * 0.3, h - 175, 10, S["encre2"] if not gris else "#9A95A3")
        disque(c, w * 0.66, 175 + (h - 175) / 2, 7, S["or_"])
    return f


def hook(c, t):
    a = prog(t, -0.05, 0.6, sortieExpo)
    tour = prog(t, T_BW - 0.2, 0.8, entreeSortie)
    cam = Cam(ax=mix(-24, -12, a) - 6 * tour, ay=mix(-30, 6 * math.sin(t * 0.8), a) + 26 * tour, tz=mix(1200, 300, a) - 200 * tour, cy=1040, tx=-260 * tour)
    lueur_s(c, 540 + 200 * tour, 800, 700, S["violetVif"], 0.12 + 0.2 * tour)
    sol(c, cam, t, y=BY + 210, alpha=0.5)
    cote = aplat(S["lavande"]); haut = aplat("#F6F2FF")
    plans = []
    for k, (x, auv, nom) in enumerate([(-BX, ("#B9B4C3", "#E6E3EA"), "You"), (BX, (S["violet"], "#FFFFFF"), "Competitor")]):
        d = prog(t, -0.05 + 0.12 * k, 0.55, lambda v: ressort(v, 1.4, 4.6))
        plans += boite((x, BY - 600 * (1 - min(d, 1.0)), 0), 440, 420, 300, dict(avant=vitrine(auv, nom), gauche=cote, droite=cote, haut=haut),
                       ay=-6 if k == 0 else 6)
        # le téléphone qui monte derrière la vitrine
        m = prog(t, T_THEY - 0.1 + 0.25 * k, 0.6, lambda v: ressort(v, 1.3, 4.6)) if t > T_THEY - 0.1 + 0.25 * k else 0
        if m > 0:
            ecr = tel(site_vieux(t, True)) if k == 0 else tel(site_moderne(t, "Competitor Co."))
            sc = 0.6 if k == 0 else mix(0.6, 0.78, tour)
            plans.append(Plan(coins((x, mix(BY, -220, m) - (90 * tour if k else 0), 180 - (180 * tour if k else 0)), 470 * sc, 960 * sc, ay=(-6 if k == 0 else 6)), 470 * sc, 960 * sc, ecr,
                              (1 - 0.5 * tour) if k == 0 else 1.0))
    scene3d(c, cam, plans)
    # le signe = entre les deux
    e = entre(t, T_BETTER - 0.12, 0.45, 2.6) * (1 - prog(t, T_THEY, 0.25))
    if e > 0:
        X, Y, _ = cam.proj((0, BY, 0))
        c.save(); c.translate(X, Y); c.scale(e, e)
        disque(c, 0, 0, 90, "#FFFFFF", 1.0, (8, 24, 0.18))
        for dy in (-22, 22): c.drawRoundRect(skia.Rect.MakeXYWH(-46, dy - 10, 92, 20), 10, 10, pgrad(-46, 0, 46, 0, GRAD_VIF))
        c.restore()
    if t > T_WEB - 0.1:
        X, Y, _ = cam.proj((BX, -220, 0))
        eclats(c, X, Y, t, T_WEB, 14, 520, graine=6)
        onde(c, X, Y, t, T_WEB, 160, 700, S["violetVif"], 10, 0.6)
    # textes
    if t < T_THEY + 0.2:
        with Calque(c, 1 - prog(t, T_THEY - 0.05, 0.25)):
            lettres(c, "YOUR", 540, 190, 110, t, -0.25, "ressort", decal=0.04, grad=False, couleur=S["encre"])
            lettres(c, "COMPETITOR", 540, 300, 128, t, TW(1) - 0.15, "ressort", decal=0.035)
            n = entre(t, TW(2) - 0.1, 0.4, 2.4)
            pill(c, "isn't better than you", 540, 470, 36, "encre", "scale", borne(n * 3), mix(0.4, 1, n), rot=-3)
    if t > T_THEY - 0.1:
        lettres(c, "THEY JUST HAVE", 540, 190, 84, t, T_THEY - 0.05, "masque", grad=False, couleur=S["encre"], decal=0.025, duree=0.35)
        lettres(c, "A BETTER", 540, 285, 120, t, T_BW - 0.12, "ressort", decal=0.035)
        lettres(c, "WEBSITE.", 540, 405, 140, t, T_WEB - 0.1, "ressort", decal=0.04)


son(0.0, "whoosh_bas", -8); son(0.35, "impact", -6); son(0.47, "impact_doux", -8); son(0.05, "pop", -12)
son(TW(1) - 0.15, "pop", -11); son(TW(2) - 0.1, "pop", -11)
son(T_BETTER - 0.12, "impact_doux", -7); son(T_BETTER, "check", -11)
son(T_THEY - 0.1, "whoosh_court", -10); son(T_THEY + 0.15, "whoosh_court", -10); son(T_THEY + 0.3, "pop", -12)
son(T_BW - 0.2, "whoosh_long", -8); son(T_WEB - 0.05, "impact", -5); son(T_WEB, "ching", -9)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_sites(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.5), (T_THEY - 0.1, T_THEY + 0.5), (T_BW - 0.2, T_BW + 0.5), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_WEB, "#FFFFFF", 0.3), (M["take"], "#FFFFFF", 0.22), (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    compose_sites(c, t, M, hook, T_B1, SOUS, K, battement(t, T_WEB, 1, 0.5) - 1)
