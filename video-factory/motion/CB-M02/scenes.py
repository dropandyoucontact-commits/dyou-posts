"""CB-M02 « 3 signes que ce n'est pas une usine » — variante courte ChinaBook (22,3 s).

Voix générée par moteur/outils/voix.py (Tomy, 3,5 mots/s) : timing.json vient
directement d'ElevenLabs. Chaque élément cite le mot qu'il illustre (TW(i)).
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *

DUREE = 22.3
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES = K.nb_images
SFX, RAPIDE = K.SFX, K.RAPIDE
flou_a = K.flou_a

# ─────────────────────────────────────────── sous-titres
SOUS = SousTitres(K, [
    [(0, "Si", "", -0.3), (1, "ton"), (2, "fournisseur"), (3, "fait"), (4, "ces"), (5, "3", "g"), (6, "choses,")],
    [(7, "ce"), (8, "n’est"), (9, "pas", "r"), (10, "une"), (11, "usine.", "r")],
    [(12, "1.", "g"), (13, "Il"), (14, "ne"), (15, "te"), (16, "montre"), (17, "jamais", "r"), (18, "l’usine.")],
    [(19, "2.", "g"), (20, "Il"), (21, "refuse", "r"), (22, "de"), (23, "te"), (24, "donner"), (25, "le"), (26, "contact"), (27, "du"), (28, "fabricant.")],
    [(29, "3.", "g"), (30, "Il"), (31, "te"), (32, "répond"), (33, "en"), (34, "français.", "r")],
    [(35, "Résultat :"), (36, "sa"), (37, "marge", "r"), (38, "s’ajoute"), (39, "à"), (40, "chaque"), (41, "commande.")],
    [(42, "Et"), (43, "toi,"), (44, "tu"), (45, "ne"), (46, "le"), (47, "vois", "r"), (48, "même"), (49, "pas.")],
    [(50, "Dans"), (51, "le"), (52, "ChinaBook,", "g"), (54, "j’ai"), (55, "rassemblé")],
    [(56, "les"), (57, "fournisseurs"), (58, "que"), (59, "j’ai"), (60, "testés", "g"), (61, "pendant"), (62, "des"), (63, "mois.")],
    [(64, "Tu"), (65, "les"), (66, "contactes"), (67, "en"), (68, "direct.", "g")],
    [(69, "Envoie-moi"), (70, "« CHINA »", "g"), (71, "sur"), (72, "WhatsApp.")],
    [(None, "Ton", "", 20.86), (None, "accès", "", 20.93), (None, "direct", "g", 21.02), (None, "à", "", 21.12), (None, "la", "", 21.17), (None, "Chine.", "", 21.23)],
])

# ─────────────────────────────────────────── repères temporels
t_trois, t_chute, t_usine = TW(5), TW(9) - 0.02, TW(11)
S1 = (0.0, 3.30)
t_un, t_q1, t_jamais, t_lusine = TW(12), TW(13) - 0.04, TW(17) - 0.04, TW(18) - 0.02
S2 = (3.10, 5.55)
t_deux, t_refuse, t_contact = TW(19), TW(21) - 0.04, TW(26) - 0.04
S3 = (5.35, 8.45)
t_trois2, t_repond, t_francais = TW(29), TW(32) - 0.04, TW(34) - 0.04
S4 = (8.25, 10.45)
t_res, t_ajoute, t_chaque, t_cmd, t_toi, t_vois, t_pas = TW(35), TW(38) - 0.04, TW(40) - 0.04, TW(41) - 0.04, TW(42), TW(47) - 0.04, TW(49) - 0.04
S5 = (10.28, 14.90)
t_logo, t_ras, t_four, t_test, t_mois, t_cont, t_direct = TW(52) - 0.06, TW(55) - 0.04, TW(57) - 0.04, TW(60) - 0.04, TW(63) - 0.06, TW(66) - 0.04, TW(68) - 0.04
S6 = (14.62, 19.42)
TL = [TW(70) - 0.16 + k * 0.07 for k in range(5)]
t_envoi, t_fin = TW(71), 20.82
S7 = (19.30, DUREE)

# ─────────────────────────────────────────── sons, flou, éclairs
for k in range(3): son(t_trois + k * 0.08, "pop", -16 - k)
son(t_chute, "whoosh_bas", -12); son(t_chute + 0.38, "impact", -6); son(t_usine + 0.08, "tampon", -9); son(3.10, "whoosh", -13)
son(3.16, "whoosh_court", -15); son(t_q1, "message", -12); son(t_jamais, "message_in", -11); son(t_jamais + 0.06, "blip", -13); son(t_lusine, "tampon", -9); son(5.35, "whoosh", -13)
son(5.40, "swipe", -15); son(5.62, "pop", -16); son(t_refuse, "tampon", -8); son(t_refuse + 0.06, "blip", -13); son(t_contact, "clic", -9); son(t_contact + 0.1, "blip", -15); son(8.25, "whoosh", -13)
son(8.30, "swipe", -15); son(t_repond, "message_in", -11); son(t_francais - 0.1, "whoosh_court", -14); son(t_francais + 0.04, "blip", -12); son(10.25, "whoosh", -13)
son(10.32, "swipe", -14); son(t_ajoute, "pop", -12); son(t_chaque, "pop", -13); son(t_cmd, "pop", -13)
for k in range(4): son(t_cmd + 0.2 + k * 0.05, "tick", -19)
son(t_vois, "whoosh_court", -16); son(t_vois + 0.25, "tampon", -10); son(14.48, "montee", -14); son(14.68, "whoosh_long", -12)
son(t_logo, "impact", -7); son(t_logo + 0.02, "verre", -8); son(15.52, "whoosh", -14)
for k in range(3): son(t_ras + k * 0.14, "pop", -16)
son(t_test, "check", -12); son(t_mois, "pop", -12); son(t_cont, "clic", -10); son(t_direct, "tampon", -8); son(t_direct + 0.02, "verre", -12); son(19.26, "whoosh", -13)
son(19.33, "pop", -14)
for tl in TL: son(tl, "frappe", -13)
son(t_envoi, "clic", -10); son(t_envoi + 0.04, "whoosh_court", -13); son(t_envoi + 0.16, "message", -10)
son(t_fin, "whoosh", -13); son(t_fin + 0.14, "impact_doux", -8); son(t_fin + 0.16, "verre", -8); son(t_fin + 0.36, "pop", -11)
for a, b in [(t_chute, t_chute + 0.45), (3.10, 3.36), (t_lusine - 0.12, t_lusine + 0.05), (5.35, 5.62), (t_refuse - 0.12, t_refuse + 0.05),
             (8.25, 8.52), (t_francais - 0.12, t_francais + 0.2), (10.25, 10.52), (14.60, 15.0), (15.5, 16.0), (t_direct - 0.12, t_direct + 0.05),
             (19.25, 19.48), (t_envoi, t_envoi + 0.32), (t_fin, t_fin + 0.36)]:
    rapide(a, b)
for t, c_, a in [(t_chute + 0.38, C["rouge"], 0.10), (t_lusine, C["rouge"], 0.08), (t_refuse, C["rouge"], 0.08), (t_francais, C["rouge"], 0.08),
                 (t_direct, C["vert"], 0.11), (t_envoi + 0.1, C["vert"], 0.08), (t_fin + 0.14, C["vert"], 0.10)]:
    eclair(t, c_, a)


def fenetre(t, s, entree_d=0.26, sortie_d=0.2, sens=(-1300, 0)):
    """décalage d'entrée / de sortie d'une scène : arrive de la droite, part vers la gauche"""
    a, b = s
    ue = prog(t, a, entree_d, sortie); us = prog(t, b - sortie_d, sortie_d, entree)
    return 1300 * (1 - ue) + sens[0] * us, sens[1] * us


def gros_numero(c, n, t, t0):
    """grand numéro pâle en fond de scène (la liste se lit même sans le son)"""
    if t < t0 - 0.05: return
    u = prog(t, t0 - 0.05, 0.4, lambda v: rebond(v, 1.6))
    c.save(); c.translate(300, 960); c.rotate(-8); c.scale(mix(0.5, 1, u), mix(0.5, 1, u))
    texte_centre(c, str(n), 0, 0, 520, C["vertDoux"], alpha=borne(u * 2))
    c.restore()


# ═══════════════════════════════════════════ S1 · La façade d'usine en carton
def usine_facade(c, t):
    """façade dessinée autour de son pied (0, 0) : murs, toit en dents de scie, cheminée, enseigne"""
    ink = C["ink"]
    # étai en bois à l'arrière (le décor est en carton)
    trait(c, 250, -300, 390, 0, "#B98B5E", 14)
    c.drawRect(skia.Rect.MakeXYWH(310, -360, 14, 360), peinture("#C9A57E"))
    # cheminée et fumée
    rrect(c, 170, -560, 64, 210, 8, ink)
    for k in range(5):
        ph = (t * 0.55 + k / 5) % 1.0
        disque(c, 202 + 30 * ph + 10 * math.sin(k + t * 2), -570 - 150 * ph, 16 + 34 * ph, "#C9D1CD", 0.75 * (1 - ph))
    # toit en dents de scie
    toit = skia.Path()
    toit.moveTo(-310, -360)
    for k in range(3):
        x0 = -310 + k * 206.7
        toit.lineTo(x0, -450); toit.lineTo(x0 + 206.7, -360)
    toit.close()
    c.drawPath(toit, peinture(C["vertMoyen"]))
    c.drawPath(toit, peinture(ink, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=6, StrokeJoin=skia.Paint.kRound_Join))
    # murs
    rrect(c, -310, -362, 620, 362, 6, "#F2F6F3", 1.0, None, ink, 6)
    # enseigne
    rrect(c, -175, -330, 350, 92, 18, ink)
    texte_centre(c, "USINE", 0, -284, 62, C["blanc"])
    # fenêtres et porte
    for lig in range(2):
        for k in range(4):
            rrect(c, -262 + k * 140, -212 + lig * 92, 100, 62, 8, C["vertDoux"], 1.0, None, ink, 4)
    rrect(c, -60, -118, 120, 118, 8, ink)


def revendeur_bureau(c, t, cx, sol):
    """ce qu'il y a derrière : un bureau, un ordinateur, un petit drapeau, des cartons"""
    # cartons
    for k, (x, y, w, h) in enumerate([(-300, -150, 150, 120), (-280, -260, 120, 110), (175, -130, 130, 110)]):
        rrect(c, cx + x, sol + y, w, h, 10, "#E7D3B5", 1.0, None, "#B98B5E", 4)
        trait(c, cx + x + w / 2, sol + y, cx + x + w / 2, sol + y + h, "#B98B5E", 4)
    # bureau
    rrect(c, cx - 200, sol - 210, 400, 26, 8, C["ink"])
    rrect(c, cx - 180, sol - 186, 20, 186, 6, C["ink"]); rrect(c, cx + 160, sol - 186, 20, 186, 6, C["ink"])
    icone(c, "laptop", cx - 70, sol - 268, 130, C["ink"], 2.0)
    # le revendeur
    disque(c, cx + 90, sol - 330, 74, C["rouge"], 1.0, (10, 24, 0.2))
    icone(c, "user", cx + 90, sol - 330, 84, C["blanc"], 2.4)
    drapeau(c, "FR", cx + 128, sol - 300, 54, 36, 6)


