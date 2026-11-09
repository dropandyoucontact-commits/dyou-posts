#!/usr/bin/env python3
"""Decoupe les plans d'AC-M09 en 1080x1920, 30 fps, sans son."""
import pathlib, subprocess, sys

SRC = {
    "logan":  ("media/logan-seg.mp4",     "crop=1920:908:0:84",  510),
    "teaser": ("media/doomsday-xmen.mp4", "crop=1920:804:0:138", 452),
    "tnga":   ("media/tng-a.mp4",         "crop=640:480:0:0",    270),
    "tngb":   ("media/tng-b.mp4",         "crop=640:480:0:0",    270),
}

# (nom, source, traitement, t_in, duree, parametre)
PLANS = [
    ("01", "logan",  "plein", 177.0, 5.00, 513),
    ("02", "logan",  "flou",  203.0, 4.00, None),
    ("03", "photo",  "photo",   0.0, 7.00, "media/photos/Patrick_Stewart_by_Gage_Skidmore.jpg"),
    ("04", "logan",  "flou",   60.0, 7.00, None),
    ("05", "photo",  "photo",   0.0, 3.50, "media/photos/Patrick_Stewart_2012.jpg"),
    ("06", "teaser", "flou",   10.0, 4.00, None),
    ("07", "photo",  "photo",   0.0, 3.30, "media/photos/Patrick_Stewart_1976.jpg"),
    ("08", "tnga",   "flou",    8.0, 5.00, None),
    ("09", "tngb",   "flou",    4.0, 4.50, None),
    ("10", "teaser", "flou",   17.8, 3.70, None),
    ("11", "logan",  "flou",  159.0, 5.70, None),
    ("12", "logan",  "plein", 101.5, 4.00, 148),
    ("13", "logan",  "plein", 186.5, 4.20, 475),
    ("14", "logan",  "flou",  119.0, 3.60, None),
    ("15", "logan",  "flou",  409.0, 5.00, None),
    ("16", "logan",  "flou",  228.5, 5.00, None),
    ("17", "teaser", "flou",   36.5, 4.00, None),
    ("18", "teaser", "flou",   41.0, 4.00, None),
    ("19", "teaser", "flou",   56.5, 2.00, None),
    ("20", "photo",  "photo",   0.0, 3.25, "media/photos/Patrick_Stewart_by_Gage_Skidmore.jpg"),
]

OUT = pathlib.Path("media/plans"); OUT.mkdir(parents=True, exist_ok=True)

def lance(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd[:6]), "...\n", r.stderr[-700:]); sys.exit(1)

for nom, src, trait, t0, dur, par in PLANS:
    dst = OUT / f"p{nom}.mp4"
    if trait == "photo":
        # panoramique tres lent, vertical : pas de zoompan (50x plus lent et illisible en poids)
        vf = ("scale=-2:2300,"
              f"crop=1080:1920:(iw-1080)/2:'min(t/{dur},1)*230',format=yuv420p")
        lance(["ffmpeg","-v","error","-loop","1","-t",f"{dur}","-i",par,"-vf",vf,
               "-r","30","-an","-c:v","libx264","-crf","20","-preset","veryfast","-y",str(dst)])
    else:
        f, lettre, larg = SRC[src]
        if trait == "plein":
            vf = f"{lettre},crop={larg}:ih:{par}:0,scale=1080:1920:flags=lanczos,format=yuv420p"
        else:
            vf = (f"{lettre},split[fg][bg];"
                  f"[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                  f"gblur=sigma=42,eq=brightness=-0.26:saturation=0.75[bgb];"
                  f"[fg]scale=1080:-2:flags=lanczos[fgs];"
                  f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2,format=yuv420p")
        lance(["ffmpeg","-v","error","-ss",f"{t0}","-t",f"{dur}","-i",f,
               "-filter_complex" if trait=="flou" else "-vf", vf,
               "-r","30","-an","-c:v","libx264","-crf","20","-preset","veryfast","-y",str(dst)])
    print(f"  p{nom}  {src:7s} {trait:5s} {t0:7.1f} +{dur:4.2f}s")
print("ok")
