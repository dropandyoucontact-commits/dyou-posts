"""DY-M14 « 3 trucs que personne te dit » — guide organique TikTok DROP&YOU (18/10/2026).

Format guide (chez @waldistribution, ce sont les guides qui font les partages) : « 3 trucs avant de commander en Chine »,
abonne-toi + enregistre juste après le hook, intention de commentaire à la fin (« ton plus gros problème quand tu
commandes en Chine »). Horodatage façon appareil photo (« 14:32 · Guangzhou ») sur les vraies images, pour le côté
« filmé sur place ». Thème glace validé, vraies paires et vraies images, zone sûre TikTok / Snap.
Conformité du 17/10 : aucune marque, aucune autre plateforme, aucune promesse de gain, « plusieurs qualités » sans grille.
"""
import math, pathlib, sys, json
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *
from studio3d import *
import glace
glace.appliquer()
from glace import verre, BLEU, balayage

DUREE = round(json.load(open(P / "timing.json"))["mots"][-1]["t1"] + 1.7, 2)
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = sous_titres(K)

LOGO = "logo-dy-blanc"
DOUDOUNE = "produits/textile/veste-doudoune-bleue"
PAIRES = ["b/c22", "b/p09", "b/c23", "b/c05", "b/c31", "b/c27", "b/c11", "b/c09", "b/c29"]
GLACIER, VERT_, ROUGE_, JAUNE_ = "#8FB4FF", "#2BD67B", "#FF4D5E", "#FFC53D"
CX = 510
_T = [0.0]

T_CHINE, T_TROIS, T_PERSONNE = TW(4), TW(7), TW(10)
T_ABO, T_ENREG, T_VIDEO, T_BESOIN = TW(13), TW(15), TW(17), TW(22)
T_UN, T_PRIX, T_VERIF, T_LIVR, T_SINON, T_SURPRISE, T_FIN1, T_CHEZ, T_COMPRISE = TW(23), TW(25), TW(26), TW(30), TW(31), TW(34), TW(38), TW(39), TW(43)
T_DEUX, T_QUAL, T_SELON, T_PLUS, T_DEMANDE, T_LAQUELLE, T_AVANT, T_PAYER = TW(44), TW(46), TW(47), TW(53), TW(54), TW(56), TW(59), TW(61)
T_TROIS3, T_TAILLES, T_VET, T_PETIT, T_DEMANDE3, T_GUIDE = TW(62), TW(64), TW(67), TW(72), TW(73), TW(75)
T_ET, T_PROBLEME, T_DIS, T_COMM = TW(78), TW(85), TW(91), TW(93)
T_FIN = T_COMM + 0.55


# ─────────────────────────────────────────── briques
def titre(c, t, l1, l2, t0, t1, y=400, t2=None, e1="masque", e2="ressort"):
    """titre éditorial (zone sûre : 760 px de large au plus) ; part avant la scène suivante"""
    if t < t0 - 0.1 or t > t1 + 0.12: return
    a = 1 - prog(t, t1 - 0.18, 0.15, entree)
    if l1:
        lettres(c, l1, 540, y, ajuste(l1, 760, 72, "noir", -0.03), t, t0 - 0.05, e1, grad=False, couleur="#FFFFFF", decal=0.025, duree=0.35, alpha=a)
    if l2:
        lettres(c, l2, 540, y + 84, ajuste(l2, 760, 128, "noir", -0.035), t, (t2 if t2 is not None else t0 + 0.1) - 0.05, e2, decal=0.03, alpha=a)


def filigrane(c, t):
    lw = 200
    image(c, LOGO, 540 - lw / 2, 262, lw, 0.9 * (1 - prog(t, T_FIN - 0.2, 0.3)))


