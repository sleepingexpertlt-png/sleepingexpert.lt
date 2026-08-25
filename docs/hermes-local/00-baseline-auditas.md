# Hermès Local — Baseline auditas (2026-08-25)

Tikslas: prieš siūlant paslaugą kitiems (Llamamaps partnerystė), pastatyti visą local
visibility sistemą ant savų 3 parduotuvių ir įrodyti, kad ji veikia.

## Parduotuvės (NAP atskaitos taškas)

| Parduotuvė | Adresas | Pastabos |
|---|---|---|
| Vilnius | PC Baldų Rojus, Kalvarijų g. 125, 3 a. | I–VII 10:00–20:00 |
| Klaipėda | PC Helios Galeria, Taikos pr. 56, 1 a. | I–VII 10:00–20:00 |
| Ukmergė | Kauno g. 9 | atidaryta 2026-05 |

Telefonas: +370 630 70001 · El. paštas: info@sleepingexpert.lt

## Kas JAU veikia (tiesioginė GMB API integracija — Windsor nereikalingas)

Šaltinis: hermes_cag + hermes_status, 2026-08-25.

- **3 lokacijos prijungtos tiesiogiai** per GBP API (account 112003996596356655394;
  location ID žr. `reference_gmb_posts_api.md` Hermès atmintyje).
- **Postai automatizuoti:** `src/agents/blog_agent.py` (6c) kryžmina blog įrašus į GBP;
  `gbp_post_publisher.py` skelbia akcijas pagal `data/frontier.db` (`gbp_post_schedule`),
  su dedup apsauga ir taisykle „OFFER tik su nuotrauka".
- **Reitingo ženkliukas + AggregateRating schema** svetainėje (Snippet #187) iš realių
  GBP atsiliepimų (4.8/5, 118 atsiliepimų).
- **Insights** naudojami savaitinėms peržiūroms (salon_signal: directions/calls/impressions
  per store), bet analizė nepilnai automatizuota.

## Salon signal baseline (7 d., 2026-08-25)

| Lokacija | Impressions | Directions | Calls | Konversija imp→dir |
|---|---|---|---|---|
| Vilnius | 604 | 5 | 0 | 0.8 % ⚠️ |
| Klaipėda | 312 | 13 | 1 | 4.2 % ✅ |
| Ukmergė | 420 | 0 | 0 | **0 %** 🔴 |

✅ **IŠSPRĘSTA (VPS patikra 2026-08-25):** Ukmergės „0 directions" buvo pasenęs
snapshot'as, NE realybė ir NE kodo bug'as. `gmb_agent.py` location ID traukia
gyvai iš API (jokių hardcode), live užklausa rodė **UKM = 13 directions /
424 impressions (7 d.)** iš teisingo ID 2791954715091405702. Liekamoji patikra:
kitas salon_signal cron turi parodyti ~13; jei vėl rodys 0 — bug'as snapshot
rašytuve, ne GBP.
⚠️ Vilnius konvertuoja 5× prasčiau nei Klaipėda — žinoma priežastis kandidatė:
P-064 (OPEN) — Vilniaus GBP kategorijos rodomos lenkiškai, keisti per GBP UI.
Pastaba: skambučiai NE KPI pagal G2 sprendimą (R-028) — nenaudoti kaip alarmo.

## Kas jau žinoma (vieši duomenys)

- Google atsiliepimai: bent vienas GBP įrašas turi **5.0★ / 25 atsiliepimai** (šaltinis:
  Google paieška, 2026-08-25). Reikia patikslinti pasiskirstymą tarp 3 lokacijų.
- Svetainė jau turi lokacijų puslapius, pvz. `/locations/sleeping-expert-klaipeda/` —
  geras pagrindas local landing strategijai.
- Baldų Rojus salono puslapis (baldurojus.lt/salonas/sleeping-expert/) — citata,
  kurią reikia įtraukti į NAP nuoseklumo patikrą.

## Spragos ir blokeriai

GBP prieiga TURIMA tiesiogiai (Windsor nereikalingas). Likusios spragos:

| # | Spraga | Sprendimas |
|---|---|---|
| 1 | 🔴 Ukmergės profilio dublikatas + 0 directions | Pašalinti/sujungti dublikatą per GBP, patikrinti pagrindinio profilio pilnumą |
| 2 | Atsakymai į atsiliepimus neautomatizuoti | Review Agent (skeleton: gbp-review-agent MCP, žr. 02 failą) per esamą OAuth |
| 3 | Geo-grid duomenų šaltinio nėra | GBP Rank Tracker (nemokamas) arba mcp-google-map |
| 4 | Nuotraukų kėlimas rankinis; Q&A API nebeveikia (tik rankiniu) | Photos — per GBP media API iš WP medijos; Q&A — rankinė SOP |
| 5 | Insights analizė nepilnai automatizuota | Visibility Agent: savaitinis salon_signal → trend ataskaita |
| 6 | AI share-of-voice nematuojamas | `ai-visibility` skill baseline |
| 7 | (Duomenų įrankiai) Windsor Free limitas ir Ahrefs planas blokuoja GSC/keyword API šioje aplinkoje | GSC duomenis imti per Hermès tiesiogiai; Windsor/Ahrefs nebekritiniai |

## Baseline metrikos, kurias reikia užfiksuoti PRIEŠ optimizavimą

1. Kiekvienos lokacijos GBP: reitingas, atsiliepimų skaičius, nuotraukų skaičius,
   postų dažnis, užpildytų laukų pilnumas (%).
2. Geo-grid pozicijos: „čiužiniai", „čiužinių parduotuvė", „lovos" — 5×5 grid
   Vilniuje/Klaipėdoje, 3×3 Ukmergėje.
3. GSC local užklausų clicks/impressions/position (90 d.).
4. AI share-of-voice: ar ChatGPT/Gemini/Perplexity rekomenduoja Sleeping Expert
   klausiant „geriausia čiužinių parduotuvė Vilniuje/Klaipėdoje" (žr. `ai-visibility` skill).
