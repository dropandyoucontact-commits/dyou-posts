"""DY-M04 « 100 vestes du Brésil » — habillage d'une vidéo tournée pour DROP&YOU (14/10/2026).

Vidéo fournie par Youssef (18,4 s, 1080×1920, 30 i/s) : hook de la caméra qui tombe (0 → 0,93 s, intact),
puis le gars aux cheveux rouges parle face caméra. Demande : « juste des sous-titres stylés avec des petites
animations, comme lui (les numéros qui défilent), cohérents avec ce que dit la vidéo, au bon moment, et rien si
ça ne le nécessite pas » ; une image plus claire et plus propre ; un son plus fort et net. Référence : un Reel
podmax.studio (sous-titres en capitales condensées blanches, compteur qui défile) — sans l'écran du bas.

    python3 montage.py apercu 1.3 4.4 …   → apercus/m_<t>.jpg et apercus/planche_montage.jpg
    python3 montage.py video              → renders/image.mp4 (sans son)
    python3 montage.py son                → audio/voix.wav (voix nettoyée) + video/DY-M04.mp4
"""
import json, math, pathlib, subprocess, sys
import numpy as np, skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
moteur.PROJET = P
from moteur import (hexa, borne, mix, prog, sortie, sortieExpo, entree, entreeSortie, rebond, ressort, texte, largeur,
                    hauteurLigne, peinture, disque, anneau, trait, icone, image, taille_img, Calque, rrect, drapeau, onde, etoile)
from kit import logo_app, logo_glyphe

W, H, FPS = 1080, 1920, 30
SRC = P / "media" / "source.mov"
DUREE = 18.4
N = int(DUREE * FPS)
T_HOOK = 0.93                       # fin du hook (caméra qui tombe) : rien avant
GRADE = "eq=contrast=1.07:saturation=1.12:gamma=0.97,unsharp=5:5:0.5:5:5:0.0"   # un peu plus de contraste, de couleur et de netteté
_ECH = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)
SFX = []

moteur._prov.registerTypeface(skia.Typeface.MakeFromFile(str(P / "media" / "Anton-Regular.ttf")), "Anton")
moteur._FAM["anton"] = "Anton"
F = "anton"


def son(t, nom, gain):
    SFX.append((round(t, 3), nom, gain))


# ─────────────────────────────────────────── mots (whisper, découpé phrase par phrase)
MOTS = [w for w in json.load(open(P / "media" / "mots-seg.json")) if w[2] not in ("?", "bien.")]
T = [w[0] for w in MOTS]
T[44] = 10.82                       # « Ah » : whisper le colle au début du morceau, la parole reprend à 10,82 s
T[0] = 0.95

# blocs de sous-titres : (indices des mots, texte affiché mot par mot, mots mis en avant)
BLOCS = [
    (range(0, 3), ["J'AI", "100", "VESTES"], {"100"}),
    (range(3, 5), ["DU", "BRÉSIL"], {"BRÉSIL"}),
    (range(5, 8), ["DANS", "LES", "MAINS"], set()),
    (range(8, 11), ["À", "TON", "AVIS,"], set()),
    (range(11, 16), ["SI", "TU", "M'EN", "PRENDS", "AUTANT,"], {"AUTANT,"}),
    (range(16, 20), ["JE", "TE", "LES", "FAIS"], set()),
    (range(20, 22), ["À", "COMBIEN ?"], {"COMBIEN ?"}),
    (range(22, 24), ["À", "L'UNITÉ"], {"L'UNITÉ"}),
    (range(24, 27), ["OU", "EN", "LOT ?"], {"LOT ?"}),
    (range(27, 30), ["C'EST", "DISPO", "CHEZ"], set()),
    (range(31, 34), ["AJOUTE-MOI", "SUR", "SNAP"], {"SNAP"}),
    (range(34, 38), ["OU", "METS-LE", "EN", "COMMENTAIRE"], set()),
    (range(38, 41), ["ET", "JE", "T'AJOUTE"], set()),
    (range(41, 44), ["AVEC", "MON", "COMPTE."], set()),
    (range(44, 50), ["AH", "OUI,", "ET", "AU", "CAS", "OÙ,"], set()),
    (range(50, 54), ["ON", "FAIT", "DU", "SOURCING"], {"SOURCING"}),
    (range(54, 56), ["EN", "CHINE,"], {"CHINE,"}),
    (range(56, 61), ["DONC", "SI", "TU", "AS", "BESOIN"], set()),
    (range(61, 65), ["DE", "QUOI", "QUE", "CE", "SOIT"], set()),
    (range(68, 73), ["TU", "ME", "CONTACTES", "EN", "PRIVÉ"], {"PRIVÉ"}),
    (range(73, 79), ["QUE", "CE", "SOIT", "POUR", "DU", "DÉTAIL"], {"DÉTAIL"}),
    (range(79, 82), ["OU", "DU", "LOT,"], {"LOT,"}),
    (range(82, 84), ["ON", "S'ARRANGE"], set()),
    (range(84, 89), ["SELON", "LA", "QUALITÉ", "DES", "PRODUITS."], {"QUALITÉ"}),
]
# « de quoi que ce soit » : indices 61-64 (« de quoi que soit » chez whisper, « ce » ajouté au temps de « que »)
BLOCS[18] = (None, [("DE", T[61]), ("QUOI", T[62]), ("QUE", T[63]), ("CE", T[63] + 0.05), ("SOIT", T[64])], set())

