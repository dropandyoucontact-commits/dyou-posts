"""CB-M10 « Tu pars en Chine ? » — organique ChinaBook / DROP&YOU (14/10/2026), 7 astuces pour dépenser moins.

Idée reprise d'un carrousel TikTok (WORLDOUT, « Tu pars seul en Chine ? ») réécrit à notre façon, faits vérifiés le
14/10 (pass métro 18 ¥ Shanghai / 20 ¥ Canton, musées nationaux gratuits sur réservation avec passeport, DiDi + Alipay,
Uber absent depuis 2016, Airbnb sans logements en Chine depuis 2022, Dianping/Meituan payables via Alipay).
Règles du 14/10 : « enregistre » dans le hook, partage ciblé au milieu, boucle ouverte (le n° 7 sous cadenas jusqu'à la
fin), fond sombre (plus de blanc), logo DROP&YOU présent, ChinaBook en violet à la fin « par DROP&YOU », son fort.
"""
import math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence
from studio import (lettres, Groupe, eclats, etoile4, rayons, curseur, clic, losange, rouleau, entre, sort,
                    flou_calque, texte_grad, pgrad, GRAD_VIF, SousTitresEncre)

DUREE = 50.4
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

JAUNE, ROUGE, VERT, BLANC = "#FFD43B", "#FF4D5E", "#2BD67B", "#FFFFFF"
V, VC = A["violet"], A["violetClair"]
CLAIR = [BLANC, "#E6DCFF"]

SOUS = SousTitresEncre(K, fusions={(52, 53): "24 h.", (56, 57): "3 €", (136, 137, 138): "Trip.com.", (173, 174): "ChinaBook,",
                                  (176, 177, 178): "DROP&YOU."}, y=1410, larg=900, taille=54, fam="gras", max_mots=5)

# ─────────────────────────────────────────── temps des parties
T_RAIL = TW(14) - 0.1                       # « Et reste jusqu'au numéro sept »
ETAPES = [TW(27), TW(48), TW(69), TW(82), TW(110), TW(131), TW(146)]     # 1 … 7
T_PARTAGE = TW(101)                         # « Envoie cette vidéo… »
FINS = [TW(48), TW(69), TW(82), TW(101), TW(131), TW(146), DUREE + 1]
T_LOGO_CB = TW(167) - 0.1                   # « Les contacts validés… »
T_COM = TW(179) - 0.1                       # « Dis-moi en commentaire »


def etape_active(t):
    k = -1
    for i, t0 in enumerate(ETAPES):
        if t >= t0 - 0.12: k = i
    return k


# ─────────────────────────────────────────── éléments persistants : logo DROP&YOU + rail des 7 astuces
RAIL_X = [392 + k * 90 for k in range(7)]
RAIL_Y = 300


def entete_marque(c, t):
    a = prog(t, 0.0, 0.01) if t > 0 else 1.0
    iw, ih = taille_img("logo-dy-blanc"); lw = 230
    image(c, "logo-dy-blanc", 70, RAIL_Y - lw * ih / iw / 2, lw, 0.95 * a)


def rail(c, t):
    if t < T_RAIL: return
    a = entre(t, T_RAIL, 0.5, 1.4)
    k_act = etape_active(t)
    with Calque(c, borne(a * 3)):
        trait(c, RAIL_X[0], RAIL_Y, RAIL_X[-1], RAIL_Y, "#FFFFFF", 4, 0.18)
        if k_act > 0:
            u = prog(t, ETAPES[k_act] - 0.12, 0.35, sortie)
            xb = mix(RAIL_X[k_act - 1], RAIL_X[k_act], u) if k_act < 7 else RAIL_X[-1]
            trait(c, RAIL_X[0], RAIL_Y, xb, RAIL_Y, JAUNE, 5)
        for k, x in enumerate(RAIL_X):
            ak = entre(t, T_RAIL + 0.05 * k, 0.4, 2.2)
            if ak <= 0: continue
            c.save(); c.translate(x, RAIL_Y - 30 * (1 - ak))
            fait, actif = k < k_act, k == k_act
            s = 1.0 + 0.28 * (prog(t, ETAPES[k] - 0.12, 0.3, lambda v: rebond(v, 2)) if actif else 0)
            c.scale(s, s)
            if k == 6 and t < ETAPES[6] - 0.12:
                pul = 0.5 + 0.5 * math.sin(t * 5)
                lueur(c, 0, 0, 70, JAUNE, 0.35 + 0.25 * pul)
                disque(c, 0, 0, 30, "#2A2040"); anneau(c, 0, 0, 30, JAUNE, 3)
                icone(c, "lock", 0, 0, 30, JAUNE, 2.6)
            elif actif:
                lueur(c, 0, 0, 70, JAUNE, 0.45); disque(c, 0, 0, 30, JAUNE)
                texte(c, str(k + 1), 0, -hauteurLigne(32) / 2, 32, "#1A1030", "noir", "centre", 0)
            elif fait:
                disque(c, 0, 0, 26, V); icone(c, "check", 0, 0, 30, BLANC, 3)
            else:
                disque(c, 0, 0, 24, "#FFFFFF", 0.08); anneau(c, 0, 0, 24, "#FFFFFF", 2, 0.35)
                texte(c, str(k + 1), 0, -hauteurLigne(26) / 2, 26, "#FFFFFF", "noir", "centre", 0, alpha=0.6)
            c.restore()
    # le cadenas du 7 qui saute à l'ouverture
    eclats(c, RAIL_X[6], RAIL_Y, t, ETAPES[6] - 0.05, 12, 200, [JAUNE, BLANC, VC], graine=9)


