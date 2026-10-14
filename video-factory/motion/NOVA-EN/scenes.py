"""NOVA, VERSION ANGLAISE (voix Tomy en anglais) — concept fictif « service & logiciel » pour la page /motion-design/ de dyou-agency.com (16:9, 14/10/2026).

Univers sombre vert nuit, accent menthe. Le chaos du lundi matin (e-mails, devis en retard, factures qui
volent) est aspiré dans l'icône NOVA ; tout se range dans un tableau de bord ; devis envoyé en un clic,
relances automatiques, paiement en ligne ; « Moins de tâches. Plus de temps. » ; signature et essai gratuit.
"""
import math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import (entre, pgrad, flou_calque, lettres, pill as _pill, curseur, clic, etoile4, eclats, rayons, lueur_s,
                    barre_progression, SousTitresEncre, rouleau, Groupe, iris, losange)

DUREE = 15.0
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

V = dict(nuit="#0B1715", nuit2="#10211E", verre="#152B27", ligne="#2A4A43", menthe="#3DF5A8", menthe2="#1FC79A",
         teal="#16A3A0", blanc="#F2FFF9", gris="#8FB3A8", rouge="#FF5C5C", ambre="#FFC24B")
GRAD_N = [V["menthe"], V["menthe2"], V["teal"]]
CX, CY = 960, 470
SOUS = SousTitresEncre(K, fusions={(1, 2): "8 a.m.", (3, 4): "40 emails,", (42, 43): "14 days."}, y=975, larg=1500, taille=42,
                       fam="fort", max_mots=7)

T = {k: TW(i) for k, i in dict(huit=1, quarante=3, devis=5, factures=9, avec=11, nova=12, tout=13, endroit=17, vos=18,
                                clic=24, relances=25, seules=29, clients=32, ligne=34, moins=35, plus=37, temps=38, fin=39,
                                essai=40, quatorze=42).items()}


# ─────────────────────────────────────────── briques sombres
def fond(c, t, pulse=0.0):
    c.clear(hexa(V["nuit"]))
    for x, y, r, col, a, v, ph in [(300, 200, 760, V["teal"], 0.22, 0.25, 0), (1650, 900, 820, V["menthe2"], 0.16, 0.2, 2),
                                   (1500, 120, 500, V["menthe"], 0.10, 0.3, 4)]:
        cx = x + 120 * math.sin(t * v + ph); cy = y + 90 * math.cos(t * v * 0.8 + ph)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r * (1 + 0.1 * pulse), [hexa(col, min(1, a * (1 + pulse))), hexa(col, 0.0)]))
        c.drawCircle(cx, cy, r * (1 + 0.1 * pulse), p)
    p = peinture(V["menthe"], 0.07)
    dx = (t * 10) % 60
    for y in range(30, H, 60):
        for x in range(-60, W + 60, 60):
            c.drawCircle(x + dx, y, 1.8, p)


def verre(c, x, y, w, h, r=28, alpha=1.0, contour=0.28, fond_=None):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    with Calque(c, alpha):
        p = skia.Paint(AntiAlias=True, Color=hexa("#000000", 0.45), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
        c.save(); c.translate(0, 20); c.drawRRect(rr, p); c.restore()
        c.drawRRect(rr, pgrad(x, y, x + w, y + h, [fond_ or V["verre"], V["nuit2"]]))
        c.drawRRect(rr, peinture(V["menthe"], contour, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        reflet = skia.Paint(AntiAlias=True)
        reflet.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + h * 0.5)], [hexa("#FFFFFF", 0.06), hexa("#FFFFFF", 0.0)]))
        c.drawRRect(rr, reflet)


def tuile_n(c, ic, cx, cy, taille, alpha=1.0, mode="grad"):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - taille / 2, cy - taille / 2, taille, taille), taille * 0.28, taille * 0.28)
    with Calque(c, alpha):
        if mode == "grad":
            lueur_s(c, cx, cy, taille * 1.1, V["menthe"], 0.25)
            c.drawRRect(rr, pgrad(cx - taille / 2, cy - taille / 2, cx + taille / 2, cy + taille / 2, GRAD_N))
            icone(c, ic, cx, cy, taille * 0.5, V["nuit"], 2.4)
        else:
            c.drawRRect(rr, peinture(V["menthe"], 0.12))
            icone(c, ic, cx, cy, taille * 0.5, V["menthe"], 2.2)


