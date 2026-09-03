# aeo_monitor vs ai_visibility_agent — atviras klausimas, STEBIMA

Data: 2026-09-03. Statusas: **neveikti, stebėti.** Owner sprendimas.

## Kaip iškilo

Telegram signalas: `ANOMALY: aeo_monitor — 101 calls / 0,6583 $ per 1 val.
(limitas 100)`.

## Ką radau kode

`src/agents/aeo_monitor.py` — tikrina, ar AI sistemos cituoja sleepingexpert.lt.
Grandinė: Perplexity → ChatGPT → Claude Haiku → DataForSEO → Groq → DuckDuckGo.
Klausimai realūs ir nišiniai („hibridinis čiužinys ar verta pirkti Lietuva",
„čiužinys skoliozei turintiems").

**101 kvietimas paaiškinamas:** cron `30 7 * * 1,4` su `--faq-sample 15`.
15 klausimų × 6 tiekėjai = 90, plius atsarginiai bandymai → 101.
Ne ciklas, ne gedimas — **limitas nustatytas žemiau nei sukonfigūruotas kiekis.**

## Kodėl klausimas neuždarytas

`src/agents/ai_visibility_agent.py:5` pažodžiui:

> „Replaces aeo_monitor.py + geo_monitor.py."

O `aeo_monitor` tebeveikia cron'e. Ir pagal `PROMISES.md`, jis liko ant
brangesnio senojo Perplexity `/chat/completions` endpoint'o, kai
`ai_visibility_agent` jau perkeltas į Agent API (~2–4× pigiau).

**Atrodo kaip dublikatas. Bet owner pastaba (2026-09-03): agentai gali
atsakyti už skirtingus įrankius skirtinguose procesuose** — tada „dublikatas"
būtų klaidingas skaitymas, o išjungimas nutrauktų grandį, kurios nematome.

## Ko reikia PRIEŠ bet kokį veiksmą

1. Ką kiekvienas realiai rašo į DB — lentelės, laukai, eilučių kiekiai
2. Kas skaito tuos duomenis — kurie agentai, ataskaitos, KPI
3. Ar užklausų rinkiniai sutampa, ar skiriasi
4. Ar `aeo_baseline.py` (G4 KPI agregatorius) skaito vieną, kitą, ar abu

Kol į šiuos keturis neatsakyta — **nekeisti nieko:** neišjungti cron'o,
netrinti, nemigruoti endpoint'o.

## Kaštai, kol stebim

~0,66 $ / paleidimas · 2× per savaitę + 2× per mėn. pilnas ≈ **6–8 $/mėn.**
Suma maža, todėl skubaus veiksmo nereikia. Rizika neveikiant — mažesnė nei
rizika išjungus tai, ko nesuprantam.
