# TASK 01 — Get the Chatbot Actually Talking (Core Functionality First)

**Read `AGENTS.md` and confirm `TASK_00_bootstrap.md` is fully complete before starting this.**
**Assume Task 00 is done: folders exist, Node/pnpm/Python/uv/Ollama/llama.cpp toolchain confirmed installed, empty Next.js + FastAPI skeletons boot.**

---

## 0. Scope — read this before doing anything

**In scope for this task:**
- Getting your fine-tuned Gemma model producing real answers from the command line / a local server.
- Getting retrieval working over your existing 2k+ node knowledge JSON.
- Wiring retrieval + generation together into one backend endpoint.
- A bare, unstyled chat page in the browser that proves the whole pipeline end to end: type a question → get a real, grounded, streamed answer.

**Explicitly out of scope for this task** (later tasks):
- Any UI design/styling — this page should look like a plain HTML form, that's correct and expected.
- The Safety/Router Agent and Verifier Agent from `AGENTS.md` Section 4 — build a **direct** retrieval→generation path for now. The safety wrapper is TASK 02, once the base pipeline is proven to work.
- Crop classifier and YOLO detection — ignored per your instruction.
- Multi-turn conversation memory, chat history persistence — a single question in, single answer out is enough for this task.

The goal of this task is one thing: **prove the novel core — your own fine-tuned model, answering from your own knowledge base, running entirely on your machine — actually works end to end.** Everything else this week is packaging around this fact.

---

## Step 1 — Get a runnable GGUF of your fine-tuned model

You have: an Unsloth LoRA adapter, a downloaded base Gemma model, and llama.cpp installed. llama.cpp needs a merged, quantized **GGUF** file to serve efficiently. There are two valid paths — try Path A first, fall back to Path B if it fails.

### Path A (preferred) — Unsloth's built-in GGUF export
Unsloth ships a direct merge + GGUF export function that handles LoRA-merging and quantization in one call, which is the least error-prone route since it's built specifically for the framework your adapter came from.

