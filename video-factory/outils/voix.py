#!/usr/bin/env python3
"""Génère les voix off ElevenLabs des 50 scripts de la bibliothèque.

La clé n'est jamais écrite ici : elle est lue dans ~/.config/dyou/elevenlabs.json
    {"api_key": "sk_...", "voice_id": "...", "model_id": "eleven_multilingual_v2"}

    ./voix.py --etat                 quota restant et coût des scripts, sans rien générer
    ./voix.py --voix                 liste les voix du compte
    ./voix.py --un RES-01            génère un seul audio
    ./voix.py --famille RES          génère les dix RES
    ./voix.py --tout                 génère tout ce qui manque
Ajoute --forcer pour régénérer un audio déjà présent.
"""
import argparse, json, os, pathlib, sys, urllib.error, urllib.request

API = "https://api.elevenlabs.io/v1"
CONF = pathlib.Path.home()/".config/dyou/elevenlabs.json"
RACINE = pathlib.Path(__file__).resolve().parent.parent
VIDEOS = RACINE/"videos"

def conf():
    if not CONF.exists():
        sys.exit(f"Aucune clé. Crée {CONF} :\n"
                 '  {"api_key": "sk_...", "voice_id": "...", "model_id": "eleven_multilingual_v2"}')
    c = json.load(open(CONF))
    if not c.get("api_key"): sys.exit(f"{CONF} ne contient pas api_key.")
    return c

def appel(chemin, cle, methode="GET", corps=None, brut=False):
    req = urllib.request.Request(f"{API}/{chemin}", method=methode,
        data=json.dumps(corps).encode() if corps else None,
        headers={"xi-api-key": cle, **({"Content-Type":"application/json"} if corps else {})})
    try:
        r = urllib.request.urlopen(req, timeout=180)
        return r.read() if brut else json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{chemin} : {e.code} {e.read().decode()[:300]}") from None

def scripts():
    """id -> (texte, chemin du mp3 attendu)"""
    out = {}
    for d in sorted(VIDEOS.iterdir()):
        if not d.is_dir(): continue
        s = d/"script.txt"
        if s.exists():
            out[d.name] = (s.read_text(encoding="utf-8").strip(), d/"audio"/f"{d.name}.mp3")
    return out

def etat(c):
    u = appel("user/subscription", c["api_key"])
    reste = u["character_limit"] - u["character_count"]
    print(f"Offre        : {u.get('tier')}")
    print(f"Crédits      : {u['character_count']} utilisés sur {u['character_limit']}  →  {reste} restants")
    sc = scripts()
    manquants = {k:v for k,v in sc.items() if not v[1].exists()}
    besoin = sum(len(t) for t,_ in manquants.values())
    print(f"\nScripts      : {len(sc)} au total, {len(manquants)} sans MP3")
    print(f"Coût restant : {besoin} caractères (1 crédit par caractère en multilingual v2)")
    if besoin > reste:
        faisables = 0; cumul = 0
        for k,(t,_) in sorted(manquants.items(), key=lambda x: len(x[1][0])):
            if cumul+len(t) > reste: break
            cumul += len(t); faisables += 1
        print(f"\n  Le quota ne couvre pas tout : {faisables} scripts sur {len(manquants)} passent.")
    else:
        print(f"\n  Le quota suffit. Il resterait {reste-besoin} crédits.")

def lister_voix(c):
    for v in appel("voices", c["api_key"])["voices"]:
        print(f"  {v['voice_id']}  {v['name']:<22} {v.get('labels',{}).get('language','')} "
              f"{v.get('labels',{}).get('gender','')} {v.get('labels',{}).get('accent','')}")

def generer(c, ident, texte, cible, forcer=False):
    if cible.exists() and not forcer:
        print(f"  {ident} : déjà là, ignoré"); return 0
    if not c.get("voice_id"): sys.exit("Ajoute voice_id dans la config (./voix.py --voix pour la liste).")
    audio = appel(f"text-to-speech/{c['voice_id']}", c["api_key"], "POST", {
        "text": texte,
        "model_id": c.get("model_id","eleven_multilingual_v2"),
        "voice_settings": c.get("voice_settings", {"stability":0.42,"similarity_boost":0.80,"style":0.30,"use_speaker_boost":True}),
    }, brut=True)
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_bytes(audio)
    print(f"  {ident} : {len(texte)} car. → {cible.relative_to(RACINE)} ({len(audio)//1024} Ko)")
    return len(texte)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--etat", action="store_true"); p.add_argument("--voix", action="store_true")
    p.add_argument("--un"); p.add_argument("--famille"); p.add_argument("--tout", action="store_true")
    p.add_argument("--forcer", action="store_true")
    a = p.parse_args()
    c = conf()
    if a.voix: return lister_voix(c)
    if a.etat or not (a.un or a.famille or a.tout): return etat(c)
    sc = scripts()
    if a.un:
        if a.un not in sc: sys.exit(f"{a.un} inconnu.")
        cibles = {a.un: sc[a.un]}
    elif a.famille:
        cibles = {k:v for k,v in sc.items() if k.startswith(a.famille.upper()+"-")}
    else:
        cibles = sc
    u = appel("user/subscription", c["api_key"])
    reste = u["character_limit"] - u["character_count"]
    total = 0
    for ident,(texte,cible) in sorted(cibles.items()):
        if not (cible.exists() and not a.forcer) and total+len(texte) > reste:
            print(f"  {ident} : ARRÊT, quota épuisé ({reste-total} crédits restants)"); break
        total += generer(c, ident, texte, cible, a.forcer)
    print(f"\n{total} caractères consommés. Il reste environ {reste-total} crédits.")

if __name__ == "__main__": main()
