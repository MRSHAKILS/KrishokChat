# DEPRECATED — legacy shim

This package (`backend/app/services/advisory/`) is a **compatibility shim only**.

- **Do not extend.** New code must use the canonical pipeline under `backend/app/application/`, `backend/app/domain/`, `backend/app/ports/`, and `backend/app/infrastructure/` per `docs/refactor/ARCHITECTURE.md`.
- `application/qa_pipeline.py` is the single source of truth for QA (safety → retrieval → generation → verifier → audit). `services/advisory/` must not contain a second active pipeline.
- Kept only so older scripts/imports (`from app.services.advisory...`) do not break. Any new advisory logic belongs in `application/` + `domain/` + `infrastructure/`.

See `docs/refactor/ARCHITECTURE.md` section 5.1 and `docs/refactor/REFACTOR_PLAN.md` for the staged migration.