def horodatage(c, x, y, s, t, alpha=1.0):
    """tampon façon appli photo de chantier : barre jaune, heure qui tourne, date, lieu"""
    sec = 7 + int(t)
    with Calque(c, alpha):
        c.save(); c.translate(x, y); c.scale(s, s)
        rrect(c, -14, -8, 330, 150, 18, "#000000", 0.28)
        rrect(c, 0, 0, 8, 134, 4, JAUNE_)
        texte(c, f"14:{32 + sec // 60:02d}", 24, -4, 64, "#FFFFFF", "noir", track=-0.02)
        texte(c, f":{sec % 60:02d}", 24 + largeur(f"14:{32 + sec // 60:02d}", 64, "noir", -0.02) + 4, 22, 30, "#FFFFFF", "titre", track=0, alpha=0.85)
        texte(c, "18/10/2026 · dimanche", 24, 72, 24, "#FFFFFF", "demi", track=0)
        icone(c, "map-pin", 34, 120, 22, JAUNE_, 2.4)
        texte(c, "Guangzhou, Chine", 52, 104, 24, "#FFFFFF", "titre", track=0)
        c.restore()


def cadre_reel(nom, t_local, vitesse=1.0, photo=False, zoom=(1.0, 1.1), stamp=0.62):
    """une vraie vidéo (ou photo) plein cadre dans une carte de verre, avec l'horodatage et le point rouge d'enregistrement"""
    def f(c, w, h):
        verre(c, 0, 0, w, h, w * 0.07)
        m = w * 0.035
        if photo:
            image_cover(c, nom, m, m, w - 2 * m, h - 2 * m, mix(zoom[0], zoom[1], borne(t_local / 3)), 0.5, 0.5, w * 0.055)
        else:
            video(c, nom, m, m, w - 2 * m, h - 2 * m, t_local, vitesse, False, rayon=w * 0.055)
        k = w / 600
        horodatage(c, m + 30 * k, h - m - 190 * k, stamp * k * 1.6, _T[0])
        disque(c, w - m - 40 * k, m + 42 * k, 11 * k, ROUGE_, 0.55 + 0.45 * math.sin(_T[0] * 7))
        texte(c, "REC", w - m - 118 * k, m + 28 * k, 26 * k, "#FFFFFF", "titre", track=0.02)
        balayage(c, 0, 0, w, h, _T[0], w * 0.07)
    return f


def produit_plan(nom, haut=0.43, place=0.6):
    def f(c, w, h):
        iw, ih = taille_img(nom)
        verre(c, 0, 0, w, h, w * 0.1)
        lueur_s(c, w / 2, h * haut, w * 0.55, BLEU, 0.4)
        s = min(w * 0.84 / iw, h * place / ih)
        image(c, nom, w / 2 - iw * s / 2, h * haut - ih * s / 2, iw * s)
        balayage(c, 0, 0, w, h, _T[0], w * 0.1)
    return f


# ─────────────────────────────────────────── 1. hook : 3 trucs que personne te dit (vraie image d'entrepôt, horodatée)
def scene_hook(c, t):
    if t > T_ABO + 0.2: return
    part = prog(t, T_ABO - 0.2, 0.35, entree)
    with Calque(c, 1 - part):
        o = prog(t, 0.0, T_ABO, douce)
        cam = Cam(ax=mix(-8, -3, o) + 1.5 * math.sin(t * 1.4), ay=mix(-16, 10, o), az=mix(-3, 1, o), tz=mix(140, 30, o) + 700 * part, cx=CX, cy=1010)
        sx, sy = secousse(t, 0.0, 12, 0.3); a, b = secousse(t, T_TROIS, 8, 0.25)
        cam.cx += sx + a; cam.cy += sy + b
        FW, FH = 600, 760
        coupe = T_TROIS - 0.08
        if t < coupe:
            dessin = cadre_reel("entrepot-cartons", t + 0.05, 0.55)
        else:
            dessin = cadre_reel("lieux/kinbo-devanture-guangzhou", t - coupe, photo=True)
        scene3d(c, cam, [Plan(coins((0, 0, 0), FW, FH), FW, FH, dessin)])
        fl = 1 - (t - coupe) / 0.14
        if 0 < fl <= 1: c.drawRect(skia.Rect.MakeWH(1080, 1920), peinture("#FFFFFF", 0.4 * fl))
    titre(c, t, "AVANT DE COMMANDER", "EN CHINE", -0.45, T_TROIS - 0.08, t2=-0.3)
    titre(c, t, "3 TRUCS QUE", "PERSONNE TE DIT", T_TROIS - 0.08, T_ABO - 0.05, t2=T_PERSONNE - 0.1, e1="ressort")


