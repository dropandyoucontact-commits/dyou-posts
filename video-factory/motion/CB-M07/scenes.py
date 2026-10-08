"""CB-M07 « Les 3 arnaques en Chine » — vidéo ORGANIQUE (42 s), remix d'un TikTok d'arnaques.

Demande de Youssef (08/10/2026) : hook agressif, remix façon ChinaBook. Discours ChinaBook : jamais « usine »,
pas de « paie seulement un compte d'entreprise » (on paie le fournisseur sur Alipay) → arnaque 2 = paiement
sans trace (Western Union, crypto), arnaque 3 = refus de l'appel vidéo pour montrer la marchandise.
Organique : « enregistre » à 3 s, boucle ouverte sur le n° 3, question en commentaire, ChinaBook en fin,
signature « proposé par DROP&YOU » sur le carton final.

Voix : moteur/outils/voix.py (Tomy, 3,8 mots/s). Chaque élément cite le mot qu'il illustre.
"""
import math, pathlib, re, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *

DUREE = 42.0
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a
ROUGE = C["rouge"]

MARQUES.update({"westernunion": "#FFDD00", "bitcoin": "#F7931A"})

# ─────────────────────────────────────────── sous-titres (construits depuis le minutage)
AFFICHE = {28: "1 :", 55: "2 :", 87: "3 :", 140: "ChinaBook."}
CACHES = {141}
VERTS = {13, 14, 16, 30, 32, 35, 36, 47, 62, 63, 65, 72, 93, 94, 98, 100, 112, 118, 123, 130, 131, 133, 136, 140, 146, 150}
ROUGES = {4, 6, 23, 49, 54, 80, 86, 89, 91, 107, 109}
COUPES = {7, 14, 21, 28, 33, 43, 48, 55, 66, 73, 77, 81, 87, 92, 103, 110, 119, 126, 137, 142, 147}


def _blocs():
    blocs, cour = [], []
    for m in K.mots:
        i = m["i"]
        if i in CACHES: continue
        mot = AFFICHE.get(i, m["w"]).replace("'", "’")
        prec = cour[-1][1] if cour else ""
        if cour and (i in COUPES or len(cour) >= 6 or re.search(r"[.?]$", prec) or (re.search(r"[,:]$", prec) and len(cour) >= 3)):
            blocs.append(cour); cour = []
        cour.append((i, mot, "g" if i in VERTS else ("r" if i in ROUGES else "")))
    blocs.append(cour)
    net = []
    for bl in blocs:
        if net and len(bl) == 1 and bl[0][0] not in COUPES and len(net[-1]) <= 6: net[-1] = net[-1] + bl
        else: net.append(bl)
    blocs = net
    blocs[0][0] = (0, "Tu", "", -0.45)
    return blocs


SOUS = SousTitres(K, _blocs())

# ─────────────────────────────────────────── fenêtres de scène
def fen(i0, i1, a=0.14, b=0.02):
    return (TW(i0) - a if i0 else 0.0, TW(i1) - b)


H = fen(0, 28)
S1, S2, S3 = fen(28, 55), fen(55, 87), fen(87, 110)
SC4, SC1, SC2 = fen(110, 119), fen(119, 126), fen(126, 140)
T_LOGO = TW(140) - 0.12
SC3 = (TW(142) - 0.1, 39.95)
T_FIN = 39.85
NUMS = [(S1, 1), (S2, 2), (S3, 3)]
NB = 3


class _Sc:
    def __init__(self, c, tr):
        self.c, self.tr = c, tr
    def __enter__(self):
        dx, dy, s, al = self.tr
        if al < 0.999: self.c.saveLayerAlpha(None, int(255 * borne(al)))
        else: self.c.save()
        self.c.translate(540 + dx, 1080 + dy); self.c.scale(s, s); self.c.translate(-540, -1080)
        return self.c
    def __exit__(self, *a):
        self.c.restore()


def scene(c, t, S, ek="gauche", sk="gauche", de=0.28, ds=0.22):
    a, b = S
    if not (a <= t <= b): return None
    ue = prog(t, a, de, sortie) if ek else 1.0
    us = prog(t, b - ds, ds, entree) if sk else 0.0
    dx = dy = 0.0; s = 1.0; al = 1.0
    if ek == "gauche": dx += 1300 * (1 - ue)
    elif ek == "droite": dx -= 1300 * (1 - ue)
    elif ek == "bas": dy += 1500 * (1 - ue)
    elif ek == "zoom": s *= mix(0.55, 1, ue); al *= ue
    if sk == "gauche": dx -= 1300 * us
    elif sk == "droite": dx += 1300 * us
    elif sk == "haut": dy -= 1500 * us
    elif sk == "zoom": s *= mix(1, 1.9, us); al *= (1 - us)
    return _Sc(c, (dx, dy, s, al))


def tel(c, cx, cy, ecran, w=480, h=960, alpha=1.0, **espace):
    with Espace(c, cx, cy, **espace):
        telephone(c, cx - w / 2, cy - h / 2, w, h, ecran, alpha)


