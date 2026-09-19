#!/usr/bin/env python3
"""Sapnų reikšmės — publikavimas į sleepingexpert.lt WordPress per REST API.

Paleidžiama iš VPS (frontier-agent), kur yra WP kredencialai:
    cd /root/sleepingexpert.lt && set -a && source /root/frontier-agent/config/secrets.env && set +a
    python3 scripts/sapnai/build.py
    python3 scripts/sapnai/publish_wp.py                 # dry-run: tik parodo planą, nieko nerašo
    python3 scripts/sapnai/publish_wp.py --apply         # sukuria/atnaujina DRAFT įrašus
    python3 scripts/sapnai/publish_wp.py --apply --limit 50   # pirmoji partija (progressive rollout)
    python3 scripts/sapnai/publish_wp.py --apply --publish    # statusas publish (tik po peržiūros)

Ką daro (idempotentiškai, pagal slug):
  1. Sukuria kategoriją „Sapnų reikšmės“ (slug sapnu-reiksmes), jei jos nėra.
  2. Sukuria kiekvienam įrašui DRAFT su pavadinimu/slug/kategorija (be turinio), kad gautų tikrus permalink'us.
  3. Pakeičia {{URL:<key>}} vietaženklius tikrais permalink'ais ir įrašo turinį, excerpt ir RankMath meta.
  4. Hub straipsnį (sapnu-reiksmes) atnaujina paskutinį – jame nuorodos į visus 120 įrašų.

Reikalingi env: WP_USER, WP_APP_PASSWORD; WP_URL gali būti svetainės šaknis (kaip secrets.env) arba pilnas /wp-json/wp/v2 kelias.
"""
from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import sys
import time

http.client._MAXHEADERS = 1000  # privaloma sleepingexpert.lt (wp-publisher skill)

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "build", "sapnu-reiksmes")


def _rest_base(raw: str | None) -> str:
    """secrets.env laiko WP_URL kaip svetainės šaknį (https://www.sleepingexpert.lt);
    priimame ir šaknį, ir pilną /wp-json/wp/v2 kelią."""
    url = (raw or "https://sleepingexpert.lt").strip().rstrip("/")
    if "/wp-json" not in url:
        url += "/wp-json/wp/v2"
    return url


WP_URL = _rest_base(os.getenv("WP_URL"))


class WP:
    def __init__(self, user: str, app_password: str, dry_run: bool, pause: float = 0.4):
        token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self.h = {"Authorization": f"Basic {token}", "Content-Type": "application/json",
                  "User-Agent": "SleepingExpert-sapnai/1.0"}
        self.dry = dry_run
        self.pause = pause

    def get(self, path: str, **params):
        r = requests.get(f"{WP_URL}/{path}", headers=self.h, params=params, timeout=60)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, data: dict):
        if self.dry:
            return {"id": 0, "link": f"{WP_URL}/DRY/{data.get('slug', path)}/", "dry": True}
        r = requests.post(f"{WP_URL}/{path}", headers=self.h, json=data, timeout=120)
        if r.status_code >= 400:
            sys.exit(f"WP klaida {r.status_code} {path}: {r.text[:500]}")
        time.sleep(self.pause)
        return r.json()


def ensure_category(wp: WP, cat: dict) -> int:
    found = wp.get("categories", slug=cat["slug"], per_page=1)
    if found:
        print(f"kategorija yra: #{found[0]['id']} {found[0]['name']} ({found[0]['count']} įrašų)")
        return found[0]["id"]
    print(f"kategorija kuriama: {cat['name']} ({cat['slug']})")
    res = wp.post("categories", {"name": cat["name"], "slug": cat["slug"], "description": cat["description"]})
    return res["id"]


