"""Format « BONHOMME » de @recto_cerveau — 29/10/2026.

Décision de Youssef le 29/10/2026, après AC-M01→M04 (« notre format visuel n'accroche pas et en plus
il met trop de temps à produire, faut aller plus simple ») : un **bonhomme animé en 2D** qui incarne
la personne dont on parle — un corps en bâtons blanc, une vraie **photo de son visage** en guise de
tête, sur le noir de la chaîne. Même palette (noir / blanc / un rouge), mais **plus de pièce 3D,
plus de grille, plus de pavés** : un sol, un bonhomme, une bulle, une photo ou deux, le sous-titre.
Ça se lit en une demi-seconde et ça se rend en quelques minutes.

Ce qu'on a repris des skills GitHub (29/10/2026, cherry-pick, pas d'installation brute) :
  - `cafermutluozkan/stick-motion` : le RIG. Longueurs d'os fixes, bras posés par angles
    (cinématique directe), jambes posées par la cible du pied au sol résolue analytiquement
    (cinématique inverse) → un pied ne flotte jamais, ne glisse jamais. Marche déterministe
    « pied verrouillé » : pure fonction du temps, on peut sauter à n'importe quel instant.
  - `QuantumCoderSys/stickman-story-reels` : la bibliothèque de poses lisibles (bras en l'air,
    pointer, courir), les expressions de visage, la règle « frame 1 bouge déjà ».
  Leur sortie est du HTML/GSAP ou du HyperFrames : on ne garde que la géométrie, portée ici en Skia.

Règles du rig (vérifiables) :
  1. jamais d'angle de cuisse écrit à la main : une jambe se pose par `pied_g`/`pied_d` (dx, dy
     par rapport au sol) et `_ik_jambe` trouve cuisse et genou ;
  2. une pose est un dict de nombres plats → `melange(p1, p2, u)` interpole tout ;
  3. les os ne changent jamais de longueur pendant une vidéo ;
  4. tout est fonction pure de t.

    from bonhomme import *
    fond_bonhomme(c, t)
    b = bonhomme(c, x, pose=melange(STAND, POINT, u), face=1, tete="hayden", u=1)
    bulle(c, b["tete"], "C'était la pom-pom girl", t, t0)
    etiquette(c, x, "HAYDEN", u)
"""
import math
import skia
import moteur
from moteur import *
from people import (FOND, FOND2, BLANC, BLANC2, NOIR, ROUGE, ROUGE2, GRIS, AXE, AXE_HAUT, LARG_T,
                    LOGO, NOM_CHAINE, BASELINE, filigrane, sous_titres_people, signature_people,
                    sons_signature_people, titre, rubrique, surlignage)

# ───────────────────────────── le sol, la pose du bonhomme
SOL = 1290.0            # ligne de sol : le bonhomme est debout dessus, les sous-titres (y 1402) en dessous
ECH = 2.9               # échelle du corps (le rig d'origine fait 250 px à l'échelle 1)
R_TETE = 28.0 * ECH * 1.55    # rayon de la tête : grosse tête photo, petit corps — ça se lit sur un téléphone
EP = 14.0               # épaisseur du trait

# longueurs d'os, en « rayons de tête » du rig d'origine (28 px) → jamais modifiées en cours de vidéo
_R = 28.0 * ECH
OS = dict(cou=_R * 0.35, tronc=_R * 3.1, bras=_R * 1.55, avant_bras=_R * 1.4,
          cuisse=_R * 1.9, tibia=_R * 1.85, pied=_R * 0.85)
H_HANCHE = (OS["cuisse"] + OS["tibia"]) * 0.955          # hauteur de hanche debout

D2R = math.pi / 180


def _bas(a, L, face):      # vecteur « référence vers le bas », angle en degrés, face = ±1
    return face * L * math.sin(a * D2R), L * math.cos(a * D2R)


def _haut(a, L, face):     # vecteur « référence vers le haut »
    return face * L * math.sin(a * D2R), -L * math.cos(a * D2R)


def _chaine(x, y, a1, L1, pli, L2, face, ref="bas"):
    v = _bas if ref == "bas" else _haut
    dx, dy = v(a1, L1, face); jx, jy = x + dx, y + dy
    a2 = a1 + pli
    dx, dy = v(a2, L2, face)
    return (jx, jy), (jx + dx, jy + dy), a2


