"""DA-M02 « On la zappe » — pub DYOU Agency pour vendre des vidéos motion (19,9 s).

Problème → mécanisme → solution : ta pub (une image fixe) se fait zapper en une seconde ; le cerveau est accro
au mouvement ; une info par seconde tient ton client jusqu'à ton offre ; avant c'était plus de 2 000 € et réservé
aux grandes marques ; maintenant commerce, artisan, indépendant ; DYOU Agency fait la tienne.
Style agence (moteur/agence.py), comme DA-M01.
"""
import math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence

DUREE = 19.9
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresFins(K, fusions={(47, 48, 49): "2 000 €,", (63, 64, 65): "DYOU Agency"})
V, VC = A["violet"], A["violetClair"]
CASQUE = "produits/electronique/casque-audio"


def entre(t, t0, d=0.42, s=1.5): return prog(t, t0, d, lambda v: rebond(v, s))
def sort(t, t0, d=0.26): return prog(t, t0, d, entree)


def degrade(c, x, y, w, h, cols):
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w, y + h)], [hexa(cols[0]), hexa(cols[1])]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), g)


def affiche_fixe(c, x, y, w, h):
    """la pub « classique » : une affiche plate, beige, qui ne bouge pas"""
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#D9D3C7"))
    rrect(c, x + w * 0.1, y + h * 0.12, w * 0.8, h * 0.42, 18, "#C4BCAE")
    icone(c, "image", x + w / 2, y + h * 0.33, w * 0.25, "#9B9284", 1.6)
    texte(c, "SOLDES", x + w / 2, y + h * 0.6, w * 0.15, "#7E7668", "noir", "centre", 0.02)
    rrect(c, x + w * 0.2, y + h * 0.78, w * 0.6, h * 0.025, 6, "#B3AA9B"); rrect(c, x + w * 0.3, y + h * 0.83, w * 0.4, h * 0.025, 6, "#C4BCAE")


# ─────────────────────────────────────────── S1 · « Ta pub, on la zappe en une seconde ? »
T_ZAP = TW(4) - 0.05
T_S2 = TW(8)


def ecran_s1(c, x, y, w, h, t):
    z = prog(t, T_ZAP, 0.32, entree)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#101018"))
    affiche_fixe(c, x, y - h * 1.05 * z, w, h)
    # le post suivant arrive par en dessous
    if z > 0:
        degrade(c, x, y + h * (1.05 - 1.05 * z), w, h, ("#4A5A86", "#252C4A"))
        icone(c, "camera", x + w / 2, y + h * (1.5 - 1.05 * z), w * 0.3, "#FFFFFF", 1.6, 0.35)


def s1(c, t):
    if t > T_S2 + 0.45: return
    u = prog(t, T_S2 - 0.05, 0.42, entreeSortie)          # le téléphone recule, l'affiche reste au centre
    cx, cy = 540, 1010
    with Calque(c, 1 - u):
        with Espace(c, cx, cy, ry=-14 + 3 * math.sin(t * 2), rx=5, s=mix(1, 0.7, u)):
            telephone_sombre(c, cx, cy, 500, 1000, lambda cc, a, b, d, e: ecran_s1(cc, a, b, d, e, t))
        # le doigt qui balaie
        f = prog(t, T_ZAP - 0.2, 0.5, entreeSortie)
        if 0 < f < 1:
            hy = mix(1300, 760, f); al = math.sin(math.pi * f)
            verre(c, 640 - 60, hy - 60, 120, 120, 60, 0.12)
            icone(c, "hand", 640, hy, 64, "#FFFFFF", 2.2, al)
            for k in range(3): trait(c, 640, hy + 80 + 40 * k, 640, hy + 110 + 40 * k, "#FFFFFF", 4, 0.4 * al * (1 - k / 3))
        a = entre(t, -0.4, 0.4, 2)
        pastille_verre(c, "Ta pub", 270, 560 + 8 * math.sin(t * 2.6), 42, "megaphone", borne(a * 2), mix(0.4, 1, a), rot=-6)
        b = entre(t, TW(6) - 0.05, 0.4, 2.4)
        if b > 0:
            pastille_verre(c, "Zappée en 1 s", 790, 1420, 42, "timer", borne(b * 2), mix(0.4, 1, b), accent=A["rouge"], rot=5)


