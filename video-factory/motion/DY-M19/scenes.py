"""DY-M19 (21/10/2026) = DY-M17 aux couleurs de DA-M18-EN, comme DY-M18 (validée « parfaite ») : verre clair, encre,
accents violets ; pause du mzé recoupée au milieu du vrai silence après « paire. ».

DY-M17 « Tu veux une paire ? » — organique TikTok DROP&YOU (20/10/2026), variante de DY-M16 (même ossature que DY-M15).

Ce qui change (demande de Youssef du 20/10) : mêmes couleurs, même signature, script réécrit avec d'autres mots, autre réglage
de voix ; TOUS les articles viennent du lot envoyé le 20/10 (banque/produits/recents-2026-10) ; Guangzhou de nuit (sa vidéo) à la
place de la photo de Kinbo ; Le mzé (@y.lemzeee, ambassadeur sur dropandyou1.com) parle dans le téléphone pendant que la
voix se tait (timing.json["pauses"], outils/inserer_pause.py) ; ses avis Snapchat ; les planches de paires défilent vite dans
un téléphone sur « un carton entier ».

Retour de Youssef sur DY-M13 (« elle, j'aime bien ») : trop centrée sur les baskets, et les paires choisies (virgule, montantes
connues) ne plaisent pas à sa cible → hook élargi « une paire, une montre, une sape », trois produits différents qui claquent
un par un ; baskets réduites à 3 paires sans virgule EN ATTENDANT QU'IL DISE LESQUELLES METTRE (liste PAIRES ci-dessous).
Fin : nouvelle signature animée (moteur/signature.py) au lieu du logo dans un cadre. Jamais de ralenti (vidéos ×1 ou plus).
Conformité du 17/10 : aucune marque écrite ni dite, aucune autre plateforme, aucune promesse de gain. Zone sûre TikTok / Snap.
"""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio3d import *
import verre_studio as vs
vs.appliquer()
BLEU = vs.ACCENT


def verre(c, x, y, w, h, r=34, alpha=1.0, contour=None, lueur=1.0, givre=0.0):
    """mêmes arguments que glace.verre (DY-M17), en verre clair"""
    vs.verre(c, x, y, w, h, r, alpha, lueur if lueur is not None else 1.0)


def balayage(c, x, y, w, h, t, r=30):
    vs.balayage(c, x, y, w, h, t, r, a=0.35)
from signature import signature, sons_signature

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 2.8, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = sous_titres(K)

LOGO = "logo-dy-encre"
ENCRE, GRIS = S["encre"], S["gris"]
R = "produits/recents-2026-10/"          # le lot d'articles de Youssef (20/10/2026) : les seuls à montrer
CASQUE, DYSON = R + "casque-airpods-max-vert", R + "dyson-airwrap-rose"
DOUDOUNE, DOUD2 = R + "doudoune-moncler-noire", R + "doudoune-lv-grise-orange"
VESTES = [R + "veste-supreme-vanson-bleue", R + "veste-courreges-vinyle-noire", R + "veste-bresil-rose-hd", R + "veste-supreme-vanson-noire"]
PAIRES = [R + "basket-chanel-blanche", R + "basket-dior-b30-grise", R + "basket-lv-skate-bleue", R + "basket-on-loewe-rose"]
MONTRES_PNG = [R + "montre-daydate-bleue", R + "montre-gmt-batman"]
DETOURES = [PAIRES[2], MONTRES_PNG[1], VESTES[3], DYSON, PAIRES[3]]
MONTRES = ["montre-sertie", "montre-glacee", "montre-arabe"]   # photos portées (coins arrondis, jamais détourées) : la photo « envoyée »
PORTEE = "photos/chaussures/baskets-portees-violettes"           # la photo « tu nous montres le modèle » : toujours un article porté
MELANGE = [(PAIRES[2], False), (MONTRES_PNG[1], False), (VESTES[3], False), (DYSON, False), (MONTRES_PNG[0], False), (PAIRES[3], False),
           (MONTRES[1], True), (DOUD2, False), (PAIRES[0], False), (CASQUE, False), (VESTES[2], False), (PAIRES[1], False)]
PLANCHES = ["photos/situation-2026-10/" + n for n in ("jordan1-low-travis-planche", "lv-sacs-plateau", "cartons-dior-prada-rue",
            "chanel-baskets-planche", "salomon-xt6-carton", "dior-b25-planche")]
AVIS = ["photos/avis/" + n for n in ("avis-claquettes-noires", "avis-sacoche-nylon-noire", "avis-sac-beige-matelasse", "avis-pochette-noire-matelassee")]
INFLU, INFLU_AT, INFLU_ROLE = "videos/influenceurs/influ-b", "@y.lemzeee", "Ambassadeur DROP&YOU"
GZ_NUIT = "videos/lot-2026-10/guangzhou-nuit-ecran"
PAUSE = json.load(open(P / "timing.json"))["pauses"][0]
P0, P1 = PAUSE["t0"], PAUSE["t1"]
T_CLIP = P0 + 0.35                                            # l'audio du clip démarre après la marge
GLACIER = S["violetVif"]                                      # l'accent clair de DY-M17 → violet
VERT_ = S["vert"]
CX = 510            # axe du contenu, décalé à gauche de la colonne de boutons TikTok
_T = [0.0]

# repères (mots) — script DY-M17
T_ART, T_UNE1, T_PAIRE, T_UNE2, T_MONTRE, T_UNE3, T_SAPE = TW(1), TW(2), TW(3), TW(4), TW(5), TW(6), TW(7)
T_ENVOIE, T_PHOTO, T_JE, T_TROUVE, T_CHINE = TW(8), TW(10), TW(11), TW(14), TW(16)
T_ABO, T_EXPL = TW(17), TW(20)
T_ON, T_PLACE, T_GZ, T_AVEC, T_FOURN, T_VALID = TW(24), TW(26), TW(28), TW(29), TW(31), TW(32)
T_TU, T_MODELE, T_OCCUPE, T_RESTE = TW(33), TW(37), TW(38), TW(41)
T_MONT, T_DOUD, T_BASK, T_ELEC = T_TU - 1.0, T_TU - 0.75, T_TU - 0.5, T_TU - 0.25     # pas de liste dans ce script : les 4 cartes claquent juste avant « Tu nous dis »
T_REGARDE, T_NOM, T_RECU = TW(42), TW(43), TW(45)
T_COMME, T_CENT, T_CLIENTS, T_AVIS = TW(48), TW(51), TW(53), TW(56)
T_SELON, T_PLUS, T_QUAL, T_ET, T_PRIX, T_LIVR = TW(61), TW(67), TW(68), TW(69), TW(71), TW(74)
T_HUIT, T_DOUZE, T_JOURS, T_DEVANT, T_PORTE = TW(75), TW(77), TW(78), TW(81), TW(83)
T_UNITE, T_QTE = TW(84), TW(88)
T_SAVE, T_VIDEO, T_JAUNE = TW(89), TW(91), TW(92)
T_COMM, T_COMMENT, T_CHERCHE, T_REPONDS, T_LA = TW(96), TW(97), TW(103), TW(104), TW(109)
T_FIN = T_LA + 0.45


# ─────────────────────────────────────────── briques
def titre(c, t, l1, l2, t0, t1, y=400, t2=None, e1="masque", e2="ressort"):
    """titre éditorial (zone sûre : 840 px de large au plus) ; part avant la scène suivante"""
    if t < t0 - 0.1 or t > t1 + 0.12: return
    a = 1 - prog(t, t1 - 0.18, 0.15, entree)
    if l1:
        lettres(c, l1, 540, y, ajuste(l1, 760, 72, "noir", -0.03), t, t0 - 0.05, e1, grad=False, couleur=ENCRE, decal=0.025, duree=0.35, alpha=a)
    if l2:
        lettres(c, l2, 540, y + 84, ajuste(l2, 760, 128, "noir", -0.035), t, (t2 if t2 is not None else t0 + 0.1) - 0.05, e2, decal=0.03, alpha=a)


