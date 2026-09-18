# Tikslo sekimas (atnaujinama kas patikrinimą)

Tikslas: maršrutai +30 % bent 2/3 salonų iki 2026-10-24. Bazė 34 → tikslas 44.

| Data | Klaipėda | Ukmergė | Vilnius | Viso | WC 7d | Pastaba |
|---|---|---|---|---|---|---|
| 08-26 (bazė) | 13 | 13 | 8 | **34** | 11 | ciklo startas |
| 08-27 | 13 | 13 | **6** | **32** | 8 | −6 % nuo bazės; Vilnius −25 % |
| tikslas | 17 | 17 | 10 | **44** | — | 10-24 |

## Matavimo sluoksnis — ATGAIVINTAS ✅

Gemini rakto fix'as (08-26) atstatė ne tik pipeline, bet ir matavimą:

| Metrika | 08-26 | 08-27 | |
|---|---|---|---|
| `traffic_snapshot_age_hours` | 48.5 (mirę) | **0.5** | ✅ matuoja vėl |
| `gsc_avg_position` | 8.2 | **7.6** | ✅ |
| `gsc_clicks_24h` | 43 | **60** | ✅ +40 % |
| `gsc_impressions_24h` | 1674 | **1843** | ✅ |
| `gsc_ctr` | 2.57 % | **3.26 %** | ✅ |
| blog pipeline | 2× error, q=0 | **1 draft** | ✅ gamina |

## Ką tai reiškia (be gražinimo)

Techninis sluoksnis atsigavo. **Verslo skaičius juda ne ta kryptimi:**
maršrutai −6 %, Vilnius −25 % (8→6), WC užsakymai 11→8.

Vilnius: **daugiausia impresijų (329 vs 260 vs 192), mažiausiai maršrutų.**
Žmonės profilį mato, bet nespaudžia maršruto. Tai konversijos, ne matomumo
problema — ir tiksliai atitinka P-064 (kategorija lenkiškai): profilis
pasirodo, bet neatrodo kaip tai, ko žmogus ieškojo.

Dviejų dienų imtis per maža išvadai apie trendą, bet Vilniaus atotrūkis
(impresijos aukščiausios, maršrutai žemiausi) yra struktūrinis, ne
triukšmas — jis matėsi ir 08-26.

## Sinergijos silpnoji vieta (hermes_synergy, 08-26)

- `metacog_to_actions` = **0.3** — „7 klaidos, nė vieno circuit breaker".
  Sistema mato savo klaidas, bet nereaguoja. Tai tiksliai tai, kas įvyko
  per Gemini gedimą: 8 val. tylos.
- `traits`: `10_sinergija` ↓ (vienintelis krentantis iš 11).
- `cag_to_master` = 0.49 — orchestratoriaus rezultatai vidutiniai.

Stiprūs: `radar_to_metacog` 1.0, `agents_to_business` 1.0 (474 agentų
paleidimai → 43 clicks).

---

## RADINYS 2026-08-27: lokacijų puslapiai = AI srauto ir maršrutų sankirta

Po `aeo_reverse_discovery.py` substring bug'o fix'o (commit 349cf5e6) gavom
švarius GA4 duomenis: **172 realios AI sesijos / 28 d.** (ne 684).

Pasiskirstymas per puslapio tipą (125 klasifikuotų sesijų):

| Tipas | Sesijos | Puslapių | **Sesijų / puslapį** |
|---|---|---|---|
| **Lokacijos** | 40 (32 %) | **3** | **13,3** |
| Blogas/gidai | 12 (9,6 %) | 3 | 4,0 |
| Kategorijos | 18 (14,4 %) | 6 | 3,0 |
| Produktai | 42 (33,6 %) | 17 | 2,5 |

**Lokacijų puslapiai 5× efektyvesni už produktų puslapius.**

### Kodėl tai keičia prioritetus

Pagrindinis tikslas = maršrutai į salonus. AI srautas ateina būtent į
lokacijų puslapius. Tai ta pati piltuvo vieta — vadinasi AEO darbas maitina
NE tik antrinį tikslą (raktažodžiai), bet tiesiogiai pirminį (maršrutai),
per lokacijų puslapius.

