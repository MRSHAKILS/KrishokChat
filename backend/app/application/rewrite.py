"""A1: conversational query rewriting — follow-ups become standalone queries.

Why it exists: retrieval (BM25 + dense + RRF) runs on the raw user query and
never sees conversation history, so a follow-up like "তাহলে কী করব?" retrieves
garbage even though the generation step has the full context. Rewrite-then-
retrieve is the established fix (CORAL, NAACL 2025 findings; ConvSearch-R1,
EMNLP 2025; SELF-multi-RAG) — rewrite the follow-up into a self-contained
retrieval query using the recent history, then retrieve.

Cost discipline (budget-free lane): the LLM rewrite fires ONLY when the query
carries a follow-up marker AND history exists. Single-turn questions (the
cached demo lane included) never trigger a rewrite call. Safety classification
is untouched — the classifier still sees the raw query; only the retrieval
query is rewritten. Any rewrite failure falls back to the raw query
(fail-open for retrieval, never for safety).
"""

from __future__ import annotations

from collections.abc import Sequence

from app.ports.llm import LLMClient

# Follow-up deixis markers: their presence (with history) suggests the query
# depends on the prior conversation and benefits from a standalone rewrite.
DEFAULT_MARKERS: tuple[str, ...] = (
    "তাহলে", "তবে", "এটা", "এগুলো", "এদের", "সেগুলো", "সেটা", "ওটা", "ওগুলো",
    "আর", "এখন", "বলো", "বলুন", "কী করব", "কী করি", "কী দেব", "কত দেব",
    "কতটা", "কতটুকু", "কেমন করে", "কীভাবে", "উপায়", "সমাধান", "এরপর",
    "বৃষ্টি", "বৃষ্টির পর", "বৃষ্টি হলে", "কী হবে", "আগে দিয়েছি", "আগে দিয়েছি",
    "সার মেশানো", "একসাথে", "মিক্স", "কতদিন পর", "কত দিন পর", "আর কোনো", "অন্য কোনো",
)


class ConversationalQueryRewriter:
    """Heuristic gate + LLM rewrite into a standalone retrieval query."""

    def __init__(
        self,
        llm: LLMClient,
        *,
        markers: Sequence[str] = DEFAULT_MARKERS,
        max_history: int = 6,
    ) -> None:
        self.llm = llm
        self.markers = tuple(markers)
        self.max_history = max_history
        self.rewrite_calls = 0

    def should_rewrite(self, query: str, history: Sequence[dict[str, str]]) -> bool:
        if not history:
            return False
        if any(marker in query for marker in self.markers):
            return True
        # Trigger rewrite if the previous assistant turn was a clarification question
        last_turn = history[-1] if history else {}
        if last_turn.get("role") == "assistant" and (
            "কোন ফসলে" in last_turn.get("content", "")
            or "বলবেন কি" in last_turn.get("content", "")
        ):
            return True
        return False

    @staticmethod
    def _prompt(query: str, history: Sequence[dict[str, str]], max_history: int) -> str:
        turns = "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')[:500]}"
            for item in history[-max_history:]
        )
        return f"""তুমি বাংলা কৃষি সহায়কের অনুসন্ধান-প্রশ্ন পুনর্লেখক।
লক্ষ্য: ব্যবহারকারীর সর্বশেষ প্রশ্নটিকে পূর্ববর্তী কথোপকথনের আলোকে একটি একক,
স্বয়ংসম্পূর্ণ অনুসন্ধান প্রশ্নে রূপান্তর করো — অর্থাৎ ইতিহাস ছাড়া পড়লেও বোঝা
যায় কোন ফসল/রোগ/বিষয় নিয়ে জিজ্ঞাসা। প্রশ্নটি ইতিমধ্যে স্বয়ংসম্পূর্ণ হলে
হুবহু অপরিবর্তিত রেখো।
নিয়ম: শুধু পুনর্লিখিত প্রশ্নটি ফেরত দাও — কোনো ব্যাখ্যা, উদ্ধৃতি বা লেবেল নয়।

পূর্ববর্তী কথোপকথন:
{turns or 'নেই'}

সর্বশেষ প্রশ্ন: {query}
পুনর্লিখিত প্রশ্ন:
"""

    async def rewrite(self, query: str, history: Sequence[dict[str, str]]) -> str:
        """Return a standalone rewrite; the raw query on any failure."""
        try:
            text = await self.llm.generate(
                self._prompt(query, history, self.max_history),
                metadata={"role": "query_rewrite"},
            )
            rewritten = text.strip().strip('"').strip("'").strip()
            return rewritten or query
        except Exception:
            return query

    async def maybe_rewrite(self, query: str, history: Sequence[dict[str, str]]) -> tuple[str, bool]:
        """(retrieval_query, was_rewritten) — never raises, never costs without a gate."""
        if not self.should_rewrite(query, history):
            return query, False
        self.rewrite_calls += 1
        rewritten = await self.rewrite(query, history)
        if rewritten == query:
            return query, False
        return rewritten, True