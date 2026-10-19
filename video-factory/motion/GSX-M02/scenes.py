"""GSX-M02 « En Chine, votre fournisseur défend ses intérêts. Qui défend les vôtres ? » — hook 2 du client (19/10/2026).
Même forme que GSX-M01 (moteur/gsx.py : fond blanc, verre clair, accent rouge, signature 3D), script mot pour mot.
Fil visuel : deux cartes face à face (VOUS / le fournisseur), la place vide « sur le terrain », puis GSX qui fait le lien."""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import Groupe, eclats, entre, curseur, clic, lueur_s, lettres, sous_titres
from studio3d import Cam, Plan, coins, scene3d, Balance
from gsx import *
import gsx

polices(P)
DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 1.9, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = sous_titres(K)
CX = 510

T_QUEST, T_POSE = TW(9), TW(12)
T_VOUS, T_INT, T_VOTRE, T_SIENS, T_MAIS, T_VOTRES, T_TERRAIN = TW(13), TW(16), TW(17), TW(21), TW(22), TW(27), TW(30)
T_A, T_DIFF, T_FIER, T_INFO, T_NEGO, T_SUIVRE, T_ASS, T_EXIG, T_RESP = TW(31), TW(35), TW(39), TW(44), TW(46), TW(50), TW(53), TW(58), TW(62)
T_UN, T_VISI, T_OU, T_COMM, T_COMPL, T_FRAG, T_REL, T_FAB = TW(63), TW(66), TW(67), TW(70), TW(72), TW(76), TW(78), TW(81)
T_CEST, T_GSX, T_PART, T_NOUS = TW(82), TW(87), TW(92), TW(94)
T_RECH, T_SEL, T_NEGOS, T_COORD, T_OBJ, T_DECI, T_ECL, T_MIEUX, T_ETAPES, T_PROJET = TW(99), TW(102), TW(106), TW(109), TW(114), TW(123), TW(124), TW(127), TW(131), TW(134)
T_PARCE, T_USINE, T_MAIS2, T_PARTN, T_MARCHE, T_EXIG2, T_OBJ2 = TW(135), TW(141), TW(142), TW(150), TW(154), TW(156), TW(159)
T_UNP, T_LIEN, T_DEUX, T_REPR, T_INT3, T_MISSION = TW(161), TW(167), TW(170), TW(173), TW(175), TW(181)
T_FIN = TW(182)

RUSHES = ["rushes/presses-jaunes", "rushes/chaine-electronique", "rushes/valises-moulage", "rushes/tissu-machine",
          "rushes/cartons-ouvrieres", "rushes/atelier-valises"]


def carte_vous(drap=True):
    def f(c, w, h):
        verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 1.0, ENCRE)
        disque(c, w / 2, h * 0.36, w * 0.24, ENCRE, 1, (10, 26, 0.25)); icone(c, "user", w / 2, h * 0.36, w * 0.24, BLANC, 2.6)
        texte(c, "VOUS", w / 2, h * 0.6, w * 0.16, ENCRE, "archivo", "centre", -0.02)
        if drap: drapeau(c, "FR", w / 2 - w * 0.12, h * 0.8, w * 0.24, w * 0.16, 6)
        balayage(c, 0, 0, w, h, gsx.T_COURANT[0], w * 0.1, 0.4, 0.4)
    return f


def carte_gsx(sous="Votre partenaire"):
    def f(c, w, h):
        verre_clair(c, 0, 0, w, h, w * 0.1, 1.0, 1.2)
        iw, ih = taille_img("sigle-gsx"); sw = w * 0.46
        image(c, "sigle-gsx", w / 2 - sw / 2, h * 0.34 - sw * ih / iw / 2, sw)
        texte(c, "GSX", w / 2, h * 0.6, w * 0.17, ENCRE, "archivo", "centre", -0.02)
        texte(c, sous, w / 2, h * 0.6 + w * 0.22, ajuste(sous, w * 0.84, w * 0.075, "demi", 0), GRIS, "demi", "centre", 0)
        balayage(c, 0, 0, w, h, gsx.T_COURANT[0], w * 0.1, 0.4, 0.4)
    return f


