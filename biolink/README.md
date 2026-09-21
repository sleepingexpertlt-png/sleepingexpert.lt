# Bio link puslapis — `biolink/index.html`

Vienas bendras įmonės „link in bio" puslapis TikTok, Instagram, Facebook, YouTube
ir kitiems profiliams. Vienas HTML failas, be priklausomybių, be serverio logikos.

Kas viduje:

- Geltonas pagrindinis CTA į e-parduotuvę, po juo kategorijos, blogas, parduotuvės.
- Socialinių tinklų ikonų eilutė (rodomos tik užpildytos).
- 3 parduotuvių kortelės su „Žemėlapis" nuoroda į Google Maps.
- Telefonas (`tel:`) ir el. paštas (`mailto:`) vienu paspaudimu.
- Dalinimosi mygtukas (native share arba kopijavimas).
- Šviesus ir tamsus režimas, Outfit šriftas, brandbook spalvos.
- `Organization` JSON-LD su `sameAs` į socialinius profilius.

## Kaip redaguoti nuorodas

Visi adresai yra failo pradžioje, bloke `window.SE_LINKS = { ... }`.
Tuščias laukas (`""`) reiškia, kad mygtukas ar ikona nerodoma.

Šiuo metu **neužpildyti** (nerasta patikrintų adresų):

```js
tiktok:   "",   // pvz. "https://www.tiktok.com/@sleepingexpert.lt"
youtube:  "",   // pvz. "https://www.youtube.com/@sleepingexpert"
linkedin: "",
pinterest: ""
```

Įrašykite tikslius profilių adresus ir ikonos atsiras automatiškai.

Facebook šiuo metu naudoja `profile.php?id=61559599675030`. Žinių bazėje
minimas ir antras puslapis „Sleeping Expert Lietuva" (`61581127108424`), kuris
gali būti dublikatas. Palikite tą, kuris naudojamas reklamai.

## Srauto žymėjimas (UTM) pagal platformą

Visos nuorodos į `sleepingexpert.lt` automatiškai gauna
`utm_source`, `utm_medium=social`, `utm_campaign=biolink`.

Šaltinis imamas iš puslapio adreso parametro `s`. Į kiekvieno profilio bio
įdėkite skirtingą variantą, ir GA4 / Rank Math rodys, iš kur atėjo žmogus:

| Profilis  | Nuoroda bio laukelyje                     |
|-----------|-------------------------------------------|
| TikTok    | `https://sleepingexpert.lt/link/?s=tiktok`    |
| Instagram | `https://sleepingexpert.lt/link/?s=instagram` |
| Facebook  | `https://sleepingexpert.lt/link/?s=facebook`  |
| YouTube   | `https://sleepingexpert.lt/link/?s=youtube`   |

Be parametro naudojamas `utm_source=biolink`.

## Kur patalpinti

Rekomenduojamas adresas: `https://sleepingexpert.lt/link/` (trumpas, savo domenas,
be trečiųjų šalių logotipų kaip Linktree).

**Variantas A — WordPress (sleepingexpert.lt), FTP / failų tvarkyklė**

1. Sukurkite katalogą `link` svetainės šaknyje (šalia `wp-content`).
2. Įkelkite `index.html` į `/link/`.
3. Atidarykite `https://sleepingexpert.lt/link/`. Jokių įskiepių nereikia.

**Variantas B — WordPress puslapis**

1. Puslapiai → Pridėti naują, slug `link`, šablonas „Blank" / „Canvas" (be antraštės ir poraštės).
2. Įdėkite bloką „Custom HTML" ir įklijuokite viso failo turinį nuo `<script>` (konfigūracija)
   iki pabaigos, praleidžiant `<html>`, `<head>` ir `<body>` žymes.
   Šriftą `Outfit` pridėkite per temos nustatymus arba palikite `<link>` eilutę.

**Variantas C — GitHub Pages / Vercel / Netlify**

Nukreipkite į katalogą `biolink/`. Tada TikTok bio naudokite subdomeną,
pvz. `link.sleepingexpert.lt` (CNAME į hostingą).

## Brandbook taisyklės, kurių laikomasi

- Spalvos: Hortense Blue `#142b6f`, Phenyl Blue `#3b40f0`, Lemon Chrome `#ffd602`, Mauvette `#e1dee7`.
- Šriftas: Outfit (Bold antraštėms, Regular tekstui).
- „Miegamasis, tai mes!" naudojamas tik kaip užbaigimas poraštėje.
- Nėra draudžiamų teiginių („premium", „nemokamas pristatymas", „pigiai" ir pan.).
