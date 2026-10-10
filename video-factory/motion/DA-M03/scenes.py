"""DA-M03 « Coach sportif » — pub DYOU Agency : la plateforme coach (site + réservation + paiement + espaces) (27,3 s).

Problème (le soir : messages, relances de paiement, séances, annulations, tout à la main) → « Stop » → tout converge
en une plateforme → démo sur le site ATHLA (concept DYOU) qui défile dans un téléphone, les blocs du site sortent en
verre : questionnaire, réservation d'un créneau, abonnement payé, espace client, espace coach → moins d'admin,
plus de coaching → DYOU Agency. Thème ATHLA : noir + jaune-vert #C8FF2E (agence.theme_athla).
La page est une capture du site (dist/realisations/athla/, 520 px de large, ×2) : media/athla-page.jpg + découpes c-*.png.
"""
import math, pathlib, sys
import numpy as np
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from agence import *
import agence

theme_athla()
DUREE = 27.3
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a

SOUS = SousTitresFins(K, fusions={(94, 95, 96): "DYOU Agency."})
J, JC, NOIR = A["violet"], A["violetClair"], A["surAccent"]
ORANGE, ROUGE, VERT = "#FFB45C", A["rouge"], A["vert"]


def entre(t, t0, d=0.42, s=1.5): return prog(t, t0, d, lambda v: rebond(v, s))
def sort(t, t0, d=0.26): return prog(t, t0, d, entree)


# ─────────────────────────────────────────── S1 · le soir du coach : messages, relances, annulations
T_STOP = TW(32) - 0.05
T_CENT = TW(34) - 0.1
T_PLAT = TW(39) - 0.05
T_SITE = TW(40) - 0.1

NOTIFS = [(TW(6) - 0.1, "Sofia", "On peut décaler à jeudi ?"), (TW(8) - 0.12, "Yanis", "Tu m'envoies le programme ?"),
          (TW(8) + 0.12, "Camille", "Dispo demain 18 h ?"), (TW(25) - 0.1, "Thomas", "Désolé, j'annule demain…")]


def ecran_soir(c, x, y, w, h, t):
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + h)], [hexa("#1B2208"), hexa("#050604")]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), g)
    texte(c, "Mardi 9 décembre", x + w / 2, y + 70, 22, "#FFFFFF", "demi", "centre", 0, 0.8)
    texte(c, "22:47", x + w / 2, y + 96, 104, "#FFFFFF", "noir", "centre", -0.02)
    arr = [n for n in NOTIFS if t >= n[0]]
    yb = y + 250
    for k, (t0, nom, msg) in enumerate(reversed(arr)):
        u = entre(t, t0, 0.35, 1.6)
        hh = 104; yy = yb + k * (hh + 12) - (1 - u) * 40
        if k > 0: yy += (hh + 12) * 0  # la pile descend d'un cran à chaque arrivée
        with Calque(c, borne(u * 2)):
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 18, yy, w - 36, hh), 26, 26)
            c.drawRRect(rr, peinture("#FFFFFF", 0.14))
            ann = "annule" in msg
            disque(c, x + 62, yy + hh / 2, 26, ROUGE if ann else VERT)
            icone(c, "message-circle", x + 62, yy + hh / 2, 28, "#FFFFFF", 2.4)
            texte(c, nom, x + 102, yy + 20, 24, "#FFFFFF", "gras", track=0)
            texte(c, "maintenant", x + w - 40, yy + 22, 18, "#FFFFFF", "demi", "droite", 0, 0.5)
            texte(c, msg, x + 102, yy + 56, 22, "#FFFFFF", "demi", track=0, alpha=0.85)


def carte_bulle(c, cx, cy, t, t0, titre, ic, col, lignes, rot):
    u = entre(t, t0, 0.45, 1.5)
    if u <= 0: return
    with Espace(c, cx, cy, ry=mix(-60, 0, u), rz=rot, s=mix(0.4, 1, u), tx=mix(-200, 0, u)):
        with Calque(c, borne(u * 2)):
            w, h = 520, 220
            verre(c, cx - w / 2, cy - h / 2, w, h, 36, 0.09)
            disque(c, cx - w / 2 + 70, cy - h / 2 + 70, 36, col)
            icone(c, ic, cx - w / 2 + 70, cy - h / 2 + 70, 38, "#FFFFFF", 2.4)
            texte(c, titre, cx - w / 2 + 124, cy - h / 2 + 50, 32, "#FFFFFF", "gras", track=-0.01)
            for k, l in enumerate(lignes):
                texte(c, l, cx - w / 2 + 40, cy - h / 2 + 124 + 40 * k, 26, "#FFFFFF", "demi", track=0, alpha=0.8)


