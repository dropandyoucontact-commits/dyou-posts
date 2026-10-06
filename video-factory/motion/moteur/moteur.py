"""Moteur de rendu motion design — Python + Skia, sans navigateur.

Une image = une fonction pure du temps t. Les scènes (scenes.py) dessinent sur un
canevas Skia ; ce module fournit les briques : texte mesuré et crénagé (HarfBuzz,
via skia.textlayout), cartes et ombres, images, icônes Lucide (SVG), perspective
3D vraie (projection des quatre coins), courbes d'animation, particules, flou de
mouvement par sous-images, et l'encodage H.264 parallélisé.

Le même code dessine les aperçus et la vidéo finale : ce qu'on vérifie est ce
qu'on exporte.
"""
import math, functools, pathlib, subprocess
import numpy as np
import skia
from skia import textlayout as tl

ICI = pathlib.Path(__file__).resolve().parent      # le moteur : fontes/, icones/, sons/
PROJET = pathlib.Path.cwd()                         # le projet vidéo : media/ (scenes.py le fixe)
W, H, FPS = 1080, 1920, 60

# ───────────────────────────── couleurs
def hexa(s, a=1.0):
    s = s.lstrip("#")
    return skia.Color(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), int(round(255 * max(0, min(1, a)))))

C = dict(ink="#0B0F0D", blanc="#FFFFFF", gris="#6B7470", grisClair="#A7AFAB", ligne="#E7EBE9", fondDoux="#F3F6F4",
         vert="#00B862", vertFonce="#00804A", vertDoux="#E2F7EB", vertMoyen="#9BE3BD",
         rouge="#FF3B30", rougeDoux="#FFE6E4", ambre="#FFB020", bleuFR="#0055A4", rougeFR="#EF4135", rougeCN="#DE2910", jauneCN="#FFDE00")