def avec_voile(dessin, t0, ic="eye-off"):
    """la carte se couvre de brouillard (manque de visibilité)"""
    def f(c, w, h):
        dessin(c, w, h)
        v = prog(gsx.T_COURANT[0], t0, 0.5, sortie)
        if v > 0:
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, 0, w, h), w * 0.08, w * 0.08)
            c.drawRRect(rr, peinture("#F1F3F7", 0.82 * v))
            disque(c, w / 2, h * 0.45, w * 0.17 * v, ENCRE, v); icone(c, ic, w / 2, h * 0.45, w * 0.2 * v, BLANC, 2.6, v)
    return f


# ─────────────────────────────────────────── 1 · hook : vous / votre fournisseur, et qui veille sur le terrain ?
def scene_duel(c, t):
    t1 = T_A - 0.12
    g = Groupe(c, t, -1, t1, ent="aucune", sor="zoom", d_out=0.3)
    if not g.visible: return
    with g:
        ecart = prog(t, T_MAIS - 0.1, 0.55, entreeSortie)
        cam = Cam(ax=-8 + 2 * math.sin(t * 1.1), ay=6 * math.sin(t * 0.8), tz=mix(0, 140, ecart), cx=CX, cy=1000)
        CW, CH = 300, 450
        plans = []
        for k, (dess, sens) in enumerate([(carte_vous(), -1), (carte_rush("rushes/presses-jaunes", -0.5, label="Votre fournisseur", ic="factory"), 1)]):
            u = prog(t, -0.45 + 0.08 * k, 0.6, lambda v: ressort(v, 1.3, 4.6))
            x = sens * mix(180, 300, ecart)
            plans.append(Plan(coins((x + sens * 700 * (1 - min(u, 1)), 0, mix(900, 0, min(u, 1.05))), CW, CH, ay=sens * mix(-50, -16, min(u, 1)) * -1),
                              CW, CH, dess, borne(u * 3)))
        scene3d(c, cam, plans)
        X0, X1 = cam.proj((-mix(180, 300, ecart), 0, 0))[0], cam.proj((mix(180, 300, ecart), 0, 0))[0]
        # la grande question, puis le point d'exclamation
        q = entre(t, T_QUEST - 0.1, 0.45, 2.0) * (1 - prog(t, T_VOUS - 0.1, 0.25))
        if q > 0:
            c.save(); c.translate(CX, 1000); c.scale(mix(0.3, 1, q), mix(0.3, 1, q)); c.rotate(10 * math.sin(t * 3))
            disque(c, 0, 0, 96, ENCRE, borne(q * 3), (14, 36, 0.3)); icone(c, "circle-help", 0, 0, 118, BLANC, 2.4, borne(q * 3))
            c.restore()
            onde(c, CX, 1000, t, T_POSE, 90, 420, ROUGE, 8, 0.5)
        bouclier(c, t, X0, 700, T_VOUS + 0.1, ENCRE, None, 0.9)
        bouclier(c, t, X1, 700, T_VOTRE + 0.15, ROUGE, None, 0.9)
        # la place vide sur le terrain
        v = entre(t, T_VOTRES - 0.15, 0.5, 1.6)
        if v > 0:
            c.save(); c.translate(CX, 1000); c.scale(mix(0.4, 1, v), mix(0.4, 1, v))
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-85, -150, 170, 300), 30, 30)
            c.drawRRect(rr, peinture("#FFFFFF", 0.5 * borne(v * 3)))
            pe = peinture(ROUGE, borne(v * 3), Style=skia.Paint.kStroke_Style, StrokeWidth=5); pe.setPathEffect(skia.DashPathEffect.Make([16, 12], t * 40))
            c.drawRRect(rr, pe)
            texte(c, "?", 0, -hauteurLigne(120, "archivo") / 2, 120, ROUGE, "archivo", "centre", 0, borne(v * 3) * (0.7 + 0.3 * math.sin(t * 6)))
            c.restore()
        pill_v(c, "Sur le terrain", CX, 1300, entre(t, T_TERRAIN - 0.1, 0.4, 2.2), "map-pin", plein=True)
        if t > T_POSE: eclats(c, CX, 1000, t, T_POSE, 12, 380, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=2)
    titre2(c, t, "AVEC UN FOURNISSEUR", "EN CHINE", -0.6, T_QUEST - 0.1, t2=-0.5)
    titre2(c, t, "UNE QUESTION", "ESSENTIELLE", T_QUEST - 0.1, T_VOUS - 0.1, t2=T_QUEST)
    titre2(c, t, "VOUS DÉFENDEZ", "VOS INTÉRÊTS", T_VOUS - 0.1, T_VOTRE - 0.1, t2=T_VOUS)
    titre2(c, t, "VOTRE FOURNISSEUR", "DÉFEND LES SIENS", T_VOTRE - 0.1, T_MAIS - 0.1, t2=TW(19) - 0.05)
    titre2(c, t, "MAIS SUR LE TERRAIN", "QUI VEILLE AUX VÔTRES ?", T_MAIS - 0.1, t1, t2=TW(23) - 0.05, c2=ROUGE)


