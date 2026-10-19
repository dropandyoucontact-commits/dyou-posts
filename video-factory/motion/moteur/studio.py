"""Style « studio clair » DYOU Agency (DA-M06 / DA-M07, 14/10/2026) : les couleurs du site refondu.

Fond papier #FCFBFE à taches lilas et bleu pâle, encre #211B33, dégradé violet → bleu du site
(#6533BF → #7C43CC → #4665AD), Inter. Demande de Youssef : battre les meilleurs studios de motion
design en animation — titres construits lettre par lettre (ressort, masque, trajectoires d'animation
avec images clés visibles), cartes blanches à liseré lilas, interfaces vivantes (timeline, navigateur,
tableau de bord), une idée par seconde, transitions variées. Sous-titres fins, encre, sans surlignage.

Le corps du message (de « Aujourd'hui » à la fin) est commun aux deux pubs : les scènes prennent un
dictionnaire M de temps-repères (mot → seconde) calculé par chaque scenes.py ; seul le hook change.
"""
import math
import numpy as np
import skia
import moteur
from moteur import *

S = dict(papier="#FCFBFE", doux="#F3F0F8", lavande="#ECE5FA", ligne="#DED7E9", encre="#211B33", encre2="#423951",
         gris="#655C73", grisClair="#A79FB5", violet="#7544D6", violetFonce="#6333BD", violetVif="#8B5CFF",
         bleu="#4665AD", bleuVif="#4F7BFF", lilas="#C9B6FF", vert="#2E9E68", vertDoux="#DDF5E8", rouge="#E5484D",
         rougeDoux="#FDE7E8", or_="#FFC53D", blanc="#FFFFFF")
GRAD = ["#6533BF", "#7C43CC", "#4665AD"]          # le dégradé des titres du site
GRAD_VIF = ["#7B3FF2", "#8B5CFF", "#4F7BFF"]      # les grands aplats (prix, boutons)
CONFETTIS = [S["violet"], S["violetVif"], S["bleuVif"], S["lilas"], "#FFFFFF", S["or_"]]

# Langue : une version étrangère remplit TR (texte français → texte affiché) et PRIX avant le rendu.
TR = {}
def tr(x): return TR.get(x, x)
CTA_PILLS = None          # pastilles du carton final, à la place de celles du motion (ex. pubs « sites »)
PRIX = dict(chiffres="290", devise="€", avant=False, mention="TTC")   # en dollars : chiffres="299", devise="$", avant=True


def entre(t, t0, d=0.42, s=1.6): return 0.0 if t <= t0 else prog(t, t0, d, lambda v: rebond(v, s))   # 0 exact avant le départ (rebond(0) ≈ 2e-16)
def sort(t, t0, d=0.26): return prog(t, t0, d, entree)


# ─────────────────────────────────────────── peintures
def pgrad(x0, y0, x1, y1, cols=GRAD, pos=None, alpha=1.0):
    p = skia.Paint(AntiAlias=True)
    pos = pos or [k / (len(cols) - 1) for k in range(len(cols))]
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [hexa(k, alpha) for k in cols], pos))
    return p


class Degrade:
    """with Degrade(c, x0, y0, x1, y1): tout ce qui est dessiné dedans prend le dégradé (texte, icônes, formes)"""
    def __init__(self, c, x0, y0, x1, y1, cols=GRAD, alpha=1.0):
        self.c, self.g, self.a, self.cols = c, (x0, y0, x1, y1), borne(alpha), cols
    def __enter__(self):
        p = skia.Paint(); p.setAlphaf(self.a)
        self.c.saveLayer(None, p); return self.c
    def __exit__(self, *a):
        p = pgrad(*self.g, cols=self.cols); p.setBlendMode(skia.BlendMode.kSrcIn)
        self.c.save(); self.c.resetMatrix(); self.c.drawRect(skia.Rect.MakeWH(W, H), p); self.c.restore()
        self.c.restore()


def texte_grad(c, s, x, y, taille, fam="noir", align="gauche", track=-0.03, alpha=1.0, cols=GRAD):
    w = largeur(s, taille, fam, track)
    x0 = x - w / 2 if align == "centre" else x - w if align == "droite" else x
    if alpha <= 0.01: return w
    with Degrade(c, x0, y, x0 + w, y + taille, cols, alpha):
        texte(c, s, x0, y, taille, S["encre"], fam, "gauche", track)
    return w


def flou_calque(c, flou, alpha=1.0):
    p = skia.Paint(ImageFilter=skia.ImageFilters.Blur(flou, flou)) if flou > 0.3 else skia.Paint()
    p.setAlphaf(borne(alpha)); c.saveLayer(None, p)


# ─────────────────────────────────────────── fond
TACHES = [(170, 430, 760, "#E2D4FF", 0.80, 0.21, 0.0), (960, 1480, 820, "#D7E3FF", 0.75, 0.17, 1.7),
          (900, 260, 520, "#EEE4FF", 0.70, 0.27, 3.1), (110, 1720, 600, "#E6DCFF", 0.60, 0.19, 4.4)]


def fond_studio(c, t, pulse=0.0):
    c.clear(hexa(S["papier"]))
    for x, y, r, col, a, v, ph in TACHES:
        x, y = x * W / 1080, y * H / 1920                       # mêmes taches en 16:9
        cx = x + 110 * math.sin(t * v + ph); cy = y + 120 * math.cos(t * v * 0.8 + ph)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r * (1 + 0.08 * pulse), [hexa(col, min(1, a * (1 + 0.3 * pulse))), hexa(col, 0.0)]))
        c.drawCircle(cx, cy, r * (1 + 0.08 * pulse), p)
    p = peinture("#CDBFEA", 0.55)
    dy = (t * 14) % 54
    for y in range(-54, H + 54, 54):
        for x in range(27, W, 54):
            c.drawCircle(x, y + 27 - dy, 2.0, p)


def fond_grad(c, t, alpha=1.0):
    """grand aplat violet → bleu du site, taches claires qui dérivent, trame blanche"""
    with Calque(c, alpha):
        c.drawRect(skia.Rect.MakeWH(W, H), pgrad(0, 0, W, H, ["#5B2BD6", "#7B3FF2", "#4F6FE8"]))
        for k, (x, y, r, a) in enumerate([(200, 500, 700, 0.30), (900, 1500, 760, 0.26), (850, 300, 420, 0.18)]):
            x, y = x * W / 1080, y * H / 1920
            cx = x + 120 * math.sin(t * 0.4 + k * 2); cy = y + 100 * math.cos(t * 0.33 + k)
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa("#C9B6FF", a), hexa("#C9B6FF", 0.0)]))
            c.drawCircle(cx, cy, r, p)
        p = peinture("#FFFFFF", 0.10)
        dy = (t * 18) % 54
        for y in range(-54, H + 54, 54):
            for x in range(27, W, 54):
                c.drawCircle(x, y + 27 - dy, 2.0, p)


# ─────────────────────────────────────────── cartes, tuiles, pastilles, boutons
def ombre_violette(c, rr, opa=0.12, flou=30, dy=22):
    if opa <= 0: return
    p = skia.Paint(AntiAlias=True, Color=hexa("#4B2E9A", opa), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, flou))
    c.save(); c.translate(0, dy); c.drawRRect(rr, p); c.restore()


def carte_s(c, x, y, w, h, r=34, fond="#FFFFFF", contour=None, ombre=0.11, alpha=1.0, ep=2):
    contour = S["ligne"] if contour is None else contour
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    with Calque(c, alpha):
        ombre_violette(c, rr, ombre)
        c.drawRRect(rr, peinture(fond))
        if contour: c.drawRRect(rr, peinture(contour, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=ep))


def tuile(c, ic, cx, cy, taille, mode="grad", alpha=1.0, ep=2.2, rot=0.0):
    """carré arrondi : « grad » dégradé + icône blanche ; « doux » lavande + icône violette"""
    c.save(); c.translate(cx, cy); c.rotate(rot)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-taille / 2, -taille / 2, taille, taille), taille * 0.28, taille * 0.28)
        if mode == "grad":
            ombre_violette(c, rr, 0.22, 18, 12)
            c.drawRRect(rr, pgrad(-taille / 2, -taille / 2, taille / 2, taille / 2, GRAD_VIF))
            c.drawRRect(rr, pgrad(0, -taille / 2, 0, 0, ["#FFFFFF", "#FFFFFF"], alpha=0.0))
            icone(c, ic, 0, 0, taille * 0.5, "#FFFFFF", ep)
        else:
            c.drawRRect(rr, peinture(S["lavande"]))
            icone(c, ic, 0, 0, taille * 0.5, S["violet"], ep)
    c.restore()


