"""CB-M01 v2 — « Le réseau en direct ». Toutes les scènes, les sous-titres et les sons.

Chaque élément est calé sur un mot de la voix (TW(i) = début du mot i dans
timing.json). dessine(c, t) peint l'image complète au temps t.
"""
import json, math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent          # ce projet
sys.path.insert(0, str(P.parent / "moteur"))
import moteur
moteur.PROJET = P
from moteur import *

TIMING = json.loads((P / "timing.json").read_text())
MOTS = TIMING["mots"]
CHINE = json.loads((P / "chine.json").read_text())
DUREE = 59.4
NB_IMAGES = round(DUREE * FPS)

def TW(i):
    return MOTS[i]["t0"]

# ─────────────────────────────────────────── sons (posés à côté de ce qu'ils accompagnent)
SFX = []
def son(t, nom, gain=0.0):
    if 0 <= t < DUREE: SFX.append((round(t, 3), nom, gain))

# fenêtres de mouvement rapide : flou de mouvement par sous-images
RAPIDE = []
def rapide(t0, t1):
    RAPIDE.append((t0, t1))

def flou_a(t):
    return 5 if any(a <= t <= b for a, b in RAPIDE) else 1

# ─────────────────────────────────────────── éclairs de couleur sur les temps forts
ECLAIRS = []
def eclair(t, couleur, a=0.11):
    ECLAIRS.append((t, couleur, a))

# ─────────────────────────────────────────── fond
def fond(c, t):
    c.clear(skia.ColorWHITE)
    p = peinture("#E6EBE8")
    dy = (t * 16) % 54
    for y in range(-54, H + 54, 54):
        for x in range(27, W, 54):
            c.drawCircle(x, y + 27 - dy, 2.3, p)

# ─────────────────────────────────────────── bandeau de marque
def bandeau(c, t):
    a = prog(t, 0.45, 0.35) * (1 - prog(t, 36.95, 0.2)) + prog(t, 41.0, 0.3) * (1 - prog(t, 57.75, 0.25))
    a = borne(a)
    if a <= 0: return
    with Calque(c, a):
        image(c, "logo", 90, 152, 170)
        lab = "LE RÉSEAU EN DIRECT"
        w = largeur(lab, 20, "fort", 0.12)
        texte(c, lab, 990, 158, 20, C["gris"], "fort", "droite", 0.12)
        disque(c, 990 - w - 20, 170, 6, C["vert"], 0.35 + 0.65 * (0.5 + 0.5 * math.cos(t * 4)))

# ─────────────────────────────────────────── sous-titres karaoké
# jeton : (indice du mot, texte affiché, style, temps imposé facultatif) — style g vert, r rouge
SOUS = [
    [(0, "T’achètes", "", -0.45), (1, "encore"), (2, "tes"), (3, "produits"), (4, "de"), (5, "Chine")],
    [(6, "à"), (7, "un"), (8, "revendeur", "r"), (9, "français"), (10, "installé"), (11, "là-bas ?")],
    [(12, "Tu"), (13, "veux"), (14, "faire"), (15, "de"), (16, "la"), (17, "marge ?", "g")],
    [(18, "Mais"), (19, "tu"), (20, "commences"), (21, "par"), (22, "payer"), (23, "la"), (24, "sienne.", "r")],
    [(25, "Regarde"), (26, "le"), (27, "circuit.", "g")],
    [(28, "Le"), (29, "fournisseur"), (30, "chinois"), (31, "vend"), (32, "au"), (33, "revendeur.", "r")],
    [(34, "Le"), (35, "revendeur"), (36, "ajoute"), (37, "sa", "r"), (38, "marge.", "r")],
    [(39, "Et"), (40, "toi,"), (41, "tu"), (42, "paies"), (42, "le", "", TW(42) + 0.14), (43, "total.", "r")],
    [(44, "À"), (45, "chaque"), (46, "commande.", "r")],
    [(47, "Et"), (48, "si"), (49, "tu"), (50, "contactais"), (51, "directement", "g")],
    [(52, "le"), (53, "fournisseur"), (54, "en"), (55, "Chine ?")],
    [(56, "Moi,"), (57, "j’ai"), (58, "passé"), (59, "des"), (60, "mois", "g"), (61, "sur"), (62, "place.")],
    [(63, "À"), (64, "chercher,", "g"), (65, "à"), (66, "commander,", "g")],
    [(67, "à"), (68, "comparer", "g"), (69, "et"), (70, "à"), (71, "faire"), (72, "le"), (73, "tri.", "g")],
    [(74, "Parce"), (75, "qu’en"), (76, "deux", "g"), (77, "semaines", "g"), (78, "à"), (79, "Guangzhou,")],
    [(80, "tu"), (81, "peux"), (82, "récupérer"), (83, "des"), (84, "contacts.")],
    [(85, "Mais"), (86, "savoir"), (87, "qui"), (88, "tient"), (89, "ses"), (90, "promesses,", "g")],
    [(91, "qui"), (92, "garde"), (93, "la"), (94, "même"), (95, "qualité", "g")],
    [(96, "et"), (97, "qui"), (98, "expédie"), (99, "correctement,", "g")],
    [(100, "ça"), (101, "demande"), (102, "du"), (103, "recul.", "g")],
    [(104, "Et"), (105, "plusieurs"), (106, "commandes.", "g")],
    [(107, "Ce"), (108, "travail,"), (109, "je"), (110, "l’ai"), (111, "fait.", "g")],
    [(112, "Dans"), (113, "le"), (114, "ChinaBook,", "g"), (116, "j’ai"), (117, "rassemblé")],
    [(118, "les"), (119, "contacts"), (120, "que"), (121, "j’ai"), (122, "testés", "g"), (123, "pendant"), (124, "des"), (125, "mois.", "", 40.78)],
    [(126, "Mes"), (127, "fournisseurs,", "g"), (128, "mon"), (129, "transitaire,", "g")],
    [(130, "le"), (131, "réseau"), (132, "que"), (133, "j’utilise"), (134, "moi-même.", "g")],
    [(135, "Tu"), (136, "contactes", "g"), (137, "les"), (138, "fournisseurs,")],
    [(139, "tu"), (140, "négocies", "g"), (141, "avec"), (142, "eux,")],
    [(143, "tu"), (144, "commandes", "g"), (145, "directement.", "g")],
    [(146, "Tu"), (147, "veux"), (148, "développer"), (149, "ton"), (150, "business ?", "g")],
    [(151, "Commence"), (152, "par"), (153, "reprendre"), (154, "le"), (155, "contrôle", "g"), (156, "de"), (157, "tes"), (158, "achats.")],
    [(159, "Envoie-moi"), (160, "« CHINA »", "g"), (161, "sur"), (162, "WhatsApp.")],
    [(163, "Je"), (164, "te"), (165, "montre"), (166, "le"), (167, "pack"), (168, "adapté"), (169, "à"), (170, "ce"), (171, "que"), (172, "tu"), (173, "veux"), (174, "vendre.", "g")],
    [(None, "Ton", "", 57.98), (None, "accès", "", 58.06), (None, "direct", "g", 58.16), (None, "à", "", 58.27), (None, "la", "", 58.32), (None, "Chine.", "", 58.38)],
]
SOUS_X, SOUS_Y, SOUS_L = 540, 292, 920

def _prepare_sous():
    blocs = []
    for k, bloc in enumerate(SOUS):
        mots = []
        for j in bloc:
            i, s = j[0], j[1]
            st = j[2] if len(j) > 2 else ""
            tw = j[3] if len(j) > 3 else TW(i)
            mots.append(dict(s=s, st=st, t=tw))
        taille = 104
        while True:
            esp = largeur(" ", taille) * 1.3
            lignes, cur, w = [], [], 0
            for m in mots:
                m["w"] = largeur(m["s"], taille)
                if cur and w + esp + m["w"] > SOUS_L:
                    lignes.append(cur); cur, w = [], 0
                w = m["w"] if not cur else w + esp + m["w"]
                cur.append(m)
            lignes.append(cur)
            if (len(lignes) <= 2 or (len(lignes) == 3 and taille <= 96)) or taille <= 70: break
            taille -= 4
        lh = taille * 1.08
        for n, ligne in enumerate(lignes):
            lw = sum(m["w"] for m in ligne) + esp * (len(ligne) - 1)
            x = SOUS_X - lw / 2
            for m in ligne:
                m["x"], m["y"] = x, SOUS_Y + n * lh
                x += m["w"] + esp
        debut = min(m["t"] for m in mots) - 0.12
        blocs.append(dict(mots=mots, taille=taille, debut=debut))
    for k, b in enumerate(blocs):
        b["fin"] = blocs[k + 1]["debut"] if k + 1 < len(blocs) else DUREE + 1
    blocs[-2]["fin"] = 57.90
    return blocs

BLOCS = _prepare_sous()

def sous_titres(c, t):
    for b in BLOCS:
        if not (b["debut"] - 0.01 <= t < b["fin"]): continue
        taille, mots = b["taille"], b["mots"]
        hl = hauteurLigne(taille)
        sortie_u = prog(t, b["fin"] - 0.16, 0.16, entree) if b["fin"] < DUREE else 0
        # mot actif : le dernier prononcé
        actifs = [k for k, m in enumerate(mots) if m["t"] - 0.05 <= t]
        ka = actifs[-1] if actifs else None
        if b is BLOCS[-1] and ka is not None:
            ka = min(ka, next(k for k, m in enumerate(mots) if m["st"] == "g"))
        # surlignage qui glisse d'un mot au suivant
        u_hl = 1.0
        k_prec, u_prec = None, 1.0   # mot que le surlignage est en train de quitter
        if ka is not None and sortie_u < 1:
            m = mots[ka]
            u = prog(t, m["t"] - 0.05, 0.12, sortie)
            prev = mots[ka - 1] if ka > 0 else None
            coul = C["rouge"] if m["st"] == "r" else C["vert"]
            pad, r = taille * 0.1, taille * 0.18
            if prev is not None and abs(prev["y"] - m["y"]) < 1:
                bx = mix(prev["x"], m["x"], u); bw = mix(prev["w"], m["w"], u); by = m["y"]
                u_hl = u
                k_prec, u_prec = ka - 1, u
                rrect(c, bx - pad, by + hl * 0.06 - sortie_u * 40, bw + 2 * pad, hl * 0.9, r, coul, 1 - sortie_u)
            else:
                # nouveau mot en début de ligne : le fond apparaît sur place
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
            base_c = C["vert"] if m["st"] == "g" else C["rouge"] if m["st"] == "r" else C["ink"]
            cx, cy = m["x"] + m["w"] / 2, m["y"] + hl / 2
            c.save(); c.translate(cx, cy + dy); c.scale(s, s)
            if k == ka and u_hl >= 0.999:
                texte(c, m["s"], -m["w"] / 2, -hl / 2, taille, C["blanc"], alpha=a)
            elif k == ka:
                texte(c, m["s"], -m["w"] / 2, -hl / 2, taille, base_c, alpha=a * (1 - u_hl))
                texte(c, m["s"], -m["w"] / 2, -hl / 2, taille, C["blanc"], alpha=a * u_hl)
            elif k == k_prec and u_prec < 0.999:
                # le fond glisse encore sous ce mot : il ne reprend sa couleur qu'en le quittant
                texte(c, m["s"], -m["w"] / 2, -hl / 2, taille, C["blanc"], alpha=a * (1 - u_prec))
                texte(c, m["s"], -m["w"] / 2, -hl / 2, taille, base_c, alpha=a * u_prec)
            else:
                texte(c, m["s"], -m["w"] / 2, -hl / 2, taille, base_c, alpha=a)
            c.restore()

