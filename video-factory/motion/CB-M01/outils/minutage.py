#!/usr/bin/env python3
"""Minutage mot à mot de la voix : whisper.cpp (mots) recalé sur les respirations
mesurées par silencedetect. Whisper avance d'environ 0,1-0,15 s en début de phrase ;
chaque phrase est décalée pour démarrer exactement à la fin du silence qui la précède."""
import json, re, subprocess
SIL = subprocess.run(["ffmpeg","-hide_banner","-i","media/voix.mp3","-af",
      "silencedetect=noise=-32dB:d=0.10","-f","null","-"],capture_output=True,text=True).stderr
starts=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",SIL)]
ends=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",SIL)]
DUREE=57.887
# segments de parole = entre la fin d'un silence et le début du suivant
seg=[]; t=ends[0] if starts and starts[0]<0.01 else 0.0
for s,e in zip(starts[1:] if starts[0]<0.01 else starts, ends[1:] if starts[0]<0.01 else ends):
    seg.append((t,s)); t=e
if t<DUREE-0.05: seg.append((t,DUREE))
mots=[l.split("\t") for l in open("media/voix-mots-whisper.tsv").read().splitlines()]
mots=[(float(a),float(b),w) for a,b,w in mots if w not in "?!.,"]
# corrections d'orthographe (la voix n'est pas modifiée, seulement la transcription)
CORR={"pelles":"paies le","ces":"ses","Chine Book,":"China Book,"}
out=[]
for i,(a,b,w) in enumerate(mots):
    out.append({"w":CORR.get(w,w),"t0":a,"t1":b})
# fusion "Chine" + "Book," en "ChinaBook"
for i in range(len(out)-1):
    if out[i]["w"]=="Chine" and out[i+1]["w"].startswith("Book"):
        out[i]["w"]="China"
# "Envoie-moi Chine sur WhatsApp" : le mot prononcé est CHINA
for i in range(len(out)-1):
    if out[i]["w"]=="Chine" and out[i+1]["w"]=="sur": out[i]["w"]="CHINA"
# recalage par segment
for (s0,s1) in seg:
    dans=[m for m in out if s0-0.30<=m["t0"]<s1-0.05 and "seg" not in m]
    if not dans: continue
    d=s0-dans[0]["t0"]
    for m in dans:
        m["t0"]=round(max(s0,m["t0"]+d),3); m["t1"]=round(min(s1,m["t1"]+d),3); m["seg"]=[round(s0,3),round(s1,3)]
for i,m in enumerate(out): m["i"]=i
json.dump({"duree_voix":DUREE,"segments":[[round(a,3),round(b,3)] for a,b in seg],"mots":out},open("timing.json","w"),ensure_ascii=False,indent=1)
print(len(seg),"segments")
print(" ".join(f'{m["i"]}:{m["w"]}@{m["t0"]:.2f}' for m in out))
