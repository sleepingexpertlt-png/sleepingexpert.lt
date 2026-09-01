#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sleeping Expert — produktu parsisiuntimas karuseles ekranui.

Paima produktus is WooCommerce (sleepingexpert.lt), normalizuoja i
`data/products.json` ir (pasirinktinai) parsisiuncia nuotraukas i `data/images/`,
kad ekranas veiktu net dingus internetui.

Naudoja TIK Python standartine biblioteka — jokiu `pip install`.

Naudojimas:
    python3 fetch_products.py                 # pagal config.json
    python3 fetch_products.py --demo          # testiniai duomenys be interneto
    python3 fetch_products.py --only-sale     # tik akcijines prekes
    python3 fetch_products.py --force         # persisiusti ir jau turimas nuotraukas
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import random
import re
import shutil
import ssl
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(HERE, "config.json")
EXAMPLE_CONFIG = os.path.join(HERE, "config.example.json")

DEFAULTS = {
    "site_url": "https://sleepingexpert.lt",
    "auth": {"consumer_key": "", "consumer_secret": ""},
    "categories": [],
    "exclude_categories": [],
    "only_on_sale": False,
    "only_in_stock": True,
    "min_discount_percent": 0,
    "max_products": 120,
    "sort": "discount",
    "download_images": True,
    "image_width": 1200,
    "output_dir": "data",
    "request_timeout": 30,
    "max_pages": 30,
    "user_agent": "SleepingExpert-Carousel/1.0 (+https://sleepingexpert.lt)",
    "demo_products": [],
    "display": {},
}

DISPLAY_DEFAULTS = {
    "slide_seconds": 9,
    "sale_slide_seconds": 12,
    "sale_ratio": 0.5,
    "sale_first": True,
    "shuffle": True,
    "show_qr": True,
    "show_stores": True,
    "show_clock": True,
    "summary_every": 8,
    "transition_ms": 700,
    "refresh_minutes": 15,
    "reload_hours": 12,
    "orientation": "auto",
    "headline": "SLEEPING EXPERT",
    "sale_badge_text": "AKCIJA",
    "qr_caption": "Nuskenuok ir pamatyk",
    "cta_text": "Klauskite konsultanto salone",
    "sale_note": "",
    "footer_text": "sleepingexpert.lt · Vilnius · Klaipėda · Ukmergė",
    "stores": [
        {"city": "Vilnius", "address": "Kalvarijų g. 125, PC Baldų Rojus"},
        {"city": "Klaipėda", "address": "Taikos pr. 56, PC HELIOS"},
        {"city": "Ukmergė", "address": "Kauno g. 9"},
    ],
    # spalvos ir sriftai — leidzia ta pati kodą naudoti bet kuriai parduotuvei
    "theme": {},
}


# --------------------------------------------------------------------------- #
# pagalbines
# --------------------------------------------------------------------------- #
def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def deep_merge(base: dict, extra: dict) -> dict:
    out = dict(base)
    for key, value in (extra or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_config(path: str) -> dict:
    if not os.path.exists(path):
        if path == DEFAULT_CONFIG and os.path.exists(EXAMPLE_CONFIG):
            log("config.json nerastas — naudojami config.example.json nustatymai")
            path = EXAMPLE_CONFIG
        else:
            log("config nerastas (%s) — naudojami numatytieji nustatymai" % path)
            return deep_merge(DEFAULTS, {"display": DISPLAY_DEFAULTS})
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    cfg = deep_merge(DEFAULTS, raw)
    cfg["display"] = deep_merge(DISPLAY_DEFAULTS, cfg.get("display") or {})
    return cfg


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


# emoji ir piktogramos: TV ekrane atrodo netvarkingai ir daznai yra svetaines
# nuorodos ("Skaitykite daugiau"), o ne prekes aprasymas
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002190-\U000021FF\U00002300-\U000027BF"
    "\U00002B00-\U00002BFF\U0000FE00-\U0000FE0F\U0001F1E6-\U0001F1FF]+")

