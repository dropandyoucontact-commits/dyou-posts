"""DA-M07 « 3 secondes » en 16:9, VERSION ANGLAISE (voix Tomy en anglais) — film de /en/motion-design/ de dyou-agency.com.

Même voix, même texte et même minutage que DA-M07 (vertical) ; toutes les scènes sont recomposées pour l'écran
large : le titre à gauche, l'objet à droite, les interfaces en largeur, les sous-titres fins en bas.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio import SousTitresEncre
import studio
studio.TIMELINE_NOMS = ["Title", "Shapes", "Text", "Sound"]

DUREE = 26.9
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

M = dict(b1=TW(12), produit=TW(16), service=TW(18), message=TW(22), oblige=TW(24), page=TW(27), b2=TW(29), motion=TW(30),
         captive=TW(33), regarde=TW(37), comprend=TW(38), action=TW(43), b3=TW(45), titre_b3="THE DIFFERENCE", attention=TW(50),
         demandes=TW(52), clients=TW(54), b4=TW(55), site=TW(58), expliquer=TW(60), facon=TW(61), simple=TW(64),
         long_texte=TW(65), b5=TW(70), script=TW(73), anime=TW(75), accroches=TW(79), tester=TW(82), prix=TW(84),
         deux=TW(85), qvd=TW(87), euros=TW(88), devis=TW(89), url=TW(93))
SOUS = SousTitresEncre(K, fusions={(4, 5): "3 seconds.", (85, 86, 87, 88): "€290.", (93, 94, 95, 96, 97): "dyou-agency.com."},
                       y=968, larg=1500, taille=44, fam="fort", max_mots=7)

T_2, T_1 = TW(6) - 0.05, TW(7) - 0.05
T_SW = TW(8) - 0.1
T_SNAP = TW(9) - 0.1
T_B1 = TW(12)
CX, CY = 960, 470            # centre de la zone utile (les sous-titres occupent le bas)


# ═══════════════════════════════════════════ HOOK
def compte(c, t):
    """à gauche l'anneau qui se vide et le compte à rebours ; à droite « Ton client · 3 SECONDES »"""
    cx, cy, R = 600, 470, 290
    a = entre(t, -0.35, 0.5, 1.4)
    lueur_s(c, cx, cy, 520, S["violetVif"], 0.18)
    anneau(c, cx, cy, R, S["lavande"], 34)
    rest = 1 - borne(t / (T_SW + 0.1))
    arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), -90, -360 * rest)
    cols = GRAD_VIF if t < T_1 else [S["rouge"], "#FF7A59", S["rouge"]]
    pa = pgrad(cx - R, cy - R, cx + R, cy + R, cols); pa.setStyle(skia.Paint.kStroke_Style); pa.setStrokeWidth(34); pa.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawPath(arc, pa)
    ang = math.radians(-90 - 360 * rest)
    disque(c, cx + R * math.cos(ang), cy + R * math.sin(ang), 24, "#FFFFFF", 1.0, (6, 16, 0.2))
    for j in range(12):
        aa = j * math.pi / 6
        trait(c, cx + (R - 54) * math.cos(aa), cy + (R - 54) * math.sin(aa), cx + (R - 70) * math.cos(aa), cy + (R - 70) * math.sin(aa), S["grisClair"], 4)
    taille = 360
    for (n, t_on, t_off) in [("3", -9, T_2), ("2", T_2, T_1), ("1", T_1, 99)]:
        if t < t_on - 0.01 or t > t_off + 0.25: continue
        u = prog(t, t_on, 0.3, sortieExpo) if t_on > 0 else a
        o = prog(t, t_off, 0.22, entree)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(cx - 230, cy - 220, 460, 440))
        flou_calque(c, 10 * o + 8 * (1 - min(1, u * 1.5)), (1 - o))
        texte_grad(c, n, cx, cy - hauteurLigne(taille) / 2 + 300 * (1 - u) - 300 * o, taille, "noir", "centre", -0.04,
                   cols=GRAD if n != "1" else [S["rouge"], "#FF7A59"])
        c.restore(); c.restore()
    b = entre(t, TW(1) - 0.1, 0.4, 2.2)
    pill(c, "Your customer", 1330, 250, 34, "blanc", "eye", borne(b * 3), mix(0.4, 1, b), rot=-3)
    lettres(c, "3", 1330, 330, 220, t, TW(4) - 0.15, "ressort", decal=0.03)
    lettres(c, "SECONDS", 1330, 560, 120, t, TW(5) - 0.2, "masque", decal=0.03, duree=0.4)
    # la jauge du temps qui file sous le titre
    u = borne(t / (T_SW + 0.1))
    if t > TW(5):
        barre_progression(c, 1070, 740, 520, u, 14, GRAD_VIF if t < T_1 else [S["rouge"], "#FF7A59"], alpha=prog(t, TW(5), 0.3))


FORMES = [(0, "rond"), (1, "carre"), (2, "etoile"), (3, "anneau"), (4, "rond"), (5, "carre"), (6, "etoile"), (7, "anneau"),
          (8, "etoile"), (9, "rond"), (10, "carre"), (11, "anneau")]


