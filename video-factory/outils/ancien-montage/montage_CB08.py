#!/usr/bin/env python3
"""CB-08 — « Même produit, deux prix » · version organique.

260 images, 8,680 s. Sept plans calés sur les sept respirations de la voix
Tomy v4 accélérée à 1,12. Produits réels de la banque DROP&YOU, détourés.

Deux règles de fond : aucun prix affiché (ils se découvrent sur le site, après
l'explication), et un appel à commenter plutôt qu'un renvoi vers un lien —
c'est du contenu organique, pas une annonce payante.
"""
import json, math, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS = 1080,1920,30
MARGE = 108
RAC = pathlib.Path(__file__).resolve().parent.parent
TRAV = pathlib.Path(__file__).parent/"_travail/CB-08"
LOGO = Image.open(RAC/"brand-ChinaBook-clair.png").convert("RGBA")
PROD = sorted((TRAV/"produits").glob("p*.png"))
NOMS = json.load(open(TRAV/"produits/noms.json"))

VIOLET=(124,58,237); VIO_VIF=(150,92,255); VIO_CLAIR=(190,168,255)
OR=(214,174,52); OR_CLAIR=(242,212,110)
BLANC=(249,249,252); NOIR=(9,8,13); CARTE=(25,22,36); BORD=(64,58,92)
ROUGE=(232,92,92); VERT=(86,206,142)
F="/System/Library/Fonts/HelveticaNeue.ttc"
def cond(s): return ImageFont.truetype(F,s,index=9)
def med(s):  return ImageFont.truetype(F,s,index=10)

def cl(x,a=0.,b=1.): return max(a,min(b,x))
def ph(t,d,f): return cl((t-d)/max(1e-6,f-d))
def eo(x): return 1-(1-cl(x))**3
def back(x,k=2.1):
    x=cl(x); return 1+(k+1)*((x-1)**3)+k*((x-1)**2)

def fond():
    g=Image.new("RGB",(2,H)); px=g.load()
    for y in range(H):
        k=(1-y/H)**1.8
        px[0,y]=px[1,y]=(int(14+32*k),int(11+15*k),int(26+62*k))
    return g.resize((W,H),Image.BILINEAR)
FOND=fond()

def halo(img, cx, cy, r, couleur, force=0.5):
    """lueur douce derrière un élément — c'est ce qui donne la profondeur"""
    l=Image.new("RGBA",(r*2,r*2),(0,0,0,0)); d=ImageDraw.Draw(l)
    for i in range(16):
        k=1-i/16; a=int(255*force*(k**2.4)/4)
        rr=int(r*(0.25+0.75*k))
        d.ellipse([r-rr,r-rr,r+rr,r+rr],fill=couleur+(a,))
    l=l.filter(ImageFilter.GaussianBlur(r*0.12))
    img.alpha_composite(l,(cx-r,cy-r)) if img.mode=="RGBA" else \
        img.paste(Image.alpha_composite(img.convert("RGBA"),
                  Image.new("RGBA",(W,H),(0,0,0,0))).convert("RGB"),(0,0))
    return l

