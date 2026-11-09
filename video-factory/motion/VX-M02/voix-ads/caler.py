"""Cale la voix B (Tomy, pub) sur les coupes du montage fait sur la voix A — v2, sans trou (30/10/2026).

v1 posait chaque phrase à son ancre : une phrase plus courte que sa fenêtre laissait jusqu'à 1,1 s de silence
(« quand il dit pas une goutte dehors, il y a encore un trou »). v2 : chaque phrase est ralentie d'au plus 12 %
pour remplir sa fenêtre moins une pause, et la suivante enchaîne après PAUSE secondes, en acceptant de démarrer
au plus AVANCE secondes avant sa coupe d'image. Il ne reste que des respirations de 0,2-0,3 s, comme chez le cagoulé.
Les frontières viennent de timing.json (indice du premier mot de chaque phrase)."""
import json, subprocess, pathlib
ICI = pathlib.Path(__file__).resolve().parent
ANCRES = [0.00, 4.33, 6.72, 10.66, 13.91, 17.25, 19.74]     # débuts de phrase de la voix A (v2)
DEBUTS = [0, 10, 19, 32, 45, 59, 70]                      # premier mot de chaque phrase de B (v3)
FIN = 23.68                                               # durée de l'image
PAUSE, AVANCE, RALENTI_MAX = 0.20, 0.35, 0.88
m = json.loads((ICI / "timing.json").read_text())["mots"]
src = ICI / "media" / "voix.mp3"
duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
# frontières : milieu du silence entre la fin du dernier mot d'une phrase et le début du premier de la suivante,
# puis la vraie fin de chaque phrase = fin de son dernier mot (pas le milieu du silence)
bornes = [0.0] + [(m[i - 1]["t1"] + m[i]["t0"]) / 2 for i in DEBUTS[1:]] + [duree]
fins = [m[DEBUTS[k + 1] - 1]["t1"] + 0.04 for k in range(len(DEBUTS) - 1)] + [duree]
segs = [(bornes[k], min(bornes[k + 1], fins[k])) for k in range(len(ANCRES))]
plan, t = [], 0.0
for k, (a, b) in enumerate(segs):
    brut = b - a
    fenetre = (ANCRES[k + 1] if k + 1 < len(ANCRES) else FIN - 1.4) - ANCRES[k]
    tempo = max(RALENTI_MAX, min(1.0, brut / max(0.3, fenetre - PAUSE)))     # < 1 = ralenti
    long_ = brut / tempo
    debut = max(t + PAUSE if k else 0.0, ANCRES[k] - AVANCE)
    plan.append((a, b, tempo, debut)); t = debut + long_
    print(f"phrase {k + 1}: {m[DEBUTS[k]]['w']:10s} {brut:.2f} s ×{1 / tempo:.2f} → {debut:.2f}-{t:.2f}  coupe {ANCRES[k]:.2f} (écart {debut - ANCRES[k]:+.2f}, pause avant {debut - (plan[-2][3] + (plan[-2][1] - plan[-2][0]) / plan[-2][2]) if k else 0:.2f})")
filtres, labels = [], []
for k, (a, b, tempo, debut) in enumerate(plan):
    d = int(debut * 1000)
    filtres.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,atempo={tempo:.4f},afade=t=in:d=0.008,adelay={d}|{d}[s{k}]")
    labels.append(f"[s{k}]")
graph = ";".join(filtres) + ";" + "".join(labels) + f"amix=inputs={len(plan)}:normalize=0[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-filter_complex", graph, "-map", "[out]", str(ICI / "media" / "voix-calee.mp3")], check=True)
print("→ media/voix-calee.mp3")