def filigrane(c, t):
    lw = 200
    image(c, LOGO, 540 - lw / 2, 262, lw, 0.9 * (1 - prog(t, T_FIN - 0.2, 0.3)))


def photo_ronde(c, nom, w, h, r=None):
    image_cover(c, nom, 0, 0, w, h, 1.0, 0.5, 0.5, r if r is not None else w * 0.1)


def produit_plan(nom, halo=True, haut=0.43, place=0.72):
    """un article détouré posé dans une carte de verre (pour un Plan 3D)"""
    def f(c, w, h):
        iw, ih = taille_img(nom)
        verre(c, 0, 0, w, h, w * 0.1)
        if halo: lueur_s(c, w / 2, h * haut, w * 0.55, BLEU, 0.4)
        s = min(w * 0.84 / iw, h * place / ih)
        image(c, nom, w / 2 - iw * s / 2, h * haut - ih * s / 2, iw * s)
        balayage(c, 0, 0, w, h, _T[0], w * 0.1)
    return f


def carte_video(nom, t_local, vitesse=1.0, boucle=True):
    """une vraie vidéo dans une carte de verre (jamais ralentie)"""
    def f(c, w, h):
        verre(c, 0, 0, w, h, w * 0.08)
        m = w * 0.04
        video(c, nom, m, m, w - 2 * m, h - 2 * m, t_local, vitesse, boucle, rayon=w * 0.06)
        balayage(c, 0, 0, w, h, _T[0], w * 0.08)
    return f


def carte_cat(dessin, lab):
    def f(c, w, h):
        dessin(c, w, h)
        rrect(c, w * 0.1, h * 0.76, w * 0.8, h * 0.17, h * 0.085, "#FFFFFF", 0.92, None, S["ligne"], 2)
        texte(c, lab, w / 2, h * 0.785, w * 0.105, ENCRE, "titre", "centre", -0.02)
    return f


def paires_defilent(t, t0, cadence=6.0):
    """carte « Baskets » : les paires défilent"""
    def f(c, w, h):
        k = int(max(0.0, t - t0) * cadence) % len(PAIRES)
        produit_plan(PAIRES[k], haut=0.42, place=0.5)(c, w, h)
    return f


def entete_dm(c, w, k):
    rrect(c, 0, 0, w, 120 * k, 0, "#FBFAFE")
    disque(c, 70 * k, 74 * k, 30 * k, S["lavande"]); image(c, LOGO, 46 * k, 64 * k, 48 * k)
    texte(c, "Drop&You", 116 * k, 52 * k, 24 * k, ENCRE, "titre", track=-0.01)
    texte(c, "Message privé", 116 * k, 82 * k, 17 * k, GRIS, "demi", track=0)


def bulle_photo(c, w, k, y, u, nom, coupe=False):
    """la photo envoyée, en bulle à droite"""
    with Calque(c, borne(u * 3)):
        x, ww, hh = w - 270 * k, 250 * k, 300 * k
        y = y + 30 * (1 - u) * k
        if coupe:
            image_cover(c, nom, x, y, ww, hh, 1.05, 0.5, 0.5, 26 * k)
        else:
            rrect(c, x, y, ww, hh, 26 * k, S["lavande"])
            iw, ih = taille_img(nom); s = min(ww * 0.86 / iw, hh * 0.8 / ih)
            image(c, nom, x + ww / 2 - iw * s / 2, y + hh / 2 - ih * s / 2, iw * s)
        icone(c, "check", x + ww - 26 * k, y + hh + 18 * k, 22 * k, GLACIER, 2.6)


def bulle_reponse(c, k, y, u, l1, l2):
    with Calque(c, borne(u * 3)):
        y = y + 20 * (1 - u) * k
        verre(c, 20 * k, y, 320 * k, 96 * k, 30 * k, 1.0, None, 0.5)
        icone(c, "badge-check", 56 * k, y + 48 * k, 30 * k, VERT_, 2.4)
        texte(c, l1, 84 * k, y + 16 * k, 24 * k, ENCRE, "titre", track=-0.01)
        texte(c, l2, 84 * k, y + 50 * k, 19 * k, GRIS, "demi", track=0)


# ─────────────────────────────────────────── 1. hook : tout jaillit du téléphone → une paire, une montre, une sape claquent
#    → le viseur sur la montre → photo en message privé → « Trouvé » en Chine
JAILLIT = [(MELANGE[j % len(MELANGE)], -0.62 + 0.15 * j, d, (-1) ** j) for j, d in enumerate(
    [(-0.55, -0.15), (0.6, -0.35), (-0.45, 0.45), (0.55, 0.4), (-0.7, -0.5), (0.35, -0.7), (-0.2, 0.7), (0.75, 0.05), (-0.65, 0.1),
     (0.25, 0.6), (-0.35, -0.75), (0.7, 0.55)])]
VIE, D3 = 0.95, 1800.0
CLAQUES = [(T_UNE1 + 0.05, T_UNE2, None, 1), (T_UNE2, T_UNE3, "UNE MONTRE ?", -1), (T_UNE3, T_ENVOIE, "UNE SAPE ?", 1)]


def objet_volant(c, item, t, t0, direc, sens, cx, cy):
    nom, photo = item
    u = (t - t0) / VIE
    if not (0 <= u <= 1): return
    v = sortie(u) * 0.35 + u ** 1.7 * 0.65
    X = direc[0] * 640 * v
    Y = direc[1] * 760 * v - 180 * math.sin(math.pi * min(1, u * 1.2))
    Z = -1560 * u ** 1.1
    f = D3 / (D3 + Z)
    x, y, w = cx + X * f, cy + Y * f, (300 if photo else 380) * f
    al = borne(u / 0.06)
    iw, ih = taille_img(nom); h_ = w * 1.2 if photo else w * ih / iw
    c.save(); c.translate(x, y); c.rotate(sens * (-16 + 64 * u))
    if photo:
        rrect(c, -w / 2 - 8, -h_ / 2 - 8, w + 16, h_ + 16, w * 0.13, "#FFFFFF", 0.9 * al, (10, 30, 0.35))
        image_cover(c, nom, -w / 2, -h_ / 2, w, h_, 1.0, 0.5, 0.5, w * 0.1, al)
    else:
        om = skia.Paint(AntiAlias=True, ImageFilter=skia.ImageFilters.DropShadowOnly(0, 0.08 * w, 0.07 * w, 0.07 * w, skia.Color4f(0.0, 0.05, 0.3, 0.55 * al)))
        c.saveLayer(None, om); image(c, nom, -w / 2, -h_ / 2, w, al); c.restore()
        image(c, nom, -w / 2, -h_ / 2, w, al)
    c.restore()


