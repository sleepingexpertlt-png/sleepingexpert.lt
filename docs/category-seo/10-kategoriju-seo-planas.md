# Kategorijų SEO planas + Hermès integracija (2026-08-25)

Tikslas: pakelti pozicijas pagal TOP raktažodžius, kategorijas ir nišą.
Strategija: pradedam nuo užklausų, kur GSC rodo 5–15 poziciją (Google jau
beveik pasitiki — mažiausia pastangų/didžiausia grąža zona). Dabartinis
atskaitos taškas: GSC avg position 8.2, ~1674 imp / 43 clicks per parą.

## Architektūra — kaip jungiasi į Hermès (orchestratoriaus žemėlapis)

```
GSC (jau traukiama kasdien)
  └► seo_opportunities lentelė (shared_state.db) — NAUJA
       keyword · page · category · position · impressions · clicks ·
       action_type (content|onpage|links) · status (new|queued|done)
            │
            ├► action=content  → BLOG PIPELINE: keyword'ai į esamą blog
            │    agent'o eilę (frontier.db) — NEkeičiant pipeline logikos,
            │    tik papildant šaltinį; QA lieka esamas (q≥90, be draudžiamų claims)
            ├► action=onpage   → OWNER/WP užduočių sąrašas (title, H1, aprašymas,
            │    FAQ blokai kategorijų puslapiuose per WP REST)
            ├► action=links    → vidinių nuorodų planas (blog → kategorija)
            │
            ├► RADAR: savaitinis „SEO opportunities" signalas (top movers,
            │    nauji patekimai į 5–15 zoną)
            └► MATAVIMAS: pirmadienio cron 07:15 — pozicijų delta sekamiems
                 keyword'ams → Telegram suvestinė (kartu su Local bloku)
```

Orchestratoriui (hermes_master_run) atsiranda vienas standartinis goal'as:
„apdorok seo_opportunities: status=new → priskirk action_type → content tipo
įmesk į blog eilę → onpage tipo įtrauk į owner ataskaitą".

## Darbo pasidalinimas

- **VPS agentas:** duomenų ištraukimas, lentelė, pipeline sujungimas, cron
  (promptas: `VPS-PROMPT-category-seo.md`).
- **Šita sesija (aš):** gavus top-30 užklausų sąrašą — strateginis kategorijų
  planas: prioritetai, turinio briefai klasteriams, on-page rekomendacijos
  kiekvienai kategorijai, kanibalizacijos patikra.
- **Owner:** WP kategorijų puslapių pakeitimų tvirtinimas.

## Sėkmės kriterijai (60 d., kartu su Local ciklu)

- GSC avg position sekamiems non-brand keyword'ams: 8.2 → ≤6.
- Non-brand clicks/parą: +50 % nuo baseline (43 → ~65).
- Bent 5 užklausos perėjusios iš 5–15 zonos į top 3.
