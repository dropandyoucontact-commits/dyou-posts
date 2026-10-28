"""AC-M01 v4 — chaîne RECTO CERVEAU (Films · Séries · Actu people), habillage NOIR figé.

La v3 a été validée telle quelle — « c'est parfait, la dernière vidéo, la voix, tout ». On ne
retouche donc ni le script, ni la voix, ni le montage, ni un seul repère temporel. Changent
seulement, à la demande de son associé qui tient le compte (28/10/2026) :
  - **fond noir**, grille en perspective qui bouge, **accent rouge et blanc** → `moteur/people.py`
  - **texte et médias plus grands** → les tailles ci-dessous
À partir d'ici l'habillage est FIGÉ : c'est le format de la chaîne.

Corrections demandées par Youssef le 27/10/2026, après la v2 :
  - **une minute minimum** (1'02) : c'est le seuil de monétisation. 63 s de voix ici.
  - **phrases complètes mais courtes et simples** — règle de son associé, qui tient le compte :
    quelqu'un qui ne connaît pas le sujet doit comprendre. 32 phrases, 8-9 mots en moyenne.
  - **cadre élargi, plus rien qui se chevauche** : l'aiguille du compteur passait sur les chiffres,
    des lettres se croisaient. Corrigé dans `people.py` (LARG_T 950 en haut, pastille sur l'anneau).
  - **de vraies vidéos de lui**, pas seulement des photos : extraits YouTube (360p seulement, d'où
    le cadre 16:9 large plutôt qu'un recadrage portrait qui ferait ressortir l'agrandissement).

Voix **Kael** (`yG4Uc56cLYQyZFnWaYv2`), grave, ralentie à 4,33 mots/s (elle sortait à 4,65).

Sujet : Eric Bauza, voix moderne de Bugs Bunny, mort le 25/10/2026 à 46 ans (NYT, WP, AP, CNN).
Angle : il a supplié un studio en public, avec la voix de Daffy, pour qu'un film enterré sorte.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import lettres, eclats, entre, rayons
from people import *
import people

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 3.2, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = sous_titres_people(K, fusions={(42, 43): "Bugs Bunny.", (48, 49): "Daffy Duck,",
                               (54, 55): "Porky Pig.", (64, 65): "Looney Tunes.",
                               (83, 84): "Woody Woodpecker,", (90, 91, 92): "Super Mario Bros.",
                               (98, 99): "Mel Blanc", (106, 107): "Mel Blanc,",
                               (136, 137): "Looney Tunes.", (203, 204): "Daffy Duck."})

PORTRAIT = "bauza-portrait-detoure"
GALA = "photos/bauza-annie"
V_PODCAST, V_ANNIE1, V_ANNIE2, V_DEMO = "videos/podcast", "videos/annie1", "videos/annie2", "videos/demo"
MEDIAS = [(PORTRAIT, False), (GALA, True)]

# ───────────────────────────── repères, tous accrochés à un mot
T_TU, T_MAIS1, T_VISAGE = TW(0), TW(9), TW(15)
T_NOM, T_MORT, T_AGE, T_COEUR, T_PREVENIR = TW(18), TW(23), TW(28), TW(31), TW(35)
T_VOIX = TW(38)
T_PERSOS = [TW(42), TW(48), TW(51), TW(54)]
NOMS = ["BUGS BUNNY", "DAFFY DUCK", "TITI", "PORKY PIG"]
T_VINGT, T_ROLES, T_EMMY, T_PRIX = TW(56), TW(66), TW(69), TW(72)
T_AUTRES, T_WOODY, T_MARIO = TW(80), TW(83), TW(90)
T_AVANT, T_MELBLANC, T_DIEU = TW(93), TW(98), TW(112)
T_PIVOT, T_PERSONNE, T_RACONTE = TW(115), TW(119), TW(121)
T_DEUXANS, T_DOUBLE = TW(124), TW(138)
T_ETPUIS, T_JAMAIS, T_TIROIR = TW(145), TW(153), TW(162)
T_REFUS, T_MONTE, T_METIER = TW(165), TW(171), TW(180)
T_SUPPLIE, T_PASSAVOIX, T_AVECDAFFY = TW(185), TW(192), TW(199)
T_ILADIT = TW(205)
T_CEDER, T_SORTI, T_CENT = TW(220), TW(226), TW(233)
T_GAGNE, T_MOIS, T_ALLAIT = TW(239), TW(242), TW(248)
T_VEILLE, T_PHOTO, T_SOURIAIT = TW(250), TW(255), TW(262)
T_CTA, T_COMMENT, T_ELEVE = TW(263), TW(265), TW(269)
T_SIGN = round(K.timing["duree_voix"] - 0.05, 2)
T_FIN = DUREE


def vitesse_grille(t):
    """le décor avance ; il accélère sur les bascules, il se fige quand il s'en va"""
    v = 0.5
    for t0 in (T_PIVOT, T_REFUS, T_CEDER, T_GAGNE, T_CTA):
        v += 2.4 * max(0.0, 1 - abs(t - t0) / 0.55) ** 2
    if t > T_MOIS - 0.1:
        v *= 1 - 0.85 * prog(t, T_MOIS - 0.1, 1.0, sortie) * (1 - prog(t, T_VEILLE - 0.2, 0.4, sortie))
    return v


