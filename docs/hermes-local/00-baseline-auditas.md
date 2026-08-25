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

## Kas jau žinoma (vieši duomenys)

- Google atsiliepimai: bent vienas GBP įrašas turi **5.0★ / 25 atsiliepimai** (šaltinis:
  Google paieška, 2026-08-25). Reikia patikslinti pasiskirstymą tarp 3 lokacijų.
- Svetainė jau turi lokacijų puslapius, pvz. `/locations/sleeping-expert-klaipeda/` —
  geras pagrindas local landing strategijai.
- Baldų Rojus salono puslapis (baldurojus.lt/salonas/sleeping-expert/) — citata,
  kurią reikia įtraukti į NAP nuoseklumo patikrą.

## Blokeriai (reikia owner'io veiksmo)

| # | Blokeris | Sprendimas |
|---|---|---|
| 1 | **Windsor: `google_my_business` connector NEprijungtas** — be jo nėra GBP postų/atsiliepimų automatizacijos | Prijungti GBP per Windsor onboard |
| 2 | **Windsor Free planas**: „more accounts than your Free plan allows" — GSC/GA4 užklausos per Windsor grąžina klaidą | Atjungti nenaudojamus account'us (lamele.lt, cookking.online, Maršalas Bing?) arba upgrade |
| 3 | **Ahrefs planas**: organic keywords API grąžina „Insufficient plan" | Naudoti GSC tiesiogiai (kai išspręstas #2) arba DataForSEO |
| 4 | Geo-grid duomenų šaltinio nėra | Žr. `02-open-source-irankiai.md` — GBP Rank Tracker (nemokamas) arba Apify pay-per-scan |

## Baseline metrikos, kurias reikia užfiksuoti PRIEŠ optimizavimą

1. Kiekvienos lokacijos GBP: reitingas, atsiliepimų skaičius, nuotraukų skaičius,
   postų dažnis, užpildytų laukų pilnumas (%).
2. Geo-grid pozicijos: „čiužiniai", „čiužinių parduotuvė", „lovos" — 5×5 grid
   Vilniuje/Klaipėdoje, 3×3 Ukmergėje.
3. GSC local užklausų clicks/impressions/position (90 d.).
4. AI share-of-voice: ar ChatGPT/Gemini/Perplexity rekomenduoja Sleeping Expert
   klausiant „geriausia čiužinių parduotuvė Vilniuje/Klaipėdoje" (žr. `ai-visibility` skill).
