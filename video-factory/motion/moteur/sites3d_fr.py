"""Version FRANÇAISE des pubs « sites » (DA-M19, 29/10/2026).

`sites3d.py` est écrit pour le marché US : tous ses libellés, et jusqu'au contenu des faux sites,
sont en anglais. Ce module rejoue les mêmes scènes en français — faux sites compris, sinon une pub
française montrerait un site anglais — et ajoute les blocs qui n'existaient pas dans le format court :
la perte silencieuse, les trois objections, le test du téléphone, la nuit qui cherche.

    import sites3d_fr as fr
    fr.francais()          # après config_sites() NON appelé : studio reste en français
"""
import math
import skia
from moteur import *
from studio import *
from studio3d import *
import studio, studio3d, sites3d
from sites3d import PW, PH, barre_recherche, tel, scene_decollage

NOM = "Morel Plomberie"
REQUETE = "plombier pres de chez moi"


# ─────────────────────────────────────────── faux sites, en français
def site_vieux_fr(t, charge=True):
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#E8E4DA"))
        c.drawRect(skia.Rect.MakeWH(w, 70 * k), peinture("#7D7B76"))
        texte(c, "MOREL PLOMBERIE SARL", 16 * k, 24 * k, 18 * k, "#EDEBE6", "fort", track=0.02)
        texte(c, "Bienvenue sur notre site !!!", 16 * k, 92 * k, 15 * k, "#3B5BA8", "demi", track=0)
        rrect(c, 16 * k, 124 * k, w - 32 * k, 230 * k, 0, "#CFCBC2")
        icone(c, "image-off", w / 2, 239 * k, 70 * k, "#9E9A92", 1.6)
        for j in range(16):
            rrect(c, 16 * k, (380 + j * 20) * k, (w - 32 * k) * (0.55 + 0.4 * ((j * 37) % 10) / 10), 7 * k, 0, "#A8A49B")
        texte(c, "Cliquez ici", 16 * k, 712 * k, 14 * k, "#3B5BA8", "demi", track=0)
        texte(c, "Copyright 2009", 16 * k, h - 40 * k, 13 * k, "#8E8A82", "demi", track=0)
        if charge:
            c.drawRect(skia.Rect.MakeWH(w, h), peinture("#FFFFFF", 0.35))
            R = 46 * k
            pa = peinture(S["gris"], 1, Style=skia.Paint.kStroke_Style, StrokeWidth=9 * k); pa.setStrokeCap(skia.Paint.kRound_Cap)
            arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(w / 2 - R, h * 0.45 - R, 2 * R, 2 * R), (t * 400) % 360, 260)
            c.drawPath(arc, pa)
    return f


def site_moderne_fr(t, nom=NOM, appui=0.0):
    def f(c, w, h):
        k = w / 440
        c.drawRect(skia.Rect.MakeWH(w, h), peinture("#FFFFFF"))
        rrect(c, 20 * k, 26 * k, 40 * k, 40 * k, 12 * k, S["violet"]); icone(c, "wrench", 40 * k, 46 * k, 24 * k, "#FFFFFF", 2.4)
        texte(c, nom, 72 * k, 32 * k, 24 * k, S["encre"], "titre", track=-0.02)
        for j in range(3): rrect(c, w - 44 * k, (34 + j * 10) * k, 22 * k, 3 * k, 1.5 * k, S["encre"])
        c.drawRoundRect(skia.Rect.MakeXYWH(16 * k, 90 * k, w - 32 * k, 360 * k), 26 * k, 26 * k, pgrad(0, 90 * k, w, 450 * k, GRAD_VIF))
        lueur_s(c, w * 0.7, 200 * k, 160 * k, "#FFFFFF", 0.22)
        texte(c, "Dépannage rapide.", 40 * k, 130 * k, 44 * k, "#FFFFFF", "noir", track=-0.03)
        texte(c, "Intervention le jour même.", 40 * k, 190 * k, 25 * k, "#E3D6FF", "titre", track=-0.02)
        for j in range(5): icone(c, "star", (52 + j * 30) * k, 262 * k, 22 * k, S["or_"], 2.4)
        s_ = (1 + 0.05 * math.sin(t * 6)) * (1 - 0.08 * appui)
        c.save(); c.translate(40 * k + 150 * k / 2 * 1.4, 345 * k); c.scale(s_, s_)
        rrect(c, -105 * k, -32 * k, 210 * k, 64 * k, 32 * k, S["vert"])
        icone(c, "phone", -62 * k, 0, 28 * k, "#FFFFFF", 2.6)
        texte(c, "Appeler", -38 * k, -hauteurLigne(26 * k, "titre") / 2, 26 * k, "#FFFFFF", "titre", track=-0.01)
        c.restore()
        for j, (ic, lab) in enumerate([("droplet", "Fuites"), ("wrench", "Dépannage"), ("house", "Installation")]):
            x = 16 * k + j * (w - 32 * k) / 3
            rrect(c, x + 4 * k, 476 * k, (w - 32 * k) / 3 - 8 * k, 140 * k, 20 * k, S["doux"])
            tuile(c, ic, x + (w - 32 * k) / 6, 526 * k, 52 * k, "doux")
            texte(c, lab, x + (w - 32 * k) / 6, 572 * k, 18 * k, S["encre"], "titre", "centre", -0.01)
        rrect(c, 16 * k, 640 * k, w - 32 * k, 120 * k, 20 * k, "#FFFFFF", 1.0, None, S["ligne"], 2 * k)
        disque(c, 56 * k, 700 * k, 22 * k, S["lilas"])
        rrect(c, 92 * k, 684 * k, 200 * k, 12 * k, 6 * k, S["ligne"]); rrect(c, 92 * k, 706 * k, 140 * k, 12 * k, 6 * k, S["ligne"])
        for j in range(5): icone(c, "star", (300 + j * 22) * k, 700 * k, 16 * k, S["or_"], 2.2)
    return f


