"""DA-M05 « Résine » — pub DYOU Agency pour les artisans des sols en résine époxy, sur les rushes de Youssef (28,7 s).
Même montage que DA-M04 (« la vidéo est parfaite, ça c'est du montage »), thème POLYRA (cuivre sur noir).

Rushes (media/rushes/, 720×1280, 24 i/s, muets — seule la voix off parle) :
  r1  3,2 s  selfie qui montre le sol → plein écran, le hook (« Si tu fais des sols en résine comme celui-ci… »)
  r2  3,9 s  ponçage            ┐ dans le téléphone 3D (« poncer, préparer, couler »)
  r3  4,3 s  coulée à la raclette ┘
  r4  6 s    ordinateur à écran VERT → vieux site fictif incrusté ; il le referme et le jette sur « Résultat »
  r5  6 s    téléphone à écran VERT → le site POLYRA incrusté, les blocs sortent en verre
  r6  6 s    il marche vers la caméra puis selfie → dans le téléphone sur « Tu veux le même ? »
Suivi des écrans verts : suivi_vert.py (fonctions de DY-M02). Site : capture mobile de /realisations/polyra/ (520 px ×2).
"""
import functools, json, math, pathlib, sys
import numpy as np
import skia
from PIL import Image

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence

theme_polyra()
DUREE = 28.7
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresFins(K, fusions={(96,): "« RÉSINE »,"})
J, JC, NOIR = A["violet"], A["violetClair"], A["surAccent"]
ORANGE, ROUGE, VERT, BLEU = "#FFB45C", A["rouge"], A["vert"], "#4C7DFF"
_ECH = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)
_ECH2 = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)


def entre(t, t0, d=0.42, s=1.5): return prog(t, t0, d, lambda v: rebond(v, s))
def sort(t, t0, d=0.26): return prog(t, t0, d, entree)


# ─────────────────────────────────────────── S0 · le hook plein écran (r1, selfie sur le sol)
T_R1 = TW(14) - 0.12          # « Tu »


def s0(c, t):
    if t > T_R1 + 0.5: return
    z = prog(t, T_R1 - 0.25, 0.5, entree)                    # le rush part en arrière, on entre dans le décor sombre
    pz = 1 + 0.04 * borne(t / 3.0)                           # léger zoom continu
    c.save(); c.translate(540, 960); s = mix(1, 0.55, z) * pz; c.scale(s, s); c.rotate(-6 * z); c.translate(-540, -960)
    with Calque(c, 1 - borne((z - 0.5) / 0.5)):
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeWH(1080, 1920), 80 * z, 80 * z), True)
        video(c, "rushes/r1", 0, 0, 1080, 1920, min(t, T_R1), vitesse=0.95, boucle=False)
        g = skia.Paint()
        g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 640)], [hexa("#000000", 0.6), hexa("#000000", 0.0)]))
        c.drawRect(skia.Rect.MakeWH(1080, 640), g)
        c.restore()
    c.restore()
    # « comme celui-ci » : le sol est désigné
    a = entre(t, TW(7) - 0.05, 0.4, 2.2) * (1 - sort(t, T_R1 - 0.3))
    if a > 0:
        y = 1560 + 14 * math.sin(t * 6)
        pastille_verre(c, "Sol en résine", 540, 1420, 46, "sparkles", borne(a * 2), mix(0.4, 1, a))
        with Calque(c, borne(a * 2)):
            for k in range(3):
                b = borne(a * 3 - k * 0.6)
                trait(c, 540 - 26, y + 40 * k, 540, y + 26 + 40 * k, "#FFFFFF", 6, 0.9 * b)
                trait(c, 540 + 26, y + 40 * k, 540, y + 26 + 40 * k, "#FFFFFF", 6, 0.9 * b)
    a = entre(t, TW(9) - 0.08, 0.4, 2.4) * (1 - sort(t, T_R1 - 0.3))
    pastille_verre(c, "C'est pour toi", 540, 1180, 44, "hand", borne(a * 2), mix(0.4, 1, a), rot=-3)


# ─────────────────────────────────────────── téléphone avec un rush dedans
def tel_rush(c, t, ecran, cx=540, cy=1060, w=470, h=940, al=1.0, ry=-10.0, s=1.0, tx=0.0, sh=0.0):
    with Espace(c, cx + sh, cy, ry=ry + 2 * math.sin(t * 1.9), rx=3, s=s, tx=tx):
        telephone_sombre(c, cx + sh, cy, w, h, ecran, al)


