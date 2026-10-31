"""DA-M21 (31/10/2026) — contenu à valeur, français, 0'36, cible coachs sportifs.

Sujet : les trois réponses qu'un prospect cherche sur son téléphone AVANT de contacter un coach
(est-ce que c'est pour moi / où-quand-combien / est-ce que je peux te croire), puis le site de
Floris (muay thaï) en démonstration, puis le prix, puis « Enregistre la vidéo ».

Format posé le 29/10 avec DA-M20 : hook choc décontextualisé, une idée par plan, preuve à l'écran,
CTA « Enregistre la vidéo », 490 € en fin + mention sur-mesure pour celui du coach.
Bruitages : règle du 30/10 — rien que des `pop` sur ce qui apparaît, un `ding` sur la signature.
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

IDX = dict(contacte=3, questions=8, decide=17, ecrire=20, tele=26, trois=30,
           r1=32, moi=38, debutant=39, blesse=40, confirme=41, suite=49, part=51,
           r2=52, ou=54, combien=56, tarif=59, demande=61, prix=63, horaires=65, lieu=68, blanc=72,
           r3=73, croire=80, visage=82, parcours=84, photos=86,
           demo=90, site=94, parle=105, formules=109, raconte=114, vient=117,
           prix0=118, euros=126, celui=127, surmesure=136,
           cta=137, video=139)
M = {k: TW(v) for k, v in IDX.items()}
SOUS = sous_titres(K)
PW_, PH_ = 470, 960
T_SIG = M["cta"] - vs.T_BOUM


def ecran(nom, zoom=1.0, fy=0.5):
    def f(c, w, h):
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#0B0A10"))
        image_cover(c, nom, 0, 0, w, h, zoom=zoom, fy=fy)
    return f


def ligne_carte(c, x, y, w, h, ic, lab, coul, alpha=1.0, mode="check"):
    """une ligne de carte blanche : pastille d'icône à gauche, libellé à droite"""
    with Calque(c, alpha):
        carte_s(c, x, y, w, h, h / 2, "#FFFFFF", None, 0.14)
        disque(c, x + h / 2, y + h / 2, h * 0.33, coul)
        icone(c, ic, x + h / 2, y + h / 2, h * 0.38, "#FFFFFF", 3.0)
        texte(c, lab, x + h * 0.95, y + h / 2 - hauteurLigne(38, "titre") / 2, 38, S["encre"], "titre", track=-0.02)


# ─────────────────────────────────────────── 1. le hook : personne ne t'écrit
def scene_hook(c, t):
    g = Groupe(c, t, -0.1, M["r1"] - 0.06, ent="zoom", sor="gauche", d_out=0.3)
    if not g.visible: return
    with g:
        a = prog(t, -0.05, 0.6, lambda v: ressort(v, 1.25, 4.6))
        z = prog(t, M["ecrire"] - 0.2, 0.5, entree)
        cam = Cam(ax=-5 + 2.5 * math.sin(t * 0.9), ay=mix(-28, -7, min(a, 1.1)) + 3 * math.sin(t * 0.7),
                  tz=mix(1250, 400, min(a, 1.1)) - 20 * z, cy=900)
        fy = mix(0.17, 0.42, prog(t, M["tele"] - 0.2, 1.0, entree))
        scene3d(c, cam, [Plan(coins((0, 40, 0), PW_, PH_), PW_, PH_, tel(ecran("floris-accueil", 1.55, fy)))])
        # la bulle qui se forme et ne part jamais
        b = entre(t, M["contacte"] - 0.3, 0.4, 2.2) * (1 - prog(t, M["questions"] + 0.15, 0.4))
        if b > 0:
            with Calque(c, borne(b * 3)):
                carte_s(c, 355, 915, 370, 150, 46, "#FFFFFF", None, 0.22)
                for j in range(3):
                    pu = 0.5 + 0.5 * math.sin(t * 6 - j * 0.8)
                    disque(c, 452 + j * 58, 990, 14, S["grisClair"], mix(0.3, 1.0, pu))
        if t < M["decide"] - 0.26:
            with Calque(c, 1 - prog(t, M["decide"] - 0.42, 0.18)):
                lettres(c, "PERSONNE", 540, 170, 136, t, -0.22, "ressort", decal=0.03, grad=False, couleur=S["encre"])
                lettres(c, "NE TE POSE", 540, 300, 122, t, M["contacte"] - 0.16, "masque", grad=True, decal=0.03, duree=0.34)
                if t > M["questions"] - 0.34:
                    lettres(c, "DE QUESTIONS.", 540, 420, 90, t, M["questions"] - 0.26, "ressort", decal=0.03,
                            grad=False, couleur=S["gris"])
        elif t < M["trois"] - 0.14:
            with Calque(c, 1 - prog(t, M["trois"] - 0.3, 0.2)):
                lettres(c, "IL A DÉJÀ", 540, 190, 132, t, M["decide"] - 0.2, "masque", grad=False,
                        couleur=S["encre"], decal=0.03, duree=0.32)
                lettres(c, "DÉCIDÉ.", 540, 320, 150, t, M["ecrire"] - 0.22, "ressort", decal=0.04)
        else:
            lettres(c, "3 RÉPONSES", 540, 250, 146, t, M["trois"] - 0.12, "ressort", decal=0.04)