def apparait(t, t0, s=1.9, d=0.34):
    return prog(t, t0, d, lambda v: rebond(v, s))


# ─────────────────────────────────────────── petits éléments
def tuile(c, nom, cx, cy, taille, u=1.0, label=None, couleur=None, rot=0.0):
    """icône d'appli : glyphe Simple Icons (nom) ou mot (label) sur carré arrondi à la couleur de la marque"""
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
    with Calque(c, borne(u * 2)):
        if label:
            rrect(c, -taille / 2, -taille / 2, taille, taille, taille * 0.24, couleur, 1.0, (10, 26, 0.18))
            tl = ajuste(label, taille * 0.84, taille * 0.3)
            texte_centre(c, label, 0, 0, tl, C["blanc"], "noir", 1.0, -0.02)
        else:
            logo_app(c, nom, 0, 0, taille)
    c.restore()


def croix(c, cx, cy, r, u):
    """barre rouge qui raye un élément : cercle et diagonale"""
    if u <= 0: return
    anneau(c, cx, cy, r, ROUGE, r * 0.14, borne(u * 3))
    d = r * 0.7 * borne(u * 1.4)
    trait(c, cx - r * 0.7, cy - r * 0.7, cx - r * 0.7 + 2 * d, cy - r * 0.7 + 2 * d, ROUGE, r * 0.14)


def coche(c, cx, cy, r, u, couleur=None):
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.scale(u, u)
    disque(c, 0, 0, r, couleur or C["vert"], 1.0, (8, 20, 0.2)); icone(c, "check", 0, 0, r * 1.1, C["blanc"], 3.6)
    c.restore()


def gros_numero(c, t):
    """au début de chaque conseil, le numéro claque au centre puis file vers le compteur"""
    for (a, b), n in NUMS:
        if a <= t <= a + 0.75:
            u = apparait(t, a + 0.02, 2.2, 0.26); so = prog(t, a + 0.5, 0.25, entree)
            x, y = mix(540, 150, so), mix(1080, 640, so)
            s_ = mix(0.3, 1, u) * mix(1, 0.32, so)
            c.save(); c.translate(x, y); c.rotate(mix(-4, -6, so)); c.scale(s_, s_)
            rrect(c, -230, -230, 460, 460, 90, C["vert"], borne(u * 2), (20, 50, 0.3))
            texte_centre(c, f"{n}", 0, -6, 300, C["blanc"], "noir", borne(u * 2))
            c.restore()
            return


def numero(c, t):
    """compteur des 10 réflexes : gros numéro + 10 points de progression"""
    for (a, b), n in NUMS:
        if a + 0.7 <= t <= b:
            u = apparait(t, a + 0.7, 2.0, 0.2)
            c.save(); c.translate(150, 640); c.rotate(-6); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
            rrect(c, -78, -64, 156, 128, 30, C["ink"], borne(u * 2), (12, 30, 0.25))
            texte_centre(c, f"{n}", 0, 0, 82, C["blanc"], "noir", borne(u * 2))
            c.restore()
            for k in range(NB):
                x = 310 + k * 90
                fait = k < n - 1 or (k == n - 1 and u > 0.5)
                disque(c, x, 640, 15 if k == n - 1 else 11, C["vert"] if fait else "#DDE3E0")
            return


def billet_yuan(c, cx, cy, w, rot, alpha=1.0):
    h = w * 0.48
    c.save(); c.translate(cx, cy); c.rotate(rot)
    rrect(c, -w / 2, -h / 2, w, h, 14, "#E86A6A", alpha, (8, 20, 0.15))
    rrect(c, -w / 2 + 14, -h / 2 + 14, w - 28, h - 28, 10, "#F28B82", alpha)
    texte_centre(c, "¥", -w * 0.22, 0, h * 0.5, "#7A1E1E", "noir", alpha)
    disque(c, w * 0.22, 0, h * 0.28, "#C94A4A", alpha)
    c.restore()


def batterie(c, cx, cy, w, ccc, alpha=1.0, rot=0.0):
    h = w * 0.58
    c.save(); c.translate(cx, cy); c.rotate(rot)
    rrect(c, -w / 2, -h / 2, w, h, 26, "#F4F4F2", alpha, (14, 34, 0.18), "#D9DBD8", 4)
    for k in range(4):
        rrect(c, -w / 2 + 28 + k * 40, -h / 2 + 26, 28, 12, 6, C["vert"] if k < 3 else "#D9DBD8", alpha)
    rrect(c, w / 2 - 70, -14, 44, 28, 8, "#C9CCC8", alpha)
    if ccc:
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=hexa(C["ink"], alpha))
        c.drawOval(skia.Rect.MakeXYWH(-w * 0.25, -h * 0.05, w * 0.5, h * 0.42), p)
        texte_centre(c, "CCC", 0, h * 0.16, h * 0.22, C["ink"], "noir", alpha, 0.02)
    else:
        rrect(c, -w * 0.25, -h * 0.02, w * 0.5, h * 0.34, 12, "#E3E5E2", alpha)
        texte_centre(c, "EU", 0, h * 0.15, h * 0.16, "#9AA09B", "noir", alpha)
    c.restore()


