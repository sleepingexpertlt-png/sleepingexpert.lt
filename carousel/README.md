# 📺 Sleeping Expert — produktų karuselė TV ekranams ir el. stendams

Savarankiška reklaminė karuselė: paima prekes iš **sleepingexpert.lt**, parodo jas
per televizorių arba elektroninį stendą — su nuotraukomis, kainomis ir
**ryškiai akcentuotomis šiuo metu vykstančiomis nuolaidomis**.

> **Nepriklauso nuo VPS, Claude, Hermes ar jokios kitos sistemos.**
> Reikia tik `python3` (jau būna kiekviename Linux/Mac; Windows — vienas diegimas).
> Jokių `pip install`, jokių node_modules, jokių API raktų.

---

## ⚡ Greitas startas (30 sekundžių)

```bash
cd carousel
cp config.example.json config.json          # nebūtina — veiks ir be jo
python3 fetch_products.py                   # parsisiunčia prekes + nuotraukas
python3 serve.py                            # paleidžia ekraną
```

Atsidaryk `http://localhost:8080/` ir spausk **F** (visas ekranas).

Nori pirma pamatyti, kaip atrodo, be jokio interneto?

```bash
python3 fetch_products.py --demo && python3 serve.py
```

---

## 🧭 Kaip tai veikia

```
sleepingexpert.lt                 ┌──────────────────────────────┐
   WooCommerce Store API  ──────► │ fetch_products.py            │
   (viešas, be raktų)             │  • kainos, nuolaidos, foto   │
                                  │  • data/products.json        │
                                  │  • data/images/*.jpg         │
                                  └──────────────┬───────────────┘
                                                 │ (veikia ir be interneto)
                                  ┌──────────────▼───────────────┐
                                  │ serve.py  →  player/         │
                                  │  karuselė naršyklėje         │
                                  └──────────────┬───────────────┘
                                                 │
                                     📺 TV / el. stendas (kioskas)
```

Kai duomenys kartą parsisiųsti, **ekranas veikia ir dingus internetui** —
nuotraukos ir kainos guli vietiniame diske.

---

## 🚀 Trys diegimo būdai

### A. Raspberry Pi / mini kompiuteris prie TV (rekomenduojama)

Pilnai automatinis: kas valandą pasiima naujas kainas, pats startuoja po elektros dingimo.

```bash
sudo mkdir -p /opt/se-carousel
sudo cp -r carousel/* /opt/se-carousel/
sudo chown -R pi:pi /opt/se-carousel

cd /opt/se-carousel
python3 fetch_products.py                    # pirmas parsisiuntimas

sudo cp systemd/se-carousel.service /etc/systemd/system/
sudo cp systemd/se-carousel-fetch.* /etc/systemd/system/
sudo cp kiosk/se-carousel-kiosk.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now se-carousel.service        # serveris
sudo systemctl enable --now se-carousel-fetch.timer    # atnaujinimas kas valandą
sudo systemctl enable --now se-carousel-kiosk.service  # Chromium pilnu ekranu
```

> Jei naudotojas ne `pi` arba katalogas kitas — pataisyk `User=` ir kelius
> `.service` failuose.

Patikrinimas:

```bash
systemctl status se-carousel.service
systemctl list-timers se-carousel-fetch.timer
journalctl -u se-carousel-fetch.service -n 30
```

### B. Vienas HTML failas ant USB atmintuko (be Python ekrane)

Tinka, kai stendas ar Smart TV moka tik atidaryti failą arba kai nenori
nieko diegti parduotuvėje.

```bash
python3 fetch_products.py
python3 tools/build_standalone.py            # → dist/karusele.html
# arba lengvesnis variantas tik su akcijomis:
python3 tools/build_standalone.py --only-sale --limit 40
```

Gaunamas **vienas failas**, kuriame jau yra viskas — logika, stilius, kainos ir
nuotraukos (įkoduotos viduje). Nusikopijuok į USB, atidaryk naršykle, spausk `F`.
Interneto nereikia visiškai.

Kai nori atnaujinti kainas — perleidi tas pačias dvi komandas ir pakeiti failą.

### C. Esamas parduotuvės kompiuteris

