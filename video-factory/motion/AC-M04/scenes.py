"""AC-M04 — RECTO CERVEAU. « Cher Kylian » : Mbappé effacé de Chine en quarante-huit heures.

FORMAT NOUVEAU, DEMANDÉ PAR YOUSSEF LE 28/10/2026 — la LETTRE.
Il a envoyé une vidéo de @darkearth sur le Ballon d'Or de Harry Kane (le sujet d'AC-M02, traité
autrement) : « regarde une vidéo bien tournée où il rentre dans les émotions des spectateurs…
je te parle pas du design du montage, je te parle du fond, comment il parle, comment il a réussi
à entraîner les gens. » Ce que sa vidéo fait, et qu'on reprend ici :
  - on ne parle pas DU sujet, on parle AU sujet : « Cher Harry, toi qu'on a si longtemps
    sous-estimé… ». Le spectateur lit par-dessus l'épaule, il n'écoute pas un bulletin ;
  - **3,25 mots/s** chez lui (nous étions à 4,47 sur AC-M03). Ici : **3,50 mots/s**, pauses
    naturelles gardées (`voix.py --sans-resserrer --sans-hook`). La gravité vient de la lenteur ;
  - l'anaphore (« toi qu'on… toi qu'on… ») puis le renversement (« et pourtant ») ;
  - le « on » collectif, qui rend le spectateur complice de ce qui est arrivé ;
  - **aucun chiffre jeté pour le chiffre**, aucune statistique de dossier ;
  - **pas de CTA, pas de question finale** : ça se termine sur une image.
  - ⚠ Chez lui il y a de la MUSIQUE douce du début à la fin. On n'en met pas (règle DY-M08) :
    à signaler, c'est une partie de l'effet qui nous manque.
Conséquence sur le hook : on ne lance PAS `hook_rapide.py`. La règle « attaque toujours rapide »
est volontairement suspendue sur ce format — l'attaque de la lettre doit être lente.

Montage : la grammaire d'AC-M03 (moins dynamique) poussée plus loin — 7 scènes, un média qui tient
8 à 12 s, zéro éclair, un seul surlignage (« TON CLUB N'A RIEN DIT »), 14 bruitages.
Rubrique « LETTRE / … » à la place de « DÉCODER / … ».

Sujet vérifié à la source (AFP via France 24 du 28/10/2026 et Al Jazeera du 27/10,
Radio France, Ouest-France) :
  - Lundi 26/10, Mbappé perd le Ballon d'Or au profit de Harry Kane (c'était AC-M02).
  - Dans le podcast The Bridge, en avril, il dit que le mème où il a « le plus rigolé » plaque son
    visage sur celui d'un homme qu'il croit être « un dictateur chinois » — Mao Zedong. Le site
    chinois Dongqiudi exhume la vidéo le lundi 26/10 au soir. The Bridge l'a depuis supprimée et
    s'est excusé.
  - Mardi 27/10 : TROIS grandes entreprises chinoises rompent (Dongpeng, boissons, dont les
    bouteilles portent son visage ; Mengniu, premier laitier du pays ; une troisième).
    La télévision d'État suspend la diffusion du championnat espagnol.
  - Mbappé s'excuse en français, en anglais et en mandarin. La Liga s'excuse aussi.
    **Le Real Madrid ne s'est pas exprimé.**
  - Mercredi 28/10 : Pékin dit prendre « au sérieux » ses excuses (porte-parole Guo Jiakun), mais
    les critiques continuent. Impossible de s'abonner à ses comptes Weibo et Xiaohongshu
    (plus de 2 millions d'abonnés au total). Dior et Hublot effacent ses contenus de leur Weibo.
    Dans la principale boutique Adidas de Pékin, des maillots du Real, aucun au nom de Mbappé.
  - Il est surnommé « Guigui » (tortue) en Chine, où il était très populaire.
  - En septembre, à L'Équipe, sur ces mèmes qui le grimaient en dictateur : « Être comparé à des
    individus qui assassinent, ou qui ont fait le malheur de millions et de millions de personnes —
    je ne crois pas avoir jamais fait quelque chose comme ça dans ma vie. »
  ÉCRIT EXPRÈS SANS : le nom de Mao, le nom des marques, toute appréciation sur la Chine.
  On raconte ce qui est arrivé à un homme, pas un dossier politique.
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

SOUS = sous_titres_people(K, fusions={(0, 1): "Cher Kylian,", (5, 6): "Ballon d'Or"})

V_MBAPPE = "videos/mbappe"
V_MBAPPE2 = "videos/mbappe2"
V_CEREMONIE = "videos/ceremonie"
V_PEKIN = "videos/pekin"
PH_BUS = "photos/bus"
PH_BOUTEILLES = "photos/bouteilles"
PH_AFFICHE = "photos/affiche"
PH_WEIBO = "photos/weibo"
MEDIAS = []

# ───────────────────────────── repères, tous accrochés à un mot
T_CHER, T_BALLON, T_PIRE, T_LENDEMAIN = TW(0), TW(4), TW(12), TW(23)
T_PHRASE, T_DITE, T_MONTAGE, T_REPONDU, T_TOI = TW(34), TW(38), TW(50), TW(64), TW(75)
T_CONTRATS, T_TELE, T_BOUTIQUE, T_AUCUN = TW(84), TW(94), TW(105), TW(121)
T_RESEAUX, T_GUIGUI = TW(126), TW(140)
T_EXCUSE, T_CHAMPIONNAT, T_CLUB = TW(148), TW(158), TW(163)
T_SEPTEMBRE, T_MONTAGES, T_COMPARE, T_CITATION = TW(169), TW(178), TW(186), TW(206)
T_PASFAB, T_TORT, T_UNJOUR, T_OUBLIERA = TW(220), TW(226), TW(234), TW(243)
T_SIGN = round(K.timing["duree_voix"] - 0.05, 2)
T_FIN = DUREE


def vitesse_grille(t):
    """le décor avance, lentement, sans à-coups : sur une lettre, rien ne doit tirer l'œil"""
    v = 0.38
    for t0 in (T_LENDEMAIN, T_CLUB):
        v += 0.8 * max(0.0, 1 - abs(t - t0) / 0.8) ** 2
    return v


