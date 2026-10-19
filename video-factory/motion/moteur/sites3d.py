"""Pubs US DYOU « sites » en 3D (DA-M15-EN, DA-M16-EN, 17/10/2026) — même style que studio3d, sans prix.

Promesses tirées de la page anglaise du site (dyou-agency.com/en) : maquette gratuite (« Free mockup »), mobile-first,
SEO et performance, appels à l'action. Rien sur l'abonnement ni la propriété du site côté anglais : on ne le dit pas.
Corps commun (texte `CORPS`) : la recherche Google → ton site lent, daté, illisible → il appelle l'autre → ton site est
ton premier commercial → ce qu'on construit (moderne, rapide, mobile, offre claire, bouton d'appel) → trouvé sur Google →
maquette offerte → fin « take off » de studio3d → carton « Get my free mockup ».
"""
import math
import skia
from moteur import *
from studio import *
from studio3d import *
import studio

CORPS = ("A customer searches on Google. Your site is slow, outdated, hard to read on a phone. So they call someone else. "
         "Your website is your first salesperson. We build sites that are modern, fast, made for phones, with a clear offer "
         "and a call button up front. Built to be found on Google. And we design your first mockup for free. "
         "We make your business take off. Tap the link.")
_REPERES = dict(g0=0, cherche=2, google=4, site=6, lent=8, date=9, illisible=10, tel_=15, donc=16, appelle=18, autre=20,
                v0=21, vendeur=26, b0=27, moderne=32, rapide=33, mobile=36, offre=40, bouton=43, devant=46,
                s0=47, trouve=50, google2=52, m0=53, maquette=58, gratuit=60,
                decolle=61, business=64, take=65, devis=67, url=69)


def reperes(TW, n_hook):
    return {k: TW(v + n_hook) for k, v in _REPERES.items()}


def config_sites():
    from studio_en import anglais
    anglais(prix=False)
    studio.TR["Ton offre, en mouvement."] = "Your business, online."
    studio.TR["Demander mon devis"] = "Get my free mockup"
    studio.CTA_PILLS = [("Mobile-first", "smartphone"), ("Built for Google", "search"), ("Free mockup", "gift")]


# ─────────────────────────────────────────── faux sites
def site_vieux(t, charge=True):
    """le site daté : beige, minuscule, image cassée, chargement qui tourne"""
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#E8E4DA"))
        c.drawRect(skia.Rect.MakeWH(w, 70 * k), peinture("#7D7B76"))
        texte(c, "MOREL PLUMBING INC.", 16 * k, 24 * k, 18 * k, "#EDEBE6", "fort", track=0.02)
        texte(c, "Welcome to our website !!!", 16 * k, 92 * k, 15 * k, "#3B5BA8", "demi", track=0)
        rrect(c, 16 * k, 124 * k, w - 32 * k, 230 * k, 0, "#CFCBC2")
        icone(c, "image-off", w / 2, 239 * k, 70 * k, "#9E9A92", 1.6)
        for j in range(16):
            rrect(c, 16 * k, (380 + j * 20) * k, (w - 32 * k) * (0.55 + 0.4 * ((j * 37) % 10) / 10), 7 * k, 0, "#A8A49B")
        texte(c, "Click here", 16 * k, 712 * k, 14 * k, "#3B5BA8", "demi", track=0)
        texte(c, "Copyright 2009", 16 * k, h - 40 * k, 13 * k, "#8E8A82", "demi", track=0)
        if charge:
            c.drawRect(skia.Rect.MakeWH(w, h), peinture("#FFFFFF", 0.35))
            R = 46 * k
            pa = peinture(S["gris"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=9 * k); pa.setStrokeCap(skia.Paint.kRound_Cap)
            arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(w / 2 - R, h * 0.45 - R, 2 * R, 2 * R), (t * 400) % 360, 260)
            c.drawPath(arc, pa)
    return f


