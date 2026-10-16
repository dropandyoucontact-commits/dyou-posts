"""Briques MONARQUE (15/10/2026, MQ-M02 clair et MQ-M03 noir) : la grammaire de CB-M14 (titres lettre par lettre,
médias dans des cases, pastilles, tampons) aux couleurs du client — blanc cassé / noir, Archivo Black, accent beige
trench. Globe blanc sculpté en vraie 3D (globe_relief.py), d'après la photo de référence envoyée par le client."""
import math
import skia
from moteur import *
import moteur
from kit import pastille, tampon, texte_centre
from agence import lueur
from studio import lettres, entre, eclats, rayons, curseur
import globe_relief as GL

PAPIER, ENCRE, GRIS, BLANC = "#F5F4F2", "#0E0E0E", "#8C8985", "#FFFFFF"
NOIR = "#050506"
BEIGE, BEIGE2 = "#C9A676", "#EAD9B8"
VERT, ROUGE = "#17A05D", "#FF3B30"
PARIS, CANTON = (2.35, 48.86), (113.26, 23.13)


def polices(P):
    moteur._prov.registerTypeface(skia.Typeface.MakeFromFile(str(P / "media" / "ArchivoBlack.ttf")), "ArchivoBlack")
    moteur._prov.registerTypeface(skia.Typeface.MakeFromFile("/System/Library/Fonts/PingFang.ttc", 0), "PingFangCJK")
    moteur._FAM["archivo"] = "ArchivoBlack"
    moteur._FAM["cjk"] = "PingFangCJK"


# ─────────────────────────────────────────── fonds
def fond_clair(c, t):
    """blanc cassé, plans sculptés qui dérivent, trame de points (MQ-M01, validé)"""
    c.clear(hexa(PAPIER))
    for x0, ph, a in [(-260, 0.0, 0.9), (330, 1.4, 0.7), (900, 2.7, 0.8)]:
        c.save(); c.translate(x0 + 70 * math.sin(t * 0.22 + ph), 960); c.rotate(-32)
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeLinear([skia.Point(-230, 0), skia.Point(230, 0)],
                                                   [hexa("#FFFFFF", 0.0), hexa("#FFFFFF", a), hexa("#E4E1DC", 0.55 * a), hexa("#E4E1DC", 0.0)], [0, 0.45, 0.55, 1]))
        c.drawRect(skia.Rect.MakeXYWH(-230, -1700, 460, 3400), g)
        c.restore()
    p = peinture("#D9D6D1", 0.55)
    dy = (t * 14) % 60
    for y in range(-60, H + 60, 60):
        for x in range(30, W, 60):
            c.drawCircle(x, y + 30 - dy, 1.7, p)


def fond_sombre(c, t, pulse=0.0):
    """noir profond, deux lueurs (beige et bleu globe) qui respirent, trame discrète, vignette"""
    c.clear(hexa(NOIR))
    for (x, y, r, col, a, v, ph) in [(280, 520, 720, "#2A2318", 0.6, 0.21, 0.0), (840, 1380, 780, "#161A33", 0.7, 0.17, 2.0)]:
        cx = x + 80 * math.sin(t * v + ph); cy = y + 90 * math.cos(t * v * 0.8 + ph)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(col, a * (1 + 0.4 * pulse)), hexa(col, 0.0)]))
        c.drawCircle(cx, cy, r, p)
    p = peinture("#FFFFFF", 0.03)
    dy = (t * 10) % 64
    for y in range(-64, H + 64, 64):
        for x in range(32, W, 64):
            c.drawCircle(x, y + 32 - dy, 1.5, p)
    v = skia.Paint(AntiAlias=True)
    v.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.75, [hexa("#000000", 0.0), hexa("#000000", 0.7)], [0.5, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), v)


