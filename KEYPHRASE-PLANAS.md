# 🔑 Produktų Secondary Keyphrase Planas — 789 Produktai

**Tikslas:** užpildyti tuščią `rank_math_additional_keywords` lauką ir — svarbiausia — įausti antrinius raktažodžius į produktų turinį, kad augtų srautas ir pardavimai. Sudaryta 2026-07-02.

**Faktinė padėtis** (šaltiniai: CLAUDE.md:L21, L71, L144):
- 789 produktai (111 čiužinių + 678 kiti); SEO įskiepis — RankMath
- 91% iš 686 produktų turi `rank_math_focus_keyword` ✅
- `rank_math_additional_keywords` laukas egzistuoja, bet nenaudojamas ❌

## ⚠️ Svarbi tiesa prieš pradedant

`rank_math_additional_keywords` **pats savaime reitingų nekelia** — Google šio lauko neskaito, tai vidinis RankMath analizės laukas. Srautą augina antrinio raktažodžio **įaudimas į turinį**: pavadinimą, trumpą aprašymą, H2, paveikslėlių alt. Todėl planas daro abu dalykus kartu — laukas užpildomas kaip darbo žymuo, o turinys papildomas kaip tikrasis variklis.

## Konvejeris (vykdyti serveryje /root/frontier-agent/)

### 1. Eksportas
WC API → visi produktai: `id, name, slug, url, rank_math_focus_keyword, short_description`. Atranka: turi focus, neturi additional. Rezultatas: darbo sąrašas (~700 eilučių).

### 2. Įrodymais grįsti kandidatai (ne fantazija)
Kiekvienam produkto URL — GSC užklausos per 90 d.: `query, impressions, clicks, position`.
**Antrinio raktažodžio kandidatas** = užklausa, kuri: (a) turi parodymų, (b) nepadengta focus keyword, (c) turi pirkimo intenciją (pvz., „...kaina", „...atsiliepimai", „...160x200", „geriausias ... nugarai").
Produktams be GSC duomenų — kategorijos šablonas (pvz., „{tipas} čiužinys {dydis} kaina") su žyma **BE-GSC-ĮRODYMO**, kad savininkas matytų skirtumą.

### 3. Kokybės filtrai (iš jūsų pačių taisyklių)
- Tik lietuvių kalba, orientuota į LT pirkėją (CLAUDE.md:328)
- JOKIŲ konkurentų pavadinimų — net kaip žodžio dalies (CLAUDE.md:L116)
- JOKIŲ išgalvotų specifikacijų, garantijų, „premium/exclusive" teiginių (CLAUDE.md:L72, feedback failai)
- Įaudimas į aprašymą — tik jei sakinys lieka natūralus ir faktiškai teisingas

### 4. Savininko patvirtinimas (RULE-02 dvasia — prieš rašant į WC, parodyti lentelę)
CSV/lentelė peržiūrai: `produktas | focus | siūlomas secondary | įrodymas (GSC užklausa + parodymai + pozicija) | kur įterpsime`. Tvirtinate bangą — tik tada rašome. Jokio rašymo be patvirtinimo.

### 5. Pilotas — 20 produktų
Atrinkti 20 su daugiausiai GSC parodymų, bet be secondary. Rašymas pagal jūsų saugos taisykles:
- Testas ant draft/private kopijos prieš gyvą (CLAUDE.md:L73)
- Po-veiksmo verifikacija tame pačiame bloke (CLAUDE.md:L75)
- NIEKADA nerašyti `rank_math_schema_*` per API — 500 klaidos rizika (CLAUDE.md:L71)
- Atributų masyvas visada siunčiamas pilnas (CLAUDE.md:L22)

### 6. Matavimas ir plėtra
GSC prieš/po pilotui: 14 d. ir 28 d. — `clicks`, `position` antrinei užklausai, produkto puslapio CTR. Jei pilotas teigiamas → bangos po ~100 produktų per savaitę su ta pačia patvirtinimo lentele. Visa apimtis: ~7 savaitės.

## Kas iš ko

| Vaidmuo | Darbas |
|---------|--------|
| Serverio Claude sesija | 1-3, 5-6 žingsniai (eksportas, GSC, kandidatai, rašymas, matavimas) |
| Savininkas | 4 žingsnis — bangos patvirtinimas (~10 min/banga) + GBP/WP prieigos jei trūksta |
| Ši sesija | Plano priežiūra, rezultatų palyginimas dashboard'e |

---

© 2026 MB „Maršalas". Šaltiniai: hermes_cag 2026-07-02 (CLAUDE.md, lessons.md citatos tekste).
