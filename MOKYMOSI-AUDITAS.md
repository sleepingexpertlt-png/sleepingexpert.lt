# 🔍 Mokymosi Grandinės Auditas — Vykdomasis Sąrašas Serveriui

**Paskirtis:** patikrinti, ar Hermes mokymosi ciklas (OCL) realiai sukasi, ar tik užfiksuotas kaip pataisytas. Sudaryta 2026-07-02 pagal lessons.md ir CAG duomenis.

**Kaip naudoti:** atidarykite Claude sesiją serveryje (`/root/frontier-agent/`) ir duokite šį failą su prašymu „įvykdyk visas patikras ir pateik ataskaitą". Kiekviena patikra turi komandą, laukiamą rezultatą ir veiksmą, jei rezultatas blogas.

**Kontekstas:** kokybės tendencija `blog_quality_slope_30d = -0.077` (neigiama), nors OCL kilpa dokumentuota kaip uždaryta 2026-06-04. Arba pataisymai neveikia, arba veikia per silpnai — šis auditas išsiaiškins.

---

## A. Ar OCL kilpa realiai sukasi? (svarbiausia patikra)

Pamoka 2026-06-04 sako, kad `_apply_ocl_to_adapt_rules()` (`src/agents/proto_incubator.py`) uždarė kilpą. Tikriname, ar ji gyva ŠIANDIEN:

```bash
# A1. Ar adapt_rules.json egzistuoja ir kada paskutinį kartą atnaujintas?
find /root/frontier-agent -name "adapt_rules.json" -exec stat -c '%y  %s bytes  %n' {} \;
# LAUKIAMA: data per paskutines 24-48 h, dydis > 100 bytes
# JEI SENAS/TUŠČIAS: kilpa neuždaryta — žr. A4

# A2. Ar taisyklės turi šviežių įrašų?
find /root/frontier-agent -name "adapt_rules.json" -exec jq '.' {} \; | head -50
# LAUKIAMA: taisyklės su timestamp'ais po 2026-06-04

# A3. Ar outcomes fiksuojami šiandien?
sqlite3 /root/frontier-agent/shared_state.db \
  "SELECT COUNT(*), MAX(ts) FROM outcomes WHERE ts > datetime('now','-24 hours');"
# LAUKIAMA: count > 0 (agentai dirba kasdien, todėl turi būti dešimtys)
# PASTABA: jei stulpelis ne 'ts' — pasižiūrėti schema: .schema outcomes

# A4. Ar proto_incubator apskritai paleidžiamas? (cron / Airflow)
crontab -l | grep -i incubator
grep -rn "proto_incubator" /root/frontier-agent/scripts/ 2>/dev/null | head
# LAUKIAMA: yra cron įrašas SU ABSOLIUČIU keliu (pamoka 2026-05-28: reliatyvūs keliai cron'e lūžta)
# JEI NĖRA: štai kodėl adapt_rules nesikeičia — įdėti į cron

# A5. Ar adapt_rules.json kas nors SKAITO? (uždaryta kilpa = rašoma IR skaitoma)
grep -rn "adapt_rules" /root/frontier-agent/src/ --include="*.py" | grep -v proto_incubator | head
# LAUKIAMA: bent vienas agentas (blog_agent, scheduler...) įsikelia taisykles
# JEI NIEKAS NESKAITO: taisyklės rašomos į stalčių — kilpa uždaryta tik puse
```

## B. Circuit breaker persistencija

Pamoka (lessons.md:1868-1872): CB būsena buvo tik atmintyje, resetindavosi su kiekvienu cron (~5 min).

