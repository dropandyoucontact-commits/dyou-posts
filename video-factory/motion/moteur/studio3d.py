"""Studio clair en vraie perspective (DA-M10 → DA-M14, 16/10/2026) — pubs US « on fait décoller ton business ».

Demande de Youssef : même style que DA-M06/DA-M07, mais accroche et motion plus forts, « beau, en perspective ».
- Petit moteur 3D : points (x, y, z) → caméra (orbite ax/ay) → projection ; chaque plan est une carte dessinée en 2D
  puis plaquée sur son quadrilatère projeté (setPolyToPoly, perspective juste) ; faces arrière éliminées, tri par profondeur.
- Briques : post gris (la pub « classique »), post motion (vivant), boîte extrudée, sol quadrillé.
- Corps commun plus court (motion design → captivé → résultat → site → script/animation/accroches),
  puis la fin « We make your business take off with videos like this » : fusée qui décolle d'une courbe en 3D, puis CTA.
"""
import math
import skia
from moteur import *
from studio import *
import studio

FOC = 1700.0


# ─────────────────────────────────────────── géométrie
def rot3(p, ax=0.0, ay=0.0, az=0.0):
    x, y, z = p
    if az:
        a = math.radians(az); x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
    if ay:
        a = math.radians(ay); x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
    if ax:
        a = math.radians(ax); y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    return (x, y, z)


class Cam:
    """caméra : orbite (ax, ay, az) autour de l'origine, puis recul tz ; écran centré sur (cx, cy)"""
    def __init__(self, ax=0.0, ay=0.0, az=0.0, tz=0.0, cx=540.0, cy=900.0, tx=0.0, ty=0.0):
        self.ax, self.ay, self.az, self.tz, self.cx, self.cy, self.tx, self.ty = ax, ay, az, tz, cx, cy, tx, ty

    def vue(self, p):
        x, y, z = rot3(p, self.ax, self.ay, self.az)
        return (x + self.tx, y + self.ty, z + self.tz)

    def proj(self, p):
        x, y, z = self.vue(p)
        z = max(z, -FOC * 0.85)
        k = FOC / (FOC + z)
        return (self.cx + x * k, self.cy + y * k, z)


def coins(centre, w, h, ax=0.0, ay=0.0, az=0.0):
    """les 4 coins (haut-gauche, haut-droit, bas-droit, bas-gauche) d'un plan w×h tourné puis posé en `centre`"""
    cx, cy, cz = centre
    out = []
    for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        X, Y, Z = rot3((x, y, 0.0), ax, ay, az)
        out.append((X + cx, Y + cy, Z + cz))
    return out


class Plan:
    """un plan à dessiner : coins 3D, taille de la carte, fonction dessin(c, w, h)"""
    def __init__(self, pts, w, h, dessin, alpha=1.0, recto=True):
        self.pts, self.w, self.h, self.dessin, self.alpha, self.recto = pts, w, h, dessin, alpha, recto


def plaque(c, cam, pl):
    P = [cam.proj(p) for p in pl.pts]
    aire = sum(P[i][0] * P[(i + 1) % 4][1] - P[(i + 1) % 4][0] * P[i][1] for i in range(4))
    if pl.recto and aire <= 0: return False
    if pl.alpha <= 0.003: return False
    m = skia.Matrix()
    ok = m.setPolyToPoly([skia.Point(0, 0), skia.Point(pl.w, 0), skia.Point(pl.w, pl.h), skia.Point(0, pl.h)],
                         [skia.Point(x, y) for x, y, _ in P])
    if not ok: return False
    c.save(); c.concat(m)
    with Calque(c, pl.alpha):
        pl.dessin(c, pl.w, pl.h)
    c.restore()
    return True


def scene3d(c, cam, plans):
    """dessine les plans du plus lointain au plus proche"""
    def prof(pl): return sum(cam.vue(p)[2] for p in pl.pts) / 4
    for pl in sorted(plans, key=prof, reverse=True):
        plaque(c, cam, pl)


