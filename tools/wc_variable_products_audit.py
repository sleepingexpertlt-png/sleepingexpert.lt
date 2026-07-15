#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WooCommerce variable products auditas + taisymas (sleepingexpert.lt).

Tikrina kiekvieną variable produktą:
  1. Ar atributai globalūs (id > 0), ne Custom
  2. Ar atributas pažymėtas "variation": true
  3. Ar sukurtos variacijos ir ar jos turi kainas
  4. Ar variacijų atributų reikšmės ne tuščios ("Any...")
  5. Ar atributų reikšmės lietuviškos (ne angliškos)
  6. (--test-cart) Ar variacijos dedasi į krepšelį be kritinės klaidos (Store API)

SAUGUMO TAISYKLĖS:
  - NIEKO NEŠALINA. Jokio DELETE. Tik PUT/POST esamiems atributams/variacijoms.
  - Be --fix veikia tik skaitymo režimu (dry-run) ir tik spausdina ataskaitą.
  - Su --fix prieš KIEKVIENĄ produkto pakeitimą klausia patvirtinimo [y/N].
  - Variacijų be kainos NETAISO automatiškai — tik praneša (kainą turi įvesti žmogus).

Paleidimas serveryje (kur yra config/secrets.env):
  python3 tools/wc_variable_products_audit.py                 # auditas (dry-run)
  python3 tools/wc_variable_products_audit.py --test-cart     # + krepšelio testas
  python3 tools/wc_variable_products_audit.py --fix           # taisymas su patvirtinimais

Autentifikacija: consumer_key/consumer_secret kaip URL parametrai
(Hostinger blokuoja Basic Auth antraštes — žr. lessons L654).
secrets.env skaitomas tiesiogiai, ne per `source` (žr. lessons L651).
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Trūksta 'requests': pip3 install requests")

BASE_URL = "https://sleepingexpert.lt"
API = f"{BASE_URL}/wp-json/wc/v3"
STORE_API = f"{BASE_URL}/wp-json/wc/store/v1"
TIMEOUT = 40

# Dažniausios angliškos atributų reikšmės/pavadinimai, kurie turi būti lietuviški
ENGLISH_WORDS = {
    "size", "color", "colour", "material", "firmness", "height", "width",
    "small", "medium", "large", "extra large", "soft", "hard", "firm",
    "white", "black", "grey", "gray", "brown", "blue", "green", "red",
    "yellow", "beige", "natural", "oak", "walnut", "left", "right",
    "with", "without", "yes", "no", "default", "standard",
}


def load_secrets():
    """Skaito config/secrets.env tiesiogiai (L651: source metodas neveikia)."""
    candidates = [
        Path("config/secrets.env"),
        Path(__file__).resolve().parent.parent / "config" / "secrets.env",
        Path.home() / "hermes" / "config" / "secrets.env",
    ]
    env = {}
    for p in candidates:
        if p.is_file():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip().strip('"').strip("'")
            break
    key = env.get("WC_CONSUMER_KEY")
    secret = env.get("WC_CONSUMER_SECRET")
    if not key or not secret:
        sys.exit("Nerasti WC_CONSUMER_KEY/WC_CONSUMER_SECRET config/secrets.env faile.")
    return key, secret


