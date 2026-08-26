#!/usr/bin/env python3
"""Įkelia paruoštą SEO turinį į WooCommerce produktą (vaikiška lova Teddy, ID 24351).

Naudoja tik standartinę biblioteką — jokių priklausomybių diegti nereikia.

Paruošimas (vieną kartą):
  WooCommerce → Settings → Advanced → REST API → Add key
    Description: seo-update
    Permissions: Read/Write
  Nusikopijuok Consumer key ir Consumer secret.

Naudojimas:
  export WC_KEY=ck_xxxxxxxx
  export WC_SECRET=cs_xxxxxxxx
  python3 scripts/wp-update-teddy.py            # peržiūra, nieko nekeičia
  python3 scripts/wp-update-teddy.py --apply    # įrašo

Papildomos vėliavėlės:
  --keep-slug     nekeisti slug'o (jei senasis URL jau indeksuotas ir 301 dar nepadarytas)
  --id 24351      kitas produkto ID
  --url https://... kitas svetainės adresas
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "docs" / "seo" / "teddy"

NAME = "Vaikiška lova Teddy"
SLUG = "vaikiska-lova-teddy"
SEO_TITLE = "Vaikiška lova Teddy – minkšta lova su patalynės dėže"
SEO_DESC = (
    "Vaikiška lova Teddy – minkštas modulinis galvūgalis, 7 Sandu audinio spalvos "
    "ir variantas su patalynės dėže. Gaminama Lenkijoje, 3 metų garantija."
)
FOCUS_KW = "vaikiška lova Teddy"


def request(method, url, key, secret, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    token = base64.b64encode(f"{key}:{secret}".encode("utf-8")).decode("ascii")
    req.add_header("Authorization", f"Basic {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "seo-update/1.0")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:800]
        sys.exit(f"KLAIDA {e.code} {method} {url}\n{body}")
    except urllib.error.URLError as e:
        sys.exit(f"Nepavyko prisijungti prie {url}: {e.reason}")


def meta_value(product, key):
    for m in product.get("meta_data", []):
        if m.get("key") == key:
            return m.get("value")
    return None


def preview(label, old, new, limit=90):
    def cut(v):
        v = "" if v is None else str(v).replace("\n", " ")
        return v[:limit] + ("…" if len(v) > limit else "")
    mark = "=" if old == new else "→"
    print(f"  {label}")
    print(f"    dabar : {cut(old)}")
    print(f"    {mark} nauja: {cut(new)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="įrašyti pakeitimus")
    ap.add_argument("--keep-slug", action="store_true", help="nekeisti slug'o")
    ap.add_argument("--id", type=int, default=24351)
    ap.add_argument("--url", default=os.environ.get("WC_URL", "https://sleepingexpert.lt"))
    args = ap.parse_args()

    key = os.environ.get("WC_KEY")
    secret = os.environ.get("WC_SECRET")
    if not key or not secret:
        sys.exit("Trūksta WC_KEY / WC_SECRET aplinkos kintamųjų. Žr. komentarą failo viršuje.")

    for f in ("description.html", "short-description.html"):
        if not (CONTENT / f).exists():
            sys.exit(f"Nerastas turinio failas: {CONTENT / f}")

    description = (CONTENT / "description.html").read_text(encoding="utf-8").strip()
    short_description = (CONTENT / "short-description.html").read_text(encoding="utf-8").strip()

    base = args.url.rstrip("/")
    endpoint = f"{base}/wp-json/wc/v3/products/{args.id}"

    print(f"Skaitau produktą {args.id} iš {base} …")
    current = request("GET", endpoint, key, secret)
    print(f"Rastas: „{current.get('name')}“  (slug: {current.get('slug')}, statusas: {current.get('status')})\n")

    payload = {
        "name": NAME,
        "description": description,
        "short_description": short_description,
        "meta_data": [
            {"key": "rank_math_title", "value": SEO_TITLE},
            {"key": "rank_math_description", "value": SEO_DESC},
            {"key": "rank_math_focus_keyword", "value": FOCUS_KW},
        ],
    }
    if not args.keep_slug:
        payload["slug"] = SLUG

    print("Keitimai:")
    preview("Pavadinimas", current.get("name"), NAME)
    if not args.keep_slug:
        preview("Slug", current.get("slug"), SLUG)
    else:
        print("  Slug — praleidžiama (--keep-slug)")
    preview("SEO title", meta_value(current, "rank_math_title"), SEO_TITLE)
    preview("Meta description", meta_value(current, "rank_math_description"), SEO_DESC)
    preview("Focus keyword", meta_value(current, "rank_math_focus_keyword"), FOCUS_KW)
    print(f"  Trumpas aprašymas: {len(current.get('short_description') or '')} → {len(short_description)} simb.")
    print(f"  Pilnas aprašymas : {len(current.get('description') or '')} → {len(description)} simb.")

    if not args.apply:
        print("\nPeržiūros režimas — niekas nepakeista. Įrašyti: pridėk --apply")
        return

    old_slug = current.get("slug")
    print("\nĮrašoma …")
    updated = request("PUT", endpoint, key, secret, payload)
    print(f"✔ Atnaujinta: {updated.get('permalink')}")

    check = request("GET", endpoint, key, secret)
    ok = True
    for label, got, want in (
        ("pavadinimas", check.get("name"), NAME),
        ("SEO title", meta_value(check, "rank_math_title"), SEO_TITLE),
        ("meta description", meta_value(check, "rank_math_description"), SEO_DESC),
    ):
        if got != want:
            ok = False
            print(f"⚠ {label} neįsirašė kaip tikėtasi — patikrink rankiniu būdu WP admin'e.")
    if ok:
        print("✔ Patikrinta: pavadinimas ir Rank Math laukai įrašyti.")

    if not args.keep_slug and old_slug and old_slug != SLUG:
        print(f"\n⚠ Slug pakeistas: {old_slug} → {SLUG}")
        print("   Jei senasis URL buvo indeksuotas, padaryk 301 nukreipimą (Rank Math → Redirections).")

    print("\nLikę rankiniai darbai (REST API jų nedaro):")
    print("  · nuotraukų ALT tekstai — Media Library")
    print("  · SKU unikalumas, kaina, matmenys, variantai")
    print("  · kategorijos ir žymos, paveldėtos iš kopijos")
    print("  · FAQ schema — Rank Math FAQ blokas")


if __name__ == "__main__":
    main()
