from __future__ import annotations

from collections.abc import AsyncIterator

from app.domain.contracts import GenerationResult, QueryContext, RetrievedSource
from app.ports.llm import LLMClient


REFERRAL = "দুঃখিত, এই প্রশ্নের নির্ভরযোগ্য উত্তর এখন দেওয়া সম্ভব নয়। স্থানীয় পরামর্শের জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"


def format_progressive_guidance_text(guidance: dict) -> str:
    """Renders structured progressive guidance into clean, professional Bengali text."""
    title = guidance.get("title_bn", "পরামর্শ ও পরিচর্যা")
    checks = "\n".join(f"• {c}" for c in guidance.get("field_checks_bn", []))
    controls = "\n".join(f"• {c}" for c in guidance.get("cultural_controls_bn", []))
    safety = guidance.get("safety_boundary_bn", "")

    parts = [f"**{title}**\n"]
    if checks:
        parts.append(f"📋 **মাঠে পর্যবেক্ষণ করুন:**\n{checks}\n")
    if controls:
        parts.append(f"🌱 **পরিবেশবান্ধব ও সাধারণ পরিচর্যা:**\n{controls}\n")
    if safety:
        parts.append(f"⚠️ **সতর্কতা ও যোগাযোগ:**\n{safety}")

    return "\n".join(parts)


class GroundedAnswerGenerator:
    def __init__(
        self,
        client: LLMClient,
        *,
        max_sources: int = 5,
        max_source_chars: int = 1200,
    ) -> None:
        self.client = client
        # Prompt-size caps. The local CPU lane lowers these (fewer, shorter
        # sources) so prompt evaluation finishes inside its timeout budget.
        self.max_sources = max_sources
        self.max_source_chars = max_source_chars

    @staticmethod
    def _prompt(
        query: str,
        context: QueryContext,
        sources: list[RetrievedSource],
        max_sources: int,
        max_source_chars: int,
    ) -> str:
        source_blocks = []
        for source in sources[:max_sources]:
            content = source.content_bn or source.content_en
            if source.metadata.get("treatment_summary_bn"):
                content += f"\nপ্রতিকার: {source.metadata['treatment_summary_bn']}"
            if source.metadata.get("prevention_bn"):
                content += f"\nপ্রতিরোধ: {source.metadata['prevention_bn']}"
            source_blocks.append(
                f"[{source.id}] {source.title_bn or source.title_en}\n{content[:max_source_chars]}"
            )
        history = "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')[:500]}"
            for item in context.history[-6:]
        )
        metadata = []
        if context.crop:
            metadata.append(f"ফসল: {context.crop}")
        if context.disease:
            metadata.append(f"রোগ: {context.disease}")
        # P2: stage-aware line only appears when a signed-in farmer supplied a
        # profile. Absent → this block is empty and the prompt is byte-identical
        # to the pre-P2 pipeline (locked by a regression test).
        farmer_line = f"কৃষকের ফসল পর্যায়: {context.farmer_context}\n\n" if context.farmer_context else ""
        return f"""তুমি বাংলাদেশি কৃষকের জন্য একটি সংক্ষিপ্ত, সতর্ক কৃষি সহায়ক।
শুধু নিচের জ্ঞানভান্ডারের তথ্য ব্যবহার করে বাংলায় উত্তর দাও। কোনো উৎসে নেই এমন
রাসায়নিকের নাম, মাত্রা বা দাবি তৈরি করবে না। তথ্য অসম্পূর্ণ হলে স্পষ্টভাবে বলবে এবং
কৃষক কল সেন্টার ১৬১২৩ উল্লেখ করবে। উত্তরটি ৩-৬টি ছোট অনুচ্ছেদ বা বুলেটে দাও।
প্রাসঙ্গিক দাবির শেষে উৎসের আইডি [ID] লিখতে পারো; উৎসের বাইরে কিছু জানলে 'তথ্যটি
জ্ঞানভান্ডারে নেই' বলবে।

{farmer_line}প্রাসঙ্গিক প্রসঙ্গ:
{' '.join(metadata) or 'নেই'}

পূর্ববর্তী কথোপকথন:
{history or 'নেই'}

জ্ঞানভান্ডারের উৎস:
{chr(10).join(source_blocks)}

কৃষকের প্রশ্ন: {query}
উত্তর:
"""

    async def generate(self, query: str, context: QueryContext, sources: list[RetrievedSource]) -> GenerationResult:
        if not sources:
            return GenerationResult(answer=REFERRAL, model=self.client.name, mode="no_sources", error="No sources")
        prompt = self._prompt(query, context, sources, self.max_sources, self.max_source_chars)
        try:
            answer = await self.client.generate(prompt, metadata={"source_ids": [source.id for source in sources]})
            return GenerationResult(
                answer=answer,
                used_source_ids=tuple(source.id for source in sources),
                model=self.client.name,
                mode="grounded",
            )
        except Exception as exc:
            return GenerationResult(
                answer=REFERRAL,
                used_source_ids=(),
                model=self.client.name,
                mode="generation_error",
                error=str(exc),
            )

    async def generate_from_text(
        self,
        answer: str,
        sources: list[RetrievedSource],
        *,
        mode: str,
    ) -> GenerationResult:
        """Wrap already streamed text without issuing a hidden second LLM call."""
        if not answer.strip():
            return GenerationResult(
                answer=REFERRAL,
                model=self.client.name,
                mode="empty_stream",
                error="LLM stream returned no text",
            )
        return GenerationResult(
            answer=answer.strip(),
            used_source_ids=tuple(source.id for source in sources),
            model=self.client.name,
            mode=mode,
        )

    async def stream(self, query: str, context: QueryContext, sources: list[RetrievedSource]) -> AsyncIterator[str]:
        if not sources:
            yield REFERRAL
            return
        prompt = self._prompt(query, context, sources, self.max_sources, self.max_source_chars)
        try:
            async for chunk in self.client.stream(
                prompt, metadata={"source_ids": [source.id for source in sources]}
            ):
                yield chunk
        except Exception:
            # Do not turn a provider failure into apparently grounded referral text.
            # The pipeline catches this and returns a low-confidence result.
            raise
