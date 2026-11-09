"""VX-M01 — VORIX en motion design, v4 « studio clair » (30/10/2026).

Youssef, après la v3 sombre : « fond blanc mais un peu cassé, un peu gris… tu peux faire tourner le truc, tu peux le
faire s'éclater, comme un hamburger qui s'éclate dans les vidéos 3D ». Donc : le shaker 3D (moteur/vorix.py) seul en
scène sur un papier gris clair, entrée en toupie, DEUX éclatés (le moteur, puis le démontage) avec la caméra qui plonge
sur la base et sur l'hélice, poudre aspirée par le vortex, gouttes d'eau sur l'éclaté final, recomposition sur « VORIX ».
Typo encre, pastilles blanches et noires, sous-titres encre. Voix Tomy inchangée (timing.json de la v3).
"""
import math, pathlib, sys, json, unicodedata
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
from moteur import *
from kit import Kit
from studio import lettres, SousTitresEncre
from studio3d import Cam, scene3d
import vorix as V

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 2.2, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a


def _n(x): return "".join(ch for ch in unicodedata.normalize("NFD", x.lower()) if ch.isalnum())
def trouve(mot, apres=-1.0):
    """t0 du premier mot égal à `mot` (sans accents ni ponctuation) qui commence après l'instant `apres`"""
    for m in K.mots:
        if m["t0"] > apres and _n(m["w"]) == _n(mot): return m["t0"]
    raise KeyError(mot)

T_MIEUX, T_MOTEUR = trouve("mieux"), trouve("moteur")
T_BASE, T_WATTS = trouve("dans"), trouve("quatre")
T_HELICE, T_CREE, T_VORTEX, T_DISSOUT = trouve("hélice"), trouve("crée"), trouve("vortex"), trouve("dissout")
T_ZERO1, T_ZERO2, T_SECOUER = trouve("coller"), trouve("plus"), trouve("secouer")
T_CINQ, T_TRITAN, T_BATT = trouve("cinq"), trouve("tritan"), trouve("batterie")
T_FINI, T_DEMONTE = trouve("fini"), trouve("démonte")
T_P_BASE, T_P_CORPS = trouve("base", T_DEMONTE), trouve("corps", T_DEMONTE)
T_P_HELICE, T_P_COUV = trouve("l'hélice", T_DEMONTE), trouve("couvercle", T_DEMONTE)
T_PASSE, T_EAU, T_VORIX = trouve("passe"), trouve("l'eau"), trouve("vorix")
FIN_VOIX = K.mots[-1]["t1"]

# ─────────────────────────────────────────── palette « studio clair »
ENCRE, GRIS, ACCENT, BLANC = "#141821", "#6B7280", "#1F6BFF", "#FFFFFF"
V.CORPS.update(bas="#242D38", haut="#66768A", alpha=0.36, spec=0.70, contre=0.45)   # verre lisible sur le papier gris
ST = SousTitresEncre(K, y=1410, larg=640, taille=46, fam="gras", max_mots=4, cx=500)

# sons et respirations
# plus de bruit de transition ni d'impact (règle du 30/10/2026) : seuls les petits pops des bénéfices, discrets
for t0 in (T_MOTEUR, T_CREE, T_DEMONTE, T_VORIX):
    rapide(t0 - 0.05, t0 + 0.14); eclair(t0, BLANC, 0.55)
for t0 in (T_BASE, T_HELICE, T_ZERO1, T_CINQ, T_SECOUER): rapide(t0 - 0.04, t0 + 0.08)
for t0 in (T_WATTS, T_VORTEX, T_TRITAN, T_BATT, T_P_BASE, T_P_CORPS, T_P_HELICE, T_P_COUV): son(t0, "pop", -8)
son(T_EAU, "verre", -12)
son(T_VORIX + 0.5, "ding", -8)


# ─────────────────────────────────────────── décor
def fond_clair(c, t):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)],
                                               [hexa("#F6F6F7"), hexa("#EAEBED"), hexa("#D8DADE")], [0.0, 0.5, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    p2 = peinture("#000000", 0.035); dy = (t * 10) % 48
    for y in range(-48, H + 48, 48):
        for x in range(24, W, 48): c.drawCircle(x, y + 24 - dy, 1.6, p2)


def halo(c, x, y, r, a):
    """la nappe grise derrière le produit : c'est elle qui fait lire le Tritan et l'impression blanche"""
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), r, [hexa("#8A9099", a), hexa("#8A9099", a * 0.55), hexa("#8A9099", 0.0)], [0.0, 0.45, 1.0]))
    c.drawCircle(x, y, r, p)


