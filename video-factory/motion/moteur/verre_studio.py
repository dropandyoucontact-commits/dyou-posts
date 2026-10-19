"""Thème « verre clair » DYOU Agency (19/10/2026) — DA-M17-EN (motion) et DA-M18-EN (sites).

Demande de Youssef : garder tout de DA-M14-EN-v2 / DA-M16-EN-v2 (texte, voix, cartes en verre, vitrine de sites, rendu qui
avance, logiciels qui sortent) sauf les couleurs : retour au fond clair du studio (DA-M06-EN, DA-M09-EN : papier lavande,
dégradé violet → bleu), et une signature 3D à la fin, comme DY-M15 / GSX, aux couleurs de l'agence.

    from studio3d import *          # ou sites3d
    import verre_studio as vs
    vs.appliquer()                  # cartes blanches → verre clair à halo violet ; faux sites et posts restent tels quels
    vs.signature(c, t, t0, MEDIAS, lignes, cta)       # dans dessine(), par-dessus tout
    vs.sons_signature(son, t0)

Les cartes de Youssef (banque/glace) sont sombres : celles qui ne sont que de l'interface (rendu, outils, piste son,
fichier) sont redessinées en clair ; celles qui sont des écrans (vitrine de modèles, icônes de logiciels) gardent leur image,
posée dans un cadre de verre clair.
"""
import math, sys, contextlib
import numpy as np
import skia
import moteur
from moteur import *
import studio
from studio import S, GRAD, GRAD_VIF, pgrad, lueur_s, tuile, entre, eclats, rayons, bouton, curseur, clic, carte_s
from studio3d import Cam, Plan, coins, scene3d, rot3

ACCENT = "#7B3FF2"
G = dict(brut=0)
_ORIG = {}


def pgrad_(x0, y0, x1, y1, cols, alpha=1.0):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [hexa(col, alpha) for col in cols]))
    return p


# ─────────────────────────────────────────── le verre clair
def verre(c, x, y, w, h, r=34, alpha=1.0, lueur=1.0, ombre=1.0):
    """carte en verre dépoli blanc : ombre violette douce, halo violet, reflet en biais, liseré blanc → lilas"""
    if alpha <= 0.003 or w <= 1 or h <= 1: return
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    k = max(0.4, min(w, h) / 300)
    with Calque(c, alpha):
        if ombre > 0:
            p = skia.Paint(AntiAlias=True, Color=hexa("#4B2E9A", 0.16 * ombre), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26 * k))
            c.save(); c.translate(0, 20 * k); c.drawRRect(rr, p); c.restore()
        if lueur > 0:
            p = skia.Paint(AntiAlias=True, Color=hexa(ACCENT, 0.18 * lueur), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 18 * k))
            c.drawRRect(rr, p)
        c.drawRRect(rr, pgrad_(x, y, x + w * 0.5, y + h, ["#FFFFFF", "#F8F5FE", "#EFEAFB"], 0.9))
        c.save(); c.clipRRect(rr, doAntiAlias=True)
        rf = skia.Paint(AntiAlias=True)
        rf.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.5, y + h * 0.5)],
                                                    [hexa("#FFFFFF", 0.0), hexa("#FFFFFF", 0.95), hexa("#FFFFFF", 0.0)], [0.28, 0.35, 0.46]))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), rf)
        if lueur > 0:
            lb = skia.Paint(AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12 * k))
            lb.setShader(skia.GradientShader.MakeRadial(skia.Point(x + w / 2, y + h), w * 0.55, [hexa(ACCENT, 0.16 * lueur), hexa(ACCENT, 0.0)]))
            c.drawRect(skia.Rect.MakeXYWH(x, y + h - 70 * k, w, 70 * k), lb)
        c.restore()
        ep = max(1.5, 2.4 * k)
        li = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=ep)
        li.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w, y + h)],
                                                    [hexa("#FFFFFF", 1.0), hexa("#C9B6FF", 0.6), hexa("#FFFFFF", 0.9), hexa("#9C7BFF", 0.9)],
                                                    [0.0, 0.4, 0.7, 1.0]))
        c.drawRRect(rr, li)