def ca_bouge(c, t):
    t0 = T_SNAP + 0.05
    rayons(c, CX, CY, t, 1500, 0.10 * prog(t, t0, 0.4), 18, S["violetVif"])
    lueur_s(c, CX, CY, 760, S["violetVif"], 0.25 * prog(t, t0, 0.4))
    for k, forme in FORMES:
        a = entre(t, t0 + 0.035 * k, 0.5, 1.8)
        if a <= 0: continue
        ang = t * (1.4 + 0.12 * k) + k * math.pi / 6
        R = mix(60, 640 + 40 * (k % 3), sortie(min(1, a)))
        x, y = CX + R * math.cos(ang), CY + R * 0.52 * math.sin(ang)
        col = [S["violetVif"], S["bleuVif"], S["or_"], S["violet"]][k % 4]
        c.save(); c.translate(x, y); c.rotate(t * 120 * (-1) ** k)
        if forme == "rond": c.drawCircle(0, 0, 32, pgrad(-32, -32, 32, 32, GRAD_VIF))
        elif forme == "carre": rrect(c, -30, -30, 60, 60, 15, col)
        elif forme == "etoile": etoile4(c, 0, 0, 44, col)
        else: anneau(c, 0, 0, 32, col, 10)
        c.restore()
    o = t0 + max(0.0, math.floor((t - t0 - 0.5) / 0.45)) * 0.45 + 0.5
    lettres(c, "IT MOVES", CX, 330, 250, t, t0, "ressort", decal=0.05, onde_t=o)
    for k in range(6):
        u = prog(t, t0 + 0.05 * k, 0.4, sortie)
        if 0 < u < 1:
            yy = 300 + 70 * k
            trait(c, mix(140, 60, u), yy, mix(140, 60, u) + 220 * (1 - u), yy, S["violetVif"], 6, 1 - u)
            trait(c, mix(1780, 1860, u), yy + 35, mix(1780, 1860, u) - 220 * (1 - u), yy + 35, S["bleuVif"], 6, 1 - u)
    eclats(c, CX, CY, t, t0, 22, 820, graine=6, duree=0.9)
    onde(c, CX, CY, t, t0, 150, 980, S["violetVif"], 12, 0.6)


def pub_grise(c, t, y0):
    """le post suivant du fil : une pub grise, plate (format paysage)"""
    c.save(); c.translate(0, y0)
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), peinture("#E7E5EB"))
    rrect(c, 160, 130, 900, 640, 26, "#D3D0D9"); icone(c, "image", 610, 450, 160, "#B3AFBB", 1.4)
    disque(c, 1190, 180, 44, "#C9C5D0"); rrect(c, 1252, 152, 240, 22, 11, "#C9C5D0"); texte(c, "Sponsored", 1252, 186, 24, "#9B96A5", "demi", track=0)
    texte(c, "SALE -10%", 1150, 300, 76, "#8A8594", "noir", track=0)
    for k in range(3): rrect(c, 1150, 430 + 46 * k, [560, 480, 360][k], 22, 11, "#CFCBD6")
    rrect(c, 1150, 640, 300, 84, 42, "#CFCBD6")
    c.restore()


def hook(c, t):
    sw = prog(t, T_SW, 0.34, sortieExpo)
    back = prog(t, T_SNAP, 0.7, lambda v: ressort(v, 1.4, 4.2)) if t >= T_SNAP else 0.0
    dy = -1150 * sw * (1 - back)
    sx, sy = secousse(t, T_SNAP + 0.05, 22)
    c.save(); c.translate(sx, dy + sy)
    if t < T_SNAP: compte(c, t)
    else: ca_bouge(c, t)
    c.restore()
    if T_SW <= t < T_SNAP + 0.5:
        gy = H + dy if t < T_SNAP else H * prog(t, T_SNAP, 0.32, entree) + (-1150 * sw + H) * (1 - prog(t, T_SNAP, 0.32, entree))
        pub_grise(c, t, gy)
    f = prog(t, T_SW - 0.22, 0.5, entreeSortie)
    if 0 < f < 1:
        hy = mix(900, 300, f); al = math.sin(math.pi * f)
        carte_s(c, 1700 - 64, hy - 64, 128, 128, 64, "#FFFFFF", None, 0.2, al)
        icone(c, "hand", 1700, hy, 66, S["encre"], 2.2, al)
        for k in range(3): trait(c, 1700, hy + 90 + 40 * k, 1700, hy + 120 + 40 * k, S["violetVif"], 5, 0.5 * al * (1 - k / 3))


# ═══════════════════════════════════════════ B1 « Aujourd'hui… il faut être à la page »
def scene_b1(c, t):
    g = Groupe(c, t, M["b1"] - 0.12, M["b2"] - 0.05, ent="zoom", sor="gauche", d_out=0.32, cy=CY)
    if not g.visible: return
    with g:
        so = prog(t, M["page"] - 0.25, 0.3, entreeSortie)
        lettres(c, "TODAY,", CX, 70 - 40 * so, 110, t, M["b1"] - 0.08, "ressort", decal=0.03, alpha=1 - so)
        cartes = [("A product", "package", M["produit"], -1), ("A service", "briefcase", M["service"], 0), ("Your message", "megaphone", M["message"], 1)]
        serre = prog(t, M["oblige"] - 0.1, 0.45, entreeSortie)
        for k, (lab, ic, t0, pos) in enumerate(cartes):
            a = entre(t, t0 - 0.12, 0.5, 1.4)
            if a <= 0: continue
            x = mix(CX + pos * 400, 330 + 0 * pos, serre) + pos * 26 * serre
            y = 500 + 20 * math.sin(t * 2.4 + k) * (1 - serre) + pos * 40 * serre
            with Espace(c, x, y, ry=mix(-95, 0, a) + 8 * pos * (1 - serre), rz=pos * 8 * serre, s=mix(1, 0.78, serre)):
                with Calque(c, borne(a * 3) * (1 - 0.3 * so)):
                    carte_s(c, x - 160, y - 185, 320, 370, 38)
                    yy = y - 60
                    if ic == "package": yy += -18 * abs(math.sin((t - t0) * 5)) * (1 - serre)
                    tuile(c, ic, x, yy, 130, rot=(8 * math.sin((t - t0) * 6) if ic == "briefcase" else 0) * (1 - serre))
                    if ic == "megaphone":
                        for j in range(3):
                            ph = ((t - t0) * 1.6 + j / 3) % 1
                            p = skia.Path(); r = 70 + 50 * ph
                            p.addArc(skia.Rect.MakeXYWH(x + 20 - r, yy - r, 2 * r, 2 * r), -35, 70)
                            c.drawPath(p, peinture(S["violetVif"], (1 - ph) * 0.8, Style=skia.Paint.kStroke_Style, StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap))
                    texte(c, lab, x, y + 74, 38, S["encre"], "titre", "centre", -0.02)
                    rrect(c, x - 70, y + 134, 140, 10, 5, S["lavande"])
        # « à la page » : la page se rabat en 3D à droite des cartes resserrées
        a = prog(t, M["page"] - 0.22, 0.55, lambda v: rebond(v, 1.3))
        if a > 0:
            cx, cy = 1180, 470
            with Espace(c, cx, cy - 220, rx=mix(-100, 0, a)):
                with Calque(c, borne(a * 3)):
                    carte_s(c, cx - 470, cy - 230, 940, 460, 44, ombre=0.18)
                    for j in range(3): rrect(c, cx - 390, cy - 170 + j * 28, 300 - 70 * j, 13, 6, S["lavande"])
                    texte_grad(c, "KEEP UP", cx, cy - 60, 150, "noir", "centre", -0.035)
                    rrect(c, cx - 390, cy + 150, 780, 13, 6, S["doux"])
            b = entre(t, M["page"] + 0.12, 0.4, 2.4)
            if b > 0:
                c.save(); c.translate(cx + 440, cy - 220); c.scale(b, b); c.rotate(-12 * (1 - b))
                disque(c, 0, 0, 66, S["vert"], 1.0, (10, 24, 0.2)); icone(c, "check", 0, 0, 74, "#FFFFFF", 3.4)
                c.restore()
            eclats(c, cx + 440, cy - 220, t, M["page"] + 0.16, 12, 260, graine=5)


