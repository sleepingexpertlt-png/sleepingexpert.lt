# Ką „top 3 garantuotojai" realiai daro GMB reitingui — ir ką darysim mes
(2026-08-25 naktinis tyrimas)

Llamamaps viešai savo metodo neatskleidžia, bet šios rūšies agentūrų playbook'as
žinomas. Svorių realybė: proximity ~55 % (nekontroliuojama), GBP signalai ~32 %
(didžiausias VALDOMAS svertas; stipriausias vienas signalas — PAGRINDINĖ
kategorija), likusi dalis — atsiliepimai/citatos/elgsena.

## Balta zona (veikia, darysim / jau darom)

| Svertas | Būklė pas mus | Veiksmas |
|---|---|---|
| **Pagrindinė kategorija** (stipriausias signalas) | ⚠️ P-064: Vilniuje kategorijos lenkiškai | AUDITAS: visų 3 lokacijų primary category = „Čiužinių parduotuvė" (Mattress store), ne „Baldų parduotuvė"; antrinės: lovos, miegamojo baldai |
| **Atsiliepimų TEMPAS** (steady > burst) | Review draftai automatizuoti; srauto sistema — ne | QR kortelės prie kasų su tiesioginiu review link kiekvienai lokacijai + pardavėjų SOP „paprašyk po pirkimo" |
| Atsakymai į atsiliepimus <48h | ✅ gbp-review-agent (draft+QA) | veikia |
| **Šviežios nuotraukos kas mėnesį** (realios!) | Rankinis, nereguliarus | Mėnesio SOP: 3–5 realios salono nuotraukos/lokacijai |
| GBP postai reguliariai | ✅ automatizuota | veikia |
| Q&A seeding | Rankinis (API miręs) | 8 kl./lokacijai — owner SOP (jau PROMISES) |
| Citatos / NAP nuoseklumas | Dalinis (baldurojus.lt, statyba.lt) | NAP suvienodinimo perėjimas per LT katalogus |
| Lokacijų landing puslapiai | ✅ /locations/ yra | Sujungti su kategorijų SEO darbu |

## Pilka/juoda zona (ką „garantuotojai" dažnai daro — mums NE)

- **Pirkti/skatinti fake atsiliepimai, review gating** → profilio suspensija; NE.
- **Keyword-stuffed pavadinimas** (pvz. „X — Čiužiniai Vilnius Pigiai") →
  guidelines pažeidimas; NE mums, BET: patikrinti, ar Vilniaus konkurentai
  (Lonas ×2, Miego Centras) taip daro — jei taip, „Suggest an edit" report'as
  yra legalus būdas išlyginti žaidimo lauką.
- **CTR manipuliacija botais** (paieškos+maršrutų imitacija) → trumpalaikis
  efektas (dienos–savaitės), policy pažeidimas, atpažįstama; NE.
- **EXIF geotagging į nuotraukas** → 2026 m. duomenimis nebe tik neveikia, bet
  gali kenkti („poison pill"); NE.
- **Masinės šlamšto citatos** → nulinė/neigiama vertė; NE.

Išvada apie Llamamaps „garantiją": tikėtina, kad jų rezultatas = kategorijų
sutvarkymas + atsiliepimų velocity + postai/nuotraukos (balta) ir galimai
pavadinimo žaidimai/CTR paslaugos (pilka). Baltą dalį mes automatizuojam
geriau; pilkos mums nereikia — rizika > nauda su gyvu verslu.

## Nauji veiksmai į backlog'ą (owner GO nereikia tyrimui, reikia vykdymui)

1. **Kategorijų auditas 3 lokacijoms** (P-064 išplėtimas) — didžiausias
   valdomas svertas, 15 min GBP UI.
2. **Review velocity sistema:** per VPS sugeneruoti kiekvienos lokacijos
   `g.page` review link + QR (place_id jau turim iš geo-grid) → spausdinti
   kortelės prie kasų + pardavėjų SOP.
3. **Konkurentų pavadinimų patikra Vilniuje** iš geo-grid duomenų (top-3
   konkurentai kiekviename taške jau surinkti) — jei keyword-stuffing,
   report'inti.
4. Mėnesinis nuotraukų SOP (realios, be EXIF žaidimų).

Šaltiniai: Whitespark-tipo faktorių pasiskirstymas, 2026 GBP gidai
(digitalapplied, teknoppy, cited.so), CTR manipuliacijos rizikos analizės
(seo.ai, citationbuilderpro), geotag „poison pill" (kingofpressurewash 2026).
