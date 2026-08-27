# Statuso auditas 2026-08-27, 21:38 (gyvi duomenys)

Owner: „patikrink statusą, atlik auditą — atrodo gyveni ne čia ir dabar."
Teisingai. Šis auditas — tik iš gyvų tool call'ų, be atminties.

## Kas gyva ir veikia

| Rodiklis | Reikšmė | |
|---|---|---|
| Servisai aktyvūs | 15 | ✅ |
| Metacog agentai | 26 | ✅ |
| Circuit breakers open | 0 | ✅ |
| Avg outcome 24h | 0.95 | ✅ |
| Blog šiandien | **published = 1** | ✅ realiai publikuota |

Pipeline'as ne tik gamina — šiandien publikavo. Po vakarykščio Gemini
gedimo tai reali atstata, ne bandymas.

## RADINYS 1: North Star skaičius 14 valandų senumo

`salon_signal.last_updated = 07:20`. Auditas daromas 21:38.
Skaičius, kurį visą dieną cituoju (32 maršrutai), išmatuotas ryte.

Ir dar blogiau — **bazė 34 buvo išmatuota 08-26, o 32 išmatuota 08-27 ryte.**
Tai 7 dienų slenkantis langas, tikrinamas kartą per parą, skirtingu paros
metu. **−2 tokioje imtyje yra triukšmas, ne kritimas.**

Visą dieną owner'iui kartojau „judam ne ta kryptimi, −6 %". Tai nebuvo
įrodyta. Tai buvo dviejų nesulygintų matavimų atimtis.

**Ką reikia:** fiksuotas matavimo laikas kas parą + bent 7 dienų eilutė
prieš darant išvadą apie trendą. Iki tol jokių „krentam" teiginių.

## RADINYS 2: calls_7d = 0 visuose trijuose salonuose

| Salonas | Maršrutai | Skambučiai | Impresijos |
|---|---|---|---|
| Klaipėda | 13 | **0** | 192 |
| Ukmergė | 13 | **0** | 260 |
| Vilnius | 6 | **0** | 329 |

Trys parduotuvės, septynios dienos, nulis skambučių iš GBP. `hermes_status`
dokumentacija pati sako: „warn if calls=0 (potential GBP setup gap)".
Bet `alert = false`. **Įspėjimas neveikia** — logika neatitinka savo pačios
specifikacijos.

Arba skambučių sekimas neveikia, arba GBP telefono numeris nesusietas taip,
kad Google jį skaičiuotų. Vilniuje telefonas įvestas formatu „(0-630) 70001" —
nestandartinis. Tai kandidatas į priežastį, bet neįrodyta.

## RADINYS 3: pažadų registras meluoja

`hermes_promises` rodo **U-009 „Vilnius GBP kategorijos lietuviškai"** kaip
atvirą, užblokuotą owner'io. Owner'io atsiųstas profilis įrodo, kad
pagrindinė kategorija = „Čiužinių parduotuvė". **Padaryta.**

Ir tai ne vienintelis: U-015, U-016, U-018, U-019, U-022, U-023, U-024
guli `user_blocked` sąraše su **„✅ RESOLVED" savo pačių tekste**.
Statistika sako 19 užblokuotų — realiai jų mažiau.

**Tai ir yra priežastis, kodėl visą dieną varinėjau owner'į taisyti to,
kas jau ištaisyta.** Ne mano atmintis buvo pasenusi — pasenęs yra šaltinis,
iš kurio ją traukiu.

## Ką tai keičia prioritetuose

1. **Sutvarkyti pažadų registrą** — kol jis meluoja, kiekvienas prioritetų
   sąrašas bus klaidingas. Tai ne biurokratija, tai duomenų šaltinis.
2. **Fiksuotas matavimo laikas** maršrutams + 7 dienų eilutė prieš išvadas.
3. **Ištirti calls = 0** — jei sekimas neveikia, mes nematom pusės piltuvo.
4. Tik tada — kanibalizacijos auditas ir WC atributai.

## Ko NEBUVO padaryta šiandien (be gražinimo)

Gyvo, viešai matomo rezultato šiandien: **3 lokacijų puslapiai + 1 blogo
įrašas + 1 pašalintas viešas markeris.** Visa kita — dokumentai ir auditai.

Maršrutai nepajudėjo. Ir dabar žinau, kad net teiginys „nukrito" buvo
neįrodytas.
