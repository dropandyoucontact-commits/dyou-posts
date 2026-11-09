#!/usr/bin/env python3
"""Le hook ecrit d'AC-M09 : une phrase tenue a l'ecran, sans voix (modele @darkearth)."""
import math, pathlib, sys
import skia
ICI = pathlib.Path.cwd()
sys.path.insert(0, str(pathlib.Path("../moteur").resolve()))
import moteur
moteur.PROJET = ICI
from moteur import W, H, texte, borne, ajuste

FPS, DUREE = 20, 9.0
CX, FAM = 495, "noir"

# (lignes, apparition, taille)
BLOCS = [
    (["EN 2017, IL A JOUÉ", "UN HOMME DONT LE", "CERVEAU S'ÉTEIGNAIT."], 0.55, 80, 1020),
    (["NEUF ANS PLUS TARD,", "C'EST CE QUI L'A T*É."], 5.10, 80, 1360),
]

def pose(c, mot, y, taille, a):
    tl = ajuste(mot, 720, taille, FAM, -0.02)
    r = max(3, int(tl * 0.05))
    for ang in range(0, 360, 30):
        dx, dy = r*math.cos(math.radians(ang)), r*math.sin(math.radians(ang))
        texte(c, mot, CX+dx, y+dy, tl, "#000000", FAM, "centre", -0.02, a*0.85)
    texte(c, mot, CX, y+r*1.7, tl, "#000000", FAM, "centre", -0.02, a*0.45)
    texte(c, mot, CX, y, tl, "#FFFFFF", FAM, "centre", -0.02, a)

out = pathlib.Path("texte-hook"); out.mkdir(exist_ok=True)
for f in out.glob("*.png"): f.unlink()
surf = skia.Surface(W, H)
n = int(round(DUREE * FPS))
for k in range(n):
    t = k / FPS
    c = surf.getCanvas(); c.clear(skia.Color4f(0, 0, 0, 0))
    for lignes, t0, taille, y0 in BLOCS:
        if t < t0: continue
        a = borne((t - t0) / 0.55)
        for i, l in enumerate(lignes):
            pose(c, l, y0 + i * int(taille * 1.16), taille, a)
    surf.makeImageSnapshot().save(str(out / f"h{k:05d}.png"), skia.kPNG)
print(n, "images de hook")
