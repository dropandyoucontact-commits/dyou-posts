"""AC-M03 — RECTO CERVEAU. Matthew Perry, trois ans après, et ce que sa sœur raconte.

Habillage figé (moteur/people.py : fond noir, grille rouge, accent blanc). On part d'AC-M02.

NOUVELLE RÈGLE DE MONTAGE, posée par Youssef le 28/10/2026 après l'échec d'AC-M01 et AC-M02 :
  « les sous-titres etc, faut être moins dynamique. Pour notre format faut plus un truc où les
   gens soient immersés totalement, où ils peuvent suivre, où t'as calculé chaque mouvement
   et animation de façon à captiver le cerveau. »
Ce que ça change, concrètement, par rapport à AC-M02 :
  - 9 scènes au lieu de 12 : chaque plan reste 8 à 10 s, on a le temps de regarder ;
  - UN SEUL élément bouge à la fois. Quand un pavé arrive, le précédent est déjà parti ;
  - `effet="masque"` partout (plus de « ressort ») et un seul surlignage dans toute la vidéo ;
  - la grille avance à vitesse constante (0,42), trois accélérations douces au lieu de six ;
  - deux éclairs au lieu de onze, 21 bruitages au lieu de 51, aucun confetti ni éclat :
    le sujet est une mort, le montage ne fête rien.
Ce qui NE change pas : le hook est un visuel (règle du 28/10), l'attaque de voix est rapide
(6,04 mots/s sur les onze premiers mots), le reste tourne à 4,47 mots/s.

Voix : TOUF (`x5uzA0wWgLQFZXEL4MbL`), le clone de l'ancienne voix de @recto_cerveau,
validé par Youssef le 28/10. multilingual_v2, stabilité 0,50, style 0, similarité 1,0,
speaker boost désactivé — `voix.py --debit 4.3`.

Sujet vérifié à la source (USA TODAY du 27/10/2026 sur le documentaire Netflix
« The One About Matthew Perry », + bureau du médecin légiste du comté de Los Angeles) :
  - Perry meurt le 28/10/2023 à 54 ans, dans le jacuzzi de sa maison de Pacific Palisades.
    Mort classée ACCIDENTELLE par le médecin légiste.
  - Le documentaire en trois parties sort le 27/10/2026, la veille des trois ans.
    Sa sœur, Mia Perry Bowick, y parle ; les cinq autres acteurs de Friends n'y sont PAS.
  - Après la saison 2, accident de jet-ski, antidouleur prescrit, jusqu'à 55 cachets par jour,
    58 kilos (128 livres). Sa sœur : « il en prenait juste assez pour se sentir bien, mais pas
    assez pour paraître défoncé », et il gérait tremblements et manque entre deux prises.
  - Épisode du mariage de Monica et Chandler : la famille est venue sur le tournage, inquiète ;
    « la question qu'on se posait tous, c'était : est-ce que c'est SON mariage à lui ? »
  - 2018 : son côlon explose, 2 % de chances annoncées, deux semaines de coma, cinq mois
    d'hôpital, neuf mois de poche. Sa sœur trouve une figurine de Batman sous son lit.
  - ≈ 7 millions de dollars dépensés pour se soigner (lui disait 9 dans le NYT).
  - Cinq personnes ont plaidé coupable, dont son assistant Kenneth Iwamasa, qui vivait chez lui.
  - Enterrement en novembre 2023, cercueil ouvert : Aniston, Kudrow, Schwimmer, Le Blanc et Cox
    se sont approchés EN SE TENANT PAR LA MAIN, et ont pleuré.
  ÉCARTÉ VOLONTAIREMENT : le nom des substances. L'info est exacte sans elles (« un antidouleur
  très puissant », « mort classée accidentelle ») et TikTok modère la mention de drogues.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import lettres, entre, rayons
from people import *
import people

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 3.2, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = sous_titres_people(K, fusions={(8, 9): "Matthew Perry", (52, 53): "Matthew Perry",
                                      (135, 136, 137): "Monica et Chandler",
                                      (224, 225): "vingt-huit octobre,"})

V_CHANDLER = "videos/chandler"
V_PERRY = "videos/perry-2022"
V_MARIAGE = "videos/mariage"
V_FUNERAILLES = "videos/funerailles"
V_CAST = "videos/cast"
PH_SOEUR = "photos/soeur"
PH_SELFIE = "photos/perry-soeur"
MEDIAS = []

# ───────────────────────────── repères, tous accrochés à un mot
T_HOOK, T_JACUZZI, T_NETFLIX = TW(0), TW(10), TW(14)
T_SOEUR, T_PREMIERE, T_MENSONGES = TW(22), TW(28), TW(32)
T_SAISON2, T_JETSKI, T_MEDECINS, T_55, T_KILOS = TW(43), TW(52), TW(59), TW(67), TW(75)
T_METHODE, T_DOSAIT, T_JUSTE, T_PRISES, T_PERSONNE = TW(85), TW(91), TW(100), TW(111), TW(120)
T_MARIAGE, T_FAMILLE, T_TOUS, T_SEUL, T_VOULAIT = TW(128), TW(138), TW(149), TW(155), TW(165)
T_2018, T_2PCT, T_COMA, T_BATMAN, T_7M = TW(175), TW(182), TW(190), TW(198), TW(208)
T_MORT, T_ACCIDENT, T_CINQ, T_ASSISTANT = TW(218), TW(229), TW(235), TW(243)
T_ENTERREMENT, T_CERCUEIL, T_MAIN, T_AUCUN = TW(252), TW(262), TW(273), TW(283)
T_CTA, T_DISLE = TW(293), TW(302)
T_SIGN = round(K.timing["duree_voix"] - 0.05, 2)
T_FIN = DUREE


def vitesse_grille(t):
    """le décor avance à vitesse constante. Trois respirations seulement, douces : le mouvement
    de fond ne doit plus tirer l'œil à chaque phrase (règle du 28/10)."""
    v = 0.42
    for t0 in (T_HOOK, T_MARIAGE, T_ENTERREMENT):
        v += 1.1 * max(0.0, 1 - abs(t - t0) / 0.7) ** 2
    return v


