"""Découpe les cartes en verre fournies par Youssef (17/10/2026) en morceaux utilisables par moteur/glace.py.

Sources : banque/glace/sources/ (kit-ui.png, vitrine-sites.png, panneau-givre.png) — la vitrine a un damier imprimé
dans l'image (faux fond transparent) : on n'en garde que l'intérieur du cadre, coins arrondis découpés au masque.
Les cadres eux-mêmes sont redessinés par glace.py (bords nets en perspective) ; on ne garde que le contenu.
"""
import pathlib
from PIL import Image, ImageDraw

B = pathlib.Path(__file__).resolve().parents[2] / "banque" / "glace"


def coupe(src, box, nom, rayon=0, echelle=2):
    im = src.crop(box)
    if rayon:
        w, h = im.size
        m = Image.new("L", (w * 4, h * 4), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 4 - 1, h * 4 - 1), rayon * 4, fill=255)
        m = m.resize((w, h), Image.LANCZOS)
        a = im.getchannel("A") if im.mode == "RGBA" else Image.new("L", (w, h), 255)
        im = im.convert("RGBA"); im.putalpha(Image.fromarray(__import__("numpy").minimum(__import__("numpy").array(a), __import__("numpy").array(m))))
    if echelle != 1:
        im = im.resize((im.width * echelle, im.height * echelle), Image.LANCZOS)
    im.save(B / f"{nom}.png")
    print(nom, im.size)


kit = Image.open(B / "sources" / "kit-ui.png").convert("RGBA")
vit = Image.open(B / "sources" / "vitrine-sites.png").convert("RGBA")
giv = Image.open(B / "sources" / "panneau-givre.png").convert("RGBA")

# kit d'interface (sans les éléments ChatGPT)
coupe(kit, (44, 680, 522, 906), "gen3d", 26)               # « Generating 3D scenes… » + 3 rendus de voiture
coupe(kit, (626, 1084, 978, 1150), "rendu_ligne", 0)       # « Rendering… » + barre (sans le logo)
coupe(kit, (562, 1237, 980, 1298), "termine_ligne", 18)    # « Completed! Your video is ready »
coupe(kit, (788, 700, 990, 780), "done", 22)
coupe(kit, (788, 818, 990, 896), "fichier", 22)
coupe(kit, (56, 1088, 506, 1278), "lecteur", 22)           # Final Edit.mov
coupe(kit, (72, 1346, 410, 1420), "outils", 24)
coupe(kit, (462, 1346, 976, 1424), "onde", 30)
for nom, box in dict(blender=(718, 953, 782, 1024), ae=(789, 953, 853, 1024), figma=(856, 953, 912, 1024),
                     reglages=(918, 953, 990, 1024)).items():
    coupe(kit, box, "app_" + nom, 16)
# vitrine de modèles de sites
coupe(vit, (58, 378, 968, 1228), "vitrine", 58)
for k, x in enumerate([77, 301, 525, 749]):
    coupe(vit, (x, 1050, x + 204, 1205), f"modele{k}", 10)
coupe(vit, (205, 460, 965, 995), "ecrans", 0)
# panneau givré (verre clair)
coupe(giv, (170, 222, 920, 1222), "givre", 48)

# cartes produits en verre clair (Youssef, 17/10/2026) : damier imprimé → découpe au masque arrondi, une carte par fichier.
# Noms de fichiers sans marque (règle de conformité du 17/10).
cp_ = Image.open(B / "sources" / "cartes-produits.png").convert("RGBA")
for nom, box in dict(lunettes=(47, 87, 528, 449), montre=(554, 90, 896, 551), baskets=(44, 492, 486, 853),
                     bracelet=(514, 590, 902, 853), ensemble=(257, 892, 686, 1621)).items():
    coupe(cp_, box, "carte_" + nom, 30, 1)
