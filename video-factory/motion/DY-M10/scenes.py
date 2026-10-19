"""DY-M10 « La photo » (v2 du 17/10 : « plusieurs qualités, selon les produits », plus de standard / 1:1 / originale) — DROP&YOU, sujet de DY-M02 (on est sur place en Chine) au style CB-M15 (cobalt, débit validé),
en 3D (17/10/2026). Hook : un chat dans un téléphone en volume, la photo d'une veste part (« Envoie-nous juste la photo »),
jaillit de l'écran et se retourne : la vraie pièce, TROUVÉE (« On la trouve pour toi, en Chine »).
Corps commun : moteur/dy3d.py. Logo DROP&YOU en filigrane tout du long."""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from dy3d import *
import agence

K = Kit(P, 1.0)
DUREE = round(K.timing["mots"][-1]["t1"] + 1.8, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
I = lambda mot, apres=0: trouve(K, mot, apres)

M = dict(dy=TW(I("chez")), place=TW(I("place")), cat0=TW(I("vestes")),
         items=[("veste", TW(I("vestes"))), ("doudoune", TW(I("doudounes"))), ("casque", TW(I("casques"))), ("moto", TW(I("motos")))],
         catalogue=TW(I("catalogue")), tel=TW(I("telephone")), qual0=TW(I("et", 40)),
         q=[TW(I("plusieurs")), TW(I("qualites")), TW(I("choix"))],
         quals=[("Veste", "", "veste"), ("Casque", "", "casque"), ("Moto", "", "moto")],
         titre_qual=("SELON LE PRODUIT", "PLUSIEURS QUALITÉS"), t_titre2=TW(I("plusieurs")),
         livr=TW(I("prix") - 1), jours=TW(I("huit")),
         fr=TW(I("france")), be=TW(I("belgique")), partout=TW(I("partout")), unite=TW(I("une", 65)), quant=TW(I("cartons")),
         revendre=TW(I("revendre")), deux=TW(I("deux", 80)), paie=TW(I("paypal")), vir=TW(I("virement")), carte=TW(I("carte")),
         ecris=TW(I("ecrisnous")), snap=TW(I("snap")), dy1=TW(I("drop", 90)), wa=TW(I("whatsapp")))
SOUS = SousTitresEncre(K, fusions={(I("drop", 90), I("drop", 90) + 1, I("drop", 90) + 2, I("drop", 90) + 3): "DropandYou1,"},
                       y=1440, larg=900, taille=54, fam="gras", max_mots=5)
T_PIECE, T_ENV, T_PHOTO, T_TROUVE, T_CHINE, T_B1 = TW(4), TW(8), TW(11), TW(14), TW(18), M["dy"]
VESTE = PRODUITS["veste2"]


def ecran_chat(t):
    envoi = prog(t, T_ENV - 0.1, 0.4, sortieExpo)
    rep = entre(t, T_TROUVE + 0.1, 0.4, 2.0)
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#0B1240"))
        c.drawRect(skia.Rect.MakeWH(w, 110 * k), peinture("#13299A"))
        disque(c, 52 * k, 70 * k, 26 * k, ORANGE)
        texte(c, "DROP&YOU", 92 * k, 54 * k, 26 * k, BLANC, "noir", track=0.02)
        texte(c, "en ligne", 92 * k, 84 * k, 18 * k, "#9FB2FF", "demi", track=0)
        rrect(c, 24 * k, 140 * k, 290 * k, 70 * k, 22 * k, "#FFFFFF", 0.12)
        texte(c, "Salut, vous trouvez ça ?", 42 * k, 162 * k, 22 * k, BLANC, "demi", track=0)
        if envoi > 0:
            y = mix(h, 240 * k, envoi)
            rrect(c, w - 300 * k, y, 276 * k, 300 * k, 26 * k, ORANGE)
            rrect(c, w - 288 * k, y + 12 * k, 252 * k, 276 * k, 20 * k, "#EEF0F6")
            if t < T_PHOTO:
                iw, ih = taille_img(VESTE); s = 220 * k / ih
                image(c, VESTE, w - 162 * k - iw * s / 2, y + 40 * k, iw * s)
            else:
                icone(c, "image", w - 162 * k, y + 150 * k, 70 * k, "#B8BCC8", 2)
        if rep > 0:
            with Calque(c, borne(rep * 3)):
                rrect(c, 24 * k, 580 * k, 300 * k, 70 * k, 22 * k, "#FFFFFF", 0.14)
                texte(c, "On s'en occupe !", 42 * k, 602 * k, 22 * k, BLANC, "fort", track=0)
        rrect(c, 20 * k, h - 90 * k, w - 40 * k, 60 * k, 30 * k, "#FFFFFF", 0.1)
    return f


def hook(c, t):
    a = prog(t, -0.05, 0.6, lambda v: ressort(v, 1.3, 4.8))
    sort = prog(t, T_PHOTO - 0.1, 0.6, lambda v: ressort(v, 1.2, 4.6)) if t > T_PHOTO - 0.1 else 0
    flip = prog(t, T_TROUVE - 0.15, 0.55, lambda v: ressort(v, 1.3, 5)) if t > T_TROUVE - 0.15 else 0
    cam = Cam(ax=-6 + 3 * math.sin(t), ay=mix(-45, -16, min(a, 1.1)) + 5 * math.sin(t * 0.8) + 14 * sort, tz=mix(520, 120, min(a, 1.1)) + 260 * sort, cy=1000)
    lueur(c, 540, 960, 600, ORANGE, 0.12 + 0.2 * flip)
    plans = [Plan(coins((0, 40, 0), 440, 900), 440, 900, tel(ecran_chat(t)), 1 - 0.45 * sort)]
    if sort > 0:
        # la photo sort de l'écran, vient vers nous, puis se retourne : la vraie pièce
        cen = (mix(80, 0, min(sort, 1.05)), mix(-40, 120, min(sort, 1.0)) + 14 * math.sin(t * 2), mix(-20, -520, min(sort, 1.05)))
        W_, H_ = 480, 520
        def photo(cc, w, h):
            rrect(cc, 0, 0, w, h, 34, ORANGE)
            rrect(cc, 14, 14, w - 28, h - 28, 26, "#EEF0F6")
            iw, ih = taille_img(VESTE); s = (h - 80) / ih
            image(cc, VESTE, w / 2 - iw * s / 2, 40, iw * s)
        f, r = plan_produit(VESTE)
        ang = 180 * min(flip, 1.03)
        plans.append(Plan(coins(cen, W_, H_, ay=ang + 8 * math.sin(t * 1.3)), W_, H_, photo))
        plans.append(Plan(coins(cen, W_, H_, ay=ang + 180 + 8 * math.sin(t * 1.3)), W_, H_, f))
    scene3d(c, cam, plans)
    if flip > 0.6:
        X, Y, _ = cam.proj((0, 120, -520))
        tampon_n(c, "TROUVÉE", X + 190, Y + 200, t, T_TROUVE + 0.25, ORANGE, -10, 56)
        eclats(c, X, Y, t, T_TROUVE + 0.2, 16, 560, [ORANGE, BLANC, ORANGE2], graine=6)
        puce(c, "En Chine", 540, 1290, entre(t, T_CHINE - 0.1, 0.4, 2.2), "map-pin", ORANGE, 40)
    # titres
    titre(c, t, "T'AS VU UNE PIÈCE", "QUI TE PLAÎT ?", -0.25, T_ENV - 0.1, y=400, t2=TW(5))
    titre(c, t, "ENVOIE-NOUS", "JUSTE LA PHOTO", T_ENV, T_TROUVE - 0.1, y=400, t2=TW(10))
    titre(c, t, "ON LA TROUVE", "POUR TOI", T_TROUVE, T_B1 + 0.2, y=400, t2=TW(15))


son(0.0, "whoosh_bas", -8); son(0.3, "impact", -5); son(0.05, "pop", -11); son(TW(5) - 0.05, "pop", -11)
son(T_ENV - 0.1, "swipe", -9); son(T_ENV + 0.1, "message_in", -7)
son(T_PHOTO - 0.1, "whoosh", -8); son(T_PHOTO + 0.3, "impact_doux", -8)
son(T_TROUVE - 0.15, "whoosh_court", -9); son(T_TROUVE + 0.1, "message_in", -11); son(T_TROUVE + 0.25, "tampon", -6); son(T_TROUVE + 0.28, "ching", -9)
son(T_CHINE - 0.1, "pop", -10)
sons_corps(K, M, DUREE)
for a, b in [(0.12, 0.4), (T_PHOTO - 0.1, T_PHOTO + 0.4), (T_TROUVE - 0.15, T_TROUVE + 0.35), (T_B1 - 0.35, T_B1 + 0.1)]: rapide(a, b)
for tt, cc_, a_ in [(T_TROUVE + 0.25, ORANGE, 0.12), (DUREE - 1.3, "#FFFFFF", 0.14)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    agence.T_COURANT[0] = t
    compose(c, t, M, hook, T_B1, SOUS, K, DUREE, pulse=battement(t, T_TROUVE + 0.25, 1, 0.6) - 1)