def entete(c, t, n, titre, t0, couleur_titre=None):
    """grand numéro jaune + titre de l'astuce"""
    a = entre(t, t0 - 0.12, 0.45, 2.0)
    if a > 0 and n:
        c.save(); c.translate(150, 500); c.rotate(-8 * (1 - a)); c.scale(mix(2.4, 1, a), mix(2.4, 1, a))
        lueur(c, 0, 0, 120, JAUNE, 0.35)
        disque(c, 0, 0, 62, JAUNE)
        texte(c, str(n), 0, -hauteurLigne(78) / 2, 78, "#1A1030", "noir", "centre", -0.02)
        c.restore()
    taille = ajuste(titre, 760 if n else 900, 96, "noir", -0.03)
    x = 240 if n else 540
    lettres(c, titre, x, 500 - taille * 0.62, taille, t, t0 - 0.05, "masque", decal=0.025, duree=0.4,
            align="gauche" if n else "centre", grad=True, cols=couleur_titre or CLAIR)


def carte(c, cx, cy, w, h, r=40, violet=0.0, alpha=1.0, s=1.0, rot=0.0, ry=0.0):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        verre(c, -w / 2, -h / 2, w, h, r, 0.08, violet=violet)
    c.restore()


def croix(c, cx, cy, r, u, couleur=ROUGE):
    """trait rouge qui barre, puis rond « interdit »"""
    if u <= 0: return
    trait(c, cx - r, cy + r * 0.6, cx - r + 2 * r * min(1, u * 1.4), cy + r * 0.6 - 1.2 * r * min(1, u * 1.4), couleur, 14)


def interdit(c, cx, cy, r, u):
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.scale(mix(1.6, 1, u), mix(1.6, 1, u))
    with Calque(c, borne(u * 3)):
        anneau(c, 0, 0, r, ROUGE, 14)
        trait(c, -r * 0.7, -r * 0.7, r * 0.7, r * 0.7, ROUGE, 14)
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


def tuile_logo(c, nom, cx, cy, taille, fond_, glyphe="#FFFFFF", alpha=1.0, s=1.0, texte_=None):
    if alpha <= 0.01 or s <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        lueur(c, 0, 0, taille * 0.95, fond_, 0.35)
        rrect(c, -taille / 2, -taille / 2, taille, taille, taille * 0.24, fond_, 1.0, (12, 30, 0.35))
        if texte_:
            tl = ajuste(texte_, taille * 0.8, taille * 0.34, "noir")
            texte(c, texte_, 0, -hauteurLigne(tl) / 2, tl, glyphe, "noir", "centre", -0.02)
        else:
            logo_glyphe(c, nom, 0, 0, taille * 0.58, glyphe)
    c.restore()


# ─────────────────────────────────────────── HOOK : « Tu pars en Chine ? Enregistre cette vidéo… »
def carte_embarquement(c, cx, cy, t, alpha=1.0, s=1.0):
    w, h = 820, 400
    c.save(); c.translate(cx, cy); c.scale(s, s); c.rotate(-3 + 1.5 * math.sin(t * 1.4))
    with Calque(c, alpha):
        verre(c, -w / 2, -h / 2, w, h, 36, 0.10, violet=0.08)
        texte(c, "CARTE D'EMBARQUEMENT", -w / 2 + 40, -h / 2 + 32, 24, VC, "titre", track=0.12)
        drapeau(c, "FR", -w / 2 + 40, -h / 2 + 90, 64, 44, 6); drapeau(c, "CN", w / 2 - 104, -h / 2 + 90, 64, 44, 6)
        texte(c, "PARIS", -w / 2 + 40, -h / 2 + 150, 64, BLANC, "noir", track=-0.02)
        texte(c, "SHANGHAI", w / 2 - 40, -h / 2 + 150, 64, BLANC, "noir", "droite", -0.02)
        # trajet en pointillés et l'avion qui avance
        x0, x1, yy = -110, 110, -h / 2 + 118
        pa = peinture(BLANC, 0.5, Style=skia.Paint.kStroke_Style, StrokeWidth=3); pa.setPathEffect(skia.DashPathEffect.Make([8, 9], (t * 40) % 17))
        pth = skia.Path(); pth.moveTo(x0, yy); pth.quadTo(0, yy - 24, x1, yy); c.drawPath(pth, pa)
        u = (t * 0.35) % 1; px = x0 + (x1 - x0) * u; py = yy - 24 * 2 * u * (1 - u)
        c.save(); c.translate(px, py); c.rotate(90 + 30 * (0.5 - u)); icone(c, "plane", 0, 0, 44, JAUNE, 2.4); c.restore()
        for k in range(26):
            hh = 60 if k % 3 else 80
            rrect(c, -w / 2 + 40 + k * 14, h / 2 - 40 - hh, 6 + (k % 2) * 3, hh, 2, BLANC, 0.75)
        texte(c, "VOL CA 934 · PORTE 12", w / 2 - 40, h / 2 - 76, 24, A["gris"], "titre", "droite", 0.06)
    c.restore()


def signet(c, cx, cy, taille, plein, alpha=1.0):
    """le bouton « enregistrer » de TikTok : un signet qui se remplit de jaune"""
    k = taille / 100
    pth = skia.Path(); pth.moveTo(cx - 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy + 50 * k)
    pth.lineTo(cx, cy + 24 * k); pth.lineTo(cx - 36 * k, cy + 50 * k); pth.close()
    with Calque(c, alpha):
        if plein > 0:
            c.save(); c.clipRect(skia.Rect.MakeXYWH(cx - 60 * k, cy + 52 * k - 104 * k * plein, 120 * k, 104 * k * plein))
            c.drawPath(pth, peinture(JAUNE)); c.restore()
        p = peinture(BLANC, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=7 * k, StrokeJoin=skia.Paint.kRound_Join)
        c.drawPath(pth, p)


