"""Attaque du hook rapide et forte (règle de Youssef, 19/10/2026) : les premiers mots de Tomy ne sortent jamais lents.
Après voix.py (qui a déjà resserré les pauses), sur la PREMIÈRE PHRASE seulement :
  - les silences internes passent à --pause (0,05 s : la virgule d'attaque ne fait plus de trou),
  - la phrase est accélérée si son débit est sous --debit (5,2 mots/s par défaut, plafond ×1,25),
  - elle prend --gain dB (attaque plus forte que le reste ; mixer.py compresse ensuite).
Le reste de la voix n'est pas touché ; timing.json est décalé en conséquence.

    lancé tout seul par voix.py (sauf --sans-hook) ; à la main, une seule fois après voix.py (sinon il s'applique deux fois)
    python3 ../moteur/outils/hook_rapide.py --mots 9    # longueur du hook en mots, si la 1re phrase est trop longue
"""
import argparse, json, pathlib, re, subprocess

ICI = pathlib.Path.cwd()


def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def silences(f, t1, seuil, d):
    r = subprocess.run(["ffmpeg", "-i", str(f), "-t", f"{t1:.3f}", "-af", f"silencedetect=noise={seuil}:d={d}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)], [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--debit", type=float, default=5.2); p.add_argument("--pause", type=float, default=0.05)
    p.add_argument("--gain", type=float, default=1.5); p.add_argument("--mots", type=int, default=0)
    p.add_argument("--seuil", default="-38dB")
    a = p.parse_args()
    voix = ICI / "media" / "voix.mp3"
    tj = json.loads((ICI / "timing.json").read_text())
    mots = tj["mots"]
    n = a.mots or next(i + 1 for i, m in enumerate(mots) if re.search(r"[.?!…]\s*$", m["w"]))
    # fin du hook = milieu du silence qui suit le dernier mot (ou sa fin si la voix enchaîne)
    fin_mot = mots[n - 1]["t1"]; suivant = mots[n]["t0"] if n < len(mots) else duree(voix)
    sil = [s for s in silences(voix, suivant + 0.3, a.seuil, 0.03) if s[1] > fin_mot - 0.05]
    H = (sil[0][0] + 0.02) if sil and sil[0][0] < suivant + 0.1 else fin_mot
    internes = [(s0, s1) for s0, s1 in silences(voix, H, a.seuil, a.pause + 0.02) if s0 > 0.05 and s1 < H - 0.01]
    coupes = []
    for s0, s1 in internes:
        r = (s1 - s0) - a.pause; m = (s0 + s1) / 2
        coupes.append((m - r / 2, m + r / 2))
    garde, t = [], 0.0
    for c0, c1 in coupes: garde.append((t, c0)); t = c1
    garde.append((t, H))
    duree_h = sum(g1 - g0 for g0, g1 in garde)
    f = max(1.0, min(1.25, a.debit / (n / max(0.1, duree_h))))
    sauve = ICI / "media" / "voix-avant-hook.mp3"
    sauve.write_bytes(voix.read_bytes())          # voix.py vient de réécrire voix.mp3 : ne pas relancer deux fois de suite
    src = str(sauve)
    filt = "".join(f"[0:a]atrim={g0:.4f}:{g1:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={max(0, g1 - g0 - 0.005):.4f}:d=0.005[h{k}];"
                   for k, (g0, g1) in enumerate(garde))
    filt += "".join(f"[h{k}]" for k in range(len(garde))) + f"concat=n={len(garde)}:v=0:a=1,atempo={f:.4f},volume={a.gain}dB[h];"
    filt += f"[0:a]atrim=start={H:.4f},asetpts=PTS-STARTPTS[r];[h][r]concat=n=2:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", filt, "-map", "[o]",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", str(voix)], check=True)

    def dans_hook(x):
        x = min(x, H)
        return (x - sum(min(c1, max(c0, x)) - c0 for c0, c1 in coupes)) / f

    nouv_h = dans_hook(H)
    for m in tj["mots"]:
        for k in ("t0", "t1"):
            x = m[k]
            m[k] = round(dans_hook(x) if x <= H else nouv_h + (x - H), 3)
    tj["duree_voix"] = round(duree(voix), 3); tj["hook_rapide"] = {"mots": n, "tempo": round(f, 3), "gain_db": a.gain}
    (ICI / "timing.json").write_text(json.dumps(tj, ensure_ascii=False, indent=1))
    print(f"hook : {n} mots, {duree_h:.2f} s sans trous → ×{f:.3f} = {n / (duree_h / f):.2f} mots/s, +{a.gain} dB ; "
          f"{H - nouv_h:.2f} s gagnées ; voix {tj['duree_voix']:.2f} s")


if __name__ == "__main__":
    main()
