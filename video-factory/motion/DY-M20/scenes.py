"""DY-M20 v2 « Tu cherches un contact fiable en Chine ? » — organique TikTok DROP&YOU (28/10/2026).

v1 refusée par Youssef. Ce qui n'allait pas, mot pour mot :
  - **le ton** : « tu parles trop comme un podcast, comme quelqu'un qui fait un vlog ».
    Et « c'est nul de dire *ce que tu as vu sur quelqu'un est dans un de ces cartons* » — trop
    indirect. → on tutoie, on va droit au but, on VEND.
  - **un plan interdit** : le plan de conteneur montrait un dos avec un **QR d'une autre
    plateforme** dessus. Ce n'était pas lui (tourné pour CHINA FACTORY) et un renvoi hors
    plateforme est banni. Plan supprimé du dossier.
  - **« on est sur place à Guangzhou »** ne se dit plus → « on travaille depuis la Chine ».

L'angle, c'est **la peur de se faire arnaquer** : « tu cherches un contact fiable en Chine mais
t'as peur de tomber sur un arnaqueur ». Tout le reste du script sert à rassurer, avec des faits
vrais : huit ans de Chine, installés sur place depuis l'an dernier, de l'unité au gros, tous les
domaines, 8-12 jours, les différences de qualité montrées en vrai, le China Book pour qui veut
traiter en direct, et un appel possible avant de commander.

**Règle d'image posée ici** : quand la voix cite une catégorie, l'article montré est celui de la
catégorie citée. Les vêtements → la doudoune. Les montres → la montre. L'électronique → le casque.
Jamais un article qui ne correspond pas au mot (c'est le bug de la v1 : la veste sous « une montre »).

Décor : `moteur/nuit.py`, la pièce bleue en perspective. Voix Tomy, attaque à 6,26 mots/s.
CTA : « ajoute-moi sur le jaune » — jamais le nom de la plateforme, jamais son logo — et
« envoie cette vidéo à un pote ». Plus d'« abonne-toi / enregistre ».
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import lettres, eclats, entre, rayons, sous_titres
import nuit
from nuit import (FOND, FOND2, FOND3, BLEU, BLEU_VIF, GLACIER, BLANC, BLANC2,
                  GRIS, ROUGE, OR, VERT, AXE, AXE_HAUT, HORIZON, SOL)
from signature import signature, sons_signature

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 3.0, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = sous_titres(K)

LOGO = "logo-dy-blanc"
R = "produits/recents-2026-10/"
VETEMENT = R + "doudoune-moncler-noire"          # « les vêtements »
MONTRE = R + "montre-gmt-batman"                 # « les montres »
CASQUE = R + "casque-airpods-max-vert"           # « l'électronique »
PAIRE = R + "basket-lv-skate-bleue"
PAIRE2 = R + "basket-on-loewe-rose"
TROIS = [VETEMENT, MONTRE, CASQUE]
MOTS3 = ["LES VÊTEMENTS", "LES MONTRES", "L'ÉLECTRONIQUE"]
PLANCHE = "photos/situation-2026-10/chanel-baskets-planche"
V_ENTREPOT = "videos/entrepot-cartons"
V_AVION, V_STOCK = "videos/avion", "videos/baskets-stock-1"
MELANGE = [(PAIRE, False), (MONTRE, False), (VETEMENT, False), (CASQUE, False),
           (PAIRE2, False), (MONTRE, False)]

# ───────────────────────────── repères
T_HOOK, T_PEUR, T_ARNAQUEUR = TW(0), TW(7), TW(13)
T_NORMAL = TW(15)
T_NOUS, T_HUITANS, T_ANNEE, T_ICI = TW(21), TW(28), TW(30), TW(36)
T_TERRAIN = TW(38)
T_UNITE, T_TROUVE1 = TW(47), TW(55)
T_GROS, T_TROUVE2 = TW(59), TW(66)
T_TROIS = [TW(71), TW(73), TW(75)]
T_DOMAINES = TW(76)
T_ENVOIES, T_RESTE = TW(83), TW(90)
T_DEPUIS, T_JOURS = TW(94), TW(104)
T_QUALITES, T_DIFF, T_PRIX, T_CHOISIS = TW(109), TW(116), TW(123), TW(129)
T_FOURNISSEURS, T_CHINABOOK = TW(135), TW(146)
T_APPELER = TW(152)
T_CTA, T_POTE = TW(160), TW(165)
T_FIN = round(K.timing["duree_voix"] - 0.1, 2)

PIVOTS = (T_HOOK, T_ARNAQUEUR, T_NOUS, T_TROIS[0], T_QUALITES, T_CHINABOOK, T_CTA)


# ═════════════════════════════ briques
def article(c, t, nom, x, y, w, u, flotte=0.0, rot=0.0, z0=5.0, a=1.0, h_max=None):
    """un vrai article posé dans la pièce : il vient du point de fuite et grandit jusqu'à nous.
    h_max borne la hauteur (une montre est deux fois plus haute que large)."""
    if u <= 0.005 or a <= 0.01: return
    iw, ih = taille_img(nom)
    h = w * ih / iw
    if h_max and h > h_max:
        x += (w - w * h_max / h) / 2
        w, h = w * h_max / h, h_max
    cx, cy = x + w / 2, y + h / 2
    z = mix(z0, 1.0, sortieExpo(borne(u)))
    s = nuit.echelle_z(z)
    px = mix(AXE, cx, sortieExpo(borne(u)))
    py = mix(HORIZON, cy, sortieExpo(borne(u)))
    dy = flotte * 14 * math.sin(t * 1.7)
    c.save(); c.translate(px, py + dy); c.rotate(rot * (1 - u) + rot * 0.25)
    c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, a * borne(u * 3)):
        nuit.pose_sol(c, cx, y + h, w * 0.9, 0.24)
        image(c, nom, x, y, w)
    c.restore()


def cadre(c, t, nom, x, y, w, h, u, a=1.0, t0=None, vid=True, zoom=1.08, fy=0.5, z0=4.0):
    """un plan réel (vidéo ou photo) posé dans la pièce, cadre en verre à liseré glacier"""
    if u <= 0.005 or a <= 0.01: return
    cx, cy = x + w / 2, y + h / 2
    z = mix(z0, 1.0, sortieExpo(borne(u)))
    sc = nuit.echelle_z(z)
    px = mix(AXE, cx, sortieExpo(borne(u)))
    py = mix(HORIZON, cy, sortieExpo(borne(u)))
    c.save(); c.translate(px, py); c.scale(sc, sc); c.translate(-cx, -cy)
    with Calque(c, a * borne(u * 3)):
        nuit.pose_sol(c, cx, y + h, w, 0.24)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 22, 22)
        nuit.halo(c, rr, 0.34, 28)
        c.drawRRect(rr, peinture(FOND2))
        if vid:
            video(c, nom, x + 8, y + 8, w - 16, h - 16, max(0.0, t - (t0 or 0.0)), 1.0, rayon=16)
        else:
            image_cover(c, nom, x + 8, y + 8, w - 16, h - 16, zoom, 0.5, fy, rayon=16)
        c.drawRRect(rr, peinture(GLACIER, 0.75, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
    c.restore()


def titre(c, txt, y, taille, t, t0, couleur=None, alpha=1.0, effet="masque", decal=0.02):
    haut = y < 775
    larg = 920 if haut else 715
    cx = AXE_HAUT if haut else AXE
    ts = ajuste(txt, larg, taille, "noir", -0.022)
    lettres(c, txt, cx, y, ts, t, t0, effet, grad=False,
            couleur=couleur or BLANC, decal=decal, track=-0.022, alpha=alpha)


def surligne(c, txt, y, taille, u, couleur=BLEU_VIF):
    if u <= 0.01: return
    haut = y < 775
    larg, cx = (920, AXE_HAUT) if haut else (715, AXE)
    ts = ajuste(txt, larg, taille, "noir", -0.022)
    w = largeur(txt, ts, "noir", -0.022)
    h = hauteurLigne(ts, "noir") * 0.82
    rrect(c, cx - w / 2 - 18, y + h * 0.16, (w + 36) * borne(u), h, 8, couleur, 1.0)


def pastille(c, txt, cx, cy, u, a=1.0, taille=50, couleur=None, encre=None, rot=0.0):
    if u <= 0.01 or a <= 0.01: return
    couleur = couleur or BLANC
    if encre is None:
        encre = BLANC if couleur in (BLEU_VIF, BLEU, ROUGE, VERT) else FOND
    ts = ajuste(txt, 620, taille, "noir", -0.02)
    w, h = largeur(txt, ts, "noir", -0.02) + 64, ts * 1.9
    c.save(); c.translate(cx, cy + mix(-60, 0, u)); c.rotate(rot); c.scale(mix(0.84, 1, u), mix(0.84, 1, u))
    with Calque(c, a * borne(u * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        nuit.halo(c, rr, 0.28, 18, couleur if couleur != BLANC else GLACIER)
        rrect(c, -w / 2, -h / 2, w, h, h / 2, couleur, 1.0)
        texte(c, txt, 0, -hauteurLigne(ts, "noir") / 2, ts, encre, "noir", "centre", -0.02)
    c.restore()


def telephone(c, t, cx, cy, h, u, dessin=None):
    if u <= 0.005: return
    w = h * 0.47
    z = mix(4.5, 1.0, sortieExpo(borne(u)))
    s = nuit.echelle_z(z)
    px, py = mix(AXE, cx, sortieExpo(borne(u))), mix(HORIZON, cy, sortieExpo(borne(u)))
    c.save(); c.translate(px, py); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, borne(u * 3)):
        nuit.pose_sol(c, cx, cy + h / 2, w * 1.3, 0.26)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), 44, 44)
        nuit.halo(c, rr, 0.34, 30)
        c.drawRRect(rr, peinture(FOND2))
        c.drawRRect(rr, peinture(GLACIER, 0.8, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        c.save()
        c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2 + 9, cy - h / 2 + 9,
                                                             w - 18, h - 18), 36, 36), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), peinture(FOND3))
        if dessin: dessin(c, cx, cy, w - 18, h - 18)
        c.restore()
        lw = w * 0.42
        image(c, LOGO, cx - lw / 2, cy - h / 2 + 34, lw)
    c.restore()


def nombre(c, valeur, suffixe, cx, cy, u, taille=190, sous=None, a=1.0):
    """un chiffre qui monte — les huit ans, les huit à douze jours"""
    if a <= 0.01 or u <= 0.004: return
    from kit import texte_centre
    n = max(1, int(round(valeur * sortieExpo(borne(u)))))
    with Calque(c, a):
        texte_centre(c, f"{n}{suffixe}", cx, cy, taille, BLANC, "noir")
        if sous:
            texte(c, sous.upper(), cx, cy + taille * 0.44, 38, GLACIER, "fort", "centre", 0.16)


def carte_qualite(c, t, titre_q, cote, u, barres, couleur):
    """deux panneaux côte à côte : la même pièce en deux qualités. Jamais de chiffre de prix —
    les barres montrent l'écart, pas un montant (règle du 17/10)."""
    if u <= 0.01: return
    w, h = 320, 420
    x = AXE + cote * 178 - w / 2
    y = 880
    with Calque(c, borne(u * 2.2)):
        c.save(); c.translate(0, mix(70 * cote, 0, sortieExpo(u)))
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 26, 26)
        nuit.halo(c, rr, 0.30, 22, couleur)
        c.drawRRect(rr, peinture(FOND2))
        c.drawRRect(rr, peinture(couleur, 0.8, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        texte(c, titre_q, x + w / 2, y + 26, 50, couleur, "noir", "centre", 0.02)
        for k in range(4):
            v = borne((u - 0.1 - 0.12 * k) * 3)
            if v <= 0: continue
            plein = k < barres
            rrect(c, x + 34, y + 114 + k * 54, (w - 68) * v, 24, 12,
                  couleur if plein else GRIS, 1.0 if plein else 0.45)
        texte(c, "PRIX", x + w / 2, y + h - 100, 32, BLANC2, "fort", "centre", 0.16)
        for k in range(3):
            plein = k < (1 if barres <= 2 else 3)
            rrect(c, x + w / 2 - 52 + k * 36, y + h - 54, 26, 26, 6,
                  couleur if plein else GRIS, 1.0 if plein else 0.4)
        c.restore()


def livre(c, t, u, cx=AXE, cy=1020):
    """le China Book : un panneau en verre, posé debout dans la pièce"""
    if u <= 0.01: return
    w, h = 420, 520
    z = mix(4.0, 1.0, sortieExpo(borne(u)))
    s = nuit.echelle_z(z)
    px, py = mix(AXE, cx, sortieExpo(borne(u))), mix(HORIZON, cy, sortieExpo(borne(u)))
    c.save(); c.translate(px, py); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, borne(u * 3)):
        nuit.pose_sol(c, cx, cy + h / 2, w * 1.2, 0.28)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), 18, 18)
        nuit.halo(c, rr, 0.38, 30)
        c.drawRRect(rr, peinture(FOND2))
        c.drawRRect(rr, peinture(GLACIER, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        rrect(c, cx - w / 2 + 16, cy - h / 2 + 16, 14, h - 32, 7, BLEU_VIF, 1.0)   # la tranche
        texte(c, "CHINA", cx + 14, cy - 110, 76, BLANC, "noir", "centre", -0.01)
        texte(c, "BOOK", cx + 14, cy - 22, 76, BLEU_VIF, "noir", "centre", -0.01)
        trait(c, cx - 104, cy + 84, cx + 132, cy + 84, GLACIER, 4, 0.8)
        texte(c, "LES FOURNISSEURS", cx + 14, cy + 112, 30, BLANC2, "fort", "centre", 0.14)
    c.restore()


# ═════════════════════════════ 1. HOOK — la peur, et la preuve derrière
def hook(c, t):
    if t > T_NOUS - 0.16: return
    sor = prog(t, T_NOUS - 0.38, 0.24, entree)
    with Calque(c, 1 - sor):
        nuit.ondes_sol(c, t, -0.1, 0.6, 5, 0.9)
        # le stock arrive, puis il REPART au point de fuite quand la peur tombe : le bon contact
        # qui s'éloigne. (La photo de cartons portait un logo de marque en gros → écartée.)
        u = prog(t, -0.14, 0.34, sortieExpo)
        recul = prog(t, T_PEUR - 0.14, 0.5, douce)
        cadre(c, t, PLANCHE, 150, 640, 780, 520, mix(borne(u), 0.52, recul),
              vid=False, zoom=1.1, z0=5.5)
        if recul > 0.3:
            nuit.ondes_sol(c, t, T_PEUR, 0.75 * recul, 5, 1.0, ROUGE)
        a_h = 1 - prog(t, T_PEUR - 0.2, 0.14, entree)
        if a_h > 0.01:
            titre(c, "TU CHERCHES UN CONTACT", 280, 88, t, TW(1) - 0.06, alpha=a_h, decal=0.012)
            if t > TW(4) - 0.08:
                titre(c, "FIABLE EN CHINE ?", 390, 104, t, TW(4) - 0.05, alpha=a_h,
                      couleur=BLEU_VIF, decal=0.016)
        if t > T_PEUR - 0.14:
            titre(c, "MAIS T'AS PEUR DE TOMBER", 280, 84, t, T_PEUR - 0.05, decal=0.01)
            if t > T_ARNAQUEUR - 0.18:
                u2 = prog(t, T_ARNAQUEUR - 0.18, 0.2, sortieExpo)
                surligne(c, "SUR UN ARNAQUEUR ?", 390, 110, u2, ROUGE)
                titre(c, "SUR UN ARNAQUEUR ?", 390, 110, t, T_ARNAQUEUR - 0.08,
                      couleur=BLANC, effet="ressort", decal=0.018)
        if t > T_NORMAL - 0.12:
            pastille(c, "C'EST NORMAL, Y EN A PARTOUT", AXE, 1310,
                     entre(t, T_NORMAL - 0.07), taille=54, couleur=ROUGE, rot=-1.4)


# ═════════════════════════════ 2. HUIT ANS, ET INSTALLÉS SUR PLACE
def huit_ans(c, t):
    if t < T_NOUS - 0.28 or t > T_UNITE - 0.16: return
    ent = prog(t, T_NOUS - 0.26, 0.3, sortieExpo)
    sor = prog(t, T_UNITE - 0.36, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        a_h = 1 - prog(t, T_ANNEE - 0.2, 0.14, entree)
        if a_h > 0.01:
            titre(c, "NOUS, ON TRAVAILLE", 280, 92, t, T_NOUS - 0.05, alpha=a_h, decal=0.014)
            titre(c, "AVEC LA CHINE DEPUIS", 390, 92, t, TW(24) - 0.05, alpha=a_h, decal=0.014)
            nombre(c, 8, " ANS", AXE, 900, prog(t, T_NOUS - 0.12, 1.1, lin), 200, None, a_h)
            pastille(c, "ET ON N'A JAMAIS BOUGÉ", AXE, 1270,
                     entre(t, T_NOUS + 0.25), a_h, taille=56, couleur=BLEU_VIF, rot=-1.4)
        if t > T_ANNEE - 0.14:
            titre(c, "ET L'ANNÉE DERNIÈRE,", 280, 88, t, T_ANNEE - 0.05, decal=0.012)
            if t > T_ICI - 0.14:
                u2 = prog(t, T_ICI - 0.16, 0.2, sortieExpo)
                surligne(c, "ON EST VENUS S'INSTALLER ICI", 390, 76, u2)
                titre(c, "ON EST VENUS S'INSTALLER ICI", 390, 76, t, T_ICI - 0.07,
                      couleur=BLANC, effet="ressort", decal=0.008)
            u3 = prog(t, T_ANNEE - 0.1, 0.45, lin)
            cadre(c, t, V_ENTREPOT, 150, 660, 780, 439, borne(u3), t0=T_ANNEE - 0.1, z0=3.4)
            if t > T_TERRAIN - 0.12:
                pastille(c, "SUR LE TERRAIN, TOUS LES JOURS", AXE, 1250,
                         entre(t, T_TERRAIN - 0.07), taille=52, couleur=BLEU_VIF, rot=1.4)


# ═════════════════════════════ 3. À L'UNITÉ OU EN GROS
def unite_gros(c, t):
    if t < T_UNITE - 0.26 or t > T_TROIS[0] - 0.14: return
    ent = prog(t, T_UNITE - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_TROIS[0] - 0.3, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        a_h = 1 - prog(t, T_GROS - 0.2, 0.14, entree)
        if a_h > 0.01:
            titre(c, "TU VEUX UN SEUL ARTICLE", 280, 88, t, T_UNITE - 0.05, alpha=a_h, decal=0.012)
            titre(c, "POUR T'HABILLER ?", 390, 100, t, TW(52) - 0.05, alpha=a_h,
                  couleur=BLEU_VIF, decal=0.016)
            article(c, t, PAIRE, 230, 640, 620, prog(t, T_UNITE - 0.12, 0.45, sortieExpo),
                    flotte=1.0, z0=4.0, a=a_h, h_max=420)
            av_u = 1 - prog(t, T_TROUVE1 - 0.18, 0.12, entree)
            if av_u > 0.01:
                pastille(c, "MÊME À L'UNITÉ", AXE, 1230, entre(t, T_UNITE + 0.12),
                         a_h * av_u, taille=62, couleur=BLEU_VIF, rot=1.4)
            if t > T_TROUVE1 - 0.12:
                pastille(c, "ON TE LE TROUVE", AXE, 1230, entre(t, T_TROUVE1 - 0.07), a_h,
                         taille=70, rot=-1.4)
        if t > T_GROS - 0.14:
            titre(c, "TU VEUX DU GROS", 280, 92, t, T_GROS - 0.05, decal=0.014)
            titre(c, "POUR TA BOUTIQUE ?", 390, 100, t, TW(63) - 0.05, couleur=BLEU_VIF, decal=0.016)
            u2 = prog(t, T_GROS - 0.1, 0.45, lin)
            cadre(c, t, V_STOCK, 150, 660, 780, 439, borne(u2), t0=T_GROS - 0.1, z0=3.2)
            if t > T_TROUVE2 - 0.12:
                pastille(c, "ON TE LE TROUVE AUSSI", AXE, 1250,
                         entre(t, T_TROUVE2 - 0.07), taille=66, couleur=BLEU_VIF, rot=1.4)


# ═════════════════════════════ 4. LES TROIS DOMAINES — l'article suit le mot
def domaines(c, t):
    if t < T_TROIS[0] - 0.2 or t > T_ENVOIES - 0.14: return
    ent = prog(t, T_TROIS[0] - 0.18, 0.24, sortieExpo)
    sor = prog(t, T_ENVOIES - 0.3, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        for k, t0 in enumerate(T_TROIS):
            suivant = T_TROIS[k + 1] if k + 1 < len(T_TROIS) else T_DOMAINES + 0.35
            # fenêtres sans recouvrement : l'article et le mot démarrent et s'arrêtent ensemble
            if t < t0 - 0.06 or t > suivant - 0.05: continue
            a = 1 - prog(t, suivant - 0.11, 0.06, entree)
            article(c, t, TROIS[k], 215, 560, 650, entre(t, t0 - 0.06, 0.2, 3.8),
                    flotte=1.0, rot=-3 if k % 2 else 3, z0=3.0, a=a, h_max=500)
            pastille(c, MOTS3[k], AXE, 1220, entre(t, t0 - 0.04), a, taille=78,
                     couleur=BLEU_VIF if k == 1 else BLANC, rot=-1.4 if k % 2 else 1.4)
            eclats(c, AXE, 820, t, t0 - 0.04, 10, 300, [BLEU_VIF, GLACIER, BLANC], 4, 0.6)
        if t > T_DOMAINES + 0.1:
            # les trois se rangent côte à côte : l'image de « tous les domaines »
            for k, nom in enumerate(TROIS):
                uu = prog(t, T_DOMAINES + 0.14 + 0.1 * k, 0.4, sortieExpo)
                article(c, t, nom, 120 + k * 290, 880, 270, uu, flotte=1.0,
                        rot=-3 + 3 * k, z0=2.6, h_max=320)
        if t > T_DOMAINES + 0.2:
            titre(c, "ON EST BRANCHÉS", 300, 96, t, T_DOMAINES + 0.24, decal=0.014)
            u2 = prog(t, TW(80) - 0.14, 0.2, sortieExpo)
            surligne(c, "DANS TOUS LES DOMAINES", 420, 92, u2)
            titre(c, "DANS TOUS LES DOMAINES", 420, 92, t, TW(80) - 0.06, couleur=BLANC,
                  effet="ressort", decal=0.012)


# ═════════════════════════════ 5. TU M'ENVOIES, JE M'OCCUPE DU RESTE
def envoie(c, t):
    if t < T_ENVOIES - 0.26 or t > T_QUALITES - 0.14: return
    ent = prog(t, T_ENVOIES - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_QUALITES - 0.3, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        a_h = 1 - prog(t, T_DEPUIS - 0.2, 0.14, entree)
        if a_h > 0.01:
            titre(c, "TU M'ENVOIES CE QUE TU CHERCHES", 280, 76, t, T_ENVOIES - 0.05,
                  alpha=a_h, decal=0.008)
            if t > T_RESTE - 0.12:
                titre(c, "JE M'OCCUPE DU RESTE", 390, 100, t, T_RESTE - 0.05, alpha=a_h,
                      couleur=BLEU_VIF, effet="ressort", decal=0.016)

            def ecran(cc, cx, cy, w, h):
                k = int(max(0.0, t - (T_ENVOIES - 0.1)) * 2.0) % 3
                nom = [PAIRE2, MONTRE, VETEMENT][k]
                iw, ih = taille_img(nom)
                pw = w * 0.80
                image(cc, nom, cx - pw / 2, cy - pw * ih / iw / 2, pw)
            telephone(c, t, AXE, 980, 650, prog(t, T_ENVOIES - 0.16, 0.42, lin) * a_h, ecran)
        if t > T_DEPUIS - 0.14:
            titre(c, "ON TRAVAILLE DEPUIS LA CHINE", 280, 76, t, T_DEPUIS - 0.05, decal=0.008)
            u2 = prog(t, T_DEPUIS - 0.1, 0.45, lin)
            cadre(c, t, V_AVION, 150, 620, 780, 439, borne(u2), t0=T_DEPUIS - 0.1, z0=3.4)
            if t > T_JOURS - 0.16:
                nombre(c, 12, " JOURS", AXE, 1230, prog(t, T_JOURS - 0.14, 0.4, lin),
                       136, "chez toi, en 8 à 12 jours")


# ═════════════════════════════ 6. LES QUALITÉS, MONTRÉES EN VRAI
def qualites(c, t):
    if t < T_QUALITES - 0.26 or t > T_FOURNISSEURS - 0.14: return
    ent = prog(t, T_QUALITES - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_FOURNISSEURS - 0.3, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        titre(c, "SUR CERTAINS ARTICLES,", 280, 82, t, T_QUALITES - 0.05, decal=0.01)
        titre(c, "IL EXISTE PLUSIEURS QUALITÉS", 390, 80, t, TW(113) - 0.05,
              couleur=GLACIER, decal=0.008)
        carte_qualite(c, t, "QUALITÉ 1", -1, prog(t, T_QUALITES + 0.05, 0.5, lin), 2, GLACIER)
        carte_qualite(c, t, "QUALITÉ 2", 1, prog(t, T_QUALITES + 0.22, 0.5, lin), 4, BLEU_VIF)
        if t > T_PRIX - 0.12:
            pastille(c, "ON TE MONTRE LES DEUX EN VRAI", AXE, 1355,
                     entre(t, T_PRIX - 0.07) * (1 - prog(t, T_CHOISIS - 0.2, 0.14, entree)),
                     taille=48, couleur=BLEU_VIF, rot=-1.4)
        if t > T_CHOISIS - 0.14:
            pastille(c, "TU CHOISIS EN CONNAISSANCE DE CAUSE", AXE, 1355,
                     entre(t, T_CHOISIS - 0.07), taille=46, rot=1.4)


# ═════════════════════════════ 7. LE CHINA BOOK
def chinabook(c, t):
    if t < T_FOURNISSEURS - 0.26 or t > T_CTA - 0.14: return
    ent = prog(t, T_FOURNISSEURS - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_CTA - 0.3, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        titre(c, "TU VEUX TRAITER AVEC", 270, 84, t, T_FOURNISSEURS - 0.05, decal=0.01)
        titre(c, "LES FOURNISSEURS TOI-MÊME ?", 370, 80, t, TW(141) - 0.05,
              couleur=BLEU_VIF, decal=0.008)
        livre(c, t, prog(t, T_FOURNISSEURS - 0.22, 0.55, lin), AXE, 1000)
        if t > T_APPELER - 0.14:
            pastille(c, "ON PEUT MÊME S'APPELER AVANT", AXE, 1355,
                     entre(t, T_APPELER - 0.07), taille=50, couleur=BLEU_VIF, rot=1.4)


# ═════════════════════════════ 8. L'APPEL
def cta(c, t):
    if t < T_CTA - 0.26 or t > T_FIN + 0.1: return
    ent = prog(t, T_CTA - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_FIN - 0.22, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        nuit.ondes_sol(c, t, T_CTA - 0.3, 0.8, 5, 0.9)
        rayons(c, AXE, 820, t, 1150, 0.09, 16, BLEU_VIF)
        a_h = 1 - prog(t, T_POTE - 0.2, 0.14, entree)
        if a_h > 0.01:
            titre(c, "ALORS AJOUTE-MOI", 330, 112, t, T_CTA - 0.05, alpha=a_h, decal=0.018)
            u = prog(t, TW(163) - 0.16, 0.2, sortieExpo)
            surligne(c, "SUR LE JAUNE", 460, 134, u * a_h)
            titre(c, "SUR LE JAUNE", 460, 134, t, TW(163) - 0.07, couleur=BLANC,
                  effet="ressort", alpha=a_h, decal=0.024)
        if t > T_POTE - 0.14:
            titre(c, "ET ENVOIE CETTE VIDÉO", 330, 92, t, T_POTE - 0.05, decal=0.012)
            titre(c, "À UN POTE QUI CHERCHE", 440, 92, t, TW(169) - 0.05,
                  couleur=BLEU_VIF, decal=0.012)
            titre(c, "UN CONTACT EN CHINE", 550, 92, t, TW(174) - 0.05, decal=0.012)
        if t > T_CTA + 0.2:
            article(c, t, PAIRE2, 290, 920, 500, prog(t, T_CTA + 0.24, 0.45, sortieExpo),
                    flotte=1.0, z0=3.4, h_max=360)


# ═════════════════════════════ sons
son(0.0, "impact", -2); son(0.0, "whoosh_long", -7)
son(T_PEUR - 0.2, "swipe", -10); son(T_ARNAQUEUR - 0.08, "impact", -4)
son(T_NORMAL - 0.07, "pop", -9)
son(T_NOUS - 0.24, "whoosh", -9); son(T_HUITANS - 0.12, "montee", -10)
son(T_ANNEE - 0.12, "whoosh_court", -10); son(T_ICI - 0.07, "tampon", -7)
son(T_TERRAIN - 0.07, "pop", -10)
son(T_UNITE - 0.24, "whoosh", -9); son(T_TROUVE1 - 0.07, "pop", -9)
son(T_GROS - 0.12, "whoosh_court", -10); son(T_TROUVE2 - 0.07, "pop", -9)
for t0 in T_TROIS:
    son(t0 - 0.1, "whoosh_court", -11); son(t0 - 0.04, "pop", -8)
son(TW(80) - 0.06, "tampon", -7)
son(T_ENVOIES - 0.24, "whoosh", -9); son(T_RESTE - 0.06, "ching", -9)
son(T_DEPUIS - 0.12, "whoosh_bas", -9); son(T_JOURS - 0.12, "montee", -10)
son(T_QUALITES - 0.24, "whoosh", -9); son(T_QUALITES + 0.03, "verre", -9)
son(T_QUALITES + 0.2, "verre", -10); son(T_CHOISIS - 0.07, "check", -9)
son(T_FOURNISSEURS - 0.24, "whoosh", -9); son(T_FOURNISSEURS - 0.18, "impact_doux", -7)
son(T_APPELER - 0.07, "pop", -9)
son(T_CTA - 0.24, "whoosh_long", -7); son(TW(163) - 0.08, "tampon", -6)
son(T_POTE - 0.07, "swipe", -10)
sons_signature(son, T_FIN)

for a, b in [(0.0, 0.6), (T_PEUR - 0.2, T_PEUR + 0.25), (T_ARNAQUEUR - 0.1, T_ARNAQUEUR + 0.35),
             (T_NOUS - 0.24, T_NOUS + 0.25), (T_ANNEE - 0.12, T_ANNEE + 0.25),
             (T_ICI - 0.1, T_ICI + 0.3), (T_UNITE - 0.24, T_UNITE + 0.25),
             (T_GROS - 0.12, T_GROS + 0.25), (T_TROIS[0] - 0.12, T_TROIS[0] + 0.16),
             (T_TROIS[1] - 0.1, T_TROIS[1] + 0.14), (T_TROIS[2] - 0.1, T_TROIS[2] + 0.14),
             (T_ENVOIES - 0.24, T_ENVOIES + 0.25), (T_DEPUIS - 0.12, T_DEPUIS + 0.25),
             (T_QUALITES - 0.24, T_QUALITES + 0.25), (T_FOURNISSEURS - 0.24, T_FOURNISSEURS + 0.25),
             (T_CTA - 0.24, T_CTA + 0.35), (T_FIN - 0.1, T_FIN + 0.6)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, BLEU_VIF, 0.10), (T_ARNAQUEUR, ROUGE, 0.13), (T_HUITANS, BLEU_VIF, 0.10),
                    (T_ICI, BLANC, 0.10), (T_TROIS[0], BLEU_VIF, 0.09), (T_JOURS, BLEU_VIF, 0.10),
                    (T_DIFF, GLACIER, 0.09), (T_FOURNISSEURS, BLEU_VIF, 0.11),
                    (T_CTA, BLEU_VIF, 0.10)]:
    eclair(tt, cc_, a_)


# ═════════════════════════════ composition
def fond(c, t):
    pulse = (battement(t, T_ARNAQUEUR, 1, 0.5) - 1) + (battement(t, T_ICI, 1, 0.5) - 1) \
          + (battement(t, T_FOURNISSEURS, 1, 0.5) - 1)
    nuit.fond(c, t, pulse, vitesse=nuit.vitesse(t, PIVOTS))


def dessine(c, t):
    fond(c, t)
    hook(c, t); huit_ans(c, t); unite_gros(c, t); domaines(c, t)
    envoie(c, t); qualites(c, t); chinabook(c, t); cta(c, t)
    if t >= T_FIN - 0.12:
        signature(c, t, T_FIN, MELANGE, LOGO, AXE, 880, accent=GLACIER, encre=BLANC)
    if t < T_FIN - 0.02:
        SOUS.dessine(c, t, BLANC)
    K.dessine_eclairs(c, t)
