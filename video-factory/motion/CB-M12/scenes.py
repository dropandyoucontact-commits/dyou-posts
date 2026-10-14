"""CB-M12 « Les 5 messages à envoyer avant de payer » — organique ChinaBook / DROP&YOU (14/10/2026).

Cinq messages WeChat à envoyer à un fournisseur avant de payer : vidéo du produit, prix par quantité, échantillon,
livraison chez ton transitaire à ton nom, vidéo du carton avant l'envoi. Discours ChinaBook : fournisseurs validés à
Guangzhou et à Shenzhen, jamais « usine ». Aucun prix chiffré. Règles : « enregistre » dans le hook, partage ciblé,
boucle ouverte (le 5 sous cadenas), fond sombre violet, Tomy à 4 mots/s, ChinaBook violet « par DROP&YOU » à la fin.
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence
from studio import lettres, Groupe, eclats, rayons, curseur, entre, SousTitresEncre

K = Kit(P, 1.0)
DUREE = round(K.timing["duree_voix"] + 1.6, 2)
K.duree = DUREE; K.nb_images = round(DUREE * FPS)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

JAUNE, ROUGE, VERT, BLANC = "#FFD43B", "#FF4D5E", "#2BD67B", "#FFFFFF"
V, VC = A["violet"], A["violetClair"]
CLAIR = [BLANC, "#E6DCFF"]
WXV = WX["vert"]

SOUS = SousTitresEncre(K, fusions={(65,): "10", (71,): "50 ? »", (197, 198): "ChinaBook,", (200, 201, 202): "DROP&YOU."},
                       y=1410, larg=900, taille=54, fam="gras", max_mots=5)

# ─────────────────────────────────────────── temps des parties
T_STOP = TW(7)                      # « Ne paie rien »
T_CINQ = TW(15)                     # « ces cinq messages »
T_ENR = TW(18)                      # « Enregistre cette vidéo »
T_RESTE = TW(28) - 0.1              # « Et le cinquième… »
ETAPES = [TW(39), TW(57), TW(87), TW(118), TW(136)]
T_PARTAGE = TW(107)
FINS = [TW(57), TW(87), TW(107), TW(136), TW(165)]
T_COM = TW(165) - 0.1
T_FIN = TW(173) - 0.1               # « Et si tu veux des fournisseurs… »
T_CB = TW(197) - 0.1                # logo ChinaBook (le sous-titre se tait)
# chaque message : (début, fin) de la citation dite par la voix
CITATIONS = [(TW(40), TW(45) + 0.4), (TW(58), TW(71) + 0.4), (TW(88), TW(92) + 0.5), (TW(119), TW(127) + 0.3), (TW(137), TW(145) + 0.4)]
MESSAGES = ["Envoie-moi une vidéo du produit, maintenant.",
            "C'est quoi ton prix à partir de 10 pièces ? Et à partir de 50 ?",
            "Tu peux m'envoyer un échantillon ?",
            "Tu peux livrer chez mon transitaire, à mon nom ?",
            "Avant l'envoi, filme-moi le carton avec ma commande dedans."]
TITRES = ["UNE VIDÉO", "LE PRIX EN GROS", "UN ÉCHANTILLON", "À TON NOM", "FILME LE CARTON"]


def etape_active(t):
    k = -1
    for i, t0 in enumerate(ETAPES):
        if t >= t0 - 0.12: k = i
    return k


# ─────────────────────────────────────────── briques
def entete_marque(c, t):
    iw, ih = taille_img("logo-dy-blanc"); lw = 230
    image(c, "logo-dy-blanc", 70, 300 - lw * ih / iw / 2, lw, 0.95)


RAIL_X = [720 + k * 70 for k in range(5)]
RAIL_Y = 300


def rail(c, t):
    if t < ETAPES[0] - 0.5 or t > T_FIN + 0.5: return
    a = entre(t, ETAPES[0] - 0.5, 0.5, 1.4) * (1 - prog(t, T_FIN, 0.3))
    k_act = etape_active(t)
    with Calque(c, borne(a * 3)):
        trait(c, RAIL_X[0], RAIL_Y, RAIL_X[-1], RAIL_Y, BLANC, 4, 0.18)
        if k_act > 0:
            u = prog(t, ETAPES[k_act] - 0.12, 0.35, sortie)
            trait(c, RAIL_X[0], RAIL_Y, mix(RAIL_X[k_act - 1], RAIL_X[k_act], u), RAIL_Y, JAUNE, 5)
        for k, x in enumerate(RAIL_X):
            c.save(); c.translate(x, RAIL_Y)
            actif, fait = k == k_act, k < k_act
            s = 1.0 + 0.28 * (prog(t, ETAPES[k] - 0.12, 0.3, lambda v: rebond(v, 2)) if actif else 0)
            c.scale(s, s)
            if k == 4 and t < ETAPES[4] - 0.12:
                lueur(c, 0, 0, 60, JAUNE, 0.35 + 0.2 * math.sin(t * 5))
                disque(c, 0, 0, 26, "#2A2040"); anneau(c, 0, 0, 26, JAUNE, 3); icone(c, "lock", 0, 0, 26, JAUNE, 2.6)
            elif actif:
                lueur(c, 0, 0, 60, JAUNE, 0.45); disque(c, 0, 0, 27, JAUNE)
                texte(c, str(k + 1), 0, -hauteurLigne(30) / 2, 30, "#1A1030", "noir", "centre", 0)
            elif fait:
                disque(c, 0, 0, 24, V); icone(c, "check", 0, 0, 28, BLANC, 3)
            else:
                disque(c, 0, 0, 22, BLANC, 0.08); anneau(c, 0, 0, 22, BLANC, 2, 0.35)
                texte(c, str(k + 1), 0, -hauteurLigne(24) / 2, 24, BLANC, "noir", "centre", 0, alpha=0.6)
            c.restore()
    eclats(c, RAIL_X[4], RAIL_Y, t, ETAPES[4] - 0.05, 12, 200, [JAUNE, BLANC, VC], graine=9)


def entete(c, t, n, titre, t0):
    a = entre(t, t0 - 0.12, 0.45, 2.0)
    if a > 0:
        c.save(); c.translate(150, 470); c.rotate(-8 * (1 - a)); c.scale(mix(2.4, 1, a), mix(2.4, 1, a))
        lueur(c, 0, 0, 120, JAUNE, 0.35); disque(c, 0, 0, 62, JAUNE)
        texte(c, str(n), 0, -hauteurLigne(78) / 2, 78, "#1A1030", "noir", "centre", -0.02)
        c.restore()
    taille = ajuste(titre, 760, 92, "noir", -0.03)
    lettres(c, titre, 240, 470 - taille * 0.62, taille, t, t0 - 0.05, "masque", decal=0.025, duree=0.4, align="gauche", grad=True, cols=CLAIR)


def coupe(txt, taille, wmax, fam="moyen"):
    lignes, cur = [], ""
    for m in txt.split(" "):
        essai = (cur + " " + m).strip()
        if largeur(essai, taille, fam, 0) > wmax and cur: lignes.append(cur); cur = m
        else: cur = essai
    lignes.append(cur)
    return lignes


def message_vert(c, t, k, y=600):
    """le message à recopier : grosse bulle verte WeChat tapée au rythme de la voix, avatar à droite"""
    t0, t1 = CITATIONS[k]
    a = entre(t, t0 - 0.25, 0.4, 1.8)
    if a <= 0: return 0
    txt = MESSAGES[k]
    taille = 44
    lignes = coupe(txt, taille, 700)
    hl = int(taille * 1.3)
    wb = max(largeur(l, taille, "moyen", 0) for l in lignes) + 64
    hb = len(lignes) * hl + 44
    xb = 1080 - 70 - 110 - wb
    n = int(borne((t - t0) / max(0.3, t1 - t0)) * len(txt) + 0.999)
    c.save(); c.translate(xb + wb, y); c.scale(mix(0.5, 1, a), mix(0.5, 1, a)); c.translate(-(xb + wb), -y)
    with Calque(c, borne(a * 3)):
        rrect(c, 1080 - 70 - 90, y, 90, 90, 14, "#CFE8D9"); icone(c, "user", 1080 - 70 - 45, y + 45, 50, "#2E7D52", 2.2)
        rrect(c, xb, y, wb, hb, 22, WXV, 1.0, (10, 30, 0.35))
        pq = skia.Path(); pq.moveTo(xb + wb - 1, y + 30); pq.lineTo(xb + wb + 16, y + 44); pq.lineTo(xb + wb - 1, y + 58); pq.close()
        c.drawPath(pq, peinture(WXV))
        reste = n
        for j, l in enumerate(lignes):
            vis = l[:max(0, reste)]; reste -= len(l) + 1
            texte(c, vis, xb + 32, y + 22 + j * hl, taille, WX["texte"], "moyen", track=0)
            if 0 < len(vis) < len(l) and int(t * 6) % 2 == 0:
                rrect(c, xb + 34 + largeur(vis, taille, "moyen", 0), y + 26 + j * hl, 4, taille * 1.05, 2, "#2E7D52")
        if t > t1:
            u = entre(t, t1, 0.3, 2.2)
            texte(c, "Envoyé", xb + wb - 8, y + hb + 10, 26, VC, "gras", "droite", 0, borne(u * 3))
    return y + hb


def reponse(c, t, t0, txt, x, y, taille=36):
    """réponse du fournisseur : bulle blanche WeChat à gauche, avec la mention « échange illustratif »"""
    a = entre(t, t0 - 0.1, 0.4, 2.0)
    if a <= 0: return
    wb = largeur(txt, taille, "moyen", 0) + 56; hb = taille * 1.3 + 36
    c.save(); c.translate(x, y); c.scale(mix(0.5, 1, a), mix(0.5, 1, a)); c.translate(-x, -y)
    with Calque(c, borne(a * 3)):
        rrect(c, x, y, 80, 80, 12, "#3E4A44"); icone(c, "store", x + 40, y + 40, 44, BLANC, 2.2)
        rrect(c, x + 100, y, wb, hb, 20, BLANC, 1.0, (8, 24, 0.3))
        pq = skia.Path(); pq.moveTo(x + 101, y + 26); pq.lineTo(x + 86, y + 40); pq.lineTo(x + 101, y + 54); pq.close()
        c.drawPath(pq, peinture(BLANC))
        texte(c, txt, x + 128, y + 18, taille, WX["texte"], "moyen", track=0)
        texte(c, "Échange illustratif", x + 100, y + hb + 8, 22, A["gris"], "gras", track=0)
    c.restore()


def tampon_c(c, label, cx, cy, t, t0, couleur=JAUNE, rot=-9, taille=52):
    if t < t0 - 0.12: return
    u = prog(t, t0 - 0.12, 0.16, entree)
    s = mix(2.6, 1, u)
    tw = largeur(label, taille, "noir"); w, h = tw + taille * 1.2, taille * 1.9
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, u):
        rrect(c, -w / 2, -h / 2, w, h, 20, "#140C26", 0.85, None, couleur, 8)
        texte(c, label, 0, -hauteurLigne(taille) / 2, taille, couleur, "noir", "centre", -0.01)
    c.restore()


def interdit(c, cx, cy, r, u):
    if u <= 0: return
    c.save(); c.translate(cx, cy); c.scale(mix(1.6, 1, u), mix(1.6, 1, u))
    with Calque(c, borne(u * 3)):
        anneau(c, 0, 0, r, ROUGE, 14); trait(c, -r * 0.7, -r * 0.7, r * 0.7, r * 0.7, ROUGE, 14)
    c.restore()


def carte(c, cx, cy, w, h, r=40, violet=0.0, alpha=1.0, s=1.0):
    if alpha <= 0.01 or s <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        verre(c, -w / 2, -h / 2, w, h, r, 0.08, violet=violet)
    c.restore()


def signet(c, cx, cy, taille, plein):
    k = taille / 100
    pth = skia.Path(); pth.moveTo(cx - 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy + 50 * k)
    pth.lineTo(cx, cy + 24 * k); pth.lineTo(cx - 36 * k, cy + 50 * k); pth.close()
    if plein > 0:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(cx - 60 * k, cy + 52 * k - 104 * k * plein, 120 * k, 104 * k * plein))
        c.drawPath(pth, peinture(JAUNE)); c.restore()
    c.drawPath(pth, peinture(BLANC, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=7 * k, StrokeJoin=skia.Paint.kRound_Join))


def tel_video(c, nom, cx, cy, w, h, t, t0, a, vitesse=2.0, rec=False):
    if a <= 0: return
    with Espace(c, cx, cy, ry=mix(-30, -8, a) + 3 * math.sin(t * 1.5), rx=4, s=mix(0.6, 1, a)):
        def ecran(cc, x, y, ww, hh):
            video(cc, nom, x, y, ww, hh, t - t0, vitesse)
            if rec:
                disque(cc, x + 50, y + 70, 12, ROUGE, 0.6 + 0.4 * (int(t * 3) % 2))
                texte(cc, "REC", x + 72, y + 56, 26, BLANC, "noir", track=0.04)
        telephone_sombre(c, cx, cy, w, h, ecran, borne(a * 3))


# ─────────────────────────────────────────── HOOK
def hook(c, t):
    if t > ETAPES[0] + 0.3: return
    fin = prog(t, ETAPES[0] - 0.3, 0.35, entree)
    with Calque(c, 1 - fin):
        part = prog(t, T_RESTE, 0.45, entreeSortie)
        lettres(c, "TU AS TROUVÉ", 540, 380 - 160 * part, 112, t, -0.7, "ressort", grad=False, couleur=BLANC, decal=0.035, alpha=1 - part)
        lettres(c, "UN FOURNISSEUR ?", 540, 505 - 160 * part, 104, t, -0.55, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.035, alpha=1 - part)
        # le téléphone : le fournisseur envoie déjà son QR Alipay
        if part < 0.99:
            gl = prog(t, T_ENR - 0.3, 0.45, entreeSortie)
            cx, cy = mix(540, 380, gl), 1020 + 700 * part ** 2
            sx, sy = secousse(t, T_STOP, 14)
            msgs = [dict(t=-1, type="texte", texte="Bonjour, ma commande ?", moi=True),
                    dict(t=-1, type="qr", legende="Scanne pour payer")]
            with Espace(c, cx + sx, cy + sy, ry=-10 + 4 * math.sin(t * 1.4), rx=3, s=1.0):
                telephone_sombre(c, cx + sx, cy + sy, 330, 680, lambda cc, x, y, w, h: ecran_wechat(cc, x, y, w, h, t, "Fournisseur", msgs), 1 - part)
            # « Ne paie rien »
            st = prog(t, T_STOP - 0.1, 0.25, sortie)
            if st > 0:
                interdit(c, cx + sx, cy + 60 + sy, 170, st * (1 - part))
                with Calque(c, 1 - part):
                    tampon_c(c, "NE PAIE RIEN", cx, cy + 300, t, TW(9), ROUGE, -7, 54)
            # « ces cinq messages » : cinq bulles vertes qui sortent du téléphone
            for k in range(5):
                u = entre(t, T_CINQ + 0.06 * k, 0.4, 1.8) * (1 - gl)
                if u <= 0: continue
                ang = -math.pi * (0.85 - 0.175 * k)
                bx, by = cx + 300 * math.cos(ang) * u, cy - 180 + 230 * math.sin(ang) * u
                c.save(); c.translate(bx, by); c.scale(u, u)
                rrect(c, -48, -36, 96, 72, 18, WXV, 1.0, (8, 20, 0.3))
                texte(c, str(k + 1), 0, -hauteurLigne(40) / 2, 40, "#1A1030", "noir", "centre", 0)
                c.restore()
        # « Enregistre » : le signet
        a = entre(t, T_ENR - 0.15, 0.4, 2.2)
        if a > 0 and part < 1:
            t_clic = T_ENR + 0.35
            plein = prog(t, t_clic, 0.3, sortie)
            cx, cy = 820, 980 + 400 * part
            b = mix(0.3, 1, a) * battement(t, t_clic, 0.2, 0.3)
            c.save(); c.translate(cx, cy); c.scale(b, b)
            lueur(c, 0, 0, 170, JAUNE, 0.25 + 0.35 * plein)
            disque(c, 0, 0, 100, "#1A1030", 0.85); anneau(c, 0, 0, 100, JAUNE if plein > 0.5 else BLANC, 4, 0.8)
            signet(c, 0, 0, 115, plein)
            c.restore()
            if plein > 0:
                pl = prog(t, t_clic, 0.8, sortie)
                texte(c, "+1", cx + 140, cy - 110 - 60 * pl, 52, JAUNE, "noir", "centre", 0, alpha=1 - max(0, pl - 0.6) / 0.4)
            pa = prog(t, t_clic - 0.4, 0.38, sortie)
            if t < t_clic + 0.6:
                curseur(c, mix(1000, cx + 10, pa), mix(1500, cy + 20, pa), 1.3, 1 - prog(t, t_clic + 0.3, 0.3),
                        prog(t, t_clic - 0.05, 0.05) * (1 - prog(t, t_clic + 0.05, 0.1)))
            eclats(c, cx, cy, t, t_clic, 14, 260, [JAUNE, BLANC, VC], graine=3)
            r = entre(t, TW(24) - 0.1, 0.4, 2.2)
            if r > 0: pastille_verre(c, "À recopier", 820, 1180 + 400 * part, 40, "copy", borne(r * 3) * (1 - part), mix(0.4, 1, r), accent="#B8901A", rot=4)
        # « le cinquième » : le 5 sous cadenas, puis il file dans le rail
        a5 = entre(t, TW(30) - 0.1, 0.5, 1.6)
        if a5 > 0:
            vol = prog(t, ETAPES[0] - 0.6, 0.45, entreeSortie)
            cx, cy = mix(540, RAIL_X[4], vol), mix(880, RAIL_Y, vol)
            s = mix(0.4, 1, a5) * mix(1, 26 / 150, vol)
            c.save(); c.translate(cx, cy); c.scale(s, s)
            lueur(c, 0, 0, 330, JAUNE, 0.3 + 0.1 * math.sin(t * 6))
            rayons(c, 0, 0, t, 520, 0.12 * (1 - vol), 12, JAUNE)
            disque(c, 0, 0, 150, "#2A2040"); anneau(c, 0, 0, 150, JAUNE, 10)
            texte(c, "5", -6, -hauteurLigne(190) / 2, 190, JAUNE, "noir", "centre", -0.02)
            c.save(); c.translate(92, 92); disque(c, 0, 0, 52, JAUNE); icone(c, "lock", 0, 0, 56, "#1A1030", 2.8); c.restore()
            c.restore()
            if vol < 0.2:
                ep = entre(t, TW(36) - 0.1, 0.4, 2.2)
                if ep > 0:
                    with Calque(c, borne(a5 * 3) * (1 - vol * 5)):
                        pastille_verre(c, "Ta commande protégée", 540, 1150, 42, "shield-check", borne(ep * 3), mix(0.4, 1, ep), accent=VERT)


# ─────────────────────────────────────────── 1 · une vidéo, maintenant
def etape1(c, t):
    g = Groupe(c, t, ETAPES[0] - 0.4, FINS[0], ent="grand", sor="gauche")
    if not g.visible: return
    with g:
        entete(c, t, 1, TITRES[0], ETAPES[0] - 0.2)
        message_vert(c, t, 0)
        # photo de catalogue (barrée) / vidéo dans sa main
        a = entre(t, TW(46) - 0.15, 0.45, 1.8)
        if a > 0:
            carte(c, 270, 1050, 340, 360, 36, alpha=borne(a * 3), s=mix(0.5, 1, a))
            with Calque(c, borne(a * 3) * (1 - 0.45 * prog(t, TW(50), 0.2))):
                rrect(c, 140, 900, 260, 200, 18, BLANC, 0.1)
                icone(c, "image", 270, 1000, 110, BLANC, 2.0)
                texte(c, "Catalogue", 270, 1140, 34, BLANC, "gras", "centre", -0.01)
            interdit(c, 270, 1030, 140, prog(t, TW(50) - 0.05, 0.25, sortie))
        b = entre(t, TW(42) - 0.15, 0.5, 1.6)
        tel_video(c, "videos/chaussures/baskets-stock-1", 760, 1060, 270, 540, t, TW(42), b, 2.2)
        d = entre(t, TW(56) - 0.1, 0.4, 2.2)
        if d > 0: pastille_verre(c, "Aujourd'hui", 760, 760, 36, "check", borne(d * 3), mix(0.4, 1, d), accent=VERT, rot=4)


# ─────────────────────────────────────────── 2 · le prix par quantité
def etape2(c, t):
    g = Groupe(c, t, FINS[0] - 0.12, FINS[1], ent="droite", sor="zoom")
    if not g.visible: return
    with g:
        entete(c, t, 2, TITRES[1], ETAPES[1])
        bas = message_vert(c, t, 1)
        a = entre(t, TW(64) - 0.15, 0.45, 1.8)
        if a > 0:
            carte(c, 540, 1110, 860, 360, 40, violet=0.15, alpha=borne(a * 3), s=mix(0.5, 1, a))
            with Calque(c, borne(a * 3)):
                texte(c, "Prix à la pièce", 150, 950, 30, A["gris"], "gras", track=0)
                for k, (lab, hmax, t0, col) in enumerate([("10 pièces", 200, TW(65), ROUGE), ("50 pièces", 110, TW(71), VERT)]):
                    u = prog(t, t0, 0.5, sortie)
                    x = 220 + k * 230
                    rrect(c, x, 1240 - hmax * u, 150, hmax * u, 16, col, 0.9)
                    texte(c, lab, x + 75, 1250, 28, BLANC, "gras", "centre", 0)
                    texte(c, "¥¥¥" if k == 0 else "¥", x + 75, 1240 - hmax * u - 48, 34, BLANC, "noir", "centre", 0, borne(u * 3))
                fl = prog(t, TW(74), 0.4, sortie)
                if fl > 0:
                    icone(c, "trending-down", 820, 1040, 120 * fl, VERT, 2.6)
                    texte(c, "Le prix baisse", 820, 1130, 30, BLANC, "gras", "centre", 0, borne(fl * 3))
        tampon_c(c, "DEMANDE-LE", 820, 900, t, TW(84) + 0.05, JAUNE, 8, 44)


# ─────────────────────────────────────────── 3 · l'échantillon
def etape3(c, t):
    g = Groupe(c, t, FINS[1] - 0.12, FINS[2], ent="bas", sor="haut")
    if not g.visible: return
    with g:
        entete(c, t, 3, TITRES[2], ETAPES[2])
        message_vert(c, t, 2)
        gros = prog(t, TW(103) - 0.2, 0.4, entreeSortie)
        a = entre(t, TW(91) - 0.1, 0.45, 1.8)
        if a > 0:
            cx = mix(540, 270, gros)
            carte(c, cx, 1060, 380, 380, 40, violet=0.2, alpha=borne(a * 3), s=mix(0.5, 1, a) * mix(1, 0.85, gros))
            with Calque(c, borne(a * 3)):
                sneaker(c, cx, 1030, 240 * mix(1, 0.85, gros), haut="#F2F2F7", accent=V)
                texte(c, "1 pièce", cx, 1170, 36, BLANC, "gras", "centre", -0.01)
            # la main qui touche
            m = entre(t, TW(99) - 0.15, 0.4, 2.0)
            if m > 0:
                c.save(); c.translate(cx + 120, mix(1200, 1090, m)); c.rotate(-20)
                icone(c, "hand", 0, 0, 100, JAUNE, 2.4, borne(m * 3))
                c.restore()
                ok = entre(t, TW(100), 0.35, 2.4)
                disque(c, cx + 140, 900, 40 * ok, VERT); icone(c, "check", cx + 140, 900, 46 * ok, BLANC, 3.2)
        if gros > 0:
            for k in range(6):
                u = entre(t, TW(104) + 0.07 * k, 0.4, 2.0)
                if u <= 0: continue
                x, y = 640 + (k % 3) * 140, 960 + (k // 3) * 130
                carton(c, x, mix(y - 200, y, u), 120, alpha=borne(u * 3), rot=(k % 2) * 6 - 3)
            gg = entre(t, TW(106) - 0.1, 0.4, 2.2)
            if gg > 0: pastille_verre(c, "En gros", 780, 1250, 38, "package", borne(gg * 3), mix(0.4, 1, gg), accent=V)


# ─────────────────────────────────────────── partage
def partage(c, t):
    g = Groupe(c, t, T_PARTAGE - 0.12, ETAPES[3], ent="zoom", sor="zoom")
    if not g.visible: return
    with g:
        lettres(c, "ENVOIE-LA", 540, 420, 120, t, T_PARTAGE - 0.05, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.035)
        a = entre(t, T_PARTAGE, 0.45, 1.8)
        if a > 0:
            b = mix(0.4, 1, a) * battement(t, T_PARTAGE + 0.5, 0.1, 0.3)
            c.save(); c.translate(540, 760); c.scale(b, b)
            lueur(c, 0, 0, 200, JAUNE, 0.35); disque(c, 0, 0, 110, JAUNE); icone(c, "share-2", -4, 0, 120, "#1A1030", 2.6)
            c.restore()
        for (lab, x, t0) in [("Toi", 250, TW(110)), ("Ton associé", 830, TW(113))]:
            b = entre(t, t0 - 0.1, 0.4, 2.2)
            if b > 0:
                c.save(); c.translate(x, 1120); c.scale(b, b)
                disque(c, 0, 0, 86, "#2A2040"); anneau(c, 0, 0, 86, VC, 4); icone(c, "user-round", 0, -6, 90, BLANC, 2.0)
                texte(c, lab, 0, 104, 34, BLANC, "gras", "centre", -0.01)
                c.restore()
        u = prog(t, TW(115) - 0.05, 0.6, entreeSortie)
        if u > 0:
            x = mix(250, 830, u); y = 1120 - 260 * math.sin(math.pi * u)
            c.save(); c.translate(x, y); c.rotate(-15 + 30 * u); c.scale(0.9, 0.9)
            rrect(c, -50, -80, 100, 160, 16, V, 1.0, (8, 20, 0.4)); icone(c, "play", 4, 0, 50, BLANC, 2.6)
            c.restore()
        if t > TW(115) + 0.55:
            ok = entre(t, TW(115) + 0.55, 0.35, 2.4)
            disque(c, 900, 1050, 34 * ok, VERT); icone(c, "check", 900, 1050, 40 * ok, BLANC, 3.2)


# ─────────────────────────────────────────── 4 · chez ton transitaire, à ton nom
def etape4(c, t):
    g = Groupe(c, t, ETAPES[3] - 0.12, FINS[3], ent="droite", sor="gauche")
    if not g.visible: return
    with g:
        entete(c, t, 4, TITRES[3], ETAPES[3])
        message_vert(c, t, 3)
        a = entre(t, TW(124) - 0.15, 0.45, 1.8)
        if a > 0:
            u = prog(t, TW(124), 0.8, entreeSortie)
            carton(c, mix(200, 470, u), 1060, 200, alpha=borne(a * 3), rot=-6 * (1 - u))
            # étiquette « à ton nom »
            e = entre(t, TW(126) - 0.05, 0.35, 2.4)
            if e > 0:
                c.save(); c.translate(mix(200, 470, u) - 20, 1080); c.rotate(-4); c.scale(e, e)
                rrect(c, -95, -32, 190, 64, 10, BLANC, 1.0, (6, 16, 0.3)); texte(c, "À TON NOM", 0, -hauteurLigne(30) / 2, 30, "#1A1030", "noir", "centre", 0)
                c.restore()
            n = entre(t, TW(124) + 0.2, 0.45, 1.8)
            c.save(); c.translate(790, 1060); c.scale(mix(0.3, 1, n), mix(0.3, 1, n))
            with Calque(c, borne(n * 3)):
                lueur(c, 0, 0, 160, VC, 0.3); verre(c, -110, -110, 220, 220, 110, 0.08, violet=0.2)
                icone(c, "warehouse", 0, -8, 110, BLANC, 2.0)
                texte(c, "Transitaire", 0, 128, 32, BLANC, "gras", "centre", -0.01)
            c.restore()
            trait(c, 320, 1060, mix(320, 670, u), 1060, JAUNE, 5, 0.6, pointille=[10, 10])
        reponse(c, t, TW(132) - 0.05, "Oui, pas de problème", 130, 830)
        tampon_c(c, "VRAI FOURNISSEUR", 540, 1270, t, TW(133) + 0.1, VERT, -5, 42)


# ─────────────────────────────────────────── 5 · filme-moi le carton
def etape5(c, t):
    if t < ETAPES[4] - 0.15: return
    g = Groupe(c, t, ETAPES[4] - 0.15, FINS[4], ent="zoom", sor="recul")
    if not g.visible: return
    with g:
        entete(c, t, 5, TITRES[4], ETAPES[4])
        message_vert(c, t, 4)
        b = entre(t, TW(139) - 0.1, 0.5, 1.6)
        tel_video(c, "videos/guangzhou/guangzhou-cartons-baskets-gros", 330, 1080, 280, 520, t, TW(139), b, 1.6, rec=True)
        o = entre(t, TW(146) - 0.1, 0.4, 2.2)
        if o > 0: pastille_verre(c, "Tu vois tout", 770, 900, 40, "eye", borne(o * 3), mix(0.4, 1, o), accent=V)
        p = entre(t, TW(154) - 0.1, 0.45, 2.0)
        if p > 0:
            c.save(); c.translate(770, 1110); c.scale(mix(0.4, 1, p), mix(0.4, 1, p))
            lueur(c, 0, 0, 170, VERT, 0.3); disque(c, 0, 0, 100, VERT)
            icone(c, "shield-check", 0, 0, 110, BLANC, 2.4)
            c.restore()
            texte(c, "Rien ne change", 770, 1230, 34, BLANC, "gras", "centre", -0.01, borne(p * 3))


# ─────────────────────────────────────────── commentaire, puis ChinaBook par DROP&YOU
def fin(c, t):
    if t < T_COM - 0.05: return
    sortie_com = prog(t, T_FIN - 0.1, 0.35, entreeSortie)
    cm = entre(t, T_COM, 0.45, 1.8)
    if cm > 0 and sortie_com < 1:
        with Calque(c, 1 - sortie_com):
            lettres(c, "DIS-MOI", 540, 560, 120, t, T_COM, "ressort", cols=[JAUNE, "#FFE98A"], decal=0.035)
            c.save(); c.translate(540, 900); c.scale(mix(0.5, 1, cm), mix(0.5, 1, cm))
            with Calque(c, borne(cm * 3)):
                verre(c, -420, -70, 840, 140, 70, 0.12)
                icone(c, "message-circle", -355, 0, 54, JAUNE, 2.4)
                rep = ["Quel message tu n'envoyais pas ?", "Le 5", "Le 2", "Le 3 !"]
                k = min(len(rep) - 1, int(max(0, t - T_COM - 0.5) / 0.45))
                mot = rep[k]
                n = len(mot) if k == 0 else int(borne((t - T_COM - 0.5 - 0.45 * k) / 0.2) * len(mot) + 0.999)
                tl = 38 if k == 0 else 54
                texte(c, mot[:n], -300, -hauteurLigne(tl, "gras") / 2, tl, A["gris"] if k == 0 else BLANC, "gras", track=-0.01)
            c.restore()
    if t < T_FIN - 0.1: return
    logo_t = prog(t, T_CB - 0.1, 0.4, entreeSortie)
    # des fournisseurs qui disent oui aux cinq
    with Calque(c, 1 - logo_t):
        lettres(c, "OUI AUX 5", 540, 470, 110, t, TW(176) - 0.1, "ressort", cols=[VERT, "#9FF5C4"], decal=0.035)
        for k in range(5):
            u = entre(t, TW(178) + 0.08 * k, 0.4, 2.2)
            if u <= 0: continue
            mv = prog(t, TW(185) - 0.3, 0.45, entreeSortie)
            x = mix(540 + (k - 2) * 200, 220 + k * 160, mv)
            c.save(); c.translate(x, mix(950, 700, mv)); c.scale(u * mix(1.45, 1, mv), u * mix(1.45, 1, mv))
            rrect(c, -56, -42, 112, 84, 20, WXV, 1.0, (8, 20, 0.3))
            texte(c, str(k + 1), -14, -hauteurLigne(40) / 2, 40, "#1A1030", "noir", "centre", 0)
            disque(c, 40, -36, 22, VERT); icone(c, "check", 40, -36, 26, BLANC, 3.2)
            c.restore()
        # les lieux : Guangzhou et Shenzhen (vraies photos)
        for k, (nom, lab, x, t0) in enumerate([("lieux/kinbo-devanture-guangzhou", "Guangzhou", 290, TW(186)),
                                                ("lieux/seg-electronics-market-shenzhen", "Shenzhen", 790, TW(190))]):
            u = entre(t, t0 - 0.2, 0.5, 1.6)
            if u <= 0: continue
            c.save(); c.translate(x, 1060); c.rotate((-4 if k == 0 else 4) * (1 - 0.3 * u)); c.scale(mix(0.5, 1, u), mix(0.5, 1, u))
            with Calque(c, borne(u * 3)):
                rrect(c, -210, -200, 420, 400, 30, BLANC, 1.0, (16, 40, 0.45))
                image_cover(c, nom, -196, -186, 392, 300, zoom=1.0 + 0.05 * (t - t0), rayon=20)
                icone(c, "map-pin", -150, 158, 40, ROUGE, 2.4)
                texte(c, lab, -118, 138, 40, "#1A1030", "noir", track=-0.02)
            c.restore()
        va = entre(t, TW(188) - 0.1, 0.4, 2.2)
        if va > 0: pastille_verre(c, "Validés", 540, 860, 40, "badge-check", borne(va * 3), mix(0.4, 1, va), accent=VERT)
    if logo_t > 0:
        ul = entre(t, T_CB + 0.1, 0.5, 1.5)
        lueur(c, 540, 860, 600 * logo_t, "#6E48F0", 0.45)
        rayons(c, 540, 860, t, 900, 0.10 * logo_t, 14, "#9B83FF")
        iw, ih = taille_img("logo-chinabook-blanc"); lw = 820 * mix(0.6, 1, ul)
        image(c, "logo-chinabook-blanc", 540 - lw / 2, 830 - lw * ih / iw / 2, lw, borne(ul * 3))
        up = entre(t, TW(199) - 0.1, 0.45, 1.8)
        if up > 0:
            texte(c, "par", 540, 990, 36, A["gris"], "gras", "centre", 0, borne(up * 3))
            iw, ih = taille_img("logo-dy-blanc"); lw2 = 440 * mix(0.6, 1, up)
            image(c, "logo-dy-blanc", 540 - lw2 / 2, 1060, lw2, borne(up * 3))


# ─────────────────────────────────────────── sons
son(0.0, "impact", -4); son(0.0, "whoosh_court", -9); son(0.05, "message_in", -10)
son(T_STOP - 0.1, "impact", -5); son(T_STOP, "croc", -8); son(TW(9) - 0.07, "tampon", -5)
for k in range(5): son(T_CINQ + 0.06 * k, "pop", -12)
son(T_ENR - 0.3, "whoosh_court", -11); son(T_ENR - 0.15, "pop", -9); son(T_ENR + 0.35, "clic", -5); son(T_ENR + 0.38, "ching", -8); son(T_ENR + 0.4, "check", -9)
son(TW(24) - 0.1, "pop", -10)
son(T_RESTE, "whoosh_bas", -9); son(TW(30) - 0.1, "impact_doux", -6); son(TW(30), "montee", -12); son(TW(36) - 0.1, "pop", -10)
son(ETAPES[0] - 0.6, "whoosh_long", -9)
for k, t0 in enumerate(ETAPES):
    son(t0 - 0.15, "whoosh" if k % 2 == 0 else "whoosh_bas", -7); son(t0 - 0.05, "impact_doux", -8); son(t0, "pop", -10)
for (t0, t1) in CITATIONS:
    son(t0 - 0.25, "message", -10)
    n = int((t1 - t0) / 0.11)
    for j in range(n): son(t0 + 0.11 * j, "frappe", -19)
    son(t1, "message_in", -11)
son(TW(46) - 0.15, "verre", -10); son(TW(50) - 0.05, "impact", -7); son(TW(42) - 0.15, "whoosh", -10); son(TW(56) - 0.1, "check", -9)
son(TW(64) - 0.15, "verre", -10); son(TW(65), "montee", -14); son(TW(71), "montee", -14); son(TW(74), "blip", -10); son(TW(84) - 0.07, "tampon", -6)
son(TW(91) - 0.1, "pop", -10); son(TW(99) - 0.15, "swipe", -10); son(TW(100), "check", -9)
for k in range(6): son(TW(104) + 0.07 * k, "pop", -14)
son(TW(106) - 0.1, "pop", -11)
son(T_PARTAGE - 0.1, "whoosh_bas", -7); son(T_PARTAGE + 0.5, "impact_doux", -9)
son(TW(110) - 0.1, "pop", -10); son(TW(113) - 0.1, "pop", -10); son(TW(115) - 0.05, "whoosh_court", -9); son(TW(115) + 0.55, "message_in", -8)
son(TW(124) - 0.15, "whoosh", -10); son(TW(126) - 0.05, "pop", -10); son(TW(124) + 0.2, "verre", -10)
son(TW(132) - 0.05, "message_in", -8); son(TW(133) + 0.03, "tampon", -5); son(TW(133) + 0.06, "ching", -10)
son(TW(139) - 0.1, "whoosh", -10); son(TW(139), "blip", -12); son(TW(146) - 0.1, "pop", -10); son(TW(154) - 0.1, "impact_doux", -7); son(TW(154), "check", -9)
son(T_COM, "message", -9)
for k in range(1, 4):
    for j in range(3): son(T_COM + 0.5 + 0.45 * k + 0.05 * j, "frappe", -17)
son(T_FIN - 0.1, "whoosh", -9)
for k in range(5): son(TW(178) + 0.08 * k, "pop", -13)
son(TW(176) - 0.1, "ching", -9); son(TW(188) - 0.1, "check", -10)
son(TW(186) - 0.2, "whoosh_court", -10); son(TW(190) - 0.2, "whoosh_court", -10)
son(T_CB - 0.1, "montee", -11); son(T_CB + 0.1, "impact", -5); son(T_CB + 0.12, "verre", -9); son(TW(199) - 0.1, "pop", -9)

for a, b in [(0.0, 0.25), (T_STOP - 0.1, T_STOP + 0.2), (ETAPES[0] - 0.75, ETAPES[0] + 0.3), (T_PARTAGE - 0.2, T_PARTAGE + 0.3),
             (T_FIN - 0.1, T_FIN + 0.3), (T_CB - 0.1, T_CB + 0.4)] + [(t0 - 0.2, t0 + 0.3) for t0 in ETAPES[1:]]:
    rapide(a, b)
for tt, cc_, a_ in [(T_STOP, ROUGE, 0.12), (T_ENR + 0.38, JAUNE, 0.10), (TW(30), JAUNE, 0.08), (ETAPES[4], JAUNE, 0.14),
                    (T_CB + 0.1, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, ETAPES[4], 1, 0.6) + battement(t, T_CB + 0.1, 1, 0.6) - 2)
    entete_marque(c, t)
    hook(c, t)
    etape1(c, t); etape2(c, t); etape3(c, t); partage(c, t); etape4(c, t); etape5(c, t)
    fin(c, t)
    rail(c, t)
    K.dessine_eclairs(c, t)
    # la bulle verte et le carton « Dis-moi » disent déjà la phrase : sous-titres masqués pendant les citations
    en_citation = any(t0 - 0.1 <= t <= t1 for t0, t1 in CITATIONS)
    if not en_citation and not (T_COM - 0.05 < t < T_FIN - 0.1) and t < T_CB: SOUS.dessine(c, t, BLANC)
