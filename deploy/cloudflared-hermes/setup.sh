#!/usr/bin/env bash
# Cloudflare named tunnel "hermes" diegimas Hermes MCP serveriui.
# Paleisti SERVERYJE, kuriame veikia Hermes MCP (kaip root arba su sudo):
#
#   sudo HERMES_PORT=8000 bash setup.sh
#
# Kintamieji (visi nebūtini):
#   HERMES_PORT     - portas, kuriuo klauso Hermes MCP (numatyta: 8000)
#   MCP_AUTH_TOKEN  - Bearer tokenas (numatyta: sugeneruojamas naujas)
#   HOSTNAME_FQDN   - viešas hostas (numatyta: api.sleepingexpert.lt)
set -euo pipefail

HERMES_PORT="${HERMES_PORT:-8000}"
HOSTNAME_FQDN="${HOSTNAME_FQDN:-api.sleepingexpert.lt}"
PROXY_PORT=9130
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() { echo -e "\n\033[1;32m==> $*\033[0m"; }

# ---------------------------------------------------------------- 0. cloudflared
if ! command -v cloudflared >/dev/null 2>&1; then
  log "Diegiamas cloudflared"
  ARCH=$(uname -m)
  case "$ARCH" in
    x86_64)  CF_ARCH=amd64 ;;
    aarch64) CF_ARCH=arm64 ;;
    *) echo "Nepalaikoma architektūra: $ARCH"; exit 1 ;;
  esac
  curl -fsSL -o /usr/local/bin/cloudflared \
    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${CF_ARCH}"
  chmod +x /usr/local/bin/cloudflared
fi
CLOUDFLARED=$(command -v cloudflared)

# ---------------------------------------------------------------- 1. login
if [ ! -f "$HOME/.cloudflared/cert.pem" ] && [ ! -f /etc/cloudflared/cert.pem ]; then
  log "Cloudflare autorizacija — atidarykite naršyklėje parodytą URL"
  "$CLOUDFLARED" tunnel login
fi

# ---------------------------------------------------------------- 2. create hermes
if ! "$CLOUDFLARED" tunnel list 2>/dev/null | awk '{print $2}' | grep -qx hermes; then
  log "Kuriamas tunelis 'hermes'"
  "$CLOUDFLARED" tunnel create hermes
else
  log "Tunelis 'hermes' jau egzistuoja — naudojamas esamas"
fi
TUNNEL_ID=$("$CLOUDFLARED" tunnel list | awk '$2=="hermes"{print $1}')
if [ -z "$TUNNEL_ID" ]; then
  echo "KLAIDA: nepavyko nustatyti tunelio ID"; exit 1
fi
log "Tunelio ID: $TUNNEL_ID"

# ---------------------------------------------------------------- 3. config.yml
log "Rašoma /etc/cloudflared/config.yml (hostname ${HOSTNAME_FQDN} -> localhost:${PROXY_PORT} -> localhost:${HERMES_PORT})"
mkdir -p /etc/cloudflared
CRED_SRC=$(ls "$HOME"/.cloudflared/"$TUNNEL_ID".json 2>/dev/null || true)
if [ -n "$CRED_SRC" ]; then
  cp "$CRED_SRC" /etc/cloudflared/hermes.json
  chmod 600 /etc/cloudflared/hermes.json
fi
if [ -f "$HOME/.cloudflared/cert.pem" ] && [ ! -f /etc/cloudflared/cert.pem ]; then
  cp "$HOME/.cloudflared/cert.pem" /etc/cloudflared/cert.pem
fi
sed "s/__TUNNEL_ID__/$TUNNEL_ID/" "$SRC_DIR/config.yml" > /etc/cloudflared/config.yml

# ---------------------------------------------------------------- 4. DNS
log "DNS: ${HOSTNAME_FQDN} -> ${TUNNEL_ID}.cfargotunnel.com"
# --overwrite-dns būtinas, nes api.sleepingexpert.lt jau turi A įrašą
"$CLOUDFLARED" tunnel route dns --overwrite-dns hermes "$HOSTNAME_FQDN"

# ---------------------------------------------------------------- 6. Bearer auth proxy
log "Diegiamas Bearer auth proxy (portas ${PROXY_PORT})"
mkdir -p /opt/hermes-mcp /etc/hermes-mcp
install -m 755 "$SRC_DIR/mcp-auth-proxy.py" /opt/hermes-mcp/mcp-auth-proxy.py

if [ -f /etc/hermes-mcp/proxy.env ] && [ -z "${MCP_AUTH_TOKEN:-}" ]; then
  # jau yra tokenas — nekeičiam
  MCP_AUTH_TOKEN=$(grep '^MCP_AUTH_TOKEN=' /etc/hermes-mcp/proxy.env | cut -d= -f2)
  log "Naudojamas esamas tokenas iš /etc/hermes-mcp/proxy.env"
else
  MCP_AUTH_TOKEN="${MCP_AUTH_TOKEN:-$(openssl rand -hex 32)}"
fi
cat > /etc/hermes-mcp/proxy.env <<EOF
MCP_AUTH_TOKEN=${MCP_AUTH_TOKEN}
LISTEN_HOST=127.0.0.1
LISTEN_PORT=${PROXY_PORT}
UPSTREAM_HOST=127.0.0.1
UPSTREAM_PORT=${HERMES_PORT}
EOF
chmod 600 /etc/hermes-mcp/proxy.env

# ---------------------------------------------------------------- 5. systemd
log "Diegiami systemd servisai"
install -m 644 "$SRC_DIR/mcp-auth-proxy.service" /etc/systemd/system/mcp-auth-proxy.service
install -m 644 "$SRC_DIR/cloudflared-hermes.service" /etc/systemd/system/cloudflared-hermes.service
sed -i "s|^ExecStart=/usr/local/bin/cloudflared|ExecStart=${CLOUDFLARED}|" /etc/systemd/system/cloudflared-hermes.service
systemctl daemon-reload
systemctl enable --now mcp-auth-proxy.service
systemctl enable --now cloudflared-hermes.service

# ---------------------------------------------------------------- 7. patikra
log "Laukiama, kol tunelis pakils (10 s)…"
sleep 10
echo "--- be tokeno (turi būti 401):"
curl -sS -o /dev/null -w "HTTP %{http_code}\n" "https://${HOSTNAME_FQDN}/mcp" || true
echo "--- su tokenu:"
curl -sS -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Authorization: Bearer ${MCP_AUTH_TOKEN}" "https://${HOSTNAME_FQDN}/mcp" || true

log "BAIGTA"
echo    "  Viešas adresas : https://${HOSTNAME_FQDN}/mcp"
echo    "  Bearer tokenas : ${MCP_AUTH_TOKEN}"
echo    "  Tokeno vieta   : /etc/hermes-mcp/proxy.env"
echo    "  Statusas       : systemctl status cloudflared-hermes mcp-auth-proxy"
