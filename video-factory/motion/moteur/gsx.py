"""Briques GSX — Global SINO Export (19/10/2026), deuxième société du client MONARQUE.

Même grammaire que MONARQUE (fond blanc cassé, Archivo Black, voix Tomy, sous-titres encre) + les éléments de DY-M15
(cartes en verre qui sortent en 3D, produits/plans qui jaillissent, signature explosive) passés EN CLAIR :
`verre_clair()` = verre givré blanc (ombre douce, reflet, liseré, lueur rouge GSX au pied) au lieu du verre fumé sombre.
Accent = rouge du logo #E8072D. Le logo est découpé en sigle (globe) et mot (Global SINO Export) dans media/.

    from gsx import *
    polices(P)
"""
import math
import numpy as np
import skia
import moteur
from moteur import *
from studio import eclats, rayons, lueur_s, entre, lettres
from studio3d import Cam, Plan, coins, scene3d, rot3
from monarque import polices, fond_clair, PAPIER, ENCRE, GRIS, BLANC, VERT

ROUGE = "#E8072D"           # rouge du logo GSX
ROUGE2 = "#FF5A6E"
GLACE = "#C9D6EA"           # liseré bleu-gris du verre clair
CN, FR = (113.26, 23.13), (2.35, 48.86)


# ─────────────────────────────────────────── le verre clair (verre givré blanc)
def verre_clair(c, x, y, w, h, r=34, alpha=1.0, lueur=1.0, accent=ROUGE, ombre=1.0):
    if alpha <= 0.003 or w <= 1 or h <= 1: return
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    k = max(0.4, min(w, h) / 300)
    with Calque(c, alpha):
        if ombre > 0:
            p = skia.Paint(AntiAlias=True, Color=hexa("#2A3550", 0.20 * ombre), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26 * k))
            c.save(); c.translate(0, 22 * k); c.drawRRect(rr, p); c.restore()
        if lueur > 0:
            p = skia.Paint(AntiAlias=True, Color=hexa(accent, 0.16 * lueur), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 18 * k))
            c.drawRRect(rr, p)
        c.drawRRect(rr, pgrad_(x, y, x + w * 0.5, y + h, ["#FFFFFF", "#F4F6FA", "#E9EDF4"], 0.86))
        c.save(); c.clipRRect(rr, doAntiAlias=True)
        rf = skia.Paint(AntiAlias=True)
        rf.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.5, y + h * 0.5)],
                                                    [hexa("#FFFFFF", 0.0), hexa("#FFFFFF", 0.9), hexa("#FFFFFF", 0.0)], [0.28, 0.35, 0.46]))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), rf)
        if lueur > 0:
            lb = skia.Paint(AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12 * k))
            lb.setShader(skia.GradientShader.MakeRadial(skia.Point(x + w / 2, y + h), w * 0.55, [hexa(accent, 0.20 * lueur), hexa(accent, 0.0)]))
            c.drawRect(skia.Rect.MakeXYWH(x, y + h - 70 * k, w, 70 * k), lb)
        c.restore()
        ep = max(1.5, 2.4 * k)
        li = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=ep)
        li.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w, y + h)],
                                                    [hexa("#FFFFFF", 1.0), hexa(GLACE, 0.55), hexa("#FFFFFF", 0.9), hexa(GLACE, 0.9)],
                                                    [0.0, 0.4, 0.7, 1.0]))
        c.drawRRect(rr, li)


def pgrad_(x0, y0, x1, y1, cols, alpha=1.0):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [hexa(col, alpha) for col in cols]))
    return p


def balayage(c, x, y, w, h, t, r=30, vitesse=0.45, a=0.55):
    """reflet blanc qui traverse la vitre"""
    u = (t * vitesse) % 1.6 - 0.3
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), doAntiAlias=True)
    p = skia.Paint(AntiAlias=True)
    x0 = x + w * u
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0 - 140, y), skia.Point(x0 + 140, y + 200)],
                                               [hexa("#FFFFFF", 0), hexa("#FFFFFF", a), hexa("#FFFFFF", 0)]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)
    c.restore()


