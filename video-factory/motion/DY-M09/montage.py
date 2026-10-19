"""DY-M09 v2 « Je vous emmène chez mes fournisseurs » — mini vlog DROP&YOU en Chine, voix off d'Avital (16/10/2026).

v1 (voix Mélodie, 43 s) gardée dans v1-melodie/. v2 demandée par Youssef : voix plus jeune, cassée, dynamique (voix dessinée
« Avital vlog » zchjMHCgSyHNevwHbPa9), parole continue au tempo d'un vrai vlog (reference/vlog.mov), texte plus long, et des
passages en motion design (fond noir ou blanc) pour expliquer et combler quand il n'y a pas assez d'images ; les plans
« lifestyle » (casino, hôtel…) tournent pendant qu'elle parle d'autre chose. Hook inchangé : la paire lancée sur l'objectif.

10 plans muets (Avital + le masqué), sources 16:9 (1280×720 et 736×400) → 9:16 : plein écran recadré (hook), cadre 4:5,
carte large sur fond flouté, deux écrans l'un sous l'autre. Pas de musique (Youssef la met dans CapCut).

    /usr/bin/python3 montage.py apercu 0.5 4.5 …   → apercus/planche.jpg
    /usr/bin/python3 montage.py video               → renders/image.mp4
    /usr/bin/python3 montage.py son                 → video/DY-M09.mp4
"""
import json, math, pathlib, subprocess, sys
import numpy as np, skia
P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur, edit
from edit import groupes, sous_titres, pastille, liste, logo_fin, mesure, _ombre_rr, _calque_ombre, SONS, VOLUME_LUFS, W, H, FPS, JAUNE, POLICE
from moteur import prog, entree, sortie, entreeSortie, rebond, borne, mix, hexa, texte, largeur, hauteurLigne, icone, peinture, Calque
from studio import lettres
moteur.PROJET = P

DUREE = 64.3
T_FIN = 60.15
CUB = skia.SamplingOptions(skia.CubicResampler.Mitchell())
LIN = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)
VIOLET, VERT, OR, ROUGE, ORANGE, BLEU = "#7C3AED", "#16A34A", "#E8A317", "#E5484D", "#F97316", "#2563EB"

# mots de la voix (temps absolus) ; « Drop and You » s'écrit DROP&YOU
_m = json.load(open(P / "mots.json"))
MOTS, k = [], 0
while k < len(_m):
    w, t = _m[k]
    if w == "Drop" and k + 2 < len(_m) and _m[k + 1][0] == "and":
        MOTS.append(("DROP&YOU.", t)); k += 3; continue
    MOTS.append((w, t)); k += 1
T, T2 = {}, {}
for m, t in MOTS: T.setdefault(m.strip(".,!?…: ").lower(), t); T2[m.strip(".,!?…: ").lower()] = t
GS = groupes(MOTS, fin=T_FIN)


def Tm(mot, apres=0.0):
    """temps du premier « mot » prononcé après `apres`"""
    return next(t for m, t in MOTS if m.strip(".,!?…: ").lower() == mot and t >= apres)

# ─────────────────────────────────────────── les images des clips (extraites à 30 i/s dans images/cNN/)
NB = {d.name: len(list(d.glob("*.jpg"))) for d in (P / "images").iterdir() if d.is_dir()}
_cache = {}


def img(clip, ct):
    i = min(NB[clip], max(1, int(round(ct * FPS)) + 1))
    if (clip, i) not in _cache:
        if len(_cache) > 60: _cache.clear()
        _cache[(clip, i)] = skia.Image.open(str(P / "images" / clip / f"{i:04d}.jpg"))
    return _cache[(clip, i)]


def courbe(cles, x):
    """interpolation lissée entre des clés [(x, y)]"""
    if x <= cles[0][0]: return cles[0][1]
    for (x0, y0), (x1, y1) in zip(cles, cles[1:]):
        if x <= x1: return mix(y0, y1, entreeSortie((x - x0) / (x1 - x0)))
    return cles[-1][1]


def lineaire(cles, x):
    if x <= cles[0][0]: return cles[0][1]
    for (x0, y0), (x1, y1) in zip(cles, cles[1:]):
        if x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return cles[-1][1]


# ─────────────────────────────────────────── mises en page 9:16
def fond(c, im, cx=None, sombre=0.42):
    """l'image elle-même, très agrandie et floutée, qui remplit l'écran derrière une carte"""
    s = skia.Surface(135, 240); k_ = s.getCanvas()
    iw, ih = im.width(), im.height(); sc = max(135 / iw, 240 / ih) * 1.2
    k_.translate(67.5, 120); k_.scale(sc, sc); k_.translate(-(cx if cx else iw / 2), -ih / 2)
    k_.drawImage(im, 0, 0, LIN)
    p = skia.Paint(ImageFilter=skia.ImageFilters.Blur(5, 5, skia.TileMode.kClamp))
    c.save(); c.scale(8, 8); c.drawImage(s.makeImageSnapshot(), 0, 0, LIN, p); c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=hexa("#000000", sombre)))