class WC:
    def __init__(self, key, secret):
        self.auth = {"consumer_key": key, "consumer_secret": secret}
        self.s = requests.Session()

    def get_all(self, path, **params):
        """Puslapiuotas GET — surenka visus įrašus."""
        out, page = [], 1
        while True:
            p = dict(self.auth, per_page=100, page=page, **params)
            r = self.s.get(f"{API}{path}", params=p, timeout=TIMEOUT)
            r.raise_for_status()
            batch = r.json()
            out.extend(batch)
            if len(batch) < 100:
                return out
            page += 1

    def get(self, path, **params):
        r = self.s.get(f"{API}{path}", params=dict(self.auth, **params), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    def put(self, path, payload):
        r = self.s.put(f"{API}{path}", params=self.auth, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    def post(self, path, payload):
        r = self.s.post(f"{API}{path}", params=self.auth, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()


def looks_english(value):
    v = value.strip().lower()
    if not v:
        return False
    if v in ENGLISH_WORDS:
        return True
    # atskiri žodžiai reikšmėje, pvz. "Extra Hard 90x200"
    words = re.findall(r"[a-ząčęėįšųūž]+", v)
    return any(w in ENGLISH_WORDS for w in words)


def audit_product(wc, product):
    """Grąžina (issues, variations). issue = (klaida, kaip_taisyti, fix_dict|None)."""
    issues = []
    pid = product["id"]
    attrs = product.get("attributes", [])

    variation_attrs = [a for a in attrs if a.get("variation")]

    if not attrs:
        issues.append(("Produktas variable, bet neturi jokių atributų",
                       "Sukurti globalų atributą (pvz. pa_dydis) ir pažymėti 'Used for variations'",
                       None))

    for a in attrs:
        name = a.get("name", "?")
        # 1. Custom vs globalus
        if a.get("id", 0) == 0:
            issues.append((f"Atributas „{name}“ yra Custom (id=0), ne globalus",
                           f"Konvertuoti į globalų pa_ atributą (--fix tai padarys automatiškai)",
                           {"type": "custom_attr", "attr": a}))
        # 2. variation flag
        if not a.get("variation"):
            issues.append((f"Atributas „{name}“ nepažymėtas 'Used for variations' (variation=false)",
                           "Pažymėti variation=true (--fix tai padarys automatiškai)",
                           {"type": "variation_flag", "attr": a}))
        # 5. angliškos reikšmės
        eng = [o for o in a.get("options", []) if looks_english(o)]
        if looks_english(name):
            issues.append((f"Atributo pavadinimas „{name}“ angliškas",
                           "Pervadinti lietuviškai (pvz. Size→Dydis, Color→Spalva) WP admin → Products → Attributes",
                           None))
        if eng:
            issues.append((f"Angliškos atributo „{name}“ reikšmės: {', '.join(eng)}",
                           "Išversti reikšmes į lietuvių k. (terminų puslapyje keisti name, paliekant slug)",
                           None))

    # 3. Variacijos ir kainos
    try:
        variations = wc.get_all(f"/products/{pid}/variations")
    except requests.HTTPError as e:
        issues.append((f"Nepavyko gauti variacijų: {e}", "Patikrinti produktą rankiniu būdu", None))
        return issues, []

    if not variations:
        issues.append(("Variable produktas be sukurtų variacijų",
                       "WP admin → produktas → Variations → 'Create variations from all attributes', tada įvesti kainas",
                       None))

    attr_options = {a["name"].lower(): a.get("options", []) for a in variation_attrs}

    for v in variations:
        vid = v["id"]
        # kaina
        if not (v.get("regular_price") or v.get("price")):
            label = ", ".join(f"{x.get('name')}: {x.get('option') or 'Any'}" for x in v.get("attributes", [])) or f"#{vid}"
            issues.append((f"Variacija #{vid} ({label}) BE KAINOS — dėl to gali lūžti krepšelis",
                           "ĮVESTI KAINĄ rankiniu būdu (skriptas kainų nekuria)",
                           None))
        # 4. tušti slugs ("Any")
        v_attr_names = {x.get("name", "").lower() for x in v.get("attributes", []) if x.get("option")}
        for a in variation_attrs:
            an = a["name"].lower()
            if an not in v_attr_names:
                opts = attr_options.get(an, [])
                fix = None
                if len(opts) == 1:
                    fix = {"type": "any_slug", "variation_id": vid, "attr": a, "option": opts[0]}
                    how = f"Priskirti vienintelę galimą reikšmę „{opts[0]}“ (--fix tai padarys)"
                else:
                    how = f"Priskirti konkrečią reikšmę iš: {', '.join(opts) or '—'} (reikia pasirinkti rankiniu būdu)"
                issues.append((f"Variacijos #{vid} atributas „{a['name']}“ tuščias (Any)", how, fix))
        # angliškos reikšmės variacijoje
        for x in v.get("attributes", []):
            if x.get("option") and looks_english(x["option"]):
                issues.append((f"Variacijos #{vid} reikšmė angliška: {x['name']}={x['option']}",
                               "Išversti termino pavadinimą į lietuvių k.", None))

    return issues, variations


def test_cart(product, variations):
    """Bando įdėti pirmą perkamą variaciją į krepšelį per Store API. Grąžina issue arba None."""
    target = None
    for v in variations:
        if v.get("purchasable") and (v.get("price") or v.get("regular_price")):
            target = v
            break
    if target is None:
        return ("Krepšelio testas praleistas — nėra perkamos variacijos su kaina",
                "Pirmiausia sutvarkyti variacijas/kainas", None)
    s = requests.Session()
    try:
        r0 = s.get(f"{STORE_API}/cart", timeout=TIMEOUT)
        nonce = r0.headers.get("Nonce") or r0.headers.get("X-WC-Store-API-Nonce", "")
        r = s.post(f"{STORE_API}/cart/add-item",
                   headers={"Nonce": nonce},
                   json={"id": target["id"], "quantity": 1},
                   timeout=TIMEOUT)
        if r.status_code >= 500:
            snippet = re.sub(r"<[^>]+>", " ", r.text)[:300].strip()
            return (f"KRITINĖ KLAIDA dedant variaciją #{target['id']} į krepšelį (HTTP {r.status_code}): {snippet}",
                    "Įjungti WP_DEBUG_LOG, pakartoti ir žiūrėti wp-content/debug.log — dažniausia priežastis: "
                    "variacija be kainos, „našlaitė“ variacija arba temos/plugino hook'as ant woocommerce_add_to_cart",
                    None)
        if r.status_code >= 400:
            err = r.json().get("message", r.text[:200]) if r.text else ""
            return (f"Variacijos #{target['id']} nepavyko įdėti į krepšelį (HTTP {r.status_code}): {err}",
                    "Patikrinti variacijos atributus/kainą — Store API atmeta nepilnas variacijas",
                    None)
    except requests.RequestException as e:
        return (f"Krepšelio testas nepavyko techniškai: {e}", "Pakartoti testą iš serverio", None)
    return None


# ---------------------------------------------------------------- taisymai

def confirm(prompt):
    try:
        return input(f"{prompt} [y/N]: ").strip().lower() in ("y", "yes", "t", "taip")
    except EOFError:
        return False


def ensure_global_attribute(wc, name, cache):
    """Randa arba sukuria globalų atributą pagal pavadinimą. Grąžina jo id."""
    if not cache:
        cache.extend(wc.get_all("/products/attributes"))
    slug_want = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    for a in cache:
        if a["name"].lower() == name.lower() or a["slug"] in (f"pa_{slug_want}", slug_want):
            return a["id"]
    created = wc.post("/products/attributes", {"name": name})
    cache.append(created)
    print(f"  + Sukurtas globalus atributas „{name}“ (id={created['id']})")
    return created["id"]


def ensure_terms(wc, attr_id, options):
    """Sukuria trūkstamus terminus. Grąžina {option_lower: term_name}."""
    existing = wc.get_all(f"/products/attributes/{attr_id}/terms")
    have = {t["name"].lower(): t["name"] for t in existing}
    out = {}
    for o in options:
        if o.lower() in have:
            out[o.lower()] = have[o.lower()]
        else:
            t = wc.post(f"/products/attributes/{attr_id}/terms", {"name": o})
            out[o.lower()] = t["name"]
            print(f"  + Sukurtas terminas „{o}“")
    return out


def fix_product(wc, product, issues, attr_cache):
    """Taiso tai, ką galima saugiai: custom→global, variation flag, Any slug.
    NIEKO NEŠALINA — visada siunčia pilną atributų sąrašą."""
    pid = product["id"]
    fixes = [i[2] for i in issues if i[2]]
    if not fixes:
        return

    print(f"\n=== {product['name']} (ID {pid}) — siūlomi taisymai:")
    for _, (klaida, kaip, fx) in enumerate((i for i in issues if i[2]), 1):
        print(f"  - {klaida} → {kaip}")
    if not confirm(f"Taisyti produktą {pid}?"):
        print("  Praleista.")
        return

    attrs = product.get("attributes", [])
    changed = False
    custom_map = {}  # custom attr name(lower) -> (new_id, {opt_lower: term_name})

    for fx in fixes:
        if fx["type"] == "custom_attr":
            a = fx["attr"]
            new_id = ensure_global_attribute(wc, a["name"], attr_cache)
            term_map = ensure_terms(wc, new_id, a.get("options", []))
            custom_map[a["name"].lower()] = (new_id, term_map)
            for x in attrs:
                if x.get("id", 0) == 0 and x["name"].lower() == a["name"].lower():
                    x["id"] = new_id
                    x["variation"] = True
                    x["visible"] = x.get("visible", True)
                    x["options"] = [term_map.get(o.lower(), o) for o in x.get("options", [])]
            changed = True
        elif fx["type"] == "variation_flag":
            for x in attrs:
                if x["name"].lower() == fx["attr"]["name"].lower():
                    x["variation"] = True
            changed = True

    if changed:
        wc.put(f"/products/{pid}", {"attributes": attrs})
        print(f"  ✓ Atnaujinti produkto {pid} atributai (nieko nepašalinta)")

    # Variacijų atnaujinimas: custom→global pavadinimų perrašymas + Any slug
    if custom_map or any(f["type"] == "any_slug" for f in fixes):
        variations = wc.get_all(f"/products/{pid}/variations")
        any_fixes = {f["variation_id"]: f for f in fixes if f["type"] == "any_slug"}
        for v in variations:
            v_attrs = v.get("attributes", [])
            v_changed = False
            for x in v_attrs:
                key = x.get("name", "").lower()
                if key in custom_map:
                    new_id, term_map = custom_map[key]
                    x["id"] = new_id
                    if x.get("option"):
                        x["option"] = term_map.get(x["option"].lower(), x["option"])
                    v_changed = True
            fx = any_fixes.get(v["id"])
            if fx:
                name_l = fx["attr"]["name"].lower()
                hit = next((x for x in v_attrs if x.get("name", "").lower() == name_l), None)
                if hit is not None:
                    hit["option"] = fx["option"]
                else:
                    entry = {"name": fx["attr"]["name"], "option": fx["option"]}
                    if fx["attr"].get("id"):
                        entry["id"] = fx["attr"]["id"]
                    v_attrs.append(entry)
                v_changed = True
            if v_changed:
                wc.put(f"/products/{pid}/variations/{v['id']}", {"attributes": v_attrs})
                print(f"  ✓ Atnaujinta variacija #{v['id']}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="WooCommerce variable produktų auditas")
    ap.add_argument("--fix", action="store_true", help="taisyti su patvirtinimu (kitaip tik ataskaita)")
    ap.add_argument("--test-cart", action="store_true", help="testuoti dėjimą į krepšelį per Store API")
    ap.add_argument("--json", metavar="FILE", help="išsaugoti pilną ataskaitą JSON failu")
    args = ap.parse_args()

    key, secret = load_secrets()
    wc = WC(key, secret)

    print("Renkami variable produktai...", file=sys.stderr)
    products = wc.get_all("/products", type="variable", status="publish")
    print(f"Rasta variable produktų: {len(products)}", file=sys.stderr)

    rows, report, attr_cache = [], [], []
    for p in products:
        issues, variations = audit_product(wc, p)
        if args.test_cart:
            cart_issue = test_cart(p, variations)
            if cart_issue:
                issues.append(cart_issue)
        for klaida, kaip, _ in issues:
            rows.append((p["name"], p["id"], klaida, kaip))
        report.append({"id": p["id"], "name": p["name"],
                       "issues": [{"klaida": k, "kaip_taisyti": h} for k, h, _ in issues]})
        if args.fix and any(i[2] for i in issues):
            fix_product(wc, p, issues, attr_cache)

    print("\n| Produkto pavadinimas | ID | Klaida | Kaip taisyti |")
    print("|---|---|---|---|")
    if rows:
        for name, pid, klaida, kaip in rows:
            print(f"| {name} | {pid} | {klaida} | {kaip} |")
    else:
        print("| — | — | Klaidų nerasta | — |")

    print(f"\nProduktų: {len(products)}, problemų: {len(rows)}")
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON ataskaita: {args.json}")


if __name__ == "__main__":
    main()
