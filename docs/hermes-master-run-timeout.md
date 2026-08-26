# Kodėl `hermes_master_run` visada timeout'ina per MCP

**Data:** 2026-08-26 · **Kontekstas:** bandymas atnaujinti WooCommerce produktą 24351 (vaikiška lova Teddy)

Ši pamoka `lessons.md` dar nėra užfiksuota — CAG užklausa patvirtino, kad įrašų apie
`master_run` trukmę, MCP limitą ar async vykdymą vault'e nėra.

---

## Išvada trumpai

`hermes_master_run` **struktūriškai netelpa** į MCP 60 s limitą. Tai ne apkrova ir ne atsitiktinumas —
tai aritmetika. Ir net jei tilptų, produkto jis vis tiek neatnaujintų, nes **WooCommerce agento
tarp prijungtų agentų nėra**.

---

## 1 priežastis: 5 LLM mazgai vs 60 s lubos

`master_run` pipeline pagal įrankio aprašymą:

| # | Mazgas | Ką daro |
|---|---|---|
| 1 | PLANNER | DSPy ChainOfThought → 3–5 sub-taskai |
| 2 | RESEARCHER | **CAG full vault** |
| 3 | REASONER | DSPy LOGIC |
| 4 | EXECUTOR | intent matching → 1–3 agentai |
| 5 | REFLECTOR | outcome score |

**Išmatuota:** `hermes_cag` savo atsakyme praneša vykdymo laiką. Du nepriklausomi matavimai
tą pačią dieną:

```
⏱ 34.9s | input=233274 | cache_read=233207 (100.0%) | cache_create=159218 | output=934
⏱ 52.4s | input=233315 | cache_read=233207 (100.0%) | cache_create=159218 | output=2419
```

Tai reiškia: **vien 2-as mazgas (RESEARCHER) suvalgo 35–52 s iš 60 s biudžeto.** Cache hit rate 100 %,
tad greičiau nebus — tokia yra 159 k tokenų konteksto kaina. Pridėjus dar keturis LLM iškvietimus,
pilnas pipeline neišvengiamai viršija 60 s.

Todėl **kiekvienas** `master_run` iškvietimas per MCP baigsis timeout'u. Du bandymai 2026-08-26
(~16:20 ir ~16:40) — abu timeout po 60 s.

### Svarbu: timeout ≠ neįvyko

MCP jungtis nutrūksta, bet pipeline serveryje lieka suktis. Iškvietėjas negauna nei rezultato,
nei klaidos, nei run ID — **negali patikrinti, ar veiksmas įvyko.** Tai blogiausias variantas
rašymo operacijoms: galimas dublikatas, jei bandoma iš naujo.

---

## 2 priežastis: EXECUTOR neturi WooCommerce maršruto

`hermes_agents` (šaltinis: `shared_state.db/outcomes`, OCL truth) grąžina 26 agentus tokiuose lane'uose:

| Lane | Agentai |
|---|---|
| Advertising | google_ads_agent, merchant_monitor |
| Content | blog_agent, blog_content_planner, blog_learning, blog_quality_gate, blog_roi_strategist, blog_scheduler, content_decay_agent, content_decay_predictor_agent |
| Forecast | demand_forecasting_agent, demand_signals |
| Intelligence | ai_visibility_agent, competitor_analysis_agent, dataforseo_agent |
| Knowledge | ai_knowledge_agent |
| Metacog | evaluation_agent |
| SEO | ctr_predictor, performance_learner_simple, performance_learning_agent, trend_analyzer |
| Video | video_ai_cinematic, video_avatar_agent, video_metacognition, video_scheduler, video_stock_agent |

**`hermes_shop_agent` sąraše NĖRA. Shop/Commerce lane'o nėra. Nė vieno WooCommerce agento.**

CAG teigė, kad `hermes_shop_agent` egzistuoja, bet pats hedge'ino — *„pavadinimo pagrindu, turėtų būti
susijęs su parduotuvės operacijomis“*. Runtime sąrašas to nepatvirtina. Vault'as ir realybė išsiskyrę.

Pasekmė: net ir spėjęs per 60 s, EXECUTOR intent matching neturėtų kur nukreipti produkto užduoties
ir nukristų į artimiausią atitikmenį — Content lane. **Būtent tai ir stebėjome:** po bandymo
activity feed rodė tik `blog_agent` srautus, o `blog_today` pasipildė nauju juodraščiu. Produktas 24351
liko nepaliestas su Nico aprašymu.

---

## Ką daryti

### Trumpalaikiai (šiandien)

1. **Nenaudoti `master_run` produktų darbui.** Naudoti `scripts/wp-update-teddy.py` — tiesioginis
   WC REST iškvietimas, be LLM mazgų, su peržiūra ir patikra po įrašymo.
2. **Niekada nebandyti `master_run` iš naujo po timeout'o** — nežinai, ar pirmas įvyko.

### Sisteminiai (verti dienos darbo)

3. **`master_run` paversti asinchroniniu.** Iškvietimas turi grąžinti `run_id` per <1 s, o rezultatas
   pasiimamas atskiru `hermes_master_status(run_id)`. Dabartinis blokuojantis dizainas su MCP
   nesuderinamas iš principo.
4. **Prijungti `wc_mcp_server` prie Claude sesijų.** CAG mini, kad jis jau veikia **portu 5011**
   ir turi WC Store API endpoint'us (`products`, `cart/add-item`, `cart`, `checkout`).
   Tai teisingas kanalas produktų darbui — tiesioginis, be LLM tarpininkų. Dabar jis pasiekiamas
   tik lokaliai serveryje.
5. **Įrašyti šią pamoką į `lessons.md`** — jos ten nėra, todėl klaida pasikartos.

---

## Atskira problema: tinklo prieiga

`sleepingexpert.lt` blokuojamas šios Claude Code aplinkos egress politikos — proxy atmeta CONNECT su 403:

```
{"kind":"connect_rejected",
 "detail":"gateway answered 403 to CONNECT (policy denial or upstream failure)",
 "host":"sleepingexpert.lt:443"}
```

Kol domenas neįtrauktas į aplinkos leidžiamų sąrašą, joks skriptas iš Claude sesijos svetainės nepasieks.
Aplinkos tinklo politika konfigūruojama Claude Code aplinkos nustatymuose:
https://code.claude.com/docs/en/claude-code-on-the-web
