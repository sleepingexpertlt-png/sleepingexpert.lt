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