# ─────────────────────────────────────────── 2. abonne-toi + enregistre (juste après le hook)
def scene_cta(c, t):
    t0, t1 = T_ABO - 0.15, T_UN - 0.12
    g = Groupe(c, t, t0, t1, ent="grand", sor="recul", d_in=0.35, d_out=0.28)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.4)
        tap1, tap2 = T_ABO + 0.35, T_VIDEO + 0.05
        ap1 = prog(t, tap1 - 0.06, 0.06, sortie) * (1 - prog(t, tap1 + 0.05, 0.14, sortie))
        ap2 = prog(t, tap2 - 0.06, 0.06, sortie) * (1 - prog(t, tap2 + 0.05, 0.14, sortie))
        abonne, rempli = t > tap1, prog(t, tap2, 0.25, sortie)
        cam = Cam(ax=-10 + 3 * math.sin(t), ay=mix(-30, 10, a) + 4 * math.sin(t * 0.8), tz=mix(800, 20, a), cx=CX, cy=980)
        W_, H_ = 680, 440
        def profil(cc, w, h):
            verre(cc, 0, 0, w, h, 50)
            cc.save(); cc.translate(w / 2, 112)
            p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 20))
            cc.drawCircle(0, 0, 74, p); disque(cc, 0, 0, 74, "#111833"); anneau(cc, 0, 0, 74, "#FFFFFF", 3, 0.7)
            iw, ih = taille_img(LOGO); image(cc, LOGO, -56, -56 * ih / iw, 112)
            cc.restore()
            texte(cc, "Drop&You", w / 2, 206, 46, "#FFFFFF", "titre", "centre", -0.02)
            texte(cc, "Ton équipe sur place, en Chine", w / 2, 264, 25, "#A9B4D4", "demi", "centre", 0)
            # bouton s'abonner
            bw, bh = 330, 84
            cc.save(); cc.translate(w / 2 - 60, 364); s_ = 1 - 0.08 * ap1; cc.scale(s_, s_)
            if not abonne:
                cc.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-bw / 2, -bh / 2, bw, bh), 22, 22), pgrad(-bw / 2, 0, bw / 2, 0, ["#FF3B5C", "#FF5A73"]))
                icone(cc, "circle-plus", -bw / 2 + 74, 0, 36, "#FFFFFF", 2.6)
                texte(cc, "S'abonner", -bw / 2 + 104, -hauteurLigne(31, "titre") / 2, 31, "#FFFFFF", "titre", track=-0.01)
            else:
                verre(cc, -bw / 2, -bh / 2, bw, bh, 22, 1.0, None, 0.6)
                icone(cc, "check", -bw / 2 + 80, 0, 32, VERT_, 3)
                texte(cc, "Abonné", -bw / 2 + 110, -hauteurLigne(31, "titre") / 2, 31, "#FFFFFF", "titre", track=-0.01)
            cc.restore()
            # bouton enregistrer (signet)
            cc.save(); cc.translate(w / 2 + 175, 364); s_ = 1 - 0.1 * ap2 + 0.12 * battement(t, tap2, 1, 0.35) - 0.12; cc.scale(s_, s_)
            verre(cc, -42, -42, 84, 84, 22, 1.0, None, 0.6)
            pth = skia.Path(); pth.moveTo(-17, -24); pth.lineTo(17, -24); pth.lineTo(17, 26); pth.lineTo(0, 13); pth.lineTo(-17, 26); pth.close()
            if rempli > 0:
                cc.save(); cc.clipRect(skia.Rect.MakeXYWH(-20, 28 - 54 * rempli, 40, 54 * rempli)); cc.drawPath(pth, peinture(JAUNE_)); cc.restore()
            cc.drawPath(pth, peinture("#FFFFFF", 1, Style=skia.Paint.kStroke_Style, StrokeWidth=4, StrokeJoin=skia.Paint.kRound_Join))
            cc.restore()
        scene3d(c, cam, [Plan(coins((0, 0, 0), W_, H_), W_, H_, profil)])
        X1, Y1 = cam.proj((-60, 364 - H_ / 2, 0))[:2]
        X2, Y2 = cam.proj((175, 364 - H_ / 2, 0))[:2]
        cu = prog(t, tap1 - 0.4, 0.35, sortie); cv = prog(t, tap2 - 0.4, 0.35, sortie)
        if cu > 0 and t < tap2 - 0.4:
            curseur(c, mix(820, X1 + 20, cu), mix(1450, Y1 + 10, cu), 1.2, 1.0, ap1); clic(c, X1, Y1, t, tap1)
        elif cv > 0:
            curseur(c, mix(X1 + 20, X2 + 20, cv), mix(Y1 + 10, Y2 + 10, cv), 1.2, 1 - prog(t, tap2 + 0.5, 0.3), ap2); clic(c, X2, Y2, t, tap2)
        if abonne: eclats(c, X1, Y1, t, tap1 + 0.02, 12, 340, graine=6)
        if t > tap2: eclats(c, X2, Y2, t, tap2 + 0.02, 14, 380, cols=[JAUNE_, "#FFFFFF", GLACIER], graine=14)
        titre(c, t, "ABONNE-TOI", "ET ENREGISTRE", T_ABO - 0.05, t1, t2=T_ENREG - 0.05, e1="ressort", e2="masque")