# ═══════════════════════════════════════════ B2 « motion design : il regarde, il comprend, il agit »
def jauge(c, t, cx, cy, sc):
    c.save(); c.translate(cx, cy); c.scale(sc, sc)
    R = 250
    lueur_s(c, 0, 0, 380, S["violetVif"], 0.22)
    arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(-R, -R, 2 * R, 2 * R), 180, 180)
    c.drawPath(arc, peinture(S["lavande"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=44, StrokeCap=skia.Paint.kRound_Cap))
    v = ressort(prog(t, M["captive"], 0.9, lin), 1.6, 3.4)
    v = borne(v * 0.98 + 0.02 * math.sin(t * 30) * borne((t - M["captive"]) / 0.3), 0, 1.04)
    arc2 = skia.Path(); arc2.addArc(skia.Rect.MakeXYWH(-R, -R, 2 * R, 2 * R), 180, 180 * min(1, v))
    pa = pgrad(-R, 0, R, 0, GRAD_VIF); pa.setStyle(skia.Paint.kStroke_Style); pa.setStrokeWidth(44); pa.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawPath(arc2, pa)
    for j in range(9):
        a_ = math.pi + j * math.pi / 8
        trait(c, (R - 60) * math.cos(a_), (R - 60) * math.sin(a_), (R - 80) * math.cos(a_), (R - 80) * math.sin(a_), S["grisClair"], 4)
    ang = math.pi + math.pi * min(1.03, v)
    trait(c, 0, 0, (R - 70) * math.cos(ang), (R - 70) * math.sin(ang), S["encre"], 12)
    disque(c, 0, 0, 26, S["encre"]); disque(c, 0, 0, 10, "#FFFFFF")
    texte(c, "ATTENTION", 0, 40, 30, S["gris"], "titre", "centre", 0.16)
    texte_grad(c, "HOOKED", 0, 90, 104, "noir", "centre", -0.03)
    c.restore()


def scene_b2(c, t):
    g = Groupe(c, t, M["b2"] - 0.1, M["b3"] - 0.05, ent="droite", sor="zoom", d_in=0.36, cy=CY)
    if not g.visible: return
    with g:
        up = prog(t, M["captive"] - 0.15, 0.4, entreeSortie)
        # MOTION DESIGN à gauche, la timeline à droite ; puis le titre se range en haut à gauche
        tx, ty, ts = mix(560, 330, up), mix(250, 40, up), mix(1, 0.5, up)
        c.save(); c.translate(tx, ty + 130); c.scale(ts, ts); c.translate(-560, -380)
        lettres(c, "MOTION", 560, 250, 170, t, M["motion"] - 0.45, "chemin", decal=0.045, duree=0.55, graine=7, grad=False, couleur=S["encre"])
        lettres(c, "DESIGN", 560, 420, 170, t, M["motion"] - 0.25, "chemin", decal=0.045, duree=0.55, graine=9)
        c.restore()
        ta = entre(t, M["motion"] - 0.1, 0.5, 1.2) * (1 - up)
        if ta > 0:
            with Espace(c, 1440, 470, ry=mix(-50, 0, ta), s=mix(0.8, 1, ta)):
                timeline(c, 1040, 300, 800, 340, t, M["motion"] - 0.1, M["captive"], borne(ta * 2))
        # captivé : la jauge naît au centre puis glisse à gauche pour laisser les trois étapes
        ja = entre(t, M["captive"] - 0.12, 0.5, 1.3)
        dn = prog(t, M["regarde"] - 0.12, 0.42, entreeSortie)
        if ja > 0:
            cx, cy = mix(CX, 400, dn), mix(560, 560, dn)
            with Calque(c, borne(ja * 3)):
                jauge(c, t, cx, cy, mix(1.15, 0.85, dn) * mix(0.5, 1, ja))
            onde(c, cx, cy, t, M["captive"] + 0.35, 120, 520, S["violetVif"], 8, 0.6)
        etapes = [("Watches", "eye", M["regarde"]), ("Gets it", "lightbulb", M["comprend"]), ("Acts", "mouse-pointer-click", M["action"])]
        xs = [920, 1240, 1560]; yN = 470
        for k in range(2):
            u = prog(t, etapes[k + 1][2] - 0.25, 0.3, sortie)
            if u > 0:
                xa, xb = xs[k] + 110, xs[k + 1] - 110
                trait(c, xa, yN, xa + (xb - xa) * u, yN, S["lilas"], 6)
                if u >= 1: losange(c, (xa + xb) / 2, yN, 10, S["violetVif"])
        for k, (lab, ic, t0) in enumerate(etapes):
            a = entre(t, t0 - 0.12, 0.45, 2.0)
            if a <= 0: continue
            x = xs[k]
            c.save(); c.translate(x, yN); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
            with Calque(c, borne(a * 3)):
                if k == 1:
                    on = prog(t, t0 + 0.1, 0.3, sortie)
                    rayons(c, 0, 0, t * 3, 180, 0.35 * on, 10, S["or_"])
                    lueur_s(c, 0, 0, 170, S["or_"], 0.4 * on)
                carte_s(c, -100, -100, 200, 200, 52, ombre=0.14)
                if k == 0:
                    cl = 1.0 if ((t - t0) % 1.4) > 0.12 else 0.15
                    c.save(); c.scale(1, cl); tuile(c, ic, 0, 0, 120); c.restore()
                elif k == 1:
                    tuile(c, ic, 0, 0, 120, "grad" if on > 0.5 else "doux")
                else:
                    tuile(c, ic, 0, 0, 120)
                texte(c, lab, 0, 124, 34, S["encre"], "titre", "centre", -0.02)
            c.restore()
            onde(c, x, yN, t, t0 - 0.02, 90, 190, S["violetVif"], 5, 0.5)
        ba = entre(t, M["action"] - 0.05, 0.4, 2.0)
        if ba > 0:
            ap = prog(t, M["action"] + 0.3, 0.1, sortie) * (1 - prog(t, M["action"] + 0.42, 0.15, sortie))
            bouton(c, "Book now", 1560, 760, 32, mix(0.4, 1, ba) * (1 - 0.06 * ap), borne(ba * 3), "check" if t > M["action"] + 0.4 else "arrow-right")
            cxu = mix(1780, 1600, prog(t, M["action"], 0.32, sortie)); cyu = mix(900, 776, prog(t, M["action"], 0.32, sortie))
            curseur(c, cxu, cyu, 1.0, borne(ba * 3), ap)
            clic(c, 1600, 770, t, M["action"] + 0.34)


# ═══════════════════════════════════════════ B3 « la différence : attention, demandes, clients »
def courbe(u):
    return 0.06 + 0.86 * (u ** 1.8) + 0.035 * math.sin(u * 17) * u


def scene_b3(c, t):
    g = Groupe(c, t, M["b3"] - 0.1, M["b4"] - 0.05, ent="grand", sor="haut", d_in=0.45, cy=CY)
    if not g.visible: return
    with g:
        lettres(c, M["titre_b3"], 160, 50, 84, t, M["b3"] - 0.05, "masque", decal=0.03, duree=0.45, align="gauche")
        x, y, w, h = 160, 170, 1040, 720
        a = entre(t, M["b3"], 0.5, 1.2)
        with Espace(c, x + w / 2, y + h / 2, ry=mix(-30, 0, a), s=mix(0.85, 1, a)):
            with Calque(c, borne(a * 3)):
                carte_s(c, x, y, w, h, 40, ombre=0.14)
                tuile(c, "chart-line", x + 70, y + 66, 76)
                texte(c, "Your business", x + 128, y + 44, 38, S["encre"], "titre", track=-0.02)
                pd = 0.5 + 0.5 * math.sin(t * 6)
                w_ = pill(c, "Live", x + w - 130, y + 66, 22, "vert")
                disque(c, x + w - 130 - w_ / 2 + 18, y + 66, 6, S["vert"], 0.4 + 0.6 * pd)
                gx, gy, gw, gh = x + 50, y + 140, w - 100, 330
                for j in range(4): trait(c, gx, gy + j * gh / 3, gx + gw, gy + j * gh / 3, S["ligne"], 2, pointille=[8, 10])
                u = prog(t, M["b3"] + 0.1, M["clients"] + 0.35 - M["b3"], lambda v: entreeSortie(v) * 0.4 + sortie(v) * 0.6)
                if u > 0:
                    n = 80; pts = [(gx + gw * k / n * u, gy + gh * (1 - courbe(k / n * u))) for k in range(n + 1)]
                    aire = skia.Path(); aire.moveTo(gx, gy + gh)
                    for p in pts: aire.lineTo(*p)
                    aire.lineTo(pts[-1][0], gy + gh); aire.close()
                    pa = skia.Paint(AntiAlias=True)
                    pa.setShader(skia.GradientShader.MakeLinear([skia.Point(0, gy), skia.Point(0, gy + gh)], [hexa(S["violetVif"], 0.28), hexa(S["bleuVif"], 0.0)]))
                    c.drawPath(aire, pa)
                    ligne = skia.Path(); ligne.moveTo(*pts[0])
                    for p in pts[1:]: ligne.lineTo(*p)
                    pl = pgrad(gx, 0, gx + gw, 0, GRAD_VIF); pl.setStyle(skia.Paint.kStroke_Style); pl.setStrokeWidth(9); pl.setStrokeCap(skia.Paint.kRound_Cap); pl.setStrokeJoin(skia.Paint.kRound_Join)
                    c.drawPath(ligne, pl)
                    hx, hy = pts[-1]
                    lueur_s(c, hx, hy, 60, S["violetVif"], 0.45); disque(c, hx, hy, 15, "#FFFFFF"); anneau(c, hx, hy, 15, S["violet"], 6)
                    if u > 0.25:
                        b = borne((u - 0.25) * 4)
                        c.save(); c.translate(hx - 30, hy - 66); c.scale(b, b)
                        rrect(c, -46, -28, 92, 56, 18, S["encre"]); icone(c, "trending-up", 0, 0, 34, "#FFFFFF", 2.8)
                        c.restore()
                kpi = [("Attention", "eye", M["attention"]), ("Inquiries", "message-circle", M["demandes"]), ("Customers", "users", M["clients"])]
                for k, (lab, ic, t0) in enumerate(kpi):
                    b = entre(t, t0 - 0.1, 0.45, 2.2)
                    if b <= 0: continue
                    kx = x + 50 + k * 320; ky = y + 530
                    c.save(); c.translate(kx + 145, ky + 65); c.scale(mix(0.4, 1, b), mix(0.4, 1, b)); c.translate(-(kx + 145), -(ky + 65))
                    with Calque(c, borne(b * 3)):
                        rrect(c, kx, ky, 290, 130, 26, S["doux"])
                        tuile(c, ic, kx + 50, ky + 46, 56, "doux", ep=2.4)
                        texte(c, lab, kx + 90, ky + 28, 30, S["encre"], "titre", track=-0.02)
                        icone(c, "trending-up", kx + 252, ky + 46, 34, S["vert"], 3.0)
                        fil = prog(t, t0, 0.6, sortie)
                        rrect(c, kx + 24, ky + 92, 242, 12, 6, S["lavande"])
                        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(kx + 24, ky + 92, 242 * mix(0.15, 0.92, fil), 12), 6, 6), pgrad(kx, 0, kx + 270, 0, GRAD_VIF))
                    c.restore()
        # à droite, les notifications s'empilent
        arrivees = [M["attention"] - 0.05, M["demandes"] - 0.05, M["demandes"] + 0.22, M["clients"] - 0.05]
        libs = ["Watched in full", "New inquiry", "New inquiry", "New customer"]
        ics = ["eye", "bell", "bell", "user-round"]
        for k, t0 in enumerate(arrivees):
            b = entre(t, t0, 0.45, 1.6)
            if b <= 0: continue
            yy = 230 + 112 * sum(prog(t, t1, 0.35, sortie) for t1 in arrivees[k + 1:])
            xx = 1260 + 700 * (1 - sortieExpo(prog(t, t0, 0.4, lin)))
            with Calque(c, borne(b * 3)):
                carte_s(c, xx, yy, 540, 92, 26, ombre=0.12)
                tuile(c, ics[k], xx + 50, yy + 46, 54, "grad")
                texte(c, libs[k], xx + 96, yy + 46 - hauteurLigne(28, "titre") / 2, 28, S["encre"], "titre", track=-0.02)
                texte(c, "just now", xx + 512, yy + 22, 20, S["gris"], "demi", "droite", 0)
        if t > M["clients"] + 0.1:
            confettis(c, 1530, 300, t, M["clients"] + 0.1, n=22, rayon=360, graine=4, cols=CONFETTIS)


