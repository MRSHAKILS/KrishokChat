# Reviewer Quick Index

Use this file when a reviewer asks for a capability.

| Reviewer asks | Open first | Live route |
|---|---|---|
| “Show a normal Bengali agricultural answer.” | `screenshots/02_chat_grounded.png` | `/chat` → `POST /api/qa/stream` |
| “What happens with a dangerous chemical?” | `screenshots/03_chat_safety_refusal.png` | `/chat` → paraquat preset |
| “What if someone asks for poisoning help?” | `screenshots/10_chemical_safety_chat_rejection.png` | `/chat` → poisoning case |
| “Can it resist prompt injection?” | `screenshots/09_chemical_safety_sandbox_full.png` | `/chat` → injection case |
| “Show the verifier.” | `screenshots/09_chemical_safety_tight_card.png` | `/chat` → dosage case |
| “Show image diagnosis.” | `screenshots/04_detect_diagnosis.png` | `/detect` → rice sample with crop hint |
| “Does it draw bounding boxes?” | `demo-assets/manifests/model_inventory.json` | answer: classification only, `boxes=[]` |
| “What about tomato?” | `images/tomato/` + case `vision.unsupported_tomato_boundary` | answer: no registered tomato disease model |
| “Show the soil model.” | `screenshots/05_soil_moisture.png` | `/soil` → analyzer remains locked |
| “Who uses or pays for this?” | `screenshots/07_business_full.png` | `/business` |
| “Show benchmark evidence.” | `screenshots/08_data_benchmark.png` | `/research/benchmark` |
| “Show safety metrics.” | `screenshots/06_analytics_dashboard.png` | `/analytics` → local audit metrics |

The machine-readable source is `manifests/demo_cases.json`. The complete test
procedure is in `DEMO_PLAN.md`; runtime startup and troubleshooting will be added
after the first end-to-end pass.
