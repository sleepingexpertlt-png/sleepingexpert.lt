# Infrastruktūros planas — kaip išnaudoti tai, ką jau turime

Būklė 2026-09-04. Nieko naujo nepirkti. Perskirstyti darbus tarp turimų resursų.

---

## 1. Ką turime

| Resursas | Specifikacija | Dabar | Problema |
|---|---|---|---|
| **VPS KVM 4** (srv1138253, 72.61.139.213, Vilnius) | 4 vCPU, 16 GB RAM, 200 GB | 5 Next.js svetainės + visas Hermès stack'as + ClickHouse + Letta | RAM ~10 GB užimta, swap 7 GB 95 % pilnas, diske liko 28 GB. Be rezervo |
| **Cloud Enterprise v1** (hPanel, pagrindinis domenas cookking.online) | 6 CPU, 12 GB RAM, 300 GB NVMe | Tuščias | Neišnaudotas. Palaiko PHP/WordPress, MySQL, **Node.js apps (Deploy Web App)**, cron, SSH be root |
| **GPU instancijos** (hPanel) | Pagal poreikį, valandinis tarifas | Nenaudojama | Reikalinga tik konkretiems darbams, ne 24/7 |
| **Hidra klasteris** (4 namų PC, Ollama) | Be dedikuotų GPU | 0 iš 4 mazgų prisijungę | Faktiškai neveikia |
| **API** (Gemini, Claude, DeepSeek, NVIDIA NIM, Groq) | Tokenai | Pagrindinė inferencija | Periodiški 402/403, kreditai baigiasi |
| **Cloudflare** | Nemokamas planas | Tik sleepingexpert.lt | lamele, marsalas, cookking eina tiesiai į VPS IP |

---

## 2. Tikslinis išdėstymas

```
Cloud Enterprise (12 GB / 6 CPU / 300 GB)        VPS KVM 4 (16 GB / 4 vCPU)
─────────────────────────────────────────        ─────────────────────────────
lamele.lt         Next.js (Deploy Web App)        frontier-agent      :5000
marsalas.lt       Next.js (Deploy Web App)        rag-api             :5001
cookking.online   Next.js (Deploy Web App)        dashboard-api       :5002
+ 2 kiti Next.js procesai                         hermes-chat         :5003
sleepingexpert.lt WordPress (jei dar ne čia)      hermes-radar        :5004
worker.sleepingexpert.lt  Node.js tiltas          hermes-mcp          :8765
MySQL             bendra DB                       claw_telegram_bot
/backups          VPS atsarginės kopijos          ClickHouse, Letta
hPanel cron       suplanuoti HTTP darbai          nginx tik subdomenams
                                                  (hermes., os., mcp., n8n., api.)

GPU instancija (on-demand, valandomis)
──────────────────────────────────────
Ollama + bge-m3 / Flux / Whisper  →  įjungiama darbui, išjungiama po jo
```

Principas: **svetainės, kurios uždirba, gyvena atskirai nuo agentų, kurie eksperimentuoja.**

---

## 3. Fazės

### Fazė 0 — apsauga (šiandien, 0 rizikos)

1. hPanel → VPS → Snapshots & Backups → **sukurti snapshot**.
2. VPS'e išmatuoti, kas kiek užima (skaičiai reikalingi Fazei 1):
   ```bash
   pm2 list
   ps -eo rss,comm,args --sort=-rss | head -25
   du -sh ~/.pm2/logs
   sudo bash scripts/swap-diagnose.sh
   ```
3. PM2 procesams uždėti ribą, kad restartuotųsi patys, o ne OOM-killer:
   ```bash
   pm2 restart lamele   --max-memory-restart 700M
   pm2 restart marsalas --max-memory-restart 300M
   pm2 install pm2-logrotate
   pm2 save
   ```
4. ClickHouse apriboti (pagal nutylėjimą pasiima iki 90 % RAM):
   ```bash
   sudo tee /etc/clickhouse-server/config.d/memory.xml >/dev/null <<'EOF'
   <clickhouse>
     <max_server_memory_usage>2000000000</max_server_memory_usage>
     <mark_cache_size>268435456</mark_cache_size>
     <uncompressed_cache_size>268435456</uncompressed_cache_size>
   </clickhouse>
   EOF
   sudo systemctl restart clickhouse-server
   ```
