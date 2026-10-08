"""CB-M06 « 10 réflexes avant la Chine » — vidéo ORGANIQUE (62,6 s), remaster d'un TikTok voyage.

Demande de Youssef (08/10/2026) : remasteriser façon ChinaBook un TikTok « 10 choses à savoir avant d'aller
en Chine » (idées et faits seulement, rien de l'autrice). Organique : « enregistre » dans les 3 premières
secondes, boucle ouverte sur le n° 9, « envoie-la à celui qui part avec toi », question en commentaire,
passerelle ChinaBook à la fin. Sujet sans produit : motion pur (logos d'applis, écrans, icônes).

Faits vérifiés le 08/10/2026 : exemption de visa 30 jours pour les Français jusqu'au 31/12/2026 et carte
d'arrivée électronique depuis le 20/11/2025 ; batteries sans marquage CCC interdites sur les vols
intérieurs depuis le 28/06/2025 ; détaxe dès 200 ¥ dans le même magasin le même jour ; Alipay accepte
les cartes Visa / Mastercard étrangères.

Voix : moteur/outils/voix.py (Tomy, 3,8 mots/s). Chaque élément cite le mot qu'il illustre.
"""
import math, pathlib, re, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *

DUREE = 62.6
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a
ROUGE = C["rouge"]

MARQUES.update({"tripdotcom": "#287DFA", "uber": "#000000", "googlemaps": "#4285F4", "instagram": "#E4405F",
                "bookingdotcom": "#003580", "googletranslate": "#4285F4", "tiktok": "#000000"})

# ─────────────────────────────────────────── sous-titres (construits depuis le minutage)
AFFICHE = {32: "1 :", 53: "2 :", 65: "3 :", 83: "4 :", 95: "5 :", 100: "6 :", 113: "7 :", 121: "8 :", 140: "9 :", 160: "10 :",
           42: "2026.", 120: "Ele.me.", 148: "CCC,", 213: "ChinaBook."}
CACHES = {147, 214}
VERTS = {4, 6, 9, 10, 18, 36, 38, 39, 41, 42, 47, 49, 55, 57, 63, 64, 76, 77, 87, 94, 99, 105, 112, 120, 123, 126, 136, 148,
         164, 171, 172, 173, 187, 190, 205, 207, 209, 213, 219, 223, 226}
ROUGES = {3, 19, 23, 29, 31, 72, 97, 103, 133, 152, 156, 196}
COUPES = {32, 43, 53, 65, 73, 83, 88, 95, 100, 106, 113, 121, 127, 134, 140, 144, 157, 160, 169, 173, 180, 191, 197, 203, 210, 215, 220, 224}


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
    # un mot seul se rattache au bloc d'avant, s'il ne commence pas un numéro
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


H = fen(0, 32)
S1, S2, S3, S4, S5 = fen(32, 53), fen(53, 65), fen(65, 83), fen(83, 95), fen(95, 100)
S6, S7, S8, S9, S10 = fen(100, 113), fen(113, 121), fen(121, 140), fen(140, 160), fen(160, 173)
SP, SC1, SC2 = fen(173, 180), fen(180, 203), fen(203, 213)
T_LOGO = TW(213) - 0.12
SC3 = (TW(215) - 0.1, TW(224) - 0.02)
SC4 = (TW(224) - 0.14, 61.15)
T_FIN = 61.0
NUMS = [(S1, 1), (S2, 2), (S3, 3), (S4, 4), (S5, 5), (S6, 6), (S7, 7), (S8, 8), (S9, 9), (S10, 10)]


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
            for k in range(10):
                x = 300 + k * 64
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


# ─────────────────────────────────────────── H · le hook : ton téléphone ne te sert plus à rien
APPS_H = ["instagram", "whatsapp", "googlemaps", "uber", "tiktok", "bookingdotcom"]
T_SAVE = TW(4) + 0.15


def ecran_apps(cc, a, b, d, e, t):
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#1D2B3A"))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(a, b), skia.Point(a, b + e)], [hexa("#3A6EA5"), hexa("#1A2433")]))
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), p)
    texte(cc, "9:41", a + 40, b + 24, 24, C["blanc"], "fort", track=0)
    hors = prog(t, TW(16) - 0.1, 0.3)
    texte(cc, "Aucun service" if hors > 0.5 else "4G", a + d - 40, b + 24, 22, "#FF6B6B" if hors > 0.5 else C["blanc"], "fort", "droite", 0)
    for k, nom in enumerate(APPS_H):
        r_, q = divmod(k, 3)
        x = a + 80 + q * (d - 160) / 2; y = b + 260 + r_ * 200
        with Calque(cc, 1 - 0.55 * prog(t, TW(18) - 0.15 + 0.05 * k, 0.2)):
            logo_app(cc, nom, x, y, 116)
        croix(cc, x, y, 62, prog(t, TW(18) - 0.15 + 0.05 * k, 0.22))


def alerte(c, t):
    """image 0 : l'alerte rouge « indisponible en Chine » posée sur le téléphone"""
    so = prog(t, TW(4) - 0.2, 0.25, entree)
    if so >= 1: return
    u = 1.0 if t < 0.05 else apparait(t, 0.0, 1.6, 0.3)
    c.save(); c.translate(560, 900 + 8 * math.sin(t * 6)); c.rotate(-3); c.scale(mix(0.6, 1.05, u) * (1 - 0.4 * so), mix(0.6, 1.05, u) * (1 - 0.4 * so))
    with Calque(c, 1 - so):
        rrect(c, -330, -86, 660, 172, 40, C["blanc"], 1.0, (20, 50, 0.3), ROUGE, 6)
        disque(c, -250, 0, 50, ROUGE); icone(c, "triangle-alert", -250, -2, 54, C["blanc"], 2.8)
        texte(c, "Appli indisponible", -180, -52, 44, C["ink"], "noir", track=0)
        texte(c, "en Chine", -180, 4, 44, ROUGE, "noir", track=0)
    c.restore()