def ondes_sol(c, t, t0, a=1.0, n=5, vitesse=0.75):
    """la voix : des anneaux qui partent du point de fuite et viennent vers nous, à même le sol"""
    if a <= 0.01: return
    for k in range(n):
        u = ((t - t0) * vitesse + k / n) % 1.0
        z = mix(7.0, 0.55, u ** 1.5)
        y = HORIZON + SOL / z
        rx = 1500 / z
        al = a * 0.62 * math.sin(math.pi * min(1.0, u * 1.08)) ** 0.7
        if y > H + 500 or al <= 0.01: continue
        c.drawOval(skia.Rect.MakeXYWH(AXE - rx, y - rx * 0.20, 2 * rx, 0.40 * rx),
                   peinture(ROUGE, al, Style=skia.Paint.kStroke_Style, StrokeWidth=4 + 22 * (1 - z / 7)))


def bobine(c, t, cx, cy, r, u):
    """la bobine de film ; u = 0 au point de fuite, 1 au premier plan"""
    if u <= 0.01: return
    z = mix(6.0, 1.0, sortieExpo(borne(u)))
    s = echelle_z(z)
    px, py = mix(AXE, cx, sortieExpo(borne(u))), mix(HORIZON, cy, sortieExpo(borne(u)))
    c.save(); c.translate(px, py); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, borne(u * 4)):
        pose_sol(c, cx, cy + r, r * 2.1, 0.3)
        disque(c, cx, cy, r, BLANC, 1.0)
        anneau(c, cx, cy, r, ROUGE, 8)
        anneau(c, cx, cy, r * 0.21, NOIR, 7)
        for k in range(6):
            a = t * 1.6 + k * math.pi / 3
            disque(c, cx + math.cos(a) * r * 0.58, cy + math.sin(a) * r * 0.58, r * 0.185, NOIR, 0.95)
    c.restore()


# ═════════════════════════════ 1. HOOK
def hook(c, t):
    if t > T_NOM + 0.25: return
    sor = prog(t, T_NOM - 0.18, 0.3, entree)
    with Calque(c, 1 - sor):
        ondes_sol(c, t, -0.1, 1.0)
        av = prog(t, T_MAIS1 - 0.2, 0.9, sortieExpo)
        carte_photo(c, t, PORTRAIT, 240, 540, 560, 740, max(0.02, av * 0.5),
                    1.0, flou=1.0, detoure=True, z0=7.0)
        a1 = 1 - prog(t, T_MAIS1 - 0.2, 0.16, entree)
        if a1 > 0:
            titre(c, "TU AS ENTENDU SA VOIX", Y_T1, 112, t, T_TU - 0.3, alpha=a1, decal=0.016)
            titre(c, "DES MILLIERS DE FOIS", Y_T2, 112, t, TW(5) - 0.06, alpha=a1, decal=0.016)
        if t > T_MAIS1 - 0.22:
            titre(c, "MAIS TU N'AS JAMAIS", Y_T1, 110, t, T_MAIS1 - 0.06, decal=0.016)
            u = prog(t, T_VISAGE - 0.16, 0.2, sortieExpo)
            surlignage(c, "VU SON VISAGE", Y_T2, 132, u)
            titre(c, "VU SON VISAGE", Y_T2, 132, t, T_VISAGE - 0.08, couleur=PAPIER3,
                  effet="ressort", decal=0.024)


