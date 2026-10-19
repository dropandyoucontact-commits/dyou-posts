"""DY-M12 « Sur place » — organique TikTok DROP&YOU (17/10/2026).

La présentation de DY-M02 (question directe → « c'est notre métier » → catalogue → photo → qualités → livraison comprise
8-12 jours → unité ou quantité), réécrite aux règles de conformité du 17/10 : aucune marque, aucun WhatsApp / Snap,
pas de « revendre », CTA organiques calés (abonne-toi juste après le hook, enregistre, commentaire + message privé).
Visuel : le verre fumé de DA-M14/M16 v2 (moteur/glace.py) en vraie 3D (studio3d) ; articles de la banque SANS logo
visible (casque, doudoune, moto) — la plupart des vestes de la banque portent des logos de grandes marques.
Logo DROP&YOU en filigrane tout du long (règle du 17/10, cf. DY-M10/M11).
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
SOUS = sous_titres(K, fusions={(13, 14, 15): "Drop&You."})
G = Globe()

LOGO = "logo-dy-blanc"
CASQUE, DOUDOUNE, MOTO = "produits/electronique/casque-audio", "produits/textile/veste-doudoune-bleue", "produits/mobilite/moto-electrique"
GZ, PARIS, BXL = (113.26, 23.13), (2.35, 48.86), (4.35, 50.85)
GLACIER = "#8FB4FF"
_T = [0.0]           # temps courant (reflets des cartes)
VERT_ = "#2BD67B"

# repères (mots)
T_CHINE, T_METIER, T_DY = TW(7), TW(8), TW(13)
T_ABO, T_EXPL, T_CAT = TW(16), TW(22), TW(27)
T_BASK, T_VET, T_ELEC, T_MONT, T_TOUT, T_TEL = TW(27), TW(28), TW(29), TW(30), TW(31), TW(37)
T_CHERCHE, T_ENVOIE, T_PHOTO, T_TROUVE, T_FOURN, T_VALID = TW(38), TW(43), TW(46), TW(49), TW(52), TW(53)
T_SELON, T_PLUS, T_QUAL, T_PRIX, T_LIVR = TW(54), TW(59), TW(60), TW(63), TW(66)
T_COMPTE, T_HUIT, T_JOURS, T_TOI, T_FR, T_BE, T_AIL = TW(67), TW(68), TW(71), TW(74), TW(76), TW(78), TW(80)
T_UNITE, T_QTE, T_GERE = TW(81), TW(85), TW(87)
T_SAVE, T_VIDEO = TW(90), TW(92)
T_COMM, T_COMMENT, T_ECRIS, T_PRIVE = TW(96), TW(99), TW(105), TW(108)
T_FIN = TW(108) + 0.45


# ─────────────────────────────────────────── briques
def titre(c, t, l1, l2, t0, t1, y=420, t2=None, e1="masque", e2="ressort"):
    """titre éditorial : petite ligne blanche, puis le mot-clé géant en dégradé glacier ; part avant la scène suivante"""
    if t < t0 - 0.1 or t > t1 + 0.12: return
    a = 1 - prog(t, t1 - 0.18, 0.15, entree)
    if l1:
        lettres(c, l1, 540, y, ajuste(l1, 940, 74, "noir", -0.03), t, t0 - 0.05, e1, grad=False, couleur="#FFFFFF", decal=0.025, duree=0.35, alpha=a)
    if l2:
        lettres(c, l2, 540, y + 86, ajuste(l2, 980, 132, "noir", -0.035), t, (t2 if t2 is not None else t0 + 0.1) - 0.05, e2, decal=0.03, alpha=a)


def filigrane(c, t):
    iw, ih = taille_img(LOGO); lw = 200
    image(c, LOGO, 540 - lw / 2, 262, lw, 0.9 * (1 - prog(t, T_FIN - 0.2, 0.3)))


def produit_plan(nom, halo=True):
    """un article détouré posé dans une carte de verre (pour un Plan 3D)"""
    iw, ih = taille_img(nom)
    def f(c, w, h):
        verre(c, 0, 0, w, h, w * 0.1)
        if halo: lueur_s(c, w / 2, h * 0.45, w * 0.5, BLEU, 0.35)
        s = min(w * 0.8 / iw, h * 0.72 / ih)
        image(c, nom, w / 2 - iw * s / 2, h * 0.43 - ih * s / 2, iw * s)
        balayage(c, 0, 0, w, h, _T[0], w * 0.1)
    return f


def basket_plan(c, w, h):
    verre(c, 0, 0, w, h, w * 0.1)
    lueur_s(c, w / 2, h * 0.45, w * 0.5, BLEU, 0.35)
    sneaker(c, w / 2, h * 0.46, w * 0.78, "#E9EEF8", BLEU, "#FFFFFF")


def icone_plan(ic):
    def f(c, w, h):
        verre(c, 0, 0, w, h, w * 0.1)
        lueur_s(c, w / 2, h * 0.43, w * 0.5, BLEU, 0.35)
        tuile(c, ic, w / 2, h * 0.43, w * 0.5)
    return f


def etiquette_plan(lab, sous=None):
    """libellé sous une carte catégorie"""
    def f(c, w, h):
        texte(c, lab, w / 2, h * 0.80, w * 0.11, "#FFFFFF", "titre", "centre", -0.02)
    return f


def carte_cat(dessin, lab):
    def f(c, w, h):
        dessin(c, w, h)
        texte(c, lab, w / 2, h * 0.80, w * 0.105, "#FFFFFF", "titre", "centre", -0.02)
    return f


def ecran_catalogue(t, t0):
    """écran du téléphone : la boutique DROP&YOU, sombre, grille d'articles qui défile"""
    noms = [DOUDOUNE, CASQUE, MOTO, DOUDOUNE, CASQUE, MOTO, CASQUE, DOUDOUNE]
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), pgrad(0, 0, 0, h, ["#0D1430", "#05070F"]))
        iw, ih = taille_img(LOGO); lw = 170 * k
        image(c, LOGO, w / 2 - lw / 2, 60 * k, lw)
        cw, ch = (w - 60 * k) / 2, 220 * k
        dy = -110 * k * prog(t, t0 + 0.4, 1.6, douce)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 120 * k, w, h - 120 * k))
        for j, nom in enumerate(noms):
            x = 20 * k + (j % 2) * (cw + 20 * k); y = 130 * k + (j // 2) * (ch + 20 * k) + dy
            verre(c, x, y, cw, ch, 22 * k, 1.0, None, 0.4)
            iw2, ih2 = taille_img(nom)
            s = min((cw - 40 * k) / iw2, (ch - 80 * k) / ih2)
            image(c, nom, x + cw / 2 - iw2 * s / 2, y + 14 * k, iw2 * s)
            rrect(c, x + 16 * k, y + ch - 38 * k, cw * 0.5, 10 * k, 5 * k, "#FFFFFF", 0.3)
            rrect(c, x + cw - 58 * k, y + ch - 46 * k, 42 * k, 26 * k, 13 * k, BLEU)
        c.restore()
    return f


def ecran_dm(t):
    """messagerie privée de l'application (aucune autre plateforme) : la photo part, la réponse arrive"""
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), pgrad(0, 0, 0, h, ["#0B1126", "#04060D"]))
        rrect(c, 0, 0, w, 120 * k, 0, "#0E1530")
        disque(c, 70 * k, 74 * k, 30 * k, "#1A2550"); image(c, LOGO, 46 * k, 64 * k, 48 * k)
        texte(c, "Drop&You", 116 * k, 52 * k, 24 * k, "#FFFFFF", "titre", track=-0.01)
        texte(c, "Message privé", 116 * k, 82 * k, 17 * k, "#8F99BA", "demi", track=0)
        # bulle « je cherche ce modèle »
        u = prog(t, T_CHERCHE - 0.1, 0.35, sortieExpo)
        if u > 0:
            with Calque(c, borne(u * 3)):
                rrect(c, w - 300 * k, (170 + 20 * (1 - u)) * k, 280 * k, 64 * k, 26 * k, BLEU)
                texte(c, "Tu as ce modèle ?", w - 280 * k, (190 + 20 * (1 - u)) * k, 22 * k, "#FFFFFF", "demi", track=0)
        # la photo envoyée
        v = prog(t, T_ENVOIE + 0.1, 0.45, sortieExpo)
        if v > 0:
            with Calque(c, borne(v * 3)):
                x, y, ww, hh = w - 270 * k, (260 + 30 * (1 - v)) * k, 250 * k, 300 * k
                rrect(c, x, y, ww, hh, 26 * k, "#E8EDF7")
                iw, ih = taille_img(DOUDOUNE); s = min(ww * 0.8 / iw, hh * 0.85 / ih)
                image(c, DOUDOUNE, x + ww / 2 - iw * s / 2, y + hh / 2 - ih * s / 2, iw * s)
                if t > T_PHOTO: icone(c, "check", x + ww - 26 * k, y + hh + 18 * k, 20 * k, GLACIER, 2.6)
        # la réponse
        r = prog(t, T_TROUVE - 0.05, 0.35, sortieExpo)
        if r > 0:
            with Calque(c, borne(r * 3)):
                verre(c, 20 * k, (610 + 20 * (1 - r)) * k, 290 * k, 70 * k, 28 * k, 1.0, None, 0.5)
                icone(c, "badge-check", 52 * k, (645 + 20 * (1 - r)) * k, 28 * k, VERT_, 2.4)
                texte(c, "Trouvé ✓", 76 * k, (630 + 20 * (1 - r)) * k, 22 * k, "#FFFFFF", "demi", track=0)
    return f


