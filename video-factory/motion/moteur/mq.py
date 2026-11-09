"""Briques de scène MONARQUE au niveau validé (MQ-M05, 16/10/2026, « le client a adoré ») — reprises par MQ-M06 et suivantes.
Graphique « vos ventes » (un modèle différent par barre), horloge, carte d'embarquement, fiche de coûts, conversation,
carton de fin à la signature du client. Voir reference/monarque.md."""
import math
import skia
from moteur import *
from kit import pastille, tampon, texte_centre
from studio import lettres, entre, eclats, curseur
from monarque import *
from monarque import VERT, ROUGE

MODELES = ["produits/veste-ceinturee-prune", "produits/blouson-cuir-noir", "produits/veste-zip-marine", "produits/chemise-rayee-bordeaux"]


def graphique(c, t, cx, cy, hb, best=None, best_on=False, alpha=1.0, s=1.0, label="VOS VENTES", modeles=MODELES, couleur=BEIGE):
    """barres + vignettes (le style que le client aime) ; renvoie (x0, y0, base)"""
    x0, y0, w, h = cx - 420, cy - 330, 840, 660
    base = y0 + 470
    if alpha <= 0.01: return x0, y0, base
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, alpha):
        cadre(c, x0, y0, w, h, 44)
        texte(c, label, x0 + 60, y0 + 50, 34, ENCRE, "noir", track=0.06)
        for k in range(4):
            x = x0 + 90 + k * 180
            on = k == best and best_on
            hh = max(14, 330 * hb[k])
            rrect(c, x, base - hh, 120, hh, 18, couleur if on else "#DCD8D2")
            rrect(c, x - 5, base + 18, 130, 150, 22, "#EFEDEA")
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 5, base + 18, 130, 150), 22, 22), True)
            image_cover(c, modeles[k], x - 5, base + 18, 130, 150, 1.0, 0.5, 0.5); c.restore()
            if on: rrect(c, x - 5, base + 18, 130, 150, 22, None, 1, None, couleur, 5)
    c.restore()
    return x0, y0, base


def horloge(c, cx, cy, r, ang, a, aiguille=ROUGE):
    if a <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(a, a)
    disque(c, 0, 0, r, BLANC, 1, (16, 40, 0.18)); anneau(c, 0, 0, r - 4, ENCRE, 8)
    for k in range(12):
        an = k * math.pi / 6
        trait(c, (r - 26) * math.sin(an), -(r - 26) * math.cos(an), (r - 14) * math.sin(an), -(r - 14) * math.cos(an), ENCRE, 6)
    trait(c, 0, 0, r * 0.45 * math.sin(ang / 12), -r * 0.45 * math.cos(ang / 12), ENCRE, 12)
    trait(c, 0, 0, r * 0.72 * math.sin(ang), -r * 0.72 * math.cos(ang), aiguille, 7)
    disque(c, 0, 0, 14, ENCRE)
    c.restore()


def billet(c, cx, cy, w, alpha=1.0, rot=0.0, s=1.0, gris=False):
    """carte d'embarquement PARIS → CHINE (sans prix, sans date)"""
    if alpha <= 0.01 or s <= 0.01: return
    h = w * 0.52
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        rrect(c, -w / 2, -h / 2, w, h, 34, BLANC, 1, (22, 50, 0.2))
        rrect(c, -w / 2, -h / 2, w, h * 0.26, 34, "#9A968F" if gris else ENCRE)
        rrect(c, -w / 2, -h / 2 + h * 0.13, w, h * 0.13, 0, "#9A968F" if gris else ENCRE)
        texte(c, "CARTE D'EMBARQUEMENT", -w / 2 + 40, -h / 2 + h * 0.13 - hauteurLigne(26, "noir") / 2, 26, BLANC, "noir", track=0.08)
        icone(c, "plane", w / 2 - 60, -h / 2 + h * 0.13, 40, BLANC, 2.6)
        y = -h / 2 + h * 0.36
        texte(c, "PARIS", -w / 2 + 40, y, 64, ENCRE, "archivo", track=-0.01)
        texte(c, "CHINE", w / 2 - 40 - largeur("CHINE", 64, "archivo", -0.01), y, 64, ENCRE, "archivo", track=-0.01)
        trait(c, -w * 0.12, y + 40, w * 0.12, y + 40, GRIS, 4, 1, [6, 10])
        icone(c, "plane", 0, y + 40, 46, ENCRE, 2.6)
        for k, (lab, val) in enumerate([("PORTE", "—"), ("SIÈGE", "—"), ("VOL", "—")]):
            x = -w / 2 + 40 + k * (w - 80) / 3
            texte(c, lab, x, h / 2 - 120, 22, GRIS, "gras", track=0.06)
            texte(c, val, x, h / 2 - 84, 34, ENCRE, "noir")
        for k in range(26):                               # code-barres décoratif
            bw = 4 + (k * 7) % 5
            rrect(c, w / 2 - 260 + k * 9, h / 2 - 116, bw * 0.6, 70, 1, ENCRE, 0.85)
    c.restore()


