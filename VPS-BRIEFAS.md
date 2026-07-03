# 🚀 VPS Claude Code — Darbų Briefas

**Kam:** Claude Code sesija serveryje `/root/frontier-agent/`
**Iš:** Maršalas strategijos sesija (claude.ai, 2026-07-02)
**Šaka:** github.com/sleepingexpertlt-png/sleepingexpert.lt → `claude/marsalas-service-provider-baz5gk`

Šis dokumentas savarankiškas — visos komandos ir kontekstas viduje. Papildomi failai toje pačioje šakoje: MOKYMOSI-AUDITAS.md, KEYPHRASE-PLANAS.md, AUDITAS-2026-07-02.md, RADAR-SIGNALAI.md, TOBULINIMAI.md.

---

## 0. Privalomos saugos taisyklės (iš CLAUDE.md — GALIOJA VISUR)

1. **Verified, ne assumed** — niekada neišgalvoti skaičių/faktų; visada patikrinti po veiksmo tame pačiame kodo bloke.
2. **Test ant draft/private** prieš rašant į gyvą WooCommerce.
3. **Niekada** `<script>`/`<style>` į WC aprašymus; **niekada** `rank_math_schema_*` per WC API (500 klaidos).
4. **Draudžiami teiginiai:** „premium", „exclusive", „Italijos dizaineriai", „geriausi pasaulyje", išgalvotos garantijos/grąžinimai.
5. **Niekada** konkurentų vardų (LONAS, Topocentras, IKEA, JYSK, Dormeo) — net kaip žodžio dalies.
6. Cron įrašai — **tik absoliutūs keliai** (pamoka 2026-05-28).
7. LT kalba, LT pirkėjas.

---

## 1. 🔴 PRIORITETAS #1 — Publish vykdiklis (svarbiausia)

