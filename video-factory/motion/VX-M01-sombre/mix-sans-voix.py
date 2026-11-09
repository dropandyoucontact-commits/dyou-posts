#!/usr/bin/env python3
"""Mix sans voix ni musique (Youssef, 30/10 : le client ajoute sa musique s'il veut) : bus de bruitages seul, crête −6 dB, posé sur renders/image.mp4.
    /usr/bin/python3 mix-sans-voix.py            → audio/mix.wav + video/<projet>.mp4"""
import json, pathlib, re, subprocess, sys
P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur" / "outils"))
import mixer
SRC = P / "renders" / "image.mp4"
MUS = P.parent / "banque" / "musiques" / "vlog-trap-afro-40s.mp3"
OUT = P / "video" / f"{P.name}.mp4"
duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)], capture_output=True, text=True).stdout)
mixer.DUREE = duree
ev = json.loads((P / "sfx.json").read_text())
mixer.ecrire(P / "audio" / "bus.wav", mixer.bus(ev))
print(len(ev), "bruitages ;", f"{duree:.2f} s")

import numpy as np
bus = mixer.lire(P / "audio" / "bus.wav")
pic = float(np.max(np.abs(bus))) or 1.0
g = 20 * np.log10(0.5 / pic)                      # crête à −6 dBFS : discret, lisible, de la place pour la musique du client
mix = P / "audio" / "mix.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "audio" / "bus.wav"), "-af", f"volume={g:.2f}dB,aformat=channel_layouts=stereo", "-c:a", "pcm_s16le", str(mix)], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(OUT)], check=True)
print(f"bruitages seuls, gain {g:+.1f} dB → {OUT.name}")
