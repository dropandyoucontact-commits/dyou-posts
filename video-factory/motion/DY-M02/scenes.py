"""DY-M02 v2 « Sur place » — DROP&YOU en vue subjective sur rushes à ÉCRAN VERT (29,5 s).

v1 (08/10/2026, dans v1/) : rushes à écran noir, suivi approximatif → le contenu « bougeait » sur le téléphone.
v2 : Youssef a régénéré les rushes avec un écran vert uni. suivi_vert.py détoure le vert (doigts et Dynamic
Island passent devant au pixel près) et ajuste les 4 bords de l'écran image par image.
Les panneaux qui sortent de l'écran sont en VERRE FUMÉ (demande de Youssef, d'après ses références) : le
rush flouté derrière, voile sombre, liseré clair, reflet ; texte blanc. Voix plus forte (mixer --lufs -9).

Voix : moteur/outils/voix.py (Tomy, 3,8 mots/s). Chaque élément cite le mot qu'il illustre.
"""
import functools, json, math, pathlib, sys
import numpy as np
import skia
from PIL import Image

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
import kit as KM

DUREE = 29.55
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a

VIOLET = dict(vert="#7C3AED", vertFonce="#5B21B6", vertDoux="#EDE9FE", vertMoyen="#C4B5FD")
VERT = dict(vert="#00B862", vertFonce="#00804A", vertDoux="#E2F7EB", vertMoyen="#9BE3BD")
C.update(VIOLET)
LILAS = "#B9A3FF"                # accent violet lisible sur verre sombre
T_CB = TW(89) - 0.08
_ECH = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)

# ─────────────────────────────────────────── sous-titres
SOUS = SousTitres(K, [
    [(0, "T’as"), (1, "besoin"), (2, "de"), (3, "quelqu’un", "g")],
    [(4, "sur"), (5, "place,", "g"), (6, "en"), (7, "Chine ?", "g")],
    [(8, "C’est"), (9, "notre"), (10, "métier,", "g")],
    [(11, "chez"), (12, "DROP&YOU.", "g")],
    [(15, "Baskets,", "g"), (16, "fringues,", "g")],
    [(17, "électronique,", "g"), (18, "montres :", "g")],
    [(19, "tout"), (20, "notre"), (21, "catalogue", "g"), (22, "tient"), (23, "dans"), (24, "ton"), (25, "téléphone.")],
    [(26, "Tu"), (27, "vises"), (28, "un"), (29, "modèle", "g"), (30, "précis ?")],
    [(31, "Envoie-nous"), (32, "simplement"), (33, "une"), (34, "photo.", "g")],
    [(35, "On"), (36, "te"), (37, "propose"), (38, "plusieurs"), (39, "qualités,", "g")],
    [(40, "avec"), (41, "un"), (42, "prix", "g"), (43, "qui"), (44, "inclut"), (45, "la"), (46, "livraison.", "g")],
    [(47, "Compte"), (48, "8"), (49, "à"), (50, "12", "g"), (51, "jours", "g")],
    [(52, "jusqu’à"), (53, "ta"), (54, "porte,", "g")],
    [(55, "en"), (56, "France,", "g"), (57, "en"), (58, "Belgique,", "g")],
    [(59, "ou"), (60, "partout", "g"), (61, "ailleurs.")],
    [(62, "Pour"), (63, "toi,", "g")],
    [(64, "ou"), (65, "pour"), (66, "revendre", "g"), (67, "en"), (68, "quantité,", "g")],
    [(69, "on"), (70, "gère"), (71, "les"), (72, "deux.", "g")],
    [(73, "Règlement"), (74, "par"), (75, "PayPal,", "g")],
    [(76, "virement", "g"), (77, "ou"), (78, "carte.", "g")],
    [(79, "Écris-nous"), (80, "sur"), (81, "Snap,", "g")],
    [(82, "dropandyou1,", "g")],
    [(86, "ou"), (87, "sur"), (88, "WhatsApp.", "g")],
    [(89, "Et"), (90, "si"), (91, "tu"), (92, "préfères"), (93, "traiter"), (94, "toi-même")],
    [(95, "avec"), (96, "les"), (97, "fournisseurs,", "g"), (98, "comme"), (99, "moi,")],
    [(100, "c’est"), (101, "dans"), (102, "le"), (103, "ChinaBook.", "g")],
    [(None, "Les", "", 28.0), (None, "fournisseurs", "", 28.08), (None, "en", "", 28.24), (None, "direct.", "g", 28.3)],
], y=262, taille=88)

# ─────────────────────────────────────────── les rushes verts : (début, fin, rush, temps source, vitesse, miroir)
FPS_R = 24
T_DIVE = TW(89) - 0.42           # on plonge dans l'écran juste avant « Et si tu préfères… »
PLANS = [
    (0.0, TW(17) - 0.04, "baskets", 0.0, 1.0, False),
    (TW(17) - 0.04, TW(31) - 0.06, "magasin", 0.05, 1.0, False),
    (TW(31) - 0.06, TW(47) - 0.06, "surron-a", 0.0, 0.93, False),
    (TW(47) - 0.06, TW(69) - 0.06, "usine", 0.0, 0.845, False),
    (TW(69) - 0.06, T_DIVE + 0.36, "surron-b", 0.0, 0.775, True),
]
T_POV = PLANS[-1][1]


@functools.lru_cache(maxsize=None)
def suivi(nom):
    return np.array(json.loads((P / "suivi" / f"{nom}.json").read_text())["coins"])


@functools.lru_cache(maxsize=300)
def fond_rush(nom, k, flou=False):
    return skia.Image.open(str(P / "renders" / "cache-rush" / nom / ("flou/" if flou else "") / f"{k + 1:05d}.jpg"))


@functools.lru_cache(maxsize=300)
def masque_rush(nom, k):
    m = np.array(Image.open(P / "suivi" / nom / f"{k + 1:05d}.png").convert("L"))
    a = np.zeros(m.shape + (4,), np.uint8); a[..., 3] = m; a[..., :3] = m[..., None]
    return skia.Image.fromarray(a)


def plan_a(t):
    for p in PLANS:
        if p[0] <= t < p[1]: return p
    return None


def etat(t):
    """rush affiché à t : (nom, image k, miroir, quadrilatère de l'écran en pixels de sortie)"""
    t = max(0.0, t)
    p = plan_a(t)
    if p is None: return None
    a, b, nom, s0, v, mir = p
    Q = suivi(nom)
    k = int(min(len(Q) - 1, max(0, (s0 + (t - a) * v) * FPS_R)))
    q = Q[k].copy()
    if mir:
        q[:, 0] = 1080 - q[:, 0]
        q = q[[1, 0, 3, 2]]
    return nom, k, mir, q


def pts(q):
    return [skia.Point(float(x), float(y)) for x, y in q]


def vers_quad(c, q, w, h):
    m = skia.Matrix()
    m.setPolyToPoly([skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)], pts(q))
    c.concat(m)


def haut_tel(q):
    return (q[0] + q[1]) / 2, float(np.linalg.norm(q[1] - q[0]))


def miroir(c, mir):
    if mir: c.translate(1080, 0); c.scale(-1, 1)


# ─────────────────────────────────────────── verre fumé
ST = [None]          # état du rush courant (le verre a besoin de l'image floutée de derrière)