# ─────────────────────────────────────────── briques de scène
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

def texte_centre(c, s, cx, cy, taille, couleur=C["ink"], fam="noir", alpha=1.0, track=-0.025):
    """centre la chaîne sur (cx, cy) en calant la hauteur des capitales"""
    base, w = _para_info(s, fam, taille, track)
    y = cy - base + 0.727 * taille / 2
    texte(c, s, cx - w / 2, y, taille, couleur, fam, "gauche", track, alpha)
    return w

def _para_info(s, fam, taille, track):
    from moteur import _para, _ls
    p = _para(s, fam, float(taille), 0xFF000000, _ls(taille, track))
    return p.AlphabeticBaseline, p.LongestLine

def telephone(c, x, y, w=480, h=960, ecran=None, t=0.0, alpha=1.0):
    """téléphone : corps noir, écran blanc découpé ; ecran(c, x, y, w, h) dessine le contenu"""
    with Calque(c, alpha):
        carte(c, x, y, w, h, 74, C["ink"], 1.0, (40, 90, 0.28))
        ex, ey, ew, eh = x + 14, y + 14, w - 28, h - 28
        c.save()
        c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(ex, ey, ew, eh), 60, 60), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(ex, ey, ew, eh), peinture(C["blanc"]))
        if ecran: ecran(c, ex, ey, ew, eh)
        c.restore()
        rrect(c, x + w / 2 - 62, y + 30, 124, 34, 17, C["ink"])

def produit(c, nom, cx, cy, w, alpha=1.0, ombre=True):
    iw, ih = taille_img(nom)
    h = w * ih / iw
    if ombre: ombre_sol(c, cx, cy + h / 2 - h * 0.02, w * 0.42, h * 0.06, 0.18 * alpha)
    image(c, nom, cx - w / 2, cy - h / 2, w, alpha)
    return h

# ═══════════════════════════════════════════ S1 · Accroche (0 → 3,62)
son(0.0, "impact", -6); son(0.0, "whoosh_court", -13)
son(TW(3) - 0.06, "whoosh", -15); son(TW(3) + 0.1, "impact_doux", -14)
son(TW(5) - 0.06, "whoosh", -15); son(TW(5) + 0.1, "impact_doux", -14)
son(1.6, "whoosh_court", -16); son(TW(8) - 0.04, "tampon", -9)
son(TW(9) - 0.04, "pop", -14); son(TW(10) - 0.04, "pop", -15); son(3.30, "whoosh", -12)
rapide(0.0, 0.26); rapide(TW(3) - 0.08, TW(3) + 0.26); rapide(TW(5) - 0.08, TW(5) + 0.26); rapide(1.55, 1.85); rapide(3.30, 3.52)
eclair(0.03, C["vert"], 0.10); eclair(TW(8), C["rouge"], 0.10)

def s1(c, t):
    if t > 3.52: return
    sortie_u = prog(t, 3.30, 0.22, entree)
    cam = 1 + 0.04 * prog(t, 0, 3.4, lin) + 0.9 * sortie_u
    dx, dy = secousse(t, 0.02, 16); ex, ey = secousse(t, TW(8), 12)
    c.save(); c.translate(540 + dx + ex, 1080 + dy + ey); c.scale(cam, cam); c.translate(-540, -1080)
    with Calque(c, 1 - sortie_u):
        tA, tB, tC = TW(3) - 0.08, TW(5) - 0.08, 1.58
        # carrousel : moto → pull → casque, puis les trois réunis
        def vol(t, t_in, t_out, cote_in=1):
            """position x et rotation y d'un produit qui entre puis sort"""
            u_in = prog(t, t_in, 0.3, sortie) if t_in > 0 else 1.0
            u_out = prog(t, t_out, 0.26, entree) if t_out else 0.0
            x = mix(1150 * cote_in, 0, u_in) + mix(0, -1150, u_out)
            ry = mix(-55 * cote_in, 0, u_in) + mix(0, 55, u_out)
            return x, ry
        # moto : déjà là à l'image 0 (arrivée frappée)
        if t < tA + 0.3:
            x, ry = vol(t, -1, tA)
            s = 1 + 0.32 * (1 - prog(t, 0, 0.3, sortie))
            with Espace(c, 540 + x, 1060, ry=ry, rz=-6 * (1 - prog(t, 0, 0.3, sortie)), s=s):
                produit(c, "moto", 540 + x, 1060, 820)
        if tA - 0.02 < t < tB + 0.3:
            x, ry = vol(t, tA, tB)
            with Espace(c, 540 + x, 1060, ry=ry):
                produit(c, "pull", 540 + x, 1040, 500)
        if tB - 0.02 < t < tC + 0.3:
            x, ry = vol(t, tB, tC)
            with Espace(c, 540 + x, 1060, ry=ry):
                produit(c, "casque", 540 + x, 1050, 520)
        # la moto revient, seule, pour recevoir l'étiquette du revendeur
        if t >= tC:
            uu = prog(t, tC, 0.34, sortie)
            x, ry = mix(1150, 0, uu), mix(-55, 0, uu)
            with Espace(c, 540 + x, 1080, ry=ry):
                produit(c, "moto", 500 + x, 1080, 700)
            # étiquette rouge du revendeur, suspendue, qui se balance
            tE = TW(8) - 0.08
            if t >= tE:
                v = t - tE
                chute = prog(t, tE, 0.22, sortie)
                ang = 26 * math.exp(-3.2 * v) * math.cos(9.5 * v) if v > 0.22 else -30 * (1 - chute)
                ax, ay = 760, 720
                c.save(); c.translate(ax, ay - 300 * (1 - chute)); c.rotate(ang)
                trait(c, 0, 0, 0, 150, C["ink"], 3)
                carte(c, -170, 150, 340, 130, 26, C["rouge"], 1.0, (14, 30, 0.2))
                disque(c, -132, 215, 13, C["blanc"])
                texte_centre(c, "REVENDEUR", 18, 196, 40, C["blanc"])
                texte_centre(c, "+ sa marge", 18, 243, 28, C["blanc"], "fort")
                c.restore()
            # repère : revendeur français installé en Chine
            tF, tG = TW(9) - 0.06, TW(10) - 0.06
            if t >= tF:
                u1 = prog(t, tF, 0.35, lambda v: rebond(v, 1.8))
                w1 = 300; cx1 = 330
                with Calque(c, borne(u1 * 2)):
                    c.save(); c.translate(cx1, 1370); c.scale(mix(0.5, 1, u1), mix(0.5, 1, u1))
                    carte(c, -w1 / 2, -48, w1, 96, 48, C["blanc"], 1.0, (12, 30, 0.14))
                    drapeau(c, "FR", -w1 / 2 + 26, -22, 66, 44)
                    texte(c, "Français", -w1 / 2 + 108, -48 + (96 - hauteurLigne(36)) / 2, 36)
                    c.restore()
            if t >= tG:
                u2 = prog(t, tG, 0.35, lambda v: rebond(v, 1.8))
                cx2 = 760
                trait(c, 490, 1370, mix(490, 600, prog(t, tG, 0.3)), 1370, C["vert"], 6, 1, (2, 14))
                with Calque(c, borne(u2 * 2)):
                    c.save(); c.translate(cx2, 1370); c.scale(mix(0.5, 1, u2), mix(0.5, 1, u2))
                    w2 = 330
                    carte(c, -w2 / 2, -48, w2, 96, 48, C["ink"], 1.0, (12, 30, 0.14))
                    drapeau(c, "CN", -w2 / 2 + 26, -22, 66, 44)
                    texte(c, "en Chine", -w2 / 2 + 108, -48 + (96 - hauteurLigne(36)) / 2, 36, C["blanc"])
                    c.restore()
    c.restore()

# ═══════════════════════════════════════════ S2 · La barre qui se fait écraser (3,40 → 6,98)
son(3.48, "swipe", -15); son(3.66, "pop", -16); son(TW(17) - 0.06, "pop", -11); son(TW(17) + 0.05, "verre", -18)
son(TW(22) - 0.08, "whoosh_court", -14); son(TW(22) + 0.06, "impact", -11); son(TW(24) - 0.04, "tampon", -10); son(6.8, "whoosh", -13)
rapide(3.46, 3.7); rapide(TW(22) - 0.05, TW(22) + 0.3); rapide(6.78, 6.98)
eclair(TW(24) - 0.02, C["rouge"], 0.10)

