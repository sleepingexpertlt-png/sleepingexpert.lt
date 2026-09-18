# VPS prompt 2026-09-18 — ar mus matyti Maps'e ten, kur LONAS

## Kodėl

Savininkas važiavo Kalvarijų gatve ir Maps žemėlapyje matė LONAS etiketę, o
Sleeping Expert — ne. Patikrinta: **LONAS yra Kalvarijų g. 125A, PC Baldų Rojus.
Mes esame Kalvarijų g. 125, PC Baldų Rojus, 3 aukštas.** Tas pats pastatas.

Ekrano nuotrauka viena savaime įrodo mažai, nes tai buvo navigacijos režimas, o
jame Google slepia daugumą POI etikečių. Bet klausimas realus ir neišmatuotas.

## Ką padaryti

### 1. Geo tinklelis apie PC Baldų Rojus

Centras: 54.7102741, 25.287502 (mūsų GBP koordinatės).
Taškai: 3×3 tinklelis, žingsnis 1 km, plius centras. Iš viso 9 taškai.

Užklausos (kiekvienam taškui visos trys):
- `čiužiniai`
- `lovos`
- `čiužinių parduotuvė`

Kiekvienam taške × užklausai užfiksuok vietinį paketą (local pack / Maps top):

`taškas (lat,lng) | užklausa | mūsų pozicija | LONAS pozicija | kas 1-as`

Jei mūsų nėra top 20 — rašyk `nerastas`, ne tuščią lauką.

### 2. Palyginimas su LONAS profiliu

Abiem (mūsų Vilnius ir LONAS Kalvarijų 125A) surink iš viešo GBP:
- pagrindinė kategorija
- papildomos kategorijos
- atsiliepimų skaičius ir vidurkis
- nuotraukų skaičius
- ar yra produktai, ar yra postai, kada paskutinis
- adreso formatas (ar 125A yra atskira gatvės numeracija, ar mes rodomi kaip
  aukštas pastate)

### 3. Atsakyk į vieną klausimą

Ar mes iš tikrųjų rodomi silpniau toje pačioje vietoje, ar nuotrauka buvo tik
navigacijos režimo artefaktas? Atsakyk skaičiais iš 1 punkto, ne nuomone.

## Hipotezė, kurią reikia patvirtinti arba paneigti

LONAS turi atskirą gatvės numerį (125A), o mes esame „125, 3 aukštas".
Google atskirą gatvės adresą laiko stipresniu vietos subjektu nei aukštą
pastate. Jei tinklelis parodys, kad mes sistemingai žemiau — tai kandidatas
į priežastį, ir tada svarstysim adreso formatą profilyje.

**Nekeisk profilio.** Šitas žingsnis tik matuoja.

## Rezultatas

Įrašyk į `docs/instrumentai/07-maps-geo-tinklelis-2026-09-18.md` ir push'ink.

## Atsakymo formatas

Trys dalys. Lentelė iš 1 punkto pilna, be sutrumpinimų.
Jei kažko nepavyko gauti — tiksli klaida, ne spėjimas.