def verre(c, x, y, w, h, r=34, voile=0.52, ombre=True, lisere=0.30):
    """panneau de verre fumé dans le repère courant (même en perspective) : rush flouté derrière,
    voile sombre, reflet, liseré clair"""
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    if ombre:
        p = skia.Paint(AntiAlias=True, Color=hexa("#05030A", 0.38), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
        c.save(); c.translate(0, 16); c.drawRRect(rr, p); c.restore()
    c.save(); c.clipRRect(rr, doAntiAlias=True)
    st = ST[0]
    if st is not None:
        nom, k, mir, q = st
        c.save(); c.resetMatrix(); miroir(c, mir)
        c.drawImageRect(fond_rush(nom, k, True), skia.Rect.MakeWH(1080, 1920), _ECH, skia.Paint())
        c.restore()
    else:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#2A2340"))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#0D0A16", voile))
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x + w * 0.35, y + h)],
                                               [hexa("#FFFFFF", 0.16), hexa("#FFFFFF", 0.03), hexa("#FFFFFF", 0.0)], [0.0, 0.45, 1.0]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), g)
    c.restore()
    bp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0)
    bp.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + h)],
                                                [hexa("#FFFFFF", lisere), hexa("#FFFFFF", lisere * 0.35)], [0.0, 1.0]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 1, y + 1, w - 2, h - 2), r - 1, r - 1), bp)


def pastille_verre(c, label, cx, cy, taille, rot, s, alpha, icone_=None, accent=None):
    if alpha <= 0.01: return
    tw = largeur(label, taille)
    ic = taille * 1.15 if icone_ else 0
    pad = taille * 0.75; h = taille * 2.1
    w = tw + 2 * pad + (ic + taille * 0.45 if icone_ else 0)
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        verre(c, -w / 2, -h / 2, w, h, h / 2, 0.48)
        x = -w / 2 + pad
        if icone_:
            disque(c, x + ic / 2, 0, ic * 0.78, accent or C["vert"])
            icone(c, icone_, x + ic / 2, 0, ic * 0.82, C["blanc"], 2.6)
            x += ic + taille * 0.45
        texte_centre(c, label, x + tw / 2, 0, taille, C["blanc"])
    c.restore()


def apparait(t, t0, s=1.9, d=0.34):
    return prog(t, t0, d, lambda v: rebond(v, s))


# ─────────────────────────────────────────── écran incrusté
SW, SH = 400, 900


def ecran_incruste(c, t, st, contenu, lueur="#FFFFFF", q=None):
    nom, k, mir, q0 = st
    q = q0 if q is None else q
    lp = skia.Path(); lp.addPoly(pts(q), True)
    p = skia.Paint(AntiAlias=True, Color=hexa(lueur, 0.26), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
    p.setBlendMode(skia.BlendMode.kScreen)
    c.drawPath(lp, p)
    c.saveLayer(None)
    c.save(); vers_quad(c, q, SW, SH)
    contenu(c, 0, 0, SW, SH)
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(SW, SH * 0.6)],
                                               [hexa("#FFFFFF", 0.12), hexa("#FFFFFF", 0.0), hexa("#FFFFFF", 0.04), hexa("#FFFFFF", 0.0)], [0.0, 0.35, 0.36, 0.6]))
    c.drawRect(skia.Rect.MakeWH(SW, SH), g)
    c.restore()
    # détourage du vert : doigts, pastille noire et cadre passent devant
    pm = skia.Paint(); pm.setBlendMode(skia.BlendMode.kDstIn)
    c.save(); miroir(c, mir)
    c.drawImageRect(masque_rush(nom, k), skia.Rect.MakeXYWH(0, -33.6, 1080, 736 * 2.7), _ECH, pm)
    c.restore()
    c.restore()


def dessine_rush(c, st):
    nom, k, mir, q = st
    c.save(); miroir(c, mir)
    c.drawImageRect(fond_rush(nom, k), skia.Rect.MakeWH(1080, 1920), _ECH, skia.Paint())
    c.restore()
    g = skia.Paint()
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 700)], [hexa("#0B0716", 0.6), hexa("#0B0716", 0.0)], [0.0, 1.0]))
    c.drawRect(skia.Rect.MakeWH(1080, 700), g)


# ─────────────────────────────────────────── panneaux qui sortent de l'écran
def plaque(cx, cy, w, h, rx=0.0, ry=0.0, rz=0.0):
    m = matrice3d(cx, cy, rx, ry, rz)
    return np.array([[p.x(), p.y()] for p in m.mapPoints([skia.Point(cx - w / 2, cy - h / 2), skia.Point(cx + w / 2, cy - h / 2),
                                                           skia.Point(cx + w / 2, cy + h / 2), skia.Point(cx - w / 2, cy + h / 2)])])


def emerge(c, t, ta, tb, qe, cible, PW, PH, dessin, d_in=0.42, d_out=0.26, retour=True, flotte=True):
    """le panneau part de l'écran (qe) et se pose sur `cible` ; à tb il y rentre"""
    if t < ta: return 0.0
    if tb is not None and t > tb + d_out: return 0.0
    u = prog(t, ta, d_in, lambda v: rebond(v, 1.12))
    q = qe + (cible - qe) * u
    if flotte: q = q + np.array([0.0, 7 * math.sin((t - ta) * 2.4)])
    al = borne(u * 4)
    if tb is not None and t > tb:
        w = prog(t, tb, d_out, entree)
        q = q + ((qe if retour else cible + np.array([0, -1400])) - q) * w
        al *= 1 - w * w
    c.save(); vers_quad(c, q, PW, PH)
    with Calque(c, al): dessin(c, PW, PH)
    c.restore()
    return u


# ─────────────────────────────────────────── contenus d'écran
CATALOGUE = [f"catalogue/c{k:02d}" for k in range(33)]


def image_contenue(cc, nom, a, b, d, e, zoom=1.0, fond="#FFFFFF"):
    cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture(fond))
    iw, ih = taille_img(nom)
    s_ = min(d / iw, e / ih) * 0.94 * zoom
    w_, h_ = iw * s_, ih * s_
    cc.save(); cc.clipRect(skia.Rect.MakeXYWH(a, b, d, e))
    image(cc, nom, a + (d - w_) / 2, b + (e - h_) / 2, w_)
    cc.restore()


def flash(cc, a, b, d, e, t, coupes, f0=0.75):
    for ct in coupes:
        f = 1 - (t - ct) / 0.1
        if 0 < f <= 1: cc.drawRect(skia.Rect.MakeXYWH(a, b, d, e), peinture("#FFFFFF", f0 * f))


def entete(c, x, y, w, titre=None):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 130), peinture(C["vert"]))
    texte(c, "9:41", x + 30, y + 22, 18, C["blanc"], "fort", track=0)
    if titre: texte(c, titre, x + 26, y + 70, 34, C["blanc"], "noir")
    else: image(c, "logo-dy-blanc", x + 24, y + 72, 190)


def ecran_catalogue(c, x, y, w, h, t, t0, vitesse=900):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#FFFFFF"))
    gap, col = 12, (w - 3 * 12) / 2
    defil = (t - t0) * vitesse
    hh = col + 46
    for k in range(60):
        r_, q = divmod(k, 2)
        yy = y + 144 + r_ * (hh + gap) - defil % ((hh + gap) * 12)
        if yy > y + h or yy + hh < y + 120: continue
        xx = x + gap + q * (col + gap)
        rrect(c, xx, yy, col, hh, 16, "#F6F4FB")
        image_contenue(c, CATALOGUE[(k * 7) % len(CATALOGUE)], xx + 6, yy + 6, col - 12, col - 12, 1.0, "#F6F4FB")
        rrect(c, xx + 10, yy + col + 4, col * 0.62, 10, 5, "#DCD6EA"); rrect(c, xx + 10, yy + col + 22, col * 0.36, 10, 5, C["vertMoyen"])
    entete(c, x, y, w)