def bulle_txt(c, txt, cx, cy, taille, fond_, coul, u, droite=False):
    if u <= 0: return
    w = largeur(txt, taille, "noir", 0) + taille * 1.4; h = taille * 2.1
    c.save(); c.translate(cx, cy); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
    with Calque(c, borne(u * 2)):
        rrect(c, -w / 2, -h / 2, w, h, h * 0.4, fond_, 1.0, (10, 26, 0.16))
        pq = skia.Path(); sx = w / 2 - 40 if droite else -w / 2 + 40
        pq.moveTo(sx - 14, h / 2 - 2); pq.lineTo(sx + 14, h / 2 - 2); pq.lineTo(sx + (22 if droite else -22), h / 2 + 22); pq.close()
        c.drawPath(pq, peinture(fond_))
        texte_centre(c, txt, 0, 0, taille, coul, "noir", 1.0, 0)
    c.restore()


def signet(c, cx, cy, taille, rempli, alpha=1.0):
    """icône « enregistrer » des réseaux : ruban marque-page"""
    w, h = taille * 0.62, taille * 0.8
    pq = skia.Path()
    pq.moveTo(cx - w / 2, cy - h / 2); pq.lineTo(cx + w / 2, cy - h / 2); pq.lineTo(cx + w / 2, cy + h / 2)
    pq.lineTo(cx, cy + h / 2 - w * 0.42); pq.lineTo(cx - w / 2, cy + h / 2); pq.close()
    if rempli: c.drawPath(pq, peinture("#FACE15", alpha))
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=taille * 0.08, StrokeJoin=skia.Paint.kRound_Join,
                   Color=hexa(C["ink"] if rempli else C["blanc"], alpha))
    c.drawPath(pq, p)


# ─────────────────────────────────────────── H · tu vas te faire arnaquer en Chine
def bulle_wx(c, txt, cx, cy, taille, u, moi=False, rot=0.0):
    """bulle façon WeChat (blanche du fournisseur, verte pour toi)"""
    if u <= 0: return
    w = largeur(txt, taille, "demi", 0) + taille * 1.6; h = taille * 2.2
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
    with Calque(c, borne(u * 2)):
        rrect(c, -w / 2, -h / 2, w, h, 18, "#95EC69" if moi else C["blanc"], 1.0, (12, 30, 0.18))
        if not moi:
            disque(c, -w / 2 - 70, 0, 46, "#E6EBE8"); icone(c, "user", -w / 2 - 70, 0, 50, C["gris"], 2.4)
        texte_centre(c, txt, 0, 0, taille, C["ink"], "demi", 1.0, 0)
    c.restore()


def h(c, t):
    sc = scene(c, t, H, None, "gauche")
    if sc is None: return
    with sc:
        so = prog(t, TW(7) - 0.2, 0.25, entreeSortie)
        # image 0 : la conversation piège, le tampon ARNAQUE claque
        if so < 1:
            with Calque(c, 1 - so):
                sx, sy = secousse(t, TW(4), 16, 0.35)
                for k in range(4):
                    v = (t * 0.7 + k * 0.25) % 1.0
                    billet_yuan(c, 540 + (-1) ** k * (200 + 220 * v), 1650 - 1100 * v, 200, k * 40 + 200 * v, borne(1 - v) * 0.6)
                bulle_wx(c, "Prix spécial pour toi", 600 + sx, 860 + sy, 52, 1.0, rot=-3)
                bulle_wx(c, "Paie d’abord, j’envoie demain", 560 + sx, 1090 + sy, 46, 1.0, rot=2)
                tampon(c, "ARNAQUE", 540, 1400, t, -0.04, 104, ROUGE, -9, "triangle-alert")
        # « ces trois pièges » : trois cartes masquées
        if so > 0:
            t3 = TW(7) - 0.05
            for k in range(3):
                uk = apparait(t, t3 + 0.07 * k, 1.8, 0.34)
                if uk <= 0: continue
                foc = prog(t, TW(23) - 0.1, 0.35, entreeSortie)
                x = 210 + k * 330; y = 1060
                if k == 2: x, y = mix(x, 540, foc), mix(y, 1180, foc)
                s_ = mix(0.3, 1, uk) * (mix(1, 1.45, foc) if k == 2 else mix(1, 0.75, foc))
                al = borne(uk * 2) * (1 if k == 2 else mix(1, 0.35, foc))
                c.save(); c.translate(x, y + 8 * math.sin(t * 3 + k)); c.rotate((k - 1) * 5); c.scale(s_, s_)
                carte(c, -140, -180, 280, 360, 44, C["blanc"], al, (18, 44, 0.2))
                rrect(c, -110, -150, 100, 86, 22, C["ink"], al); texte_centre(c, f"{k + 1}", -60, -107, 60, C["blanc"], "noir", al)
                disque(c, 0, 50, 76, ROUGE if k == 2 and foc > 0.5 else "#E6EBE8", al)
                texte_centre(c, "?", 0, 46, 96, C["blanc"] if k == 2 and foc > 0.5 else C["gris"], "noir", al)
                c.restore()
            if t >= TW(23) - 0.05:
                u = apparait(t, TW(23) - 0.05)
                pastille_rot(c, "PRESQUE PERSONNE", 540, 1620, 44, ROUGE, C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "triangle-alert", (14, 32, 0.25))
        # « Enregistre cette vidéo »
        us = apparait(t, TW(14) - 0.1, 1.8, 0.34) * (1 - prog(t, TW(21) - 0.1, 0.2, entree))
        if us > 0:
            rempli = t >= T_SAVE
            b = 1 + 0.25 * (1 - prog(t, T_SAVE, 0.25)) if rempli else 1
            c.save(); c.translate(540, 1480); c.scale(mix(0.3, 1, us) * b, mix(0.3, 1, us) * b)
            disque(c, 0, 0, 110, C["ink"], borne(us * 2), (14, 36, 0.3)); signet(c, 0, 0, 120, rempli, borne(us * 2))
            c.restore()
            if rempli: etincelles(c, 540, 1480, t, T_SAVE, 10, 200, "#FACE15")


