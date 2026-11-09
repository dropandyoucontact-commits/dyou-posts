"""Identité de la chaîne d'actu people / cinéma / séries / sport — v3 NOIRE, 28/10/2026.

AC-M01 v3 (papier crème) a été validée sur la voix, l'écriture et le montage — « c'est parfait,
la dernière vidéo, la voix, tout ». Seul l'habillage change, et il se **fige** ici : c'est son
associé qui tient @recto_cerveau et qui a tranché (Youssef, 28/10/2026) :

    « fond noir, la grille qui bouge, accent en rouge et blanc, le texte et les médias plus grands,
      juste en changeant la signature visuelle, comme ça on la fige »

D'où le parti pris définitif de la chaîne :

  - **le décor est une pièce, pas un fond** : un sol quadrillé ROUGE qui fuit vers un point de
    fuite et qui avance vers nous, un quadrillage de plafond BLANC qui lui répond. Tout est posé
    DANS cette pièce. C'est ce mouvement lent « qui approche » qui tient l'œil.
  - **noir, blanc, un seul rouge.** Rien d'autre. Pas de dégradé de couleur, pas de verre,
    pas de violet : le portefeuille sombre+violet (DROP&YOU, ChinaBook, DYOU) ne doit jamais
    être confondu avec cette chaîne, et inversement.
  - **sur noir, une ombre ne dit rien** : ce qui ancre un objet au sol, c'est une LUEUR rouge.
    Les cartes ne portent pas une ombre mais un halo.
  - **typo énorme en capitales, blanche**, un mot en rouge par écran, surligneur rouge avec le
    mot en blanc par-dessus, et des mots barrés quand on corrige une idée reçue.
  - **les photos et les extraits arrivent du fond** : petits au point de fuite, ils grandissent
    jusqu'à nous. La profondeur raconte : ce qui arrive vient du fond, ce qui part y repart.

    from people import *
    fond_grille(c, t)                           # toujours, en premier
    rubrique(c, t, a, "DISPARITION")
    titre(c, "SA VOIX,", Y_T1, 120, t, t0, rouge=True)
    carte_photo(c, t, "photo", x, y, w, h, u, profondeur=z)
    signature_people(c, t, T_FIN - 2.4, MEDIAS)

Grille de mise en page (zone sûre TikTok / Snap du 17/10/2026), identique dans toutes les vidéos :
  rubrique 220 · titre1 330 · titre2 460 · visuel 580-1120 · info1 1180 · info2 1300
  sous-titres 1410 (réservé) · RIEN sous 1480.
"""
import math
import numpy as np
import skia
import moteur
from moteur import *

# ───────────────────────────── nom de la chaîne (une ligne à changer)
NOM_CHAINE = "RECTO CERVEAU"
BASELINE = "Films · Séries · Actu people"
LOGO = "logo-recto-cerveau"          # 900 × 179, fabriqué par outils/logo_people.py

# ───────────────────────────── palette : noir, blanc, un rouge. Rien d'autre.
FOND, FOND2, FOND3 = "#08080A", "#101014", "#1A1A21"
BLANC, BLANC2 = "#FFFFFF", "#9B9BA8"
NOIR = "#0A0A0C"                     # l'encre, quand on écrit SUR du blanc ou du rouge clair
ROUGE, ROUGE2 = "#E8252D", "#FF6152"
GRIS = "#50505E"                     # la seule nuance autorisée : fonds de jauge, lignes mortes

# aliases rétro-compatibles : les scènes déjà écrites parlent encore papier/encre
PAPIER, PAPIER2, PAPIER3 = FOND, FOND2, BLANC
ENCRE, ENCRE2 = BLANC, BLANC2
BRUN, SABLE = ROUGE, GRIS
BLEU = "#1F4E79"

# ───────────────────────────── grille de page
AXE = 500          # axe du contenu SOUS y 816 : la colonne de boutons TikTok mord à droite
AXE_HAUT = 540     # au-dessus de y 816 il n'y a aucun bouton : on utilise toute la largeur
Y_RUB, Y_T1, Y_T2, Y_VIS, H_VIS, Y_I1, Y_I2, Y_SOUS = 220, 330, 460, 590, 540, 1180, 1300, 1410
LARG_T = 950       # valeur validée en v3 : au-delà, les bords partent dans le rognage de TikTok
LARG_BAS = 715     # tout ce qui passe sous y 816 reste à l'écart des boutons (x > 860)

