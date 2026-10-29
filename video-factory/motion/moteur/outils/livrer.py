#!/usr/bin/env python3
"""Livre une vidéo finie sur Telegram, en fichier, sans perte de qualité.

Deux destinations, choisies toutes seules d'après le nom du projet :

- **AC-…** → le canal « Tiktok » partagé avec l'associé qui publie @recto_cerveau.
- **tout le reste** (DA-, DY-, CB-, MQ-, GSX-, clients) → la **conversation privée
  avec le bot média**, parce que l'associé n'a rien à faire de ces vidéos-là.

    cd video-factory/motion/AC-M02
    /usr/bin/python3 ../moteur/outils/livrer.py video/AC-M02.mp4 --legende "AC-M02 · ..."

**La qualité d'origine, toujours, quelle que soit la route.** Deux cas, choisis tout seuls :

- **≤ 49 Mo → en FICHIER dans le canal** (`sendDocument`). Jamais `sendVideo` : Telegram
  ré-encode tout ce qui part en vidéo. En document, l'octet envoyé est l'octet reçu, et le
  fichier se range quand même dans la galerie du téléphone.
- **> 49 Mo → un LIEN dans le canal.** L'API des bots plafonne à 50 Mo ; au-delà le master
  est déposé sur le VPS et le bot poste son adresse. Le téléchargement rend le fichier
  d'origine, octet pour octet. L'URL porte un jeton aléatoire et le dossier n'a pas d'index.
  Il faut avoir lancé **une fois** `outils/installer-livraisons.sh`.

Le script ne recompresse **jamais** de lui-même : une vidéo livrée l'est en qualité maximale.

Le jeton du bot ne quitte pas le VPS : tout passe par lui, et le fichier temporaire est effacé.
"""
import argparse, hashlib, json, pathlib, secrets, shlex, subprocess, sys

VPS = "root@108.61.187.118"
CANAL = "-1003764863983"            # « Tiktok » — capté le 28/10/2026, AC- UNIQUEMENT
BOT = "8113650676"                  # conversation privée de Youssef avec le bot média
ENV = "/opt/media-bot/.env"         # porte TELEGRAM_BOT_TOKEN
DOSSIER = "/srv/livraisons"
HOTE = "https://videos.108-61-187-118.sslip.io"
LIMITE = 49 * 1024 * 1024           # marge sous les 50 Mo de l'API


def ou(canal):
    """nom lisible de la destination, pour les messages"""
    return "le canal « Tiktok »" if str(canal) == CANAL else "le bot (privé)"


def destination(fichier, choix):
    """Le canal partagé est réservé aux vidéos AC- (@recto_cerveau).

    Tout le reste — DA-, DY-, CB-, MQ-, GSX-, clients — part dans la conversation
    privée avec le bot. L'associé qui lit le canal n'a rien à faire des autres marques,
    et une vidéo postée là peut finir sur la mauvaise chaîne.
    """
    if choix:                                   # --canal explicite : on obéit
        return choix
    nom = fichier.stem.upper()
    parent = fichier.parent.name.upper()
    if nom.startswith("AC-") or parent.startswith("AC-"):
        return CANAL
    return BOT


def ssh(cmd):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", VPS, cmd],
                          capture_output=True, text=True)