def find_post(wp: WP, slug: str) -> dict | None:
    # viena užklausa visiems statusams (autentifikuotam vartotojui leidžiamas sąrašas) + pauzė:
    # 2026-09-08 pamoka – bulk WP užklausos be pauzės užblokavo visą domeną (429).
    found = wp.get("posts", slug=slug, status="publish,draft,pending,private,future",
                   per_page=1, _fields="id,link,status,slug,title")
    time.sleep(0.25)
    return found[0] if found else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="tikrai rašyti į WordPress (numatyta: dry-run)")
    ap.add_argument("--publish", action="store_true", help="statusas publish vietoj draft")
    ap.add_argument("--limit", type=int, default=0, help="publikuoti tik pirmus N simbolių įrašų (partijomis)")
    ap.add_argument("--only", default="", help="kableliais atskirti key'ai, pvz. gyvate,dantys (ir hub visada)")
    ap.add_argument("--skip-hub", action="store_true", help="neatnaujinti hub straipsnio")
    args = ap.parse_args()

    with open(os.path.join(BUILD, "manifest.json"), encoding="utf-8") as f:
        m = json.load(f)

    user, pw = os.getenv("WP_USER"), os.getenv("WP_APP_PASSWORD")
    dry = not args.apply
    if not dry and (not user or not pw):
        sys.exit("Trūksta WP_USER / WP_APP_PASSWORD (source /root/frontier-agent/config/secrets.env)")
    if requests is None:
        sys.exit("Reikia `pip install requests`")

    posts = m["posts"]
    if args.only:
        keys = {k.strip() for k in args.only.split(",")}
        posts = [p for p in posts if p["key"] in keys]
    if args.limit:
        posts = posts[: args.limit]
    status = "publish" if args.publish else "draft"
    print(f"{'DRY-RUN' if dry else 'APPLY'} → {WP_URL} | įrašų: {len(posts)} + hub | statusas: {status}")

    if dry and not (user and pw):
        # be kredencialų – tik lokalus planas
        for p in posts:
            print(f"  [{p['category']}] {p['slug']:<36} {p['title']}  ({p['words']} ž.)")
        print(f"  hub  {m['hub']['slug']:<36} {m['hub']['title']}  ({m['hub']['words']} ž.)")
        print("Planas be WP užklausų (nėra kredencialų). Su kredencialais dry-run dar patikrina, kurie įrašai jau yra.")
        return 0

    wp = WP(user, pw, dry_run=dry)
    cat_id = ensure_category(wp, m["category"])

    # 1) sukurti visus įrašus be turinio → gauti permalink'us
    items = posts + ([] if args.skip_hub else [m["hub"]])
    links: dict[str, str] = {}
    ids: dict[str, int] = {}
    for p in items:
        existing = find_post(wp, p["slug"])
        if existing:
            ids[p["key"]], links[p["key"]] = existing["id"], existing["link"]
            print(f"  yra   #{existing['id']} {existing['status']:<8} {existing['link']}")
        else:
            res = wp.post("posts", {"title": p["title"], "slug": p["slug"], "status": "draft",
                                    "categories": [cat_id], "excerpt": p["excerpt"]})
            ids[p["key"]], links[p["key"]] = res["id"], res["link"]
            print(f"  nauja #{res['id']} draft    {res['link']}")

    # hub link visada reikalingas – jei hub praleistas, bandome rasti esamą
    if m["hub"]["key"] not in links:
        existing = find_post(wp, m["hub"]["slug"])
        links[m["hub"]["key"]] = existing["link"] if existing else f"https://sleepingexpert.lt/{m['hub']['slug']}/"

    # 2) turinys su tikromis nuorodomis
    def resolve(html: str) -> str:
        missing = set()
        def rep(match):
            key = match.group(1)
            if key in links:
                return links[key]
            missing.add(key)
            return f"https://sleepingexpert.lt/{key}/"  # atsarginis – sukuriamas vėliau kitoje partijoje
        import re
        out = re.sub(r"\{\{URL:([a-z0-9-]+)\}\}", rep, html)
        if missing:
            print(f"    ⚠️ nuorodos į dar nesukurtus įrašus ({len(missing)}): {sorted(missing)[:6]}…")
        return out

    for p in items:
        with open(os.path.join(BUILD, p["file"]), encoding="utf-8") as f:
            content = resolve(f.read())
        data = {"content": content, "status": status, "excerpt": p["excerpt"], "categories": [cat_id],
                "meta": {"rank_math_focus_keyword": p["focus_keyword"],
                         "rank_math_secondary_keywords": p["secondary_keywords"]}}
        wp.post(f"posts/{ids[p['key']]}", data)
        print(f"  ✅ {p['slug']} → {links[p['key']]} ({p['words']} ž., {status})")

    print("Baigta. Peržiūrėkite draft'us WP admin → Posts → Drafts ir spauskite Publish (arba --publish).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