# ─────────────────────────────────────────── 2 · à distance, difficile de tout maîtriser
TACHES = [(T_INFO, "file-text", "Les informations transmises", "VOUS FIER"), (T_NEGO, "scale", "Les conditions commerciales", "NÉGOCIER"),
          (T_SUIVRE, "factory", "Le suivi de production", "SUIVRE"), (T_ASS, "badge-check", "Vos exigences respectées", "VOUS ASSURER")]


def scene_distance(c, t):
    t0, t1 = T_A - 0.12, T_UN - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="haut", d_in=0.4, d_out=0.3)
    if not g.visible: return
    with g:
        liste = prog(t, T_FIER - 0.25, 0.5, entreeSortie)
        if liste < 1:
            a = entre(t, t0, 0.6, 1.3)
            lon = mix(25, 70, prog(t, t0, T_FIER - t0, douce))
            R = 330 * mix(0.7, 1, a) * mix(1, 0.3, liste)
            cx, cy = CX, mix(1000, 700, liste)
            with Calque(c, 1 - liste):
                G = globe(c, lon, 30, cx, cy, R, 1.0)
                u = prog(t, T_A, 1.0, entreeSortie)
                tete = G.arc(c, FR, CN, cx, cy, R, lon, 30, u, ROUGE, 7, 0.35, [16, 12])
                if u < 1 and tete: icone(c, "plane", tete[0], tete[1], 44, ENCRE, 2.6)
                G.repere(c, *FR, cx, cy, R, lon, 30, "Vous", ENCRE, "FR", entre(t, T_A + 0.1, 0.4, 2.0), haut=60)
                G.repere(c, *CN, cx, cy, R, lon, 30, "L'usine", ROUGE, "CN", entre(t, T_A + 0.5, 0.4, 2.0), haut=70)
            pill_v(c, "Difficile de tout maîtriser", CX, 1300, entre(t, T_DIFF - 0.1, 0.4, 2.2) * (1 - liste), "triangle-alert", plein=True)
        for k, (tk, ic, lab, _) in enumerate(TACHES):
            rangee(c, t, CX, 650 + k * 165, 740, ic, lab, tk, "?", tk + 0.45)
        titre2(c, t, "À DISTANCE", "DIFFICILE DE TOUT MAÎTRISER", T_A - 0.05, T_FIER - 0.15, t2=T_DIFF - 0.1)
        for k, (tk, _, _, l2) in enumerate(TACHES):
            fin = TACHES[k + 1][0] - 0.1 if k < 3 else t1
            titre2(c, t, "VOUS DEVEZ" if k == 0 else None, l2, (T_FIER - 0.15) if k == 0 else tk - 0.1, fin, t2=tk - 0.1, e2="ressort")


