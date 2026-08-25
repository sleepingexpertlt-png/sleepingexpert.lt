# VPS Deploy Prompt — Kategorijų SEO (copy-paste į VPS Claude sesiją)

```
Jungi kategorijų SEO sluoksnį prie Hermès. Žingsniai eilės tvarka, po kiekvieno
patikrink. Jokių WP/GBP rašymo veiksmų be mano patvirtinimo.

KONTEKSTAS:
- GSC duomenys jau traukiami (traits_business_fetcher.py, cron 06:30) — reuse
  tą pačią autentifikaciją, nekurk naujos.
- Blog pipeline veikia (blog_agent.py, quality gate q>=90) — jo logikos NEKEISTI.
- Brand voice: be draudžiamų teiginių (premium, exclusive, Italijos dizaineriai).

ŽINGSNIS 1 — Ištraukimas:
Iš GSC API paimk 90 d. užklausas su: avg position 4.5–15, impressions >= 50,
be brand užklausų (išfiltruok: sleeping expert, sleepingexpert ir variantus).
Kiekvienai: keyword, geriausias landing page, position, impressions, clicks.
Išsaugok data/seo_opportunities_2026-08-25.json.

ŽINGSNIS 2 — Kategorizavimas:
Priskirk kiekvienai užklausai category pagal landing page path:
/produkto-kategorija/<X>/ → X; /parduotuve/... → product; kita → blog.
Ir action_type: jei landing = kategorijos puslapis → onpage;
jei landing = blog įrašas arba tinkamo puslapio nėra → content;
jei puslapis geras, bet pozicija 8–15 → links (vidinės nuorodos).

ŽINGSNIS 3 — Lentelė:
shared_state.db sukurk seo_opportunities(keyword PK, page, category, position,
impressions, clicks, action_type, status DEFAULT 'new', added_at, last_position,
last_checked). Supilk žingsnio 1–2 duomenis.

ŽINGSNIS 4 — Jungtis į blog pipeline (TIK eilė, ne logika):
Išsiaiškink, iš kur blog_agent.py ima keyword'us (frontier.db / config eilė).
Top 10 action_type='content' užklausų įrašyk į tą eilę su žyma
source='seo_opportunities', status='queued'. NEPUBLIKUOK nieko pats — pipeline
su savo QA padarys savo darbą įprasta tvarka.

ŽINGSNIS 5 — Savaitinis matavimas:
Naujas scripts/seo_opportunities_weekly.py (pagal local_visibility_weekly.py
šabloną): pirmadieniais 07:15 atnaujina last_position visiems sekamiems
keyword'ams iš GSC (7 d. langas), Telegram žinutėje (toje pačioje pirmadienio
suvestinėje) prideda bloką: top 3 pagerėjimai, top 3 kritimai, kiek užklausų
top3 zonoje. Cron eilutė BE jokių raktų (GSC auth — per esamą mechanizmą).

ŽINGSNIS 6 — Verifikacija (išoriniai įrodymai):
(a) JSON failas su >=20 užklausų, (b) SELECT COUNT(*) iš seo_opportunities,
(c) blog eilėje matosi 10 įrašų su source='seo_opportunities',
(d) crontab -l rodo 07:15 eilutę, (e) rankinis seo_opportunities_weekly.py
paleidimas praeina be klaidų. Parodyk visus 5.

PABAIGOJE: grąžink man top-30 užklausų lentelę (keyword, category, position,
impressions, action_type) — ją perduosim strateginiam planui.
```

Gavus top-30 lentelę → grąžinti į claude.ai/code sesiją: ten daromas
kategorijų prioritetų planas, turinio briefai ir on-page rekomendacijos.