def ondes_sol(c, t, t0, a=1.0, n=4, vitesse=0.45):
    """anneaux rouges qui montent du point de fuite vers nous, à même le sol"""
    if a <= 0.01: return
    for k in range(n):
        u = ((t - t0) * vitesse + k / n) % 1.0
        z = mix(7.0, 0.55, u ** 1.5)
        y = HORIZON + SOL / z
        rx = 1500 / z
        al = a * 0.42 * math.sin(math.pi * min(1.0, u * 1.08)) ** 0.7
        if y > H + 500 or al <= 0.01: continue
        c.drawOval(skia.Rect.MakeXYWH(AXE - rx, y - rx * 0.20, 2 * rx, 0.40 * rx),
                   peinture(ROUGE, al, Style=skia.Paint.kStroke_Style, StrokeWidth=4 + 16 * (1 - z / 7)))


# ═════════════════════════════ 1. L'EN-TÊTE DE LA LETTRE
def entete(c, t):
    if t > T_PHRASE - 0.04: return
    sor = prog(t, T_PHRASE - 0.30, 0.26, entree)
    with Calque(c, 1 - sor):
        # image 0 : lui, en smoking, le soir où le trophée lui passe sous le nez. Aucun texte.
        arr = prog(t, -0.12, 0.40, sortieExpo)
        bascule = prog(t, T_LENDEMAIN - 0.22, 0.34, entree)
        a_h = 1 - prog(t, T_LENDEMAIN - 0.26, 0.2, entree)
        if bascule < 0.99:
            w1 = mix(1000, 900, borne(arr)); h1 = w1 * 0.5625
            carte_video(c, t, V_CEREMONIE, AXE_HAUT - w1 / 2, 600, w1, h1,
                        borne(arr) * (1 - bascule), t0=-0.4, z0=5.5)
        # « Cher Kylian, » arrive au 5e mot : c'est l'en-tête d'une lettre, pas un titre d'info
        if t > T_BALLON - 0.1 and a_h > 0.01:
            titre(c, "CHER KYLIAN,", Y_T2, 104, t, T_BALLON - 0.04, alpha=a_h, decal=0.02)
        if bascule > 0.01:
            # son visage sur les bus de Shanghai : l'image de ce qu'il était là-bas
            carte_photo(c, t, PH_BUS, 90, 600, 900, 506, bascule, fy=0.5, z0=1.6)
            titre(c, "UN PAYS A COMMENCÉ", Y_T1, 84, t, T_LENDEMAIN - 0.04, decal=0.012)
            if t > TW(32) - 0.1:
                titre(c, "À T'EFFACER", Y_T2, 104, t, TW(32) - 0.04, rouge=True, decal=0.02)


