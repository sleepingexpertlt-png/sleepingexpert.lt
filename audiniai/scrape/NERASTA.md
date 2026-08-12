# Scraping ataskaita — VPS sesija (2026-08-11)

## Statistika pagal tiekėją

| Tiekėjas | Kolekcijų (sąraše) | Rasta | Kodų iš viso |
|---|---|---|---|
| Davis | 19 | 19/19 | 429 |
| Fargotex | 22 | 22/22 | 349 |
| Top Textil | 26 | 26/26 | 658 |
| Elastron | 13 | 12/13 | 185 |
| **Viso** | **80** | **79/80** | **1621** |

`import_swatches.py --dry-run` patvirtino: 79/80 kolekcijų su kodais, 0 dublikatų,
0 nežinomų kolekcijų (visi pavadinimai sutapo su `audiniai.json`).

## Nerasta (1)

- **Elastron / Fox** — kolekcijos svetainėje `elastrongroup.com` nėra. Patikrinta
  dviem būdais: (1) pilnas katalogas per `/collections/all/products.json` (188
  produktų, jokio "Fox"), (2) svetainės paieška `?q=fox` — 0 rezultatų. Tikėtina,
  arba pervadinta, arba nutraukta.

## Pavadinimų neatitikimai (kodus surinkau, bet svetainės pavadinimas kitoks)

Pagal taisyklę #2 — mūsų `audiniai.json` pavadinimo NETAISIAU, tik fiksuoju čia:

| Mūsų sąrašas | Tiekėjo svetainėje | Tiekėjas |
|---|---|---|
| Lincoln | **Lincoln LN** + **Lincoln D** (du atskiri puslapiai) | Davis |
| Nube | **Nube DB** | Davis |
| Seatlle | **Seattle** (tikėtina rašybos klaida mūsų sąraše) | Elastron |
| Ruggia | **Rugia** (viena raide "g" mažiau) | Top Textil |
| Baloo | **Baloo Boucle** (slug: `balooboucle`) | Top Textil |

**Lincoln** — Davis šią kolekciją dabar dalina į du atskirus produktus (LN ir D,
tikėtina skirtinga medžiaga/sudėtis). Surinkau kodus iš ABIEJŲ puslapių po mūsų
bendru pavadinimu "Lincoln" (28 kodai iš viso) — jei reikia atskirti, reikės
sprendimo, kurį variantą (ar abu) rodyti kaip "Lincoln".

## Elastron — nėra atskiro užsakymo kodo, tik spalvos pavadinimas

Elastron (Shopify parduotuvė) NETURI atskiro skaitinio užsakymo kodo — jų
sistemoje spalva identifikuojama TIK pavadinimu (pvz. "Gold", "Pearl", "Sand").
Shopify `variant.sku` laukas visiems tuščias. Todėl CSV stulpelyje `kodas`
įrašytas spalvos pavadinimas (tas pats kas `spalva` stulpelyje) — tai NE
išgalvotas kodas, o tikras, svetainėje rodomas identifikatorius, tiesiog
teksto, ne skaičiaus formato.

## Kaip radau kodus — pagal tiekėją

- **Davis** — WordPress svetainė, kodas failo varde iškart po kolekcijos slug'o
  (`aragon-03_ARAGON-03.jpg`). Naudojau `product-sitemap.xml`, kad rasčiau visus
  `/kolekcja/{slug}/` adresus.
- **Fargotex** — WordPress/WooCommerce, kodas paimtas iš `data-large_image`
  atributo (WooCommerce standartinis pilnos raiškos nuorodos atributas), kodas —
  pirmas skaičius faile po kolekcijos pavadinimo. Naudojau `product-sitemap.xml`.
- **Top Textil** — WordPress (Bricks Builder), kodas TIESIOGIAI nurodytas
  `data-title="228.01"` atribute prie kiekvienos galerijos nuotraukos — patikimiausias
  šaltinis iš visų keturių, nes tai eksplicitinis tekstas, ne spėjimas iš failo
  vardo. Naudojau `wp-sitemap-posts-kolekcja-1.xml`.
- **Elastron** — Shopify, `/collections/{handle}/products.json` API grąžina
  visus variantus (spalvas) su nuotraukomis vienu užklausimu, be HTML parsinimo.

## robots.txt patikra

| Tiekėjas | Rezultatas |
|---|---|
| Davis | Pilnai atviras (`Disallow:` tuščias) |
| Fargotex | Bendras `User-agent: *` leidžia (tik admin/logs keliai uždrausti); AI-training botai (GPTBot, Google-Extended, meta-externalagent) eksplicitiškai blokuoti — mes jais nesinaudojome |
| Top Textil | `robots.txt` neegzistuoja (404) — jokių apribojimų nedeklaruota |
| Elastron | Eksplicitiškai `Allow: /`, pati svetainė rekomenduoja naudoti `/products.json` API |

Visur laikytasi ≥0.7s pauzės tarp užklausų tam pačiam host'ui.

## Pastaba dėl teisių (primenu)

Kodai ir nuotraukų NUORODOS surinkti — tai TIK duomenys, ne leidimas jas
publikuoti sleepingexpert.lt. Laiškai tiekėjams (`uzklausa-tiekejams.md`) vis
tiek reikalingi prieš viešinant.
