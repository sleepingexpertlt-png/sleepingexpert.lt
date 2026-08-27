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

---

## RADINYS 2026-08-27: lokacijų puslapiai = AI srauto ir maršrutų sankirta

Po `aeo_reverse_discovery.py` substring bug'o fix'o (commit 349cf5e6) gavom
švarius GA4 duomenis: **172 realios AI sesijos / 28 d.** (ne 684).

Pasiskirstymas per puslapio tipą (125 klasifikuotų sesijų):

| Tipas | Sesijos | Puslapių | **Sesijų / puslapį** |
|---|---|---|---|
| **Lokacijos** | 40 (32 %) | **3** | **13,3** |
| Blogas/gidai | 12 (9,6 %) | 3 | 4,0 |
| Kategorijos | 18 (14,4 %) | 6 | 3,0 |
| Produktai | 42 (33,6 %) | 17 | 2,5 |

**Lokacijų puslapiai 5× efektyvesni už produktų puslapius.**

### Kodėl tai keičia prioritetus

Pagrindinis tikslas = maršrutai į salonus. AI srautas ateina būtent į
lokacijų puslapius. Tai ta pati piltuvo vieta — vadinasi AEO darbas maitina
NE tik antrinį tikslą (raktažodžiai), bet tiesiogiai pirminį (maršrutai),
per lokacijų puslapius.

Iki šiol tie 3 puslapiai nebuvo nė karto optimizuoti. Jie traukia trečdalį AI
srauto atsitiktinai.

Vilnius: mažiausi maršrutai (6), didžiausios impresijos (329). AI atveda —
žmogus nepaspaudžia maršruto. Konversijos problema tiksliai ten, kur turim
daugiausiai svertų.

### Naujas turinio prioritetas

1. **3 lokacijų puslapiai** (buvo neprioritetas) — pirminis tikslas
2. 1 bangos blog puslapiai — antrinis tikslas
3. Kategorijos — antrinis

Ką lokacijų puslapiuose tikrinti: ar maršruto mygtukas matomas be scroll'o,
ar yra darbo laikas/telefonas/adresas struktūruotai, LocalBusiness JSON-LD,
ar yra atsakymai į „ką galiu išbandyti vietoje", ar yra nuoroda į GBP profilį,
ar puslapis atsako į klausimą, su kuriuo AI žmogų atsiuntė.