def poser(img, prod, cx, cy, haut, p=1.0, ombre=True):
    """pose un produit détouré, avec son ombre portée"""
    if p<=0: return
    h=int(haut*(0.86+0.14*cl(p))); w=max(1,int(prod.width*h/prod.height))
    im=prod.resize((w,h),Image.LANCZOS)
    al=im.split()[3].point(lambda v:int(v*cl(p*1.4)))
    if ombre:
        o=Image.new("RGBA",(w,h),(0,0,0,0)); o.putalpha(al.point(lambda v:int(v*0.5)))
        o=o.filter(ImageFilter.GaussianBlur(18))
        img.alpha_composite(o,(cx-w//2+6, cy-h//2+22))
    im.putalpha(al)
    img.alpha_composite(im,(cx-w//2, cy-h//2))

def mots(d,texte,t,depart,pas,police,x0,y,couleur,trainee=True):
    x=x0
    for i,m in enumerate(texte.split(" ")):
        p=ph(t,depart+i*pas,depart+i*pas+0.20)
        if p>0:
            dy=int(26*(1-back(p))); a=int(255*cl(p*1.7))
            if trainee and p<0.55:
                for o in (12,6):
                    d.text((x,y+dy-o),m,font=police,fill=couleur+(int(a*0.15*(1-p)),))
            d.text((x,y+dy),m,font=police,fill=couleur+(a,))
        x+=d.textlength(m+" ",font=police)

def jalons(img, dr, t, etapes, y, depart=0.10, pas=0.11):
    """La chaîne d'achat, en pastilles reliées. C'est le sujet des plans 3 et 4 :
    le dire en texte ne suffit pas, il faut voir le maillon en trop."""
    n=len(etapes); lg=W-2*MARGE; ecart=lg/(n-1) if n>1 else 0
    for i in range(n-1):
        q=eo(ph(t,depart+i*pas+0.05,depart+i*pas+0.24))
        if q<=0: continue
        x0=MARGE+i*ecart; x1=x0+ecart*q
        dr.line([x0,y,x1,y],fill=(255,255,255,120),width=4)
    for i,(lab,coul,barre) in enumerate(etapes):
        q=back(ph(t,depart+i*pas,depart+i*pas+0.26))
        if q<=0: continue
        a=int(255*cl(ph(t,depart+i*pas,depart+i*pas+0.14)*1.8))
        x=int(MARGE+i*ecart); r=int(46*(0.8+0.2*cl(q)))
        dr.ellipse([x-r,y-r,x+r,y+r],fill=CARTE+(int(246*a/255),),
                   outline=coul+(a,),width=4)
        f=cond(34); lar=dr.textlength(lab,font=f)
        dr.text((x-lar/2,y+r+16),lab,font=f,fill=coul+(a,))
        if barre:
            dr.line([x-r-10,y-r-10,x+r+10,y+r+10],fill=ROUGE+(a,),width=7)
            dr.line([x-r-10,y+r+10,x+r+10,y-r-10],fill=ROUGE+(a,),width=7)

def secousse(t,quand,force=14,duree=0.22):
    p=ph(t,quand,quand+duree)
    if p<=0 or p>=1: return (0,0)
    a=force*(1-p)**2
    return (int(a*math.sin(p*40)), int(a*0.55*math.cos(p*33)))

def flash(img,t,quand,duree=0.08,coul=(255,255,255),force=0.42):
    p=ph(t,quand,quand+duree)
    if p<=0 or p>=1: return
    a=int(255*force*(1-p)**1.7)
    if a>2: img.alpha_composite(Image.new("RGBA",(W,H),coul+(a,)))

def neuf():
    img=Image.new("RGBA",(W,H),(0,0,0,255)); img.paste(FOND.convert("RGBA"),(0,0)); return img

def grain(img):
    return img

# ---- 1 : 22 img — « Même produit, » -----------------------------------
HERO = Image.open(PROD[0]).convert("RGBA")          # sac Hermès : détourage net
def p1(t,d):
    """Hook : un seul sac, grand. Il faut que le pouce s'arrête là."""
    img=neuf(); dr=ImageDraw.Draw(img,"RGBA")
    dx,dy=secousse(t,0.0,20)
    halo(img,W//2+dx,1020+dy,450,VIOLET,0.6)
    p=back(ph(t,0.00,0.36))
    poser(img,HERO,W//2+dx,1020+dy,720,p)
    mots(dr,"MÊME PRODUIT.",t,0.02,0.10,cond(104),MARGE+dx,300+dy,BLANC)
    flash(img,t,0.0,0.09,(190,160,255),0.5)
    return img

# ---- 2 : 30 img — « deux prix d'achat. » ------------------------------
def p2(t,d):
    """Le sac se dédouble : un seul produit, deux prix. L'écart se voit avant
    d'être dit — les deux étiquettes tombent juste après la séparation."""
    img=neuf(); dr=ImageDraw.Draw(img,"RGBA")
    e=eo(ph(t,0.00,0.30))                 # écartement
    haut=int(720-310*e); ecart=int(236*e)
    halo(img,W//2,1000,420,VIOLET,0.45)
    for s in (-1,1):
        poser(img,HERO,W//2+s*ecart,1000,haut,1.0)
    mots(dr,"DEUX PRIX.",t,0.02,0.09,cond(108),MARGE,300,VIO_CLAIR)
    for i,(lab,coul,quand) in enumerate([("REVENDEUR",ROUGE,0.30),("FOURNISSEUR",VIO_VIF,0.44)]):
        p=back(ph(t,quand,quand+0.26))
        if p<=0: continue
        a=int(255*cl(ph(t,quand,quand+0.15)*1.8))
        lg=372; x=W//2+(-1 if i==0 else 1)*236-lg//2
        y=1300+int(44*(1-p))
        dr.rounded_rectangle([x,y,x+lg,y+92],22,fill=CARTE+(int(242*a/255),),
                             outline=coul+(int(225*a/255),),width=3)
        f=cond(44)
        dr.text((x+lg/2-dr.textlength(lab,font=f)/2,y+24),lab,font=f,fill=coul+(a,))
        flash(img,t,quand,0.05,coul,0.22)
    return img

# ---- 3 : 43 img — « Le revendeur prend sa marge ; » -------------------
def p3(t,d):
    img=neuf(); dr=ImageDraw.Draw(img,"RGBA")
    dx,dy=secousse(t,0.22,16)
    mots(dr,"IL PREND",t,0.00,0.08,cond(96),MARGE+dx,250+dy,BLANC)
    mots(dr,"SA MARGE.",t,0.18,0.08,cond(96),MARGE+dx,354+dy,ROUGE)
    jalons(img,dr,t,[("USINE",VIO_CLAIR,False),("REVENDEUR",ROUGE,False),("TOI",BLANC,False)],580)
    lg=W-2*MARGE; y=790
    dr.rounded_rectangle([MARGE,y,MARGE+lg,y+58],29,fill=(255,255,255,24))
    p=eo(ph(t,0.32,0.95))
    if p>0: dr.rounded_rectangle([MARGE,y,MARGE+lg*p,y+58],29,fill=ROUGE+(248,))
    q=eo(ph(t,0.62,1.15))
    if q>0:
        part=lg*0.60
        dr.rounded_rectangle([MARGE+part,y,MARGE+part+(lg-part)*q,y+58],29,fill=OR+(250,))
        halo(img,int(MARGE+part+(lg-part)*q/2),y+29,140,OR,0.5*q)
        f=cond(50)
        dr.text((MARGE+part+14,y-78),"LA MARGE",font=f,fill=OR_CLAIR+(int(255*q),))
    r=ph(t,0.88,1.15)
    if r>0:
        f=med(40); txt="elle sort de ta poche"
        dr.text((W//2-dr.textlength(txt,font=f)/2,880),txt,font=f,fill=(216,212,234,int(248*r)))
    s=back(ph(t,0.40,0.78))
    if s>0:
        halo(img,W//2,1190,300,ROUGE,0.26*cl(s))
        poser(img,HERO,W//2,1190,460,s)
    flash(img,t,0.62,0.07,(255,205,95),0.32)
    return img

# ---- 4 : 47 img — « le fournisseur te donne son prix. » ---------------
def p4(t,d):
    img=neuf(); dr=ImageDraw.Draw(img,"RGBA")
    dx,dy=secousse(t,0.20,16)
    mots(dr,"LE FOURNISSEUR",t,0.00,0.07,cond(80),MARGE+dx,250+dy,BLANC)
    mots(dr,"TE DONNE SON PRIX.",t,0.20,0.06,cond(80),MARGE+dx,346+dy,VIO_CLAIR)
    jalons(img,dr,t,[("FOURNISSEUR",VIO_CLAIR,False),("REVENDEUR",ROUGE,True),("TOI",BLANC,False)],580)
    lg=W-2*MARGE; y=790
    dr.rounded_rectangle([MARGE,y,MARGE+lg,y+58],29,fill=(255,255,255,24))
    p=eo(ph(t,0.34,0.92))
    if p>0:
        dr.rounded_rectangle([MARGE,y,MARGE+lg*0.60*p,y+58],29,fill=VIO_VIF+(250,))
        if p>0.8: halo(img,int(MARGE+lg*0.30),y+29,170,VIOLET,0.42)
    q=ph(t,0.80,1.20)
    if q>0:
        dr.line([MARGE+lg*0.60,y-34,MARGE+lg*0.60,y+92],fill=(255,255,255,int(190*q)),width=3)
        f=cond(54); txt="LE RESTE EST À TOI"
        dr.text((W//2-dr.textlength(txt,font=f)/2,875),txt,font=f,fill=VIO_CLAIR+(int(255*q),))
    s=back(ph(t,0.42,0.80))
    if s>0:
        halo(img,W//2,1190,300,VIOLET,0.34*cl(s))
        poser(img,HERO,W//2,1190,460,s)
    flash(img,t,0.34,0.07,(150,110,255),0.3)
    return img

# ---- 5 : 63 img — « Compare aussi la qualité et le transport. » -------
GRILLE=[1,2,4,5,6,7,8,9,12,13]
def p5(t,d):
    img=neuf(); dr=ImageDraw.Draw(img,"RGBA")
    # mur de produits : trois rangées qui glissent à vitesses différentes
    base=eo(ph(t,0.05,2.10))
    for r in range(3):
        y=660+r*300
        sens=1 if r%2==0 else -1
        dec=int((base*210+t*26)*sens)
        for c in range(5):
            k=GRILLE[(r*3+c)%len(GRILLE)]
            pr=Image.open(PROD[k]).convert("RGBA")
            x=((c*260+dec) % (5*260)) - 130
            a=cl(ph(t,0.10+c*0.05,0.42+c*0.05))
            if a<=0: continue
            dr.rounded_rectangle([x-108,y-108,x+108,y+108],26,
                                 fill=(246,246,250,int(242*a)))
            poser(img,pr,x,y,168,a,ombre=False)
    # voile pour détacher les pastilles
    v=Image.new("RGBA",(W,H),(0,0,0,0)); dv=ImageDraw.Draw(v)
    dv.rectangle([0,0,W,620],fill=(10,8,20,215))
    for i in range(14): dv.rectangle([0,620+i*14,W,620+(i+1)*14],fill=(10,8,20,int(215*(1-i/14)**1.4)))
    for i in range(26): dv.rectangle([0,H-(i+1)*30,W,H-i*30],fill=(10,8,20,int(236*(i/26)**0.75)))
    img.alpha_composite(v)
    # le titre se pose sur le voile, sinon le mur le noie
    mots(dr,"PAS QUE LE PRIX.",t,0.00,0.08,cond(92),MARGE,250,BLANC)
    for i,(txt,quand) in enumerate([("LA QUALITÉ",0.70),("LE TRANSPORT",1.20)]):
        p=back(ph(t,quand,quand+0.28))
        if p<=0: continue
        a=int(255*cl(ph(t,quand,quand+0.15)*1.8))
        f=cond(58); lg=dr.textlength(txt,font=f)+150
        y=1130+i*124+int(40*(1-p))
        dr.rounded_rectangle([W//2-lg/2,y,W//2+lg/2,y+100],28,
                             fill=CARTE+(int(244*a/255),),outline=VIO_VIF+(int(220*a/255),),width=3)
        dr.text((W//2-lg/2+40,y+22),txt,font=f,fill=BLANC+(a,))
        cx=int(W//2+lg/2-56); cy=y+50
        dr.ellipse([cx-28,cy-28,cx+28,cy+28],fill=VERT+(int(235*a/255),))
        dr.line([cx-12,cy+1,cx-3,cy+12,cx+13,cy-10],fill=(255,255,255,a),width=6)
        flash(img,t,quand,0.05,(130,230,175),0.2)
    return img

# ---- 6 : 29 img — « Commente CHINABOOK » ------------------------------
def p6(t,d):
    img=neuf(); dr=ImageDraw.Draw(img,"RGBA")
    dx,dy=secousse(t,0.02,20)
    halo(img,W//2+dx,960+dy,460,VIOLET,0.6)
    f0=med(50); txt="COMMENTE"
    a0=int(255*eo(ph(t,0.02,0.24)))
    dr.text((W//2-dr.textlength(txt,font=f0)/2,660+dy),txt,font=f0,fill=(220,216,238,a0))
    p=back(ph(t,0.14,0.52))
    if p>0:
        s=int(126*(0.78+0.22*cl(p))); f=cond(s); mot="CHINABOOK"
        while dr.textlength(mot,font=f)>W-2*MARGE and s>50:
            s-=3; f=cond(s)
        a=int(255*cl(ph(t,0.14,0.32)*1.8))
        dr.text((W//2-dr.textlength(mot,font=f)/2+dx,770+dy),mot,font=f,fill=VIO_CLAIR+(a,))
    q=back(ph(t,0.42,0.80))
    if q>0:
        a=int(248*cl(ph(t,0.42,0.60)*1.7))
        lg=620; y=1060+int(36*(1-cl(q)))
        dr.rounded_rectangle([W//2-lg/2,y,W//2+lg/2,y+112],30,fill=CARTE+(a,),
                             outline=VIO_VIF+(int(a*0.9),),width=3)
        dr.polygon([(W//2-40,y+112),(W//2+12,y+112),(W//2-26,y+150)],fill=CARTE+(a,))
        f2=med(42); t2="et je t'envoie le lien"
        dr.text((W//2-dr.textlength(t2,font=f2)/2,y+34),t2,font=f2,fill=(226,222,242,a))
    flash(img,t,0.14,0.07,(180,145,255),0.36)
    return img

# ---- 7 : 26 img — contacts -------------------------------------------
def p7(t,d):
    img=neuf(); dr=ImageDraw.Draw(img,"RGBA")
    p=back(ph(t,0.00,0.34))
    lw=int(620*(0.84+0.16*cl(p)))
    lo=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width)),Image.LANCZOS)
    al=lo.split()[3].point(lambda v:int(v*cl(ph(t,0.00,0.22)*1.7)))
    lo.putalpha(al); img.alpha_composite(lo,((W-lw)//2,560+int(40*(1-cl(p)))))
    lignes=[("WhatsApp","+1 480 569 1625",0.26),("Snapchat","dropandyou1",0.46)]
    for i,(titre,valeur,quand) in enumerate(lignes):
        q=back(ph(t,quand,quand+0.28))
        if q<=0: continue
        a=int(250*cl(ph(t,quand,quand+0.16)*1.7))
        y=940+i*170+int(34*(1-cl(q)))
        dr.rounded_rectangle([MARGE,y,W-MARGE,y+140],30,fill=CARTE+(a,),
                             outline=VIO_VIF+(int(a*0.75),),width=3)
        dr.text((MARGE+46,y+24),titre,font=med(36),fill=(196,192,218,a))
        dr.text((MARGE+46,y+70),valeur,font=cond(54),fill=BLANC+(a,))
        flash(img,t,quand,0.05,(170,130,255),0.2)
    return img

PLANS=[(22,p1),(30,p2),(43,p3),(47,p4),(63,p5),(29,p6),(26,p7)]

if __name__=="__main__":
    out=TRAV/"frames"; out.mkdir(parents=True,exist_ok=True)
    i=0
    for n,fn in PLANS:
        for k in range(n):
            fn(k/FPS,n/FPS).convert("RGB").save(out/f"f{i:04d}.png"); i+=1
        print(f"  {fn.__name__}: {n}",flush=True)
    print(f"{i} images ({i/FPS:.3f} s)")
