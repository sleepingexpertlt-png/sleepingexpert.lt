# Sapnų reikšmės — blogo kategorija su paieška (projektas)

**Tikslas (G3 blogas / G4 AI matomumas):** nauja `sleepingexpert.lt` blogo kategorija „Sapnų reikšmės“:
vienas hub straipsnis su paieška ir A–Ž žodynu + 305 atskiri įrašai (po vieną simboliui) + 12 mindfulness
praktikų straipsnių, sujungtų vidinėmis nuorodomis (hub ↔ įrašas ↔ susiję simboliai ↔ praktika). Turinys – originalus lietuviškas tekstas,
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
| `data/sapnu-reiksmes/symbols/*.json` | Turinys: 9 kategorijos, 305 simboliai (failai `_2` – antra partija, `papildymai.json` – dažniausiai ieškomi papildymai su `category` lauku). Vienas šaltinis tiesai. |
| `data/sapnu-reiksmes/practices.json` | 12 mindfulness praktikų (žingsniai, kada naudoti, mokslas, susiję simboliai). |
| `scripts/sapnai/build.py` | Generatorius → `build/sapnu-reiksmes/` (WP fragmentai + manifest + peržiūra). |
| `scripts/sapnai/publish_wp.py` | Publikavimas į WP per REST API (dry-run pagal nutylėjimą, draft statusas). |
| `scripts/sapnai/fetch_products.py` | Realūs produktai reklamos kortelėms → `data/sapnu-reiksmes/products.json`. |
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
python3 scripts/sapnai/fetch_products.py              # realūs produktai kortelėms (nebūtina)
python3 scripts/sapnai/build.py
python3 scripts/sapnai/publish_wp.py                  # dry-run: parodo, kas bus sukurta / kas jau yra
python3 scripts/sapnai/publish_wp.py --apply --limit 50   # 1 partija: 50 draft'ų + hub
# peržiūra WP admin → Posts → Drafts → Publish; po 1–2 sav. indeksavimo – kita partija
python3 scripts/sapnai/publish_wp.py --apply          # visi likę
```

Skriptas idempotentiškas: įrašus randa pagal slug, todėl pakartotinis paleidimas tik atnaujina turinį.
Nuorodos tarp įrašų sugeneruojamos kaip `{{URL:slug}}` ir pakeičiamos tikrais permalink'ais tik
sukūrus įrašus – todėl WP permalink struktūros žinoti iš anksto nereikia.

## Mindfulness praktikos

12 atskirų straipsnių (`/praktika-<slug>/`): sapnų dienoraštis, vaizduotės repeticija košmarams (IRT),
įžeminimas 5-4-3-2-1, kūno skenavimas, 4-7-8 kvėpavimas, sąmoningas pabudimas, RAIN, mintys kaip debesys,
vakaro ritualas, dėkingumo praktika, tikrovės testai, rytiniai puslapiai. Kiekvienas simbolis mindfulness
bloke rodo nuorodą į tinkamą praktiką: pirma pagal praktikos `related` sąrašą, tada pagal kategoriją
(`PRACTICE_BY_CATEGORY`). Praktikų puslapiai turi HowTo + Article schema.

## Kokybės vartai (seo-programmatic skill)

- Kiekvienas įrašas ≈ 440–630 žodžių, iš jų 50–57 % unikalaus (ne šabloninio) teksto – virš 40 % slenksčio.
- Hub ≈ 20 000 žodžių: visų 305 simbolių trumpos reikšmės + „Plačiau“ (pirma psichologinė pastraipa) + paieška + praktikų sekcija. Pilnos pastraipos – tik simbolių puslapiuose, kad hub liktų lengvas mobiliesiems.
- Kiekvienas įrašas: Article + FAQPage (3 kl.) + BreadcrumbList schema, 3–6 susiję simboliai, nuoroda į hub.
- Progressive rollout: pirma partija 50 įrašų + hub + praktikos, stebėti indeksavimą 1–2 sav., tada po 100.
- Statusas visada `draft`; publish tik rankiniu būdu arba `--publish` po peržiūros.
- Šaltinių DOI (5 vnt.) šioje sesijoje per tinklą patikrinti nepavyko (doi.org užblokuotas proxy) –
  prieš `--publish` paleisti `curl -I https://doi.org/<doi>` iš VPS.
- `WP_URL` secrets.env faile yra svetainės šaknis (`https://www.sleepingexpert.lt`) – skriptas pats prideda `/wp-json/wp/v2`.