def resultat_fr(nom, url, moderne, alpha=1.0):
    return sites3d.resultat(nom, url, moderne, alpha)


# ─────────────────────────────────────────── C1 : la recherche, ton vieux site, il appelle l'autre
def scene_recherche(c, t, M):
    g = Groupe(c, t, M["g0"] - 0.12, M["sil0"] - 0.05, ent="zoom", sor="gauche", d_out=0.32)
    if not g.visible: return
    with g:
        plonge = prog(t, M["site"] - 0.3, 0.6, entreeSortie)
        bascule = prog(t, M["donc"] - 0.1, 0.6, entreeSortie)
        if plonge < 1:
            cam = Cam(ax=mix(-26, -10, plonge), ay=6 * math.sin(t * 0.8), tz=mix(200, -900, plonge), cy=1000)
            plans = []
            for k, (nom, url, mod) in enumerate([(NOM, "morel-plomberie.fr", False), ("Plomberie Duval", "plomberie-duval.fr", True),
                                                 ("AquaService", "aquaservice.fr", False)]):
                a = prog(t, M["g0"] + 0.15 + 0.12 * k, 0.45, sortieExpo)
                if a <= 0: continue
                plans.append(Plan(coins((0, -280 + k * 270, mix(600, 0, a)), 840, 230), 840, 230, resultat_fr(nom, url, mod), borne(a * 3) * (1 - plonge)))
            scene3d(c, cam, plans)
            if t > M["site"] - 0.4:
                eti = entre(t, M["site"] - 0.35, 0.4, 2.4) * (1 - plonge)
                pill(c, "Ton site", 260, 560, 32, "encre", "arrow-down", borne(eti * 3), mix(0.4, 1, eti), rot=-4)
            barre_recherche(c, t, M["cherche"], REQUETE, 210, 1 - plonge)
        if plonge > 0:
            cam = Cam(ax=4 * math.sin(t * 0.9), ay=mix(30, -14, plonge) + 3 * math.sin(t * 0.7) - 60 * bascule, tz=mix(1400, 80, plonge), cy=880, tx=-300 * bascule)
            scene3d(c, cam, [Plan(coins((0, 0, 0), PW, PH), PW, PH, tel(site_vieux_fr(t)), 1 - borne(bascule * 1.4))])
            for k, (lab, ic, cle, x, y, r) in enumerate([("Lent", "hourglass", "lent", 290, 470, -6), ("Daté", "calendar", "date", 800, 740, 5),
                                                         ("Illisible", "eye-off", "illisible", 330, 1060, -3)]):
                e = entre(t, M[cle] - 0.1, 0.4, 2.6) * (1 - bascule)
                if e <= 0: continue
                c.save(); c.translate(x, y); c.rotate(r); z = mix(2.2, 1, prog(t, M[cle] - 0.1, 0.18, entree)); c.scale(z, z)
                pill(c, lab, 0, 0, 50, "rouge", ic, borne(e * 3))
                c.restore()
        if bascule > 0:
            appui = prog(t, M["appelle"] - 0.05, 0.08, sortie) * (1 - prog(t, M["appelle"] + 0.1, 0.15, sortie))
            cam = Cam(ay=mix(70, 0, bascule) + 4 * math.sin(t * 0.8), ax=3 * math.sin(t), tz=mix(600, 40, bascule), cy=880, tx=mix(500, 0, bascule))
            scene3d(c, cam, [Plan(coins((0, 0, 0), PW, PH), PW, PH, tel(site_moderne_fr(t, "Plomberie Duval", appui)))])
            pill(c, "Quelqu'un d'autre", 540, 300, 36, "grad", "users", borne(bascule * 3), mix(0.4, 1, bascule), rot=3)
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
                    texte(c, "Appel en cours…", -195, -hauteurLigne(34, "titre") / 2, 34, S["encre"], "titre", track=-0.02)
                c.restore()
                onde(c, 280, 1230, t, M["appelle"] + 0.2, 40, 200, S["vert"], 6, 0.6)


