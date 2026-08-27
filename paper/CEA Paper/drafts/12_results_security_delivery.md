# Section 12: Results — Security, Offline Resilience & Constrained Delivery (Draft Skeleton)

## 12.1 Security & Prompt Injection Immunity
- 1,400 injection and context-poisoning attacks (Layer E07, E22).
- BAA achieves 0.0% injection survivability [0.0%, 0.27%] into final advice or outbound SMS (Table 9).

## 12.2 Deterministic SMS Compression Fidelity
- 1,000 certified advisory tuples compressed into 160-char GSM payloads (Layer E15).
- 100.0% critical parameter survival (dosage, PHI, interval) in 102--115 chars vs 64.4% PHI truncation hazard in LLM-composed SMS.

## 12.3 Rural Cellular Network Degradation
- Stress testing under simulated 4G, 3G, Rural Edge (800ms / 15% loss), and Severe 2G (1200ms / 30% loss) (Layer E14).
- Offline-first cache sustains 91.4% delivery at 15% loss and 80.3% at 30% loss (+21.6 pp over cloud RAG).
