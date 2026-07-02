# 🔧 Patobulinimų Backlog — 2026-07-02

Šaltiniai: Hermes žinių bazė (`hermes_cag`, cituojami vault failai), gyvos metrikos (`hermes_status`, `hermes_business_metrics`), sistemos auditas 2026-07-02.

## 🔴 P0 — Savininko veiksmai (šiandien, didžiausias svertas)

| # | Darbas | Kodėl dabar | Šaltinis |
|---|--------|-------------|----------|
| 1 | **GBP telefono mygtukas** — skambučiai 0 per 7 d. visose 3 parduotuvėse (Vilnius 18 maršrutų/0 skamb., Klaipėda 5/0, Ukmergė 3/0) | Tiesioginis pajamų nutekėjimas; sistema pažymėjo `alert: true` | hermes_status (salon_signal) |
| 2 | **Council eskalacija laukia** — „llms.txt regression fix" (balas 5.7, nuo 2026-07-01 19:39) | AEO strategijos failas užstrigęs be sprendimo; `/council_approve` arba `/council_reject` per Telegram | hermes_activity_feed |
| 3 | **Šios paros blogo klaida** — publikavimas nulūžta PO Council PROCEED: 06:17 patvirtintas „Latekso čiužiniai: atsiliepimai ir ekspertų verdiktas 2026" (7.3), bet error=1, published=0. Klaida publikavimo žingsnyje (WP?). 11:57 paleistas master_run tyrimui | Kasdienė turinio gamyba = AEO strategijos pagrindas | hermes_status + hermes_activity_feed |
| 4 | **Hermes MCP įrankių leidimai** — pusė funkcijų už „requires approval" (agents, blog_today, synergy, radar, brandbook, promises, council_pending); Supabase MCP — taip pat | Be jų neįmanoma pilna kontrolė ir auditas | MCP auditas 2026-07-02 |

## 🟡 P1 — Greita grąža (šią savaitę)

| # | Darbas | Detalės | Šaltinis |
|---|--------|---------|----------|
| 5 | **SE čiužinių kategorijos CLS 0.32** 🔴 | Optimizuoti puslapio elementus (vaizdai, filtrai) — rezervuoti vietą, išvengti išdėstymo šuolių. Reikia savininko leidimo | project_sites_status_2026-06-07.md |
| 6 | **lamele.lt blogo nėra — AEO spraga** | Sukurti blogo platformą ir edukacinį turinį (Perplexity cituoja gidus, ne produktus) | project_sites_status_2026-06-07.md |
| 7 | **cookking Organization schema** — trūksta pilnų Maršalas MB rekvizitų | Adresas ir kodas jau žinomi (Pylimo g. 23, 304859731); trūksta PVM kodo iš savininko | project_cookking.md |
| 8 | **cookking FAQPage + MerchantReturnPolicy** | Reikia savininko patvirtintų pristatymo/garantijos/grąžinimo terminų (nefabrikuota) | project_cookking.md |

## 🔴 P0-B — Pastatyta, bet nenaudojama (patvirtinta savininko 2026-07-02)

