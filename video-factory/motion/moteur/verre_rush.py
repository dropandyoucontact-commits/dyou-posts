# -*- coding: utf-8 -*-
"""Fenetres « liquid glass » posees sur le rush, memes codes que DY-M18 (moteur/verre_studio.py) :
verre clair depoli, halo violet, lisere blanc -> lilas, reflet en biais. Ici le fond est une VRAIE
video : le verre floute et refracte ce qu'il y a derriere au lieu d'etre pose sur du papier."""
import math, skia

F = '/Users/mohamedelhadad/Desktop/dyou-posts/video-factory/motion/moteur/fontes/'
_tf = {}
def police(n):
    if n not in _tf: _tf[n] = skia.Typeface.MakeFromFile(F + n)
    return _tf[n]
GROS   = skia.Font(police('InterDisplay-Bold.ttf'), 1)
PETIT  = skia.Font(police('Inter-SemiBold.ttf'), 1)

ACCENT, ENCRE, GRIS = '#7B3FF2', '#211B33', '#6B6480'

def hexa(c, a=1.0):
    c = c.lstrip('#')
    r, v, b = int(c[0:2],16), int(c[2:4],16), int(c[4:6],16)
    return skia.Color4f(r/255, v/255, b/255, a).toColor()

def borne(v, a=0.0, b=1.0): return max(a, min(b, v))

def ressort(u, amp=1.15, k=5.2):
    if u >= 1: return 1.0
    return 1 - (1 - u) ** 2 * math.cos(u * k) * amp if u > 0 else 0.0

def douce(u): return u * u * (3 - 2 * u)

def larg(txt, taille, font, track=0.0):
    f = skia.Font(font.getTypeface(), taille)
    return f.measureText(txt) + track * taille * max(0, len(txt) - 1)

def texte(c, txt, x, y, taille, col, font, ancre='gauche', track=0.0, alpha=1.0):
    f = skia.Font(font.getTypeface(), taille); f.setSubpixel(True); f.setEdging(skia.Font.Edging.kAntiAlias)
    w = larg(txt, taille, font, track)
    if ancre == 'droite': x -= w
    elif ancre == 'centre': x -= w / 2
    p = skia.Paint(AntiAlias=True, Color=hexa(col, alpha))
    if track == 0.0:
        c.drawString(txt, x, y, f, p); return
    for ch in txt:
        c.drawString(ch, x, y, f, p)
        x += f.measureText(ch) + track * taille

def fenetre(c, fond, x, y, w, h, r, t_ent, alpha=1.0, lueur=1.0):
    """fond = skia.Image de l'image video en cours ; le verre prend ce qu'il y a derriere, le floute,
    l'eclaircit, et le refracte legerement sur les bords."""
    if alpha <= 0.004 or w < 2 or h < 2: return
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    k = max(0.4, min(w, h) / 160)
    c.saveLayerAlpha(None, int(255 * borne(alpha)))
    # ombre portee violette
    p = skia.Paint(AntiAlias=True, Color=hexa('#2A1055', 0.30),
                   MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16 * k))
    c.save(); c.translate(0, 10 * k); c.drawRRect(rr, p); c.restore()
    # halo violet
    if lueur > 0:
        p = skia.Paint(AntiAlias=True, Color=hexa(ACCENT, 0.26 * lueur),
                       MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 13 * k))
        c.drawRRect(rr, p)
    c.save(); c.clipRRect(rr, doAntiAlias=True)
    # 1. le fond floute (depoli)
    pb = skia.Paint(ImageFilter=skia.ImageFilters.Blur(17, 17, skia.TileMode.kClamp))
    c.drawImage(fond, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), pb)
    # 2. refraction : le meme fond agrandi, garde seulement sur l'anneau du bord
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 9 * k, y + 9 * k, w - 18 * k, h - 18 * k),
                                      max(1, r - 9 * k), max(1, r - 9 * k)), skia.ClipOp.kDifference, True)
    c.translate(x + w / 2, y + h / 2); c.scale(1.14, 1.14); c.translate(-(x + w / 2), -(y + h / 2))
    c.drawImage(fond, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear),
                skia.Paint(ImageFilter=skia.ImageFilters.Blur(9, 9, skia.TileMode.kClamp), Alphaf=0.85))
    c.restore()
    # 3. le depoli clair par-dessus (c'est lui qui donne la carte blanche de DY-M18)
    pf = skia.Paint(AntiAlias=True)
    pf.setShader(skia.GradientShader.MakeLinear(
        [skia.Point(x, y), skia.Point(x + w * 0.5, y + h)],
        [hexa('#FFFFFF', 0.80), hexa('#F8F5FE', 0.74), hexa('#EFEAFB', 0.78)]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pf)
    # 4. reflet en biais
    rf = skia.Paint(AntiAlias=True)
    rf.setShader(skia.GradientShader.MakeLinear(
        [skia.Point(x, y), skia.Point(x + w * 0.5, y + h * 0.5)],
        [hexa('#FFFFFF', 0.0), hexa('#FFFFFF', 0.75), hexa('#FFFFFF', 0.0)], [0.28, 0.35, 0.46]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), rf)
    # 5. halo violet interieur en bas
    if lueur > 0:
        lb = skia.Paint(AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9 * k))
        lb.setShader(skia.GradientShader.MakeRadial(skia.Point(x + w / 2, y + h), w * 0.55,
                                                    [hexa(ACCENT, 0.20 * lueur), hexa(ACCENT, 0.0)]))
        c.drawRect(skia.Rect.MakeXYWH(x, y + h - 46 * k, w, 46 * k), lb)
    # 6. balayage unique a l'ouverture
    if 0.0 < t_ent < 1.0:
        u = mixe(-0.35, 1.35, douce(t_ent))
        bp = skia.Paint(AntiAlias=True)
        x0 = x + w * u
        bp.setShader(skia.GradientShader.MakeLinear(
            [skia.Point(x0 - 80, y), skia.Point(x0 + 80, y + h)],
            [hexa('#FFFFFF', 0), hexa('#FFFFFF', 0.55), hexa('#FFFFFF', 0)]))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), bp)
    c.restore()
    # 7. lisere blanc -> lilas
    li = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.4, 1.9 * k))
    li.setShader(skia.GradientShader.MakeLinear(
        [skia.Point(x, y), skia.Point(x + w, y + h)],
        [hexa('#FFFFFF', 1.0), hexa('#C9B6FF', 0.65), hexa('#FFFFFF', 0.9), hexa('#9C7BFF', 0.95)],
        [0.0, 0.4, 0.7, 1.0]))
    c.drawRRect(rr, li)
    c.restore()

def mixe(a, b, u): return a + (b - a) * u