def boite(centre, w, h, d, faces, ax=0.0, ay=0.0, az=0.0, alpha=1.0):
    """boîte extrudée : faces = dict(avant, arriere, gauche, droite, haut, bas) → fonction dessin(c, w, h) ; renvoie des Plans"""
    cx, cy, cz = centre
    def pose(dx, dy, dz, fw, fh, fax, fay):
        loc = coins((0, 0, 0), fw, fh, fax, fay)
        out = []
        for p in loc:
            q = (p[0] + dx, p[1] + dy, p[2] + dz)
            X, Y, Z = rot3(q, ax, ay, az)
            out.append((X + cx, Y + cy, Z + cz))
        return out
    defs = {"avant": (0, 0, -d / 2, w, h, 0, 0), "arriere": (0, 0, d / 2, w, h, 0, 180),
            "gauche": (-w / 2, 0, 0, d, h, 0, 90), "droite": (w / 2, 0, 0, d, h, 0, -90),
            "haut": (0, -h / 2, 0, w, d, -90, 0), "bas": (0, h / 2, 0, w, d, 90, 0)}
    plans = []
    for nom, f in faces.items():
        dx, dy, dz, fw, fh, fax, fay = defs[nom]
        plans.append(Plan(pose(dx, dy, dz, fw, fh, fax, fay), fw, fh, f, alpha))
    return plans


def aplat(couleur, r=0, cols=None):
    def f(c, w, h):
        if cols: c.drawRoundRect(skia.Rect.MakeWH(w, h), r, r, pgrad(0, 0, w, h, cols))
        else: rrect(c, 0, 0, w, h, r, couleur)
    return f


def sol(c, cam, t, y=520, alpha=0.5, pas=200, n=14, defile=0.0, couleur=None):
    """sol quadrillé en perspective (lignes lilas qui s'éteignent au loin)"""
    couleur = couleur or S["lilas"]
    for i in range(-n, n + 1):
        x = i * pas
        p0, p1 = cam.proj((x, y, -200)), cam.proj((x, y, 4200))
        trait(c, p0[0], p0[1], p1[0], p1[1], couleur, 2, alpha * 0.6)
    for j in range(0, 22):
        z = j * pas - (defile % pas)
        if z < -200: continue
        a = alpha * (1 - z / 4400)
        p0, p1 = cam.proj((-n * pas, y, z)), cam.proj((n * pas, y, z))
        trait(c, p0[0], p0[1], p1[0], p1[1], couleur, 2, max(0, a))


# ─────────────────────────────────────────── contenus de cartes
ICONES_PRO = ["store", "utensils", "scissors", "dumbbell", "wrench", "coffee", "flower-2", "car", "house", "shirt", "pizza", "stethoscope"]
NOMS_PRO = ["Corner Shop", "Bella Pasta", "Fresh Cuts", "Iron Gym", "Fix-It Pro", "Bean There", "Bloom Co.", "AutoCare",
            "Home & Co", "Thread Lab", "Pizza Nova", "City Clinic"]


def post_gris(k=0, gris=0.0):
    """la pub classique : photo plate, grise, texte qu'on ne lit pas"""
    def f(c, w, h):
        rrect(c, 0, 0, w, h, w * 0.06, "#F4F3F7", 1.0, None, "#D5D0DD", w * 0.006)
        disque(c, w * 0.12, h * 0.075, w * 0.055, "#CFCBD6")
        texte(c, NOMS_PRO[k % len(NOMS_PRO)], w * 0.21, h * 0.045, w * 0.055, "#7E788A", "fort", track=0)
        rrect(c, w * 0.21, h * 0.095, w * 0.25, w * 0.025, w * 0.012, "#D9D5DF")
        rrect(c, w * 0.05, h * 0.15, w * 0.9, h * 0.56, w * 0.04, "#DAD6E0")
        icone(c, ICONES_PRO[k % len(ICONES_PRO)], w / 2, h * 0.43, w * 0.2, "#B7B2C0", 1.8)
        for j, lw in enumerate([0.8, 0.62, 0.45]):
            rrect(c, w * 0.05, h * (0.76 + 0.065 * j), w * lw, w * 0.032, w * 0.016, "#D6D2DC")
        if gris > 0: rrect(c, 0, 0, w, h, w * 0.06, "#E7E5EB", gris)
    return f


