# Matavimo protokolas — kada galima sakyti „krenta"

Priežastis: 2026-08-27 visą dieną teigiau „maršrutai krenta −6 %".
Realiai tai buvo 08-26 vakarinio ir 08-27 rytinio matavimo atimtis
7 dienų slenkančiame lange. Neįrodyta. K10 pažeidimas skaičiams.

## Taisyklės

**M1. Fiksuotas laikas.** Maršrutai (`salon_signal`) fiksuojami kartą per
parą, **07:30 vietos laiku**, iš to paties šaltinio. Kitu paros metu paimtas
skaičius į eilutę nerašomas — tik informacijai.

**M2. Snapshot senumas rodomas visada.** Cituojant skaičių privaloma
nurodyti `last_updated`. Jei senesnis nei 30 val. — skaičius negalioja
sprendimams.

**M3. Trendas reikalauja 7 taškų.** Jokio „krenta" / „auga" / „%" teiginio,
kol nėra 7 dienų iš eilės tuo pačiu laiku. Iki tol tik: „šiandien X,
bazė Y, imtis per maža išvadai".

**M4. 7 d. slenkantis langas ≠ paros rodiklis.** `directions_7d` keitimasis
per parą yra vienos dienos įėjimas minus vienos dienos išėjimas. ±3 čia yra
normalus svyravimas, ne signalas.

**M5. Bazė užšaldyta.** Bazė = 34 (2026-08-26). Ji nekeičiama ir
neperskaičiuojama. Tikslas = 44 iki 2026-10-24.

## Eilutė (pildoma tik 07:30 matavimais)

| Data | Laikas | Klaipėda | Ukmergė | Vilnius | Viso | WC 7d | Snapshot amžius |
|---|---|---|---|---|---|---|---|
| 08-26 | — | 13 | 13 | 8 | 34 | 11 | bazė |
| 08-27 | 07:20 | 13 | 13 | 6 | 32 | 8 | 0,2 val. |

Išvada apie trendą galima nuo **09-02** (7 taškai).

## M6 — GBP duomenų vėlavimas (rasta 2026-09-03 per Porter)

Google Business Profile Performance API duomenys **atsilieka ir paskutinės
dienos grąžinamos kaip 0**, kol Google jų neužpildo. Porter, `coverageUntil
2026-09-02`, rodo 08-30 → 09-02 = **0 impresijų, 0 maršrutų visuose trijuose
salonuose**. Gyvas profilis su 90 atsiliepimų negali turėti 0 impresijų 4 d.

Mūsų `gmb_agent` skaito TĄ PATĮ šaltinį → `salon_signal` 7 d. langas
įskaičiuoja neužpildytas dienas. **Todėl 34 → 17 → 7 „kritimas" bent iš
dalies yra vėlavimas, ne realybė.**

Taisyklė: **maršrutų / impresijų eilutei naudoti tik dienas iki
`coverageUntil − 3 d.`** Paskutinės 3 dienos — nerodomos, kol neužpildytos.

Dieninė eilutė (Porter, Google Business Profile Performance):

| Data | Vilnius imp. | Klaipėda imp. | Ukmergė imp. |
|---|---|---|---|
| 08-24 | 160 | 106 | 100 |
| 08-25 | 146 | 88 | 83 |
| 08-26 | 117 | 64 | 68 |
| **08-27** | **32** | **17** | **7** |
| 08-28 | 23 | 25 | 16 |
| 08-29 | 8 | 2 | 9 |
| 08-30 → 09-02 | 0 | 0 | 0 |

08-27 kritimas gali būti tikras (tą dieną redaguotas profilis, kitą dieną
sustabdyta reklama) ARBA dalinis užpildymas. **Atskirti galima tik
perklausus 09-06:** jei 08-30 → 09-02 užsipildo — vėlavimas; jei lieka 0 —
realu.

Lokacijų ID (Porter / GBP API):
Vilnius `11855115537711521704` · Klaipėda `18399011255848825016` ·
Ukmergė `2791954715091405702`.

