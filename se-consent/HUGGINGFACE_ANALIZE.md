# Hugging Face analizė: ką distiliavome į SE Consent

**Metodas:** Hugging Face Hub paieška (modeliai, duomenų rinkiniai, Spaces, straipsniai)
pagal raktažodžius *cookie, cookie consent, tracker, privacy policy, dark patterns,
consent banner*. Atranka vyko trimis žingsniais: (1) ar produktas susijęs su sutikimais
arba sekikliais, (2) kokia licencija, (3) ar jį realiai įmanoma pritaikyti mūsų įskiepyje.

**Bendra išvada:** HF yra ML platforma, todėl paruoštų CMP įskiepių ten nėra. Dauguma
„cookie" rezultatų yra nesusiję LLM modeliai ar robotikos duomenys. Vertingi radiniai trys,
ir iš jų distiliavome **metodiką ir duomenis**, o ne pačius modelius.

## 1. Patikrinti produktai

| Produktas | Kas tai | Licencija | Vertinimas |
|---|---|---|---|
| [olafuraron/tracker-classifier](https://hf.co/olafuraron/tracker-classifier) | Neuroninis tinklas, kuris klasifikuoja domeną kaip sekiklį arba ne. 181 KB, F1 0,85 (RF/XGBoost 0,90) | MIT | ⭐ **Distiliuota metodika** |
| [olafuraron/tracker-radar-ml](https://hf.co/datasets/olafuraron/tracker-radar-ml) | 16 165 domenai su 295 elgsenos požymiais (DuckDuckGo Tracker Radar) | CC-BY-**NC**-SA | ❌ Duomenų nenaudojame: nekomercinė licencija |
| [getreadystack/pre-consent-cookie-audit-2026](https://hf.co/spaces/getreadystack/pre-consent-cookie-audit-2026) | CNIL/AEPD/Garante pažeidimų skaičiuoklė. Duomenys vedami ranka, pilna versija kainuoja $60 | MIT | ⭐ **Distiliuoti tikrinimo kriterijai** |
| [sonhask/cookie-policy-extracttion-corpus](https://hf.co/datasets/sonhask/cookie-policy-extracttion-corpus) | LLM ištraukos iš slapukų politikų (IT→VI→EN), tik „error" kontroliniai taškai | nenurodyta | ❌ Netvarkingi duomenys, be licencijos |
| Wravn/privacy-policy-content-* (14 modelių) | RoBERTa klasifikatoriai privatumo politikos skyriams | nenurodyta | ➖ Mums neaktualu: politiką rašome patys |
| asquirous/bert-base-uncased-dark_patterns | BERT modelis, aptinkantis manipuliacinius e. parduotuvių tekstus | Apache-2.0 | ➖ Banerio tekstas mūsų, todėl kontroliuojame patys |
| Open Cookie Database (GitHub, rastas per analizę) | 2 262 slapukų įrašai su tiekėju, kategorija ir trukme | Apache-2.0 | ⭐ **Integruota į skenerį** |

## 2. Ką distiliavome ir kaip padarėme geriau

### a) tracker-classifier → elgsenos įvertinimas skeneryje
Modelio požymių svarba (`results.json`) rodo, kas labiausiai išduoda sekiklį: slapukų
nustatymas ir jų paplitimas, API kvietimų įvairovė, fingerprinting svoriai, subdomenai.
Pačio modelio paleisti negalime: jam reikia 295 požymių iš viso interneto skenavimo
(pvz. „kiek svetainių naudoja šį domeną"), o tie duomenys nekomerciniai.

**Ką padarėme:** skeneris (`tools/scan.mjs`) dabar **kiekvienam nežinomam trečiosios
šalies domenui** fiksuoja:
- canvas / WebGL / audio / šriftų / navigator / screen / WebRTC / UA-CH API kvietimus
  (pagal steką žinoma, kuris scenarijus kvietė);
- ar domenas nustato slapukus ir kiek jie galioja;
- sekimo pikselius ir „ping" užklausas su identifikatoriais;
- ar domenas yra Open Cookie Database.

Pagal tai skaičiuojamas **balas**. Jei balas ≥ 3, skeneris pasiūlo paruoštą blokavimo
taisyklę (`domenas | marketing`). **Geriau už originalą:** modelis atsako tik „taip/ne",
o mūsų įvertinimas paaiškina **kodėl** ir pasako, **ką daryti**. Jis veikia mūsų
svetainės realioje aplinkoje ir naudoja tik leidžiamus duomenis.

### b) pre-consent-cookie-audit → 6 automatiniai patikrinimai
Ten 4 CNIL dažniausiai baudžiami pažeidimai skaičiuojami iš ranka suvestų skaičių.
Pas mus tie patys kriterijai **tikrinami automatiškai** realioje svetainėje:

| # | Patikrinimas | Kaip tikrinama |
|---|---|---|
| 1 | Nieko neveikia iki sutikimo | slapukai, localStorage ir užklausos prieš bet kokį paspaudimą |
| 2 | „Atmesti" pirmame sluoksnyje, vienodo svorio | randami mygtukai, palyginamas jų plotas (> 80 %) |
| 3 | Nurodytos paskirtys | kategorijų aprašymai ir slapukų sąrašas |
| 4 | Atšaukimas veikia | `withdraw()` → perkrovimas → ar liko slapukų ir užklausų |
| 5 | Slapukai ≤ 13 mėn. | visų slapukų (ir HttpOnly) galiojimas |
| 6 | Sutikimas klausiamas iš naujo ≤ 13 mėn. | įskiepio nustatymas |

Rezultatas pateikiamas kaip įvertinimas, pvz. `Atitiktis: 6/6`. Skeneris tinka cron'ui ir
nesiunčia jokių duomenų trečiosioms šalims. Įdomu, kad pats šis HF įrankis krauna
`grow.me` sekiklį dar prieš sutikimą.

### c) Open Cookie Database → automatinis nedeklaruotų slapukų aprašymas
Nedeklaruotiems slapukams skeneris iš karto pateikia **eilutę, paruoštą įklijuoti**
į nustatymus: tiekėją, kategoriją, paskirtį ir trukmę. DB atnaujinama kas savaitę ir
saugoma vietiniame podėlyje.

**Geriau už originalą:** OCD daug trečiųjų šalių įrankių žymi kaip „Functional"
(pvz. Hotjar ID), o tai reikštų „nereikia sutikimo". Mūsų testai tai sugavo. Dabar
trečiųjų šalių tiekėjai **niekada** nelaikomi būtinaisiais: analitikos tiekėjai
priskiriami statistikai, reklamos – rinkodarai, kiti – nuostatų kategorijai.

### d) Iš skenerio radinio → pataisa įskiepyje
Skeneris parodė, kad Google `_ga` slapukas pagal nutylėjimą galioja **2 metus**, nors
leidžiama ne daugiau 13 mėn. Įskiepis dabar automatiškai nustato
`gtag('set', {cookie_expires: 395 d.})`. Šis pakeitimas galioja visiems GA4 ir Google Ads
`config`, o reikšmę galima keisti nustatymuose.

## 3. Ko sąmoningai nedarėme
- **Neįdėjome ML modelio į naršyklę.** 181 KB modelis ir WASM variklis sulėtintų puslapį,
  o tikslumu nusileistų žinomų paslaugų sąrašui ir skeneriui. Sekiklius atpažįstame
  serveryje ir skenavimo metu, ne lankytojo naršyklėje.
- **Nenaudojame NC licencijos duomenų** (Tracker Radar): Sleeping Expert yra komercinė
  įmonė.

## 4. Testai
- `tests/scan-test.mjs` – vietinė svetainė ir „trečioji šalis" su nutekančiu sekikliu,
  fingerprinting scenarijumi, pikseliu, 2 metų `_ga` slapuku ir nedeklaruotu Hotjar
  slapuku. 11 iš 11 patikrinimų praėjo.
- `tests/browser-test.mjs` – 32 iš 32 (įskaitant naują Google slapukų galiojimo patikrinimą).
- `tests/blocker-test.php` – 16 iš 16.