def poser(c, im, rect, cx, cy=None, zoom=1.0, rayon=0):
    """remplit rect avec l'image (recadrée autour de cx, cy, sans sortir de l'image)"""
    x, y, w, h = rect
    iw, ih = im.width(), im.height()
    s = max(w / iw, h / ih) * zoom
    vw, vh = w / s, h / s
    cx = min(max(cx if cx is not None else iw / 2, vw / 2), iw - vw / 2)
    cy = min(max(cy if cy is not None else ih / 2, vh / 2), ih - vh / 2)
    r = skia.Rect.MakeXYWH(x, y, w, h)
    if rayon:
        rr = skia.RRect.MakeRectXY(r, rayon, rayon); _ombre_rr(c, rr, 0.45, 14, 26)
    c.save()
    if rayon: c.clipRRect(skia.RRect.MakeRectXY(r, rayon, rayon), True)
    else: c.clipRect(r)
    c.translate(x + w / 2, y + h / 2); c.scale(s, s); c.translate(-cx, -cy)
    c.drawImage(im, 0, 0, CUB); c.restore()


CARTE = (24, 500, 1032, 780)                    # carte large au milieu (les 736×400 recadrés autour de cx)
CADRE = (24, 430, 1032, 1290)                   # 4:5
HAUT, BAS = (24, 300, 1032, 640), (24, 964, 1032, 640)


def ct_de(p, t):
    """temps dans le clip : ralenti/accéléré pour remplir le créneau, ou remappé (hook)"""
    if "remap" in p: return lineaire(p["remap"], t - p["t0"])
    return (t - p["t0"]) * p.get("vit", 1.0) + p.get("dep", 0.0)


def dessine_plan(c, p, t):
    u = borne((t - p["t0"]) / (p["t1"] - p["t0"]))
    if p["mise"] == "plein":
        ct = ct_de(p, t); im = img(p["clip"], ct)
        poser(c, im, (0, 0, W, H), courbe(p["cx"], ct), zoom=1.0 + 0.03 * u)
    elif p["mise"] == "cadre":
        ct = ct_de(p, t); im = img(p["clip"], ct); cx = courbe(p["cx"], ct)
        fond(c, im, cx); poser(c, im, CADRE, cx, zoom=1.0 + 0.05 * u, rayon=34)
    elif p["mise"] == "carte":
        ct = ct_de(p, t); im = img(p["clip"], ct)
        fond(c, im); poser(c, im, CARTE, p.get("cx", [(0, None)])[0][1], zoom=1.0 + 0.06 * u, rayon=34)
    elif p["mise"] in ("noir", "blanc"):
        c.clear(skia.Color(11, 11, 12) if p["mise"] == "noir" else skia.Color(244, 242, 238))
        p["motion"](c, t)
    elif p["mise"] == "duo":
        a, b = p["clips"]; ct = (t - p["t0"]) * p.get("vit", 1.0)
        ia, ib = img(a, ct), img(b, ct + p.get("dep_b", 0.0))
        fond(c, ia, sombre=0.5)
        poser(c, ia, HAUT, None, zoom=1.0 + 0.05 * u, rayon=30)
        poser(c, ib, BAS, None, zoom=1.05 - 0.05 * u, rayon=30)


# le hook : remap pour que la paire frappe l'écran sur « fournisseurs » et que la caméra tombe sur « En Chine »
T_IMPACT, T_CHUTE = 3.80, 4.55


def _plans():
    return [
        dict(t0=0.0, t1=5.55, mise="plein", clip="c03", remap=[(0, 0), (T_IMPACT, 4.70), (T_CHUTE, 5.40), (5.55, 5.98)],
             cx=[(0, 900), (0.85, 900), (1.42, 520), (1.55, 600), (2.8, 600), (3.0, 560), (3.8, 590), (4.2, 650), (4.6, 600), (5.0, 620), (5.4, 640)]),
        dict(t0=5.55, t1=11.25, mise="carte", clip="c08", vit=4.0 / 5.7, cx=[(0, 368)]),
        dict(t0=11.25, t1=16.45, mise="noir", motion=scene_canton),
        dict(t0=16.45, t1=24.1, mise="cadre", clip="c01", vit=5.95 / 7.65, cx=[(0, 560), (2.6, 600), (3.4, 760), (4.3, 820), (5.0, 640), (5.6, 600)]),
        dict(t0=24.1, t1=28.15, mise="blanc", motion=scene_unite),
        dict(t0=28.15, t1=34.97, mise="cadre", clip="c02", vit=5.95 / 6.82, cx=[(0, 600), (3, 620), (6, 600)]),
        dict(t0=34.97, t1=39.3, mise="carte", clip="c04", vit=1.15, cx=[(0, 365)]),
        dict(t0=39.3, t1=45.76, mise="noir", motion=scene_secret),
        dict(t0=45.76, t1=50.65, mise="duo", clips=("c06", "c07"), vit=0.8),
        dict(t0=50.65, t1=55.5, mise="duo", clips=("c09", "c05"), vit=0.8),
        dict(t0=55.5, t1=DUREE, mise="carte", clip="c10", vit=3.95 / 4.7, cx=[(0, 330)]),
    ]