# ─────────────────────────────────────────── 1. hook : quelqu'un sur place, en Chine ?
def globe_verre(c, t, cx, cy, R, lon0, lat0, alpha=1.0):
    with Calque(c, alpha):
        p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.45), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, R * 0.12))
        c.drawCircle(cx, cy, R, p)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx - R * 0.35, cy - R * 0.4), R * 1.6, [hexa("#24304F"), hexa("#0A0F1F"), hexa("#04060C")], [0, 0.6, 1]))
        c.drawCircle(cx, cy, R, p)
        G.terres(c, cx, cy, R, lon0, lat0, couleurs={0: "#3E5C9E", 1: "#9CC4FF", 2: "#3E5C9E", 3: "#5A7BC4", 4: "#3E5C9E"}, grossir={1: 1.35})
        li = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3)
        li.setShader(skia.GradientShader.MakeLinear([skia.Point(cx - R, cy - R), skia.Point(cx + R, cy + R)], [hexa("#FFFFFF", 0.7), hexa("#FFFFFF", 0.05), hexa(GLACIER, 0.8)]))
        c.drawCircle(cx, cy, R, li)
        rf = skia.Paint(AntiAlias=True)
        rf.setShader(skia.GradientShader.MakeRadial(skia.Point(cx - R * 0.4, cy - R * 0.45), R * 0.5, [hexa("#FFFFFF", 0.16), hexa("#FFFFFF", 0)]))
        c.drawCircle(cx, cy, R, rf)