def pastille(c, label, cx, cy, taille=26, mode="menthe", icone_=None, alpha=1.0, s=1.0, rot=0.0):
    if alpha <= 0.01 or s <= 0.01: return 0
    tw = largeur(label, taille, "fort", -0.01)
    h = taille * 2.0; ic = taille * 1.1 if icone_ else 0
    w = tw + ic + (taille * 0.4 if icone_ else 0) + taille * 1.5
    fond_, coul = {"menthe": (V["menthe"], V["nuit"]), "verre": (V["verre"], V["blanc"]), "rouge": ("#3A1A1C", V["rouge"]),
                   "doux": ("#173A31", V["menthe"])}[mode]
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        c.drawRRect(rr, peinture(fond_))
        if mode in ("verre", "rouge"): c.drawRRect(rr, peinture(coul, 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        x = -w / 2 + taille * 0.75
        if icone_:
            icone(c, icone_, x + ic / 2, 0, ic, coul, 2.6); x += ic + taille * 0.4
        texte(c, label, x, -hauteurLigne(taille, "fort") / 2, taille, coul, "fort", track=-0.01)
    c.restore()
    return w


def logo_nova(c, cx, cy, taille, t, alpha=1.0):
    """icône NOVA : carré arrondi menthe, étoile à quatre branches qui tourne lentement"""
    tuile_n(c, "sparkle", cx, cy, taille, alpha) if False else None
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - taille / 2, cy - taille / 2, taille, taille), taille * 0.3, taille * 0.3)
    with Calque(c, alpha):
        lueur_s(c, cx, cy, taille * 1.3, V["menthe"], 0.35)
        c.drawRRect(rr, pgrad(cx - taille / 2, cy - taille / 2, cx + taille / 2, cy + taille / 2, GRAD_N))
        etoile4(c, cx, cy, taille * 0.32, V["nuit"], 1.0, t * 0.6)
        disque(c, cx + taille * 0.2, cy - taille * 0.2, taille * 0.06, V["nuit"])


# ─────────────────────────────────────────── 1. le chaos du lundi
RNG = np.random.default_rng(3)
MAILS = [(RNG.uniform(120, 1800), RNG.uniform(90, 860), RNG.uniform(-14, 14), RNG.uniform(0, 1.4)) for _ in range(14)]
FACTS = [(RNG.uniform(150, 1770), RNG.uniform(120, 820), RNG.uniform(-25, 25), k) for k in range(7)]


def aspire(t, x, y):
    """vers l'icône NOVA, à « Avec NOVA »"""
    u = prog(t, T["avec"] - 0.05, 0.5, entree)
    return mix(x, CX, u), mix(y, CY, u), 1 - u


