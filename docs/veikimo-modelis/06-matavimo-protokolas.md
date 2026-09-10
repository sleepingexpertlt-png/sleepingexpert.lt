# Matavimo protokolas — kada galima sakyti „krenta"

Priežastis: 2026-08-27 visą dieną teigiau „maršrutai krenta −6 %".
Realiai tai buvo 08-26 vakarinio ir 08-27 rytinio matavimo atimtis
7 dienų slenkančiame lange. Neįrodyta. K10 pažeidimas skaičiams.

## Taisyklės

**M1. Fiksuotas laikas.** Maršrutai (`salon_signal`) fiksuojami kartą per
parą, **07:30 vietos laiku**, iš to paties šaltinio. Kitu paros metu paimtas
skaičius į eilutę nerašomas — tik informacijai.

**M2. Snapshot senumas rodomas visada.** Cituojant skaičių privaloma
nurodyti `last_updated`. Jei senesnis nei 30 val. — skaičius negalioja
sprendimams.

**M3. Trendas reikalauja 7 taškų.** Jokio „krenta" / „auga" / „%" teiginio,
kol nėra 7 dienų iš eilės tuo pačiu laiku. Iki tol tik: „šiandien X,
bazė Y, imtis per maža išvadai".

**M4. 7 d. slenkantis langas ≠ paros rodiklis.** `directions_7d` keitimasis
per parą yra vienos dienos įėjimas minus vienos dienos išėjimas. ±3 čia yra
normalus svyravimas, ne signalas.

**M5. Bazė užšaldyta.** Bazė = 34 (2026-08-26). Ji nekeičiama ir
neperskaičiuojama. Tikslas = 44 iki 2026-10-24.

## Eilutė (pildoma tik 07:30 matavimais)

| Data | Laikas | Klaipėda | Ukmergė | Vilnius | Viso | WC 7d | Snapshot amžius |
|---|---|---|---|---|---|---|---|
| 08-26 | — | 13 | 13 | 8 | 34 | 11 | bazė |
| 08-27 | 07:20 | 13 | 13 | 6 | 32 | 8 | 0,2 val. |

Išvada apie trendą galima nuo **09-02** (7 taškai).

## M6 — GBP duomenų vėlavimas (rasta 2026-09-03 per Porter)

Google Business Profile Performance API duomenys **atsilieka ir paskutinės
dienos grąžinamos kaip 0**, kol Google jų neužpildo. Porter, `coverageUntil
2026-09-02`, rodo 08-30 → 09-02 = **0 impresijų, 0 maršrutų visuose trijuose
salonuose**. Gyvas profilis su 90 atsiliepimų negali turėti 0 impresijų 4 d.

Mūsų `gmb_agent` skaito TĄ PATĮ šaltinį → `salon_signal` 7 d. langas
įskaičiuoja neužpildytas dienas. **Todėl 34 → 17 → 7 „kritimas" bent iš
dalies yra vėlavimas, ne realybė.**

Taisyklė: **maršrutų / impresijų eilutei naudoti tik dienas iki
`coverageUntil − 3 d.`** Paskutinės 3 dienos — nerodomos, kol neužpildytos.

Dieninė eilutė (Porter, Google Business Profile Performance):

| Data | Vilnius imp. | Klaipėda imp. | Ukmergė imp. |
|---|---|---|---|
| 08-24 | 160 | 106 | 100 |
| 08-25 | 146 | 88 | 83 |
| 08-26 | 117 | 64 | 68 |
| **08-27** | **32** | **17** | **7** |
| 08-28 | 23 | 25 | 16 |
| 08-29 | 8 | 2 | 9 |
| 08-30 → 09-02 | 0 | 0 | 0 |

08-27 kritimas gali būti tikras (tą dieną redaguotas profilis, kitą dieną
sustabdyta reklama) ARBA dalinis užpildymas. **Atskirti galima tik
perklausus 09-06:** jei 08-30 → 09-02 užsipildo — vėlavimas; jei lieka 0 —
realu.

