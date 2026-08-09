# Multi-Turn Chat — Session Memory Plan

## Objective
Enable follow-up questions in the QA chat by maintaining conversation history per session, so the LLM understands references like "মাত্রা কত?" after "আলুর দেরি ব্লাইটের প্রতিকার কি?".

## Research Findings

### Industry Standards (2024-2026)
1. **OpenAI Chat Completions format**: Messages array with `role: system|user|assistant|tool`. Each request includes full conversation. Most widely adopted.
2. **Vercel AI SDK**: `useChat` hook manages message history, streaming, and session state. Industry standard for Next.js.
3. **Session management patterns**:
   - **Stateless**: Client sends full history each request (simple, scales horizontally)
   - **Stateful server**: Server stores history keyed by session_id (lower bandwidth, needs eviction)
   - **Redis-backed**: For multi-server deployments
4. **Context window management**: Keep last N turns (typically 6-10) to avoid exceeding token limits. Summarize older turns if needed.
5. **Streaming**: SSE with `text/event-stream` for token-by-token display. Vercel AI SDK uses this natively.

### Best Practices
- **Session ID**: UUID v4, generated client-side, sent with each request
- **History limit**: Max 10 turns (20 messages) to stay within context window
- **TTL**: 30-minute inactivity eviction for server-side stores
- **Format**: `[{role: "user", content: "..."}, {role: "assistant", content: "..."}]`
- **System prompt**: Include detected crop/disease context + safety rules
- **Error handling**: If history too long, drop oldest turns (keep first system message)

### Interface Design
```
┌─────────────────────────────────────┐
│  🌾 কৃষক চ্যাট                      │
│  ─────────────────────────────────  │
│  👤 আলুর দেরি ব্লাইটের প্রতিকার কি?   │
│  ─────────────────────────────────  │
│  🤖 আলুর লেট ব্লাইট দমনে...          │
│     প্রতি লিটার পানিতে ২ গ্রাম...    │
│  ─────────────────────────────────  │
│  👤 মাত্রা কত?                       │
│  ─────────────────────────────────  │
│  🤖 আপনার পূর্বের প্রশ্নে উল্লেখিত... │
│     মাত্রা: প্রতি লিটার ২ গ্রাম...     │
│  ─────────────────────────────────  │
│  [আপনার প্রশ্ন লিখুন...] [জিজ্ঞাসা]    │
└─────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Backend — Session Store + History API

**File: `backend/app/services/advisory/session_store.py`**
```python
"""In-memory session store with TTL eviction."""
import time
import threading
from collections import OrderedDict
from typing import Optional

class SessionStore:
    def __init__(self, max_turns: int = 10, ttl_seconds: int = 1800):
        self._store: OrderedDict[str, list[dict]] = OrderedDict()
        self._timestamps: dict[str, float] = {}
        self._max_turns = max_turns
        self._ttl = ttl_seconds
        self._lock = threading.Lock()

    def get(self, session_id: str) -> list[dict]:
        with self._lock:
            self._evict_expired()
            return self._store.get(session_id, [])

    def append(self, session_id: str, role: str, content: str):
        with self._lock:
            self._evict_expired()
            if session_id not in self._store:
                self._store[session_id] = []
            history = self._store[session_id]
            history.append({"role": role, "content": content})
            # Keep only last max_turns * 2 messages (user + assistant pairs)
            if len(history) > self._max_turns * 2:
                self._store[session_id] = history[-self._max_turns * 2:]
            self._timestamps[session_id] = time.time()

    def clear(self, session_id: str):
        with self._lock:
            self._store.pop(session_id, None)
            self._timestamps.pop(session_id, None)

    def _evict_expired(self):
        now = time.time()
        expired = [sid for sid, ts in self._timestamps.items() if now - ts > self._ttl]
        for sid in expired:
            self._store.pop(sid, None)
            self._timestamps.pop(sid, None)