# ─────────────────────────────────────────── S2 · « une image fixe, personne ne s'arrête dessus »
T_S3 = TW(16)


def s2(c, t):
    if t < T_S2 - 0.1 or t > T_S3 + 0.4: return
    u = entre(t, T_S2 - 0.05, 0.5, 1.2); o = sort(t, T_S3 - 0.25, 0.22)
    cx, cy = 540, 1000
    # des posts qui défilent derrière, sans jamais s'arrêter sur l'affiche
    a = prog(t, TW(12) - 0.2, 0.3, sortie) * (1 - o)
    if a > 0:
        for k in range(10):
            yy = (k * 260 - (t - TW(12)) * 1500) % 2600 - 300
            xx = 160 if k % 2 else 920
            cols = [("#4A5A86", "#252C4A"), ("#86504A", "#4A2525"), ("#4A866E", "#254A3C"), ("#86764A", "#4A3F25")][k % 4]
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xx - 110, yy, 220, 220), 26, 26), True)
            with Calque(c, 0.55 * a): degrade(c, xx - 110, yy, 220, 220, cols)
            c.restore()
    with Espace(c, cx, cy, rx=mix(30, 0, u), s=mix(0.6, 1, u) * (1 - 0.4 * o), ty=-500 * o):
        with Calque(c, borne(u * 2) * (1 - o)):
            verre(c, cx - 260, cy - 360, 520, 720, 40, 0.06)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 236, cy - 336, 472, 672), 26, 26), True)
            affiche_fixe(c, cx - 236, cy - 336, 472, 672)
            c.restore()
            p = entre(t, TW(10) - 0.05, 0.4, 2.2)
            if p > 0:
                disque(c, cx + 200, cy - 300, 56 * p, "#2A2738"); icone(c, "pause", cx + 200, cy - 300, 50 * p, "#FFFFFF", 2.6)
    b = entre(t, TW(10) - 0.05, 0.42, 2.2) * (1 - o)
    pastille_verre(c, "Image fixe", 300, 600, 42, "image-off", borne(b * 2), mix(0.4, 1, b), rot=-5)
    d = entre(t, TW(12) - 0.05, 0.42, 2.2) * (1 - o)
    pastille_verre(c, "Personne ne s'arrête", 600, 1420, 42, "eye-off", borne(d * 2), mix(0.4, 1, d), accent=A["rouge"], rot=4)


# ─────────────────────────────────────────── S3 · « Le cerveau, lui, est accro au mouvement »
T_S4 = TW(23)
_RNG = np.random.default_rng(5)
NEURONES = [(540 + 380 * math.cos(a) * r, 1000 + 380 * math.sin(a) * r) for a, r in zip(_RNG.uniform(0, 6.28, 26), _RNG.uniform(0.55, 1.0, 26))]


