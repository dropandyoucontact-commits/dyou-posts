"""CB-M11 « La nouvelle taxe sur les colis » — organique ChinaBook / DROP&YOU (14/10/2026).

Faits vérifiés le 14/10/2026 (info.gouv.fr, règlement (UE) 2026/382) : depuis le 1er juillet 2026, fin de la franchise de
150 € ; droit forfaitaire de 3 € par catégorie d'article (position tarifaire) dans les colis de 150 € ou moins venus hors UE ;
redevance européenne de gestion par colis annoncée pour le 1er novembre 2026 (montant non affiché : pas encore fixé).
Règles : « enregistre » dans le hook, partage ciblé, boucle ouverte (l'astuce sous cadenas jusqu'à la fin), fond sombre
violet (jamais blanc), Tomy à 4 mots/s, ChinaBook violet « par DROP&YOU » à la fin.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence
from studio import lettres, Groupe, eclats, rayons, curseur, entre, rouleau, SousTitresEncre

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.6, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

JAUNE, ROUGE, VERT, BLANC, BLEU = "#FFD43B", "#FF4D5E", "#2BD67B", "#FFFFFF", "#3D7BFF"
V, VC = A["violet"], A["violetClair"]
CLAIR = [BLANC, "#E6DCFF"]

SOUS = SousTitresEncre(K, fusions={(6, 7): "1er juillet,", (45, 46, 47): "150 €", (57, 58): "3 €", (64, 65): "3 €,",
                                  (80, 81): "9 €.", (112,): "10", (116,): "10", (129,): "20",
                                  (197, 198): "ChinaBook,", (200, 201, 202): "DROP&YOU."},
                       y=1410, larg=900, taille=54, fam="gras", max_mots=5)

# ─────────────────────────────────────────── temps des parties
T_ENR = TW(14)                      # « Enregistre cette vidéo »
T_X2 = TW(24)                       # « deux fois trop »
T_RESTE = TW(27) - 0.1              # « Et reste jusqu'à la fin »
T_AVANT = TW(39)                    # « Avant, un colis… »
T_FINI = TW(53)                     # « C'est fini. »
T_REGLE = TW(55)                    # « Maintenant, c'est trois euros… »
T_PARTAGE = TW(82)                  # « Envoie cette vidéo… »
T_NOV = TW(94)                      # « Et ce n'est pas tout : en novembre… »
T_ASTUCE = TW(120)                  # « Alors voilà l'astuce. »
ETAPES = [TW(123), TW(146), TW(156)]
T_COM = TW(175) - 0.1               # « Dis-moi en commentaire… »
T_LOGO_CB = TW(185) - 0.1           # « Les fournisseurs et le transitaire… »
T_SANS_SOUS = TW(197) - 0.05        # le logo dit « ChinaBook par DROP&YOU » : plus de sous-titre


# ─────────────────────────────────────────── briques communes
def entete_marque(c, t):
    iw, ih = taille_img("logo-dy-blanc"); lw = 230
    image(c, "logo-dy-blanc", 70, 300 - lw * ih / iw / 2, lw, 0.95)


def entete(c, t, n, titre, t0, cols=None, y=500):
    a = entre(t, t0 - 0.12, 0.45, 2.0)
    if a > 0 and n:
        c.save(); c.translate(150, y); c.rotate(-8 * (1 - a)); c.scale(mix(2.4, 1, a), mix(2.4, 1, a))
        lueur(c, 0, 0, 120, JAUNE, 0.35)
        disque(c, 0, 0, 62, JAUNE)
        texte(c, str(n), 0, -hauteurLigne(78) / 2, 78, "#1A1030", "noir", "centre", -0.02)
        c.restore()
    taille = ajuste(titre, 760 if n else 940, 96, "noir", -0.03)
    lettres(c, titre, 240 if n else 540, y - taille * 0.62, taille, t, t0 - 0.05, "masque", decal=0.025, duree=0.4,
            align="gauche" if n else "centre", grad=True, cols=cols or CLAIR)


def carte(c, cx, cy, w, h, r=40, violet=0.0, alpha=1.0, s=1.0, rot=0.0):
    if alpha <= 0.01 or s <= 0.01: return
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        verre(c, -w / 2, -h / 2, w, h, r, 0.08, violet=violet)
    c.restore()


def tampon_c(c, label, cx, cy, t, t0, couleur=JAUNE, rot=-9, taille=52):
    if t < t0 - 0.12: return
    u = prog(t, t0 - 0.12, 0.16, entree)
    s = mix(2.6, 1, u)
    tw = largeur(label, taille, "noir"); w, h = tw + taille * 1.2, taille * 1.9
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, u):
        rrect(c, -w / 2, -h / 2, w, h, 20, "#140C26", 0.85, None, couleur, 8)
        texte(c, label, 0, -hauteurLigne(taille) / 2, taille, couleur, "noir", "centre", -0.01)
    c.restore()


def interdit(c, cx, cy, r, u):
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.scale(mix(1.6, 1, u), mix(1.6, 1, u))
    with Calque(c, borne(u * 3)):
        anneau(c, 0, 0, r, ROUGE, 14)
        trait(c, -r * 0.7, -r * 0.7, r * 0.7, r * 0.7, ROUGE, 14)
    c.restore()


def signet(c, cx, cy, taille, plein, alpha=1.0):
    k = taille / 100
    pth = skia.Path(); pth.moveTo(cx - 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy + 50 * k)
    pth.lineTo(cx, cy + 24 * k); pth.lineTo(cx - 36 * k, cy + 50 * k); pth.close()
    with Calque(c, alpha):
        if plein > 0:
            c.save(); c.clipRect(skia.Rect.MakeXYWH(cx - 60 * k, cy + 52 * k - 104 * k * plein, 120 * k, 104 * k * plein))
            c.drawPath(pth, peinture(JAUNE)); c.restore()
        c.drawPath(pth, peinture(BLANC, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=7 * k, StrokeJoin=skia.Paint.kRound_Join))


def drapeau_ue(c, x, y, w, h, r=8):
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#003399"))
    for k in range(12):
        a = k * math.pi / 6
        c.drawPath(etoile(x + w / 2 + h * 0.33 * math.cos(a), y + h / 2 + h * 0.33 * math.sin(a), h * 0.065), peinture("#FFCC00"))
    c.restore()


def pantalon(c, cx, cy, h, couleur="#5B6CFF", alpha=1.0, rot=0.0):
    k = h / 100
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(k, k)
    with Calque(c, alpha):
        p = skia.Path()
        p.moveTo(-26, -50); p.lineTo(26, -50); p.lineTo(30, 50); p.lineTo(8, 50); p.lineTo(0, -12)
        p.lineTo(-8, 50); p.lineTo(-30, 50); p.close()
        c.drawPath(p, peinture(couleur))
        rrect(c, -27, -50, 54, 11, 3, "#FFFFFF", 0.25)
        trait(c, 0, -39, 0, -14, "#000000", 2, 0.25)
    c.restore()


def objet(c, nom, cx, cy, taille, a, couleur=BLANC):
    """un article dans une bulle de verre : pantalon, basket, montre, t-shirt"""
    if a <= 0: return
    c.save(); c.translate(cx, cy); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
    with Calque(c, borne(a * 3)):
        lueur(c, 0, 0, taille * 0.9, VC, 0.25)
        verre(c, -taille / 2, -taille / 2, taille, taille, taille * 0.28, 0.08, violet=0.15)
        if nom == "pantalon": pantalon(c, 0, 0, taille * 0.62)
        elif nom == "basket": sneaker(c, 0, 4, taille * 0.72, haut="#F2F2F7", accent=V, semelle="#FFFFFF")
        elif nom == "montre": icone(c, "watch", 0, 0, taille * 0.55, JAUNE, 2.2)
        else: icone(c, "shirt", 0, 0, taille * 0.55, couleur, 2.2)
    c.restore()


def etiquette(c, label, cx, cy, a, couleur=JAUNE, rot=-6, taille=40):
    """étiquette de prix accrochée (forme de ticket)"""
    if a <= 0: return
    tw = largeur(label, taille, "noir"); w, h = tw + 70, taille * 1.7
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
    with Calque(c, borne(a * 3)):
        p = skia.Path(); p.moveTo(-w / 2, 0); p.lineTo(-w / 2 + h / 2, -h / 2); p.lineTo(w / 2, -h / 2); p.lineTo(w / 2, h / 2)
        p.lineTo(-w / 2 + h / 2, h / 2); p.close()
        c.drawPath(p, peinture(couleur))
        disque(c, -w / 2 + h / 2 - 4, 0, 7, "#1A1030")
        texte(c, label, 18, -hauteurLigne(taille) / 2, taille, "#1A1030", "noir", "centre", -0.02)
    c.restore()


def colis(c, cx, cy, w, a, rot=0.0, tag=None, ta=0.0):
    if a <= 0: return
    c.save(); c.translate(cx, cy); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
    carton(c, 0, 0, w, alpha=borne(a * 3), rot=rot)
    c.restore()
    if tag: etiquette(c, tag, cx + w * 0.42, cy - w * 0.38, ta, ROUGE, 8, max(18, w * 0.16))


# ─────────────────────────────────────────── HOOK
def hook(c, t):
    if t > T_AVANT + 0.3: return
    fin = prog(t, T_AVANT - 0.35, 0.35, entree)
    with Calque(c, 1 - fin):
        part = prog(t, T_RESTE, 0.45, entreeSortie)        # tout laisse la place au cadenas de l'astuce
        lettres(c, "TU COMMANDES", 540, 400 - 160 * part, 118, t, -0.7, "ressort", grad=False, couleur=BLANC, decal=0.035, alpha=1 - part)
        lettres(c, "EN CHINE ?", 540, 530 - 160 * part, 132, t, -0.55, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.04, alpha=1 - part)
        # le colis qui arrive de Chine, posé dès l'image 0
        if part < 0.99:
            sx, sy = secousse(t, TW(11), 16)
            cy = 960 + 650 * part ** 2 + 8 * math.sin(t * 2.2)
            lueur(c, 540, cy, 380, V, 0.35)
            carton(c, 540 + sx, cy + sy, 440, alpha=1 - part, rot=-4 + 2 * math.sin(t * 1.3))
            drapeau(c, "CN", 540 - 190 + sx, cy - 150 + sy, 90, 60, 8)
            # « Depuis le premier juillet »
            a = entre(t, TW(4) - 0.1, 0.4, 2.2)
            if a > 0:
                pj = 1 - prog(t, T_ENR - 0.35, 0.25, entree)
                pastille_verre(c, "1er juillet 2026", 540, cy + 250, 42, "calendar", borne(a * 3) * pj, mix(0.4, 1, a), accent="#B8901A", rot=-3)
            # « chaque colis te coûte plus cher » : l'étiquette rouge qui claque
            etiquette(c, "+ €", 540 + 200 + sx, cy - 120 + sy, entre(t, TW(11) - 0.08, 0.35, 2.4) * (1 - part), ROUGE, 10, 64)
            # « deux fois trop »
            if part < 0.6:
                with Calque(c, 1 - part * 1.6):
                    tampon_c(c, "× 2 TROP", 540 + sx, cy + 30 + sy, t, T_X2, ROUGE, -12, 62)
        # « Enregistre » : le signet qui se remplit sous le doigt
        a = entre(t, T_ENR - 0.15, 0.4, 2.2)
        if a > 0 and part < 1:
            t_clic = T_ENR + 0.35
            plein = prog(t, t_clic, 0.3, sortie)
            cx, cy = 850, 1220 + 400 * part
            b = mix(0.3, 1, a) * battement(t, t_clic, 0.2, 0.3)
            c.save(); c.translate(cx, cy); c.scale(b, b)
            lueur(c, 0, 0, 170, JAUNE, 0.25 + 0.35 * plein)
            disque(c, 0, 0, 100, "#1A1030", 0.85); anneau(c, 0, 0, 100, JAUNE if plein > 0.5 else BLANC, 4, 0.8)
            signet(c, 0, 0, 115, plein)
            c.restore()
            if plein > 0:
                pl = prog(t, t_clic, 0.8, sortie)
                texte(c, "+1", cx + 140, cy - 110 - 60 * pl, 52, JAUNE, "noir", "centre", 0, alpha=1 - max(0, pl - 0.6) / 0.4)
            pa = prog(t, t_clic - 0.4, 0.38, sortie)
            if t < t_clic + 0.6:
                curseur(c, mix(1000, cx + 10, pa), mix(1600, cy + 20, pa), 1.3, 1 - prog(t, t_clic + 0.3, 0.3),
                        prog(t, t_clic - 0.05, 0.05) * (1 - prog(t, t_clic + 0.05, 0.1)))
            eclats(c, cx, cy, t, t_clic, 14, 260, [JAUNE, BLANC, VC], graine=3)
            pastille_verre(c, "Enregistre-la", 300, 1220 + 400 * part, 44, "bookmark", borne(a * 3) * (1 - part), mix(0.4, 1, a), accent="#B8901A", rot=-4)


def astuce_cadenas(c, t):
    """« reste jusqu'à la fin » : l'astuce sous cadenas, garée en haut à droite jusqu'à « voilà l'astuce »"""
    if t < T_RESTE or t > T_ASTUCE + 1.2: return
    a = entre(t, T_RESTE, 0.5, 1.6)
    gare = prog(t, T_AVANT - 0.6, 0.5, entreeSortie)
    retour = prog(t, T_ASTUCE - 0.1, 0.45, entreeSortie)
    cx = mix(mix(540, 900, gare), 540, retour); cy = mix(mix(900, 300, gare), 880, retour)
    s = mix(0.4, 1, a) * mix(1, 0.32, gare) * mix(1, 3.1, retour)
    ouvre = prog(t, T_ASTUCE + 0.35, 0.3, sortie)
    if ouvre >= 1 and t > T_ASTUCE + 0.9: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, 1 - prog(t, T_ASTUCE + 0.65, 0.25)):
        pul = 0.5 + 0.5 * math.sin(t * 5)
        lueur(c, 0, 0, 300, JAUNE, 0.3 + 0.12 * pul)
        if gare < 0.5: rayons(c, 0, 0, t, 520, 0.10 * (1 - gare * 2), 12, JAUNE)
        verre(c, -230, -130, 460, 260, 50, 0.12, violet=0.25)
        texte(c, "L'ASTUCE", 0, -hauteurLigne(84) / 2, 84, JAUNE, "noir", "centre", -0.02)
        c.save(); c.translate(200, -120 - 60 * ouvre); c.rotate(-30 * ouvre)
        disque(c, 0, 0, 62, JAUNE); icone(c, "lock-open" if ouvre > 0.3 else "lock", 0, 0, 66, "#1A1030", 2.8)
        c.restore()
    c.restore()
    if a > 0 and gare < 0.3:
        ep = entre(t, TW(32) - 0.1, 0.4, 2.2)
        if ep > 0:
            with Calque(c, 1 - gare * 3.3):
                pastille_verre(c, "Pour payer moins", 540, 1130, 44, "trending-down", borne(ep * 3), mix(0.4, 1, ep), accent=VERT)
    eclats(c, cx, cy, t, T_ASTUCE + 0.35, 16, 380, [JAUNE, BLANC, VC], graine=7)


# ─────────────────────────────────────────── AVANT / C'EST FINI
def avant(c, t):
    g = Groupe(c, t, T_AVANT - 0.2, T_REGLE, ent="bas", sor="gauche")
    if not g.visible: return
    with g:
        entete(c, t, None, "AVANT JUILLET", T_AVANT - 0.05)
        a = entre(t, TW(40) - 0.1, 0.45, 1.8)
        if a > 0:
            carte(c, 540, 860, 820, 300, 40, violet=0.15, alpha=borne(a * 3), s=mix(0.5, 1, a))
            with Calque(c, borne(a * 3)):
                carton(c, 260, 860, 210)
                drapeau_ue(c, 820, 740, 84, 56, 8)
                texte(c, "Colis de moins de", 410, 760, 34, A["gris"], "gras", track=-0.01)
                b = entre(t, TW(45) - 0.1, 0.35, 2.2)
                if b > 0:
                    w3 = rouleau(c, 1, 410, 800, 110, t, TW(45) - 0.1, TW(46), BLANC)
                    texte(c, "50 €", 410 + w3 - 6, 800, 110, BLANC, "noir", track=-0.03, alpha=borne(b * 3))
        d = entre(t, TW(49) - 0.1, 0.4, 2.2)
        if d > 0:
            pastille_verre(c, "0 € de douane", 540, 1110, 46, "check", borne(d * 3), mix(0.4, 1, d), accent=VERT)
            bb = prog(t, T_FINI, 0.22, sortie)
            if bb > 0: trait(c, 300, 1135, 300 + 480 * bb, 1085, ROUGE, 12)
        tampon_c(c, "C'EST FINI", 540, 990, t, T_FINI + 0.1, ROUGE, -8, 76)


# ─────────────────────────────────────────── 3 € PAR CATÉGORIE
def regle(c, t):
    g = Groupe(c, t, T_REGLE - 0.12, T_PARTAGE, ent="droite", sor="zoom")
    if not g.visible: return
    with g:
        entete(c, t, None, "3 € PAR CATÉGORIE", T_REGLE, [JAUNE, "#FFE98A"])
        # le gros 3 € qui roule, puis laisse la place aux exemples
        big = entre(t, TW(57) - 0.1, 0.45, 1.8) * (1 - prog(t, TW(62) - 0.25, 0.3, entree))
        if big > 0:
            c.save(); c.translate(540, 900); c.scale(mix(0.5, 1, big), mix(0.5, 1, big))
            with Calque(c, borne(big * 3)):
                lueur(c, 0, 0, 340, JAUNE, 0.3)
                w3 = rouleau(c, 3, -150, -130, 280, t, TW(57) - 0.1, TW(58) + 0.05, JAUNE)
                texte(c, "€", -150 + w3 + 10, -130, 280, JAUNE, "noir", track=-0.03)
                texte(c, "par catégorie d'article", 0, 190, 40, BLANC, "gras", "centre", -0.01)
            c.restore()
        # exemple 1 : deux pantalons = 3 € une seule fois
        ex1 = entre(t, TW(62) - 0.15, 0.45, 1.8)
        ex1_sort = prog(t, TW(69) - 0.2, 0.3, entree)
        if ex1 > 0 and ex1_sort < 1:
            with Calque(c, 1 - ex1_sort):
                objet(c, "pantalon", 380, 860, 220, ex1)
                objet(c, "pantalon", 640, 860, 220, entre(t, TW(63) - 0.05, 0.45, 1.8))
                u = prog(t, TW(64) - 0.1, 0.3, sortie)
                if u > 0:      # l'accolade qui réunit les deux
                    trait(c, 270, 1000, 270 + 480 * u, 1000, JAUNE, 6)
                    trait(c, 270, 990, 270, 1010, JAUNE, 6, borne(u * 3)); trait(c, 750, 990, 750, 1010, JAUNE, 6, borne(u * 3) if u > 0.95 else 0)
                etiquette(c, "3 €", 510, 1080, entre(t, TW(64) - 0.05, 0.35, 2.4), JAUNE, -4, 52)
                ok = entre(t, TW(66) - 0.05, 0.4, 2.2)
                if ok > 0: pastille_verre(c, "Une seule fois", 840, 1200, 36, "check", borne(ok * 3), mix(0.4, 1, ok), accent=VERT, rot=4)
        # exemple 2 : pantalon + baskets + montre = 3 catégories = 9 €
        if t > TW(69) - 0.3:
            xs = [230, 540, 850]
            for k, (nom, t0, tt) in enumerate([("pantalon", TW(69), TW(70)), ("basket", TW(71), TW(74)), ("montre", TW(76), TW(77))]):
                objet(c, nom, xs[k], 830, 230, entre(t, t0 - 0.15, 0.45, 1.8))
                etiquette(c, "3 €", xs[k] + 20, 1000, entre(t, tt + 0.05, 0.35, 2.4), JAUNE, -5, 44)
            cat = entre(t, TW(78) - 0.1, 0.4, 2.2)
            if cat > 0: pastille_verre(c, "3 catégories", 540, 1140, 36, "layers", borne(cat * 3), mix(0.4, 1, cat), accent=V)
            tot = entre(t, TW(80) - 0.12, 0.45, 2.0)
            if tot > 0:
                c.save(); c.translate(540, 1280); c.scale(mix(0.4, 1, tot) * battement(t, TW(81), 0.08, 0.3), mix(0.4, 1, tot) * battement(t, TW(81), 0.08, 0.3))
                rrect(c, -170, -62, 340, 124, 62, ROUGE, borne(tot * 3), (10, 30, 0.4))
                texte(c, "= 9 €", 0, -hauteurLigne(72) / 2, 72, BLANC, "noir", "centre", -0.02, borne(tot * 3))
                c.restore()


# ─────────────────────────────────────────── PARTAGE
def partage(c, t):
    g = Groupe(c, t, T_PARTAGE - 0.12, T_NOV, ent="zoom", sor="zoom")
    if not g.visible: return
    with g:
        lettres(c, "ENVOIE-LA", 540, 420, 120, t, T_PARTAGE - 0.05, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.035)
        a = entre(t, T_PARTAGE, 0.45, 1.8)
        if a > 0:
            b = mix(0.4, 1, a) * battement(t, T_PARTAGE + 0.5, 0.1, 0.3)
            c.save(); c.translate(540, 740); c.scale(b, b)
            lueur(c, 0, 0, 200, JAUNE, 0.35); disque(c, 0, 0, 105, JAUNE)
            icone(c, "share-2", -4, 0, 115, "#1A1030", 2.6)
            c.restore()
        # le pote, enseveli sous les petits colis
        p = entre(t, TW(86) - 0.1, 0.4, 2.2)
        if p > 0:
            c.save(); c.translate(540, 1120); c.scale(p, p)
            disque(c, 0, 0, 86, "#2A2040"); anneau(c, 0, 0, 86, VC, 4)
            icone(c, "user-round", 0, -6, 90, BLANC, 2.0)
            texte(c, "Ton pote", 0, 104, 34, BLANC, "gras", "centre", -0.01)
            c.restore()
        for k in range(9):
            t0 = TW(91) - 0.1 + 0.07 * k
            u = prog(t, t0, 0.35, lambda v: rebond(v, 1.8))
            if u <= 0: continue
            ang = -math.pi / 2 + (k - 4) * 0.36
            r = 230 + 30 * (k % 2)
            x, y = 540 + r * math.cos(ang), 1110 + r * math.sin(ang) * 0.9 + 80
            carton(c, x, mix(y - 300, y, u), 92, alpha=borne(u * 3), rot=(k - 4) * 6)


# ─────────────────────────────────────────── NOVEMBRE : la redevance par colis
def novembre(c, t):
    g = Groupe(c, t, T_NOV - 0.12, T_ASTUCE + 0.1, ent="bas", sor="recul")
    if not g.visible: return
    with g:
        entete(c, t, None, "ET EN NOVEMBRE…", T_NOV, CLAIR)
        a = entre(t, TW(100) - 0.15, 0.45, 1.8)
        dix = prog(t, TW(111) - 0.2, 0.35, entreeSortie)
        if a > 0:
            cy = mix(840, 700, dix)
            carte(c, 540, cy, 820, 230, 40, violet=0.2, alpha=borne(a * 3), s=mix(0.5, 1, a) * mix(1, 0.8, dix))
            with Calque(c, borne(a * 3)):
                c.save(); c.translate(540, cy); c.scale(mix(1, 0.8, dix), mix(1, 0.8, dix)); c.translate(-540, -cy)
                rrect(c, 170, cy - 80, 150, 160, 22, BLANC)
                rrect(c, 170, cy - 80, 150, 46, 22, ROUGE); c.drawRect(skia.Rect.MakeXYWH(170, cy - 56, 150, 22), peinture(ROUGE))
                texte(c, "NOV.", 245, cy - 78, 30, BLANC, "noir", "centre", 0.04)
                texte(c, "1", 245, cy - 30, 84, "#1A1030", "noir", "centre", -0.02)
                texte(c, "Redevance", 360, cy - 70, 54, BLANC, "noir", track=-0.02)
                texte(c, "de gestion", 360, cy - 8, 54, VC, "noir", track=-0.02)
                c.restore()
        pc = entre(t, TW(108) - 0.1, 0.4, 2.2)
        if pc > 0 and dix < 0.5:
            with Calque(c, 1 - dix * 2):
                pastille_verre(c, "+ pour chaque colis", 540, 1060, 44, "package", borne(pc * 3), mix(0.4, 1, pc), accent=ROUGE)
        # dix petits colis, dix fois les frais
        if t > TW(111) - 0.2:
            for k in range(10):
                col, lig = k % 5, k // 5
                x, y = 180 + col * 180, 940 + lig * 190
                t0 = TW(112) + 0.06 * k
                colis(c, x, y, 120, entre(t, t0 - 0.1, 0.35, 2.2), rot=(k % 3 - 1) * 5, tag="+", ta=entre(t, TW(117) + 0.04 * k, 0.3, 2.4))
            tampon_c(c, "× 10 LES FRAIS", 540, 1290, t, TW(118) + 0.1, ROUGE, -5, 54)


# ─────────────────────────────────────────── L'ASTUCE : 3 étapes
RAIL_X = [810, 900, 990]
RAIL_Y = 300


def rail(c, t):
    if t < T_ASTUCE + 0.6: return
    a = entre(t, T_ASTUCE + 0.6, 0.5, 1.4)
    k_act = max([k for k, t0 in enumerate(ETAPES) if t >= t0 - 0.12] or [-1])
    with Calque(c, borne(a * 3) * (1 - prog(t, T_LOGO_CB - 0.1, 0.3))):
        trait(c, RAIL_X[0], RAIL_Y, RAIL_X[-1], RAIL_Y, BLANC, 4, 0.18)
        if k_act > 0:
            u = prog(t, ETAPES[k_act] - 0.12, 0.35, sortie)
            trait(c, RAIL_X[0], RAIL_Y, mix(RAIL_X[k_act - 1], RAIL_X[k_act], u), RAIL_Y, JAUNE, 5)
        for k, x in enumerate(RAIL_X):
            ak = entre(t, T_ASTUCE + 0.6 + 0.05 * k, 0.4, 2.2)
            if ak <= 0: continue
            c.save(); c.translate(x, RAIL_Y - 30 * (1 - ak))
            actif, fait = k == k_act, k < k_act
            s = 1.0 + 0.28 * (prog(t, ETAPES[k] - 0.12, 0.3, lambda v: rebond(v, 2)) if actif else 0)
            c.scale(s, s)
            if actif:
                lueur(c, 0, 0, 70, JAUNE, 0.45); disque(c, 0, 0, 30, JAUNE)
                texte(c, str(k + 1), 0, -hauteurLigne(32) / 2, 32, "#1A1030", "noir", "centre", 0)
            elif fait:
                disque(c, 0, 0, 26, V); icone(c, "check", 0, 0, 30, BLANC, 3)
            else:
                disque(c, 0, 0, 24, BLANC, 0.08); anneau(c, 0, 0, 24, BLANC, 2, 0.35)
                texte(c, str(k + 1), 0, -hauteurLigne(26) / 2, 26, BLANC, "noir", "centre", 0, alpha=0.6)
            c.restore()


def titre_astuce(c, t):
    if not (T_ASTUCE - 0.1 <= t < ETAPES[0] + 0.2): return
    with Calque(c, 1 - prog(t, ETAPES[0] - 0.2, 0.3, entree)):
        lettres(c, "VOILÀ L'ASTUCE", 540, 1080, 92, t, T_ASTUCE + 0.3, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.03)


def etape1(c, t):
    g = Groupe(c, t, ETAPES[0] - 0.3, ETAPES[1], ent="grand", sor="gauche")
    if not g.visible: return
    with g:
        entete(c, t, 1, "REGROUPE", ETAPES[0])
        st = entre(t, TW(127) - 0.1, 0.4, 2.2)
        if st > 0: pastille_verre(c, "par catégorie", 420, 640, 38, "layers", borne(st * 3), mix(0.4, 1, st), accent=V)
        # à gauche : le colis mélangé (barré) ; à droite : 20 paires dans le même envoi
        m = entre(t, TW(137) - 0.15, 0.45, 1.8)
        if m > 0:
            carte(c, 290, 960, 400, 420, 40, alpha=borne(m * 3), s=mix(0.5, 1, m))
            with Calque(c, borne(m * 3)):
                carton(c, 290, 1030, 230)
                for (dx, dy, rot, nom) in [(-70, -150, -18, "pantalon"), (0, -175, 4, "basket"), (75, -145, 16, "montre")]:
                    c.save(); c.translate(290 + dx, 1030 + dy + 10 * math.sin(t * 3 + dx)); c.rotate(rot)
                    if nom == "pantalon": pantalon(c, 0, 0, 110, "#7C8CFF")
                    elif nom == "basket": sneaker(c, 0, 0, 120, haut="#F2F2F7", accent=V)
                    else: icone(c, "watch", 0, 0, 80, JAUNE, 2.4)
                    c.restore()
                texte(c, "Mélangé", 290, 1170, 36, BLANC, "gras", "centre", -0.01)
            interdit(c, 290, 990, 150, prog(t, TW(141) - 0.05, 0.25, sortie))
        v = entre(t, TW(124) - 0.15, 0.45, 1.8)
        if v > 0:
            cen = 1 - m if m > 0 else 1.0
            cx = mix(780, 540, cen)
            carte(c, cx, 960, 420, 420, 40, violet=0.25, alpha=borne(v * 3), s=mix(0.5, 1, v))
            with Calque(c, borne(v * 3)):
                carton(c, cx, 1040, 250)
                for k in range(6):
                    u = entre(t, TW(130) + 0.06 * k, 0.35, 2.0)
                    if u <= 0: continue
                    sneaker(c, cx - 80 + (k % 3) * 80, 860 + (k // 3) * 56 + 40 * (1 - u), 110, haut="#F2F2F7", accent=V, alpha=borne(u * 3))
                c.save(); c.translate(cx + 130, 820); c.scale(entre(t, TW(130) + 0.3, 0.35, 2.4), entre(t, TW(130) + 0.3, 0.35, 2.4))
                disque(c, 0, 0, 62, JAUNE); texte(c, "× 20", 0, -hauteurLigne(40) / 2, 40, "#1A1030", "noir", "centre", -0.02)
                c.restore()
                texte(c, "Même envoi", cx, 1170, 36, BLANC, "gras", "centre", -0.01)
            ok = entre(t, TW(134) - 0.05, 0.35, 2.4)
            if ok > 0: disque(c, cx + 170, 1150, 40 * ok, VERT); icone(c, "check", cx + 170, 1150, 46 * ok, BLANC, 3.2)


def etape2(c, t):
    g = Groupe(c, t, ETAPES[1] - 0.12, ETAPES[2], ent="droite", sor="zoom")
    if not g.visible: return
    with g:
        entete(c, t, 2, "PAS À L'UNITÉ", ETAPES[1])
        # un calendrier : un petit colis tous les trois jours
        a = entre(t, TW(148) - 0.15, 0.45, 1.8)
        barre = prog(t, TW(147) + 0.6, 0.01) * 0 + prog(t, TW(155) - 0.05, 0.25, sortie)
        if a > 0:
            carte(c, 540, 900, 900, 440, 40, violet=0.12, alpha=borne(a * 3), s=mix(0.5, 1, a))
            with Calque(c, borne(a * 3)):
                for j, jr in enumerate("LMMJVSD"):
                    texte(c, jr, 165 + j * 125, 715, 30, A["gris"], "gras", "centre", 0)
                for k in range(14):
                    x, y = 165 + (k % 7) * 125, 800 + (k // 7) * 150
                    rrect(c, x - 52, y - 52, 104, 104, 18, BLANC, 0.06)
                    if k % 3 == 0:
                        u = entre(t, TW(149) + 0.05 * k, 0.3, 2.2)
                        if u > 0: carton(c, x, y, 80 * u, alpha=borne(u * 3) * (1 - 0.5 * barre), rot=(k % 2) * 8 - 4)
        if barre > 0:
            interdit(c, 540, 900, 210, barre)
        u1 = entre(t, TW(152) - 0.1, 0.4, 2.2)
        if u1 > 0: pastille_verre(c, "Tous les 3 jours", 540, 1210, 42, "calendar", borne(u1 * 3), mix(0.4, 1, u1), accent=ROUGE)


def etape3(c, t):
    if t < ETAPES[2] - 0.15: return
    g = Groupe(c, t, ETAPES[2] - 0.15, T_COM + 0.1, ent="bas", sor="recul")
    if not g.visible: return
    with g:
        entete(c, t, 3, "UN TRANSITAIRE", ETAPES[2])
        # le transitaire : la vraie vidéo des cartons à Guangzhou dans une carte
        a = entre(t, TW(160) - 0.1, 0.5, 1.6)
        if a > 0:
            c.save(); c.translate(540, 900); c.scale(mix(0.5, 1, a), mix(0.5, 1, a)); c.translate(-540, -900)
            with Calque(c, borne(a * 3)):
                lueur(c, 540, 900, 300, V, 0.4)
                verre(c, 380, 700, 320, 400, 40, 0.1, violet=0.2)
                video(c, "videos/guangzhou/guangzhou-cartons-baskets-gros", 396, 716, 288, 300, t - TW(160), 1.6, rayon=28)
                icone(c, "warehouse", 470, 1060, 44, JAUNE, 2.2)
                texte(c, "Transitaire", 500, 1042, 34, BLANC, "gras", track=-0.01)
            c.restore()
        # les colis de tous tes fournisseurs qui convergent
        for k, (y, t0) in enumerate([(720, TW(166)), (900, TW(167)), (1080, TW(168))]):
            n = entre(t, t0 - 0.1, 0.4, 2.2)
            if n <= 0: continue
            c.save(); c.translate(130, y); c.scale(n, n)
            disque(c, 0, 0, 62, "#2A2040"); anneau(c, 0, 0, 62, VC, 3); icone(c, "store", 0, 0, 58, BLANC, 2.0)
            c.restore()
            u = prog(t, t0 + 0.15, 0.55, entreeSortie)
            if 0 < u < 1:
                carton(c, mix(200, 400, u), mix(y, 900, u), 70, rot=20 * u)
            trait(c, 200, y, 370, mix(y, 900, 0.85), BLANC, 3, 0.25 * borne(n * 3), pointille=[8, 8])
        if t > TW(161) - 0.1:
            texte(c, "Fournisseurs", 130, 1170, 28, A["gris"], "gras", "centre", 0, borne(entre(t, TW(168), 0.4) * 3))
        # un seul envoi, vers chez toi
        e = entre(t, TW(172) - 0.1, 0.45, 1.8)
        if e > 0:
            u = prog(t, TW(172) - 0.1, 0.6, entreeSortie)
            carton(c, mix(700, 900, u), 900, 170, alpha=borne(e * 3), rot=-6 * (1 - u))
            drapeau(c, "FR", 900 - 40, 1010, 80, 54, 8)
            pastille_verre(c, "1 seul envoi", 900, 760, 34, "package", borne(e * 3), mix(0.4, 1, e), accent=VERT, rot=5)
            trait(c, 700, 900, mix(700, 810, u), 900, JAUNE, 5)


# ─────────────────────────────────────────── commentaire puis ChinaBook par DROP&YOU
def fin(c, t):
    if t < T_COM - 0.05: return
    logo_t = prog(t, T_LOGO_CB - 0.1, 0.4, entreeSortie)
    cm = entre(t, T_COM, 0.45, 1.8)
    if cm > 0 and logo_t < 1:
        with Calque(c, 1 - logo_t):
            lettres(c, "DIS-MOI", 540, 560, 120, t, T_COM, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.035)
            c.save(); c.translate(540, 900); c.scale(mix(0.5, 1, cm), mix(0.5, 1, cm))
            with Calque(c, borne(cm * 3)):
                verre(c, -420, -70, 840, 140, 70, 0.12)
                icone(c, "message-circle", -355, 0, 54, JAUNE, 2.4)
                rep = ["Combien de colis par mois ?", "4", "12", "30 !"]
                k = min(len(rep) - 1, int(max(0, t - T_COM - 0.6) / 0.6))
                mot = rep[k]
                n = len(mot) if k == 0 else int(borne((t - T_COM - 0.6 - 0.6 * k) / 0.25) * len(mot) + 0.999)
                tl = 40 if k == 0 else 54
                texte(c, mot[:n], -300, -hauteurLigne(tl, "gras") / 2, tl, A["gris"] if k == 0 else BLANC, "gras", track=-0.01)
            c.restore()
    if logo_t > 0:
        ul = entre(t, T_LOGO_CB + 0.1, 0.5, 1.5)
        lueur(c, 540, 860, 600 * logo_t, "#6E48F0", 0.45)
        rayons(c, 540, 860, t, 900, 0.10 * logo_t, 14, "#9B83FF")
        # ce que contient le ChinaBook : fournisseurs + transitaire
        for k, (lab, ic, x, t0) in enumerate([("Fournisseurs", "store", 330, TW(186)), ("Transitaire", "warehouse", 750, TW(189))]):
            p = entre(t, t0 - 0.1, 0.4, 2.2)
            if p > 0: pastille_verre(c, lab, x, 600, 38, ic, borne(p * 3), mix(0.4, 1, p), accent=V)
        iw, ih = taille_img("logo-chinabook-blanc"); lw = 820 * mix(0.6, 1, ul)
        image(c, "logo-chinabook-blanc", 540 - lw / 2, 830 - lw * ih / iw / 2, lw, borne(ul * 3))
        up = entre(t, TW(199) - 0.1, 0.45, 1.8)
        if up > 0:
            texte(c, "par", 540, 990, 36, A["gris"], "gras", "centre", 0, borne(up * 3))
            iw, ih = taille_img("logo-dy-blanc"); lw2 = 440 * mix(0.6, 1, up)
            image(c, "logo-dy-blanc", 540 - lw2 / 2, 1060, lw2, borne(up * 3))


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(0.05, "pop", -11)
son(TW(4) - 0.1, "pop", -9); son(TW(11) - 0.08, "impact", -6); son(TW(11) - 0.05, "ching", -10)
son(T_ENR - 0.15, "pop", -9); son(T_ENR + 0.35, "clic", -5); son(T_ENR + 0.38, "ching", -8); son(T_ENR + 0.4, "check", -9)
son(T_X2 - 0.07, "tampon", -6)
son(T_RESTE, "impact_doux", -6); son(T_RESTE + 0.05, "montee", -12); son(TW(32) - 0.1, "pop", -10)
son(T_AVANT - 0.6, "whoosh_long", -9); son(T_AVANT - 0.2, "whoosh_bas", -8)
son(TW(40) - 0.1, "verre", -9)
for k in range(8): son(TW(45) - 0.1 + 0.04 * k, "tick", -15)
son(TW(49) - 0.1, "check", -10); son(T_FINI, "croc", -8); son(T_FINI + 0.05, "tampon", -5)
son(T_REGLE - 0.15, "whoosh", -7); son(T_REGLE, "impact_doux", -8)
for k in range(10): son(TW(57) - 0.1 + 0.035 * k, "tick", -15)
son(TW(58) + 0.05, "ching", -8)
son(TW(62) - 0.15, "pop", -10); son(TW(63) - 0.05, "pop", -10); son(TW(64) - 0.05, "ching", -9); son(TW(66) - 0.05, "check", -10)
son(TW(69) - 0.2, "whoosh_court", -10)
for t0 in [TW(69), TW(71), TW(76)]: son(t0 - 0.15, "pop", -10)
for t0 in [TW(70), TW(74), TW(77)]: son(t0 + 0.05, "blip", -11)
son(TW(78) - 0.1, "pop", -11); son(TW(80) - 0.12, "impact", -6); son(TW(80), "ching", -9)
son(T_PARTAGE - 0.1, "whoosh_bas", -7); son(T_PARTAGE + 0.5, "impact_doux", -9); son(TW(86) - 0.1, "pop", -10)
for k in range(9): son(TW(91) - 0.1 + 0.07 * k, "pop", -15)
son(T_NOV - 0.15, "whoosh", -7); son(TW(100) - 0.15, "verre", -9); son(TW(108) - 0.1, "pop", -9)
son(TW(111) - 0.2, "whoosh_court", -10)
for k in range(10): son(TW(112) + 0.06 * k - 0.1, "pop", -16)
for k in range(10): son(TW(117) + 0.04 * k, "tick", -16)
son(TW(118) + 0.03, "tampon", -5)
son(T_ASTUCE - 0.1, "whoosh_long", -9); son(T_ASTUCE + 0.35, "clic", -5); son(T_ASTUCE + 0.38, "impact", -5); son(T_ASTUCE + 0.4, "ching", -8)
son(T_ASTUCE + 0.6, "whoosh", -10)
for k in range(3): son(T_ASTUCE + 0.6 + 0.05 * k, "tick", -15)
for k, t0 in enumerate(ETAPES):
    son(t0 - 0.15, "whoosh" if k % 2 == 0 else "whoosh_bas", -7); son(t0 - 0.05, "impact_doux", -8); son(t0, "pop", -10)
son(TW(127) - 0.1, "pop", -10); son(TW(124) - 0.15, "verre", -9)
for k in range(6): son(TW(130) + 0.06 * k, "pop", -15)
son(TW(130) + 0.3, "ching", -9); son(TW(134) - 0.05, "check", -9); son(TW(137) - 0.15, "verre", -10); son(TW(141) - 0.05, "impact", -6)
son(TW(148) - 0.15, "verre", -9)
for k in range(0, 14, 3): son(TW(149) + 0.05 * k, "pop", -14)
son(TW(152) - 0.1, "pop", -10); son(TW(155) - 0.05, "impact", -6)
son(TW(160) - 0.1, "verre", -9)
for t0 in [TW(166), TW(167), TW(168)]: son(t0 - 0.1, "pop", -11); son(t0 + 0.15, "whoosh_court", -13)
son(TW(172) - 0.1, "whoosh", -9); son(TW(172) + 0.4, "ching", -9)
son(T_COM, "message", -9)
for k in range(1, 4):
    for j in range(3): son(T_COM + 0.6 + 0.6 * k + 0.07 * j, "frappe", -17)
son(T_LOGO_CB - 0.1, "montee", -11); son(T_LOGO_CB + 0.1, "impact", -5); son(T_LOGO_CB + 0.12, "verre", -9)
son(TW(186) - 0.1, "pop", -10); son(TW(189) - 0.1, "pop", -10); son(TW(199) - 0.1, "pop", -9)

for a, b in [(0.0, 0.25), (T_AVANT - 0.6, T_AVANT + 0.2), (T_REGLE - 0.15, T_REGLE + 0.3), (T_PARTAGE - 0.2, T_PARTAGE + 0.3),
             (T_NOV - 0.2, T_NOV + 0.3), (T_ASTUCE - 0.1, T_ASTUCE + 0.5), (T_LOGO_CB - 0.1, T_LOGO_CB + 0.4)] + \
            [(t0 - 0.3, t0 + 0.3) for t0 in ETAPES]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(11) - 0.05, ROUGE, 0.10), (T_ENR + 0.38, JAUNE, 0.10), (T_FINI + 0.05, ROUGE, 0.12),
                    (T_ASTUCE + 0.38, JAUNE, 0.14), (T_LOGO_CB + 0.1, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, T_ASTUCE + 0.35, 1, 0.6) + battement(t, T_LOGO_CB + 0.1, 1, 0.6) - 2)
    entete_marque(c, t)
    hook(c, t)
    avant(c, t); regle(c, t); partage(c, t); novembre(c, t)
    titre_astuce(c, t); etape1(c, t); etape2(c, t); etape3(c, t)
    astuce_cadenas(c, t)
    fin(c, t)
    rail(c, t)
    K.dessine_eclairs(c, t)
    if not (T_COM - 0.05 < t < T_LOGO_CB) and t < T_SANS_SOUS: SOUS.dessine(c, t, BLANC)
