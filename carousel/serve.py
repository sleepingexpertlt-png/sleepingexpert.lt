#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mazas vietinis serveris karuselei.

Atiduoda `player/` kaip `/` ir `data/` kaip `/data/`. Tik standartine biblioteka.

    python3 serve.py                 # http://localhost:8080
    python3 serve.py --port 8000 --host 127.0.0.1
"""

from __future__ import annotations

import argparse
import os
import posixpath
import socket
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYER_DIR = os.path.join(HERE, "player")
DATA_DIR = os.path.join(HERE, "data")

EXTRA_TYPES = {
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".svg": "image/svg+xml",
    ".json": "application/json; charset=utf-8",
}


class CarouselHandler(SimpleHTTPRequestHandler):
    server_version = "SleepingExpertCarousel/1.0"

    def translate_path(self, path: str) -> str:
        path = urllib.parse.urlparse(path).path
        path = posixpath.normpath(urllib.parse.unquote(path))
        parts = [part for part in path.split("/") if part and part not in (".", "..")]
        if parts and parts[0] == "data":
            root, parts = DATA_DIR, parts[1:]
        else:
            root = PLAYER_DIR
        return os.path.join(root, *parts)

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in EXTRA_TYPES:
            return EXTRA_TYPES[ext]
        return super().guess_type(path)

    def end_headers(self):
        # ekranas visada turi matyti sviežiausius duomenis
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def log_message(self, fmt, *args):
        # args gali buti ne tik tekstas (pvz. HTTPStatus), todel visada verciame i eilute
        line = " ".join(str(arg) for arg in args)
        if "?t=" in line:
            return  # netrikdome zurnalo periodiniais duomenu atnaujinimais
        super().log_message(fmt, *args)


def local_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        sock.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sleeping Expert karuseles serveris")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    if not os.path.exists(os.path.join(DATA_DIR, "products.json")):
        print("! Nerasta data/products.json — pirmiausia paleisk:  python3 fetch_products.py --demo")

    server = ThreadingHTTPServer((args.host, args.port), CarouselHandler)
    print("Karuselė veikia:")
    print("  vietoje:  http://localhost:%d/" % args.port)
    if args.host == "0.0.0.0":
        print("  tinkle:   http://%s:%d/   (TV / stendui)" % (local_ip(), args.port))
    print("Sustabdyti — Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSustabdyta.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
