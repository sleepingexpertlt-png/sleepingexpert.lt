# Raktažodžių surinkimas — LT paklausa iš savų šaltinių (owner GO 2026-08-27)

Owner pastebėjimas: trūksta raktažodžių, ypač long tail. Klausimas buvo, ar
juos imti iš Lenkijos rinkos.

## Principas: Lenkija NĖRA raktažodžių šaltinis

Raktažodžiai nekeliauja per kalbą. Išvertus lenkišką frazę gaunam tekstą,
kurio LT niekas neieško — kiti įpročiai, kiti prekės ženklai, kitas žodynas.

Iš Lenkijos imam **TEMŲ SPRAGAS**: kokios temos ten turi didelę paklausą, o
pas mus jų nėra. Tada tikrinam, ar ta tema egzistuoja LT paklausoje, ir tik
tada darom. Lenkija = hipotezių generatorius, ne šaltinis.

## Šaltinių eilė (visi keturi pirmi — 0 €)

| # | Šaltinis | Ką duoda | Kodėl pirma |
|---|---|---|---|
| 1 | **GSC pilna uodega** | realios LT frazės su faktine paklausa | Žiūrėjom tik 5–15 zoną. Tūkstančiai užklausų su 1–5 impresijomis — ten ir gyvena long tail |
| 2 | **Vidinė svetainės paieška** | gryna pirkimo intencija | Ką žmonės rašo MŪSŲ paieškos laukelyje. Visiškai neliestas šaltinis |
| 3 | **Elmo 111 promptų** | AI pusės klausimai | Jau kasama (16-temu-paklausos-tyrimas.md) |
| 4 | **Salono klausimai** | unikalūs, konkurentų neturimi | 3 parduotuvės, pardavėjai girdi tikrus klausimus kasdien. Owner darbas |
| 5 | Lenkija | temų spragos | TIK po 1–4, ir tik hipotezėms |

## Kodėl 4 punktas svarbiausias strategiškai

Konkurentas gali nukopijuoti mūsų tekstą. Negali nukopijuoti to, ką girdi
mūsų pardavėjai. Tai pirminiai duomenys — tiksliai to reikalauja T1 (unikali
vertė) ir E-E-A-T. Net 20 klausimų sąrašas vertingesnis už pirktą įrankį.

## Techninė užduotis (1–3)

**1. GSC pilna uodega**
- Ištraukti VISAS užklausas per 90 d., ne tik 5–15 pozicijų
- Filtras: impressions >= 3 (žemiau — triukšmas)
- Grupuoti: intencija (informacinė / komercinė / lokalinė / prekės ženklo)
- Pažymėti, kurios NETURI atitinkamo puslapio pas mus — tai spragų sąrašas
- Long tail apibrėžimas: >= 4 žodžiai užklausoje

**2. Vidinė svetainės paieška**
- Patikrinti, ar WooCommerce/WP logina paieškos užklausas
  (dažnai per `s=` parametrą GA4 arba per plugin'ą)
- Jei loginа — ištraukti 90 d. ir sugrupuoti kaip 1 punkte
- Jei NEloginа — pasakyti, ir pasiūlyti minimalų būdą įjungti (tai atskiras GO)

**3. Sujungimas**
- Viena lentelė: frazė · šaltinis (GSC/paieška/Elmo) · intencija · ar turim
  puslapį · impresijos/dažnis
- Tema, kuri kartojasi >= 2 šaltiniuose = aukščiausias prioritetas
- Rezultatas: prioritetų sąrašas 2 bangai, ne vien raktažodžių krūva

## Saugikliai

- 0 €. Jokių pirkimų šiame etape.
- Jei kuris šaltinis neprieinamas — pasakyti, neapeiti tyliai (K4).
- Raktažodžių NEKELTI į topic_bank automatiškai — pirma owner peržiūra
  (T2: tempas pagal paklausą, ne pagal pajėgumą).

---

## REZULTATAI (VPS, 2026-08-27) — pilna ataskaita: `data/keyword_gap_report_2026-08-27.md`

| Šaltinis | Kiekis |
|---|---|
| GSC (impressions ≥3) | 1179 frazių iš 2382 |
| — long tail (≥4 žodžiai) | 152 |
| — spragos (atsako tik homepage) | 79 (1 klaidingai teigiamas — brand) |
| **Vidinė paieška** | **499 terminų — LOGINA, GO nereikėjo** |
| Elmo | 111 |
| **Sujungta unikalių** | **1675, iš jų 53 aukšto prioriteto (≥2 šaltiniai)** |

### Top 3 prioritetai 2 bangai

1. **Čiužinys alergiškiems / didelio svorio žmonėms** — 307 impr., svorio tema
   NEDENGTA. Tai patvirtina owner įžvalgą: svoris = individualiausias kriterijus,
   dėl kurio einama konsultuotis, ir mes į jį neatsakom niekur.
2. **„Kur pirkti / kaina / pigiausia čiužinį internetu LT"** klasė — >1200 impr.
   sudėjus variantus, krenta į kategoriją/homepage, nėra dedikuoto gido.
   **B2 draft #24374 jau parašytas šia tema** — greičiausias laimėjimas.
3. Rankų darbo medinės lovos — 134 impr., nišinė.

### Artefaktas

Kelios top frazės turi uodegą „in lithuania?" — panašu į AI-asistento
performuluotas užklausas GSC duomenyse, ne tikrą vartotojo įvestį. Temą imti
pagal pagrindinį lietuvišką klausimą, frazių NEKOPIJUOTI pažodžiui.

## IŠVADA: parinkimo įrankis vietoj straipsnių

Owner: *„4 tai labai individualu — dėl to ateina konsultuotis pas pardavėjus."*

Duomenys tai patvirtina. Individualių klausimų nepaversi raktažodžiais, bet
juos dabar žmonės užduoda AI vietoj to, kad ateitų į saloną. Sprendimas — ne
straipsnis kiekvienam atvejui, o **parinkimo įrankis**: svoris + miego poza +
problema → rekomendacija + „išbandyk salone".

Kodėl tai teisingas formatas:
- padengia šimtus individualių derinių vienu puslapiu
- unikalu (logika gimė iš 600+ modelių ir 3 salonų patirties)
- struktūruota → tokį turinį AI ir cituoja
- pabaigoje vis tiek veda į saloną → dirba PAGRINDINIAM tikslui (maršrutai)

Iš owner reikia ne klausimų sąrašo, o **sprendimo logikos**: pagal ką pardavėjas
renkasi (svoris → kietumo klasė; poza → aukštis; nugaros skausmas → ...;
prakaitavimas → ...; po operacijos → ko vengti). ~10–15 taisyklių, ne šimtai atvejų.
