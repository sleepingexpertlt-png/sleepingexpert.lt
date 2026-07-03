# 🗂️ Dokumentų Priskyrimas — Kuris Failas Kuriai Įmonei / Projektui

Patikrinta 2026-07-02 Linear workspace: **tik viena komanda „SleepingExpert" (SLE)**; Maršalas atskiro Linear projekto NETURI. Šis žemėlapis pašalina painiavą, kylančią dėl to, kad viskas kraunasi į vieną git šaką `claude/marsalas-service-provider-baz5gk`.

## Du juridiniai asmenys (NEmaišyti)

| Įmonė | Turtas | Vaidmuo |
|-------|--------|---------|
| **Sleeping Expert LT, MB** | sleepingexpert.lt, lamele.lt, ši GitHub repo, Hermès AI sistema | Miego prekių retail; AI = pelno svertas |
| **MB „Maršalas"** (kodas 304859731) | cookking.online, marsalas.lt | AI paslaugų teikėjas; diegia/prižiūri agentus |

## Failų priskyrimas

### → Sleeping Expert LT, MB · Linear projektas „Hermès AI Sistema" (SLE)
Visas operacinis darbas — Hermes sistema valdo sleepingexpert.lt:

| Failas | Ką dengia | Linear ticket (kurti VPS'e, kai Linear atrakintas) |
|--------|-----------|------|
| `VPS-BRIEFAS.md` | Vykdymo paketas serveriui | — (viršelis) |
| `AUDITAS-2026-07-02.md` | Sistemos auditas | 🔴 Publish fix; 🔴 OCL auditas |
| `MOKYMOSI-AUDITAS.md` | OCL kilpos patikros A–J | 🔴 Mokymosi kilpos auditas |
| `KEYPHRASE-PLANAS.md` | 789 produktų secondary keyphrase | 🟡 Keyphrase pilotas 20 produktų |
| `TOBULINIMAI.md` | Bendras backlog (P0–P2, B1–B12) | daug — skaidyti pagal eilutes |
| Dashboard (Artifact) | Gyvos metrikos | — (stebėjimo įrankis) |

### → MB „Maršalas" · pozicionavimas (Linear projekto nėra — kandidatas naujam)
Paslaugų teikėjo tapatybė ir pardavimo medžiaga:

| Failas | Ką dengia |
|--------|-----------|
| `MARSALAS.md` | Įmonės profilis, rekvizitai, valdomi projektai |
| `PASLAUGA.md` | Paslaugos vienpuslapis (done-for-you AI diegimas) |
| `AI-ORG.md` | „Conducting AI" agentų org schema |
| `RADAR-SIGNALAI.md` | Dalis (Twenty CRM, Cybersecurity) → Maršalas paslaugoms; kita dalis (stop-slop, awesome eval, ECC) → Sleeping Expert Hermès |

## Kur būsimas darbas turi gulti

- **Bet kas apie sleepingexpert.lt turinį, SEO, agentus, blogą, WooCommerce, mokymąsi** → Sleeping Expert / Hermès AI Sistema (SLE).
- **Bet kas apie AI paslaugos pardavimą klientams, marsalas.lt platformą, cookking.online** → Maršalas.
- **Abejojant:** ar tai kelia sleepingexpert.lt pardavimus (→ SE), ar tai Maršalas parduoda paslaugą kitiems (→ Maršalas)?

## Atviri organizaciniai klausimai savininkui

1. **Linear ticketai užblokuoti** (nemokamas limitas viršytas) — operaciniam darbui ticketai laukia arba Linear plano, arba kuriami VPS sesijoje vėliau.
2. **Ar kurti atskirą git repo / Linear komandą Maršalas?** Dabar Maršalas pozicionavimas guli Sleeping Expert repozitorijoje — techniškai veikia, bet ilgainiui verta atskirti (pvz., repo `marsalas` arba `marsalas.lt`).

---

© 2026. Sudaryta iš Linear workspace patikros (SLE komanda, 4 projektai) ir 2026-07-02 darbo.
