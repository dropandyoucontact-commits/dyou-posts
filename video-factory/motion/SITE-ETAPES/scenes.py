"""SITE-ETAPES (21/10/2026) — les 4 boucles muettes de la section « 4 étapes. C'est tout. » de dyou-agency.com/motion-design/.

Demande de Youssef : la section devait avoir des vidéos ; une par étape, sans son, qui montre ce qui est écrit.
Style du site clair (studio : papier lavande, encre #211B33, dégradé violet → bleu, verre clair de verre_studio).
Boucles de 6 s : tout part du fond vide et y revient (raccord invisible). Une seule scène par rendu :

    ETAPE=1 LANGUE=fr python3 ../moteur/rendu.py video        (ETAPE 1-4, LANGUE fr|en)

1 Vous commandez        : la carte bancaire se pose, « Payer 290 € » cliqué, commande confirmée.
2 Vous nous parlez de vous : le questionnaire se remplit, le logo tombe dans sa case, « Envoyer ».
3 Sous 48 h             : l'aperçu filigrané tourne, une demande de retouche, « Corrigé », retouches illimitées.
4 Vous validez          : « Valider », le filigrane part, 16:9 + 9:16 en HD, 4 débuts, version finale.
"""
import math, os, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
import verre_studio as vs
vs.appliquer()

ETAPE = int(os.environ.get("ETAPE", "1"))
FR = os.environ.get("LANGUE", "fr") == "fr"
def tx(a, b): return a if FR else b

DUREE = 6.0 if ETAPE <= 4 else 4.0      # 5-8 : les 4 accroches de la démo « Le même message, 3 ou 4 façons d'accrocher »
K = Kit(P, DUREE)
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
ENCRE, GRIS, VIOLET = S["encre"], S["gris"], S["violetVif"]
PRIX = tx("290 €", "$299")


def enveloppe(t):
    """tout disparaît sur la fin : la boucle repart du fond vide"""
    if ETAPE > 4: return 1 - prog(t, DUREE - 0.3, 0.28, entree)      # accroches : courte sortie, la suivante s'enchaîne
    return 1 - prog(t, DUREE - 0.5, 0.42, entree)


def ecrit(s, t, t0, d):
    if t <= t0: return ""
    return s[:int(borne((t - t0) / d) * len(s) + 0.999)]


def caret(c, x, y, h, t):
    if int(t * 3) % 2 == 0: rrect(c, x + 4, y, 4, h, 2, VIOLET)


# ─────────────────────────────────────────── briques communes
def carte_bancaire(c, cx, cy, w, rot=0.0, alpha=1.0):
    h = w * 0.63
    c.save(); c.translate(cx, cy); c.rotate(rot)
    with Calque(c, alpha):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.06, w * 0.06)
        p = skia.Paint(AntiAlias=True, Color=hexa("#3B1E8C", 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, w * 0.05))
        c.save(); c.translate(0, w * 0.05); c.drawRRect(rr, p); c.restore()
        c.drawRRect(rr, pgrad(-w / 2, -h / 2, w / 2, h / 2, GRAD_VIF))
        c.save(); c.clipRRect(rr, doAntiAlias=True)
        disque(c, w * 0.42, -h * 0.55, w * 0.42, "#FFFFFF", 0.10); disque(c, -w * 0.5, h * 0.6, w * 0.35, "#FFFFFF", 0.07)
        c.restore()
        rrect(c, -w * 0.38, -h * 0.16, w * 0.14, w * 0.105, w * 0.018, "#FFD86B")
        trait(c, -w * 0.38, -h * 0.16 + w * 0.052, -w * 0.24, -h * 0.16 + w * 0.052, "#C9A23E", 2)
        icone(c, "signal", w * 0.36, -h * 0.3, w * 0.09, "#FFFFFF", 2.4)
        texte(c, "••••  ••••  ••••  4242", -w * 0.38, h * 0.08, w * 0.062, "#FFFFFF", "titre", track=0.02)
        texte(c, tx("VOTRE ENTREPRISE", "YOUR BUSINESS"), -w * 0.38, h * 0.3, w * 0.036, "#FFFFFF", "fort", track=0.06, alpha=0.85)
    c.restore()