def balayage(c, x, y, w, h, t, r=30, vitesse=0.45, a=0.6):
    """reflet blanc qui traverse la vitre"""
    u = (t * vitesse) % 1.6 - 0.3
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), doAntiAlias=True)
    p = skia.Paint(AntiAlias=True)
    x0 = x + w * u
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0 - 160, y), skia.Point(x0 + 160, y + 200)],
                                               [hexa("#FFFFFF", 0), hexa("#FFFFFF", a), hexa("#FFFFFF", 0)]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)
    c.restore()


@contextlib.contextmanager
def brut():
    """contenu « réel » (faux site, post) : cartes d'origine, pas de verre"""
    G["brut"] += 1
    try: yield
    finally: G["brut"] -= 1


def _blanc(col):
    return isinstance(col, str) and col.upper() in ("#FFFFFF", "#FFF")


def rrect_v(c, x, y, w, h, r, couleur, alpha=1.0, ombre=None, contour=None, ep=0):
    if not G["brut"] and _blanc(couleur) and w >= 90 and h >= 56:
        return verre(c, x, y, w, h, r, alpha, 0.8, 0.8)
    return _ORIG["rrect"](c, x, y, w, h, r, couleur, alpha, ombre, contour, ep)


def carte_s_v(c, x, y, w, h, r=34, fond="#FFFFFF", contour=None, ombre=0.11, alpha=1.0, ep=2):
    if not G["brut"] and _blanc(fond):
        return verre(c, x, y, w, h, r, alpha)
    return _ORIG["carte_s"](c, x, y, w, h, r, fond, contour, ombre, alpha, ep)


def _installe(nom, fn):
    for mod in list(sys.modules.values()):
        d = getattr(mod, "__dict__", None)
        if d is None or mod is sys.modules[__name__]: continue
        if nom in d and callable(d[nom]) and getattr(d[nom], "__module__", "") != __name__:
            _ORIG.setdefault(nom, d[nom])
            d[nom] = fn


def _brut_fab(nom):
    fab = _ORIG[nom]
    def fab2(*a, **k):
        f = fab(*a, **k)
        def g(c, w, h):
            with brut(): f(c, w, h)
        return g
    fab2.__module__ = __name__
    return fab2


def appliquer():
    for nom, fn in [("rrect", rrect_v), ("carte_s", carte_s_v)]:
        _installe(nom, fn)
    for nom in ("site_vieux", "site_moderne", "post_gris"):
        for mod in list(sys.modules.values()):
            d = getattr(mod, "__dict__", None)
            if d and nom in d and nom not in _ORIG: _ORIG[nom] = d[nom]
        if nom in _ORIG: _installe(nom, _brut_fab(nom))


# ─────────────────────────────────────────── cartes de Youssef, en clair
def _imgr(c, nom, x, y, w, h, alpha=1.0):
    i = moteur._img("glace/" + nom)
    p = skia.Paint(AntiAlias=True)
    if alpha < 1: p.setAlphaf(borne(alpha))
    c.drawImageRect(i, skia.Rect.MakeXYWH(x, y, w, h), moteur._ECH, p)


def taille_g(nom):
    i = moteur._img("glace/" + nom); return i.width(), i.height()


def barre(c, x, y, w, u, h=10):
    _ORIG.get("rrect", rrect)(c, x, y - h / 2, w, h, h / 2, S["lavande"])
    if u > 0.005:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - h / 2, max(h, w * u), h), h / 2, h / 2), pgrad(x, 0, x + w, 0, GRAD_VIF))
        lueur_s(c, x + w * u, y, h * 3, S["violetVif"], 0.45)


def _pose(c, cx, cy, s, rot, alpha):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    return Calque(c, alpha)


