"""DA-M08 « Un meilleur site » — pub verticale DYOU Agency pour vendre les sites internet (14/10/2026). Format AD :
aucun « commente / enregistre », appel final « Clique sur le lien ». Voix Tomy à 4,0 mots/s (rythme validé).

Cible : un patron qui sent qu'il n'est plus dans la course. Hook : deux fois la même entreprise, seule différence le site ;
le concurrent gagne. Google : ton site lent, daté, illisible → le client ferme et appelle l'autre. 2019 → 2026.
Ton site = ton premier commercial ; s'il vieillit, tu vieillis. DYOU : site moderne, rapide, mobile, offre claire,
boutons appel / WhatsApp, trouvé sur Google. Dès 490 €, sans abonnement, le site est à toi. Clique sur le lien.
Style « studio clair » du site (moteur/studio.py).
"""
import math, pathlib, sys
import skia

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from kit import *
from studio import *

DUREE = 29.4
K = Kit(P, DUREE)
TW, son, rapide, eclair = K.TW, K.son, K.rapide, K.eclair
NB_IMAGES, SFX, flou_a = K.nb_images, K.SFX, K.flou_a
SOUS = sous_titres(K, fusions={(38, 39, 40): "2026.", (56, 57, 58): "DYOU Agency,", (89, 90, 91, 92): "490 €,"})

T = {k: TW(i) for k, i in dict(concurrent=1, pas=3, toi=6, juste=9, msite=11, client=14, cherche=16, google=18, tombe=20,
                                site=23, lent=24, date=25, illisible=26, tel=28, ferme=30, appelle=33, autre=34, on=35,
                                deux=38, vingt=40, tonsite=41, premier=45, commercial=46, sil=47, vieux=49, toi2=51, vieux2=54,
                                chez=55, agency=58, moderne=64, rapide=65, pense=66, tel2=69, offre=71, claire=72, bouton=74,
                                appeler=76, whatsapp=80, google2=82, trouve=85, vitrine=86, des=88, quatre=89, qvd=91,
                                euros=92, sans=93, abonnement=94, atoi=99, clique=100, lien=103, maquette=107, fin=108).items()}
B = dict(h=0.0, g=T["client"] - 0.1, an=T["on"] - 0.1, com=T["tonsite"] - 0.1, dy=T["chez"] - 0.1, prix=T["vitrine"] - 0.15,
         cta=T["clique"] - 0.12)
VERT_WA = "#25D366"


# ═══════════════════════════════════════════ les deux sites
def site_moderne(c, x, y, w, h, t, u=1.0, nom="Martin", metier="Plomberie"):
    """site récent : bandeau dégradé, titre fort, deux boutons ; u (0→1) = passage du gris au vif"""
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#FFFFFF"))
    k = w / 900
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    with Calque(c, u):
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h * 0.62), pgrad(x, y, x + w, y + h * 0.62, ["#F1EAFF", "#E6EEFF"]))
        lueur_s(c, x + w * 0.8, y + h * 0.2, 260 * k, S["violetVif"], 0.25)
    texte(c, nom.upper(), x + 34 * k, y + 24 * k, 26 * k, S["encre"] if u > 0.5 else "#8A8594", "noir", track=0.08)
    for j in range(3): rrect(c, x + w - (250 - 80 * j) * k, y + 36 * k, 56 * k, 8 * k, 4 * k, S["ligne"])
    if u > 0.02:
        with Calque(c, u):
            texte(c, f"{metier},", x + 34 * k, y + 90 * k, 56 * k, S["encre"], "titre", track=-0.035)
            texte_grad(c, "sans attendre.", x + 34 * k, y + 152 * k, 56 * k, "titre", "gauche", -0.035)
            rrect(c, x + 34 * k, y + 250 * k, 220 * k, 64 * k, 32 * k, S["violet"])
            texte(c, "Appeler", x + 144 * k, y + 266 * k, 26 * k, "#FFFFFF", "fort", "centre", 0)
            rrect(c, x + 270 * k, y + 250 * k, 220 * k, 64 * k, 32 * k, VERT_WA)
            texte(c, "WhatsApp", x + 380 * k, y + 266 * k, 26 * k, "#FFFFFF", "fort", "centre", 0)
            for j in range(3):
                carte_s(c, x + (34 + 280 * j) * k, y + 350 * k, 250 * k, 110 * k, 18 * k, ombre=0.08)
                tuile(c, ["wrench", "clock", "shield-check"][j], x + (84 + 280 * j) * k, y + 405 * k, 56 * k, "doux")
                rrect(c, x + (124 + 280 * j) * k, y + 392 * k, 130 * k, 10 * k, 5 * k, S["ligne"])
    if u < 0.98:
        with Calque(c, 1 - u):
            site_vieux_corps(c, x, y, w, h, t)
    c.restore()