def pill(c, label, cx, cy, taille=30, mode="doux", icone_=None, alpha=1.0, s=1.0, rot=0.0, fam="fort"):
    """pastille : « doux » lavande/violet, « grad » dégradé/blanc, « blanc » carte blanche, « encre » sombre"""
    if alpha <= 0.01 or s <= 0.01: return 0
    tw = largeur(label, taille, fam, -0.01)
    h = taille * 2.0; ic = taille * 1.1 if icone_ else 0
    w = tw + ic + (taille * 0.4 if icone_ else 0) + taille * 1.5
    fond, coul = {"doux": (S["lavande"], S["violetFonce"]), "grad": (None, "#FFFFFF"), "blanc": ("#FFFFFF", S["encre"]),
                  "encre": (S["encre"], "#FFFFFF"), "vert": (S["vertDoux"], S["vert"]), "rouge": (S["rougeDoux"], S["rouge"])}[mode]
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        if mode == "grad":
            ombre_violette(c, rr, 0.22, 18, 10); c.drawRRect(rr, pgrad(-w / 2, 0, w / 2, 0, GRAD_VIF))
        elif mode == "blanc":
            ombre_violette(c, rr, 0.12, 16, 10); c.drawRRect(rr, peinture(fond))
            c.drawRRect(rr, peinture(S["ligne"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        else:
            c.drawRRect(rr, peinture(fond))
        x = -w / 2 + taille * 0.75
        if icone_:
            icone(c, icone_, x + ic / 2, 0, ic, coul, 2.6); x += ic + taille * 0.4
        texte(c, label, x, -hauteurLigne(taille, fam) / 2, taille, coul, fam, track=-0.01)
    c.restore()
    return w


def bouton(c, label, cx, cy, taille=44, s=1.0, alpha=1.0, icone_="arrow-right", largeur_min=0):
    tw = largeur(label, taille, "titre", -0.01)
    h = taille * 2.6; w = max(largeur_min, tw + taille * 2.0 + (taille * 1.2 if icone_ else 0))
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        ombre_violette(c, rr, 0.32, 26, 16)
        c.drawRRect(rr, pgrad(-w / 2, -h / 2, w / 2, h / 2, GRAD_VIF))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 1.5, -h / 2 + 1.5, w - 3, h - 3), h / 2, h / 2),
                    peinture("#FFFFFF", 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        x = -(tw + (taille * 1.2 if icone_ else 0)) / 2
        texte(c, label, x, -hauteurLigne(taille, "titre") / 2, taille, "#FFFFFF", "titre", track=-0.01)
        if icone_: icone(c, icone_, x + tw + taille * 0.75, 0, taille * 0.8, "#FFFFFF", 2.6)
    c.restore()
    return w, h


_FLECHE = [(0, 0), (0, 36), (9, 27.5), (15.5, 42), (22, 39), (15.5, 25), (27, 25)]


def curseur(c, x, y, s=1.0, alpha=1.0, appui=0.0):
    """pointeur de souris (pointe en x, y) ; appui 0→1 l'enfonce"""
    if alpha <= 0.01: return
    k = s * 1.6 * (1 - 0.18 * appui)
    pth = skia.Path(); pth.moveTo(x, y)
    for px, py in _FLECHE[1:]: pth.lineTo(x + px * k, y + py * k)
    pth.close()
    with Calque(c, alpha):
        p = skia.Paint(AntiAlias=True, Color=hexa("#2A1B5C", 0.25), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.save(); c.translate(3, 6); c.drawPath(pth, p); c.restore()
        c.drawPath(pth, peinture(S["encre"]))
        c.drawPath(pth, peinture("#FFFFFF", 1, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, StrokeJoin=skia.Paint.kRound_Join))


def clic(c, x, y, t, t0, couleur=None):
    onde(c, x, y, t, t0, 10, 90, couleur or S["violetVif"], 6, 0.5)
    onde(c, x, y, t, t0 + 0.08, 10, 60, couleur or S["bleuVif"], 4, 0.45)


def etoile4(c, cx, cy, r, couleur, alpha=1.0, rot=0.0):
    """étincelle à quatre branches (✦)"""
    if alpha <= 0.01 or r <= 0.5: return
    p = skia.Path(); n = 8
    for k in range(n):
        a = rot + k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.22
        (p.moveTo if k == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close(); c.drawPath(p, peinture(couleur, alpha))


def eclats(c, cx, cy, t, t0, n=10, r=300, cols=None, graine=3, duree=0.8):
    """étincelles ✦ et pastilles projetées depuis (cx, cy)"""
    if t < t0 or t > t0 + duree: return
    cols = cols or CONFETTIS
    rng = np.random.default_rng(graine); u = (t - t0) / duree
    for k in range(n):
        a = k / n * 2 * math.pi + rng.uniform(-0.3, 0.3)
        d = r * rng.uniform(0.6, 1.1) * sortie(min(1, u * 1.6))
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        al = 1 - max(0, u - 0.5) / 0.5
        if k % 3 == 0: disque(c, x, y, 9 * (1 - u * 0.5), cols[k % len(cols)], al)
        else: etoile4(c, x, y, 24 * (1 - u * 0.4), cols[k % len(cols)], al, u * 3 + k)


def rayons(c, cx, cy, t, r=900, alpha=0.12, n=14, couleur="#FFFFFF"):
    if alpha <= 0.01: return
    for k in range(n):
        a0 = t * 0.35 + k * 2 * math.pi / n
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + r * math.cos(a0 - 0.07), cy + r * math.sin(a0 - 0.07)); p.lineTo(cx + r * math.cos(a0 + 0.07), cy + r * math.sin(a0 + 0.07)); p.close()
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(couleur, alpha), hexa(couleur, 0.0)]))
        c.drawPath(p, g)


def losange(c, cx, cy, r, couleur, alpha=1.0, contour=None):
    p = skia.Path(); p.moveTo(cx, cy - r); p.lineTo(cx + r, cy); p.lineTo(cx, cy + r); p.lineTo(cx - r, cy); p.close()
    c.drawPath(p, peinture(couleur, alpha))
    if contour: c.drawPath(p, peinture(contour, alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))


def lueur_s(c, cx, cy, r, couleur=None, a=0.35):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(couleur or S["violetVif"], a), hexa(couleur or S["violetVif"], 0.0)]))
    c.drawCircle(cx, cy, r, p)


# ─────────────────────────────────────────── titres cinétiques, lettre par lettre
def _bezier(p0, p1, p2, p3, u):
    v = 1 - u
    return (v ** 3 * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u ** 3 * p3[0],
            v ** 3 * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u ** 3 * p3[1])


_GLYPHES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&?"


def lettres(c, s, cx, y, taille, t, t0, effet="ressort", fam="noir", couleur=None, grad=True, decal=0.035, duree=0.5,
            track=-0.03, alpha=1.0, align="centre", graine=1, sortie_t=None, cols=GRAD, onde_t=None):
    """titre construit lettre par lettre. effets : ressort (tombe et rebondit), masque (monte dans sa ligne),
    flou (net depuis grand et flou), chemin (vole le long d'une trajectoire d'animation, images clés visibles),
    glitch (caractères aléatoires puis la vraie lettre). sortie_t : les lettres repartent vers le haut.
    onde_t : vague qui fait sauter les lettres une à une (accent)."""
    if alpha <= 0.01 or t < t0 - 0.05: return largeur(s, taille, fam, track)
    couleur = couleur or S["encre"]
    w = largeur(s, taille, fam, track)
    x0 = cx - w / 2 if align == "centre" else cx
    hl = hauteurLigne(taille, fam)
    rng = np.random.default_rng(graine)
    ws = [largeur(ch, taille, fam, track) for ch in s]
    xs = [largeur(s[:i + 1], taille, fam, track) - ws[i] if i else 0.0 for i in range(len(s))]   # (une espace finale ne compte pas dans la mesure)
    traces = []
    if grad: cm = Degrade(c, x0, y, x0 + w, y + hl, cols, alpha)
    else: cm = Calque(c, alpha)
    with cm:
        for i, ch in enumerate(s):
            dep = [rng.uniform(-1, 1) for _ in range(4)]
            if ch == " ": continue
            ti = t0 + i * decal
            if t < ti - 0.001: continue
            u = borne((t - ti) / duree)
            lx, ly = x0 + xs[i], y
            cxl, cyl = lx + ws[i] / 2, ly + hl / 2
            dx = dy = rot = 0.0; sc = 1.0; al = 1.0; fl = 0.0; car = ch
            if effet == "ressort":
                v = ressort(u, 2.2, 5.0)
                dy = -taille * 1.1 * (1 - v); rot = 28 * dep[0] * (1 - v); sc = mix(0.4, 1, min(1, v)); al = borne(u * 5)
            elif effet == "masque":
                dy = hl * 1.05 * (1 - sortieExpo(u))
            elif effet == "flou":
                v = sortie(u); sc = mix(2.2, 1, v); fl = 14 * (1 - v); al = borne(u * 3)
            elif effet == "glitch":
                al = borne(u * 6)
                if u < 0.7: car = _GLYPHES[int((t * 30 + i * 7) % len(_GLYPHES))]
                dx = 10 * dep[1] * (1 - u) * math.sin(t * 90)
            elif effet == "chemin":
                v = sortie(u)
                p0 = (cxl + dep[0] * 520, cyl + 380 + dep[1] * 240)
                p1 = (p0[0] + dep[2] * 300, p0[1] - 420)
                p2 = (cxl + dep[3] * 220, cyl - 260)
                p3 = (cxl, cyl)
                px, py = _bezier(p0, p1, p2, p3, v)
                dx, dy = px - cxl, py - cyl
                rot = 40 * dep[1] * (1 - v); sc = mix(0.5, 1, v); al = borne(u * 4)
                traces.append((p0, p1, p2, p3, v, t - (ti + duree)))
            if sortie_t is not None and t > sortie_t + i * decal * 0.5:
                o = prog(t, sortie_t + i * decal * 0.5, 0.3, entree)
                dy -= 160 * o; al *= 1 - o; fl += 10 * o
            if onde_t is not None and onde_t + i * 0.04 <= t <= onde_t + i * 0.04 + 0.35:
                o = (t - onde_t - i * 0.04) / 0.35
                dy -= taille * 0.22 * math.sin(math.pi * o); sc *= 1 + 0.12 * math.sin(math.pi * o)
            if al <= 0.01: continue
            c.save(); c.translate(cxl + dx, cyl + dy); c.rotate(rot); c.scale(sc, sc); c.translate(-cxl, -cyl)
            if fl > 0.3:
                flou_calque(c, fl, al); texte(c, car, lx, ly, taille, couleur, fam, track=track); c.restore()
            else:
                texte(c, car, lx, ly, taille, couleur, fam, track=track, alpha=al)
            c.restore()
    # trajectoires d'animation : pointillés lilas et images clés en losange (par-dessus, hors dégradé)
    for (p0, p1, p2, p3, v, apres) in traces:
        a_tr = alpha * (1 - borne(apres / 0.45)) if apres > 0 else alpha
        if a_tr <= 0.02: continue
        pth = skia.Path(); pth.moveTo(*p0)
        n = 24
        for k in range(1, n + 1):
            pth.lineTo(*_bezier(p0, p1, p2, p3, v * k / n))
        pa = peinture(S["violetVif"], 0.55 * a_tr, Style=skia.Paint.kStroke_Style, StrokeWidth=3)
        pa.setPathEffect(skia.DashPathEffect.Make([8, 10], (t * 60) % 18)); c.drawPath(pth, pa)
        losange(c, p0[0], p0[1], 9, "#FFFFFF", a_tr, S["violetVif"])
        if v > 0.5: losange(c, *_bezier(p0, p1, p2, p3, 0.5), 7, S["violetVif"], a_tr * 0.8)
    return w