# ─────────────────────────────────────────── cases à médias
def cadre(c, x, y, w, h, r=36, sombre=False, accent=None, alpha=1.0):
    if sombre:
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
        c.drawRRect(rr, peinture("#FFFFFF", 0.035 * alpha))
        c.drawRRect(rr, peinture(accent or "#FFFFFF", (0.9 if accent else 0.18) * alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
    else:
        carte(c, x, y, w, h, r, BLANC, alpha, (26, 60, 0.16))
        if accent:
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
            c.drawRRect(rr, peinture(accent, alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=5))


def media(c, t, nom, x, y, w, h, alpha=1.0, s=1.0, video_t0=None, vitesse=1.0, zoom=1.0, fx=0.5, fy=0.5,
          accent=None, pad=12, r=36, sombre=False, rot=0.0, voile=None):
    """une case (blanche à ombre, ou fine sur fond noir) avec sa photo ou sa vidéo ; s et rot depuis le centre.
    w, h constants pour une vidéo (cache d'images à cette taille)."""
    if alpha <= 0.01 or s <= 0.01: return
    cx, cy = x + w / 2, y + h / 2
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, alpha):
        cadre(c, x, y, w, h, r, sombre, accent)
        if video_t0 is None:
            image_cover(c, nom, x + pad, y + pad, w - 2 * pad, h - 2 * pad, zoom, fx, fy, rayon=r - pad / 2)
        else:
            video(c, nom, x + pad, y + pad, int(w - 2 * pad), int(h - 2 * pad), t - video_t0, vitesse, rayon=r - pad / 2)
        if voile:
            col, a = voile
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + pad, y + pad, w - 2 * pad, h - 2 * pad), r - pad / 2, r - pad / 2), peinture(col, a))
    c.restore()


def pilule(c, label, cx, cy, a, ic=None, fond_=ENCRE, col=BLANC, taille=34, rot=0.0, fam="noir"):
    """pastille pleine qui jaillit (a = progression à rebond)"""
    if a <= 0.01: return
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.35, 1, a), mix(0.35, 1, a))
    pastille(c, label, 0, 0, taille, fond_, col, ic, borne(a * 2.5), (12, 30, 0.22), fam=fam)
    c.restore()