def h(c, t):
    sc = scene(c, t, H, None, "gauche")
    if sc is None: return
    with sc:
        ue = prog(t, 0, 0.4, sortie)
        sx, sy = secousse(t, TW(18) - 0.1, 12, 0.3)
        tel(c, 560 + sx, 1180 + sy, lambda cc, a, b, d, e: ecran_apps(cc, a, b, d, e, t),
            ry=mix(-22, -8, ue) + 3 * math.sin(t * 2.2), rz=mix(-6, 2, ue), s=mix(1.08, 1, ue))
        alerte(c, t)
        # drapeau chinois dès l'image 0
        c.save(); c.translate(860, 700); c.rotate(8); c.scale(mix(1.4, 1, ue), mix(1.4, 1, ue))
        rrect(c, -90, -60, 180, 120, 22, "#FFFFFF", 1.0, (14, 36, 0.25)); drapeau(c, "CN", -76, -46, 152, 92, 12)
        c.restore()
        # « Enregistre cette vidéo » : le signet se remplit
        us = apparait(t, TW(4) - 0.1, 1.8, 0.34) * (1 - prog(t, TW(7) + 0.1, 0.2, entree))
        if us > 0:
            rempli = t >= T_SAVE
            b = 1 + 0.25 * (1 - prog(t, T_SAVE, 0.25)) if rempli else 1
            c.save(); c.translate(230, 1060); c.scale(mix(0.3, 1, us) * b, mix(0.3, 1, us) * b)
            disque(c, 0, 0, 110, C["ink"], borne(us * 2), (14, 36, 0.3)); signet(c, 0, 0, 120, rempli, borne(us * 2))
            c.restore()
            if rempli: etincelles(c, 230, 1060, t, T_SAVE, 10, 200, "#FACE15")
            pastille_rot(c, "ENREGISTRE", 230, 1230, 34, "#FACE15", C["ink"], -6, mix(0.3, 1, us), borne(us * 2), None, (12, 28, 0.2))
        # « dix réflexes » : le 10 qui claque
        u10 = apparait(t, TW(9) - 0.08, 2.0, 0.3) * (1 - prog(t, TW(20) - 0.1, 0.2, entree))
        if u10 > 0:
            c.save(); c.translate(250, 1500); c.rotate(-8); c.scale(mix(0.3, 1, u10), mix(0.3, 1, u10))
            rrect(c, -130, -110, 260, 220, 50, C["vert"], borne(u10 * 2), (16, 40, 0.3))
            texte_centre(c, "10", 0, -8, 150, C["blanc"], "noir", borne(u10 * 2))
            c.restore()
        # « reste jusqu'au neuf » : la carte n° 9 masquée, la batterie en suspens
        u9 = apparait(t, TW(21) - 0.05, 1.6, 0.4)
        if u9 > 0:
            bob = 8 * math.sin(t * 4)
            c.save(); c.translate(820, 1560 + bob); c.rotate(6); c.scale(mix(0.3, 1, u9), mix(0.3, 1, u9))
            carte(c, -200, -150, 400, 300, 44, C["blanc"], borne(u9 * 2), (20, 46, 0.2))
            rrect(c, -170, -120, 110, 90, 22, C["ink"], borne(u9 * 2)); texte_centre(c, "9", -115, -75, 64, C["blanc"], "noir", borne(u9 * 2))
            batterie(c, 40, 30, 230, False, borne(u9 * 2), -6)
            uq = apparait(t, TW(29) - 0.05)
            if uq > 0:
                croix(c, 40, 30, 120, prog(t, TW(29) - 0.05, 0.25))
            c.restore()
            if t >= TW(31) - 0.1:
                ua = apparait(t, TW(31) - 0.1)
                pastille_rot(c, "AÉROPORT", 820, 1780, 36, ROUGE, C["blanc"], -4, mix(0.3, 1, ua), borne(ua * 2), "plane", (12, 28, 0.2))


# ─────────────────────────────────────────── S1 · pas de visa, la carte d'arrivée
def ecran_arrivee(cc, a, b, d, e, t):
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#F5F6F8"))
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, 190), peinture("#C8102E"))
    texte(cc, "9:41", a + 40, b + 24, 24, C["blanc"], "fort", track=0)
    texte(cc, "Arrival Card", a + 40, b + 96, 40, C["blanc"], "noir", track=0)
    texte(cc, "China Entry", a + 40, b + 146, 22, "#FFD6DC", "fort", track=0)
    t0 = TW(46)
    for k in range(5):
        y = b + 240 + k * 120
        uk = prog(t, t0 + 0.12 * k, 0.25)
        rrect(cc, a + 30, y, d - 60, 92, 20, C["blanc"], 1.0, None, "#E2E5EA", 3)
        rrect(cc, a + 54, y + 18, 120, 14, 7, "#C9CED6")
        rrect(cc, a + 54, y + 50, (d - 200) * uk, 18, 9, C["ink"])
    ub = prog(t, TW(50), 0.3, lambda v: rebond(v, 1.6))
    if ub > 0:
        rrect(cc, a + 30, b + 860, d - 60, 96, 48, C["vert"], borne(ub * 2))
        texte_centre(cc, "Envoyé", a + d / 2, b + 908, 34, C["blanc"], "noir", borne(ub * 2))


