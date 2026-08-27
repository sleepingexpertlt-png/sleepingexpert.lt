# Temų paklausos tyrimas — ką žmonės realiai klausia (owner GO 2026-08-27)

Owner tikslus formulavimas: *„ne turinį kopijuosime, o mums reikia temas žinoti,
apie ką cituojama. Mes esame ekspertai ir nežinome, ko reikia žmonėms. Esame
atviri pasidalinimui."*

Tai **paklausos** tyrimas, ne formato. Ir jo duomenys jau nupirkti.

## RADINYS: duomenys jau yra, nenaudoti nuo 2026-08-03

`data/elmo_snapshot_2026-07-18/`:
- **6 108 citatos**
- **1 125 prompt paleidimai**
- **111 promptų** (= 111 klausimų, kuriuos žmonės kelia AI miego/čiužinių temoje)
- **7 konkurentai**

Eksportuota, kai Elmo buvo pauzintas dėl kaštų (U-014/R-050), kad vienintelis
turtingas duomenų langas nedingtų. Nuo tada niekas jo neatidarė.

Tai TIESIOGIAI atsako į owner klausimą. Pirkti naujus duomenis prieš iškasant
šituos būtų kartojimas tos pačios klaidos (Ahrefs vietoj GSC).

## Seka (griežtai šia tvarka)

| # | Žingsnis | Kaina |
|---|---|---|
| 1 | Iškasti Elmo snapshot'ą: temų klasifikacija, citavimo dažnis, kas cituojamas | **0 €** |
| 2 | Sukryžminti su GSC 5–15 zona + `question_bank_master.json` + `wp_faq` | **0 €** |
| 3 | Pirkti (LLM Source Annotations) TIK tai, ko po 1–2 vis dar trūksta | pagal poreikį |

## 1 žingsnio konkretus rezultatas

Iš 111 promptų ir 6 108 citatų padaryti:

1. **Temų žemėlapis** — į kokias grupes skyla klausimai (pasirinkimas / sveikata /
   priežiūra / kainos / garantijos / palyginimai / problemos)
2. **Dažnio eilė** — kurios temos generuoja daugiausiai klausimų
3. **Kas atsakinėja** — kurie domenai cituojami dažniausiai kiekvienoje temoje
4. **MŪSŲ SPRAGA** — temos, kur klausimų daug, o mūsų nėra visai. Tai
   prioritetų sąrašas turiniui.
5. **Konkurentų spraga** — temos, kur NIEKAS gerai neatsako. Tai vertingiausia:
   laisva vieta.

## 2 žingsnio kryžminimas

- Tema yra Elmo duomenyse IR GSC 5–15 → **aukščiausias prioritetas** (paklausa
  patvirtinta dviem nepriklausomais šaltiniais)
- Tik Elmo → AI paklausa be Google paklausos → AEO taikinys
- Tik GSC → klasikinis SEO taikinys
- Nei vienur → nekurti

## 3. ATVIRAS PASIDALINIMAS — strateginis ėjimas

Owner: *„esame atviri pasidalinimui."*

Iš šio tyrimo padaryti **viešą LT miego klausimų tyrimą** — originalius duomenis,
kurių neturi nė vienas konkurentas: kiek klausimų, kokios temos, kaip pasiskirsto.

Kodėl tai stipriausias turinys, kurį galim padaryti:
- **T1 (unikali vertė):** pirminiai duomenys, ne perpasakojimas. Būtent to
  reikalauja 2026-08 spam update.
- **E-E-A-T:** tyrimas su metodika ir skaičiais = ekspertizės įrodymas, ne deklaracija.
- **Citabilumas:** AI cituoja pirminius šaltinius. Tapdami šaltiniu, nustojam
  konkuruoti dėl citatos — tampam ja.
- **Kaina: 0 €.** Duomenys jau turimi.

Metodika skelbiama atvirai (imtis, laikotarpis, ribos) — kitaip tai nebus
pasitikėjimo vertas šaltinis.

## Saugikliai

- Konkurentų vardai viešame tyrime — tik faktiniai skaičiai, jokių vertinimų
  (žr. „competitor-name leak guard", L72).
- Snapshot yra 2026-07-18 — **skelbiant nurodyti datą**, nevadinti „dabartiniu".
- Jei duomenys pasirodys per skurdūs išvadai — rašom „nepakanka", neskelbiam.
