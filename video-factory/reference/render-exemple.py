#!/usr/bin/env python3
"""DYOU × Résine — motion calé sur la voix ElevenLabs (25,81 s).
Charte DYOU : fond violet profond, typo condensée, cartes arrondies.
Zone de sécurité : marges latérales 10 %, rien d'important sous 75 % de hauteur."""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS = 1080,1920,30
MARGE = 108
BAS_SUR = int(H*0.75)                       # 1440 px
HOME = pathlib.Path.home()
POLY = HOME/"Desktop/dyou-netlify-ready/assets/work/polyra"
LOGO = Image.open(HOME/"Desktop/dyou-netlify-ready/assets/images/dyou-logo-horizontal.webp").convert("RGBA")
ICI  = pathlib.Path(__file__).parent

VIOLET=(124,58,237); VIO_CLAIR=(167,139,250); BLANC=(248,248,251)
NOIR=(8,9,13); CARTE=(26,23,37); BORD=(60,54,86)
FONT="/System/Library/Fonts/HelveticaNeue.ttc"
def cond(s): return ImageFont.truetype(FONT,s,index=9)   # Condensed Black
def medium(s): return ImageFont.truetype(FONT,s,index=10)

def eo(t): return 1-(1-t)**3
def cl(x,a=0.,b=1.): return max(a,min(b,x))
def ph(t,d,f): return cl((t-d)/max(1e-6,f-d))
def couvrir(im,w,h):
    r=max(w/im.width,h/im.height)
    im=im.resize((max(1,int(im.width*r)+1),max(1,int(im.height*r)+1)),Image.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))

# --- fond violet dégradé, calculé une seule fois ------------------------
def _fond():
    g=Image.new("RGB",(2,H))
    px=g.load()
    for y in range(H):
        k=y/H
        px[0,y]=px[1,y]=(int(30+34*(1-k)**1.6), int(20+22*(1-k)**1.6), int(58+60*(1-k)**1.6))
    return g.resize((W,H),Image.BILINEAR)
FOND=_fond()

PHOTOS={n:Image.open(POLY/f"{n}.webp").convert("RGB")
        for n in ["polyra-residential","polyra-matte","reel-geste","reel-marbre"]}
ECRANS=sorted((ICI/"phone").glob("p*.png"))

# --- habillage permanent ----------------------------------------------
def entete(img,t,prog):
    d=ImageDraw.Draw(img,"RGBA")
    n=8; lg=(W-2*MARGE-(n-1)*10)/n
    for i in range(n):
        x=MARGE+i*(lg+10); plein=cl(prog*n-i)
        d.rounded_rectangle([x,96,x+lg,102],3,fill=(255,255,255,46))
        if plein>0: d.rounded_rectangle([x,96,x+lg*plein,102],3,fill=VIO_CLAIR+(235,))
    lw=116; lo=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width)),Image.LANCZOS)
    img.paste(lo,(MARGE,140),lo)
    d.text((MARGE+lw+22,154),"DYOU Agency",font=medium(30),fill=(226,226,236,228))

