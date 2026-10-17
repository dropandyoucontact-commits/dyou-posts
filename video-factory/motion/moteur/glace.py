"""Thème « glace » (17/10/2026) — DA-M14-EN et DA-M16-EN refaites en verre fumé, même voix, même texte.

Demande de Youssef : des cadres comme ses cartes (banque/glace/sources/) — fond noir transparent, effet glace, liseré
clair et lueur bleue — pour tout ce qui « s'ouvre » ou « sort », et ses visuels animés dedans (modèles de sites qui
défilent, barres de rendu qui avancent, outils qui sortent). Objectif : montrer qu'on est plus forts que les autres studios.

    from glace import *        # après studio / studio3d / sites3d
    appliquer()                # passe tout le moteur studio en sombre + verre

Principe : la palette S (partagée) passe en sombre ; les cartes blanches (rrect blanc, carte_s, pill) deviennent du verre ;
les contenus « réels » (faux sites, post gris) restent clairs grâce à `clair()`. Les cadres sont redessinés (nets en
perspective), seul le contenu des images de Youssef est réutilisé (outils/glace_decoupe.py → banque/glace/).
"""
import math, sys, contextlib
import skia
import moteur
from moteur import *
import studio
from studio import S, GRAD, GRAD_VIF, CONFETTIS, pgrad, lueur_s, tuile, entre

BLEU = "#3D7BFF"
G = dict(actif=False, clair=0)
_ORIG = {}

SOMBRE = dict(papier="#04050B", doux="#121729", lavande="#1A2240", ligne="#2B3454", encre="#F3F6FF", encre2="#C9D2EE",
              gris="#8F99BA", grisClair="#5E6788", violet="#8E6BFF", violetFonce="#B9A4FF", violetVif="#8B5CFF",
              bleu="#5B8CFF", bleuVif="#3D7BFF", lilas="#7FA6FF", vert="#2BD67B", vertDoux="#0E2A1E", rouge="#FF4D5E",
              rougeDoux="#2C1118", or_="#FFC53D", blanc="#FFFFFF")
CLAIR = dict(S)
GRAD_CLAIR = list(GRAD)


@contextlib.contextmanager
def clair():
    """contenu « réel » (faux site, post photo) : palette claire d'origine, pas de verre"""
    sauve, sg = dict(S), list(GRAD); S.update(CLAIR); GRAD[:] = GRAD_CLAIR; G["clair"] += 1
    try: yield
    finally: S.update(sauve); GRAD[:] = sg; G["clair"] -= 1


def _installe(nom, fn):
    vieux = _ORIG.setdefault(nom, None)
    for mod in list(sys.modules.values()):
        d = getattr(mod, "__dict__", None)
        if d is None or mod is sys.modules[__name__]: continue
        if nom in d and callable(d[nom]) and getattr(d[nom], "__module__", "") != __name__:
            _ORIG[nom] = _ORIG[nom] or d[nom]
            d[nom] = fn


