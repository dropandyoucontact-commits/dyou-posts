#!/usr/bin/env python3
"""Contrôle de conformité avant rendu (règle du 17/10/2026, voir video-factory/CLAUDE.md « Conformité »).

    cd motion/<ID> && python3 ../moteur/outils/conformite.py      → code 1 si une faute bloquante est trouvée

Lit script.txt (la voix), scenes.py (textes à l'écran, logos appelés) et le nom du dossier. Bloquant pour les vidéos
DROP&YOU / ChinaBook (dossiers CB- et DY-) ; pour les autres (DA-, MQ-…) il ne fait qu'avertir.
Ce qu'il ne voit pas : un logo ou une marque visibles DANS une image ou une vidéo → à vérifier à l'œil sur les aperçus.
"""
import pathlib, re, sys

MARQUES = ["saucony", "nike", "jordan", "adidas", "yeezy", "new balance", "asics", "salomon", "puma", "reebok", "vans",
           "converse", "louis vuitton", "vuitton", "gucci", "dior", "chanel", "prada", "hermes", "hermès", "rolex", "cartier",
           "balenciaga", "moncler", "stone island", "supreme", "off-white", "lacoste", "ralph lauren", "burberry", "versace",
           "fendi", "celine", "céline", "ysl", "saint laurent", "goyard", "bottega", "loewe", "miu miu", "valentino",
           "givenchy", "the north face", "north face", "canada goose", "arc'teryx", "arcteryx", "trapstar", "corteiz",
           "essentials", "fear of god", "patek", "audemars", "omega", "apple", "airpods", "iphone", "dyson", "sur-ron",
           "surron", "lv"]
PLATEFORMES = ["whatsapp", "snapchat", "snap", "telegram", "instagram", "insta", "wechat"]
CONTREFACON = ["contrefaçon", "contrefacon", "contrefait", "copie", "copies", "réplique", "replique", "replica", "faux",
               "fake", "dupe", "dupes", "aaa"]
GAIN = [r"ach[eè]te[sz]?\s+\d+", r"\brevend", r"\bresell", r"\bbénéfice", r"\bprofit", r"\brentabilis", r"\bx\s?\d+\s+ta mise"]


def lignes(p):
    return p.read_text(errors="ignore").splitlines() if p.exists() else []


def cherche(texte, mots):
    t = texte.lower()
    return [m for m in mots if re.search(r"(?<![\w-])" + re.escape(m) + r"(?![\w-])", t)]


def main():
    ici = pathlib.Path.cwd()
    bloquant = re.match(r"(CB|DY)-", ici.name) is not None
    fautes, alertes = [], []
    sources = [("nom du dossier", [ici.name.replace("-", " ")])]
    sources.append(("script.txt (voix)", lignes(ici / "script.txt")))
    # dans scenes.py on ne regarde que les chaînes de caractères (ce qui peut s'afficher) et les logos appelés
    chaines = []
    for k, l in enumerate(lignes(ici / "scenes.py"), 1):
        if l.lstrip().startswith("#"): continue
        for s in re.findall(r'"([^"\n]*)"|\'([^\'\n]*)\'', l):
            s = s[0] or s[1]
            if s and not re.fullmatch(r"[\w./-]*\.(png|jpg|mp4|mov|json|svg)", s):
                chaines.append(f"l.{k}: {s}")
        if re.search(r"cta_whatsapp|logo_app\(\s*c\s*,\s*\"(whatsapp|snap|snapchat|telegram|instagram)", l):
            fautes.append(f"scenes.py l.{k} : appel d'un logo/CTA d'une autre plateforme → {l.strip()[:90]}")
    sources.append(("scenes.py (textes)", chaines))
    for nom, ls in sources:
        for l in ls:
            for m in cherche(l, MARQUES): fautes.append(f"{nom} : marque « {m} » → {l.strip()[:100]}")
            for m in cherche(l, PLATEFORMES): fautes.append(f"{nom} : autre plateforme « {m} » → {l.strip()[:100]}")
            for m in cherche(l, CONTREFACON): fautes.append(f"{nom} : mot interdit « {m} » → {l.strip()[:100]}")
            for g in GAIN:
                if re.search(g, l.lower()): alertes.append(f"{nom} : promesse de gain ? → {l.strip()[:100]}")
    script = " ".join(lignes(ici / "script.txt")).lower()
    if bloquant and re.search(r"comment", script) and re.search(r"lien autour|link around", script):
        alertes.append("CTA mélangé : appel à commenter dans une pub (pub = « contacte-moi via le lien autour de cette vidéo »)")
    for a in alertes: print("⚠", a)
    for f in fautes: print("✗", f)
    if not fautes:
        print("conformité : rien à signaler dans le texte (vérifier encore les images à l'œil)")
        return 0
    if bloquant:
        print(f"\n{len(fautes)} faute(s) : rendu bloqué (règle du 17/10/2026, video-factory/CLAUDE.md « Conformité »).")
        return 1
    print(f"\n{len(fautes)} point(s) à regarder (projet hors DROP&YOU / ChinaBook : non bloquant).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
