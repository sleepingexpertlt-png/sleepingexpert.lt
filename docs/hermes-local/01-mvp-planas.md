# Hermès Local — MVP planas

Konceptas: Llamamaps parduoda rankinį „Google Maps top 3 per 90 d." darbą.
Mūsų versija — automatizuotas local + AI visibility variklis, pirmiausia įrodytas
ant savų 3 parduotuvių. Tik su rezultatais rankoje kalbamės apie partnerystę.

## Architektūra

```
┌─ DATA LAYER ────────────────────────────────────────────┐
│ GBP API — TIESIOGINĖ integracija (gmb_agent.py, veikia) │
│ GSC · GA4 (Windsor / tiesiogiai)                        │
│ Geo-grid: GBP Rank Tracker (open source) / Apify actor  │
│ AI probes: ai-visibility skill (ChatGPT/Gemini/Perplexity)│
└──────────────┬──────────────────────────────────────────┘
┌─ AGENT LAYER ▼ ─────────────────────────────────────────┐
│ 1. Audit Agent — GBP pilnumo skoras kiekvienai lokacijai│
│ 2. Content Agent — GBP postai LT (brand voice, be       │
│    draudžiamų teiginių)                                 │
│ 3. Review Agent — atsakymų juodraščiai + QA gate        │
│ 4. Citation Agent — NAP nuoseklumas (baldurojus.lt,     │
│    statyba.lt, kt. katalogai)                           │
│ 5. Visibility Agent — geo-grid + AI share-of-voice      │
└──────────────┬──────────────────────────────────────────┘
┌─ ORCHESTRATION ▼ ───────────────────────────────────────┐
│ Hermès Master + savaitinės cron rutinos                 │
│ Žmogaus patvirtinimas prieš bet kokį publikavimą        │
└──────────────┬──────────────────────────────────────────┘
┌─ OUTPUT ▼ ──────────────────────────────────────────────┐
│ Dashboard (heatmap + AI SoV trend) · mėn. ataskaita     │
└─────────────────────────────────────────────────────────┘
```

## Fazės

**F0 — Atblokavimas (owner, ~30 min):**
- 🔴 Sutvarkyti Ukmergės GBP dublikatą (420 impressions / 0 directions — žr. 00 failą).
- Įdiegti geo-grid įrankį (žr. 02 failą) ir paleisti pirmą skenavimą.
- (Windsor GBP NEREIKALINGAS — GMB API prijungtas tiesiogiai per Hermès.)

**F1 — Baseline (1 savaitė):** užfiksuoti visas 00 faile išvardintas metrikas.
Niekas neoptimizuojama, kol nėra „prieš" nuotraukos.

**F2 — Optimizavimas (2–4 savaitės):**
- GBP profilių pilnumas iki 100 % (kategorijos, paslaugos, produktai, Q&A).
- 2 postai/sav. kiekvienai lokacijai (Content Agent, žmogus tvirtina).
- Atsakymai į visus atsiliepimus <48 h (Review Agent juodraščiai).
- Lokacijų puslapiai: LocalBusiness/Store JSON-LD schema, GBP nuorodos.
- NAP suvienodinimas kataloguose.

**F3 — Matavimas (60 d. po F2 starto):** geo-grid „prieš/po", GSC local
užklausų pokytis, AI SoV pokytis.

## Sėkmės kriterijai (kill criteria partnerystės idėjai)

- Per 60 d. bent 2 iš 3 lokacijų pagerina geo-grid vidurkį ≥2 pozicijomis
  pagrindinėms frazėms, ARBA GSC local užklausų paspaudimai +30 %.
- Jei ne — įrankį pasiliekam vidiniam naudojimui, partnerystės nestumiam.

## Kaštai

- Open-source geo-grid: 0 € (desktop) arba Apify ~pay-per-scan.
- AI probes: API kaštai ~kelios dešimtys €/mėn.
- Owner laikas: F0 ~30 min, po to tik postų/atsakymų tvirtinimas (~15 min/sav.).
