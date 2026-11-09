"""VX-M01-sombre — VORIX, bande-annonce produit sur fond noir, SANS voix (30/10/2026, retour client).

Mikail, sur la v4 claire : « ça ressemble pas trop à ma gourde, je pensais avoir une bande-annonce avec un fond
sombre et la gourde qui passe comme les pubs, sans voix ». Donc : le shaker 3D (moteur/vorix.py) corrigé d'après
ses photos — impression NOIRE sur le Tritan, couvercle en dôme, petit fouet d'acier — qui traverse l'écran dans
le noir, se révèle, plonge sur la base, mélange, s'éclate et se recompose. Pas de voix : des titres courts, des
pastilles en verre, une musique, les pops des bénéfices. Minutage fixe (pas de timing.json).
"""
import math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
moteur.PROJET = P
from moteur import *
from studio import lettres
from glace import pill_g, appliquer
appliquer()
from studio3d import Cam, scene3d
import vorix as V

DUREE = 24.4
NB_IMAGES = round(DUREE * FPS)
SFX, RAPIDE = [], []


def son(t, nom, gain=0.0): SFX.append((round(t, 3), nom, gain))
def rapide(t0, t1): RAPIDE.append((t0, t1))
def flou_a(t): return 4 if any(a <= t <= b for a, b in RAPIDE) else 1


# ─────────────────────────────────────────── repères (secondes)
T_HOOK, T_REVEL, T_MOTEUR, T_BASE = 0.0, 2.8, 4.3, 6.5
T_WATTS, T_VORTEX, T_NIVEAU, T_SPIN = 7.2, 9.3, 9.5, 10.4
T_HELICE, T_VX, T_ZERO = 10.5, 11.2, 12.0
T_FICHE, T_CINQ, T_TRITAN, T_BATT = 13.5, 13.9, 14.7, 15.5
T_DEMONTE, T_P_COUV, T_P_CORPS, T_P_HELICE, T_P_BASE = 17.0, 17.6, 18.0, 18.4, 18.8
T_EAU, T_VORIX, T_LOGO, FIN = 19.4, 20.6, 21.4, DUREE

NOIR, BLANC, GLACE, ENCRE_IMP = "#05070A", "#FFFFFF", "#DCE6F0", "#0E1217"   # blanc glace, jamais de bleu/violet
# verre sur fond noir : assez clair pour que l'encre noire se lise, liseré spéculaire franc
V.CORPS.update(bas="#2A3542", haut="#CFDDE9", alpha=0.34, spec=1.0, contre=1.0)

for t0 in (T_REVEL, T_BASE, T_VORTEX, T_FICHE, T_DEMONTE, T_VORIX): rapide(t0 - 0.05, t0 + 0.16)
rapide(T_FICHE, T_FICHE + 1.6)                      # le tour complet
for t0 in (T_WATTS, T_HELICE, T_VX, T_CINQ, T_TRITAN, T_BATT, T_P_COUV, T_P_CORPS, T_P_HELICE, T_P_BASE): son(t0, "pop", -8)
son(T_EAU + 0.1, "verre", -12)
son(T_LOGO + 0.4, "ding", -8)


# ─────────────────────────────────────────── décor
def fond(c, t, lueur, cy=0.42):
    c.drawRect(skia.Rect.MakeWH(W, H), peinture(NOIR))
    if lueur <= 0.01: return
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * cy), W * 0.95,
                                               [hexa("#18222D", 0.95 * lueur), hexa("#0B1016", 0.5 * lueur), hexa(NOIR, 0.0)], [0.0, 0.45, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


def halo(c, x, y, r, a):
    """nappe grise derrière le produit : sans elle, la fenêtre transparente et l'encre noire se perdent dans le noir"""
    if a <= 0.01: return
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), r, [hexa("#4A5666", a), hexa("#2A3340", a * 0.55), hexa(NOIR, 0.0)], [0.0, 0.45, 1.0]))
    c.drawCircle(x, y, r, p)