def pub(c, x, y, w, h, t, logo_s=1.0):
    """la vidéo du client, en miniature : fond lavande vivant, logo, titre qui se construit"""
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), min(w, h) * 0.04, min(w, h) * 0.04)
    c.save(); c.clipRRect(rr, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pgrad(x, y, x + w, y + h, ["#F6F1FF", "#E3D7FF", "#D9E3FF"]))
    for k, (fx, fy, r, col) in enumerate([(0.2, 0.3, 0.45, "#B79BFF"), (0.85, 0.75, 0.5, "#8FB1FF"), (0.6, 0.1, 0.3, "#D9C8FF")]):
        cx_ = x + w * (fx + 0.06 * math.sin(t * 1.3 + k * 2)); cy_ = y + h * (fy + 0.06 * math.cos(t * 1.1 + k))
        lueur_s(c, cx_, cy_, max(w, h) * r, col, 0.5)
    m = min(w, h)
    lx, ly = x + w * 0.5, y + h * (0.3 if h > w else 0.33)
    s = m * 0.13 * logo_s
    disque(c, lx, ly, s, "#FFFFFF", 1.0, (0, s * 0.3, 0.25))
    icone(c, "sparkles", lx, ly, s * 1.05, VIOLET, 2.6)
    l1 = tx("VOTRE MARQUE", "YOUR BRAND")
    tl = ajuste(l1, w * 0.82, m * (0.16 if h > w else 0.13), "noir", -0.03)
    lettres(c, l1, x + w / 2, y + h * (0.52 if h > w else 0.55), tl, (t % 3.0) + 10, 10.05, "masque", decal=0.03, duree=0.35)
    pill(c, tx("Découvrir", "Discover"), x + w / 2, y + h * (0.74 if h > w else 0.8), m * 0.045, "grad", "arrow-right")
    c.restore()
    c.drawRRect(rr, peinture(S["ligne"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=3))


def filigrane_apercu(c, x, y, w, h, alpha):
    if alpha <= 0.01: return
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    c.translate(x + w / 2, y + h / 2); c.rotate(-18)
    mot = tx("APERÇU", "PREVIEW"); tm = min(w, h) * 0.09
    lw = largeur(mot, tm, "noir") + tm * 1.6
    for j in range(-4, 5):
        for i in range(-4, 5):
            texte(c, mot, i * lw + (j % 2) * lw / 2, j * tm * 2.4, tm, "#FFFFFF", "noir", "centre", 0.02, 0.55 * alpha)
    c.restore()


def lecteur(c, x, y, w, h, t, fili, logo_s=1.0, barre=True):
    """la vidéo dans une carte de verre, avec sa barre de lecture"""
    m = 26
    vs.verre(c, x - m, y - m, w + 2 * m, h + 2 * m + (70 if barre else 0), 44)
    pub(c, x, y, w, h, t, logo_s)
    filigrane_apercu(c, x, y, w, h, fili)
    if barre:
        by = y + h + 44
        u = (t / 6.0) % 1.0
        icone(c, "play", x + 22, by, 34, ENCRE, 2.6)
        rrect(c, x + 60, by - 5, w - 60, 10, 5, S["lavande"])
        rrect(c, x + 60, by - 5, (w - 60) * u, 10, 5, VIOLET)
        disque(c, x + 60 + (w - 60) * u, by, 13, "#FFFFFF", 1.0, (0, 3, 0.25)); anneau(c, x + 60 + (w - 60) * u, by, 13, VIOLET, 3)


def champ(c, x, y, w, lab, val, t, t0, d, actif):
    texte(c, lab, x, y, 30, GRIS, "demi", track=0)
    rrect(c, x, y + 46, w, 84, 20, S["doux"], 1.0, None, VIOLET if actif else S["ligne"], 3 if actif else 2)
    s = ecrit(val, t, t0, d)
    lw = texte(c, s, x + 28, y + 46 + 42 - hauteurLigne(40, "fort") / 2, 40, ENCRE, "fort", track=-0.01)
    if actif: caret(c, x + 28 + lw, y + 46 + 22, 40, t)
    if s == val and t > t0 + d + 0.05:
        icone(c, "check", x + w - 44, y + 46 + 42, 36, S["vert"], 3, borne((t - t0 - d) * 6))


# ─────────────────────────────────────────── 1. vous commandez
def etape1(c, t):
    a = entre(t, 0.05, 0.6)
    X, Y, W_, H_ = 900, 150, 800, 780
    pose = prog(t, 1.25, 0.5, entreeSortie)            # la carte glisse dans le champ
    tap = 2.75
    ok = prog(t, tap + 0.35, 0.5, sortieExpo)
    with Calque(c, borne(a * 3)):
        c.save(); c.translate(0, 70 * (1 - a))
        vs.verre(c, X, Y, W_, H_, 48)
        icone(c, "lock", X + 70, Y + 76, 40, S["vert"], 2.6)
        texte(c, tx("Paiement sécurisé", "Secure checkout"), X + 110, Y + 76 - hauteurLigne(32, "fort") / 2, 32, S["vert"], "fort", track=0)
        texte(c, tx("Vidéo motion design", "Motion design video"), X + 60, Y + 150, 44, ENCRE, "titre", track=-0.02)
        texte(c, tx("30-45 s · 3 ou 4 débuts", "30-45 s · 3 or 4 openings"), X + 60, Y + 212, 32, GRIS, "demi", track=0)
        texte(c, PRIX, X + 60, Y + 270, 120, ENCRE, "noir", track=-0.04)
        texte(c, tx("Une seule fois · sans abonnement", "One time · no subscription"), X + 60, Y + 410, 30, GRIS, "demi", track=0)
        # champ carte
        fy = Y + 480
        rrect(c, X + 60, fy, W_ - 120, 96, 22, S["doux"], 1.0, None, VIOLET if 1.2 < t < 2.4 else S["ligne"], 3 if 1.2 < t < 2.4 else 2)
        icone(c, "credit-card", X + 110, fy + 48, 44, VIOLET, 2.4)
        num = ecrit("4242  4242  4242  4242", t, 1.65, 0.5)
        texte(c, num, X + 160, fy + 48 - hauteurLigne(38, "fort") / 2, 38, ENCRE, "fort", track=0.02)
        # bouton
        ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
        if ok < 0.5:
            bouton(c, tx(f"Payer {PRIX}", f"Pay {PRIX}"), X + W_ / 2, Y + 680, 38, (1 - 0.06 * ap) * (1 - ok), 1 - 2 * ok, "lock")
        c.restore()
    # la carte bancaire : arrive de la gauche, flotte, puis plonge dans le champ
    ca = entre(t, 0.25, 0.7, 1.4)
    if ca > 0 and pose < 1:
        cx = mix(-300, 470, min(ca, 1.05)); cy = 540 + 14 * math.sin(t * 2.4)
        cx, cy = mix(cx, X + 300, pose), mix(cy, Y + 528, pose)
        carte_bancaire(c, cx, cy, mix(620, 230, pose), mix(-14, -4, min(ca, 1)) * (1 - pose) + 3 * math.sin(t * 1.7) * (1 - pose), borne(ca * 3) * (1 - entree(pose)))
    # curseur → clic
    cu = prog(t, tap - 0.6, 0.55, sortie)
    if cu > 0:
        curseur(c, mix(1820, X + W_ / 2 + 40, cu), mix(1060, Y + 690, cu), 1.4, 1 - prog(t, tap + 0.4, 0.3), ap)
        clic(c, X + W_ / 2 + 30, Y + 680, t, tap)
    # commande confirmée
    if ok > 0:
        c.save(); c.translate(X + W_ / 2, Y + 680); s_ = mix(0.5, 1, entre(t, tap + 0.35, 0.5, 2.0)); c.scale(s_, s_)
        pill(c, tx("Commande confirmée", "Order confirmed"), 0, 0, 40, "vert", "circle-check", borne(ok * 3))
        c.restore()
        eclats(c, X + W_ / 2, Y + 680, t, tap + 0.4, 14, 380, cols=[VIOLET, S["lilas"], S["vert"], "#FFC53D"], graine=3)


# ─────────────────────────────────────────── 2. vous nous parlez de vous
def etape2(c, t):
    a = entre(t, 0.05, 0.6)
    X, Y, W_, H_ = 380, 70, 1160, 940
    tap = 4.15
    with Calque(c, borne(a * 3)):
        c.save(); c.translate(0, 70 * (1 - a))
        vs.verre(c, X, Y, W_, H_, 48)
        tuile(c, "file-text", X + 100, Y + 92, 76, "grad")
        texte(c, tx("Parlez-nous de vous", "Tell us about you"), X + 160, Y + 52, 44, ENCRE, "titre", track=-0.02)
        texte(c, tx("Questionnaire · 5 minutes", "Form · 5 minutes"), X + 160, Y + 106, 30, GRIS, "demi", track=0)
        pill(c, "5 min", X + W_ - 130, Y + 92, 30, "doux", "timer")
        champs = [(tx("Votre activité", "Your business"), tx("Salon de coiffure à Lyon", "Hair salon in Austin"), 0.55, 0.65),
                  (tx("Vos clients", "Your customers"), tx("Jeunes actifs du quartier", "Young local professionals"), 1.35, 0.6),
                  (tx("À mettre en avant", "What to highlight"), tx("La coupe sans rendez-vous", "Walk-in haircuts"), 2.1, 0.6)]
        for k, (lab, val, t0, d) in enumerate(champs):
            u = entre(t, 0.2 + 0.1 * k, 0.5)
            with Calque(c, borne(u * 3)):
                champ(c, X + 60, Y + 180 + 160 * k + 30 * (1 - u), W_ - 120, lab, val, t, t0, d, t0 - 0.1 < t < t0 + d + 0.15)
        # le logo
        ly = Y + 680
        texte(c, tx("Votre logo", "Your logo"), X + 60, ly, 30, GRIS, "demi", track=0)
        bx, by_, bw = X + 60, ly + 46, 170
        posé = prog(t, 2.95, 0.45, lambda v: ressort(v, 1.3, 5))
        if posé <= 0:
            rrect(c, bx, by_, bw, bw, 24, S["doux"], 1.0, None, S["lilas"], 3)
            icone(c, "image", bx + bw / 2, by_ + bw / 2, 56, S["lilas"], 2.2)
        else:
            rrect(c, bx, by_, bw, bw, 24, "#FFFFFF", 1.0, None, VIOLET, 3)
        texte(c, tx("logo.png", "logo.png"), bx + bw + 40, by_ + 44, 36, ENCRE if posé > 0.5 else S["grisClair"], "fort", track=0)
        texte(c, tx("Glissez votre fichier", "Drop your file"), bx + bw + 40, by_ + 96, 28, GRIS, "demi", track=0)
        ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
        envoye = prog(t, tap + 0.3, 0.45, sortieExpo)
        if envoye < 0.5:
            bouton(c, tx("Envoyer", "Send"), X + W_ - 230, ly + 130, 38, 1 - 0.06 * ap, 1 - 2 * envoye, "send")
        else:
            c.save(); c.translate(X + W_ - 300, ly + 130); s_ = mix(0.5, 1, entre(t, tap + 0.3, 0.5, 2.0)); c.scale(s_, s_)
            pill(c, tx("C'est tout !", "That's all!"), 0, 0, 40, "vert", "circle-check", borne(envoye * 3))
            c.restore()
        c.restore()
    # le logo qui tombe dans sa case
    chute = prog(t, 2.55, 0.5, entree)
    posé = prog(t, 2.95, 0.45, lambda v: ressort(v, 1.3, 5))
    if t > 2.4:
        bx, by_, bw = X + 60, Y + 726, 170
        cx = mix(bx + bw / 2 + 260, bx + bw / 2, chute); cy = mix(by_ - 380, by_ + bw / 2, chute)
        r = mix(72, 58, chute) * (1 + 0.12 * (posé - min(posé, 1)) * 4)
        disque(c, cx, cy, r, "#FFFFFF", 1.0, (0, 10, 0.25)); anneau(c, cx, cy, r, VIOLET, 4)
        icone(c, "sparkles", cx, cy, r * 1.0, VIOLET, 2.6)
        if t > 2.95: onde(c, bx + bw / 2, by_ + bw / 2, t, 2.97, 60, 200, VIOLET, 5, 0.5)
    cu = prog(t, tap - 0.6, 0.55, sortie)
    if cu > 0:
        curseur(c, mix(1880, X + W_ - 200, cu), mix(1060, Y + 680 + 140, cu), 1.4, 1 - prog(t, tap + 0.4, 0.3),
                prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie)))
        clic(c, X + W_ - 210, Y + 680 + 130, t, tap)
    if t > tap + 0.3: eclats(c, X + W_ - 300, Y + 810, t, tap + 0.35, 14, 360, cols=[VIOLET, S["lilas"], S["vert"], "#FFC53D"], graine=5)


