"""Briques de scène au standard CB-M01, partagées par toutes les vidéos.

Fond à points, bandeau de marque, sous-titres karaoké, pastilles, texte centré,
téléphone, produit posé, éclairs de couleur, et les registres de sons et de
fenêtres rapides. Une vidéo importe ce module dans son scenes.py :

    from kit import *
    K = Kit(dossier_du_projet, duree=22.3)
    TW = K.TW ; son = K.son ; rapide = K.rapide ; eclair = K.eclair
"""
import json, math, pathlib
import skia
import moteur
from moteur import *


class Kit:
    def __init__(self, dossier, duree):
        self.P = pathlib.Path(dossier)
        moteur.PROJET = self.P
        self.timing = json.loads((self.P / "timing.json").read_text())
        self.mots = self.timing["mots"]
        self.duree = duree
        self.nb_images = round(duree * FPS)
        self.SFX, self.RAPIDE, self.ECLAIRS = [], [], []

    def TW(self, i):
        return self.mots[i]["t0"]

    def son(self, t, nom, gain=0.0):
        if 0 <= t < self.duree: self.SFX.append((round(t, 3), nom, gain))

    def rapide(self, t0, t1):
        self.RAPIDE.append((t0, t1))

    def flou_a(self, t):
        return 5 if any(a <= t <= b for a, b in self.RAPIDE) else 1

    def eclair(self, t, couleur, a=0.11):
        self.ECLAIRS.append((t, couleur, a))

    def dessine_eclairs(self, c, t):
        for t0, coul, a in self.ECLAIRS:
            if t0 - 0.02 <= t <= t0 + 0.5:
                u = (t - t0 + 0.02) / 0.52
                al = a * (1 - u) ** 2 if u > 0.08 else a * u / 0.08
                c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), peinture(coul, al))


# ─────────────────────────────────────────── fond et bandeau
def fond(c, t):
    c.clear(skia.ColorWHITE)
    p = peinture("#E6EBE8")
    dy = (t * 16) % 54
    for y in range(-54, H + 54, 54):
        for x in range(27, W, 54):
            c.drawCircle(x, y + 27 - dy, 2.3, p)


def bandeau(c, t, alpha):
    if alpha <= 0: return
    with Calque(c, alpha):
        image(c, "logo", 90, 152, 170)
        lab = "LE RÉSEAU EN DIRECT"
        w = largeur(lab, 20, "fort", 0.12)
        texte(c, lab, 990, 158, 20, C["gris"], "fort", "droite", 0.12)
        disque(c, 990 - w - 20, 170, 6, C["vert"], 0.35 + 0.65 * (0.5 + 0.5 * math.cos(t * 4)))


# ─────────────────────────────────────────── texte et pastilles
def _para_info(s, fam, taille, track):
    p = moteur._para(s, fam, float(taille), 0xFF000000, moteur._ls(taille, track))
    return p.AlphabeticBaseline, p.LongestLine


def texte_centre(c, s, cx, cy, taille, couleur=C["ink"], fam="noir", alpha=1.0, track=-0.025):
    """centre la chaîne sur (cx, cy) en calant la hauteur des capitales"""
    base, w = _para_info(s, fam, taille, track)
    texte(c, s, cx - w / 2, cy - base + 0.727 * taille / 2, taille, couleur, fam, "gauche", track, alpha)
    return w


def pastille(c, label, cx, cy, taille, fond_, texte_c, icone_=None, alpha=1.0, ombre=None, contour=None, ep=0, fam="noir", pad=None):
    tw = largeur(label, taille, fam)
    ic = taille * 1.15 if icone_ else 0
    gap = taille * 0.35 if icone_ else 0
    pad = pad if pad is not None else taille * 0.8
    h = taille * 2.05
    w = tw + ic + gap + 2 * pad
    rrect(c, cx - w / 2, cy - h / 2, w, h, h / 2, fond_, alpha, ombre, contour, ep)
    x = cx - w / 2 + pad
    if icone_:
        icone(c, icone_, x + ic / 2, cy, ic, texte_c, 2.6, alpha)
        x += ic + gap
    texte_centre(c, label, x + tw / 2, cy, taille, texte_c, fam, alpha)
    return w, h


