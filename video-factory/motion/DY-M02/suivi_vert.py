#!/usr/bin/env python3
"""Rushes à écran VERT (v2, 08/10/2026) : détourage du vert + suivi des 4 coins de l'écran.

Pour chaque image du rush (400×736, 24 i/s) :
  - clé verte k = G − max(R, B) ; alpha doux = (k − 18) / 42 borné : 1 sur l'écran, 0 sur les doigts,
    la pastille noire (Dynamic Island) et le décor → le contenu passe SOUS les doigts au pixel près ;
  - quadrilatère : contour du bloc vert (trous bouchés), chaque côté ajusté par une droite robuste qui
    ignore les creux des doigts et les coins arrondis ; coins = intersections (coins « vifs » virtuels) ;
  - images 1080×1920 (agrandies ×2,7, recadrées de 33,6 px en haut et en bas), vert retiré des bords
    (despill), et version floutée pour le verre dépoli des panneaux.
Sortie : suivi/<rush>.json (coins en pixels de SORTIE 1080×1920), suivi/<rush>/NNNNN.png (alpha, taille
source), renders/cache-rush/<rush>/NNNNN.jpg et renders/cache-rush/<rush>/flou/NNNNN.jpg.

    python3 suivi_vert.py            → tous les rushes de media/vert/
    python3 suivi_vert.py baskets    → un seul
"""
import json, pathlib, sys
import cv2
import numpy as np

P = pathlib.Path(__file__).resolve().parent
S = 2.7
OY = (736 * S - 1920) / 2


def cle(im):
    b, g, r = [im[..., i].astype(np.int16) for i in range(3)]
    return g - np.maximum(r, b)


def droite_robuste(pts, normale_ext):
    """ajuste une droite n·p = d aux points ; les points en retrait (doigts) sont écartés.
    normale_ext : vecteur unitaire vers l'extérieur de l'écran"""
    pts = np.asarray(pts, float)
    n = np.asarray(normale_ext, float)
    for _ in range(4):
        c = pts.mean(0)
        u, s, vt = np.linalg.svd(pts - c)
        nn = vt[1] if np.dot(vt[1], n) > 0 else -vt[1]
        d = np.dot(c, nn)
        res = pts @ nn - d                       # > 0 : vers l'extérieur ; < 0 : creux (doigt)
        garde = res > -1.2
        if garde.sum() < 10 or garde.all(): break
        pts = pts[garde]
    return nn, d


def inter(l1, l2):
    (n1, d1), (n2, d2) = l1, l2
    return np.linalg.solve(np.array([n1, n2]), np.array([d1, d2]))


def quad(k):
    m = (k > 40).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n < 2: return None
    j = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    if st[j, cv2.CC_STAT_AREA] < 2000: return None
    comp = (lab == j).astype(np.uint8)
    cs, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cs, key=cv2.contourArea)[:, 0, :].astype(float)
    (cx, cy), (w, h), ang = cv2.minAreaRect(cnt.astype(np.float32))
    box = cv2.boxPoints(((cx, cy), (w, h), ang))
    # ordonner HG HD BD BG
    s_, d_ = box.sum(1), box[:, 0] - box[:, 1]
    box = np.array([box[np.argmin(s_)], box[np.argmax(d_)], box[np.argmax(s_)], box[np.argmin(d_)]])
    centre = box.mean(0)
    cotes = []
    for a in range(4):
        p0, p1 = box[a], box[(a + 1) % 4]
        L = np.linalg.norm(p1 - p0); t = (p1 - p0) / L
        nrm = np.array([t[1], -t[0]])
        if np.dot((p0 + p1) / 2 - centre, nrm) < 0: nrm = -nrm
        # points du contour proches de ce côté, hors coins arrondis (14 % à chaque bout)
        rel = cnt - p0
        le_long = rel @ t; dist = np.abs(rel @ nrm)
        sel = (le_long > 0.14 * L) & (le_long < 0.86 * L) & (dist < 0.12 * min(w, h) + 3)
        if sel.sum() < 8: return None
        cotes.append(droite_robuste(cnt[sel], nrm))
    q = np.array([inter(cotes[3], cotes[0]), inter(cotes[0], cotes[1]), inter(cotes[1], cotes[2]), inter(cotes[2], cotes[3])])
    return q


