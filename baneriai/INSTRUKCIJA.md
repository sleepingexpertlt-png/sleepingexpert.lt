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

## Patarimas dėl mobiliųjų

Dabar mobiliajame rodomas tas pats 1440×450 baneris (viskas telpa, niekas nenukerpama,
tik tekstas mažesnis). Jei norėsite dar geresnio skaitomumo telefone, sukurkite banerių
mobilias versijas (pvz., 800×500) ir pakeiskite `<img ...>` į:

```html
<picture>
  <source media="(max-width: 767px)" srcset="MOBILAUS-BANERIO-URL.webp">
  <img src="https://sleepingexpert.lt/wp-content/uploads/2026/07/graikiski-materace-1440x450-1.webp" alt="...">
</picture>
```

ir CSS bloke pridėkite:

```css
@media (max-width:767px){
  .se-banner-slide{aspect-ratio:8/5;}
}
```