def pastille_rot(c, label, cx, cy, taille, fond_, texte_c, rot, s, alpha, icone_=None, ombre=(12, 30, 0.18)):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    pastille(c, label, 0, 0, taille, fond_, texte_c, icone_, alpha, ombre)
    c.restore()


def tampon(c, label, cx, cy, t, t0, taille=56, couleur=C["rouge"], rot=-9, icone_=None):
    """tampon qui claque : arrive de très grand, contour épais"""
    if t < t0 - 0.12: return
    u = prog(t, t0 - 0.12, 0.16, entree)
    s = mix(2.6, 1, u)
    tw = largeur(label, taille)
    ic = taille * 1.0 if icone_ else 0
    w, h = tw + ic + (taille * 0.3 if icone_ else 0) + taille * 1.1, taille * 1.95
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, u):
        rrect(c, -w / 2, -h / 2, w, h, 22, C["blanc"], 0.94, None, couleur, 8)
        x = -w / 2 + taille * 0.55
        if icone_:
            icone(c, icone_, x + ic / 2, 0, ic, couleur, 2.8); x += ic + taille * 0.3
        texte_centre(c, label, x + tw / 2, 0, taille, couleur)
    c.restore()


def telephone(c, x, y, w=480, h=960, ecran=None, alpha=1.0):
    """téléphone : corps noir, écran découpé ; ecran(c, x, y, w, h) dessine le contenu"""
    with Calque(c, alpha):
        carte(c, x, y, w, h, 74 * w / 480, C["ink"], 1.0, (40, 90, 0.28))
        ex, ey, ew, eh = x + 14, y + 14, w - 28, h - 28
        c.save()
        c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(ex, ey, ew, eh), 60 * w / 480, 60 * w / 480), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(ex, ey, ew, eh), peinture(C["blanc"]))
        if ecran: ecran(c, ex, ey, ew, eh)
        c.restore()
        rrect(c, x + w / 2 - 62 * w / 480, y + 30 * w / 480, 124 * w / 480, 34 * w / 480, 17 * w / 480, C["ink"])


def produit(c, nom, cx, cy, w, alpha=1.0, ombre=True):
    iw, ih = taille_img(nom)
    h = w * ih / iw
    if ombre: ombre_sol(c, cx, cy + h / 2 - h * 0.02, w * 0.42, h * 0.06, 0.18 * alpha)
    image(c, nom, cx - w / 2, cy - h / 2, w, alpha)
    return h


def bulle(c, txt, droite, xs, y, w_ecran, t, t0, fond_, coul, taille=26, ombre=None):
    """bulle de conversation qui naît de son coin"""
    if t < t0 - 0.02: return 0
    lignes = txt.split("\n")
    tw = max(largeur(l, taille, "demi", 0) for l in lignes)
    bw, bh = tw + 44, len(lignes) * taille * 1.3 + 30
    x = xs + w_ecran - 26 - bw if droite else xs + 26
    u = prog(t, t0, 0.32, lambda v: rebond(v, 1.8))
    ax = x + (bw if droite else 0)
    c.save(); c.translate(ax, y + bh); c.scale(mix(0.3, 1, u), mix(0.3, 1, u)); c.translate(-ax, -(y + bh))
    with Calque(c, borne(u * 2)):
        rrect(c, x, y, bw, bh, 28, fond_, 1.0, ombre)
        for k, l in enumerate(lignes):
            texte(c, l, x + 22, y + 15 + k * taille * 1.3, taille, coul, "demi", track=0)
    c.restore()
    return bh


