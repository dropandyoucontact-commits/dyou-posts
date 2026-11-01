"""DA-M22 (02/11/2026) — contenu à valeur, français, cible coachs sportifs.

Sujet : les trois critères que Google utilise pour classer les résultats locaux — pertinence,
distance, notoriété — vérifiés à la source le 02/11/2026 sur support.google.com/business/answer/7091
(« Local results are mainly based on relevance, distance, and prominence » ; la notoriété est
nourrie par « how many websites link to your business and how many reviews you have »).
Aucun chiffre, aucun classement promis : seulement ce que Google écrit lui-même.

Format DA-M20/M21 : hook choc décontextualisé, une idée par plan, preuve à l'écran, démo du site
de Floris, 490 € + mention sur-mesure, CTA « Enregistre la vidéo ».
Bruitages : règle du 30/10 — des `pop` et un `ding`, rien d'autre.
"""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio3d import *
from sites3d_fr import voile_bas
import verre_studio as vs
vs.appliquer()

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 2.0, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

IDX = dict(critere=4, google=6, changer=12,
           classe=18, trois=23, luimeme=29,
           c1=30, pertinence=32, propose=38, cherche0=42, cherche1=44,
           c2=45, distance=47, personne=52, celuila=55, controles=59, pas=60,
           c3=61, notoriete=63, nourrit=70, sites=74, avis=82,
           fiche=83, relier=91, siteoui=92,
           demo=95, site=99, ville=106, histoire=115, page=120,
           prix0=121, euros=129, celui=130,
           cta=140, video=142)
M = {k: TW(v) for k, v in IDX.items()}
SOUS = sous_titres(K)
PW_, PH_ = 470, 960
T_SIG = M["cta"] - vs.T_BOUM


def ecran(nom, zoom=1.0, fy=0.5):
    def f(c, w, h):
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#0B0A10"))
        image_cover(c, nom, 0, 0, w, h, zoom=zoom, fy=fy)
    return f


def ligne_carte(c, x, y, w, h, ic, lab, coul, alpha=1.0, taille=38):
    with Calque(c, alpha):
        carte_s(c, x, y, w, h, h / 2, "#FFFFFF", None, 0.14)
        disque(c, x + h / 2, y + h / 2, h * 0.33, coul)
        icone(c, ic, x + h / 2, y + h / 2, h * 0.38, "#FFFFFF", 3.0)
        texte(c, lab, x + h * 0.95, y + h / 2 - hauteurLigne(taille, "titre") / 2, taille, S["encre"], "titre", track=-0.02)


def radar(c, cx, cy, t, u, n_anneaux=4, r_max=360, alpha=1.0):
    """cercles de distance autour de la personne qui cherche + quelques points autour"""
    with Calque(c, alpha):
        for k in range(n_anneaux):
            v = borne((u - 0.08 * k) * 2.2)
            if v <= 0: continue
            r = r_max * (k + 1) / n_anneaux * v
            anneau(c, cx, cy, r, S["lilas"], 3, 0.55 * (1 - 0.14 * k))
        pulse = 0.5 + 0.5 * math.sin(t * 2.4)
        lueur_s(c, cx, cy, 120 * (0.8 + 0.25 * pulse), S["violetVif"], 0.26 * borne(u * 2))
        disque(c, cx, cy, 26 * borne(u * 2.5), S["violet"])
        icone(c, "user-round", cx, cy, 30 * borne(u * 2.5), "#FFFFFF", 3.0)


def epingle(c, x, y, s=1.0, alpha=1.0, actif=False):
    with Calque(c, alpha):
        c.save(); c.translate(x, y); c.scale(s, s)
        disque(c, 0, 0, 34, S["violet"] if actif else "#FFFFFF")
        if not actif: anneau(c, 0, 0, 34, S["ligne"], 3)
        icone(c, "map-pin", 0, 0, 34, "#FFFFFF" if actif else S["grisClair"], 2.8)
        c.restore()