def s1(c, t):
    if not (S1[0] <= t <= S1[1]): return
    dx = -1300 * prog(t, S1[1] - 0.2, 0.2, entree)
    sx, sy = secousse(t, t_chute + 0.38, 18)
    c.save(); c.translate(dx + sx, sy)
    cx, sol = 540, 1250
    # derrière : le vrai décor
    if t >= t_chute:
        revendeur_bureau(c, t, cx, sol)
    # la façade : légère oscillation de décor, puis elle tombe en arrière sur sa base
    chute = prog(t, t_chute, 0.38, entree)
    if chute < 0.999:
        rx = -88 * chute
        rz = 1.4 * math.sin(t * 5.2) * (1 - chute)
        with Espace(c, cx, sol, rx=rx, ry=-10, rz=rz):
            c.save(); c.translate(cx, sol)
            ombre_sol(c, 0, 0, 360, 22, 0.16)
            usine_facade(c, t)
            c.restore()
    else:
        trait(c, cx - 320, sol, cx + 320, sol, C["ink"], 8, 1 - prog(t, t_chute + 0.4, 0.25))
    # poussière à l'impact
    if t >= t_chute + 0.36:
        u = prog(t, t_chute + 0.36, 0.7, sortie)
        for k in range(9):
            a = math.pi * (k / 8)
            disque(c, cx + math.cos(a) * 380 * u * (1 if k % 2 else 0.8) * (-1 if k < 4 else 1), sol - 10 - 60 * u * math.sin(a), 20 + 40 * u, "#D5DBD8", 0.8 * (1 - u))
    tampon(c, "REVENDEUR", cx + 120, sol - 520, t, t_usine + 0.12, 54, C["rouge"], -8)
    c.restore()


