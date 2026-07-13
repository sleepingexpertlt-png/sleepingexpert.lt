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

## Mobiliosios banerių versijos (nebenaudojamos)

Kataloge `baneriai/mobile/` yra AI atkurtos mobiliosios banerių versijos (800×500).
DĖMESIO: jose CANDIA ir flexyflex logotipai yra supaprastinti (ne originalūs
prekių ženklų logotipai), todėl pagrindiniame kode jos NENAUDOJAMOS — karuselė
visur rodo originalius 1440×450 banerius.

Jei norėsite tikrų mobiliųjų versijų, jas reikia pasigaminti iš originalių
maketo failų (su tikrais logotipais), įkelti į Mediją ir apvynioti `<img>` taip:

```html
<picture>
  <source media="(max-width: 767px)" srcset="MOBILIOJO-BANERIO-URL.webp">
  <img src="ORIGINALAUS-BANERIO-URL.webp" alt="...">
</picture>
```
