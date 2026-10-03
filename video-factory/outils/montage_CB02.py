#!/usr/bin/env python3
"""CB-02 — « Le même objet, deux pays, deux prix ».

Format rafale : le chiffre est le héros, le produit le prouve. Les fonds
changent de thème à chaque bascule du propos (ce que ça coûte ici, ce que ça
coûte là-bas, ce que tu peux sourcer), parce qu'une vidéo qui garde le même
fond du début à la fin n'a pas de respiration.

Deux règles tenues : les prix « France » sont les prix réellement affichés sur
dropandyou, et aucun prix fournisseur n'est écrit — il se donne en commentaire.
Les montants du Surron viennent de Youssef (04/10/2026).
"""
import json, math, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import theme as TH

W, H, FPS = 1080, 1920, 30
MARGE = 108
BAS_SUR = 1440                      # rien d'important sous cette ligne
RAC = pathlib.Path(__file__).resolve().parent.parent
TRAV = pathlib.Path(__file__).parent/"_travail/CB-02"
LOGO = Image.open(RAC/"brand-ChinaBook-clair.png").convert("RGBA")
VEDETTES = json.load(open(TRAV/"vedettes.json"))      # produits + prix réels
RAFALE = 4                            # les quatre fiches du plan 3

F = "/System/Library/Fonts/HelveticaNeue.ttc"
def cond(s): return ImageFont.truetype(F, s, index=9)
def med(s):  return ImageFont.truetype(F, s, index=10)

def cl(x, a=0., b=1.): return max(a, min(b, x))
def ph(t, d, f): return cl((t-d)/max(1e-6, f-d))
def eo(x): return 1-(1-cl(x))**3
def back(x, k=2.1):
    x = cl(x); return 1+(k+1)*((x-1)**3)+k*((x-1)**2)

def neuf(nom):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img.alpha_composite(TH.fond(nom))
    return img

def pal(nom): return TH.THEMES[nom]

def halo(img, cx, cy, r, couleur, force=0.5):
    l = Image.new("RGBA", (r*2, r*2), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for i in range(16):
        k = 1-i/16; a = int(255*force*(k**2.4)/4); rr = int(r*(0.25+0.75*k))
        d.ellipse([r-rr, r-rr, r+rr, r+rr], fill=couleur+(a,))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(r*0.12)), (cx-r, cy-r))