def carte_rendu(c, cx, cy, w, u, alpha=1.0, s=1.0, t=0.0):
    """« Rendering… » : la barre avance pour de vrai, le pourcentage suit ; à 100 % → « Completed! »"""
    if alpha <= 0.01 or s <= 0.01: return
    H_ = 168
    fini = borne((u - 0.98) * 50)
    with _pose(c, cx, cy, s, 0, alpha):
        verre(c, -w / 2, -H_ / 2, w, H_, 40)
        with Calque(c, 1 - fini):
            tuile(c, "clapperboard", -w / 2 + 80, 0, 92, "grad")
            x0 = -w / 2 + 150; x1 = w / 2 - 36
            texte(c, "Rendering…", x0, -56, 38, S["encre"], "titre", track=-0.02)
            texte(c, "Estimated time: 2 min", x0, -8, 26, S["gris"], "demi", track=-0.01)
            texte(c, f"{int(u * 100)}%", x1, -50, 34, S["violetFonce"], "titre", "droite", -0.02)
            barre(c, x0, 48, x1 - x0, u, 12)
        if fini > 0:
            with Calque(c, fini):
                z = mix(0.6, 1, prog(fini, 0, 1, sortie))
                disque(c, -w / 2 + 80, 0, 46 * z, S["vert"])
                icone(c, "check", -w / 2 + 80, 0, 54 * z, "#FFFFFF", 3.4)
                texte(c, "Completed!", -w / 2 + 150, -46, 40, S["encre"], "titre", track=-0.02)
                texte(c, "Your video is ready", -w / 2 + 150, 4, 28, S["gris"], "demi", track=-0.01)
                icone(c, "chevron-right", w / 2 - 60, 0, 44, S["violet"], 2.6)
        balayage(c, -w / 2, -H_ / 2, w, H_, t, 40)
    c.restore()


def carte_outils(c, cx, cy, w, alpha=1.0, s=1.0, rot=0.0, t=0.0):
    """la barre d'outils d'un logiciel d'animation ; l'outil actif passe de l'un à l'autre"""
    if alpha <= 0.01 or s <= 0.01: return
    ics = ["crop", "square-dashed", "type", "pencil", "square"]
    h = w * 0.22; pas = (w - 40) / len(ics)
    actif = int(t * 2.2) % len(ics)
    with _pose(c, cx, cy, s, rot, alpha):
        verre(c, -w / 2, -h / 2, w, h, h / 2)
        for j, ic in enumerate(ics):
            x = -w / 2 + 20 + pas * (j + 0.5)
            if j == actif:
                c.drawRoundRect(skia.Rect.MakeXYWH(x - h * 0.36, -h * 0.36, h * 0.72, h * 0.72), h * 0.2, h * 0.2, pgrad(x - h * 0.36, -h * 0.36, x + h * 0.36, h * 0.36, GRAD_VIF))
            icone(c, ic, x, 0, h * 0.42, "#FFFFFF" if j == actif else S["encre"], 2.4)
        balayage(c, -w / 2, -h / 2, w, h, t, h / 2)
    c.restore()


