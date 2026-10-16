"""Briques de scène MONARQUE au niveau validé (MQ-M05, 16/10/2026, « le client a adoré ») — reprises par MQ-M06 et suivantes.
Graphique « vos ventes » (un modèle différent par barre), horloge, carte d'embarquement, fiche de coûts, conversation,
carton de fin à la signature du client. Voir reference/monarque.md."""
import math
import skia
from moteur import *
from kit import pastille, tampon, texte_centre
from studio import lettres, entre, eclats, curseur
from monarque import *
from monarque import VERT, ROUGE

MODELES = ["produits/veste-ceinturee-prune", "produits/blouson-cuir-noir", "produits/veste-zip-marine", "produits/chemise-rayee-bordeaux"]


def graphique(c, t, cx, cy, hb, best=None, best_on=False, alpha=1.0, s=1.0, label="VOS VENTES", modeles=MODELES, couleur=BEIGE):
    """barres + vignettes (le style que le client aime) ; renvoie (x0, y0, base)"""
    x0, y0, w, h = cx - 420, cy - 330, 840, 660
    base = y0 + 470
    if alpha <= 0.01: return x0, y0, base
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, alpha):
        cadre(c, x0, y0, w, h, 44)
        texte(c, label, x0 + 60, y0 + 50, 34, ENCRE, "noir", track=0.06)
        for k in range(4):
            x = x0 + 90 + k * 180
            on = k == best and best_on
            hh = max(14, 330 * hb[k])
            rrect(c, x, base - hh, 120, hh, 18, couleur if on else "#DCD8D2")
            rrect(c, x - 5, base + 18, 130, 150, 22, "#EFEDEA")
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 5, base + 18, 130, 150), 22, 22), True)
            image_cover(c, modeles[k], x - 5, base + 18, 130, 150, 1.0, 0.5, 0.5); c.restore()
            if on: rrect(c, x - 5, base + 18, 130, 150, 22, None, 1, None, couleur, 5)
    c.restore()
    return x0, y0, base


def horloge(c, cx, cy, r, ang, a, aiguille=ROUGE):
    if a <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(a, a)
    disque(c, 0, 0, r, BLANC, 1, (16, 40, 0.18)); anneau(c, 0, 0, r - 4, ENCRE, 8)
    for k in range(12):
        an = k * math.pi / 6
        trait(c, (r - 26) * math.sin(an), -(r - 26) * math.cos(an), (r - 14) * math.sin(an), -(r - 14) * math.cos(an), ENCRE, 6)
    trait(c, 0, 0, r * 0.45 * math.sin(ang / 12), -r * 0.45 * math.cos(ang / 12), ENCRE, 12)
    trait(c, 0, 0, r * 0.72 * math.sin(ang), -r * 0.72 * math.cos(ang), aiguille, 7)
    disque(c, 0, 0, 14, ENCRE)
    c.restore()


