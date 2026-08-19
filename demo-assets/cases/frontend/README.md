# Frontend Route Index

All routes build cleanly (`pnpm build` verified 2026-08, Next.js 16.3.0).

| Route | Purpose | Screenshot |
|-------|---------|------------|
| `/` | Landing/marketing | `screenshots/01_landing_full.png` |
| `/chat` | QA chat with agent trace stepper | `screenshots/02_chat_grounded.png` |
| `/detect` | Disease diagnosis (classification) | `screenshots/04_detect_diagnosis.png` |
| `/soil` | Soil moisture dataset (analyzer locked) | `screenshots/05_soil_moisture.png` |
| `/analytics` | Safety metrics from local audit | `screenshots/06_analytics_dashboard.png` |
| `/business` | Business model | `screenshots/07_business_full.png` |
| `/research` (+ `/research/benchmark`, `/research/methodology`, `/research/safety`) | Credibility content | `screenshots/08_data_benchmark.png` |
| `/data` | Dataset library | — |
| `/library` | Model/paper library | — |
| `/about`, `/team`, `/contact` | Static | — |
| `/auth`, `/account` | Supabase auth (additive, never gates the demo) | — |

Agent trace: the chat and detect pages render a Motion-animated stepper
(safety → retrieval → generation → verifier) driven by `agent_trace` events.