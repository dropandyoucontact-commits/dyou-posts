"""DY-M09 : voix « Avital vlog » phrase par phrase, chaque phrase posée sur son plan (segments.json : début, fin visée, texte).
ElevenLabs avec horodatage → voix/segNN.mp3 + .json ; ne régénère pas une prise existante (crédit)."""
import base64, json, pathlib, sys, urllib.request
ICI = pathlib.Path(__file__).resolve().parent
c = json.load(open(pathlib.Path.home() / ".config/dyou/elevenlabs.json"))
LEO = "zchjMHCgSyHNevwHbPa9"   # « Avital vlog » : jeune, cassée, dynamique (voix dessinée, choisie le 16/10)
for k, (t0, t1, txt) in enumerate(json.load(open(ICI / "segments.json"))):
    f = ICI / "voix" / f"seg{k:02d}.mp3"
    if f.exists() and "--forcer" not in sys.argv: continue
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{LEO}/with-timestamps?output_format=mp3_44100_128", method="POST",
        data=json.dumps({"text": txt, "model_id": c.get("model_id", "eleven_v4"), "language_code": "fr",
                         "voice_settings": {"stability": 0.32, "similarity_boost": 0.8, "style": 0.45, "use_speaker_boost": True}}).encode(),
        headers={"xi-api-key": c["api_key"], "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    f.write_bytes(base64.b64decode(r["audio_base64"]))
    (ICI / "voix" / f"seg{k:02d}.json").write_text(json.dumps(r.get("normalized_alignment") or r["alignment"], ensure_ascii=False))
    print(k, "ok", len(txt))