def nappe_sol(c, x, y, w, a):
    """flaque de lumière au sol sous le produit"""
    if a <= 0.01: return
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), w, [hexa("#35485C", 0.60 * a), hexa("#18222D", 0.25 * a), hexa(NOIR, 0.0)], [0.0, 0.4, 1.0]))
    c.save(); c.translate(x, y); c.scale(1.0, 0.22); c.translate(-x, -y)
    c.drawCircle(x, y, w, p); c.restore()


def titre(c, s, t, t0, y, taille=100, fin=None, couleur=BLANC, duree=0.42):
    taille = ajuste(s, 700, taille, "noir", -0.02)   # ≤ 700 px : bord droit à 850, hors colonne TikTok
    a = 1.0 if fin is None else 1 - prog(t, fin, 0.25, entree)
    if a <= 0.01: return
    lettres(c, s, 500, y, taille, t, t0, "masque", fam="noir", couleur=couleur, grad=False, decal=0.028, duree=duree, track=-0.02, alpha=a)


def etiquette(c, t, t0, label, x, y, ax_, ay_, cote=1, fin=None, mode="doux"):
    """pastille en verre reliée par un filet clair à un point du produit"""
    if t < t0 - 0.05: return
    e = prog(t, t0, 0.5, lambda u: ressort(u, 1.2, 5.0)) * (1.0 if fin is None else 1 - prog(t, fin, 0.25, entree))
    if e <= 0.01: return
    u = prog(t, t0 + 0.05, 0.35)
    trait(c, ax_, ay_, mix(ax_, x - cote * 150, u), mix(ay_, y, u), GLACE, 2.5, 0.9 * e)
    c.drawCircle(ax_, ay_, 7, peinture(GLACE, 0.95 * e))
    pill_g(c, label, x, y, 34, mode, alpha=e, s=mix(0.8, 1.0, e))


