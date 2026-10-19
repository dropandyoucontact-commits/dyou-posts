"""DROP&YOU « on est sur place » en 3D, couleurs cobalt (DY-M10, DY-M11 — 17/10/2026).

Demande de Youssef : le sujet de DY-M02 (quelqu'un sur place en Chine : catalogue, qualités, livraison comprise
8-12 jours, à l'unité ou en quantité, paiement, Snap / WhatsApp), mais avec le rythme de voix et les couleurs de
CB-M15 (cobalt bleu nuit / orange), d'autres articles de la banque, de la 3D (les articles sortent du téléphone),
et le logo DROP&YOU présent sur toute la vidéo (oublié sur CB-M15 : « tu n'as pas marqué ma vidéo »).
Les scènes lisent un dictionnaire M de temps-repères ; seul le hook change d'une vidéo à l'autre.
"""
import math
import unicodedata
import skia
from moteur import *
from kit import logo_app
from studio import lettres, eclats, rayons, entre, SousTitresEncre, pill, pgrad
from studio3d import Cam, Plan, coins, scene3d, boite, aplat, sol, tel, rot3, FOC
from agence import lueur
from noir import puce, etiquette_case, tampon_n, coche, BLANC, ROUGE, VERT
from cobalt import *

OR_C = [ORANGE, ORANGE2]
BLEU_CASE = "#0A1650"
LOGO = "logo-dy-blanc"
TR = {}                 # version anglaise : texte français affiché → texte anglais
def tr(x): return TR.get(x, x) if x else x

PRODUITS = dict(veste="produits/textile/veste-racing-bleue", veste2="produits/textile/veste-racing-blanche",
                doudoune="produits/textile/veste-doudoune-bleue", gilet="produits/textile/gilet-maille-creme",
                casque="produits/electronique/casque-audio", moto="produits/mobilite/moto-electrique")


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(ch for ch in s if ch.isalnum() and unicodedata.category(ch) != "Mn")


def trouve(K, mot, apres=0):
    """indice du premier mot égal à `mot` (sans accents ni ponctuation) à partir de `apres`"""
    cible = _norm(mot)
    for i, m in enumerate(K.timing["mots"]):
        if i >= apres and _norm(m["w"]) == cible: return i
    raise KeyError(mot)


# ─────────────────────────────────────────── briques
def titre(c, t, l1, l2, t0, t1, y=400, t2=None):
    """deux lignes : blanche puis orange ; partent avant la scène suivante"""
    if t < t0 - 0.1 or t > t1 + 0.1: return
    a = 1 - prog(t, t1 - 0.2, 0.15, entree)
    l1, l2 = tr(l1), tr(l2)
    if l1:
        ts = ajuste(l1, 960, 92, "noir", -0.03)
        lettres(c, l1, 540, y, ts, t, t0 - 0.05, "ressort", grad=False, couleur=BLANC, decal=0.03, alpha=a)
    if l2:
        ts = ajuste(l2, 960, 104, "noir", -0.03)
        lettres(c, l2, 540, y + 108, ts, t, (t2 if t2 is not None else t0 + 0.12) - 0.05, "ressort", cols=OR_C, decal=0.03, alpha=a)


def plan_produit(nom, glow=True):
    iw, ih = taille_img(nom)
    def f(c, w, h):
        if glow:
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(w / 2, h / 2), max(w, h) * 0.62, [hexa(ORANGE, 0.32), hexa(ORANGE, 0.0)]))
            c.drawCircle(w / 2, h / 2, max(w, h) * 0.62, p)
            c.drawCircle(w / 2, h / 2, min(w, h) * 0.46, peinture("#FFFFFF", 0.10))
        image(c, nom, w * 0.08, h * 0.08, w * 0.84, 1.0, h * 0.84)
    return f, iw / ih


