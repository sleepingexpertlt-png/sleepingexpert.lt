# Local inventory feed — patvirtintas formatas (2026-08-28)

Klausimas kilo, nes dokumentacija tą pačią reikšmę rašo dviem formatais.
Atsakymas gautas ne iš atminties: VPS perskaitė `generate_merchant_feed.py`
ir patikrino Google dokumentaciją per raw HTML (ne per AI perfrazavimą).

## Kuris kanalas mūsų

`generate_merchant_feed.py` generuoja **klasikinį RSS/XML Google Shopping
feed'ą** (`xmlns:g="http://base.google.com/ns/1.0"`) ir kelia jį kaip
statinį failą. Jokio `googleapis.com`, `content/v2` ar `merchantapi`
kreipinio faile nėra.

**Vadinasi galioja feed atributų formatas, ne Merchant API proto enum.**

| Kanalas | `pickup_method` literalas |
|---|---|
| **RSS/XML feed — MŪSŲ** | `ship to store` (tarpas, mažosios) |
| Merchant API REST/JSON | `SHIP_TO_STORE` (proto enum) |

## Verslo modelis → laukai

Ekspozicija skiriasi, **sandėlis bendras, kiekviena parduotuvė parduoda viską.**
Google tai tiesiogiai numato: pardavėjai su `ship to store` „must be able to
fulfill store pickup orders even when a product isn't physically in-stock at
your store locations".

| Situacija | `availability` | `pickup_method` | `pickup_SLA` |
|---|---|---|---|
| Stovi salone, išsinešama | `in_stock` | `buy` | `same day` |
| Stovi salone, užsakomas | `on_display_to_order` | `reserve` | `2-day` … |
| Salone nestovi, parduodam | **ne** `in_stock` | `ship to store` | pagal atvežimą |

Trečia eilutė = ~90 % katalogo.

## Kas dar blokuoja LIA

- store code VNO / KLP / UKM
- GMC ↔ Business Profile susiejimas
- per-parduotuvės fizinio inventoriaus sąrašas iš owner'io

## Sprendimas dėl eiliškumo

**LIA atidėtas.** Iki 2026-10-24 tikslo (maršrutai 32→44) jis nespėja:
store codes, susiejimas, feed'as, Google patvirtinimas — savaitės.

Šiandien daromas kitas dalykas: **produktų vitrina GBP profilyje** per
GMC katalogą. Tam LIA nereikia.