def scene_hook(c, t):
    if t > T_ABO + 0.3: return
    sortie_ = prog(t, T_ABO - 0.25, 0.4, entree)
    a = prog(t, -0.05, 0.9, sortieExpo)
    plonge = prog(t, T_METIER - 0.1, 0.8, entreeSortie)
    lon0 = mix(-40, GZ[0], prog(t, 0.0, 1.3, entreeSortie)) + 6 * plonge
    lat0 = mix(10, GZ[1] * 0.8, prog(t, 0.0, 1.3, entreeSortie))
    R = mix(260, 380, a) * (1 + 1.6 * plonge)
    cx, cy = 540, mix(1000, 960, a) + 260 * plonge
    with Calque(c, 1 - sortie_):
        globe_verre(c, t, cx, cy, R, lon0, lat0, borne(a * 2) * (1 - 0.6 * plonge))
        u = entre(t, T_CHINE - 0.2, 0.5, 2.0)
        x, y, z = G.pos(*GZ, lon0, lat0, R, cx, cy)
        if u > 0 and z > 0.1:
            onde(c, x, y, t, T_CHINE - 0.1, 20, 160, GLACIER, 5, 0.8)
            onde(c, x, y, t, T_CHINE + 0.5, 20, 160, GLACIER, 4, 0.8)
            lueur_s(c, x, y, 120, BLEU, 0.5 * borne(u))
            c.save(); c.translate(x, y - 40 * u); s_ = mix(0.3, 1, u) * (1 - 0.4 * plonge); c.scale(s_, s_)
            tuile(c, "map-pin", 0, -40, 90)
            c.restore()
            b = entre(t, T_CHINE, 0.45, 2.2) * (1 - plonge)
            if b > 0:
                pill(c, "En direct de Guangzhou", x, y + 90, 30, "vert", None, borne(b * 3), mix(0.4, 1, b))
                disque(c, x - largeur("En direct de Guangzhou", 30, "fort", -0.01) / 2 - 2, y + 90, 7, VERT_, 0.5 + 0.5 * math.sin(t * 9))
        # « notre métier » : le logo dans un disque de verre qui jaillit du globe
        d = entre(t, T_DY - 0.25, 0.55, 1.8)
        if d > 0:
            c.save(); c.translate(540, 1010); c.scale(mix(0.3, 1, d), mix(0.3, 1, d))
            rayons(c, 0, 0, t, 700, 0.10 * borne(d), 16, GLACIER)
            p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.5), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 40))
            c.drawCircle(0, 0, 230, p)
            verre(c, -230, -230, 460, 460, 230)
            iw, ih = taille_img(LOGO); lw = 330
            image(c, LOGO, -lw / 2, -lw * ih / iw / 2, lw, borne(d * 3))
            c.restore()
            eclats(c, 540, 1010, t, T_DY - 0.05, 16, 520, graine=3)
    titre(c, t, "T'AS BESOIN DE QUELQU'UN", "SUR PLACE ?", 0.0, T_METIER, y=420, t2=TW(4))
    titre(c, t, "C'EST EXACTEMENT", "NOTRE MÉTIER", T_METIER, T_ABO - 0.05, y=420, t2=TW(10))


# ─────────────────────────────────────────── 2. abonne-toi (juste après le hook)
def scene_abo(c, t):
    t0, t1 = T_ABO - 0.15, T_CAT - 0.12
    g = Groupe(c, t, t0, t1, ent="grand", sor="recul", d_in=0.4, d_out=0.3)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.6, 1.4)
        tap = T_EXPL + 0.15
        ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
        abonne = t > tap
        cam = Cam(ax=-12 + 3 * math.sin(t), ay=mix(-35, 12, a) + 4 * math.sin(t * 0.8), tz=mix(900, 20, a), cy=960)
        W_, H_ = 760, 470
        def profil(cc, w, h):
            verre(cc, 0, 0, w, h, 50)
            cc.save(); cc.translate(w / 2, 120)
            p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 20))
            cc.drawCircle(0, 0, 78, p)
            disque(cc, 0, 0, 78, "#111833"); anneau(cc, 0, 0, 78, "#FFFFFF", 3, 0.7)
            iw, ih = taille_img(LOGO); image(cc, LOGO, -58, -58 * ih / iw, 116)
            cc.restore()
            texte(cc, "Drop&You", w / 2, 220, 48, "#FFFFFF", "titre", "centre", -0.02)
            texte(cc, "Ton équipe sur place, en Chine", w / 2, 282, 26, "#A9B4D4", "demi", "centre", 0)
            # le bouton s'abonner → abonné
            bw, bh = 380, 88
            s_ = 1 - 0.08 * ap
            cc.save(); cc.translate(w / 2, 390); cc.scale(s_, s_)
            if not abonne:
                cc.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-bw / 2, -bh / 2, bw, bh), 22, 22), pgrad(-bw / 2, 0, bw / 2, 0, ["#FF3B5C", "#FF5A73"]))
                icone(cc, "circle-plus", -bw / 2 + 92, 0, 40, "#FFFFFF", 2.6)
                texte(cc, "S'abonner", -bw / 2 + 124, -hauteurLigne(34, "titre") / 2, 34, "#FFFFFF", "titre", track=-0.01)
            else:
                verre(cc, -bw / 2, -bh / 2, bw, bh, 22, 1.0, None, 0.6)
                icone(cc, "check", -bw / 2 + 96, 0, 36, VERT_, 3)
                texte(cc, "Abonné", -bw / 2 + 128, -hauteurLigne(34, "titre") / 2, 34, "#FFFFFF", "titre", track=-0.01)
            cc.restore()
        scene3d(c, cam, [Plan(coins((0, 0, 0), W_, H_), W_, H_, profil)])
        cu = prog(t, tap - 0.45, 0.4, sortie)
        if cu > 0:
            curseur(c, mix(900, 600, cu), mix(1450, 1200, cu), 1.2, 1 - prog(t, tap + 0.5, 0.3), ap)
            clic(c, 590, 1190, t, tap)
        if abonne:
            eclats(c, 540, 1160, t, tap + 0.02, 14, 420, graine=6)
            for j in range(5):
                hj = prog(t, tap + 0.05 + 0.08 * j, 1.1, sortie)
                if 0 < hj < 1:
                    icone(c, "heart", 640 + 60 * math.sin(j * 2.1), 1160 - 520 * hj, 44 * (1 - 0.4 * hj), "#FF5A73", 2.6, 1 - hj)
        titre(c, t, "ABONNE-TOI", "SI C'EST PAS FAIT", T_ABO - 0.05, t1, y=420, t2=TW(18), e1="ressort", e2="masque")


