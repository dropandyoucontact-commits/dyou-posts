#!/usr/bin/env python3
"""Détoure une photo produit sur fond blanc pour la banque (PNG transparent, recadré).

    python3 banque_detourer.py SOURCE.jpg banque/produits/textile/nom.png [--seuil 238] [--sat 12]

Le fond est la zone presque blanche ET peu saturée reliée au bord de l'image
(composantes connexes) : un produit blanc ou crème au milieu n'est pas mangé, tant
qu'il ne touche pas le bord. Bord adouci d'un pixel, couleur décontaminée du blanc.
"""
import argparse, numpy as np, scipy.ndimage as nd
from PIL import Image, ImageFilter

def detourer(src, dst, seuil=238, sat_max=12, halo_min=241):
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    mn, mx = im.min(axis=2), im.max(axis=2)
    fondc = (mn >= seuil) & ((mx - mn) <= sat_max)
    lab, _ = nd.label(fondc)
    bord = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fond = np.isin(lab, list(bord))
    # seconde passe : halo clair laissé par l'éclairage du studio (presque blanc, un peu teinté),
    # seulement s'il touche le fond déjà trouvé
    # les ombres ajoutées par les outils de détourage des vendeurs sont des gris parfaitement
    # neutres (R = G = B), alors qu'un tissu, même gris, garde un léger écart de couleur
    halo = (((mn >= halo_min) & ((mx - mn) <= 24)) | (((mx - mn) == 0) & (mn >= 110))) & ~fond
    lab2, n2 = nd.label(halo)
    if n2:
        tailles = nd.sum(halo, lab2, range(1, n2 + 1))
        voisins = nd.binary_dilation(fond, iterations=2)
        touche = {k for k in set(np.unique(lab2[voisins & halo])) - {0} if tailles[k - 1] >= 400}
        fond |= np.isin(lab2, list(touche))
    fond = nd.binary_opening(fond, iterations=1) | (fond & ~nd.binary_dilation(~fond, iterations=2))
    a = (~fond).astype(np.float32)
    a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255
    a = np.where(fond, np.minimum(a, 0.0), a)
    aa = np.maximum(a, 1e-3)[..., None]
    rgb = np.clip((im - (1 - aa) * 255) / aa, 0, 255)
    rgb = np.where(a[..., None] > 0.98, im, rgb)
    img = Image.fromarray(np.dstack([rgb, a * 255]).astype(np.uint8), "RGBA")
    img = img.crop(img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    if max(img.size) > 1400:
        img.thumbnail((1400, 1400), Image.LANCZOS)
    img.save(dst)
    return img.size

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--seuil", type=int, default=238); p.add_argument("--sat", type=int, default=12)
    p.add_argument("--halo", type=int, default=241, help="luminance minimale du halo clair à retirer (255 = pas de seconde passe)")
    a = p.parse_args()
    print(a.dst, detourer(a.src, a.dst, a.seuil, a.sat, a.halo))
