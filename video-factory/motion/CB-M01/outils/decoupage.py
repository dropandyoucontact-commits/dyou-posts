#!/usr/bin/env python3
"""Écrit DECOUPAGE.md à partir du code : temps réels des phrases (calés sur la voix)
et fenêtres des scènes. À relancer après toute modification de scenes.py."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import scenes

ICI = pathlib.Path(__file__).resolve().parent.parent

PLANS = [
    (0.00, 3.52, "Accroche", "La moto frappe l'écran, puis le pull et le casque défilent en 3D. La moto revient avec l'étiquette rouge « REVENDEUR + sa marge », puis les repères « Français → en Chine »."),
    (3.46, 6.98, "La marge", "Barre de prix : Usine, puis « Ta marge » en vert. Au mot « payer », « Sa marge » en rouge s'insère et écrase la verte contre le prix de vente. Tampon « LA SIENNE »."),
    (6.84, 15.80, "Le circuit", "Fournisseur → Revendeur → Toi. Le colis descend et reçoit « + MARGE » chez le revendeur, puis arrive chez toi avec le ticket. « À chaque commande » : trois colis en rafale, compteur × 2, × 3."),
    (15.80, 18.62, "En direct", "Les ciseaux coupent deux fois, le revendeur tombe. Fournisseur et Toi se rejoignent par une ligne verte, pastille « EN DIRECT » et confettis."),
    (18.42, 24.72, "Sur place", "Carte de Chine entière, zoom sur Guangzhou, épingle et « SUR PLACE ». Quatre tuiles calées sur les verbes : Chercher, Commander, Comparer, Trier."),
    (24.55, 28.20, "Deux semaines", "Calendrier « SUR PLACE » qui défile de 1 à 14 jours. Cinq cartes de contacts « À vérifier » s'empilent, puis des « ? » apparaissent."),
    (28.20, 33.95, "Le tri", "Les cartes passent en liste. Trois critères (Promesses, Qualité, Expédition) éliminent les contacts un par un : croix rouge, sortie. Le dernier devient « FIABLE ». Au mot « recul » : zoom arrière, les semaines se cochent."),
    (33.80, 37.30, "Commandes test", "Trois colis tombent (moto, pull, casque), coches vertes. Au mot « fait » : grande coche verte qui remplit l'écran."),
    (37.05, 41.10, "ChinaBook", "Plein écran vert, le logo blanc frappe, puis le vert se range dans l'écran du téléphone : catalogue par catégories, contacts directs vérifiés, pastille « TESTÉS PENDANT DES MOIS »."),
    (40.90, 44.97, "Le réseau", "Le téléphone devient le moyeu ChinaBook. Fournisseurs et Transitaire s'y raccordent, le réseau s'étend. Tampon « MOI-MÊME »."),
    (44.80, 49.45, "Contacter, négocier, commander", "Conversation illustrative avec un fournisseur : demande, photo, réponse, discussion, puis « Commande envoyée ». Tampon « EN DIRECT »."),
    (49.25, 53.48, "Reprendre le contrôle", "Le catalogue s'agrandit, puis un grand interrupteur passe de « INTERMÉDIAIRE » (rouge) à « DIRECT » (vert) au mot « contrôle »."),
    (53.30, 57.86, "Appel à l'action", "Conversation ChinaBook : « CHINA » se tape lettre par lettre au rythme de la voix et s'envoie. Réponse « Voici le pack adapté… » avec trois catégories."),
    (57.86, 59.40, "Carton final", "Logo ChinaBook, bouton « Envoie « CHINA » sur WhatsApp » qui pulse, titre « Ton accès direct à la Chine. »"),
]

def main():
    l = ["# CB-M01 — découpage final, recalé sur la voix", "",
         "Vidéo 1080 × 1920, 60 i/s, 59,4 s (voix 57,89 s + 1,5 s de carton final).",
         "Généré par `outils/decoupage.py` à partir de `scenes.py` et `timing.json`.", "",
         "## Plans", "", "| Début | Fin | Plan | Ce qui se passe |", "|---:|---:|---|---|"]
    for a, b, nom, quoi in PLANS:
        l.append(f"| {a:05.2f} | {b:05.2f} | {nom} | {quoi} |")
    l += ["", "## Sous-titres (chaque mot apparaît au moment où il est prononcé)", "",
          "| Début | Fin | Texte à l'écran |", "|---:|---:|---|"]
    for bl in scenes.BLOCS:
        fin = min(bl["fin"], scenes.DUREE)
        l.append(f"| {max(0, bl['debut']):05.2f} | {fin:05.2f} | {' '.join(m['s'] for m in bl['mots'])} |")
    l += ["", f"## Bruitages", "", f"{len(scenes.SFX)} sons posés sous la voix (liste exacte : `sfx.json`).", ""]
    (ICI / "DECOUPAGE.md").write_text("\n".join(l))
    print("DECOUPAGE.md :", len(scenes.BLOCS), "blocs de sous-titres,", len(PLANS), "plans")

if __name__ == "__main__":
    main()