# ─────────────────────────────────────────── S1 · des jours à poncer, préparer, couler (r2 puis r3 dans le téléphone)
T_S1 = T_R1 - 0.1
T_PB = TW(27) - 0.1           # « Et quand un client… »
T_COULE = TW(22) - 0.05


def s1(c, t):
    if t < T_S1 or t > T_PB + 0.45: return
    u = entre(t, T_S1, 0.55, 1.3); o = prog(t, T_PB - 0.05, 0.4, entree)
    x = borne((t - T_COULE) / 0.25)
    def ecran(cc, a, b, d, e):
        if x < 1: video(cc, "rushes/r2", a, b, d, e, (t - T_S1) * 1.25, boucle=False)
        if x > 0: video(cc, "rushes/r3", a, b, d, e, (t - T_COULE) * 1.2 + 0.4, boucle=False, alpha=x)
    vib = secousse(t, T_COULE, 10, 0.35)[0]
    tel_rush(c, t, ecran, al=borne(u * 2) * (1 - o), s=mix(0.6, 1, u) * mix(1, 0.8, o), sh=vib, tx=-700 * o)
    fin = sort(t, T_PB - 0.25)
    for t0, lab, ic, x_, y_, rot, acc in [(TW(17) - 0.1, "Des jours", "calendar", 540, 500, 0, None),
                                         (TW(19) - 0.1, "Ponçage", "hammer", 260, 760, -6, None),
                                         (TW(21) - 0.1, "Préparation", "paintbrush", 820, 1000, 5, None),
                                         (TW(23) - 0.1, "Coulée", "sparkles", 270, 1290, -4, None),
                                         (TW(26) - 0.1, "Un sol parfait", "check", 700, 1570, 3, VERT)]:
        a = entre(t, t0, 0.4, 2.2) * (1 - fin)
        pastille_verre(c, lab, x_, y_, 42, ic, borne(a * 2), mix(0.4, 1, a), accent=acc, rot=rot)
    confettis(c, 700, 1500, t, TW(26), 18, 340, 3, cols=[J, JC, "#FFFFFF"])


# ─────────────────────────────────────────── cadre de verre avec un rush à écran vert (r4, r5)
def _coins(nom): return np.array(json.loads((P / "suivi" / f"{nom}.json").read_text())["coins"])
Q = {"r4": _coins("r4"), "r5": _coins("r5")}


@functools.lru_cache(maxsize=160)
def image_rush(nom, k):
    return skia.Image.open(str(P / "renders" / "cache-rush" / nom / f"{k + 1:05d}.jpg"))


@functools.lru_cache(maxsize=160)
def masque(nom, k):
    m = np.array(Image.open(P / "suivi" / nom / f"{k + 1:05d}.png").convert("L"))
    a = np.zeros(m.shape + (4,), np.uint8); a[..., 3] = m; a[..., :3] = m[..., None]
    return skia.Image.fromarray(a)


def vers_quad(c, q, w, h):
    m = skia.Matrix()
    m.setPolyToPoly([skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)], [skia.Point(*p) for p in q])
    c.concat(m)


def cadre_vert(c, t, nom, k, src, cx, cy, fw, contenu, cw, ch, u, o, sortie_x=-900):
    """le rush 1080×1920 recadré sur src=(x, y, w, h), posé dans une carte de verre de largeur fw centrée en (cx, cy) ;
    contenu(c, w, h) est dessiné dans l'écran vert (sous les doigts). Renvoie la fonction écran→coordonnées vidéo."""
    sx, sy, sw, sh = src
    sc = fw / sw; fh = sh * sc
    x0, y0 = cx - fw / 2, cy - fh / 2
    q = Q[nom][k]
    with Espace(c, cx, cy, ry=mix(-40, -4, u) + 1.5 * math.sin(t * 1.5), s=mix(0.5, 1, u) * mix(1, 0.85, o), tx=sortie_x * o):
        with Calque(c, borne(u * 2) * (1 - o)):
            lueur(c, cx, cy, 700, J, 0.18)
            verre(c, x0 - 16, y0 - 16, fw + 32, fh + 32, 52, 0.08)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0, fw, fh), 40, 40), True)
            c.translate(x0, y0); c.scale(sc, sc); c.translate(-sx, -sy)
            c.drawImageRect(image_rush(nom, k), skia.Rect.MakeWH(1080, 1920), _ECH, skia.Paint())
            lp = skia.Path(); lp.addPoly([skia.Point(*p) for p in q], True)
            c.drawPath(lp, skia.Paint(AntiAlias=True, Color=hexa(J, 0.3), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)))
            c.saveLayer(None)
            c.save(); vers_quad(c, q, cw, ch); contenu(c, cw, ch); c.restore()
            mp = skia.Paint(); mp.setBlendMode(skia.BlendMode.kDstIn)
            c.drawImageRect(masque(nom, k), skia.Rect.MakeWH(1080, 1920), _ECH, mp)
            c.restore()
            c.restore()
    return lambda p: (x0 + (p[0] - sx) * sc, y0 + (p[1] - sy) * sc)