# ─────────────────────────────────────────── 3. sous 48 h, l'aperçu ; retouches
def etape3(c, t):
    a = entre(t, 0.05, 0.6)
    X, Y, W_, H_ = 300, 150, 1040, 585
    corr = prog(t, 3.0, 0.5, lambda v: ressort(v, 1.3, 5))
    with Calque(c, borne(a * 3)):
        c.save(); c.translate(0, 70 * (1 - a))
        lecteur(c, X, Y, W_, H_, t, 1.0, mix(1.0, 1.45, corr))
        c.restore()
    # 48 h
    h = entre(t, 0.35, 0.5, 2.0)
    if h > 0:
        c.save(); c.translate(X + 40, Y - 20); c.rotate(-4); c.scale(mix(0.4, 1, h), mix(0.4, 1, h))
        pill(c, tx("Livrée en 48 h", "Delivered in 48 h"), 140, 0, 38, "grad", "clock", borne(h * 3))
        c.restore()
    # la demande de retouche
    d = entre(t, 1.5, 0.5, 1.6)
    if d > 0:
        bx, by = 1180, 560
        c.save(); c.translate(0, 40 * (1 - min(d, 1)))
        with Calque(c, borne(d * 3)):
            vs.verre(c, bx, by, 600, 190, 40)
            disque(c, bx + 70, by + 70, 36, S["lavande"]); icone(c, "user-round", bx + 70, by + 70, 40, VIOLET, 2.2)
            texte(c, tx("Vous", "You"), bx + 125, by + 34, 28, GRIS, "demi", track=0)
            s = tx("Le logo un peu plus grand ?", "Make the logo a bit bigger?")
            lw = texte(c, ecrit(s, t, 1.75, 0.7), bx + 125, by + 72, ajuste(s, 440, 36, "titre", -0.01), ENCRE, "titre", track=-0.01)
            if t < 2.6: caret(c, bx + 125 + lw, by + 78, 36, t)
            ok = prog(t, 3.0, 0.35, sortieExpo)
            if ok > 0:
                pill(c, tx("Corrigé", "Fixed"), bx + 210, by + 152, 28, "vert", "check", borne(ok * 3))
        c.restore()
    if t > 3.0: onde(c, X + W_ / 2, Y + H_ * 0.33, t, 3.02, 80, 300, VIOLET, 6, 0.55)
    r = entre(t, 3.7, 0.5, 2.0)
    if r > 0:
        c.save(); c.translate(X + W_ / 2 + 60, 945); c.rotate(-2); c.scale(mix(0.4, 1, r), mix(0.4, 1, r))
        pill(c, tx("Retouches illimitées", "Unlimited revisions"), 0, 0, 40, "doux", "refresh-cw", borne(r * 3))
        c.restore()
        eclats(c, X + W_ / 2 + 60, 945, t, 3.75, 12, 320, cols=[VIOLET, S["lilas"], "#FFC53D"], graine=7)


