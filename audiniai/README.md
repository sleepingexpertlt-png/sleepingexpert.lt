# Lovų audinių katalogas

Paruoštas blokas puslapiui
`/parduotuve/lovos/lovu-audiniu-meginiai/audiniu-pavyzdziai/`

**80 audinių, 4 tiekėjai, 4 grupės** — tik tai, kas realiai siūloma salonuose.

| Tiekėjas | I | II | III | IV | Viso |
|---|--:|--:|--:|--:|--:|
| Davis | 12 | 7 | — | — | 19 |
| Fargotex | 2 | 6 | 9 | 5 | 22 |
| Top Textil | 15 | 7 | 3 | 1 | 26 |
| Elastron | — | 3 | 6 | 4 | 13 |
| **Viso** | **29** | **23** | **18** | **10** | **80** |

## Failai

| Failas | Paskirtis |
|---|---|
| `audiniai.json` | Duomenys |
| `build.py` | Generatorius |
| `audiniu-katalogas.html` | Rezultatas — įklijuoti į WP „Custom HTML" bloką |

## Kaip publikuoti

1. `python3 audiniai/build.py`
2. Nukopijuoti visą `audiniu-katalogas.html` turinį
3. WP → puslapis → blokas **Custom HTML** → įklijuoti → Atnaujinti

Blokas savarankiškas: CSS ir JS viduje, jokių išorinių bibliotekų, jokių
užklausų. Klasės su prefiksu `se-fab__`, kad nesikirstų su tema.

## Duomenų atnaujinimas

Redaguoti `audiniai.json` → paleisti `build.py` → perkopijuoti HTML.

Šaltinis: savininko pateiktas salonų sąrašas (2026-08-11). Hermès vault'e
(`reference_alina_pricing_rules.md`) yra pilnas gamintojų sąrašas su 367
audiniais ir tiekėju PIK — **jis čia sąmoningai nenaudojamas**.

### Padaryti pataisymai

| Sąraše | Faile | Kodėl |
|---|---|---|
| `Seatlle` | `Seattle` | Rašybos klaida — gamintojo katalogas rašo Seattle |

### Neatitikimai su vault (paliktas salonų sąrašo variantas)

- **Kingston** (Fargotex) — vault rašo `KINGSTONE`
- **Maya** priskirtas Fargotex III — vault turi `MAYA` prie Elastron I
- **Adventure** (Davis) I grupėje — vault turi II grupėje
- **Smart Velvet** (Top Textil) I grupėje — vault turi II grupėje

Verta sutikrinti prieš publikuojant, ypač Maya — skiriasi ir tiekėjas, ir grupė.

## Swatch nuotraukos

Pagal nutylėjimą nuotraukų nėra — rodomi raidiniai vietos rezervai.

Įjungimas:

1. Įkelti nuotraukas į `/wp-content/uploads/audiniai/{tiekėjas}/{audinys}.webp`
   Pvz.: `/wp-content/uploads/audiniai/top-textil/magic-velvet.webp`
2. `python3 audiniai/build.py --images`
3. Perkopijuoti HTML

Slug taisyklė: mažosios raidės, ne raidiniai simboliai → `-`
(`Now or Never` → `now-or-never`, `Grace Collection` → `grace-collection`).

Nuotraukų teisės: swatch'ai priklauso tiekėjams. Prieš keliant turėti raštišką
leidimą arba fotografuoti savo salonų pavyzdžius.

## Kainos

Blokas **nerodo** skaičių — tik grupių pavadinimus. Norint rodyti priemokas,
reikia suskaičiuoti mažmenines EUR sumas (vault'e esančios gr1–gr4 sumos yra
hurt PLN savikaina, jų publikuoti negalima).