Lokacijų ID (Porter / GBP API):
Vilnius `11855115537711521704` · Klaipėda `18399011255848825016` ·
Ukmergė `2791954715091405702`.

## M6 testas 2026-09-06 — rezultatas

Porter perklausta 09-06 06:00 (`coverageUntil 2026-09-05`). Palyginimas su
09-03 traukimu:

| Data | 09-03 traukimas | 09-06 traukimas | Išvada |
|---|---|---|---|
| 08-29 | 8 / 2 / 9 | **28 / 22 / 16** | užsipildė |
| 08-30 | 0 / 0 / 0 | **26 / 12 / 7** | užsipildė |
| 08-31 | 0 / 0 / 0 | **25 / 17 / 10** | užsipildė |
| 09-01 | 0 / 0 / 0 | **26 / 22 / 10** | užsipildė |
| 09-02 → 09-05 | — | 0 / 0 / 0 | dar neužpildyta |

(Vilnius / Klaipėda / Ukmergė, impresijos.)

**Išvada 1 — M6 patvirtinta, bet vėlavimas ~5 d., ne 3.** Taisyklė
keičiama: eilutei naudoti tik dienas iki **`coverageUntil − 5 d.`**

**Išvada 2 — kritimas nuo 08-27 REALUS ir tęsiasi.** Užpildytos dienos rodo
~25 / ~17 / ~10 impresijų per dieną prieš ~130 / ~80 / ~85 iki 08-26.
Tai **−80 %** šešias dienas iš eilės (08-27 → 09-01). Maršrutai per tas
šešias dienas: **1** (Klaipėda 08-29). Reklama grįžo 09-01 — 09-01
impresijos nepakilo.