def hook(c, t):
    if t > ETAPES[0] + 0.3: return
    sortie_h = prog(t, ETAPES[0] - 0.3, 0.35, entree)
    with Calque(c, 1 - sortie_h):
        part = prog(t, T_RAIL, 0.45, entreeSortie)            # la carte et le signet laissent la place au 7
        lettres(c, "TU PARS", 540, 400 - 160 * part, 132, t, -0.7, "ressort", grad=False, couleur=BLANC, decal=0.04, alpha=1 - part)
        lettres(c, "EN CHINE ?", 540, 535 - 160 * part, 132, t, -0.55, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.04, alpha=1 - part)
        carte_embarquement(c, 540, 930 + 600 * part ** 2, t, 1 - part)
        # « Enregistre » : le signet qui se remplit sous le doigt
        a = entre(t, TW(4) - 0.15, 0.4, 2.2)
        if a > 0 and part < 1:
            t_clic = TW(4) + 0.35
            plein = prog(t, t_clic, 0.3, sortie)
            cx, cy = 820, 1150 + 400 * part
            c.save(); c.translate(cx, cy); c.scale(mix(0.3, 1, a) * battement(t, t_clic, 0.2, 0.3), mix(0.3, 1, a) * battement(t, t_clic, 0.2, 0.3))
            lueur(c, 0, 0, 170, JAUNE, 0.25 + 0.35 * plein)
            disque(c, 0, 0, 105, "#1A1030", 0.85); anneau(c, 0, 0, 105, JAUNE if plein > 0.5 else BLANC, 4, 0.8)
            signet(c, 0, 0, 120, plein)
            c.restore()
            if plein > 0:
                pl = prog(t, t_clic, 0.8, sortie)
                texte(c, "+1", cx + 150, cy - 110 - 60 * pl, 52, JAUNE, "noir", "centre", 0, alpha=1 - max(0, pl - 0.6) / 0.4)
            pa = prog(t, t_clic - 0.4, 0.38, sortie)
            if t < t_clic + 0.6:
                curseur(c, mix(1000, cx + 10, pa), mix(1500, cy + 20, pa), 1.3, 1 - prog(t, t_clic + 0.3, 0.3), prog(t, t_clic - 0.05, 0.05) * (1 - prog(t, t_clic + 0.05, 0.1)))
            eclats(c, cx, cy, t, t_clic, 14, 260, [JAUNE, BLANC, VC], graine=3)
            pastille_verre(c, "Enregistre-la", 380, 1150 + 400 * part, 44, "bookmark", borne(a * 3), mix(0.4, 1, a), accent="#B8901A", rot=-4)
        if part < 0.99:
            with Calque(c, 1 - part):
                tampon_c(c, "AVANT DE RÉSERVER", 540, 1000 + 600 * part ** 2, t, TW(7) + 0.05, JAUNE, -7, 50)
        # « reste jusqu'au numéro sept » : le 7 sous cadenas, puis il file dans le rail
        a7 = entre(t, TW(17) - 0.1, 0.5, 1.6)
        if a7 > 0:
            vol = prog(t, ETAPES[0] - 0.6, 0.45, entreeSortie)
            cx, cy = mix(540, RAIL_X[6], vol), mix(900, RAIL_Y, vol)
            s = mix(0.4, 1, a7) * mix(1, 30 / 150, vol)
            c.save(); c.translate(cx, cy); c.scale(s, s)
            lueur(c, 0, 0, 330, JAUNE, 0.3 + 0.1 * math.sin(t * 6))
            rayons(c, 0, 0, t, 520, 0.12 * (1 - vol), 12, JAUNE)
            disque(c, 0, 0, 150, "#2A2040"); anneau(c, 0, 0, 150, JAUNE, 10)
            texte(c, "7", -12, -hauteurLigne(190) / 2, 190, JAUNE, "noir", "centre", -0.02)
            c.save(); c.translate(92, 92); disque(c, 0, 0, 52, JAUNE); icone(c, "lock", 0, 0, 56, "#1A1030", 2.8); c.restore()
            c.restore()
            if vol < 0.2:
                ep = entre(t, TW(24) - 0.1, 0.4, 2.2)
                if ep > 0:
                    with Calque(c, borne(a7 * 3) * (1 - vol * 5)):
                        pastille_verre(c, "Le plus rentable", 540, 1150, 44, "trophy", borne(ep * 3), mix(0.4, 1, ep), accent="#B8901A")
            if TW(24) - 0.05 <= t:
                for k in range(8):
                    u = prog(t, TW(24) - 0.05 + 0.05 * k, 0.6, sortie)
                    if 0 < u < 1:
                        a_ = k * math.pi / 4 + 0.3
                        texte(c, "€", 540 + 260 * u * math.cos(a_), 900 + 260 * u * math.sin(a_) - 40, 64, JAUNE, "noir", "centre", 0, alpha=1 - u)