T_SAVE = TW(14) + 0.2


# ─────────────────────────────────────────── S1 · le prix trop beau
def s1(c, t):
    sc = scene(c, t, S1, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_fuite = TW(48) - 0.1
        e = prog(t, t_fuite, 0.4, entreeSortie)
        if e < 1:
            with Calque(c, 1 - e):
                # étiquette de prix qui brille
                ue = apparait(t, TW(30) - 0.08, 1.7, 0.4) * (1 - prog(t, TW(34) - 0.2, 0.25, entree))
                if ue > 0:
                    c.save(); c.translate(540, 1120 + 10 * math.sin(t * 4)); c.rotate(-10); c.scale(mix(0.3, 1, ue), mix(0.3, 1, ue))
                    pq = skia.Path(); pq.moveTo(-260, -150); pq.lineTo(180, -150); pq.lineTo(300, 0); pq.lineTo(180, 150); pq.lineTo(-260, 150); pq.close()
                    c.drawPath(pq, peinture(C["vert"])); disque(c, 190, 0, 26, C["blanc"])
                    texte_centre(c, "PROMO", -50, 0, 92, C["blanc"], "noir", 1.0, 0.02)
                    c.restore()
                # comparaison des fournisseurs : barres sans nombres
                ub = prog(t, TW(34) - 0.15, 0.3, sortie)
                if ub > 0:
                    for k in range(4):
                        uk = apparait(t, TW(34) - 0.1 + 0.08 * k, 1.6, 0.34)
                        y = 860 + k * 190
                        louche = k == 3
                        c.save(); c.translate(0, 60 * (1 - uk))
                        with Calque(c, borne(uk * 2)):
                            disque(c, 150, y, 54, "#E6EBE8"); icone(c, "store", 150, y, 54, C["gris"], 2.4)
                            lmax = 640 if not louche else 320 * (1 if t > TW(37) else mix(2, 1, prog(t, TW(36), 0.4)))
                            rrect(c, 230, y - 32, lmax * borne(uk), 64, 32, ROUGE if louche and t > TW(36) else C["vert"])
                        c.restore()
                    if t >= TW(37) - 0.05:
                        u = apparait(t, TW(37) - 0.05)
                        pastille_rot(c, "2× MOINS CHER", 780, 1430, 44, ROUGE, C["blanc"], 5, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))
                    tampon(c, "TROP BEAU", 560, 1700, t, TW(47) - 0.05, 60, ROUGE, -6, "triangle-alert")
        if e > 0:
            # il encaisse, et il disparaît
            ui = apparait(t, t_fuite, 1.6, 0.4)
            dis = prog(t, TW(54) - 0.1, 0.5, entreeSortie)
            c.save(); c.translate(540, 1080); c.scale(mix(0.4, 1, ui), mix(0.4, 1, ui))
            with Calque(c, mix(1, 0.6, dis)):
                carte(c, -380, -150, 760, 300, 50, C["blanc"], 1.0, (20, 46, 0.18))
                disque(c, -250, 0, 80, "#E6EBE8"); icone(c, "user", -250, 0, 84, C["gris"], 2.4)
                texte(c, "Fournisseur" if dis < 0.5 else "Contact introuvable", -140, -44, 48 if dis < 0.5 else 40, C["ink"] if dis < 0.5 else ROUGE, "noir", track=0)
                rrect(c, -140, 26, 300, 26, 13, "#E6EBE8")
            c.restore()
            for k in range(5):
                v = prog(t, TW(49) - 0.05 + 0.06 * k, 0.6, entree)
                if 0 < v < 1:
                    billet_yuan(c, mix(540 + (k - 2) * 120, 300, v), mix(1700, 1080, v), 200 * (1 - 0.6 * v), -20 + 10 * k, 1 - v)
            if dis > 0.5:
                tampon(c, "DISPARU", 560, 1420, t, TW(54) + 0.15, 64, ROUGE, -6, "circle-x")