def fiche_couts(c, t, x, y, w, h, t0, lignes, titre_="COSTING", rouges=()):
    """fiche de coûts sans montants : une barre par poste ; les postes de `rouges` passent au rouge"""
    texte(c, titre_, x + 30, y + 34, 34, ENCRE, "archivo", track=0.02)
    disque(c, x + w - 54, y + 56, 30, ENCRE); icone(c, "euro", x + w - 54, y + 56, 32, BLANC, 2.6)
    pas_ = min(124, (h - 150) / max(1, len(lignes)))
    for k, (lab, v) in enumerate(lignes):
        yy = y + 130 + k * pas_
        r = k in rouges
        texte(c, lab, x + 30, yy, 34, ROUGE if r else ENCRE, "gras", track=-0.01)
        rrect(c, x + 30, yy + 50, w - 60, 16, 8, "#E8E5E0")
        rrect(c, x + 30, yy + 50, (w - 60) * v * prog(t, t0 + 0.08 * k, 0.5, sortie), 16, 8, ROUGE if r else ENCRE)


def conversation(c, t, x, y, w, h, t0, titre_, msgs, ic="factory", ecart=0.3):
    """une conversation : msgs = [(texte, moi)] ; moi → bulle noire à droite, sinon blanche à gauche"""
    rrect(c, x, y, w, h, 22, "#EFEDEA")
    rrect(c, x, y, w, 76, 22, ENCRE)
    disque(c, x + 42, y + 38, 22, "#3A3A3A"); icone(c, ic, x + 42, y + 38, 24, BLANC, 2.2)
    texte(c, titre_, x + 76, y + 38 - hauteurLigne(26, "gras") / 2, 26, BLANC, "gras", track=-0.01)
    yy = y + 100
    for k, (m, moi) in enumerate(msgs):
        a = entre(t, t0 + ecart * k, 0.35, 2.2)
        if a <= 0: continue
        tw = largeur(m, 26, "gras", -0.01); bw = min(w - 40, tw + 40)
        bx = x + w - 18 - bw if moi else x + 18
        c.save(); c.translate(bx + (bw if moi else 0), yy + 28); c.scale(a, a); c.translate(-(bx + (bw if moi else 0)), -(yy + 28))
        rrect(c, bx, yy, bw, 56, 22, ENCRE if moi else BLANC, 1, None if moi else (4, 12, 0.08))
        texte(c, m, bx + 20, yy + 28 - hauteurLigne(26, "gras") / 2, 26, BLANC if moi else ENCRE, "gras", track=-0.01)
        c.restore()
        yy += 74


def flash_noir(c, t, t0, t1, l1, l2, couleur2=BEIGE, taille=150):
    """disque noir plein écran + deux lignes (le « SOYONS CLAIRS. » de MQ-M05) ; renvoie le rayon"""
    if t < t0 - 0.15 or t > t1 + 0.4: return 0
    r = disque_noir(c, t, t0 - 0.12, t1 - 0.12)
    a = entre(t, t0 - 0.02, 0.4, 2.0) * (1 - prog(t, t1 - 0.14, 0.14))
    if a > 0:
        ts1 = ajuste(l1, 960, taille, "archivo", -0.01); ts2 = ajuste(l2, 960, taille, "archivo", -0.01)
        lettres(c, l1, 540, 960 - ts1 * 1.05, ts1, t, t0 - 0.02, "ressort", fam="archivo", grad=False, couleur=BLANC, decal=0.03, alpha=borne(a * 3))
        lettres(c, l2, 540, 960 + ts2 * 0.1, ts2, t, t0 + 0.2, "ressort", fam="archivo", grad=False, couleur=couleur2, decal=0.03, alpha=borne(a * 3))
    return r


