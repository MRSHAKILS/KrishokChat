"""Backward-compatibility shim for tests importing from tests.test_pipeline.

Re-exports fakes and utilities from tests.rag_pipeline.test_pipeline.
"""

from tests.rag_pipeline.test_pipeline import (
    FakeAudit,
    FakeLLM,
    FakeRetriever,
    FakeSessions,
    make_pipeline,
)

__all__ = [
    "FakeAudit",
    "FakeLLM",
    "FakeRetriever",
    "FakeSessions",
    "make_pipeline",
]