# transitions : « fouet » (glissé flouté), « fouet_v » (vertical) ou « flash » (coupe franche + flash + coup de zoom)
TRANS = {5.55: "flash", 11.25: "flash", 16.45: "fouet", 24.1: "fouet_v", 28.15: "fouet", 34.97: "fouet", 39.3: "flash", 45.76: "flash",
         50.65: "fouet_v", 55.5: "flash"}
FOUET = 0.32


def plan_a(t):
    for p in PLANS:
        if p["t0"] <= t < p["t1"]: return p
    return PLANS[-1]


def coups(t):
    """coups de zoom sur les mots forts et aux flashs"""
    s = 1.0
    for tc, f in COUPS:
        if tc - 0.02 <= t <= tc + 0.9:
            u = (t - tc + 0.02) / 0.92
            s += f * (math.sin(math.pi * min(1, u * 3.2)) if u < 0.16 else (1 - (u - 0.16) / 0.84) ** 2)
    return s


def secousse(t):
    """la paire frappe l'objectif"""
    if not (T_IMPACT <= t < T_IMPACT + 0.5): return 0.0, 0.0
    a = (1 - (t - T_IMPACT) / 0.5) ** 2 * 34
    return a * math.sin(t * 97), a * math.cos(t * 83)


def surface_plan(p, t):
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.ColorBLACK)
    dessine_plan(c, p, t)
    return s.makeImageSnapshot()


def video_a(c, t):
    """le fond vidéo (plans + transitions + zooms + secousse)"""
    z = coups(t); dx, dy = secousse(t)
    c.save(); c.translate(540 + dx, 900 + dy); c.scale(z, z); c.translate(-540, -900)
    fait = False
    for tc, genre in TRANS.items():
        if genre.startswith("fouet") and tc - FOUET / 2 <= t < tc + FOUET / 2:
            i = next(k for k, p in enumerate(PLANS) if p["t0"] == tc)
            a, b = surface_plan(PLANS[i - 1], t), surface_plan(PLANS[i], t)
            u = entreeSortie((t - tc + FOUET / 2) / FOUET)
            fl = 70 * math.sin(math.pi * u)
            vert = genre == "fouet_v"
            filt = skia.Paint(ImageFilter=skia.ImageFilters.Blur(0.1 if vert else fl, fl if vert else 0.1, skia.TileMode.kClamp))
            if vert:
                c.drawImage(a, 0, -H * u, LIN, filt); c.drawImage(b, 0, H * (1 - u), LIN, filt)
            else:
                c.drawImage(a, -W * u, 0, LIN, filt); c.drawImage(b, W * (1 - u), 0, LIN, filt)
            fait = True; break
    if not fait:
        fl = 18 * prog(t, T_FIN - 0.05, 0.5)
        if fl > 0.2: c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.Blur(fl, fl, skia.TileMode.kClamp)))
        dessine_plan(c, plan_a(t), t)
        if fl > 0.2: c.restore()
    c.restore()
    # flashs blancs : changements de chapitre et impact
    for tc in [k_ for k_, g in TRANS.items() if g == "flash"] + [T_IMPACT]:
        if tc - 0.05 <= t <= tc + 0.24:
            a = (1 - abs(t - tc - 0.02) / 0.22) * (0.5 if tc == T_IMPACT else 0.55)
            if a > 0: c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=hexa("#FFFFFF", borne(a))))


