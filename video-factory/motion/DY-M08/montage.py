"""DY-M08 « Depuis que je suis parti en Chine » — vlog DROP&YOU monté sur la vidéo muette de Youssef (16/10/2026).

Vidéo source : deux morceaux recollés (38,3 s) — billets, fisheye, regard, profil pensif, passeport, Chine, motos, cartons de
baskets, montres et sacs, marche en ville. Pas de voix d'origine : voix off Léo (`jsScnYkNNda9Q1NES5nn`, celle des edits,
DY-M06) générée phrase par phrase et posée sur son plan (`segments.json`, `voix_segments.py`, `assembler_voix.py`), débit
naturel de vlog. Musique déjà payée posée sous la voix (media/musique.mp3) ; pour les suivantes, pas de musique générée :
Youssef l'ajoute dans CapCut (16/10/2026). `montage.py son --sans-musique` sort la version voix + bruitages.

    /usr/bin/python3 montage.py apercu 2.2 6 …   → apercus/planche.jpg
    /usr/bin/python3 montage.py video            → renders/image.mp4
    /usr/bin/python3 montage.py son              → video/DY-M08.mp4
"""
import json, math, pathlib, subprocess, sys
import numpy as np, skia
P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / "moteur"))
from edit import Edit, groupes, sous_titres, pastille, liste, logo_fin, bouton_enregistre, mesure, SONS, VOLUME_LUFS, W, H
from moteur import prog, entree, rebond, borne, mix, hexa, image, taille_img, Calque

DUREE = 40.6
T_FIN = 38.45

# mots de la voix (temps absolus) ; « Drop and You » s'écrit DROP&YOU
_m = json.load(open(P / "mots.json"))
MOTS, k = [], 0
while k < len(_m):
    w, t = _m[k]
    if w == "Drop" and k + 2 < len(_m) and _m[k + 1][0] == "and":
        MOTS.append(("DROP&YOU.", t)); k += 3; continue
    MOTS.append((w, t)); k += 1
T, T2 = {}, {}                       # T : première occurrence d'un mot, T2 : la dernière
for m, t in MOTS: T.setdefault(m.strip(".,!?… ").lower(), t); T2[m.strip(".,!?… ").lower()] = t
GS = groupes(MOTS, fin=38.4)

VIOLET, VERT, OR, ROUGE, ORANGE, BLEU = "#7C3AED", "#16A34A", "#E8A317", "#E5484D", "#F97316", "#2563EB"
COUPES = [1.55, 4.05, 4.65, 5.31, 7.48, 11.48, 13.65, 15.65, 18.81, 22.98, 29.62, 36.32]   # changements de plan de la source
FLASH = [11.48, 18.81, 29.62, 36.32]                                                         # grandes transitions (chapitres)


def flash(c, t):
    for tc in FLASH:
        if tc - 0.06 <= t <= tc + 0.22:
            a = (1 - abs(t - tc - 0.03) / 0.2) * 0.55
            if a > 0: c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=hexa("#FFFFFF", borne(a))))


def logo_pop(c, t, t0, t1, y=520, larg=430):
    a = prog(t, t0, 0.38, lambda v: rebond(v, 1.7)); o = prog(t, t1, 0.15, entree)
    if a <= 0 or o >= 1: return
    iw, ih = taille_img("logo-dy-blanc"); lh = larg * ih / iw
    c.save(); c.translate(540, y + 6 * math.sin(t * 3)); c.rotate(-3); c.scale(mix(0.4, 1, borne(a)) * a, mix(0.4, 1, borne(a)) * a)
    c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.DropShadow(0, 8, 16, 16, hexa("#000000", 0.6))))
    with Calque(c, borne(a * 2) * (1 - o)):
        image(c, "logo-dy-blanc", -larg / 2, -lh / 2, larg)
    c.restore(); c.restore()