def duree(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        s = float(r.stdout.strip())
        return f"{int(s // 60)}'{int(s % 60):02d}"
    except ValueError:
        return "?"


def empreinte(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for bloc in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def telegram(methode, champs, fichier=None):
    """appelle l'API depuis le VPS, pour que le jeton n'en sorte pas"""
    args = " ".join(f"-F {shlex.quote(k)}={shlex.quote(v)}" for k, v in champs.items())
    if fichier:
        args += f" -F document=@{shlex.quote(fichier)}"
    cmd = (f'set -a; . {ENV}; set +a; curl -s {args} '
           f'"https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/{methode}"')
    r = ssh(cmd)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f"réponse illisible de Telegram : {r.stdout[:300]} {r.stderr[:300]}")


def en_fichier(f, legende, canal):
    dist = f"/tmp/{f.name}"
    print("→ copie vers le VPS…")
    if subprocess.run(["scp", "-o", "BatchMode=yes", str(f), f"{VPS}:{dist}"]).returncode:
        sys.exit("copie vers le VPS échouée")
    print(f"→ envoi vers {ou(canal)}, en fichier (qualité intacte)…")
    d = telegram("sendDocument", {"chat_id": canal, "caption": legende,
                                  "disable_content_type_detection": "true"}, dist)
    ssh(f"rm -f {shlex.quote(dist)}")
    if not d.get("ok"):
        sys.exit(f"Telegram refuse : {d.get('description')}")
    doc = d["result"].get("document", {})
    recu = doc.get("file_size", 0)
    print(f"✓ livré en fichier : {doc.get('file_name')} — {recu/1048576:.1f} Mo")
    if recu != f.stat().st_size:
        print("⚠ la taille reçue diffère de la taille envoyée — à vérifier")


def en_lien(f, legende, canal):
    r = ssh(f"test -d {shlex.quote(DOSSIER)} && echo oui || echo non")
    if "oui" not in r.stdout:
        sys.exit(f"{DOSSIER} n'existe pas sur le VPS.\n"
                 f"Lancer une fois : bash ../moteur/outils/installer-livraisons.sh")
    jeton = secrets.token_urlsafe(9)
    dest = f"{DOSSIER}/{jeton}"
    ssh(f"mkdir -p {shlex.quote(dest)}")
    print(f"→ dépôt du master sur le VPS ({f.stat().st_size/1048576:.1f} Mo)…")
    if subprocess.run(["scp", "-o", "BatchMode=yes", str(f),
                       f"{VPS}:{dest}/{f.name}"]).returncode:
        sys.exit("copie vers le VPS échouée")
    ssh(f"chmod -R a+rX {shlex.quote(dest)}")

    local = empreinte(f)
    r = ssh(f"sha256sum {shlex.quote(dest + '/' + f.name)} | cut -d' ' -f1")
    distant = r.stdout.strip()
    if distant and distant != local:
        sys.exit("l'empreinte du fichier déposé ne correspond pas — copie à refaire")
    print(f"✓ empreinte identique ({local[:16]}…)")

    url = f"{HOTE}/{jeton}/{f.name}"
    r = ssh(f'curl -s -o /dev/null -w "%{{http_code}}" -I {shlex.quote(url)}')
    if r.stdout.strip() not in ("200", "204"):
        print(f"⚠ le lien répond {r.stdout.strip()} — vérifier Caddy")

    texte = (f"{legende}\n\n"
             f"⬇️ Fichier d'origine ({f.stat().st_size/1048576:.0f} Mo, trop gros pour "
             f"partir en pièce jointe Telegram) :\n{url}\n\n"
             f"À poster tel quel, sans repasser par CapCut.")
    d = telegram("sendMessage", {"chat_id": canal, "text": texte,
                                 "disable_web_page_preview": "true"})
    if not d.get("ok"):
        sys.exit(f"Telegram refuse : {d.get('description')}")
    print(f"✓ lien posté vers {ou(canal)} : {url}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--legende", default=None)
    ap.add_argument("--canal", default=None,
                    help="identifiant de destination ; par défaut le canal pour les AC-, "
                         "le bot privé pour tout le reste")
    ap.add_argument("--bot", action="store_true",
                    help="forcer la conversation privée avec le bot")
    ap.add_argument("--lien", action="store_true",
                    help="forcer le lien même sous 49 Mo")
    a = ap.parse_args()

    f = pathlib.Path(a.fichier).resolve()
    if not f.exists():
        sys.exit(f"introuvable : {f}")
    canal = BOT if a.bot else destination(f, a.canal)
    taille = f.stat().st_size
    legende = a.legende or f"{f.stem} · {duree(f)}"
    print(f"{f.name} — {taille/1048576:.1f} Mo, {duree(f)} → {ou(canal)}")

    if a.lien or taille > LIMITE:
        en_lien(f, legende, canal)
    else:
        en_fichier(f, legende, canal)


if __name__ == "__main__":
    main()