def chaos(c, t):
    if t > T["tout"] + 0.1: return
    sx, sy = secousse(t, T["factures"] + 0.3, 8, 0.4)
    c.save(); c.translate(sx, sy)
    # notifications d'e-mails qui tombent partout
    for k, (x, y, rot, d) in enumerate(MAILS):
        t0 = T["quarante"] - 0.1 + d * 0.5
        a = entre(t, t0, 0.35, 2.0)
        if a <= 0: continue
        x2, y2, k_ = aspire(t, x, y)
        if k_ <= 0.01: continue
        c.save(); c.translate(x2, y2); c.rotate(rot * k_); c.scale(mix(0.3, 1, a) * k_, mix(0.3, 1, a) * k_)
        verre(c, -150, -38, 300, 76, 20)
        tuile_n(c, "mail", -108, 0, 44, 1.0, "doux")
        rrect(c, -72, -14, 150, 10, 5, V["ligne"]); rrect(c, -72, 6, 100, 10, 5, V["ligne"])
        disque(c, 128, -24, 9, V["rouge"])
        c.restore()
    # factures qui volent
    for (x, y, rot, k) in FACTS:
        t0 = T["factures"] - 0.1 + 0.06 * k
        a = entre(t, t0, 0.4, 1.6)
        if a <= 0: continue
        x2, y2, k_ = aspire(t, x + 40 * math.sin(t * 2 + k), y)
        if k_ <= 0.01: continue
        c.save(); c.translate(x2, y2); c.rotate((rot + 30 * (1 - a) + 4 * math.sin(t * 3 + k)) * k_); c.scale(k_ * mix(1.6, 1, a), k_ * mix(1.6, 1, a))
        rrect(c, -80, -105, 160, 210, 12, "#E9F5F0", borne(a * 3))
        texte(c, "INVOICE", -60, -88, 20, "#2E4A43", "titre", track=0.08, alpha=borne(a * 3))
        for j in range(5): rrect(c, -60, -44 + 26 * j, 120 - 24 * (j % 2), 9, 4, "#BFD6CE", borne(a * 3))
        c.restore()
    # l'horloge et le compteur d'e-mails, au centre
    a = entre(t, -0.2, 0.5, 1.4)
    x2, y2, k_ = aspire(t, CX, 330)
    if k_ > 0.01:
        c.save(); c.translate(x2, y2); c.scale(k_, k_)
        verre(c, -330, -150, 660, 300, 40, borne(a * 3), 0.4)
        texte(c, "MONDAY", -270, -112, 34, V["gris"], "titre", track=0.18, alpha=borne(a * 3))
        hh = "08:00" if t > T["huit"] else "07:59"
        texte(c, hh, -275, -70, 150, V["blanc"], "noir", track=-0.03, alpha=borne(a * 3))
        b = entre(t, T["quarante"] - 0.1, 0.4, 2.2)
        if b > 0:
            c.save(); c.translate(250, -10); c.scale(b, b)
            disque(c, 0, 0, 86, V["rouge"], 1.0, (10, 30, 0.4))
            n = int(borne((t - T["quarante"]) / 0.45) * 40)
            texte(c, str(max(1, n)), 0, -hauteurLigne(70) / 2, 70, "#FFFFFF", "noir", "centre", -0.03)
            c.restore()
            icone(c, "mail", 250, 110, 44, V["gris"], 2.2)
        c.restore()
    # trois devis en retard
    for k in range(3):
        t0 = T["devis"] - 0.1 + 0.12 * k
        a = entre(t, t0, 0.4, 2.0)
        if a <= 0: continue
        x2, y2, k_ = aspire(t, 560 + 400 * k, 720)
        if k_ <= 0.01: continue
        c.save(); c.translate(x2, y2); c.rotate((-6 + 6 * k) * k_); c.scale(k_ * mix(0.4, 1, a), k_ * mix(0.4, 1, a))
        verre(c, -170, -62, 340, 124, 22, 1.0, 0.0, "#2A1719")
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -62, 340, 124), 22, 22), peinture(V["rouge"], 0.6, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        texte(c, f"Quote #01{27 + k}", -140, -40, 28, V["blanc"], "titre", track=-0.01)
        pastille(c, "Overdue", -60, 26, 18, "rouge", "triangle-alert")
        c.restore()
    c.restore()


# ─────────────────────────────────────────── 2. NOVA : l'icône, puis le tableau de bord
def apparition_nova(c, t):
    t0 = T["avec"] + 0.25
    if t < t0 - 0.1 or t > T["vos"]: return
    a = entre(t, t0 - 0.05, 0.5, 2.2)
    o = prog(t, T["tout"] - 0.05, 0.35, entreeSortie)
    rayons(c, CX, CY, t, 1300, 0.12 * a * (1 - o), 16, V["menthe"])
    onde(c, CX, CY, t, t0, 100, 700, V["menthe"], 10, 0.6)
    logo_nova(c, mix(CX, 410, o), mix(CY, 200, o), mix(220, 70, o) * mix(0.3, 1, a), t, borne(a * 3) * (1 - prog(t, T["endroit"], 0.3)))
    if o < 1:
        lettres(c, "NOVA", CX, CY + 150, 110, t, T["nova"] - 0.05, "masque", grad=True, cols=GRAD_N, decal=0.05, alpha=1 - o)


def tableau(c, t):
    """tableau de bord : tout arrive au même endroit"""
    t0 = T["tout"] - 0.1
    if t < t0 or t > T["clients"] + 0.2: return
    a = entre(t, t0, 0.55, 1.3)
    zo = prog(t, T["vos"] - 0.15, 0.45, entreeSortie)       # on plonge vers la carte devis
    x, y, w, h = 300, 90, 1320, 800
    c.save(); c.translate(CX, CY); s = mix(0.85, 1, a) * mix(1, 1.6, zo); c.scale(s, s); c.translate(-CX - 380 * zo, -CY + 60 * zo)
    with Calque(c, borne(a * 3) * (1 - prog(t, T["clic"] + 0.4, 0.3)) * mix(1, 0.3, zo)):
        verre(c, x, y, w, h, 36, 1.0, 0.3)
        logo_nova(c, x + 70, y + 66, 64, t)
        texte(c, "NOVA", x + 120, y + 44, 38, V["blanc"], "noir", track=0.04)
        menu = [("inbox", "Inbox"), ("file-text", "Quotes"), ("receipt", "Invoices"), ("refresh-cw", "Follow-ups")]
        for k, (ic, lab) in enumerate(menu):
            yy = y + 160 + 74 * k
            act = k == 1 and t > T["vos"] - 0.2
            if act: rrect(c, x + 26, yy - 30, 230, 60, 16, V["menthe"], 0.14)
            icone(c, ic, x + 64, yy, 30, V["menthe"] if act else V["gris"], 2.2)
            texte(c, lab, x + 96, yy - hauteurLigne(28, "fort") / 2, 28, V["blanc"] if act else V["gris"], "fort", track=0)
        trait(c, x + 280, y + 120, x + 280, y + h - 30, V["ligne"], 2)
        # trois colonnes qui se remplissent de cartes rangées
        cols = [("Inbox", "mail"), ("Quotes", "file-text"), ("Invoices", "receipt")]
        for j, (nom, ic) in enumerate(cols):
            cx0 = x + 320 + j * 330
            texte(c, nom.upper(), cx0, y + 120, 22, V["gris"], "titre", track=0.14)
            for k in range(4):
                tk = T["tout"] + 0.05 + 0.07 * (k * 3 + j)
                b = entre(t, tk, 0.4, 1.8)
                if b <= 0: continue
                yy = y + 170 + 120 * k - 60 * (1 - b)
                verre(c, cx0, yy, 300, 100, 20, borne(b * 3), 0.18, "#1A3631")
                tuile_n(c, ic, cx0 + 50, yy + 50, 52, borne(b * 3), "doux")
                rrect(c, cx0 + 92, yy + 34, 150 - 30 * (k % 2), 11, 5, V["ligne"], borne(b * 3))
                rrect(c, cx0 + 92, yy + 58, 100, 11, 5, V["ligne"], borne(b * 3))
                if j == 1 and k == 0:
                    pastille(c, "Ready", cx0 + 250, yy + 32, 15, "menthe", None, borne(b * 3))
    c.restore()


# ─────────────────────────────────────────── 3. le devis part en un clic
def devis_envoye(c, t):
    t0 = T["vos"] - 0.1
    if t < t0 or t > T["relances"] + 0.1: return
    a = entre(t, t0, 0.5, 1.4)
    env = prog(t, T["clic"] + 0.12, 0.32, entree)
    o = prog(t, T["relances"] - 0.25, 0.3, entree)
    cx, cy = CX + 1100 * env, 450 - 300 * env
    sc = 1.2 * mix(0.6, 1, a) * mix(1, 0.4, env)
    c.save(); c.translate(cx, cy); c.rotate(-18 * env); c.scale(sc, sc)
    with Calque(c, borne(a * 3)):
        verre(c, -330, -230, 660, 460, 34, 1.0, 0.35)
        texte(c, "QUOTE #0128", -280, -192, 26, V["gris"], "titre", track=0.12)
        texte(c, "Kitchen renovation", -280, -148, 48, V["blanc"], "titre", track=-0.02)
        for j in range(3):
            rrect(c, -280, -60 + 46 * j, 360, 12, 6, V["ligne"]); rrect(c, 180, -60 + 46 * j, 100, 12, 6, V["ligne"])
        trait(c, -280, 90, 280, 90, V["ligne"], 2)
        ap = prog(t, T["clic"] - 0.06, 0.06, sortie) * (1 - prog(t, T["clic"] + 0.05, 0.12, sortie))
        ok = t > T["clic"] + 0.05
        sb = 1 - 0.06 * ap
        c.save(); c.translate(150, 160); c.scale(sb, sb)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-130, -40, 260, 80), 40, 40)
        c.drawRRect(rr, pgrad(-130, 0, 130, 0, GRAD_N))
        texte(c, "Sent" if ok else "Send", -20 if ok else -30, -hauteurLigne(30, "titre") / 2, 30, V["nuit"], "titre", "centre", -0.01)
        icone(c, "check" if ok else "send", 80, 0, 30, V["nuit"], 2.8)
        c.restore()
    c.restore()
    if env < 0.05:
        cu = prog(t, T["clic"] - 0.5, 0.42, sortie)
        if cu > 0:
            ap = prog(t, T["clic"] - 0.06, 0.06, sortie) * (1 - prog(t, T["clic"] + 0.05, 0.12, sortie))
            curseur(c, mix(1500, 1150, cu), mix(900, 660, cu), 1.1, 1.0, ap)
    clic(c, 1140, 642, t, T["clic"], V["menthe"])
    # l'avion en papier qui file
    if env > 0:
        trait(c, 1140, 640, cx, cy, V["menthe"], 4, 0.5 * (1 - env))
    pc = 0
    eclats(c, 1140, 642, t, T["clic"] + 0.04, 12, 260, [V["menthe"], V["blanc"], V["teal"], V["ambre"]], graine=7)
    if pc > 0:
        pastille(c, "Quote sent", CX, 470, 44, "menthe", "circle-check", borne(pc * 3), mix(0.4, 1, pc))
        eclats(c, CX, 470, t, T["clic"] + 0.3, 14, 380, [V["menthe"], V["blanc"], V["teal"], V["ambre"]], graine=7)


