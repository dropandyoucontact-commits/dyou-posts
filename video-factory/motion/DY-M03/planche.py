"""planche horodatée : python3 planche.py debut fin pas sortie.jpg"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
a, b, pas, out = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
src = sys.argv[5] if len(sys.argv) > 5 else "media/source.mov"
ts = list(np.arange(a, b, pas)); W, H = 400, 225; cols = 8
im = Image.new("RGB", (W * cols, H * ((len(ts) + cols - 1) // cols)))
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
for i, t in enumerate(ts):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = Image.frombytes("RGB", (W, H), raw); d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, 80, 32], fill="black"); d.text((5, 3), f"{t:.2f}", font=f, fill="yellow")
    im.paste(fr, ((i % cols) * W, (i // cols) * H))
im.save(out, quality=85)
