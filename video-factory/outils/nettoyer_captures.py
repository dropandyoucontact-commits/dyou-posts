#!/usr/bin/env python3
"""Mesure la partie exploitable de chaque capture d'écran iPhone.

Un enregistrement se termine souvent sur le Centre de contrôle : l'arrière-plan
est alors FLOUTÉ, et c'est ce qui le distingue d'un simple changement de page.
On cherche donc, dans la dernière seconde et demie, une chute brutale de netteté
accompagnée d'un saut d'image, et on coupe juste avant.

    ./nettoyer_captures.py           mesure et écrit captures-communes/utiles.json
    ./nettoyer_captures.py --voir    affiche le relevé sans écrire
"""
import json, pathlib, subprocess, sys, tempfile
import numpy as np
from PIL import Image

RAC = pathlib.Path(__file__).resolve().parent.parent
CAP = RAC/"captures-communes"
FENETRE  = 4.0     # secondes examinées en fin de capture
QUEUE    = 1.6     # on ne cherche le parasite que dans cette fin-là
CHUTE    = 0.50    # netteté sous la moitié de la médiane = arrière-plan flouté
SAUT     = 20.0    # écart image-à-image qui accompagne l'ouverture de l'interface
MARGE    = 0.30    # sécurité retirée avant le point détecté

def duree(f):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",str(f)],capture_output=True,text=True).stdout.strip())

def mesurer(f):
    d = duree(f); debut = max(0.0, d-FENETRE)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg","-v","error","-ss",str(debut),"-i",str(f),
                        "-vf","scale=128:-1,fps=10","-y",f"{tmp}/%03d.png"],check=True)
        arr=[np.asarray(Image.open(p).convert("L"),dtype=np.float32)
             for p in sorted(pathlib.Path(tmp).glob("*.png"))]
    if len(arr) < 6: return d, d, "trop court"
    net = [ (np.abs(np.diff(a,axis=1)).mean()+np.abs(np.diff(a,axis=0)).mean())/2 for a in arr ]
    ecart = [float(np.abs(arr[i+1]-arr[i]).mean()) for i in range(len(arr)-1)]
    med = float(np.median(net))
    premier = max(0, len(net)-int(QUEUE*10))
    for i in range(premier, len(net)):
        saut_proche = max(ecart[max(0,i-2):i+1]) if i > 0 else 0
        if net[i] < CHUTE*med and saut_proche > SAUT:
            return d, max(1.0, round(debut + i/10 - MARGE, 2)), f"flou {net[i]:.1f} / {med:.1f}"
    return d, d, "rien à couper"

if __name__ == "__main__":
    out={}
    print(f"{'capture':<26}{'brute':>8}{'utile':>8}{'coupe':>8}   motif")
    for f in sorted(CAP.glob("site-*.mp4")):
        d,u,motif = mesurer(f)
        out[f.name]={"duree_brute":round(d,2),"duree_utile":u}
        print(f"  {f.name:<24}{d:>8.2f}{u:>8.2f}{d-u:>8.2f}   {motif}")
    if "--voir" not in sys.argv:
        (CAP/"utiles.json").write_text(json.dumps(out,ensure_ascii=False,indent=2))
        print(f"\nécrit dans {CAP/'utiles.json'}")
