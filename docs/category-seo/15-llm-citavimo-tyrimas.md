# LLM citavimo pattern'ų tyrimas (owner GO 2026-08-27)

Klausimas, į kurį atsakom: **kokios FORMOS puslapius ChatGPT/Gemini realiai
cituoja čiužinių temoje** — ir ar LT rinkoje ta vieta jau užimta, ar tuščia.

Įrankis: DataForSEO **LLM Source Annotations** (2026-07, grąžina cituotą URL,
ne tik paminėjimą) + LLM Mentions.

## Kodėl per Lenkiją

LT rinka maža → LLM'ai turi mažai LT šaltinių → citatų gali beveik nebūti.
PL rinka ta pati produktų kategorija, ta pati ES aplinka, ~13× didesnė →
citavimo pattern'as matomas. Iš jos imame **struktūrą, ne turinį**.

⚠️ **Griežta riba (T1 + rugpjūčio spam update):** kopijuoti konkurentų temas
ar tekstą DRAUDŽIAMA. Perkeliame tik atsakymą į klausimą „kokios formos
puslapiai cituojami" — lentelės, specifikacijos, DUK, forumai, agregatoriai.

## Eksperimento apimtis (viena partija, be cron)

| Grupė | Kiek | Pavyzdžiai |
|---|---|---|
| LT — mūsų taikiniai | 10 | „geriausi spyruokliniai čiužiniai", „koks čiužinys tinka alergiškiems", „kur pirkti čiužinį internetu", „kaip išsirinkti pagalvę" |
| PL — tie patys klausimai lenkiškai | 10 | „najlepsze materace kieszeniowe", „jaki materac dla alergika", „jak wybrać poduszkę" |
| EN — kontrolė | 5 | tas pats angliškai, kad matytume, ar skirtumas dėl kalbos, ar dėl rinkos |

## Ką fiksuoti KIEKVIENAI citatai (tai svarbiau už patį citatų skaičių)

1. Cituotas URL + domenas
2. **Puslapio tipas:** gidas / kategorija / produktas / forumas / agregatorius / žiniasklaida
3. Ar puslapyje yra **palyginimo lentelė**? (taip/ne)
4. Ar yra **DUK blokas**? (taip/ne)
5. Ar yra **konkretūs skaičiai/specifikacijos** pirmuose 200 žodžių?
6. Ar yra **struktūruoti duomenys** (JSON-LD)?
7. Apytikslis ilgis

## Rezultatas, kurio siekiam

Ne ataskaita, o **3–5 taisyklės mūsų turiniui**, pvz.: „cituojami puslapiai
90 % atvejų turi palyginimo lentelę pirmame ekrane" arba „LT užklausose
citatų 0 → laukas tuščias, formatas svarbesnis už autoritetą".

Tos taisyklės tada eina į `14-banga1-turinys.md` kaip privalomi elementai.

## Kaštai ir saugikliai

- 10 € — **signalizacija, ne lubos** (owner sprendimas 2026-08-27).
  10–25 € — tęsiam, jei matyti rezultatas. >25 € — atskiras sprendimas.
- **Kietas stabdis: JOKIO cron.** Tik rankiniai kvietimai. Būtent automatinis
  kartojimas, ne suma, degino 20 $/mėn. iki 2026-08-02 (R-042).
- Kiekvienas kvietimas → `cost_log` (matomumo taisyklė).
- `seo-dataforseo` skill'ui reikia guard'o: jis gali būti pakviestas bet kurio
  agento ir pradėti leisti pinigus be sprendimo. Atskira užduotis.

## Kodėl tai nėra „dar vienas matavimas"

Turim 937 probe eilutes ir savaitinį cron'ą — istorijos netrūksta. Trūksta
teisingumo: mūsų probe rodo 0 % ChatGPT citavimo, o GA4 tuo pačiu metu 121
realią ChatGPT sesiją. Šis tyrimas ne prideda trendo liniją, o atsako, kuris
iš dviejų skaičių meluoja.
