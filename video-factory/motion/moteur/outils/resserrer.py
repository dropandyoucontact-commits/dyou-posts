"""Resserre les pauses de la voix (15/10/2026) : chaque silence plus long que --pause est ramené à --pause, comme la
prise anglaise de DA-M07-169-EN (pauses ≤ 0,2 s) que Youssef veut comme rythme. Décale timing.json en conséquence.

    python3 ../moteur/outils/resserrer.py              # depuis le dossier de la vidéo, après voix.py
    python3 ../moteur/outils/resserrer.py --pause 0.16

Les silences viennent de l'audio lui-même (silencedetect), pas de l'alignement : on ne coupe jamais une fin de mot.
À relancer après chaque voix.py (qui réécrit voix.mp3 et timing.json).
"""
import argparse, json, pathlib, re, subprocess

ICI = pathlib.Path.cwd()


def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pause", type=float, default=0.18, help="durée maximale d'un silence, en secondes")
    p.add_argument("--seuil", default="-38dB")
    a = p.parse_args()
    voix = ICI / "media" / "voix.mp3"
    r = subprocess.run(["ffmpeg", "-i", str(voix), "-af", f"silencedetect=noise={a.seuil}:d={a.pause + 0.02}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    debuts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    fins = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    D = duree(voix)
    coupes = []                                  # (début, fin) des morceaux retirés
    for s0, s1 in zip(debuts, fins):
        if s0 < 0.05 or s1 > D - 0.05: continue   # ni le silence d'attaque ni celui de fin
        retire = (s1 - s0) - a.pause
        if retire > 0.02:
            m = (s0 + s1) / 2
            coupes.append((m - retire / 2, m + retire / 2))
    if not coupes:
        print("aucune pause à resserrer"); return
    garde, t = [], 0.0
    for c0, c1 in coupes:
        garde.append((t, c0)); t = c1
    garde.append((t, D))
    sauve = ICI / "media" / "voix-avant-resserrer.mp3"
    sauve.write_bytes(voix.read_bytes())
    filt = "".join(f"[0:a]atrim={g0:.4f}:{g1:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.006,afade=t=out:st={max(0, g1 - g0 - 0.006):.4f}:d=0.006[a{k}];"
                   for k, (g0, g1) in enumerate(garde))
    filt += "".join(f"[a{k}]" for k in range(len(garde))) + f"concat=n={len(garde)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(sauve), "-filter_complex", filt, "-map", "[o]",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", str(voix)], check=True)

    def decale(x):
        return x - sum(min(c1, max(c0, x)) - c0 for c0, c1 in coupes)

    tj = json.loads((ICI / "timing.json").read_text())
    for m in tj["mots"]:
        m["t0"], m["t1"] = round(decale(m["t0"]), 3), round(decale(m["t1"]), 3)
    tj["duree_voix"] = round(duree(voix), 3)
    tj["pauses_resserrees"] = a.pause
    (ICI / "timing.json").write_text(json.dumps(tj, ensure_ascii=False, indent=1))
    mo = tj["mots"]
    print(f"{len(coupes)} pauses resserrées, {sum(c1 - c0 for c0, c1 in coupes):.2f} s retirées ; voix {tj['duree_voix']:.2f} s ; "
          f"{len(mo) / (mo[-1]['t1'] - mo[0]['t0']):.2f} mots/s")
    print(" ".join(f"{m['i']}:{m['w']}@{m['t0']:.2f}" for m in mo))


if __name__ == "__main__":
    main()
