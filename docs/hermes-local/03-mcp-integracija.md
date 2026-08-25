# Open-source MCP skeleton'ų integracija į Hermès (2026-08-25)

Abu repo klonuoti ir peržiūrėti. Verdiktas: **abu saugūs naudoti**, jokių trečiųjų
šalių endpoint'ų ar telemetrijos — tik `*.googleapis.com`.

## 1. Geo-grid: `@cablate/mcp-google-map`

- Audituotas commit: `be966cc` (v0.0.55, 2026-08-16). Node >=18, MIT tipo naudojimas per npm.
- **Saugumas ✅:** visi 18 tools read-only; API raktas tik iš env `GOOGLE_MAPS_API_KEY`;
  užklausos keliauja tik į maps/places/routes/weather/airquality.googleapis.com.
- **Pagrindinis mums įrankis:** `maps_local_rank_tracker` — Local Falcon analogas:
  placeId + centro koordinatė + grid (3×3…7×7) + žingsnis 100–10000 m, iki 3 keywords,
  grąžina rank kiekviename taške, top-3 konkurentus ir ARP/ATRP/SoLV suvestinę.
- **Diegimas (Hermès serveryje):**
  ```jsonc
  // .mcp.json / MCP klientas
  {
    "google-map": {
      "command": "npx",
      "args": ["-y", "@cablate/mcp-google-map"],
      "env": {
        "GOOGLE_MAPS_API_KEY": "<raktas iš esamo GCP projekto>",
        "GOOGLE_MAPS_ENABLED_TOOLS": "maps_local_rank_tracker,maps_search_places,maps_place_details"
      }
    }
  }
  ```
  `GOOGLE_MAPS_ENABLED_TOOLS` allowlist — įjungiam tik 3 reikalingus tools.
- **Kaštų kontrolė:** vienas 5×5 skenas × 2 keywords = 50 Places užklausų.
  Savaitinis ciklas 3 parduotuvėms × 2 keywords ≈ 300 užklausų/sav. — smulku, bet
  GCP projekte būtina užsidėti Places API kvotos limitą (pvz., 2000/d.), kad
  agentas negalėtų netyčia išdeginti biudžeto.
- **Prerequisite:** GCP projekte įjungti Places API (New) ir sukurti atskirą,
  tik Places/Geocoding apribotą API raktą (ne bendrą).

## 2. Atsiliepimai: `satheeshds/gbp-review-agent`

- Audituotas commit: `a940309` (2025-12-03). MIT licencija.
- **Saugumas ✅ su dviem pastabom:**
  - Endpoint'ai tik `mybusiness.googleapis.com/v4` + Google OAuth
    (scope `business.manage` — tas pats, kurį jau naudojam postams).
  - LLM atsakymai generuojami per **MCP sampling** — jokio atskiro OpenAI/kt.
    rakto, tekstą generuoja mūsų pačių MCP klientas (Hermès). Labai gerai.
  - ⚠️ OAuth tokenai saugomi plaintext `.tokens.json` projekto kataloge —
    diegiant: `chmod 600`, katalogas ne repo viduje, backup'uose neįtraukti.
  - ⚠️ `postReply` yra WRITE veiksmas — pirmam etapui įjungti tik
    `getReviews` + `generateReply` (juodraščiai), o `postReply` leisti tik per
    Hermès QA gate (žmogus patvirtina), kaip ir GBP postams.
- **Tools:** listLocations, getReviews, getReviewDayStats, generateReply, postReply.
- **Diegimas:** reuse esamo GCP projekto (GBP API access jau patvirtintas — postai
  veikia). Env: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`,
  `GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback`; vienkartinis
  `npm run auth` OAuth flow. Yra `ENABLE_MOCK_MODE=true` — pirmus testus daryti
  mock režimu be realių API kvietimų.

## 3. Pirmo paleidimo testas (kai įdiegta Hermès serveryje)

1. `maps_search_places("Sleeping Expert Vilnius")` → gauti placeId visoms 3 lokacijoms.
2. `maps_local_rank_tracker`: keyword „čiužiniai", Vilniaus centras (Kalvarijų 125),
   grid 5×5, žingsnis 1000 m → užfiksuoti baseline heatmap į `docs/hermes-local/`.
3. Pakartoti Klaipėdai (5×5) ir Ukmergei (3×3, žingsnis 500 m).
4. gbp-review-agent mock režimu: `getReviews` + `generateReply` → patikrinti
   juodraščių toną pagal brand voice (be draudžiamų teiginių).
5. Įjungti savaitinį cron: pirmadieniais geo-grid skenas + atsiliepimų suvestinė.

## Kas lieka nepadengta šių dviejų skeleton'ų

- GBP postai — jau turim savo (`gbp_post_publisher.py`), nieko nekeičiam.
- AI share-of-voice — `ai-visibility` skill (atskiras žingsnis).
- Nuotraukų kėlimas, Q&A — rankinis (SOP), API nepalaiko arba miręs.
