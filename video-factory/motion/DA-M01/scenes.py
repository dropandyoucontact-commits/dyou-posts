"""DA-M01 « T'as remarqué ? » — pub DYOU Agency pour vendre des vidéos motion (21,7 s).

Mécanique : la vidéo se prend elle-même en preuve. Accroche dopamine (ton commerce dans une vidéo comme ça),
rupture (« T'as remarqué ? Ça fait cinq secondes que tu regardes » + chronomètre qui tourne depuis le début),
transfert (c'est ce que ça fait à tes clients : le fil s'arrête, la rétention tient), usage (vendre / message),
prix d'avant (plus de 2 000 €, grandes entreprises), bascule (aujourd'hui, même un indépendant), DYOU Agency.
Style agence (moteur/agence.py) : fond sombre, verre dépoli, violet du logo, sous-titres fins.
"""
import math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence

DUREE = 21.7
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresFins(K, fusions={(64, 65, 66): "2 000 €.", (73, 74, 75): "DYOU Agency."})
V, VC = A["violet"], A["violetClair"]


def ressort(v, s=1.6): return rebond(v, s)
def entre(t, t0, d=0.42, s=1.5): return prog(t, t0, d, lambda v: rebond(v, s))
def sort(t, t0, d=0.26): return prog(t, t0, d, entree)


# ─────────────────────────────────────────── écrans
PUBS = [  # (dégradé, image ou icône, accroche)
    (("#8B5CFF", "#3A12B8"), ("img", "produits/electronique/casque-audio"), "NOUVEAU"),
    (("#FF8A3D", "#B8341A"), ("ic", "utensils"), "MENU DU JOUR"),
    (("#2EC4B6", "#0E5E67"), ("ic", "scissors"), "RÉSERVE TA PLACE"),
    (("#4C7DFF", "#1B2C8F"), ("img", "produits/textile/veste-doudoune-bleue"), "COLLECTION HIVER"),
    (("#FF4D8D", "#8E1450"), ("ic", "dumbbell"), "1ʳᵉ SÉANCE OFFERTE"),
]


def degrade(c, x, y, w, h, cols):
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w, y + h)], [hexa(cols[0]), hexa(cols[1])]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), g)


def pub(c, x, y, w, h, t, k, entree_=1.0):
    """une mini-pub animée (ce que DYOU fabrique) : dégradé, objet qui flotte, accroche, bouton"""
    cols, (genre, nom), lab = PUBS[k % len(PUBS)]
    degrade(c, x, y, w, h, cols)
    for j in range(5):                       # formes qui dérivent
        a = t * (0.6 + 0.2 * j) + j
        disque(c, x + w * (0.15 + 0.18 * j) + 30 * math.sin(a), y + h * (0.2 + 0.13 * ((j * 3) % 5)) + 40 * math.cos(a), w * 0.13, "#FFFFFF", 0.07)
    cx, cy = x + w / 2, y + h * 0.43 + 16 * math.sin(t * 3.1)
    s = mix(0.6, 1, entree_)
    if genre == "img":
        iw, ih = taille_img(nom); ww = w * 0.74 * s
        image(c, nom, cx - ww / 2, cy - ww * ih / iw / 2, ww)
    else:
        disque(c, cx, cy, w * 0.27 * s, "#FFFFFF", 0.16)
        icone(c, nom, cx, cy, w * 0.32 * s, "#FFFFFF", 2.2)
    T = w * 0.085
    texte(c, lab, cx, y + h * 0.7, T, "#FFFFFF", "noir", "centre", -0.02, entree_)
    bw, bh = w * 0.56, w * 0.14
    rrect(c, cx - bw / 2, y + h * 0.8, bw, bh, bh / 2, "#FFFFFF", entree_)
    texte(c, "Commander", cx, y + h * 0.8 + bh / 2 - hauteurLigne(w * 0.05, "fort") / 2, w * 0.05, cols[1], "fort", "centre", 0, entree_)