# ═══════════════════════════════════════════ la liste des 3 signes (en bas, de 1 à « Résultat »)
SIGNES = [("Usine cachée", None, t_jamais), ("Contact caché", None, t_refuse), ("Parle français", None, t_francais)]


def liste(c, t):
    if t > t_res + 0.4: return
    part = prog(t, t_res - 0.02, 0.32, entree)
    for k, (label, ic, ta) in enumerate(SIGNES):
        t0 = -0.3 + k * 0.08
        u = prog(t, t0, 0.35, lambda v: rebond(v, 1.9)) * battement(t, t_trois + k * 0.08, 0.14)
        if u <= 0: continue
        cx, cy = 210 + k * 330, 1372 + 300 * part
        on = prog(t, ta, 0.25, lambda v: rebond(v, 1.6))
        sx, _ = secousse(t, ta + 0.05, 10, 0.3)
        c.save(); c.translate(cx + sx, cy); c.scale(mix(0.4, 1, u) * battement(t, ta, 0.12), mix(0.4, 1, u) * battement(t, ta, 0.12))
        with Calque(c, borne(u * 2) * (1 - part)):
            w, h = 300, 96
            if on < 1:
                rrect(c, -w / 2, -h / 2, w, h, 26, C["blanc"], 1.0, (10, 24, 0.10))
                p = peinture(C["grisClair"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=4)
                p.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 2, -h / 2 + 2, w - 4, h - 4), 24, 24), p)
                disque(c, -w / 2 + 50, 0, 26, C["fondDoux"])
                texte_centre(c, str(k + 1), -w / 2 + 50, 0, 32, C["grisClair"])
                texte_centre(c, "?", 30, 0, 44, C["grisClair"])
            if on > 0:
                rrect(c, -w / 2, -h / 2, w, h, 26, C["rouge"], on, (12, 28, 0.2))
                with Calque(c, on):
                    disque(c, -w / 2 + 46, 0, 28, C["blanc"])
                    texte_centre(c, str(k + 1), -w / 2 + 46, 0, 34, C["rouge"])
                    lx = -w / 2 + 88
                    taille = ajuste(label, w / 2 - 12 - lx, 34)
                    texte_centre(c, label, (lx + w / 2 - 12) / 2, 0, taille, C["blanc"])
        c.restore()


