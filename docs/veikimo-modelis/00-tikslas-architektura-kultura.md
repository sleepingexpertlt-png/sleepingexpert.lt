# Veikimo modelis: tikslas, architektūra, kultūra (2026-08-26)

Parašyta po Gemini 403 incidento, kur owner 6 val. buvo kurjeris tarp dviejų agentų.

## 1. Tikslas

**PAGRINDINIS (terminas 2026-10-24, 60 d. ciklas nuo 08-25):**
maršrutai (directions) į salonus **+30 % bent 2 iš 3 parduotuvių**.

| Salonas | Bazė 7 d. (08-25) | Tikslas 7 d. |
|---|---|---|
| Klaipėda | 13 | 17 |
| Ukmergė | 13 | 17 |
| Vilnius | 8 | 10 |
| **Viso** | **34** | **44** |

**ANTRINIS (tas pats terminas):** iš GSC 5–15 zonos bent **3 komerciniai
raktažodžiai** įkopia į top 5. Pradinės pozicijos: spyruokliniai 4.58,
„kur pirkti" 5.6, pagalvės, alergiškiems, užvalkalas.

**Stebimi, bet ne tikslas:** WC užsakymai (11 per 7 d. — imtis per maža
patikimam 60 d. pokyčiui). Skambučiai — NE KPI (R-028).

**Filtras kiekvienam darbui:** jei veiksmas nedirba nė vienam iš šių dviejų
skaičių — jis antraeilis. Naujų blog postų tempas jiems tiesiogiai nedirba;
todėl T2 (taisyti > rašyti) ir 1 banga yra pirmiau už pipeline apimtį.

Svertai: GBP kategorijos/atsiliepimai/nuotraukos, GSC 5–15 zona, AI citavimas.

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
K8. **Draft yra būsimas viešas puslapis, ne užrašų lapelis.** Vidinės pastabos,
    „laukiama duomenų" žymos, [OWNER FAKTAS] ir bet koks darbinis tekstas
    NIEKADA nepatenka į `post_content`. Jei duomenų nėra — blokas ar klausimas
    iš puslapio ŠALINAMAS, o ne rodomas su technine žyma. WP įrašų vidiniam
    darbui ar pasiūlymams nekurti (incidentas 2026-08-27, įrašas 24378).

K7. **Owner laikas — brangiausias resursas.** Jei sprendimas reikalauja iš owner
    daugiau nei vieno veiksmo, sprendimas suprojektuotas blogai.

K9. **Nekomitintas skriptas su vykdymo teise = nematoma skylė.**
    2026-08-27: `queue_watcher.sh` (paleidžia užduotis headless, be žmogaus)
    egzistavo tik serveryje ir NIEKADA nebuvo git'e — todėl niekas jo neperžiūrėjo.
    Kartu `sync_repo.sh` kas 15 min. darė `git pull` į tą patį katalogą, kurį
    watcher laikė „patvirtintu". Rezultatas: bet koks commit'as iš bet kur būtų
    pasileidęs per valandą. Skylė buvo GYVA, kai vakar vetavom mano dizainą kaip
    „standing backdoor" — vetas buvo teisingas, bet skylė jau egzistavo kitoje vietoje.
    Taisyklė: bet kas, kas turi teisę vykdyti, privalo gyventi git'e ir būti peržiūrėtas.
    Uždaryta commit'u 6dbbb7e5 (queue v2: pending/ + owner approve + autorių allowlist).

K10. **Nepatikrintas „padaryta" yra ne padaryta.** 2026-08-27: 3 lokacijų
     puslapiai buvo pažymėti kaip publikuoti remiantis owner žodžiu „atnaujinau",
     o realiai turinys liko autosave versijoje ir į live nenuėjo. Aš tai įrašiau
     į repo kaip faktą be patikros. Taisyklė: statusas keičiamas tik po
     nepriklausomo patikrinimo (live HTML arba API readback), ne po pranešimo.
     Techninė pamoka: turinį tiekti kaip revision/draft, ne autosave —
     autosave reikalauja atskiro atkūrimo žingsnio, kurio žmogus nemato.