# ─────────────────────────────────────────── C1b : la perte silencieuse (nouveau, format long)
def scene_silence(c, t, M):
    """Il ne te le dira pas. Il ne se plaindra pas. Il passe au nom suivant — et tu ne le sauras jamais."""
    g = Groupe(c, t, M["sil0"] - 0.12, M["v0"] - 0.05, ent="bas", sor="zoom", d_in=0.4)
    if not g.visible: return
    with g:
        lettres(c, "CE CLIENT", 540, 190, 104, t, M["sil0"] - 0.05, "ressort", decal=0.03, grad=False, couleur=S["encre"])
        lettres(c, "NE TE DIRA RIEN", 540, 300, 96, t, M["dira"] - 0.12, "masque", grad=True, decal=0.03, duree=0.35)
        # la liste des noms : le tien barré, le curseur descend au suivant
        noms = [(NOM, True), ("Plomberie Duval", False), ("AquaService", False), ("SOS Canalisation", False)]
        a = entre(t, M["sil0"] + 0.1, 0.5, 1.4)
        cam = Cam(ax=-16 + 3 * math.sin(t * 0.8), ay=mix(-30, -8, a) + 4 * math.sin(t * 0.6), tz=mix(900, 180, a), cy=1060)
        plans = []
        for k, (nom, moi) in enumerate(noms):
            e = prog(t, M["sil0"] + 0.15 + 0.1 * k, 0.4, sortieExpo)
            if e <= 0: continue
            choisi = k == 1 and t > M["suivant"] - 0.1
            plans.append(Plan(coins((0, -300 + k * 200, mix(500, 0, e)), 800, 170), 800, 170,
                              resultat_fr(nom, "", choisi), borne(e * 3) * (0.35 if (moi and t > M["suivant"]) else 1)))
        scene3d(c, cam, plans)
        # la croix sur le tien
        if t > M["dira"]:
            X, Y, _ = cam.proj((330, -300, 0))
            e = entre(t, M["dira"], 0.3, 2.4)
            disque(c, X, Y, 34 * borne(e * 3), S["rouge"]); icone(c, "x", X, Y, 38 * borne(e * 3), "#FFFFFF", 3.2)
        # la flèche qui descend vers le nom suivant
        if t > M["suivant"] - 0.2:
            s_ = entre(t, M["suivant"] - 0.2, 0.4, 2.0)
            pill(c, "Au nom suivant", 540, 1270, 38, "grad", "arrow-down", borne(s_ * 3), mix(0.4, 1, s_), rot=-3)
        # « tu ne le sauras jamais » : l'écran du patron reste vide
        j = entre(t, M["jamais"] - 0.15, 0.45, 2.0)
        if j > 0:
            with Calque(c, borne(j * 3)):
                carte_s(c, 230, 420, 620, 140, 40, "#FFFFFF", None, 0.18)
                icone(c, "bell", 310, 490, 48, S["gris"], 2.2)
                texte(c, "Aucune notification", 360, 490 - hauteurLigne(34, "titre") / 2, 34, S["gris"], "titre", track=-0.02)


