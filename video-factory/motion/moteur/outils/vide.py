#!/usr/bin/env python3
"""Règle « jamais de vide » : repère les moments où la zone centrale de l'écran est presque vide.

    cd video-factory/motion/MON-ID
    python3 ../moteur/outils/vide.py [pas_s=0.1] [bande_px=300]

Rend une image toutes les `pas_s` secondes (sans flou) et la compare à un fond de référence (fond à points
+ éclairs, sans aucune scène). Dans la zone 60 ≤ x ≤ 1020, 640 ≤ y ≤ 1440, une ligne de pixels « contient
quelque chose » si au moins 7 pixels diffèrent du fond ; on cherche la plus grande bande de lignes vides
consécutives. Une plage où cette bande dépasse `bande_px` pendant au moins 0,3 s est signalée. Les
sous-titres (au-dessus de y = 640) ne comptent pas : c'est le visuel qui doit occuper l'écran.
"""
import sys, pathlib
import numpy as np
ICI = pathlib.Path.cwd()
sys.path.insert(0, str(ICI)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import moteur, scenes

Y0, Y1, X0, X1 = 640, 1440, 60, 1020

def fond_reference(t):
    s = moteur.surface(); c = s.getCanvas()
    scenes.fond(c, t)
    if hasattr(scenes, "K"): scenes.K.dessine_eclairs(c, t)
    return s.toarray()[Y0:Y1, X0:X1, :3].astype(np.int16)

def plus_grande_bande(vide_ligne):
    best = cur = 0
    for v in vide_ligne:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best

def main():
    pas = float(sys.argv[1]) if len(sys.argv) > 1 else 0.1
    seuil = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    ts = np.arange(0.0, scenes.DUREE - 0.05, pas)
    bandes, couv = [], []
    for t in ts:
        a = moteur.image_rgba(scenes.dessine, float(t), 1)[Y0:Y1, X0:X1, :3].astype(np.int16)
        diff = np.abs(a - fond_reference(float(t))).sum(axis=2) > 18
        lignes_vides = diff.sum(axis=1) < 7
        bandes.append(plus_grande_bande(lignes_vides)); couv.append(diff.mean())
    bandes, couv = np.array(bandes), np.array(couv)
    print(f"couverture moyenne {couv.mean():.0%} ; plus grande bande vide : {bandes.max()} px à {ts[bandes.argmax()]:.1f} s")
    deb, trous = None, []
    for k, b in enumerate(bandes > seuil):
        if b and deb is None: deb = k
        if (not b or k == len(bandes) - 1) and deb is not None:
            fin = k if not b else k + 1
            if (fin - deb) * pas >= 0.3 - 1e-9: trous.append((ts[deb], ts[fin - 1] + pas, int(bandes[deb:fin].max())))
            deb = None
    if not trous: print(f"aucun vide (bande ≤ {seuil} px)")
    for a, b, m in trous: print(f"VIDE de {a:.1f} s à {b:.1f} s (bande vide jusqu'à {m} px)")
    return 1 if trous else 0

if __name__ == "__main__":
    sys.exit(main())