# Global instance
session_store = SessionStore()
```

**File: `backend/app/models/schema.py` — Update QARequest**
```python
class QARequest(BaseModel):
    query: str
    session_id: str | None = None
    crop: str | None = None
    disease: str | None = None
    history: list[dict] = []  # [{role, content}] — client can pass history directly
```

**File: `backend/app/api/qa.py` — History integration**
```python
# In qa_endpoint:
if request.session_id and not request.history:
    request.history = session_store.get(request.session_id)

# After generation:
if request.session_id:
    session_store.append(request.session_id, "user", request.query)
    session_store.append(request.session_id, "assistant", gen["response"])
```

**File: `backend/app/services/advisory/generator.py` — History in prompt**
```python
def build_prompt(query, detected_crop, detected_disease, intent,
                 retrieved_nodes, disease_details=None, history=None):
    context_parts = []

    # Add conversation history (excluding current query)
    if history:
        context_parts.append("### পূর্ববর্তী কথোপকথন:")
        for msg in history[-6:]:  # Last 3 turns
            role = "কৃষক" if msg["role"] == "user" else "সহায়ক"
            context_parts.append(f"{role}: {msg['content']}")
        context_parts.append("")

    # ... rest of context building ...
```

### Phase 2: Frontend — Chat UI with History

**File: `frontend/src/components/qa-panel.tsx`**
```tsx
// Add state:
const [sessionId] = useState(() => crypto.randomUUID())
const [messages, setMessages] = useState<Array<{role: "user" | "assistant", content: string}>>([])

// On submit:
setMessages(prev => [...prev, {role: "user", content: query}])
const history = messages.map(m => ({role: m.role === "user" ? "user" : "assistant", content: m.content}))
const final = await streamQuestion(query, applyEvent, detectedCrop, detectedDisease, sessionId, history)

// Render messages:
<div className="space-y-3 max-h-96 overflow-y-auto">
  {messages.map((msg, i) => (
    <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ${
        msg.role === "user" ? "bg-[#1a5632] text-white" : "bg-gray-100 text-gray-800"
      }`}>
        {msg.content}
      </div>
    </div>
  ))}
</div>
```

### Phase 3: API Client Update

**File: `frontend/src/lib/api.ts`**
```tsx
export async function streamQuestion(
  query: string,
  onEvent: (e: AgentStageEvent) => void,
  crop?: string | null,
  disease?: string | null,
  sessionId?: string | null,
  history?: Array<{role: string; content: string}>,
): Promise<QAResponse> {
  const res = await fetch(`${API_BASE}/api/qa/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, crop, disease, session_id: sessionId, history }),
  });
  // ... rest unchanged
}
```

## Execution Order

1. Create `session_store.py`
2. Update `QARequest` schema
3. Update `generator.py` build_prompt to include history
4. Update `qa.py` endpoints to use session store
5. Update `api.ts` streamQuestion signature
6. Rewrite `qa-panel.tsx` with chat bubbles + history state
7. Test: two-turn conversation (ask treatment → ask dosage → verify context)

## Verification

**Test 1: Follow-up resolution**
```
User: আলুর দেরি ব্লাইটের প্রতিকার কি?
Assistant: [explains treatment with dosage]
User: মাত্রা কত?
Assistant: [refers back to previous answer] ✅
```

**Test 2: Session isolation**
```
Session A: asks about potato
Session B: asks about rice
No cross-contamination ✅
```

**Test 3: TTL eviction**
```
Wait 30 minutes → new session created ✅
```

## Files to Create/Modify

| File | Action |
|---|---|
| `backend/app/services/advisory/session_store.py` | Create |
| `backend/app/models/schema.py` | Modify (add history field) |
| `backend/app/services/advisory/generator.py` | Modify (history in prompt) |
| `backend/app/api/qa.py` | Modify (session integration) |
| `frontend/src/lib/api.ts` | Modify (new params) |
| `frontend/src/components/qa-panel.tsx` | Rewrite (chat UI) |
| `backend/scripts/test_multi_turn.py` | Create (test) |