# ═════════════════════════════ 2. IDENTITÉ
def ecg(c, t, a):
    """la ligne du cœur, tracée à l'encre, qui s'aplatit sur « sans prévenir »"""
    y0, x0, x1, amp = 1215, 110, 970, 0.62
    u = borne((t - T_COEUR) / max(0.25, T_PREVENIR - T_COEUR + 0.05))
    plat = prog(t, T_PREVENIR - 0.02, 0.3, sortie)
    with Calque(c, a):
        trait(c, x0, y0, x1, y0, SABLE, 4, 0.8)
        p = skia.Path(); p.moveTo(x0, y0)
        n, dernier = 520, x0
        for k in range(1, n + 1):
            f = k / n
            if f > u: break
            x = mix(x0, x1, f); dernier = x
            ph = (f * 2.0) % 1.0
            if   ph < 0.50: dy = 0
            elif ph < 0.55: dy = -36
            elif ph < 0.60: dy = 96
            elif ph < 0.66: dy = -170
            elif ph < 0.72: dy = 72
            elif ph < 0.78: dy = -22
            else:           dy = 0
            p.lineTo(x, y0 + dy * amp * (1 - plat))
        c.drawPath(p, peinture(ROUGE, 1.0, Style=skia.Paint.kStroke_Style, StrokeWidth=9))
        disque(c, dernier, y0, 11, ROUGE)


def identite(c, t):
    if t < T_NOM - 0.4 or t > T_VOIX - 0.14: return
    sor = prog(t, T_VOIX - 0.4, 0.26, entree)
    with Calque(c, 1 - sor):
        rubrique(c, t, borne((t - T_NOM + 0.25) * 4), "DISPARITION")
        u = prog(t, T_NOM - 0.34, 0.5, lin)
        carte_photo(c, t, PORTRAIT, 290, 400, 460, 565, borne(u),
                    flou=1 - prog(t, T_NOM - 0.04, 0.26, sortie), detoure=True, z0=3.2)
        titre(c, "ERIC BAUZA", 990, 128, t, T_NOM - 0.02, effet="ressort", decal=0.024)
        if t > T_MORT - 0.14:
            bloc(c, "MORT DIMANCHE", AXE - 159, 1345, entre(t, T_MORT - 0.08), taille=48, rot=-1.5)
        if t > T_AGE - 0.12:
            bloc(c, "46 ANS", AXE + 211, 1345, entre(t, T_AGE - 0.07), taille=48, couleur=ROUGE, rot=1.5)
        a_e = entre(t, T_NOM + 0.1, 0.4, 2.0) * (1 - prog(t, T_VOIX - 0.5, 0.25, entree))
        if a_e > 0.01:
            trait(c, 110, 1215, 970, 1215, GRIS, 4, 0.8 * a_e)      # la ligne attend, posée
        if t > T_COEUR - 0.14:
            a = prog(t, T_COEUR - 0.1, 0.3, sortie) * (1 - prog(t, T_VOIX - 0.5, 0.25, entree))
            if a > 0.01:
                ecg(c, t, a)


# ═════════════════════════════ 3. LES VOIX — l'extrait de podcast
def les_voix(c, t):
    if t < T_VOIX - 0.3 or t > T_VINGT - 0.16: return
    ent = prog(t, T_VOIX - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_VINGT - 0.4, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "QUI C'ÉTAIT")
        titre(c, "C'ÉTAIT SA VOIX", Y_T1, 120, t, T_VOIX - 0.05, decal=0.02)
        u = prog(t, T_VOIX - 0.22, 0.42, lin)
        carte_video(c, t, V_PODCAST, 90, 585, 900, 506, borne(u), t0=T_VOIX - 0.2, z0=3.4)
        for k, t0 in enumerate(T_PERSOS):
            suivant = T_PERSOS[k + 1] if k + 1 < len(T_PERSOS) else T_VINGT
            if t < t0 - 0.14 or t > suivant - 0.02: continue
            a = 1 - prog(t, suivant - 0.13, 0.09, entree)
            bloc(c, NOMS[k], AXE, 1250, entre(t, t0 - 0.09), a, taille=80,
                 couleur=ROUGE if k % 2 else ENCRE, rot=-1.5 if k % 2 else 1.5)


