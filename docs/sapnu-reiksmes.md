# Sapnų reikšmės — blogo kategorija su paieška (projektas)

**Tikslas (G3 blogas / G4 AI matomumas):** nauja `sleepingexpert.lt` blogo kategorija „Sapnų reikšmės“:
vienas hub straipsnis su paieška ir A–Ž žodynu + 120 atskirų įrašų (po vieną simboliui), sujungtų
vidinėmis nuorodomis (hub ↔ įrašas ↔ susiję simboliai). Turinys – originalus lietuviškas tekstas,
paremtas viešai prieinama sapnų psichologija (Freudas, Jungas, tęstinumo hipotezė, grėsmės simuliacijos
teorija, REM emocijų apdorojimas) ir mindfulness praktikomis. Jokių prietarų kaip faktų, jokių
medicininių teiginių, jokių konkurentų pavadinimų.

## Kodėl ne „nukopijuoti nemokamą sapnininką“

Laisvai pasiekiama ≠ laisvai naudojama. Lietuviški sapnininkų puslapiai yra autorių teisių saugomi,
o vieši (public domain) šaltiniai (Freudo *Die Traumdeutung* 1900, G. H. Millerio *10,000 Dreams
Interpreted* 1901) yra angliški/vokiški ir vertimas vis tiek reikalauja perrašymo. Todėl visas tekstas
parašytas iš naujo, o šaltiniai cituojami straipsnių pabaigoje. Tai ir SEO požiūriu vienintelis
saugus kelias (Google „scaled content abuse“ politika, 2024–2025).

## Failai

| Kelias | Kas tai |
|---|---|
| `data/sapnu-reiksmes/symbols/*.json` | Turinys: 8 kategorijos, 120 simbolių. Vienas šaltinis tiesai. |
| `scripts/sapnai/build.py` | Generatorius → `build/sapnu-reiksmes/` (WP fragmentai + manifest + peržiūra). |
| `scripts/sapnai/publish_wp.py` | Publikavimas į WP per REST API (dry-run pagal nutylėjimą, draft statusas). |
| `build/` | Sugeneruota (git ignore). Paleisk `build.py`, kad atsirastų. |

### Simbolio įrašo laukai (`symbols/*.json`)

```
slug         vidinis raktas (be diakritikų), naudojamas nuorodoms `related`
word         žodis vardininku („Gyvatė“)
title        „Sapnuoti gyvatę“ – iš jo formuojamas WP pavadinimas ir focus keyword
aliases      sinonimai paieškai ir RankMath secondary keywords
short        1–2 sakinių reikšmė (snippet, excerpt, DUK atsakymas Nr. 1)
psychology   2–3 pastraipos: psichologinis aiškinimas
variants     3 situacijos → reikšmės (lentelė)
mindfulness  1 rytinė praktika / klausimas sau
sleep_note   (nebūtina) miego higienos pastaba; čia leistina švelni produkto kategorijos nuoroda
related      3–6 kitų simbolių slug'ai (tikrinama build metu)
```

## Kaip paleisti

```bash
python3 scripts/sapnai/build.py                # sugeneruoja build/sapnu-reiksmes/
open build/sapnu-reiksmes/preview/index.html   # peržiūra su veikiančia paieška ir vidiniais puslapiais
```

Publikavimas vyksta **iš VPS**, nes tik ten yra `WP_USER` / `WP_APP_PASSWORD` (Hostinger blokuoja
curl iš kitur, o Claude Code web sesija sleepingexpert.lt nepasiekia):

```bash
cd /root/sleepingexpert.lt && git pull
set -a && source /root/frontier-agent/config/secrets.env && set +a
python3 scripts/sapnai/build.py
python3 scripts/sapnai/publish_wp.py                  # dry-run: parodo, kas bus sukurta / kas jau yra
python3 scripts/sapnai/publish_wp.py --apply --limit 50   # 1 partija: 50 draft'ų + hub
# peržiūra WP admin → Posts → Drafts → Publish; po 1–2 sav. indeksavimo – kita partija
python3 scripts/sapnai/publish_wp.py --apply          # visi likę
```

Skriptas idempotentiškas: įrašus randa pagal slug, todėl pakartotinis paleidimas tik atnaujina turinį.
Nuorodos tarp įrašų sugeneruojamos kaip `{{URL:slug}}` ir pakeičiamos tikrais permalink'ais tik
sukūrus įrašus – todėl WP permalink struktūros žinoti iš anksto nereikia.

## Kokybės vartai (seo-programmatic skill)

- Kiekvienas įrašas ≈ 440–630 žodžių, iš jų 50–57 % unikalaus (ne šabloninio) teksto – virš 40 % slenksčio.
- Hub ≈ 17 000 žodžių: visų 120 simbolių trumpos reikšmės + „Plačiau“ (psichologinės pastraipos) + paieška.
- Kiekvienas įrašas: Article + FAQPage (3 kl.) + BreadcrumbList schema, 3–6 susiję simboliai, nuoroda į hub.
- Progressive rollout: pirma partija 50 įrašų, stebėti indeksavimą 1–2 sav., tada likusius.
- Statusas visada `draft`; publish tik rankiniu būdu arba `--publish` po peržiūros.
- Šaltinių DOI (5 vnt.) šioje sesijoje per tinklą patikrinti nepavyko (doi.org užblokuotas proxy) –
  prieš `--publish` paleisti `curl -I https://doi.org/<doi>` iš VPS.
- `WP_URL` secrets.env faile yra svetainės šaknis (`https://www.sleepingexpert.lt`) – skriptas pats prideda `/wp-json/wp/v2`.

## WP slug'ų schema

- Hub: `/sapnu-reiksmes/` (kategorija: `sapnu-reiksmes`)
- Simboliai: `/sapnuoti-<slug>/` (pvz. `/sapnuoti-gyvate/`), būsenoms – aiškesni: `/kosmarai-ka-reiskia/`,
  `/pasikartojantys-sapnai/`, `/samoningi-sapnai/`, `/miego-paralyzius/`, `/baime-sapne/`, `/klaidingas-pabudimas/`.

## Kas toliau (owner sprendimai)

1. Paleisti `publish_wp.py --apply --limit 50` iš VPS ir peržiūrėti 3–5 draft'us WP admin.
2. Pridėti kategoriją „Sapnų reikšmės“ į blogo meniu / sidebar, kad hub gautų vidinį svorį.
3. Po pirmos partijos: GSC užklausos su „sapn“ → pildyti trūkstamus simbolius (tas pats JSON formatas).
4. Ahrefs Keywords Explorer šiam planui neprieinamas („Insufficient plan“) – paklausos skaičius rinkti iš GSC po publikavimo.