def panneau(c, t, ta, tb, nom, src, cible, w, extra=None, ry=-8):
    u = prog(t, ta, 0.5, lambda v: rebond(v, 1.15))
    o = prog(t, tb, 0.3, entree)
    if u <= 0 or o >= 1: return
    iw, ih = taille_img(nom); h = w * ih / iw
    v = u * (1 - o)
    px, py_ = mix(src[0], cible[0], v), mix(src[1], cible[1], v)
    with Espace(c, px, py_, ry=mix(20, ry, v), s=mix(0.15, 1, v)):
        with Calque(c, borne(v * 3)):
            pad = 16
            lueur(c, px, py_, w * 0.8, J, 0.2 * v)
            verre(c, px - w / 2 - pad, py_ - h / 2 - pad, w + 2 * pad, h + 2 * pad, 36, 0.1)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(px - w / 2, py_ - h / 2, w, h), 22, 22), True)
            image(c, nom, px - w / 2, py_ - h / 2, w)
            c.restore()
            if extra: extra(c, px - w / 2, py_ - h / 2, w / iw)


def surligne(c, x0, y0, k, r, t, t0, ep=5, coul=None):
    u = prog(t, t0, 0.35, lambda v: rebond(v, 1.8))
    if u <= 0: return
    coul = coul or J
    x, y, w, h = x0 + r[0] * k, y0 + r[1] * k, (r[2] - r[0]) * k, (r[3] - r[1]) * k
    g = 10 * (1 - u)
    lueur(c, x + w / 2, y + h / 2, max(w, h) * 0.7, coul, 0.25 * u)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - g, y - g, w + 2 * g, h + 2 * g), 14, 14),
                peinture(coul, u, Style=skia.Paint.kStroke_Style, StrokeWidth=ep))


# ─────────────────────────────────────────── S2 · le vieux site (r4) : il le referme et le jette
T_NOUS = TW(57) - 0.12
T_JETTE = TW(51) - 0.05       # « Résultat »
V_R4 = 0.715
SRC4 = (60, 250, 1020, 1330)