# ─────────────────────────────────────────── S2 · Western Union, crypto, sans trace
def s2(c, t):
    sc = scene(c, t, S2, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_perdu = TW(73) - 0.1
        e = prog(t, t_perdu, 0.4, entreeSortie)
        if e < 1:
            with Calque(c, 1 - e):
                up0 = apparait(t, S2[0] + 0.45, 1.7, 0.35) * (1 - prog(t, TW(62) - 0.15, 0.2, entree))
                if up0 > 0:
                    c.save(); c.translate(540, 1150); c.scale(mix(0.3, 1, up0), mix(0.3, 1, up0))
                    disque(c, 0, 0, 220, C["ink"], borne(up0 * 2), (18, 46, 0.3)); icone(c, "banknote", 0, 0, 220, C["blanc"], 2.4, borne(up0 * 2))
                    c.restore()
                uw = apparait(t, TW(62) - 0.08, 1.8, 0.36)
                if uw > 0:
                    c.save(); c.translate(300, 1000); c.rotate(-6); c.scale(mix(0.3, 1, uw), mix(0.3, 1, uw))
                    rrect(c, -130, -130, 260, 260, 60, MARQUES["westernunion"], 1.0, (12, 30, 0.2))
                    logo_glyphe(c, "westernunion", 0, 0, 160, C["ink"])
                    c.restore()
                tuile(c, "bitcoin", 780, 1000, 260, apparait(t, TW(65) - 0.08, 1.8, 0.36), rot=6)
                ut = apparait(t, TW(69) - 0.08, 1.7, 0.4)
                if ut > 0:
                    c.save(); c.translate(540, 1420); c.scale(mix(0.3, 1, ut), mix(0.3, 1, ut))
                    rrect(c, -300, -90, 600, 180, 50, C["ink"], borne(ut * 2), (14, 32, 0.25))
                    icone(c, "eye-off", -200, 0, 80, C["blanc"], 2.6, borne(ut * 2)); texte_centre(c, "SANS TRACE", 50, 0, 54, C["blanc"], "noir", borne(ut * 2))
                    c.restore()
        if e > 0:
            # l'argent s'envole
            for k in range(7):
                v = (prog(t, t_perdu + 0.1 * k, 1.4, lin))
                if 0 < v < 1:
                    billet_yuan(c, 540 + math.sin(k * 1.7) * 420 * v, 1300 - 900 * v, 300 * (1 - 0.5 * v), k * 33 + 260 * v, 1 - v)
            up = apparait(t, t_perdu + 0.05, 1.7, 0.4)
            if up > 0:
                c.save(); c.translate(540, 1150); c.scale(mix(0.3, 1, up), mix(0.3, 1, up))
                disque(c, 0, 0, 200, "#E6EBE8", borne(up * 2)); icone(c, "wallet", 0, 0, 200, C["gris"], 2.4, borne(up * 2))
                c.restore()
            tampon(c, "PERDU", 560, 1450, t, TW(80) - 0.05, 80, ROUGE, -7, "x-circle")
            if t >= TW(82) - 0.1:
                u = apparait(t, TW(82) - 0.1)
                pastille_rot(c, "AUCUN RECOURS", 760, 1700, 42, C["ink"], C["blanc"], 4, mix(0.3, 1, u), borne(u * 2), "lock", (14, 32, 0.25))


# ─────────────────────────────────────────── S3 · il refuse l'appel vidéo
def ecran_appel(cc, a, b, d, e, t):
    refus = t >= TW(89) - 0.05
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#1B1D1C"))
    texte(cc, "9:41", a + 40, b + 24, 24, C["blanc"], "fort", track=0)
    disque(cc, a + d / 2, b + 320, 110, "#3A3D3B"); icone(cc, "user", a + d / 2, b + 320, 120, "#9AA09B", 2.4)
    texte_centre(cc, "Fournisseur", a + d / 2, b + 490, 40, C["blanc"], "noir", 1.0, 0)
    texte_centre(cc, "Appel refusé" if refus else "Appel vidéo…", a + d / 2, b + 545, 28, "#FF6B6B" if refus else "#9AA09B", "fort", 1.0, 0)
    pulse = 1 + 0.08 * math.sin(t * 10) if not refus else 1
    disque(cc, a + d * 0.28, b + e - 160, 62 * pulse, ROUGE); icone(cc, "phone", a + d * 0.28, b + e - 160, 60, C["blanc"], 2.6)
    disque(cc, a + d * 0.72, b + e - 160, 62, C["vert"] if not refus else "#3A3D3B"); icone(cc, "video-off" if refus else "camera", a + d * 0.72, b + e - 160, 56, C["blanc"], 2.6)


def ecran_direct(cc, a, b, d, e, t):
    video(cc, "videos/chaussures/baskets-stock-1", a, b, d, e, t - TW(92) + 0.3, 2.2)
    rrect(cc, a + 30, b + 70, 190, 56, 28, ROUGE)
    disque(cc, a + 62, b + 98, 10, C["blanc"], 0.5 + 0.5 * math.sin(t * 8)); texte(cc, "EN DIRECT", a + 82, b + 82, 26, C["blanc"], "noir", track=0)


def s3(c, t):
    sc = scene(c, t, S3, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_vrai = TW(92) - 0.1
        t_exc = TW(103) - 0.1
        sx, sy = secousse(t, TW(89) - 0.05, 12, 0.3)
        if t < t_exc + 0.3:
            ecr = ecran_appel if t < t_vrai else ecran_direct
            with Calque(c, 1 - prog(t, t_exc, 0.3)):
                tel(c, 540 + sx, 1150 + sy, lambda cc, a, b, d, e: ecr(cc, a, b, d, e, t), ry=-6 + 3 * math.sin(t * 2.2))
            if t < t_vrai:
                tampon(c, "REFUSÉ", 790, 800, t, TW(89) + 0.05, 56, ROUGE, 8, "video-off")
            else:
                if t >= TW(98) - 0.1:
                    u = apparait(t, TW(98) - 0.1)
                    pastille_rot(c, "TA MARCHANDISE", 290, 780, 40, C["vert"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "package", (14, 32, 0.25))
                coche(c, 820, 1580, 70, apparait(t, TW(101) - 0.05, 2.0, 0.3))
        if t >= t_exc:
            for k, (txt, x, y, rot) in enumerate((("Pas dispo aujourd’hui", 540, 900, -3), ("Demain, promis", 600, 1100, 2), ("Le réseau ne marche pas", 520, 1300, -2))):
                bulle_wx(c, txt, x, y, 40, apparait(t, t_exc + 0.12 + 0.2 * k, 1.7, 0.34), rot=rot)
            tampon(c, "TU FUIS", 560, 1600, t, TW(109) - 0.05, 80, ROUGE, -7, "x-circle")


# ─────────────────────────────────────────── SC4 · dis-moi en commentaire si tu t'es déjà fait avoir
def sc4(c, t):
    sc = scene(c, t, SC4, "droite", "gauche", de=0.25)
    if sc is None: return
    with sc:
        u = prog(t, SC4[0], 0.25, sortie)
        y0 = mix(1050, 880, u)
        carte(c, 60, y0, 960, 760, 54, C["blanc"], 1.0, (26, 60, 0.2))
        icone(c, "message-circle", 140, y0 + 80, 52, C["ink"], 2.4)
        texte(c, "Commentaires", 190, y0 + 56, 38, C["ink"], "noir", track=0)
        for k in range(3):
            yy = y0 + 170 + k * 140
            disque(c, 140, yy + 30, 40, "#E6EBE8"); rrect(c, 200, yy + 4, 260 - 40 * k, 20, 10, "#E6EBE8"); rrect(c, 200, yy + 40, 520 - 60 * k, 20, 10, "#EEF1EF")
        actif = t >= TW(112)
        rrect(c, 100, y0 + 610, 880, 100, 50, "#F2F4F3", 1.0, None, C["vert"] if actif else "#E1E5E3", 4)
        texte(c, "Ajoute un commentaire…", 150, y0 + 634, 38, C["grisClair"], "moyen", track=0)
        if actif and int(t * 4) % 2 == 0: rrect(c, 148, y0 + 632, 5, 50, 2, C["ink"])
        if t >= TW(112) - 0.1:
            ub = apparait(t, TW(112) - 0.1)
            pastille_rot(c, "EN COMMENTAIRE", 300, 760, 42, C["vert"], C["blanc"], -6, mix(0.3, 1, ub), borne(ub * 2), "message-circle", (14, 32, 0.25))


# ─────────────────────────────────────────── SC1 · et si tu veux éviter tout ça
def sc1(c, t):
    sc = scene(c, t, SC1, "zoom", "gauche", de=0.25)
    if sc is None: return
    with sc:
        u = apparait(t, SC1[0] + 0.05, 1.7, 0.4)
        c.save(); c.translate(540, 1120); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
        disque(c, 0, 0, 230, C["vert"], borne(u * 2), (18, 46, 0.3)); icone(c, "shield-check", 0, 0, 240, C["blanc"], 2.4, borne(u * 2))
        c.restore()
        for k, ic in enumerate(("receipt", "eye-off", "video-off")):
            uk = apparait(t, TW(123) - 0.1 + 0.08 * k, 1.8, 0.3)
            if uk <= 0: continue
            x = 220 + k * 320
            c.save(); c.translate(x, 1520); c.scale(uk, uk)
            disque(c, 0, 0, 70, "#E6EBE8"); icone(c, ic, 0, 0, 70, C["gris"], 2.4)
            c.restore()
            croix(c, x, 1520, 80, prog(t, TW(124) + 0.08 * k, 0.25))


def sc2(c, t):
    sc = scene(c, t, SC2, "gauche", None, de=0.3)
    if sc is None: return
    with sc:
        e = prog(t, SC2[0] + 0.05, 0.45, sortie)
        lignes = [dict(t=TW(130) - 0.05, image="photos/chaussures/etagere-baskets-running-6-modeles", nom="Baskets", ville="Guangzhou"),
                  dict(t=TW(133) - 0.05, image="produits/electronique/casque-audio", nom="Électronique", ville="Shenzhen"),
                  dict(t=TW(136) - 0.05, image="produits/textile/veste-racing-noire", nom="Textile", ville="Guangzhou")]
        tel(c, 540, 1150, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-30, -4, e) + 2 * math.sin(t * 2.2), s=mix(0.6, 1, e), alpha=borne(e * 2))
        tampon(c, "VALIDÉS PAR MOI", 760, 760, t, TW(131) - 0.05, 50, C["vert"], -8, "badge-check")


def disque_logo(c, t):
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (SC3[0] - 0.05, 1750), (SC3[0] + 0.35, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, C["ink"])
        if T_LOGO + 0.2 <= t <= SC3[0] + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, SC3[0] - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * so)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2, lw, borne(u * 3) * (1 - so))
    return r


