#!/usr/bin/env python3
"""Aperçus et rendu final — à lancer depuis le dossier du projet (celui qui contient scenes.py).

    cd video-factory/motion/CB-M01
    python3 ../moteur/rendu.py apercu 0.5 3.2 9.8 …   → apercus/planche.jpg (et une image PNG par temps)
    python3 ../moteur/rendu.py video                  → renders/image.mp4 (sans son), 3 processus
"""
import os, sys, pathlib, subprocess, time
ICI = pathlib.Path.cwd()                      # le projet
sys.path.insert(0, str(ICI))                  # (aussi pour les processus de rendu)
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw
import moteur, scenes

def apercu(temps):
    (ICI / "apercus").mkdir(exist_ok=True)
    vignettes = []
    for t in temps:
        a = moteur.image_rgba(scenes.dessine, t, scenes.flou_a(t))
        im = Image.fromarray(a[..., :3])
        im.save(ICI / "apercus" / f"t{t:06.2f}.png")
        vignettes.append((t, im.resize((270, 480), Image.LANCZOS)))
    n = len(vignettes); cols = min(4, n); lig = (n + cols - 1) // cols
    planche = Image.new("RGB", (cols * 272, lig * 482), (40, 40, 40)); d = ImageDraw.Draw(planche)
    for k, (t, im) in enumerate(vignettes):
        x, y = (k % cols) * 272 + 1, (k // cols) * 482 + 1
        planche.paste(im, (x, y)); d.text((x + 5, y + 4), f"{t:.2f}", fill=(255, 0, 0))
    planche.save(ICI / "apercus" / "planche.jpg", quality=82)

def video(nproc=3):
    (ICI / "renders").mkdir(exist_ok=True)
    N = scenes.NB_IMAGES
    # préchauffage : le processus principal extrait d'abord les images des vidéos de la banque,
    # pour que les processus de rendu ne les extraient pas en même temps
    for tt in np.arange(0.0, N / moteur.FPS, 0.4):
        moteur.image_rgba(scenes.dessine, float(tt), 1)
    bornes = np.linspace(0, N, nproc * 2 + 1).astype(int)   # 6 segments répartis sur 3 processus
    taches = [("scenes", int(bornes[k]), int(bornes[k + 1]), str(ICI / "renders" / f"seg{k}.mp4")) for k in range(len(bornes) - 1)]
    t0 = time.time()
    with Pool(nproc) as pool:
        for f in pool.imap_unordered(moteur.encode_segment, taches):
            print("fini", pathlib.Path(f).name, f"{time.time() - t0:.0f}s", flush=True)
    liste = ICI / "renders" / "segments.txt"
    liste.write_text("".join(f"file '{tache[3]}'\n" for tache in taches))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(ICI / "renders" / "image.mp4")], check=True)
    print("vidéo sans son :", ICI / "renders" / "image.mp4", f"{time.time() - t0:.0f}s")

if __name__ == "__main__":
    if sys.argv[1] == "apercu":
        apercu([float(x) for x in sys.argv[2:]])
    else:
        video()
