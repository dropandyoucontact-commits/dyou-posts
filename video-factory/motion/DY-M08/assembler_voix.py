"""Pose chaque phrase de Léo sur son plan (accélérée au plus ×1,2 si elle déborde de sa fenêtre) → voix/voix.wav + mots.json"""
import json, pathlib, subprocess
import numpy as np
ICI = pathlib.Path(__file__).resolve().parent
SR, DUREE = 48000, 40.6
seg = json.load(open(ICI / "segments.json"))
piste = np.zeros(int(DUREE * SR), np.float32)
mots = []
for k, (t0, t1, txt) in enumerate(seg):
    al = json.load(open(ICI / "voix" / f"seg{k:02d}.json"))
    ch, deb, fin = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    parole = fin[-1]
    f = min(1.2, max(1.0, parole / (t1 - t0)))
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(ICI / "voix" / f"seg{k:02d}.mp3"), "-af", f"atempo={f:.4f}",
                                      "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    x = x[:int((parole / f + 0.25) * SR)]
    i0 = int(t0 * SR); piste[i0:i0 + len(x)] += x[:len(piste) - i0]
    cur = None
    for c_, a in zip(ch, deb):
        if c_.isspace():
            if cur: mots.append(cur); cur = None
            continue
        if cur is None: cur = [c_, round(t0 + a / f, 3)]
        else: cur[0] += c_
    if cur: mots.append(cur)
    print(k, f"×{f:.2f}", f"{t0:.2f} → {t0 + parole / f:.2f}")
# ponctuation isolée recollée au mot d'avant
propres = []
for m, t in mots:
    if propres and all(c in "?!:;.,…" for c in m): propres[-1][0] += " " + m
    else: propres.append([m, t])
(ICI / "voix").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", str(ICI / "voix" / "voix.wav")],
               input=piste.tobytes(), check=True)
json.dump(propres, open(ICI / "mots.json", "w"), ensure_ascii=False)
print(len(propres), "mots")
