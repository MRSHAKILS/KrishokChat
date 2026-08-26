"""R13 — Tests for the grounded chunk fallback (Amendment 03).

Invariants checked:
  1. Chunker: every chunk is an exact substring of its source file
     (char offsets + sha256), size bounds respected, headings resolved.
  2. Node→MD map: institution must match; precision-first threshold.
  3. Resolver: mini index retrieval returns provenance-carrying sources;
     tampered/rotated corpus disables the fallback (fail-closed), never crashes.
  4. Pipeline integration:
     - Node-first: chunk fallback is NEVER consulted when node sources exist.
     - Flag off (chunk_fallback=None): zero-source behavior byte-identical
       (REFERRAL, mode "no_sources").
     - Flag on + hit: chunk sections flow through the normal generation +
       verifier path as evidence (tier T3), sources carry chunk provenance.
     - Flag on + no chunk hit: still REFERRAL (terminal refusal unchanged).
"""
from __future__ import annotations

import importlib.util
import json
import sys
import threading
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.chunk_fallback import ChunkFallbackResolver
from app.application.qa_pipeline import QAInput, QAPipeline
from app.domain.contracts import (
    GenerationResult,
    RetrievedSource,
    SafetyDecision,
    VerificationResult,
)
from app.domain.enums import ResolutionTier, SafetyCategory, VerificationConfidence
from app.ports.verifier import Verifier

TOOLS_RAG = Path(__file__).resolve().parents[2] / "tools" / "rag" / "15_build_chunk_index.py"


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_chunk_index_test", TOOLS_RAG)
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_chunk_index_test"] = module
    spec.loader.exec_module(module)
    return module


BLIGHT_MD = """# Potato Late Blight Control

দেরিতে ধান কাটা হলে অথবা জমি ভেজা থাকলে আলুর নাবি ধ্বসা রোগ দেখা দেয়।
রোগ দেখা দিলে ম্যানকোজেব গ্রুপের ছত্রানাশক ২ গ্রাম প্রতি লিটার হারে মিশিয়ে স্প্রে করতে হবে।
৭ দিন পরপর স্প্রে পুনরাবৃত্তি করা যেতে পারে এবং ফসল তোলার ৭ দিন আগে স্প্রে বন্ধ রাখতে হবে।

জমিতে পানি নিষ্কাশনের ব্যবস্থা রাখতে হবে এবং আক্রান্ত গাছ তুলে ফেলতে হবে।
সুষম সার ব্যবহার করে গাছের রোগ প্রতিরোধ ক্ষমতা বাড়ানো যায়।
"""

SOIL_MD = """# Soil pH Management Guide

মাটির অম্লতা পরীক্ষা করে চুনের পরিমাণ নির্ধারণ করতে হবে।
জমির পিএইচ ৬ এর নিচে হলে প্রতি হেক্টরে ডলোমাইট চুন প্রয়োগ করা যুক্তিসঙ্গত।
মাটি পরীক্ষার নমুনা তোলার সময় জমির বিভিন্ন স্থান থেকে মাটি সংগ্রহ করে মিশিয়ে নিতে হবে।
চুন প্রয়োগের দুই সপ্তাহ পর সার প্রয়োগ করা উত্তম ফল দেয়।
"""

RICE_MD = """# Rice Blast Disease Advisory

ধানের ব্লাস্ট রোগ পাতায় বাদামি দাগ তৈরি করে এবং ফলন মারাত্মকভাবে কমিয়ে দিতে পারে।
আক্রান্ত জমিতে পটাশ সারের ব্যবহার নিশ্চিত করতে হবে এবং জমিতে পানির স্তর ঠিক রাখতে হবে।
প্রয়োজনে ট্রাইসাইক্লাজোল গ্রুপের ছত্রানাশক স্প্রে করা যেতে পারে।
রোগ প্রতিরোধে প্রতিরোধী জাত নির্বাচন করা সবচেয়ে ভালো পদ্ধতি।
"""


def _make_corpus(root: Path) -> Path:
    src = root / "source_md"
    (src / "DAE" / "pest_guide" / "sections").mkdir(parents=True)
    (src / "BARC" / "soil_guide" / "sections").mkdir(parents=True)
    (src / "BRRI_IRRI" / "rice_guide" / "sections").mkdir(parents=True)
    (src / "DAE" / "pest_guide" / "sections" / "001_potato_late_blight_control.md").write_text(
        BLIGHT_MD, encoding="utf-8"
    )
    (src / "BARC" / "soil_guide" / "sections" / "002_soil_ph_management.md").write_text(
        SOIL_MD, encoding="utf-8"
    )
    (src / "BRRI_IRRI" / "rice_guide" / "sections" / "003_rice_blast_advisory.md").write_text(
        RICE_MD, encoding="utf-8"
    )
    return src