def ecran_hook(t):
    """le viseur braqué sur la montre (vraie vidéo, vitesse normale), puis la photo part en message privé, puis « Trouvé »"""
    def f(c, w, h):
        k = w / 440
        if t < T_PHOTO + 0.05:
            video(c, "montres-serties", 0, 0, w, h, t + 7.0, 1.0)
            m, l = 46 * k, 70 * k
            for sx, sy in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                x0 = m if sx == 0 else w - m; y0 = 170 * k if sy == 0 else h - 230 * k
                dx, dy = (l if sx == 0 else -l), (l if sy == 0 else -l)
                trait(c, x0, y0, x0 + dx, y0, "#FFFFFF", 6 * k); trait(c, x0, y0, x0, y0 + dy, "#FFFFFF", 6 * k)
            mise = prog(t, T_ENVOIE, 0.35, sortie)
            anneau(c, w / 2, h * 0.5, mix(170, 110, mise) * k, "#FFD86B", 4 * k, 0.9 * borne(mise * 3))
            disque(c, w / 2, h - 110 * k, 46 * k, "#FFFFFF", 0.95); anneau(c, w / 2, h - 110 * k, 58 * k, "#FFFFFF", 5 * k, 0.9)
            disque(c, 50 * k, 72 * k, 9 * k, "#FF3B5C", 0.6 + 0.4 * math.sin(t * 8))
        else:
            c.drawRect(skia.Rect.MakeWH(w, h), pgrad(0, 0, 0, h, ["#FFFFFF", "#F3F0F8"]))
            entete_dm(c, w, k)
            bulle_photo(c, w, k, 170 * k, prog(t, T_PHOTO + 0.05, 0.4, sortieExpo), MONTRES[0], coupe=True)
            r = prog(t, T_TROUVE - 0.1, 0.35, sortieExpo)
            if r > 0: bulle_reponse(c, k, 520 * k, r, "Trouvé", "chez nos fournisseurs, en Chine")
        fl = 1 - (t - T_PHOTO) / 0.25
        if 0 < fl <= 1: c.drawRect(skia.Rect.MakeWH(w, h), peinture("#FFFFFF", fl))
        for _, t0, _, _ in JAILLIT:
            g = 1 - (t - t0) / 0.2
            if 0 < g <= 1 and t0 < T_UNE1 - 0.3: c.drawRect(skia.Rect.MakeWH(w, h), peinture("#FFFFFF", 0.35 * g))
    return f


def dessin_claque(j, t):
    if j == 0: return lambda c, w, h: image(c, PAIRES[2], 0, 0, w)
    if j == 1: return lambda c, w, h: image(c, MONTRES_PNG[1], 0, 0, w)
    return lambda c, w, h: image(c, VESTES[3], 0, 0, w)


def claque(c, t, j):
    """un produit qui arrive du fond, claque devant la caméra (dépassement), puis s'éjecte sur le côté"""
    t0, t1, lab, sens = CLAQUES[j]
    if t < t0 - 0.12 or t > t1 + 0.2: return
    u = prog(t, t0 - 0.1, 0.42, lambda v: ressort(v, 1.4, 5.0))
    o = prog(t, t1 - 0.14, 0.24, entree)
    if j == 0: W_ = 600; iw, ih = taille_img(PAIRES[2]); H_ = W_ * ih / iw
    elif j == 1: H_ = 640; iw, ih = taille_img(MONTRES_PNG[1]); W_ = H_ * iw / ih
    else: H_ = 560; iw, ih = taille_img(VESTES[3]); W_ = H_ * iw / ih
    cam = Cam(ax=-8 + 2 * math.sin(t * 2), ay=4 * math.sin(t * 1.7), cx=CX, cy=1040)
    pos = (mix(0, sens * -1300, o), mix(0, -200, o), mix(2600, 0, u))
    pl = Plan(coins(pos, W_, H_, ay=mix(sens * 80, sens * -10, u) + sens * -60 * o, az=mix(sens * -25, sens * 4, u) + sens * 30 * o),
              W_, H_, dessin_claque(j, t), borne(u * 4), recto=False)
    lueur_s(c, CX, 1040, 520, BLEU, 0.45 * borne(u * 2) * (1 - o))
    scene3d(c, cam, [pl])
    onde(c, CX, 1040, t, t0 + 0.12, 120, 620, S["lilas"], 8, 0.6)
    eclats(c, CX, 1040, t, t0 + 0.12, 12, 470, cols=[S["lilas"], GLACIER, "#FFC53D"], graine=31 + j)
    titre(c, t, None, lab, t0 - 0.02, t1 - 0.02, y=330, t2=t0 - 0.02)


def scene_hook(c, t):
    if t > T_ABO + 0.3: return
    part = prog(t, T_ABO - 0.25, 0.4, entree)
    retrait = prog(t, T_UNE1 - 0.15, 0.25, sortie) * (1 - prog(t, T_ENVOIE - 0.2, 0.4, sortie))
    with Calque(c, 1 - part):
        o = prog(t, 0.0, 1.4, douce)
        cam = Cam(ax=mix(-26, -12, o) + 2 * math.sin(t * 1.3), ay=mix(-30, 16, o) + 4 * math.sin(t * 0.9), az=mix(-6, 2, o),
                  tz=mix(260, 60, o) + 900 * part + 1500 * retrait, cx=CX, cy=1000)
        sx, sy = secousse(t, 0.0, 14, 0.3)
        for _, t0, _, _ in JAILLIT:
            if t0 < T_UNE1 - 0.3:
                a, b = secousse(t, t0, 6, 0.16); sx, sy = sx + a, sy + b
        for t0, _, _, _ in CLAQUES:
            a, b = secousse(t, t0 + 0.12, 18, 0.25); sx, sy = sx + a, sy + b
        a, b = secousse(t, T_PHOTO, 10, 0.25); sx, sy = sx + a, sy + b
        cam.cx, cam.cy = CX + sx, 1000 + sy
        PW_, PH_ = 370, 756
        with Calque(c, 1 - 0.97 * retrait):
            scene3d(c, cam, [Plan(coins((0, 0, 0), PW_, PH_), PW_, PH_, tel(ecran_hook(t)))])
        X0, Y0 = cam.proj((0, -60, 0))[:2]
        for _, t0, _, _ in JAILLIT:
            if t0 < T_UNE1 - 0.3: onde(c, X0, Y0, t, t0, 80, 420, S["lilas"], 6, 0.55)
        for item, t0, direc, sens in JAILLIT:
            if t0 < T_UNE1 - 0.3: objet_volant(c, item, t, t0, direc, sens, X0, Y0)
        c.save(); c.translate(sx, sy)
        for j in range(3): claque(c, t, j)
        c.restore()
        u = entre(t, T_CHINE - 0.12, 0.4, 2.2)
        if u > 0:
            with Espace(c, 760, 760, ry=-26 + 8 * math.sin(t * 3), rx=12, rz=8):
                c.save(); c.translate(760, 760); c.scale(mix(0.2, 1, u), mix(0.2, 1, u))
                rrect(c, -88, -60, 176, 120, 22, "#FFFFFF", borne(u * 2), (14, 36, 0.25))
                drapeau(c, "CN", -74, -46, 148, 92, 12)
                c.restore()
            eclats(c, 760, 760, t, T_CHINE - 0.05, 12, 360, graine=4)
        if t > T_TROUVE - 0.1: eclats(c, X0, Y0 + 200, t, T_TROUVE, 14, 420, cols=[VERT_, S["lilas"], GLACIER], graine=2)
    titre(c, t, "TU VEUX", "UNE PAIRE ?", -0.45, T_UNE2 - 0.04, t2=-0.3)
    titre(c, t, "ENVOIE", "LA PHOTO", T_ENVOIE - 0.04, T_JE - 0.04, t2=T_PHOTO - 0.1, e1="ressort")
    titre(c, t, "ON TE LA TROUVE", "EN CHINE", T_JE - 0.04, T_ABO - 0.05, t2=T_CHINE - 0.1)


