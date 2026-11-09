#!/usr/bin/env python3
"""timing.json estimé, sans dépenser un crédit ElevenLabs.

Sert quand les crédits sont épuisés : on peut chorégraphier toute la vidéo au
rythme validé (4,2 mots/s, pauses 0,18 s, hook à 5,2 mots/s) et poser la vraie
voix après, en relançant voix.py puis le rendu. Les mots tombent à ±0,15 s près.

    cd video-factory/motion/MON-ID
    python3 ../moteur/outils/timing_estime.py            # 4,2 mots/s
    python3 ../moteur/outils/timing_estime.py --debit 4.0

timing.json porte "source": "estime" — verifier.py et le rendu final doivent
voir "elevenlabs-with-timestamps" avant la livraison.
"""
import argparse, json, pathlib, re, sys

ICI = pathlib.Path.cwd()
PONCT_FIN = ".!?…"
PONCT_COURTE = ",;:"


def mots_du_script(texte):
    texte = re.sub(r"\s+", " ", texte.strip())
    out = []
    for brut in texte.split(" "):
        if not brut:
            continue
        if out and all(ch in PONCT_FIN + PONCT_COURTE + "»)" for ch in brut):
            out[-1] = out[-1] + " " + brut
        else:
            out.append(brut)
    return out


def estime(mots, debit, pause_fin, pause_courte, debit_hook):
    nus = [re.sub(r"[^\wÀ-ÿ'’-]", "", m) for m in mots]
    moy = sum(len(n) for n in nus) / max(1, len(nus))
    # la première phrase part plus vite : règle du hook (19/10/2026)
    fin_hook = next((i for i, m in enumerate(mots) if m and m[-1] in PONCT_FIN), 0)
    res, t = [], 0.0
    for i, (m, n) in enumerate(zip(mots, nus)):
        d = (1.0 / (debit_hook if i <= fin_hook else debit)) * (0.45 + 0.55 * len(n) / moy)
        res.append({"w": m, "t0": round(t, 3), "t1": round(t + d, 3), "i": i})
        t += d
        if m and m[-1] in PONCT_FIN:
            t += pause_fin
        elif m and m[-1] in PONCT_COURTE:
            t += pause_courte
    return res, t


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--debit", type=float, default=4.2)
    p.add_argument("--hook", type=float, default=5.2)
    p.add_argument("--pause", type=float, default=0.18)
    p.add_argument("--pause-courte", type=float, default=0.09)
    a = p.parse_args()

    src = ICI / "script.txt"
    if not src.exists():
        sys.exit("script.txt introuvable dans " + str(ICI))
    mots = mots_du_script(src.read_text(encoding="utf-8"))
    # le débit de référence (voix.py) se mesure pauses comprises : on resserre
    # les mots jusqu'à ce que la mesure globale tombe sur la valeur demandée
    d, h = a.debit, a.hook
    for _ in range(8):
        res, fin = estime(mots, d, a.pause, a.pause_courte, h)
        mesure = len(res) / (res[-1]["t1"] - res[0]["t0"])
        if abs(mesure - a.debit) < 0.01:
            break
        k = a.debit / mesure
        d, h = d * k, h * k
    parle = res[-1]["t1"] - res[0]["t0"]
    (ICI / "timing.json").write_text(json.dumps(
        {"duree_voix": round(fin + 0.3, 3), "vitesse": 1.0, "source": "estime",
         "mots": res}, ensure_ascii=False, indent=1))
    print(f"{len(res)} mots · {len(res) / parle:.2f} mots/s · voix estimée {fin + 0.3:.2f} s")
    print(" ".join(f"{m['i']}:{m['w']}@{m['t0']:.2f}" for m in res))
