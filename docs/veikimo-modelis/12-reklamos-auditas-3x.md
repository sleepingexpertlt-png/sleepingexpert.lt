# 🔍 Auditor Report — reklamos gerinimas, patikrinta 3×

**Data:** 2026-10-04
**Skill:** `hermes-auditor` (5 testai)
**Hipotezė tikrinta:** „daugiau maršrutų = daugiau pinigų" + „perkelti Search
biudžetą (774,15 €/mėn) į PMax (2,67 €/maršrutą)"

## Divergence Score: 10,0/10 🔴

| Matas | Vykdymas |
|---|---|
| Šiaurinė žvaigždė (maršrutai 76 / tikslas 44) | **173 %** |
| Pinigai (39 806 € / 83 000 €) | **48 %** |

`|173−48| / 48 × 10 = 26 → cap 10`. Metrika, kurią perkame, viršyta 1,7×.
Metrika, kuri moka, pusiaukelėje. Tai DIVERGENCE ALERT, ne sėkmė.

---

## PATIKRA 1 — aritmetika (perskaičiuota iš šaltinių)

| Šaltinis | Amžius | Testas 5 |
|---|---|---|
| `hermes_business_metrics` 2026-10-04 06:15 | ~12 h | ⚠️ |
| vault `project_typed_judgments_2026-09-30.md` (09-29) | 5 d. | ⚠️ |
| `hermes_status` snapshot 2026-10-04 07:20 | 10,5 h | ⚠️ |
| Porter Ads matavimas 2026-09-14 (langas 08-14→09-13) | **20 d.** | 🔴 |

Salonų −7 839,56 € = −4 138,31 € (4 užsakymai) + −3 701,25 € (krepšelis
1 034,58 → 944,30 €). Dalys sutampa su suma iki cento. ✅

## PATIKRA 2 — natūralus eksperimentas (falsifikacija)

| | 09-28/29 | 10-04 | Pokytis |
|---|---|---|---|
| Maršrutai 7 d. | 63 | 76 | **+20,6 %** |
| Apyvarta 30 d. | 48 004 € | 39 806 € | **−17,1 %** |

**Hipotezė „daugiau maršrutų = daugiau pinigų" šiame lange FALSIFIKUOTA.**
Koreliacija neigiama.

Sąžiningas apribojimas: maršrutų langas 7 d., apyvartos — 30 d. slenkantis;
čiužinio pirkimas yra svarstomas pirkinys su savaičių lagu. Todėl testas
**neįrodo**, kad maršrutai beverčiai. Jis įrodo, kad maršrutai **netinka kaip
trumpalaikis pinigų prediktorius**, o mes būtent pagal juos optimizuojame.

## PATIKRA 3 — nepriklausomas Brain Council (`hermes_council`)

`escalation_id 202`, avg 5,86/10, sprendimas **escalate**.

| Agentas | Balas | Verdiktas |
|---|---|---|
| skeptic | 4 | **REJECT** |
| cfo | 6 | ESCALATE — reikia ROI pagrindimo |

Likę agentai (seo/brand/customer/neuro/video_script) vertino turinio
formuluotę, ne biudžeto logiką — jų balai šiai temai nerelevantūs ir į
sprendimą neimami. Du relevantūs agentai abu sako: neperkelti.

---

## SIMULIACIJA — Search → PMax

| Scenarijus | Prielaida | Rezultatas |
|---|---|---|
| Be išsėmimo | 2,67 €/maršrutą išlieka | +290 → 540 maršrutų/mėn |
| Ribinė kaina ×1,5 | aukciono prisotinimas | +193 → 443/mėn |
| Ribinė kaina ×2,0 | realistiškiausia | +145 → 395/mėn |

**Visi trys scenarijai perka tą pačią metriką, kuri PATIKROJE 2 parodė
neigiamą koreliaciją su pinigais.** Ir visi trys sunaikina kanalą, kurio
rezultato nematome — ne todėl, kad jo nėra, o todėl, kad Search be location
assets fiziškai negali fiksuoti Local actions.

**Verdiktas: NEVYKDYTI.** Perskirstymas pagrįstas nuliu, kurį sukūrė pats
matavimas.

---

## Ką daryti vietoj to (visi 0 € biudžeto)

| # | Veiksmas | Kaina | Ką atrakina |
|---|---|---|---|
| 1 | PAUSE asset grupę su Destination Not Accessible | 0 € | vienintelė vieta, kur 100 % nuostolis |
| 2 | Pirkimo konversijos sekimas | 0 € | 1 441 €/mėn nustoja būti akli; ROAS tampa skaičiuojamas |
| 3 | Location assets prie 7 Search kampanijų | 0 € | 774 €/mėn tampa matuojami |
| 4 | Automated promotions → Off (iki 10-11) | 0 € | žr. dok. 10 |
| 5 | Proximity 30 km → 10 km (23941125495) | 0 € | 171,97 €/mėn į teisingą geografiją |
| 6 | Image quality ×4 | 0 € | PMax nustoja dirbti sužalotas |

Nė vienas nereikalauja papildomo euro. Visi šeši reikalauja prieigos prie
paskyros.

## 🔁 RITUAL FLAG — tikroji kliūtis turi numerį

`hermes_promises` → **U-003: „Google Ads OAuth (different account) — current
OAuth account lacks customer 7015063449 access. Action: user re-OAuth with SE
admin Google account."** Statusas: user-blocked.

Tai nėra nauja problema ir ne šios sesijos trūkumas. Tai užregistruota kliūtis,
dėl kurios Hermès negali nei skaityti, nei rašyti į reklamos paskyrą. Kol
U-003 atviras, kiekvienas reklamos pasiūlymas lieka tekstu.

## Didžiausias pinigas yra ne reklamoje

Krepšelio kritimas −3 701 €/mėn = **2,6× viso reklamos biudžeto** (1 441,63 €).
Net tobulai sutvarkyta reklama šito nepadengia. Geriausia reklamos optimizacija
šiandien duoda mažiau nei grąžinti vidutinį krepšelį iš 944 € į 1 035 €.
