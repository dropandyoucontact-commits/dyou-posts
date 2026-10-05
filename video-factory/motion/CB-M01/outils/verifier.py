#!/usr/bin/env python3
"""Vérifie le MP4 FINAL (pas les aperçus) : flux, durée, volume, et planches
d'images extraites du fichier exporté lui-même.

    python3 outils/verifier.py video/CB-M01.mp4 0.3 3.0 6.6 …
"""
import json, pathlib, re, subprocess, sys
from PIL import Image, ImageDraw

def main():
    mp4 = pathlib.Path(sys.argv[1]); temps = [float(x) for x in sys.argv[2:]]
    sortie = mp4.parent.parent / "verification"; sortie.mkdir(exist_ok=True)
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
                                      "-of", "json", str(mp4)], capture_output=True, text=True).stdout)
    print(json.dumps(info, ensure_ascii=False))
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    print("volume intégré", re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1], "LUFS ; crête vraie", re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1], "dBFS")
    vign = []
    for t in temps:
        f = sortie / f"mp4_{t:06.2f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", str(f)], check=True)
        vign.append((t, Image.open(f).convert("RGB").resize((270, 480), Image.LANCZOS)))
    for k in range(0, len(vign), 16):
        lot = vign[k:k + 16]; cols = 4; lig = (len(lot) + 3) // 4
        pl = Image.new("RGB", (cols * 272, lig * 482), (40, 40, 40)); d = ImageDraw.Draw(pl)
        for i, (t, im) in enumerate(lot):
            x, y = (i % cols) * 272 + 1, (i // cols) * 482 + 1
            pl.paste(im, (x, y)); d.text((x + 5, y + 4), f"{t:.2f}", fill=(255, 0, 0))
        pl.save(sortie / f"planche_mp4_{k // 16}.jpg", quality=82)
    print("planches :", sorted(p.name for p in sortie.glob("planche_mp4_*.jpg")))

if __name__ == "__main__":
    main()
