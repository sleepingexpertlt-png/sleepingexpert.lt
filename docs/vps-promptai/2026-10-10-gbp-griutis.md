# VPS promptas — GBP signalas sugriuvo 95 % (2026-10-10). Priežastis, ne spėjimas.

## Faktai (hermes_status, snapshot 2026-10-10 07:20)

| 7 d. | 10-04 | 10-06 | 10-10 |
|---|---|---|---|
| Maršrutai | 76 | 52 | **4** (KLP 3 / UKM 1 / VLN 0) |
| Impresijos KLP/VLN/UKM | 1512/814/269 | 1106/829/220 | **39/39/30** |

Langai 10-06 ir 10-10 persidengia 4 dienomis — tos dienos negali atgaline
data netekti ~700 impresijų. Trys salonai nukrito į beveik vienodą skaičių.
Tai arba pipeline'o langas, arba Google pusė. Savininkas sako: „GBP sugriuvo".

## Tą pačią dieną — 10-04 — sustojo keli dalykai (hermes_agents / telegram_feed)

| Kas | Paskutinis veikimas |
|---|---|
| `merchant_monitor` | 2026-10-04 06:38 |
| `blog_scheduler` | 2026-10-04 14:34 |
| `blog_agent` | 2026-10-04 17:23 |
| Telegram feed DB (ta, kurią skaito MCP) | 2026-10-04 20:23 |

Botas Telegram'e rašo (savininkas mato daug „Metacognition" klaidų), bet MCP
`hermes_telegram_feed` rodo 0 žinučių, o `hermes_synergy` — 0 klaidų per 24 h.
**Stebėjimo sluoksnis skaito negyvas lenteles nuo 10-04.** Kas 10-04 keista VPS'e?

## Užduotys — tik skaitymas, atsakymai skaičiais

### 1. GBP — ar profiliai gyvi (Business Information API)
Kiekvienam iš 3 salonų (Vilnius `locations/11855115537711521704`, Klaipėda, Ukmergė — ID iš `gbp` config):
```
GET https://mybusinessverifications.googleapis.com/v1/locations/{id}/VoiceOfMerchantState
GET https://mybusinessbusinessinformation.googleapis.com/v1/locations/{id}?readMask=name,title,metadata,openInfo
```
Atsakyti: `hasVoiceOfMerchant`, `complyWithGuidelines` (= suspensija), `verify`, `openInfo.status`.
Jei `complyWithGuidelines` užpildytas — profilis **suspenduotas**, tai ir yra priežastis.

### 2. GBP Performance API — diskriminuojantis testas
```
fetchMultiDailyMetricsTimeSeries dailyMetrics=BUSINESS_IMPRESSIONS_MOBILE_MAPS,BUSINESS_IMPRESSIONS_DESKTOP_MAPS,BUSINESS_IMPRESSIONS_MOBILE_SEARCH,BUSINESS_IMPRESSIONS_DESKTOP_SEARCH,BUSINESS_DIRECTION_REQUESTS
dailyRange 2026-09-29 → 2026-10-06, visiems 3 salonams
```
Jei grąžina ~1106/829/220 → **pipeline'o langas sulūžęs** (tikrinti `gbp_snapshot` skripto datų logiką — ar nenuslinko į ateitį po 10-04 pakeitimų).
Jei grąžina ~39 arba 403 → **Google pusė** → 1 punktas atsako kodėl.

### 3. Google Ads — ar reklama rodoma
`python3 /root/frontier-agent/src/agents/google_ads_agent.py` skaitymo režimu arba GAQL:
```
SELECT campaign.name, campaign.status, metrics.impressions, metrics.cost_micros
FROM campaign WHERE segments.date BETWEEN '2026-10-03' AND '2026-10-09'
```
Jei impresijos ≈ 0 nuo kurios nors dienos → reklama sustojo (billing? suspensija?). Tai paaiškintų −77…−89 %, bet ne vienodus 39/39/30.

### 4. Kas pakeista 10-04
```
crontab -l > /tmp/cron_now.txt; ls -la /var/spool/cron/crontabs/ ; journalctl --since "2026-10-04" --until "2026-10-05" | grep -iE "cron|systemd.*(stop|fail)" | head -40
cd /root/frontier-agent && git log --since=2026-10-04 --until=2026-10-05 --stat | head -80
```
Atsakyti: kuris pakeitimas 10-04 nutraukė telegram feed DB rašymą, merchant_monitor, blog_scheduler.

### 5. Merchant Center (iš 10-06/10-07 prompto, dar neatsakyta)
`merchant_agent --sync` — full ar delta? `productstatuses.list`: kiek prekių dabar aktyvios (buvo 346)?

## Ko NEDARYTI
Nieko nerašyti į GBP, Ads, Merchant Center. Tik skaityti. Atsakymai į
`docs/veikimo-modelis/02-tikslo-sekimas.md` arba Telegram savininkui.
