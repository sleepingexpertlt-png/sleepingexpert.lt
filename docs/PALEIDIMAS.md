# Kaip paleisti pašto peržiūrą (žingsnis po žingsnio)

Tikslas: perskaityti info@sleepingexpert.lt pašto istoriją ir gauti lentelę —
kas rašė, kiek kartų, ar jau yra HubSpot'e ir ką su tuo daryti.

**Šis paleidimas nieko nekeičia** — nei pašte, nei HubSpot'e. Tik perskaito ir sukuria du CSV failus.

---

## 1 žingsnis. Pasidaryti HubSpot raktą (naršyklėje, ~2 min.)

1. Atidaryti https://app-eu1.hubspot.com/private-apps/148451001
2. **Create private app** → pavadinimas: `Pasto perkelimas`
3. Skirtukas **Scopes** → **Add new scope** → pažymėti:
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
   - `sales-email-read`
4. **Create app** → **Continue creating** → **Show token** → **Copy**

Raktas atrodo taip: `pat-eu1-xxxxxxxx-xxxx-...`

> Rakto niekam nesiųskite ir nerašykite pokalbyje. Jis įvedamas tik VPS terminale.

---

## 2 žingsnis. Prisijungti prie VPS

Windows: atidaryti **PowerShell** (Start → įrašyti „PowerShell“) ir įvesti:

```bash
ssh root@72.61.139.213
```

---

## 3 žingsnis. Parsisiųsti skriptą

Įklijuoti į terminalą visą bloką iš karto:

```bash
cd /root
rm -rf se-pastas
git clone -b claude/hubspot-email-integration-tkvjca \
  https://github.com/sleepingexpertlt-png/sleepingexpert.lt.git se-pastas
cd se-pastas
```

---

## 4 žingsnis. Įvesti prisijungimus

Pakeisti `SLAPTAZODIS` ir `pat-eu1-...` savo reikšmėmis:

```bash
export IMAP_USER='info@sleepingexpert.lt'
export IMAP_PASSWORD='SLAPTAZODIS'
export HUBSPOT_TOKEN='pat-eu1-...'
```

`IMAP_PASSWORD` — tas pats Hostinger pašto slaptažodis, kurį įvedėte HubSpot lange.

---

## 5 žingsnis. Pasitikrinti aplankų pavadinimus

```bash
python3 scripts/hubspot_imap_backfill.py --list-folders
```

Turi išvesti sąrašą: `INBOX`, `INBOX.Sent`, `INBOX.Drafts` ir pan.
Jei „Sent“ vadinasi kitaip, tą pavadinimą naudokite 6 žingsnyje.

---

## 6 žingsnis. Peržiūra (nieko nekeičia)

```bash
python3 scripts/hubspot_imap_backfill.py --folder INBOX --since 2024-01-01
python3 scripts/hubspot_imap_backfill.py --folder INBOX.Sent --since 2024-01-01
```

Ekrane pamatysite suvestinę, pvz.:

```
Pašnekovai (312 unikalūs adresai):
  IGNORUOTI              141
  ESAMAS KLIENTAS         78
  PERŽIŪRĖTI              54
  PARTNERIS/TIEKĖJAS      31
  NAUJAS LEAD              8
```

---

## 7 žingsnis. Parsisiųsti lentelę

Sukurti failai: `hubspot_backfill_contacts.csv` (rūšiavimo lentelė) ir
`hubspot_backfill_report.csv` (kiekvienas laiškas atskirai).

Peržiūrėti vietoje:

```bash
column -s, -t hubspot_backfill_contacts.csv | head -40
```

Arba parsisiųsti į kompiuterį — **naujame** PowerShell lange (ne tame, kur prisijungę prie VPS):

```bash
scp root@72.61.139.213:/root/se-pastas/hubspot_backfill_contacts.csv .
```

Failas nukris į `C:\Users\<jūsų vardas>\`. Atsiųskite jį man — kartu nuspręsime,
kuriuos adresus kelti į HubSpot kaip lead'us.

---

## 8 žingsnis. Kėlimas į HubSpot (tik po peržiūros)

Atlikti **tik** kai bus peržiūrėta lentelė:

```bash
python3 scripts/hubspot_imap_backfill.py --folder INBOX --since 2024-01-01 --apply
python3 scripts/hubspot_imap_backfill.py --folder INBOX.Sent --since 2024-01-01 --apply
```

Kelia laiškus tik tiems, kurie **jau yra** HubSpot'e. Naujų kontaktų nekuria.
Norint kurti ir naujus — pridėti `--create-contacts`, bet tik susiaurinus laikotarpį
(pvz. `--since 2025-09-01`), kad nepasikartotų 2026-05 importas, kai į CRM pateko
384 adresai, iš kurių 37 buvo robotai.

Skriptą galima leisti pakartotinai — tie patys laiškai antrą kartą nekeliami.

---

## Jei kas nors neveikia

| Klaida | Ką daryti |
|---|---|
| `AUTHENTICATIONFAILED` | Neteisingas pašto slaptažodis. Pasitikrinti prisijungiant per mail.hostinger.com |
| `Nepavyko atidaryti aplanko` | Netikslus aplanko pavadinimas — paleisti `--list-folders` |
| `HubSpot ... 401` | Neteisingas arba pasibaigęs raktas — pasidaryti naują (1 žingsnis) |
| `HubSpot ... 403` | Rakte trūksta scope — pridėti trūkstamą (1 žingsnis, 3 punktas) |
| `command not found: python3` | Naudoti `/root/frontier-agent/venv/bin/python3` vietoje `python3` |

Nukopijuokite klaidos tekstą ir atsiųskite man — pasakysiu, kas negerai.