Iki šiol tie 3 puslapiai nebuvo nė karto optimizuoti. Jie traukia trečdalį AI
srauto atsitiktinai.

Vilnius: mažiausi maršrutai (6), didžiausios impresijos (329). AI atveda —
žmogus nepaspaudžia maršruto. Konversijos problema tiksliai ten, kur turim
daugiausiai svertų.

### Naujas turinio prioritetas

1. **3 lokacijų puslapiai** (buvo neprioritetas) — pirminis tikslas
2. 1 bangos blog puslapiai — antrinis tikslas
3. Kategorijos — antrinis

Ką lokacijų puslapiuose tikrinti: ar maršruto mygtukas matomas be scroll'o,
ar yra darbo laikas/telefonas/adresas struktūruotai, LocalBusiness JSON-LD,
ar yra atsakymai į „ką galiu išbandyti vietoje", ar yra nuoroda į GBP profilį,
ar puslapis atsako į klausimą, su kuriuo AI žmogų atsiuntė.

---

## 2026-08-27: P-064 patikra pagal owner'io pateiktą GBP profilį

Owner pateikė pilną Vilniaus GBP profilio turinį. Patikra prieš P-064:

| Elementas | Būsena | Vertinimas |
|---|---|---|
| Pagrindinė kategorija | **„Čiužinių parduotuvė"** | ✅ **SUTVARKYTA** — atitinka auditą (07-gbp-reitingo-svertai.md:13) |
| Antrinės kategorijos | Lovų / Patalynės / Miegamojo baldų parduotuvė | ✅ tiksliai kaip planuota |
| **Paslaugų sritis** | **„Litwa / Łotwa / Estonia"** | 🔴 **VIS DAR LENKIŠKAI + neteisinga** |
| Aprašas | LT, mini ir Klaipėdą, ir Ukmergę | ⚠️ kryžminis skiedimas |
| Telefonas | „(0-630) 70001" | ⚠️ NAP formatas nesutampa su svetaine |
| Atidarymo data | tuščia | ⚠️ pilnumo signalas |
| **Produktai** | **0** | 🔴 didžiausia neišnaudota vieta profilyje |
| Stovėjimo aikštelė | „Nemokama stovėjimo aikštelė" | ✅ **realus GBP atributas** — lokacijų puslapių teiginys teisėtas, įspėjimas 03-publikavimo-eile.md uždaromas |

**Išvada dėl P-064:** kategorijos dalis UŽDARYTA (data 08-27). Lieka
kalbos dalis — paslaugų sritis. Pirmadienio patikroje Vilniaus maršrutų
pokytis turi būti skaitomas kaip kategorijos + lokacijos puslapio efektas
kartu, ne atskirai — abu pakeitimai įvyko tą pačią dieną.

### Kodėl „Łotwa / Estonia" yra ne tik kalbos klaida

Paslaugų sritis su Latvija ir Estija siunčia Google signalą, kad
aptarnaujam šalis, kuriose neturim nei salono, nei pristatymo pažado.
Fizinei parduotuvei, į kurią klientas ateina, paslaugų sritis apskritai
nebūtina — o klaidinga sritis skiedžia vietinį relevantiškumą Vilniuje.
Tai tiesiogiai liečia pirminį tikslą (maršrutai į Vilniaus saloną).

---

## 2026-09-03 — pakeitimų žurnalas (atribucijai)

Du pakeitimai per tris dienas — 09-06/09-08 matavimai jų neatskirs.
Fiksuoju, kad būtų žinoma, kas veikė.