# ───────────────────────────── courbes
def borne(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(mix(x, y, u) for x, y in zip(a, b))
    return a + (b - a) * u

def lin(u): return u
def sortie(u): return 1 - (1 - u) ** 3
def entree(u): return u ** 3
def douce(u): return u * u * (3 - 2 * u)
def sortieExpo(u): return 1.0 if u >= 1 else 1 - 2 ** (-10 * u)
def entreeSortie(u): return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2

def rebond(u, s=1.70158):
    u -= 1
    return u * u * ((s + 1) * u + s) + 1

def ressort(u, f=3.2, amorti=4.6):
    """ressort normalisé : part de 0, dépasse 1 puis s'y pose (u de 0 à 1)"""
    if u <= 0: return 0.0
    if u >= 1: return 1.0
    return 1 - math.exp(-amorti * u) * math.cos(2 * math.pi * f * u) * (1 - u) ** 0.4

def prog(t, t0, d, courbe=sortie):
    """progression 0→1 d'un mouvement qui commence à t0 et dure d"""
    if d <= 0: return 1.0 if t >= t0 else 0.0
    return courbe(borne((t - t0) / d))

def cles(t, cles_, courbe=sortie):
    """interpolation par clés [(t, valeur[, courbe]), ...] ; la courbe d'une clé mène à elle"""
    if t <= cles_[0][0]: return cles_[0][1]
    for i in range(1, len(cles_)):
        t1 = cles_[i][0]
        if t <= t1:
            t0, v0 = cles_[i - 1][0], cles_[i - 1][1]
            c = cles_[i][2] if len(cles_[i]) > 2 else courbe
            return mix(v0, cles_[i][1], c(borne((t - t0) / (t1 - t0)) if t1 > t0 else 1))
    return cles_[-1][1]

def secousse(t, t0, amp=14, duree=0.32, freq=26.0):
    """décalage (dx, dy) amorti après un impact"""
    if t < t0 or t > t0 + duree: return 0.0, 0.0
    u = (t - t0) / duree
    e = (1 - u) ** 2
    return amp * e * math.sin(2 * math.pi * freq * (t - t0)), amp * 0.6 * e * math.cos(2 * math.pi * freq * 0.83 * (t - t0))

def battement(t, t0, a=0.06, d=0.3):
    """facteur d'échelle 1 → 1+a → 1"""
    if t < t0 or t > t0 + d: return 1.0
    u = (t - t0) / d
    return 1 + a * math.sin(math.pi * u) * (1 - u) ** 0.5 * 1.6

# ───────────────────────────── texte (mesuré et dessiné par le même moteur)
_FAM = {"noir": "InterDisplay-Black", "xgras": "InterDisplay-ExtraBold", "gras": "InterDisplay-Bold",
        "titre": "Inter-ExtraBold", "fort": "Inter-Bold", "demi": "Inter-SemiBold", "moyen": "Inter-Medium"}
_prov = tl.TypefaceFontProvider()
for _f in set(_FAM.values()):
    _prov.registerTypeface(skia.Typeface.MakeFromFile(str(ICI / "fontes" / f"{_f}.ttf")), _f)
_fc = tl.FontCollection()
_fc.setDefaultFontManager(_prov)
_UNI = skia.Unicode.ICU_Make()

@functools.lru_cache(maxsize=6000)
def _para(s, fam, taille, couleur, ls):
    ts = tl.TextStyle()
    ts.setFontFamilies([_FAM.get(fam, fam)]); ts.setFontSize(taille); ts.setColor(couleur); ts.setLetterSpacing(ls)
    b = tl.ParagraphBuilder.make(tl.ParagraphStyle(), _fc, _UNI)
    b.pushStyle(ts); b.addText(s)
    p = b.Build(); p.layout(100000)
    return p

def _ls(taille, track):
    return round(taille * track, 2)

def largeur(s, taille, fam="noir", track=-0.025):
    return _para(s, fam, float(taille), 0xFF000000, _ls(taille, track)).LongestLine

def texte(c, s, x, y, taille, couleur=C["ink"], fam="noir", align="gauche", track=-0.025, alpha=1.0):
    """dessine s ; y = haut de la boîte de ligne ; renvoie la largeur"""
    if alpha <= 0.004: return largeur(s, taille, fam, track)
    a = round(borne(alpha) * 40) / 40
    p = _para(s, fam, float(taille), hexa(couleur, a), _ls(taille, track))
    w = p.LongestLine
    if align == "centre": x -= w / 2
    elif align == "droite": x -= w
    p.paint(c, x, y)
    return w

def hauteurLigne(taille, fam="noir"):
    return _para("Hg", fam, float(taille), 0xFF000000, 0.0).Height

def ajuste(s, larg_max, taille, fam="noir", track=-0.025, mini=10):
    """plus grande taille ≤ taille pour que s tienne dans larg_max"""
    while taille > mini and largeur(s, taille, fam, track) > larg_max:
        taille -= 1
    return taille

# ───────────────────────────── formes
def peinture(couleur, alpha=1.0, **kw):
    return skia.Paint(AntiAlias=True, Color=hexa(couleur, alpha), **kw)

def rrect(c, x, y, w, h, r, couleur, alpha=1.0, ombre=None, contour=None, ep=0):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    if ombre and alpha > 0:
        dy, flou, opa = ombre
        p = peinture(couleur, alpha)
        p.setImageFilter(skia.ImageFilters.DropShadow(0, dy, flou / 2, flou / 2, hexa("#0B0F0D", opa * alpha)))
        c.drawRRect(rr, p)
    elif alpha > 0 and couleur:
        c.drawRRect(rr, peinture(couleur, alpha))
    if contour and ep > 0 and alpha > 0:
        c.drawRRect(rr, peinture(contour, alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=ep))

def carte(c, x, y, w, h, r=40, couleur=C["blanc"], alpha=1.0, ombre=(26, 56, 0.13), contour=None, ep=0):
    rrect(c, x, y, w, h, r, couleur, alpha, ombre, contour, ep)

def disque(c, cx, cy, r, couleur, alpha=1.0, ombre=None):
    p = peinture(couleur, alpha)
    if ombre:
        dy, flou, opa = ombre
        p.setImageFilter(skia.ImageFilters.DropShadow(0, dy, flou / 2, flou / 2, hexa("#0B0F0D", opa * alpha)))
    c.drawCircle(cx, cy, r, p)

def anneau(c, cx, cy, r, couleur, ep, alpha=1.0):
    c.drawCircle(cx, cy, r, peinture(couleur, alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=ep))

def trait(c, x0, y0, x1, y1, couleur, ep, alpha=1.0, pointille=None, rond=True):
    p = peinture(couleur, alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=ep)
    if rond: p.setStrokeCap(skia.Paint.kRound_Cap)
    if pointille: p.setPathEffect(skia.DashPathEffect.Make(pointille, 0))
    c.drawLine(x0, y0, x1, y1, p)

def chemin_svg(d):
    """chemin SVG simple (M/L/C/Q/Z, coordonnées absolues)"""
    p = skia.Path()
    jet = d.replace(",", " ").replace("M", " M ").replace("L", " L ").replace("C", " C ").replace("Q", " Q ").replace("Z", " Z ").split()
    i, cmd = 0, None
    while i < len(jet):
        tok = jet[i]
        if tok in "MLCQZ":
            cmd = tok; i += 1
            if cmd == "Z": p.close(); continue
        n = {"M": 2, "L": 2, "C": 6, "Q": 4}[cmd]
        v = [float(x) for x in jet[i:i + n]]; i += n
        if cmd == "M": p.moveTo(*v); cmd = "L"
        elif cmd == "L": p.lineTo(*v)
        elif cmd == "C": p.cubicTo(*v)
        elif cmd == "Q": p.quadTo(*v)
    return p

def etoile(cx, cy, r, rot=-math.pi / 2):
    p = skia.Path()
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.382
        a = rot + k * math.pi / 5
        (p.moveTo if k == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close()
    return p

def drapeau(c, pays, x, y, w, h, r=8):
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), doAntiAlias=True)
    if pays == "FR":
        for k, col in enumerate([C["bleuFR"], C["blanc"], C["rougeFR"]]):
            c.drawRect(skia.Rect.MakeXYWH(x + k * w / 3, y, w / 3 + 1, h), peinture(col))
    elif pays == "TH":
        for (u0, u1, col) in [(0, 1, "#A51931"), (1, 2, "#F4F5F8"), (2, 4, "#2D2A4A"), (4, 5, "#F4F5F8"), (5, 6, "#A51931")]:
            c.drawRect(skia.Rect.MakeXYWH(x, y + h * u0 / 6, w, h * (u1 - u0) / 6 + 1), peinture(col))
    elif pays == "BE":
        for k, col in enumerate(["#111111", "#FDDA24", "#EF3340"]):
            c.drawRect(skia.Rect.MakeXYWH(x + k * w / 3, y, w / 3 + 1, h), peinture(col))
    elif pays == "MA":
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#C1272D"))
        c.drawPath(etoile(x + w / 2, y + h / 2 + h * 0.02, h * 0.3), peinture("#006233", Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.5, h * 0.05)))
    else:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(C["rougeCN"]))
        c.drawPath(etoile(x + w * 0.17, y + h * 0.27, h * 0.16), peinture(C["jauneCN"]))
        for (px, py) in [(0.33, 0.1), (0.4, 0.2), (0.4, 0.35), (0.33, 0.45)]:
            c.drawPath(etoile(x + w * px, y + h * py, h * 0.055), peinture(C["jauneCN"]))
    c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), peinture("#000000", 0.08, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5))

