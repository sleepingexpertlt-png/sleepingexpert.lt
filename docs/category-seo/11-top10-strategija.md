# GSC 5–15 rezultatai ir strategija (2026-08-25/26)

Įvykdyta: 191 kvalifikuojanti užklausa → question_bank 5889→5971 (82 nauji,
109 papildyti, backup patikrintas). Klasės: 71 TAISYTI / 120 RAŠYTI.
Taikinio #1 („koks geriausias čiužinys lietuvoje") citabilumo draft'as
paruoštas (€0, rule-based; live puslapis nepaliestas).

## ⚠️ Divergence užfiksuota

Kanoninis kontekstas iš kokybes-auditas sesijos teigė, kad egzistuoja
`tools/recommend.py` — **failo NĖRA** (repo yra auditor.py, site_scorer.py,
wai_calc.py). Klasifikacija atlikta skaidria VPS euristika (dedikuotas turinio
puslapis → TAISYTI; kategorija/homepage/tag → RAŠYTI). Grąžinti šį faktą į
kokybes-auditas sesiją, kad ledgeris atitiktų realybę.

REKOMENDACIJA (laukia owner GO): formalizuoti euristiką kaip
`kokybes-auditas/tools/recommend.py` — deterministinis, be LLM kaštų, kad
klasės būtų stabilios savaitė iš savaitės ir atitiktų kanoninį aprašą.

## Prioritetų logika: € tikslas > srautas

90 d. tikslas — įrodyti grandinę veiksmas→citavimas→srautas→užsakymas, todėl
pirmenybė KOMERCINĖMS užklausoms, ne didžiausiam srautui.

### Banga 1 — TAISYTI draft'ai (laukia owner GO, ~€0.3–0.75 viso, telpa į ≤1 €/d.)

| Pri | Keyword | Pozicija | Kodėl |
|---|---|---|---|
| 1 | geriausi spyruokliniai čiužiniai | **4.58** | Arčiausiai top 3 — mažiausias postūmis, komercinė |
| 2 | kur internetu pirkti čiužinį lietuvoje | 5.6 | Tiesioginis pirkimo intent — geriausia €-grandinės kandidatė |
| 3 | pagalvės miegui (2 kw → vienas puslapis) | 8.8/12.6 | 1752 impressions, komercinė, /geriausios-pagalves-2025/ |
| 4 | koks čiužinys tinka alergiškiems | 6.94 | Komercinė-informacinė, aiškus DUK formatas |
| 5 | čiužinio užvalkalas 160x200 | 7.89 | Produkto puslapis — dydžių lentelė |

### Banga 2 — srauto/autoriteto žaidimas (atskiras GO)

- „sapnų reikšmės" (2 kw, **5716 impressions**, pos 5.3–6.9) — didžiausias
  srauto magnetas sąraše, bet pirkimo intent žemas. Vertė: AI discovery /
  autoritetas / retargeting auditorija. Daryti PO 1 bangos.

### NE-taikiniai

- #7 „sulankstomas čiužinys" → /zyma/ (tag) puslapis — į tag puslapį
  neinvestuoti; jei užklausa verta, jai reikia turinio puslapio (RAŠYTI eilė).

## Struktūrinė įžvalga — kategorijų praturtinimas (atskira darbo linija)

Dauguma iš 120 RAŠYTI atvejų nukreipia į KATEGORIJŲ puslapius, kurie patys
rikiuojasi 5–15. Tai reiškia: dažnai reikia ne naujo straipsnio, o kategorijos
puslapio praturtinimo (intro atsakymo blokas, DUK + FAQPage schema, palyginimo
lentelė kategorijos viršuje/apačioje). Pasiūlymas: pilotas su 2 kategorijomis,
kurias VPS duomenys rodo stipriausiai (išsirinkti iš top-30 pagal impressions),
DRAFT režimu, po 1 bangos rezultatų.

## Owner GO sąrašas (kiekvienam atskirai taip/ne)

1. GO formalizuoti recommend.py (0 € LLM, vienkartinis failas kokybes-auditas repo).
2. GO 1 bangos 5 draft'ams (~€0.3–0.75; TIK draft, publikuoja owner).
3. GO/vėliau: „sapnų" puslapio citabilumas (2 banga).
4. GO/vėliau: 2 kategorijų praturtinimo pilotas (po 1 bangos matavimo).