def _ik_jambe(hx, hy, px, py, L1, L2, face, genou=1):
    """cuisse + genou pour que le pied touche exactement (px, py). Jamais d'angle écrit à la main."""
    dx, dy = (px - hx) * face, py - hy
    d = math.hypot(dx, dy)
    d = min(max(d, abs(L1 - L2) + 0.5), L1 + L2 - 0.01)
    a_pied = math.atan2(dx, dy)
    B = math.acos(borne((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1))
    C = math.acos(borne((L1 * L1 + L2 * L2 - d * d) / (2 * L1 * L2), -1, 1))
    return (a_pied - genou * B) / D2R, genou * (math.pi - C) / D2R


# ───────────────────────────── poses : des nombres plats, rien d'autre
def pose(**kw):
    p = dict(tronc=0, cou=0, ep_g=-10, coude_g=12, ep_d=10, coude_d=12,
             pied_gx=-30, pied_gy=0, pied_dx=30, pied_dy=0, pied_g=90, pied_d=90, hanche=0)
    p.update(kw); return p


STAND = pose()
POINT = pose(tronc=4, cou=2, ep_d=-92, coude_d=-4)                       # bras droit tendu devant (vers « face »)
WAVE = pose(tronc=2, cou=-4, ep_d=-150, coude_d=60)
CHEER = pose(ep_g=-170, coude_g=-10, ep_d=170, coude_d=10, pied_gx=-40, pied_dx=40)
SHRUG = pose(cou=-6, ep_g=60, coude_g=-150, ep_d=-60, coude_d=150, pied_gx=-36, pied_dx=36)   # mains ouvertes, paumes au ciel
HEAD_DOWN = pose(tronc=18, cou=38, ep_g=8, coude_g=10, ep_d=-6, coude_d=10)                   # tête basse
FACEPALM = pose(tronc=8, cou=22, ep_d=-140, coude_d=-115, ep_g=-6, coude_g=10)
THINK = pose(cou=8, ep_d=-30, coude_d=-120, ep_g=-6, coude_g=10)                              # main au menton
PHONE = pose(cou=14, ep_d=-20, coude_d=-130)                                                   # téléphone à l'oreille
CROSSED = pose(ep_g=40, coude_g=-120, ep_d=-40, coude_d=120, pied_gx=-34, pied_dx=34)         # bras croisés
CROUCH = pose(tronc=8, cou=6, ep_g=35, coude_g=70, ep_d=-35, coude_d=-70, pied_gx=-32, pied_dx=32, hanche=56)
JUMP = pose(tronc=-4, cou=-2, ep_g=-150, coude_g=20, ep_d=150, coude_d=-20,
            pied_gx=-16, pied_gy=-70, pied_dx=16, pied_dy=-70, pied_g=60, pied_d=60, hanche=-70)
SHAKE = pose(tronc=3, ep_d=-38, coude_d=-12, ep_g=-8, coude_g=12)                                   # poignée de main
SIT = pose(tronc=-4, cou=4, ep_g=-50, coude_g=60, ep_d=-50, coude_d=60,
           pied_gx=70, pied_gy=0, pied_dx=90, pied_dy=0, hanche=int(H_HANCHE * 0.42))         # assis sur une chaise basse
TALK = pose(cou=2, ep_d=-60, coude_d=-70, ep_g=-8, coude_g=14)                                 # une main qui parle


def melange(p1, p2, u):
    u = borne(u)
    return {k: mix(p1[k], p2[k], u) for k in p1}


def respire(p, t, amp=1.0):
    """le bonhomme n'est jamais figé : un souffle lent sur le tronc et le cou"""
    s = math.sin(t * 2.1) * amp
    q = dict(p); q["tronc"] = p["tronc"] + 1.2 * s; q["cou"] = p["cou"] - 1.6 * s; q["hanche"] = p["hanche"] + 2.0 * s
    return q


# ───────────────────────────── marche déterministe, pied verrouillé (stick-motion)
MARCHE = dict(T=0.72, duty=0.62, pas=26.0 * ECH * 0.55, rebond=8.0 * ECH * 0.5)


def _pied_marche(tm, vitesse, dephasage):
    T, duty = MARCHE["T"], MARCHE["duty"]
    phi = ((tm / T) + dephasage) % 1.0
    amp = vitesse * T * duty                        # recul de la hanche pendant un appui
    if phi < duty:
        u = phi / duty
        return amp / 2 - amp * u, 0.0               # pied planté : il recule exactement à la vitesse de la hanche
    u = (phi - duty) / (1 - duty)
    e = 2 * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 2 / 2
    return -amp / 2 + amp * e, -MARCHE["pas"] * math.sin(math.pi * u)


def pose_marche(tm, vitesse):
    """pose de marche à l'instant tm (s), pour une hanche qui avance à `vitesse` px/s (valeur signée
    par `face`, en valeur absolue ici). Le dessinateur doit faire avancer x_hanche de vitesse·tm."""
    v = abs(vitesse)
    dx_d, dy_d = _pied_marche(tm, v, 0.0)
    dx_g, dy_g = _pied_marche(tm, v, 0.5)
    w = 2 * math.pi * tm / MARCHE["T"]
    bal = 22 if v > 1 else 0
    return pose(tronc=4 if v > 1 else 0, cou=0,
                ep_d=bal * math.sin(w), coude_d=14, ep_g=-bal * math.sin(w), coude_g=14,
                pied_gx=dx_g, pied_gy=dy_g, pied_dx=dx_d, pied_dy=dy_d, pied_g=90, pied_d=90,
                hanche=-MARCHE["rebond"] * abs(math.sin(w / 2)))


def pose_course(tm, vitesse):
    MARCHE_C = dict(MARCHE); MARCHE_C.update(T=0.46, duty=0.42, pas=MARCHE["pas"] * 1.8)
    sauve = dict(MARCHE); MARCHE.update(MARCHE_C)
    try:
        p = pose_marche(tm, vitesse)
    finally:
        MARCHE.update(sauve)
    p["tronc"] = 14; p["ep_d"] *= 2.4; p["ep_g"] *= 2.4; p["coude_d"] = 70; p["coude_g"] = 70
    return p


# ───────────────────────────── le visage dessiné (quand il n'y a pas de photo)
def visage(c, cx, cy, r, expr="neutre", regard=0.0, encre=NOIR, ep=EP):
    ex = (cx - r * 0.34 + regard * r * 0.12, cx + r * 0.34 + regard * r * 0.12); ey = cy - r * 0.06
    grand = expr in ("peur", "cri")
    for x in ex:
        c.drawOval(skia.Rect.MakeXYWH(x - r * (0.11 if grand else 0.09), ey - r * (0.16 if grand else 0.13),
                                      2 * r * (0.11 if grand else 0.09), 2 * r * (0.16 if grand else 0.13)), peinture(encre))
    bw, by = r * 0.22, ey - r * 0.3
    if expr in ("inquiet", "peur"):
        trait(c, ex[0] - bw, by + r * 0.02, ex[0] + bw * 0.7, by - r * 0.1, encre, ep * 0.4)
        trait(c, ex[1] + bw, by + r * 0.02, ex[1] - bw * 0.7, by - r * 0.1, encre, ep * 0.4)
    if expr in ("severe", "cri"):
        trait(c, ex[0] - bw, by - r * 0.08, ex[0] + bw * 0.7, by + r * 0.04, encre, ep * 0.4)
        trait(c, ex[1] + bw, by - r * 0.08, ex[1] - bw * 0.7, by + r * 0.04, encre, ep * 0.4)
    my = cy + r * 0.42
    if grand:
        c.drawOval(skia.Rect.MakeXYWH(cx - r * 0.18, my - r * 0.2, r * 0.36, r * 0.4), peinture(encre))
    elif expr == "inquiet":
        p = skia.Path(); p.moveTo(cx - r * 0.2, my + r * 0.04); p.quadTo(cx, my - r * 0.08, cx + r * 0.2, my + r * 0.04)
        c.drawPath(p, peinture(encre, Style=skia.Paint.kStroke_Style, StrokeWidth=ep * 0.35, StrokeCap=skia.Paint.kRound_Cap))
    elif expr == "severe":
        trait(c, cx - r * 0.2, my, cx + r * 0.2, my, encre, ep * 0.38)
    else:
        p = skia.Path(); p.moveTo(cx - r * 0.2, my - r * 0.03); p.quadTo(cx, my + r * 0.12, cx + r * 0.2, my - r * 0.03)
        c.drawPath(p, peinture(encre, Style=skia.Paint.kStroke_Style, StrokeWidth=ep * 0.35, StrokeCap=skia.Paint.kRound_Cap))


SENS_PHOTO = {}     # nom de photo → sens du regard (+1 vers la droite, −1 vers la gauche) ; miroir automatique


def tete_photo(c, cx, cy, r, nom, zoom=1.0, fx=0.5, fy=0.38, alpha=1.0, anneau=ROUGE, gris=0.0, miroir=False):
    """la vraie tête : la photo de la personne dans un disque, cerclé de rouge (le « recto »)"""
    with Calque(c, alpha):
        c.save(); c.clipPath(skia.Path.Circle(cx, cy, r), doAntiAlias=True)
        if miroir: c.translate(cx, 0); c.scale(-1, 1); c.translate(-cx, 0)
        if gris > 0.01:
            c.saveLayer(None, skia.Paint(ColorFilter=skia.ColorFilters.Matrix(
                [mix(1, .3, gris), mix(0, .59, gris), mix(0, .11, gris), 0, 0,
                 mix(0, .3, gris), mix(1, .59, gris), mix(0, .11, gris), 0, 0,
                 mix(0, .3, gris), mix(0, .59, gris), mix(1, .11, gris), 0, 0, 0, 0, 0, 1, 0])))
        image_cover(c, nom, cx - r, cy - r, 2 * r, 2 * r, zoom, fx, fy)
        if gris > 0.01: c.restore()
        c.restore()
        anneau_ = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=EP * 0.5, Color=hexa(anneau))
        c.drawCircle(cx, cy, r, anneau_)