# ─────────────────────────────────────────── 4. vous validez, elle est à vous
def etape4(c, t):
    a = entre(t, 0.05, 0.6)
    tap = 1.25
    lib = prog(t, tap + 0.15, 0.4, sortie)              # le filigrane s'en va
    sep = prog(t, 2.0, 0.7, entreeSortie)               # deux formats
    ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
    # 16:9 : grand au centre, puis à gauche
    W1 = mix(1000, 860, sep); H1 = W1 * 9 / 16
    X1 = mix(460, 230, sep); Y1 = mix(150, 250, sep)
    with Calque(c, borne(a * 3)):
        c.save(); c.translate(0, 70 * (1 - a))
        lecteur(c, X1, Y1, W1, H1, t, 1 - lib, 1.0, barre=False)
        if sep > 0.3:
            pill(c, "16:9 · HD", X1 + 150, Y1 + H1 + 70, 30, "blanc", "laptop", borne((sep - 0.3) * 3))
        c.restore()
    if lib < 1:
        bouton(c, tx("Valider la vidéo", "Approve the video"), 960, 900, 40, 1 - 0.06 * ap, borne(a * 3) * (1 - lib), "check")
        cu = prog(t, tap - 0.6, 0.55, sortie)
        if cu > 0:
            curseur(c, mix(1840, 1010, cu), mix(1070, 915, cu), 1.4, 1 - prog(t, tap + 0.4, 0.3), ap)
            clic(c, 1000, 905, t, tap)
    if t > tap + 0.15:
        fl = 1 - (t - tap - 0.15) / 0.3
        if 0 < fl <= 1: c.drawRect(skia.Rect.MakeWH(1920, 1080), peinture("#FFFFFF", 0.5 * fl))
    # 9:16 qui sort à droite
    if sep > 0:
        W2 = 300; H2 = W2 * 16 / 9
        X2 = mix(1300, 1330, sep); Y2 = 200
        with Calque(c, borne(sep * 2)):
            c.save(); c.translate(80 * (1 - sep), 0)
            vs.verre(c, X2 - 22, Y2 - 22, W2 + 44, H2 + 44, 40)
            pub(c, X2, Y2, W2, H2, t)
            c.restore()
            pill(c, "9:16 · HD", X2 + W2 / 2, Y2 + H2 + 70, 30, "blanc", "smartphone")
    # 3 ou 4 débuts
    for k in range(4):
        u = entre(t, 3.0 + 0.12 * k, 0.45, 2.0)
        if u > 0:
            c.save(); c.translate(400 + 330 * k, 990); c.rotate(-3 + 2 * k); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
            pill(c, tx(f"Début {k + 1}", f"Opening {k + 1}"), 0, 0, 30, "doux", "play", borne(u * 3))
            c.restore()
    f = entre(t, 3.9, 0.5, 2.0)
    if f > 0:
        c.save(); c.translate(960, 105); c.rotate(-2); c.scale(mix(0.4, 1, f), mix(0.4, 1, f))
        pill(c, tx("Version finale · sans filigrane", "Final version · no watermark"), 0, 0, 38, "grad", "download", borne(f * 3))
        c.restore()
        eclats(c, 960, 105, t, 3.95, 16, 420, cols=[VIOLET, S["lilas"], S["vert"], "#FFC53D"], graine=9)


