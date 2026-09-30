#!/usr/bin/env python3
"""
Sleeping Expert product feed generator for Lithuanian price-comparison portals
(kainos1.lt, kainos.lt, kaina24.lt ...).

Reads the PUBLIC WooCommerce Store API (no credentials needed) and writes:
  <out>/kainos-google.xml  Google Shopping RSS 2.0 (g: namespace)
  <out>/kainos.xml         flat <products><product> XML

It does NOT touch the existing Google Merchant Center feed
(/feeds/google-shopping-feed.xml, generate_merchant_feed.py) — separate files.

Usage (on the VPS, e.g. daily cron):
  python3 scripts/generate_kainos_feed.py --out /var/www/html/feeds
Offline / debugging with cached Store API JSON pages:
  python3 scripts/generate_kainos_feed.py --pages-dir se-pages --out ./out

Cached layout: <pages-dir>/page1.json ... pageN.json (products?per_page=100&page=N)
               <pages-dir>/variations/<parent_id>.json (products?type=variation&parent=ID)
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

SHOP_URL = "https://sleepingexpert.lt"
SHOP_NAME = "Sleeping Expert"
API = SHOP_URL + "/wp-json/wc/store/v1/products"
DEFAULT_BRAND = "Sleeping Expert"
CATEGORY_ROOT = "Sleeping Expert"

# Google product taxonomy by top-level category slug
GOOGLE_CATEGORY = {
    "lovos": "Furniture > Beds & Accessories > Beds & Bed Frames",
    "ciuziniai": "Furniture > Beds & Accessories > Mattresses",
    "antciuziniai": "Furniture > Beds & Accessories > Mattress Toppers",
    "pagalves": "Home & Garden > Linens & Bedding > Bedding > Pillows",
    "antklodes": "Home & Garden > Linens & Bedding > Bedding > Blankets",
    "lovos-groteles": "Furniture > Beds & Accessories > Bed Frames",
    "baldai": "Furniture",
}
GOOGLE_CATEGORY_DEFAULT = "Furniture > Beds & Accessories"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "SE-kainos-feed/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def load_products(pages_dir):
    products = []
    if pages_dir:
        i = 1
        while True:
            p = os.path.join(pages_dir, f"page{i}.json")
            if not os.path.exists(p):
                break
            products += json.load(open(p, encoding="utf-8"))
            i += 1
    else:
        page = 1
        while True:
            batch = fetch_json(f"{API}?per_page=100&page={page}")
            if not batch:
                break
            products += batch
            page += 1
    return products


def load_variations(parent_id, pages_dir):
    if pages_dir:
        p = os.path.join(pages_dir, "variations", f"{parent_id}.json")
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
    try:
        return fetch_json(f"{API}?type=variation&parent={parent_id}&per_page=100")
    except Exception as e:  # keep the parent entry instead of failing the whole feed
        print(f"WARN variations {parent_id}: {e}", file=sys.stderr)
        return None


def clean_text(s):
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def xml_escape(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&apos;"))


def money(minor, unit):
    return f"{int(minor) / (10 ** int(unit)):.2f}"


def category_path(product, slug_to_name):
    """Deepest category as 'Root > Sub > Leaf' using the category link hierarchy."""
    best = []
    for c in product.get("categories", []):
        slug_to_name[c["slug"]] = html.unescape(c["name"])
        m = re.search(r"/produkto-kategorija/(.+?)/?$", c.get("link", ""))
        chain = m.group(1).split("/") if m else [c["slug"]]
        if len(chain) > len(best):
            best = chain
    return best


def attr_term(product, name):
    for a in product.get("attributes", []):
        if a.get("name") == name and a.get("terms"):
            return html.unescape(a["terms"][0]["name"])
    return ""


def build_items(products, pages_dir):
    slug_to_name = {}
    for p in products:  # first pass so every slug has a name
        for c in p.get("categories", []):
            slug_to_name[c["slug"]] = html.unescape(c["name"])

    items = []
    skipped = {"no_image": 0, "no_category": 0, "zero_price": 0, "not_purchasable": 0}

    for p in products:
        if not p.get("images"):
            skipped["no_image"] += 1
            continue
        if not p.get("categories"):  # services like "Įnešimas + surinkimas"
            skipped["no_category"] += 1
            continue
        if not p.get("is_purchasable", True):
            skipped["not_purchasable"] += 1
            continue

        chain = category_path(p, slug_to_name)
        cat_names = [slug_to_name.get(s, s) for s in chain]
        category = " > ".join([CATEGORY_ROOT] + cat_names)
        google_cat = GOOGLE_CATEGORY.get(chain[0] if chain else "", GOOGLE_CATEGORY_DEFAULT)
        brand = (p.get("brands") or [{}])[0].get("name") or attr_term(p, "Gamintojas") or DEFAULT_BRAND
        delivery_time = attr_term(p, "Pristatymo laikas")
        description = clean_text(p.get("short_description") or p.get("description"))[:5000]
        title = clean_text(p["name"])
        images = [im["src"] for im in p["images"]]

        def entry(src, vid, gid, vtitle, link, vimages, sku):
            pr = src["prices"]
            unit = pr.get("currency_minor_unit", 2)
            price = money(pr["price"], unit)
            regular = money(pr["regular_price"], unit)
            if float(price) <= 0:
                skipped["zero_price"] += 1
                return None
            return {
                "id": str(vid), "group_id": str(gid), "title": vtitle,
                "description": description, "link": link,
                "image": vimages[0], "additional_images": vimages[1:10],
                "price": price, "regular_price": regular,
                "on_sale": bool(src.get("on_sale")) and float(regular) > float(price),
                "available": bool(src.get("is_in_stock", True)),
                "brand": html.unescape(brand), "sku": sku or "",
                "category": category, "google_category": google_cat,
                "weight_kg": src.get("weight") or "", "delivery_time": delivery_time,
            }

        variations = load_variations(p["id"], pages_dir) if p.get("type") == "variable" else None
        if variations:
            for v in variations:
                vt = clean_text(v.get("variation") or "")
                vtitle = f"{title} — {vt}" if vt else title
                vimages = [im["src"] for im in v.get("images") or []] or images
                e = entry(v, v["id"], p["id"], vtitle, v.get("permalink") or p["permalink"], vimages, v.get("sku"))
                if e:
                    items.append(e)
        else:
            e = entry(p, p["id"], p["id"], title, p["permalink"], images, p.get("sku"))
            if e:
                items.append(e)

    return items, skipped


def write_google(items, path):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">', "  <channel>",
           f"    <title>{xml_escape(SHOP_NAME)}</title>", f"    <link>{SHOP_URL}</link>",
           "    <description>Čiužiniai, lovos, pagalvės ir miegamojo baldai. Pristatymas visoje Lietuvoje.</description>"]
    for it in items:
        out.append("    <item>")
        out.append(f"      <g:id>{xml_escape(it['id'])}</g:id>")
        if it["id"] != it["group_id"]:
            out.append(f"      <g:item_group_id>{xml_escape(it['group_id'])}</g:item_group_id>")
        out.append(f"      <g:title>{xml_escape(it['title'])}</g:title>")
        out.append(f"      <g:description>{xml_escape(it['description'])}</g:description>")
        out.append(f"      <g:link>{xml_escape(it['link'])}</g:link>")
        out.append(f"      <g:image_link>{xml_escape(it['image'])}</g:image_link>")
        for src in it["additional_images"]:
            out.append(f"      <g:additional_image_link>{xml_escape(src)}</g:additional_image_link>")
        if it["on_sale"]:
            out.append(f"      <g:price>{it['regular_price']} EUR</g:price>")
            out.append(f"      <g:sale_price>{it['price']} EUR</g:sale_price>")
        else:
            out.append(f"      <g:price>{it['price']} EUR</g:price>")
        out.append(f"      <g:availability>{'in stock' if it['available'] else 'out of stock'}</g:availability>")
        out.append("      <g:condition>new</g:condition>")
        out.append(f"      <g:brand>{xml_escape(it['brand'])}</g:brand>")
        if it["sku"]:
            out.append(f"      <g:mpn>{xml_escape(it['sku'])}</g:mpn>")
        out.append(f"      <g:google_product_category>{xml_escape(it['google_category'])}</g:google_product_category>")
        out.append(f"      <g:product_type>{xml_escape(it['category'])}</g:product_type>")
        if it["weight_kg"]:
            out.append(f"      <g:shipping_weight>{xml_escape(it['weight_kg'])} kg</g:shipping_weight>")
        out.append("      <g:identifier_exists>no</g:identifier_exists>")
        out.append("    </item>")
    out += ["  </channel>", "</rss>", ""]
    open(path, "w", encoding="utf-8").write("\n".join(out))


def write_flat(items, path):
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<products shop="{xml_escape(SHOP_NAME)}" url="{SHOP_URL}" currency="EUR" generated="{generated}">']
    for it in items:
        out.append("  <product>")
        out.append(f"    <id>{xml_escape(it['id'])}</id>")
        out.append(f"    <group_id>{xml_escape(it['group_id'])}</group_id>")
        out.append(f"    <sku>{xml_escape(it['sku'])}</sku>")
        out.append(f"    <title>{xml_escape(it['title'])}</title>")
        out.append(f"    <description>{xml_escape(it['description'])}</description>")
        out.append(f"    <url>{xml_escape(it['link'])}</url>")
        out.append(f"    <image_url>{xml_escape(it['image'])}</image_url>")
        for src in it["additional_images"]:
            out.append(f"    <additional_image_url>{xml_escape(src)}</additional_image_url>")
        out.append(f"    <price>{it['price']}</price>")
        if it["on_sale"]:
            out.append(f"    <old_price>{it['regular_price']}</old_price>")
        out.append("    <currency>EUR</currency>")
        out.append(f"    <availability>{'in_stock' if it['available'] else 'out_of_stock'}</availability>")
        out.append("    <condition>new</condition>")
        out.append(f"    <brand>{xml_escape(it['brand'])}</brand>")
        out.append(f"    <category>{xml_escape(it['category'])}</category>")
        out.append(f"    <google_product_category>{xml_escape(it['google_category'])}</google_product_category>")
        if it["weight_kg"]:
            out.append(f"    <weight_kg>{xml_escape(it['weight_kg'])}</weight_kg>")
        if it["delivery_time"]:
            out.append(f"    <delivery_time>{xml_escape(it['delivery_time'])}</delivery_time>")
        out.append("  </product>")
    out += ["</products>", ""]
    open(path, "w", encoding="utf-8").write("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=".", help="output directory")
    ap.add_argument("--pages-dir", help="use cached Store API JSON instead of live requests")
    args = ap.parse_args()

    products = load_products(args.pages_dir)
    items, skipped = build_items(products, args.pages_dir)
    os.makedirs(args.out, exist_ok=True)
    google_path = os.path.join(args.out, "kainos-google.xml")
    flat_path = os.path.join(args.out, "kainos.xml")
    write_google(items, google_path)
    write_flat(items, flat_path)
    print(f"products={len(products)} items={len(items)} skipped={skipped}")
    print(f"wrote {google_path} and {flat_path}")


if __name__ == "__main__":
    main()