def dessin(c, t):
    flash(c, t)
    # hook : l'argent, puis l'appel à enregistrer
    pastille(c, t, T["d'argent"] - 0.05, 3.25, 540, 1090, "Beaucoup d'argent", "banknote", VERT, rot=-4)
    pastille(c, t, T["enregistre"], 6.95, 540, 1090, "Enregistre la vidéo", "bookmark", OR, rot=3, depuis=1)
    # qui il est
    logo_pop(c, t, T["drop&you"] - 0.05, 8.65, y=1090)
    pastille(c, t, T["fournisseurs"], 11.35, 540, 1090, "Fournisseurs chinois", "factory", ROUGE, rot=-3, depuis=-1)
    # le départ
    pastille(c, t, T["billet"], 13.5, 540, 1090, "Billet pris", "plane", BLEU, rot=-4, check=True)
    pastille(c, t, T["direction"], 14.4, 540, 1090, "Direction la Chine", "plane-takeoff", ROUGE, rot=3, depuis=1)
    # ce qu'il a vu
    pastille(c, t, T["vu"], 16.8, 540, 560, "Vu de mes yeux", "eye", VIOLET, rot=-3)
    pastille(c, t, T["motos"], 18.7, 540, 600, "Motos électriques", "zap", ORANGE, rot=3, depuis=1)
    pastille(c, t, T["cartons"], 21.5, 540, 600, "Cartons de baskets", "package", VERT, rot=-3, depuis=-1)
    # l'offre
    pastille(c, t, T["propose"], 29.4, 540, 470, "Tous ces produits", "shopping-bag", VIOLET, rot=-3)
    liste(c, t, [("À l'unité", "package", OR, T["l'unité"]), ("En lot", "boxes", VERT, T["lot"])], 29.4, 280, 610)
    liste(c, t, [("Montres", "watch", OR, T["montres"]), ("Sacs", "shopping-bag", VIOLET, T["sacs"]), ("Tout", "sparkles", VERT, T2["tout"])],
          32.05, 280, 470)
    pastille(c, t, T2["fournisseurs"], 36.2, 540, 560, "Mes fournisseurs", "users", ROUGE, rot=-3)
    pastille(c, t, T["vends"], 36.2, 540, 680, "Disponibles aussi", "key-round", OR, rot=3, depuis=1, check=True)
    pastille(c, t, T["commentaire"], 38.4, 540, 1090, "Dis-le en commentaire", "message-circle", BLEU, rot=-3)
    # fin
    logo_fin(c, t, T_FIN, y=820)
    bouton_enregistre(c, t, T_FIN + 0.5, DUREE + 1, cy=1060)
    sous_titres(c, t, GS)


# coups de zoom : sur les mots forts et sur les grandes transitions (effet de « punch » à la coupe)
COUPS = [(T["d'argent"], 0.05), (T["enregistre"], 0.04), (T["drop&you"], 0.05), (T["billet"], 0.04), (T2["chine"], 0.05),
         (T["motos"], 0.04), (T["baskets"], 0.04), (T["propose"], 0.04), (T2["tout"], 0.05), (T["vends"], 0.05)] + [(tc, 0.07) for tc in FLASH]
E = Edit(P, P / "media" / "source.mp4", DUREE, dessin, COUPS, centre_zoom=(540, 900))

# bruitages, discrets (la musique porte le rythme)
for tc in COUPES: E.son_(tc - 0.06, "whoosh_court", -24)
for tc in FLASH: E.son_(tc - 0.12, "whoosh", -19); E.son_(tc, "impact_doux", -21)
for t0 in (T["d'argent"] - 0.05, T["enregistre"], T["fournisseurs"], T["billet"], T["vu"], T["motos"], T["cartons"], T["propose"], T2["fournisseurs"], T["commentaire"]):
    E.son_(t0, "pop", -20)