# ─────────────────────────────────────────── le motion
def fissure(c, t, cx, cy):
    """vitre fissurée là où la paire frappe, jusqu'à la chute de la caméra"""
    if not (T_IMPACT <= t < T_CHUTE - 0.02): return
    a = prog(t, T_IMPACT, 0.05) * (1 - prog(t, T_CHUTE - 0.12, 0.1))
    rng = np.random.default_rng(7)
    c.save(); c.translate(cx, cy); s = mix(0.85, 1.0, prog(t, T_IMPACT, 0.08)); c.scale(s, s)
    sombre = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=hexa("#000000", 0.35 * a), StrokeJoin=skia.Paint.kRound_Join)
    clair = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=hexa("#FFFFFF", 0.9 * a), StrokeJoin=skia.Paint.kRound_Join)
    rayons = []
    for i in range(15):
        ang = i / 15 * 2 * math.pi + rng.uniform(-0.18, 0.18)
        L = rng.uniform(380, 1150); pts = [(0, 0)]; r = 0
        while r < L:
            r += rng.uniform(50, 120); an = ang + rng.uniform(-0.12, 0.12)
            pts.append((r * math.cos(an), r * math.sin(an)))
        rayons.append(pts)
    chem = skia.Path()
    for pts in rayons:
        chem.moveTo(*pts[0])
        for q in pts[1:]: chem.lineTo(*q)
    for R in (70, 165, 300):                       # anneaux brisés entre les rayons
        for pts in rayons:
            if rng.uniform() < 0.65:
                ang0 = math.atan2(pts[1][1], pts[1][0])
                chem.moveTo(R * math.cos(ang0), R * math.sin(ang0))
                chem.lineTo(R * 1.08 * math.cos(ang0 + 0.38), R * 1.08 * math.sin(ang0 + 0.38))
    c.drawPath(chem, sombre); c.drawPath(chem, clair)
    p = skia.Paint(AntiAlias=True, Color=hexa("#FFFFFF", 0.55 * a), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
    c.drawCircle(0, 0, 46, p)
    c.restore()


def entete(c, t, t0, t1, num, titre, t_titre=None):
    """« FOURNISSEUR 0X » en pilule jaune + le produit en grand, en haut de l'écran"""
    a = prog(t, t0 - 0.05, 0.36, lambda v: rebond(v, 1.7)); o = prog(t, t1 - 0.15, 0.15, entree)
    if a <= 0 or o >= 1: return
    lab = f"FOURNISSEUR {num:02d}"; tl = 34
    w = largeur(lab, tl, "noir", 0.06) + 56; h = 64; y = 214
    c.save(); c.translate(540, y + h / 2 - 18 * o); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
    with Calque(c, borne(a * 3) * (1 - o)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        _ombre_rr(c, rr); c.drawRRect(rr, peinture(JAUNE))
        texte(c, lab, 0, -hauteurLigne(tl, "noir") / 2, tl, "#141414", "noir", "centre", 0.06)
    c.restore()
    tt = t_titre if t_titre is not None else t0 + 0.15
    if t >= tt - 0.05:
        _calque_ombre(c)
        lettres(c, titre, 540, 296 - 16 * o, 76, t, tt, "ressort", fam="noir", couleur="#FFFFFF", grad=False, decal=0.025,
                track=-0.01, alpha=1 - o)
        c.restore()


def horloge(c, t, t0, t1, t_bascule):
    """« minuit » → « demain matin » : l'heure qui défile de 00:00 à 09:00, la lune devient soleil"""
    a = prog(t, t0 - 0.05, 0.4, lambda v: rebond(v, 1.6)); o = prog(t, t1 - 0.15, 0.15, entree)
    if a <= 0 or o >= 1: return
    b = prog(t, t_bascule, 0.55, entreeSortie)
    minutes = int(9 * 60 * b) // 15 * 15
    h_ = f"{minutes // 60:02d}:{minutes % 60:02d}"
    c.save(); c.translate(540, 400 - 20 * o); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
    with Calque(c, borne(a * 3) * (1 - o)):
        _calque_ombre(c)
        tw = largeur("00:00", 132, "noir", -0.02)
        texte(c, h_, -tw / 2 + 50, -hauteurLigne(132, "noir") / 2, 132, "#FFFFFF", "noir", track=-0.02)
        c.restore()
        ic = "sun" if b > 0.5 else "moon"
        r = 46 * (1 - abs(b - 0.5) * 2 if 0 < b < 1 else 1) if 0 < b < 1 else 46
        disque_ = skia.Paint(AntiAlias=True, Color=hexa(OR if b > 0.5 else VIOLET))
        c.drawCircle(-tw / 2 - 30, 0, 50, disque_)
        icone(c, ic, -tw / 2 - 30, 0, 52 * borne(abs(b - 0.5) * 2) if 0 < b < 1 else 52, "#FFFFFF", 2.6)
    c.restore()


def bouton_ajoute(c, t, t0, cy):
    """« Ajoute-moi sur DROP&YOU » : pilule jaune, le + qui se remplit"""
    a = prog(t, t0, 0.36, lambda v: rebond(v, 1.8))
    if a <= 0: return
    lab = "Ajoutez-moi sur DROP&YOU"; tl = 42
    tw = largeur(lab, tl, POLICE, 0.0); h = 90; w = tw + 136
    clic = prog(t, t0 + 0.5, 0.1) * (1 - prog(t, t0 + 0.62, 0.14))
    s = mix(0.5, 1, a) * (1 - 0.06 * clic)
    c.save(); c.translate(540, cy + 5 * math.sin(t * 3)); c.scale(s, s)
    with Calque(c, borne(a * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        _ombre_rr(c, rr); c.drawRRect(rr, peinture(JAUNE))
        rempli = prog(t, t0 + 0.5, 0.2)
        c.drawCircle(-w / 2 + 54, 0, 26 * rempli, peinture("#141414"))
        icone(c, "circle-plus", -w / 2 + 54, 0, 52, "#FFFFFF" if rempli > 0.6 else "#141414", 2.6)
        texte(c, lab, -w / 2 + 96, -hauteurLigne(tl, POLICE) / 2, tl, "#141414", POLICE, track=0.0)
    c.restore()


# ─────────────────────────────────────────── scènes de motion (fond noir / blanc) : expliquer quand les images manquent
def _halo(c, cx, cy, r, coul, a):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(coul, a), hexa(coul, 0)], [0, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


def _points(c, t, coul="#FFFFFF", a=0.07):
    """trame de points qui dérive lentement (profondeur du fond)"""
    p = peinture(coul, a)
    dy = (t * 18) % 60
    for y in range(-60, H + 60, 60):
        for x in range(30, W, 60):
            c.drawCircle(x, y + dy, 2.2, p)


def scene_canton(c, t):
    """« Canton, c'est la capitale du business. Ce que vous achetez en ligne… ça part d'ici » : la ville, puis les produits
    du monde entier qui tournent autour de l'épingle et s'y engouffrent sur « d'ici »"""
    t_c, t_cap, t_ach, t_ici = Tm("canton", 11), Tm("capitale"), Tm("achetez"), Tm("d'ici")
    _points(c, t); _halo(c, 540, 760, 700, ROUGE, 0.22)
    _calque_ombre(c)
    lettres(c, "CANTON", 540, 300, 170, t, t_c - 0.1, "ressort", fam="noir", couleur="#FFFFFF", grad=False, decal=0.04)
    c.restore()
    # épingle qui tombe, anneaux qui pulsent
    a = prog(t, t_c - 0.05, 0.5, lambda v: rebond(v, 1.8))
    if a > 0:
        for k_ in range(3):
            ph = ((t - t_c) * 0.8 + k_ / 3) % 1
            c.drawCircle(540, 800, 60 + 260 * ph, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4,
                                                            Color=hexa(ROUGE, 0.5 * (1 - ph) * borne(a))))
        absorbe = prog(t, t_ici - 0.05, 0.25, rebond)
        c.save(); c.translate(540, 760 - 260 * (1 - borne(a))); s = a * (1 + 0.25 * math.sin(math.pi * borne(absorbe)))
        c.scale(s, s)
        c.drawCircle(0, 0, 92, peinture(ROUGE)); icone(c, "map-pin", 0, 0, 104, "#FFFFFF", 2.6)
        c.restore()
    pastille(c, t, t_cap - 0.05, 16.5, 540, 1160, "Capitale du business", "trending-up", VERT, rot=-3)
    # les produits en orbite, puis aspirés
    ics = [("shirt", VIOLET), ("headphones", BLEU), ("watch", OR), ("smartphone", "#141414"), ("shopping-bag", ROUGE),
           ("package", ORANGE), ("zap", VERT), ("gem", VIOLET)]
    rentre = prog(t, t_ici - 0.25, 0.4, entree)
    for k_, (ic, coul) in enumerate(ics):
        u = prog(t, t_ach - 0.05 + 0.09 * k_, 0.35, lambda v: rebond(v, 1.7))
        if u <= 0 or rentre >= 1: continue
        ang = k_ / len(ics) * 2 * math.pi + (t - t_ach) * 0.6
        r = 330 * (1 - rentre)
        x, y = 540 + r * math.cos(ang), 790 + r * 0.82 * math.sin(ang)
        s = u * (1 - rentre)
        c.save(); c.translate(x, y); c.scale(s, s)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-52, -52, 104, 104), 30, 30)
        _ombre_rr(c, rr, 0.4, 8, 16); c.drawRRect(rr, peinture("#FFFFFF"))
        icone(c, ic, 0, 0, 56, coul, 2.6)
        c.restore()
    if t >= t_ici:                                   # éclair d'absorption
        v = prog(t, t_ici + 0.08, 0.45)
        if 0 < v < 1:
            c.drawCircle(540, 760, 120 + 500 * v, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=10 * (1 - v),
                                                            Color=hexa("#FFFFFF", 0.8 * (1 - v))))


