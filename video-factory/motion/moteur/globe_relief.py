"""Globe blanc sculpté (MONARQUE, 15/10/2026) : sphère blanc lavande, continents en relief éclairés de haut à gauche,
liseré bleu en bas à droite — le rendu de la photo de référence du client, mais en vraie 3D qui tourne.

Cartes équirectangulaires (three-globe, d'après la NASA) : media/globe-relief.png (altitude) et media/globe-eau.png
(blanc = océan). Projection orthographique ; globe_relief() renvoie une skia.Image carrée de côté 2R (cache par angle).
"""
import functools, math
import numpy as np
import skia
from PIL import Image, ImageFilter
from moteur import ICI

_TW, _TH = 2048, 1024


@functools.lru_cache(maxsize=1)
def _cartes():
    eau = np.asarray(Image.open(ICI / "media" / "globe-eau.png").convert("L").resize((_TW, _TH), Image.BILINEAR), np.float32) / 255
    terre = 1 - eau
    alt = np.asarray(Image.open(ICI / "media" / "globe-relief.png").convert("L"), np.float32) / 255
    # hauteur : un socle net (les côtes en falaise, comme la photo) + le relief réel, adouci
    socle = np.asarray(Image.fromarray((terre * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)), np.float32) / 255
    h = 0.9 * socle + 2.6 * (alt ** 0.8) * terre
    # ombre portée des continents sur l'océan (lumière de haut à gauche : l'ombre tombe vers l'est et le sud)
    dec = np.roll(np.roll(socle, 5, 1), 4, 0)
    portee = np.asarray(Image.fromarray((np.clip(dec, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4)), np.float32) / 255
    portee = np.clip(portee - socle, 0, 1)
    # dérivées (est, nord) en unités de texture
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5
    gy = (np.roll(h, 1, 0) - np.roll(h, -1, 0)) * 0.5
    return terre, h, gx, gy, portee


def rotation(lon0, lat0):
    """matrice monde → vue : (lon0, lat0) face à la caméra"""
    l0, f0 = math.radians(lon0), math.radians(lat0)
    cy, sy = math.cos(-l0), math.sin(-l0)
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    cx, sx = math.cos(f0), math.sin(f0)
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    return rx @ ry


def projette(lon, lat, lon0, lat0, R, cx, cy, lift=0.0):
    """position écran d'un point (lon, lat) du globe centré en (cx, cy) ; z > 0 : face visible"""
    lo, la = math.radians(lon), math.radians(lat)
    v = np.array([math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo)]) * (1 + lift)
    x, y, z = rotation(lon0, lat0) @ v
    return cx + R * x, cy - R * y, z


