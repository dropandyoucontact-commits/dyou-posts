#!/usr/bin/env python3
"""Simule l'affichage TikTok sur un iPhone 13 (écran 19,5:9) au-dessus d'images 1080×1920.

    python3 zone_tiktok.py image1.png [image2.png …] -o planche.jpg

Mesuré sur une capture de Youssef (17/10/2026) : TikTok remplit la hauteur, donc la vidéo 9:16 est rognée de ~96 px
à gauche et à droite ; la barre de recherche couvre y 115-197, la colonne de boutons x 860-965 de y 816 à 1555,
la légende y 1555-1766, la barre de commentaire en dessous. Ce qui touche une zone rouge sera caché ou rogné.
Snapchat (pubs) laisse libres les 150 px du haut et ~340 px du bas : la même zone sûre convient aux deux.
"""
import argparse
from PIL import Image, ImageDraw

ROGNE = 96
ZONES = [(0, 0, 1080, 205), (860, 816, 1080, 1555), (0, 1555, 1080, 1920)]   # en pixels de la vidéo


def simule(chemin):
    im = Image.open(chemin).convert("RGB").resize((1080, 1920))
    voile = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(voile)
    for z in ZONES: d.rectangle(z, fill=(255, 0, 60, 70), outline=(255, 0, 60, 255), width=3)
    im = Image.alpha_composite(im.convert("RGBA"), voile).convert("RGB")
    return im.crop((ROGNE, 0, 1080 - ROGNE, 1920))


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("images", nargs="+"); a.add_argument("-o", default="zone-tiktok.jpg")
    a.add_argument("--haut", type=int, default=640)
    x = a.parse_args()
    ims = [simule(p) for p in x.images]
    ims = [i.resize((int(i.width * x.haut / i.height), x.haut)) for i in ims]
    P = Image.new("RGB", (sum(i.width for i in ims) + 10 * (len(ims) - 1), x.haut), "white")
    o = 0
    for i in ims: P.paste(i, (o, 0)); o += i.width + 10
    P.save(x.o, quality=85); print(x.o)
