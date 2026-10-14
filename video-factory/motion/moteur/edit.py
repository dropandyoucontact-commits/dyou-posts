"""Edit d'une vidéo tournée (15/10/2026) : on garde l'image de Youssef, on remplace la voix par Léo (changeur de voix,
même rythme), et on habille : petits sous-titres centrés dans la zone que TikTok laisse libre, pastilles posées sur le
mot qui les appelle, coups de zoom, logo DROP&YOU à la fin.

Chaque vidéo garde un `montage.py` qui fixe ses mots (texte corrigé + temps whisper), ses pastilles et ses zooms,
puis appelle `Edit(...).apercu(...)`, `.video()` et `.son()`.

Zone sûre TikTok (1080 × 1920) : la légende et le nom du compte occupent le bas jusqu'à y ≈ 1500, la colonne des
boutons occupe x > 930 entre y ≈ 850 et 1700, le haut (onglets) jusqu'à y ≈ 170. Les sous-titres tiennent sur une
seule ligne de 760 px au plus, centrée sur x = 540, autour de y = 1250.
"""
import math, pathlib, subprocess
import numpy as np, skia
import moteur
from moteur import hexa, borne, mix, prog, entree, rebond, texte, largeur, hauteurLigne, peinture, disque, icone, image, taille_img, Calque

W, H, FPS = 1080, 1920, 30
POLICE = "xgras"                  # Inter Display ExtraBold
JAUNE = "#FFD60A"
Y_SOUS = 1250                      # centre de la ligne de sous-titres
LARG_SOUS = 760
VOLUME_LUFS = -13                  # demande du 15/10 : au niveau de la norme TikTok (−14), un poil au-dessus, crête −1 dB
_ECH = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)
SONS = pathlib.Path(__file__).resolve().parent / "sons"


# ─────────────────────────────────────────── sous-titres
def groupes(mots, taille=60, larg=LARG_SOUS, max_mots=4, pause=0.55, fin=None):
    """mots = [(texte, t)] → lignes de 1 à 4 mots ; coupe après une ponctuation, sur une pause, ou quand ça déborde.
    Chaque groupe : dict(mots=[(texte, t)], t0, t1)."""
    gs, cur = [], []
    for k, (m, t) in enumerate(mots):
        if cur:
            w = largeur(" ".join(x for x, _ in cur + [(m, t)]), taille, POLICE, 0.0)
            coupe = (len(cur) >= max_mots or w > larg or cur[-1][0][-1] in ".,?!:" or t - cur[-1][1] > pause + 0.35)
            if coupe: gs.append(cur); cur = []
        cur.append((m, t))
    if cur: gs.append(cur)
    out = []
    for i, g in enumerate(gs):
        t_der = g[-1][1]
        suivant = gs[i + 1][0][1] if i + 1 < len(gs) else (fin if fin is not None else t_der + 1.0)
        out.append(dict(mots=g, t0=g[0][1], t1=min(suivant - 0.07, t_der + 0.35 + 0.08 * len(g[-1][0]) + pause)))
    return out


def _calque_ombre(c):
    """contour sombre serré + ombre douce : lisible sur n'importe quel fond, sans gros contour de karaoké"""
    f = skia.ImageFilters.Compose(skia.ImageFilters.DropShadow(0, 5, 10, 10, hexa("#000000", 0.55)),
                                  skia.ImageFilters.DropShadow(0, 0, 2.2, 2.2, hexa("#000000", 0.9)))
    c.saveLayer(None, skia.Paint(ImageFilter=f))


def sous_titres(c, t, gs, taille=60, masque=()):
    """la ligne est placée d'un bloc (les mots ne bougent pas quand le suivant arrive), chaque mot se pose à son temps
    (petit saut + fondu), le mot dit en ce moment est jaune ; masque = [(t0, t1)] où rien ne s'affiche"""
    if any(a <= t <= b for a, b in masque): return
    esp = taille * 0.34
    hl = hauteurLigne(taille, POLICE)
    for g in gs:
        if not (g["t0"] - 0.05 <= t <= g["t1"]): continue
        o = prog(t, g["t1"] - 0.08, 0.08, entree)
        ws = [largeur(m, taille, POLICE, 0.0) for m, _ in g["mots"]]
        x = 540 - (sum(ws) + esp * (len(ws) - 1)) / 2
        _calque_ombre(c)
        for k, ((m, tm), w) in enumerate(zip(g["mots"], ws)):
            if t >= tm - 0.05:
                u = prog(t, tm - 0.05, 0.16, lambda v: rebond(v, 2.0))
                suiv = g["mots"][k + 1][1] if k + 1 < len(g["mots"]) else g["t1"]
                actif = tm - 0.05 <= t < suiv - 0.05
                s = mix(0.82, 1.0, u) * (1.04 if actif else 1.0)
                cx, cy = x + w / 2, Y_SOUS
                c.save(); c.translate(cx, cy + 10 * (1 - u) - 14 * o); c.scale(s, s); c.translate(-cx, -cy)
                texte(c, m, x, Y_SOUS - hl / 2, taille, JAUNE if actif else "#FFFFFF", POLICE, track=0.0, alpha=borne(u * 2.5) * (1 - o))
                c.restore()
            x += w + esp
        c.restore()


