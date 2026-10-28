"""DY-M21 « Viens par ici » — Léo (maillot Barça) présente une tablette à écran vert (28/10/2026).

Rush de 10 s à 24 i/s, voix remplacée par le clone de Léo (accent espagnol, R roulés) avant ce montage.
Dans la tablette, en paysage, un montage motion qui ne s'arrête jamais :
  0,0 → 1,8   signature DROP&YOU (aspiration → explosion → logo en 3D)
  1,8 → 5,1   appli DROP&YOU : en-tête logo + carrousel de BASKETS (articles récents du 20/10) qui dérive,
              puis suit le doigt quand il touche (3,92-4,40)
  4,76 → 5,10 le doigt pousse vers la droite → la page glisse : vidéo des CARTONS (« je travaille en Chine »)
  6,05        tap du doigt sur la vidéo : onde + pastille
  7,50 → 7,70 nouvelle poussée → page VESTES (articles récents), carrousel qui suit le doigt (8,42-8,60)
  8,60 → 10   signature DROP&YOU de fin
Le suivi de l'écran vient de suivi_tab.py (coins reconstruits depuis le coin haut-droit, jamais caché) ;
le détourage du vert laisse la main et les reflets DEVANT le contenu. Les gestes du doigt sont lus dans
suivi/doigt.json (centroïde du trou non vert par image) et convertis dans le repère de l'écran.
"""
import functools, json, math, pathlib, sys
import numpy as np
import skia, cv2
from PIL import Image

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
moteur.PROJET = P
from moteur import *
from studio import eclats, rayons, lueur_s
from signature import signature, sons_signature

DUREE = 10.5                       # 10 s de rush + 0,5 s sur la dernière image : la signature de fin se pose
NB_IMAGES = round(DUREE * FPS)
SFX, RAPIDE = [], []
def son(t, nom, g=0.0):
    if 0 <= t < DUREE: SFX.append((round(t, 3), nom, g))
def rapide(a, b): RAPIDE.append((a, b))
def flou_a(t): return 5 if any(a <= t <= b for a, b in RAPIDE) else 1

# ───────────────────────────── le rush et son suivi
RUSH, FPS_R, N_R, ECH_R = "leo-barca", 24.0, 240, 1.5
SW, SH = 1200, 900                                   # l'écran de la tablette, 4:3 en paysage
_Q = np.array(json.load(open(P / "suivi" / f"{RUSH}.json"))["coins"])
_D = json.load(open(P / "suivi" / "doigt.json"))     # [i, x0, x1, y0, y1, occlusion, cx, cy, ymin] en pixels source
_OCC = np.array([r[5] for r in _D], float)
_CX = np.array([r[6] for r in _D], float); _CY = np.array([r[7] for r in _D], float)
for a in (_CX, _CY):                                 # lissage sur 3 images
    b = a.copy()
    for i in range(1, len(a) - 1): b[i] = 0.25 * a[i - 1] + 0.5 * a[i] + 0.25 * a[i + 1]
    a[:] = b

def _interp(arr, t):
    f = max(0.0, t * FPS_R); i = min(int(f), N_R - 1); j = min(i + 1, N_R - 1)
    return arr[i] * (1 - (f - i)) + arr[j] * (f - i)

def k_rush(t): return int(min(N_R - 1, max(0, t * FPS_R)))
def quad(t): return _interp(_Q, t)

@functools.lru_cache(maxsize=4096)
def _doigt_ecran(ti):
    """position du doigt dans le repère de l'écran (pixels du canevas SW×SH) à l'image ti (60 i/s)"""
    t = ti / FPS
    q = quad(t).astype(np.float32)
    M = cv2.getPerspectiveTransform(q, np.array([[0, 0], [SW, 0], [SW, SH], [0, SH]], np.float32))
    p = np.array([[[_interp(_CX, t) * ECH_R, _interp(_CY, t) * ECH_R]]], np.float32)
    u, v = cv2.perspectiveTransform(p, M)[0, 0]
    return float(u), float(v)

def doigt(t): return _doigt_ecran(int(round(t * FPS)))
def du(t, t0): return doigt(t)[0] - doigt(t0)[0]

@functools.lru_cache(maxsize=400)
def fond_rush(k): return skia.Image.open(str(P / "renders" / "cache-rush" / RUSH / f"{k + 1:05d}.jpg"))