def pill_v(c, label, cx, cy, a, ic=None, accent=ROUGE, taille=32, rot=0.0, plein=False):
    """pastille en verre clair (texte encre, icône accent) ou pleine (fond accent, texte blanc) ; a = progression à rebond"""
    if a <= 0.01: return 0
    tw = largeur(label, taille, "titre", -0.01)
    h = taille * 2.0; ic_w = taille * 1.1 if ic else 0
    w = tw + ic_w + (taille * 0.4 if ic else 0) + taille * 1.5
    c.save(); c.translate(cx, cy); c.rotate(rot); s = mix(0.35, 1, a); c.scale(s, s)
    with Calque(c, borne(a * 2.5)):
        if plein:
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
            p = skia.Paint(AntiAlias=True, Color=hexa(accent, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, taille * 0.5))
            c.save(); c.translate(0, taille * 0.3); c.drawRRect(rr, p); c.restore()
            c.drawRRect(rr, peinture(accent))
            c.drawRRect(rr, peinture("#FFFFFF", 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        else:
            verre_clair(c, -w / 2, -h / 2, w, h, h / 2, 1.0, 0.8, accent, 0.8)
        x = -w / 2 + taille * 0.75
        if ic:
            icone(c, ic, x + ic_w / 2, 0, ic_w, BLANC if plein else accent, 2.6); x += ic_w + taille * 0.4
        texte(c, label, x, -hauteurLigne(taille, "titre") / 2, taille, BLANC if plein else ENCRE, "titre", track=-0.01)
    c.restore()
    return w


def titre2(c, t, l1, l2, t0, t1, y=330, t2=None, e1="masque", e2="ressort", c2=ENCRE, larg=780, cx=540, grand=108):
    """titre éditorial (petite ligne grise + grande ligne Archivo) ; la grande ligne passe sur deux lignes plutôt que
    de rapetisser sous 84 px ; zone sûre : 780 px de large"""
    if t < t0 - 0.1 or t > t1 + 0.12: return
    a = 1 - prog(t, t1 - 0.18, 0.15, entree)
    if l1:
        lettres(c, l1, cx, y, ajuste(l1, larg, 50, "titre", -0.02), t, t0 - 0.05, e1, fam="titre", grad=False, couleur=GRIS,
                decal=0.022, duree=0.32, alpha=a, track=-0.02)
    if l2:
        lignes = [l2]
        if ajuste(l2, larg, grand, "archivo", -0.02) < 84 and " " in l2:
            mots = l2.split(" ")
            k = min(range(1, len(mots)), key=lambda i: abs(len(" ".join(mots[:i])) - len(" ".join(mots[i:]))))
            lignes = [" ".join(mots[:k]), " ".join(mots[k:])]
        taille = min(ajuste(l, larg, grand, "archivo", -0.02) for l in lignes)
        for j, l in enumerate(lignes):
            lettres(c, l, cx, y + 62 + j * taille * 1.02, taille, t, (t2 if t2 is not None else t0 + 0.1) - 0.05 + 0.08 * j, e2,
                    fam="archivo", grad=False, couleur=c2, decal=0.026, alpha=a, track=-0.02)


def coche_v(c, cx, cy, r, a, couleur=VERT):
    if a <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(a, a)
    disque(c, 0, 0, r, couleur, 1, (8, 20, 0.25)); icone(c, "check", 0, 0, r * 1.1, BLANC, 3.2)
    c.restore()


def croix_v(c, cx, cy, r, a, couleur=ROUGE):
    if a <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(a, a)
    disque(c, 0, 0, r, couleur, 1, (8, 20, 0.25)); icone(c, "x", 0, 0, r * 1.1, BLANC, 3.2)
    c.restore()


# ─────────────────────────────────────────── logo
def logo_gsx(c, cx, cy, w, alpha=1.0, blanc=False):
    if alpha <= 0.01: return
    nom = "logo-gsx-blanc" if blanc else "logo-gsx"
    iw, ih = taille_img(nom); image(c, nom, cx - w / 2, cy - w * ih / iw / 2, w, alpha)


# ─────────────────────────────────────────── globe en points, Chine allumée en rouge
_G = []


def globe(c, lon0, lat0, cx, cy, R, lum=1.0, alpha=1.0, france=True):
    if not _G:
        from kit import Globe
        _G.append(Globe())
    G = _G[0]
    with Calque(c, alpha):
        ombre_sol(c, cx, cy + R * 1.06, R * 0.78, R * 0.09, 0.14)
        if lum > 0:
            kx, ky, kz = G.pos(*CN, lon0, lat0, R, cx, cy)
            if kz > 0:
                p = skia.Paint(AntiAlias=True)
                p.setShader(skia.GradientShader.MakeRadial(skia.Point(kx, ky), R * 0.8, [hexa(ROUGE, 0.22 * lum), hexa(ROUGE, 0.0)]))
                c.drawCircle(kx, ky, R * 0.8, p)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx - R * 0.3, cy - R * 0.35), R * 1.5, [hexa("#FFFFFF"), hexa("#ECEEF2")], [0.0, 1.0]))
        c.drawCircle(cx, cy, R, p); anneau(c, cx, cy, R, "#D8DCE3", 3)
        terre = "#BCC2CC"
        G.terres(c, cx, cy, R, lon0, lat0, couleurs={0: terre, 1: _melange(terre, ROUGE, lum), 2: terre, 3: ENCRE if france else terre, 4: terre},
                 grossir={1: mix(1.0, 1.35, lum), 2: 0.6, 3: 1.0})
    return G