T_LOGO = T[30] - 0.04               # « DROP&YOU » : le logo remplace le mot
T_LISTE = [T[65], T[66], T[67]]     # textile, électronique, motos Surron : la liste remplace les sous-titres
Y_SOUS = 1290
TAILLE = 104
LARG = 900


ASC = moteur._para("H", "Anton", 100.0, 0xFF000000, 0.0).AlphabeticBaseline / 100.0


def _mise(bloc):
    idx, mots, forts = bloc
    if idx is None: items = [(m, t) for m, t in mots]
    else: items = [(m, T[i]) for m, i in zip(mots, idx)]
    taille = TAILLE
    while True:
        esp = taille * 0.24
        lignes, cur, lw = [], [], 0.0
        for m, t in items:
            tm = taille * (1.16 if m in forts else 1.0)
            w = largeur(m, tm, F, 0.0) if m != "100" else 3 * largeur("0", tm, F, 0.0)   # le compteur : 3 rouleaux de la largeur d'un 0
            if cur and lw + esp + w > LARG:
                lignes.append((cur, lw)); cur, lw = [], 0.0
            cur.append((m, t, tm, w)); lw += (esp if len(cur) > 1 else 0) + w
        lignes.append((cur, lw))
        if len(lignes) <= 2 or taille <= 80: break
        taille -= 6
    pos, y = [], Y_SOUS - (len(lignes) - 1) * taille * 0.62
    for ligne, lw in lignes:
        x = 540 - lw / 2
        tmax = max(tm for _, _, tm, _ in ligne)
        for m, t, tm, w in ligne:
            yb = y + ASC * (tmax - tm)          # même ligne de base pour les mots agrandis
            pos.append(dict(m=m, t=t, taille=tm, x=x, y=yb, w=w)); x += w + esp
        y += taille * 1.22
    return pos


MISES = [_mise(b) for b in BLOCS]
for k, pos in enumerate(MISES):
    pos[0]["fin"] = None
DEBUTS = [p[0]["t"] for p in MISES]


def fin_bloc(k):
    if k == 9: return T_LOGO                       # « chez » → le logo prend la place
    if k == 18: return T_LISTE[0] - 0.05           # la liste prend la place
    if k == len(MISES) - 1: return DUREE + 1
    return DEBUTS[k + 1] - 0.03


def ombre_texte(c):
    p = skia.Paint(ImageFilter=skia.ImageFilters.DropShadow(0, 6, 9, 9, hexa("#000000", 0.62)))
    c.saveLayer(None, p)


def chiffres_rouleau(c, cible, x, y, taille, t, t0, t1, couleur="#FFFFFF"):
    """compteur qui défile (chaque chiffre est un rouleau) de 000 à `cible`"""
    s = str(cible); n = len(s)
    u = borne((t - t0) / max(0.05, t1 - t0))
    hl = taille * 1.2
    wd = largeur("0", taille, F, 0.0)
    xx = x
    for k, ch in enumerate(s):
        tours = (n - k) * 10 + int(ch)          # les unités tournent plus vite que les centaines
        v = ressort(u, 1.3, 4.0) if u < 1 else 1.0
        pos = tours * min(1.04, v)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(xx - 6, y - taille * 0.05, wd + 12, hl))
        for j in range(int(pos) - 1, int(pos) + 2):
            d = (j - pos) * hl
            ch_ = str(j % 10)
            texte(c, ch_, xx + (wd - largeur(ch_, taille, F, 0.0)) / 2, y + d, taille, couleur, F, track=0.0)
        c.restore()
        xx += wd
    return xx - x


