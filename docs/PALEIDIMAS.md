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

## 4 žingsnis. Slaptažodžiai — nieko nereikia įrašyti į komandas

Skriptas **pats paklaus** pašto slaptažodžio ir HubSpot rakto, kai bus paleistas.
Įvedant ekrane nieko nesimato — tai normalu, tiesiog įveskite ir spauskite Enter.

Slaptažodžio ir rakto **niekur nerašykite**: nei į komandų eilutę, nei į Claude pokalbį,
nei į VPS Claude sesiją. Viskas, kas įrašoma į pokalbį, lieka jo istorijoje.

Jei skriptą leisite kelis kartus ir nenorite kaskart vesti, galima įrašyti į failus,
kuriuos gali skaityti tik root (komandos paklaus reikšmės, ekrane nesimatys):

```bash
mkdir -p ~/.se-pastas && chmod 700 ~/.se-pastas
read -rs -p "Pašto slaptažodis: " P; printf '%s' "$P" > ~/.se-pastas/imap_password; unset P; echo
read -rs -p "HubSpot token: " T; printf '%s' "$T" > ~/.se-pastas/hubspot_token; unset T; echo
chmod 600 ~/.se-pastas/*
```

Kai baigsite darbą, failus galima ištrinti: `rm -rf ~/.se-pastas`.

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

## Trumpiausias kelias: 2 komandos terminale, likusį darbą daro VPS Claude

Jei nenorite patys leisti skripto, terminale reikia padaryti tik du dalykus — prisijungti ir
įrašyti pašto slaptažodį į failą, kurį gali skaityti tik root. Po to viską paleidžia Claude,
kuris jau veikia VPS'e, o slaptažodžio jis niekada nemato.

**1. PowerShell / Komandinė eilutė (jūsų kompiuteryje):**

```
ssh root@72.61.139.213
```

Kai eilutė pasikeis į `root@...:~#`, esate VPS'e.

**2. Įklijuoti (paklaus pašto slaptažodžio, rašant nesimatys):**

```
mkdir -p ~/.se-pastas && chmod 700 ~/.se-pastas && read -rs -p "info@sleepingexpert.lt slaptazodis: " P && printf '%s' "$P" > ~/.se-pastas/imap_password && unset P && chmod 600 ~/.se-pastas/imap_password && echo && echo OK
```

Turi išvesti `OK`. Tiek terminale ir viskas.

**3. Paleisti VPS Claude** (`claude`) ir jam nusiųsti šį tekstą:

> Pašto slaptažodis jau yra faile `~/.se-pastas/imap_password` (root-only, 0600) — jo neskaityk ir nerodyk,
> skriptas pats jį nuskaito. Šioje žinutėje jokių slaptažodžių nėra.
> Padaryk: `cd /root && rm -rf se-pastas && git clone -b claude/hubspot-email-integration-tkvjca https://github.com/sleepingexpertlt-png/sleepingexpert.lt.git se-pastas && cd se-pastas`
> Tada `python3 scripts/hubspot_imap_backfill.py --list-folders` ir
> `python3 scripts/hubspot_imap_backfill.py --folder INBOX --since 2024-01-01` bei tą patį su `--folder INBOX.Sent`.
> HubSpot token'o nėra — kai paklaus, spausk Enter (dry run veikia be jo). Nieko į HubSpot nerašyk (be `--apply`).
> Parodyk ekrano suvestinę ir `hubspot_backfill_contacts.csv` pirmas 40 eilučių.

Jei VPS Claude paklaus slaptažodžio — jis neteisingai suprato; slaptažodis jau faile, jam jo nereikia.
Jei skriptas neinteraktyvioje aplinkoje neranda failo, jis aiškiai pasakys `Trūksta imap_password`.

---

## Jei kas nors neveikia

| Klaida | Ką daryti |
|---|---|
| `AUTHENTICATIONFAILED` | Neteisingas pašto slaptažodis. Pasitikrinti prisijungiant per mail.hostinger.com; jei naudojate failą — `rm ~/.se-pastas/imap_password` ir paleisti iš naujo |
| `Nepavyko atidaryti aplanko` | Netikslus aplanko pavadinimas — paleisti `--list-folders` |
| `HubSpot ... 401` | Neteisingas arba pasibaigęs raktas — pasidaryti naują (1 žingsnis); jei naudojate failą — `rm ~/.se-pastas/hubspot_token` |
| `HubSpot ... 403` | Rakte trūksta scope — pridėti trūkstamą (1 žingsnis, 3 punktas) |
| `Trūksta imap_password ...` | Skriptas paleistas ne interaktyviame terminale — paleisti tiesiogiai SSH lange arba įrašyti į failą (4 žingsnis) |
| `command not found: python3` | Naudoti `/root/frontier-agent/venv/bin/python3` vietoje `python3` |

Nukopijuokite klaidos tekstą ir atsiųskite man — pasakysiu, kas negerai.