# svetaines raginimai, likę aprasymo gale
TAIL = re.compile(
    r"[\s.,;:–—-]*(skaitykite|skaityti|placiau|plačiau|suzinokite|sužinokite|"
    r"read more|learn more)\b.*$", re.IGNORECASE)


def clean_description(text: str) -> str:
    """Isvalo aprasyma rodymui ekrane: be emoji ir be 'Skaitykite daugiau'."""
    text = EMOJI.sub(" ", strip_html(text))
    text = TAIL.sub("", text)
    return re.sub(r"\s+", " ", text).strip(" .,;:–—-")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "prekė"


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
class Http:
    def __init__(self, cfg: dict):
        self.timeout = int(cfg.get("request_timeout", 30))
        self.ua = cfg.get("user_agent") or DEFAULTS["user_agent"]
        auth = cfg.get("auth") or {}
        self.key = (auth.get("consumer_key") or os.environ.get("WC_KEY") or "").strip()
        self.secret = (auth.get("consumer_secret") or os.environ.get("WC_SECRET") or "").strip()
        self.ctx = ssl.create_default_context()

    def _request(self, url: str, with_auth: bool = False) -> urllib.request.Request:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", self.ua)
        req.add_header("Accept", "application/json, */*")
        if with_auth and self.key and self.secret:
            token = base64.b64encode(("%s:%s" % (self.key, self.secret)).encode()).decode()
            req.add_header("Authorization", "Basic " + token)
        return req

    def get_json(self, url: str, with_auth: bool = False, retries: int = 3):
        last = None
        for attempt in range(retries):
            try:
                req = self._request(url, with_auth)
                with urllib.request.urlopen(req, timeout=self.timeout, context=self.ctx) as resp:
                    return json.loads(resp.read().decode("utf-8", "replace"))
            except urllib.error.HTTPError as exc:
                raise exc
            except Exception as exc:  # tinklo triktis — bandome dar karta
                last = exc
                time.sleep(2 ** attempt)
        raise last if last else RuntimeError("nepavyko: " + url)

    def download(self, url: str, dest: str) -> bool:
        tmp = dest + ".part"
        try:
            req = self._request(url)
            with urllib.request.urlopen(req, timeout=self.timeout, context=self.ctx) as resp, \
                    open(tmp, "wb") as fh:
                shutil.copyfileobj(resp, fh)
            if os.path.getsize(tmp) < 512:
                os.remove(tmp)
                return False
            os.replace(tmp, dest)
            return True
        except Exception as exc:
            log("  ! nuotraukos klaida %s (%s)" % (url, exc))
            if os.path.exists(tmp):
                os.remove(tmp)
            return False


# --------------------------------------------------------------------------- #
# WooCommerce Store API (viesas, be raktu) + atsarginis WC REST v3
# --------------------------------------------------------------------------- #
def fetch_store_api(http: Http, base: str, cfg: dict) -> list:
    items, page = [], 1
    while page <= int(cfg.get("max_pages", 30)):
        params = {"per_page": 100, "page": page, "orderby": "date", "order": "desc"}
        if cfg.get("only_on_sale"):
            params["on_sale"] = "true"
        url = base + "/wp-json/wc/store/v1/products?" + urllib.parse.urlencode(params)
        batch = http.get_json(url)
        if not isinstance(batch, list) or not batch:
            break
        items.extend(batch)
        log("  Store API puslapis %d — %d prekes (viso %d)" % (page, len(batch), len(items)))
        if len(batch) < 100:
            break
        page += 1
    return items


def fetch_v3_api(http: Http, base: str, cfg: dict) -> list:
    items, page = [], 1
    while page <= int(cfg.get("max_pages", 30)):
        params = {"per_page": 100, "page": page, "status": "publish"}
        if cfg.get("only_on_sale"):
            params["on_sale"] = "true"
        url = base + "/wp-json/wc/v3/products?" + urllib.parse.urlencode(params)
        batch = http.get_json(url, with_auth=True)
        if not isinstance(batch, list) or not batch:
            break
        items.extend(batch)
        log("  REST v3 puslapis %d — %d prekes (viso %d)" % (page, len(batch), len(items)))
        if len(batch) < 100:
            break
        page += 1
    return items