# ─────────────────────────────────────────── groupes de scène (entrée / sortie)
class Groupe:
    """transformation commune d'une scène : entrée (bas, droite, zoom, grand) et sortie (haut, gauche, zoom, recul)"""
    def __init__(self, c, t, t_in, t_out, ent="bas", sor="haut", d_in=0.42, d_out=0.3, cy=900):
        self.c, self.cy = c, cy
        ue = prog(t, t_in, d_in, sortieExpo) if ent != "aucune" else 1.0
        us = prog(t, t_out - d_out * 0.4, d_out, entree) if sor != "aucune" else (1.0 if t > t_out + 0.02 else 0.0)
        self.visible = t >= t_in - 0.01 and us < 0.999
        tx = ty = 0.0; s = 1.0; a = 1.0
        if ent == "bas": ty += 340 * (1 - ue); s *= mix(0.9, 1, ue); a *= borne(ue * 2.5)
        elif ent == "droite": tx += (W + 70) * (1 - ue)
        elif ent == "zoom": s *= mix(0.55, 1, ue); a *= borne(ue * 2.5)
        elif ent == "grand": s *= mix(1.7, 1, ue); a *= borne(ue * 2.5)
        if sor == "haut": ty -= 420 * us; a *= 1 - us
        elif sor == "gauche": tx -= (W + 70) * us
        elif sor == "zoom": s *= mix(1, 2.6, us); a *= 1 - us
        elif sor == "recul": s *= mix(1, 0.6, us); a *= 1 - us
        self.tx, self.ty, self.s, self.a = tx, ty, s, a
    def __enter__(self):
        c = self.c; c.save(); c.translate(W / 2 + self.tx, self.cy + self.ty); c.scale(self.s, self.s); c.translate(-W / 2, -self.cy)
        if self.a < 0.999: c.saveLayerAlpha(None, int(255 * borne(self.a)))
        return c
    def __exit__(self, *a):
        if self.a < 0.999: self.c.restore()
        self.c.restore()


def iris(c, cx, cy, r, dessin):
    """dessine `dessin(c)` à l'intérieur d'un disque de rayon r (révélation circulaire)"""
    if r <= 1: return
    c.save(); pth = skia.Path(); pth.addCircle(cx, cy, r); c.clipPath(pth, doAntiAlias=True)
    dessin(c); c.restore()


# ─────────────────────────────────────────── maquettes
def telephone_s(c, cx, cy, w, h, ecran=None, alpha=1.0, gris=0.0):
    """téléphone sombre sur fond clair : ombre violette douce, cadre métal, écran découpé"""
    x, y = cx - w / 2, cy - h / 2; k = w / 480
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 72 * k, 72 * k)
        ombre_violette(c, rr, 0.28, 40, 34)
        c.drawRRect(rr, pgrad(x, y, x + w, y + h, ["#4A4560", "#14111C", "#3A3550"]))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 6 * k, y + 6 * k, w - 12 * k, h - 12 * k), 66 * k, 66 * k), peinture("#06050A"))
        ex, ey, ew, eh = x + 14 * k, y + 14 * k, w - 28 * k, h - 28 * k
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(ex, ey, ew, eh), 58 * k, 58 * k), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(ex, ey, ew, eh), peinture("#FFFFFF"))
        if ecran: ecran(c, ex, ey, ew, eh)
        if gris > 0: c.drawRect(skia.Rect.MakeXYWH(ex, ey, ew, eh), peinture("#8E8A99", 0.55 * gris))
        rf = skia.Paint(AntiAlias=True)
        rf.setShader(skia.GradientShader.MakeLinear([skia.Point(ex, ey), skia.Point(ex + ew, ey + eh * 0.6)],
                                                    [hexa("#FFFFFF", 0.0), hexa("#FFFFFF", 0.10), hexa("#FFFFFF", 0.0)], [0.3, 0.42, 0.55]))
        c.drawRect(skia.Rect.MakeXYWH(ex, ey, ew, eh), rf)
        c.restore()
        rrect(c, cx - 58 * k, y + 28 * k, 116 * k, 32 * k, 16 * k, "#000000")


def barre_progression(c, x, y, w, u, h=14, cols=GRAD_VIF, fond=None, alpha=1.0, tete=True):
    with Calque(c, alpha):
        rrect(c, x, y - h / 2, w, h, h / 2, fond or S["lavande"])
        if u > 0.002:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - h / 2, max(h, w * u), h), h / 2, h / 2), pgrad(x, 0, x + w, 0, cols))
            if tete:
                lueur_s(c, x + w * u, y, h * 2.6, cols[-1], 0.45); disque(c, x + w * u, y, h * 0.75, "#FFFFFF")


def lignes_texte(c, x, y, w, n, t, t0, pas=0.08, h=14, ecart=30, cols=None, graine=2, accent=()):
    """paragraphe simulé : barres arrondies qui s'écrivent une à une ; accent = indices surlignés en lilas"""
    rng = np.random.default_rng(graine)
    for k in range(n):
        lw = w * (rng.uniform(0.55, 0.98) if k < n - 1 else 0.45)
        u = prog(t, t0 + k * pas, 0.22, sortie)
        if u <= 0: continue
        col = S["lilas"] if k in accent else (cols or S["ligne"])
        rrect(c, x, y + k * ecart, lw * u, h, h / 2, col)


TIMELINE_NOMS = ["Titre", "Formes", "Texte", "Son"]     # une version anglaise les remplace


def timeline(c, x, y, w, h, t, t0, t1, alpha=1.0):
    """panneau de montage : calques nommés, barres, images clés qui naissent, tête de lecture qui balaie"""
    with Calque(c, alpha):
        carte_s(c, x, y, w, h, 28)
        rangs = list(zip([tr(n_) for n_ in TIMELINE_NOMS], [S["violetVif"], S["bleuVif"], "#A87BFF", "#7FA2FF"]))
        rh = (h - 70) / len(rangs)
        texte(c, "00:00:0" + str(min(9, int(max(0, t - t0) * 3))), x + 28, y + 18, 22, S["gris"], "fort", track=0.02)
        for j in range(12):
            trait(c, x + 190 + j * (w - 220) / 11, y + 30, x + 190 + j * (w - 220) / 11, y + 40, S["ligne"], 2)
        for k, (nom, col) in enumerate(rangs):
            yy = y + 60 + k * rh
            texte(c, nom, x + 28, yy + rh / 2 - hauteurLigne(22, "fort") / 2, 22, S["encre2"], "fort", track=0)
            u = prog(t, t0 + 0.06 * k, 0.4, sortie)
            bx, bw = x + 190 + 40 * k, (w - 260 - 60 * k) * u
            rrect(c, bx, yy + rh * 0.22, bw, rh * 0.56, rh * 0.18, col, 0.28)
            for j in range(4):
                kx = bx + (w - 260 - 60 * k) * (0.08 + 0.29 * j)
                a = entre(t, t0 + 0.15 + 0.1 * j + 0.05 * k, 0.3, 2.4)
                if a > 0: losange(c, kx, yy + rh / 2, 9 * a, col, 1.0, "#FFFFFF")
        ph = x + 190 + (w - 220) * borne((t - t0) / max(0.1, t1 - t0))
        trait(c, ph, y + 26, ph, y + h - 14, S["rouge"], 3)
        losange(c, ph, y + 26, 10, S["rouge"])