def sous_titres(c, t):
    for k, pos in enumerate(MISES):
        t_deb, t_fin = pos[0]["t"] - 0.04, fin_bloc(k)
        if t < t_deb or t > t_fin + 0.1 or t < T_HOOK: continue
        o = prog(t, t_fin, 0.08, entree)
        ombre_texte(c)
        for m in pos:
            if t < m["t"] - 0.04: continue
            u = prog(t, m["t"] - 0.04, 0.2, lambda v: rebond(v, 2.2))
            s = mix(0.55, 1.0, u) * (1 - 0.15 * o)
            cx, cy = m["x"] + m["w"] / 2, m["y"] + m["taille"] * 0.6
            c.save(); c.translate(cx, cy - 18 * o); c.scale(s, s); c.translate(-cx, -cy)
            al = borne(u * 3) * (1 - o)
            if m["m"] == "100":
                with Calque(c, al):
                    chiffres_rouleau(c, 100, m["x"], m["y"], m["taille"], t, m["t"] - 0.02, m["t"] + 0.45)
            else:
                texte(c, m["m"], m["x"], m["y"], m["taille"], "#FFFFFF", F, track=0.0, alpha=al)
            c.restore()
        c.restore()


# ─────────────────────────────────────────── petites animations, seulement où le texte en appelle une
def pop(t, t0, d=0.3, s=1.9):
    return prog(t, t0, d, lambda v: rebond(v, s))


def ombre_douce(c, rr, opa=0.35):
    p = skia.Paint(AntiAlias=True, Color=hexa("#000000", opa), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
    c.save(); c.translate(0, 10); c.drawRRect(rr, p); c.restore()


def drapeau_bresil(c, x, y, w, h):
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 8, 8), doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#009C3B"))
    p = skia.Path(); p.moveTo(x + w / 2, y + h * 0.1); p.lineTo(x + w * 0.92, y + h / 2); p.lineTo(x + w / 2, y + h * 0.9); p.lineTo(x + w * 0.08, y + h / 2); p.close()
    c.drawPath(p, peinture("#FFDF00"))
    c.drawCircle(x + w / 2, y + h / 2, h * 0.24, peinture("#002776"))
    c.restore()


def sticker_drapeau(c, t, pays, t0, t1, cx, cy, rot):
    a = pop(t, t0) * (1 - prog(t, t1, 0.12, entree))
    if a <= 0: return
    c.save(); c.translate(cx, cy + 6 * math.sin(t * 5)); c.rotate(rot + 4 * math.sin(t * 3)); c.scale(a, a)
    w, h = 132, 92
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 - 8, -h / 2 - 8, w + 16, h + 16), 18, 18)
    ombre_douce(c, rr); c.drawRRect(rr, peinture("#FFFFFF"))
    if pays == "BR": drapeau_bresil(c, -w / 2, -h / 2, w, h)
    else: drapeau(c, pays, -w / 2, -h / 2, w, h, 8)
    c.restore()


_RNG = np.random.default_rng(4)


