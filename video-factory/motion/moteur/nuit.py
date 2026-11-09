"""Pièce en perspective bleu nuit — décor DROP&YOU (28/10/2026).

Demande de Youssef : « je veux faire fond bleu foncé comme ça en perspective qui bouge pour
DROP&YOU, avec les couleurs de DY-M14 ». C'est le décor de `people.py` (la chaîne RECTO CERVEAU)
porté aux couleurs de la maison : au lieu du noir et du rouge, le bleu nuit et le bleu vif du
thème glace, ceux de DY-M14.

Ce module ne fournit QUE le décor et sa palette. Tout le reste d'une vidéo DROP&YOU ne bouge pas :
cartes en verre de `glace.py`, paires détourées, mockups, et la fin en `signature.py` (produits
aspirés → explosion → DROP&YOU recomposé en 3D). On remplace le fond, pas la grammaire.

    from kit import *
    import glace; glace.appliquer()
    import nuit
    ...
    def dessine(c, t):
        nuit.fond(c, t, vitesse=nuit.vitesse(t, pivots))   # toujours en premier
        ...                                                 # le reste comme d'habitude

Le principe qui a fait AC-M02 et qu'on garde : **la profondeur raconte**. Ce qui arrive vient du
point de fuite et grandit, ce qui disparaît y repart. Le sol avance toujours un peu — c'est ce
mouvement lent « qui approche » qui tient l'œil sans voler la vedette au produit.
"""
import math
import numpy as np
import skia
import moteur
from moteur import *

# ───────────────────────────── palette : celle de DY-M14 (thème glace), rien d'inventé
FOND, FOND2, FOND3 = "#050917", "#0B1430", "#152046"
BLEU, BLEU_VIF, GLACIER = "#5B8CFF", "#3D7BFF", "#8FB4FF"
BLANC, BLANC2 = "#F3F6FF", "#C9D2EE"
GRIS = "#5E6788"
ROUGE, OR, VERT = "#FF4D5E", "#FFC53D", "#2BD67B"

# ───────────────────────────── grille de page (zone sûre TikTok / Snap du 17/10/2026)
AXE = 500          # contenu SOUS y 816 : la colonne de boutons TikTok mord à droite (x > 860)
AXE_HAUT = 540     # au-dessus de y 816 il n'y a aucun bouton
HORIZON = 700.0    # hauteur du point de fuite
SOL = 1180.0       # constante de fuite du sol : y = HORIZON + SOL / z

_GRAIN = None


def _grain(c, t):
    """grain d'image : un bruit clair et fixe, pour que le bleu ne soit pas un aplat mort"""
    rng = np.random.default_rng(11)
    p = peinture(BLANC, 0.030)
    for x, y, r in rng.uniform([0, 0, 0.8], [W, H, 2.2], size=(520, 3)):
        c.drawCircle(float(x), float(y), float(r), p)


def fond(c, t, pulse=0.0, vitesse=0.55, densite=1.0):
    """bleu nuit + sol quadrillé BLEU VIF qui avance vers nous + plafond glacier + halo au fond.

    vitesse : lignes de sol franchies par seconde. Le décor avance toujours un peu."""
    global _GRAIN
    c.clear(hexa(FOND))
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeRadial(skia.Point(AXE, HORIZON), H * 0.80,
                                               [hexa(FOND3, 1.0), hexa(FOND2, 1.0), hexa(FOND, 1.0)],
                                               [0.0, 0.40, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)

    phase = (t * vitesse) % 1.0
    # ── sol : lignes bleu vif qui se resserrent vers l'horizon et avancent vers nous
    for k in range(1, 17):
        z = k - phase
        if z <= 0.35: continue
        y = HORIZON + SOL / z
        if y > H + 40: continue
        a = 0.70 * min(1.0, (z - 0.3) / 1.6) * densite
        a *= min(1.0, (y - HORIZON) / 60)
        trait(c, -60, y, W + 60, y, BLEU_VIF, max(1.8, 5.4 / z), a)
    # ── sol : fuyantes, qui convergent vers le point de fuite
    for k in range(-9, 10):
        x_sol = AXE + k * 320
        a = 0.44 * densite * (1 - min(1.0, abs(k) / 11))
        trait(c, AXE + (x_sol - AXE) * 0.045, HORIZON + SOL / 16, x_sol, H + 200, BLEU_VIF, 3.2, a)
    # ── plafond : le même quadrillage en glacier, discret, qui répond en haut
    for k in range(1, 11):
        z = k - phase
        if z <= 0.4: continue
        y = HORIZON - SOL * 0.62 / z
        if y < -40: continue
        trait(c, -60, y, W + 60, y, GLACIER, max(1.2, 3.4 / z),
              0.17 * densite * min(1.0, (z - 0.35) / 1.8))
    for k in range(-6, 7):
        x_h = AXE + k * 360
        trait(c, AXE + (x_h - AXE) * 0.05, HORIZON - SOL * 0.62 / 10, x_h, -200, GLACIER,
              2.2, 0.14 * densite * (1 - min(1.0, abs(k) / 8)))

    # ── halo au point de fuite : la pièce a une source de lumière, et elle bat
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(AXE, HORIZON), 580,
                                               [hexa(BLEU_VIF, 0.34 * (1 + 0.35 * pulse)),
                                                hexa(BLEU_VIF, 0.0)]))
    c.drawCircle(AXE, HORIZON, 580, p)

    if _GRAIN is None:
        s = surface(); _grain(s.getCanvas(), 0); _GRAIN = s.makeImageSnapshot()
    c.drawImage(_GRAIN, 0, 0)

    v = skia.Paint(AntiAlias=True)
    v.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.82,
                                               [hexa("#000000", 0.0), hexa("#000000", 0.60)], [0.40, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), v)