def ombre_sol(c, x, y, w, a):
    p = skia.Paint(AntiAlias=True, Color=hexa("#0A0D12", a), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, w * 0.07))
    c.drawOval(skia.Rect.MakeXYWH(x - w / 2, y - w * 0.10, w, w * 0.20), p)


def pill_c(c, label, cx, cy, taille=32, mode="clair", alpha=1.0, s=1.0):
    """pastille du thème clair : « clair » blanche à texte encre, « encre » noire, « accent » bleue"""
    if alpha <= 0.01 or s <= 0.01: return 0
    tw = largeur(label, taille, "fort", -0.01); h = taille * 2.0; w = tw + taille * 1.5
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        p = skia.Paint(AntiAlias=True, Color=hexa("#0B0F16", 0.16), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, taille * 0.45))
        c.save(); c.translate(0, taille * 0.35); c.drawRRect(rr, p); c.restore()
        fond, enc, bord = {"clair": (BLANC, ENCRE, "#D3D6DC"), "encre": (ENCRE, BLANC, None), "accent": (ACCENT, BLANC, None)}[mode]
        c.drawRRect(rr, peinture(fond))
        if bord: c.drawRRect(rr, peinture(bord, 1.0, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6))
        texte(c, label, -w / 2 + taille * 0.75, -hauteurLigne(taille, "fort") / 2, taille, enc, "fort", track=-0.01)
    c.restore()
    return w