def billet(c, cx, cy, w, alpha=1.0, rot=0.0, s=1.0, gris=False):
    """carte d'embarquement PARIS → CHINE (sans prix, sans date)"""
    if alpha <= 0.01 or s <= 0.01: return
    h = w * 0.52
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        rrect(c, -w / 2, -h / 2, w, h, 34, BLANC, 1, (22, 50, 0.2))
        rrect(c, -w / 2, -h / 2, w, h * 0.26, 34, "#9A968F" if gris else ENCRE)
        rrect(c, -w / 2, -h / 2 + h * 0.13, w, h * 0.13, 0, "#9A968F" if gris else ENCRE)
        texte(c, "CARTE D'EMBARQUEMENT", -w / 2 + 40, -h / 2 + h * 0.13 - hauteurLigne(26, "noir") / 2, 26, BLANC, "noir", track=0.08)
        icone(c, "plane", w / 2 - 60, -h / 2 + h * 0.13, 40, BLANC, 2.6)
        y = -h / 2 + h * 0.36
        texte(c, "PARIS", -w / 2 + 40, y, 64, ENCRE, "archivo", track=-0.01)
        texte(c, "CHINE", w / 2 - 40 - largeur("CHINE", 64, "archivo", -0.01), y, 64, ENCRE, "archivo", track=-0.01)
        trait(c, -w * 0.12, y + 40, w * 0.12, y + 40, GRIS, 4, 1, [6, 10])
        icone(c, "plane", 0, y + 40, 46, ENCRE, 2.6)
        for k, (lab, val) in enumerate([("PORTE", "—"), ("SIÈGE", "—"), ("VOL", "—")]):
            x = -w / 2 + 40 + k * (w - 80) / 3
            texte(c, lab, x, h / 2 - 120, 22, GRIS, "gras", track=0.06)
            texte(c, val, x, h / 2 - 84, 34, ENCRE, "noir")
        for k in range(26):                               # code-barres décoratif
            bw = 4 + (k * 7) % 5
            rrect(c, w / 2 - 260 + k * 9, h / 2 - 116, bw * 0.6, 70, 1, ENCRE, 0.85)
    c.restore()


def fiche_couts(c, t, x, y, w, h, t0, lignes, titre_="COSTING", rouges=()):
    """fiche de coûts sans montants : une barre par poste ; les postes de `rouges` passent au rouge"""
    texte(c, titre_, x + 30, y + 34, 34, ENCRE, "archivo", track=0.02)
    disque(c, x + w - 54, y + 56, 30, ENCRE); icone(c, "euro", x + w - 54, y + 56, 32, BLANC, 2.6)
    pas_ = min(124, (h - 150) / max(1, len(lignes)))
    for k, (lab, v) in enumerate(lignes):
        yy = y + 130 + k * pas_
        r = k in rouges
        texte(c, lab, x + 30, yy, 34, ROUGE if r else ENCRE, "gras", track=-0.01)
        rrect(c, x + 30, yy + 50, w - 60, 16, 8, "#E8E5E0")
        rrect(c, x + 30, yy + 50, (w - 60) * v * prog(t, t0 + 0.08 * k, 0.5, sortie), 16, 8, ROUGE if r else ENCRE)


def conversation(c, t, x, y, w, h, t0, titre_, msgs, ic="factory", ecart=0.3):
    """une conversation : msgs = [(texte, moi)] ; moi → bulle noire à droite, sinon blanche à gauche"""
    rrect(c, x, y, w, h, 22, "#EFEDEA")
    rrect(c, x, y, w, 76, 22, ENCRE)
    disque(c, x + 42, y + 38, 22, "#3A3A3A"); icone(c, ic, x + 42, y + 38, 24, BLANC, 2.2)
    texte(c, titre_, x + 76, y + 38 - hauteurLigne(26, "gras") / 2, 26, BLANC, "gras", track=-0.01)
    yy = y + 100
    for k, (m, moi) in enumerate(msgs):
        a = entre(t, t0 + ecart * k, 0.35, 2.2)
        if a <= 0: continue
        tw = largeur(m, 26, "gras", -0.01); bw = min(w - 40, tw + 40)
        bx = x + w - 18 - bw if moi else x + 18
        c.save(); c.translate(bx + (bw if moi else 0), yy + 28); c.scale(a, a); c.translate(-(bx + (bw if moi else 0)), -(yy + 28))
        rrect(c, bx, yy, bw, 56, 22, ENCRE if moi else BLANC, 1, None if moi else (4, 12, 0.08))
        texte(c, m, bx + 20, yy + 28 - hauteurLigne(26, "gras") / 2, 26, BLANC if moi else ENCRE, "gras", track=-0.01)
        c.restore()
        yy += 74


