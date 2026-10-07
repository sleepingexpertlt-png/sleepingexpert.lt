# VPS promptas — Merchant Center aktyvių prekių kritimas 617 → 346 (2026-10-05)

## Faktai (patikrinta 2026-10-06 iš šios sesijos)

| Šaltinis | Faktas |
|---|---|
| GMC alert, paskyra 5594987667 | 2026-10-04 23:10 → 10-05 05:10 EEST: Free listings LT ir Shopping ads LT **−43 % (617 → 346)**. Priežastis pagal Google: „items are either expiring within the next 3 days or not available" |
| WooCommerce Store API (viešas, patikrinta pačiam) | svetainėje **~627 matomi produktai** (7 puslapiai × 100, paskutinis 27), **tik 12 outofstock** |
| PROMISES P-076 | dataSource `10626898137` („Content API") = 627 sveikų produktų autoritetinis šaltinis; `merchant_agent.py` cron'as jį pildo |
| hermes_business_metrics | kelios metrikos užšalo ties **2026-09-05 23:07** (avižieniai, kaunas, mažeikiai, be_miesto) — tą dieną VPS'e kažkas sustojo |

**Išvada:** svetainė sveika. Prekės dingsta **Google pusėje**, nes Content API
įrašai turi 30 d. galiojimą ir niekas jų neatnaujina. 10-05 − 30 d. = **09-05**,
ta pati diena, kai užšalo metrikų rašymas. Likusios 346 išnyks per artimiausias
dienas — Google tai rašo tiesiai: „expiring within the next 3 days".

**Verslo pasekmė:** PMax (vienintelis matuojamas kanalas, 2,67 € už maršrutą,
250 maršrutų/mėn) maitinamas iš Merchant Center. Be prekių PMax neturi ko
rodyti. Tai skubiau už viską, kas aptarta reklamos audite.

## Ką daryti VPS sesijoje — tik skaitymas, paskui vienas nedestruktyvus veiksmas

### 1. Patvirtinti diagnozę (skaitymas)
```
crontab -l | grep -i merchant
systemctl list-timers | grep -i merchant
ls -la /root/frontier-agent/logs/ | grep -i merchant
tail -50 /root/frontier-agent/logs/merchant_agent*.log
grep -n "expiration\|expir\|30" /root/frontier-agent/src/agents/merchant_agent.py | head
```
Atsakyti: **kada merchant_agent.py paskutinį kartą sėkmingai pastūmė prekes?**
Jei paskutinis sėkmingas įrašas ≈ 2026-09-05 — diagnozė patvirtinta.

### 2. Patikrinti Merchant API (skaitymas)
Per `merchant_agent.py` turimą OAuth: `products.list` dataSource `10626898137` —
kiek prekių, kiek su `expirationDate` < 2026-10-10. Užrašyti skaičių.

### 3. Atstatyti (vienas veiksmas, nedestruktyvus)
```
python3 /root/frontier-agent/src/agents/merchant_agent.py
```
Tai **perstumia visas 627 prekes** per Content API ir atnaujina jų galiojimą
dar 30 d. Nieko netrina, nieko nekeičia feed'e. Po paleidimo — `products.list`
dar kartą: skaičius turi grįžti į ~617–627.

### 4. Įjungti cron'ą atgal ir užtikrinti, kad nebenumirtų
Jei cron eilutės nėra arba ji užkomentuota — grąžinti. Jei ji yra, bet
nesisuko nuo 09-05 — rasti, kas 09-05 nutiko (tas pats incidentas, kuris
užšaldė metrikų rašymą; žr. metacog/shared_state rašymo logus tą dieną).

## Ko NEDARYTI

- **NEVYKDYTI P-076 / MC-FIX-2026-09-28.** Tas planas liepia IŠTRINTI dataSource
  `10626898137` — būtent tą, kurioje yra 627 sveikos prekės. Blokavimas buvo
  teisingas; dabartinis incidentas tai įrodo.
- Neliesti feed dataSource `10694621223` ir `10574913166`, kol neatsakyta į 1 ir 2.
- Jokių Google Ads pakeitimų.

## Atsiskaitymas (į repo, `docs/veikimo-modelis/02-tikslo-sekimas.md`)

5 eilutės: paskutinio sėkmingo push data | kiek prekių Merchant API prieš |
kiek po | ar cron grąžintas | kas 09-05 sustabdė.

---

## PATAISA 2026-10-07 — 09-05 hipotezė PANEIGTA (VPS faktai)

| Mano prielaida | VPS faktas (tik skaitymas, 2026-10-07 ~06:35) |
|---|---|
| `merchant_agent.py` nestumia nuo 09-05 | `--sync` paskutinis sėkmingas **2026-10-05 05:15:28**, 0 klaidų; 7 savaitiniai paleidimai iš eilės nuo 08-24 |
| Prekės baigia galioti, nes niekas neatnaujina | Feed XML (`generate_shopping_feed.py`) kasdien, paskutinis 10-07 04:15, 625 prekės, HTTP 200 |

Klaida: 10-05 − 30 d. = 09-05 sutapimą su metrikų užšalimu priėmiau kaip
priežastį, nepatikrinęs, ar sync'as apskritai sustojęs. Nebuvo.

**Nauja hipotezė (netikrinta):** savaitinis `--sync` stumia tik pasikeitusias
prekes (delta); Content API galiojimas = paskutinis push + 30 d.; nepakeistos
prekės baigia galioti. 271 nelietos nuo ~09-05 → išnyko 10-05.

**Testas (VPS, skaitymas):**
1. `merchant_agent.py` — full ar delta? ar nustato `expirationDate`?
2. Merchant API `productstatuses.list`: kiek `expirationDate` < 2026-10-10,
   kokie `itemLevelIssues` ant išmestųjų.
3. Jei delta — pilnas re-push visų 627.

**Atskiri gedimai iš VPS ataskaitos:**
- Merchant Monitor išjungtas nuo 2026-07-08 — MC būsenos niekas nestebi.
- VPS nemato šakos `claude/llamamaps-suggestions-opportunities-m1b2tr`
  (origin'e yra, 6b70a58). Tikrinti `git remote -v`, fetch refspec.
- WordPress posts turinio REST atnaujinimai tyliai neišsisaugo (L2026-10-07-1).
- 10 VPS commit'ų nepushinta.