def s3(c, t):
    if t < T_S3 - 0.1 or t > T_S4 + 0.4: return
    u = entre(t, T_S3 + 0.02, 0.5, 1.4); o = sort(t, T_S4 - 0.05, 0.3)
    cx, cy = 540, 1000
    acc = prog(t, TW(20) - 0.05, 0.3, sortie)
    mv = prog(t, TW(22) - 0.05, 0.3, sortie)
    with Calque(c, borne(u * 2) * (1 - o)):
        lueur(c, cx, cy, 520 + 120 * acc + 40 * math.sin(t * 6) * acc, V, 0.35 + 0.3 * acc)
        # réseau de neurones : les liaisons s'allument sur « accro »
        for k, (x, y) in enumerate(NEURONES):
            x2, y2 = NEURONES[(k * 7 + 3) % len(NEURONES)]
            on = borne(acc * 3 - k / len(NEURONES) * 2)
            trait(c, x, y, x2, y2, VC, 2, 0.12 + 0.5 * on)
            trait(c, x, y, cx, cy, "#FFFFFF", 1.5, 0.05 + 0.15 * on)
        for k, (x, y) in enumerate(NEURONES):
            on = borne(acc * 3 - k / len(NEURONES) * 2)
            ph = 0.5 + 0.5 * math.sin(t * 9 + k)
            disque(c, x, y, 6 + 6 * on * ph, "#FFFFFF" if on > 0.5 else VC, 0.5 + 0.5 * on)
        # sur « mouvement » : des formes en orbite rapide
        if mv > 0:
            for k in range(6):
                a = t * (3.2 + 0.4 * k) + k * 1.05
                R = 300 + 40 * k
                disque(c, cx + R * math.cos(a), cy + R * 0.45 * math.sin(a), 16, ["#FF8A3D", "#2EC4B6", VC, "#FF4D8D", "#FFFFFF", "#4C7DFF"][k], mv)
                anneau(c, cx, cy, R * mix(0.6, 1, mv), "#FFFFFF", 1.5, 0.08 * mv)
        c.save(); c.translate(cx, cy); s = mix(0.4, 1, u) * battement(t, TW(20), 0.12, 0.3); c.scale(s, s)
        verre(c, -170, -170, 340, 340, 170, 0.08, violet=0.12)
        icone(c, "brain", 0, 0, 190, "#FFFFFF", 1.8)
        c.restore()
    b = entre(t, TW(20) - 0.05, 0.42, 2.2) * (1 - o)
    pastille_verre(c, "Dopamine", 780, 620, 42, "zap", borne(b * 2), mix(0.4, 1, b), accent="#FF8A3D", rot=6)
    d = entre(t, TW(22) - 0.05, 0.42, 2.2) * (1 - o)
    pastille_verre(c, "Mouvement", 300, 1410, 42, "sparkles", borne(d * 2), mix(0.4, 1, d), rot=-5)


# ─────────────────────────────────────────── S4 · une info par seconde, jusqu'à ton offre
T_OFFRE = TW(37) - 0.05
T_S5 = TW(39)
INFOS = [(TW(24) - 0.1, "Le produit", "gem", "#8B5CFF"), (TW(27) - 0.1, "Les avis", "star", "#FFB020"),
         (TW(29) - 0.1, "La livraison", "truck", "#2EC4B6"), (TW(31) - 0.1, "Le bonus", "sparkles", "#FF4D8D")]


def carte_info(c, x, y, titre, ic, col, t, t0):
    verre(c, x - 170, y - 210, 340, 420, 40, 0.08)
    lueur(c, x, y - 50, 150, col, 0.35)
    disque(c, x, y - 50, 80, col)
    icone(c, ic, x, y - 50, 80, "#FFFFFF", 2.2)
    if ic == "star":
        for j in range(5):
            a = prog(t, t0 + 0.1 + 0.05 * j, 0.25, lambda v: rebond(v, 2.4))
            if a > 0: icone(c, "star", x - 100 + 50 * j, y + 70, 36 * a, "#FFB020", 2.6)
    else:
        rrect(c, x - 110, y + 60, 220, 16, 8, "#FFFFFF", 0.3)
    texte(c, titre, x, y + 120, 36, "#FFFFFF", "gras", "centre", -0.01)