def tableur(c, cx, cy, t, t0):
    u = entre(t, t0, 0.45, 1.6)
    if u <= 0: return
    with Espace(c, cx, cy, rx=mix(50, 0, u), rz=-7, s=mix(0.4, 1, u)):
        with Calque(c, borne(u * 2)):
            w, h = 470, 330
            verre(c, cx - w / 2, cy - h / 2, w, h, 30, 0.1)
            texte(c, "Suivi clients.xlsx", cx - w / 2 + 30, cy - h / 2 + 22, 24, "#FFFFFF", "gras", track=0)
            x0, y0 = cx - w / 2 + 24, cy - h / 2 + 70
            for i in range(5):
                for j in range(4):
                    on = (t - t0) * 9 > i * 4 + j
                    rrect(c, x0 + j * 106, y0 + i * 48, 98, 40, 6, "#FFFFFF", 0.16 if on else 0.06)
                    if on and (i * 4 + j) % 3: rrect(c, x0 + j * 106 + 12, y0 + i * 48 + 16, 50 + 20 * ((i + j) % 2), 8, 4, "#FFFFFF", 0.5)
            icone(c, "paintbrush", cx + w / 2 - 40, cy + h / 2 - 40, 44, ORANGE, 2.4)


def s1(c, t):
    if t > T_CENT + 0.6: return
    st = prog(t, T_STOP, 0.2, sortie)                     # « Stop » : tout se fige et s'assombrit
    cv = prog(t, T_CENT, 0.55, entree)                    # « centralise » : tout est aspiré au centre
    def aspire(cx, cy):
        return mix(cx, 540, cv), mix(cy, 1000, cv), mix(1, 0.15, cv)
    al = 1 - 0.45 * st
    cx, cy, s = aspire(540, 1020)
    sh = secousse(t, TW(28), 10)[0] * (1 - st)
    with Calque(c, al * (1 - borne((cv - 0.7) / 0.3))):
        with Espace(c, cx + sh, cy, ry=-12 + 2 * math.sin(t * 2) * (1 - st), rx=4, s=s * mix(1, 0.94, st)):
            telephone_sombre(c, cx + sh, cy, 470, 940, lambda cc, a, b, d, e: ecran_soir(cc, a, b, d, e, min(t, T_STOP)))
        u = entre(t, -0.4, 0.4, 2)
        x, y, s2 = aspire(260, 560)
        pastille_verre(c, "Coach sportif", x, y + 8 * math.sin(t * 2.5), 42, "dumbbell", borne(u * 2), mix(0.4, 1, u) * s2, rot=-6)
        u = entre(t, TW(4) - 0.1, 0.4, 2)
        x, y, s2 = aspire(820, 600)
        pastille_verre(c, "22:47", x, y, 42, "clock", borne(u * 2), mix(0.4, 1, u) * s2, rot=6)
        x, y, s2 = aspire(620, 1250)
        c.save(); c.translate(x, y); c.scale(s2, s2); c.translate(-x, -y)
        carte_bulle(c, x, y, min(t, T_STOP), TW(10) - 0.1, "Relance paiement", "wallet", ORANGE, ["« Petit rappel pour ce mois-ci »", "En attente"], -4)
        c.restore()
        x, y, s2 = aspire(450, 760)
        c.save(); c.translate(x, y); c.scale(s2, s2); c.translate(-x, -y)
        carte_bulle(c, x, y, min(t, T_STOP), TW(16) - 0.1, "Séance de jeudi ?", "calendar", "#4C7DFF", ["« Toujours bon pour 18 h ? »", "Pas de réponse"], 5)
        c.restore()
        u = prog(t, TW(25) - 0.05, 0.3, lambda v: rebond(v, 2.6))
        if u > 0:
            x, y, s2 = aspire(760, 1460)
            pastille_verre(c, "Séance annulée", x, y, 44, "x", borne(u * 2), mix(1.6, 1, u) * s2, accent=ROUGE, rot=-5)
        x, y, s2 = aspire(330, 1300)
        c.save(); c.translate(x, y); c.scale(s2, s2); c.translate(-x, -y)
        tableur(c, x, y, min(t, T_STOP), TW(27) - 0.1)
        c.restore()
    # « Stop » : la main qui claque
    u = prog(t, T_STOP, 0.3, lambda v: rebond(v, 2.6)) * (1 - prog(t, T_CENT, 0.25, entree))
    if u > 0:
        c.save(); c.translate(540, 1000); c.scale(mix(2.2, 1, u), mix(2.2, 1, u))
        with Calque(c, borne(u * 3)):
            lueur(c, 0, 0, 380, J, 0.5)
            disque(c, 0, 0, 150, J)
            icone(c, "hand", 0, 0, 150, NOIR, 2.4)
        c.restore()