def _carte_achat(c, t, t0, cx, cy, lab, ic, coul, rot):
    a = prog(t, t0 - 0.05, 0.4, lambda v: rebond(v, 1.7))
    if a <= 0: return
    w, h = 420, 400
    c.save(); c.translate(cx, cy + 120 * (1 - borne(a))); c.rotate(rot * borne(a)); c.scale(mix(0.6, 1, a), mix(0.6, 1, a))
    with Calque(c, borne(a * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 44, 44)
        _ombre_rr(c, rr, 0.18, 18, 30); c.drawRRect(rr, peinture("#FFFFFF"))
        c.drawCircle(0, -50, 92, peinture(coul)); icone(c, ic, 0, -50, 96, "#FFFFFF", 2.6)
        texte(c, lab, 0, 90, 50, "#141414", "noir", "centre", -0.01)
    c.restore()


def scene_unite(c, t):
    """« Vous pouvez acheter à l'unité, en gros… et tout se négocie » : deux cartes et le tampon"""
    from kit import tampon
    _points(c, t, "#141414", 0.06)
    lettres(c, "ET LE MIEUX ?", 540, 290, 110, t, Tm("mieux") - 0.35, "ressort", fam="noir", couleur="#141414", grad=False, decal=0.03)
    _carte_achat(c, t, Tm("l'unité"), 300, 720, "À l'unité", "package", VIOLET, -4)
    _carte_achat(c, t, Tm("gros"), 780, 720, "En gros", "boxes", VERT, 4)
    tampon(c, "TOUT SE NÉGOCIE", 540, 1030, t, Tm("négocie"), taille=64, couleur=ROUGE, rot=-7, icone_="heart-handshake")
    # bande sombre sous les sous-titres (lisibles sur le blanc)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(110, 1250 - 58, 860, 116), 58, 58)
    c.drawRRect(rr, peinture("#141414", 0.92))


def scene_secret(c, t):
    """« Mon secret ? Je ne bosse jamais avec un inconnu. Chaque fournisseur : vu, testé, validé. »"""
    t_s, t_inc, t_ch = Tm("mon", 39), Tm("inconnu"), Tm("chaque")
    _points(c, t); _halo(c, 540, 700, 760, OR, 0.18)
    _calque_ombre(c)
    lettres(c, "MON SECRET", 540, 270, 140, t, t_s - 0.1, "ressort", fam="noir", couleur="#FFFFFF", grad=False, decal=0.035)
    c.restore()
    # l'inconnu barré
    a = prog(t, t_inc - 0.3, 0.4, lambda v: rebond(v, 1.7)); o = prog(t, t_ch - 0.1, 0.3, entree)
    if a > 0 and o < 1:
        c.save(); c.translate(540, 720 - 80 * o); s = mix(0.5, 1, a) * (1 - 0.5 * o); c.scale(s, s)
        with Calque(c, borne(a * 3) * (1 - o)):
            c.drawCircle(0, 0, 150, peinture("#2A2A2E")); icone(c, "user", 0, 0, 170, "#8A8A92", 2.4)
            x_ = prog(t, t_inc + 0.1, 0.25, sortie)
            if x_ > 0:
                p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=22, Color=hexa(ROUGE), StrokeCap=skia.Paint.kRound_Cap)
                c.drawLine(-120, -120, -120 + 240 * x_, -120 + 240 * x_, p)
            texte(c, "Jamais d'inconnu", 0, 190, 54, "#FFFFFF", "noir", "centre", -0.01)
        c.restore()
    liste(c, t, [("Vu", "eye", BLEU, Tm("vu")), ("Testé", "hand", ORANGE, Tm("testé")), ("Validé", "badge-check", VERT, Tm("validé"))],
          45.9, 330, 560, pas=160, taille=64)


