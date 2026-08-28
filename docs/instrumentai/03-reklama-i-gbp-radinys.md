# Reklama → GBP maršrutai: patikrinimas 2026-08-27

Owner klausimas: „ar galime siųsti klientus su reklamomis į GMB ir taip kelti
reitingus?" Atsakymas po patikrinimo: **idėja teisinga, bet ji jau įgyvendinta —
ir kaip tik ten, kur jos NĖRA, ir yra mūsų silpniausia vieta.**

## Ką patikrinau ir kuo

Windsor `google_ads` konektorius **užblokuotas** (Free plano paskyrų limitas —
ta pati kliūtis kaip GSC). Tikri duomenys gauti per Hermès CAG (59 failai,
`lessons.md`, `ukmerge_ads_launch.md`).

Šalutinis radinys: **U-003 „Google Ads OAuth (different account)" registre
kabo kaip atviras — bet paskyra 701-506-3449 prijungta tiesiogiai prie Hermès
ir skaitoma per Google Ads API.** Dar vienas pasenęs registro įrašas.

## Radinys 1: reklama į GBP jau veikia

Always-on PMax kampanijos, ne nauja idėja (`lessons.md:L70`, 2026-07-30):

| Kampanija | Biudžetas | Realios išlaidos 7 d. | Tikslas |
|---|---|---|---|
| Klaipėda | 5 €/d | 36,99 € | parduotuvės lankomumas |
| Ukmergė always-on | 5 €/d | 34,50 € | parduotuvės lankomumas |
| E-com | 5 €/d | 34,93 € | **internetiniai pardavimai** |
| Vilnius PMax | ? | **atskirų išlaidų duomenų nėra** | ? |

Ir tai patvirtinta: Google Ads veiksmai su prijungtais lokacijos ištekliais
(PMax store goals + `LOCATION_SYNC`) **prisideda prie GBP maršrutų metrikos.**

## Radinys 2: koreliacija, kurios negalima ignoruoti

| Salonas | Sava lokali kampanija | Maršrutai 7 d. | GBP impresijos |
|---|---|---|---|
| Klaipėda | ✅ 36,99 €/7d | **13** | 192 |
| Ukmergė | ✅ 34,50 €/7d | **13** | 260 |
| **Vilnius** | ❓ nepatvirtinta | **6** | **329** |

Du salonai su sava lokalia kampanija — po 13 maršrutų.
Vilnius, su **didžiausiomis impresijomis ir mažiausiais maršrutais** — be
patvirtintos lokalios kampanijos, tikėtinai apimtas „E-com" kampanijos,
kuri optimizuoja internetinius pardavimus, ne apsilankymus salone.

Tai paaiškintų simptomą tiksliai: žmonės profilį mato (impresijos aukščiausios),
bet niekas jų nestumia į „Maršrutas", nes kampanija optimizuoja kitą veiksmą.

**Du taškai nėra įrodymas** (M3 galioja). Bet tai stipriausia hipotezė, kurią
turim, ir ji pigiai patikrinama.

## Radinys 3: 24 €/d guli ant kampanijų, kurios nerodomos

| Kampanija | Biudžetas | Parodymai 7 d. |
|---|---|---|
| SE — Antialerginiai sprendimai [niche] | 8 €/d | **2** |
| Medicininiai | 8 €/d | **5** |
| Vėsinantys | 8 €/d | **0** |

Pinigai NEdeginami — jos tiesiog nesirodo, tad ir neišleidžia. Bet trys
įjungtos kampanijos, kurios per savaitę surinko 7 parodymus, yra negyvos.
Tai vieta, iš kurios paimti biudžetą Vilniui — sąmoningai suprantant, kad
realios išlaidos tada padidės (nes dabar jos = 0).

## Techninė kliūtis, kurią būtina žinoti

`lessons.md:L14`: **GBP lokacijos ištekliai prie kampanijų prisegami TIK per
Google Ads UI, ne per API.** Vadinasi agentas gali sukurti ir valdyti kampaniją,
bet patį GBP susiejimą turi padaryti owner ranka. Be to žingsnio kampanija
neves maršrutų — ves tik klikus į svetainę.

## Kur riba

Tai NĖRA juoda zona. Reali reklama realiems žmonėms per oficialų Google
produktą (PMax store goals) — Google pats tai parduoda. Juoda zona lieka ta
pati: botai, CTR imitacija, fake atsiliepimai. Riba nesikeičia.

## Ką siūlau — vienas veiksmas, ne sąrašas

Patikrinti Google Ads UI, ar Vilniaus GBP lokacija prisegta prie kampanijos su
parduotuvės lankomumo tikslu. Jei ne — tai stipriausias vienas svertas
silpniausiam salonui, ir jis paaiškina 329 → 6.