def s2(c, t):
    if t < T_PB - 0.1 or t > T_NOUS + 0.45: return
    u = entre(t, T_PB - 0.05, 0.6, 1.2); o = prog(t, T_NOUS - 0.05, 0.4, entree)
    k = int(min(len(Q["r4"]) - 1, max(0, (t - T_PB) * V_R4 * 24)))
    def vieux(cc, w, h):
        cc.drawImageRect(moteur._img("vieux-site"), skia.Rect.MakeWH(w, h), _ECH2, skia.Paint())
    sh = secousse(t, T_JETTE + 0.15, 18, 0.4)
    c.save(); c.translate(sh[0], sh[1])
    vers = cadre_vert(c, t, "r4", k, SRC4, 540, 1100, 860, vieux, 960, 600, u, o)
    c.restore()
    fin = sort(t, T_JETTE - 0.1)
    a = entre(t, TW(33) - 0.1, 0.4, 2.2) * (1 - fin)
    pastille_verre(c, "Ton site", 800, 520, 46, "globe", borne(a * 2), mix(0.4, 1, a), rot=4)
    a = entre(t, TW(39) - 0.1, 0.4, 2.4) * (1 - fin)
    pastille_verre(c, "Mis à jour en 2011", 330, 640, 40, "clock", borne(a * 2), mix(0.4, 1, a), accent=ROUGE, rot=-4)
    # les trois photos floues sortent de l'écran
    qc = Q["r4"][k].mean(0)
    def barre(cc, x0_, y0_, kk):
        b = prog(t, TW(43) - 0.05, 0.35, lambda v: rebond(v, 2))
        if b > 0:
            for j in range(3):
                cx_, cy_ = x0_ + (85 + 170 * j) * kk, y0_ + 80 * kk
                c.save(); c.translate(cx_, cy_); c.scale(b, b)
                disque(cc, 0, 0, 34, ROUGE); icone(cc, "eye-off", 0, 0, 34, "#FFFFFF", 2.6)
                c.restore()
    panneau(c, t, TW(41) - 0.1, T_JETTE - 0.15, "c-photos", vers(qc), (540, 1500), 760, barre, ry=-4)
    a = entre(t, TW(46) - 0.1, 0.4, 2.4) * (1 - fin)
    pastille_verre(c, "Ton travail ne se voit pas", 540, 1720, 40, "image-off", borne(a * 2), mix(0.4, 1, a), accent=ROUGE)
    # « il appelle un autre artisan »
    a = entre(t, TW(53) - 0.1, 0.45, 1.8) * (1 - o)
    if a > 0:
        y = 600
        with Espace(c, 540, y, rx=mix(50, 0, a), s=mix(0.5, 1, a)):
            with Calque(c, borne(a * 2)):
                w, h = 680, 170
                verre(c, 540 - w / 2, y - h / 2, w, h, 44, 0.1)
                p_ = battement(t, TW(53), 0.12, 0.5) * (1 + 0.06 * math.sin(t * 18) * borne(1 - (t - TW(53)) / 1.2))
                c.save(); c.translate(540 - w / 2 + 90, y); c.scale(p_, p_)
                disque(c, 0, 0, 50, VERT); icone(c, "phone", 0, 0, 50, "#FFFFFF", 2.6)
                c.restore()
                texte(c, "Appel en cours…", 540 - w / 2 + 170, y - 46, 34, "#FFFFFF", "noir", track=-0.01)
                texte(c, "Un autre artisan", 540 - w / 2 + 170, y + 6, 28, "#FFFFFF", "demi", track=0, alpha=0.65)
    a = entre(t, TW(56) - 0.1, 0.4, 2.6) * (1 - o)
    pastille_verre(c, "Client perdu", 800, 760, 40, "trending-down", borne(a * 2), mix(0.4, 1, a), accent=ROUGE, rot=5)


# ─────────────────────────────────────────── S3 · POLYRA dans le téléphone à écran vert (r5), les blocs sortent
T_CTA0 = TW(88) - 0.1         # « Tu veux le même… »
V_R5 = 0.58
SRC5 = (40, 160, 760, 1080)
DEFIL = [(T_NOUS, 0), (TW(68) - 0.3, 0), (TW(68) - 0.05, 4980, entreeSortie), (TW(72) - 0.3, 5000),
         (TW(72) - 0.05, 7640, entreeSortie), (TW(76) - 0.3, 7660), (TW(76) - 0.05, 10940, entreeSortie),
         (TW(78) - 0.3, 10960), (TW(78) - 0.05, 13930, entreeSortie), (T_CTA0, 13950)]


def ecran_polyra(cc, w, h, t):
    py = cles(t, DEFIL)
    k = w / 1040
    cc.drawImageRect(moteur._img("polyra-page"), skia.Rect.MakeXYWH(0, py, 1040, h / k), skia.Rect.MakeWH(w, h), _ECH2, skia.Paint())