# ═══════════════════════════════════════════ S2 · Signe 1 : il ne montre jamais l'usine
def ecran_appel(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(C["ink"]))
    texte_centre(c, "Appel vidéo", x + w / 2, y + 70, 22, "#9AA39E", "fort")
    texte_centre(c, "Fournisseur", x + w / 2, y + 108, 30, C["blanc"])
    pulse = 1 + 0.06 * math.sin(t * 6)
    c.save(); c.translate(x + w / 2, y + h * 0.45); c.scale(pulse, pulse)
    disque(c, 0, 0, 86, "#1E2622"); icone(c, "video-off", 0, 0, 96, C["blanc"], 2.0)
    c.restore()
    texte_centre(c, "Caméra désactivée", x + w / 2, y + h * 0.45 + 140, 24, "#C9D1CD", "fort")
    for k, (coul, ic) in enumerate([("#2B3430", "mic"), (C["rouge"], "x"), ("#2B3430", "video-off")]):
        bx = x + w / 2 + (k - 1) * 92
        disque(c, bx, y + h - 90, 34, coul)
        if ic in ("x", "video-off"): icone(c, ic, bx, y + h - 90, 34, C["blanc"], 2.6)


def s2(c, t):
    if not (S2[0] <= t <= S2[1]): return
    dx, _ = fenetre(t, S2)
    c.save(); c.translate(dx, 0)
    gros_numero(c, 1, t, t_un)
    pw, ph = 330, 660
    px, py = 600, 618
    with Espace(c, px + pw / 2, py + ph / 2, ry=-14 + 4 * math.sin(t * 1.4), rz=3):
        telephone(c, px, py, pw, ph, lambda cc, a, b, d, e: ecran_appel(cc, a, b, d, e, t))
    bulle(c, "Tu me montres\nl’usine ?", True, 90, 700, 480, t, t_q1, C["vert"], C["blanc"], 30)
    bulle(c, "Pas possible…", False, 70, 880, 480, t, t_jamais, C["blanc"], C["ink"], 30, (12, 30, 0.16))
    tampon(c, "JAMAIS", 330, 1110, t, t_lusine, 60, C["rouge"], -10, "eye-off")
    c.restore()