def post_motion(t, l1="YOUR", l2="BUSINESS", l3="IN MOTION", bouton_="Book now"):
    """la même pub en motion design : tout vit (formes qui tournent, titre qui rebondit, bouton qui pulse)"""
    def f(c, w, h):
        c.drawRoundRect(skia.Rect.MakeWH(w, h), w * 0.06, w * 0.06, pgrad(0, 0, w, h, GRAD_VIF))
        k = w / 500
        cx, cy = w / 2, h * 0.42
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeWH(w, h), w * 0.06, w * 0.06), doAntiAlias=True)
        lueur_s(c, cx, cy, 300 * k, "#FFFFFF", 0.18)
        for j in range(3):
            r = (120 + 60 * j + 10 * math.sin(t * 3 + j)) * k
            c.save(); c.translate(cx, cy); c.rotate(t * (40 + 25 * j) * (-1) ** j)
            rrect(c, -r, -r, 2 * r, 2 * r, r * 0.45, None, 1.0, None, "#FFFFFF", 3 * k)
            c.restore()
        for j in range(6):
            a = t * 1.3 + j * 1.05
            etoile4(c, cx + 170 * k * math.cos(a), cy + 210 * k * math.sin(a), (16 + 6 * math.sin(t * 5 + j)) * k, "#FFFFFF", 0.85, t * 2)
        tl = (t + 0.4) % 2.0
        c.save(); c.translate(cx, 0); c.scale(k, k)
        lettres(c, l1, 0, cy / k - 120, 74, tl, 0.0, "ressort", grad=False, couleur="#FFFFFF", decal=0.05)
        lettres(c, l2, 0, cy / k - 44, 74, tl, 0.1, "ressort", grad=False, couleur="#FFFFFF", decal=0.04)
        lettres(c, l3, 0, cy / k + 40, 38, tl, 0.35, "masque", grad=False, couleur="#E3D6FF", decal=0.03)
        c.restore()
        c.save(); c.translate(cx, h * 0.75); c.scale(k, k)
        pill(c, bouton_, 0, 0, 28, "blanc", "sparkles", 1.0, 1 + 0.06 * math.sin(t * 7))
        c.restore()
        barre_progression(c, w * 0.08, h - 50 * k, w * 0.84, (t * 0.45) % 1, 8 * k, ["#FFFFFF", "#FFFFFF"], "#FFFFFF40", tete=False)
        c.restore()
    return f


def tel(contenu, voile=0.0, pause=False):
    """téléphone vu de face, à plaquer sur un Plan (w×h ≈ 1:2) ; contenu = fonction dessin(c, w, h) de l'écran"""
    def f(c, w, h):
        r = w * 0.15
        rrect(c, 0, 0, w, h, r, "#17131F")
        rrect(c, w * 0.012, w * 0.012, w * 0.976, h - w * 0.024, r * 0.95, None, 1.0, None, "#4A4458", w * 0.006)
        m = w * 0.035
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(m, m, w - 2 * m, h - 2 * m), r * 0.8, r * 0.8), doAntiAlias=True)
        c.translate(m, m); contenu(c, w - 2 * m, h - 2 * m)
        if voile > 0: c.drawRect(skia.Rect.MakeWH(w, h), peinture("#3A3446", voile))
        c.restore()
        rrect(c, w / 2 - w * 0.14, m + w * 0.03, w * 0.28, w * 0.075, w * 0.0375, "#0B0910")
    return f


