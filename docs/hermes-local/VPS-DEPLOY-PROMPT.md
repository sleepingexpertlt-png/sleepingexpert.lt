# VPS Deploy Prompt — Hermès Local

Copy-paste žemiau esantį promptą į Claude Code sesiją VPS'e (ten, kur veikia Hermès).
Prieš paleidžiant turėti: Google Maps API raktą (Places API New įjungtas, kvota apribota).

---

```
Diegi „Hermès Local" modulį šiame serveryje. Daryk žingsnius eilės tvarka,
po kiekvieno patikrink, ir nieko nepublikuok į GBP be mano patvirtinimo.

KONTEKSTAS (faktai, netikrinti iš naujo):
- GBP API jau veikia per src/agents/gmb_agent.py (OAuth ok, 3 lokacijos:
  Vilnius, Klaipėda, Ukmergė; location ID žr. reference_gmb_posts_api.md).
- Ukmergės GBP dublikatas JAU ištrintas (PROMISES R-026). Ukmergė dabar rodo
  0 directions/7d prie ~420 impressions — įtariamas bug'as, ne realybė.
- KPI pagal G2 sprendimą (R-028): directions + WC orders. Calls NĖRA KPI.
- Brand voice: be draudžiamų teiginių (premium, exclusive, Italijos dizaineriai).

ŽINGSNIS 1 — Bug patikra (pirmiausia):
Patikrink src/agents/gmb_agent.py: iš kurio location ID skaitomos Ukmergės
directions. Jei naudojamas senas/ištrintas ID (5771168054047785891) — pataisyk
į aktyvųjį (2791954715091405702), paleisk fetch iš naujo ir parodyk man diff'ą
prieš commit'ą.

ŽINGSNIS 2 — Geo-grid MCP:
Į MCP konfigą pridėk:
{
  "google-map": {
    "command": "npx",
    "args": ["-y", "@cablate/mcp-google-map"],
    "env": {
      "GOOGLE_MAPS_API_KEY": "<RAKTAS>",
      "GOOGLE_MAPS_ENABLED_TOOLS": "maps_local_rank_tracker,maps_search_places,maps_place_details"
    }
  }
}
Auditas atliktas ant commit be966cc — jei npx traukia naujesnę versiją, pin'ink
@cablate/mcp-google-map@0.0.55.

ŽINGSNIS 3 — Baseline skenai:
maps_search_places → placeId visoms 3 lokacijoms. Tada maps_local_rank_tracker:
- Vilnius: keywords ["čiužiniai","čiužinių parduotuvė"], grid 5, spacing 1000
- Klaipėda: tie patys keywords, grid 5, spacing 1000
- Ukmergė: ["čiužiniai"], grid 3, spacing 500
Rezultatus (JSON + ARP/SoLV suvestinę) išsaugok data/local_visibility_baseline_<data>.json.

ŽINGSNIS 4 — Review agentas (TIK juodraščiai):
git clone https://github.com/satheeshds/gbp-review-agent (audituotas commit
a940309 — checkout būtent jį), npm install && npm run build. Env: reuse esamo GCP
projekto GOOGLE_CLIENT_ID/SECRET, redirect http://localhost:3000/auth/callback,
vienkartinis npm run auth. .tokens.json → chmod 600, ne git'e. MCP konfige
įjunk TIK listLocations, getReviews, generateReply. postReply NEjungti.

ŽINGSNIS 5 — Storage + cron:
shared_state.db pridėk lentelę local_visibility(date, store, impressions,
directions, wc_orders, grid_arp, ai_sov). Cron: pirmadieniais 07:00 —
geo-grid skenas + GBP insights + įrašas į lentelę; jei directions krito >30%
sav/sav — Telegram alert.

ŽINGSNIS 6 — Verifikacija (auditor principu, išoriniai įrodymai):
(a) baseline JSON failas egzistuoja ir turi visų 3 lokacijų grid'us,
(b) getReviews grąžina realius atsiliepimus bent 1 lokacijai,
(c) local_visibility turi >=3 eilutes su šiandienos data,
(d) cron įrašytas (crontab -l). Parodyk visų 4 įrodymus.

GUARDRAILS: jokių GBP write veiksmų be patvirtinimo; Places kvotą apribok
GCP konsolėje iki 2000/d; nekeisti gbp_post_publisher.py ir blog pipeline.
```
