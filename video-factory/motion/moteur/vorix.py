"""VORIX — shaker électrique, client Mikail (VX-M01, 29/10/2026).

Le client n'a pas de packshot : il n'a que des vidéos filmées dans son évier. Le produit est donc
reconstruit en 3D, aux cotes réelles relevées sur la boîte (209 × 83 mm, 500 ml, 323 g) :
base moteur noire à ergots, corps transparent habillé d'un manchon noir siglé, deux fenêtres de
niveau opposées, bague filetée, hélice démontable.

Le cylindre est un ruban de bandes verticales projetées une à une (studio3d.Plan) : chaque bande
porte sa propre teinte selon l'angle de sa normale, ce qui donne le galbe, le liseré spéculaire et
la retombée d'ombre sans aucun moteur d'éclairage. Les faces arrière ne sont pas éliminées pour le
verre — c'est leur empilement qui fait la transparence.
"""
import functools
import math
import skia
import moteur
from moteur import *
from studio3d import Cam, Plan, coins, scene3d, rot3, FOC

# ─────────────────────────────────────────── palette
NOIR = "#101317"          # corps du manchon, dans l'ombre
NOIR_H = "#454E59"        # le même, sous la lumière
GRAPHITE = "#1B2027"
VERRE = "#9FB4C8"         # teinte du Tritan
BLANC = "#FFFFFF"
ENCRE = "#161B22"         # l'encre du logo imprimé
ACIER = "#C7D2DD"
FOND = "#07090C"

SYMBOLE = "vorix-symbole"  # media/vorix-symbole.png — blanc sur alpha, extrait de la boîte

# matière du corps en Tritan ; une scène sur fond clair la remplace (CORPS.update(...)) : sur du blanc, les teintes
# claires qui faisaient le verre sur fond noir le rendent laiteux (VX-M01 v4, 30/10/2026)
CORPS = dict(bas="#1A232E", haut="#C2D6E8", alpha=0.62, spec=1.0, contre=0.75)

# lumière : trois quarts avant-gauche, plus un contre-jour froid à droite
A_LUM = math.radians(-152)
A_SPEC = math.radians(-124)
A_CONTRE = math.radians(-28)


