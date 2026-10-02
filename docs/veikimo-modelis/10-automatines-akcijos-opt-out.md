# Google Ads „Automated promotions" — SPRENDIMAS: IŠJUNGTI

**Data:** 2026-10-02
**Deadline:** 2026-10-12 (Google įjungia automatiškai, opt-in be mūsų sutikimo)

## Kas keičiasi

Nuo 2026-10-12 Google Ads pats nuskaito mūsų svetainę, išrenka „akcijas"
(kuponus, nuolaidas) ir prikabina jas kaip promotion assets prie Search ir
PMax kampanijų, **kurios turi location assets ir dar neturi promotion assets**.
Google įjungia mus automatiškai. Išjungiama tik paskyros lygmeniu.

Mūsų paskyra 7015063449 atitinka kriterijus 100 %: visos kampanijos turi
location assets, promotion assets neturime nė vienos.

## Faktai iš svetainės (2026-10-02, WooCommerce Store API)

`GET /wp-json/wc/store/products?on_sale=true` → ~47 produktai pažymėti
„akcijoje". Patikrinus `regular_price` vs `sale_price`:

| Produktas | Įprasta | Akcija | Nuolaida |
|---|---|---|---|
| Lova BIANCA Sleeping Expert | 635,00 € | 585,00 € | −7,9 % |
| Lova Astrid Sleeping Expert | 888,00 € | 799,00 € | −10,0 % |
| likę ~45 | = | = | **0 % (sale_price == regular_price)** |

Tai reiškia dvi rizikas vienu metu:
1. **Tikra nuolaida** (iki −10 %) nuteka į vietinius / Maps skelbimus.
2. **Netikra nuolaida** — ~45 produktai su „akcijos" žyme be jokios nuolaidos.
   Būtent iš tokių duomenų gimsta klaidinantis skelbimas.

## Kodėl išjungiame

**1. Maržos matematika.** Salono AOV = 1 013,30 € (measured_at 2026-09-28).
Automatinė −10 % akcija vietiniame skelbime = **−101 € nuo kiekvieno salono
pardavimo**. Prie ~47 salono pardavimų/mėn. tai iki **4 700 €/mėn.** maržos.
Visas reklamos biudžetas = 1 441 €/mėn. Rizika 3× didesnė už visą kanalą.

**2. Nuolaidos dydžio nenustatome mes.** Scraperis pats pasirenka, kurį
pasiūlymą rodyti, kokiomis sąlygomis ir kada. Mes nekontroliuojame nei
procento, nei galiojimo datų, nei to, ar akcija veikia fizinėje parduotuvėje.
Klientas atvyksta į saloną su skelbimu, kurio personalas nežino.

**3. Paskyra jau turi policy problemų.** Image quality atmesta 4 asset
grupėse, „Destination not working" — Miegamojo baldų parduotuvė / Helios
Klaipėda. Automatiškai sugeneruota akcija iš ~45 netikrų „sale" žymų =
realus kandidatas į „misleading offer". Dar vienas policy smūgis šiai
paskyrai nepriimtinas.

**4. Mūsų tikslas nėra nuolaidų pirkėjas.** Pilaitė: 34 % apyvartos,
884 € vidutinis krepšelis. Centras: 1 407 €. Nuolaidų signalas traukia
priešingą segmentą nei tas, kurį auditas parodė kaip vertingiausią.

## Veiksmas (reikia owner rankos — API kelio nėra)

Google Ads → **Settings → Account settings → Automated assets**
→ **Automated promotions → Off**

Atlikti **iki 2026-10-11**.

Kodėl ne per API: paskyros lygmens automated assets nustatymo Google Ads API
neeksponuoja (API `AssetAutomationSetting` liečia tik PMax teksto
automatizaciją, kampanijos lygmeniu). Šioje sesijoje Ads rašymo kelio nėra
apskritai: `hermes_ads_mutate` neprieinamas, Porter neautorizuotas,
Windsor išjungtas owner sprendimu (K19).

## Alternatyva, kurios NEsirenkame

Prikabinti savo kontroliuojamą promotion asset — tai irgi išjungtų
automatinį scraperį (taikoma tik kampanijoms „that don't already have
promotion assets"). Atmetame: tai reikštų savanoriškai pradėti nuolaidų
komunikaciją 1 013 € AOV kanale. Opt-out be jokios akcijos yra teisingas
pasirinkimas.

## Antra, atskira problema, kurią šie faktai atskleidė

~45 produktai svetainėje turi `on_sale` žymę su `sale_price == regular_price`.
Tai klaidina pirkėją ir dabar, be jokio Google. Taisyti WooCommerce — nuvalyti
`_sale_price` tiems produktams, kurie nėra akcijoje.