# ─────────────────────────────────────────── 1. le hook
def scene_hook(c, t):
    g = Groupe(c, t, -0.1, M["c1"] - 0.06, ent="zoom", sor="gauche", d_out=0.3)
    if not g.visible: return
    with g:
        u = prog(t, M["critere"] - 0.3, 0.9, entree)
        radar(c, 540, 960, t, u, 4, 310, 1.0)
        for k, (x, y) in enumerate([(250, 760), (806, 840), (300, 1200), (786, 1180)]):
            e = entre(t, M["google"] - 0.1 + 0.1 * k, 0.4, 2.2)
            if e > 0: epingle(c, x, y, mix(1.5, 1, prog(t, M["google"] - 0.1 + 0.1 * k, 0.22, entree)), borne(e * 3))
        if t < M["classe"] - 0.3:
            with Calque(c, 1 - prog(t, M["classe"] - 0.46, 0.18)):
                lettres(c, "UN CRITÈRE", 540, 170, 132, t, -0.22, "ressort", decal=0.03, grad=False, couleur=S["encre"])
                lettres(c, "QUE TU NE PEUX", 540, 300, 96, t, M["critere"] - 0.14, "masque", grad=True, decal=0.03, duree=0.32)
                if t > M["changer"] - 0.34:
                    lettres(c, "PAS CHANGER.", 540, 410, 100, t, M["changer"] - 0.26, "ressort", decal=0.03,
                            grad=False, couleur=S["gris"])
        else:
            with Calque(c, 1 - prog(t, M["c1"] - 0.34, 0.2)):
                lettres(c, "GOOGLE EN A", 540, 190, 104, t, M["classe"] - 0.22, "masque", grad=False,
                        couleur=S["encre"], decal=0.03, duree=0.32)
                lettres(c, "TROIS.", 540, 310, 160, t, M["trois"] - 0.2, "ressort", decal=0.04)
                if t > M["luimeme"] - 0.34:
                    lettres(c, "IL LES ÉCRIT LUI-MÊME.", 540, 490, 60, t, M["luimeme"] - 0.26, "masque",
                            grad=False, couleur=S["gris"], decal=0.022, duree=0.3)


