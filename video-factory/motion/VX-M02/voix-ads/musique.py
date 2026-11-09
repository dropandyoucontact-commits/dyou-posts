#!/usr/bin/env python3
"""Version pub : pose la musique de la banque sous le mix (voix Tomy calée + bruitages), effacée sous la voix.

Youssef, 30/10/2026 : « le son coupe » — entre deux phrases de Tomy (plus courtes que celles du cagoulé), il ne
restait que du silence numérique. Recette DY-M08 : musique à −27 LUFS, −8 dB sous la voix, fondu de fin ;
mix final ramené à −13 LUFS / −1 dB crête. Entrée video/VX-M02-pub.mp4 → video/VX-M02-pub.mp4 (sauvegarde -sans-musique)."""
import pathlib, re, shutil, subprocess, sys
P = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
SRC = P / "video" / "VX-M02-pub.mp4"           # argument facultatif : dossier du projet (VX-M02-pub depuis le 30/10)
SAUV = P / "video" / "VX-M02-pub-sans-musique.mp4"
MUS = P.parent / "banque" / "musiques" / "vlog-trap-afro-40s.mp3"
if not SAUV.exists(): shutil.copy(SRC, SAUV)

def lufs(f, extra=()):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(f), *extra, "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])

duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SAUV)], capture_output=True, text=True).stdout)
g_mus = -27.0 - lufs(MUS)
graph = (f"[1:a]aresample=48000,volume={g_mus:.2f}dB,atrim=0:{duree:.3f},afade=t=in:d=0.4,afade=t=out:st={duree - 1.6:.3f}:d=1.6[m];"
         "[0:a]aresample=48000,asplit=2[v][k];"
         "[m][k]sidechaincompress=threshold=0.03:ratio=1.6:attack=25:release=420:makeup=1[md];"
         "[v][md]amix=inputs=2:normalize=0:duration=first[mx]")
tmp = P / "audio" / "pub-musique.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SAUV), "-i", str(MUS), "-filter_complex", graph, "-map", "[mx]", "-c:a", "pcm_s16le", str(tmp)], check=True)
corr = -13.0 - lufs(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SAUV), "-i", str(tmp), "-map", "0:v", "-map", "1:a",
                "-af", f"volume={corr:.2f}dB,alimiter=limit=0.89:attack=1.5:release=50:level=false", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(SRC)], check=True)
print(f"musique {g_mus:+.1f} dB, correction finale {corr:+.1f} dB → {SRC.name} : {lufs(SRC):.1f} LUFS")