def jour_un(c, t, t0, t1):
    """« CHINE · JOUR 1 » façon carnet de voyage, l'épingle rouge à gauche"""
    a = prog(t, t0 - 0.05, 0.42, lambda v: rebond(v, 1.7)); o = prog(t, t1 - 0.15, 0.15, entree)
    if a <= 0 or o >= 1: return
    c.save(); c.translate(540, 175 - 20 * o); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
    with Calque(c, borne(a * 3) * (1 - o)):
        _calque_ombre(c)
        w1 = largeur("CHINE", 96, "noir", -0.02)
        icone(c, "map-pin", -w1 / 2 - 50, 0, 84, ROUGE, 3.0)
        texte(c, "CHINE", -w1 / 2 + 10, -hauteurLigne(96, "noir") / 2, 96, "#FFFFFF", "noir", track=-0.02)
        c.restore()
        lab = "JOUR 1"; w = largeur(lab, 36, "noir", 0.08) + 50
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, 62, w, 58), 29, 29); _ombre_rr(c, rr); c.drawRRect(rr, peinture(JAUNE))
        texte(c, lab, 0, 91 - hauteurLigne(36, "noir") / 2, 36, "#141414", "noir", "centre", 0.08)
    c.restore()


def jauge(c, t, t0, t_haut, t1):
    """« du bas de gamme au très haut de gamme » : un curseur qui file de € à €€€€"""
    a = prog(t, t0 - 0.05, 0.35, lambda v: rebond(v, 1.6)); o = prog(t, t1, 0.15, entree)
    if a <= 0 or o >= 1: return
    c.save(); c.translate(540, 200); c.scale(mix(0.6, 1, a), mix(0.6, 1, a))
    with Calque(c, borne(a * 3) * (1 - o)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-430, -62, 860, 124), 62, 62); _ombre_rr(c, rr); c.drawRRect(rr, peinture("#FFFFFF"))
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(-300, 0), skia.Point(300, 0)], [hexa("#A1A1AA"), hexa(OR)]))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-300, -9, 600, 18), 9, 9), p)
        texte(c, "€", -360, -hauteurLigne(44, "noir") / 2, 44, "#71717A", "noir", "centre")
        texte(c, "€€€€", 362, -hauteurLigne(40, "noir") / 2, 40, OR, "noir", "centre", -0.04)
        x = mix(-300, 300, prog(t, t0 + 0.1, max(0.3, t_haut - t0), entreeSortie))
        c.drawCircle(x, 0, 30, peinture("#141414")); c.drawCircle(x, 0, 14, peinture(JAUNE))
    c.restore()


PLANS = _plans()