# ─────────────────────────────────────────── S2 · une seule plateforme
SAT = [("globe", "Site"), ("calendar", "Réservations"), ("credit-card", "Paiements"), ("message-circle", "Messages")]


def s2(c, t):
    if t < T_CENT + 0.2 or t > T_SITE + 0.45: return
    u = entre(t, T_CENT + 0.35, 0.5, 1.8); o = sort(t, T_SITE - 0.05, 0.4)
    cx, cy = 540, 1000
    with Calque(c, borne(u * 2) * (1 - o)):
        lueur(c, cx, cy, 520, J, 0.35 + 0.15 * math.sin(t * 5))
        p = prog(t, T_PLAT, 0.5, sortie)
        for k, (ic, lab) in enumerate(SAT):
            a = -math.pi / 2 + k * math.pi / 2 + 0.3 * math.sin(t * 0.8) * 0
            R = mix(0, 350, p)
            x, y = cx + R * math.cos(a + 0.785), cy + R * math.sin(a + 0.785)
            if p > 0:
                trait(c, cx, cy, x, y, J, 3, 0.5 * p)
                disque(c, mix(cx, x, (t * 1.6 + k / 4) % 1), mix(cy, y, (t * 1.6 + k / 4) % 1), 6, JC, p)
                pastille_verre(c, lab, x, y, 40, ic, p, mix(0.4, 1, p))
        c.save(); c.translate(cx, cy); s = mix(0.3, 1, u) * (1 - 0.4 * o); c.scale(s, s)
        verre(c, -190, -190, 380, 380, 70, 0.1)
        disque(c, 0, -40, 80, J); icone(c, "dumbbell", 0, -40, 80, NOIR, 2.4)
        texte(c, "Ta plateforme", 0, 70, 40, "#FFFFFF", "noir", "centre", -0.02)
        c.restore()


# ─────────────────────────────────────────── S3-S6 · le site dans le téléphone, les blocs qui en sortent
TX, TY, TWD, THT = 300, 1040, 450, 920          # le téléphone, tourné vers les panneaux à droite
T_FORM = TW(51) - 0.1
T_RESA = TW(54) - 0.12
T_PRIX = TW(59) - 0.12
T_APP = TW(63) - 0.1
T_COACH = TW(75) - 0.1
T_FIN_TEL = TW(89) - 0.1
DEFIL = [(T_SITE + 0.2, 0), (TW(46), 1000, sortie), (T_FORM - 0.3, 1200), (T_FORM, 6420, entreeSortie), (T_RESA - 0.25, 6900, sortie),
         (T_RESA, 19480, entreeSortie), (T_PRIX - 0.25, 19560), (T_PRIX, 16300, entreeSortie), (T_APP - 0.3, 16500),
         (T_APP, 8560, entreeSortie), (T_COACH - 0.3, 8900, sortie), (T_COACH, 23050, entreeSortie), (T_FIN_TEL, 23300, sortie)]


def ecran_site(c, x, y, w, h, t):
    py = cles(t, DEFIL)
    k = w / 1040
    c.drawImageRect(moteur._img("athla-page"), skia.Rect.MakeXYWH(0, py, 1040, h / k), skia.Rect.MakeXYWH(x, y, w, h),
                    skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), skia.Paint())