def _melange(c1, c2, u):
    a, b = hexa(c1), hexa(c2); u = borne(u)
    f = lambda s: int(round(((a >> s) & 255) * (1 - u) + ((b >> s) & 255) * u))
    return "#%02X%02X%02X" % (f(16), f(8), f(0))


# ─────────────────────────────────────────── signature de fin GSX (version claire de moteur/signature.py)
T_BOUM = 0.5


def _objet(c, nom, video_, x, y, w, alpha, rot, t):
    """carte dessinée à taille fixe 200 × 300 puis mise à l'échelle (une seule taille de cache vidéo)"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(w / 200, w / 200)
    with Calque(c, alpha):
        verre_clair(c, -106, -156, 212, 312, 28, 1.0, 0.5, ROUGE, 0.6)
        if video_: video(c, nom, -100, -150, 200, 300, t, 1.0, rayon=22)
        else: image_cover(c, nom, -100, -150, 200, 300, 1.0, 0.5, 0.5, 22)
    c.restore()


def _balayage_png(c, w, h, u):
    if not (0 < u < 1): return
    x = mix(-160, w + 160, u)
    p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kSrcATop)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x - 110, 0), skia.Point(x + 110, 0)],
                                               [hexa("#FFFFFF", 0), hexa("#FFFFFF", 0.85), hexa("#FFFFFF", 0)], [0.0, 0.5, 1.0]))
    c.drawRect(skia.Rect.MakeWH(w, h), p)


def signature_gsx(c, t, t0, medias, lignes, cx=510, cy=760):
    """medias : [(nom, est_video)] aspirés au centre → explosion (verre, ondes rouges) → sigle-globe extrudé qui tourne et
    claque → « Global SINO Export » recomposé en tranches 3D → lignes [(texte, t, taille, couleur)] posées au mot"""
    u = t - t0
    if u < -0.05: return
    rng, rng2 = np.random.default_rng(7), np.random.default_rng(8)
    boum = t0 + T_BOUM
    sx, sy = secousse(t, boum, 24, 0.45)
    c.save(); c.translate(sx, sy)
    n = len(medias)
    for k, (nom, vid) in enumerate(medias):
        d0 = 0.04 * k
        v = borne((u - d0) / (T_BOUM - d0 - 0.02))
        if v <= 0 or v >= 1: continue
        a = k / n * 2 * math.pi + 0.4
        for g in (2, 1, 0):
            vg = max(0.0, v - 0.09 * g)
            r = 720 * (1 - vg ** 2.2)
            _objet(c, nom, vid, cx + r * math.cos(a), cy + r * math.sin(a) * 1.25, mix(260, 40, vg ** 2.2),
                   (0.18 if g else 1.0) * borne(v * 5), 300 * vg * (1 if k % 2 else -1), t)
    nv = prog(t, t0 + 0.2, T_BOUM - 0.2, entree) * (1 - prog(t, boum, 0.25))
    if nv > 0:
        lueur_s(c, cx, cy, 80 + 260 * nv, ROUGE, 0.5 * nv)
        disque(c, cx, cy, 10 + 40 * nv, ROUGE, nv)
    if u >= T_BOUM - 0.02:
        fl = 1 - (t - boum) / 0.22
        if 0 < fl <= 1: c.drawRect(skia.Rect.MakeXYWH(-100, -100, 1280, 2120), peinture("#FFFFFF", 0.7 * fl * fl))
        onde(c, cx, cy, t, boum, 40, 1150, ROUGE, 14, 0.7)
        onde(c, cx, cy, t, boum + 0.08, 30, 800, ENCRE, 6, 0.7)
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
                c.drawPath(pa, peinture("#DCE3EE", 0.55 * al))
                c.drawPath(pa, peinture(ROUGE if k % 3 == 0 else "#9AA8BF", 0.9 * al, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2))
        eclats(c, cx, cy, t, boum, 20, 620, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=21, duree=0.9)
        eclats(c, cx, cy, t, boum + 0.1, 14, 380, cols=[ROUGE, GRIS], graine=22, duree=0.8)
    if u >= T_BOUM:
        e = t - boum
        a = borne(e / 0.4)
        lueur_s(c, cx, cy - 60, 560, ROUGE, 0.10 * a)
        ou = prog(t, boum + 0.05, 1.2, douce)
        cam = Cam(ax=-10 + 4 * math.sin(t * 1.3), ay=mix(-28, 8, ou) + 5 * math.sin(t * 0.9), tz=mix(380, 0, ou), cx=cx, cy=cy)
        plans = []
        ann = prog(t, boum + 0.35, 0.6, sortie)
        if ann > 0:                                  # anneau des plans de la vidéo, derrière le logo
            for k, (nom, vid) in enumerate(medias):
                ang = t * 0.8 + k * 2 * math.pi / n
                R = mix(200, 420, ann)
                pos = (R * math.cos(ang), -40 + 60 * math.sin(ang * 2), 300 + 230 * math.sin(ang))
                w_, h_ = 150.0, 225.0
                def dess(cc, w, h, nom=nom, vid=vid):
                    verre_clair(cc, 0, 0, w, h, w * 0.12, 1.0, 0.4, ROUGE, 0.5)
                    m = w * 0.05
                    if vid: video(cc, nom, m, m, w - 2 * m, h - 2 * m, t, 1.0, rayon=w * 0.09)
                    else: image_cover(cc, nom, m, m, w - 2 * m, h - 2 * m, 1.0, 0.5, 0.5, w * 0.09)
                cache = 1 - 0.65 * borne(1 - abs(pos[0]) / 260)
                plans.append(Plan(coins(pos, w_, h_, ay=-math.degrees(ang) + 90), w_, h_, dess, 0.8 * ann * cache, recto=False))
        # sigle-globe extrudé : couches empilées, il fait un tour et claque
        iw, ih = taille_img("sigle-gsx"); SW = 300.0; SH = SW * ih / iw
        sg = prog(t, boum, 0.75, lambda v: ressort(v, 1.2, 5.0))
        if sg > 0:
            tour = mix(340, 0, min(sg, 1.08)); s_ = mix(0.2, 1, min(sg, 1.1))
            for k in range(12, -1, -1):
                tint = mix(0.45, 0.85, k / 12)
                def couche(cc, w, h, k=k, tint=tint):
                    p = skia.Paint(AntiAlias=True)
                    if k > 0: p.setColorFilter(skia.ColorFilters.Blend(skia.Color4f(0.55 * tint, 0.02, 0.10, 1).toColor(), skia.BlendMode.kSrcIn))
                    cc.saveLayer(None)
                    i = moteur._img("sigle-gsx")
                    cc.drawImageRect(i, skia.Rect.MakeWH(w, h), moteur._ECH, p)
                    if k == 0: _balayage_png(cc, w, h, prog(t, boum + 1.05, 0.55, douce))
                    cc.restore()
                ctr = rot3((0, 0, 3.4 * k * s_), 0, tour, 0)
                plans.append(Plan(coins((ctr[0], -150 + ctr[1], ctr[2]), SW * s_, SH * s_, ay=tour), SW * s_, SH * s_, couche, borne(sg * 4), recto=False))
        # « Global SINO Export » sur une ligne : 3 mots en tranches qui volent et se recomposent
        MW = 700.0; mots = ["Global", "SINO", "Export"]
        taille = 88; esp = 22
        ws = [largeur(m, taille, "gras", -0.03) for m in mots]
        tot = sum(ws) + esp * 2; k_ = MW / tot if tot > MW else 1.0
        x = -tot * k_ / 2
        for j, (m, wm) in enumerate(zip(mots, ws)):
            d = prog(t, boum + 0.22 + 0.09 * j, 0.55, lambda v: ressort(v, 1.15, 5.2))
            ww = wm * k_; hh = hauteurLigne(taille, "gras") * k_
            if d > 0:
                dep = (rng2.uniform(-900, 900), rng2.uniform(-1100, 1100), rng2.uniform(-1300, 900)); rr = rng2.uniform(-260, 260, 3)
                q = min(d, 1.06)
                pos = (mix(dep[0], x + ww / 2, q), mix(dep[1], 110, q), mix(dep[2], 0, q))
                def mot(cc, w, h, m=m):
                    cc.saveLayer(None)
                    texte(cc, m, 0, 0, taille * k_, ROUGE if m == "SINO" else ENCRE, "gras", track=-0.03)
                    _balayage_png(cc, w, h, prog(t, boum + 1.2, 0.7, douce))
                    cc.restore()
                plans.append(Plan(coins(pos, ww + 4, hh, ax=rr[0] * (1 - q), ay=rr[1] * (1 - q), az=rr[2] * (1 - q)), ww + 4, hh, mot, borne(d * 4), recto=False))
            else:
                rng2.uniform(size=6)
            x += ww + esp * k_
        scene3d(c, cam, plans)
        # lignes de marque au mot
        y = cy + 250
        for txt, tl, tai, col in lignes:
            b = prog(t, tl - 0.05, 0.4, sortie)
            morceaux = [txt]
            if largeur(txt, tai, "titre", -0.02) > 780 and " " in txt:          # phrase longue : deux lignes plutôt qu'un texte minuscule
                m = txt.split(" ")
                k = min(range(1, len(m)), key=lambda i: abs(len(" ".join(m[:i])) - len(" ".join(m[i:]))))
                morceaux = [" ".join(m[:k]), " ".join(m[k:])]
            for mo in morceaux:
                if b > 0:
                    texte(c, mo, cx, y + 22 * (1 - b), ajuste(mo, 780, tai, "titre", -0.02), col, "titre", "centre", -0.02, b)
                y += tai * 1.2
            y += tai * 0.2
        b = prog(t, boum + 0.9, 0.45, sortie)
        if b > 0:
            lw = 220 * b; rrect(c, cx - lw / 2, cy + 215, lw, 5, 2.5, ROUGE, b)
    c.restore()


def sons_signature(son, t0):
    son(t0, "montee", -9); son(t0 + 0.05, "whoosh_long", -9)
    son(t0 + T_BOUM, "impact", -4); son(t0 + T_BOUM + 0.02, "whoosh_bas", -6); son(t0 + T_BOUM + 0.05, "verre", -8)
    for k in range(3): son(t0 + T_BOUM + 0.22 + 0.09 * k + 0.4, "pop", -13)
    son(t0 + T_BOUM + 0.7, "impact_doux", -9)
    son(t0 + T_BOUM + 1.15, "ching", -9); son(t0 + T_BOUM + 0.9, "whoosh_court", -13)


# ─────────────────────────────────────────── briques communes des films GSX (GSX-M02 et suivants)
from kit import tampon
T_COURANT = [0.0]          # à mettre à jour au début de dessine() : T_COURANT[0] = t


def tuile_v(c, ic, cx, cy, taille, accent=ROUGE):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - taille / 2, cy - taille / 2, taille, taille), taille * 0.28, taille * 0.28)
    p = skia.Paint(AntiAlias=True, Color=hexa(accent, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, taille * 0.12))
    c.save(); c.translate(0, taille * 0.08); c.drawRRect(rr, p); c.restore()
    fonce = {ROUGE: "#A80020", VERT: "#0E7A44", ENCRE: "#000000"}.get(accent, "#6D7380")
    c.drawRRect(rr, pgrad_(cx - taille / 2, cy - taille / 2, cx + taille / 2, cy + taille / 2, [accent, fonce]))
    icone(c, ic, cx, cy, taille * 0.52, BLANC, 2.6)


def carte_rush(nom, t0, vitesse=1.0, label=None, ic=None, accent=ROUGE, plein=True):
    """une vraie vidéo du client dans une carte de verre clair (plan entier, jamais ralentie) ; à plaquer sur un Plan"""
    def f(c, w, h):
        t = T_COURANT[0]
        verre_clair(c, 0, 0, w, h, w * 0.08)
        m = w * 0.045
        video(c, nom, m, m, w - 2 * m, h - 2 * m, t - t0, vitesse, True, rayon=w * 0.055)
        balayage(c, 0, 0, w, h, t, w * 0.08, 0.4, 0.35)
        if label:
            pill_v(c, label, w / 2, h - m - w * 0.12, 1.0, ic, accent, taille=max(20, w * 0.068), plein=plein)
    return f


def carte_ic(ic, lab, sous=None, accent=ROUGE, gris=0.0):
    """carte de verre : tuile d'icône + titre (+ sous-titre)"""
    def f(c, w, h):
        verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 1 - gris, accent)
        tuile_v(c, ic, w / 2, h * 0.36, w * 0.42, accent if not gris else "#A9AFBA")
        lw = ajuste(lab, w * 0.84, w * 0.13, "archivo", -0.02)
        texte(c, lab, w / 2, h * 0.62, lw, ENCRE if not gris else "#9AA0AA", "archivo", "centre", -0.02)
        if sous: texte(c, sous, w / 2, h * 0.62 + lw * 1.3, ajuste(sous, w * 0.84, w * 0.075, "demi", 0), GRIS, "demi", "centre", 0)
        balayage(c, 0, 0, w, h, T_COURANT[0], w * 0.1, 0.4, 0.4)
    return f