# ─────────────────────────────────────────── le verre
def verre(c, x, y, w, h, r=34, alpha=1.0, contour=None, lueur=1.0, givre=0.0):
    """carte en verre fumé : ombre noire, lueur bleue autour, corps sombre translucide, reflet en haut, liseré clair → bleu"""
    if alpha <= 0.003 or w <= 1 or h <= 1: return
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    k = max(0.4, min(w, h) / 300)
    with Calque(c, alpha):
        p = skia.Paint(AntiAlias=True, Color=hexa("#000000", 0.55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 26 * k))
        c.save(); c.translate(0, 18 * k); c.drawRRect(rr, p); c.restore()
        if lueur > 0:
            p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.30 * lueur), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 16 * k))
            c.drawRRect(rr, p)
        c.drawRRect(rr, pgrad(x, y, x + w * 0.4, y + h, ["#222A42", "#121728", "#0A0D19"], alpha=0.86))
        if givre > 0: c.drawRRect(rr, peinture("#DCE6FF", 0.10 * givre))
        c.save(); c.clipRRect(rr, doAntiAlias=True)
        rf = skia.Paint(AntiAlias=True)
        rf.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + min(h, 260 * k))],
                                                    [hexa("#FFFFFF", 0.10), hexa("#FFFFFF", 0.0)]))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), rf)
        rf = skia.Paint(AntiAlias=True)          # éclat en biais (comme le panneau givré)
        rf.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.5, y + h * 0.5)],
                                                    [hexa("#FFFFFF", 0.0), hexa("#FFFFFF", 0.07), hexa("#FFFFFF", 0.0)], [0.30, 0.36, 0.46]))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), rf)
        lb = skia.Paint(AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10 * k))
        lb.setShader(skia.GradientShader.MakeRadial(skia.Point(x + w / 2, y + h), w * 0.6, [hexa(BLEU, 0.35 * lueur), hexa(BLEU, 0.0)]))
        c.drawRect(skia.Rect.MakeXYWH(x, y + h - 60 * k, w, 60 * k), lb)
        c.restore()
        ep = max(1.5, 2.2 * k)
        li = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=ep)
        li.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w, y + h)],
                                                    [hexa("#FFFFFF", 0.75), hexa("#FFFFFF", 0.14), hexa("#9DBBFF", 0.18), hexa("#6E9BFF", 0.85)],
                                                    [0.0, 0.35, 0.65, 1.0]))
        c.drawRRect(rr, li)
        if contour and contour not in (S["ligne"], "#DED7E9"):
            c.drawRRect(rr, peinture(contour, 0.8, Style=skia.Paint.kStroke_Style, StrokeWidth=ep * 1.3))


def _blanc(col):
    return isinstance(col, str) and col.upper() in ("#FFFFFF", "#FFF", "#FCFBFE", "#F4F3F7")


def rrect_g(c, x, y, w, h, r, couleur, alpha=1.0, ombre=None, contour=None, ep=0):
    if G["actif"] and not G["clair"] and _blanc(couleur) and w >= 90 and h >= 56:
        return verre(c, x, y, w, h, r, alpha, contour)
    return _ORIG["rrect"](c, x, y, w, h, r, couleur, alpha, ombre, contour, ep)


def carte_s_g(c, x, y, w, h, r=34, fond="#FFFFFF", contour=None, ombre=0.11, alpha=1.0, ep=2):
    if not G["clair"] and _blanc(fond):
        return verre(c, x, y, w, h, r, alpha, contour)
    return _ORIG["carte_s"](c, x, y, w, h, r, fond, contour, ombre, alpha, ep)


def ombre_violette_g(c, rr, opa=0.12, flou=30, dy=22):
    if opa <= 0: return
    p = skia.Paint(AntiAlias=True, Color=hexa("#000000", min(0.7, opa * 3)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, flou))
    c.save(); c.translate(0, dy); c.drawRRect(rr, p); c.restore()