# ─────────────────────────────────────────── SC3 · tu leur écris sur WeChat, tu paies sur Alipay
MSGS = [dict(t=TW(144) - 0.05, moi=True, type="texte", texte="Je veux 2 paires de B30"),
        dict(t=TW(146), moi=False, type="qr")]


def sc3(c, t):
    sc = scene(c, t, SC3, None, None)
    if sc is None: return
    with sc:
        e = prog(t, SC3[0] + 0.2, 0.4, sortie)
        t_pay = TW(148) - 0.1
        if t < t_pay:
            tel(c, 540, mix(2200, 1160, e), lambda cc, a, b, d, e_: ecran_wechat(cc, a, b, d, e_, t, "Fournisseur Baskets", MSGS), ry=-6 + 2 * math.sin(t * 2))
            tuile(c, "wechat", 200, 800, 150, apparait(t, TW(146) - 0.1), rot=-8)
        else:
            tel(c, 540, 1160, lambda cc, a, b, d, e_: ecran_alipay(cc, a, b, d, e_, t, t_pay + 0.1, TW(150) + 0.15, "Fournisseur"), ry=-6 + 2 * math.sin(t * 2))
            tuile(c, "alipay", 880, 800, 150, apparait(t, TW(150) - 0.1), rot=8)
        texte_centre(c, "Échange illustratif", 540, 1665, 22, C["grisClair"], "fort", 1.0, 0.04)


