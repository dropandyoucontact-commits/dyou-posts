#!/usr/bin/env python3
"""Bruitages seuls (pas de voix, pas de musique : le client pose la sienne), crête −6 dB, posés sur renders/image.mp4."""
import json, pathlib, subprocess, sys
import numpy as np
P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur" / "outils"))
import mixer
SRC, OUT = P / "renders" / "image.mp4", P / "video" / f"{P.name}.mp4"
duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)], capture_output=True, text=True).stdout)
mixer.DUREE = duree
ev = json.loads((P / "sfx.json").read_text())
bus = mixer.bus(ev); mixer.ecrire(P / "audio" / "bus.wav", bus)
g = 20 * np.log10(0.5 / (float(np.max(np.abs(bus))) or 1.0))
mix = P / "audio" / "mix.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "audio" / "bus.wav"), "-af", f"volume={g:.2f}dB,aformat=channel_layouts=stereo", "-c:a", "pcm_s16le", str(mix)], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(OUT)], check=True)
print(f"{len(ev)} bruitages, gain {g:+.1f} dB → {OUT.name} ({duree:.1f} s)")
