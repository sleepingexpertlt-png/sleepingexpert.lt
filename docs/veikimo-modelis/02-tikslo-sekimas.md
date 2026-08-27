# Tikslo sekimas (atnaujinama kas patikrinimą)

Tikslas: maršrutai +30 % bent 2/3 salonų iki 2026-10-24. Bazė 34 → tikslas 44.

| Data | Klaipėda | Ukmergė | Vilnius | Viso | WC 7d | Pastaba |
|---|---|---|---|---|---|---|
| 08-26 (bazė) | 13 | 13 | 8 | **34** | 11 | ciklo startas |
| 08-27 | 13 | 13 | **6** | **32** | 8 | −6 % nuo bazės; Vilnius −25 % |
| tikslas | 17 | 17 | 10 | **44** | — | 10-24 |

## Matavimo sluoksnis — ATGAIVINTAS ✅

Gemini rakto fix'as (08-26) atstatė ne tik pipeline, bet ir matavimą:

| Metrika | 08-26 | 08-27 | |
|---|---|---|---|
| `traffic_snapshot_age_hours` | 48.5 (mirę) | **0.5** | ✅ matuoja vėl |
| `gsc_avg_position` | 8.2 | **7.6** | ✅ |
| `gsc_clicks_24h` | 43 | **60** | ✅ +40 % |
| `gsc_impressions_24h` | 1674 | **1843** | ✅ |
| `gsc_ctr` | 2.57 % | **3.26 %** | ✅ |
| blog pipeline | 2× error, q=0 | **1 draft** | ✅ gamina |

## Ką tai reiškia (be gražinimo)

Techninis sluoksnis atsigavo. **Verslo skaičius juda ne ta kryptimi:**
maršrutai −6 %, Vilnius −25 % (8→6), WC užsakymai 11→8.

Vilnius: **daugiausia impresijų (329 vs 260 vs 192), mažiausiai maršrutų.**
Žmonės profilį mato, bet nespaudžia maršruto. Tai konversijos, ne matomumo
problema — ir tiksliai atitinka P-064 (kategorija lenkiškai): profilis
pasirodo, bet neatrodo kaip tai, ko žmogus ieškojo.

Dviejų dienų imtis per maža išvadai apie trendą, bet Vilniaus atotrūkis
(impresijos aukščiausios, maršrutai žemiausi) yra struktūrinis, ne
triukšmas — jis matėsi ir 08-26.

## Sinergijos silpnoji vieta (hermes_synergy, 08-26)

- `metacog_to_actions` = **0.3** — „7 klaidos, nė vieno circuit breaker".
  Sistema mato savo klaidas, bet nereaguoja. Tai tiksliai tai, kas įvyko
  per Gemini gedimą: 8 val. tylos.
- `traits`: `10_sinergija` ↓ (vienintelis krentantis iš 11).
- `cag_to_master` = 0.49 — orchestratoriaus rezultatai vidutiniai.

Stiprūs: `radar_to_metacog` 1.0, `agents_to_business` 1.0 (474 agentų
paleidimai → 43 clicks).