def navigateur(c, x, y, w, h, url, contenu=None, alpha=1.0):
    with Calque(c, alpha):
        carte_s(c, x, y, w, h, 30, ombre=0.16)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 30, 30), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, 76), peinture(S["doux"]))
        trait(c, x, y + 76, x + w, y + 76, S["ligne"], 2, rond=False)
        for k, col in enumerate(["#FF6159", "#FFBD2E", "#28C941"]):
            disque(c, x + 40 + 30 * k, y + 38, 9, col)
        rrect(c, x + 150, y + 18, w - 190, 40, 20, "#FFFFFF")
        icone(c, "lock", x + 178, y + 38, 18, S["gris"], 2.4)
        texte(c, url, x + 198, y + 38 - hauteurLigne(22, "demi") / 2, 22, S["gris"], "demi", track=0)
        if contenu: contenu(c, x, y + 78, w, h - 78)
        c.restore()


# ─────────────────────────────────────────── sous-titres fins à l'encre
from agence import SousTitresFins


class SousTitresEncre(SousTitresFins):
    """comme SousTitresFins, mais la phrase précédente libère la place avant que la suivante ne se pose"""
    def dessine(self, c, t, couleur=None):
        couleur = couleur or S["encre"]
        for k, pos in enumerate(self.mise):
            t_deb = pos[0][1] - 0.05
            t_fin = self.mise[k + 1][0][1] - 0.16 if k + 1 < len(self.mise) else 1e9
            if t < t_deb or t > t_fin + 0.14: continue
            o = prog(t, t_fin, 0.12, entree)
            for txt, t0, x, y in pos:
                u = 1.0 if t0 <= 0.05 else prog(t, t0 - 0.03, 0.22, sortie)
                if u <= 0: continue
                from agence import texte_flou
                texte_flou(c, txt, x, y + mix(18, 0, u) - 30 * o, self.taille, couleur, self.fam,
                           alpha=u * (1 - o), flou=mix(8, 0, u) + 8 * o)


def sous_titres(K, fusions=None):
    """zone sûre TikTok / Snap (17/10/2026) : sur un téléphone 19,5:9, l'appli rogne ~96 px de chaque côté de la vidéo
    et la colonne de boutons couvre x > 860 de y 816 à 1555 → bloc décalé à gauche, 640 px de large (x 180-820)"""
    return SousTitresEncre(K, fusions=fusions, y=1410, larg=640, taille=50, fam="fort", max_mots=5, cx=500)


# ═══════════════════════════════════════════ CORPS COMMUN (de « Aujourd'hui » à la fin)
# M : repères en secondes. Clés : b1 (début « Aujourd'hui »), produit, service, message, oblige, page,
# b2 (début phrase motion), motion, captive, regarde, comprend, action, b3 (« Résultat » / « La différence »),
# attention, demandes, clients, b4 (phrase du site), site, expliquer, facon, simple, [long_texte], b5 (« On écrit »),
# script, anime, accroches, tester, prix, deux, qvd, euros, devis, url, fin. titre_b3 : « RÉSULTAT » …

def scene_b1(c, t, M):
    g = Groupe(c, t, M["b1"] - 0.12, M["b2"] - 0.05, ent="zoom", sor="gauche", d_out=0.32)
    if not g.visible: return
    with g:
        so = prog(t, M["page"] - 0.25, 0.3, entreeSortie)          # le titre laisse la place à la page
        lettres(c, tr("AUJOURD'HUI,"), 540, 300 - 60 * so, 124, t, M["b1"] - 0.08, "ressort", decal=0.03, alpha=1 - so)
        cartes = [(tr("Un produit"), "package", M["produit"], -1), (tr("Un service"), "briefcase", M["service"], 0), (tr("Ton message"), "megaphone", M["message"], 1)]
        serre = prog(t, M["oblige"] - 0.1, 0.45, entreeSortie)
        for k, (lab, ic, t0, pos) in enumerate(cartes):
            a = entre(t, t0 - 0.12, 0.5, 1.4)
            if a <= 0: continue
            x = 540 + pos * 340 * (1 - serre) + pos * 40 * serre
            y = 840 + 20 * math.sin(t * 2.4 + k) * (1 - serre) - 120 * serre + abs(pos) * 30 * serre
            with Espace(c, x, y, ry=mix(-95, 0, a) + 8 * pos * (1 - serre), rz=pos * 9 * serre, s=mix(1, 0.72, serre)):
                with Calque(c, borne(a * 3) * (1 - 0.35 * so)):
                    carte_s(c, x - 150, y - 175, 300, 350, 36)
                    yy = y - 60
                    if ic == "package": yy += -18 * abs(math.sin((t - t0) * 5)) * (1 - serre)
                    tuile(c, ic, x, yy, 124, rot=(8 * math.sin((t - t0) * 6) if ic == "briefcase" else 0) * (1 - serre))
                    if ic == "megaphone":
                        for j in range(3):
                            ph = ((t - t0) * 1.6 + j / 3) % 1
                            p = skia.Path(); r = 70 + 50 * ph
                            p.addArc(skia.Rect.MakeXYWH(x + 20 - r, yy - r, 2 * r, 2 * r), -35, 70)
                            c.drawPath(p, peinture(S["violetVif"], (1 - ph) * 0.8, Style=skia.Paint.kStroke_Style, StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap))
                    texte(c, lab, x, y + 70, 36, S["encre"], "titre", "centre", -0.02)
                    rrect(c, x - 70, y + 128, 140, 10, 5, S["lavande"])
        # « à la page » : une page qui se rabat en 3D, coche verte
        a = prog(t, M["page"] - 0.22, 0.55, lambda v: rebond(v, 1.3))
        if a > 0:
            cx, cy = 540, 1000
            with Espace(c, cx, cy - 230, rx=mix(-100, 0, a), s=1.0):
                with Calque(c, borne(a * 3)):
                    carte_s(c, cx - 380, cy - 230, 760, 400, 40, ombre=0.18)
                    for j in range(3): rrect(c, cx - 300, cy - 180 + j * 26, 260 - 60 * j, 12, 6, S["lavande"])
                    texte_grad(c, tr("À LA PAGE"), cx, cy - 70, 118, "noir", "centre", -0.035)
                    rrect(c, cx - 300, cy + 100, 600, 12, 6, S["doux"])
            b = entre(t, M["page"] + 0.12, 0.4, 2.4)
            if b > 0:
                c.save(); c.translate(cx + 360, cy - 220); c.scale(b, b); c.rotate(-12 * (1 - b))
                disque(c, 0, 0, 62, S["vert"], 1.0, (10, 24, 0.2)); icone(c, "check", 0, 0, 70, "#FFFFFF", 3.4)
                c.restore()
            eclats(c, cx + 360, cy - 220, t, M["page"] + 0.16, 10, 220, graine=5)