def money_from_minor(value, minor_unit: int):
    if value in (None, "", False):
        return None
    try:
        return int(str(value)) / (10 ** int(minor_unit))
    except (TypeError, ValueError):
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return None


def money_from_decimal(value):
    if value in (None, "", False):
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def pick_image(images, want_width: int):
    """Is srcset renkasi maziausia varianta, kuris vis dar >= want_width."""
    if not images:
        return None
    first = images[0] or {}
    src = first.get("src") or first.get("thumbnail") or ""
    best, best_w = src, 10 ** 9 if src else 0
    srcset = first.get("srcset") or ""
    candidates = []
    for chunk in srcset.split(","):
        chunk = chunk.strip()
        match = re.match(r"^(\S+)\s+(\d+)w$", chunk)
        if match:
            candidates.append((match.group(1), int(match.group(2))))
    fitting = [c for c in candidates if c[1] >= want_width]
    if fitting:
        best, best_w = min(fitting, key=lambda c: c[1])
    elif candidates:
        best, best_w = max(candidates, key=lambda c: c[1])
    return best or src or None


def normalize_store(raw: dict, cfg: dict) -> dict | None:
    prices = raw.get("prices") or {}
    minor = prices.get("currency_minor_unit", 2)
    price = money_from_minor(prices.get("price"), minor)
    regular = money_from_minor(prices.get("regular_price"), minor)
    sale = money_from_minor(prices.get("sale_price"), minor)

    price_from = False
    rng = prices.get("price_range")
    if isinstance(rng, dict) and rng.get("min_amount"):
        low = money_from_minor(rng.get("min_amount"), minor)
        high = money_from_minor(rng.get("max_amount"), minor)
        if low is not None:
            price = low
            price_from = high is not None and high > low

    return build_product(
        pid=raw.get("id"),
        name=strip_html(raw.get("name")),
        url=raw.get("permalink") or "",
        image=pick_image(raw.get("images") or [], int(cfg.get("image_width", 1200))),
        price=price,
        regular=regular,
        sale=sale,
        on_sale=bool(raw.get("on_sale")),
        in_stock=bool(raw.get("is_in_stock", True)),
        sku=raw.get("sku") or "",
        categories=[c.get("name") for c in (raw.get("categories") or []) if c.get("name")],
        category_slugs=[c.get("slug") for c in (raw.get("categories") or []) if c.get("slug")],
        short=clean_description(raw.get("short_description")),
        currency=prices.get("currency_symbol") or "€",
        price_from=price_from,
    )


def normalize_v3(raw: dict, cfg: dict) -> dict | None:
    images = [{"src": img.get("src", "")} for img in (raw.get("images") or [])]
    return build_product(
        pid=raw.get("id"),
        name=strip_html(raw.get("name")),
        url=raw.get("permalink") or "",
        image=pick_image(images, int(cfg.get("image_width", 1200))),
        price=money_from_decimal(raw.get("price")),
        regular=money_from_decimal(raw.get("regular_price")),
        sale=money_from_decimal(raw.get("sale_price")),
        on_sale=bool(raw.get("on_sale")),
        in_stock=(raw.get("stock_status", "instock") == "instock"),
        sku=raw.get("sku") or "",
        categories=[c.get("name") for c in (raw.get("categories") or []) if c.get("name")],
        category_slugs=[c.get("slug") for c in (raw.get("categories") or []) if c.get("slug")],
        short=clean_description(raw.get("short_description")),
        currency="€",
        price_from=bool(raw.get("type") == "variable"),
    )


