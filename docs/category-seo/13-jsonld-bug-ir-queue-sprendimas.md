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

## SKENO REZULTATAI (2026-08-26, VPS): 349 items, 1447 blokų, 98.2 % validūs

- **A klasė (5 psl., 16 blokų):** <script> žyma DINGSTA render metu, JSON tampa
  MATOMU tekstu lankytojui su lenktomis kabutėmis. Paveikti: 16084 (pos 4.58!),
  klaidos-renkantis, lova-spintoje, kaip-daznai-keisti-patalyne, vesinantys.
  Fix: mu-plugin (bet turi spręsti ir TAG STRIPPING, ne vien texturize).
- **B klasė (10 psl.):** PATIKSLINTA ŠAKNIS (mano json.dumps hipotezė buvo
  klaidinga): blog_agent.py „Auto-boost internal links" (~4930 eil.) įterpia
  <a href> į VISĄ content, įskaitant anksčiau (4602–4866 eil.) pridėtus JSON-LD
  blokus — nuoroda įkrenta į JSON string reikšmę ir sulaužo sintaksę.
  ✅ FIX: script-blokų placeholder apsauga prieš auto-link (įdiegta, patikrinta
  atkartojant tikslų korupcijos atvejį). Puslapiai: 9/10 sutaisyti su backup,
  paskutinis (miego-architektura, TinyMCE šiukšlės) atkuriamas.
- **A klasės BLOKERIS:** VPS neturi hostingo FS/SSH prieigos (svetainė kitame
  serveryje už Cloudflare; tik WP REST API) → mu-plugin agentas įdiegti negali.
  Keliai: (1) owner įdiegia mu-plugin ranka (precedentas: se-gcr-optin.php
  2026-08-04), (2) REKOMENDUOJAMA — schema perkelti iš post_content į RankMath
  meta/wp_head kelią, kuris the_content filtrų grandinę apeina (įrodyta:
  RankMath sitewide schema renderinasi be klaidų).
- 1421 blokai sveiki — fix'ai privalo jų nesugadinti (regresijos patikra).

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
