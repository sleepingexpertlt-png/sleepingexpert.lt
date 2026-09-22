# Sąskaitų registro taisyklės

Savininko nurodymai (2026-09-22). Galioja visiems registrams, generuojamiems iš WooCommerce OSL sąskaitų.

## Privalomi stulpeliai

| Stulpelis | Šaltinis | Pastaba |
|---|---|---|
| Sąskaitos Nr. | PDF „Sąskaita Numeris“ (OSL000XXX) | WC meta `_wcpdf_invoice_number` |
| **Sąskaitos (dokumento) data** | PDF „Sąskaita Data“ | Išrašymo data. NE užsakymo data. |
| Užsakymo Nr. | PDF „Užsakymo numeris“ / CSV `Order Number` | WooCommerce ID |
| **Užsakymo data** | PDF „Užsakymo data“ / CSV `Order Date` | Atskiras stulpelis nuo sąskaitos datos. |
| **Gamintojo užsakymo ID** | PDF „Pastaba“ laukas | Visada 5 skaitmenys. Formos: `ID 52990`, `52943`, `ID53124`, `UKM 00615/53124` (imti skaičių po `/`). |
| Pirkėjas | PDF pirkėjo blokas | Juridiniam asmeniui: pavadinimas + įm. kodas + PVM kodas |
| Vieta | PDF „Vieta:“ | Vilnius / Klaipėda / Ukmergė / e-shop |
| Mokėjimo būdas | PDF „Mokėjimo būdas:“ arba „Mokėjimo metodas“ | |
| Suma be PVM, PVM, Suma su PVM | PDF „Viso“ + „įskaičiuota PVM“ | 21 % LT; 0 % ES atvirkštinis (PVM21) |
| Avansas / Likusi suma | PDF „Sumokėtas avansas“, „Likusi suma“ | |

## Griežtos taisyklės

1. Užsakymo data ir sąskaitos data yra skirtingi dalykai. Abu stulpeliai privalomi.
2. Gamintojo ID (5 skaitmenų) iš pastabų privalomas kiekvienoje eilutėje. Jei jo nėra, eilutė žymima „TRŪKSTA ID“, o ne paliekama tuščia be įspėjimo.
3. Sąskaitų numeriai imami tik iš šaltinio (PDF arba WC meta). Numerių fabrikuoti negalima.
4. Apskaitos programa: Finvalda. Importas per XML (`PVM1` = 21 %, kategorija `PAJAMOS`).

## Šaltiniai VPS

- Kanoninis rankinis registras: Google Sheets `SASKAITU_REGISTRAS_2026`.
- Hermes skill'ai: `invoice`, `perdavimo-aktas`.
