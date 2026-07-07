#!/usr/bin/env bash
# Įdiegia TIK Bearer auth proxy (be cloudflared) — naudoti, kai tunelis
# sukurtas per Cloudflare Zero Trust puslapį (dashboard-managed tunnel).
#
#   sudo HERMES_PORT=8000 bash proxy-only.sh
#
set -euo pipefail

HERMES_PORT="${HERMES_PORT:-8000}"
PROXY_PORT=9130
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p /opt/hermes-mcp /etc/hermes-mcp
install -m 755 "$SRC_DIR/mcp-auth-proxy.py" /opt/hermes-mcp/mcp-auth-proxy.py

if [ -f /etc/hermes-mcp/proxy.env ] && [ -z "${MCP_AUTH_TOKEN:-}" ]; then
  MCP_AUTH_TOKEN=$(grep '^MCP_AUTH_TOKEN=' /etc/hermes-mcp/proxy.env | cut -d= -f2)
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

install -m 644 "$SRC_DIR/mcp-auth-proxy.service" /etc/systemd/system/mcp-auth-proxy.service
systemctl daemon-reload
systemctl enable --now mcp-auth-proxy.service

echo ""
echo "==> Auth proxy veikia: 127.0.0.1:${PROXY_PORT} -> 127.0.0.1:${HERMES_PORT}"
echo "==> Bearer tokenas: ${MCP_AUTH_TOKEN}"
echo "==> Cloudflare tunelio Public Hostname nukreipkite i: http://localhost:${PROXY_PORT}"