def build_product(pid, name, url, image, price, regular, sale, on_sale, in_stock,
                  sku, categories, category_slugs, short, currency, price_from) -> dict | None:
    if not name or price is None or price <= 0:
        return None  # 0 EUR prekes (pvz. "kaina pagal uzklausa") ekranui netinka
    if regular is None or regular <= 0:
        regular = price
    if sale is not None and sale > 0 and sale < regular:
        price = min(price, sale)
    discount = 0
    save = 0.0
    if regular > price > 0:
        discount = int(round((regular - price) / regular * 100))
        save = round(regular - price, 2)
    # WooCommerce zymi variantine preke kaip "akcijoje" net kai pigiausio varianto
    # kaina nesumazejusi. Ekranui akcija yra tik tai, ka galima parodyti skaiciumi —
    # kitaip uzsidegtu "AKCIJA" be jokios matomos nuolaidos.
    on_sale = discount > 0
    return {
        "id": pid,
        "name": name,
        "url": url,
        "sku": sku,
        "image": None,               # uzpildoma parsisiuntus
        "image_remote": image or "",
        "price": round(price, 2),
        "regular_price": round(regular, 2),
        "price_from": bool(price_from),
        "on_sale": on_sale,
        "discount_percent": discount,
        "save_amount": save,
        "in_stock": bool(in_stock),
        "currency": currency or "€",
        "categories": categories or [],
        "category_slugs": category_slugs or [],
        "short": (short or "")[:220],
    }


# --------------------------------------------------------------------------- #
# filtravimas / rusiavimas
# --------------------------------------------------------------------------- #
def apply_filters(products: list, cfg: dict) -> list:
    include = {s.lower() for s in (cfg.get("categories") or [])}
    exclude = {s.lower() for s in (cfg.get("exclude_categories") or [])}
    min_disc = int(cfg.get("min_discount_percent", 0))
    out = []
    for prod in products:
        slugs = {s.lower() for s in prod.get("category_slugs") or []}
        names = {slugify(n) for n in prod.get("categories") or []}
        tags = slugs | names
        if include and not (tags & include):
            continue
        if exclude and (tags & exclude):
            continue
        if cfg.get("only_in_stock", True) and not prod.get("in_stock", True):
            continue
        if cfg.get("only_on_sale") and not prod.get("on_sale"):
            continue
        if min_disc and prod.get("discount_percent", 0) < min_disc:
            continue
        if not prod.get("image_remote"):
            continue
        out.append(prod)
    return out


def sort_products(products: list, mode: str) -> list:
    if mode == "discount":
        return sorted(products, key=lambda p: (-p.get("discount_percent", 0), -p.get("save_amount", 0)))
    if mode == "price_desc":
        return sorted(products, key=lambda p: -p.get("price", 0))
    if mode == "price_asc":
        return sorted(products, key=lambda p: p.get("price", 0))
    if mode == "name":
        return sorted(products, key=lambda p: p.get("name", "").lower())
    if mode == "random":
        shuffled = list(products)
        random.shuffle(shuffled)
        return shuffled
    return products


# --------------------------------------------------------------------------- #
# nuotraukos
# --------------------------------------------------------------------------- #
def sync_images(http: Http, products: list, out_dir: str, force: bool) -> None:
    img_dir = os.path.join(out_dir, "images")
    os.makedirs(img_dir, exist_ok=True)
    keep = set()
    for idx, prod in enumerate(products, 1):
        remote = prod.get("image_remote") or ""
        if not remote:
            continue
        ext = os.path.splitext(urllib.parse.urlparse(remote).path)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"):
            ext = ".jpg"
        fname = "%s-%s%s" % (prod.get("id") or idx, slugify(prod["name"])[:40], ext)
        dest = os.path.join(img_dir, fname)
        keep.add(fname)
        if force or not os.path.exists(dest) or os.path.getsize(dest) < 512:
            if http.download(remote, dest):
                log("  ↓ %s" % fname)
            else:
                keep.discard(fname)
                continue
        prod["image"] = "images/" + fname
    removed = 0
    for fname in os.listdir(img_dir):
        if fname not in keep and not fname.endswith(".part"):
            os.remove(os.path.join(img_dir, fname))
            removed += 1
    if removed:
        log("  ✂ pasalinta %d nebenaudojamu nuotrauku" % removed)


