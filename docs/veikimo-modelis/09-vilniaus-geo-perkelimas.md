# Vilniaus reklamos perkėlimas į Pilaitę ir Centrą — 2026-09-19

Savininko sprendimas: tvarkom.

## Pagrindas (6 mėn. WooCommerce pašto kodų duomenys, 27 Vilniaus užsakymai, 20 779 €)

| Zona | Užsak. | Apyvarta | Vid. čekis | % apyvartos |
|---|---|---|---|---|
| Centras / Naujamiestis | 4 | 5 627 € | **1 407 €** | 27,1 % |
| Justiniškės / Pašilaičiai | 2 | 1 900 € | 950 € | 9,1 % |
| **Pilaitė** | 8 | 7 075 € | 884 € | **34,0 %** |
| Lazdynai | 3 | 2 156 € | 719 € | 10,4 % |
| Šnipiškės / Žirmūnai / Verkiai | 6 | 3 386 € | **564 €** | 16,3 % |
| Vilniaus rajonas | 2 | 573 € | 286 € | 2,8 % |

Pilaitės pašto kodai duomenyse: 0411x, 0413x, 1130x, 1132x, 1134x
Centro pašto kodai duomenyse: 0016x, 0210x, 0310x, 0313x

## KĄ KEISTI

**Kampanija: `SE — Vilnius čiužiniai + lovos [always-on]`, ID 23941125495**

Dabar: 171,97 € / 30 d. (5,73 €/d), 127 klikai, **0 išmatuotų konversijų**,
taikymas — visas Vilnius tolygiai.

Keisti: geo taikymą į Pilaitę + Centrą/Naujamiestį. Biudžetas nesikeičia.
Tai didžiausios vienos kampanijos Vilniaus išlaidos ir jos rezultatas nematuojamas,
todėl rizika perkeliant yra mažiausia visoje paskyroje.

## KO NELIESTI — svarbu

**PMax-4, ID 23231305809 — geo NEKEISTI.**

Ji aptarnauja ir Vilnių (69,47 €, 76 veiksmai), ir **Klaipėdą (21,01 €, 73 veiksmai
po 0,29 €)**. Klaipėdos 0,29 € yra geriausias rodiklis visoje paskyroje.
Susiaurinus PMax-4 iki Pilaitės ir Centro, Klaipėda dingtų.

Tai spąstai, į kuriuos būtų lengva įlipti vykdant „perkelkim Vilnių į Pilaitę".

## Ko tikėtis

Zonų vidutiniai čekiai: Pilaitė 884 €, Centras 1 407 €, prie parduotuvės 564 €.
Tas pats reklamos euras turėtų atnešti 1,6–2,5 karto didesnį pirkinį.

**Bet mastas mažas.** Visa Vilniaus vietos reklama yra ~83 €/mėn.
Tai tvarkymasis, ne augimas. Spraga iki 83 000 € lieka 58 186 €.

## Vykdymas

Šioje sesijoje neįvykdyta: `hermes_ads_mutate` neprieinamas, Windsor uždraustas (K19).
Vykdyti per VPS `google_ads_agent.py` arba Google Ads sąsajoje.
Radiuso taškus geriausia rinkti sąsajoje, kur matomas žemėlapis.

Po pakeitimo matuoti 14 d.: ar Vilniaus vidutinis čekis pakilo virš 770 €.

---

## 2026-09-19 — RASTA TIKROJI PRIEŽASTIS

Nuskaityta iš paskyros (Porter `google_ads.campaign_criterion_list`, read veikia):

```
campaign 23941125495  type: PROXIMITY  criterionId: 2492543513932
geoPoint: 54.6872, 25.2797
radius: 30 KILOMETERS
```

**Kampanija vardu „Vilnius" taikoma 30 km spinduliu.** Tai Vilnius plius Trakai,
Lentvaris, Grigiškės, Nemenčinė, Rūdiškės ir visas Vilniaus rajono kaimas.
Todėl 171,97 €/mėn. ir 0 išmatuotų konversijų.

Sutampa su pašto kodų duomenimis: Vilniaus rajonas (14xxx) = 286 € čekis,
blogiausias, 2,8 % apyvartos.

Kiti kriterijai toje kampanijoje: kalbos en/lt/pl/ru, 3 įrenginiai,
4 neigiami raktažodžiai (jysk, dormeo, bikuva, ikea lovos). Miesto lygio
LOCATION kriterijų nėra — tik šis vienas spindulys.

### Pataisa (savininkas patvirtino 2026-09-19)

**30 km → 10 km, tas pats centras 54.6872, 25.2797.**

10 km padengia visus Vilniaus rajonus: Pilaitė 6,4 km, Fabijoniškės 5,8 km,
Lazdynai, Justiniškės, Centras. Nukerta tik 10–30 km žiedą.

### Vykdymo būklė: NEĮVYKDYTA

| Kelias | Būklė |
|---|---|
| Porter read | ✅ veikia (taip ir rasta priežastis) |
| Porter write | 🔴 `NO_BALANCE` — kreditų nėra |
| Hermès `hermes_ads_mutate` | 🔴 sesijoje neprieinamas |
| Windsor | 🔴 savininko išjungtas 2026-09-19 |

Tvarka, jei vykdoma per API: **pirma sukurti 10 km, tik tada šalinti 30 km**,
kad kampanija neliktų be taikymo (be jokio geo kriterijaus ji rodytųsi visur).

Senojo kriterijaus duomenys atstatymui: `customers/7015063449/campaignCriteria/23941125495~2492543513932`,
54.6872 / 25.2797 / 30 km.

Sąsajoje tai vienas laukelis.
