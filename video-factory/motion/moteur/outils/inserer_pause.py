#!/usr/bin/env python3
"""Insère une pause dans la voix off, pour laisser parler quelqu'un d'autre (un influenceur dans le téléphone).

    python3 ../moteur/outils/inserer_pause.py --apres 62 --clip ../banque/videos/influenceurs/influ-a.mov [--marge 0.35] [--lufs -16]

Après le mot d'indice --apres (timing.json), la voix se tait le temps du clip (+ marge avant et après) et l'audio du clip
est posé dans media/voix.mp3 au même niveau que la voix (loudnorm vers --lufs, par défaut le niveau mesuré de la voix).
timing.json est décalé ; une clé "pauses" [{"t0", "t1", "clip", "apres"}] est ajoutée pour scenes.py.
La coupure tombe au milieu du VRAI silence qui suit le mot (silencedetect), jamais sur t1 de l'alignement : la fin
d'un mot alignée déborde jusqu'au début du suivant, et couper 0,12 s après tranchait le mot d'après (DY-M16/M17, 20/10/2026 :
« Et » et « Comme » coupés au début et repris à la fin). Fondus de 8 ms aux raccords.
Idempotent : repart toujours de media/voix-sans-pause.mp3 / timing-sans-pause.json (créés au premier passage).
Plusieurs pauses : relancer avec les indices de mots de la voix D'ORIGINE, tous dans la même commande (--apres 62 --clip a --apres 90 --clip b).
"""
import argparse, json, pathlib, shutil, subprocess

ICI = pathlib.Path.cwd()

def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout)

def lufs(f):
    out = subprocess.run(["ffmpeg", "-i", str(f), "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in out.splitlines() if "I:" in l][-1].split("I:")[1].split("LUFS")[0])

def silences(f, seuil=-40, mini=0.05):
    out = subprocess.run(["ffmpeg", "-i", str(f), "-af", f"silencedetect=n={seuil}dB:d={mini}", "-f", "null", "-"], capture_output=True, text=True).stderr
    deb = [float(l.split("silence_start:")[1]) for l in out.splitlines() if "silence_start:" in l]
    fin = [float(l.split("silence_end:")[1].split("|")[0]) for l in out.splitlines() if "silence_end:" in l]
    return list(zip(deb, fin))

def point_de_coupe(mot, suivant, sil):
    """milieu du silence entre la fin du mot et le début du suivant (le plus long s'il y en a plusieurs)"""
    lim1 = suivant["t0"] + 0.15 if suivant else mot["t1"] + 0.6
    cands = [(b - a, a, b) for a, b in sil if a > mot["t0"] + 0.05 and a < lim1]
    if not cands:
        raise SystemExit(f"pas de silence après « {mot.get('w', mot)} » : choisir un autre mot (--apres), fin de phrase de préférence")
    _, a, b = max(cands)
    return (a + b) / 2

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apres", type=int, action="append", required=True); p.add_argument("--clip", action="append", required=True)
    p.add_argument("--marge", type=float, default=0.35); p.add_argument("--lufs", type=float)
    a = p.parse_args()
    assert len(a.apres) == len(a.clip)
    voix0, tim0 = ICI / "media" / "voix-sans-pause.mp3", ICI / "timing-sans-pause.json"
    if not voix0.exists(): shutil.copy(ICI / "media" / "voix.mp3", voix0)
    if not tim0.exists(): shutil.copy(ICI / "timing.json", tim0)
    tim = json.load(open(tim0)); mots = tim["mots"]
    cible = a.lufs if a.lufs is not None else lufs(voix0)
    tmp = ICI / "audio"; tmp.mkdir(exist_ok=True)
    sil = silences(voix0)
    morceaux, pauses, decal, prev = [], [], 0.0, 0.0
    ordre = sorted(zip(a.apres, a.clip))
    for n, (i, clip) in enumerate(ordre):
        coupe = point_de_coupe(mots[i], mots[i + 1] if i + 1 < len(mots) else None, sil)
        print(f"coupe après « {mots[i].get('w', '')} » à {coupe:.3f} s (fin alignée {mots[i]['t1']:.3f}, mot suivant {mots[i+1]['t0'] if i + 1 < len(mots) else '-'})")
        d = duree(clip); gap = d + 2 * a.marge
        seg = tmp / f"seg{n}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voix0), "-ss", f"{prev:.3f}", "-to", f"{coupe:.3f}", "-af", "afade=t=in:d=0.008,areverse,afade=t=in:d=0.008,areverse", "-ar", "44100", "-ac", "1", str(seg)], check=True)
        cl = tmp / f"clip{n}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vn", "-af", f"loudnorm=I={cible}:TP=-1.5:LRA=9,aresample=44100,adelay={int(a.marge*1000)}|{int(a.marge*1000)},apad=pad_dur={a.marge}",
                        "-ar", "44100", "-ac", "1", str(cl)], check=True)
        morceaux += [seg, cl]
        pauses.append({"t0": round(coupe + decal, 3), "t1": round(coupe + decal + gap, 3), "clip": clip, "apres": i})
        for m in mots[i + 1:]:
            m.setdefault("_d", 0.0); m["_d"] += gap
        decal += gap; prev = coupe
    fin = tmp / "segfin.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voix0), "-ss", f"{prev:.3f}", "-af", "afade=t=in:d=0.008", "-ar", "44100", "-ac", "1", str(fin)], check=True)
    morceaux.append(fin)
    liste = tmp / "concat.txt"; liste.write_text("".join(f"file '{m.resolve()}'\n" for m in morceaux))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(liste), "-c:a", "libmp3lame", "-b:a", "192k", str(ICI / "media" / "voix.mp3")], check=True)
    for m in mots:
        d = m.pop("_d", 0.0); m["t0"] = round(m["t0"] + d, 3); m["t1"] = round(m["t1"] + d, 3)
    tim["mots"] = mots; tim["pauses"] = pauses; tim["duree_voix"] = round(duree(ICI / "media" / "voix.mp3"), 3)
    json.dump(tim, open(ICI / "timing.json", "w"), ensure_ascii=False, indent=1)
    print("pauses :", pauses, "; voix", tim["duree_voix"], "s ; clips à", round(cible, 1), "LUFS")

if __name__ == "__main__":
    main()