# ───────────────────────────── images et icônes
_ECH = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)

BANQUE = ICI.parent / "banque"   # banque commune : produits/<catégorie>/, videos/, lieux/, logos/


def chemin_media(nom, exts=(".png",)):
    """cherche d'abord dans le projet (media/), puis dans le moteur (media/), puis dans la banque"""
    for base in (PROJET / "media", ICI / "media", BANQUE):
        for e in exts:
            f = base / f"{nom}{e}"
            if f.exists():
                return f
    raise FileNotFoundError(f"média introuvable : {nom} ({', '.join(exts)})")


@functools.lru_cache(maxsize=None)
def _img(nom):
    return skia.Image.open(str(chemin_media(nom, (".png", ".jpg")))).withDefaultMipmaps()

def taille_img(nom):
    i = _img(nom)
    return i.width(), i.height()

def image(c, nom, x, y, w, alpha=1.0, h=None):
    i = _img(nom)
    h = h if h is not None else w * i.height() / i.width()
    p = skia.Paint(AntiAlias=True)
    if alpha < 1: p.setAlphaf(borne(alpha))
    c.drawImageRect(i, skia.Rect.MakeXYWH(x, y, w, h), _ECH, p)
    return h

def ombre_sol(c, cx, cy, rx, ry, opa=0.16):
    """ombre portée elliptique douce sous un objet posé"""
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(0, 0), 1.0, [hexa("#0B0F0D", opa), hexa("#0B0F0D", 0)], [0.0, 1.0]))
    c.save(); c.translate(cx, cy); c.scale(rx, ry)
    c.drawCircle(0, 0, 1.0, p)
    c.restore()