def ecran_photo(cc, nom, a, b, d, e, t, t0, couv=False, fx=0.5, fy=0.5):
    z = 1.04 + 0.22 * max(0.0, t - t0)
    if couv: image_cover(cc, nom, a, b, d, e, z, fx, fy)
    else: image_contenue(cc, nom, a, b, d, e, z)


def ecran_discussion(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#F3F0FA"))
    msgs = [(TW(34) - 0.05, True, "img", 240), (TW(39) - 0.05, False, "qual", 150), (TW(42) - 0.05, False, "prix", 62)]
    yy = y + 150
    for t0, moi, ty, hb in msgs:
        if t < t0: continue
        u = prog(t, t0, 0.3, lambda v: rebond(v, 1.6))
        wb = w * 0.72
        xb = x + w - 14 - wb if moi else x + 14
        c.save(); c.translate(xb + wb / 2, yy + hb / 2); c.scale(mix(0.4, 1, u), mix(0.4, 1, u)); c.translate(-(xb + wb / 2), -(yy + hb / 2))
        with Calque(c, borne(u * 2)):
            rrect(c, xb, yy, wb, hb, 16, C["vert"] if moi else "#FFFFFF", 1.0, (2, 4, 0.12))
            if ty == "img": image_cover(c, "lv-noire", xb + 6, yy + 6, wb - 12, hb - 12, 1.0, 0.5, 0.72, rayon=12)
            elif ty == "qual":
                for j in range(3):
                    rrect(c, xb + 10, yy + 12 + j * 44, wb - 20, 36, 10, "#F4F1FB")
                    rrect(c, xb + 20, yy + 25 + j * 44, 70, 10, 5, "#CFC8E2")
                    for s_ in range(j + 1): c.drawPath(etoile(xb + wb - 30 - s_ * 20, yy + 30 + j * 44, 8), peinture("#F5B301"))
            else:
                texte(c, "Livraison incluse ✓", xb + 16, yy + 18, 21, C["ink"], "fort", track=0)
        c.restore()
        yy += hb + 12
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 130), peinture(C["vert"]))
    texte(c, "9:41", x + 30, y + 22, 18, C["blanc"], "fort", track=0)
    disque(c, x + 52, y + 92, 24, "#FFFFFF"); image(c, "logo-dy", x + 34, y + 88, 36)
    texte(c, "DROP&YOU", x + 86, y + 72, 24, C["blanc"], "noir", track=0)
    texte(c, "en ligne", x + 86, y + 100, 16, "#E4DAFF", "demi", track=0)


def ecran_livraison(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(C["vert"]))
    texte(c, "9:41", x + 30, y + 22, 18, C["blanc"], "fort", track=0)
    image(c, "logo-dy-blanc", x + 24, y + 72, 190)
    bob = 6 * math.sin(t * 8)
    icone(c, "truck", x + w / 2, y + h * 0.42 + bob, 170, C["blanc"], 2.2)
    texte_centre(c, "8 – 12 JOURS", x + w / 2, y + h * 0.62, 40, C["blanc"])
    rrect(c, x + 40, y + h * 0.70, w - 80, 14, 7, "#FFFFFF", 0.3)
    rrect(c, x + 40, y + h * 0.70, (w - 80) * (0.25 + 0.75 * borne((t - TW(47)) / 3.2)), 14, 7, "#FFFFFF")


def mix_coul(a, b, u):
    ca, cb = hexa(a), hexa(b)
    f = lambda s, d: int(round(s + (d - s) * borne(u)))
    r = lambda v, s: (v >> s) & 255
    return "#%02X%02X%02X" % (f(r(ca, 16), r(cb, 16)), f(r(ca, 8), r(cb, 8)), f(r(ca, 0), r(cb, 0)))


PAIE = [(TW(75) - 0.08, "PayPal"), (TW(76) - 0.08, "Virement"), (TW(78) - 0.08, "Carte")]


def ecran_paiement(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#FFFFFF"))
    entete(c, x, y, w, "Paiement")
    for j, (t0, lab) in enumerate(PAIE):
        yy = y + 170 + j * 112
        on = prog(t, t0, 0.25)
        rrect(c, x + 22, yy, w - 44, 92, 22, mix_coul("#F6F4FB", C["vertDoux"], on), 1.0, None, C["vert"] if on > 0.5 else "#E3DEEF", 3)
        texte(c, lab, x + 46, yy + 30, 28, C["ink"], "noir", track=0)
        disque(c, x + w - 64, yy + 46, 18, C["vert"] if on > 0.5 else "#DCD6EA")
        if on > 0.5: icone(c, "check", x + w - 64, yy + 46, 22, C["blanc"], 3.4)
    rrect(c, x + 22, y + h - 130, w - 44, 80, 40, C["vert"])
    texte_centre(c, "Payer", x + w / 2, y + h - 90, 30, C["blanc"])


def ecran_contact(c, x, y, w, h, t):
    """Snap puis WhatsApp dans l'écran"""
    if t < TW(86) - 0.06:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(MARQUES["snapchat"]))
        logo_app(c, "snapchat", x + w / 2, y + h * 0.36, 150, 1.0, None)
        texte_centre(c, "dropandyou1", x + w / 2, y + h * 0.56, 40, C["ink"])
        rrect(c, x + 60, y + h * 0.64, w - 120, 70, 35, C["ink"])
        texte_centre(c, "Ajouter", x + w / 2, y + h * 0.64 + 35, 30, C["blanc"])
    else:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(MARQUES["whatsapp"]))
        logo_glyphe(c, "whatsapp", x + w / 2, y + h * 0.40, 170, C["blanc"])
        texte_centre(c, "DROP&YOU", x + w / 2, y + h * 0.60, 40, C["blanc"])
        flash(c, x, y, w, h, t, [TW(86) - 0.06])


# ─────────────────────────────────────────── P1 · le hook : baskets qui jaillissent de l'écran
D3 = 1800.0
JAILLIT = [("hook/c22", -0.30, (-0.42, 0.10), 1), ("hook/c05", 0.10, (0.62, -0.25), -1), ("hook/c08", 0.42, (-0.6, -0.4), 1),
           ("hook/c11", 0.78, (0.5, 0.35), -1), ("hook/c09", 1.12, (-0.25, -0.75), 1), ("hook/c22", 1.55, (0.55, -0.5), -1),
           ("hook/c05", 2.05, (-0.55, 0.2), 1), ("hook/c08", 2.55, (0.4, -0.6), -1)]
VIE = 0.72


def basket_volante(c, nom, t, t0, direc, sens, cx, cy):
    u = (t - t0) / VIE
    if not (0 <= u <= 1): return
    v = sortie(u) * 0.35 + u ** 1.7 * 0.65
    X = direc[0] * 560 * v
    Y = direc[1] * 640 * v - 160 * math.sin(math.pi * min(1, u * 1.2))
    Z = -1560 * u ** 1.1
    f = D3 / (D3 + Z)
    x, y = cx + X * f, cy + Y * f
    w = 200 * f
    rot = sens * (-18 + 70 * u)
    al = borne(u / 0.06)
    iw, ih = taille_img(nom)
    c.save(); c.translate(x, y); c.rotate(rot)
    h_ = w * ih / iw
    om = skia.Paint(AntiAlias=True, ImageFilter=skia.ImageFilters.DropShadowOnly(0, 0.08 * w, 0.06 * w, 0.06 * w, skia.Color4f(0.05, 0.0, 0.15, 0.5 * al)))
    c.saveLayer(None, om); image(c, nom, -w / 2, -h_ / 2, w, al); c.restore()
    image(c, nom, -w / 2, -h_ / 2, w, al)
    c.restore()


