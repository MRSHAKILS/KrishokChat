"""The single authoritative QA pipeline used by both HTTP endpoints."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import replace

from app.application.generation import GroundedAnswerGenerator, REFERRAL
from app.application.query_builder import build_retrieval_query
from app.application.rewrite import ConversationalQueryRewriter
from app.application.safety import SafetyClassifier
from app.application.telemetry import (
    STAGE_NAMES,
    capture_tokens,
    current_request_id,
    estimate_cost,
    serving_provider,
    stage_timer,
)
from app.core.config import settings
from app.domain.contracts import (
    PipelineEvent,
    QAResult,
    QueryContext,
    RetrievedSource,
    SafetyDecision,
    VerificationResult,
)
from app.domain.enums import PipelineStage, SafetyCategory, StageStatus, VerificationConfidence
from app.domain.safety_policy import canned_response
from app.infrastructure.cache.demo import DemoAnswerCache, qa_result_from_dict, qa_result_to_dict
from app.ports.audit import AuditSink
from app.ports.retriever import Retriever
from app.ports.session import SessionStore
from app.ports.verifier import Verifier


EventCallback = Callable[[PipelineEvent], Awaitable[None]]


class QAInput:
    def __init__(
        self,
        *,
        query: str,
        session_id: str | None = None,
        crop: str | None = None,
        disease: str | None = None,
        history: list[dict[str, str]] | None = None,
        seed_sources: list[RetrievedSource] | None = None,
        channel: str = "chat",
        model: str | None = None,
    ) -> None:
        self.query = query
        self.session_id = session_id
        self.crop = crop
        self.disease = disease
        self.history = history or []
        self.seed_sources = seed_sources or []
        self.channel = channel
        self.model = model


class QAPipeline:
    def __init__(
        self,
        *,
        safety: SafetyClassifier,
        retriever: Retriever,
        generator: GroundedAnswerGenerator,
        verifier: Verifier,
        audit: AuditSink,
        sessions: SessionStore,
        top_k: int = 5,
        generation_clients: dict[str, object] | None = None,
        generation_tuning: dict[str, dict[str, int]] | None = None,
        answer_cache: DemoAnswerCache | None = None,
        rewriter: ConversationalQueryRewriter | None = None,
        local_lane_models: frozenset[str] | None = None,
        local_lane_concurrency: int | None = None,
        corpus_version: str | None = None,
    ) -> None:
        self.safety = safety
        self.retriever = retriever
        self.generator = generator
        self.verifier = verifier
        self.audit = audit
        self.sessions = sessions
        self.top_k = top_k
        # Optional per-request model registry: {"krishokchat-4b": LLMClient}.
        # The default generator's client is used when no match is found.
        self.generation_clients = generation_clients or {}
        # Optional per-model prompt tuning (e.g. {"krishokchat-4b":
        # {"max_sources": 3, "max_source_chars": 800}}) applied when the
        # matching client is selected.
        self.generation_tuning = generation_tuning or {}
        # B1 demo answer cache (exact-replay of curated demo questions).
        # None = caching disabled entirely (default; tests construct the
        # pipeline without a cache and keep their exact behavior).
        self.answer_cache = answer_cache
        # A1 conversational query rewriting (follow-ups -> standalone
        # retrieval queries). None = raw query retrieval (default).
        self.rewriter = rewriter
        # P0-6: local-lane concurrency guard. Model names in
        # ``local_lane_models`` (the llama.cpp lane) are gated by a lazily
        # created asyncio.Semaphore sized by ``local_lane_concurrency``;
        # extra requests queue instead of overloading the inference process.
        # None concurrency (default) = guard entirely off, behavior unchanged.
        self.local_lane_models = local_lane_models or frozenset()
        self.local_lane_concurrency = local_lane_concurrency
        self._local_semaphore: asyncio.Semaphore | None = None
        self._local_semaphore_lock = threading.Lock()
        # P0-7: corpus-generation tag appended to demo-cache keys. None (old
        # pipelines/tests) keeps the exact previous key shape.
        self.corpus_version = corpus_version

    def _ensure_local_semaphore(self) -> asyncio.Semaphore:
        sem = self._local_semaphore
        if sem is None:
            with self._local_semaphore_lock:
                if self._local_semaphore is None:
                    self._local_semaphore = asyncio.Semaphore(self.local_lane_concurrency)
                sem = self._local_semaphore
        return sem

    @asynccontextmanager
    async def _local_lane_guard(self, model: str | None) -> AsyncIterator[None]:
        """No-op for non-local lanes; otherwise hold the lane semaphore for
        the whole generation stage (wait-queued, never 429)."""
        if self.local_lane_concurrency is None or model not in self.local_lane_models:
            yield
            return
        async with self._ensure_local_semaphore():
            yield

    def _generator_for(self, model: str | None) -> GroundedAnswerGenerator:
        if model and model in self.generation_clients:
            tuning = self.generation_tuning.get(model, {})
            return GroundedAnswerGenerator(self.generation_clients[model], **tuning)
        return self.generator

    async def run(self, request: QAInput, on_event: EventCallback | None = None) -> QAResult:
        trace: list[PipelineEvent] = []

        async def emit(stage: PipelineStage, status: StageStatus, detail: str | None = None) -> None:
            event = PipelineEvent(stage=stage, status=status, detail=detail)
            trace.append(event)
            if on_event:
                await on_event(event)

        history = request.history or (
            self.sessions.get(request.session_id) if request.session_id else []
        )
        context = QueryContext(
            crop=request.crop,
            disease=request.disease,
            history=tuple(history),
        )
        decision: SafetyDecision | None = None
        sources: list[RetrievedSource] = []
        retrieved: list[RetrievedSource] = []
        verifier_flags: tuple[str, ...] = ()
        result: QAResult | None = None
        cached_hit = False
        # T0-05: per-stage wall-clock latencies. Every stage name is present;
        # stages that did not run (terminal/exception paths, cache replays)
        # stay 0.0 — the trace's SKIP status explains them.
        timings: dict[str, float] = {name: 0.0 for name in STAGE_NAMES}
        # The lane object that actually served generation (the generator's
        # client for GroundedAnswerGenerator, else the generator itself).
        generation_lane: object | None = None
        # A1: the retrieval query (possibly rewritten); audited as-is so the
        # metrics panel and paper can see exactly what was searched.
        retrieval_query = request.query
        rewritten = False
        cache_key = (
            self.answer_cache.key_for(
                request.query,
                request.crop,
                request.disease,
                request.model,
                self.corpus_version,
            )
            if self.answer_cache is not None
            else None
        )

        def _cached_replay() -> tuple[QAResult, tuple[PipelineEvent, ...]] | None:
            """Replay a curated safe_agri demo-cache answer, or None on miss.

            Only safe_agri entries with no generation error replay; refusals
            are never stored, and a corrupt entry degrades to a miss.
            """
            if cache_key is None:
                return None
            payload = self.answer_cache.get(cache_key)
            if payload is None:
                return None
            try:
                cached_result = qa_result_from_dict(payload)
            except (KeyError, ValueError, TypeError):
                return None  # corrupt entry -> treat as miss
            if (
                cached_result.category is not SafetyCategory.SAFE_AGRI
                or cached_result.error is not None
            ):
                return None
            post_safety_trace = tuple(
                event
                for event in cached_result.trace
                if event.stage is not PipelineStage.SAFETY
            )
            return (
                replace(
                    cached_result,
                    query=request.query,
                    trace=tuple(trace) + post_safety_trace,
                ),
                post_safety_trace,
            )

        try:
            await emit(PipelineStage.SAFETY, StageStatus.START)
            with stage_timer("safety", timings):
                decision = await self.safety.classify(request.query, context)
                await emit(PipelineStage.SAFETY, StageStatus.COMPLETE, decision.category.value)

            if decision.terminal:
                if decision.classifier_outage:
                    # Classifier unreachable: replay the curated cache when the
                    # exact question was previously verified safe_agri, so the
                    # demo keeps working offline. Real terminal decisions
                    # (deterministic rules, LLM refusals) NEVER replay.
                    replay = _cached_replay()
                    if replay is not None:
                        cached_hit = True
                        result, post_safety_trace = replay
                        for event in post_safety_trace:
                            if on_event:
                                await on_event(event)
                        return result
                for stage in (PipelineStage.RETRIEVAL, PipelineStage.GENERATION, PipelineStage.VERIFIER):
                    await emit(stage, StageStatus.SKIP, "terminal safety decision")
                result = QAResult(
                    query=request.query,
                    category=decision.category,
                    answer=decision.response or canned_response(decision.category),
                    confidence=VerificationConfidence.BLOCKED,
                    trace=tuple(trace),
                    matched_rules=decision.matched_rules,
                    safety_reason=decision.reason or None,
                )
                return result

            # B1 exact replay is deliberately checked only AFTER the live
            # safety decision. A stored answer may never bypass a newer safety
            # rule, classifier update, or changed interpretation of the raw
            # query. Cache hits skip retrieval/generation/verification only.
            replay = _cached_replay()
            if replay is not None:
                cached_hit = True
                result, post_safety_trace = replay
                for event in post_safety_trace:
                    if on_event:
                        await on_event(event)
                return result

            await emit(PipelineStage.RETRIEVAL, StageStatus.START)
            with stage_timer("retrieval", timings):
                if self.rewriter is not None:
                    retrieval_query, rewritten = await self.rewriter.maybe_rewrite(
                        request.query, context.history
                    )
                retrieval_query = build_retrieval_query(retrieval_query, context, decision.category.value)
                retrieved = await asyncio.to_thread(self.retriever.retrieve, retrieval_query, top_k=self.top_k)
                seen_ids: set[str] = set()
                sources = []
                for source in [*request.seed_sources, *retrieved]:
                    if source.id not in seen_ids:
                        seen_ids.add(source.id)
                        sources.append(source)
                # P3: surface the dialect expansion in the agent trace (honest
                # evidence the mapping ran; nothing shown when no terms matched).
                detail = f"{len(sources)} sources"
                if rewritten:
                    detail += " · rewritten"
                expansion = getattr(self.retriever, "last_expansion", None)
                if expansion and expansion[2]:
                    detail += " · " + "; ".join(expansion[2][:3])
                await emit(PipelineStage.RETRIEVAL, StageStatus.COMPLETE, detail)

            await emit(PipelineStage.GENERATION, StageStatus.START)
            with stage_timer("generation", timings):
                # P0-6: local-lane gate around the generation stage (both the
                # streaming and non-streaming paths). Non-local lanes pass
                # through without touching the semaphore.
                async with self._local_lane_guard(request.model):
                    generator = self._generator_for(request.model)
                    generation_lane = getattr(generator, "client", None) or generator
                    if on_event and sources:
                        chunks: list[str] = []
                        async for chunk in generator.stream(request.query, context, sources):
                            chunks.append(chunk)
                            await on_event(
                                PipelineEvent(
                                    stage=PipelineStage.GENERATION,
                                    status=StageStatus.COMPLETE,
                                    event_type="token",
                                    text=chunk,
                                )
                            )
                        generated = await generator.generate_from_text(
                            "".join(chunks), sources, mode="grounded_stream"
                        )
                    else:
                        generated = await generator.generate(request.query, context, sources)
                await emit(PipelineStage.GENERATION, StageStatus.COMPLETE, generated.model)

            await emit(PipelineStage.VERIFIER, StageStatus.START)
            with stage_timer("verifier", timings):
                verification = self.verifier.verify(generated.answer, sources)
                verifier_flags = verification.flags
                # A generation failure must not be stamped verified: the answer is
                # referral text, not grounded content.
                if generated.error:
                    verification = VerificationResult(
                        confidence=VerificationConfidence.LOW_CONFIDENCE,
                        flags=verification.flags + (f"generation_error: {generated.error[:120]}",),
                        unverified_claims=verification.unverified_claims,
                    )
                    verifier_flags = verification.flags
                # P1 annotate-and-drop: unsupported dosage claims are removed from
                # the final answer (never hard-blocked); an emptied answer maps to
                # the referral text. The streamed preview may briefly show the raw
                # text, but the authoritative final event always carries the
                # sanitized answer.
                final_answer = generated.answer
                if verification.sanitized_answer is not None:
                    final_answer = verification.sanitized_answer or REFERRAL
                await emit(PipelineStage.VERIFIER, StageStatus.COMPLETE, verification.confidence.value)

            result = QAResult(
                query=request.query,
                category=decision.category,
                answer=final_answer,
                sources=tuple(sources),
                confidence=verification.confidence,
                trace=tuple(trace),
                verifier_flags=verification.flags,
                verifier_claims=verification.claims,
                model=generated.model,
                error=generated.error,
            )
            # B1: store verified safe answers for exact replay. Terminal
            # refusals are never cached (they must re-run safety every time),
            # and error results (generation/verification failures) are never
            # cached — only grounded, answerable content.
            if (
                cache_key is not None
                and result.category is SafetyCategory.SAFE_AGRI
                and result.error is None
            ):
                self.answer_cache.put(cache_key, qa_result_to_dict(result))
            return result
        except Exception as exc:
            # Keep the user-facing behavior controlled if an adapter unexpectedly fails.
            await emit(PipelineStage.VERIFIER, StageStatus.ERROR, str(exc)[:200])
            category = decision.category if decision else SafetyCategory.LOW_CONFIDENCE
            result = QAResult(
                query=request.query,
                category=category,
                answer=REFERRAL,
                sources=tuple(sources),
                confidence=VerificationConfidence.LOW_CONFIDENCE,
                trace=tuple(trace),
                verifier_flags=(str(exc),),
                error=str(exc),
            )
            return result
        finally:
            if result is not None:
                self._audit(
                    request,
                    result,
                    verifier_flags if not cached_hit else result.verifier_flags,
                    decision=decision,
                    retrieved=retrieved,
                    cached=cached_hit,
                    retrieval_query=retrieval_query,
                    rewritten=rewritten,
                    timings=timings,
                    generation_lane=generation_lane,
                )
                if request.session_id and result.category is SafetyCategory.SAFE_AGRI:
                    self.sessions.append(request.session_id, "user", request.query)
                    self.sessions.append(request.session_id, "assistant", result.answer)

    def _audit(
        self,
        request: QAInput,
        result: QAResult,
        verifier_flags: tuple[str, ...],
        decision: SafetyDecision | None = None,
        retrieved: list[RetrievedSource] | None = None,
        cached: bool = False,
        retrieval_query: str | None = None,
        rewritten: bool = False,
        timings: dict[str, float] | None = None,
        generation_lane: object | None = None,
    ) -> None:
        # P1 refusal counters (TRUST-SCORE style, honest subset):
        # - answered_without_sources: a safe-agri query that produced a real
        #   answer with zero retrieved passages = over-responsiveness signal.
        #   Today the generator refuses in this case (REFERRAL), so this flag
        #   guards regressions.
        answered_without_sources = bool(
            result.category is SafetyCategory.SAFE_AGRI
            and not result.sources
            and result.answer not in ("", REFERRAL)
        )
        # P2 per-step validity (dual-view): each stage's logged decision is the
        # exact evidence the UI stepper renders. Router = deterministic rule +
        # LLM confidence; retrieval = hit/miss + top-1 score from the actual
        # passages the retriever returned (seed sources excluded, they are
        # context, not hits); verifier = the pass verdict on the final answer.
        retrieved_sources = retrieved or []
        top1_score = None
        scores = [s.score for s in retrieved_sources if isinstance(getattr(s, "score", None), (int, float))]
        if scores:
            top1_score = round(max(scores), 4)
        # T0-05: token counts and provider are only recorded when the lane
        # exposes them (None otherwise); cost stays null until a real price
        # table exists (see telemetry.estimate_cost).
        tokens = capture_tokens(generation_lane) if generation_lane is not None else None
        provider = (
            serving_provider(generation_lane, settings.llm_provider)
            if generation_lane is not None
            else None
        )
        self.audit.record(
            {
                # v2 = per-step validity fields (router/retrieval/verifier).
                # Metrics aggregates only count v2 entries so legacy log rows
                # without these fields cannot distort the live panel.
                # cached=true = B1 exact replay; the metrics panel counts it
                # in totals but excludes it from per-stage aggregates (it is
                # not a new retrieval/verifier event).
                "pipeline_version": 2,
                "cached": cached,
                "query": request.query,
                "category": result.category.value,
                "action": "blocked-canned-response" if result.category is not SafetyCategory.SAFE_AGRI else "answered",
                "flagged": result.confidence is VerificationConfidence.FLAGGED_UNVERIFIED,
                "safety_confidence": round(decision.confidence, 4) if decision else None,
                "safety_reason": decision.reason[:300] if decision and decision.reason else None,
                "safety_matched_rules": list(decision.matched_rules) if decision else None,
                "retrieved_count": len(retrieved_sources),
                "retrieval_top1_score": top1_score,
                "retrieval_hit": len(retrieved_sources) > 0,
                "verifier_passed": (
                    None
                    if result.confidence is VerificationConfidence.BLOCKED
                    else result.confidence is VerificationConfidence.VERIFIED
                ),
                "verifier_flag": "; ".join(verifier_flags) or None,
                "verifier_checked": sum(1 for claim in result.verifier_claims if claim.verdict in ("grounded", "unsupported")),
                "verifier_grounded": sum(1 for claim in result.verifier_claims if claim.verdict == "grounded"),
                "verifier_unsupported": sum(1 for claim in result.verifier_claims if claim.verdict == "unsupported"),
                "verifier_claims": [
                    {"text": claim.text[:300], "verdict": claim.verdict, "reason": claim.reason[:200]}
                    for claim in result.verifier_claims
                ],
                "answered_without_sources": answered_without_sources,
                "model": result.model,
                "source_ids": [source.id for source in result.sources],
                "error": result.error,
                "channel": request.channel,
                "crop": request.crop,
                "disease": request.disease,
                "model_choice": request.model,
                "retrieval_query_used": retrieval_query or request.query,
                "retrieval_query_rewritten": rewritten,
                # T0-05 telemetry — all optional; pre-T0-05 records/consumers
                # tolerate absence. stage_timings_ms keys are exactly
                # safety/retrieval/generation/verifier; skipped stages are 0.0.
                "stage_timings_ms": timings if timings is not None else None,
                "tokens": tokens,
                "provider": provider,
                "cost_estimate": estimate_cost(tokens, provider),
                "request_id": current_request_id(),
            }
        )

    async def stream(self, request: QAInput) -> AsyncIterator[PipelineEvent | QAResult]:
        queue: asyncio.Queue[PipelineEvent | QAResult | None] = asyncio.Queue()

        async def publish(event: PipelineEvent) -> None:
            await queue.put(event)

        async def execute() -> None:
            result = await self.run(request, on_event=publish)
            await queue.put(result)
            await queue.put(None)

        task = asyncio.create_task(execute())
        try:
            while True:
                item = await queue.get()
                if item is None:
                    break
                yield item
        finally:
            if not task.done():
                task.cancel()
            else:
                await task
