"""Suivi des repères (points accrochés aux objets) par flux optique, plan par plan.

Chaque repère : nom, début et fin du plan, instant de départ et point de départ (coordonnées 1920×1080).
On suit en avant et en arrière depuis le point de départ (médiane du déplacement des coins détectés
autour du point), puis on lisse. Sortie : suivi/<nom>.json = liste de [t, x, y] à 30 i/s.
    python3 suivi.py            → tous les repères
    python3 suivi.py controle   → apercus/controle_suivi.jpg
"""
import json, pathlib, subprocess, sys
import numpy as np, cv2

P = pathlib.Path(__file__).resolve().parent
SRC = P / "media" / "source.mov"
FPS = 30
REPERES = {
    "roue":     (4.17, 4.70, 4.30, (930, 440)),
    "usine":    (5.33, 6.60, 5.36, (1420, 718)),
    "essai":    (6.63, 7.95, 7.60, (1240, 800)),
    "montre1":  (8.70, 9.36, 9.00, (1233, 702)),
    "montre2":  (9.40, 10.55, 10.0, (1480, 886)),
    "basket":   (12.53, 13.66, 12.7, (1253, 864)),
    "veste":    (15.10, 16.70, 15.47, (1600, 660)),
    "casque":   (16.76, 18.79, 16.9, (1300, 600)),
}


def images(t0, t1, w=960):
    """images en niveaux de gris, demi-résolution"""
    h = w * 9 // 16
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", str(SRC), "-t", f"{t1 - t0:.3f}",
                          "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    n = len(raw) // (w * h)
    return np.frombuffer(raw[:n * w * h], np.uint8).reshape(n, h, w)


def suit(ims, k0, p0, rayon=60):
    """position du point dans chaque image, en partant de l'image k0"""
    pos = {k0: np.array(p0, float)}
    for sens in (1, -1):
        p = np.array(p0, float); k = k0
        while 0 <= k + sens < len(ims):
            a, b = ims[k], ims[k + sens]
            m = np.zeros_like(a); cv2.circle(m, (int(p[0]), int(p[1])), rayon, 255, -1)
            coins = cv2.goodFeaturesToTrack(a, 60, 0.01, 4, mask=m)
            if coins is not None and len(coins) >= 4:
                nv, st, _ = cv2.calcOpticalFlowPyrLK(a, b, coins, None, winSize=(31, 31), maxLevel=3)
                ok = st.ravel() == 1
                if ok.sum() >= 3:
                    d = np.median((nv - coins)[ok].reshape(-1, 2), axis=0)
                    p = p + d
            k += sens
            pos[k] = p.copy()
    return np.array([pos[k] for k in range(len(ims))])


def lisse(xy, f=5):
    if len(xy) < f: return xy
    noyau = np.ones(f) / f
    pad = np.pad(xy, ((f // 2, f // 2), (0, 0)), mode="edge")
    return np.stack([np.convolve(pad[:, j], noyau, mode="valid") for j in range(2)], 1)


def tout():
    (P / "suivi").mkdir(exist_ok=True)
    for nom, (a, b, ts, p0) in REPERES.items():
        ims = images(a, b)
        k0 = min(len(ims) - 1, round((ts - a) * FPS))
        xy = lisse(suit(ims, k0, (p0[0] / 2, p0[1] / 2)) * 2)
        json.dump([[round(a + k / FPS, 4), round(float(x), 1), round(float(y), 1)] for k, (x, y) in enumerate(xy)],
                  open(P / "suivi" / f"{nom}.json", "w"))
        print(nom, len(xy), "images", "écart max", np.abs(xy - xy[k0]).max(0).round())


def controle():
    from PIL import Image, ImageDraw
    vign = []
    for nom in REPERES:
        pts = json.load(open(P / "suivi" / f"{nom}.json"))
        for q in (0.05, 0.5, 0.95):
            t, x, y = pts[int(q * (len(pts) - 1))]
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t + 0.001:.3f}", "-i", str(SRC), "-frames:v", "1",
                                  "-vf", "scale=480:270", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            im = Image.frombytes("RGB", (480, 270), raw); d = ImageDraw.Draw(im)
            d.ellipse([x / 4 - 7, y / 4 - 7, x / 4 + 7, y / 4 + 7], outline=(255, 0, 255), width=3)
            d.text((5, 5), f"{nom} {t:.2f}", fill=(255, 255, 0))
            vign.append(im)
    pl = Image.new("RGB", (480 * 3, 270 * len(REPERES)))
    for k, im in enumerate(vign): pl.paste(im, ((k % 3) * 480, (k // 3) * 270))
    pl.save(P / "apercus" / "controle_suivi.jpg", quality=80)


if __name__ == "__main__":
    controle() if sys.argv[1:] == ["controle"] else tout()
