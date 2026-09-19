#!/usr/bin/env python3
"""Core Web Vitals patikra sleepingexpert.lt — realūs Chrome (CrUX) duomenys + Lighthouse.

GSC Core Web Vitals ataskaita neturi API, todėl tą patį šaltinį (CrUX, 28 d. p75) traukiame
per PageSpeed Insights API. Su GOOGLE_API_KEY lauko duomenys imami iš CrUX API
(atskira kvota, be dienos limito), o Lighthouse – iš PSI; jei rakto PSI kvota išnaudota, PSI
bandomas anonimiškai (kelios dešimtys užklausų per dieną iš vieno IP).

Naudojimas (iš VPS):
    python3 scripts/cwv/cwv_check.py                       # numatyti URL, mobile
    python3 scripts/cwv/cwv_check.py --strategy desktop
    python3 scripts/cwv/cwv_check.py --urls urls.txt --out build/cwv
    GOOGLE_API_KEY=... python3 scripts/cwv/cwv_check.py --crux-history   # 25 sav. tendencija

Išvestis: build/cwv/cwv_<data>.json + build/cwv/cwv_<data>.md (lentelė: URL, CrUX LCP/INP/CLS
p75 su būsena, Lighthouse LCP elementas, TTFB, top 5 galimybės).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_URLS = [
    "https://sleepingexpert.lt/",
    "https://sleepingexpert.lt/produkto-kategorija/ciuziniai/",
    "https://sleepingexpert.lt/produkto-kategorija/lovos/",
    "https://sleepingexpert.lt/produkto-kategorija/pagalves/",
    "https://sleepingexpert.lt/blogas/",
    "https://sleepingexpert.lt/parduotuves/",
]
PSI = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CRUX_HISTORY = "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord"
CRUX_RECORD = "https://chromeuxreport.googleapis.com/v1/records:queryRecord"

# Google slenksčiai (p75)
THRESHOLDS = {"LARGEST_CONTENTFUL_PAINT_MS": (2500, 4000), "INTERACTION_TO_NEXT_PAINT": (200, 500),
              "CUMULATIVE_LAYOUT_SHIFT_SCORE": (10, 25), "EXPERIMENTAL_TIME_TO_FIRST_BYTE": (800, 1800),
              "FIRST_CONTENTFUL_PAINT_MS": (1800, 3000)}
SHORT = {"LARGEST_CONTENTFUL_PAINT_MS": "LCP", "INTERACTION_TO_NEXT_PAINT": "INP",
         "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS", "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "TTFB",
         "FIRST_CONTENTFUL_PAINT_MS": "FCP"}


def get_json(url: str, params: dict, retries: int = 3) -> dict:
    full = url + "?" + urllib.parse.urlencode(params, doseq=True)
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(full, headers={"User-Agent": "se-cwv/1.0"}), timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")[:300]
            if e.code == 429 and i < retries - 1:
                time.sleep(5 * (i + 1))
                continue
            return {"error": {"code": e.code, "message": body}}
        except Exception as e:  # noqa: BLE001
            if i < retries - 1:
                time.sleep(3)
                continue
            return {"error": {"code": 0, "message": str(e)}}
    return {"error": {"code": 0, "message": "retries exhausted"}}


def fmt_metric(name: str, m: dict | None) -> str:
    if not m:
        return "–"
    p = m.get("percentile")
    cat = {"FAST": "✅", "AVERAGE": "⚠️", "SLOW": "🔴"}.get(m.get("category", ""), "")
    if name == "CUMULATIVE_LAYOUT_SHIFT_SCORE":
        return f"{p / 100:.2f} {cat}"
    return f"{p / 1000:.1f}s {cat}" if name != "INTERACTION_TO_NEXT_PAINT" else f"{p}ms {cat}"


def crux_record(url: str, key: str, form_factor: str) -> dict:
    """CrUX API (atskira kvota nuo PSI: 150/min, be dienos limito). Grąžina PSI formato metrics."""
    body = json.dumps({"url": url, "formFactor": form_factor}).encode()
    req = urllib.request.Request(f"{CRUX_RECORD}?key={key}", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": {"code": e.code, "message": e.read().decode(errors="replace")[:200]}}
    except Exception as e:  # noqa: BLE001
        return {"error": {"code": 0, "message": str(e)}}
    names = {"largest_contentful_paint": "LARGEST_CONTENTFUL_PAINT_MS", "interaction_to_next_paint": "INTERACTION_TO_NEXT_PAINT",
             "cumulative_layout_shift": "CUMULATIVE_LAYOUT_SHIFT_SCORE", "experimental_time_to_first_byte": "EXPERIMENTAL_TIME_TO_FIRST_BYTE",
             "first_contentful_paint": "FIRST_CONTENTFUL_PAINT_MS"}
    metrics = {}
    for k, v in d.get("record", {}).get("metrics", {}).items():
        if k not in names:
            continue
        p75 = v.get("percentiles", {}).get("p75")
        p75 = float(p75) * 100 if k == "cumulative_layout_shift" else p75
        good, poor = THRESHOLDS[names[k]]
        metrics[names[k]] = {"percentile": p75, "category": "FAST" if p75 <= good else ("AVERAGE" if p75 <= poor else "SLOW")}
    return {"id": d.get("record", {}).get("key", {}).get("url", url), "metrics": metrics,
            "period": d.get("record", {}).get("collectionPeriod", {})}


def _quota_exhausted(err: dict) -> bool:
    return err.get("code") == 429 and "Queries per day" in str(err.get("message", ""))


def analyze(url: str, strategy: str, key: str | None) -> dict:
    field = None
    if key:  # tikslus GSC šaltinis, nepriklauso nuo PSI dienos kvotos
        rec = crux_record(url, key, "PHONE" if strategy == "mobile" else "DESKTOP")
        if "error" not in rec:
            field = rec
        elif rec["error"].get("code") != 404:
            print(f"   CrUX API klaida: {rec['error']}")
    params = {"url": url, "strategy": strategy, "category": "performance"}
    if key:
        params["key"] = key
    d = get_json(PSI, params)
    if "error" in d and key and _quota_exhausted(d["error"]):
        print("   PSI: rakto dienos kvota išnaudota → bandau anonimiškai")
        params.pop("key", None)
        d = get_json(PSI, params)
    if "error" in d:
        if not field:
            return {"url": url, "error": d["error"]}
        d = {"loadingExperience": {"id": field["id"], "metrics": field["metrics"]}, "lighthouseResult": {},
             "_note": f"Lighthouse nepasiekiamas ({d['error'].get('code')}); CrUX iš CrUX API"}
    elif field:  # CrUX API duomenys tikslesni už PSI įdėtus (visada URL lygmens, jei yra)
        d["loadingExperience"] = {"id": field["id"], "metrics": field["metrics"],
                                  "overall_category": d.get("loadingExperience", {}).get("overall_category")}
    le = d.get("loadingExperience", {})
    ole = d.get("originLoadingExperience", {})
    lh = d.get("lighthouseResult", {})
    a = lh.get("audits", {})
    lcp_el = a.get("largest-contentful-paint-element", {}).get("details", {}).get("items", [])
    lcp_node = ""
    if lcp_el:
        node = lcp_el[0].get("items", [{}])[0].get("node", {}) if "items" in lcp_el[0] else lcp_el[0].get("node", {})
        lcp_node = (node.get("selector") or "") + " | " + (node.get("snippet") or "")[:160]
    cls_items = a.get("layout-shifts", a.get("layout-shift-elements", {})).get("details", {}).get("items", [])
    cls_top = []
    for it in cls_items[:3]:
        node = it.get("node", {})
        cls_top.append({"score": it.get("score"), "selector": node.get("selector"), "snippet": (node.get("snippet") or "")[:140]})
    opps = sorted(
        [(aid, x.get("displayValue"), (x.get("details") or {}).get("overallSavingsMs", 0))
         for aid, x in a.items() if (x.get("details") or {}).get("type") == "opportunity" and (x.get("score") or 1) < 0.9],
        key=lambda t: -(t[2] or 0))[:6]
    return {
        "url": url, "strategy": strategy, "fetched": dt.datetime.now().isoformat(timespec="seconds"),
        "crux_scope": "url" if le.get("id") == url else ("origin" if le else "none"),
        "crux": {SHORT.get(k, k): {"p75": v.get("percentile"), "category": v.get("category")}
                 for k, v in le.get("metrics", {}).items()},
        "crux_origin": {SHORT.get(k, k): {"p75": v.get("percentile"), "category": v.get("category")}
                        for k, v in ole.get("metrics", {}).items()},
        "crux_overall": le.get("overall_category"), "origin_overall": ole.get("overall_category"),
        "lighthouse": {
            "score": (lh.get("categories", {}).get("performance", {}) or {}).get("score"),
            "lcp": a.get("largest-contentful-paint", {}).get("displayValue"),
            "cls": a.get("cumulative-layout-shift", {}).get("displayValue"),
            "tbt": a.get("total-blocking-time", {}).get("displayValue"),
            "ttfb": a.get("server-response-time", {}).get("displayValue"),
            "lcp_element": lcp_node, "cls_top": cls_top, "opportunities": opps,
        },
        "note": d.get("_note", ""),
        "raw_metrics": le.get("metrics", {}),
    }


def crux_history(url: str, key: str, form_factor: str) -> dict:
    body = json.dumps({"url": url, "formFactor": form_factor, "metrics": [
        "largest_contentful_paint", "interaction_to_next_paint", "cumulative_layout_shift"]}).encode()
    req = urllib.request.Request(f"{CRUX_HISTORY}?key={key}", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(errors="replace")[:200]}
    out = {}
    for name, m in d.get("record", {}).get("metrics", {}).items():
        out[name] = [p.get("p75") for p in m.get("percentilesTimeseries", {}).get("p75s", [])]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", help="failas su URL (po vieną eilutėje)")
    ap.add_argument("--strategy", default="mobile", choices=["mobile", "desktop"])
    ap.add_argument("--out", default=os.path.join(ROOT, "build", "cwv"))
    ap.add_argument("--crux-history", action="store_true", help="25 sav. p75 tendencija (reikia GOOGLE_API_KEY)")
    ap.add_argument("--pause", type=float, default=2.0, help="pauzė tarp užklausų (anoniminė kvota)")
    args = ap.parse_args()
    key = os.getenv("GOOGLE_API_KEY")
    urls = [u.strip() for u in open(args.urls, encoding="utf-8")] if args.urls else DEFAULT_URLS
    urls = [u for u in urls if u and not u.startswith("#")]
    os.makedirs(args.out, exist_ok=True)
    stamp = dt.date.today().isoformat()

    results = []
    for u in urls:
        print(f"→ {u} ({args.strategy})", flush=True)
        r = analyze(u, args.strategy, key)
        if "error" in r:
            print(f"   klaida: {r['error']}")
        else:
            c = r["raw_metrics"]
            print("   CrUX", r["crux_scope"], "|",
                  " ".join(f"{SHORT[k]}={fmt_metric(k, c.get(k))}" for k in SHORT if k in c),
                  "| LH", r["lighthouse"]["score"], "LCP", r["lighthouse"]["lcp"], "CLS", r["lighthouse"]["cls"])
            if r["lighthouse"]["lcp_element"]:
                print("   LCP elementas:", r["lighthouse"]["lcp_element"][:200])
        if args.crux_history and key:
            r["history"] = crux_history(u, key, "PHONE" if args.strategy == "mobile" else "DESKTOP")
        results.append(r)
        time.sleep(args.pause)

    jpath = os.path.join(args.out, f"cwv_{stamp}_{args.strategy}.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    lines = [f"# Core Web Vitals – {stamp} ({args.strategy})", "",
             "Šaltinis: PageSpeed Insights API (CrUX 28 d. p75 = tas pats, ką rodo GSC CWV ataskaita; Lighthouse = laboratorinis).", "",
             "| URL | CrUX | LCP | INP | CLS | TTFB | LH | LCP elementas |", "|---|---|---|---|---|---|---|---|"]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['url']} | klaida | | | | | | {r['error'].get('message','')[:80]} |")
            continue
        c = r["raw_metrics"]
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            r["url"].replace("https://sleepingexpert.lt", ""), r["crux_scope"],
            fmt_metric("LARGEST_CONTENTFUL_PAINT_MS", c.get("LARGEST_CONTENTFUL_PAINT_MS")),
            fmt_metric("INTERACTION_TO_NEXT_PAINT", c.get("INTERACTION_TO_NEXT_PAINT")),
            fmt_metric("CUMULATIVE_LAYOUT_SHIFT_SCORE", c.get("CUMULATIVE_LAYOUT_SHIFT_SCORE")),
            fmt_metric("EXPERIMENTAL_TIME_TO_FIRST_BYTE", c.get("EXPERIMENTAL_TIME_TO_FIRST_BYTE")),
            r["lighthouse"]["score"], (r["lighthouse"]["lcp_element"] or "").replace("|", "/")[:90]))
    lines += ["", "## Galimybės (Lighthouse, pagal sutaupomą laiką)", ""]
    for r in results:
        if "error" in r:
            continue
        lines.append(f"**{r['url']}**")
        for oid, dv, ms in r["lighthouse"]["opportunities"]:
            lines.append(f"- {oid}: {dv or ''} ({int(ms or 0)} ms)")
        for it in r["lighthouse"]["cls_top"]:
            lines.append(f"- CLS šaltinis {it['score']}: `{it['selector']}` {it['snippet']}")
        lines.append("")
    mpath = os.path.join(args.out, f"cwv_{stamp}_{args.strategy}.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nĮrašyta: {jpath}\n         {mpath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