# ═════════════════════════════ 2. LA PHRASE
def phrase(c, t):
    if t < T_PHRASE - 0.34 or t > T_CONTRATS - 0.04: return
    ent = prog(t, T_PHRASE - 0.32, 0.38, sortieExpo)
    sor = prog(t, T_CONTRATS - 0.30, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, borne((t - T_PHRASE + 0.28) * 3), "CE QUE TU AS DIT", gauche="LETTRE")
        a_h = 1 - prog(t, T_TOI - 0.24, 0.18, entree)
        if a_h > 0.01:
            titre(c, "UNE PHRASE. UNE SEULE.", Y_T1, 86, t, T_PHRASE - 0.04, alpha=a_h, decal=0.014)
            if t > T_DITE - 0.12:
                titre(c, "DITE SIX MOIS PLUS TÔT", Y_T2, 76, t, T_DITE - 0.05, alpha=a_h, decal=0.01)
        carte_video(c, t, V_MBAPPE, 90, 560, 900, 506, prog(t, T_PHRASE - 0.26, 0.6, lin),
                    t0=T_PHRASE - 0.24, z0=4.0)
        if t > T_REPONDU - 0.14:
            document(c, t, ["« Celui où j'ai le plus rigolé,", "je crois que c'est un dictateur chinois. »"],
                     AXE, 1250, 700, entre(t, T_REPONDU - 0.07), "Kylian Mbappé, en avril", rot=-2.0)
        if t > T_TOI - 0.16:
            titre(c, "TU N'AVAIS RIEN DESSINÉ,", Y_T1, 76, t, T_TOI - 0.05, decal=0.01)
            titre(c, "RIEN PUBLIÉ, RIEN DEMANDÉ", Y_T2, 76, t, T_TOI + 0.55, decal=0.01)


# ═════════════════════════════ 3. CE QUE ÇA LUI A COÛTÉ
def contrats(c, t):
    if t < T_CONTRATS - 0.34 or t > T_RESEAUX - 0.04: return
    ent = prog(t, T_CONTRATS - 0.32, 0.38, sortieExpo)
    sor = prog(t, T_RESEAUX - 0.30, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "VINGT-QUATRE HEURES", gauche="LETTRE")
        bascule = prog(t, T_BOUTIQUE - 0.24, 0.3, entree)
        a_h = 1 - prog(t, T_BOUTIQUE - 0.24, 0.18, entree)
        if a_h > 0.01:
            titre(c, "TROIS GÉANTS CHINOIS", Y_T1, 86, t, T_CONTRATS - 0.04, alpha=a_h, decal=0.014)
            titre(c, "ROMPENT LEURS CONTRATS", Y_T2, 80, t, TW(88) - 0.05, alpha=a_h, decal=0.012)
        if bascule < 0.99:
            carte_photo(c, t, PH_BOUTEILLES, 90, 600, 900, 506,
                        prog(t, T_CONTRATS - 0.26, 0.6, lin) * (1 - bascule), fy=0.45, z0=4.0)
            if t > T_TELE - 0.14:
                bloc(c, "LA TÉLÉ D'ÉTAT COUPE TON CHAMPIONNAT", AXE, 1280,
                     entre(t, T_TELE - 0.07), 1 - bascule, taille=50, couleur=ROUGE, rot=-1.1)
        if bascule > 0.01:
            carte_video(c, t, V_PEKIN, 90, 600, 900, 506, bascule, t0=T_BOUTIQUE - 0.2, z0=1.6)
            titre(c, "À PÉKIN, TON NOM DISPARAÎT", Y_T1, 72, t, T_BOUTIQUE - 0.05, decal=0.01)
            if t > T_AUCUN - 0.14:
                titre(c, "DES VITRINES ET DES MAILLOTS", Y_T2, 82, t, T_AUCUN - 0.05, rouge=True, decal=0.012)


