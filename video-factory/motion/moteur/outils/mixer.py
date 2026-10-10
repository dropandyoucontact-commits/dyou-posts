#!/usr/bin/env python3
"""Mixe les bruitages sous la voix avec FFmpeg et pose le son sur la vidéo.

La liste des bruitages n'est pas écrite à la main : edit.js l'émet (ligne
SFX_JSON de `higgsedit build`), chaque son étant déclaré à côté de l'animation
qu'il accompagne. On la range dans sfx.json, puis :

    python3 outils/mixer.py                       # → audio/mix.wav
    python3 outils/mixer.py renders/CB-M01.mp4    # → et video/CB-M01.mp4 (vidéo copiée, son AAC)

Chaîne : voix ramenée à -16 LUFS puis compressée (elle reste en avant, mots réguliers) ; bus de
bruitages compressé par la voix (sidechain : il s'efface sous chaque mot) ; somme, gain de sortie
ajusté pour que le mix final atteigne -11 LUFS, limiteur à -1 dB crête. Pas de musique de fond.

Pourquoi -11 : à -16 la voix sonnait faible sur téléphone et Youssef la remontait à la main dans
CapCut à chaque vidéo (06/10/2026). -11 LUFS / -1 dBTP est le niveau des Reels et TikTok qui
sonnent fort, sans saturer.
"""
import json, pathlib, re, subprocess, sys, wave
import numpy as np

MOTEUR = pathlib.Path(__file__).resolve().parent.parent   # sons/ fabriqués par sons.py
ICI = pathlib.Path.cwd()                                   # le projet : sfx.json, media/voix.mp3
SR = 48000
DUREE = 59.4          # remplacée par la durée de la vidéo quand on en donne une
CIBLE_LUFS = -16.0     # voix seule, avant compression
CIBLE_MIX = -11.0      # mix final


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
            cache[nom] = lire(MOTEUR / "sons" / f"{nom}.wav")
        s = cache[nom] * (10 ** (gain / 20))
        i = int(round(t * SR))
        x[i:i + len(s)] += s[: max(0, len(x) - i)]
    return x[: int(DUREE * SR)]


def mix_fort(voix, g, mix, ecart):
    """mix au-dessus de -10,5 LUFS (09/10/2026) : la voix est compressée et montée SEULE à son niveau, les
    bruitages sont posés à `ecart` LU en dessous et s'effacent sous chaque mot ; limiteur final.
    (Avant : un seul gain de sortie de +25 dB remontait aussi les bruitages, non compressés → ils couvraient la voix.)"""
    v = ICI / "audio" / "voix-traitee.wav"
    vgain = 0.0
    for _ in range(6):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voix), "-af",
                        f"aresample={SR},aformat=channel_layouts=mono,volume={g:.2f}dB,"
                        "acompressor=threshold=0.06:ratio=4:attack=4:release=110:makeup=1,"
                        f"volume={vgain:.2f}dB,alimiter=limit=0.89:attack=1.5:release=50:level=false,apad=whole_dur={DUREE}",
                        "-t", str(DUREE), "-c:a", "pcm_s16le", str(v)], check=True)
        e = CIBLE_MIX - 0.4 - loudness(v)
        if abs(e) < 0.2: break
        vgain += e
    lv = loudness(v)
    b = ICI / "audio" / "bus.wav"
    sgain = (lv - ecart) - loudness(b)
    filtre = (f"[1:a]aresample={SR},volume={sgain:.2f}dB[s];[0:a]asplit=2[v][vsc];"
              "[s][vsc]sidechaincompress=threshold=0.03:ratio=4:attack=6:release=260:makeup=1[sd];"
              "[v][sd]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:attack=2:release=60:level=false,"
              "aformat=channel_layouts=stereo[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-i", str(b), "-filter_complex", filtre, "-map", "[out]",
                    "-t", str(DUREE), "-c:a", "pcm_s16le", str(mix)], check=True)
    print(f"voix seule {lv:.1f} LUFS, bruitages {lv - ecart:.1f} LUFS ({ecart:.0f} LU dessous) ; mix {loudness(mix):.1f} LUFS → {mix.relative_to(ICI)}")


def main():
    global DUREE, CIBLE_MIX
    # options : --lufs -9 (mix final plus fort) ; --sfx -3 (bruitages baissés de 3 dB sous la voix)
    sfx_db = 0.0
    ecart = -1.0     # mode fort : bruitages 1 LU AU-DESSUS de la voix avant l'effacement sous les mots.
                     # DY-M02 (09/10/2026) validée à +1 LU dessous, mais « bruitages encore un peu trop bas » : +2 dB pour les suivantes
    args = sys.argv[1:]
    while args and args[0].startswith("--"):
        if args[0] == "--lufs": CIBLE_MIX = float(args[1])
        elif args[0] == "--sfx": sfx_db = float(args[1])
        elif args[0] == "--ecart": ecart = float(args[1])
        args = args[2:]
    sys.argv = sys.argv[:1] + args
    if len(sys.argv) > 1:
        DUREE = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", sys.argv[1]],
                                     capture_output=True, text=True).stdout.strip())
    ev = json.loads((ICI / "sfx.json").read_text())
    print(len(ev), "bruitages,", len({e[1] for e in ev}), "sons différents")
    ecrire(ICI / "audio" / "bus.wav", bus(ev))
    voix = ICI / "media" / "voix.mp3"
    g = CIBLE_LUFS - loudness(voix)
    mix = ICI / "audio" / "mix.wav"
    if CIBLE_MIX > -10.5:
        mix_fort(voix, g, mix, ecart)
        return poser(mix)
    comp_seuil, comp_ratio = 0.1, 3
    sortie_db = 4.0
    for _ in range(8):
        filtre = (f"[0:a]aresample={SR},aformat=channel_layouts=mono,volume={g:.2f}dB,"
                  f"acompressor=threshold={comp_seuil}:ratio={comp_ratio}:attack=5:release=120:makeup=1,"
                  f"apad=whole_dur={DUREE},asplit=2[v][vsc];"
                  f"[1:a]aresample={SR},volume={sfx_db:.2f}dB[s];"
                  "[s][vsc]sidechaincompress=threshold=0.03:ratio=3:attack=6:release=260:makeup=1[sd];"
                  f"[v][sd]amix=inputs=2:normalize=0:duration=first,volume={sortie_db:.2f}dB,"
                  "alimiter=limit=0.89:attack=2:release=60:level=false,"
                  "aformat=channel_layouts=stereo[out]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voix), "-i", str(ICI / "audio" / "bus.wav"),
                        "-filter_complex", filtre, "-map", "[out]", "-t", str(DUREE), "-c:a", "pcm_s16le", str(mix)], check=True)
        ecart = CIBLE_MIX - loudness(mix)
        if abs(ecart) < 0.3: break
        sortie_db += ecart
    print(f"voix +{g:.2f} dB, sortie +{sortie_db:.1f} dB ; mix {loudness(mix):.1f} LUFS → {mix.relative_to(ICI)}")
    poser(mix)


def poser(mix):
    if len(sys.argv) > 1:
        video = pathlib.Path(sys.argv[1])
        sortie = ICI / "video" / f"{ICI.name}.mp4"
        sortie.parent.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-t", str(DUREE),
                        "-movflags", "+faststart", str(sortie)], check=True)
        print("→", sortie.relative_to(ICI))


if __name__ == "__main__":
    main()