def dessin(c, t):
    video_a(c, t)
    # hook : le fournisseur masqué, la paire qui frappe l'écran, « EN CHINE »
    pastille(c, t, 0.15, 0.85, 540, 1080, "Mon fournisseur", "eye-off", ROUGE, rot=-4)
    pastille(c, t, T["paires"] - 0.05, 2.25, 540, 1420, "Mes paires", "flame", ORANGE, rot=3, depuis=1)
    fissure(c, t, 520, 940)
    if T_CHUTE - 0.05 <= t < 5.7:
        o = prog(t, 5.45, 0.15, entree)
        _calque_ombre(c)
        lettres(c, "EN CHINE.", 540, 700, 180, t, T["chine"] - 0.25, "ressort", fam="noir", couleur="#FFFFFF", grad=False,
                decal=0.03, alpha=1 - o)
        c.restore()
        b = prog(t, T["chine"] + 0.05, 0.3, sortie) * (1 - o)
        if b > 0: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(540 - 300 * b, 920, 600 * b, 18), 9, 9), peinture(ROUGE))
    # jour 1 : arrivée à minuit → demain matin
    jour_un(c, t, T["jour"], 11.25)
    horloge(c, t, T["minuit"] - 0.1, 11.25, T["demain"])
    # les fournisseurs
    entete(c, t, Tm("premier"), 24.08, 1, "Motos électriques", Tm("motos") - 0.1)
    pastille(c, t, Tm("centaines") - 0.05, 22.2, 540, 1430, "Par centaines", "boxes", ORANGE, rot=-3)
    pastille(c, t, Tm("impressionnant") - 0.4, 24.08, 540, 1430, "Encore mieux en vrai", "eye", VIOLET, rot=3, depuis=1)
    entete(c, t, Tm("deuxième"), 34.95, 2, "Vestes", Tm("vestes") - 0.1)
    liste(c, t, [("Matière", "hand", VIOLET, Tm("matière")), ("Coutures", "scissors", BLEU, Tm("coutures")),
                 ("Validé", "badge-check", VERT, Tm("accord"))], 34.9, 90, 1360, pas=96, taille=40)
    entete(c, t, Tm("troisième"), 39.28, 3, "Électronique", Tm("l'électronique") - 0.1)
    pastille(c, t, Tm("cartons") - 0.05, 39.25, 540, 1490, "Par cartons entiers", "package", OR, rot=3, depuis=1)
    # les plans « détente » tournent pendant qu'elle explique
    pastille(c, t, Tm("journée") - 0.05, 48.4, 540, 200, "Fin de journée", "sun", ORANGE, rot=-3)
    pastille(c, t, Tm("tout", 50) - 0.3, 51.25, 540, 200, "On trouve TOUT", "sparkles", VIOLET, rot=3, depuis=1)
    jauge(c, t, Tm("bas", 50), Tm("haut", 50), Tm("problème") - 0.3)
    pastille(c, t, Tm("problème") - 0.1, 55.45, 540, 200, "Le vrai problème : à qui parler ?", "circle-help", ROUGE, rot=-3, taille=40)
    # appel à l'action
    pastille(c, t, T["produits"] - 0.1, T_FIN - 0.1, 540, 250, "Les produits", "shopping-bag", VIOLET, rot=-3)
    pastille(c, t, T2["fournisseurs"] - 0.05, T_FIN - 0.1, 540, 380, "Mes fournisseurs", "users", ROUGE, rot=3, depuis=1)
    if t >= T_FIN - 0.05:
        voile = prog(t, T_FIN - 0.05, 0.35)
        c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=hexa("#000000", 0.45 * voile)))
    logo_fin(c, t, T_FIN, y=760, larg=640)
    bouton_ajoute(c, t, T["ajoutez-moi"] - 0.1, 1050)
    b = prog(t, T2["demain"] - 0.1, 0.35, sortie)
    if b > 0:
        _calque_ombre(c)
        texte(c, "À demain pour le jour 2", 540, 1170 + 16 * (1 - b), 46, "#FFFFFF", POLICE, "centre", 0.0, alpha=b)
        c.restore()
    pl = plan_a(t)["mise"]
    edit.Y_SOUS = {"duo": 952, "carte": 1370}.get(pl, 1250)
    sous_titres(c, t, GS, masque=[(T_CHUTE - 0.05, 5.6), (T_FIN - 0.05, DUREE + 1)])


COUPS = [(T["paires"], 0.04), (Tm("motos"), 0.04), (Tm("centaines"), 0.03), (Tm("impressionnant"), 0.04), (Tm("vestes"), 0.04),
         (Tm("accord"), 0.04), (Tm("l'électronique"), 0.04), (Tm("cartons"), 0.04), (Tm("tout", 50), 0.05), (Tm("parler"), 0.04),
         (T2["fournisseurs"], 0.04)] + [(tc, 0.07) for tc, g in TRANS.items() if g == "flash"] + [(T_IMPACT, 0.09)]

# ─────────────────────────────────────────── rendu
SFX = []
def son_(t, nom, g): SFX.append((round(t, 3), nom, g))

for tc, g in TRANS.items():
    if g.startswith("fouet"): son_(tc - 0.16, "whoosh_court", -18)
    else: son_(tc - 0.12, "whoosh", -19); son_(tc, "impact_doux", -20)
son_(T_IMPACT - 0.6, "whoosh", -17)                             # le lancer
son_(T_IMPACT, "impact", -13); son_(T_IMPACT + 0.01, "verre", -15)
son_(T_CHUTE - 0.05, "whoosh_bas", -18); son_(T["chine"] - 0.2, "impact_doux", -17)
for t0 in (0.15, T["paires"] - 0.05, T["jour"] - 0.05, Tm("capitale") - 0.05, Tm("centaines") - 0.05, Tm("impressionnant") - 0.4,
           Tm("cartons") - 0.05, Tm("journée") - 0.05, Tm("tout", 50) - 0.3, Tm("problème") - 0.1, T["produits"] - 0.1, T2["fournisseurs"] - 0.05):
    son_(t0, "pop", -20)
