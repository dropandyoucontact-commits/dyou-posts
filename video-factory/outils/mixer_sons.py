#!/usr/bin/env python3
"""Pose les bruitages sur la voix off d'une vidéo.

Chaque événement est (seconde, son, gain dB). Les sons viennent de ../sons,
fabriqués par faire_sons.py. Aucune musique de fond : le contrat l'interdit,
et une nappe sous une voix off de 22 s ne fait que brouiller le message.

    ./mixer_sons.py RES-01
"""
import json, pathlib, subprocess, sys

RAC = pathlib.Path(__file__).resolve().parent.parent
SONS = RAC/"sons"

def mixer(voix, evenements, sortie, gain_voix=0.0):
    entrees = ["-i", str(voix)]
    uniques = sorted({e[1] for e in evenements})
    for s in uniques: entrees += ["-i", str(SONS/f"{s}.wav")]
    idx = {s: i+1 for i, s in enumerate(uniques)}
    filtres, etiquettes = [], []
    for n, (sec, son, gain) in enumerate(evenements):
        filtres.append(f"[{idx[son]}]adelay={int(sec*1000)}|{int(sec*1000)},"
                       f"volume={gain}dB[s{n}]")
        etiquettes.append(f"[s{n}]")
    filtres.append(f"[0]loudnorm=I=-16:TP=-1.5:LRA=11,volume={gain_voix}dB[v]")
    filtres.append("[v]" + "".join(etiquettes) +
                   f"amix=inputs={len(evenements)+1}:normalize=0:duration=first[m]")
    filtres.append("[m]alimiter=limit=0.95,aresample=44100[out]")
    cmd = ["ffmpeg","-v","error","-y"] + entrees + [
        "-filter_complex", ";".join(filtres), "-map","[out]",
        "-c:a","pcm_s16le", str(sortie)]
    subprocess.run(cmd, check=True)
    return sortie

def evenements_RES01():
    """Timecodes tirés des bornes de plan de montage_RES01.py."""
    deb = [0.000, 2.400, 8.000, 10.867, 18.200, 20.467]
    ev = []
    # changement de plan
    for d in deb[1:]: ev.append((d, "whoosh", -15))
    # lignes de titre (d0 + 0,10 s par ligne)
    for d, d0 in zip(deb, [0.08, 0.05, 0.03, 0.05, 0.03, None]):
        if d0 is None: continue
        ev += [(d+d0, "tick", -13), (d+d0+0.10, "tick", -14)]
    # cartes et libellés
    ev += [(2.400+1.50, "pop", -11)]                                  # « 10 MINUTES »
    ev += [(8.000+q, "pop", -12) for q in (0.35, 0.70, 1.05)]         # les trois artisans
    ev += [(10.867+q, "pop", -13) for q in (1.10, 3.00, 4.90)]        # libellés du mockup
    # défilement dans le téléphone
    ev += [(10.867+q, "swipe", -20) for q in (0.9, 2.4, 4.1, 5.8)]
    # carton final
    ev += [(20.467, "impact", -9), (20.467+0.60, "pop", -11)]
    return sorted(ev)

def evenements_CB08():
    """CB-08 : trame dense. Un tick par mot révélé, un pop par élément,
    un whoosh à chaque coupe, un impact sur les temps forts.

    Les bornes sont les cumuls d'images de PLANS dans montage_CB08.py
    (22, 30, 43, 47, 63, 29, 26 à 30 i/s), pas des secondes arrondies à la
    main : une demi-image de décalage s'entend sur un montage aussi serré.
    """
    deb = [0.000, 0.733, 1.733, 3.167, 4.733, 6.833, 7.800]
    ev = []
    for d in deb[1:]: ev.append((d, "whoosh", -11))
    # un tick par mot de titre, aux décalages de mots() dans le montage
    titres = [(deb[0], [0.02, 0.12]),
              (deb[1], [0.02, 0.11]),
              (deb[2], [0.00, 0.08, 0.18, 0.26]),
              (deb[3], [0.00, 0.07, 0.20, 0.26, 0.32, 0.38]),
              (deb[4], [0.00, 0.08, 0.16, 0.24]),
              (deb[5], [0.02, 0.14])]
    for base, offs in titres:
        for o in offs: ev.append((base+o, "tick", -12))
    ev += [(deb[0]+0.02,"pop",-11), (deb[0]+0.07,"pop",-11)]          # les deux valises
    ev += [(deb[1]+0.26,"pop",-10), (deb[1]+0.40,"pop",-10)]          # revendeur / fournisseur
    ev += [(deb[2]+0.32,"pop",-11), (deb[2]+0.62,"impact",-10)]       # barre puis la marge
    ev += [(deb[3]+0.34,"pop",-11), (deb[3]+0.80,"pop",-12)]          # barre puis le trait
    ev += [(deb[4]+q,"swipe",-17) for q in (0.10, 0.20, 0.30)]        # le mur qui défile
    ev += [(deb[4]+0.70,"pop",-10), (deb[4]+1.20,"pop",-10)]          # qualité / transport
    ev += [(deb[5]+0.14,"impact",-8), (deb[5]+0.42,"pop",-10)]        # CHINABOOK puis la bulle
    ev += [(deb[6]+0.00,"impact",-9)]                                 # logo
    ev += [(deb[6]+0.26,"pop",-10), (deb[6]+0.46,"pop",-10)]          # WhatsApp / Snapchat
    ev += [(deb[0],"impact",-11)]                                     # accent d'ouverture
    return sorted(ev)

if __name__ == "__main__":
    ident = sys.argv[1] if len(sys.argv) > 1 else "RES-01"
    voix = RAC/f"videos/{ident}/audio/{ident}.mp3"
    sortie = pathlib.Path(__file__).parent/f"_travail/{ident}/piste.wav"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    ev = {"RES-01": evenements_RES01, "CB-08": evenements_CB08}[ident]()
    mixer(voix, ev, sortie)
    print(f"{len(ev)} bruitages posés -> {sortie}")