def puce_n(c, label, cx, cy, a, ic=None, couleur=BEIGE, taille=34):
    """étiquette fine sur fond noir : icône accent + texte blanc"""
    if a <= 0.01: return
    tw = largeur(label, taille, "gras", -0.01)
    w, h = tw + (taille * 1.6 if ic else 0) + taille * 1.2, taille * 2.0
    c.save(); c.translate(cx, cy); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
    with Calque(c, borne(a * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        c.drawRRect(rr, peinture("#0B0A0F", 0.85))
        c.drawRRect(rr, peinture("#FFFFFF", 0.22, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        x = -w / 2 + taille * 0.6
        if ic:
            icone(c, ic, x + taille * 0.55, 0, taille * 1.05, couleur, 2.4); x += taille * 1.6
        texte(c, label, x, -hauteurLigne(taille, "gras") / 2, taille, BLANC, "gras", track=-0.01)
    c.restore()


def tampon_n(c, label, cx, cy, t, t0, couleur=BEIGE, rot=-8, taille=52, fond_="#0B0A0F"):
    """tampon qui s'écrase (fond sombre ou blanc)"""
    if t < t0 - 0.12: return
    u = prog(t, t0 - 0.12, 0.16, entree)
    s = mix(2.6, 1, u)
    tw = largeur(label, taille, "noir"); w, h = tw + taille * 1.2, taille * 1.9
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, u):
        rrect(c, -w / 2, -h / 2, w, h, 18, fond_, 0.92, (8, 24, 0.3), couleur, 7)
        texte(c, label, 0, -hauteurLigne(taille) / 2, taille, couleur, "noir", "centre", -0.01)
    c.restore()


def coche(c, cx, cy, r, a, couleur=VERT):
    if a <= 0.01: return
    disque(c, cx, cy, r * a, couleur, 1, (6, 16, 0.25)); icone(c, "check", cx, cy, r * 1.15 * a, BLANC, 3.2)


def croix(c, cx, cy, r, a, couleur=ROUGE):
    if a <= 0.01: return
    disque(c, cx, cy, r * a, couleur, 1, (6, 16, 0.25)); icone(c, "x", cx, cy, r * 1.15 * a, BLANC, 3.2)


def signe(c, s, cx, cy, a, couleur, r=74, t=0.0, t0=0.0):
    """disque plein avec ≠ ou = au milieu de deux cases, secoué à l'arrivée"""
    if a <= 0.01: return
    sh = secousse(t, t0, 12, 0.3)
    c.save(); c.translate(cx + sh[0], cy + sh[1]); c.scale(a, a)
    disque(c, 0, 0, r, couleur, 1, (12, 30, 0.3)); texte_centre(c, s, 0, 2, r * 1.55, BLANC, "noir")
    c.restore()


# ─────────────────────────────────────────── titres et logo
def titre(c, t, txt, t0, t1, y=430, couleur=ENCRE, taille=96, larg=960, effet="masque"):
    """titre construit lettre par lettre (Archivo Black), qui s'efface à t1"""
    if t < t0 - 0.1 or t > t1 + 0.3: return
    ts = ajuste(txt, larg, taille, "archivo", -0.01)
    a = 1 - prog(t, t1 - 0.2, 0.15, entree)              # parti avant que le suivant n'entre (t1 = suivant − 0,1)
    lettres(c, txt, 540, y - ts * 0.62, ts, t, t0 - 0.05, effet, fam="archivo", grad=False, couleur=couleur,
            decal=0.022, duree=0.4, track=-0.01, alpha=a)


def logo(c, cx, cy, w, blanc=False, alpha=1.0):
    if alpha <= 0.01: return
    nom = "logo-blanc" if blanc else "logo-noir"
    iw, ih = taille_img(nom); image(c, nom, cx - w / 2, cy - w * ih / iw / 2, w, alpha)


def entete(c, t, blanc, alpha=1.0):
    logo(c, 180, 200, 230, blanc, 0.92 * alpha)


def disque_noir(c, t, t0, t1, cx=540, cy=960, couleur=ENCRE):
    r = cles(t, [(t0, 0), (t0 + 0.28, 2100, entree), (t1, 2100), (t1 + 0.34, 0, entreeSortie)])
    if r > 1: disque(c, cx, cy, r, couleur)
    return r


# ─────────────────────────────────────────── globe : épingles et arc
def epingle(c, x, y, label, u, col=ENCRE, drapeau_=None, haut=80, taille=30, fond_=None, txt=BLANC):
    if u <= 0.01: return
    with Calque(c, borne(u * 2)):
        disque(c, x, y, 11, col); anneau(c, x, y, 20 * u, col, 3, 0.45)
        trait(c, x, y, x, y - haut * u, col, 4)
        c.save(); c.translate(x, y - haut * u); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
        w, h = pastille(c, label, 0, -34, taille, fond_ or col, txt, None, 1.0, (10, 26, 0.25))
        if drapeau_: drapeau(c, drapeau_, -w / 2 - 58, -52, 48, 34, 6)
        c.restore()


def arc_globe(c, lon0, lat0, cx, cy, R, A, B, u, couleur=ENCRE, ep=7, lift=0.22):
    """arc de grand cercle de A vers B (lon, lat), tracé jusqu'à u, levé au-dessus du globe ; renvoie la tête"""
    if u <= 0: return None
    import numpy as np
    def v(p):
        lo, la = math.radians(p[0]), math.radians(p[1])
        return np.array([math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo)])
    a, b = v(A), v(B)
    om = math.acos(max(-1, min(1, float(a @ b))))
    M = GL.rotation(lon0, lat0)
    pa = peinture(couleur, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=ep); pa.setStrokeCap(skia.Paint.kRound_Cap)
    path, tete, n = skia.Path(), None, 60
    debut = True
    for k in range(n + 1):
        s = u * k / n
        p = (math.sin((1 - s) * om) * a + math.sin(s * om) * b) / math.sin(om)
        p = p * (1 + lift * math.sin(math.pi * s))
        x, y, z = M @ p
        X, Y = cx + R * x, cy - R * y
        if z < -0.05:
            debut = True; continue
        (path.moveTo if debut else path.lineTo)(X, Y); debut = False
        tete = (X, Y)
    c.drawPath(path, pa)
    return tete


# ─────────────────────────────────────────── carton final
def carton_fin(c, t, t0, t_url, sombre=False, accroche="Présentez votre projet"):
    """logo, accroche, bouton monarqueprod.com cliqué"""
    if t < t0 - 0.05: return
    u = entre(t, t0, 0.55, 1.4)
    ink = BLANC if sombre else ENCRE
    if sombre:
        lueur(c, 540, 860, 640 * u, BEIGE, 0.16)
        rayons(c, 540, 860, t, 900, 0.06 * u, 14, BEIGE2)
    logo(c, 540, 820, 820 * mix(0.7, 1, u), sombre, borne(u * 3))
    a = entre(t, t0 + 0.35, 0.45, 1.6)
    if a > 0:
        texte_centre(c, accroche, 540, 1040 + 30 * (1 - a), 46, GRIS if not sombre else "#B9B5AE", "gras", borne(a * 3), -0.01)
    b = entre(t, t_url - 0.15, 0.45, 2.0)
    if b > 0:
        clic = prog(t, t_url + 0.45, 0.12) * (1 - prog(t, t_url + 0.6, 0.15))
        s = mix(0.4, 1, b) * (1 - 0.06 * clic)
        c.save(); c.translate(540, 1190); c.scale(s, s)
        fond_ = BEIGE if sombre else ENCRE
        txt = ENCRE if sombre else BLANC
        tw = largeur("monarqueprod.com", 50, "noir", -0.01); w, h = tw + 190, 116
        rrect(c, -w / 2, -h / 2, w, h, h / 2, fond_, borne(b * 3), (16, 40, 0.3))
        icone(c, "arrow-right", w / 2 - 66, 0, 46, txt, 3.0, borne(b * 3))
        texte(c, "monarqueprod.com", -w / 2 + 56, -hauteurLigne(50) / 2, 50, txt, "noir", track=-0.01, alpha=borne(b * 3))
        c.restore()
        pc = prog(t, t_url + 0.05, 0.4, sortie)
        if t < t_url + 1.2:
            curseur(c, mix(980, 700, pc), mix(1560, 1210, pc), 1.3, 1 - prog(t, t_url + 0.9, 0.3), clic)
        eclats(c, 540, 1190, t, t_url + 0.5, 12, 300, [BEIGE, BEIGE2, BLANC if sombre else ENCRE], graine=4)


# ─────────────────────────────────────────── globe en points, pays allumé (retour du client, 16/10/2026)
# Le client préfère le globe en points de ChinaBook (photo de référence : banque/monarque/references/whatsapp-globe-a-points.png)
# au globe blanc sculpté : terres en points gris, la Chine qui s'allume en noir, halo beige. Premier usage : MQ-M05.
TERRE = "#BDB8B1"
_GLOBE = []


def _globe():
    if not _GLOBE:
        from kit import Globe
        _GLOBE.append(Globe())
    return _GLOBE[0]


def melange(c1, c2, u):
    a, b = hexa(c1), hexa(c2)
    u = borne(u)
    f = lambda s: int(round(((a >> s) & 255) * (1 - u) + ((b >> s) & 255) * u))
    return "#%02X%02X%02X" % (f(16), f(8), f(0))


def globe_points(c, lon0, lat0, cx, cy, R, lum=1.0, allume=CANTON):
    """sphère claire, terres en points, Chine allumée selon lum (0 → 1), France en noir"""
    G = _globe()
    ombre_sol(c, cx, cy + R * 1.06, R * 0.78, R * 0.09, 0.14)
    if lum > 0:
        kx, ky, kz = G.pos(*allume, lon0, lat0, R, cx, cy)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(kx, ky), R * 0.9, [hexa(BEIGE, 0.35 * lum), hexa(BEIGE, 0.0)]))
        c.drawCircle(kx, ky, R * 0.9, p)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx - R * 0.3, cy - R * 0.35), R * 1.5, [hexa("#FFFFFF"), hexa("#ECEAE6")], [0.0, 1.0]))
    c.drawCircle(cx, cy, R, p); anneau(c, cx, cy, R, "#DAD6D0", 3)
    G.terres(c, cx, cy, R, lon0, lat0, couleurs={0: TERRE, 1: melange(TERRE, ENCRE, lum), 2: TERRE, 3: ENCRE, 4: TERRE},
             grossir={1: mix(1.0, 1.35, lum), 2: 0.6, 3: 1.0})
    return G