def etiquette_prix(c, t):
    """« je te les fais à combien ? » : une étiquette dont les chiffres tournent sans s'arrêter, puis « ?? € »"""
    t0, t_q, t1 = T[15] - 0.05, T[21] + 0.25, T[22] - 0.12      # « autant » → « combien » → fin de la pause
    a = pop(t, t0, 0.4, 1.6) * (1 - prog(t, t1, 0.15, entree))
    if a <= 0: return
    cx, cy = 872, 520
    c.save(); c.translate(cx, cy + 8 * math.sin(t * 4)); c.rotate(-8 + 3 * math.sin(t * 2.6)); c.scale(0.86 * a, 0.86 * a)
    w, h = 330, 190
    pth = skia.Path(); r = 22
    pth.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 40, -h / 2, w - 40, h), r, r))
    pth.moveTo(-w / 2 + 44, -h / 2 + 4); pth.lineTo(-w / 2, 0); pth.lineTo(-w / 2 + 44, h / 2 - 4); pth.close()
    p = skia.Paint(AntiAlias=True, Color=hexa("#000000", 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
    c.save(); c.translate(0, 10); c.drawPath(pth, p); c.restore()
    c.drawPath(pth, peinture("#FFFFFF"))
    disque(c, -w / 2 + 34, 0, 13, "#1A1A1A")
    texte(c, "PRIX À L'UNITÉ", 10, -h / 2 + 22, 26, "#1A1A1A", F, "centre", 0.06)
    # chiffres qui tournent
    ty = -h / 2 + 62; taille = 92; hl = taille * 1.2
    wd = largeur("0", taille, F, 0.0)
    xx = 10 - (2 * wd + largeur(" €", taille, F, 0.0)) / 2
    for k in range(2):
        c.save(); c.clipRect(skia.Rect.MakeXYWH(xx - 4, ty - 4, wd + 8, hl))
        if t < t_q:
            pos = (t - t0) * (22 + 9 * k) + k * 3.3
            for j in range(int(pos) - 1, int(pos) + 2):
                texte(c, str(j % 10), xx, ty + (j - pos) * hl, taille, "#1A1A1A", F, track=0.0)
        else:
            u = prog(t, t_q + 0.06 * k, 0.3, lambda v: rebond(v, 2.0))
            texte(c, "?", xx + wd * 0.18, ty + hl * (1 - u), taille, "#E5484D", F, track=0.0)
        c.restore()
        xx += wd
    texte(c, " €", xx, ty, taille, "#1A1A1A", F, track=0.0)
    c.restore()


def logo_dropandyou(c, t):
    """« chez DROP&YOU » : le logo prend la place du mot"""
    t0, t1 = T_LOGO, T[31] - 0.05
    a = pop(t, t0, 0.32, 1.7) * (1 - prog(t, t1, 0.12, entree))
    if a <= 0: return
    iw, ih = taille_img("logo-dy-blanc"); lw = 760; lh = lw * ih / iw
    c.save(); c.translate(540, Y_SOUS + 40); c.scale(mix(1.6, 1, a) * a, mix(1.6, 1, a) * a)
    p = skia.Paint(ImageFilter=skia.ImageFilters.DropShadow(0, 8, 14, 14, hexa("#000000", 0.6)))
    c.saveLayer(None, p)
    image(c, "logo-dy-blanc", -lw / 2, -lh / 2, lw)
    c.restore()
    c.restore()


def icone_bulle(c, t, t0, t1, cx, cy, quoi):
    """petite icône qui accompagne un mot : Snap, commentaire, Chine, message privé"""
    a = pop(t, t0, 0.3, 2.2) * (1 - prog(t, t1, 0.1, entree))
    if a <= 0: return
    c.save(); c.translate(cx, cy + 5 * math.sin(t * 5)); c.rotate(6 * math.sin(t * 3)); c.scale(a, a)
    if quoi == "snap":
        logo_app(c, "snapchat", 0, 0, 120)
    elif quoi == "commentaire":
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -54, 160, 108), 40, 40)
        ombre_douce(c, rr); c.drawRRect(rr, peinture("#FFFFFF"))
        q = skia.Path(); q.moveTo(-40, 46); q.lineTo(-62, 74); q.lineTo(-10, 50); q.close(); c.drawPath(q, peinture("#FFFFFF"))
        for k in range(3):
            b = 0.5 + 0.5 * math.sin(t * 9 - k * 0.9)
            disque(c, -36 + 36 * k, 0 - 8 * b, 11, "#1A1A1A", 0.5 + 0.5 * b)
    elif quoi == "prive":
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-60, -60, 120, 120), 60, 60)
        ombre_douce(c, rr); c.drawRRect(rr, peinture("#FFFFFF"))
        icone(c, "send", -3, 3, 62, "#1A1A1A", 2.4)
        disque(c, 44, -44, 18, "#E5484D"); texte(c, "1", 44, -44 - hauteurLigne(24, "titre") / 2, 24, "#FFFFFF", "titre", "centre", 0)
    c.restore()


LISTE = [("TEXTILE", "shirt"), ("ÉLECTRONIQUE", "smartphone"), ("MOTOS SURRON", "bike")]