def dos_tel(c, w, h):
    r = w * 0.15
    c.drawRoundRect(skia.Rect.MakeWH(w, h), r, r, pgrad(0, 0, w, h, ["#2A1E52", "#4B3A9A", "#2A1E52"]))
    rrect(c, w * 0.08, w * 0.08, w * 0.38, w * 0.38, w * 0.1, "#1B1430")
    for j, (x, y) in enumerate([(0.17, 0.17), (0.35, 0.17), (0.17, 0.35)]): disque(c, w * x, w * y, w * 0.06, "#0B0910")
    image(c, "dyou-icon-512", w / 2 - w * 0.17, h / 2 - w * 0.17, w * 0.34)


def carte_blanche(dessin_contenu, r=34):
    def f(c, w, h):
        rrect(c, 0, 0, w, h, r, "#FFFFFF", 1.0, None, S["ligne"], 2)
        dessin_contenu(c, w, h)
    return f


# ─────────────────────────────────────────── corps : balancement 3D léger
class Balance:
    """toute la suite du film respire en perspective (caméra qui flotte)"""
    def __init__(self, c, t, amp=1.0):
        self.c, self.t, self.amp = c, t, amp
    def __enter__(self):
        t = self.t
        self.e = Espace(self.c, 540, 900, rx=2.6 * self.amp * math.sin(t * 0.9), ry=3.4 * self.amp * math.sin(t * 0.67 + 1))
        return self.e.__enter__()
    def __exit__(self, *a):
        self.e.__exit__(*a)


# ─────────────────────────────────────────── fin : « We make your business take off »
def scene_decollage(c, t, M):
    t0, t1 = M["decolle"] - 0.15, M["devis"] - 0.1
    if t < t0 or t > t1 + 0.45: return
    entree_ = prog(t, t0, 0.5, sortieExpo)
    sortie_ = prog(t, t1, 0.4, entree)
    tk = M["take"]
    leve = prog(t, tk - 0.1, 1.2, entreeSortie)               # la caméra lève les yeux avec la fusée
    cam = Cam(ax=mix(-24, -8, entree_) + 14 * leve, ay=mix(16, -6, prog(t, t0, t1 - t0 + 0.4, douce)), tz=mix(900, -60, entree_) + 900 * sortie_, cy=860 + 300 * leve, tx=-90)
    with Calque(c, borne(entree_ * 3) * (1 - sortie_)):
        sol(c, cam, t, y=420, alpha=0.55, defile=(t - t0) * 900 * (1 + 3 * leve))
        # le panneau de croissance, debout sur le sol
        W_, H_ = 980, 660
        cz = 300
        def panneau(cc, w, h):
            rrect(cc, 0, 0, w, h, 40, "#FFFFFF", 1.0, None, S["ligne"], 3)
            tuile(cc, "trending-up", 80, 80, 80)
            texte(cc, tr("Ton activité"), 140, 54, 40, S["encre"], "titre", track=-0.02)
            pill(cc, "Live", w - 110, 80, 24, "vert")
            for j in range(4): rrect(cc, 60, 180 + j * 100, w - 120, 2, 1, S["ligne"])
            u = prog(t, t0 + 0.1, tk - t0, lambda v: entreeSortie(v))
            pth = skia.Path(); n = 60
            for j in range(n + 1):
                q = j / n * u
                x = 60 + (w - 120) * q
                y = h - 80 - (h - 200) * (q ** 2.4) - 18 * math.sin(q * 9) * (1 - q)
                (pth.moveTo if j == 0 else pth.lineTo)(x, y)
            pa = pgrad(0, 0, w, 0, GRAD_VIF); pa.setStyle(skia.Paint.kStroke_Style); pa.setStrokeWidth(12); pa.setStrokeCap(skia.Paint.kRound_Cap)
            cc.drawPath(pth, pa)
        scene3d(c, cam, [Plan(coins((0, 420 - H_ / 2, cz), W_, H_), W_, H_, panneau)])
        # la fusée : part du bout de la courbe, file vers le haut et le fond
        lv = prog(t, tk - 0.05, 1.1, entree)
        bx, by, bz = W_ / 2 - 60, 420 - H_ + 120, cz - 10
        trajet = lambda u: (bx - 380 * u, by - 1700 * u - 900 * u * u, bz - 1100 * u)
        if t > tk - 0.3:
            for j in range(34):
                u = lv - j * 0.016
                if u <= 0: continue
                X, Y, _ = cam.proj(trajet(u))
                disque(c, X, Y, (64 - j * 1.6) * FOC / (FOC + cam.vue(trajet(u))[2]), [S["violetVif"], S["bleuVif"], S["lilas"], S["or_"]][j % 4], 0.55 * (1 - j / 34))
            X, Y, Z = cam.proj(trajet(lv))
            k = FOC / (FOC + Z)
            a = entre(t, tk - 0.3, 0.4, 2.2)
            c.save(); c.translate(X, Y); c.rotate(mix(0, -40, lv)); c.scale(k * mix(0.4, 1, a) * 1.9, k * mix(0.4, 1, a) * 1.9)
            lueur_s(c, 0, 0, 120, S["violetVif"], 0.4)
            tuile(c, "rocket", 0, 0, 120)
            c.restore()
            if lv > 0.02:
                onde(c, cam.proj((bx, by, bz))[0], cam.proj((bx, by, bz))[1], t, tk, 60, 360, S["violetVif"], 8, 0.6)
                eclats(c, cam.proj((bx, by, bz))[0], cam.proj((bx, by, bz))[1], t, tk, 14, 380, graine=13)
    # titres posés devant la scène
    with Calque(c, 1 - sortie_):
        lettres(c, "WE MAKE", 540, 200, 92, t, M["decolle"] - 0.05, "ressort", decal=0.03, grad=False, couleur=S["encre"])
        b = entre(t, M["business"] - 0.1, 0.4, 2.2)
        pill(c, "Your business", 540, 360, 38, "encre", "store", borne(b * 3), mix(0.4, 1, b), rot=-3)
        lettres(c, "TAKE OFF", 540, 440, 170, t, tk - 0.08, "ressort", decal=0.04, onde_t=tk + 0.6)
        d = entre(t, M["ceci"] - 0.12, 0.4, 2.4) if "ceci" in M else 0
        if d > 0:
            pill(c, "With videos like this one", 540, 1290, 32, "grad", "play", borne(d * 3), mix(0.4, 1, d), rot=2)