# ─────────────────────────────────────────── 5-8. les accroches (00:00 — 00:03), la démo les enchaîne
def titre_accroche(c, t, l1, l2, y=150, t0=0.1):
    """accroche en deux lignes : la 1re en encre, la 2e au dégradé"""
    lettres(c, l1, 960, y, ajuste(l1, 1700, 104, "noir", -0.035), t, t0, "masque", grad=False, couleur=ENCRE, decal=0.022, duree=0.32)
    lettres(c, l2, 960, y + 122, ajuste(l2, 1700, 104, "noir", -0.035), t, t0 + 0.3, "ressort", decal=0.025, duree=0.4)


def accroche_probleme(c, t):
    titre_accroche(c, t, tx("Vos clients ne comprennent", "Do customers struggle"), tx("pas votre offre ?", "to understand your offer?"))
    # une page d'offre illisible : des blocs gris serrés qui s'empilent, le client perdu
    a = entre(t, 0.35, 0.55)
    X, Y, W_, H_ = 560, 470, 800, 520
    with Calque(c, borne(a * 3)):
        c.save(); c.translate(0, 60 * (1 - a))
        vs.verre(c, X, Y, W_, H_, 40)
        for k in range(9):
            u = prog(t, 0.5 + 0.08 * k, 0.3, sortie)
            if u <= 0: continue
            w = (W_ - 120) * (0.55 + 0.45 * ((k * 37) % 10) / 10)
            rrect(c, X + 60, Y + 60 + 46 * k, w * u, 22, 11, S["grisClair"], 0.55)
        c.restore()
    # trois points d'interrogation qui sautent
    for k, (x, y, r) in enumerate([(470, 560, -14), (1460, 640, 12), (1400, 930, -8)]):
        u = entre(t, 1.2 + 0.18 * k, 0.45, 2.2)
        if u <= 0: continue
        c.save(); c.translate(x, y + 8 * math.sin(t * 4 + k)); c.rotate(r); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
        disque(c, 0, 0, 70, "#FFFFFF", borne(u * 3), (0, 14, 0.2)); anneau(c, 0, 0, 70, S["rouge"], 5, borne(u * 3))
        texte(c, "?", 0, -hauteurLigne(84, "noir") / 2, 84, S["rouge"], "noir", "centre", alpha=borne(u * 3))
        c.restore()
    # le client qui décroche : curseur qui part
    cu = prog(t, 2.2, 0.8, entree)
    if 0 < cu < 1: curseur(c, mix(960, 1900, cu), mix(760, 1100, cu), 1.6, 1 - cu)
    if t > 1.2: secousse(t, 1.2)