def pill_g(c, label, cx, cy, taille=30, mode="doux", icone_=None, alpha=1.0, s=1.0, rot=0.0, fam="fort"):
    """pastille en verre : texte blanc, icône teintée ; « grad » reste un aplat bleu-violet lumineux"""
    if G["clair"]: return _ORIG["pill"](c, label, cx, cy, taille, mode, icone_, alpha, s, rot, fam)
    if alpha <= 0.01 or s <= 0.01: return 0
    tw = largeur(label, taille, fam, -0.01)
    h = taille * 2.0; ic = taille * 1.1 if icone_ else 0
    w = tw + ic + (taille * 0.4 if icone_ else 0) + taille * 1.5
    teinte = {"doux": "#9DBBFF", "grad": "#FFFFFF", "blanc": "#9DBBFF", "encre": "#FFFFFF", "vert": S["vert"], "rouge": S["rouge"]}[mode]
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        if mode == "grad":
            p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, taille * 0.5))
            c.drawRRect(rr, p)
            c.drawRRect(rr, pgrad(-w / 2, 0, w / 2, 0, GRAD_VIF))
            c.drawRRect(rr, peinture("#FFFFFF", 0.45, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        else:
            verre(c, -w / 2, -h / 2, w, h, h / 2, 1.0, None, 0.7 if mode != "encre" else 1.0)
            if mode in ("vert", "rouge"):
                c.drawRRect(rr, peinture(teinte, 0.16))
                c.drawRRect(rr, peinture(teinte, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4))
        x = -w / 2 + taille * 0.75
        if icone_:
            icone(c, icone_, x + ic / 2, 0, ic, teinte, 2.6); x += ic + taille * 0.4
        texte(c, label, x, -hauteurLigne(taille, fam) / 2, taille, "#FFFFFF", fam, track=-0.01)
    c.restore()
    return w


def tuile_g(c, ic, cx, cy, taille, mode="grad", alpha=1.0, ep=2.2, rot=0.0):
    if mode == "grad" or G["clair"]: return _ORIG["tuile"](c, ic, cx, cy, taille, mode, alpha, ep, rot)
    c.save(); c.translate(cx, cy); c.rotate(rot)
    verre(c, -taille / 2, -taille / 2, taille, taille, taille * 0.28, alpha)
    icone(c, ic, 0, 0, taille * 0.5, "#9DBBFF", ep, alpha)
    c.restore()


_FLECHE = [(0, 0), (0, 36), (9, 27.5), (15.5, 42), (22, 39), (15.5, 25), (27, 25)]


def curseur_g(c, x, y, s=1.0, alpha=1.0, appui=0.0):
    if alpha <= 0.01: return
    k = s * 1.6 * (1 - 0.18 * appui)
    pth = skia.Path(); pth.moveTo(x, y)
    for px, py in _FLECHE[1:]: pth.lineTo(x + px * k, y + py * k)
    pth.close()
    with Calque(c, alpha):
        p = skia.Paint(AntiAlias=True, Color=hexa("#000000", 0.5), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.save(); c.translate(3, 6); c.drawPath(pth, p); c.restore()
        c.drawPath(pth, peinture("#0A0D19"))
        c.drawPath(pth, peinture("#FFFFFF", 1, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, StrokeJoin=skia.Paint.kRound_Join))


def navigateur_g(c, x, y, w, h, url, contenu=None, alpha=1.0):
    """cadre de navigateur en verre ; la page dedans reste un vrai site clair"""
    def page(cc, *a):
        with clair(): contenu(cc, *a)
    return _ORIG["navigateur"](c, x, y, w, h, url, page if contenu else None, alpha)


_LOGOS = {"dyou-logo-horizontal-black": "logo-agence-blanc"}


def image_g(c, nom, x, y, w, alpha=1.0, h=None):
    return _ORIG["image"](c, _LOGOS.get(nom, nom) if not G["clair"] else nom, x, y, w, alpha, h)


def taille_img_g(nom):
    return _ORIG["taille_img"](_LOGOS.get(nom, nom) if not G["clair"] else nom)


# ─────────────────────────────────────────── fond : nuit bleue, nébuleuses qui dérivent, trame de points
TACHES = [(170, 430, 820, "#1D3BFF", 0.30, 0.21, 0.0), (960, 1480, 860, "#5B2BD6", 0.28, 0.17, 1.7),
          (900, 260, 560, "#2F6BFF", 0.22, 0.27, 3.1), (110, 1720, 640, "#2A1FA0", 0.30, 0.19, 4.4)]


def fond_glace(c, t, pulse=0.0):
    W, H = moteur.W, moteur.H
    c.clear(hexa(S["papier"]))
    for x, y, r, col, a, v, ph in TACHES:
        x, y = x * W / 1080, y * H / 1920
        cx = x + 110 * math.sin(t * v + ph); cy = y + 120 * math.cos(t * v * 0.8 + ph)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r * (1 + 0.08 * pulse), [hexa(col, min(1, a * (1 + 0.5 * pulse))), hexa(col, 0.0)]))
        c.drawCircle(cx, cy, r * (1 + 0.08 * pulse), p)
    p = peinture("#7FA6FF", 0.10)
    dy = (t * 14) % 54
    for y in range(-54, H + 54, 54):
        for x in range(27, W, 54):
            c.drawCircle(x, y + 27 - dy, 1.8, p)
    # vignette
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.45), H * 0.75, [hexa("#000000", 0.0), hexa("#000000", 0.55)], [0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


def _clair_fab(nom):
    fab = _ORIG[nom]
    def fab2(*a, **k):
        f = fab(*a, **k)
        def g(c, w, h):
            c.save(); c.clipRect(skia.Rect.MakeWH(w, h))      # le faux site ne déborde plus de son cadre
            with clair(): f(c, w, h)
            c.restore()
        return g
    fab2.__module__ = __name__
    return fab2


def appliquer():
    G["actif"] = True
    S.update(SOMBRE)
    GRAD[:] = ["#FFFFFF", "#C4D6FF", "#7FA6FF"]
    GRAD_VIF[:] = ["#2F6BFF", "#5B6CFF", "#8B5CFF"]
    CONFETTIS[:] = [BLEU, "#8B5CFF", "#7FA6FF", "#FFFFFF", "#B9A4FF", S["or_"]]
    for nom, fn in [("rrect", rrect_g), ("carte_s", carte_s_g), ("ombre_violette", ombre_violette_g), ("pill", pill_g),
                    ("tuile", tuile_g), ("curseur", curseur_g), ("image", image_g), ("taille_img", taille_img_g),
                    ("fond_studio", fond_glace), ("navigateur", navigateur_g)]:
        _installe(nom, fn)
    for nom in ("site_vieux", "site_moderne", "post_gris"):
        for mod in list(sys.modules.values()):
            d = getattr(mod, "__dict__", None)
            if d and nom in d and nom not in _ORIG: _ORIG[nom] = d[nom]
        if nom in _ORIG: _installe(nom, _clair_fab(nom))


# ─────────────────────────────────────────── cartes de Youssef, animées
def _imgr(c, nom, x, y, w, h, alpha=1.0):
    i = moteur._img("glace/" + nom)
    p = skia.Paint(AntiAlias=True)
    if alpha < 1: p.setAlphaf(borne(alpha))
    c.drawImageRect(i, skia.Rect.MakeXYWH(x, y, w, h), moteur._ECH, p)


def taille_g(nom):
    i = moteur._img("glace/" + nom); return i.width(), i.height()


def balayage(c, x, y, w, h, t, r=30, vitesse=0.45, a=0.10):
    """reflet qui traverse la vitre"""
    u = (t * vitesse) % 1.6 - 0.3
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), doAntiAlias=True)
    p = skia.Paint(AntiAlias=True)
    x0 = x + w * u
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0 - 160, y), skia.Point(x0 + 160, y + 200)],
                                               [hexa("#FFFFFF", 0), hexa("#FFFFFF", a), hexa("#FFFFFF", 0)]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)
    c.restore()