```bash
python3 fetch_products.py && python3 serve.py
```

Serveris rodo ir tinklo adresą (pvz. `http://192.168.1.42:8080/`) — tą adresą
gali atsidaryti bet kuris tame pačiame tinkle esantis TV ar planšetė.

---

## 🎛️ Nustatymai — `config.json`

Nukopijuok `config.example.json` → `config.json`.

### Kokias prekes imti

| Laukas | Reikšmė |
|---|---|
| `site_url` | Svetainės adresas (`https://sleepingexpert.lt`) |
| `categories` | Rodyti tik šias kategorijas, pvz. `["ciuziniai", "pagalves"]`. Tuščias = visos |
| `exclude_categories` | Kategorijos, kurių nerodyti |
| `only_on_sale` | `true` → **ekrane tik akcijos** |
| `min_discount_percent` | Pvz. `20` → tik nuolaidos nuo −20 % |
| `only_in_stock` | Nerodyti to, ko nėra sandėlyje |
| `max_products` | Kiek daugiausia prekių (numatyta 120) |
| `sort` | `discount` (didžiausios nuolaidos pirma), `price_desc`, `price_asc`, `name`, `random` |
| `download_images` | `true` = veiks be interneto; `false` = nuotraukos tiesiai iš svetainės |

### Kaip rodyti — `display`

| Laukas | Reikšmė |
|---|---|
| `slide_seconds` / `sale_slide_seconds` | Kiek sekundžių rodoma įprasta / akcijinė prekė (akcijos ilgiau) |
| `sale_ratio` | Kokia dalis skaidrių turi būti akcijos. `0.5` = pusė, `0.7` = 70 % |
| `sale_first` | Didžiausios nuolaidos rodomos anksčiau |
| `summary_every` | Kas kelias prekes įterpti **„Akcijos — iki −38 %“** suvestinės skaidrę (`0` = išjungti) |
| `show_qr` | QR kodas su nuoroda į prekę — klientas nuskenuoja telefonu |
| `cta_text` | Geltona raginimo juosta, pvz. `"Klauskite konsultanto salone"` |
| `sale_note` | Smulkus prierašas prie akcijų (pvz. akcijos sąlygos). Tuščias — nerodomas |
| `orientation` | `auto`, `portrait` (stendams), `landscape` (TV) |
| `refresh_minutes` | Kas kiek minučių ekranas pasiima naujus duomenis nepertraukdamas rodymo |
| `reload_hours` | Profilaktinis puslapio perkrovimas (kioske naudinga; `0` = išjungti) |
| `stores`, `footer_text`, `headline` | Apatinė juosta ir logotipo užrašas |

Pakeitus `display` nustatymus, perleisk `python3 fetch_products.py`
(jis perrašo `data/display.json`) arba redaguok `data/display.json` tiesiogiai.

---

## 🔥 Kaip akcentuojamos nuolaidos

Nuolaidos ekrane matomos iškart, be jokio papildomo darbo:

1. **Raudonas pulsuojantis ženklas `−38 %`** ant nuotraukos.
2. **Perbraukta sena kaina** šalia geltonos naujos kainos.
3. **„Sutaupote 30,00 €“** — konkreti nauda eurais, ne tik procentai.
4. **Akcijos rodomos ilgiau** (`sale_slide_seconds`) ir dažniau (`sale_ratio`).
5. **Suvestinės skaidrė** kas kelias prekes: „Akcijos — iki −38 %“ su 6 didžiausiomis nuolaidomis.
6. Norint 100 % akcijų ekrano — `"only_on_sale": true` arba adresas `…:8080/?only_sale=1`.

Kainos ir nuolaidos imamos tiesiai iš WooCommerce, todėl **ekranas visada rodo
tą pačią kainą kaip svetainė** — nieko nereikia vesti ranka.

---

## ⌨️ Valdymas ekrane

| Klavišas | Veiksmas |
|---|---|
| `Tarpas` | Pauzė / tęsti |
| `←` `→` | Ankstesnė / kita prekė |
| `F` | Visas ekranas |
| `R` | Perkrauti duomenis |
| `S` | Perjungti „tik akcijos“ ↔ „visos prekės“ |
| `H` | Valdymo priminimas |