def s3(c, t):
    if t < T_NOUS - 0.1 or t > T_CTA0 + 0.45: return
    u = entre(t, T_NOUS - 0.05, 0.6, 1.2); o = prog(t, T_CTA0 - 0.05, 0.4, entree)
    k = int(min(len(Q["r5"]) - 1, max(0, (t - T_NOUS) * V_R5 * 24)))
    vers = cadre_vert(c, t, "r5", k, SRC5, 540, 1130, 820, lambda cc, w, h: ecran_polyra(cc, w, h, t), 400, 860, u, o)
    src = vers(Q["r5"][k].mean(0))
    cible = (690, 1330)
    a = entre(t, TW(64) - 0.1, 0.4, 2.2) * (1 - sort(t, TW(68) - 0.15))
    pastille_verre(c, "À l'image de ta marque", 600, 540, 42, "wand-sparkles", borne(a * 2), mix(0.4, 1, a), rot=3)
    panneau(c, t, TW(68) - 0.1, TW(72) - 0.2, "c-espace", src, cible, 500)
    a = entre(t, TW(71) - 0.1, 0.4, 2.4) * (1 - sort(t, TW(72) - 0.2))
    pastille_verre(c, "En grand", 690, 1745, 42, "eye", borne(a * 2), mix(0.4, 1, a), rot=-3)
    def finitions(cc, x0_, y0_, kk):
        surligne(cc, x0_, y0_, kk, (8, 50, 392, 850), t, TW(75) - 0.1)
        surligne(cc, x0_, y0_, kk, (418, 50, 866, 850), t, TW(75) + 0.05)
        b = prog(t, TW(73) - 0.1, 0.35, lambda v: rebond(v, 2))
        if b > 0:
            for cx_ in (200, 640):
                c.save(); c.translate(x0_ + cx_ * kk, y0_ + 400 * kk); c.scale(b, b)
                disque(cc, 0, 0, 40, "#FFFFFF", 0.85); icone(cc, "play", 4, 0, 36, NOIR, 2.6)
                c.restore()
    panneau(c, t, TW(72) - 0.1, TW(76) - 0.2, "c-finitions", src, cible, 560, finitions)
    def methode(cc, x0_, y0_, kk):
        for j, (ya, yb) in enumerate([(48, 452), (496, 900), (940, 1344), (1384, 1788)]):
            surligne(cc, x0_, y0_, kk, (20, ya, 988, yb), t, TW(77) - 0.1 + 0.13 * j, 4)
    panneau(c, t, TW(76) - 0.1, TW(78) - 0.2, "c-methode", src, cible, 450, methode)
    def devis(cc, x0_, y0_, kk):
        surligne(cc, x0_, y0_, kk, (48, 872, 948, 976), t, TW(84) - 0.1, 6)
        # deux clics
        for j, tc in enumerate((TW(86) - 0.05, TW(87) - 0.05)):
            b = prog(t, tc, 0.4, sortie)
            if 0 < b < 1:
                anneau(cc, x0_ + 880 * kk, y0_ + 924 * kk, mix(10, 70, b), "#FFFFFF", 4, 1 - b)
        m = prog(t, TW(85) - 0.2, 0.4, entreeSortie)
        if m > 0:
            mx, my = mix(x0_ + 1100 * kk, x0_ + 890 * kk, m), mix(y0_ + 1200 * kk, y0_ + 935 * kk, m)
            pr = 1 - 0.15 * (battement(t, TW(86) - 0.05, 1, 0.15) + battement(t, TW(87) - 0.05, 1, 0.15) - 2)
            c.save(); c.translate(mx, my); c.scale(pr, pr)
            icone(cc, "mouse-pointer-click", 0, 0, 64, "#FFFFFF", 2.6)
            c.restore()
    panneau(c, t, TW(78) - 0.1, T_CTA0 - 0.1, "c-devis", src, cible, 540, devis)
    a = entre(t, TW(87) + 0.1, 0.4, 2.4) * (1 - o)
    pastille_verre(c, "Demande de devis reçue", 600, 1720, 40, "check", borne(a * 2), mix(0.4, 1, a), accent=VERT, rot=-3)
    confettis(c, 690, 1500, t, TW(87) + 0.1, 22, 380, 5, cols=[J, JC, "#FFFFFF", VERT])


# ─────────────────────────────────────────── S4 · « Tu veux le même ? » (r6) puis « Commente RÉSINE »
T_LOGO = TW(100) + 0.4
T_CTA = T_LOGO + 0.75
MOT = "RÉSINE"
T_TAPE = [TW(96) - 0.05 + k * 0.07 for k in range(len(MOT))]
T_ENVOI = TW(97)