# ───────────────────────────── le bonhomme
def bonhomme(c, x, pose_, face=1, tete=None, expr="neutre", regard=0.0, u=1.0, alpha=1.0,
             couleur=BLANC, ep=EP, sol=SOL, r_tete=R_TETE, zoom=1.0, fx=0.5, fy=0.38, gris=0.0,
             anneau=ROUGE, props=None, taille=1.0, seulement_anneau=False):
    """dessine le bonhomme debout en x (hanche), sur la ligne `sol`.

    face : +1 regarde vers la droite, −1 vers la gauche. tete : nom d'une photo (media/photos)
    ou None → visage dessiné. u < 1 : il surgit du sol (entrée). Retourne les points utiles :
    tete, cou, epaule, main_g, main_d, pied_g, pied_d, hanche, r (rayon de tête)."""
    if alpha <= 0.01 or u <= 0.005: return None
    p = pose_
    hy = sol - H_HANCHE + p["hanche"]
    with Calque(c, alpha):
        c.save()
        if taille != 1.0: c.translate(x, sol); c.scale(taille, taille); c.translate(-x, -sol)
        if u < 0.999:                                         # il se déplie depuis le sol
            s = mix(0.2, 1.0, sortie(u)); c.translate(x, sol); c.scale(s, s); c.translate(-x, -sol)
        # tronc, cou, tête (cinématique directe, référence « haut »)
        dx, dy = _haut(p["tronc"], OS["tronc"], face); ex, ey = x + dx, hy + dy
        dx, dy = _haut(p["tronc"] + p["cou"], OS["cou"], face); nx, ny = ex + dx, ey + dy
        dx, dy = _haut(p["tronc"] + p["cou"], r_tete * 0.92, face); tx, ty = nx + dx, ny + dy
        # jambes : cible du pied au sol → IK
        pieds = {}
        for cote, kx, ky, kb in (("g", "pied_gx", "pied_gy", "pied_g"), ("d", "pied_dx", "pied_dy", "pied_d")):
            px, py = x + p[kx], sol + p[ky]
            a1, pli = _ik_jambe(x, hy, px, py, OS["cuisse"], OS["tibia"], face, 1)
            genou, pied, a2 = _chaine(x, hy, a1, OS["cuisse"], pli, OS["tibia"], face)
            fdx, fdy = _bas(a2 + p[kb], OS["pied"], face)
            pieds[cote] = (genou, pied, (pied[0] + fdx, pied[1] + fdy))
        pt = peinture(couleur, Style=skia.Paint.kStroke_Style, StrokeWidth=ep, StrokeCap=skia.Paint.kRound_Cap,
                      StrokeJoin=skia.Paint.kRound_Join)
        if seulement_anneau:                                   # il ne reste que le cercle rouge, vide
            c.drawCircle(tx, ty, r_tete, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=EP * 0.5, Color=hexa(anneau)))
            c.restore()
            mains = {"g": (ex, ey), "d": (ex, ey)}
            pieds = {"g": ((x, hy), (x, sol), (x, sol)), "d": ((x, hy), (x, sol), (x, sol))}
            M = lambda q: (x + (q[0] - x) * taille, sol + (q[1] - sol) * taille)
            return dict(tete=M((tx, ty)), cou=M((nx, ny)), epaule=M((ex, ey)), main_g=M((ex, ey)), main_d=M((ex, ey)),
                        pied_g=(x, sol), pied_d=(x, sol), hanche=M((x, hy)), r=r_tete * taille, face=face)
        for cote in ("g", "d"):
            genou, pied, bout = pieds[cote]
            path = skia.Path(); path.moveTo(x, hy); path.lineTo(*genou); path.lineTo(*pied); path.lineTo(*bout)
            c.drawPath(path, pt)
        path = skia.Path(); path.moveTo(x, hy); path.lineTo(ex, ey); path.lineTo(nx, ny)
        c.drawPath(path, pt)
        # bras (cinématique directe, référence « bas », accrochés à l'épaule)
        mains = {}
        for cote, ka, kc in (("g", "ep_g", "coude_g"), ("d", "ep_d", "coude_d")):
            coude, main, _ = _chaine(ex, ey, p[ka], OS["bras"], p[kc], OS["avant_bras"], face)
            path = skia.Path(); path.moveTo(ex, ey); path.lineTo(*coude); path.lineTo(*main)
            c.drawPath(path, pt)
            c.drawCircle(main[0], main[1], ep * 0.62, peinture(couleur))
            mains[cote] = main
        # tête
        if tete:
            tete_photo(c, tx, ty, r_tete, tete, zoom, fx, fy, 1.0, anneau, gris, miroir=(SENS_PHOTO.get(tete, face) != face))
        else:
            c.drawCircle(tx, ty, r_tete, peinture(FOND2))
            c.drawCircle(tx, ty, r_tete, peinture(couleur, Style=skia.Paint.kStroke_Style, StrokeWidth=ep * 0.72))
            visage(c, tx, ty, r_tete, expr, regard * face, couleur, ep)
        c.restore()
    M = lambda q: (x + (q[0] - x) * taille, sol + (q[1] - sol) * taille)
    return dict(tete=M((tx, ty)), cou=M((nx, ny)), epaule=M((ex, ey)), main_g=M(mains["g"]), main_d=M(mains["d"]),
                pied_g=M(pieds["g"][1]), pied_d=M(pieds["d"][1]), hanche=M((x, hy)), r=r_tete * taille, face=face)