# ═════════════════════════════ 4. LES CHIFFRES
def chiffres(c, t):
    if t < T_VINGT - 0.3 or t > T_AUTRES - 0.16: return
    ent = prog(t, T_VINGT - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_AUTRES - 0.4, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "VINGT ANS DE CARRIÈRE")
        titre(c, "IL A FAIT PARLER", Y_T1, 106, t, T_VINGT - 0.05, decal=0.016)
        titre(c, "LES LOONEY TUNES", Y_T2, 114, t, TW(63) - 0.06, rouge=True, decal=0.018)
        # la jauge VIDE arrive dès l'annonce et ne se remplit que sur « quatre cents rôles » :
        # sinon l'écran reste nu 2,2 s entre le titre et le chiffre (règle « jamais de vide »).
        arr = prog(t, T_VINGT - 0.14, 0.5, sortieExpo)
        if arr > 0.01:
            u = prog(t, T_ROLES - 0.06, 0.45, lin)
            z = mix(5.0, 1.0, arr)
            # elle occupe d'abord le bas de l'écran (y 960) et ne remonte qu'au moment où
            # « 3 Emmy Awards » vient prendre la place sous elle
            place = prog(t, T_EMMY - 0.25, 0.4, sortie)
            cy_g, r_g = mix(960, 880, place), mix(168, 158, place)
            c.save(); c.translate(AXE, mix(HORIZON, cy_g, arr))
            c.scale(echelle_z(z), echelle_z(z)); c.translate(-AXE, -cy_g)
            with Calque(c, borne(arr * 3)):
                pose_sol(c, AXE, cy_g + r_g + 24, 440, 0.22)
                donut(c, AXE, cy_g, r_g, u, [(0.88, ROUGE)], t, ep=44 - 2 * place, graduations=20)
                compteur(c, 400, "", AXE, cy_g, u, 140, sous="rôles")
            c.restore()
        if t > T_EMMY - 0.16:
            a = entre(t, T_EMMY - 0.09)
            bloc(c, "3 EMMY AWARDS", AXE, 1155, a, taille=70)
        if t > T_PRIX - 0.14:
            titre(c, "LE PLUS GRAND PRIX", 1245, 58, t, T_PRIX - 0.06, decal=0.008)
            titre(c, "DE LA TÉLÉ AMÉRICAINE", 1320, 58, t, TW(76) - 0.05, decal=0.008)


# ═════════════════════════════ 5. LES AUTRES RÔLES
def autres(c, t):
    if t < T_AUTRES - 0.3 or t > T_AVANT - 0.16: return
    ent = prog(t, T_AUTRES - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_AVANT - 0.4, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "PAS QUE LES LOONEY TUNES")
        titre(c, "IL DOUBLAIT AUSSI", Y_T1, 112, t, T_AUTRES - 0.05, decal=0.016)
        u = prog(t, T_AUTRES - 0.2, 0.42, lin)
        carte_video(c, t, V_DEMO, 90, 550, 900, 506, borne(u), t0=T_AUTRES - 0.18, z0=3.4)
        if t > T_WOODY - 0.14:
            bloc(c, "WOODY WOODPECKER", AXE, 1165, entre(t, T_WOODY - 0.08), taille=66, rot=-1.5)
        if t > T_MARIO - 0.14:
            bloc(c, "SUPER MARIO BROS", AXE, 1305, entre(t, T_MARIO - 0.08), taille=66,
                 couleur=ROUGE, rot=1.5)


# ═════════════════════════════ 6. MEL BLANC
def melblanc(c, t):
    if t < T_AVANT - 0.3 or t > T_PIVOT - 0.18: return
    ent = prog(t, T_AVANT - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_PIVOT - 0.42, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "AVANT LUI")
        titre(c, "AVANT LUI, CES VOIX,", Y_T1, 96, t, T_AVANT - 0.05, decal=0.012)
        if t > T_MELBLANC - 0.16:
            u = prog(t, T_MELBLANC - 0.16, 0.2, sortieExpo)
            surlignage(c, "C'ÉTAIT MEL BLANC", Y_T2 + 10, 122, u)
            titre(c, "C'ÉTAIT MEL BLANC", Y_T2 + 10, 122, t, T_MELBLANC - 0.08,
                  couleur=PAPIER3, effet="ressort", decal=0.02)
        # « avant lui, ces voix » : on le remontre en train de les faire, puis la coupure prend
        # le relais sur la citation. Sans ce plan l'écran restait vide 2,4 s.
        sor_v = prog(t, TW(103) - 0.34, 0.26, entree)
        if sor_v < 0.99:
            uv = prog(t, T_AVANT - 0.18, 0.42, lin)
            carte_video(c, t, V_PODCAST, 90, 640, 900, 506, borne(uv), 1 - sor_v,
                        t0=T_AVANT - 0.18 - 11.0, z0=3.4)
        if t > TW(103) - 0.14:
            document(c, t, ["« Mel Blanc, pour moi,", "c'est la voix de Dieu. »"],
                     AXE, 1010, 700, entre(t, TW(103) - 0.08), "Eric Bauza")
        if t > T_DIEU - 0.14:
            titre(c, "LA VOIX DE DIEU", 1285, 94, t, T_DIEU - 0.07, rouge=True,
                  effet="ressort", decal=0.024)