T_BAS, T_FRI, T_ELE, T_MON, T_CATA = TW(15) - 0.05, TW(16) - 0.04, TW(17) - 0.04, TW(18) - 0.04, TW(19) - 0.06
CATS = [("BASKETS", T_BAS, -250, 150, -7, "sparkles"), ("FRINGUES", T_FRI, 255, 70, 6, "shirt"),
        ("ÉLECTRONIQUE", T_ELE, -235, 330, -5, "headphones"), ("MONTRES", T_MON, 250, 260, 6, "clock")]


def ecran_p1(cc, a, b, d, e, t):
    if t < T_BAS:
        ecran_catalogue(cc, a, b, d, e, t, -0.6)
        flash(cc, a, b, d, e, t, [n[1] for n in JAILLIT], 0.6)
    elif t < T_FRI:
        k = min(2, int((t - T_BAS) / 0.2))
        ecran_photo(cc, ["chanel-noire", "lv-noire", "catalogue/c12"][k], a, b, d, e, t, T_BAS + 0.2 * k, couv=k < 2, fy=0.6)
        flash(cc, a, b, d, e, t, [T_BAS, T_BAS + 0.2, T_BAS + 0.4])
    else:
        k = 0 if t < T_FRI + 0.22 else 1
        ecran_photo(cc, ["catalogue/c02", "catalogue/c26"][k], a, b, d, e, t, T_FRI)
        flash(cc, a, b, d, e, t, [T_FRI, T_FRI + 0.22])


def pastilles_cats(c, t, st):
    A, lw = haut_tel(st[3]); sc = st[3].mean(0)
    for lab, t0, dx, dy, rot, ic in CATS:
        if not (t0 - 0.06 <= t < TW(21) + 0.1): continue
        u = apparait(t, t0 - 0.06)
        w = prog(t, TW(21) - 0.12, 0.2, entree)
        x, y = mix(A[0] + dx, sc[0], w), mix(A[1] + dy, sc[1], w)
        pastille_verre(c, lab, x, y, 32, rot, mix(0.3, 1, u) * (1 - 0.7 * w), borne(u * 2) * (1 - w), ic)


def p1(c, t, st):
    q = st[3]; A, lw = haut_tel(q); sc = q.mean(0)
    ecran_incruste(c, t, st, lambda cc, a, b, d, e: ecran_p1(cc, a, b, d, e, t), C["vertMoyen"])
    for nom_, t0, direc, sens in JAILLIT: onde(c, sc[0], sc[1], t, t0, 60, 320, "#FFFFFF", 6, 0.45)
    for nom_, t0, direc, sens in JAILLIT: basket_volante(c, nom_, t, t0, direc, sens, sc[0], sc[1])
    sortie_ = 1 - prog(t, T_BAS - 0.2, 0.2, entree)
    if t >= TW(7) - 0.1 and sortie_ > 0:
        u = apparait(t, TW(7) - 0.1, 2.0, 0.32) * sortie_
        cx, cy = A[0] + 235, A[1] - 110
        with Espace(c, cx, cy, ry=-28 + 10 * math.sin(t * 3), rx=12, rz=8):
            c.save(); c.translate(cx, cy); c.scale(mix(0.2, 1, u), mix(0.2, 1, u))
            with Calque(c, borne(u * 2)):
                verre(c, -104, -72, 208, 144, 28, 0.35)
                drapeau(c, "CN", -82, -50, 164, 100, 14)
            c.restore()
    if t >= TW(10) - 0.12 and sortie_ > 0:
        u = apparait(t, TW(10) - 0.12) * sortie_
        pastille_verre(c, "AGENT SUR PLACE", A[0] - 150, A[1] - 120, 30, -6, mix(0.3, 1, u), borne(u * 2), "map-pin")
    pastilles_cats(c, t, st)


# ─────────────────────────────────────────── P2 · électronique, montres, le catalogue, « un modèle précis »
EVENTAIL = ["catalogue/c05", "catalogue/c11", "catalogue/c02", "catalogue/c22", "catalogue/c26", "catalogue/c09", "catalogue/c14"]
T_EV_FIN = TW(25) + 0.15
T_VISE = TW(29) - 0.1


def ecran_p2(cc, a, b, d, e, t):
    if t < T_MON:
        k = min(2, int((t - T_ELE) / 0.26))
        ecran_photo(cc, ["dyson-airwrap", "dyson-supersonic", "dyson-airstrait"][k], a, b, d, e, t, T_ELE + 0.26 * k, couv=True)
        flash(cc, a, b, d, e, t, [T_ELE, T_ELE + 0.26, T_ELE + 0.52])
    elif t < T_CATA:
        video(cc, "montres-bleues", a, b, d, e, t - T_MON + 1.0, 1.4)
        flash(cc, a, b, d, e, t, [T_MON])
    elif t < T_VISE:
        ecran_catalogue(cc, a, b, d, e, t, T_CATA, 1100)
        flash(cc, a, b, d, e, t, [T_CATA])
    else:
        ecran_photo(cc, "catalogue/c12", a, b, d, e, t, T_VISE - 0.4)
        u = prog(t, T_VISE, 0.35, lambda v: rebond(v, 1.8))
        if u > 0:
            cx, cy = a + d / 2, b + e / 2; r = 130 * mix(2.2, 1, u)
            for sx_, sy_ in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                trait(cc, cx + sx_ * r, cy + sy_ * r, cx + sx_ * r * 0.6, cy + sy_ * r, C["vert"], 9, borne(u * 2))
                trait(cc, cx + sx_ * r, cy + sy_ * r, cx + sx_ * r, cy + sy_ * r * 0.6, C["vert"], 9, borne(u * 2))
        flash(cc, a, b, d, e, t, [T_VISE])


def p2(c, t, st):
    q = st[3]; A, lw = haut_tel(q)
    ecran_incruste(c, t, st, lambda cc, a, b, d, e: ecran_p2(cc, a, b, d, e, t))
    pastilles_cats(c, t, st)
    n = len(EVENTAIL)
    for j, nom in enumerate(EVENTAIL):
        ang = (j - (n - 1) / 2) * 15
        cx = A[0] + math.sin(math.radians(ang)) * 450
        cy = A[1] + 280 - math.cos(math.radians(ang)) * 430 - 60
        def d(c_, W, H, nom=nom):
            verre(c_, 0, 0, W, H, 28, 0.45)
            rrect(c_, 10, 10, W - 20, W - 20, 20, "#FFFFFF")
            image_contenue(c_, nom, 14, 14, W - 28, W - 28)
            rrect(c_, 16, W + 2, W * 0.6, 12, 6, "#FFFFFF", 0.55); rrect(c_, 16, W + 22, W * 0.35, 12, 6, LILAS)
        emerge(c, t, TW(21) - 0.1 + 0.05 * abs(j - (n - 1) / 2), T_EV_FIN + 0.03 * j, q,
               plaque(cx, cy, 190, 240, rx=10, ry=ang * 1.4, rz=ang * 0.9), 190, 240, d, 0.4, 0.24)
    # « un modèle précis » : fiche en verre qui sort de l'écran
    def fiche(c_, W, H):
        verre(c_, 0, 0, W, H, 34, 0.5)
        rrect(c_, 16, 16, 150, 150, 22, "#FFFFFF"); image_contenue(c_, "catalogue/c12", 20, 20, 142, 142)
        texte(c_, "Modèle trouvé", 186, 34, 30, C["blanc"], "noir")
        pastille(c_, "Disponible", 186 + largeur("Disponible", 20, "noir") / 2 + 30, 116, 20, C["vert"], C["blanc"], "check")
    emerge(c, t, T_VISE + 0.05, PLANS[1][1] - 0.25, q, plaque(A[0], A[1] - 190, 520, 182, rx=10, rz=-3), 520, 182, fiche)