def site_vieux_corps(c, x, y, w, h, t):
    k = w / 900
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#ECEBEF"))
    rrect(c, x + 34 * k, y + 80 * k, w - 68 * k, 150 * k, 4, "#D3D0D9"); icone(c, "image", x + w / 2, y + 155 * k, 70 * k, "#B3AFBB", 1.4)
    for j in range(6): rrect(c, x + 34 * k, y + (260 + 26 * j) * k, (w - 68 * k) * (0.95 - 0.1 * (j % 3)), 9 * k, 2, "#C9C5D0")
    texte(c, "Bienvenue sur notre site internet", x + 34 * k, y + 430 * k, 20 * k, "#9B96A5", "demi", track=0)
    texte(c, "© 2019", x + w - 34 * k, y + h - 34 * k, 18 * k, "#9B96A5", "demi", "droite", 0)


def site_vieux(c, x, y, w, h, t):
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h)); site_vieux_corps(c, x, y, w, h, t); c.restore()


# ═══════════════════════════════════════════ 1. HOOK : même entreprise, seul le site change
def hook(c, t):
    if t > B["g"] + 0.3: return
    o = prog(t, B["g"] - 0.15, 0.35, entree)
    c.save(); c.translate(0, -300 * o)
    with Calque(c, 1 - o):
        bascule = prog(t, T["juste"] - 0.1, 0.4, entreeSortie)
        lettres(c, "PAS MEILLEUR", 540, 120 - 60 * bascule, 92, t, -0.45, "ressort", decal=0.03, alpha=1 - bascule)
        lettres(c, "QUE TOI.", 540, 222 - 60 * bascule, 92, t, -0.25, "masque", decal=0.03, alpha=1 - bascule, grad=False, couleur=S["encre"])
        if bascule > 0:
            lettres(c, "JUSTE UN", 540, 120, 92, t, T["juste"] - 0.05, "masque", decal=0.03, grad=False, couleur=S["encre"])
            lettres(c, "MEILLEUR SITE.", 540, 222, 92, t, T["msite"] - 0.05, "ressort", decal=0.03)
        u = prog(t, T["msite"] - 0.05, 0.5, entreeSortie)
        for k, (lab, ic, y0) in enumerate([("Ton concurrent", "store", 430), ("Toi", "user-round", 960)]):
            a = entre(t, -0.45 + 0.1 * k, 0.5, 1.4)
            if a <= 0: continue
            chute = prog(t, T["msite"] + 0.2, 0.5, entree) if k == 1 else 0
            s = mix(0.7, 1, a) * (1 + 0.06 * u if k == 0 else 1 - 0.1 * chute)
            cx, cy = 540, y0 + 220
            c.save(); c.translate(cx, cy + 40 * chute); c.rotate(-6 * chute); c.scale(s, s); c.translate(-cx, -cy)
            with Calque(c, borne(a * 3) * (1 - 0.45 * chute)):
                if k == 0 and u > 0: lueur_s(c, cx, cy, 560, S["violetVif"], 0.30 * u)
                navigateur(c, 110, y0, 860, 440, "martin-plomberie.fr" if k == 0 else "dupont-plomberie.fr",
                           (lambda cc, x, y, w, h: site_moderne(cc, x, y, w, h, t, u)) if k == 0 else
                           (lambda cc, x, y, w, h: site_vieux(cc, x, y, w, h, t)))
            c.restore()
            pill(c, lab, 250, y0 - 6, 28, "encre" if k == 0 else "blanc", ic, borne(a * 3), mix(0.5, 1, a), rot=-4)
        if u > 0:
            b = entre(t, T["msite"] + 0.1, 0.4, 2.4)
            c.save(); c.translate(920, 440); c.scale(b, b)
            disque(c, 0, 0, 62, S["or_"], 1.0, (8, 24, 0.25)); icone(c, "trophy", 0, 0, 64, "#FFFFFF", 2.6)
            c.restore()
            eclats(c, 920, 440, t, T["msite"] + 0.15, 14, 300, graine=3)
        eg = 1 - u
        if eg > 0.02 and t > 0.4:
            disque(c, 540, 915, 44, "#FFFFFF", eg, (6, 18, 0.15)); texte(c, "=", 540, 915 - hauteurLigne(60) / 2, 60, S["violet"], "noir", "centre", 0, eg)


# ═══════════════════════════════════════════ 2. GOOGLE : le client tombe sur ton site et part
RESULTATS = [("Dupont Plomberie", "dupont-plomberie.fr", True), ("Martin Plomberie", "martin-plomberie.fr", False),
             ("Plombier 24/7", "plombier-express.fr", False)]