def rangee(c, t, x, y, w, ic, lab, t0, etat=None, t_etat=None, accent=ROUGE, h=140):
    """ligne de liste en verre qui glisse en place ; etat = "ok" (coche verte), "ko" (croix rouge), "?" (inconnu qui clignote)"""
    u = entre(t, t0 - 0.12, 0.45, 1.8)
    if u <= 0: return
    c.save(); c.translate(x + 380 * (1 - min(u, 1)), y); c.rotate(-4 * (1 - min(u, 1)))
    with Calque(c, borne(u * 3)):
        verre_clair(c, -w / 2, -h / 2, w, h, 40, 1.0, 0.8, accent)
        tuile_v(c, ic, -w / 2 + 74, 0, h * 0.68, accent)
        texte(c, lab, -w / 2 + 140, -hauteurLigne(38, "archivo") / 2, ajuste(lab, w - 250, 38, "archivo", -0.02), ENCRE, "archivo", track=-0.02)
        if etat and t_etat is not None:
            e = entre(t, t_etat, 0.35, 2.4)
            if etat == "ok": coche_v(c, w / 2 - 56, 0, 30, e)
            elif etat == "ko": croix_v(c, w / 2 - 56, 0, 30, e)
            elif e > 0:
                disque(c, w / 2 - 56, 0, 30 * min(e, 1.1), "#C4CAD4"); texte(c, "?", w / 2 - 56, -hauteurLigne(38, "archivo") / 2, 38, BLANC, "archivo", "centre", 0,
                                                                          0.6 + 0.4 * math.sin(t * 7))
        balayage(c, -w / 2, -h / 2, w, h, t + y * 0.01, 40, 0.5, 0.4)
    c.restore()


