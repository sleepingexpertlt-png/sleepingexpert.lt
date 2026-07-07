# Cloudflare Tunnel „hermes" — Hermes MCP serveriui

Named Cloudflare tunelis, publikuojantis Hermes MCP serverį adresu
`https://api.sleepingexpert.lt/mcp` su Bearer token autentifikacija.

## Architektūra

```
Internetas ──HTTPS──> Cloudflare ──tunelis──> cloudflared (serveryje)
                                                 │
                                                 ▼
                                   mcp-auth-proxy (127.0.0.1:9130)
                                   tikrina Authorization: Bearer <token>
                                                 │
                                                 ▼
                                   Hermes MCP (127.0.0.1:HERMES_PORT)
```

## Diegimas (viena komanda)

Serveryje, kuriame veikia Hermes MCP:

```bash
git pull
cd deploy/cloudflared-hermes
sudo HERMES_PORT=8000 bash setup.sh   # pakeiskite 8000 į tikrą Hermes MCP portą
```

Skriptas atlieka visus žingsnius:

1. **`cloudflared tunnel login`** — terminale parodys URL; atidarykite jį
   naršyklėje, pasirinkite zoną `sleepingexpert.lt` ir patvirtinkite.
2. **`cloudflared tunnel create hermes`** — sukuria named tunelį.
3. **config.yml** — `api.sleepingexpert.lt` → `localhost:9130` (auth proxy)
   → `localhost:$HERMES_PORT`. Įrašoma į `/etc/cloudflared/config.yml`.
4. **DNS** — `cloudflared tunnel route dns --overwrite-dns hermes
   api.sleepingexpert.lt`. `--overwrite-dns` būtinas, nes
   `api.sleepingexpert.lt` šiuo metu jau turi A įrašą (72.61.139.213) —
   jis bus pakeistas CNAME į tunelį.
5. **systemd** — `cloudflared-hermes.service` ir `mcp-auth-proxy.service`
   įjungiami su `enable --now`, tad pakyla po serverio perkrovimo.
6. **Bearer tokenas** — sugeneruojamas (`openssl rand -hex 32`), įrašomas į
   `/etc/hermes-mcp/proxy.env` ir parodomas skripto pabaigoje.
7. **Patikra** — `curl` be tokeno (laukiama 401) ir su tokenu.

## Patikra rankiniu būdu

```bash
# be tokeno — 401 Unauthorized:
curl -I https://api.sleepingexpert.lt/mcp

# su tokenu — atsako Hermes MCP (200/405/406 priklausomai nuo metodo):
curl -I -H "Authorization: Bearer <TOKENAS>" https://api.sleepingexpert.lt/mcp
```

Pastaba: `curl -I` siunčia HEAD užklausą — dalis MCP serverių į ją atsako
405/406. Tai normalu; svarbu, kad be tokeno gaunate 401, o su tokenu — ne 401.

## MCP kliento konfigūracija

```json
{
  "mcpServers": {
    "hermes": {
      "type": "http",
      "url": "https://api.sleepingexpert.lt/mcp",
      "headers": {
        "Authorization": "Bearer <TOKENAS>"
      }
    }
  }
}
```

## Valdymas

```bash
systemctl status cloudflared-hermes mcp-auth-proxy   # būsena
journalctl -u cloudflared-hermes -f                  # tunelio logai
journalctl -u mcp-auth-proxy -f                      # auth proxy logai
sudo systemctl restart cloudflared-hermes            # perkrauti tunelį
cat /etc/hermes-mcp/proxy.env                        # tokenas ir portai
```

Norint pakeisti Hermes MCP portą vėliau: redaguokite `UPSTREAM_PORT`
faile `/etc/hermes-mcp/proxy.env` ir `sudo systemctl restart mcp-auth-proxy`.

## Saugumas

- Auth proxy ir Hermes MCP klauso tik `127.0.0.1` — iš išorės pasiekiami
  tik per Cloudflare tunelį.
- Tokenas laikomas `/etc/hermes-mcp/proxy.env` (chmod 600) — **niekada
  nekomitinkite jo į git**.
- Tunelio kredencialai: `/etc/cloudflared/hermes.json` (chmod 600) — taip
  pat ne į git.