def carton_final(c, t):
    """carton final ChinaBook avec la signature « proposé par DROP&YOU »"""
    if t < T_FIN: return
    u = prog(t, T_FIN, 0.4, sortie)
    disque(c, 540, 1060, 440 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
    ul = prog(t, T_FIN + 0.08, 0.36, lambda v: rebond(v, 1.6))
    lw = 760 * mix(0.6, 1, ul)
    iw_, ih_ = taille_img("logo"); lh = lw * ih_ / iw_
    image(c, "logo", 540 - lw / 2, 960 - lh / 2, lw, borne(ul * 2))
    ub = prog(t, T_FIN + 0.3, 0.36, lambda v: rebond(v, 1.8))
    if ub > 0:
        c.save(); c.translate(540, 1130); c.scale(mix(0.4, 1, ub), mix(0.4, 1, ub))
        with Calque(c, borne(ub * 2)):
            rrect(c, -250, -54, 500, 108, 54, C["ink"], 1.0, (16, 40, 0.25))
            signet(c, -170, 0, 56, True); texte_centre(c, "Enregistre-la", 40, 0, 40, C["blanc"], "noir")
        c.restore()
    etincelles(c, 540, 1130, t, T_FIN + 0.45, 12, 360)
    ud = prog(t, T_FIN + 0.55, 0.4, sortie)
    if ud > 0:
        texte_centre(c, "proposé par", 540, 1300, 26, C["gris"], "fort", ud, 0.04)
        image(c, "logo-dropandyou", 540 - 160, 1330, 320, ud)


# ─────────────────────────────────────────── sons, flou, éclairs
son(0.0, "impact", -5); son(0.0, "whoosh_court", -12); son(0.0, "tampon", -6); son(TW(4) - 0.02, "impact", -7)
for k in range(3): son(TW(12) - 0.08 + 0.07 * k, "pop", -11)
son(TW(7) - 0.15, "whoosh_court", -13); son(TW(14) - 0.1, "pop", -11); son(T_SAVE, "ching", -10)
son(TW(23) - 0.1, "whoosh", -14); son(TW(24) - 0.1, "pop", -11)
for (a, b), n in NUMS:
    son(a - 0.02, "whoosh", -13); son(a + 0.05, "pop", -10)
son(TW(30) - 0.08, "pop", -11); son(TW(32) - 0.05, "ching", -11)
for k in range(4): son(TW(34) - 0.1 + 0.08 * k, "blip", -15)
son(TW(36), "whoosh_court", -13); son(TW(37) - 0.05, "pop", -10); son(TW(47) - 0.17, "tampon", -7)
son(TW(48) - 0.1, "whoosh_court", -12)
for k in range(5): son(TW(49) - 0.05 + 0.06 * k, "swipe", -16)
son(TW(54) - 0.1, "whoosh_long", -14); son(TW(54) + 0.05, "tampon", -7); son(TW(54) + 0.07, "impact", -8)
son(TW(62) - 0.08, "pop", -10); son(TW(65) - 0.08, "pop", -10); son(TW(69) - 0.08, "pop", -11)
son(TW(73) - 0.1, "whoosh_long", -13); son(TW(80) - 0.17, "tampon", -6); son(TW(80) - 0.12, "impact", -7); son(TW(82) - 0.1, "pop", -11)
for k in range(6): son(S3[0] + 0.3 + 0.33 * k, "blip", -18)
son(TW(89) - 0.05, "impact_doux", -8); son(TW(89) - 0.07, "tampon", -8); son(TW(92) - 0.1, "whoosh_court", -12)
son(TW(98) - 0.1, "pop", -11); son(TW(101) - 0.05, "check", -10)
for k in range(3): son(TW(103) - 0.1 + 0.12 + 0.2 * k, "message_in", -12)
son(TW(109) - 0.17, "tampon", -6); son(TW(109) - 0.12, "impact", -7)
son(SC4[0], "whoosh", -13); son(TW(112) - 0.1, "pop", -11)
son(SC1[0] - 0.02, "whoosh", -13); son(SC1[0] + 0.05, "ching", -11)
for k in range(3): son(TW(124) + 0.08 * k, "impact_doux", -12)
son(SC2[0] - 0.02, "whoosh", -13); son(TW(131) - 0.17, "tampon", -8)
for i in (130, 133, 136): son(TW(i) - 0.05, "ching", -14)
son(T_LOGO - 0.1, "montee", -15); son(T_LOGO + 0.24, "impact", -7); son(T_LOGO + 0.26, "verre", -9); son(SC3[0], "whoosh_long", -14)
son(TW(144) - 0.05, "message", -11); son(TW(146), "message_in", -11); son(TW(146) - 0.1, "pop", -12); son(TW(148) - 0.1, "whoosh_court", -12); son(TW(150) + 0.15, "ching", -9)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.1, "impact_doux", -8); son(T_FIN + 0.12, "verre", -8); son(T_FIN + 0.3, "pop", -11); son(T_FIN + 0.55, "pop", -13)