def ondes_sol(c, t, t0, a=1.0, n=4, vitesse=0.55):
    """anneaux rouges qui montent du point de fuite vers nous, à même le sol"""
    if a <= 0.01: return
    for k in range(n):
        u = ((t - t0) * vitesse + k / n) % 1.0
        z = mix(7.0, 0.55, u ** 1.5)
        y = HORIZON + SOL / z
        rx = 1500 / z
        al = a * 0.5 * math.sin(math.pi * min(1.0, u * 1.08)) ** 0.7
        if y > H + 500 or al <= 0.01: continue
        c.drawOval(skia.Rect.MakeXYWH(AXE - rx, y - rx * 0.20, 2 * rx, 0.40 * rx),
                   peinture(ROUGE, al, Style=skia.Paint.kStroke_Style, StrokeWidth=4 + 18 * (1 - z / 7)))


# ═════════════════════════════ 1. HOOK — un visuel, et rien d'autre pendant 2,6 s
def hook(c, t):
    if t > T_SOEUR + 0.2: return
    sor = prog(t, T_SOEUR - 0.12, 0.3, entree)
    with Calque(c, 1 - sor):
        # image 0 : Chandler, plein cadre, qui arrive sur nous. Aucun texte.
        # À « mourait », il monte et le visage de 2022 arrive du point de fuite en dessous :
        # le avant / après est à l'écran avant qu'un seul mot ne soit écrit.
        arr = prog(t, -0.14, 0.34, sortieExpo)
        sp = prog(t, T_JACUZZI - 0.16, 0.52, sortieExpo)
        w1 = mix(1000, 900, sp); h1 = w1 * 0.5625
        carte_video(c, t, V_CHANDLER, AXE_HAUT - w1 / 2, mix(620, 300, sp), w1, h1,
                    borne(arr), t0=-1.6, z0=6.0)
        if sp > 0.01:
            carte_video(c, t, V_PERRY, AXE - 350, 930, 700, 394, sp, t0=T_JACUZZI - 0.14, z0=4.5)
        if t > T_NETFLIX - 0.12:
            bloc(c, "LE DOCUMENTAIRE SORT AUJOURD'HUI", AXE, 1330,
                 entre(t, T_NETFLIX - 0.06), taille=54, couleur=ROUGE, rot=-1.2)


