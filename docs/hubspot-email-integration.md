# HubSpot + el. pašto integracija — auditas ir tvarkymosi planas

Data: 2026-09-03. Portalas: HubSpot EU1, account ID 148451001, vartotojas info@sleepingexpert.lt.
Tikslas: prieš pradedant dirbti su HubSpot, susitvarkyti visą praeitį (CRM duomenis ir el. pašto istoriją)
ir prijungti darbinį paštą info@sleepingexpert.lt.

## 1. Kas jau yra HubSpot (faktinė būklė 2026-09-03)

| Objektas | Kiekis | Šaltinis | Pastaba |
|---|---|---|---|
| Kontaktai | 1016 | 1014 „Hermes CRM Sync“ (integracija), 2 HubSpot pavyzdiniai | 632 = `customer` (turi užsakymų), 384 = `lead` (importuoti iš Gmail adresų knygos, be užsakymų) |
| Įmonės | 234 | auto-sukurtos iš el. pašto domenų 2026-05-10 | 65 be pavadinimo; daug tiekėjų/SaaS domenų (anthropic, odoo, temu, wordfence…) |
| Sandoriai (deals) | 753 | „Hermes CRM Sync“ iš WooCommerce | 737 sukurti 2026-05-10 (pradinis importas), po to tik 16 per 3,5 mėn. |
| El. laiškai (engagements) | 2 | HubSpot pavyzdiniai (lenkiški) | **Paštas prie HubSpot NEprijungtas** — jokių realių laiškų |
| Bilietai (tickets) | 0 | — | — |
| Savininkai (owners) | 1 | Sleeping Expert (92125541) | Komandų nėra |

Paskyros nustatymai: laiko juosta **US/Eastern**, valiuta **USD**, onboarding **nepradėtas**.
Atnaujinimai 2026-09-03 (264 kontaktai, 22 sandoriai) įvykdyti per API po 10 įrašų, 0 klaidų, patikrinta atsitiktine imtimi.
Visi sandoriai be `deal_currency_code`, todėl 660 331 (realiai EUR) rodomi kaip USD.

### 1.1 Sandorių etapai (WooCommerce statusas → HubSpot stage)

| WC statusas | HubSpot etapas | Kiekis |
|---|---|---|
| completed | Closed Won | 610 |
| deposit-paid | Closed Won | 17 |
| processing | Contract Sent | 79 |
| store-review | Appointment Scheduled | 13 |
| pending | Appointment Scheduled | 2 |
| on-hold | Decision Maker Bought-In | 1 |
| cancelled / refunded | Closed Lost | 31 |

Problemos:
1. Naudojamas numatytasis „Sales Pipeline“ su bendrais etapais (Contract Sent, Appointment Scheduled), kurie
   nieko nereiškia e-parduotuvės užsakymui. Reikia atskiro „Užsakymai (WooCommerce)“ pipeline'o su etapais:
   Naujas → Apmokėtas / Avansas → Gamyboje / Peržiūra salone → Pristatyta (Won) → Atšauktas (Lost).
2. Sync'as etapų **neatnaujina**: 79 „processing“ užsakymai nuo 2024–2025 m. HubSpot'e vis dar „Contract Sent“,
   nors WooCommerce jie seniai completed. Reikia, kad Hermes sync'as atnaujintų `dealstage` pasikeitus statusui.