def ecran_google(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#FFFFFF"))
    k = w / 480
    cols = ["#4285F4", "#EA4335", "#FBBC05", "#4285F4", "#34A853", "#EA4335"]
    gx = x + w / 2 - largeur("Google", 50 * k, "fort", 0) / 2
    for j, ch in enumerate("Google"):
        texte(c, ch, gx, y + 90 * k, 50 * k, cols[j], "fort", track=0); gx += largeur(ch, 50 * k, "fort", 0)
    rrect(c, x + 24 * k, y + 170 * k, w - 48 * k, 70 * k, 35 * k, "#F1F3F4")
    icone(c, "search", x + 60 * k, y + 205 * k, 30 * k, "#5F6368", 2.4)
    req = "plombier Lyon"
    n = int(borne((t - T["cherche"]) / 0.45) * len(req) + 0.999) if t >= T["cherche"] else 0
    texte(c, req[:n], x + 90 * k, y + 205 * k - hauteurLigne(28 * k, "demi") / 2, 28 * k, "#202124", "demi", track=0)
    if T["cherche"] <= t < T["google"] and int(t * 4) % 2 == 0:
        rrect(c, x + 92 * k + largeur(req[:n], 28 * k, "demi", 0), y + 188 * k, 3, 34 * k, 1, "#202124")
    for j, (nom, url, toi) in enumerate(RESULTATS):
        a = entre(t, T["google"] + 0.08 * j, 0.35, 1.6)
        if a <= 0: continue
        yy = y + (280 + 150 * j) * k + 30 * (1 - a)
        with Calque(c, borne(a * 3)):
            hl = (toi and T["tombe"] - 0.1 < t < T["ferme"]) or (not toi and j == 1 and t > T["appelle"] - 0.15)
            if hl: rrect(c, x + 14 * k, yy - 14 * k, w - 28 * k, 130 * k, 18 * k, S["lavande"])
            texte(c, url, x + 30 * k, yy, 20 * k, "#5F6368", "demi", track=0)
            texte(c, nom, x + 30 * k, yy + 32 * k, 32 * k, "#1A0DAB", "fort", track=-0.01)
            rrect(c, x + 30 * k, yy + 84 * k, w * 0.7, 9 * k, 4, "#E8EAED")


def ecran_vieux(c, x, y, w, h, t):
    """ton site sur téléphone : chargement interminable, texte minuscule, mise en page d'ordinateur"""
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#F4F3F6"))
    ch = prog(t, T["site"], 0.9, lambda v: v ** 2.4)
    rrect(c, x, y + 60, w * ch, 6, 3, "#4285F4")
    if t < T["lent"] + 0.15:
        ang = t * 400
        c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(ang)
        pa = peinture("#B3AFBB", 1, Style=skia.Paint.kStroke_Style, StrokeWidth=8, StrokeCap=skia.Paint.kRound_Cap)
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(-40, -40, 80, 80), 0, 270); c.drawPath(p, pa)
        c.restore()
        return
    # le site d'ordinateur rétréci : tout est minuscule
    site_vieux(c, x + 10, y + 90, w - 20, (w - 20) * 0.62, t)
    for j in range(14): rrect(c, x + 20, y + 420 + 22 * j, (w - 40) * (0.9 - 0.15 * (j % 3)), 6, 2, "#C9C5D0")
    if t > T["illisible"] - 0.1:
        u = prog(t, T["illisible"] - 0.1, 0.3, sortie)
        cx, cy = x + w / 2, y + 560
        c.save(); c.translate(cx, cy)
        for sgn in (-1, 1):
            disque(c, sgn * 60 * (1 + u), 0, 26, "#FFFFFF", 0.85, (4, 10, 0.2))
        c.restore()


def ecran_appel(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), pgrad(x, y, x, y + h, ["#2B2E3A", "#14161D"]))
    texte(c, "Martin Plomberie", x + w / 2, y + 200, 40, "#FFFFFF", "titre", "centre", -0.01)
    texte(c, "Appel en cours…", x + w / 2, y + 256, 26, "#B7BAC6", "demi", "centre", 0)
    for j in range(3):
        ph = ((t - T["appelle"]) * 1.2 + j / 3) % 1
        anneau(c, x + w / 2, y + 520, 80 + 120 * ph, "#34C759", 4)
    disque(c, x + w / 2, y + 520, 80, "#34C759"); icone(c, "phone", x + w / 2, y + 520, 70, "#FFFFFF", 2.4)