# ─────────────────────────────────────────── 3 · manque de visibilité, mauvaise communication, relation fragilisée
def scene_friction(c, t):
    t0, t1 = T_UN - 0.12, T_CEST + 0.2
    g = Groupe(c, t, t0, t1, ent="droite", sor="aucune", d_in=0.32)
    if not g.visible: return
    with g:
        cam = Cam(ax=-8 + 2 * math.sin(t), ay=5 * math.sin(t * 0.8), tz=40, cx=CX, cy=1000)
        CW, CH = 310, 460
        fab = avec_voile(carte_rush("rushes/chaine-electronique", t0, label="Votre fabricant", ic="factory"), T_VISI - 0.05)
        sx, sy = secousse(t, T_FRAG + 0.1, 18, 0.35)
        cam.cx += sx; cam.cy += sy
        scene3d(c, cam, [Plan(coins((-215, 0, 0), CW, CH, ay=16), CW, CH, carte_vous()),
                         Plan(coins((215, 0, 0), CW, CH, ay=-16), CW, CH, fab)])
        xa, xb = cam.proj((-60, 0, 0))[0], cam.proj((60, 0, 0))[0]
        lien(c, t, xa, xb, 1000, t0 + 0.1, casse=T_FRAG + 0.1)
        b = entre(t, T_COMM - 0.1, 0.45, 2.0)
        if b > 0:
            c.save(); c.translate(CX, 760); c.scale(mix(0.3, 1, b), mix(0.3, 1, b)); c.rotate(-4 + 3 * math.sin(t * 5))
            with Calque(c, borne(b * 3)):
                verre_clair(c, -190, -60, 380, 120, 40, 1.0, 1.0)
                icone(c, "message-circle-x", -130, 0, 52, ROUGE, 2.6)
                for j in range(3):
                    l = 40 + 30 * ((j * 7 + int(t * 6)) % 3)
                    rrect(c, -80 + j * 80, -8, l, 16, 8, "#C4CAD4")
            c.restore()
        pill_v(c, "Projet compliqué", CX, 1300, entre(t, T_COMPL - 0.1, 0.4, 2.2) * (1 - prog(t, T_FRAG - 0.1, 0.2)), "triangle-alert", plein=True)
        if t > T_FRAG + 0.1:
            tampon(c, "FRAGILISÉE", CX, 1290, t, T_REL, 52, ROUGE, -7)
            eclats(c, CX, 1000, t, T_FRAG + 0.1, 14, 380, cols=[ROUGE, ENCRE, "#9AA8BF"], graine=7)
        titre2(c, t, "UN MANQUE DE", "VISIBILITÉ", T_UN - 0.05, T_OU - 0.05, t2=T_VISI - 0.1)
        titre2(c, t, "UNE MAUVAISE", "COMMUNICATION", T_OU - 0.05, T_FRAG - 0.1, t2=T_COMM - 0.1)
        titre2(c, t, "FRAGILISE VOTRE RELATION", "AVEC LE FABRICANT", T_FRAG - 0.1, t1 - 0.2, t2=T_REL - 0.05, c2=ROUGE)


# ─────────────────────────────────────────── 4 · GSX, votre partenaire sourcing (disque noir)
def scene_gsx(c, t):
    r = disque_gsx(c, t, T_CEST, T_GSX, T_NOUS, CX, 1000, "C'EST POUR CETTE RAISON QUE")
    if r > 1000:
        pill_v(c, "Votre partenaire sourcing", CX, 1300, entre(t, T_PART - 0.1, 0.4, 2.2) * (1 - prog(t, T_NOUS - 0.2, 0.2)), "heart-handshake", plein=True)
    return r


