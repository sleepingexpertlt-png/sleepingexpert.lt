# GitHub atvirojo kodo analogų analizė → SE Consent

**Metodas:** 4 populiariausi atvirojo kodo sutikimų valdikliai buvo klonuoti ir jų kodas
išnagrinėtas (tik skaitant, nieko nepaleidžiant). Kiekvienas palygintas su SE Consent
funkcijų sąrašu. Tada atrinkti dalykai, kuriuos siūlo keli analogai, ir įdiegti su testais.

| Analogas | Versija | Licencija | Dydis | Stiprybė |
|---|---|---|---|---|
| [orestbida/cookieconsent](https://github.com/orestbida/cookieconsent) | 3.1.0 | MIT | 23 KB JS + 32 KB CSS | Prieinamumas, paslaugų jungikliai, API |
| [klaro-org/klaro](https://github.com/klaro-org/klaro) | 0.7.22 | BSD-3 | 68–236 KB | Sutikimas atskirai kiekvienai paslaugai, slapukų trynimas pagal domeną |
| [AmauriC/tarteaucitron.js](https://github.com/AmauriC/tarteaucitron.js) | 1.36.0 | MIT | — | 249 paruoštos paslaugos su slapukų sąrašais, DNT, UET |
| [Really-Simple-Plugins/complianz-gdpr](https://github.com/Really-Simple-Plugins/complianz-gdpr) | 7.5.5 | GPLv2 | WP įskiepis | 105 įskiepių integracijos, GPC, sutikimų įrodymų kopijos |

## Ką siūlė keli analogai → įdiegta

| # | Funkcija | Kas turėjo | SE Consent dabar | Testas |
|---|---|---|---|---|
| 1 | **Sutikimas atskirai kiekvienai paslaugai** (pvz. Meta „ne", GA4 „taip") | visi 3 JS analogai | 17 paslaugų su atskirais jungikliais kategorijose; Consent Mode atsižvelgia į Google Ads / GA4 paslaugą | ✅ 9 patikrinimai |
| 2 | **Paslaugos slapukų trynimas** atšaukus (visuose domeno variantuose) | Klaro, tarteaucitron, CookieConsent | kiekviena paslauga turi savo slapukų sąrašą; atšaukus Meta trinamas tik `_fbp`/`_fbc` | ✅ |
| 3 | **Placeholderis leidžia tik tą turinį** („accept once") | Klaro | YouTube mygtukas leidžia tik YouTube, ne visą rinkodarą | ✅ |
| 4 | **Global Privacy Control** | Complianz (ir DNT – tarteaucitron) | naršyklės „ne" = atsisakymas, žurnale `gpc` | ✅ 3 patikrinimai |
| 5 | **Prieinamumas** (EAA nuo 2025-06) | CookieConsent, Complianz | fokuso spąstai, `aria-modal`, Esc, fokusas grąžinamas | ✅ 3 patikrinimai |
| 6 | **Microsoft UET consent mode** | tarteaucitron | `uetq consent default/update` | ✅ |
| 7 | **Microsoft Clarity consentv2** | Complianz | signalas siunčiamas net prieš Clarity įkėlimą | ✅ |
| 8 | **Žurnale – paslaugų pasirinkimai** | Klaro (įvykio diff) | stulpelis `services_off`, CSV eksportas | ✅ |

## Ko sąmoningai neperėmėme
- **Complianz kodo** (GPLv2): naudojome tik kaip faktų šaltinį (kurie URL ir slapukai priklauso kuriai paslaugai), kodas parašytas savas.
- **tarteaucitron lietuviško vertimo**: jis mašininis („Tęsiant slankiojimą"); mūsų tekstai geresni.
- **hideFromBots** (CookieConsent): slėptų banerį nuo Lighthouse ir mūsų pačių skenerio — skeneris tada negalėtų patikrinti atitikties.
- **Opt-out režimo**: ES reikalauja opt-in.
- **Banerio A/B testų**: Complianz tai mokama funkcija; EDPB laiko manipuliavimą sutikimo dažniu rizikingu.

## Kur SE Consent lenkia visus 4
- Vienintelis turi **serverio filtrą + kliento blokavimą + atitikties skenerį** viename.
- Vienintelis turi **Cookiebot API suderinamumą** (migracija be GTM pakeitimų).
- Vienintelis **automatiškai riboja Google slapukų galiojimą iki 13 mėn.**
- Mažesnis už Klaro (25 KB prieš 68–236 KB), jokių priklausomybių.

## Testai (paleista 5 kartus iš eilės, 0 klaidų)
| Rinkinys | Patikrinimai |
|---|---|
| Blokatorius (PHP) | 18 |
| Naršyklė (WordPress versija) | 52 |
| Versija be WordPress | 9 |
| Skeneris | 11 |
| **Iš viso** | **90 × 5 = 450** |