# --------------------------------------------------------------------------- #
# demo duomenys (be interneto)
# --------------------------------------------------------------------------- #
DEMO = [
    {"name": "Ortopedinis čiužinys Comfort Plus 160x200", "regular": 549.0, "price": 399.0,
     "category": "Čiužiniai", "short": "Kišeninės spyruoklės, 7 zonų palaikymas, nuimamas užvalkalas."},
    {"name": "Latekso čiužinys Natural Sleep 180x200", "regular": 899.0, "price": 719.0,
     "category": "Čiužiniai", "short": "Natūralus lateksas, itin kvėpuojantis, tinka alergiškiems."},
    {"name": "Atminties putų pagalvė Memory Soft", "regular": 79.0, "price": 49.0,
     "category": "Pagalvės", "short": "Prisitaiko prie kaklo linijos, tinka miegantiems ant šono."},
    {"name": "Antčiužinis Hotel Line 160x200", "regular": 149.0, "price": 149.0,
     "category": "Antčiužiniai", "short": "Papildomas minkštumo sluoksnis viešbučio standartu."},
    {"name": "Kontinentinė lova Elegance 160x200", "regular": 1290.0, "price": 990.0,
     "category": "Lovos", "short": "Su spyruokliniu pagrindu ir topperiu, aksomo apmušalas."},
    {"name": "Čiužinio apsauga Aqua Stop 90x200", "regular": 45.0, "price": 32.0,
     "category": "Čiužinių apsaugos", "short": "Neperšlampama, kvėpuojanti, skalbiama 60°C."},
    {"name": "Pūkinė antklodė Nordic 200x220", "regular": 219.0, "price": 219.0,
     "category": "Patalynė", "short": "Natūralūs pūkai, keturių sezonų sprendimas."},
    {"name": "Spyruoklinis čiužinys Basic 140x200", "regular": 329.0, "price": 249.0,
     "category": "Čiužiniai", "short": "Bonelio spyruoklės, vidutinio kietumo, greitas pristatymas."},
    {"name": "Vaikiškas čiužinys Junior 80x160", "regular": 189.0, "price": 149.0,
     "category": "Čiužiniai", "short": "Hipoalerginis, be kenksmingų medžiagų, plonas profilis."},
    {"name": "Miego kaukė Deep Rest", "regular": 19.0, "price": 12.0,
     "category": "Miego aksesuarai", "short": "Visiškai neperšviečiama, minkšti kraštai."},
]

SVG_TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900">'
    '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c2}"/>'
    '</linearGradient></defs>'
    '<rect width="1200" height="900" fill="url(#g)"/>'
    '<circle cx="960" cy="180" r="220" fill="#ffffff" fill-opacity="0.08"/>'
    '<rect x="140" y="380" width="920" height="260" rx="40" fill="#ffffff" fill-opacity="0.14"/>'
    '<text x="600" y="330" font-family="Georgia,serif" font-size="64" fill="#ffffff" '
    'text-anchor="middle" opacity="0.92">{cat}</text>'
    '<text x="600" y="530" font-family="Georgia,serif" font-size="46" fill="#ffffff" '
    'text-anchor="middle">{name}</text>'
    '<text x="600" y="800" font-family="Georgia,serif" font-size="34" fill="{accent}" '
    'text-anchor="middle">DEMO nuotrauka</text></svg>'
)