# ═════════════════════════════ 2. CELLE QUI PARLE
def soeur(c, t):
    if t < T_SOEUR - 0.26 or t > T_SAISON2 - 0.14: return
    ent = prog(t, T_SOEUR - 0.24, 0.34, sortieExpo)
    sor = prog(t, T_SAISON2 - 0.36, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, borne((t - T_SOEUR + 0.2) * 3), "LE DOCUMENTAIRE")
        titre(c, "C'EST SA SŒUR QUI PARLE", Y_T1, 82, t, T_SOEUR - 0.04, decal=0.01)
        if t > T_PREMIERE - 0.12:
            titre(c, "POUR LA PREMIÈRE FOIS", Y_T2, 82, t, T_PREMIERE - 0.05, rouge=True, decal=0.01)
        carte_photo(c, t, PH_SOEUR, 90, 600, 900, 506, prog(t, T_SOEUR - 0.2, 0.55, lin),
                    fy=0.40, z0=4.0)
        if t > T_MENSONGES - 0.12:
            bloc(c, "DIX ANS DE MENSONGES", AXE, 1300, entre(t, T_MENSONGES - 0.06),
                 taille=64, rot=1.2)


# ═════════════════════════════ 3. COMMENT ÇA COMMENCE
def engrenage(c, t):
    if t < T_SAISON2 - 0.26 or t > T_METHODE - 0.14: return
    ent = prog(t, T_SAISON2 - 0.24, 0.34, sortieExpo)
    sor = prog(t, T_METHODE - 0.36, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "SAISON 2 DE FRIENDS")
        a_h = 1 - prog(t, T_55 - 0.22, 0.16, entree)
        if a_h > 0.01:
            titre(c, "TOUT COMMENCE SUR LE TOURNAGE", Y_T1, 76, t, T_SAISON2 - 0.04,
                  alpha=a_h, decal=0.01)
            if t > T_MEDECINS - 0.12:
                titre(c, "UN ACCIDENT, PUIS UNE ORDONNANCE", Y_T2, 72, t, T_MEDECINS - 0.05,
                      alpha=a_h, decal=0.01)
        carte_video(c, t, V_CHANDLER, 90, 600, 900, 506, prog(t, T_SAISON2 - 0.2, 0.55, lin),
                    t0=T_SAISON2 - 0.18, z0=4.0)
        # un seul fait à la fois : le pavé du jet-ski s'en va quand les cachets arrivent
        av = 1 - prog(t, T_55 - 0.2, 0.14, entree)
        if t > T_JETSKI - 0.12 and av > 0.01:
            bloc(c, "UN ACCIDENT DE JET-SKI", AXE, 1300, entre(t, T_JETSKI - 0.06), av,
                 taille=60, rot=-1.2)
        if t > T_55 - 0.14:
            av2 = 1 - prog(t, T_KILOS - 0.2, 0.14, entree)
            if av2 > 0.01:
                compteur(c, 55, " PAR JOUR", AXE, 1230, prog(t, T_55 - 0.1, 0.5, lin),
                         taille=150, a=av2, couleur=ROUGE, sous="CACHETS D'ANTIDOULEUR")
            if t > T_KILOS - 0.14:
                compteur(c, 58, " KILOS", AXE, 1230, prog(t, T_KILOS - 0.1, 0.5, lin),
                         taille=150, sous="DEVANT DES MILLIONS DE GENS")