def panneau(c, t, ta, tb, nom, cx, cy, w, extra=None, ry=-10):
    """bloc du site qui sort de l'écran du téléphone, se pose à droite, et y retourne"""
    u = prog(t, ta, 0.5, lambda v: rebond(v, 1.15))
    o = prog(t, tb, 0.3, entree)
    if u <= 0 or o >= 1: return
    iw, ih = taille_img(nom); h = w * ih / iw
    v = u * (1 - o)
    px, py_ = mix(TX + 40, cx, v), mix(TY, cy, v)
    with Espace(c, px, py_, ry=mix(14, ry, v), s=mix(0.3, 1, v)):
        with Calque(c, borne(v * 3)):
            pad = 18
            lueur(c, px, py_, w * 0.8, J, 0.18 * v)
            verre(c, px - w / 2 - pad, py_ - h / 2 - pad, w + 2 * pad, h + 2 * pad, 40, 0.08)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(px - w / 2, py_ - h / 2, w, h), 26, 26), True)
            image(c, nom, px - w / 2, py_ - h / 2, w)
            c.restore()
            if extra: extra(c, px - w / 2, py_ - h / 2, w / iw)


def surligne(c, x0, y0, k, r, t, t0, ep=5):
    """cadre jaune qui se dessine autour d'une zone (coordonnées de la découpe)"""
    u = prog(t, t0, 0.35, lambda v: rebond(v, 1.8))
    if u <= 0: return
    x, y, w, h = x0 + r[0] * k, y0 + r[1] * k, (r[2] - r[0]) * k, (r[3] - r[1]) * k
    g = 10 * (1 - u)
    lueur(c, x + w / 2, y + h / 2, max(w, h) * 0.7, J, 0.25 * u)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - g, y - g, w + 2 * g, h + 2 * g), 16, 16),
                peinture(J, u, Style=skia.Paint.kStroke_Style, StrokeWidth=ep))


