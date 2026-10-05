#!/usr/bin/env python3
"""Fabrique la banque de bruitages DYOU par synthèse — aucun téléchargement,
aucun droit à vérifier. Sons courts, secs, sans queue de réverbération :
le contrat dit « bruitages courts sur les apparitions et transitions,
sans musique de fond »."""
import numpy as np, pathlib, wave

SR = 44100
OUT = pathlib.Path(__file__).resolve().parent.parent/"sons"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(7)

def ecrire(nom, x):
    x = np.clip(x, -1, 1)
    x = x / (np.max(np.abs(x))+1e-9) * 0.82
    # fondu de 3 ms aux deux bouts : pas de clic parasite
    n = int(SR*0.003)
    x[:n] *= np.linspace(0,1,n); x[-n:] *= np.linspace(1,0,n)
    st = (x*32767).astype(np.int16)
    with wave.open(str(OUT/nom),"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(st.tobytes())
    print(f"  {nom:<14} {len(x)/SR*1000:5.0f} ms")

def t(d): return np.linspace(0, d, int(SR*d), endpoint=False)

def passe_bas(x, a):           # un pôle, suffisant pour adoucir
    y = np.zeros_like(x); p = 0.0
    for i, v in enumerate(x):
        p += a*(v-p); y[i] = p
    return y

# --- tick : apparition d'une ligne de titre ---------------------------
d = t(0.045)
tick = (np.sin(2*np.pi*2400*d)*0.6 + rng.normal(0,0.35,len(d))) * np.exp(-d*120)
tick += np.sin(2*np.pi*5200*d)*0.25*np.exp(-d*220)
ecrire("tick.wav", tick)

# --- pop : apparition d'une carte -------------------------------------
d = t(0.11)
f = 420 + 620*(1-np.exp(-d*28))
pop = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-d*26)
pop += rng.normal(0,0.10,len(d))*np.exp(-d*90)
ecrire("pop.wav", pop)

# --- whoosh : changement de plan --------------------------------------
d = t(0.38)
bruit = rng.normal(0, 1, len(d))
env = np.sin(np.pi*np.clip(d/0.38,0,1))**1.6
whoosh = passe_bas(bruit, 0.06) * env
whoosh += passe_bas(bruit, 0.22) * env * 0.5 * np.linspace(0.2,1,len(d))
ecrire("whoosh.wav", whoosh)

# --- impact : carton final --------------------------------------------
d = t(0.42)
f = 150*np.exp(-d*9) + 42
imp = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-d*7)
imp += rng.normal(0,0.5,len(d))*np.exp(-d*85)*0.6
ecrire("impact.wav", imp)

# --- swipe : défilement dans le mockup --------------------------------
d = t(0.22)
bruit = rng.normal(0,1,len(d))
swipe = passe_bas(bruit,0.14)*np.exp(-d*11)*np.sin(np.pi*np.clip(d/0.22,0,1))
ecrire("swipe.wav", swipe)

print("\nbanque écrite dans", OUT)