# ─────────────────────────────────────────── 3. truc n°1 : le prix (livraison comprise ?)
def scene_prix(c, t):
    t0, t1 = T_UN - 0.12, T_DEUX - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="gauche", d_in=0.3, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        chez = prog(t, T_CHEZ - 0.2, 0.6, entreeSortie)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-24, 8, a) + 4 * math.sin(t * 0.8) - 10 * chez, tz=mix(600, 20, a), cx=CX, cy=1005)
        RW, RH = 560, 720
        surprise = prog(t, T_SURPRISE - 0.1, 0.35, sortieExpo)
        def ticket(cc, w, h):
            verre(cc, 0, 0, w, h, 40)
            iw, ih = taille_img("b/c22"); s = min(w * 0.66 / iw, 220 / ih)
            lueur_s(cc, w / 2, 140, w * 0.4, BLEU, 0.4)
            image(cc, "b/c22", w / 2 - iw * s / 2, 140 - ih * s / 2, iw * s)
            rrect(cc, 36, 272, w - 72, 2, 1, "#2B3454")
            # lignes du ticket
            texte(cc, "Produit", 44, 300, 32, "#FFFFFF", "titre", track=-0.01)
            icone(cc, "check", w - 70, 322, 32, VERT_, 3)
            l = prog(t, T_LIVR - 0.1, 0.35, sortieExpo)
            if l > 0:
                with Calque(cc, borne(l * 3)):
                    texte(cc, "Livraison", 44, 384, 32, "#FFFFFF", "titre", track=-0.01)
                    if chez <= 0.5:
                        texte(cc, "?", w - 82, 376, 44, JAUNE_, "noir", track=0)
            if surprise > 0 and chez < 1:
                with Calque(cc, borne(surprise * 3) * (1 - chez)):
                    texte(cc, "+ frais en plus", 44, 468, 32, ROUGE_, "titre", track=-0.01)
                    texte(cc, "!", w - 74, 460, 44, ROUGE_, "noir", track=0)
            rrect(cc, 36, 556, w - 72, 2, 1, "#2B3454")
            texte(cc, "Total", 44, 600, 36, "#A9B4D4", "titre", track=-0.01)
            if chez > 0.5:
                texte(cc, "comprise", w - 44 - largeur("comprise", 32, "titre"), 388, 32, VERT_, "titre", track=-0.01)
                icone(cc, "check", w - 70, 622, 34, VERT_, 3)
            elif surprise > 0:
                texte(cc, "???", w - 44 - largeur("???", 40, "noir"), 594, 40, ROUGE_, "noir", track=0)
        plans = []
        if chez > 0:
            AW, AH = 360, 470
            plans.append(Plan(coins((mix(0, -170, chez), mix(0, -60, chez), mix(300, 140, chez)), AW, AH, ay=mix(0, 16, chez)), AW, AH,
                              cadre_reel("avion", t - T_CHEZ + 0.6, 1.0, stamp=0.5), borne(chez * 2)))
        plans.append(Plan(coins((mix(0, 110, chez), 0, 0), RW, RH, ay=mix(0, -10, chez)), RW, RH, ticket))
        sx, sy = secousse(t, T_SURPRISE, 12, 0.3)
        cam.cx += sx; cam.cy += sy
        scene3d(c, cam, plans)
        if t > T_SURPRISE: eclats(c, CX + 120, 1140, t, T_SURPRISE + 0.02, 10, 300, cols=[ROUGE_, "#FFFFFF"], graine=3)
        tp = entre(t, T_COMPRISE - 0.12, 0.4, 2.6)
        if tp > 0:
            c.save(); c.translate(CX + 60, 1300); c.rotate(-7); c.scale(mix(1.8, 1, tp), mix(1.8, 1, tp))
            with Calque(c, borne(tp * 3)):
                rrect(c, -250, -50, 500, 100, 24, None, 1.0, None, VERT_, 6)
                texte(c, "LIVRAISON COMPRISE", 0, -24, 40, VERT_, "noir", "centre", -0.01)
            c.restore()
            eclats(c, CX + 60, 1300, t, T_COMPRISE, 14, 380, cols=[VERT_, "#FFFFFF", GLACIER], graine=11)
        titre(c, t, "TRUC N°1", "LE PRIX", T_UN - 0.05, T_CHEZ - 0.1, t2=T_PRIX - 0.05, e1="ressort")
        titre(c, t, "CHEZ NOUS", "ELLE EST COMPRISE", T_CHEZ - 0.1, t1, t2=T_COMPRISE - 0.12)


