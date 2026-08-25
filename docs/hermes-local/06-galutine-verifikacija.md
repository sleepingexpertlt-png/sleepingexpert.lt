# Galutinė verifikacija — visi 6 žingsniai baigti (2026-08-25)

| # | Reikalavimas | Įrodymas |
|---|---|---|
| 1 | gmb_agent bug patikra | ✅ bug'o nebuvo; live API patvirtino UKM 13 dir/424 imp |
| 2 | Geo-grid MCP | ✅ @cablate/mcp-google-map@0.0.55 + --stdio, raktas, kvota 2000/d |
| 3 | Baseline | ✅ data/local_visibility_baseline_2026-08-25.json (3 lokacijos) |
| 4 | Review agent | ✅ post_reply pašalintas iš kodo; getReviews grąžina realius atsiliepimus visoms 3 lokacijoms |
| 5 | Storage + cron | ✅ local_visibility 3 eilutės; crontab: pirmadieniais 07:00 |
| 6 | Verifikacija a–d | ✅ visi 4 punktai išoriniais įrodymais |

## Papildomas laimėjimas — upstream bug fix

`gbp-review-agent/src/services/googleAuth.ts`: `getAuthenticatedClient()` darė
lokalų `expires_at` patikrinimą PRIEŠ API kvietimą, tad pasibaigus access_token
visi kvietimai lūžo, nors refresh_token buvo geras (googleapis auto-refresh
negaudavo progos). Pataisyta + patvirtinta realiu kvietimu. VERTA: pasiūlyti
kaip PR į satheeshds/gbp-review-agent — ir bendruomenei, ir kad mūsų fork'as
nenutoltų nuo upstream.

## Atviri punktai (ne blokeriai)

1. 🔐 GOOGLE_CLIENT_SECRET rotacija — **ATIDĖTA owner sprendimu (2026-08-25)**
   iki pilno rezultato. Rizikos įvertis: vien secret be refresh tokeno GBP
   prieigos neduoda; liekamoji rizika — OAuth phishing prisidengiant app'u.
   PERŽIŪRA: kartu su 60 d. ciklo rezultatais (≈2026-10-24) arba anksčiau,
   jei pastebimas įtartinas OAuth aktyvumas GCP audit loguose.
2. 🔐 Maps API raktas guli plaintext crontab'e IR buvo transkriptuose —
   kompensuojama GCP apribojimais (Places-only + VPS IP). PATIKRINTI, kad
   apribojimai uždėti ant TEISINGO rakto (paskutinių 4 simbolių sutapimas su
   /root/.mcp.json; „Speed" raktas — ne tas). Ilgesniu horizontu: perkelti raktą
   į config/local_visibility.env (chmod 600) ir crontab eilutę palikti be jo.
3. Q&A rankinis (API miręs) — SOP vėliau.

## 60 d. matavimo ciklas — STARTAS 2026-08-25

- KPI: directions + WC orders per parduotuvę (grid ARP/SoLV — tik diagnostika).
- Sėkmė: per 60 d. bent 2/3 parduotuvių directions +30 % ARBA aiškus trendas.
- Vertės darbai (nebe infrastruktūra!):
  1. Ukmergė — profilio KONVERSIJOS auditas (nuotraukos, aprašymas, darbo laikas);
     rikiavimas jau #1, problema — imp→dir santykis.
  2. Vilnius — rikiavimo atstatymas: P-064 kategorijos LT, atsiliepimų srautas,
     postų reguliarumas; konkurentų (Lonas ×2, Miego Centras) gap analizė iš
     grid duomenų.
  3. Klaipėda — neliesti, veikia.
