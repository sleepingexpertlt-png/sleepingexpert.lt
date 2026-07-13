# Banerių karuselė — įdiegimo instrukcija

Failas `baneris-karusele.html` — paruošta banerių karuselė pagrindiniam puslapiui:

- ✅ Baneriai keičiasi automatiškai kas 5 sek. (sustoja užvedus pelę)
- ✅ Mobiliesiems — braukimas pirštu (swipe) ir taškeliai apačioje
- ✅ Desktope — rodyklės kairėje/dešinėje
- ✅ Abu baneriai visada vienodo dydžio (1440×450 proporcija) — viskas lygu
- ✅ Suapvalinti kampai, švelnus šešėlis
- ✅ Be jokių papildomų įskiepių — veikia bet kurioje WordPress temoje

## Kaip įdėti į puslapį

1. Atsidarykite **WP Administravimas → Puslapiai → Pagrindinis puslapis → Redaguoti su WPBakery**.
2. Toje vietoje, kur turi būti baneriai, pridėkite elementą **„Raw HTML"**
   (jei redaguojate su Gutenberg — bloką **„Custom HTML"**).
3. Nukopijuokite **visą** failo `baneris-karusele.html` turinį ir įklijuokite.
4. Išsaugokite ir peržiūrėkite puslapį — baneriai jau suksis.

## Ką galima keisti

| Kas | Kur |
|-----|-----|
| Į kokį puslapį veda baneris | `href="..."` prie kiekvieno `<a class="se-banner-slide">` (dabar veda į čiužinių kategoriją) |
| Keitimosi greitis | `var DELAY = 5000;` (milisekundėmis, pvz. `7000` = 7 sek.) |
| Pridėti trečią banerį | Nukopijuokite vieną `<a class="se-banner-slide">...</a>` bloką ir pakeiskite paveikslėlio URL — taškeliai atsiras automatiškai |
| Pakeisti banerį pasibaigus akcijai | Įkelkite naują paveikslėlį į Medija ir pakeiskite `src="..."` nuorodą |

## Mobiliosios banerių versijos

Kataloge `baneriai/mobile/` yra dvi paruoštos mobiliosios versijos (800×500,
su gerokai didesniu tekstu telefonams):

- `graikiski-mobile-800x500.webp`
- `italiski-mobile-800x500.webp`

**Ką padaryti:**

1. Atsisiųskite abu failus ir įkelkite į **WP Administravimas → Medija**
   (nekeiskite failų pavadinimų).
2. Karuselės kodas jau paruoštas — telefonuose (ekranas iki 767 px) jis
   automatiškai rodys mobiliąją versiją, o kompiuteryje — pilną 1440×450 banerį.
3. Jei WordPress įkeliant pakeis failo pavadinimą (pvz., pridės `-1`),
   atnaujinkite `srcset="..."` nuorodas kode (jos pažymėtos komentaru).
