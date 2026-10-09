"""images à t donnés, réduites de moitié, grille tous les 10 % (coordonnées 1920×1080 affichées)"""
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont
ts = [float(x) for x in sys.argv[2:]]; out = sys.argv[1]
W, H = 960, 540; cols = 2
im = Image.new("RGB", (W * cols, H * ((len(ts) + cols - 1) // cols)))
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
for i, t in enumerate(ts):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", "media/source.mov", "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = Image.frombytes("RGB", (W, H), raw); d = ImageDraw.Draw(fr)
    for k in range(1, 10):
        d.line([(k * 96, 0), (k * 96, H)], fill=(255, 255, 0), width=1); d.line([(0, k * 54), (W, k * 54)], fill=(255, 255, 0), width=1)
        d.text((k * 96 + 2, 2), str(k * 192), font=f, fill="yellow"); d.text((2, k * 54 + 2), str(k * 108), font=f, fill="yellow")
    d.rectangle([W - 90, H - 30, W, H], fill="black"); d.text((W - 85, H - 27), f"{t:.2f}", font=f, fill="white")
    im.paste(fr, ((i % cols) * W, (i // cols) * H))
im.save(out, quality=80)
