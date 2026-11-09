#!/usr/bin/env python3
"""Fabrique le logo de la chaîne d'actu people, au format exigé par signature.py.

    /usr/bin/python3 moteur/outils/logo_people.py            # nom par défaut (people.NOM_CHAINE)
    /usr/bin/python3 moteur/outils/logo_people.py "LE SPOT"  # ou un autre nom

Sortie : moteur/media/logo-<ardoise>.png, 900 × 179, BLANC et rouge sur fond transparent (la chaine vit sur noir).
Le sigle occupe x 0-285 (le « recto / verso » : disque coupé, encre et rouge), le mot x 300-900.
signature_people() le pose tel quel sur le papier : les couleurs finales sont celles du fichier.
"""
import math, pathlib, re, sys, unicodedata
import skia

ICI = pathlib.Path(__file__).resolve().parent.parent      # moteur/
sys.path.insert(0, str(ICI))
from moteur import texte, largeur, hauteurLigne, peinture, hexa, disque, trait, ajuste
import people

W, H = 900, 179
SIGLE_W, MOT_X = 285, 300


def ardoise(s):
    s = "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fabrique(nom):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kUnpremul_AlphaType))
    c = surf.getCanvas()
    c.clear(skia.ColorTRANSPARENT)

    # ── sigle : « recto / verso ». Un disque coupé net, moitié encre moitié rouge.
    #    Abstrait, lisible à 32 px, et il dit le nom sans l'illustrer bêtement.
    cx, cy, r = 112, H / 2, 54
    c.drawCircle(cx, cy, r, peinture(people.ENCRE))
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(cx, cy - r - 4, cx + r + 4, cy + r + 4))
    c.drawCircle(cx, cy, r, peinture(people.ROUGE))
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(cx - 3, cy - r - 10, 6, 2 * r + 20), peinture(people.FOND))
    c.drawCircle(cx, cy, r + 13, peinture(people.ENCRE, 1.0, Style=skia.Paint.kStroke_Style, StrokeWidth=7))

    # ── mot : le nom de la chaîne, centré dans x 300-900
    larg = W - MOT_X - 24
    taille = ajuste(nom, larg, 108, "noir", -0.03)
    w = largeur(nom, taille, "noir", -0.03)
    texte(c, nom, MOT_X + (larg - w) / 2, cy - hauteurLigne(taille, "noir") / 2, taille,
          people.ENCRE, "noir", "gauche", -0.03)

    dest = ICI / "media" / f"logo-{ardoise(nom)}.png"
    dest.parent.mkdir(exist_ok=True)
    surf.makeImageSnapshot().save(str(dest), skia.EncodedImageFormat.kPNG)
    return dest


if __name__ == "__main__":
    if len(sys.argv) > 1:
        nom = sys.argv[1]
    else:
        import people
        nom = people.NOM_CHAINE
    print(fabrique(nom))