def signature(c, t, t0, lignes, t_bouton, label="monarqueprod.com", logo_y=640):
    """carton final : logo, lignes [(texte, t, fam, couleur)], bouton cliqué"""
    if t < t0 - 0.1: return
    u = entre(t, t0 - 0.05, 0.55, 1.4)
    logo(c, 540, logo_y, 820 * mix(0.7, 1, u), False, borne(u * 3))
    y = logo_y + 200
    for (txt, tl, fam, col) in lignes:
        a = entre(t, tl - 0.05, 0.45, 1.6)
        if a > 0: texte_centre(c, txt, 540, y + 30 * (1 - a), 46, col, fam, borne(a * 3), -0.01)
        y += 66
    d = entre(t, t_bouton - 0.15, 0.45, 2.0)
    if d > 0:
        by = y + 90
        clic = prog(t, t_bouton + 0.45, 0.12) * (1 - prog(t, t_bouton + 0.6, 0.15))
        s = mix(0.4, 1, d) * (1 - 0.06 * clic)
        c.save(); c.translate(540, by); c.scale(s, s)
        tw = largeur(label, 50, "noir", -0.01); w, h = tw + 190, 116
        rrect(c, -w / 2, -h / 2, w, h, h / 2, ENCRE, borne(d * 3), (16, 40, 0.3))
        icone(c, "arrow-right", w / 2 - 66, 0, 46, BLANC, 3.0, borne(d * 3))
        texte(c, label, -w / 2 + 56, -hauteurLigne(50) / 2, 50, BLANC, "noir", track=-0.01, alpha=borne(d * 3))
        c.restore()
        pc = prog(t, t_bouton + 0.05, 0.4, sortie)
        curseur(c, mix(980, 700, pc), mix(by + 370, by + 20, pc), 1.3, 1 - prog(t, t_bouton + 0.9, 0.3), clic)
        eclats(c, 540, by, t, t_bouton + 0.5, 12, 300, [BEIGE, BEIGE2, ENCRE], graine=4)


def logo_monarque(c, t, t_mq, t_pose, t_part, y=250, w=340):
    """disque noir + grand logo blanc au mot « Monarque », puis le logo noir monte se poser en tête ; renvoie le rayon"""
    if t < t_mq - 0.15 or t > t_part + 0.4: return 0
    r = disque_noir(c, t, t_mq - 0.12, t_pose)
    u = prog(t, t_mq + 0.05, 0.36, lambda v: rebond(v, 1.6))
    v = prog(t, t_pose, 0.42, entreeSortie)
    o = prog(t, t_part - 0.15, 0.3, entree)
    if t >= t_mq + 0.03:
        lw = mix(1.5, 1, u) * mix(860, w, v)
        ly = mix(960, y, v)
        if v < 1: logo(c, 540, ly, lw, True, borne(u * 3) * (1 - v))
        if v > 0: logo(c, 540, ly - 300 * o, lw, False, v * (1 - o))
    return r


# ─────────────────────────────────────────── signature de fin 3D MONARQUE (20/10/2026, demande de Youssef : « les dernières
# Monarque n'avaient pas de signature 3D ») — version Monarque de gsx.signature_gsx : cartes blanches aspirées → explosion
# (flash, ondes beige et encre, éclats) → les 8 lettres du logo MONARQUE arrivent en tranches extrudées de partout, le mot
# fait un tour et claque → « PRODUCTION AND DEVELOPMENT » glisse dessous → lignes → bouton monarqueprod.com cliqué.
import numpy as _np
from studio3d import Cam as _Cam, Plan as _Plan, coins as _coins, scene3d as _scene3d, rot3 as _rot3
import moteur as _moteur

LOGO_MQ = "logo-noir"          # 704 × 159 : lettres y 5-126, tagline y 134-159
LETTRES = [(5, 110), (118, 198), (206, 283), (291, 380), (387, 462), (465, 545), (552, 628), (637, 700)]
LY0, LY1, TAG = 5, 126, (300, 704, 133, 159)
T_BOUM = 0.5