# ═══════════════════════════════════════════ B4 « sur ton site : il explique, clairement »
def ecran_explicatif(c, x, y, w, h, t, t_play):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pgrad(x, y, x + w, y + h, ["#F4EEFF", "#E9F0FF"]))
    if t < t_play:
        lueur_s(c, x + w / 2, y + h / 2, 200, S["violetVif"], 0.25)
        disque(c, x + w / 2, y + h / 2, 62, S["violet"], 1.0, (8, 20, 0.2)); icone(c, "play", x + w / 2 + 5, y + h / 2, 56, "#FFFFFF", 2.6)
        return
    etapes = [("Quote", "receipt"), ("Design", "paintbrush"), ("Install", "hammer")]
    dt = (M["simple"] - t_play) / 3.2
    for k, (lab, ic) in enumerate(etapes):
        t0 = t_play + 0.08 + k * dt
        a = entre(t, t0, 0.4, 2.0)
        if a <= 0: continue
        cx = x + w * (0.2 + 0.3 * k); cy = y + h * 0.44
        if k > 0:
            u = prog(t, t0 - 0.12, 0.2, sortie)
            trait(c, cx - w * 0.3 + 56, cy, cx - w * 0.3 + 56 + (w * 0.3 - 112) * u, cy, S["violetVif"], 5)
        c.save(); c.translate(cx, cy); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
        tuile(c, ic, 0, 0, 92)
        disque(c, 38, -38, 18, S["encre"]); texte(c, str(k + 1), 38, -38 - hauteurLigne(20) / 2, 20, "#FFFFFF", "noir", "centre", 0)
        texte(c, lab, 0, 62, 26, S["encre"], "titre", "centre", -0.02)
        c.restore()
    barre_progression(c, x + 30, y + h - 26, w - 60, borne((t - t_play) / (M["simple"] + 0.4 - t_play)), 8, tete=False)