@functools.lru_cache(maxsize=8192)
def _teinte(bas, haut, u):
    """mélange deux couleurs hexa et renvoie une chaîne hexa"""
    u = round(u * 256) / 256
    b = [int(bas.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    h = [int(haut.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(int(borne(b[i] + (h[i] - b[i]) * u, 0, 255)) for i in range(3))


@functools.lru_cache(maxsize=16384)
def eclaire(a, bas, haut, spec=0.85, dur=26, contre=0.30):
    """luminosité d'une bande de cylindre dont la normale pointe vers l'angle `a`"""
    a = round(a * 512) / 512
    d = max(0.0, math.cos(a - A_LUM))
    k = 0.10 + 0.90 * d ** 1.25
    c = max(0.0, math.cos(a - A_CONTRE)) ** 3
    k = borne(k + contre * c)
    col = _teinte(bas, haut, k)
    s = spec * max(0.0, math.cos(a - A_SPEC)) ** dur
    return _teinte(col, BLANC, borne(s))


def fresnel(a, base=0.16, pic=0.92, dur=2.2):
    """opacité d'une paroi de verre : transparente de face, dense en incidence rasante"""
    f = (1.0 - abs(math.sin(a))) ** dur
    return base + (pic - base) * f


def _quad(r, a0, a1, y0, y1):
    """les 4 coins (HG, HD, BD, BG) d'une bande de cylindre entre deux angles"""
    return [(r * math.cos(a0), y0, r * math.sin(a0)),
            (r * math.cos(a1), y0, r * math.sin(a1)),
            (r * math.cos(a1), y1, r * math.sin(a1)),
            (r * math.cos(a0), y1, r * math.sin(a0))]


def _pose(pts, centre, ax=0.0, ay=0.0, az=0.0):
    cx, cy, cz = centre
    out = []
    for p in pts:
        x, y, z = rot3(p, ax, ay, az)
        out.append((x + cx, y + cy, z + cz))
    return out


def _pente(a, pente):
    """décalage vertical de l'arête haute : 0 au point bas, -amplitude au point haut (angle `pente[0]`)"""
    if not pente: return 0.0
    ang, amp = pente
    return -amp * (0.5 + 0.5 * math.cos(a - ang))


def cylindre(centre, r, h, bas, haut, n=56, rot=0.0, ax=0.0, alpha=1.0,
             spec=0.85, dur=26, contre=0.30, recto=True, decor=None, r2=None, verre=False, pente=None):
    """un cylindre (ou tronc de cône si r2) en bandes verticales ; `verre` applique le Fresnel par bande ;
    `pente` incline l'arête du haut (le dessus d'un couvercle qui monte vers la charnière)"""
    plans = []
    r2 = r if r2 is None else r2
    for i in range(n):
        a0 = rot + 2 * math.pi * i / n
        a1 = rot + 2 * math.pi * (i + 1) / n
        am = (a0 + a1) / 2
        p0 = _quad(r, a0, a1, -h / 2, -h / 2)
        if pente:
            p0 = [(p0[0][0], p0[0][1] + _pente(a0, pente), p0[0][2]), (p0[1][0], p0[1][1] + _pente(a1, pente), p0[1][2]), p0[2], p0[3]]
        p1 = _quad(r2, a0, a1, h / 2, h / 2)
        pts = _pose([p0[0], p0[1], p1[2], p1[3]], centre, ax=ax)
        col = eclaire(am, bas, haut, spec, dur, contre)
        a = alpha * fresnel(am) if verre else alpha

        def dessin(c, w, hh, col=col, am=am):
            c.drawRect(skia.Rect.MakeWH(w + 1.2, hh), peinture(col))
            if decor: decor(c, w, hh, am)
        plans.append(Plan(pts, 46, max(10.0, abs(h)), dessin, a, recto))
    return plans


def disque(centre, r, couleur, n=56, ax=0.0, alpha=1.0, creux=0.0, pente=None):
    """un disque plein, vu comme un éventail de triangles aplatis en bandes fines ; `pente` l'incline"""
    plans = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 1) / n
        ri = r * creux
        yc = _pente(0.0, pente) / 2 if pente else 0.0       # le centre du disque incliné est à mi-pente
        p = [(ri * math.cos(a0), yc, ri * math.sin(a0)), (ri * math.cos(a1), yc, ri * math.sin(a1)),
             (r * math.cos(a1), _pente(a1, pente), r * math.sin(a1)), (r * math.cos(a0), _pente(a0, pente), r * math.sin(a0))]
        pts = _pose(p, centre, ax=ax)
        col = _teinte(couleur, BLANC, 0.10 + 0.14 * max(0.0, math.cos((a0 + a1) / 2 - A_LUM)))

        def dessin(c, w, hh, col=col):
            c.drawRect(skia.Rect.MakeWH(w + 1.2, hh + 1.2), peinture(col))
        plans.append(Plan(pts, 46, 46, dessin, alpha, False))
    return plans


def manchon(centre, r, h, rot=0.0, ax=0.0, alpha=1.0, theta=0.72, hf=0.80, rc=0.09, n=96,
            bas="#0A0D11", haut="#30373F"):
    """la coque noire du corps, percée de deux fenêtres opposées à coins arrondis (photos du client, 30/10/2026 :
    « une vitre en plastique avec les contours noirs autour »). theta : demi-ouverture angulaire d'une fenêtre ;
    hf : hauteur de la fenêtre en part de h ; rc : rayon des coins en part de h. La fenêtre avant est centrée
    sur le logo (angle rot − π/2), l'arrière à l'opposé."""
    plans = []
    hw = h * hf; rcp = h * rc
    for i in range(n):
        a0 = rot + 2 * math.pi * i / n
        a1 = rot + 2 * math.pi * (i + 1) / n
        am = (a0 + a1) / 2
        # distance angulaire au centre de la fenêtre la plus proche
        d = min(abs((am - (rot - math.pi / 2) + math.pi) % (2 * math.pi) - math.pi),
                abs((am - (rot + math.pi / 2) + math.pi) % (2 * math.pi) - math.pi))
        s_arc = d * r; sw = theta * r
        col = eclaire(am, bas, haut, 0.45, 40, 0.30)

        def dessin(c, w, hh, col=col):
            c.drawRect(skia.Rect.MakeWH(w + 1.2, hh + 1.2), peinture(col))
        if s_arc >= sw:
            segs = [(-h / 2, h / 2)]
        else:
            dy = rcp - math.sqrt(max(0.0, rcp * rcp - (s_arc - (sw - rcp)) ** 2)) if s_arc > sw - rcp else 0.0
            segs = [(-h / 2, -hw / 2 + dy), (hw / 2 - dy, h / 2)]
        for y0, y1 in segs:
            if y1 - y0 < 0.5: continue
            pts = _pose(_quad(r, a0, a1, y0, y1), centre, ax=ax)
            plans.append(Plan(pts, 46, max(10.0, y1 - y0), dessin, alpha, True))
    return plans


# ─────────────────────────────────────────── le logo
def symbole(c, cx, cy, w, couleur=BLANC, alpha=1.0):
    """le V de VORIX, extrait de la boîte du client (PNG blanc sur alpha), teinté"""
    i = moteur._img(SYMBOLE)
    h = w * i.height() / i.width()
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(skia.ColorFilters.Blend(hexa(couleur, 1.0), skia.BlendMode.kSrcIn))
    if alpha < 1: p.setAlphaf(borne(alpha))
    c.drawImageRect(i, skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), moteur._ECH, p)


def mot(c, cx, cy, taille, couleur=BLANC, alpha=1.0, track=0.30):
    """VORIX — capitales géométriques très espacées, comme sur la boîte ; cy = milieu du mot"""
    texte(c, "VORIX", cx + taille * track / 2, cy - taille * 0.70, taille, couleur, "noir",
          align="centre", track=track, alpha=alpha)


def baseline(c, cx, cy, taille, couleur=BLANC, alpha=1.0):
    """— TRAIN. FUEL. PERFORM. — avec ses deux filets ; cy = milieu de la ligne"""
    t = "TRAIN.  FUEL.  PERFORM."
    l = largeur(t, taille, "noir", 0.34)
    texte(c, t, cx + taille * 0.17, cy - taille * 0.70, taille, couleur, "noir",
          align="centre", track=0.34, alpha=alpha)
    for s in (-1, 1):
        x = cx + s * (l / 2 + taille * 1.9)
        trait(c, x - taille * 0.9, cy, x + taille * 0.9, cy, couleur, max(1.6, taille * 0.09), alpha)


def logo(c, cx, cy, w, couleur=BLANC, alpha=1.0, avec_baseline=True):
    """le bloc complet : symbole, VORIX, baseline — proportions de la boîte"""
    symbole(c, cx, cy - w * 0.20, w * 0.52, couleur, alpha)
    mot(c, cx, cy + w * 0.30, w * 0.235, couleur, alpha)
    if avec_baseline:
        baseline(c, cx, cy + w * 0.46, w * 0.052, couleur, alpha * 0.92)


def decal(centre, r, w, h, nom, rot=0.0, ax=0.0, alpha=1.0, couleur=BLANC, n=14, assombri=0.0, encre=False):
    """plaque une image (blanc sur alpha) sur le flanc d'un cylindre, centrée sur l'angle `rot`"""
    i = nom if isinstance(nom, skia.Image) else moteur._img(nom)
    iw, ih = i.width(), i.height()
    theta = min(w / r, math.pi * 0.9)          # longueur d'arc → angle couvert
    cx, cy, cz = centre
    plans = []
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        a0 = rot - theta / 2 + theta * u0
        a1 = rot - theta / 2 + theta * u1
        am = (a0 + a1) / 2
        p0 = _quad(r, a0, a1, -h / 2, -h / 2)
        p1 = _quad(r, a0, a1, h / 2, h / 2)
        pts = _pose([p0[0], p0[1], p1[2], p1[3]], centre, ax=ax)
        # l'impression s'assombrit quand elle fuit vers le bord du cylindre
        k2 = borne(0.30 + 0.70 * max(0.0, math.cos(am - rot)) ** 0.7)
        # une encre noire s'éclaircit légèrement vers le bord (le verre la voile), une blanche s'assombrit
        col = _teinte("#4A545F", couleur, k2) if encre else _teinte("#2A3340", couleur, k2 * (1 - assombri))
        src = skia.Rect.MakeXYWH(iw * u0, 0, iw * (u1 - u0) + 0.6, ih)

        def dessin(c, w2, h2, src=src, col=col, i=i):
            p = skia.Paint(AntiAlias=True)
            p.setColorFilter(skia.ColorFilters.Blend(hexa(col, 1.0), skia.BlendMode.kSrcIn))
            c.drawImageRect(i, src, skia.Rect.MakeWH(w2 + 0.8, h2), moteur._ECH, p)
        plans.append(Plan(pts, 64, max(10.0, h), dessin, alpha, True))
    return plans


# ─────────────────────────────────────────── le produit
# cotes réelles relevées sur la boîte : 209 mm de haut, 83 mm de diamètre, 500 ml
# proportions relevées sur les photos de face du client (IMG_3419 / IMG_3420 / IMG_3422)
H_MM, D_MM = 209.0, 83.0
Y_BASE, Y_CORPS, Y_COUV = 0.250, 0.550, 0.200       # part de la hauteur
R_BASE, R_CORPS, R_COUV = 0.492, 0.500, 0.498       # fractions du diamètre


@functools.lru_cache(maxsize=4)
def _bloc_logo(w=560):
    """le bloc logo imprimé sur le corps, rendu une fois en image blanche sur alpha"""
    h = int(w * 0.62)
    s = skia.Surface(int(w), h)
    c = s.getCanvas()
    c.clear(0x00000000)
    symbole(c, w / 2, h * 0.27, w * 0.30, BLANC, 1.0)
    mot(c, w / 2, h * 0.645, w * 0.196, BLANC, 1.0)
    baseline(c, w / 2, h * 0.845, w * 0.044, BLANC, 0.95)
    return s.makeImageSnapshot()


@functools.lru_cache(maxsize=4)
def _bloc_grad(w=150):
    """l'échelle graduée oz / ml sérigraphiée près du haut du corps"""
    h = int(w * 1.55)
    s = skia.Surface(int(w), h)
    c = s.getCanvas()
    c.clear(0x00000000)
    for k, (oz, ml) in enumerate([("17", "500"), ("14", "400"), ("10", "300"), ("7", "200")]):
        y = h * (0.10 + 0.27 * k)
        trait(c, w * 0.04, y, w * 0.34, y, BLANC, max(1.4, w * 0.016), 0.95)
        texte(c, oz, w * 0.40, y - w * 0.105, w * 0.155, BLANC, "noir", alpha=0.95)
        texte(c, "/", w * 0.60, y - w * 0.105, w * 0.155, BLANC, "noir", alpha=0.6)
        texte(c, ml, w * 0.70, y - w * 0.105, w * 0.155, BLANC, "noir", alpha=0.95)
    return s.makeImageSnapshot()


def shaker(cam, cy=0.0, h=620.0, rot=0.0, ax=0.0, cx=0.0, cz=0.0, alpha=1.0,
           niveau=0.0, helice=True, led=0.0, bec=0.0, eclate=0.0, rot_helice=None, ecart=1.0, pieces=None,
           encre=None, manchon_=False):
    """renvoie les Plans du shaker complet, centré en (cx, cy, cz), haut de `h` pixels.

    rot : rotation du produit sur son axe (le logo est face caméra à rot = 0)
    niveau : 0 à 1, hauteur du liquide ; led : 0 à 1, éclat du bouton ; bec : 0 à 1, bec relevé
    eclate : 0 à 1, vue éclatée — le couvercle monte, l'hélice et la base descendent, le corps reste
    rot_helice : angle propre des pales (None = solidaire du produit) ; ecart : amplitude de l'éclaté (1 = standard)
    pieces : sous-ensemble de {"base", "corps", "helice", "couvercle"} à dessiner (None = tout)
    encre : couleur de l'impression sur le corps (None = blanc, comme la boîte ; le vrai produit est imprimé en NOIR
            sur le Tritan — photos du client IMG_3419/3420/3422, relu le 30/10/2026 après son retour)
    manchon_ : coque noire autour du corps, percée de deux fenêtres (le vrai produit ; False = corps nu, v3/v4)
    """
    pieces = pieces or {"base", "corps", "helice", "couvercle"}
    d = h * D_MM / H_MM
    rb, rc, rk = d * R_BASE, d * R_CORPS, d * R_COUV
    hb, hc, hk = h * Y_BASE, h * Y_CORPS, h * Y_COUV
    E = borne(eclate) * ecart
    y_base = cy + h / 2 - hb / 2 + E * h * 0.34
    y_corps = cy + h / 2 - hb - hc / 2
    y_couv = cy - h / 2 + hk / 2 - E * h * 0.30
    P = []
    P_tout = P

    # ── corps : Tritan transparent — Fresnel par bande, l'arrière se lit à travers l'avant
    if "corps" not in pieces: P = []
    P += cylindre((cx, y_corps, cz), rc, hc, CORPS["bas"], CORPS["haut"], n=72, rot=rot, ax=ax,
                  alpha=CORPS["alpha"] * alpha, spec=CORPS["spec"], dur=44, contre=CORPS["contre"], recto=False, verre=True)

    # ── liquide
    if niveau > 0.02:
        hl = hc * borne(niveau) * 0.86
        yl = cy + h / 2 - hb - hl / 2
        P += cylindre((cx, yl, cz), rc * 0.95, hl, "#49566A", "#CBD9E8", n=64, rot=rot, ax=ax,
                      alpha=0.46 * alpha, spec=0.60, dur=16, contre=0.40, recto=False, verre=True)
        P += disque((cx, yl - hl / 2, cz), rc * 0.95, "#DCE6F0", n=56, ax=ax, alpha=0.72 * alpha)

    P = P_tout if "corps" in pieces else []
    # ── hélice de mélange : petit fouet d'acier à deux pales sur son axe, au fond du corps (photos du client)
    if helice and "helice" in pieces:
        rh = rot if rot_helice is None else rot_helice
        ya = cy + h / 2 - hb - hc * 0.14 + E * h * 0.20
        P += cylindre((cx, ya, cz), d * 0.028, hc * 0.24, "#8E99A6", "#F2F6FA", n=14, rot=rot, ax=ax,
                      alpha=0.92 * alpha, spec=1.0, dur=14, contre=0.6, recto=False)
        for b in range(2):
            ab = rh + math.pi * b + math.pi / 4
            p = [(0, -hc * 0.012, 0), (d * 0.30 * math.cos(ab), -hc * 0.040, d * 0.30 * math.sin(ab)),
                 (d * 0.30 * math.cos(ab), hc * 0.000, d * 0.30 * math.sin(ab)), (0, hc * 0.020, 0)]
            pts = _pose(p, (cx, ya - hc * 0.09, cz), ax=ax)
            col = _teinte("#AEB9C5", BLANC, 0.30 + 0.60 * max(0.0, math.cos(ab - A_LUM)))

            def dessin(c, w2, h2, col=col):
                c.drawRect(skia.Rect.MakeWH(w2, h2), peinture(col))
            P.append(Plan(pts, 40, 40, dessin, 0.85 * alpha, False))

    # ── sérigraphies sur le corps : graduations en haut, bloc logo au centre
    P = P_tout if "corps" in pieces else []
    c_grad, c_logo = ("#E9F1F8", BLANC) if encre is None else (encre, encre)
    P += decal((cx, y_corps - hc * 0.30, cz), rc * 1.004, d * 0.30, hc * 0.30, _bloc_grad(),
               rot=rot - math.pi / 2 + math.radians(30), ax=ax, alpha=0.80 * alpha, couleur=c_grad, n=8, encre=encre is not None)
    P += decal((cx, y_corps + hc * 0.02, cz), rc * 1.004, d * 0.70, hc * 0.46, _bloc_logo(),
               rot=rot - math.pi / 2, ax=ax, alpha=0.96 * alpha, couleur=c_logo, n=16, encre=encre is not None)

    if manchon_ and "corps" in pieces:
        P += manchon((cx, y_corps, cz), rc * 1.03, hc * 1.002, rot=rot, ax=ax, alpha=alpha)

    # ── base moteur : noire mate, anneau de jonction, bouton LED
    P = P_tout if "base" in pieces else []
    P += cylindre((cx, y_base, cz), rb, hb, "#07090C", "#272E37", n=72, rot=rot, ax=ax,
                  alpha=alpha, spec=0.42, dur=46, contre=0.30)
    P += disque((cx, y_base + hb / 2, cz), rb, "#07090C", n=48, ax=ax, alpha=alpha)
    P += cylindre((cx, y_base - hb / 2 + h * 0.011, cz), rb * 1.012, h * 0.022, "#05070A", "#4E5862",
                  n=72, rot=rot, ax=ax, alpha=alpha, spec=0.85, dur=24, contre=0.45)
    # le bouton, légèrement en relief sur la face avant de la base
    yb = y_base + hb * 0.16
    P += decal((cx, yb, cz), rb * 1.008, d * 0.17, hb * 0.20, _bouton(led),
               rot=rot - math.pi / 2, ax=ax, alpha=alpha, couleur=BLANC, n=6)

    # ── couvercle noir : jupe, puis un DÔME arrondi (anneaux tronconiques), le clapet du bec posé dessus
    P = P_tout if "couvercle" in pieces else []
    y_jupe = y_couv + hk / 2 - hk * 0.26
    P += cylindre((cx, y_jupe, cz), rk, hk * 0.52, "#080B0F", "#2B323B", n=72, rot=rot, ax=ax,
                  alpha=alpha, spec=0.50, dur=42, contre=0.32, r2=rk * 1.012)
    y_top = y_couv + hk / 2 - hk * 0.52
    r_prev = rk * 1.0
    for frac_h, frac_r, bas_, haut_ in ((0.15, 0.965, "#090D12", "#30383F"), (0.13, 0.90, "#0A0E13", "#363E47"),
                                        (0.11, 0.78, "#0B1015", "#3B434C"), (0.09, 0.56, "#0C1116", "#424A53")):
        hh_ = hk * frac_h; r_new = rk * frac_r
        P += cylindre((cx, y_top - hh_ / 2, cz), r_prev, hh_, bas_, haut_, n=72, rot=rot, ax=ax,
                      alpha=alpha, spec=0.55, dur=30, contre=0.36, r2=r_new)
        y_top -= hh_; r_prev = r_new
    P += disque((cx, y_top, cz), r_prev, "#141A21", n=56, ax=ax, alpha=alpha)
    y_dome = y_top
    P += cylindre((cx, y_couv + hk / 2 - h * 0.008, cz), rk * 1.018, h * 0.016, "#04060A", "#525C67",
                  n=72, rot=rot, ax=ax, alpha=alpha, spec=0.9, dur=22, contre=0.5)

    # le clapet : plaque arrondie posée sur le dôme, vers l'avant, relevée de `bec`
    ab = rot - math.pi / 2
    lx, lz = math.cos(ab), math.sin(ab)
    incl = -22 - 50 * borne(bec)
    yc = y_dome - hk * 0.04
    for (dw, dd, ep, col, ya) in ((0.46, 0.50, 0.055, "#171D25", 0.0),
                                  (0.30, 0.34, 0.030, "#232B35", -0.026)):
        p = []
        for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            px = sx * d * dw / 2
            pz = sz * d * dd / 2
            yy = pz * math.tan(math.radians(incl))
            p.append((px * lz - pz * lx + cx, yc + yy + h * ya, px * lx + pz * lz + cz))
        colb = _teinte(col, BLANC, 0.22 + 0.30 * max(0.0, math.cos(ab - A_LUM)))

        def dessin(c, w2, h2, colb=colb, dw=dw):
            rrect(c, 0, 0, w2, h2, min(w2, h2) * 0.26, colb)
            rrect(c, w2 * 0.06, h2 * 0.05, w2 * 0.88, h2 * 0.30, min(w2, h2) * 0.18, "#FFFFFF", 0.055)
        P.append(Plan(p, 180, 180, dessin, alpha, False))

    # charnière : petit fût couché contre l'arrière du dessus
    hz = (rk * 0.50)
    P += cylindre((cx + lx * hz, yc + hk * 0.06, cz + lz * hz), d * 0.046, d * 0.26,
                  "#05070B", "#3A424D", n=20, rot=rot, ax=90, alpha=alpha, spec=0.7, dur=26, contre=0.4)

    return P_tout


@functools.lru_cache(maxsize=8)
def _bouton(led=0.0):
    """pastille du bouton de démarrage, avec sa diode quand il tourne"""
    w, h = 160, 190
    s = skia.Surface(w, h)
    c = s.getCanvas()
    c.clear(0x00000000)
    rrect(c, w * 0.16, h * 0.20, w * 0.68, h * 0.58, w * 0.30, "#FFFFFF", 0.13)
    rrect(c, w * 0.16, h * 0.20, w * 0.68, h * 0.58, w * 0.30, "#FFFFFF", 0.0, None, "#FFFFFF", 2.0)
    if led > 0.01:
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(w / 2, h * 0.49), w * 0.46,
                                                   [hexa("#CFE4FF", 0.95 * led), hexa("#5FA8FF", 0.0)]))
        c.drawCircle(w / 2, h * 0.49, w * 0.46, p)
    return s.makeImageSnapshot()