# ─────────────────────────────────────────── 1 · train de nuit
def etape1(c, t):
    g = Groupe(c, t, ETAPES[0] - 0.4, FINS[0], ent="grand", sor="gauche")
    if not g.visible: return
    with g:
        entete(c, t, 1, "TRAIN DE NUIT", ETAPES[0] - 0.2)
        # l'avion qu'on oublie
        a = entre(t, ETAPES[0] - 0.2, 0.45, 1.8)
        barre = prog(t, TW(36), 0.25, sortie)
        if a > 0:
            dx = -120 * prog(t, TW(37), 0.4, entreeSortie)
            carte(c, 300 + dx, 840, 360, 330, 40, alpha=borne(a * 3) * (1 - 0.5 * barre), s=mix(0.5, 1, a) * (1 - 0.12 * barre))
            icone(c, "plane", 300 + dx, 800, 120, BLANC, 2.0, borne(a * 3) * (1 - 0.5 * barre))
            texte(c, "Vol intérieur", 300 + dx, 900, 34, A["gris"], "gras", "centre", -0.01, borne(a * 3))
            croix(c, 300 + dx, 840, 150, barre)
        # le train de nuit
        b = entre(t, TW(30) - 0.1, 0.5, 1.6)
        if b > 0:
            cen = prog(t, TW(37) - 0.05, 0.45, entreeSortie)
            cx, cy = mix(780, 600, cen), mix(840, 860, cen)
            s = mix(0.5, 1, b) * mix(1, 1.18, cen)
            carte(c, cx, cy, 400, 360, 44, violet=0.25, alpha=borne(b * 3), s=s)
            c.save(); c.translate(cx, cy); c.scale(s, s)
            lueur(c, 0, -30, 160, VC, 0.3)
            icone(c, "train-front", 0, -20, 140, BLANC, 2.0)
            icone(c, "moon", 120, -120, 60, JAUNE, 2.4)
            texte(c, "Train de nuit", 0, 100, 34, BLANC, "gras", "centre", -0.01)
            c.restore()
            if t > TW(38):
                for k in range(3):
                    u = ((t - TW(38)) * 0.9 + k / 3) % 1
                    texte(c, "z", cx + 150 + 40 * u + 20 * k, cy - 150 - 120 * u, 40 + 14 * k, VC, "noir", "centre", 0, alpha=math.sin(math.pi * u))
        # la nuit d'hôtel en moins
        h = entre(t, TW(43) - 0.1, 0.45, 1.8)
        if h > 0:
            carte(c, 540, 1180, 640, 150, 34, alpha=borne(h * 3), s=mix(0.5, 1, h))
            with Calque(c, borne(h * 3)):
                icone(c, "bed-double", 290, 1180, 70, BLANC, 2.0)
                texte(c, "1 nuit d'hôtel", 350, 1180 - hauteurLigne(42, "gras") / 2, 42, BLANC, "gras", track=-0.01)
                texte(c, "€€", 780, 1180 - hauteurLigne(52) / 2, 52, JAUNE, "noir", "centre", 0)
                bb = prog(t, TW(47) - 0.05, 0.22, sortie)
                if bb > 0: trait(c, 250, 1200, 250 + 590 * bb, 1160, ROUGE, 10)
            tampon_c(c, "− 1 NUIT", 820, 1080, t, TW(47) + 0.1, JAUNE, 8, 46)


# ─────────────────────────────────────────── 2 · pass métro 24 h
def etape2(c, t):
    g = Groupe(c, t, FINS[0] - 0.12, FINS[1], ent="droite", sor="zoom")
    if not g.visible: return
    with g:
        entete(c, t, 2, "PASS MÉTRO 24 H", ETAPES[1])
        a = entre(t, TW(50) - 0.1, 0.5, 1.4)
        if a > 0:
            with Espace(c, 540, 820, rx=mix(50, 0, a), s=mix(0.6, 1, a)):
                with Calque(c, borne(a * 3)):
                    verre(c, 130, 660, 820, 320, 40, 0.08, violet=0.18)
                    icone(c, "train-front", 230, 760, 90, BLANC, 2.0)
                    texte(c, "PASS", 300, 700, 46, VC, "titre", track=0.12)
                    texte(c, "24 H", 300, 750, 128, BLANC, "noir", track=-0.03)
                    pastille_verre(c, "Illimité", 330, 930, 30, "check", 1.0, entre(t, TW(51) + 0.2, 0.4, 2.2), accent=VERT)
                    # horloge 24 h qui fait le tour sur « toute la journée »
                    cx, cy, R = 800, 820, 100
                    anneau(c, cx, cy, R, BLANC, 10, 0.15)
                    u = prog(t, TW(65) - 0.1, 0.9, entreeSortie)
                    if u > 0:
                        pth = skia.Path(); pth.addArc(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), -90, 360 * u)
                        c.drawPath(pth, peinture(JAUNE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=10, StrokeCap=skia.Paint.kRound_Cap))
                    icone(c, "clock", cx, cy, 90, BLANC, 2.0)
        # moins de 3 €
        p = entre(t, TW(54) - 0.1, 0.45, 1.8)
        if p > 0:
            c.save(); c.translate(540, 1130); c.scale(mix(0.5, 1, p), mix(0.5, 1, p))
            lueur(c, 0, 0, 260, JAUNE, 0.25)
            texte(c, "MOINS DE", -150, -hauteurLigne(40, "titre") / 2 - 4, 40, BLANC, "titre", "droite", 0.04)
            w3 = rouleau(c, 3, -120, -100, 170, t, TW(54) - 0.1, TW(56) + 0.1, JAUNE)
            texte(c, "€", -120 + w3 + 16, -100 + 10, 150, JAUNE, "noir", track=-0.02)
            c.restore()
        for (lab, t0, x) in [("Shanghai · 18 ¥", TW(59), 300), ("Canton · 20 ¥", TW(62), 780)]:
            b = entre(t, t0 - 0.1, 0.42, 2.2)
            if b > 0: pastille_verre(c, lab, x, 1300, 34, "map-pin", borne(b * 3), mix(0.4, 1, b))


# ─────────────────────────────────────────── 3 · musées gratuits
def passeport(c, cx, cy, s, rot, alpha):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, alpha):
        rrect(c, -130, -180, 260, 360, 22, "#7A1F2B", 1.0, (14, 34, 0.4))
        anneau(c, 0, -30, 58, "#E2C36B", 5); etoile4(c, 0, -30, 34, "#E2C36B")
        texte(c, "PASSEPORT", 0, 60, 30, "#E2C36B", "noir", "centre", 0.08)
        rrect(c, -40, 120, 80, 18, 6, "#E2C36B", 0.7)
    c.restore()