def ecran_cobalt(t, rangee=None):
    """écran du téléphone : catalogue DROP&YOU en grille sur bleu nuit"""
    noms = [PRODUITS[k] for k in (rangee or ["veste", "doudoune", "casque", "moto", "gilet", "veste2"])]
    def f(c, w, h):
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, h)], [hexa("#0A1D7A"), hexa(NUIT)]))
        c.drawRect(skia.Rect.MakeWH(w, h), g)
        k = w / 440
        iw, ih = taille_img(LOGO); lw = 180 * k
        image(c, LOGO, w / 2 - lw / 2, 50 * k, lw)
        cw, ch = (w - 60 * k) / 2, 230 * k
        for j, nom in enumerate(noms):
            x = 20 * k + (j % 2) * (cw + 20 * k); y = 120 * k + (j // 2) * (ch + 20 * k) - ((t * 40) % 1 if False else 0)
            rrect(c, x, y, cw, ch, 22 * k, "#FFFFFF", 0.08, None, "#FFFFFF", 1.5 * k)
            iw2, ih2 = taille_img(nom)
            s = min((cw - 30 * k) / iw2, (ch - 70 * k) / ih2)
            image(c, nom, x + cw / 2 - iw2 * s / 2, y + 12 * k, iw2 * s)
            rrect(c, x + 16 * k, y + ch - 40 * k, cw * 0.55, 12 * k, 6 * k, "#FFFFFF", 0.35)
            rrect(c, x + cw - 64 * k, y + ch - 48 * k, 48 * k, 28 * k, 14 * k, ORANGE)
    return f


def carton3d(centre, taille, ay=0.0, ax=0.0, az=0.0, alpha=1.0):
    def face(c, w, h):
        rrect(c, 0, 0, w, h, 8, "#C8955A")
        rrect(c, w * 0.42, 0, w * 0.16, h, 0, "#E2B97E")
        rrect(c, w * 0.12, h * 0.6, w * 0.3, h * 0.24, 6, "#FFFFFF", 0.9)
        trait(c, w * 0.16, h * 0.68, w * 0.36, h * 0.68, "#8A6A45", 3); trait(c, w * 0.16, h * 0.76, w * 0.3, h * 0.76, "#8A6A45", 3)
    def cote(c, w, h):
        rrect(c, 0, 0, w, h, 8, "#B48048")
    def haut(c, w, h):
        rrect(c, 0, 0, w, h, 8, "#D9A86A"); rrect(c, 0, h * 0.42, w, h * 0.16, 0, "#EAC48E")
    return boite(centre, taille, taille * 0.8, taille * 0.8, dict(avant=face, arriere=face, gauche=cote, droite=cote, haut=haut, bas=cote), ax=ax, ay=ay, az=az, alpha=alpha)


def filigrane(c, t, alpha=1.0):
    """le logo DROP&YOU, présent sur toute la vidéo, sous la zone de l'interface Snap"""
    if alpha <= 0: return
    iw, ih = taille_img(LOGO); lw = 210
    image(c, LOGO, 540 - lw / 2, 262, lw, 0.92 * alpha)


# ─────────────────────────────────────────── 1. sur place
def scene_sur_place(c, t, M):
    t0, t1 = M["dy"] - 0.15, M["cat0"] - 0.1
    if t < t0 or t > t1 + 0.4: return
    a = prog(t, t0, 0.6, lambda v: ressort(v, 1.3, 4.6))
    s = prog(t, t1, 0.35, entree)
    with Calque(c, 1 - s):
        cam = Cam(ax=-30 + 4 * math.sin(t), ay=mix(-40, 10, min(a, 1.1)) + 6 * math.sin(t * 0.7), tz=mix(1500, 200, min(a, 1.1)), cy=1000)
        sol(c, cam, t, y=260, alpha=0.4, couleur="#5F7BFF")
        iw, ih = taille_img(LOGO)
        lw = 760
        def logo_plan(cc, w, h):
            image(cc, LOGO, 0, 0, w)
        plans = [Plan(coins((0, -60, 0), lw, lw * ih / iw, ay=6 * math.sin(t * 1.3)), lw, lw * ih / iw, logo_plan)]
        scene3d(c, cam, plans)
        # l'épingle qui tombe sur « sur place »
        e = prog(t, M["place"] - 0.25, 0.5, lambda v: ressort(v, 1.6, 5.0)) if t > M["place"] - 0.25 else 0
        if e > 0:
            X, Y, Z = cam.proj((0, 260, 120))
            yy = Y - 600 * (1 - min(e, 1.0))
            c.drawOval(skia.Rect.MakeXYWH(X - 90, Y - 18, 180, 36), peinture("#000000", 0.25))
            for k in range(3):
                u = ((t - M["place"]) * 0.9 + k / 3) % 1
                c.drawOval(skia.Rect.MakeXYWH(X - 90 - 260 * u, Y - 18 - 52 * u, 180 + 520 * u, 36 + 104 * u),
                           peinture(ORANGE, 0.5 * (1 - u), Style=skia.Paint.kStroke_Style, StrokeWidth=4))
            disque(c, X, yy - 120, 70, ORANGE); disque(c, X, yy - 120, 28, BLEU_CASE)
            pth = skia.Path(); pth.moveTo(X - 60, yy - 90); pth.lineTo(X, yy); pth.lineTo(X + 60, yy - 90); pth.close(); c.drawPath(pth, peinture(ORANGE))
            puce(c, tr("Sur place, en Chine"), 540, 1290, entre(t, M["place"], 0.4, 2.2), "map-pin", ORANGE, 38)


# ─────────────────────────────────────────── 2. le catalogue sort du téléphone
POS_ORBITE = [(-360, -110, -380), (350, -70, -420), (-350, 330, -360), (330, 360, -460), (0, 560, -300)]


def scene_catalogue(c, t, M):
    t0, t1 = M["cat0"] - 0.2, M["qual0"] - 0.1
    if t < t0 or t > t1 + 0.4: return
    a = prog(t, t0, 0.55, sortieExpo)
    s = prog(t, t1, 0.4, entree)
    cam = Cam(ax=-6 + 3 * math.sin(t * 0.9), ay=mix(35, -12, a) + 8 * math.sin(t * 0.6), tz=mix(1400, 380, a) + 1200 * s, cy=1010)
    lueur(c, 540, 930, 620, ORANGE, 0.16)
    plans = [Plan(coins((0, 40, 0), 430, 880), 430, 880, tel(ecran_cobalt(t)), 1 - s)]
    for k, (cle, t_mot) in enumerate(M["items"]):
        u = prog(t, t_mot - 0.18, 0.7, lambda v: ressort(v, 1.3, 4.4)) if t > t_mot - 0.18 else 0
        if u <= 0: continue
        f, r = plan_produit(PRODUITS[cle])
        h = 360 if r < 1.2 else 270
        w = h * r
        px, py, pz = POS_ORBITE[k % len(POS_ORBITE)]
        flot = 18 * math.sin(t * 2 + k)
        cen = (mix(0, px, min(u, 1.05)), mix(40, py, min(u, 1.05)) + flot, mix(10, pz, min(u, 1.05)))
        plans.append(Plan(coins(cen, w, h, ay=mix(80, 0, min(u, 1)) + 10 * math.sin(t * 1.4 + k), az=mix(-25, 0, min(u, 1))), w, h, f, borne(u * 3) * (1 - s), recto=False))
    scene3d(c, cam, plans)
    for k, (cle, t_mot) in enumerate(M["items"]):
        if 0 < t - t_mot < 0.6:
            X, Y, _ = cam.proj((0, 40, -20))
            eclats(c, X, Y, t, t_mot, 10, 420, [ORANGE, BLANC, ORANGE2], graine=3 + k)
    l1, l2 = M.get("titre_cat", ("TOUT LE CATALOGUE", "DANS TON TÉLÉPHONE"))
    titre(c, t, l1, l2, M["catalogue"] - 0.1, t1, y=400, t2=M["tel"])


# ─────────────────────────────────────────── 3. les trois qualités (mêmes noms que CB-M15)
QUALS = [("Standard", tr("Le modèle"), "heart"), ("1:1", tr("Les détails"), "copy"), ("Qualité originale", tr("Le plus proche"), "gem")]


def scene_qualites(c, t, M):
    """trois cartes ; par défaut les qualités des sacs (CB-M15) — pour le catalogue général, M["quals"] montre des articles
    différents sans nommer de qualité (règle du 17/10 : plusieurs qualités, selon les produits)"""
    t0, t1 = M["qual0"] - 0.15, M["livr"] - 0.1
    if t < t0 or t > t1 + 0.4: return
    a = prog(t, t0, 0.55, sortieExpo)
    s = prog(t, t1, 0.35, entree)
    quals = M.get("quals") or [(n, tg, "veste") for (n, tg, ic) in QUALS]
    l1, l2 = M.get("titre_qual", ("TU CHOISIS", "TA QUALITÉ"))
    titre(c, t, l1, l2, M["qual0"] - 0.1, t1, y=400, t2=M.get("t_titre2"))
    actif = max([k for k in range(3) if t >= M["q"][k] - 0.12] or [-1])
    cam = Cam(ax=-8 + 2 * math.sin(t), ay=4 * math.sin(t * 0.7), tz=mix(1200, 160, a) + 900 * s, cy=960)
    plans = []
    for k, (nom, tag, prod) in enumerate(quals):
        f, r = plan_produit(PRODUITS[prod], glow=False)
        on = k == actif
        lev = prog(t, M["q"][k] - 0.12, 0.4, lambda v: ressort(v, 1.4, 4.6)) if t > M["q"][k] - 0.12 else 0
        lev *= 1 - (prog(t, M["q"][k + 1] - 0.12, 0.3) if k < 2 else 0) * 0.7
        def carte(cc, w, h, k=k, on=on, nom=tr(nom), f=f, r=r):
            cc.drawRoundRect(skia.Rect.MakeWH(w, h), 36, 36, pgrad(0, 0, w, h, ["#13299A", "#0A1650"]))
            rrect(cc, 0, 0, w, h, 36, None, 1.0, None, ORANGE if on else "#FFFFFF", 6 if on else 2)
            hh = min(w * 0.8 / r, h * 0.56); ww = hh * r
            cc.save(); cc.translate(w / 2 - ww / 2, h * 0.1); f(cc, ww, hh); cc.restore()
            texte(cc, nom, w / 2, h * 0.76, 46 if len(nom) < 8 else 36, ORANGE if on else BLANC, "noir", "centre", -0.02)
            for j in range(3): disque(cc, w / 2 + (j - 1) * 34, h * 0.9, 9, ORANGE if (on and j <= k) or j == 0 else "#FFFFFF", 0.9)
        x = (k - 1) * 330
        plans.append(Plan(coins((x, 40 - 80 * lev, -220 * lev), 300, 480, ay=(1 - k) * 22 * (1 - lev)), 300, 480, carte, (1 - s) * (1.0 if (on or k < actif or actif < 0) else 0.55)))
    scene3d(c, cam, plans)
    for k, (nom, tag, prod) in enumerate(quals):
        e = entre(t, M["q"][k] + 0.25, 0.35, 2.4) * (1 - s)
        if e > 0 and k == actif and tag:
            etiquette_case(c, tr(tag), 540, 1290, e, ORANGE if k < 2 else VERT, 40, "noir", BLEU_CASE if k < 2 else BLANC)


# ─────────────────────────────────────────── 4. livraison comprise
def scene_livraison(c, t, M):
    t0, t1 = M["livr"] - 0.15, M["unite"] - 0.1
    if t < t0 or t > t1 + 0.4: return
    a = prog(t, t0, 0.5, sortieExpo)
    s = prog(t, t1, 0.35, entree)
    with Calque(c, 1 - s):
        cam = Cam(ax=-22 + 3 * math.sin(t), ay=mix(-30, 10, a) + 5 * math.sin(t * 0.6), tz=mix(1200, 300, a), cy=820)
        sol(c, cam, t, y=330, alpha=0.4, couleur="#5F7BFF", defile=(t - t0) * 500)
        u = prog(t, M["livr"], t1 - M["livr"] - 0.2, douce)
        # trajet en arc de la Chine (au fond à gauche) vers chez toi (devant à droite)
        p0, p1 = (-700, 200, 2400), (300, 200, -100)
        def arc(v): return (mix(p0[0], p1[0], v), mix(p0[1], p1[1], v) - 480 * math.sin(math.pi * v), mix(p0[2], p1[2], v))
        for j in range(40):
            v = j / 40
            if v > u: break
            X, Y, Z = cam.proj(arc(v))
            disque(c, X, Y, 7 * FOC / (FOC + Z), ORANGE, 0.8)
        for (p, lab) in [(p0, tr("Chine")), (p1, tr("Chez toi"))]:
            X, Y, Z = cam.proj((p[0], 330, p[2]))
            k = FOC / (FOC + Z)
            disque(c, X, Y, 22 * k, ORANGE); puce(c, lab, X, Y + 60 * k, 1.0, "map-pin", ORANGE, 30 * max(0.6, k))
        cp = arc(u)
        scene3d(c, cam, carton3d(cp, 300, ay=40 * u + 20 * math.sin(t), ax=-10, az=12 * math.sin(t * 2)))
    titre(c, t, "LIVRAISON", "COMPRISE", M["livr"] - 0.1, t1, y=400)
    j = entre(t, M["jours"] - 0.1, 0.4, 2.4) * (1 - s)
    if j > 0:
        c.save(); c.translate(700, 720); c.rotate(6); z = mix(2.2, 1, prog(t, M["jours"] - 0.1, 0.2, entree)); c.scale(z, z)
        etiquette_case(c, tr("8 à 12 jours"), 0, 0, borne(j * 3) * (1 - s), ORANGE, 52, "noir", BLEU_CASE)
        c.restore()
    for k, (cle, lab) in enumerate([("fr", tr("France")), ("be", tr("Belgique")), ("partout", tr("Partout"))]):
        e = entre(t, M[cle] - 0.1, 0.4, 2.2) * (1 - s)
        if e > 0: puce(c, lab, 230 + k * 310, 1290, e, "map-pin" if k < 2 else "globe", ORANGE, 34)


# ─────────────────────────────────────────── 5. pour toi ou pour revendre
def scene_quantite(c, t, M):
    t0, t1 = M["unite"] - 0.15, M["paie"] - 0.1
    if t < t0 or t > t1 + 0.4: return
    a = prog(t, t0, 0.5, sortieExpo)
    s = prog(t, t1, 0.35, entree)
    with Calque(c, 1 - s):
        cam = Cam(ax=-18 + 2 * math.sin(t), ay=mix(30, -8, a) + 5 * math.sin(t * 0.6), tz=mix(1000, 250, a), cy=1000)
        f, r = plan_produit(PRODUITS["doudoune"])
        plans = [Plan(coins((-300, -40 + 15 * math.sin(t * 2), 0), 300 * r, 300, ay=12 * math.sin(t * 1.2)), 300 * r, 300, f)]
        for i in range(3):
            for j in range(3):
                for kz in range(2):
                    n = i + 3 * j + 9 * kz
                    td = M["quant"] - 0.25 + 0.04 * n
                    u = prog(t, td, 0.4, lambda v: ressort(v, 1.2, 5)) if t > td else 0
                    if u <= 0: continue
                    plans += carton3d((250 + (i - 1) * 150, mix(-900, 120 - j * 130, min(u, 1.05)), kz * 150), 140, ay=-8)
        scene3d(c, cam, plans)
        puce(c, tr("Pour toi"), 260, 1180, entre(t, M["unite"], 0.4, 2.2), "user-round", ORANGE, 36)
        puce(c, tr("Pour revendre"), 800, 1180, entre(t, M["revendre"] - 0.1, 0.4, 2.2), "package", ORANGE, 36)
    titre(c, t, "À L'UNITÉ", "OU EN QUANTITÉ", M["unite"] - 0.1, t1, y=400, t2=M["quant"])
    if "deux" in M:
        e = entre(t, M["deux"] - 0.1, 0.4, 2.4) * (1 - s)
        if e > 0: etiquette_case(c, tr("On gère les deux"), 540, 1300, e, VERT, 40, "noir", BLANC)


# ─────────────────────────────────────────── 6. le paiement
def scene_paiement(c, t, M):
    t0, t1 = M["paie"] - 0.15, M["ecris"] - 0.1
    if t < t0 or t > t1 + 0.4: return
    a = prog(t, t0, 0.5, sortieExpo)
    s = prog(t, t1, 0.35, entree)
    cam = Cam(ax=-10 + 2 * math.sin(t), ay=4 * math.sin(t * 0.7), tz=mix(900, 200, a) + 800 * s, cy=900)
    plans = []
    for k, (cle, lab, ic, cols) in enumerate([("paie", "PayPal", "wallet", ["#2B6BFF", "#1433B8"]), ("vir", tr("Virement"), "landmark", ["#13299A", "#0A1650"]),
                                              ("carte", tr("Carte"), "credit-card", [ORANGE, "#E0560A"])]):
        u = prog(t, M[cle] - 0.15, 0.55, lambda v: ressort(v, 1.3, 4.6)) if t > M[cle] - 0.15 else 0
        if u <= 0: continue
        def carte(cc, w, h, lab=lab, ic=ic, cols=cols):
            cc.drawRoundRect(skia.Rect.MakeWH(w, h), 34, 34, pgrad(0, 0, w, h, cols))
            rrect(cc, 0, 0, w, h, 34, None, 1.0, None, "#FFFFFF", 2)
            rrect(cc, 40, 60, 80, 60, 12, "#FFD58A")
            icone(cc, ic, w - 80, 90, 64, BLANC, 2.4)
            texte(cc, lab, 150, 52, 64, BLANC, "noir", track=-0.02)
            for j in range(4): rrect(cc, 40 + j * 110, h * 0.5, 80, 16, 8, "#FFFFFF", 0.4)
        plans.append(Plan(coins(((k - 1) * 50, -230 + k * 230, mix(1600, -k * 60, min(u, 1.05))), 620, 380, ax=mix(-70, 10, min(u, 1)), ay=mix(40, -14, min(u, 1)), az=(k - 1) * -6), 620, 380, carte, (1 - s)))
    scene3d(c, cam, plans)


# ─────────────────────────────────────────── 7. écris-nous : Snap, Drop and You 1, WhatsApp
def scene_contact(c, t, M, duree):
    t0 = M["ecris"] - 0.15
    t1 = M.get("cb0", duree - 1.4) - 0.1
    if t < t0 or t > t1 + 0.4: return
    a = prog(t, t0, 0.5, sortieExpo)
    s = prog(t, t1, 0.35, entree)
    with Calque(c, 1 - s):
        titre(c, t, "ÉCRIS-NOUS", None, M["ecris"] - 0.1, t1 + 0.3, y=420)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-40, 0, a) + 6 * math.sin(t * 0.8), tz=mix(1000, 120, a), cy=900)
        def tuile_app(nom):
            def f(cc, w, h): logo_app(cc, nom, w / 2, h / 2, w * 0.92, 1.0, None)
            return f
        u1 = prog(t, M["snap"] - 0.15, 0.5, lambda v: ressort(v, 1.4, 4.6)) if t > M["snap"] - 0.15 else 0
        u2 = prog(t, M["wa"] - 0.15, 0.5, lambda v: ressort(v, 1.4, 4.6)) if t > M["wa"] - 0.15 else 0
        plans = []
        if u1 > 0: plans.append(Plan(coins((-220, -60, mix(900, 0, min(u1, 1.05))), 300, 300, ay=mix(-90, 14, min(u1, 1)) + 6 * math.sin(t * 1.5)), 300, 300, tuile_app("snapchat"), borne(u1 * 3)))
        if u2 > 0: plans.append(Plan(coins((220, -60, mix(900, 0, min(u2, 1.05))), 300, 300, ay=mix(90, -14, min(u2, 1)) + 6 * math.sin(t * 1.5 + 1)), 300, 300, tuile_app("whatsapp"), borne(u2 * 3)))
        scene3d(c, cam, plans)
        if u1 > 0:
            X, Y, _ = cam.proj((-220, 190, 0))
            ub = entre(t, M["dy1"] - 0.2, 0.4, 1.8)
            if ub > 0:
                with Calque(c, borne(ub * 3)):
                    wb = 460; x0 = X - 120
                    rrect(c, x0 - 40, 1130, wb, 92, 46, "#FFFC00")
                    icone(c, "search", x0 + 10, 1176, 34, "#111111", 2.6)
                    q = "dropandyou1"
                    n = int(borne((t - M["dy1"]) / 0.55) * len(q) + 0.999) if t > M["dy1"] else 0
                    texte(c, q[:n], x0 + 46, 1176 - hauteurLigne(40, "titre") / 2, 40, "#111111", "titre", track=-0.01)
            eclats(c, X, Y - 250, t, M["snap"] + 0.1, 12, 360, [ORANGE, BLANC, "#FFFC00"], graine=4)
        if u2 > 0:
            X, Y, _ = cam.proj((220, -60, 0))
            eclats(c, X, Y, t, M["wa"] + 0.1, 12, 360, [ORANGE, BLANC, VERT], graine=5)