# ═════════════════════════════ 4. EFFACÉ DES ÉCRANS
def reseaux(c, t):
    if t < T_RESEAUX - 0.34 or t > T_EXCUSE - 0.04: return
    ent = prog(t, T_RESEAUX - 0.32, 0.38, sortieExpo)
    sor = prog(t, T_EXCUSE - 0.30, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "SUR LEURS RÉSEAUX", gauche="LETTRE")
        bascule = prog(t, T_GUIGUI - 0.24, 0.3, entree)
        a_h = 1 - prog(t, T_GUIGUI - 0.24, 0.18, entree)
        if a_h > 0.01:
            titre(c, "DEUX MILLIONS DE GENS", Y_T1, 84, t, T_RESEAUX - 0.04, alpha=a_h, decal=0.014)
            titre(c, "NE PEUVENT PLUS TE SUIVRE", Y_T2, 78, t, TW(133) - 0.05, alpha=a_h, decal=0.012)
        if bascule < 0.99:
            carte_photo(c, t, PH_WEIBO, 240, 580, 600, 506,
                        prog(t, T_RESEAUX - 0.26, 0.6, lin) * (1 - bascule), fy=0.45, z0=4.0)
            bloc(c, "TES COMPTES SONT BLOQUÉS", AXE, 1230,
                 entre(t, T_RESEAUX + 0.3), 1 - bascule, taille=58, couleur=ROUGE, rot=-1.1)
        if bascule > 0.01:
            carte_photo(c, t, PH_AFFICHE, 90, 600, 900, 506, bascule, fy=0.45, z0=1.6)
            titre(c, "LÀ-BAS, ON T'APPELAIT GUIGUI", Y_T1, 74, t, T_GUIGUI - 0.05, decal=0.01)
            if t > TW(144) - 0.12:
                bloc(c, "LA TORTUE", AXE, 1250, entre(t, TW(144) - 0.06), taille=78, rot=1.1)


# ═════════════════════════════ 5. LES EXCUSES, ET LE SILENCE
def excuses(c, t):
    if t < T_EXCUSE - 0.34 or t > T_SEPTEMBRE - 0.04: return
    ent = prog(t, T_EXCUSE - 0.32, 0.38, sortieExpo)
    sor = prog(t, T_SEPTEMBRE - 0.30, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "CE QUE TU AS FAIT", gauche="LETTRE")
        a_h = 1 - prog(t, T_CLUB - 0.24, 0.18, entree)
        if a_h > 0.01:
            titre(c, "TU T'ES EXCUSÉ EN TROIS LANGUES", Y_T1, 70, t, T_EXCUSE - 0.04,
                  alpha=a_h, decal=0.01)
            if t > T_CHAMPIONNAT - 0.12:
                titre(c, "TON CHAMPIONNAT AUSSI", Y_T2, 80, t, T_CHAMPIONNAT - 0.05,
                      alpha=a_h, decal=0.012)
        carte_video(c, t, V_MBAPPE2, 90, 600, 900, 506, prog(t, T_EXCUSE - 0.26, 0.6, lin),
                    t0=T_EXCUSE - 0.24, z0=4.0)
        if t > T_CLUB - 0.16:
            # le seul surlignage de toute la vidéo : la phrase qui fait mal
            u2 = prog(t, T_CLUB - 0.1, 0.3, sortieExpo)
            surlignage(c, "TON CLUB, LUI,", Y_T1, 86, u2)
            titre(c, "TON CLUB, LUI,", Y_T1, 86, t, T_CLUB - 0.04, couleur=BLANC, decal=0.014)
            if t > TW(166) - 0.12:
                titre(c, "N'A RIEN DIT.", Y_T2, 100, t, TW(166) - 0.05, decal=0.018)


# ═════════════════════════════ 6. CE QU'IL AVAIT DÉJÀ DIT EN SEPTEMBRE
def septembre(c, t):
    if t < T_SEPTEMBRE - 0.34 or t > T_PASFAB - 0.04: return
    ent = prog(t, T_SEPTEMBRE - 0.32, 0.38, sortieExpo)
    sor = prog(t, T_PASFAB - 0.30, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "EN SEPTEMBRE DÉJÀ", gauche="LETTRE")
        a_h = 1 - prog(t, T_CITATION - 0.26, 0.18, entree)
        if a_h > 0.01:
            titre(c, "AU DÉBUT, ÇA TE FAISAIT SOURIRE", Y_T1, 70, t, T_MONTAGES - 0.04,
                  alpha=a_h, decal=0.01)
            if t > T_COMPARE - 0.12:
                titre(c, "ET PUIS BEAUCOUP MOINS", Y_T2, 80, t, T_COMPARE - 0.05,
                      alpha=a_h, rouge=True, decal=0.012)
        carte_video(c, t, V_MBAPPE, 90, 560, 900, 506, prog(t, T_SEPTEMBRE - 0.26, 0.6, lin),
                    t0=T_SEPTEMBRE - 2.6, z0=4.0)
        if t > T_CITATION - 0.16:
            document(c, t, ["« Je ne crois pas avoir jamais", "fait ça de ma vie. »"],
                     AXE, 1250, 700, entre(t, T_CITATION - 0.08), "Kylian Mbappé, en septembre",
                     rot=2.0)


