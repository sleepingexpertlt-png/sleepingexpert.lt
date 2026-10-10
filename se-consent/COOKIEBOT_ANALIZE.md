# Cookiebot → SE Consent: funkcijų analizė

Tikslas: atsisakyti mokamo Cookiebot (Usercentrics) ir turėti savo sprendimą, kuris
daro viską, ko mums reikia, greičiau ir be mėnesinio mokesčio.

## 1. Ką iš tikrųjų daro Cookiebot (distiliuotai)

| # | Cookiebot funkcija | Kam reikalinga | SE Consent |
|---|---|---|---|
| 1 | Sutikimo baneris (1 ir 2 sluoksnis, kategorijos: būtinieji / nuostatų / statistikos / rinkodaros) | BDAR + ERĮ: sutikimas prieš neprivalomus slapukus | ✅ tos pačios 4 kategorijos, tie patys raktai |
| 2 | Automatinis blokavimas (*auto-blocking*): sekikliai nepaleidžiami iki sutikimo | Kad Meta, TikTok ir kt. neveiktų be sutikimo | ✅ serveryje (HTML filtras) + naršyklėje (dinaminiai scenarijai) |
| 3 | Google Consent Mode v2 (`ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`…) | Privaloma Google Ads/GA4 EEE erdvėje nuo 2024-03 | ✅ default + update, advanced ir basic režimai |
| 4 | Sutikimų žurnalas (*consent log*) | BDAR 7 str. 1 d. — įrodyti, kad sutikimas gautas | ✅ mūsų DB, maskuotas IP, CSV eksportas |
| 5 | Mėnesinis svetainės skenavimas, slapukų sąrašas | Žinoti, kokie slapukai yra; deklaracija | ✅ `tools/scan.mjs` — ir dar tikrina pažeidimus |
| 6 | Slapukų deklaracija (`[cookie_declaration]`) | Privatumo politikos dalis | ✅ `[se_cookie_declaration]`, `[cookie_declaration]` veikia toliau |
| 7 | Sutikimo atnaujinimas / atšaukimas (plaukiojantis mygtukas, `Cookiebot.renew()`) | Atšaukti turi būti taip pat lengva kaip duoti | ✅ mygtukas, nuoroda, trumpasis kodas, `Cookiebot.renew()` |
| 8 | Sutikimo galiojimas (12 mėn.) ir pakartotinis klausimas pasikeitus | Periodinis sutikimo atnaujinimas | ✅ galiojimas + „banerio versija" |
| 9 | Iframe (YouTube, Maps) blokavimas su užrašu | Įterptas turinys deda slapukus | ✅ placeholderis su mygtuku „Leisti ir rodyti" |
| 10 | JS API ir įvykiai (`Cookiebot.consent.*`, `CookiebotOnAccept`) | Kiti įskiepiai/GTM tikrina sutikimą | ✅ suderinamas `window.Cookiebot` shim |
| 11 | GTM integracija (`cookie_consent_*` dataLayer įvykiai) | Esami GTM trigeriai | ✅ tie patys įvykių pavadinimai |
| 12 | WP Consent API (WooCommerce, Site Kit) | WP įskiepiai žino sutikimo būseną | ✅ |
| 13 | Daugiakalbystė (47 kalbos, automatinis vertimas) | Lankytojai kitomis kalbomis | ⚠️ LT + EN; kitas kalbas galima pridėti |
| 14 | Geo-taikymas (baneris tik EEE ir pan.) | Tarptautinėms svetainėms | ➖ nereikia: visi mūsų klientai EEE |
| 15 | IAB TCF 2.2 | Leidėjams, **parduodantiems** reklamos vietas (AdSense, Ad Manager) | ➖ mums nereikia: mes reklamuojamės, o ne parduodame reklamą |
| 16 | Daugelio domenų valdymas vienoje paskyroje | Agentūroms | ➖ nereikia; subdomenams — „Slapuko domenas" |