def s1(c, t):
    sc = scene(c, t, S1, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_form = TW(43) - 0.1
        part = prog(t, t_form, 0.4, entreeSortie)
        # passeport + « pas besoin de visa »
        if part < 1:
            with Calque(c, 1 - part):
                up = apparait(t, S1[0] + 0.1, 1.6, 0.4)
                c.save(); c.translate(540 - 700 * part, 1120); c.rotate(-5); c.scale(mix(0.4, 1, up), mix(0.4, 1, up))
                rrect(c, -230, -310, 460, 620, 34, "#1F2A44", 1.0, (24, 56, 0.28))
                rrect(c, -200, -280, 400, 560, 24, None or "#26355A", 1.0, None, "#C9A84A", 3)
                disque(c, 0, -60, 90, "#C9A84A"); disque(c, 0, -60, 74, "#26355A")
                texte_centre(c, "PASSEPORT", 0, 120, 44, "#C9A84A", "noir", 1.0, 0.08)
                c.restore()
                tampon(c, "SANS VISA", 560, 1080, t, TW(36), 70, C["vert"], -10, "check")
                if t >= TW(38) - 0.08:
                    u = apparait(t, TW(38) - 0.08)
                    pastille_rot(c, "30 JOURS", 300, 800, 44, C["ink"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "calendar", (14, 32, 0.25))
                if t >= TW(41) - 0.08:
                    u = apparait(t, TW(41) - 0.08)
                    pastille_rot(c, "JUSQU’AU 31/12/2026", 680, 1500, 40, C["vert"], C["blanc"], 4, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))
        if part > 0:
            tel(c, 540 + 900 * (1 - part), 1150, lambda cc, a, b, d, e: ecran_arrivee(cc, a, b, d, e, t), ry=-6 + 3 * math.sin(t * 2))
            if t >= TW(49) - 0.05:
                u = apparait(t, TW(49) - 0.05)
                pastille_rot(c, "EN LIGNE", 830, 760, 40, C["vert"], C["blanc"], 6, mix(0.3, 1, u), borne(u * 2), "globe", (14, 32, 0.25))
            tampon(c, "AVANT DE PARTIR", 540, 1720, t, TW(51), 52, ROUGE, -4, "plane-takeoff")


# ─────────────────────────────────────────── S2 · Alipay et WeChat installés en France, carte liée
def ecran_carte(cc, a, b, d, e, t):
    bleu = MARQUES["alipay"]
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#F5F7FA"))
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, 300), peinture(bleu))
    texte(cc, "9:41", a + 40, b + 24, 24, C["blanc"], "fort", track=0)
    logo_glyphe(cc, "alipay", a + 70, b + 130, 56, C["blanc"])
    texte(cc, "Ajouter une carte", a + 116, b + 108, 32, C["blanc"], "noir", track=0)
    uc = prog(t, TW(61) - 0.1, 0.45, lambda v: rebond(v, 1.4))
    y = mix(b + e + 100, b + 360, uc)
    rrect(cc, a + 40, y, d - 80, 240, 26, "#1B1F3B", 1.0, (14, 30, 0.25))
    rrect(cc, a + 76, y + 46, 70, 52, 10, "#D4AF37")
    for k in range(4): rrect(cc, a + 76 + k * 76, y + 150, 58, 18, 9, "#8A90B8")
    texte(cc, "VISA", a + d - 80 - 30, y + 180, 34, C["blanc"], "noir", "droite", 0.02)
    ul = prog(t, TW(64) - 0.1, 0.3, lambda v: rebond(v, 1.6))
    if ul > 0:
        rrect(cc, a + 40, b + 660, d - 80, 100, 50, C["vert"], borne(ul * 2))
        texte_centre(cc, "Carte liée", a + d / 2, b + 710, 34, C["blanc"], "noir", borne(ul * 2))


def s2(c, t):
    sc = scene(c, t, S2, "gauche", "gauche")
    if sc is None: return
    with sc:
        e = prog(t, TW(60) - 0.2, 0.4, entreeSortie)
        tuile(c, "alipay", mix(330, 220, e), mix(1100, 820, e), mix(260, 140, e), apparait(t, TW(55) - 0.08, 1.8, 0.36), rot=-6)
        tuile(c, "wechat", mix(750, 860, e), mix(1100, 820, e), mix(260, 140, e), apparait(t, TW(57) - 0.08, 1.8, 0.36), rot=6)
        if t >= TW(59) - 0.08 and e < 1:
            u = apparait(t, TW(59) - 0.08) * (1 - e)
            pastille_rot(c, "DEPUIS LA FRANCE", 540, 1400, 44, C["ink"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))
            c.save(); c.translate(540, 1530); drapeau(c, "FR", -60, -40 * u, 120, 80 * u, 10); c.restore()
        if e > 0:
            tel(c, 540, mix(2300, 1200, e), lambda cc, a, b, d, e_: ecran_carte(cc, a, b, d, e_, t), ry=-6 + 3 * math.sin(t * 2))


