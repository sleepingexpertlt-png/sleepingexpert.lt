# Pirkėjų geografijos auditas — 2026-09-18

Šaltinis: Hermès `hermes_business_metrics`, `revenue_30d_salon_store_miestas_*`,
matuota 2026-09-05. Salono pardavimai, 30 dienų, 29 užsakymai, 21 910,97 €.

## Kas perka brangiausiai

| Miestas | Apyvarta | Užsak. | **Vid. čekis** | % apyvartos |
|---|---|---|---|---|
| **Avižieniai** | 3 864,41 € | 1 | **3 864 €** | 17,6 % |
| **Vilnius** | 7 130,75 € | 8 | **891 €** | 32,5 % |
| Inowrocław (PL) | 1 638,70 € | 2 | 819 € | 7,5 % |
| Klaipėda | 6 505,30 € | 9 | 723 € | 29,7 % |
| **Ukmergė** | 2 518,31 € | 6 | **420 €** | 11,5 % |
| Kaunas | 115,50 € | 1 | 116 € | 0,5 % |
| be miesto | 85,00 € | 1 | 85 € | 0,4 % |
| Mažeikiai | 53,00 € | 1 | 53 € | 0,2 % |
| **Viso** | **21 910,97 €** | **29** | **756 €** | |

## Trys faktai

**1. Vilniaus regionas duoda pusę apyvartos iš trečdalio užsakymų.**
Vilnius + Avižieniai: 10 995 € iš 9 užsakymų. Tai 50 % salonų apyvartos
iš 31 % užsakymų. Vidutinis čekis ten **1 222 €**, kai bendras vidurkis 756 €.

**2. Avižieniai — vienas užsakymas už 3 864 €.**
Tai 17,6 % visos mėnesio salonų apyvartos iš vieno kliento. Avižieniai yra
naujas pasiturintis Vilniaus rajono priemiestis.
⚠️ **n = 1.** Vienas užsakymas nėra dėsnis. Bet tai didžiausias vieno kliento
čekis per mėnesį ir jis atėjo ne iš miesto centro.

**3. Ukmergė perka 9,2 karto pigiau nei Avižieniai.**
Vidutinis čekis 420 € prieš 3 864 €. Ukmergė duoda 11,5 % apyvartos iš 21 %
užsakymų — daugiausiai darbo už mažiausiai pinigų.

## Kaip tai susieja su reklama

2026-09-14 reklamos auditas parodė, kad Ukmergė buvo prasčiausia ir reklamoje:
30,95 € už maršrutą, kai Vilniaus PMax duoda po 2,30 €. Dabar matome, kad ir
atėjęs Ukmergės klientas palieka 9 kartus mažiau.

**Abi metrikos rodo tą pačią kryptį. Tai ne atsitiktinumas.**

## Ką tai reiškia taikymui

Dabartinė Vilniaus vietos reklama (2,32 €/d) išbarstyta po visą miestą vienodai.
Duomenys sako, kad taip neturi būti.

Prioritetinės zonos pagal čekio dydį:
1. **Avižieniai ir Vilniaus šiaurės vakarų priemiesčiai** (Avižieniai, Pilaitė,
   Bajorai, Santariškės, Verkiai) — nauji namai, didžiausi čekiai
2. **Vilniaus miestas** — 891 € vidutinis čekis
3. Klaipėda — 723 €
4. Ukmergė — 420 €, mažiausias prioritetas

## Ko trūksta, kad auditas būtų tvirtas

- **n per mažas.** 29 užsakymai per 30 d. Avižieniai n=1, Kaunas n=1,
  Mažeikiai n=1. Reikia 90 d. pjūvio, kad išvados būtų patikimos.
- **Nėra pašto kodo pjūvio.** Miestas per stambus. Vilnius yra ir Naujininkai,
  ir Žvėrynas. Reikia rajono arba pašto kodo lygio.
- **`salon_store_match_30d_pct = 0`** — pardavimas nesusiejamas su parduotuve.
- **Nežinoma, kurį pasiūlymą pirko.** Be to negalima pasakyti, ar brangus čekis
  yra dėl rajono, ar dėl konkretaus produkto.

Šie keturi dalykai yra kitas žingsnis, jei norima taikyti pagal rajonus tiksliai.