# ─────────────────────────────────────────── 4. relances automatiques
def relances(c, t):
    t0 = T["relances"] - 0.15
    if t < t0 or t > T["clients"] + 0.1: return
    g = prog(t, T["clients"] - 0.3, 0.35, entree)
    a = entre(t, t0, 0.5, 1.4)
    c.save(); c.translate(0, -700 * g)
    with Calque(c, borne(a * 3)):
        # l'interrupteur « Relance auto »
        verre(c, 260, 330, 560, 280, 36, 1.0, 0.3)
        texte(c, "Auto follow-up", 310, 380, 46, V["blanc"], "titre", track=-0.02)
        on = prog(t, T["relances"] + 0.3, 0.25, sortie)
        sx, sy = 310, 490
        rrect(c, sx, sy, 170, 84, 42, V["menthe"] if on > 0.5 else V["ligne"])
        disque(c, sx + 42 + 86 * on, sy + 42, 34, "#FFFFFF", 1.0, (4, 12, 0.3))
        texte(c, "On" if on > 0.5 else "Off", sx + 200, sy + 22, 32, V["menthe"] if on > 0.5 else V["gris"], "fort", track=0)
        # la frise J+3, J+7, J+14 qui se coche toute seule
        xs = [1020, 1270, 1520]
        for k, lab in enumerate(["Day 3", "Day 7", "Day 14"]):
            tk = T["relances"] + 0.45 + 0.22 * k
            b = entre(t, tk, 0.4, 2.0)
            if k > 0:
                u = prog(t, tk - 0.15, 0.2, sortie)
                trait(c, xs[k - 1] + 70, 470, xs[k - 1] + 70 + (xs[k] - xs[k - 1] - 140) * u, 470, V["menthe"], 5)
            if b <= 0: continue
            c.save(); c.translate(xs[k], 470); c.scale(mix(0.3, 1, b), mix(0.3, 1, b))
            verre(c, -70, -70, 140, 140, 34, 1.0, 0.4)
            icone(c, "mail", 0, -12, 46, V["menthe"], 2.2)
            texte(c, lab, 0, 22, 26, V["blanc"], "titre", "centre", 0)
            ck = entre(t, tk + 0.15, 0.3, 2.4)
            if ck > 0:
                disque(c, 56, -56, 26 * ck, V["menthe"]); icone(c, "check", 56, -56, 30 * ck, V["nuit"], 3.2)
            c.restore()
        b = entre(t, T["seules"] - 0.1, 0.4, 2.0)
        if b > 0: pastille(c, "On autopilot", 1270, 650, 28, "doux", "zap", borne(b * 3), mix(0.4, 1, b), -3)
    c.restore()


