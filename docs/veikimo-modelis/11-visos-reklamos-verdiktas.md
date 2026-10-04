# Visos reklamos kampanijos — verdiktas

**Sudaryta:** 2026-10-04
**Duomenų šaltinis:** paskutinis realus paskyros 7015063449 matavimas
2026-09-14 (langas 2026-08-14 → 2026-09-13, 30 d., per Porter) + optimization
score ekranai 2026-10-04 (owner foto).
**Apribojimas:** šiandien Google Ads skaitymo prieigos nėra (`hermes_ads_gaql`
neprieinamas, Porter neautorizuotas, Windsor išjungtas). Kaštų skaičiai yra
**3 savaičių senumo**. Score — šiandienos.

---

## A. VEIKIA — saugoti

PMax matuojamas: paskyra optimizuojama į „Local actions — Directions",
PMax generuoja šią konversiją ir ji užfiksuojama. Todėl PMax kaina už
maršrutą yra tikras skaičius, ne spėjimas.

| Kampanija | € / 30 d. | Maršrutai | € / maršrutą | Score 10-04 |
|---|---|---|---|---|
| PMax-4 (23231305809) | 193,90 | 93 | **2,08** | 14 % |
| Vilnius PMax (A2) | 142,69 | 62 | **2,30** | 14,1 % |
| Klaipėda PMax (A3) | 133,10 | 50 | **2,66** | 16,1 % |
| Vaikiškos lovos PMax | 73,75 | 26 | 2,84 | 13,6 % |

**Bendrai PMax: 667,48 € → 250 maršrutų = 2,67 € už maršrutą.**

Visos keturios veikia su atmestais assetais (Image quality, 4 asset grupės,
matyta 09-23). Tai reiškia, kad šie 2,08–2,84 € yra pasiekti **sužalota**
kampanija. Sutvarkius assetus kaina turėtų kristi, ne kilti.

## B. SULŪŽĘ — taisyti dabar

| Problema | Kampanija | Įrodymas | Nuostolis |
|---|---|---|---|
| Destination Not Accessible | Miegamojo baldų parduotuvė / Helios Klaipėda asset grupė | Google policy ekranas 09-23 | **100 % — klikas veda į niekur** |
| Proximity 30 km | Vilnius Search (23941125495), criterion 2492543513932 | GAQL 09-19 | 171,97 €/mėn į Vilniaus rajoną, ne į Vilnių |
| Image quality atmesta ×4 | PMax-4, Klaipėda A3, Vilnius A2, Vaikiškos lovos | policy ekranas 09-23 | kokybės, ne nulinis |

30 km spindulys nuo 54,6872 / 25,2797 apima Nemenčinę, Maišiagalą, Rūdiškes.
Pirkėjų auditas (08): Pilaitė 34 % apyvartos, 884 € krepšelis; Centras 1 407 €.
Taikymas neatitinka pirkėjo nė viena kryptimi.

## C. BRANGU — matuojama ir patvirtinta

| Kampanija | € / 30 d. | Maršrutai | € / maršrutą | Score |
|---|---|---|---|---|
| **Ukmergė PMax** (23941982295) | 20,63 | 2 | **10,31** | 13,5 % |

Ukmergė PMax yra 5× brangesnė už PMax-4 toje pačioje sistemoje, su tuo pačiu
matavimu. Čia palyginimas teisėtas. 09-10 svarstyta hipotezė „Ukmergė badauja"
duomenų nepatvirtinta: badaujanti kampanija turi normalią kainą ir mažą kiekį,
o šios kaina nenormali.

## D. NEMATUOJAMA — negalima nei girti, nei pjauti

| Kampanija | € / 30 d. | Maršrutai | Score |
|---|---|---|---|
| E-com Paieška | 202,30 | 0 | **61,5 %** |
| Vilnius Search always-on | 171,97 | 0 | — |
| Antialerginiai [niche] | 126,18 | 1 | — |
| Klaipėda Search | 106,36 | 1 | — |
| Ukmergė Search always-on (23941122366) | 103,15 | 2 | — |
| Ąžuolinės lovos Vilnius | 43,83 | 1 | — |
| Medicininiai [niche] | 19,44 | 0 | — |

**Viso Search: 774,15 €/mėn → 5 užfiksuoti maršrutai.**

**Šito NEGALIMA skaityti kaip „Search neveikia".** Search kampanijos fiziškai
negali generuoti „Local actions" konversijų, jei prie jų neprikabinti location
assets (`tasks/lessons.md` L14 — kabinami tik per UI). Pirkimo konversijos
paskyroje irgi nėra nė vienos. Todėl 774 € per mėnesį leidžiama **aklai**, o ne
įrodytai iššvaistoma. Pjauti nematuojamą kanalą remiantis nuliu, kurį pats
matavimas ir sukūrė — tai ta pati klaida, kurią padariau 09-10 su PMax-4 CTR.

**Teisingas veiksmas čia nėra pjauti. Teisingas veiksmas — prikabinti location
assets, kad per 30 d. atsirastų tikras skaičius, ir tada spręsti.**

E-com Paieška atskirai: 202,30 €/mėn, o visas online kanalas per 30 d. duoda
3 užsakymus / 1 089,45 € (2026-10-04). Score 61,5 % — sveikiausia paskyroje.
Bet 202 € prieš 1 089 € viso online kanalo yra klausimas, į kurį atsakys tik
pirkimo konversijos sekimas.

## E. NEGYVA — nulis naudos, nulis žalos

| Kampanija | Būsena |
|---|---|
| SE — Shopping Hilding Nevada -20% (24203056043) | ENABLED, 0 impresijų, 0 klikų, 0 € per 9 d. (09-10 patikra) |
| PMax-3 (23085196755) | PAUSED 09-18 — mano veiksmas |
| PMax-2 (22773843568) | PAUSED 09-18 — mano veiksmas |

PMax-3 ir PMax-2 sustabdytos todėl, kad dubliavo PMax-4 tuose pačiuose miestuose
3,9× brangiau (Klaipėda: 0,29 € vs 1,12 € už veiksmą). Sprendimas lieka teisingas
pagal skaičius. Bet jis buvo priimtas nepatikrinus asset grupių tinkamumo — tai
mano klaida, pripažinta 09-23 ir vis dar neištaisyta.

---

## Veiksmų eilė pagal € (ne pagal patogumą)

1. **PAUSE** asset grupę su Destination Not Accessible (Helios Klaipėda).
   Vienintelis punktas, kur kiekviena diena = 100 % nuostolis.
2. **Automated promotions → Off** (iki 10-11; žr. dok. 10).
3. **Proximity 30 km → 10 km** kampanijoje 23941125495. Sukurti naują, tada
   šalinti `customers/7015063449/campaignCriteria/23941125495~2492543513932`.
   **PMax-4 (23231305809) geo NELIESTI.**
4. **Image quality ×4** — pakeisti atmestus paveikslėlius.
5. **Ukmergė PMax** — stabdyti arba perdaryti. 10,31 € už maršrutą nepateisinama.
6. **Location assets prie Search kampanijų** — kad 774 €/mėn nustotų būti akli.
7. **Shopping Hilding Nevada (24203056043)** — šalinti, tik triukšmas.

## Ko šiame dokumente NĖRA ir kodėl

Šviežių kaštų. Paskutinis realus matavimas — 09-14. Be Google Ads skaitymo
prieigos naujesnių skaičių paimti neįmanoma, o spėti — ne.
