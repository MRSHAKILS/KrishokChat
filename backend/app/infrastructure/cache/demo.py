"""Demo answer cache (B1): JSON-file-backed replay of verified answers.

Why it exists: the curated demo questions are asked repeatedly against a live
pipeline. With DEMO_MODE=true the server stores the first verified answer for
each normalized question and replays it on subsequent hits after a fresh safety
decision. A hit avoids retrieval, generation, and verification work while the
safety router still runs every time. Only safe_agri results with no generation
error are stored, and the stored payload keeps the original sources and
verifier stamps so the UI renders consistently.

Honesty rules:
- Cached replays still write audit rows (with ``cached: true``) so the demo
  metrics panel never hides them; the panel excludes replays from
  per-stage aggregates (they are not new retrieval/verifier events).
- The cache key includes the detected crop/disease context, model, and corpus
  version, so a cached answer is never replayed into a different context or
  after a retrieval-corpus rebuild (P0-7).
- Cache lookup occurs only after the current safety decision. A real terminal
  decision (deterministic rule, classifier refusal) always wins and never
  replays. The single exception: when the classifier provider is unreachable
  (fail-closed outage), the curated safe_agri entry for the exact question may
  replay so the demo keeps working offline; anything not in the cache still
  fails closed.
"""

from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from typing import Any

from app.domain.contracts import (
    PipelineEvent,
    QAResult,
    RetrievedSource,
    VerifierClaim,
)
from app.domain.enums import PipelineStage, ResolutionTier, SafetyCategory, StageStatus, VerificationConfidence


# --------------------------------------------------------------------------
# QAResult <-> dict serialization (the cache file format).
# --------------------------------------------------------------------------


def qa_result_to_dict(result: QAResult) -> dict[str, Any]:
    return {
        "query": result.query,
        "category": result.category.value,
        "answer": result.answer,
        "confidence": result.confidence.value,
        "model": result.model,
        "error": result.error,
        "matched_rules": list(result.matched_rules),
        "safety_reason": result.safety_reason,
        # R3: tier stored so replays report the original tier, not the default.
        "resolution_tier": result.resolution_tier.value,
        "sources": [
            {
                "id": source.id,
                "score": source.score,
                "title_en": source.title_en,
                "title_bn": source.title_bn,
                "content_en": source.content_en,
                "content_bn": source.content_bn,
                "source": source.source,
                "citation": source.citation,
                "metadata": source.metadata,
            }
            for source in result.sources
        ],
        "trace": [
            {
                "stage": event.stage.value,
                "status": event.status.value,
                "detail": event.detail,
                "event_type": event.event_type,
                "text": event.text,
            }
            for event in result.trace
        ],
        "verifier_flags": list(result.verifier_flags),
        "verifier_claims": [
            {"text": claim.text, "verdict": claim.verdict, "reason": claim.reason}
            for claim in result.verifier_claims
        ],
    }


def qa_result_from_dict(payload: dict[str, Any]) -> QAResult:
    # R3: legacy cache entries have no resolution_tier; they were all verified
    # safe_agri T3 answers (the only kind ever stored), so grounded_generation
    # is the factually correct default, not a guess.
    raw_tier = payload.get("resolution_tier", "grounded_generation")
    try:
        tier = ResolutionTier(raw_tier)
    except ValueError:
        tier = ResolutionTier.GROUNDED_GENERATION
    return QAResult(
        query=payload["query"],
        category=SafetyCategory(payload["category"]),
        answer=payload["answer"],
        confidence=VerificationConfidence(payload["confidence"]),
        model=payload.get("model") or "",
        error=payload.get("error"),
        matched_rules=tuple(payload.get("matched_rules") or ()),
        safety_reason=payload.get("safety_reason"),
        resolution_tier=tier,
        sources=tuple(
            RetrievedSource(
                id=source["id"],
                score=source["score"],
                title_en=source.get("title_en", ""),
                title_bn=source.get("title_bn", ""),
                content_en=source.get("content_en", ""),
                content_bn=source.get("content_bn", ""),
                source=source.get("source", ""),
                citation=source.get("citation", ""),
                metadata=source.get("metadata") or {},
            )
            for source in payload.get("sources") or ()
        ),
        trace=tuple(
            PipelineEvent(
                stage=PipelineStage(event["stage"]),
                status=StageStatus(event["status"]),
                detail=event.get("detail"),
                event_type=event.get("event_type", "stage"),
                text=event.get("text"),
            )
            for event in payload.get("trace") or ()
        ),
        verifier_flags=tuple(payload.get("verifier_flags") or ()),
        verifier_claims=tuple(
            VerifierClaim(text=claim["text"], verdict=claim["verdict"], reason=claim.get("reason", ""))
            for claim in payload.get("verifier_claims") or ()
        ),
    )


class DemoAnswerCache:
    """Thread-safe JSON-file cache: key -> serialized QAResult payload.

    Loaded once at construction (startup or prewarm script); writes are
    atomic (tmp file + replace) and best-effort — a persistence failure never
    breaks the pipeline, the in-memory copy still serves this process.
    """

    def __init__(self, path: Path, *, max_entries: int = 100) -> None:
        self.path = Path(path)
        self.max_entries = max_entries
        self._lock = threading.Lock()
        self._items: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                self._items = {k: v for k, v in data.items() if isinstance(v, dict)}
        except (OSError, json.JSONDecodeError):
            # A corrupt cache file degrades to an empty cache, never a crash.
            self._items = {}

    @staticmethod
    def normalize(query: str) -> str:
        """Key normalization: collapse whitespace and strip any trailing run
        of terminal punctuation / whitespace (e.g. "?", "!", "।", and mixes
        like "? ।") so equivalent phrasings share one cache key."""
        return re.sub(r"[।?!\s]+$", "", " ".join(query.split()))

    def key_for(
        self,
        query: str,
        crop: str | None = None,
        disease: str | None = None,
        model: str | None = None,
        corpus: str | None = None,
    ) -> str:
        # Crop/disease/model/corpus are part of the key so a stored answer is
        # never replayed into a different context, a different model's lane,
        # or a different retrieval-corpus generation (P0-7: bump CORPUS_VERSION
        # after rebuilding the index to invalidate stale demo replays).
        return (
            f"{crop or ''}|{disease or ''}|{model or ''}|{corpus or ''}|"
            f"{self.normalize(query)}"
        )

    def get(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            payload = self._items.get(key)
            return dict(payload) if payload is not None else None

    def put(self, key: str, payload: dict[str, Any]) -> None:
        with self._lock:
            self._items[key] = payload
            while len(self._items) > self.max_entries:
                self._items.pop(next(iter(self._items)))  # evict oldest (insertion order)
            self._save()

    def delete(self, key: str) -> None:
        """Remove one entry (used by the prewarm tool to purge stale
        pre-safety entries whose fresh classification is terminal)."""
        with self._lock:
            if key in self._items:
                del self._items[key]
                self._save()

    def _save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(self.path.suffix + ".tmp")
            tmp.write_text(json.dumps(self._items, ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(self.path)
        except OSError:
            pass  # best-effort persistence; never break the pipeline

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