def scene_google(c, t):
    if t < B["g"] - 0.2 or t > B["an"] + 0.3: return
    a = prog(t, B["g"] - 0.2, 0.5, lambda v: rebond(v, 1.3))
    o = prog(t, B["an"] - 0.1, 0.35, entree)
    def ecran(cc, x, y, w, h):
        if t < T["tombe"] + 0.15:
            ecran_google(cc, x, y, w, h, t)
        elif t < T["ferme"]:
            ecran_vieux(cc, x, y, w, h, t)
        elif t < T["appelle"] - 0.05:
            u = prog(t, T["ferme"], 0.3, entree)
            ecran_google(cc, x, y, w, h, t)
            cc.save(); cc.translate(0, h * u); ecran_vieux(cc, x, y, w, h, t); cc.restore()
        else:
            ecran_appel(cc, x, y, w, h, t)
    with Calque(c, 1 - o):
        cy = mix(1500, 800, a)
        with Espace(c, 540, cy, ry=mix(-30, -6, a) + 4 * math.sin(t), s=1.0 - 0.3 * o):
            telephone_s(c, 540, cy, 520, 1040, ecran)
        # le doigt qui tape sur ton résultat, puis sur celui du concurrent
        for tt, yy in [(T["tombe"], 640), (T["appelle"] - 0.15, 790)]:
            f = prog(t, tt - 0.35, 0.3, sortie) * (1 - prog(t, tt + 0.25, 0.25, sortie))
            if f > 0:
                carte_s(c, 680 - 56, yy + 60 - 56 + 40 * (1 - f), 112, 112, 56, "#FFFFFF", None, 0.2, f)
                icone(c, "hand", 680, yy + 60 + 40 * (1 - f), 58, S["encre"], 2.2, f)
                clic(c, 640, yy, t, tt)
        # les tampons au mot près
        for lab, ic, tt, x, y, rot in [("LENT", "timer", T["lent"], 230, 420, -10), ("DATÉ", "calendar", T["date"], 860, 560, 8),
                                        ("ILLISIBLE", "eye-off", T["illisible"], 250, 1120, -6)]:
            if T["lent"] - 0.2 < t < T["ferme"] + 0.2:
                with Calque(c, 1 - prog(t, T["ferme"], 0.2, entree)):
                    tampon(c, lab, x, y, t, tt, 52, S["rouge"], rot, ic)
        if t > T["ferme"] - 0.05:
            b = entre(t, T["ferme"] - 0.05, 0.3, 2.4) * (1 - prog(t, T["appelle"] - 0.2, 0.2, entree))
            if b > 0:
                c.save(); c.translate(860, 380); c.scale(b, b); disque(c, 0, 0, 60, S["rouge"]); icone(c, "x", 0, 0, 64, "#FFFFFF", 3.4); c.restore()
        b = entre(t, T["autre"], 0.4, 2.2)
        if b > 0:
            pill(c, "Client perdu", 540, 300, 40, "rouge", "user-round", borne(b * 3), mix(0.4, 1, b), rot=-4)


# ═══════════════════════════════════════════ 3. 2019 → 2026
def scene_annee(c, t):
    g = Groupe(c, t, B["an"], B["com"] - 0.05, ent="zoom", sor="haut", cy=800)
    if not g.visible: return
    with g:
        a = entre(t, B["an"], 0.4, 1.6)
        pill(c, "On est en", 540, 520, 40, "blanc", "calendar", borne(a * 3), mix(0.4, 1, a))
        taille = 300
        w0 = largeur("20", taille, "noir", -0.04); wd = largeur("0", taille, "noir", -0.04)
        x = 540 - (w0 + 2 * wd) / 2; y = 620
        with Degrade(c, x, y, x + w0 + 2 * wd, y + taille, GRAD):
            texte(c, "20", x, y, taille, S["encre"], "noir", track=-0.04)
            rouleau(c, 2, x + w0, y, taille, t, T["deux"] - 0.1, T["vingt"] + 0.05, S["encre"])
            rouleau(c, 6, x + w0 + wd, y, taille, t, T["deux"] - 0.05, T["vingt"] + 0.25, S["encre"])
        if t < T["deux"] - 0.1:
            with Calque(c, 1 - prog(t, T["deux"] - 0.3, 0.2)):
                rrect(c, x, y, w0 + 2 * wd, taille * 1.05, 20, S["papier"])
                texte(c, "2019", 540, y, taille, S["grisClair"], "noir", "centre", -0.04)
        eclats(c, 540, 780, t, T["vingt"] + 0.3, 16, 460, graine=13)
        onde(c, 540, 780, t, T["vingt"] + 0.25, 120, 520, S["violetVif"], 8, 0.6)


# ═══════════════════════════════════════════ 4. ton site = ton premier commercial ; s'il vieillit, tu vieillis
def vieillir(c, x, y, w, h, u):
    if u <= 0: return
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#A8946B", 0.28 * u))
    for j in range(5):
        p = skia.Path(); px, py = x + w * (0.15 + 0.17 * j), y + h * (0.1 + 0.15 * (j % 3))
        p.moveTo(px, py)
        for q in range(5): px += 22 * ((q % 2) * 2 - 1) + 6; py += 34; p.lineTo(px, py)
        c.drawPath(p, peinture("#5E5241", 0.55 * u, Style=skia.Paint.kStroke_Style, StrokeWidth=3))