def s4(c, t):
    if t < T_CTA0 - 0.1 or t > T_LOGO + 0.4: return
    u = entre(t, T_CTA0, 0.55, 1.3)
    cx, cy = 540, 1040
    so = sort(t, TW(95) - 0.2, 0.3)
    # r6 dans le téléphone : il arrive vers toi
    if so < 1:
        tel_rush(c, t, lambda cc, a, b, d, e: video(cc, "rushes/r6", a, b, d, e, (t - T_CTA0) * 1.6 + 0.6, boucle=False),
                 cx=540, cy=1300, w=330, h=660, al=borne(u * 2) * (1 - so), s=mix(0.6, 1, u), ry=-8, tx=-700 * so)
    # le site qui prend ton nom
    a = entre(t, TW(91) - 0.1, 0.45, 1.8) * (1 - sort(t, TW(94) + 0.25, 0.25))
    if a > 0:
        with Espace(c, cx, 760, rx=mix(40, 0, a), s=mix(0.5, 1, a)):
            with Calque(c, borne(a * 2)):
                verre(c, cx - 330, 600, 660, 320, 44, 0.09)
                texte(c, "POLYRA", cx, 650, 34, "#FFFFFF", "noir", "centre", 0.3, 1 - prog(t, TW(93) - 0.1, 0.3))
                b = prog(t, TW(93) - 0.1, 0.35, lambda v: rebond(v, 1.8))
                if b > 0:
                    rrect(c, cx - 220 * b, 636, 440 * b, 64, 32, J)
                    texte(c, "TON NOM ICI", cx, 652, 30, NOIR, "noir", "centre", 0.12, b)
                texte(c, "Ton site. Tes sols.", cx, 750, 40, "#FFFFFF", "noir", "centre", -0.02)
                texte(c, "Ta marque, en grand.", cx, 810, 30, JC, "demi", "centre", 0)
    # la zone de commentaire : « RÉSINE » tapé, envoyé
    b = entre(t, TW(95) - 0.15, 0.5, 1.4)
    if b > 0:
        with Espace(c, cx, cy + 160, rx=mix(45, 0, b), s=mix(0.6, 1, b), ty=mix(200, 0, b)):
            with Calque(c, borne(b * 2)):
                y = cy + 100
                verre(c, 90, y - 120, 900, 380, 44, 0.09)
                texte(c, "Commentaires", 540, y - 90, 30, "#FFFFFF", "gras", "centre", 0)
                trait(c, 130, y - 40, 950, y - 40, "#FFFFFF", 2, 0.12)
                n = sum(1 for tt in T_TAPE if t >= tt)
                env = prog(t, T_ENVOI, 0.4, lambda v: rebond(v, 1.4))
                if env > 0:
                    yy = y + mix(150, 30, env)
                    with Calque(c, borne(env * 2)):
                        disque(c, 175, yy + 30, 34, "#FFFFFF", 0.2); icone(c, "user", 175, yy + 30, 34, "#FFFFFF", 2.2)
                        texte(c, "toi", 230, yy, 24, "#FFFFFF", "gras", track=0, alpha=0.7)
                        texte(c, "RÉSINE", 230, yy + 30, 46, J, "noir", track=0.02)
                        h_ = prog(t, T_ENVOI + 0.35, 0.3, lambda v: rebond(v, 2.6))
                        if h_ > 0: icone(c, "heart", 900, yy + 30, 44 * h_, ROUGE, 2.6)
                yf = y + 170 if env <= 0 else y + 190
                rrect(c, 130, yf - 40, 700, 80, 40, "#FFFFFF", 0.1)
                txt = MOT[:n] if env <= 0 else ""
                texte(c, txt or ("Ajoute un commentaire…" if env > 0 or n == 0 else ""), 170, yf - hauteurLigne(34) / 2, 34,
                      "#FFFFFF" if txt else A["gris"], "noir" if txt else "demi", track=0.02 if txt else 0)
                if txt and (t * 2) % 1 < 0.5:
                    rrect(c, 172 + largeur(txt, 34, "noir", 0.02), yf - 22, 4, 44, 2, J)
                p = battement(t, T_ENVOI - 0.05, 0.2, 0.3)
                c.save(); c.translate(900, yf); c.scale(p, p)
                disque(c, 0, 0, 46, J); icone(c, "send", -2, 2, 44, NOIR, 2.6)
                c.restore()
    a = entre(t, TW(99) - 0.1, 0.4, 2.4)
    pastille_verre(c, "Je t'explique en privé", 540, 1500, 44, "message-circle", borne(a * 2), mix(0.4, 1, a), accent=VERT)
    a = entre(t, TW(95) + 0.02, 0.4, 2.4) * (1 - sort(t, TW(97), 0.2))
    if a > 0:
        b_ = battement(t, TW(96), 0.15, 0.4)
        c.save(); c.translate(540, 640); c.scale(mix(0.4, 1, a) * b_, mix(0.4, 1, a) * b_)
        with Calque(c, borne(a * 2)):
            lueur(c, 0, 0, 260, J, 0.4)
            disque(c, 0, 0, 90, J); icone(c, "message-circle", 0, 0, 90, NOIR, 2.4)
        c.restore()


