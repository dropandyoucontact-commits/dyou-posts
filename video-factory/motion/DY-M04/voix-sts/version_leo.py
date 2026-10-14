"""DY-M04 avec la voix Léo (changeur de voix ElevenLabs) : son du hook d'origine jusqu'à 0,93 s, puis Léo, bruitages par-dessus."""
import subprocess, sys, pathlib
import numpy as np
P = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(P)); sys.argv = ["x"]
import montage
def lire(f, filtre=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(f)] + (["-af", filtre] if filtre else []) + ["-ac", "1", "-ar", "48000", "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).copy()
orig = lire(P / "audio" / "voix.wav")                       # son d'origine nettoyé (hook compris)
leo = lire(P / "voix-sts" / "DY-M04-voix-leo.mp3")
n = int(18.39 * 48000); x = np.zeros(n, np.float32)
c = int(0.93 * 48000); f = int(0.04 * 48000)
x[:c] = orig[:c]; x[c - f:c] *= np.linspace(1, 0, f)
x[c:] += leo[c:n] if len(leo) >= n else np.pad(leo, (0, n - len(leo)))[c:n]
for t0, nom, g in montage.SFX:
    s = lire(P.parent / "moteur" / "sons" / f"{nom}.wav") * 10 ** (g / 20)
    i0 = int(t0 * 48000); i1 = min(n, i0 + len(s)); x[i0:i1] += s[:i1 - i0]
mix = P / "voix-sts" / "mix-leo.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", "-af",
                "volume=1.5dB,alimiter=limit=0.7:attack=1:release=50:level=false,pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", str(mix)],
               input=x.tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "renders" / "image.mp4"), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                str(P / "video" / "DY-M04-voix-leo.mp4")], check=True)