# ─────────────────────────────────────────── 2. est-ce que c'est pour moi
def scene_r1(c, t):
    g = Groupe(c, t, M["r1"] - 0.1, M["r2"] - 0.06, ent="bas", sor="zoom", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Réponse 1", 540, 160, 40, "encre", "user-round", 1.0, 1.0, rot=-2)
        lettres(c, "C'EST POUR MOI ?", 540, 270, 104, t, M["r1"] + 0.05, "masque", grad=True, decal=0.03, duree=0.32)
        for j, (cle, lab, ic) in enumerate([("debutant", "Débutant", "sparkles"),
                                            ("blesse", "Blessé, je reprends", "heart"),
                                            ("confirme", "Confirmé", "flame")]):
            e = entre(t, M[cle] - 0.14, 0.4, 2.4)
            if e <= 0: continue
            y = 480 + j * 150
            c.save(); c.translate(0, mix(60, 0, borne(e)))
            ligne_carte(c, 150, y, 700, 118, ic, lab, S["violet"], borne(e * 3))
            c.restore()
        # s'il ne se reconnaît pas, il part
        s = entre(t, M["suite"] - 0.14, 0.45, 2.0)
        if s > 0:
            with Calque(c, borne(s * 3)):
                carte_s(c, 150, 960, 700, 150, 48, "#FFFFFF", None, 0.16)
                texte(c, "Il ne se reconnaît pas.", 210, 1035 - hauteurLigne(38, "titre") / 2, 38, S["gris"], "titre", track=-0.02)
        pa = entre(t, M["part"] - 0.14, 0.42, 2.2)
        if pa > 0:
            dx = mix(0, 80, prog(t, M["part"] - 0.1, 0.6, entree))
            c.save(); c.translate(dx, 0); c.rotate(-3, 470, 1215)
            with Calque(c, borne(pa * 3) * (1 - prog(t, M["part"] + 0.55, 0.4))):
                carte_s(c, 170, 1150, 600, 130, 44, "#FFFFFF", None, 0.2)
                disque(c, 250, 1215, 40, S["rouge"]); icone(c, "arrow-right", 250, 1215, 42, "#FFFFFF", 3.0)
                texte(c, "Il part.", 320, 1215 - hauteurLigne(44, "noir") / 2, 44, S["rouge"], "noir", track=-0.02)
            c.restore()


# ─────────────────────────────────────────── 3. où, quand, combien
def scene_r2(c, t):
    g = Groupe(c, t, M["r2"] - 0.1, M["r3"] - 0.06, ent="droite", sor="gauche", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Réponse 2", 540, 160, 40, "encre", "map-pin", 1.0, 1.0, rot=2)
        lettres(c, "OÙ, QUAND,", 540, 260, 110, t, M["r2"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.3)
        lettres(c, "COMBIEN.", 540, 370, 126, t, M["combien"] - 0.18, "ressort", decal=0.035)
        # « tarif sur demande », barré
        d = entre(t, M["tarif"] - 0.14, 0.42, 2.2) * (1 - prog(t, M["prix"] + 0.1, 0.35))
        if d > 0:
            with Calque(c, borne(d * 3)):
                c.save(); c.rotate(-2, 540, 610)
                carte_s(c, 170, 540, 660, 140, 44, "#FFFFFF", None, 0.16)
                texte(c, "Tarif sur demande", 540, 610 - hauteurLigne(44, "titre") / 2, 44, S["gris"], "titre", "centre", -0.02)
                bl = prog(t, M["demande"] - 0.12, 0.3, entree)
                if bl > 0:
                    rrect(c, 195, 604, mix(0, 610, bl), 9, 5, S["rouge"])
                c.restore()
        for j, (cle, lab, ic) in enumerate([("prix", "50 € par mois", "wallet"),
                                            ("horaires", "3 séances par semaine", "calendar"),
                                            ("lieu", "Le Puy-en-Velay", "map-pin")]):
            e = entre(t, M[cle] - 0.14, 0.4, 2.4)
            if e <= 0: continue
            y = 700 + j * 150
            z = mix(1.25, 1, prog(t, M[cle] - 0.14, 0.22, entree))
            c.save(); c.translate(500, y + 59); c.scale(z, z); c.translate(-500, -(y + 59))
            ligne_carte(c, 150, y, 700, 118, ic, lab, S["vert"], borne(e * 3))
            c.restore()
        bn = entre(t, M["blanc"] - 0.16, 0.42, 2.0)
        if bn > 0:
            pill(c, "Écrit noir sur blanc", 500, 1215, 40, "grad", "check", borne(bn * 3), mix(0.45, 1, bn), rot=-2)


# ─────────────────────────────────────────── 4. est-ce que je peux te croire
def scene_r3(c, t):
    g = Groupe(c, t, M["r3"] - 0.1, M["demo"] - 0.08, ent="bas", sor="recul", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Réponse 3", 540, 160, 40, "encre", "shield-check", 1.0, 1.0, rot=-2)
        lettres(c, "JE PEUX", 540, 260, 118, t, M["r3"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.3)
        lettres(c, "TE CROIRE ?", 540, 375, 118, t, M["croire"] - 0.18, "ressort", decal=0.035)
        a = entre(t, M["r3"] + 0.12, 0.5, 1.4)
        cam = Cam(ax=-8 + 3 * math.sin(t * 0.8), ay=mix(26, -6, a) + 4 * math.sin(t * 0.6), tz=mix(1200, 620, a), cy=960)
        scene3d(c, cam, [Plan(coins((0, 60, 0), PW_, PH_), PW_, PH_, tel(ecran("floris-qui-suis-je", 1.35, 0.62)))])
        for cle, lab, ic, x, y, r in [("visage", "Ton visage", "user-round", 320, 640, -5),
                                      ("parcours", "Ton parcours", "trophy", 740, 790, 4),
                                      ("photos", "De vraies photos", "image", 400, 1180, -3)]:
            e = entre(t, M[cle] - 0.12, 0.4, 2.4)
            if e <= 0: continue
            c.save(); c.translate(x, y + 7 * math.sin(t * 2)); c.rotate(r)
            z = mix(1.6, 1, prog(t, M[cle] - 0.12, 0.2, entree)); c.scale(z, z)
            pill(c, lab, 0, 0, 38, "blanc" if cle != "photos" else "grad", ic, borne(e * 3))
            c.restore()


# ─────────────────────────────────────────── 5. le site de Floris
def scene_demo(c, t):
    g = Groupe(c, t, M["demo"] - 0.1, M["prix0"] - 0.06, ent="zoom", sor="haut", d_in=0.42)
    if not g.visible: return
    with g:
        a = entre(t, M["demo"], 0.5, 1.4)
        b = prog(t, M["formules"] - 0.25, 0.5, entreeSortie)     # bascule vers la page d'inscription
        d = prog(t, M["raconte"] - 0.25, 0.45, entree)           # puis « qui suis-je »
        cam = Cam(ax=4 * math.sin(t * 0.8), ay=mix(32, -8, a) + 4 * math.sin(t * 0.7) - 24 * b + 16 * d,
                  tz=mix(1300, 300, a), cy=900, tx=mix(0, -130, b))
        if d < 0.5:
            contenu = ecran("floris-inscription", 1.0, 0.33) if b > 0.5 else ecran("floris-accueil", 1.55, 0.17)
        else:
            contenu = ecran("floris-qui-suis-je", 1.0, 0.18)
        scene3d(c, cam, [Plan(coins((0, 40, 0), PW_, PH_), PW_, PH_, tel(contenu))])
        if t < M["site"] + 0.2:
            lettres(c, "REGARDE.", 540, 180, 120, t, M["demo"] - 0.05, "ressort", decal=0.035,
                    grad=False, couleur=S["encre"])
        else:
            pill(c, "Le site d'un coach", 540, 190, 38, "grad", "smartphone", 1.0, 1.0, rot=-2)
        for lab, ic, cle, fin, x, y, r, mode in [("À qui il parle", "users", "parle", "formules", 330, 600, -5, "blanc"),
                                                 ("Ses formules et son prix", "wallet", "formules", "raconte", 520, 1130, 3, "vert"),
                                                 ("D'où il vient", "plane-takeoff", "raconte", None, 420, 760, -3, "grad")]:
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
        scene_hook(c, t); scene_r1(c, t); scene_r2(c, t); scene_r3(c, t); scene_demo(c, t); scene_prix(c, t)
    K.dessine_eclairs(c, t)
    if t < M["cta"] - 0.3:
        voile_bas(c)
        SOUS.dessine(c, t, S["encre"])
    vs.signature(c, t, T_SIG, ["modele0", "modele1", "vitrine", "modele2", "modele3"],
                 [("Enregistre la vidéo.", M["video"] - 0.1, 58)])


# ─────────────────────────────────────────── bruitages (règle du 30/10 : pop + un ding, rien d'autre)
for cle in ("debutant", "blesse", "confirme", "part"):
    son(M[cle] - 0.14, "pop", -8)
for cle in ("prix", "horaires", "lieu"):
    son(M[cle] - 0.14, "pop", -8)
son(M["blanc"] - 0.16, "pop", -8)
for cle in ("visage", "parcours", "photos"):
    son(M[cle] - 0.12, "pop", -8)
for cle in ("parle", "formules", "raconte"):
    son(M[cle] - 0.12, "pop", -8)
son(M["euros"] - 0.18, "pop", -8); son(M["euros"] + 0.35, "pop", -8); son(M["celui"] - 0.12, "pop", -8)
son(T_SIG + vs.T_BOUM, "ding", -8)

for a, b in [(0.0, 0.5), (M["trois"] - 0.12, M["trois"] + 0.4), (M["r1"] - 0.15, M["r1"] + 0.3),
             (M["r2"] - 0.15, M["r2"] + 0.3), (M["r3"] - 0.15, M["r3"] + 0.3),
             (M["demo"] - 0.15, M["demo"] + 0.3), (M["formules"] - 0.25, M["formules"] + 0.25),
             (M["prix0"] - 0.15, M["prix0"] + 0.3), (M["euros"] - 0.22, M["euros"] + 0.5)]:
    rapide(a, b)
for tt, cc_, a_ in [(M["part"] - 0.14, S["rouge"], 0.07), (M["euros"] - 0.18, "#FFFFFF", 0.22)]:
    eclair(tt, cc_, a_)
