# R6 — Capability Registry (the extension seam)

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part D.1 + Part J item R6
- **Depends on:** R5 (produces the `Intent` capabilities route on)
- **Blocks:** future capability modules (irrigation, market price, drone) — none in this task
- **Amendment:** none — introduces a port + registration of *existing* features; no new farmer-facing behavior

## Goal

Make farmer-facing features **plug-ins behind one port** instead of branches
inside the pipeline, so adding irrigation/market-price/drone later is "register a
capability + its data artifacts," not "edit the orchestrator." R6 defines the
`Capability` port and **registers the features that already exist** — several as
honest `available: false` stubs. It changes **no** routing behavior yet: the QA
pipeline still runs exactly as today; the registry is introspective metadata plus
a routing *seam* that currently only describes reality.

This is deliberately a **seam, not a rewrite**. The clean-architecture layers
(`domain / application / ports / infrastructure`) already exist; R6 adds the
missing capability contract and an honest registry the UI and paper can point at.

## The port (from plan D.1)

```python
class Capability(Protocol):
    id: str                              # "disease_advisory", "qa_advisory", ...
    requires: frozenset[str]             # "vision" | "weather" | "farm_profile" | "facts"
    available: bool                      # honest false when assets are missing
    def can_handle(self, intent: Intent) -> float      # 0..1 claim strength
    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult
```

`CapabilityResult` carries `resolution_tier` (R3), answer, provenance, and cost —
i.e. the same shape a `QAResult` already exposes, so registering the existing QA
path is wrapping, not reinventing.

## What to register now (plan D.1 — honesty over vapor)

| id | requires | available today | backing |
|---|---|---|---|
| `qa_advisory` | `facts?`,`corpus` | **true** | wraps the existing T3 QA pipeline |
| `disease_advisory` | `vision`,`facts` | **true** | vision classifiers + (R4) fact resolver |
| `soil_advisory` | `soil` | **true (replay-only)** | replay analyzer; flag replay-only in metadata |
| `weather_risk` | `weather` | **true** | PR1 late-blight alert |
| `stage_advice` | `farm_profile`,`facts` | **true** | P2 crop calendar |
| `safety_escalation` | — | **true** | 16123 canned redirect |
| `irrigation` | `sensor`,`weather` | **false** | reserved stub |
| `market_price` | `timeseries` | **false** | reserved stub |
| `drone_survey` | `vision` | **false** | reserved stub |
| `livestock` | — | **false** | reserved stub |
| `credit` | — | **false** | reserved stub |

`available` must be computed from whether the required assets/loaders are present
at container build time — never hardcoded true. A stub with no assets reports
`false` and `can_handle` returns 0.

## Design — a seam that describes reality first

R6 lands in two safe halves so it can never break the live path:

1. **Registry + introspection (this task's core).** Build the registry at
   container time, register the wrappers above, and expose it read-only via a new
   `GET /api/capabilities` (id, available, requires, short Bengali label). This
   is pure metadata — the QA pipeline is untouched. The UI/paper immediately gets
   an honest capability map.
2. **Routing seam (behind a default-off flag).** An optional
   `CapabilityRouter.route(intent) -> Capability | None` that, when
   `capability_routing_enabled` is on, picks the highest `can_handle` available
   capability. **Default off → the pipeline behaves exactly as today** (every
   query goes to `qa_advisory`, i.e. the current path). With the flag on, the
   only capability that can currently *resolve differently* is still the QA
   pipeline, so even on, behavior is unchanged until a real second capability
   ships. The flag exists so R-future capabilities are a registration, not a
   pipeline edit.

## Scope — create
- `backend/app/ports/capability.py` — the `Capability` Protocol +
  `CapabilityContext` + `CapabilityResult` dataclasses.
- `backend/app/application/capabilities/__init__.py`
- `backend/app/application/capabilities/registry.py` — `CapabilityRegistry`
  (register, list, `available` computation) + `CapabilityRouter` (flagged).
- `backend/app/application/capabilities/qa_capability.py` — wraps the existing
  `QAPipeline.answer` as the `qa_advisory` capability (the one real resolver).
- `backend/app/application/capabilities/stubs.py` — the `available: false`
  reserved capabilities + thin wrappers for soil/weather/stage/safety that
  declare metadata without duplicating their logic.
- `backend/app/api/capabilities.py` — `GET /api/capabilities` (read-only).
- `backend/tests/test_capability_registry.py`

## Scope — modify
- `backend/app/application/container.py` — build the registry from the already-
  constructed services (`build_container`, line 56+); attach it to
  `AppContainer`. Compute `available` from real asset presence.
- `backend/app/main.py` (or the router include site) — mount `/api/capabilities`.
- `backend/app/core/config.py` + `.env.example` — `CAPABILITY_ROUTING_ENABLED`
  (default `false`).

## Do not touch
- `qa_pipeline.py` answer logic — the QA capability *wraps* it, does not modify
  it. No change to safety, retrieval, generation, verifier.
- Any capability's underlying feature (soil replay, PR1, P2) — R6 only *declares*
  them, it does not re-implement them.

## Invariants
- **Flag off → byte-identical to today** (full suite + golden replay unchanged).
- `available` is derived from asset presence at build time, never a literal
  `True`; a stub with missing assets is provably `false` (test-locked).
- Registering a capability performs **no network and no LLM call** at
  construction (assert with a fake that raises).
- `GET /api/capabilities` is read-only, requires no auth beyond existing rules,
  and never exposes provider keys, prompts, or internal paths.
- A reserved stub's `can_handle` returns 0 and `resolve` raises
  `CapabilityUnavailable` (never a fabricated answer).

## Verification gate (stop/go)
1. `uv run pytest tests/test_capability_registry.py -v` — green (registration,
   `available` computation, stub refusal, no-I/O-at-build).
2. `uv run pytest tests/test_api.py -v` — green; `/api/capabilities` returns the
   honest map (6 available, 5 reserved-false).
3. Full `tests/` suite — 410/7/0 baseline held.
4. Golden replay 50/50 PASS with flag off and on (on = still all `qa_advisory`).
5. `pnpm build` green (no frontend change required in R6; R11 consumes the map).

## Rollback
`git revert`. Additive port + registry + one read-only route + a default-off
flag; nothing in the live answer path changes.

## External sources
None.

## Notes for the implementing agent
- The temptation is to start *routing* real traffic through the registry. Do not.
  R6's value is the honest seam + the introspection endpoint. Real routing only
  becomes meaningful when a second resolving capability exists, and each such
  capability is its own future task with its own assets + golden set (plan D.3).
- Keep `available` honest: soil is replay-only, weather depends on R8's real
  snapshot, disease_advisory's fact half depends on R4. Encode those dependencies
  in the `requires`/`available` computation rather than optimistic defaults.
