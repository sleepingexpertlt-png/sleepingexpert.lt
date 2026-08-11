# Lovų audinių katalogas

Paruoštas blokas puslapiui
`/parduotuve/lovos/lovu-audiniu-meginiai/audiniu-pavyzdziai/`

## Failai

| Failas | Paskirtis |
|---|---|
| `audiniai.json` | Duomenys — 367 audiniai, 5 tiekėjai, 4 grupės |
| `build.py` | Generatorius |
| `audiniu-katalogas.html` | Rezultatas — įklijuoti į WP „Custom HTML" bloką |

## Kaip publikuoti

1. `python3 audiniai/build.py`
2. Nukopijuoti visą `audiniu-katalogas.html` turinį
3. WP → puslapis → blokas **Custom HTML** → įklijuoti → Atnaujinti

Blokas savarankiškas: CSS ir JS viduje, jokių išorinių bibliotekų, jokių užklausų.
Klasės su prefiksu `se-fab__`, kad nesikirstų su tema.

## Duomenų atnaujinimas

Redaguoti `audiniai.json` → paleisti `build.py` → perkopijuoti HTML.

Šaltinis: Hermès vault `reference_alina_pricing_rules.md:40-166`
(*Łóżka 2026 GRUPY TKANIN*).

⚠️ **Prieš publikuojant sutikrinti su `WYKAZ-TKANIN-SALONY-2026.pdf`** — vault
duomenys paimti iš kainodaros taisyklių, ne iš salonų sąrašo. Sąrašai gali
skirtis (pvz. PIK yra vault'e, bet jo nebuvo tiekėjų nuorodose).

## Swatch nuotraukos

Pagal nutylėjimą nuotraukų nėra — rodomos raidinės vietos rezervas.

Įjungimas:

1. Įkelti nuotraukas į `/wp-content/uploads/audiniai/{tiekėjas}/{audinys}.webp`
   Pvz.: `/wp-content/uploads/audiniai/elastron/royal-suede.webp`
2. `python3 audiniai/build.py --images`
3. Perkopijuoti HTML

Slug taisyklė: mažosios raidės, ne raidiniai simboliai → `-`
(`ROYAL SUEDE` → `royal-suede`, `DOT LN` → `dot-ln`).

Nuotraukų teisės: swatch'ai priklauso tiekėjams (Davis, Fargotex, Toptextil,
Elastron, PIK). Prieš keliant turėti raštišką leidimą arba fotografuoti savo
salonų pavyzdžius.

## Kainos

Blokas **nerodo** skaičių — tik grupių pavadinimus. Vault'e esančios gr1–gr4
kainos yra **hurt PLN** (savikaina iš Alina Group), ne mažmena. Jų publikuoti
negalima. Norint rodyti priemokas — pirma suskaičiuoti mažmenines EUR sumas.
