# VPS Prompt — GSC 5–15 → question_bank / TAISYTI (v2, suvienodinta)

v1 (atskira seo_opportunities lentelė + naujas cron) ATŠAUKTA — pagal owner
kanoninį kontekstą iš kokybes-auditas sesijos naudojama esama sistema.

```
Jungi GSC 5–15 pozicijų sluoksnį į ESAMĄ sistemą (question_bank_master.json +
kokybes-auditas recommend.py). Jokių naujų lentelių, failų, cron'ų ar config
pakeitimų be owner GO. Jokių publikavimų — tik draft'ai, ir tik po owner GO.

PRIEŠ PRADEDANT: patikrink, ar ankstesnis hermes_master_run bandymas (2026-08-25
vakaras, goal apie seo_opportunities) nepaliko dalinių artefaktų (lentelė
seo_opportunities ar data/seo_opportunities_*.json). Jei paliko — peržiūrėk ir
įtrauk į šį darbą, dublikatų nekurk.

ŽINGSNIS 1 — Ištraukimas (read-only, be kaštų):
GSC API (esama autentifikacija iš traits_business_fetcher.py): 90 d. užklausos,
avg position 4.5–15, impressions >= 50, be brand (sleeping expert / 
sleepingexpert variantai). Kiekvienai: keyword, geriausias landing page,
position, impressions, clicks.

ŽINGSNIS 2 — Merge į question_bank_master.json (NE naujas failas):
Kiekvieną užklausą dedup'ink pagal text prieš esamus 5889 įrašus.
Naujiems: {text, source:["gsc_5_15"], gsc_impressions, gsc_position,
landing_page, ar_jau_matuojamas:false}. Esamiems (pvz., iš GSC 167 šaltinio) —
papildyk source ir gsc_position/landing_page laukus. Prieš rašymą — backup
kopija; po rašymo parodyk diff santrauką (kiek naujų, kiek papildytų).

ŽINGSNIS 3 — Klasifikacija per recommend.py:
Paleisk kokybes-auditas tools/recommend.py ant atnaujinto bank'o (read-only).
Lauktina: dauguma 5–15 → TAISYTI (turinys yra, trūksta citabilumo:
Trumpai: blokas, palyginimo lentelė, DUK+FAQPage schema); be landing → RAŠYTI.

ŽINGSNIS 4 — Pasiūlymas owner'iui (NE vykdymas):
Pagal VYKDYMAS.md procesą suformuok top-10 TAISYTI sąrašą su: keyword,
puslapis, pozicija, impressions, konkretus citabilumo darbas, kaina (LLM
kaštai draft'ui). Įtrauk jau GO gavusį taikinį „koks geriausias čiužinys
lietuvoje" (#4, AIO cituoja konkurentus) kaip #1 — jam draft'ą daryk iškart.

ŽINGSNIS 5 — Verifikacija:
(a) question_bank_master.json count prieš/po + backup egzistuoja,
(b) recommend.py output klasės pasiskirstymas, (c) taikinio #1 draft
(TIK draft statusu WP), (d) top-10 pasiūlymo lentelė owner'iui.

GELEŽINĖS: jokio auto-publish; business faktai tik iš owner; draudžiami
premium/exclusive/Italijos dizaineriai/geriausi pasaulyje; matavimų
nepaleidinėti (savaitinis ciklas jau yra, kaštų taisyklė ≤1 €/parą).
```