3. 22 sandoriai be kliento vardo pavadinime („#12028 —  (2025-12-31)“).
4. Nuo 2026-05-11 sukurta tik 16 sandorių (gegužę 5, birželį 6, liepą 1, rugpjūtį 9), o 2025–2026 pradžioje
   buvo 40–57 užsakymai per mėnesį. Arba web užsakymai krito, arba sync'as praleidžia dalį užsakymų — patikrinti
   WooCommerce užsakymų skaičių už birželį–rugpjūtį.
5. Vienas sandoris „GCR Test“ (#21141) — testinis, trinti.

### 1.2 Kontaktai

632 klientai (su užsakymais): el. paštas 100 %, telefonas 92 %, miestas 83 % — geros kokybės, neliečiami.

384 „lead“ kontaktai buvo importuoti iš Gmail adresų knygos (visi su `hs_lead_status = NEW`). Suskirstymas:

| Grupė | Kiekis | Padaryta 2026-09-03 | Ką daryti toliau |
|---|---|---|---|
| Sisteminiai / noreply / tiekėjų palaikymo adresai (support@, invoice@, temu, anthropic, dpd, omniva…) | 37 | Lifecycle Stage → **Other**, Lead Status → **Unqualified** | Ištrinti HubSpot lange (sąrašas `docs/hubspot-cleanup/contacts_to_delete.csv`) |
| Verslo domenai (tiekėjai, partneriai, PC administracija, bankai, kurjeriai, agentūros) | 227 | Lifecycle Stage → **Other** | Palikti kaip partnerių sąrašą; neįtraukti į marketingo laiškus (`contacts_partners_review.csv`) |
| Privatūs asmenys be užsakymo (gmail / yahoo / hotmail) | 120 | Nekeista (lieka Lead / New) | Peržiūrėti rankiniu būdu (`contacts_private_no_order_review.csv`): dalis — realios užklausos, dalis — atsitiktiniai |

Kaip HubSpot lange ištrinti 37 sisteminius: Contacts → All contacts → Filter → Lead status = Unqualified
→ pažymėti visus → Actions → Delete. (Trynimas per MCP negalimas.)

### 1.3 Įmonės

234 įmonės sukurtos automatiškai iš importuotų kontaktų domenų. `docs/hubspot-cleanup/companies_to_delete.csv`
— 125 įmonės, kurias siūloma trinti: SaaS / naujienlaiškių / atsitiktiniai domenai (anthropic, odoo, wordfence,
rankmath, yithemes, temu, fastspring, qr.io, smartsupp, mercell…) ir 65 įmonės be pavadinimo („--“).
Pasilikti tik realius tiekėjus ir partnerius (Hilding, Alina Group, Baldų Rojus, Helios, Omniva, DPD, Venipak,
Luminor, ESTO, Finvalda, aspa.lt ir pan.).

Kaip trinti HubSpot lange: Companies → Filter → Company name is unknown (65 vnt.) → pažymėti → Delete;
likusias iš CSV — per Search pagal domeną arba importuojant CSV su `hs_object_id` stulpeliu ir pasirenkant
„Delete“ veiksmą (Import → Delete records).

Rekomendacija: Settings → Objects → Companies → išjungti „Automatically create and associate companies with
contacts“, kad kiekvienas naujas gmail.com pirkėjas nekurtų tuščių įmonių.

### 1.4 Sandoriai — padaryta 2026-09-03

22 sandoriai be kliento vardo pervadinti: 4 pagal susieto kontakto vardą (Promo Group, UAB ×2; Pavel Kanusevič;
Valdas Skėrys), 18 — pagal el. pašto adresą (pvz. „#10145 — info@marsalas.lt (2025-01-17)“).

## 2. Pašto dėžutės

| Dėžutė | Kur hostinama | Prijungta prie Claude | Prijungta prie HubSpot |
|---|---|---|---|
| info@sleepingexpert.lt (darbinis, WooCommerce siuntėjas, HubSpot vartotojas) | **Hostinger Email** (autodiscover/autoconfig → mail.hostinger.com), naudojama per Outlook programą | Ne | Ne — reikia prijungti |
| sleepingexpertlt@gmail.com (Google paskyra reklamos įrankiams) | Gmail | Taip | Ne — **nejungiame** (sprendimas 2026-09-03: ten tik Google Ads / Merchant / SaaS triukšmas) |

### 2.1 Kaip prijungti info@sleepingexpert.lt prie HubSpot (Hostinger = IMAP)

1. HubSpot → ⚙ Settings → General → **Email** → **Connect personal email**.
   Tiesioginė nuoroda: https://app-eu1.hubspot.com/settings/148451001/user-preferences/email
2. Pasirinkti **Other** (ne Gmail, ne Office 365) → įvesti info@sleepingexpert.lt ir Hostinger pašto slaptažodį.
3. Jei HubSpot automatiškai neatpažįsta serverių, įvesti rankiniu būdu:
   - IMAP: `imap.hostinger.com`, portas **993**, SSL/TLS
   - SMTP: `smtp.hostinger.com`, portas **465**, SSL/TLS
   - Prisijungimo vardas — pilnas adresas info@sleepingexpert.lt
4. Įjungti **Turn on inbox automation** (Log + Track), kad gaunami ir siunčiami laiškai automatiškai kristų prie kontaktų.
5. Settings → General → Email → **Log and Track** → „Never log“ pridėti: `google.com`, `googlemail.com`,
   `linkedin.com`, `hubspot.com`, `anthropic.com`, `microsoft.com`, `ivesk.lt`, `every-pay.com`,
   `worldline-solutions.com`, `invoice123.com`, `paddle.com`, `fastspring.com` — kad į CRM nekristų sąskaitos
   ir sisteminiai pranešimai.
6. Patikra: iš Outlook išsiųsti vieną laišką bet kuriam esamam klientui iš HubSpot; po 1–2 min. jis turi
   atsirasti kontakto kortelėje (Activities → Emails).

Svarbu: HubSpot prijungus dėžutę **istorijos neimportuoja** — logina tik naujus laiškus. Praeitis — 3 skyriuje.

### 2.2 Paskyros nustatymai, kuriuos reikia pakeisti UI (MCP negali)

- Settings → Account Defaults → Time zone: **Europe/Vilnius** (dabar US/Eastern).
- Settings → Account Defaults → Company currency: **EUR** (dabar USD; visi 660 tūkst. sandorių sumų yra eurai).
- Settings → Account Defaults → Language: lietuvių (dalis savybių lenkiškos: „Preferowane kanały“).
- Settings → Objects → Deals → Pipelines: sukurti „Užsakymai (WooCommerce)“ pipeline'ą su etapais
  Naujas → Apmokėtas / Avansas → Gamyboje / Peržiūra salone → Pristatyta (Won) → Atšauktas (Lost),
  ir perjungti Hermes CRM Sync, kad naudotų jį bei **atnaujintų** etapą pasikeitus WooCommerce statusui.
- Onboarding tikslas per MCP jau nustatytas: „Organize and track contacts“.

## 3. Praeities laiškų (info@) perkėlimas į HubSpot

Skriptas `scripts/hubspot_imap_backfill.py` (tik standartinė Python 3 biblioteka) paima laiškus iš Hostinger
per IMAP ir sukuria HubSpot „Email“ veiklas prie atitinkamų kontaktų. Idempotentiškas (pagal Message-ID),
numatytas režimas — dry run, sisteminiai/noreply laiškai ir ignoruojami domenai praleidžiami.

Reikalavimai:
- HubSpot **Private App** token: Settings → Integrations → Private Apps → Create → scopes
  `crm.objects.contacts.read`, `crm.objects.contacts.write`, `sales-email-read` (ir `crm.objects.contacts.write`
  reikalingas tik su `--create-contacts`). Token prasideda `pat-eu1-…`.
- Paleisti iš kompiuterio arba Hermes VPS (Claude sandbox'as neturi prieigos prie api.hubapi.com ir IMAP).

```bash
export IMAP_USER='info@sleepingexpert.lt'
export IMAP_PASSWORD='***'
export HUBSPOT_TOKEN='pat-eu1-***'

python3 scripts/hubspot_imap_backfill.py --list-folders                     # aplankų pavadinimai
python3 scripts/hubspot_imap_backfill.py --folder INBOX --since 2024-06-01   # dry run, ataskaita CSV
python3 scripts/hubspot_imap_backfill.py --folder INBOX.Sent --since 2024-06-01
python3 scripts/hubspot_imap_backfill.py --folder INBOX --since 2024-06-01 --apply
python3 scripts/hubspot_imap_backfill.py --folder INBOX.Sent --since 2024-06-01 --apply
```

Dry run sukuria `hubspot_backfill_report.csv` su stulpeliu `action` (would-log / skip:noise /
skip:no-contact-in-hubspot / already-logged) — pirmiausia peržiūrėti jį, tik tada leisti su `--apply`.
Laiškai kontaktams, kurių HubSpot'e nėra, praleidžiami (kad nekurtų naujų šiukšlių); jei norima kurti —
`--create-contacts`.

Alternatyva be skripto: iš Outlook persiųsti pasirinktus senus laiškus į HubSpot „Forward to CRM“ adresą
(Settings → General → Email → Forwarding address) — kiekvienas persiųstas laiškas prisikabina prie kontakto
pagal originalų siuntėją.

## 4. Kas liko padaryti rankiniu būdu (checklist)

- [ ] Prijungti info@sleepingexpert.lt prie HubSpot (2.1)
- [ ] Time zone → Europe/Vilnius, valiuta → EUR (2.2)
- [ ] Ištrinti 37 sisteminius kontaktus (filtras Lead status = Unqualified)
- [ ] Ištrinti 2 HubSpot pavyzdinius kontaktus („Maria Johnson (Sample Contact)“, „Brian Halligan (Sample Contact)“) ir 2 pavyzdinius laiškus
- [ ] Ištrinti 125 įmones iš `docs/hubspot-cleanup/companies_to_delete.csv`
- [ ] Peržiūrėti 120 privačių asmenų be užsakymų (`contacts_private_no_order_review.csv`)
- [ ] Sukurti WooCommerce pipeline'ą ir pataisyti Hermes CRM Sync etapų atnaujinimą; patikrinti, kodėl nuo
      2026-05 sync'as sukūrė tik 16 sandorių
- [ ] Paleisti `hubspot_imap_backfill.py` (dry run → apply) senai info@ istorijai