def vitesse(t, pivots=(), base=0.5, coup=2.6, large=0.55):
    """le décor accélère sur les bascules du récit : passer les temps forts en `pivots`"""
    v = base
    for t0 in pivots:
        v += coup * max(0.0, 1 - abs(t - t0) / large) ** 2
    return v


def echelle_z(z):
    """facteur d'échelle d'un objet placé à la profondeur z (1 = au premier plan)"""
    return 1.0 / max(0.25, z)


def pose_sol(c, cx, y_bas, w, a=0.28, couleur=None):
    """lueur bleue au sol sous un objet : sur un fond sombre une ombre ne dit rien, c'est le
    halo qui ancre l'objet dans la pièce et l'empêche d'avoir l'air collé sur un fond."""
    rx = max(24.0, w * 0.62)
    ry = max(8.0, w * 0.105)
    yy = y_bas + 8
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, yy), rx,
                                               [hexa(couleur or BLEU_VIF, min(0.62, a * 2.0)),
                                                hexa(couleur or BLEU_VIF, 0.0)]))
    c.save(); c.translate(cx, yy); c.scale(1.0, ry / rx); c.translate(-cx, -yy)
    c.drawCircle(cx, yy, rx, p)
    c.restore()


def halo(c, rr, a=0.30, flou=24, couleur=None):
    """le halo d'un cadre : à la place de l'ombre portée, invisible sur un fond sombre"""
    p = skia.Paint(AntiAlias=True, Color=hexa(couleur or BLEU_VIF, a),
                   MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, flou))
    c.drawRRect(rr, p)


def arrivee(c, t, x, y, w, h, u, dessin, z0=5.0, rot=0.0):
    """pose un objet qui VIENT DU FOND : petit au point de fuite, il grandit jusqu'à sa place.

    `dessin(c)` dessine l'objet dans son repère final (x, y, w, h) ; le reste est géré ici."""
    if u <= 0.005: return
    cx, cy = x + w / 2, y + h / 2
    z = mix(z0, 1.0, sortieExpo(borne(u)))
    s = echelle_z(z)
    px = mix(AXE, cx, sortieExpo(borne(u)))
    py = mix(HORIZON, cy, sortieExpo(borne(u)))
    c.save(); c.translate(px, py); c.rotate(rot * (1 - u)); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, borne(u * 3)):
        pose_sol(c, cx, y + h, w, 0.26)
        dessin(c)
    c.restore()


def ondes_sol(c, t, t0, a=1.0, n=5, vitesse_o=0.78, couleur=None):
    """anneaux qui partent du point de fuite et viennent vers nous, à même le sol.
    C'est ce qui tient le bas de l'écran quand il n'y a que du texte (règle « jamais de vide »)."""
    if a <= 0.01: return
    for k in range(n):
        u = ((t - t0) * vitesse_o + k / n) % 1.0
        z = mix(7.0, 0.55, u ** 1.5)
        y = HORIZON + SOL / z
        rx = 1500 / z
        al = a * 0.58 * math.sin(math.pi * min(1.0, u * 1.08)) ** 0.7
        if y > H + 500 or al <= 0.01: continue
        c.drawOval(skia.Rect.MakeXYWH(AXE - rx, y - rx * 0.20, 2 * rx, 0.40 * rx),
                   peinture(couleur or BLEU_VIF, al, Style=skia.Paint.kStroke_Style,
                            StrokeWidth=4 + 22 * (1 - z / 7)))