@functools.lru_cache(maxsize=400)
def masque_rush(k):
    m = np.array(Image.open(P / "suivi" / RUSH / f"{k + 1:05d}.png").convert("L"))
    a = np.zeros(m.shape + (4,), np.uint8); a[..., 3] = m; a[..., :3] = m[..., None]
    return skia.Image.fromarray(a)

def pts(q): return [skia.Point(float(x), float(y)) for x, y in q]

# ───────────────────────────── gestes du doigt (lus dans le rush) et pages
T_APP = 1.80                       # la signature d'intro laisse la place à l'appli
SWIPES = [(4.76, 5.10, 1), (7.50, 7.70, 2)]          # (début, fin, page atteinte) : le doigt pousse vers la droite
DRAGS = {0: (3.92, 4.40), 2: (8.42, 8.60)}            # carrousel de la page qui suit le doigt
T_TAP = 6.08
T_FIN = 8.60                       # signature de fin (le doigt quitte l'écran à 8,67)
DERIVE = -26.0                     # px/s : les cartes glissent toujours un peu

def offset_pages(t):
    """décalage horizontal du pager : la page suivante est à GAUCHE et arrive quand le doigt pousse à droite"""
    o = 0.0
    for t0, t1, page in SWIPES:
        if t < t0: break
        base = (page - 1) * SW
        if t <= t1:
            o = base + borne(du(t, t0), 0, SW)
        else:
            d1 = borne(du(t1, t0), 0, SW)
            o = base + d1 + (SW - d1) * sortieExpo(borne((t - t1) / 0.42))
    return o

def offset_carrousel(t, page):
    o = DERIVE * max(0.0, t - T_APP)
    if page in DRAGS:
        t0, t1 = DRAGS[page]
        if t0 <= t <= t1: o += du(t, t0)
        elif t > t1:
            d1 = du(t1, t0); v1 = (du(t1, t0) - du(t1 - 0.08, t0)) / 0.08
            o += d1 + v1 * 0.30 * (1 - math.exp(-(t - t1) / 0.30))
    return o

# ───────────────────────────── contenu : produits
R = "produits/recents-2026-10/"
BASKETS = [R + "basket-chanel-blanche", R + "basket-dior-b30-grise", R + "basket-lv-skate-bleue",
           R + "basket-on-loewe-rose", R + "claquette-nocta-bleue"]
VESTES = [R + "veste-bresil-rose-hd", R + "veste-supreme-vanson-bleue", R + "veste-courreges-vinyle-noire",
          R + "doudoune-moncler-noire", R + "veste-supreme-vanson-noire", R + "doudoune-lv-grise-orange"]
PRODUITS_SIG = [(R + "basket-chanel-blanche", False), (R + "veste-bresil-rose-hd", False), (R + "montre-gmt-batman", False),
                (R + "casque-airpods-max-vert", False), (R + "basket-dior-b30-grise", False), (R + "doudoune-moncler-noire", False)]
LOGO = "logo-dy-blanc"
ACCENT, FOND, FOND2 = "#8FB4FF", "#0B0A1A", "#171433"

def fond_app(c, t):
    g = skia.Paint()
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(SW, SH)], [hexa(FOND2), hexa(FOND)], [0.0, 1.0]))
    c.drawRect(skia.Rect.MakeWH(SW, SH), g)
    lueur_s(c, SW * 0.78, SH * 0.1, 520, ACCENT, 0.16 + 0.04 * math.sin(t * 1.3))
    lueur_s(c, SW * 0.15, SH * 0.95, 420, "#7439FC", 0.14)

def verre(c, x, y, w, h, r=28, voile=0.10, lisere=0.32):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    p = skia.Paint(AntiAlias=True, Color=hexa("#05030A", 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    c.save(); c.translate(0, 10); c.drawRRect(rr, p); c.restore()
    c.drawRRect(rr, peinture("#FFFFFF", voile))
    c.save(); c.clipRRect(rr, doAntiAlias=True)
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.4, y + h)],
                                               [hexa("#FFFFFF", 0.18), hexa("#FFFFFF", 0.03), hexa("#FFFFFF", 0.0)], [0.0, 0.5, 1.0]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), g)
    c.restore()
    bp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0)
    bp.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + h)], [hexa("#FFFFFF", lisere), hexa("#FFFFFF", lisere * 0.3)], [0.0, 1.0]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 1, y + 1, w - 2, h - 2), r - 1, r - 1), bp)

