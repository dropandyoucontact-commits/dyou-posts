"""DA-M20 (29/10/2026) — premier format « contenu à valeur », français, moins d'une minute.

Demande de Youssef : pas forcément une minute (on ne vise pas la rémunération TikTok), appel à
ENREGISTRER la vidéo, donner de la valeur aux entrepreneurs, viser les COACHS SPORTIFS, et montrer
des extraits du site de Floris (muay thaï). Prix affiché : 490 €.

Ce n'est plus une pub frontale : trois raisons concrètes pour lesquelles un coach perd des élèves
sans le savoir, puis le site de Floris en démonstration de ce que ça résout, puis le prix,
puis « Enregistre la vidéo ».
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

IDX = dict(perdu=6, eleves=8, savoir=12, trois=13,
           r1=15, msg=18, h23=21, repond=24, ailleurs=32,
           r2=33, main=39, relance=43, abo=45, auto=47, trace=59, comptable=60,
           r3=62, ecrit=65, contrat=68, reglement=72, litige=77, parole=80,
           demo=84, site=88, muay=92, formule=97, signe=99, preleve=102, espace=112,
           prix0=113, euros=121, surmesure=131,
           cta=132, video=134)
M = {k: TW(v) for k, v in IDX.items()}
SOUS = sous_titres(K)
PW_, PH_ = 470, 960
T_SIG = M["cta"] - vs.T_BOUM


def jeton_eleve(perdu):
    def f(c, w, h):
        disque(c, w / 2, h / 2, w / 2 - 4, "#FFFFFF", 1.0, None)
        anneau(c, w / 2, h / 2, w / 2 - 6, S["rouge"] if perdu else S["lilas"], 6)
        icone(c, "user-round", w / 2, h / 2, w * 0.52, S["rouge"] if perdu else S["violet"], 2.4)
    return f


# ─────────────────────────────────────────── 1. le hook
def scene_hook(c, t):
    g = Groupe(c, t, -0.1, M["r1"] - 0.06, ent="zoom", sor="gauche", d_out=0.3)
    if not g.visible: return
    with g:
        a = prog(t, -0.05, 0.55, lambda v: ressort(v, 1.3, 4.8))
        cam = Cam(ax=-8 + 3 * math.sin(t * 0.9), ay=mix(-34, -10, min(a, 1.1)) + 4 * math.sin(t * 0.7),
                  tz=mix(1200, 320, min(a, 1.1)), cy=1000)
        plans = []
        for i in range(10):
            ts = M["perdu"] - 0.3 + 0.13 * i
            u = (t - ts) / 1.0
            cote = 1 if i % 2 else -1
            x0, y0 = cote * (150 + 80 * ((i * 7) % 5)), -260 + 130 * ((i * 3) % 5)
            if i == 9:                                   # celui qui reste
                plans.append(Plan(coins((0, 60, -120), 150, 150), 150, 150, jeton_eleve(False)))
                continue
            if u <= 0: 
                plans.append(Plan(coins((x0 * 0.5, y0 * 0.7, -160), 130, 130), 130, 130, jeton_eleve(False)))
                continue
            if u >= 1: continue
            v = entree(u)
            p = (mix(x0 * 0.5, cote * 1400, v), mix(y0 * 0.7, y0 * 0.7 - 420 * v, v), mix(-160, -520, v))
            plans.append(Plan(coins(p, 130, 130), 130, 130, jeton_eleve(True), borne((1 - u) * 3)))
        scene3d(c, cam, plans)
        if t < M["trois"] - 0.12:
            with Calque(c, 1 - prog(t, M["trois"] - 0.28, 0.2)):
                lettres(c, "TU PERDS", 540, 180, 126, t, -0.22, "ressort", decal=0.03, grad=False, couleur=S["encre"])
                lettres(c, "DES ÉLÈVES", 540, 300, 126, t, M["perdu"] - 0.14, "masque", grad=True, decal=0.03, duree=0.35)
                if t > M["savoir"] - 0.3:
                    lettres(c, "SANS LE SAVOIR.", 540, 420, 84, t, M["savoir"] - 0.22, "ressort", decal=0.03,
                            grad=False, couleur=S["gris"])
        else:
            lettres(c, "3 RAISONS", 540, 250, 150, t, M["trois"] - 0.1, "ressort", decal=0.04)


# ─────────────────────────────────────────── 2. le message de 23 h
def bulle(c, x, y, w, h, txt, heure, moi=False, alpha=1.0):
    with Calque(c, alpha):
        carte_s(c, x, y, w, h, 36, "#FFFFFF", None, 0.16)
        if moi:
            c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 36, 36, pgrad(x, y, x + w, y + h, GRAD_VIF))
        texte(c, txt, x + 34, y + 26, 32, "#FFFFFF" if moi else S["encre"], "titre", track=-0.02)
        texte(c, heure, x + w - 150, y + h - 46, 24, "#E3D6FF" if moi else S["gris"], "demi", track=0)


def scene_r1(c, t):
    g = Groupe(c, t, M["r1"] - 0.1, M["r2"] - 0.06, ent="bas", sor="zoom", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Raison 1", 540, 170, 40, "encre", "message-circle", 1.0, 1.0, rot=-2)
        lettres(c, "TU RÉPONDS", 540, 300, 104, t, M["r1"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.3)
        lettres(c, "TROP TARD.", 540, 410, 112, t, M["h23"] - 0.12, "ressort", decal=0.035)
        e1 = entre(t, M["msg"] - 0.12, 0.4, 2.4)
        if e1 > 0:
            bulle(c, 150, 600, 700, 160, "« Salut, tu prends encore", "23:04", False, borne(e1 * 3))
            texte(c, "des élèves ? »", 184, 672, 32, S["encre"], "titre", track=-0.02)
        e2 = entre(t, M["repond"] - 0.12, 0.4, 2.4)
        if e2 > 0:
            bulle(c, 300, 830, 560, 150, "« Oui bien sûr ! »", "12:30", True, borne(e2 * 3))
            pill(c, "le lendemain", 760, 1010, 30, "rouge", "clock", borne(e2 * 3), 1.0, rot=5)
        e3 = entre(t, M["ailleurs"] - 0.16, 0.45, 2.2)
        if e3 > 0:
            c.save(); c.translate(540, 1200); z = mix(1.6, 1, prog(t, M["ailleurs"] - 0.16, 0.2, entree)); c.scale(z, z)
            with Calque(c, borne(e3 * 3)):
                carte_s(c, -360, -80, 720, 160, 50, "#FFFFFF", None, 0.2)
                disque(c, -270, 0, 46, S["rouge"]); icone(c, "x", -270, 0, 48, "#FFFFFF", 3.2)
                texte(c, "Déjà inscrit ailleurs", -200, -hauteurLigne(38, "titre") / 2, 38, S["rouge"], "titre", track=-0.02)
            c.restore()


# ─────────────────────────────────────────── 3. l'encaissement à la main
def scene_r2(c, t):
    g = Groupe(c, t, M["r2"] - 0.1, M["r3"] - 0.06, ent="droite", sor="gauche", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Raison 2", 540, 170, 40, "encre", "credit-card", 1.0, 1.0, rot=2)
        lettres(c, "TU COURS", 540, 300, 112, t, M["r2"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.3)
        lettres(c, "APRÈS L'ARGENT.", 540, 410, 86, t, M["main"] - 0.12, "ressort", decal=0.03)
        # à gauche : la liste des relances
        a = entre(t, M["main"] - 0.1, 0.45, 1.6) * (1 - prog(t, M["auto"] + 0.5, 0.4))
        if a > 0:
            with Calque(c, borne(a * 3)):
                carte_s(c, 130, 580, 400, 560, 44, "#FFFFFF", None, 0.16)
                texte(c, "À relancer", 170, 620, 34, S["gris"], "fort", track=0.02)
                for j in range(5):
                    y = 700 + j * 82
                    disque(c, 200, y + 20, 22, S["doux"])
                    rrect(c, 236, y + 10, 230 - 26 * (j % 3), 20, 10, S["ligne"])
                    k = entre(t, M["relance"] - 0.3 + 0.08 * j, 0.3, 3.0)
                    if k > 0: icone(c, "bell", 480, y + 20, 34, S["rouge"], 2.4, borne(k * 3))
        # à droite : le prélèvement automatique
        b = entre(t, M["abo"] - 0.12, 0.5, 1.5)
        if b > 0:
            with Calque(c, borne(b * 3)):
                z = mix(1.4, 1, prog(t, M["abo"] - 0.12, 0.25, entree))
                c.save(); c.translate(760, 860); c.scale(z, z); c.translate(-760, -860)
                carte_s(c, 560, 580, 400, 560, 44, "#FFFFFF", None, 0.2)
                texte(c, "Prélèvement auto.", 600, 620, 32, S["violet"], "fort", track=0.02)
                for j in range(5):
                    y = 700 + j * 82
                    ok = entre(t, M["auto"] - 0.25 + 0.07 * j, 0.3, 3.0)
                    disque(c, 630, y + 20, 22, S["doux"])
                    rrect(c, 666, y + 10, 190 - 22 * (j % 3), 20, 10, S["ligne"])
                    if ok > 0:
                        disque(c, 905, y + 20, 24, S["vert"], borne(ok * 3))
                        icone(c, "check", 905, y + 20, 26, "#FFFFFF", 3.0, borne(ok * 3))
                c.restore()
        tr = entre(t, M["trace"] - 0.14, 0.42, 2.2)
        if tr > 0:
            pill(c, "Une trace comptable propre", 540, 1230, 38, "grad", "wallet", borne(tr * 3), mix(0.4, 1, tr), rot=-2)


# ─────────────────────────────────────────── 4. aucun écrit
def scene_r3(c, t):
    g = Groupe(c, t, M["r3"] - 0.1, M["demo"] - 0.08, ent="bas", sor="recul", d_in=0.4)
    if not g.visible: return
    with g:
        pill(c, "Raison 3", 540, 170, 40, "encre", "file-text", 1.0, 1.0, rot=-2)
        lettres(c, "AUCUN ÉCRIT.", 540, 310, 124, t, M["ecrit"] - 0.12, "ressort", decal=0.04)
        a = entre(t, M["r3"] + 0.1, 0.5, 1.4)
        cam = Cam(ax=-14 + 3 * math.sin(t * 0.8), ay=mix(-40, -10, a) + 4 * math.sin(t * 0.6), tz=mix(900, 260, a), cy=1000)
        def feuille(cc, w, h):
            rrect(cc, 0, 0, w, h, 30, "#FFFFFF", 1.0, None, S["ligne"], 3)
            pa = peinture(S["lilas"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=3)
            pa.setPathEffect(skia.DashPathEffect.Make([12, 10], 0))
            for j in range(9):
                cc.drawRoundRect(skia.Rect.MakeXYWH(50, 120 + j * 64, w - 100 - 40 * (j % 3), 26), 13, 13, pa)
            texte(cc, "Contrat accepté", 50, 48, 34, S["gris"], "titre", track=-0.02)
        scene3d(c, cam, [Plan(coins((0, 40, 0), 620, 740), 620, 740, feuille)])
        for k, (lab, cle, x, y, r) in enumerate([("Pas de contrat", "contrat", 250, 560, -5), ("Pas de règlement", "reglement", 730, 660, 4)]):
            e = entre(t, M[cle] - 0.12, 0.4, 2.4)
            if e <= 0: continue
            pill(c, lab, x, y, 34, "rouge", "x", borne(e * 3), mix(0.4, 1, e), rot=r)
        lt = entre(t, M["litige"] - 0.14, 0.42, 2.0)
        if lt > 0:
            c.save(); c.translate(540, 1230); c.rotate(-7)
            z = mix(2.0, 1, prog(t, M["litige"] - 0.14, 0.22, entree)); c.scale(z, z)
            with Calque(c, borne(lt * 3)):
                rrect(c, -300, -58, 600, 116, 18, None, 1.0, None, S["rouge"], 6)
                texte(c, "TA PAROLE, ET C'EST TOUT", 0, -hauteurLigne(34, "noir") / 2, 34, S["rouge"], "noir", "centre", 0.03)
            c.restore()


# ─────────────────────────────────────────── 5. le site de Floris
def ecran(nom, zoom=1.0, fy=0.5):
    def f(c, w, h):
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#0B0A10"))
        image_cover(c, nom, 0, 0, w, h, zoom=zoom, fy=fy)
    return f


def scene_demo(c, t):
    g = Groupe(c, t, M["demo"] - 0.1, M["prix0"] - 0.06, ent="zoom", sor="haut", d_in=0.42)
    if not g.visible: return
    with g:
        a = entre(t, M["demo"], 0.5, 1.4)
        b = prog(t, M["formule"] - 0.2, 0.55, entreeSortie)      # bascule vers la page d'inscription
        d = prog(t, M["espace"] - 0.25, 0.5, entree)             # puis l'espace du coach
        cam = Cam(ax=4 * math.sin(t * 0.8), ay=mix(32, -8, a) + 4 * math.sin(t * 0.7) - 26 * b + 18 * d,
                  tz=mix(1300, 300, a), cy=900, tx=mix(0, -140, b))
        if d < 0.5:
            contenu = ecran("floris-inscription", 1.0, 0.30) if b > 0.5 else ecran("floris-accueil", 1.55, 0.17)
        else:
            contenu = ecran("floris-mon-compte", 1.0, 0.22)
        scene3d(c, cam, [Plan(coins((0, 40, 0), PW_, PH_), PW_, PH_, tel(contenu))])
        lettres(c, "REGARDE.", 540, 180, 118, t, M["demo"] - 0.05, "ressort", decal=0.035,
                grad=False, couleur=S["encre"]) if t < M["site"] + 0.2 else None
        if t > M["site"] + 0.1:
            pill(c, "Le site d'un coach", 540, 190, 38, "grad", "smartphone", 1.0, 1.0, rot=-2)
        for lab, ic, cle, x, y, r, mode in [("Il choisit sa formule", "target", "formule", 300, 560, -5, "blanc"),
                                            ("Il signe", "check", "signe", 820, 700, 4, "encre"),
                                            ("Prélevé chaque mois", "credit-card", "preleve", 330, 1180, -3, "vert"),
                                            ("Le coach voit tout", "eye", "espace", 760, 1060, 4, "grad")]:
            e = entre(t, M[cle] - 0.12, 0.4, 2.4)
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
        lettres(c, "UN SITE CHEZ NOUS", 540, 300, 78, t, M["prix0"] - 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.32)
        e = entre(t, M["euros"] - 0.2, 0.5, 1.2)
        if e > 0:
            z = mix(2.2, 1, prog(t, M["euros"] - 0.2, 0.3, lambda v: ressort(v, 1.2, 4.6)))
            c.save(); c.translate(540, 640); c.scale(z, z); c.translate(-540, -640)
            lettres(c, "490 €", 540, 540, 230, t, M["euros"] - 0.16, "ressort", decal=0.05, onde_t=M["euros"] + 0.5)
            c.restore()
            eclats(c, 540, 640, t, M["euros"] + 0.1, 14, 460, graine=4)
        p = entre(t, M["euros"] + 0.35, 0.4, 2.2)
        if p > 0:
            pill(c, "Site vitrine, livré", 540, 900, 38, "blanc", "check", borne(p * 3), mix(0.4, 1, p), rot=-2)
        sm = entre(t, M["surmesure"] - 0.2, 0.45, 2.0)
        if sm > 0:
            with Calque(c, borne(sm * 3)):
                carte_s(c, 150, 1060, 780, 170, 44, "#FFFFFF", None, 0.18)
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


# ─────────────────────────────────────────── bruitages
son(0.0, "whoosh_bas", -8); son(0.05, "pop", -12); son(0.3, "impact", -6)
son(M["perdu"] - 0.14, "whoosh_court", -10)
for i in range(9): son(M["perdu"] - 0.3 + 0.13 * i + 0.25, "croc" if i % 3 == 0 else "blip", -17)
son(M["savoir"] - 0.22, "impact_doux", -9)
son(M["trois"] - 0.1, "impact", -6); son(M["trois"], "ching", -11)
son(M["r1"] - 0.1, "whoosh_long", -9); son(M["msg"] - 0.12, "message_in", -8)
son(M["repond"] - 0.12, "message_in", -10); son(M["ailleurs"] - 0.16, "croc", -8); son(M["ailleurs"], "impact", -7)
son(M["r2"] - 0.1, "swipe", -9); son(M["main"] - 0.12, "impact_doux", -9)
for j in range(5): son(M["relance"] - 0.3 + 0.08 * j, "blip", -16)
son(M["abo"] - 0.12, "whoosh_court", -10)
for j in range(5): son(M["auto"] - 0.25 + 0.07 * j, "check", -14)
son(M["trace"] - 0.14, "pop", -11)
son(M["r3"] - 0.1, "whoosh", -9); son(M["ecrit"] - 0.12, "impact_doux", -8)
for cle in ("contrat", "reglement"): son(M[cle] - 0.12, "pop", -11)
son(M["litige"] - 0.14, "tampon", -6)
son(M["demo"] - 0.1, "whoosh_long", -8); son(M["demo"], "ding", -12)
for cle in ("formule", "signe", "preleve", "espace"): son(M[cle] - 0.12, "pop", -10)
son(M["formule"] - 0.2, "swipe", -11); son(M["espace"] - 0.25, "swipe", -12)
son(M["prix0"] - 0.1, "whoosh_bas", -8); son(M["euros"] - 0.2, "montee", -9)
son(M["euros"] - 0.16, "impact", -5); son(M["euros"] + 0.1, "ching", -9)
son(M["surmesure"] - 0.2, "pop", -11)
vs.sons_signature(son, T_SIG)
son(M["video"] - 0.1, "ding", -11)
for a, b in [(0.0, 0.5), (M["trois"] - 0.12, M["trois"] + 0.4), (M["r1"] - 0.15, M["r1"] + 0.3),
             (M["r2"] - 0.15, M["r2"] + 0.3), (M["abo"] - 0.15, M["abo"] + 0.3), (M["r3"] - 0.15, M["r3"] + 0.3),
             (M["demo"] - 0.15, M["demo"] + 0.3), (M["formule"] - 0.2, M["formule"] + 0.3),
             (M["prix0"] - 0.15, M["prix0"] + 0.3), (M["euros"] - 0.2, M["euros"] + 0.5)]:
    rapide(a, b)
for tt, cc_, a_ in [(M["ailleurs"], S["rouge"], 0.08), (M["litige"] - 0.14, S["rouge"], 0.07),
                    (M["euros"] - 0.16, "#FFFFFF", 0.22)]:
    eclair(tt, cc_, a_)