# ─────────────────────────────────────────── 5 · recherche, sélection, négociations, coordination → décisions éclairées
GRILLE = ["rushes/valises-moulage", "rushes/presses-jaunes", "rushes/tissu-machine", "rushes/cartons-ouvrieres"]
ETAPES = [("Recherche", "search"), ("Sélection", "badge-check"), ("Négociation", "scale"), ("Achat", "package"), ("Suivi", "eye")]


def scene_accompagne(c, t):
    t0, t1 = T_NOUS - 0.12, T_PARCE - 0.12
    g = Groupe(c, t, t0, t1, ent="aucune", sor="gauche", d_out=0.3)
    if not g.visible: return
    with g:
        obj = prog(t, T_OBJ - 0.2, 0.55, entreeSortie)
        if obj < 1:
            cam = Cam(ax=-12 + 3 * math.sin(t), ay=8 * math.sin(t * 0.7), tz=mix(0, 1400, obj), cx=CX, cy=980)
            plans = []
            CW, CH = 250, 360
            for k, nom in enumerate(GRILLE):
                u = prog(t, T_NOUS + 0.05 * k, 0.5, lambda v: ressort(v, 1.3, 4.8))
                if u <= 0: continue
                x, y = (-140 if k % 2 == 0 else 140), (-200 if k < 2 else 200)
                choisi = k == 1 and t > T_SEL
                dim = 0.35 if (t > T_SEL and k != 1) else 1.0
                z = mix(1200, 0, min(u, 1.05)) - (160 * prog(t, T_SEL, 0.4, sortie) if k == 1 else 0)
                plans.append(Plan(coins((x, y, z), CW, CH, ay=(k % 2 - 0.5) * -14), CW, CH,
                                  carte_rush(nom, t0, label="Sélectionné" if choisi else None, ic="badge-check", accent=VERT),
                                  borne(u * 3) * dim))
            scene3d(c, cam, plans)
            # la loupe qui passe sur les fournisseurs
            lp = prog(t, T_RECH - 0.2, T_SEL - T_RECH + 0.2, lin)
            if 0 < lp < 1 or (t > T_SEL and t < T_SEL + 0.4):
                ang = lp * 2 * math.pi
                x, y = CX + 150 * math.cos(ang + 2.3), 980 + 210 * math.sin(ang + 2.3)
                a = 1 - prog(t, T_SEL + 0.1, 0.3)
                disque(c, x, y, 70, BLANC, 0.85 * a, (10, 26, 0.25)); anneau(c, x, y, 70, ROUGE, 6, a)
                trait(c, x + 50, y + 50, x + 100, y + 100, ROUGE, 14, a)
            if t > T_SEL: eclats(c, CX + 140, 780, t, T_SEL + 0.1, 12, 300, cols=[VERT, ROUGE, ENCRE], graine=4)
            pill_v(c, "Négociations", CX, 1300, entre(t, T_NEGOS - 0.1, 0.4, 2.2) * (1 - prog(t, T_COORD - 0.1, 0.2)), "scale", plein=True)
            pill_v(c, "Coordination des achats", CX, 1300, entre(t, T_COORD - 0.1, 0.4, 2.2) * (1 - obj), "package", plein=True)
        if obj > 0:
            # l'ampoule qui s'allume (décisions éclairées), puis la piste des étapes
            l = prog(t, T_ECL - 0.1, 0.4, sortie)
            et = prog(t, T_MIEUX - 0.15, 0.5, entreeSortie)
            cy = mix(900, 820, et)
            c.save(); c.translate(CX, cy); s = mix(0.4, 1, obj) * mix(1, 0.8, et); c.scale(s, s)
            with Calque(c, obj):
                if l > 0:
                    rayons(c, 0, 0, t, 520, 0.12 * l, 14, ROUGE)
                    lueur_s(c, 0, 0, 300, ROUGE, 0.25 * l)
                verre_clair(c, -150, -150, 300, 300, 80, 1.0, l)
                icone(c, "lightbulb", 0, 0, 160, ROUGE if l > 0.5 else "#B8BEC8", 2.6)
            c.restore()
            if t > T_ECL: eclats(c, CX, cy, t, T_ECL, 14, 380, cols=[ROUGE, "#FFC53D", ENCRE], graine=5)
            if et > 0:
                y = 1180; x0, x1 = CX - 320, CX + 320
                with Calque(c, et):
                    rrect(c, x0, y - 5, x1 - x0, 10, 5, "#D5DAE3")
                    p = prog(t, T_ETAPES - 0.2, T_PROJET + 0.3 - T_ETAPES, lin)
                    rrect(c, x0, y - 5, (x1 - x0) * p, 10, 5, ROUGE)
                    for i, (lab, ic) in enumerate(ETAPES):
                        x = x0 + i * (x1 - x0) / 4
                        on = p >= i / 4 - 0.01
                        disque(c, x, y, 34 if on else 28, ROUGE if on else BLANC, 1, (6, 16, 0.2))
                        icone(c, "check" if on else ic, x, y, 32, BLANC if on else GRIS, 2.6)
                        texte(c, lab, x, y + 46, 24, ENCRE if on else GRIS, "titre", "centre", -0.01)
        for (a_, b_, l1, l2) in [(T_NOUS - 0.05, T_SEL - 0.1, "NOUS VOUS ACCOMPAGNONS", "RECHERCHE"), (T_SEL - 0.1, T_NEGOS - 0.1, "ET", "SÉLECTION"),
                                 (T_NEGOS - 0.1, T_COORD - 0.1, None, "NÉGOCIATIONS"), (T_COORD - 0.1, T_OBJ - 0.1, None, "COORDINATION"),
                                 (T_OBJ - 0.1, T_MIEUX - 0.1, "NOTRE OBJECTIF", "DES DÉCISIONS ÉCLAIRÉES"), (T_MIEUX - 0.1, t1, "MIEUX MAÎTRISER", "CHAQUE ÉTAPE")]:
            titre2(c, t, l1, l2, a_, b_, t2=a_ + 0.05, c2=ROUGE if l2 == "DES DÉCISIONS ÉCLAIRÉES" else ENCRE)