# ─────────────────────────────────────────── 5. paiement en ligne
def ecran_paiement(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(V["nuit2"]))
    paye = t > T["ligne"] + 0.05
    texte(c, "Invoice F-0412", x + 36, y + 110, 30, V["blanc"], "titre", track=-0.01)
    texte(c, "Kitchen renovation", x + 36, y + 152, 24, V["gris"], "demi", track=0)
    for j in range(3): rrect(c, x + 36, y + 230 + 44 * j, w - 72 - 40 * j, 12, 6, V["ligne"])
    bx, by = x + 36, y + h - 200
    if not paye:
        rrect(c, bx, by, w - 72, 90, 45, V["menthe"])
        texte(c, "Pay online", x + w / 2, by + 45 - hauteurLigne(30, "titre") / 2, 30, V["nuit"], "titre", "centre", -0.01)
    else:
        u = entre(t, T["ligne"] + 0.05, 0.4, 2.4)
        lueur_s(c, x + w / 2, by + 10, 220, V["menthe"], 0.35 * u)
        disque(c, x + w / 2, by + 10, 70 * u, V["menthe"]); icone(c, "check", x + w / 2, by + 10, 70 * u, V["nuit"], 3.4)
        texte(c, "Paid", x + w / 2, by + 100, 40, V["menthe"], "noir", "centre", -0.02, borne(u * 2))


