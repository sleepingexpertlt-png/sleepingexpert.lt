#!/usr/bin/env python3
"""Generuoja audinių katalogo HTML bloką iš audiniai.json.

Naudojimas:
    python3 build.py            # -> audiniu-katalogas.html
    python3 build.py --images   # įjungia swatch nuotraukas (IMG_BASE)

Rezultatą įklijuoti į WP puslapį kaip "Custom HTML" bloką.
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "audiniai.json"
OUT = HERE / "audiniu-katalogas.html"

# Kur guli swatch nuotraukos WP Media Library'je.
# Failo kelias: {IMG_BASE}/{tiekejo-slug}/{audinio-slug}.webp
IMG_BASE = "/wp-content/uploads/audiniai"

BRAND_NAVY = "#142b6f"
BRAND_LEMON = "#ffd602"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build(with_images: bool) -> str:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    suppliers = data["tiekejai"]
    groups = data["grupes"]

    items = []
    for supplier in suppliers:
        for group, fabrics in sorted(supplier["audiniai"].items()):
            for fabric in fabrics:
                items.append(
                    {
                        "name": fabric,
                        "supplier": supplier["vardas"],
                        "supplier_slug": supplier["slug"],
                        "group": group,
                        "slug": slugify(fabric),
                    }
                )
    items.sort(key=lambda i: (i["supplier"], int(i["group"]), i["name"]))

    total = len(items)
    group_counts = {g: sum(1 for i in items if i["group"] == g) for g in sorted(groups)}
    supplier_counts = {s["vardas"]: sum(1 for i in items if i["supplier"] == s["vardas"]) for s in suppliers}

    # --- filtrų mygtukai ---
    supplier_chips = ['<button type="button" class="se-fab__chip is-active" data-filter="supplier" data-value="all">Visi tiekėjai <span>%d</span></button>' % total]
    for supplier in suppliers:
        supplier_chips.append(
            '<button type="button" class="se-fab__chip" data-filter="supplier" data-value="%s">%s <span>%d</span></button>'
            % (esc(supplier["vardas"]), esc(supplier["vardas"]), supplier_counts[supplier["vardas"]])
        )

    group_chips = ['<button type="button" class="se-fab__chip is-active" data-filter="group" data-value="all">Visos grupės</button>']
    for group in sorted(groups):
        group_chips.append(
            '<button type="button" class="se-fab__chip" data-filter="group" data-value="%s">%s <span>%d</span></button>'
            % (esc(group), esc(groups[group]["pavadinimas"]), group_counts.get(group, 0))
        )

    # --- korteles ---
    cards = []
    for item in items:
        if with_images:
            media = (
                '<img class="se-fab__img" loading="lazy" decoding="async" '
                'src="%s/%s/%s.webp" alt="Lovos audinys %s (%s, %s)">'
                % (
                    IMG_BASE,
                    item["supplier_slug"],
                    item["slug"],
                    esc(item["name"]),
                    esc(item["supplier"]),
                    esc(groups[item["group"]]["pavadinimas"]),
                )
            )
        else:
            media = '<span class="se-fab__ph" aria-hidden="true">%s</span>' % esc(item["name"][:2])

        cards.append(
            '<li class="se-fab__card" data-supplier="%s" data-group="%s" data-name="%s">'
            '<span class="se-fab__media">%s<span class="se-fab__badge">%s gr.</span></span>'
            '<span class="se-fab__meta"><strong class="se-fab__name">%s</strong>'
            '<span class="se-fab__supplier">%s</span></span></li>'
            % (
                esc(item["supplier"]),
                esc(item["group"]),
                esc(item["name"].lower()),
                media,
                esc(item["group"]),
                esc(item["name"]),
                esc(item["supplier"]),
            )
        )

    group_legend = "".join(
        '<li><strong>%s</strong> — %s</li>' % (esc(groups[g]["pavadinimas"]), esc(groups[g]["aprasymas"]))
        for g in sorted(groups)
    )

    return TEMPLATE % {
        "navy": BRAND_NAVY,
        "lemon": BRAND_LEMON,
        "total": total,
        "supplier_chips": "\n      ".join(supplier_chips),
        "group_chips": "\n      ".join(group_chips),
        "cards": "\n    ".join(cards),
        "group_legend": group_legend,
    }


TEMPLATE = """<!-- Sleeping Expert — lovų audinių katalogas. Generuota: audiniai/build.py. Rankomis neredaguoti. -->
<div class="se-fab" id="se-fab">
  <style>
    .se-fab{--navy:%(navy)s;--lemon:%(lemon)s;--line:#e3e6ef;--muted:#5b6478;
      font-family:inherit;color:var(--navy);max-width:1200px;margin:0 auto}
    .se-fab *{box-sizing:border-box}
    .se-fab__intro{margin:0 0 1.5rem;font-size:1.05rem;line-height:1.6;color:var(--muted)}
    .se-fab__legend{list-style:none;padding:1rem 1.25rem;margin:0 0 1.75rem;border:1px solid var(--line);
      border-radius:12px;background:#f7f8fc;font-size:.92rem;line-height:1.6}
    .se-fab__legend li+li{margin-top:.35rem}
    .se-fab__legend strong{color:var(--navy)}
    .se-fab__controls{display:flex;flex-direction:column;gap:.85rem;margin-bottom:1.5rem}
    .se-fab__search{width:100%%;padding:.75rem 1rem;font-size:1rem;border:1px solid var(--line);
      border-radius:10px;color:var(--navy);background:#fff}
    .se-fab__search:focus{outline:2px solid var(--navy);outline-offset:1px}
    .se-fab__row{display:flex;flex-wrap:wrap;gap:.5rem}
    .se-fab__chip{appearance:none;cursor:pointer;font:inherit;font-size:.85rem;line-height:1;
      padding:.55rem .85rem;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--navy);
      transition:background .15s,border-color .15s}
    .se-fab__chip span{opacity:.55;margin-left:.3rem;font-variant-numeric:tabular-nums}
    .se-fab__chip:hover{border-color:var(--navy)}
    .se-fab__chip.is-active{background:var(--navy);border-color:var(--navy);color:#fff}
    .se-fab__chip.is-active span{opacity:.7}
    .se-fab__count{font-size:.9rem;color:var(--muted);margin:0 0 1rem}
    .se-fab__grid{list-style:none;padding:0;margin:0;display:grid;gap:1rem;
      grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
    .se-fab__card{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;
      display:flex;flex-direction:column}
    .se-fab__card[hidden]{display:none}
    .se-fab__media{position:relative;display:flex;align-items:center;justify-content:center;
      aspect-ratio:4/3;background:#eef0f7}
    .se-fab__img{width:100%%;height:100%%;object-fit:cover;display:block}
    .se-fab__ph{font-size:1.6rem;font-weight:700;letter-spacing:.05em;color:#aab0c4}
    .se-fab__badge{position:absolute;top:.5rem;right:.5rem;background:var(--lemon);color:var(--navy);
      font-size:.72rem;font-weight:700;padding:.2rem .45rem;border-radius:5px}
    .se-fab__meta{padding:.7rem .8rem;display:flex;flex-direction:column;gap:.15rem}
    .se-fab__name{font-size:.92rem;line-height:1.25}
    .se-fab__supplier{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
    .se-fab__empty{padding:2.5rem 1rem;text-align:center;color:var(--muted)}
    .se-fab__empty[hidden]{display:none}
    .se-fab__note{margin:2rem 0 0;padding-top:1.25rem;border-top:1px solid var(--line);
      font-size:.87rem;line-height:1.6;color:var(--muted)}
  </style>

  <p class="se-fab__intro">Mūsų lovas galite užsisakyti su bet kuriuo iš %(total)d audinių. Audiniai suskirstyti į
  keturias grupes — grupė lemia lovos kainą. Rinkitės pagal tiekėją, grupę arba ieškokite pagal pavadinimą.</p>

  <ul class="se-fab__legend">%(group_legend)s</ul>

  <div class="se-fab__controls">
    <label class="screen-reader-text" for="se-fab-search">Ieškoti audinio pagal pavadinimą</label>
    <input class="se-fab__search" id="se-fab-search" type="search" autocomplete="off"
           placeholder="Ieškoti audinio, pvz. VELVET, SORO, MAYA…">
    <div class="se-fab__row" role="group" aria-label="Filtruoti pagal tiekėją">
      %(supplier_chips)s
    </div>
    <div class="se-fab__row" role="group" aria-label="Filtruoti pagal audinių grupę">
      %(group_chips)s
    </div>
  </div>

  <p class="se-fab__count" aria-live="polite" id="se-fab-count">Rodoma %(total)d iš %(total)d audinių</p>

  <ul class="se-fab__grid" id="se-fab-grid">
    %(cards)s
  </ul>

  <p class="se-fab__empty" id="se-fab-empty" hidden>Pagal šiuos kriterijus audinių nerasta. Pabandykite kitą paiešką.</p>

  <p class="se-fab__note">Spalvos ekrane gali skirtis nuo tikrųjų. Prieš užsakant rekomenduojame apžiūrėti
  audinių pavyzdžius mūsų salonuose Vilniuje, Klaipėdoje ar Ukmergėje.</p>
</div>

<script>
(function () {
  var root = document.getElementById('se-fab');
  if (!root || root.dataset.init) return;
  root.dataset.init = '1';

  var cards = Array.prototype.slice.call(root.querySelectorAll('.se-fab__card'));
  var search = document.getElementById('se-fab-search');
  var countEl = document.getElementById('se-fab-count');
  var emptyEl = document.getElementById('se-fab-empty');
  var total = cards.length;
  var state = { supplier: 'all', group: 'all', q: '' };

  function apply() {
    var shown = 0;
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i];
      var ok = (state.supplier === 'all' || card.dataset.supplier === state.supplier) &&
               (state.group === 'all' || card.dataset.group === state.group) &&
               (state.q === '' || card.dataset.name.indexOf(state.q) !== -1);
      card.hidden = !ok;
      if (ok) shown++;
    }
    countEl.textContent = 'Rodoma ' + shown + ' iš ' + total + ' audinių';
    emptyEl.hidden = shown !== 0;
  }

  root.addEventListener('click', function (event) {
    var chip = event.target.closest('.se-fab__chip');
    if (!chip || !root.contains(chip)) return;
    var type = chip.dataset.filter;
    var siblings = root.querySelectorAll('.se-fab__chip[data-filter="' + type + '"]');
    for (var i = 0; i < siblings.length; i++) siblings[i].classList.remove('is-active');
    chip.classList.add('is-active');
    state[type] = chip.dataset.value;
    apply();
  });

  var timer;
  search.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      state.q = search.value.trim().toLowerCase();
      apply();
    }, 120);
  });
})();
</script>
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", action="store_true", help="įjungti swatch nuotraukas")
    args = parser.parse_args()
    html = build(args.images)
    OUT.write_text(html, encoding="utf-8")
    print("Sugeneruota: %s (%d simboliai)" % (OUT, len(html)))