# ─────────────────────────────────────────── 4. truc n°2 : la qualité (demande laquelle tu reçois)
def scene_qualite(c, t):
    t0, t1 = T_DEUX - 0.12, T_TROIS3 - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="gauche", d_in=0.3, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        ev = prog(t, T_SELON - 0.15, 0.6, entreeSortie)
        dem = prog(t, T_DEMANDE - 0.15, 0.5, entreeSortie)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-20, 8, a) + 4 * math.sin(t * 0.8), tz=mix(500, 30, a) + 60 * ev, cx=CX, cy=1000)
        plans = []
        # la vraie photo de l'atelier (horodatée), qui recule derrière les cartes
        FW, FH = 520, 680
        plans.append(Plan(coins((0, mix(0, -40, ev), mix(0, 420, ev)), FW, FH), FW, FH,
                          cadre_reel("couture-semelle", t - t0, photo=True, stamp=0.55), 1 - 0.65 * ev))
        CW, CH = 250, 330
        choix = 2
        for k in range(3):
            u = prog(t, T_SELON - 0.1 + 0.1 * k, 0.5, sortieExpo)
            if u <= 0: continue
            sel = (k == choix) * entre(t, T_LAQUELLE - 0.05, 0.4, 2.0)
            def carte(cc, w, h, k=k, sel=sel):
                produit_plan("b/p09", haut=0.42, place=0.4)(cc, w, h)
                for j in range(3): disque(cc, w / 2 - 30 + 30 * j, h * 0.84, 9, GLACIER, 1.0 if j <= k else 0.2)
                if sel > 0: rrect(cc, 3, 3, w - 6, h - 6, w * 0.1, None, 1.0, None, VERT_, 6 * borne(sel))
            plans.append(Plan(coins(((k - 1) * 230, mix(0, -40, dem) - 30 * (sel > 0), (1 - u) * 700 - 40 * sel), CW, CH, ay=(k - 1) * -12), CW, CH, carte, borne(u * 3)))
        scene3d(c, cam, plans)
        # la question au fournisseur, en bulle
        if dem > 0:
            c.save(); c.translate(CX, 1250); c.scale(mix(0.5, 1, dem), mix(0.5, 1, dem))
            with Calque(c, borne(dem * 3)):
                verre(c, -300, -58, 600, 116, 40)
                tuile(c, "message-circle", -230, 0, 74, "grad")
                texte(c, "Laquelle je reçois ?", -176, -28, 40, "#FFFFFF", "titre", track=-0.02)
            c.restore()
        pa = entre(t, T_AVANT - 0.1, 0.4, 2.2)
        if pa > 0:
            c.save(); c.translate(CX + 170, 1355); c.rotate(-4)
            pill(c, "Avant de payer", 0, 0, 30, "grad", "lock", borne(pa * 3), mix(0.4, 1, pa))
            c.restore()
        titre(c, t, "TRUC N°2", "LA QUALITÉ", T_DEUX - 0.05, T_DEMANDE - 0.1, t2=T_QUAL - 0.05, e1="ressort")
        titre(c, t, "DEMANDE TOUJOURS", "LAQUELLE", T_DEMANDE - 0.1, t1, t2=T_LAQUELLE - 0.05)


