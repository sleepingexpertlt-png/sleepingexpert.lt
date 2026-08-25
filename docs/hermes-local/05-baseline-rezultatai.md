# Geo-grid baseline (2026-08-25, VPS sesija)

Pirmas skenas per mcp-google-map (Places API, kvota 2000/d nustatyta).
ARP = vidutinė pozicija tinklelyje; SoLV = % taškų, kur patenkama į top 3.
Duomenys: data/local_visibility_baseline_2026-08-25.json + shared_state.db:local_visibility (3 eilutės).

| Parduotuvė | „čiužiniai" ARP | SoLV | „čiužinių parduotuvė" ARP | SoLV |
|---|---|---|---|---|
| Vilnius (5×5, 1000 m) | 9.0 | **0 %** | 6.8 | **0 %** |
| Klaipėda (5×5, 1000 m) | 2.9 | 68 % | 2.5 | 96 % |
| Ukmergė (3×3, 500 m) | **1.0** | **100 %** | — | — |

## Interpretacija

- **Ukmergė: rikiavimas idealus (#1 visuose 9 taškuose).** Žemas directions/impressions
  santykis (13/424) yra KONVERSIJOS problema (profilio nuotraukos, aprašymas, darbo
  laikas), ne SEO. Veiksmas: profilio turinio auditas, ne pozicijų kėlimas.
- **Klaipėda: stipri** (top 3 beveik visur pagal „čiužinių parduotuvė") — sutampa su
  geriausia impressions→directions konversija (4.2 %). Palaikymas, ne remontas.
- **Vilnius: 0 % SoLV abiem frazėms — dominuoja Lonas (2 lokacijos) ir Miego Centras.**
  Tai vienintelė tikra „ranking" problema. Pirmi svertai: P-064 (kategorijos LT),
  profilio pilnumas, atsiliepimų srautas, postų reguliarumas Vilniaus profilyje.
- Metodikos pastaba: Places API ≈ aproksimacija realaus Maps UI; naudoti trendui
  (savaitė prieš savaitę), ne absoliučiai tiesai.

## Deploy būklė po šio etapo

Step 1 ✅ · Step 2 ✅ (raktas + kvota 2000/d) · Step 3 ✅ (baseline) ·
Step 4 ✅ (be post_reply; OAuth done) · Step 5 🟡 (lentelė ✅, cron daromas) ·
Step 6 🟡 (a ✅ b ✅ c ✅, liko d — cron įrašas).

⚠️ NEUŽMIRŠTI: GOOGLE_CLIENT_SECRET rotacija (nutekėjo į VPS transkriptą) —
GCP → Credentials → reset → atnaujinti secrets.env ir /root/gbp-review-agent/.env.
Papildomai: Maps API raktas taip pat matėsi transkripte — apriboti raktą GCP
konsolėje (API restrictions: tik Places; application restrictions: server IP)
arba pergeneruoti.
