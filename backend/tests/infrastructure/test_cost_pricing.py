"""R7 — Tests for model pricing table and cost estimation.

Locks all R7 invariants:
  1. estimate_cost returns real USD cost only when tokens and price entry exist.
  2. Unknown tokens or unknown model strictly returns None (no fabrication).
  3. Local inference / Ollama computes to $0.00.
  4. load_model_prices is fail-open (missing/corrupt file returns {}).
  5. Committed backend/config/model_prices.json conforms to schema and has source_url + fetched_at.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.application.telemetry import estimate_cost, load_model_prices


# ---------------------------------------------------------------------------
# Unit tests for estimate_cost
# ---------------------------------------------------------------------------


def test_estimate_cost_exact_calculation() -> None:
    custom_table = {
        "openrouter/google/gemini-2.5-flash-lite": {
            "input_usd_per_1k": 0.000100,
            "output_usd_per_1k": 0.000400,
        }
    }
    tokens = {"input": 2000, "output": 500}
    cost = estimate_cost(
        tokens=tokens,
        provider="openrouter",
        model="google/gemini-2.5-flash-lite",
        price_table=custom_table,
    )
    # Expected: (2000/1000)*0.0001 + (500/1000)*0.0004 = 0.0002 + 0.0002 = 0.0004
    assert cost is not None
    assert pytest.approx(cost, rel=1e-6) == 0.0004


def test_estimate_cost_zero_for_local_inference() -> None:
    custom_table = {
        "ollama/krishokchat-4b": {
            "input_usd_per_1k": 0.0,
            "output_usd_per_1k": 0.0,
        }
    }
    tokens = {"input": 1500, "output": 350}
    cost = estimate_cost(
        tokens=tokens,
        provider="ollama",
        model="krishokchat-4b",
        price_table=custom_table,
    )
    assert cost == 0.0


def test_estimate_cost_missing_tokens_returns_none() -> None:
    assert estimate_cost(tokens=None, provider="openrouter", model="google/gemini-2.5-flash-lite") is None
    assert estimate_cost(tokens={}, provider="openrouter", model="google/gemini-2.5-flash-lite") is None


def test_estimate_cost_unknown_model_returns_none() -> None:
    custom_table = {"openrouter/known-model": {"input_usd_per_1k": 0.001, "output_usd_per_1k": 0.002}}
    tokens = {"input": 100, "output": 100}
    cost = estimate_cost(
        tokens=tokens,
        provider="openrouter",
        model="unknown-model-xyz",
        price_table=custom_table,
    )
    assert cost is None


def test_estimate_cost_missing_provider_returns_none() -> None:
    tokens = {"input": 100, "output": 100}
    assert estimate_cost(tokens=tokens, provider=None, model="some-model") is None


# ---------------------------------------------------------------------------
# Loader fail-open tests
# ---------------------------------------------------------------------------


def test_load_model_prices_missing_file(tmp_path: Path) -> None:
    prices = load_model_prices(path=tmp_path / "nonexistent.json")
    assert prices == {}


def test_load_model_prices_corrupt_file(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("invalid json", encoding="utf-8")
    prices = load_model_prices(path=bad)
    assert prices == {}


def test_load_model_prices_valid_file(tmp_path: Path) -> None:
    f = tmp_path / "prices.json"
    f.write_text(
        json.dumps({
            "version": 1,
            "prices": {"test/model": {"input_usd_per_1k": 0.001, "output_usd_per_1k": 0.002}}
        }),
        encoding="utf-8",
    )
    prices = load_model_prices(path=f)
    assert "test/model" in prices
    assert prices["test/model"]["input_usd_per_1k"] == 0.001


# ---------------------------------------------------------------------------
# Committed artifact schema verification
# ---------------------------------------------------------------------------


def test_committed_model_prices_schema() -> None:
    artifact_path = Path(__file__).resolve().parents[2] / "config" / "model_prices.json"
    assert artifact_path.exists(), "backend/config/model_prices.json must exist"

    with open(artifact_path, encoding="utf-8") as fh:
        data = json.load(fh)

    assert "version" in data
    assert "fetched_at" in data
    assert "prices" in data and isinstance(data["prices"], dict)
    assert len(data["prices"]) > 0

    for key, row in data["prices"].items():
        assert "input_usd_per_1k" in row, f"Missing input_usd_per_1k for {key}"
        assert "output_usd_per_1k" in row, f"Missing output_usd_per_1k for {key}"
        assert "source_url" in row, f"Missing source_url for {key}"
        assert "fetched_at" in row, f"Missing fetched_at for {key}"
        assert isinstance(row["input_usd_per_1k"], (int, float))
        assert isinstance(row["output_usd_per_1k"], (int, float))
        assert row["input_usd_per_1k"] >= 0.0
        assert row["output_usd_per_1k"] >= 0.0
