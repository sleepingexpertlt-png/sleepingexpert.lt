# VPS prompt 2026-09-14 — PMax konsolidacija (išlaidų optimizavimas be biudžeto kėlimo)

Vykdyk tiesiogiai per `src/agents/google_ads_agent.py`, customer **7015063449**.
Porter nenaudojamas (K18).

## Kodėl

Trys bendros „Local store visits and promotions" PMax kampanijos dubliuoja viena
kitą **tuose pačiuose miestuose**, o PMax-4 ten 3–4 kartus pigesnė. Duomenys
2026-08-14 → 2026-09-13, kaina už lokalų veiksmą:

| Miestas | PMax-4 | Konkuruojanti | Skirtumas |
|---|---|---|---|
| Klaipėda | **0,29 €** | PMax-3 — 1,12 € | PMax-4 3,9× pigiau |
| Vilnius | **0,91 €** | PMax-2 — 2,70 € | PMax-4 3,0× pigiau |

PMax-3 86 % savo biudžeto leidžia Klaipėdoje, PMax-2 — Vilniuje. Abu miestus
PMax-4 jau dengia ir dengia geriau. **Stabdymas geografinės skylės nepalieka.**

## Ką padaryti

1. Sustabdyk (status PAUSED, NE remove):
   - `customers/7015063449/campaigns/23085196755` — Local store visits and promotions-Performance Max-3
   - `customers/7015063449/campaigns/22773843568` — Local store visits and promotions-Performance Max-2

2. Sužinok PMax-4 biudžeto resource name:
   ```
   SELECT campaign.id, campaign.name, campaign_budget.resource_name,
          campaign_budget.amount_micros
   FROM campaign
   WHERE campaign.id = 23231305809
   ```

3. Padidink to biudžeto `amount_micros` lygiai **3,45 € per dieną**
   (= 3450000 micros) prie dabartinės reikšmės. Tai lygiai tiek, kiek atlaisvina
   sustabdytos kampanijos (103,42 € / 30 d.).

**Bendros paskyros išlaidos nesikeičia.** Tai perskirstymas, ne biudžeto kėlimas
(savininko 2026-07-30 sprendimas galioja).

## Laukiamas rezultatas

Tie patys 103,42 € per mėnesį:

| | Dabar (PMax-2 + PMax-3) | PMax-4 tempu |
|---|---|---|
| Lokalūs veiksmai | 79 | ~127 |
| Maršrutai | 17 | ~50 |

Grynas pokytis prie to paties biudžeto: **+48 veiksmai, +33 maršrutai per mėnesį.**

## Rizikos, kurias fiksuoju iš anksto

1. Pakėlus PMax-4 biudžetą ji trumpam grįžta į mokymosi fazę. Galimas 3–7 dienų
   rezultato svyravimas. Tai normalu, nestabdyk dėl to.
2. PMax-2 imtis maža (5 veiksmai). Bet jos suma 17,39 €/mėn., tad klaidos kaina
   nedidelė.
3. PMax-4 geografijoje yra „Unknown" 58,62 € su 40 veiksmų. Geo priskyrimas
   nepilnas, todėl skaičiai kryptingi, ne tikslūs iki cento.

## Ko NEDARYTI

Neliesk Search kampanijų. Jų rezultatas **nematuojamas** (paskyroje nėra pirkimo
konversijos, o lokalių veiksmų jos negali generuoti be location assets). Jų
paieškos terminai patikrinti — jie komerciniai ir tinkami („čiužiniai 180x200",
„lova su čiužiniu", „kontinentinė lova"). Pjauti jas aklai reikštų pjauti
pardavimus, kurių niekas nefiksuoja.

## Atsakymo formatas

1. Ar abi kampanijos sustabdytos (patvirtink statusą GAQL užklausa).
2. Koks buvo ir koks tapo PMax-4 biudžetas.
3. Jei kas nepavyko — kokia tiksli klaida.