## M6 testas 2026-09-06 — rezultatas

Porter perklausta 09-06 06:00 (`coverageUntil 2026-09-05`). Palyginimas su
09-03 traukimu:

| Data | 09-03 traukimas | 09-06 traukimas | Išvada |
|---|---|---|---|
| 08-29 | 8 / 2 / 9 | **28 / 22 / 16** | užsipildė |
| 08-30 | 0 / 0 / 0 | **26 / 12 / 7** | užsipildė |
| 08-31 | 0 / 0 / 0 | **25 / 17 / 10** | užsipildė |
| 09-01 | 0 / 0 / 0 | **26 / 22 / 10** | užsipildė |
| 09-02 → 09-05 | — | 0 / 0 / 0 | dar neužpildyta |

(Vilnius / Klaipėda / Ukmergė, impresijos.)

**Išvada 1 — M6 patvirtinta, bet vėlavimas ~5 d., ne 3.** Taisyklė
keičiama: eilutei naudoti tik dienas iki **`coverageUntil − 5 d.`**

**Išvada 2 — kritimas nuo 08-27 REALUS ir tęsiasi.** Užpildytos dienos rodo
~25 / ~17 / ~10 impresijų per dieną prieš ~130 / ~80 / ~85 iki 08-26.
Tai **−80 %** šešias dienas iš eilės (08-27 → 09-01). Maršrutai per tas
šešias dienas: **1** (Klaipėda 08-29). Reklama grįžo 09-01 — 09-01
impresijos nepakilo.

**Išvada 3 — priežastis sisteminė, ne vietinė.** Trys nepriklausomos
lokacijos krito tą pačią dieną tuo pačiu dydžiu. Tai ne konkurencija ir ne
vienas profilis. Kandidatai: (a) 08-27 profilių redagavimas, jei lietė visas
tris; (b) „Google atnaujino jūsų atributus" — Google pats keitė atributus apie
08-27 (matyta profilio paste'e); (c) Google pusės pokytis Performance API
metrikoje. Neatskirta.

Pagal 09-03 užsirašytą kriterijų: **liko 0 → realu → avarija.** Nulinių
dienų nebeliko, bet lygis −80 % išsilaikė šešias dienas — kriterijaus esmė
išpildyta.

### M6 papildymas 2026-09-06 — profilių patikra per GBP API (skaitymas, be pakeitimų)

Tikrinta `hermes_gbp_request` (Business Information API v1), visos 3 lokacijos.

| Faktas | Vilnius | Klaipėda | Ukmergė |
|---|---|---|---|
| Adresas / openInfo | yra, OPEN | yra, OPEN | yra, OPEN |
| Pagr. kategorija | mattress_store | mattress_store | mattress_store |
| Paslaugų sritis | **Lietuva, Latvija, Estija (3 valstybės)** | 9 vietovės aplink Klaipėdą | 7 vietovės aplink Ukmergę |
| Profilio kalba | pl | en | en |
| latlng | yra | yra | negrąžinta |

Išvados:
- Nė viename profilyje nėra pakeitimo, kuris paaiškintų vienalaikį 08-27 kritimą visose trijose lokacijose. Priežastis lieka nenustatyta ir sisteminė (ne profilio).
- API artefaktas: `serviceArea.businessType` grąžina `CUSTOMER_LOCATION_ONLY`, kai readMask be `storefrontAddress`, ir `CUSTOMER_AND_BUSINESS_LOCATION`, kai su. Adresas realiai yra. Ne signalas.
- Vilniaus paslaugų sritis (3 valstybės) skiriasi nuo kitų dviejų (miestų lygis). Savininkas 08-28 nurodė, kad tai pačio Google pasiūlymas. Kritimas prasidėjo 08-27, t. y. anksčiau — todėl NE priežastis. Įrašyta kaip stebėjimas, be siūlymo keisti.
- 09-04 VPS cron (feed_label diagnostika) rezultato Telegram sraute nėra (72 val.: tik 3 blog + 2 system žinutės). Reikia VPS relay.
