# Open-source įrankių tyrimas (2026-08-25)

Klausimas: ar yra paruoštų skeleton'ų, kad nereikėtų statyti nuo nulio? Atsakymas —
taip, visi trys sluoksniai turi perpanaudojamus komponentus. HuggingFace šiai sričiai
nieko paruošto neturi (tai modelių hub'as) — viskas GitHub'e.

## 1. Geo-grid rank tracking (Local Falcon pakaitalai)

| Įrankis | Kas tai | Verdiktas |
|---|---|---|
| **GBP Rank Tracker** (vdesignu.com, kodas GitHub) | Nemokama open-source desktop app (Win/macOS): geo-grid skenavimas per naršyklės automatizaciją, heatmap. Veikia 100 % lokaliai | ✅ **Naudoti F1 baseline** — 0 € |
| **mcp-google-map** (github.com/cablate/mcp-google-map) | MCP serveris su Google Maps API: verslo rank per geo-grid, iki 3 keywords, top-3 konkurentai kiekviename taške | ✅ **Integruoti į Hermès** — MCP formatas idealiai tinka mūsų stack'ui; reikia Google Maps API rakto |
| **Geo-Grid Local Rank Tracker** (Apify, fayoussef) | Pay-per-scan actor, be API rakto | 🟡 Atsarginis variantas, jei desktop/MCP nepatiks |

## 2. GBP automatizacija (postai, atsiliepimai)

| Įrankis | Kas tai | Verdiktas |
|---|---|---|
| **gbp-review-agent** (github.com/satheeshds/gbp-review-agent) | MCP serveris GBP atsiliepimams: OAuth, automatinis atsakymų postinimas, rate limiting | ✅ **Skeleton Review Agent'ui** — MCP, tiesiai į Hermès |
| **google/alligator2** (github.com/google/alligator2) | Oficialus Google pavyzdys: GMB Insights → BigQuery + sentiment analizė | 🟡 Referencinis kodas Insights duomenims |
| **GoogleReviewsAI** (github.com/gallo2000sv/GoogleReviewsAI) | Python + OpenAI atsakymai į atsiliepimus | 🟡 Idėjos, bet Windows-only, sena architektūra |

## 3. AI visibility / GEO monitoringas

| Įrankis | Kas tai | Verdiktas |
|---|---|---|
| **AI Monitor** (github topic: ai-visibility-tracker) | Open-source brand mentions ChatGPT/AI Overview/Perplexity trackeris, self-hosted, BYOK | ✅ Palyginti su mūsų `ai-visibility` skill'u; jei brandesnis — perimti jų promptų/personų struktūrą |
| **generative-engine-optimization-tools** (github.com/izak-fisher) | Awesome list — GEO įrankių katalogas | ✅ Nuolatinis šaltinis radarui |
| Profound/Peec alternatyvos (github topics: ai-seo, generative-engine-optimization) | MIT licencijos AEO/GEO platformos, self-hostable | 🟡 Peržiūrėti detaliau prieš F3 |

## Išvada

Statyti nuo nulio nereikia. MVP surinkimas = **2 MCP serveriai (mcp-google-map +
gbp-review-agent) prijungti prie Hermès** + GBP Rank Tracker baseline'ui + mūsų
`ai-visibility` skill AI sluoksniui. Unikali mūsų dalis (moat) — ne komponentai,
o orkestracija: agentai + brand voice + QA gate + viena ataskaita.

Kitas žingsnis: klonuoti mcp-google-map ir gbp-review-agent, code review
(saugumas: OAuth scope'ai, kur keliauja duomenys), tada bandomasis paleidimas
su Vilniaus lokacija.