son_(Tm("canton", 11) - 0.1, "impact_doux", -18)
for k_ in range(8): son_(Tm("achetez") - 0.05 + 0.09 * k_, "blip", -25)
son_(Tm("d'ici") - 0.2, "whoosh_long", -20); son_(Tm("d'ici") + 0.05, "ching", -19)
for k_ in range(0, 9): son_(T["demain"] + k_ * 0.06, "tick", -27)
for t0 in (Tm("premier"), Tm("deuxième"), Tm("troisième")): son_(t0 - 0.05, "pop", -19)
for t0 in (Tm("matière"), Tm("coutures"), Tm("accord"), Tm("vu"), Tm("testé"), Tm("validé")): son_(t0, "check", -21)
son_(Tm("l'unité") - 0.05, "pop", -19); son_(Tm("gros") - 0.05, "pop", -19); son_(Tm("négocie") - 0.1, "tampon", -15)
son_(Tm("inconnu") + 0.1, "croc", -20)
son_(Tm("bas", 50), "montee", -22)
son_(T["ajoutez-moi"] - 0.1, "pop", -18); son_(T["ajoutez-moi"] + 0.4, "clic", -17)
son_(T_FIN, "whoosh", -18); son_(T_FIN + 0.08, "ching", -18)


def image_a(t):
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.ColorBLACK)
    dessin(c, t)
    return s.toarray(colorType=skia.kRGBA_8888_ColorType)


def apercu(temps):
    from PIL import Image, ImageDraw
    (P / "apercus").mkdir(exist_ok=True)
    vign = []
    for t in temps:
        im = Image.fromarray(image_a(t)[..., :3]); im.save(P / "apercus" / f"m_{t:05.2f}.jpg", quality=88)
        vign.append((t, im.resize((270, 480))))
    cols = min(6, len(vign)); lig = (len(vign) + cols - 1) // cols
    pl = Image.new("RGB", (cols * 272, lig * 482), (30, 30, 30)); d = ImageDraw.Draw(pl)
    for k_, (t, im) in enumerate(vign):
        x, y = (k_ % cols) * 272 + 1, (k_ // cols) * 482 + 1
        pl.paste(im, (x, y)); d.text((x + 5, y + 4), f"{t:.2f}", fill=(255, 0, 0))
    pl.save(P / "apercus" / "planche.jpg", quality=85)


def video():
    (P / "renders").mkdir(exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-vf", "unsharp=5:5:0.5:5:5:0.0", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart",
                            str(P / "renders" / "image.mp4")], stdin=subprocess.PIPE)
    for k_ in range(int(DUREE * FPS)):
        enc.stdin.write(image_a(k_ / FPS).tobytes())
        if k_ % 90 == 0: print(f"{k_ / FPS:.1f} s", flush=True)
    enc.stdin.close(); enc.wait()


def son():
    """voix d'Avital (nettoyée, compressée) + bruitages, volume final −13 LUFS / −1 dB ; pas de musique (CapCut)"""
    a = P / "audio"; a.mkdir(exist_ok=True)
    v = a / "voix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "voix" / "voix.wav"), "-af",
                    "highpass=f=90,equalizer=f=250:t=q:w=1.2:g=-1.5,equalizer=f=4000:t=q:w=1.0:g=2,equalizer=f=11000:t=h:w=0.7:g=1.5,"
                    "acompressor=threshold=0.08:ratio=3:attack=5:release=90:makeup=2",
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_f32le", str(v)], check=True)
    lire = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                                  capture_output=True).stdout, np.float32).copy()
    n = int(DUREE * 48000)
    x = lire(v); x *= 10 ** ((-16 - mesure(v)[0]) / 20); x = np.pad(x, (0, max(0, n - len(x))))[:n]
    if (P / "media" / "musique.mp3").exists() and "--sans-musique" not in sys.argv:
        print("musique ignorée : Youssef la met dans CapCut")
    for t0, nomson, g in SFX:
        s = lire(SONS / f"{nomson}.wav") * 10 ** (g / 20)
        i0 = int(t0 * 48000); i1 = min(n, i0 + len(s))
        if 0 <= i0 < n: x[i0:i1] += s[:i1 - i0]
    brut = a / "mix-brut.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", str(brut)],
                   input=x.astype(np.float32).tobytes(), check=True)
    mixw = a / "mix.wav"
    g = VOLUME_LUFS - mesure(brut)[0]
    for _ in range(3):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(brut), "-af",
                        f"aresample=192000,volume={g:.2f}dB,alimiter=limit=0.87:attack=0.5:release=40:level=false,"
                        "alimiter=limit=0.87:attack=0.1:release=20:level=false,aresample=48000,pan=stereo|c0=c0|c1=c0",
                        "-c:a", "pcm_s16le", str(mixw)], check=True)
        i_, _ = mesure(mixw)
        if abs(i_ - VOLUME_LUFS) < 0.25: break
        g += VOLUME_LUFS - i_
    (P / "video").mkdir(exist_ok=True)
    out = P / "video" / "DY-M09.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "renders" / "image.mp4"), "-i", str(mixw), "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    return out, mesure(out)


if __name__ == "__main__":
    if sys.argv[1] == "apercu": apercu([float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == "video": video()
    elif sys.argv[1] == "son": print(son())
