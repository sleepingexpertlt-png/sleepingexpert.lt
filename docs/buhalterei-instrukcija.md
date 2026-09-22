# Instrukcija buhalterei: kaip užsakyti registrą ir Finvaldos XML

Claude Code sesija atidaroma per claude.ai/code arba per esamą sesijos nuorodą, kurią duoda savininkas. Repozitorija: `sleepingexpertlt-png/sleepingexpert.lt`.

## Ką prisegti

1. PDF su WooCommerce sąskaitomis už laikotarpį (WooCommerce → Užsakymai → pasirinkti → „PDF Invoice“ eksportas, vienas failas).
2. CSV užsakymų eksportas už tą patį laikotarpį (WooCommerce → Užsakymai → Export).

## Ką parašyti (nukopijuoti ir įklijuoti)

```
/saskaitos
Laikotarpis: 2026 m. rugsėjis.
Prisegu PDF sąskaitas ir WC užsakymų CSV.
Reikia: 1) pardavimų registro (XLSX + Google Sheets, esamo registro formatu),
2) Finvaldos importo XML, 3) trūkstamų gamintojo ID ir nesutapimų su CSV sąrašo.
Eilutės kodas Finvaldoje: PAJAMOS. Alinos refaktūrai PVM kodas: PVM21.
```

Jei kažkas kitaip (kitas kodas, kitas PVM kodas, tik registras be XML), pakeiskite paskutinę eilutę.

## Ką gausite

- XLSX failą ir Google Sheets nuorodą (tame pačiame Drive aplanke, kur esami registrai).
- `pardavimai_OSL_<nuo>-<iki>_<mėnuo>.xml` importui į Finvaldą (Įrankiai → Duomenų importas → XML importas).
- Ataskaitą: sąskaitų skaičius, sumos, kurioms sąskaitoms trūksta gamintojo ID, kur sumos nesutampa su WC.

## Ko Claude nedarys

- Neišrašys naujų sąskaitų ir nekurs numerių.
- Nekeis esamų Google Sheets lentelių, tik kurs naujas (esamų redagavimas rankomis).