| # | Darbas | Detalės | Šaltinis |
|---|--------|---------|----------|
| B1 | **DUK snippet'o rankinis pataisymas** ⚠️ teisinė rizika | Code Snippet 16: draudžiamas teiginys „gamintojų garantijos iki 20 metų" tebėra gyvas — plugin'as tyliai ignoruoja PUT (HTTP 200 false success). Taisyti per WP admin rankiniu būdu | Correction 2026-06-03 |
| B2 | **Radaro → veiksmo kilpa** | 10 tier-1 signalų, 0 reakcijų (radar_to_metacog sinergija 0.3). Įjungti: signalas → council pasiūlymas → backlog automatiškai | Štabo 2026-06-15 |
| B3 | **Chroniškas blog publikavimas** | Ta pati klaida fiksuota 06-15 („CHRONIC 8d") ir 07-02 — root cause serveryje, dengia MOKYMOSI-AUDITAS.md F blokas | Štabo 2026-06-15 |
| B4 | **Klaipėdos GBP konversijos diagnostika** | 18% konversija vs Vilnius 34%, Ukmergė 35%. Hipotezės: senas listing'as, kategorijos, neatsakyti reviews, multi-tenant adresas, Photos sekcija | Letta 2026-05-27 |

## 🟡 P1-B — Upgrade kandidatai (radaro pastebėti, neįdiegti)

| # | Darbas | Detalės | Šaltinis |
|---|--------|---------|----------|
| B5 | **Memory Palace vietoj Letta** | Letta mėtė HTTP 500 (07-02), chat išjungtas („LLM auth dead"). Memory Palace: self-hosted, MCP-compatible, rollback + Write Guard. Vertinimo blokas — MOKYMOSI-AUDITAS.md H | Radaras 2026-05-24 |
| B6 | **Higgsfield AI MCP video generavimui** | Alternatyva fal.ai/Kling (05-31 balanso krizė su tyliu zoom-fallback) | Radaras 2026-05-23 |
| B7 | **NotebookLM 7 promptų rinkinys** | B2B sleep coaching niša (€100–300 vizitas) — nauja Maršalas paslaugų linija | Radaras 2026-05-23 |
| B8 | **ASSET MAP aktyvavimas** | Turtas sužymėtas nišoms (TPNC→medicina, 6 kalbos→užsieniečiai, MBSR→menopauzė, ortopedija→post-surgery, B2B hospitality) — parinkti 1 nišą ir paleisti bandomąją kampaniją | Letta 2026-05-23 |

## 🔺 Piramidės kryptis (savininko sprendimas 2026-07-02)

Kilti ne aukštyn (L7 Self-Mod), o užlopyti apačią — mokymosi lygį (trait 4 = -0.077, vienintelis raudonas). Seka: (1) mokymosi auditas serveryje → (2) radaro→veiksmo kilpa (B2) → (3) Memory Palace vertinimas (B5) → (4) DUK snippet fix (B1). Pagal pamoką: „AGI-research-tier ≠ Hermès strategos, prioritetas — pelnas."

## 🟢 P2 — Suplanuoti (šį mėnesį)

| # | Darbas | Detalės | Šaltinis |
|---|--------|---------|----------|
| 9 | cookking raktažodžių spragų analizė + GTIN/kainų neatitikimai | Deferred: keyword gap (D), gtin/price (C) | project_cookking.md |
| 10 | cookking `force-dynamic` produkto puslapyje — TTFB rizika | Ištirti, ar būtinas; optimizuoti renderinimą | project_cookking.md |
| 11 | Hidra klasterio užbaigimas | node2-4 onboarding + `llm_router.py` wiring pc_hidra→:11430 su fallback | project_hidra_cluster.md |
| 12 | Letta pakaitalo vertinimas — Memory Palace | Self-hosted agent memory OS, MCP-compatible; Letta jau kartą mėtė HTTP 500 | Radar signalas 2026-05-24 |
| 13 | SE pagrindinio puslapio PSI 50-60 | Atidėta dėl žemo ROI (WP temos apribojimai) — tik jei savininkas prioritetizuoja | project_sites_status_2026-06-07.md |
| 14 | `hermes_master_run` asinchroninis režimas | Per MCP 5-node pipeline nukertamas 60 s limito (2 nepavykę bandymai 07-02). Fix: paleidimas grąžina run_id, rezultatas paimamas atskiru kvietimu | MCP auditas 2026-07-02 |
| 15 | Supermetrics — NEpirkti | Trial baigėsi 05-22; GSC duomenis serveris traukia nemokamai per savo integraciją. Sprendimas 07-02: nemokėti | Savininkas 2026-07-02 |

## ✅ Atlikta šioje sesijoje (2026-07-02)

- Google Cloud billing atstatytas → `hermes_cag` ir `hermes_letta_query` vėl veikia
- MB „Maršalas" profilis (`MARSALAS.md`) su dokumentuota „done-for-you" strategija
- „Conducting AI" agentų org schema (`AI-ORG.md`) su tikrais agentų vardais
- Maršalas paslaugos vienpuslapis (`PASLAUGA.md`) pagal outcome-funnel principą
- Ištaisytas juridinių asmenų atskyrimas (Sleeping Expert LT, MB ≠ MB Maršalas)

---

© 2026 MB „Maršalas" / Sleeping Expert LT, MB. Atnaujinta 2026-07-02.
