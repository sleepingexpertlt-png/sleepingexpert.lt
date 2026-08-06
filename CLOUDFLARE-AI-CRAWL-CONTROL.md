# Cloudflare AI Crawl Control — konfigūracija AI matomumui (AEO/GEO)

> **✅ IŠSPRĘSTA 2026-08-06 ~16:30:** visi Cloudflare AI blokai išjungti (Block AI bots, Bot Fight Mode, AI Labyrinth, Managed robots.txt → „Disable robots.txt configuration"), per-crawler blokai AI Crawl Control lentelėje — off. Gyvas robots.txt — švarus v2.1 be Cloudflare Managed Content sekcijos. AI Crawl Control statistika patvirtino srautą: Claude-User 105 allowed/0 blocked, ChatGPT-User 23 allowed. Hostinger patikrintas — nekaltas (užklausos serverio nepasiekdavo). Likutis: AI sistemų robots.txt kešai (iki ~24 h) išsivalys savaime.

**Data:** 2026-08-06
**Problema:** Cloudflare tinklo lygiu (403) blokuoja AI botus, kuriuos robots.txt v2.1 leidžia.
**Tikslas (G4):** GPTBot / ClaudeBot / PerplexityBot ir „user request" fetcher'iai turi gauti 200, kad AI galėtų skaityti ir cituoti sleepingexpert.lt.

---

## Patvirtinta diagnozė (2026-08-06)

| Testas | Rezultatas |
|---|---|
| `https://sleepingexpert.lt/robots.txt` per Anthropic fetcher (Claude-User) | **HTTP 403** |
| `https://sleepingexpert.lt/` per Anthropic fetcher | **HTTP 403** |

Net `robots.txt` grąžina 403 AI klientams — tai reiškia, kad blokas veikia **tinklo lygiu (WAF/Bot nustatymai)**, o ne per robots.txt. Todėl visos AEO investicijos (llms.txt, atsakymų blokai, schema) AI sistemoms nepasiekiamos, ir tai tiesiogiai paaiškina 0 % citavimą probe'uose.

Papildomai: robots.txt viršuje yra „Cloudflare Managed Content" sekcija su `Disallow: /` visiems AI botams ir `Content-Signal: ai-train=no` — ji prieštarauja mūsų v2.1 politikai.

---

## FIX — 2 jungikliai Cloudflare dashboard'e

### 1. Išjungti tinklo lygio AI botų bloką (403 šaltinis)

Dashboard → domenas `sleepingexpert.lt` → **Security → Settings** → filtras **Bot traffic**:

- **„AI Scrapers and Crawlers" / „Block AI bots"** → nustatyti **Do not block (Off)**.

Tada **AI Crawl Control → Security (Crawlers) tab** — kiekvienam botui veiksmas **Allow**:

| Botas | Operatorius | Kam reikalingas |
|---|---|---|
| GPTBot | OpenAI | ChatGPT žinios / training |
| OAI-SearchBot | OpenAI | ChatGPT Search indeksas |
| ChatGPT-User | OpenAI | **Realaus laiko fetch, kai vartotojas klausia** |
| ClaudeBot, Claude-SearchBot | Anthropic | Claude žinios / paieška |
| Claude-User | Anthropic | **Realaus laiko fetch** |
| PerplexityBot, Perplexity-User | Perplexity | Perplexity atsakymai ir citatos |
| Google-Extended | Google | Gemini grounding |
| Amazonbot | Amazon | Alexa atsakymai |
| Applebot-Extended | Apple | Apple Intelligence |
| Meta-ExternalAgent | Meta | Meta AI |
| CCBot | Common Crawl | Duomenų rinkinys daugeliui modelių |

`*-User` fetcher'iai svarbiausi citavimui — jie kviečiami tą akimirką, kai AI formuoja atsakymą vartotojui.

(Bytespider / ByteDance galima palikti Block — AEO naudos LT rinkoje beveik nėra, o krauna serverį.)

### 2. Išjungti Cloudflare valdomą robots.txt („Managed Content" sekcija)

Dashboard → **Security → Settings** → filtras **Bot traffic**:

- **„Set your preference to block training in robots.txt"** → **Off**.

Tai pašalins automatiškai injektuojamą sekciją su `Disallow: /` ir `Content-Signal: ai-train=no`. Liks tik mūsų robots.txt v2.1 (2026-08-02), kuris AI botus leidžia.

---

## Verifikacija (po pakeitimų, ~5 min propagacijai)

```bash
# Visi turi grąžinti 200 (ne 403):
curl -s -o /dev/null -w "GPTBot: %{http_code}\n"      -A "GPTBot/1.2"        https://sleepingexpert.lt/robots.txt
curl -s -o /dev/null -w "ClaudeBot: %{http_code}\n"   -A "ClaudeBot/1.0"     https://sleepingexpert.lt/robots.txt
curl -s -o /dev/null -w "Perplexity: %{http_code}\n"  -A "PerplexityBot/1.0" https://sleepingexpert.lt/
curl -s -o /dev/null -w "ChatGPT-User: %{http_code}\n" -A "ChatGPT-User/1.0" https://sleepingexpert.lt/

# robots.txt nebeturi turėti "Cloudflare Managed Content" sekcijos:
curl -s https://sleepingexpert.lt/robots.txt | head -20
```

Papildomas išorinis įrodymas: ChatGPT'e paklausti „What is sleepingexpert.lt?" su web search — turi sugebėti atsidaryti puslapį (ne „unable to access").

## Stebėjimas

- **AI Crawl Control → Metrics**: po 24–48 h turi matytis GPTBot/ClaudeBot užklausos su 200 statusu (dabar — 403).
- **Robots.txt tab**: sekti, ar crawleriai nepažeidžia v2.1 direktyvų.
- 111 promptų AI visibility matavimą kartoti po 1–2 sav. — laukiamas citavimo pokytis nuo 0 %.
