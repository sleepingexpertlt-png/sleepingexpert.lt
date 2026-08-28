# GeoLook — sprendimas 2026-08-28: NEĮTRAUKIAM

Įrankis: https://github.com/aigclink/geolook (patikrinta, egzistuoja).
Modelis: 4 sluoksniai — Access → Orientation → Understanding → Quotability.

## Sprendimas

**Įrankio neimam. Paimam dvi idėjas į esamą pipeline'ą.**

## Kodėl ne

**Antra vertinimo sistema — pagrindinė priežastis.** Turim WQS v2.0,
`site_scorer.py`, `auditor.py`, `ai-visibility`. Įdėjus GeoLook, tas pats
puslapis turėtų du balus, kurie nesutaps. Tada nepasitikima nei vienu.
Tai organizacinė kaina, ne techninė.

**Kitos priežastys:**

| | |
|---|---|
| Niekas jo nepaleido | sprendimas dėl to, kas neišbandyta |
| „86 % auto-verifiable" | jų pavyzdinio projekto skaičius, ne mūsų prognozė |
| MIT „lengva pasiimti gabalus" | MIT reikalauja licencijos teksto; gabalai = amžinai palaikoma šaka |
| Python 3.9 įrašytas kaip pliusas | tai apribojimas; VPS Python versija netikrinta |
| Laikas | AI srautas 172 sesijos/28 d. — net padvigubintas neduotų +12 maršrutų iki 10-24 |

## Ką paimam — ir tai NE GEO funkcijos

Abi yra proceso taisymai, reikalingi nepriklausomai nuo GeoLook.

**1. Mašininiu būdu tikrinama „done" sąlyga.**
Taisyklė K10 („nepatikrintas done nėra done") yra, bet rankinė.
2026-08-28 du kartus turėjom „padaryta", kuris nebuvo:
lokacijų puslapiai (autosave neatkurtas) ir GMC sync'as (mirė ties
289/642, atrodė baigtas). Automatinis patikrinimas K10 padarytų
neapeinamą.

**Forma:** kiekviena užduotis turi `acceptance` lauką su komanda,
kuri grąžina 0/1. Užduotis neuždaroma, kol komanda negrąžina 1.

**2. Fabrikacijos patikra prieš publikavimą.**
Jau atsitiko: 129 įrašai su prasimanytais teiginiais, 8 su owner'io
vardu netikruose sertifikatuose (U-023, U-024). Valymas kainavo realų
darbą.

**Forma:** prieš publikavimą tikrinti teiginius, kurių nėra šaltiniuose —
skaičius, datas, sertifikatus, asmenvardžius, veiklos trukmę.
Radus — blokuoti, ne žymėti.

## Peržiūra

Po 2026-10-24. Jei tada norėsim grįžti — pirmas žingsnis vienas ir pigus:
paleisti GeoLook ant **vieno** mūsų puslapio ir palyginti jo balą su WQS.
Sutampa — nieko naujo. Skiriasi — bus apie ką kalbėti.