# ═══════════════════════════════════════════ S3 · Signe 2 : le contact du fabricant refusé
def s3(c, t):
    if not (S3[0] <= t <= S3[1]): return
    dx, _ = fenetre(t, S3)
    sx, _ = secousse(t, t_contact + 0.06, 14, 0.36)
    c.save(); c.translate(dx, 0)
    gros_numero(c, 2, t, t_deux)
    x, y, w, h = 110, 660, 860, 600
    u = prog(t, S3[0] + 0.05, 0.4, lambda v: rebond(v, 1.4))
    c.save(); c.translate(540, y + h / 2); c.scale(mix(0.85, 1, u), mix(0.85, 1, u)); c.translate(-540, -(y + h / 2))
    carte(c, x, y, w, h, 44, C["blanc"], 1.0, (24, 56, 0.13))
    disque(c, x + 74, y + 74, 36, C["vertDoux"]); icone(c, "factory", x + 74, y + 74, 40, C["vert"], 2.3)
    texte(c, "CONTACT DU FABRICANT", x + 130, y + 52, 26, C["gris"], "fort", track=0.08)
    for k, champ in enumerate(["Nom", "Téléphone", "WeChat"]):
        yy = y + 150 + k * 108
        ur = prog(t, S3[0] + 0.25 + k * 0.1, 0.3, sortie)
        with Calque(c, ur):
            texte(c, champ, x + 50, yy + 10, 32, C["ink"], "fort")
            bx = x + 330 + 30 * (1 - ur)
            rrect(c, bx, yy, 470, 52, 12, C["ink"])
            for q in range(6):
                rrect(c, bx + 20 + q * 52, yy + 14, 38, 24, 5, "#2B3430")
            icone(c, "lock", bx + 430, yy + 26, 32, C["blanc"], 2.6)
    # bouton qui refuse
    by = y + h - 120
    rouge = prog(t, t_contact, 0.15)
    c.save(); c.translate(sx, 0)
    rrect(c, x + 50, by, w - 100, 84, 42, C["vertFonce"] if rouge < 0.5 else C["rouge"])
    icone(c, "lock", x + 112, by + 42, 36, C["blanc"], 2.6)
    texte_centre(c, "Afficher le contact" if rouge < 0.5 else "Accès refusé", 540 + 20, by + 42, 34, C["blanc"])
    c.restore()
    c.restore()
    tampon(c, "REFUSÉ", 700, 760, t, t_refuse, 62, C["rouge"], 8)
    c.restore()


# ═══════════════════════════════════════════ S4 · Signe 3 : il répond en français
def s4(c, t):
    if not (S4[0] <= t <= S4[1]): return
    dx, _ = fenetre(t, S4)
    c.save(); c.translate(dx, 0)
    gros_numero(c, 3, t, t_trois2)
    x, y, w, h = 110, 660, 860, 470
    carte(c, x, y, w, h, 44, "#F6F9F7", 1.0, (24, 56, 0.12))
    rrect(c, x, y, w, 140, 44, C["blanc"]); c.drawRect(skia.Rect.MakeXYWH(x, y + 100, w, 40), peinture(C["blanc"]))
    trait(c, x, y + 140, x + w, y + 140, C["ligne"], 3, rond=False)
    ax, ay = x + 90, y + 70
    disque(c, ax, ay, 44, C["vertDoux"]); icone(c, "factory", ax, ay, 46, C["vert"], 2.3)
    texte(c, "Fournisseur « chinois »", x + 160, y + 34, 34)
    texte(c, "en ligne", x + 160, y + 80, 24, C["vert"], "demi")
    bulle(c, "Bonjour ! Pas de souci,\nje m’occupe de tout. 😉".replace(" 😉", ""), False, x, y + 200, w, t, t_repond, C["blanc"], C["ink"], 36)
    # la loupe démasque l'accent : petit drapeau français sur l'avatar
    if t >= t_francais - 0.14:
        u = prog(t, t_francais - 0.14, 0.3, sortie)
        lx, ly = mix(x + w + 120, ax + 40, u), mix(y + 520, ay + 40, u)
        uf = prog(t, t_francais + 0.08, 0.3, lambda v: rebond(v, 2.0))
        c.save(); c.translate(ax + 34, ay + 30); c.scale(uf, uf); drapeau(c, "FR", -27, -18, 54, 36, 6); c.restore()
        c.save(); c.translate(lx, ly); c.rotate(-12)
        disque(c, 0, 0, 78, C["blanc"], 0.35)
        anneau(c, 0, 0, 78, C["ink"], 12)
        trait(c, 55, 55, 130, 130, C["ink"], 22)
        c.restore()
        if t >= t_francais + 0.12:
            uu = prog(t, t_francais + 0.12, 0.32, lambda v: rebond(v, 1.9))
            pastille_rot(c, "Il est français", x + 520, y + 400, 40, C["rouge"], C["blanc"], -5, mix(0.3, 1, uu), borne(uu * 2), "triangle-alert", (14, 36, 0.25))
    c.restore()


