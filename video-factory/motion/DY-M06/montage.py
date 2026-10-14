"""DY-M06 « Pépites de malade » — edit d'une vidéo tournée en showroom (baskets, sacs) pour DROP&YOU (15/10/2026).

Vidéo de Youssef (22,4 s, 1072×1904, 60 i/s) ; voix d'origine passée au changeur de voix ElevenLabs avec Léo (même rythme,
`voix-sts/DY-M06-voix-leo.mp3`). Mots : whisper (small, -dtw) sur la voix Léo, temps recalés sur les débuts de parole
(whisper -dtw arrive ≈ 0,1 s après l'attaque du mot).

    /usr/bin/python3 montage.py apercu 2.2 6 …   → apercus/planche.jpg
    /usr/bin/python3 montage.py video            → renders/image.mp4
    /usr/bin/python3 montage.py son              → video/DY-M06.mp4
"""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from edit import Edit, groupes, sous_titres, pastille, liste, logo_fin, bouton_enregistre

DUREE = 22.36
MOTS = [("La", .26), ("famille,", .62), ("là,", .82), ("je", .92), ("vous", 1.0), ("ai", 1.16), ("sorti", 1.38),
        ("des", 1.70), ("pépites", 1.98), ("de", 2.48), ("malade.", 2.98),
        ("T'es", 3.86), ("malade !", 4.04),
        ("Ça,", 4.50), ("c'est", 5.23), ("de", 5.36), ("la", 5.46), ("clone,", 5.68),
        ("c'est", 6.02), ("pas", 6.18), ("de", 6.26), ("la", 6.36), ("full", 6.48), ("qualité,", 6.72),
        ("c'est", 7.02), ("de", 7.08), ("la", 7.16), ("clone,", 7.36),
        ("c'est", 7.56), ("encore", 7.72), ("mieux.", 8.02),
        ("T'es", 8.70), ("malade.", 8.84),
        ("Quand", 11.04), ("je", 11.14), ("vous", 11.22), ("dis", 11.36), ("la", 11.48), ("famille,", 11.74),
        ("je", 11.90), ("vous", 12.0), ("sors", 12.18), ("les", 12.36), ("meilleures", 12.52), ("qualités", 12.82),
        ("et", 13.24), ("on", 13.34), ("a", 13.48), ("le", 13.60), ("meilleur", 13.68), ("prix.", 14.04),
        ("Full", 15.13), ("packaging,", 15.52),
        ("t'es", 16.40), ("malade,", 16.56), ("couture,", 16.82), ("tout.", 17.40),
        ("On", 18.37), ("n'a", 18.44), ("pas", 18.54), ("peur", 18.72), ("de", 18.86), ("zoomer.", 19.0)]
T = dict()
for m, t in MOTS: T.setdefault(m.strip(".,!? "), t)
GS = groupes(MOTS, fin=19.45)
T_FIN = 19.45

VIOLET, VERT, OR, ROUGE, GRIS, ORANGE = "#7C3AED", "#16A34A", "#E8A317", "#E5484D", "#6B7280", "#F97316"


def dessin(c, t):
    # « pépites de malade »
    pastille(c, t, 1.92, 3.75, 540, 600, "Pépites de malade", "gem", VIOLET, rot=-4)
    # « c'est de la clone, c'est pas de la full qualité… c'est encore mieux »
    pastille(c, t, 5.64, 8.6, 540, 580, "Qualité clone", "badge-check", VERT, rot=-4, check=True)
    pastille(c, t, 6.44, 7.32, 560, 720, "Full qualité", "x", GRIS, taille=38, rot=4, depuis=1)
    pastille(c, t, 7.98, 8.6, 560, 720, "Encore mieux", "trending-up", OR, taille=40, rot=3)
    # « les meilleures qualités et le meilleur prix »
    pastille(c, t, 12.78, 14.7, 470, 560, "Meilleure qualité", "star", OR, rot=-4, depuis=-1)
    pastille(c, t, 13.64, 14.7, 610, 690, "Meilleur prix", "euro", VERT, rot=3, depuis=1)
    # « full packaging, couture, tout »
    liste(c, t, [("Full packaging", "package", ORANGE, 15.13), ("Couture", "scissors", VIOLET, 16.80), ("Tout", "search", VERT, 17.38)],
          18.25, 200, 520)
    # fin
    logo_fin(c, t, T_FIN, y=820)
    bouton_enregistre(c, t, T_FIN + 0.5, DUREE + 1, cy=1060)
    sous_titres(c, t, GS)


# coups de zoom sur les mots forts ; « on n'a pas peur de zoomer » : vrai zoom
COUPS = [(T["pépites"], 0.04), (3.86, 0.06), (T["clone"], 0.04), (8.02, 0.05), (8.70, 0.05), (13.68, 0.04), (15.13, 0.04),
         (18.86, 0.16)]
E = Edit(P, P / "media" / "source.mp4", DUREE, dessin, COUPS, centre_zoom=(540, 960))

for t0 in (1.92, 5.64, 12.78, 13.64): E.son_(t0, "pop", -17)
E.son_(6.44, "whoosh_court", -20); E.son_(7.98, "montee", -21)
E.son_(13.64, "ching", -19)
for t0 in (15.13, 16.80, 17.38): E.son_(t0 - 0.04, "whoosh_court", -21); E.son_(t0, "check", -19)
E.son_(18.86, "whoosh_long", -19)
E.son_(T_FIN, "whoosh", -18); E.son_(T_FIN + 0.08, "ching", -18); E.son_(T_FIN + 0.95, "clic", -18)

if __name__ == "__main__":
    if sys.argv[1] == "apercu": E.apercu([float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == "video": E.video()
    elif sys.argv[1] == "son": print(E.son(P / "voix-sts" / "DY-M06-voix-leo.mp3", "DY-M06"))