def accroche_benefice(c, t):
    titre_accroche(c, t, tx("Votre offre,", "Your offer,"), tx("comprise en quelques secondes.", "understood in seconds."))
    # un chrono qui fait 3 s pendant que trois cartes nettes se posent : quoi, pour qui, combien
    a = entre(t, 0.35, 0.55)
    cx, cy = 560, 720
    with Calque(c, borne(a * 3)):
        vs.verre(c, cx - 170, cy - 170, 340, 340, 170)
        u = borne((t - 0.5) / 2.4)
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=18, StrokeCap=skia.Paint.kRound_Cap)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(cx - 130, cy), skia.Point(cx + 130, cy)], [hexa(x) for x in GRAD_VIF]))
        pth = skia.Path(); pth.addArc(skia.Rect.MakeXYWH(cx - 130, cy - 130, 260, 260), -90, 360 * u); c.drawPath(pth, p)
        n = min(3, int(u * 3) + (1 if u > 0 else 0)) if u < 1 else 3
        texte(c, f"{n} s", cx, cy - hauteurLigne(88, "noir") / 2, 88, ENCRE, "noir", "centre")
    cartes = [("target", tx("Ce que vous faites", "What you do")), ("users-round", tx("Pour qui", "Who it's for")), ("sparkles", tx("Pourquoi vous", "Why you"))]
    for k, (ic, lab) in enumerate(cartes):
        u = entre(t, 0.8 + 0.6 * k, 0.5, 1.8)
        if u <= 0: continue
        x, y = 860, 520 + 150 * k
        c.save(); c.translate(80 * (1 - min(u, 1)), 0)
        with Calque(c, borne(u * 3)):
            vs.verre(c, x, y, 620, 120, 30)
            tuile(c, ic, x + 70, y + 60, 72, "grad")
            texte(c, lab, x + 130, y + 60 - hauteurLigne(44, "titre") / 2, 44, ENCRE, "titre", track=-0.02)
            icone(c, "check", x + 570, y + 60, 44, S["vert"], 3.2, borne((t - 1.1 - 0.6 * k) * 4))
        c.restore()


