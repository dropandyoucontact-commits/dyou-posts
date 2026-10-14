"""FORMA — concept fictif « marque & produit » pour la page /motion-design/ de dyou-agency.com (16:9, 14/10/2026).

Fond blanc, typographie orange et encre. Une gourde isotherme dessinée (ombrage cylindrique, reflet métal) :
la goutte qui tombe, froid 24 h / chaud 12 h, acier et zéro plastique, le sac et la main, cinq couleurs qui
se fondent en une seule forme, puis le logotype « FORMA. Une marque. Un réflexe. »
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import entre, pgrad, flou_calque, lettres, etoile4, eclats, rayons, lueur_s, SousTitresEncre, rouleau, losange

DUREE = 13.0
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

F = dict(blanc="#FFFFFF", creme="#FFF6EE", orange="#FF5B1F", orange2="#FF8A3D", encre="#17120E", gris="#8A817A",
         ligne="#F0E6DD", glace="#5FA8E8")
COULEURS = [("#FF5B1F", "#C93F0C"), ("#25211E", "#0C0A09"), ("#93AE8E", "#5E7A5A"), ("#86B9EA", "#4E86C0"), ("#EFE2CC", "#C7B595")]
GRAD_O = [F["orange"], F["orange2"]]
CX, CY = 960, 470
SOUS = SousTitresEncre(K, fusions={(10, 11): "24 heures,", (15, 16): "12 heures."}, y=975, larg=1500, taille=42, fam="fort", max_mots=7)

T = {k: TW(i) for k, i in dict(eau=1, fraiche=2, toute=3, forma=6, froid=9, vingt=10, chaud=14, douze=15, acier=17, zero=19,
                                elle=21, sac=25, main=29, cinq=30, couleurs=31, une=32, forme=34, fin=35, marque=37, reflexe=39).items()}


def fond(c, t):
    c.clear(hexa(F["blanc"]))
    p = skia.Paint(AntiAlias=True)
    cx = 1500 + 80 * math.sin(t * 0.4); cy = 200 + 60 * math.cos(t * 0.3)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), 900, [hexa("#FFE9DC", 0.9), hexa("#FFE9DC", 0.0)]))
    c.drawCircle(cx, cy, 900, p)
    p2 = skia.Paint(AntiAlias=True)
    p2.setShader(skia.GradientShader.MakeRadial(skia.Point(200, 950), 700, [hexa("#FFF1E6", 0.9), hexa("#FFF1E6", 0.0)]))
    c.drawCircle(200, 950, 700, p2)


# ─────────────────────────────────────────── la gourde
def chemin_gourde(cx, cy, h):
    """silhouette : bouchon, col, épaules arrondies, corps ; (cx, cy) = centre ; h = hauteur totale"""
    w = h * 0.30
    top = cy - h / 2
    corps = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, top + h * 0.22, w, h * 0.78), w * 0.32, w * 0.32)
    col = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w * 0.34, top + h * 0.13, w * 0.68, h * 0.14), w * 0.12, w * 0.12)
    bouchon = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w * 0.38, top + h * 0.03, w * 0.76, h * 0.12), w * 0.14, w * 0.14)
    return w, top, corps, col, bouchon


def gourde(c, cx, cy, h, couleur=0, t=0.0, reflet=None, alpha=1.0, logo=True, ombre=True):
    if alpha <= 0.01 or h < 4: return
    base, fonce = COULEURS[couleur] if isinstance(couleur, int) else couleur
    w, top, corps, col, bouchon = chemin_gourde(cx, cy, h)
    with Calque(c, alpha):
        if ombre:
            p = skia.Paint(AntiAlias=True, Color=hexa("#5A2A10", 0.16), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, h * 0.03))
            c.drawOval(skia.Rect.MakeXYWH(cx - w * 0.75, cy + h / 2 - h * 0.02, w * 1.5, h * 0.06), p)
        # anse du bouchon
        anneau(c, cx, top + h * 0.03, w * 0.2, "#2A2420", w * 0.07)
        x0, x1 = cx - w / 2, cx + w / 2
        cyl = [hexa(fonce), hexa(base), hexa("#FFFFFF", 1.0), hexa(base), hexa(fonce)]
        for rr, dark in [(bouchon, True), (col, True), (corps, False)]:
            pc = skia.Paint(AntiAlias=True)
            cols = [hexa("#110E0C"), hexa("#3B342F"), hexa("#6B625B"), hexa("#2A2420"), hexa("#110E0C")] if dark else \
                   [hexa(fonce), hexa(base), mix_couleur(base, "#FFFFFF", 0.35), hexa(base), hexa(fonce)]
            pc.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)], cols, [0.0, 0.32, 0.42, 0.62, 1.0]))
            c.drawRRect(rr, pc)
        # bague métal entre col et corps
        rrect(c, cx - w * 0.36, top + h * 0.215, w * 0.72, h * 0.018, h * 0.009, "#CFC8C2")
        if logo:
            lw = largeur("FORMA", w * 0.17, "noir", 0.12)
            claire = couleur in (4,) if isinstance(couleur, int) else False
            texte(c, "FORMA", cx - lw / 2, cy + h * 0.06, w * 0.17, F["encre"] if claire else "#FFFFFF", "noir", track=0.12, alpha=0.92)
        if reflet is not None and 0 < reflet < 1:
            c.save(); c.clipRRect(corps, doAntiAlias=True)
            p = skia.Paint(AntiAlias=True); xr = mix(x0 - w, x1 + w, reflet)
            p.setShader(skia.GradientShader.MakeLinear([skia.Point(xr - w * 0.5, top), skia.Point(xr + w * 0.5, top + h * 0.3)],
                                                       [hexa("#FFFFFF", 0), hexa("#FFFFFF", 0.75), hexa("#FFFFFF", 0)]))
            c.drawRect(skia.Rect.MakeXYWH(x0, top, w, h), p); c.restore()


def mix_couleur(a, b, u):
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]; cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    r, g, bb = [round(x + (y - x) * u) for x, y in zip(ca, cb)]
    return skia.Color(r, g, bb, 255)


def contour_gourde(c, cx, cy, h, couleur, ep, alpha=1.0):
    w, top, corps, col, bouchon = chemin_gourde(cx, cy, h)
    pa = peinture(couleur, alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=ep)
    for rr in (bouchon, col, corps): c.drawRRect(rr, pa)


def pastille_o(c, label, cx, cy, taille, icone_=None, mode="blanc", alpha=1.0, s=1.0, rot=0.0):
    if alpha <= 0.01: return
    tw = largeur(label, taille, "fort", -0.01)
    h = taille * 2.0; ic = taille * 1.1 if icone_ else 0
    w = tw + ic + (taille * 0.4 if icone_ else 0) + taille * 1.5
    fond_, coul = {"blanc": ("#FFFFFF", F["encre"]), "orange": (F["orange"], "#FFFFFF"), "encre": (F["encre"], "#FFFFFF")}[mode]
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        p = skia.Paint(AntiAlias=True, Color=hexa("#7A3A10", 0.14), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
        c.save(); c.translate(0, 10); c.drawRRect(rr, p); c.restore()
        c.drawRRect(rr, peinture(fond_))
        if mode == "blanc": c.drawRRect(rr, peinture(F["ligne"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        x = -w / 2 + taille * 0.75
        if icone_:
            icone(c, icone_, x + ic / 2, 0, ic, F["orange"] if mode == "blanc" else "#FFFFFF", 2.6); x += ic + taille * 0.4
        texte(c, label, x, -hauteurLigne(taille, "fort") / 2, taille, coul, "fort", track=-0.01)
    c.restore()


# ─────────────────────────────────────────── 1. la goutte, fraîche, toute la journée
def ouverture(c, t):
    if t > T["forma"] + 0.1: return
    o = prog(t, T["forma"] - 0.25, 0.3, entree)
    with Calque(c, 1 - o):
        lettres(c, "Votre eau.", 160, 170, 150, t, -0.05, "masque", grad=False, couleur=F["encre"], decal=0.03, align="gauche")
        lettres(c, "Fraîche.", 160, 340, 150, t, T["fraiche"] - 0.08, "ressort", grad=True, cols=GRAD_O, decal=0.04, align="gauche")
        lettres(c, "Toute la journée.", 160, 520, 96, t, T["toute"] - 0.08, "masque", grad=False, couleur=F["encre"], decal=0.025, align="gauche")
        # la goutte
        gx, sol = 1380, 640
        u = prog(t, -0.1, T["eau"] + 0.1, entree)
        if u < 1:
            gy = mix(-80, sol, u)
            p = skia.Path(); r = 46
            p.moveTo(gx, gy - r * 2.1); p.cubicTo(gx + r * 0.2, gy - r * 1.3, gx + r, gy - r * 0.6, gx + r, gy)
            p.arcTo(skia.Rect.MakeXYWH(gx - r, gy - r, 2 * r, 2 * r), 0, 180, False)
            p.cubicTo(gx - r, gy - r * 0.6, gx - r * 0.2, gy - r * 1.3, gx, gy - r * 2.1); p.close()
            c.drawPath(p, pgrad(gx - r, gy - 2 * r, gx + r, gy + r, [F["orange2"], F["orange"]]))
        ts = T["eau"] + 0.02
        if t >= ts:
            for k in range(3):
                v = prog(t, ts + 0.12 * k, 0.9, sortie)
                if 0 < v < 1:
                    pa = peinture(F["orange"], 1 - v, Style=skia.Paint.kStroke_Style, StrokeWidth=6 * (1 - v) + 1)
                    c.drawOval(skia.Rect.MakeXYWH(gx - 300 * v, sol - 60 * v, 600 * v, 120 * v), pa)
            for k in range(8):
                v = prog(t, ts, 0.55, sortie)
                if v < 1:
                    a = math.pi + k * math.pi / 7
                    disque(c, gx + 180 * v * math.cos(a), sol + 160 * v * math.sin(a) + 260 * v * v, 12 * (1 - v), F["orange"], 1 - v)
        # fraîche : cristaux qui naissent autour du point d'impact
        for k in range(7):
            a = entre(t, T["fraiche"] + 0.04 * k, 0.4, 2.0)
            if a <= 0: continue
            ang = k * 2 * math.pi / 7 + t * 0.4
            x, y = gx + 230 * math.cos(ang), 440 + 170 * math.sin(ang)
            c.save(); c.translate(x, y); c.rotate(t * 40 + k * 20); c.scale(a, a)
            icone(c, "snowflake", 0, 0, 54 + 10 * (k % 3), F["glace"], 2.2)
            c.restore()
        # toute la journée : un soleil qui traverse l'arc du jour
        if t > T["toute"] - 0.15:
            a = prog(t, T["toute"] - 0.15, 0.3, sortie)
            pa = peinture(F["orange"], 0.45 * a, Style=skia.Paint.kStroke_Style, StrokeWidth=4); pa.setPathEffect(skia.DashPathEffect.Make([10, 12], 0))
            arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(1080, 340, 600, 600), 180, 180); c.drawPath(arc, pa)
            u = prog(t, T["toute"], 0.75, entreeSortie)
            ang = math.pi + math.pi * u
            sx, sy = 1380 + 300 * math.cos(ang), 640 + 300 * math.sin(ang)
            lueur_s(c, sx, sy, 120, F["orange2"], 0.5 * a)
            icone(c, "sun" if u < 0.55 else "moon", sx, sy, 70, F["orange"], 2.6, a)


# ─────────────────────────────────────────── 2. la gourde : 24 h froid, 12 h chaud
def scene_gourde(c, t):
    t0 = T["forma"] - 0.15
    if t < t0 or t > T["elle"] + 0.1: return
    a = prog(t, t0, 0.6, lambda v: ressort(v, 1.2, 4.0))
    sor = prog(t, T["elle"] - 0.25, 0.3, entree)
    h = 680; cy = mix(CY + 900, CY + 50, a) - 800 * sor
    rot = 6 * math.sin(t * 1.3) * (1 - prog(t, T["acier"] - 0.2, 0.4, sortie))
    rf = prog(t, T["acier"] - 0.05, 0.6, entreeSortie)
    rf2 = prog(t, T["acier"] + 0.65, 0.5, entreeSortie)
    with Calque(c, 1 - sor):
        c.save(); c.translate(CX, cy); c.rotate(rot); c.translate(-CX, -cy)
        gourde(c, CX, cy, h, 0, t, reflet=(rf if rf < 1 else rf2))
        c.restore()
        lettres(c, "FORMA", CX, 36, 56, t, T["forma"] - 0.05, "masque", grad=False, couleur=F["orange"], decal=0.04, track=0.12)
        # FROID — 24 h
        b = entre(t, T["froid"] - 0.12, 0.5, 1.6) * (1 - prog(t, T["acier"] - 0.3, 0.3, entree))
        if b > 0:
            c.save(); c.translate(mix(CX, 470, sortie(min(1, b))), 470); c.scale(mix(0.4, 1, b), mix(0.4, 1, b))
            with Calque(c, borne(b * 3)):
                carte(c, -230, -170, 460, 340, 40, "#FFFFFF", 1.0, (20, 50, 0.10), F["ligne"], 2)
                icone(c, "snowflake", -150, -90, 70, F["glace"], 2.6)
                texte(c, "FROID", -100, -112, 30, F["gris"], "titre", track=0.18)
                n = rouleau_num(t, T["vingt"] - 0.1, T["vingt"] + 0.35, 24)
                texte(c, f"{n} h", -190, -40, 150, F["glace"], "noir", track=-0.04)
            c.restore()
        # CHAUD — 12 h
        b = entre(t, T["chaud"] - 0.12, 0.5, 1.6) * (1 - prog(t, T["acier"] - 0.3, 0.3, entree))
        if b > 0:
            c.save(); c.translate(mix(CX, 1450, sortie(min(1, b))), 470); c.scale(mix(0.4, 1, b), mix(0.4, 1, b))
            with Calque(c, borne(b * 3)):
                carte(c, -230, -170, 460, 340, 40, "#FFFFFF", 1.0, (20, 50, 0.10), F["ligne"], 2)
                fl = 1 + 0.08 * math.sin(t * 14)
                c.save(); c.translate(-150, -90); c.scale(fl, 1 / fl); icone(c, "flame", 0, 0, 70, F["orange"], 2.6); c.restore()
                texte(c, "CHAUD", -100, -112, 30, F["gris"], "titre", track=0.18)
                n = rouleau_num(t, T["douze"] - 0.1, T["douze"] + 0.3, 12)
                texte(c, f"{n} h", -190, -40, 150, F["orange"], "noir", track=-0.04)
            c.restore()
        # ACIER INOXYDABLE / ZÉRO PLASTIQUE : repères qui partent de la gourde
        for k, (lab, ic, tk, side) in enumerate([("Acier inoxydable", "shield-check", T["acier"], -1), ("Zéro plastique", "circle-slash", T["zero"], 1)]):
            b = entre(t, tk - 0.1, 0.45, 1.8)
            if b <= 0: continue
            y0 = 400 + 150 * k
            xa = CX + side * 130; xb = CX + side * 420
            u = prog(t, tk - 0.1, 0.3, sortie)
            disque(c, xa, y0, 10, F["encre"], borne(b * 3))
            trait(c, xa, y0, xa + (xb - xa) * u, y0, F["encre"], 3, borne(b * 3))
            pastille_o(c, lab, xb + side * 190, y0, 34, ic, "blanc" if k == 0 else "orange", borne(b * 3), mix(0.4, 1, b))


def rouleau_num(t, t0, t1, cible):
    u = borne((t - t0) / max(0.05, t1 - t0))
    return max(1, int(round(sortie(u) * cible)))


# ─────────────────────────────────────────── 3. le sac et la main
def sac_main(c, t):
    t0 = T["elle"] - 0.15
    if t < t0 or t > T["cinq"] + 0.05: return
    o = prog(t, T["cinq"] - 0.25, 0.25, entree)
    with Calque(c, 1 - o):
        lettres(c, "Elle tient partout.", CX, 40, 80, t, T["elle"] - 0.05, "masque", grad=False, couleur=F["encre"], decal=0.02)
        for k, (lab, ic, tk) in enumerate([("dans le sac", "backpack", T["sac"]), ("dans la main", "hand", T["main"])]):
            b = entre(t, tk - 0.35, 0.5, 1.5)
            if b <= 0: continue
            cx = 600 + 720 * k
            c.save(); c.translate(cx, 520); c.scale(mix(0.5, 1, b), mix(0.5, 1, b))
            with Calque(c, borne(b * 3)):
                carte(c, -280, -330, 560, 640, 48, "#FFFFFF" if k == 0 else F["orange"], 1.0, (24, 60, 0.12), F["ligne"] if k == 0 else None, 2)
                col = F["orange"] if k == 0 else "#FFFFFF"
                if k == 0:
                    d = prog(t, tk - 0.1, 0.4, lambda v: rebond(v, 1.4))
                    icone(c, ic, 0, 30, 300, col, 1.6)
                    c.save(); c.clipRect(skia.Rect.MakeXYWH(-280, -330, 560, 222))
                    gourde(c, 0, mix(-560, -150, d), 240, 1, t, ombre=False)
                    c.restore()
                else:
                    g = 4 * math.sin(t * 6)
                    gourde(c, 10, -90 + g, 300, 4, t, ombre=False)
                    icone(c, ic, 0, 70, 260, col, 1.6)
                texte(c, lab, 0, 220, 40, F["encre"] if k == 0 else "#FFFFFF", "titre", "centre", -0.02)
            c.restore()
            if t > tk:
                c.save(); c.translate(cx + 220, 230)
                ck = entre(t, tk, 0.35, 2.4)
                disque(c, 0, 0, 40 * ck, F["encre"]); icone(c, "check", 0, 0, 44 * ck, "#FFFFFF", 3.2)
                c.restore()


# ─────────────────────────────────────────── 4. cinq couleurs, une seule forme
def couleurs(c, t):
    t0 = T["cinq"] - 0.12
    if t < t0 or t > T["fin"] + 0.05: return
    o = prog(t, T["fin"] - 0.2, 0.22, entree)
    conv = prog(t, T["une"] - 0.05, 0.5, entreeSortie)
    # le fond prend la couleur de la gourde qui vient de tomber
    k_act = min(4, int(max(0, (t - T["cinq"]) / 0.14)))
    if conv < 1:
        bg = COULEURS[k_act][0]
        c.drawRect(skia.Rect.MakeWH(W, H), peinture(bg, 0.12 * (1 - conv) * (1 - o)))
    with Calque(c, 1 - o):
        lettres(c, "Cinq couleurs.", 160, 40, 96, t, T["cinq"] - 0.05, "ressort", grad=False, couleur=F["encre"], decal=0.03, align="gauche")
        lettres(c, "Une seule forme.", 1760, 40, 96, t, T["une"] - 0.05, "masque", grad=True, cols=GRAD_O, decal=0.03, align="gauche") if False else None
        if t > T["une"] - 0.05:
            w = largeur("Une seule forme.", 96, "noir", -0.03)
            lettres(c, "Une seule forme.", 1760 - w, 40, 96, t, T["une"] - 0.05, "masque", grad=True, cols=GRAD_O, decal=0.03, align="gauche")
        for k in (4, 3, 2, 1, 0):
            tk = T["cinq"] + 0.14 * k - 0.05
            a = prog(t, tk, 0.5, lambda v: ressort(v, 1.4, 4.2))
            if a <= 0: continue
            x = mix(CX + (k - 2) * 300, CX, conv)
            y = mix(-500, 560, a)
            gourde(c, x, y, 620, k, t, alpha=borne(1 - conv * 1.6) if k != 0 else 1.0, logo=conv < 0.3 or k == 0)
        if conv > 0:
            contour_gourde(c, CX, 560, 620 * mix(1, 1.08, conv), F["orange"], 5, conv)
            eclats(c, CX, 560, t, T["forme"] - 0.05, 14, 460, [F["orange"], F["orange2"], F["encre"], "#FFD3BD"], graine=9)


# ─────────────────────────────────────────── 5. signature
def signature(c, t):
    t0 = T["fin"] - 0.1
    if t < t0: return
    a = entre(t, t0, 0.5, 1.6)
    lueur_s(c, CX, 360, 800, F["orange2"], 0.18 * a)
    lettres(c, "FORMA", CX, 200, 300, t, T["fin"] - 0.05, "ressort", grad=True, cols=GRAD_O, decal=0.06, track=0.04)
    lettres(c, "Une marque.", CX - 300, 560, 64, t, T["marque"] - 0.1, "masque", grad=False, couleur=F["encre"], decal=0.03)
    lettres(c, "Un réflexe.", CX + 300, 560, 64, t, T["reflexe"] - 0.1, "masque", grad=False, couleur=F["encre"], decal=0.03)
    for k in range(5):
        b = entre(t, T["reflexe"] + 0.3 + 0.08 * k, 0.45, 1.8)
        if b <= 0: continue
        disque(c, CX + (k - 2) * 70, 740, 22 * b, COULEURS[k][0])
        if k == 4: anneau(c, CX + (k - 2) * 70, 740, 22 * b, F["ligne"], 2)
    if t > DUREE - 1.6:
        texte(c, "Concept fictif · film DYOU Studio", W - 60, H - 70, 20, F["gris"], "demi", "droite", 0.04, prog(t, DUREE - 1.6, 0.4))


# ─────────────────────────────────────────── sons
son(0.0, "whoosh_bas", -12); son(T["eau"], "pop", -6); son(T["eau"] + 0.02, "impact_doux", -9)
son(T["fraiche"] - 0.08, "verre", -10)
for k in range(7): son(T["fraiche"] + 0.04 * k, "tick", -18)
son(T["toute"] - 0.1, "whoosh_long", -12); son(T["toute"] + 0.7, "ding", -16)
son(T["forma"] - 0.15, "whoosh", -8); son(T["forma"] + 0.3, "impact", -7)
son(T["froid"] - 0.12, "pop", -11)
for i in range(8): son(T["vingt"] - 0.1 + i * 0.055, "tick", -17)
son(T["chaud"] - 0.12, "pop", -11)
for i in range(6): son(T["douze"] - 0.1 + i * 0.065, "tick", -17)
son(T["acier"] - 0.05, "ching", -9); son(T["acier"], "pop", -12); son(T["zero"], "pop", -12); son(T["zero"] + 0.05, "croc", -14)
son(T["elle"] - 0.25, "whoosh", -10); son(T["sac"] - 0.1, "whoosh_court", -11); son(T["sac"] + 0.25, "impact_doux", -10)
son(T["sac"], "check", -13); son(T["main"] - 0.35, "pop", -12); son(T["main"], "check", -13)
for k in range(5): son(T["cinq"] + 0.14 * k - 0.05, "pop", -9 - k)
son(T["une"] - 0.05, "whoosh_long", -10); son(T["forme"] - 0.05, "ching", -10)
son(T["fin"] - 0.15, "whoosh_bas", -8); son(T["fin"] - 0.05, "impact", -6)
son(T["marque"] - 0.1, "pop", -13); son(T["reflexe"] - 0.1, "pop", -13)
for k in range(5): son(T["reflexe"] + 0.3 + 0.08 * k, "blip", -16)
son(DUREE - 1.3, "ding", -16)
for a, b in [(T["forma"] - 0.15, T["forma"] + 0.25), (T["une"] - 0.05, T["une"] + 0.4), (T["fin"] - 0.15, T["fin"] + 0.2)]: rapide(a, b)
for tt, cc_, a_ in [(T["eau"], F["orange"], 0.06), (T["forma"] + 0.3, F["orange"], 0.08), (T["fin"] - 0.05, F["orange"], 0.10)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    fond(c, t)
    ouverture(c, t)
    scene_gourde(c, t)
    sac_main(c, t)
    couleurs(c, t)
    signature(c, t)
    K.dessine_eclairs(c, t)
    if t < T["fin"] - 0.2: SOUS.dessine(c, t, F["encre"])