# ─────────────────────────────────────────── 3. le catalogue
def scene_catalogue(c, t):
    t0, t1 = T_CAT - 0.12, T_CHERCHE - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="zoom", d_in=0.3, d_out=0.32)
    if not g.visible: return
    with g:
        entre_tel = prog(t, T_TOUT - 0.25, 0.7, entreeSortie)
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.9), ay=mix(-14, 10, entre_tel) + 5 * math.sin(t * 0.7), tz=mix(-120, 60, entre_tel), cy=940)
        cats = [(T_BASK, basket_plan, "Baskets"), (T_VET, produit_plan(DOUDOUNE), "Vêtements"),
                (T_ELEC, produit_plan(CASQUE), "Électronique"), (T_MONT, icone_plan("watch"), "Montres")]
        plans = []
        CW, CH = 330, 400
        for k, (tk, dessin, lab) in enumerate(cats):
            u = prog(t, tk - 0.15, 0.55, lambda v: ressort(v, 1.3, 4.6)) if t > tk - 0.15 else 0.0
            if u <= 0: continue
            # éventail 2×2, puis les cartes plongent dans l'écran du téléphone
            gx, gy = (-185 if k % 2 == 0 else 185), (-230 if k < 2 else 210)
            x = mix(gx, 0, entre_tel); y = mix(gy, 0, entre_tel); z = mix(900, 0, min(u, 1.05)) + 900 * entre_tel
            rot = mix(-40 if k % 2 == 0 else 40, (k - 1.5) * 4, min(u, 1))
            plans.append(Plan(coins((x, y, z), CW, CH, ay=rot, az=(k - 1.5) * 2 * (1 - entre_tel)), CW, CH, carte_cat(dessin, lab), borne(u * 3) * (1 - entre_tel)))
        if entre_tel > 0:
            PW_, PH_ = 400, 816
            plans.append(Plan(coins((0, mix(900, -10, entre_tel), mix(400, 0, entre_tel)), PW_, PH_, ay=mix(-30, -8, entre_tel)), PW_, PH_,
                              tel(ecran_catalogue(t, T_TOUT)), borne(entre_tel * 2)))
        scene3d(c, cam, plans)
        titre(c, t, "TOUT LE CATALOGUE", "DANS TA POCHE", T_TOUT - 0.05, t1, y=400, t2=TW(36))
        if t < T_TOUT - 0.1:
            # le mot de la catégorie, en grand, à l'instant où il est dit
            for tk, lab, y in [(T_BASK, "BASKETS", 400), (T_VET, "VÊTEMENTS", 400), (T_ELEC, "ÉLECTRONIQUE", 400), (T_MONT, "MONTRES", 400)]:
                fin = min([x for x in (T_VET, T_ELEC, T_MONT, T_TOUT) if x > tk] or [T_TOUT])
                if tk - 0.1 < t < fin:
                    lettres(c, lab, 540, y, ajuste(lab, 960, 140, "noir", -0.035), t, tk - 0.08, "masque", decal=0.02, duree=0.3,
                            alpha=1 - prog(t, fin - 0.08, 0.08))


