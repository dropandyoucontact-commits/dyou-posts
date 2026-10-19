"""Signature de fin DROP&YOU (18/10/2026) — remplace « le logo posé dans un cadre » que Youssef trouvait nul.

    from signature import signature, sons_signature
    signature(c, t, T_FIN, PRODUITS)          # dans dessine(), par-dessus tout
    sons_signature(son, T_FIN)                # avec les autres sons

Déroulé (≈ 2,4 s) : les produits de la vidéo sont aspirés au centre en traînées → noyau de lumière → EXPLOSION
(flash, deux ondes, éclats de verre qui volent en 3D vers la caméra, étincelles, secousse) → le sigle DY sort en volume
(extrudé, il fait un tour et claque) → DROP&YOU se recompose en tranches qui arrivent de partout en 3D → reflet qui
balaie le logo, produits en anneau qui tournent derrière, phrase de marque.
PRODUITS : liste de (nom, photo) — photo=False pour un PNG détouré, True pour une photo en situation (coins arrondis).
Zone sûre TikTok / Snap : tout tient entre x 190 et 830 autour de cx=510.
"""
import math
import numpy as np
import skia
from moteur import *
import moteur
from studio import eclats, rayons, lueur_s, entre
from studio3d import Cam, Plan, coins, scene3d, rot3

LOGO_DY = "logo-dy-blanc"     # 900 × 179 : sigle DY (x 0-285) puis DROP&YOU (x 300-900)
SIGLE, MOT = (0, 285), (300, 900)
T_ASP, T_BOUM = 0.0, 0.5      # aspiration, explosion (secondes après t0)


def _crop(c, nom, sx0, sx1, w, h, paint=None):
    i = moteur._img(nom)
    k = i.width() / 900.0
    c.drawImageRect(i, skia.Rect.MakeLTRB(sx0 * k, 0, sx1 * k, i.height()), skia.Rect.MakeWH(w, h), moteur._ECH, paint or skia.Paint(AntiAlias=True))


def _objet(c, nom, photo, x, y, w, alpha=1.0, rot=0.0):
    """un produit centré en (x, y), largeur w"""
    iw, ih = taille_img(nom)
    c.save(); c.translate(x, y); c.rotate(rot)
    if photo:
        h = w * 1.2
        image_cover(c, nom, -w / 2, -h / 2, w, h, 1.0, 0.5, 0.5, w * 0.12, alpha)
    else:
        image(c, nom, -w / 2, -w * ih / iw / 2, w, alpha)
    c.restore()


def _balayage_logo(c, w, h, x0, larg, u):
    """reflet clair qui traverse le logo de gauche à droite (dans le calque du morceau : ne touche que ses pixels) ;
    x0 = position du morceau dans le logo, larg = largeur totale du logo"""
    if not (0 < u < 1): return
    x = mix(-160, larg + 160, u) - x0
    p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kSrcATop)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x - 120, 0), skia.Point(x + 120, 0)],
                                               [hexa("#FFFFFF", 0), hexa("#BFD6FF", 0.95), hexa("#FFFFFF", 0)], [0.0, 0.5, 1.0]))
    c.drawRect(skia.Rect.MakeWH(w, h), p)