# ─────────────────────────────────────────── sons
son(0.0, "whoosh_court", -12); son(TW(7) - 0.05, "pop", -11); son(TW(9) - 0.08, "pop", -12)
son(T_R1 - 0.25, "whoosh_long", -10); son(T_S1 + 0.2, "impact_doux", -10)
for t0 in (TW(17), TW(19), TW(21), TW(23)): son(t0 - 0.1, "pop", -12)
son(T_COULE, "whoosh_court", -12); son(TW(26) - 0.1, "check", -10)
son(T_PB, "whoosh_long", -9); son(T_PB + 0.4, "impact_doux", -10)
son(TW(33) - 0.1, "pop", -12); son(TW(39) - 0.1, "blip", -11)
son(TW(41) - 0.1, "whoosh_court", -12); son(TW(41) + 0.1, "verre", -15); son(TW(43) - 0.05, "blip", -12)
son(TW(46) - 0.1, "pop", -12)
son(T_JETTE + 0.12, "impact", -7); son(T_JETTE + 0.14, "tampon", -9)
for j in range(3): son(TW(53) + 0.25 * j, "message_in", -12)
son(TW(56) - 0.1, "whoosh_bas", -12)
son(T_NOUS, "whoosh_long", -9); son(T_NOUS + 0.4, "impact_doux", -10); son(TW(64) - 0.1, "pop", -12)
for t0 in (TW(68), TW(72), TW(76), TW(78)): son(t0 - 0.1, "whoosh_court", -12); son(t0 + 0.1, "verre", -15)
son(TW(71) - 0.1, "pop", -12); son(TW(73) - 0.1, "blip", -12)
son(TW(75) - 0.1, "blip", -13); son(TW(75) + 0.05, "blip", -13)
for j in range(4): son(TW(77) - 0.1 + 0.13 * j, "blip", -13)
son(TW(84) - 0.1, "pop", -12); son(TW(86) - 0.05, "clic", -9); son(TW(87) - 0.05, "clic", -9); son(TW(87) + 0.1, "ching", -9)
son(T_CTA0, "whoosh", -11); son(TW(93) - 0.1, "pop", -11); son(TW(95) - 0.1, "pop", -10)
for tt in T_TAPE: son(tt, "frappe", -12)
son(T_ENVOI, "message", -8); son(T_ENVOI + 0.35, "pop", -11); son(TW(99) - 0.1, "ding", -12)
son(T_LOGO - 0.1, "montee", -14); son(T_LOGO + 0.24, "impact", -6); son(T_LOGO + 0.26, "verre", -9)
son(T_CTA, "whoosh", -12); son(T_CTA + 0.3, "pop", -10)

for a, b in [(T_R1 - 0.25, T_R1 + 0.3), (T_PB - 0.05, T_PB + 0.5), (TW(41) - 0.1, TW(41) + 0.4), (T_NOUS - 0.05, T_NOUS + 0.5),
             (TW(68) - 0.1, TW(68) + 0.4), (TW(72) - 0.1, TW(72) + 0.4), (TW(76) - 0.1, TW(76) + 0.4), (TW(78) - 0.1, TW(78) + 0.4),
             (T_CTA0 - 0.05, T_CTA0 + 0.5), (T_LOGO, T_LOGO + 0.35), (T_CTA - 0.1, T_CTA + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_JETTE + 0.12, ROUGE, 0.16), (TW(26), VERT, 0.08), (TW(87) + 0.1, VERT, 0.1), (T_ENVOI, J, 0.14),
                    (T_LOGO + 0.24, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, TW(87), 1, 0.5) + battement(t, T_ENVOI, 1, 0.5) - 2)
    if t < T_LOGO + 0.45:
        s1(c, t); s2(c, t); s3(c, t); s4(c, t)
        s0(c, t)
    disque_logo(c, t, T_LOGO, T_CTA)
    carton_agence(c, t, T_CTA + 0.25, accroche="Commente « RÉSINE » sous la vidéo")
    K.dessine_eclairs(c, t)
    if t < T_LOGO + 0.15: SOUS.dessine(c, t)
