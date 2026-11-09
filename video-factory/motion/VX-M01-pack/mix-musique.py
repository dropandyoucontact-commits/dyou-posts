#!/usr/bin/env python3
"""Musique de fond seule (Youssef, 30/10 : « juste une musique de fond », aucun bruitage) : −16 LUFS, fondu d'entrée 0,5 s et
de sortie 2 s, crête −1 dB, posée sur renders/image.mp4 → video/<projet>.mp4"""
import pathlib, re, subprocess, sys
P = pathlib.Path(__file__).resolve().parent
SRC, OUT = P / "renders" / "image.mp4", P / "video" / f"{P.name}.mp4"
MUS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else P.parent / "banque" / "musiques" / "vlog-trap-afro-40s.mp3"
def lufs(f):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(f), "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)], capture_output=True, text=True).stdout)
g = -16.0 - lufs(MUS)
mix = P / "audio" / "mix.wav"; mix.parent.mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(MUS), "-af", f"aresample=48000,volume={g:.2f}dB,atrim=0:{d:.3f},afade=t=in:d=0.5,afade=t=out:st={d-2.0:.3f}:d=2.0,alimiter=limit=0.89:attack=1.5:release=50:level=false,aformat=channel_layouts=stereo", "-c:a", "pcm_s16le", str(mix)], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{d:.3f}", "-movflags", "+faststart", str(OUT)], check=True)
print(f"musique {MUS.name} {g:+.1f} dB → {OUT.name} : {lufs(OUT):.1f} LUFS")
