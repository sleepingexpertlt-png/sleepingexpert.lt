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
