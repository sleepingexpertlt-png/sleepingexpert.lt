# Deploy statusas (VPS sesijos raportas, 2026-08-25)

| Žingsnis | Statusas | Įrodymas |
|---|---|---|
| 1. gmb_agent bug patikra | ✅ Bug'o NĖRA | Live API: UKM 13 dir / 424 imp (7d), teisingas location ID. „0" buvo pasenęs snapshot |
| 2. Geo-grid MCP | ⏸ BLOKUOTA | Nėra GOOGLE_MAPS_API_KEY (owner pridės vėliau); pin @0.0.55 patvirtintas |
| 3. Baseline skenai | ⏸ | Laukia 2 žingsnio |
| 4. Review agent | 🟡 90 % | Klonuota @a940309, build ok, .env chmod 600; **postReply IŠIMTAS iš kodo** (ne tik deny) + deny rule settings.json. Liko: OAuth consent |
| 5. Storage | ✅ | `local_visibility` lentelė sukurta shared_state.db |
| 6. Verifikacija | 1/4 | (d) laukia cron, kuris rašomas tik po 2 žingsnio |

## Atviri veiksmai (eilės tvarka)

1. **Owner:** GCP Console → OAuth client (GMB_CLIENT_ID) → Authorized redirect
   URIs → pridėti `http://localhost:3000/auth/callback` → VPS sesijoje tęsti
   `npm run auth` per SSH tunelį (vykdoma dabar).
2. **Owner (po auth):** 🔐 ROTUOTI GOOGLE_CLIENT_SECRET — jis buvo atsitiktinai
   atspausdintas VPS transkripte (file-change notification). GCP → Credentials →
   reset secret; tada atnaujinti secrets.env IR /root/gbp-review-agent/.env,
   perkrauti MCP. Refresh tokenai lieka galioti, bet keitimams naudojamas naujas secret.
3. **Owner (kada patogu):** Google Maps API raktas (Places API New, kvota 2000/d)
   → VPS žingsniai 2-3 + cron + pilna 6 žingsnio verifikacija.
4. **Patikra kitą pirmadienį:** salon_signal UKM turi rodyti ~13 dir, ne 0 —
   jei 0, bug'as snapshot rašytuve (dashboard/cache kelias), ne GBP.

## Saugumo sprendimai, priimti VPS sesijoje (patvirtinti gerais)

- postReply pašalintas iš MCP serverio kodo (ne tik permission deny) — teisinga,
  nes standalone serveris pasiekiamas ir be Claude gate.
- Atsisakyta gmb_token.json refresh-token copy-shortcut'o — teisinga: tas tokenas
  read+write, jo perkėlimas būtų apėjęs „be write veiksmų" taisyklę.
