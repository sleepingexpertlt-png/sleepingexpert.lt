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

## ŽINGSNIS 0 — NEMOKAMAS, DAROMAS PIRMA (be jo nepirkti)

Mes JAU turim citavimo įrodymų: GA4 rodo, į kuriuos mūsų puslapius ateina
ChatGPT lankytojai (`/locations/sleeping-expert-vilnius/` 15,
`/produkto-kategorija/pagalves/latekso-pagalves/` 11, realūs produktų psl.).
Tai atsako į dalį klausimo nemokamai.

BET tie duomenys dabar **klaidingi 5×**: `aeo_reverse_discovery.py:575`
`is_ai = ... or "ai" in medium` — substring'as įskaito „(data not available)"
(83 sesijos), `fb` (431), `ig` (33). Realus AI srautas ≈127, ne 684.

**0.1** Pataisyti tą sąlygą (tikslus atitikmuo vietoj substring'o) +
reprodukcinis testas: „(data not available)" neturi patekti į AI lentelę. 0 €.
**0.2** Su švariais duomenimis surinkti: kokio TIPO mūsų puslapiai gauna AI
srautą (lokacijos / kategorijos / produktai / blogas). 0 €.
**0.3** Tik jei po 0.2 lieka neatsakyta „ko mums trūksta, ko turi kiti" —
pirkti žemiau aprašytą tyrimą.

Priežastis, kodėl tai pirma: pirkti duomenis prieš išnaudojant turimus yra
ta pati klaida, kaip griebtis Ahrefs, kai GSC po ranka.

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

## Kas tikrina struktūrą (spraga, kurią reikėjo užpildyti)

API grąžina URL, ne puslapio sandarą. 3–7 punktai reikalauja atskiro crawl
žingsnio — **VPS pusėje**, nes claude.ai sesijai dauguma domenų uždaryti per
egress proxy. Be šio žingsnio 3–7 punktai lieka neužpildyti.

## Minimali imtis (kitaip — triukšmas, pateiktas kaip žinojimas)

- <15 skirtingų cituotų URL → išvada yra **„nepakanka duomenų"**, taisyklių
  NEKURIAME.
- ≥15 → taisyklė formuluojama tik jei pattern'as pasikartoja ≥70 % atvejų.
- PL duomenys duoda **hipotezes, ne išvadas**. EN kontrolė atskiria kalbos
  efektą nuo rinkos efekto, bet neįrodo, kad PL pattern'as veiks LT.

## Sprendimai IŠ ANKSTO (kitaip tai smalsumo pirkinys)

| Rezultatas | Ką darom |
|---|---|
| LT citatų ~0, PL turtingos | Laukas tuščias → formatas svarbiau už autoritetą. Taikom PL formų pamokas 1 bangoje, greitai. |
| LT citatos yra, bet ne mūsų | Konkurentai užėmė → lyginam jų formą su mūsų, taisom konkrečius puslapius. |
| LT citatos yra ir mūsų tarpe | Mūsų probe (0 % ChatGPT) melavo → keičiam matavimo metodiką, ne turinį. |
| Duomenų per mažai visose grupėse | DataForSEO LT rinkai netinka → uždarom kryptį, negrįžtam. |

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
