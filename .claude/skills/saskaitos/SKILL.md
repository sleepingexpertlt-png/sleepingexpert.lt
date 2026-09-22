---
name: saskaitos
description: Sleeping Expert LT, MB pardavimo sąskaitų registras ir Finvaldos importas. Naudok, kai buhalterė ar savininkas atsiunčia WooCommerce PDF sąskaitas (OSL serija) ir užsakymų CSV, prašo registro, Finvaldos XML, i.SAF suvestinės, sutikrinimo su WC, trūkstamų ID sąrašo. Triggers: sąskaitos, registras, Finvalda, XML importas, OSL, PVM registras, i.SAF, buhalterija, apskaita, mėnesio uždarymas.
---

# /saskaitos — pardavimo sąskaitų registras ir Finvaldos importas

Įmonė: **Sleeping Expert LT, MB**, į. k. 306722375, PVM LT100016824715. Apskaitos programa: **Finvalda** (importas: Įrankiai → Duomenų importas → XML importas).

## Ką atsiunčia buhalterė

1. **PDF** su WooCommerce sąskaitomis (eksportas iš WC PDF Invoices įskiepio, OSL000XXX serija). Gali būti vienas failas su daug puslapių.
2. **CSV** užsakymų eksportas iš WooCommerce (stulpeliai „Order Number“, „Order Date“, „Order Total Amount“, „Order Total Tax Amount“, „Customer Note“ ir kt.).
3. Laikotarpį (mėnesį) ir ką reikia: registro, Finvaldos XML, abu.

Jei trūksta vieno iš failų, paprašyk jo. Be PDF registro nedaryk (sąskaitų numeriai ir datos imami tik iš PDF).

## Griežtos taisyklės (savininko, 2026-09-22)

1. **Užsakymo data ≠ sąskaitos data.** Registre abi atskirais stulpeliais: „Uzsak. data“ (WC) ir „Sask. data“ (PDF „Sąskaita Data“). Niekada nemaišyti.
2. **Gamintojo užsakymo ID (5 skaitmenys, 5xxxx)** iš PDF lauko „Pastaba“ privalomas stulpelyje „Uzsak. Nr. (is pastabos)“. Formos: `ID 52990`, `52943`, `ID53124`, `UKM 00615/53124` (imti skaičių po `/`). Nėra → įrašyti `TRŪKSTA ID`, pažymėti geltonai ir išvardinti ataskaitoje. 6 skaitmenų ID → pažymėti „PATIKRINTI“.
3. **Sąskaitų numerių niekada nefabrikuoti.** Tik iš PDF (`Sąskaita Numeris`) arba WC meta `_wcpdf_invoice_number`.
4. Registro formatas = esamos Google Sheets lentelės „Sleeping Expert 2026 - VISOS PARDAVIMO SASKAITOS“ formatas (stulpeliai žemiau). Nekurti naujo formato.
5. Sumos sutikrinamos su WC CSV (viso ir PVM). Nesutapimai žymimi raudonai ir išvardinami.
6. Finvalda: datos `YYYY-MM-DD`, dešimtainiai su tašku, XML pretty-printed, UTF-8.

## Registro stulpeliai

`Menuo | Sask. data | Numeris | Klientas | Kli. valstybe | Zurn. | Tipas | PVM % | Kliento PVM kodas | Suma be PVM | PVM | Viso suma | Uzsak. Nr. (is pastabos) | WC uzsak. Nr. | Uzsak. data | Vieta | Pastaba | CSV sutikrinta | Failas`

- Zurn./Tipas visada `PARD`.
- LT klientas: `21%`, `PVM1`. Alina Group (PL, refaktūra): `0% (atvirkst. Art.44)`, `PVM13` registre, pastaba `REVERSE CHARGE - Google Ads refaktura`.
- Juridinis asmuo: `Pavadinimas (k. 123456789)`; Alina: `Alina Group Sp. z o.o. (NIP 5562799519)`.
- Vieta: iš PDF „Vieta:“ (Vilnius / Klaipėda / Ukmergė), kitaip `E-shop`.
- Pastaba: avansas, kvitas, įspėjimai.

## Žingsniai

1. PDF → tekstas: `pymupdf` (sistemos `pypdf`/`pdfplumber` šioje aplinkoje lūžta dėl `cryptography`, todėl daryk venv: `python3 -m venv pdfenv && pdfenv/bin/pip install pymupdf openpyxl`).
2. Paleisk `scripts/saskaitu_registras_parse.py` (PDF tekstas + CSV → `register.json`, XLSX, CSV). Prieš tai atnaujink kelius skripto viršuje arba paduok argumentais.
3. Peržiūrėk išvestį: visos sąskaitos rastos (PDF „PVM SĄSKAITA FAKTŪRA“ skaičius = eilučių skaičius), numeracija be tarpų, sumos = CSV.
4. Finvaldos XML: `python3 scripts/finvalda_pardavimai_xml.py <registras.csv> -o pardavimai_OSL_<nuo>-<iki>_<mėnuo>.xml`. Patikrink `xml.etree` parse. Alinos eilutei XML naudoja `PVM21`/0,00 % (pagal VPS XML šabloną). Eilutės kodas `PAJAMOS` (jei buhalterė sako 5001, `--kodas 5001`).
5. Išvestis buhalterei: XLSX (SendUserFile), Google Sheets kopija tame pačiame Drive aplanke kaip esamas registras (parentId `0AFLk2m9MdL4jUk9PVA`), XML failas.
6. Ataskaita: sąskaitų skaičius, sumos (be PVM, PVM, viso), trūkstamų ID sąrašas, nesutapimai su CSV, numeracijos tarpai lyginant su paskutiniu esamo registro įrašu.

## Kur kas yra

- Kanoninis registras: Google Sheets `📊 SASKAITU_REGISTRAS_2026` (ID `10uQ50qSSify2wo5Llodx10dTC17_jcrvIhfZffBo3C4`).
- Pardavimų lentelės: „VISOS PARDAVIMO SASKAITOS (geguze + birzelis)“ (`1CPxy0kesfuVSsbwjnv-q3VV1UgRHXKtPC1o9rdxbScQ`), „PARDAVIMO SASKAITOS rugpjutis (OSL000851-896)“ (`1ie1K5xRU08DmujcgYUNQiLT-YQpHx2dwO4q5XIltI2o`).
- VPS žinios: `hermes_cag` klausimai apie `reference_finvalda_xml_format.md`, `lessons.md`; Hermes skill'ai `invoice`, `perdavimo-aktas`.
- Taisyklės: `docs/saskaitu-registras.md`.

## Ko nedaryti

- Neatsakinėti teorija apie registrus. Iš karto daryti iš atsiųstų failų.
- Nekurti naujų sąskaitų, kreditinių ar numerių. Tai tik registras ir importas.
- Neapvalinti sumų kitaip nei PDF. PVM imamas iš PDF „įskaičiuota … PVM“, ne skaičiuojamas iš naujo.
