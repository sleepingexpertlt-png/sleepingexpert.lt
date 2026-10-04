#!/usr/bin/env python3
"""Realūs produktai reklaminiams blokams sapnų straipsniuose (iš VPS, viešas WC Store API, be auth).

    python3 scripts/sapnai/fetch_products.py            # → data/sapnu-reiksmes/products.json

Ima po kelis produktus iš kategorijų pagalves, ciuziniai, antklodes, miego-aksesuarai (pavadinimas,
nuoroda, nuotrauka – be kainų, nes kainos keičiasi). build.py šį failą naudoja, jei jis yra;
jei nėra – rodo kategorijų korteles. Užklausos retinamos (2026-09-08 pamoka: bulk be pauzės = 429).
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "data", "sapnu-reiksmes", "products.json")
SITE = os.getenv("WP_URL", "https://sleepingexpert.lt").rstrip("/").split("/wp-json")[0]
STORE = f"{SITE}/wp-json/wc/store/v1"
WANT = {"pagalves": 6, "ciuziniai": 6, "antklodes": 4, "miego-aksesuarai": 4}


def get(path: str, **params):
    url = f"{STORE}/{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"User-Agent": "se-sapnai/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    time.sleep(1.0)
    return data


def main() -> int:
    cats = {}
    page = 1
    while True:
        batch = get("products/categories", per_page=100, page=page)
        if not batch:
            break
        for c in batch:
            cats[c["slug"]] = c
        if len(batch) < 100:
            break
        page += 1
    result = {}
    for slug, n in WANT.items():
        cat = cats.get(slug)
        if not cat:
            print(f"⚠️ kategorija nerasta: {slug} (yra: {', '.join(sorted(cats)[:30])}…)")
            continue
        prods = get("products", category=cat["id"], per_page=n, orderby="popularity")
        result[slug] = [{"name": p["name"], "permalink": p["permalink"],
                         "image": (p.get("images") or [{}])[0].get("thumbnail") or (p.get("images") or [{}])[0].get("src", "")}
                        for p in prods if p.get("permalink", "").startswith(SITE + "/parduotuve/")]
        print(f"{slug}: {len(result[slug])} produktai")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("→", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
