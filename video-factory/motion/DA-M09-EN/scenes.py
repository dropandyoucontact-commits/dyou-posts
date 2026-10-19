"""DA-M09-EN « $5,000 » — pub DYOU Agency pour le marché US (anglais, Snapchat Ads, 16/10/2026), SANS PRIX :
on ancre la valeur, puis on renvoie sur le site pour le tarif.

Hook (ancrage de prix + la vidéo se prend en preuve) : « Big brands pay five thousand dollars for a video like this
one » — facture d'agence dont le total roule jusqu'à $5,000. « You're watching one right now » : on recule, la facture
est dans un téléphone, c'est cette vidéo. « And yours costs way less » : le total est barré, WAY LESS tombe dessus.
Corps commun (moteur/studio.py, version anglaise studio_en) ; pas d'écran prix ; fin « See what yours would cost. Tap the link. »
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio_en import anglais
import studio
anglais(prix=False)
studio.TR["Demander mon devis"] = "See pricing"

DUREE = 24.6
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

M = dict(b1=TW(22), produit=TW(26), service=TW(28), message=TW(32), oblige=TW(34), page=TW(37), b2=TW(39), motion=TW(40),
         captive=TW(43), regarde=TW(47), comprend=TW(48), action=TW(53), b3=TW(55), titre_b3="THE DIFFERENCE", attention=TW(60),
         demandes=TW(62), clients=TW(64), b4=TW(65), site=TW(68), expliquer=TW(70), facon=TW(71), simple=TW(74),
         long_texte=TW(75), b5=TW(80), script=TW(83), anime=TW(85), accroches=TW(89), tester=TW(92), prix=None,
         devis=TW(94), url=TW(99))
SOUS = sous_titres(K, fusions={(3, 4, 5): "$5,000"})

T_TITRE, T_FIVE, T_DOL, T_THIS = TW(0), TW(3), TW(5), TW(10)
T_YOU, T_NOW, T_COST, T_WAY, T_LESS, T_B1 = TW(12), TW(16), TW(19), TW(20), TW(21), TW(22)


# ─────────────────────────────────────────── la facture d'agence
def facture(c, t):
    x, y, w, h = 110, 520, 860, 700
    a = entre(t, -0.2, 0.55, 1.4)
    with Espace(c, 540, y + h / 2, rx=mix(30, 0, a), s=mix(0.8, 1, a)):
        with Calque(c, borne(a * 3)):
            carte_s(c, x, y, w, h, 40, ombre=0.16)
            tuile(c, "receipt", x + 86, y + 86, 84)
            texte(c, "INVOICE", x + 150, y + 52, 40, S["encre"], "noir", track=0.04)
            texte(c, "Big agency · #0417", x + 150, y + 100, 24, S["gris"], "demi", track=0)
            pill(c, "Due", x + w - 110, y + 86, 24, "rouge", "clock")
            lignes = [("Motion design video", "30 s"), ("Script & storyboard", ""), ("Animation & sound", "")]
            for k, (lab, d) in enumerate(lignes):
                u = entre(t, 0.15 + 0.12 * k, 0.4, 2.0)
                if u <= 0: continue
                yy = y + 190 + k * 86
                with Calque(c, borne(u * 3)):
                    disque(c, x + 62, yy + 20, 9, S["lilas"])
                    texte(c, lab, x + 90, yy + 4, 32, S["encre2"], "fort", track=-0.01)
                    if d: texte(c, d, x + w - 60, yy + 6, 28, S["gris"], "demi", "droite", 0)
                    rrect(c, x + 60, yy + 62, w - 120, 2, 1, S["ligne"])
            # le total qui roule jusqu'à $5,000
            ty = y + 470
            texte(c, "TOTAL", x + 60, ty + 52, 34, S["gris"], "titre", track=0.12)
            taille = 130
            parts = ["$", 5, ",", 0, 0, 0]
            ws = [largeur(str(p), taille, "noir", -0.04) for p in parts]
            xx = x + w - 60 - sum(ws)
            ua = entre(t, T_FIVE - 0.2, 0.3, 2)
            with Calque(c, borne(ua * 3)):
                for k, p in enumerate(parts):
                    if isinstance(p, int):
                        rouleau(c, p, xx, ty, taille, t, T_FIVE - 0.15 + 0.05 * k, T_DOL - 0.05 + 0.04 * k, S["encre"])
                    else:
                        texte(c, p, xx, ty, taille, S["encre"], "noir", track=-0.04)
                    xx += ws[k]
            # barré sur « costs »
            br = prog(t, T_COST - 0.05, 0.25, sortie)
            if br > 0:
                x0 = x + w - 60 - sum(ws) - 20
                trait(c, x0, ty + 120, x0 + (sum(ws) + 40) * br, ty + 30, S["rouge"], 14)
            # lueur sur le total à « dollars »
            sh = prog(t, T_DOL + 0.05, 0.5, lin)
            if 0 < sh < 1:
                p = skia.Paint(AntiAlias=True); sxp = mix(x, x + w, sh)
                p.setShader(skia.GradientShader.MakeLinear([skia.Point(sxp - 100, 0), skia.Point(sxp + 100, 0)], [hexa("#FFFFFF", 0), hexa("#FFFFFF", 0.6), hexa("#FFFFFF", 0)]))
                c.drawRect(skia.Rect.MakeXYWH(x, ty, w, 150), p)


def monde(c, t):
    """ce que montre l'écran : le titre et la facture"""
    lettres(c, "BIG BRANDS", 540, 230, 128, t, T_TITRE - 0.25, "ressort", decal=0.035)
    b = entre(t, TW(2) - 0.1, 0.4, 2.2)
    pill(c, "pay this", 540, 430, 34, "encre", "building-2", borne(b * 3), mix(0.4, 1, b), rot=-3)
    facture(c, t)
    if t > T_DOL:
        eclats(c, 760, 1050, t, T_DOL, 12, 380, graine=5)