def lisse(Q):
    """lissage léger (le suivi est précis : un fort lissage ferait glisser le contenu)"""
    Q = np.array(Q, float); out = Q.copy()
    for i in range(1, len(Q) - 1):
        out[i] = 0.25 * Q[i - 1] + 0.5 * Q[i] + 0.25 * Q[i + 1]
    return out


def agrandit(im):
    g = cv2.resize(im, (1080, int(round(736 * S))), interpolation=cv2.INTER_LANCZOS4)
    y0 = int(round(OY))
    g = g[y0:y0 + 1920]
    flou = cv2.GaussianBlur(g, (0, 0), 3)
    return cv2.addWeighted(g, 1.5, flou, -0.5, 0)


def suivre(nom):
    src = P / "media" / "vert" / f"{nom}.mov"
    dm = P / "suivi" / nom; dm.mkdir(parents=True, exist_ok=True)
    dc = P / "renders" / "cache-rush" / nom; (dc / "flou").mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(src)); fps = cap.get(cv2.CAP_PROP_FPS)
    Q, ratees, i = [], 0, 0
    while True:
        ok, im = cap.read()
        if not ok: break
        k = cle(im)
        q = quad(k)
        if q is None: ratees += 1
        Q.append(q)
        alpha = np.clip((k.astype(float) - 18) / 42, 0, 1)
        cv2.imwrite(str(dm / f"{i + 1:05d}.png"), (alpha * 255).astype(np.uint8))
        # despill : le liseré vert des doigts et du cadre redevient neutre
        b_, g_, r_ = [im[..., c].astype(np.int16) for c in range(3)]
        zone = cv2.dilate((k > 10).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        g2 = np.where(zone, np.minimum(g_, np.maximum(r_, b_) + 6), g_)
        im2 = np.stack([b_, g2, r_], -1).clip(0, 255).astype(np.uint8)
        grand = agrandit(im2)
        cv2.imwrite(str(dc / f"{i + 1:05d}.jpg"), grand, [cv2.IMWRITE_JPEG_QUALITY, 95])
        petit = cv2.resize(grand, (270, 480), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(dc / "flou" / f"{i + 1:05d}.jpg"), cv2.resize(cv2.GaussianBlur(petit, (0, 0), 6), (1080, 1920), interpolation=cv2.INTER_CUBIC), [cv2.IMWRITE_JPEG_QUALITY, 90])
        i += 1
    ok_ = [j for j, q in enumerate(Q) if q is not None]
    for j in range(len(Q)):
        if Q[j] is None:
            a = max([x for x in ok_ if x < j], default=None); b = min([x for x in ok_ if x > j], default=None)
            Q[j] = Q[b] if a is None else Q[a] if b is None else Q[a] + (Q[b] - Q[a]) * (j - a) / (b - a)
    # bord bas caché par les pouces : on impose le format de l'écran (médiane du rush)
    Q = np.array(Q, float)
    larg = np.linalg.norm(Q[:, 1] - Q[:, 0], axis=1)
    cote = (np.linalg.norm(Q[:, 2] - Q[:, 1], axis=1) + np.linalg.norm(Q[:, 3] - Q[:, 0], axis=1)) / 2
    r = cote / larg; m = float(np.median(r))
    for j in np.where(np.abs(r - m) / m > 0.02)[0]:
        for haut, bas in ((1, 2), (0, 3)):
            v = Q[j, bas] - Q[j, haut]; v /= np.linalg.norm(v)
            Q[j, bas] = Q[j, haut] + v * m * larg[j]
    print(nom, "format", round(m, 3), "bords bas corrigés :", int((np.abs(r - m) / m > 0.02).sum()))
    Q = lisse(Q)
    Qs = Q * S; Qs[..., 1] -= OY
    (P / "suivi" / f"{nom}.json").write_text(json.dumps(dict(fps=fps, n=len(Q), echelle=S, oy=OY, coins=np.round(Qs, 2).tolist())))
    print(nom, len(Q), "images,", ratees, "ratées")


if __name__ == "__main__":
    noms = sys.argv[1:] or sorted(p.stem for p in (P / "media" / "vert").glob("*.mov"))
    for n in noms: suivre(n)