# ═══════════════════════════════════════════ S5 · La marge qui s'ajoute, et qu'on ne voit pas
def s5(c, t):
    if not (S5[0] <= t <= S5[1]): return
    ue = prog(t, S5[0], 0.3, sortie)
    cam = 1 + 0.04 * prog(t, t_toi, 1.4, douce)
    c.save(); c.translate(540, 1000); c.scale(cam, cam); c.translate(-540, -1000 + 260 * (1 - ue))
    with Calque(c, ue):
        x, y, w, h = 150, 650, 780, 700
        carte(c, x, y, w, h, 40, C["blanc"], 1.0, (24, 56, 0.13))
        icone(c, "receipt", x + 70, y + 66, 46, C["ink"], 2.2)
        texte(c, "TA FACTURE", x + 120, y + 48, 30, C["gris"], "fort", track=0.1)
        trait(c, x + 40, y + 120, x + w - 40, y + 120, C["ligne"], 3, rond=False)
        invisible = prog(t, t_vois, 0.45, douce)
        for k, tk in enumerate([t_ajoute, t_chaque, t_cmd]):
            if t < tk - 0.02: continue
            yy = y + 150 + k * 120
            u = prog(t, tk, 0.3, sortie)
            texte(c, f"Commande {k + 1}", x + 40 + 30 * (1 - u), yy + 18, 34, C["ink"], "noir", alpha=u)
            lp = 230 * prog(t, tk, 0.3, sortie)
            rrect(c, x + 340, yy + 22, lp, 40, 12, C["ink"], u)
            um = prog(t, tk + 0.14, 0.26, lambda v: rebond(v, 1.6))
            if um > 0:
                mx = x + 340 + 230 + 10
                if invisible < 1:
                    rrect(c, mx, yy + 22, 150 * um, 40, 12, C["rouge"], (1 - invisible))
                    if um > 0.6: texte_centre(c, "+ marge", mx + 75, yy + 42, 24, C["blanc"], "noir", (1 - invisible) * borne((um - 0.6) * 3))
                if invisible > 0:
                    p = peinture(C["rouge"], 0.45 * invisible, Style=skia.Paint.kStroke_Style, StrokeWidth=3)
                    p.setPathEffect(skia.DashPathEffect.Make([10, 8], 0))
                    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(mx, yy + 22, 150, 40), 12, 12), p)
        # total : il ne bouge pas, même quand la marge devient invisible
        if t >= t_cmd + 0.25:
            u = prog(t, t_cmd + 0.25, 0.35, sortie)
            yy = y + h - 130
            trait(c, x + 40, yy - 20, x + w - 40, yy - 20, C["ligne"], 3, rond=False)
            texte(c, "TOTAL", x + 40, yy + 14, 44, alpha=u)
            rrect(c, x + 340, yy + 18, 400 * u, 48, 14, C["ink"])
            if u > 0.05 and invisible < 1:
                rrect(c, x + 340 + 240 * u, yy + 18, 160 * u, 48, 14, C["rouge"], 1 - invisible)
        tampon(c, "INVISIBLE", 680, 790, t, t_vois + 0.28, 54, C["rouge"], 7, "eye-off")
    c.restore()
    # le disque vert qui remplit l'écran (vers ChinaBook)
    if t >= 14.60:
        u = prog(t, 14.60, 0.3, entree)
        disque(c, 540, 1000, 40 + 1500 * u, C["vert"])


# ═══════════════════════════════════════════ S6 · ChinaBook : les fournisseurs testés, en direct
PH = (300, 664, 480, 960)