def scene_b2(c, t, M):
    g = Groupe(c, t, M["b2"] - 0.1, M["b3"] - 0.05, ent="droite", sor="zoom", d_in=0.36)
    if not g.visible: return
    with g:
        # MOTION DESIGN : chaque lettre arrive par sa trajectoire, images clés visibles
        up = prog(t, M["captive"] - 0.15, 0.4, entreeSortie)
        y0 = 290 - 40 * up
        with Calque(c, 1 - 0.0 * up):
            c.save(); c.translate(540, y0 + 130); c.scale(mix(1, 0.62, up), mix(1, 0.62, up)); c.translate(-540, -(y0 + 130))
            lettres(c, "MOTION", 540, y0, 150, t, M["motion"] - 0.45, "chemin", decal=0.045, duree=0.55, graine=7, grad=False, couleur=S["encre"])
            lettres(c, "DESIGN", 540, y0 + 150, 150, t, M["motion"] - 0.25, "chemin", decal=0.045, duree=0.55, graine=9)
            c.restore()
        # la timeline de montage sous le titre
        ta = entre(t, M["motion"] - 0.1, 0.5, 1.2) * (1 - up)
        if ta > 0:
            with Espace(c, 540, 820, rx=mix(50, 0, ta), s=mix(0.8, 1, ta)):
                timeline(c, 90, 700, 900, 300, t, M["motion"] - 0.1, M["captive"], borne(ta * 2))
        # captivé : jauge d'attention qui s'affole puis se cale au maximum
        ja = entre(t, M["captive"] - 0.12, 0.5, 1.3)
        dn = prog(t, M["regarde"] - 0.12, 0.42, entreeSortie)
        if ja > 0:
            cx, cy = 540, mix(860, 640, dn)
            sc = mix(1, 0.62, dn)
            c.save(); c.translate(cx, cy); c.scale(sc * mix(0.5, 1, ja), sc * mix(0.5, 1, ja))
            with Calque(c, borne(ja * 3)):
                R = 250
                lueur_s(c, 0, 0, 380, S["violetVif"], 0.22)
                arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(-R, -R, 2 * R, 2 * R), 180, 180)
                c.drawPath(arc, peinture(S["lavande"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=44, StrokeCap=skia.Paint.kRound_Cap))
                v = ressort(prog(t, M["captive"], 0.9, lin), 1.6, 3.4)
                v = borne(v * 0.98 + 0.02 * math.sin(t * 30) * borne((t - M["captive"]) / 0.3), 0, 1.04)
                arc2 = skia.Path(); arc2.addArc(skia.Rect.MakeXYWH(-R, -R, 2 * R, 2 * R), 180, 180 * min(1, v))
                pa = pgrad(-R, 0, R, 0, GRAD_VIF); pa.setStyle(skia.Paint.kStroke_Style); pa.setStrokeWidth(44); pa.setStrokeCap(skia.Paint.kRound_Cap)
                c.drawPath(arc2, pa)
                for j in range(9):
                    a_ = math.pi + j * math.pi / 8
                    trait(c, (R - 60) * math.cos(a_), (R - 60) * math.sin(a_), (R - 80) * math.cos(a_), (R - 80) * math.sin(a_), S["grisClair"], 4)
                ang = math.pi + math.pi * min(1.03, v)
                trait(c, 0, 0, (R - 70) * math.cos(ang), (R - 70) * math.sin(ang), S["encre"], 12)
                disque(c, 0, 0, 26, S["encre"]); disque(c, 0, 0, 10, "#FFFFFF")
                texte(c, "ATTENTION", 0, 40, 30, S["gris"], "titre", "centre", 0.16)
                texte_grad(c, tr("CAPTIVÉ"), 0, 90, 104, "noir", "centre", -0.03)
            c.restore()
            onde(c, cx, cy, t, M["captive"] + 0.35, 120, 420, S["violetVif"], 8, 0.6)
        # il regarde → il comprend → il agit
        etapes = [(tr("Il regarde"), "eye", M["regarde"]), (tr("Il comprend"), "lightbulb", M["comprend"]), (tr("Il agit"), "mouse-pointer-click", M["action"])]
        xs = [210, 540, 870]; yN = 1060
        for k in range(2):
            u = prog(t, etapes[k + 1][2] - 0.25, 0.3, sortie)
            if u > 0:
                xa, xb = xs[k] + 110, xs[k + 1] - 110
                trait(c, xa, yN, xa + (xb - xa) * u, yN, S["lilas"], 6)
                if u >= 1: losange(c, (xa + xb) / 2, yN, 10, S["violetVif"])
        for k, (lab, ic, t0) in enumerate(etapes):
            a = entre(t, t0 - 0.12, 0.45, 2.0)
            if a <= 0: continue
            x = xs[k]
            c.save(); c.translate(x, yN); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
            with Calque(c, borne(a * 3)):
                if k == 1:
                    on = prog(t, t0 + 0.1, 0.3, sortie)
                    rayons(c, 0, 0, t * 3, 180, 0.35 * on, 10, S["or_"])
                    lueur_s(c, 0, 0, 170, S["or_"], 0.4 * on)
                carte_s(c, -100, -100, 200, 200, 52, ombre=0.14)
                if k == 0:
                    cl = 1.0 if ((t - t0) % 1.4) > 0.12 else 0.15
                    c.save(); c.scale(1, cl); tuile(c, ic, 0, 0, 120); c.restore()
                elif k == 1:
                    tuile(c, ic, 0, 0, 120, "grad" if on > 0.5 else "doux")
                else:
                    tuile(c, ic, 0, 0, 120)
                texte(c, lab, 0, 124, 34, S["encre"], "titre", "centre", -0.02)
            c.restore()
            onde(c, x, yN, t, t0 - 0.02, 90, 190, S["violetVif"], 5, 0.5)
        # l'action : un bouton « Réserver » cliqué
        ba = entre(t, M["action"] - 0.05, 0.4, 2.0)
        if ba > 0:
            ap = prog(t, M["action"] + 0.3, 0.1, sortie) * (1 - prog(t, M["action"] + 0.42, 0.15, sortie))
            bouton(c, tr("Réserver"), 870, 1270, 34, mix(0.4, 1, ba) * (1 - 0.06 * ap), borne(ba * 3), "check" if t > M["action"] + 0.4 else "arrow-right")
            cxu = mix(1040, 900, prog(t, M["action"], 0.32, sortie)); cyu = mix(1420, 1286, prog(t, M["action"], 0.32, sortie))
            curseur(c, cxu, cyu, 1.0, borne(ba * 3), ap)
            clic(c, 900, 1280, t, M["action"] + 0.34)


def courbe(u):
    """courbe de croissance (0..1 → 0..1), avec de petites respirations"""
    return 0.06 + 0.86 * (u ** 1.8) + 0.035 * math.sin(u * 17) * u


def scene_b3(c, t, M):
    g = Groupe(c, t, M["b3"] - 0.1, M["b4"] - 0.05, ent="grand", sor="haut", d_in=0.45)
    if not g.visible: return
    with g:
        lettres(c, M.get("titre_b3", "RÉSULTAT"), 540, 250, 96, t, M["b3"] - 0.05, "masque", decal=0.03, duree=0.45)
        x, y, w, h = 90, 410, 900, 640
        a = entre(t, M["b3"], 0.5, 1.2)
        with Espace(c, 540, y + h / 2, rx=mix(-40, 0, a), s=mix(0.85, 1, a)):
            with Calque(c, borne(a * 3)):
                carte_s(c, x, y, w, h, 40, ombre=0.14)
                tuile(c, "chart-line", x + 70, y + 66, 76)
                texte(c, tr("Ton activité"), x + 128, y + 44, 38, S["encre"], "titre", track=-0.02)
                pd = 0.5 + 0.5 * math.sin(t * 6)
                w_ = pill(c, tr("En direct"), x + w - 130, y + 66, 22, "vert")
                disque(c, x + w - 130 - w_ / 2 + 18, y + 66, 6, S["vert"], 0.4 + 0.6 * pd)
                # graphique
                gx, gy, gw, gh = x + 50, y + 140, w - 100, 300
                for j in range(4): trait(c, gx, gy + j * gh / 3, gx + gw, gy + j * gh / 3, S["ligne"], 2, pointille=[8, 10])
                u = prog(t, M["b3"] + 0.1, M["clients"] + 0.35 - M["b3"], lambda v: entreeSortie(v) * 0.4 + sortie(v) * 0.6)
                if u > 0:
                    n = 70; pts = [(gx + gw * k / n * u, gy + gh * (1 - courbe(k / n * u))) for k in range(n + 1)]
                    aire = skia.Path(); aire.moveTo(gx, gy + gh)
                    for p in pts: aire.lineTo(*p)
                    aire.lineTo(pts[-1][0], gy + gh); aire.close()
                    pa = skia.Paint(AntiAlias=True)
                    pa.setShader(skia.GradientShader.MakeLinear([skia.Point(0, gy), skia.Point(0, gy + gh)], [hexa(S["violetVif"], 0.28), hexa(S["bleuVif"], 0.0)]))
                    c.drawPath(aire, pa)
                    ligne = skia.Path(); ligne.moveTo(*pts[0])
                    for p in pts[1:]: ligne.lineTo(*p)
                    pl = pgrad(gx, 0, gx + gw, 0, GRAD_VIF); pl.setStyle(skia.Paint.kStroke_Style); pl.setStrokeWidth(9); pl.setStrokeCap(skia.Paint.kRound_Cap); pl.setStrokeJoin(skia.Paint.kRound_Join)
                    c.drawPath(ligne, pl)
                    hx, hy = pts[-1]
                    lueur_s(c, hx, hy, 60, S["violetVif"], 0.45); disque(c, hx, hy, 15, "#FFFFFF"); anneau(c, hx, hy, 15, S["violet"], 6)
                    if u > 0.25:
                        b = borne((u - 0.25) * 4)
                        c.save(); c.translate(hx - 30, hy - 66); c.scale(b, b)
                        rrect(c, -46, -28, 92, 56, 18, S["encre"]); icone(c, "trending-up", 0, 0, 34, "#FFFFFF", 2.8)
                        c.restore()
                # trois indicateurs, sans chiffres
                kpi = [(tr("Attention"), "eye", M["attention"]), (tr("Demandes"), "message-circle", M["demandes"]), (tr("Clients"), "users", M["clients"])]
                for k, (lab, ic, t0) in enumerate(kpi):
                    b = entre(t, t0 - 0.1, 0.45, 2.2)
                    if b <= 0: continue
                    kx = x + 50 + k * 275; ky = y + 470
                    c.save(); c.translate(kx + 125, ky + 65); c.scale(mix(0.4, 1, b), mix(0.4, 1, b)); c.translate(-(kx + 125), -(ky + 65))
                    with Calque(c, borne(b * 3)):
                        rrect(c, kx, ky, 250, 130, 26, S["doux"])
                        tuile(c, ic, kx + 50, ky + 46, 56, "doux", ep=2.4)
                        texte(c, lab, kx + 90, ky + 28, 28, S["encre"], "titre", track=-0.02)
                        icone(c, "trending-up", kx + 214, ky + 46, 34, S["vert"], 3.0)
                        fil = prog(t, t0, 0.6, sortie)
                        rrect(c, kx + 24, ky + 92, 202, 12, 6, S["lavande"])
                        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(kx + 24, ky + 92, 202 * mix(0.15, 0.92, fil), 12), 6, 6), pgrad(kx, 0, kx + 230, 0, GRAD_VIF))
                    c.restore()
        # notifications « Nouvelle demande » : la plus récente en haut, les autres glissent dessous
        arrivees = [M["demandes"] - 0.05, M["demandes"] + 0.22, M["clients"] - 0.05]
        for k, t0 in enumerate(arrivees):
            b = entre(t, t0, 0.45, 1.6)
            if b <= 0: continue
            yy = 1100 + 92 * sum(prog(t, t1, 0.35, sortie) for t1 in arrivees[k + 1:])
            xx = 110 + 900 * (1 - sortieExpo(prog(t, t0, 0.4, lin)))
            with Calque(c, borne(b * 3)):
                carte_s(c, xx, yy, 860, 76, 24, ombre=0.12)
                tuile(c, "bell", xx + 44, yy + 38, 48, "grad")
                texte(c, tr("Nouvelle demande") if k < 2 else tr("Nouveau client"), xx + 86, yy + 38 - hauteurLigne(28, "titre") / 2, 28, S["encre"], "titre", track=-0.02)
                texte(c, tr("à l'instant"), xx + 830, yy + 38 - hauteurLigne(22, "demi") / 2, 22, S["gris"], "demi", "droite", 0)