# ─────────────────────────────────────────── 2. abonne-toi (juste après le hook)
def scene_abo(c, t):
    t0, t1 = T_ABO - 0.15, T_ON - 0.12
    g = Groupe(c, t, t0, t1, ent="grand", sor="recul", d_in=0.4, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        tap = T_EXPL + 0.15
        ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
        abonne = t > tap
        cam = Cam(ax=-12 + 3 * math.sin(t), ay=mix(-35, 12, a) + 4 * math.sin(t * 0.8), tz=mix(900, 20, a), cx=CX, cy=980)
        W_, H_ = 680, 440
        def profil(cc, w, h):
            verre(cc, 0, 0, w, h, 50)
            cc.save(); cc.translate(w / 2, 112)
            p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 20))
            cc.drawCircle(0, 0, 74, p)
            disque(cc, 0, 0, 74, "#FFFFFF"); anneau(cc, 0, 0, 74, S["lilas"], 3, 0.9)
            iw, ih = taille_img(LOGO); image(cc, LOGO, -56, -56 * ih / iw, 112)
            cc.restore()
            texte(cc, "Drop&You", w / 2, 206, 46, ENCRE, "titre", "centre", -0.02)
            texte(cc, "Basés à Guangzhou, en Chine", w / 2, 264, 25, GRIS, "demi", "centre", 0)
            bw, bh = 360, 84
            s_ = 1 - 0.08 * ap
            cc.save(); cc.translate(w / 2, 364); cc.scale(s_, s_)
            if not abonne:
                cc.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-bw / 2, -bh / 2, bw, bh), 22, 22), pgrad(-bw / 2, 0, bw / 2, 0, ["#FF3B5C", "#FF5A73"]))
                icone(cc, "circle-plus", -bw / 2 + 86, 0, 38, "#FFFFFF", 2.6)
                texte(cc, "S'abonner", -bw / 2 + 118, -hauteurLigne(32, "titre") / 2, 32, "#FFFFFF", "titre", track=-0.01)
            else:
                verre(cc, -bw / 2, -bh / 2, bw, bh, 22, 1.0, None, 0.6)
                icone(cc, "check", -bw / 2 + 92, 0, 34, VERT_, 3)
                texte(cc, "Abonné", -bw / 2 + 122, -hauteurLigne(32, "titre") / 2, 32, ENCRE, "titre", track=-0.01)
            cc.restore()
        # derrière la carte, les produits qui tournent lentement (le produit reste à l'écran)
        plans = []
        for j in range(4):
            ang = t * 0.9 + j * math.pi / 2
            nom = DETOURES[j % len(DETOURES)]; iw, ih = taille_img(nom); ww = 230 if ih < iw else 180; hh = ww * ih / iw
            plans.append(Plan(coins((300 * math.cos(ang), -40 + 160 * math.sin(ang * 0.7), 260 + 160 * math.sin(ang)), ww, hh, ay=20 * math.cos(ang)),
                              ww, hh, lambda cc, w, h, nom=nom: image(cc, nom, 0, 0, w), 0.55 * borne(a * 2)))
        plans.append(Plan(coins((0, 0, 0), W_, H_), W_, H_, profil))
        scene3d(c, cam, plans)
        cu = prog(t, tap - 0.45, 0.4, sortie)
        if cu > 0:
            curseur(c, mix(820, 590, cu), mix(1450, 1210, cu), 1.2, 1 - prog(t, tap + 0.5, 0.3), ap)
            clic(c, 580, 1200, t, tap)
        if abonne:
            eclats(c, CX, 1160, t, tap + 0.02, 14, 400, graine=6)
            for j in range(5):
                hj = prog(t, tap + 0.05 + 0.08 * j, 1.1, sortie)
                if 0 < hj < 1:
                    icone(c, "heart", 620 + 60 * math.sin(j * 2.1), 1160 - 520 * hj, 44 * (1 - 0.4 * hj), "#FF5A73", 2.6, 1 - hj)
        titre(c, t, "ABONNE-TOI", "JE TE MONTRE", T_ABO - 0.05, t1, t2=TW(18), e1="ressort", e2="masque")


# ─────────────────────────────────────────── 3. sur place, à Guangzhou, fournisseurs validés (vraies vidéos)
def scene_place(c, t):
    t0, t1 = T_ON - 0.12, T_BASK - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="zoom", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.7, 1.3)
        cam = Cam(ax=-8 + 2 * math.sin(t), ay=mix(-26, 10, prog(t, t0, t1 - t0, douce)), tz=mix(500, 40, a), cx=CX, cy=980)
        FW, FH = 560, 700
        # seulement la 1re seconde de l'entrepôt (ensuite on lit une marque sur les cartons) ; le lieu réel 1 s sur « Guangzhou »
        coupe, retour = T_GZ - 0.1, T_AVEC + 0.25
        if t < coupe:
            dessin = carte_video("entrepot-cartons", t - t0, 1.0, False)
        elif t < retour:
            dessin = carte_video(GZ_NUIT, t - coupe + 0.8, 1.0, False)       # Guangzhou de nuit, filmé par Youssef
        else:
            dessin = carte_video("entrepot-cartons", t - retour, 1.0, False)
        scene3d(c, cam, [Plan(coins((0, 0, 0), FW, FH), FW, FH, dessin)])
        for tc in (coupe, retour):
            fl = 1 - (t - tc) / 0.14
            if 0 < fl <= 1: c.drawRect(skia.Rect.MakeWH(1080, 1920), peinture("#FFFFFF", 0.35 * fl))
        b = entre(t, T_GZ - 0.1, 0.45, 2.2)
        if b > 0:
            pill(c, "Guangzhou, la nuit", CX, 690, 30, "vert", None, borne(b * 3), mix(0.4, 1, b))
            disque(c, CX - largeur("Guangzhou, la nuit", 30, "fort", -0.01) / 2 - 2, 690, 7, VERT_, 0.5 + 0.5 * math.sin(t * 9))
        f = entre(t, T_FOURN - 0.12, 0.45, 2.0)
        if f > 0:
            c.save(); c.translate(CX + 40, 1190); c.rotate(-3); c.scale(mix(0.4, 1, f), mix(0.4, 1, f))
            with Calque(c, borne(f * 3)):
                verre(c, -250, -80, 500, 160, 40)
                tuile(c, "badge-check", -170, 0, 86, "grad")
                texte(c, "Fournisseur", -110, -46, 34, ENCRE, "titre", track=-0.02)
                texte(c, "validé", -110, -4, 34, GLACIER, "titre", track=-0.02)
                for j in range(3): disque(c, 160 + 26 * j, 0, 8, VERT_, 1.0 if t > T_VALID + 0.05 * j else 0.25)
            c.restore()
            eclats(c, CX + 40, 1190, t, T_VALID, 12, 340, graine=8)
        titre(c, t, "ON EST BASÉS", "À GUANGZHOU", T_ON - 0.05, T_MONT - 0.05, t2=T_GZ - 0.05)


# ─────────────────────────────────────────── 4. montres, doudounes, baskets, électronique → tu montres le modèle
def ecran_modele(t):
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), pgrad(0, 0, 0, h, ["#FFFFFF", "#F3F0F8"]))
        entete_dm(c, w, k)
        bulle_photo(c, w, k, 170 * k, prog(t, T_MODELE - 0.25, 0.4, sortieExpo), PORTEE, coupe=True)
        r = prog(t, T_OCCUPE - 0.05, 0.35, sortieExpo)
        if r > 0: bulle_reponse(c, k, 540 * k, r, "C'est noté", "on s'occupe de tout")
    return f