# ─────────────────────────────────────────── C2 : ton premier commercial
def scene_vendeur(c, t, M):
    g = Groupe(c, t, M["v0"] - 0.1, M["b0"] - 0.05, ent="droite", sor="zoom", d_in=0.36)
    if not g.visible: return
    with g:
        lettres(c, "TON PREMIER", 540, 230, 96, t, M["v0"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
        lettres(c, "COMMERCIAL", 540, 340, 118, t, M["vendeur"] - 0.15, "ressort", decal=0.035)
        a = entre(t, M["v0"] - 0.05, 0.6, 1.3)
        cam = Cam(ax=-8 + 3 * math.sin(t), ay=mix(-50, 18, a) + 4 * math.sin(t * 0.8), tz=mix(900, 330, a), cy=900)
        def nav(cc, w, h):
            rrect(cc, 0, 0, w, h, 34, "#FFFFFF", 1.0, None, S["ligne"], 3)
            rrect(cc, 0, 0, w, 64, 0, S["doux"])
            for j, col in enumerate(["#FF6B6B", "#FFC53D", "#2E9E68"]): disque(cc, 34 + j * 30, 32, 9, col)
            rrect(cc, 140, 16, w - 200, 32, 16, "#FFFFFF"); texte(cc, "ton-entreprise.fr", 170, 20, 22, S["gris"], "demi", track=0)
            cc.save(); cc.translate(0, 64)
            site_moderne_fr(t, "Ton entreprise")(cc, w, h - 64)
            cc.restore()
        scene3d(c, cam, [Plan(coins((0, 0, 0), 760, 900), 760, 900, nav)])
        for k, (lab, ic, x, y, r) in enumerate([("Ouvert 24h/24", "clock", 230, 640, -5), ("Parle à chaque visiteur", "message-circle", 740, 1180, 4)]):
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
            site_moderne_fr(t, NOM)(cc, w, h)
            cc.restore()
        plans = [Plan(coins((-160, -120, 300), 760, 860), 760, 860, nav, 1 - 0.4 * mob),
                 Plan(coins((mix(420, 200, mob), mix(160, 40, mob), mix(-60, -260, mob)), PW * 0.82, PH * 0.82, ay=mix(-14, 10, mob)), PW * 0.82, PH * 0.82,
                      tel(site_moderne_fr(t, NOM, appui)), borne(prog(t, M["b0"] + 0.1, 0.5) * 3))]
        scene3d(c, cam, plans)
        lettres(c, "ON CONSTRUIT", 540, 200, 108, t, M["b0"] - 0.05, "ressort", decal=0.035)
        for k, (lab, ic, cle, x, y, r, mode) in enumerate([("Moderne", "sparkles", "moderne", 220, 420, -6, "grad"), ("Rapide", "zap", "rapide", 860, 520, 5, "encre"),
                                                          ("Pensé pour le téléphone", "smartphone", "mobile", 300, 1180, -3, "blanc"),
                                                          ("Offre claire", "target", "offre", 790, 1020, 4, "grad"), ("Bouton d'appel", "phone", "bouton", 310, 820, -4, "vert")]):
            e = entre(t, M[cle] - 0.12, 0.4, 2.4)
            if e <= 0: continue
            c.save(); c.translate(x, y + 10 * math.sin(t * 2 + k)); c.rotate(r); z = mix(1.8, 1, prog(t, M[cle] - 0.12, 0.2, entree)); c.scale(z, z)
            pill(c, lab, 0, 0, 36, mode, ic, borne(e * 3))
            c.restore()
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
        barre_recherche(c, t, M["s0"] + 0.05, REQUETE, 230)
        cam = Cam(ax=-22 + 3 * math.sin(t), ay=8 * math.sin(t * 0.7), tz=150, cy=1000)
        monte = prog(t, M["trouve"] - 0.15, 0.6, lambda v: ressort(v, 1.3, 4.6)) if t > M["trouve"] - 0.15 else 0
        plans = []
        for k, (nom, url) in enumerate([("AquaService", "aquaservice.fr"), ("SOS Canalisation", "sos-canalisation.fr"), (NOM, "morel-plomberie.fr")]):
            a = prog(t, M["s0"] + 0.05 * k, 0.45, sortieExpo)
            moi = k == 2
            y = -260 + k * 270
            if moi: y = mix(y, -330, monte)
            z = mix(500, 0, a) + (mix(0, -320, monte) if moi else 0)
            plans.append(Plan(coins((0, y, z), 840, 230), 840, 230, resultat_fr(nom, url, moi), borne(a * 3)))
        scene3d(c, cam, plans)
        if monte > 0:
            lueur_s(c, 540, 640, 420, S["violetVif"], 0.25 * borne(monte))
            b = entre(t, M["google2"] - 0.1, 0.4, 2.4)
            pill(c, "Fait pour être trouvé", 540, 1260, 38, "grad", "search", borne(b * 3), mix(0.4, 1, b), rot=-3)
            eclats(c, 540, 640, t, M["trouve"] + 0.2, 14, 520, graine=5)


# ─────────────────────────────────────────── C5 : la maquette offerte
def scene_maquette(c, t, M):
    g = Groupe(c, t, M["m0"] - 0.1, M["obj0"] - 0.1, ent="droite", sor="zoom", d_in=0.38)
    if not g.visible: return
    with g:
        lettres(c, "TA PREMIÈRE", 540, 200, 96, t, M["m0"] + 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.35)
        lettres(c, "MAQUETTE", 540, 310, 140, t, M["maquette"] - 0.12, "ressort", decal=0.04)
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
                 Plan(coins((0, 0, -4), W_, H_), W_, H_, site_moderne_fr(t, "Ton entreprise"), couleur)]
        scene3d(c, cam, plans)
        gf = entre(t, M["gratuit"] - 0.12, 0.4, 2.6)
        if gf > 0:
            c.save(); c.translate(790, 1180); c.rotate(-8); z = mix(2.4, 1, prog(t, M["gratuit"] - 0.12, 0.2, entree)); c.scale(z, z)
            pill(c, "OFFERTE", 0, 0, 52, "vert", "gift", borne(gf * 3))
            c.restore()
            eclats(c, 790, 1180, t, M["gratuit"], 14, 380, graine=10)


# ─────────────────────────────────────────── C6 : les trois objections (nouveau)
OBJ = [("Je n'ai pas le temps", "Un message, on fait le reste", "clock", "obj1", "rep1"),
       ("Ça coûte trop cher", "Moins qu'un client perdu par mois", "wallet", "obj2", "rep2"),
       ("Le mien va très bien", "Ouvre-le sur ton téléphone", "check", "obj3", "rep3")]


def scene_objections(c, t, M):
    g = Groupe(c, t, M["obj0"] - 0.12, M["test0"] - 0.05, ent="bas", sor="gauche", d_in=0.42)
    if not g.visible: return
    with g:
        lettres(c, "TU TE DIS", 540, 180, 92, t, M["obj0"] - 0.05, "masque", grad=False, couleur=S["encre"], decal=0.03, duree=0.3)
        lettres(c, "TROIS CHOSES", 540, 290, 110, t, M["trois"] - 0.12, "ressort", decal=0.035)
        for k, (q, r, ic, cq, cr) in enumerate(OBJ):
            e = entre(t, M[cq] - 0.14, 0.42, 2.2)
            if e <= 0: continue
            y = 560 + k * 300
            with Calque(c, borne(e * 3)):
                z = mix(1.5, 1, prog(t, M[cq] - 0.14, 0.22, entree))
                c.save(); c.translate(540, y); c.scale(z, z); c.translate(-540, -y)
                carte_s(c, 150, y - 95, 780, 190, 44, "#FFFFFF", None, 0.16)
                disque(c, 250, y - 30, 44, S["doux"]); icone(c, "message-circle", 250, y - 30, 42, S["gris"], 2.2)
                texte(c, "« " + q + " »", 320, y - 30 - hauteurLigne(36, "titre") / 2, 36, S["gris"], "titre", track=-0.02)
                rep = entre(t, M[cr] - 0.1, 0.35, 2.4)
                if rep > 0:
                    with Calque(c, borne(rep * 3)):
                        disque(c, 250, y + 46, 30, S["vert"]); icone(c, "check", 250, y + 46, 30, "#FFFFFF", 3.0)
                        texte(c, r, 300, y + 46 - hauteurLigne(32, "titre") / 2, 32, S["encre"], "titre", track=-0.02)
                c.restore()


# ─────────────────────────────────────────── C7 : le test du téléphone (nouveau)
def scene_test(c, t, M):
    g = Groupe(c, t, M["test0"] - 0.1, M["nuit0"] - 0.05, ent="zoom", sor="recul", d_in=0.4)
    if not g.visible: return
    with g:
        lettres(c, "COMPTE", 540, 180, 120, t, M["test0"] - 0.05, "ressort", decal=0.035, grad=False, couleur=S["encre"])
        lettres(c, "LES SECONDES", 540, 300, 104, t, M["compte"] - 0.12, "masque", grad=True, decal=0.03, duree=0.35)
        a = entre(t, M["test0"], 0.5, 1.4)
        cam = Cam(ax=6 * math.sin(t * 0.8), ay=mix(-26, -6, a) + 4 * math.sin(t * 0.7), tz=mix(1100, 340, a), cy=980)
        scene3d(c, cam, [Plan(coins((0, 60, 0), PW, PH), PW, PH, tel(site_vieux_fr(t)))])
        # le chronomètre qui monte pendant que ça charge
        ch = entre(t, M["compte"] - 0.1, 0.4, 2.0)
        if ch > 0:
            s = borne((t - M["compte"]) / (M["client"] - M["compte"])) * 7.0
            with Calque(c, borne(ch * 3)):
                carte_s(c, 330, 410, 420, 160, 50, "#FFFFFF", None, 0.2)
                icone(c, "timer", 418, 490, 58, S["rouge"], 2.4)
                texte(c, f"{s:.1f} s", 486, 490 - hauteurLigne(68, "noir") / 2, 68, S["rouge"], "noir", track=-0.03)


# ─────────────────────────────────────────── C8 : la nuit qui cherche (nouveau)
def scene_nuit(c, t, M):
    g = Groupe(c, t, M["nuit0"] - 0.1, M["decolle"] - 0.1, ent="haut", sor="zoom", d_in=0.42)
    if not g.visible: return
    with g:
        lettres(c, "CETTE NUIT", 540, 190, 118, t, M["nuit0"] - 0.05, "ressort", decal=0.035, grad=False, couleur=S["encre"])
        lettres(c, "ILS CHERCHENT", 540, 310, 100, t, M["cherchent"] - 0.12, "masque", grad=True, decal=0.03, duree=0.35)
        a = entre(t, M["nuit0"], 0.55, 1.3)
        cam = Cam(ax=-24 + 3 * math.sin(t * 0.7), ay=6 * math.sin(t * 0.6), tz=mix(900, 220, a), cy=1040)
        # une nappe de téléphones allumés dans la ville
        plans = []
        for k in range(12):
            col, lig = k % 4, k // 4
            e = prog(t, M["nuit0"] + 0.06 * k, 0.4, sortieExpo)
            if e <= 0: continue
            x = -480 + col * 320
            y = -300 + lig * 330
            plans.append(Plan(coins((x, y, mix(600, 0, e)), 230, 470, ay=(-8 + 5 * col)), 230, 470,
                              tel(site_moderne_fr(t, "Ton entreprise")), borne(e * 3) * 0.95))
        scene3d(c, cam, plans)
        q = entre(t, M["question"] - 0.12, 0.42, 2.2)
        if q > 0:
            pill(c, "Sur quel site ils tombent ?", 540, 1330, 40, "grad", "search", borne(q * 3), mix(0.4, 1, q), rot=-2)


def sons_fr(K, M):
    """bruitages du montage français, repères du format long compris"""
    son, rapide = K.son, K.rapide
    son(M["g0"] - 0.12, "whoosh_long", -9)
    for i in range(15): son(M["cherche"] + i * 0.037, "frappe", -18)
    for k in range(3): son(M["google"] - 0.1 + 0.1 * k, "pop", -13)
    son(M["site"] - 0.3, "whoosh_bas", -8); son(M["site"], "pop", -11)
    for k in ("lent", "date", "illisible"): son(M[k] - 0.1, "tampon", -9); son(M[k] - 0.05, "croc", -15)
    son(M["donc"] - 0.1, "swipe", -9); son(M["appelle"], "clic", -6); son(M["appelle"] + 0.15, "message_in", -9); son(M["autre"], "ding", -12)
    # la perte silencieuse
    son(M["sil0"] - 0.12, "whoosh", -9); son(M["dira"] - 0.12, "impact_doux", -8); son(M["dira"], "croc", -12)
    son(M["suivant"] - 0.2, "swipe", -11); son(M["jamais"] - 0.15, "whoosh_bas", -11)
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
    # objections
    son(M["obj0"] - 0.12, "whoosh_long", -9); son(M["trois"] - 0.12, "impact_doux", -9)
    for _, _, _, cq, cr in OBJ:
        son(M[cq] - 0.14, "pop", -11); son(M[cr] - 0.1, "check", -12)
    # test du téléphone
    son(M["test0"] - 0.1, "whoosh", -9); son(M["compte"] - 0.12, "montee", -11)
    for i in range(7): son(M["compte"] + 0.18 * i, "blip", -20)
    son(M["client"] - 0.1, "croc", -11)
    # la nuit
    son(M["nuit0"] - 0.1, "whoosh_bas", -8)
    for k in range(12): son(M["nuit0"] + 0.06 * k, "blip", -20)
    son(M["cherchent"] - 0.12, "impact_doux", -9); son(M["question"] - 0.12, "pop", -10)
    # décollage et signature
    son(M["decolle"] - 0.2, "whoosh_bas", -8); son(M["decolle"], "impact_doux", -9)
    son(M["business"] - 0.1, "pop", -11)
    son(M["take"] - 0.45, "montee", -9); son(M["take"] - 0.05, "impact", -5); son(M["take"], "whoosh_long", -6); son(M["take"] + 0.05, "ching", -10)
    son(M["devis"] - 0.12, "whoosh", -9); son(M["devis"] + 0.18, "verre", -10); son(M["devis"] + 0.75, "clic", -6)
    for i in range(15): son(M["url"] + i * 0.034, "frappe", -18)
    son(M["url"] + 0.4, "pop", -13)
    for a, b in [(M["g0"] - 0.15, M["g0"] + 0.3), (M["site"] - 0.3, M["site"] + 0.3), (M["donc"] - 0.1, M["donc"] + 0.4),
                 (M["sil0"] - 0.15, M["sil0"] + 0.3), (M["v0"] - 0.15, M["v0"] + 0.3), (M["b0"] - 0.15, M["b0"] + 0.3),
                 (M["mobile"] - 0.15, M["mobile"] + 0.3), (M["s0"] - 0.15, M["s0"] + 0.3), (M["m0"] - 0.15, M["m0"] + 0.3),
                 (M["obj0"] - 0.15, M["obj0"] + 0.3), (M["test0"] - 0.15, M["test0"] + 0.3), (M["nuit0"] - 0.15, M["nuit0"] + 0.3),
                 (M["decolle"] - 0.2, M["decolle"] + 0.3), (M["take"] - 0.05, M["take"] + 0.6), (M["devis"] - 0.15, M["devis"] + 0.3)]:
        rapide(a, b)


def voile_bas(c, alpha=0.82):
    """dégradé blanc très doux sous la bande des sous-titres (y 1410) : sur DA-M19 le texte passait
    par-dessus les tuiles d'un faux site et le chronomètre. Ce n'est pas un surlignage — rien ne
    change de couleur, le fond s'éclaircit seulement là où le texte se pose."""
    pa = skia.Paint()
    pa.setShader(skia.GradientShader.MakeLinear(
        points=[(0.0, 1230.0), (0.0, 1560.0)],
        colors=[skia.Color4f(1, 1, 1, 0.0), skia.Color4f(1, 1, 1, alpha)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1230, 1080, 430), pa)


def compose_fr(c, t, M, hook, T_B1, SOUS, K, pulse=0.0):
    fond_studio(c, t, pulse)
    with Balance(c, t):
        scene_recherche(c, t, M); scene_silence(c, t, M); scene_vendeur(c, t, M); scene_construit(c, t, M)
        scene_google(c, t, M); scene_maquette(c, t, M); scene_objections(c, t, M); scene_test(c, t, M); scene_nuit(c, t, M)
    scene_decollage(c, t, M)
    if t < T_B1 + 0.3:
        o = prog(t, T_B1 - 0.3, 0.35, entree)
        c.save(); c.translate(540, 900); c.scale(mix(1, 2.2, o), mix(1, 2.2, o)); c.translate(-540, -900)
        with Calque(c, 1 - o):
            hook(c, t)
        c.restore()
    K.dessine_eclairs(c, t)
    if t < M["devis"] - 0.25:
        voile_bas(c)
        SOUS.dessine(c, t, S["encre"])


def francais():
    """libellés du carton final, des pastilles et du décollage, côté studio"""
    studio.CTA_PILLS = [("Pensé mobile", "smartphone"), ("Fait pour Google", "search"), ("Maquette offerte", "gift")]
    studio3d.MOTS_DECOLLAGE.update(l1="ON FAIT", pill="Ton activité", l2="DÉCOLLER", taille2=150)