def ecran_pubs(c, x, y, w, h, t, t0=-0.3, dt=0.42):
    """les pubs défilent façon stories : barres en haut, chaque pub glisse sur la précédente"""
    n = len(PUBS)
    k = int(max(0, t - t0) // dt); f = (max(0, t - t0) % dt) / dt
    u = sortie(min(1, f / 0.35))
    pub(c, x, y, w, h, t, k - 1)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x + w * (1 - u), y, w, h))
    pub(c, x + w * (1 - u) * 0.35, y, w, h, t, k, u)
    c.restore()
    bw = (w - 40 - (n - 1) * 6) / n
    for j in range(n):
        rrect(c, x + 20 + j * (bw + 6), y + 26, bw, 5, 2.5, "#FFFFFF", 0.3)
        fill = 1 if j < k % n else (f if j == k % n else 0)
        if fill > 0: rrect(c, x + 20 + j * (bw + 6), y + 26, bw * fill, 5, 2.5, "#FFFFFF", 0.95)


def ecran_fil(c, x, y, w, h, t, t_stop, t_fin):
    """fil d'actualité : posts gris qui défilent vite, puis arrêt net sur la vidéo motion qui se lit jusqu'au bout"""
    ph = h * 0.86; gap = 18; cible = 7
    yc = cible * (ph + gap)
    if t < t_stop:
        off = yc - (t_stop - t) * 1700
    else:
        off = yc + 70 * math.exp(-(t - t_stop) * 9) * math.sin((t - t_stop) * 26)
    for k in range(cible - 9, cible + 2):
        py = y + h * 0.07 + k * (ph + gap) - off
        if py > y + h or py + ph < y: continue
        if k == cible:
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 14, py, w - 28, ph), 26, 26), True)
            pub(c, x + 14, py, w - 28, ph, t, 0)
            # barre de lecture : elle va jusqu'au bout
            pr = borne((t - t_stop) / max(0.1, t_fin - t_stop))
            rrect(c, x + 34, py + ph - 26, w - 68, 8, 4, "#FFFFFF", 0.3)
            rrect(c, x + 34, py + ph - 26, (w - 68) * pr, 8, 4, "#FFFFFF")
            c.restore()
        else:
            cols = [("#4A5A86", "#252C4A"), ("#86504A", "#4A2525"), ("#4A866E", "#254A3C"), ("#86764A", "#4A3F25"), ("#6E4A86", "#3A254A")][k % 5]
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 14, py, w - 28, ph), 26, 26), True)
            degrade(c, x + 14, py, w - 28, ph, cols)
            icone(c, ["image", "shirt", "coffee", "camera", "car"][k % 5], x + w / 2, py + ph * 0.42, w * 0.3, "#FFFFFF", 1.6, 0.35)
            disque(c, x + 60, py + ph - 120, 24, "#FFFFFF", 0.35)
            rrect(c, x + 96, py + ph - 132, w * 0.35, 12, 6, "#FFFFFF", 0.35); rrect(c, x + 96, py + ph - 112, w * 0.22, 10, 5, "#FFFFFF", 0.2)
            rrect(c, x + 34, py + ph - 70, w * 0.6, 14, 7, "#FFFFFF", 0.25)
            c.restore()


# ─────────────────────────────────────────── S1 + S2 · l'accroche
T_REG = TW(7)
CHIPS = [("Boutique", "shopping-bag", -330, -400, -8, -0.30), ("Restaurant", "utensils", 330, -250, 7, -0.18),
         ("Coiffeur", "scissors", -340, 180, 6, 0.30), ("Coach", "dumbbell", 330, 330, -7, 0.55)]