def s2(c, t):
    if not (3.46 <= t <= 6.98): return
    entree_u = prog(t, 3.46, 0.32, sortie); sortie_u = prog(t, 6.78, 0.2, entree)
    x0, x1, yb, hb = 100, 980, 1090, 150
    tUs, tTa, tSa, tSi = 3.62, TW(17) - 0.06, TW(22) - 0.08, TW(24) - 0.04
    lUs = 360 * prog(t, tUs, 0.4, sortie)
    lSa = 300 * prog(t, tSa, 0.36, lambda v: rebond(v, 1.3))
    lTa_max = x1 - x0 - lUs
    lTa = (x1 - x0 - 360) * prog(t, tTa, 0.42, lambda v: rebond(v, 1.4)) - lSa
    lTa = max(0, min(lTa, lTa_max - lSa))
    dx, dy = secousse(t, tSa + 0.3, 12); ex, ey = secousse(t, tSi, 10)
    c.save(); c.translate(dx + ex, dy + ey - 1300 * sortie_u + 200 * (1 - entree_u))
    with Calque(c, entree_u):
        # le produit, posé au-dessus de la barre
        produit(c, "moto", 290, 860, 330)
        texte(c, "Ce que tu achètes", 470, 812, 34, C["gris"], "demi")
        texte(c, "en Chine", 470, 856, 34, C["gris"], "demi")
        # repère du prix de vente (fixe)
        trait(c, x1, yb - 70, x1, yb + hb + 70, C["ink"], 4, 1, (10, 10))
        texte(c, "PRIX DE VENTE", x1, yb + hb + 84, 24, C["ink"], "fort", "droite", 0.08)
        # la barre
        rrect(c, x0, yb, x1 - x0, hb, 34, C["fondDoux"])
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, yb, x1 - x0, hb), 34, 34), doAntiAlias=True)
        segs = [("Fournisseur", lUs, C["ink"]), ("Sa marge", lSa, C["rouge"]), ("Ta marge", lTa, C["vert"])]
        x = x0
        for nom, l, coul in segs:
            if l > 1:
                c.drawRect(skia.Rect.MakeXYWH(x, yb, l + 1, hb), peinture(coul))
                taille = ajuste(nom, l - 30, 44, mini=18)
                if l > 60: texte_centre(c, nom, x + l / 2, yb + hb / 2, taille, C["blanc"])
                x += l
        c.restore()
        # pression : la marge verte écrasée
        if t > tSa + 0.2:
            u = prog(t, tSa + 0.2, 0.3)
            xr = x0 + lUs + lSa
            for k in range(3):
                yy = yb + 30 + k * 45
                trait(c, xr + 10 + 14 * math.sin(t * 30 + k), yy, xr + 40 + 14 * math.sin(t * 30 + k), yy, C["blanc"], 5, u * 0.8)
        # bulle « TA MARGE ? » puis tampon « LA SIENNE »
        if tTa <= t < tSa + 0.2:
            u = prog(t, tTa, 0.35, lambda v: rebond(v, 1.8)); a = 1 - prog(t, tSa, 0.2)
            pastille_rot(c, "TA MARGE ?", 760, yb - 90, 34, C["vert"], C["blanc"], -6, mix(0.3, 1, u), a)
        if t >= tSi - 0.12:
            u = prog(t, tSi - 0.12, 0.16, entree)
            s = mix(2.6, 1, u)
            c.save(); c.translate(560, yb - 105); c.rotate(-8); c.scale(s, s)
            with Calque(c, u):
                w, h = 380, 110
                rrect(c, -w / 2, -h / 2, w, h, 22, C["blanc"], 0.92, None, C["rouge"], 8)
                texte_centre(c, "LA SIENNE", 0, 0, 54, C["rouge"])
            c.restore()
    c.restore()

def pastille_rot(c, label, cx, cy, taille, fond_, texte_c, rot, s, alpha, icone_=None, ombre=(12, 30, 0.18)):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    pastille(c, label, 0, 0, taille, fond_, texte_c, icone_, alpha, ombre)
    c.restore()

# ═══════════════════════════════════════════ S3 · Le circuit, puis le contact direct (6,84 → 18,62)
NX, NR = 200, 82
RANG = {"usine": 820, "rev": 1080, "toi": 1340}
tC0 = TW(25) - 0.02
t_vend, t_arr = TW(31) - 0.05, TW(33)
t_marge = TW(37) - 0.04
t_toi = TW(39) - 0.04
t_total = TW(43) - 0.06
t_boucle = TW(44) - 0.04
t_cis1, t_cis2, t_chute = TW(50) - 0.04, TW(50) + 0.32, TW(51) - 0.06
t_ligne, t_direct = TW(53) - 0.06, TW(55) - 0.06
son(tC0, "pop", -16); son(tC0 + 0.15, "pop", -17); son(tC0 + 0.3, "pop", -18)
son(TW(29) - 0.06, "pop", -16); son(t_vend, "whoosh_court", -15); son(t_arr, "clic", -13)
son(t_marge - 0.1, "whoosh_court", -16); son(t_marge + 0.06, "tampon", -8)
son(t_toi, "whoosh_court", -15); son(t_toi + 0.42, "clic", -13); son(t_total, "pop", -11); son(t_total + 0.25, "swipe", -17)
for k in range(3):
    son(t_boucle + k * 0.24, "whoosh_court", -20); son(t_boucle + k * 0.24 + 0.22, "pop", -16 - k)
son(15.82, "whoosh", -15); son(t_cis1, "clic", -8); son(t_cis1 + 0.02, "swipe", -14); son(t_cis2, "clic", -8); son(t_cis2 + 0.02, "swipe", -14)
son(t_chute, "whoosh_bas", -11); son(t_chute + 0.5, "impact_doux", -15)
son(t_ligne, "swipe", -14); son(t_direct, "verre", -10); son(t_direct + 0.02, "pop", -11); son(18.42, "whoosh", -13)
rapide(t_vend, t_vend + 0.4); rapide(t_marge - 0.14, t_marge + 0.08); rapide(t_toi, t_toi + 0.42); rapide(t_boucle - 0.02, t_boucle + 0.95)
rapide(t_chute, t_chute + 0.55); rapide(18.42, 18.62)
eclair(t_marge + 0.06, C["rouge"], 0.09); eclair(TW(46), C["rouge"], 0.09); eclair(t_direct, C["vert"], 0.12)

def colis(c, cx, cy, s=1.0, marge=0.0, alpha=1.0, rot=0.0):
    """colis : carte produit + étiquette de prix dont la partie rouge grandit avec la marge"""
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        carte(c, -110, -95, 220, 190, 30, C["blanc"], 1.0, (16, 36, 0.16))
        produit(c, "moto", 0, -22, 168, ombre=False)
        lu = 120; lm = 70 * marge
        x0 = -(lu + lm) / 2
        rrect(c, x0, 50, lu, 22, 11, C["ink"])
        if lm > 1: rrect(c, x0 + lu - 11, 50, lm + 11, 22, 11, C["rouge"])
    c.restore()