# ─────────────────────────────────────────── 5. truc n°3 : les tailles (guide des tailles)
def scene_tailles(c, t):
    t0, t1 = T_TROIS3 - 0.12, T_ET - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.3, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        pet = prog(t, T_PETIT - 0.35, 0.5, entreeSortie)
        gui = prog(t, T_DEMANDE3 - 0.1, 0.55, entreeSortie)
        cam = Cam(ax=-10 + 2 * math.sin(t), ay=mix(-20, 8, a) + 4 * math.sin(t * 0.8), tz=mix(500, 40, a), cx=CX, cy=1010)
        plans = []
        DW, DH = 400, 500
        def veste(cc, w, h):
            verre(cc, 0, 0, w, h, 40)
            lueur_s(cc, w / 2, h * 0.46, w * 0.55, BLEU, 0.4)
            iw, ih = taille_img(DOUDOUNE); s = min(w * 0.8 / iw, h * 0.74 / ih) * mix(1.0, 0.8, pet)
            image(cc, DOUDOUNE, w / 2 - iw * s / 2, h * 0.47 - ih * s / 2, iw * s)
            rrect(cc, w - 104, 24, 80, 56, 16, "#FFFFFF")
            texte(cc, "M", w - 64, 30, 38, "#0B1126", "noir", "centre", 0)
            if pet > 0:
                for j in range(2):
                    icone(cc, "arrow-down", w / 2 + (j * 2 - 1) * (w * 0.36), h * 0.5, 44, ROUGE_, 3, borne(pet * 3))
        plans.append(Plan(coins((mix(0, -150, gui), 0, mix(0, 120, gui)), DW, DH, ay=mix(0, 14, gui)), DW, DH, veste))
        if gui > 0:
            GW, GH = 420, 460
            def guide(cc, w, h):
                verre(cc, 0, 0, w, h, 36)
                texte(cc, "Guide des tailles", 34, 28, 34, "#FFFFFF", "titre", track=-0.02)
                for j, lab in enumerate(["Taille", "Poitrine", "Longueur"]):
                    texte(cc, lab, 34 + j * 132, 96, 22, "#8F99BA", "demi", track=0)
                rang = [("S", "48", "64"), ("M", "50", "66"), ("L", "53", "68"), ("XL", "56", "70")]
                for i, r in enumerate(rang):
                    v = prog(t, T_GUIDE - 0.1 + 0.08 * i, 0.3, sortieExpo)
                    if v <= 0: continue
                    y = 146 + i * 72
                    with Calque(cc, borne(v * 3)):
                        if r[0] == "L": rrect(cc, 20, y - 10, w - 40, 62, 16, BLEU, 0.35)
                        for j, val in enumerate(r):
                            texte(cc, val + (" cm" if j else ""), 34 + j * 132, y, 30, "#FFFFFF" if j == 0 else GLACIER, "titre", track=-0.01)
            plans.append(Plan(coins((mix(400, 115, gui), -10, mix(-200, -40, gui)), GW, GH, ay=mix(-30, -10, gui)), GW, GH, guide, borne(gui * 2)))
        scene3d(c, cam, plans)
        b = entre(t, T_PETIT - 0.2, 0.4, 2.2) * (1 - gui)
        if b > 0: pill(c, "Ça taille petit", CX, 1320, 32, "doux", "shirt", borne(b * 3), mix(0.4, 1, b), rot=-3)
        titre(c, t, "TRUC N°3", "LES TAILLES", T_TROIS3 - 0.05, T_DEMANDE3 - 0.1, t2=T_TAILLES - 0.05, e1="ressort")
        titre(c, t, "DEMANDE LE", "GUIDE DES TAILLES", T_DEMANDE3 - 0.1, t1, t2=T_GUIDE - 0.05)


