#!/usr/bin/env python3
"""CB-08 « Même produit, deux prix d'achat » — motion dense, calé au mot.

Sept plans sur 11,467 s (344 images) : moins de 1,7 s chacun. Tout est corrélé
aux respirations du MP3 ; chaque entrée a sa courbe, son flash et son bruitage.

Aucun montant n'est affiché : le contrat interdit d'inventer prix, témoignages
ou preuves. L'écart se montre en barres, pas en euros."""
import math, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS = 1080,1920,30
MARGE = 108
RAC = pathlib.Path(__file__).resolve().parent.parent
V = RAC/"videos/CB-08"
LOGO = Image.open(RAC/"brand-ChinaBook-clair.png").convert("RGBA")

VIOLET=(124,58,237); VIO_VIF=(150,92,255); VIO_CLAIR=(186,162,255)
OR=(201,162,39); OR_CLAIR=(238,205,96)
BLANC=(248,248,251); NOIR=(10,10,14); CARTE=(24,22,34); BORD=(62,56,88)
ROUGE=(228,86,86)
F="/System/Library/Fonts/HelveticaNeue.ttc"
def cond(s): return ImageFont.truetype(F,s,index=9)
def med(s):  return ImageFont.truetype(F,s,index=10)

def cl(x,a=0.,b=1.): return max(a,min(b,x))
def ph(t,d,f): return cl((t-d)/max(1e-6,f-d))
def eo(x): return 1-(1-x)**3
def back(x, k=1.9):
    """dépassement élastique : l'élément va trop loin puis revient"""
    x=cl(x); return 1+ (k+1)*((x-1)**3) + k*((x-1)**2)
def rebond(x):
    x=cl(x)
    return 1-abs(math.cos(x*math.pi*1.5))*(1-x)**1.4

IM = {n: Image.open(V/f"images/{n}.webp").convert("RGB") for n in ["01","02"]}

def couvrir(im,w,h):
    r=max(w/im.width,h/im.height)
    im=im.resize((max(1,int(im.width*r)+1),max(1,int(im.height*r)+1)),Image.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))

def fond_nuit():
    g=Image.new("RGB",(2,H)); px=g.load()
    for y in range(H):
        k=(1-y/H)**1.7
        px[0,y]=px[1,y]=(int(16+30*k),int(13+16*k),int(28+58*k))
    return g.resize((W,H),Image.BILINEAR)
FOND=fond_nuit()

def secousse(t, quand, force=16, duree=0.26):
    """décalage de caméra court après un impact"""
    p=ph(t,quand,quand+duree)
    if p<=0 or p>=1: return (0,0)
    a=force*(1-p)**2
    return (int(a*math.sin(p*38)), int(a*0.6*math.cos(p*31)))

def flash(img, t, quand, duree=0.09, couleur=(255,255,255), force=0.5):
    p=ph(t,quand,quand+duree)
    if p<=0 or p>=1: return
    a=int(255*force*(1-p)**1.6)
    if a<=2: return
    v=Image.new("RGBA",(W,H),couleur+(a,))
    img.paste(Image.alpha_composite(img.convert("RGBA"),v).convert("RGB"),(0,0))

def mots(d, texte, t, depart, pas, police, x0, y, couleurs, trainee=True):
    """révèle le texte mot à mot, chacun monte avec un dépassement"""
    x=x0
    for i,m in enumerate(texte.split(" ")):
        p=ph(t, depart+i*pas, depart+i*pas+0.22)
        if p>0:
            dy=int(30*(1-back(p))); al=int(255*cl(p*1.6))
            c=couleurs[i] if isinstance(couleurs,list) else couleurs
            if trainee and p<0.6:   # traînée : deux copies fantômes au-dessus
                for k,o in enumerate((14,7)):
                    d.text((x,y+dy-o),m,font=police,fill=c+(int(al*0.16*(1-p)),))
            d.text((x,y+dy),m,font=police,fill=c+(al,))
        x += d.textlength(m+" ",font=police)