# ───────────────────────────── le décor : rien, ou presque
def fond_bonhomme(c, t, sol=SOL, a_sol=0.55, grain=True):
    c.clear(hexa(FOND))
    # un halo très sombre au centre pour que le noir ne soit pas plat
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(AXE_HAUT, 900), 1100, [hexa("#17171C"), hexa(FOND)], [0.0, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    # la ligne de sol, blanche, qui respire
    trait(c, 60, sol, W - 60, sol, BLANC, 3, a_sol * (0.85 + 0.15 * math.sin(t * 1.3)))


def etiquette(c, cx, y, txt, u=1.0, alpha=1.0, taille=40, rouge=True):
    """le nom sous le bonhomme : pastille rouge, capitales blanches"""
    if u <= 0.005 or alpha <= 0.01: return
    w = largeur(txt, taille, "noir", 0.04) + 56
    s = mix(0.6, 1.0, rebond(borne(u), 1.4))
    c.save(); c.translate(cx, y); c.scale(s, s)
    rrect(c, -w / 2, -taille * 0.78, w, taille * 1.56, taille * 0.78, ROUGE if rouge else BLANC, alpha)
    texte(c, txt, 0, -taille * 0.62, taille, BLANC if rouge else NOIR, "noir", "centre", 0.04, alpha)
    c.restore()


def bulle(c, pt, lignes, t, t0, cote=1, taille=46, larg_max=520, alpha=1.0, duree=0.3, rouge=None):
    """une bulle de parole / pensée accrochée à la tête (pt = (x, y) centre de tête, r = rayon)."""
    if isinstance(lignes, str): lignes = [lignes]
    u = prog(t, t0, duree, lambda v: rebond(v, 1.5))
    if u <= 0.005: return
    tx, ty = pt["tete"]; r = pt["r"]
    lh = hauteurLigne(taille, "noir") * 1.02
    w = max(largeur(l, taille, "noir") for l in lignes) + 64
    h = lh * len(lignes) + 44
    # la bulle se place du côté `cote`, au-dessus de la tête, et reste dans la zone sûre
    bx = tx + cote * (r + 40)
    if cote > 0: bx = min(bx, LARG_T + 65 - w)
    else: bx = max(bx - w, 65)
    by = ty - r - h - 10
    by = max(by, 120)
    ax, ay = bx + (w * 0.18 if cote > 0 else w * 0.82), by + h          # ancre de la queue
    c.save(); c.translate(ax, ay); c.scale(u, u); c.translate(-ax, -ay)
    with Calque(c, alpha):
        fond_ = rouge or BLANC
        queue = skia.Path(); queue.moveTo(ax - 22, ay - 2); queue.lineTo(ax + 22, ay - 2)
        queue.lineTo(tx + cote * r * 0.55, ty - r * 0.75); queue.close()
        c.drawPath(queue, peinture(fond_))
        rrect(c, bx, by, w, h, 26, fond_)
        for k, l in enumerate(lignes):
            texte(c, l, bx + w / 2, by + 22 + k * lh, taille, BLANC if rouge else NOIR, "noir", "centre", -0.02)
    c.restore()


def pensee(c, pt, lignes, t, t0, cote=1, taille=44, alpha=1.0):
    """comme bulle, mais en nuage à petits ronds (ce qu'il pense, pas ce qu'il dit)"""
    u = prog(t, t0, 0.3, sortie)
    if u <= 0.005: return
    tx, ty = pt["tete"]; r = pt["r"]
    for k, (f, rr) in enumerate(((0.62, 9), (0.8, 15), (1.0, 22))):
        v = borne((u - 0.15 * k) / 0.55)
        if v > 0:
            c.drawCircle(tx + cote * r * (0.5 + 0.55 * f), ty - r * (0.75 + 0.7 * f), rr * v, peinture(BLANC, alpha))
    bulle(c, dict(tete=(tx, ty + 70), r=r + 80), lignes, t, t0 + 0.12, cote, taille, alpha=alpha)


# ───────────────────────────── accessoires simples (formes, pas d'images)
def coeur(c, cx, cy, r, couleur=ROUGE, alpha=1.0, rot=0.0):
    p = skia.Path()
    p.moveTo(0, r * 0.35)
    p.cubicTo(-r * 1.1, -r * 0.5, -r * 0.55, -r * 1.25, 0, -r * 0.45)
    p.cubicTo(r * 0.55, -r * 1.25, r * 1.1, -r * 0.5, 0, r * 0.35); p.close()
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(1.5, 1.5); c.drawPath(p, peinture(couleur, alpha)); c.restore()


def coeurs(c, pt, t, t0, n=5, alpha=1.0):
    """des cœurs qui montent au-dessus de la tête"""
    tx, ty = pt["tete"]; r = pt["r"]
    for k in range(n):
        tk = t0 + k * 0.22
        if t < tk: continue
        v = (t - tk) / 1.6
        if v > 1: continue
        x = tx + math.sin(k * 2.3) * r * 0.9 + 30 * math.sin(v * 6 + k)
        y = ty - r - 20 - v * 320
        coeur(c, x, y, 14 + 6 * (k % 3), ROUGE, alpha * (1 - v) ** 0.7)


def croix(c, cx, cy, r, t, t0, couleur=ROUGE, ep=18):
    """une grande croix rouge qui se dessine en deux traits"""
    u1 = prog(t, t0, 0.16, sortie); u2 = prog(t, t0 + 0.12, 0.16, sortie)
    if u1 > 0: trait(c, cx - r, cy - r, cx - r + 2 * r * u1, cy - r + 2 * r * u1, couleur, ep)
    if u2 > 0: trait(c, cx + r, cy - r, cx + r - 2 * r * u2, cy - r + 2 * r * u2, couleur, ep)


def trophee(c, cx, cy, h, couleur=BLANC, alpha=1.0):
    """une coupe simple : deux anses, un pied"""
    w = h * 0.7
    with Calque(c, alpha):
        p = skia.Path(); p.moveTo(cx - w / 2, cy - h); p.lineTo(cx + w / 2, cy - h)
        p.quadTo(cx + w / 2, cy - h * 0.3, cx, cy - h * 0.25); p.quadTo(cx - w / 2, cy - h * 0.3, cx - w / 2, cy - h); p.close()
        c.drawPath(p, peinture(couleur))
        for s in (-1, 1):
            a = skia.Path(); a.moveTo(cx + s * w / 2, cy - h * 0.92)
            a.quadTo(cx + s * w * 0.95, cy - h * 0.8, cx + s * w / 2, cy - h * 0.45)
            c.drawPath(a, peinture(couleur, Style=skia.Paint.kStroke_Style, StrokeWidth=h * 0.07, StrokeCap=skia.Paint.kRound_Cap))
        rrect(c, cx - w * 0.08, cy - h * 0.27, w * 0.16, h * 0.2, 4, couleur)
        rrect(c, cx - w * 0.3, cy - h * 0.08, w * 0.6, h * 0.08, 4, couleur)
        etoile_ = etoile(cx, cy - h * 0.62, h * 0.12)
        c.drawPath(etoile_, peinture(ROUGE))


def billets(c, cx, cy, w, t, t0, n=4, couleur=BLANC):
    """des billets qui tombent (de l'argent qui part, ou qui arrive)"""
    for k in range(n):
        tk = t0 + k * 0.14
        if t < tk: continue
        v = (t - tk) / 1.3
        if v > 1.0: continue
        x = cx + (k - n / 2) * w * 0.55 + 18 * math.sin(v * 5 + k)
        y = cy + v * 380
        c.save(); c.translate(x, y); c.rotate(25 * math.sin(v * 4 + k))
        rrect(c, -w / 2, -w * 0.3, w, w * 0.6, 6, couleur, (1 - v) ** 0.5)
        c.drawCircle(0, 0, w * 0.14, peinture(ROUGE, (1 - v) ** 0.5))
        texte(c, "€", 0, -w * 0.12, w * 0.24, BLANC, "noir", "centre", 0, (1 - v) ** 0.5)
        c.restore()


def tele(c, cx, cy, w, h, t, nom=None, u=1.0, alpha=1.0, t0=0.0, est_video=False, rogne=(0, 0, 0, 0)):
    """un poste de télé / un écran de téléphone géant, avec une photo ou un extrait dedans"""
    if u <= 0.005 or alpha <= 0.01: return
    s = mix(0.7, 1.0, sortie(borne(u)))
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha * borne(u * 3)):
        rrect(c, -w / 2 - 14, -h / 2 - 14, w + 28, h + 28, 22, BLANC)
        rrect(c, -w / 2, -h / 2, w, h, 12, FOND2)
        if nom:
            if est_video:
                video(c, nom, -w / 2, -h / 2, w, h, max(0.0, t - t0), 1.0, rayon=12, rogne=rogne)
            else:
                image_cover(c, nom, -w / 2, -h / 2, w, h, 1.0 + 0.02 * math.sin(t * 0.6), 0.5, 0.4, rayon=12)
        # deux pieds
        trait(c, -w * 0.25, h / 2 + 14, -w * 0.32, h / 2 + 60, BLANC, 10)
        trait(c, w * 0.25, h / 2 + 14, w * 0.32, h / 2 + 60, BLANC, 10)
    c.restore()