# ─────────────────────────────────────────── 6. et toi, ton plus gros problème ? → commentaire
def scene_fin(c, t):
    t0 = T_ET - 0.12
    if t < t0: return
    fin = prog(t, T_FIN - 0.1, 0.4, entreeSortie)
    with Calque(c, 1 - fin):
        a = entre(t, t0, 0.5, 1.5)
        cam = Cam(ax=-10 + 3 * math.sin(t), ay=mix(-30, 8, a) + 4 * math.sin(t * 0.8), tz=mix(800, 60, a), cx=CX, cy=1020)
        W_, H_ = 680, 230
        s = "Les tailles, trop petites"
        def commentaire(cc, w, h):
            verre(cc, 0, 0, w, h, 44)
            disque(cc, 76, 86, 40, "#1A2550"); icone(cc, "user-round", 76, 86, 42, GLACIER, 2.2)
            texte(cc, "Toi", 136, 50, 26, "#A9B4D4", "demi", track=0)
            n = int(borne((t - T_PROBLEME) / 0.9) * len(s) + 0.999) if t > T_PROBLEME else 0
            texte(cc, s[:n], 136, 88, 34, "#FFFFFF", "titre", track=-0.01)
            if n < len(s) and int(t * 3) % 2 == 0: rrect(cc, 140 + largeur(s[:n], 34, "titre", -0.01), 90, 4, 38, 2, GLACIER)
            icone(cc, "heart", w - 60, 86, 38, "#FF5A73", 2.6)
            texte(cc, "Répondre", 136, 168, 22, "#8F99BA", "demi", track=0)
        scene3d(c, cam, [Plan(coins((0, 0, 0), W_, H_), W_, H_, commentaire)])
        b = entre(t, T_DIS - 0.1, 0.45, 2.2)
        if b > 0:
            c.save(); c.translate(CX, 1250); c.scale(mix(0.4, 1, b), mix(0.4, 1, b))
            pill(c, "Dis-le en commentaire", 0, 0, 34, "grad", "message-circle", borne(b * 3))
            c.restore()
        titre(c, t, "ET TOI ?", "TON PLUS GROS PROBLÈME", T_ET - 0.05, T_FIN, t2=T_PROBLEME - 0.1, e1="ressort")
    if fin > 0:
        d = entre(t, T_FIN - 0.05, 0.6, 1.5)
        glace.panneau_givre(c, 180, 660, 680, 560, borne(d * 3), t)
        rayons(c, 520, 940, t, 760, 0.08 * borne(d), 16, GLACIER)
        iw, ih = taille_img(LOGO); lw = 500 * mix(0.6, 1, d)
        image(c, LOGO, 520 - lw / 2, 900 - lw * ih / iw / 2, lw, borne(d * 3))
        bb = prog(t, T_FIN + 0.2, 0.4, sortie)
        if bb > 0: texte(c, "Ton équipe sur place, en Chine", 520, 1060 + 20 * (1 - bb), 38, "#FFFFFF", "titre", "centre", -0.02, bb)