def entete(c, t, page):
    """en-tête d'appli : logo DROP&YOU à gauche, onglets à droite"""
    image(c, LOGO, 44, 34, 48 * 900 / 179)
    onglets = ["Baskets", "Cartons", "Vestes"]
    x = SW - 44
    for i in range(len(onglets) - 1, -1, -1):
        s = onglets[i]; w = largeur(s, 26, "fort", -0.01) + 40
        x -= w
        act = 1.0 if i == page else 0.0
        rrect(c, x, 32, w, 50, 25, "#FFFFFF", 0.10 + 0.75 * act)
        texte(c, s, x + 20, 42, 26, FOND if act else "#FFFFFF", "fort", "gauche", -0.01, 0.9)
        x -= 12
    trait(c, 44, 108, SW - 44, 108, "#FFFFFF", 1.5, 0.14)

def carte_produit(c, nom, x, y, w, h, label, t, k):
    verre(c, x, y, w, h)
    iw, ih = taille_img(nom)
    zone_w, zone_h = w - 36, h - 126
    s = min(zone_w / iw, zone_h / ih)
    pw, ph = iw * s, ih * s
    dy = 6 * math.sin(t * 1.6 + k)
    ombre_sol(c, x + w / 2, y + 18 + zone_h - 4, pw * 0.42, 12, 0.35)
    image(c, nom, x + (w - pw) / 2, y + 18 + (zone_h - ph) / 2 + dy, pw)
    texte(c, label, x + 26, y + h - 100, 30, "#FFFFFF", "titre", "gauche", -0.02)
    disque(c, x + 34, y + h - 44, 6, "#4BE38A")
    texte(c, "Disponible", x + 50, y + h - 58, 22, "#FFFFFF", "moyen", "gauche", 0.0, 0.75)

def carrousel(c, t, page, noms, label):
    cw, ch, gap, y = 330, 600, 28, 160
    o = offset_carrousel(t, page)
    tot = len(noms) * (cw + gap)
    for k, nom in enumerate(noms):
        x = 44 + k * (cw + gap) + o
        x = ((x + cw + gap) % tot) - cw - gap + 44 if tot else x   # boucle infinie
        if x > SW or x + cw < 0: continue
        carte_produit(c, nom, x, y, cw, ch, label, t, k)

def page_baskets(c, t):
    fond_app(c, t); carrousel(c, t, 0, BASKETS, "Basket"); entete(c, t, 0)

def page_vestes(c, t):
    fond_app(c, t); carrousel(c, t, 2, VESTES, "Veste"); entete(c, t, 2)

def page_cartons(c, t):
    fond_app(c, t)
    t0 = SWIPES[0][0]
    tl = max(0.0, t - t0) % 2.4
    tl = tl if tl <= 1.2 else 2.4 - tl            # aller-retour sur les 1,2 premières secondes (après : boîtes de marque lisibles)
    z = 1.0 + 0.06 * borne((t - t0) / 3.0)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 110, SW, SH - 110))
    c.translate(SW / 2, SH / 2); c.scale(z, z); c.translate(-SW / 2, -SH / 2)
    video(c, "videos/cartons", 0, 0, SW, SH, tl, 1.0, boucle=False)
    c.restore()
    g = skia.Paint()
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, SH - 320), skia.Point(0, SH)], [hexa(FOND, 0.0), hexa(FOND, 0.85)], [0.0, 1.0]))
    c.drawRect(skia.Rect.MakeXYWH(0, SH - 320, SW, 320), g)
    # pastille qui apparaît au tap du doigt, onde sous le doigt
    a = prog(t, T_TAP, 0.35, lambda v: ressort(v, 1.3, 5))
    if a > 0:
        ux, uy = doigt(T_TAP + 0.05)
        onde(c, ux, uy, t, T_TAP, 10, 180, "#FFFFFF", 8, 0.55)
        c.save(); c.translate(ux + 40, uy - 120); c.scale(min(a, 1.08), min(a, 1.08))
        verre(c, 0, 0, 380, 110, 24, 0.14)
        disque(c, 40, 55, 9, "#4BE38A")
        texte(c, "Fournisseur validé", 64, 32, 30, "#FFFFFF", "titre", "gauche", -0.02)
        c.restore()
    b = prog(t, t0 + 0.5, 0.5)
    texte(c, "On travaille depuis la Chine", 44, SH - 150 + 20 * (1 - b), 46, "#FFFFFF", "titre", "gauche", -0.02, b)
    texte(c, "Chez toi en 8 à 12 jours", 44, SH - 92 + 20 * (1 - b), 30, ACCENT, "fort", "gauche", -0.01, b)
    entete(c, t, 1)

PAGES = [page_baskets, page_cartons, page_vestes]