def s_site(c, t):
    if t < T_SITE - 0.1 or t > T_FIN_TEL + 0.5: return
    u = entre(t, T_SITE, 0.55, 1.2); o = prog(t, T_FIN_TEL, 0.45, entree)
    x = TX + mix(700, 0, u) - 800 * o
    with Espace(c, x, TY, ry=mix(-40, 14, u) + 2 * math.sin(t * 1.7), s=mix(0.7, 1, u)):
        telephone_sombre(c, x, TY, TWD, THT, lambda cc, a, b, d, e: ecran_site(cc, a, b, d, e, t), borne(u * 2) * (1 - o))
    # « pro, à ton image »
    a = entre(t, TW(43) - 0.1, 0.4, 2.2) * (1 - sort(t, T_FORM - 0.2))
    pastille_verre(c, "Pro", 790, 760, 46, "badge-check", borne(a * 2), mix(0.4, 1, a), rot=5)
    b = entre(t, TW(45) - 0.1, 0.4, 2.2) * (1 - sort(t, T_FORM - 0.2))
    pastille_verre(c, "À ton image", 760, 1260, 46, "paintbrush", borne(b * 2), mix(0.4, 1, b), rot=-5)
    # le questionnaire
    panneau(c, t, T_FORM, T_RESA - 0.3, "c-form", 700, 980, 600)
    a = entre(t, TW(51) - 0.05, 0.4, 2.2) * (1 - sort(t, T_RESA - 0.3))
    pastille_verre(c, "3 questions", 740, 640, 42, "list-filter", borne(a * 2), mix(0.4, 1, a), rot=-4)
    # la réservation : un créneau libre s'allume
    def resa(cc, x0, y0, k):
        surligne(cc, x0, y0, k, (225, 210, 400, 318), t, TW(56) - 0.1, 6)
        if t > TW(56) + 0.1:
            a_ = prog(t, TW(56) + 0.1, 0.3, lambda v: rebond(v, 2.4))
            disque(cc, x0 + 400 * k, y0 + 210 * k, 22 * a_, J); icone(cc, "check", x0 + 400 * k, y0 + 210 * k, 26 * a_, NOIR, 3.2)
    panneau(c, t, T_RESA, T_PRIX - 0.3, "c-resa", 700, 1000, 620, resa)
    a = entre(t, TW(56) - 0.05, 0.4, 2.2) * (1 - sort(t, T_PRIX - 0.3))
    pastille_verre(c, "Créneau réservé", 700, 1330, 42, "calendar", borne(a * 2), mix(0.4, 1, a), rot=3)
    # l'abonnement : le bouton se presse, paiement validé
    def prix(cc, x0, y0, k):
        surligne(cc, x0, y0, k, (50, 945, 910, 1062), t, TW(61) - 0.05, 6)
    panneau(c, t, T_PRIX, T_APP - 0.3, "c-prix", 700, 1000, 560, prix)
    a = entre(t, TW(62) - 0.1, 0.4, 2.4) * (1 - sort(t, T_APP - 0.3))
    pastille_verre(c, "Paiement validé", 700, 1450, 44, "credit-card", borne(a * 2), mix(0.4, 1, a), accent=VERT, rot=-3)
    confettis(c, 700, 1300, t, TW(62), 22, 380, 7, cols=[J, JC, "#FFFFFF", VERT])
    # l'espace client
    panneau(c, t, T_APP, T_COACH - 0.3, "c-app", 700, 940, 600)
    for k, (t0, lab, ic) in enumerate([(TW(66) - 0.1, "Programme", "dumbbell"), (TW(68) - 0.1, "Séances", "calendar"), (TW(71) - 0.1, "Messages", "message-circle")]):
        a = entre(t, t0, 0.4, 2.2) * (1 - sort(t, T_COACH - 0.3))
        pastille_verre(c, lab, [420, 770, 600][k], [1300, 1300, 1410][k], 40, ic, borne(a * 2), mix(0.4, 1, a))
    a = entre(t, TW(74) - 0.1, 0.4, 2.2) * (1 - sort(t, T_COACH - 0.3))
    pastille_verre(c, "Son espace", 760, 600, 44, "user", borne(a * 2), mix(0.4, 1, a), rot=4)
    # l'espace coach : planning, clients, paiements
    def coach(cc, x0, y0, k):
        surligne(cc, x0, y0, k, (40, 525, 990, 1240), t, TW(80) - 0.1)
        surligne(cc, x0, y0, k, (505, 105, 985, 312), t, TW(82) - 0.1)
        surligne(cc, x0, y0, k, (505, 320, 985, 505), t, TW(85) - 0.1)
    panneau(c, t, T_COACH, T_FIN_TEL, "c-coach", 650, 1020, 680, coach, ry=-6)
    a = entre(t, TW(76) - 0.1, 0.4, 2.2) * (1 - sort(t, T_FIN_TEL))
    pastille_verre(c, "Toi, le coach", 300, 560, 44, "dumbbell", borne(a * 2), mix(0.4, 1, a), rot=-5)
    a = entre(t, TW(87) - 0.1, 0.4, 2.4) * (1 - sort(t, T_FIN_TEL))
    pastille_verre(c, "Tout au même endroit", 600, 1450, 44, "check", borne(a * 2), mix(0.4, 1, a), accent=VERT)


# ─────────────────────────────────────────── S7 · moins d'admin, plus de coaching
T_LOGO = TW(94) - 0.12
T_CTA = TW(97) - 0.1


def s7(c, t):
    if t < T_FIN_TEL or t > T_LOGO + 0.4: return
    u = entre(t, T_FIN_TEL + 0.05, 0.45, 1.4)
    for k, (lab, ic, t0, de, a_, col) in enumerate([("Admin", "clock", TW(89) - 0.05, 1.0, 0.18, ROUGE), ("Coaching", "dumbbell", TW(91) - 0.05, 0.25, 1.0, J)]):
        a = entre(t, t0 - 0.25, 0.4, 1.6)
        if a <= 0: continue
        y = 840 + 300 * k
        f = mix(de, a_, prog(t, t0, 0.6, entreeSortie))
        with Espace(c, 540, y, rx=mix(50, 0, a), s=mix(0.6, 1, a)):
            with Calque(c, borne(a * 2)):
                verre(c, 110, y - 110, 860, 220, 40, 0.08)
                disque(c, 190, y, 46, col); icone(c, ic, 190, y, 48, NOIR if col == J else "#FFFFFF", 2.4)
                texte(c, lab, 260, y - 56, 40, "#FFFFFF", "noir", track=-0.02)
                rrect(c, 260, y + 20, 640, 30, 15, "#FFFFFF", 0.1)
                rrect(c, 260, y + 20, 640 * f, 30, 15, col)
                icone(c, "trending-up" if k else "x", 900, y - 36, 40, col, 2.6)


