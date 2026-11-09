# -*- coding: utf-8 -*-
import subprocess, sys, math, numpy as np, skia
sys.path.insert(0, '/private/tmp/claude-501/-Users-mohamedelhadad/e3c20a03-d971-41a8-b383-0aecc512e06d/scratchpad/leo-benef')
from verre import fenetre, texte, larg, GROS, PETIT, ENCRE, GRIS, borne, ressort, douce, mixe

D = '/private/tmp/claude-501/-Users-mohamedelhadad/e3c20a03-d971-41a8-b383-0aecc512e06d/scratchpad/leo-benef/'
RUSH, SON = D + 'rush.mp4', D + 'voix-13.wav'
OUT = '/Users/mohamedelhadad/Movies/edits/leo-benefices-cartons-v2.mp4'
W, H, FPS = 720, 1280, 24
NB = 481

DROITE, HAUT = 672, 186          # zone sure : 48 px du bord droit, loin du bas TikTok
T_ENT, T_SOR = 0.28, 0.20
TAI_M, TAI_L = 56, 19            # montant, etiquette

# mot du prix -> fenetre ; cale sur les timings scribe du fichier livre
CARTES = [
    dict(montant='20 000 €',  label='DE BÉNÉFICES',   t0=0.35, t1=1.75),
    dict(montant='600 €',     label='PETITS CARTONS', t0=2.80, t1=4.25),
    dict(montant='1 300 €',   label='GRANDS CARTONS', t0=5.55, t1=6.85),
    dict(montant='1 000 €',   label='CEUX-LÀ',        t0=7.52, t1=8.45),
]
for k in CARTES:
    wm = larg(k['montant'], TAI_M, GROS)
    wl = larg(k['label'], TAI_L, PETIT, 0.12)
    k['w'] = max(wm, wl) + 54
    k['h'] = 122

lire = subprocess.Popen(['ffmpeg','-v','error','-i',RUSH,'-f','rawvideo','-pix_fmt','rgb24','-'],
                        stdout=subprocess.PIPE)
ecrire = subprocess.Popen(
    ['ffmpeg','-y','-v','error',
     '-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
     '-i',SON,'-map','0:v:0','-map','1:a:0',
     '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p',
     '-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart', OUT],
    stdin=subprocess.PIPE)

info = skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kUnpremul_AlphaType)
n = 0
while True:
    brut = lire.stdout.read(W * H * 3)
    if len(brut) < W * H * 3: break
    t = n / FPS
    actives = [k for k in CARTES if k['t0'] - 0.02 <= t <= k['t1'] + T_SOR]
    if not actives:
        ecrire.stdin.write(brut); n += 1; continue
    rgb = np.frombuffer(brut, np.uint8).reshape(H, W, 3)
    rgba = np.dstack([rgb, np.full((H, W, 1), 255, np.uint8)])
    surf = skia.Surface(W, H)
    with surf as c:
        fond = skia.Image.fromarray(rgba, skia.kRGBA_8888_ColorType)
        c.drawImage(fond, 0, 0)
        for k in actives:
            ent = borne((t - k['t0']) / T_ENT)
            sor = borne((t - k['t1']) / T_SOR)
            if sor >= 1: continue
            e = ressort(ent, 1.12, 5.0)
            s = mixe(0.84, 1.0, min(e, 1.08)) * mixe(1.0, 1.045, douce(sor))
            a = borne(ent * 3.2) * (1 - douce(sor))
            dy = mixe(-16, 0, borne(e))
            w, h = k['w'], k['h']
            cx, cy = DROITE - w / 2, HAUT + h / 2 + dy
            c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy)
            x, y = cx - w / 2, cy - h / 2
            fenetre(c, fond, x, y, w, h, 30, ent if ent < 1 else 1.0, a)
            c.saveLayerAlpha(None, int(255 * borne(a)))
            texte(c, k['label'], x + 27, y + 42, TAI_L, GRIS, PETIT, 'gauche', 0.12)
            texte(c, k['montant'], x + 27, y + 96, TAI_M, ENCRE, GROS)
            c.restore()
            c.restore()
    img = surf.makeImageSnapshot().convert(alphaType=skia.kUnpremul_AlphaType)
    ecrire.stdin.write(img.tobytes()[:, :, :3].tobytes() if False else
                       np.array(img)[:, :, :3].tobytes())
    n += 1
ecrire.stdin.close(); ecrire.wait(); lire.wait()
print('images', n, '->', OUT)