def etiquette(c, t, t0, label, x, y, ax_, ay_, cote=1, fin=None, mode="clair"):
    """pastille reliée par un filet encre à un point du produit"""
    if t < t0 - 0.05: return
    e = prog(t, t0, 0.5, lambda u: ressort(u, 1.2, 5.0)) * (1.0 if fin is None else 1 - prog(t, fin, 0.25, entree))
    if e <= 0.01: return
    u = prog(t, t0 + 0.05, 0.35)
    trait(c, ax_, ay_, mix(ax_, x - cote * 150, u), mix(ay_, y, u), ENCRE, 2.4, 0.75 * e)
    c.drawCircle(ax_, ay_, 7, peinture(ENCRE, 0.95 * e))
    c.drawCircle(ax_, ay_, 7, peinture(BLANC, 0.95 * e, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
    pill_c(c, label, x, y, 32, mode, alpha=e, s=mix(0.8, 1.0, e))


def titre(c, s, t, t0, y, taille=108, fin=None, couleur=ENCRE):
    taille = ajuste(s, 640, taille, "noir", -0.02)
    a = 1.0 if fin is None else 1 - prog(t, fin, 0.25, entree)
    lettres(c, s, 500, y, taille, t, t0, "masque", fam="noir", couleur=couleur, grad=False, decal=0.028, duree=0.42, track=-0.02, alpha=a)


# ─────────────────────────────────────────── chorégraphie du produit
HH = 1150


def etat(t):
    """tous les paramètres du produit et de la caméra à l'instant t"""
    a_in = prog(t, 0.0, 0.85, lambda u: ressort(u, 1.1, 5.0))
    rot = (-14 + 10 * math.sin(t * 0.45) + 540 * (1 - prog(t, 0.0, 1.5, sortie))
           + 360 * prog(t, T_SECOUER - 0.1, 0.6, sortie) + 110 * prog(t, T_DEMONTE, 4.2, lambda u: u))
    ecl1 = prog(t, T_MOTEUR, 0.7, lambda u: ressort(u, 1.0, 5.0)) * (1 - prog(t, T_CREE, 0.55, lambda u: ressort(u, 1.0, 5.5)))
    ecl2 = prog(t, T_DEMONTE, 0.9, lambda u: ressort(u, 1.0, 5.0)) * (1 - prog(t, T_VORIX, 0.6, lambda u: ressort(u, 1.0, 5.5)))
    ecart = ecl1 * 0.85 + ecl2 * 1.3                     # amplitude réelle de l'éclaté (le ressort peut dépasser 1)
    # caméra : positions mesurées par projection (haut ≥ 205, bas sous les titres / au-dessus des sous-titres)
    tz, dy, ax = 860.0, -200.0, -5.0
    for t0, d, tz1, dy1, ax1 in ((T_MOTEUR, 0.6, 1450, -230, -5), (T_BASE, 0.6, 560, -680, -5), (T_HELICE, 0.6, 620, -345, -5),
                                 (T_CREE, 0.7, 860, -200, -5), (T_DEMONTE, 0.8, 1770, -199, -11), (T_VORIX, 0.7, 960, -210, -5)):
        k = prog(t, t0, d, sortie); tz, dy, ax = mix(tz, tz1, k), mix(dy, dy1, k), mix(ax, ax1, k)
    dy += mix(900, 0, a_in)
    dx = -170 * prog(t, T_CINQ - 0.2, 0.5, sortie) * (1 - prog(t, T_FINI, 0.5, sortie))
    niveau = prog(t, T_VORTEX, 1.0, sortie) * 0.55 * (1 - prog(t, T_DEMONTE - 0.3, 0.4))
    led = prog(t, T_WATTS, 0.3) * (0.6 + 0.4 * (0.5 + 0.5 * math.sin(t * 18))) * (1 - prog(t, T_DEMONTE - 0.3, 0.4))
    spin = 40.0 * (min(t, T_CINQ) - T_HELICE) if t >= T_HELICE else 0.0
    return dict(a_in=a_in, rot=rot, ecart=ecart, tz=tz, dy=dy, ax=ax, dx=dx, niveau=niveau, led=led, spin=spin,
                hh=HH * mix(0.92, 1.0, a_in))


def produit(c, e):
    cam = Cam(ax=e["ax"], ay=0, tz=e["tz"], cx=W / 2 + e["dx"], cy=H / 2 + e["dy"])
    rot = math.radians(e["rot"])
    scene3d(c, cam, V.shaker(cam, cy=0, h=e["hh"], rot=rot, ax=0, niveau=e["niveau"], led=e["led"],
                             eclate=1.0 if e["ecart"] > 0.001 else 0.0, ecart=max(e["ecart"], 0.001), rot_helice=rot + e["spin"], alpha=e["a_in"]))
    return cam


def pieces_y(e):
    """ordonnées (repère produit) du centre de chaque pièce, éclaté compris — mêmes formules que vorix.shaker"""
    h, E = e["hh"], e["ecart"]
    hb, hc, hk = h * V.Y_BASE, h * V.Y_CORPS, h * V.Y_COUV
    return dict(base=h / 2 - hb / 2 + E * h * 0.34, bas=h / 2 + E * h * 0.34, corps=h / 2 - hb - hc / 2,
                helice=h / 2 - hb - hc * 0.14 + E * h * 0.20 - hc * 0.09, couv=-h / 2 + hk / 2 - E * h * 0.30,
                liquide=h / 2 - hb - hc * borne(e["niveau"]) * 0.86)


# ─────────────────────────────────────────── matières : vortex, poudre, eau
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
        pa.setColor(hexa("#3C5A7C", 0.34 * k)); c.drawPath(path, pa)


_RNG = np.random.default_rng(11)
POUDRE = [(float(a), float(b), float(c_), float(d_)) for a, b, c_, d_ in zip(_RNG.uniform(0, 6.283, 48), _RNG.uniform(0.0, 0.5, 48), _RNG.uniform(0.55, 0.95, 48), _RNG.uniform(5, 10, 48))]
GOUTTES = [(float(a), float(b), float(c_), float(d_)) for a, b, c_, d_ in zip(_RNG.uniform(-0.9, 0.9, 44), _RNG.uniform(-0.5, 0.5, 44), _RNG.uniform(0.0, 0.7, 44), _RNG.uniform(14, 26, 44))]


def poudre(c, cam, e, t):
    """les grains tombent dans le corps, s'enroulent dans le vortex, se dissolvent"""
    t0, duree = T_VORTEX - 0.1, T_DISSOUT - T_VORTEX + 1.0
    d, py = e["hh"] * V.D_MM / V.H_MM, pieces_y(e)
    for ang0, dec, r0, taille in POUDRE:
        u = (t - t0 - dec) / duree
        if u <= 0 or u >= 1: continue
        y = mix(py["corps"] - e["hh"] * 0.26, py["liquide"] + 40, sortie(u))
        r = d * 0.5 * r0 * (1 - 0.85 * u ** 1.5)
        ang = ang0 + u * 11.0
        X, Y, Z = cam.proj((r * math.cos(ang), y, r * math.sin(ang)))
        kp = 1700.0 / (1700.0 + Z); a = (1 - u) ** 1.2 * 0.9
        c.drawCircle(X, Y, taille * 1.5 * kp * (1 - 0.6 * u), peinture("#A8895A", a))


def gouttes(c, cam, e, t):
    """l'eau qui traverse l'éclaté sur « sous l'eau »"""
    t0, duree = T_PASSE - 0.05, 1.25
    d, py = e["hh"] * V.D_MM / V.H_MM, pieces_y(e)
    for x0, z0, dec, long_ in GOUTTES:
        u = (t - t0 - dec * 0.6) / (duree * 0.55)
        if u <= 0 or u >= 1: continue
        y = mix(py["couv"] - e["hh"] * 0.45, py["bas"] + 60, u * u)
        X, Y, Z = cam.proj((x0 * d * 0.55, y, z0 * d * 0.5))
        kp = 1700.0 / (1700.0 + Z)
        a = min(1.0, u * 6) * (1 - u ** 3) * 0.85
        c.drawOval(skia.Rect.MakeXYWH(X - 4.5 * kp, Y - long_ * 1.3 * kp, 9 * kp, long_ * 2.6 * kp), peinture("#2F7FFF", a))
        c.drawCircle(X - 1.6 * kp, Y - long_ * 0.6 * kp, 2.0 * kp, peinture(BLANC, a * 0.9))
    # l'onde au sol quand l'eau touche
    u = prog(t, t0 + 0.35, 0.7)
    if 0 < u < 1:
        X, Y, Z = cam.proj((0, py["bas"] + 60, 0)); kp = 1700.0 / (1700.0 + Z)
        for j in range(2):
            uj = borne(u - 0.18 * j); r = d * kp * (0.3 + 0.9 * uj)
            pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0 * (1 - uj) + 0.5)
            pa.setColor(hexa("#3B8BFF", 0.55 * (1 - uj)))
            c.drawOval(skia.Rect.MakeXYWH(X - r, Y - r * 0.22, 2 * r, r * 0.44), pa)


def helice_vitesse(c, cam, e, k):
    """anneaux de vitesse autour de l'hélice quand elle tourne seule"""
    if k <= 0.01: return
    d, py = e["hh"] * V.D_MM / V.H_MM, pieces_y(e)
    X, Y, Z = cam.proj((0, py["helice"], 0)); kp = 1700.0 / (1700.0 + Z)
    for i in range(3):
        r = d * kp * (0.30 + 0.07 * i); a0 = (e["spin"] * 2.0 + i * 1.6) % 6.283
        path = skia.Path(); path.addArc(skia.Rect.MakeXYWH(X - r, Y - r * 0.28, 2 * r, r * 0.56), math.degrees(a0), 110)
        pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, StrokeCap=skia.Paint.kRound_Cap)
        pa.setColor(hexa(ACCENT, 0.55 * k * (1 - 0.25 * i))); c.drawPath(path, pa)


