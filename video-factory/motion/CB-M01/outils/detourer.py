#!/usr/bin/env python3
"""Détoure les trois photos produit (fond blanc uni) par composantes connexes.
Sortie : PNG RGBA recadrés au plus près, bords adoucis et décontaminés du blanc."""
import numpy as np, scipy.ndimage as nd
from PIL import Image, ImageFilter
import sys
# dossier des photos d'origine (fond blanc) : python3 outils/detourer.py DOSSIER
U = (sys.argv[1] if len(sys.argv) > 1 else "media/originaux") + "/"
SRC = {"moto": "moto.jpg", "casque": "casque.jpg", "pull": "pull.jpg"}

def detourer(nom, f, enclos=False, seuil=243, seuil_enclos=251, sat_max=255):
    im = np.asarray(Image.open(U+f).convert("RGB")).astype(np.float32)
    mn = im.min(axis=2)
    sat = im.max(axis=2) - mn
    blanc = (mn >= seuil) & (sat <= sat_max)
    lab, n = nd.label(blanc)
    bord = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fond = np.isin(lab, list(bord))
    if enclos:  # zones blanches fermées (entre les arceaux du casque)
        tb = mn >= seuil_enclos
        lab2, n2 = nd.label(tb)
        tailles = nd.sum(tb, lab2, range(1, n2+1))
        grosses = [i+1 for i, s in enumerate(tailles) if s > 300]
        fond |= np.isin(lab2, grosses)
    a = (~fond).astype(np.float32)
    # adoucir 1 px et garder un dégradé sur la transition blanc → produit
    a = np.asarray(Image.fromarray((a*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)/255
    # alpha basé aussi sur l'écart au blanc pour les bords clairs (ombre portée de la moto)
    ecart = np.clip((255-mn)/40.0, 0, 1)
    a = np.where(fond, np.minimum(a, ecart*0.0), a)
    a = np.clip(a, 0, 1)
    # décontamination : retirer le blanc mélangé aux bords
    aa = np.maximum(a, 1e-3)[..., None]
    rgb = np.clip((im - (1-aa)*255)/aa, 0, 255)
    rgb = np.where(a[..., None] > 0.98, im, rgb)
    out = np.dstack([rgb, a*255]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    bb = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    img = img.crop(bb)
    img.save(f"media/{nom}.png")
    print(nom, img.size, "fond", int(fond.sum()))

# l'ombre grise sous les roues et le halo gris autour du pull partent avec le fond :
# seuil bas, mais seulement sur des gris neutres (saturation faible) reliés au bord.
detourer("moto", SRC["moto"], enclos=True, seuil=200, sat_max=14, seuil_enclos=246)
detourer("casque", SRC["casque"], enclos=True)
detourer("pull", SRC["pull"], seuil=200, sat_max=22)

def detourer_sombre(nom, f, coeur=150, clair=215):
    """Produit sombre sur fond clair avec halo : le masque vient de la luminance,
    trous bouchés (logo crème, zip) pour garder l'intérieur."""
    im = np.asarray(Image.open(U+f).convert("RGB")).astype(np.float32)
    lum = im @ np.array([0.299, 0.587, 0.114], np.float32)
    c = nd.binary_fill_holes(nd.binary_opening(lum < coeur, iterations=1))
    lab, n = nd.label(c)
    tailles = nd.sum(c, lab, range(1, n+1))
    c = lab == (int(np.argmax(tailles)) + 1)
    c = nd.binary_fill_holes(c)
    pres = nd.binary_dilation(c, iterations=3)
    bord = np.clip((clair - lum)/(clair - coeur), 0, 1)
    a = np.where(c, 1.0, np.where(pres, bord, 0.0)).astype(np.float32)
    a = np.asarray(Image.fromarray((a*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)/255
    aa = np.maximum(a, 1e-3)[..., None]
    rgb = np.clip((im - (1-aa)*255)/aa, 0, 255)
    rgb = np.where(a[..., None] > 0.98, im, rgb)
    img = Image.fromarray(np.dstack([rgb, a*255]).astype(np.uint8), "RGBA")
    img = img.crop(img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    img.save(f"media/{nom}.png"); print(nom, img.size)

detourer_sombre("pull", SRC["pull"])