# ─────────────────────────────────────────── 6 · le fournisseur connaît son usine ; GSX comprend votre marché
PUCES = [(T_MARCHE, "Votre marché", "store"), (T_EXIG2, "Vos exigences", "file-text"), (T_OBJ2, "Vos objectifs", "target")]


def scene_usine(c, t):
    t0, t1 = T_PARCE - 0.12, T_UNP - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="aucune", d_in=0.32)
    if not g.visible: return
    with g:
        deux = prog(t, T_MAIS2 - 0.1, 0.55, entreeSortie)
        cam = Cam(ax=-8 + 2 * math.sin(t), ay=mix(-14, 6, prog(t, t0, 1.5, douce)) + 4 * math.sin(t * 0.7), tz=mix(-80, 60, deux), cx=CX, cy=mix(980, 900, deux))
        CW, CH = 320, 470
        plans = [Plan(coins((mix(0, -190, deux), 0, 0), CW, CH, ay=mix(0, 14, deux)), CW, CH,
                      carte_rush("rushes/atelier-valises", t0 - 1.0, label="Son usine", ic="factory"))]
        u = prog(t, T_PARTN - 0.2, 0.5, lambda v: ressort(v, 1.3, 4.6)) if t > T_PARTN - 0.2 else 0.0
        if u > 0:
            plans.append(Plan(coins((190 + 600 * (1 - min(u, 1)), 0, mix(900, 0, min(u, 1.05))), CW, CH, ay=-14), CW, CH, carte_gsx(), borne(u * 3)))
        scene3d(c, cam, plans)
        for k, (tk, lab, ic) in enumerate(PUCES):
            pill_v(c, lab, CX + 190, 1180 + k * 72, entre(t, tk - 0.1, 0.4, 2.2), ic, taille=28, plein=k == 2)
        if u > 0: eclats(c, CX + 190, 980, t, T_PARTN, 12, 340, cols=[ROUGE, ENCRE], graine=8)
        titre2(c, t, "VOTRE FOURNISSEUR", "CONNAÎT SON USINE", T_PARCE - 0.05, T_MAIS2 - 0.1, t2=TW(139) - 0.05)
        titre2(c, t, "MAIS IL VOUS FAUT AUSSI", "UN PARTENAIRE", T_MAIS2 - 0.1, T_MARCHE - 0.1, t2=T_PARTN - 0.1, c2=ROUGE)
        titre2(c, t, "QUI COMPREND", "VOTRE MARCHÉ", T_MARCHE - 0.1, T_EXIG2 - 0.1, t2=T_MARCHE - 0.05)
        titre2(c, t, None, "VOS EXIGENCES", T_EXIG2 - 0.1, T_OBJ2 - 0.1, t2=T_EXIG2 - 0.05)
        titre2(c, t, None, "VOS OBJECTIFS", T_OBJ2 - 0.1, t1, t2=T_OBJ2 - 0.05)