# ═════════════════════════════ 4. LA MÉTHODE
def methode(c, t):
    if t < T_METHODE - 0.26 or t > T_MARIAGE - 0.04: return
    ent = prog(t, T_METHODE - 0.24, 0.34, sortieExpo)
    sor = prog(t, T_MARIAGE - 0.28, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "CE QUE SA SŒUR RACONTE")
        a_h = 1 - prog(t, T_PERSONNE - 0.22, 0.16, entree)
        if a_h > 0.01:
            titre(c, "IL SE DOSAIT POUR L'ÉCRAN", Y_T1, 80, t, T_DOSAIT - 0.04,
                  alpha=a_h, decal=0.01)
        carte_video(c, t, V_PERRY, 90, 560, 900, 506, prog(t, T_METHODE - 0.2, 0.55, lin),
                    t0=T_METHODE - 0.18, z0=4.0)
        av = 1 - prog(t, T_PRISES - 0.22, 0.16, entree)
        if t > T_JUSTE - 0.14 and av > 0.01:
            document(c, t, ["« Juste assez pour tenir.", "Jamais assez pour que ça se voie. »"],
                     AXE, 1255, 700, entre(t, T_JUSTE - 0.07) * av, "Sa sœur",
                     rot=-2.2)
        if t > T_PRISES - 0.14:
            bloc(c, "IL CACHAIT SES TREMBLEMENTS", AXE, 1240,
                 entre(t, T_PRISES - 0.07) * (1 - prog(t, T_PERSONNE - 0.2, 0.14, entree)),
                 taille=58, rot=1.2)
        if t > T_PERSONNE - 0.14:
            # le seul surlignage de toute la vidéo : il tombe sur la phrase qui fait mal
            u2 = prog(t, T_PERSONNE - 0.12, 0.26, sortieExpo)
            surlignage(c, "PERSONNE N'A RIEN VU", Y_T1, 92, u2)
            titre(c, "PERSONNE N'A RIEN VU", Y_T1, 92, t, T_PERSONNE - 0.05, couleur=BLANC,
                  decal=0.014)


# ═════════════════════════════ 5. LE MARIAGE
def mariage(c, t):
    if t < T_MARIAGE - 0.42 or t > T_2018 - 0.04: return
    ent = prog(t, T_MARIAGE - 0.40, 0.36, sortieExpo)
    sor = prog(t, T_2018 - 0.28, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "L'ÉPISODE DU MARIAGE")
        a_h = 1 - prog(t, T_TOUS - 0.22, 0.16, entree)
        if a_h > 0.01:
            titre(c, "MONICA ET CHANDLER SE MARIENT", Y_T1, 74, t, T_MARIAGE - 0.04,
                  alpha=a_h, decal=0.01)
            if t > T_FAMILLE - 0.12:
                titre(c, "SA FAMILLE EST VENUE SUR LE PLATEAU", Y_T2, 68, t, T_FAMILLE - 0.05,
                      alpha=a_h, decal=0.01)
        carte_video(c, t, V_MARIAGE, 90, 560, 900, 506, prog(t, T_MARIAGE - 0.2, 0.55, lin),
                    t0=T_MARIAGE - 0.18, z0=4.0)
        if t > T_TOUS - 0.14:
            titre(c, "ILS PENSAIENT TOUS LA MÊME CHOSE", Y_T1, 72, t, T_TOUS - 0.05, decal=0.01)
        if t > T_SEUL - 0.1:
            document(c, t, ["« C'est peut-être le seul", "mariage qu'il aura. »"],
                     AXE, 1255, 680, entre(t, T_SEUL - 0.03), "Sa sœur",
                     rot=2.2)


# ═════════════════════════════ 6. 2018, L'HÔPITAL
def hopital(c, t):
    if t < T_2018 - 0.42 or t > T_MORT - 0.14: return
    ent = prog(t, T_2018 - 0.40, 0.36, sortieExpo)
    sor = prog(t, T_MORT - 0.36, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "2018")
        a_h = 1 - prog(t, T_BATMAN - 0.22, 0.16, entree)
        if a_h > 0.01:
            titre(c, "SON CORPS LÂCHE", Y_T1, 96, t, T_2018 - 0.04, alpha=a_h, decal=0.016)
            carte_video(c, t, V_PERRY, 90, 560, 900, 506, prog(t, T_2018 - 0.18, 0.55, lin), a_h,
                        t0=T_2018 - 3.6, z0=4.0)
            av = 1 - prog(t, T_COMA - 0.2, 0.14, entree)
            if t > T_2PCT - 0.12 and av > 0.01:
                compteur(c, 2, " %", AXE, 1210, prog(t, T_2PCT - 0.1, 0.55, lin),
                         taille=170, a=a_h * av, couleur=ROUGE, sous="DE CHANCES DE SURVIE")
            if t > T_COMA - 0.12:
                bloc(c, "DEUX SEMAINES DE COMA", AXE, 1180, entre(t, T_COMA - 0.06), a_h,
                     taille=58, rot=-1.2)
                bloc(c, "CINQ MOIS D'HÔPITAL", AXE, 1300, entre(t, TW(195) - 0.06), a_h,
                     taille=58, rot=1.2)
        if t > T_BATMAN - 0.16:
            titre(c, "SA SŒUR TROUVE ÇA SOUS SON LIT", Y_T1, 70, t, T_BATMAN - 0.06, decal=0.01)
            titre(c, "UNE FIGURINE DE BATMAN", Y_T2, 78, t, T_BATMAN + 0.45, rouge=True, decal=0.01)
            carte_photo(c, t, PH_SELFIE, 150, 640, 780, 439,
                        prog(t, T_BATMAN - 0.12, 0.55, lin), fy=0.38, z0=4.0)
            if t > T_7M - 0.14:
                bloc(c, "SEPT MILLIONS DE DOLLARS POUR S'EN SORTIR", AXE, 1250,
                     entre(t, T_7M - 0.07), taille=50, rot=-1.2)