def _hexf(s):
    s = s.lstrip("#"); return np.array([int(s[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


@functools.lru_cache(maxsize=8)
def _grille(R):
    n = 2 * R
    ys, xs = np.mgrid[0:n, 0:n].astype(np.float32)
    x = (xs + 0.5 - R) / R; y = (R - ys - 0.5) / R
    r2 = x * x + y * y
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    bord = np.clip((1 - np.sqrt(r2)) * R / 1.2, 0, 1)          # anticrénelage du contour
    return x, y, z, bord


@functools.lru_cache(maxsize=400)
def _globe(lon0, lat0, R, sombre):
    terre, h, gx, gy, portee = _cartes()
    x, y, z, bord = _grille(R)
    Mi = rotation(lon0, lat0).T                                  # vue → monde
    wx = Mi[0, 0] * x + Mi[0, 1] * y + Mi[0, 2] * z
    wy = Mi[1, 0] * x + Mi[1, 1] * y + Mi[1, 2] * z
    wz = Mi[2, 0] * x + Mi[2, 1] * y + Mi[2, 2] * z
    lat = np.arcsin(np.clip(wy, -1, 1)); lon = np.arctan2(wx, wz)
    u = (lon / (2 * np.pi) + 0.5) * _TW; v = (0.5 - lat / np.pi) * _TH
    i0 = np.floor(u).astype(np.int32); j0 = np.clip(np.floor(v).astype(np.int32), 0, _TH - 2)
    fu = (u - i0)[..., None] if False else (u - i0); fv = v - j0
    i0 %= _TW; i1 = (i0 + 1) % _TW; j1 = j0 + 1

    def ech(m):
        return (m[j0, i0] * (1 - fu) * (1 - fv) + m[j0, i1] * fu * (1 - fv) + m[j1, i0] * (1 - fu) * fv + m[j1, i1] * fu * fv)

    T, dx, dy, PO = ech(terre), ech(gx), ech(gy), ech(portee)
    pole = np.clip((1.45 - np.abs(lat)) / 0.15, 0, 1)            # pas de relief au pôle (singularité de la carte)
    dx, dy = dx * pole, dy * pole
    # repère tangent en vue : est = d/dlon, nord = d/dlat
    M = rotation(lon0, lat0)
    cl, sl, cf, sf = np.cos(lon), np.sin(lon), np.cos(lat), np.sin(lat)
    ex_w = np.stack([cl, np.zeros_like(cl), -sl])
    nx_w = np.stack([-sf * sl, cf, -sf * cl])
    ex = np.tensordot(M, ex_w, 1); no = np.tensordot(M, nx_w, 1)
    k = 3.2
    nxv = x - k * (dx * ex[0] + dy * no[0])
    nyv = y - k * (dx * ex[1] + dy * no[1])
    nzv = z - k * (dx * ex[2] + dy * no[2])
    nn = np.sqrt(nxv ** 2 + nyv ** 2 + nzv ** 2) + 1e-6
    nxv, nyv, nzv = nxv / nn, nyv / nn, nzv / nn
    L = np.array([-0.55, 0.62, 0.56]); L /= np.linalg.norm(L)
    lamb = np.clip(nxv * L[0] + nyv * L[1] + nzv * L[2], 0, 1)
    lamb_s = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1)        # la sphère seule (océans lisses)
    rim = np.clip(1 - z, 0, 1) ** 2.2 * np.clip(0.6 * x - 0.8 * y + 0.2, 0, 1)   # liseré bleu bas-droite
    if sombre:
        haut, bas, bleu = _hexf("#FFFFFF"), _hexf("#9EA3C8"), _hexf("#6F8CFF")
    else:
        haut, bas, bleu = _hexf("#FFFFFF"), _hexf("#C6C8E0"), _hexf("#7D93F0")
    ombre = T * lamb + (1 - T) * (0.15 * lamb + 0.85 * lamb_s)
    ombre = (0.08 + 0.92 * ombre) ** 1.25
    ombre = ombre * (1 - 0.32 * (1 - T)) * (1 - 0.45 * PO)   # océans en retrait, ombre portée des côtes
    col = bas[None, None, :] * (1 - ombre[..., None]) + haut[None, None, :] * ombre[..., None]
    col = col * (1 - 0.55 * rim[..., None]) + bleu[None, None, :] * 0.55 * rim[..., None]
    # léger voile lumineux sur les terres (le blanc sculpté de la photo)
    col = col + 0.05 * T[..., None] * ombre[..., None]
    a = bord
    rgba = np.concatenate([np.clip(col, 0, 1) * a[..., None], a[..., None]], -1)
    arr = np.ascontiguousarray((rgba * 255).astype(np.uint8))
    return skia.Image.fromarray(arr, colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kPremul_AlphaType)


def globe_relief(lon0, lat0, R, sombre=False):
    """image du globe (côté 2R) ; l'angle est arrondi à 0,25° pour le cache"""
    return _globe(round(lon0 * 4) / 4, round(lat0 * 4) / 4, int(R), sombre)


def dessine_globe(c, lon0, lat0, cx, cy, R, alpha=1.0, sombre=False, ombre_sol=True, Rimg=420):
    """globe de rayon R à l'écran ; l'image est toujours calculée à Rimg (cache stable quand R s'anime)"""
    if alpha <= 0.01 or R <= 1: return
    img = globe_relief(lon0, lat0, Rimg, sombre)
    if ombre_sol:
        p = skia.Paint(AntiAlias=True)
        col = (40, 50, 140) if sombre else (70, 80, 160)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx + R * 0.3, cy + R * 0.3), R * 1.3,
                                                   [skia.Color(*col, int((110 if sombre else 70) * alpha)), skia.Color(*col, 0)]))
        c.drawCircle(cx + R * 0.3, cy + R * 0.3, R * 1.3, p)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(alpha)
    c.drawImageRect(img, skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), skia.SamplingOptions(skia.FilterMode.kLinear), p)