# ─────────────────────────────────────────── sons
son(0.0, "impact", -6); son(0.0, "pop", -14); son(TW(4) - 0.1, "pop", -13)
for t0, *_ in NOTIFS: son(t0, "message_in", -10)
son(TW(10) - 0.1, "whoosh_court", -12); son(TW(10), "message", -12)
son(TW(16) - 0.1, "whoosh_court", -12); son(TW(16), "message", -12)
son(TW(25) - 0.05, "tampon", -8); son(TW(25), "impact_doux", -10)
son(TW(27) - 0.1, "whoosh_court", -12)
for k in range(10): son(TW(27) + 0.11 * k, "frappe", -17)
son(TW(28), "impact_doux", -11)
son(T_STOP, "impact", -4); son(T_STOP + 0.02, "verre", -10)
son(T_CENT, "whoosh_long", -9); son(T_CENT + 0.5, "impact_doux", -9)
son(T_PLAT, "montee", -14)
for k in range(4): son(T_PLAT + 0.08 * k, "pop", -14)
son(T_SITE, "whoosh", -10); son(TW(43) - 0.1, "pop", -12); son(TW(45) - 0.1, "pop", -12)
for t0 in (T_FORM, T_RESA, T_PRIX, T_APP, T_COACH): son(t0 - 0.1, "swipe", -13); son(t0 + 0.05, "whoosh_court", -12); son(t0 + 0.2, "verre", -15)
son(TW(51) - 0.05, "pop", -13); son(TW(56) - 0.1, "clic", -9); son(TW(56) + 0.1, "check", -11)
son(TW(61) - 0.05, "clic", -9); son(TW(62) - 0.1, "ching", -9)
for t0 in (TW(66) - 0.1, TW(68) - 0.1, TW(71) - 0.1, TW(74) - 0.1): son(t0, "pop", -13)
son(TW(76) - 0.1, "pop", -13)
for t0 in (TW(80) - 0.1, TW(82) - 0.1, TW(85) - 0.1): son(t0, "blip", -12)
son(TW(87) - 0.1, "check", -11)
son(T_FIN_TEL, "whoosh", -11); son(TW(89), "whoosh_bas", -12); son(TW(91), "montee", -13); son(TW(91) + 0.5, "ding", -12)
son(T_LOGO - 0.1, "montee", -14); son(T_LOGO + 0.24, "impact", -6); son(T_LOGO + 0.26, "verre", -9)
son(T_CTA, "whoosh", -12); son(T_CTA + 0.3, "pop", -10)

for a, b in [(T_STOP, T_STOP + 0.2), (T_CENT, T_CENT + 0.55), (T_SITE, T_SITE + 0.4), (T_FORM - 0.05, T_FORM + 0.5),
             (T_RESA - 0.05, T_RESA + 0.5), (T_PRIX - 0.05, T_PRIX + 0.5), (T_APP - 0.05, T_APP + 0.5), (T_COACH - 0.05, T_COACH + 0.5),
             (T_FIN_TEL, T_FIN_TEL + 0.45), (T_LOGO, T_LOGO + 0.35), (T_CTA - 0.1, T_CTA + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(TW(25), ROUGE, 0.12), (T_STOP, J, 0.2), (T_CENT + 0.5, "#FFFFFF", 0.12), (TW(62), VERT, 0.1),
                    (TW(91) + 0.3, J, 0.1), (T_LOGO + 0.24, "#FFFFFF", 0.18)]:
    eclair(tt, cc_, a_)


# ─────────────────────────────────────────── composition
def dessine(c, t):
    agence.T_COURANT[0] = t
    fond_agence(c, t, battement(t, T_STOP, 1, 0.5) + battement(t, TW(62), 1, 0.5) - 2)
    if t < T_LOGO + 0.45:
        s1(c, t); s2(c, t); s_site(c, t); s7(c, t)
    disque_logo(c, t, T_LOGO, T_CTA)
    carton_agence(c, t, T_CTA + 0.25, accroche="Ton site et ton espace coach, prêts")
    K.dessine_eclairs(c, t)
    if t < T_LOGO + 0.15: SOUS.dessine(c, t)
