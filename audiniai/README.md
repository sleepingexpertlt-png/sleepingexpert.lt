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

## Gamintojo spalvų kodai

Užsakymai vykdomi pagal gamintojo kodą, todėl kortelėje turi būti ne tik
kolekcijos pavadinimas, bet ir konkretus kodas (`Monolith 48`).

Audinys `audiniai.json` faile gali būti aprašytas dviem būdais:

```jsonc
"I": [
  "Castel",                                        // kolekcija be kodų
  { "vardas": "Aragon", "spalvos": ["03", "06"] }  // kolekcija su kodais
]
```

Kai nurodytos `spalvos`, kiekvienas kodas gauna **atskirą kortelę** su užrašu
`Kodas: Aragon 03`, o paieška randa ir pagal pavadinimą, ir pagal kodą.

⚠️ **Kodus rašyti tik iš gamintojo katalogo.** Neteisingas kodas = ne ta
spalva užsakyme. Šiuo metu nė vienam iš 80 audinių kodų nėra — laukiama
tiekėjų duomenų.

## Duomenų atnaujinimas

Redaguoti `audiniai.json` → paleisti `build.py` → perkopijuoti HTML.

Šaltinis: savininko pateiktas salonų sąrašas (2026-08-11). Hermès vault'e
(`reference_alina_pricing_rules.md`) yra pilnas gamintojų sąrašas su 367
audiniais ir tiekėju PIK — **jis čia sąmoningai nenaudojamas**.

Pavadinimai, tiekėjai ir grupės perrašyti **pažodžiui** iš salonų sąrašo —
savininko sprendimu niekas netaisoma.

### Neatitikimai su vault (žinomi, sąmoningai palikti)

| Salonų sąraše | `reference_alina_pricing_rules.md` |
|---|---|
| `Seatlle` (Elastron II) | `SEATTLE` |
| `Kingston` (Fargotex I) | `KINGSTONE` |
| `Maya` — Fargotex III | `MAYA` — Elastron I |
| `Adventure` — Davis I | Davis II |
| `Smart Velvet` — Top Textil I | Top Textil II |

Fiksuota 2026-08-11. Jei kada bus sutikrinta su Alina — atnaujinti čia.

## Swatch nuotraukos

Pagal nutylėjimą nuotraukų nėra — rodomi raidiniai vietos rezervai.

Įjungimas:

1. Įkelti nuotraukas į `/wp-content/uploads/audiniai/{tiekėjas}/{audinys}.webp`
   Pvz.: `/wp-content/uploads/audiniai/top-textil/magic-velvet.webp`
2. `python3 audiniai/build.py --images`
3. Perkopijuoti HTML

Slug taisyklė: mažosios raidės, ne raidiniai simboliai → `-`
(`Now or Never` → `now-or-never`, `Grace Collection` → `grace-collection`).

Kai audinys turi spalvų kodus, slug'as jungia pavadinimą ir kodą:
`Aragon` + `03` → `aragon-03.webp`.

Nuotraukų teisės: swatch'ai priklauso tiekėjams. Prieš keliant turėti raštišką
leidimą arba fotografuoti savo salonų pavyzdžius.

## Kainos

Blokas **nerodo** skaičių — tik grupių pavadinimus. Norint rodyti priemokas,
reikia suskaičiuoti mažmenines EUR sumas (vault'e esančios gr1–gr4 sumos yra
hurt PLN savikaina, jų publikuoti negalima).