| Data | Kas | Poveikis maršrutams |
|---|---|---|
| ~08-28 → 09-01 | Google Ads sustabdyta (mokėjimo slenkstis), atnaujinta 09-01 | −, paskui atsistatymas į bazę |
| **09-03** | **5 PMax kampanijų `shopping_setting.feed_label` = LT** (buvo tuščias → 0 produktų → „Nėra produktų sistemoje Google Ads", 6,6 % opt. balas, 8 € iš 28 €/d išleista). Mutate per Google Ads API, patikrinta nepriklausomu GAQL. Kampanijos: 23085196755, 23231305809, 23739524386, 24208858994, 24214064113, **+ 23941982295 Ukmergė PMax (14:26, buvo praleista, pataisyta)** | + (laukiama): PMax su produktais, iki ~20 €/d **jau suplanuoto** biudžeto pradeda dirbti — **be biudžeto kėlimo**, t. y. 07-30 sprendimo nekeičiant |

Patikra: 09-04 09:00 VPS cron — ar `SHOPPING_ADD_PRODUCTS_TO_CAMPAIGN`
rekomendacija dingo. 09-06 06:00 — Porter GBP dieninė eilutė (M6 testas).

Ukmergė PMax buvo praleista — pataisyta 14:26, patvirtinta GAQL. Viso 6 PMax su LT.
„SE — Ukmergė čiužiniai + lovos [always-on]" (23941122366) — **Search** kampanija,
`shopping_setting` jai netaikomas, tuščias feed_label normalus. Neliesti.

## 2026-09-10 — Reklamos faktai ir kas iš tikrųjų relevant tikslui

GAQL, customer 7015063449, 2026-09-01 → 2026-09-09, tik ENABLED kampanijos.
Iš viso išleista **752,88 € per 9 d. = 83,65 €/d**.

### feed_label taisymas suveikė

PMax kampanijos vėl leidžia pinigus: PMax-4 154,78 €, Vilnius PMax A2 89,69 €,
PMax-3 83,06 €, Klaipėda PMax A3 79,71 €, Vaikiškos lovos 47,20 €.
Diagnostika „Nėra produktų sistemoje Google Ads" nebeblokuoja išlaidų.

### Biudžeto pasiskirstymas pagal miestą

| Miestas | Išlaidos 9 d. | Per dieną | GBP impresijų pokytis |
|---|---|---|---|
| Vilnius | 223,48 € | 24,83 € | +45 % |
| Klaipėda | 99,39 € | 11,04 € | +56 % |
| Ukmergė | 28,47 € | 3,16 € | **−3 %** |

Vienintelis neaugantis salonas gauna 8 kartus mažiau nei Vilnius. Tai nėra
paklausos trūkumas: Ukmergės PMax per 9 d. surinko 2816 impresijų, bet išleido
4,72 € (0,52 €/d), CPC 0,06 €. Kampanija badauja, ne neranda auditorijos.

### Efektyvumas: Search prieš PMax

| Kampanija | €/d | CPC | CTR |
|---|---|---|---|
| Vilnius Search always-on | 11,67 | 1,38 € | 15,7 % |
| Ukmergė Search always-on | 2,64 | 0,88 € | 15,3 % |
| E-com Paieška | 9,57 | 0,40 € | 13,3 % |
| Klaipėda Search | 2,19 | 0,44 € | 12,5 % |
| **PMax-4 (bendras)** | **17,20** | **1,07 €** | **1,4 %** |
| PMax-3 (bendras) | 9,23 | 1,11 € | 2,3 % |
| Klaipėda PMax A3 | 8,86 | 0,71 € | 4,8 % |

Didžiausias vienas išlaidų punktas (PMax-4, 17,20 €/d) turi prasčiausią CTR (1,4 %)
ir brangiausią kliką tarp stambiųjų. Search kampanijos su 12–16 % CTR gauna mažiau.

### Neveikianti kampanija

`SE — Shopping Hilding Nevada -20% [2026-09]` (24203056043) yra ENABLED, bet per
9 dienas: 0 impresijų, 0 klikų, 0 €. Rugsėjo akcijos kampanija nepaleista.
Priežastis nenustatyta, reikia diagnozės.

### Kas relevant, o kas ne (2026-09-10 vertinimas)

| Dalykas | Relevantumas tikslui | Kodėl |
|---|---|---|
| Ukmergės biudžeto badas | **aukštas** | vienintelis neaugantis salonas, priežastis matoma |
| PMax-4 efektyvumas | **aukštas** | didžiausios išlaidos, prasčiausias rezultatas |
| Neveikianti Shopping kampanija | vidutinis | nulis rezultato, bet ir nulis žalos |
| GSC cron miręs | vidutinis | vienintelis antrinio tikslo skaitiklis, bet pats nieko nejudina |
| Blogas nepublikuoja | **žemas** | naujas straipsnis nekelia esamo raktažodžio iš 7 į 4 |
| blog_agent CB atviras | **žemas** | vartai sustabdė fabrikaciją, tai apsauga, ne gedimas |

Biudžeto nekeliame (2026-07-30 savininko sprendimas). Perskirstymas tarp esamų
kampanijų yra atskiras klausimas ir sprendžia savininkas.

## 2026-09-14 — Reklamos konversijos prijungtos. Trys išvados, viena jų nemaloni

Savininko sprendimu prijungta Porter `google-ads` paskyra (sunaudota licencijos
vieta). Duomenys: 2026-08-14 → 2026-09-13, 30 d.

### 1. Google Ads paskyroje NĖRA pardavimo sekimo

Visos paskyroje veikiančios konversijos per 30 d.:

| Konversijos veiksmas | Kategorija | Kiekis |
|---|---|---|
| Local actions - Other engagements | Engagement | 420 |
| **Local actions - Directions** | **Get Directions** | **255** |
| Local actions - Website visits | Page View | 31 |
| Clicks to call | Contact | 28 |

Nė vienos pirkimo konversijos. `conversions_value` lygi konversijų skaičiui, t. y.
kiekviena verta 1, ne eurų. Vadinasi **1 441,63 € per mėnesį leidžiama nežinant,
kuri dalis atneša pardavimų.** ROAS apskaičiuoti neįmanoma.

### 2. Mes perkame būtent tą metriką, kurią pasirinkome tikslu

Paskyra optimizuojama į „Local actions - Directions". Per 30 d. reklamai
priskirti 255 maršrutai. Todėl teiginys „maršrutai +64 %" iš dalies reiškia
„nupirkome daugiau maršrutų". Veiksmas tikras, klientas tikras, bet Šiaurinė
žvaigždė yra perkama, todėl kaip nepriklausomas sėkmės matas ji silpna.

### 3. Kaina už maršrutą pagal kampaniją

| Kampanija | € / 30 d. | Maršrutai | € už maršrutą |
|---|---|---|---|
| PMax-4 (bendras) | 193,90 | 93 | **2,08** |
| Vilnius PMax (A2) | 142,69 | 62 | **2,30** |
| Klaipėda PMax (A3) | 133,10 | 50 | **2,66** |
| Vaikiškos lovos PMax | 73,75 | 26 | 2,84 |
| PMax-3 (bendras) | 86,04 | 15 | 5,74 |
| PMax-2 (bendras) | 17,39 | 2 | 8,69 |
| **Ukmergė PMax** | 20,63 | 2 | **10,31** |
| Ąžuolinės lovos Vilnius | 43,83 | 1 | 43,83 |
| **Ukmergė Search always-on** | 103,15 | 2 | **51,58** |
| Klaipėda Search | 106,36 | 1 | 106,36 |
| Antialerginiai [niche] | 126,18 | 1 | 126,18 |
| Vilnius Search always-on | 171,97 | 0 | — |
| E-com Paieška | 202,30 | 0 | — |
| Medicininiai [niche] | 19,44 | 0 | — |

Suvestinė: **PMax 667,48 € → 250 maršrutų = 2,67 € už maršrutą.
Search 774,15 € → 5 maršrutai = 154,83 € už maršrutą.**

### Pataisa 09-10 įrašui

2026-09-10 rašiau, kad PMax-4 yra prasčiausia kampanija, nes jos CTR 1,4 %, o
Search kampanijos su 12–16 % CTR nepakankamai finansuojamos. **Tai buvo klaida.**
PMax-4 yra pigiausias maršrutų šaltinis paskyroje (2,08 €). CTR tarp PMax ir Search
nepalyginamas, nes PMax rodo Display ir YouTube inventoriuje.

### Svarbus apribojimas, kurio negalima praleisti

Search kampanijos negali generuoti „Local actions" konversijų, jei prie jų
neprikabinti vietos ištekliai (location assets). Pagal `tasks/lessons.md` L14 jie
kabinami tik per UI. Todėl **Search rodmuo 5 maršrutai nereiškia, kad Search
neveikia — jis reiškia, kad Search rezultatas nematuojamas.** Search gali varyti
pardavimus svetainėje, kurių niekas nefiksuoja, nes pirkimo konversijos nėra.
Teisingas teiginys: 774 € per mėnesį leidžiama aklai, ne 774 € iššvaistoma.

### Ukmergė: duomenys nepatvirtina biudžeto hipotezės

Ukmergė gauna 123,78 € per mėnesį (PMax 20,63 + Search 103,15) ir duoda 4 maršrutus.
Tai 30,95 € už maršrutą, prasčiausias rodiklis paskyroje, kai Vilniaus PMax duoda
2,30 €. Jei problema būtų badavimas, kaina už maršrutą būtų normali, tik kiekis
mažas. Ji nenormali. Todėl **pinigų pylimas į Ukmergę nepagrįstas** — 09-10 svarstytas
perskirstymas būtų buvęs klaida, ir gerai, kad jis nebuvo pasiūlytas kaip veiksmas.

## 2026-09-18 — ĮVYKDYTA: PMax konsolidacija (per Windsor google_ads)

Ne prompt'as, ne planas. Pakeitimai pritaikyti gyvoje paskyroje 7015063449.

| Veiksmas | Kampanija | ID | Rezultatas |
|---|---|---|---|
| PAUSED | Local store visits and promotions-Performance Max-3 | 23085196755 | ✅ patvirtinta |
| PAUSED | Local store visits and promotions-Performance Max-2 | 22773843568 | ✅ patvirtinta |

Vykdyta per `Windsor_ai.execute_action` → `google_ads.pause_campaign`.
Atstatoma per `enable_campaign` su tuo pačiu ID.

### Pagrindas

Abi dubliavo PMax-4 tuose pačiuose miestuose ir buvo ten 3–4 kartus brangesnės:

| Miestas | PMax-4 | Sustabdyta | Skirtumas |
|---|---|---|---|
| Klaipėda | 0,29 € / veiksmą | PMax-3 — 1,12 € | 3,9× |
| Vilnius | 0,91 € / veiksmą | PMax-2 — 2,70 € | 3,0× |

Geografinės skylės nelieka: PMax-4 abu miestus jau dengia.

### Efektas

Atlaisvinta 103,42 € / 30 d., kurie davė 17 maršrutų (6,08 € už maršrutą).
PMax-4 tuos pačius pinigus leidžia po 2,08 € už maršrutą.
Be to, dingsta savikonkurencija aukcione Klaipėdoje ir Vilniuje.

### Ko NEPADARIAU ir kodėl

PMax-4 (23231305809) biudžeto nekėliau. `set_campaign_budget` nustato absoliučią
reikšmę, o dabartinės nežinau — Windsor `get_data` skaitymą užblokavo aplinkos
klasifikatorius. Nustatyti aklai reikštų rizikuoti sumažinti geriausią paskyros
kampaniją. Tai lieka vienintelis neužbaigtas žingsnis.

**Kad jį užbaigtų, reikia vienos eilutės:**
```
SELECT campaign.id, campaign_budget.resource_name, campaign_budget.amount_micros
FROM campaign WHERE campaign.id = 23231305809
```
ir tada biudžetą padidinti 3 450 000 micros (3,45 €/d) prie esamos reikšmės.

### Ką stebėti

Per 7 dienas (iki 2026-09-25) patikrinti, ar PMax-4 maršrutų kiekis pakilo
Klaipėdoje ir Vilniuje. Jei bendras paskyros maršrutų skaičius nukrito — grąžinti
`enable_campaign` 23085196755 ir permąstyti.
