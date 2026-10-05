#!/usr/bin/env python3
"""Mixe les bruitages sous la voix avec FFmpeg et pose le son sur la vidéo.

La liste des bruitages n'est pas écrite à la main : edit.js l'émet (ligne
SFX_JSON de `higgsedit build`), chaque son étant déclaré à côté de l'animation
qu'il accompagne. On la range dans sfx.json, puis :

    python3 outils/mixer.py                       # → audio/mix.wav
    python3 outils/mixer.py renders/CB-M01.mp4    # → et video/CB-M01.mp4 (vidéo copiée, son AAC)

Chaîne : voix ramenée à -16 LUFS (gain fixe, pas de compression) ; bus de
bruitages compressé par la voix (sidechain : il s'efface sous chaque mot) ;
somme, limiteur à 0,95. Pas de musique de fond.
"""
import json, pathlib, re, subprocess, sys, wave
import numpy as np

ICI = pathlib.Path(__file__).resolve().parent.parent
SR = 48000
DUREE = 59.4
CIBLE_LUFS = -16.0


def lire(chemin):
    with wave.open(str(chemin)) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def ecrire(chemin, x):
    chemin.parent.mkdir(exist_ok=True)
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())


def loudness(chemin):
    sortie = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(chemin), "-af", "ebur128", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", sortie)[-1])


def bus(evenements):
    x = np.zeros(int(DUREE * SR) + SR, np.float32)
    cache = {}
    for t, nom, gain in evenements:
        if nom not in cache:
            cache[nom] = lire(ICI / "sons" / f"{nom}.wav")
        s = cache[nom] * (10 ** (gain / 20))
        i = int(round(t * SR))
        x[i:i + len(s)] += s[: max(0, len(x) - i)]
    return x[: int(DUREE * SR)]


def main():
    ev = json.loads((ICI / "sfx.json").read_text())
    print(len(ev), "bruitages,", len({e[1] for e in ev}), "sons différents")
    ecrire(ICI / "audio" / "bus.wav", bus(ev))
    voix = ICI / "media" / "voix.mp3"
    g = CIBLE_LUFS - loudness(voix)
    filtre = (f"[0:a]aresample={SR},aformat=channel_layouts=mono,volume={g:.2f}dB,apad=whole_dur={DUREE},asplit=2[v][vsc];"
              f"[1:a]aresample={SR}[s];"
              "[s][vsc]sidechaincompress=threshold=0.03:ratio=3:attack=6:release=260:makeup=1[sd];"
              "[v][sd]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95:level=false,"
              "aformat=channel_layouts=stereo[out]")
    mix = ICI / "audio" / "mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voix), "-i", str(ICI / "audio" / "bus.wav"),
                    "-filter_complex", filtre, "-map", "[out]", "-t", str(DUREE), "-c:a", "pcm_s16le", str(mix)], check=True)
    print(f"voix +{g:.2f} dB ; mix {loudness(mix):.1f} LUFS → {mix.relative_to(ICI)}")
    if len(sys.argv) > 1:
        video = pathlib.Path(sys.argv[1])
        sortie = ICI / "video" / "CB-M01.mp4"
        sortie.parent.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-t", str(DUREE),
                        "-movflags", "+faststart", str(sortie)], check=True)
        print("→", sortie.relative_to(ICI))


if __name__ == "__main__":
    main()
