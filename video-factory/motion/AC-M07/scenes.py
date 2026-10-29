"""AC-M07 — RECTO CERVEAU. O.J. Simpson : le procureur qu'on a poussé à la faute.

COMMANDE DE YOUSSEF (29/10/2026 au soir) : il envoie https://vm.tiktok.com/ZGdXJDaQX/ —
**@darkearth, 2,7 M de vues, 219 900 j'aime, 82 s, postée le 14/07/2026** — et demande
« une autre vidéo sur cette vidéo là… la même mais à une autre façon ».

Ce que fait @darkearth (décortiqué, cf. mémoire reference-darkearth-gant-oj) :
  - **10 secondes sans voix** : archives plein cadre + une phrase écrite tenue à l'écran
    (« Ils étaient certains de le condamner… jusqu'à ce qu'il enfile ce gant ») + musique ;
  - puis 229 mots à **3,2 mots/s**, 24 plans, 0,28 coupe/s, sous-titres **un mot à la fois** ;
  - 100 % archives réelles, zéro graphisme, zéro logo, **fin sur une image** sans CTA ;
  - les mots sensibles sont censurés à l'écran (« M*RTS. »).

NOTRE AUTRE FAÇON — même affaire, angle inverse. Lui raconte « un gant a fait basculer le
procès ». Nous racontons **comment un procureur s'est fait pousser à la faute en trente
secondes**, et nous donnons le détail qu'il a raté : quelques jours plus tard, le fabricant
apporte la MÊME paire, neuve, et elle va parfaitement à Simpson. Le jury ne l'a jamais vu.
Format bonhomme (29/10/2026), pas d'archives : on n'en a pas, et c'est l'identité de la chaîne.

⚠ Erreur de @darkearth corrigée : il date la scène du gant au **3 octobre 1995**. C'est la date
du VERDICT. L'essayage a eu lieu le **15 juin 1995**.

Faits vérifiés (fr.wikipedia « Affaire O. J. Simpson », chronologie sourcée Toobin 2016 ;
Ouest-France 03/10/2025 ; 1995blog.com) :
  - 12/06/1994 : Nicole Brown Simpson et Ronald Goldman sont tués. 17/06/1994 : la fuite en
    Ford Bronco, suivie par ~95 millions de téléspectateurs.
  - Gants Aris Lights, taille extra-large, numéro de série 70263, achetés par Nicole en 1990.
  - 15/06/1995 : pendant la pause, les avocats de la défense essaient les gants et les trouvent
    petits. Marcia Clark et Bill Hodgman décident de NE PAS faire essayer ; Darden acquiesce.
    F. Lee Bailey le provoque (« tu n'en as pas le courage, je le ferai moi-même »). Darden
    panique, réclame l'essayage, voulait le faire hors jury mais le juge les a déjà fait entrer.
    Simpson enfile des gants en latex, Darden lui tend le gant de Bundy en disant Rockingham,
    Simpson garde le pouce plié et grimace.
  - Johnnie Cochran, en plaidoirie : « If it doesn't fit, you must acquit. »
  - 03/10/1995 : non coupable. 1997 : responsable au civil, 33,5 M$.
  - **Le détail clé** : Richard Rubin, ancien directeur d'Aris Isotoner, apporte une paire
    identique non tachée ; Simpson l'essaie et, selon Rubin, « ils s'ajustent plutôt bien ».

ÉCRIT SANS : le mot « meurtre » à l'écran (OCR de la modération), toute affirmation de
culpabilité (il a été acquitté au pénal), toute image de violence.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from bonhomme import *
import bonhomme as B

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 3.4, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
NB_IMAGES = K.nb_images
SFX = K.SFX
TW = K.TW; son = K.son; rapide = K.rapide; flou_a = K.flou_a

# la modération lit le texte à l'écran : @darkearth censure « M*RTS. », on fait pareil
SOUS = sous_titres_bonhomme(K, fusions={(34,): "m*rt"})
MEDIAS = ()

# ═════════════════════════════ repères
T_PROCUREUR, T_PERDU, T_30SEC, T_LUI, T_DEMANDE = TW(5), TW(7), TW(13), TW(17), TW(20)
T_LA, T_OJ, T_STAR, T_JUGE, T_NICOLE, T_RONALD = TW(21), TW(23), TW(26), TW(31), TW(38), TW(43)
T_UNAN, T_FUITE, T_DIRECT, T_95 = TW(44), TW(49), TW(56), TW(58)
T_PREUVE, T_DEUXGANTS, T_LIEUX = TW(61), TW(65), TW(72)
T_MARQUE, T_TAILLE, T_NUMERO, T_NICOLE2, T_PAIRES = TW(73), TW(75), TW(77), TW(81), TW(86)
T_JOURLA, T_PAUSE, T_ESSAIENT, T_PETITS = TW(87), TW(91), TW(97), TW(103)
T_ENFACE, T_CLARK, T_TRANCHE, T_ONNEFAIT, T_RISQUE = TW(104), TW(108), TW(110), TW(111), TW(121)
T_DARDEN, T_DACCORD = TW(125), TW(127)
T_ETPUIS, T_AVOCAT, T_PROVOQUE, T_COURAGE, T_SAPLACE = TW(130), TW(133), TW(138), TW(146), TW(156)
T_CRAQUE, T_RECLAME, T_SANSJURES, T_TROPTARD, T_ENTRER = TW(158), TW(160), TW(168), TW(169), TW(177)
T_SIMPSON2, T_LATEX, T_PREUVE2, T_MAUVAIS = TW(178), TW(184), TW(190), TW(195)
T_POUCE, T_GRIMACE, T_MONTRE, T_ARRIVEPAS = TW(200), TW(203), TW(206), TW(211)
T_SONAVOCAT, T_PHRASE, T_SI, T_ACQUITTER = TW(213), TW(218), TW(221), TW(229)
T_3OCT, T_NONCOUP = TW(230), TW(236)
T_CEQUE, T_JAMAISVU, T_FABRICANT, T_NEUVE, T_ESSAIE, T_ELLELUIVA = TW(238), TW(244), TW(250), TW(255), TW(259), TW(263)
T_FIN = K.timing["duree_voix"]
T_SIGN = T_FIN + 0.35

X_G, X_D, X_C = 330, 720, 500
X_HORS_D, X_HORS_G = 1200, -120


def fondu(t, a, b, d=0.35):
    return prog(t, a, d, sortie) * (1 - prog(t, b - d, d, entree))


def marche(t, t0, x0, x1, duree):
    """x de la hanche + pose, pendant une marche de x0 à x1 ; debout ensuite"""
    if t < t0: return x0, STAND, False
    if t > t0 + duree: return x1, STAND, True
    u = (t - t0) / duree
    return mix(x0, x1, u), pose_marche(t - t0, abs(x1 - x0) / duree), False


# ═════════════════════════════ S1 — le hook : le gant tombe aux pieds du procureur
def s1(c, t):
    a = fondu(t, -1, T_LA)
    if a <= 0.01: return
    with Calque(c, a):
        # le gant tombe du haut dès l'image 0 et rebondit au sol : ça bouge avant le premier mot
        chute = borne(t / 0.52)
        gy = mix(-120, SOL - 70, entree(chute)) + (34 * math.sin((t - 0.52) * 17) * max(0.0, 1 - (t - 0.52) / 0.5) if t > 0.52 else 0)
        down = prog(t, T_PERDU - 0.1, 0.7, douce)
        d = bonhomme(c, X_C + secousse_x(t, 0.52, 7, 0.4), respire(melange(STAND, HEAD_DOWN, down), t), 1, "darden")
        etiquette(c, X_C, 1338, "CHRISTOPHER DARDEN · PROCUREUR", prog(t, T_PROCUREUR - 0.05, 0.3, sortie), taille=30)
        gant(c, X_C + 215, gy, 215, rot=mix(-52, 14, entree(chute)))
        if t >= T_PROCUREUR - 0.05:
            rubrique(c, t, prog(t, T_PROCUREUR - 0.05, 0.4, sortie), "15 JUIN 1995", "LE PROCÈS DU SIÈCLE")
        if t >= T_30SEC - 0.05:
            chiffre_geant(c, "30 SECONDES", 540, 330, t, T_30SEC - 0.05, 130, ROUGE)
        if t >= T_LUI - 0.05:
            chiffre_geant(c, "ET C'EST LUI QUI L'A DEMANDÉ", 540, 440, t, T_LUI - 0.05, 60, BLANC)


# ═════════════════════════════ S2 — qui est l'accusé, et la fuite suivie par 95 millions
def s2(c, t):
    a = fondu(t, T_LA, T_PREUVE)
    if a <= 0.01: return
    with Calque(c, a):
        x, p, fini = marche(t, T_OJ - 0.45, X_HORS_D, X_C, 1.0)
        if fini: p = respire(STAND, t)
        oj = bonhomme(c, x, p, -1, "oj")
        etiquette(c, X_C, 1338, "O.J. SIMPSON", prog(t, T_OJ + 0.6, 0.3, sortie), taille=34)
        if T_STAR - 0.05 <= t < T_UNAN - 0.2:
            u = prog(t, T_STAR - 0.05, 0.3, lambda v: rebond(v, 1.4)) * (1 - prog(t, T_UNAN - 0.45, 0.25, entree))
            etiquette(c, X_C, 420, "STAR DU FOOTBALL AMÉRICAIN", u, taille=40, rouge=False)
        # le banc du tribunal apparaît derrière lui quand on dit qu'il est jugé
        if t >= T_JUGE - 0.1:
            banc(c, 110, 970, 960, 7, t, prog(t, T_JUGE - 0.1, 0.7, sortie) * (1 - prog(t, T_UNAN - 0.3, 0.3, entree)), 0.5, 0.27)
        # les deux noms, sobres, puis ils s'effacent
        for k, (nom, t0) in enumerate((("NICOLE", T_NICOLE), ("RONALD", T_RONALD))):
            u = prog(t, t0 - 0.05, 0.35, sortie) * (1 - prog(t, T_UNAN - 0.3, 0.3, entree))
            if u > 0.01: etiquette(c, X_C, 300 + k * 95, nom, u, taille=44)
        # la fuite : le 4x4 traverse l'écran, lentement
        if t >= T_UNAN - 0.1:
            u_v = prog(t, T_UNAN - 0.1, 0.5, sortie)
            xv = mix(-260, 1340, borne((t - T_FUITE + 1.2) / 5.4))
            voiture(c, xv, SOL - 24, 420, u_v)
            if t >= T_95 - 0.05:
                chiffre_geant(c, "95 MILLIONS", 540, 300, t, T_95 - 0.05, 140, ROUGE)
                chiffre_geant(c, "LE REGARDENT EN DIRECT", 540, 410, t, TW(60) - 0.05, 56, BLANC)


# ═════════════════════════════ S3 — la preuve : deux gants identiques
def s3(c, t):
    a = fondu(t, T_PREUVE, T_JOURLA)
    if a <= 0.01: return
    with Calque(c, a):
        titre(c, "LA PREUVE", 300, 110, t, T_PREUVE + 0.05, rouge=True,
              alpha=1 - prog(t, T_MARQUE - 0.3, 0.3, entree))
        for k, s in enumerate((-1, 1)):
            u = prog(t, T_DEUXGANTS - 0.05 + k * 0.18, 0.5, sortie)
            if u <= 0.01: continue
            xg = mix(540 + s * 820, 540 + s * 215, sortieExpo(u))
            gant(c, xg, 780, mix(120, 300, u), rot=s * 11)
        for k, (txt, t0) in enumerate((("MÊME MARQUE", T_MARQUE), ("MÊME TAILLE", T_TAILLE), ("MÊME NUMÉRO DE SÉRIE", T_NUMERO))):
            u = prog(t, t0 - 0.05, 0.3, lambda v: rebond(v, 1.4)) * (1 - prog(t, T_NICOLE2 - 0.3, 0.25, entree))
            if u > 0.01: etiquette(c, 540, 285 + k * 92, txt, u, taille=42)
        if t >= T_NICOLE2 - 0.05:
            chiffre_geant(c, "NICOLE EN AVAIT ACHETÉ", 540, 300, t, T_NICOLE2 - 0.05, 62, BLANC)
            chiffre_geant(c, "DEUX PAIRES", 540, 400, t, T_PAIRES - 0.18, 110, ROUGE)


# ═════════════════════════════ S4 — la pause : la défense essaie, Clark dit non
def s4(c, t):
    a = fondu(t, T_JOURLA, T_ETPUIS)
    if a <= 0.01: return
    with Calque(c, a):
        titre(c, "PENDANT LA PAUSE", 300, 96, t, T_PAUSE - 0.05, rouge=True,
              alpha=1 - prog(t, T_ENFACE - 0.3, 0.3, entree))
        # la défense essaie les gants : deux bonhommes et un gant qui passe de main en main
        u_d = prog(t, T_ESSAIENT - 0.5, 0.45, sortie) * (1 - prog(t, T_ENFACE - 0.25, 0.3, entree))
        if u_d > 0.01:
            b1 = bonhomme(c, X_G, respire(melange(STAND, POINT, prog(t, T_ESSAIENT - 0.1, 0.4, sortie)), t), 1, "bailey", alpha=u_d, taille=0.9)
            b2 = bonhomme(c, X_D, respire(THINK, t + 1), -1, "cochran", alpha=u_d, taille=0.9)
            gant(c, mix(b1["main_d"][0], b2["main_d"][0], prog(t, T_ESSAIENT, 0.6, entreeSortie)) + 10,
                 b1["main_d"][1] + 36, 130, u_d, rot=-10)
            if t >= T_PETITS - 0.05:
                bulle(c, b2, "ILS SONT PETITS", t, T_PETITS - 0.05, 1, 42, alpha=u_d)
        # Marcia Clark tranche
        u_c = prog(t, T_ENFACE - 0.05, 0.45, sortie)
        if u_c > 0.01:
            cl = bonhomme(c, X_G, respire(melange(STAND, POINT, prog(t, T_TRANCHE - 0.1, 0.4, sortie)), t), 1, "clark", u=u_c)
            etiquette(c, X_G, 1338, "MARCIA CLARK", u_c, taille=32)
            if T_ONNEFAIT - 0.05 <= t < T_RISQUE - 0.15:
                bulle(c, cl, ["ON NE LUI FAIT", "PAS ESSAYER."], t, T_ONNEFAIT - 0.05, -1, 42,
                      alpha=1 - prog(t, T_RISQUE - 0.4, 0.25, entree))
            elif t >= T_RISQUE - 0.1:
                bulle(c, cl, "TROP RISQUÉ.", t, T_RISQUE - 0.1, -1, 46, rouge=ROUGE)
            u_dd = prog(t, T_DARDEN - 0.45, 0.4, sortie)
            if u_dd > 0.01:
                dd = bonhomme(c, X_D, respire(melange(STAND, THINK, prog(t, T_DACCORD - 0.2, 0.4, sortie)), t + 1), -1, "darden", u=u_dd)
                etiquette(c, X_D, 1338, "DARDEN", u_dd, taille=32)


# ═════════════════════════════ S5 — la provocation
def s5(c, t):
    a = fondu(t, T_ETPUIS, T_CRAQUE)
    if a <= 0.01: return
    with Calque(c, a):
        dx = secousse_x(t, T_COURAGE - 0.05, 14, 0.7) + secousse_x(t, T_SAPLACE - 0.05, 12, 0.6)
        dd = bonhomme(c, X_D + dx, respire(CROSSED, t + 1), -1, "darden", u=prog(t, T_ETPUIS, 0.4, sortie))
        etiquette(c, X_D, 1338, "DARDEN", prog(t, T_ETPUIS, 0.4, sortie), taille=32)
        x, p, fini = marche(t, T_AVOCAT - 0.35, X_HORS_G, X_G, 0.9)
        if fini: p = respire(melange(STAND, POINT, prog(t, T_PROVOQUE - 0.15, 0.4, sortie)), t)
        ba = bonhomme(c, x, p, 1, "bailey")
        etiquette(c, X_G, 1338, "F. LEE BAILEY · DÉFENSE", prog(t, T_PROVOQUE - 0.3, 0.3, sortie), taille=28)
        if T_COURAGE - 0.05 <= t < T_SAPLACE - 0.15:
            bulle(c, ba, ["T'AS PAS", "LE CRAN."], t, T_COURAGE - 0.05, -1, 52, rouge=ROUGE,
                  alpha=1 - prog(t, T_SAPLACE - 0.4, 0.25, entree))
        elif t >= T_SAPLACE - 0.1:
            bulle(c, ba, ["JE LE FERAI", "À TA PLACE."], t, T_SAPLACE - 0.1, -1, 46, rouge=ROUGE)


# ═════════════════════════════ S6 — Darden craque, le jury entre
def s6(c, t):
    a = fondu(t, T_CRAQUE, T_SIMPSON2)
    if a <= 0.01: return
    with Calque(c, a):
        u = prog(t, T_CRAQUE, 0.4, sortie)
        dd = bonhomme(c, X_C, respire(melange(STAND, CHEER, prog(t, T_RECLAME - 0.1, 0.4, lambda v: rebond(v, 1.3))), t), 1, "darden", u=u)
        etiquette(c, X_C, 1338, "DARDEN", u, taille=32)
        if T_RECLAME - 0.05 <= t < T_TROPTARD - 0.2:
            bulle(c, dd, ["QU'IL LES", "ESSAIE !"], t, T_RECLAME - 0.05, 1, 52, rouge=ROUGE,
                  alpha=1 - prog(t, T_TROPTARD - 0.45, 0.25, entree))
        if t >= T_ENTRER - 1.3:
            banc(c, 110, 970, 940, 8, t, prog(t, T_ENTRER - 1.3, 1.4, sortie), 0.85, 0.28)
            etiquette(c, 540, 1020, "LE JURY", prog(t, T_ENTRER - 0.1, 0.35, sortie), taille=34)
        if t >= T_TROPTARD - 0.05:
            chiffre_geant(c, "TROP TARD", 540, 300, t, T_TROPTARD - 0.05, 150, ROUGE)


# ═════════════════════════════ S7 — l'essayage qui rate
def s7(c, t):
    a = fondu(t, T_SIMPSON2, T_SONAVOCAT)
    if a <= 0.01: return
    with Calque(c, a):
        u = prog(t, T_SIMPSON2, 0.4, sortie)
        dd = bonhomme(c, X_G, respire(melange(STAND, POINT, prog(t, T_MAUVAIS - 0.5, 0.45, sortie)), t + 1), 1, "darden", u=u, taille=0.92)
        etiquette(c, X_G, 1338, "DARDEN", u, taille=30)
        secoue = secousse_x(t, T_POUCE - 0.05, 9, 0.8)
        p = respire(melange(STAND, THINK, prog(t, T_POUCE - 0.1, 0.5, sortie)), t)
        oj = bonhomme(c, X_D + secoue, p, -1, "oj", u=u)
        etiquette(c, X_D, 1338, "SIMPSON", u, taille=30)
        if T_LATEX - 0.05 <= t < T_MAUVAIS - 0.25:
            bulle(c, oj, "GANTS EN LATEX D'ABORD", t, T_LATEX - 0.05, 1, 36,
                  alpha=1 - prog(t, T_MAUVAIS - 0.5, 0.25, entree))
        # le gant passe de Darden à Simpson
        if t >= T_MAUVAIS - 0.6:
            v = prog(t, T_MAUVAIS - 0.5, 0.6, entreeSortie)
            ax, ay = dd["main_d"]; bx, by = oj["main_d"]
            gant(c, mix(ax, bx, v) + 10, mix(ay, by, v) + 40 - 90 * math.sin(math.pi * v), 140, rot=mix(-25, -8, v))
        if T_MAUVAIS - 0.05 <= t < T_MONTRE:
            etiquette(c, 540, 300, "LE MAUVAIS GANT", prog(t, T_MAUVAIS - 0.05, 0.3, lambda v: rebond(v, 1.4)) * (1 - prog(t, T_MONTRE - 0.3, 0.25, entree)), taille=46)
        if t >= T_GRIMACE - 0.05:
            points_interrogation(c, oj, t, T_GRIMACE - 0.05, 2)
        if t >= T_ARRIVEPAS - 0.05:
            croix(c, X_D + 20, 760, 95, t, T_ARRIVEPAS - 0.05, ROUGE, 22)


# ═════════════════════════════ S8 — la phrase de Cochran
def s8(c, t):
    a = fondu(t, T_SONAVOCAT, T_3OCT)
    if a <= 0.01: return
    with Calque(c, a):
        x, p, fini = marche(t, T_SONAVOCAT - 0.2, X_HORS_D, X_C + 110, 0.9)
        if fini: p = respire(melange(STAND, TALK, prog(t, T_SI - 0.3, 0.4, sortie)), t)
        co = bonhomme(c, x, p, -1, "cochran")
        etiquette(c, X_C + 110, 1338, "JOHNNIE COCHRAN · DÉFENSE", prog(t, T_PHRASE - 0.2, 0.3, sortie), taille=28)
        if t >= T_SI - 0.08:
            bulle(c, co, ["SI ÇA NE LUI", "VA PAS, VOUS DEVEZ", "L'ACQUITTER."], t, T_SI - 0.08, -1, 46, rouge=ROUGE)


# ═════════════════════════════ S9 — le verdict
def s9(c, t):
    a = fondu(t, T_3OCT, T_CEQUE)
    if a <= 0.01: return
    with Calque(c, a):
        titre(c, "3 OCTOBRE 1995", 300, 96, t, T_3OCT, rouge=True,
              alpha=1 - prog(t, T_NONCOUP - 0.25, 0.25, entree))
        u = prog(t, T_3OCT + 0.2, 0.4, sortie)
        oj = bonhomme(c, X_C, respire(melange(STAND, CHEER, prog(t, T_NONCOUP - 0.05, 0.4, lambda v: rebond(v, 1.3))), t), 1, "oj", u=u)
        etiquette(c, X_C, 1338, "SIMPSON", u, taille=32)
        banc(c, 110, 970, 960, 8, t, u, 0.4, 0.26)
        if t >= T_NONCOUP - 0.05:
            chiffre_geant(c, "NON COUPABLE", 540, 300, t, T_NONCOUP - 0.05, 140, ROUGE)


# ═════════════════════════════ S10 — ce que le jury n'a jamais vu
def s10(c, t):
    a = fondu(t, T_CEQUE, T_SIGN + 0.3)
    if a <= 0.01: return
    with Calque(c, a):
        if t < T_FABRICANT - 0.2:
            chiffre_geant(c, "CE QUE LE JURY", 540, 300, t, T_CEQUE - 0.05, 80, BLANC)
            chiffre_geant(c, "N'A JAMAIS VU", 540, 400, t, T_JAMAISVU - 0.15, 96, ROUGE)
        u = prog(t, T_FABRICANT - 0.5, 0.45, sortie)
        if u <= 0.01: return
        # le fabricant arrive avec une paire neuve
        x, p, fini = marche(t, T_FABRICANT - 0.4, X_HORS_G, X_G, 0.9)
        if fini: p = respire(melange(STAND, POINT, prog(t, T_NEUVE - 0.3, 0.4, sortie)), t)
        fa = bonhomme(c, x, p, 1, None, "neutre")
        etiquette(c, X_G, 1338, "LE FABRICANT", prog(t, T_NEUVE - 0.5, 0.3, sortie), taille=30)
        oj = bonhomme(c, X_D, respire(melange(STAND, THINK, prog(t, T_ESSAIE - 0.3, 0.4, sortie)), t + 1), -1, "oj", u=u)
        etiquette(c, X_D, 1338, "SIMPSON", u, taille=30)
        if T_NEUVE - 0.05 <= t < T_ESSAIE - 0.3:
            etiquette(c, 540, 300, "LA MÊME PAIRE, NEUVE", prog(t, T_NEUVE - 0.05, 0.3, lambda v: rebond(v, 1.4)) * (1 - prog(t, T_ESSAIE - 0.55, 0.25, entree)), taille=44, rouge=False)
        # le gant neuf passe au bout de sa main et y reste
        v = prog(t, T_ESSAIE - 0.25, 0.7, entreeSortie)
        ax, ay = fa["main_d"]; bx, by = oj["main_d"]
        gant(c, mix(ax, bx, v) + 10, mix(ay, by, v) + 36 - 80 * math.sin(math.pi * v), 140,
             rot=mix(-18, -6, v), couleur=FOND2)
        if t >= T_ELLELUIVA - 0.05:
            coche(c, X_D + 150, 700, 78, t, T_ELLELUIVA - 0.05, BLANC, 20)
            chiffre_geant(c, "ELLE LUI VA", 540, 300, t, T_ELLELUIVA - 0.05, 110, BLANC)
            chiffre_geant(c, "TRÈS BIEN.", 540, 410, t, TW(266) - 0.1, 110, ROUGE)


# ═════════════════════════════ sons — sobres, un par vrai évènement
son(0.50, "impact", -8)                       # le gant qui touche le sol
son(T_PROCUREUR - 0.05, "whoosh_court", -12)
son(T_30SEC - 0.05, "impact_doux", -9)
son(T_LUI - 0.05, "pop", -12)
son(T_LA, "whoosh_long", -11)
son(T_OJ - 0.45, "swipe", -13)
son(T_STAR - 0.05, "pop", -13)
son(T_JUGE - 0.1, "tick", -13)
son(T_NICOLE - 0.05, "clic", -13); son(T_RONALD - 0.05, "clic", -13)
son(T_UNAN - 0.1, "whoosh_bas", -12)
son(T_95 - 0.05, "impact_doux", -9)
son(T_PREUVE, "whoosh_court", -12)
son(T_DEUXGANTS - 0.05, "verre", -11); son(T_DEUXGANTS + 0.13, "verre", -12)
for t0 in (T_MARQUE, T_TAILLE, T_NUMERO): son(t0 - 0.05, "clic", -12)
son(T_PAIRES - 0.18, "impact_doux", -9)
son(T_JOURLA, "whoosh_court", -12)
son(T_ESSAIENT, "swipe", -13)
son(T_PETITS - 0.05, "pop", -13)
son(T_ENFACE - 0.05, "whoosh_bas", -12)
son(T_ONNEFAIT - 0.05, "pop", -13)
son(T_RISQUE - 0.1, "impact_doux", -10)
son(T_ETPUIS, "whoosh_court", -12)
son(T_AVOCAT - 0.35, "swipe", -13)
son(T_COURAGE - 0.05, "impact", -8)
son(T_SAPLACE - 0.1, "pop", -11)
son(T_CRAQUE, "montee", -11)
son(T_RECLAME - 0.05, "impact", -8)
son(T_ENTRER - 1.3, "swipe", -13); son(T_ENTRER - 0.1, "tampon", -11)
son(T_TROPTARD - 0.05, "impact", -7)
son(T_SIMPSON2, "whoosh_court", -12)
son(T_LATEX - 0.05, "blip", -13)
son(T_MAUVAIS - 0.5, "swipe", -12); son(T_MAUVAIS - 0.05, "pop", -11)
son(T_GRIMACE - 0.05, "croc", -12)
son(T_ARRIVEPAS - 0.05, "impact", -7)
son(T_SONAVOCAT - 0.2, "swipe", -13)
son(T_SI - 0.08, "verre", -10)
son(T_3OCT, "whoosh_long", -11)
son(T_NONCOUP - 0.05, "tampon", -6)
son(T_CEQUE - 0.05, "whoosh_bas", -11)
son(T_JAMAISVU - 0.15, "impact_doux", -9)
son(T_FABRICANT - 0.4, "swipe", -13)
son(T_NEUVE - 0.05, "pop", -12)
son(T_ESSAIE - 0.25, "swipe", -12)
son(T_ELLELUIVA - 0.05, "check", -6)
sons_signature_people(son, T_SIGN)

for a_, b_ in [(0.0, 0.8), (T_TROPTARD - 0.1, T_TROPTARD + 0.3),
               (T_ARRIVEPAS - 0.1, T_ARRIVEPAS + 0.3), (T_SIGN + 0.4, T_SIGN + 0.9)]:
    rapide(a_, b_)


# ═════════════════════════════ composition
def fond(c, t):
    fond_bonhomme(c, t)


def dessine(c, t):
    fond(c, t)
    s1(c, t); s2(c, t); s3(c, t); s4(c, t); s5(c, t)
    s6(c, t); s7(c, t); s8(c, t); s9(c, t); s10(c, t)
    if t >= T_SIGN - 0.12:
        signature_people(c, t, T_SIGN, MEDIAS)
    filigrane(c, 0.26 * (1 - prog(t, T_SIGN - 0.2, 0.2, entree)))
    K.dessine_eclairs(c, t)
    if t < T_SIGN - 0.02:
        SOUS.dessine(c, t, BLANC)