def scene_commercial(c, t):
    g = Groupe(c, t, B["com"], B["dy"] - 0.05, ent="droite", sor="recul", cy=800)
    if not g.visible: return
    with g:
        a = entre(t, B["com"] + 0.05, 0.5, 1.4)
        age = prog(t, T["vieux"] - 0.2, 0.6, entreeSortie)
        x, y, w, h = 110, 300, 860, 520
        with Calque(c, borne(a * 3)):
            navigateur(c, x, y, w, h, "ton-site.fr", lambda cc, xx, yy, ww, hh: (site_moderne(cc, xx, yy, ww, hh, t, 1 - age), vieillir(cc, xx, yy, ww, hh, age)))
        b = entre(t, T["premier"] - 0.1, 0.45, 2.0)
        if b > 0:
            c.save(); c.translate(820, 300); c.rotate(8); c.scale(mix(0.3, 1, b), mix(0.3, 1, b))
            pill(c, "Commercial n°1", 0, 0, 34, "grad", "briefcase", borne(b * 3) * (1 - age * 0.6))
            c.restore()
        # toi : la carte du patron qui grisonne avec son site
        d = entre(t, T["toi2"] - 0.15, 0.45, 1.8)
        if d > 0:
            gr = prog(t, T["vieux2"] - 0.1, 0.4, sortie)
            cx, cy = 540, 1120
            c.save(); c.translate(cx, cy); c.scale(mix(0.4, 1, d), mix(0.4, 1, d))
            with Calque(c, borne(d * 3)):
                carte_s(c, -330, -150, 660, 300, 40, ombre=0.14)
                c.save(); c.translate(-200, 0)
                disque(c, 0, 0, 92, mix_hex(S["violet"], "#9C9AA3", gr)); icone(c, "user-round", 0, 0, 100, "#FFFFFF", 2.2)
                c.restore()
                texte(c, "Toi", -70, -78, 56, S["encre"], "titre", track=-0.02)
                texte(c, "Le patron", -70, -10, 30, S["gris"], "demi", track=0)
                if gr > 0: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-330, -150, 660, 300), 40, 40), peinture("#A8946B", 0.22 * gr))
            c.restore()
            tampon(c, "DÉPASSÉ", 760, 1230, t, T["vieux2"], 50, S["rouge"], -8, "trending-down")


def mix_hex(a, b, u):
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]; cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * u):02X}" for x, y in zip(ca, cb))


# ═══════════════════════════════════════════ 5. DYOU : le site qui travaille
def ecran_dyou(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), peinture("#FFFFFF"))
    k = w / 480
    hero = prog(t, T["moderne"] - 0.1, 0.4, sortieExpo)
    # avant « moderne » : le squelette du site qui se construit, bloc par bloc, avec un reflet qui balaie
    if hero < 1:
        blocs = [(24, 60, 140, 26), (24, 140, 380, 60), (24, 212, 300, 60), (24, 300, 260, 22), (24, 380, 200, 64), (240, 380, 200, 64),
                 (24, 480, 432, 80), (24, 576, 432, 80), (24, 672, 432, 80)]
        for j, (bx, by, bw, bh) in enumerate(blocs):
            u = prog(t, B["dy"] + 0.35 + 0.06 * j, 0.3, sortieExpo)
            if u > 0: rrect(c, x + bx * k, y + by * k, bw * k * u, bh * k, 14 * k, S["lavande"])
        sh = ((t - B["dy"]) * 1.4) % 1
        p = skia.Paint(AntiAlias=True); yy = y + h * mix(-0.2, 1.2, sh)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, yy - 120), skia.Point(x, yy + 120)], [hexa("#FFFFFF", 0), hexa("#FFFFFF", 0.7), hexa("#FFFFFF", 0)]))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h * hero + 1))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h * 0.5), pgrad(x, y, x + w, y + h * 0.5, ["#5B2BD6", "#7B3FF2", "#4F6FE8"]))
    texte(c, "MARTIN", x + 30 * k, y + 80 * k, 24 * k, "#FFFFFF", "noir", track=0.1)
    texte(c, "Plomberie,", x + 30 * k, y + 150 * k, 54 * k, "#FFFFFF", "titre", track=-0.035)
    texte(c, "sans attendre.", x + 30 * k, y + 212 * k, 54 * k, "#E3D6FF", "titre", track=-0.035)
    texte(c, "Dépannage et rénovation, Lyon", x + 30 * k, y + 290 * k, 22 * k, "#E3D6FF", "demi", track=0)
    c.restore()
    # chargement instantané
    if T["rapide"] - 0.1 < t < T["rapide"] + 0.5:
        u = prog(t, T["rapide"] - 0.1, 0.18, sortieExpo)
        rrect(c, x, y + 44 * k, w * u, 6, 3, "#FFFFFF", 1 - prog(t, T["rapide"] + 0.2, 0.25))
    # l'offre claire : trois services
    for j, (ic, lab) in enumerate([("wrench", "Dépannage"), ("house", "Rénovation"), ("shield-check", "Garantie")]):
        a = entre(t, T["offre"] - 0.1 + 0.08 * j, 0.4, 1.8)
        if a <= 0: continue
        yy = y + (h * 0.5 + 24 * k) + j * 92 * k + 30 * (1 - a)
        with Calque(c, borne(a * 3)):
            carte_s(c, x + 24 * k, yy, w - 48 * k, 78 * k, 20 * k, ombre=0.08)
            tuile(c, ic, x + 66 * k, yy + 39 * k, 50 * k, "doux")
            texte(c, lab, x + 104 * k, yy + 39 * k - hauteurLigne(26 * k, "fort") / 2, 26 * k, S["encre"], "fort", track=0)
            icone(c, "check", x + w - 60 * k, yy + 39 * k, 28 * k, S["vert"], 3.0)
    # les deux boutons
    for j, (lab, ic, col, tt) in enumerate([("Appeler", "phone", S["violet"], T["appeler"]), ("WhatsApp", "message-circle", VERT_WA, T["whatsapp"])]):
        a = entre(t, tt - 0.15, 0.4, 2.2)
        if a <= 0: continue
        bx = x + 24 * k + j * (w - 48 * k) / 2 + 6 * j * k; bw = (w - 60 * k) / 2; by = y + h - 120 * k
        pu = 1 + 0.05 * max(0, math.sin((t - tt) * 7)) * (1 - borne((t - tt) / 1.2))
        c.save(); c.translate(bx + bw / 2, by + 36 * k); c.scale(mix(0.4, 1, a) * pu, mix(0.4, 1, a) * pu)
        rrect(c, -bw / 2, -36 * k, bw, 72 * k, 36 * k, col)
        icone(c, ic, -bw / 2 + 40 * k, 0, 28 * k, "#FFFFFF", 2.6)
        texte(c, lab, 14 * k, -hauteurLigne(24 * k, "fort") / 2, 24 * k, "#FFFFFF", "fort", "centre", 0)
        c.restore()