# ─────────────────────────────────────────── S3 · plus de cash, le QR code
def s3(c, t):
    sc = scene(c, t, S3, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_qr = TW(73) - 0.1
        part = prog(t, t_qr, 0.4, entreeSortie)
        if part < 1:
            with Calque(c, 1 - part):
                for k in range(5):
                    uk = apparait(t, TW(66) - 0.1 + 0.07 * k, 1.6, 0.35)
                    billet_yuan(c, 540 + (k - 2) * 60, 1120 - k * 40 + 60 * (1 - uk), 520 * mix(0.5, 1, uk), -14 + 7 * k, borne(uk * 2))
                croix(c, 540, 1060, 300, prog(t, TW(72) - 0.08, 0.3))
                tampon(c, "FINI LE CASH", 540, 1500, t, TW(72), 64, ROUGE, -6, "banknote")
        if part > 0:
            tel(c, 540 + 900 * (1 - part), 1150, lambda cc, a, b, d, e: ecran_alipay(cc, a, b, d, e, t, TW(74), TW(81), "Métro"),
                ry=-6 + 3 * math.sin(t * 2))
            if t >= TW(76) - 0.08:
                u = apparait(t, TW(76) - 0.08)
                pastille_rot(c, "TU SCANNES", 280, 760, 40, C["vert"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "scan-line", (14, 32, 0.25))
            if t >= TW(80) - 0.08:
                u = apparait(t, TW(80) - 0.08)
                pastille_rot(c, "OU ON TE SCANNE", 790, 1640, 38, C["ink"], C["blanc"], 5, mix(0.3, 1, u), borne(u * 2), "smile", (14, 32, 0.25))


# ─────────────────────────────────────────── S4 · Trip.com, pas Booking
def s4(c, t):
    sc = scene(c, t, S4, "gauche", "gauche")
    if sc is None: return
    with sc:
        ut = apparait(t, TW(87) - 0.1, 1.7, 0.4)
        for k, (ic, lab, i, x) in enumerate((("bed-double", "Hôtels", 84, 230), ("plane", "Vols", 85, 540), ("ticket", "Trains", 86, 850))):
            u = apparait(t, TW(i) - 0.08, 1.8, 0.34)
            if u <= 0: continue
            y = mix(1080, 1440, ut) if ut > 0 else 1080
            c.save(); c.translate(x, y); c.rotate((k - 1) * 4); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
            carte(c, -130, -130, 260, 260, 44, C["blanc"], borne(u * 2), (18, 40, 0.16))
            disque(c, 0, -26, 64, C["vertDoux"], borne(u * 2)); icone(c, ic, 0, -26, 70, C["vertFonce"], 2.4, borne(u * 2))
            texte_centre(c, lab, 0, 76, 34, C["ink"], "noir", borne(u * 2))
            c.restore()
        if ut > 0:
            tuile(c, "tripdotcom", 540, 1020, 280, ut, rot=-4)
            if t >= TW(87) + 0.1:
                u = apparait(t, TW(87) + 0.1)
                pastille_rot(c, "TRIP.COM", 540, 1220, 46, MARQUES["tripdotcom"], C["blanc"], -3, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))
        ub = apparait(t, TW(94) - 0.1, 1.8, 0.34)
        if ub > 0:
            tuile(c, "bookingdotcom", 830, 760, 150, ub, rot=8)
            croix(c, 830, 760, 92, prog(t, TW(94) + 0.05, 0.25))


# ─────────────────────────────────────────── S5 · oublie Uber, c'est Didi
def duel(c, t, nom_out, out_label, t_out, t_x, in_lab, in_coul, t_in, extra=None):
    uo = apparait(t, t_out, 1.7, 0.36)
    sw = prog(t, t_in - 0.1, 0.35, entreeSortie)
    if uo > 0 and sw < 1:
        with Calque(c, 1 - sw):
            tuile(c, nom_out, mix(540, 260, sw), mix(1100, 820, sw), mix(320, 180, sw), uo, label=out_label, couleur="#000000" if out_label else None, rot=-4)
            croix(c, mix(540, 260, sw), mix(1100, 820, sw), mix(200, 112, sw), prog(t, t_x, 0.25))
    ui = apparait(t, t_in, 1.8, 0.4)
    if ui > 0:
        bob = 10 * math.sin(t * 3.5)
        tuile(c, None, 540, 1100 + bob, 340, ui, label=in_lab, couleur=in_coul, rot=3)
        if extra: extra(ui)


def s5(c, t):
    sc = scene(c, t, S5, "gauche", "gauche")
    if sc is None: return
    with sc:
        duel(c, t, "uber", None, S5[0] + 0.1, TW(97) - 0.05, "DiDi", "#FF7A00", TW(99) - 0.1)
        if t >= TW(99) + 0.1:
            u = apparait(t, TW(99) + 0.1)
            pastille_rot(c, "TON TAXI", 540, 1380, 44, C["ink"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))


# ─────────────────────────────────────────── S6 · oublie Google Maps, c'est Amap
def plan_amap(c, cx, cy, w, h, t, t0):
    rrect(c, cx - w / 2, cy - h / 2, w, h, 40, "#EAF2FB", 1.0, (18, 40, 0.16))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), 40, 40), doAntiAlias=True)
    for k in range(-3, 4):
        trait(c, cx - w, cy + k * 90 + 20, cx + w, cy + k * 90 - 60, "#FFFFFF", 22)
        trait(c, cx + k * 120, cy - h, cx + k * 120 + 80, cy + h, "#FFFFFF", 16)
    c.restore()
    for k, (dx, dy) in enumerate(((-160, -60), (120, -110), (40, 90), (-90, 120), (190, 60))):
        u = apparait(t, t0 + 0.08 * k, 2.0, 0.3)
        if u <= 0: continue
        c.save(); c.translate(cx + dx, cy + dy - 30 * (1 - u)); c.scale(u, u)
        disque(c, 0, 0, 34, ROUGE if k % 2 == 0 else "#1E7BFF", 1.0, (6, 14, 0.2)); icone(c, "map-pin", 0, 0, 34, C["blanc"], 2.6)
        c.restore()


def s6(c, t):
    sc = scene(c, t, S6, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_plan = TW(106) - 0.1
        e = prog(t, t_plan, 0.4, entreeSortie)
        with Calque(c, 1 - e):
            duel(c, t, "googlemaps", None, S6[0] + 0.1, TW(103) - 0.05, "Amap", "#1E7BFF", TW(105) - 0.1)
        if e > 0:
            plan_amap(c, 540, mix(1700, 1180, e), 820, 620, t, TW(110) - 0.1)
            tuile(c, None, 230, mix(1400, 820, e), 170, e, label="Amap", couleur="#1E7BFF", rot=-6)
            if t >= TW(112) - 0.1:
                u = apparait(t, TW(112) - 0.1)
                pastille_rot(c, "LES RESTOS", 800, 1560, 42, ROUGE, C["blanc"], 5, mix(0.3, 1, u), borne(u * 2), "map-pin", (14, 32, 0.25))


# ─────────────────────────────────────────── S7 · se faire livrer : Ele.me
def s7(c, t):
    sc = scene(c, t, S7, "gauche", "gauche")
    if sc is None: return
    with sc:
        ul = apparait(t, TW(114) - 0.1, 1.7, 0.4)
        if ul > 0:
            bas = prog(t, TW(120) - 0.2, 0.35, entreeSortie)
            x = mix(-200, 540, prog(t, TW(114) - 0.1, 0.5, sortie)) + mix(0, -240, bas) + 6 * math.sin(t * 12)
            y = mix(1100, 1480, bas); r_ = mix(190, 110, bas)
            c.save(); c.translate(x, y); c.scale(ul, ul)
            disque(c, 0, 0, r_, "#0097FF", 1.0, (12, 30, 0.2)); icone(c, "bike", 0, 0, r_ * 1.1, C["blanc"], 2.6)
            c.restore()
            for k in range(4): trait(c, x - r_ - 40 - k * 30, y - 40 + k * 26, x - r_ - 130 - k * 30, y - 40 + k * 26, "#9CCBF5", 8)
        ue = apparait(t, TW(120) - 0.1, 1.8, 0.4)
        tuile(c, None, 560, 1020, 330, ue, label="Ele.me", couleur="#0097FF", rot=-3)
        if t >= TW(119) - 0.1:
            u = apparait(t, TW(119) - 0.1)
            pastille_rot(c, "À MANGER", 800, 1500, 44, C["ink"], C["blanc"], 5, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))


