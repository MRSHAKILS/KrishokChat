# KrishokChat Frontend Workflow Checklist

Use this file after a session ends. Work through the checklist from top to bottom.

## Main product workflow

```text
Photo → Disease classification → Grounded advisory → Sources → Follow-up question
```

The frontend must stay honest about the backend:

- The current vision models perform **classification**, not bounding-box detection.
- Do not invent boxes, localization, dosage, weather data, or confidence values.
- Disease treatment advice must remain grounded in the backend QA/retrieval/verifier path.

## Completed in the current frontend pass

- [x] Added image type and file-size validation.
- [x] Added client-side image resizing/compression for large photos.
- [x] Revoke old preview object URLs to avoid memory leaks.
- [x] Added request timeout and cancellation for chat and disease requests.
- [x] Prevent duplicate chat submissions.
- [x] Prevent stale detection requests from overwriting newer state.
- [x] Display streamed assistant tokens while the answer is being generated.
- [x] Added cancel buttons for chat and disease analysis.
- [x] Added retry actions for failed chat and disease requests.
- [x] Added a simple offline indicator on the disease page.
- [x] Added basic chat persistence in localStorage.
- [x] Restructured the treatment card into:
  - [x] Immediate action
  - [x] Chemical dosage, only when present in the advisory text
  - [x] Safety warning
  - [x] Weather limitation notice
  - [x] Confidence/verifier status
  - [x] Sources
  - [x] Follow-up actions
- [x] Added follow-up chips that return the farmer to the chat composer.
- [x] Preserved 48px-class touch targets for important mobile actions.
- [x] Added keyboard access to the image intake zone.

## Next work: do these one by one

### 1. Test the complete workflow manually

- [ ] Start the backend and frontend.
- [ ] Open `/detect` on a 360px-wide viewport.
- [ ] Upload a valid JPEG, PNG, and WebP image.
- [ ] Try an invalid file type.
- [ ] Try an image larger than the configured limit.
- [ ] Select a crop manually and run detection.
- [ ] Run detection without selecting a crop.
- [ ] Cancel detection while it is loading.
- [ ] Retry after stopping the backend.
- [ ] Confirm that a diagnosis displays sources and verifier status.
- [ ] Tap each follow-up chip and confirm the question appears in chat.

### 2. Test low-network behavior

- [ ] Use Chrome DevTools Slow 3G.
- [ ] Confirm the loading state remains understandable.
- [ ] Confirm a timed-out request can be retried.
- [ ] Turn the network offline before submitting.
- [ ] Confirm the offline message is visible and no request is sent.
- [ ] Restore the network and retry.

### 3. Test mobile usability

- [ ] Test at 360px width.
- [ ] Test one-handed use with the primary action near the thumb zone.
- [ ] Confirm no horizontal scrolling.
- [ ] Confirm Bengali text does not clip or overlap.
- [ ] Confirm textarea, microphone, send, cancel, retry, and follow-up controls are easy to tap.
- [ ] Test with browser text size increased.
- [ ] Test with `prefers-reduced-motion` enabled.

### 4. Add automated frontend tests

- [ ] Add a Playwright test for upload → detection result.
- [ ] Add a Playwright test for detection failure → retry.
- [ ] Add a Playwright test for chat streaming and cancellation.
- [ ] Add a Playwright test for follow-up chip → prefilled chat question.
- [ ] Add a test proving duplicate clicks create only one request.
- [ ] Add a test proving an old detection response cannot replace a newer image result.

### 5. Improve persistence carefully

- [x] Persist the latest scan result separately from chat history. (2026-08-11: `krishokchat:latest-scan:v1` key, lazy useState init, no image bytes stored.)
- [x] Do not store large original images in localStorage. (Stores only the JSON result + crop hint, not the image.)
- [ ] Use a small thumbnail or IndexedDB if previous-image continuation is required.
- [x] Restore crop and disease context after refresh. (Restored from the same scan key on mount.)
- [ ] Expire old local data instead of accumulating unlimited sessions.

### 6. Add farmer context only after the backend contract is ready

The current QA schema has crop and disease, but no location. Do not add fake location behavior.

- [ ] Add a reviewed `location`/`district` field to the backend QA contract.
- [ ] Pass district context through `/api/qa` and `/api/qa/stream`.
- [ ] Persist the farmer's selected district locally.
- [ ] Add weather information only when a real, documented backend source exists.
- [ ] Show a clear “weather unavailable” state when it is not available.

### 7. Keep the advisory contract structured

When backend work is scheduled, prefer this response shape instead of parsing long text in React:

```ts
type AdvisoryData = {
  immediate_action: string[];
  dosage: string | null;
  safety_warning: string[];
  weather_consideration: string | null;
  sources: SourceNode[];
};
```

- [ ] Add the backend schema.
- [ ] Populate fields only from grounded retrieval/generation output.
- [ ] Add verifier tests for Bengali numerals and chemical units.
- [ ] Update the frontend to render fields directly.
- [ ] Keep the old text field temporarily for compatibility.

## Files changed in the current pass

- `frontend/src/app/(app)/detect/page.tsx`
- `frontend/src/components/detect/intake-zone.tsx`
- `frontend/src/components/detect/treatment-card.tsx`
- `frontend/src/components/qa-panel.tsx`
- `frontend/src/components/chat/chat-message.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/image.ts`

## Files changed in the persistence pass (2026-08-11)

- `frontend/src/app/(app)/detect/page.tsx` — lazy useState init from `krishokchat:latest-scan:v1`, persist result + crop hint on change, clear function.
- `frontend/src/components/detect/diagnosis-card.tsx` — added `onClear` prop + dismiss button on the diagnosed card.

## Verification commands

Run from `frontend/`:

```bash
pnpm exec tsc --noEmit
pnpm exec eslint "src/lib/api.ts" "src/lib/image.ts" "src/app/(app)/detect/page.tsx" "src/components/qa-panel.tsx" "src/components/chat/chat-message.tsx" "src/components/detect/intake-zone.tsx" "src/components/detect/treatment-card.tsx"
pnpm build
```

Run from the repository root:

```bash
git status --short
```

## Important scope rule

Do not add a global state library, upload queue, service worker, offline sync system, or new
backend service until the simple workflow above is tested on a real Android device.
