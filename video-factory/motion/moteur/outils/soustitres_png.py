#!/usr/bin/env python3
"""Couche de sous-titres mot à mot, en PNG transparents, à superposer à des archives.

    cd video-factory/motion/AC-M08
    /usr/bin/python3 ../moteur/outils/soustitres_png.py --duree 17.0 --fps 20 --sortie texte

Pourquoi des PNG et pas le moteur : sur le format ARCHIVES, l'image est une vraie vidéo, pas un
dessin. La faire passer image par image dans Skia remplirait le disque (≈ 1 Go de cache pour 70 s)
pour ne rien y ajouter. On ne rend donc que le TEXTE, en transparent, et ffmpeg le superpose.
L'ffmpeg de ce Mac n'a ni `drawtext` ni `subtitles` (pas de libass) : il n'y a pas d'autre voie.

Style repris de @darkearth (2,7 M de vues) : UN SEUL MOT à l'écran à la fois, capitales grasses
blanches, ombre portée, centré, dans le tiers bas — et rien d'autre.
"""
import argparse, json, pathlib, sys
import skia

ICI = pathlib.Path.cwd()
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import moteur
moteur.PROJET = ICI
from moteur import W, H, texte, largeur, hexa, borne, prog, sortie, ajuste


def rendre(mots, duree, fps, sortie_dir, taille, y, cx, fam, filigrane, censure):
    sortie_dir = pathlib.Path(sortie_dir); sortie_dir.mkdir(parents=True, exist_ok=True)
    for f in sortie_dir.glob("*.png"): f.unlink()
    n = int(round(duree * fps))
    surf = skia.Surface(W, H)
    for k in range(n):
        t = k / fps
        c = surf.getCanvas()
        c.clear(skia.Color4f(0, 0, 0, 0))
        # le mot en cours : celui dont le temps est passé et qui n'est pas encore remplacé
        cour = None
        for i, m in enumerate(mots):
            if m["t0"] - 0.06 <= t and (i + 1 >= len(mots) or t < mots[i + 1]["t0"] - 0.06):
                cour = (i, m); break
        if cour:
            i, m = cour
            mot = censure.get(i, m["w"]).upper().strip()
            if mot not in ("", "—"):
                tl = ajuste(mot, 900, taille, fam, -0.02)
                u = borne((t - (m["t0"] - 0.06)) / 0.09)          # apparition nette et courte
                a = 0.25 + 0.75 * u
                for dx, dy, al in ((0, 7, 0.55), (0, 0, 1.0)):     # ombre portée puis le mot
                    texte(c, mot, cx + dx, y + dy, tl, "#000000" if al < 1 else "#FFFFFF",
                          fam, "centre", -0.02, a * al)
        if filigrane:
            texte(c, filigrane, 108, 1500, 30, "#FFFFFF", "noir", "gauche", 0.2, 0.30)
        img = surf.makeImageSnapshot()
        img.save(str(sortie_dir / f"t{k:05d}.png"), skia.kPNG)
    return n


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--duree", type=float, required=True)
    p.add_argument("--fps", type=float, default=20.0)
    p.add_argument("--sortie", default="texte")
    p.add_argument("--taille", type=int, default=96)
    p.add_argument("--y", type=int, default=1210)
    p.add_argument("--cx", type=int, default=520)
    p.add_argument("--fam", default="noir")
    p.add_argument("--filigrane", default="RECTO CERVEAU")
    p.add_argument("--censure", default="", help="i:mot,i:mot — remplace l'affichage d'un mot (OCR de la modération)")
    a = p.parse_args()
    mots = json.loads((ICI / "timing.json").read_text())["mots"]
    cens = {}
    for bout in filter(None, a.censure.split(",")):
        i, m = bout.split(":", 1); cens[int(i)] = m
    n = rendre(mots, a.duree, a.fps, a.sortie, a.taille, a.y, a.cx, a.fam, a.filigrane, cens)
    total = sum(f.stat().st_size for f in pathlib.Path(a.sortie).glob("*.png"))
    print(f"{n} images à {a.fps} i/s dans {a.sortie}/ — {total/1e6:.1f} Mo")