# ─────────────────────────────────────────── pastilles et listes
def _ombre_rr(c, rr, opa=0.32, dy=10, flou=18):
    p = skia.Paint(AntiAlias=True, Color=hexa("#000000", opa), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, flou))
    c.save(); c.translate(0, dy); c.drawRRect(rr, p); c.restore()


def _pastille_corps(c, lab, ic, coul, taille, x, y, check=False):
    """pastille blanche : disque de couleur + icône, texte sombre ; (x, y) = centre gauche ; renvoie la largeur"""
    tw = largeur(lab, taille, POLICE, 0.0)
    h = taille * 1.9; d = h - 18
    w = d + 24 + tw + (h * 0.62 + 16 if check else 0) + 34
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - h / 2, w, h), h / 2, h / 2)
    _ombre_rr(c, rr); c.drawRRect(rr, peinture("#FFFFFF"))
    disque(c, x + 9 + d / 2, y, d / 2, coul)
    if ic == "point": pass
    elif ic: icone(c, ic, x + 9 + d / 2, y, d * 0.56, "#FFFFFF", 2.4)
    texte(c, lab, x + d + 24, y - hauteurLigne(taille, POLICE) / 2, taille, "#141414", POLICE, track=0.0)
    if check:
        cx = x + w - 26 - h * 0.31
        disque(c, cx, y, h * 0.3, "#22C55E"); icone(c, "check", cx, y, h * 0.36, "#FFFFFF", 3.2)
    return w


def pastille(c, t, t0, t1, cx, cy, lab, ic, coul, taille=44, rot=-4, check=False, depuis=0):
    """pastille qui saute en place sur son mot (depuis = −1 / +1 : glisse de la gauche / de la droite), flotte, puis se retire"""
    a = prog(t, t0, 0.36, lambda v: rebond(v, 1.8))
    o = prog(t, t1, 0.16, entree)
    if a <= 0 or o >= 1: return
    tw = largeur(lab, taille, POLICE, 0.0); h = taille * 1.9
    w = (h - 18) + 24 + tw + (h * 0.62 + 16 if check else 0) + 34
    s = mix(0.4, 1.0, a) * (1 - 0.3 * o)
    c.save(); c.translate(cx + depuis * 280 * (1 - borne(a)) + 6 * math.sin(t * 2.1), cy + 6 * math.sin(t * 3.1) - 30 * o)
    c.rotate(rot + 1.5 * math.sin(t * 2.4)); c.scale(s, s)
    with Calque(c, borne(a * 3) * (1 - o)):
        _pastille_corps(c, lab, ic, coul, taille, -w / 2, 0, check)
    c.restore()


def liste(c, t, items, t1, x, y0, pas=112, taille=44):
    """lignes qui tombent une à une (items = [(texte, icône, couleur, t)]), cochées en vert, alignées à gauche sur x"""
    o = prog(t, t1, 0.16, entree)
    if o >= 1: return
    for k, (lab, ic, coul, tk) in enumerate(items):
        a = prog(t, tk - 0.04, 0.34, lambda v: rebond(v, 1.7))
        if a <= 0: continue
        y = y0 + k * pas
        c.save(); c.translate(-240 * (1 - borne(a)) * (1 if k % 2 else -1) * 0 + 0, -18 * (1 - a) - 26 * o)
        c.translate(x, y); c.rotate(-2 + 1.2 * math.sin(t * 2 + k)); c.scale(mix(0.6, 1, a), mix(0.6, 1, a))
        with Calque(c, borne(a * 3) * (1 - o)):
            _pastille_corps(c, lab, ic, coul, taille, 0, 0, check=True)
        c.restore()


