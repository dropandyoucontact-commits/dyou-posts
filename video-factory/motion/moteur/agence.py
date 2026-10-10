"""Style DYOU Agency (DA-M01, 10/10/2026) : fond sombre vivant, verre dépoli, violet du logo, sous-titres fins.

Demande de Youssef pour les vidéos de l'agence : plus de sous-titres « karaoké » qui surlignent le mot en vert ou
en violet. Ici le texte est fin et propre : la phrase en cours, en blanc, chaque mot qui se pose (flou → net,
petit glissement) au moment où il est prononcé ; la phrase s'efface d'un bloc quand la suivante arrive.

    from agence import *
    SOUS = SousTitresFins(K, fusions={(73, 74): "DYOU"})
    def dessine(c, t):
        fond_agence(c, t)
        ...
        SOUS.dessine(c, t)
"""
import math, re
import numpy as np
import skia
import moteur
from moteur import *

A = dict(fond="#07060C", violet="#7439FC", violetClair="#A98BFF", violetPale="#D9CCFF", indigo="#2A1B70",
         blanc="#FFFFFF", gris="#A7A3B8", grisFonce="#5F5B70", vert="#2BD67B", rouge="#FF4D5E",
         surAccent="#FFFFFF", poussiere="#C9B8FF", verreFond="#120E22", disque=("#8B5CFF", "#7439FC", "#4B1FC0"),
         bouton=("#9168FF", "#5B26E8"), logoDisque="logo-agence-blanc")
# « violet » = la couleur d'accent ; un thème la remplace (theme_athla : jaune-vert ATHLA, texte noir dessus)

# taches de lumière du fond : (x, y, rayon, couleur, alpha, vitesse, phase)
TACHES = [(140, 380, 760, "#5B2BD6", 0.42, 0.23, 0.0), (980, 1560, 820, "#3A1FA0", 0.40, 0.17, 1.7),
           (860, 200, 560, "#7439FC", 0.22, 0.29, 3.1), (80, 1760, 600, "#1E1660", 0.45, 0.21, 4.4)]


def _taches(c, t, gain=1.0, dx=0.0):
    for x, y, r, col, a, v, ph in TACHES:
        cx = x + 90 * math.sin(t * v + ph) + dx
        cy = y + 110 * math.cos(t * v * 0.8 + ph)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(col, a * gain), hexa(col, 0.0)]))
        c.drawCircle(cx, cy, r, p)


def fond_agence(c, t, pulse=0.0):
    """noir violet, taches de lumière qui dérivent, trame de points très discrète, vignette"""
    c.clear(hexa(A["fond"]))
    _taches(c, t, 1.0 + 0.35 * pulse)
    p = peinture("#FFFFFF", 0.045)
    dy = (t * 14) % 60
    for y in range(-60, H + 60, 60):
        for x in range(30, W, 60):
            c.drawCircle(x, y + 30 - dy, 1.8, p)
    poussieres(c, t)
    v = skia.Paint(AntiAlias=True)
    v.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.72, [hexa("#000000", 0.0), hexa("#000000", 0.55)], [0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), v)


_RNG = np.random.default_rng(11)
_POUSS = [(_RNG.uniform(0, W), _RNG.uniform(0, H), _RNG.uniform(1.2, 3.2), _RNG.uniform(20, 70), _RNG.uniform(0, 6.3)) for _ in range(70)]


def poussieres(c, t):
    """particules de lumière qui montent et scintillent"""
    for x, y, r, v, ph in _POUSS:
        yy = (y - t * v) % (H + 40) - 20
        a = 0.25 + 0.35 * (0.5 + 0.5 * math.sin(t * 2.2 + ph))
        disque(c, x + 14 * math.sin(t * 0.7 + ph), yy, r, A["poussiere"], a)