def etape3(c, t):
    g = Groupe(c, t, FINS[1] - 0.12, FINS[2], ent="grand", sor="haut")
    if not g.visible: return
    with g:
        entete(c, t, 3, "MUSÉES GRATUITS", ETAPES[2])
        a = entre(t, TW(71) - 0.15, 0.5, 1.6)
        if a > 0:
            c.save(); c.translate(400, 840); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
            lueur(c, 0, 0, 230, VC, 0.3)
            verre(c, -170, -170, 340, 340, 170, 0.08, violet=0.2)
            icone(c, "landmark", 0, -10, 170, BLANC, 1.8)
            c.restore()
        b = entre(t, TW(72) - 0.05, 0.45, 1.8)
        if b > 0:
            carte(c, 540, 1160, 600, 150, 30, alpha=borne(b * 3), s=mix(0.5, 1, b))
            with Calque(c, borne(b * 3)):
                icone(c, "ticket", 300, 1160, 64, BLANC, 2.0)
                texte(c, "Entrée", 350, 1160 - hauteurLigne(44, "gras") / 2, 44, BLANC, "gras", track=-0.01)
                texte(c, "¥ ¥ ¥", 760, 1160 - hauteurLigne(48) / 2, 48, A["gris"], "noir", "centre", 0)
                bb = prog(t, TW(74) - 0.05, 0.2, sortie)
                if bb > 0: trait(c, 680, 1180, 680 + 170 * bb, 1140, ROUGE, 9)
            tampon_c(c, "GRATUIT", 760, 1060, t, TW(74) + 0.1, VERT, -10, 58)
        p = entre(t, TW(79) - 0.1, 0.5, 1.6)
        if p > 0:
            passeport(c, mix(1200, 790, p), 800, 0.9, mix(25, 8, p), 1.0)
            ok = entre(t, TW(80), 0.35, 2.4)
            if ok > 0:
                disque(c, 890, 640, 44 * ok, VERT); icone(c, "check", 890, 640, 50 * ok, BLANC, 3.2)


# ─────────────────────────────────────────── 4 · Dianping
ORANGE_DP = "#FF6633"


