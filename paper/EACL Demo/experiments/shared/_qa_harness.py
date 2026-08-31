"""Shared offline harness for E01/E04/E06/E08 — real QAPipeline, no live LLM, no network.

Builds a real QAPipeline (BM25Retriever + deterministic precheck safety + HardenedDosageVerifier)
with a deterministic stub LLM, so every number is measured via stage_timer and recorded in the
audit sink. Dense retrieval needs OPENROUTER_API_KEY; offline runs are BM25-only and self-label.

The harness is deliberately isolated from the vision harness (_vision_common) to keep paper-track
code from polluting the frontend bundle scan.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
BACKEND = REPO_ROOT / "backend"
EVAL_BENCHMARK = BACKEND / "ml_assets" / "rag_index" / "eval" / "farmer_benchmark_1000.jsonl"
BM25_INDEX = BACKEND / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl"
BM25_CORPUS = BACKEND / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
# Fallback corpus per test_smoke_qa_pipeline.py
ALT_CORPUS = BACKEND / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"

# Ensure backend/app is importable
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def git_head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e:
        return f"unavailable:{e}"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def provenance(script: Path, inputs: dict[str, Path] | None = None) -> dict[str, Any]:
    import sys as _sys
    versions = {"python": _sys.version.split()[0]}
    for mod in ("torch", "ultralytics", "onnx", "onnxruntime", "fastapi"):
        try:
            m = __import__(mod)
            versions[mod] = getattr(m, "__version__", "unknown")
        except ImportError:
            versions[mod] = "not installed"
    payload: dict[str, Any] = {
        "script": str(script.resolve().relative_to(REPO_ROOT)).replace("\\", "/"),
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_head": git_head(),
        "python": versions["python"],
        "versions": versions,
        "machine": {"platform": platform.platform(), "processor": platform.processor(), "cpu_count": os.cpu_count()},
    }
    if inputs:
        payload["input_sha256"] = {k: (sha256_of(v) if v.exists() else "missing") for k, v in sorted(inputs.items())}
    return payload


def percentiles(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"n": 0, "mean": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
    s = sorted(values)
    def pct(p: float) -> float:
        k = (len(s) - 1) * p / 100
        f = int(k)
        c = min(f + 1, len(s) - 1)
        if f == c:
            return float(s[f])
        d = k - f
        return float(s[f] * (1 - d) + s[c] * d)
    return {"n": len(s), "mean": round(sum(s) / len(s), 3), "p50": round(pct(50), 3), "p95": round(pct(95), 3), "p99": round(pct(99), 3), "min": round(s[0], 3), "max": round(s[-1], 3)}


class InMemoryAudit:
    """AuditSink that captures records in memory for per-query stage_timings extraction."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def record(self, entry: dict[str, Any]) -> None:  # type: ignore[no-untyped-def]
        self.records.append(entry)


def _deterministic_sample(items: list[dict[str, Any]], n: int, seed: int) -> list[dict[str, Any]]:
    rnd = random.Random(seed)
    if n >= len(items):
        return items
    return rnd.sample(items, n)


def load_farmer_benchmark(n: int = 400, seed: int = 42) -> list[dict[str, Any]]:
    """Load and sample farmer_benchmark_1000.jsonl. Returns list of {question, row_id, source}."""
    if not EVAL_BENCHMARK.exists():
        raise SystemExit(f"missing benchmark: {EVAL_BENCHMARK}")
    rows: list[dict[str, Any]] = []
    with EVAL_BENCHMARK.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            # question is top-level or in messages[0]
            q = obj.get("question")
            if not q and "messages" in obj:
                try:
                    q = obj["messages"][0]["content"]
                except Exception:
                    q = None
            if not q:
                continue
            rows.append({"question": q, "row_id": obj.get("row_id", ""), "metadata": obj.get("metadata", {}), "raw": obj})
    sampled = _deterministic_sample(rows, n, seed)
    return sampled


# Stub LLM — offline, deterministic, grounded when sources present
class StubLLM:
    name = "eacl-offline-stub"

    async def generate(self, query: str, context, sources: list[Any]) -> Any:  # type: ignore[no-untyped-def]
        from app.application.generation import REFERRAL, GenerationResult

        if not sources:
            return GenerationResult(answer=REFERRAL, model=self.name, mode="no_sources", error="No sources")
        # Minimal grounded answer referencing first source — enough for verifier to pass as grounded
        txt = f"উত্তরটি উৎস {sources[0].id} অনুযায়ী প্রণীত।"
        return GenerationResult(answer=txt, used_source_ids=tuple(s.id for s in sources), model=self.name, mode="grounded")

    async def stream(self, query: str, context, sources: list[Any]):  # type: ignore[no-untyped-def]
        from app.application.generation import REFERRAL

        if not sources:
            yield REFERRAL
        else:
            yield f"উত্তরটি উৎস {sources[0].id} অনুযায়ী প্রণীত।"

    async def generate_from_text(self, answer: str, sources: list[Any], *, mode: str) -> Any:  # type: ignore[no-untyped-def]
        from app.application.generation import REFERRAL, GenerationResult

        return GenerationResult(answer=answer.strip() or REFERRAL, used_source_ids=tuple(s.id for s in sources), model=self.name, mode=mode)


class DeterministicSafety:
    """Real precheck rules + safe_agri stub (no LLM call). Keeps offline runs honest."""

    async def classify(self, query: str, context) -> Any:  # type: ignore[no-untyped-def]
        from app.domain.contracts import SafetyDecision
        from app.domain.enums import SafetyCategory
        from app.domain.safety_policy import precheck

        m = precheck(query)
        if m:
            cat, rules = m
            return SafetyDecision(category=cat, confidence=1.0, reason="Deterministic safety rule matched", matched_rules=rules, requires_escalation=cat is SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL, response=None, intent=None)
        from app.domain.intent import keyword_intent
        intent = keyword_intent(query)
        return SafetyDecision(category=SafetyCategory.SAFE_AGRI, confidence=1.0, reason="no deterministic rule matched", matched_rules=(), requires_escalation=False, response=None, intent=intent)


def build_offline_pipeline(audit: InMemoryAudit | None = None, top_k: int = 5):  # type: ignore[no-untyped-def]
    """Build a real QAPipeline with BM25-only retriever, deterministic safety, stub LLM."""
    from app.application.qa_pipeline import QAPipeline
    from app.application.verifier import HardenedDosageVerifier
    from app.infrastructure.retrieval.bm25 import BM25Retriever
    from app.infrastructure.sessions.memory import InMemorySessionStore

    audit = audit or InMemoryAudit()
    index = BM25_INDEX if BM25_INDEX.exists() else None
    corpus = BM25_CORPUS if BM25_CORPUS.exists() else (ALT_CORPUS if ALT_CORPUS.exists() else None)
    if index is None or corpus is None:
        raise SystemExit(f"missing BM25 index/corpus: {index} / {corpus}")
    retriever = BM25Retriever(index_path=index, corpus_path=corpus)
    return QAPipeline(
        safety=DeterministicSafety(),
        retriever=retriever,
        generator=StubLLM(),
        verifier=HardenedDosageVerifier(),
        audit=audit,  # type: ignore[arg-type]
        sessions=InMemorySessionStore(max_turns=10, ttl_seconds=1800),
        top_k=top_k,
    ), audit, index, corpus  # type: ignore[return-value]