1. 🔎 Search for the current Unsloth documentation page on **saving/exporting to GGUF** (their docs and GitHub README are the source of truth — this API has changed across Unsloth versions, don't rely on memorized syntax).
2. Set up a Python environment with `unsloth` installed (this can be a separate throwaway venv if you don't want it polluting the backend's dependencies — it's only needed once, to produce the GGUF file, not at inference time).
3. Load the base model + your adapter through Unsloth as documented, then call its GGUF export/save function, specifying a 4-bit quantization scheme (e.g. `Q4_K_M` — 🔎 confirm current recommended quantization naming/options from Unsloth's docs, and cross-check against llama.cpp's supported quant types since Unsloth calls into llama.cpp's quantizer under the hood).
4. This should produce one `.gguf` file. Move it into `backend/ml_assets/gemma/`.

### Path B (fallback) — manual merge + llama.cpp conversion
Use this only if Path A fails (e.g. version incompatibility, model architecture too new for your installed Unsloth version).

1. In Python, load the base model at **full precision (fp16/bf16), not 4-bit** — merging into a 4-bit-loaded base degrades quality. Use `peft`'s adapter-loading + `merge_and_unload()` to bake the LoRA weights into the base model, then save the merged model in Hugging Face format (safetensors).
2. 🔎 Search llama.cpp's repo for the current conversion script (commonly `convert_hf_to_gguf.py` or similar — the exact script name has changed over llama.cpp's history, confirm the current one). Run it against your merged HF model to produce an fp16 GGUF.
3. 🔎 Confirm your base model's architecture is supported by your installed llama.cpp build (Gemma variants have sometimes required a specific minimum llama.cpp version after release — check llama.cpp's recent release notes/issues if conversion fails with an unrecognized-architecture error, and update llama.cpp if needed).
4. Use llama.cpp's quantization tool (commonly `llama-quantize`) to produce a 4-bit quantized GGUF (`Q4_K_M` is a solid default — 🔎 confirm current recommended default for a model this size).
5. Move the resulting `.gguf` into `backend/ml_assets/gemma/`.

**Verify:** you have exactly one working `.gguf` file for your fine-tuned model sitting in `backend/ml_assets/gemma/`, and its file size is roughly what you'd expect for a 4-bit quant of this model size (sanity-check, not a load-bearing check).

---

## Step 2 — Serve the model locally and test it raw, before touching your backend

1. Start llama.cpp's server binary (commonly `llama-server` — 🔎 confirm current binary/flag names for your installed llama.cpp version, they've shifted over time) pointing at your GGUF file, exposing its local HTTP API (default port commonly `8080` — confirm from your build's `--help` output).
2. From a separate terminal, send one raw test request (`curl`) with a simple Bengali agriculture question, formatted using **Gemma's chat template** (`<start_of_turn>user ... <end_of_turn><start_of_turn>model`) — 🔎 confirm the exact current template for your specific Gemma variant, get it wrong and output quality silently degrades. Many llama.cpp server builds also expose an OpenAI-compatible `/v1/chat/completions` endpoint that applies the chat template for you automatically if the GGUF's metadata includes it — check whether that's working for you, it's less error-prone than hand-formatting the prompt yourself.
3. Confirm the response is coherent, in Bengali (or matches whatever language your fine-tune targets), and reflects your fine-tuning (not generic base-model behavior).
4. Time this raw request. This is your baseline latency number — everything you add later (retrieval, backend hop, streaming) only adds to it, so know this number now.

**Verify:** one successful raw curl round-trip, coherent fine-tuned-quality output, baseline latency noted somewhere (even just a comment in a scratch file).

---

## Step 3 — Load and index your knowledge base JSON

You have a single JSON file with 2,000+ knowledge nodes (treatments, etc.). Start simple — do not reach for a heavy vector database for this.

1. Place the JSON file at `backend/ml_assets/rag_index/knowledge_nodes.json`. Use a rich, structured schema for knowledge nodes. Ensure fields cover: `id`, `crop_bn`, `crop_en`, `disease_bn`, `problem_type`, `question`, `answer`, `treatment`, `dosage` (array of objects with product, amount, unit), `safety_warnings`, `legal_status`, `source`, and `expert_verified`.
2. Write `backend/app/services/rag_index.py`:
   - A loader that reads the JSON once at startup into memory.
   - A retrieval function using **Hybrid BM25 + Dense Retrieval**. Install `rank-bm25` and a lightweight sentence transformer (or FAISS/Chroma). Implement Bangla and Banglish text normalization.
   - Implement crop/disease metadata filtering (e.g., if the query mentions rice, filter by `crop_en=rice`).
   - The retrieval function should take a query string and return the top-k (start with k=3–5) most relevant knowledge nodes.
   - **Low Confidence Rule:** If top-k retrieval confidence is below a defined threshold, return a `low_confidence` flag rather than forcing an ungrounded generation.
3. Write a tiny throwaway test script that loads the index and runs 2–3 sample queries from your domain (e.g. a rice blast treatment question), printing the retrieved nodes, so you can eyeball whether retrieval quality looks right before wiring it into anything else.

**Verify:** retrieval function returns sensible, topically-relevant nodes for a handful of test queries you already know the right answer to.

---

## Step 4 — Wire retrieval + generation together in the backend

1. Write `backend/app/services/llm_client.py`: a thin wrapper (using `httpx`, async) that sends a chat request to your local llama.cpp server and yields the response as a stream of tokens/chunks (not a single blocking call — streaming is what makes this feel fast in the UI later).
2. Write `backend/app/agents/generation_agent.py`: takes a user query + the retrieved knowledge nodes from Step 3, builds a single grounded prompt (system instruction + retrieved context + user question, in the correct chat template format), and calls `llm_client.py` to stream the answer. Keep the system instruction simple and explicit: answer only using the provided context, answer in Bengali, if the context doesn't contain the answer say so rather than guessing.
3. Write `backend/app/api/qa.py`: a `POST /api/qa` route accepting `{"query": "..."}", calling retrieval then `generation_agent`, and streaming the response back to the client (FastAPI's `StreamingResponse`, or Server-Sent Events if that pairs better with your frontend streaming setup in Step 5 — 🔎 confirm which streaming approach the current Vercel AI SDK version expects on the backend side, since it expects a specific response format/protocol).
4. Register this route in `backend/app/main.py`.
5. Test with `curl` directly against `/api/qa` (not through the frontend yet) — confirm you get a streamed, grounded, coherent answer end-to-end from the backend alone.

**Verify:** one successful `curl` call to your own `/api/qa` endpoint returns a streamed answer that's clearly using retrieved context (test with a question you know is covered in the knowledge JSON, and separately test one you know isn't, to confirm the "don't know" behavior works).

---

## Step 5 — Bare-minimum chat page

No design, no styling beyond whatever shadcn defaults happen to apply. Function only.

1. In `frontend/`, create a single page (e.g. `app/chat/page.tsx`) with: a text input, a submit action, and a scrolling area showing the conversation so far.
2. Wire it to `/api/qa` using the Vercel AI SDK's streaming chat hook, pointed at your FastAPI backend (confirm CORS is enabled on the backend for local dev, or proxy the request through a Next.js route handler — 🔎 confirm the current recommended pattern in the AI SDK docs for a non-Next.js/non-Vercel-function backend, since the SDK's default examples usually assume a colocated API route).
3. Type a question, hit submit, watch tokens stream in.

**Verify:** you can open the chat page in a browser, ask a real Bengali agriculture question, and watch a real, grounded, streamed answer come back from your own fine-tuned model — with no design polish at all. This is the milestone. Everything else this week builds on top of this working.

---

## Step 6 — Sanity test set & Evaluation Metrics

Before calling this task done, run through a preliminary test set and establish evaluation metrics for the publication:
1. 2–3 questions you know are well-covered in the knowledge JSON → expect specific, grounded, correct answers.
2. 1 question clearly outside the knowledge base's coverage → expect an honest "I don't have information on this" rather than a hallucinated answer.
3. 1 question in mixed Bengali/English (matching how you'd naturally phrase it) → expect the model to handle it gracefully, since that's realistic usage.
4. **Latency Metrics:** Note the end-to-end latency (question submitted → first token appears, and question submitted → full answer done).
5. **Retrieval Evaluation Metrics:** Prepare scripts to compute Recall@k, Precision@k, MRR, nDCG@k, and Hit rate over an offline benchmark dataset to evaluate hybrid vs BM25 retrieval. Note expert relevance rating procedures.

---

## Step 7 — Report back

Write `TASK_01_REPORT.md` at repo root:
- Which path (A or B) worked for GGUF export, and the exact quantization used.
- Confirmed llama.cpp server command that successfully serves the model (so it's reproducible without re-discovering flags).
- Retrieval approach used (BM25 confirmed working) and the knowledge JSON's actual field schema as discovered in Step 3.
- Results of the Step 6 sanity test set, including latency numbers.
- Anything that had to deviate from this plan, and why.

**Stop here.** Do not touch UI design, the safety/verifier agents, the crop classifier, or YOLO in this task — those are separate, later tasks, and this document's only job was proving the core chatbot works.