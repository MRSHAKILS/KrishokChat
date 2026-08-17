"""T0-04: request-ID middleware.

Pure-ASGI pass-through middleware: echoes a client-supplied request ID when it
is well-formed, otherwise generates a uuid4 hex. Never rejects, redirects, or
authenticates. The ID is stored in a contextvar so application log records can
carry it, and is cleared after the response completes.

Chosen over BaseHTTPMiddleware because the app serves SSE streams
(``/api/qa/stream``) and BaseHTTPMiddleware historically buffers/rewraps
streaming responses; a ~40-line ASGI wrapper passes the send callable straight
through and has no such interaction.
"""

from __future__ import annotations

import re
import uuid

from app.core.logging import request_id_var

_MAX_HEADER_LEN = 128
_HEADER_RE = re.compile(r"^[A-Za-z0-9-]+$")


class RequestIDMiddleware:
    """Echo a valid client request ID or generate one; store it in a contextvar."""

    def __init__(self, app, header_name: str = "X-Request-ID") -> None:
        self.app = app
        self.header_name = header_name
        self.header_bytes = header_name.lower().encode("latin-1")

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = self._resolve_request_id(scope)
        # P0-3: also expose the ID via ASGI scope state. Exception handlers run
        # OUTSIDE this middleware (Starlette's ServerErrorMiddleware catches
        # after our finally already reset the contextvar), so the contextvar
        # alone would be blank in 500 envelopes — scope state survives.
        scope.setdefault("state", {})["request_id"] = request_id
        token = request_id_var.set(request_id)
        try:
            await self.app(scope, receive, self._send_with_request_id(send, request_id))
        finally:
            request_id_var.reset(token)

    def _resolve_request_id(self, scope) -> str:
        """Return a valid client-supplied ID or a fresh uuid4 hex.

        Client garbage is never trusted: anything malformed (wrong charset,
        too long, empty, duplicate header) falls back to a generated ID.
        """
        for name, value in scope.get("headers", []):
            if name != self.header_bytes:
                continue
            raw = value.decode("latin-1")
            if 0 < len(raw) <= _MAX_HEADER_LEN and _HEADER_RE.fullmatch(raw):
                return raw
            break
        return uuid.uuid4().hex

    def _send_with_request_id(self, send, request_id):
        header = (self.header_bytes, request_id.encode("latin-1"))

        async def sender(message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                if not any(name == self.header_bytes for name, _ in headers):
                    headers.append(header)
                message = dict(message, headers=headers)
            await send(message)

        return sender