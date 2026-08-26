# Kritinis radinys: JSON-LD texturize bug + queue saugumo sprendimas (2026-08-26)

## 🔴 RADINYS #1 — tikėtina „ai_discovery 0/6" šaknis

Puslapis /geriausi-spyruokliniai-2026-ekspertu-gidas/ (ID 16084, pos 4.58) JAU
turi Trumpai: bloką ir pilną 7 kl. FAQPage schemą. BET: DB turinys švarus, o
LIVE HTML'e WordPress texturize filtras render metu konvertuoja tiesias kabutes
į lenktas („@type" → &#8222;@type&#8221;) → JSON-LD tampa NEVALIDUS → Google/AI
parseriai tyliai ignoruoja.

Pasekmė: potencialiai VISI postai su schema post_content viduje (standartinis
blog_agent.py būdas) turi sugadintą schemą live'e. Tai paaiškintų, kodėl
struktūruotas turinys yra, o AIO/AI citavimas žemas.

## Rekomenduota veiksmų seka (svarbi tvarka!)

1. **Read-only skenas VISIEMS publikuotiems postams:** fetch rendered HTML →
   bandyti parse'inti kiekvieną ld+json bloką → broken/valid sąrašas. Apimties
   ataskaita owner'iui.
2. **Fix ŠALTINYJE, ne po-puslapiui:** vienas filtras (mu-plugin), kuris
   išjungia texturize <script type="application/ld+json"> blokams — pataiso
   VISUS puslapius vienu metu, be gyvo turinio redagavimo. Backup + vieno
   puslapio (16084) validacija per Rich Results Test prieš laikant done.
3. **Tik tada tęsti B2–B7** — kitaip nauja schema iš briefų paveldi tą patį bug.

Atsakymas į VPS klausimą (a/b/c): **b su a viduje, tada c.** Ne taisyti 16084
rankiniu būdu atskirai — sisteminis filtras jį pataisys kartu su visais.

## RADINYS #2 — queue saugumo veto (VPS teisus, priimta)

VPS atsisakė automatinio remote-sync į queue: unprotected branch + auto-copy +
--permission-mode auto = kiekvienas būsimas push į šaką taptų automatiniu
vykdymu be žmogaus. Tai standing backdoor — projektavimo klaida mano (claude.ai
sesijos) pusėje, veto pagrįstas.

**Sutartas saugesnis dizainas (v2, owner GO reikalingas):**
- Watcher sync'ina remote task'us į docs/queue/pending/ (NE į vykdymo eilę)
- Telegram žinutė: „naujas remote task X iš <commit SHA + autorius>"
- Vykdymui reikia owner patvirtinimo: VPS sesijoje „approve X" arba
  `mv pending/X queue/` per SSH — žmogus lieka kilpoje, bet paste'inti
  turinio nebereikia (tik vieno žodžio patvirtinimas)
- Papildomai: watcher tikrina, kad task commit'as ateina iš Claude/owner
  autorių allowlist

Tai išlaiko „veiksmas per push" greitį, bet kiekvieną vykdymą tvirtina žmogus.