def carte_image(c, nom, cx, cy, w, alpha=1.0, s=1.0, rot=0.0, t=0.0, cadre=True):
    """une carte du kit, posée dans un cadre de verre net"""
    if alpha <= 0.01 or s <= 0.01: return
    iw, ih = taille_g(nom); h = w * ih / iw
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        r = min(h / 2, 28)
        if cadre: verre(c, -w / 2 - 10, -h / 2 - 10, w + 20, h + 20, r + 8)
        _imgr(c, nom, -w / 2, -h / 2, w, h)
        balayage(c, -w / 2, -h / 2, w, h, t, r)
    c.restore()


def barre(c, x, y, w, u, h=8):
    rrect_g(c, x, y - h / 2, w, h, h / 2, "#2A3045")
    if u > 0.005:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - h / 2, max(h, w * u), h), h / 2, h / 2), pgrad(x, 0, x + w, 0, ["#2F6BFF", "#5B9BFF"]))
        lueur_s(c, x + w * u, y, h * 3, BLEU, 0.5)


def carte_rendu(c, cx, cy, w, u, alpha=1.0, s=1.0, t=0.0):
    """« Rendering… » : la barre avance pour de vrai, le pourcentage suit ; à 100 % → « Completed! »"""
    if alpha <= 0.01 or s <= 0.01: return
    iw, ih = taille_g("rendu_ligne"); h_l = (w - 150) * ih / iw
    H_ = h_l + 50
    fini = prog(u, 0.985, 0.015, lin) if u >= 0.985 else 0.0
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        verre(c, -w / 2, -H_ / 2, w, H_, 34)
        tuile(c, "clapperboard", -w / 2 + 75, 0, 84, "grad")
        x0, y0 = -w / 2 + 135, -h_l / 2
        with Calque(c, 1 - borne(u * 60 - 59)):
            _imgr(c, "rendu_ligne", x0, y0, w - 150, h_l)
            # on repeint la barre et le pourcentage
            k = (w - 150) / 352
            rrect_g(c, x0 + 270 * k, y0 + 22 * k, 72 * k, 22 * k, 4, "#252A33")
            texte(c, f"{int(u * 100)}%", x0 + 340 * k, y0 + 20 * k, 17 * k, "#E8ECF6", "demi", "droite", 0)
            rrect_g(c, x0 + 8 * k, y0 + 50 * k, 330 * k, 12 * k, 4, "#252A33")
            barre(c, x0 + 10 * k, y0 + 56 * k, 326 * k, u, 7 * k)
        if u >= 0.98:
            iw2, ih2 = taille_g("termine_ligne"); w2 = w - 40
            with Calque(c, borne(u * 60 - 59)):
                _imgr(c, "termine_ligne", -w2 / 2, -w2 * ih2 / iw2 / 2, w2, w2 * ih2 / iw2)
        balayage(c, -w / 2, -H_ / 2, w, H_, t, 34)
    c.restore()