# ═════════════════════════════ 7. LE 28 OCTOBRE
def mort(c, t):
    if t < T_MORT - 0.26 or t > T_ENTERREMENT - 0.14: return
    ent = prog(t, T_MORT - 0.24, 0.34, sortieExpo)
    sor = prog(t, T_ENTERREMENT - 0.36, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "28 OCTOBRE 2023")
        a_h = 1 - prog(t, T_CINQ - 0.22, 0.16, entree)
        if a_h > 0.01:
            titre(c, "IL MEURT CHEZ LUI", Y_T1, 96, t, T_MORT - 0.04, alpha=a_h, decal=0.016)
            titre(c, "À CINQUANTE-QUATRE ANS", Y_T2, 80, t, TW(226) - 0.05, alpha=a_h, decal=0.01)
        carte_video(c, t, V_FUNERAILLES, 90, 600, 900, 506, prog(t, T_MORT - 0.2, 0.55, lin),
                    t0=T_MORT - 0.18, z0=4.0)
        av = 1 - prog(t, T_ASSISTANT - 0.2, 0.14, entree)
        if t > T_ACCIDENT - 0.12 and av > 0.01:
            bloc(c, "MORT CLASSÉE ACCIDENTELLE", AXE, 1280, entre(t, T_ACCIDENT - 0.06), av,
                 taille=58, rot=1.2)
        if t > T_CINQ - 0.14:
            titre(c, "CINQ PERSONNES", Y_T1, 96, t, T_CINQ - 0.05, decal=0.016)
            titre(c, "ONT PLAIDÉ COUPABLE", Y_T2, 84, t, TW(238) - 0.05, rouge=True, decal=0.012)
            if t > T_ASSISTANT - 0.14:
                bloc(c, "DONT SON PROPRE ASSISTANT", AXE, 1280, entre(t, T_ASSISTANT - 0.07),
                     taille=58, couleur=ROUGE, rot=-1.2)


# ═════════════════════════════ 8. LES CINQ AUTRES
def cercueil(c, t):
    if t < T_ENTERREMENT - 0.26 or t > T_CTA - 0.14: return
    ent = prog(t, T_ENTERREMENT - 0.24, 0.34, sortieExpo)
    sor = prog(t, T_CTA - 0.34, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "À SON ENTERREMENT")
        a_h = 1 - prog(t, T_MAIN - 0.22, 0.16, entree)
        if a_h > 0.01:
            titre(c, "IL Y A EU CETTE IMAGE", Y_T1, 86, t, T_ENTERREMENT - 0.04,
                  alpha=a_h, decal=0.012)
            if t > T_CERCUEIL - 0.12:
                titre(c, "LES CINQ AUTRES ACTEURS", Y_T2, 80, t, T_CERCUEIL - 0.05,
                      alpha=a_h, decal=0.01)
        carte_video(c, t, V_CAST, 90, 600, 900, 506, prog(t, T_ENTERREMENT - 0.2, 0.55, lin),
                    t0=T_ENTERREMENT - 0.18, z0=4.0)
        if t > T_MAIN - 0.14:
            titre(c, "ILS SE TENAIENT", Y_T1, 92, t, T_MAIN - 0.05, decal=0.016)
            titre(c, "PAR LA MAIN", Y_T2, 110, t, TW(276) - 0.05, rouge=True, decal=0.02)
        if t > T_AUCUN - 0.14:
            bloc(c, "AUCUN N'A VOULU PARLER", AXE, 1280, entre(t, T_AUCUN - 0.07),
                 taille=64, couleur=ROUGE, rot=1.2)