# ─────────────────────────────────────────── 4. envoie une photo → on la trouve chez nos fournisseurs validés
def scene_photo(c, t):
    t0, t1 = T_CHERCHE - 0.12, T_SELON - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="gauche", d_in=0.38, d_out=0.32)
    if not g.visible: return
    with g:
        sort_ = prog(t, T_TROUVE - 0.3, 0.7, entreeSortie)
        cam = Cam(ax=-8 + 3 * math.sin(t), ay=mix(16, -22, sort_) + 4 * math.sin(t * 0.8), tz=mix(140, 380, sort_), cy=980, tx=-120 * sort_)
        PW_, PH_ = 420, 856
        plans = [Plan(coins((0, -20, 0), PW_, PH_), PW_, PH_, tel(ecran_dm(t)))]
        # la photo sort de l'écran et se pose en carte de verre, avec la fiche fournisseur derrière
        if sort_ > 0:
            CW, CH = 400, 480
            plans.append(Plan(coins((mix(60, 330, sort_), mix(-60, -160, sort_), mix(-5, -420, sort_)), CW, CH, ay=mix(0, -18, sort_), az=mix(0, 4, sort_)),
                              CW, CH, produit_plan(DOUDOUNE), borne(sort_ * 3)))
        scene3d(c, cam, plans)
        f = entre(t, T_FOURN - 0.12, 0.45, 2.0)
        if f > 0:
            c.save(); c.translate(760, 1220); c.rotate(3); c.scale(mix(0.4, 1, f), mix(0.4, 1, f))
            with Calque(c, borne(f * 3)):
                verre(c, -250, -80, 500, 160, 40)
                tuile(c, "badge-check", -170, 0, 86, "grad")
                texte(c, "Fournisseur", -110, -46, 34, "#FFFFFF", "titre", track=-0.02)
                texte(c, "validé", -110, -4, 34, GLACIER, "titre", track=-0.02)
                for j in range(3): disque(c, 160 + 26 * j, 0, 8, VERT_, 1.0 if t > T_VALID + 0.05 * j else 0.25)
            c.restore()
            eclats(c, 760, 1220, t, T_VALID, 12, 360, graine=8)
        sc = prog(t, T_TROUVE - 0.05, 0.6, lin)
        if 0 < sc < 1:
            X0, Y0 = cam.proj((330, -400, -420))[:2]
            trait(c, X0 - 200, mix(Y0, Y0 + 460, sc), X0 + 200, mix(Y0, Y0 + 460, sc), GLACIER, 4, 0.8)
            lueur_s(c, X0, mix(Y0, Y0 + 460, sc), 160, BLEU, 0.4)
        titre(c, t, "TU CHERCHES", "UN MODÈLE ?", T_CHERCHE - 0.05, T_ENVOIE + 0.05, y=400, t2=TW(41))
        titre(c, t, "ENVOIE UNE PHOTO", "ON LE TROUVE", T_ENVOIE + 0.05, t1, y=400, t2=T_TROUVE - 0.1, e1="ressort")


# ─────────────────────────────────────────── 5. plusieurs qualités, livraison comprise
def scene_qualites(c, t):
    t0, t1 = T_SELON - 0.12, T_COMPTE - 0.12
    g = Groupe(c, t, t0, t1, ent="droite", sor="haut", d_in=0.32, d_out=0.3)
    if not g.visible: return
    with g:
        ev = prog(t, T_PLUS - 0.2, 0.7, entreeSortie)
        prix_ = prog(t, T_PRIX - 0.15, 0.6, entreeSortie)
        cam = Cam(ax=-10 + 3 * math.sin(t), ay=8 * math.sin(t * 0.7) - 12 * prix_, tz=mix(300, 200, ev), cy=960)
        CW, CH = 360, 440
        plans = []
        for k in range(3):
            u = prog(t, t0 + 0.1 + 0.12 * k, 0.5, sortieExpo)
            x = mix(0, (k - 1) * 300, ev); z = (k - 1) * -30 + (1 - u) * 800 + mix(k * 40, 0, ev)
            def carte(cc, w, h, k=k):
                produit_plan(CASQUE)(cc, w, h)
                for j in range(3):
                    disque(cc, w / 2 - 34 + 34 * j, h * 0.86, 10, GLACIER, 1.0 if j <= k else 0.2)
            plans.append(Plan(coins((x, -40 - 160 * prix_, z + 300 * prix_), CW, CH, ay=mix(0, (k - 1) * -14, ev)), CW, CH, carte, borne(u * 3) * (1 - 0.75 * prix_)))
        scene3d(c, cam, plans)
        b = entre(t, T_QUAL - 0.1, 0.45, 2.2) * (1 - prix_)
        if b > 0: pill(c, "Selon les produits", 540, 1250, 32, "doux", "layers", borne(b * 3), mix(0.4, 1, b), rot=-2)
        # l'étiquette de prix : livraison comprise (aucun montant)
        if prix_ > 0:
            c.save(); c.translate(540, 1200); c.rotate(mix(-14, -4, prix_)); s_ = mix(0.3, 1, prix_); c.scale(s_, s_)
            with Calque(c, borne(prix_ * 3)):
                verre(c, -330, -90, 660, 180, 44)
                tuile(c, "truck", -240, 0, 96, "grad")
                texte(c, "Livraison", -170, -54, 40, "#FFFFFF", "titre", track=-0.02)
                l = entre(t, T_LIVR - 0.1, 0.4, 2.4)
                if l > 0:
                    c.save(); c.translate(-170 + largeur("comprise", 44, "noir") / 2, 22); c.scale(mix(1.8, 1, l), mix(1.8, 1, l))
                    texte(c, "comprise", -largeur("comprise", 44, "noir") / 2, -26, 44, GLACIER, "noir", track=-0.02, alpha=borne(l * 3))
                    c.restore()
                    icone(c, "check", 250, 0, 60, VERT_, 3.4, borne(l * 3))
            c.restore()
            eclats(c, 540, 1200, t, T_LIVR, 14, 420, graine=11)
        titre(c, t, "SELON LES PRODUITS", "PLUSIEURS QUALITÉS", T_SELON - 0.05, T_PRIX - 0.1, y=400, t2=T_PLUS - 0.05)
        titre(c, t, "ET LE PRIX", "COMPREND LA LIVRAISON", T_PRIX - 0.1, t1, y=400, t2=TW(64) - 0.05)