# ═════════════════════════════ 7. LA FIN DE LA LETTRE — pas de question, une image
def fin(c, t):
    if t < T_PASFAB - 0.34 or t > T_SIGN + 0.08: return
    ent = prog(t, T_PASFAB - 0.32, 0.38, sortieExpo)
    sor = prog(t, T_SIGN - 0.18, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        rayons(c, AXE, 840, t, 1150, 0.06, 14, ROUGE)
        ondes_sol(c, t, T_PASFAB - 0.3, 0.55, 4, 0.5)
        a_h = 1 - prog(t, T_UNJOUR - 0.26, 0.2, entree)
        if a_h > 0.01:
            titre(c, "TU N'AS PAS FABRIQUÉ", 480, 86, t, T_PASFAB - 0.04, alpha=a_h, decal=0.014)
            titre(c, "CES IMAGES", 600, 86, t, TW(223) - 0.05, alpha=a_h, decal=0.014)
            if t > T_TORT - 0.14:
                bloc(c, "TU AS JUSTE EU LE TORT D'EN PARLER", AXE, 1250,
                     entre(t, T_TORT - 0.07), a_h, taille=54, couleur=ROUGE, rot=-1.1)
        # son visage tient la fin : la lettre se termine sur lui, pas sur une question
        carte_video(c, t, V_MBAPPE2, 160, 720, 760, 428, prog(t, T_PASFAB - 0.26, 0.6, lin),
                    t0=T_PASFAB - 5.6, z0=4.0)
        if t > T_UNJOUR - 0.18:
            titre(c, "UN JOUR, ON DIRA", 480, 90, t, T_UNJOUR - 0.05, decal=0.016)
            titre(c, "QUE TU AS TOUT GAGNÉ", 600, 90, t, TW(239) - 0.05, decal=0.016)
            if t > T_OUBLIERA - 0.14:
                bloc(c, "ET ON OUBLIERA CETTE SEMAINE-LÀ", AXE, 1250,
                     entre(t, T_OUBLIERA - 0.07), taille=56, rot=1.1)


# ═════════════════════════════ sons — 14 seulement, aucun éclair : c'est une lettre
son(0.0, "whoosh_long", -11)
son(T_LENDEMAIN - 0.2, "whoosh_bas", -11)
son(T_PHRASE - 0.28, "whoosh_court", -11)
son(T_REPONDU - 0.07, "verre", -11)
son(T_TOI - 0.05, "impact_doux", -10)
son(T_CONTRATS - 0.28, "whoosh_court", -11)
son(T_TELE - 0.07, "pop", -12)
son(T_BOUTIQUE - 0.2, "swipe", -12); son(T_AUCUN - 0.05, "impact_doux", -9)
son(T_RESEAUX - 0.28, "whoosh_court", -11)
son(T_GUIGUI - 0.2, "swipe", -12)
son(T_EXCUSE - 0.28, "whoosh_court", -11)
son(T_CLUB - 0.06, "impact", -7)
son(T_SEPTEMBRE - 0.28, "whoosh_court", -11); son(T_CITATION - 0.08, "verre", -11)
son(T_PASFAB - 0.28, "whoosh_long", -10)
sons_signature_people(son, T_SIGN)

# flou de mouvement : uniquement sur les deux bascules de média
for a, b in [(0.0, 0.5), (T_LENDEMAIN - 0.2, T_LENDEMAIN + 0.3),
             (T_CLUB - 0.1, T_CLUB + 0.3), (T_SIGN + 0.4, T_SIGN + 0.9)]:
    rapide(a, b)


# ═════════════════════════════ composition
def fond(c, t):
    """le décor seul — outils/vide.py s'en sert comme référence"""
    pulse = (battement(t, T_CLUB, 1, 0.5) - 1)
    fond_grille(c, t, pulse, vitesse=vitesse_grille(t))


def dessine(c, t):
    fond(c, t)
    entete(c, t); phrase(c, t); contrats(c, t); reseaux(c, t)
    excuses(c, t); septembre(c, t); fin(c, t)
    if t >= T_SIGN - 0.12:
        signature_people(c, t, T_SIGN, MEDIAS)
    filigrane(c, 0.26 * (1 - prog(t, T_SIGN - 0.2, 0.2, entree)))
    K.dessine_eclairs(c, t)
    if t < T_SIGN - 0.02:
        SOUS.dessine(c, t, BLANC)