def photo_plein(c, t, nom, u=1.0, alpha=1.0, y=120, h=1100, zoom=1.0, fy=0.4, legende=None, gris=0.0):
    """une vraie photo, grande, posée à plat (pas de 3D) : elle glisse du bas et se pose"""
    if u <= 0.005 or alpha <= 0.01: return
    x, w = 90, LARG_T - 50
    dy = (1 - sortie(borne(u))) * 260
    c.save(); c.translate(0, dy)
    with Calque(c, alpha * borne(u * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 16, 16)
        c.drawRRect(rr, peinture(BLANC))
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 10, y + 10, w - 20, h - 20), 10, 10), doAntiAlias=True)
        if gris > 0.01:
            c.saveLayer(None, skia.Paint(ColorFilter=skia.ColorFilters.Matrix(
                [mix(1, .3, gris), mix(0, .59, gris), mix(0, .11, gris), 0, 0,
                 mix(0, .3, gris), mix(1, .59, gris), mix(0, .11, gris), 0, 0,
                 mix(0, .3, gris), mix(0, .59, gris), mix(1, .11, gris), 0, 0, 0, 0, 0, 1, 0])))
        image_cover(c, nom, x + 10, y + 10, w - 20, h - 20, zoom * (1 + 0.025 * math.sin(t * 0.45)), 0.5, fy)
        if gris > 0.01: c.restore()
        c.restore()
        if legende:
            etiquette(c, x + w / 2, y + h + 50, legende, 1.0, 1.0, 36)
    c.restore()


