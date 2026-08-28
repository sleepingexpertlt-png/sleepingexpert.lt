# MiniCPM — lokalus atvirojo kodo modelis mūsų instrumentuose

Patikrinta gyvai HuggingFace 2026-08-27.

| Modelis | Tipas | Atsisiuntimai | Atnaujintas |
|---|---|---|---|
| **`openbmb/MiniCPM5-1B`** | text-generation, 1B | 916 977 | 2026-08-17 |
| `openbmb/MiniCPM-V-4.6` | image-text-to-text | 605 447 | 2026-08-17 |
| `openbmb/MiniCPM-o-4_5` | any-to-any (garsas+vaizdas) | 994 338 | 2026-08-18 |

Licencija ir tikslus modelio dydis diske tikrinami prieš diegimą — čia
užfiksuoti tik gyvai patikrinti Hub duomenys, ne prielaidos.

## Kodėl į mūsų instrumentus

Šiandien KIEKVIENA smulki operacija eina per mokamą API. Dauguma jų nėra
kūryba — tai klasifikavimas ir ištraukimas. Tam 1B modelio pakanka, ir jis
sukasi vietoje už 0 €.

## Darbų padalijimas (griežtas)

**MiniCPM (lokaliai, 0 €) — mechaninis darbas:**
- NAP normalizavimas ir palyginimas (L5): ar „(0-630) 70001" ir
  „+370 630 70001" yra tas pats numeris
- Atsiliepimų sentimentas ir kategorizavimas prieš atsakymo juodraštį (L3)
- Produktų atributų ištraukimas iš aprašymų (WooCommerce spraga:
  spyruoklių tipas, dydis, kietumas — dažnai jau parašyta tekste)
- Raktažodžių grupavimas į temas (1675 frazės iš 17 failo)
- Kanibalizacijos pirminė atranka: kurios URL poros persidengia
- Turinio „thin content" filtras prieš K11 patikrą

**Claude / mokamas API — tik ten, kur reikia kokybės:**
- Bet koks klientui matomas tekstas (brand voice, draudžiami teiginiai)
- Atsakymai į atsiliepimus (galutinis variantas)
- Sprendimai ir auditai

**Riba viena ir aiški: jei rezultatą matys klientas — ne MiniCPM.**

## Kaštų logika

Mechaninis darbas šiandien yra didžioji dalis iškvietimų ir mažoji dalis
vertės. Perkėlus jį į lokalų modelį, mokamas API lieka tik ten, kur jo
kokybė realiai skiriasi. Tikslus sutaupymas skaičiuojamas iš `cost_log`
po pirmo mėnesio — be to skaičiaus jokių „sutaupysim X" teiginių
(M3 taisyklė galioja ir kaštams).

## Diegimo reikalavimai — patikrinti PRIEŠ diegiant

VPS turi ribotą diską (`main` šakoje ką tik atsirado swap/zram runbook —
tai signalas, kad atmintis įtempta). Todėl prieš diegimą:

1. Laisva vieta diske ir RAM
2. GGUF kvantizuotas variantas, ne pilnas svoriai
3. Ar `llama.cpp` / `ollama` jau yra serveryje
4. Licencija komerciniam naudojimui
5. Paleisti kaip atskirą servisą su atminties limitu — kad nenugriautų
   blogo pipeline'o, kuris ką tik atsistatė

Jei RAM nepakanka — instrumentas neįrašomas. Geriau nieko, negu nugriautas
veikiantis pipeline'as.
