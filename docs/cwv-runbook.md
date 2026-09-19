# Core Web Vitals runbook — sleepingexpert.lt

Skirta GSC ataskaitai *Core Web Vitals → mobilusis → problema* (nuoroda su `sharing_key` atidaroma tik
naršyklėje; API jai nėra). Tas pats duomenų šaltinis (CrUX, 28 d. p75) pasiekiamas per PageSpeed
Insights API – `scripts/cwv/cwv_check.py`.

## 1. Ką jau žinome (Hermès atmintis, 2026-06-07 statusas ir lessons)

| Rodiklis | Vertė | Puslapis | Šaltinis |
|---|---|---|---|
| Lighthouse perf (mobile) | 50–60 / 100 | visa svetainė | project_sites_status_2026-06-07 |
| LCP p75 (mobile) | 7,8 s („volatilus“) | pradinis | project_sites_status_2026-06-07 |
| CLS (mobile) | 0,32 🔴 | /produkto-kategorija/ciuziniai/ | project_sites_status_2026-06-07 |
| TBT | 500 ms → 80 ms ✅ | GA4 `setTimeout` pašalintas | lessons L33–L34 |
| Infrastruktūra | Hostinger + LiteSpeed Cache; nuo 2026-08-05 Cloudflare Free (proxied, WooCommerce bypass cache rule) | | Letta 2026-08-05 |

CLS priežastis užfiksuota: **vaizdai ir filtrai be rezervuotos vietos** kategorijų puslapiuose.
Įgyvendinta nebuvo – laukė owner sprendimo („dėl perf/CLS klausti“). LCP po GA4 pataisos toliau
nematuotas.

Google slenksčiai (p75): LCP ≤ 2,5 s · INP ≤ 200 ms · CLS ≤ 0,10. 0,32 CLS yra „Poor“ (> 0,25).

## 2. Kaip išmatuoti dabar (iš VPS, 2 min.)

```bash
cd /root/sleepingexpert.lt && git pull
python3 scripts/cwv/cwv_check.py                 # mobile: pradinis, 3 kategorijos, blogas, parduotuvės
python3 scripts/cwv/cwv_check.py --strategy desktop
cat build/cwv/cwv_$(date +%F)_mobile.md
```

Skriptas parodo CrUX p75 (tai, ką rodo GSC), Lighthouse LCP elementą ir CLS šaltinius (selektoriai).
Su `GOOGLE_API_KEY` (Google Cloud → PageSpeed Insights API + Chrome UX Report API) `--crux-history`
duoda 25 sav. tendenciją – matysis, ar problema sena, ar prasidėjo po Cloudflare (08-05) ar po
429 incidento (09-08).

## 3. Taisymas pagal rodiklį

### CLS 0,32 kategorijų puslapiuose (labiausiai tikėtina ataskaitos problema)

Priežastis: produktų kortelių vaizdai ir filtrų blokas neturi rezervuotos vietos, todėl įsikrovę
nustumia turinį.

1. **Vaizdų matmenys.** WooCommerce kortelėse `<img>` turi turėti `width`/`height` (WP juos deda, jei
   vaizdo metaduomenys yra). Patikrinti: `Media → Regenerate thumbnails` (Regenerate Thumbnails
   plugin) po temos/miniatiūrų dydžio keitimo. CSS apsauga temos *Additional CSS*:
   ```css
   .woocommerce ul.products li.product img{aspect-ratio:1/1;width:100%;height:auto}
   ```
   (santykį parinkti pagal realų miniatiūros dydį – `woocommerce_thumbnail` nustatymuose).
2. **LiteSpeed lazyload.** LiteSpeed Cache → Page Optimization → Media: *Lazy Load Images* ON,
   **Responsive Placeholder ON** (rezervuoja vietą), *LQIP* nebūtina. *Lazy Load Iframes* ON.
   Viewport Images (VPI) ON – pirmi matomi vaizdai be lazyload.
3. **Filtrų blokas.** Jei filtrai (kainos slankiklis, atributai) kraunami JS, rezervuoti aukštį:
   `.widget_layered_nav, .price_slider_wrapper{min-height:48px}`. Jei tai Ajax filtrai – tikrinti,
   ar jie neperpiešia viso sąrašo su kitokiu aukščiu.
4. **Šriftai.** `font-display: swap` be `size-adjust` sukelia teksto šuolį. LiteSpeed → CSS →
   *Font Display: Swap* + Google Fonts *Localize* arba preload pagrindinio šrifto.
5. **Banneriai / cookie juosta / GMB badge** turi būti `position: fixed` arba su rezervuota vieta,
   ne įterpiami virš turinio.

Kiekvieną žingsnį tikrinti Lighthouse „Avoid large layout shifts“ sąraše – `cwv_check.py` jį spausdina
kaip *CLS šaltinis*.

### LCP 7,8 s pradiniame (mobile)

1. Nustatyti LCP elementą (`cwv_check.py` → *LCP elementas*). Beveik visada – hero/slider vaizdas.
2. Hero vaizdas: ≤ 200 KB, WebP (LiteSpeed → Image Optimization → *WebP replacement*), be lazyload
   (VPI arba `data-no-lazy`), `fetchpriority="high"`, `<link rel="preload" as="image">` – LiteSpeed
   neturi UI, dedama per temos header hook arba WPCode snippet.
3. Slider'is: jei tai Elementor/Slider Revolution – pirmas slide be animacijos, likę lazy. Dažniausias
   laimėjimas – pakeisti slider'į statiniu hero.
4. Render-blocking CSS/JS: LiteSpeed → CSS Minify + *Load CSS Asynchronously* (atsargiai, tikrinti
   CLS), *Generate Critical CSS* ON; JS *Deferred* (ne *Delayed*, kad nesugadintų WC). Guest Mode +
   Guest Optimization ON.
5. TTFB: Cloudflare proxied + LiteSpeed page cache. Patikrinti `cf-cache-status` ir
   `x-litespeed-cache: hit` antraštes pradiniame kaip anoniminiam lankytojui. Jei `miss` – cache
   nevyksta (cookie, per trumpas TTL, WC bypass taisyklė per plati).

### INP > 200 ms

Dažniausiai – trečiųjų šalių skriptai (Meta Pixel, Klaviyo, GTM) ir WC Ajax krepšelio įvykiai.
Jei `cwv_check.py` rodo INP ⚠️/🔴: LiteSpeed JS *Delayed* tik trečiųjų šalių skriptams (Delay
JS exclude sąraše palikti WC ir temos JS), GA4/Pixel įkelti po pirmos sąveikos (kaip L34).

## 4. Po pataisų

- LiteSpeed → Toolbox → *Purge All*; Cloudflare → Caching → *Purge Everything*.
- Per 2–3 d. `cwv_check.py` Lighthouse turi rodyti pagerėjimą; CrUX p75 (ir GSC) atsinaujina per 28 d.
- GSC ataskaitoje spausti *Validate fix* tik kai Lighthouse CLS < 0,1 keliose kategorijose.

## 5. Ko iš Claude Code web sesijos padaryti negalima

sleepingexpert.lt, search.google.com ir PageSpeed API (anoniminė kvota išnaudota) iš šios aplinkos
nepasiekiami; WP Admin / LiteSpeed nustatymai keičiami tik per UI (App Password neturi `nonce`).
Todėl: matavimas – iš VPS, nustatymų keitimas – owner per WP Admin, CSS – per temos Additional CSS.