def barre(d, x0, y, lg, h, p, couleur, etiquette=None, police=None, al=255):
    d.rounded_rectangle([x0,y,x0+lg,y+h],h//2,fill=(255,255,255,26))
    if p>0:
        d.rounded_rectangle([x0,y,x0+lg*cl(p),y+h],h//2,fill=couleur+(al,))
    if etiquette and police:
        d.text((x0,y-54),etiquette,font=police,fill=couleur+(al,))

# ---------------- plans ----------------------------------------------
def p1(t,d):      # 30 img — « Même produit, »
    img=Image.new("RGB",(W,H),NOIR)
    z=1.22-0.20*eo(ph(t,0,d*1.5))
    im=couvrir(IM["01"],int(W*z),int(H*z))
    dx,dy=secousse(t,0.0,22)
    img.paste(im,((W-im.width)//2+dx,(H-im.height)//2+dy))
    v=Image.new("RGBA",(W,H),(0,0,0,0)); dv=ImageDraw.Draw(v)
    dv.rectangle([0,0,W,620],fill=(8,7,16,190))
    img.paste(Image.alpha_composite(img.convert("RGBA"),v).convert("RGB"),(0,0))
    dr=ImageDraw.Draw(img,"RGBA")
    mots(dr,"MÊME PRODUIT.",t,0.04,0.11,cond(96),MARGE,250,BLANC)
    flash(img,t,0.0,0.10,(190,160,255),0.55)
    return img

def p2(t,d):      # 37 img — « deux prix d'achat. »
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    dr=ImageDraw.Draw(img,"RGBA")
    dx,dy=secousse(t,0.0,14)
    mots(dr,"DEUX PRIX.",t,0.02,0.10,cond(104),MARGE+dx,250+dy,VIO_CLAIR)
    # deux colonnes qui tombent
    for i,(lab,coul,quand) in enumerate([("REVENDEUR",ROUGE,0.26),("FOURNISSEUR",VIO_VIF,0.42)]):
        p=back(ph(t,quand,quand+0.30))
        if p<=0: continue
        al=int(255*cl(ph(t,quand,quand+0.18)*1.6))
        x=MARGE+i*((W-2*MARGE)//2+16); lg=(W-2*MARGE)//2-16
        y=640+int(60*(1-p))
        dr.rounded_rectangle([x,y,x+lg,y+300],26,fill=CARTE+(int(238*al/255),),
                             outline=coul+(int(200*al/255),),width=3)
        f=cond(40)
        dr.text((x+lg/2-dr.textlength(lab,font=f)/2,y+40),lab,font=f,fill=coul+(al,))
        f2=cond(120); q="?" 
        dr.text((x+lg/2-dr.textlength(q,font=f2)/2,y+120),q,font=f2,fill=(255,255,255,int(al*0.7)))
    flash(img,t,0.26,0.07,(255,120,120),0.30)
    flash(img,t,0.42,0.07,(170,130,255),0.30)
    return img

def p3(t,d):      # 50 img — « Le revendeur prend sa marge ; »
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    dr=ImageDraw.Draw(img,"RGBA")
    dx,dy=secousse(t,0.30,18)
    mots(dr,"IL PREND",t,0.02,0.09,cond(92),MARGE+dx,230+dy,BLANC)
    mots(dr,"SA MARGE.",t,0.22,0.09,cond(92),MARGE+dx,330+dy,ROUGE)
    # la barre du revendeur se remplit, le surplus se détache
    p=eo(ph(t,0.45,1.25))
    barre(dr,MARGE,760,W-2*MARGE,54,p,ROUGE,"CE QUE TU PAIES",med(34))
    q=eo(ph(t,0.75,1.45))
    if q>0:
        lg=(W-2*MARGE); part=lg*0.62
        dr.rounded_rectangle([MARGE+part,760,MARGE+part+(lg-part)*q,814],27,
                             fill=OR+(int(240*q),))
        f=cond(46); txt="LA MARGE"
        dr.text((MARGE+part+10,700-int(16*q)),txt,font=f,fill=OR_CLAIR+(int(255*q),))
    r=ph(t,1.05,1.35)
    if r>0:
        f=med(36); txt="elle sort de ta poche"
        dr.text((W//2-dr.textlength(txt,font=f)/2,900),txt,font=f,
                fill=(214,210,230,int(240*r)))
    flash(img,t,0.75,0.08,(255,200,90),0.34)
    return img

def p4(t,d):      # 57 img — « le fournisseur te donne son prix. »
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    dr=ImageDraw.Draw(img,"RGBA")
    dx,dy=secousse(t,0.30,18)
    mots(dr,"LE FOURNISSEUR",t,0.02,0.08,cond(78),MARGE+dx,230+dy,BLANC)
    mots(dr,"TE DONNE SON PRIX.",t,0.24,0.07,cond(78),MARGE+dx,322+dy,VIO_CLAIR)
    p=eo(ph(t,0.50,1.20))
    barre(dr,MARGE,760,W-2*MARGE,54,p*0.62,VIO_VIF,"PRIX USINE",med(34))
    q=ph(t,1.05,1.55)
    if q>0:
        lg=W-2*MARGE
        dr.line([MARGE+lg*0.62,700,MARGE+lg*0.62,836],fill=(255,255,255,int(180*q)),width=3)
        f=cond(52); txt="TOUT CE QUI RESTE EST À TOI"
        s=52
        while s>26 and dr.textlength(txt,font=cond(s))>W-2*MARGE: s-=2
        f=cond(s)
        dr.text((W//2-dr.textlength(txt,font=f)/2,900),txt,font=f,fill=VIO_CLAIR+(int(255*q),))
    flash(img,t,0.50,0.08,(150,110,255),0.34)
    return img

def p5(t,d):      # 68 img — « Compare aussi qualité et transport. »
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    dr=ImageDraw.Draw(img,"RGBA")
    mots(dr,"PAS QUE LE PRIX.",t,0.02,0.09,cond(88),MARGE,230,BLANC)
    for i,(txt,quand) in enumerate([("LE PRIX",0.40),("LA QUALITÉ",0.78),("LE TRANSPORT",1.16)]):
        p=back(ph(t,quand,quand+0.30))
        if p<=0: continue
        al=int(255*cl(ph(t,quand,quand+0.16)*1.8))
        y=560+i*190+int(70*(1-p))
        coul = VIO_VIF if i else (90,84,118)
        dr.rounded_rectangle([MARGE,y,W-MARGE,y+150],28,fill=CARTE+(int(240*al/255),),
                             outline=coul+(int(210*al/255),),width=3)
        f=cond(56)
        dr.text((MARGE+52,y+44),txt,font=f,fill=BLANC+(al,))
        # pastille de contrôle
        cx=W-MARGE-80; cy=y+75; r=34
        dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=coul+(int(230*al/255),))
        if i: dr.line([cx-15,cy+2,cx-4,cy+14,cx+16,cy-12],fill=BLANC+(al,),width=7)
        flash(img,t,quand,0.06,(160,120,255),0.22)
    return img

def p6(t,d):      # 52 img — « Tu veux voir des exemples concrets ? »
    img=Image.new("RGB",(W,H),NOIR)
    z=1.18-0.14*eo(ph(t,0,d*1.4))
    im=couvrir(IM["02"],int(W*z),int(H*z))
    dx,dy=secousse(t,0.0,18)
    img.paste(im,((W-im.width)//2+dx,(H-im.height)//2+dy))
    v=Image.new("RGBA",(W,H),(0,0,0,0)); dv=ImageDraw.Draw(v)
    dv.rectangle([0,0,W,640],fill=(8,7,16,205))
    for i in range(30): dv.rectangle([0,H-(i+1)*42,W,H-i*42],fill=(8,7,16,int(228*(i/30)**0.8)))
    img.paste(Image.alpha_composite(img.convert("RGBA"),v).convert("RGB"),(0,0))
    dr=ImageDraw.Draw(img,"RGBA")
    mots(dr,"DES EXEMPLES",t,0.03,0.09,cond(84),MARGE,240,BLANC)
    mots(dr,"CONCRETS ?",t,0.26,0.09,cond(84),MARGE,336,VIO_CLAIR)
    flash(img,t,0.0,0.09,(190,160,255),0.45)
    return img

def p7(t,d):      # 50 img — « Va sur le site ChinaBook. »
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    dr=ImageDraw.Draw(img,"RGBA")
    p=back(ph(t,0.02,0.40))
    lw=int(680*(0.82+0.18*cl(p)))
    lo=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width)),Image.LANCZOS)
    al=lo.split()[3].point(lambda v:int(v*cl(ph(t,0.02,0.26)*1.6)))
    img.paste(lo,((W-lw)//2,700+int(50*(1-cl(p)))),al)
    q=ph(t,0.42,0.72)
    if q>0:
        f=med(44); txt="Le réseau, pas l'intermédiaire."
        dr.text((W//2-dr.textlength(txt,font=f)/2,900),txt,font=f,
                fill=(214,210,232,int(245*q)))
    r=back(ph(t,0.62,0.98))
    if r>0:
        lg=620; y=1090+int(40*(1-cl(r)))
        a=int(252*cl(ph(t,0.62,0.80)*1.6))
        dr.rounded_rectangle([W//2-lg/2,y,W//2+lg/2,y+118],32,fill=VIOLET+(a,))
        f=cond(52); txt="VOIR LES PACKS"
        dr.text((W//2-dr.textlength(txt,font=f)/2,y+32),txt,font=f,fill=BLANC+(a,))
    flash(img,t,0.02,0.10,(255,255,255),0.40)
    flash(img,t,0.62,0.07,(170,130,255),0.26)
    return img

PLANS=[(30,p1),(37,p2),(50,p3),(57,p4),(68,p5),(52,p6),(50,p7)]

if __name__=="__main__":
    out=pathlib.Path(__file__).parent/"_travail/CB-08/frames"
    out.mkdir(parents=True,exist_ok=True)
    i=0
    for n,fn in PLANS:
        for k in range(n):
            fn(k/FPS,n/FPS).save(out/f"f{i:04d}.png"); i+=1
        print(f"  {fn.__name__}: {n}",flush=True)
    print(f"{i} images ({i/FPS:.3f} s)")