def s1(c, t):
    if t > T_REG + 0.45: return
    z = prog(t, T_REG, 0.42, entree)                     # « Regarde » : on plonge dans l'écran
    cx, cy = 540, 1010
    s = mix(1, 2.6, z); al = 1 - borne((z - 0.55) / 0.45)
    lueur(c, cx, cy, 560 + 150 * (battement(t, TW(1), 0.4, 0.4) - 1), V, 0.45 * al)
    with Espace(c, cx, cy, ry=mix(-16, 0, z) + 3 * math.sin(t * 2.2), rx=mix(6, 0, z), s=s):
        telephone_sombre(c, cx, cy, 500, 1000, lambda cc, a, b, d, e: ecran_pubs(cc, a, b, d, e, t), al)
    for lab, ic, dx, dy, rot, t0 in CHIPS:
        u = entre(t, t0, 0.45, 2.0)
        if u <= 0: continue
        fl = 10 * math.sin(t * 2.4 + dx)
        ex = (dx * 2.2) * z
        pastille_verre(c, lab, cx + dx + ex, cy + dy + fl - 60 * z, 42, ic, borne(u * 2) * al, mix(0.4, 1, u), rot=rot)


def s2(c, t):
    if t < T_REG + 0.1 or t > TW(17) + 0.3: return
    o = sort(t, TW(17) - 0.05, 0.3)
    with Calque(c, 1 - o):
        # « bouge » : trois cartes jaillissent en 3D
        cartes = [(-300, 760, -14, "#FF8A3D", "flame"), (300, 700, 12, "#2EC4B6", "heart"), (0, 640, 0, "#8B5CFF", "sparkles")]
        for k, (dx, y, rz, col, ic) in enumerate(cartes):
            u = entre(t, TW(9) - 0.12 + 0.07 * k, 0.5, 1.4)
            if u <= 0: continue
            cx = 540 + dx * u; cy = y + 18 * math.sin(t * 2 + k) - 400 * o
            with Espace(c, cx, cy, ry=mix(70, 0, u) * (1 if dx >= 0 else -1), rz=rz * u, s=mix(0.3, 1, u)):
                verre(c, cx - 150, cy - 180, 300, 360, 40, 0.08)
                disque(c, cx, cy - 30, 70, col)
                icone(c, ic, cx, cy - 30, 70, "#FFFFFF", 2.4)
                rrect(c, cx - 90, cy + 80, 180, 16, 8, "#FFFFFF", 0.35); rrect(c, cx - 60, cy + 110, 120, 14, 7, "#FFFFFF", 0.2)
        # « claque » : la grande tuile qui s'écrase
        u = prog(t, TW(11) - 0.06, 0.32, lambda v: rebond(v, 2.6))
        if u > 0:
            sx = secousse(t, TW(11) + 0.1, 14)[0]
            s = mix(2.2, 1, u)
            c.save(); c.translate(540 + sx, 1040); c.scale(s, s); c.rotate(-4)
            with Calque(c, borne(u * 3)):
                lueur(c, 0, 0, 420, V, 0.55)
                verre(c, -330, -150, 660, 300, 56, 0.1, violet=0.18)
                icone(c, "zap", -200, 0, 120, "#FFFFFF", 2.4)
                texte(c, "Ça claque.", -110, -hauteurLigne(84) / 2, 84, "#FFFFFF", "noir")
            c.restore()
        # « chaque seconde t'apporte un truc » : la frise des secondes
        u = entre(t, TW(12) - 0.1, 0.4, 1.2)
        if u > 0:
            y = 1360; x0, x1 = 120, 960
            verre(c, x0 - 30, y - 70, x1 - x0 + 60, 140, 70, 0.07)
            ics = ["star", "heart", "flame", "gem", "rocket", "trophy"]
            for j in range(6):
                xj = x0 + 40 + j * (x1 - x0 - 80) / 5
                tj = TW(12) + 0.13 * j
                a = prog(t, tj, 0.3, lambda v: rebond(v, 2.2))
                disque(c, xj, y, 34, "#FFFFFF", 0.12)
                if a > 0:
                    disque(c, xj, y, 34 * a, V)
                    icone(c, ics[j], xj, y, 34 * a, "#FFFFFF", 2.4)
                    yi = y - 120 - 26 * math.sin(min(1, (t - tj) / 0.5) * math.pi)
                texte(c, f"{j + 1}s", xj, y + 50, 22, "#FFFFFF", "fort", "centre", 0, 0.5 * u)
            if u > 0:
                pr = borne((t - TW(12)) / (0.13 * 5 + 0.2))
                trait(c, x0 + 40, y - 52, x0 + 40 + (x1 - x0 - 80) * pr, y - 52, VC, 4, 0.9)


