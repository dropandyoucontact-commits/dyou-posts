"""DY-M03 « À la source » — habillage d'une vidéo tournée (pas de voix, pas de motion design explicatif).

Vidéo fournie par Youssef (18,8 s, 1920×1080, 30 i/s, musique + compte à rebours déjà incrusté) :
départ → usine de motos électriques → bijouterie → entrepôt de baskets → vêtements → marché électronique.
On garde la vidéo intacte et on pose dessus, en verre fumé comme les panneaux de DY-M02 :
  · une pastille DROP&YOU en haut à gauche, un indicateur de chapitre en haut à droite ;
  · une phrase en grand sur les plans flous (3,1 s et 11,4 s) ;
  · une carte de chapitre en bas à gauche par lieu ;
  · des repères accrochés aux objets (suivi.py : flux optique) avec une étiquette ;
  · un carton de fin de 3 s sur la dernière image figée (Snap + WhatsApp).

    python3 montage.py apercu 3.6 5.0 …   → apercus/m_<t>.jpg et apercus/planche_montage.jpg
    python3 montage.py video              → renders/image.mp4 (sans son) puis video/DY-M03.mp4
"""
import json, math, pathlib, subprocess, sys
import numpy as np, cv2, skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
moteur.PROJET = P
from moteur import (hexa, borne, mix, prog, sortie, entree, entreeSortie, rebond, texte, largeur, hauteurLigne,
                    peinture, disque, anneau, trait, icone, image, taille_img, Calque, matrice3d)
from kit import texte_centre, logo_glyphe, MARQUES

W, H, FPS = 1920, 1080, 30
SRC = P / "media" / "source.mov"
FIN_SRC = 18.8                     # fin de la vidéo fournie
T_FIN = 18.55                      # le carton de fin commence (flou qui monte)
DUREE = 21.9
N = round(DUREE * FPS)
LILAS, VIOLET, VOILE = "#B9A3FF", "#7C3AED", "#0D0A16"
_ECH = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)
FOND = [None]                      # image floutée courante (le verre la montre derrière lui)
SFX = []


def son(t, nom, gain):
    SFX.append((round(t, 3), nom, gain))


# ─────────────────────────────────────────── verre fumé
def verre(c, x, y, w, h, r, voile=0.46, ombre=True, lisere=0.32):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    if ombre:
        p = skia.Paint(AntiAlias=True, Color=hexa("#05030A", 0.34), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
        c.save(); c.translate(0, 18); c.drawRRect(rr, p); c.restore()
    c.save(); c.clipRRect(rr, doAntiAlias=True)
    c.save(); c.resetMatrix()
    c.drawImageRect(FOND[0], skia.Rect.MakeWH(W, H), _ECH, skia.Paint())
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(VOILE, voile))
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.35, y + h)],
                                               [hexa("#FFFFFF", 0.15), hexa("#FFFFFF", 0.03), hexa("#FFFFFF", 0.0)], [0.0, 0.45, 1.0]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), g)
    c.restore()
    bp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0)
    bp.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + h)],
                                                [hexa("#FFFFFF", lisere), hexa("#FFFFFF", lisere * 0.3)], [0.0, 1.0]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 1, y + 1, w - 2, h - 2), r - 1, r - 1), bp)


def ressort(v, s=1.25):
    return rebond(v, s)


# ─────────────────────────────────────────── pastille de marque et chapitres
CHAPITRES = [  # début, fin, numéro, lieu, titre, ligne
    (4.22, 8.55, "01", "USINE", "Motos électriques", "En direct de l’usine"),
    (8.80, 11.15, "02", "BIJOUTERIE", "Montres & bijoux", "Plusieurs qualités au choix"),
    (12.58, 14.15, "03", "ENTREPÔT", "Baskets", "Une photo suffit, on trouve le modèle"),
    (14.36, 16.66, "04", "GROSSISTE", "Vêtements", "Pour toi, ou en quantité pour revendre"),
    (16.82, T_FIN - 0.05, "05", "MARCHÉ", "Électronique", "Livré chez toi en 8 à 12 jours"),
]