def balayage(c, t, t0, duree, largeur_bande=0.18, x0=-0.35, x1=1.35):
    """masque : tout disparaît sauf une bande de lumière qui traverse (à appliquer sur un calque)"""
    u = borne((t - t0) / duree)
    x = mix(x0, x1, u) * W
    p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kDstIn)
    lb = largeur_bande * W
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x - lb, 0), skia.Point(x + lb, 0)],
                                               [hexa("#000000", 0.0), hexa("#000000", 1.0), hexa("#000000", 0.0)], [0.0, 0.5, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


# ─────────────────────────────────────────── chorégraphie du produit
HH = 1150


def etat(t):
    """paramètres du produit et de la caméra à l'instant t"""
    # A. passage dans le noir : très près, traverse de droite à gauche en tournant
    if t < T_REVEL:
        u = borne(t / T_REVEL)
        return dict(hh=HH, rot=mix(-70, 30, u), tz=-430.0, dy=-40.0, dx=mix(700, -700, u), ax=-2.0,
                    niveau=0.0, led=0.0, ecart=0.0, spin=0.0, alpha=1.0, passage=True)
    # B. révélation : arrive du bas, en toupie, se pose
    a_in = prog(t, T_REVEL, 0.9, lambda u: ressort(u, 1.05, 5.0))
    rot = -12 + 8 * math.sin(t * 0.45) + 540 * (1 - prog(t, T_REVEL, 1.6, sortie))
    rot += 360 * prog(t, T_FICHE, 1.7, sortie)                    # le tour complet sur la fiche
    rot += 80 * prog(t, T_DEMONTE, 3.8, lambda u: u)              # dérive lente sur l'éclaté
    rot = mix(rot, 0.0, prog(t, T_VORIX, 1.0, sortie)) if t >= T_VORIX else rot
    tz, dy, ax = 1400.0, -160.0, -8.0
    for t0, d, tz1, dy1, ax1 in ((T_REVEL, 1.3, 820, -160, -4), (T_BASE, 0.6, 540, -700, -4), (T_VORTEX, 0.7, 820, -160, -4),
                                 (T_DEMONTE, 0.8, 1770, -199, -11), (T_VORIX, 0.7, 960, -210, -5)):
        k = prog(t, t0, d, sortie); tz, dy, ax = mix(tz, tz1, k), mix(dy, dy1, k), mix(ax, ax1, k)
    dy += mix(950, 0, a_in)
    dx = mix(420, 0, a_in) - 170 * prog(t, T_FICHE - 0.2, 0.5, sortie) * (1 - prog(t, T_DEMONTE - 0.3, 0.5, sortie))
    ecl = prog(t, T_DEMONTE, 0.9, lambda u: ressort(u, 1.0, 5.0)) * (1 - prog(t, T_VORIX, 0.6, lambda u: ressort(u, 1.0, 5.5)))
    niveau = prog(t, T_NIVEAU, 1.2, sortie) * 0.55 * (1 - prog(t, T_DEMONTE - 0.3, 0.4))
    led = prog(t, T_WATTS - 0.2, 0.3) * (0.6 + 0.4 * (0.5 + 0.5 * math.sin(t * 18))) * (1 - prog(t, T_DEMONTE - 0.3, 0.4))
    spin = 40.0 * (min(t, T_DEMONTE) - T_SPIN) if t >= T_SPIN else 0.0
    return dict(hh=HH * mix(0.92, 1.0, a_in), rot=rot, tz=tz, dy=dy, dx=dx, ax=ax, niveau=niveau, led=led,
                ecart=ecl * 1.3, spin=spin, alpha=a_in, passage=False)


def camera(e): return Cam(ax=e["ax"], ay=0, tz=e["tz"], cx=W / 2 + e["dx"], cy=H / 2 + e["dy"])


def produit(c, e, cam=None):
    cam = cam or camera(e)
    rot = math.radians(e["rot"])
    scene3d(c, cam, V.shaker(cam, cy=0, h=e["hh"], rot=rot, ax=0, niveau=e["niveau"], led=e["led"],
                             eclate=1.0 if e["ecart"] > 0.001 else 0.0, ecart=max(e["ecart"], 0.001),
                             rot_helice=rot + e["spin"], alpha=e["alpha"], encre=ENCRE_IMP, manchon_=True))
    return cam


def pieces_y(e):
    """ordonnées (repère produit) du centre de chaque pièce, éclaté compris — mêmes formules que vorix.shaker"""
    h, E = e["hh"], e["ecart"]
    hb, hc, hk = h * V.Y_BASE, h * V.Y_CORPS, h * V.Y_COUV
    return dict(base=h / 2 - hb / 2 + E * h * 0.34, bas=h / 2 + E * h * 0.34, corps=h / 2 - hb - hc / 2,
                helice=h / 2 - hb - hc * 0.14 + E * h * 0.20 - hc * 0.09, couv=-h / 2 + hk / 2 - E * h * 0.30,
                liquide=h / 2 - hb - hc * borne(e["niveau"]) * 0.86)


# ─────────────────────────────────────────── matières
def vortex(c, cam, e, k):
    if k <= 0.01: return
    d = e["hh"] * V.D_MM / V.H_MM
    y = pieces_y(e)["liquide"]
    X, Y, Z = cam.proj((0, y, 0)); kp = 1700.0 / (1700.0 + Z)
    for i in range(7):
        ang = e["spin"] * 0.9 + i * 0.9
        r = d * kp * (0.40 + 0.08 * math.sin(e["spin"] * 0.3 + i))
        path = skia.Path(); path.addArc(skia.Rect.MakeXYWH(X - r, Y - r * 0.26, 2 * r, r * 0.52), math.degrees(ang) % 360, 46)
        pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, StrokeCap=skia.Paint.kRound_Cap)
        pa.setColor(hexa("#DCEBFA", 0.40 * k)); c.drawPath(path, pa)