PW, PH = 470, 940


def hook(c, t):
    recul = prog(t, T_YOU - 0.12, 0.5, entreeSortie)
    if recul <= 0:
        monde(c, t)
    else:
        retour = prog(t, T_COST - 0.25, 0.45, entreeSortie)
        s = mix(2.35, 1, recul) * mix(1, 1.18, retour)
        def ecran(cc, x, y, w, h):
            cc.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(S["papier"]))
            k = w / 1080
            cc.save(); cc.translate(x, y + (h - 1920 * k) / 2); cc.scale(k, k); monde(cc, t)
            cc.restore()
            barre_progression(cc, x + 24, y + h - 34, w - 48, borne((t - T_YOU + 1.2) / 4.5), 8, tete=False)
        with Espace(c, 540, 900, ry=6 * math.sin(t * 1.3) * recul, s=s):
            telephone_s(c, 540, 900, PW, PH, ecran)
        # « this video » : l'étiquette qui désigne le téléphone
        e = entre(t, T_YOU, 0.4, 2.2) * (1 - prog(t, T_COST - 0.2, 0.25, entree))
        if e > 0:
            pill(c, "This video", 540, 330, 36, "grad", "play", borne(e * 3), mix(0.4, 1, e), rot=-4)
            hy = 1400 + 18 * math.sin(t * 7)
            carte_s(c, 760 - 60, hy - 60, 120, 120, 60, "#FFFFFF", None, 0.18, borne(e * 3))
            icone(c, "hand", 760, hy, 62, S["encre"], 2.2, borne(e * 3))
        n = entre(t, T_NOW - 0.1, 0.4, 2.4) * (1 - prog(t, T_COST - 0.2, 0.25, entree))
        if n > 0:
            pill(c, "Right now", 300, 1180, 30, "rouge", "eye", borne(n * 3), mix(0.4, 1, n), rot=5)
    # WAY LESS tombe sur la facture
    st = entre(t, T_WAY - 0.08, 0.45, 2.6)
    if st > 0:
        sx_, sy_ = secousse(t, T_WAY, 18)
        c.save(); c.translate(540 + sx_, 1010 + sy_); c.rotate(-7)
        z = mix(2.6, 1, prog(t, T_WAY - 0.08, 0.22, entree))
        c.scale(z, z)
        with Calque(c, borne(st * 3)):
            carte_s(c, -380, -120, 760, 240, 50, "#FFFFFF", None, 0.22)
            texte_grad(c, "WAY LESS.", 0, -78, 128, "noir", "centre", -0.035)
        c.restore()
        g = entre(t, T_LESS + 0.05, 0.4, 2.4)
        if g > 0:
            pill(c, "Yours", 790, 1190, 32, "vert", "circle-check", borne(g * 3), mix(0.4, 1, g), rot=6)
        eclats(c, 540, 1010, t, T_WAY + 0.02, 16, 560, graine=7)
        onde(c, 540, 1010, t, T_WAY, 150, 700, S["violetVif"], 10, 0.6)


# ─────────────────────────────────────────── sons du hook
son(0.0, "impact", -7); son(0.0, "whoosh_court", -12); son(0.05, "pop", -13)
for k in range(3): son(0.15 + 0.12 * k, "pop", -17)
son(TW(2) - 0.1, "pop", -10)
for i in range(12): son(T_FIVE - 0.15 + i * (T_DOL - T_FIVE + 0.1) / 12, "tick", -16)
son(T_DOL - 0.05, "impact", -7); son(T_DOL, "ching", -9)
son(T_YOU - 0.12, "whoosh_bas", -9); son(T_YOU, "pop", -11); son(T_NOW - 0.1, "pop", -12)
son(T_COST - 0.25, "whoosh_court", -12); son(T_COST, "croc", -9)
son(T_WAY - 0.08, "whoosh_bas", -8); son(T_WAY, "tampon", -6); son(T_WAY + 0.03, "impact", -6); son(T_WAY + 0.06, "ching", -12)
son(T_LESS + 0.05, "check", -11)
son(T_B1 - 0.3, "whoosh_long", -9)
sons_corps(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.2), (T_YOU - 0.12, T_YOU + 0.35), (T_WAY - 0.1, T_WAY + 0.2), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_DOL, "#FFFFFF", 0.22), (T_WAY + 0.02, "#FFFFFF", 0.3), (M["page"] + 0.12, "#FFFFFF", 0.25),
                    (M["captive"] + 0.35, S["violetVif"], 0.08), (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    fond_studio(c, t, battement(t, T_WAY, 1, 0.5) + battement(t, M["captive"] + 0.35, 1, 0.5) - 2)
    scene_b1(c, t, M); scene_b2(c, t, M); scene_b3(c, t, M); scene_b4(c, t, M); scene_b5(c, t, M)
    scene_cta(c, t, M, DUREE)
    scene_prix(c, t, M)
    if t < T_B1 + 0.3:
        o = prog(t, T_B1 - 0.3, 0.35, entree)
        c.save(); c.translate(540, 900); c.scale(mix(1, 2.2, o), mix(1, 2.2, o)); c.translate(-540, -900)
        with Calque(c, 1 - o):
            hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    if t < M["devis"] - 0.25: SOUS.dessine(c, t, S["encre"])