def scene_cats(c, t):
    t0, t1 = T_MONT - 0.12, T_REGARDE - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="gauche", d_in=0.3, d_out=0.3)
    if not g.visible: return
    with g:
        tel_ = prog(t, T_TU - 0.2, 0.7, entreeSortie)
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.9), ay=mix(-14, 8, tel_) + 5 * math.sin(t * 0.7), tz=mix(-60, 80, tel_), cx=CX, cy=1000)
        cats = [(T_MONT, lambda cc, w, h: carte_video("montres-bleues", t - T_MONT + 1.0, 1.3)(cc, w, h), "Montres"),
                (T_DOUD, produit_plan(DOUD2, place=0.6), "Doudounes"),
                (T_BASK, paires_defilent(t, T_BASK), "Baskets"),
                (T_ELEC, produit_plan(DYSON, place=0.6), "High-tech")]
        plans = []
        CW, CH = 300, 370
        for k, (tk, dessin, lab) in enumerate(cats):
            u = prog(t, tk - 0.15, 0.55, lambda v: ressort(v, 1.3, 4.6)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            gx, gy = (-165 if k % 2 == 0 else 165), (-195 if k < 2 else 200)
            x = mix(gx, gx * 2.2, tel_); y = mix(gy, gy * 1.6, tel_); z = mix(900, 0, min(u, 1.05)) - 300 * tel_
            rot = mix(-40 if k % 2 == 0 else 40, (k - 1.5) * 4, min(u, 1))
            plans.append(Plan(coins((x, y, z), CW, CH, ay=rot, az=(k - 1.5) * 2), CW, CH, carte_cat(dessin, lab), borne(u * 3) * (1 - tel_)))
        if tel_ > 0:
            PW_, PH_ = 400, 816
            plans.append(Plan(coins((0, mix(900, 0, tel_), mix(400, 0, tel_)), PW_, PH_, ay=mix(-30, -6, tel_)), PW_, PH_, tel(ecran_modele(t)), borne(tel_ * 2)))
        scene3d(c, cam, plans)
        if False:
            for tk, lab in [(T_MONT, "MONTRES"), (T_DOUD, "DOUDOUNES"), (T_BASK, "BASKETS"), (T_ELEC, "CASQUES")]:
                fin = min([x for x in (T_DOUD, T_BASK, T_ELEC, T_TU) if x > tk] or [T_TU])
                if tk - 0.1 < t < fin:
                    lettres(c, lab, 540, 420, ajuste(lab, 760, 140, "noir", -0.035), t, tk - 0.08, "masque", decal=0.02, duree=0.3,
                            alpha=1 - prog(t, fin - 0.08, 0.08))
        if t > T_OCCUPE: eclats(c, CX, 1100, t, T_OCCUPE + 0.05, 12, 380, cols=[VERT_, S["lilas"], GLACIER], graine=9)
        titre(c, t, "TU NOUS DIS", "LE MODÈLE", T_TU - 0.05, T_OCCUPE - 0.05, t2=T_MODELE - 0.05)
        titre(c, t, "ON S'OCCUPE", "DE TOUT", T_OCCUPE - 0.05, t1, t2=T_RESTE - 0.1, e1="ressort")


# ─────────────────────────────────────────── 4 bis. « Regarde Alyssa » : elle parle dans le téléphone (la voix off se tait),
#    puis « comme elle, des centaines de clients » : ses avis Snapchat en éventail
def ecran_influ(t):
    def f(c, w, h):
        k = w / 440
        video(c, INFLU, 0, 0, w, h, t - T_CLIP, 1.0, False)
        # bandeau du compte, en haut de l'écran (logo DROP&YOU en en-tête d'appli)
        rrect(c, 0, 0, w, 96 * k, 0, "#05070F", 0.55)
        disque(c, 44 * k, 48 * k, 24 * k, "#FFFFFF"); image(c, LOGO, 26 * k, 40 * k, 36 * k)
        texte(c, INFLU_AT, 80 * k, 26 * k, 22 * k, "#FFFFFF", "titre", track=-0.01)
        texte(c, INFLU_ROLE, 80 * k, 56 * k, 16 * k, "#D9D3E6", "demi", track=0)
        icone(c, "badge-check", w - 40 * k, 48 * k, 28 * k, VERT_, 2.4)
        # barre de lecture
        d = prog(t, T_CLIP, P1 - 0.35 - T_CLIP, lin)
        rrect(c, 24 * k, h - 30 * k, w - 48 * k, 6 * k, 3 * k, "#FFFFFF", 0.25); rrect(c, 24 * k, h - 30 * k, (w - 48 * k) * d, 6 * k, 3 * k, GLACIER)
        if t < T_CLIP: disque(c, w / 2, h / 2, 54 * k, "#FFFFFF", 0.9); icone(c, "play", w / 2 + 4 * k, h / 2, 44 * k, "#0B1126", 3)
    return f


def scene_influ(c, t):
    t0, t1 = T_REGARDE - 0.12, T_PLUS - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="gauche", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        av = prog(t, T_COMME - 0.2, 0.7, entreeSortie)             # les avis arrivent, le téléphone recule à gauche
        cam = Cam(ax=-8 + 2 * math.sin(t * 0.8), ay=mix(-24, 6, a) + 3 * math.sin(t * 0.6) - 10 * av, tz=mix(700, 0, a) + 220 * av, cx=CX, cy=1000)
        PW_, PH_ = 440, 900
        plans = [Plan(coins((mix(0, -260, av), mix(0, -40, av), mix(0, 260, av)), PW_, PH_, ay=mix(0, 22, av)), PW_, PH_, tel(ecran_influ(t)), borne(a * 2))]
        if av > 0:
            for j, nom in enumerate(AVIS):
                d = prog(t, T_CENT - 0.1 + 0.12 * j, 0.5, lambda v: ressort(v, 1.3, 4.8))
                if d <= 0: continue
                AW, AH = 250, 330
                x = 80 + (j % 2) * 215; y = -220 + (j // 2) * 360 + 700 * (1 - min(d, 1))
                plans.append(Plan(coins((x, y, 80 - 40 * j), AW, AH, ay=-12 + 4 * j, az=-5 + 3 * j), AW, AH,
                                  lambda cc, w, h, nom=nom: (photo_ronde(cc, nom, w, h, w * 0.08), icone(cc, "badge-check", w - 30, 30, 34, VERT_, 2.6)), borne(d * 3)))
        scene3d(c, cam, plans)
        if P0 + 0.4 < t < P1 - 0.1:       # pendant qu'elle parle : ce qu'elle dit, à la place des sous-titres
            u = entre(t, P0 + 0.4, 0.4, 1.6)
            pill(c, "« J'ai commandé une paire chez Drop and You »", 500, 1410, 28, "doux", None, borne(u * 3) * (1 - prog(t, P1 - 0.4, 0.3)), mix(0.6, 1, u))
        if av > 0:
            m = entre(t, T_AVIS - 0.1, 0.45, 2.2)
            if m > 0: pill(c, "Leurs avis sont sur le site", CX, 1330, 30, "grad", "star", borne(m * 3), mix(0.4, 1, m), rot=-2)
        titre(c, t, "LUI, IL A COMMANDÉ", "SA PAIRE", T_REGARDE - 0.05, P0 + 0.3, t2=T_RECU - 0.1, e1="ressort")
        titre(c, t, "COMME LUI", "DES CENTAINES DE CLIENTS", T_COMME - 0.05, t1, t2=T_CENT - 0.05)


# ─────────────────────────────────────────── 5. plusieurs qualités, livraison incluse
def scene_qualites(c, t):
    t0, t1 = T_SELON - 0.12, T_HUIT - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        ev = prog(t, T_PLUS - 0.1, 0.7, entreeSortie)
        prix_ = prog(t, T_ET - 0.1, 0.6, entreeSortie)
        TROIS = [VESTES[1], MONTRES_PNG[0], PAIRES[0]]
        cam = Cam(ax=-10 + 3 * math.sin(t), ay=8 * math.sin(t * 0.7) - 12 * prix_, tz=mix(120, 20, ev), cx=CX, cy=960)
        CW, CH = 260, 360
        plans = []
        for k in range(3):
            u = prog(t, t0 + 0.1 + 0.12 * k, 0.5, sortieExpo)
            x = mix(0, (k - 1) * 230, ev); z = (k - 1) * -30 + (1 - u) * 800 + mix(k * 40, 0, ev)
            def carte(cc, w, h, k=k):
                produit_plan(TROIS[k], haut=0.42, place=0.5)(cc, w, h)
                for j in range(3):
                    disque(cc, w / 2 - 30 + 30 * j, h * 0.84, 9, GLACIER, 1.0 if j <= k else 0.2)
            plans.append(Plan(coins((x, -40 - 160 * prix_, z + 300 * prix_), CW, CH, ay=mix(0, (k - 1) * -14, ev)), CW, CH, carte, borne(u * 3) * (1 - 0.75 * prix_)))
        scene3d(c, cam, plans)
        b = entre(t, T_QUAL - 0.1, 0.45, 2.2) * (1 - prix_)
        if b > 0: pill(c, "Selon les articles", CX, 1260, 32, "doux", "layers", borne(b * 3), mix(0.4, 1, b), rot=-2)
        if prix_ > 0:
            c.save(); c.translate(CX, 1190); c.rotate(mix(-14, -4, prix_)); s_ = mix(0.3, 1, prix_); c.scale(s_, s_)
            with Calque(c, borne(prix_ * 3)):
                verre(c, -310, -90, 620, 180, 44)
                tuile(c, "truck", -225, 0, 92, "grad")
                texte(c, "Livraison", -158, -54, 40, ENCRE, "titre", track=-0.02)
                l = entre(t, T_LIVR - 0.1, 0.4, 2.4)
                if l > 0:
                    c.save(); c.translate(-158 + largeur("comprise", 44, "noir") / 2, 22); c.scale(mix(1.8, 1, l), mix(1.8, 1, l))
                    texte(c, "comprise", -largeur("comprise", 44, "noir") / 2, -26, 44, GLACIER, "noir", track=-0.02, alpha=borne(l * 3))
                    c.restore()
                    icone(c, "check", 236, 0, 56, VERT_, 3.4, borne(l * 3))
            c.restore()
            eclats(c, CX, 1190, t, T_LIVR, 14, 400, graine=11)
        titre(c, t, "SELON LES ARTICLES", "PLUSIEURS QUALITÉS", T_SELON - 0.05, T_ET - 0.08, t2=T_PLUS - 0.05)
        titre(c, t, "ET LE PRIX", "COMPREND LA LIVRAISON", T_ET - 0.08, t1, t2=T_PRIX)


# ─────────────────────────────────────────── 6. 8 à 12 jours, devant ta porte (vraie vidéo de l'avion)
def carton3d_g(centre, taille, ay=0.0, ax=0.0, az=0.0, alpha=1.0):
    def face(c, w, h):
        rrect(c, 0, 0, w, h, 8, "#C8955A")
        rrect(c, w * 0.42, 0, w * 0.16, h, 0, "#E2B97E")
        rrect(c, w * 0.12, h * 0.6, w * 0.3, h * 0.24, 6, "#F3F0EA", 0.95)
    def cote(c, w, h): rrect(c, 0, 0, w, h, 8, "#B48048")
    def haut(c, w, h):
        rrect(c, 0, 0, w, h, 8, "#D9A86A"); rrect(c, 0, h * 0.42, w, h * 0.16, 0, "#EAC48E")
    return boite(centre, taille, taille * 0.8, taille * 0.8, dict(avant=face, arriere=face, gauche=cote, droite=cote, haut=haut, bas=cote),
                 ax=ax, ay=ay, az=az, alpha=alpha)


def scene_livraison(c, t):
    t0, t1 = T_HUIT - 0.12, T_UNITE - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="recul", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        porte = prog(t, T_DEVANT - 0.15, 0.5, entreeSortie)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-24, 14, prog(t, t0, t1 - t0, douce)), tz=mix(600, 120, a), cx=CX, cy=1090)
        FW, FH = 520, 640
        plans = [Plan(coins((0, 0, mix(0, 160, porte)), FW, FH), FW, FH, carte_video("avion", t - t0 + 0.2, 1.0), 1 - 0.5 * porte)]
        if porte > 0:
            d = prog(t, T_DEVANT - 0.1, 0.5, lambda v: ressort(v, 1.3, 4.6))
            plans += carton3d_g((0, mix(-700, 120, min(d, 1)), -260), 200, ay=24 + 30 * (1 - min(d, 1)))
        scene3d(c, cam, plans)
        if porte > 0:
            u = entre(t, T_PORTE - 0.1, 0.45, 2.2)
            if u > 0: pill(c, "Devant ta porte", CX, 1330, 32, "grad", "house", borne(u * 3), mix(0.4, 1, u), rot=-2)
        n = entre(t, T_HUIT - 0.1, 0.45, 1.8)
        if n > 0:
            j = 8 if t < T_DOUZE - 0.2 else 8 + int(round(4 * prog(t, T_DOUZE - 0.2, 0.35, sortie)))
            with Calque(c, borne(n * 3) * (1 - prog(t, t1 - 0.2, 0.15))):
                lettres(c, f"8 À {j}" if j > 8 else "8", 540, 380, 150, t, T_HUIT - 0.08, "ressort", decal=0.04)
                lettres(c, "JOURS", 540, 550, 80, t, T_JOURS - 0.1, "masque", grad=False, couleur=ENCRE, decal=0.03, duree=0.3)