def chiffre_geant(c, txt, cx, cy, t, t0, taille=220, couleur=ROUGE, alpha=1.0):
    """un seul chiffre ou mot, énorme, qui claque"""
    u = prog(t, t0, 0.32, lambda v: rebond(v, 1.3))
    if u <= 0.005: return
    tl = ajuste(txt, LARG_T - 40, taille, "noir")
    c.save(); c.translate(cx, cy); c.scale(u, u)
    texte(c, txt, 0, -tl * 0.62, tl, couleur, "noir", "centre", -0.03, alpha)
    c.restore()


def larmes(c, pt, t, t0, alpha=1.0):
    tx, ty = pt["tete"]; r = pt["r"]
    for k, s in enumerate((-1, 1)):
        for j in range(3):
            tk = t0 + j * 0.5 + k * 0.2
            if t < tk: continue
            v = (t - tk) / 0.9
            if v > 1: continue
            x = tx + s * r * 0.4; y = ty + r * 0.1 + v * 300
            c.drawOval(skia.Rect.MakeXYWH(x - 9, y - 16, 18, 32), peinture("#8FD3FF", alpha * (1 - v)))


def zzz(c, pt, t, t0):
    tx, ty = pt["tete"]; r = pt["r"]
    for k in range(3):
        v = ((t - t0) / 1.4 + k / 3) % 1
        if t < t0: break
        texte(c, "z", tx + r * 0.9 + v * 120, ty - r * 0.9 - v * 160, 40 + 30 * v, BLANC, "noir", "centre", 0, (1 - v))