# ─────────────────────────────────────────── 2. la pertinence
def scene_c1(c, t):
    g = Groupe(c, t, M["c1"] - 0.1, M["c2"] - 0.06, ent="bas", sor="zoom", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Critère 1", 540, 160, 40, "encre", "target", 1.0, 1.0, rot=-2)
        lettres(c, "LA PERTINENCE", 540, 270, 108, t, M["pertinence"] - 0.2, "masque", grad=True, decal=0.03, duree=0.32)
        a = entre(t, M["propose"] - 0.2, 0.45, 1.8)
        if a > 0:
            with Calque(c, borne(a * 3)):
                carte_s(c, 150, 520, 700, 130, 65, "#FFFFFF", None, 0.16)
                icone(c, "search", 225, 585, 44, S["grisClair"], 2.8)
                n = int(borne((t - (M["propose"] - 0.1)) / 0.9) * 26)
                texte(c, "cours de muay thaï Le Puy"[:n], 275, 585 - hauteurLigne(36, "titre") / 2, 36, S["encre"], "titre", track=-0.02)
        for j, (cle, lab, ic) in enumerate([("propose", "Ce que tu proposes", "dumbbell"),
                                            ("cherche0", "Ce qui est cherché", "search")]):
            e = entre(t, M[cle] - 0.12, 0.42, 2.2)
            if e <= 0: continue
            ligne_carte(c, 150, 760 + j * 150, 700, 118, ic, lab, S["violet"], borne(e * 3))


# ─────────────────────────────────────────── 3. la distance
def scene_c2(c, t):
    g = Groupe(c, t, M["c2"] - 0.1, M["c3"] - 0.06, ent="droite", sor="gauche", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Critère 2", 540, 160, 40, "encre", "map-pin", 1.0, 1.0, rot=2)
        lettres(c, "LA DISTANCE", 540, 270, 122, t, M["c2"] + 0.05, "masque", grad=True, decal=0.03, duree=0.32)
        u = prog(t, M["distance"], 0.8, entree)
        radar(c, 500, 900, t, u, 3, 300, 1.0)
        for k, (x, y) in enumerate([(230, 700), (790, 760), (260, 1110), (760, 1090)]):
            e = entre(t, M["personne"] - 0.3 + 0.09 * k, 0.4, 2.2)
            if e > 0: epingle(c, x, y, 1.0, borne(e * 3))
        ct = entre(t, M["celuila"] + 0.05, 0.42, 2.0)
        if ct > 0:
            c.save(); c.rotate(-3, 500, 1270)
            pill(c, "Tu ne le contrôles pas", 500, 1270, 42, "rouge", "lock", borne(ct * 3),
                 mix(1.5, 1, prog(t, M["celuila"] + 0.05, 0.22, entree)))
            c.restore()


# ─────────────────────────────────────────── 4. la notoriété
def scene_c3(c, t):
    g = Groupe(c, t, M["c3"] - 0.1, M["demo"] - 0.08, ent="bas", sor="recul", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Critère 3", 540, 160, 40, "encre", "trending-up", 1.0, 1.0, rot=-2)
        lettres(c, "LA NOTORIÉTÉ", 540, 270, 116, t, M["c3"] + 0.05, "masque", grad=True, decal=0.03, duree=0.32)
        df = entre(t, M["notoriete"] + 0.25, 0.42, 2.0) * (1 - prog(t, M["nourrit"] - 0.35, 0.25))
        if df > 0:
            pill(c, "À quel point on te connaît", 500, 445, 38, "blanc", "users", borne(df * 3), 1.0, rot=-2)
        # ce que Google cite : des sites qui pointent vers toi, des avis
        av = 1 - prog(t, M["fiche"] - 0.2, 0.25)
        if av > 0:
            with Calque(c, av):
                n = entre(t, M["nourrit"] - 0.2, 0.42, 2.0)
                if n > 0:
                    pill(c, "Ce que Google cite", 500, 470, 36, "blanc", "file-text", borne(n * 3), 1.0, rot=2)
                for j, (cle, lab, ic) in enumerate([("sites", "Des sites qui parlent de toi", "share-2"),
                                                    ("avis", "Des avis", "star")]):
                    e = entre(t, M[cle] - 0.16, 0.42, 2.2)
                    if e <= 0: continue
                    ligne_carte(c, 150, 580 + j * 150, 700, 118, ic, lab, S["violet"], borne(e * 3))
        # la fiche seule : rien ne s'y rattache — puis le site arrive et les liens se branchent
        f_ = entre(t, M["fiche"] + 0.05, 0.45, 1.8)
        if f_ > 0:
            with Calque(c, borne(f_ * 3)):
                z = mix(1.35, 1, prog(t, M["fiche"] + 0.05, 0.26, entree))
                c.save(); c.translate(500, 920); c.scale(z, z); c.translate(-500, -920)
                carte_s(c, 310, 845, 380, 150, 46, "#FFFFFF", None, 0.2)
                disque(c, 390, 920, 40, S["grisClair"]); icone(c, "map-pin", 390, 920, 42, "#FFFFFF", 3.0)
                texte(c, "Ta fiche", 455, 920 - hauteurLigne(40, "titre") / 2, 40, S["encre"], "titre", track=-0.02)
                c.restore()
            # les trois attaches partent dans le vide…
            r = entre(t, M["relier"] - 0.16, 0.4, 2.2)
            if r > 0:
                s_ = prog(t, M["siteoui"] - 0.1, 0.45, entree)
                for k in range(3):
                    v = borne((r - 0.08 * k) * 2)
                    if v <= 0: continue
                    x1 = mix(500, 310 + k * 190, mix(0.45, 1.0, s_))
                    y1 = mix(1020, 1130, mix(0.4, 1.0, s_))
                    pa = peinture(S["ligne"] if s_ < 0.3 else S["lilas"], 0.95,
                                  Style=skia.Paint.kStroke_Style, StrokeWidth=5)
                    if s_ < 0.3: pa.setPathEffect(skia.DashPathEffect.Make([14, 12], 0))
                    c.drawLine(500, 1000, x1, y1, pa)
            # … jusqu'à ce qu'un site leur donne quelque chose à relier
            w_ = entre(t, M["siteoui"] - 0.1, 0.45, 1.8)
            if w_ > 0:
                with Calque(c, borne(w_ * 3)):
                    carte_s(c, 290, 1130, 420, 150, 46, "#FFFFFF", None, 0.22)
                    disque(c, 370, 1205, 42, S["violet"]); icone(c, "globe", 370, 1205, 44, "#FFFFFF", 3.0)
                    texte(c, "Ton site", 437, 1205 - hauteurLigne(40, "titre") / 2, 40, S["encre"], "titre", track=-0.02)


# ─────────────────────────────────────────── 5. le site de Floris
def scene_demo(c, t):
    g = Groupe(c, t, M["demo"] - 0.1, M["prix0"] - 0.06, ent="zoom", sor="haut", d_in=0.42)
    if not g.visible: return
    with g:
        a = entre(t, M["demo"], 0.5, 1.4)
        d = prog(t, M["histoire"] - 0.25, 0.45, entree)
        cam = Cam(ax=4 * math.sin(t * 0.8), ay=mix(32, -8, a) + 4 * math.sin(t * 0.7) + 16 * d,
                  tz=mix(1300, 300, a), cy=900, tx=mix(0, -110, d))
        contenu = ecran("floris-qui-suis-je", 1.0, 0.18) if d > 0.5 else ecran("floris-accueil", 1.55, 0.17)
        scene3d(c, cam, [Plan(coins((0, 40, 0), PW_, PH_), PW_, PH_, tel(contenu))])
        if t < M["site"] + 0.2:
            lettres(c, "REGARDE.", 540, 180, 120, t, M["demo"] - 0.05, "ressort", decal=0.035,
                    grad=False, couleur=S["encre"])
        else:
            pill(c, "Le site d'un coach", 540, 190, 38, "grad", "smartphone", 1.0, 1.0, rot=-2)
        for lab, ic, cle, fin, x, y, r, mode in [("Sa ville dès la 1re ligne", "map-pin", "ville", "histoire", 430, 600, -4, "blanc"),
                                                 ("Son histoire, une vraie page", "file-text", "histoire", None, 470, 1130, 3, "grad")]:
            e = entre(t, M[cle] - 0.12, 0.4, 2.4)
            if fin: e *= 1 - prog(t, M[fin] - 0.3, 0.28)
            if e <= 0: continue
            c.save(); c.translate(x, y + 8 * math.sin(t * 2)); c.rotate(r)
            z = mix(1.7, 1, prog(t, M[cle] - 0.12, 0.2, entree)); c.scale(z, z)
            pill(c, lab, 0, 0, 36, mode, ic, borne(e * 3))
            c.restore()


# ─────────────────────────────────────────── 6. le prix
def scene_prix(c, t):
    g = Groupe(c, t, M["prix0"] - 0.1, M["cta"] - 0.12, ent="bas", sor="zoom", d_in=0.42)
    if not g.visible: return
    with g:
        lettres(c, "UN SITE CHEZ NOUS", 540, 300, 78, t, M["prix0"] - 0.05, "masque", grad=False,
                couleur=S["encre"], decal=0.03, duree=0.32)
        e = entre(t, M["euros"] - 0.22, 0.5, 1.2)
        if e > 0:
            z = mix(2.2, 1, prog(t, M["euros"] - 0.22, 0.3, lambda v: ressort(v, 1.2, 4.6)))
            c.save(); c.translate(540, 640); c.scale(z, z); c.translate(-540, -640)
            lettres(c, "490 €", 540, 540, 230, t, M["euros"] - 0.18, "ressort", decal=0.05, onde_t=M["euros"] + 0.5)
            c.restore()
            eclats(c, 540, 640, t, M["euros"] + 0.1, 14, 460, graine=4)
        p = entre(t, M["euros"] + 0.35, 0.4, 2.2)
        if p > 0:
            pill(c, "Site vitrine, livré", 540, 900, 38, "blanc", "check", borne(p * 3), mix(0.4, 1, p), rot=-2)
        sm = entre(t, M["celui"] - 0.12, 0.45, 2.0)
        if sm > 0:
            with Calque(c, borne(sm * 3)):
                carte_s(c, 150, 1060, 710, 170, 44, "#FFFFFF", None, 0.18)
                icone(c, "sparkles", 240, 1145, 52, S["violet"], 2.4)
                texte(c, "Celui du coach : sur-mesure", 300, 1145 - hauteurLigne(36, "titre") / 2, 36, S["encre"], "titre", track=-0.02)


def dessine(c, t):
    fond_studio(c, t, 0.0)
    with Balance(c, t):
        scene_hook(c, t); scene_c1(c, t); scene_c2(c, t); scene_c3(c, t); scene_demo(c, t); scene_prix(c, t)
    K.dessine_eclairs(c, t)
    if t < M["cta"] - 0.3:
        voile_bas(c)
        SOUS.dessine(c, t, S["encre"])
    vs.signature(c, t, T_SIG, ["modele0", "modele1", "vitrine", "modele2", "modele3"],
                 [("Enregistre la vidéo.", M["video"] - 0.1, 58)])


# ─────────────────────────────────────────── bruitages (pop + un ding)
for k in range(4): son(M["google"] - 0.1 + 0.1 * k, "pop", -8)
son(M["luimeme"] - 0.22, "pop", -8)
son(M["propose"] + 0.55, "pop", -8); son(M["cherche1"] - 0.1, "pop", -8); son(M["cherche1"] + 0.35, "pop", -8)
for k in range(4): son(M["personne"] - 0.3 + 0.09 * k, "pop", -8)
son(M["controles"] - 0.16, "pop", -8)
son(M["notoriete"] + 0.25, "pop", -8); son(M["nourrit"] - 0.2, "pop", -8); son(M["sites"] - 0.16, "pop", -8); son(M["avis"] - 0.16, "pop", -8)
son(M["fiche"] + 0.05, "pop", -8); son(M["siteoui"] - 0.1, "pop", -8)
son(M["ville"] - 0.12, "pop", -8); son(M["histoire"] - 0.12, "pop", -8)
son(M["euros"] - 0.18, "pop", -8); son(M["euros"] + 0.35, "pop", -8); son(M["celui"] - 0.12, "pop", -8)
son(T_SIG + vs.T_BOUM, "ding", -8)

for a, b in [(0.0, 0.5), (M["classe"] - 0.22, M["classe"] + 0.3), (M["c1"] - 0.15, M["c1"] + 0.3),
             (M["c2"] - 0.15, M["c2"] + 0.3), (M["c3"] - 0.15, M["c3"] + 0.3),
             (M["fiche"] - 0.15, M["fiche"] + 0.3), (M["demo"] - 0.15, M["demo"] + 0.3),
             (M["histoire"] - 0.25, M["histoire"] + 0.25),
             (M["prix0"] - 0.15, M["prix0"] + 0.3), (M["euros"] - 0.22, M["euros"] + 0.5)]:
    rapide(a, b)
for tt, cc_, a_ in [(M["controles"] - 0.16, S["rouge"], 0.07), (M["euros"] - 0.18, "#FFFFFF", 0.22)]:
    eclair(tt, cc_, a_)