def marque(c, t):
    u = prog(t, 0.35, 0.6, sortie) * (1 - prog(t, T_FIN, 0.3, entree))
    if u <= 0.01: return
    lab = "TON AGENT EN CHINE"
    lw = 176; iw, ih = taille_img("logo-dy-blanc"); lh = lw * ih / iw
    tw = largeur(lab, 19, "fort", 0.14)
    w = 34 + lw + 30 + 2 + 30 + 18 + tw + 34; h = 76
    x = mix(-w - 20, 56, u); y = 48
    with Calque(c, borne(u * 2)):
        verre(c, x, y, w, h, h / 2, 0.42)
        image(c, "logo-dy-blanc", x + 34, y + h / 2 - lh / 2, lw)
        c.drawRect(skia.Rect.MakeXYWH(x + 34 + lw + 30, y + 22, 2, h - 44), peinture("#FFFFFF", 0.25))
        dx = x + 34 + lw + 62
        disque(c, dx + 5, y + h / 2, 5, LILAS, 0.45 + 0.55 * (0.5 + 0.5 * math.cos(t * 4)))
        texte(c, lab, dx + 18, y + h / 2 - hauteurLigne(19, "fort") / 2, 19, "#FFFFFF", "fort", track=0.14, alpha=0.92)


def progression(c, t):
    u = prog(t, CHAPITRES[0][0], 0.5, sortie) * (1 - prog(t, T_FIN, 0.3, entree))
    if u <= 0.01: return
    actif = max([k for k, ch in enumerate(CHAPITRES) if t >= ch[0]], default=0)
    n = len(CHAPITRES); seg, gap = 38, 10
    lab = f"{CHAPITRES[actif][2]} / 0{n}"
    tw = largeur(lab, 20, "fort", 0.08)
    w = 30 + tw + 22 + n * seg + (n - 1) * gap + 30; h = 76
    x = mix(W + 20, W - 56 - w, u); y = 48
    with Calque(c, borne(u * 2)):
        verre(c, x, y, w, h, h / 2, 0.42)
        texte(c, lab, x + 30, y + h / 2 - hauteurLigne(20, "fort") / 2, 20, "#FFFFFF", "fort", track=0.08)
        sx = x + 30 + tw + 22
        for k in range(n):
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx + k * (seg + gap), y + h / 2 - 3, seg, 6), 3, 3)
            c.drawRRect(rr, peinture("#FFFFFF", 0.22))
            if k < actif:
                c.drawRRect(rr, peinture(LILAS, 0.95))
            elif k == actif:
                f = borne((t - CHAPITRES[k][0]) / max(0.1, CHAPITRES[k][1] - CHAPITRES[k][0]))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx + k * (seg + gap), y + h / 2 - 3, seg * f, 6), 3, 3), peinture(LILAS))


def carte_chapitre(c, t, ch):
    ta, tb, num, lieu, titre, ligne = ch
    if t < ta - 0.01 or t > tb + 0.4: return
    u = prog(t, ta, 0.6, lambda v: ressort(v, 1.1)); o = prog(t, tb, 0.36, entree)
    T1, T2 = 72, 30
    w = max(largeur(titre, T1, "noir"), largeur(ligne, T2, "demi", 0)) + 96
    h = 236; x = 72; y = H - 72 - h
    m = matrice3d(x + w / 2, y + h, rx=mix(-38, 0, u) + 26 * o, ty=mix(90, 0, u) + 50 * o)
    c.save(); c.concat(m)
    with Calque(c, borne(u * 3) * (1 - o)):
        verre(c, x, y, w, h, 34, 0.48)
        # surtitre : numéro dans une pastille violette + lieu espacé
        e = prog(t, ta + 0.12, 0.4, sortie)
        ex, ey = x + 48, y + 44
        disque(c, ex + 19, ey + 15, 19 * e, VIOLET)
        texte_centre(c, num, ex + 19, ey + 15, 17, "#FFFFFF", "noir", e)
        texte(c, lieu, ex + 52, ey + 15 - hauteurLigne(19, "fort") / 2, 19, LILAS, "fort", track=0.2, alpha=e)
        # titre révélé par un volet, ligne qui suit
        r = prog(t, ta + 0.18, 0.5, sortie)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, 48 + (w - 48) * r, h))
        texte(c, titre, x + 48 + mix(-30, 0, r), y + 74, T1, "#FFFFFF", "noir", track=-0.03)
        c.restore()
        l = prog(t, ta + 0.42, 0.45, sortie)
        texte(c, ligne, x + 48, y + 74 + hauteurLigne(T1) + 4 + mix(14, 0, l), T2, "#FFFFFF", "demi", track=0, alpha=0.82 * l)
    c.restore()