_SVG_DONNEES = []   # garde les octets en vie : le flux Skia ne les copie pas

@functools.lru_cache(maxsize=None)
def _svg(nom, couleur, ep):
    src = (ICI / "icones" / f"{nom}.svg").read_text().replace("currentColor", couleur).replace('stroke-width="2"', f'stroke-width="{ep}"')
    data = skia.Data.MakeWithCopy(src.encode())
    _SVG_DONNEES.append(data)
    dom = skia.SVGDOM.MakeFromStream(skia.MemoryStream(data))
    if dom is None:
        raise RuntimeError(f"icône illisible : {nom}")
    dom.setContainerSize(skia.Size(24, 24))
    return dom

def icone(c, nom, cx, cy, taille, couleur=C["ink"], ep=2.0, alpha=1.0):
    dom = _svg(nom, couleur, ep)
    c.save()
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(cx - taille, cy - taille, 2 * taille, 2 * taille), int(255 * borne(alpha)))
    c.translate(cx - taille / 2, cy - taille / 2); c.scale(taille / 24, taille / 24)
    dom.render(c)
    if alpha < 1: c.restore()
    c.restore()

def image_cover(c, nom, x, y, w, h, zoom=1.0, fx=0.5, fy=0.5, rayon=0, alpha=1.0):
    """photo de la banque qui remplit le cadre (recadrage « cover »), zoom ≥ 1 centré sur (fx, fy)
    en fractions de l'image : animer zoom et fx/fy donne un travelling lent (effet Ken Burns).
    Sert aux photos en situation (portées, posées, en rayon) montrées dans un téléphone."""
    i = _img(nom)
    iw, ih = i.width(), i.height()
    s = max(w / iw, h / ih) * max(1.0, zoom)
    vw, vh = w / s, h / s                                   # fenêtre visible dans l'image source
    sx = min(max(fx * iw - vw / 2, 0), iw - vw)
    sy = min(max(fy * ih - vh / 2, 0), ih - vh)
    c.save()
    if rayon: c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), rayon, rayon), doAntiAlias=True)
    else: c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    p = skia.Paint(AntiAlias=True)
    if alpha < 1: p.setAlphaf(borne(alpha))
    c.drawImageRect(i, skia.Rect.MakeXYWH(sx, sy, vw, vh), skia.Rect.MakeXYWH(x, y, w, h), _ECH, p)
    c.restore()