HORIZON = 700.0                # hauteur du point de fuite
SOL = 1180.0                   # constante de fuite du sol : y = HORIZON + SOL / z


# ═════════════════════════════ le décor : une pièce quadrillée en perspective
def _grain(c, t):
    """grain d'image : un bruit clair et fixe, pour que le noir ne soit pas un aplat mort"""
    rng = np.random.default_rng(11)
    p = peinture(BLANC, 0.035)
    for x, y, r in rng.uniform([0, 0, 0.8], [W, H, 2.2], size=(520, 3)):
        c.drawCircle(float(x), float(y), float(r), p)


_GRAIN = None


def fond_grille(c, t, pulse=0.0, vitesse=0.55, densite=1.0):
    """noir + sol quadrillé ROUGE qui avance vers nous + plafond BLANC + halo rouge au point de fuite.

    vitesse : lignes de sol franchies par seconde (le décor avance toujours un peu — c'est ce
    mouvement lent « qui approche » qui tient l'œil sans voler la vedette au sujet)."""
    global _GRAIN
    c.clear(hexa(FOND))
    # le fond s'éclaire très légèrement vers l'horizon : la pièce a une profondeur, pas un aplat
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeRadial(skia.Point(AXE, HORIZON), H * 0.80,
                                               [hexa(FOND3, 1.0), hexa(FOND2, 1.0), hexa(FOND, 1.0)],
                                               [0.0, 0.40, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)

    phase = (t * vitesse) % 1.0
    # ── sol : lignes rouges qui se resserrent vers l'horizon et avancent vers nous
    for k in range(1, 17):
        z = k - phase
        if z <= 0.35: continue
        y = HORIZON + SOL / z
        if y > H + 40: continue
        a = 0.66 * min(1.0, (z - 0.3) / 1.6) * densite        # les plus proches s'effacent
        a *= min(1.0, (y - HORIZON) / 60)
        trait(c, -60, y, W + 60, y, ROUGE, max(1.8, 5.4 / z), a)
    # ── sol : fuyantes, qui convergent vers le point de fuite
    for k in range(-9, 10):
        x_sol = AXE + k * 320
        a = 0.40 * densite * (1 - min(1.0, abs(k) / 11))
        trait(c, AXE + (x_sol - AXE) * 0.045, HORIZON + SOL / 16, x_sol, H + 200, ROUGE, 3.2, a)
    # ── plafond : le même quadrillage en blanc, discret, qui répond en haut
    for k in range(1, 11):
        z = k - phase
        if z <= 0.4: continue
        y = HORIZON - SOL * 0.62 / z
        if y < -40: continue
        trait(c, -60, y, W + 60, y, BLANC, max(1.2, 3.4 / z),
              0.17 * densite * min(1.0, (z - 0.35) / 1.8))
    for k in range(-6, 7):
        x_h = AXE + k * 360
        trait(c, AXE + (x_h - AXE) * 0.05, HORIZON - SOL * 0.62 / 10, x_h, -200, BLANC,
              2.2, 0.14 * densite * (1 - min(1.0, abs(k) / 8)))

    # ── halo rouge au point de fuite : la pièce a une source de lumière, et elle bat
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(AXE, HORIZON), 560,
                                               [hexa(ROUGE, 0.30 * (1 + 0.35 * pulse)), hexa(ROUGE, 0.0)]))
    c.drawCircle(AXE, HORIZON, 560, p)

    if _GRAIN is None:
        s = surface(); _grain(s.getCanvas(), 0); _GRAIN = s.makeImageSnapshot()
    c.drawImage(_GRAIN, 0, 0)

    v = skia.Paint(AntiAlias=True)
    v.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.82,
                                               [hexa("#000000", 0.0), hexa("#000000", 0.62)], [0.40, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), v)


def echelle_z(z):
    """facteur d'échelle d'un objet placé à la profondeur z (1 = au premier plan)"""
    return 1.0 / max(0.25, z)


def pose_sol(c, cx, y_bas, w, a=0.28):
    """lueur rouge au sol sous un objet. Sur noir une ombre ne dit rien : c'est le halo qui
    ancre l'objet dans la pièce et qui fait qu'il n'a pas l'air collé sur un fond."""
    rx = max(24.0, w * 0.62)
    ry = max(8.0, w * 0.105)
    yy = y_bas + 8
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, yy), rx,
                                               [hexa(ROUGE, min(0.62, a * 2.0)), hexa(ROUGE, 0.0)]))
    c.save(); c.translate(cx, yy); c.scale(1.0, ry / rx); c.translate(-cx, -yy)
    c.drawCircle(cx, yy, rx, p)
    c.restore()


