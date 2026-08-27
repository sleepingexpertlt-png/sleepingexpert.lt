# AUDITAS: kodėl 1 bangos puslapiai tušti (2026-08-27)

Atliktas pagal owner reikalavimą. Įrodymai: mano paties spec
`14-banga1-turinys.md` + owner ekrano nuotrauka su realiu #24373 turiniu.

## B1 (#24373) — spec vs realybė

| Elementas | Spec | Realybė | |
|---|---|---|---|
| Title | 3 variantai | variantas 2 | ✅ |
| Trumpai (48 ž.) | yra | yra, žodis į žodį | ✅ |
| **Palyginimo lentelė** | **5–7 eilutės** | **NĖRA** | 🔴 |
| DUK 5 kl. su atsakymais | yra | yra | ✅ |
| JSON-LD | yra | yra | ✅ |

Apytiksliai ~300 žodžių. SEO 7/100.

**Be lentelės puslapis yra: bendra bonnell/pocket definicija + 5 bendri DUK.**
Nė vieno dalyko, kurio nėra kiekvieno konkurento puslapyje. T1 (unikali vertė)
neįvykdytas. Lentelė buvo VIENINTELIS unikalus elementas.

## ŠAKNIS — projektavimo klaida, ne vykdymo

Mano spec'e lentelė pažymėta `[OWNER FAKTAS / WC]`. Tai reiškia: puslapio
vienintelė unikali vertė buvo padaryta priklausoma nuo duomenų, kuriuos aš
pats pažymėjau kaip neturimus.

Tada įvedžiau K8: „nėra atsakymo → blokas ŠALINAMAS, ne rodomas su žyma".

**Dvi taisyklės kartu garantavo tuščią puslapį.** VPS negalėjo įvykdyti
teisingai — bet kuris vykdytojas būtų gavęs tą patį rezultatą. Tai ne jo
klaida ir ne owner klaida.

## MASTAS — problema ne viename puslapyje

Patikrinau visą spec'ą (`grep` placeholder'ių):

| Psl. | Priklausomybė nuo [OWNER FAKTAS]/[WC] | Kas lieka po K8 šalinimo |
|---|---|---|
| B1 | lentelė (vienintelė unikali vertė) | intro + 5 bendri DUK → **thin** |
| B2 | **3 iš 5 DUK** | **tik 2 DUK** → **dar blogiau nei B1** |
| B3 | lentelės stulpelis „pavyzdys iš asortimento" | lentelė be pavyzdžių → dalinai |
| B4 | nėra | **vienintelis švarus puslapis** |
| B5 | lentelė + 1 DUK | be lentelės → **thin** |

**4 iš 5 puslapių buvo suprojektuoti taip, kad neatėjus duomenims taptų
tuščiais.** Ir aš juos pateikiau tau publikuoti.

## Ką tai reiškia praktiškai

- Publikavus juos tokius, būtume patys pagaminę tiksliai tokį turinį, kokį
  aprašo mūsų pačių `google-spam-2026-08-vadovelis.md` T1/T6 kaip baudžiamą.
- „Kur pirkti internetu" (B2) yra didžiausias taikinys (>1200 impr.) ir
  būtų nuėjęs su 2 DUK ir be nieko daugiau.

## Taisymas (privalomas prieš bet kokį publikavimą)

1. **Lentelės pildomos iš WooCommerce**, ne iš owner. Duomenys sistemoje YRA.
2. **B2 DUK**: 3 klausimai apie pristatymą/grąžinimą/finansavimą — atsakymai
   yra WooCommerce nustatymuose ir svetainės taisyklių puslapiuose
   (`/pirkimo-taisykles-ir-salygos/` jau egzistuoja ir buvo redaguotas 08-04).
   Owner klausti nereikėjo — reikėjo perskaityti savo pačių puslapį.
3. Nė vienas puslapis neteikiamas peržiūrai be verdikto GALIMA (K11).

## Pamoka į taisykles

**K12: specifikacija, kurios unikalios vertės elementas priklauso nuo
neturimų duomenų, yra bloga specifikacija.** Prieš rašant spec'ą reikia
patikrinti, ar duomenys pasiekiami sistemoje. Jei ne — arba surandamas kitas
vertės šaltinis, arba puslapis nedaromas. Placeholder'is turinio spec'e =
suplanuotas thin content.
