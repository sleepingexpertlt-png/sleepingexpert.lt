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

## Kaip patalpinti adresu sleepingexpert.lt/link/

Svetainė hostinama Hostinger, failų sistema nepasiekiama, todėl naudojami du
dalykai: WP media (failo saugykla) ir Code Snippet (atiduoda failą adresu `/link/`).

**1 žingsnis, vieną kartą: Code Snippet**

1. WP Admin → Snippets → Add New.
2. Pavadinimas: `SE Bio Link (/link/)`.
3. Įklijuokite `biolink/wp-snippet.php` turinį be pirmos eilutės `<?php`.
4. Scope: „Run snippet everywhere". Save Changes and Activate.

Snippet'as reaguoja tik į `/link/`. Kol media bibliotekoje nėra failo, jis nieko
nedaro ir svetainė veikia kaip anksčiau.

**2 žingsnis, kiekvieną kartą atnaujinus puslapį: įkelti failą**

Iš VPS (`72.61.139.213`), kur yra `secrets.env` su `WP_USER` ir `WP_APP_PASSWORD`:

```bash
cd /root/sleepingexpert.lt && git pull
set -a && source /root/frontier-agent/config/secrets.env && set +a
python3 biolink/deploy.py            # dry run: parodo, ką darys
python3 biolink/deploy.py --apply    # įkelia, ištrina senas versijas
```

Skriptas įkelia `index.html` į media kaip `se-biolink-<data>.html`. Jei WordPress
neleidžia `.html`, automatiškai įkelia kaip `.txt`, snippet'ui tai nesvarbu.
Senos versijos ištrinamos, kad snippet'as visada rastų naujausią.

**3 žingsnis: patikrinti**

Atidarykite `https://sleepingexpert.lt/link/?s=tiktok`. Jei matote seną versiją,
LiteSpeed Cache → Toolbox → Purge All.

Kodėl ne paprastas WP puslapis: tema apvyniotų jį savo header ir footer, o
WordPress redaktorius keistų HTML. Snippet'as atiduoda failą tokį, koks yra.

## Brandbook taisyklės, kurių laikomasi

- Spalvos: Hortense Blue `#142b6f`, Phenyl Blue `#3b40f0`, Lemon Chrome `#ffd602`, Mauvette `#e1dee7`.
- Šriftas: Outfit (Bold antraštėms, Regular tekstui).
- „Miegamasis, tai mes!" naudojamas tik kaip užbaigimas poraštėje.
- Nėra draudžiamų teiginių („premium", „nemokamas pristatymas", „pigiai" ir pan.).