# ─────────────────────────────────────────── 7 · faire le lien entre les deux, représenter vos intérêts
def scene_lien(c, t):
    t0, t1 = T_UNP - 0.12, T_FIN + 0.3
    g = Groupe(c, t, t0, t1, ent="zoom", sor="recul", d_in=0.35, d_out=0.4)
    if not g.visible: return
    with g:
        cam = Cam(ax=-8 + 2 * math.sin(t), ay=4 * math.sin(t * 0.8), tz=120, cx=CX, cy=1000)
        CW, CH = 290, 430
        scene3d(c, cam, [Plan(coins((-250, 0, 0), CW, CH, ay=14), CW, CH, carte_vous()),
                         Plan(coins((250, 0, 0), CW, CH, ay=-14), CW, CH, carte_rush("rushes/valises-moulage", t0, label="Le fournisseur", ic="factory"))])
        xa, xb = cam.proj((-110, 0, 0))[0], cam.proj((110, 0, 0))[0]
        lien(c, t, xa, xb, 1000, T_LIEN - 0.1, t_sigle=T_DEUX - 0.1)
        bouclier(c, t, cam.proj((-250, 0, 0))[0], 730, T_REPR, ROUGE, None, 0.85)
        pill_v(c, "Vos intérêts représentés", CX, 1300, entre(t, T_INT3 - 0.05, 0.4, 2.2), "shield-check", plein=True)
        titre2(c, t, "UN PARTENAIRE CAPABLE", "DE FAIRE LE LIEN", T_UNP - 0.05, T_REPR - 0.1, t2=T_LIEN - 0.1)
        titre2(c, t, "ET DE REPRÉSENTER", "VOS INTÉRÊTS", T_REPR - 0.1, T_FIN - 0.05, t2=T_INT3 - 0.1, c2=ROUGE)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_bas", -8); son(0.05, "whoosh", -10)