# ─────────────────────────────────────────── sons
son(0.0, "whoosh_bas", -8); son(0.0, "impact", -7); son(0.1, "clic", -12)
son(T_TROIS - 0.08, "impact_doux", -8)
for k in range(3): son(T_TROIS + 0.09 * k, "pop", -10)
son(T_PERSONNE - 0.1, "whoosh_court", -10)
son(T_ABO - 0.15, "whoosh", -9); son(T_ABO + 0.35, "clic", -6); son(T_ABO + 0.4, "check", -10)
son(T_VIDEO + 0.05, "clic", -6); son(T_VIDEO + 0.1, "ching", -9)
son(T_UN - 0.12, "whoosh_long", -9); son(T_UN, "impact_doux", -8); son(T_LIVR - 0.1, "pop", -10)
son(T_SURPRISE - 0.1, "impact", -6); son(T_SURPRISE, "blip", -12)
son(T_CHEZ - 0.2, "whoosh", -9); son(T_COMPRISE - 0.12, "tampon", -7); son(T_COMPRISE, "ching", -10)
son(T_DEUX - 0.12, "whoosh_long", -9); son(T_DEUX, "impact_doux", -8)
for k in range(3): son(T_SELON - 0.1 + 0.1 * k, "pop", -12)
son(T_DEMANDE - 0.15, "message_in", -9); son(T_LAQUELLE - 0.05, "check", -10); son(T_AVANT - 0.1, "pop", -11)
son(T_TROIS3 - 0.12, "whoosh_long", -9); son(T_TROIS3, "impact_doux", -8)
son(T_PETIT - 0.35, "montee", -14); son(T_PETIT - 0.2, "pop", -11)
son(T_DEMANDE3 - 0.1, "whoosh", -9)
for i in range(4): son(T_GUIDE - 0.1 + 0.08 * i, "blip", -15)
son(T_ET - 0.12, "swipe", -10)
for i in range(18): son(T_PROBLEME + i * 0.05, "frappe", -18)
son(T_DIS - 0.1, "pop", -9); son(T_COMM, "message_in", -10)
son(T_FIN - 0.1, "whoosh_long", -8); son(T_FIN + 0.05, "impact", -6); son(T_FIN + 0.1, "verre", -10)
son(DUREE - 1.0, "ding", -16)
for a, b in [(0.0, 0.25), (T_TROIS - 0.1, T_TROIS + 0.1), (T_ABO - 0.15, T_ABO + 0.2), (T_UN - 0.12, T_UN + 0.2), (T_SURPRISE - 0.05, T_SURPRISE + 0.12),
             (T_DEUX - 0.12, T_DEUX + 0.2), (T_TROIS3 - 0.12, T_TROIS3 + 0.2), (T_ET - 0.12, T_ET + 0.2), (T_FIN - 0.1, T_FIN + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_TROIS - 0.08, "#FFFFFF", 0.3), (T_VIDEO + 0.05, "#FFFFFF", 0.16), (T_SURPRISE, ROUGE_, 0.14), (T_COMPRISE, VERT_, 0.12),
                    (T_LAQUELLE, VERT_, 0.08), (T_FIN + 0.05, "#FFFFFF", 0.22)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    _T[0] = t
    glace.fond_glace(c, t, battement(t, T_TROIS - 0.08, 1, 0.5) - 1)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_cta(c, t); scene_prix(c, t); scene_qualite(c, t); scene_tailles(c, t)
    scene_fin(c, t)
    filigrane(c, t)
    K.dessine_eclairs(c, t)
    if t < T_FIN - 0.1: SOUS.dessine(c, t, "#FFFFFF")
