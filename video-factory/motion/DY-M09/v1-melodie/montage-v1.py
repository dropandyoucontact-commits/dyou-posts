"""DY-M09 « Je t'emmène chez mes fournisseurs » — mini vlog DROP&YOU en Chine, voix off d'Avital (16/10/2026).

10 plans muets de Youssef (Avital + le masqué) : baskets (le lancer de paire = hook), motos, vestes, électronique, moto de
nuit, centre commercial, casino, hôtel, ascenseur, jet. Voix Mélodie (eleven_v4) phrase par phrase, le montage suit la voix
(`segments.json`, `voix_segments.py`, `assembler_voix.py`). Sources en 16:9 (1280×720 et 736×400) → 9:16 :
plein écran recadré (hook), cadre 4:5, carte 16:9 sur fond flouté, deux écrans l'un sous l'autre. Pas de musique
(Youssef la met dans CapCut).

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

DUREE = 43.0
T_FIN = 40.95
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
    elif p["mise"] == "duo":
        a, b = p["clips"]; ct = (t - p["t0"]) * p.get("vit", 1.0)
        ia, ib = img(a, ct), img(b, ct + p.get("dep_b", 0.0))
        fond(c, ia, sombre=0.5)
        poser(c, ia, HAUT, None, zoom=1.0 + 0.05 * u, rayon=30)
        poser(c, ib, BAS, None, zoom=1.05 - 0.05 * u, rayon=30)


# le hook : remap pour que la paire frappe l'écran sur « fournisseurs » et que la caméra tombe sur « En Chine »
T_IMPACT, T_CHUTE = 4.45, 5.45
PLANS = [
    dict(t0=0.0, t1=6.62, mise="plein", clip="c03", remap=[(0, 0), (T_IMPACT, 4.70), (T_CHUTE, 5.40), (6.62, 5.98)],
         cx=[(0, 900), (0.85, 900), (1.42, 520), (1.55, 600), (2.8, 600), (3.0, 560), (3.8, 590), (4.2, 650), (4.6, 600), (5.0, 620), (5.4, 640)]),
    dict(t0=6.62, t1=11.05, mise="carte", clip="c08", vit=4.0 / 4.6, cx=[(0, 368)]),
    dict(t0=11.05, t1=17.48, mise="cadre", clip="c01", vit=5.95 / 6.6, cx=[(0, 560), (2.6, 600), (3.4, 760), (4.3, 820), (5.0, 640), (5.6, 600)]),
    dict(t0=17.48, t1=24.18, mise="cadre", clip="c02", vit=5.95 / 6.9, cx=[(0, 600), (3, 620), (6, 600)]),
    dict(t0=24.18, t1=29.28, mise="carte", clip="c04", vit=5.0 / 5.3, cx=[(0, 365)]),
    dict(t0=29.28, t1=32.2, mise="duo", clips=("c06", "c07"), vit=0.95),
    dict(t0=32.2, t1=36.1, mise="duo", clips=("c09", "c05"), vit=0.95),
    dict(t0=36.1, t1=DUREE, mise="carte", clip="c10", vit=3.95 / 4.9, cx=[(0, 330)]),
]
# transitions : « fouet » (glissé flouté) ou « flash » (coupe franche + flash + coup de zoom)
TRANS = {6.62: "flash", 11.05: "fouet", 17.48: "fouet", 24.18: "fouet", 29.28: "flash", 32.2: "fouet_v", 36.1: "flash"}
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
    c.save(); c.translate(540, 370 - 20 * o); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
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
    lab = "Ajoute-moi sur DROP&YOU"; tl = 42
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


def dessin(c, t):
    video_a(c, t)
    # hook : le fournisseur masqué, la paire qui frappe l'écran, « EN CHINE »
    pastille(c, t, 0.2, 0.95, 540, 1080, "Mon fournisseur", "eye-off", ROUGE, rot=-4)
    pastille(c, t, T["paires"] - 0.05, 2.7, 540, 1420, "Mes paires", "flame", ORANGE, rot=3, depuis=1)
    fissure(c, t, 520, 940)
    if 5.5 <= t < 6.75:
        o = prog(t, 6.45, 0.15, entree)
        _calque_ombre(c)
        lettres(c, "EN CHINE.", 540, 700, 180, t, T["chine"] - 0.25, "ressort", fam="noir", couleur="#FFFFFF", grad=False,
                decal=0.03, alpha=1 - o)
        c.restore()
        b = prog(t, T["chine"] + 0.05, 0.3, sortie) * (1 - o)
        if b > 0: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(540 - 300 * b, 920, 600 * b, 18), 9, 9), peinture(ROUGE))
    # arrivée : Canton, minuit → demain matin
    pastille(c, t, T["canton"] - 0.05, 11.0, 540, 225, "Canton, Chine", "map-pin", ROUGE, rot=-3)
    horloge(c, t, T["minuit"] - 0.1, 11.0, T["demain"])
    # les fournisseurs
    entete(c, t, T["premier"], 17.45, 1, "Motos électriques", T["motos"] - 0.1)
    pastille(c, t, T["centaines"] - 0.05, 17.4, 540, 1430, "Des centaines", "boxes", ORANGE, rot=-3)
    entete(c, t, T["deuxième"], 24.15, 2, "Vestes", T["vestes"] - 0.1)
    liste(c, t, [("Matière", "hand", VIOLET, T["touche"]), ("Coutures", "scissors", BLEU, T["coutures"]),
                 ("Validé", "badge-check", VERT, T["accord"])], 24.1, 90, 1360, pas=96, taille=40)
    entete(c, t, T["troisième"], 29.25, 3, "Électronique", T["l'électronique"] - 0.1)
    pastille(c, t, T["cartons"] - 0.05, 29.2, 540, 1490, "Par cartons entiers", "package", OR, rot=3, depuis=1)
    # le soir
    pastille(c, t, T["soir"] - 0.05, 32.15, 540, 230, "Le soir", "moon", VIOLET, rot=-3)
    pastille(c, t, T["fête"] - 0.05, 36.05, 540, 230, "On fête ça", "sparkles", OR, rot=3, depuis=1)
    # appel à l'action
    pastille(c, t, T["produits"] - 0.1, T_FIN - 0.1, 540, 250, "Les mêmes produits", "shopping-bag", VIOLET, rot=-3)
    pastille(c, t, T2["fournisseurs"] - 0.05, T_FIN - 0.1, 540, 380, "Mes fournisseurs", "users", ROUGE, rot=3, depuis=1)
    if t >= T_FIN - 0.05:
        voile = prog(t, T_FIN - 0.05, 0.35)
        c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=hexa("#000000", 0.45 * voile)))
    logo_fin(c, t, T_FIN, y=780, larg=640)
    bouton_ajoute(c, t, T["ajoute-moi"] - 0.05, mix(1490, 1060, prog(t, T_FIN + 0.05, 0.4, entreeSortie)))
    edit.Y_SOUS = {"duo": 952, "carte": 1370}.get(plan_a(t)["mise"], 1250)
    sous_titres(c, t, GS, masque=[(5.5, 6.75), (T_FIN - 0.05, DUREE + 1)])


COUPS = [(T["paires"], 0.04), (T["canton"], 0.04), (T["motos"], 0.04), (T["centaines"], 0.03), (T["vestes"], 0.04),
         (T["accord"], 0.04), (T["l'électronique"], 0.04), (T["cartons"], 0.04), (T["fête"], 0.05), (T2["fournisseurs"], 0.04)] + \
        [(tc, 0.07) for tc, g in TRANS.items() if g == "flash"] + [(T_IMPACT, 0.09)]

# ─────────────────────────────────────────── rendu
SFX = []
def son_(t, nom, g): SFX.append((round(t, 3), nom, g))

for tc, g in TRANS.items():
    if g.startswith("fouet"): son_(tc - 0.16, "whoosh_court", -18)
    else: son_(tc - 0.12, "whoosh", -19); son_(tc, "impact_doux", -20)
son_(3.95, "whoosh", -17)                                       # le lancer
son_(T_IMPACT, "impact", -13); son_(T_IMPACT + 0.01, "verre", -15)
son_(T_CHUTE - 0.05, "whoosh_bas", -18); son_(T["chine"] - 0.2, "impact_doux", -17)
for t0 in (0.2, T["paires"] - 0.05, T["canton"] - 0.05, T["centaines"] - 0.05, T["cartons"] - 0.05, T["soir"] - 0.05, T["fête"] - 0.05,
           T["produits"] - 0.1, T2["fournisseurs"] - 0.05):
    son_(t0, "pop", -20)
for k_ in range(0, 9): son_(T["demain"] + k_ * 0.06, "tick", -27)
for t0 in (T["premier"], T["deuxième"], T["troisième"]): son_(t0 - 0.05, "pop", -19)
for t0 in (T["touche"], T["coutures"], T["accord"]): son_(t0, "check", -21)
son_(T["ajoute-moi"] - 0.05, "pop", -18); son_(T["ajoute-moi"] + 0.45, "clic", -17)
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