def _halo(c, rr, a=0.30, flou=24, couleur=None):
    """le halo d'une carte : à la place de l'ombre portée, qui est invisible sur noir"""
    p = skia.Paint(AntiAlias=True, Color=hexa(couleur or ROUGE, a),
                   MaskFilter=skia.MaskFilter.MakeBlur(skia.kOuter_BlurStyle, flou))
    c.drawRRect(rr, p)


# ═════════════════════════════ les photos : elles arrivent du fond de la pièce
def carte_photo(c, t, nom, x, y, w, h, u=1.0, alpha=1.0, flou=0.0, zoom=1.0, fy=0.42,
                detoure=False, liseré=True, z0=5.0, rot=0.0):
    """une photo de star, posée dans la pièce : elle vient du point de fuite (petite) et grandit.

    u : 0 → au loin, 1 → en place. z0 : profondeur de départ."""
    if alpha <= 0.01 or u <= 0.005: return
    cx, cy = x + w / 2, y + h / 2
    z = mix(z0, 1.0, sortieExpo(borne(u)))
    s = echelle_z(z)
    # elle part du point de fuite et glisse jusqu'à sa place
    px = mix(AXE, cx, sortieExpo(borne(u)))
    py = mix(HORIZON, cy, sortieExpo(borne(u)))
    c.save(); c.translate(px, py); c.rotate(rot * (1 - u)); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, alpha * borne(u * 3)):
        pose_sol(c, cx, y + h, w, 0.26)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 10, 10)
        _halo(c, rr, 0.30, 26)
        c.drawRRect(rr, peinture(FOND2))
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 9, y + 9, w - 18, h - 18), 4, 4), doAntiAlias=True)
        if flou > 0.02:
            c.saveLayer(skia.Rect.MakeXYWH(x - 60, y - 60, w + 120, h + 120),
                        skia.Paint(ImageFilter=skia.ImageFilters.Blur(34 * flou, 34 * flou)))
        if detoure:
            iw, ih0 = taille_img(nom)
            ih = ih0 / iw * (w - 18)
            image(c, nom, x + 9, y + h - 9 - ih, w - 18)
        else:
            image_cover(c, nom, x + 9, y + 9, w - 18, h - 18,
                        zoom * (1 + 0.02 * math.sin(t * 0.5)), 0.5, fy, rayon=4)
        if flou > 0.02: c.restore()
        c.restore()
        if liseré:
            c.drawRRect(rr, peinture(BLANC, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    c.restore()


def carte_video(c, t, nom, x, y, w, h, u=1.0, alpha=1.0, t0=0.0, vitesse=1.0, z0=4.0, rogne=(0.0, 0.0, 0.0, 0.0)):
    """un extrait réel (interview, scène, plateau) posé dans la pièce, même grammaire que carte_photo.

    Les sources d'archive sont souvent en 640×360 : on les montre en cadre 16:9 LARGE plutôt que
    recadrées en portrait, sinon l'agrandissement se voit. Jamais de ralenti (vitesse ≥ 1)."""
    if alpha <= 0.01 or u <= 0.005: return
    cx, cy = x + w / 2, y + h / 2
    z = mix(z0, 1.0, sortieExpo(borne(u)))
    sc = echelle_z(z)
    px = mix(AXE, cx, sortieExpo(borne(u)))
    py = mix(HORIZON, cy, sortieExpo(borne(u)))
    c.save(); c.translate(px, py); c.scale(sc, sc); c.translate(-cx, -cy)
    with Calque(c, alpha * borne(u * 3)):
        pose_sol(c, cx, y + h, w, 0.26)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 10, 10)
        _halo(c, rr, 0.32, 28)
        c.drawRRect(rr, peinture(FOND2))
        video(c, nom, x + 9, y + 9, w - 18, h - 18, max(0.0, t - t0), vitesse, rayon=4, rogne=rogne)
        c.drawRRect(rr, peinture(BLANC, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    c.restore()


# ═════════════════════════════ typographie
def titre(c, txt, y, taille, t, t0, rouge=False, alpha=1.0, effet="masque", decal=0.02, couleur=None):
    """le titre de la chaîne : capitales ultra-grasses blanches, un seul mot en rouge.

    Au-dessus de y 816 on prend toute la largeur (aucun bouton TikTok à cette hauteur) ;
    en dessous on se recale sur l'axe 500 et on se limite à LARG_BAS."""
    from studio import lettres
    haut = y < 775
    larg = LARG_T if haut else LARG_BAS
    cx = AXE_HAUT if haut else AXE
    ts = ajuste(txt, larg, taille, "noir", -0.022)
    lettres(c, txt, cx, y, ts, t, t0, effet, grad=False,
            couleur=couleur or (ROUGE if rouge else BLANC), decal=decal, track=-0.022, alpha=alpha)


def titre_mixte(c, lignes, y0, taille, t, t0, interligne=None, decal=0.02, effet="masque"):
    """plusieurs lignes d'un coup : [(texte, rouge?), ...] — chaque ligne part 0,1 s après la précédente"""
    ts = min(ajuste(txt, LARG_T, taille, "noir", -0.03) for txt, _ in lignes)
    il = interligne if interligne is not None else ts * 1.12
    for k, (txt, rouge) in enumerate(lignes):
        titre(c, txt, y0 + k * il, ts, t, t0 + 0.1 * k, rouge, effet=effet, decal=decal)
    return y0 + len(lignes) * il


def _cadre(y):
    return (LARG_T, AXE_HAUT) if y < 775 else (LARG_BAS, AXE)


def barre_rouge(c, txt, y, taille, u, fam="noir"):
    """trait rouge qui raye un mot : on corrige une idée reçue"""
    if u <= 0.01: return
    larg, cx = _cadre(y)
    ts = ajuste(txt, larg, taille, fam, -0.022)
    w = largeur(txt, ts, fam, -0.022)
    yy = y + hauteurLigne(ts, fam) * 0.52
    trait(c, cx - w / 2 - 10, yy, cx - w / 2 - 10 + (w + 20) * borne(u), yy, ROUGE, max(6, ts * 0.09))


def surlignage(c, txt, y, taille, u, couleur=ROUGE, fam="noir"):
    """bloc rouge qui se déroule derrière un mot — le mot passe en BLANC par-dessus"""
    if u <= 0.01: return
    larg, cx = _cadre(y)
    ts = ajuste(txt, larg, taille, fam, -0.022)
    w = largeur(txt, ts, fam, -0.022)
    h = hauteurLigne(ts, fam) * 0.82
    rrect(c, cx - w / 2 - 16, y + h * 0.16, (w + 32) * borne(u), h, 4, couleur, 1.0)


# ═════════════════════════════ habillage éditorial
def rubrique(c, t, a, libelle, gauche="DÉCODER"):
    """micro-typo en haut + filet : la signature de la chaîne, présente du début à la fin"""
    if a <= 0.01: return
    with Calque(c, a):
        s = f"{gauche} / {libelle.upper()}"
        texte(c, s, 90, Y_RUB, 30, BLANC, "fort", "gauche", 0.22, 0.9)
        trait(c, 90, Y_RUB + 48, 990, Y_RUB + 48, BLANC, 3, 0.40)
        disque(c, 990, Y_RUB + 48, 8, ROUGE, 0.4 + 0.6 * (0.5 + 0.5 * math.cos(t * 5)))


def bloc(c, label, cx, cy, u, a=1.0, taille=48, couleur=None, encre=None, rot=0.0):
    """pavé plein : un fait marquant, posé dans la pièce avec sa lueur.

    Pavé BLANC → texte noir ; pavé ROUGE → texte blanc. C'est tout le contraste de la chaîne."""
    if u <= 0.01 or a <= 0.01: return
    couleur = couleur or BLANC
    if encre is None:
        encre = BLANC if couleur in (ROUGE, ROUGE2) else NOIR
    ts = ajuste(label, 630, taille, "noir", -0.02)   # 470 bridait : tous les pavés sortaient à la même taille
    w, h = largeur(label, ts, "noir", -0.02) + 64, ts * 1.86
    c.save(); c.translate(cx, cy + mix(-70, 0, u)); c.rotate(rot); c.scale(mix(0.8, 1, u), mix(0.8, 1, u))
    with Calque(c, a * borne(u * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 6, 6)
        _halo(c, rr, 0.26, 18, ROUGE if couleur in (ROUGE, ROUGE2) else BLANC)
        rrect(c, -w / 2, -h / 2, w, h, 6, couleur, 1.0)
        texte(c, label, 0, -hauteurLigne(ts, "noir") / 2, ts, encre, "noir", "centre", -0.02)
    c.restore()


def legende(c, lignes, x, y, u, taille=38):
    """légende d'un graphique : carré de couleur + libellé, qui s'empile"""
    for k, (carre, lab) in enumerate(lignes):
        a = borne((u - 0.18 * k) * 3)
        if a <= 0.01: continue
        yy = y + k * (taille * 1.75)
        with Calque(c, a):
            rrect(c, x, yy, taille * 0.78, taille * 0.78, 3, carre, 1.0)
            texte(c, lab, x + taille * 1.25, yy - hauteurLigne(taille, "fort") * 0.5 + taille * 0.39,
                  taille, BLANC, "fort", track=-0.01)


def donut(c, cx, cy, r, u, parts, t, ep=52, graduations=20):
    """jauge graduée qui se remplit — la brique data de la chaîne.
    parts : [(fraction, couleur), ...] cumulées dans l'ordre."""
    anneau(c, cx, cy, r, GRIS, ep, 0.50)
    for k in range(graduations + 1):
        a = -math.pi / 2 + k / graduations * 2 * math.pi
        l = 18 if k % 5 == 0 else 10
        trait(c, cx + math.cos(a) * (r + ep / 2 + 8), cy + math.sin(a) * (r + ep / 2 + 8),
              cx + math.cos(a) * (r + ep / 2 + 8 + l), cy + math.sin(a) * (r + ep / 2 + 8 + l),
              BLANC, 2.5, 0.55)
    deb = -90.0
    for frac, col in parts:
        bal = 360 * frac * borne(u)
        if bal <= 0.2: continue
        p = skia.Paint(AntiAlias=True, Color=hexa(col), Style=skia.Paint.kStroke_Style, StrokeWidth=ep)
        c.drawArc(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), deb, bal, False, p)
        deb += bal
    # repère de fin de course : une pastille POSÉE SUR L'ANNEAU, jamais une aiguille qui
    # traverse le centre — elle passait sur les chiffres du compteur (Youssef, 27/10/2026)
    a = math.radians(deb)
    px, py = cx + math.cos(a) * r, cy + math.sin(a) * r
    disque(c, px, py, ep * 0.42, BLANC)
    anneau(c, px, py, ep * 0.42, ROUGE, 5)


def compteur(c, valeur, suffixe, cx, cy, u, taille=120, a=1.0, couleur=None, sous=None):
    """nombre qui monte de 0 à valeur, avec sa légende en micro-typo"""
    if a <= 0.01 or u <= 0.004: return          # jamais figé sur « 0 » : ça se lit comme une erreur
    from kit import texte_centre
    n = max(1, int(round(valeur * sortieExpo(borne(u)))))
    with Calque(c, a):
        texte_centre(c, f"{n:,}".replace(",", " ") + suffixe, cx, cy, taille, couleur or BLANC, "noir")
        if sous:
            texte(c, sous.upper(), cx, cy + taille * 0.42, 28, BLANC2, "fort", "centre", 0.2)


def document(c, t, lignes, cx, cy, w, u, titre_doc=None, rot=-3.0):
    """coupure de presse posée en perspective — la preuve qu'on montre. Elle reste BLANCHE :
    c'est du papier, et sur le noir c'est elle qui crève l'écran.
    Largeur plafonnée à 720 : au-delà, le cadre mord sur la colonne de boutons de TikTok
    (x > 860 entre y 816 et 1555) même si le texte, lui, tient."""
    if u <= 0.01: return
    w = min(w, 700)
    h = w * 0.40
    c.save(); c.translate(cx, cy)
    with Espace(c, 0, 0, rx=16, ry=-8, s=mix(0.86, 1, sortieExpo(u))):
        c.rotate(rot)
        with Calque(c, borne(u * 3)):
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 2, 2)
            _halo(c, rr, 0.30, 26, BLANC)
            c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), peinture(BLANC))
            y = -h / 2 + 28
            if titre_doc:
                texte(c, titre_doc.upper(), -w / 2 + 30, y, 30, ROUGE, "noir", track=0.18)
                y += 50
            for ligne in lignes:
                ts = ajuste(ligne, w - 60, 46, "fort", -0.01)
                texte(c, ligne, -w / 2 + 30, y, ts, NOIR, "fort", track=-0.01)
                y += ts * 1.34
    c.restore()