# ─────────────────────────────────────────── S8 · e-SIM ou VPN, et un traducteur
def puce(c, cx, cy, w, u):
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(-8); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
    with Calque(c, borne(u * 2)):
        pq = skia.Path(); h = w * 1.3; cut = w * 0.28
        pq.moveTo(-w / 2, -h / 2); pq.lineTo(w / 2 - cut, -h / 2); pq.lineTo(w / 2, -h / 2 + cut); pq.lineTo(w / 2, h / 2); pq.lineTo(-w / 2, h / 2); pq.close()
        c.drawPath(pq, peinture(C["ink"]))
        rrect(c, -w * 0.3, -w * 0.22, w * 0.6, w * 0.5, 12, "#D4AF37")
        texte_centre(c, "e-SIM", 0, h * 0.34, w * 0.2, C["blanc"], "noir", 1.0, 0)
    c.restore()


def s8(c, t):
    sc = scene(c, t, S8, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_trad = TW(134) - 0.1
        e = prog(t, t_trad, 0.4, entreeSortie)
        if e < 1:
            with Calque(c, 1 - e):
                puce(c, 280, 1060, 240, apparait(t, TW(123) - 0.08))
                uv = apparait(t, TW(126) - 0.08)
                if uv > 0:
                    c.save(); c.translate(790, 1060); c.rotate(6); c.scale(mix(0.3, 1, uv), mix(0.3, 1, uv))
                    disque(c, 0, 0, 130, C["vert"], borne(uv * 2), (14, 34, 0.25)); icone(c, "shield-check", 0, -12, 120, C["blanc"], 2.6, borne(uv * 2))
                    texte_centre(c, "VPN", 0, 80, 40, C["blanc"], "noir", borne(uv * 2))
                    c.restore()
                for k, nom in enumerate(("instagram", "whatsapp")):
                    x = 380 + k * 320
                    u = apparait(t, TW(127) - 0.05 + 0.1 * k, 1.8, 0.34)
                    tuile(c, nom, x, 1480, 210, u)
                    if u > 0:
                        ok = prog(t, TW(132) - 0.05, 0.25)
                        c.save(); c.translate(x + 80, 1390)
                        disque(c, 0, 0, 40, ROUGE if ok < 0.5 else C["vert"], u)
                        icone(c, "lock" if ok < 0.5 else "check", 0, 0, 44, C["blanc"], 3, u)
                        c.restore()
        if e > 0:
            tuile(c, "googletranslate", 540, mix(1700, 880, e), 200, e)
            bulle_txt(c, "Bonjour !", 360, 1160, 50, C["blanc"], C["ink"], apparait(t, TW(136) - 0.1), False)
            bulle_txt(c, "Nǐ hǎo !", 720, 1330, 50, C["vert"], C["blanc"], apparait(t, TW(136) + 0.15), True)
            ua = apparait(t, TW(137) - 0.05)
            if ua > 0:
                bulle_txt(c, "English ?", 420, 1560, 46, C["blanc"], C["ink"], ua, False)
                croix(c, 420, 1560, 120, prog(t, TW(138), 0.25))


# ─────────────────────────────────────────── S9 · la batterie externe CCC
def s9(c, t):
    sc = scene(c, t, S9, "gauche", "gauche")
    if sc is None: return
    with sc:
        t_ok = TW(157) - 0.1
        e = prog(t, t_ok, 0.4, entreeSortie)
        ub = apparait(t, TW(142) - 0.08, 1.7, 0.4)
        if e < 1 and ub > 0:
            with Calque(c, 1 - e):
                sx, sy = secousse(t, TW(152), 14, 0.35)
                batterie(c, 540 + sx, 1100 + sy, 560 * mix(0.5, 1, ub), False, borne(ub * 2), -6)
                if t >= TW(146) - 0.1:
                    u = apparait(t, TW(146) - 0.1)
                    pastille_rot(c, "PAS DE LOGO CCC", 320, 820, 40, C["ink"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), None, (14, 32, 0.25))
                croix(c, 540, 1100, 320, prog(t, TW(152) - 0.05, 0.3))
                tampon(c, "CONFISQUÉE", 560, 1500, t, TW(152), 66, ROUGE, -8, "triangle-alert")
                if t >= TW(155) - 0.1:
                    u = apparait(t, TW(155) - 0.1)
                    pastille_rot(c, "VOL INTÉRIEUR", 780, 1700, 38, C["ink"], C["blanc"], 4, mix(0.3, 1, u), borne(u * 2), "plane", (14, 32, 0.25))
        if e > 0:
            bob = 8 * math.sin(t * 3)
            batterie(c, 540, mix(1800, 1100, e) + bob, 560, True, 1.0, 4)
            coche(c, 800, 900, 60, apparait(t, t_ok + 0.25, 2.0, 0.3))
            if t >= TW(158) - 0.05:
                u = apparait(t, TW(158) - 0.05)
                pastille_rot(c, "ACHÈTE-LA EN CHINE", 540, 1480, 42, C["vert"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "store", (14, 32, 0.25))


# ─────────────────────────────────────────── S10 · le tax refund dès 200 ¥
def s10(c, t):
    sc = scene(c, t, S10, "gauche", "gauche")
    if sc is None: return
    with sc:
        ur = apparait(t, TW(161) - 0.08, 1.6, 0.4)
        if ur > 0:
            c.save(); c.translate(540, 1110); c.rotate(-4); c.scale(mix(0.4, 0.85, ur), mix(0.4, 0.85, ur))
            with Calque(c, borne(ur * 2)):
                pq = skia.Path(); w, hh = 520, 680
                pq.moveTo(-w / 2, -hh / 2)
                pq.lineTo(w / 2, -hh / 2)
                for k in range(10):
                    pq.lineTo(w / 2 - (k + 0.5) * w / 10, hh / 2 + (14 if k % 2 == 0 else 0))
                pq.lineTo(-w / 2, hh / 2); pq.close()
                ombre_sol(c, 0, hh / 2 + 40, 240, 24, 0.15)
                c.drawPath(pq, peinture("#FFFFFF"))
                rrect(c, -w / 2, -hh / 2, w, 130, 0, C["ink"])
                texte_centre(c, "TAX FREE", 0, -hh / 2 + 65, 58, C["blanc"], "noir", 1.0, 0.04)
                for k in range(5): rrect(c, -w / 2 + 50, -hh / 2 + 190 + k * 70, (w - 100) * (0.9 - 0.12 * (k % 3)), 20, 10, "#E1E4E2")
                rrect(c, -w / 2 + 40, hh / 2 - 150, w - 80, 2, 1, "#C9CCC8")
                texte(c, "≥ 200 ¥", -w / 2 + 50, hh / 2 - 120, 52, C["ink"], "noir", track=0)
            c.restore()
        if t >= TW(163) - 0.08:
            u = apparait(t, TW(163) - 0.08)
            pastille_rot(c, "200 ¥ MINIMUM", 790, 790, 42, C["ink"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "receipt", (14, 32, 0.25))
        if t >= TW(167) - 0.08:
            u = apparait(t, TW(167) - 0.08)
            pastille_rot(c, "MÊME MAGASIN", 290, 1500, 38, C["vert"], C["blanc"], -5, mix(0.3, 1, u), borne(u * 2), "store", (14, 32, 0.25))
        tampon(c, "REMBOURSÉ", 620, 1700, t, TW(171), 64, C["vert"], -6, "banknote")
        confettis(c, 620, 1700, t, TW(171) + 0.04, 22, 320, 7)


# ─────────────────────────────────────────── SP · envoie-la à celui qui part avec toi
def sp(c, t):
    sc = scene(c, t, SP, "zoom", "gauche", de=0.25)
    if sc is None: return
    with sc:
        u = apparait(t, SP[0] + 0.05, 1.8, 0.4)
        c.save(); c.translate(540, 1050); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
        disque(c, 0, 0, 200, C["vert"], borne(u * 2), (18, 46, 0.3)); icone(c, "send", -8, 8, 200, C["blanc"], 2.6, borne(u * 2))
        c.restore()
        ua = apparait(t, TW(176) - 0.05)
        if ua > 0:
            c.save(); c.translate(540, 1420); c.scale(mix(0.3, 1, ua), mix(0.3, 1, ua))
            rrect(c, -230, -70, 460, 140, 70, C["ink"], borne(ua * 2), (14, 32, 0.25))
            icone(c, "users", -150, 0, 70, C["blanc"], 2.6, borne(ua * 2)); texte_centre(c, "Ton pote", 50, 0, 46, C["blanc"], "noir", borne(ua * 2))
            c.restore()
        # papier qui part
        up = prog(t, TW(177), 0.5, entree)
        if 0 < up < 1:
            x, y = mix(540, 1150, up), mix(1050, 500, up)
            c.save(); c.translate(x, y); c.rotate(-30); icone(c, "send", 0, 0, 90, C["vert"], 2.6, 1 - up); c.restore()


# ─────────────────────────────────────────── SC1 · tu vas en Chine acheter de la marchandise ? pas besoin d'y aller
def sc1(c, t):
    sc = scene(c, t, SC1, "gauche", "gauche")
    if sc is None: return
    with sc:
        ua = apparait(t, SC1[0] + 0.05, 1.8, 0.4) * (1 - prog(t, TW(187) - 0.2, 0.2, entree))
        if ua > 0:
            c.save(); c.translate(540, 1100 + 10 * math.sin(t * 4)); c.rotate(-8); c.scale(mix(0.3, 1, ua), mix(0.3, 1, ua))
            disque(c, 0, 0, 220, C["ink"], borne(ua * 2), (18, 46, 0.3)); icone(c, "plane", 0, 0, 230, C["blanc"], 2.4, borne(ua * 2))
            rrect(c, 120, -250, 180, 120, 22, "#FFFFFF", borne(ua * 2), (14, 36, 0.25)); drapeau(c, "CN", 134, -236, 152, 92, 12)
            c.restore()
        for k, (dx, dy) in enumerate(((-120, 90), (120, 90), (0, -60), (-240, -60), (240, -60))):
            uk = apparait(t, TW(187) - 0.1 + 0.06 * k, 2.0, 0.32)
            if uk > 0:
                carton(c, 540 + dx, 1180 + dy - 220 * (1 - uk), 210, 0, borne(uk * 2), 3 * math.sin(t * 5 + k))
        us = apparait(t, TW(190) - 0.08, 1.7, 0.4)
        if us > 0:
            sneaker(c, 300, 870 + 8 * math.sin(t * 4), 330 * mix(0.5, 1, us), alpha=borne(us * 2), rot=-8)
        tampon(c, "PAS BESOIN D’Y ALLER", 540, 1560, t, TW(196) - 0.05, 56, ROUGE, -5, "x-circle")
        if t >= TW(199) - 0.1:
            u = apparait(t, TW(199) - 0.1)
            pastille_rot(c, "DÉJÀ FAIT", 800, 820, 46, C["vert"], C["blanc"], 6, mix(0.3, 1, u), borne(u * 2), "check", (14, 32, 0.25))


# ─────────────────────────────────────────── SC2 · nos fournisseurs validés à Guangzhou et Shenzhen
def sc2(c, t):
    sc = scene(c, t, SC2, "gauche", None, de=0.3)
    if sc is None: return
    with sc:
        e = prog(t, SC2[0] + 0.05, 0.45, sortie)
        lignes = [dict(t=TW(205) - 0.05, image="photos/chaussures/etagere-baskets-running-6-modeles", nom="Baskets", ville="Guangzhou"),
                  dict(t=TW(207) - 0.05, image="produits/electronique/casque-audio", nom="Électronique", ville="Shenzhen"),
                  dict(t=TW(209), image="produits/textile/veste-racing-noire", nom="Textile", ville="Guangzhou")]
        tel(c, 540, 1150, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-30, -4, e) + 2 * math.sin(t * 2.2), s=mix(0.6, 1, e), alpha=borne(e * 2))
        tampon(c, "VALIDÉS", 800, 760, t, TW(205), 58, C["vert"], -8, "badge-check")


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
MSGS = [dict(t=TW(217) - 0.05, moi=True, type="texte", texte="Je veux 2 paires de B30"),
        dict(t=TW(219), moi=False, type="qr")]


def sc3(c, t):
    sc = scene(c, t, SC3, None, "gauche")
    if sc is None: return
    with sc:
        e = prog(t, SC3[0] + 0.2, 0.4, sortie)
        t_pay = TW(221) - 0.1
        if t < t_pay:
            tel(c, 540, mix(2200, 1160, e), lambda cc, a, b, d, e_: ecran_wechat(cc, a, b, d, e_, t, "Fournisseur Baskets", MSGS), ry=-6 + 2 * math.sin(t * 2))
            tuile(c, "wechat", 200, 800, 150, apparait(t, TW(219) - 0.1), rot=-8)
        else:
            tel(c, 540, 1160, lambda cc, a, b, d, e_: ecran_alipay(cc, a, b, d, e_, t, t_pay + 0.1, TW(223) + 0.2, "Fournisseur"), ry=-6 + 2 * math.sin(t * 2))
            tuile(c, "alipay", 880, 800, 150, apparait(t, TW(223) - 0.1), rot=8)
        texte_centre(c, "Échange illustratif", 540, 1665, 22, C["grisClair"], "fort", 1.0, 0.04)


# ─────────────────────────────────────────── SC4 · dis-moi en commentaire ce que tu revends
REPONSE = "Des sneakers"
T_TAPE = [TW(227) + k * 0.07 for k in range(len(REPONSE))]


def sc4(c, t):
    sc = scene(c, t, SC4, "bas", None, de=0.3)
    if sc is None: return
    with sc:
        u = prog(t, SC4[0], 0.4, sortie)
        y0 = mix(2000, 1000, u)
        carte(c, 60, y0, 960, 760, 54, C["blanc"], 1.0, (26, 60, 0.2))
        icone(c, "message-circle", 140, y0 + 80, 52, C["ink"], 2.4)
        texte(c, "Commentaires", 190, y0 + 56, 38, C["ink"], "noir", track=0)
        for k in range(3):
            yy = y0 + 170 + k * 140
            disque(c, 140, yy + 30, 40, "#E6EBE8"); rrect(c, 200, yy + 4, 260 - 40 * k, 20, 10, "#E6EBE8"); rrect(c, 200, yy + 40, 520 - 60 * k, 20, 10, "#EEF1EF")
        rrect(c, 100, y0 + 610, 880, 100, 50, "#F2F4F3", 1.0, None, C["vert"] if t >= TW(224) else "#E1E5E3", 4)
        tx = "".join(l for l, tl in zip(REPONSE, T_TAPE) if t >= tl)
        texte(c, tx or "Ajoute un commentaire…", 150, y0 + 634, 38, C["ink"] if tx else C["grisClair"], "noir" if tx else "moyen", track=0)
        if TW(224) <= t < T_TAPE[-1] + 0.6 and int(t * 4) % 2 == 0:
            rrect(c, 150 + largeur(tx, 38, "noir", 0) + 4, y0 + 632, 5, 50, 2, C["ink"])
        if t >= TW(225) - 0.1:
            ub = apparait(t, TW(225) - 0.1)
            pastille_rot(c, "EN COMMENTAIRE", 300, 820, 42, C["vert"], C["blanc"], -6, mix(0.3, 1, ub), borne(ub * 2), "message-circle", (14, 32, 0.25))


def carton_final(c, t):
    if t < T_FIN: return
    u = prog(t, T_FIN, 0.4, sortie)
    disque(c, 540, 1060, 440 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
    ul = prog(t, T_FIN + 0.08, 0.36, lambda v: rebond(v, 1.6))
    lw = 760 * mix(0.6, 1, ul)
    iw_, ih_ = taille_img("logo"); lh = lw * ih_ / iw_
    image(c, "logo", 540 - lw / 2, 1000 - lh / 2, lw, borne(ul * 2))
    ub = prog(t, T_FIN + 0.3, 0.36, lambda v: rebond(v, 1.8))
    if ub > 0:
        c.save(); c.translate(540, 1180); c.scale(mix(0.4, 1, ub), mix(0.4, 1, ub))
        with Calque(c, borne(ub * 2)):
            rrect(c, -250, -54, 500, 108, 54, C["ink"], 1.0, (16, 40, 0.25))
            signet(c, -170, 0, 56, True); texte_centre(c, "Enregistre-la", 40, 0, 40, C["blanc"], "noir")
        c.restore()
    etincelles(c, 540, 1180, t, T_FIN + 0.45, 12, 360)


# ─────────────────────────────────────────── sons, flou, éclairs
son(0.0, "impact", -6); son(0.0, "whoosh_court", -12); son(0.25, "pop", -13)
son(TW(4) - 0.1, "pop", -11); son(T_SAVE, "ching", -10); son(TW(9) - 0.08, "tampon", -8)
son(TW(16) - 0.1, "blip", -13)
for k in range(len(APPS_H)): son(TW(18) - 0.15 + 0.05 * k, "clic", -13)
son(TW(18) - 0.1, "impact_doux", -9); son(TW(21) - 0.05, "pop", -11); son(TW(29) - 0.05, "tampon", -9); son(TW(31) - 0.1, "pop", -12)
for (a, b), n in NUMS:
    son(a - 0.02, "whoosh", -13); son(a + 0.05, "pop", -10)
son(TW(36) - 0.12, "tampon", -7); son(TW(38) - 0.08, "pop", -11); son(TW(41) - 0.08, "pop", -11); son(TW(43) - 0.1, "whoosh_court", -13)
for k in range(5): son(TW(46) + 0.12 * k, "frappe", -15)
son(TW(49) - 0.05, "pop", -11); son(TW(50), "check", -11); son(TW(51) - 0.12, "tampon", -8)
son(TW(55) - 0.08, "pop", -10); son(TW(57) - 0.08, "pop", -10); son(TW(59) - 0.08, "pop", -12); son(TW(60) - 0.2, "whoosh_long", -15)
son(TW(61) - 0.1, "swipe", -14); son(TW(64) - 0.1, "check", -10)
for k in range(5): son(TW(66) - 0.1 + 0.07 * k, "swipe", -16)
son(TW(72) - 0.12, "tampon", -7); son(TW(72) - 0.08, "impact", -8); son(TW(73) - 0.1, "whoosh_court", -13)
son(TW(74), "blip", -12); son(TW(76) - 0.08, "pop", -11); son(TW(80) - 0.08, "pop", -11); son(TW(81), "ching", -10)
for i in (84, 85, 86): son(TW(i) - 0.08, "pop", -11)
son(TW(87) - 0.1, "whoosh_court", -12); son(TW(87) + 0.1, "pop", -10); son(TW(94) - 0.1, "pop", -12); son(TW(94) + 0.05, "impact_doux", -9)
son(S5[0] + 0.1, "pop", -11); son(TW(97) - 0.05, "impact_doux", -9); son(TW(99) - 0.1, "ching", -10); son(TW(99) + 0.1, "pop", -12)
son(S6[0] + 0.1, "pop", -11); son(TW(103) - 0.05, "impact_doux", -9); son(TW(105) - 0.1, "ching", -10); son(TW(106) - 0.1, "whoosh_court", -13)
for k in range(5): son(TW(110) - 0.1 + 0.08 * k, "blip", -16)
son(TW(112) - 0.1, "pop", -11)
son(TW(117) - 0.1, "whoosh_long", -14); son(TW(119) - 0.1, "pop", -11); son(TW(120) - 0.1, "ching", -10)
son(TW(123) - 0.08, "pop", -11); son(TW(126) - 0.08, "pop", -11); son(TW(127) - 0.05, "pop", -12); son(TW(127) + 0.05, "pop", -12)
son(TW(132) - 0.05, "check", -10); son(TW(134) - 0.1, "whoosh_court", -13); son(TW(136) - 0.1, "message", -11); son(TW(136) + 0.15, "message_in", -11)
son(TW(137) - 0.05, "pop", -12); son(TW(138), "impact_doux", -10)
son(TW(142) - 0.08, "pop", -10); son(TW(146) - 0.1, "pop", -11); son(TW(152) - 0.12, "tampon", -6); son(TW(152) - 0.08, "impact", -7)
son(TW(155) - 0.1, "pop", -12); son(TW(157) - 0.1, "whoosh_court", -12); son(TW(157) + 0.15, "check", -10); son(TW(158) - 0.05, "pop", -11)
son(TW(161) - 0.08, "pop", -10); son(TW(163) - 0.08, "pop", -11); son(TW(167) - 0.08, "pop", -11); son(TW(171) - 0.12, "tampon", -7); son(TW(171) + 0.04, "ching", -10)
son(SP[0] - 0.02, "whoosh", -13); son(SP[0] + 0.05, "pop", -10); son(TW(176) - 0.05, "pop", -11); son(TW(177), "whoosh_court", -11)
son(SC1[0] - 0.02, "whoosh", -13)
for k in range(5): son(TW(187) - 0.1 + 0.06 * k, "impact_doux", -13)
son(TW(190) - 0.08, "pop", -11); son(TW(196) - 0.17, "tampon", -7); son(TW(199) - 0.1, "pop", -11)
son(SC2[0] - 0.02, "whoosh", -13); son(TW(205) - 0.12, "tampon", -8); son(TW(205) - 0.05, "ching", -12); son(TW(207) - 0.05, "ching", -14); son(TW(209), "ching", -14)
son(T_LOGO - 0.1, "montee", -15); son(T_LOGO + 0.24, "impact", -7); son(T_LOGO + 0.26, "verre", -9); son(SC3[0], "whoosh_long", -14)
son(TW(217) - 0.05, "message", -11); son(TW(219), "message_in", -11); son(TW(219) - 0.1, "pop", -12); son(TW(221) - 0.1, "whoosh_court", -12); son(TW(223) + 0.2, "ching", -9)
son(SC4[0], "whoosh", -13); son(TW(225) - 0.1, "pop", -11)
for tl in T_TAPE: son(tl, "frappe", -15)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.1, "impact_doux", -8); son(T_FIN + 0.12, "verre", -8); son(T_FIN + 0.3, "pop", -11)

for a, b in [(TW(18) - 0.15, TW(18) + 0.15)] + [(a - 0.02, a + 0.3) for (a, b), n in NUMS] + \
            [(TW(43) - 0.1, TW(43) + 0.3), (TW(60) - 0.2, TW(60) + 0.2), (TW(73) - 0.1, TW(73) + 0.3), (TW(106) - 0.1, TW(106) + 0.3),
             (TW(134) - 0.1, TW(134) + 0.3), (TW(157) - 0.1, TW(157) + 0.3), (SP[0] - 0.02, SP[0] + 0.3), (SC1[0] - 0.02, SC1[0] + 0.3),
             (SC2[0] - 0.02, SC2[0] + 0.3), (T_LOGO, T_LOGO + 0.4), (SC3[0], SC3[0] + 0.4), (SC4[0], SC4[0] + 0.3), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, "#FFFFFF", 0.2), (T_SAVE, "#FACE15", 0.12), (TW(18) - 0.1, C["rouge"], 0.12), (TW(36), C["vert"], 0.08), (TW(72) - 0.08, C["rouge"], 0.12),
                    (TW(99) - 0.1, "#FF7A00", 0.08), (TW(105) - 0.1, "#1E7BFF", 0.08), (TW(120) - 0.1, "#0097FF", 0.08), (TW(152) - 0.08, C["rouge"], 0.14),
                    (TW(171), C["vert"], 0.10), (TW(196) - 0.1, C["rouge"], 0.10), (T_LOGO + 0.24, C["blanc"], 0.15), (TW(223) + 0.2, C["vert"], 0.08),
                    (T_FIN + 0.1, C["vert"], 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def alpha_bandeau(t, r):
    return borne(prog(t, 0.45, 0.3) * (1 - prog(t, T_FIN - 0.05, 0.25)) * (1 - borne(r / 400)))


def dessine(c, t):
    fond(c, t)
    for s in (h, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, sp, sc1, sc2, sc3, sc4):
        s(c, t)
    numero(c, t)
    gros_numero(c, t)
    r = disque_logo(c, t)
    bandeau(c, t, alpha_bandeau(t, r))
    carton_final(c, t)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if r > 900 else C["ink"])