# ─────────────────────────────────────────── 6. 8 à 12 jours, jusqu'à chez toi
def scene_livraison(c, t):
    t0, t1 = T_COMPTE - 0.12, T_UNITE - 0.12
    g = Groupe(c, t, t0, t1, ent="zoom", sor="recul", d_in=0.35, d_out=0.3)
    if not g.visible: return
    with g:
        a = prog(t, t0, 0.8, sortieExpo)
        vol = prog(t, T_HUIT, T_TOI + 0.2 - T_HUIT, entreeSortie)
        lon0 = mix(GZ[0], 50, vol); lat0 = mix(28, 42, vol)
        R = mix(300, 400, a); cx, cy = 540, 1080
        globe_verre(c, t, cx, cy, R, lon0, lat0, borne(a * 2))
        G.arc(c, GZ, PARIS, cx, cy, R, lon0, lat0, 1.0, "#3E5C9E", 4, 0.35, [2, 14])
        x, y, z = G.arc(c, GZ, PARIS, cx, cy, R, lon0, lat0, max(0.02, vol), GLACIER, 7, 0.35)
        # le carton qui voyage sur l'arc
        if vol < 0.995:
            cam = Cam(ax=-18, ay=30 + 50 * t, tz=0, cx=x, cy=y)
            scene3d(c, cam, carton3d_g((0, 0, 0), 90))
        for lieu, lab, tk, dx in [(PARIS, "France", T_FR, 0), (BXL, "Belgique", T_BE, 0)]:
            px, py, pz = G.pos(*lieu, lon0, lat0, R, cx, cy)
            u = entre(t, tk - 0.1, 0.45, 2.2)
            if u > 0 and pz > 0.05:
                disque(c, px, py, 9, GLACIER)
                c.save(); c.translate(px + (90 if lab == "Belgique" else -90), py - 70 * u); c.scale(mix(0.3, 1, u), mix(0.3, 1, u))
                pill(c, lab, 0, 0, 28, "doux", "map-pin", borne(u * 3))
                c.restore()
        u = entre(t, T_AIL - 0.1, 0.45, 2.2)
        if u > 0: pill(c, "Et ailleurs", 540, 1500 - 60, 30, "grad", "globe", borne(u * 3), mix(0.4, 1, u), rot=-2)
        if vol >= 0.99:
            onde(c, x, y, t, T_TOI + 0.2, 20, 200, GLACIER, 6, 0.7)
        # le compteur 8 → 12 jours
        n = entre(t, T_HUIT - 0.1, 0.45, 1.8)
        if n > 0:
            j = 8 if t < T_JOURS - 0.25 else 8 + int(round(4 * prog(t, T_JOURS - 0.25, 0.4, sortie)))
            with Calque(c, borne(n * 3) * (1 - prog(t, t1 - 0.2, 0.15))):
                s = f"8 À {j}" if j > 8 else "8"
                lettres(c, s, 540, 400, 170, t, T_HUIT - 0.08, "ressort", decal=0.04)
                lettres(c, "JOURS", 540, 590, 86, t, T_JOURS - 0.1, "masque", grad=False, couleur="#FFFFFF", decal=0.03, duree=0.3)


def carton3d_g(centre, taille, ay=0.0, ax=0.0, az=0.0, alpha=1.0):
    """carton d'expédition (même dessin que dy3d), scotch et étiquette"""
    def face(c, w, h):
        rrect(c, 0, 0, w, h, 8, "#C8955A")
        rrect(c, w * 0.42, 0, w * 0.16, h, 0, "#E2B97E")
        rrect(c, w * 0.12, h * 0.6, w * 0.3, h * 0.24, 6, "#F3F0EA", 0.95)
    def cote(c, w, h): rrect(c, 0, 0, w, h, 8, "#B48048")
    def haut(c, w, h):
        rrect(c, 0, 0, w, h, 8, "#D9A86A"); rrect(c, 0, h * 0.42, w, h * 0.16, 0, "#EAC48E")
    return boite(centre, taille, taille * 0.8, taille * 0.8, dict(avant=face, arriere=face, gauche=cote, droite=cote, haut=haut, bas=cote),
                 ax=ax, ay=ay, az=az, alpha=alpha)


# ─────────────────────────────────────────── 7. à l'unité ou en quantité
def scene_quantite(c, t):
    t0, t1 = T_UNITE - 0.12, T_SAVE - 0.12
    g = Groupe(c, t, t0, t1, ent="bas", sor="zoom", d_in=0.3, d_out=0.3)
    if not g.visible: return
    with g:
        q = prog(t, T_QTE - 0.15, 0.9, sortie)
        cam = Cam(ax=-22 + 3 * math.sin(t), ay=24 + 10 * math.sin(t * 0.6) - 20 * q, tz=mix(-200, 500, q), cy=1040)
        sol(c, cam, t, y=150, alpha=0.45, couleur="#4A6FD0")
        plans = []
        a = prog(t, t0, 0.5, lambda v: ressort(v, 1.4, 4.6))
        plans += carton3d_g((0, 150 - 90 - 140 * (1 - min(a, 1)) * 2, 0), 180, ay=20)
        # la pile qui monte
        n = 0
        for i in range(-2, 3):
            for k_ in range(3):
                for h_ in range(3):
                    if i == 0 and k_ == 0 and h_ == 0: continue
                    n += 1
                    d = prog(t, T_QTE - 0.1 + 0.025 * n, 0.4, lambda v: ressort(v, 1.3, 5))
                    if d <= 0: continue
                    plans += carton3d_g((i * 200, 150 - 72 - h_ * 145 - 900 * (1 - min(d, 1)), k_ * 190), 180, ay=20)
        scene3d(c, cam, plans)
        titre(c, t, "À L'UNITÉ", "OU EN QUANTITÉ", T_UNITE - 0.05, t1, y=400, t2=T_QTE - 0.05, e1="ressort", e2="ressort")
        b = entre(t, T_GERE - 0.1, 0.45, 2.2)
        if b > 0: pill(c, "On gère les deux", 540, 1290, 34, "grad", "check", borne(b * 3), mix(0.4, 1, b), rot=-2)


