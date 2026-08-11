#!/usr/bin/env python3
"""Suveda surinktus swatch'us į katalogą.

Įvestis: swatches.csv su stulpeliais
    tiekejas,kolekcija,kodas,spalva,url

    tiekejas   — Davis | Fargotex | Top Textil | Elastron
    kolekcija  — tiksliai kaip audiniai.json (Aragon, Matt Velvet, ...)
    kodas      — gamintojo užsakymo kodas (03, 17B, ...)
    spalva     — spalvos pavadinimas, jei yra (neprivaloma)
    url        — nuotraukos adresas ARBA vietinis kelias

Ką daro:
    1. Patikrina, ar kolekcija tikrai yra mūsų sąraše (kitaip praleidžia).
    2. Atsisiunčia nuotraukas į out/ ir pervadina pagal slug taisyklę.
    3. Įrašo kodus į audiniai.json.

Grupė NEIMAMA iš CSV — ji nuskaitoma iš audiniai.json. Taip scraperis
negali įterpti audinio, kurio salonuose nėra, ar pakeisti grupės.

Naudojimas:
    python3 import_swatches.py swatches.csv
    python3 import_swatches.py swatches.csv --dry-run     # tik ataskaita
    python3 import_swatches.py swatches.csv --no-images   # tik kodai
"""

import argparse
import csv
import json
import re
import shutil
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE.parent / "audiniai.json"
OUT = HERE / "out"

UA = "Mozilla/5.0 (compatible; SleepingExpertCatalog/1.0; +https://sleepingexpert.lt)"
DELAY = 0.7      # sekundes tarp uzklausu tam paciam hostui
RETRIES = 3


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()


def load_catalog():
    """Grazina (data, index) kur index: (tiekejas_lower, kolekcija_lower) -> (supplier, grupe)."""
    data = json.loads(DATA.read_text(encoding="utf-8"))
    index = {}
    for supplier in data["tiekejai"]:
        for group, fabrics in supplier["audiniai"].items():
            for fabric in fabrics:
                name = fabric if isinstance(fabric, str) else fabric["vardas"]
                index[(supplier["vardas"].lower(), name.lower())] = (supplier, group, name)
    return data, index


def download(url: str, dest: Path) -> None:
    if not url.startswith(("http://", "https://")):
        source = Path(url)
        if not source.is_file():
            raise FileNotFoundError(url)
        shutil.copyfile(source, dest)
        return

    last = None
    for attempt in range(RETRIES):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(request, timeout=30) as response:
                dest.write_bytes(response.read())
            return
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as error:
            last = error
            time.sleep(2 ** attempt)
    raise RuntimeError("%s -> %s" % (url, last))


def to_webp(path: Path) -> Path:
    """Konvertuoja i webp, jei yra Pillow. Kitaip palieka kaip yra."""
    try:
        from PIL import Image
    except ImportError:
        return path
    target = path.with_suffix(".webp")
    if target == path:
        return path
    with Image.open(path) as image:
        image.convert("RGB").save(target, "webp", quality=82, method=5)
    path.unlink()
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="swatches.csv")
    parser.add_argument("--dry-run", action="store_true", help="nieko nerašo, tik ataskaita")
    parser.add_argument("--no-images", action="store_true", help="tik kodai, be atsisiuntimo")
    args = parser.parse_args()

    data, index = load_catalog()

    rows = list(csv.DictReader(Path(args.csv_file).read_text(encoding="utf-8").splitlines()))
    required = {"tiekejas", "kolekcija", "kodas"}
    if not rows or not required.issubset(rows[0].keys()):
        print("KLAIDA: CSV turi turėti stulpelius %s (+ url, spalva)" % ", ".join(sorted(required)))
        return 1

    codes = defaultdict(set)      # (tiekejas, kolekcija) -> {kodai}
    downloads = []                # (url, dest_slug)
    unknown = defaultdict(set)
    dupes = 0

    for row in rows:
        supplier_name = (row.get("tiekejas") or "").strip()
        collection = (row.get("kolekcija") or "").strip()
        code = (row.get("kodas") or "").strip()
        url = (row.get("url") or "").strip()

        key = (supplier_name.lower(), collection.lower())
        if key not in index:
            unknown[supplier_name].add(collection)
            continue
        if not code:
            continue

        supplier, _group, canonical = index[key]
        if code in codes[(supplier["vardas"], canonical)]:
            dupes += 1
            continue
        codes[(supplier["vardas"], canonical)].add(code)

        if url and not args.no_images:
            downloads.append((url, supplier["slug"], slugify("%s-%s" % (canonical, code))))

    # --- ataskaita ---
    total_codes = sum(len(v) for v in codes.values())
    print("Kolekcijų su kodais : %d / %d" % (len(codes), len(index)))
    print("Kodų iš viso        : %d" % total_codes)
    print("Nuotraukų parsiųsti  : %d" % len(downloads))
    if dupes:
        print("Dublikatų praleista : %d" % dupes)
    if unknown:
        print("\n⚠️  Nežinomos kolekcijos (praleistos — jų nėra salonų sąraše):")
        for supplier_name, names in sorted(unknown.items()):
            print("   %s: %s" % (supplier_name, ", ".join(sorted(names))))

    missing = [
        "%s / %s" % (supplier["vardas"], name)
        for (_s, _c), (supplier, _g, name) in index.items()
        if (supplier["vardas"], name) not in codes
    ]
    if missing:
        print("\n⚠️  Be kodų liko %d kolekcijų:" % len(missing))
        for entry in sorted(missing):
            print("   %s" % entry)

    if args.dry_run:
        print("\n(dry-run — nieko neįrašyta)")
        return 0

    # --- nuotraukos ---
    failed = []
    if downloads:
        for i, (url, supplier_slug, slug) in enumerate(downloads, 1):
            folder = OUT / supplier_slug
            folder.mkdir(parents=True, exist_ok=True)
            suffix = Path(url.split("?")[0]).suffix or ".jpg"
            dest = folder / (slug + suffix)
            try:
                download(url, dest)
                to_webp(dest)
            except Exception as error:  # noqa: BLE001 — norime tęsti su likusiais
                failed.append((url, str(error)))
            if i % 25 == 0:
                print("   ... %d/%d" % (i, len(downloads)))
            time.sleep(DELAY)
        print("\nAtsisiųsta: %d, nepavyko: %d" % (len(downloads) - len(failed), len(failed)))
        for url, error in failed[:10]:
            print("   ✗ %s — %s" % (url, error))

    # --- kodai i audiniai.json ---
    for supplier in data["tiekejai"]:
        for group, fabrics in supplier["audiniai"].items():
            updated = []
            for fabric in fabrics:
                name = fabric if isinstance(fabric, str) else fabric["vardas"]
                found = codes.get((supplier["vardas"], name))
                if not found:
                    updated.append(fabric)
                    continue
                existing = set() if isinstance(fabric, str) else set(fabric.get("spalvos", []))
                merged = sorted(existing | found, key=lambda c: (len(c), c))
                updated.append({"vardas": name, "spalvos": merged})
            supplier["audiniai"][group] = updated

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n✅ audiniai.json atnaujintas. Toliau: python3 ../build.py --images")
    if not OUT.exists():
        return 0
    print("   Nuotraukos: %s → kelti į /wp-content/uploads/audiniai/" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
