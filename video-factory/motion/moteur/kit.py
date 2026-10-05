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
