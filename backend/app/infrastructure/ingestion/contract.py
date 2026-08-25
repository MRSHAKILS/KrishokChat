"""R1 — Knowledge-Ingestion Contract shared helpers.

Every knowledge asset (dose reference, crop calendars, fact base, …) must
satisfy these six contract clauses (see
``docs/production_readiness/KNOWLEDGE_INGESTION_CONTRACT.md``):

1. Curated source is a human-editable data file with ``source`` + ``grounding``.
2. Builder is deterministic + offline (no timestamps in payload body).
3. Artifact is versioned, committed, and SHA-256-pinned.
4. Loader is fail-open (returns None on missing/corrupt, never a 500).
5. No fabricated rows.
6. Rejections are archived, not deleted.

This module provides the shared plumbing that enforces clauses 2, 3, and 4,
extracted from the two reference implementations so future assets inherit them
for free without re-implementing.

Reference implementations (the pattern, do not reinvent):
  ``backend/scripts/build_dose_reference.py``
  ``backend/app/infrastructure/verification/dose_reference.py``
  ``backend/scripts/build_crop_calendars.py``
  ``backend/app/infrastructure/agronomy/calendar_store.py``
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TypeVar

logger = logging.getLogger("krishokchat.ingestion")

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Clause 2 + 3: deterministic serialisation and SHA-256 pinning
# ---------------------------------------------------------------------------


def write_deterministic_json(path: Path, payload: dict[str, Any]) -> str:
    """Serialise *payload* to *path* in the canonical contract format:
    - keys sorted recursively (``sort_keys=True``),
    - ``ensure_ascii=False`` (keep Bengali characters readable),
    - 2-space indent,
    - trailing newline,
    - no timestamp in the payload body (put it in a ``provenance`` sub-key).

    Returns the hex SHA-256 of the bytes written.  The caller should record
    this in the artifact's ``provenance.sha256`` field.

    Parent directories are created automatically.  An existing file is
    **overwritten atomically** (tmp file → replace) so a concurrent reader
    never sees a partial write.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    encoded = body.encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(encoded)
    tmp.replace(path)
    return digest


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 of the bytes in *path*; raises on I/O error."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Clause 3: ArtifactProvenance dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArtifactProvenance:
    """Provenance block that every R1-contract artifact must carry.

    Lives in a dedicated ``provenance`` key at the top level of the payload —
    never merged into the data rows, so it cannot corrupt row-level content.

    Fields
    ------
    source_id : str
        Human-readable name of the curated source file or corpus endpoint.
    endpoint_or_file : str
        The actual path or URL the builder read (relative to repo root).
    fetched_at : str
        ISO-8601 datetime string recorded at *build time*, not at load time.
        (The *payload body* must not change on a re-run with the same inputs;
        this field lives in ``provenance``, not in ``facts`` or ``entries``.)
    builder : str
        Relative path of the script that wrote the artifact.
    sha256 : str
        SHA-256 hex digest of the serialised artifact bytes (self-referential
        when the builder writes it last, as both existing builders do).
    """

    source_id: str
    endpoint_or_file: str
    fetched_at: str
    builder: str
    sha256: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "endpoint_or_file": self.endpoint_or_file,
            "fetched_at": self.fetched_at,
            "builder": self.builder,
            "sha256": self.sha256,
        }


# ---------------------------------------------------------------------------
# Clause 4: fail-open loader
# ---------------------------------------------------------------------------


def load_fail_open(path: Path, validate: Callable[[dict[str, Any]], T]) -> T | None:
    """Load a JSON artifact in a fail-open manner.

    *validate* receives the parsed dict and must return a value of type ``T``
    or raise ``ValueError`` / ``KeyError`` / ``TypeError`` if the artifact is
    structurally invalid.

    Returns ``None`` on any error (missing file, corrupt JSON, validation
    failure) — never raises.  The caller is responsible for surfacing the
    honest "feature unavailable" state to the user.

    This mirrors the pattern in ``calendar_store.load_crop_calendars`` and
    ``dose_reference.load_dose_reference``.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
    except FileNotFoundError:
        logger.warning("knowledge artifact not found at %s — feature disabled", path)
        return None
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("knowledge artifact unreadable at %s (%s) — feature disabled", path, exc)
        return None
    try:
        return validate(payload)
    except (KeyError, ValueError, TypeError) as exc:
        logger.warning("knowledge artifact at %s failed validation (%s) — feature disabled", path, exc)
        return None
