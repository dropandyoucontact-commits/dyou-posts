"""AC-M05 — RECTO CERVEAU. Hanouna / Obispo : la réconciliation du 28/10/2026 sur W9.

PREMIÈRE VIDÉO DU FORMAT « BONHOMME » (29/10/2026). Youssef : « notre format visuel n'accroche
pas et en plus il met trop de temps à produire, faut aller plus simple… un bonhomme animé 2D,
quand tu parles de quelqu'un tu peux animer un bonhomme. »
→ `moteur/bonhomme.py` : rig articulé (cinématique directe/inverse, marche sans glissement),
   tête = vraie photo dans un disque cerclé de rouge, bulles, étiquettes, accessoires en formes.
   Plus de pièce 3D, plus de grille, plus de pavés : noir, un sol, des bonhommes, le sous-titre.

Sujet vérifié (Télé-Loisirs / programme-tv.net du 28/10/2026, Closer) :
  - 27/08/2026 : concert caritatif à l'Arkéa Arena de Bordeaux pour les sinistrés des incendies
    de l'été (initiative Pascal Obispo + Julien Courbet ; Zazie, Gaëtan Roussel, Gauvain Sers,
    Julien Clerc, Renaud…). Diffusé sur M6 grâce à Hanouna, qui a assumé les coûts de production.
  - Obispo n'a pas cité Hanouna dans ses remerciements ; Gilles Verdez l'a relevé dans
    « Tout beau, tout neuf » (W9) ; Hanouna « agacé », « mots forts » pendant plusieurs jours.
  - Mercredi 28/10 : Obispo invité surprise sur le plateau. « oublis maladroits… non intentionnels,
    je tenais à te le dire les yeux dans les lunettes » ; « tu as dit oui en trois secondes et
    demi » ; « tu as aidé… à rapporter 1,7 million d'euros ». Cadeau : un casque de pompier venu
    de Bordeaux. Hanouna : « Ça me touche de fou, tu es un amour. »

Grammaire du format : UN mouvement à la fois. Un bonhomme entre en marchant, l'autre est déjà là.
Les bulles disent ce que la voix cite, pas plus. Les chiffres en géant, une fois chacun.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import rayons
from bonhomme import *
import bonhomme as B

K = Kit(P, 1.0)
B.SENS_PHOTO.update(hanouna=-1, obispo=1)      # sur la photo du plateau, Cyril regarde à gauche, Pascal à droite
DUREE = round(K.timing["duree_voix"] + 3.4, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
NB_IMAGES = K.nb_images
SFX = K.SFX
TW = K.TW; son = K.son; rapide = K.rapide; flou_a = K.flou_a

SOUS = sous_titres_bonhomme(K)
MEDIAS = ()

# ═════════════════════════════ repères (indices de timing.json)
T_MOTS, T_DURS, T_JOURS, T_HIER, T_DEBARQUE, T_PREVENIR = TW(5), TW(7), TW(11), TW(15), TW(19), TW(24)
T_ETE, T_INCENDIES, T_OBISPO2, T_COURBET, T_CONCERT = TW(25), TW(29), TW(34), TW(37), TW(41)
T_ZAZIE, T_RENAUD, T_CLERC, T_PRESENT = TW(45), TW(46), TW(47), TW(49)
T_MAIS, T_CHER, T_APPELLE, T_HANOUNA3, T_OUI, T_PAIE, T_M6, T_RESULTAT, T_MILLION = TW(54), TW(58), TW(64), TW(65), TW(69), TW(76), TW(82), TW(87), TW(88)
T_SAUF, T_REMERCIE, T_SAUFCYRIL, T_CYRIL2 = TW(96), TW(103), TW(110), TW(111)
T_VERDEZ, T_TRAHI, T_ENERVE, T_MOTS2, T_PLUSIEURS = TW(112), TW(118), TW(123), TW(128), TW(134)
T_HIER2, T_ENTRE, T_NEUF, T_REGARDE, T_OUBLI, T_SANS, T_GRACE = TW(137), TW(140), TW(149), TW(150), TW(160), TW(166), TW(172)
T_PUIS, T_CASQUE, T_BORDEAUX, T_CRAQUE, T_TOUCHE, T_AMOUR = TW(180), TW(186), TW(191), TW(193), TW(195), TW(200)
T_DEUX, T_RECONC, T_VOUS = TW(204), TW(216), TW(221)
T_FIN = K.timing["duree_voix"]
T_SIGN = T_FIN + 0.3

X_G, X_D = 330, 720            # les deux places : à gauche face à droite, à droite face à gauche
X_HORS = 1180                   # hors champ, à droite


def fondu(t, a, b, d=0.35):
    """1 entre a et b, avec entrée et sortie douces"""
    return prog(t, a, d, sortie) * (1 - prog(t, b - d, d, entree))


def marche_vers(t, t0, x0, x1, duree):
    """x de la hanche et pose pendant une marche de x0 à x1 entre t0 et t0+duree, puis debout"""
    if t < t0: return x0, pose_marche(0.0, 0.0), 0.0
    if t > t0 + duree: return x1, STAND, 1.0
    u = (t - t0) / duree
    x = mix(x0, x1, u)
    v = abs(x1 - x0) / duree
    return x, pose_marche(t - t0, v), 0.0


# ═════════════════════════════ S1 — le hook : Cyril seul, Obispo débarque
def s1(c, t):
    a = fondu(t, -1, T_ETE)
    if a <= 0.01: return
    with Calque(c, a):
        # Cyril : debout puis il pointe le vide à droite, et tremble sur « durs »
        u_p = prog(t, 0.0, 0.5, sortie)
        p = respire(melange(STAND, POINT, u_p), t)
        dx = secousse_x(t, T_DURS - 0.05, 10, 0.45)
        cy = bonhomme(c, X_G + dx, p, 1, "hanouna", u=1.0)
        etiquette(c, X_G, 1338, "CYRIL", prog(t, TW(1) - 0.05, 0.3, sortie), taille=34)
        if T_MOTS - 0.05 <= t < T_HIER + 0.2:
            bulle(c, cy, "!!!", t, T_MOTS - 0.05, 1, 60, rouge=ROUGE, alpha=1 - prog(t, T_HIER, 0.2, entree))
        # Obispo arrive en marchant depuis la droite, sur « débarqué… sans prévenir »
        if t >= T_HIER - 0.1:
            x, po, fin = marche_vers(t, T_HIER, X_HORS, X_D, T_PREVENIR - T_HIER - 0.1)
            if fin: po = respire(melange(STAND, TALK, prog(t, T_PREVENIR, 0.4, sortie)), t + 1)
            ob = bonhomme(c, x, po, -1, "obispo")
            etiquette(c, X_D, 1338, "OBISPO", prog(t, T_PREVENIR - 0.1, 0.3, sortie), taille=34)
        rubrique(c, t, prog(t, T_JOURS, 0.4, sortie), "HANOUNA · OBISPO", "RÉCONCILIATION")


# ═════════════════════════════ S2 — l'été, le concert, les artistes
def s2(c, t):
    a = fondu(t, T_ETE, T_MAIS)
    if a <= 0.01: return
    with Calque(c, a):
        titre(c, "ÉTÉ 2026", 300, 110, t, T_ETE + 0.1, rouge=True, alpha=1 - prog(t, T_ZAZIE - 0.3, 0.3, entree))
        if t >= T_INCENDIES - 0.1:
            flammes(c, t, SOL - 4, 60, 1000, 9, 150, prog(t, T_INCENDIES - 0.1, 0.5, sortie) * (1 - prog(t, T_CONCERT - 0.2, 0.4, entree)))
        # Obispo pense au concert
        u_o = prog(t, T_OBISPO2 - 0.1, 0.4, sortie)
        if u_o > 0:
            cheer = prog(t, T_PRESENT - 0.05, 0.4, lambda v: rebond(v, 1.3))
            po = respire(melange(melange(STAND, THINK, prog(t, T_CONCERT - 0.1, 0.4, sortie)), CHEER, cheer), t)
            ob = bonhomme(c, X_G, po, 1, "obispo", u=u_o)
            etiquette(c, X_G, 1338, "OBISPO", u_o, taille=34)
            if T_CONCERT - 0.05 <= t < T_ZAZIE + 0.2:
                pensee(c, ob, "UN CONCERT", t, T_CONCERT - 0.05, 1, 44, alpha=1 - prog(t, T_ZAZIE, 0.2, entree))
        u_c = prog(t, T_COURBET - 0.1, 0.4, sortie)
        if u_c > 0:
            cheer = prog(t, T_PRESENT + 0.05, 0.4, lambda v: rebond(v, 1.3))
            pc = respire(melange(STAND, CHEER, cheer), t + 0.7)
            co = bonhomme(c, X_D, pc, -1, None, "neutre", u=u_c)
            etiquette(c, X_D, 1338, "COURBET", u_c, taille=34)
        # les artistes répondent présent : trois noms qui se posent à droite, en haut
        for k, (txt, t0) in enumerate((("ZAZIE", T_ZAZIE), ("RENAUD", T_RENAUD), ("JULIEN CLERC", T_CLERC))):
            u = prog(t, t0 - 0.05, 0.3, lambda v: rebond(v, 1.4))
            if u > 0:
                etiquette(c, 540, 300 + k * 95, txt, u, taille=42, rouge=False)


# ═════════════════════════════ S3 — l'appel, le oui, la production, M6, 1,7 million
def s3(c, t):
    a = fondu(t, T_MAIS, T_SAUF)
    if a <= 0.01: return
    with Calque(c, a):
        u_o = prog(t, T_MAIS, 0.4, sortie)
        tel = prog(t, T_APPELLE - 0.1, 0.4, sortie)
        po = respire(melange(STAND, PHONE, tel), t)
        ob = bonhomme(c, X_G, po, 1, "obispo", u=u_o)
        etiquette(c, X_G, 1338, "OBISPO", u_o, taille=34)
        if T_CHER - 0.05 <= t < T_APPELLE:
            pensee(c, ob, ["ÇA COÛTE", "CHER…"], t, T_CHER - 0.05, 1, 44)
        u_c = prog(t, T_HANOUNA3 - 0.05, 0.4, sortie)
        if u_c > 0:
            pc = respire(melange(PHONE, CHEER if t >= T_OUI else PHONE, prog(t, T_OUI - 0.05, 0.3, lambda v: rebond(v, 1.3))), t + 0.5)
            if t >= T_PAIE - 0.1:
                pc = respire(melange(CHEER, POINT, prog(t, T_PAIE - 0.1, 0.4, sortie)), t + 0.5)
            cy = bonhomme(c, X_D, pc, -1, "hanouna", u=u_c)
            etiquette(c, X_D, 1338, "CYRIL", u_c, taille=34)
            if T_OUI - 0.05 <= t < T_PAIE:
                bulle(c, cy, "OUI !", t, T_OUI - 0.05, 1, 64, rouge=ROUGE)
            if t >= T_PAIE:
                billets(c, cy["main_d"][0] - 40, cy["main_d"][1] + 20, 90, t, T_PAIE, 5)
        # la télé : le concert passe sur M6
        if t >= T_M6 - 0.15:
            u_t = prog(t, T_M6 - 0.15, 0.45, sortie) * (1 - prog(t, T_RESULTAT - 0.1, 0.3, entree))
            if u_t > 0.01:
                c.save(); c.translate(0, 0)
                tele(c, 540, 290, 540, 300, t, None, u_t, u_t)
                texte(c, "M6", 540, 232, 110, BLANC, "noir", "centre", -0.03, u_t)
                c.restore()
        if t >= T_RESULTAT:
            chiffre_geant(c, "1,7 MILLION €", 540, 300, t, T_MILLION - 0.05, 150, ROUGE)
            u2 = prog(t, TW(92) - 0.05, 0.3, sortie)
            if u2 > 0: texte(c, "POUR LES SINISTRÉS", 540, 400, 44, BLANC, "noir", "centre", 0.02, u2)


# ═════════════════════════════ S4 — les remerciements, sauf Cyril
def s4(c, t):
    a = fondu(t, T_SAUF, T_VERDEZ)
    if a <= 0.01: return
    with Calque(c, a):
        u_o = prog(t, T_SAUF, 0.4, sortie)
        po = respire(melange(STAND, TALK, prog(t, T_REMERCIE - 0.1, 0.4, sortie)), t)
        ob = bonhomme(c, X_G, po, 1, "obispo", u=u_o)
        etiquette(c, X_G, 1338, "OBISPO", u_o, taille=34)
        if t >= T_REMERCIE - 0.05:
            bulle(c, ob, ["MERCI ZAZIE,", "MERCI RENAUD,", "MERCI À TOUS…"], t, T_REMERCIE - 0.05, -1, 42)
        u_c = prog(t, T_SAUFCYRIL - 0.05, 0.4, sortie)
        if u_c > 0:
            cy = bonhomme(c, X_D, respire(SHRUG, t), -1, "hanouna", u=u_c, gris=0.85)
            etiquette(c, X_D, 1338, "CYRIL", u_c, taille=34)
            points_interrogation(c, cy, t, T_CYRIL2 - 0.05)


# ═════════════════════════════ S5 — Verdez le remarque, Hanouna s'énerve
def s5(c, t):
    a = fondu(t, T_VERDEZ, T_HIER2)
    if a <= 0.01: return
    with Calque(c, a):
        u_v = prog(t, T_VERDEZ, 0.4, sortie) * (1 - prog(t, T_ENERVE, 0.4, entree))
        if u_v > 0.01:
            ve = bonhomme(c, X_G, respire(melange(STAND, POINT, prog(t, T_VERDEZ + 0.3, 0.4, sortie)), t), 1, None, "severe", u=1.0, alpha=u_v)
            etiquette(c, X_G, 1338, "VERDEZ", u_v, taille=34)
        u_c = prog(t, T_VERDEZ, 0.4, sortie)
        dx = secousse_x(t, T_ENERVE - 0.05, 16, 0.7) + secousse_x(t, T_MOTS2 - 0.05, 12, 0.6)
        pc = respire(melange(CROSSED, CHEER, prog(t, T_ENERVE - 0.05, 0.3, lambda v: rebond(v, 1.3))), t)
        if t >= T_MOTS2 - 0.1: pc = respire(melange(CHEER, POINT, prog(t, T_MOTS2 - 0.1, 0.35, sortie)), t)
        cy = bonhomme(c, X_D + dx, pc, -1, "hanouna", u=u_c)
        etiquette(c, X_D, 1338, "CYRIL", u_c, taille=34)
        if T_TRAHI - 0.05 <= t < T_MOTS2 - 0.1:
            bulle(c, cy, "TRAHI", t, T_TRAHI - 0.05, 1, 60, rouge=ROUGE, alpha=1 - prog(t, T_MOTS2 - 0.3, 0.2, entree))
        if t >= T_MOTS2 - 0.05:
            bulle(c, cy, "@#%! !!!", t, T_MOTS2 - 0.05, 1, 60, rouge=ROUGE)
        if t >= T_PLUSIEURS - 0.05:
            chiffre_geant(c, "PLUSIEURS JOURS", 540, 330, t, T_PLUSIEURS - 0.05, 96, BLANC)


# ═════════════════════════════ S6 — hier soir : Obispo entre, s'explique
def s6(c, t):
    a = fondu(t, T_HIER2, T_PUIS)
    if a <= 0.01: return
    with Calque(c, a):
        titre(c, "HIER SOIR", 300, 110, t, T_HIER2, rouge=True, alpha=1 - prog(t, T_REGARDE, 0.4, entree))
        u_c = prog(t, T_HIER2, 0.4, sortie)
        cy = bonhomme(c, X_G, respire(STAND, t), 1, "hanouna", u=u_c)
        etiquette(c, X_G, 1338, "CYRIL", u_c, taille=34)
        if t >= T_ENTRE - 0.1:
            x, po, fin = marche_vers(t, T_ENTRE, X_HORS, X_D, T_NEUF - T_ENTRE)
            if fin: po = respire(melange(STAND, TALK, prog(t, T_REGARDE, 0.4, sortie)), t + 1)
            ob = bonhomme(c, x, po, -1, "obispo")
            etiquette(c, X_D, 1338, "OBISPO", prog(t, T_NEUF - 0.1, 0.3, sortie), taille=34)
            if T_OUBLI - 0.05 <= t < T_SANS - 0.1:
                bulle(c, ob, ["C'ÉTAIT UN OUBLI,", "PAS UNE TRAHISON"], t, T_OUBLI - 0.05, 1, 42, alpha=1 - prog(t, T_SANS - 0.3, 0.2, entree))
            elif T_SANS - 0.05 <= t < T_GRACE - 0.1:
                bulle(c, ob, ["SANS TOI,", "RIEN N'AURAIT EXISTÉ"], t, T_SANS - 0.05, 1, 42, alpha=1 - prog(t, T_GRACE - 0.3, 0.2, entree))
            elif t >= T_GRACE - 0.05:
                bulle(c, ob, "C'EST GRÂCE À TOI", t, T_GRACE - 0.05, 1, 42)


# ═════════════════════════════ S7 — le casque de pompier, Hanouna craque
def s7(c, t):
    a = fondu(t, T_PUIS, T_DEUX)
    if a <= 0.01: return
    with Calque(c, a):
        u = prog(t, T_PUIS, 0.4, sortie)
        # Obispo tend le casque, puis il est sur la tête de Cyril
        tend = prog(t, T_CASQUE - 0.1, 0.5, sortie)
        ob = bonhomme(c, X_D, respire(melange(TALK, POINT, tend), t + 1), -1, "obispo", u=u)
        etiquette(c, X_D, 1338, "OBISPO", u, taille=34)
        cy = bonhomme(c, X_G, respire(melange(STAND, CHEER, prog(t, T_CRAQUE - 0.05, 0.4, lambda v: rebond(v, 1.3))), t), 1, "hanouna", u=u)
        etiquette(c, X_G, 1338, "CYRIL", u, taille=34)
        if t >= T_CASQUE - 0.1:
            v = prog(t, T_BORDEAUX + 0.1, 0.6, entreeSortie)
            hx, hy = ob["main_d"]
            tx, ty = cy["tete"]
            x = mix(hx, tx, v); y = mix(hy - 30, ty - cy["r"] - 10, v) - 160 * math.sin(math.pi * v)
            casque(c, x, y, 190 * mix(0.7, 1.0, v), prog(t, T_CASQUE - 0.1, 0.3, sortie), rot=mix(0, -8, v))
        if t >= T_CRAQUE:
            coeurs(c, cy, t, T_CRAQUE, 7)
        if T_TOUCHE - 0.05 <= t < T_AMOUR - 0.1:
            bulle(c, cy, "ÇA ME TOUCHE DE FOU", t, T_TOUCHE - 0.05, -1, 42, alpha=1 - prog(t, T_AMOUR - 0.3, 0.2, entree))
        elif t >= T_AMOUR - 0.05:
            bulle(c, cy, "TU ES UN AMOUR", t, T_AMOUR - 0.05, -1, 42)


# ═════════════════════════════ S8 — deux amis, la question
def s8(c, t):
    a = fondu(t, T_DEUX, T_SIGN + 0.3)
    if a <= 0.01: return
    with Calque(c, a):
        u = prog(t, T_DEUX, 0.4, sortie)
        # ils marchent l'un vers l'autre et se serrent la main sur « réconcilient »
        v = prog(t, T_RECONC - 1.2, 1.1, sortie)
        xg, xd = mix(X_G, 390, v), mix(X_D, 690, v)
        if 0 < v < 1:
            pg = pose_marche(t - (T_RECONC - 1.2), (390 - X_G) / 1.1)
            pd = pose_marche(t - (T_RECONC - 1.2), (X_D - 690) / 1.1)
        else:
            s = prog(t, T_RECONC - 0.1, 0.4, sortie) if v >= 1 else 0.0
            pg = respire(melange(STAND, SHAKE, s), t); pd = respire(melange(STAND, SHAKE, s), t + 1)
        cy = bonhomme(c, xg, pg, 1, "hanouna", u=u)
        ob = bonhomme(c, xd, pd, -1, "obispo", u=u)
        if t >= T_RECONC:
            coeur(c, 540, 470 - 40 * prog(t, T_RECONC, 0.6, sortie), 30, ROUGE, prog(t, T_RECONC, 0.3, sortie))
        if t >= T_VOUS - 0.05:
            chiffre_geant(c, "VOUS AURIEZ PARDONNÉ ?", 540, 330, t, T_VOUS - 0.05, 90, BLANC)


# ═════════════════════════════ sons — sobres
son(0.02, "impact_doux", -9)
son(T_MOTS - 0.05, "pop", -12)
son(T_HIER, "swipe", -13)
son(T_PREVENIR - 0.1, "impact_doux", -10)
son(T_ETE, "whoosh_court", -12)
son(T_INCENDIES - 0.1, "whoosh_bas", -12)
son(T_CONCERT - 0.05, "pop", -13)
for t0 in (T_ZAZIE, T_RENAUD, T_CLERC): son(t0 - 0.05, "clic", -12)
son(T_PRESENT - 0.05, "ding", -12)
son(T_APPELLE - 0.1, "blip", -13)
son(T_OUI - 0.05, "pop", -10)
son(T_PAIE, "swipe", -12)
son(T_M6 - 0.15, "whoosh_court", -12)
son(T_MILLION - 0.05, "ching", -8)
son(T_REMERCIE - 0.05, "pop", -13)
son(T_CYRIL2 - 0.05, "blip", -12)
son(T_TRAHI - 0.05, "impact_doux", -9)
son(T_ENERVE - 0.05, "impact", -8)
son(T_PLUSIEURS - 0.05, "whoosh_court", -12)
son(T_HIER2, "whoosh_long", -11)
son(T_ENTRE, "swipe", -13)
son(T_OUBLI - 0.05, "pop", -13); son(T_SANS - 0.05, "pop", -13); son(T_GRACE - 0.05, "pop", -13)
son(T_CASQUE - 0.1, "verre", -11)
son(T_CRAQUE, "ding", -10)
son(T_TOUCHE - 0.05, "pop", -13)
son(T_RECONC, "ching", -10)
son(T_VOUS - 0.05, "impact_doux", -9)
sons_signature_people(son, T_SIGN)

for a_, b_ in [(T_SIGN + 0.4, T_SIGN + 0.9)]:
    rapide(a_, b_)


# ═════════════════════════════ composition
def fond(c, t):
    fond_bonhomme(c, t)


def dessine(c, t):
    fond(c, t)
    s1(c, t); s2(c, t); s3(c, t); s4(c, t); s5(c, t); s6(c, t); s7(c, t); s8(c, t)
    if t >= T_SIGN - 0.12:
        signature_people(c, t, T_SIGN, MEDIAS)
    filigrane(c, 0.26 * (1 - prog(t, T_SIGN - 0.2, 0.2, entree)))
    K.dessine_eclairs(c, t)
    if t < T_SIGN - 0.02:
        SOUS.dessine(c, t, BLANC)
