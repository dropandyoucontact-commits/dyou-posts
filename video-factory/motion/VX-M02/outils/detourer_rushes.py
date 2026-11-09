#!/usr/bin/env python3
"""Détoure les rushes du client (rembg u2net, CPU) sur les seules plages utilisées par le montage et
recompose chaque rush sur un fond sombre « glace », en conservant sa durée et son minutage :
media/videos/<nom>-d.mov a la même longueur que l'original (noir hors des plages), donc scenes.py
n'a qu'à changer le nom. Masques lissés dans le temps (moyenne sur 3 images) pour limiter le papillotement.

    /usr/bin/python3 outils/detourer_rushes.py plages-detourage.json [--test IMG_3413 1.5 0.7]
"""
import json, pathlib, subprocess, sys, time
import numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session

P = pathlib.Path(__file__).resolve().parent.parent
FPS = 30
W = H = None
SESSION = new_session("u2net", providers=["CPUExecutionProvider"])


def dims(src):
    """largeur × hauteur TELLES QU'AFFICHÉES (les .mov iPhone sont 1920×1080 avec un drapeau de rotation)"""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation",
                          "-of", "default=nw=1", str(src)], capture_output=True, text=True).stdout
    d = dict(l.split("=") for l in out.splitlines() if "=" in l)
    w, h = int(d["width"]), int(d["height"])
    return (h, w) if abs(int(float(d.get("rotation", 0)))) % 180 == 90 else (w, h)


def fond_glace():
    """le même fond que les cartes de verre : nuit bleue, un peu plus claire au centre"""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W * 0.5) / (W * 0.75)) ** 2 + ((y - H * 0.42) / (H * 0.9)) ** 2)
    k = np.clip(1 - r, 0, 1) ** 1.6
    c0, c1 = np.array([4, 5, 11], np.float32), np.array([22, 28, 48], np.float32)
    return (c0 + (c1 - c0) * k[..., None]).astype(np.float32)


FOND = None


def masque(im):
    """alpha 0-1 du produit (et de la main) par rembg"""
    a = np.asarray(remove(im, session=SESSION, only_mask=True)).astype(np.float32) / 255
    return a


def compose(rgb, a):
    a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
    a = np.clip((a - 0.08) / 0.84, 0, 1)[..., None]       # resserre un peu le bord (halo du fond)
    return (rgb.astype(np.float32) * a + FOND * (1 - a)).astype(np.uint8)


def traiter(nom, plages, test=None):
    global W, H, FOND
    src = P / "media" / "videos" / f"{nom}.mov"
    dst = P / "media" / "videos" / f"{nom}-d.mov"
    W, H = dims(src); FOND = fond_glace()
    print(f"{nom} : {W}×{H}", flush=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
    n = int(round(dur * FPS))
    actif = np.zeros(n, bool)
    for a, b in plages:
        actif[max(0, int(a * FPS)):min(n, int(b * FPS) + 1)] = True
    if test: dst = P / "media" / "videos" / f"{nom}-test.mov"
    lecteur = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)], stdin=subprocess.PIPE)
    noir = np.zeros((H, W, 3), np.uint8)
    pend = []              # [(rgb, alpha)] : l'image k s'écrit quand on connaît le masque de k+1 (lissage sur 3)
    t0 = time.time(); fait = 0

    def ecrire(i):
        voisins = [pend[j][1] for j in (i - 1, i, i + 1) if 0 <= j < len(pend)]
        enc.stdin.write(compose(pend[i][0], np.mean(voisins, axis=0)).tobytes())

    def vider():
        for i in range(len(pend)): ecrire(i) if i == len(pend) - 1 or i == 0 and len(pend) == 1 else None
        pend.clear()

    for k in range(n):
        raw = lecteur.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        if not actif[k]:
            if pend:
                if len(pend) >= 2: ecrire(len(pend) - 1)
                else: ecrire(0)
                pend.clear()
            enc.stdin.write(noir.tobytes()); continue
        rgb = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
        a = masque(Image.fromarray(rgb))
        pend.append((rgb, a))
        if len(pend) == 1: pass                      # on attend le voisin de droite
        else: ecrire(len(pend) - 2)                  # l'avant-dernière a ses deux voisins (ou un seul au début)
        if len(pend) > 3: pend.pop(0)
        fait += 1
        if fait % 30 == 0: print(f"{nom} {fait} images, {(time.time() - t0) / fait:.1f} s/image", flush=True)
    if pend: ecrire(len(pend) - 1) if len(pend) >= 2 else ecrire(0)
    enc.stdin.close(); enc.wait(); lecteur.wait()
    print(f"→ {dst.name} : {fait} images détourées en {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    if "--test" in sys.argv:
        i = sys.argv.index("--test"); nom, a, d = sys.argv[i + 1], float(sys.argv[i + 2]), float(sys.argv[i + 3])
        traiter(nom, [(a, a + d)], test=True)
    else:
        plages = json.load(open(sys.argv[1]))
        for nom, pl in plages.items(): traiter(nom, pl)
