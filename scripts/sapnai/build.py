#!/usr/bin/env python3
"""Sapnų reikšmės — generatorius.

Iš data/sapnu-reiksmes/symbols/*.json sugeneruoja:
  build/sapnu-reiksmes/hub.html          WordPress įrašo turinys (fragmentas): žodynas su paieška
  build/sapnu-reiksmes/posts/<slug>.html WordPress įrašų turiniai (fragmentai): po vieną simboliui
  build/sapnu-reiksmes/manifest.json     sąrašas publish_wp.py skriptui (slug, title, excerpt, keywords)
  build/sapnu-reiksmes/preview/          pilni HTML puslapiai peržiūrai naršyklėje (index + posts/)

WordPress fragmentuose nuorodos į kitus įrašus rašomos kaip {{URL:<slug>}} — publish_wp.py
jas pakeičia tikrais permalink'ais, kai įrašai jau sukurti. Peržiūroje – santykinės nuorodos.

Naudojimas:  python3 scripts/sapnai/build.py [--out build/sapnu-reiksmes]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import html
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT, "data", "sapnu-reiksmes", "symbols")

SITE = "https://sleepingexpert.lt"
HUB_SLUG = "sapnu-reiksmes"
HUB_TITLE = "Sapnų reikšmės: 120 simbolių psichologijos ir mindfulness požiūriu"
CATEGORY_NAME = "Sapnų reikšmės"
CATEGORY_SLUG = "sapnu-reiksmes"
AUTHOR = "Sleeping Expert komanda"

LT_ALPHABET = list("AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽ")
LT_ORDER = {ch: i for i, ch in enumerate(LT_ALPHABET)}

# Simbolių WP slug'ai: numatytas "sapnuoti-<slug>", būsenoms – aiškesni.
WP_SLUG_OVERRIDES = {
    "kosmaras": "kosmarai-ka-reiskia",
    "pasikartojantis-sapnas": "pasikartojantys-sapnai",
    "samoningas-sapnas": "samoningi-sapnai",
    "miego-paralyzius": "miego-paralyzius",
    "baime": "baime-sapne",
    "sapnas-sapne": "klaidingas-pabudimas",
}

SOURCES = [
    ("Revonsuo A. (2000). The reinterpretation of dreams: An evolutionary hypothesis of the function of dreaming. "
     "<em>Behavioral and Brain Sciences</em>, 23(6), 877–901.", "10.1017/S0140525X00004015"),
    ("Schredl M., Hofmann F. (2003). Continuity between waking activities and dream activities. "
     "<em>Consciousness and Cognition</em>, 12(2), 298–308.", "10.1016/S1053-8100(02)00072-7"),
    ("Walker M. P., van der Helm E. (2009). Overnight therapy? The role of sleep in emotional brain processing. "
     "<em>Psychological Bulletin</em>, 135(5), 731–748.", "10.1037/a0016570"),
    ("Nielsen T., Levin R. (2007). Nightmares: A new neurocognitive model. "
     "<em>Sleep Medicine Reviews</em>, 11(4), 295–310.", "10.1016/j.smrv.2007.03.004"),
    ("Krakow B. et al. (2001). Imagery rehearsal therapy for chronic nightmares in sexual assault survivors with "
     "posttraumatic stress disorder: A randomized controlled trial. <em>JAMA</em>, 286(5), 537–545.", "10.1001/jama.286.5.537"),
    ("Freud S. (1900). <em>Die Traumdeutung</em>. Leipzig/Wien: Franz Deuticke (viešoji nuosavybė).", None),
    ("Jung C. G. (red.) (1964). <em>Man and His Symbols</em>. London: Aldus Books.", None),
    ("Hall C. S., Van de Castle R. L. (1966). <em>The Content Analysis of Dreams</em>. New York: Appleton-Century-Crofts.", None),
]

STORES = [
    ("Vilnius", "PC Baldų Rojus, Kalvarijų g. 125, 3 aukštas"),
    ("Klaipėda", "PC Helios Galeria, Taikos pr. 56, 1 aukštas"),
    ("Ukmergė", "Kauno g. 9"),
]


# --------------------------------------------------------------------------- helpers
def esc(s: str) -> str:
    return html.escape(s, quote=True)


def strip_diacritics(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def lt_sort_key(word: str):
    return [LT_ORDER.get(ch, 100 + ord(ch)) for ch in word.upper()]


def first_letter(word: str) -> str:
    ch = word.strip()[0].upper()
    return ch if ch in LT_ORDER else strip_diacritics(ch)


def wp_slug(slug: str) -> str:
    return WP_SLUG_OVERRIDES.get(slug, f"sapnuoti-{slug}")


def q_phrase(e: dict) -> str:
    t = e["title"]
    return t[0].lower() + t[1:] if t.lower().startswith("sapnuoti") else e["word"].lower()


def post_title(e: dict) -> str:
    t = e["title"]
    return f"{t}: ką tai reiškia?" if t.lower().startswith("sapnuoti") else t


def word_count(text_html: str) -> int:
    text_html = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", text_html, flags=re.S)
    return len(re.sub(r"<[^>]+>", " ", text_html).split())


def load_entries() -> tuple[list[dict], dict[str, str]]:
    entries, categories = [], {}
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        categories[d["category"]] = d["category_name"]
        for e in d["entries"]:
            e = dict(e)
            e["category"] = d["category"]
            e["category_name"] = d["category_name"]
            e.setdefault("aliases", [])
            e.setdefault("sleep_note", "")
            entries.append(e)
    slugs = [e["slug"] for e in entries]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        sys.exit(f"Dubliuoti slug'ai: {sorted(dupes)}")
    by_slug = {e["slug"]: e for e in entries}
    for e in entries:
        for r in e["related"]:
            if r not in by_slug:
                sys.exit(f"{e['slug']}: nežinomas related slug '{r}'")
    entries.sort(key=lambda e: lt_sort_key(e["word"]))
    return entries, categories


# --------------------------------------------------------------------------- CSS (scoped)
CSS = """
.se-sapnai{--se-blue:#142b6f;--se-accent:#3b40f0;--se-yellow:#ffd602;--se-mauve:#e1dee7;--se-gray:#6b6b7b;--se-bg:#f7f7f8;font-family:Outfit,system-ui,-apple-system,sans-serif;line-height:1.7;color:#1a1a2e}
.se-sapnai h2,.se-sapnai h3,.se-sapnai h4{color:var(--se-blue);line-height:1.25;font-weight:700}
.se-sapnai a{color:var(--se-accent)}
.se-sapnai .se-box{background:var(--se-bg);border-left:4px solid var(--se-yellow);border-radius:8px;padding:16px 20px;margin:24px 0}
.se-sapnai .se-box--note{border-left-color:var(--se-accent)}
.se-sapnai .se-box p:last-child{margin-bottom:0}
.se-sapnai .se-search{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:#fff;padding:12px 0;margin:16px 0 8px;border-bottom:1px solid var(--se-mauve)}
.se-sapnai .se-search input{width:100%;box-sizing:border-box;font:inherit;font-size:18px;padding:14px 16px;border:2px solid var(--se-blue);border-radius:12px;outline:none}
.se-sapnai .se-search input:focus{border-color:var(--se-accent);box-shadow:0 0 0 4px rgba(59,64,240,.15)}
.se-sapnai .se-count{font-size:14px;color:var(--se-gray);margin-top:6px}
.se-sapnai .se-letters{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.se-sapnai .se-letters a,.se-sapnai .se-letters span{display:inline-block;min-width:34px;text-align:center;padding:6px 8px;border-radius:8px;background:var(--se-mauve);color:var(--se-blue);text-decoration:none;font-weight:700;font-size:14px}
.se-sapnai .se-letters span{opacity:.35}
.se-sapnai .se-chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 20px}
.se-sapnai .se-chips button{font:inherit;font-size:14px;padding:8px 14px;border-radius:999px;border:1px solid var(--se-blue);background:#fff;color:var(--se-blue);cursor:pointer}
.se-sapnai .se-chips button[aria-pressed=true]{background:var(--se-blue);color:#fff}
.se-sapnai .se-item{border:1px solid var(--se-mauve);border-radius:12px;padding:16px 20px;margin:12px 0;background:#fff}
.se-sapnai .se-item h4{margin:0 0 6px;font-size:20px}
.se-sapnai .se-item h4 a{color:var(--se-blue);text-decoration:none}
.se-sapnai .se-item h4 a:hover{text-decoration:underline}
.se-sapnai .se-item .se-cat{display:inline-block;font-size:12px;color:var(--se-gray);background:var(--se-bg);border-radius:6px;padding:2px 8px;margin-left:8px;vertical-align:middle;font-weight:400}
.se-sapnai .se-item p{margin:6px 0}
.se-sapnai .se-item details{margin-top:8px}
.se-sapnai .se-item summary{cursor:pointer;color:var(--se-accent);font-weight:500}
.se-sapnai .se-item .se-more{display:inline-block;margin-top:8px;font-weight:700}
.se-sapnai .se-letter{margin-top:32px}
.se-sapnai .se-letter h3{font-size:28px;border-bottom:2px solid var(--se-yellow);padding-bottom:4px}
.se-sapnai .se-empty{padding:24px;text-align:center;color:var(--se-gray);background:var(--se-bg);border-radius:12px}
.se-sapnai .se-variants{width:100%;border-collapse:collapse;margin:16px 0}
.se-sapnai .se-variants th,.se-sapnai .se-variants td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--se-mauve)}
.se-sapnai .se-variants th{color:var(--se-blue);width:34%}
.se-sapnai .se-related{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none}
.se-sapnai .se-related li a{display:inline-block;padding:8px 14px;border-radius:999px;background:var(--se-mauve);color:var(--se-blue);text-decoration:none;font-weight:500}
.se-sapnai .se-related li a:hover{background:var(--se-yellow)}
.se-sapnai .se-crumbs{font-size:14px;color:var(--se-gray);margin-bottom:8px}
.se-sapnai .se-faq h3{font-size:18px;margin:18px 0 4px}
.se-sapnai .se-sources{font-size:14px;color:var(--se-gray)}
.se-sapnai .se-sources li{margin-bottom:6px}
.se-sapnai .se-bio{display:flex;gap:16px;align-items:flex-start;background:var(--se-bg);border-radius:12px;padding:16px 20px;margin:24px 0}
.se-sapnai .se-bio .se-avatar{flex:0 0 56px;width:56px;height:56px;border-radius:50%;background:var(--se-blue);color:var(--se-yellow);display:flex;align-items:center;justify-content:center;font-size:26px}
.se-sapnai .se-contact{background:var(--se-blue);color:#fff;border-radius:12px;padding:20px 24px;margin:24px 0}
.se-sapnai .se-contact h3{color:var(--se-yellow);margin-top:0}
.se-sapnai .se-contact p{margin:4px 0}
.se-sapnai .se-contact a{color:var(--se-yellow)}
.se-sapnai .se-cta{display:inline-block;background:var(--se-yellow);color:var(--se-blue);font-weight:700;padding:12px 20px;border-radius:10px;text-decoration:none;margin-top:8px}
@media (max-width:600px){.se-sapnai .se-variants th,.se-sapnai .se-variants td{display:block;width:auto}.se-sapnai .se-variants th{border-bottom:0;padding-bottom:0}.se-sapnai .se-item h4{font-size:18px}}
"""

SEARCH_JS = """
(function(){
  var q=document.getElementById('seSapnaiQ');if(!q)return;
  var items=[].slice.call(document.querySelectorAll('.se-sapnai .se-item'));
  var letters=[].slice.call(document.querySelectorAll('.se-sapnai .se-letter'));
  var chips=[].slice.call(document.querySelectorAll('.se-sapnai .se-chips button'));
  var empty=document.getElementById('seSapnaiEmpty');
  var count=document.getElementById('seSapnaiCount');
  var cat='';
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
  function run(){
    var t=norm(q.value.trim()),shown=0;
    items.forEach(function(it){
      var ok=(!cat||it.getAttribute('data-cat')===cat)&&(!t||it.getAttribute('data-search').indexOf(t)>-1);
      it.hidden=!ok;if(ok)shown++;
    });
    letters.forEach(function(sec){sec.hidden=!sec.querySelector('.se-item:not([hidden])');});
    empty.hidden=shown>0;
    count.textContent=shown===items.length?'Iš viso simbolių: '+items.length:'Rasta: '+shown+' iš '+items.length;
    if(t&&shown===1){var d=items.filter(function(i){return !i.hidden;})[0].querySelector('details');if(d)d.open=true;}
  }
  q.addEventListener('input',run);
  chips.forEach(function(b){b.addEventListener('click',function(){
    cat=b.getAttribute('aria-pressed')==='true'?'':b.getAttribute('data-cat');
    chips.forEach(function(c){c.setAttribute('aria-pressed',c.getAttribute('data-cat')===cat?'true':'false');});
    run();
  });});
  if(location.hash&&location.hash.indexOf('#q=')===0){q.value=decodeURIComponent(location.hash.slice(3));}
  run();
})();
"""


# --------------------------------------------------------------------------- shared blocks
def sources_block(full: bool) -> str:
    items = SOURCES if full else SOURCES[:3]
    lis = []
    for text, doi in items:
        lis.append(f"<li>{text}" + (f' DOI: <a href="https://doi.org/{doi}" rel="nofollow noopener">{doi}</a>' if doi else "") + "</li>")
    return '<h2>Šaltiniai</h2><ol class="se-sources">' + "".join(lis) + "</ol>"


def bio_block(short: bool = False) -> str:
    if short:
        return (f'<div class="se-bio"><div class="se-avatar" aria-hidden="true">☾</div><div><p><strong>{AUTHOR}</strong> – '
                "sertifikuoti miego konsultantai (MBSR/MBCT). Tekstas remiasi viešais moksliniais šaltiniais ir nėra medicininė diagnostika.</p></div></div>")
    return (
        '<div class="se-bio"><div class="se-avatar" aria-hidden="true">☾</div><div>'
        f"<p><strong>{AUTHOR}</strong> – sertifikuoti miego konsultantai (MBSR/MBCT). "
        "Sapnų reikšmes aiškiname ne kaip pranašystes, o kaip psichologijos ir miego mokslo požiūrį į tai, "
        "ką naktį apdoroja jūsų smegenys. Tekstas parengtas remiantis viešai prieinamais moksliniais šaltiniais "
        "ir nėra medicininė diagnostika.</p></div></div>"
    )


def contact_block(full: bool = True) -> str:
    stores = "".join(f"<p>🏪 <strong>{c}</strong>: {a}</p>" for c, a in STORES)
    if not full:
        return (
            '<div class="se-contact"><h3>Neramūs sapnai prasideda nuo neramaus miego</h3>'
            f"<p>Sertifikuoto miego konsultanto konsultacija – Vilniuje, Klaipėdoje ir Ukmergėje. "
            f'<a href="{SITE}/parduotuves/">Parduotuvės ir darbo laikas</a> · 📞 +370 630 70001</p></div>'
        )
    return (
        '<div class="se-contact"><h3>Blogas miegas – blogi sapnai. Pasikalbėkime apie jūsų miegą.</h3>'
        "<p>Neramūs sapnai dažnai prasideda nuo neramaus miego. Atvykite pasikonsultuoti su sertifikuotu miego "
        "konsultantu – 15 minučių pokalbis apie jūsų miego poziciją, čiužinį ir pagalvę dažnai paaiškina daugiau nei sapnininkas.</p>"
        f"{stores}<p>📞 +370 630 70001 · 📧 info@sleepingexpert.lt</p>"
        f'<a class="se-cta" href="{SITE}/parduotuves/">Parduotuvės ir darbo laikas</a></div>'
    )


def json_ld(obj: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


# --------------------------------------------------------------------------- spoke page
def render_post(e: dict, by_slug: dict, link, today: str) -> str:
    url = link(e["slug"])
    hub = link(HUB_SLUG)
    title = post_title(e)
    qp = q_phrase(e)
    parts = []
    parts.append(f'<div class="se-sapnai"><style>{CSS}</style>')
    parts.append(f'<p class="se-crumbs"><a href="{hub}">Sapnų reikšmės</a> › {esc(e["category_name"])} › {esc(e["word"])}</p>')
    parts.append(f'<div class="speakable"><p><strong>{esc(e["short"])}</strong></p></div>')
    aliases = [a for a in e["aliases"] if a.lower() != e["word"].lower()][:6]
    if aliases:
        parts.append(f"<p>Šį sapną žmonės įvardija įvairiai: {esc(', '.join(aliases))}. Kategorija žodyne – "
                     f"{esc(e['category_name'].lower())}; visą <a href=\"{hub}\">sapnų reikšmių žodyną su paieška</a> rasite čia.</p>")
    else:
        parts.append(f"<p>Kategorija žodyne – {esc(e['category_name'].lower())}; visą <a href=\"{hub}\">sapnų reikšmių žodyną su paieška</a> rasite čia.</p>")
    parts.append(f"<h2>Ką reiškia {esc(qp)}: psichologinis žvilgsnis</h2>")
    for p in e["psychology"]:
        parts.append(f"<p>{esc(p)}</p>")
    parts.append("<h2>Dažniausi sapno variantai</h2>")
    parts.append('<table class="se-variants"><thead><tr><th>Situacija sapne</th><th>Ką tai dažniausiai reiškia</th></tr></thead><tbody>')
    for v in e["variants"]:
        parts.append(f"<tr><th>{esc(v['situation'])}</th><td>{esc(v['meaning'])}</td></tr>")
    parts.append("</tbody></table>")
    parts.append("<h2>Mindfulness praktika ryte</h2>")
    parts.append(f'<div class="se-box"><p>🌱 {esc(e["mindfulness"])}</p></div>')
    if e["sleep_note"]:
        parts.append("<h2>Miego pastaba</h2>")
        parts.append(f'<div class="se-box se-box--note"><p>🛏️ {esc(e["sleep_note"])}</p></div>')
    parts.append("<h2>Susiję sapnų simboliai</h2>")
    parts.append('<ul class="se-related">' + "".join(
        f'<li><a href="{link(r)}">{esc(by_slug[r]["word"])}</a></li>' for r in e["related"]) + "</ul>")
    parts.append(f'<p>Visą žodyną su paieška rasite čia: <a href="{hub}">Sapnų reikšmės A–Ž</a>.</p>')

    # FAQ
    v0 = e["variants"][0]
    faq = [
        (f"Ką reiškia {qp}?", e["short"]),
        (f"Ar {qp} – blogas ženklas?",
         "Ne. Sapnai nepranašauja įvykių – psichologijos požiūriu jie atspindi jūsų dabartinius jausmus ir rūpesčius. "
         f"Svarbiausia yra emocija, kurią jautėte sapne, ir konkreti situacija: pavyzdžiui, jei {v0['situation'][0].lower() + v0['situation'][1:]}, "
         f"tai dažniausiai reiškia štai ką: {v0['meaning'][0].lower() + v0['meaning'][1:]}"),
        ("Ką daryti, jei toks sapnas kartojasi?",
         f"{e['mindfulness']} Jei sapnas grįžta kelias savaites iš eilės, jį verta užrašyti ir sąmoningai sugalvoti kitą pabaigą – "
         "šis metodas (vaizduotės repeticija) yra ištirtas ir veikia daugumai žmonių. Plačiau: straipsnis apie pasikartojančius sapnus."),
    ]
    parts.append('<div class="se-faq"><h2>DUK</h2>')
    for q, a in faq:
        a_html = esc(a)
        if "pasikartojančius sapnus" in a:
            a_html = a_html.replace("straipsnis apie pasikartojančius sapnus",
                                    f'<a href="{link("pasikartojantis-sapnas")}">straipsnis apie pasikartojančius sapnus</a>')
        parts.append(f"<h3>{esc(q)}</h3><p>{a_html}</p>")
    parts.append("</div>")
    parts.append(sources_block(full=False))
    parts.append(bio_block(short=True))
    parts.append(contact_block(full=False))
    parts.append(f'<p class="se-sources">Atnaujinta: {today}</p>')

    parts.append(json_ld({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": title, "description": e["short"], "inLanguage": "lt",
             "author": {"@type": "Organization", "name": AUTHOR},
             "publisher": {"@type": "Organization", "name": "Sleeping Expert", "url": SITE},
             "datePublished": today, "dateModified": today, "mainEntityOfPage": url,
             "isPartOf": {"@type": "WebPage", "@id": hub, "name": HUB_TITLE}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Blogas", "item": f"{SITE}/blogas/"},
                {"@type": "ListItem", "position": 2, "name": CATEGORY_NAME, "item": hub},
                {"@type": "ListItem", "position": 3, "name": e["word"], "item": url}]},
        ]}))
    parts.append("</div>")
    return "\n".join(parts)


# --------------------------------------------------------------------------- hub page
def render_hub(entries: list[dict], categories: dict, link, today: str) -> str:
    hub = link(HUB_SLUG)
    parts = [f'<div class="se-sapnai"><style>{CSS}</style>']
    parts.append(
        '<div class="speakable"><p><strong>Sapnų reikšmės čia aiškinamos ne kaip pranašystės, o kaip psichologijos ir miego '
        'mokslo žvilgsnis į tai, ką naktį apdoroja jūsų smegenys. Įveskite žodį į paiešką arba naršykite pagal abėcėlę – '
        f'kiekvienas iš {len(entries)} simbolių turi trumpą reikšmę čia pat ir atskirą straipsnį su variantais, mindfulness '
        'praktika ir miego pastabomis.</strong></p></div>'
    )
    parts.append(
        "<p>Sapnininkai Lietuvoje gyvuoja šimtmečius, bet dauguma jų remiasi prietarais: „gyvatė – priešas“, „dantys – mirtis“. "
        "Šis žodynas sudarytas kitaip. Kiekvieno simbolio reikšmė remiasi trimis šaltiniais: klasikine sapnų psichologija "
        "(S. Freudas, K. G. Jungas), šiuolaikiniais miego tyrimais (tęstinumo hipotezė, grėsmės simuliacijos teorija, "
        "emocijų apdorojimas REM miego metu) ir mindfulness praktika, kuri padeda sapną paversti įžvalga. Kur sapnas turi "
        "fiziologinį paaiškinimą (pavyzdžiui, negalėjimas bėgti ar miego paralyžius), tai pasakome tiesiai.</p>"
    )
    parts.append("<h2>Kaip naudotis šiuo sapnininku</h2><ol>"
                 "<li><strong>Pirmiausia prisiminkite emociją</strong>, ne siužetą. Ta pati gyvatė gali reikšti baimę arba atsinaujinimą – skiria jausmas.</li>"
                 "<li><strong>Įveskite žodį</strong> (galima be lietuviškų raidžių: „gyvate“, „ziurke“) arba pasirinkite kategoriją.</li>"
                 "<li><strong>Perskaitykite trumpą reikšmę</strong>, o jei norite variantų, praktikos ir miego pastabų – atsidarykite pilną straipsnį.</li>"
                 "<li><strong>Užrašykite sapną ryte.</strong> Sapnų dienoraštis – paprasčiausias būdas pastebėti, kurios temos kartojasi.</li></ol>")

    parts.append('<div class="se-search"><label for="seSapnaiQ"><strong>Sapnų paieška</strong></label>'
                 '<input id="seSapnaiQ" type="search" autocomplete="off" placeholder="Įveskite žodį, pvz.: gyvatė, dantys, kristi, buvęs…">'
                 f'<div class="se-count" id="seSapnaiCount">Iš viso simbolių: {len(entries)}</div></div>')

    present = {first_letter(e["word"]) for e in entries}
    parts.append('<nav class="se-letters" aria-label="Abėcėlė">' + "".join(
        f'<a href="#sapnai-{strip_diacritics(ch).lower()}">{ch}</a>' if ch in present else f"<span>{ch}</span>"
        for ch in LT_ALPHABET) + "</nav>")
    parts.append('<div class="se-chips" role="group" aria-label="Kategorijos">' + "".join(
        f'<button type="button" data-cat="{c}" aria-pressed="false">{esc(n)}</button>' for c, n in categories.items()) + "</div>")

    parts.append("<h2>Sapnų simbolių žodynas A–Ž</h2>")
    current = None
    for e in entries:
        ch = first_letter(e["word"])
        if ch != current:
            if current is not None:
                parts.append("</section>")
            current = ch
            parts.append(f'<section class="se-letter" id="sapnai-{strip_diacritics(ch).lower()}"><h3>{ch}</h3>')
        search = strip_diacritics(" ".join([e["word"], e["title"]] + e["aliases"] + [e["short"]])).lower()
        url = link(e["slug"])
        parts.append(f'<article class="se-item" id="s-{e["slug"]}" data-cat="{e["category"]}" data-search="{esc(search)}">')
        parts.append(f'<h4><a href="{url}">{esc(e["word"])}</a><span class="se-cat">{esc(e["category_name"])}</span></h4>')
        parts.append(f"<p>{esc(e['short'])}</p>")
        parts.append("<details><summary>Plačiau apie šį sapną</summary>")
        for p in e["psychology"]:
            parts.append(f"<p>{esc(p)}</p>")
        parts.append(f'<a class="se-more" href="{url}">Visas straipsnis: {esc(e["title"])} →</a></details></article>')
    parts.append("</section>")
    parts.append('<p class="se-empty" id="seSapnaiEmpty" hidden>Tokio simbolio dar nėra. Pabandykite sinonimą (pvz., „lokys“ vietoj „meška“) '
                 'arba parašykite mums – žodyną nuolat pildome.</p>')

    parts.append("<h2>Kodėl sapnuojame: trys teorijos, kuriomis remiasi šis žodynas</h2>")
    parts.append("<p><strong>Tęstinumo hipotezė.</strong> Sapnų turinys atkartoja tai, kas mums rūpi dieną (M. Schredl). Todėl sapnas apie "
                 "darbą po sunkios darbo savaitės nereikalauja simbolinės interpretacijos – jis tiesiog tęsia dieną.</p>"
                 "<p><strong>Grėsmės simuliacijos teorija.</strong> A. Revonsuo teigia, kad sapnai – evoliucinis treniruoklis: smegenys "
                 "naktį repetuoja pavojų atpažinimą. Tai paaiškina, kodėl persekiojimas, kritimas ir gyvatės sapnuojami visose kultūrose.</p>"
                 "<p><strong>Emocijų apdorojimas REM miego metu.</strong> M. Walkerio tyrimai rodo, kad REM miegas mažina emocinių "
                 "prisiminimų intensyvumą. Sapnas – šio proceso šalutinis produktas, todėl po sunkaus sapno dažnai pabundame lengvesni.</p>"
                 "<p>Prie šių teorijų pridedame Jungo simbolių kalbą (šešėlis, anima, savastis) ten, kur ji padeda įvardyti jausmą, "
                 "ir mindfulness praktikas, kurios sapną paverčia rytiniu klausimu sau.</p>")

    faq = [
        ("Ar sapnų reikšmės yra moksliškai pagrįstos?",
         "Konkrečių simbolių reikšmės („gyvatė reiškia X“) moksliškai neįrodytos – jos kyla iš psichologinių mokyklų ir kultūros. "
         "Moksliškai pagrįsta tai, kad sapnai atspindi budrų gyvenimą, apdoroja emocijas ir repetuoja grėsmes. Šis žodynas remiasi būtent tuo."),
        ("Ar sapnas gali pranašauti ateitį?",
         "Ne. Nėra jokių tyrimų, patvirtinančių pranašiškus sapnus. Sapnai gali atspindėti jūsų nuojautas ir rūpesčius, "
         "kurių dieną neįvardijote – todėl kartais atrodo, kad „išsipildė“."),
        ("Kodėl neprisimenu savo sapnų?",
         "Sapnus prisimename tik pabudę REM fazėje ar iškart po jos. Padeda pastovus miego laikas, sapnų dienoraštis prie lovos ir "
         "kelios sekundės ramybės ryte prieš imant telefoną."),
        ("Ką daryti, jei sapnuoju košmarus kelis kartus per savaitę?",
         "Jei tai tęsiasi ilgiau nei mėnesį, tai laikoma miego sutrikimu ir yra gydoma – vaizduotės repeticijos terapija turi tvirtus "
         "įrodymus. Pirmieji žingsniai: reguliarus miego laikas, jokio alkoholio prieš miegą, vėsus ir tamsus miegamasis."),
        ("Ar prasta lova gali sukelti blogus sapnus?",
         "Tiesiogiai – ne, bet netiesiogiai – taip: nepatogus čiužinys ar netinkama pagalvė dažnina prabudimus, o dažni prabudimai REM "
         "fazėje reiškia, kad sapnus prisimenate ryškiau ir dažniau, įskaitant nemalonius. Geras miegas – pirmas žingsnis prie ramesnių sapnų."),
    ]
    parts.append('<div class="se-faq"><h2>DUK apie sapnus</h2>')
    for q, a in faq:
        parts.append(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>")
    parts.append("</div>")
    parts.append(sources_block(full=True))
    parts.append(bio_block())
    parts.append(contact_block())
    parts.append(f'<p class="se-sources">Atnaujinta: {today}. Žodynas pildomas – trūkstamą simbolį galite pasiūlyti el. paštu.</p>')
    parts.append(f"<script>{SEARCH_JS}</script>")
    parts.append(json_ld({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": HUB_TITLE, "inLanguage": "lt",
             "description": "Sapnų reikšmių žodynas su paieška: 120 simbolių, aiškinamų psichologijos, miego mokslo ir mindfulness požiūriu.",
             "author": {"@type": "Organization", "name": AUTHOR},
             "publisher": {"@type": "Organization", "name": "Sleeping Expert", "url": SITE},
             "datePublished": today, "dateModified": today, "mainEntityOfPage": hub},
            {"@type": "ItemList", "name": "Sapnų simboliai", "numberOfItems": len(entries),
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": e["word"], "url": link(e["slug"])}
                                 for i, e in enumerate(entries)]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        ]}))
    parts.append("</div>")
    return "\n".join(parts)


# --------------------------------------------------------------------------- preview wrapper
def wrap_artifact(title: str, body: str, depth: int) -> str:
    return f"""<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#ffffff;--fg:#1a1a2e;--head:#142b6f;color-scheme:light}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:Outfit,system-ui,sans-serif;font-size:16px}}
.wrap{{max-width:820px;margin:0 auto;padding-block:24px 64px;padding-inline:16px}}
.top{{background:#142b6f;color:#fff;padding-block:14px;padding-inline:16px}}
.top .in{{max-width:820px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}}
.top a{{color:#ffd602;text-decoration:none;font-weight:700}}
.top small{{opacity:.8}}
h1{{color:#142b6f;font-size:clamp(26px,5vw,38px);line-height:1.2;margin:8px 0 16px;text-wrap:balance}}
</style>
<div class="top"><div class="in"><a href="{'../' * depth}index.html">☾ Sleeping Expert · Sapnų reikšmės</a><small>Peržiūra – taip atrodys WordPress įrašas</small></div></div>
<main class="wrap">
<h1>{esc(title)}</h1>
{body}
</main>
"""


def wrap_preview(title: str, body: str, description: str, depth: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="lt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#ffffff;--fg:#1a1a2e;--head:#142b6f}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#ffffff;--fg:#1a1a2e}}}}
:root[data-theme="dark"]{{--bg:#ffffff;--fg:#1a1a2e}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:Outfit,system-ui,sans-serif}}
.wrap{{max-width:820px;margin:0 auto;padding:24px 16px 64px}}
.top{{background:#142b6f;color:#fff;padding:14px 16px}}
.top .in{{max-width:820px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}}
.top a{{color:#ffd602;text-decoration:none;font-weight:700}}
.top small{{opacity:.8}}
h1{{color:#142b6f;font-size:clamp(26px,5vw,38px);line-height:1.2;margin:8px 0 16px}}
</style>
</head>
<body>
<div class="top"><div class="in"><a href="{'../' * depth}index.html">☾ Sleeping Expert · Sapnų reikšmės</a><small>Peržiūra – taip atrodys WordPress įrašas</small></div></div>
<main class="wrap">
<h1>{esc(title)}</h1>
{body}
</main>
</body>
</html>
"""


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "build", "sapnu-reiksmes"))
    args = ap.parse_args()
    out = args.out
    today = dt.date.today().isoformat()

    entries, categories = load_entries()
    by_slug = {e["slug"]: e for e in entries}

    os.makedirs(os.path.join(out, "posts"), exist_ok=True)
    os.makedirs(os.path.join(out, "preview", "posts"), exist_ok=True)
    os.makedirs(os.path.join(out, "artifact", "posts"), exist_ok=True)

    # 1) WordPress fragments with placeholders
    wp_link = lambda slug: "{{URL:" + slug + "}}"
    hub_html = render_hub(entries, categories, wp_link, today)
    with open(os.path.join(out, "hub.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)
    manifest = {
        "generated": today,
        "category": {"name": CATEGORY_NAME, "slug": CATEGORY_SLUG,
                     "description": "Sapnų reikšmės psichologijos, miego mokslo ir mindfulness požiūriu. 120 simbolių su paieška."},
        "hub": {"slug": HUB_SLUG, "key": HUB_SLUG, "title": HUB_TITLE, "file": "hub.html",
                "excerpt": "Sapnų reikšmių žodynas su paieška: 120 simbolių, aiškinamų psichologijos, miego mokslo ir mindfulness požiūriu.",
                "focus_keyword": "sapnų reikšmės", "secondary_keywords": "sapnininkas, sapnų aiškinimas, ką reiškia sapnuoti, sapnų žodynas",
                "words": word_count(hub_html)},
        "posts": [],
    }
    for e in entries:
        body = render_post(e, by_slug, wp_link, today)
        fn = f"{e['slug']}.html"
        with open(os.path.join(out, "posts", fn), "w", encoding="utf-8") as f:
            f.write(body)
        manifest["posts"].append({
            "key": e["slug"], "slug": wp_slug(e["slug"]), "title": post_title(e), "file": f"posts/{fn}",
            "excerpt": e["short"], "category": e["category_name"],
            "focus_keyword": q_phrase(e), "secondary_keywords": ", ".join(e["aliases"][:5]),
            "words": word_count(body),
        })
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 2) Preview (relative links)
    def prev_link_factory(depth: int):
        prefix = "../" * depth
        return lambda slug: f"{prefix}index.html" if slug == HUB_SLUG else f"{prefix}posts/{slug}.html"

    with open(os.path.join(out, "preview", "index.html"), "w", encoding="utf-8") as f:
        f.write(wrap_preview(HUB_TITLE, render_hub(entries, categories, prev_link_factory(0), today),
                             manifest["hub"]["excerpt"], 0))
    for e in entries:
        with open(os.path.join(out, "preview", "posts", f"{e['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(wrap_preview(post_title(e), render_post(e, by_slug, prev_link_factory(1), today), e["short"], 1))

    # 3) Artifact (claude.ai) – fragments without document skeleton
    with open(os.path.join(out, "artifact", "index.html"), "w", encoding="utf-8") as f:
        f.write(wrap_artifact("Sapnų reikšmės A–Ž", render_hub(entries, categories, prev_link_factory(0), today), 0))
    for e in entries:
        with open(os.path.join(out, "artifact", "posts", f"{e['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(wrap_artifact(post_title(e), render_post(e, by_slug, prev_link_factory(1), today), 1))

    words = [p["words"] for p in manifest["posts"]]
    print(f"OK: {len(entries)} simboliai, {len(categories)} kategorijos → {out}")
    print(f"hub: {manifest['hub']['words']} žodžių; įrašai: min {min(words)} / vid {sum(words)//len(words)} / max {max(words)} žodžių")
    return 0


if __name__ == "__main__":
    sys.exit(main())