def scene_dyou(c, t):
    g = Groupe(c, t, B["dy"], B["prix"] + 0.3, ent="bas", sor="aucune", cy=800)
    if not g.visible: return
    with g:
        a = entre(t, B["dy"] + 0.05, 0.5, 1.5)
        iw, ih = taille_img("dyou-logo-horizontal-black"); lw = 420 * mix(0.6, 1, a)
        with Calque(c, borne(a * 3)):
            image(c, "dyou-logo-horizontal-black", 540 - lw / 2, 150 - lw * ih / iw / 2, lw)
        b = entre(t, B["dy"] + 0.2, 0.55, 1.3)
        if b > 0:
            rot = mix(-25, -8, b) + 3 * math.sin(t * 1.2)
            with Espace(c, 540, 840, ry=rot, rx=4, s=mix(0.7, 1, b)):
                telephone_s(c, 540, 840, 470, 940, lambda cc, x, y, w, h: ecran_dyou(cc, x, y, w, h, t), borne(b * 3))
        for k, (lab, ic, tt, x, y, rot) in enumerate([("Moderne", "sparkles", T["moderne"], 170, 430, -6), ("Rapide", "zap", T["rapide"], 920, 560, 6),
                                                      ("Mobile", "smartphone", T["tel2"], 165, 760, -4), ("Offre claire", "lightbulb", T["claire"], 910, 960, 5)]):
            d = entre(t, tt - 0.1, 0.4, 2.2)
            if d > 0: pill(c, lab, x, y, 32, "blanc" if k % 2 else "grad", ic, borne(d * 3), mix(0.4, 1, d), rot)
        # Google te trouve : la fiche résultat qui sort du téléphone
        e = entre(t, T["google2"] - 0.1, 0.5, 1.6)
        if e > 0:
            c.save(); c.translate(540, 300); c.rotate(-3); c.scale(mix(0.5, 1, e), mix(0.5, 1, e))
            with Calque(c, borne(e * 3)):
                carte_s(c, -400, -82, 800, 164, 32, ombre=0.16)
                cols = ["#4285F4", "#EA4335", "#FBBC05", "#4285F4", "#34A853", "#EA4335"]
                gx = -360
                for j, ch in enumerate("Google"): texte(c, ch, gx, -60, 30, cols[j], "fort", track=0); gx += largeur(ch, 30, "fort", 0)
                texte(c, "Martin Plomberie · Lyon", -360, -10, 34, "#1A0DAB", "fort", track=-0.01)
                texte(c, "martin-plomberie.fr", -360, 34, 22, "#5F6368", "demi", track=0)
                tr = entre(t, T["trouve"] - 0.05, 0.35, 2.4)
                if tr > 0:
                    c.save(); c.translate(320, 0); c.scale(tr, tr); disque(c, 0, 0, 46, S["vert"]); icone(c, "check", 0, 0, 52, "#FFFFFF", 3.4); c.restore()
            c.restore()