def carte_gen3d(c, cx, cy, w, u, alpha=1.0, s=1.0, t=0.0):
    """« Generating 3D scenes… » : barre et pourcentage vivants"""
    if alpha <= 0.01 or s <= 0.01: return
    iw, ih = taille_g("gen3d"); h = w * ih / iw; k = w / 478
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        verre(c, -w / 2 - 12, -h / 2 - 12, w + 24, h + 24, 36)
        x0, y0 = -w / 2, -h / 2
        _imgr(c, "gen3d", x0, y0, w, h)
        rrect_g(c, x0 + 6 * k, y0 + 196 * k, 470 * k, 22 * k, 4, "#1E222B")
        barre(c, x0 + 10 * k, y0 + 204 * k, 400 * k, u, 7 * k)
        texte(c, f"{int(u * 100)}%", x0 + 466 * k, y0 + 194 * k, 16 * k, "#E8ECF6", "demi", "droite", 0)
        balayage(c, x0, y0, w, h, t, 26)
    c.restore()


def dock_outils(c, cx, cy, t, t0, alpha=1.0, s=1.0):
    """le dock d'outils pro : chaque logiciel jaillit à son tour"""
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
            lueur_s(c, 0, 0, 80, BLEU, 0.25 * borne(e))
            _imgr(c, "app_" + n, -tl / 2, -hh / 2, tl, hh, borne(e * 3))
            c.restore()
    c.restore()


def vitrine(t, defile=0.0):
    """la vitrine de modèles de sites, vivante : la rangée « Premium Templates » défile, reflet qui passe ;
    à plaquer sur un Plan (w × h ≈ 910 × 850)"""
    def f(c, w, h):
        k = w / 910
        r = 58 * k
        verre(c, -14 * k, -14 * k, w + 28 * k, h + 28 * k, r + 12 * k)
        _imgr(c, "vitrine", 0, 0, w, h)
        # la rangée défile
        y0, hh = 668 * k, 160 * k
        c.save(); c.clipRect(skia.Rect.MakeXYWH(16 * k, y0, w - 32 * k, hh + 4 * k))
        c.drawRect(skia.Rect.MakeXYWH(16 * k, y0, w - 32 * k, hh + 4 * k), peinture("#0B1024"))
        pas = 224 * k; dx = (defile * 150 * k) % (4 * pas)
        for j in range(-1, 6):
            x = 19 * k + j * pas - dx
            _imgr(c, f"modele{j % 4}", x, y0 + 4 * k, 204 * k, 155 * k)
        c.restore()
        balayage(c, 0, 0, w, h, t, r, 0.35, 0.09)
    return f


def panneau_givre(c, x, y, w, h, alpha=1.0, t=0.0):
    """le panneau de verre givré clair (fond du carton final)"""
    if alpha <= 0.01: return
    with Calque(c, alpha):
        p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 30))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 60, 60), p)
        _imgr(c, "givre", x, y, w, h, 0.32)
        verre(c, x, y, w, h, 60, 0.55, None, 0.6)
        balayage(c, x, y, w, h, t, 60, 0.3, 0.12)