def ecran_explicatif(c, x, y, w, h, t, t_play, M):
    """le film explicatif dans le lecteur du site : 1 Devis → 2 Conception → 3 Pose"""
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pgrad(x, y, x + w, y + h, ["#F4EEFF", "#E9F0FF"]))
    if t < t_play:
        lueur_s(c, x + w / 2, y + h / 2, 200, S["violetVif"], 0.25)
        disque(c, x + w / 2, y + h / 2, 62, S["violet"], 1.0, (8, 20, 0.2)); icone(c, "play", x + w / 2 + 5, y + h / 2, 56, "#FFFFFF", 2.6)
        return
    etapes = [(tr("Devis"), "receipt"), (tr("Conception"), "paintbrush"), (tr("Pose"), "hammer")]
    dt = (M["simple"] - t_play) / 3.2
    for k, (lab, ic) in enumerate(etapes):
        t0 = t_play + 0.08 + k * dt
        a = entre(t, t0, 0.4, 2.0)
        if a <= 0: continue
        cx = x + w * (0.2 + 0.3 * k); cy = y + h * 0.44
        if k > 0:
            u = prog(t, t0 - 0.12, 0.2, sortie)
            trait(c, cx - w * 0.3 + 56, cy, cx - w * 0.3 + 56 + (w * 0.3 - 112) * u, cy, S["violetVif"], 5)
        c.save(); c.translate(cx, cy); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
        tuile(c, ic, 0, 0, 92)
        disque(c, 38, -38, 18, S["encre"]); texte_centre_s(c, str(k + 1), 38, -38, 20, "#FFFFFF")
        texte(c, lab, 0, 62, 26, S["encre"], "titre", "centre", -0.02)
        c.restore()
    barre_progression(c, x + 30, y + h - 26, w - 60, borne((t - t_play) / (M["simple"] + 0.4 - t_play)), 8, tete=False)


def texte_centre_s(c, s, cx, cy, taille, couleur, fam="noir"):
    texte(c, s, cx, cy - hauteurLigne(taille, fam) / 2, taille, couleur, fam, "centre", 0)