def paiement(c, t):
    t0 = T["clients"] - 0.2
    if t < t0 or t > T["moins"] - 0.1: return
    a = entre(t, t0, 0.5, 1.4)
    o = prog(t, T["moins"] - 0.4, 0.28, entree)
    c.save(); c.translate(0, -500 * o)
    with Calque(c, borne(a * 3) * (1 - o)):
        with Espace(c, 1250, 470, ry=mix(-40, -12, a), rz=4):
            telephone_s_n(c, 1250, 470, 400, 800, lambda cc, x, y, w, h: ecran_paiement(cc, x, y, w, h, t))
        lettres(c, "Paid", 560, 300, 170, t, T["clients"] - 0.1, "ressort", grad=True, cols=GRAD_N, decal=0.05)
        lettres(c, "online.", 560, 480, 110, t, T["ligne"] - 0.1, "masque", grad=False, couleur=V["blanc"], decal=0.03)
        if t > T["ligne"] + 0.05:
            confettis(c, 1250, 600, t, T["ligne"] + 0.05, n=26, rayon=420, graine=2, cols=[V["menthe"], V["blanc"], V["teal"], V["ambre"]])
    c.restore()


def telephone_s_n(c, cx, cy, w, h, ecran):
    x, y = cx - w / 2, cy - h / 2; k = w / 480
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 72 * k, 72 * k)
    p = skia.Paint(AntiAlias=True, Color=hexa("#000000", 0.5), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
    c.save(); c.translate(0, 30); c.drawRRect(rr, p); c.restore()
    c.drawRRect(rr, pgrad(x, y, x + w, y + h, ["#3C5A53", "#0A1412", "#2E4A43"]))
    ex, ey, ew, eh = x + 14 * k, y + 14 * k, w - 28 * k, h - 28 * k
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(ex, ey, ew, eh), 58 * k, 58 * k), doAntiAlias=True)
    ecran(c, ex, ey, ew, eh)
    c.restore()
    rrect(c, cx - 58 * k, y + 28 * k, 116 * k, 32 * k, 16 * k, "#000000")