# ─────────────────────────────────────────── P3 · la fenêtre de discussion en verre : photo, qualités, prix
T_FEN = TW(31) - 0.02
FRAPPE = "Tu l’as en stock ?"
T_FRAPPE0, T_FRAPPE1 = TW(31) + 0.1, TW(33) + 0.05
T_ENVOI = TW(34) - 0.08


def fenetre_chat(c_, W, H, t):
    verre(c_, 0, 0, W, H, 40, 0.56)
    disque(c_, 58, 58, 30, "#FFFFFF"); image(c_, "logo-dy", 36, 53, 44)
    texte(c_, "DROP&YOU", 104, 32, 28, C["blanc"], "noir", track=0)
    disque(c_, 112, 80, 6, "#34D399"); texte(c_, "en ligne", 124, 68, 20, "#D8D2EA", "demi", track=0)
    trait(c_, 24, 108, W - 24, 108, "#FFFFFF", 1.5, 0.14)
    yy = 128
    if t >= T_ENVOI:
        u = prog(t, T_ENVOI, 0.3, lambda v: rebond(v, 1.5)); hb = 190; wb = 250
        c_.save(); c_.translate(W - 24 - wb, yy + hb); c_.scale(mix(0.5, 1, u), mix(0.5, 1, u)); c_.translate(-(W - 24 - wb), -(yy + hb))
        with Calque(c_, borne(u * 2)):
            rrect(c_, W - 24 - wb, yy, wb, hb, 22, C["vert"])
            image_cover(c_, "lv-noire", W - 24 - wb + 8, yy + 8, wb - 16, hb - 52, 1.0, 0.5, 0.72, rayon=16)
            texte(c_, FRAPPE, W - 24 - wb + 16, yy + hb - 38, 20, C["blanc"], "fort", track=0)
        c_.restore()
        yy += hb + 14
    if t >= TW(39) - 0.08:
        u = prog(t, TW(39) - 0.08, 0.3, lambda v: rebond(v, 1.5)); hb = 150; wb = 330
        with Calque(c_, borne(u * 2)):
            c_.save(); c_.translate(24, yy); c_.scale(mix(0.6, 1, u), mix(0.6, 1, u))
            rrect(c_, 0, 0, wb, hb, 22, "#FFFFFF", 0.14, None, "#FFFFFF", 1)
            for j in range(3):
                ul = prog(t, TW(39) + 0.08 * j, 0.25)
                with Calque(c_, ul):
                    texte(c_, f"Qualité {j + 1}", 18, 14 + j * 44, 24, C["blanc"], "fort", track=0)
                    for s_ in range(j + 1): c_.drawPath(etoile(wb - 30 - s_ * 26, 30 + j * 44, 11), peinture("#FBBF24"))
            c_.restore()
        yy += hb + 14
    if t >= TW(42) - 0.08:
        u = prog(t, TW(42) - 0.08, 0.3, lambda v: rebond(v, 1.5))
        lab = "Prix livraison incluse"
        wb = largeur(lab, 26, "noir", 0) + 90
        with Calque(c_, borne(u * 2)):
            c_.save(); c_.translate(24, yy); c_.scale(mix(0.6, 1, u), mix(0.6, 1, u))
            rrect(c_, 0, 0, wb, 64, 22, "#FFFFFF")
            icone(c_, "truck", 36, 32, 30, C["vert"], 2.4)
            texte(c_, lab, 62, 17, 26, C["ink"], "noir", track=0)
            c_.restore()
    # barre de saisie : le message s'écrit
    by = H - 92
    rrect(c_, 20, by, W - 40, 72, 36, "#FFFFFF", 0.10, None, "#FFFFFF", 1.5)
    icone(c_, "camera", 60, by + 36, 30, "#D8D2EA", 2.2)
    if T_FRAPPE0 <= t < T_ENVOI:
        n = int(len(FRAPPE) * borne((t - T_FRAPPE0) / (T_FRAPPE1 - T_FRAPPE0)))
        s = FRAPPE[:n]
        texte(c_, s, 92, by + 20, 28, C["blanc"], "demi", track=0)
        if int(t * 5) % 2 == 0: rrect(c_, 96 + largeur(s, 28, "demi", 0), by + 18, 3, 36, 1.5, LILAS)
    else:
        texte(c_, "Message", 92, by + 20, 28, "#9F98B8", "demi", track=0)
    ue = prog(t, T_ENVOI - 0.1, 0.2, lambda v: rebond(v, 2.0))
    disque(c_, W - 60, by + 36, 28, C["vert"]); icone(c_, "send" if ue > 0 else "mic", W - 62, by + 36, 28, C["blanc"], 2.4)


def p3(c, t, st):
    q = st[3]; A, lw = haut_tel(q)
    ecran_incruste(c, t, st, lambda cc, a, b, d, e: ecran_discussion(cc, a, b, d, e, t))
    emerge(c, t, T_FEN, PLANS[2][1] - 0.3, q, plaque(A[0] + 10, A[1] - 150, 640, 520, rx=9, ry=-6, rz=-1.5), 760, 620,
           lambda c_, W, H: fenetre_chat(c_, W, H, t), 0.5, 0.28)
    texte_centre(c, "Échange illustratif", 540, 1860, 22, C["blanc"], "fort", 0.8, 0.04)


# ─────────────────────────────────────────── P4 · le globe dans une bulle de verre, puis « pour toi ou pour revendre »
class GlobeVerre(Globe):
    COUL = {0: "#E2DAFF", 1: "#A78BFA", 2: "#FFFFFF", 3: "#FFFFFF", 4: "#EDE7FF"}


G = GlobeVerre()
GZ, PAR, BRU = (113.26, 23.13), (2.35, 48.86), (4.35, 50.85)
MONDE = [(-17.4, 14.7), (28.0, -26.2), (55.3, 25.2), (37.6, 55.75), (103.8, 1.35)]
T_GLOBE, T_GLOBE_FIN = TW(47) - 0.12, TW(62) - 0.2
T_TOI, T_REV, T_GROS = TW(63) - 0.1, TW(66) - 0.1, TW(68) - 0.1


