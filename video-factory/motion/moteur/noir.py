"""Style « noir » (Youssef, 14/10/2026, CB-M13 / CB-M14) : fond noir profond, cases fines à bord clair et fond
à peine visible, accents or. Les médias réels (vidéos, photos) vivent dans ces cases."""
import math
import skia
from moteur import *
from agence import A, lueur, pastille_verre
from studio import lettres, entre, eclats, curseur

NOIR = "#050506"
OR, OR2 = "#E8C27A", "#F6E2B3"
BLANC, ROUGE, VERT = "#FFFFFF", "#FF4D5E", "#2BD67B"
GRIS = "#9A97A6"


def fond_noir(c, t, pulse=0.0):
    """noir, une lueur chaude qui respire à peine, trame de points très discrète, vignette"""
    c.clear(hexa(NOIR))
    for (x, y, r, col, a, v, ph) in [(300, 500, 700, "#2A2216", 0.55, 0.21, 0.0), (820, 1400, 760, "#1A1626", 0.6, 0.17, 2.0)]:
        cx = x + 80 * math.sin(t * v + ph); cy = y + 90 * math.cos(t * v * 0.8 + ph)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [hexa(col, a * (1 + 0.4 * pulse)), hexa(col, 0.0)]))
        c.drawCircle(cx, cy, r, p)
    p = peinture("#FFFFFF", 0.03)
    dy = (t * 10) % 64
    for y in range(-64, H + 64, 64):
        for x in range(32, W, 64):
            c.drawCircle(x, y + 32 - dy, 1.5, p)
    v = skia.Paint(AntiAlias=True)
    v.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.75, [hexa("#000000", 0.0), hexa("#000000", 0.7)], [0.5, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), v)


def case(c, x, y, w, h, r=28, alpha=1.0, bord=0.18, fond=0.035, accent=None):
    """la case fine : fond blanc presque transparent, filet clair de 2 px"""
    if alpha <= 0.01: return
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    c.drawRRect(rr, peinture("#FFFFFF", fond * alpha))
    c.drawRRect(rr, peinture(accent or "#FFFFFF", (0.9 if accent else bord) * alpha, Style=skia.Paint.kStroke_Style, StrokeWidth=2))


def case_media(c, t, nom, x, y, w, h, alpha=1.0, s=1.0, video_t0=None, vitesse=1.0, zoom=1.0, fx=0.5, fy=0.5,
               accent=None, pad=10, r=28, rogne=(0.0, 0.0, 0.0, 0.0)):
    """une case avec sa photo (video_t0=None) ou sa vidéo dedans ; s = échelle depuis le centre"""
    if alpha <= 0.01 or s <= 0.01: return
    cx, cy = x + w / 2, y + h / 2
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy)
    with Calque(c, alpha):
        case(c, x, y, w, h, r, 1.0, accent=accent)
        if video_t0 is None:
            image_cover(c, nom, x + pad, y + pad, w - 2 * pad, h - 2 * pad, zoom, fx, fy, rayon=r - pad / 2)
        else:
            video(c, nom, x + pad, y + pad, w - 2 * pad, h - 2 * pad, t - video_t0, vitesse, rayon=r - pad / 2, rogne=rogne)
    c.restore()


def etiquette_case(c, label, x, y, a, couleur=OR, taille=34, fam="noir", texte_c="#0B0A0F"):
    """pastille pleine posée sur le coin d'une case"""
    if a <= 0: return
    tw = largeur(label, taille, fam, -0.01); w, h = tw + taille * 1.1, taille * 1.75
    c.save(); c.translate(x, y); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
    with Calque(c, borne(a * 3)):
        rrect(c, -w / 2, -h / 2, w, h, h / 2, couleur, 1.0, (8, 24, 0.5))
        texte(c, label, 0, -hauteurLigne(taille, fam) / 2, taille, texte_c, fam, "centre", -0.01)
    c.restore()