def points_interrogation(c, pt, t, t0, n=3):
    tx, ty = pt["tete"]; r = pt["r"]
    for k in range(n):
        u = prog(t, t0 + k * 0.14, 0.3, lambda v: rebond(v, 1.6))
        if u <= 0: continue
        a = -0.6 + k * 0.6
        x, y = tx + math.sin(a) * (r + 90), ty - math.cos(a) * (r + 90)
        c.save(); c.translate(x, y); c.scale(u, u)
        texte(c, "?", 0, -40, 64 + 10 * k, ROUGE, "noir", "centre")
        c.restore()


def sous_titres_bonhomme(K, fusions=None):
    """les mêmes sous-titres que la chaîne, sous la ligne de sol"""
    return sous_titres_people(K, fusions)


def casque(c, cx, cy, w, alpha=1.0, rot=0.0):
    """un casque de pompier : dôme rouge, visière, bande blanche. (cx, cy) = centre de la base."""
    with Calque(c, alpha):
        c.save(); c.translate(cx, cy); c.rotate(rot)
        h = w * 0.62
        dome = skia.Path(); dome.moveTo(-w * 0.42, 0); dome.quadTo(-w * 0.45, -h * 1.1, 0, -h * 1.1)
        dome.quadTo(w * 0.45, -h * 1.1, w * 0.42, 0); dome.close()
        c.drawPath(dome, peinture(ROUGE))
        rrect(c, -w * 0.55, -8, w * 1.1, 16, 8, ROUGE2)                 # la visière
        rrect(c, -w * 0.07, -h * 1.08, w * 0.14, h * 0.75, 6, BLANC)       # la crête
        trait(c, -w * 0.3, -h * 0.45, w * 0.3, -h * 0.45, BLANC, 6)
        c.restore()


def flammes(c, t, y, x0=80, x1=1000, n=9, h=120, alpha=1.0, graine=2):
    """une rangée de flammes rouges qui dansent sur la ligne de sol"""
    import random
    rd = random.Random(graine)
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n + rd.uniform(-30, 30)
        hh = h * (0.7 + 0.3 * rd.random()) * (0.85 + 0.15 * math.sin(t * (5 + k) + k))
        w = hh * 0.55
        p = skia.Path(); p.moveTo(x - w / 2, y); p.quadTo(x - w * 0.6, y - hh * 0.5, x, y - hh)
        p.quadTo(x + w * 0.6, y - hh * 0.5, x + w / 2, y); p.close()
        c.drawPath(p, peinture(ROUGE, alpha * 0.9))
        p2 = skia.Path(); p2.moveTo(x - w * 0.25, y); p2.quadTo(x - w * 0.3, y - hh * 0.3, x, y - hh * 0.55)
        p2.quadTo(x + w * 0.3, y - hh * 0.3, x + w * 0.25, y); p2.close()
        c.drawPath(p2, peinture(ROUGE2, alpha * 0.9))


def secousse_x(t, t0, amp=12, duree=0.5, freq=22.0):
    """décalage horizontal qui tremble puis s'éteint (pour un bonhomme qui s'énerve)"""
    if t < t0 or t > t0 + duree: return 0.0
    u = (t - t0) / duree
    return amp * math.sin((t - t0) * freq * 2 * math.pi) * (1 - u) ** 1.5


def barreaux(c, cx, cy, w, h, u=1.0, n=5, alpha=1.0):
    """des barreaux blancs qui descendent devant quelqu'un"""
    if u <= 0.005: return
    for k in range(n):
        x = cx - w / 2 + w * k / (n - 1)
        trait(c, x, cy - h / 2, x, cy - h / 2 + h * sortie(borne(u)), BLANC, 12, alpha)
    trait(c, cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2, BLANC, 12, alpha * borne(u * 3))


def livre(c, cx, cy, w, u=1.0, alpha=1.0, rot=-6.0):
    """un livre fermé : couverture blanche, tranche rouge"""
    if u <= 0.005: return
    h = w * 1.35
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(u, u)
    rrect(c, -w / 2 - 10, -h / 2 + 8, w, h, 6, ROUGE, alpha)
    rrect(c, -w / 2, -h / 2, w, h, 6, BLANC, alpha)
    trait(c, -w * 0.3, -h * 0.2, w * 0.3, -h * 0.2, NOIR, 6, alpha)
    trait(c, -w * 0.3, -h * 0.05, w * 0.2, -h * 0.05, NOIR, 6, alpha)
    c.restore()


def flash(c, cx, cy, t, t0, r=90, duree=0.35):
    """l'éclair d'un appareil photo"""
    if t < t0 or t > t0 + duree: return
    u = (t - t0) / duree
    c.drawCircle(cx, cy, r * (0.4 + 0.6 * u), peinture(BLANC, (1 - u) ** 1.5 * 0.9))
    for k in range(6):
        a = k * math.pi / 3 + 0.3
        trait(c, cx + math.cos(a) * r * 0.5, cy + math.sin(a) * r * 0.5, cx + math.cos(a) * r * (0.8 + 0.8 * u), cy + math.sin(a) * r * (0.8 + 0.8 * u), BLANC, 6, (1 - u) ** 2)