def logo_fin(c, t, t0, t1=None, y=860, larg=620, sous=None):
    """logo DROP&YOU blanc qui arrive en grand puis se pose, voile sombre derrière ; sous = petite ligne sous le logo"""
    a = prog(t, t0, 0.42, lambda v: rebond(v, 1.5))
    o = prog(t, t1, 0.15, entree) if t1 else 0.0
    if a <= 0 or o >= 1: return
    voile = skia.Paint(AntiAlias=True)
    voile.setShader(skia.GradientShader.MakeRadial(skia.Point(540, y), 760, [hexa("#000000", 0.55 * borne(a) * (1 - o)), hexa("#000000", 0)], [0, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), voile)
    iw, ih = taille_img("logo-dy-blanc"); lh = larg * ih / iw
    s = mix(1.5, 1.0, borne(a)) * a
    c.save(); c.translate(540, y); c.scale(s, s)
    c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.DropShadow(0, 8, 16, 16, hexa("#000000", 0.6))))
    with Calque(c, borne(a * 2) * (1 - o)):
        image(c, "logo-dy-blanc", -larg / 2, -lh / 2, larg)
    c.restore(); c.restore()
    if sous:
        b = prog(t, t0 + 0.3, 0.3)
        with Calque(c, b * (1 - o)):
            _calque_ombre(c)
            texte(c, sous, 540, y + lh / 2 + 34 + 12 * (1 - b), 46, "#FFFFFF", POLICE, "centre", 0.0)
            c.restore()


def bouton_enregistre(c, t, t0, t1, cx=540, cy=1080):
    """pastille « Enregistre la vidéo » avec le signet qui se remplit"""
    a = prog(t, t0, 0.36, lambda v: rebond(v, 1.8)); o = prog(t, t1, 0.15, entree)
    if a <= 0 or o >= 1: return
    lab = "Enregistre la vidéo"; taille = 42
    tw = largeur(lab, taille, POLICE, 0.0); h = 86; w = tw + 130
    c.save(); c.translate(cx, cy + 5 * math.sin(t * 3)); c.scale(mix(0.5, 1, a), mix(0.5, 1, a))
    with Calque(c, borne(a * 3) * (1 - o)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        _ombre_rr(c, rr); c.drawRRect(rr, peinture(JAUNE))
        rempli = prog(t, t0 + 0.45, 0.2)
        icone(c, "bookmark", -w / 2 + 52, 0, 44, "#141414", 2.6)
        if rempli > 0:
            c.save(); c.clipRect(skia.Rect.MakeXYWH(-w / 2 + 30, 22 - 44 * rempli, 44, 44 * rempli))
            icone(c, "bookmark", -w / 2 + 52, 0, 44, "#141414", 7.0); c.restore()
        texte(c, lab, -w / 2 + 92, -hauteurLigne(taille, POLICE) / 2, taille, "#141414", POLICE, track=0.0)
    c.restore()


# ─────────────────────────────────────────── l'image
def zoom(t, coups, lent=0.03, duree=None):
    """léger travelling avant continu + coups de zoom (t, force) qui claquent puis redescendent"""
    s = 1.0 + lent * borne(t / duree) if duree else 1.0
    for tc, f in coups:
        if tc - 0.02 <= t <= tc + 0.9:
            u = (t - tc + 0.02) / 0.92
            s += f * (math.sin(math.pi * min(1, u * 3.2)) if u < 0.16 else (1 - (u - 0.16) / 0.84) ** 2)
    return s


def mesure(f):
    """(volume intégré LUFS, crête vraie dBFS)"""
    import re
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])


