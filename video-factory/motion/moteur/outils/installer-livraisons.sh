#!/bin/bash
# Ouvre la livraison par lien pour les vidéos RECTO CERVEAU de plus de 50 Mo.
# À lancer UNE SEULE FOIS, depuis le Mac :
#     bash video-factory/motion/moteur/outils/installer-livraisons.sh
#
# Ce que ça fait sur le VPS (108.61.187.118) :
#   1. crée /srv/livraisons, qui ne contiendra que les masters à télécharger ;
#   2. ajoute UN hôte à Caddy — videos.108-61-187-118.sslip.io — qui sert ce dossier
#      en HTTPS, sans index : on n'atteint un fichier que par son URL exacte, et
#      chaque URL porte un jeton aléatoire que `livrer.py` génère ;
#   3. valide la configuration AVANT de recharger, et restaure la sauvegarde si la
#      validation échoue. Rien d'autre n'est touché : les sites DROP&YOU, ChinaBook,
#      Maison Drop et CHINA FACTORY gardent leurs blocs tels quels.
set -euo pipefail
VPS=root@108.61.187.118

ssh "$VPS" 'bash -s' <<'DISTANT'
set -euo pipefail
mkdir -p /srv/livraisons
chown mediabot:mediabot /srv/livraisons
chmod 755 /srv/livraisons

if grep -q "videos.108-61-187-118.sslip.io" /etc/caddy/Caddyfile; then
  echo "L'hote de livraison existe deja, rien a faire."
  exit 0
fi

cp /etc/caddy/Caddyfile "/etc/caddy/Caddyfile.avant-livraisons-$(date +%Y%m%d-%H%M)"
cat >> /etc/caddy/Caddyfile <<'BLOC'

# Livraisons video RECTO CERVEAU (28/10/2026). Les masters depassent les 50 Mo que
# l'API Telegram des bots accepte : le bot poste un lien dans le canal, le fichier
# part d'ici en qualite d'origine, octet pour octet. Aucun index : on n'atteint un
# fichier que par son URL exacte, qui porte un jeton aleatoire.
videos.108-61-187-118.sslip.io {
	root * /srv/livraisons
	file_server
	header {
		Strict-Transport-Security "max-age=31536000"
		X-Content-Type-Options nosniff
		Content-Disposition attachment
	}
}
BLOC

if ! caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/dev/null 2>&1; then
  echo "Configuration refusee par Caddy : je remets la sauvegarde." >&2
  cp "$(ls -t /etc/caddy/Caddyfile.avant-livraisons-* | head -1)" /etc/caddy/Caddyfile
  exit 1
fi

systemctl reload caddy
sleep 4
echo ok > /srv/livraisons/.ping
code=$(curl -s -o /dev/null -w "%{http_code}" "https://videos.108-61-187-118.sslip.io/.ping" || true)
rm -f /srv/livraisons/.ping
if [ "$code" = "200" ]; then
  echo "Livraison par lien en service : https://videos.108-61-187-118.sslip.io/"
else
  echo "L'hote repond $code — le certificat met parfois une minute a sortir, relancer le test."
fi
DISTANT