# ───────────────────────────── vidéos de la banque (images extraites une fois, lues à la demande)
def prepare_video(nom, w, h, rogne=(0.0, 0.0, 0.0, 0.0)):
    """extrait la vidéo en images JPEG au format exact du cadre (recadrage « cover »).
    rogne = fractions (gauche, haut, droite, bas) retirées de la source avant le recadrage :
    sert à couper un sous-titre ou un logo incrusté. Le processus principal extrait avant le
    rendu parallèle ; les autres trouvent le travail fait."""
    w, h = int(w), int(h)
    src = chemin_media(nom, (".mp4", ".mov"))
    tag = "" if not any(rogne) else "-r" + "".join(f"{int(round(v * 100)):02d}" for v in rogne)
    cache = PROJET / "renders" / "cache-videos" / f"{pathlib.Path(nom).name}-{w}x{h}{tag}"
    if not (cache / "fini").exists():
        cache.mkdir(parents=True, exist_ok=True)
        g, hh, d, b = rogne
        pre = f"crop=iw*{1 - g - d:.4f}:ih*{1 - hh - b:.4f}:iw*{g:.4f}:ih*{hh:.4f}," if any(rogne) else ""
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an",
                        "-vf", f"{pre}scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
                        "-q:v", "3", str(cache / "%05d.jpg")], check=True)
        fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                              "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip()
        (cache / "fini").write_text(fps)
    num, _, den = (cache / "fini").read_text().strip().partition("/")
    return cache, len(list(cache.glob("*.jpg"))), float(num) / float(den or 1)


@functools.lru_cache(maxsize=600)
def _image_video(dossier, k):
    return skia.Image.open(f"{dossier}/{k:05d}.jpg")


def video(c, nom, x, y, w, h, t_local, vitesse=1.0, boucle=True, rayon=0, alpha=1.0, rogne=(0.0, 0.0, 0.0, 0.0)):
    """dessine l'image de la vidéo au temps t_local × vitesse (×2 ou ×2,5 pour tenir dans une phrase)"""
    cache, n, fps = prepare_video(nom, w, h, rogne)
    k = int(max(0.0, t_local) * vitesse * fps)
    k = k % n if boucle else min(k, n - 1)
    c.save()
    if rayon: c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), rayon, rayon), doAntiAlias=True)
    p = skia.Paint(AntiAlias=True)
    if alpha < 1: p.setAlphaf(borne(alpha))
    c.drawImageRect(_image_video(str(cache), k + 1), skia.Rect.MakeXYWH(x, y, w, h), _ECH, p)
    c.restore()


# ───────────────────────────── perspective 3D vraie
def matrice3d(cx, cy, rx=0.0, ry=0.0, rz=0.0, s=1.0, tx=0.0, ty=0.0, d=1800.0):
    """projection des coins d'un carré tourné en 3D autour de (cx, cy) ; angles en degrés"""
    rx, ry, rz = math.radians(rx), math.radians(ry), math.radians(rz)
    h = 300.0
    src, dst = [], []
    for x, y in [(-h, -h), (h, -h), (h, h), (-h, h)]:
        X, Y = x * s, y * s
        X, Y = X * math.cos(rz) - Y * math.sin(rz), X * math.sin(rz) + Y * math.cos(rz)
        Z = 0.0
        X, Z = X * math.cos(ry) + Z * math.sin(ry), -X * math.sin(ry) + Z * math.cos(ry)
        Y, Z = Y * math.cos(rx) - Z * math.sin(rx), Y * math.sin(rx) + Z * math.cos(rx)
        f = d / (d + Z)
        src.append(skia.Point(cx + x, cy + y)); dst.append(skia.Point(cx + tx + X * f, cy + ty + Y * f))
    m = skia.Matrix()
    m.setPolyToPoly(src, dst)
    return m

class Espace:
    """with Espace(c, cx, cy, rx=..., ry=..., s=...): dessin dans un plan tourné en 3D"""
    def __init__(self, c, cx, cy, **kw):
        self.c, self.m = c, matrice3d(cx, cy, **kw)
    def __enter__(self):
        self.c.save(); self.c.concat(self.m); return self.c
    def __exit__(self, *a):
        self.c.restore()

