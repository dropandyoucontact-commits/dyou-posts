#!/usr/bin/env python3
"""Suivi de l'écran du téléphone dans les rushes (mains gantées + téléphone dans les allées).

Le seuil seul ne suffit pas : les reflets éclaircissent l'écran et les gants sont presque aussi
sombres que lui. On suit donc la SILHOUETTE du téléphone sur le décor clair, au-dessus des mains :
  - bord haut et bords gauche/droit = transitions sombre → clair, ajustées par des droites ;
  - les coins du bas sont déduits du rapport hauteur/largeur de l'écran mesuré quand le téléphone
    est entièrement visible (prise à une main, début des rushes) ;
  - masque des doigts : pixels « gant » reliés aux mains hors de l'écran, pour que le contenu
    passe SOUS les pouces.
Sortie : suivi/<rush>.json (4 coins de l'ÉCRAN par image, pixels de la source, ordre HG HD BD BG)
et suivi/<rush>/NNNNN.png (masque : 255 = écran visible, 0 = doigt ou dehors).

    python3 suivi.py              → tous les rushes
    python3 suivi.py surron       → un seul
"""
import json, pathlib, sys
import cv2
import numpy as np

P = pathlib.Path(__file__).resolve().parent
SOMBRE = 34          # silhouette du téléphone (corps + écran) contre le décor
ECRAN = 12           # écran noir pur


def images(chemin):
    cap = cv2.VideoCapture(str(chemin))
    while True:
        ok, im = cap.read()
        if not ok: break
        yield im


def droite(ys, xs):
    """x = a·y + b, ajustement robuste (deux passes, rejet des écarts)"""
    ys, xs = np.asarray(ys, float), np.asarray(xs, float)
    a, b = np.polyfit(ys, xs, 1)
    for _ in range(2):
        r = np.abs(xs - (a * ys + b)); ok = r < max(1.5, 2.5 * np.median(r))
        if ok.sum() < 6: break
        a, b = np.polyfit(ys[ok], xs[ok], 1)
    return a, b


def silhouette(g, cx_prec):
    """bords haut / gauche / droit du téléphone ; renvoie (HG, HD, dir_g, dir_d, largeur) ou None"""
    h, w = g.shape
    d = g < SOMBRE
    # haut du téléphone : première ligne où une course sombre large passe par le centre attendu
    cx = int(cx_prec)
    haut = None
    for y in range(int(h * 0.15), int(h * 0.85)):
        if d[y, cx] and d[y, max(0, cx - 8):cx + 9].mean() > 0.9:
            haut = y; break
    if haut is None: return None
    gs, ds, ys = [], [], []
    l0 = None
    for y in range(haut + 4, min(h, haut + 260)):
        ligne = d[y]
        if not ligne[cx]:
            # le centre peut tomber sur un reflet : chercher le pixel sombre le plus proche
            v = np.where(ligne[max(0, cx - 30):cx + 30])[0]
            if len(v) == 0: break
            c0 = max(0, cx - 30) + v[np.argmin(np.abs(v - 30))]
        else:
            c0 = cx
        # course sombre « tolérante » : on traverse les reflets (pixels clairs isolés < 6 px)
        l = c0
        while l > 0 and (ligne[l - 1] or ligne[max(0, l - 9):l - 1].any()): l -= 1
        r = c0
        while r < w - 1 and (ligne[r + 1] or ligne[r + 2:min(w, r + 10)].any()): r += 1
        larg = r - l
        if l0 is None: l0 = []
        if len(l0) >= 8 and larg > 1.18 * np.median(l0): break        # les gants commencent
        l0.append(larg); gs.append(l); ds.append(r); ys.append(y)
    if len(ys) < 25: return None
    ag, bg = droite(ys, gs); ad, bd = droite(ys, ds)
    # bord haut : sur les 60 % centraux, première ligne sombre de chaque colonne
    xa, xb = ag * haut + bg, ad * haut + bd
    cols = np.linspace(xa + 0.2 * (xb - xa), xb - 0.2 * (xb - xa), 24).astype(int)
    tops = []
    for x in cols:
        col = d[max(0, haut - 25):haut + 25, x]
        k = np.argmax(col) if col.any() else 25
        tops.append(max(0, haut - 25) + k)
    a_h, b_h = droite(cols, tops)     # y = a_h·x + b_h
    def inter(a, b):                   # bord latéral x = a·y + b ∩ bord haut y = a_h·x + b_h
        y = (a_h * b + b_h) / (1 - a_h * a); return np.array([a * y + b, y])
    # contrôle : bords latéraux presque verticaux et presque parallèles
    if abs(ag) > 0.35 or abs(ad) > 0.35 or abs(ag - ad) > 0.22: return None
    HG, HD = inter(ag, bg), inter(ad, bd)
    if not (40 < HD[0] - HG[0] < 160): return None
    dg = np.array([ag, 1.0]); dg /= np.linalg.norm(dg)
    dd = np.array([ad, 1.0]); dd /= np.linalg.norm(dd)
    return HG, HD, dg, dd, ys[-1]