def build_demo(cfg: dict, out_dir: str) -> list:
    """Testiniai duomenys be interneto. Prekes ir spalvas galima nurodyti config faile."""
    img_dir = os.path.join(out_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    items = cfg.get("demo_products") or DEMO
    theme = (cfg.get("display") or {}).get("theme") or {}
    base = theme.get("brand_deep") or "#142b6f"
    soft = theme.get("brand_soft") or theme.get("brand") or "#2b4bb0"
    accent = theme.get("accent") or "#ffd602"
    palette = [(base, soft), (soft, base), (base, accent + "40")]

    products = []
    for idx, item in enumerate(items, 1):
        name = item["name"]
        regular = float(item.get("regular", item.get("price", 0)))
        price = float(item.get("price", regular))
        category = item.get("category", "")
        colors = palette[idx % len(palette)]
        fname = "demo-%02d.svg" % idx
        short_name = name if len(name) <= 34 else name[:33] + "…"
        with open(os.path.join(img_dir, fname), "w", encoding="utf-8") as fh:
            fh.write(SVG_TEMPLATE.format(
                c1=colors[0], c2=colors[1], accent=accent,
                cat=html.escape(category), name=html.escape(short_name)))
        prod = build_product(
            pid=9000 + idx, name=name,
            url="%s/produktas/%s/" % (cfg.get("site_url", "").rstrip("/"), slugify(name)),
            image="", price=price, regular=regular, sale=price if price < regular else None,
            on_sale=price < regular, in_stock=True, sku="DEMO-%03d" % idx,
            categories=[category] if category else [], category_slugs=[slugify(category)] if category else [],
            short=item.get("short", ""), currency="€", price_from=False)
        prod["image"] = "images/" + fname
        products.append(prod)
    return products


# --------------------------------------------------------------------------- #
# irasymas
# --------------------------------------------------------------------------- #
def write_json(path: str, payload: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    if os.path.exists(path):
        shutil.copyfile(path, path + ".bak")
    os.replace(tmp, path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sleeping Expert karuseles produktu parsisiuntimas")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--demo", action="store_true", help="sugeneruoti testinius duomenis be interneto")
    parser.add_argument("--only-sale", action="store_true", help="tik akcijines prekes")
    parser.add_argument("--limit", type=int, default=None, help="max prekiu skaicius")
    parser.add_argument("--no-images", action="store_true", help="nesiusti nuotrauku (naudoti tiesiogines nuorodas)")
    parser.add_argument("--force", action="store_true", help="persisiusti visas nuotraukas is naujo")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.only_sale:
        cfg["only_on_sale"] = True
    if args.limit:
        cfg["max_products"] = args.limit
    if args.no_images:
        cfg["download_images"] = False

    out_dir = cfg["output_dir"]
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(HERE, out_dir)
    os.makedirs(out_dir, exist_ok=True)

    http = Http(cfg)
    base = (cfg.get("site_url") or "").rstrip("/")
    source = "demo"

    if args.demo:
        log("DEMO rezimas — duomenys generuojami vietoje")
        products = build_demo(cfg, out_dir)
    else:
        log("Jungiamasi prie %s" % base)
        raw_items, normalizer = [], normalize_store
        try:
            raw_items = fetch_store_api(http, base, cfg)
            source = "store-api"
        except Exception as exc:
            log("Store API nepavyko (%s)" % exc)
            if http.key and http.secret:
                log("Bandome WooCommerce REST v3 su raktais…")
                raw_items = fetch_v3_api(http, base, cfg)
                normalizer = normalize_v3
                source = "wc-v3"
            else:
                log("KLAIDA: nepavyko gauti produktu ir nera API raktu. "
                    "Senesni duomenys paliekami nepakeisti.")
                return 2
        products = [p for p in (normalizer(item, cfg) for item in raw_items) if p]
        log("Normalizuota %d prekiu" % len(products))
        products = apply_filters(products, cfg)
        log("Po filtru liko %d prekiu" % len(products))
        products = sort_products(products, cfg.get("sort", "discount"))
        products = products[: int(cfg.get("max_products", 120))]
        if cfg.get("download_images", True):
            log("Siunciamos nuotraukos…")
            sync_images(http, products, out_dir, args.force)
            products = [p for p in products if p.get("image")]
        else:
            for prod in products:
                prod["image"] = prod["image_remote"]

    if not products:
        log("KLAIDA: nera nei vienos tinkamos prekes — failai nekeiciami.")
        return 3

    on_sale = [p for p in products if p.get("on_sale")]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source,
        "site": base,
        "counts": {
            "total": len(products),
            "on_sale": len(on_sale),
            "max_discount": max([p["discount_percent"] for p in on_sale], default=0),
        },
        "products": products,
    }
    write_json(os.path.join(out_dir, "products.json"), payload)
    write_json(os.path.join(out_dir, "display.json"), cfg["display"])
    max_discount = payload["counts"]["max_discount"]
    log("Irasyta: %s (%d prekes, %d akcijoje%s)" % (
        os.path.join(out_dir, "products.json"), len(products), len(on_sale),
        ", didziausia nuolaida -%d%%" % max_discount if max_discount else ""))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
