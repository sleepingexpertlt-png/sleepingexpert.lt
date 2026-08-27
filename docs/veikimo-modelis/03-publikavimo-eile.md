# Owner publikavimo eilė (2026-08-27)

Visas šios savaitės turinys guli draft'uose. Publikuoja TIK owner (geležinė
taisyklė). WP admin → kiekviena nuoroda → peržiūra → Atnaujinti/Publikuoti.

## 1. Lokacijų puslapiai — ✅ GYVI IR PATIKRINTI (2026-08-27, VPS readback)

| Puslapis | Naujas turinys | Maršruto mygtukas | DUK | JSON-LD | Mojibake |
|---|---|---|---|---|---|
| Vilnius 12434 | ✅ | ✅ | ✅ | ✅ FAQPage + FurnitureStore | nėra |
| Klaipėda 12438 | ✅ (perdaryta) | ✅ | ✅ | ✅ | nėra |
| Ukmergė 12440 | ✅ (pataisyta) | ✅ | ✅ | ✅ | nėra |

**Klaipėdos tikroji priežastis (ne restore klaida):** jos autosave NIEKADA
neturėjo naujo turinio — buvo senas šablonas (location-page, ne v2), su
neatitinkančiais DUK tarp HTML ir JSON-LD, sena Place+BreadcrumbList schema
ir sulaužyta telefono nuoroda `href="http://+37060240202"` (rodė KITĄ numerį
nei matomas tekstas). Atkurti nebuvo ko — perdaryta iš generavimo skripto.

**K8 pažeidimas buvo GYVAS:** Ukmergės puslapyje viešai matėsi
`[OWNER FAKTAS — atsakymas dar nepatvirtintas...]`. Jį įnešė pats
`build_location_drafts.py`, o owner restore iškėlė į live. Pašalintas pagal
K8 (nėra atsakymo → blokas šalinamas, ne rodomas su žyma).

**Pastaba dėl dokumentų:** `docs/hermes-local/08-lokaciju-puslapiu-turinys.md`
gyvena ŠIAME repo (sleepingexpert.lt), ne frontier-agent repo — todėl VPS jo
`find` nerado. Ateityje nuorodas VPS'ui duoti kaip raw URL, ne kaip kelią.