def ecran_app(c, t):
    o = offset_pages(t)
    for i, page in enumerate(PAGES):
        x = -i * SW + o
        if x >= SW or x + SW <= 0: continue
        c.save(); c.translate(x, 0); c.clipRect(skia.Rect.MakeWH(SW, SH))
        page(c, t)
        c.restore()
    # ombre entre deux pages pendant la glisse
    if 0 < o % SW < SW:
        xs = (o % SW)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(xs - 60, 0), skia.Point(xs, 0)], [hexa("#000000", 0.0), hexa("#000000", 0.45)], [0.0, 1.0]))
        c.drawRect(skia.Rect.MakeXYWH(xs - 60, 0, 60, SH), g)

def ecran_signature(c, t, t0, phrase):
    c.drawRect(skia.Rect.MakeWH(SW, SH), peinture(FOND))
    lueur_s(c, SW / 2, SH / 2, 700, "#2A2360", 0.6)
    c.save(); c.clipRect(skia.Rect.MakeWH(SW, SH))
    signature(c, t, t0, PRODUITS_SIG, cx=SW / 2, cy=400, phrase=phrase, accent=ACCENT)
    c.restore()

def contenu(c, t):
    """tout ce qui se passe dans l'écran, en pixels SW×SH"""
    if t < T_APP + 0.4:
        ecran_signature(c, t, 0.0, "On travaille depuis la Chine")
    if T_APP <= t < T_FIN + 0.3:
        u = prog(t, T_APP, 0.4, sortieExpo)
        v = 1 - prog(t, T_FIN, 0.3, entree)
        c.save()
        c.translate(SW / 2, SH / 2); c.scale(mix(0.92, 1.0, u) * mix(0.9, 1.0, v), mix(0.92, 1.0, u) * mix(0.9, 1.0, v)); c.translate(-SW / 2, -SH / 2 + SH * (1 - u))
        with Calque(c, u * v):
            c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeWH(SW, SH), 24 * (1 - u * v) + 1, 24 * (1 - u * v) + 1), doAntiAlias=True)
            ecran_app(c, t)
        c.restore()
    if t >= T_FIN:
        with Calque(c, prog(t, T_FIN, 0.25)):
            ecran_signature(c, t, T_FIN, "On travaille depuis la Chine")

# ───────────────────────────── composition
def ecran_incruste(c, t):
    q = quad(t); k = k_rush(t)
    lp = skia.Path(); lp.addPoly(pts(q), True)
    p = skia.Paint(AntiAlias=True, Color=hexa("#9FB8FF", 0.22), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 36))
    p.setBlendMode(skia.BlendMode.kScreen)
    c.drawPath(lp, p)
    c.saveLayer(None)
    c.save()
    m = skia.Matrix(); m.setPolyToPoly([skia.Point(0, 0), skia.Point(SW, 0), skia.Point(SW, SH), skia.Point(0, SH)], pts(q)); c.concat(m)
    c.clipRect(skia.Rect.MakeWH(SW, SH))
    contenu(c, t)
    g = skia.Paint(AntiAlias=True)   # reflet de vitre
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(SW, SH * 0.7)],
                                               [hexa("#FFFFFF", 0.10), hexa("#FFFFFF", 0.0), hexa("#FFFFFF", 0.04), hexa("#FFFFFF", 0.0)], [0.0, 0.35, 0.36, 0.6]))
    c.drawRect(skia.Rect.MakeWH(SW, SH), g)
    c.restore()
    pm = skia.Paint(); pm.setBlendMode(skia.BlendMode.kDstIn)    # le vert seulement : main, cadre, reflets devant
    c.drawImageRect(masque_rush(k), skia.Rect.MakeXYWH(0, 0, 1080, 1920), moteur._ECH, pm)
    c.restore()

def dessine(c, t):
    t = borne(t, 0.0, DUREE - 1 / FPS)
    c.drawImageRect(fond_rush(k_rush(t)), skia.Rect.MakeWH(1080, 1920), moteur._ECH, skia.Paint())
    ecran_incruste(c, t)

# ───────────────────────────── sons et flou
sons_signature(son, 0.0)
son(T_APP, "whoosh_court", -12)
for t0, t1, _ in SWIPES:
    son(t0 + 0.05, "swipe", -10); rapide(t0, t1 + 0.3)
for t0, t1 in DRAGS.values(): son(t0 + 0.05, "tick", -16)
son(T_TAP, "clic", -12); son(T_TAP + 0.1, "pop", -14)
sons_signature(son, T_FIN)