def accroche_curiosite(c, t):
    titre_accroche(c, t, tx("Et si votre meilleur commercial", "What if your best salesperson"), tx("était une vidéo ?", "was a video?"))
    # un lecteur vidéo au centre, avec la mallette du commercial, qui travaille tout seul : les demandes arrivent
    a = entre(t, 0.4, 0.6, 1.8)
    X, Y, W_, H_ = 640, 470, 640, 400
    with Calque(c, borne(a * 3)):
        c.save(); c.translate(960, Y + H_ / 2); s_ = mix(0.5, 1, a); c.scale(s_, s_); c.translate(-960, -(Y + H_ / 2))
        vs.verre(c, X, Y, W_, H_, 40)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(X + 24, Y + 24, W_ - 48, H_ - 48), 28, 28), pgrad(X, Y, X + W_, Y + H_, ["#F1EAFF", "#DCE6FF"]))
        tuile(c, "briefcase", 960, Y + H_ / 2 - 20, 130, "grad", rot=-4 + 4 * math.sin(t * 2))
        rrect(c, X + 60, Y + H_ - 70, W_ - 120, 10, 5, S["lavande"]); rrect(c, X + 60, Y + H_ - 70, (W_ - 120) * borne(t / 3.6), 10, 5, VIOLET)
        c.restore()
    # les demandes qui arrivent toutes seules, de chaque côté
    msgs = [tx("Nouveau client", "New customer"), tx("Demande de devis", "Quote request"), tx("Rendez-vous pris", "Meeting booked"), tx("Nouveau message", "New message")]
    for k, m in enumerate(msgs):
        u = entre(t, 1.3 + 0.35 * k, 0.45, 2.0)
        if u <= 0: continue
        x = (370 if k % 2 == 0 else 1550); y = 560 + 170 * (k // 2) + 30 * (k % 2)
        c.save(); c.translate(x, y); c.rotate(-4 if k % 2 == 0 else 4); c.scale(mix(0.4, 1, u), mix(0.4, 1, u))
        pill(c, m, 0, 0, 44, "blanc", "bell-ring", borne(u * 3))
        c.restore()


def accroche_solution(c, t):
    titre_accroche(c, t, tx("Montrez ce que vous faites.", "Show what you do."), tx("Donnez envie.", "Make it compelling."))
    # la vidéo du client qui joue, et les réactions qui montent
    a = entre(t, 0.35, 0.55, 1.6)
    X, Y, W_, H_ = 620, 470, 680, 383
    with Calque(c, borne(a * 3)):
        c.save(); c.translate(0, 60 * (1 - min(a, 1)))
        vs.verre(c, X - 24, Y - 24, W_ + 48, H_ + 48, 40)
        pub(c, X, Y, W_, H_, t + 0.6)
        c.restore()
    for k in range(9):
        u = prog(t, 1.4 + 0.22 * k, 1.3, sortie)
        if not 0 < u < 1: continue
        x = 1380 + 60 * math.sin(k * 2.3) + 40 * u * math.sin(k)
        icone(c, "heart" if k % 3 else "star", x, 900 - 520 * u, 60 * (1 - 0.3 * u), "#FF5A73" if k % 3 else "#FFC53D", 2.8, 1 - u)
    v = entre(t, 1.6, 0.5, 2.0)
    if v > 0:
        c.save(); c.translate(560, 900); c.rotate(-4); c.scale(mix(0.4, 1, v), mix(0.4, 1, v))
        pill(c, tx("Je veux le même", "I want this"), 0, 0, 46, "grad", "arrow-right", borne(v * 3))
        c.restore()
        eclats(c, 560, 900, t, 1.65, 12, 300, cols=[VIOLET, S["lilas"], "#FFC53D"], graine=12)


SCENES = {1: etape1, 2: etape2, 3: etape3, 4: etape4, 5: accroche_probleme, 6: accroche_benefice, 7: accroche_curiosite, 8: accroche_solution}


def dessine(c, t):
    fond_studio(c, 0.0)
    with Calque(c, enveloppe(t)):
        SCENES[ETAPE](c, t)