# ─────────────────────────────────────────── montage
def dessine(c, t):
    fond_clair(c, t)
    e = etat(t)
    sx, sy = 0.0, 0.0
    for t0 in (T_MOTEUR, T_CREE, T_DEMONTE, T_VORIX):
        a, b = secousse(t, t0, 16, 0.38); sx += a; sy += b
    c.save(); c.translate(sx, sy)

    # la nappe grise et l'ombre au sol, puis le produit
    cam0 = Cam(ax=e["ax"], ay=0, tz=e["tz"], cx=W / 2 + e["dx"], cy=H / 2 + e["dy"])
    py = pieces_y(e)
    d = e["hh"] * V.D_MM / V.H_MM
    X0, Y0, Z0 = cam0.proj((0, (py["couv"] + py["base"]) / 2, 0))
    halo(c, X0, Y0, 640 * 1700.0 / (1700.0 + Z0) + 140, 0.55 * e["a_in"])
    Xs, Ys, Zs = cam0.proj((0, py["bas"] + 14, 0)); ks = 1700.0 / (1700.0 + Zs)
    ombre_sol(c, Xs, Ys, d * ks * 1.55, 0.30 * e["a_in"])
    cam = produit(c, e)

    def pt(y, side=0.0, z=-0.5):
        return cam.proj((side * d * 0.5, y, z * d))

    # matières
    k_vx = prog(t, T_VORTEX, 0.5) * (1 - prog(t, T_CINQ, 0.4))
    vortex(c, cam, e, k_vx)
    poudre(c, cam, e, t)
    helice_vitesse(c, cam, e, prog(t, T_HELICE + 0.1, 0.3) * (1 - prog(t, T_CREE - 0.1, 0.3)))
    gouttes(c, cam, e, t)

    # 1. hook : la toupie, puis la question
    titre(c, "MIEUX QUE TA MAIN.", t, T_MIEUX, 1250, 100, fin=T_MOTEUR - 0.05)
    # 2. éclaté 1 : le moteur
    titre(c, "PARCE QU'IL A UN MOTEUR.", t, T_MOTEUR + 0.1, 1340, 84, fin=T_BASE - 0.05, couleur=ACCENT)
    # 3. la base, le moteur 4,5 W
    if T_BASE <= t < T_HELICE + 0.4:
        bx, by, _ = pt(py["base"], -0.45)
        etiquette(c, t, T_WATTS, "MOTEUR 4,5 W", 290, 1230, bx, by, cote=1, fin=T_HELICE, mode="encre")
    # 4. l'hélice qui tourne seule, puis le vortex
    if T_HELICE <= t < T_ZERO1 + 0.4:
        hx, hy, _ = pt(py["helice"], 0.30)
        etiquette(c, t, T_HELICE + 0.05, "HÉLICE", 700, 1180, hx, hy, cote=-1, fin=T_ZERO1, mode="encre")
    if T_VORTEX - 0.1 <= t < T_ZERO1 + 0.4:
        vx_, vy_, _ = pt(py["liquide"], 0.42)
        etiquette(c, t, T_VORTEX, "VORTEX", 700, 1300, vx_, vy_, cote=-1, fin=T_ZERO1, mode="accent")
    # 5. zéro grumeau, zéro bras
    titre(c, "RIEN NE COLLE AU FOND.", t, T_ZERO1, 1250, 92, fin=T_CINQ - 0.05)
    titre(c, "PLUS RIEN À SECOUER.", t, T_ZERO2, 1360, 92, fin=T_CINQ - 0.05, couleur=ACCENT)
    # 6. les trois chiffres de la fiche
    for k, (lab, t0, mode) in enumerate((("500 ML", T_CINQ, "encre"), ("CORPS TRITAN", T_TRITAN, "clair"), ("SE RECHARGE", T_BATT, "clair"))):
        if t < t0 - 0.05 or t > T_FINI + 0.4: continue
        a = prog(t, t0, 0.5, lambda u: ressort(u, 1.2, 5.0)) * (1 - prog(t, T_FINI, 0.25, entree))
        w = largeur(lab, 32, "fort", -0.01) + 48          # alignées à gauche sur x 600, hors du produit, sous x 984
        pill_c(c, lab, 600 + w / 2 + 140 * (1 - a), 540 + k * 118, 32, mode, alpha=a, s=mix(0.8, 1.0, a))
    # 7. éclaté 2 : une étiquette par pièce, sur son mot
    if T_DEMONTE <= t < T_VORIX + 0.3:
        fin = T_VORIX
        etiquette(c, t, T_P_COUV, "COUVERCLE À BEC", 740, 250, *pt(py["couv"], 0.35, -0.3)[:2], cote=-1, fin=fin)
        etiquette(c, t, T_P_CORPS, "CORPS 500 ML", 290, 700, *pt(py["corps"], -0.40)[:2], cote=1, fin=fin)
        etiquette(c, t, T_P_HELICE, "HÉLICE", 290, 960, *pt(py["helice"], -0.22, -0.2)[:2], cote=1, fin=fin)
        etiquette(c, t, T_P_BASE, "BASE MOTEUR", 290, 1270, *pt(py["base"], -0.40)[:2], cote=1, fin=fin)
    # 8. signature : le produit se recompose, le logo se pose en encre
    if t >= T_VORIX:
        a = prog(t, T_VORIX + 0.2, 0.5)
        V.logo(c, 500, 1330, 340, ENCRE, a)

    if T_BASE - 0.1 <= t < T_VORIX - 0.1 and not (T_ZERO1 <= t < T_CINQ):
        ST.dessine(c, t, ENCRE)
    c.restore()
    K.dessine_eclairs(c, t)