def liste_produits(c, t):
    """« textile, électronique, motos Surron » : trois lignes qui tombent une à une à la place des sous-titres"""
    t1 = T[68] - 0.05
    if t < T_LISTE[0] - 0.05 or t > t1 + 0.15: return
    o = prog(t, t1, 0.12, entree)
    for k, ((lab, ic), t0) in enumerate(zip(LISTE, T_LISTE)):
        a = prog(t, t0 - 0.04, 0.32, lambda v: rebond(v, 1.8))
        if a <= 0: continue
        y = 1150 + k * 128
        taille = 76
        tw = largeur(lab, taille, F, 0.0)
        w = tw + 150; h = 106
        x = 540 - w / 2 + (1 - a) * (-260 if k % 2 == 0 else 260)
        with Calque(c, borne(a * 3) * (1 - o)):
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - h / 2, w, h), h / 2, h / 2)
            ombre_douce(c, rr, 0.4); c.drawRRect(rr, peinture("#FFFFFF"))
            disque(c, x + 56, y, 38, "#1A1A1A"); icone(c, ic, x + 56, y, 40, "#FFFFFF", 2.2)
            texte(c, lab, x + 108, y - hauteurLigne(taille, F) / 2, taille, "#1A1A1A", F, track=0.0)


def filigrane(c, t):
    """petit logo DROP&YOU en haut, discret, effacé quand le grand logo est à l'écran"""
    a = prog(t, T_HOOK + 0.1, 0.4) * (1 - 0.999 * (prog(t, T_LOGO - 0.1, 0.15) - prog(t, T[31], 0.2)))
    if a <= 0.01: return
    iw, ih = taille_img("logo-dy-blanc"); lw = 260
    p = skia.Paint(ImageFilter=skia.ImageFilters.DropShadow(0, 3, 6, 6, hexa("#000000", 0.5))); p.setAlphaf(0.92 * a)
    c.saveLayer(None, p)
    image(c, "logo-dy-blanc", 540 - lw / 2, 250, lw)
    c.restore()


# ─────────────────────────────────────────── l'image : léger travelling par plan, petit coup de zoom sur les mots forts
PLANS = [(0.0, 0.93), (0.93, 5.0), (5.0, 5.77), (5.77, 10.8), (10.8, 18.4)]
COUPS = [T[1], T[21], T_LOGO, T[55], T[72]]          # 100, combien, DROP&YOU, Chine, privé


def zoom(t):
    if t < T_HOOK: return 1.0, 540, 900
    a, b = next((a, b) for a, b in PLANS if a <= t < b + 1e-6) if t < 18.4 else PLANS[-1]
    s = 1.0 + 0.035 * borne((t - a) / (b - a))
    for tc in COUPS:
        if tc - 0.02 <= t <= tc + 0.5:
            u = (t - tc + 0.02) / 0.52
            s += 0.045 * math.sin(math.pi * min(1, u * 2.2)) if u < 0.45 else 0.045 * max(0, 1 - (u - 0.45) / 0.55) ** 2
    return s, 540, 820


def dessine(c, t, img):
    s, cx, cy = zoom(t)
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy)
    c.drawImageRect(img, skia.Rect.MakeWH(W, H), _ECH, skia.Paint())
    c.restore()
    if t < T_HOOK: return
    sticker_drapeau(c, t, "BR", T[4] - 0.03, T[5] - 0.05, 860, Y_SOUS - 150, 8)
    etiquette_prix(c, t)
    logo_dropandyou(c, t)
    icone_bulle(c, t, T[33] - 0.03, T[34] - 0.05, 900, Y_SOUS - 140, "snap")
    icone_bulle(c, t, T[37] - 0.03, T[38] - 0.05, 880, Y_SOUS - 170, "commentaire")
    sticker_drapeau(c, t, "CN", T[55] - 0.03, T[56] - 0.05, 860, Y_SOUS - 150, -7)
    icone_bulle(c, t, T[72] - 0.03, T[73] - 0.05, 880, Y_SOUS - 170, "prive")
    liste_produits(c, t)
    sous_titres(c, t)