def disque_gsx(c, t, t_debut, t_gsx, t_fin, cx=510, cy=1000, avant=None):
    """disque noir qui couvre tout, logo GSX qui claque au mot « GSX », puis tout se rouvre ; renvoie le rayon"""
    r = cles(t, [(t_debut - 0.1, 0), (t_debut + 0.25, 2200, entree), (t_fin - 0.15, 2200), (t_fin + 0.2, 0, entreeSortie)])
    if r <= 1: return 0
    disque(c, cx, cy, r, ENCRE)
    u = entre(t, t_gsx - 0.12, 0.55, 1.8)
    if u > 0:
        sx, sy = secousse(t, t_gsx, 16, 0.3)
        so = prog(t, t_fin - 0.2, 0.3, entree)
        lueur_s(c, cx, 960, 520, ROUGE, 0.25 * borne(u * 2) * (1 - so))
        logo_gsx(c, cx + sx, mix(960, 300, so) + sy, 720 * mix(0.4, 1, u) * mix(1, 0.4, so), borne(u * 3), blanc=True)
        onde(c, cx, 960, t, t_gsx + 0.05, 100, 760, ROUGE, 12, 0.6)
        eclats(c, cx, 960, t, t_gsx + 0.05, 16, 560, cols=[ROUGE, BLANC, "#9AA8BF"], graine=9)
    if avant: titre2(c, t, avant, None, t_debut, t_gsx - 0.1, y=860)
    return r


