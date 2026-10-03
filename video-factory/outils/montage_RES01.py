#!/usr/bin/env python3
"""Montage RES-01 — calé sur la voix Tomy v4 (22,439 s, 673 images).
Charte DYOU : marges 10 %, rien d'important sous 75 %, alternance photo / carton violet."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

W,H,FPS = 1080,1920,30
MARGE = 108
RAC = pathlib.Path(__file__).resolve().parent.parent
V = RAC/"videos/RES-01"
TRAV = pathlib.Path(__file__).parent/"_travail/RES-01"
LOGO = Image.open(RAC/"brand-DYOU-original.png").convert("RGB")

VIOLET=(124,58,237); VIO_CLAIR=(167,139,250); BLANC=(248,248,251)
NOIR=(8,9,13); CARTE=(26,23,37); BORD=(60,54,86); ROUGE=(224,96,96)
F="/System/Library/Fonts/HelveticaNeue.ttc"
def cond(s): return ImageFont.truetype(F,s,index=9)
def med(s):  return ImageFont.truetype(F,s,index=10)
def eo(t): return 1-(1-t)**3
def cl(x,a=0.,b=1.): return max(a,min(b,x))
def ph(t,d,f): return cl((t-d)/max(1e-6,f-d))
def couvrir(im,w,h):
    r=max(w/im.width,h/im.height)
    im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))

def _fond():
    g=Image.new("RGB",(2,H)); px=g.load()
    for y in range(H):
        k=(1-y/H)**1.6
        px[0,y]=px[1,y]=(int(30+34*k),int(20+22*k),int(58+60*k))
    return g.resize((W,H),Image.BILINEAR)
FOND=_fond()
IMG={n:Image.open(V/f"images/{n}.webp").convert("RGB") for n in ["01","02","03"]}
ECR=sorted((TRAV/"phone").glob("p*.png"))

def entete(img,prog):
    d=ImageDraw.Draw(img,"RGBA")
    n=6; lg=(W-2*MARGE-(n-1)*10)/n
    for i in range(n):
        x=MARGE+i*(lg+10); p=cl(prog*n-i)
        d.rounded_rectangle([x,96,x+lg,102],3,fill=(255,255,255,46))
        if p>0: d.rounded_rectangle([x,96,x+lg*p,102],3,fill=VIO_CLAIR+(235,))
    lo=LOGO.resize((62,62),Image.LANCZOS); img.paste(lo,(MARGE,136))
    d.text((MARGE+78,152),"DYOU Agency",font=med(30),fill=(226,226,236,228))

def titre(img,t,d0,lignes,y=252):
    d=ImageDraw.Draw(img,"RGBA")
    for i,(txt,vi) in enumerate(lignes):
        p=eo(ph(t,d0+i*0.10,d0+i*0.10+0.40)); al=int(255*p)
        s=84
        while s>38 and d.textlength(txt,font=cond(s))>W-2*MARGE: s-=2
        f=cond(s)
        d.text((W//2-d.textlength(txt,font=f)/2, y+i*94+int(24*(1-p))), txt, font=f,
               fill=(VIO_CLAIR if vi else BLANC)+(al,))

def photo(img,n,p,zoom=0.12,haut=0.62):
    z=1.0+zoom*p
    im=couvrir(IMG[n],int(W*z),int(H*z))
    img.paste(im,((W-im.width)//2,(H-im.height)//2))
    v=Image.new("RGBA",(W,H),(0,0,0,0)); dv=ImageDraw.Draw(v)
    for i in range(40): dv.rectangle([0,H-(i+1)*48,W,H-i*48],fill=(10,8,20,int(236*(i/40)**0.7)))
    dv.rectangle([0,0,W,500],fill=(10,8,20,int(255*haut)))
    img.paste(Image.alpha_composite(img.convert("RGBA"),v).convert("RGB"),(0,0))

# ---- 1 : 72 img — le sol est magnifique
def p1(t,d):
    img=Image.new("RGB",(W,H),NOIR); photo(img,"01",eo(ph(t,0,d)),0.14,0.66)
    titre(img,t,0.08,[("TON DERNIER SOL",0),("EST MAGNIFIQUE.",1)])
    return img

# ---- 2 : 168 img — tu fouilles ton téléphone
def p2(t,d):
    img=Image.new("RGB",(W,H),NOIR); photo(img,"02",eo(ph(t,0,d)),0.12,0.60)
    titre(img,t,0.05,[("TU FOUILLES",0),("TON TÉLÉPHONE.",1)])
    dr=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,1.5,2.0))
    if a>0:
        y=1080; dr.rounded_rectangle([MARGE,y,W-MARGE,y+150],26,
            fill=CARTE+(int(240*a),),outline=BORD+(int(200*a),),width=2)
        f=cond(92); txt="10 MINUTES"
        dr.text((W//2-dr.textlength(txt,font=f)/2,y+26),txt,font=f,fill=ROUGE+(int(255*a),))
        b=eo(ph(t,2.4,2.9)); f2=med(38)
        dr.text((W//2-dr.textlength("à chercher les bonnes photos",font=f2)/2,y+182),
                "à chercher les bonnes photos",font=f2,fill=(206,202,224,int(240*b)))
    return img

# ---- 3 : 86 img — il compare trois artisans
def p3(t,d):
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    titre(img,t,0.03,[("PENDANT CE TEMPS,",0),("IL EN COMPARE TROIS.",1)])
    dr=ImageDraw.Draw(img,"RGBA")
    noms=[("ARTISAN A","site à jour",0.35,False),("ARTISAN B","photos rangées",0.70,False),
          ("TOI","photos dans le téléphone",1.05,True)]
    for i,(nom,sous,quand,moi) in enumerate(noms):
        a=eo(ph(t,quand,quand+0.34))
        if a<=0: continue
        y=740+i*180; dy=int(28*(1-a))
        dr.rounded_rectangle([MARGE,y+dy,W-MARGE,y+146+dy],24,
            fill=(CARTE if not moi else (46,24,28))+(int(240*a),),
            outline=(ROUGE if moi else BORD)+(int(220*a),),width=3 if moi else 2)
        dr.text((MARGE+44,y+dy+26),nom,font=cond(50),fill=(ROUGE if moi else BLANC)+(int(255*a),))
        dr.text((MARGE+44,y+dy+90),sous,font=med(32),fill=(200,196,218,int(236*a)))
    return img

# ---- 4 : 221 img — le site DYOU
def p4(t,d,k):
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    titre(img,t,0.05,[("TOUT EST RANGÉ.",0),("LE DEVIS EST LÀ.",1)])
    dr=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,0.30,0.80))
    pw,phh=390,820; px,py=(W-pw)//2,500+int(48*(1-a))
    dr.rounded_rectangle([px-17,py-17,px+pw+17,py+phh+17],56,
                         fill=(18,17,24,int(255*a)),outline=(92,88,116,int(228*a)),width=3)
    ec=Image.open(ECR[min(k,len(ECR)-1)]).convert("RGB")
    m=Image.new("L",(pw,phh),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw-1,phh-1],radius=44,fill=int(255*a))
    img.paste(ec,(px,py),m)
    for txt,quand in [("TES RÉALISATIONS",1.1),("TES FINITIONS",3.0),("DEMANDE DE DEVIS",4.9)]:
        b=eo(ph(t,quand,quand+0.30))*(1-ph(t,quand+1.45,quand+1.72))
        if b<=0: continue
        f=cond(42); lg=dr.textlength(txt,font=f)+80; y=1348
        dr.rounded_rectangle([W//2-lg/2,y,W//2+lg/2,y+76],22,fill=VIOLET+(int(246*b),))
        dr.text((W//2-dr.textlength(txt,font=f)/2,y+18),txt,font=f,fill=BLANC+(int(255*b),))
    return img

# ---- 5 : 68 img — montre ton travail
def p5(t,d):
    # le texte parle du travail : on remontre le sol, cadre plus serre qu'au plan 1
    img=Image.new("RGB",(W,H),NOIR); photo(img,"01",0.55+0.45*eo(ph(t,0,d)),0.34,0.62)
    titre(img,t,0.03,[("MONTRE TON TRAVAIL",0),("COMME IL LE MÉRITE.",1)])
    return img

# ---- 6 : 59 img — CTA
def p6(t,d):
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    dr=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,0.02,0.36)); s=int(260*(0.9+0.1*a))
    lo=LOGO.resize((s,s),Image.LANCZOS)
    tmp=Image.new("RGB",(W,H),(0,0,0)); tmp.paste(lo,((W-s)//2,560))
    msk=Image.new("L",(W,H),0); ImageDraw.Draw(msk).rectangle([(W-s)//2,560,(W-s)//2+s,560+s],fill=int(255*a))
    img.paste(tmp,(0,0),msk)
    b=eo(ph(t,0.30,0.68)); f=cond(96)
    for i,txt in enumerate(["REMPLIS","LE FORMULAIRE"]):
        dr.text((W//2-dr.textlength(txt,font=f)/2,900+i*106),txt,font=f,fill=BLANC+(int(255*b),))
    c=eo(ph(t,0.60,0.95))
    if c>0:
        y=1180; lg=600
        dr.rounded_rectangle([W//2-lg/2,y,W//2+lg/2,y+112],30,fill=VIOLET+(int(252*c),))
        f2=cond(48); txt="DYOU-AGENCY.COM"
        dr.text((W//2-dr.textlength(txt,font=f2)/2,y+32),txt,font=f2,fill=BLANC+(int(255*c),))
    return img

PLANS=[(72,p1),(168,p2),(86,p3),(220,p4),(68,p5),(59,p6)]

if __name__=="__main__":
    out=TRAV/"frames"; out.mkdir(parents=True,exist_ok=True)
    tot=sum(n for n,_ in PLANS); i=0
    for n,fn in PLANS:
        for k in range(n):
            img = fn(k/FPS,n/FPS,k) if fn is p4 else fn(k/FPS,n/FPS)
            entete(img,i/tot); img.save(out/f"f{i:04d}.png"); i+=1
        print(f"  {fn.__name__}: {n}",flush=True)
    print(f"{i} images ({i/FPS:.3f} s)")