# ─────────────────────────────────────────── 6. moins de tâches, plus de temps
def moins_plus(c, t):
    t0 = T["moins"] - 0.12
    if t < t0 or t > T["fin"] + 0.1: return
    o = prog(t, T["fin"] - 0.32, 0.22, entree)
    with Calque(c, 1 - o):
        lettres(c, "Fewer tasks.", 160, 200, 120, t, T["moins"] - 0.05, "masque", grad=False, couleur=V["blanc"], decal=0.025, align="gauche")
        lettres(c, "More time.", 160, 380, 128, t, T["plus"] - 0.05, "ressort", grad=True, cols=GRAD_N, decal=0.035, align="gauche")
        # la liste de tâches qui se raye et disparaît
        for k, lab in enumerate(["Chase Mr. Smith", "Redo the quote", "Find the invoice"]):
            tk = T["moins"] + 0.05 + 0.12 * k
            b = entre(t, tk - 0.2, 0.35, 1.6)
            if b <= 0: continue
            dis = prog(t, T["plus"] - 0.2 + 0.06 * k, 0.3, entree)
            yy = 600 + 90 * k
            with Calque(c, borne(b * 3) * (1 - dis)):
                verre(c, 160 - 200 * dis, yy, 560, 70, 18, 1.0, 0.2)
                anneau(c, 200 - 200 * dis, yy + 35, 14, V["menthe"], 3)
                texte(c, lab, 232 - 200 * dis, yy + 35 - hauteurLigne(28, "fort") / 2, 28, V["blanc"], "fort", track=0)
                r = prog(t, tk, 0.2, sortie)
                trait(c, 225 - 200 * dis, yy + 36, 225 - 200 * dis + 460 * r, yy + 36, V["menthe"], 4)
        # l'horloge qui s'ouvre en grand
        a = entre(t, T["plus"] - 0.1, 0.6, 1.4)
        if a > 0:
            cx, cy, R = 1500, 470, 270 * mix(0.4, 1, a)
            lueur_s(c, cx, cy, R * 1.8, V["menthe"], 0.22 * a)
            anneau(c, cx, cy, R, V["ligne"], 26)
            u = prog(t, T["plus"], 1.4, sortie)
            arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), -90, 300 * u)
            pa = pgrad(cx - R, cy - R, cx + R, cy + R, GRAD_N); pa.setStyle(skia.Paint.kStroke_Style); pa.setStrokeWidth(26); pa.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawPath(arc, pa)
            ang = math.radians(-90 + 300 * u)
            trait(c, cx, cy, cx + R * 0.62 * math.cos(ang), cy + R * 0.62 * math.sin(ang), V["blanc"], 12)
            trait(c, cx, cy, cx + R * 0.4 * math.cos(ang * 0.2 - 1), cy + R * 0.4 * math.sin(ang * 0.2 - 1), V["blanc"], 14)
            disque(c, cx, cy, 20, V["menthe"])


# ─────────────────────────────────────────── 7. signature
def signature(c, t):
    t0 = T["fin"] - 0.12
    if t < t0: return
    a = entre(t, t0, 0.6, 1.8)
    rayons(c, CX, 360, t, 1400, 0.10 * a, 16, V["menthe"])
    onde(c, CX, 360, t, t0 + 0.1, 100, 900, V["menthe"], 10, 0.7)
    logo_nova(c, CX, 300, 200 * mix(0.3, 1, a), t, borne(a * 3))
    lettres(c, "NOVA", CX, 440, 150, t, T["fin"] - 0.05, "ressort", grad=False, couleur=V["blanc"], decal=0.06)
    b = entre(t, T["essai"] - 0.1, 0.45, 2.0)
    if b > 0:
        pastille(c, "Free trial · 14 days", CX - 190, 700, 30, "doux", "sparkles", borne(b * 3), mix(0.4, 1, b))
        bt = entre(t, T["quatorze"], 0.45, 2.0)
        if bt > 0:
            c.save(); c.translate(CX + 260, 700); c.scale(mix(0.4, 1, bt) * (1 + 0.03 * max(0, math.sin((t - T["quatorze"] - 0.6) * 5))), mix(0.4, 1, bt))
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-160, -46, 320, 92), 46, 46)
            lueur_s(c, 0, 0, 220, V["menthe"], 0.25)
            c.drawRRect(rr, pgrad(-160, 0, 160, 0, GRAD_N))
            texte(c, "Get started", -22, -hauteurLigne(32, "titre") / 2, 32, V["nuit"], "titre", "centre", -0.01)
            icone(c, "arrow-right", 100, 0, 32, V["nuit"], 2.8)
            c.restore()
    if t > DUREE - 1.6:
        texte(c, "Fictional concept · a DYOU Studio film", W - 60, H - 70, 20, V["gris"], "demi", "droite", 0.04, prog(t, DUREE - 1.6, 0.4))


