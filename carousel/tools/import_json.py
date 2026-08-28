#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sukuria products.json is jau turimo WooCommerce Store API atsakymo (JSON failo).

Kam to reikia: kartais ekrano masina ar aplinka negali tiesiogiai pasiekti
svetaines (uzkarda, izoliuotas tinklas). Tada Store API atsakyma galima issaugoti
kitur ir importuoti cia — normalizavimas, filtrai ir rusiavimas identiski
`fetch_products.py`.

    curl -s "https://parduotuve.lt/wp-json/wc/store/v1/products?per_page=100" > raw.json
    python3 tools/import_json.py --config profiles/cookking.json --input raw.json

Nuotraukos: jei `data-*/images/` jau yra failas su prekes ID pradzioje, naudojamas
jis (veikia be interneto); kitu atveju paliekama tiesiogine nuoroda i svetaine.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from fetch_products import (  # noqa: E402
    DEFAULT_CONFIG, apply_filters, load_config, normalize_store, slugify,
    sort_products, write_json,
)


def find_local_image(img_dir: str, product: dict) -> str | None:
    """Suranda jau parsisiusta nuotrauka pagal prekes ID priesaga."""
    if not os.path.isdir(img_dir):
        return None
    prefix = "%s-" % product.get("id")
    for fname in sorted(os.listdir(img_dir)):
        if fname.startswith(prefix):
            return "images/" + fname
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Store API JSON -> karuseles products.json")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--input", action="append", required=True,
                        help="Store API atsakymo failas (galima nurodyti kelis kartus)")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only-sale", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.only_sale:
        cfg["only_on_sale"] = True
    if args.limit:
        cfg["max_products"] = args.limit

    out_dir = cfg["output_dir"]
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(ROOT, out_dir)
    os.makedirs(out_dir, exist_ok=True)
    img_dir = os.path.join(out_dir, "images")

    raw_items, seen = [], set()
    for path in args.input:
        with open(path, "r", encoding="utf-8") as fh:
            batch = json.load(fh)
        if isinstance(batch, dict):
            batch = batch.get("products") or [batch]
        for item in batch:
            if item.get("id") in seen:
                continue
            seen.add(item.get("id"))
            raw_items.append(item)
    print("Nuskaityta %d unikaliu irasu is %d failu" % (len(raw_items), len(args.input)))

    products = [p for p in (normalize_store(item, cfg) for item in raw_items) if p]
    products = apply_filters(products, cfg)
    products = sort_products(products, cfg.get("sort", "discount"))
    products = products[: int(cfg.get("max_products", 120))]

    local, remote = 0, 0
    for product in products:
        found = find_local_image(img_dir, product)
        if found:
            product["image"] = found
            local += 1
        else:
            product["image"] = product.get("image_remote") or ""
            remote += 1

    if not products:
        print("! Neliko nei vienos prekes — failai nekeiciami.")
        return 3

    on_sale = [p for p in products if p.get("on_sale")]
    payload = {
        "generated_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).isoformat(timespec="seconds"),
        "source": "import-json",
        "site": (cfg.get("site_url") or "").rstrip("/"),
        "counts": {
            "total": len(products),
            "on_sale": len(on_sale),
            "max_discount": max([p["discount_percent"] for p in on_sale], default=0),
        },
        "products": products,
    }
    write_json(os.path.join(out_dir, "products.json"), payload)
    write_json(os.path.join(out_dir, "display.json"), cfg["display"])
    print("Irasyta: %s" % os.path.join(out_dir, "products.json"))
    print("  prekes: %d (akcijoje %d) | nuotraukos: %d vietines, %d nuotolines"
          % (len(products), len(on_sale), local, remote))
    return 0


if __name__ == "__main__":
    sys.exit(main())