def scene_b4(c, t):
    g = Groupe(c, t, M["b4"] - 0.1, M["b5"] - 0.05, ent="bas", sor="recul", d_in=0.45, cy=CY)
    if not g.visible: return
    with g:
        x, y, w, h = 260, 130, 1400, 770
        b = entre(t, M["b4"] - 0.05, 0.55, 1.2)
        t_play = M["expliquer"] - 0.05
        vx_ = x + 700; vy_ = y + 78 + 150; vw_ = 620; vh_ = vw_ * 9 / 16
        def contenu(cc, x_, y_, w_, h_):
            cc.drawRect(skia.Rect.MakeXYWH(x_, y_, w_, h_), peinture("#FFFFFF"))
            texte(cc, "MOREL", x_ + 60, y_ + 34, 34, S["encre"], "noir", track=0.06)
            texte(cc, "· kitchens", x_ + 184, y_ + 40, 26, S["gris"], "demi", track=0)
            for j in range(4): rrect(cc, x_ + w_ - 470 + j * 110, y_ + 50, 80, 10, 5, S["ligne"])
            texte(cc, "Your kitchen,", x_ + 60, y_ + 170, 66, S["encre"], "titre", track=-0.035)
            texte_grad(cc, "made to measure.", x_ + 60, y_ + 244, 66, "titre", "gauche", -0.035)
            lignes_texte(cc, x_ + 60, y_ + 360, 480, 3, t, M["b4"], 0.06, 14, 32)
            rrect(cc, x_ + 60, y_ + 480, 260, 70, 35, S["violet"]); texte(cc, "Book a visit", x_ + 190, y_ + 500, 22, "#FFFFFF", "fort", "centre", 0)
            cc.save(); cc.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(vx_, vy_, vw_, vh_), 22, 22), doAntiAlias=True)
            ecran_explicatif(cc, vx_, vy_, vw_, vh_, t, t_play)
            cc.restore()
            cc.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(vx_, vy_, vw_, vh_), 22, 22), peinture(S["ligne"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        with Espace(c, x + w / 2, y + h / 2, rx=mix(35, 0, b), s=mix(0.75, 1, b) * (1 + 0.01 * math.sin(t * 1.5))):
            navigateur(c, x, y, w, h, "morel-kitchens.com", contenu, borne(b * 3))
        a = entre(t, M["site"] - 0.12, 0.4, 2.2)
        pill(c, "On your website", CX, 62, 34, "grad", "laptop", borne(a * 3), mix(0.4, 1, a))
        la = entre(t, M["long_texte"] - 0.12, 0.45, 1.6)
        if la > 0:
            c.save(); c.translate(560, 800); c.rotate(-5); c.scale(mix(0.5, 1, la), mix(0.5, 1, la))
            with Calque(c, borne(la * 3)):
                carte_s(c, -230, -110, 460, 220, 28, ombre=0.16)
                lignes_texte(c, -190, -76, 380, 6, t, M["long_texte"] - 0.1, 0.03, 12, 26, cols=S["grisClair"])
                bar = prog(t, M["long_texte"] + 0.25, 0.22, sortie)
                if bar > 0:
                    trait(c, -210, 60, -210 + 420 * bar, -60, S["rouge"], 10)
                    bb = entre(t, M["long_texte"] + 0.4, 0.35, 2.4)
                    if bb > 0:
                        disque(c, 210, -100, 34 * bb, S["rouge"]); icone(c, "x", 210, -100, 38 * bb, "#FFFFFF", 3.4)
            c.restore()
        px0, py0 = vx_ + vw_ / 2, vy_ + vh_ / 2
        cu = prog(t, t_play - 0.5, 0.42, sortie)
        if cu > 0:
            ap = prog(t, t_play - 0.06, 0.06, sortie) * (1 - prog(t, t_play + 0.05, 0.12, sortie))
            curseur(c, mix(1820, px0 + 6, cu), mix(980, py0 + 6, cu), 1.0, 1 - prog(t, t_play + 0.5, 0.3, sortie), ap)
            clic(c, px0, py0, t, t_play)
        d = entre(t, M["simple"] - 0.08, 0.4, 2.4)
        if d > 0:
            s_ = mix(2.2, 1, prog(t, M["simple"] - 0.08, 0.2, entree))
            c.save(); c.translate(1640, 250); c.rotate(-8); c.scale(s_, s_)
            pill(c, "Clear", 0, 0, 40, "vert", "circle-check", borne(d * 3))
            c.restore()
            eclats(c, 1640, 250, t, M["simple"], 10, 220, graine=8)


# ═══════════════════════════════════════════ B5 « script, animation, 3 ou 4 accroches »
ACCROCHES = [("01", "The problem", "Customers don't get it?"), ("02", "The benefit", "Clear in seconds."),
             ("03", "Curiosity", "Your best salesperson?"), ("04", "The solution", "Show it. Make them want it.")]


def mini_ecran(c, x, y, w, h, t, k):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pgrad(x, y, x + w, y + h, [GRAD_VIF[0], GRAD_VIF[2]] if k % 2 == 0 else ["#2A1E52", "#4B3A9A"]))
    num, nom, phrase = ACCROCHES[k]
    texte(c, num, x + 24, y + 60, 26, "#FFFFFF", "titre", track=0.06, alpha=0.7)
    texte(c, nom.upper(), x + 24, y + 94, 19, "#FFFFFF", "titre", track=0.1, alpha=0.8)
    ly = y + 150; lx = x + 24
    for j, m in enumerate(phrase.split(" ")):
        tl = 32; mw = largeur(m, tl, "noir")
        if lx + mw > x + w - 20: lx = x + 24; ly += 40
        texte(c, m, lx, ly + 2 * math.sin(t * 5 + j + k), tl, "#FFFFFF", "noir", track=-0.02); lx += mw + 10
    barre_progression(c, x + 20, y + h - 36, w - 40, ((t * 0.5 + k * 0.23) % 1), 8, ["#FFFFFF", "#FFFFFF"], "#FFFFFF40", tete=False)


def scene_b5(c, t):
    g = Groupe(c, t, M["b5"] - 0.1, M["prix"] - 0.1, ent="droite", sor="aucune", d_in=0.38, cy=CY)
    if not g.visible: return
    with g:
        part = prog(t, M["accroches"] - 0.35, 0.4, entreeSortie)
        if part < 1:
            with Calque(c, 1 - part):
                a = entre(t, M["b5"] - 0.05, 0.5, 1.4)
                sx, sy = 640, 470 - 900 * part
                with Espace(c, sx, sy, ry=mix(-70, 0, a), rz=-3):
                    with Calque(c, borne(a * 3)):
                        carte_s(c, sx - 300, sy - 300, 600, 560, 36, ombre=0.15)
                        texte(c, "SCRIPT.txt", sx - 250, sy - 262, 26, S["gris"], "titre", track=0.06)
                        disque(c, sx + 250, sy - 248, 8, S["violetVif"])
                        lignes_texte(c, sx - 250, sy - 190, 500, 10, t, M["script"] - 0.15, 0.07, 14, 40, accent=(1, 2, 6))
                        k = int(borne((t - M["script"] + 0.15) / 0.07, 0, 9))
                        if int(t * 5) % 2 == 0 and t < M["anime"]: rrect(c, sx - 250 + 400, sy - 196 + k * 40, 4, 26, 2, S["violet"])
                pill(c, "SCRIPT", sx, sy + 320, 32, "blanc", "file-text", borne(a * 3))
                b = entre(t, M["anime"] - 0.15, 0.5, 1.4)
                if b > 0:
                    ax, ay = 1290, 470 - 900 * part
                    with Espace(c, ax, ay, ry=mix(70, 0, b), rz=3):
                        with Calque(c, borne(b * 3)):
                            carte_s(c, ax - 300, ay - 300, 600, 560, 36, ombre=0.15)
                            ph = ((t - M["anime"]) * 1.4) % 1
                            bx = ax - 200 + 400 * ph; by = ay - 60 - 180 * abs(math.sin(math.pi * ph * 2))
                            pth = skia.Path(); pth.moveTo(ax - 200, ay - 60)
                            for j in range(1, 41):
                                q = j / 40; pth.lineTo(ax - 200 + 400 * q, ay - 60 - 180 * abs(math.sin(math.pi * q * 2)))
                            pa = peinture(S["lilas"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=4); pa.setPathEffect(skia.DashPathEffect.Make([8, 10], 0)); c.drawPath(pth, pa)
                            for q in (0, 0.25, 0.5, 0.75, 1.0): losange(c, ax - 200 + 400 * q, ay - 60 - 180 * abs(math.sin(math.pi * q * 2)), 9, "#FFFFFF", 1, S["violetVif"])
                            sq = 1 + 0.25 * max(0, 1 - abs(math.sin(math.pi * ph * 2)) * 6)
                            c.save(); c.translate(bx, by); c.scale(sq, 1 / sq)
                            c.drawCircle(0, -32, 32, pgrad(-32, -64, 32, 0, GRAD_VIF)); c.restore()
                            timeline(c, ax - 270, ay + 20, 540, 210, t, M["anime"] - 0.1, M["accroches"], 1.0)
                    pill(c, "ANIMATION", ax, ay + 320, 32, "blanc", "clapperboard", borne(b * 3))
        if t > M["accroches"] - 0.3:
            lettres(c, "3 OR 4 HOOKS", CX, 40, 96, t, M["accroches"] - 0.25, "ressort", decal=0.03)
            for k in range(4):
                a = entre(t, M["accroches"] - 0.1 + 0.08 * k, 0.55, 1.5)
                if a <= 0: continue
                ang = mix(0, (-1.5 + k) * 7, a)
                cx = CX + mix(0, (-1.5 + k) * 340, a); cy = 520 + abs(-1.5 + k) * 26 * a
                gagne = k == 1 and t > M["tester"] - 0.05
                lev = prog(t, M["tester"] - 0.05, 0.35, lambda v: rebond(v, 1.8)) if k == 1 else 0
                c.save(); c.translate(cx, cy - 60 * lev); c.rotate(ang * (1 - lev)); c.scale(1 + 0.1 * lev, 1 + 0.1 * lev)
                telephone_s(c, 0, 0, 260, 520, lambda cc, ex, ey, ew, eh, k=k: mini_ecran(cc, ex, ey, ew, eh, t, k), borne(a * 3))
                if gagne:
                    disque(c, 104, -240, 40, S["or_"], 1.0, (8, 20, 0.2)); icone(c, "trophy", 104, -240, 42, "#FFFFFF", 2.6)
                c.restore()
            b = entre(t, M["tester"] - 0.1, 0.4, 2.2)
            if b > 0:
                pill(c, "Test them", CX + 700, 860, 32, "encre", "split", borne(b * 3), mix(0.4, 1, b), rot=-4)
                eclats(c, CX - 340 + 340, 420, t, M["tester"] + 0.1, 12, 360, graine=11)


# ═══════════════════════════════════════════ prix
def scene_prix(c, t):
    t_in, t_out = M["prix"] - 0.22, M["devis"] - 0.12
    if t < t_in or t > t_out + 0.5: return
    R = cles(t, [(t_in, 0), (t_in + 0.42, 1250, sortieExpo), (t_out, 1250), (t_out + 0.4, 0, entreeSortie)])
    def dessin(cc):
        fond_grad(cc, t)
        rayons(cc, CX, 470, t, 1400, 0.10, 18)
        a = entre(t, M["prix"] - 0.05, 0.4, 1.6)
        texte(cc, "FROM", CX, 130 + 20 * (1 - a), 46, "#FFFFFF", "titre", "centre", 0.14, borne(a * 3))
        taille = 330
        ws = [largeur(ch, taille, "noir", -0.04) for ch in "290"]
        we = largeur("€", 210, "noir", -0.02)
        tot = sum(ws) + we + 30
        xe = CX - tot / 2; x = xe + we + 30; y = 220            # en anglais : €290
        arr = [M["deux"] + 0.08, M["qvd"] + 0.2, M["euros"] - 0.06]
        for k, ch in enumerate("290"):
            rouleau(cc, int(ch), x, y, taille, t, M["prix"] - 0.05 + 0.04 * k, arr[k])
            x += ws[k]
        e = entre(t, M["euros"] - 0.05, 0.4, 2.6)
        if e > 0:
            cc.save(); cc.translate(xe + we / 2, y + 120); cc.scale(mix(0.2, 1, e), mix(0.2, 1, e))
            texte(cc, "€", 0, -hauteurLigne(210) / 2 + 20, 210, "#FFFFFF", "noir", "centre", -0.02)
            cc.restore()
            pill(cc, "incl. VAT", xe + tot / 2, y + 400, 30, "blanc", None, borne(e * 3), mix(0.3, 1, e))
        sh = prog(t, M["euros"] + 0.1, 0.5, lin)
        if 0 < sh < 1:
            p = skia.Paint(AntiAlias=True); sxp = mix(300, 1620, sh)
            p.setShader(skia.GradientShader.MakeLinear([skia.Point(sxp - 140, 0), skia.Point(sxp + 140, 0)], [hexa("#FFFFFF", 0), hexa("#FFFFFF", 0.35), hexa("#FFFFFF", 0)]))
            cc.drawRect(skia.Rect.MakeXYWH(0, y, W, 360), p)
        onde(cc, CX, 400, t, M["euros"], 120, 760, "#FFFFFF", 8, 0.7)
        eclats(cc, CX, 400, t, M["euros"] + 0.02, 18, 700, ["#FFFFFF", "#E3D6FF", S["or_"], "#C9D8FF"], graine=4, duree=0.9)
        chips = [("30–45 s", "clock"), ("3–4 hooks", "layers"), ("Script included", "file-text"), ("2nd format free", "gift")]
        for k, (lab, ic) in enumerate(chips):
            b = entre(t, M["euros"] + 0.1 + 0.08 * k, 0.4, 2.2)
            pill(cc, lab, CX + (k - 1.5) * 380, 760, 28, "blanc", ic, borne(b * 3), mix(0.4, 1, b))
    iris(c, CX, 470, R, dessin)


# ═══════════════════════════════════════════ appel à l'action
def scene_cta(c, t):
    t0 = M["devis"] - 0.15
    if t < t0: return
    a = entre(t, t0 + 0.05, 0.55, 1.5)
    iw, ih = taille_img("dyou-logo-horizontal-black"); lw = 760 * mix(0.6, 1, a)
    c.save()
    flou_calque(c, 14 * (1 - prog(t, t0 + 0.05, 0.35, sortie)), borne(a * 3))
    image(c, "dyou-logo-horizontal-black", CX - lw / 2, 170 - lw * ih / iw / 2, lw)
    c.restore(); c.restore()
    b = prog(t, t0 + 0.2, 0.4, sortie)
    if b > 0:
        texte(c, "Your offer, in motion.", CX, 300 + 20 * (1 - b), 68, S["encre"], "titre", "centre", -0.03, b)
    bt = entre(t, M["devis"] + 0.18, 0.5, 1.8)
    tc = M["devis"] + 0.75
    ap = prog(t, tc - 0.06, 0.06, sortie) * (1 - prog(t, tc + 0.05, 0.14, sortie))
    pulse = 1 + 0.025 * max(0, math.sin((t - tc - 0.4) * 5)) if t > tc + 0.4 else 1
    if bt > 0:
        bouton(c, "Request my quote", CX - 330, 520, 40, mix(0.2, 1, bt) * (1 - 0.07 * ap) * pulse, borne(bt * 3))
    cu = prog(t, tc - 0.5, 0.45, sortie)
    if cu > 0:
        curseur(c, mix(400, CX - 260, cu), mix(900, 534, cu), 1.1, 1 - prog(t, tc + 0.6, 0.3, sortie), ap)
        clic(c, CX - 260, 527, t, tc)
    eclats(c, CX - 330, 520, t, tc + 0.02, 12, 420, graine=12)
    ub = entre(t, M["url"] - 0.25, 0.45, 1.6)
    if ub > 0:
        with Calque(c, borne(ub * 3)):
            wb = 560; xb = CX + 330; yb = 520
            carte_s(c, xb - wb / 2, yb - 46, wb, 92, 46, ombre=0.12)
            icone(c, "lock", xb - wb / 2 + 50, yb, 28, S["vert"], 2.6)
            url = "dyou-agency.com"
            n = int(borne((t - M["url"]) / 0.5) * len(url) + 0.999) if t >= M["url"] else 0
            xs_ = xb - wb / 2 + 84
            texte(c, url[:n], xs_, yb - hauteurLigne(38, "titre") / 2, 38, S["encre"], "titre", track=-0.01)
            if int(t * 3) % 2 == 0: rrect(c, xs_ + largeur(url[:n], 38, "titre", -0.01) + 4, yb - 22, 4, 44, 2, S["violet"])
    for k, (lab, ic) in enumerate([("30–45 s", "clock"), ("3–4 hooks", "layers"), ("from €290 incl. VAT", "sparkles"), ("2nd format free", "gift")]):
        b = entre(t, M["url"] + 0.4 + 0.08 * k, 0.4, 2.2)
        if b > 0:
            pill(c, lab, CX + (k - 1.5) * 390, 760, 30, "doux", ic, borne(b * 3), mix(0.4, 1, b))


# ═══════════════════════════════════════════ sons
son(0.0, "impact", -7); son(0.0, "tick", -10); son(0.05, "pop", -13)
for tt in (0.5, 1.0): son(tt, "tick", -14)
son(TW(1) - 0.1, "pop", -12); son(TW(4) - 0.15, "pop", -10); son(TW(5) - 0.2, "whoosh_court", -12)
son(T_2, "tick", -9); son(T_2, "whoosh_court", -15); son(T_1, "tick", -8); son(T_1, "whoosh_court", -15)
son(T_SW - 0.22, "swipe", -9); son(T_SW, "whoosh", -8)
son(T_SNAP - 0.05, "whoosh_bas", -8); son(T_SNAP + 0.05, "impact", -5); son(T_SNAP + 0.08, "verre", -10); son(T_SNAP + 0.1, "ching", -13)
for k in range(8): son(T_SNAP + 0.1 + 0.05 * k, "pop", -18)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps(K, M)
son(M["clients"] + 0.1, "pop", -14); son(M["attention"] - 0.05, "message_in", -13)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.2), (T_SW - 0.05, T_SW + 0.35), (T_SNAP - 0.05, T_SNAP + 0.4), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_SNAP + 0.05, "#FFFFFF", 0.35), (M["page"] + 0.12, "#FFFFFF", 0.25), (M["captive"] + 0.35, S["violetVif"], 0.08),
                    (M["euros"] - 0.06, "#FFFFFF", 0.22), (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


# ═══════════════════════════════════════════ composition
def dessine(c, t):
    fond_studio(c, t, battement(t, T_SNAP + 0.05, 1, 0.5) + battement(t, M["captive"] + 0.35, 1, 0.5) - 2)
    scene_b1(c, t); scene_b2(c, t); scene_b3(c, t); scene_b4(c, t); scene_b5(c, t)
    scene_cta(c, t)
    scene_prix(c, t)
    if t < T_B1 + 0.3:
        o = prog(t, T_B1 - 0.3, 0.35, entree)
        c.save(); c.translate(CX, CY); c.scale(mix(1, 2.2, o), mix(1, 2.2, o)); c.translate(-CX, -CY)
        with Calque(c, 1 - o):
            hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    if t < M["prix"] - 0.25: SOUS.dessine(c, t, S["encre"])