for a, b in [(TW(7) - 0.15, TW(7) + 0.15), (TW(23) - 0.1, TW(23) + 0.25)] + [(a - 0.02, a + 0.3) for (a, b), n in NUMS] + \
            [(TW(48) - 0.1, TW(48) + 0.3), (TW(73) - 0.1, TW(73) + 0.3), (TW(92) - 0.1, TW(92) + 0.2), (TW(103) - 0.1, TW(103) + 0.2),
             (SC4[0], SC4[0] + 0.3), (SC1[0] - 0.02, SC1[0] + 0.3), (SC2[0] - 0.02, SC2[0] + 0.3), (T_LOGO, T_LOGO + 0.4), (SC3[0], SC3[0] + 0.4), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, C["rouge"], 0.2), (TW(4), C["rouge"], 0.12), (T_SAVE, "#FACE15", 0.12), (TW(47) - 0.05, C["rouge"], 0.12), (TW(54) + 0.1, C["rouge"], 0.12),
                    (TW(80) - 0.1, C["rouge"], 0.14), (TW(89), C["rouge"], 0.12), (TW(101), C["vert"], 0.08), (TW(109) - 0.1, C["rouge"], 0.14),
                    (SC1[0] + 0.05, C["vert"], 0.10), (T_LOGO + 0.24, C["blanc"], 0.15), (TW(150) + 0.15, C["vert"], 0.08), (T_FIN + 0.1, C["vert"], 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def alpha_bandeau(t, r):
    return borne(prog(t, 0.45, 0.3) * (1 - prog(t, T_FIN - 0.05, 0.25)) * (1 - borne(r / 400)))


def dessine(c, t):
    fond(c, t)
    for s in (h, s1, s2, s3, sc4, sc1, sc2, sc3):
        s(c, t)
    numero(c, t)
    gros_numero(c, t)
    r = disque_logo(c, t)
    bandeau(c, t, alpha_bandeau(t, r))
    carton_final(c, t)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if r > 900 else C["ink"])
