"""Style « cobalt » (CB-M15, 15/10/2026) : remplace le noir et or de CB-M13/CB-M14.

Choix tirés de ce qui retient l'attention :
- contraste de complémentaires bleu / orange : l'orange ressort sans effort sur le bleu (repérage pré-attentif),
  le bleu profond reste reposant sur la durée, l'orange chaud porte l'alerte ;
- mouvement « qui approche » (anneaux qui grandissent depuis le centre) : le cerveau surveille d'office ce qui vient
  vers lui, donc le fond n'est jamais immobile sans voler la vedette ;
- formes rondes (anneaux, orbes, cases arrondies) : préférées aux angles, perçues comme sûres.
Les cases fines, pastilles et tampons de noir.py s'utilisent tels quels : on remplace seulement leur accent.
"""
import math
import skia
from moteur import *
import noir

NUIT, COBALT = "#050D33", "#1433B8"
ORANGE, ORANGE2, CREME = "#FF7A1F", "#FFB46B", "#FFF3E4"
CYAN = "#5FD4FF"

noir.OR, noir.OR2 = ORANGE, ORANGE2          # les briques de noir.py prennent l'accent orange


def fond_cobalt(c, t, pulse=0.0):
    """bleu nuit → cobalt, anneaux qui approchent, orbes chaudes et froides qui dérivent, vignette"""
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42), H * 0.85, [hexa(COBALT), hexa("#0A1D7A"), hexa(NUIT)], [0.0, 0.45, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    # anneaux : partent du centre et grandissent (≈ 4 s chacun), plus visibles en approchant puis s'effacent
    for k in range(5):
        u = ((t * 0.25) + k / 5) % 1.0
        r = 80 + 1500 * u ** 1.6
        a = 0.10 * math.sin(math.pi * u) * (1 + 0.6 * pulse)
        c.drawCircle(W / 2, H * 0.45, r, peinture("#FFFFFF", a, Style=skia.Paint.kStroke_Style, StrokeWidth=2 + 6 * u))
    # orbes : une chaude, une froide
    for (x, y, r, col, a, v, ph) in [(240, 420, 520, ORANGE, 0.22, 0.23, 0.0), (860, 1480, 600, CYAN, 0.16, 0.19, 2.1),
                                     (900, 300, 360, "#7A5CFF", 0.14, 0.27, 4.0)]:
        cx = x + 90 * math.sin(t * v + ph); cy = y + 110 * math.cos(t * v * 0.8 + ph)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(col, a * (1 + 0.5 * pulse)), hexa(col, 0.0)]))
        c.drawCircle(cx, cy, r, p)
    # grain de points très fin, qui descend
    p = peinture("#FFFFFF", 0.05)
    dy = (t * 12) % 64
    for y in range(-64, H + 64, 64):
        for x in range(32, W, 64):
            c.drawCircle(x, y + 32 - dy, 1.4, p)
    v = skia.Paint(AntiAlias=True)
    v.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.8, [hexa("#000000", 0.0), hexa("#000000", 0.55)], [0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), v)