# ─────────────────────────────────────────── S3 · « T'as remarqué ? » le chronomètre
T_CHRONO0 = TW(4) + 0.08          # le chronomètre compte depuis « vidéo » : il affiche 5 sur « cinq »
T_RQ = TW(17)
T_S4 = TW(26)


def chrono(c, cx, cy, R, t, al=1.0):
    sec = max(0.0, t - T_CHRONO0)
    with Calque(c, al):
        lueur(c, cx, cy, R * 1.6, V, 0.4)
        verre(c, cx - R, cy - R, 2 * R, 2 * R, R, 0.07)
        anneau(c, cx, cy, R * 0.82, "#FFFFFF", R * 0.05, 0.12)
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=R * 0.05, StrokeCap=skia.Paint.kRound_Cap)
        p.setShader(skia.GradientShader.MakeSweep(cx, cy, [hexa(VC), hexa(V), hexa(VC)]))
        c.drawArc(skia.Rect.MakeXYWH(cx - R * 0.82, cy - R * 0.82, R * 1.64, R * 1.64), -90, 360 * (sec % 1.0), False, p)
        a = -math.pi / 2 + 2 * math.pi * (sec % 1.0)
        disque(c, cx + R * 0.82 * math.cos(a), cy + R * 0.82 * math.sin(a), R * 0.05, "#FFFFFF")
        s = int(sec)
        b = battement(t, T_CHRONO0 + s, 0.08, 0.25)
        c.save(); c.translate(cx, cy); c.scale(b, b)
        texte_centre(c, f"00:{s:02d}", 0, -R * 0.05, R * 0.36, "#FFFFFF", "noir", track=-0.02)
        c.restore()
        texte(c, "TU REGARDES DEPUIS", cx, cy + R * 0.26, R * 0.075, VC, "fort", "centre", 0.18)


def s3(c, t):
    if t < T_RQ - 0.1 or t > T_S4 + 0.5: return
    u = entre(t, T_RQ - 0.05, 0.5, 1.3)
    m = prog(t, T_S4 - 0.05, 0.45, entreeSortie)          # il part se ranger en haut à droite
    cx, cy, R = mix(540, 850, m), mix(1000, 560, m), mix(330, 120, m)
    with Espace(c, cx, cy, rx=mix(40, 0, u), s=mix(0.5, 1, u)):
        chrono(c, cx, cy, R, t, borne(u * 2) * (1 - sort(t, T_S4 + 0.25, 0.25)))
    ue = entre(t, TW(25) - 0.05, 0.4, 2)
    pastille_verre(c, "Attention captée", 540, 1450 - 20 * m, 42, "eye", borne(ue * 2) * (1 - m), mix(0.5, 1, ue))


# ─────────────────────────────────────────── S4 · tes clients : le fil s'arrête, la rétention tient
T_STOP = TW(33) - 0.02
T_FINR = TW(41)
T_S5 = TW(42)