def carte_onde(c, cx, cy, w, alpha=1.0, s=1.0, rot=0.0, t=0.0):
    """la piste son : forme d'onde violette qui vit, durée, bouton lecture"""
    if alpha <= 0.01 or s <= 0.01: return
    h = w * 0.15
    with _pose(c, cx, cy, s, rot, alpha):
        verre(c, -w / 2, -h / 2, w, h, h / 2)
        x0, x1 = -w / 2 + h * 0.55, w / 2 - h * 1.9
        n = 64; lb = (x1 - x0) / n
        tete = (t * 0.22) % 1
        for j in range(n):
            q = j / n
            amp = 0.18 + 0.82 * abs(math.sin(j * 0.73 + t * 6) * math.sin(j * 0.21 + 1.3)) * (0.5 + 0.5 * math.sin(q * 9 + 1))
            hh = max(4, h * 0.62 * amp)
            col = S["violetVif"] if q <= tete else S["lilas"]
            c.drawRoundRect(skia.Rect.MakeXYWH(x0 + j * lb + lb * 0.2, -hh / 2, lb * 0.6, hh), lb * 0.3, lb * 0.3, peinture(col))
        texte(c, f"0:{int(tete * 14):02d}", x1 + h * 0.2, -hauteurLigne(h * 0.26, "demi") / 2, h * 0.26, S["gris"], "demi")
        c.drawCircle(w / 2 - h * 0.55, 0, h * 0.34, pgrad(w / 2 - h, -h / 2, w / 2, h / 2, GRAD_VIF))
        icone(c, "play", w / 2 - h * 0.52, 0, h * 0.3, "#FFFFFF", 2.6)
        balayage(c, -w / 2, -h / 2, w, h, t, h / 2)
    c.restore()


def carte_fichier(c, cx, cy, w, alpha=1.0, s=1.0, rot=0.0, t=0.0):
    """le fichier final : render.mov, 124 MB · MP4, téléchargement"""
    if alpha <= 0.01 or s <= 0.01: return
    h = w * 0.39
    with _pose(c, cx, cy, s, rot, alpha):
        verre(c, -w / 2, -h / 2, w, h, h * 0.3)
        tuile(c, "file-text", -w / 2 + h * 0.52, 0, h * 0.62, "doux")
        x = -w / 2 + h * 0.98
        texte(c, "render.mov", x, -h * 0.30, h * 0.24, S["encre"], "titre", track=-0.02)
        texte(c, "124 MB · MP4", x, h * 0.04, h * 0.17, S["gris"], "demi", track=-0.01)
        icone(c, "download", w / 2 - h * 0.42, 4 * math.sin(t * 5), h * 0.36, S["violet"], 2.6)
        balayage(c, -w / 2, -h / 2, w, h, t, h * 0.3)
    c.restore()


def dock_outils(c, cx, cy, t, t0, alpha=1.0, s=1.0):
    """le dock des logiciels pro, en verre clair : chaque logiciel jaillit à son tour"""
    if alpha <= 0.01 or t < t0: return
    noms = ["ae", "blender", "figma", "reglages"]
    tl = 112; pas = 128
    w = pas * len(noms) + 40; h = 150
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        a = entre(t, t0, 0.45, 1.6)
        c.save(); c.scale(mix(0.6, 1, a), mix(0.6, 1, a))
        verre(c, -w / 2, -h / 2, w, h, 44, borne(a * 3))
        c.restore()
        for j, n in enumerate(noms):
            e = entre(t, t0 + 0.12 + 0.1 * j, 0.45, 2.4)
            if e <= 0: continue
            x = -w / 2 + 20 + pas * j + pas / 2
            iw, ih = taille_g("app_" + n); hh = tl * ih / iw
            c.save(); c.translate(x, -30 * (1 - min(1, e)) + 4 * math.sin(t * 3 + j)); c.scale(mix(0.3, 1, e), mix(0.3, 1, e))
            lueur_s(c, 0, 0, 80, S["violetVif"], 0.22 * borne(e))
            _imgr(c, "app_" + n, -tl / 2, -hh / 2, tl, hh, borne(e * 3))
            c.restore()
    c.restore()


def vitrine(t, defile=0.0):
    """la vitrine de modèles de sites (un écran), dans un cadre de verre clair ; la rangée « Premium Templates » défile"""
    def f(c, w, h):
        k = w / 910
        r = 58 * k
        verre(c, -16 * k, -16 * k, w + 32 * k, h + 32 * k, r + 14 * k)
        _imgr(c, "vitrine", 0, 0, w, h)
        y0, hh = 668 * k, 160 * k
        c.save(); c.clipRect(skia.Rect.MakeXYWH(16 * k, y0, w - 32 * k, hh + 4 * k))
        c.drawRect(skia.Rect.MakeXYWH(16 * k, y0, w - 32 * k, hh + 4 * k), peinture("#0B1024"))
        pas = 224 * k; dx = (defile * 150 * k) % (4 * pas)
        for j in range(-1, 6):
            _imgr(c, f"modele{j % 4}", 19 * k + j * pas - dx, y0 + 4 * k, 204 * k, 155 * k)
        c.restore()
        balayage(c, 0, 0, w, h, t, r, 0.35, 0.18)
    return f


