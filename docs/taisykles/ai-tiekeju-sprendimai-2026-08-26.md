# AI tiekėjų sprendimai (owner, 2026-08-26)

Kontekstas: inventorizacija rado 11 raktų (artifact: ai_vendor_inventory).
Principas: PIPELINE NELIEČIAMAS — Gemini ir Anthropic jame atskiri sąmoningai
(Gemini CAG context caching 230k/1h; Anthropic prompt caching + rašymas).
Keitimai tik po vieną, tik su owner GO šiame pokalbyje.

| Tiekėjas | Sprendimas | Pastabos |
|---|---|---|
| Anthropic | KEEP DIRECT | pipeline core |
| Gemini | KEEP DIRECT | CAG caching; + Letta embeddings (free tier / ~$0.02/mėn) |
| OpenAI (frontier) | KEEP DIRECT | GYVAS (gpt-5-search-api 08-25); ChatGPT probe'ai; $3.90 balansas gyvas — Letta .env turėjo SENĄ negyvą raktą |
| Groq | KEEP | greitos/pigios užduotys |
| OpenRouter | KEEP | jau naudojamas, $7.53; „uodegos" bazė — Kimi/Mistral/MiniMax/DeepSeek per jį, atskirų raktų NEKURTI |
| Perplexity | KEEP | testas 08-26: gyvas ✅; kvietimus rodyti cost_log |
| XAI | AVARINIS | owner sprendimas nelaikyti DELETE; ketvirtinis 1-kvietimo testas privalomas (netestuotas avarinis = neegzistuojantis); pasitikrinti ar tikrai free |
| DeepSeek | KEEP + ATGAIVINTI | owner: „kažkas ant jo stovi"; raktas 402 nuo 08-23 → owner top-up platform.deepseek.com ARBA (su atskiru GO) tas komponentas į OpenRouter |
| Letta OpenAI raktas | IŠIMTI | po Gemini fix'o nebereikalingas |

## Letta (2026-08-26)

- Fix: .env OPENAI_API_KEY ← GEMINI reikšmė + docker --force-recreate (OWNER,
  dar NEATLIKTA — cost_log jau rodo 6/6 failed embedding).
- Embedding tiekėjo NEKEISTI ateityje be re-embed plano (vektorių suderinamumas).
- Matomumas: scripts/letta_embedding_cost_log.py (frontier-agent 36c9aed0),
  cron 06:10 kasdien. Žinomas env quirk: docker logs --tail >5000 grąžina
  tuščią → cap 2000 su WARNING.
- Rotacijos laukia: LETTA_SERVER_PASSWORD, LETTA_PG_PASS (nutekėjo į transkriptą).

## Ateities fallback grandinė (dizainas, ne darbas; atskiras GO diegimui)

Pagrindinis → Groq → OpenRouter(:free) → XAI.
