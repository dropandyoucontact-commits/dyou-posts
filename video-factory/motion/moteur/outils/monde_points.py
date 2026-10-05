#!/usr/bin/env python3
"""Fabrique media/monde-points.json : les terres émergées en points régulièrement espacés
(grille adaptée à la latitude, ~1,5°), pour le globe en points du kit.

Source : Natural Earth 1:110m, pays (domaine public), github.com/nvkelso/natural-earth-vector.
Chaque point porte une étiquette : 0 terre, 1 Chine, 2 Thaïlande, 3 France, 4 reste de l'Europe.

    python3 outils/monde_points.py
"""
import json, math, pathlib, urllib.request
import numpy as np
from PIL import Image, ImageDraw

ICI = pathlib.Path(__file__).resolve().parent.parent
URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
SRC = pathlib.Path("/tmp/ne110.geojson")
PAS = 1.5
LARG, HAUT = 2880, 1440

def anneaux(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [p[0] for p in polys]

def masque(features):
    im = Image.new("L", (LARG, HAUT), 0); d = ImageDraw.Draw(im)
    for f in features:
        for ring in anneaux(f["geometry"]):
            pts = [((lo + 180) / 360 * LARG, (90 - la) / 180 * HAUT) for lo, la in ring]
            if len(pts) > 2: d.polygon(pts, fill=255)
    return np.asarray(im) > 0

def main():
    if not SRC.exists(): SRC.write_bytes(urllib.request.urlopen(URL, timeout=60).read())
    feats = json.loads(SRC.read_text())["features"]
    pays = lambda a3: [f for f in feats if f["properties"].get("ADM0_A3") == a3 or f["properties"].get("ISO_A3") == a3]
    terre = masque(feats)
    chine, thai, fra = masque(pays("CHN")), masque(pays("THA")), masque(pays("FRA"))
    europe = masque([f for f in feats if f["properties"].get("CONTINENT") == "Europe"])
    lon, lat, tag = [], [], []
    la = -84.0
    while la <= 84.0:
        n = max(1, round(360 * math.cos(math.radians(la)) / PAS))
        for i in range(n):
            lo = -180 + (i + 0.5) * 360 / n
            x = min(LARG - 1, int((lo + 180) / 360 * LARG)); y = min(HAUT - 1, int((90 - la) / 180 * HAUT))
            if terre[y, x]:
                lon.append(round(lo, 2)); lat.append(round(la, 2))
                tag.append(1 if chine[y, x] else 2 if thai[y, x] else 3 if fra[y, x] else 4 if europe[y, x] else 0)
        la += PAS
    (ICI / "media" / "monde-points.json").write_text(json.dumps({"lon": lon, "lat": lat, "tag": tag}))
    print(len(lon), "points ;", {k: tag.count(k) for k in sorted(set(tag))})

if __name__ == "__main__":
    main()
