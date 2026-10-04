# Nepriklausoma patikra kitam AI — Sleeping Expert strategija

**Užduotis:** patikrinti žemiau esančius teiginius NEPASITIKINT jais. Kiekvienam
teiginiui — išorinis įrodymas arba „NEPATVIRTINTA". Vidiniai self-report'ai
(agentų žinutės, dokumentai repo) NĖRA įrodymas. Atsakymas — lentelė:
`teiginys | šaltinis, kurį pats atidarei | PATVIRTINTA / PANEIGTA / NEPATIKRINAMA | skaičius`.

## Teiginiai, kuriuos reikia patikrinti

| # | Teiginys | Kaip patikrinti |
|---|---|---|
| 1 | Apyvarta 30 d. 2026-10-04 = 39 805,89 €, 44 užsakymai; 2026-09-29 = 48 004 €, 50 užs. | WC REST `GET /wp-json/wc/v3/orders?after=…&status=completed,processing` — susumuoti pačiam, abiem langams |
| 2 | Salono AOV krito 1 034,58 € → 944,30 € (−8,7 %) | tas pats, filtruojant pagal store meta lauką |
| 3 | GBP maršrutai 7 d. = 76 (VLN 34 / KLP 26 / UKM 16); 09-28 buvo 63 | GBP Performance API `fetchMultiDailyMetricsTimeSeries`, BUSINESS_DIRECTION_REQUESTS, abiem langams. DĖMESIO: maršrutai backfill'inami 7–10 d., todėl naujausios dienos neužpildytos |
| 4 | Google Ads 7015063449: nėra NĖ VIENOS pirkimo konversijos; visos 4 — Local actions / Clicks to call | GAQL `SELECT conversion_action.name, conversion_action.category FROM conversion_action` |
| 5 | PMax 30 d.: 667,48 € → 250 maršrutų (2,67 €); Search 774,15 € → 5 | GAQL per `campaign.advertising_channel_type`, `metrics.cost_micros`, `metrics.conversions` su `segments.conversion_action_name='Local actions - Directions'`, langas 2026-08-14→09-13 IR šviežias 30 d. langas |
| 6 | Search kampanijos neturi location assets | GAQL `campaign_asset` WHERE `asset.type=LOCATION` — kiek Search kampanijų turi |
| 7 | Kampanija 23941125495 turi proximity 30 km nuo 54,6872/25,2797 | GAQL `campaign_criterion` WHERE `campaign.id=23941125495 AND campaign_criterion.type=PROXIMITY` |
| 8 | 4 asset grupės INELIGIBLE (Image quality); 1 — Destination not working (Helios Klaipėda) | GAQL `asset_group_asset` su `policy_summary` / UI Policy manager. Nustatyti TIKRĄ sulūžusį URL |
| 9 | Ukmergė PMax (23941982295): 10,31 € už maršrutą | GAQL kaip #5, tik ši kampanija |
| 10 | PMax-2 (22773843568) ir PMax-3 (23085196755) yra PAUSED nuo 2026-09-18 | GAQL `campaign.status`, `change_event` nuo 09-17 |
| 11 | Automated promotions paskyros lygmeniu = ON (Google auto opt-in nuo 10-12) | UI: Settings → Account settings → Automated assets. API neeksponuoja — PATIKRINTI, ar tai tiesa |
| 12 | Svetainėje ~47 produktai `on_sale=true`, iš jų tik 2 su tikra nuolaida | `GET /wp-json/wc/store/products?on_sale=true&per_page=100` — suskaičiuoti `regular_price != sale_price` |
| 13 | Hermès OAuth paskyra neturi prieigos prie customer 7015063449 (U-003) | PROMISES.md U-003 + realus `customer.list_accessible_customers` kvietimas |

## Strateginiai klausimai, į kuriuos verifikatorius turi atsakyti savarankiškai

A. Ar metrika, kurios 86 % (255/296) nuperkama už reklamą ir kuri per 6 d. pakilo
   +20,6 %, kol apyvarta krito −17,1 %, gali būti North Star? Jei ne — kokią
   siūlai vietoj jos, remdamasis TIK duomenimis, kuriuos pats ištraukei?
B. Ar 774 €/mėn Search be location assets ir be pirkimo konversijos reikia
   (a) pjauti, (b) palikti, (c) pirma padaryti matuojamą? Pagrįsk.
C. Ukmergė: 16 maršrutų/sav. → 3 užsakymai/mėn po 409 €. Pardavimo, lokacijos
   ar matavimo problema? Kokį vieną testą darytum per 14 d.?
D. Kiek iš −8 198 € kritimo yra kalendorius (rugpjūčio pabaiga = PEAK, iškrito
   iš 30 d. lango)? Suskaičiuok iš dienos eilutės, ne spėk.

## Ko NEDARYTI

- Nesiūlyti kelti biudžeto (owner sprendimas 2026-07-30).
- Nenaudoti Ahrefs, Windsor (owner draudimas).
- Nerašyti į Google Ads be owner patvirtinimo per `.claude/state/approved.json`.
- Neskaityti „0" kaip nulio, jei metrika be timestamp arba backfill lange.