**Problema:** blog draft→published grandinė lūžta PO Council PROCEED. 2026-07-02: 7 juodraščiai (kokybė 74–88, visi virš 70 slenksčio), 5+ Council PROCEED, **0 published**. Klaidos statusas išnyko, bet publikavimas neįvyksta niekam. Chroniška — fiksuota ir 06-15 („CHRONIC 8d").

**Kritinė pasekmė:** `capture_outcome()` (`src/utils/outcome_capture_hook.py`) kabinamas `run_pipeline()` PO `results["published"] += 1`. Kol published=0, **mokymosi signalas nefiksuojamas** → trait 4 mokymasis -0.077. Vienas fix atgaivina IR publikavimą, IR mokymąsi.

```bash
# 1.1 Rasti kur pipeline pasiekia (ar ne) published:
grep -rn "published" /root/frontier-agent/src/ --include="*.py" | grep -i "pipeline\|publish\|wp_" | head -30
grep -rn "def run_pipeline" /root/frontier-agent/src/

# 1.2 Rasti WP publish žingsnį ir jo klaidų logą:
grep -rn "wp_publish\|rest/wp\|status.*publish\|POST.*posts" /root/frontier-agent/src/ --include="*.py" | head
find /root/frontier-agent/logs -name "*.log" -mtime -1 -exec grep -l "publish\|error" {} \;

# 1.3 Šiandienos draft su PROCEED statusu DB:
sqlite3 /root/frontier-agent/shared_state.db \
  "SELECT id, title, status, quality_score, ts FROM blog_articles WHERE date(ts)=date('now') ORDER BY ts;"

# 1.4 Pataisyti šaknį, tada TESTAS: publikuoti bent 1 (latekso čiužiniai, q~81) ant staging/draft
#     patikrinti WP, kad tikrai matomas, TADA gyvai.
# 1.5 Verifikacija: po fix paleisti pipeline, patvirtinti published += 1 IR capture_outcome įrašą outcomes lentelėje.
```

---

## 2. 🔴 PRIORITETAS #2 — Mokymosi auditas (OCL kilpa)

**Kontekstas:** agentai GYVI (patikrinta — `performance_learner_simple`, `content_decay_simple`, `trend_analyzer_simple` dirba kasdien), bet jų rezultatai nepasiekia outcomes lentelės. Klausimas: ar OCL kilpa realiai sukasi.

```bash
# 2.1 Ar adapt_rules.json atsinaujina? (OCL galutinis artefaktas)
find /root/frontier-agent -name "adapt_rules.json" -exec stat -c '%y  %s bytes  %n' {} \;
#     LAUKIAMA: <48h, >100 bytes. JEI SENAS → kilpa neuždaryta.

# 2.2 Ar _apply_ocl_to_adapt_rules() paleidžiamas? (proto_incubator.py)
crontab -l | grep -i "incubator\|ocl\|learn"
grep -rn "proto_incubator\|_apply_ocl" /root/frontier-agent/scripts/ /root/frontier-agent/src/

# 2.3 Ar KAS NORS skaito adapt_rules.json? (uždaryta kilpa = rašoma IR skaitoma)
grep -rn "adapt_rules" /root/frontier-agent/src/ --include="*.py" | grep -v proto_incubator

# 2.4 Outcomes fiksuojami šiandien?
sqlite3 /root/frontier-agent/shared_state.db \
  "SELECT COUNT(*), MAX(ts) FROM outcomes WHERE ts > datetime('now','-24 hours');"

# 2.5 Circuit breaker persistencija (buvo tik atmintyje, resetindavosi):
sqlite3 /root/frontier-agent/metacog.db ".tables"
grep -n "circuit" /root/frontier-agent/src/agents/metacognition.py | head

# 2.6 detect_patterns skaito iš tos pačios vietos, kur rašo evaluate_and_learn?
grep -n -A5 "def detect_patterns" /root/frontier-agent/src/agents/metacognition.py

# 2.7 Kokybės kreivė -0.077 šaltinis:
grep -rn "quality_slope\|blog_quality" /root/frontier-agent/scripts/traits_business_fetcher.py

# VEIKSMAS: kiekvienam radiniui — pataisyti (dažniausia priežastis pagal pamokas:
# agentas parašytas, bet ne crontab'e — 2026-04-05). Pateikti ataskaitą kas veikė / kas pataisyta.
```

---

## 3. 🟡 PRIORITETAS #3 — ai_visibility_agent cron (savininko GO gautas)

```bash
# Absoliutūs keliai! Trečiadieniais 08:00 (project_ai_visibility_agent.md rekomendacija)
(crontab -l; echo "0 8 * * 3 /root/frontier-agent/venv/bin/python3 /root/frontier-agent/src/agents/ai_visibility_agent.py >> /root/frontier-agent/logs/ai_visibility.log 2>&1") | crontab -
# Bandomasis paleidimas + patikrinti outcomes fiksavimą. Rezultatus (AI matomumo spragas) į hermes_status.
```

## 4. 🟡 PRIORITETAS #4 — Keyphrase pilotas (20 produktų, BE rašymo)

**Faktai:** 789 produktai, RankMath, 91% turi focus_keyword, `rank_math_additional_keywords` tuščias. SVARBU: šis laukas pats reitingų nekelia — srautą augina keyphrase ĮAUDIMAS į turinį (pavadinimą, aprašymą, alt). GSC integracija JAU serveryje (iš ten gsc_clicks_24h) — Supermetrics NEreikia.

```bash
# 4.1 Eksportas: WC API → produktai su focus, be additional (~700).
# 4.2 Kiekvienam URL: GSC 90d užklausos (impressions,clicks,position).
#     Secondary kandidatas = užklausa su parodymais, NEpadengta focus, su pirkimo intencija
#     (pvz. „...kaina", „...atsiliepimai", „...160x200").
# 4.3 Atrinkti 20 su daugiausiai parodymų. Kokybės filtrai (0 skyrius).
# 4.4 PATEIKTI SAVININKUI lentelę: produktas | focus | siūlomas secondary | GSC įrodymas | kur įterpsime.
#     JOKIO rašymo į WC be patvirtinimo.
```

## 5. 🟡 Council darbai (savininkas APPROVED 2026-07-02, callback_triggered=false)

Abu patvirtinti, bet automatiškai nepasileido — paleisti rankiniu būdu:
- **#169 AEO Goal Architecture** — kiekviename blog straipsnyje ir produkto puslapyje „AI-search klausimas" → direct-answer blokas.
- **#170 llms.txt regression fix** — regeneruoti llms.txt (regenerate_llms.py ar ekvivalentas).

## 6. 🟢 Radaro signalai (idėjų peržiūrai, ne skubu)

Iš RADAR-SIGNALAI.md, susieti su aukščiau: **stop-slop** (AI-slop remover → blogo kokybei, pritaikyti LT+brandbook), **awesome eval** (agentų vertinimas → OCL kilpai #2), **ECC agent-eval/continuous-agent-loop** (idėjos OCL, ne aklas diegimas). Twenty CRM + Cybersecurity Skills — Maršalas paslaugoms, po core stabilizavimo.

---

## Sėkmės kriterijai (po 1–2 savaičių)

| Rodiklis | Dabar | Tikslas |
|----------|-------|---------|
| blog_published_24h | 0 🔴 | >0 kasdien |
| adapt_rules.json amžius | ? | <48h |
| outcomes 24h | ? | dešimtys |
| blog_quality_slope_30d | -0.077 🔴 | >0 |
| ai_visibility_agent | staging | veikia savaitiniu cron |
| keyphrase pilotas | 0 | 20 patvirtinta, GSC prieš/po matuojama |

## Grįžtamasis ryšys

Po darbų — trumpa ataskaita savininkui (kas pataisyta / kas liko / skaičiai). Svarbius sprendimus fiksuoti Letta atmintyje ir atnaujinti TOBULINIMAI.md šakoje. Verified, ne assumed — po kiekvieno rašymo į gyvą sistemą.

---

© 2026 MB „Maršalas". Sudaryta iš 2026-07-02 audito ir sistemos telemetrijos. Jokių išgalvotų skaičių.