# ─────────────────────────────────────────── sous-titres karaoké
class SousTitres:
    """blocs : liste de listes de jetons (indice du mot | None, texte, style, temps imposé)
    style « g » vert, « r » rouge ; le mot prononcé passe sur fond coloré."""

    def __init__(self, kit, blocs, x=540, y=292, larg=920, taille=104):
        self.K, self.x, self.y, self.larg = kit, x, y, larg
        self.blocs = []
        for bloc in blocs:
            mots = []
            for j in bloc:
                i, s = j[0], j[1]
                st = j[2] if len(j) > 2 else ""
                tw = j[3] if len(j) > 3 else kit.TW(i)
                mots.append(dict(s=s, st=st, t=tw))
            tl = taille
            while True:
                esp = largeur(" ", tl) * 1.3
                lignes, cur, w = [], [], 0
                for m in mots:
                    m["w"] = largeur(m["s"], tl)
                    if cur and w + esp + m["w"] > larg:
                        lignes.append(cur); cur, w = [], 0
                    w = m["w"] if not cur else w + esp + m["w"]
                    cur.append(m)
                lignes.append(cur)
                if (len(lignes) <= 2 or (len(lignes) == 3 and tl <= 96)) or tl <= 70: break
                tl -= 4
            lh = tl * 1.08
            for n, ligne in enumerate(lignes):
                lw = sum(m["w"] for m in ligne) + esp * (len(ligne) - 1)
                xx = x - lw / 2
                for m in ligne:
                    m["x"], m["y"] = xx, y + n * lh
                    xx += m["w"] + esp
            self.blocs.append(dict(mots=mots, taille=tl, debut=min(m["t"] for m in mots) - 0.12))
        for k, b in enumerate(self.blocs):
            b["fin"] = self.blocs[k + 1]["debut"] if k + 1 < len(self.blocs) else kit.duree + 1

    def textes(self):
        return [(max(0, b["debut"]), min(b["fin"], self.K.duree), " ".join(m["s"] for m in b["mots"])) for b in self.blocs]

    def dessine(self, c, t, encre=C["ink"]):
        for b in self.blocs:
            if not (b["debut"] - 0.01 <= t < b["fin"]): continue
            taille, mots = b["taille"], b["mots"]
            hl = hauteurLigne(taille)
            sortie_u = prog(t, b["fin"] - 0.16, 0.16, entree) if b["fin"] < self.K.duree else 0
            actifs = [k for k, m in enumerate(mots) if m["t"] - 0.05 <= t]
            ka = actifs[-1] if actifs else None
            if b is self.blocs[-1] and ka is not None and any(m["st"] == "g" for m in mots):
                ka = min(ka, next(k for k, m in enumerate(mots) if m["st"] == "g"))
            u_hl, k_prec, u_prec = 1.0, None, 1.0
            if ka is not None and sortie_u < 1:
                m = mots[ka]
                u = prog(t, m["t"] - 0.05, 0.12, sortie)
                prev = mots[ka - 1] if ka > 0 else None
                coul = C["rouge"] if m["st"] == "r" else C["vert"]
                pad, r = taille * 0.1, taille * 0.18
                if prev is not None and abs(prev["y"] - m["y"]) < 1:
                    bx = mix(prev["x"], m["x"], u); bw = mix(prev["w"], m["w"], u)
                    u_hl, k_prec, u_prec = u, ka - 1, u
                    rrect(c, bx - pad, m["y"] + hl * 0.06 - sortie_u * 40, bw + 2 * pad, hl * 0.9, r, coul, 1 - sortie_u)
                else:
                    s_b = mix(0.7, 1, u); u_hl = u
                    cxb, cyb = m["x"] + m["w"] / 2, m["y"] + hl * 0.51
                    bw, bh = (m["w"] + 2 * pad) * s_b, hl * 0.9 * s_b
                    rrect(c, cxb - bw / 2, cyb - bh / 2 - sortie_u * 40, bw, bh, r, coul, u * (1 - sortie_u))
            for k, m in enumerate(mots):
                ta = m["t"] - 0.06
                if t < ta: continue
                u = borne((t - ta) / 0.34)
                s = 0.62 + 0.38 * rebond(u, 2.2) if u < 1 else 1.0
                a = borne((t - ta) / 0.07) * (1 - sortie_u)
                dy = 30 * (1 - sortie(u)) - 44 * sortie_u
                base_c = C["vert"] if m["st"] == "g" else C["rouge"] if m["st"] == "r" else encre
                c.save(); c.translate(m["x"] + m["w"] / 2, m["y"] + hl / 2 + dy); c.scale(s, s)
                x0, y0 = -m["w"] / 2, -hl / 2
                if k == ka and u_hl >= 0.999:
                    texte(c, m["s"], x0, y0, taille, C["blanc"], alpha=a)
                elif k == ka:
                    texte(c, m["s"], x0, y0, taille, base_c, alpha=a * (1 - u_hl))
                    texte(c, m["s"], x0, y0, taille, C["blanc"], alpha=a * u_hl)
                elif k == k_prec and u_prec < 0.999:
                    texte(c, m["s"], x0, y0, taille, C["blanc"], alpha=a * (1 - u_prec))
                    texte(c, m["s"], x0, y0, taille, base_c, alpha=a * u_prec)
                else:
                    texte(c, m["s"], x0, y0, taille, base_c, alpha=a)
                c.restore()