# ─────────────────────────────────────────── 7. une seule pièce, ou un carton entier (les planches défilent dans le téléphone)
def ecran_planches(t):
    """défilé rapide des planches de paires (4 photos par seconde) : ça glisse vers le haut comme un fil"""
    def f(c, w, h):
        c.drawRect(skia.Rect.MakeWH(w, h), pgrad(0, 0, 0, h, ["#FFFFFF", "#F3F0F8"]))
        k = w / 440
        entete_dm(c, w, k)
        u = max(0.0, t - T_QTE) * 4.0
        i, fr = int(u), u - int(u)
        g = sortieExpo(fr)
        ph = h - 120 * k
        for d in (0, 1):
            nom = PLANCHES[(i + d) % len(PLANCHES)]
            y = 120 * k + (d - g) * ph
            image_cover(c, nom, 0, y, w, ph, 1.0, 0.5, 0.35, 0)
        rrect(c, 0, 120 * k, w, 6 * k, 0, "#FBFAFE")
    return f


def scene_quantite(c, t):
    t0, t1 = T_UNITE - 0.12, T_SAVE - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="zoom", d_in=0.3, d_out=0.3)
    if not g.visible: return
    with g:
        q = prog(t, T_QTE - 0.25, 0.6, entreeSortie)
        a = prog(t, t0, 0.55, lambda v: ressort(v, 1.4, 4.6))
        cam = Cam(ax=-14 + 3 * math.sin(t), ay=18 * math.sin(t * 0.8) * (1 - q), tz=mix(0, 120, q), cx=CX, cy=1000)
        plans = []
        # l'unité : le casque seul
        iw, ih = taille_img(PAIRES[3]); PWU = 440; PHU = PWU * ih / iw
        plans.append(Plan(coins((0, mix(400, 0, min(a, 1)), mix(0, -400, q)), PWU, PHU, ay=25 * math.sin(t * 1.4)), PWU, PHU,
                          lambda cc, w, h: image(cc, PAIRES[3], 0, 0, w), borne(a * 3) * (1 - q)))
        # la quantité : le téléphone où les planches de paires défilent vite (photos en situation, jamais détourées),
        # et quelques articles du lot qui tombent autour
        if q > 0:
            PW_, PH_ = 400, 816
            plans.append(Plan(coins((0, mix(700, 0, q), mix(300, -40, q)), PW_, PH_, ay=mix(-26, -4, q)), PW_, PH_, tel(ecran_planches(t)), borne(q * 2)))
            for n, (nom, photo) in enumerate(MELANGE[:6]):
                d = prog(t, T_QTE + 0.15 + 0.06 * n, 0.45, lambda v: ressort(v, 1.3, 5))
                if d <= 0 or photo: continue
                iw, ih = taille_img(nom); w_ = 170; h_ = w_ * ih / iw
                if h_ > 170: h_ = 170; w_ = h_ * iw / ih
                x = (-330 if n % 2 == 0 else 330); y = (n // 2 - 1) * 250 - 700 * (1 - min(d, 1))
                plans.append(Plan(coins((x, y, 120), w_, h_, az=-8 + 5 * n), w_, h_, lambda cc, w, h, nom=nom: image(cc, nom, 0, 0, w), borne(d * 3)))
        scene3d(c, cam, plans)
        titre(c, t, "À L'UNITÉ", "OU EN QUANTITÉ", T_UNITE - 0.05, t1, t2=T_QTE - 0.1, e1="ressort", e2="ressort")


# ─────────────────────────────────────────── 8. enregistre la vidéo
def scene_save(c, t):
    t0, t1 = T_SAVE - 0.12, T_COMM - 0.12
    jaune = prog(t, T_JAUNE - 0.15, 0.5, entreeSortie)
    g = Groupe(c, t, t0, t1, ent="grand", sor="gauche", d_in=0.3, d_out=0.28)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.6)
        tap = T_VIDEO + 0.05
        rempli = prog(t, tap, 0.25, sortie)
        ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
        # les produits en orbite autour du signet
        for j in range(5):
            ang = t * 1.1 + j * 2 * math.pi / 5
            x, y = CX + 300 * math.cos(ang), 990 + 210 * math.sin(ang)
            pr = 0.5 + 0.5 * math.sin(ang)
            nom = DETOURES[j % len(DETOURES)]
            w = 150 + 80 * pr
            if math.sin(ang) < 0: image(c, nom, x - w / 2, y - w * 0.3, w, 0.5 * borne(a * 2))
        c.save(); c.translate(CX, 980); s_ = mix(0.4, 1, a) * (1 - 0.08 * ap) * (1 + 0.1 * battement(t, tap, 1, 0.4) - 0.1) * (1 - jaune)
        c.scale(s_, s_); c.rotate(4 * math.sin(t * 1.6))
        p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.5 + 0.3 * rempli), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 40))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200, -200, 400, 400), 100, 100), p)
        verre(c, -200, -200, 400, 400, 100)
        pth = skia.Path(); pth.moveTo(-76, -114); pth.lineTo(76, -114); pth.lineTo(76, 124); pth.lineTo(0, 66); pth.lineTo(-76, 124); pth.close()
        if rempli > 0:
            c.save(); c.clipRect(skia.Rect.MakeXYWH(-90, 134 - 260 * rempli, 180, 260 * rempli))
            c.drawPath(pth, pgrad(-76, -114, 76, 124, ["#FFD86B", "#FFC53D"])); c.restore()
        c.drawPath(pth, peinture(ENCRE, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=10, StrokeJoin=skia.Paint.kRound_Join))
        c.restore()
        for j in range(5):
            ang = t * 1.1 + j * 2 * math.pi / 5
            if math.sin(ang) >= 0:
                x, y = CX + 300 * math.cos(ang), 990 + 210 * math.sin(ang)
                pr = 0.5 + 0.5 * math.sin(ang); w = 150 + 80 * pr
                image(c, DETOURES[j % len(DETOURES)], x - w / 2, y - w * 0.3, w, borne(a * 2))
        cu = prog(t, tap - 0.45, 0.4, sortie)
        if cu > 0:
            curseur(c, mix(820, 580, cu), mix(1450, 1040, cu), 1.3, 1 - prog(t, tap + 0.4, 0.25), ap)
            clic(c, 570, 1030, t, tap)
        if t > tap: eclats(c, CX, 980, t, tap + 0.02, 16, 440, cols=["#FFC53D", S["lilas"], GLACIER], graine=14)
        titre(c, t, "ENREGISTRE", "LA VIDÉO", T_SAVE - 0.05, T_JAUNE - 0.05, t2=T_VIDEO - 0.05, e1="ressort", e2="masque")
        titre(c, t, "AJOUTE-MOI SUR", "L'APPLI JAUNE", T_JAUNE - 0.05, t1, t2=TW(94) - 0.05, e1="ressort", e2="ressort")
        if jaune > 0:
            # une bulle jaune qui remplace le signet : fantôme jamais dessiné, juste la couleur
            c.save(); c.translate(CX, 980); s_ = mix(0.3, 1, jaune); c.scale(s_, s_); c.rotate(-6 + 6 * jaune)
            with Calque(c, borne(jaune * 3)):
                p = skia.Paint(AntiAlias=True, Color=hexa("#FFFC00", 0.55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 40))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200, -200, 400, 400), 100, 100), p)
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200, -200, 400, 400), 100, 100), pgrad(-200, -200, 200, 200, ["#FFFC00", "#F2E600"]))
                icone(c, "user-round", -20, 0, 170, "#0B0F0D", 2.6); icone(c, "circle-plus", 110, -70, 80, "#0B0F0D", 3.0)
            c.restore()
            eclats(c, CX, 980, t, T_JAUNE + 0.3, 14, 420, cols=["#FFFC00", S["lilas"], "#F2C200"], graine=21)


