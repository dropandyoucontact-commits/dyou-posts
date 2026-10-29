"""AC-M06 — RECTO CERVEAU. Hayden Panettiere : « Elle a sauvé le monde à la télé. »

Deuxième vidéo du format « BONHOMME » (29/10/2026) — voir AC-M05 et `moteur/bonhomme.py`.
Ici le bonhomme raconte UNE VIE (le « draw my life » des TikTok à millions de vues) : il grandit
scène après scène (`taille`), les autres personnages sont des bonhommes sans photo (la mère, le
père, l'homme, le frère), et la fin est un cercle rouge vide.

Sujet vérifié (BBC 28/10/2026 « Death of US actress Hayden Panettiere ruled accidental », NBC, CBS ;
BBC « A life of struggles alongside screen success ») :
  - 28/10 : la police de Greenville (Caroline du Sud) classe sa mort « accidentelle », enquête close.
    Retrouvée sans vie le 16/08/2026, à 36 ans. Le médecin légiste avait conclu à une overdose
    accidentelle en septembre. **On ne nomme aucune substance** (règle AC-M03).
  - Première pub à 11 mois ; feuilleton (One Life to Live) à 4 ans ; Remember the Titans avec
    Denzel Washington en 2000 (10-11 ans) ; sa mère Lesley Vogel était sa manager ;
    Heroes en 2006 à 17 ans, Claire la pom-pom girl qui se régénère, « Save the cheerleader,
    save the world » ; paparazzis ; une « happy pill » donnée par une attachée de presse avant un
    tapis rouge, « the gateway drug » selon elle ; fille Kaya née fin 2014 (elle a 25 ans) avec
    Wladimir Klitschko ; dépression post-partum, alcool ; garde confiée au père quand la petite a
    3 ans ; « no one should ever have to raise a child on FaceTime » ; Brian Hickerson, violences,
    condamné en 2021 ; frère Jansen mort en 2023 à 28 ans ; autobiographie « This Is Me » en mai 2026.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from bonhomme import *
import bonhomme as B

K = Kit(P, 1.0)
B.SENS_PHOTO.update({"hayden": 1, "hayden-jaune": 1, "hayden-sourire": 1})
DUREE = round(K.timing["duree_voix"] + 3.4, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
NB_IMAGES = K.nb_images
SFX = K.SFX
TW = K.TW; son = K.son; rapide = K.rapide; flou_a = K.flou_a

SOUS = sous_titres_bonhomme(K)
MEDIAS = ()

# ═════════════════════════════ repères
T_SAUVE, T_PERSONNE, T_HIER, T_HAYDEN, T_ACCIDENT, T_FERME, T_36 = TW(2), TW(8), TW(14), TW(22), TW(24), TW(26), TW(30)
T_PUB, T_ONZE, T_QUATRE, T_FEUILLETON, T_DIX, T_DENZEL, T_ENFANCE, T_MERE, T_MANAGER = TW(32), TW(38), TW(40), TW(47), TW(48), TW(56), TW(58), TW(63), TW(68)
T_17, T_GLOIRE, T_HEROES, T_CLAIRE, T_MOURIR, T_MONDE, T_SAUVEZ, T_SAUVEZ2 = TW(69), TW(74), TW(75), TW(78), TW(86), TW(87), TW(94), TW(98)
T_MAIS, T_PAPARAZZIS, T_TAPIS, T_ATTACHEE, T_PILULE, T_SOURIRE, T_DIRA, T_COMMENCE = TW(101), TW(104), TW(107), TW(111), TW(118), TW(120), TW(121), TW(126)
T_25, T_MAMAN, T_EFFONDRE, T_DEPRESSION, T_ALCOOL, T_PERE, T_GARDE, T_ACCEPTE, T_VISIO = TW(130), TW(135), TW(138), TW(139), TW(140), TW(141), TW(152), TW(154), TW(160)
T_PUIS, T_HOMME, T_FRAPPE, T_PRISON, T_2023, T_FRERE, T_MEURT, T_28 = TW(161), TW(163), TW(167), TW(171), TW(172), TW(176), TW(177), TW(179)
T_ANNEE, T_LIVRE, T_ECRIT, T_PASSE, T_ESPOIR = TW(181), TW(186), TW(189), TW(194), TW(198)
T_TROIS, T_RETROUVE, T_SANSVIE, T_CAROLINE, T_FILLE, T_ECRAN, T_ET, T_SAUVEE = TW(199), TW(205), TW(206), TW(212), TW(215), TW(223), TW(224), TW(228)
T_FIN = K.timing["duree_voix"]
T_SIGN = T_FIN + 0.3

X_C, X_G, X_D = 500, 330, 720
X_HORS = 1180


def fondu(t, a, b, d=0.35):
    return prog(t, a, d, sortie) * (1 - prog(t, b - d, d, entree))


# ═════════════════════════════ S1 — hook : elle a sauvé le monde, personne ne l'a sauvée
def s1(c, t):
    a = fondu(t, -1, T_HIER)
    if a <= 0.01: return
    with Calque(c, a):
        u_c = prog(t, 0.0, 0.45, lambda v: rebond(v, 1.3))
        down = prog(t, T_PERSONNE - 0.05, 0.7, douce)
        p = respire(melange(melange(STAND, CHEER, u_c), HEAD_DOWN, down), t)
        h = bonhomme(c, X_C, p, 1, "hayden")
        # le monde : un disque blanc qui monte au-dessus d'elle, puis qui s'éteint
        wa = prog(t, T_SAUVE - 0.05, 0.4, sortie) * (1 - down)
        if wa > 0.01:
            cx, cy = X_C, h["tete"][1] - h["r"] - 150 + 30 * (1 - wa)
            c.drawCircle(cx, cy, 90, peinture(BLANC, 0.0, Style=skia.Paint.kStroke_Style, StrokeWidth=8))
            anneau(c, cx, cy, 90, BLANC, 8, wa)
            for k in range(3):
                yy = cy - 60 + 60 * k
                dx = math.sqrt(max(0, 90 ** 2 - (yy - cy) ** 2))
                trait(c, cx - dx, yy, cx + dx, yy, BLANC, 5, wa * 0.8)
            trait(c, cx, cy - 90, cx, cy + 90, BLANC, 5, wa * 0.8)
        etiquette(c, X_C, 1338, "HAYDEN", prog(t, 0.3, 0.3, sortie), taille=34)
        if t >= T_PERSONNE + 0.6:
            larmes(c, h, t, T_PERSONNE + 0.6)


# ═════════════════════════════ S2 — hier : la police, un accident, 36 ans
def s2(c, t):
    a = fondu(t, T_HIER, T_PUB)
    if a <= 0.01: return
    with Calque(c, a):
        photo_plein(c, t, "rouge-plein", prog(t, T_HIER, 0.6, sortie), 1.0, y=130, h=980, zoom=1.0, fy=0.35)
        rubrique(c, t, prog(t, T_HAYDEN - 0.1, 0.4, sortie), "HAYDEN PANETTIERE", "DISPARITION")
        if t >= T_ACCIDENT - 0.05:
            etiquette(c, 540, 1180, "ACCIDENT · DOSSIER FERMÉ", prog(t, T_ACCIDENT - 0.05, 0.3, lambda v: rebond(v, 1.3)), taille=38)
        if t >= T_36 - 0.05:
            chiffre_geant(c, "36 ANS", 540, 1270, t, T_36 - 0.05, 120, BLANC)


# ═════════════════════════════ S3 — l'enfance : elle grandit, sa mère manager
def s3(c, t):
    a = fondu(t, T_PUB, T_17)
    if a <= 0.01: return
    with Calque(c, a):
        # la taille suit l'âge : 11 mois → 4 ans → 10 ans
        tl = cles(t, [(T_PUB, 0.32), (T_QUATRE - 0.1, 0.32), (T_QUATRE + 0.5, 0.5), (T_DIX - 0.1, 0.5), (T_DIX + 0.5, 0.68)], douce)
        down = prog(t, T_ENFANCE - 0.05, 0.6, douce)
        p = respire(melange(STAND, HEAD_DOWN, down), t)
        xh = X_G if t < T_DENZEL - 0.6 or t >= T_ENFANCE else X_G
        h = bonhomme(c, X_G, p, 1, None, "neutre", taille=tl)
        etiquette(c, X_G, 1338, "HAYDEN", prog(t, T_PUB, 0.3, sortie), taille=34)
        # la télé en haut : pub, puis feuilleton
        if T_ONZE - 0.1 <= t < T_DIX - 0.2:
            u_t = prog(t, T_ONZE - 0.1, 0.45, sortie) * (1 - prog(t, T_DIX - 0.4, 0.3, entree))
            tele(c, 640, 330, 460, 280, t, None, u_t, u_t)
            lab = "PUB" if t < T_FEUILLETON - 0.05 else "FEUILLETON"
            texte(c, lab, 640, 290, 70 if lab == "PUB" else 54, BLANC, "noir", "centre", 0.0, u_t)
        # Denzel : un grand bonhomme à droite
        u_d = prog(t, T_DENZEL - 0.5, 0.5, sortie) * (1 - prog(t, T_ENFANCE - 0.2, 0.3, entree))
        if u_d > 0.01:
            d = bonhomme(c, X_D, respire(melange(STAND, TALK, prog(t, T_DENZEL, 0.4, sortie)), t + 1), -1, None, "neutre", alpha=u_d)
            etiquette(c, X_D, 1338, "DENZEL", u_d, taille=34)
        # la mère, au téléphone
        u_m = prog(t, T_MERE - 0.1, 0.45, sortie)
        if u_m > 0.01:
            m = bonhomme(c, X_D, respire(PHONE, t + 2), -1, None, "severe", u=u_m)
            etiquette(c, X_D, 1338, "SA MÈRE", u_m, taille=34)
            if t >= T_MANAGER - 0.05:
                etiquette(c, X_D, 420, "MANAGER", prog(t, T_MANAGER - 0.05, 0.3, lambda v: rebond(v, 1.4)), taille=40, rouge=False)


# ═════════════════════════════ S4 — 17 ans, Heroes, la pom-pom girl
def s4(c, t):
    a = fondu(t, T_17, T_MAIS)
    if a <= 0.01: return
    with Calque(c, a):
        titre(c, "17 ANS", 300, 110, t, T_17, rouge=True, alpha=1 - prog(t, T_HEROES - 0.3, 0.3, entree))
        u_j = prog(t, T_17, 0.4, sortie) * (1 - prog(t, T_HEROES - 0.3, 0.3, entree))
        if u_j > 0.01:
            bonhomme(c, X_C, respire(melange(STAND, CHEER, prog(t, T_GLOIRE - 0.05, 0.4, lambda v: rebond(v, 1.3))), t), 1, "hayden-jaune", alpha=u_j, taille=0.85)
            etiquette(c, X_C, 1338, "HAYDEN", u_j, taille=34)
        u_p = prog(t, T_HEROES - 0.1, 0.6, sortie) * (1 - prog(t, T_MONDE - 0.3, 0.35, entree))
        if u_p > 0.01:
            photo_plein(c, t, "claire-plein", u_p, u_p, y=130, h=1000, zoom=1.0, fy=0.3, legende="CLAIRE · HEROES")
        if t >= T_MONDE - 0.3:
            u_c = prog(t, T_MONDE - 0.3, 0.45, sortie)
            cheer = prog(t, T_SAUVEZ - 0.05, 0.4, lambda v: rebond(v, 1.3))
            h = bonhomme(c, X_C, respire(melange(STAND, CHEER, cheer), t), 1, "hayden-jaune", u=u_c)
            etiquette(c, X_C, 1338, "HAYDEN · 17 ANS", u_c, taille=34)
            if t >= T_SAUVEZ - 0.05:
                chiffre_geant(c, "SAUVEZ LA POM-POM GIRL,", 540, 300, t, T_SAUVEZ - 0.05, 72, BLANC)
            if t >= T_SAUVEZ2 - 0.05:
                chiffre_geant(c, "SAUVEZ LE MONDE.", 540, 400, t, T_SAUVEZ2 - 0.05, 84, ROUGE)


# ═════════════════════════════ S5 — paparazzis, la pilule
def s5(c, t):
    a = fondu(t, T_MAIS, T_25)
    if a <= 0.01: return
    with Calque(c, a):
        u_h = prog(t, T_MAIS, 0.4, sortie)
        down = prog(t, T_PAPARAZZIS, 0.6, douce) * (1 - prog(t, T_ATTACHEE - 0.2, 0.4, douce))
        dx = secousse_x(t, T_PILULE + 0.3, 6, 0.6)
        h = bonhomme(c, X_C + dx, respire(melange(STAND, HEAD_DOWN, down), t), 1, "hayden-jaune", u=u_h)
        etiquette(c, X_C, 1338, "HAYDEN", u_h, taille=34)
        # deux paparazzis sans visage, petits, qui flashent
        u_pp = prog(t, T_PAPARAZZIS - 0.1, 0.4, sortie) * (1 - prog(t, T_TAPIS, 0.4, entree))
        if u_pp > 0.01:
            for k, (xx, f) in enumerate(((140, 1), (880, -1))):
                pp = bonhomme(c, xx, respire(PHONE, t + k), f, None, "severe", alpha=u_pp, taille=0.7)
                for j in range(4):
                    flash(c, pp["main_d"][0] + f * 30, pp["main_d"][1] - 20, t, T_PAPARAZZIS + 0.2 + j * 0.55 + k * 0.27, 70)
        # le tapis rouge : une bande rouge au sol
        u_tr = prog(t, T_TAPIS - 0.05, 0.5, sortie)
        if u_tr > 0.01:
            rrect(c, 60, SOL + 6, (W - 120) * u_tr, 22, 4, ROUGE, 0.9)
        # l'attachée de presse donne la pilule
        u_a = prog(t, T_ATTACHEE - 0.1, 0.45, sortie)
        if u_a > 0.01:
            tend = prog(t, T_PILULE - 0.4, 0.5, sortie)
            at = bonhomme(c, X_D + 60, respire(melange(STAND, POINT, tend), t + 1), -1, None, "neutre", u=u_a)
            etiquette(c, X_D + 60, 1338, "ATTACHÉE DE PRESSE", u_a, taille=30)
            if t >= T_PILULE - 0.3:
                v = prog(t, T_PILULE, 0.5, entreeSortie)
                ax, ay = at["main_d"]; bx, by = h["main_d"]
                pilule(c, mix(ax, bx, v), mix(ay, by, v) - 60 * math.sin(math.pi * v), 70)
        if t >= T_COMMENCE - 0.05:
            chiffre_geant(c, "TOUT A COMMENCÉ LÀ", 540, 320, t, T_COMMENCE - 0.05, 88, BLANC)


# ═════════════════════════════ S6 — maman, l'effondrement, la garde, la visio
def s6(c, t):
    a = fondu(t, T_25, T_PUIS)
    if a <= 0.01: return
    with Calque(c, a):
        u_h = prog(t, T_25, 0.4, sortie)
        eff = prog(t, T_EFFONDRE - 0.05, 0.7, douce)
        p = respire(melange(STAND, HEAD_DOWN, eff), t)
        if t >= T_VISIO - 0.2:
            p = respire(melange(HEAD_DOWN, PHONE, prog(t, T_VISIO - 0.2, 0.5, sortie)), t)
        h = bonhomme(c, X_G, p, 1, "hayden", u=u_h)
        etiquette(c, X_G, 1338, "HAYDEN · 25 ANS", u_h, taille=34)
        if T_EFFONDRE + 0.3 <= t < T_PERE:
            larmes(c, h, t, T_EFFONDRE + 0.3)
        for k, (txt, t0) in enumerate((("DÉPRESSION", T_DEPRESSION), ("ALCOOL", T_ALCOOL))):
            u = prog(t, t0 - 0.05, 0.3, lambda v: rebond(v, 1.4)) * (1 - prog(t, T_GARDE - 0.3, 0.3, entree))
            if u > 0: etiquette(c, X_G, 300 + k * 95, txt, u, taille=44)
        # la petite : elle apparaît à côté de sa mère, puis marche vers son père sur « la garde »
        u_k = prog(t, T_MAMAN - 0.1, 0.45, lambda v: rebond(v, 1.3))
        if u_k > 0.01:
            x0, x1 = X_G + 215, X_D - 190
            v = prog(t, T_GARDE - 0.3, 1.2, lin)
            xk = mix(x0, x1, v)
            pk = pose_marche(t - (T_GARDE - 0.3), (x1 - x0) / 1.2) if 0 < v < 1 else STAND
            kid = bonhomme(c, xk, respire(pk, t + 3, 0.5), 1, None, "neutre", u=u_k, taille=0.38)
        u_p = prog(t, T_PERE - 0.1, 0.45, sortie)
        if u_p > 0.01:
            pere = bonhomme(c, X_D, respire(melange(STAND, POINT, prog(t, T_PERE + 0.3, 0.4, sortie) * (1 - prog(t, T_ACCEPTE, 0.4, douce))), t + 1), -1, None, "severe", u=u_p)
            etiquette(c, X_D, 1338, "LE PÈRE", u_p, taille=34)
        if t >= T_VISIO - 0.1:
            u_v = prog(t, T_VISIO - 0.1, 0.4, sortie)
            def ecran(c, x, y, w, h_):
                bonhomme(c, x + w / 2, STAND, 1, None, "neutre", sol=y + h_ - 14, taille=0.2, ep=6)
            telephone_main(c, h, t, u_v, 1.0, ecran)


# ═════════════════════════════ S7 — l'homme, la prison, le frère
def s7(c, t):
    a = fondu(t, T_PUIS, T_ANNEE)
    if a <= 0.01: return
    with Calque(c, a):
        u_h = prog(t, T_PUIS, 0.4, sortie)
        dx = secousse_x(t, T_FRAPPE - 0.02, 18, 0.6)
        down = prog(t, T_FRAPPE - 0.05, 0.5, douce)
        h = bonhomme(c, X_G + dx, respire(melange(STAND, HEAD_DOWN, down), t), 1, "hayden", u=u_h)
        etiquette(c, X_G, 1338, "HAYDEN", u_h, taille=34)
        # l'homme : il arrive, lève le bras, puis les barreaux tombent devant lui
        u_m = prog(t, T_HOMME - 0.1, 0.45, sortie) * (1 - prog(t, T_2023 - 0.1, 0.35, entree))
        if u_m > 0.01:
            lev = prog(t, T_FRAPPE - 0.45, 0.4, sortie) * (1 - prog(t, T_FRAPPE + 0.3, 0.4, douce))
            m = bonhomme(c, X_D, respire(melange(STAND, WAVE, lev), t + 1), -1, None, "severe", alpha=u_m)
            etiquette(c, X_D, 1338, "L'HOMME", u_m, taille=34)
            if t >= T_PRISON - 0.1:
                barreaux(c, X_D, 900, 300, 800, prog(t, T_PRISON - 0.1, 0.45, sortie), 5, u_m)
        if t >= T_FRAPPE - 0.02 and t < T_FRAPPE + 0.35:
            c.drawRect(skia.Rect.MakeWH(W, H), peinture(ROUGE, 0.35 * (1 - (t - T_FRAPPE + 0.02) / 0.37)))
        # le frère : à droite, puis il s'efface et il reste 28 ANS
        u_f = prog(t, T_FRERE - 0.2, 0.45, sortie) * (1 - prog(t, T_MEURT + 0.1, 0.8, douce))
        if u_f > 0.01:
            fr = bonhomme(c, X_D, respire(STAND, t + 2), -1, None, "neutre", alpha=u_f)
            etiquette(c, X_D, 1338, "JANSEN, SON FRÈRE", u_f, taille=30)
        if t >= T_2023 - 0.05:
            chiffre_geant(c, "2023", 540, 300, t, T_2023 - 0.05, 110, BLANC)
        if t >= T_28 - 0.05:
            chiffre_geant(c, "28 ANS", 540, 420, t, T_28 - 0.05, 100, ROUGE)


# ═════════════════════════════ S8 — le livre, l'espoir
def s8(c, t):
    a = fondu(t, T_ANNEE, T_TROIS)
    if a <= 0.01: return
    with Calque(c, a):
        u_h = prog(t, T_ANNEE, 0.4, sortie)
        h = bonhomme(c, X_C, respire(melange(STAND, TALK, prog(t, T_ECRIT - 0.1, 0.4, sortie)), t), 1, "hayden", u=u_h)
        etiquette(c, X_C, 1338, "HAYDEN · 2026", u_h, taille=34)
        if t >= T_LIVRE - 0.1:
            bx, by = h["main_g"]
            livre(c, bx - 20, by - 70, 110, prog(t, T_LIVRE - 0.1, 0.4, lambda v: rebond(v, 1.3)))
        if T_PASSE - 0.05 <= t < T_ESPOIR - 0.1:
            bulle(c, h, "J'AI ACCEPTÉ MON PASSÉ", t, T_PASSE - 0.05, 1, 40, alpha=1 - prog(t, T_ESPOIR - 0.3, 0.2, entree))
        elif t >= T_ESPOIR - 0.05:
            bulle(c, h, "J'AI DE L'ESPOIR", t, T_ESPOIR - 0.05, 1, 44)


# ═════════════════════════════ S9 — trois mois plus tard : le cercle vide
def s9(c, t):
    a = fondu(t, T_TROIS, T_SIGN + 0.3)
    if a <= 0.01: return
    with Calque(c, a):
        u_h = prog(t, T_TROIS, 0.4, sortie)
        gris = prog(t, T_RETROUVE - 0.2, 0.8, douce)
        eff = prog(t, T_SANSVIE, 1.2, douce)
        if eff < 0.999:
            bonhomme(c, X_C, respire(STAND, t, 1 - eff), 1, "hayden", u=u_h, alpha=1 - eff, gris=gris)
        bonhomme(c, X_C, STAND, 1, "hayden", seulement_anneau=True, alpha=prog(t, T_SANSVIE, 0.6, sortie))
        etiquette(c, X_C, 1338, "HAYDEN", u_h * (1 - eff), taille=34)
        if t >= T_CAROLINE - 0.05:
            etiquette(c, 540, 1180, "CAROLINE DU SUD · 16 AOÛT", prog(t, T_CAROLINE - 0.05, 0.3, sortie) * (1 - prog(t, T_FILLE, 0.3, entree)), taille=34, rouge=False)
        if t >= T_FILLE - 0.05:
            chiffre_geant(c, "ELLE NE POUVAIT PAS MOURIR", 540, 280, t, T_FILLE - 0.05, 74, BLANC)
            if t >= T_ECRAN - 0.05:
                chiffre_geant(c, "À L'ÉCRAN.", 540, 370, t, T_ECRAN - 0.05, 74, BLANC)
        if t >= T_SAUVEE - 0.05:
            chiffre_geant(c, "PERSONNE NE L'A SAUVÉE.", 540, 1180, t, T_SAUVEE - 0.05, 72, ROUGE)


# ═════════════════════════════ sons
son(0.02, "impact_doux", -9)
son(T_SAUVE - 0.05, "ding", -12)
son(T_PERSONNE - 0.05, "whoosh_bas", -12)
son(T_HIER, "whoosh_long", -11)
son(T_ACCIDENT - 0.05, "impact_doux", -9)
son(T_36 - 0.05, "impact", -8)
son(T_PUB, "whoosh_court", -12)
son(T_ONZE - 0.1, "pop", -13); son(T_FEUILLETON - 0.05, "clic", -13)
son(T_DENZEL - 0.5, "swipe", -13)
son(T_ENFANCE - 0.05, "whoosh_bas", -12)
son(T_MERE - 0.1, "swipe", -13); son(T_MANAGER - 0.05, "pop", -13)
son(T_17, "whoosh_court", -12)
son(T_HEROES - 0.1, "verre", -11)
son(T_SAUVEZ - 0.05, "impact_doux", -9); son(T_SAUVEZ2 - 0.05, "impact", -8)
son(T_MAIS, "whoosh_court", -12)
for j in range(4):
    son(T_PAPARAZZIS + 0.2 + j * 0.55, "clic", -11); son(T_PAPARAZZIS + 0.47 + j * 0.55, "clic", -12)
son(T_ATTACHEE - 0.1, "swipe", -13)
son(T_PILULE, "blip", -12)
son(T_COMMENCE - 0.05, "impact_doux", -9)
son(T_25, "whoosh_court", -12)
son(T_MAMAN - 0.1, "pop", -13)
son(T_EFFONDRE - 0.05, "whoosh_bas", -11)
son(T_DEPRESSION - 0.05, "clic", -12); son(T_ALCOOL - 0.05, "clic", -12)
son(T_PERE - 0.1, "swipe", -13)
son(T_GARDE - 0.3, "tick", -13)
son(T_VISIO - 0.1, "pop", -13)
son(T_PUIS, "whoosh_court", -12)
son(T_FRAPPE - 0.02, "impact", -6)
son(T_PRISON - 0.1, "tampon", -10)
son(T_2023 - 0.05, "whoosh_bas", -12)
son(T_MEURT, "whoosh_long", -13)
son(T_28 - 0.05, "impact_doux", -9)
son(T_ANNEE, "whoosh_court", -12)
son(T_LIVRE - 0.1, "pop", -12)
son(T_PASSE - 0.05, "pop", -13); son(T_ESPOIR - 0.05, "ding", -12)
son(T_TROIS, "whoosh_long", -11)
son(T_SANSVIE, "whoosh_bas", -10)
son(T_FILLE - 0.05, "impact_doux", -9)
son(T_SAUVEE - 0.05, "impact", -7)
sons_signature_people(son, T_SIGN)

for a_, b_ in [(T_SIGN + 0.4, T_SIGN + 0.9)]:
    rapide(a_, b_)


# ═════════════════════════════ composition
def fond(c, t):
    fond_bonhomme(c, t)


def dessine(c, t):
    fond(c, t)
    s1(c, t); s2(c, t); s3(c, t); s4(c, t); s5(c, t); s6(c, t); s7(c, t); s8(c, t); s9(c, t)
    if t >= T_SIGN - 0.12:
        signature_people(c, t, T_SIGN, MEDIAS)
    filigrane(c, 0.26 * (1 - prog(t, T_SIGN - 0.2, 0.2, entree)))
    K.dessine_eclairs(c, t)
    if t < T_SIGN - 0.02:
        SOUS.dessine(c, t, BLANC)
