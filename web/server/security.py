"""Request guard for a server that must only ever answer its own page.

- Host must be the local app (blocks DNS rebinding).
- Origin, when a browser sends one, must be the local app.
- Cross-site requests are refused outright.
- Anything that is not a plain read needs the per-launch token.
The token lives in memory for one launch and is never written to disk.
"""
from __future__ import annotations

import hmac
import json

SAFE_METHODS = {"GET", "HEAD"}
CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; "
       "base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
EXTRA_HEADERS = [
    (b"x-content-type-options", b"nosniff"),
    (b"referrer-policy", b"no-referrer"),
    (b"cross-origin-opener-policy", b"same-origin"),
    (b"cross-origin-resource-policy", b"same-origin"),
    (b"cache-control", b"no-store"),
    (b"content-security-policy", CSP.encode()),
]


class Guard:
    def __init__(self, app, *, token: str, port: int, extra_origins: tuple[str, ...] = ()):
        self.app = app
        self.token = token
        self.hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        self.origins = {f"http://127.0.0.1:{port}", f"http://localhost:{port}", *extra_origins}
        for origin in extra_origins:
            self.hosts.add(origin.split("://", 1)[1])

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            return await self.app(scope, receive, send)
        if scope["type"] != "http":
            return
        headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope["headers"]}
        if headers.get("host", "") not in self.hosts:
            return await self._deny(send, "host not allowed")
        origin = headers.get("origin")
        if origin is not None and origin not in self.origins:
            return await self._deny(send, "origin not allowed")
        if headers.get("sec-fetch-site", "same-origin") not in ("same-origin", "none"):
            return await self._deny(send, "cross-site request refused")
        if scope["method"] not in SAFE_METHODS:
            supplied = headers.get("x-mc-token", "")
            if not hmac.compare_digest(supplied.encode(), self.token.encode()):
                return await self._deny(send, "missing or wrong session token")

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                present = {k.lower() for k, _ in message.get("headers", [])}
                message.setdefault("headers", [])
                message["headers"] = list(message["headers"]) + [h for h in EXTRA_HEADERS if h[0] not in present]
            await send(message)

        await self.app(scope, receive, send_with_headers)

    @staticmethod
    async def _deny(send, reason: str):
        body = json.dumps({"error": "refused", "reason": reason}).encode()
        await send({"type": "http.response.start", "status": 403,
                    "headers": [(b"content-type", b"application/json"),
                                (b"content-length", str(len(body)).encode()), *EXTRA_HEADERS]})
        await send({"type": "http.response.body", "body": body})