def sons_corps3d(K, M):
    son, rapide = K.son, K.rapide
    son(M["b2"] - 0.1, "whoosh_long", -9)
    for i in range(12): son(M["motion"] - 0.45 + 0.045 * i, "blip", -19)
    son(M["motion"] + 0.25, "impact_doux", -10)
    son(M["captive"] - 0.1, "montee", -11); son(M["captive"] + 0.35, "impact", -8)
    for k in ("regarde", "comprend", "action"): son(M[k] - 0.12, "pop", -11)
    son(M["comprend"] + 0.1, "ding", -14); son(M["action"] + 0.34, "clic", -7); son(M["action"] + 0.4, "check", -10)
    son(M["b3"] - 0.12, "whoosh", -9); son(M["b3"] + 0.1, "montee", -14)
    for k in ("attention", "demandes", "clients"): son(M[k] - 0.1, "pop", -11)
    son(M["demandes"] - 0.05, "message_in", -10); son(M["demandes"] + 0.22, "message_in", -12); son(M["clients"] - 0.05, "ching", -11)
    son(M["b4"] - 0.1, "swipe", -10); son(M["site"] - 0.12, "pop", -11)
    son(M["expliquer"] - 0.05, "clic", -7)
    for k in range(3): son(M["expliquer"] + 0.03 + k * (M["simple"] - M["expliquer"]) / 3.2, "blip", -15)
    son(M["long_texte"] + 0.2, "croc", -12)
    son(M["simple"] - 0.08, "tampon", -9); son(M["simple"], "check", -12)
    son(M["b5"] - 0.1, "whoosh", -10)
    for i in range(10): son(M["script"] - 0.15 + 0.07 * i, "frappe", -17)
    son(M["anime"] - 0.15, "whoosh_court", -11); son(M["anime"], "pop", -12)
    son(M["accroches"] - 0.35, "whoosh_long", -10)
    for k in range(4): son(M["accroches"] - 0.1 + 0.08 * k, "swipe", -15)
    son(M["tester"] - 0.05, "montee", -14); son(M["tester"] + 0.05, "ching", -11)
    # décollage
    son(M["decolle"] - 0.2, "whoosh_bas", -8); son(M["decolle"], "impact_doux", -9)
    son(M["business"] - 0.1, "pop", -11)
    son(M["take"] - 0.45, "montee", -9); son(M["take"] - 0.05, "impact", -5); son(M["take"], "whoosh_long", -6); son(M["take"] + 0.05, "ching", -10)
    if "ceci" in M: son(M["ceci"] - 0.12, "pop", -11)
    son(M["devis"] - 0.12, "whoosh", -9); son(M["devis"] + 0.18, "verre", -10); son(M["devis"] + 0.75, "clic", -6)
    for i in range(15): son(M["url"] + i * 0.034, "frappe", -18)
    son(M["url"] + 0.4, "pop", -13)
    for a, b in [(M["b2"] - 0.15, M["b2"] + 0.3), (M["b3"] - 0.15, M["b3"] + 0.3), (M["b4"] - 0.15, M["b4"] + 0.3),
                 (M["b5"] - 0.15, M["b5"] + 0.3), (M["accroches"] - 0.35, M["accroches"] + 0.1),
                 (M["decolle"] - 0.2, M["decolle"] + 0.3), (M["take"] - 0.05, M["take"] + 0.6), (M["devis"] - 0.15, M["devis"] + 0.3)]:
        rapide(a, b)


