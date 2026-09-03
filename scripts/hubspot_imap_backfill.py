#!/usr/bin/env python3
"""
Sukelia info@sleepingexpert.lt (Hostinger Email, IMAP) laiškų istoriją į HubSpot
kaip "Email" veiklas (engagements) prie atitinkamų kontaktų.

Kam tai reikalinga: HubSpot, prijungus pašto dėžutę, logina TIK naujus laiškus.
Senoji istorija (2024–2026) į CRM nepatenka. Šis skriptas ją perkelia vieną kartą.

Naudojimas (numatytasis režimas — DRY RUN, į HubSpot nieko nerašoma):

    python3 scripts/hubspot_imap_backfill.py --list-folders
    python3 scripts/hubspot_imap_backfill.py --folder INBOX --since 2024-01-01
    python3 scripts/hubspot_imap_backfill.py --folder INBOX.Sent --since 2024-01-01
    python3 scripts/hubspot_imap_backfill.py --folder INBOX --since 2024-01-01 --apply

Kas daroma su kiekvienu laišku:
  1. Nustatoma kryptis: iš mūsų adreso -> išsiųstas (EMAIL), kitaip -> gautas (INCOMING_EMAIL).
  2. Nustatomas pašnekovas (kitas adresas nei mūsų). Sisteminiai / noreply / ignoruojamų domenų
     laiškai praleidžiami (Google Ads, LinkedIn, sąskaitų robotai ir pan.).
  3. HubSpot'e ieškomas kontaktas pagal el. paštą. Jei nėra — praleidžiama, nebent --create-contacts.
  4. Pagal Message-ID patikrinama, ar laiškas jau įkeltas (idempotentiška — galima leisti pakartotinai).
  5. Sukuriamas Email objektas (/crm/v3/objects/emails) su tekstu, tema, data, antraštėmis ir
     susiejamas su kontaktu (association type 198 = email -> contact).

Slaptažodžiai (IMAP slaptažodis, HubSpot token) NIEKUR nerašomi komandų eilutėje ir jokiame pokalbyje.
Skriptas jų paklausia interaktyviai (įvedant ekrane nesimato) arba skaito iš failų:

    ~/.se-pastas/imap_password    ir    ~/.se-pastas/hubspot_token     (teisės 0600)

Aplinkos kintamieji IMAP_PASSWORD / HUBSPOT_TOKEN irgi veikia, bet nerekomenduojami —
lieka shell istorijoje. IMAP_USER numatytasis: info@sleepingexpert.lt.

Tik standartinė Python 3 biblioteka, jokių priklausomybių.
"""
from __future__ import annotations

import argparse
import csv
import email
import email.header
import email.utils
import html
import getpass
import imaplib
import json
import os
import stat
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.message import Message
from typing import Iterable

HUBSPOT_API = "https://api.hubapi.com"
EMAIL_TO_CONTACT_ASSOCIATION_TYPE_ID = 198  # HubSpot-defined: Email -> Contact
MAX_BODY_CHARS = 60_000  # hs_email_text riba HubSpot'e ~65k

DEFAULT_OUR_ADDRESSES = ["info@sleepingexpert.lt"]

# Domenai, kurių laiškų į CRM nekeliame (sisteminiai pranešimai, reklamos platformos, SaaS).
DEFAULT_SKIP_DOMAINS = [
    "google.com", "googlemail.com", "gmail.com-noreply", "accounts.google.com", "ads.google.com",
    "linkedin.com", "hubspot.com", "anthropic.com", "mail.anthropic.com", "email.anthropic.com",
    "microsoft.com", "communication.microsoft.com", "facebook.com", "facebookmail.com", "meta.com",
    "tiktok.com", "paddle.com", "fastspring.com", "temu.com", "eu-order.temu.com", "orders.temu.com",
    "every-pay.com", "ivesk.lt", "iki.lt", "pastas.iki.lt", "worldline-solutions.com",
    "invoice123.com", "notifications.hubspot.com", "supabase.com", "vercel.com", "github.com",
    "zilliz.com", "news.zilliz.com", "openrouter.ai", "moonshot.kimi.ai", "groq.co",
    "deepseek.com", "nvidia.com", "tumblr.com", "youtube.com", "portermetrics.com", "clarify.ai",
    "originality.ai", "linear.app", "updates.linear.app", "bonami.lt", "biurogidas.lt-ml",
]