5. Nužudyti paliktas `claude` sesijas tmux'e (Hostinger patikroje jos matomos kaip RAM vartotojai).
6. Patikrinti, kad vidiniai portai neklauso viešai:
   ```bash
   ss -tlnp | grep -vE '127.0.0.1|::1'    # 5000-5004 ir 8765 turi būti tik localhost
   ```

### Fazė 1 — svetainės į Cloud Enterprise (ši savaitė)

Tvarka nuo mažiausios rizikos. Kiekvienai svetainei tas pats ciklas:
**deploy → testas laikinu URL → DNS → tik tada `pm2 delete`.**

| # | Svetainė | Kodėl tokia tvarka | DNS keitimas |
|---|---|---|---|
| 1 | marsalas.lt | Mažiausia (75 MB), jei nepavyks, niekas nenukentės | Išorinis registratorius → A įrašas į Cloud IP |
| 2 | cookking.online | Jau yra Cloud plano pagrindinis domenas | Hostinger DNS zonoje |
| 3 | lamele.lt | Didžiausias laimėjimas (940 MB) | Hostinger DNS |
| 4 | Kiti 2 Next.js | Identifikuoti per `pm2 list` / `ps` | Pagal domeną |

Žingsniai hPanel'e: **Websites → Add Website → Deploy Web App → Import Git Repository** → repo + branch → Environment variables (nukopijuoti iš VPS `.env`) → Deploy. Build output gula į `/home/{user}/domains/{domain}/nodejs`.

Pastabos:
- Jei hPanel'e nėra „Deploy Web App" / „Node.js Apps", vienintelis klausimas Hostinger agentui: *„įjunkite Node.js apps mano Cloud Enterprise v1 planui"*. Dokumentacija sako, kad visi Cloud planai tai palaiko.
- **cookking.online užsakymų JSON**: redeploy gali perrašyti app katalogą. Prieš DNS keitimą: sukurti testinį užsakymą → redeploy → patikrinti, ar failas išliko. Jei ne, JSON laikyti už app katalogo ribų arba perkelti į plano MySQL.
- Hostinger Next.js pavyzdys su teisinga konfigūracija: https://github.com/hostinger/deploy-nextjs
- Po kiekvieno perkėlimo VPS'e: `pm2 delete <app>`, pašalinti nginx server bloką, `pm2 save`, `sudo nginx -t && sudo systemctl reload nginx`.

Laukiamas rezultatas: VPS atsilaisvina **mažiausiai 1 GB RAM** (išmatuota: lamele + marsalas), realiai 1,5–2,5 GB su visais penkiais procesais. Swap nustoja būti kritinis.

### Fazė 2 — atsarginės kopijos į 300 GB (iškart po Fazės 1)

Cloud Enterprise SSH prieiga + rsync iš VPS, kasdien per cron:

```bash
# VPS'e, /etc/cron.daily/backup-to-cloud (chmod +x)
#!/usr/bin/env bash
set -euo pipefail
DEST='uXXXXXX@<cloud-ssh-host>:/home/uXXXXXX/backups/vps'   # iš hPanel → SSH Access
PORT=65002                                                   # Hostinger SSH portas
rsync -az --delete -e "ssh -p $PORT" \
  /etc/nginx /etc/systemd/system /root/.pm2 \
  /root/frontier-agent/.env /root/rag-api/.env \
  "$DEST/config/"
clickhouse-client -q "BACKUP DATABASE default TO Disk('backups', 'ch-$(date +%F).zip')" || true
pg_dump letta | gzip > /tmp/letta-$(date +%F).sql.gz && rsync -az -e "ssh -p $PORT" /tmp/letta-*.sql.gz "$DEST/db/"
```

Kelius ir vartotoją pasitikslinti VPS'e. Tikslas: serverį galima atstatyti iš kopijos per valandą.

### Fazė 3 — tiltas: darbai iš VPS į Cloud Enterprise CPU (po mažu)

Hosting'o branduolių VPS procesams tiesiogiai naudoti negalima (nėra root, systemd, Python demonų). Bet galima **perduoti darbą per HTTP**: Cloud'e veikia viena Node.js app'ą, VPS agentai ją kviečia.

