# Llamamaps modulis — distiliuotas į instrumentą

Šaltiniai: `docs/hermes-local/01-mvp-planas.md` (architektūra),
`docs/hermes-local/07-gbp-reitingo-svertai.md` (svertų tyrimas),
`docs/hermes-local/02-open-source-irankiai.md` (komponentai).

Distiliavimas = ne santrauka. Iš trijų dokumentų paimta tai, kas gali būti
paleista kaip kodas, ir išmesta viskas, kas tik aprašo.

## Distiliato branduolys (viena pastraipa)

Llamamaps parduoda „top 3 per 90 d.". Realiai reitingas dalijasi taip:
**proximity ~55 % (nevaldoma), GBP signalai ~32 % (valdoma), likę ~13 %
atsiliepimai / citatos / elgsena.** Vadinasi visa jų „garantija" yra
aritmetika ant 32 % — profilio užpildymas iki galo ir laikymas šviežio.
Tai nėra paslaptis, tai disciplina. **Distiliatas: paversti tuos 32 %
savaitiniu ciklu, kuris matuoja spragą ir grąžina vieną veiksmą.**

## Instrumentas: 5 tikrinimai × 3 lokacijos, savaitinis ciklas

Kiekvienas tikrinimas grąžina `(reikšmė, spraga, vienas veiksmas)`.
Balas 0–100 lokacijai. Be balo nėra prioriteto.

| # | Tikrinimas | Ką matuoja | Kodėl | Kas taiso |
|---|---|---|---|---|
| **L1** | Pagrindinė kategorija | ar primary = „Čiužinių parduotuvė" visose 3 | stipriausias VIENAS valdomas signalas | owner (GBP UI) |
| **L2** | Profilio pilnumas | produktai, paslaugos, atributai, aprašas, paslaugų sritis, Q&A — kiek laukų tuščių | 32 % svorio branduolys; tuščias laukas = atiduotas taškas | owner + agentas ruošia turinį |
| **L3** | Atsiliepimų tempas | atsiliepimų/sav. slenkantis vidurkis; **stabilus > šuolis** | tempas svarbesnis už bendrą skaičių | QR prie kasų + pardavėjų SOP |
| **L4** | Šviežumas | postai/mėn. + REALIOS nuotraukos/mėn. | šviežumo signalas gęsta per ~30 d. | Content Agent + mėn. foto SOP |
| **L5** | NAP nuoseklumas | telefonas / adresas / pavadinimas identiški GBP, svetainėje, kataloguose | nesutapimas skaido signalą | Citation Agent |

**Balo formulė (fiksuota, nediskutuojama kas kartą):**
`L1 = 40 tšk. (dvejetainis: 40 arba 0) · L2 = 25 · L3 = 15 · L4 = 12 · L5 = 8`

L1 sveria daugiausia, nes tyrimas rodo jį stipriausiu vienu signalu, ir jis
dvejetainis — arba teisinga kategorija, arba ne.

## Ką ciklas grąžina

Vieną eilutę lokacijai: `Vilnius 73/100 — silpniausia L2 (produktai 0)`.
Ir vieną veiksmą — silpniausio tikrinimo. Ne sąrašą. Vieną.

## Juoda zona — instrumentas privalo atsisakyti

Šie veiksmai NIEKADA nesiūlomi, net jei balas kristų:
fake atsiliepimai · review gating · raktažodžiai pavadinime · CTR
imitacija botais · EXIF geotagging (2026 m. duomenimis kenkia) · masinės
šlamšto citatos. Instrumentas, pasiūlęs bet kurį iš šių — brokas.

Vienintelė leistina „agresija": jei Vilniaus konkurentai kemša raktažodžius
į pavadinimą, „Suggest an edit" report'as yra legalus.

## Kas iš to jau veikia, kas ne

| Sluoksnis | Būklė |
|---|---|
| GBP API tiesioginė integracija (`gmb_agent.py`) | ✅ veikia |
| Review draftai + QA gate | ✅ veikia |
| GBP postai | ✅ automatizuota |
| L1 kategorija | ✅ Vilnius sutvarkytas 08-27 |
| L2 produktai | 🔴 **0 produktų visuose 3 profiliuose** |
| L2 paslaugų sritis | 🔴 Vilniuje lenkiškai („Litwa/Łotwa/Estonia") |
| L3 atsiliepimų tempo sistema | 🔴 nėra (QR neįdiegtas) |
| L4 nuotraukų SOP | 🔴 rankinis, nereguliarus |
| L5 NAP | 🟡 dalinis; telefono formatas GBP ≠ svetainė |
| Geo-grid | 🟡 įrankis parinktas, nepaleistas |

**Silpniausia grandis šiandien = L2 produktai.** Trys profiliai, nulis
produktų — didžiausia viena spraga 32 % svorio bloke.