# ═════════════════════════════ 7. PIVOT
def pivot(c, t):
    if t < T_PIVOT - 0.26 or t > T_DEUXANS + 0.2: return
    ent = prog(t, T_PIVOT - 0.24, 0.28, sortie)
    sor = prog(t, T_DEUXANS - 0.2, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rayons(c, AXE, 880, t, 1100, 0.11, 16, ROUGE)
        titre(c, "MAIS VOILÀ CE QUE", 560, 118, t, T_PIVOT - 0.04, effet="ressort", decal=0.018)
        if t > T_PERSONNE - 0.16:
            u = prog(t, T_PERSONNE - 0.16, 0.2, sortieExpo)
            surlignage(c, "PERSONNE", 700, 148, u)
            titre(c, "PERSONNE", 700, 148, t, T_PERSONNE - 0.06, couleur=PAPIER3, decal=0.022)
        if t > T_RACONTE - 0.14:
            titre(c, "NE RACONTE SUR LUI.", 932, 100, t, T_RACONTE - 0.06, effet="ressort", decal=0.014)


# ═════════════════════════════ 8-9. LE FILM ENTERRÉ
def enterre(c, t):
    if t < T_DEUXANS - 0.3 or t > T_REFUS - 0.16: return
    ent = prog(t, T_DEUXANS - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_REFUS - 0.42, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "LE DOSSIER")
        titre(c, "UN STUDIO AVAIT TOURNÉ", Y_T1, 94, t, T_DEUXANS - 0.05, decal=0.012)
        if t > TW(134) - 0.14:
            titre(c, "UN FILM LOONEY TUNES", Y_T2, 106, t, TW(134) - 0.06, rouge=True, decal=0.014)
        arrive = prog(t, T_DEUXANS - 0.1, 0.5, sortieExpo)
        recul = prog(t, T_JAMAIS + 0.02, 0.5, entreeSortie)
        bobine(c, t, AXE, 880, 250, arrive * (1 - 0.93 * recul))
        if t > T_DOUBLE - 0.14:
            a = 1 - prog(t, T_ETPUIS - 0.22, 0.18, entree)
            if a > 0.01:
                bloc(c, "IL AVAIT TOUT DOUBLÉ", AXE, 1220, entre(t, T_DOUBLE - 0.08), a,
                     taille=64, rot=-1.5)
        if t > T_ETPUIS + 0.04:
            document(c, t, ["Le studio a retiré le film de son calendrier.",
                            "Aucune sortie prévue, nulle part."],
                     AXE, 1145, 720, entre(t, T_ETPUIS + 0.1), "archive")
        if t > T_TIROIR - 0.14:
            titre(c, "DANS UN TIROIR", 1318, 84, t, T_TIROIR - 0.06, rouge=True,
                  effet="ressort", decal=0.02)


# ═════════════════════════════ 10-12. IL MONTE SUR SCÈNE ET SUPPLIE
def sur_scene(c, t):
    if t < T_REFUS - 0.3 or t > T_CEDER - 0.18: return
    ent = prog(t, T_REFUS - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_CEDER - 0.44, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "CE QU'IL A FAIT")
        a_h = 1 - prog(t, T_SUPPLIE - 0.32, 0.18, entree)
        if a_h > 0.01:
            titre(c, "ERIC N'A PAS ACCEPTÉ.", Y_T1, 106, t, T_REFUS - 0.05, alpha=a_h, decal=0.014)
            if t > T_MONTE - 0.14:
                titre(c, "IL EST MONTÉ SUR SCÈNE", Y_T2, 94, t, T_MONTE - 0.06, alpha=a_h, decal=0.012)
        if t > T_SUPPLIE - 0.36:
            titre(c, "IL A SUPPLIÉ LE STUDIO", Y_T1, 102, t, T_SUPPLIE - 0.12, decal=0.012)
        u1 = prog(t, T_REFUS - 0.2, 0.42, lin)
        bascule = prog(t, T_AVECDAFFY - 0.3, 0.3, entree)
        if bascule < 0.99:
            carte_video(c, t, V_ANNIE1, 90, 585, 900, 506, borne(u1) * (1 - bascule),
                        t0=T_REFUS - 0.18, z0=3.4)
        if bascule > 0.01:
            carte_video(c, t, V_ANNIE2, 90, 585, 900, 506, bascule, t0=T_AVECDAFFY - 0.25, z0=1.6)
        if t > T_METIER - 0.14:
            a = entre(t, T_METIER - 0.08) * (1 - prog(t, T_SUPPLIE - 0.22, 0.16, entree))
            if a > 0.01:
                bloc(c, "DEVANT TOUT LE MÉTIER", AXE, 1210, 1.0, a, taille=64, rot=-1.5)
        if t > T_PASSAVOIX - 0.14:
            a = 1 - prog(t, T_ILADIT - 0.32, 0.18, entree)
            if a > 0.01:
                titre(c, "PAS AVEC SA VOIX À LUI", 1160, 74, t, T_PASSAVOIX - 0.06,
                      alpha=a, decal=0.01)
                if t > T_AVECDAFFY - 0.16:
                    u = prog(t, T_AVECDAFFY - 0.16, 0.2, sortieExpo)
                    surlignage(c, "AVEC LA VOIX DE DAFFY", 1262, 80, u * a)
                    titre(c, "AVEC LA VOIX DE DAFFY", 1262, 80, t, T_AVECDAFFY - 0.07,
                          couleur=PAPIER3, effet="ressort", decal=0.012, alpha=a)
        if t > T_ILADIT - 0.14:
            document(c, t, ["« C'est le personnage qui sait", "le mieux supplier. »"],
                     AXE, 1230, 720, entre(t, T_ILADIT - 0.08), "Eric Bauza")


# ═════════════════════════════ 13. LE STUDIO CÈDE
def cedent(c, t):
    if t < T_CEDER - 0.44 or t > T_GAGNE - 0.2: return
    ent = prog(t, T_CEDER - 0.42, 0.3, sortieExpo)
    sor = prog(t, T_GAGNE - 0.48, 0.28, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "CE QUI S'EST PASSÉ")
        titre(c, "LE STUDIO A CÉDÉ.", Y_T1, 128, t, T_CEDER - 0.05, rouge=True,
              effet="ressort", decal=0.024)
        if t > T_SORTI - 0.14:
            titre(c, "LE FILM EST SORTI", Y_T2, 96, t, T_SORTI - 0.06, decal=0.012)
        bobine(c, t, AXE, 880, 220, prog(t, T_CEDER - 0.1, 0.55, sortieExpo))
        eclats(c, AXE, 880, t, T_CEDER, 14, 360, [ROUGE, ENCRE, SABLE], 5, 0.8)
        if t > T_CENT - 0.16:
            u = prog(t, T_CENT - 0.06, 0.38, lin)
            compteur(c, 100, " M$", AXE, 1210, u, 140, sous="au box-office")


# ═════════════════════════════ 14. IL A GAGNÉ, PUIS IL S'EN VA
def gagne(c, t):
    if t < T_GAGNE - 0.4 or t > T_VEILLE - 0.18: return
    ent = prog(t, T_GAGNE - 0.38, 0.3, sortieExpo)
    sor = prog(t, T_VEILLE - 0.46, 0.3, entree)
    with Calque(c, ent * (1 - sor)):
        a_g = 1 - prog(t, T_MOIS - 0.3, 0.16, entree)
        if a_g > 0.01:
            u = prog(t, T_GAGNE - 0.15, 0.2, sortieExpo)
            surlignage(c, "IL AVAIT GAGNÉ", 620, 140, u)
            titre(c, "IL AVAIT GAGNÉ", 620, 140, t, T_GAGNE - 0.04, couleur=PAPIER3,
                  effet="ressort", decal=0.024, alpha=a_g)
            titre(c, "SON COMBAT.", 800, 110, t, TW(240) - 0.05, alpha=a_g, decal=0.02)
            confettis(c, AXE, 700, t, T_GAGNE, 20, 320, 4, [ROUGE, ENCRE, SABLE, ROUGE2])
            ondes_sol(c, t, T_GAGNE - 0.2, 0.8 * a_g, 5, 0.85)
        if t > T_MOIS - 0.16:
            titre(c, "QUELQUES MOIS PLUS TARD,", Y_T1, 86, t, T_MOIS - 0.06, decal=0.01)
            titre(c, "IL S'EN ALLAIT.", Y_T2, 106, t, T_ALLAIT - 0.12, rouge=True, decal=0.02)
            dep = prog(t, T_ALLAIT - 0.5, 1.1, douce)
            carte_photo(c, t, PORTRAIT, 290, 690, 460, 575, mix(0.95, 0.06, dep),
                        1.0, detoure=True, z0=1.05)


# ═════════════════════════════ 15. LA VEILLE
def veille(c, t):
    if t < T_VEILLE - 0.4 or t > T_CTA + 0.18: return
    ent = prog(t, T_VEILLE - 0.38, 0.3, sortieExpo)
    sor = prog(t, T_CTA - 0.26, 0.26, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "24 H AVANT")
        titre(c, "LA VEILLE DE SA MORT,", Y_T1, 94, t, T_VEILLE - 0.05, decal=0.012)
        u = prog(t, T_VEILLE - 0.3, 0.45, lin)
        carte_photo(c, t, GALA, 275, 500, 490, 640, borne(u), zoom=1.05, fy=0.34, z0=3.2)
        if t > T_PHOTO - 0.12:
            titre(c, "IL POSTAIT ENCORE UNE PHOTO", 1165, 62, t, T_PHOTO - 0.06, decal=0.006)
        if t > T_SOURIAIT - 0.16:
            titre(c, "IL SOURIAIT.", 1255, 116, t, T_SOURIAIT - 0.07, rouge=True,
                  effet="ressort", decal=0.026)


# ═════════════════════════════ 16. L'APPEL AU COMMENTAIRE
def cta(c, t):
    if t < T_CTA - 0.3 or t > T_SIGN + 0.08: return
    ent = prog(t, T_CTA - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_SIGN - 0.2, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        ondes_sol(c, t, T_CTA - 0.3, 0.7, 4, 0.8)
        titre(c, "QUEL DESSIN ANIMÉ", 560, 118, t, T_CTA - 0.04, decal=0.016)
        if t > T_ELEVE - 0.16:
            u = prog(t, T_ELEVE - 0.16, 0.2, sortieExpo)
            surlignage(c, "T'A ÉLEVÉ, TOI ?", 700, 130, u)
            titre(c, "T'A ÉLEVÉ, TOI ?", 700, 130, t, T_ELEVE - 0.07, couleur=PAPIER3,
                  effet="ressort", decal=0.024)
        if t > T_COMMENT + 0.2:
            bloc(c, "DIS-LE EN COMMENTAIRE", AXE, 1205, entre(t, T_COMMENT + 0.25), taille=62, rot=-1.5)


# ═════════════════════════════ sons
son(0.0, "impact", -3); son(0.0, "whoosh_long", -8)
son(T_MAIS1 - 0.1, "swipe", -11); son(T_VISAGE - 0.1, "tampon", -8)
son(T_NOM - 0.18, "impact_doux", -5); son(T_NOM + 0.06, "ching", -10)
son(T_MORT - 0.09, "pop", -9); son(T_AGE - 0.08, "pop", -10)
son(T_COEUR - 0.14, "whoosh_bas", -9); son(T_PREVENIR - 0.05, "impact", -6)
son(T_VOIX - 0.3, "whoosh", -9)
for t0 in T_PERSOS: son(t0 - 0.09, "pop", -9)
son(T_VINGT - 0.3, "whoosh", -9); son(T_ROLES - 0.1, "montee", -11); son(T_EMMY - 0.08, "check", -10)
son(T_AUTRES - 0.3, "whoosh_court", -9); son(T_WOODY - 0.08, "pop", -10); son(T_MARIO - 0.08, "pop", -10)
son(T_AVANT - 0.3, "whoosh", -9); son(T_MELBLANC - 0.1, "tampon", -8); son(T_DIEU - 0.07, "ching", -8)
son(T_VINGT - 0.16, "whoosh_court", -11); son(TW(103) - 0.3, "swipe", -11)
son(T_PIVOT - 0.24, "whoosh_long", -7); son(T_PERSONNE - 0.1, "tampon", -8)
son(T_RACONTE - 0.06, "impact_doux", -6)
son(T_DEUXANS - 0.24, "whoosh", -9); son(T_DOUBLE - 0.08, "pop", -10)
son(T_ETPUIS + 0.02, "verre", -9); son(T_JAMAIS + 0.02, "whoosh_bas", -8)
son(T_TIROIR - 0.07, "impact", -6)
son(T_REFUS - 0.26, "whoosh_long", -8); son(T_MONTE - 0.08, "pop", -10)
son(T_METIER - 0.08, "pop", -10); son(T_AVECDAFFY - 0.22, "swipe", -9)
son(T_AVECDAFFY - 0.1, "tampon", -8); son(T_ILADIT - 0.08, "verre", -10)
son(T_CEDER - 0.12, "impact", -4); son(T_CEDER + 0.08, "ching", -8)
son(T_SORTI - 0.06, "check", -9); son(T_CENT - 0.08, "montee", -10)
son(T_GAGNE - 0.14, "impact", -4); son(T_GAGNE + 0.05, "ching", -7)
son(T_MOIS - 0.14, "whoosh_bas", -9); son(T_ALLAIT - 0.4, "swipe", -11)
son(T_VEILLE - 0.24, "whoosh", -9); son(T_SOURIAIT - 0.08, "pop", -9)
son(T_CTA - 0.24, "whoosh_long", -7); son(T_ELEVE - 0.1, "tampon", -8)
son(T_COMMENT + 0.22, "pop", -9)
sons_signature_people(son, T_SIGN)

for a, b in [(0.0, 0.5), (T_NOM - 0.2, T_NOM + 0.3), (T_VOIX - 0.3, T_VOIX + 0.2),
             (T_VINGT - 0.3, T_VINGT + 0.2), (T_AUTRES - 0.3, T_AUTRES + 0.2),
             (T_AVANT - 0.3, T_AVANT + 0.2), (T_PIVOT - 0.26, T_PIVOT + 0.3),
             (T_DEUXANS - 0.24, T_DEUXANS + 0.25), (T_JAMAIS - 0.05, T_JAMAIS + 0.4),
             (T_REFUS - 0.26, T_REFUS + 0.3), (T_AVECDAFFY - 0.3, T_AVECDAFFY + 0.3),
             (T_CEDER - 0.12, T_CEDER + 0.45), (T_GAGNE - 0.14, T_GAGNE + 0.4),
             (T_ALLAIT - 0.4, T_ALLAIT + 0.3), (T_VEILLE - 0.24, T_VEILLE + 0.3),
             (T_CTA - 0.24, T_CTA + 0.4), (T_SIGN + 0.4, T_SIGN + 0.9)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, ROUGE, 0.08), (T_NOM, ENCRE, 0.10), (T_PREVENIR, ROUGE, 0.12),
                    (T_PIVOT, ENCRE, 0.09), (T_TIROIR, ENCRE, 0.10), (T_AVECDAFFY, ROUGE, 0.11),
                    (T_CEDER, ROUGE, 0.12), (T_GAGNE, ROUGE, 0.12), (T_CTA, ROUGE, 0.09)]:
    eclair(tt, cc_, a_)


# ═════════════════════════════ composition
def fond(c, t):
    """le décor seul — `outils/vide.py` s'en sert comme référence pour traquer les images vides"""
    pulse = (battement(t, T_NOM, 1, 0.5) - 1) + (battement(t, T_CEDER, 1, 0.5) - 1) \
          + (battement(t, T_GAGNE, 1, 0.5) - 1)
    fond_grille(c, t, pulse, vitesse=vitesse_grille(t))


def dessine(c, t):
    fond(c, t)
    hook(c, t); identite(c, t); les_voix(c, t); chiffres(c, t); autres(c, t)
    melblanc(c, t); pivot(c, t); enterre(c, t); sur_scene(c, t); cedent(c, t)
    gagne(c, t); veille(c, t); cta(c, t)
    if t >= T_SIGN - 0.12:
        signature_people(c, t, T_SIGN, MEDIAS)
    filigrane(c, 0.22 * (1 - prog(t, T_SIGN - 0.2, 0.2, entree)))
    K.dessine_eclairs(c, t)
    if t < T_SIGN - 0.02:
        SOUS.dessine(c, t, ENCRE)