# ═══════════════════════════════════════════ 6. prix
def scene_prix(c, t):
    t_in, t_out = B["prix"], B["cta"]
    if t < t_in or t > t_out + 0.5: return
    R = cles(t, [(t_in, 0), (t_in + 0.42, 1500, sortieExpo), (t_out, 1500), (t_out + 0.4, 0, entreeSortie)])
    def dessin(cc):
        fond_grad(cc, t)
        rayons(cc, 540, 860, t, 1100, 0.10)
        a = entre(t, T["vitrine"] - 0.05, 0.4, 1.6)
        texte(cc, "SITE VITRINE", 540, 420 + 20 * (1 - a), 56, "#FFFFFF", "titre", "centre", 0.12, borne(a * 3))
        b = entre(t, T["des"] - 0.05, 0.4, 1.6)
        texte(cc, "DÈS", 540, 510 + 20 * (1 - b), 40, "#E3D6FF", "titre", "centre", 0.2, borne(b * 3))
        taille = 300
        ws = [largeur(ch, taille, "noir", -0.04) for ch in "490"]
        we = largeur("€", 190, "noir", -0.02)
        x = 540 - (sum(ws) + we + 30) / 2; y = 600
        arr = [T["quatre"] + 0.1, T["qvd"] + 0.15, T["euros"] - 0.06]
        for k, ch in enumerate("490"):
            rouleau(cc, int(ch), x, y, taille, t, T["quatre"] - 0.15 + 0.04 * k, arr[k]); x += ws[k]
        e = entre(t, T["euros"] - 0.05, 0.4, 2.6)
        if e > 0:
            cc.save(); cc.translate(x + 30 + we / 2, y + 110); cc.scale(mix(0.2, 1, e), mix(0.2, 1, e))
            texte(cc, "€", 0, -hauteurLigne(190) / 2 + 20, 190, "#FFFFFF", "noir", "centre", -0.02); cc.restore()
        onde(cc, 540, 760, t, T["euros"], 120, 560, "#FFFFFF", 8, 0.7)
        eclats(cc, 540, 760, t, T["euros"] + 0.02, 16, 520, ["#FFFFFF", "#E3D6FF", S["or_"], "#C9D8FF"], graine=4, duree=0.9)
        for k, (lab, ic, tt) in enumerate([("Sans abonnement", "circle-slash", T["sans"]), ("Le site est à toi", "key-round", T["atoi"]),
                                           ("Maquette offerte", "gift", T["atoi"] + 0.15)]):
            d = entre(t, tt - 0.1, 0.4, 2.2)
            if d > 0: pill(cc, lab, 540, 1050 + 100 * k, 34, "blanc", ic, borne(d * 3), mix(0.4, 1, d))
    iris(c, 540, 860, R, dessin)


# ═══════════════════════════════════════════ 7. clique sur le lien
def scene_cta(c, t):
    t0 = B["cta"]
    if t < t0: return
    a = entre(t, t0 + 0.05, 0.55, 1.5)
    iw, ih = taille_img("dyou-logo-horizontal-black"); lw = 600 * mix(0.6, 1, a)
    c.save(); flou_calque(c, 14 * (1 - prog(t, t0 + 0.05, 0.35, sortie)), borne(a * 3))
    image(c, "dyou-logo-horizontal-black", 540 - lw / 2, 330 - lw * ih / iw / 2, lw)
    c.restore(); c.restore()
    lettres(c, "CLIQUE SUR", 540, 560, 112, t, T["clique"] - 0.05, "ressort", decal=0.03, grad=False, couleur=S["encre"])
    lettres(c, "LE LIEN", 540, 690, 132, t, T["lien"] - 0.1, "ressort", decal=0.04)
    # la flèche qui pointe vers le lien sous la vidéo
    b = entre(t, T["lien"] + 0.05, 0.4, 2.0)
    if b > 0:
        bob = 26 * abs(math.sin((t - T["lien"]) * 4.5))
        c.save(); c.translate(540, 900 + bob); c.scale(b, b)
        disque(c, 0, 0, 70, S["violet"], 1.0, (8, 24, 0.25)); icone(c, "arrow-down", 0, 0, 72, "#FFFFFF", 3.0)
        c.restore()
    bt = entre(t, T["maquette"] - 0.1, 0.5, 1.8)
    tc = T["maquette"] + 0.55
    ap = prog(t, tc - 0.06, 0.06, sortie) * (1 - prog(t, tc + 0.05, 0.14, sortie))
    if bt > 0:
        bouton(c, "Recevoir ma maquette gratuite", 540, 1110, 36, mix(0.2, 1, bt) * (1 - 0.07 * ap), borne(bt * 3), "gift")
    cu = prog(t, tc - 0.5, 0.45, sortie)
    if cu > 0:
        curseur(c, mix(960, 760, cu), mix(1400, 1130, cu), 1.1, 1 - prog(t, tc + 0.6, 0.3, sortie), ap)
        clic(c, 760, 1122, t, tc)
    eclats(c, 540, 1110, t, tc + 0.02, 12, 420, graine=12)
    for k, (lab, ic) in enumerate([("dès 490 €", "sparkles"), ("sans abonnement", "circle-slash"), ("dyou-agency.com", "globe")]):
        d = entre(t, T["fin"] + 0.3 + 0.08 * k, 0.4, 2.2)
        if d > 0: pill(c, lab, [215, 540, 865][k], 1290, 24, "doux", ic, borne(d * 3), mix(0.4, 1, d))