def flash_noir(c, t, t0, t1, l1, l2, couleur2=BEIGE, taille=150):
    """disque noir plein écran + deux lignes (le « SOYONS CLAIRS. » de MQ-M05) ; renvoie le rayon"""
    if t < t0 - 0.15 or t > t1 + 0.4: return 0
    r = disque_noir(c, t, t0 - 0.12, t1 - 0.12)
    a = entre(t, t0 - 0.02, 0.4, 2.0) * (1 - prog(t, t1 - 0.14, 0.14))
    if a > 0:
        ts1 = ajuste(l1, 960, taille, "archivo", -0.01); ts2 = ajuste(l2, 960, taille, "archivo", -0.01)
        lettres(c, l1, 540, 960 - ts1 * 1.05, ts1, t, t0 - 0.02, "ressort", fam="archivo", grad=False, couleur=BLANC, decal=0.03, alpha=borne(a * 3))
        lettres(c, l2, 540, 960 + ts2 * 0.1, ts2, t, t0 + 0.2, "ressort", fam="archivo", grad=False, couleur=couleur2, decal=0.03, alpha=borne(a * 3))
    return r


def signature(c, t, t0, lignes, t_bouton, label="monarqueprod.com", logo_y=640):
    """carton final : logo, lignes [(texte, t, fam, couleur)], bouton cliqué"""
    if t < t0 - 0.1: return
    u = entre(t, t0 - 0.05, 0.55, 1.4)
    logo(c, 540, logo_y, 820 * mix(0.7, 1, u), False, borne(u * 3))
    y = logo_y + 200
    for (txt, tl, fam, col) in lignes:
        a = entre(t, tl - 0.05, 0.45, 1.6)
        if a > 0: texte_centre(c, txt, 540, y + 30 * (1 - a), 46, col, fam, borne(a * 3), -0.01)
        y += 66
    d = entre(t, t_bouton - 0.15, 0.45, 2.0)
    if d > 0:
        by = y + 90
        clic = prog(t, t_bouton + 0.45, 0.12) * (1 - prog(t, t_bouton + 0.6, 0.15))
        s = mix(0.4, 1, d) * (1 - 0.06 * clic)
        c.save(); c.translate(540, by); c.scale(s, s)
        tw = largeur(label, 50, "noir", -0.01); w, h = tw + 190, 116
        rrect(c, -w / 2, -h / 2, w, h, h / 2, ENCRE, borne(d * 3), (16, 40, 0.3))
        icone(c, "arrow-right", w / 2 - 66, 0, 46, BLANC, 3.0, borne(d * 3))
        texte(c, label, -w / 2 + 56, -hauteurLigne(50) / 2, 50, BLANC, "noir", track=-0.01, alpha=borne(d * 3))
        c.restore()
        pc = prog(t, t_bouton + 0.05, 0.4, sortie)
        curseur(c, mix(980, 700, pc), mix(by + 370, by + 20, pc), 1.3, 1 - prog(t, t_bouton + 0.9, 0.3), clic)
        eclats(c, 540, by, t, t_bouton + 0.5, 12, 300, [BEIGE, BEIGE2, ENCRE], graine=4)


def logo_monarque(c, t, t_mq, t_pose, t_part, y=250, w=340):
    """disque noir + grand logo blanc au mot « Monarque », puis le logo noir monte se poser en tête ; renvoie le rayon"""
    if t < t_mq - 0.15 or t > t_part + 0.4: return 0
    r = disque_noir(c, t, t_mq - 0.12, t_pose)
    u = prog(t, t_mq + 0.05, 0.36, lambda v: rebond(v, 1.6))
    v = prog(t, t_pose, 0.42, entreeSortie)
    o = prog(t, t_part - 0.15, 0.3, entree)
    if t >= t_mq + 0.03:
        lw = mix(1.5, 1, u) * mix(860, w, v)
        ly = mix(960, y, v)
        if v < 1: logo(c, 540, ly, lw, True, borne(u * 3) * (1 - v))
        if v > 0: logo(c, 540, ly - 300 * o, lw, False, v * (1 - o))
    return r
