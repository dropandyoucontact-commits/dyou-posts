#!/usr/bin/env python3
"""Rush tablette à écran VERT (DY-M21, 28/10/2026) — adapté de DY-M02/suivi_vert.py.
Source 720×1280 à 24 i/s → sortie 1080×1920 (×1,5, sans recadrage).
  suivi/<rush>.json : coins HG HD BD BG en pixels de sortie ; suivi/<rush>/NNNNN.png : alpha (taille source) ;
  renders/cache-rush/<rush>/NNNNN.jpg : image agrandie, vert retiré des bords ; flou/ : version floutée.
"""
import json, pathlib, sys
import cv2, numpy as np
P = pathlib.Path(__file__).resolve().parent
S, OY = 1.5, 0.0

def cle(im):
    b, g, r = [im[..., i].astype(np.int16) for i in range(3)]
    return g - np.maximum(r, b)

def droite_robuste(pts, normale_ext):
    pts = np.asarray(pts, float); n = np.asarray(normale_ext, float)
    for _ in range(4):
        c = pts.mean(0); u, s, vt = np.linalg.svd(pts - c)
        nn = vt[1] if np.dot(vt[1], n) > 0 else -vt[1]
        d = np.dot(c, nn); res = pts @ nn - d
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
    s_, d_ = box.sum(1), box[:, 0] - box[:, 1]
    box = np.array([box[np.argmin(s_)], box[np.argmax(d_)], box[np.argmax(s_)], box[np.argmin(d_)]])
    centre = box.mean(0); cotes = []
    for a in range(4):
        p0, p1 = box[a], box[(a + 1) % 4]
        L = np.linalg.norm(p1 - p0); t = (p1 - p0) / L
        nrm = np.array([t[1], -t[0]])
        if np.dot((p0 + p1) / 2 - centre, nrm) < 0: nrm = -nrm
        rel = cnt - p0; le_long = rel @ t; dist = np.abs(rel @ nrm)
        sel = (le_long > 0.14 * L) & (le_long < 0.86 * L) & (dist < 0.12 * min(w, h) + 3)
        if sel.sum() < 8: return None
        cotes.append(droite_robuste(cnt[sel], nrm))
    return np.array([inter(cotes[3], cotes[0]), inter(cotes[0], cotes[1]), inter(cotes[1], cotes[2]), inter(cotes[2], cotes[3])])

def lisse(Q):
    Q = np.array(Q, float); out = Q.copy()
    for i in range(1, len(Q) - 1): out[i] = 0.25 * Q[i - 1] + 0.5 * Q[i] + 0.25 * Q[i + 1]
    return out

def reconstruire(Q):
    """la tablette est rigide : le coin haut-droit et le bord haut ne sont jamais cachés ; la largeur, le vecteur du
    côté droit et l'écart gauche/droit (perspective) varient lentement → interpolés depuis les images propres."""
    Q = np.array(Q, float); n = len(Q)
    HG, HD, BD, BG = Q[:, 0], Q[:, 1], Q[:, 2], Q[:, 3]
    top = HD - HG; w = np.linalg.norm(top, axis=1); u = top / w[:, None]
    vr = BD - HD; vl = BG - HG; h = np.linalg.norm(vr, axis=1)
    dev = np.linalg.norm(vl - vr, axis=1) / w; bot = np.linalg.norm(BD - BG, axis=1) / w; ratio = h / w
    med = np.median(ratio[(dev < 0.025) & (np.abs(bot - 1) < 0.03)])
    clean = (dev < 0.025) & (np.abs(bot - 1) < 0.03) & (np.abs(ratio - med) < 0.015 * med)
    idx = np.arange(n); ci = idx[clean]
    I = lambda a: np.interp(idx, ci, a[clean])
    w_i = I(w); vr_i = np.stack([I(vr[:, 0]), I(vr[:, 1])], 1); d_i = np.stack([I((vl - vr)[:, 0]), I((vl - vr)[:, 1])], 1)
    HD2 = HD.copy(); u2 = u.copy()
    for i in range(1, n - 1):
        HD2[i] = 0.25 * HD[i - 1] + 0.5 * HD[i] + 0.25 * HD[i + 1]
        u2[i] = 0.25 * u[i - 1] + 0.5 * u[i] + 0.25 * u[i + 1]
    u2 /= np.linalg.norm(u2, axis=1)[:, None]
    HG2 = HD2 - u2 * w_i[:, None]; BD2 = HD2 + vr_i; BG2 = HG2 + vr_i + d_i
    print("reconstruction : images propres", int(clean.sum()), "/", n, "format", round(float(med), 3))
    return np.stack([HG2, HD2, BD2, BG2], 1)


def agrandit(im):
    g = cv2.resize(im, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    flou = cv2.GaussianBlur(g, (0, 0), 3)
    return cv2.addWeighted(g, 1.5, flou, -0.5, 0)

def suivre(nom):
    src = P / "media" / "vert" / f"{nom}.mp4"
    dm = P / "suivi" / nom; dm.mkdir(parents=True, exist_ok=True)
    dc = P / "renders" / "cache-rush" / nom; (dc / "flou").mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(src)); fps = cap.get(cv2.CAP_PROP_FPS)
    Q, ratees, i = [], 0, 0
    while True:
        ok, im = cap.read()
        if not ok: break
        k = cle(im); q = quad(k)
        if q is None: ratees += 1
        Q.append(q)
        alpha = np.clip((k.astype(float) - 30) / 26, 0, 1)
        cv2.imwrite(str(dm / f"{i + 1:05d}.png"), (alpha * 255).astype(np.uint8))
        b_, g_, r_ = [im[..., c].astype(np.int16) for c in range(3)]
        zone = cv2.dilate((k > 4).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        g2 = np.where(zone, np.minimum(g_, (r_ + b_) // 2 + 2), g_)
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
    Q = np.array(Q, float)
    larg = np.linalg.norm(Q[:, 1] - Q[:, 0], axis=1)
    cote = (np.linalg.norm(Q[:, 2] - Q[:, 1], axis=1) + np.linalg.norm(Q[:, 3] - Q[:, 0], axis=1)) / 2
    r = cote / larg; m = float(np.median(r))
    for j in np.where(np.abs(r - m) / m > 0.02)[0]:
        for haut, bas in ((1, 2), (0, 3)):
            v = Q[j, bas] - Q[j, haut]; v /= np.linalg.norm(v)
            Q[j, bas] = Q[j, haut] + v * m * larg[j]
    print(nom, "format h/l", round(m, 3), "bords bas corrigés :", int((np.abs(r - m) / m > 0.02).sum()))
    Q = reconstruire(Q)
    Qs = Q * S; Qs[..., 1] -= OY
    (P / "suivi" / f"{nom}.json").write_text(json.dumps(dict(fps=fps, n=len(Q), echelle=S, oy=OY, coins=np.round(Qs, 2).tolist())))
    print(nom, len(Q), "images,", ratees, "ratées, fps", fps)

if __name__ == "__main__":
    for n in (sys.argv[1:] or sorted(p.stem for p in (P / "media" / "vert").glob("*.mp4"))): suivre(n)