# Vietinės dalys (prieš @), kurios reiškia robotą, o ne žmogų.
NOREPLY_LOCALPART = re.compile(
    r"^(no[-_.]?reply|noreply|donotreply|do[-_.]not[-_.]reply|notifications?|notice|alerts?|"
    r"mailer|mailer-daemon|postmaster|bounce[s]?|newsletter|news|updates?|marketing|marketingas|"
    r"support\+news|invoice\+statements|failed-payments|payments-noreply|shopping-noreply|"
    r"businessprofile-noreply|adctr|msa)$",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------------------
# Laiškų parsinimas
# --------------------------------------------------------------------------------------

@dataclass
class ParsedMail:
    message_id: str
    date: datetime
    subject: str
    from_addr: str
    from_name: str
    to: list[tuple[str, str]]  # (name, email)
    cc: list[tuple[str, str]]
    text: str
    direction: str = ""  # EMAIL (išsiųstas) | INCOMING_EMAIL (gautas)
    counterparts: list[str] = field(default_factory=list)


def decode_header_value(raw: str | None) -> str:
    if not raw:
        return ""
    parts = email.header.decode_header(raw)
    out = []
    for value, charset in parts:
        if isinstance(value, bytes):
            try:
                out.append(value.decode(charset or "utf-8", errors="replace"))
            except LookupError:
                out.append(value.decode("utf-8", errors="replace"))
        else:
            out.append(value)
    return "".join(out).strip()


def parse_addresses(raw: str | None) -> list[tuple[str, str]]:
    if not raw:
        return []
    decoded = decode_header_value(raw)
    result = []
    for name, addr in email.utils.getaddresses([decoded]):
        addr = addr.strip().lower()
        if addr and "@" in addr:
            result.append((name.strip().strip('"'), addr))
    return result


_TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
_BR_RE = re.compile(r"<\s*(br|/p|/div|/tr|/li|/h[1-6])\s*/?>", re.IGNORECASE)
_ANY_TAG_RE = re.compile(r"<[^>]+>")


def html_to_text(raw_html: str) -> str:
    txt = _TAG_RE.sub("", raw_html)
    txt = _BR_RE.sub("\n", txt)
    txt = _ANY_TAG_RE.sub("", txt)
    txt = html.unescape(txt)
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    txt = re.sub(r"\n\s*\n\s*\n+", "\n\n", txt)
    return txt.strip()


def _payload_text(part: Message) -> str:
    payload = part.get_payload(decode=True)
    if payload is None:
        return ""
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def extract_text(msg: Message) -> str:
    """Grąžina text/plain jei yra, kitaip HTML paverstą tekstu."""
    plain, html_body = "", ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if "attachment" in disp.lower():
                continue
            if ctype == "text/plain" and not plain:
                plain = _payload_text(part)
            elif ctype == "text/html" and not html_body:
                html_body = _payload_text(part)
    else:
        if msg.get_content_type() == "text/html":
            html_body = _payload_text(msg)
        else:
            plain = _payload_text(msg)
    text = plain.strip() or html_to_text(html_body)
    return text[:MAX_BODY_CHARS]


def parse_message(raw: bytes, our_addresses: Iterable[str]) -> ParsedMail | None:
    msg = email.message_from_bytes(raw)
    ours = {a.lower() for a in our_addresses}

    message_id = (msg.get("Message-ID") or "").strip()
    date_hdr = msg.get("Date")
    try:
        dt = email.utils.parsedate_to_datetime(date_hdr) if date_hdr else None
    except (TypeError, ValueError):
        dt = None
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    from_list = parse_addresses(msg.get("From"))
    from_name, from_addr = (from_list[0] if from_list else ("", ""))
    to = parse_addresses(msg.get("To"))
    cc = parse_addresses(msg.get("Cc"))
    subject = decode_header_value(msg.get("Subject")) or "(be temos)"

    if not message_id:
        # Sintetinis ID, kad idempotencija veiktų ir be Message-ID
        message_id = f"<synthetic-{int(dt.timestamp())}-{abs(hash((from_addr, subject))) % 10**10}@backfill>"

    direction = "EMAIL" if from_addr in ours else "INCOMING_EMAIL"
    if direction == "EMAIL":
        counterparts = [a for _, a in to + cc if a not in ours]
    else:
        counterparts = [from_addr] if from_addr else []

    return ParsedMail(
        message_id=message_id, date=dt, subject=subject, from_addr=from_addr, from_name=from_name,
        to=to, cc=cc, text=extract_text(msg), direction=direction,
        counterparts=list(dict.fromkeys(counterparts)),
    )


def is_noise_address(addr: str, skip_domains: Iterable[str]) -> bool:
    local, _, domain = addr.lower().partition("@")
    if NOREPLY_LOCALPART.match(local):
        return True
    for d in skip_domains:
        d = d.lower()
        if domain == d or domain.endswith("." + d):
            return True
    return False


def split_name(display_name: str) -> tuple[str, str]:
    name = display_name.strip().strip('"')
    if not name or "@" in name:
        return "", ""
    parts = name.split()
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


# --------------------------------------------------------------------------------------
# HubSpot API
# --------------------------------------------------------------------------------------

class HubSpot:
    def __init__(self, token: str, owner_id: str | None = None, sleep_s: float = 0.12):
        self.token = token
        self.owner_id = owner_id
        self.sleep_s = sleep_s
        self._contact_cache: dict[str, str | None] = {}

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        url = HUBSPOT_API + path
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Content-Type", "application/json")
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    time.sleep(self.sleep_s)
                    raw = resp.read()
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code >= 500:
                    wait = float(e.headers.get("Retry-After") or (2 ** attempt))
                    time.sleep(wait)
                    continue
                detail = e.read().decode(errors="replace")
                raise RuntimeError(f"HubSpot {method} {path} -> {e.code}: {detail}") from None
        raise RuntimeError(f"HubSpot {method} {path}: per daug bandymų (429/5xx)")

    def contact_info(self, addr: str) -> dict | None:
        """Grąžina {'id', 'lifecyclestage', 'num_associated_deals'} arba None."""
        addr = addr.lower()
        if addr in self._contact_cache:
            return self._contact_cache[addr]
        body = {
            "filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": addr}]}],
            "properties": ["email", "lifecyclestage", "num_associated_deals"],
            "limit": 1,
        }
        res = self._request("POST", "/crm/v3/objects/contacts/search", body)
        results = res.get("results") or []
        info = None
        if results:
            props = results[0].get("properties") or {}
            info = {
                "id": str(results[0]["id"]),
                "lifecyclestage": props.get("lifecyclestage") or "",
                "num_associated_deals": props.get("num_associated_deals") or "0",
            }
        self._contact_cache[addr] = info
        return info

    def find_contact_by_email(self, addr: str) -> str | None:
        info = self.contact_info(addr)
        return info["id"] if info else None

    def create_contact(self, addr: str, display_name: str) -> str:
        first, last = split_name(display_name)
        props = {"email": addr, "lifecyclestage": "lead"}
        if first:
            props["firstname"] = first
        if last:
            props["lastname"] = last
        if self.owner_id:
            props["hubspot_owner_id"] = self.owner_id
        res = self._request("POST", "/crm/v3/objects/contacts", {"properties": props})
        cid = str(res["id"])
        self._contact_cache[addr.lower()] = {"id": cid, "lifecyclestage": "lead",
                                             "num_associated_deals": "0"}
        return cid

    def email_exists(self, message_id: str) -> bool:
        body = {
            "filterGroups": [{"filters": [
                {"propertyName": "hs_email_message_id", "operator": "EQ", "value": message_id}
            ]}],
            "properties": ["hs_email_message_id"],
            "limit": 1,
        }
        res = self._request("POST", "/crm/v3/objects/emails/search", body)
        return bool(res.get("results"))

    def create_email(self, mail: ParsedMail, contact_ids: list[str]) -> str:
        headers = {
            "from": {"email": mail.from_addr, "firstName": split_name(mail.from_name)[0],
                     "lastName": split_name(mail.from_name)[1]},
            "to": [{"email": a} for _, a in mail.to],
            "cc": [{"email": a} for _, a in mail.cc],
            "bcc": [],
        }
        props = {
            "hs_timestamp": str(int(mail.date.timestamp() * 1000)),
            "hs_email_direction": mail.direction,
            "hs_email_status": "SENT",
            "hs_email_subject": mail.subject[:255],
            "hs_email_text": mail.text,
            "hs_email_headers": json.dumps(headers, ensure_ascii=False),
            "hs_email_message_id": mail.message_id,
        }
        if self.owner_id:
            props["hubspot_owner_id"] = self.owner_id
        associations = [
            {"to": {"id": cid},
             "types": [{"associationCategory": "HUBSPOT_DEFINED",
                        "associationTypeId": EMAIL_TO_CONTACT_ASSOCIATION_TYPE_ID}]}
            for cid in contact_ids
        ]
        res = self._request("POST", "/crm/v3/objects/emails",
                            {"properties": props, "associations": associations})
        return str(res["id"])