```bash
# B1. Ar CB būsena saugoma DB?
sqlite3 /root/frontier-agent/metacog.db ".tables"
sqlite3 /root/frontier-agent/metacog.db \
  "SELECT * FROM circuit_breakers ORDER BY rowid DESC LIMIT 5;" 2>/dev/null
# LAUKIAMA: lentelė egzistuoja ir turi įrašų su būsenomis

# B2. Ar kodas įkelia būseną startuodamas?
grep -n "circuit" /root/frontier-agent/src/agents/metacognition.py | head -20
# LAUKIAMA: load/restore logika __init__ arba startup kelyje, ne tik in-memory dict
```

## C. detect_patterns ↔ strategy_log neatitikimas

Pamoka (lessons.md:2573-2575): `evaluate_and_learn` rašė į `strategy_log`, o `detect_patterns` skaitė iš `memory` — streak visada 0.

```bash
# C1. Iš kur detect_patterns skaito DABAR?
grep -n -A5 "def detect_patterns" /root/frontier-agent/src/agents/metacognition.py
# LAUKIAMA: skaito iš tos pačios vietos, kur rašo evaluate_and_learn

# C2. Ar streak'ai gyvi?
sqlite3 /root/frontier-agent/metacog.db \
  "SELECT agent, COUNT(*) FROM strategy_log GROUP BY agent ORDER BY 2 DESC LIMIT 10;" 2>/dev/null
# LAUKIAMA: įrašai kaupiasi; jei lentelė tuščia arba neauga — mokymosi signalas vis dar 0
```

## D. Traits duomenų šaltinis („lavono spąstai")

Pamoka (lessons.md:2390-2399): savidiagnostika skaitė iš `metacog.db/metacog_outcomes`, kur dominavo video/distribucijos agentai — traits rodė ne realų verslo darbą.

```bash
# D1. Iš kur traits skaičiuojami dabar?
grep -n "metacog.db\|shared_state.db" /root/frontier-agent/scripts/traits_business_fetcher.py
# LAUKIAMA: shared_state.db/outcomes (OCL tiesa), NE metacog.db/metacog_outcomes
# JEI metacog.db: visi 10 traits (įsk. mokymosi -0.077) gali rodyti iškreiptą vaizdą
```

## E. Kodėl kokybės kreivė neigiama?

```bash
# E1. Iš kur skaičiuojamas blog_quality_slope_30d?
grep -rn "quality_slope\|blog_quality" /root/frontier-agent/scripts/traits_business_fetcher.py

# E2. Žali duomenys — kokybės balai per 30 d. (lentelės pavadinimą patikslinti pagal E1):
sqlite3 /root/frontier-agent/shared_state.db \
  "SELECT date(ts), ROUND(AVG(quality_score),1), COUNT(*) FROM blog_articles
   WHERE ts > datetime('now','-30 days') GROUP BY date(ts) ORDER BY 1;" 2>/dev/null
# ANALIZĖ: ar po 2026-06-25 quality gate sugriežtinimo balai kyla?
# Jei balai stovi ~70-75 ir nekyla: rašymo prompt'ai negauna grįžtamojo ryšio iš QG blokavimo priežasčių
```

## F. Šiandienos publikavimo klaida (bonus — P0 iš backlog'o)

```bash
# F1. Kas nulūžo po Council PROCEED 2026-07-02 06:17 („Latekso čiužiniai...")?
grep -rn "error" /root/frontier-agent/logs/*.log --include="*.log" -l 2>/dev/null | tail -3
sqlite3 /root/frontier-agent/shared_state.db \
  "SELECT * FROM blog_articles WHERE date(ts)=date('now') AND status='error';" 2>/dev/null
# VEIKSMAS: jei klaida vienkartinė (API timeout, WP 500) — pakartoti publikavimą
```

## G. Kilpos uždarymas iki galo: pamoka → taisyklė (naujas darbas)

Dabar lessons.md pamokos taikomos tik tada, kai jas kas nors perskaito. Kad taptų mokymusi:

1. Kiekviena nauja pamoka su tag'u `#quality` ar `#publish` turi automatiškai virsti tikrinama sąlyga `quality_guards.py` arba pre-publish check'u.
2. Minimalus variantas: savaitinis cron, kuris paima naujas lessons.md sekcijas → siunčia LLM su prompt'u „paversk vykdoma quality_guards taisykle arba atsakyk NEAUTOMATIZUOJAMA" → sukuria PR/patch žmogaus peržiūrai.
3. Matavimas: `adapt_rules.json` taisyklių skaičius ir amžius rodomi `hermes_status` išvestyje — kad mokymosi sveikata būtų matoma kasdien, ne kartą per mėnesį.

## H. Memory Palace vertinimas (Letta pakaitalas — patvirtinta savininko 2026-07-02)

Kontekstas: Letta grąžina HTTP 500 (2026-07-02), chat išjungtas („LLM auth dead"). Radaro signalas 2026-05-24: Memory Palace (github.com/AGI-is-going-to-arrive/Memory-Palace) — self-hosted, SQLite, 9 MCP tools, rollback/Write Guard, forgetting curve.

```bash
# H1. Kiek Letta faktų turime (migracijos apimtis)?
# Per MCP: hermes_letta_query įvairiais raktažodžiais arba tiesiogiai Letta API
# Užfiksuoti: faktų skaičių, seniausio/naujausio datą

# H2. Bandomasis diegimas (atskirai nuo prod):
git clone https://github.com/AGI-is-going-to-arrive/Memory-Palace /root/eval/memory-palace
# Perskaityti README: DB schema, MCP tools sąrašas, resource requirements
# KRITERIJAI: (1) ar semantic search prilygsta Letta? (2) ar Write Guard apsaugo nuo
# haliucinuotų faktų? (3) ar rollback veikia? (4) kiek RAM/CPU?

# H3. Migracijos testas: eksportuoti 10 Letta faktų → importuoti → palyginti search rezultatus
# SPRENDIMAS: jei H2-H3 teigiami → migracija į Hermès v2 planą; jei ne → taisyti Letta LLM auth
```

## I. Radaro → veiksmo kilpa (B2 iš backlog'o)

Problema (Štabo 2026-06-15): 10 tier-1 signalų, 0 reakcijų — radar_to_metacog sinergija 0.3.

```bash
# I1. Kur radaras rašo signalus ir kas juos turėtų skaityti?
grep -rn "radar" /root/frontier-agent/src/agents/*.py -l
grep -rn "tier.*1\|tier1" /root/frontier-agent/src/agents/radar*.py | head

# I2. Ar egzistuoja consumer'is? (pagal 2026-04-05 pamoką — modulis gali būti parašytas, bet ne crontab'e)
crontab -l | grep -i radar

# I3. Minimalus fix: tier-1 signalas → automatinis hermes_council pasiūlymas (proposal_type='general')
# → jei council PROCEED → įrašas į backlog/Linear. Tada signalai nebemiega Letta atmintyje.
```

---

## Sėkmės kriterijai (po pataisymų tikrinti po 1-2 savaičių)

| Rodiklis | Dabar | Tikslas |
|----------|-------|---------|
| `adapt_rules.json` amžius | ? (tikrinti A1) | < 48 h visada |
| Streak'ai strategy_log | ? (tikrinti C2) | Auga kasdien |
| CB būsena po cron restarto | ? (tikrinti B) | Išlieka |
| `blog_quality_slope_30d` | **-0.077** 🔴 | **> 0** ✅ |
| Traits šaltinis | ? (tikrinti D1) | shared_state.db |
| Radaro tier-1 signalai → reakcijos | 10 → 0 🔴 | Kiekvienas tier-1 gauna council sprendimą |
| Letta/Memory Palace | Letta HTTP 500 🔴 | Veikianti ilgalaikė atmintis be klaidų |

---

© 2026 MB „Maršalas" — AI sistemų priežiūra. Šaltiniai: lessons.md (L856-L2575), CAG 2026-07-02, hermes_traits 2026-07-02.
