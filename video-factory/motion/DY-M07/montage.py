"""DY-M07 « Collection d'hiver » — edit d'une visite de showroom (vestes, doudounes) pour DROP&YOU (15/10/2026).

Vidéo de Youssef (30,0 s, 1072×1904, 59,94 i/s) ; voix d'origine passée au changeur de voix ElevenLabs avec Léo (même
rythme, `voix-sts/DY-M07-voix-leo.mp3`). Mots : whisper (small, -dtw) sur la voix Léo en 4 morceaux (le fichier entier
fait planter -dtw), temps recalés sur les débuts de parole. Les marques dites à voix haute sont masquées d'une étoile dans
les sous-titres. La dernière image tient 1,5 s pour le carton de fin.

    /usr/bin/python3 montage.py apercu 2.2 6 …   → apercus/planche.jpg
    /usr/bin/python3 montage.py video            → renders/image.mp4
    /usr/bin/python3 montage.py son              → video/DY-M07.mp4
"""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from edit import Edit, groupes, sous_titres, pastille, liste, logo_fin, bouton_enregistre

DUREE = 31.5
T_FIN = 30.05
MOTS = [("On", .14), ("est", .32), ("revenus", .54), ("pour", 1.23), ("vous", 1.34), ("montrer", 1.62), ("un", 1.82), ("peu", 1.92),
        ("plus", 2.10), ("les", 2.22), ("collections", 2.44), ("d'hiver.", 2.62),
        ("Y'a", 3.20), ("cette", 3.46), ("veste", 3.62), ("qui", 3.88), ("est", 3.96), ("arrivée", 4.14), ("en", 4.56), ("noir.", 4.84),
        ("Vous", 5.51), ("avez", 5.62), ("filmé", 5.82), ("la", 6.04), ("bleue", 6.16), ("la", 6.28), ("dernière", 6.42), ("fois,", 6.74),
        ("qui", 7.34), ("est", 7.44), ("toujours", 7.72), ("disponible", 7.98), ("en", 8.36), ("bleu.", 8.56),
        ("Pour", 9.57), ("tout", 9.72), ("ce", 9.84), ("qui", 9.92), ("est", 10.0), ("M*ncler,", 10.18),
        ("j'ai", 10.92), ("eu", 11.04), ("beaucoup", 11.28), ("de", 11.44), ("demandes.", 11.64),
        ("Il", 12.66), ("y", 12.74), ("a", 12.78), ("tous", 12.92), ("les", 13.06), ("modèles", 13.24), ("Maya", 13.90), ("et", 14.36), ("autres.", 14.66),
        ("Il", 15.46), ("y", 15.50), ("a", 15.54), ("aussi", 15.70), ("cette", 15.94), ("veste", 16.08),
        ("que", 16.51), ("je", 16.58), ("vous", 16.66), ("avais", 16.78), ("montrée", 16.96), ("la", 17.20), ("dernière", 17.30), ("fois.", 17.56),
        ("Là,", 18.25), ("on", 18.48), ("la", 18.58), ("voit", 18.70), ("un", 18.88), ("peu", 18.98), ("mieux.", 19.20),
        ("Et", 19.78), ("pour", 20.08), ("tout", 20.22), ("ce", 20.34), ("qui", 20.44), ("est", 20.62), ("M*ncler,", 21.08),
        ("B*rberry,", 21.82), ("L*uis", 22.50), ("V*itton,", 22.68), ("il", 23.10), ("y", 23.14), ("a", 23.16), ("tout", 23.28), ("disponible.", 23.52),
        ("Les", 24.40), ("plumes,", 24.66), ("les", 24.98), ("vestes,", 25.10), ("vraiment", 25.38), ("toute", 25.56), ("la", 25.72),
        ("collection", 25.92), ("d'hiver.", 26.32),
        ("Et", 27.11), ("pour", 27.20), ("ceux", 27.32), ("qui", 27.46), ("veulent,", 27.66), ("les", 28.08), ("boîtes", 28.26), ("et", 28.52),
        ("les", 28.62), ("sacs", 28.76), ("en", 28.90), ("plus,", 29.06), ("c'est", 29.26), ("disponible.", 29.50)]
GS = groupes(MOTS, fin=T_FIN)

BLEU_GLACE, NOIR, BLEU, ROUGE, VIOLET, VERT, ORANGE, OR = "#0EA5E9", "#111111", "#2563EB", "#E5484D", "#7C3AED", "#16A34A", "#F97316", "#E8A317"


def dessin(c, t):
    pastille(c, t, 2.40, 3.15, 540, 560, "Hiver 2026", "snowflake", BLEU_GLACE, rot=-4)
    pastille(c, t, 4.80, 5.45, 540, 560, "Nouveau coloris : noir", "point", NOIR, rot=3, depuis=1)
    pastille(c, t, 7.95, 9.45, 540, 560, "Noir · Bleu", "point", BLEU, rot=-3, check=True, depuis=-1)
    pastille(c, t, 11.24, 12.55, 540, 560, "Le plus demandé", "flame", ROUGE, rot=-4)
    pastille(c, t, 13.20, 15.35, 540, 560, "Tous les coloris", "layers", VIOLET, rot=3)
    pastille(c, t, 16.90, 18.15, 540, 560, "De retour", "refresh-cw", ORANGE, rot=-3, depuis=1)
    liste(c, t, [("Plumes", "snowflake", BLEU_GLACE, 24.62), ("Vestes", "shirt", VIOLET, 25.06),
                 ("Toute la collection", "layers", OR, 25.90)], 26.95, 200, 500)
    liste(c, t, [("Boîtes", "package", ORANGE, 28.22), ("Sacs", "shopping-bag", ROUGE, 28.72)], 29.95, 200, 520)
    logo_fin(c, t, T_FIN, y=820)
    bouton_enregistre(c, t, T_FIN + 0.45, DUREE + 1, cy=1060)
    sous_titres(c, t, GS)


COUPS = [(2.62, 0.04), (4.84, 0.04), (8.56, 0.04), (10.18, 0.04), (13.90, 0.04), (18.58, 0.10), (21.08, 0.04), (23.52, 0.04),
         (26.32, 0.04), (29.50, 0.04)]
E = Edit(P, P / "media" / "source.mp4", DUREE, dessin, COUPS, centre_zoom=(540, 960))

for t0 in (2.40, 4.80, 7.95, 13.20, 16.90): E.son_(t0, "pop", -17)
for k in range(3): E.son_(11.24 + 0.16 * k, "message_in", -21)
E.son_(18.48, "whoosh_court", -20)
for t0 in (24.62, 25.06, 25.90, 28.22, 28.72): E.son_(t0 - 0.04, "whoosh_court", -21); E.son_(t0, "check", -19)
E.son_(T_FIN, "whoosh", -18); E.son_(T_FIN + 0.08, "ching", -18); E.son_(T_FIN + 0.9, "clic", -18)

if __name__ == "__main__":
    if sys.argv[1] == "apercu": E.apercu([float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == "video": E.video()
    elif sys.argv[1] == "son": print(E.son(P / "voix-sts" / "DY-M07-voix-leo.mp3", "DY-M07"))