# ─────────────────────────────────────────── 8. enregistre la vidéo
def scene_save(c, t):
    t0, t1 = T_SAVE - 0.12, T_COMM - 0.12
    g = Groupe(c, t, t0, t1, ent="grand", sor="gauche", d_in=0.3, d_out=0.28)
    if not g.visible: return
    with g:
        a = entre(t, t0, 0.5, 1.6)
        tap = T_VIDEO + 0.05
        rempli = prog(t, tap, 0.25, sortie)
        ap = prog(t, tap - 0.06, 0.06, sortie) * (1 - prog(t, tap + 0.05, 0.14, sortie))
        c.save(); c.translate(540, 980); s_ = mix(0.4, 1, a) * (1 - 0.08 * ap) * (1 + 0.1 * battement(t, tap, 1, 0.4) - 0.1)
        c.scale(s_, s_); c.rotate(4 * math.sin(t * 1.6))
        p = skia.Paint(AntiAlias=True, Color=hexa(BLEU, 0.5 + 0.3 * rempli), MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, 40))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-210, -210, 420, 420), 100, 100), p)
        verre(c, -210, -210, 420, 420, 100)
        # le signet : contour, puis plein
        pth = skia.Path(); pth.moveTo(-80, -120); pth.lineTo(80, -120); pth.lineTo(80, 130); pth.lineTo(0, 70); pth.lineTo(-80, 130); pth.close()
        if rempli > 0:
            c.save(); c.clipRect(skia.Rect.MakeXYWH(-90, 140 - 270 * rempli, 180, 270 * rempli))
            c.drawPath(pth, pgrad(-80, -120, 80, 130, ["#FFD86B", "#FFC53D"])); c.restore()
        c.drawPath(pth, peinture("#FFFFFF", 1, Style=skia.Paint.kStroke_Style, StrokeWidth=10, StrokeJoin=skia.Paint.kRound_Join))
        c.restore()
        cu = prog(t, tap - 0.45, 0.4, sortie)
        if cu > 0:
            curseur(c, mix(900, 600, cu), mix(1450, 1040, cu), 1.3, 1 - prog(t, tap + 0.4, 0.25), ap)
            clic(c, 590, 1030, t, tap)
        if t > tap: eclats(c, 540, 980, t, tap + 0.02, 16, 480, cols=["#FFC53D", "#FFFFFF", GLACIER], graine=14)
        titre(c, t, "ENREGISTRE", "LA VIDÉO", T_SAVE - 0.05, t1, y=400, t2=T_VIDEO - 0.05, e1="ressort", e2="masque")


# ─────────────────────────────────────────── 9. commente / message privé, puis le logo
def scene_fin(c, t):
    t0 = T_COMM - 0.12
    if t < t0: return
    fin = prog(t, T_FIN - 0.1, 0.4, entreeSortie)
    with Calque(c, 1 - fin):
        a = entre(t, t0, 0.5, 1.5)
        cam = Cam(ax=-10 + 3 * math.sin(t), ay=mix(-30, 10, a) + 4 * math.sin(t * 0.8), tz=mix(800, 40, a), cy=980)
        W_, H_ = 860, 320
        def commentaire(cc, w, h):
            verre(cc, 0, 0, w, h, 44)
            disque(cc, 80, 90, 42, "#1A2550"); icone(cc, "user-round", 80, 90, 44, GLACIER, 2.2)
            texte(cc, "Toi", 144, 56, 28, "#A9B4D4", "demi", track=0)
            s = "Je cherche…"
            n = int(borne((t - T_COMMENT) / 0.45) * len(s) + 0.999) if t > T_COMMENT else 0
            texte(cc, s[:n], 144, 96, 40, "#FFFFFF", "titre", track=-0.01)
            if int(t * 3) % 2 == 0: rrect(cc, 148 + largeur(s[:n], 40, "titre", -0.01), 98, 4, 44, 2, GLACIER)
            icone(cc, "heart", w - 70, 90, 40, "#FF5A73", 2.6)
            rrect(cc, 40, 200, w - 80, 2, 1, "#2B3454")
            texte(cc, "Répondre", 144, 222, 24, "#8F99BA", "demi", track=0)
        def message(cc, w, h):
            verre(cc, 0, 0, w, h, 44)
            tuile(cc, "send", 90, h / 2, 96, "grad")
            texte(cc, "Écris-moi", 170, h / 2 - 54, 44, "#FFFFFF", "titre", track=-0.02)
            texte(cc, "en message privé", 170, h / 2 + 2, 40, GLACIER, "titre", track=-0.02)
        m = prog(t, T_ECRIS - 0.2, 0.6, entreeSortie)
        plans = [Plan(coins((0, mix(-80, -260, m), mix(0, 200, m)), W_, H_, ax=0), W_, H_, commentaire, 1 - 0.3 * m)]
        if m > 0:
            plans.append(Plan(coins((0, mix(400, 120, m), mix(600, -60, m)), W_, H_), W_, H_, message, borne(m * 3)))
        scene3d(c, cam, plans)
        pv = entre(t, T_PRIVE - 0.1, 0.4, 2.4)
        if pv > 0: eclats(c, 540, 1100, t, T_PRIVE, 12, 380, graine=15)
        titre(c, t, "DIS-MOI EN", "COMMENTAIRE", T_COMM - 0.05, T_ECRIS - 0.15, y=400, t2=T_COMMENT - 0.05)
        titre(c, t, "OU ÉCRIS-MOI", "EN PRIVÉ", T_ECRIS - 0.15, T_FIN, y=400, t2=T_PRIVE - 0.1)
    if fin > 0:
        d = entre(t, T_FIN - 0.05, 0.6, 1.5)
        glace.panneau_givre(c, 150, 640, 780, 620, borne(d * 3), t)
        rayons(c, 540, 950, t, 800, 0.08 * borne(d), 16, GLACIER)
        iw, ih = taille_img(LOGO); lw = 560 * mix(0.6, 1, d)
        image(c, LOGO, 540 - lw / 2, 900 - lw * ih / iw / 2, lw, borne(d * 3))
        b = prog(t, T_FIN + 0.2, 0.4, sortie)
        if b > 0: texte(c, "Ton équipe sur place, en Chine", 540, 1060 + 20 * (1 - b), 40, "#FFFFFF", "titre", "centre", -0.02, b)