# ─────────────────────────────────────────── repères accrochés aux objets
SUIVI = {p.stem: np.array(json.load(open(p))) for p in (P / "suivi").glob("*.json")}
REPERES = [  # suivi, apparition, disparition, étiquette, icône
    ("usine", 5.42, 6.45, "Face au fabricant", "factory"),
    ("essai", 6.75, 7.85, "Essai sur place", "check"),
    ("montre1", 8.76, 9.30, "Contrôle de près", "search"),
    ("montre2", 9.48, 10.45, "On compare les qualités", "scale"),
    ("basket", 12.62, 13.55, "Le modèle exact", "check"),
    ("veste", 15.16, 16.35, "Matière vérifiée", "shirt"),
    ("casque", 16.92, 18.40, "Prix livraison incluse", "truck"),
]


def point(nom, t):
    a = SUIVI[nom]
    return float(np.interp(t, a[:, 0], a[:, 1])), float(np.interp(t, a[:, 0], a[:, 2]))


def repere(c, t, nom, ta, tb, lab, ic):
    if t < ta or t > tb + 0.28: return
    x, y = point(nom, t)
    o = prog(t, tb, 0.28, entree); al = 1 - o
    u = prog(t, ta, 0.4, lambda v: ressort(v, 2.0))
    # anneau qui pulse + point
    for k in range(2):
        ph = ((t - ta) * 1.1 + k * 0.5) % 1.0
        anneau(c, x, y, 16 + 50 * ph, "#FFFFFF", 2.5, (1 - ph) * 0.75 * al * borne(u * 2))
    disque(c, x, y, 26 * u, VOILE, 0.35 * al)
    anneau(c, x, y, 19 * u, "#FFFFFF", 3, al)
    disque(c, x, y, 8 * u, "#FFFFFF", al)
    # trait coudé vers l'étiquette : on s'éloigne du bord le plus proche
    sx = 1 if x < 1300 else -1
    sy = -1 if y > 360 else 1
    d1, d2 = 96, 56
    p0 = (x + sx * 22 * 0.7071, y + sy * 22 * 0.7071)
    p1 = (x + sx * d1, y + sy * d1)
    p2 = (p1[0] + sx * d2, p1[1])
    lu = prog(t, ta + 0.1, 0.32, sortie)
    L1 = math.dist(p0, p1); L = L1 + d2; s = lu * L
    if s > 0:
        q = min(1, s / L1)
        trait(c, p0[0], p0[1], mix(p0[0], p1[0], q), mix(p0[1], p1[1], q), "#FFFFFF", 3, 0.9 * al)
        if s > L1:
            trait(c, p1[0], p1[1], p1[0] + sx * (s - L1), p1[1], "#FFFFFF", 3, 0.9 * al)
    # étiquette de verre qui se déplie depuis le bout du trait
    e = prog(t, ta + 0.32, 0.42, lambda v: ressort(v, 1.2))
    if e <= 0: return
    T = 30; hh = 70; ici = 40
    tw = largeur(lab, T, "fort", 0)
    w = 16 + ici + 16 + tw + 30
    ww = max(hh, w * borne(e))
    bx = p2[0] if sx > 0 else p2[0] - ww
    by = p2[1] - hh / 2
    with Calque(c, al * borne(e * 3)):
        verre(c, bx, by, ww, hh, hh / 2, 0.5)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(bx, by, ww, hh))
        ox = bx if sx > 0 else bx + ww - w
        disque(c, ox + 16 + ici / 2, by + hh / 2, ici / 2, VIOLET)
        icone(c, ic, ox + 16 + ici / 2, by + hh / 2, 24, "#FFFFFF", 2.6)
        texte(c, lab, ox + 16 + ici + 16, by + hh / 2 - hauteurLigne(T, "fort") / 2, T, "#FFFFFF", "fort", track=0)
        c.restore()


# ─────────────────────────────────────────── phrases en grand sur les plans flous
PHRASES = [  # début, fin, surtitre, lignes
    (3.12, 4.30, "DROP&YOU · EN CHINE", ["On va à la source."], "Usines, entrepôts, marchés de gros"),
    (11.42, 12.50, "SUR PLACE", ["Tu choisis.", "On s’occupe du reste."], None),
]