class Calque:
    """with Calque(c, alpha): groupe dessiné avec une opacité commune"""
    def __init__(self, c, alpha):
        self.c, self.a = c, borne(alpha)
    def __enter__(self):
        if self.a < 0.999: self.c.saveLayerAlpha(None, int(255 * self.a))
        else: self.c.save()
        return self.c
    def __exit__(self, *a):
        self.c.restore()

# ───────────────────────────── particules
def confettis(c, cx, cy, t, t0, n=22, rayon=330, graine=1, cols=None):
    if t < t0 or t > t0 + 1.25: return
    cols = cols or [C["vert"], C["ink"], C["vertMoyen"], C["vertFonce"], C["ambre"]]
    rng = np.random.default_rng(graine)
    u = t - t0
    for k in range(n):
        a = k / n * 2 * math.pi + rng.uniform(-0.3, 0.3)
        v = rayon * rng.uniform(0.55, 1.15)
        dx = math.cos(a) * v * sortie(min(1, u / 0.45))
        dy = math.sin(a) * v * sortie(min(1, u / 0.45)) - 60 * sortie(min(1, u / 0.45)) + 520 * max(0, u - 0.35) ** 2
        rot = rng.uniform(0, 360) + 520 * u * rng.choice([-1, 1])
        w, h = rng.uniform(10, 18), rng.uniform(18, 30)
        al = borne(1 - max(0, u - 0.8) / 0.45)
        c.save(); c.translate(cx + dx, cy + dy); c.rotate(rot)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 3, 3), peinture(cols[k % len(cols)], al))
        c.restore()

def onde(c, cx, cy, t, t0, r0=60, r1=260, couleur=C["vert"], ep=6, duree=0.6):
    if t < t0 or t > t0 + duree: return
    u = (t - t0) / duree
    anneau(c, cx, cy, mix(r0, r1, sortie(u)), couleur, ep * (1 - u) + 1, 1 - u)

def etincelles(c, cx, cy, t, t0, n=8, r=110, couleur=C["vert"]):
    if t < t0 or t > t0 + 0.5: return
    u = (t - t0) / 0.5
    for k in range(n):
        a = k / n * 2 * math.pi
        d0, d1 = r * 0.35 * sortie(u), r * sortie(u)
        trait(c, cx + math.cos(a) * d0, cy + math.sin(a) * d0, cx + math.cos(a) * d1, cy + math.sin(a) * d1, couleur, 6 * (1 - u) + 1, 1 - u ** 2)

# ───────────────────────────── rendu
def surface():
    return skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))

def image_rgba(dessine, t, flou=0):
    """une image à t ; flou>1 : moyenne de sous-images sur un demi-intervalle (flou de mouvement)"""
    s = surface(); c = s.getCanvas()
    if flou <= 1:
        dessine(c, t)
        return s.toarray()
    acc = None
    for k in range(flou):
        tk = t + (k / (flou - 1) - 0.5) * (0.5 / FPS)
        c.clear(skia.ColorWHITE); dessine(c, tk)
        a = s.toarray().astype(np.uint16)
        acc = a if acc is None else acc + a
    return (acc // flou).astype(np.uint8)

def encode_segment(args):
    """rend les images [i0, i1) et les encode dans un fichier H.264"""
    module, i0, i1, sortie_mp4 = args
    import importlib
    sc = importlib.import_module(module)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-g", "120", "-bf", "2",
           "-x264-params", "keyint=120:min-keyint=120:scenecut=0", "-threads", "2", sortie_mp4]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(i0, i1):
        t = i / FPS
        pr.stdin.write(image_rgba(sc.dessine, t, sc.flou_a(t)).tobytes())
    pr.stdin.close(); pr.wait()
    return sortie_mp4
