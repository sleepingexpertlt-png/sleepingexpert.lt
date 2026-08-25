# Kategorijų SEO planas — SUVIENODINTA su kokybes-auditas sistema (2026-08-25 v2)

Kontekstas gautas iš GEO/audito sesijos (trigger 2026-08-25). Šis planas
NEBEKURIA lygiagrečios sistemos — jungiasi į esamą.

## Kas jau egzistuoja (nekurti iš naujo)

- `question_bank_master.json` — 5 889 klausimai (topic_bank 3738, WP FAQ 1845,
  GSC 167, Elmo 111, RankMath 44)
- Savaitinis matavimas: `aeo_monitor.py` (58 queries) + `ai_visibility_agent.py`
  (21 kw) per Perplexity/ChatGPT/Gemini + Google AIO (DataForSEO)
- Baseline citavimas: AIO 62 %, Perplexity 30 %, Gemini 26 %, ChatGPT 0/105
  (turinio spraga, ne blokas)
- Rekomendacijų variklis: kokybes-auditas `tools/recommend.py` — klasės
  RAŠYTI / TAISYTI / KANALAS / STIPRINTI; sprendimai VYKDYMAS.md, kaštai BIUDZETAS.md
- Nepriklausomas auditorius: se-auditor (Actions, 06:30 UTC)

## Mano GSC 5–15 darbo vieta šioje sistemoje

**GSC 5–15 pozicija = TAISYTI klasė:** turinys egzistuoja ir rikiuojasi,
trūksta citabilumo (Trumpai: blokas, palyginimo lentelė, DUK + FAQPage schema).

Jungtis:
1. GSC ištraukimas (90 d., pos 4.5–15, imp ≥ 50, non-brand) — kaip planuota.
2. Output NE į naują failą/lentelę, o į `question_bank_master.json` formatą:
   `{text, source:["gsc_5_15"], gsc_impressions, gsc_position, landing_page,
   ar_jau_matuojamas}` — merge su dedup pagal text.
3. Klasifikacija — per `recommend.py`: dauguma 5–15 kris į TAISYTI;
   be landing page → RAŠYTI.
4. Vykdymas — per VYKDYMAS.md procesą: pasiūlymas su kaina → owner GO →
   tik tada draft'ai. JOKIO auto-publikavimo (viskas draft, publikuoja owner).
5. Matavimas — esamas savaitinis ciklas (aeo_monitor + GSC). NAUJŲ cron'ų
   ir matavimo paleidimų NEDAROMA be owner GO (kaštų taisyklė: ≤1 €/parą,
   1×/sav. cron, tas pats klausimas tam pačiam provideriui maks 1×/parą).

## Pirmas patvirtintas taikinys (owner GO jau duotas)

„koks geriausias čiužinys lietuvoje" — #4 organikoje, AIO cituoja
comfi/miegoimperija/gintarobaldai vietoj mūsų. Citabilumo pataisa DRAFT režimu.

## Geležinės taisyklės (galioja visam šiam darbui)

- Blog: TIK draft, publikuoja owner.
- Business faktai (kainos, pristatymas, garantija) — TIK iš owner.
- Draudžiami: premium, exclusive, Italijos dizaineriai, geriausi pasaulyje.

## 90 d. tikslas, į kurį tai lenda

Žinoti, kiek € atneša kiekvienas kanalas, ir įrodyti bent vieną grandinę
veiksmas → citavimas → srautas → užsakymas (iki 2026-11-24).
Salonas ~€961 AOV / ~€29.7k per 30 d.; online ~€135/d.