# ─────────────────────────────────────────── logos d'applications (Simple Icons, CC0)
MARQUES = {"wechat": "#07C160", "alipay": "#1677FF"}
_LOGO_DATA = []


def _logo_dom(nom, couleur):
    import functools
    cle = (nom, couleur)
    if cle not in _logo_dom.cache:
        src = (moteur.BANQUE / "logos" / f"{nom}.svg").read_text().replace("<path ", f'<path fill="{couleur}" ')
        data = skia.Data.MakeWithCopy(src.encode()); _LOGO_DATA.append(data)
        dom = skia.SVGDOM.MakeFromStream(skia.MemoryStream(data)); dom.setContainerSize(skia.Size(24, 24))
        _logo_dom.cache[cle] = dom
    return _logo_dom.cache[cle]
_logo_dom.cache = {}


def logo_glyphe(c, nom, cx, cy, taille, couleur=None, alpha=1.0):
    dom = _logo_dom(nom, couleur or MARQUES.get(nom, C["ink"]))
    c.save()
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(cx - taille, cy - taille, 2 * taille, 2 * taille), int(255 * borne(alpha)))
    c.translate(cx - taille / 2, cy - taille / 2); c.scale(taille / 24, taille / 24); dom.render(c)
    if alpha < 1: c.restore()
    c.restore()


def logo_app(c, nom, cx, cy, taille, alpha=1.0, ombre=(10, 26, 0.18)):
    """icône d'application : carré arrondi à la couleur de la marque, glyphe blanc"""
    rrect(c, cx - taille / 2, cy - taille / 2, taille, taille, taille * 0.24, MARQUES[nom], alpha, ombre)
    logo_glyphe(c, nom, cx, cy, taille * 0.62, C["blanc"], alpha)


# ─────────────────────────────────────────── écran WeChat
WX = dict(fond="#EDEDED", barre="#EDEDED", trait="#D5D5D5", vert="#95EC69", texte="#111111", gris="#8C8C8C", saisie="#F7F7F7")


def _wx_entete(c, x, y, w, titre):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 150), peinture(WX["barre"]))
    texte(c, "9:41", x + 42, y + 22, 24, WX["texte"], "fort", track=0)
    icone(c, "signal", x + w - 110, y + 38, 26, WX["texte"], 2.4); icone(c, "battery-full", x + w - 66, y + 38, 30, WX["texte"], 2.2)
    icone(c, "chevron-left", x + 40, y + 108, 40, WX["texte"], 2.6)
    texte_centre(c, titre, x + w / 2, y + 108, 30, WX["texte"], "demi", track=0)
    icone(c, "ellipsis", x + w - 46, y + 108, 38, WX["texte"], 2.6)
    trait(c, x, y + 150, x + w, y + 150, WX["trait"], 2, rond=False)


def _wx_saisie(c, x, y, w, h):
    yb = y + h - 112
    c.drawRect(skia.Rect.MakeXYWH(x, yb, w, 112), peinture(WX["saisie"]))
    trait(c, x, yb, x + w, yb, WX["trait"], 2, rond=False)
    anneau(c, x + 46, yb + 50, 22, WX["texte"], 2.4); icone(c, "mic", x + 46, yb + 50, 24, WX["texte"], 2.2)
    rrect(c, x + 84, yb + 22, w - 220, 58, 10, C["blanc"])
    icone(c, "smile", x + w - 104, yb + 50, 44, WX["texte"], 2.0); icone(c, "circle-plus", x + w - 48, yb + 50, 44, WX["texte"], 2.0)