def puce(c, label, cx, cy, a, ic=None, couleur=OR, taille=36):
    """étiquette fine en case : icône or + texte blanc"""
    if a <= 0: return
    tw = largeur(label, taille, "gras", -0.01)
    w, h = tw + (taille * 1.6 if ic else 0) + taille * 1.2, taille * 2.0
    c.save(); c.translate(cx, cy); c.scale(mix(0.4, 1, a), mix(0.4, 1, a))
    with Calque(c, borne(a * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
        c.drawRRect(rr, peinture("#0B0A0F", 0.82))
        c.drawRRect(rr, peinture("#FFFFFF", 0.22, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        x = -w / 2 + taille * 0.6
        if ic:
            icone(c, ic, x + taille * 0.55, 0, taille * 1.05, couleur, 2.4); x += taille * 1.6
        texte(c, label, x, -hauteurLigne(taille, "gras") / 2, taille, BLANC, "gras", track=-0.01)
    c.restore()


def tampon_n(c, label, cx, cy, t, t0, couleur=OR, rot=-8, taille=52):
    if t < t0 - 0.12: return
    u = prog(t, t0 - 0.12, 0.16, entree)
    s = mix(2.6, 1, u)
    tw = largeur(label, taille, "noir"); w, h = tw + taille * 1.2, taille * 1.9
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    with Calque(c, u):
        rrect(c, -w / 2, -h / 2, w, h, 18, "#0B0A0F", 0.88, None, couleur, 7)
        texte(c, label, 0, -hauteurLigne(taille) / 2, taille, couleur, "noir", "centre", -0.01)
    c.restore()


def barre(c, x0, y0, x1, y1, u, couleur=ROUGE, ep=12):
    if u > 0: trait(c, x0, y0, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, couleur, ep)


def coche(c, cx, cy, r, a, couleur=VERT):
    if a <= 0: return
    disque(c, cx, cy, r * a, couleur); icone(c, "check", cx, cy, r * 1.15 * a, BLANC, 3.2)


def signet(c, cx, cy, taille, plein):
    k = taille / 100
    pth = skia.Path(); pth.moveTo(cx - 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy - 46 * k); pth.lineTo(cx + 36 * k, cy + 50 * k)
    pth.lineTo(cx, cy + 24 * k); pth.lineTo(cx - 36 * k, cy + 50 * k); pth.close()
    if plein > 0:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(cx - 60 * k, cy + 52 * k - 104 * k * plein, 120 * k, 104 * k * plein))
        c.drawPath(pth, peinture(OR)); c.restore()
    c.drawPath(pth, peinture(BLANC, 1, Style=skia.Paint.kStroke_Style, StrokeWidth=7 * k, StrokeJoin=skia.Paint.kRound_Join))


def bouton_enregistre(c, t, t_enr, cx, cy, alpha=1.0):
    """le signet TikTok qu'on remplit d'un clic, +1, éclats"""
    a = entre(t, t_enr - 0.15, 0.4, 2.2)
    if a <= 0 or alpha <= 0.01: return
    t_clic = t_enr + 0.35
    plein = prog(t, t_clic, 0.3, sortie)
    with Calque(c, alpha):
        b = mix(0.3, 1, a) * battement(t, t_clic, 0.2, 0.3)
        c.save(); c.translate(cx, cy); c.scale(b, b)
        lueur(c, 0, 0, 170, OR, 0.2 + 0.3 * plein)
        disque(c, 0, 0, 96, "#0B0A0F", 0.9); anneau(c, 0, 0, 96, OR if plein > 0.5 else BLANC, 3, 0.8)
        signet(c, 0, 0, 110, plein)
        c.restore()
        if plein > 0:
            pl = prog(t, t_clic, 0.8, sortie)
            texte(c, "+1", cx + 130, cy - 100 - 60 * pl, 50, OR, "noir", "centre", 0, alpha=1 - max(0, pl - 0.6) / 0.4)
        pa = prog(t, t_clic - 0.4, 0.38, sortie)
        if t < t_clic + 0.6:
            curseur(c, mix(1000, cx + 10, pa), mix(1600, cy + 20, pa), 1.3, 1 - prog(t, t_clic + 0.3, 0.3),
                    prog(t, t_clic - 0.05, 0.05) * (1 - prog(t, t_clic + 0.05, 0.1)))
        eclats(c, cx, cy, t, t_clic, 14, 260, [OR, BLANC, OR2], graine=3)


def cadenas(c, cx, cy, s, t, label, ouvre=0.0, alpha=1.0):
    """case fine avec un libellé or et un cadenas : la boucle ouverte"""
    if alpha <= 0.01 or s <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    with Calque(c, alpha):
        lueur(c, 0, 0, 280, OR, 0.18 + 0.08 * math.sin(t * 5))
        tw = largeur(label, 64, "noir", -0.02); w = tw + 140
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -80, w, 160), 40, 40)
        c.drawRRect(rr, peinture("#0B0A0F", 0.9))
        c.drawRRect(rr, peinture(OR, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        texte(c, label, 0, -hauteurLigne(64) / 2, 64, OR, "noir", "centre", -0.02)
        c.save(); c.translate(w / 2 - 10, -80 - 50 * ouvre); c.rotate(-30 * ouvre)
        disque(c, 0, 0, 50, OR); icone(c, "lock-open" if ouvre > 0.3 else "lock", 0, 0, 54, "#0B0A0F", 2.8)
        c.restore()
    c.restore()


def commentaire(c, t, t0, question, reponses, cy=900, pas=0.5):
    """barre de commentaire en case fine : la question en gris, puis des réponses tapées"""
    cm = entre(t, t0, 0.45, 1.8)
    if cm <= 0: return
    c.save(); c.translate(540, cy); c.scale(mix(0.5, 1, cm), mix(0.5, 1, cm))
    with Calque(c, borne(cm * 3)):
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-420, -70, 840, 140), 70, 70)
        c.drawRRect(rr, peinture("#FFFFFF", 0.05)); c.drawRRect(rr, peinture("#FFFFFF", 0.25, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        icone(c, "message-circle", -355, 0, 54, OR, 2.4)
        rep = [question] + reponses
        k = min(len(rep) - 1, int(max(0, t - t0 - 0.5) / pas))
        mot = rep[k]
        n = len(mot) if k == 0 else int(borne((t - t0 - 0.5 - pas * k) / 0.2) * len(mot) + 0.999)
        tl = 38 if k == 0 else 54
        texte(c, mot[:n], -300, -hauteurLigne(tl, "gras") / 2, tl, GRIS if k == 0 else BLANC, "gras", track=-0.01)
    c.restore()


def partage(c, t, t0, t_fleche, lab_b="Ton pote"):
    """« Envoie-la » : icône de partage, toi → ton pote"""
    lettres(c, "ENVOIE-LA", 540, 430, 120, t, t0 - 0.05, "ressort", cols=[OR, OR2], decal=0.035)
    a = entre(t, t0, 0.45, 1.8)
    if a > 0:
        b = mix(0.4, 1, a) * battement(t, t0 + 0.5, 0.1, 0.3)
        c.save(); c.translate(540, 760); c.scale(b, b)
        lueur(c, 0, 0, 200, OR, 0.3); disque(c, 0, 0, 105, OR); icone(c, "share-2", -4, 0, 115, "#0B0A0F", 2.6)
        c.restore()
    for (lab, x, tt) in [("Toi", 250, t0 + 0.3), (lab_b, 830, t0 + 0.6)]:
        b = entre(t, tt, 0.4, 2.2)
        if b > 0:
            c.save(); c.translate(x, 1110); c.scale(b, b)
            disque(c, 0, 0, 84, "#0B0A0F", 0.9); anneau(c, 0, 0, 84, BLANC, 2, 0.3)
            icone(c, "user-round", 0, -6, 88, BLANC, 2.0)
            texte(c, lab, 0, 102, 34, BLANC, "gras", "centre", -0.01)
            c.restore()
    u = prog(t, t_fleche, 0.6, entreeSortie)
    if u > 0:
        x = mix(250, 830, u); y = 1110 - 260 * math.sin(math.pi * u)
        c.save(); c.translate(x, y); c.rotate(-15 + 30 * u); c.scale(0.9, 0.9)
        rrect(c, -50, -80, 100, 160, 16, OR, 1.0, (8, 20, 0.5)); icone(c, "play", 4, 0, 50, "#0B0A0F", 2.6)
        c.restore()
    if t > t_fleche + 0.55: coche(c, 900, 1040, 34, entre(t, t_fleche + 0.55, 0.35, 2.4))


# ─────────────────────────────────────────── les trois sacoches (même modèle, trois qualités)
PHOTO_3 = "photos/sacs/sacoches-3-qualites-face"
VIDEO_SANGLES = "videos/sacs/sacoches-3-qualites-sangles"
# (nom, prix, position verticale du sac dans la photo) — de la plus lisse (en bas) à la plus granuleuse (en haut)
QUALITES = [("Standard", "120 – 150 €", 0.645), ("Top 1:1", "200 – 250 €", 0.462), ("Originale", "+ 300 €", 0.305)]
BANDES_Y = [540, 815, 1090]


def trois_sacoches(c, t, t_photo, t_split, t_qual, t_prix, t_fin):
    """la photo des trois sacoches dans une grande case, puis trois bandes : un sac par bande, nom et prix"""
    if t < t_photo - 0.3 or t > t_fin + 0.4: return
    sortie_ = prog(t, t_fin - 0.1, 0.35, entree)
    with Calque(c, 1 - sortie_):
        a = entre(t, t_photo - 0.2, 0.5, 1.5)
        sp = prog(t, t_split - 0.15, 0.45, entreeSortie)
        if sp < 1:
            case_media(c, t, PHOTO_3, 90, 500, 900, 860, borne(a * 3) * (1 - sp), mix(0.6, 1, a) * mix(1, 0.9, sp),
                       zoom=1.0 + 0.04 * max(0, t - t_photo), fy=0.48)
        if sp > 0:
            actif = max([k for k in range(3) if t >= t_qual[k] - 0.15] or [-1])
            for k, (nom, prix, fy) in enumerate(QUALITES):
                u = entre(t, t_split - 0.15 + 0.08 * k, 0.45, 1.6)
                if u <= 0: continue
                y = BANDES_Y[k]
                on = k == actif
                dim = 1.0 if (actif < 0 or on or k < actif) else 0.45
                c.save(); c.translate((1 - u) * 300, 0)
                case_media(c, t, PHOTO_3, 90, y, 900, 250, borne(u * 3) * dim, 1.0, zoom=1.08 + 0.03 * on * max(0, t - t_qual[k]),
                           fx=0.52, fy=fy, accent=OR if on else None)
                c.restore()
                puce(c, nom, 90 + 40 + largeur(nom, 32, "gras") / 2 + 30, y + 52, entre(t, t_qual[k] - 0.1, 0.4, 2.2), None, OR, 32)
                etiquette_case(c, prix, 990 - 40 - largeur(prix, 38, "noir") / 2 - 20, y + 250 - 48, entre(t, t_prix[k] - 0.05, 0.35, 2.4),
                               OR if k < 2 else VERT, 38)


def grain(c, t, t0, t_lisse, t_ferr, t_fin):
    """gros plan sur le grain de l'originale, les deux autres « trop lisses », puis les sangles et ferrures en vidéo"""
    if t < t0 - 0.3 or t > t_fin + 0.4: return
    sortie_ = prog(t, t_fin - 0.1, 0.35, entree)
    with Calque(c, 1 - sortie_):
        sf = prog(t, t_ferr - 0.15, 0.4, entreeSortie)
        a = entre(t, t0 - 0.2, 0.5, 1.5)
        if sf < 1:
            with Calque(c, 1 - sf):
                case_media(c, t, PHOTO_3, 90, 500, 900, 540, borne(a * 3), mix(0.6, 1, a), zoom=3.0 + 0.15 * max(0, t - t0),
                           fx=0.42, fy=QUALITES[2][2] + 0.01, accent=OR)
                puce(c, "Le grain", 260, 560, entre(t, t0 + 0.2, 0.4, 2.2), "scan-line", OR, 34)
                coche(c, 940, 560, 36, entre(t, t0 + 0.4, 0.35, 2.4))
                for k in range(2):
                    b = entre(t, t_lisse - 0.15 + 0.1 * k, 0.45, 1.8)
                    x = 90 + k * 460
                    case_media(c, t, PHOTO_3, x, 1070, 440, 250, borne(b * 3), mix(0.6, 1, b), zoom=3.0, fx=0.42,
                               fy=QUALITES[k][2] + 0.01)
                    if b > 0:
                        etiquette_case(c, "Trop lisse", x + 220, 1070 + 205, entre(t, t_lisse + 0.25 + 0.1 * k, 0.35, 2.4), ROUGE, 30, "noir", BLANC)
        if sf > 0:
            case_media(c, t, VIDEO_SANGLES, 190, 500, 700, 840, borne(sf * 3), mix(0.7, 1, sf), video_t0=t_ferr - 0.15, vitesse=1.6,
                       accent=OR)
            puce(c, "Ferrures", 300, 1240, entre(t, t_ferr + 0.1, 0.4, 2.2), "check", VERT, 34)
            puce(c, "Sangle", 780, 1240, entre(t, t_ferr + 0.6, 0.4, 2.2), "check", VERT, 34)
