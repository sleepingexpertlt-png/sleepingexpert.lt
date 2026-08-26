# Backlog triage pagal 60 d. tikslą (2026-08-26)

Šaltinis: `hermes_promises` — 4 open, 19 user-blocked, 83 resolved.
Filtras: ar veiksmas judina **maršrutus +30 %** arba **3 raktažodžius į top 5**
iki 2026-10-24? Jei ne — antraeilis, nesvarbu kiek seniai kabo.

## A. JUDINA PAGRINDINĮ SKAIČIŲ (maršrutai) — daryti pirma

| # | Kas | Kodėl svarbu | Kieno |
|---|---|---|---|
| 1 | **U-009 / P-064: Vilniaus GBP kategorijos lenkiškai** | Pagrindinė kategorija = stipriausias valdomas GBP signalas (~32 % svorio). Lenkiška kategorija reiškia, kad Vilnius rikiuojasi ne pagal tai, ko ieško LT vartotojas. Vilnius silpniausias: 8 maršrutai vs 13/13. | Owner, GBP UI, ~5 min. |
| 2 | **U-010 / P-065: Q&A seeding Vilnius + Klaipėda** | 8 klausimai/lokacijai jau paruošti. Q&A rodomi profilyje ir veikia konversiją į maršrutą. API miręs (501) — tik ranka. | Owner, Maps UI |
| 3 | Atsiliepimų QR prie kasų | Atsiliepimų TEMPAS (steady > burst) — antras stipriausias svertas. Sistema neegzistuoja. | Owner + VPS (QR generavimas) |

**Pastaba:** visi trys — rankiniai. Automatizuoti jų negalima (GBP Q&A API
deprecated, kategorijos tik per UI). Tai ne sistemos trūkumas.

## B. JUDINA ANTRINĮ SKAIČIŲ (raktažodžiai į top 5)

| # | Kas | Statusas |
|---|---|---|
| 4 | 1 banga B1–B5 (paruoštas tekstas `14-banga1-turinys.md`) | Laukia VPS įkėlimo |
| 5 | B7 kategorijų pilotas (čiužiniai, pagalvės) | Tekstas paruoštas, tik draft/staging |

## C. GADINA MATAVIMĄ — taisyti, nes be to nežinosim, ar pavyko

| # | Radinys | Poveikis |
|---|---|---|
| 6 | **`traffic_snapshot_age_hours` = 48.5** | GSC metrikos (`gsc_avg_position` 8.2, `gsc_clicks_24h` 43, `impressions` 1674) paskutinį kartą matuotos **08-25 07:30**. Šiandien nebuvo. Tyliai. Be šviežio GSC negalim sekti antrinio tikslo. |
| 7 | **AI referrer bug** (`aeo_reverse_discovery.py:575`) | `"ai" in medium` substring'as — „(data not available)" skaitomas kaip AI srautas. 684 AI sesijos realiai ≈ **127** (chatgpt 121 + gemini 5 + copilot 1). Likę fb/ig/an — klaidingi. Radinys užfiksuotas 08-03, **iki šiol netaisytas**. |
| 8 | R3: scheduler rodo `errors: []` su 0 straipsnių | Šiandienos gedimas buvo nematomas 8 val. |

**Fix #7 (vienas kondicijos pakeitimas, ne perrašymas):**
`is_ai = any(p in source for p in ai_platforms) or "ai" in medium`
→ `medium` tikrinti tik tiksliais atitikmenimis (pvz. `medium in {"ai", "ai_referral"}`),
ne substring'u. Reprodukcinis testas: „(data not available)" neturi patekti į AI lentelę.

## D. NEJUDINA NEI VIENO — nesivelti iki 10-24

P-006 (TikTok creators), P-007 (NEURO Warfare), P-008 (backlog triage 4 sav.),
P-070 (250 netriažuotų eilučių), U-003 (Google Ads OAuth), U-004 (LinkedIn token),
U-005 (MCP stable URL), U-008 (YouTube shorts mapping), U-013 (.htaccess),
U-014 (Elmo — sąmoningai pauzėje, kaštai), U-017 (GCR badge — laukia duomenų),
U-020 (CookieYes rescan), U-021 (WC retention nustatymai), U-022.

Tai NEREIŠKIA „nesvarbu" — tai reiškia „ne šiame 60 d. lange". Kai kurie
(U-013, U-020, U-021) yra teisiniai/saugumo, spręstini atskiru ciklu.

## Išvada viena eilute

Pagrindinį skaičių judina **trys rankiniai owner veiksmai**, kurių jokia
automatika neatstos. Antrinį — 1 banga, kuri jau paruošta. Viskas kita
šiame lange yra triukšmas arba matavimo higiena.