def qr_code(c, x, y, taille, graine=7, couleur="#111111"):
    """motif de QR code (décoratif, non lisible) : 25 × 25 modules, trois repères d'angle"""
    import numpy as np
    n = 25; m = taille / n
    rng = np.random.default_rng(graine); g = rng.random((n, n)) < 0.48
    p = peinture(couleur)
    for i in range(n):
        for j in range(n):
            coin = (i < 8 and j < 8) or (i < 8 and j >= n - 8) or (i >= n - 8 and j < 8)
            if g[i, j] and not coin: c.drawRect(skia.Rect.MakeXYWH(x + j * m, y + i * m, m + 0.4, m + 0.4), p)
    for (ci, cj) in ((0, 0), (0, n - 7), (n - 7, 0)):
        rrect(c, x + cj * m, y + ci * m, 7 * m, 7 * m, m * 1.4, couleur)
        rrect(c, x + (cj + 1) * m, y + (ci + 1) * m, 5 * m, 5 * m, m, C["blanc"])
        rrect(c, x + (cj + 2) * m, y + (ci + 2) * m, 3 * m, 3 * m, m * 0.6, couleur)


def _wx_bulle(c, m, xb, yb, wb, hb, moi):
    coul = WX["vert"] if moi else C["blanc"]
    rrect(c, xb, yb, wb, hb, 12, coul)
    pq = skia.Path()
    if moi:
        pq.moveTo(xb + wb - 1, yb + 26); pq.lineTo(xb + wb + 12, yb + 36); pq.lineTo(xb + wb - 1, yb + 46)
    else:
        pq.moveTo(xb + 1, yb + 26); pq.lineTo(xb - 12, yb + 36); pq.lineTo(xb + 1, yb + 46)
    pq.close(); c.drawPath(pq, peinture(coul))


def _wx_mesure(m, wmax):
    """taille (w, h) du contenu d'un message"""
    if m["type"] == "texte":
        lignes = m["texte"].split("\n")
        return max(largeur(l, 30, "moyen", 0) for l in lignes) + 44, len(lignes) * 40 + 32
    if m["type"] == "image": return 300, 300
    if m["type"] == "video": return 250, 420
    if m["type"] == "qr": return min(wmax, 310), 420
    if m["type"] == "carte": return min(wmax, 380), 150
    return 200, 80


def ecran_wechat(c, x, y, w, h, t, titre, messages):
    """conversation WeChat. messages : dicts {t, moi, type (texte|image|video|qr|carte), …}.
    Les messages apparaissent à leur temps et la conversation défile quand elle déborde."""
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(WX["fond"]))
    haut, bas = y + 170, y + h - 130
    ya, poses_ = haut, []
    for m in messages:
        mw, mh = _wx_mesure(m, w - 24 - 72 - 20 - 36)
        poses_.append((ya, mw, mh)); ya += mh + 34
    # défilement : le dernier message apparu doit rester visible
    vus = [k for k, m in enumerate(messages) if t >= m["t"] - 0.05]
    def bas_de(k): return poses_[k][0] + poses_[k][2]
    dec = 0.0
    for k in vus:
        cible = max(0.0, bas_de(k) - bas)
        dec = mix(dec, cible, prog(t, messages[k]["t"] - 0.05, 0.3, sortie))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y + 151, w, h - 151 - 112))
    for k in vus:
        m = messages[k]; yy, mw, mh = poses_[k]; yy -= dec
        u = prog(t, m["t"] - 0.05, 0.3, lambda v: rebond(v, 1.6))
        moi = m.get("moi", False)
        ax = x + w - 24 - 72 if moi else x + 24
        xb = ax - 20 - mw if moi else ax + 72 + 20
        c.save(); pivot_x = xb + (mw if moi else 0); c.translate(pivot_x, yy); c.scale(mix(0.5, 1, u), mix(0.5, 1, u)); c.translate(-pivot_x, -yy)
        with Calque(c, borne(u * 2)):
            rrect(c, ax, yy, 72, 72, 10, "#3E4A44" if not moi else "#CFE8D9")
            icone(c, "store" if not moi else "user", ax + 36, yy + 36, 40, C["blanc"] if not moi else "#2E7D52", 2.2)
            if m["type"] == "texte":
                _wx_bulle(c, m, xb, yy, mw, mh, moi)
                for n, l in enumerate(m["texte"].split("\n")):
                    texte(c, l, xb + 22, yy + 16 + n * 40, 30, WX["texte"], "moyen", track=0)
            elif m["type"] == "image":
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xb, yy, mw, mh), 12, 12), doAntiAlias=True)
                c.drawRect(skia.Rect.MakeXYWH(xb, yy, mw, mh), peinture(C["blanc"]))
                iw, ih = taille_img(m["image"]); s = min((mw - 30) / iw, (mh - 30) / ih)
                image(c, m["image"], xb + (mw - iw * s) / 2, yy + (mh - ih * s) / 2, iw * s)
                c.restore()
            elif m["type"] == "video":
                video(c, m["video"], xb, yy, mw, mh, t - m["t"], m.get("vitesse", 1.0), rayon=12)
                disque(c, xb + 34, yy + mh - 34, 18, "#000000", 0.35); icone(c, "play", xb + 35, yy + mh - 34, 18, C["blanc"], 2.6)
            elif m["type"] == "qr":
                rrect(c, xb, yy, mw, mh, 12, C["blanc"])
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xb, yy, mw, mh), 12, 12), doAntiAlias=True)
                c.drawRect(skia.Rect.MakeXYWH(xb, yy, mw, 84), peinture(MARQUES["alipay"]))
                c.restore()
                logo_glyphe(c, "alipay", xb + 44, yy + 42, 40, C["blanc"])
                texte(c, "Alipay", xb + 78, yy + 24, 32, C["blanc"], "noir", track=0)
                q = mw - 90
                qr_code(c, xb + 45, yy + 104, q, m.get("graine", 7))
                texte_centre(c, m.get("legende", "Scanne pour payer"), xb + mw / 2, yy + 104 + q + 30, 22, WX["gris"], "fort", track=0)
            elif m["type"] == "carte":
                rrect(c, xb, yy, mw, mh, 12, C["blanc"])
                texte(c, m["titre"], xb + 24, yy + 28, 28, WX["texte"], "fort", track=0)
                texte(c, m.get("sous", ""), xb + 24, yy + 74, 24, WX["gris"], "demi", track=0)
        c.restore()
    c.restore()
    _wx_entete(c, x, y, w, titre)
    _wx_saisie(c, x, y, w, h)


