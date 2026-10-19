"""Enchaîne les phrases de la voix « Avital vlog » comme un vrai vlog (débit continu, réf. reference/vlog.mov ≈ 3,8 mots/s) :
dans chaque phrase les silences de plus de PAUSE s sont ramenés à PAUSE, la phrase est légèrement accélérée (TEMPO),
puis les phrases sont posées bout à bout avec ECART s entre elles (ECARTS pour les exceptions).
→ voix/voix.wav, mots.json, et les temps [début, fin] réécrits dans segments.json (le montage s'en sert)."""
import json, pathlib, subprocess
import numpy as np
ICI = pathlib.Path(__file__).resolve().parent
SR = 48000
PAUSE, TEMPO, ECART = 0.18, 1.1, 0.2
ECARTS = {1: 0.12, 2: 0.2, 3: 0.55}            # avant la phrase k : hook serré, puis la place du titre « En Chine »
DEBUT = 0.1

seg = json.load(open(ICI / "segments.json"))


def lire(f, tempo=1.0):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-af", f"atempo={tempo:.4f}", "-ac", "1", "-ar", str(SR),
                                         "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()


def resserre(x):
    """retire l'excédent des silences internes ; renvoie (x resserré, fonction temps ancien → nouveau)"""
    win = int(0.01 * SR)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, mode="same"))
    muet = rms < 10 ** (-42 / 20)
    coupes, i, n = [], 0, len(x)
    while i < n:
        if muet[i]:
            j = i
            while j < n and muet[j]: j += 1
            if i > 0 and j < n and (j - i) / SR > PAUSE:
                exc = (j - i) - int(PAUSE * SR); m = (i + j) // 2
                coupes.append((m - exc // 2, m - exc // 2 + exc))
            i = j
        else: i += 1
    garde, prec = [], 0
    for a, b in coupes: garde.append(x[prec:a]); prec = b
    garde.append(x[prec:])

    def carte(t):
        s = int(t * SR); retire = sum(min(b, max(a, s)) - a for a, b in coupes)
        return (s - retire) / SR
    return np.concatenate(garde), carte


morceaux, mots, t = [], [], DEBUT
for k, (_, _, txt) in enumerate(seg):
    t += ECARTS.get(k, ECART) if k else 0
    al = json.load(open(ICI / "voix" / f"seg{k:02d}.json"))
    x, carte = resserre(lire(ICI / "voix" / f"seg{k:02d}.mp3"))
    x = x[:int((carte(al["character_end_times_seconds"][-1]) + 0.12) * SR)]
    tmp = ICI / "voix" / "tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(tmp)], input=x.tobytes(), check=True)
    x = lire(tmp, TEMPO)
    morceaux.append((t, x))
    cur = None
    for c_, a in zip(al["characters"], al["character_start_times_seconds"]):
        if c_.isspace():
            if cur: mots.append(cur); cur = None
            continue
        if cur is None: cur = [c_, round(t + carte(a) / TEMPO, 3)]
        else: cur[0] += c_
    if cur: mots.append(cur)
    fin = t + len(x) / SR - 0.1
    seg[k][0], seg[k][1] = round(t, 3), round(fin, 3)
    print(k, f"{t:.2f} → {fin:.2f}")
    t = fin

piste = np.zeros(int((t + 4) * SR), np.float32)
for t0, x in morceaux:
    i0 = int(t0 * SR); piste[i0:i0 + len(x)] += x
propres = []
for m, tm in mots:                                   # ponctuation isolée recollée au mot d'avant
    if propres and all(c in "?!:;.,…" for c in m): propres[-1][0] += " " + m
    else: propres.append([m, tm])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", str(ICI / "voix" / "voix.wav")],
               input=piste.tobytes(), check=True)
json.dump(propres, open(ICI / "mots.json", "w"), ensure_ascii=False)
json.dump(seg, open(ICI / "segments.json", "w"), ensure_ascii=False, indent=0)
print(len(propres), "mots ;", f"fin de la voix {t:.2f} s ; {len(propres) / (t - DEBUT):.2f} mots/s")
