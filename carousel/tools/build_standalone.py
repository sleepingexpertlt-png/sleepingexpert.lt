#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sukuria VIENA HTML faila, kuriame yra viskas: stilius, logika, duomenys ir nuotraukos.

Toks failas veikia be serverio ir be interneto — uztenka ji atidaryti narsykle
(dukart spustelejus) arba nusikopijuoti i USB atmintuka ir paleisti ant TV / stendo.

    python3 tools/build_standalone.py
    python3 tools/build_standalone.py --limit 40 --out dist/karusele.html
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLAYER = os.path.join(ROOT, "player")
DATA = os.path.join(ROOT, "data")

mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/avif", ".avif")


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def as_data_uri(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as fh:
        return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Vieno failo (offline) karuseles versija")
    parser.add_argument("--out", default=os.path.join(ROOT, "dist", "karusele.html"))
    parser.add_argument("--limit", type=int, default=0, help="kiek prekiu itraukti (0 = visos)")
    parser.add_argument("--only-sale", action="store_true", help="itraukti tik akcijines prekes")
    parser.add_argument("--data", default=None,
                        help="duomenu katalogas (numatyta: data/); naudinga, kai keli klientai")
    args = parser.parse_args()

    global DATA
    if args.data:
        DATA = args.data if os.path.isabs(args.data) else os.path.join(ROOT, args.data)

    products_path = os.path.join(DATA, "products.json")
    if not os.path.exists(products_path):
        print("! Nerasta data/products.json — pirmiausia paleisk: python3 fetch_products.py")
        return 2

    payload = json.load(open(products_path, encoding="utf-8"))
    display_path = os.path.join(DATA, "display.json")
    display = json.load(open(display_path, encoding="utf-8")) if os.path.exists(display_path) else {}

    products = payload.get("products", [])
    if args.only_sale:
        products = [p for p in products if p.get("on_sale")]
    if args.limit:
        products = products[: args.limit]

    embedded, skipped, total_bytes = [], 0, 0
    for product in products:
        item = dict(product)
        rel = item.get("image") or ""
        if rel and not rel.startswith(("http://", "https://", "data:")):
            uri = as_data_uri(os.path.join(DATA, rel))
            if not uri:
                skipped += 1
                continue
            item["image"] = uri
            total_bytes += len(uri)
        item.pop("image_remote", None)
        embedded.append(item)

    if not embedded:
        print("! Neliko nei vienos prekes su nuotrauka.")
        return 3

    payload = dict(payload)
    payload["products"] = embedded
    payload["counts"] = {
        "total": len(embedded),
        "on_sale": len([p for p in embedded if p.get("on_sale")]),
        "max_discount": max([p.get("discount_percent", 0) for p in embedded] or [0]),
    }

    html = read(os.path.join(PLAYER, "index.html"))
    css = read(os.path.join(PLAYER, "style.css"))
    qr_js = read(os.path.join(PLAYER, "qr.js"))
    app_js = read(os.path.join(PLAYER, "app.js"))

    favicon = as_data_uri(os.path.join(PLAYER, "favicon.svg")) or ""
    html = html.replace('<link rel="icon" href="favicon.svg" type="image/svg+xml">',
                        '<link rel="icon" href="%s">' % favicon)
    html = html.replace('<link rel="stylesheet" href="style.css">',
                        "<style>\n%s\n</style>" % css)

    blob = json.dumps({"products": payload, "display": display}, ensure_ascii=False)
    blob = blob.replace("</", "<\\/")  # kad neuzdarytu <script> zymos
    html = html.replace(
        '<script src="qr.js"></script>',
        "<script>window.__SE_DATA__ = %s;</script>\n  <script>\n%s\n</script>" % (blob, qr_js))
    html = html.replace('<script src="app.js"></script>', "<script>\n%s\n</script>" % app_js)

    out_path = args.out
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print("Sukurta: %s" % out_path)
    print("  prekes: %d (akcijoje %d)%s" % (
        len(embedded), payload["counts"]["on_sale"],
        ", praleista be nuotraukos: %d" % skipped if skipped else ""))
    print("  dydis:  %.1f MB" % size_mb)
    if size_mb > 60:
        print("  ! Failas didelis — apriboti galima su --limit arba --only-sale")
    print("Atidaryk ji narsykle (dukart spustelejus) — interneto nereikia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