# ─────────────────────────────────────────── sons (discrets : la voix reste devant)
son(T[1], "montee", -22)
for k in range(8): son(T[1] + 0.05 * k, "tick", -24)
son(T[4] - 0.03, "pop", -18)
son(T[15] - 0.05, "pop", -18)
for k in range(14): son(T[15] + 0.08 * k, "tick", -26)
son(T[21] + 0.25, "clic", -18)
son(T_LOGO, "whoosh_court", -18); son(T_LOGO + 0.05, "ching", -19)
son(T[33] - 0.03, "pop", -18); son(T[37] - 0.03, "message_in", -20)
son(T[55] - 0.03, "pop", -18)
for t0 in T_LISTE: son(t0 - 0.04, "whoosh_court", -20); son(t0, "pop", -19)
son(T[72] - 0.03, "message", -20)


# ─────────────────────────────────────────── lecture, aperçus, rendu
def lecteur():
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(SRC), "-vf", GRADE, "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
    taille = W * H * 4
    while True:
        b = pr.stdout.read(taille)
        if len(b) < taille: break
        yield b
    pr.wait()


def image_a(t, buf):
    img = skia.Image.fromarray(np.frombuffer(buf, np.uint8).reshape(H, W, 4), colorType=skia.kRGBA_8888_ColorType)
    s = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    dessine(s.getCanvas(), t, img)
    return s.toarray()


def apercu(temps):
    from PIL import Image
    (P / "apercus").mkdir(exist_ok=True)
    vign = []
    for t in temps:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(SRC), "-frames:v", "1", "-vf", GRADE,
                              "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True).stdout
        a = image_a(t, raw)
        im = Image.fromarray(a[..., :3]); im.save(P / "apercus" / f"m_{t:05.2f}.jpg", quality=88)
        vign.append((t, im.resize((270, 480))))
    cols = min(5, len(vign)); lig = (len(vign) + cols - 1) // cols
    pl = Image.new("RGB", (cols * 272, lig * 482), (30, 30, 30))
    from PIL import ImageDraw
    d = ImageDraw.Draw(pl)
    for k, (t, im) in enumerate(vign):
        x, y = (k % cols) * 272 + 1, (k // cols) * 482 + 1
        pl.paste(im, (x, y)); d.text((x + 5, y + 4), f"{t:.2f}", fill=(255, 0, 0))
    pl.save(P / "apercus" / "planche_montage.jpg", quality=85)


def video():
    (P / "renders").mkdir(exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(P / "renders" / "image.mp4")],
                           stdin=subprocess.PIPE)
    for k, buf in enumerate(lecteur()):
        if k >= N: break
        enc.stdin.write(image_a(k / FPS, buf).tobytes())
        if k % 60 == 0: print(f"{k / FPS:.1f} s", flush=True)
    enc.stdin.close(); enc.wait()


def mixage():
    """voix d'origine (déjà écrêtée à 0 dB) : réparation des écrêtages, coupe des graves, débruitage léger, présence,
    compression douce, gain et limiteur à −1 dB ; puis bruitages discrets dessous"""
    (P / "audio").mkdir(exist_ok=True)
    voix = P / "audio" / "voix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-vn", "-af",
                    "adeclip=w=55:o=75:a=8:t=10:n=1000,highpass=f=75,afftdn=nr=8:nf=-30,"
                    "equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3800:t=q:w=1.0:g=2.5,equalizer=f=9000:t=h:w=0.7:g=1.5,"
                    "acompressor=threshold=0.18:ratio=2.5:attack=4:release=90:makeup=1.6,volume=4dB",
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_f32le", str(voix)], check=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(voix), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    for t0, nom, g in SFX:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(P.parent / "moteur" / "sons" / f"{nom}.wav"), "-ac", "1", "-ar", "48000",
                            "-f", "f32le", "-"], capture_output=True).stdout
        s = np.frombuffer(r, np.float32) * 10 ** (g / 20)
        i0 = int(t0 * 48000); i1 = min(len(x), i0 + len(s))
        if i0 < len(x): x[i0:i1] += s[:i1 - i0]
    mix = P / "audio" / "mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", "-af",
                    "volume=1.5dB,alimiter=limit=0.7:attack=1:release=50:level=false,pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", str(mix)],
                   input=x.tobytes(), check=True)
    (P / "video").mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "renders" / "image.mp4"), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                    str(P / "video" / "DY-M04.mp4")], check=True)


if __name__ == "__main__":
    if sys.argv[1] == "apercu": apercu([float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == "video": video()
    elif sys.argv[1] == "son": mixage()