def pilule(c, cx, cy, w, alpha=1.0, rot=30.0):
    c.save(); c.translate(cx, cy); c.rotate(rot)
    rrect(c, -w / 2, -w * 0.2, w, w * 0.4, w * 0.2, BLANC, alpha)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, -w * 0.2, w / 2, w * 0.4))
    rrect(c, -w / 2, -w * 0.2, w, w * 0.4, w * 0.2, ROUGE, alpha)
    c.restore(); c.restore()


def telephone_main(c, pt, t, u=1.0, alpha=1.0, contenu=None):
    """un téléphone tenu devant soi (dans la main droite), avec un petit écran noir ; contenu(c, x, y, w, h) dessine dedans"""
    if u <= 0.005: return
    hx, hy = pt["main_d"]; w, h = 110, 190
    c.save(); c.translate(hx, hy - h * 0.55); c.scale(u, u)
    rrect(c, -w / 2 - 6, -h / 2 - 6, w + 12, h + 12, 18, BLANC, alpha)
    rrect(c, -w / 2, -h / 2, w, h, 12, FOND, alpha)
    if contenu: contenu(c, -w / 2, -h / 2, w, h)
    c.restore()


def gant(c, cx, cy, w, alpha=1.0, rot=0.0, couleur=NOIR, contour=BLANC, ep=6):
    """un gant en cuir vu de face, pouce à gauche. (cx, cy) = centre de la paume, w = largeur."""
    if alpha <= 0.01: return
    h = w * 1.25
    with Calque(c, alpha):
        c.save(); c.translate(cx, cy); c.rotate(rot)
        pt_f = peinture(couleur)
        pt_c = peinture(contour, Style=skia.Paint.kStroke_Style, StrokeWidth=ep,
                        StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        # les quatre doigts : des capsules qui montent de la paume
        doigts = ((-0.21, 0.52), (-0.04, 0.60), (0.13, 0.55), (0.29, 0.42))
        for dx, lg in doigts:
            x, dw = w * dx, w * 0.175
            y0, y1 = -h * 0.08, -h * lg
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - dw / 2, y1, x + dw / 2, y0), dw / 2, dw / 2)
            c.drawRRect(rr, pt_f); c.drawRRect(rr, pt_c)
        # le pouce, en biais à gauche
        c.save(); c.translate(-w * 0.40, h * 0.02); c.rotate(-38)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w * 0.10, -h * 0.34, w * 0.10, h * 0.08), w * 0.10, w * 0.10)
        c.drawRRect(rr, pt_f); c.drawRRect(rr, pt_c); c.restore()
        # la paume, par-dessus les attaches
        paume = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w * 0.38, -h * 0.18, w * 0.40, h * 0.34), w * 0.13, w * 0.13)
        c.drawRRect(paume, pt_f); c.drawRRect(paume, pt_c)
        # la bande de poignet
        band = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w * 0.34, h * 0.26, w * 0.36, h * 0.50), w * 0.07, w * 0.07)
        c.drawRRect(band, pt_f); c.drawRRect(band, pt_c)
        c.restore()


def banc(c, x0, x1, y, n=6, t=0.0, u=1.0, alpha=1.0, taille=0.30, ep=7):
    """une rangée de petits bonhommes sans visage, en fond : le jury, le public, une foule."""
    if u <= 0.005 or alpha <= 0.01: return
    for k in range(n):
        v = borne((u - 0.05 * k) / 0.5)
        if v <= 0: continue
        x = x0 + (x1 - x0) * (k + 0.5) / n
        bonhomme(c, x, respire(STAND, t + k * 0.7, 0.6), 1 if k % 2 else -1, None, "neutre",
                 u=v, alpha=alpha, taille=taille, sol=y, ep=ep, r_tete=R_TETE * 0.78)


def voiture(c, cx, cy, w, alpha=1.0, couleur=BLANC, encre=FOND, ep=6):
    """un 4x4 de profil, tourné vers la droite. (cx, cy) = milieu, au niveau des roues."""
    if alpha <= 0.01: return
    h = w * 0.46
    with Calque(c, alpha):
        caisse = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(cx - w / 2, cy - h * 0.52, cx + w / 2, cy), w * 0.05, w * 0.05)
        c.drawRRect(caisse, peinture(couleur))
        toit = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(cx - w * 0.34, cy - h * 1.02, cx + w * 0.30, cy - h * 0.46), w * 0.05, w * 0.05)
        c.drawRRect(toit, peinture(couleur))
        for x0, x1 in ((-0.30, -0.03), (0.02, 0.26)):          # les vitres
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(cx + w * x0, cy - h * 0.94, cx + w * x1, cy - h * 0.56), w * 0.02, w * 0.02)
            c.drawRRect(rr, peinture(encre))
        for rx in (-0.28, 0.29):                               # les roues
            c.drawCircle(cx + w * rx, cy, h * 0.30, peinture(couleur))
            c.drawCircle(cx + w * rx, cy, h * 0.13, peinture(encre))


def coche(c, cx, cy, r, t, t0, couleur=BLANC, ep=16):
    """une coche qui se trace en deux temps"""
    u1 = prog(t, t0, 0.14, sortie); u2 = prog(t, t0 + 0.12, 0.2, sortie)
    if u1 > 0: trait(c, cx - r, cy, cx - r + r * 0.75 * u1, cy + r * 0.72 * u1, couleur, ep)
    if u2 > 0: trait(c, cx - r * 0.25, cy + r * 0.72, cx - r * 0.25 + r * 1.3 * u2, cy + r * 0.72 - r * 1.5 * u2, couleur, ep)