MINI_NODES = [
    {
        "node_id": "DAE_PEST_001",
        "title_en": "Potato Late Blight Control",
        "section_title": "Potato Late Blight Control",
        "citation": "DAE. Potato Late Blight Control. Pest Guide. pp. 1-1.",
    },
    {
        "node_id": "BARC_SOIL_001",
        "title_en": "Soil pH Management Guide",
        "section_title": "Soil pH Management",
        "citation": "BARC. Soil pH Management Guide. pp. 2-2.",
    },
]


@pytest.fixture()
def built(tmp_path: Path):
    """Build a complete mini chunk index with the REAL builder logic."""
    builder = _load_builder()
    src = _make_corpus(tmp_path)
    nodes_path = tmp_path / "knowledge_nodes.json"
    nodes_path.write_text(json.dumps(MINI_NODES), encoding="utf-8")
    builder.SOURCE_MD = src
    builder.NODES_PATH = nodes_path
    builder.OUT_INDEX = tmp_path / "indexes"
    builder.OUT_PROV = tmp_path / "provenance"
    assert builder.main() == 0
    return builder, src, tmp_path / "indexes", tmp_path / "provenance"


# ---------------------------------------------------------------------------
# Chunker unit tests
# ---------------------------------------------------------------------------


class TestChunker:
    def test_chunks_are_exact_substrings(self, tmp_path: Path) -> None:
        builder = _load_builder()
        text = ("# Heading\n\n" + "অ্যামিনো অ্যাসিড সমৃদ্ধ জৈব সার। " * 60 + "\n\n" + "second paragraph here. " * 80)
        chunks = builder.chunk_text(text, "Fallback Title")
        assert chunks
        for ch in chunks:
            seg = text[ch["char_start"]:ch["char_end"]]
            assert ch["n_words"] == len(seg.split())
            import hashlib

            assert hashlib.sha256(seg.encode("utf-8")).hexdigest() == ch["sha256"]

    def test_size_bounds(self) -> None:
        builder = _load_builder()
        text = "\n\n".join(f"paragraph number {i} with some words about crops and soil fertility." for i in range(200))
        chunks = builder.chunk_text(text, "Doc")
        assert chunks
        for ch in chunks:
            assert ch["char_end"] - ch["char_start"] <= 2 * builder.MAX_CHARS
            assert ch["n_words"] >= builder.MIN_WORDS or len(chunks) == 1

    def test_oversize_paragraph_hard_split(self) -> None:
        builder = _load_builder()
        text = "word " * 5000  # single giant paragraph, no breaks
        chunks = builder.chunk_text(text, "Doc")
        assert len(chunks) >= 2
        joined = [text[ch["char_start"]:ch["char_end"]] for ch in chunks]
        for seg in joined:
            assert len(seg) <= 2 * builder.MAX_CHARS
            assert seg in text

    def test_tiny_file_drops_all(self) -> None:
        builder = _load_builder()
        assert builder.chunk_text("# T\n\nshort.", "T") == []


# ---------------------------------------------------------------------------
# Build + map
# ---------------------------------------------------------------------------