_RNG = np.random.default_rng(11)
POUDRE = [(float(a), float(b), float(c_), float(d_)) for a, b, c_, d_ in zip(_RNG.uniform(0, 6.283, 48), _RNG.uniform(0.0, 0.5, 48), _RNG.uniform(0.55, 0.95, 48), _RNG.uniform(5, 10, 48))]
GOUTTES = [(float(a), float(b), float(c_), float(d_)) for a, b, c_, d_ in zip(_RNG.uniform(-0.9, 0.9, 44), _RNG.uniform(-0.5, 0.5, 44), _RNG.uniform(0.0, 0.7, 44), _RNG.uniform(14, 26, 44))]


def poudre(c, cam, e, t):
    t0, duree = T_NIVEAU + 0.3, 2.2
    d, py = e["hh"] * V.D_MM / V.H_MM, pieces_y(e)
    for ang0, dec, r0, taille in POUDRE:
        u = (t - t0 - dec) / duree
        if u <= 0 or u >= 1: continue
        y = mix(py["corps"] - e["hh"] * 0.26, py["liquide"] + 40, sortie(u))
        r = d * 0.5 * r0 * (1 - 0.85 * u ** 1.5)
        ang = ang0 + u * 11.0
        X, Y, Z = cam.proj((r * math.cos(ang), y, r * math.sin(ang)))
        kp = 1700.0 / (1700.0 + Z); a = (1 - u) ** 1.2 * 0.9
        c.drawCircle(X, Y, taille * 1.5 * kp * (1 - 0.6 * u), peinture("#C9A36A", a))


def gouttes(c, cam, e, t):
    t0, duree = T_EAU - 0.05, 1.25
    d, py = e["hh"] * V.D_MM / V.H_MM, pieces_y(e)
    for x0, z0, dec, long_ in GOUTTES:
        u = (t - t0 - dec * 0.6) / (duree * 0.55)
        if u <= 0 or u >= 1: continue
        y = mix(py["couv"] - e["hh"] * 0.45, py["bas"] + 60, u * u)
        X, Y, Z = cam.proj((x0 * d * 0.55, y, z0 * d * 0.5))
        kp = 1700.0 / (1700.0 + Z)
        a = min(1.0, u * 6) * (1 - u ** 3) * 0.85
        c.drawOval(skia.Rect.MakeXYWH(X - 4.5 * kp, Y - long_ * 1.3 * kp, 9 * kp, long_ * 2.6 * kp), peinture("#BFD9F5", a))
        c.drawCircle(X - 1.6 * kp, Y - long_ * 0.6 * kp, 2.0 * kp, peinture(BLANC, a * 0.9))
    u = prog(t, t0 + 0.35, 0.7)
    if 0 < u < 1:
        X, Y, Z = cam.proj((0, py["bas"] + 60, 0)); kp = 1700.0 / (1700.0 + Z)
        for j in range(2):
            uj = borne(u - 0.18 * j); r = d * kp * (0.3 + 0.9 * uj)
            pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0 * (1 - uj) + 0.5)
            pa.setColor(hexa("#CFE2F5", 0.55 * (1 - uj)))
            c.drawOval(skia.Rect.MakeXYWH(X - r, Y - r * 0.22, 2 * r, r * 0.44), pa)


def helice_vitesse(c, cam, e, k):
    if k <= 0.01: return
    d, py = e["hh"] * V.D_MM / V.H_MM, pieces_y(e)
    X, Y, Z = cam.proj((0, py["helice"], 0)); kp = 1700.0 / (1700.0 + Z)
    for i in range(3):
        r = d * kp * (0.30 + 0.07 * i); a0 = (e["spin"] * 2.0 + i * 1.6) % 6.283
        path = skia.Path(); path.addArc(skia.Rect.MakeXYWH(X - r, Y - r * 0.28, 2 * r, r * 0.56), math.degrees(a0), 110)
        pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, StrokeCap=skia.Paint.kRound_Cap)
        pa.setColor(hexa(GLACE, 0.5 * k * (1 - 0.25 * i))); c.drawPath(path, pa)


