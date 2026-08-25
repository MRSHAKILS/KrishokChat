# Knowledge Ingestion Contract

**Owner:** researcher / sole engineer
**Status:** R1 DONE — 2026-08-25
**Enforced by:** `backend/tests/test_ingestion_contract.py`

---

## The invariant

> **Adding knowledge is editing a data file and re-running a builder — never a
> Python change.**

---

## The six clauses

| # | Clause | Enforcement |
|---|---|---|
| 1 | **Curated source is a data file.** Human-editable JSON with per-entry `source` (citation) + `grounding` (`corpus-extracted` \| `curated-approximation`). | Convention; tested by `test_curated_calendars_no_invented_grounding`. |
| 2 | **Builder is deterministic + offline.** Same inputs → byte-identical output (sorted keys, no timestamps in the payload body — provenance dates live in a `provenance` sub-key). | `test_*_builder_zero_diff` tests re-run both builders and diff. |
| 3 | **Artifact is versioned + committed + SHA-256-pinned.** Filename carries `_vN`; builder prints and records a SHA-256 digest; the version participates in cache keys. | `sha256_of` + `ArtifactProvenance.sha256` in every artifact's `provenance` block. |
| 4 | **Loader is fail-open.** Missing/corrupt/empty artifact → feature inert (returns `None`), never a 500. | `load_fail_open` helper; `test_load_fail_open_*` tests. |
| 5 | **No fabricated rows, ever.** An unextractable value is absent or marked `curated-approximation`, never invented. | Code review + `test_curated_calendars_no_invented_grounding`. |
| 6 | **Rejections are archived, not deleted.** Extraction candidates that fail build-time validation are written to a `rejected/` sibling for the paper's error analysis. | `build_fact_base.py` implements this (R2); future builders must too. |

---

## Shared helpers (`app.infrastructure.ingestion.contract`)

```python
from app.infrastructure.ingestion.contract import (
    write_deterministic_json,   # clause 2+3: sorted, utf-8, trailing newline, atomic
    sha256_of,                  # clause 3: SHA-256 of an artifact file
    ArtifactProvenance,         # clause 3: provenance block dataclass
    load_fail_open,             # clause 4: fail-open JSON loader with validation callback
)
```

### `write_deterministic_json(path, payload) -> str`
Writes `payload` to `path` with sorted keys, `ensure_ascii=False`, 2-space indent, trailing newline, atomically (tmp → replace). Returns the hex SHA-256 of the bytes written. Use the return value in `provenance.sha256`.

### `sha256_of(path) -> str`
Returns the hex SHA-256 of the bytes of an existing file.

### `ArtifactProvenance`
```python
ArtifactProvenance(
    source_id="dose_reference",
    endpoint_or_file="ml_assets/rag_index/derived/dose_reference_v1.json",
    fetched_at="2026-08-25T00:00:00Z",  # build time, not request time
    builder="backend/scripts/build_dose_reference.py",
    sha256="<hex digest>",
)
```

### `load_fail_open(path, validate) -> T | None`
Loads a JSON file and passes the parsed dict to `validate(payload) -> T`. Returns `None` on any error (missing file, corrupt JSON, `ValueError` / `KeyError` / `TypeError` from validate). Logs a warning in all failure cases.

---

## Reference implementations

Both existed before R1 and ARE the pattern. Do not reinvent:

- **Builder:** [`backend/scripts/build_dose_reference.py`](../../../backend/scripts/build_dose_reference.py)
- **Loader:** [`backend/app/infrastructure/verification/dose_reference.py`](../../../backend/app/infrastructure/verification/dose_reference.py) → `load_dose_reference`

- **Builder:** [`backend/scripts/build_crop_calendars.py`](../../../backend/scripts/build_crop_calendars.py)
- **Loader:** [`backend/app/infrastructure/agronomy/calendar_store.py`](../../../backend/app/infrastructure/agronomy/calendar_store.py) → `load_crop_calendars`

---

## New asset checklist

When adding a new knowledge asset (crop, pest, deficiency, …):

- [ ] Edit the curated source JSON (human-editable seed).
- [ ] Re-run the builder script: `uv run python scripts/build_<asset>.py`.
- [ ] Verify zero diff: `git diff --exit-code <artifact_path>`.
- [ ] Commit the updated artifact.
- [ ] Add/update the artifact's `provenance.sha256` from the builder's printed digest.
- [ ] Run `uv run pytest tests/test_ingestion_contract.py -v` — green.
- [ ] **No Python changes required** — if you needed to edit Python to add data, the contract is broken.