# ─────────────────────────────────────────── signature de fin DYOU (DY-M15 / GSX, version agence)
LOGO = "dyou-logo-horizontal-black"            # 1000 × 300 : sigle x 62-357, DYOU AGENCY x 370-893
SIGLE, MOT, LY = (60, 360), (366, 896), (48, 208)
T_BOUM = 0.5


def _crop(c, x0, x1, w, h, paint=None):
    i = moteur._img(LOGO)
    k = i.width() / 1000.0
    c.drawImageRect(i, skia.Rect.MakeLTRB(x0 * k, LY[0] * k, x1 * k, LY[1] * k), skia.Rect.MakeWH(w, h), moteur._ECH, paint or skia.Paint(AntiAlias=True))


def _balayage_png(c, w, h, u):
    """reflet qui ne touche que les pixels du logo"""
    if not (0 < u < 1): return
    x = mix(-160, w + 160, u)
    p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kSrcATop)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x - 110, 0), skia.Point(x + 110, 0)],
                                               [hexa("#FFFFFF", 0), hexa("#E4D8FF", 0.95), hexa("#FFFFFF", 0)]))
    c.drawRect(skia.Rect.MakeWH(w, h), p)


def _media(c, nom, w, h, t):
    """une carte du film en mini-verre : icône de logiciel (carrée) ou capture"""
    iw, ih = taille_g(nom)
    if nom.startswith("app_"):
        hh = w * ih / iw; _imgr(c, nom, 0, (h - hh) / 2, w, hh)
        return
    verre(c, 0, 0, w, h, w * 0.12, 1.0, 0.5, 0.5)
    m = w * 0.05
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(m, m, w - 2 * m, h - 2 * m), w * 0.09, w * 0.09), doAntiAlias=True)
    i = moteur._img("glace/" + nom)
    sc = max((w - 2 * m) / iw, (h - 2 * m) / ih)
    c.drawImageRect(i, skia.Rect.MakeXYWH(w / 2 - iw * sc / 2, h / 2 - ih * sc / 2, iw * sc, ih * sc), moteur._ECH, skia.Paint(AntiAlias=True))
    c.restore()


def _dims(nom):
    return (150.0, 150.0 * taille_g(nom)[1] / taille_g(nom)[0]) if nom.startswith("app_") else (160.0, 200.0)