def ecran_app(c, x, y, w, h, t, retr_entete):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture(C["blanc"]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, mix(h, 170, retr_entete)), peinture(C["vert"]))
    texte(c, "9:41", x + 40, y + 24, 24, C["blanc"], "fort")
    image(c, "logo-tout-blanc", x + 36, y + 92, 230)
    texte(c, "Fournisseurs testés", x + 36, y + 196, 40)
    lignes = [("Mobilité électrique", "moto", 120), ("Textile", "pull", 70), ("Électronique", "casque", 76)]
    for k, (nom, img, iw) in enumerate(lignes):
        u = prog(t, t_ras + k * 0.14, 0.34, sortie)
        if u <= 0: continue
        yy = y + 260 + k * 170
        xx = x + 22 + 160 * (1 - u)
        with Calque(c, u):
            rrect(c, xx, yy, w - 44, 150, 28, C["fondDoux"])
            iw_, ih_ = taille_img(img); hh = iw * ih_ / iw_
            image(c, img, xx + 24, yy + 75 - hh / 2, iw)
            texte(c, nom, xx + 160, yy + 30, ajuste(nom, w - 44 - 190, 28))
            if t >= t_test + k * 0.08:
                ub = prog(t, t_test + k * 0.08, 0.28, lambda v: rebond(v, 2.0))
                c.save(); c.translate(xx + 160 + 60, yy + 98); c.scale(ub, ub)
                rrect(c, -60, -18, 120, 36, 18, C["vertDoux"]); texte_centre(c, "TESTÉ", 0, 0, 18, C["vertFonce"], "fort")
                c.restore()
            # bouton « contacter » sur la première ligne
            if k == 0 and t >= t_cont - 0.3:
                ub = prog(t, t_cont - 0.3, 0.3, lambda v: rebond(v, 1.8)) * battement(t, t_cont, -0.15, 0.22)
                c.save(); c.translate(xx + w - 44 - 70, yy + 98); c.scale(ub, ub)
                disque(c, 0, 0, 34, C["vert"]); icone(c, "message-circle", 0, 0, 36, C["blanc"], 2.4)
                c.restore()


def s6(c, t):
    if not (S6[0] <= t <= S6[1]): return
    x, y, w, h = PH
    ex, ey, ew, eh = x + 14, y + 14, w - 28, h - 28
    t_retr = t_logo + 0.62
    retr = prog(t, t_retr, 0.5, entreeSortie)
    sortie_u = prog(t, 19.24, 0.18, entree)
    c.save(); c.translate(0, 1300 * sortie_u)
    if t < t_retr + 0.5:
        if retr > 0:
            with Espace(c, 540, 1144, ry=mix(-25, 0, retr)):
                carte(c, mix(-40, x, retr), mix(-40, y, retr), mix(W + 80, w, retr), mix(H + 80, h, retr), mix(0, 74, retr), C["ink"], 1.0, (40, 90, 0.28 * retr))
        rrect(c, mix(0, ex, retr), mix(0, ey, retr), mix(W, ew, retr), mix(H, eh, retr), mix(0, 60, retr), C["vert"])
        if t >= t_logo - 0.04:
            u = prog(t, t_logo, 0.3, lambda v: rebond(v, 1.5))
            lw = mix(1.6, 1, u) * mix(760, 230, retr)
            image(c, "logo-tout-blanc", mix(540 - lw / 2, ex + 36, retr), mix(960, ey + 92, retr), lw, borne(u * 3))
    else:
        sway = 2.2 * math.sin((t - t_retr) * 1.7)
        with Espace(c, 540, 1144, ry=sway):
            telephone(c, x, y, w, h, lambda cc, a, b, d, e: ecran_app(cc, a, b, d, e, t, prog(t, t_retr + 0.5, 0.3, entreeSortie)))
        if t >= t_mois:
            u = prog(t, t_mois, 0.35, lambda v: rebond(v, 1.8))
            pastille_rot(c, "TESTÉS PENDANT DES MOIS", 640, 1430, 28, C["vert"], C["blanc"], -4, mix(0.3, 1, u), borne(u * 2), "badge-check", (14, 36, 0.25))
        if t >= t_direct - 0.12:
            tampon(c, "EN DIRECT", 760, 1150, t, t_direct, 58, C["vert"], -10, "zap")
            confettis(c, 760, 1150, t, t_direct + 0.04, 22, 340, 7)
    c.restore()


