"""T0-04: structured JSON logging for the krishokchat app logger.

stdlib-only (``contextvars`` + ``logging`` + a small formatter): every record
becomes one JSON object with ``ts``, ``level``, ``logger``, ``msg``,
``request_id`` (from the middleware contextvar), plus serializable extras
passed via ``logging`` ``extra=`` kwargs.
"""

from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from datetime import datetime, timezone

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

_RESERVED = frozenset(
    {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "taskName",
        "thread",
        "threadName",
    }
)


class JSONFormatter(logging.Formatter):
    """One JSON object per record: ts, level, logger, msg, request_id + extras."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": request_id_var.get(),
        }
        for key, value in record.__dict__.items():
            if key in payload or key in _RESERVED or key.startswith("_"):
                continue
            if not isinstance(value, (str, int, float, bool, type(None))):
                continue
            payload[key] = value
        if record.exc_info:
            payload["traceback"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(level: str | int = logging.INFO) -> None:
    """Attach the JSON formatter to the ``krishokchat`` app logger.

    Idempotent: existing handlers on that logger are replaced, so repeated
    calls (e.g. per ``create_app`` in tests) never stack duplicate handlers.
    """
    logger = logging.getLogger("krishokchat")
    logger.setLevel(level)
    logger.propagate = False
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)