# ─────────────────────────────────────────── sons
son(0.0, "whoosh_bas", -8); son(0.15, "impact_doux", -9)
son(T_CHINE - 0.15, "montee", -12); son(T_CHINE, "pop", -9); son(T_CHINE + 0.05, "ding", -14)
son(T_METIER - 0.1, "whoosh_long", -9); son(T_DY - 0.2, "impact", -6); son(T_DY - 0.15, "ching", -10)
son(T_ABO - 0.15, "whoosh", -9); son(T_EXPL + 0.15, "clic", -6); son(T_EXPL + 0.2, "check", -10)
for j in range(5): son(T_EXPL + 0.22 + 0.08 * j, "blip", -18)
for tk in (T_BASK, T_VET, T_ELEC, T_MONT): son(tk - 0.15, "whoosh_court", -11); son(tk - 0.05, "pop", -10)
son(T_TOUT - 0.25, "whoosh_long", -9); son(T_TEL - 0.1, "impact_doux", -9)
son(T_CHERCHE - 0.12, "swipe", -10); son(T_CHERCHE, "message_in", -10)
son(T_ENVOIE + 0.1, "whoosh_court", -10); son(T_ENVOIE + 0.15, "message_in", -11)
son(T_TROUVE - 0.3, "whoosh", -9); son(T_TROUVE, "montee", -12); son(T_TROUVE - 0.05, "message_in", -12)
son(T_FOURN - 0.12, "pop", -10); son(T_VALID, "check", -9); son(T_VALID + 0.05, "ching", -12)
son(T_SELON - 0.12, "swipe", -10)
for k in range(3): son(T_SELON + 0.1 + 0.12 * k, "pop", -12)
son(T_PLUS - 0.2, "whoosh_court", -11); son(T_QUAL - 0.1, "pop", -11)
son(T_PRIX - 0.15, "whoosh", -9); son(T_LIVR - 0.1, "tampon", -8); son(T_LIVR, "ching", -10)
son(T_COMPTE - 0.12, "whoosh_long", -9); son(T_HUIT - 0.1, "impact_doux", -9)
for i in range(4): son(T_JOURS - 0.25 + 0.1 * i, "blip", -16)
son(T_FR - 0.1, "pop", -11); son(T_BE - 0.1, "pop", -11); son(T_TOI + 0.2, "ding", -12); son(T_AIL - 0.1, "pop", -11)
son(T_UNITE - 0.12, "whoosh", -9); son(T_UNITE + 0.2, "impact_doux", -9)
for i in range(10): son(T_QTE - 0.05 + 0.06 * i, "tampon" if i % 3 == 0 else "pop", -16)
son(T_GERE - 0.1, "check", -10)
son(T_SAVE - 0.12, "whoosh", -9); son(T_VIDEO + 0.05, "clic", -6); son(T_VIDEO + 0.1, "ching", -9)
son(T_COMM - 0.12, "swipe", -10)
for i in range(11): son(T_COMMENT + i * 0.04, "frappe", -18)
son(T_ECRIS - 0.2, "whoosh_court", -10); son(T_PRIVE, "message_in", -9)
son(T_FIN - 0.1, "whoosh_long", -8); son(T_FIN + 0.05, "impact", -6); son(T_FIN + 0.1, "verre", -10)
son(DUREE - 1.0, "ding", -16)
for a, b in [(0.0, 0.3), (T_METIER - 0.1, T_METIER + 0.3), (T_ABO - 0.15, T_ABO + 0.2), (T_CAT - 0.12, T_CAT + 0.2), (T_TOUT - 0.25, T_TOUT + 0.3),
             (T_CHERCHE - 0.12, T_CHERCHE + 0.2), (T_TROUVE - 0.3, T_TROUVE + 0.3), (T_SELON - 0.12, T_SELON + 0.2), (T_COMPTE - 0.12, T_COMPTE + 0.3),
             (T_UNITE - 0.12, T_UNITE + 0.2), (T_SAVE - 0.12, T_SAVE + 0.2), (T_COMM - 0.12, T_COMM + 0.2), (T_FIN - 0.1, T_FIN + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T_DY - 0.2, "#FFFFFF", 0.22), (T_VALID, GLACIER, 0.1), (T_LIVR, "#FFFFFF", 0.14), (T_VIDEO + 0.05, "#FFFFFF", 0.18), (T_FIN + 0.05, "#FFFFFF", 0.22)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    _T[0] = t
    glace.fond_glace(c, t, battement(t, T_DY - 0.2, 1, 0.5) - 1)
    scene_hook(c, t)
    with Balance(c, t, 0.8):
        scene_abo(c, t); scene_catalogue(c, t); scene_photo(c, t); scene_qualites(c, t); scene_livraison(c, t); scene_quantite(c, t); scene_save(c, t)
    scene_fin(c, t)
    filigrane(c, t)
    K.dessine_eclairs(c, t)
    if t < T_FIN - 0.1: SOUS.dessine(c, t, "#FFFFFF")