def site_moderne(t, nom="Morel Plumbing", appui=0.0):
    """le site DYOU : clair, titre fort, bouton d'appel en évidence"""
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#FFFFFF"))
        c.save(); c.translate(0, 0)
        rrect(c, 20 * k, 26 * k, 40 * k, 40 * k, 12 * k, S["violet"]); icone(c, "wrench", 40 * k, 46 * k, 24 * k, "#FFFFFF", 2.4)
        texte(c, nom, 72 * k, 32 * k, 24 * k, S["encre"], "titre", track=-0.02)
        for j in range(3): rrect(c, w - 44 * k, (34 + j * 10) * k, 22 * k, 3 * k, 1.5 * k, S["encre"])
        c.drawRoundRect(skia.Rect.MakeXYWH(16 * k, 90 * k, w - 32 * k, 360 * k), 26 * k, 26 * k, pgrad(0, 90 * k, w, 450 * k, GRAD_VIF))
        lueur_s(c, w * 0.7, 200 * k, 160 * k, "#FFFFFF", 0.22)
        texte(c, "Fast repairs.", 40 * k, 130 * k, 48 * k, "#FFFFFF", "noir", track=-0.03)
        texte(c, "Same-day service.", 40 * k, 190 * k, 28 * k, "#E3D6FF", "titre", track=-0.02)
        for j in range(5): icone(c, "star", (52 + j * 30) * k, 262 * k, 22 * k, S["or_"], 2.4)
        s_ = (1 + 0.05 * math.sin(t * 6)) * (1 - 0.08 * appui)
        c.save(); c.translate(40 * k + 150 * k / 2 * 1.4, 345 * k); c.scale(s_, s_)
        rrect(c, -105 * k, -32 * k, 210 * k, 64 * k, 32 * k, S["vert"])
        icone(c, "phone", -62 * k, 0, 28 * k, "#FFFFFF", 2.6)
        texte(c, "Call now", -38 * k, -hauteurLigne(26 * k, "titre") / 2, 26 * k, "#FFFFFF", "titre", track=-0.01)
        c.restore()
        for j, (ic, lab) in enumerate([("droplet", "Leaks"), ("wrench", "Repairs"), ("house", "Installs")]):
            x = 16 * k + j * (w - 32 * k) / 3
            rrect(c, x + 4 * k, 476 * k, (w - 32 * k) / 3 - 8 * k, 140 * k, 20 * k, S["doux"])
            tuile(c, ic, x + (w - 32 * k) / 6, 526 * k, 52 * k, "doux")
            texte(c, lab, x + (w - 32 * k) / 6, 572 * k, 20 * k, S["encre"], "titre", "centre", -0.01)
        rrect(c, 16 * k, 640 * k, w - 32 * k, 120 * k, 20 * k, "#FFFFFF", 1.0, None, S["ligne"], 2 * k)
        disque(c, 56 * k, 700 * k, 22 * k, S["lilas"])
        rrect(c, 92 * k, 684 * k, 200 * k, 12 * k, 6 * k, S["ligne"]); rrect(c, 92 * k, 706 * k, 140 * k, 12 * k, 6 * k, S["ligne"])
        for j in range(5): icone(c, "star", (300 + j * 22) * k, 700 * k, 16 * k, S["or_"], 2.2)
        c.restore()
    return f


def resultat(nom, url, moderne, alpha=1.0):
    def f(c, w, h):
        rrect(c, 0, 0, w, h, 30, "#FFFFFF", 1.0, None, S["ligne"] if not moderne else S["lilas"], 3 if not moderne else 5)
        if moderne:
            disque(c, 50, 50, 22, S["violet"]); icone(c, "wrench", 50, 50, 22, "#FFFFFF", 2.4)
        else:
            disque(c, 50, 50, 22, "#CFCBD6")
        texte(c, url, 86, 34, 24, S["gris"], "demi", track=0)
        texte(c, nom, 30, 92, 38, S["violet"] if moderne else "#6E6878", "titre", track=-0.02)
        rrect(c, 30, 156, w - 120, 14, 7, S["ligne"]); rrect(c, 30, 182, w - 220, 14, 7, S["ligne"])
    return f


