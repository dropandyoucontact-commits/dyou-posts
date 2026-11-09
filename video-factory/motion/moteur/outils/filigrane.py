#!/usr/bin/env python3
"""Pose un filigrane DYOU en diagonale sur toute l'image — version d'aperçu envoyée au client.

    cd video-factory/motion/VX-M01
    /usr/bin/python3 ../moteur/outils/filigrane.py video/VX-M01.mp4

Règle posée par Youssef le 29/10/2026 : l'aperçu part AVANT paiement, il doit donc être
inutilisable tel quel et impossible à détourer — le filigrane traverse toute l'image en
diagonale, se répète, et passe par-dessus le sujet. Le fichier propre ne part qu'après
règlement. Sort `<nom>-apercu.mp4` à côté de la source, sans toucher à l'original.
"""
import argparse, math, pathlib, subprocess, sys, tempfile

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))


def dalle(texte, w, h, pas, taille, angle, opacite):
    """fabrique la tuile du filigrane : le texte répété, incliné, sur fond transparent"""
    import skia
    from moteur import hexa
    import moteur
    s = skia.Surface(w, h)
    c = s.getCanvas()
    c.clear(0x00000000)
    c.save()
    c.translate(w / 2, h / 2)
    c.rotate(angle)
    c.translate(-w / 2, -h / 2)
    lignes = int(h / pas) + 6
    cols = int(w / (pas * 2.1)) + 4
    for i in range(-3, lignes):
        for j in range(-2, cols):
            x = j * pas * 2.1 + (pas * 1.05 if i % 2 else 0)
            y = i * pas
            moteur.texte(c, texte, x, y, taille, "#FFFFFF", "noir", alpha=opacite)
            moteur.texte(c, texte, x + 1.5, y + 1.5, taille, "#000000", "noir", alpha=opacite * 0.45)
    c.restore()
    return s.makeImageSnapshot()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("--texte", default="DYOU AGENCY  ·  APERÇU")
    p.add_argument("--opacite", type=float, default=0.22)
    p.add_argument("--taille", type=int, default=0, help="0 = proportionnel à la largeur")
    p.add_argument("--angle", type=float, default=-32.0)
    p.add_argument("--sortie", default=None)
    a = p.parse_args()

    src = pathlib.Path(a.source).resolve()
    if not src.exists(): sys.exit(f"introuvable : {src}")
    out = pathlib.Path(a.sortie) if a.sortie else src.with_name(src.stem + "-apercu.mp4")

    dim = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)],
                         capture_output=True, text=True).stdout.strip().split(",")
    w, h = int(dim[0]), int(dim[1])
    taille = a.taille or max(22, int(w * 0.040))
    pas = int(taille * 3.4)

    import skia
    img = dalle(a.texte, w, h, pas, taille, a.angle, a.opacite)
    tmp = pathlib.Path(tempfile.mkdtemp()) / "filigrane.png"
    img.save(str(tmp), skia.kPNG)

    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(tmp),
                    "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v]",
                    "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", str(out)], check=True)
    print("aperçu filigrané :", out)


if __name__ == "__main__":
    main()