# ─────────────────────────────────────────── sons
son(0.0, "impact", -8); son(0.0, "tick", -10)
for k in range(5): son(0.1 + 0.2 * k, "tick", -16)
son(T["huit"], "ding", -12)
for k in range(14): son(T["quarante"] - 0.1 + MAILS[k][3] * 0.5, "message_in", -16 - (k % 3) * 2)
for k in range(3): son(T["devis"] - 0.1 + 0.12 * k, "croc", -12)
for k in range(7): son(T["factures"] - 0.1 + 0.06 * k, "swipe", -15)
son(T["factures"] + 0.3, "impact_doux", -10)
son(T["avec"] - 0.05, "whoosh_long", -8); son(T["avec"] + 0.25, "impact", -6); son(T["avec"] + 0.3, "verre", -10); son(T["nova"], "ching", -12)
son(T["tout"] - 0.1, "whoosh", -10)
for k in range(12): son(T["tout"] + 0.05 + 0.07 * k, "pop", -18)
son(T["vos"] - 0.15, "whoosh_court", -10); son(T["clic"], "clic", -6); son(T["clic"] + 0.2, "whoosh", -9); son(T["clic"] + 0.25, "check", -10)
son(T["relances"] - 0.15, "swipe", -11); son(T["relances"] + 0.3, "clic", -9)
for k in range(3): son(T["relances"] + 0.45 + 0.22 * k, "pop", -12); son(T["relances"] + 0.6 + 0.22 * k, "check", -14)
son(T["clients"] - 0.2, "whoosh_court", -10); son(T["ligne"] + 0.05, "ching", -8); son(T["ligne"] + 0.08, "tampon", -12)
son(T["moins"] - 0.15, "whoosh", -10)
for k in range(3): son(T["moins"] + 0.05 + 0.12 * k, "frappe", -14)
son(T["plus"] - 0.1, "montee", -10); son(T["plus"] + 0.2, "impact_doux", -10)
son(T["fin"] - 0.2, "whoosh_bas", -8); son(T["fin"] - 0.05, "impact", -6); son(T["fin"], "ching", -10)
son(T["essai"] - 0.1, "pop", -12); son(T["quatorze"], "pop", -12)
son(DUREE - 1.3, "ding", -16)
for a, b in [(T["avec"] - 0.05, T["avec"] + 0.5), (T["clic"] + 0.15, T["clic"] + 0.6), (T["fin"] - 0.2, T["fin"] + 0.2)]: rapide(a, b)
for tt, cc_, a_ in [(T["avec"] + 0.25, "#FFFFFF", 0.3), (T["ligne"] + 0.05, V["menthe"], 0.10), (T["fin"] - 0.05, "#FFFFFF", 0.2)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    fond(c, t, battement(t, T["avec"] + 0.25, 1, 0.5) + battement(t, T["fin"] - 0.05, 1, 0.5) - 2)
    chaos(c, t)
    apparition_nova(c, t)
    tableau(c, t)
    devis_envoye(c, t)
    relances(c, t)
    paiement(c, t)
    moins_plus(c, t)
    signature(c, t)
    K.dessine_eclairs(c, t)
    if t < T["fin"] - 0.2: SOUS.dessine(c, t, V["blanc"])