def entete(c, t, t_on, t_off):
    a = prog(t, t_on, 0.3, sortie) * (1 - prog(t, t_off - 0.15, 0.25))
    if a > 0: logo_gsx(c, 540, 240, 210, a)


def lien(c, t, xa, xb, y, t0, t_sigle=None, casse=None):
    """trait rouge tendu entre deux cartes ; sigle GSX au milieu ; casse = instant où le lien se rompt"""
    v = prog(t, t0, 0.6, entreeSortie)
    if v <= 0: return
    pe = peinture(ROUGE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=8); pe.setStrokeCap(skia.Paint.kRound_Cap)
    pe.setPathEffect(skia.DashPathEffect.Make([18, 12], -t * 80))
    if casse is not None and t > casse:
        k = prog(t, casse, 0.5, sortie); m = (xa + xb) / 2
        c.drawLine(xa, y, m - 30 - 60 * k, y + 40 * k, pe); c.drawLine(m + 30 + 60 * k, y - 40 * k, xb, y, pe)
        for j in range(5):
            a = j * 1.3
            c.drawLine(m, y, m + 40 * k * math.cos(a), y + 40 * k * math.sin(a), peinture(ROUGE, 1 - k, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        return
    c.drawLine(xa, y, mix(xa, xb, v), y, pe)
    if t_sigle is not None:
        s = entre(t, t_sigle, 0.45, 2.2)
        if s > 0:
            m = (xa + xb) / 2
            disque(c, m, y, 70 * s, BLANC, 1, (10, 26, 0.25)); anneau(c, m, y, 70 * s, ROUGE, 4)
            iw, ih = taille_img("sigle-gsx"); image(c, "sigle-gsx", m - 46 * s, y - 46 * s * ih / iw, 92 * s)
            eclats(c, m, y, t, t_sigle + 0.05, 12, 300, cols=[ROUGE, ENCRE], graine=3)


def bouclier(c, t, cx, cy, t0, couleur=ROUGE, marque="?", taille=1.0):
    u = entre(t, t0, 0.45, 2.0)
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(6 * math.sin(t * 2)); s = mix(0.3, 1, u) * taille; c.scale(s, s)
    with Calque(c, borne(u * 3)):
        verre_clair(c, -100, -100, 200, 200, 56, 1.0, 1.0, couleur)
        icone(c, "shield-check", 0, -6, 104, couleur, 2.6)
        if marque:
            disque(c, 68, 66, 32, ENCRE); texte(c, marque, 68, 66 - hauteurLigne(44, "archivo") / 2, 44, BLANC, "archivo", "centre", 0)
    c.restore()
