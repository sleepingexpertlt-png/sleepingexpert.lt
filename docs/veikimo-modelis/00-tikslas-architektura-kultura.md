# Veikimo modelis: tikslas, architektūra, kultūra (2026-08-26)

Parašyta po Gemini 403 incidento, kur owner 6 val. buvo kurjeris tarp dviejų agentų.

## 1. Tikslas

**Verslo:** daugiau maršrutų (directions) į 3 salonus ir WC užsakymų — R-028 KPI;
skambučiai NĖRA KPI. Svertai: GBP kategorijos/atsiliepimai, GSC 5–15 zona, AI
citavimas.

**Sisteminis:** veikti be kasdienio owner dalyvavimo. Matas —
**owner intervencijų skaičius per savaitę**. Jei jis auga, sistema degraduoja,
net jei visi agentai „dirba".

## 2. Architektūra

| Sluoksnis | Atsakomybė | Ribos |
|---|---|---|
| Owner | sprendimai, verslo faktai, kredencialai, publish | nedaro to, ką gali mašina |
| claude.ai sesija | planai, auditas, dokumentai, Letta atmintis, nepriklausoma verifikacija per Hermès MCP | nepasiekia serverio |
| VPS agentas | vykdymas: WP draftai, pipeline, kodas, cron | neliečia kredencialų |
| Hermès | 26 agentai, orchestratorius, kokybės vartai, atmintis | draft-only |

**Žinoma silpna vieta:** jungtis claude.ai ↔ VPS. Šiandien ta jungtis buvo owner
(copy-paste). Taisymas — queue v2: užduotis įrašoma į repo, watcher pasiima,
owner patvirtina vienu žodžiu. Laukia GO.

## 3. Kultūrinės taisyklės (visos patvirtintos realiais incidentais)

K1. **Įrodymas, ne pasakojimas.** „Veikia" = draft ID + q reikšmė, HTTP kodas,
    commit SHA. Be jų — nedeklaruoti.
K2. **Agentai neliečia kredencialų.** Nei „owner GO pokalbyje", nei suskaidžius
    į žingsnius. Agentas pateikia komandą, žmogus paleidžia.
K3. **Netestuotas avarinis kelias = neegzistuojantis.** Kiekviena fallback grandis
    turi periodinį liveness testą (DeepSeek buvo miręs 3 paras nepastebėtas).
K4. **Tylus gedimas blogiau už garsų.** 0 rezultatų su `errors: []` yra klaida,
    ne sėkmė. Kiekvienas nulinis rezultatas privalo turėti signalą.
K5. **TAISYTI > RAŠYTI.** Išsemtas temų bankas = teisingas „ne", ne bug'as
    (žr. T2 spam-update vadovėlyje).
K6. **Klaida taisoma iškart, be gynybos.** Šioje sesijoje: 3 klaidingos diagnozės
    ir 1 klaidingas nurodymas VPS'ui — kiekvieną kartą greičiau pripažinti.
K7. **Owner laikas — brangiausias resursas.** Jei sprendimas reikalauja iš owner
    daugiau nei vieno veiksmo, sprendimas suprojektuotas blogai.