def s4(c, t):
    if t < T_S4 - 0.1 or t > T_S5 + 0.4: return
    o = sort(t, T_S5 - 0.25, 0.22)
    n_arr = sum(1 for t0, *_ in INFOS if t >= t0)
    # carrousel : chaque nouvelle carte pousse les autres vers la gauche
    dec = 0.0
    for k, (t0, *_r) in enumerate(INFOS):
        dec += 460 * prog(t, t0, 0.38, sortie) if k > 0 else 0
    off_offre = prog(t, T_OFFRE - 0.1, 0.4, entreeSortie)
    for k, (t0, titre, ic, col) in enumerate(INFOS):
        a = entre(t, t0, 0.45, 1.6)
        if a <= 0: continue
        x = 540 + 460 * k - dec - 900 * off_offre
        if x < -300 or x > 1380: continue
        y = 980 + 10 * math.sin(t * 2.2 + k)
        with Espace(c, x, y, ry=mix(70, 0, a) + (x - 540) * -0.03, s=mix(0.5, 1.25, a) * (1 - 0.22 * min(1, abs(x - 540) / 460))):
            with Calque(c, borne(a * 2) * (1 - o) * (1 - off_offre * 0.3)):
                carte_info(c, x, y, titre, ic, col, t, t0)
    # la barre « voir la suite » : elle avance par paliers d'une seconde
    b = entre(t, TW(23) - 0.05, 0.4, 1.3) * (1 - o)
    if b > 0:
        with Calque(c, borne(b * 2)):
            y = 1390
            verre(c, 140, y - 46, 800, 92, 46, 0.07)
            pr = borne((t - TW(23)) / (T_OFFRE - TW(23)))
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeLinear([skia.Point(180, y), skia.Point(900, y)], [hexa(V), hexa(VC)]))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(180, y - 9, 720 * pr, 18), 9, 9), g)
            rrect(c, 180, y - 9, 720, 18, 9, "#FFFFFF", 0.1)
            lueur(c, 180 + 720 * pr, y, 40, VC, 0.7); disque(c, 180 + 720 * pr, y, 12, "#FFFFFF")
            texte(c, "voir la suite", 180, y - 90, 26, VC, "fort", track=0.04, alpha=prog(t, TW(33) - 0.1, 0.3))
    # « ton offre » : la carte violette qui s'impose
    a = entre(t, T_OFFRE, 0.5, 1.6)
    if a > 0:
        x, y = 540, 990
        sx = secousse(t, T_OFFRE + 0.25, 12)[0]
        with Espace(c, x + sx, y, rx=mix(-40, 0, a), s=mix(1.8, 1, a) * (1 - 0.4 * o), ty=-500 * o):
            with Calque(c, borne(a * 3) * (1 - o)):
                lueur(c, x, y, 520, V, 0.6)
                verre(c, x - 280, y - 330, 560, 660, 48, 0.08, violet=0.28)
                texte(c, "TON OFFRE", x, y - 270, 30, A["violetPale"], "fort", "centre", 0.24)
                iw, ih = taille_img(CASQUE); ww = 300
                image(c, CASQUE, x - ww / 2, y - 210 + 8 * math.sin(t * 3), ww)
                bb = battement(t, T_OFFRE + 0.45, 0.1, 0.3)
                c.save(); c.translate(x, y + 200); c.scale(bb, bb)
                rrect(c, -190, -50, 380, 100, 50, "#FFFFFF")
                texte(c, "Commander", 0, -hauteurLigne(38) / 2, 38, V, "noir", "centre")
                c.restore()
    confettis(c, 540, 1000, t, T_OFFRE + 0.3, 26, 460, 3, cols=[V, VC, "#FFFFFF", A["violetPale"], "#FFB020"])


# ─────────────────────────────────────────── S5 · avant : plus de 2 000 €, réservé aux grandes marques
T_S6 = TW(54)
T_PRIX = TW(39) + 0.15