def courbes(c, x, y, w, h, t, t0):
    verre(c, x, y, w, h, 34, 0.08)
    texte(c, "Rétention", x + 34, y + 28, 30, "#FFFFFF", "gras")
    gx, gy, gw, gh = x + 34, y + 90, w - 68, h - 170
    trait(c, gx, gy + gh, gx + gw, gy + gh, "#FFFFFF", 2, 0.2)
    pr = borne((t - t0) / max(0.1, T_FINR - t0))
    def chemin(f, col, ep, al):
        pth = skia.Path(); n = 40
        for k in range(n + 1):
            v = k / n * pr
            px, py = gx + gw * v, gy + gh * (1 - f(v))
            pth.moveTo(px, py) if k == 0 else pth.lineTo(px, py)
        c.drawPath(pth, peinture(col, al, Style=skia.Paint.kStroke_Style, StrokeWidth=ep, StrokeCap=skia.Paint.kRound_Cap))
        return gx + gw * pr, gy + gh * (1 - f(pr))
    chemin(lambda v: 0.95 * math.exp(-4.2 * v) + 0.03, A["gris"], 6, 0.75)
    ex, ey = chemin(lambda v: 0.96 - 0.12 * v ** 1.6, VC, 8, 1.0)
    lueur(c, ex, ey, 40, VC, 0.6); disque(c, ex, ey, 10, "#FFFFFF")
    yl = y + h - 58
    disque(c, gx + 8, yl, 8, A["gris"]); texte(c, "Vidéo classique", gx + 26, yl - 14, 24, A["gris"], "fort", track=0)
    disque(c, gx + 260, yl, 8, VC); texte(c, "Vidéo motion", gx + 278, yl - 14, 24, "#FFFFFF", "fort", track=0)


def s4(c, t):
    if t < T_S4 - 0.1 or t > T_S5 + 0.4: return
    u = entre(t, T_S4 - 0.05, 0.5, 1.2); o = sort(t, T_S5 - 0.28, 0.24)
    cx, cy = mix(540, 400, prog(t, TW(38) - 0.2, 0.4, sortie)), 1000 + 900 * o
    with Espace(c, cx, cy, ry=mix(30, 8, u) + 2 * math.sin(t * 1.8), s=mix(0.6, 0.92, u), ty=mix(500, 0, u)):
        telephone_sombre(c, cx, cy, 500, 1000, lambda cc, a, b, d, e: ecran_fil(cc, a, b, d, e, t, T_STOP, T_FINR), borne(u * 2) * (1 - o))
    # « tes clients »
    for k, (dx, dy) in enumerate([(-380, -380), (380, -330), (-400, 300)]):
        a = entre(t, TW(31) - 0.1 + 0.08 * k, 0.4, 2) * (1 - prog(t, TW(36), 0.3, entree))
        if a > 0.01:
            x, y = 540 + dx, 1000 + dy + 8 * math.sin(t * 2 + k)
            with Calque(c, borne(a * 2)):
                verre(c, x - 56 * a, y - 56 * a, 112 * a, 112 * a, 56 * a, 0.1)
                icone(c, "user", x, y, 52 * a, "#FFFFFF", 2.2)
    # « ils arrêtent de scroller »
    a = entre(t, T_STOP, 0.4, 2.2) * (1 - prog(t, TW(38) - 0.2, 0.3, entree))
    pastille_verre(c, "Scroll stoppé", 540, 1500, 42, "hand", borne(a * 2), mix(0.4, 1, a))
    # « ils restent jusqu'à la fin »
    a = entre(t, TW(38) - 0.15, 0.45, 1.2)
    if a > 0:
        with Espace(c, 790, 1080, ry=mix(-50, -10, a), s=mix(0.6, 1, a), tx=mix(300, 0, a), ty=900 * o):
            with Calque(c, borne(a * 2) * (1 - o)):
                courbes(c, 560, 900, 470, 360, t, TW(38) - 0.1)
    if t >= T_FINR - 0.05:
        b = entre(t, T_FINR - 0.05, 0.35, 2.4)
        pastille_verre(c, "Jusqu'à la fin", 790, 1330 + 900 * o, 42, "check", borne(b * 2) * (1 - o), mix(0.4, 1, b), accent=A["vert"])


# ─────────────────────────────────────────── S5 · vendre / faire passer un message
T_S6 = TW(52)


