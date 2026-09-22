#!/usr/bin/env python3
"""
Įkelia biolink/index.html į sleepingexpert.lt WordPress media biblioteką.

Leidžiama iš VPS (72.61.139.213), kur yra /root/frontier-agent/config/secrets.env
su WP_USER ir WP_APP_PASSWORD:

    set -a && source /root/frontier-agent/config/secrets.env && set +a
    python3 biolink/deploy.py            # dry run: parodo, ką darys
    python3 biolink/deploy.py --apply    # įkelia ir ištrina senas versijas

Puslapį adresu /link/ atiduoda Code Snippet iš biolink/wp-snippet.php
(įdiegiamas vieną kartą per WP Admin → Snippets).
"""
import argparse
import base64
import datetime as dt
import http.client
import json
import os
import pathlib
import sys

http.client._MAXHEADERS = 1000  # privaloma sleepingexpert.lt (daug antraščių)

try:
    import requests
except ImportError:
    sys.exit("Trūksta 'requests': pip install requests")

WP_URL = os.environ.get("WP_URL", "https://sleepingexpert.lt").rstrip("/")
WP_USER = os.environ.get("WP_USER")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD")
TITLE_PREFIX = "se-biolink"
HERE = pathlib.Path(__file__).resolve().parent
HTML_FILE = HERE / "index.html"


def auth_headers():
    if not WP_USER or not WP_APP_PASSWORD:
        sys.exit("Nerasti WP_USER / WP_APP_PASSWORD. Pirma: set -a && source secrets.env && set +a")
    token = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def list_existing(headers):
    r = requests.get(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers=headers,
        params={"search": TITLE_PREFIX, "per_page": 50, "orderby": "date", "order": "desc"},
        timeout=60,
    )
    r.raise_for_status()
    return [m for m in r.json() if m.get("title", {}).get("rendered", "").startswith(TITLE_PREFIX)]


def upload(headers, html_bytes, filename):
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **headers,
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": "text/html",
        },
        data=html_bytes,
        timeout=120,
    )
    if r.status_code == 415 or (r.status_code >= 400 and "not permitted" in r.text):
        # Hostinger/WP gali neleisti .html — bandome .txt su tuo pačiu turiniu.
        alt = filename[:-5] + ".txt"
        r = requests.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            headers={
                **headers,
                "Content-Disposition": f'attachment; filename="{alt}"',
                "Content-Type": "text/plain",
            },
            data=html_bytes,
            timeout=120,
        )
    if r.status_code != 201:
        sys.exit(f"KLAIDA {r.status_code}: {r.text[:400]}")
    media = r.json()
    # Pavadinimas turi prasidėti TITLE_PREFIX, kad snippet'as jį rastų.
    requests.post(
        f"{WP_URL}/wp-json/wp/v2/media/{media['id']}",
        headers={**headers, "Content-Type": "application/json"},
        data=json.dumps({"title": filename.rsplit(".", 1)[0], "alt_text": "Sleeping Expert bio link"}),
        timeout=60,
    )
    return media


def delete(headers, media_id):
    r = requests.delete(
        f"{WP_URL}/wp-json/wp/v2/media/{media_id}",
        headers=headers,
        params={"force": "true"},
        timeout=60,
    )
    return r.status_code == 200


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="iš tikrųjų įkelti (be šio flag'o — tik dry run)")
    ap.add_argument("--keep-old", action="store_true", help="netrinti ankstesnių versijų")
    args = ap.parse_args()

    if not HTML_FILE.exists():
        sys.exit(f"Nerastas {HTML_FILE}")
    html_bytes = HTML_FILE.read_bytes()
    if b"SE_LINKS" not in html_bytes:
        sys.exit("index.html neatrodo kaip bio link puslapis (nėra SE_LINKS bloko)")

    headers = auth_headers()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"{TITLE_PREFIX}-{stamp}.html"
    existing = list_existing(headers)

    print("DRY RUN" if not args.apply else "APPLY")
    print(f"  Failas:    {HTML_FILE} ({len(html_bytes)} B)")
    print(f"  Endpoint:  {WP_URL}/wp-json/wp/v2/media")
    print(f"  Įkels kaip: {filename}")
    print(f"  Esamos versijos: {len(existing)}" + ("" if args.keep_old else " (bus ištrintos po įkėlimo)"))
    for m in existing:
        print(f"    - id={m['id']} {m.get('source_url')}")
    if not args.apply:
        print("\nPaleisk su --apply, kad įkeltų.")
        return

    media = upload(headers, html_bytes, filename)
    print(f"\nOK  media id={media['id']}")
    print(f"OK  {media['source_url']}")

    if not args.keep_old:
        for m in existing:
            ok = delete(headers, m["id"])
            print(f"{'OK ' if ok else '!! '} ištrinta sena versija id={m['id']}" if ok else f"!!  nepavyko ištrinti id={m['id']}")

    print(f"\nPuslapis: {WP_URL}/link/")
    print("Jei rodo 404 — Code Snippet iš biolink/wp-snippet.php dar neįdiegtas arba neaktyvus.")
    print("Jei rodo seną versiją — LiteSpeed: Toolbox → Purge All.")


if __name__ == "__main__":
    main()