def s5(c, t):
    if t < T_S5 - 0.1 or t > T_S6 + 0.9: return
    u = entre(t, T_S5 - 0.05, 0.42, 2)
    mo = prog(t, T_S6 - 0.05, 0.3, entree)
    pastille_verre(c, "Avant", 540, 640 - 300 * mo, 46, "clock", borne(u * 2) * (1 - mo), mix(0.4, 1, u))
    a = entre(t, T_PRIX, 0.45, 1.4)
    if a > 0:
        cx, cy = 540, 1000
        casse = prog(t, T_S6 + 0.2, 0.6, entree)
        sx = secousse(t, TW(49), 18)[0]
        with Espace(c, cx + sx, cy + 1300 * casse ** 1.5, rx=mix(50, 0, a), rz=14 * casse, s=mix(0.5, 1, a)):
            with Calque(c, borne(a * 2)):
                lueur(c, cx, cy, 480, "#FFB020", 0.25 * (1 - casse))
                verre(c, cx - 400, cy - 200, 800, 400, 56, 0.09)
                v = int(2000 * sortie(prog(t, T_PRIX, TW(49) - T_PRIX + 0.05, lin)))
                lab = f"{v:,}".replace(",", " ") + " €"
                texte(c, "+", cx - largeur(lab, 150) / 2 - 70, cy - hauteurLigne(150) / 2 - 6, 110, VC, "noir")
                texte(c, lab, cx, cy - hauteurLigne(150) / 2 - 20, 150, "#FFFFFF", "noir", "centre", -0.04)
                texte(c, "une vidéo motion", cx, cy + 90, 32, A["gris"], "demi", "centre", 0)
                b = prog(t, T_S6 + 0.02, 0.22, sortie)
                if b > 0: trait(c, cx - 300, cy + 40, cx - 300 + 600 * b, cy - 70, A["rouge"], 14, 1.0)
    # « réservé aux grandes marques » : le cordon VIP
    g = entre(t, TW(50) - 0.1, 0.42, 2) * (1 - mo)
    if g > 0:
        with Calque(c, borne(g * 2)):
            y = 1330
            for xx in (210, 870):
                rrect(c, xx - 10, y - 60, 20, 120, 10, "#D4AF37"); disque(c, xx, y - 66, 18, "#E8C766")
            pth = skia.Path(); pth.moveTo(210, y - 50); pth.quadTo(540, y + 30 + 10 * math.sin(t * 3), 870, y - 50)
            c.drawPath(pth, peinture("#B3263A", 1, Style=skia.Paint.kStroke_Style, StrokeWidth=14, StrokeCap=skia.Paint.kRound_Cap))
        h = entre(t, TW(52) - 0.1, 0.42, 2) * (1 - mo)
        pastille_verre(c, "Grandes marques", 540, 1470, 42, "building-2", borne(h * 2), mix(0.4, 1, h))


# ─────────────────────────────────────────── S6 · maintenant : commerce, artisan, indépendant
T_LOGO = TW(63) - 0.12
T_CTA = TW(69) - 0.1


def s6(c, t):
    if t < T_S6 - 0.1 or t > T_LOGO + 0.4: return
    u = entre(t, T_S6 - 0.05, 0.45, 2)
    with Calque(c, borne(u * 2)):
        cx, cy = 540, 680
        lueur(c, cx, cy, 280, A["vert"], 0.25)
        verre(c, cx - 110, cy - 110, 220, 220, 110, 0.08)
        ouv = t > T_S6 + 0.25
        b = battement(t, T_S6 + 0.25, 0.15, 0.3)
        icone(c, "lock-open" if ouv else "lock", cx, cy, 110 * b, A["vert"] if ouv else "#FFFFFF", 2.4)
        onde(c, cx, cy, t, T_S6 + 0.25, 110, 330, A["vert"], 6)
    profils = [("Commerce", "store", TW(55) - 0.1, -1), ("Artisan", "hammer", TW(56) - 0.1, 1), ("Indépendant", "laptop", TW(58) - 0.1, -1)]
    for k, (lab, ic, t0, sgn) in enumerate(profils):
        a = entre(t, t0, 0.42, 2.2)
        if a <= 0: continue
        y = 960 + k * 170 + 6 * math.sin(t * 2.4 + k)
        w = pastille_verre(c, lab, 540 + sgn * 60 * (1 - a), y, 46, ic, borne(a * 2), mix(0.4, 1, a))
        ch = prog(t, t0 + 0.2, 0.3, lambda v: rebond(v, 2.4))
        if ch > 0 and w:
            disque(c, 540 + w / 2 + 36, y, 30 * ch, A["vert"]); icone(c, "check", 540 + w / 2 + 36, y, 34 * ch, "#FFFFFF", 3)
    a = entre(t, TW(62) - 0.1, 0.4, 2.4)
    if a > 0:
        pastille_verre(c, "Toi aussi", 540, 1470, 46, "sparkles", borne(a * 2), mix(0.4, 1, a), accent=A["vert"])
    confettis(c, 540, 1150, t, TW(62), 26, 420, 4, cols=[V, VC, "#FFFFFF", A["violetPale"], A["vert"]])