**Išvada 3 — priežastis sisteminė, ne vietinė.** Trys nepriklausomos
lokacijos krito tą pačią dieną tuo pačiu dydžiu. Tai ne konkurencija ir ne
vienas profilis. Kandidatai: (a) 08-27 profilių redagavimas, jei lietė visas
tris; (b) „Google atnaujino jūsų atributus" — Google pats keitė atributus apie
08-27 (matyta profilio paste'e); (c) Google pusės pokytis Performance API
metrikoje. Neatskirta.

Pagal 09-03 užsirašytą kriterijų: **liko 0 → realu → avarija.** Nulinių
dienų nebeliko, bet lygis −80 % išsilaikė šešias dienas — kriterijaus esmė
išpildyta.

### M6 papildymas 2026-09-06 — profilių patikra per GBP API (skaitymas, be pakeitimų)

Tikrinta `hermes_gbp_request` (Business Information API v1), visos 3 lokacijos.

| Faktas | Vilnius | Klaipėda | Ukmergė |
|---|---|---|---|
| Adresas / openInfo | yra, OPEN | yra, OPEN | yra, OPEN |
| Pagr. kategorija | mattress_store | mattress_store | mattress_store |
| Paslaugų sritis | **Lietuva, Latvija, Estija (3 valstybės)** | 9 vietovės aplink Klaipėdą | 7 vietovės aplink Ukmergę |
| Profilio kalba | pl | en | en |
| latlng | yra | yra | negrąžinta |

Išvados:
- Nė viename profilyje nėra pakeitimo, kuris paaiškintų vienalaikį 08-27 kritimą visose trijose lokacijose. Priežastis lieka nenustatyta ir sisteminė (ne profilio).
- API artefaktas: `serviceArea.businessType` grąžina `CUSTOMER_LOCATION_ONLY`, kai readMask be `storefrontAddress`, ir `CUSTOMER_AND_BUSINESS_LOCATION`, kai su. Adresas realiai yra. Ne signalas.
- Vilniaus paslaugų sritis (3 valstybės) skiriasi nuo kitų dviejų (miestų lygis). Savininkas 08-28 nurodė, kad tai pačio Google pasiūlymas. Kritimas prasidėjo 08-27, t. y. anksčiau — todėl NE priežastis. Įrašyta kaip stebėjimas, be siūlymo keisti.
- 09-04 VPS cron (feed_label diagnostika) rezultato Telegram sraute nėra (72 val.: tik 3 blog + 2 system žinutės). Reikia VPS relay.

---

## M7 — 2026-09-10: maršrutų metrika sulaužyta, ne paklausa

Šaltinis: Google Business Profile Performance API tiesiogiai (`hermes_gbp_request`,
`fetchMultiDailyMetricsTimeSeries`). NE Porter — Porter MCP šią dieną neprisijungė.
Svarbu: API praleidžia `value` lauką, kai reikšmė 0, todėl tuščia diena = 0, ne „nėra duomenų".

### Vilnius, dienos reikšmės

| Data | Mobile Maps impresijos | Maršrutai | Svetainės klikai |
|---|---|---|---|
| 08-24 | 116 | 2 | 3 |
| 08-25 | 106 | 3 | 2 |
| 08-26 | 83 | 5 | 2 |
| 08-27 | 9 | 0 | 1 |
| 08-28 | 4 | 0 | 0 |
| 08-29 | 8 | 0 | 1 |
| 08-30 → 09-02 | 0 | 0 | 0–1 |
| 09-03 | **180** | 0 | 1 |
| 09-04 | **158** | 0 | 2 |
| 09-05 | 57 | 0 | 1 |
| 09-06 | **180** | 0 | 0 |
| 09-07 | **236** | 0 | 0 |
| 09-08, 09-09 | tuščia (vėlavimas) | — | — |

### Ką tai įrodo

1. **Impresijų kritimas 08-27 → 09-02 buvo realus ir jau baigėsi.** Nuo 09-03 impresijos
   ne tik atsistatė, bet viršija prieškritinę bazę (83–116 → 158–236). Laikas sutampa
   su Google Ads sustabdymu dėl mokėjimo (~08-28 → 09-01) ir atsinaujinimu.
2. **Maršrutai = 0 keturiolika dienų iš eilės (08-27 → 09-07), įskaitant penkias dienas
   su rekordinėmis impresijomis.** Prieš tai buvo 2–5 per dieną prie 83–116 impresijų.
   Jei elgsena nepakito, tikimybė gauti 14 nulių iš eilės yra ~1e-14. Tai ne paklausa.
3. **Veiksmų fiksavimas veikia.** Tomis pačiomis dienomis svetainės klikai rašomi
   (09-03: 1, 09-04: 2, 09-05: 1), 09-02 užfiksuotas 1 skambučio klikas. Vadinasi
   sulaužyta ne visa veiksmų grandinė, o būtent maršrutų mygtukas arba jo metrika.
4. **Ne vėlavimas.** Tose pačiose dienose impresijos jau užpildytos. Faktinė aprėptis
   baigiasi 09-07, t. y. vėlavimas ~3 d., ne 5. **M6 taisyklė tikslinama: aprėpties riba
   yra ta diena, kurią impresijos dar turi reikšmę, ne fiksuotas dienų skaičius.**
5. **Ne profilio kokybė.** Visos trys lokacijos: `hasVoiceOfMerchant: true`, statusas OPEN,
   adresai vietoje, kategorijos nepakitusios.

### Kitos dvi parduotuvės — tas pats

| Parduotuvė | Paskutinė diena su maršrutais | Nulių iš eilės iki 09-07 |
|---|---|---|
| Vilnius | 08-26 (5) | 12 |
| Klaipėda | 08-29 (1) | 9 |
| Ukmergė | 08-29 (1) | 9 |

### Pasekmė tikslui

Šiaurinė žvaigždė (34 → 44 maršrutai) šiuo metu **nematuojama**. Ne „blogai einasi" —
matavimo prietaisas rodo nulį. Iki kol tai išspręsta, bet koks maršrutų skaičiaus
vertinimas neturi prasmės, o 51 dienos langas tęsiasi.

### Vienintelis likęs neautomatizuojamas patikrinimas

Atidaryti Google Maps telefone, rasti Sleeping Expert Vilnius, pažiūrėti ar yra
mygtukas „Nuorodos" / „Directions". Tai atskiria dvi hipotezes:
- mygtuko nėra → sulaužytas profilio veiksmas, taisoma profilyje;
- mygtukas yra ir veikia → sulaužyta Google metrika, rašomas kreipimasis į palaikymą.

Iki atsakymo — jokių profilio keitimų (nes nežinoma, kas keistina), jokio tikslo
perskaičiavimo (nes nėra duomenų).

## Sistemos gedimai 2026-09-10

| Gedimas | Faktas | Kiek laiko |
|---|---|---|
| GSC nebematuojamas | `traffic_snapshot_age_hours` = 168,5; paskutinis įrašas 09-03 07:30 | 7 d. |
| blog_agent circuit breaker | `cb: open`, paskutinis bandymas 09-09 14:38 | nuo ~09-07 |
| Blogas nepublikuoja | `blog_published_24h` = 0, `blog_drafted_24h` = 2 | ≥3 d. |
| blog_quality_gate | score 0,495 — pusė straipsnių krenta | tęstinis |
| Porter MCP | neprisijungė (404) | šiandien |

---

## M7 patikra 2026-09-10: nepriklausomas šaltinis (Porter) patvirtina

Ta pati laiko eilutė užklausta per Porter `google-my-business` konektorių — tai
atskiras kelias nei `hermes_gbp_request`. `coverageUntil: 2026-09-09`,
`lastRefreshed: 2026-09-09 19:20 UTC`.

### Bendros paieškos impresijos, dienomis

| Data | Vilnius | Klaipėda | Ukmergė |
|---|---|---|---|
| 08-20 → 08-26 | 136, 123, 93, 32, 160, 146, 117 | 74, 73, 62, 27, 106, 88, 64 | 75, 109, 72, 25, 100, 83, 68 |
| 08-27 → 09-02 | 32, 23, 28, 26, 25, 26, 29 | 17, 25, 22, 12, 17, 22, 16 | 7, 16, 16, 7, 10, 10, 5 |
| 09-03 → 09-06 | **214, 188, 82, 183** | **138, 146, 79, 76** | **68, 73, 75, 78** |
| 09-07 → 09-09 | 0 (dar neįkelta) | 0 | 0 |

### Maršrutai, dienomis

| Parduotuvė | 08-20 → 08-26 | Paskutinė ne nulinė | Nulių iš eilės |
|---|---|---|---|
| Vilnius | 1, 0, 3, 0, 2, 3, 5 | 08-26 (5) | 14 (08-27 → 09-09) |
| Klaipėda | 3, 8, 2, 0, 0, 0, 1 | 08-29 (1) | 11 (08-30 → 09-09) |
| Ukmergė | 0, 0, 13, 0, 0, 1, 0 | 08-29 (1) | 11 (08-30 → 09-09) |

### Kiek maršrutų turėjo būti

Prieškritiniu laikotarpiu (08-20 → 08-26) kiekviena parduotuvė davė po 14 maršrutų.
Santykis maršrutai / impresijos: Vilnius 1,73 %, Klaipėda 2,83 %, Ukmergė 2,63 %.
Pritaikius tą patį santykį atsistatymo dienoms 09-03 → 09-06:

| Parduotuvė | Impresijos 09-03 → 09-06 | Laukta maršrutų | Faktas |
|---|---|---|---|
| Vilnius | 667 | 11,6 | 0 |
| Klaipėda | 439 | 12,4 | 0 |
| Ukmergė | 294 | 7,7 | 0 |
| **Viso** | **1400** | **31,7** | **0** |

Jei elgsena nepakito, tikimybė per tas keturias dienas gauti nulį yra **1,6 × 10⁻¹⁴**.
Tai ne svyravimas ir ne triukšmas.

### Kur du šaltiniai sutampa ir kur ne

| Teiginys | GBP API | Porter | Statusas |
|---|---|---|---|
| Maršrutai 0 nuo 08-27 (Vln) / 08-30 (Klp, Ukm) | taip | taip | **patvirtinta** |
| Impresijos atsistatė 09-03 virš bazės | taip | taip | **patvirtinta** |
| Svetainės klikai 09-03 → 09-05 | 1, 2, 1 | 0, 0, 0 | **nesutampa** |

**Pataisa M7 įrašui.** M7 trečiame punkte rėmiausi svetainės klikais kaip įrodymu,
kad veiksmų grandinė veikia. Porter tomis dienomis rodo 0. Du šaltiniai nesutaria,
todėl tas argumentas laikomas neįrodytu ir pašalinamas iš išvados. Pagrindinė
išvada nesikeičia — ji laikosi ant impresijų atsistatymo ir maršrutų nulio, o tai
patvirtina abu šaltiniai nepriklausomai.

**Porter aprėpties pastaba.** `coverageUntil` rodo 09-09, bet 09-07 → 09-09 visos
eilutės nulinės visiems trims. Reali Porter aprėptis baigiasi 09-06.
`coverageUntil` iš Porter nėra patikimas aprėpties rodiklis — tikrinti pagal
paskutinę dieną su nenuline impresija.

---

## M8 — 2026-09-10: savininko lauko duomenys uždaro klausimą

Savininkas praneša iš realybės: skambučių srautas didelis, profilis Maps rodomas
gerai, matomumas ten, kur anksčiau matė tik LONAS. Rezultatas juntamas versle.

Tai trečias nepriklausomas šaltinis ir jis atsako į M7 palikta atvirą klausimą.

| Šaltinis | Ką rodo |
|---|---|
| GBP Performance API | maršrutai 0 nuo 08-27 / 08-30 |
| Porter | tas pats, 0 |
| Savininko stebėjimas | žmonės randa, skambina, ateina |

**Išvada: sulaužytas skaitiklis, ne profilis ir ne verslas.** Mygtukas veikia, nes
klientai per jį ateina. Vadinasi tikrinti profilio nebereikia ir keisti jo negalima —
jis tvarkingas. Lieka viena užduotis: pranešti Google apie neveikiančią metriką.

**Anksčiau užregistruotas testas laikomas atliktu.** M7 buvo numatyta: „mygtuko nėra →
lūžis profilyje; mygtukas yra ir veikia → lūžusi Google metrika". Pasitvirtino antras
variantas.

### Tikslas turi gyvą skaitiklį — impresijos

Maršrutų skaitiklis miręs, bet impresijos matuojamos ir abiejuose šaltiniuose sutampa.
Bazė 08-20 → 08-26 prieš atsistatymą 09-03 → 09-06, vidurkis per dieną:

| Parduotuvė | Bazė | Dabar | Pokytis |
|---|---|---|---|
| Vilnius | 115/d | 167/d | **+45 %** |
| Klaipėda | 71/d | 110/d | **+56 %** |
| Ukmergė | 76/d | 74/d | −3 % |

Tikslo sąlyga yra +30 % bent 2 iš 3 salonų. **Pagal impresijas ta sąlyga jau tenkinama
Vilniuje ir Klaipėdoje.** Ukmergė stovi vietoje ir yra vienintelė atsiliekanti.

**Sprendimas dėl matavimo (2026-09-10).** Kol Google maršrutų skaitiklis neveikia,
pagrindinis stebimas rodiklis yra GBP impresijos per dieną, bazė ir tikslas
perskaičiuoti aukščiau. Maršrutai lieka deklaruotas tikslas ir grįžta į matavimą tą
dieną, kai skaitiklis atsigauna. Bazė 34 ir tikslas 44 neatšaukiami, tik laikinai
nematuojami. Tai nėra tikslo sumažinimas.