# ─────────────────────────────────────────── écran Alipay
def ecran_alipay(c, x, y, w, h, t, t_scan, t_paye, marchand="Fournisseur"):
    """paiement Alipay : QR scanné (ligne qui balaie), puis « Paiement réussi ». Montant masqué."""
    bleu = MARQUES["alipay"]
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#F5F7FA"))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 330), peinture(bleu))
    texte(c, "9:41", x + 42, y + 22, 24, C["blanc"], "fort", track=0)
    logo_glyphe(c, "alipay", x + w / 2 - 78, y + 150, 64, C["blanc"])
    texte(c, "Alipay", x + w / 2 - 34, y + 122, 52, C["blanc"], "noir")
    texte_centre(c, "Payer le marchand", x + w / 2, y + 236, 26, "#D6E6FF", "fort", track=0)
    cx, cy = x + w / 2, y + 330 + 240
    carte(c, x + 30, y + 290, w - 60, h - 420, 28, C["blanc"], 1.0, (10, 30, 0.12))
    ok = prog(t, t_paye, 0.35, lambda v: rebond(v, 1.7))
    if ok < 1:
        with Calque(c, 1 - ok):
            texte_centre(c, marchand, cx, y + 350, 30, C["ink"], "noir")
            texte_centre(c, "¥ • • • •", cx, y + 410, 40, C["ink"], "noir")
            qr_code(c, cx - 150, y + 460, 300, 11)
            if t >= t_scan:
                yy = y + 460 + 300 * ((t - t_scan) * 1.6 % 1.0)
                trait(c, cx - 170, yy, cx + 170, yy, bleu, 6, 0.9)
            rrect(c, x + 70, y + 800, w - 140, 84, 42, bleu)
            texte_centre(c, "Payer", cx, y + 842, 32, C["blanc"])
    if ok > 0:
        c.save(); c.translate(cx, y + 560); c.scale(mix(0.3, 1, ok), mix(0.3, 1, ok))
        with Calque(c, borne(ok * 2)):
            disque(c, 0, 0, 110, bleu)
            icone(c, "check", 0, 0, 120, C["blanc"], 3.2)
        c.restore()
        texte_centre(c, "Paiement réussi", cx, y + 740, 40, C["ink"], "noir", borne(ok * 2))
        texte_centre(c, "Le fournisseur expédie chez ton transitaire", cx, y + 800, 24, C["gris"], "fort", borne(ok * 2))