def scene_b4(c, t, M):
    g = Groupe(c, t, M["b4"] - 0.1, M["b5"] - 0.05, ent="bas", sor="recul", d_in=0.45)
    if not g.visible: return
    with g:
        a = entre(t, M["site"] - 0.12, 0.4, 2.2)
        pill(c, tr("Sur ton site"), 540, 300, 36, "grad", "laptop", borne(a * 3), mix(0.4, 1, a))
        x, y, w, h = 80, 400, 920, 860
        b = entre(t, M["b4"] - 0.05, 0.55, 1.2)
        t_play = M["expliquer"] - 0.05
        def contenu(cc, x_, y_, w_, h_):
            cc.drawRect(skia.Rect.MakeXYWH(x_, y_, w_, h_), peinture("#FFFFFF"))
            texte(cc, "MOREL", x_ + 44, y_ + 30, 34, S["encre"], "noir", track=0.06)
            texte(cc, tr("· cuisines"), x_ + 168, y_ + 36, 26, S["gris"], "demi", track=0)
            for j in range(3): rrect(cc, x_ + w_ - 330 + j * 100, y_ + 46, 70, 10, 5, S["ligne"])
            texte(cc, tr("Votre cuisine,"), x_ + 44, y_ + 110, 56, S["encre"], "titre", track=-0.035)
            texte_grad(cc, tr("sur mesure."), x_ + 44, y_ + 172, 56, "titre", "gauche", -0.035)
            vx, vy, vw = x_ + 44, y_ + 270, w_ - 88
            vh = vw * 9 / 16
            cc.save(); cc.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(vx, vy, vw, vh), 22, 22), doAntiAlias=True)
            ecran_explicatif(cc, vx, vy, vw, vh, t, t_play, M)
            cc.restore()
            cc.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(vx, vy, vw, vh), 22, 22), peinture(S["ligne"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        with Espace(c, 540, y + h / 2, rx=mix(45, 0, b), s=mix(0.75, 1, b) * (1 + 0.012 * math.sin(t * 1.5))):
            navigateur(c, x, y, w, h, tr("cuisines-morel.fr"), contenu, borne(b * 3))
        # « sans un long texte » : le pavé de texte qu'on ne lira pas, barré
        if "long_texte" in M:
            la = entre(t, M["long_texte"] - 0.12, 0.45, 1.6)
            if la > 0:
                c.save(); c.translate(760, 1200); c.rotate(5); c.scale(mix(0.5, 1, la), mix(0.5, 1, la))
                with Calque(c, borne(la * 3)):
                    carte_s(c, -230, -110, 460, 220, 28, ombre=0.16)
                    lignes_texte(c, -190, -76, 380, 6, t, M["long_texte"] - 0.1, 0.03, 12, 26, cols=S["grisClair"])
                    bar = prog(t, M["long_texte"] + 0.25, 0.22, sortie)
                    if bar > 0:
                        trait(c, -210, 60, -210 + 420 * bar, -60, S["rouge"], 10)
                        bb = entre(t, M["long_texte"] + 0.4, 0.35, 2.4)
                        if bb > 0:
                            disque(c, 210, -100, 34 * bb, S["rouge"]); icone(c, "x", 210, -100, 38 * bb, "#FFFFFF", 3.4)
                c.restore()
        # le curseur va appuyer sur lecture
        cu = prog(t, t_play - 0.5, 0.42, sortie)
        if cu > 0:
            ap = prog(t, t_play - 0.06, 0.06, sortie) * (1 - prog(t, t_play + 0.05, 0.12, sortie))
            px, py = mix(980, 545, cu), mix(1500, 870, cu)
            curseur(c, px, py, 1.0, 1 - prog(t, t_play + 0.5, 0.3, sortie), ap)
            clic(c, 545, 870, t, t_play)
        d = entre(t, M["simple"] - 0.08, 0.4, 2.4)
        if d > 0:
            c.save(); c.translate(880, 470); c.rotate(-8); c.scale(mix(2.2, 1, prog(t, M["simple"] - 0.08, 0.2, entree)), mix(2.2, 1, prog(t, M["simple"] - 0.08, 0.2, entree)))
            pill(c, tr("Clair"), 0, 0, 38, "vert", "circle-check", borne(d * 3))
            c.restore()
            eclats(c, 880, 470, t, M["simple"], 10, 200, graine=8)


ACCROCHES = [("01", "Le problème", "Tes clients ne comprennent pas ?"), ("02", "Le bénéfice", "Compris en quelques secondes."),
             ("03", "La curiosité", "Ton meilleur vendeur ?"), ("04", "La solution", "Montre. Donne envie.")]


def mini_ecran_accroche(c, x, y, w, h, t, k):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pgrad(x, y, x + w, y + h, [GRAD_VIF[0], GRAD_VIF[2]] if k % 2 == 0 else ["#2A1E52", "#4B3A9A"]))
    num, nom, phrase = ACCROCHES[k]; nom, phrase = tr(nom), tr(phrase)
    texte(c, num, x + 24, y + 70, 26, "#FFFFFF", "titre", track=0.06, alpha=0.7)
    texte(c, nom.upper(), x + 24, y + 104, 20, "#FFFFFF", "titre", track=0.1, alpha=0.8)
    mots = phrase.split(" ")
    ly = y + 170; lx = x + 24
    for j, m in enumerate(mots):
        tl = 34; mw = largeur(m, tl, "noir")
        if lx + mw > x + w - 20: lx = x + 24; ly += 42
        bump = 6 * math.sin(t * 5 + j + k)
        texte(c, m, lx, ly + bump * 0.3, tl, "#FFFFFF", "noir", track=-0.02); lx += mw + 10
    barre_progression(c, x + 20, y + h - 40, w - 40, ((t * 0.5 + k * 0.23) % 1), 8, ["#FFFFFF", "#FFFFFF"], "#FFFFFF40", tete=False)


def scene_b5(c, t, M):
    g = Groupe(c, t, M["b5"] - 0.1, (M["prix"] if M.get("prix") is not None else M.get("decolle", M["devis"])) - 0.1, ent="droite", sor="aucune" if "decolle" not in M else "zoom", d_in=0.38)
    if not g.visible: return
    with g:
        part = prog(t, M["accroches"] - 0.35, 0.4, entreeSortie)        # script et animation s'envolent
        ani = prog(t, M["anime"] - 0.2, 0.45, entreeSortie)
        if part < 1:
            with Calque(c, 1 - part):
                # carte SCRIPT
                a = entre(t, M["b5"] - 0.05, 0.5, 1.4)
                sx = mix(540, 300, ani); sy = 820 - 700 * part
                with Espace(c, sx, sy, ry=mix(-70, 0, a) + 10 * ani, rz=-4 * ani, s=mix(1, 0.78, ani)):
                    with Calque(c, borne(a * 3)):
                        carte_s(c, sx - 230, sy - 300, 460, 600, 36, ombre=0.15)
                        texte(c, "SCRIPT.txt", sx - 190, sy - 262, 26, S["gris"], "titre", track=0.06)
                        disque(c, sx + 186, sy - 248, 8, S["violetVif"])
                        lignes_texte(c, sx - 190, sy - 190, 380, 11, t, M["script"] - 0.15, 0.07, 14, 40, accent=(1, 2, 6))
                        k = int(borne((t - M["script"] + 0.15) / 0.07, 0, 10))
                        if int(t * 5) % 2 == 0 and t < M["anime"]: rrect(c, sx - 190 + 300, sy - 196 + k * 40, 4, 26, 2, S["violet"])
                pill(c, "SCRIPT", sx, sy + 360 * mix(1, 0.78, ani), 32, "blanc", "file-text", borne(a * 3), mix(1, 0.85, ani))
                # carte ANIMATION
                b = entre(t, M["anime"] - 0.15, 0.5, 1.4)
                if b > 0:
                    ax, ay = 790, 820 - 700 * part
                    with Espace(c, ax, ay, ry=mix(70, 0, b), rz=4, s=0.82):
                        with Calque(c, borne(b * 3)):
                            carte_s(c, ax - 230, ay - 300, 460, 600, 36, ombre=0.15)
                            # une balle qui rebondit sur sa trajectoire
                            ph = ((t - M["anime"]) * 1.4) % 1
                            bx = ax - 150 + 300 * ph; by = ay - 40 - 200 * abs(math.sin(math.pi * ph * 2))
                            pth = skia.Path(); pth.moveTo(ax - 150, ay - 40)
                            for j in range(1, 41):
                                q = j / 40; pth.lineTo(ax - 150 + 300 * q, ay - 40 - 200 * abs(math.sin(math.pi * q * 2)))
                            pa = peinture(S["lilas"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=4); pa.setPathEffect(skia.DashPathEffect.Make([8, 10], 0)); c.drawPath(pth, pa)
                            for q in (0, 0.25, 0.5, 0.75, 1.0): losange(c, ax - 150 + 300 * q, ay - 40 - 200 * abs(math.sin(math.pi * q * 2)), 9, "#FFFFFF", 1, S["violetVif"])
                            sq = 1 + 0.25 * max(0, 1 - abs(math.sin(math.pi * ph * 2)) * 6)
                            c.save(); c.translate(bx, by); c.scale(sq, 1 / sq)
                            c.drawCircle(0, -32, 32, pgrad(-32, -64, 32, 0, GRAD_VIF)); c.restore()
                            timeline(c, ax - 205, ay + 60, 410, 210, t, M["anime"] - 0.1, M["accroches"], 1.0)
                    pill(c, "ANIMATION", ax, ay + 300, 32, "blanc", "clapperboard", borne(b * 3), 0.85)
        # 3 OU 4 ACCROCHES : quatre écrans qui s'ouvrent en éventail
        if t > M["accroches"] - 0.3:
            lettres(c, tr("3 OU 4"), 540, 250, 110, t, M["accroches"] - 0.25, "ressort", decal=0.04)
            lettres(c, tr("ACCROCHES"), 540, 370, 110, t, M["accroches"] - 0.05, "masque", decal=0.03, duree=0.4)
            for k in range(4):
                a = entre(t, M["accroches"] - 0.1 + 0.08 * k, 0.55, 1.5)
                if a <= 0: continue
                ang = mix(0, (-1.5 + k) * 11, a)
                cx = 540 + mix(0, (-1.5 + k) * 215, a); cy = 920 + abs(-1.5 + k) * 40 * a
                gagne = k == 1 and t > M["tester"] - 0.05
                lev = prog(t, M["tester"] - 0.05, 0.35, lambda v: rebond(v, 1.8)) if k == 1 else 0
                c.save(); c.translate(cx, cy - 90 * lev); c.rotate(ang * (1 - lev)); c.scale(1 + 0.12 * lev, 1 + 0.12 * lev)
                telephone_s(c, 0, 0, 250, 500, lambda cc, ex, ey, ew, eh, k=k: mini_ecran_accroche(cc, ex, ey, ew, eh, t, k), borne(a * 3))
                if gagne:
                    disque(c, 100, -230, 40, S["or_"], 1.0, (8, 20, 0.2)); icone(c, "trophy", 100, -230, 42, "#FFFFFF", 2.6)
                c.restore()
            b = entre(t, M["tester"] - 0.1, 0.4, 2.2)
            if b > 0:
                pill(c, tr("À tester"), 540, 1300, 34, "encre", "split", borne(b * 3), mix(0.4, 1, b))
                eclats(c, 540, 830, t, M["tester"] + 0.1, 12, 360, graine=11)


# ─────────────────────────────────────────── prix (aplat dégradé, rouleaux de chiffres)
def rouleau(c, chiffre, x, y, taille, t, t_dep, t_arr, couleur="#FFFFFF"):
    """colonne de chiffres qui défile puis se cale (avec rebond) sur `chiffre`"""
    hl = taille * 1.05
    tours = 2 * 10 + chiffre
    u = borne((t - t_dep) / max(0.05, t_arr - t_dep))
    v = ressort(u, 1.4, 4.0) if u < 1 else 1.0
    pos = tours * min(1.06, v) if u > 0 else 0.0
    w = largeur("0", taille, "noir", -0.04)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x - 10, y - hl * 0.05, w + 20, hl * 1.08))
    for j in range(int(pos) - 1, int(pos) + 2):
        d = (j - pos) * hl
        texte(c, str(j % 10), x, y + d, taille, couleur, "noir", track=-0.04)
    c.restore()
    return w


def scene_prix(c, t, M):
    if M.get("prix") is None: return          # version sans prix : on laisse le site l'annoncer
    t_in, t_out = M["prix"] - 0.22, M["devis"] - 0.12
    if t < t_in or t > t_out + 0.5: return
    R = cles(t, [(t_in, 0), (t_in + 0.42, 1500, sortieExpo), (t_out, 1500), (t_out + 0.4, 0, entreeSortie)])
    cyc = mix(1000, 1060, prog(t, t_out, 0.4, entreeSortie))
    ch_, dev, avant = PRIX["chiffres"], PRIX["devise"], PRIX["avant"]
    def dessin(cc):
        fond_grad(cc, t)
        rayons(cc, 540, 900, t, 1100, 0.10)
        a = entre(t, M["prix"] - 0.05, 0.4, 1.6)
        texte(cc, tr("À PARTIR DE"), 540, 560 + 20 * (1 - a), 46, "#FFFFFF", "titre", "centre", 0.14, borne(a * 3))
        taille = 300
        td = 190 if not avant else 210
        ws = [largeur(ch, taille, "noir", -0.04) for ch in ch_]
        we = largeur(dev, td, "noir", -0.02)
        tot = sum(ws) + we + 30
        xd = 540 - tot / 2 if avant else 540 - tot / 2 + sum(ws) + 30      # x de la devise
        x = 540 - tot / 2 + (we + 30 if avant else 0); y = 660
        arr = [M["deux"] + 0.08, M["qvd"] + 0.2, M["euros"] - 0.06]
        for k, ch in enumerate(ch_):
            rouleau(cc, int(ch), x, y, taille, t, M["prix"] - 0.05 + 0.04 * k, arr[k])
            x += ws[k]
        e = entre(t, M["euros"] - 0.05, 0.4, 2.6)
        if e > 0:
            cc.save(); cc.translate(xd + we / 2, y + 110); cc.scale(mix(0.2, 1, e), mix(0.2, 1, e))
            texte(cc, dev, 0, -hauteurLigne(td) / 2 + 20, td, "#FFFFFF", "noir", "centre", -0.02)
            cc.restore()
            if PRIX["mention"]:
                px_ = xd + we / 2 if not avant else 540
                pill(cc, PRIX["mention"], px_, y + 290 + (60 if avant else 0), 30, "blanc", None, borne(e * 3), mix(0.3, 1, e))
        # reflet qui balaie les chiffres
        sh = prog(t, M["euros"] + 0.1, 0.5, lin)
        if 0 < sh < 1:
            p = skia.Paint(AntiAlias=True)
            sxp = mix(-200, 1280, sh)
            p.setShader(skia.GradientShader.MakeLinear([skia.Point(sxp - 120, 0), skia.Point(sxp + 120, 0)], [hexa("#FFFFFF", 0), hexa("#FFFFFF", 0.35), hexa("#FFFFFF", 0)]))
            cc.drawRect(skia.Rect.MakeXYWH(0, y, W, 330), p)
        onde(cc, 540, 820, t, M["euros"], 120, 560, "#FFFFFF", 8, 0.7)
        eclats(cc, 540, 820, t, M["euros"] + 0.02, 16, 520, ["#FFFFFF", "#E3D6FF", S["or_"], "#C9D8FF"], graine=4, duree=0.9)
        chips = [("30–45 s", "clock"), (tr("3–4 accroches"), "layers"), (tr("Script inclus"), "file-text")]
        for k, (lab, ic) in enumerate(chips):
            b = entre(t, M["euros"] + 0.1 + 0.08 * k, 0.4, 2.2)
            pill(cc, lab, 540, 1130 + k * 92 + (40 if avant and PRIX["mention"] else 0), 30, "blanc", ic, borne(b * 3), mix(0.4, 1, b))
    iris(c, 540, cyc, R, dessin)