# ─────────────────────────────────────────── montage
def dessine(c, t):
    e = etat(t)

    # A. le passage dans le noir : le produit n'existe que dans les rais de lumière
    if e["passage"]:
        fond(c, t, 0.12, cy=0.40)
        s = skia.Surface(W, H); cc = s.getCanvas(); cc.clear(0)
        produit(cc, e)
        img = s.makeImageSnapshot()
        p = skia.Paint(AntiAlias=True); p.setAlphaf(0.18)
        c.drawImage(img, 0, 0, moteur._ECH, p)                       # le fantôme du produit
        for k, (t0, d_) in enumerate(((0.10, 1.3), (0.95, 1.2), (1.75, 1.1))):
            if t0 <= t <= t0 + d_:
                s2 = skia.Surface(W, H); c2 = s2.getCanvas(); c2.clear(0)
                c2.drawImage(img, 0, 0)
                balayage(c2, t, t0, d_, 0.24 + 0.03 * k, x0=1.35, x1=-0.35)
                c.drawImage(s2.makeImageSnapshot(), 0, 0)
                p2 = skia.Paint(AntiAlias=True); p2.setAlphaf(0.35); p2.setBlendMode(skia.BlendMode.kScreen)
                c.drawImage(s2.makeImageSnapshot(), 0, 0, moteur._ECH, p2)
        titre(c, "DES GRUMEAUX", t, 0.8, 1215, 104, fin=T_REVEL - 0.25)
        titre(c, "DANS TA WHEY ?", t, 1.05, 1335, 104, fin=T_REVEL - 0.25)
        v = 1 - borne(t / 0.4)
        if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture(NOIR, v))
        return

    lueur = 0.55 + 0.25 * prog(t, T_REVEL, 1.0) + 0.2 * prog(t, T_LOGO, 1.2)
    fond(c, t, lueur, cy=0.40)
    sx, sy = 0.0, 0.0
    for t0 in (T_REVEL + 0.45, T_DEMONTE, T_VORIX):
        a, b = secousse(t, t0, 12, 0.36); sx += a; sy += b
    c.save(); c.translate(sx, sy)

    cam = camera(e)
    py = pieces_y(e)
    d = e["hh"] * V.D_MM / V.H_MM
    Xs, Ys, Zs = cam.proj((0, py["bas"] + 14, 0)); ks = 1700.0 / (1700.0 + Zs)
    nappe_sol(c, Xs, Ys, d * ks * 2.2, 0.9 * e["alpha"])
    X0, Y0, Z0 = cam.proj((0, (py["couv"] + py["base"]) / 2, 0))
    halo(c, X0, Y0, 560 * 1700.0 / (1700.0 + Z0) + 160, 0.55 * e["alpha"])
    produit(c, e, cam)

    def pt(y, side=0.0, z=-0.5):
        return cam.proj((side * d * 0.5, y, z * d))

    # matières
    vortex(c, cam, e, prog(t, T_SPIN + 0.2, 0.5) * (1 - prog(t, T_FICHE + 1.0, 0.5)))
    poudre(c, cam, e, t)
    helice_vitesse(c, cam, e, prog(t, T_SPIN, 0.3) * (1 - prog(t, T_FICHE - 0.2, 0.3)))
    gouttes(c, cam, e, t)

    # le rai de lumière sur le produit recomposé
    if T_LOGO - 0.6 <= t <= T_LOGO + 0.7:
        s = skia.Surface(W, H); cc = s.getCanvas(); cc.clear(0)
        produit(cc, e, cam)
        balayage(cc, t, T_LOGO - 0.6, 1.3, 0.12)
        p = skia.Paint(AntiAlias=True); p.setAlphaf(0.7); p.setBlendMode(skia.BlendMode.kScreen)
        c.drawImage(s.makeImageSnapshot(), 0, 0, moteur._ECH, p)

    # B. révélation
    titre(c, "VORIX.", t, T_MOTEUR - 0.3, 1230, 128, fin=T_BASE - 0.3)
    titre(c, "LE SHAKER ÉLECTRIQUE.", t, T_MOTEUR + 0.2, 1350, 80, fin=T_BASE - 0.3)
    titre(c, "UN MOTEUR DANS LA BASE.", t, T_BASE + 0.25, 1420, 84, fin=T_VORTEX - 0.3)
    # C. la base
    if T_BASE <= t < T_VORTEX + 0.4:
        bx, by, _ = pt(py["base"], -0.45)
        etiquette(c, t, T_WATTS, "MOTEUR 4,5 W", 300, 1230, bx, by, cote=1, fin=T_VORTEX)
    # D. le vortex
    if T_HELICE - 0.1 <= t < T_FICHE + 0.4:
        hx, hy, _ = pt(py["helice"], 0.30)
        etiquette(c, t, T_HELICE, "HÉLICE", 690, 1160, hx, hy, cote=-1, fin=T_FICHE)
        vx_, vy_, _ = pt(py["liquide"], 0.42)
        etiquette(c, t, T_VX, "VORTEX", 690, 1280, vx_, vy_, cote=-1, fin=T_FICHE)
    titre(c, "IL MÉLANGE TOUT SEUL.", t, T_ZERO, 1420, 92, fin=T_FICHE - 0.3)
    # E. la fiche : trois pastilles à droite, le produit fait un tour
    for k, (lab, t0, mode) in enumerate((("500 ML", T_CINQ, "doux"), ("CORPS TRITAN", T_TRITAN, "doux"), ("SE RECHARGE", T_BATT, "doux"))):
        if t < t0 - 0.05 or t > T_DEMONTE + 0.4: continue
        a = prog(t, t0, 0.5, lambda u: ressort(u, 1.2, 5.0)) * (1 - prog(t, T_DEMONTE - 0.2, 0.25, entree))
        w = largeur(lab, 34, "fort", -0.01) + 51
        pill_g(c, lab, 600 + w / 2 + 140 * (1 - a), 560 + k * 118, 34, mode, alpha=a, s=mix(0.8, 1.0, a))
    titre(c, "ZÉRO GRUMEAU.", t, T_BATT + 0.6, 1420, 92, fin=T_DEMONTE - 0.3)
    # F. l'éclaté
    if T_DEMONTE <= t < T_VORIX + 0.3:
        fin = T_VORIX
        etiquette(c, t, T_P_COUV, "COUVERCLE À BEC", 740, 250, *pt(py["couv"], 0.35, -0.3)[:2], cote=-1, fin=fin)
        etiquette(c, t, T_P_CORPS, "CORPS 500 ML", 290, 700, *pt(py["corps"], -0.40)[:2], cote=1, fin=fin)
        etiquette(c, t, T_P_HELICE, "HÉLICE", 290, 960, *pt(py["helice"], -0.22, -0.2)[:2], cote=1, fin=fin)
        etiquette(c, t, T_P_BASE, "BASE MOTEUR", 290, 1270, *pt(py["base"], -0.40)[:2], cote=1, fin=fin)
    titre(c, "TOUT SE DÉMONTE.", t, T_DEMONTE + 0.3, 1460, 84, fin=T_EAU - 0.35)
    titre(c, "PASSE SOUS L'EAU.", t, T_EAU, 1460, 84, fin=T_VORIX - 0.3)
    # G. signature
    if t >= T_LOGO:
        V.logo(c, 500, 1330, 340, BLANC, prog(t, T_LOGO, 0.6))
    c.restore()
    v = prog(t, FIN - 0.6, 0.6)
    if v: c.drawRect(skia.Rect.MakeWH(W, H), peinture("#000000", v))