E.son_(T["d'argent"], "ching", -19); E.son_(T["drop&you"] - 0.05, "impact", -20)
for t0 in (T["l'unité"], T["lot"], T["montres"], T["sacs"], T2["tout"]): E.son_(t0, "check", -21)
E.son_(T["vends"], "ching", -19)
E.son_(T_FIN, "whoosh", -18); E.son_(T_FIN + 0.08, "ching", -18); E.son_(T_FIN + 0.95, "clic", -18)


def son():
    """voix Léo (nettoyée, compressée) + musique effacée sous la voix (sidechain) + bruitages, volume final −13 LUFS / −1 dB"""
    a = P / "audio"; a.mkdir(exist_ok=True)
    v = a / "voix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "voix" / "voix.wav"), "-af",
                    "highpass=f=80,equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=10000:t=h:w=0.7:g=1.5,"
                    "acompressor=threshold=0.08:ratio=3:attack=5:release=90:makeup=2",
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_f32le", str(v)], check=True)
    lire = lambda f, extra=(): np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), *extra, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                                            capture_output=True).stdout, np.float32).copy()
    n = int(DUREE * 48000)
    x = lire(v); x *= 10 ** ((-16 - mesure(v)[0]) / 20); x = np.pad(x, (0, max(0, n - len(x))))[:n]
    # musique : posée à −27 LUFS, enveloppe qui descend de 7 dB quand la voix parle, fondu de fin
    if not (P / "media" / "musique.mp3").exists() or "--sans-musique" in sys.argv:
        mu = np.zeros(n, np.float32)
    else:
        mu = lire(P / "media" / "musique.mp3")
    mu = np.pad(mu, (0, max(0, n - len(mu))))[:n]
    tmp = a / "mu.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", str(tmp)], input=mu.astype(np.float32).tobytes(), check=True)
    if mu.any(): mu *= 10 ** ((-25 - mesure(tmp)[0]) / 20)
    env = np.abs(x); win = 4800
    env = np.convolve(env, np.ones(win) / win, mode="same")
    parle = (env > 0.004).astype(np.float32)
    lis = np.convolve(parle, np.ones(9600) / 9600, mode="same")          # 0,2 s d'adoucissement
    gain = 10 ** (-7 * lis / 20)
    fin = np.ones(n, np.float32); i = int((DUREE - 1.2) * 48000); fin[i:] = np.linspace(1, 0, n - i)
    deb = np.ones(n, np.float32); deb[:2400] = np.linspace(0, 1, 2400)
    x = x + mu * gain * fin * deb
    for t0, nomson, g in E.sfx:
        s = lire(SONS / f"{nomson}.wav") * 10 ** (g / 20)
        i0 = int(t0 * 48000); i1 = min(n, i0 + len(s))
        if 0 <= i0 < n: x[i0:i1] += s[:i1 - i0]
    brut = a / "mix-brut.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", str(brut)], input=x.astype(np.float32).tobytes(), check=True)
    mixw = a / "mix.wav"
    g = VOLUME_LUFS - mesure(brut)[0]
    for _ in range(3):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(brut), "-af",
                        f"aresample=192000,volume={g:.2f}dB,alimiter=limit=0.87:attack=0.5:release=40:level=false,"
                        "alimiter=limit=0.87:attack=0.1:release=20:level=false,aresample=48000,pan=stereo|c0=c0|c1=c0",
                        "-c:a", "pcm_s16le", str(mixw)], check=True)
        i_, _ = mesure(mixw)
        if abs(i_ - VOLUME_LUFS) < 0.25: break
        g += VOLUME_LUFS - i_
    (P / "video").mkdir(exist_ok=True)
    out = P / "video" / "DY-M08.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "renders" / "image.mp4"), "-i", str(mixw), "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    return out, mesure(out)


if __name__ == "__main__":
    if sys.argv[1] == "apercu": E.apercu([float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == "video": E.video()
    elif sys.argv[1] == "son": print(son())
