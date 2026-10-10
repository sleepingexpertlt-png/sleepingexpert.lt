#!/usr/bin/env python3
"""Išorinė patikra po publikavimo – skaito tik WordPress REST API (nieko nerašo).

    set -a && source /root/frontier-agent/config/secrets.env && set +a
    python3 scripts/sapnai/verify_wp.py

Spausdina: kategorijos būseną, kiek manifest'o įrašų WP turi (pagal statusą), ar hub turi paiešką,
ar turinyje neliko {{URL:…}} vietaženklių, ar kategorijos aprašyme yra nuoroda į hub, 5 pavyzdinius adresus.
Baigiasi kodu 0 jei viskas gerai, 1 jei yra trūkumų.
"""
from __future__ import annotations

import base64
import http.client
import json
import os
import re
import sys
import time

http.client._MAXHEADERS = 1000
import requests  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "build", "sapnu-reiksmes")
raw = (os.getenv("WP_URL") or "https://sleepingexpert.lt").strip().rstrip("/")
WP_URL = raw if "/wp-json" in raw else raw + "/wp-json/wp/v2"
user, pw = os.getenv("WP_USER"), os.getenv("WP_APP_PASSWORD")
if not (user and pw):
    sys.exit("Trūksta WP_USER / WP_APP_PASSWORD")
H = {"Authorization": "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode(), "User-Agent": "se-sapnai-verify/1.0"}


def get(path, **params):
    r = requests.get(f"{WP_URL}/{path}", headers=H, params=params, timeout=60)
    r.raise_for_status()
    time.sleep(0.25)
    return r.json()


def main() -> int:
    m = json.load(open(os.path.join(BUILD, "manifest.json"), encoding="utf-8"))
    problems = []
    cats = get("categories", slug=m["category"]["slug"], per_page=1)
    if not cats:
        print("🔴 kategorija 'sapnu-reiksmes' neegzistuoja")
        return 1
    cat = cats[0]
    print(f"kategorija #{cat['id']} „{cat['name']}“: {cat['count']} publikuotų įrašų, archyvas {cat['link']}")
    if "sapnu-reiksmes" not in (cat.get("description") or ""):
        problems.append("kategorijos aprašyme nėra nuorodos į hub")
    else:
        print("✅ kategorijos aprašymas rodo į hub")

    # visi kategorijos įrašai (bet kuriuo statusu), puslapiais
    found = {}
    page = 1
    while True:
        batch = get("posts", categories=cat["id"], status="publish,draft,pending,private,future",
                    per_page=100, page=page, _fields="id,slug,link,status,content")
        for p in batch:
            found[p["slug"]] = p
        if len(batch) < 100:
            break
        page += 1
    expected = [m["hub"]] + m["posts"] + m["practices"]
    by_status = {}
    missing = []
    placeholders = []
    for e in expected:
        p = found.get(e["slug"])
        if not p:
            missing.append(e["slug"])
            continue
        by_status[p["status"]] = by_status.get(p["status"], 0) + 1
        if "{{URL:" in p["content"]["rendered"]:
            placeholders.append(e["slug"])
    print(f"manifest: {len(expected)} įrašų | WP rasta: {len(expected) - len(missing)} | pagal statusą: {by_status}")
    if missing:
        problems.append(f"trūksta WP įrašų: {len(missing)} (pvz. {missing[:5]})")
    if placeholders:
        problems.append(f"neišspręsti {{{{URL:}}}} vietaženkliai: {placeholders[:5]}")
    extra = sorted(set(found) - {e["slug"] for e in expected})
    if extra:
        print(f"ℹ️ kategorijoje yra {len(extra)} įrašų ne iš manifest'o (pvz. {extra[:3]})")

    hub = found.get(m["hub"]["slug"])
    if hub:
        c = hub["content"]["rendered"]
        items = c.count('class="se-item"')
        ok_search = 'id="seSapnaiQ"' in c and "seSapnaiCount" in c and "<script" in c
        print(f"hub: {hub['status']} {hub['link']} | simbolių kortelių: {items} | paieška (input+script): {'✅' if ok_search else '🔴'}")
        if not ok_search:
            problems.append("hub be paieškos skripto – WP išmetė <script> (reikia unfiltered_html teisės) arba turinys senas")
        if items != len(m["posts"]):
            problems.append(f"hub rodo {items} simbolių, manifest'e {len(m['posts'])} – paleiskite publish_wp.py dar kartą")
        if "praktika-" not in c and "#praktikos" not in c:
            problems.append("hub be praktikų sekcijos – senas turinys")
    for e in (m["posts"][:3] + m["practices"][:2]):
        p = found.get(e["slug"])
        if p:
            print(f"  {p['status']:<8} {p['link']}")

    if problems:
        print("\n🔴 TRŪKUMAI:")
        for pr in problems:
            print(" -", pr)
        return 1
    print("\n✅ Viskas sutampa su manifest'u.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