def barre_recherche(c, t, t0, requete, y=210, alpha=1.0):
    with Calque(c, alpha):
        carte_s(c, 120, y - 50, 840, 100, 50, "#FFFFFF", None, 0.16)
        icone(c, "search", 180, y, 40, S["violet"], 2.6)
        n = int(borne((t - t0) / 0.55) * len(requete) + 0.999) if t > t0 else 0
        texte(c, requete[:n], 220, y - hauteurLigne(40, "titre") / 2, 40, S["encre"], "titre", track=-0.01)
        if int(t * 3) % 2 == 0: rrect(c, 224 + largeur(requete[:n], 40, "titre", -0.01), y - 22, 4, 44, 2, S["violet"])


PW, PH = 470, 960


# ─────────────────────────────────────────── C1 : la recherche, ton vieux site, il appelle l'autre
def scene_recherche(c, t, M):
    g = Groupe(c, t, M["g0"] - 0.12, M["v0"] - 0.05, ent="zoom", sor="gauche", d_out=0.32)
    if not g.visible: return
    with g:
        plonge = prog(t, M["site"] - 0.3, 0.6, entreeSortie)
        bascule = prog(t, M["donc"] - 0.1, 0.6, entreeSortie)
        # résultats de recherche en perspective
        if plonge < 1:
            cam = Cam(ax=mix(-26, -10, plonge), ay=6 * math.sin(t * 0.8), tz=mix(200, -900, plonge), cy=1000)
            plans = []
            for k, (nom, url, mod) in enumerate([("Morel Plumbing", "morelplumbing.com", False), ("Pro Plumbing Co.", "proplumbing.co", True),
                                                 ("City Pipes", "citypipes.net", False)]):
                a = prog(t, M["g0"] + 0.15 + 0.12 * k, 0.45, sortieExpo)
                if a <= 0: continue
                plans.append(Plan(coins((0, -280 + k * 270, mix(600, 0, a)), 840, 230), 840, 230, resultat(nom, url, mod), borne(a * 3) * (1 - plonge)))
            scene3d(c, cam, plans)
            if t > M["site"] - 0.4:
                eti = entre(t, M["site"] - 0.35, 0.4, 2.4) * (1 - plonge)
                pill(c, "Your site", 260, 560, 32, "encre", "arrow-down", borne(eti * 3), mix(0.4, 1, eti), rot=-4)
            barre_recherche(c, t, M["cherche"], "plumber near me", 210, 1 - plonge)
        # le vieux site dans le téléphone, puis le site du concurrent
        if plonge > 0:
            cam = Cam(ax=4 * math.sin(t * 0.9), ay=mix(30, -14, plonge) + 3 * math.sin(t * 0.7) - 60 * bascule, tz=mix(1400, 80, plonge), cy=880, tx=-300 * bascule)
            plans = [Plan(coins((0, 0, 0), PW, PH), PW, PH, tel(site_vieux(t)), 1 - borne(bascule * 1.4))]
            scene3d(c, cam, plans)
            for k, (lab, ic, cle, x, y, r) in enumerate([("Slow", "hourglass", "lent", 290, 470, -6), ("Outdated", "calendar", "date", 800, 740, 5),
                                                        ("Hard to read", "eye-off", "illisible", 330, 1060, -3)]):
                e = entre(t, M[cle] - 0.1, 0.4, 2.6) * (1 - bascule)
                if e <= 0: continue
                c.save(); c.translate(x, y); c.rotate(r); z = mix(2.2, 1, prog(t, M[cle] - 0.1, 0.18, entree)); c.scale(z, z)
                pill(c, lab, 0, 0, 50, "rouge", ic, borne(e * 3))
                c.restore()
        if bascule > 0:
            appui = prog(t, M["appelle"] - 0.05, 0.08, sortie) * (1 - prog(t, M["appelle"] + 0.1, 0.15, sortie))
            cam = Cam(ay=mix(70, 0, bascule) + 4 * math.sin(t * 0.8), ax=3 * math.sin(t), tz=mix(600, 40, bascule), cy=880, tx=mix(500, 0, bascule))
            scene3d(c, cam, [Plan(coins((0, 0, 0), PW, PH), PW, PH, tel(site_moderne(t, "Pro Plumbing Co.", appui)))])
            pill(c, "Someone else", 540, 300, 36, "grad", "users", borne(bascule * 3), mix(0.4, 1, bascule), rot=3)
            cu = prog(t, M["appelle"] - 0.45, 0.4, sortie)
            if cu > 0:
                cx_, cy_ = 430, 880 - PH / 2 + 345 * PH / 960 * 0.98 + 30
                curseur(c, mix(900, cx_, cu), mix(1500, cy_, cu), 1.2, 1 - prog(t, M["autre"] + 0.3, 0.3), appui)
                clic(c, cx_, cy_, t, M["appelle"])
            ap = entre(t, M["appelle"] + 0.15, 0.45, 2.0)
            if ap > 0:
                c.save(); c.translate(540, 1230); c.scale(mix(0.5, 1, ap), mix(0.5, 1, ap))
                with Calque(c, borne(ap * 3)):
                    carte_s(c, -330, -70, 660, 140, 70, "#FFFFFF", None, 0.2)
                    disque(c, -260, 0, 48, S["vert"]); icone(c, "phone", -260, 0, 46, "#FFFFFF", 2.6)
                    texte(c, "Calling Pro Plumbing…", -195, -hauteurLigne(34, "titre") / 2, 34, S["encre"], "titre", track=-0.02)
                c.restore()
                onde(c, 280, 1230, t, M["appelle"] + 0.2, 40, 200, S["vert"], 6, 0.6)


