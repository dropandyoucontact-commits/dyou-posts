#!/usr/bin/env python3
"""Détoure une photo produit sur fond blanc pour la banque (PNG transparent, recadré).

    python3 banque_detourer.py SOURCE.jpg banque/produits/textile/nom.png [--seuil 238] [--sat 12]

--trous : objet ajouré (jante à rayons, anse, cadre de vélo…) : efface aussi le blanc franc enfermé dans l'objet.
Sans cette option, le fond resté entre les rayons se voit en blanc sur un fond coloré (moto de DY-M10/M11, 17/10/2026).
Toujours vérifier le PNG sur un fond FONCÉ avant de l'utiliser. Si des taches blanches restent (petite image, rayons fins) :
rembg modèle « isnet-general-use » avec alpha matting (/usr/bin/python3, ≈ 9 s) — c'est lui qui a refait la moto de la banque.

Le fond est la zone presque blanche ET peu saturée reliée au bord de l'image
(composantes connexes) : un produit blanc ou crème au milieu n'est pas mangé, tant
qu'il ne touche pas le bord. Bord adouci d'un pixel, couleur décontaminée du blanc.
"""
import argparse, numpy as np, scipy.ndimage as nd
from PIL import Image, ImageFilter

def detourer(src, dst, seuil=238, sat_max=12, halo_min=241, trous=False):
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    mn, mx = im.min(axis=2), im.max(axis=2)
    fondc = (mn >= seuil) & ((mx - mn) <= sat_max)
    lab, _ = nd.label(fondc)
    bord = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fond = np.isin(lab, list(bord))
    if trous:
        # objets ajourés (jantes à rayons, anses, cadres) : le blanc ENFERMÉ dans l'objet est aussi du fond.
        # Seulement le blanc studio franc (≥ 246, neutre) et en zones de plus de 60 px, pour ne pas trouer un produit blanc.
        franc = (mn >= 246) & ((mx - mn) <= 8) & ~fond
        lab3, n3 = nd.label(franc)
        if n3:
            t3 = nd.sum(franc, lab3, range(1, n3 + 1))
            fond |= np.isin(lab3, [k + 1 for k in range(n3) if t3[k] >= 60])
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
    p.add_argument("--trous", action="store_true", help="objet ajouré : effacer aussi le blanc enfermé (rayons, anses)")
    a = p.parse_args()
    print(a.dst, detourer(a.src, a.dst, a.seuil, a.sat, a.halo, a.trous))