# ═════════════════════════════ 9. L'APPEL AU COMMENTAIRE
def cta(c, t):
    if t < T_CTA - 0.26 or t > T_SIGN + 0.08: return
    ent = prog(t, T_CTA - 0.24, 0.34, sortieExpo)
    sor = prog(t, T_SIGN - 0.18, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        rayons(c, AXE, 820, t, 1150, 0.07, 14, ROUGE)
        ondes_sol(c, t, T_CTA - 0.3, 0.6, 4, 0.6)
        titre(c, "POURQUOI AUCUN DES CINQ", 520, 84, t, T_CTA - 0.04, decal=0.012)
        if t > TW(297) - 0.14:
            titre(c, "N'A VOULU PARLER ?", 660, 110, t, TW(297) - 0.06, rouge=True, decal=0.02)
        if t > T_CTA + 0.3:
            bloc(c, "DIS-LE EN COMMENTAIRE", AXE, 1020, entre(t, T_CTA + 0.36),
                 taille=62, rot=-1.2)


# ═════════════════════════════ sons — 21 au lieu de 51 : on n'illustre que les bascules
son(0.0, "impact", -4); son(0.0, "whoosh_long", -9)
son(T_JACUZZI - 0.14, "whoosh_bas", -10)
son(T_NETFLIX - 0.06, "tampon", -9)
son(T_SOEUR - 0.22, "whoosh_court", -10); son(T_MENSONGES - 0.06, "pop", -11)
son(T_SAISON2 - 0.22, "whoosh_court", -10); son(T_JETSKI - 0.06, "pop", -11)
son(T_55 - 0.1, "impact_doux", -8); son(T_KILOS - 0.1, "impact_doux", -9)
son(T_METHODE - 0.22, "whoosh_court", -10); son(T_JUSTE - 0.07, "verre", -10)
son(T_PERSONNE - 0.06, "impact", -6)
son(T_MARIAGE - 0.22, "whoosh", -9); son(T_SEUL - 0.03, "verre", -10)
son(T_2018 - 0.22, "whoosh_court", -10); son(T_2PCT - 0.1, "impact_doux", -8)
son(T_BATMAN - 0.12, "swipe", -11)
son(T_MORT - 0.22, "whoosh_bas", -9); son(T_CINQ - 0.05, "impact_doux", -8)
son(T_ENTERREMENT - 0.22, "whoosh", -9); son(T_MAIN - 0.05, "impact_doux", -7)
son(T_CTA - 0.22, "whoosh_long", -9)
sons_signature_people(son, T_SIGN)

# flou de mouvement : seulement sur les trois vraies bascules
for a, b in [(0.0, 0.55), (T_JACUZZI - 0.14, T_JACUZZI + 0.3),
             (T_MARIAGE - 0.22, T_MARIAGE + 0.25), (T_ENTERREMENT - 0.22, T_ENTERREMENT + 0.25),
             (T_SIGN + 0.4, T_SIGN + 0.9)]:
    rapide(a, b)
# deux éclairs dans toute la vidéo, bas
eclair(0.02, ROUGE, 0.09)
eclair(T_PERSONNE, BLANC, 0.08)


# ═════════════════════════════ composition
def fond(c, t):
    """le décor seul — outils/vide.py s'en sert comme référence"""
    pulse = (battement(t, T_PERSONNE, 1, 0.5) - 1) + (battement(t, T_MAIN, 1, 0.5) - 1)
    fond_grille(c, t, pulse, vitesse=vitesse_grille(t))


def dessine(c, t):
    fond(c, t)
    hook(c, t); soeur(c, t); engrenage(c, t); methode(c, t); mariage(c, t)
    hopital(c, t); mort(c, t); cercueil(c, t); cta(c, t)
    if t >= T_SIGN - 0.12:
        signature_people(c, t, T_SIGN, MEDIAS)
    filigrane(c, 0.26 * (1 - prog(t, T_SIGN - 0.2, 0.2, entree)))
    K.dessine_eclairs(c, t)
    if t < T_SIGN - 0.02:
        SOUS.dessine(c, t, BLANC)
