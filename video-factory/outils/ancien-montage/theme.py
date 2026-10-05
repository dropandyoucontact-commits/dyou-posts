#!/usr/bin/env python3
"""Fonds et palettes des vidéos de la factory.

Un seul fond violet sur cinquante vidéos, c'est une bibliothèque qui se
ressemble. Chaque thème définit sa palette et sa texture de fond — dégradé,
quadrillage, rayons, grain — et le montage n'appelle que `fond()` et les
couleurs du thème, jamais une valeur en dur.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920

THEMES = {
    # nuit : le violet ChinaBook, pour les plans de marque
    "nuit": dict(haut=(46, 26, 102), bas=(14, 11, 26), accent=(150, 92, 255),
                 accent2=(190, 168, 255), texte=(249, 249, 252), sourd=(188, 184, 212),
                 carte=(25, 22, 36), bord=(64, 58, 92), texture="rayons"),
    # encre : noir et or, pour les plans de prix — le chiffre doit dominer
    "encre": dict(haut=(26, 24, 22), bas=(8, 8, 9), accent=(214, 174, 52),
                  accent2=(242, 212, 110), texte=(250, 248, 242), sourd=(186, 180, 166),
                  carte=(23, 21, 18), bord=(74, 66, 44), texture="quadrillage"),
    # sable : fond clair, texte noir — casse la série, très premium
    "sable": dict(haut=(243, 238, 229), bas=(222, 214, 201), accent=(28, 26, 24),
                  accent2=(124, 58, 237), texte=(22, 20, 18), sourd=(96, 90, 82),
                  carte=(252, 250, 246), bord=(206, 197, 183), texture="quadrillage"),
    # acier : gris bleu froid, pour la logistique et les chiffres
    "acier": dict(haut=(38, 50, 66), bas=(12, 16, 22), accent=(86, 170, 226),
                  accent2=(158, 212, 248), texte=(244, 248, 252), sourd=(176, 190, 206),
                  carte=(22, 29, 39), bord=(58, 76, 96), texture="quadrillage"),
    # braise : noir vers rouge profond, pour ce qui coûte cher
    "braise": dict(haut=(92, 20, 26), bas=(12, 8, 10), accent=(232, 92, 92),
                   accent2=(255, 162, 150), texte=(252, 246, 244), sourd=(206, 184, 180),
                   carte=(30, 16, 18), bord=(92, 48, 48), texture="rayons"),
}


def _degrade(haut, bas, courbe=1.8):
    g = Image.new("RGB", (2, H)); px = g.load()
    for y in range(H):
        k = (1 - y/H)**courbe
        px[0, y] = px[1, y] = tuple(int(b + (h-b)*k) for h, b in zip(haut, bas))
    return g.resize((W, H), Image.BILINEAR)


def _quadrillage(img, couleur, pas=90, opacite=26):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    for x in range(0, W+1, pas): d.line([(x, 0), (x, H)], fill=couleur+(opacite,))
    for y in range(0, H+1, pas): d.line([(0, y), (W, y)], fill=couleur+(opacite,))
    img.alpha_composite(c)


def _rayons(img, couleur, n=9, opacite=16):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    cx, cy = W//2, -420
    for i in range(n):
        a = math.pi*(0.16 + 0.68*i/(n-1))
        d.polygon([(cx, cy),
                   (cx+math.cos(a)*2600, cy+math.sin(a)*2600),
                   (cx+math.cos(a+0.045)*2600, cy+math.sin(a+0.045)*2600)],
                  fill=couleur+(opacite,))
    img.alpha_composite(c.filter(ImageFilter.GaussianBlur(6)))


_CACHE = {}


def fond(nom="nuit"):
    """Image de fond du thème, calculée une fois puis gardée en mémoire."""
    if nom in _CACHE: return _CACHE[nom].copy()
    t = THEMES[nom]
    img = _degrade(t["haut"], t["bas"]).convert("RGBA")
    if t["texture"] == "quadrillage": _quadrillage(img, t["accent"])
    elif t["texture"] == "rayons":    _rayons(img, t["accent"])
    _CACHE[nom] = img
    return img.copy()


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path("/private/tmp/claude-501/-Users-mohamedelhadad/"
                       "888844c7-09f5-4498-847c-fd72fa17e642/scratchpad")
    noms = list(THEMES)
    pl = Image.new("RGB", (300*len(noms), 540), (20, 20, 24))
    d = ImageDraw.Draw(pl)
    for i, n in enumerate(noms):
        pl.paste(fond(n).convert("RGB").resize((280, 498)), (300*i+10, 32))
        d.text((300*i+12, 10), n, fill=(255, 255, 255))
    pl.save(out/"themes.png"); print(out/"themes.png")