# ─────────────────────────────────────────── sons
son(0.0, "impact", -6); son(0.0, "pop", -13)
son(T_ZAP - 0.2, "swipe", -9); son(T_ZAP, "whoosh_court", -10); son(TW(6) - 0.05, "pop", -11); son(TW(6), "tick", -10)
son(T_S2 - 0.05, "whoosh", -11); son(TW(10) - 0.05, "clic", -10); son(TW(10), "pop", -13)
for k in range(9): son(TW(12) - 0.2 + 0.18 * k, "swipe", -19)
son(TW(12) - 0.05, "pop", -12)
son(T_S3 - 0.05, "whoosh_bas", -9); son(TW(17), "impact_doux", -10)
for k in range(8): son(TW(20) - 0.05 + 0.04 * k, "blip", -18)
son(TW(20) - 0.05, "montee", -13); son(TW(20), "pop", -12); son(TW(22) - 0.05, "whoosh_long", -12); son(TW(22), "pop", -12)
son(T_S4 - 0.05, "whoosh", -11)
for t0, *_ in INFOS: son(t0, "whoosh_court", -13); son(t0 + 0.05, "pop", -13)
for j in range(5): son(INFOS[1][0] + 0.1 + 0.05 * j, "tick", -16)
son(TW(33) - 0.1, "clic", -12)
son(T_OFFRE, "impact", -5); son(T_OFFRE + 0.02, "verre", -9); son(T_OFFRE + 0.3, "ching", -10)
son(T_S5 - 0.05, "swipe", -11); son(T_PRIX, "whoosh", -12); son(T_PRIX + 0.05, "montee", -11)
for k in range(10): son(T_PRIX + k * (TW(49) - T_PRIX) / 10, "tick", -17)
son(TW(49), "impact", -6); son(TW(50) - 0.1, "tampon", -10); son(TW(52) - 0.1, "pop", -12)
son(T_S6 - 0.05, "verre", -9); son(T_S6 + 0.02, "whoosh_court", -10); son(T_S6 + 0.25, "clic", -9)
for t0 in (TW(55) - 0.1, TW(56) - 0.1, TW(58) - 0.1): son(t0, "pop", -12); son(t0 + 0.2, "check", -14)
son(TW(62) - 0.1, "pop", -11); son(TW(62), "ching", -11)
son(T_LOGO - 0.1, "montee", -14); son(T_LOGO + 0.24, "impact", -6); son(T_LOGO + 0.26, "verre", -9)
son(T_CTA, "whoosh", -12); son(T_CTA + 0.3, "pop", -10)

for a, b in [(T_ZAP, T_ZAP + 0.3), (T_S2 - 0.1, T_S2 + 0.3), (T_S3 - 0.1, T_S3 + 0.3), (T_S4 - 0.1, T_S4 + 0.3),
             (T_OFFRE, T_OFFRE + 0.3), (T_S5 - 0.1, T_S5 + 0.3), (T_S6, T_S6 + 0.6), (T_LOGO, T_LOGO + 0.35), (T_CTA - 0.1, T_CTA + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_ZAP + 0.05, "#FFFFFF", 0.08), (TW(20), V, 0.14), (T_OFFRE + 0.05, V, 0.18), (TW(49), "#FFB020", 0.12),
                    (T_S6 + 0.25, A["vert"], 0.1), (T_LOGO + 0.24, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, TW(20), 1, 0.5) + battement(t, T_OFFRE, 1, 0.5) - 2)
    if t < T_LOGO + 0.45:
        s1(c, t); s2(c, t); s3(c, t); s4(c, t); s5(c, t); s6(c, t)
    disque_logo(c, t, T_LOGO, T_CTA)
    carton_agence(c, t, T_CTA + 0.25)
    K.dessine_eclairs(c, t)
    if t < T_LOGO + 0.15: SOUS.dessine(c, t)
