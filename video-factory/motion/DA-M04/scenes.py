"""DA-M04 « Stop, coach » — pub DYOU Agency pour coachs sportifs, sur les rushes humoristiques de Youssef (26 s).

Rushes (media/rushes/, personnages muets, seule la voix off parle) :
  r1  1,5 s  plein écran : « Stop ! » et la main qui frappe l'écran (son d'origine gardé, la voix part juste après)
  r2  4 s    elle tient un téléphone à écran VERT, le coach pointe → le site ATHLA incrusté (suivi_vert.py)
  r3  8 s    développé couché : elle soulève, le coach reste bouche bée
  r4  10 s   haltères : elle prend les lourds, lui les petits roses
Seul r1 est en plein écran ; r3 et r4 passent dans un téléphone, r2 dans un grand cadre de verre.
Thème ATHLA (noir + #C8FF2E). Voix : timing.json décalé de 0,95 s (media/voix.mp3 = « Stop » de r1 + voix Tomy).
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

theme_athla()
DUREE = 26.0
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresFins(K, fusions={(82,): "« COACH »,"})
J, JC, NOIR = A["violet"], A["violetClair"], A["surAccent"]
ORANGE, ROUGE, VERT, BLEU = "#FFB45C", A["rouge"], A["vert"], "#4C7DFF"
_ECH = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)


def entre(t, t0, d=0.42, s=1.5): return prog(t, t0, d, lambda v: rebond(v, s))
def sort(t, t0, d=0.26): return prog(t, t0, d, entree)


# ─────────────────────────────────────────── S0 · le hook plein écran (r1)
T_IMP = 0.80          # la main touche l'écran
T_R1 = 1.5
FISSURES = [(a, l) for a, l in zip(np.linspace(0, 2 * math.pi, 11, endpoint=False) + 0.3, [260, 180, 320, 210, 290, 160, 240, 330, 190, 270, 220])]


def s0(c, t):
    if t > T_R1 + 0.4: return
    sh = secousse(t, T_IMP, 26, 0.4)
    z = prog(t, T_R1 - 0.25, 0.5, entree)                    # le rush part en arrière, on entre dans le décor sombre
    c.save(); c.translate(540 + sh[0], 960 + sh[1]); s = mix(1, 0.55, z); c.scale(s, s); c.rotate(-6 * z); c.translate(-540, -960)
    with Calque(c, 1 - borne((z - 0.5) / 0.5)):
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeWH(1080, 1920), 80 * z, 80 * z), True)
        video(c, "rushes/r1", 0, 0, 1080, 1920, min(t, T_R1 - 0.02), boucle=False)
        g = skia.Paint()
        g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 640)], [hexa("#000000", 0.6), hexa("#000000", 0.0)]))
        c.drawRect(skia.Rect.MakeWH(1080, 640), g)
        # la vitre qui se fend sous la frappe
        f = prog(t, T_IMP, 0.12, sortie)
        if f > 0:
            cx, cy = 560, 1010
            for k, (a, l) in enumerate(FISSURES):
                x1, y1 = cx + math.cos(a) * l * f, cy + math.sin(a) * l * f
                trait(c, cx, cy, x1, y1, "#FFFFFF", 3, 0.75)
                b = a + 0.5 * (1 if k % 2 else -1)
                trait(c, cx + math.cos(a) * l * 0.55 * f, cy + math.sin(a) * l * 0.55 * f,
                      cx + math.cos(a) * l * 0.55 * f + math.cos(b) * 90 * f, cy + math.sin(a) * l * 0.55 * f + math.sin(b) * 90 * f, "#FFFFFF", 2, 0.55)
            anneau(c, cx, cy, 70 * f, "#FFFFFF", 3, 0.6); anneau(c, cx, cy, 150 * f, "#FFFFFF", 2, 0.35)
        c.restore()
    c.restore()


# ─────────────────────────────────────────── téléphone avec un rush dedans
TEL = (540, 1060, 470, 940)


def tel_rush(c, t, nom, t_local, cx=540, cy=1060, w=470, h=940, al=1.0, ry=-10.0, s=1.0, tx=0.0, sh=0.0):
    with Espace(c, cx + sh, cy, ry=ry + 2 * math.sin(t * 1.9), rx=3, s=s, tx=tx):
        telephone_sombre(c, cx + sh, cy, w, h, lambda cc, a, b, d, e: video(cc, nom, a, b, d, e, t_local, boucle=False), al)


# ─────────────────────────────────────────── S1-S3 · le soir : messages, paiement, annulation (r4 dans le téléphone)
T_S1 = T_R1 - 0.15
T_NOUS = TW(35) - 0.1
NOTIFS = [(TW(16) - 0.1, "Changer d'horaire ?", "calendar", BLEU, -320, 730, -6),
          (TW(22) - 0.1, "Paiement en attente", "wallet", ORANGE, 330, 860, 5),
          (TW(27) - 0.08, "Séance annulée", "x", ROUGE, -300, 1350, -4)]


def s1(c, t):
    if t < T_S1 or t > T_NOUS + 0.45: return
    u = entre(t, T_S1, 0.55, 1.3); o = prog(t, T_NOUS - 0.05, 0.4, entree)
    vib = secousse(t, TW(12), 10, 0.45)[0] + secousse(t, TW(27), 12, 0.35)[0]
    tel_rush(c, t, "rushes/r4", (t - T_S1) * 0.72, al=borne(u * 2) * (1 - o), s=mix(0.6, 1, u) * mix(1, 0.8, o), sh=vib, tx=-700 * o)
    a = entre(t, TW(7) - 0.1, 0.4, 2.2) * (1 - sort(t, TW(30) - 0.1))
    pastille_verre(c, "22:47", 290, 540, 44, "moon", borne(a * 2), mix(0.4, 1, a), rot=-5)
    b = entre(t, TW(12) - 0.1, 0.4, 2.4) * (1 - sort(t, TW(30) - 0.1))
    if b > 0:
        cx, cy = 790, 560
        with Calque(c, borne(b * 2)):
            c.save(); c.translate(cx, cy); c.rotate(14 * math.sin((t - TW(12)) * 30) * max(0, 1 - (t - TW(12)) / 0.6)); c.scale(mix(0.4, 1, b), mix(0.4, 1, b))
            verre(c, -60, -60, 120, 120, 60, 0.1)
            icone(c, "bell-ring", 0, 0, 60, J, 2.4)
            n = sum(1 for n_ in NOTIFS if t >= n_[0])
            if n: disque(c, 46, -46, 24, ROUGE); texte_centre(c, str(n), 46, -46, 26, "#FFFFFF", "noir")
            c.restore()
    for t0, lab, ic, col, dx, y, rot in NOTIFS:
        a = prog(t, t0, 0.42, lambda v: rebond(v, 1.6 if col != ROUGE else 2.6)) * (1 - sort(t, TW(30) - 0.05, 0.3))
        if a <= 0: continue
        x = 540 + dx
        with Espace(c, x, y, ry=mix(70 if dx < 0 else -70, 0, a), rz=rot, s=mix(1.6 if col == ROUGE else 0.4, 1, a)):
            with Calque(c, borne(a * 2)):
                w, h = 420, 150
                verre(c, x - w / 2, y - h / 2, w, h, 34, 0.1)
                disque(c, x - w / 2 + 64, y, 36, col); icone(c, ic, x - w / 2 + 64, y, 38, "#FFFFFF", 2.6)
                texte(c, lab, x - w / 2 + 116, y - 38, 30, "#FFFFFF", "gras", track=-0.01)
                texte(c, "Client · maintenant", x - w / 2 + 116, y + 6, 22, "#FFFFFF", "demi", track=0, alpha=0.6)
    # « ton coaching passe après »
    a = entre(t, TW(32) - 0.1, 0.45, 2.2) * (1 - o)
    if a > 0:
        y = 600
        with Calque(c, borne(a * 2)):
            c.save(); c.translate(540, y); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
            verre(c, -300, -80, 600, 160, 40, 0.1)
            disque(c, -220, 0, 46, ROUGE); icone(c, "trending-down", -220, 0, 50, "#FFFFFF", 2.6)
            texte(c, "Ton coaching", -150, -50, 36, "#FFFFFF", "noir", track=-0.02)
            f = mix(1, 0.18, prog(t, TW(33) - 0.1, 0.6, entreeSortie))
            rrect(c, -150, 14, 400, 24, 12, "#FFFFFF", 0.12); rrect(c, -150, 14, 400 * f, 24, 12, ROUGE)
            c.restore()


# ─────────────────────────────────────────── S4 · r2 : le téléphone à écran vert, le site incrusté, les blocs qui sortent
T_S5 = TW(58) - 0.1
CADRE = (540, 1135, 780)                  # centre x, centre y, largeur du cadre (le rush 1080×1920 y est réduit)
Q2 = np.array(json.loads((P / "suivi" / "r2.json").read_text())["coins"])
V_R2 = 0.62


@functools.lru_cache(maxsize=120)
def image_r2(k):
    return skia.Image.open(str(P / "renders" / "cache-rush" / "r2" / f"{k + 1:05d}.jpg"))


@functools.lru_cache(maxsize=120)
def masque_r2(k):
    m = np.array(Image.open(P / "suivi" / "r2" / f"{k + 1:05d}.png").convert("L"))
    a = np.zeros(m.shape + (4,), np.uint8); a[..., 3] = m; a[..., :3] = m[..., None]
    return skia.Image.fromarray(a)


DEFIL = [(T_NOUS, 0), (TW(40), 900, sortie), (TW(44) - 0.3, 1100), (TW(44) - 0.05, 23050, entreeSortie), (TW(48) - 0.3, 23200),
         (TW(48) - 0.05, 16300, entreeSortie), (TW(51) - 0.3, 16450), (TW(51) - 0.05, 19480, entreeSortie), (T_S5, 19500)]


def ecran_site(c, x, y, w, h, t):
    py = cles(t, DEFIL)
    k = w / 1040
    c.drawImageRect(moteur._img("athla-page"), skia.Rect.MakeXYWH(0, py, 1040, h / k), skia.Rect.MakeXYWH(x, y, w, h),
                    skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), skia.Paint())


def vers_quad(c, q, w, h):
    m = skia.Matrix()
    m.setPolyToPoly([skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)], [skia.Point(*p) for p in q])
    c.concat(m)


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


def surligne(c, x0, y0, k, r, t, t0, ep=5):
    u = prog(t, t0, 0.35, lambda v: rebond(v, 1.8))
    if u <= 0: return
    x, y, w, h = x0 + r[0] * k, y0 + r[1] * k, (r[2] - r[0]) * k, (r[3] - r[1]) * k
    g = 10 * (1 - u)
    lueur(c, x + w / 2, y + h / 2, max(w, h) * 0.7, J, 0.25 * u)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - g, y - g, w + 2 * g, h + 2 * g), 14, 14),
                peinture(J, u, Style=skia.Paint.kStroke_Style, StrokeWidth=ep))


def s4(c, t):
    if t < T_NOUS - 0.1 or t > T_S5 + 0.45: return
    u = entre(t, T_NOUS - 0.05, 0.6, 1.2); o = prog(t, T_S5 - 0.05, 0.4, entree)
    k = int(min(len(Q2) - 1, max(0, (t - T_NOUS) * V_R2 * 24)))
    cx, cy, cw = CADRE
    sc = cw / 1080; ch = 1920 * sc
    x0, y0 = cx - cw / 2, cy - ch / 2
    q = Q2[k]
    with Espace(c, cx, cy, ry=mix(-40, -4, u) + 1.5 * math.sin(t * 1.5), s=mix(0.5, 1, u) * mix(1, 0.85, o), tx=-900 * o):
        with Calque(c, borne(u * 2) * (1 - o)):
            lueur(c, cx, cy, 700, J, 0.18)
            verre(c, x0 - 16, y0 - 16, cw + 32, ch + 32, 52, 0.08)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0, cw, ch), 40, 40), True)
            c.translate(x0, y0); c.scale(sc, sc)
            c.drawImageRect(image_r2(k), skia.Rect.MakeWH(1080, 1920), _ECH, skia.Paint())
            # le site dans l'écran vert, sous les doigts (masque du vert)
            lp = skia.Path(); lp.addPoly([skia.Point(*p) for p in q], True)
            gl = skia.Paint(AntiAlias=True, Color=hexa(J, 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
            c.drawPath(lp, gl)
            c.saveLayer(None)
            c.save(); vers_quad(c, q, 400, 860)
            ecran_site(c, 0, 0, 400, 860, t)
            c.restore()
            mp = skia.Paint(); mp.setBlendMode(skia.BlendMode.kDstIn)
            c.drawImageRect(masque_r2(k), skia.Rect.MakeWH(1080, 1920), _ECH, mp)
            c.restore()
            c.restore()
    # point de départ des panneaux : l'écran de son téléphone, en coordonnées écran
    qc = q.mean(0); src = (x0 + qc[0] * sc, y0 + qc[1] * sc)
    cible = (700, 1240)
    a = entre(t, TW(40) - 0.1, 0.4, 2.2) * (1 - sort(t, TW(44) - 0.15))
    pastille_verre(c, "Ton site", 760, 560, 46, "globe", borne(a * 2) * (1 - o), mix(0.4, 1, a), rot=4)
    def coach(cc, x0_, y0_, kk):
        surligne(cc, x0_, y0_, kk, (505, 105, 985, 312), t, TW(45) - 0.05)
        surligne(cc, x0_, y0_, kk, (505, 320, 985, 505), t, TW(45) + 0.1)
    panneau(c, t, TW(44) - 0.1, TW(48) - 0.2, "c-coach", src, cible, 560, coach)
    def prix(cc, x0_, y0_, kk):
        surligne(cc, x0_, y0_, kk, (50, 945, 910, 1062), t, TW(50) - 0.05, 6)
    panneau(c, t, TW(48) - 0.1, TW(51) - 0.2, "c-prix", src, cible, 470, prix)
    def resa(cc, x0_, y0_, kk):
        surligne(cc, x0_, y0_, kk, (225, 210, 400, 318), t, TW(53) - 0.1, 6)
    panneau(c, t, TW(51) - 0.1, T_S5 - 0.1, "c-resa", src, cible, 560, resa)
    a = entre(t, TW(55) - 0.1, 0.4, 2.4) * (1 - o)
    pastille_verre(c, "Payé en ligne", 700, 1500, 44, "credit-card", borne(a * 2), mix(0.4, 1, a), accent=VERT, rot=-3)
    confettis(c, 700, 1380, t, TW(55), 22, 380, 5, cols=[J, JC, "#FFFFFF", VERT])


# ─────────────────────────────────────────── S5-S6 · r3 : son programme, et toi un seul écran
T_CTA0 = TW(74) - 0.1


def s5(c, t):
    if t < T_S5 - 0.1 or t > T_CTA0 + 0.45: return
    u = entre(t, T_S5, 0.55, 1.2); o = prog(t, T_CTA0 - 0.05, 0.4, entree)
    dep = prog(t, TW(65) - 0.2, 0.5, entreeSortie)          # « et toi » : le téléphone glisse à gauche
    cx = mix(540, 300, dep)
    tel_rush(c, t, "rushes/r3", (t - T_S5) * 1.4, cx=cx, al=borne(u * 2) * (1 - o), s=mix(0.6, 1, u) * mix(1, 0.92, dep), ry=mix(-10, 12, dep), tx=-800 * o)
    # le programme, sorti du téléphone
    panneau(c, t, TW(59) - 0.1, TW(65) - 0.25, "c-app", (540, 1060), (680, 1250), 520)
    a = entre(t, TW(64) - 0.1, 0.4, 2.2) * (1 - sort(t, TW(65) - 0.2))
    pastille_verre(c, "Dans sa poche", 320, 600, 44, "smartphone", borne(a * 2), mix(0.4, 1, a), rot=-5)
    # l'espace coach : tout sur un seul écran
    def coach(cc, x0_, y0_, kk):
        for j, r in enumerate([(40, 525, 990, 1240), (505, 105, 985, 312), (505, 320, 985, 505)]):
            surligne(cc, x0_, y0_, kk, r, t, TW(69) - 0.1 + 0.12 * j)
    panneau(c, t, TW(66) - 0.1, T_CTA0 - 0.1, "c-coach", (cx, 1060), (650, 1040), 640, coach, ry=-6)
    a = entre(t, TW(72) - 0.1, 0.4, 2.4) * (1 - o)
    pastille_verre(c, "Un seul écran", 650, 1500, 44, "check", borne(a * 2), mix(0.4, 1, a), accent=VERT)


# ─────────────────────────────────────────── S7 · « Commente COACH »
T_LOGO = TW(86) + 0.4
T_CTA = T_LOGO + 0.75
MOT = "COACH"
T_TAPE = [TW(82) - 0.05 + k * 0.08 for k in range(len(MOT))]
T_ENVOI = TW(83)


def s7(c, t):
    if t < T_CTA0 - 0.1 or t > T_LOGO + 0.4: return
    u = entre(t, T_CTA0, 0.55, 1.3)
    cx, cy = 540, 1040
    # « le même pour ton activité » : le site qui prend ton nom
    a = entre(t, TW(77) - 0.1, 0.45, 1.8) * (1 - sort(t, TW(80) + 0.25, 0.25))
    if a > 0:
        with Espace(c, cx, 800, rx=mix(40, 0, a), s=mix(0.5, 1, a)):
            with Calque(c, borne(a * 2)):
                verre(c, cx - 330, 640, 660, 320, 44, 0.09)
                texte(c, "ATHLA", cx, 690, 34, "#FFFFFF", "noir", "centre", 0.3, 1 - prog(t, TW(79) - 0.1, 0.3))
                b = prog(t, TW(79) - 0.1, 0.35, lambda v: rebond(v, 1.8))
                if b > 0:
                    rrect(c, cx - 220 * b, 676, 440 * b, 64, 32, J)
                    texte(c, "TON NOM ICI", cx, 692, 30, NOIR, "noir", "centre", 0.12, b)
                texte(c, "Ton site. Ton espace coach.", cx, 790, 40, "#FFFFFF", "noir", "centre", -0.02)
                texte(c, "Tes clients, au même endroit.", cx, 850, 30, JC, "demi", "centre", 0)
    # la zone de commentaire : « COACH » tapé, envoyé
    b = entre(t, TW(81) - 0.15, 0.5, 1.4)
    if b > 0:
        with Espace(c, cx, cy + 160, rx=mix(45, 0, b), s=mix(0.6, 1, b), ty=mix(200, 0, b)):
            with Calque(c, borne(b * 2)):
                y = cy + 100
                verre(c, 90, y - 120, 900, 380, 44, 0.09)
                texte(c, "Commentaires", 540, y - 90, 30, "#FFFFFF", "gras", "centre", 0)
                trait(c, 130, y - 40, 950, y - 40, "#FFFFFF", 2, 0.12)
                n = sum(1 for tt in T_TAPE if t >= tt)
                env = prog(t, T_ENVOI, 0.4, lambda v: rebond(v, 1.4))
                # le commentaire publié
                if env > 0:
                    yy = y + mix(150, 30, env)
                    with Calque(c, borne(env * 2)):
                        disque(c, 175, yy + 30, 34, "#FFFFFF", 0.2); icone(c, "user", 175, yy + 30, 34, "#FFFFFF", 2.2)
                        texte(c, "toi", 230, yy, 24, "#FFFFFF", "gras", track=0, alpha=0.7)
                        texte(c, "COACH", 230, yy + 30, 46, J, "noir", track=0.02)
                        h_ = prog(t, T_ENVOI + 0.35, 0.3, lambda v: rebond(v, 2.6))
                        if h_ > 0: icone(c, "heart", 900, yy + 30, 44 * h_, ROUGE, 2.6)
                # le champ de saisie
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
    a = entre(t, TW(85) - 0.1, 0.4, 2.4)
    pastille_verre(c, "Je t'explique en privé", 540, 1500, 44, "message-circle", borne(a * 2), mix(0.4, 1, a), accent=VERT)
    a = entre(t, TW(81) + 0.02, 0.4, 2.4) * (1 - sort(t, TW(83), 0.2))
    if a > 0:
        b_ = battement(t, TW(82), 0.15, 0.4)
        c.save(); c.translate(540, 640); c.scale(mix(0.4, 1, a) * b_, mix(0.4, 1, a) * b_)
        with Calque(c, borne(a * 2)):
            lueur(c, 0, 0, 260, J, 0.4)
            disque(c, 0, 0, 90, J); icone(c, "message-circle", 0, 0, 90, NOIR, 2.4)
        c.restore()


# ─────────────────────────────────────────── sons
son(T_IMP, "impact", -8); son(T_IMP + 0.02, "verre", -9); son(T_R1 - 0.25, "whoosh_long", -10)
son(TW(7) - 0.1, "pop", -12)
for k in range(3): son(TW(12) + 0.12 * k, "message_in", -11)
for t0, *_ in NOTIFS: son(t0, "whoosh_court", -12); son(t0 + 0.05, "message", -11)
son(TW(27), "tampon", -8); son(TW(27) + 0.02, "impact_doux", -10)
son(TW(30) - 0.1, "whoosh", -12); son(TW(32) - 0.1, "pop", -12); son(TW(33), "whoosh_bas", -12)
son(T_NOUS, "whoosh_long", -9); son(T_NOUS + 0.4, "impact_doux", -10); son(TW(40) - 0.1, "pop", -12)
for t0 in (TW(44) - 0.1, TW(48) - 0.1, TW(51) - 0.1): son(t0, "whoosh_court", -12); son(t0 + 0.2, "verre", -15)
son(TW(45) - 0.05, "blip", -13); son(TW(50) - 0.05, "clic", -10); son(TW(53) - 0.1, "clic", -10)
son(TW(55) - 0.1, "ching", -9)
son(T_S5, "whoosh", -11); son(TW(59) - 0.1, "whoosh_court", -12); son(TW(64) - 0.1, "pop", -12)
son(TW(65) - 0.2, "swipe", -12); son(TW(66) - 0.1, "verre", -13)
for j in range(3): son(TW(69) - 0.1 + 0.12 * j, "blip", -13)
son(TW(72) - 0.1, "check", -11)
son(T_CTA0, "whoosh", -11); son(TW(79) - 0.1, "pop", -11); son(TW(81) - 0.1, "pop", -10)
for tt in T_TAPE: son(tt, "frappe", -12)
son(T_ENVOI, "message", -8); son(T_ENVOI + 0.35, "pop", -11); son(TW(85) - 0.1, "ding", -12)
son(T_LOGO - 0.1, "montee", -14); son(T_LOGO + 0.24, "impact", -6); son(T_LOGO + 0.26, "verre", -9)
son(T_CTA, "whoosh", -12); son(T_CTA + 0.3, "pop", -10)

for a, b in [(T_R1 - 0.25, T_R1 + 0.3), (T_NOUS - 0.05, T_NOUS + 0.5), (TW(44) - 0.1, TW(44) + 0.4), (TW(48) - 0.1, TW(48) + 0.4),
             (TW(51) - 0.1, TW(51) + 0.4), (T_S5 - 0.05, T_S5 + 0.5), (TW(66) - 0.1, TW(66) + 0.4), (T_CTA0 - 0.05, T_CTA0 + 0.5),
             (T_LOGO, T_LOGO + 0.35), (T_CTA - 0.1, T_CTA + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_IMP, "#FFFFFF", 0.35), (TW(27), ROUGE, 0.12), (TW(55), VERT, 0.1), (T_ENVOI, J, 0.14), (T_LOGO + 0.24, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, TW(55), 1, 0.5) + battement(t, T_ENVOI, 1, 0.5) - 2)
    if t < T_LOGO + 0.45:
        s1(c, t); s4(c, t); s5(c, t); s7(c, t)
        s0(c, t)
    disque_logo(c, t, T_LOGO, T_CTA)
    carton_agence(c, t, T_CTA + 0.25, accroche="Commente « COACH » sous la vidéo")
    K.dessine_eclairs(c, t)
    if t < T_LOGO + 0.15: SOUS.dessine(c, t)