**Išvada:** iš 16 Cookiebot funkcijų 12 turime pilnai, 1 dalinai (kalbos), 3 mums
nereikalingos. Teisiškai būtinos (1–9) — visos padengtos.

## 2. Kur SE Consent geresnis

1. **Greitis.** Cookiebot kraunamas iš `consent.cookiebot.com` (papildomas DNS + TLS + JS
   failas, kuris blokuoja kitų scenarijų paleidimą). SE Consent — ~20 KB (~6 KB gzip)
   tiesiai HTML'e, **0 papildomų užklausų**. Baneris `position: fixed` — nėra CLS.
2. **Jokio duomenų perdavimo trečiajai šaliai.** Cookiebot žurnalas ir lankytojų IP
   keliauja į Usercentrics serverius. Pas mus viskas lieka mūsų DB.
3. **Pažeidimų paieška.** Cookiebot skeneris tik surašo slapukus. `tools/scan.mjs`
   dar ir patikrina, ar kas nors **veikia be sutikimo** (slapukai, localStorage,
   užklausos trečiosioms šalims) — tai tikrasis BDAR rizikos taškas.
4. **Atšaukimas tikrai išvalo.** Atšaukus kategoriją, jos slapukai ištrinami ir
   puslapis perkraunamas — jau paleistas sekiklis nebegali tęsti darbo.
5. **Grįžtantis lankytojas** — sutikimas pritaikomas sinchroniškai iškart po
   `consent default`, todėl pirmas GA4 `page_view` jau keliauja su teisinga būsena.
6. **Vienodi mygtukai.** „Tik būtinieji" ir „Sutinku su visais" — vienodo dydžio ir
   spalvos, fokusas nenukreipiamas į sutikimą (EDPB 03/2022 „dark patterns" gairės).
7. **Statistika** — sutikimo procentai (visi / tik būtinieji / pasirinkti) skydelyje.
8. **Kaina — 0 €**, nepriklauso nuo puslapių skaičiaus.

## 3. Ką reikia žinoti (rizikos)

- **Google sertifikuotas CMP.** Google reikalauja sertifikuoto CMP tik *leidėjams*
  (AdSense / Ad Manager / AdMob). Google Ads ir GA4 *reklamuotojams* pakanka teisingai
  veikiančio Consent Mode v2 — tai SE Consent daro. Jei kada nors pardavinėtume reklamos
  vietas savo svetainėje — tada reikėtų TCF sertifikuoto CMP.
- **Skenavimą reikia paleisti patiems** — rekomenduoju kas savaitę per cron VPS'e
  (žr. README). Cookiebot tai darė automatiškai.
- **Naujas sekiklis** — jei pridedamas įrankis, kurio nėra žinomų paslaugų sąraše,
  skeneris jį parodys kaip pažeidimą; tada pridėti taisyklę nustatymuose.
- **Puslapių podėlis** — HTML vienodas visiems lankytojams, sprendimai priimami
  naršyklėje, todėl WP Rocket / LiteSpeed Cache veikia be išimčių.

## 4. Teisinis pagrindas (santrauka)

- ES ePrivacy direktyvos 5 str. 3 d. ir LR elektroninių ryšių įstatymo 61 str. —
  neprivalomiems slapukams reikia išankstinio sutikimo.
- BDAR 4 str. 11 p., 7 str. — sutikimas laisvas, konkretus, informuotas, aiškus; turi būti
  įrodomas; atšaukti taip pat lengva kaip duoti.
- EDPB gairės 05/2020 (sutikimas) ir 03/2022 (apgaulingi dizaino modeliai).
- Priežiūros institucija Lietuvoje — VDAI.

Prieš paleidžiant rekomenduoju, kad privatumo politikos tekstą peržiūrėtų teisininkas;
techninė dalis atitinka aukščiau nurodytus reikalavimus.