def phrase(c, t, ph):
    ta, tb, sur, lignes, sous = ph
    if t < ta or t > tb + 0.32: return
    u = prog(t, ta, 0.62, lambda v: ressort(v, 1.15)); o = prog(t, tb, 0.32, entree)
    T = 92
    tw = max(largeur(s, T) for s in lignes)
    if sous: tw = max(tw, largeur(sous, 34, "demi", 0))
    w = tw + 140
    h = 70 + 40 + len(lignes) * hauteurLigne(T) + (60 if sous else 0) + 50
    x, y = W / 2 - w / 2, H / 2 - h / 2
    m = matrice3d(W / 2, H / 2, rx=mix(32, 0, u) - 14 * o, s=mix(0.86, 1, u), ty=mix(60, 0, u) - 70 * o)
    c.save(); c.concat(m)
    with Calque(c, borne(u * 3) * (1 - o)):
        verre(c, x, y, w, h, 44, 0.5)
        texte(c, sur, W / 2, y + 58, 22, LILAS, "fort", "centre", 0.24, prog(t, ta + 0.1, 0.4))
        yy = y + 100
        for k, s in enumerate(lignes):
            r = prog(t, ta + 0.16 + 0.22 * k, 0.48, sortie)
            c.save(); c.clipRect(skia.Rect.MakeXYWH(x, yy - 10, w, hauteurLigne(T) + 20))
            texte(c, s, W / 2, yy + mix(hauteurLigne(T), 0, r), T, "#FFFFFF", "noir", "centre", -0.035)
            c.restore()
            yy += hauteurLigne(T)
        if sous:
            texte(c, sous, W / 2, yy + 16, 34, "#FFFFFF", "demi", "centre", 0, 0.8 * prog(t, ta + 0.42, 0.4))
    c.restore()


# ─────────────────────────────────────────── carton de fin
def carton(c, t):
    u = prog(t, T_FIN + 0.15, 0.6, lambda v: ressort(v, 1.12))
    if u <= 0: return
    w, h = 1080, 560
    x, y = W / 2 - w / 2, H / 2 - h / 2 + 10
    m = matrice3d(W / 2, H / 2, rx=mix(30, 0, u), s=mix(0.86, 1, u), ty=mix(70, 0, u))
    c.save(); c.concat(m)
    with Calque(c, borne(u * 3)):
        verre(c, x, y, w, h, 48, 0.55)
        lw = 560; iw, ih = taille_img("logo-dy-blanc"); lh = lw * ih / iw
        ul = prog(t, T_FIN + 0.3, 0.5, sortie)
        image(c, "logo-dy-blanc", W / 2 - lw / 2, y + 74 + mix(16, 0, ul), lw, ul)
        texte(c, "Ton agent en Chine", W / 2, y + 74 + lh + 26, 40, "#FFFFFF", "demi", "centre", 0, 0.88 * prog(t, T_FIN + 0.45, 0.4))
        cats = "Motos · Montres · Baskets · Vêtements · Électronique"
        texte(c, cats, W / 2, y + 74 + lh + 90, 25, LILAS, "fort", "centre", 0.04, prog(t, T_FIN + 0.6, 0.4))
        # deux boutons : Snapchat et WhatsApp
        boutons = [("snapchat", "dropandyou1", MARQUES["snapchat"], "#0B0F0D"), ("whatsapp", "WhatsApp", MARQUES["whatsapp"], "#FFFFFF")]
        hb = 92; T = 36
        ws = [hb + largeur(lab, T, "noir", -0.01) + 46 for _, lab, _, _ in boutons]
        gap = 28; tot = sum(ws) + gap
        bx = W / 2 - tot / 2; by = y + h - 70 - hb
        for k, (nom, lab, fond_, enc) in enumerate(boutons):
            ub = prog(t, T_FIN + 0.75 + 0.14 * k, 0.45, lambda v: ressort(v, 1.8))
            if ub > 0:
                cx = bx + ws[k] / 2
                c.save(); c.translate(cx, by + hb / 2); c.scale(mix(0.5, 1, ub), mix(0.5, 1, ub)); c.translate(-cx, -(by + hb / 2))
                with Calque(c, borne(ub * 2)):
                    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(bx, by, ws[k], hb), hb / 2, hb / 2)
                    c.drawRRect(rr, peinture(fond_))
                    logo_glyphe(c, nom, bx + hb / 2 + 8, by + hb / 2, 46, enc, contour="#0B0F0D" if nom == "snapchat" else None)
                    texte(c, lab, bx + hb + 8, by + hb / 2 - hauteurLigne(T) / 2, T, enc, "noir", track=-0.01)
                c.restore()
            bx += ws[k] + gap
    c.restore()


# ─────────────────────────────────────────── sons
for ph in PHRASES:
    son(ph[0], "whoosh_long", -15); son(ph[0] + 0.18, "verre", -16)
    son(ph[1], "whoosh_court", -20)
for ch in CHAPITRES:
    son(ch[0], "whoosh_court", -15); son(ch[0] + 0.14, "clic", -16)
for r in REPERES:
    son(r[1], "blip", -19); son(r[1] + 0.32, "pop", -17)
