import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "moteur"))
import skia, moteur
from moteur import *
import people
from people import PAPIER, ENCRE, ENCRE2, ROUGE, AXE
from kit import texte_centre

for num, (nom, debit) in enumerate([("KAEL", "4,65"), ("PAUL K", "3,97"), ("MARTIN", "3,87")], 1):
    s = surface(); c = s.getCanvas()
    people.fond_grille(c, 0.0)
    texte_centre(c, f"VOIX {num} SUR 3", AXE, 700, 44, ENCRE2, "fort")
    texte_centre(c, nom, AXE, 850, 150, ENCRE, "noir")
    texte_centre(c, f"{debit} mots par seconde", AXE, 980, 50, ROUGE, "fort")
    rrect(c, AXE - 200, 1040, 400, 8, 4, ROUGE, 1.0)
    texte_centre(c, "LE SPOT", AXE, 1500, 30, ENCRE2, "noir")
    s.makeImageSnapshot().save(f"carton-{num}.png", skia.EncodedImageFormat.kPNG)
    print("carton-%d.png %s" % (num, nom))