class TestBuildAndMap:
    def test_build_outputs_exist_and_consistent(self, built) -> None:
        builder, src, index_dir, prov_dir = built
        corpus = [json.loads(l) for l in (index_dir / "chunks_corpus.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        assert (index_dir / "chunks_bm25.pkl").exists()
        assert (index_dir / "chunks_sha256.txt").exists()
        assert len(corpus) >= 1
        assert all("covered_by_node" in rec for rec in corpus)

    def test_node_map_matches_by_institution(self, built) -> None:
        builder, src, index_dir, prov_dir = built
        node_map = json.loads((prov_dir / "node_to_md_map.json").read_text(encoding="utf-8"))
        md_paths = node_map["md_paths"]
        assert "DAE/pest_guide/sections/001_potato_late_blight_control.md" in md_paths
        assert "DAE_PEST_001" in md_paths["DAE/pest_guide/sections/001_potato_late_blight_control.md"]

    def test_covered_by_node_stamped_on_chunks(self, built) -> None:
        builder, src, index_dir, prov_dir = built
        corpus = [json.loads(l) for l in (index_dir / "chunks_corpus.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        dae = [rec for rec in corpus if rec["institution"] == "DAE"]
        assert dae and all("DAE_PEST_001" in rec["covered_by_node"] for rec in dae)


# ---------------------------------------------------------------------------
# Resolver unit tests
# ---------------------------------------------------------------------------


class TestResolver:
    def test_retrieve_returns_grounded_sources(self, built) -> None:
        _builder, src, index_dir, _prov = built
        resolver = ChunkFallbackResolver(index_dir=index_dir, source_dir=src)
        assert resolver.available
        results = resolver.retrieve("আলুর নাবি ধ্বসা ম্যানকোজেব স্প্রে")
        assert results
        top = results[0]
        assert top.metadata["evidence_kind"] == "chunk_fallback"
        assert top.metadata["institution"] == "DAE"
        assert "ম্যানকোজেব" in top.content_bn
        assert top.id  # chunk_id present

    def test_irrelevant_query_no_results(self, built) -> None:
        _builder, src, index_dir, _prov = built
        resolver = ChunkFallbackResolver(index_dir=index_dir, source_dir=src)
        assert resolver.retrieve("qqq zzz unrelated tokens") == []

    def test_tampered_source_disables_fallback(self, built) -> None:
        _builder, src, index_dir, _prov = built
        resolver = ChunkFallbackResolver(index_dir=index_dir, source_dir=src)
        assert resolver.retrieve("আলুর নাবি ধ্বসা ম্যানকোজেব স্প্রে")
        # Rotate the corpus: edit text INSIDE a chunked span (same length, so
        # only the sha256 pin can catch it), then a fresh resolver must fail
        # closed (no evidence, no crash).
        target = next(src.rglob("*.md"))
        text = target.read_text(encoding="utf-8")
        target.write_text(text.replace("ম্যানকোজেব", "ট্যাম্পারড", 1), encoding="utf-8")
        fresh = ChunkFallbackResolver(index_dir=index_dir, source_dir=src)
        assert fresh.retrieve("আলুর নাবি ধ্বসা ম্যানকোজেব স্প্রে") == []

    def test_missing_index_unavailable(self, tmp_path: Path) -> None:
        resolver = ChunkFallbackResolver(index_dir=tmp_path, source_dir=tmp_path)
        assert not resolver.available
        assert resolver.retrieve("anything") == []

    def test_threaded_retrieve_is_stable(self, built) -> None:
        _builder, src, index_dir, _prov = built
        resolver = ChunkFallbackResolver(index_dir=index_dir, source_dir=src)
        outcomes: list[list[RetrievedSource]] = []

        def run() -> None:
            outcomes.append(resolver.retrieve("আলুর নাবি ধ্বসা ম্যানকোজেব স্প্রে"))

        threads = [threading.Thread(target=run) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert all(len(o) == len(outcomes[0]) for o in outcomes)


# ---------------------------------------------------------------------------
# Pipeline integration tests
# ---------------------------------------------------------------------------


def _setup_mock_pipeline(
    *,
    chunk_fallback: object | None = None,
    node_sources: list[RetrievedSource] | None = None,
    tmp_path: Path,
):
    fake_safety_decision = SafetyDecision(
        category=SafetyCategory.SAFE_AGRI,
        confidence=0.99,
        reason="safe",
        matched_rules=(),
    )
    fake_safety = AsyncMock()
    fake_safety.classify = AsyncMock(return_value=fake_safety_decision)

    fake_retriever = MagicMock()
    fake_retriever.retrieve = MagicMock(return_value=node_sources if node_sources is not None else [])
    fake_retriever.last_expansion = None

    fake_generator = MagicMock()
    fake_generator.client = None

    async def _generate(query, context, sources):
        if not sources:
            return GenerationResult(answer=REFERRAL_ANSWER, model="stub", mode="no_sources", error="No sources")
        return GenerationResult(
            answer="উত্তর: " + " ".join(s.content_bn[:60] for s in sources[:1]),
            used_source_ids=tuple(s.id for s in sources),
            model="stub",
            mode="grounded",
        )

    fake_generator.generate = AsyncMock(side_effect=_generate)

    fake_verifier = MagicMock(spec=Verifier)
    fake_verifier.verify = MagicMock(
        return_value=VerificationResult(confidence=VerificationConfidence.VERIFIED)
    )

    fake_audit = MagicMock()
    fake_audit.record = MagicMock()
    fake_audit.path = tmp_path / "audit.jsonl"

    fake_sessions = MagicMock()
    fake_sessions.get = MagicMock(return_value=[])
    fake_sessions.append = MagicMock()

    pipeline = QAPipeline(
        safety=fake_safety,
        retriever=fake_retriever,
        generator=fake_generator,
        verifier=fake_verifier,
        audit=fake_audit,
        sessions=fake_sessions,
        chunk_fallback=chunk_fallback,
    )
    return pipeline, fake_generator, fake_retriever


REFERRAL_ANSWER = "দুঃখিত, এই প্রশ্নের নির্ভরযোগ্য উত্তর এখন দেওয়া সম্ভব নয়।"


class _ExplodingFallback:
    """Node-first proof: any call is a violation."""

    def retrieve(self, query: str):  # pragma: no cover - fails the test if called
        raise AssertionError("chunk fallback must never run when node sources exist")


class _StaticFallback:
    def __init__(self, sources: list[RetrievedSource]) -> None:
        self.sources = sources
        self.calls: list[str] = []

    def retrieve(self, query: str) -> list[RetrievedSource]:
        self.calls.append(query)
        return self.sources


def _chunk_source() -> RetrievedSource:
    return RetrievedSource(
        id="chunk_abc",
        score=3.2,
        title_en="Potato Late Blight Control",
        content_bn="ম্যানকোজেব ২ গ্রাম/লিটার স্প্রে করুন।",
        citation="DAE. Potato Late Blight Control",
        metadata={"evidence_kind": "chunk_fallback", "institution": "DAE", "md_path": "DAE/x.md"},
    )


@pytest.mark.asyncio
async def test_pipeline_node_first_never_calls_fallback(tmp_path: Path) -> None:
    node_source = RetrievedSource(id="N1", score=1.0, content_bn="node content", citation="DAE")
    pipeline, _gen, _ret = _setup_mock_pipeline(
        chunk_fallback=_ExplodingFallback(), node_sources=[node_source], tmp_path=tmp_path
    )
    result = await pipeline.run(QAInput(query="আলুর নাবি ধ্বসা রোগের প্রতিকার কী?"))
    assert result.sources and result.sources[0].id == "N1"
    assert result.resolution_tier is ResolutionTier.GROUNDED_GENERATION


@pytest.mark.asyncio
async def test_pipeline_flag_off_zero_sources_refuses(tmp_path: Path) -> None:
    pipeline, generator, _ret = _setup_mock_pipeline(chunk_fallback=None, tmp_path=tmp_path)
    result = await pipeline.run(QAInput(query="একদম অজানা প্রশ্ন"))
    assert result.answer == REFERRAL_ANSWER
    assert result.error == "No sources"
    # generator saw zero sources
    assert generator.generate.call_args.args[2] == []


@pytest.mark.asyncio
async def test_pipeline_fallback_hit_flows_through_generation(tmp_path: Path) -> None:
    fallback = _StaticFallback([_chunk_source()])
    pipeline, generator, _ret = _setup_mock_pipeline(chunk_fallback=fallback, tmp_path=tmp_path)
    result = await pipeline.run(QAInput(query="একদম অজানা প্রশ্ন"))
    assert fallback.calls  # consulted exactly on the zero-source branch
    sources_passed = generator.generate.call_args.args[2]
    assert len(sources_passed) == 1
    assert sources_passed[0].metadata["evidence_kind"] == "chunk_fallback"
    assert result.sources[0].metadata["institution"] == "DAE"
    assert result.resolution_tier is ResolutionTier.GROUNDED_GENERATION
    assert result.error is None


@pytest.mark.asyncio
async def test_pipeline_fallback_miss_still_refuses(tmp_path: Path) -> None:
    fallback = _StaticFallback([])
    pipeline, generator, _ret = _setup_mock_pipeline(chunk_fallback=fallback, tmp_path=tmp_path)
    result = await pipeline.run(QAInput(query="একদম অজানা প্রশ্ন"))
    assert fallback.calls
    assert result.answer == REFERRAL_ANSWER
    assert result.error == "No sources"


@pytest.mark.asyncio
async def test_pipeline_seed_sources_prevent_fallback(tmp_path: Path) -> None:
    """Seed sources (e.g. vision-detected context) count as sources: fallback stays off."""
    fallback = _ExplodingFallback()
    pipeline, _gen, _ret = _setup_mock_pipeline(chunk_fallback=fallback, tmp_path=tmp_path)
    result = await pipeline.run(
        QAInput(query="আলুর রোগ?", seed_sources=[RetrievedSource(id="S1", score=1.0, content_bn="seed")])
    )
    assert result.sources and result.sources[0].id == "S1"
