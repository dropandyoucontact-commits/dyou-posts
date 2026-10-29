"""DA-M19 (29/10/2026) — première pub « sites » en FRANÇAIS et au format long (1 minute).

Hook choc décontextualisé, demandé par Youssef : « il y a quelqu'un qui travaille contre toi,
chaque nuit, pendant que tu dors, tu le paies tous les mois, et c'est toi qui l'as choisi » —
on croit à un employé, une fiche de personnel s'assemble avec un visage masqué, et la fiche
pivote sur « c'est ton site internet » pour révéler un navigateur. La phrase ne se comprend
qu'après coup.

Corps français : moteur/sites3d_fr.py (les scènes de sites3d rejouées en français, faux sites
compris) + les quatre blocs du format long : la perte silencieuse, les trois objections,
le test du téléphone, la nuit qui cherche. Fin : signature 3D DYOU (verre_studio).
"""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio3d import *
import sites3d_fr as fr
from sites3d_fr import site_vieux_fr, site_moderne_fr, PW, PH, tel
import verre_studio as vs
vs.appliquer()
fr.francais()

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 2.0, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

# ─────────────────────────────────────────── repères, posés sur les index réels du script
IDX = dict(g0=41, cherche=43, google=45, site=47, lent=49, date=50, illisible=51, tel_=53,
           donc=54, appelle=56, autre=58,
           sil0=59, dira=63, suivant=76, jamais=84,
           v0=103, vendeur=108,
           b0=125, moderne=129, rapide=130, mobile=134, offre=137, bouton=141, devant=145,
           s0=146, trouve=149, google2=151,
           m0=152, maquette=155, gratuit=160,
           obj0=161, trois=166, obj1=168, rep1=173, obj2=182, rep2=186, obj3=196, rep3=199,
           test0=202, compte=210, client=219,
           nuit0=220, cherchent=228, question=232,
           decolle=242, take=244, business=246, devis=247)
M = {k: TW(v) for k, v in IDX.items()}
M["url"] = M["devis"] + 1.1
SOUS = sous_titres(K)
T_B1 = M["g0"]

T_CONTRE, T_NUIT, T_PAIES, T_CHOISI, T_SITE, T_VOILA = TW(5), TW(8), TW(16), TW(25), TW(26), TW(30)
FW, FH = 680, 880


# ─────────────────────────────────────────── le hook : la fiche employé qui se révèle navigateur
def fiche(t, paie, tampon):
    """fiche de personnel : photo masquée, poste vide, ligne de prélèvement, tampon « choisi par toi »"""
    def f(c, w, h):
        k = w / FW
        rrect(c, 0, 0, w, h, 34 * k, "#FFFFFF", 1.0, None, S["ligne"], 3 * k)
        rrect(c, 0, 0, w, 96 * k, 0, S["doux"])
        texte(c, "FICHE DE PERSONNEL", 36 * k, 34 * k, 26 * k, S["gris"], "fort", track=0.06)
        # la photo masquée
        rrect(c, 36 * k, 140 * k, 200 * k, 240 * k, 24 * k, S["doux"])
        icone(c, "user-round", 136 * k, 240 * k, 120 * k, "#C7C2D2", 2.0)
        texte(c, "?", 136 * k, 300 * k, 90 * k, S["gris"], "noir", "centre", -0.03)
        # les lignes d'identité, floutées
        for j, lg in enumerate([0.78, 0.52, 0.64]):
            rrect(c, 270 * k, (160 + j * 60) * k, (w - 320 * k) * lg, 22 * k, 11 * k, S["ligne"])
        texte(c, "Poste : ?", 270 * k, 350 * k, 30 * k, S["gris"], "titre", track=-0.02)
        # horaires : toutes les nuits
        rrect(c, 36 * k, 430 * k, w - 72 * k, 110 * k, 26 * k, "#FFFFFF", 1.0, None, S["ligne"], 2 * k)
        icone(c, "moon", 96 * k, 485 * k, 48 * k, S["violet"], 2.4)
        texte(c, "Horaires : toutes les nuits", 146 * k, 485 * k - hauteurLigne(32 * k, "titre") / 2, 32 * k, S["encre"], "titre", track=-0.02)
        # la ligne de prélèvement, qui arrive sur « tu le paies »
        if paie > 0:
            with Calque(c, borne(paie * 3)):
                rrect(c, 36 * k, 570 * k, w - 72 * k, 110 * k, 26 * k, "#FFFFFF", 1.0, None, S["rouge"], 3 * k)
                icone(c, "credit-card", 96 * k, 625 * k, 46 * k, S["rouge"], 2.4)
                texte(c, "Prélevé tous les mois", 146 * k, 625 * k - hauteurLigne(32 * k, "titre") / 2, 32 * k, S["rouge"], "titre", track=-0.02)
        # le tampon « choisi par toi »
        if tampon > 0:
            c.save(); c.translate(w * 0.62, 760 * k); c.rotate(-11)
            z = mix(2.2, 1, borne(tampon))
            c.scale(z, z)
            with Calque(c, borne(tampon * 3)):
                rrect(c, -190 * k, -46 * k, 380 * k, 92 * k, 16 * k, None, 1.0, None, S["encre"], 5 * k)
                texte(c, "CHOISI PAR TOI", 0, -hauteurLigne(34 * k, "noir") / 2, 34 * k, S["encre"], "noir", "centre", 0.04)
            c.restore()
    return f