```
frontier-agent (VPS)  ──POST /jobs/<name>──▶  worker.sleepingexpert.lt (Cloud, Node.js)
                      ◀── JSON rezultatas ──   auth: X-Worker-Token iš .env
hPanel cron           ──GET  /jobs/<name>──▶  (suplanuoti darbai, VPS nedalyvauja)
```

Kas tinka tiltui (stateless, CPU sunkus, Node): paveikslėlių apdorojimas (sharp, WebP), sitemap/RSS generavimas, WooCommerce REST sinchronizacija, scraping'as (fetch + cheerio), LLM API kvietimai, kurie tik laukia atsakymo.

Kas netinka: ClickHouse, Letta, lokalūs embeddings, viskas, kas Python demonas.

Pirmas žingsnis: vienas izoliuotas darbas (blogo paveikslėlių apdorojimas), 50 eilučių endpoint'as, vienas pakeistas kvietimas frontier-agent'e. Veikia savaitę → kitas darbas.

### Fazė 4 — GPU pagal poreikį (kai Fazės 1–2 baigtos)

GPU 24/7 neapsimoka. GPU valandomis apsimoka konkretiems darbams:

| Darbas | Kodėl GPU | Įvertis valandų |
|---|---|---|
| Zilliz embeddings perskaičiavimas su bge-m3 | MiniLM 384 dim lietuviškam RAG silpnas; CPU užtruktų valandas | 1–2 val. per atnaujinimą |
| Blogo paveikslėlių generavimas (Flux/SDXL) | Pexels uždraustas, API paveikslėliai kainuoja už vienetą | kelios val./mėn. partijomis |
| Whisper transkripcijos video | YouTube pipeline'ui tekstai ir subtitrai | pagal video kiekį |
| Atsarginis LLM (qwen/glm per Ollama) | Kai API grąžina 402/403 | tik incidentų metu |

`llm_router.py` Ollama endpoint'ą jau palaiko (buvo skirtas Hidra klasteriui): pakeisti adresą iš namų PC tunelio į GPU instancijos IP. Ilgainiui frontier-agent gali pats įjungti instanciją per Hostinger API, kai susikaupia eilė, ir išjungti po valandos tylos.

Pirmas bandymas: įjungti → perskaičiuoti Zilliz embeddings su bge-m3 → išjungti → pažiūrėti sąskaitą ir RAG kokybę. Tai ir bus sprendimas, ką daryti su neveikiančiu Hidra klasteriu.

---

## 4. Sprendimų vartai

| Po fazės | Klausimas | Jei taip | Jei ne |
|---|---|---|---|
| 1 | VPS `free -h` available > 4 GB ir swap < 50 %? | Fazė 2 | Ieškoti kito RAM vartotojo (`ps --sort=-rss`), tikrinti ClickHouse ir Letta |
| 2 | Atstatymas iš kopijos į švarų katalogą suveikia? | Fazė 3 | Taisyti backup skriptą, ne eiti toliau |
| 3 | Pirmas tilto darbas veikia savaitę be klaidų? | Kitas darbas | Palikti tą vieną, netempti |
| 4 | GPU valandų sąskaita < API sutaupymo + kokybė geresnė? | Įtraukti į pipeline | Likti prie API |

---

## 5. Ko nedaryti

- Nekelti VPS plano, kol neperkeltos svetainės. Tai užmaskuoja problemą, o ne sprendžia.
- Nekurti naujų serverių. Turimų pakanka.
- Ne `swapoff -a`. Žr. `swap-runbook.md`.
- Nedaryti dviejų perkėlimų vienu metu. Po vieną, su DNS patikra tarp jų.
- Nejungti GPU instancijos „kad būtų". Tik su konkrečiu darbu ir išjungimu po jo.

## Šaltiniai

- Hostinger Node.js hosting options: https://www.hostinger.com/support/node-js-hosting-options-at-hostinger/
- Deploy a Node.js web app: https://www.hostinger.com/support/how-to-deploy-a-nodejs-website-in-hostinger/
- Node.js app docs: https://docs.hostinger.com/node.js/creating-an-app
- GPU instancijos: https://www.hostinger.com/support/how-to-set-up-a-gpu-instance-at-hostinger/
