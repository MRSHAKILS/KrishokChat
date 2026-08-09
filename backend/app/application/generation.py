from __future__ import annotations

from collections.abc import AsyncIterator

from app.domain.contracts import GenerationResult, QueryContext, RetrievedSource
from app.ports.llm import LLMClient


REFERRAL = "দুঃখিত, এই প্রশ্নের নির্ভরযোগ্য উত্তর এখন দেওয়া সম্ভব নয়। স্থানীয় পরামর্শের জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"


class GroundedAnswerGenerator:
    def __init__(self, client: LLMClient) -> None:
        self.client = client

    @staticmethod
    def _prompt(query: str, context: QueryContext, sources: list[RetrievedSource]) -> str:
        source_blocks = []
        for source in sources[:5]:
            content = source.content_bn or source.content_en
            if source.metadata.get("treatment_summary_bn"):
                content += f"\nপ্রতিকার: {source.metadata['treatment_summary_bn']}"
            if source.metadata.get("prevention_bn"):
                content += f"\nপ্রতিরোধ: {source.metadata['prevention_bn']}"
            source_blocks.append(
                f"[{source.id}] {source.title_bn or source.title_en}\n{content[:1200]}"
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
        return f"""তুমি বাংলাদেশি কৃষকের জন্য একটি সংক্ষিপ্ত, সতর্ক কৃষি সহায়ক।
শুধু নিচের জ্ঞানভান্ডারের তথ্য ব্যবহার করে বাংলায় উত্তর দাও। কোনো উৎসে নেই এমন
রাসায়নিকের নাম, মাত্রা বা দাবি তৈরি করবে না। তথ্য অসম্পূর্ণ হলে স্পষ্টভাবে বলবে এবং
কৃষক কল সেন্টার ১৬১২৩ উল্লেখ করবে। উত্তরটি ৩-৬টি ছোট অনুচ্ছেদ বা বুলেটে দাও।
প্রাসঙ্গিক দাবির শেষে উৎসের আইডি [ID] লিখতে পারো; উৎসের বাইরে কিছু জানলে 'তথ্যটি
জ্ঞানভান্ডারে নেই' বলবে।

প্রাসঙ্গিক প্রসঙ্গ:
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
        prompt = self._prompt(query, context, sources)
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
        prompt = self._prompt(query, context, sources)
        try:
            async for chunk in self.client.stream(
                prompt, metadata={"source_ids": [source.id for source in sources]}
            ):
                yield chunk
        except Exception:
            # Do not turn a provider failure into apparently grounded referral text.
            # The pipeline catches this and returns a low-confidence result.
            raise
