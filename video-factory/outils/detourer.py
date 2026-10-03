#!/usr/bin/env python3
"""Détoure les photos produit de la banque DROP&YOU et écarte les mauvaises.

La banque est hétérogène : certaines photos sont sur fond blanc de studio,
d'autres sur une table ou une moquette. On ne fixe donc pas un seuil absolu.

Le fond est retiré par propagation depuis le cadre, de proche en proche : un
pixel rejoint le fond si l'écart avec son voisin déjà classé fond est faible.
Un seuil global ne suffisait pas — sous un sac, le socle du studio est séparé
du cadre par une ombre portée, donc il restait collé au produit. La propagation
locale, elle, traverse le dégradé de l'ombre et s'arrête sur l'arête nette du
produit. Une photo dont le cadre n'est pas uni est rejetée : il y a 2 035
produits dans la banque, inutile d'en rafistoler un.
"""
import json, pathlib
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

PAS = 10          # écart maximal avec le voisin déjà classé fond
SOL = 165         # on ne descend pas sous cette luminance
POCHE = 0.15      # aire max d'une poche de fond enfermée dans le produit
SALE = 0.04       # part de fond résiduel au-delà de laquelle on rejette
CADRE_UNI = 10.0  # écart-type max sur le cadre pour un fond de studio


def _cadre(a, e=6):
    return np.concatenate([a[:e].reshape(-1, 3), a[-e:].reshape(-1, 3),
                           a[:, :e].reshape(-1, 3), a[:, -e:].reshape(-1, 3)])


def _propager(g, depart, pas=PAS, sol=SOL):
    """Étend `depart` aux voisins dont la valeur est proche, sans descendre sous `sol`."""
    fond = depart.copy()
    val = np.where(fond, g, np.nan)
    for _ in range(400):
        ajout = np.zeros_like(fond)
        for ax, sens in ((0, 1), (0, -1), (1, 1), (1, -1)):
            ref = np.roll(val, sens, axis=ax)
            ok = ~fond & ~np.isnan(ref) & (np.abs(g - np.nan_to_num(ref)) < pas) & (g > sol)
            ajout |= ok
        if not ajout.any():
            break
        fond |= ajout
        val = np.where(fond, g, np.nan)
    return fond


def detourer(src, cote=760):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape

    bord = _cadre(a)
    if bord.std(axis=0).mean() > CADRE_UNI or np.median(bord, axis=0).min() < 200:
        return None, "fond non uni"

    g = a.mean(axis=2)
    depart = np.zeros((h, w), bool)
    depart[:3] = depart[-3:] = True
    depart[:, :3] = depart[:, -3:] = True
    depart &= g > SOL
    fond = _propager(g, depart)

    # on ne garde que la silhouette principale : le reste est du bruit de fond
    lab, n = ndimage.label(~fond)
    if n == 0:
        return None, "produit introuvable"
    aire = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    produit = lab == 1 + int(np.argmax(aire))

    # poches de fond enfermées par le produit : le vide entre les montants
    # d'une poignée de valise, l'intérieur d'une anse. La propagation ne les
    # atteint pas, elles sont closes — on les repère à leur couleur.
    proche = np.linalg.norm(a - np.median(bord, axis=0), axis=2) < 26
    lab2, n2 = ndimage.label(produit & proche)
    for i in range(1, n2 + 1):
        poche = lab2 == i
        if poche.sum() < POCHE * h * w:
            produit &= ~poche

    if produit.sum() < 0.04 * h * w:
        return None, "produit introuvable"
    if (produit & proche).sum() / produit.sum() > SALE:
        return None, "fond résiduel"
    # garde-fou : la propagation peut traverser une matière claire et manger
    # une anse. On ne compte que la matière franche — une ombre portée, elle,
    # reste proche du fond et doit partir sans faire rejeter la photo.
    matiere = np.linalg.norm(a - np.median(bord, axis=0), axis=2) > 70
    if (matiere & ~produit).sum() / max(1, matiere.sum()) > 0.02:
        return None, "matière mangée"
    garde = produit

    alpha = Image.fromarray((garde * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    out = im.convert("RGBA"); out.putalpha(alpha)
    bb = alpha.point(lambda v: 255 if v > 24 else 0).getbbox()
    if bb: out = out.crop(bb)
    if min(out.size) < 0.12 * max(out.size):
        return None, "silhouette plate"
    r = cote / max(out.size)
    return out.resize((max(1, int(out.width * r)), max(1, int(out.height * r))), Image.LANCZOS), "ok"


if __name__ == "__main__":
    sel = json.load(open("/tmp/sacs.json"))
    out = pathlib.Path(__file__).parent / "_travail/CB-08/produits"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("p*.png"): f.unlink()
    gardes = []
    for marque, nom, f in sel:
        im, mot = detourer(f)
        if im is None:
            print(f"  rejet  {marque:<16}{mot:<18}{nom[:34]}")
            continue
        im.save(out / f"p{len(gardes):02d}.png")
        gardes.append([marque, nom])
        print(f"  p{len(gardes)-1:02d}    {marque:<16}{str(im.size):<12}{nom[:34]}")
    json.dump(gardes, open(out / "noms.json", "w"), ensure_ascii=False)
    print(len(gardes), "gardés /", len(sel))