# ─────────────────────────────────────────── C2 : ton site, ton premier commercial
def scene_vendeur(c, t, M):
    g = Groupe(c, t, M["v0"] - 0.1, M["b0"] - 0.05, ent="droite", sor="zoom", d_in=0.36)
    if not g.visible: return
    with g:
        lettres(c, "YOUR FIRST", 540, 230, 96, t, M["v0"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
        lettres(c, "SALESPERSON", 540, 340, 118, t, M["vendeur"] - 0.15, "ressort", decal=0.035)
        a = entre(t, M["v0"] - 0.05, 0.6, 1.3)
        cam = Cam(ax=-8 + 3 * math.sin(t), ay=mix(-50, 18, a) + 4 * math.sin(t * 0.8), tz=mix(900, 330, a), cy=900)
        def nav(cc, w, h):
            rrect(cc, 0, 0, w, h, 34, "#FFFFFF", 1.0, None, S["ligne"], 3)
            rrect(cc, 0, 0, w, 64, 0, S["doux"])
            for j, col in enumerate(["#FF6B6B", "#FFC53D", "#2E9E68"]): disque(cc, 34 + j * 30, 32, 9, col)
            rrect(cc, 140, 16, w - 200, 32, 16, "#FFFFFF"); texte(cc, "yourbusiness.com", 170, 20, 22, S["gris"], "demi", track=0)
            cc.save(); cc.translate(0, 64)
            site_moderne(t, "Your business")(cc, w, h - 64)
            cc.restore()
        scene3d(c, cam, [Plan(coins((0, 0, 0), 760, 900), 760, 900, nav)])
        for k, (lab, ic, x, y, r) in enumerate([("Open 24/7", "clock", 230, 640, -5), ("Talks to every visitor", "message-circle", 760, 1180, 4)]):
            b = entre(t, M["v0"] + 0.3 + 0.35 * k, 0.4, 2.4)
            if b > 0: pill(c, lab, x, y, 34, "blanc" if k else "grad", ic, borne(b * 3), mix(0.4, 1, b), rot=r)


# ─────────────────────────────────────────── C3 : ce qu'on construit
def scene_construit(c, t, M):
    g = Groupe(c, t, M["b0"] - 0.1, M["s0"] - 0.05, ent="bas", sor="recul", d_in=0.45)
    if not g.visible: return
    with g:
        a = entre(t, M["b0"] - 0.05, 0.6, 1.3)
        mob = prog(t, M["mobile"] - 0.15, 0.6, entreeSortie)
        appui = prog(t, M["bouton"] + 0.2, 0.08, sortie) * (1 - prog(t, M["bouton"] + 0.35, 0.15, sortie))
        cam = Cam(ax=-10 + 3 * math.sin(t * 0.9), ay=mix(40, 22, a) - 30 * mob + 4 * math.sin(t * 0.6), tz=mix(1200, 420, a), cy=860)
        def nav(cc, w, h):
            rrect(cc, 0, 0, w, h, 30, "#FFFFFF", 1.0, None, S["ligne"], 3)
            rrect(cc, 0, 0, w, 56, 0, S["doux"])
            for j, col in enumerate(["#FF6B6B", "#FFC53D", "#2E9E68"]): disque(cc, 30 + j * 26, 28, 8, col)
            cc.save(); cc.translate(0, 56); cc.scale(1, (h - 56) / h)
            site_moderne(t, "Morel Plumbing")(cc, w, h)
            cc.restore()
        plans = [Plan(coins((-160, -120, 300), 760, 860), 760, 860, nav, 1 - 0.4 * mob),
                 Plan(coins((mix(420, 200, mob), mix(160, 40, mob), mix(-60, -260, mob)), PW * 0.82, PH * 0.82, ay=mix(-14, 10, mob)), PW * 0.82, PH * 0.82,
                      tel(site_moderne(t, "Morel Plumbing", appui)), borne(prog(t, M["b0"] + 0.1, 0.5) * 3))]
        scene3d(c, cam, plans)
        lettres(c, "WE BUILD", 540, 200, 120, t, M["b0"] - 0.05, "ressort", decal=0.035)
        for k, (lab, ic, cle, x, y, r, mode) in enumerate([("Modern", "sparkles", "moderne", 220, 420, -6, "grad"), ("Fast", "zap", "rapide", 860, 520, 5, "encre"),
                                                         ("Made for phones", "smartphone", "mobile", 270, 1180, -3, "blanc"),
                                                         ("Clear offer", "target", "offre", 800, 1020, 4, "grad"), ("Call button", "phone", "bouton", 300, 820, -4, "vert")]):
            e = entre(t, M[cle] - 0.12, 0.4, 2.4)
            if e <= 0: continue
            c.save(); c.translate(x, y + 10 * math.sin(t * 2 + k)); c.rotate(r); z = mix(1.8, 1, prog(t, M[cle] - 0.12, 0.2, entree)); c.scale(z, z)
            pill(c, lab, 0, 0, 36, mode, ic, borne(e * 3))
            c.restore()
        # jauge de vitesse sur « fast »
        f = entre(t, M["rapide"] - 0.1, 0.5, 1.6) * (1 - prog(t, M["mobile"] - 0.2, 0.3))
        if f > 0:
            with Calque(c, borne(f * 3)):
                cx_, cy_ = 860, 680
                carte_s(c, cx_ - 120, cy_ - 90, 240, 150, 30, ombre=0.14)
                pa = peinture(S["lavande"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=14); pa.setStrokeCap(skia.Paint.kRound_Cap)
                arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(cx_ - 70, cy_ - 50, 140, 140), 180, 180); c.drawPath(arc, pa)
                v = ressort(prog(t, M["rapide"], 0.6, lin), 1.6, 4) if t > M["rapide"] else 0
                pg = pgrad(cx_ - 70, 0, cx_ + 70, 0, [S["vert"], "#7BD88F"]); pg.setStyle(skia.Paint.kStroke_Style); pg.setStrokeWidth(14); pg.setStrokeCap(skia.Paint.kRound_Cap)
                arc2 = skia.Path(); arc2.addArc(skia.Rect.MakeXYWH(cx_ - 70, cy_ - 50, 140, 140), 180, 175 * min(1.03, v)); c.drawPath(arc2, pg)
                ang = math.radians(180 + 175 * min(1.03, v))
                trait(c, cx_, cy_ + 20, cx_ + 52 * math.cos(ang), cy_ + 20 + 52 * math.sin(ang), S["encre"], 6)
        if t > M["bouton"] + 0.2:
            onde(c, 650, 900, t, M["bouton"] + 0.25, 40, 240, S["vert"], 8, 0.6)


# ─────────────────────────────────────────── C4 : trouvé sur Google
def scene_google(c, t, M):
    g = Groupe(c, t, M["s0"] - 0.1, M["m0"] - 0.05, ent="grand", sor="haut", d_in=0.45)
    if not g.visible: return
    with g:
        barre_recherche(c, t, M["s0"] + 0.05, "plumber near me", 230)
        cam = Cam(ax=-22 + 3 * math.sin(t), ay=8 * math.sin(t * 0.7), tz=150, cy=1000)
        monte = prog(t, M["trouve"] - 0.15, 0.6, lambda v: ressort(v, 1.3, 4.6)) if t > M["trouve"] - 0.15 else 0
        plans = []
        for k, (nom, url) in enumerate([("City Pipes", "citypipes.net"), ("Drain Masters", "drainmasters.com"), ("Morel Plumbing", "morelplumbing.com")]):
            a = prog(t, M["s0"] + 0.05 * k, 0.45, sortieExpo)
            moi = k == 2
            y = -260 + k * 270
            if moi: y = mix(y, -330, monte)
            z = mix(500, 0, a) + (mix(0, -320, monte) if moi else 0)
            plans.append(Plan(coins((0, y, z), 840, 230), 840, 230, resultat(nom, url, moi), borne(a * 3)))
        scene3d(c, cam, plans)
        if monte > 0:
            lueur_s(c, 540, 640, 420, S["violetVif"], 0.25 * borne(monte))
            b = entre(t, M["google2"] - 0.1, 0.4, 2.4)
            pill(c, "Built to be found", 540, 1260, 38, "grad", "search", borne(b * 3), mix(0.4, 1, b), rot=-3)
            eclats(c, 540, 640, t, M["trouve"] + 0.2, 14, 520, graine=5)


# ─────────────────────────────────────────── C5 : la maquette offerte
def scene_maquette(c, t, M):
    g = Groupe(c, t, M["m0"] - 0.1, M["decolle"] - 0.1, ent="droite", sor="zoom", d_in=0.38)
    if not g.visible: return
    with g:
        lettres(c, "YOUR FIRST", 540, 200, 96, t, M["m0"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
        lettres(c, "MOCKUP", 540, 310, 150, t, M["maquette"] - 0.12, "ressort", decal=0.04)
        couleur = prog(t, M["maquette"] - 0.05, 0.6, entreeSortie)
        a = entre(t, M["m0"] - 0.05, 0.6, 1.3)
        cam = Cam(ax=-12 + 3 * math.sin(t), ay=mix(-60, -16, a) + 26 * couleur + 4 * math.sin(t * 0.8), tz=mix(1000, 120, a), cy=960)
        def filaire(cc, w, h):
            rrect(cc, 0, 0, w, h, 30, "#FFFFFF", 1.0, None, S["lilas"], 4)
            pa = peinture(S["lilas"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=3); pa.setPathEffect(skia.DashPathEffect.Make([12, 10], 0))
            for (x, y, ww, hh) in [(30, 30, 240, 50), (30, 110, w - 60, 330), (30, 470, (w - 80) / 3, 150), (40 + (w - 80) / 3, 470, (w - 80) / 3, 150),
                                   (50 + 2 * (w - 80) / 3, 470, (w - 80) / 3, 150), (30, 650, w - 60, 140)]:
                cc.drawRoundRect(skia.Rect.MakeXYWH(x, y, ww, hh), 18, 18, pa)
        W_, H_ = 560, 840
        plans = [Plan(coins((0, 0, 0), W_, H_), W_, H_, filaire, 1 - couleur),
                 Plan(coins((0, 0, -4), W_, H_), W_, H_, site_moderne(t, "Your business"), couleur)]
        scene3d(c, cam, plans)
        gf = entre(t, M["gratuit"] - 0.12, 0.4, 2.6)
        if gf > 0:
            c.save(); c.translate(800, 1180); c.rotate(-8); z = mix(2.4, 1, prog(t, M["gratuit"] - 0.12, 0.2, entree)); c.scale(z, z)
            pill(c, "FREE", 0, 0, 56, "vert", "gift", borne(gf * 3))
            c.restore()
            eclats(c, 800, 1180, t, M["gratuit"], 14, 380, graine=10)


def sons_sites(K, M):
    son, rapide = K.son, K.rapide
    son(M["g0"] - 0.12, "whoosh_long", -9)
    for i in range(15): son(M["cherche"] + i * 0.037, "frappe", -18)
    for k in range(3): son(M["google"] - 0.1 + 0.1 * k, "pop", -13)
    son(M["site"] - 0.3, "whoosh_bas", -8); son(M["site"], "pop", -11)
    for k in ("lent", "date", "illisible"): son(M[k] - 0.1, "tampon", -9); son(M[k] - 0.05, "croc", -15)
    son(M["donc"] - 0.1, "swipe", -9); son(M["appelle"], "clic", -6); son(M["appelle"] + 0.15, "message_in", -9); son(M["autre"], "ding", -12)
    son(M["v0"] - 0.1, "whoosh", -9); son(M["vendeur"] - 0.15, "impact_doux", -8)
    for k in range(2): son(M["v0"] + 0.3 + 0.35 * k, "pop", -12)
    son(M["b0"] - 0.1, "whoosh_long", -9); son(M["b0"], "impact_doux", -10)
    for cle in ("moderne", "rapide", "mobile", "offre", "bouton"): son(M[cle] - 0.12, "pop", -10)
    son(M["rapide"], "montee", -14); son(M["mobile"] - 0.15, "whoosh_court", -11); son(M["bouton"] + 0.2, "clic", -7); son(M["bouton"] + 0.25, "check", -11)
    son(M["s0"] - 0.1, "whoosh", -9)
    for i in range(15): son(M["s0"] + 0.05 + i * 0.037, "frappe", -19)
    son(M["trouve"] - 0.15, "montee", -10); son(M["trouve"] + 0.2, "ching", -10)
    son(M["google2"] - 0.1, "pop", -11)
    son(M["m0"] - 0.1, "swipe", -10); son(M["maquette"] - 0.12, "impact_doux", -9)
    for i in range(8): son(M["maquette"] + 0.05 * i, "blip", -19)
    son(M["gratuit"] - 0.12, "tampon", -7); son(M["gratuit"], "ching", -9)
    son(M["decolle"] - 0.2, "whoosh_bas", -8); son(M["decolle"], "impact_doux", -9)
    son(M["business"] - 0.1, "pop", -11)
    son(M["take"] - 0.45, "montee", -9); son(M["take"] - 0.05, "impact", -5); son(M["take"], "whoosh_long", -6); son(M["take"] + 0.05, "ching", -10)
    son(M["devis"] - 0.12, "whoosh", -9); son(M["devis"] + 0.18, "verre", -10); son(M["devis"] + 0.75, "clic", -6)
    for i in range(15): son(M["url"] + i * 0.034, "frappe", -18)
    son(M["url"] + 0.4, "pop", -13)
    for a, b in [(M["g0"] - 0.15, M["g0"] + 0.3), (M["site"] - 0.3, M["site"] + 0.3), (M["donc"] - 0.1, M["donc"] + 0.4), (M["v0"] - 0.15, M["v0"] + 0.3),
                 (M["b0"] - 0.15, M["b0"] + 0.3), (M["mobile"] - 0.15, M["mobile"] + 0.3), (M["s0"] - 0.15, M["s0"] + 0.3), (M["m0"] - 0.15, M["m0"] + 0.3),
                 (M["decolle"] - 0.2, M["decolle"] + 0.3), (M["take"] - 0.05, M["take"] + 0.6), (M["devis"] - 0.15, M["devis"] + 0.3)]:
        rapide(a, b)


def compose_sites(c, t, M, hook, T_B1, SOUS, K, pulse=0.0):
    fond_studio(c, t, pulse)
    with Balance(c, t):
        scene_recherche(c, t, M); scene_vendeur(c, t, M); scene_construit(c, t, M); scene_google(c, t, M); scene_maquette(c, t, M)
    scene_decollage(c, t, M)
    scene_cta(c, t, M, 0)
    if t < T_B1 + 0.3:
        o = prog(t, T_B1 - 0.3, 0.35, entree)
        c.save(); c.translate(540, 900); c.scale(mix(1, 2.2, o), mix(1, 2.2, o)); c.translate(-540, -900)
        with Calque(c, 1 - o):
            hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    if t < M["devis"] - 0.25: SOUS.dessine(c, t, S["encre"])