# ─────────────────────────────────────────── 9. dis-moi en commentaire ce que tu cherches → on te répond
def scene_fin(c, t):
    t0 = T_COMM - 0.12
    if t < t0: return
    fin = prog(t, T_FIN - 0.1, 0.4, entreeSortie)
    with Calque(c, 1 - fin):
        a = entre(t, t0, 0.5, 1.5)
        rep = prog(t, T_REPONDS - 0.2, 0.55, entreeSortie)
        cam = Cam(ax=-10 + 3 * math.sin(t), ay=mix(-30, 8, a) + 4 * math.sin(t * 0.8), tz=mix(800, 60, a), cx=CX, cy=1000)
        W_, H_ = 700, 300
        def commentaire(cc, w, h):
            verre(cc, 0, 0, w, h, 44)
            disque(cc, 76, 86, 40, S["lavande"]); icone(cc, "user-round", 76, 86, 42, GLACIER, 2.2)
            texte(cc, "Toi", 136, 50, 26, GRIS, "demi", track=0)
            s = "Vous avez ce sac ?"
            n = int(borne((t - T_COMMENT) / 0.55) * len(s) + 0.999) if t > T_COMMENT else 0
            texte(cc, s[:n], 136, 88, 36, ENCRE, "titre", track=-0.01)
            if n < len(s) and int(t * 3) % 2 == 0: rrect(cc, 140 + largeur(s[:n], 36, "titre", -0.01), 90, 4, 40, 2, GLACIER)
            ph = prog(t, T_CHERCHE - 0.1, 0.35, sortieExpo)
            if ph > 0:
                with Calque(cc, borne(ph * 3)):
                    image_cover(cc, PLANCHES[1], 136, 146, 150, 130, 1.0, 0.5, 0.4, 18)
            icone(cc, "heart", w - 60, 86, 38, "#FF5A73", 2.6)
        def reponse(cc, w, h):
            verre(cc, 0, 0, w, h, 44)
            disque(cc, 76, 86, 40, "#FFFFFF"); anneau(cc, 76, 86, 40, S["lilas"], 2, 0.9)
            iw, ih = taille_img(LOGO); image(cc, LOGO, 46, 86 - 30 * ih / iw, 60)
            texte(cc, "Drop&You", 136, 50, 26, GLACIER, "titre", track=0)
            rrect(cc, 136 + largeur("Drop&You", 26, "titre") + 12, 54, 104, 30, 15, BLEU)
            texte(cc, "Créateur", 136 + largeur("Drop&You", 26, "titre") + 64, 57, 18, "#FFFFFF", "demi", "centre", 0)
            texte(cc, "Oui, on l'a", 136, 98, 44, ENCRE, "titre", track=-0.02)
            ok = entre(t, T_LA - 0.1, 0.4, 2.4)
            if ok > 0: icone(cc, "badge-check", 136 + largeur("Oui, on l'a", 44, "titre", -0.02) + 40, 124, 46 * mix(0.4, 1, ok), VERT_, 2.8, borne(ok * 3))
        plans = [Plan(coins((0, mix(-60, -190, rep), mix(0, 160, rep)), W_, H_), W_, H_, commentaire, 1 - 0.3 * rep)]
        if rep > 0:
            plans.append(Plan(coins((40, mix(420, 150, rep), mix(600, -60, rep)), W_ - 40, 230), W_ - 40, 230, reponse, borne(rep * 3)))
        scene3d(c, cam, plans)
        if t > T_LA: eclats(c, CX, 1160, t, T_LA, 14, 400, cols=[VERT_, S["lilas"], GLACIER], graine=15)
        titre(c, t, "DIS-MOI EN COMMENTAIRE", "CE QUE TU CHERCHES", T_COMM - 0.05, T_REPONDS - 0.12, t2=T_COMMENT - 0.05)
        titre(c, t, "JE TE RÉPONDS", "SI ON L'A", T_REPONDS - 0.12, T_FIN, t2=TW(107) - 0.05, e1="ressort")