# ─────────────────────────────────────────── fin : logo DROP&YOU
def scene_fin(c, t, M, duree):
    t0 = duree - 1.45
    if t < t0 - 0.1: return
    ul = entre(t, t0, 0.55, 1.5)
    lueur(c, 540, 900, 620 * borne(ul), ORANGE, 0.28)
    rayons(c, 540, 900, t, 900, 0.09 * borne(ul), 14, ORANGE2)
    cam = Cam(ax=-6, ay=mix(-70, 0, min(ul, 1.05)) + 4 * math.sin(t * 2), tz=mix(800, 0, min(ul, 1.05)), cy=900)
    iw, ih = taille_img(LOGO); lw = 760
    scene3d(c, cam, [Plan(coins((0, 0, 0), lw, lw * ih / iw), lw, lw * ih / iw, lambda cc, w, h: image(cc, LOGO, 0, 0, w), borne(ul * 3))])
    eclats(c, 540, 900, t, t0 + 0.15, 16, 560, [ORANGE, BLANC, ORANGE2], graine=9)


def sons_corps(K, M, duree):
    son, rapide = K.son, K.rapide
    son(M["dy"] - 0.15, "whoosh_long", -8); son(M["dy"] + 0.2, "impact_doux", -7); son(M["place"] - 0.25, "whoosh_court", -10); son(M["place"] + 0.1, "impact", -6)
    son(M["cat0"] - 0.2, "whoosh", -8)
    for k, (cle, tm) in enumerate(M["items"]): son(tm - 0.18, "whoosh_court", -11); son(tm, "pop", -8)
    son(M["catalogue"] - 0.1, "ching", -10)
    son(M["qual0"] - 0.15, "whoosh_long", -8)
    for k in range(3): son(M["q"][k] - 0.12, "pop", -8); son(M["q"][k] + 0.25, "ching" if k == 2 else "check", -10)
    son(M["livr"] - 0.15, "whoosh", -8); son(M["livr"], "montee", -12); son(M["jours"] - 0.1, "tampon", -7)
    for cle in ("fr", "be", "partout"): son(M[cle] - 0.1, "pop", -10)
    son(M["unite"] - 0.15, "whoosh", -8); son(M["unite"], "pop", -9)
    for n in range(18): son(M["quant"] - 0.25 + 0.04 * n + 0.15, "clic", -16)
    if "deux" in M: son(M["deux"] - 0.1, "check", -8)
    for cle in ("paie", "vir", "carte"): son(M[cle] - 0.15, "whoosh_court", -10); son(M[cle] + 0.1, "impact_doux", -10)
    son(M["ecris"] - 0.15, "whoosh_long", -8); son(M["snap"] - 0.1, "pop", -7); son(M["wa"] - 0.1, "pop", -7)
    for i in range(11): son(M["dy1"] + i * 0.05, "frappe", -16)
    son(duree - 1.45, "montee", -10); son(duree - 1.3, "impact", -4); son(duree - 1.28, "ching", -8)
    for a, b in [(M["dy"] - 0.15, M["dy"] + 0.3), (M["cat0"] - 0.2, M["cat0"] + 0.3), (M["qual0"] - 0.15, M["qual0"] + 0.3), (M["livr"] - 0.15, M["livr"] + 0.3),
                 (M["unite"] - 0.15, M["unite"] + 0.3), (M["paie"] - 0.15, M["paie"] + 0.3), (M["ecris"] - 0.15, M["ecris"] + 0.3), (duree - 1.5, duree - 1.1)]:
        rapide(a, b)


def compose(c, t, M, hook, T_B1, SOUS, K, duree, extra=None, pulse=0.0):
    fond_cobalt(c, t, pulse)
    scene_sur_place(c, t, M); scene_catalogue(c, t, M); scene_qualites(c, t, M); scene_livraison(c, t, M)
    scene_quantite(c, t, M); scene_paiement(c, t, M); scene_contact(c, t, M, duree)
    if extra: extra(c, t)
    scene_fin(c, t, M, duree)
    if t < T_B1 + 0.3:
        o = prog(t, T_B1 - 0.3, 0.35, entree)
        c.save(); c.translate(540, 900); c.scale(mix(1, 2.2, o), mix(1, 2.2, o)); c.translate(-540, -900)
        with Calque(c, 1 - o):
            hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    filigrane(c, t, 1 - prog(t, duree - 1.6, 0.3))
    if t < duree - 1.5: SOUS.dessine(c, t, BLANC)
