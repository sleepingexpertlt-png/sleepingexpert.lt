#!/usr/bin/env python3
"""Bearer token reverse proxy Hermes MCP serveriui.

Grandinė: cloudflared -> šis proxy (LISTEN_PORT) -> Hermes MCP (UPSTREAM_PORT).

Tikrina "Authorization: Bearer <MCP_AUTH_TOKEN>" pirmoje kiekvieno TCP
ryšio užklausoje, tada permetinėja baitus abiem kryptimis (SSE/streaming
saugu). Tolimesnės užklausos tame pačiame ryšyje nebetikrinamos — ryšys
jau autentifikuotas, o vienintelis klientas yra lokalus cloudflared.
"""
import asyncio
import hmac
import os
import sys

LISTEN_HOST = os.environ.get("LISTEN_HOST", "127.0.0.1")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "9130"))
UPSTREAM_HOST = os.environ.get("UPSTREAM_HOST", "127.0.0.1")
UPSTREAM_PORT = int(os.environ.get("UPSTREAM_PORT", "8000"))
TOKEN = os.environ.get("MCP_AUTH_TOKEN", "")

DENY = (
    b"HTTP/1.1 401 Unauthorized\r\n"
    b"Content-Type: text/plain\r\n"
    b"Connection: close\r\n"
    b"Content-Length: 12\r\n"
    b"\r\n"
    b"Unauthorized"
)

BAD_GATEWAY = (
    b"HTTP/1.1 502 Bad Gateway\r\n"
    b"Connection: close\r\n"
    b"Content-Length: 0\r\n"
    b"\r\n"
)


async def pipe(reader, writer):
    try:
        while True:
            data = await reader.read(65536)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError):
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass


def auth_ok(header_block: bytes) -> bool:
    expected = b"Bearer " + TOKEN.encode()
    for line in header_block.split(b"\r\n"):
        if line.lower().startswith(b"authorization:"):
            value = line.split(b":", 1)[1].strip()
            return hmac.compare_digest(value, expected)
    return False


async def handle(client_r, client_w):
    try:
        head = await asyncio.wait_for(
            client_r.readuntil(b"\r\n\r\n"), timeout=30
        )
    except Exception:
        client_w.close()
        return

    if not auth_ok(head):
        client_w.write(DENY)
        await client_w.drain()
        client_w.close()
        return

    try:
        up_r, up_w = await asyncio.open_connection(UPSTREAM_HOST, UPSTREAM_PORT)
    except OSError:
        client_w.write(BAD_GATEWAY)
        await client_w.drain()
        client_w.close()
        return

    up_w.write(head)
    await up_w.drain()
    await asyncio.gather(pipe(client_r, up_w), pipe(up_r, client_w))


async def main():
    if not TOKEN:
        print("KLAIDA: MCP_AUTH_TOKEN nenustatytas", file=sys.stderr)
        sys.exit(1)
    server = await asyncio.start_server(handle, LISTEN_HOST, LISTEN_PORT)
    print(
        f"mcp-auth-proxy: {LISTEN_HOST}:{LISTEN_PORT} "
        f"-> {UPSTREAM_HOST}:{UPSTREAM_PORT}"
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