# ═══════════════════════════════════════════ sons
son(0.0, "impact", -7); son(0.05, "whoosh_court", -12); son(0.23, "whoosh_court", -13)
son(T["pas"] - 0.15, "pop", -12); son(T["toi"] - 0.2, "pop", -13)
son(T["juste"] - 0.1, "swipe", -11); son(T["msite"] - 0.05, "montee", -12); son(T["msite"] + 0.1, "ching", -9); son(T["msite"] + 0.25, "impact_doux", -11)
son(B["g"] - 0.2, "whoosh_long", -9)
for i in range(13): son(T["cherche"] + i * 0.035, "frappe", -18)
for j in range(3): son(T["google"] + 0.08 * j, "pop", -15)
son(T["tombe"], "clic", -7); son(T["site"], "tick", -16)
for i in range(6): son(T["site"] + 0.1 + i * 0.09, "tick", -19)
for k in ("lent", "date", "illisible"): son(T[k] - 0.12, "tampon", -8)
son(T["ferme"] - 0.05, "swipe", -9); son(T["ferme"], "croc", -10)
son(T["appelle"] - 0.15, "clic", -7); son(T["appelle"], "ding", -12); son(T["autre"], "impact", -8)
son(B["an"] - 0.05, "whoosh", -9)
for i in range(16): son(T["deux"] - 0.1 + i * 0.04, "tick", -17)
son(T["vingt"] + 0.25, "impact", -6); son(T["vingt"] + 0.3, "ching", -10)
son(B["com"] - 0.05, "whoosh_court", -10); son(T["premier"] - 0.1, "pop", -11)
son(T["vieux"] - 0.2, "whoosh_bas", -11); son(T["toi2"] - 0.15, "pop", -12); son(T["vieux2"] - 0.12, "tampon", -8)
son(B["dy"] - 0.05, "whoosh_long", -9); son(B["dy"] + 0.1, "verre", -11)
son(T["moderne"] - 0.25, "whoosh", -10)
for k in ("moderne", "rapide", "tel2", "claire"): son(T[k] - 0.1, "pop", -12)
son(T["rapide"] - 0.1, "whoosh_court", -12)
for j in range(3): son(T["offre"] - 0.1 + 0.08 * j, "blip", -15)
son(T["appeler"] - 0.15, "pop", -10); son(T["whatsapp"] - 0.15, "message_in", -9)
son(T["google2"] - 0.1, "swipe", -11); son(T["trouve"] - 0.05, "check", -9)
son(B["prix"], "whoosh_bas", -8); son(T["vitrine"], "pop", -12)
for i in range(14): son(T["quatre"] - 0.15 + i * (T["euros"] - T["quatre"]) / 14, "tick", -17)
son(T["euros"] - 0.06, "impact", -5); son(T["euros"], "ching", -9)
son(T["sans"] - 0.1, "pop", -12); son(T["atoi"] - 0.1, "pop", -12); son(T["atoi"] + 0.05, "pop", -13)
son(B["cta"], "whoosh", -9); son(B["cta"] + 0.05, "verre", -11); son(T["lien"] + 0.05, "impact_doux", -9)
son(T["maquette"] - 0.1, "pop", -11); son(T["maquette"] + 0.55, "clic", -6); son(T["maquette"] + 0.6, "ching", -11)
son(DUREE - 1.2, "ding", -16)
for a, b in [(0.0, 0.25), (B["g"] - 0.2, B["g"] + 0.3), (T["ferme"] - 0.05, T["ferme"] + 0.3), (B["an"] - 0.1, B["an"] + 0.3),
             (T["deux"] - 0.1, T["vingt"] + 0.3), (B["dy"] - 0.1, B["dy"] + 0.3), (B["prix"], B["prix"] + 0.4), (B["cta"], B["cta"] + 0.3)]:
    rapide(a, b)
for tt, cc_, a_ in [(T["msite"] + 0.1, "#FFFFFF", 0.25), (T["autre"], S["rouge"], 0.08), (T["vingt"] + 0.25, "#FFFFFF", 0.3),
                    (T["euros"] - 0.06, "#FFFFFF", 0.22), (T["lien"] + 0.05, S["violetVif"], 0.06)]:
    eclair(tt, cc_, a_)


def dessine(c, t):
    fond_studio(c, t, battement(t, T["msite"] + 0.1, 1, 0.5) + battement(t, T["vingt"] + 0.25, 1, 0.5) - 2)
    hook(c, t)
    scene_google(c, t)
    scene_annee(c, t)
    scene_commercial(c, t)
    scene_dyou(c, t)
    scene_cta(c, t)
    scene_prix(c, t)
    K.dessine_eclairs(c, t)
    if t < B["prix"] - 0.1: SOUS.dessine(c, t, S["encre"])
