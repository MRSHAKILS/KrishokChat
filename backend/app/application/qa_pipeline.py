"""The single authoritative QA pipeline used by both HTTP endpoints."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import replace

from app.application.chunk_fallback import ChunkFallbackResolver
from app.application.generation import GroundedAnswerGenerator, REFERRAL
from app.application.query_builder import build_retrieval_query
from app.application.rewrite import ConversationalQueryRewriter
from app.application.safety import SafetyClassifier
from app.application.structured_resolver import StructuredResolver
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
from app.domain.enums import PipelineStage, ResolutionTier, SafetyCategory, StageStatus, VerificationConfidence
from app.domain.resolution import tier_for
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
        farmer_context: str | None = None,
    ) -> None:
        self.query = query
        self.session_id = session_id
        self.crop = crop
        self.disease = disease
        self.history = history or []
        self.seed_sources = seed_sources or []
        self.channel = channel
        self.model = model
        # P2: optional stage-aware context (None on anonymous/DEMO requests).
        self.farmer_context = farmer_context


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
        # R4: optional T1/T2 resolver (None = off, T3 always, flag default).
        resolver: StructuredResolver | None = None,
        # R13: optional grounded chunk fallback (None = off). Only consulted on
        # the zero-node-source branch that today refuses (Amendment 03).
        chunk_fallback: ChunkFallbackResolver | None = None,
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
        # R4: T1/T2 structured resolver (None = off, default).
        self.resolver = resolver
        self.chunk_fallback = chunk_fallback
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
            farmer_context=request.farmer_context,
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
        # R3: LLM call counter for this request.  Count what actually ran:
        # +1 if the safety classifier reached its LLM branch (no matched_rules)
        # +1 if the query was rewritten (ConversationalQueryRewriter called LLM)
        # +1 when the generation stage executed.
        # A deterministic precheck refusal records 0; rewritten normal = 3.
        llm_calls: int = 0
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
                # R3: LLM was called if the classifier had no precheck match.
                if not decision.matched_rules:
                    llm_calls += 1
                result = QAResult(
                    query=request.query,
                    category=decision.category,
                    answer=decision.response or canned_response(decision.category),
                    confidence=VerificationConfidence.BLOCKED,
                    trace=tuple(trace),
                    matched_rules=decision.matched_rules,
                    safety_reason=decision.reason or None,
                    resolution_tier=tier_for(
                        category=decision.category,
                        matched_rules=decision.matched_rules,
                    ),
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

            # R4: T1/T2 structured resolver — runs only when
            # STRUCTURED_RESOLVER_ENABLED=true (resolver is not None).
            # Inserted after the cache-replay check, before retrieval.
            # On any miss, falls through to T3 with zero observable difference.
            if self.resolver is not None:
                resolved = self.resolver.resolve(
                    request.query,
                    stage=getattr(context, "stage", None),
                    crop_hint=request.crop,
                    problem_hint=request.disease,
                )
                if resolved is not None:
                    # Build the source from the fact row's provenance.
                    fact_source = RetrievedSource(
                        id=resolved.fact.source_node_id or f"{resolved.fact.crop}/{resolved.fact.problem}",
                        score=resolved.fact.confidence,
                        title_en=f"{resolved.fact.crop} {resolved.fact.problem}",
                        title_bn=f"{resolved.fact.crop_bn} {resolved.fact.problem_bn}",
                        content_en=resolved.answer,
                        content_bn=resolved.answer,
                        source=resolved.fact.source_doc or resolved.fact.citation,
                        citation=resolved.fact.citation,
                        metadata={"grounding": resolved.fact.grounding},
                    )
                    # Emit RETRIEVAL/GENERATION/VERIFIER as SKIP.
                    for stage in (PipelineStage.RETRIEVAL, PipelineStage.GENERATION, PipelineStage.VERIFIER):
                        await emit(stage, StageStatus.SKIP, "structured fact answer")
                    # R3: LLM was called if the safety classifier had no precheck match.
                    if not decision.matched_rules:
                        llm_calls += 1
                    result = QAResult(
                        query=request.query,
                        category=decision.category,
                        answer=resolved.answer,
                        sources=(fact_source,),
                        confidence=VerificationConfidence.VERIFIED,
                        trace=tuple(trace),
                        matched_rules=decision.matched_rules,
                        safety_reason=None,
                        resolution_tier=resolved.tier,
                    )
                    return result

            # Module 2: Cross-Modal Contradiction Intercept
            # If the user uploaded a photo of Crop A (request.crop / context.crop) but typed a question about Crop B:
            # (e.g. Image = Potato, Text = Begun / Brinjal), halt retrieval to prevent dangerous cross-crop pesticide recommendation!
            from app.domain.intent import _match_crop_alias, detect_cross_modal_conflict

            img_crop = request.crop or context.crop
            has_conflict, img_norm, query_norm, conflict_prompt = detect_cross_modal_conflict(
                img_crop, request.query
            )
            if has_conflict and conflict_prompt:
                for stage in (PipelineStage.RETRIEVAL, PipelineStage.GENERATION, PipelineStage.VERIFIER):
                    await emit(stage, StageStatus.SKIP, "cross-modal contradiction — clarification requested")
                if not decision.matched_rules:
                    llm_calls += 1
                result = QAResult(
                    query=request.query,
                    category=decision.category,
                    answer=conflict_prompt,
                    sources=(),
                    confidence=VerificationConfidence.VERIFIED,
                    trace=tuple(trace),
                    matched_rules=decision.matched_rules,
                    safety_reason="Cross-modal contradiction: image and text crop mismatch",
                    resolution_tier=ResolutionTier.INTERACTIVE_CLARIFICATION,
                )
                self._audit(
                    request,
                    result,
                    verifier_flags=(),
                    decision=decision,
                    retrieved=[],
                    cached=False,
                    retrieval_query=retrieval_query,
                    rewritten=False,
                    timings=timings,
                    generation_lane=None,
                    llm_calls=llm_calls,
                )
                if request.session_id:
                    self.sessions.append(request.session_id, "user", request.query)
                    self.sessions.append(request.session_id, "assistant", result.answer)
                return result

            # NLU Disambiguation & Clarification Intercept:
            # If the query is an ambiguous crop-specific problem/treatment inquiry with NO crop context,
            # do NOT retrieve blindly across unrelated crops. Intercept with a targeted clarification turn.
            has_crop = bool(
                request.crop
                or context.crop
                or (decision.intent and decision.intent.crop)
                or _match_crop_alias(request.query.lower())
                or request.seed_sources
            )
            if (
                decision.intent is not None
                and decision.intent.is_ambiguous
                and not has_crop
            ):
                clarification_text = (
                    decision.intent.clarification_question_bn
                    or "কোন ফসলে এই সমস্যা দেখা দিয়েছে বলবেন কি? (যেমন: আলু, ধান, বা টমেটো)"
                )
                for stage in (PipelineStage.RETRIEVAL, PipelineStage.GENERATION, PipelineStage.VERIFIER):
                    await emit(stage, StageStatus.SKIP, "missing crop slot — clarification requested")
                if not decision.matched_rules:
                    llm_calls += 1
                result = QAResult(
                    query=request.query,
                    category=decision.category,
                    answer=clarification_text,
                    sources=(),
                    confidence=VerificationConfidence.VERIFIED,
                    trace=tuple(trace),
                    matched_rules=decision.matched_rules,
                    safety_reason="Interactive disambiguation: crop slot missing",
                    resolution_tier=ResolutionTier.INTERACTIVE_CLARIFICATION,
                )
                self._audit(
                    request,
                    result,
                    verifier_flags=(),
                    decision=decision,
                    retrieved=[],
                    cached=False,
                    retrieval_query=retrieval_query,
                    rewritten=False,
                    timings=timings,
                    generation_lane=None,
                    llm_calls=llm_calls,
                )
                if request.session_id:
                    self.sessions.append(request.session_id, "user", request.query)
                    self.sessions.append(request.session_id, "assistant", result.answer)
                return result

            await emit(PipelineStage.RETRIEVAL, StageStatus.START)
            with stage_timer("retrieval", timings):
                if self.rewriter is not None:
                    retrieval_query, rewritten = await self.rewriter.maybe_rewrite(
                        request.query, context.history
                    )
                    if rewritten:
                        llm_calls += 1  # R3: rewriter consumed one LLM call
                retrieval_query = build_retrieval_query(retrieval_query, context, decision.category.value)
                retrieved = await asyncio.to_thread(self.retriever.retrieve, retrieval_query, top_k=self.top_k)
                seen_ids: set[str] = set()
                sources = []
                for source in [*request.seed_sources, *retrieved]:
                    if source.id not in seen_ids:
                        seen_ids.add(source.id)
                        sources.append(source)
                # R13: grounded chunk fallback — nodes first, always. This runs
                # ONLY when node retrieval produced zero sources, i.e. the branch
                # that today returns REFERRAL ("no_sources"). Chunk sections
                # become ordinary evidence for the same generation + verifier
                # path; if retrieval and fallback both come up empty, behavior
                # is byte-identical to today.
                if not sources and self.chunk_fallback is not None:
                    chunk_sources = await asyncio.to_thread(
                        self.chunk_fallback.retrieve, retrieval_query
                    )
                    if chunk_sources:
                        sources = chunk_sources
                        retrieved = chunk_sources
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

            # R3: LLM was called if the safety classifier had no precheck match.
            if not decision.matched_rules:
                llm_calls += 1  # safety LLM branch
            llm_calls += 1  # generation stage
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
                resolution_tier=tier_for(
                    category=decision.category,
                    matched_rules=decision.matched_rules,
                    generated=True,
                ),
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
                resolution_tier=tier_for(
                    category=category,
                    matched_rules=decision.matched_rules if decision else (),
                    generated=False,
                ),
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
                    llm_calls=llm_calls,
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
        llm_calls: int = 0,
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
        # T1-04: write-time PII redaction for stored audit query text.
        # The user-visible answer and retrieval response are untouched — only
        # the persisted audit record is scrubbed, and only when the switch is
        # on (default off, 0 = keep verbatim). Best-effort regex.
        query_for_audit = request.query
        retrieval_for_audit = retrieval_query or request.query
        if getattr(settings, "pii_redaction_enabled", False):
            try:
                from app.core.redaction import redact_pii

                query_for_audit = redact_pii(request.query)
                retrieval_for_audit = redact_pii(retrieval_query or request.query)
            except Exception:
                query_for_audit = request.query
                retrieval_for_audit = retrieval_query or request.query
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
                "query": query_for_audit,
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
                "retrieval_query_used": retrieval_for_audit,
                "retrieval_query_rewritten": rewritten,
                # T0-05 telemetry — all optional; pre-T0-05 records/consumers
                # tolerate absence. stage_timings_ms keys are exactly
                # safety/retrieval/generation/verifier; skipped stages are 0.0.
                "stage_timings_ms": timings if timings is not None else None,
                "tokens": tokens,
                "provider": provider,
                "cost_estimate": estimate_cost(tokens, provider, model=result.model or request.model),
                "request_id": current_request_id(),
                # R3: resolution tier + LLM call count — the two keys that
                # power R7's tier-mix / zero-LLM-rate experiment.
                "resolution_tier": result.resolution_tier.value,
                "llm_calls": llm_calls,
                # R5: advisory routing hint (kind only; slot fields not audited
                # to avoid PII if upazila/crop come from the query text).
                "intent_kind": decision.intent.kind if decision and decision.intent else None,
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