def s5(c, t):
    if t < T_S5 - 0.1 or t > T_S6 + 0.4: return
    o = sort(t, T_S6 - 0.05, 0.3)
    u = entre(t, T_S5 - 0.05, 0.4, 2.2)
    if u > 0:
        pastille_verre(c, "Parfait pour", 540, 600 - 300 * o, 42, "sparkles", borne(u * 2) * (1 - o), mix(0.4, 1, u))
    for k, (t0, x, rz, titre, ic) in enumerate([(T_S5 - 0.05, 300, -5, "Vendre un produit", None), (TW(47) - 0.1, 780, 5, "Faire passer un message", "megaphone")]):
        a = entre(t, t0, 0.5, 1.4)
        if a <= 0: continue
        cy = 1060 + 14 * math.sin(t * 2 + k)
        x = x + (900 if k else -900) * o
        with Espace(c, x, cy, ry=mix(60 if k else -60, 0, a), rz=rz, s=mix(0.4, 1, a)):
            with Calque(c, borne(a * 2)):
                verre(c, x - 210, cy - 300, 420, 600, 44, 0.08)
                if k == 0:
                    lueur(c, x, cy - 110, 190, V, 0.5)
                    iw, ih = taille_img("produits/electronique/casque-audio"); ww = 260
                    image(c, "produits/electronique/casque-audio", x - ww / 2, cy - 110 - ww * ih / iw / 2 + 8 * math.sin(t * 3), ww)
                    b = battement(t, TW(46), 0.12, 0.3)
                    c.save(); c.translate(x, cy + 100); c.scale(b, b)
                    rrect(c, -150, -38, 300, 76, 38, V)
                    icone(c, "shopping-bag", -100, 0, 32, "#FFFFFF", 2.4)
                    texte(c, "Au panier", -70, -hauteurLigne(28, "fort") / 2, 28, "#FFFFFF", "fort", track=0)
                    c.restore()
                else:
                    lueur(c, x, cy - 70, 190, "#FF8A3D", 0.4)
                    disque(c, x, cy - 70, 110, "#FF8A3D")
                    icone(c, ic, x, cy - 70, 110, "#FFFFFF", 2.2)
                    for j in range(3):
                        wv = prog(t, TW(51) - 0.1 + 0.08 * j, 0.5, sortie)
                        if wv > 0: anneau(c, x + 30, cy - 70, 120 + 90 * wv + 40 * j, "#FF8A3D", 4, (1 - wv) * 0.8)
                    rrect(c, x - 150, cy + 150, 300, 18, 9, "#FFFFFF", 0.35); rrect(c, x - 110, cy + 186, 220, 16, 8, "#FFFFFF", 0.2)
                texte(c, titre, x, cy + 190 if k == 0 else cy + 70, 34, "#FFFFFF", "gras", "centre", -0.01)


# ─────────────────────────────────────────── S6 · il y a un mois : plus de 2 000 €
T_S7 = TW(67)
T_PRIX = TW(60) - 0.1