# --------------------------------------------------------------------------------------
# IMAP
# --------------------------------------------------------------------------------------

def imap_connect(host: str, port: int, user: str, password: str) -> imaplib.IMAP4_SSL:
    conn = imaplib.IMAP4_SSL(host, port)
    conn.login(user, password)
    return conn


def imap_list_folders(conn: imaplib.IMAP4_SSL) -> list[str]:
    typ, data = conn.list()
    out = []
    for line in data or []:
        if not line:
            continue
        decoded = line.decode(errors="replace") if isinstance(line, bytes) else str(line)
        m = re.search(r'"([^"]*)"\s*$|(\S+)\s*$', decoded)
        if m:
            out.append(m.group(1) or m.group(2))
    return out


def imap_search_uids(conn: imaplib.IMAP4_SSL, folder: str, since: str | None, before: str | None) -> list[bytes]:
    typ, _ = conn.select(f'"{folder}"', readonly=True)
    if typ != "OK":
        raise RuntimeError(f"Nepavyko atidaryti aplanko {folder!r}")
    criteria = []
    if since:
        criteria += ["SINCE", datetime.strptime(since, "%Y-%m-%d").strftime("%d-%b-%Y")]
    if before:
        criteria += ["BEFORE", datetime.strptime(before, "%Y-%m-%d").strftime("%d-%b-%Y")]
    typ, data = conn.uid("search", None, *(criteria or ["ALL"]))
    if typ != "OK":
        raise RuntimeError("IMAP SEARCH nepavyko")
    return data[0].split() if data and data[0] else []