# ─────────────────────────────────────────── sons
son(0.0, "whoosh_bas", -8); son(0.0, "impact", -7)
for _, t0, _, _ in JAILLIT:
    if 0 <= t0 < T_UNE1 - 0.3: son(t0, "whoosh_court", -12); son(t0 + 0.02, "pop", -13)
for t0, _, _, _ in CLAQUES: son(t0 - 0.1, "whoosh", -8); son(t0 + 0.12, "impact", -6)
son(T_ENVOIE - 0.2, "whoosh_court", -10); son(T_ENVOIE, "montee", -13); son(T_PHOTO, "clic", -5); son(T_PHOTO + 0.02, "impact_doux", -9); son(T_PHOTO + 0.1, "message_in", -11)
son(T_TROUVE - 0.1, "message_in", -10); son(T_TROUVE, "check", -9); son(T_CHINE - 0.12, "pop", -9); son(T_CHINE, "ching", -11)
son(T_ABO - 0.15, "whoosh", -9); son(T_EXPL + 0.15, "clic", -6); son(T_EXPL + 0.2, "check", -10)
for j in range(5): son(T_EXPL + 0.22 + 0.08 * j, "blip", -18)
son(T_ON - 0.12, "whoosh_long", -9); son(T_GZ - 0.1, "impact_doux", -8); son(T_GZ, "ding", -13)
son(T_FOURN - 0.12, "pop", -10); son(T_VALID, "check", -9); son(T_VALID + 0.05, "ching", -12)
for tk in (T_MONT, T_DOUD, T_BASK, T_ELEC): son(tk - 0.15, "whoosh_court", -11); son(tk - 0.05, "pop", -10)
son(T_TU - 0.2, "whoosh_long", -9); son(T_MODELE - 0.25, "message_in", -10); son(T_OCCUPE - 0.05, "message_in", -11); son(T_OCCUPE + 0.05, "check", -10)
son(T_REGARDE - 0.12, "whoosh", -9); son(T_NOM - 0.1, "pop", -10); son(T_CLIP - 0.05, "clic", -8)
son(T_COMME - 0.2, "whoosh_court", -10)
for j in range(4): son(T_CENT - 0.1 + 0.12 * j + 0.2, "impact_doux", -11)
son(T_AVIS - 0.1, "ding", -12)
son(T_SELON - 0.12, "swipe", -10)
for k in range(3): son(T_SELON + 0.1 + 0.12 * k, "pop", -12)
son(T_PLUS - 0.2, "whoosh_court", -11); son(T_QUAL - 0.1, "pop", -11)
son(T_ET - 0.1, "whoosh", -9); son(T_LIVR - 0.1, "tampon", -8); son(T_LIVR, "ching", -10)
son(T_HUIT - 0.12, "whoosh_long", -9); son(T_HUIT - 0.1, "impact_doux", -9)
for i in range(4): son(T_DOUZE - 0.2 + 0.09 * i, "blip", -16)
son(T_DEVANT - 0.1, "whoosh_court", -10); son(T_DEVANT + 0.3, "tampon", -8); son(T_PORTE - 0.1, "ding", -12)
son(T_UNITE - 0.12, "whoosh", -9); son(T_UNITE + 0.2, "impact_doux", -9)
son(T_QTE - 0.2, "whoosh_long", -10)
for i in range(10): son(T_QTE + 0.25 * i, "swipe", -17)
for i in range(6): son(T_QTE + 0.15 + 0.06 * i + 0.3, "pop", -15)
son(T_SAVE - 0.12, "whoosh", -9); son(T_VIDEO + 0.05, "clic", -6); son(T_VIDEO + 0.1, "ching", -9); son(T_JAUNE - 0.1, "pop", -9); son(T_JAUNE + 0.3, "ding", -11)
son(T_COMM - 0.12, "swipe", -10)
for i in range(14): son(T_COMMENT + i * 0.04, "frappe", -18)
son(T_CHERCHE - 0.1, "pop", -11); son(T_REPONDS - 0.2, "whoosh_court", -10); son(T_REPONDS + 0.1, "message_in", -9); son(T_LA, "check", -8)
sons_signature(son, T_FIN)
for a, b in [(0.0, 0.25), (T_UNE1 - 0.1, T_UNE1 + 0.15), (T_UNE2 - 0.1, T_UNE2 + 0.15), (T_UNE3 - 0.1, T_UNE3 + 0.15),
             (T_PHOTO - 0.05, T_PHOTO + 0.15), (T_ABO - 0.15, T_ABO + 0.2), (T_ON - 0.12, T_ON + 0.2), (T_MONT - 0.12, T_MONT + 0.2),
             (T_TU - 0.2, T_TU + 0.3), (T_REGARDE - 0.12, T_REGARDE + 0.25), (T_COMME - 0.2, T_COMME + 0.2), (T_SELON - 0.12, T_SELON + 0.2), (T_HUIT - 0.12, T_HUIT + 0.25), (T_UNITE - 0.12, T_UNITE + 0.2),
             (T_QTE - 0.2, T_QTE + 0.2), (T_SAVE - 0.12, T_SAVE + 0.2), (T_COMM - 0.12, T_COMM + 0.2), (T_FIN + 0.4, T_FIN + 0.75)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_UNE1 + 0.12, "#FFFFFF", 0.22), (T_UNE2 + 0.12, "#FFFFFF", 0.22), (T_UNE3 + 0.12, "#FFFFFF", 0.22),
                    (T_PHOTO, "#FFFFFF", 0.3), (T_GZ - 0.1, "#FFFFFF", 0.16), (T_VALID, GLACIER, 0.1), (T_LIVR, "#FFFFFF", 0.14),
                    (T_VIDEO + 0.05, "#FFFFFF", 0.18), (T_LA, VERT_, 0.1)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    _T[0] = t
    fond_studio(c, t, battement(t, T_PHOTO, 1, 0.5) - 1)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_abo(c, t); scene_place(c, t); scene_cats(c, t); scene_influ(c, t); scene_qualites(c, t); scene_livraison(c, t); scene_quantite(c, t); scene_save(c, t)
    scene_fin(c, t)
    filigrane(c, t)
    signature(c, t, T_FIN, MELANGE[:6], LOGO, CX, 880, accent=GLACIER, encre=ENCRE)
    K.dessine_eclairs(c, t)
    if t < T_FIN - 0.1 and not (P0 + 0.3 < t < P1 - 0.25): SOUS.dessine(c, t, ENCRE)   # muets pendant que Le mzé parle