def s6(c, t):
    if t < T_S6 - 0.1 or t > T_S7 + 0.9: return
    u = entre(t, T_S6 - 0.05, 0.4, 2)
    mo = prog(t, T_S7 - 0.05, 0.3, entree)
    # calendrier qui remonte d'un mois : grand au centre, puis il monte laisser la place au prix
    with Calque(c, borne(u * 2) * (1 - mo)):
        up = prog(t, TW(57) - 0.1, 0.4, entreeSortie)
        cx, cy, k = 540, mix(960, 620, up) - 200 * mo, mix(1.25, 0.8, up)
        c.save(); c.translate(cx, cy); c.scale(k * mix(0.6, 1, u), k * mix(0.6, 1, u))
        lueur(c, 0, 0, 380, V, 0.35)
        verre(c, -300, -120, 600, 240, 48, 0.09)
        disque(c, -190, 0, 62, V); icone(c, "calendar", -190, 0, 62, "#FFFFFF", 2.4)
        f = prog(t, TW(55) - 0.12, 0.42, lambda v: rebond(v, 1.3))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(-110, -80, 390, 160))
        texte(c, "Octobre", -100, -hauteurLigne(64) / 2 - 130 * f, 64, "#FFFFFF", "noir")
        texte(c, "Septembre", -100, -hauteurLigne(64) / 2 + 130 * (1 - f), 64, "#FFFFFF", "noir")
        c.restore()
        c.restore()
    # le prix qui grimpe
    a = entre(t, TW(60) - 0.1, 0.45, 1.4)
    if a > 0:
        cx, cy = 540, 1050
        crash = prog(t, T_S7, 0.6, entree)
        sx = secousse(t, TW(66), 18)[0]
        with Espace(c, cx + sx, cy + 1300 * crash ** 1.5, rx=mix(50, 0, a), rz=-14 * crash, s=mix(0.5, 1, a)):
            with Calque(c, borne(a * 2)):
                lueur(c, cx, cy, 480, "#FFB020", 0.25 * (1 - crash))
                verre(c, cx - 400, cy - 200, 800, 400, 56, 0.09)
                v = int(2000 * sortie(prog(t, T_PRIX, TW(66) - T_PRIX + 0.05, lin)))
                lab = f"{v:,}".replace(",", " ") + " €"
                texte(c, "+", cx - largeur(lab, 150) / 2 - 70, cy - hauteurLigne(150) / 2 - 6, 110, VC, "noir")
                texte(c, lab, cx, cy - hauteurLigne(150) / 2 - 20, 150, "#FFFFFF", "noir", "centre", -0.04)
                texte(c, "une vidéo motion", cx, cy + 90, 32, A["gris"], "demi", "centre", 0)
                # le barré de la bascule
                b = prog(t, T_S7 + 0.02, 0.22, sortie)
                if b > 0: trait(c, cx - 300, cy + 40, cx - 300 + 600 * b, cy - 70, A["rouge"], 14, 1.0)
    g = entre(t, TW(61) - 0.05, 0.4, 2) * (1 - mo)
    if g > 0:
        pastille_verre(c, "Grandes entreprises", 540, 1390, 42, "building-2", borne(g * 2), mix(0.4, 1, g))
        if t > TW(61):
            icone(c, "lock", 540 + 230, 1300, 44, VC, 2.4, borne(g * 2))


# ─────────────────────────────────────────── S7 · aujourd'hui, même un indépendant
T_LOGO = TW(73) - 0.12
T_CTA = TW(76) - 0.1


def s7(c, t):
    if t < T_S7 - 0.1 or t > T_LOGO + 0.4: return
    u = entre(t, T_S7 - 0.05, 0.45, 2)
    with Calque(c, borne(u * 2)):
        cx, cy = 540, 700
        lueur(c, cx, cy, 280, A["vert"], 0.25)
        verre(c, cx - 110, cy - 110, 220, 220, 110, 0.08)
        ouv = t > T_S7 + 0.25
        b = battement(t, T_S7 + 0.25, 0.15, 0.3)
        icone(c, "lock-open" if ouv else "lock", cx, cy, 110 * b, A["vert"] if ouv else "#FFFFFF", 2.4)
        onde(c, cx, cy, t, T_S7 + 0.25, 110, 330, A["vert"], 6)
    profils = [("Indépendant", "laptop", TW(70) - 0.12, -1), ("Artisan", "hammer", TW(71) - 0.1, 1), ("Petit commerce", "store", TW(72) - 0.1, -1)]
    for k, (lab, ic, t0, sgn) in enumerate(profils):
        a = entre(t, t0, 0.42, 2.2)
        if a <= 0: continue
        y = 980 + k * 170 + 6 * math.sin(t * 2.4 + k)
        w = pastille_verre(c, lab, 540 + sgn * 60 * (1 - a), y, 44, ic, borne(a * 2), mix(0.4, 1, a))
        ch = prog(t, t0 + 0.2, 0.3, lambda v: rebond(v, 2.4))
        if ch > 0 and w:
            disque(c, 540 + w / 2 + 34, y, 30 * ch, A["vert"]); icone(c, "check", 540 + w / 2 + 34, y, 34 * ch, "#FFFFFF", 3)
    confettis(c, 540, 1150, t, TW(72), 26, 420, 4, cols=[V, VC, "#FFFFFF", A["violetPale"], A["vert"]])