def titre(img,t,d0,lignes,y=250):
    d=ImageDraw.Draw(img,"RGBA")
    for i,(txt,viol) in enumerate(lignes):
        p=eo(ph(t,d0+i*0.11,d0+i*0.11+0.42)); al=int(255*p)
        taille=86
        while taille>40:
            f=cond(taille)
            if d.textlength(txt,font=f)<=W-2*MARGE: break
            taille-=2
        f=cond(taille)
        dy=int(26*(1-p))
        d.text((W//2-d.textlength(txt,font=f)/2, y+i*96+dy), txt, font=f,
               fill=(VIO_CLAIR if viol else BLANC)+(al,))

def carte(d,x0,y0,x1,y1,a=1.0,plein=CARTE,r=26):
    d.rounded_rectangle([x0,y0,x1,y1],r,fill=plein+(int(238*a),),outline=BORD+(int(190*a),),width=2)

def photo_fond(img,nom,p,zoom=0.10,sombre=0.42):
    z=1.0+zoom*p
    im=couvrir(PHOTOS[nom],int(W*z),int(H*z))
    img.paste(im,((W-im.width)//2,(H-im.height)//2))
    v=Image.new("RGBA",(W,H),(0,0,0,0)); dv=ImageDraw.Draw(v)
    for i in range(44):   # voile dégradé bas→haut pour détacher le texte
        dv.rectangle([0,H-(i+1)*44,W,H-i*44],fill=(10,8,20,int(238*(i/44)**0.7)))
    dv.rectangle([0,0,W,470],fill=(10,8,20,int(255*sombre)))
    img.alpha_composite(v) if img.mode=="RGBA" else img.paste(Image.alpha_composite(img.convert("RGBA"),v).convert("RGB"),(0,0))

# ---------------- les 8 plans -----------------------------------------
def p1(t,d):      # 0,00 → 2,73   "Tu poses des sols en résine qui transforment une pièce."
    img=Image.new("RGB",(W,H),NOIR)
    photo_fond(img,"polyra-residential",eo(ph(t,0,d)),zoom=0.13,sombre=0.66)
    titre(img,t,0.10,[("TU POSES DES SOLS",0),("EN RÉSINE",1)],y=250)
    if t>0.95: titre(img,t,1.00,[("QUI TRANSFORMENT",0),("UNE PIÈCE.",0)],y=452)
    return img

def p2(t,d):      # 2,73 → 4,41   "Mais pour décrocher un chantier…"
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    titre(img,t,0.05,[("MAIS POUR DÉCROCHER",0),("UN CHANTIER…",1)],y=250)
    d_=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,0.30,0.70))
    if a>0:
        carte(d_,MARGE,700,W-MARGE,1180,a)
        f=cond(50)
        d_.text((W//2-d_.textlength("TON TEMPS PART DANS",font=f)/2,776),
                "TON TEMPS PART DANS",font=f,fill=BLANC+(int(255*a),))
        for i,txt in enumerate(["LES PHOTOS","LES EXPLICATIONS"]):
            b=eo(ph(t,0.60+i*0.22,0.95+i*0.22))
            if b<=0: continue
            y=896+i*98; fw=d_.textlength(txt,font=medium(40))
            d_.rounded_rectangle([W//2-fw/2-34,y,W//2+fw/2+34,y+70],18,
                                 fill=(44,38,66,int(238*b)),outline=BORD+(int(200*b),),width=2)
            d_.text((W//2-fw/2,y+16),txt,font=medium(40),fill=(222,220,236,int(255*b)))
    return img

def p3(t,d):      # 4,41 → 8,41   "Tes soirées dans les messages."
    img=Image.new("RGB",(W,H),NOIR)
    photo_fond(img,"reel-geste",eo(ph(t,0,d)),zoom=0.12,sombre=0.62)
    titre(img,t,0.05,[("TES SOIRÉES",1),("DANS LES MESSAGES.",0)],y=250)
    d_=ImageDraw.Draw(img,"RGBA")
    bulles=[("Bonjour, vous faites du marbré ?",0,0.45),
            ("Voici les photos du chantier…",1,1.15),
            ("Et les finitions ?",0,1.85),
            ("Je vous envoie un devis demain",1,2.45)]
    for n,(txt,moi,quand) in enumerate(bulles):
        a=eo(ph(t,quand,quand+0.30))
        if a<=0: continue
        f=medium(36); lg=d_.textlength(txt,font=f)+56
        y=700+n*118
        x=(W-MARGE-lg) if moi else MARGE
        d_.rounded_rectangle([x,y,x+lg,y+82],24,
            fill=(VIOLET if moi else (38,34,52))+(int(242*a),))
        d_.text((x+28,y+22),txt,font=f,fill=BLANC+(int(255*a),))
    return img

def p4(t,d):      # 8,41 → 11,68  "Les mêmes questions."
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    titre(img,t,0.05,[("LES MÊMES",0),("QUESTIONS.",1)],y=250)
    d_=ImageDraw.Draw(img,"RGBA")
    for i,txt in enumerate(["QUEL RENDU ?","QUELLE FINITION ?","COMMENT DEMANDER UN DEVIS ?"]):
        a=eo(ph(t,0.45+i*0.42,0.85+i*0.42))
        if a<=0: continue
        y=710+i*172; dy=int(30*(1-a))
        carte(d_,MARGE,y+dy,W-MARGE,y+136+dy,a)
        taille=48
        while taille>26 and d_.textlength(txt,font=cond(taille))>W-2*MARGE-70: taille-=2
        f=cond(taille)
        d_.text((W//2-d_.textlength(txt,font=f)/2,y+dy+42),txt,font=f,fill=BLANC+(int(255*a),))
    return img

def p5(t,d):      # 11,68 → 13,30  signature
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    d_=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,0.05,0.50)); lw=int(430*(0.88+0.12*a))
    lo=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width)),Image.LANCZOS)
    tmp=Image.new("RGBA",(W,H),(0,0,0,0)); tmp.paste(lo,((W-lw)//2,620),lo)
    img.paste(tmp.convert("RGB"),(0,0),tmp.split()[3].point(lambda v:int(v*a)))
    f=cond(76)
    d_.text((W//2-d_.textlength("DYOU AGENCY",font=f)/2,900),"DYOU AGENCY",font=f,fill=BLANC+(int(255*a),))
    b=eo(ph(t,0.45,0.85)); f2=medium(38)
    d_.text((W//2-d_.textlength("TES CHANTIERS MIS EN VALEUR.",font=f2)/2,1010),
            "TES CHANTIERS MIS EN VALEUR.",font=f2,fill=VIO_CLAIR+(int(242*b),))
    return img

def p6(t,d,i_frame):   # 13,30 → 19,20  le site, dans un vrai téléphone
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    titre(img,t,0.05,[("UN SITE POUR",0),("MONTRER TON TRAVAIL.",1)],y=250)
    d_=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,0.25,0.70))
    pw,phh=390,820; px,py=(W-pw)//2,500+int(50*(1-a))
    d_.rounded_rectangle([px-17,py-17,px+pw+17,py+phh+17],56,
                         fill=(18,17,24,int(255*a)),outline=(92,88,116,int(230*a)),width=3)
    k=min(i_frame,len(ECRANS)-1)
    ec=Image.open(ECRANS[k]).convert("RGB")
    m=Image.new("L",(pw,phh),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw-1,phh-1],radius=44,fill=int(255*a))
    img.paste(ec,(px,py),m)
    libelles=[("RÉALISATIONS",0.6),("PRESTATIONS",2.3),("DEMANDE DE DEVIS",4.0)]
    for txt,quand in libelles:
        b=eo(ph(t,quand,quand+0.32))*(1-ph(t,quand+1.45,quand+1.70))
        if b<=0: continue
        f=cond(40); lg=d_.textlength(txt,font=f)+76
        y=1348
        d_.rounded_rectangle([W//2-lg/2,y,W//2+lg/2,y+74],22,fill=VIOLET+(int(246*b),))
        d_.text((W//2-d_.textlength(txt,font=f)/2,y+18),txt,font=f,fill=BLANC+(int(255*b),))
    return img

def p7(t,d):      # 19,20 → 23,10  "Ton savoir-faire mérite mieux."
    img=Image.new("RGB",(W,H),NOIR)
    photo_fond(img,"polyra-matte",eo(ph(t,0,d)),zoom=0.12,sombre=0.64)
    titre(img,t,0.05,[("TON SAVOIR-FAIRE",0),("MÉRITE MIEUX.",1)],y=250)
    d_=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,0.90,1.35))
    if a>0:
        y=1180; carte(d_,MARGE,y,W-MARGE,y+196,a,plein=(16,14,26))
        f=cond(46); f2=medium(36)
        d_.text((W//2-d_.textlength("QUE DES PHOTOS PERDUES",font=f)/2,y+44),
                "QUE DES PHOTOS PERDUES",font=f,fill=BLANC+(int(255*a),))
        d_.text((W//2-d_.textlength("DANS UNE CONVERSATION.",font=f2)/2,y+116),
                "DANS UNE CONVERSATION.",font=f2,fill=(200,196,220,int(246*a)))
    return img

def p8(t,d):      # 23,10 → 25,80  CTA
    img=Image.new("RGB",(W,H),NOIR); img.paste(FOND)
    d_=ImageDraw.Draw(img,"RGBA")
    a=eo(ph(t,0.05,0.42)); lw=int(360*(0.9+0.1*a))
    lo=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width)),Image.LANCZOS)
    tmp=Image.new("RGBA",(W,H),(0,0,0,0)); tmp.paste(lo,((W-lw)//2,470),lo)
    img.paste(tmp.convert("RGB"),(0,0),tmp.split()[3].point(lambda v:int(v*a)))
    b=eo(ph(t,0.35,0.75)); f0=medium(44)
    d_.text((W//2-d_.textlength("ÉCRIS",font=f0)/2,760),"ÉCRIS",font=f0,fill=(214,212,230,int(248*b)))
    f=cond(118); txt="« RÉSINE »"
    d_.text((W//2-d_.textlength(txt,font=f)/2,838),txt,font=f,fill=VIO_CLAIR+(int(255*b),))
    c=eo(ph(t,0.80,1.15))
    if c>0:
        y=1100; lg=560
        d_.rounded_rectangle([W//2-lg/2,y,W//2+lg/2,y+112],30,fill=VIOLET+(int(252*c),))
        f2=cond(50)
        d_.text((W//2-d_.textlength("MAQUETTE GRATUITE",font=f2)/2,y+30),
                "MAQUETTE GRATUITE",font=f2,fill=BLANC+(int(255*c),))
        f3=medium(32)
        d_.text((W//2-d_.textlength("Parlons de ton projet.",font=f3)/2,y+170),
                "Parlons de ton projet.",font=f3,fill=(190,186,212,int(236*c)))
    return img

# bornes en IMAGES : 82+50+120+98+49+177+117+81 = 774
PLANS=[(82,p1),(50,p2),(120,p3),(98,p4),(49,p5),(177,p6),(117,p7),(81,p8)]

if __name__=="__main__":
    out=ICI/"frames"; out.mkdir(exist_ok=True)
    total=sum(n for n,_ in PLANS); i=0
    for n,fn in PLANS:
        d=n/FPS
        for k in range(n):
            t=k/FPS
            img = fn(t,d,k) if fn is p6 else fn(t,d)
            entete(img,t,i/total)
            img.save(out/f"f{i:04d}.png"); i+=1
        print(f"  {fn.__name__}: {n} images",flush=True)
    print(f"{i} images")