def theme_athla():
    """jaune-vert ATHLA (#C8FF2E) sur noir #0A0B0D, texte noir sur l'accent"""
    A.update(fond="#060705", violet="#C8FF2E", violetClair="#D9FF6B", violetPale="#EEF7D0", surAccent="#0A0B0D",
             poussiere="#E4FF9A", verreFond="#10130A", disque=("#E4FF7A", "#C8FF2E", "#9BCC12"), bouton=("#D9FF6B", "#B5EB1A"),
             logoDisque="logo-agence-noir", gris="#9AA391")
    TACHES[:] = [(140, 380, 760, "#5C7A0E", 0.32, 0.23, 0.0), (980, 1560, 820, "#3A4D08", 0.36, 0.17, 1.7),
                 (860, 200, 560, "#C8FF2E", 0.10, 0.29, 3.1), (80, 1760, 600, "#1E2808", 0.45, 0.21, 4.4)]


# ─────────────────────────────────────────── verre dépoli
T_COURANT = [0.0]     # temps courant : le verre redessine le fond derrière lui


def verre(c, x, y, w, h, r=36, teinte=0.08, lisere=0.34, ombre=0.5, violet=0.0):
    """carte de verre : le fond flouté derrière (taches sans trame), voile clair, reflet, liseré dégradé"""
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    if ombre > 0:
        p = skia.Paint(AntiAlias=True, Color=hexa("#000000", ombre), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 34))
        c.save(); c.translate(0, 26); c.drawRRect(rr, p); c.restore()
    c.save(); c.clipRRect(rr, doAntiAlias=True)
    c.save(); c.resetMatrix()
    c.drawRect(skia.Rect.MakeWH(W, H), peinture(A["verreFond"]))
    _taches(c, T_COURANT[0], 1.25)
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#FFFFFF", teinte))
    if violet > 0: c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(A["violet"], violet))
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.45, y + h)],
                                               [hexa("#FFFFFF", 0.14), hexa("#FFFFFF", 0.02), hexa("#FFFFFF", 0.0)], [0.0, 0.5, 1.0]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), g)
    c.restore()
    bp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0)
    bp.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.3, y + h)],
                                                [hexa("#FFFFFF", lisere), hexa("#FFFFFF", lisere * 0.25)], [0.0, 1.0]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 1, y + 1, w - 2, h - 2), r - 1, r - 1), bp)


def lueur(c, cx, cy, r, couleur=None, a=0.5):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(couleur or A["violet"], a), hexa(couleur or A["violet"], 0.0)]))
    c.drawCircle(cx, cy, r, p)


def pastille_verre(c, label, cx, cy, taille=34, icone_=None, alpha=1.0, s=1.0, accent=None, rot=0.0, fam="gras"):
    """pastille de verre : icône dans un disque violet + libellé blanc"""
    if alpha <= 0.01 or s <= 0.01: return
    tw = largeur(label, taille, fam, -0.01)
    h = taille * 2.15; ic = h - 22 if icone_ else 0
    w = tw + (ic + 16 + 14 if icone_ else 2 * taille * 0.8) + taille * 0.8
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        verre(c, -w / 2, -h / 2, w, h, h / 2, 0.08, ombre=0.4)
        x = -w / 2 + (11 if icone_ else taille * 0.8)
        if icone_:
            disque(c, x + ic / 2, 0, ic / 2, accent or A["violet"])
            icone(c, icone_, x + ic / 2, 0, ic * 0.55, A["surAccent"] if not accent else "#FFFFFF", 2.4)
            x += ic + 16
        texte(c, label, x, -hauteurLigne(taille, fam) / 2, taille, "#FFFFFF", fam, track=-0.01)
    c.restore()
    return w


def texte_flou(c, s, x, y, taille, couleur="#FFFFFF", fam="gras", align="gauche", track=-0.02, alpha=1.0, flou=0.0):
    if alpha <= 0.01: return
    if flou > 0.3:
        p = skia.Paint(ImageFilter=skia.ImageFilters.Blur(flou, flou)); p.setAlphaf(borne(alpha))
        c.saveLayer(None, p)
        texte(c, s, x, y, taille, couleur, fam, align, track)
        c.restore()
    else:
        texte(c, s, x, y, taille, couleur, fam, align, track, alpha)