def imap_fetch(conn: imaplib.IMAP4_SSL, uid: bytes) -> bytes | None:
    typ, data = conn.uid("fetch", uid, "(BODY.PEEK[])")
    if typ != "OK" or not data:
        return None
    for item in data:
        if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], bytes):
            return item[1]
    return None


# --------------------------------------------------------------------------------------
# Pagrindinė eiga
# --------------------------------------------------------------------------------------

def aggregate_counterparts(agg: dict, mail: ParsedMail, skip_domains: Iterable[str]) -> None:
    """Kaupia statistiką pagal kiekvieną pašnekovą (kas rašė, kiek kartų, kada)."""
    for addr in mail.counterparts:
        entry = agg.setdefault(addr, {
            "email": addr, "name": "", "domain": addr.split("@")[-1],
            "gauta": 0, "issiusta": 0, "pirmas": mail.date, "paskutinis": mail.date,
            "paskutine_tema": "", "sisteminis": is_noise_address(addr, skip_domains),
        })
        if mail.direction == "INCOMING_EMAIL":
            entry["gauta"] += 1
            if not entry["name"] and mail.from_name:
                entry["name"] = mail.from_name
        else:
            entry["issiusta"] += 1
            if not entry["name"]:
                entry["name"] = next((n for n, a in mail.to + mail.cc if a == addr and n), "")
        if mail.date < entry["pirmas"]:
            entry["pirmas"] = mail.date
        if mail.date >= entry["paskutinis"]:
            entry["paskutinis"] = mail.date
            entry["paskutine_tema"] = mail.subject