class Edit:
    def __init__(self, dossier, source, duree, dessin, coups=(), grade="eq=contrast=1.05:saturation=1.1:gamma=0.98,unsharp=5:5:0.45:5:5:0.0",
                 centre_zoom=(540, 900)):
        self.P = pathlib.Path(dossier); moteur.PROJET = self.P
        self.src, self.duree, self.dessin, self.coups, self.grade, self.cz = source, duree, dessin, coups, grade, centre_zoom
        self.sfx = []

    def son_(self, t, nom, gain):
        self.sfx.append((round(t, 3), nom, gain))

    def _vf(self):
        return f"fps={FPS},scale={W}:{H}:flags=lanczos,{self.grade}"

    def image_a(self, t, buf):
        img = skia.Image.fromarray(np.frombuffer(buf, np.uint8).reshape(H, W, 4), colorType=skia.kRGBA_8888_ColorType)
        surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
        c = surf.getCanvas()
        s = zoom(t, self.coups, duree=self.duree); cx, cy = self.cz
        c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy)
        c.drawImageRect(img, skia.Rect.MakeWH(W, H), _ECH, skia.Paint()); c.restore()
        self.dessin(c, t)
        return surf.toarray()

    def apercu(self, temps):
        from PIL import Image, ImageDraw
        (self.P / "apercus").mkdir(exist_ok=True)
        vign = []
        dsrc = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(self.src)],
                                    capture_output=True, text=True).stdout)
        for t in temps:
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{min(t, dsrc - 0.1):.3f}", "-i", str(self.src), "-frames:v", "1", "-vf", f"scale={W}:{H}:flags=lanczos,{self.grade}",
                                  "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True).stdout
            im = Image.fromarray(self.image_a(t, raw)[..., :3]); im.save(self.P / "apercus" / f"m_{t:05.2f}.jpg", quality=88)
            vign.append((t, im.resize((270, 480))))
        cols = min(5, len(vign)); lig = (len(vign) + cols - 1) // cols
        pl = Image.new("RGB", (cols * 272, lig * 482), (30, 30, 30)); d = ImageDraw.Draw(pl)
        for k, (t, im) in enumerate(vign):
            x, y = (k % cols) * 272 + 1, (k // cols) * 482 + 1
            pl.paste(im, (x, y)); d.text((x + 5, y + 4), f"{t:.2f}", fill=(255, 0, 0))
        pl.save(self.P / "apercus" / "planche.jpg", quality=85)

    def video(self):
        (self.P / "renders").mkdir(exist_ok=True)
        lec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(self.src), "-vf", self._vf(), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                                "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(self.P / "renders" / "image.mp4")],
                               stdin=subprocess.PIPE)
        n, taille = int(self.duree * FPS), W * H * 4
        prec = None
        for k in range(n):
            b = lec.stdout.read(taille)
            if len(b) < taille:
                if prec is None: break
                b = prec                       # durée plus longue que le rush : la dernière image tient (carton de fin)
            prec = b
            enc.stdin.write(self.image_a(k / FPS, b).tobytes())
            if k % 90 == 0: print(f"{k / FPS:.1f} s", flush=True)
        lec.kill(); enc.stdin.close(); enc.wait()

    def son(self, voix, nom):
        """voix Léo (sortie du changeur de voix, très basse) : nettoyage, présence, compression, bruitages dessous,
        puis volume final à VOLUME_LUFS intégrés, crête vraie −1 dB (suréchantillonné pour que l'AAC ne dépasse pas)"""
        a = self.P / "audio"; a.mkdir(exist_ok=True)
        v = a / "voix.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voix), "-af",
                        "highpass=f=80,equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=10000:t=h:w=0.7:g=1.5,"
                        "acompressor=threshold=0.08:ratio=3:attack=5:release=90:makeup=2",
                        "-ac", "1", "-ar", "48000", "-c:a", "pcm_f32le", str(v)], check=True)
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
        x *= 10 ** ((-16 - mesure(v)[0]) / 20)            # voix posée à −16 LUFS avant les bruitages (gains des sons relatifs à ça)
        n = int(self.duree * 48000)
        x = np.pad(x, (0, max(0, n - len(x))))[:n]
        for t0, nomson, g in self.sfx:
            s = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(SONS / f"{nomson}.wav"), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                             capture_output=True).stdout, np.float32) * 10 ** (g / 20)
            i0 = int(t0 * 48000); i1 = min(len(x), i0 + len(s))
            if 0 <= i0 < len(x): x[i0:i1] += s[:i1 - i0]
        brut = a / "mix-brut.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", str(brut)],
                       input=x.tobytes(), check=True)
        mixw = a / "mix.wav"
        # gain réglé par mesure (3 essais au plus) : gain, limiteur à −1 dB vrai (suréchantillonné), mesure EBU R128
        gain = VOLUME_LUFS - mesure(brut)[0]
        for _ in range(3):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(brut), "-af",
                            f"aresample=192000,volume={gain:.2f}dB,alimiter=limit=0.87:attack=0.5:release=40:level=false,"
                            "alimiter=limit=0.87:attack=0.1:release=20:level=false,aresample=48000,pan=stereo|c0=c0|c1=c0",
                            "-c:a", "pcm_s16le", str(mixw)], check=True)
            i, _ = mesure(mixw)
            if abs(i - VOLUME_LUFS) < 0.25: break
            gain += VOLUME_LUFS - i
        (self.P / "video").mkdir(exist_ok=True)
        out = self.P / "video" / f"{nom}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(self.P / "renders" / "image.mp4"), "-i", str(mixw), "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out)], check=True)
        return out