# ─────────────────────────────────────────── sons
son(0.0, "impact", -6); son(0.0, "whoosh_court", -12)
for _, _, _, _, _, t0 in CHIPS: son(max(0, t0), "pop", -14)
for k in range(1, 5): son(-0.3 + 0.42 * k, "swipe", -16)
son(TW(1), "verre", -13); son(T_REG, "whoosh_long", -10)
for k in range(3): son(TW(9) - 0.12 + 0.07 * k, "whoosh_court", -13)
son(TW(11) - 0.02, "impact", -5); son(TW(11), "tampon", -9)
for j in range(6): son(TW(12) + 0.13 * j, "tick", -12); son(TW(12) + 0.13 * j + 0.01, "pop", -17)
son(T_RQ - 0.05, "whoosh_bas", -9); son(T_RQ + 0.1, "impact_doux", -9)
for s_ in range(3, 8): son(T_CHRONO0 + s_, "tick", -11)
son(TW(21), "ding", -10); son(TW(25) - 0.05, "pop", -12)
son(T_S4 - 0.05, "whoosh", -11)
for k in range(3): son(TW(31) - 0.1 + 0.08 * k, "pop", -15)
for k in range(8): son(T_S4 + 0.2 + 0.2 * k, "swipe", -20)
son(T_STOP, "clic", -8); son(T_STOP + 0.02, "impact_doux", -10)
son(TW(38) - 0.15, "whoosh_court", -12); son(T_FINR - 0.05, "check", -10)
son(T_S5 - 0.05, "pop", -11); son(TW(44) - 0.1, "whoosh_court", -12); son(TW(46), "ching", -12)
son(TW(49) - 0.1, "whoosh_court", -12); son(TW(51) - 0.1, "montee", -16)
son(T_S6 - 0.05, "swipe", -12); son(TW(55) - 0.1, "clic", -11)
son(TW(60) - 0.1, "whoosh", -11); son(T_PRIX, "montee", -11)
for k in range(10): son(T_PRIX + k * (TW(66) - T_PRIX) / 10, "tick", -17)
son(TW(66), "impact", -6); son(TW(61) - 0.05, "pop", -13)
son(T_S7 - 0.05, "verre", -9); son(T_S7 + 0.02, "whoosh_court", -10); son(T_S7 + 0.25, "clic", -9)
for _, _, t0, _ in [("", "", TW(70) - 0.12, 0), ("", "", TW(71) - 0.1, 0), ("", "", TW(72) - 0.1, 0)]:
    son(t0, "pop", -12); son(t0 + 0.2, "check", -14)
son(TW(72), "ching", -11)
son(T_LOGO - 0.1, "montee", -14); son(T_LOGO + 0.24, "impact", -6); son(T_LOGO + 0.26, "verre", -9)
son(T_CTA, "whoosh", -12); son(T_CTA + 0.3, "pop", -10)

for a, b in [(T_REG, T_REG + 0.42), (TW(9) - 0.12, TW(9) + 0.25), (TW(11) - 0.06, TW(11) + 0.15), (T_RQ - 0.1, T_RQ + 0.3),
             (T_S4 - 0.05, T_STOP), (T_S5 - 0.1, T_S5 + 0.3), (T_S6 - 0.1, T_S6 + 0.3), (T_S7, T_S7 + 0.6),
             (T_LOGO, T_LOGO + 0.35), (T_CTA - 0.1, T_CTA + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(11), V, 0.18), (T_RQ, "#FFFFFF", 0.08), (TW(21), V, 0.12), (T_STOP, "#FFFFFF", 0.1),
                    (TW(66), "#FFB020", 0.12), (T_S7 + 0.25, A["vert"], 0.1), (T_LOGO + 0.24, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, TW(11), 1, 0.5) + battement(t, TW(66), 1, 0.5) - 2)
    if t < T_LOGO + 0.45:
        s1(c, t); s2(c, t); s3(c, t); s4(c, t); s5(c, t); s6(c, t); s7(c, t)
    r = disque_logo(c, t, T_LOGO, T_CTA)
    carton_agence(c, t, T_CTA + 0.25)
    K.dessine_eclairs(c, t)
    if t < T_LOGO + 0.15: SOUS.dessine(c, t)
