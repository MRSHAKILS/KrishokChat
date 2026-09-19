# Gemma — Local Model Assets

This directory holds the local KrishokTech Gemma weights and Ollama `Modelfile`.

## Canonical GGUF

* **Canonical file:** `krishoktech.f16.gguf` (1.36 GB, SHA256 `1D627304F74520284844812600F5F0E172240C8A23C88126BA7D1C1F73B84673`)
* **Alias:** `model.gguf` is a **hardlink** to `krishoktech.f16.gguf` — same inode, zero extra space. Kept only because `backend/app/core/config.py:gguf_path` defaults to `backend/ml_assets/gemma/model.gguf` and `scripts/local_model.ps1` / `Modelfile: FROM ./model.gguf` reference that name.

> Do not create a second independent copy. If you replace the weights, replace `krishoktech.f16.gguf` and re-create the hardlink:
> ```powershell
> Remove-Item backend/ml_assets/gemma/model.gguf
> New-Item -ItemType HardLink -Path backend/ml_assets/gemma/model.gguf -Value backend/ml_assets/gemma/krishoktech.f16.gguf
> fsutil hardlink list backend/ml_assets/gemma/krishoktech.f16.gguf  # should show 2 entries
> ```

## Modelfile

* `Modelfile` — canonical Ollama definition (`FROM ./model.gguf`, tag `krishoktech-4b`). Used by `scripts/local_model.ps1`.
* `Modelfile.krishoktech` — archived variant (`FROM gemma3:4b`, no GGUF). Kept for reference, not used in the current flow.

## Git status

`*.gguf` and `*.safetensors` are gitignored (`.gitignore: backend/ml_assets/gemma/*.gguf`). Only `.gitkeep`, `README.md`, and `Modelfile` are tracked.

## Warning

The checked-in `krishoktech.f16.gguf` is **truncated** and must not be served (see `docs/refactor/PROJECT_HANDOFF.md` + `paper/system_evolution_plan_2026/execution_planning_2026_08_12/14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`). The verified demo runtime uses an external Q4_K_M base + LoRA via `scripts/start_krishoktech_local.ps1`.

## Verification after H2

```powershell
Get-FileHash backend/ml_assets/gemma/krishoktech.f16.gguf
Get-FileHash backend/ml_assets/gemma/model.gguf   # same hash
fsutil hardlink list backend/ml_assets/gemma/krishoktech.f16.gguf  # 2 entries
```