def signature(c, t, t0, medias, lignes, cta=None, cx=510, cy=700):
    """medias : noms de banque/glace aspirés au centre → explosion (verre, ondes violettes) → sigle DYOU extrudé qui tourne
    et claque → DYOU AGENCY recomposé en tranches 3D → lignes [(texte, t, taille)] posées au mot →
    cta = dict(label, t_bouton, t_clic, url, t_url) : bouton cliqué puis adresse tapée"""
    u = t - t0
    if u < -0.05: return
    rng, rng2 = np.random.default_rng(7), np.random.default_rng(8)
    boum = t0 + T_BOUM
    sx, sy = secousse(t, boum, 24, 0.45)
    c.save(); c.translate(sx, sy)
    n = len(medias)
    # 1. aspiration : les cartes du film arrivent des bords en traînées et se compriment au centre
    for k, nom in enumerate(medias):
        d0 = 0.04 * k
        v = borne((u - d0) / (T_BOUM - d0 - 0.02))
        if v <= 0 or v >= 1: continue
        a = k / n * 2 * math.pi + 0.4
        w_, h_ = _dims(nom)
        for g in (2, 1, 0):
            vg = max(0.0, v - 0.09 * g)
            r = 760 * (1 - vg ** 2.2)
            z = mix(1.5, 0.2, vg ** 2.2)
            c.save(); c.translate(cx + r * math.cos(a), cy + r * math.sin(a) * 1.25); c.rotate(300 * vg * (1 if k % 2 else -1)); c.scale(z, z)
            with Calque(c, (0.18 if g else 1.0) * borne(v * 5)):
                c.translate(-w_ / 2, -h_ / 2); _media(c, nom, w_, h_, t)
            c.restore()
    nv = prog(t, t0 + 0.2, T_BOUM - 0.2, entree) * (1 - prog(t, boum, 0.25))
    if nv > 0:
        lueur_s(c, cx, cy, 80 + 260 * nv, S["violetVif"], 0.55 * nv)
        disque(c, cx, cy, 10 + 40 * nv, S["violetVif"], nv)
    # 2. explosion
    if u >= T_BOUM - 0.02:
        fl = 1 - (t - boum) / 0.22
        if 0 < fl <= 1: c.drawRect(skia.Rect.MakeXYWH(-100, -100, 1280, 2120), peinture("#FFFFFF", 0.7 * fl * fl))
        onde(c, cx, cy, t, boum, 40, 1150, S["violetVif"], 14, 0.7)
        onde(c, cx, cy, t, boum + 0.08, 30, 800, S["bleuVif"], 6, 0.7)
        cam = Cam(cx=cx, cy=cy)
        e = t - boum
        if e < 1.4:
            for k in range(34):                      # éclats de verre en 3D
                dx, dy, dz = rng.normal(size=3); dz = -abs(dz) * 1.6
                nn = math.sqrt(dx * dx + dy * dy + dz * dz) or 1
                vit = rng.uniform(900, 2000)
                d = vit * (1 - math.exp(-2.6 * e)) / 2.6 * 2.2
                P = (dx / nn * d, dy / nn * d + 260 * e * e, dz / nn * d)
                taille = rng.uniform(26, 70)
                rx, ry, rz = rng.uniform(0, 360, 3) + e * rng.uniform(200, 700, 3)
                pts = [rot3((taille * math.cos(b), taille * math.sin(b) * rng.uniform(0.4, 1), 0), rx, ry, rz) for b in (0, 2.2, 4.1)]
                pr = [cam.proj((P[0] + q[0], P[1] + q[1], P[2] + q[2])) for q in pts]
                if min(z for _, _, z in pr) < -1300: continue
                pa = skia.Path(); pa.moveTo(pr[0][0], pr[0][1]); pa.lineTo(pr[1][0], pr[1][1]); pa.lineTo(pr[2][0], pr[2][1]); pa.close()
                al = borne(1 - e / 1.4)
                c.drawPath(pa, peinture("#E6DCFB", 0.6 * al))
                c.drawPath(pa, peinture(S["violetVif"] if k % 3 == 0 else "#B7A6DE", 0.9 * al, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2))
        eclats(c, cx, cy, t, boum, 20, 620, cols=[S["violetVif"], S["bleuVif"], S["or_"]], graine=21, duree=0.9)
        eclats(c, cx, cy, t, boum + 0.1, 14, 380, cols=[S["violet"], S["lilas"]], graine=22, duree=0.8)
    # 3. le logo en 3D
    if u >= T_BOUM:
        e = t - boum
        a = borne(e / 0.4)
        rayons(c, cx, cy - 40, t, 900, 0.10 * a, 16, "#C9B6FF")
        lueur_s(c, cx, cy - 40, 560, S["violetVif"], 0.14 * a)
        ou = prog(t, boum + 0.05, 1.2, douce)
        cam = Cam(ax=-10 + 4 * math.sin(t * 1.3), ay=mix(-28, 8, ou) + 5 * math.sin(t * 0.9), tz=mix(380, 0, ou), cx=cx, cy=cy)
        plans = []
        ann = prog(t, boum + 0.35, 0.6, sortie)
        if ann > 0:                                  # anneau des cartes du film, derrière le logo
            for k, nom in enumerate(medias):
                ang = t * 0.8 + k * 2 * math.pi / n
                R = mix(260, 540, ann)
                pos = (R * math.cos(ang), -30 + 60 * math.sin(ang * 2), 300 + 230 * math.sin(ang))
                w_, h_ = _dims(nom)
                def dess(cc, w, h, nom=nom): _media(cc, nom, w, h, t)
                cache = borne((abs(pos[0]) - 340) / 110)               # visible seulement sur les côtés : jamais à travers le logo
                plans.append(Plan(coins(pos, w_, h_, ay=-math.degrees(ang) + 90), w_, h_, dess, 0.85 * ann * cache, recto=False))
        # sigle extrudé : couches empilées en profondeur, il fait un tour et claque
        SW = 330.0; SH = SW * (LY[1] - LY[0]) / (SIGLE[1] - SIGLE[0])
        sg = prog(t, boum, 0.75, lambda v: ressort(v, 1.2, 5.0))
        if sg > 0:
            tour = mix(340, 0, min(sg, 1.08)); s_ = mix(0.2, 1, min(sg, 1.1))
            for k in range(12, -1, -1):
                tint = mix(0.45, 1.0, k / 12)
                def couche(cc, w, h, k=k, tint=tint):
                    p = skia.Paint(AntiAlias=True)
                    if k > 0: p.setColorFilter(skia.ColorFilters.Blend(skia.Color4f(0.30 * tint, 0.13 * tint, 0.62 * tint, 1).toColor(), skia.BlendMode.kSrcIn))
                    cc.saveLayer(None)
                    _crop(cc, SIGLE[0], SIGLE[1], w, h, p)
                    if k == 0: _balayage_png(cc, w, h, prog(t, boum + 1.05, 0.55, douce))
                    cc.restore()
                ctr = rot3((0, 0, 3.4 * k * s_), 0, tour, 0)
                plans.append(Plan(coins((ctr[0], -150 + ctr[1], ctr[2]), SW * s_, SH * s_, ay=tour), SW * s_, SH * s_, couche, borne(sg * 4), recto=False))
        # DYOU AGENCY : 8 tranches qui volent depuis des points 3D et se recomposent
        MW = 600.0; MH = MW * (LY[1] - LY[0]) / (MOT[1] - MOT[0]); nt = 8
        for k in range(nt):
            d = prog(t, boum + 0.22 + 0.045 * k, 0.55, lambda v: ressort(v, 1.15, 5.2))
            dep = (rng2.uniform(-900, 900), rng2.uniform(-1100, 1100), rng2.uniform(-1300, 900)); rr = rng2.uniform(-260, 260, 3)
            if d <= 0: continue
            sw = MW / nt; x_fin = -MW / 2 + sw * (k + 0.5)
            q = min(d, 1.06)
            pos = (mix(dep[0], x_fin, q), mix(dep[1], 95, q), mix(dep[2], 0, q))
            def tranche(cc, w, h, k=k, sw=sw):
                cc.saveLayer(None)
                s0 = MOT[0] + (MOT[1] - MOT[0]) * k / nt; s1 = MOT[0] + (MOT[1] - MOT[0]) * (k + 1) / nt
                _crop(cc, s0, s1, w + 0.6, h)
                if 0 < prog(t, boum + 1.2, 0.7, douce) < 1:
                    x = mix(-160, MW + 160, prog(t, boum + 1.2, 0.7, douce)) - sw * k
                    p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kSrcATop)
                    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x - 110, 0), skia.Point(x + 110, 0)],
                                                               [hexa("#FFFFFF", 0), hexa("#E4D8FF", 0.95), hexa("#FFFFFF", 0)]))
                    cc.drawRect(skia.Rect.MakeWH(w, h), p)
                cc.restore()
            plans.append(Plan(coins(pos, sw + 0.6, MH, ax=rr[0] * (1 - q), ay=rr[1] * (1 - q), az=rr[2] * (1 - q)), sw + 0.6, MH, tranche,
                              borne(d * 4), recto=False))
        scene3d(c, cam, plans)
        # trait sous le logo, puis les lignes au mot
        b = prog(t, boum + 0.9, 0.45, sortie)
        if b > 0:
            lw = 220 * b; c.drawRoundRect(skia.Rect.MakeXYWH(cx - lw / 2, cy + 200, lw, 6), 3, 3, pgrad(cx - lw / 2, 0, cx + lw / 2, 0, GRAD_VIF))
        y = cy + 250
        for txt, tl, tai in lignes:
            b = prog(t, tl - 0.05, 0.4, sortie)
            if b > 0:
                texte(c, txt, cx, y + 22 * (1 - b), ajuste(txt, 780, tai, "titre", -0.02), S["encre"], "titre", "centre", -0.02, b)
            y += tai * 1.4
        if cta:
            yb = y + 70
            bt = entre(t, cta["t_bouton"], 0.5, 1.8)
            tc = cta["t_clic"]
            ap = prog(t, tc - 0.06, 0.06, sortie) * (1 - prog(t, tc + 0.05, 0.14, sortie))
            pulse = 1 + 0.025 * max(0, math.sin((t - tc - 0.4) * 5)) if t > tc + 0.4 else 1
            if bt > 0:
                bouton(c, cta["label"], cx, yb, 40, mix(0.2, 1, bt) * (1 - 0.07 * ap) * pulse, borne(bt * 3))
                cu = prog(t, tc - 0.5, 0.45, sortie)
                if cu > 0:
                    curseur(c, mix(900, cx + 120, cu), mix(1450, yb + 14, cu), 1.1, 1 - prog(t, tc + 0.6, 0.3, sortie), ap)
                    clic(c, cx + 120, yb + 8, t, tc)
                eclats(c, cx, yb, t, tc + 0.02, 12, 420, graine=12)
            ub = entre(t, cta["t_url"] - 0.25, 0.45, 1.6)
            if ub > 0:
                wb, yu = 560, yb + 150
                with Calque(c, borne(ub * 3)):
                    verre(c, cx - wb / 2, yu - 42, wb, 84, 42, 1.0, 0.6, 0.6)
                    icone(c, "lock", cx - wb / 2 + 48, yu, 28, S["vert"], 2.6)
                    url = cta["url"]
                    nb = int(borne((t - cta["t_url"]) / 0.5) * len(url) + 0.999) if t >= cta["t_url"] else 0
                    xs_ = cx - wb / 2 + 82
                    texte(c, url[:nb], xs_, yu - hauteurLigne(36, "titre") / 2, 36, S["encre"], "titre", track=-0.01)
                    if int(t * 3) % 2 == 0: _ORIG.get("rrect", rrect)(c, xs_ + largeur(url[:nb], 36, "titre", -0.01) + 4, yu - 21, 4, 42, 2, S["violet"])
    c.restore()


def sons_signature(son, t0):
    son(t0, "montee", -9); son(t0 + 0.05, "whoosh_long", -9)
    son(t0 + T_BOUM, "impact", -4); son(t0 + T_BOUM + 0.02, "whoosh_bas", -6); son(t0 + T_BOUM + 0.05, "verre", -8)
    for k in range(8): son(t0 + T_BOUM + 0.22 + 0.045 * k + 0.4, "pop", -15)
    son(t0 + T_BOUM + 0.7, "impact_doux", -9)
    son(t0 + T_BOUM + 1.15, "ching", -9); son(t0 + T_BOUM + 0.9, "whoosh_court", -13)