Adreso parametrai (patogu, kai keli ekranai iš to paties serverio):

```
http://localhost:8080/?only_sale=1                 → tik akcijos
http://localhost:8080/?interval=6                  → greitesnė rotacija
http://localhost:8080/?orientation=portrait        → stendo režimas
http://localhost:8080/?nochrome=1                  → be laikrodžio ir adresų juostos
```

Pvz. TV salėje rodo visas prekes, o stendas prie įėjimo — tik akcijas.

---

## 🖥️ Patarimai TV ir stendams

- **Vertikalus stendas**: `"orientation": "portrait"` arba `?orientation=portrait`.
  Ekrano pasukimas Raspberry Pi: į `/boot/firmware/config.txt` įrašyk `display_rotate=1`.
- **Ekranas neužmiega**: `kiosk/start-kiosk.sh` tai padaro pats (`xset -dpms`).
- **Pelės žymeklis paslėptas** (`cursor: none` + `unclutter`).
- **Įdegimo (burn-in) prevencija**: skaidrės nuolat keičiasi, statiškų elementų
  beveik nėra. OLED ekranams verta `slide_seconds` laikyti ≤ 12 s.
- **Nutrūkus internetui** ekranas nesustoja — rodo paskutinius parsisiųstus duomenis.
- **Dingus elektrai** `systemd` viską pakelia automatiškai.

---

## 🔧 Trikčių šalinimas

| Simptomas | Sprendimas |
|---|---|
| „Kraunami produktai…“ neišnyksta | Nepaleistas `fetch_products.py`. Paleisk `python3 fetch_products.py --demo` ir patikrink, ar atsiranda `data/products.json` |
| `Store API nepavyko` | Svetainėje išjungtas WooCommerce Store API. Įrašyk `auth.consumer_key` / `consumer_secret` į `config.json` (WooCommerce → Nustatymai → Išplėstiniai → REST API) — tada naudojamas `wc/v3` |
| Nėra nuotraukų | Paleisk `python3 fetch_products.py --force` (persisiunčia iš naujo) |
| Rodo senas kainas | `systemctl list-timers se-carousel-fetch.timer`; rankiniu būdu — `python3 fetch_products.py` ir ekrane `R` |
| Per daug / per mažai akcijų | Keisk `sale_ratio` ir `min_discount_percent` |
| Chromium rodo „netvarkingai išsijungė“ | `start-kiosk.sh` tai išvalo automatiškai — naudok jį, ne rankinį paleidimą |
| Failas `dist/karusele.html` per didelis | `--limit 40` arba `--only-sale` |

Naudingos komandos:

```bash
python3 fetch_products.py --only-sale     # tik akcijos
python3 fetch_products.py --limit 30      # mažiau prekių
python3 fetch_products.py --no-images     # nuotraukos tiesiai iš svetainės
python3 serve.py --port 8000              # kitas prievadas
```

---

## 📁 Failų struktūra

```
carousel/
├── fetch_products.py          # produktų parsisiuntimas (WooCommerce → JSON + nuotraukos)
├── serve.py                   # vietinis serveris (be priklausomybių)
├── config.example.json        # visi nustatymai su paaiškinimais
├── player/
│   ├── index.html             # ekrano karkasas
│   ├── style.css              # dizainas (Hortense Blue #142b6f + Lemon Chrome #ffd602)
│   ├── app.js                 # rotacija, akcijų logika, atsparumas triktims
│   └── qr.js                  # QR kodų generatorius (be interneto)
├── tools/
│   └── build_standalone.py    # vienas HTML failas su viskuo viduje
├── systemd/                   # automatinis paleidimas ir atnaujinimas
├── kiosk/                     # Chromium kiosko paleidimas
└── data/                      # parsisiųsti duomenys (į git nekeliama)
```

---

## ✅ Ko reikia

| | |
|---|---|
| **Būtina** | `python3` (3.8+) ir bet kokia naršyklė |
| **Nebūtina** | `unclutter`, `curl` (kioske) |
| **Nereikia** | interneto ryšio nuolat, VPS, duomenų bazės, API raktų, `pip`, `npm` |