# ─────────────────────────────────────────── corps commun (texte identique dans les 5 pubs, seul le hook change)
CORPS = ("A motion design video grabs attention. Your customer watches, gets it right away, and takes action. "
         "The result: more attention, more inquiries, more customers. On your website, it explains what you do, "
         "without a wall of text. We write the script, we animate everything, and you get three or four hooks to test. "
         "We make your business take off with videos like this. Tap the link.")
# indices des mots du corps (à décaler du nombre de mots du hook)
_REPERES = dict(b2=0, motion=1, captive=4, regarde=8, comprend=9, action=14, b3=16, attention=19, demandes=21, clients=23,
                b4=24, site=26, expliquer=28, facon=29, simple=31, long_texte=34, b5=37, script=40, anime=42, accroches=47,
                tester=52, decolle=53, business=56, take=57, ceci=62, devis=63, url=65)


def reperes(TW, n_hook):
    M = {k: TW(v + n_hook) for k, v in _REPERES.items()}
    M["titre_b3"] = "THE RESULT"; M["prix"] = None
    return M


def config_us():
    from studio_en import anglais
    anglais(prix=False)
    studio.TR["Ton offre, en mouvement."] = "Your business, in motion."


def compose(c, t, M, hook, T_B1, SOUS, K, pulse=0.0):
    fond_studio(c, t, battement(t, M["captive"] + 0.35, 1, 0.5) - 1 + pulse)
    with Balance(c, t):
        scene_b2(c, t, M); scene_b3(c, t, M); scene_b4(c, t, M); scene_b5(c, t, M)
    scene_decollage(c, t, M)
    scene_cta(c, t, M, 0)
    if t < T_B1 + 0.3:
        o = prog(t, T_B1 - 0.3, 0.35, entree)
        c.save(); c.translate(540, 900); c.scale(mix(1, 2.2, o), mix(1, 2.2, o)); c.translate(-540, -900)
        with Calque(c, 1 - o):
            hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    if t < M["devis"] - 0.25: SOUS.dessine(c, t, S["encre"])
