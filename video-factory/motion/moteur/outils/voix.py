#!/usr/bin/env python3
"""Voix off ElevenLabs (Tomy, modèle eleven_v4) d'un projet motion, avec le temps de chaque mot.

    cd video-factory/motion/MON-ID            (le dossier contient script.txt)
    python3 ../moteur/outils/voix.py --etat   crédits restants et coût du script, sans rien générer
    python3 ../moteur/outils/voix.py          script.txt → media/voix.mp3 + timing.json
    python3 ../moteur/outils/voix.py --debit 3.6        réaccélère la prise existante (gratuit)

1. ElevenLabs génère la prise à sa vitesse naturelle, avec l'horodatage de chaque
   caractère (endpoint with-timestamps) → media/voix-brut.mp3 + media/voix-alignement.json.
   Pas de transcription : on sait exactement ce qui est dit, et quand.
2. FFmpeg accélère sans changer la hauteur (atempo) jusqu'au débit visé
   (--debit, en mots par seconde ; 3,5 par défaut = débit TikTok rapide mais net)
   → media/voix.mp3.
3. timing.json : {"mots": [{"w", "t0", "t1", "i"}], ...} — même format que celui de
   minutage.py (whisper), donc scenes.py s'en sert de la même façon.

La clé est lue dans ~/.config/dyou/elevenlabs.json (jamais écrite ici). Une prise
déjà générée n'est pas refaite sans --forcer : c'est du crédit.
"""
import argparse, base64, json, pathlib, re, subprocess, sys, urllib.error, urllib.request

API = "https://api.elevenlabs.io/v1"
CONF = pathlib.Path.home() / ".config/dyou/elevenlabs.json"
ICI = pathlib.Path.cwd()
PONCT = set("?!:;.,…»)")

def conf():
    if not CONF.exists():
        sys.exit(f"Aucune clé ElevenLabs : crée {CONF}")
    return json.load(open(CONF))

def appel(chemin, c, corps=None):
    req = urllib.request.Request(f"{API}/{chemin}", method="POST" if corps else "GET",
                                 data=json.dumps(corps).encode() if corps else None,
                                 headers={"xi-api-key": c["api_key"], **({"Content-Type": "application/json"} if corps else {})})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs {chemin} : {e.code} {e.read().decode()[:400]}")

def credits(c):
    u = appel("user/subscription", c)
    return u["character_limit"] - u["character_count"], u

def mots_depuis_alignement(al):
    """regroupe les caractères en mots ; la ponctuation isolée (« ? », « ! ») se colle au mot d'avant"""
    car, deb, fin = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    mots, cur = [], None
    for ch, a, b in zip(car, deb, fin):
        if ch.isspace():
            if cur: mots.append(cur); cur = None
            continue
        if cur is None: cur = {"w": "", "t0": a, "t1": b}
        cur["w"] += ch; cur["t1"] = b
    if cur: mots.append(cur)
    propres = []
    for m in mots:
        if propres and all(ch in PONCT for ch in m["w"]):
            propres[-1]["w"] += " " + m["w"]; propres[-1]["t1"] = m["t1"]
        elif m["w"] in ("«", "—", "–") and propres is not None:
            m["colle_suivant"] = True; propres.append(m)
        else:
            if propres and propres[-1].get("colle_suivant"):
                prev = propres.pop(); m["w"] = prev["w"] + " " + m["w"]; m["t0"] = prev["t0"]
            propres.append(m)
    return propres

def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)

def accelerer(debit):
    al = json.loads((ICI / "media" / "voix-alignement.json").read_text())
    mots = mots_depuis_alignement(al)
    naturel = len(mots) / max(0.1, mots[-1]["t1"] - mots[0]["t0"])
    f = max(1.0, min(1.3, debit / naturel))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ICI / "media" / "voix-brut.mp3"), "-filter:a", f"atempo={f:.4f}",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", str(ICI / "media" / "voix.mp3")], check=True)
    d = duree(ICI / "media" / "voix.mp3")
    out = [{"w": m["w"], "t0": round(m["t0"] / f, 3), "t1": round(m["t1"] / f, 3), "i": i} for i, m in enumerate(mots)]
    (ICI / "timing.json").write_text(json.dumps({"duree_voix": round(d, 3), "vitesse": round(f, 4), "source": "elevenlabs-with-timestamps",
                                                  "mots": out}, ensure_ascii=False, indent=1))
    print(f"débit naturel {naturel:.2f} mots/s → ×{f:.3f} → {len(mots) / (out[-1]['t1'] - out[0]['t0']):.2f} mots/s ; voix {d:.2f} s ; {len(out)} mots dans timing.json")
    print(" ".join(f"{m['i']}:{m['w']}@{m['t0']:.2f}" for m in out))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--etat", action="store_true"); p.add_argument("--forcer", action="store_true")
    p.add_argument("--debit", type=float, default=3.5, help="mots par seconde visés après accélération")
    a = p.parse_args()
    c = conf()
    texte = (ICI / "script.txt").read_text(encoding="utf-8").strip()
    texte = re.sub(r"\s+", " ", texte)
    reste, _ = credits(c)
    if a.etat:
        print(f"script : {len(texte)} caractères ≈ {len(texte)} crédits ; restant sur le compte : {reste}")
        return
    brut = ICI / "media" / "voix-brut.mp3"
    if not brut.exists() or a.forcer:
        if len(texte) > reste:
            sys.exit(f"Crédits insuffisants : {len(texte)} nécessaires, {reste} restants.")
        r = appel(f"text-to-speech/{c['voice_id']}/with-timestamps?output_format=mp3_44100_128", c, {
            "text": texte, "model_id": c.get("model_id", "eleven_v4"),
            "voice_settings": c.get("voice_settings", {"stability": 0.42, "similarity_boost": 0.80, "style": 0.30, "use_speaker_boost": True})})
        brut.parent.mkdir(exist_ok=True)
        brut.write_bytes(base64.b64decode(r["audio_base64"]))
        (ICI / "media" / "voix-alignement.json").write_text(json.dumps(r.get("normalized_alignment") or r["alignment"], ensure_ascii=False))
        print(f"prise générée : {len(texte)} caractères ; crédits restants ≈ {reste - len(texte)}")
    accelerer(a.debit)

if __name__ == "__main__":
    main()