son(T_FIN, "whoosh_long", -12); son(T_FIN + 0.2, "impact_doux", -10); son(T_FIN + 0.32, "verre", -12)
son(T_FIN + 0.75, "pop", -13); son(T_FIN + 0.89, "pop", -13)


# ─────────────────────────────────────────── composition
def flou_de(a):
    s = cv2.resize(a, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    s = cv2.GaussianBlur(s, (0, 0), 7)
    return skia.Image.fromarray(np.ascontiguousarray(s), colorType=skia.kRGBA_8888_ColorType)


def dessine(c, t, img):
    nette = skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType)
    FOND[0] = flou_de(img)
    z = 1 + 0.05 * prog(t, FIN_SRC, DUREE - FIN_SRC, sortie)       # léger zoom sur l'image figée
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    c.drawImage(nette, 0, 0)
    f = prog(t, T_FIN, 0.55, entreeSortie)
    if f > 0:
        c.drawImageRect(FOND[0], skia.Rect.MakeWH(W, H), _ECH, skia.Paint(Alphaf=f))
        c.drawRect(skia.Rect.MakeWH(W, H), peinture(VOILE, 0.35 * f))
    c.restore()
    marque(c, t); progression(c, t)
    for ph in PHRASES: phrase(c, t, ph)
    for ch in CHAPITRES: carte_chapitre(c, t, ch)
    for r in REPERES: repere(c, t, *r)
    carton(c, t)


def lecteur():
    """images de la vidéo fournie, une à une ; la dernière se répète ensuite"""
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(SRC), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
    der = None
    while True:
        b = pr.stdout.read(W * H * 4)
        if len(b) < W * H * 4: break
        der = np.frombuffer(b, np.uint8).reshape(H, W, 4).copy()
        yield der
    while True:
        yield der


def image_a(t, img):
    s = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    dessine(s.getCanvas(), t, img)
    return s.toarray()


def apercu(temps):
    from PIL import Image
    (P / "apercus").mkdir(exist_ok=True)
    vign = []
    for t in temps:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{min(t, FIN_SRC - 0.04):.3f}", "-i", str(SRC), "-frames:v", "1",
                              "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True).stdout
        img = np.frombuffer(raw[:W * H * 4], np.uint8).reshape(H, W, 4).copy()
        im = Image.fromarray(image_a(t, img)[..., :3])
        im.save(P / "apercus" / f"m_{t:05.2f}.jpg", quality=88)
        vign.append(im.resize((640, 360), Image.LANCZOS))
    cols = 3; pl = Image.new("RGB", (640 * cols, 360 * ((len(vign) + cols - 1) // cols)))
    for k, im in enumerate(vign): pl.paste(im, ((k % cols) * 640, (k // cols) * 360))
    pl.save(P / "apercus" / "planche_montage.jpg", quality=85)


def video():
    (P / "renders").mkdir(exist_ok=True)
    sortie_ = P / "renders" / "image.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", str(sortie_)], stdin=subprocess.PIPE)
    src = lecteur()
    for i in range(N):
        enc.stdin.write(image_a(i / FPS, next(src)).tobytes())
        if i % 60 == 0: print(f"{i}/{N}", flush=True)
    enc.stdin.close(); enc.wait()
    mixage()


def lire_audio(chemin):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(chemin), "-vn", "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def mixage():
    sr = 48000
    a = lire_audio(SRC)
    n = int(DUREE * sr); out = np.zeros((n, 2), np.float32)
    # la musique fournie s'éteint doucement sous l'arrivée du carton
    t = np.arange(len(a)) / sr
    a *= np.clip((FIN_SRC - t) / (FIN_SRC - (T_FIN - 0.1)), 0, 1)[:, None] ** 1.5
    out[:min(n, len(a))] += a[:n]
    sons = P.parent / "moteur" / "sons"
    for ts, nom, g in SFX:
        s = lire_audio(sons / f"{nom}.wav") * 10 ** (g / 20)
        k = int(ts * sr); m = min(len(s), n - k)
        if m > 0: out[k:k + m] += s[:m]
    tmp = P / "renders" / "mix.f32"
    out.tofile(tmp)
    (P / "video").mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "renders" / "image.mp4"),
                    "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", str(tmp),
                    "-af", "alimiter=limit=0.79:attack=3:release=60", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-movflags", "+faststart", "-shortest", str(P / "video" / "DY-M03.mp4")], check=True)
    print("fini :", P / "video" / "DY-M03.mp4")


if __name__ == "__main__":
    if sys.argv[1] == "apercu": apercu([float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == "son": mixage()
    else: video()