def poser(img, prod, cx, cy, haut, p=1.0, ombre=True):
    if p <= 0: return
    h = int(haut*(0.86+0.14*cl(p))); w = max(1, int(prod.width*h/prod.height))
    im = prod.resize((w, h), Image.LANCZOS)
    al = im.split()[3].point(lambda v: int(v*cl(p*1.4)))
    if ombre:
        o = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        o.putalpha(al.point(lambda v: int(v*0.45)))
        img.alpha_composite(o.filter(ImageFilter.GaussianBlur(20)), (cx-w//2+6, cy-h//2+24))
    im.putalpha(al); img.alpha_composite(im, (cx-w//2, cy-h//2))

def centre(d, txt, police, y, couleur, a=255):
    d.text((W//2-d.textlength(txt, font=police)/2, y), txt, font=police, fill=couleur+(a,))

def mots(d, texte, t, depart, pas, police, x0, y, couleur, trainee=True):
    x = x0
    for i, m in enumerate(texte.split(" ")):
        p = ph(t, depart+i*pas, depart+i*pas+0.20)
        if p > 0:
            dy = int(26*(1-back(p))); a = int(255*cl(p*1.7))
            if trainee and p < 0.55:
                for o in (12, 6):
                    d.text((x, y+dy-o), m, font=police, fill=couleur+(int(a*0.15*(1-p)),))
            d.text((x, y+dy), m, font=police, fill=couleur+(a,))
        x += d.textlength(m+" ", font=police)

def secousse(t, quand, force=14, duree=0.22):
    p = ph(t, quand, quand+duree)
    if p <= 0 or p >= 1: return (0, 0)
    a = force*(1-p)**2
    return (int(a*math.sin(p*40)), int(a*0.55*math.cos(p*33)))

def flash(img, t, quand, duree=0.08, coul=(255, 255, 255), force=0.4):
    p = ph(t, quand, quand+duree)
    if p <= 0 or p >= 1: return
    a = int(255*force*(1-p)**1.7)
    if a > 2: img.alpha_composite(Image.new("RGBA", (W, H), coul+(a,)))

def euros(n): return f"{n:,.0f}".replace(",", " ")+" €"

def compteur(d, t, depart, duree, debut, fin, y, couleur, taille=168):
    """Le chiffre monte au lieu d'apparaître : c'est lui qu'on doit regarder."""
    p = eo(ph(t, depart, depart+duree))
    if p <= 0: return
    v = debut+(fin-debut)*p
    f = cond(int(taille*(0.9+0.1*p)))
    centre(d, euros(v), f, y, couleur, int(255*cl(p*4)))

# ---- 1 : 38 img — ce que ça coûte ici ---------------------------------
def p1(t, d):
    c = pal("braise"); img = neuf("braise"); dr = ImageDraw.Draw(img, "RGBA")
    dx, dy = secousse(t, 0.00, 20)
    mots(dr, "EN FRANCE,", t, 0.02, 0.09, cond(86), MARGE+dx, 320+dy, c["texte"])
    mots(dr, "UN SURRON :", t, 0.20, 0.09, cond(86), MARGE+dx, 424+dy, c["accent2"])
    halo(img, W//2, 880, 420, c["accent"], 0.42*eo(ph(t, 0.30, 0.80)))
    compteur(dr, t, 0.30, 0.85, 0, 7000, 760, c["texte"], 190)
    q = ph(t, 0.90, 1.14)
    if q > 0:
        centre(dr, "selon le modèle", med(42), 1010, c["sourd"], int(240*q))
    flash(img, t, 0.00, 0.09, (255, 150, 120), 0.45)
    return img

# ---- 2 : 34 img — ce que ça coûte là-bas ------------------------------
def p2(t, d):
    c = pal("encre"); img = neuf("encre"); dr = ImageDraw.Draw(img, "RGBA")
    dx, dy = secousse(t, 0.00, 22)
    mots(dr, "EN CHINE,", t, 0.02, 0.09, cond(86), MARGE+dx, 320+dy, c["texte"])
    mots(dr, "LE MÊME :", t, 0.18, 0.09, cond(86), MARGE+dx, 424+dy, c["accent2"])
    halo(img, W//2, 880, 440, c["accent"], 0.5*eo(ph(t, 0.26, 0.74)))
    compteur(dr, t, 0.26, 0.70, 7000, 1500, 760, c["accent2"], 190)
    q = back(ph(t, 0.74, 1.04))
    if q > 0:
        a = int(252*cl(ph(t, 0.74, 0.88)*1.8))
        txt = "le même engin"; f = cond(52)
        lg = dr.textlength(txt, font=f)+120; y = 1030+int(40*(1-cl(q)))
        dr.rounded_rectangle([W//2-lg/2, y, W//2+lg/2, y+100], 28,
                             fill=c["carte"]+(a,), outline=c["accent"]+(a,), width=3)
        centre(dr, txt, f, y+24, c["texte"], a)
    flash(img, t, 0.26, 0.08, (255, 225, 150), 0.4)
    return img

# ---- 3 : 96 img — la rafale de produits -------------------------------
#        quatre produits réels, leur prix France affiché, le prix d'achat caché
def p3(t, d):
    i = min(RAFALE-1, int(t/0.80))               # 24 images par produit
    v = VEDETTES[i]; u = (t - i*0.80)/0.80       # avancement dans la fiche
    c = pal("sable"); img = neuf("sable"); dr = ImageDraw.Draw(img, "RGBA")
    dx, dy = secousse(t, i*0.80, 16)
    prod = Image.open(TRAV/"produits"/v["fichier"]).convert("RGBA")
    halo(img, W//2+dx, 820+dy, 360, (210, 198, 180), 0.5*eo(ph(u, 0.02, 0.30)))
    poser(img, prod, W//2+dx, 820+dy, 620, back(ph(u, 0.00, 0.34)))
    f = cond(66); nom = v["titre"]
    while dr.textlength(nom, font=f) > W-2*MARGE and f.size > 30:
        f = cond(f.size-2)
    a = int(255*cl(ph(u, 0.10, 0.26)*1.8))
    centre(dr, nom, f, 300+dy, c["texte"], a)
    # le prix affiché, lui, est vérifiable : c'est celui du site
    q = back(ph(u, 0.22, 0.52))
    if q > 0:
        aq = int(255*cl(ph(u, 0.22, 0.36)*1.8))
        lg = 460; y = 1210+int(40*(1-cl(q)))
        dr.rounded_rectangle([W//2-lg/2, y, W//2+lg/2, y+134], 30,
                             fill=c["carte"]+(aq,), outline=c["bord"]+(aq,), width=3)
        centre(dr, "PRIX BOUTIQUE", med(32), y+22, c["sourd"], aq)
        centre(dr, euros(v["prix"]), cond(72), y+56, c["texte"], aq)
    flash(img, t, i*0.80, 0.06, (255, 255, 255), 0.3)
    return img

# ---- 4 : 44 img — et le prix d'achat, lui, ne s'écrit pas -------------
def p4(t, d):
    c = pal("acier"); img = neuf("acier"); dr = ImageDraw.Draw(img, "RGBA")
    dx, dy = secousse(t, 0.00, 18)
    mots(dr, "LE PRIX", t, 0.00, 0.08, cond(96), MARGE+dx, 300+dy, c["texte"])
    mots(dr, "FOURNISSEUR", t, 0.16, 0.08, cond(96), MARGE+dx, 404+dy, c["accent2"])
    # la case du prix reste floutée : on ne l'écrit pas, on le donne en message
    p = back(ph(t, 0.30, 0.64))
    if p > 0:
        a = int(252*cl(ph(t, 0.30, 0.46)*1.8))
        lg = 800; y = 660+int(44*(1-cl(p)))
        dr.rounded_rectangle([W//2-lg/2, y, W//2+lg/2, y+290], 36,
                             fill=c["carte"]+(a,), outline=c["accent"]+(int(a*0.8),), width=4)
        voile = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dv = ImageDraw.Draw(voile)
        for k in range(8):
            dv.rounded_rectangle([W//2-lg/2+56+k*92, y+74, W//2-lg/2+136+k*92, y+212],
                                 18, fill=c["accent"]+(int(a*0.55),))
        img.alpha_composite(voile.filter(ImageFilter.GaussianBlur(17)))
        centre(dr, "RÉSERVÉ", med(40), y+228, c["sourd"], a)
    q = ph(t, 0.70, 1.00)
    if q > 0:
        centre(dr, "je te l'envoie en message", med(48), 1060, c["texte"], int(250*q))
    flash(img, t, 0.30, 0.07, (120, 200, 255), 0.3)
    return img

# ---- 5 : 40 img — tout le reste suit la même règle --------------------
def p5(t, d):
    c = pal("nuit"); img = neuf("nuit"); dr = ImageDraw.Draw(img, "RGBA")
    base = eo(ph(t, 0.04, 1.40))
    for r in range(3):
        y = 700+r*300; sens = 1 if r % 2 == 0 else -1
        dec = int((base*230+t*30)*sens)
        for col in range(5):
            v = VEDETTES[(r*3+col) % len(VEDETTES)]
            pr = Image.open(TRAV/"produits"/v["fichier"]).convert("RGBA")
            x = ((col*260+dec) % (5*260))-130
            a = cl(ph(t, 0.08+col*0.05, 0.40+col*0.05))
            if a <= 0: continue
            dr.rounded_rectangle([x-108, y-108, x+108, y+108], 26,
                                 fill=(246, 246, 250, int(242*a)))
            poser(img, pr, x, y, 168, a, ombre=False)
    v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dv = ImageDraw.Draw(v)
    dv.rectangle([0, 0, W, 640], fill=(10, 8, 20, 220))
    for i in range(14):
        dv.rectangle([0, 640+i*14, W, 640+(i+1)*14], fill=(10, 8, 20, int(220*(1-i/14)**1.4)))
    for i in range(24):
        dv.rectangle([0, H-(i+1)*32, W, H-i*32], fill=(10, 8, 20, int(238*(i/24)**0.75)))
    img.alpha_composite(v)
    mots(dr, "ET SUR TOUT", t, 0.00, 0.08, cond(94), MARGE, 260, c["texte"])
    mots(dr, "LE RESTE AUSSI.", t, 0.24, 0.08, cond(94), MARGE, 364, c["accent2"])
    return img

# ---- 6 : 36 img — l'appel --------------------------------------------
def p6(t, d):
    c = pal("nuit"); img = neuf("nuit"); dr = ImageDraw.Draw(img, "RGBA")
    dx, dy = secousse(t, 0.02, 20)
    halo(img, W//2+dx, 900+dy, 470, c["accent"], 0.6)
    a0 = int(255*eo(ph(t, 0.02, 0.24)))
    centre(dr, "COMMENTE", med(52), 640+dy, c["sourd"], a0)
    p = back(ph(t, 0.14, 0.52))
    if p > 0:
        s = 130; f = cond(s)
        while dr.textlength("CHINABOOK", font=f) > W-2*MARGE and s > 50:
            s -= 3; f = cond(s)
        a = int(255*cl(ph(t, 0.14, 0.32)*1.8))
        centre(dr, "CHINABOOK", f, 750+dy, c["accent2"], a)
    q = back(ph(t, 0.42, 0.80))
    if q > 0:
        a = int(248*cl(ph(t, 0.42, 0.60)*1.7))
        lg = 640; y = 1040+int(36*(1-cl(q)))
        dr.rounded_rectangle([W//2-lg/2, y, W//2+lg/2, y+112], 30,
                             fill=c["carte"]+(a,), outline=c["accent"]+(int(a*0.9),), width=3)
        dr.polygon([(W//2-40, y+112), (W//2+12, y+112), (W//2-26, y+150)], fill=c["carte"]+(a,))
        centre(dr, "et je t'envoie les prix", med(44), y+34, c["texte"], a)
    flash(img, t, 0.14, 0.07, (180, 145, 255), 0.36)
    return img

# ---- 7 : 30 img — contacts -------------------------------------------
def p7(t, d):
    c = pal("nuit"); img = neuf("nuit"); dr = ImageDraw.Draw(img, "RGBA")
    p = back(ph(t, 0.00, 0.34))
    lw = int(620*(0.84+0.16*cl(p)))
    lo = LOGO.resize((lw, int(LOGO.height*lw/LOGO.width)), Image.LANCZOS)
    lo.putalpha(lo.split()[3].point(lambda v: int(v*cl(ph(t, 0.00, 0.22)*1.7))))
    img.alpha_composite(lo, ((W-lw)//2, 560+int(40*(1-cl(p)))))
    for i, (titre, valeur, quand) in enumerate([("WhatsApp", "+1 480 569 1625", 0.26),
                                                ("Snapchat", "dropandyou1", 0.46)]):
        q = back(ph(t, quand, quand+0.28))
        if q <= 0: continue
        a = int(250*cl(ph(t, quand, quand+0.16)*1.7))
        y = 940+i*170+int(34*(1-cl(q)))
        dr.rounded_rectangle([MARGE, y, W-MARGE, y+140], 30, fill=c["carte"]+(a,),
                             outline=c["accent"]+(int(a*0.75),), width=3)
        dr.text((MARGE+46, y+24), titre, font=med(36), fill=c["sourd"]+(a,))
        dr.text((MARGE+46, y+70), valeur, font=cond(54), fill=c["texte"]+(a,))
        flash(img, t, quand, 0.05, (170, 130, 255), 0.2)
    return img

# Chaque plan tient une phrase de la voix off. Le premier nombre est la durée
# réelle, calée sur les respirations détectées dans CB-02.mp3 ; le second est la
# durée pour laquelle l'animation a été écrite. Le montage étire ou resserre le
# temps entre les deux, ce qui évite de réécrire toutes les phases à chaque
# nouvelle prise de voix — une rafale un peu plus serrée se lit mieux, un hook
# un peu plus lent laisse voir le chiffre monter.
PLANS = [(76, p1, 38),      # « Un Surron, en France, ça monte à sept mille euros. »
         (64, p2, 34),      # « En Chine, le même : mille cinq cents. »
         (79, p3, 96),      # « Un sac, des lunettes, une valise, c'est pareil. »
         (57, p4, 44),      # « Le prix fournisseur, je ne l'écris pas. »
         (42, p5, 40),      # « C'est comme ça sur tout le reste. »
         (56, p6, 36),      # « Commente CHINABOOK et je te l'envoie. »
         (30, p7, 30)]      # la carte de contacts, sur la queue de silence


def bornes():
    """Début de chaque plan en secondes, pour le mixage des bruitages."""
    t, b = 0, []
    for n, _, _ in PLANS:
        b.append(t/FPS); t += n
    return b


def echelles():
    """Facteur temps de chaque plan : nominal / réel."""
    return [nom/n for n, _, nom in PLANS]


if __name__ == "__main__":
    out = TRAV/"frames"; out.mkdir(parents=True, exist_ok=True)
    i = 0
    for n, fn, nom in PLANS:
        ech = nom/n
        for k in range(n):
            fn(k/FPS*ech, nom/FPS).convert("RGB").save(out/f"f{i:04d}.png"); i += 1
        print(f"  {fn.__name__}: {n} images  (x{ech:.2f})", flush=True)
    print(f"{i} images ({i/FPS:.3f} s)")