## Reklama (produktų blokai)

Kiekvienas įrašas turi du blokus: „Miego eksperto pastaba“ po variantų lentele (kontekstinis tekstas +
CTA į produktų kategoriją) ir produktų korteles prieš kontaktus. Tipas parenkamas pagal simbolį
(`AD_BY_SLUG`) arba kategoriją (`AD_BY_CATEGORY`) `build.py` faile:

| Tipas | Kada | Produktai |
|---|---|---|
| pozicija | košmarai, miego paralyžius, baimė, skendimas, dantys | pagalvės (šoninė padėtis) |
| temperatura | sniegas, ugnis, saulė, audra, vanduo, jūra | antklodės pagal sezoną |
| kunas | kojos, rankos, žaizda, liga, kritimas, laiptai | čiužiniai (CE Medical Device) |
| tamsa | tamsa, šviesa, mėnulis, žvaigždės, langas, telefonas | miego aksesuarai (kaukės) |
| lova | lova, namas, darbas, vėlavimas, laikrodis | čiužiniai (amžius 8–10 m.) |
| bendras | visi kiti | čiužiniai + konsultacija |

Kortelės su realiais produktais imamos iš `data/sapnu-reiksmes/products.json`; jį generuoja
`scripts/sapnai/fetch_products.py` iš VPS (viešas WC Store API, be auth). Be failo rodomos
kategorijų plytelės. Kainos nerodomos sąmoningai – jos keičiasi, o straipsniai ne.

## Kategorijos archyvas = hub (nukreipimas)

`/kategorija/sapnu-reiksmes/` yra WordPress archyvas: kol įrašai juodraščiai – tuščias, po publikavimo –
įrašų sąrašas be paieškos. Kad šis adresas atidarytų patį žodyną su paieška, reikia 301 nukreipimo
į hub (`/sapnu-reiksmes/`). Du būdai, abu owner per WP admin (1 min.):

1. **Rank Math → Redirections → Add New:** Source `kategorija/sapnu-reiksmes/` (Exact), Destination
   `https://sleepingexpert.lt/sapnu-reiksmes/`, tipas 301.
2. **WPCode snippet (PHP):**
   ```php
   add_action('template_redirect', function () {
       if (is_category('sapnu-reiksmes') && !is_paged()) {
           wp_redirect(home_url('/sapnu-reiksmes/'), 301);
           exit;
       }
   });
   ```

Be nukreipimo `publish_wp.py` vis tiek palieka du saugiklius: kategorijos aprašymas su nuoroda į hub ir
hub kaip naujausias įrašas (publikuojant datos išdėstomos taip, kad hub būtų pirmas sąraše).

## Vieta svetainėje

Apie 4 MB `wp_posts` turinio (hub 340 KB, įrašas vid. 13 KB), 0 naujų failų `uploads`. Simbolių ir praktikų
įrašai turi tik bazinį CSS, hub – visą (paieška, raidės, filtrai). `publish_wp.py` po kiekvieno atnaujinimo
ištrina senas revizijas (`--keep-revisions`, numatyta 1), kad DB neaugtų dvigubai su kiekvienu `--apply`.

## WP slug'ų schema

- Hub: `/sapnu-reiksmes/`; kategorijos archyvas: `/kategorija/sapnu-reiksmes/` (aprašymas su nuoroda į hub
  įrašomas `publish_wp.py` metu, kad archyvo puslapis turėtų ką paspausti)
- Simboliai: `/sapnuoti-<slug>/` (pvz. `/sapnuoti-gyvate/`), būsenoms – aiškesni: `/kosmarai-ka-reiskia/`,
  `/pasikartojantys-sapnai/`, `/samoningi-sapnai/`, `/miego-paralyzius/`, `/baime-sapne/`, `/klaidingas-pabudimas/`.

## Kas toliau (owner sprendimai)

1. Paleisti `publish_wp.py --apply --limit 50` iš VPS ir peržiūrėti 3–5 draft'us WP admin.
2. Pridėti kategoriją „Sapnų reikšmės“ į blogo meniu / sidebar, kad hub gautų vidinį svorį.
3. Po pirmos partijos: GSC užklausos su „sapn“ → pildyti trūkstamus simbolius (tas pats JSON formatas).
4. Ahrefs Keywords Explorer šiam planui neprieinamas („Insufficient plan“) – paklausos skaičius rinkti iš GSC po publikavimo.