def suggest_action(entry: dict) -> str:
    """Siūlymas, ką su šiuo adresu daryti CRM'e."""
    if entry["sisteminis"]:
        return "IGNORUOTI — sisteminis/noreply adresas"
    stage = entry.get("hubspot_lifecyclestage") or ""
    if entry.get("hubspot_id"):
        if stage == "customer":
            return "ESAMAS KLIENTAS — laiškus kelti prie kortelės"
        if stage == "other":
            return "PARTNERIS/TIEKĖJAS — kelti laiškus, į marketingą neįtraukti"
        return "ESAMAS KONTAKTAS — kelti laiškus"
    if entry["issiusta"] and entry["gauta"]:
        return "NAUJAS LEAD — susirašinėjome abipusiai, verta sukurti kontaktą"
    if entry["gauta"] and not entry["issiusta"]:
        return "PERŽIŪRĖTI — rašė mums, bet neatsakėme (galimas prarastas lead)"
    return "PERŽIŪRĖTI — rašėme mes, atsakymo nebuvo"


def write_summary(path: str, agg: dict) -> None:
    fields = ["email", "name", "domain", "gauta", "issiusta", "viso", "pirmas", "paskutinis",
              "paskutine_tema", "hubspot_id", "hubspot_lifecyclestage", "hubspot_sandoriai",
              "siulymas"]
    rows = []
    for e in agg.values():
        rows.append({
            "email": e["email"], "name": e["name"], "domain": e["domain"],
            "gauta": e["gauta"], "issiusta": e["issiusta"], "viso": e["gauta"] + e["issiusta"],
            "pirmas": e["pirmas"].date().isoformat(), "paskutinis": e["paskutinis"].date().isoformat(),
            "paskutine_tema": e["paskutine_tema"],
            "hubspot_id": e.get("hubspot_id", ""),
            "hubspot_lifecyclestage": e.get("hubspot_lifecyclestage", ""),
            "hubspot_sandoriai": e.get("hubspot_sandoriai", ""),
            "siulymas": suggest_action(e),
        })
    rows.sort(key=lambda r: (-r["viso"], r["email"]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


SECRET_DIR = os.path.expanduser("~/.se-pastas")


def read_secret(name: str, env_var: str, prompt: str, required: bool = True) -> str | None:
    """Slaptažodis iš: 1) aplinkos kintamojo, 2) failo ~/.se-pastas/<name>, 3) interaktyvaus klausimo.

    Failas turi būti pasiekiamas tik savininkui (0600); kitaip įspėjama, bet skaitoma.
    Interaktyvus klausimas rodomas tik jei terminalas interaktyvus; kitaip grąžinama None.
    """
    val = os.environ.get(env_var)
    if val:
        return val.strip()
    path = os.path.join(SECRET_DIR, name)
    if os.path.exists(path):
        mode = stat.S_IMODE(os.stat(path).st_mode)
        if mode & 0o077:
            print(f"ĮSPĖJIMAS: {path} teisės {oct(mode)} — pataisykite: chmod 600 {path}", file=sys.stderr)
        with open(path, encoding="utf-8") as f:
            val = f.read().strip()
        if val:
            return val
    if sys.stdin.isatty():
        val = getpass.getpass(prompt)
        if val:
            return val.strip()
    if required:
        print(f"Trūksta {name}: nustatykite {env_var}, įrašykite į {path} (chmod 600) "
              f"arba paleiskite interaktyviame terminale.", file=sys.stderr)
    return None


def load_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"done_message_ids": [], "skipped": {}}


def save_state(path: str, state: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--imap-host", default=os.environ.get("IMAP_HOST", "imap.hostinger.com"))
    p.add_argument("--imap-port", type=int, default=int(os.environ.get("IMAP_PORT", "993")))
    p.add_argument("--folder", default="INBOX", help='IMAP aplankas, pvz. INBOX arba "INBOX.Sent"')
    p.add_argument("--list-folders", action="store_true", help="Tik parodyti aplankus ir baigti")
    p.add_argument("--since", help="YYYY-MM-DD (imtinai)")
    p.add_argument("--before", help="YYYY-MM-DD (neimtinai)")
    p.add_argument("--limit", type=int, default=0, help="Apdoroti ne daugiau N laiškų (0 = visus)")
    p.add_argument("--apply", action="store_true", help="Rašyti į HubSpot (be šio — dry run)")
    p.add_argument("--create-contacts", action="store_true",
                   help="Kurti kontaktus, kurių HubSpot'e nėra (numatyta: praleisti tokius laiškus)")
    p.add_argument("--our-address", action="append", default=None,
                   help="Mūsų adresas (galima kartoti). Numatyta: info@sleepingexpert.lt")
    p.add_argument("--skip-domain", action="append", default=[], help="Papildomas ignoruojamas domenas")
    p.add_argument("--state-file", default="hubspot_backfill_state.json")
    p.add_argument("--report-csv", default="hubspot_backfill_report.csv")
    p.add_argument("--summary-csv", default="hubspot_backfill_contacts.csv",
                   help="Suvestinė pagal pašnekovą su siūlymu, ką daryti CRM'e")
    p.add_argument("--owner-id", default=os.environ.get("HUBSPOT_OWNER_ID", "92125541"),
                   help="HubSpot owner ID, kuriam priskiriamos veiklos")
    args = p.parse_args(argv)

    our_addresses = args.our_address or DEFAULT_OUR_ADDRESSES
    skip_domains = DEFAULT_SKIP_DOMAINS + args.skip_domain

    user = os.environ.get("IMAP_USER") or our_addresses[0]
    password = read_secret("imap_password", "IMAP_PASSWORD", f"Pašto slaptažodis ({user}): ")
    if not password:
        return 2

    conn = imap_connect(args.imap_host, args.imap_port, user, password)
    del password
    if args.list_folders:
        for f in imap_list_folders(conn):
            print(f)
        conn.logout()
        return 0

    hs: HubSpot | None = None
    # Dry run: token nebūtinas, bet su juo lentelė rodo, kas jau yra HubSpot'e.
    # --apply: token privalomas.
    token = read_secret("hubspot_token", "HUBSPOT_TOKEN",
                        "HubSpot Private App token (Enter = praleisti, tik dry run): ",
                        required=args.apply)
    if args.apply and not token:
        print("--apply reikalauja HubSpot token", file=sys.stderr)
        conn.logout()
        return 2
    if token:
        hs = HubSpot(token, owner_id=args.owner_id)
    del token

    state = load_state(args.state_file)
    done = set(state["done_message_ids"])

    uids = imap_search_uids(conn, args.folder, args.since, args.before)
    if args.limit:
        uids = uids[-args.limit:]
    print(f"Aplankas {args.folder}: {len(uids)} laiškų atitinka filtrą. Režimas: "
          f"{'APPLY (rašoma į HubSpot)' if args.apply else 'DRY RUN'}")

    counts = {"total": 0, "logged": 0, "already": 0, "noise": 0, "no_contact": 0,
              "no_counterpart": 0, "unparsable": 0, "created_contacts": 0}
    rows = []
    agg: dict[str, dict] = {}
    for uid in uids:
        counts["total"] += 1
        raw = imap_fetch(conn, uid)
        mail = parse_message(raw, our_addresses) if raw else None
        if mail is None:
            counts["unparsable"] += 1
            continue
        row = {"date": mail.date.isoformat(), "direction": mail.direction, "from": mail.from_addr,
               "counterparts": ";".join(mail.counterparts), "subject": mail.subject, "action": ""}
        rows.append(row)
        aggregate_counterparts(agg, mail, skip_domains)

        if mail.message_id in done:
            counts["already"] += 1
            row["action"] = "already-logged"
            continue
        if not mail.counterparts:
            counts["no_counterpart"] += 1
            row["action"] = "skip:no-counterpart"
            continue
        real = [a for a in mail.counterparts if not is_noise_address(a, skip_domains)]
        if not real:
            counts["noise"] += 1
            row["action"] = "skip:noise"
            continue

        contact_ids: list[str] = []
        if hs:
            for addr in real:
                cid = hs.find_contact_by_email(addr)
                if not cid and args.create_contacts and args.apply:
                    name = mail.from_name if addr == mail.from_addr else \
                        next((n for n, a in mail.to + mail.cc if a == addr), "")
                    cid = hs.create_contact(addr, name)
                    counts["created_contacts"] += 1
                if cid:
                    contact_ids.append(cid)
            if not contact_ids:
                counts["no_contact"] += 1
                row["action"] = "skip:no-contact-in-hubspot"
                continue
            if hs.email_exists(mail.message_id):
                counts["already"] += 1
                row["action"] = "already-logged"
                done.add(mail.message_id)
                continue

        if args.apply and hs:
            eid = hs.create_email(mail, contact_ids)
            row["action"] = f"logged:{eid}"
            done.add(mail.message_id)
            state["done_message_ids"] = sorted(done)
            save_state(args.state_file, state)
        else:
            row["action"] = "would-log" + (f" -> contacts {contact_ids}" if contact_ids else "")
        counts["logged"] += 1

    conn.logout()

    # Kiekvienam pašnekovui pažiūrime, ar jis jau yra HubSpot'e
    if hs:
        for addr, entry in agg.items():
            if entry["sisteminis"]:
                continue
            info = hs.contact_info(addr)
            if info:
                entry["hubspot_id"] = info["id"]
                entry["hubspot_lifecyclestage"] = info["lifecyclestage"]
                entry["hubspot_sandoriai"] = info["num_associated_deals"]

    with open(args.report_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "direction", "from", "counterparts", "subject", "action"])
        w.writeheader()
        w.writerows(rows)
    write_summary(args.summary_csv, agg)

    print("\nSuvestinė:")
    for k, v in counts.items():
        print(f"  {k:18} {v}")

    by_suggestion: dict[str, int] = {}
    for e in agg.values():
        key = suggest_action(e).split(" — ")[0]
        by_suggestion[key] = by_suggestion.get(key, 0) + 1
    print(f"\nPašnekovai ({len(agg)} unikalūs adresai):")
    for k, v in sorted(by_suggestion.items(), key=lambda kv: -kv[1]):
        print(f"  {k:22} {v}")

    print(f"\nLaiškų ataskaita:      {args.report_csv}")
    print(f"Pašnekovų suvestinė:   {args.summary_csv}")
    if args.apply:
        print(f"Būsena:                {args.state_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
