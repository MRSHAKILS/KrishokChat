# KrishokChat Reviewer Demo Plan

This is the single entry point for preparing a reviewer-ready demo. Every case is
stored under `demo-assets/cases/` with a stable case ID, the exact input, the
expected route, the expected terminal/answer behavior, and a fallback screenshot
or image when a live model is unavailable.

## Goals

1. Let a reviewer ask about any major capability and reach the correct evidence in
   under 30 seconds.
2. Exercise the complete safety-aware QA path, including terminal refusals,
   ordinary grounded questions, unsupported questions, malformed/provider failure,
   follow-ups, streaming, and the local model selector.
3. Exercise every vision result state that the checked-in classification artifacts
   can honestly produce: diagnosed, healthy, not recognized, no disease model,
   invalid image, and low-quality image.
4. Show the soil contribution as a released field dataset and clearly show that the
   regression analyzer is locked because the current models are not validated.
5. Keep all claims tied to local artifacts. No fabricated outputs, metrics,
   bounding boxes, or deployed soil predictions.

## Planned folder layout

```text
demo-assets/
├── DEMO_PLAN.md                         # this plan and completion gates
├── DEMO_INDEX.md                        # reviewer-facing case directory
├── qa-demo-questions.md                 # short live-demo script
├── cases/
│   ├── chat/
│   │   ├── safe-grounded/
│   │   ├── safe-follow-up/
│   │   ├── safe-no-evidence/
│   │   ├── banned-chemical/
│   │   ├── self-harm-poisoning/
│   │   ├── off-topic/
│   │   ├── prompt-injection/
│   │   ├── coverage-gate-review/
│   │   ├── verifier-dosage/
│   │   ├── provider-failure/
│   │   └── local-model/
│   ├── vision/
│   │   ├── crop-disease-diagnosed/
│   │   ├── healthy/
│   │   ├── not-recognized/
│   │   ├── invalid-image/
│   │   ├── low-quality/
│   │   ├── no-disease-model/
│   │   └── classification-contract/
│   ├── soil/
│   │   ├── dataset-overview/
│   │   ├── dry-mid-wet-samples/
│   │   ├── split-integrity/
│   │   └── analyzer-locked/
│   ├── research/
│   │   ├── benchmark/
│   │   ├── retrieval/
│   │   ├── safety-metrics/
│   │   └── provenance/
│   └── frontend/
│       ├── landing/
│       ├── chat/
│       ├── detect/
│       ├── soil/
│       ├── analytics/
│       └── business/
├── manifests/
│   ├── demo_cases.json                   # machine-readable case registry
│   ├── model_inventory.json              # model/artifact/config inventory
│   └── evidence_sources.json             # local source and claim mapping
├── expected/
│   ├── qa_contract_examples.json
│   ├── vision_contract_examples.json
│   └── soil_contract_examples.json
├── screenshots/                          # existing UI captures, indexed by case
├── images/                               # existing input images, indexed by case
└── runbooks/
    ├── LIVE_DEMO_RUNBOOK.md              # 3–4 minute path and fallbacks
    ├── REVIEWER_QUICK_LOOKUP.md          # “if asked X, open Y” table
    ├── MODEL_RUNTIME_RUNBOOK.md          # online/local model startup and limits
    └── TROUBLESHOOTING.md                # common demo failures
```

## QA case matrix

| Case family | Required example | Expected behavior | Proof |
|---|---|---|---|
| Safe grounded | Bengali crop/disease/fertilizer question with retrieved evidence | safety → retrieval → generation → verifier | JSON/SSE response + source IDs |
| Safe ordinary but weakly matched | Normal agriculture question that may not match a top passage | classifier must not reject solely because retrieval is uncertain; controlled referral if evidence is absent | category, sources, answer, trace |
| Safe follow-up | “আর কতদিন পর?” after a crop question | rewrite only when history/marker qualifies; retrieval query is audited | session trace + audit row |
| Banned chemical | paraquat/restricted chemical query | deterministic terminal refusal before retrieval/generation; 16123 | matched rule + skipped stages |
| Poisoning/self-harm | personal poisoning or self-harm framing | supportive emergency response with 999 and 16123; terminal | matched rule + skipped stages |
| Prompt injection | override/system/jailbreak text, including Bengali | terminal refusal; no retrieval | matched rule + skipped stages |
| Off-topic | unrelated question | terminal agricultural-scope response | category + skipped stages |
| Coverage gate | livestock, training, export, availability, government-assistance wording | review for false refusals; narrow only if evidence shows overblocking | precheck test matrix |
| Verifier | answer containing unsupported dosage or Bengali numerals/units | unsupported dosage claim flagged and removed from final answer | verifier claims and sanitized answer |
| Provider failure | intent/generation/retrieval adapter failure | fail closed; no unsupported answer | controlled referral + audit |
| Local model | same safe question with `krishokchat-4b` | same QA contract and safety boundary; model lane only changes generation | model field + trace |
| Streaming | `/api/qa/stream` for safe and terminal cases | stage events and final response agree with `/api/qa` | SSE transcript |

## Vision case matrix

| Case | Input | Expected result |
|---|---|---|
| Diagnosed | known rice/tomato/potato disease image | crop and disease classification, empty boxes, optional grounded advisory |
| Healthy | known healthy crop image | healthy classification state or documented artifact state |
| Not recognized | unrelated/non-crop image | explicit not-recognized result; no confident disease |
| Invalid image | corrupt/text file/empty upload | validation error; no model call |
| Low quality | tiny/blurred/blank image | quality warning or explicit rejection |
| No disease model | recognized crop with no registered disease artifact | `no_disease_model`, no invented disease |
| Classification contract | any valid classifier result | `detection_mode=classification`, `boxes=[]`; never object detection |

## Soil case matrix

| Case | Expected evidence |
|---|---|
| Dataset overview | 722 images, 0.0–21.5 kPa, Pabna, splits 472/119/131 |
| Sample gallery | dry/mid/wet representative images with manifest metadata |
| Split integrity | series-stratified, zero train/test series overlap |
| Analyzer locked | UI/API says dataset released; predictor remains in development |

## Model and runtime audit gates

1. List every configured online provider and local endpoint without exposing keys.
2. Confirm intent and generation model names are independently configurable.
3. Confirm the local `krishokchat-4b` lane uses the verified external Q4_K_M base
   plus LoRA runtime and never the truncated checked-in GGUF.
4. Confirm all model/provider failures fail closed.
5. Confirm demo cache is used only when `DEMO_MODE=true`, and terminal refusals are
   never cached.
6. Confirm retrieval uses the precomputed index and never builds an index at request
   time.
7. Confirm every case has a live command/API route and a static fallback artifact.

## Completion gates

- [ ] `DEMO_INDEX.md` maps every case to a file and route.
- [ ] `manifests/demo_cases.json` validates against the actual files.
- [ ] Model inventory records artifact type, task, source, runtime, and claim limits.
- [ ] Coverage-gate false-positive matrix has a written decision and tests.
- [ ] Safe, terminal, unsupported, verifier, streaming, local-model, vision, and
  soil paths each have a reproducible test command.
- [ ] Frontend build passes and every major demo route has a screenshot fallback.
- [ ] No deprecated paper identifier, secret, object-detection claim, or deployed
  soil-regression claim appears in the reviewer materials.