def ecran_dianping(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#F5F5F5"))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 170), peinture(ORANGE_DP))
    texte(c, "Dianping", x + 34, y + 70, 46, BLANC, "noir", track=-0.02)
    rrect(c, x + 30, y + 190, w - 60, 56, 28, BLANC)
    icone(c, "search", x + 64, y + 218, 28, "#999999", 2.4)
    texte(c, "Restaurants près de moi", x + 90, y + 202, 24, "#999999", "fort", track=0)
    noms = ["Hotpot du quartier", "Raviolis maison", "Canard laqué"]
    for k in range(3):
        t0 = TW(88) + 0.15 * k
        u = entre(t, t0, 0.35, 1.6)
        if u <= 0: continue
        yy = y + 280 + k * 180
        c.save(); c.translate(0, 30 * (1 - u))
        with Calque(c, borne(u * 3)):
            rrect(c, x + 24, yy, w - 48, 160, 22, BLANC, 1.0, (4, 12, 0.08))
            rrect(c, x + 40, yy + 16, 128, 128, 18, "#FFE3D6"); icone(c, "utensils", x + 104, yy + 80, 60, ORANGE_DP, 2.2)
            texte(c, noms[k], x + 186, yy + 28, 28, "#1A1A1A", "fort", track=0)
            for j in range(5): icone(c, "star", x + 200 + j * 30, yy + 86, 24, "#FFB020", 2.2)
            p = entre(t, TW(94) + 0.1 * k, 0.32, 2.4)
            if p > 0:
                c.save(); c.translate(x + w - 100, yy + 104); c.scale(p, p)
                rrect(c, -62, -22, 124, 44, 22, ORANGE_DP); texte(c, "PROMO", 0, -hauteurLigne(22, "noir") / 2, 22, BLANC, "noir", "centre", 0.04)
                c.restore()
        c.restore()


def etape4(c, t):
    g = Groupe(c, t, FINS[2] - 0.12, FINS[3], ent="bas", sor="gauche")
    if not g.visible: return
    with g:
        entete(c, t, 4, "RESTO : DIANPING", ETAPES[3])
        a = entre(t, TW(87) - 0.15, 0.55, 1.4)
        if a > 0:
            with Espace(c, 540, 990, ry=mix(-40, -8, a) + 3 * math.sin(t * 1.6), rx=4, s=mix(0.6, 1, a)):
                telephone_sombre(c, 540, 990, 400, 760, lambda cc, x, y, w, h: ecran_dianping(cc, x, y, w, h, t), borne(a * 3))
        # au comptoir ¥¥¥ (barré) / dans l'appli ¥
        b = entre(t, TW(97) - 0.1, 0.42, 2.2)
        if b > 0:
            pastille_verre(c, "Comptoir  ¥¥¥", 220, 1210, 34, "store", borne(b * 3), mix(0.4, 1, b), accent=ROUGE, rot=-5)
            bb = prog(t, TW(98), 0.2, sortie)
            if bb > 0: trait(c, 80, 1225, 80 + 300 * bb, 1195, ROUGE, 8)
        d = entre(t, TW(99) - 0.05, 0.42, 2.2)
        if d > 0: pastille_verre(c, "Appli  ¥", 860, 700, 38, "badge-percent", borne(d * 3), mix(0.4, 1, d), accent="#B8901A", rot=5)


# ─────────────────────────────────────────── partage : « Envoie cette vidéo à celui qui part avec toi »
def partage(c, t):
    g = Groupe(c, t, T_PARTAGE - 0.12, FINS[3] + (ETAPES[4] - FINS[3]), ent="zoom", sor="zoom")
    if not g.visible or t >= ETAPES[4] + 0.2: return
    with g:
        lettres(c, "ENVOIE-LA", 540, 420, 120, t, T_PARTAGE - 0.05, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.035)
        a = entre(t, T_PARTAGE, 0.45, 1.8)
        if a > 0:
            c.save(); c.translate(540, 760); c.scale(mix(0.4, 1, a) * battement(t, T_PARTAGE + 0.5, 0.1, 0.3), mix(0.4, 1, a) * battement(t, T_PARTAGE + 0.5, 0.1, 0.3))
            lueur(c, 0, 0, 200, JAUNE, 0.35); disque(c, 0, 0, 110, JAUNE)
            icone(c, "share-2", -4, 0, 120, "#1A1030", 2.6)
            c.restore()
        for (lab, x, t0) in [("Toi", 250, TW(103)), ("Ton pote", 830, TW(105))]:
            b = entre(t, t0 - 0.1, 0.4, 2.2)
            if b > 0:
                c.save(); c.translate(x, 1120); c.scale(b, b)
                disque(c, 0, 0, 86, "#2A2040"); anneau(c, 0, 0, 86, VC, 4)
                icone(c, "user-round", 0, -6, 90, BLANC, 2.0)
                texte(c, lab, 0, 104, 34, BLANC, "gras", "centre", -0.01)
                c.restore()
        # la vidéo part de toi vers ton pote
        u = prog(t, TW(106) - 0.05, 0.6, entreeSortie)
        if 0 < u < 1.0 or t > TW(106) + 0.55:
            x = mix(250, 830, u); y = 1120 - 260 * math.sin(math.pi * u)
            c.save(); c.translate(x, y); c.rotate(-15 + 30 * u); c.scale(0.9, 0.9)
            rrect(c, -50, -80, 100, 160, 16, V, 1.0, (8, 20, 0.4)); icone(c, "play", 4, 0, 50, BLANC, 2.6)
            c.restore()
        if t > TW(106) + 0.55:
            ok = entre(t, TW(106) + 0.55, 0.35, 2.4)
            disque(c, 900, 1050, 34 * ok, VERT); icone(c, "check", 900, 1050, 40 * ok, BLANC, 3.2)


# ─────────────────────────────────────────── 5 · DiDi, pas Uber
ORANGE_DIDI = "#FF7A00"


def etape5(c, t):
    g = Groupe(c, t, FINS[3] + (ETAPES[4] - FINS[3]) - 0.12, FINS[4], ent="droite", sor="zoom")
    if not g.visible or t < ETAPES[4] - 0.15: return
    with g:
        entete(c, t, 5, "DIDI, PAS UBER", ETAPES[4])
        a = entre(t, TW(111) - 0.1, 0.42, 2.0)
        if a > 0:
            sx = secousse(t, TW(114), 14)[0]
            tuile_logo(c, "uber", 310 + sx, 820, 230, "#000000", BLANC, borne(a * 3) * (1 - 0.45 * prog(t, TW(114), 0.2)), mix(0.4, 1, a))
            interdit(c, 310 + sx, 820, 150, prog(t, TW(114) - 0.05, 0.25, sortie))
        b = entre(t, TW(117) - 0.1, 0.45, 1.8)
        if b > 0:
            tuile_logo(c, None, 770, 820, 250, ORANGE_DIDI, BLANC, borne(b * 3), mix(0.4, 1, b) * battement(t, TW(118), 0.08, 0.3), texte_="DiDi")
        # la course : prix affiché avant, payé avec Alipay
        d = entre(t, TW(120) - 0.1, 0.45, 1.6)
        if d > 0:
            carte(c, 540, 1160, 820, 220, 36, alpha=borne(d * 3), s=mix(0.5, 1, d))
            with Calque(c, borne(d * 3)):
                disque(c, 200, 1120, 14, VERT); disque(c, 200, 1200, 14, ROUGE)
                trait(c, 200, 1134, 200, 1186, BLANC, 3, 0.5, pointille=[6, 6])
                texte(c, "Départ", 230, 1104, 28, BLANC, "fort", track=0); texte(c, "Arrivée", 230, 1184, 28, BLANC, "fort", track=0)
                u = ((t - TW(120)) * 0.4) % 1
                icone(c, "car-taxi-front", 200, mix(1120, 1200, u), 34, JAUNE, 2.2)
                pr = entre(t, TW(122) - 0.05, 0.4, 2.2)
                if pr > 0:
                    c.save(); c.translate(600, 1160); c.scale(pr, pr)
                    rrect(c, -150, -46, 300, 92, 46, JAUNE)
                    texte(c, "Prix affiché", 0, -hauteurLigne(32, "noir") / 2, 32, "#1A1030", "noir", "centre", 0)
                    c.restore()
            al = entre(t, TW(130) - 0.1, 0.4, 2.4)
            if al > 0: tuile_logo(c, "alipay", 880, 1160, 120, MARQUES["alipay"], BLANC, borne(al * 3), al)


# ─────────────────────────────────────────── 6 · Trip.com, Airbnb absent
def etape6(c, t):
    g = Groupe(c, t, FINS[4] - 0.12, FINS[5], ent="grand", sor="gauche")
    if not g.visible: return
    with g:
        entete(c, t, 6, "DORMIR : TRIP.COM", ETAPES[5])
        a = entre(t, ETAPES[5] + 0.15, 0.45, 1.8)
        if a > 0: tuile_logo(c, "tripdotcom", 340, 800, 230, "#287DFA", BLANC, borne(a * 3), mix(0.4, 1, a))
        b = entre(t, TW(139) - 0.1, 0.42, 2.0)
        if b > 0:
            tuile_logo(c, "airbnb", 770, 800, 200, "#FF5A5F", BLANC, borne(b * 3) * (1 - 0.45 * prog(t, TW(141), 0.2)), mix(0.4, 1, b))
            interdit(c, 770, 800, 130, prog(t, TW(141) - 0.05, 0.25, sortie))
            tampon_c(c, "PAS EN CHINE", 770, 980, t, TW(143), ROUGE, 6, 34)
        d = entre(t, TW(137) - 0.05, 0.45, 1.6)
        if d > 0:
            carte(c, 540, 1180, 820, 190, 36, alpha=borne(d * 3), s=mix(0.5, 1, d))
            with Calque(c, borne(d * 3)):
                rrect(c, 160, 1115, 130, 130, 22, "#287DFA", 0.25); icone(c, "hotel", 225, 1180, 70, BLANC, 2.0)
                texte(c, "Hôtel · centre-ville", 320, 1128, 34, BLANC, "gras", track=-0.01)
                for j in range(4): icone(c, "star", 336 + j * 34, 1200, 28, JAUNE, 2.2)
                ok = prog(t, TW(138), 0.25, sortie)
                rrect(c, 690, 1148, 190, 64, 32, VERT if ok > 0.5 else "#287DFA")
                texte(c, "Réservé" if ok > 0.5 else "Réserver", 785, 1180 - hauteurLigne(28, "noir") / 2, 28, BLANC, "noir", "centre", 0)


# ─────────────────────────────────────────── 7 · direct au fournisseur, puis ChinaBook par DROP&YOU
def noeud(c, x, y, ic, lab, a, couleur=BLANC, fond=None):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(mix(0.3, 1, a), mix(0.3, 1, a))
    with Calque(c, borne(a * 3)):
        lueur(c, 0, 0, 140, fond or VC, 0.28)
        verre(c, -95, -95, 190, 190, 95, 0.08, violet=0.2 if fond is None else 0.05)
        icone(c, ic, 0, 0, 96, couleur, 2.0)
        texte(c, lab, 0, 118, 32, BLANC, "gras", "centre", -0.01)
    c.restore()


def etape7(c, t):
    if t < ETAPES[6] - 0.15: return
    g = Groupe(c, t, ETAPES[6] - 0.15, DUREE + 1, ent="zoom", sor="aucune")
    with g:
        logo_t = prog(t, T_LOGO_CB - 0.1, 0.4, entreeSortie)
        with Calque(c, 1 - logo_t):
            entete(c, t, 7, "DIRECT FOURNISSEUR", ETAPES[6], [JAUNE, "#FFE98A"])
            y = 1000
            noeud(c, 190, y, "user-round", "Toi", entre(t, TW(149) - 0.1, 0.4, 2))
            mid = entre(t, TW(161) - 0.15, 0.4, 2)
            chute = prog(t, TW(162) + 0.15, 0.6, entree)
            noeud(c, 540, y + 600 * chute ** 2, "store", "Intermédiaire", mid * (1 - chute))
            interdit(c, 540, y + 600 * chute ** 2, 110, prog(t, TW(162) - 0.05, 0.25, sortie) * (1 - chute))
            noeud(c, 890, y, "package", "Fournisseur", entre(t, TW(153) - 0.1, 0.4, 2), JAUNE, JAUNE)
            # les flèches : d'abord par l'intermédiaire, puis en direct
            for (xa, xb, t0) in [(290, 445, TW(161)), (635, 790, TW(161) + 0.1)]:
                u = prog(t, t0, 0.25, sortie) * (1 - chute)
                if u > 0: trait(c, xa, y, xa + (xb - xa) * u, y, BLANC, 5, 0.5)
            u = prog(t, TW(163) - 0.05, 0.5, sortie)
            if u > 0:
                pth = skia.Path(); n = 40
                for k in range(n + 1):
                    v = k / n * u; x = mix(220, 860, v); yy = y - 120 - 230 * math.sin(math.pi * v)
                    (pth.moveTo if k == 0 else pth.lineTo)(x, yy)
                c.drawPath(pth, peinture(JAUNE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=10, StrokeCap=skia.Paint.kRound_Cap))
                if u >= 1:
                    pastille_verre(c, "En direct", 540, y - 360, 40, "zap", 1.0, entre(t, TW(164), 0.35, 2.2), accent="#B8901A")
            eclats(c, 860, y - 110, t, TW(164), 12, 240, [JAUNE, BLANC, VC], graine=4)
        # ChinaBook (violet) par DROP&YOU
        if logo_t > 0:
            ul = entre(t, T_LOGO_CB + 0.1, 0.5, 1.5)
            lueur(c, 540, 860, 600 * logo_t, "#6E48F0", 0.45)
            rayons(c, 540, 860, t, 900, 0.10 * logo_t, 14, "#9B83FF")
            iw, ih = taille_img("logo-chinabook-blanc"); lw = 820 * mix(0.6, 1, ul)
            image(c, "logo-chinabook-blanc", 540 - lw / 2, 800 - lw * ih / iw / 2, lw, borne(ul * 3))
            up = entre(t, TW(175) - 0.1, 0.45, 1.8)
            if up > 0:
                texte(c, "par", 540, 960, 36, A["gris"], "gras", "centre", 0, borne(up * 3))
                iw, ih = taille_img("logo-dy-blanc"); lw2 = 440 * mix(0.6, 1, up)
                image(c, "logo-dy-blanc", 540 - lw2 / 2, 1030, lw2, borne(up * 3))
            # « Dis-moi en commentaire ta ville de départ »
            cm = entre(t, T_COM, 0.45, 1.8)
            if cm > 0:
                c.save(); c.translate(540, 1270); c.scale(mix(0.5, 1, cm), mix(0.5, 1, cm))
                with Calque(c, borne(cm * 3)):
                    verre(c, -400, -60, 800, 120, 60, 0.12)
                    icone(c, "message-circle", -340, 0, 50, JAUNE, 2.4)
                    villes = ["Ta ville de départ ?", "Paris", "Lyon", "Marseille", "Bruxelles"]
                    k = min(len(villes) - 1, int(max(0, t - T_COM - 0.3) / 0.55))
                    mot = villes[k]
                    n = len(mot) if k == 0 else int(borne((t - T_COM - 0.3 - 0.55 * k) / 0.3) * len(mot) + 0.999)
                    coul = A["gris"] if k == 0 else BLANC
                    texte(c, mot[:n], -290, -hauteurLigne(40, "gras") / 2, 40, coul, "gras", track=-0.01)
                    if k > 0 and int(t * 4) % 2 == 0: rrect(c, -290 + largeur(mot[:n], 40, "gras", -0.01) + 6, -24, 4, 48, 2, JAUNE)
                c.restore()


# ─────────────────────────────────────────── sons (forts, propres, sur de vraies actions)
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(0.05, "pop", -11)
son(TW(4) - 0.15, "pop", -9); son(TW(4) + 0.35, "clic", -5); son(TW(4) + 0.38, "ching", -8); son(TW(4) + 0.4, "check", -9)
son(TW(7) - 0.07, "tampon", -6)
son(T_RAIL, "whoosh", -8)
for k in range(7): son(T_RAIL + 0.05 * k, "tick", -15)
son(TW(17) - 0.1, "impact_doux", -6); son(TW(17), "montee", -12)
for k in range(6): son(TW(24) - 0.05 + 0.06 * k, "ching", -16)
son(ETAPES[0] - 0.6, "whoosh_long", -9)
for k, t0 in enumerate(ETAPES):
    son(t0 - 0.15, "whoosh" if k % 2 == 0 else "whoosh_bas", -7)
    son(t0 - 0.05, "impact_doux", -8); son(t0, "pop", -10)
son(TW(29) - 0.1, "pop", -11); son(TW(36), "croc", -7); son(TW(30) - 0.1, "whoosh_court", -10)
son(TW(43) - 0.1, "pop", -11); son(TW(47) - 0.05, "croc", -9); son(TW(47), "tampon", -6)
son(TW(50) - 0.1, "verre", -9); son(TW(51) + 0.2, "check", -11)
for k in range(10): son(TW(54) - 0.1 + 0.035 * k, "tick", -15)
son(TW(56) + 0.1, "ching", -8); son(TW(59) - 0.1, "pop", -10); son(TW(62) - 0.1, "pop", -10); son(TW(65) - 0.1, "montee", -13)
son(TW(71) - 0.15, "pop", -10); son(TW(72) - 0.05, "pop", -11); son(TW(74) - 0.05, "croc", -9); son(TW(74), "tampon", -6)
son(TW(79) - 0.1, "swipe", -9); son(TW(80), "check", -9)
son(TW(87) - 0.15, "whoosh", -9)
for k in range(3): son(TW(88) + 0.15 * k, "pop", -13); son(TW(94) + 0.1 * k, "blip", -13)
son(TW(97) - 0.1, "pop", -10); son(TW(98), "croc", -9); son(TW(99) - 0.05, "ching", -9)
son(T_PARTAGE - 0.1, "whoosh_bas", -7); son(T_PARTAGE + 0.5, "impact_doux", -9)
son(TW(103) - 0.1, "pop", -10); son(TW(105) - 0.1, "pop", -10); son(TW(106) - 0.05, "whoosh_court", -9); son(TW(106) + 0.55, "message_in", -8)
son(TW(111) - 0.1, "pop", -10); son(TW(114) - 0.05, "impact", -7); son(TW(117) - 0.1, "pop", -9); son(TW(118), "ching", -12)
son(TW(120) - 0.1, "verre", -10); son(TW(122) - 0.05, "check", -9); son(TW(130) - 0.1, "pop", -10)
son(ETAPES[5] + 0.15, "pop", -9); son(TW(137) - 0.05, "verre", -10); son(TW(138), "check", -9)
son(TW(139) - 0.1, "pop", -10); son(TW(141) - 0.05, "impact", -7); son(TW(143) - 0.07, "tampon", -7)
son(ETAPES[6] - 0.05, "impact", -4); son(ETAPES[6], "ching", -8)
son(TW(149) - 0.1, "pop", -10); son(TW(153) - 0.1, "pop", -10); son(TW(161) - 0.15, "pop", -10)
son(TW(162) - 0.05, "impact", -6); son(TW(162) + 0.15, "whoosh_bas", -10); son(TW(163) - 0.05, "whoosh_long", -9); son(TW(164), "ching", -9)
son(T_LOGO_CB - 0.1, "montee", -11); son(T_LOGO_CB + 0.1, "impact", -5); son(T_LOGO_CB + 0.12, "verre", -9)
son(TW(175) - 0.1, "pop", -9); son(T_COM, "message", -9)
for k in range(1, 5):
    for j in range(5): son(T_COM + 0.3 + 0.55 * k + 0.06 * j, "frappe", -17)

for a, b in [(0.0, 0.25), (T_RAIL, T_RAIL + 0.3), (ETAPES[0] - 0.75, ETAPES[0] + 0.3)] + \
            [(t0 - 0.2, t0 + 0.3) for t0 in ETAPES[1:]] + [(T_PARTAGE - 0.2, T_PARTAGE + 0.3), (TW(106) - 0.05, TW(106) + 0.5),
                                                           (T_LOGO_CB - 0.1, T_LOGO_CB + 0.4), (TW(162) + 0.1, TW(162) + 0.6)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(4) + 0.38, JAUNE, 0.10), (TW(17), JAUNE, 0.08), (ETAPES[6], JAUNE, 0.14), (T_LOGO_CB + 0.1, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, ETAPES[6], 1, 0.6) + battement(t, T_LOGO_CB + 0.1, 1, 0.6) - 2)
    entete_marque(c, t)
    hook(c, t)
    etape1(c, t); etape2(c, t); etape3(c, t); etape4(c, t); partage(c, t); etape5(c, t); etape6(c, t); etape7(c, t)
    rail(c, t)
    K.dessine_eclairs(c, t)
    if not (T_LOGO_CB < t < T_COM): SOUS.dessine(c, t, BLANC)
