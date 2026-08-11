# Užduotis VPS Claude Code sesijai

Nukopijuok viską žemiau į Claude Code sesiją, paleistą VPS'e (ten tinklas
atviras). Pirma `git pull` šitą repo, kad turėtų `audiniai/`.

---

## Užduotis

Surinkti gamintojų spalvų kodus ir swatch nuotraukas 80-čiai audinių, kuriuos
Sleeping Expert siūlo salonuose.

**Šaltiniai:**

| Tiekėjas | Adresas |
|---|---|
| Davis | https://www.davis.pl/en/collections/ |
| Fargotex | https://fargotex.pl/kategoria-produktu/tkaniny-obiciowe/ |
| Top Textil | https://www.toptextil.pl/tkaniny/ |
| Elastron | https://www.elastrongroup.com/collections/all |

**Kurias kolekcijas rinkti:** tik tas, kurios yra `audiniai/audiniai.json`.
Sąrašas — `audiniai/uzklausa-tiekejams.md` apačioje. Nieko nepridėti.

## Rezultatas

Vienas failas: `audiniai/scrape/swatches.csv`

```csv
tiekejas,kolekcija,kodas,spalva,url
Davis,Aragon,03,Beige,https://www.davis.pl/media/aragon-03.jpg
Davis,Aragon,06,Graphite,https://www.davis.pl/media/aragon-06.jpg
```

| Stulpelis | Ką rašyti |
|---|---|
| `tiekejas` | Tiksliai: `Davis`, `Fargotex`, `Top Textil`, `Elastron` |
| `kolekcija` | Tiksliai kaip `audiniai.json` (`Matt Velvet`, ne `MATTVELVET`) |
| `kodas` | Gamintojo užsakymo kodas, kaip svetainėje |
| `spalva` | Spalvos pavadinimas, jei yra. Nėra — palikti tuščią |
| `url` | Tiesioginis nuotraukos adresas. Rinktis didžiausią raišką |

Grupės į CSV **nerašyti** — ji jau žinoma iš `audiniai.json`.

## Taisyklės

1. **Kodų neišgalvoti.** Jei kolekcijos svetainėje nėra arba kodai neaiškūs —
   palikti ją be eilučių ir surašyti į `NERASTA.md`. Klaidingas kodas reiškia
   ne tos spalvos užsakymą.
2. **Pavadinimų netaisyti.** `Seatlle`, `Kingston` — palikti kaip
   `audiniai.json`, net jei svetainėje kitaip. Neatitikimus surašyti į
   `NERASTA.md`.
3. **Gerbti `robots.txt`** ir daryti pauzę ≥0.5 s tarp užklausų. Skubėti nėra
   kur.
4. **Naudoti Playwright**, jei turinys kraunamas JS (Elastron — Shopify, ten
   veikia `/collections/{handle}/products.json`).
5. **Nieko nepublikuoti** — tik sugeneruoti CSV ir pushinti į šaką.

## Kai CSV paruoštas

```bash
cd audiniai/scrape
python3 import_swatches.py swatches.csv --dry-run   # patikrinti ataskaitą
python3 import_swatches.py swatches.csv             # įrašyti
cd .. && python3 build.py --images
```

`import_swatches.py` pats atsisiunčia nuotraukas, konvertuoja į `.webp`,
pervadina pagal slug taisyklę ir sulieja kodus į `audiniai.json`. Kolekcijos,
kurios nėra mūsų sąraše, atmetamos automatiškai.

Rezultatą — `swatches.csv`, `NERASTA.md`, `out/` ir atnaujintą
`audiniai.json` — commit'inti į `claude/labas-lhrx8j`.

## Ataskaita

Pabaigus parašyti:
- kiek kodų surinkta iš kiekvieno tiekėjo
- kurių kolekcijų nerasta ir kodėl
- kur svetainės pavadinimai skyrėsi nuo mūsų sąrašo
- ar buvo `robots.txt` apribojimų

---

## Pastaba dėl teisių

Nuotraukos priklauso tiekėjams. Rinkti jas techniškai galima, bet publikuoti
sleepingexpert.lt reikia jų leidimo — laiškai paruošti
`audiniai/uzklausa-tiekejams.md`. Verta išsiųsti lygiagrečiai, nelaukiant
scrapinimo pabaigos.