def bandes(c, t, images, u, y=Y_VIS, h=H_VIS):
    """écran divisé : 1, 2 ou 3 bandes qui arrivent l'une après l'autre"""
    n = len(images)
    larg = 820 / n
    for k, (nom, fy) in enumerate(images):
        a = borne((u - 0.22 * k) * 2.2)
        if a <= 0.01: continue
        x = 100 + k * larg
        with Calque(c, a):
            c.save()
            c.clipRect(skia.Rect.MakeXYWH(x, y, larg - 8, h * borne(a * 1.4)))
            image_cover(c, nom, x, y, larg - 8, h, 1.12, 0.5, fy)
            c.restore()
            c.drawRect(skia.Rect.MakeXYWH(x, y, larg - 8, h), peinture(BLANC, 0.9,
                       Style=skia.Paint.kStroke_Style, StrokeWidth=3))


def filigrane(c, a=0.26):
    """le nom de la chaîne, discret, dans la zone sûre"""
    if a <= 0.01: return
    texte(c, NOM_CHAINE, 110, 1498, 30, BLANC2, "noir", "gauche", 0.2, a)


# ═════════════════════════════ signature de fin, propre à la chaîne
def signature_people(c, t, t0, medias=(), phrase=BASELINE):
    """Le logo arrive du fond de la pièce — le même langage que tout le reste : la profondeur
    raconte. Flash rouge, ondes au sol, le logo fonce vers nous en 3D, se pose, le filet se
    déroule, la baseline arrive."""
    u = t - t0
    if u < -0.05: return
    from studio import rayons

    fl = 1 - u / 0.2                                   # flash rouge court
    if 0 < fl <= 1:
        c.drawRect(skia.Rect.MakeWH(W, H), peinture(ROUGE, 0.46 * fl * fl))

    for k in range(5):                                 # ondes au sol depuis le point de fuite
        v = borne((u - 0.05 * k) / 0.9)
        if v <= 0 or v >= 1: continue
        z = mix(6.0, 0.6, v ** 1.4)
        y = HORIZON + SOL / z
        rx = 1500 / z
        c.drawOval(skia.Rect.MakeXYWH(AXE - rx, y - rx * 0.2, 2 * rx, 0.4 * rx),
                   peinture(ROUGE, 0.62 * (1 - v) ** 0.6, Style=skia.Paint.kStroke_Style,
                            StrokeWidth=4 + 20 * (1 - v)))

    rayons(c, AXE, 880, t, 1100, 0.17 * borne(u / 0.16), 18, ROUGE)   # plein tout de suite

    av = prog(t, t0 + 0.02, 0.62, lambda v: ressort(v, 1.1, 5.0))    # le logo vient du fond, vite :
    # à 0,8 s il restait minuscule une demi-seconde et l'écran passait pour vide
    if av > 0:
        z = mix(7.0, 1.0, min(av, 1.06))
        s_ = echelle_z(z)
        py = mix(HORIZON, 880, min(av, 1.0))
        iw, ih = taille_img(LOGO)
        LW = 870.0
        LH = LW * ih / iw
        c.save(); c.translate(AXE, py); c.scale(s_, s_)
        with Espace(c, 0, 0, ry=mix(70, 0, min(av, 1.04)), rx=mix(-14, 0, min(av, 1.04)), s=1.0):
            with Calque(c, borne(av * 4)):
                pose_sol(c, 0, LH * 0.62, LW * 0.42, 0.24)
                image(c, LOGO, -LW / 2, -LH / 2, LW)
        c.restore()

    b = prog(t, t0 + 0.75, 0.4, sortie)                # filet rouge
    if b > 0:
        lw = 680 * b
        rrect(c, AXE - lw / 2, 1015, lw, 7, 3, ROUGE, 1.0)
    b2 = prog(t, t0 + 0.95, 0.4, sortie)               # baseline
    if b2 > 0:
        texte(c, phrase, AXE, 1070 + 20 * (1 - b2), 50, BLANC, "titre", "centre", -0.02, b2)


def sons_signature_people(son, t0):
    son(t0 - 0.04, "impact", -3)
    son(t0 + 0.02, "whoosh_long", -7)
    son(t0 + 0.55, "ching", -8)
    son(t0 + 0.78, "swipe", -11)
    son(t0 + 1.0, "pop", -11)


# ═════════════════════════════ sous-titres de la chaîne
def sous_titres_people(K, fusions=None):
    """Plus gros que le réglage commun (`studio.sous_titres`, 50 px) : sur cette chaîne on écoute
    autant qu'on regarde, et Youssef veut le texte plus grand (28/10/2026). 60 px, 4 mots par
    carton, bloc x 140-860 pour rester hors de la colonne de boutons TikTok."""
    from studio import SousTitresEncre
    return SousTitresEncre(K, fusions=fusions, y=1402, larg=720, taille=60,
                           fam="fort", max_mots=4, cx=AXE)