def s3(c, t):
    if not (6.84 <= t <= 18.62): return
    sortie_u = prog(t, 18.42, 0.2, entree)
    entree_u = prog(t, 6.84, 0.3, sortie)
    c.save(); c.translate(0, -1350 * sortie_u + 160 * (1 - entree_u))
    with Calque(c, entree_u):
        # rapprochement final : fournisseur et toi se rejoignent
        uRap = prog(t, t_chute + 0.35, 0.5, entreeSortie)
        yU = mix(RANG["usine"], 900, uRap); yT = mix(RANG["toi"], 1240, uRap)
        uCut = prog(t, t_chute, 0.6, entree)
        yR = RANG["rev"] + 700 * uCut; rotR = 28 * uCut; aR = 1 - prog(t, t_chute + 0.3, 0.3)
        # rail (gris), puis rail direct (vert)
        uRail = prog(t, tC0, 0.6, sortie)
        if uRail > 0 and t < t_chute + 0.4:
            a = 1 - prog(t, t_chute, 0.3)
            # rail coupé en deux par les ciseaux
            gap1 = 26 * prog(t, t_cis1, 0.15); gap2 = 26 * prog(t, t_cis2, 0.15)
            yc1 = (RANG["usine"] + RANG["rev"]) / 2; yc2 = (RANG["rev"] + RANG["toi"]) / 2
            yfin = mix(RANG["usine"], RANG["toi"], uRail)
            trait(c, NX, RANG["usine"], NX, min(yfin, yc1 - gap1), C["ligne"], 14, a)
            if yfin > yc1 + gap1: trait(c, NX, yc1 + gap1, NX, min(yfin, yc2 - gap2), C["ligne"], 14, a)
            if yfin > yc2 + gap2: trait(c, NX, yc2 + gap2, NX, yfin, C["ligne"], 14, a)
            # flux qui descend
            if t > t_vend:
                p = peinture(C["grisClair"], a, Style=skia.Paint.kStroke_Style, StrokeWidth=6)
                p.setStrokeCap(skia.Paint.kRound_Cap); p.setPathEffect(skia.DashPathEffect.Make([2, 22], -(t * 60) % 24))
                c.drawLine(NX, RANG["usine"], NX, yfin, p)
        if t >= t_ligne:
            u = prog(t, t_ligne, 0.35, sortie)
            trait(c, NX, yU, NX, mix(yU, yT, u), C["vert"], 14)
            p = peinture(C["blanc"], 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=6)
            p.setStrokeCap(skia.Paint.kRound_Cap); p.setPathEffect(skia.DashPathEffect.Make([2, 22], -(t * 90) % 24))
            c.drawLine(NX, yU, NX, mix(yU, yT, u), p)
        # nœuds et étiquettes
        def noeud(y, coul, ic, titre, sous, t_in, alpha=1.0, rot=0.0, pulse=1.0):
            u = prog(t, t_in, 0.4, lambda v: rebond(v, 1.9))
            if u <= 0: return
            c.save(); c.translate(NX, y); c.rotate(rot); s = mix(0.3, 1, u) * pulse; c.scale(s, s)
            with Calque(c, alpha * borne(u * 2)):
                disque(c, 0, 0, NR, coul, 1.0, (14, 34, 0.18))
                icone(c, ic, 0, 0, 78, C["blanc"], 2.2)
            c.restore()
            with Calque(c, alpha * borne(u * 2)):
                c.save(); c.translate(0, 0) if rot == 0 else None
                texte(c, titre, NX + NR + 34 + 30 * (1 - u), y - 50, 54)
                texte(c, sous, NX + NR + 34 + 30 * (1 - u), y + 10, 30, C["gris"], "demi")
                c.restore()
        pU = battement(t, TW(29) - 0.06, 0.12) * battement(t, t_boucle, 0.08)
        noeud(yU, C["vert"], "factory", "Fournisseur", "en Chine", tC0, pulse=pU)
        if aR > 0:
            c.save()
            if uCut > 0: c.translate(NX, RANG["rev"]); c.rotate(rotR); c.translate(-NX, -RANG["rev"])
            pR = battement(t, t_arr, 0.12) * battement(t, t_marge + 0.06, 0.12)
            noeud(yR, C["rouge"], "store", "Revendeur", "l’intermédiaire", tC0 + 0.15, aR, 0, pR)
            # étiquettes « + marge » empilées sur le revendeur
            for k, tt in enumerate([t_boucle + j * 0.24 + 0.12 for j in range(3)]):
                if t >= tt:
                    u = prog(t, tt, 0.25, lambda v: rebond(v, 2.0))
                    pastille_rot(c, "+ MARGE", 400 + k * 165, yR + 112 + (k % 2) * 10, 24, C["rouge"], C["blanc"], [-8, 5, -3][k], mix(0.3, 1, u), aR * borne(u * 2))
            c.restore()
        noeud(yT, C["ink"], "user", "Toi", "le client final", tC0 + 0.3, pulse=battement(t, t_toi + 0.42, 0.12) * battement(t, t_total, 0.1))
        # colis : fournisseur → revendeur → toi
        XC = 840
        if t >= TW(29) - 0.06 and t < t_boucle + 0.05:
            u0 = prog(t, TW(29) - 0.06, 0.35, lambda v: rebond(v, 1.6))
            y = cles(t, [(t_vend, RANG["usine"]), (t_vend + 0.4, RANG["rev"], entreeSortie), (t_toi, RANG["rev"]), (t_toi + 0.42, RANG["toi"], entreeSortie)])
            marge = prog(t, t_marge + 0.04, 0.3, lambda v: rebond(v, 1.6))
            fin = prog(t, t_total - 0.12, 0.16, entree)
            colis(c, mix(XC, NX, fin), y, mix(0.4, 1, u0) * mix(1, 0.3, fin), marge, borne(u0 * 2) * (1 - fin), 4 * math.sin(t * 3))
        # la marge qui saute du revendeur sur le colis
        if t_marge - 0.14 <= t < t_marge + 0.1:
            u = prog(t, t_marge - 0.14, 0.18, entree)
            pastille_rot(c, "+ MARGE", mix(NX + 60, XC, u), mix(RANG["rev"], RANG["rev"] - 40, u), 30, C["rouge"], C["blanc"], mix(-20, 10, u), mix(0.6, 1.2, u), 1)
        # ticket de caisse
        if t >= t_total and t < t_boucle:
            u = prog(t, t_total, 0.3, sortie); a = 1 - prog(t, t_boucle - 0.2, 0.16)
            with Calque(c, a):
                c.save(); c.translate(690, 1236)
                hh = 230 * u
                carte(c, 0, 0, 280, max(1, hh), 18, C["blanc"], 1.0, (12, 28, 0.14))
                c.clipRect(skia.Rect.MakeXYWH(0, 0, 280, hh))
                texte(c, "TICKET", 24, 18, 22, C["gris"], "fort", track=0.1)
                rrect(c, 24, 66, 150, 16, 8, C["ink"]); rrect(c, 24, 100, 90, 16, 8, C["rouge"])
                trait(c, 24, 140, 256, 140, C["ligne"], 3)
                texte(c, "TOTAL", 24, 158, 34)
                rrect(c, 150, 166, 106, 22, 11, C["ink"]); rrect(c, 218, 166, 38, 22, 11, C["rouge"])
                c.restore()
        # « à chaque commande » : trois colis en rafale
        for j in range(3):
            t0 = t_boucle + j * 0.24
            if t0 <= t <= t0 + 0.55:
                y = cles(t, [(t0, RANG["usine"]), (t0 + 0.22, RANG["rev"], entree), (t0 + 0.45, RANG["toi"], sortie)])
                marge = prog(t, t0 + 0.2, 0.08)
                colis(c, XC, y, 0.62, marge, 1 - prog(t, t0 + 0.45, 0.1), 0)
        if t >= t_boucle:
            n = sum(1 for j in range(3) if t >= t_boucle + j * 0.24 + 0.45)
            if n and t < t_cis1:
                pastille_rot(c, f"× {n + 1}", NX + 70, RANG["toi"] - 70, 30, C["ink"], C["blanc"], -8, battement(t, t_boucle + (n - 1) * 0.24 + 0.45, 0.25), 1 - prog(t, t_cis1 - 0.2, 0.2))
        # ciseaux : deux coups, puis le revendeur tombe
        if t_cis1 - 0.35 <= t < t_chute + 0.3:
            yc1 = (RANG["usine"] + RANG["rev"]) / 2; yc2 = (RANG["rev"] + RANG["toi"]) / 2
            y = cles(t, [(t_cis1 - 0.35, yc1 - 200), (t_cis1, yc1, sortie), (t_cis2 - 0.12, yc1), (t_cis2, yc2, entreeSortie)])
            x = cles(t, [(t_cis1 - 0.35, 1150), (t_cis1, NX + 40, sortie)])
            ouvre = 1 if (t < t_cis1 - 0.05 or (t_cis1 + 0.06 < t < t_cis2 - 0.05)) else 0
            a = 1 - prog(t, t_chute + 0.1, 0.2)
            c.save(); c.translate(x, y); c.rotate(180 + 20 * ouvre)
            icone(c, "scissors", 0, 0, 130, C["ink"], 2.2, a)
            c.restore()
        # « EN DIRECT »
        if t >= t_direct:
            u = prog(t, t_direct, 0.4, lambda v: rebond(v, 2.0))
            pastille_rot(c, "EN DIRECT", 640, (yU + yT) / 2, 46, C["vert"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "zap", (16, 40, 0.25))
            confettis(c, 640, (yU + yT) / 2, t, t_direct + 0.05, 24, 360, 3)
            onde(c, 640, (yU + yT) / 2, t, t_direct, 80, 320)
    c.restore()

# ═══════════════════════════════════════════ S5 · Des mois sur place (18,42 → 24,72)
t_pin, t_gz, t_sp = TW(60) - 0.04, TW(61) - 0.02, TW(62) - 0.04
VERBES = [("Chercher", "search", TW(64) - 0.06), ("Commander", "package", TW(66) - 0.06), ("Comparer", "scale", TW(68) - 0.06), ("Trier", "list-filter", TW(71) - 0.06)]
son(18.44, "whoosh", -13); son(18.7, "montee", -20); son(t_pin, "impact_doux", -9); son(t_pin + 0.02, "pop", -14); son(t_gz, "pop", -16); son(t_sp, "pop", -14)
for _, _, tv in VERBES: son(tv, "tampon", -13); son(tv + 0.05, "pop", -15)
son(24.5, "whoosh", -13)
rapide(18.42, 18.72); rapide(24.5, 24.72)
for _, _, tv in VERBES: rapide(tv, tv + 0.12)

_CARTE = chemin_svg(CHINE["d"])

def s5(c, t):
    if not (18.42 <= t <= 24.72): return
    entree_u = prog(t, 18.42, 0.3, sortie); sortie_u = prog(t, 24.5, 0.22, entree)
    c.save(); c.translate(-1300 * sortie_u, 1350 * (1 - entree_u))
    # la carte : zoom sur Guangzhou, puis elle remonte quand les verbes arrivent
    tR = VERBES[0][2] - 0.25
    remonte = prog(t, tR, 0.45, entreeSortie)
    zp = prog(t, 19.0, 0.62, entreeSortie)
    zoom = mix(1.0, 2.5, zp)
    gz = CHINE["guangzhou"]
    centre = (mix(CHINE["largeur"] / 2, gz[0], zp), mix(CHINE["hauteur"] / 2, gz[1], zp))
    # cadre de la carte
    fx, fy, fw, fh = 70, mix(760, 700, remonte), 940, mix(640, 330, remonte)
    carte(c, fx, fy, fw, fh, 44, C["blanc"], 1.0, (22, 50, 0.12))
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(fx, fy, fw, fh), 44, 44), doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(fx, fy, fw, fh), peinture("#F4F8F6"))
    for gx in range(int(fx), int(fx + fw), 60): trait(c, gx, fy, gx, fy + fh, "#E3ECE7", 2, rond=False)
    for gy in range(int(fy), int(fy + fh), 60): trait(c, fx, gy, fx + fw, gy, "#E3ECE7", 2, rond=False)
    # Guangzhou toujours au centre-haut du cadre
    cible = (fx + fw / 2, fy + fh * 0.48)
    base = min((fw - 60) / CHINE["largeur"], (fh - 50) / CHINE["hauteur"]) if remonte < 0.01 else min((940 - 60) / CHINE["largeur"], (640 - 50) / CHINE["hauteur"])
    c.translate(cible[0], cible[1]); c.scale(base * zoom, base * zoom); c.translate(-centre[0], -centre[1])
    c.drawPath(_CARTE, peinture(C["vertDoux"]))
    c.drawPath(_CARTE, peinture(C["vert"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2 / zoom, StrokeJoin=skia.Paint.kRound_Join))
    c.restore()
    # repère Guangzhou
    if t >= t_pin:
        u = prog(t, t_pin, 0.4, lambda v: rebond(v, 1.6))
        px, py = cible[0] + base * zoom * (gz[0] - centre[0]), cible[1] + base * zoom * (gz[1] - centre[1])
        for k in range(3):
            t0 = t_pin + 0.25 + k * 0.45
            while t0 + 1.3 < t: t0 += 1.35
            onde(c, px, py, t, t0, 10, 120, C["vert"], 5, 1.3)
        ombre_sol(c, px, py, 26 * u, 9 * u, 0.25)
        c.save(); c.translate(px, py - 220 * (1 - u))
        disque(c, 0, -62, 30, C["blanc"])
        icone(c, "map-pin", 0, -50, 108, C["vert"], 2.4)
        disque(c, 0, -60, 13, C["vert"])
        c.restore()
        if t >= t_gz:
            u2 = prog(t, t_gz, 0.3, lambda v: rebond(v, 1.8))
            pastille_rot(c, "GUANGZHOU", px + 190, py - 60, 30, C["ink"], C["blanc"], 0, mix(0.4, 1, u2), borne(u2 * 2))
        if t >= t_sp:
            u3 = prog(t, t_sp, 0.3, lambda v: rebond(v, 1.8))
            pastille_rot(c, "SUR PLACE", px + 190, py + 20, 30, C["vert"], C["blanc"], 0, mix(0.4, 1, u3), borne(u3 * 2), "map-pin")
    # les quatre verbes
    for k, (nom, ic, tv) in enumerate(VERBES):
        if t < tv - 0.02: continue
        col, lig = k % 2, k // 2
        x, y = 70 + col * 480, 1080 + lig * 180
        u = prog(t, tv, 0.36, lambda v: rebond(v, 1.9))
        actif = 1 - prog(t, tv + 0.55, 0.3)
        c.save(); c.translate(x + 230, y + 80); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
        with Calque(c, borne(u * 2)):
            fondc = C["vert"] if actif > 0.5 else C["blanc"]
            carte(c, -230, -80, 460, 160, 40, C["blanc"], 1.0, (16, 36, 0.12))
            if actif > 0: rrect(c, -230, -80, 460, 160, 40, C["vert"], actif)
            rrect(c, -200, -50, 100, 100, 28, C["vertDoux"] if actif < 0.5 else C["blanc"], 1.0)
            icone(c, ic, -150, 0, 56, C["vert"], 2.4)
            taille = ajuste(nom, 270, 46)
            texte_centre(c, nom, -60 + largeur(nom, taille) / 2, 0, taille, C["blanc"] if actif > 0.5 else C["ink"])
            if t >= tv + 0.55:
                uu = prog(t, tv + 0.55, 0.3, lambda v: rebond(v, 2.0))
                c.save(); c.translate(200, -62); c.scale(uu, uu)
                disque(c, 0, 0, 26, C["vert"], 1.0, (6, 14, 0.2)); icone(c, "check", 0, 0, 30, C["blanc"], 3.4)
                c.restore()
        c.restore()
    c.restore()

# ═══════════════════════════════════════════ S6+S7 · Deux semaines, des contacts, et le tri (24,55 → 33,95)
t_cal = TW(76) - 0.1; t_jours = TW(77) - 0.08; t_cont = TW(82) - 0.06; t_q = TW(85) - 0.02
CRIT = [("Promesses", "badge-check", TW(90) - 0.06, [1, 3]), ("Qualité", "shield-check", TW(95) - 0.06, [4]), ("Expédition", "truck", TW(99) - 0.06, [2])]
t_fiable = TW(99) + 0.45; t_recul = TW(100) - 0.06
son(24.56, "whoosh", -13); son(t_cal, "whoosh_court", -14)
for k in range(13): son(t_jours + 0.62 * (1 - (1 - k / 13) ** 1.6), "tick", -19)
son(t_jours + 0.66, "pop", -12)
for k in range(5): son(t_cont + k * 0.09, "whoosh_court", -20 - k)
for k in range(5): son(t_q + k * 0.07, "blip", -17)
son(t_q + 0.45, "whoosh", -16)
for nom, ic, tc, out in CRIT:
    son(tc, "swipe", -15); son(tc + 0.3, "blip", -15); son(tc + 0.42, "whoosh_court", -17)
son(t_fiable, "check", -10); son(t_fiable + 0.02, "verre", -15); son(t_recul, "whoosh_long", -14); son(33.78, "whoosh", -13)
rapide(24.55, 24.85); rapide(t_cont, t_cont + 0.5); rapide(t_q + 0.42, t_q + 0.85)
for _, _, tc, _ in CRIT: rapide(tc + 0.38, tc + 0.7)
rapide(33.78, 33.95)
eclair(t_fiable, C["vert"], 0.09)

def carte_contact(c, x, y, w, n, statut, alpha=1.0, rot=0.0, s=1.0, badge=None, ub=0.0):
    c.save(); c.translate(x + w / 2, y + 66); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        carte(c, -w / 2, -66, w, 132, 30, C["blanc"], 1.0, (14, 32, 0.13))
        disque(c, -w / 2 + 70, 0, 40, C["fondDoux"]); icone(c, "user", -w / 2 + 70, 0, 44, C["gris"], 2.2)
        texte(c, f"Fournisseur {n}", -w / 2 + 128, -44, 36)
        coulS = C["ambre"] if statut == "À vérifier" else C["vert"]
        texte(c, statut, -w / 2 + 128, 4, 28, coulS, "fort")
        if badge and ub > 0:
            c.save(); c.translate(w / 2 - 52, 0); c.scale(ub, ub)
            if badge == "?":
                disque(c, 0, 0, 30, C["ambre"]); texte_centre(c, "?", 0, 0, 38, C["blanc"])
            elif badge == "x":
                disque(c, 0, 0, 30, C["rouge"]); icone(c, "x", 0, 0, 34, C["blanc"], 3.4)
            else:
                disque(c, 0, 0, 30, C["vert"]); icone(c, "check", 0, 0, 34, C["blanc"], 3.4)
            c.restore()
    c.restore()

def s6(c, t):
    if not (24.55 <= t <= 33.95): return
    entree_u = prog(t, 24.55, 0.3, sortie); sortie_u = prog(t, 33.78, 0.17, entree)
    recul = prog(t, t_recul, 0.85, entreeSortie)
    cam = mix(1, 0.7, recul) * mix(1, 1.8, sortie_u)
    c.save(); c.translate(540 + 1300 * (1 - entree_u), 1080); c.scale(cam, cam); c.translate(-540, -1080)
    with Calque(c, 1 - sortie_u):
        # calendrier qui défile jusqu'à 14
        dep = prog(t, t_q + 0.4, 0.45, entree)
        if t >= t_cal - 0.02 and dep < 1:
            u = prog(t, t_cal, 0.42, lambda v: rebond(v, 1.6))
            cx, cy = 300 - 900 * dep, 1070
            c.save(); c.translate(cx, cy); c.rotate(-5 + 12 * (1 - u)); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            with Calque(c, borne(u * 2)):
                carte(c, -200, -260, 400, 520, 44, C["blanc"], 1.0, (22, 50, 0.14))
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200, -260, 400, 520), 44, 44), doAntiAlias=True)
                c.drawRect(skia.Rect.MakeXYWH(-200, -260, 400, 120), peinture(C["vert"]))
                c.restore()
                for k in (-90, 90): rrect(c, k - 10, -282, 20, 56, 10, C["ink"])
                texte_centre(c, "SUR PLACE", 0, -200, 34, C["blanc"])
                # compteur à rouleaux
                v = prog(t, t_jours, 0.66, lambda q: 1 - (1 - q) ** 1.6) * 13
                n = int(v); fr = sortie(min(1.0, (v - n) / 0.4))
                c.save(); c.clipRect(skia.Rect.MakeXYWH(-200, -122, 400, 228))
                for kk, yy in ((n, -fr * 220), (n + 1, (1 - fr) * 220)):
                    if kk <= 13:
                        texte_centre(c, str(kk + 1), 0, -10 + yy, 190, C["ink"])
                c.restore()
                texte_centre(c, "JOURS", 0, 150, 40, C["gris"], "fort")
                for k in range(14):
                    on = 1 if k <= v else 0
                    rrect(c, -163 + (k % 7) * 47, 196 + (k // 7) * 30, 38, 22, 7, C["vert"] if on else C["ligne"])
            c.restore()
        # cartes de contacts : en pile, puis en liste, puis triées
        vir = {}
        for _, _, tc, out in CRIT:
            for n in out: vir[n] = tc + 0.4
        if t >= t_cont:
            liste = prog(t, t_q + 0.42, 0.5, entreeSortie)
            def rang_de(n):
                return sum(1 - (prog(t, vir[m] + 0.3, 0.35, entreeSortie) if m in vir else 0) for m in range(1, n))
            for n in range(1, 6):
                k = n - 1
                u = prog(t, t_cont + k * 0.09, 0.4, lambda v: rebond(v, 1.5))
                if u <= 0: continue
                # pile désordonnée
                px, py, pr = 548 - k * 6 + (k % 2) * 12, 820 + k * 72, [-7, 5, -3, 8, -5][k]
                lx, ly = 110, 744 + rang_de(n) * 140
                x = mix(px, lx, liste); y = mix(py, ly, liste); rot = mix(pr, 0, liste)
                xin = mix(700, 0, u)
                badge, ub = None, 0
                if t >= t_q + k * 0.07:
                    badge, ub = "?", prog(t, t_q + k * 0.07, 0.3, lambda v: rebond(v, 2.2))
                al = 1.0
                if n in vir and t >= vir[n] - 0.38:
                    badge, ub = "x", 1.0
                    vv = prog(t, vir[n], 0.35, entree)
                    x += 1100 * vv; rot += 20 * vv; al = 1 - vv
                elif t >= CRIT[0][2] + 0.3:
                    # un critère passé avec succès : coche verte
                    ok = [tc for _, _, tc, out in CRIT if n not in out and t >= tc + 0.3]
                    if ok: badge, ub = "v", prog(t, ok[-1], 0.25, lambda v: rebond(v, 2.0))
                statut = "Fiable" if (n == 5 or n not in vir) and t >= t_fiable else "À vérifier"
                carte_contact(c, x + xin, y, 860 * mix(0.51, 1, liste), n, statut, al * borne(u * 2), rot, 1.0, badge, ub)
            # filtres : trois critères qui s'allument
            for k, (nom, ic, tc, out) in enumerate(CRIT):
                if t < tc - 0.05: continue
                u = prog(t, tc, 0.3, lambda v: rebond(v, 1.9))
                cx = 220 + k * 320
                pastille_rot(c, nom, cx, 690, 30, C["vert"] if t > tc + 0.3 else C["ink"], C["blanc"], 0, mix(0.4, 1, u), borne(u * 2), ic)
                # barre de balayage
                if tc <= t <= tc + 0.4:
                    yy = mix(760, 1500, prog(t, tc, 0.4, entreeSortie))
                    trait(c, 90, yy, 990, yy, C["vert"], 6, 1 - prog(t, tc + 0.3, 0.1))
            if t >= t_fiable:
                u = prog(t, t_fiable, 0.35, lambda v: rebond(v, 2.0))
                pastille_rot(c, "FIABLE", 540, 990, 46, C["vert"], C["blanc"], -5, mix(0.3, 1, u), borne(u * 2), "badge-check", (14, 36, 0.25))
                etincelles(c, 540, 990, t, t_fiable + 0.05, 10, 220)
        # recul : la frise des semaines apparaît autour
        if recul > 0:
            for k in range(26):
                col, lig = k % 13, k // 13
                xx = -240 + col * 120; yy = 1560 + lig * 92
                rrect(c, xx, yy, 96, 72, 18, C["vertDoux"], recul)
                if t > t_recul + 0.2 + k * 0.028:
                    uu = prog(t, t_recul + 0.2 + k * 0.028, 0.18, sortie)
                    rrect(c, xx, yy, 96, 72, 18, C["vert"], recul * uu)
                    icone(c, "check", xx + 48, yy + 36, 40, C["blanc"], 3.2, recul * uu)
            texte_centre(c, "DES SEMAINES DE COMMANDES TEST", 540, 1500, 34, C["vertFonce"], "noir", recul)
    c.restore()

# ═══════════════════════════════════════════ S8 · Les commandes, et « je l'ai fait » (33,80 → 37,30)
T_COM = [TW(105) - 0.04, TW(105) + 0.3, TW(106) + 0.12]
t_fait = TW(111) - 0.06
for tc in T_COM: son(tc + 0.18, "impact", -12)
for k in range(3): son(TW(107) + 0.15 + k * 0.14, "check", -17)
son(t_fait - 0.3, "montee", -14); son(t_fait, "impact", -6); son(t_fait + 0.02, "verre", -9); son(36.92, "whoosh_long", -12)
for tc in T_COM: rapide(tc - 0.02, tc + 0.22)
rapide(t_fait - 0.05, t_fait + 0.2); rapide(36.92, 37.32)
eclair(t_fait + 0.02, C["vert"], 0.1)

def boite(c, cx, cy, nom, w, alpha=1.0, coche=0.0):
    with Calque(c, alpha):
        carte(c, cx - 140, cy - 130, 280, 260, 24, "#F7F2EA", 1.0, (16, 36, 0.18))
        rrect(c, cx - 22, cy - 130, 44, 260, 0, C["vert"], 0.9)
        carte(c, cx - 110, cy - 70, 220, 160, 18, C["blanc"], 1.0, None)
        iw, ih = taille_img(nom); hh = w * ih / iw
        image(c, nom, cx - w / 2, cy + 10 - hh / 2, w)
        texte_centre(c, "COMMANDE TEST", cx, cy + 110, 22, C["ink"], "fort")
        if coche > 0:
            c.save(); c.translate(cx + 120, cy - 120); c.scale(coche, coche)
            disque(c, 0, 0, 36, C["vert"], 1.0, (8, 18, 0.25)); icone(c, "check", 0, 0, 42, C["blanc"], 3.4)
            c.restore()

def s8(c, t):
    if not (33.80 <= t <= 37.30): return
    entree_u = prog(t, 33.80, 0.25, sortie)
    dx, dy = 0, 0
    for tc in T_COM:
        a, b = secousse(t, tc + 0.18, 13); dx += a; dy += b
    a, b = secousse(t, t_fait + 0.1, 18); dx += a; dy += b
    c.save(); c.translate(dx, dy)
    with Calque(c, entree_u):
        sol = 1160
        trait(c, 70, sol + 168, 1010, sol + 168, C["ligne"], 6)
        for k, (nom, w) in enumerate([("moto", 200), ("pull", 120), ("casque", 130)]):
            tc = T_COM[k]
            if t < tc - 0.05: continue
            y = cles(t, [(tc - 0.05, sol - 900), (tc + 0.18, sol, entree), (tc + 0.3, sol - 40, sortie), (tc + 0.42, sol, entree)])
            cx = 220 + k * 320
            dim = 1 - 0.75 * prog(t, t_fait - 0.25, 0.25)
            coche = prog(t, TW(107) + 0.15 + k * 0.14, 0.3, lambda v: rebond(v, 2.0))
            c.save(); c.translate(cx, y); c.scale(1.1, 1.1); c.translate(-cx, -y)
            boite(c, cx, y, nom, w, dim, coche)
            c.restore()
        if t >= t_fait - 0.1:
            u = prog(t, t_fait - 0.1, 0.3, lambda v: rebond(v, 1.7))
            grand = prog(t, 36.92, 0.38, entree)
            r = mix(0, 170, u) * mix(1, 9.5, grand)
            disque(c, 540, 1060, r, C["vert"], 1.0, (20, 60, 0.3) if grand < 0.1 else None)
            if grand < 0.6:
                c.save(); c.translate(540, 1060); c.rotate(mix(-40, 0, u)); c.scale(u * (1 - grand), u * (1 - grand))
                icone(c, "check", 0, 0, 200, C["blanc"], 3.4)
                c.restore()
            onde(c, 540, 1060, t, t_fait + 0.1, 170, 420, C["vert"], 8)
            confettis(c, 540, 1060, t, t_fait + 0.1, 30, 460, 7)
    c.restore()

# ═══════════════════════════════════════════ S9+S10 · ChinaBook, puis le réseau (37,05 → 44,97)
PH = (300, 664, 480, 960)
t_logo = TW(114) - 0.08; t_tel = TW(114) + 0.25; t_cat = TW(117) - 0.04; t_cont2 = TW(119) - 0.04; t_test = TW(122) - 0.04; t_mois = TW(123) - 0.04
t_hub = TW(126) - 0.32; t_four = TW(127) - 0.06; t_trans = TW(129) - 0.06; t_res = TW(130) - 0.02; t_moi = TW(134) - 0.04
son(t_logo - 0.04, "impact", -7); son(t_logo, "verre", -8); son(t_tel, "whoosh_long", -13)
for k in range(3): son(t_cat + k * 0.16, "pop", -16)
for k in range(2): son(t_cont2 + k * 0.15, "pop", -17)
son(t_test, "check", -12); son(t_mois, "pop", -12)
son(t_hub, "whoosh", -14); son(t_hub + 0.32, "pop", -12); son(t_four - 0.1, "swipe", -17); son(t_four, "pop", -12)
son(t_trans - 0.1, "swipe", -17); son(t_trans, "pop", -12)
for k in range(6): son(t_res + 0.1 + k * 0.1, "tick", -18)
son(t_moi, "tampon", -10); son(t_moi + 0.02, "verre", -12); son(44.78, "whoosh", -13)
rapide(t_logo - 0.05, t_logo + 0.18); rapide(t_tel, t_tel + 0.5); rapide(t_hub, t_hub + 0.4); rapide(44.78, 44.97)
eclair(t_moi, C["vert"], 0.08)

def ecran_catalogue(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(C["blanc"]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, mix(h, 170, prog(t, t_tel + 0.5, 0.3, entreeSortie))), peinture(C["vert"]))
    texte(c, "9:41", x + 40, y + 24, 24, C["blanc"], "fort")
    image(c, "logo-tout-blanc", x + 36, y + 92, 230)
    texte(c, "Catalogue", x + 36, y + 196, 46)
    texte(c, "Contacts directs, testés", x + 36, y + 256, 26, C["gris"], "demi")
    cats = [("Mobilité", "électrique", "moto", 170), ("Textile", "", "pull", 96), ("Électronique", "", "casque", 104)]
    for k, (l1, l2, nom, iw) in enumerate(cats):
        u = prog(t, t_cat + k * 0.16, 0.36, sortie)
        if u <= 0: continue
        yy = y + 310 + k * 150; xx = x + 22 + 160 * (1 - u)
        with Calque(c, u):
            rrect(c, xx, yy, w - 44, 134, 28, C["fondDoux"])
            texte(c, l1, xx + 24, yy + (22 if l2 else 30), 30)
            if l2: texte(c, l2, xx + 24, yy + 58, 30)
            rrect(c, xx + 24, yy + 94, 96, 28, 14, C["vertDoux"]); texte_centre(c, "TESTÉ", xx + 72, yy + 108, 16, C["vertFonce"], "fort")
            ih_w, ih_h = taille_img(nom); hh = iw * ih_h / ih_w
            image(c, nom, xx + w - 44 - iw - 20, yy + 67 - hh / 2, iw)
    texte(c, "Contacts directs", x + 36, y + 772, 30, alpha=prog(t, t_cont2 - 0.1, 0.2))
    for k in range(2):
        u = prog(t, t_cont2 + k * 0.15, 0.3, sortie)
        if u <= 0: continue
        yy = y + 818 + k * 74 + 20 * (1 - u)
        with Calque(c, u):
            disque(c, x + 60, yy + 30, 28, C["vertDoux"]); icone(c, "factory", x + 60, yy + 30, 30, C["vert"], 2.2)
            texte(c, "Fournisseur · Guangzhou", x + 102, yy + 8, 24, C["ink"], "fort")
            if t >= t_test + k * 0.1:
                uu = prog(t, t_test + k * 0.1, 0.25, lambda v: rebond(v, 2.0))
                c.save(); c.translate(x + w - 50, yy + 30); c.scale(uu, uu); icone(c, "badge-check", 0, 0, 40, C["vert"], 2.4); c.restore()

def s9(c, t):
    if not (37.05 <= t <= 44.97): return
    sortie_u = prog(t, 44.78, 0.19, entree)
    c.save(); c.translate(1300 * sortie_u, 0)
    # plein écran vert hérité de la coche, qui se rétracte dans l'écran du téléphone
    retr = prog(t, t_tel, 0.5, entreeSortie)
    x, y, w, h = PH
    ex, ey, ew, eh = x + 14, y + 14, w - 28, h - 28
    rx = mix(0, ex, retr); ry = mix(0, ey, retr); rw = mix(W, ew, retr); rh = mix(H, eh, retr); rr = mix(0, 60, retr)
    hub = prog(t, t_hub, 0.4, entreeSortie)
    if t < t_tel + 0.5:
        if retr > 0:
            u = retr
            with Espace(c, 540, 1120, ry=mix(-25, 0, u), s=1):
                carte(c, mix(-40, x, u), mix(-40, y, u), mix(W + 80, w, u), mix(H + 80, h, u), mix(0, 74, u), C["ink"], 1.0, (40, 90, 0.28 * u))
        rrect(c, rx, ry, rw, rh, rr, C["vert"])
        # logo blanc qui claque
        if t >= t_logo - 0.04:
            u = prog(t, t_logo, 0.3, lambda v: rebond(v, 1.5))
            lw = mix(1.6, 1, u) * mix(760, 230, retr)
            lx = mix(540 - lw / 2, ex + 36, retr); ly = mix(980, ey + 92, retr)
            image(c, "logo-tout-blanc", lx, ly, lw, borne(u * 3))
    else:
        if hub < 1:
            sway = 2.5 * math.sin((t - t_tel) * 1.6)
            s = mix(1, 0.24, hub); yy = mix(0, -420, hub)
            with Calque(c, 1 - prog(t, t_hub + 0.25, 0.15)):
                with Espace(c, 540, 1120 + yy, ry=sway * (1 - hub), s=s):
                    telephone(c, x, y + yy, w, h, lambda cc, a, b, d, e: ecran_catalogue(cc, a, b, d, e, t), t)
            # bulles produits autour du téléphone
            for k, (nom, iw, bx, by) in enumerate([("moto", 96, 170, 900), ("pull", 70, 910, 1010), ("casque", 76, 160, 1260)]):
                u = prog(t, t_cat + 0.1 + k * 0.12, 0.35, lambda v: rebond(v, 1.8)) * (1 - hub)
                if u <= 0: continue
                bob = 10 * math.sin(t * 2.2 + k)
                c.save(); c.translate(bx, by + bob); c.scale(u, u)
                disque(c, 0, 0, 72, C["blanc"], 1.0, (12, 30, 0.14))
                iw_, ih_ = taille_img(nom); hh = iw * ih_ / iw_
                image(c, nom, -iw / 2, -hh / 2, iw)
                c.restore()
            if t >= t_mois:
                u = prog(t, t_mois, 0.35, lambda v: rebond(v, 1.8)) * (1 - hub)
                pastille_rot(c, "TESTÉS PENDANT DES MOIS", 640, 1430, 28, C["vert"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "badge-check", (14, 36, 0.25))
    # le réseau
    if t >= t_hub + 0.2:
        hx, hy = 540, 780
        u = prog(t, t_hub + 0.2, 0.35, lambda v: rebond(v, 1.7))
        nodes = [("Fournisseurs", "Validés, vérifiés", "factory", 280, 1060, t_four), ("Transitaire", "Logistique", "ship", 790, 1060, t_trans)]
        for titre, sous_, ic, nx, ny, tn in nodes:
            if t < tn - 0.12: continue
            ul = prog(t, tn - 0.12, 0.3, sortie)
            trait(c, hx, hy + 60, mix(hx, nx, ul), mix(hy + 60, ny - 110, ul), C["vert"], 8, 1, (2, 18))
            un = prog(t, tn, 0.36, lambda v: rebond(v, 1.8))
            c.save(); c.translate(nx, ny); c.scale(mix(0.3, 1, un), mix(0.3, 1, un))
            with Calque(c, borne(un * 2)):
                carte(c, -200, -110, 400, 220, 40, C["blanc"], 1.0, (18, 40, 0.13))
                disque(c, 0, -32, 50, C["vertDoux"]); icone(c, ic, 0, -32, 58, C["vert"], 2.3)
                texte_centre(c, titre, 0, 46, ajuste(titre, 360, 40), C["ink"])
                texte_centre(c, sous_, 0, 86, 24, C["gris"], "demi")
            c.restore()
        # nœuds secondaires
        sec = [("bike", 130, 1330), ("shirt", 300, 1290), ("headphones", 450, 1370), ("package", 630, 1370), ("truck", 780, 1290), ("user", 950, 1330)]
        for k, (ic, nx, ny) in enumerate(sec):
            tk = t_res + 0.1 + k * 0.1
            if t < tk - 0.1: continue
            src = (280, 1170) if k < 3 else (800, 1170)
            ul = prog(t, tk - 0.1, 0.25)
            trait(c, src[0], src[1], mix(src[0], nx, ul), mix(src[1], ny, ul), C["vertMoyen"], 4)
            un = prog(t, tk, 0.3, lambda v: rebond(v, 2.0)) * battement(t, t_moi + k * 0.04, 0.2)
            c.save(); c.translate(nx, ny); c.scale(un, un)
            disque(c, 0, 0, 48, C["blanc"], 1.0, (10, 24, 0.14)); icone(c, ic, 0, 0, 46, C["vert"], 2.3)
            c.restore()
        # moyeu ChinaBook
        c.save(); c.translate(hx, hy); s = mix(0.4, 1, u) * battement(t, t_moi, 0.12); c.scale(s, s)
        with Calque(c, borne(u * 2)):
            carte(c, -230, -70, 460, 140, 70, C["blanc"], 1.0, (18, 44, 0.16))
            image(c, "logo", -170, -37, 340)
        c.restore()
        if t >= t_moi:
            uu = prog(t, t_moi - 0.1, 0.18, entree)
            c.save(); c.translate(820, 690); c.rotate(-10); c.scale(mix(2.4, 1, uu), mix(2.4, 1, uu))
            with Calque(c, uu):
                rrect(c, -170, -48, 340, 96, 22, C["blanc"], 0.95, None, C["vert"], 7)
                texte_centre(c, "MOI-MÊME", 0, 0, 44, C["vert"])
            c.restore()
    c.restore()

# ═══════════════════════════════════════════ S11 · Contacter, négocier, commander (44,80 → 49,45)
B1 = TW(136) - 0.04; B2 = B1 + 0.34; BT = B1 + 0.66; B3 = TW(139) - 0.24; B4 = TW(140) - 0.04; B5 = TW(141); BO = TW(144) - 0.06; BD = TW(145) - 0.04
son(44.82, "whoosh", -13); son(B1, "message", -11); son(B2, "message", -14); son(BT, "frappe", -21); son(B3, "message_in", -11)
son(B4, "message", -11); son(B5, "message_in", -11); son(BO - 0.06, "swipe", -15); son(BO, "pop", -11); son(BD - 0.05, "tampon", -7); son(BD, "verre", -11)
son(49.25, "whoosh_bas", -14)
rapide(44.80, 45.12); rapide(BD - 0.12, BD + 0.05); rapide(49.25, 49.45)
eclair(BD, C["vert"], 0.1)

def bulle(c, txt, droite, xs, y, w_ecran, t, t0, fond_, coul):
    if t < t0 - 0.02: return 0
    lignes = txt.split("\n")
    tw = max(largeur(l, 26, "demi", 0) for l in lignes)
    bw, bh = tw + 44, len(lignes) * 34 + 30
    x = xs + w_ecran - 26 - bw if droite else xs + 26
    u = prog(t, t0, 0.32, lambda v: rebond(v, 1.8))
    c.save(); c.translate(x + (bw if droite else 0), y + bh); c.scale(mix(0.3, 1, u), mix(0.3, 1, u)); c.translate(-(x + (bw if droite else 0)), -(y + bh))
    with Calque(c, borne(u * 2)):
        rrect(c, x, y, bw, bh, 28, fond_)
        for k, l in enumerate(lignes):
            texte(c, l, x + 22, y + 15 + k * 34, 26, coul, "demi", track=0)
    c.restore()
    return bh

def ecran_chat(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#F4F7F5"))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 150), peinture(C["blanc"]))
    trait(c, x, y + 150, x + w, y + 150, C["ligne"], 2, rond=False)
    disque(c, x + 62, y + 96, 34, C["vertDoux"]); icone(c, "factory", x + 62, y + 96, 36, C["vert"], 2.2)
    texte(c, "Fournisseur", x + 112, y + 68, 30)
    texte(c, "Échange illustratif", x + 112, y + 106, 21, C["ambre"], "fort")
    bulle(c, "Bonjour !\nCe modèle est dispo ?", True, x, y + 176, w, t, B1, C["vert"], C["blanc"])
    if t >= B2 - 0.02:
        u = prog(t, B2, 0.3, lambda v: rebond(v, 1.8))
        c.save(); c.translate(x + w - 26 - 110, y + 370); c.scale(u, u)
        rrect(c, -110, -80, 220, 160, 26, C["blanc"], 1.0, None, C["ligne"], 2)
        image(c, "moto", -92, -66, 184)
        c.restore()
    if BT <= t < B3:
        rrect(c, x + 26, y + 470, 100, 60, 30, C["blanc"])
        for k in range(3):
            disque(c, x + 54 + k * 22, y + 500 - 8 * max(0, math.sin((t - BT) * 12 - k)), 7, C["grisClair"])
    bulle(c, "Oui, en stock.\nQuelle quantité ?", False, x, y + 470, w, t, B3, C["blanc"], C["ink"])
    bulle(c, "On peut discuter\ndu prix ?", True, x, y + 584, w, t, B4, C["vert"], C["blanc"])
    bulle(c, "Oui, on en parle.", False, x, y + 698, w, t, B5, C["blanc"], C["ink"])
    if t >= BO - 0.02:
        u = prog(t, BO, 0.36, sortie)
        yy = y + 770 + 160 * (1 - u)
        with Calque(c, u):
            carte(c, x + 22, yy, w - 44, 120, 26, C["blanc"], 1.0, (10, 24, 0.12))
            disque(c, x + 82, yy + 60, 34, C["vert"]); icone(c, "check", x + 82, yy + 60, 38, C["blanc"], 3.4)
            texte(c, "Commande envoyée", x + 134, yy + 26, 28)
            texte(c, "Direct fournisseur", x + 134, yy + 66, 22, C["gris"], "demi")

def s11(c, t):
    if not (44.80 <= t <= 49.45): return
    entree_u = prog(t, 44.80, 0.32, sortie); sortie_u = prog(t, 49.25, 0.2, entree)
    x, y, w, h = PH
    dx, dy = secousse(t, BD + 0.05, 14)
    c.save(); c.translate(dx - 1300 * (1 - entree_u), dy + 1300 * sortie_u)
    with Espace(c, 540, 1120, ry=mix(-30, 0, entree_u) + 2 * math.sin(t * 1.3), rz=mix(-8, 0, entree_u)):
        telephone(c, x, y, w, h, lambda cc, a, b, d, e: ecran_chat(cc, a, b, d, e, t), t)
    if t >= BD - 0.12:
        u = prog(t, BD - 0.12, 0.16, entree)
        c.save(); c.translate(760, 1330); c.rotate(-10); c.scale(mix(2.6, 1, u), mix(2.6, 1, u))
        with Calque(c, u):
            rrect(c, -190, -60, 380, 120, 24, C["blanc"], 0.95, None, C["vert"], 8)
            texte_centre(c, "EN DIRECT", 0, 0, 56, C["vert"])
        c.restore()
        confettis(c, 760, 1330, t, BD + 0.04, 22, 340, 11)
    c.restore()

# ═══════════════════════════════════════════ S12 · Reprendre le contrôle (49,25 → 53,48)
t_cata = TW(148) - 0.1; t_sw = TW(155) - 0.06
son(49.28, "swipe", -15)
for k in range(6): son(t_cata + k * 0.11, "pop", -17)
son(TW(151) - 0.1, "whoosh", -15); son(t_sw, "clic", -7); son(t_sw + 0.04, "impact_doux", -12); son(t_sw + 0.1, "verre", -11); son(53.3, "whoosh", -13)
rapide(t_sw - 0.02, t_sw + 0.28); rapide(53.28, 53.48)
eclair(t_sw + 0.08, C["vert"], 0.12)

def s12(c, t):
    if not (49.25 <= t <= 53.48): return
    entree_u = prog(t, 49.25, 0.3, sortie); sortie_u = prog(t, 53.28, 0.2, entree)
    cam = mix(1, 1.7, sortie_u)
    c.save(); c.translate(540, 1080); c.scale(cam, cam); c.translate(-540, -1080 - 300 * (1 - entree_u))
    with Calque(c, entree_u * (1 - sortie_u)):
        # le catalogue qui grandit (« développer ton business »)
        monte = prog(t, TW(151) - 0.1, 0.45, entreeSortie)
        tuiles = [("moto", None), ("pull", None), ("casque", None), (None, "bike"), (None, "shirt"), (None, "headphones")]
        for k, (img, ic) in enumerate(tuiles):
            tk = t_cata + k * 0.11
            if t < tk - 0.02: continue
            u = prog(t, tk, 0.32, lambda v: rebond(v, 1.9))
            col, lig = k % 3, k // 3
            tx = 90 + col * 310 + 150; ty = mix(820 + lig * 230, 700 + lig * 0 + col * 0, 0) - 120 * monte
            s = mix(0.3, 1, u) * mix(1, 0.62, monte)
            ty = mix(820 + lig * 230, 760 + lig * 150, monte)
            tx = mix(90 + col * 310 + 150, 255 + col * 285, monte)
            c.save(); c.translate(tx, ty); c.scale(s, s)
            with Calque(c, borne(u * 2) * mix(1, 0.35, prog(t, t_sw, 0.3))):
                carte(c, -140, -100, 280, 200, 34, C["blanc"] if img else C["vertDoux"], 1.0, (14, 32, 0.12))
                if img:
                    iw_, ih_ = taille_img(img); ww = {"moto": 210, "pull": 120, "casque": 130}[img]; hh = ww * ih_ / iw_
                    image(c, img, -ww / 2, -hh / 2, ww)
                else:
                    icone(c, ic, 0, 0, 90, C["vert"], 2.2)
            c.restore()
        # l'interrupteur géant
        if monte > 0:
            u = prog(t, TW(151) - 0.05, 0.4, lambda v: rebond(v, 1.6))
            sw = prog(t, t_sw, 0.34, lambda v: rebond(v, 1.5))
            col = C["rouge"] if sw < 0.5 else C["vert"]
            c.save(); c.translate(540, 1210); s = mix(0.4, 1, u) * battement(t, t_sw + 0.1, 0.06); c.scale(s, s)
            with Calque(c, borne(u * 2)):
                tw_, th = 700, 230
                rrect(c, -tw_ / 2, -th / 2, tw_, th, th / 2, C["rouge"], 1.0, (20, 50, 0.18))
                if sw > 0: rrect(c, -tw_ / 2, -th / 2, tw_, th, th / 2, C["vert"], borne(sw * 1.2))
                kx = mix(-tw_ / 2 + th / 2, tw_ / 2 - th / 2, sw)
                disque(c, kx, 0, th / 2 - 18, C["blanc"], 1.0, (10, 30, 0.25))
                icone(c, "x" if sw < 0.5 else "check", kx, 0, 90, col, 3.2)
                la = 1 - borne(sw * 1.6); lb = borne(sw * 1.6 - 0.4)
                texte_centre(c, "INTERMÉDIAIRE", 100, 0, 44, C["blanc"], alpha=la)
                texte_centre(c, "DIRECT", -90, 0, 64, C["blanc"], alpha=lb)
            c.restore()
            etincelles(c, 540 + 230, 1210, t, t_sw + 0.2, 10, 220)
            confettis(c, 540, 1210, t, t_sw + 0.15, 20, 380, 5)
    c.restore()

# ═══════════════════════════════════════════ S13 · Appel à l'action et carton final (53,30 → 59,40)
LETTRES = "CHINA"
TL = [TW(160) - 0.22 + k * 0.09 for k in range(5)]
t_env = TW(162) - 0.02; t_rep = TW(165) - 0.06; t_chips = TW(167) - 0.04; t_fin = 57.86
son(53.32, "pop", -13)
for tl_ in TL: son(tl_, "frappe", -13)
son(t_env, "clic", -10); son(t_env + 0.04, "whoosh_court", -13); son(t_env + 0.16, "message", -10)
son(t_rep - 0.45, "frappe", -21); son(t_rep, "message_in", -10)
for k in range(3): son(t_chips + k * 0.12, "pop", -15)
son(t_fin, "whoosh", -13); son(t_fin + 0.14, "impact_doux", -8); son(t_fin + 0.16, "verre", -8); son(t_fin + 0.36, "pop", -11)
rapide(53.30, 53.6); rapide(t_env, t_env + 0.32); rapide(t_fin, t_fin + 0.36)
eclair(t_fin + 0.14, C["vert"], 0.10)

def ecran_whatsapp(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#EEF3F0"))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 150), peinture(C["vert"]))
    disque(c, x + 62, y + 96, 34, C["blanc"])
    image(c, "logo-marque", x + 62 - 19, y + 96 - 20, 38)
    texte(c, "ChinaBook", x + 112, y + 66, 30, C["blanc"])
    texte(c, "en ligne", x + 112, y + 104, 22, C["vertDoux"], "demi")
    # champ de saisie
    rrect(c, x + 20, y + h - 92, w - 120, 66, 33, C["blanc"])
    xs = x + 46
    if t < TL[0]:
        texte(c, "Message", xs, y + h - 92 + (66 - hauteurLigne(28, "moyen")) / 2, 28, C["grisClair"], "moyen")
    elif t < t_env + 0.04:
        xl = xs
        for k, l in enumerate(LETTRES):
            if t >= TL[k]:
                u = prog(t, TL[k], 0.12, sortie)
                texte(c, l, xl, y + h - 92 + (66 - hauteurLigne(32)) / 2 - 8 * (1 - u), 32, C["ink"], alpha=u)
                xl += largeur(l, 32)
        if int(t * 4) % 2 == 0: rrect(c, xl + 3, y + h - 76, 3, 34, 1.5, C["vert"])
    sb = battement(t, t_env - 0.04, -0.18, 0.25)
    c.save(); c.translate(x + w - 60, y + h - 59); c.scale(sb, sb)
    disque(c, 0, 0, 33, C["vert"]); icone(c, "send", 0, 0, 32, C["blanc"], 2.4)
    c.restore()
    if t >= t_env:
        u = prog(t, t_env, 0.34, sortie)
        bw = largeur("CHINA", 40) + 60
        bx = x + w - 26 - bw; by = mix(y + h - 92, y + 600, u)
        with Calque(c, u):
            rrect(c, bx, by, bw, 80, 28, C["vert"])
            texte_centre(c, "CHINA", bx + bw / 2, by + 40, 40, C["blanc"])
    if t_rep - 0.45 <= t < t_rep:
        rrect(c, x + 26, y + 700, 100, 60, 30, C["blanc"])
        for k in range(3):
            disque(c, x + 54 + k * 22, y + 730 - 8 * max(0, math.sin((t - t_rep) * 12 - k)), 7, C["grisClair"])
    bulle(c, "Voici le pack adapté\nà ce que tu veux vendre.", False, x, y + 700, w, t, t_rep, C["blanc"], C["ink"])
    for k, (nom, iw) in enumerate([("moto", 104), ("pull", 54), ("casque", 60)]):
        tk = t_chips + k * 0.12
        if t < tk - 0.02: continue
        u = prog(t, tk, 0.3, lambda v: rebond(v, 2.0))
        cx = x + 26 + 64 + k * 140; cy = y + 860
        c.save(); c.translate(cx, cy); c.scale(u, u)
        rrect(c, -64, -40, 128, 80, 20, C["blanc"], 1.0, None, C["vertMoyen"], 3)
        iw_, ih_ = taille_img(nom); hh = iw * ih_ / iw_
        image(c, nom, -iw / 2, -hh / 2, iw)
        c.restore()

def s13(c, t):
    if t < 53.30: return
    x, y, w, h = PH
    entree_u = prog(t, 53.30, 0.36, lambda v: rebond(v, 1.4)); part = prog(t, t_fin, 0.36, entree)
    if part < 1:
        c.save(); c.translate(0, 1200 * part)
        with Espace(c, 540, 1120, rz=mix(8, 0, borne(entree_u)), s=mix(0.7, 1, entree_u)):
            with Calque(c, borne(entree_u * 2) * (1 - part)):
                telephone(c, x, y, w, h, lambda cc, a, b, d, e: ecran_whatsapp(cc, a, b, d, e, t), t)
        confettis(c, 760, 1220, t, t_env + 0.36, 16, 280, 13)
        c.restore()
    if t >= t_fin + 0.05:
        u = prog(t, t_fin + 0.05, 0.4, sortie)
        disque(c, 540, 1060, 420 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
        ul = prog(t, t_fin + 0.12, 0.36, lambda v: rebond(v, 1.6))
        lw = 760 * mix(0.6, 1, ul)
        iw_, ih_ = taille_img("logo"); lh = lw * ih_ / iw_
        image(c, "logo", 540 - lw / 2, 960 - lh / 2, lw, borne(ul * 2))
        ub = prog(t, t_fin + 0.36, 0.36, lambda v: rebond(v, 1.8))
        if ub > 0:
            s = mix(0.4, 1, ub) * (1 + 0.035 * max(0, math.sin((t - t_fin - 0.8) * 5)) if t > t_fin + 0.8 else mix(0.4, 1, ub))
            c.save(); c.translate(540, 1170); c.scale(s, s)
            pastille(c, "Envoie « CHINA » sur WhatsApp", 0, 0, 40, C["vert"], C["blanc"], "message-circle", borne(ub * 2), (18, 46, 0.3))
            c.restore()
        etincelles(c, 540, 1170, t, t_fin + 0.5, 12, 380)

# ─────────────────────────────────────────── composition d'une image
SCENES = [s1, s2, s3, s5, s6, s8, s9, s11, s12, s13]

def eclairs(c, t):
    for t0, coul, a in ECLAIRS:
        if t0 - 0.02 <= t <= t0 + 0.5:
            u = (t - t0 + 0.02) / 0.52
            al = a * (1 - u) ** 2 if u > 0.08 else a * u / 0.08
            c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), peinture(coul, al))

def dessine(c, t):
    fond(c, t)
    bandeau(c, t)
    for s in SCENES:
        s(c, t)
    eclairs(c, t)
    sous_titres(c, t)
