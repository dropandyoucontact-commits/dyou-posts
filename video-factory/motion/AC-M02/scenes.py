"""AC-M02 — RECTO CERVEAU. Harry Kane, Ballon d'Or 2026, et Thierry Henry.

Habillage figé le 28/10/2026 (moteur/people.py, fond noir, grille rouge, accent blanc).
Trois règles nouvelles, posées par Youssef le 28/10 et valables pour TOUTES les vidéos de la chaîne :
  1. **Le hook est un VISUEL, pas du texte.** L'image 0 est un plan choc, plein cadre, et le
     premier titre n'arrive qu'après. On ne démarre plus sur une phrase écrite.
  2. **L'attaque de la voix doit être impactante** : `voix.py --sans-hook` puis
     `hook_rapide.py --mots 11 --debit 6.0` (ici 5,68 mots/s sur les onze premiers mots).
  3. **Débit général légèrement relevé** : 4,66 mots/s (AC-M01 était à 4,33), `--debit 4.0`.

Sujet vérifié à la source (ballondor.com, L'Équipe, franceinfo, ESPN, Evening Standard, GB News,
Yahoo, tribuna, transcriptions CBS) :
  - Harry Kane gagne le Ballon d'Or 2026 le lundi 26/10 au London Palladium, 70e cérémonie.
    Premier Anglais depuis Michael Owen en 2001. 61 buts en 51 matches en 2025-26.
  - Cinq jours avant, sur CBS, Henry écarte Kane : « the best player in Germany last year was
    Michael Olise » — Olise est son coéquipier au Bayern. Kane regardait.
  - Sur le plateau de CBS, Henry le lui redit en face ; Kane répond : « I was watching, I was
    watching a few weeks ago, don't worry. » Le plateau hurle.
  - Henry PRÉSENTE la cérémonie. Il n'a jamais gagné ce trophée : 2e en 2003 (Nedvěd),
    3e en 2006 (Cannavaro 173 pts, Buffon 124, Henry 121).
  - Toute la soirée : question à Yamal sur le prix qu'il voulait vraiment, reprise de sa
    coprésentatrice sur scène — accusations que son humour est allé trop loin.
  - Après le sacre, sur scène : « you're a worthy winner. Well done. »
  ÉCARTÉ après vérification : Forbes écrit que Kane a battu la France en petite finale du Mondial.
  FAUX — il est resté 90 minutes sur le banc, Saka a marqué un triplé. Ne pas l'utiliser.
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

SOUS = sous_titres_people(K, fusions={(4, 5): "Thierry Henry", (27, 28): "Ballon d'Or.",
                                      (75, 76): "Michael Olise.", (184, 185): "Lamine Yamal",
                                      (267, 268, 269): "Ligue des champions."})

V_REPLIQUE = "videos/kane-replique"
V_HENRY_FR = "videos/henry-francais"
V_SCENE = "videos/henry-scene"
V_CHOC = "videos/kane-choc"
V_TROPHEE = "videos/kane-trophee"
V_FINAL = "videos/henry-final"
V_YAMAL = "videos/yamal"
MEDIAS = []

# ───────────────────────────── repères, tous accrochés à un mot
T_HOOK, T_HURLE, T_CINQ, T_JALOUSIE = TW(0), TW(11), TW(17), TW(29)
T_PLATEAU, T_DEMANDE, T_LACHE = TW(36), TW(44), TW(52)
T_PASMEILLEUR, T_POURLUI, T_COEQUIPIER = TW(61), TW(72), TW(77)
T_SEMAINE, T_YEUX, T_REPETE, T_SOURIT, T_PUIS = TW(84), TW(93), TW(101), TW(108), TW(112)
T_CITATION, T_EXPLOSE = TW(117), TW(126)
T_LUNDI, T_DEVINEZ, T_SEUL, T_RANGS, T_JAMAIS1 = TW(134), TW(141), TW(148), TW(158), TW(168)
T_PIEDS, T_YAMAL, T_GAMIN, T_REPREND, T_RESEAUX = TW(170), TW(181), TW(193), TW(202), TW(209)
T_GAGNE, T_MONTE, T_REDIT, T_SOUFFERT, T_MERITE = TW(217), TW(222), TW(230), TW(236), TW(244)
T_CAMP1, T_LIGUE, T_CAMP2, T_HENRYNON = TW(252), TW(262), TW(270), TW(277)
T_CTA, T_JALOUX, T_HONNETE, T_PLUSFORT = TW(285), TW(289), TW(295), TW(301)
T_SIGN = round(K.timing["duree_voix"] - 0.05, 2)
T_FIN = DUREE


def vitesse_grille(t):
    """le décor avance ; il accélère sur les bascules du récit"""
    v = 0.5
    for t0 in (T_HOOK, T_CITATION, T_DEVINEZ, T_GAGNE, T_CAMP1, T_CTA):
        v += 2.6 * max(0.0, 1 - abs(t - t0) / 0.55) ** 2
    return v


# ═════════════════════════════ briques propres à cette vidéo
def podium(c, t, cx, cy, u, h1=280, larg=200):
    """Le podium du Ballon d'Or vu par Thierry Henry : la 2e et la 3e marche pleines,
    la 1re VIDE, en pointillés rouges. Tout le sujet tient dans cette image."""
    if u <= 0.01: return
    marches = [(-1, 0.62, "3e", "2006"), (0, 1.0, "1er", None), (1, 0.78, "2e", "2003")]
    for k, (pos, f, rang, an) in enumerate(marches):
        a = borne((u - 0.14 * k) * 2.4)
        if a <= 0.01: continue
        h = h1 * f
        x = cx + pos * (larg + 14) - larg / 2
        y = cy - h
        with Calque(c, a):
            if rang == "1er":
                # la marche qu'il n'a jamais eue : contour rouge, rien dedans
                p = skia.Paint(AntiAlias=True, Color=hexa(ROUGE), Style=skia.Paint.kStroke_Style,
                               StrokeWidth=6, PathEffect=skia.DashPathEffect.Make([16.0, 12.0], 0.0))
                c.drawRect(skia.Rect.MakeXYWH(x, y, larg, h), p)
                texte(c, "VIDE", cx, y + h / 2 - 30, 52, ROUGE, "noir", "centre", 0.04)
            else:
                pose_sol(c, x + larg / 2, cy, larg * 1.3, 0.22)
                rrect(c, x, y, larg, h, 4, BLANC, 1.0)
                texte(c, rang, x + larg / 2, y + 26, 72, NOIR, "noir", "centre", -0.01)
                if an:
                    texte(c, an, x + larg / 2, y + 116, 44, NOIR, "fort", "centre", 0.04)
    trait(c, cx - (larg * 1.5 + 36), cy, cx + (larg * 1.5 + 36), cy, BLANC, 6, 0.85 * borne(u * 3))


def ondes_sol(c, t, t0, a=1.0, n=5, vitesse=0.78):
    """anneaux rouges qui partent du point de fuite et viennent vers nous, à même le sol"""
    if a <= 0.01: return
    for k in range(n):
        u = ((t - t0) * vitesse + k / n) % 1.0
        z = mix(7.0, 0.55, u ** 1.5)
        y = HORIZON + SOL / z
        rx = 1500 / z
        al = a * 0.58 * math.sin(math.pi * min(1.0, u * 1.08)) ** 0.7
        if y > H + 500 or al <= 0.01: continue
        c.drawOval(skia.Rect.MakeXYWH(AXE - rx, y - rx * 0.20, 2 * rx, 0.40 * rx),
                   peinture(ROUGE, al, Style=skia.Paint.kStroke_Style, StrokeWidth=4 + 22 * (1 - z / 7)))


def puce(c, txt, cx, y, u, a=1.0, taille=44, rouge=False):
    """une réaction de réseau social : une pastille de texte qui se pose, légèrement de travers"""
    if u <= 0.01 or a <= 0.01: return
    ts = ajuste(txt, 620, taille, "fort", -0.01)
    w, h = largeur(txt, ts, "fort", -0.01) + 60, ts * 1.95
    c.save(); c.translate(cx + mix(260, 0, sortieExpo(u)), y); c.rotate(mix(7, -1.2, u))
    with Calque(c, a * borne(u * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        people._halo(c, rr, 0.22, 16, ROUGE if rouge else BLANC)
        c.drawRRect(rr, peinture(ROUGE if rouge else FOND3))
        if not rouge:
            c.drawRRect(rr, peinture(BLANC, 0.5, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        texte(c, txt, 0, -hauteurLigne(ts, "fort") / 2, ts, BLANC, "fort", "centre", -0.01)
    c.restore()


def camp(c, titre_c, lignes, cote, u, rouge=False):
    """une moitié du débat : un camp à gauche, un camp à droite, un filet rouge entre les deux"""
    if u <= 0.01: return
    cx = AXE_HAUT + cote * 225
    with Calque(c, borne(u * 2.2)):
        c.save(); c.translate(0, mix(60 * cote, 0, sortieExpo(u)))
        ts = ajuste(titre_c, 380, 66, "noir", -0.02)
        texte(c, titre_c, cx, 540, ts, ROUGE if rouge else BLANC, "noir", "centre", -0.02)
        trait(c, cx - 150, 628, cx + 150, 628, ROUGE if rouge else BLANC, 5, 0.9)
        y = 670
        for ligne in lignes:
            t2 = ajuste(ligne, 400, 46, "fort", -0.01)
            texte(c, ligne, cx, y, t2, BLANC, "fort", "centre", -0.01)
            y += t2 * 1.42
        c.restore()


# ═════════════════════════════ 1. HOOK — un VISUEL, pas du texte
def hook(c, t):
    if t > T_CINQ + 0.2: return
    sor = prog(t, T_CINQ - 0.1, 0.3, entree)
    with Calque(c, 1 - sor):
        # image 0 : le plan de Kane, grand, qui fonce sur nous. AUCUN texte.
        # Au 4e mot il monte et le visage de Henry arrive du fond, en dessous : le face-à-face
        # est à l'écran avant qu'un seul mot ne soit écrit (règle du 28/10 : le hook est un visuel).
        arr = prog(t, -0.16, 0.32, sortieExpo)
        sp = prog(t, TW(3) - 0.14, 0.44, sortieExpo)
        w1 = mix(1000, 920, sp); h1 = w1 * 0.5625
        carte_video(c, t, V_REPLIQUE, AXE_HAUT - w1 / 2, mix(600, 280, sp), w1, h1,
                    borne(arr), t0=-2.0, z0=6.0)
        if sp > 0.01:
            carte_video(c, t, V_HENRY_FR, AXE - 360, 920, 720, 405, sp, t0=TW(3) - 0.12, z0=4.5)
        if t > TW(4) + 0.02:
            a = 1 - prog(t, T_HURLE - 0.12, 0.14, entree)
            if a > 0.01:
                titre(c, "IL LE RECADRE EN DIRECT", 818, 66, t, TW(4) + 0.04, alpha=a,
                      rouge=True, effet="ressort", decal=0.012)
        if t > T_HURLE - 0.1:
            u2 = prog(t, TW(16) - 0.14, 0.2, sortieExpo)
            surlignage(c, "LE PLATEAU A HURLÉ", 812, 70, u2)
            titre(c, "LE PLATEAU A HURLÉ", 812, 70, t, T_HURLE - 0.05, couleur=BLANC,
                  effet="ressort", decal=0.012)


# ═════════════════════════════ 2. LE SACRE, ET LE MOT QUI REVIENT
def sacre(c, t):
    if t < T_CINQ - 0.3 or t > T_PLATEAU - 0.14: return
    ent = prog(t, T_CINQ - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_PLATEAU - 0.38, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, borne((t - T_CINQ + 0.2) * 4), "BALLON D'OR 2026")
        a_h = 1 - prog(t, T_JALOUSIE - 0.2, 0.16, entree)
        if a_h > 0.01:
            titre(c, "CINQ JOURS PLUS TARD,", Y_T1, 84, t, T_CINQ - 0.05, alpha=a_h, decal=0.012)
            titre(c, "HENRY LUI REMET LE TROPHÉE", Y_T2, 84, t, TW(21) - 0.06, alpha=a_h, decal=0.012)
        u = prog(t, T_CINQ - 0.2, 0.42, lin)
        carte_video(c, t, V_TROPHEE, 90, 585, 900, 506, borne(u), t0=T_CINQ - 0.2, z0=3.6)
        if t > T_JALOUSIE - 0.14:
            titre(c, "ET DEPUIS, UN SEUL MOT", Y_T1, 76, t, T_JALOUSIE - 0.06, decal=0.01)
            u2 = prog(t, TW(35) - 0.16, 0.2, sortieExpo)
            surlignage(c, "JALOUX", Y_T2 - 6, 140, u2)
            titre(c, "JALOUX", Y_T2 - 6, 140, t, TW(35) - 0.07, couleur=BLANC,
                  effet="ressort", decal=0.026)


# ═════════════════════════════ 3. LA PHRASE QUI DÉCLENCHE TOUT
def declenche(c, t):
    if t < T_PLATEAU - 0.26 or t > T_SEMAINE - 0.14: return
    ent = prog(t, T_PLATEAU - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_SEMAINE - 0.38, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "CE QU'IL A DIT")
        a_h = 1 - prog(t, T_PASMEILLEUR - 0.22, 0.16, entree)
        if a_h > 0.01:
            titre(c, "TOUT PART D'UN PLATEAU TÉLÉ", Y_T1, 76, t, T_PLATEAU - 0.05,
                  alpha=a_h, decal=0.01)
            if t > T_DEMANDE - 0.12:
                titre(c, "ON LUI DEMANDE QUI MÉRITE", Y_T2, 76, t, T_DEMANDE - 0.06,
                      alpha=a_h, decal=0.01)
        u = prog(t, T_PLATEAU - 0.2, 0.42, lin)
        bas = prog(t, T_PASMEILLEUR - 0.3, 0.4, sortie)
        carte_video(c, t, V_HENRY_FR, 90, mix(585, 430, bas), 900, 506, borne(u),
                    t0=T_PLATEAU - 0.2, z0=3.6)
        if t > T_PASMEILLEUR - 0.14:
            document(c, t, ["« Le meilleur joueur d'Allemagne,", "ce n'est pas Harry Kane. »"],
                     AXE, 1120, 700, entre(t, T_PASMEILLEUR - 0.08), "Thierry Henry")
        if t > T_POURLUI - 0.12:
            a = 1 - prog(t, T_COEQUIPIER - 0.18, 0.14, entree)
            if a > 0.01:
                bloc(c, "MICHAEL OLISE", AXE, 1340, entre(t, T_POURLUI - 0.07), a,
                     taille=66, couleur=ROUGE, rot=-1.5)
        if t > T_COEQUIPIER - 0.12:
            bloc(c, "SON COÉQUIPIER AU BAYERN", AXE, 1340, entre(t, T_COEQUIPIER - 0.07),
                 taille=60, rot=1.5)


# ═════════════════════════════ 4. LES YEUX DANS LES YEUX
def face(c, t):
    if t < T_SEMAINE - 0.26 or t > T_CITATION - 0.16: return
    ent = prog(t, T_SEMAINE - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_CITATION - 0.4, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "UNE SEMAINE APRÈS")
        a_h = 1 - prog(t, T_SOURIT - 0.24, 0.16, entree)
        if a_h > 0.01:
            titre(c, "KANE REVIENT SUR LE PLATEAU", Y_T1, 76, t, T_SEMAINE - 0.05,
                  alpha=a_h, decal=0.01)
            if t > T_YEUX - 0.12:
                titre(c, "LES YEUX DANS LES YEUX", Y_T2, 88, t, T_YEUX - 0.06,
                      alpha=a_h, rouge=True, decal=0.014)
        u = prog(t, T_SEMAINE - 0.2, 0.42, lin)
        bascule = prog(t, T_SOURIT - 0.22, 0.26, entree)
        if bascule < 0.99:
            carte_video(c, t, V_HENRY_FR, 90, 585, 900, 506, borne(u) * (1 - bascule),
                        t0=T_SEMAINE - 0.2 - 2.0, z0=3.6)
        if bascule > 0.01:
            carte_video(c, t, V_REPLIQUE, 90, 585, 900, 506, bascule,
                        t0=T_SOURIT - 0.2, z0=1.5)
        if t > T_SOURIT - 0.14:
            titre(c, "KANE ÉCOUTE.", Y_T1, 92, t, T_SOURIT - 0.06, decal=0.014)
            if t > TW(110) - 0.1:
                titre(c, "KANE SOURIT.", Y_T2, 92, t, TW(110) - 0.05, rouge=True,
                      effet="ressort", decal=0.018)
        if t > T_PUIS - 0.12:
            bloc(c, "PUIS IL LÂCHE SA PHRASE", AXE, 1300, entre(t, T_PUIS - 0.07),
                 taille=60, rot=-1.5)


# ═════════════════════════════ 5. LA RÉPLIQUE
def replique(c, t):
    if t < T_CITATION - 0.3 or t > T_LUNDI - 0.16: return
    ent = prog(t, T_CITATION - 0.28, 0.3, sortieExpo)
    sor = prog(t, T_LUNDI - 0.4, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rayons(c, AXE, 760, t, 1100, 0.10, 16, ROUGE)
        u = prog(t, T_CITATION - 0.24, 0.4, lin)
        carte_video(c, t, V_REPLIQUE, 90, 400, 900, 506, borne(u),
                    t0=T_CITATION - 0.22 - 2.4, z0=2.2)
        document(c, t, ["« Je regardais, il y a quelques", "semaines. T'inquiète pas. »"],
                 AXE, 1080, 700, entre(t, T_CITATION - 0.1), "Harry Kane", rot=-2.4)
        if t > T_EXPLOSE - 0.14:
            eclats(c, AXE, 1080, t, T_EXPLOSE - 0.08, 16, 400, [ROUGE, BLANC, ROUGE2], 5, 0.8)
            u2 = prog(t, T_EXPLOSE - 0.14, 0.2, sortieExpo)
            surlignage(c, "LE PLATEAU EXPLOSE", 1330, 70, u2)
            titre(c, "LE PLATEAU EXPLOSE", 1330, 70, t, T_EXPLOSE - 0.06, couleur=BLANC,
                  effet="ressort", decal=0.014)


# ═════════════════════════════ 6. LA CÉRÉMONIE, ET QUI LA PRÉSENTE
def ceremonie(c, t):
    if t < T_LUNDI - 0.26 or t > T_SEUL - 0.14: return
    ent = prog(t, T_LUNDI - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_SEUL - 0.36, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "LUNDI SOIR, LONDRES")
        titre(c, "LA CÉRÉMONIE COMMENCE", Y_T1, 84, t, T_LUNDI - 0.05, decal=0.012)
        u = prog(t, T_LUNDI - 0.22, 0.42, lin)
        carte_video(c, t, V_SCENE, 90, 585, 900, 506, borne(u), t0=T_LUNDI - 0.2, z0=3.6)
        if t > T_DEVINEZ - 0.14:
            titre(c, "ET DEVINEZ QUI PRÉSENTE", Y_T2, 80, t, T_DEVINEZ - 0.06, decal=0.01)
            if t > TW(146) - 0.1:
                bloc(c, "THIERRY HENRY", AXE, 1300, entre(t, TW(146) - 0.06),
                     taille=80, couleur=ROUGE, rot=-1.5)


# ═════════════════════════════ 7. LE TROPHÉE QU'IL N'A JAMAIS EU
def jamais(c, t):
    if t < T_SEUL - 0.26 or t > T_PIEDS - 0.16: return
    ent = prog(t, T_SEUL - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_PIEDS - 0.4, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "CE QU'IL N'A JAMAIS EU")
        titre(c, "LE SEUL TROPHÉE", Y_T1, 102, t, T_SEUL - 0.05, decal=0.016)
        titre(c, "QU'IL N'A JAMAIS GAGNÉ", Y_T2, 90, t, TW(152) - 0.06, rouge=True, decal=0.014)
        # les marches se posent dès « le seul trophée » : sans ça l'écran restait nu 1,8 s
        podium(c, t, AXE, 1150, prog(t, T_SEUL - 0.24, 1.15, lin))
        if t > T_JAMAIS1 - 0.12:
            u2 = prog(t, T_JAMAIS1 - 0.12, 0.2, sortieExpo)
            surlignage(c, "JAMAIS PREMIER", 1290, 76, u2)
            titre(c, "JAMAIS PREMIER", 1290, 76, t, T_JAMAIS1 - 0.06, couleur=BLANC,
                  effet="ressort", decal=0.016)


# ═════════════════════════════ 8. LES PIEDS DANS LE PLAT
def pieds(c, t):
    if t < T_PIEDS - 0.26 or t > T_RESEAUX - 0.16: return
    ent = prog(t, T_PIEDS - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_RESEAUX - 0.38, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "TOUTE LA SOIRÉE")
        a_h = 1 - prog(t, T_GAMIN - 0.24, 0.16, entree)
        if a_h > 0.01:
            titre(c, "IL MET LES PIEDS DANS LE PLAT", Y_T1, 76, t, T_PIEDS - 0.05,
                  alpha=a_h, decal=0.01)
            if t > T_YAMAL - 0.12:
                titre(c, "IL CHARRIE LAMINE YAMAL", Y_T2, 82, t, T_YAMAL - 0.06,
                      alpha=a_h, rouge=True, decal=0.012)
        u = prog(t, T_PIEDS - 0.2, 0.42, lin)
        carte_video(c, t, V_YAMAL, 90, 585, 900, 506, borne(u), t0=T_PIEDS - 0.2, z0=3.6)
        if t > T_GAMIN - 0.14:
            titre(c, "LE GAMIN BAISSE LA TÊTE", Y_T1, 80, t, T_GAMIN - 0.06, decal=0.01)
            if t > TW(198) - 0.1:
                titre(c, "LA SALLE RIT JAUNE", Y_T2, 88, t, TW(198) - 0.05, rouge=True,
                      effet="ressort", decal=0.014)
        if t > T_REPREND - 0.12:
            bloc(c, "IL REPREND SA COPRÉSENTATRICE", AXE, 1310,
                 entre(t, T_REPREND - 0.07), taille=56, rot=-1.5)


# ═════════════════════════════ 9. LES RÉSEAUX
def reseaux(c, t):
    if t < T_RESEAUX - 0.26 or t > T_GAGNE - 0.14: return
    ent = prog(t, T_RESEAUX - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_GAGNE - 0.36, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        titre(c, "ET LÀ, LES RÉSEAUX", 500, 96, t, T_RESEAUX - 0.05, decal=0.016)
        u2 = prog(t, TW(216) - 0.14, 0.2, sortieExpo)
        surlignage(c, "PARTENT EN VRILLE", 630, 104, u2)
        titre(c, "PARTENT EN VRILLE", 630, 104, t, TW(216) - 0.06, couleur=BLANC,
              effet="ressort", decal=0.018)
        puces = [("« Il est jaloux, c'est tout »", True), ("« Il a jamais eu le Ballon d'Or »", False),
                 ("« Il dit juste la vérité »", False), ("« Respecte le gars »", True)]
        for k, (txt, rouge) in enumerate(puces):
            puce(c, txt, AXE, 870 + k * 132, prog(t, T_RESEAUX - 0.26 + 0.2 * k, 0.38, sortieExpo),
                 taille=54, rouge=rouge)


# ═════════════════════════════ 10. KANE GAGNE
def gagne(c, t):
    if t < T_GAGNE - 0.24 or t > T_CAMP1 - 0.16: return
    ent = prog(t, T_GAGNE - 0.22, 0.3, sortieExpo)
    sor = prog(t, T_CAMP1 - 0.4, 0.24, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "CE QU'IL A DIT APRÈS")
        a_h = 1 - prog(t, T_MONTE - 0.2, 0.14, entree)
        if a_h > 0.01:
            u2 = prog(t, T_GAGNE - 0.14, 0.2, sortieExpo)
            surlignage(c, "ET KANE GAGNE", Y_T1 + 40, 120, u2 * a_h)
            titre(c, "ET KANE GAGNE", Y_T1 + 40, 120, t, T_GAGNE - 0.05, couleur=BLANC,
                  effet="ressort", alpha=a_h, decal=0.024)
            uc = prog(t, T_GAGNE - 0.16, 0.4, lin)
            carte_video(c, t, V_CHOC, 90, 620, 900, 506, borne(uc), a_h, t0=T_GAGNE - 0.16 - 3.2, z0=3.0)
            confettis(c, AXE, 560, t, T_GAGNE, 18, 300, 4, [ROUGE, BLANC, ROUGE2, GRIS])
        if t > T_MONTE - 0.14:
            titre(c, "HENRY REPREND LE MICRO", Y_T1, 84, t, T_MONTE - 0.05, decal=0.012)
            u = prog(t, T_MONTE - 0.16, 0.42, lin)
            carte_video(c, t, V_FINAL, 90, 520, 900, 506, borne(u), t0=T_MONTE - 0.14, z0=3.2)
            if t > T_SOUFFERT - 0.12:
                bloc(c, "IL A ÉNORMÉMENT SOUFFERT", AXE, 1130,
                     entre(t, T_SOUFFERT - 0.07) * (1 - prog(t, T_MERITE - 0.2, 0.16, entree)),
                     taille=56, rot=-1.5)
            if t > T_MERITE - 0.14:
                document(c, t, ["« Un vainqueur mérité.", "Bravo. »"],
                         AXE, 1180, 700, entre(t, T_MERITE - 0.08), "Thierry Henry, sur scène")


# ═════════════════════════════ 11. LE DÉBAT — les deux camps
def debat(c, t):
    if t < T_CAMP1 - 0.26 or t > T_CTA - 0.16: return
    ent = prog(t, T_CAMP1 - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_CTA - 0.34, 0.22, entree)
    with Calque(c, ent * (1 - sor)):
        rubrique(c, t, 1.0, "LE VRAI DÉBAT")
        titre(c, "DEUX CAMPS", 330, 118, t, T_CAMP1 - 0.05, decal=0.022)
        camp(c, "IL A RAISON", ["Kane n'a jamais gagné", "la Ligue des champions"],
             -1, prog(t, T_CAMP1 + 0.05, 0.5, lin))
        camp(c, "IL EST JALOUX", ["Henry non plus", "n'a jamais eu ce trophée"],
             1, prog(t, T_CAMP2 - 0.1, 0.5, lin), rouge=True)
        a = borne((t - T_CAMP1 - 0.1) * 2)
        if a > 0.01:
            trait(c, AXE_HAUT, 520, AXE_HAUT, 520 + 400 * borne(a), ROUGE, 6, 0.9)
        # l'objet du litige reste à l'écran pendant tout le débat (règle « jamais de vide »)
        carte_video(c, t, V_TROPHEE, AXE - 360, 880, 720, 405,
                    prog(t, T_CAMP1 - 0.06, 0.45, lin), t0=T_CAMP1 - 0.04, z0=3.4)
        if t > T_HENRYNON - 0.12:
            bloc(c, "ZÉRO BALLON D'OR", AXE, 1350, entre(t, T_HENRYNON - 0.07),
                 taille=70, couleur=ROUGE, rot=1.5)


# ═════════════════════════════ 12. L'APPEL AU COMMENTAIRE
def cta(c, t):
    if t < T_CTA - 0.26 or t > T_SIGN + 0.08: return
    ent = prog(t, T_CTA - 0.24, 0.3, sortieExpo)
    sor = prog(t, T_SIGN - 0.18, 0.2, entree)
    with Calque(c, ent * (1 - sor)):
        rayons(c, AXE, 820, t, 1150, 0.09, 16, ROUGE)
        ondes_sol(c, t, T_CTA - 0.3, 0.75, 5, 0.85)
        a_h = 1 - prog(t, T_PLUSFORT - 0.2, 0.14, entree)
        if a_h > 0.01:
            titre(c, "THIERRY HENRY,", 500, 110, t, T_JALOUX - 0.05, alpha=a_h, decal=0.02)
            if t > TW(293) - 0.1:
                u2 = prog(t, TW(293) - 0.14, 0.2, sortieExpo)
                surlignage(c, "JALOUX ?", 645, 150, u2 * a_h)
                titre(c, "JALOUX ?", 645, 150, t, TW(293) - 0.06, couleur=BLANC,
                      effet="ressort", alpha=a_h, decal=0.028)
            if t > T_HONNETE - 0.12:
                titre(c, "OU JUSTE HONNÊTE ?", 850, 88, t, T_HONNETE - 0.06, alpha=a_h, decal=0.012)
        if t > T_PLUSFORT - 0.14:
            titre(c, "HENRY OU KANE,", 500, 112, t, T_PLUSFORT - 0.05, decal=0.02)
            u3 = prog(t, TW(305) - 0.14, 0.2, sortieExpo)
            surlignage(c, "C'ÉTAIT QUI ?", 645, 140, u3)
            titre(c, "C'ÉTAIT QUI ?", 645, 140, t, TW(305) - 0.06, couleur=BLANC,
                  effet="ressort", decal=0.026)
        if t > T_CTA + 0.14:
            bloc(c, "DIS-LE EN COMMENTAIRE", AXE, 1130, entre(t, T_CTA + 0.18),
                 taille=62, rot=-1.5)
        if t > T_CTA + 0.5:
            puce(c, "ON RÉPOND À TOUT LE MONDE", AXE, 1310,
                 prog(t, T_CTA + 0.55, 0.4, sortieExpo), taille=50, rouge=True)


# ═════════════════════════════ sons
son(0.0, "impact", -2); son(0.0, "whoosh_long", -7)
son(TW(3) - 0.08, "tampon", -8); son(TW(16) - 0.08, "impact", -5)
son(T_CINQ - 0.24, "whoosh", -9); son(TW(35) - 0.08, "tampon", -7)
son(T_PLATEAU - 0.22, "whoosh_court", -9); son(T_PASMEILLEUR - 0.08, "verre", -9)
son(T_POURLUI - 0.07, "pop", -9); son(T_COEQUIPIER - 0.07, "pop", -10)
son(T_SEMAINE - 0.22, "whoosh", -9); son(T_YEUX - 0.06, "impact_doux", -7)
son(T_SOURIT - 0.2, "swipe", -10); son(T_PUIS - 0.07, "pop", -9)
son(T_CITATION - 0.24, "whoosh_long", -6); son(T_CITATION - 0.08, "verre", -8)
son(T_EXPLOSE - 0.08, "impact", -3); son(T_EXPLOSE + 0.1, "ching", -8)
son(T_LUNDI - 0.22, "whoosh", -9); son(TW(146) - 0.07, "tampon", -7)
son(T_SEUL - 0.22, "whoosh_court", -9); son(T_RANGS - 0.2, "montee", -10)
son(T_JAMAIS1 - 0.07, "impact", -5)
son(T_PIEDS - 0.22, "whoosh", -9); son(T_YAMAL - 0.06, "swipe", -10)
son(TW(198) - 0.06, "pop", -9); son(T_REPREND - 0.07, "pop", -10)
son(T_RESEAUX - 0.22, "whoosh_long", -8)
for k in range(4): son(T_RESEAUX + 0.14 + 0.22 * k, "pop", -11)
son(T_GAGNE - 0.14, "impact", -3); son(T_GAGNE + 0.08, "ching", -7)
son(T_MONTE - 0.14, "whoosh_bas", -9); son(T_MERITE - 0.08, "verre", -9)
son(T_CAMP1 - 0.22, "whoosh_long", -7); son(T_CAMP2 - 0.1, "swipe", -10)
son(T_HENRYNON - 0.07, "tampon", -7)
son(T_CTA - 0.22, "whoosh_long", -7); son(TW(293) - 0.08, "tampon", -7)
son(TW(305) - 0.08, "tampon", -7); son(T_CTA + 0.32, "pop", -9)
sons_signature_people(son, T_SIGN)

for a, b in [(0.0, 0.6), (T_CINQ - 0.24, T_CINQ + 0.3), (T_JALOUSIE - 0.1, T_JALOUSIE + 0.3),
             (T_PLATEAU - 0.22, T_PLATEAU + 0.25), (T_PASMEILLEUR - 0.1, T_PASMEILLEUR + 0.3),
             (T_SEMAINE - 0.22, T_SEMAINE + 0.25), (T_SOURIT - 0.2, T_SOURIT + 0.3),
             (T_CITATION - 0.24, T_CITATION + 0.4), (T_EXPLOSE - 0.1, T_EXPLOSE + 0.4),
             (T_LUNDI - 0.22, T_LUNDI + 0.25), (T_SEUL - 0.22, T_SEUL + 0.25),
             (T_JAMAIS1 - 0.1, T_JAMAIS1 + 0.3), (T_PIEDS - 0.22, T_PIEDS + 0.25),
             (T_RESEAUX - 0.22, T_RESEAUX + 0.3), (T_GAGNE - 0.14, T_GAGNE + 0.4),
             (T_MONTE - 0.14, T_MONTE + 0.3), (T_CAMP1 - 0.22, T_CAMP1 + 0.4),
             (T_CTA - 0.22, T_CTA + 0.4), (T_SIGN + 0.4, T_SIGN + 0.9)]:
    rapide(a, b)
for tt, cc_, a_ in [(0.02, ROUGE, 0.10), (TW(16), BLANC, 0.10), (T_JALOUSIE, ROUGE, 0.11),
                    (T_PASMEILLEUR, ROUGE, 0.10), (T_CITATION, BLANC, 0.11),
                    (T_EXPLOSE, ROUGE, 0.13), (T_DEVINEZ, ROUGE, 0.10),
                    (T_JAMAIS1, BLANC, 0.10), (T_GAGNE, ROUGE, 0.12),
                    (T_CAMP1, BLANC, 0.09), (T_CTA, ROUGE, 0.10)]:
    eclair(tt, cc_, a_)


# ═════════════════════════════ composition
def fond(c, t):
    """le décor seul — outils/vide.py s'en sert comme référence"""
    pulse = (battement(t, T_EXPLOSE, 1, 0.5) - 1) + (battement(t, T_GAGNE, 1, 0.5) - 1) \
          + (battement(t, T_JALOUSIE, 1, 0.5) - 1)
    fond_grille(c, t, pulse, vitesse=vitesse_grille(t))


def dessine(c, t):
    fond(c, t)
    hook(c, t); sacre(c, t); declenche(c, t); face(c, t); replique(c, t)
    ceremonie(c, t); jamais(c, t); pieds(c, t); reseaux(c, t); gagne(c, t)
    debat(c, t); cta(c, t)
    if t >= T_SIGN - 0.12:
        signature_people(c, t, T_SIGN, MEDIAS)
    filigrane(c, 0.26 * (1 - prog(t, T_SIGN - 0.2, 0.2, entree)))
    K.dessine_eclairs(c, t)
    if t < T_SIGN - 0.02:
        SOUS.dessine(c, t, BLANC)
