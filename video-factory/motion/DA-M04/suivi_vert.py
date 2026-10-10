#!/usr/bin/env python3
"""Écran vert de r2 (720×1280, 24 i/s) : détourage + suivi des 4 coins, avec les fonctions de DY-M02/suivi_vert.py.
Sortie en coordonnées 1080×1920 (×1,5, pas de recadrage) : suivi/r2.json, suivi/r2/NNNNN.png (alpha, taille source),
renders/cache-rush/r2/NNNNN.jpg (image 1080×1920, vert neutralisé autour des doigts).
    python3 suivi_vert.py
"""
import importlib.util, json, pathlib
import cv2
import numpy as np

P = pathlib.Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("sv", P.parent / "DY-M02" / "suivi_vert.py")
sv = importlib.util.module_from_spec(_s); _s.loader.exec_module(sv)
S = 1.5


def suivre(nom="r2"):
    dm = P / "suivi" / nom; dm.mkdir(parents=True, exist_ok=True)
    dc = P / "renders" / "cache-rush" / nom; dc.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(P / "media" / "rushes" / f"{nom}.mp4")); fps = cap.get(cv2.CAP_PROP_FPS)
    Q, i = [], 0
    while True:
        ok, im = cap.read()
        if not ok: break
        k = sv.cle(im)
        Q.append(sv.quad(k))
        cv2.imwrite(str(dm / f"{i + 1:05d}.png"), (np.clip((k.astype(float) - 18) / 42, 0, 1) * 255).astype(np.uint8))
        b_, g_, r_ = [im[..., c].astype(np.int16) for c in range(3)]
        zone = cv2.dilate((k > 10).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        g2 = np.where(zone, np.minimum(g_, np.maximum(r_, b_) + 6), g_)
        im2 = np.stack([b_, g2, r_], -1).clip(0, 255).astype(np.uint8)
        cv2.imwrite(str(dc / f"{i + 1:05d}.jpg"), cv2.resize(im2, (1080, 1920), interpolation=cv2.INTER_LANCZOS4), [cv2.IMWRITE_JPEG_QUALITY, 94])
        i += 1
    ok_ = [j for j, q in enumerate(Q) if q is not None]
    for j in range(len(Q)):
        if Q[j] is None:
            a = max([x for x in ok_ if x < j], default=None); b = min([x for x in ok_ if x > j], default=None)
            Q[j] = Q[b] if a is None else Q[a] if b is None else Q[a] + (Q[b] - Q[a]) * (j - a) / (b - a)
    Q = sv.lisse(np.array(Q, float)) * S
    (P / "suivi" / f"{nom}.json").write_text(json.dumps(dict(fps=fps, n=len(Q), coins=np.round(Q, 2).tolist())))
    print(nom, len(Q), "images,", len(Q) - len(ok_), "ratées")


if __name__ == "__main__":
    suivre()