def signature(c, t, t0, produits, logo=LOGO_DY, cx=510, cy=880, phrase="Ton équipe sur place, en Chine", accent="#8FB4FF"):
    u = t - t0
    if u < -0.05: return
    rng, rng2 = np.random.default_rng(7), np.random.default_rng(8)
    boum = t0 + T_BOUM
    sx, sy = secousse(t, boum, 26, 0.45)
    c.save(); c.translate(sx, sy)

    # 1. aspiration : les produits arrivent de tous les bords en traînées et se compriment au centre
    n = len(produits)
    for k, (nom, photo) in enumerate(produits * 2):
        d0 = 0.03 * k
        v = borne((u - d0) / (T_BOUM - d0 - 0.02))
        if v <= 0 or v >= 1: continue
        a = k / (2 * n) * 2 * math.pi + 0.4
        for g in (2, 1, 0):                         # traînée : 2 fantômes pâles derrière l'objet
            vg = max(0.0, v - 0.09 * g)
            r = 950 * (1 - vg ** 2.2)
            x, y = cx + r * math.cos(a), cy + r * math.sin(a) * 1.25
            w = mix(280, 40, vg ** 2.2)
            _objet(c, nom, photo, x, y, w, (0.18 if g else 1.0) * borne(v * 5), 300 * vg * (1 if k % 2 else -1))
    # noyau de lumière qui gonfle avant l'explosion
    nv = prog(t, t0 + 0.2, T_BOUM - 0.2, entree) * (1 - prog(t, boum, 0.25))
    if nv > 0:
        lueur_s(c, cx, cy, 80 + 260 * nv, "#FFFFFF", 0.9 * nv)
        disque(c, cx, cy, 10 + 40 * nv, "#FFFFFF", nv)

    # 2. explosion
    if u >= T_BOUM - 0.02:
        fl = 1 - (t - boum) / 0.22
        if 0 < fl <= 1:
            c.drawRect(skia.Rect.MakeXYWH(-100, -100, 1280, 2120), peinture("#FFFFFF", 0.5 * fl * fl))
        onde(c, cx, cy, t, boum, 40, 1150, "#FFFFFF", 16, 0.7)
        onde(c, cx, cy, t, boum + 0.08, 30, 800, accent, 10, 0.7)
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
                c.drawPath(pa, peinture("#DDE8FF", 0.28 * al))
                c.drawPath(pa, peinture("#FFFFFF" if k % 3 else accent, 0.85 * al, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2))
        eclats(c, cx, cy, t, boum, 20, 620, cols=["#FFFFFF", accent, "#FFD86B"], graine=21, duree=0.9)
        eclats(c, cx, cy, t, boum + 0.1, 14, 380, cols=["#FFFFFF", accent], graine=22, duree=0.8)

    # 3. le logo en 3D : rayons, anneau de produits derrière, sigle extrudé, DROP&YOU en tranches
    if u >= T_BOUM:
        e = t - boum
        a = borne(e / 0.4)
        rayons(c, cx, cy, t, 900, 0.10 * a, 16, accent)
        lueur_s(c, cx, cy, 520, accent, 0.30 * a)
        ou = prog(t, boum + 0.05, 1.2, douce)
        cam = Cam(ax=-12 + 4 * math.sin(t * 1.3), ay=mix(-28, 10, ou) + 5 * math.sin(t * 0.9), tz=mix(380, 0, ou), cx=cx, cy=cy)
        plans = []
        # anneau de produits qui tournent autour du logo
        ann = prog(t, boum + 0.35, 0.6, sortie)
        if ann > 0:
            for k, (nom, photo) in enumerate(produits):
                ang = t * 0.9 + k * 2 * math.pi / n
                R = mix(200, 400, ann)
                pos = (R * math.cos(ang), 10 + 60 * math.sin(ang * 2), 260 + 230 * math.sin(ang))   # toujours derrière le logo
                iw, ih = taille_img(nom)
                w_ = 170.0; h_ = w_ * 1.2 if photo else w_ * ih / iw
                def dess(cc, w, h, nom=nom, photo=photo):
                    if photo: image_cover(cc, nom, 0, 0, w, h, 1.0, 0.5, 0.5, w * 0.12)
                    else: image(cc, nom, 0, 0, w)
                cache = 1 - 0.6 * borne(1 - abs(pos[0]) / 260)                 # pâlit quand il passe derrière le logo
                plans.append(Plan(coins(pos, w_, h_, ay=-math.degrees(ang) + 90), w_, h_, dess, 0.85 * ann * cache, recto=False))
        # sigle DY extrudé (couches empilées en profondeur) qui fait un tour et claque
        SW = 270.0; SH = SW * 179 / 285
        sg = prog(t, boum, 0.75, lambda v: ressort(v, 1.2, 5.0))
        if sg > 0:
            tour = mix(320, 0, min(sg, 1.08)); s_ = mix(0.2, 1, min(sg, 1.1))
            for k in range(12, -1, -1):
                tint = mix(0.25, 0.9, k / 12)
                def couche(cc, w, h, k=k, tint=tint):
                    p = skia.Paint(AntiAlias=True)
                    if k > 0: p.setColorFilter(skia.ColorFilters.Blend(skia.Color4f(0.08 * tint, 0.16 * tint, 0.42 + 0.2 * tint, 1).toColor(), skia.BlendMode.kSrcIn))
                    cc.saveLayer(None)
                    _crop(cc, logo, SIGLE[0], SIGLE[1], w, h, p)
                    if k == 0: _balayage_logo(cc, w, h, 0, w, prog(t, boum + 1.05, 0.55, douce))
                    cc.restore()
                ctr = rot3((0, 0, 3.2 * k * s_), 0, tour, 0)
                plans.append(Plan(coins((ctr[0], -125 + ctr[1], ctr[2]), SW * s_, SH * s_, ay=tour), SW * s_, SH * s_, couche, borne(sg * 4), recto=False))
        # DROP&YOU : 8 tranches qui volent depuis des points 3D et se recomposent
        MW = 660.0; MH = MW * 179 / 600; nt = 8
        for k in range(nt):
            d = prog(t, boum + 0.22 + 0.045 * k, 0.55, lambda v: ressort(v, 1.15, 5.2))
            if d <= 0: continue
            sw = MW / nt; x_fin = -MW / 2 + sw * (k + 0.5)
            dep = (rng2.uniform(-900, 900), rng2.uniform(-1100, 1100), rng2.uniform(-1300, 900))
            rr = rng2.uniform(-260, 260, 3)
            q = min(d, 1.06)
            pos = (mix(dep[0], x_fin, q), mix(dep[1], 105, q), mix(dep[2], 0, q))
            def tranche(cc, w, h, k=k):
                cc.saveLayer(None)
                s0 = MOT[0] + (MOT[1] - MOT[0]) * k / nt; s1 = MOT[0] + (MOT[1] - MOT[0]) * (k + 1) / nt
                _crop(cc, logo, s0, s1, w + 0.6, h)
                _balayage_logo(cc, w, h, sw * k, MW, prog(t, boum + 1.2, 0.7, douce))
                cc.restore()
            plans.append(Plan(coins(pos, sw + 0.6, MH, ax=rr[0] * (1 - q), ay=rr[1] * (1 - q), az=rr[2] * (1 - q)), sw + 0.6, MH, tranche,
                              borne(d * 4), recto=False))
        scene3d(c, cam, plans)
        # phrase de marque
        b = prog(t, boum + 0.85, 0.45, sortie)
        if b > 0:
            texte(c, phrase, cx, cy + 270 + 24 * (1 - b), 46, "#FFFFFF", "titre", "centre", -0.02, b)
            lw = largeur(phrase, 46, "titre", -0.02) * b
            rrect(c, cx - lw / 2, cy + 342, lw, 4, 2, accent, 0.9 * b)
    c.restore()


def sons_signature(son, t0):
    son(t0, "montee", -9); son(t0 + 0.05, "whoosh_long", -9)
    son(t0 + T_BOUM, "impact", -4); son(t0 + T_BOUM + 0.02, "whoosh_bas", -6); son(t0 + T_BOUM + 0.05, "verre", -8)
    for k in range(8): son(t0 + T_BOUM + 0.22 + 0.045 * k + 0.4, "pop", -15)
    son(t0 + T_BOUM + 0.7, "impact_doux", -9)
    son(t0 + T_BOUM + 1.15, "ching", -9); son(t0 + T_BOUM + 0.9, "whoosh_court", -13)