def _crop_logo(c, x0, x1, y0, y1, w, h, paint=None):
    i = _moteur._img(LOGO_MQ)
    k = i.width() / 704.0
    c.drawImageRect(i, skia.Rect.MakeLTRB(x0 * k, y0 * k, x1 * k, y1 * k), skia.Rect.MakeWH(w, h), _moteur._ECH, paint or skia.Paint(AntiAlias=True))


def _balayage_png(c, w, h, u):
    if not (0 < u < 1): return
    x = mix(-160, w + 160, u)
    p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kSrcATop)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x - 110, 0), skia.Point(x + 110, 0)],
                                               [hexa("#FFFFFF", 0), hexa("#FFFFFF", 0.85), hexa("#FFFFFF", 0)], [0.0, 0.5, 1.0]))
    c.drawRect(skia.Rect.MakeWH(w, h), p)


def _carte_mq(c, nom, vid, x, y, w, alpha, rot, t):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(w / 200, w / 200)
    with Calque(c, alpha):
        cadre(c, -106, -156, 212, 312, 28)
        if vid: video(c, nom, -100, -150, 200, 300, t, 1.0, rayon=22)
        else: image_cover(c, nom, -100, -150, 200, 300, 1.0, 0.5, 0.5, 22)
    c.restore()


def signature_mq(c, t, t0, medias, lignes, t_bouton=None, label="monarqueprod.com", cx=510, cy=760):
    """medias : [(nom, est_video)] ; lignes : [(texte, t, taille, couleur)] ; t_bouton : le bouton monarqueprod.com cliqué"""
    u = t - t0
    if u < -0.05: return
    rng, rng2 = _np.random.default_rng(7), _np.random.default_rng(8)
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
            _carte_mq(c, nom, vid, cx + r * math.cos(a), cy + r * math.sin(a) * 1.25, mix(260, 40, vg ** 2.2),
                      (0.18 if g else 1.0) * borne(v * 5), 300 * vg * (1 if k % 2 else -1), t)
    nv = prog(t, t0 + 0.2, T_BOUM - 0.2, entree) * (1 - prog(t, boum, 0.25))
    if nv > 0:
        lueur(c, cx, cy, 80 + 260 * nv, BEIGE, 0.5 * nv)
        disque(c, cx, cy, 10 + 40 * nv, ENCRE, nv)
    if u >= T_BOUM - 0.02:
        fl = 1 - (t - boum) / 0.22
        if 0 < fl <= 1: c.drawRect(skia.Rect.MakeXYWH(-100, -100, 1280, 2120), peinture("#FFFFFF", 0.7 * fl * fl))
        onde(c, cx, cy, t, boum, 40, 1150, BEIGE, 14, 0.7)
        onde(c, cx, cy, t, boum + 0.08, 30, 800, ENCRE, 6, 0.7)
        cam = _Cam(cx=cx, cy=cy)
        e = t - boum
        if e < 1.4:
            for k in range(34):
                dx, dy, dz = rng.normal(size=3); dz = -abs(dz) * 1.6
                nn = math.sqrt(dx * dx + dy * dy + dz * dz) or 1
                vit = rng.uniform(900, 2000)
                d = vit * (1 - math.exp(-2.6 * e)) / 2.6 * 2.2
                P = (dx / nn * d, dy / nn * d + 260 * e * e, dz / nn * d)
                taille = rng.uniform(26, 70)
                rx, ry, rz = rng.uniform(0, 360, 3) + e * rng.uniform(200, 700, 3)
                pts = [_rot3((taille * math.cos(b), taille * math.sin(b) * rng.uniform(0.4, 1), 0), rx, ry, rz) for b in (0, 2.2, 4.1)]
                pr = [cam.proj((P[0] + q[0], P[1] + q[1], P[2] + q[2])) for q in pts]
                if min(z for _, _, z in pr) < -1300: continue
                pa = skia.Path(); pa.moveTo(pr[0][0], pr[0][1]); pa.lineTo(pr[1][0], pr[1][1]); pa.lineTo(pr[2][0], pr[2][1]); pa.close()
                al = borne(1 - e / 1.4)
                c.drawPath(pa, peinture("#FFFFFF", 0.7 * al))
                c.drawPath(pa, peinture(BEIGE if k % 3 == 0 else "#C9C4BC", 0.9 * al, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2))
        eclats(c, cx, cy, t, boum, 20, 620, cols=[BEIGE, ENCRE, "#C9C4BC"], graine=21, duree=0.9)
        eclats(c, cx, cy, t, boum + 0.1, 14, 380, cols=[BEIGE2, GRIS], graine=22, duree=0.8)
    if u >= T_BOUM:
        e = t - boum
        a = borne(e / 0.4)
        lueur(c, cx, cy - 60, 560, BEIGE, 0.12 * a)
        ou = prog(t, boum + 0.05, 1.2, douce)
        cam = _Cam(ax=-10 + 4 * math.sin(t * 1.3), ay=mix(-28, 8, ou) + 5 * math.sin(t * 0.9), tz=mix(380, 0, ou), cx=cx, cy=cy)
        plans = []
        ann = prog(t, boum + 0.35, 0.6, sortie)
        if ann > 0:                                  # anneau des médias de la vidéo, derrière le logo
            for k, (nom, vid) in enumerate(medias):
                ang = t * 0.8 + k * 2 * math.pi / n
                R = mix(200, 420, ann)
                pos = (R * math.cos(ang), -40 + 60 * math.sin(ang * 2), 300 + 230 * math.sin(ang))
                w_, h_ = 150.0, 225.0
                def dess(cc, w, h, nom=nom, vid=vid):
                    cadre(cc, 0, 0, w, h, w * 0.12)
                    m = w * 0.05
                    if vid: video(cc, nom, m, m, w - 2 * m, h - 2 * m, t, 1.0, rayon=w * 0.09)
                    else: image_cover(cc, nom, m, m, w - 2 * m, h - 2 * m, 1.0, 0.5, 0.5, w * 0.09)
                cache = borne((abs(pos[0]) - 300) / 110)
                plans.append(_Plan(_coins(pos, w_, h_, ay=-math.degrees(ang) + 90), w_, h_, dess, 0.85 * ann * cache, recto=False))
        # les 8 lettres : tranches extrudées qui volent de partout, puis le mot entier fait un tour et claque
        MW = 760.0; k_ = MW / (LETTRES[-1][1] - LETTRES[0][0]); LH = (LY1 - LY0) * k_
        tour = mix(300, 0, min(prog(t, boum + 0.25, 0.9, lambda v: ressort(v, 1.2, 5.0)), 1.08))
        x = -MW / 2
        for j, (lx0, lx1) in enumerate(LETTRES):
            ww = (lx1 - lx0) * k_
            d = prog(t, boum + 0.1 + 0.07 * j, 0.55, lambda v: ressort(v, 1.15, 5.2))
            if d > 0:
                dep = (rng2.uniform(-900, 900), rng2.uniform(-1100, 1100), rng2.uniform(-1300, 900)); rr = rng2.uniform(-260, 260, 3)
                q = min(d, 1.06)
                base = (x + ww / 2, -60, 0)
                for kk in range(6, -1, -1):           # extrusion : 7 couches beige derrière la lettre noire
                    tint = mix(0.55, 0.95, kk / 6)
                    def lettre(cc, w, h, kk=kk, tint=tint, lx0=lx0, lx1=lx1):
                        p = skia.Paint(AntiAlias=True)
                        if kk > 0: p.setColorFilter(skia.ColorFilters.Blend(skia.Color4f(0.79 * tint, 0.65 * tint, 0.46 * tint, 1).toColor(), skia.BlendMode.kSrcIn))
                        cc.saveLayer(None)
                        _crop_logo(cc, lx0, lx1, LY0, LY1, w, h, p)
                        if kk == 0: _balayage_png(cc, w, h, prog(t, boum + 1.25 + 0.04 * j, 0.5, douce))
                        cc.restore()
                    ctr = _rot3((base[0], base[1], base[2] + 3.2 * kk), 0, tour, 0)
                    pos = (mix(dep[0], ctr[0], q), mix(dep[1], ctr[1], q), mix(dep[2], ctr[2], q))
                    plans.append(_Plan(_coins(pos, ww, LH, ax=rr[0] * (1 - q), ay=tour + rr[1] * (1 - q), az=rr[2] * (1 - q)), ww, LH, lettre, borne(d * 4), recto=False))
            else:
                rng2.uniform(size=6)
            x += ww + (LETTRES[j + 1][0] - lx1) * k_ if j < 7 else 0
        # la ligne « PRODUCTION AND DEVELOPMENT » glisse sous le mot
        tg = prog(t, boum + 0.95, 0.5, sortie)
        if tg > 0:
            tw = (TAG[1] - TAG[0]) * k_; th = (TAG[3] - TAG[2]) * k_
            def tag(cc, w, h):
                cc.saveLayer(None); _crop_logo(cc, *TAG, w, h); _balayage_png(cc, w, h, prog(t, boum + 1.5, 0.5, douce)); cc.restore()
            ctr = _rot3((MW / 2 - tw / 2, -60 + LH / 2 + th / 2 + 10 + 40 * (1 - tg), 0), 0, tour, 0)
            plans.append(_Plan(_coins(ctr, tw, th, ay=tour), tw, th, tag, tg, recto=False))
        _scene3d(c, cam, plans)
        # lignes de marque au mot
        y = cy + 170
        for txt, tl, tai, col in lignes:
            b = prog(t, tl - 0.05, 0.4, sortie)
            morceaux = [txt]
            if largeur(txt, tai, "gras", -0.01) > 780 and " " in txt:
                m = txt.split(" ")
                k = min(range(1, len(m)), key=lambda i: abs(len(" ".join(m[:i])) - len(" ".join(m[i:]))))
                morceaux = [" ".join(m[:k]), " ".join(m[k:])]
            for mo in morceaux:
                if b > 0: texte(c, mo, cx, y + 22 * (1 - b), ajuste(mo, 780, tai, "gras", -0.01), col, "gras", "centre", -0.01, b)
                y += tai * 1.2
            y += tai * 0.2
        b = prog(t, boum + 0.9, 0.45, sortie)
        if b > 0:
            lw = 220 * b; rrect(c, cx - lw / 2, cy + 135, lw, 5, 2.5, BEIGE, b)
        if t_bouton is not None:
            d = entre(t, t_bouton - 0.15, 0.45, 2.0)
            if d > 0:
                by = y + 70
                clic = prog(t, t_bouton + 0.45, 0.12) * (1 - prog(t, t_bouton + 0.6, 0.15))
                s = mix(0.4, 1, d) * (1 - 0.06 * clic)
                c.save(); c.translate(cx, by); c.scale(s, s)
                tw = largeur(label, 46, "noir", -0.01); w, h = tw + 170, 106
                rrect(c, -w / 2, -h / 2, w, h, h / 2, ENCRE, borne(d * 3), (16, 40, 0.3))
                icone(c, "arrow-right", w / 2 - 60, 0, 42, BLANC, 3.0, borne(d * 3))
                texte(c, label, -w / 2 + 50, -hauteurLigne(46) / 2, 46, BLANC, "noir", track=-0.01, alpha=borne(d * 3))
                c.restore()
                pc = prog(t, t_bouton + 0.05, 0.4, sortie)
                if t < t_bouton + 1.3: curseur(c, mix(900, cx + 160, pc), mix(by + 370, by + 20, pc), 1.3, 1 - prog(t, t_bouton + 0.9, 0.3), clic)
                eclats(c, cx, by, t, t_bouton + 0.5, 12, 300, [BEIGE, BEIGE2, ENCRE], graine=4)
    c.restore()


def sons_signature_mq(son, t0, t_bouton=None):
    son(t0, "montee", -9); son(t0 + 0.05, "whoosh_long", -9)
    son(t0 + T_BOUM, "impact", -4); son(t0 + T_BOUM + 0.02, "whoosh_bas", -6); son(t0 + T_BOUM + 0.05, "verre", -8)
    for k in range(8): son(t0 + T_BOUM + 0.1 + 0.07 * k + 0.4, "pop", -14)
    son(t0 + T_BOUM + 1.1, "impact_doux", -8); son(t0 + T_BOUM + 1.15, "ching", -9); son(t0 + T_BOUM + 0.95, "whoosh_court", -13)
    if t_bouton is not None: son(t_bouton - 0.15, "pop", -9); son(t_bouton + 0.45, "clic", -5); son(t_bouton + 0.5, "ching", -8)