def lisse(Q, r=3):
    Q = np.array(Q, float); out = Q.copy()
    for i in range(len(Q)):
        a, b = max(0, i - r), min(len(Q), i + r + 1)
        wts = np.exp(-0.5 * ((np.arange(a, b) - i) / (r / 1.5)) ** 2)
        med = np.median(Q[a:b], axis=0)
        out[i] = 0.5 * med + 0.5 * (Q[a:b] * wts[:, None, None]).sum(0) / wts.sum()
    return out


def masque_doigts(g, q):
    """255 = écran visible ; les doigts (gant relié aux mains hors de l'écran) sont exclus"""
    h, w = g.shape
    dedans = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(dedans, np.round(q).astype(np.int32), 1)
    # luminance de l'écran lui-même (zone haute et centrale, rarement couverte par un doigt)
    qq = np.asarray(q)
    hg, hd, bd_, bg_ = qq
    zone = [hg + (hd - hg) * fx + (bg_ - hg) * fy for fx in np.linspace(0.3, 0.7, 6) for fy in np.linspace(0.1, 0.45, 8)]
    vals = [g[int(min(h - 1, max(0, y))), int(min(w - 1, max(0, x)))] for x, y in zone]
    ref = float(np.median([v for v in vals if v < 110] or [10]))
    gant = ((g >= max(28, ref + 16)) & (g < 110)).astype(np.uint8)
    # mains : composantes « gant » qui touchent le bas de l'image
    n, lab = cv2.connectedComponents(gant, 8)
    bas = np.unique(lab[-3:, :]); bas = bas[bas > 0]
    mains = np.isin(lab, bas)
    # on ne garde, dans l'écran, que les parties de mains qui touchent le bord inférieur ou latéral
    # du quadrilatère depuis l'extérieur (un reflet du haut de l'écran n'est pas relié)
    doigts = mains & (dedans > 0)
    doigts = cv2.morphologyEx(doigts.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    m = (dedans > 0) & ~(doigts > 0)
    return (m * 255).astype(np.uint8)


def suivre(nom):
    src = P / "media" / "rushes" / f"{nom}.mp4"
    dossier = P / "suivi" / nom; dossier.mkdir(parents=True, exist_ok=True)
    gr = [cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) for im in images(src)]
    h, w = gr[0].shape
    # centre de départ : le plus grand bloc d'écran noir de la première image
    m0 = (gr[0] < ECRAN).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(m0, 8)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); cx = cen[k][0]
    brut, rapports = [], []
    for i, g in enumerate(gr):
        s = silhouette(cv2.GaussianBlur(g, (3, 3), 0), cx)
        brut.append(s)
        if s: cx = 0.5 * (s[0][0] + s[1][0])
        # rapport hauteur/largeur mesuré sur les images où tout l'écran est visible
        if s and i < 40:
            mm = (g < ECRAN).astype(np.uint8)
            n, lab, st, _ = cv2.connectedComponentsWithStats(mm, 8)
            kk = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            hh, ww = st[kk, cv2.CC_STAT_HEIGHT], st[kk, cv2.CC_STAT_WIDTH]
            if 1.7 < hh / ww < 2.6: rapports.append((hh + 6) / (ww + 6))
    A = 2.16    # écran d'iPhone (19,5:9) ; la mesure sur le bloc sombre sous-estimait (doigts sur les bords)
    Q = [None] * len(brut)
    for i, s in enumerate(brut):
        if s is None: continue
        HG, HD, dg, dd, _ = s
        L = A * np.linalg.norm(HD - HG)
        Q[i] = np.array([HG, HD, HD + dd * L, HG + dg * L])
    # images ratées : interpolation linéaire entre les voisines valables
    ok = [i for i, q in enumerate(Q) if q is not None]
    for i in range(len(Q)):
        if Q[i] is not None: continue
        a = max([j for j in ok if j < i], default=None); b = min([j for j in ok if j > i], default=None)
        if a is None: Q[i] = Q[b]
        elif b is None: Q[i] = Q[a]
        else: Q[i] = Q[a] + (Q[b] - Q[a]) * (i - a) / (b - a)
    Q = lisse(Q)
    # l'écran est en retrait du corps : 3 % de chaque côté
    E = []
    for q in Q:
        c = q.mean(0); E.append(c + (q - c) * 0.95)
    for i, (g, q) in enumerate(zip(gr, E)):
        cv2.imwrite(str(dossier / f"{i + 1:05d}.png"), masque_doigts(g, q))
    fps = cv2.VideoCapture(str(src)).get(cv2.CAP_PROP_FPS)
    (P / "suivi" / f"{nom}.json").write_text(json.dumps(dict(fps=fps, w=w, h=h, rapport=A, coins=np.round(E, 2).tolist())))
    print(nom, len(Q), "images, rapport", round(A, 3), "ratées", sum(s is None for s in brut))


if __name__ == "__main__":
    noms = sys.argv[1:] or sorted(p.stem for p in (P / "media" / "rushes").glob("*.mp4"))
    for n in noms: suivre(n)