# ═══════════════════════════════════════════ S7 · « CHINA » sur WhatsApp, puis le carton final
def s7(c, t):
    if t < S7[0]: return
    part = prog(t, t_fin, 0.32, entree)
    if part < 1:
        u = prog(t, S7[0], 0.36, lambda v: rebond(v, 1.4))
        x, y, w, h = 90, 650, 900, 660
        c.save(); c.translate(540, y + h / 2 + 900 * part); s_ = mix(0.6, 1, u); c.scale(s_, s_); c.translate(-540, -(y + h / 2))
        with Calque(c, borne(u * 2) * (1 - part)):
            # fenêtre de conversation avec ChinaBook
            carte(c, x, y, w, h, 46, "#EEF3F0", 1.0, (24, 56, 0.14))
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 46, 46), doAntiAlias=True)
            c.drawRect(skia.Rect.MakeXYWH(x, y, w, 130), peinture(C["vert"]))
            c.restore()
            disque(c, x + 80, y + 65, 42, C["blanc"]); image(c, "logo-marque", x + 80 - 24, y + 65 - 25, 48)
            texte(c, "ChinaBook", x + 140, y + 30, 38, C["blanc"])
            texte(c, "en ligne", x + 140, y + 78, 26, C["vertDoux"], "demi")
            # message envoyé
            if t >= t_envoi:
                ub = prog(t, t_envoi, 0.34, sortie)
                bw = largeur("CHINA", 64) + 100
                bx, by = x + w - 30 - bw, mix(y + h - 120, y + 300, ub)
                rrect(c, bx, by, bw, 124, 40, C["vert"], ub, (12, 30, 0.2))
                texte_centre(c, "CHINA", bx + bw / 2 - 12, by + 62, 64, C["blanc"], alpha=ub)
                icone(c, "check", bx + bw - 38, by + 92, 28, C["blanc"], 3, ub)
                if t >= t_envoi + 0.3:
                    uv = prog(t, t_envoi + 0.3, 0.25, sortie)
                    texte(c, "Lu", bx + bw - 40, by + 134, 22, C["vertFonce"], "fort", alpha=uv)
            # champ de saisie
            iy = y + h - 110
            rrect(c, x + 24, iy, w - 150, 86, 43, C["blanc"])
            if t < TL[0]:
                texte(c, "Message", x + 64, iy + (86 - hauteurLigne(38, "moyen")) / 2, 38, C["grisClair"], "moyen")
            elif t < t_envoi + 0.04:
                xl = x + 64
                for k, l in enumerate("CHINA"):
                    if t >= TL[k]:
                        uu = prog(t, TL[k], 0.12, sortie)
                        texte(c, l, xl, iy + (86 - hauteurLigne(48)) / 2 - 10 * (1 - uu), 48, C["ink"], alpha=uu)
                        xl += largeur(l, 48)
                if int(t * 4) % 2 == 0: rrect(c, xl + 4, iy + 22, 4, 42, 2, C["vert"])
            sb = battement(t, t_envoi - 0.04, -0.18, 0.25)
            c.save(); c.translate(x + w - 70, iy + 43); c.scale(sb, sb)
            disque(c, 0, 0, 46, C["vert"], 1.0, (8, 20, 0.2)); icone(c, "send", -3, 2, 44, C["blanc"], 2.4)
            c.restore()
        c.restore()
    # carton final
    if t >= t_fin + 0.05:
        u = prog(t, t_fin + 0.05, 0.4, sortie)
        disque(c, 540, 1060, 420 * u * (1 + 0.02 * math.sin(t * 3)), C["vertDoux"])
        ul = prog(t, t_fin + 0.12, 0.36, lambda v: rebond(v, 1.6))
        lw = 760 * mix(0.6, 1, ul)
        iw_, ih_ = taille_img("logo"); lh = lw * ih_ / iw_
        image(c, "logo", 540 - lw / 2, 960 - lh / 2, lw, borne(ul * 2))
        ub = prog(t, t_fin + 0.36, 0.36, lambda v: rebond(v, 1.8))
        etincelles(c, 540, 1170, t, t_fin + 0.5, 12, 380)
        if ub > 0:
            s = mix(0.4, 1, ub) * (1 + 0.035 * max(0, math.sin((t - t_fin - 0.8) * 5)) if t > t_fin + 0.8 else 1)
            c.save(); c.translate(540, 1170); c.scale(s, s)
            pastille(c, "Envoie « CHINA » sur WhatsApp", 0, 0, 40, C["vert"], C["blanc"], "message-circle", borne(ub * 2), (18, 46, 0.3))
            c.restore()


# ─────────────────────────────────────────── composition
def alpha_bandeau(t):
    return borne(prog(t, 0.35, 0.3) * (1 - prog(t, 14.62, 0.15)) + prog(t, 16.2, 0.3) * (1 - prog(t, t_fin - 0.05, 0.25)))


def dessine(c, t):
    fond(c, t)
    bandeau(c, t, alpha_bandeau(t))
    for s in (s1, s2, s3, s4, s5, s6, s7):
        s(c, t)
    liste(c, t)
    K.dessine_eclairs(c, t)
    SOUS.dessine(c, t, C["blanc"] if 14.7 <= t <= 15.95 else C["ink"])