def navigateur(t):
    """l'autre face de la fiche : un navigateur ouvert sur le vieux site"""
    def f(c, w, h):
        k = w / FW
        rrect(c, 0, 0, w, h, 34 * k, "#FFFFFF", 1.0, None, S["ligne"], 3 * k)
        rrect(c, 0, 0, w, 86 * k, 0, S["doux"])
        for j, col in enumerate(["#FF6B6B", "#FFC53D", "#2E9E68"]): disque(c, (44 + j * 38) * k, 43 * k, 12 * k, col)
        rrect(c, 180 * k, 22 * k, w - 230 * k, 44 * k, 22 * k, "#FFFFFF")
        texte(c, "ton-site.fr", 212 * k, 30 * k, 26 * k, S["gris"], "demi", track=0)
        c.save(); c.translate(0, 86 * k); c.scale(1, (h - 86 * k) / h)
        site_vieux_fr(t, charge=True)(c, w, h)
        c.restore()
    return f


def hook(c, t):
    a = prog(t, -0.05, 0.6, lambda v: ressort(v, 1.3, 4.8))
    pivot = prog(t, T_SITE - 0.22, 0.55, entreeSortie)        # la fiche se retourne sur la révélation
    recul = prog(t, T_VOILA - 0.1, 0.6, entree)
    ang = 180 * pivot
    face_b = pivot > 0.5
    cam = Cam(ax=-7 + 3 * math.sin(t * 0.9), ay=mix(-38, -10, min(a, 1.1)) + 4 * math.sin(t * 0.7) + 16 * recul,
              tz=mix(1300, 300, min(a, 1.1)) + 700 * recul, cy=960)
    lueur_s(c, 540, 980, 640, S["violetVif"], 0.10 * prog(t, T_NUIT, 0.5))
    paie = entre(t, T_PAIES - 0.12, 0.45, 2.2) if t < T_SITE - 0.1 else borne((T_SITE - 0.1 - t) * 6 + 1)
    tamp = prog(t, T_CHOISI - 0.1, 0.35, lambda v: ressort(v, 1.2, 5.0)) if t < T_SITE - 0.1 else borne((T_SITE - 0.1 - t) * 6 + 1)
    contenu = navigateur(t) if face_b else fiche(t, paie, tamp)
    plans = [Plan(coins((0, 40, 0), FW, FH, ay=ang if not face_b else ang - 180), FW, FH, contenu)]
    scene3d(c, cam, plans)
    # textes du hook
    if t < T_NUIT - 0.1:
        with Calque(c, 1 - prog(t, T_NUIT - 0.25, 0.2)):
            lettres(c, "QUELQU'UN", 540, 170, 118, t, -0.25, "ressort", decal=0.03, grad=False, couleur=S["encre"])
            lettres(c, "TRAVAILLE", 540, 290, 118, t, T_CONTRE - 0.14, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
            lettres(c, "CONTRE TOI.", 540, 410, 124, t, T_CONTRE + 0.12, "ressort", decal=0.035)
    if T_NUIT - 0.15 < t < T_SITE - 0.15:
        with Calque(c, 1 - prog(t, T_SITE - 0.3, 0.2)):
            lettres(c, "CHAQUE NUIT.", 540, 200, 110, t, T_NUIT - 0.1, "ressort", decal=0.035, grad=False, couleur=S["encre"])
            if t > T_PAIES - 0.2:
                lettres(c, "ET TU LE PAIES.", 540, 320, 104, t, T_PAIES - 0.12, "masque", grad=True, decal=0.03, duree=0.35)
    if t > T_SITE - 0.15:
        with Calque(c, 1 - prog(t, T_VOILA - 0.15, 0.25)):
            lettres(c, "C'EST TON SITE.", 540, 230, 132, t, T_SITE - 0.1, "ressort", decal=0.04)


# ─────────────────────────────────────────── bruitages
son(0.0, "whoosh_bas", -8); son(0.05, "pop", -12); son(0.3, "impact", -6); son(0.33, "verre", -12)
son(T_CONTRE - 0.14, "whoosh_court", -10); son(T_CONTRE + 0.12, "impact_doux", -8)
son(T_NUIT - 0.1, "montee", -12); son(T_PAIES - 0.12, "croc", -10); son(T_PAIES, "tampon", -9)
son(T_CHOISI - 0.1, "tampon", -6); son(T_CHOISI, "impact", -8)
son(T_SITE - 0.22, "swipe", -7); son(T_SITE - 0.1, "impact", -5); son(T_SITE + 0.1, "verre", -10)
son(T_VOILA - 0.1, "whoosh_long", -9)
fr.sons_fr(K, M)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.5), (T_CONTRE + 0.1, T_CONTRE + 0.5), (T_CHOISI - 0.1, T_CHOISI + 0.4),
             (T_SITE - 0.25, T_SITE + 0.5), (T_B1 - 0.35, T_B1 + 0.1)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_CONTRE + 0.12, S["rouge"], 0.07), (T_SITE - 0.1, "#FFFFFF", 0.20),
                    (M["take"], "#FFFFFF", 0.22), (M["devis"] + 0.75, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)

T_SIG = M["devis"] - vs.T_BOUM
MEDIAS = ["modele0", "modele1", "vitrine", "modele2", "modele3"]
vs.sons_signature(son, T_SIG)


def dessine(c, t):
    fr.compose_fr(c, t, M, hook, T_B1, SOUS, K, 0.0)
    vs.signature(c, t, T_SIG, MEDIAS, [("Clique sur le lien.", M["devis"] + 0.25, 56)],
                 dict(label="Ma maquette offerte", t_bouton=M["devis"] + 0.45, t_clic=M["devis"] + 0.75,
                      url="dyou-agency.com", t_url=M["url"]))