def globe_flottant(c, t, st):
    q = st[3]; A, lw = haut_tel(q)
    if not (T_GLOBE <= t <= T_GLOBE_FIN + 0.3): return
    u = prog(t, T_GLOBE, 0.5, lambda v: rebond(v, 1.25))
    w = prog(t, T_GLOBE_FIN, 0.3, entree)
    e = u * (1 - w)
    if e <= 0.01: return
    sc = q.mean(0)
    cx, cy = mix(sc[0], 540, e), mix(sc[1], A[1] - 250, e) + 6 * math.sin(t * 2.2)
    R = 200 * e
    c.save()
    pth = skia.Path(); pth.addCircle(cx, cy, R * 1.08)
    sh = skia.Paint(AntiAlias=True, Color=hexa("#05030A", 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
    c.drawCircle(cx, cy + 18, R * 1.08, sh)
    c.clipPath(pth, doAntiAlias=True)
    nom, k, mir, _ = st
    c.save(); miroir(c, mir); c.drawImageRect(fond_rush(nom, k, True), skia.Rect.MakeWH(1080, 1920), _ECH, skia.Paint()); c.restore()
    c.drawCircle(cx, cy, R * 1.1, peinture("#0D0A16", 0.55))
    c.restore()
    anneau(c, cx, cy, R * 1.08, "#FFFFFF", 2, 0.3)
    lon0 = cles(t, [(T_GLOBE, 120), (TW(55), 35, entreeSortie), (TW(59), 45, entreeSortie)]); lat0 = cles(t, [(T_GLOBE, 28), (TW(55), 36, entreeSortie)])
    G.terres(c, cx, cy, R, lon0, lat0, grossir={1: 1.2, 3: 1.3})
    G.repere(c, *GZ, cx, cy, R, lon0, lat0, "CHINE", C["vert"], "CN", apparait(t, T_GLOBE + 0.2, 1.8, 0.4), 0.8, 60)
    pr = prog(t, TW(51) - 0.1, TW(54) - TW(51) + 0.1, entreeSortie)
    if pr > 0:
        G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, 1.0, "#FFFFFF", 4, 0.38)
        x_, y_, z_ = G.arc(c, GZ, PAR, cx, cy, R, lon0, lat0, pr, LILAS, 7, 0.38)
        if pr < 1 and z_ > 0: carton(c, x_, y_ - 16, 64, 0, 1.0, 8 * math.sin(t * 9))
    G.repere(c, *PAR, cx, cy, R, lon0, lat0, "FRANCE", C["ink"], "FR", apparait(t, TW(56) - 0.05, 1.8, 0.4), 0.8, 100)
    G.repere(c, *BRU, cx, cy, R, lon0, lat0, "BELGIQUE", C["ink"], "BE", apparait(t, TW(58) - 0.05, 1.8, 0.4), 0.8, 40)
    for k_, lieu in enumerate(MONDE):
        pm = prog(t, TW(60) + 0.08 * k_, 0.5, entreeSortie)
        if pm > 0:
            G.arc(c, GZ, lieu, cx, cy, R, lon0, lat0, pm, LILAS, 5, 0.3)
            if pm >= 1:
                x2, y2, z2 = G.pos(*lieu, lon0, lat0, R, cx, cy)
                if z2 > 0: disque(c, x2, y2, 8, LILAS); onde(c, x2, y2, t, TW(60) + 0.08 * k_ + 0.5, 8, 56, LILAS, 4)


def carte_profil(c_, W, H, t, titre, sous, ic, img, t_check):
    verre(c_, 0, 0, W, H, 34, 0.5)
    rrect(c_, W / 2 - 78, 26, 156, 156, 78, "#FFFFFF")
    KM._cercle_image(c_, img, W / 2, 104, 72, 1.2)
    texte_centre(c_, titre, W / 2, 222, ajuste(titre, W - 40, 38), C["blanc"], "noir")
    pastille(c_, sous, W / 2, 278, 21, C["vert"], C["blanc"], ic)
    uc = apparait(t, t_check, 2.0, 0.3)
    if uc > 0:
        c_.save(); c_.translate(W - 40, 40); c_.scale(uc, uc); disque(c_, 0, 0, 32, "#34D399", 1.0, (8, 20, 0.2)); icone(c_, "check", 0, 0, 38, C["blanc"], 3.6); c_.restore()


PROFILS = [("Pour toi", "Acheteur", "shirt", "catalogue/c02", -215, -200, 20), ("Revendeur", "En quantité", "store", "carton-gros", 215, -165, -20)]
T_DEUX = TW(72) - 0.08


def p4(c, t, st):
    q = st[3]; A, lw = haut_tel(q)
    def ecran(cc, a, b, d, e):
        if t < T_GLOBE_FIN: ecran_livraison(cc, a, b, d, e, t)
        elif t < T_GROS:
            ecran_photo(cc, "catalogue/c02", a, b, d, e, t, T_GLOBE_FIN); flash(cc, a, b, d, e, t, [T_GLOBE_FIN])
        else:
            ecran_photo(cc, "carton-gros", a, b, d, e, t, T_GROS, couv=True); flash(cc, a, b, d, e, t, [T_GROS])
    ecran_incruste(c, t, st, ecran, C["vertMoyen"])
    sc = q.mean(0)
    onde(c, sc[0], sc[1], t, T_GLOBE, 30, 220, "#FFFFFF", 6, 0.5)
    globe_flottant(c, t, st)
    if TW(48) - 0.1 <= t < T_GLOBE_FIN + 0.2:
        u = apparait(t, TW(48) - 0.1) * (1 - prog(t, T_GLOBE_FIN, 0.2, entree))
        pastille_verre(c, "8 À 12 JOURS", A[0] - 245, A[1] + 140, 32, -6, mix(0.3, 1, u), borne(u * 2), "calendar")
    if TW(60) - 0.1 <= t < T_GLOBE_FIN + 0.2:
        u = apparait(t, TW(60) - 0.1) * (1 - prog(t, T_GLOBE_FIN, 0.2, entree))
        pastille_verre(c, "PARTOUT", A[0] + 250, A[1] + 250, 32, 5, mix(0.3, 1, u), borne(u * 2), "globe")
    for titre, sous, ic, img, dx, dy, ry in PROFILS:
        t0 = T_TOI if titre == "Pour toi" else T_REV
        emerge(c, t, t0, None, q, plaque(A[0] + dx, A[1] + dy, 300, 310, rx=8, ry=ry, rz=-ry * 0.25), 320, 330,
               lambda c_, W, H, a=(titre, sous, ic, img): carte_profil(c_, W, H, t, *a, 99))
    tampon(c, "EN GROS", A[0] + 40, A[1] + 340, t, TW(68), 60, C["rouge"], 7, "package")


# ─────────────────────────────────────────── P5 · « on gère les deux », paiement, Snap, WhatsApp
PSEUDO = "dropandyou1"
T_PSEUDO = [TW(82) + k * (TW(85) + 0.2 - TW(82)) / len(PSEUDO) for k in range(len(PSEUDO))]
T_P5 = PLANS[4][0]


def logo_paypal(c, x, y, taille):
    w1 = largeur("Pay", taille, "noir", -0.02)
    texte(c, "Pay", x, y, taille, "#FFFFFF", "noir", track=-0.02)
    texte(c, "Pal", x + w1, y, taille, "#7DD3FC", "noir", track=-0.02)


def p5(c, t, st):
    q = st[3]; A, lw = haut_tel(q)
    def ecran(cc, a, b, d, e):
        if t < TW(73) - 0.1: ecran_photo(cc, "carton-gros", a, b, d, e, t, T_GROS, couv=True)
        elif t < TW(79) - 0.1: ecran_paiement(cc, a, b, d, e, t); flash(cc, a, b, d, e, t, [TW(73) - 0.1])
        else: ecran_contact(cc, a, b, d, e, t); flash(cc, a, b, d, e, t, [TW(79) - 0.1])
    if t < T_DIVE: ecran_incruste(c, t, st, ecran)
    for titre, sous, ic, img, dx, dy, ry in PROFILS:
        emerge(c, t, T_P5 - 0.02, TW(73) - 0.25, q, plaque(A[0] + dx, A[1] + dy, 300, 310, rx=8, ry=ry, rz=-ry * 0.25), 320, 330,
               lambda c_, W, H, a=(titre, sous, ic, img): carte_profil(c_, W, H, t, *a, T_DEUX + (0.1 if a[0] != "Pour toi" else 0)), 0.01, 0.24)
    for k, (t0, lab) in enumerate(PAIE):
        def d(c_, W, H, lab=lab, ic=[None, "landmark", "credit-card"][k], t0=t0):
            verre(c_, 0, 0, W, H, 30, 0.5)
            rrect(c_, 16, 16, H - 32, H - 32, 22, "#FFFFFF", 0.12)
            if ic is None:
                texte_centre(c_, "P", 16 + (H - 32) / 2, H / 2, 50, "#7DD3FC", "noir")
                logo_paypal(c_, H + 4, H / 2 - hauteurLigne(42) / 2, 42)
            else:
                icone(c_, ic, 16 + (H - 32) / 2, H / 2, 50, LILAS, 2.3)
                texte(c_, lab, H + 4, H / 2 - hauteurLigne(40) / 2, 40, C["blanc"], "noir")
            uc = apparait(t, t0 + 0.2, 2.0, 0.3)
            if uc > 0:
                c_.save(); c_.translate(W - 46, H / 2); c_.scale(uc, uc); disque(c_, 0, 0, 28, "#34D399"); icone(c_, "check", 0, 0, 34, C["blanc"], 3.6); c_.restore()
        emerge(c, t, t0 - 0.06, TW(79) - 0.3, q, plaque(A[0] + (k - 1) * 60, A[1] - 395 + k * 132, 480, 108, rx=14, ry=(1 - k) * 8, rz=(k - 1) * 3), 480, 108, d, 0.4, 0.22)
    def snap(c_, W, H):
        verre(c_, 0, 0, W, H, 38, 0.5)
        rrect(c_, 22, 22, 116, 116, 30, MARQUES["snapchat"]); logo_app(c_, "snapchat", 80, 80, 92, 1.0, None)
        texte(c_, "Snapchat", 160, 30, 24, "#D8D2EA", "fort", track=0)
        xl = 160
        for k, l in enumerate(PSEUDO):
            if t >= T_PSEUDO[k]:
                ul = prog(t, T_PSEUDO[k], 0.1, sortie)
                texte(c_, l, xl, 64 - 8 * (1 - ul), 50, C["blanc"], "noir", alpha=ul, track=-0.01)
                xl += largeur(l, 50, "noir", -0.01)
        if TW(82) - 0.1 <= t < TW(85) + 0.4 and int(t * 5) % 2 == 0: rrect(c_, xl + 4, 66, 4, 50, 2, MARQUES["snapchat"])
        ub = apparait(t, TW(85) + 0.2, 2.0, 0.3)
        if ub > 0:
            c_.save(); c_.translate(W / 2, H - 50); c_.scale(ub, ub)
            rrect(c_, -W / 2 + 22, -30, W - 44, 60, 30, MARQUES["snapchat"]); texte_centre(c_, "Ajouter", 0, 0, 28, C["ink"])
            c_.restore()
    emerge(c, t, TW(79) - 0.12, T_DIVE - 0.12, q, plaque(A[0], A[1] - 300, 600, 240, rx=12, rz=-3), 600, 240, snap, 0.42, 0.22)
    def wa(c_, W, H):
        verre(c_, 0, 0, W, H, H / 2, 0.45)
        disque(c_, H / 2, H / 2, H / 2 - 12, MARQUES["whatsapp"]); logo_glyphe(c_, "whatsapp", H / 2, H / 2, 50, C["blanc"])
        texte(c_, "Écris-nous sur WhatsApp", H + 6, H / 2 - hauteurLigne(34) / 2, 34, C["blanc"], "noir", track=0)
    emerge(c, t, TW(87) - 0.12, T_DIVE - 0.12, q, plaque(A[0], A[1] - 40, 560, 104, rx=10, rz=2), 560, 104, wa, 0.4, 0.22)


# ─────────────────────────────────────────── S8 · ChinaBook (motion pur, comme DY-M01) et fin
T_FIN = TW(104) + 0.62
S8 = (T_DIVE + 0.2, T_FIN)
T_LOGO = TW(103) - 0.15


def tel(c, cx, cy, ecran, w=480, h=960, alpha=1.0, **espace):
    with Espace(c, cx, cy, **espace):
        telephone(c, cx - w / 2, cy - h / 2, w, h, ecran, alpha)


def s8_contenu(c, t):
    fond(c, t)
    e = prog(t, T_DIVE + 0.1, 0.45, sortie)
    lignes = [dict(t=TW(92), image="catalogue/c12", nom="Baskets", ville="Guangzhou"),
              dict(t=TW(94) - 0.05, image="dyson-supersonic", nom="Électronique", ville="Shenzhen", zoom=1.6, fy=0.4),
              dict(t=TW(97) - 0.05, image="chanel-noire", nom="Luxe", ville="Guangzhou", fy=0.55)]
    tel(c, 540, 1144, lambda cc, a, b, d, e_: ecran_contacts(cc, a, b, d, e_, t, lignes), ry=mix(-30, -4, e) + 2 * math.sin(t * 2.2), s=mix(0.6, 1, e), alpha=borne(e * 2))
    if t >= TW(98) - 0.1:
        u = apparait(t, TW(98) - 0.1)
        pastille_rot(c, "COMME MOI", 300, 700, 38, C["ink"], C["blanc"], -6, mix(0.3, 1, u), borne(u * 2), "user", (14, 32, 0.22))
    tampon(c, "EN DIRECT", 790, 760, t, TW(97), 58, C["vert"], -8, "zap")
    confettis(c, 790, 760, t, TW(97) + 0.04, 22, 320, 9)


def disque_logo(c, t):
    r = cles(t, [(T_LOGO, 0), (T_LOGO + 0.28, 1750, entree), (T_FIN - 0.1, 1750), (T_FIN + 0.3, 0, entreeSortie)])
    if r > 1:
        disque(c, 540, 1080, r, C["vert"])
        if T_LOGO + 0.2 <= t <= T_FIN + 0.1:
            u = prog(t, T_LOGO + 0.24, 0.3, lambda v: rebond(v, 1.5)); so = prog(t, T_FIN - 0.15, 0.25, entree)
            lw = mix(1.5, 1, u) * 780 * (1 - 0.3 * so)
            image(c, "logo-tout-blanc", 540 - lw / 2, 1000 - lw * 0.2167 / 2, lw, borne(u * 3) * (1 - so))
    return r


def carton_final(c, t):
    if t < T_FIN + 0.05: return
    u = prog(t, T_FIN + 0.05, 0.4, sortie)
    disque(c, 540, 1060, 420 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
    ul = prog(t, T_FIN + 0.12, 0.36, lambda v: rebond(v, 1.6))
    lw = 760 * mix(0.6, 1, ul)
    iw_, ih_ = taille_img("logo"); lh = lw * ih_ / iw_
    image(c, "logo", 540 - lw / 2, 960 - lh / 2, lw, borne(ul * 2))
    ub = prog(t, T_FIN + 0.36, 0.36, lambda v: rebond(v, 1.8))
    etincelles(c, 540, 1170, t, T_FIN + 0.5, 12, 380)
    if ub > 0:
        s = mix(0.4, 1, ub) * (1 + 0.035 * max(0, math.sin((t - T_FIN - 0.8) * 5)) if t > T_FIN + 0.8 else 1)
        lab = "Envoie « CHINA » sur WhatsApp"
        tw = largeur(lab, 40); wb, hb = tw + 150, 116
        c.save(); c.translate(540, 1170); c.scale(s, s)
        with Calque(c, borne(ub * 2)):
            rrect(c, -wb / 2, -hb / 2, wb, hb, hb / 2, MARQUES["whatsapp"], 1.0, (18, 46, 0.3))
            logo_glyphe(c, "whatsapp", -wb / 2 + 70, 0, 56, C["blanc"])
            texte_centre(c, lab, -wb / 2 + 118 + tw / 2, 0, 40, C["blanc"])
        c.restore()
    ud = prog(t, T_FIN + 0.6, 0.4, sortie)
    if ud > 0:
        texte_centre(c, "proposé par", 540, 1380, 26, C["gris"], "fort", ud, 0.04)
        image(c, "logo-dy", 540 - 160, 1410, 320, ud)


def bandeau_dy(c, t, alpha, blanc):
    if alpha <= 0: return
    with Calque(c, alpha):
        image(c, "logo-dy-blanc" if blanc else "logo-dy", 86, 150, 200)
        lab = "TON AGENT EN CHINE"
        w = largeur(lab, 20, "fort", 0.12)
        texte(c, lab, 990, 158, 20, C["blanc"] if blanc else C["gris"], "fort", "droite", 0.12)
        disque(c, 990 - w - 20, 170, 6, C["vertMoyen"] if blanc else C["vert"], 0.35 + 0.65 * (0.5 + 0.5 * math.cos(t * 4)))


# ─────────────────────────────────────────── la vue subjective
def pov(c, t):
    st = etat(t)
    if st is None: return
    ST[0] = st
    dessine_rush(c, st)
    p = plan_a(max(0.0, t))
    if p is PLANS[0]: p1(c, t, st)
    elif p is PLANS[1]: p2(c, t, st)
    elif p is PLANS[2]: p3(c, t, st)
    elif p is PLANS[3]: p4(c, t, st)
    else:
        u = prog(t, T_DIVE, 0.36, entreeSortie)
        if u > 0:
            # plongée : l'écran grandit jusqu'à remplir le cadre, on entre dans le ChinaBook
            plein = np.array([[0, 0], [1080, 0], [1080, 1920], [0, 1920]], float)
            qd = st[3] + (plein - st[3]) * u
            def dedans(cc, a, b, d, e):
                cc.save(); cc.scale(d / 1080, e / 1920); C.update(VERT); s8_contenu(cc, t); C.update(VIOLET); cc.restore()
            ecran_incruste(c, t, st, dedans, C["blanc"], qd)
            if u > 0.55:
                with Calque(c, borne((u - 0.55) / 0.3)):
                    c.save(); vers_quad(c, qd, SW, SH); c.scale(SW / 1080, SH / 1920); C.update(VERT); s8_contenu(c, t); C.update(VIOLET); c.restore()
        p5(c, t, st)
    ST[0] = None


# ─────────────────────────────────────────── sons, flou, éclairs
son(0.0, "impact", -5); son(0.0, "whoosh_court", -12)
for _n, _t0, _d, _s in JAILLIT:
    if _t0 > 0: son(_t0, "whoosh_court", -12); son(_t0 + 0.02, "pop", -15)
son(TW(7) - 0.1, "pop", -11); son(TW(10) - 0.12, "pop", -11)
for _, t0, *_ in CATS: son(t0, "clic", -10); son(t0 + 0.01, "swipe", -17); son(t0 + 0.02, "pop", -13)
for t0 in (T_BAS + 0.2, T_BAS + 0.4, T_FRI + 0.22, T_ELE + 0.26, T_ELE + 0.52): son(t0, "clic", -13)
son(T_CATA, "clic", -10); son(TW(21) - 0.1, "whoosh_long", -13)
for j in range(len(EVENTAIL)): son(TW(21) - 0.05 + 0.04 * j, "pop", -18)
son(T_EV_FIN, "whoosh", -14); son(T_VISE, "blip", -11); son(T_VISE + 0.05, "whoosh_court", -13)
son(PLANS[2][0], "whoosh", -12); son(T_FEN, "whoosh_long", -13)
for k_ in range(len(FRAPPE)): son(T_FRAPPE0 + k_ * (T_FRAPPE1 - T_FRAPPE0) / len(FRAPPE), "frappe", -17)
son(T_ENVOI, "message", -10); son(TW(39) - 0.08, "message_in", -11); son(TW(42) - 0.08, "message_in", -11)
son(PLANS[3][0], "whoosh", -12); son(T_GLOBE, "clic", -9); son(T_GLOBE, "whoosh_long", -13)
son(TW(48) - 0.1, "pop", -10); son(TW(54), "ding", -12); son(TW(56) - 0.05, "pop", -11); son(TW(58) - 0.05, "pop", -11)
for k in range(5): son(TW(60) + 0.08 * k, "blip", -15)
son(TW(60) - 0.1, "pop", -11); son(T_GLOBE_FIN, "whoosh", -13)
son(T_TOI, "whoosh_court", -13); son(T_REV, "whoosh_court", -13); son(TW(68) - 0.1, "tampon", -7); son(TW(68) - 0.08, "impact", -9)
son(PLANS[4][0], "whoosh", -12); son(T_DEUX, "check", -12); son(T_DEUX + 0.1, "check", -12)
son(TW(73) - 0.1, "clic", -11)
for t0, _ in PAIE: son(t0 - 0.06, "whoosh_court", -14); son(t0 + 0.2, "check", -12)
son(TW(79) - 0.12, "whoosh_court", -12); son(TW(79) - 0.1, "clic", -11)
for tl in T_PSEUDO: son(tl, "frappe", -15)
son(TW(85) + 0.2, "pop", -12); son(TW(87) - 0.12, "pop", -10); son(TW(88), "message", -12)
son(T_DIVE, "whoosh_long", -10); son(T_DIVE + 0.3, "impact_doux", -9)
son(TW(98) - 0.1, "pop", -11); son(TW(92), "pop", -12); son(TW(94) - 0.05, "pop", -12); son(TW(97) - 0.05, "pop", -12); son(TW(97) - 0.1, "tampon", -9); son(TW(97) + 0.04, "ching", -11)
son(T_LOGO - 0.1, "montee", -15); son(T_LOGO + 0.24, "impact", -7); son(T_LOGO + 0.26, "verre", -9)
son(T_FIN, "whoosh", -13); son(T_FIN + 0.14, "impact_doux", -8); son(T_FIN + 0.16, "verre", -8); son(T_FIN + 0.36, "pop", -11)

for a, b in [(0.0, 1.0), (T_CATA - 0.02, T_CATA + 0.1), (TW(21) - 0.1, TW(21) + 0.35), (T_EV_FIN, T_EV_FIN + 0.3), (T_VISE + 0.05, T_VISE + 0.4),
             (T_FEN, T_FEN + 0.45), (T_ENVOI - 0.05, T_ENVOI + 0.25), (TW(46) - 0.2, TW(46) + 0.05), (PLANS[2][1] - 0.3, PLANS[2][1] + 0.05),
             (T_GLOBE, T_GLOBE + 0.4), (T_GLOBE_FIN, T_GLOBE_FIN + 0.3), (T_TOI, T_TOI + 0.3), (T_REV, T_REV + 0.3), (TW(68) - 0.2, TW(68) + 0.05),
             (PAIE[0][0] - 0.1, PAIE[0][0] + 0.25), (PAIE[1][0] - 0.1, PAIE[1][0] + 0.25), (PAIE[2][0] - 0.1, PAIE[2][0] + 0.25),
             (TW(79) - 0.35, TW(79) + 0.3), (TW(87) - 0.15, TW(87) + 0.25), (T_DIVE - 0.12, T_DIVE + 0.4), (T_LOGO, T_LOGO + 0.4), (T_FIN, T_FIN + 0.36)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, "#7C3AED", 0.12), (TW(42), "#7C3AED", 0.07), (TW(68) - 0.08, C["rouge"], 0.10),
                    (T_DIVE + 0.3, C["blanc"], 0.25), (TW(88), "#25D366", 0.08), (TW(97), "#00B862", 0.10), (T_LOGO + 0.24, C["blanc"], 0.15), (T_FIN + 0.14, "#00B862", 0.10)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    en_pov = t < T_POV
    blanc = en_pov and t < T_DIVE + 0.2
    C.update(VIOLET if (t < T_CB or blanc) else VERT)
    if not en_pov:
        fond(c, t)
        if S8[0] <= t <= S8[1]: s8_contenu(c, t)
    else:
        pov(c, t)
    r = disque_logo(c, t)
    a = borne(prog(t, 0.15, 0.3) * (1 - prog(t, T_LOGO, 0.2)))
    if t < T_CB or blanc: bandeau_dy(c, t, a, blanc)
    else: bandeau(c, t, a)
    carton_final(c, t)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if (r > 900 or blanc) else C["ink"])