# ─────────────────────────────────────────── sous-titres fins
class SousTitresFins:
    """phrase en cours, blanc, mot par mot (flou → net), sans surlignage ; fusions : {(i, j…): "affichage"}"""

    def __init__(self, kit, fusions=None, y=300, larg=900, taille=64, fam="gras", max_mots=5):
        mots = kit.mots
        fusions = fusions or {}
        prem = {k[0]: (k, v) for k, v in fusions.items()}
        jet = []           # (texte, t0, fin_de_phrase)
        i = 0
        while i < len(mots):
            if i in prem:
                k, v = prem[i]
                jet.append([v, mots[k[0]]["t0"], bool(re.search(r"[.?!:]$", mots[k[-1]]["w"]))]); i = k[-1] + 1
            else:
                w = mots[i]["w"]
                jet.append([w, mots[i]["t0"], bool(re.search(r"[.?!:,]$", w))]); i += 1
        self.blocs, cur = [], []
        for tok in jet:
            cur.append(tok)
            if tok[2] or len(cur) >= max_mots:
                self.blocs.append(cur); cur = []
        if cur: self.blocs.append(cur)
        # une virgule seule ne coupe pas un bloc de moins de 3 mots : on recolle
        fus = []
        for b in self.blocs:
            if fus and len(fus[-1]) < 3 and fus[-1][-1][0].endswith(",") and len(fus[-1]) + len(b) <= max_mots + 1:
                fus[-1] = fus[-1] + b
            else:
                fus.append(b)
        self.blocs = fus
        self.y, self.larg, self.taille, self.fam = y, larg, taille, fam
        self.mise = [self._mise(b) for b in self.blocs]

    def _mise(self, bloc):
        T, fam = self.taille, self.fam
        esp = largeur("a a", T, fam) - largeur("aa", T, fam)
        lignes, cur, lw = [], [], 0
        for txt, t0, _ in bloc:
            w = largeur(txt, T, fam, -0.02)
            if cur and lw + esp + w > self.larg:
                lignes.append((cur, lw)); cur, lw = [], 0
            cur.append((txt, t0, w)); lw += (esp if len(cur) > 1 else 0) + w
        lignes.append((cur, lw))
        pos = []
        hl = hauteurLigne(T, fam) * 1.04
        for k, (ligne, lw) in enumerate(lignes):
            x = 540 - lw / 2
            for txt, t0, w in ligne:
                pos.append((txt, t0, x, self.y + k * hl)); x += w + esp
        return pos

    def dessine(self, c, t, couleur="#FFFFFF"):
        for k, pos in enumerate(self.mise):
            t_deb = pos[0][1] - 0.05
            t_fin = self.mise[k + 1][0][1] - 0.05 if k + 1 < len(self.mise) else 1e9
            if t < t_deb or t > t_fin + 0.2: continue
            o = prog(t, t_fin, 0.18, entree)
            for txt, t0, x, y in pos:
                u = 1.0 if t0 <= 0.05 else prog(t, t0 - 0.05, 0.24, sortie)
                if u <= 0: continue
                texte_flou(c, txt, x, y + mix(22, 0, u) - 26 * o, self.taille, couleur, self.fam,
                           alpha=u * (1 - o), flou=mix(10, 0, u) + 10 * o)


# ─────────────────────────────────────────── téléphone sombre
def telephone_sombre(c, cx, cy, w, h, ecran=None, alpha=1.0, fond_ecran="#000000"):
    x, y = cx - w / 2, cy - h / 2
    k = w / 480
    with Calque(c, alpha):
        p = skia.Paint(AntiAlias=True, Color=hexa("#000000", 0.55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y + 40, w, h), 74 * k, 74 * k), p)
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w, y + h)], [hexa("#4A4658"), hexa("#16141D"), hexa("#3A3647")], [0, 0.55, 1]))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 74 * k, 74 * k), g)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 6 * k, y + 6 * k, w - 12 * k, h - 12 * k), 68 * k, 68 * k), peinture("#050408"))
        ex, ey, ew, eh = x + 14 * k, y + 14 * k, w - 28 * k, h - 28 * k
        c.save()
        c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(ex, ey, ew, eh), 60 * k, 60 * k), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(ex, ey, ew, eh), peinture(fond_ecran))
        if ecran: ecran(c, ex, ey, ew, eh)
        # reflet en biais sur la vitre
        rf = skia.Paint(AntiAlias=True)
        rf.setShader(skia.GradientShader.MakeLinear([skia.Point(ex, ey), skia.Point(ex + ew, ey + eh * 0.6)],
                                                    [hexa("#FFFFFF", 0.0), hexa("#FFFFFF", 0.07), hexa("#FFFFFF", 0.0)], [0.3, 0.42, 0.55]))
        c.drawRect(skia.Rect.MakeXYWH(ex, ey, ew, eh), rf)
        c.restore()
        rrect(c, cx - 62 * k, y + 30 * k, 124 * k, 34 * k, 17 * k, "#000000")