# ─────────────────────────────────────────── appel à l'action
def scene_cta(c, t, M, duree):
    t0 = M["devis"] - 0.15
    if t < t0: return
    a = entre(t, t0 + 0.05, 0.55, 1.5)
    iw, ih = taille_img("dyou-logo-horizontal-black"); lw = 640 * mix(0.6, 1, a)
    c.save()
    flou_calque(c, 14 * (1 - prog(t, t0 + 0.05, 0.35, sortie)), borne(a * 3))
    image(c, "dyou-logo-horizontal-black", 540 - lw / 2, 560 - lw * ih / iw / 2, lw)
    c.restore(); c.restore()
    b = prog(t, t0 + 0.2, 0.4, sortie)
    if b > 0:
        texte(c, tr("Ton offre, en mouvement."), 540, 700 + 20 * (1 - b), 52, S["encre"], "titre", "centre", -0.03, b)
    # le bouton naît de l'iris qui se referme
    bt = entre(t, M["devis"] + 0.18, 0.5, 1.8)
    tc = M["devis"] + 0.75
    ap = prog(t, tc - 0.06, 0.06, sortie) * (1 - prog(t, tc + 0.05, 0.14, sortie))
    pulse = 1 + 0.025 * max(0, math.sin((t - tc - 0.4) * 5)) if t > tc + 0.4 else 1
    if bt > 0:
        bouton(c, tr("Demander mon devis"), 540, 900, 44, mix(0.2, 1, bt) * (1 - 0.07 * ap) * pulse, borne(bt * 3))
    cu = prog(t, tc - 0.5, 0.45, sortie)
    if cu > 0:
        curseur(c, mix(960, 650, cu), mix(1300, 912, cu), 1.1, 1 - prog(t, tc + 0.6, 0.3, sortie), ap)
        clic(c, 650, 905, t, tc)
    eclats(c, 540, 900, t, tc + 0.02, 12, 420, graine=12)
    # barre d'adresse qui se tape
    ub = entre(t, M["url"] - 0.25, 0.45, 1.6)
    if ub > 0:
        with Calque(c, borne(ub * 3)):
            wb = 620; yb = 1080
            carte_s(c, 540 - wb / 2, yb - 44, wb, 88, 44, ombre=0.12)
            icone(c, "lock", 540 - wb / 2 + 50, yb, 28, S["vert"], 2.6)
            url = "dyou-agency.com"
            n = int(borne((t - M["url"]) / 0.5) * len(url) + 0.999) if t >= M["url"] else 0
            xs_ = 540 - wb / 2 + 84
            texte(c, url[:n], xs_, yb - hauteurLigne(38, "titre") / 2, 38, S["encre"], "titre", track=-0.01)
            if int(t * 3) % 2 == 0: rrect(c, xs_ + largeur(url[:n], 38, "titre", -0.01) + 4, yb - 22, 4, 44, 2, S["violet"])
    for k, (lab, ic) in enumerate(CTA_PILLS or [("30–45 s", "clock"), (tr("3–4 accroches"), "layers"), (tr("dès 290 € TTC"), "sparkles")]):
        b = entre(t, M["url"] + 0.4 + 0.08 * k, 0.4, 2.2)
        if b > 0:
            pill(c, lab, [215, 540, 865][k], 1230, 26, "doux", ic, borne(b * 3), mix(0.4, 1, b))


# ─────────────────────────────────────────── sons et flous du corps
def sons_corps(K, M):
    son, rapide = K.son, K.rapide
    son(M["b1"] - 0.12, "whoosh", -9)
    for i in range(10): son(M["b1"] - 0.05 + i * 0.03, "tick", -20)
    for k in ("produit", "service", "message"): son(M[k] - 0.12, "whoosh_court", -12); son(M[k], "pop", -11)
    son(M["oblige"] - 0.1, "swipe", -12)
    son(M["page"] - 0.2, "whoosh_bas", -10); son(M["page"] + 0.1, "impact_doux", -8); son(M["page"] + 0.14, "check", -10); son(M["page"] + 0.16, "ching", -14)
    son(M["b2"] - 0.1, "whoosh_long", -9)
    for i in range(12): son(M["motion"] - 0.45 + 0.045 * i, "blip", -19)
    son(M["motion"] + 0.25, "impact_doux", -10)
    for i in range(6): son(M["motion"] + 0.1 * i, "clic", -21)
    son(M["captive"] - 0.1, "montee", -11); son(M["captive"] + 0.35, "impact", -8)
    for k in ("regarde", "comprend", "action"): son(M[k] - 0.12, "pop", -11)
    son(M["comprend"] + 0.1, "ding", -14); son(M["action"] + 0.34, "clic", -7); son(M["action"] + 0.4, "check", -10)
    son(M["b3"] - 0.12, "whoosh", -9); son(M["b3"] + 0.1, "montee", -14)
    for k in ("attention", "demandes", "clients"): son(M[k] - 0.1, "pop", -11)
    son(M["demandes"] - 0.05, "message_in", -10); son(M["demandes"] + 0.22, "message_in", -12); son(M["clients"] - 0.05, "ching", -11)
    son(M["b4"] - 0.1, "swipe", -10); son(M["site"] - 0.12, "pop", -11)
    son(M["expliquer"] - 0.05, "clic", -7)
    for k in range(3): son(M["expliquer"] + 0.03 + k * (M["simple"] - M["expliquer"]) / 3.2, "blip", -15)
    if "long_texte" in M: son(M["long_texte"] + 0.2, "croc", -12)
    son(M["simple"] - 0.08, "tampon", -9); son(M["simple"], "check", -12)
    son(M["b5"] - 0.1, "whoosh", -10)
    for i in range(10): son(M["script"] - 0.15 + 0.07 * i, "frappe", -17)
    son(M["anime"] - 0.15, "whoosh_court", -11); son(M["anime"], "pop", -12)
    son(M["accroches"] - 0.35, "whoosh_long", -10)
    for k in range(4): son(M["accroches"] - 0.1 + 0.08 * k, "swipe", -15)
    son(M["tester"] - 0.05, "montee", -14); son(M["tester"] + 0.05, "ching", -11)
    if M.get("prix") is not None:
        son(M["prix"] - 0.22, "whoosh_bas", -8); son(M["prix"] - 0.05, "montee", -12)
        for i in range(14): son(M["prix"] + i * (M["euros"] - M["prix"]) / 14, "tick", -17)
        son(M["deux"] + 0.08, "clic", -10); son(M["qvd"] + 0.2, "clic", -10); son(M["euros"] - 0.06, "impact", -5); son(M["euros"], "ching", -9)
        son(M["euros"] + 0.1, "pop", -13)
    son(M["devis"] - 0.12, "whoosh", -9); son(M["devis"] + 0.18, "verre", -10); son(M["devis"] + 0.75, "clic", -6)
    for i in range(15): son(M["url"] + i * 0.034, "frappe", -18)
    son(M["url"] + 0.4, "pop", -13)
    for a, b in [(M["b1"] - 0.12, M["b1"] + 0.25), (M["b2"] - 0.15, M["b2"] + 0.3), (M["b3"] - 0.15, M["b3"] + 0.3),
                 (M["b4"] - 0.15, M["b4"] + 0.3), (M["b5"] - 0.15, M["b5"] + 0.3), (M["accroches"] - 0.35, M["accroches"] + 0.1),
                 *([(M["prix"] - 0.25, M["prix"] + 0.25), (M["prix"], M["euros"] + 0.05)] if M.get("prix") is not None else []),
                 (M["devis"] - 0.15, M["devis"] + 0.3)]:
        rapide(a, b)