son(T_QUEST - 0.1, "pop", -8); son(T_POSE, "impact_doux", -7)
son(T_VOUS + 0.1, "pop", -9); son(T_VOTRE + 0.15, "pop", -9); son(T_MAIS - 0.1, "whoosh_court", -9); son(T_VOTRES - 0.15, "montee", -12)
son(T_TERRAIN - 0.1, "ding", -11)
son(T_A - 0.12, "whoosh_long", -8); son(T_A + 0.5, "ding", -12); son(T_DIFF - 0.1, "pop", -10)
for tk, _, _, _ in TACHES: son(tk - 0.12, "whoosh_court", -10); son(tk + 0.45, "blip", -13)
son(T_UN - 0.12, "swipe", -9); son(T_VISI - 0.05, "whoosh_bas", -9); son(T_COMM - 0.1, "message_in", -9); son(T_COMM + 0.2, "croc", -11)
son(T_COMPL - 0.1, "pop", -10); son(T_FRAG + 0.1, "verre", -6); son(T_FRAG + 0.1, "impact", -7); son(T_REL, "tampon", -7)
son(T_CEST - 0.1, "whoosh_bas", -7); son(T_GSX - 0.1, "montee", -11); son(T_GSX, "impact", -4); son(T_GSX + 0.05, "ching", -9); son(T_PART - 0.1, "pop", -9)
son(T_NOUS - 0.1, "whoosh", -8)
for k in range(4): son(T_NOUS + 0.05 * k, "pop", -13)
son(T_RECH - 0.2, "whoosh_long", -12); son(T_SEL, "check", -8); son(T_SEL + 0.05, "ching", -11)
son(T_NEGOS - 0.1, "pop", -10); son(T_COORD - 0.1, "pop", -10)
son(T_OBJ - 0.2, "whoosh_bas", -8); son(T_ECL - 0.1, "montee", -11); son(T_ECL, "ching", -8)
for i in range(5): son(T_ETAPES - 0.2 + i * (T_PROJET + 0.3 - T_ETAPES) / 4, "check", -12)
son(T_PARCE - 0.12, "swipe", -9); son(T_PARTN - 0.2, "whoosh", -8); son(T_PARTN, "impact_doux", -8)
for tk, _, _ in PUCES: son(tk - 0.1, "pop", -10)
son(T_UNP - 0.12, "whoosh_court", -9); son(T_LIEN - 0.1, "whoosh_long", -10); son(T_DEUX - 0.1, "impact_doux", -7); son(T_DEUX, "ching", -10)
son(T_REPR, "pop", -9); son(T_INT3 - 0.05, "check", -9)
sons_signature(son, T_FIN)
for tl in (TW(183), TW(185), TW(187)): son(tl - 0.05, "pop", -11)
for a, b in [(0.0, 0.25), (T_MAIS - 0.1, T_MAIS + 0.2), (T_A - 0.15, T_A + 0.25), (T_FIER - 0.25, T_FIER + 0.2), (T_UN - 0.15, T_UN + 0.25),
             (T_FRAG, T_FRAG + 0.3), (T_NOUS - 0.15, T_NOUS + 0.25), (T_OBJ - 0.2, T_OBJ + 0.25), (T_PARCE - 0.15, T_PARCE + 0.25),
             (T_UNP - 0.15, T_UNP + 0.25), (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_POSE, ROUGE, 0.06), (T_FRAG + 0.1, ROUGE, 0.07), (T_GSX, "#FFFFFF", 0.12), (T_SEL, VERT, 0.05), (T_ECL, "#FFFFFF", 0.12)]:
    eclair(tt, cc_, a_)


SIGN_MEDIAS = [(n, True) for n in RUSHES]


def dessine(c, t):
    gsx.T_COURANT[0] = t
    fond_clair(c, t)
    scene_duel(c, t)
    with Balance(c, t, 0.8):
        scene_distance(c, t); scene_friction(c, t)
    r = scene_gsx(c, t)
    with Balance(c, t, 0.8):
        if r < 2100:
            scene_accompagne(c, t); scene_usine(c, t); scene_lien(c, t)
    entete(c, t, T_NOUS - 0.05, T_FIN)
    signature_gsx(c, t, T_FIN, SIGN_MEDIAS, [("Vos ambitions.", TW(183), 50, ENCRE), ("Vos exigences.", TW(185), 50, ENCRE),
                                               ("Vos intérêts au cœur de notre sourcing.", TW(187), 44, ROUGE)], cy=820)
    K.dessine_eclairs(c, t)
    cache = (T_CEST - 0.1 < t < T_NOUS - 0.05) or t > T_FIN - 0.1
    if not cache: SOUS.dessine(c, t, ENCRE)