# ─────────────────────────────────────────── logo et fin
def logo_agence(c, cx, cy, w, alpha=1.0, blanc=False):
    nom = "logo-agence-blanc" if blanc else "logo-agence"
    iw, ih = taille_img(nom); h = w * ih / iw
    image(c, nom, cx - w / 2, cy - h / 2, w, alpha)


def disque_logo(c, t, t0, t1, cx=540, cy=980):
    """disque violet qui remplit l'écran, logo blanc qui claque ; renvoie le rayon"""
    r = cles(t, [(t0, 0), (t0 + 0.3, 1800, entree), (t1, 1800), (t1 + 0.32, 0, entreeSortie)])
    if r > 1:
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), max(r, 2), [hexa(k) for k in A["disque"]], [0, 0.55, 1]))
        c.drawCircle(cx, cy, r, g)
        if t0 + 0.2 <= t <= t1 + 0.12:
            u = prog(t, t0 + 0.24, 0.32, lambda v: rebond(v, 1.5)); so = prog(t, t1 - 0.12, 0.24, entree)
            iw, ih = taille_img(A["logoDisque"]); lw = mix(1.4, 1, u) * 820 * (1 - 0.3 * so)
            image(c, A["logoDisque"], cx - lw / 2, cy - lw * ih / iw / 2, lw, borne(u * 3) * (1 - so))
    return r


def carton_agence(c, t, t0, site="dyou-agency.com", accroche="Des vidéos motion pour ton activité"):
    if t < t0: return
    u = prog(t, t0, 0.45, sortie)
    lueur(c, 540, 900, 700 * u, A["violet"], 0.45)
    ul = prog(t, t0 + 0.06, 0.4, lambda v: rebond(v, 1.5))
    logo_agence(c, 540, 790, 820 * mix(0.6, 1, ul), borne(ul * 2))
    ub = prog(t, t0 + 0.3, 0.42, lambda v: rebond(v, 1.8))
    if ub > 0:
        s = mix(0.4, 1, ub) * (1 + 0.03 * max(0, math.sin((t - t0 - 0.8) * 5)) if t > t0 + 0.8 else 1)
        lab = "Écris-nous"
        T = 46; tw = largeur(lab, T, "noir"); hb = 124; wb = tw + hb + 70
        c.save(); c.translate(540, 1080); c.scale(s, s)
        with Calque(c, borne(ub * 2)):
            lueur(c, 0, 0, wb * 0.75, A["violet"], 0.5)
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeLinear([skia.Point(-wb / 2, -hb / 2), skia.Point(wb / 2, hb / 2)], [hexa(A["bouton"][0]), hexa(A["bouton"][1])]))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-wb / 2, -hb / 2, wb, hb), hb / 2, hb / 2), g)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-wb / 2 + 1, -hb / 2 + 1, wb - 2, hb - 2), hb / 2, hb / 2),
                        peinture("#FFFFFF", 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
            icone(c, "message-circle", -wb / 2 + hb / 2 + 8, 0, 54, A["surAccent"], 2.4)
            texte(c, lab, -wb / 2 + hb + 10, -hauteurLigne(T) / 2, T, A["surAccent"], "noir")
        c.restore()
    ud = prog(t, t0 + 0.5, 0.4, sortie)
    texte(c, site, 540, 1200 + mix(16, 0, ud), 36, A["violetPale"], "demi", "centre", 0.02, ud)
    ut = prog(t, t0 + 0.18, 0.4, sortie)
    texte(c, accroche, 540, 940 + mix(16, 0, ut), 40, "#FFFFFF", "demi", "centre", -0.01, 0.9 * ut)
