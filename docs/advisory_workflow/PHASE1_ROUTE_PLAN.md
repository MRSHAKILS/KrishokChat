# Phase 1: Route Structure & Shared Layouts — Plan

## Objective
Restructure the Next.js app to industry-standard production layout with proper route groups, shared layouts, and loading/error/not-found states. This is the foundation for all future pages and deployment.

## Current State
- Single `app/page.tsx` with tab-based navigation
- Basic navbar component (not integrated into layout)
- No loading/error/not-found states
- No route groups or shared layouts
- Components are functional but not organized for scale

## Proposed Structure
```
frontend/src/app/
├── layout.tsx                  ← root (fonts, metadata, providers)
├── page.tsx                    ← landing/hero page (redirects to /detect)
├── loading.tsx                 ← global skeleton loader
├── error.tsx                   ← global error boundary
├── not-found.tsx               ← custom 404 page
├── globals.css                 ← global styles (already exists)
│
├── (app)/                      ← route group for main app (no URL prefix)
│   ├── layout.tsx              ← shared app layout (navbar + footer + children)
│   ├── detect/
│   │   └── page.tsx            ← disease detection page
│   ├── chat/
│   │   └── page.tsx            ← QA chat page
│   └── analytics/
│       └── page.tsx            ← safety metrics dashboard
│
├── (marketing)/                ← route group for public pages
│   ├── layout.tsx              ← marketing layout (simple, no auth)
│   ├── page.tsx                ← landing/hero page
│   ├── about/
│   │   └── page.tsx            ← about project page
│   └── contact/
│       └── page.tsx            ← contact/credits page
│
└── api/
    └── health/
        └── route.ts            ← health check endpoint
```

## Key Design Decisions

### Route Groups `(app)` and `(marketing)`
- `(app)` groups all authenticated/main app pages — shared layout with navbar + footer
- `(marketing)` groups public pages — simpler layout, no app chrome
- Parentheses mean no URL prefix: `(app)/detect` → `/detect`

### Shared Layouts
- **Root layout**: fonts, metadata, global providers, Toaster
- **App layout**: navbar + footer + children (for detect/chat/analytics)
- **Marketing layout**: minimal header + footer (for landing/about/contact)

### Loading States
- `app/loading.tsx` — global skeleton (animated)
- Each route can have its own `loading.tsx` for page-specific skeletons

### Error Handling
- `app/error.tsx` — global error boundary with retry button
- Each route can have its own `error.tsx`

### Not Found
- `app/not-found.tsx` — custom 404 with link back to home

## File-by-File Execution Plan

### Step 1: Create route group directories
```
mkdir app/\(app\)/detect
mkdir app/\(app\)/chat
mkdir app/\(app\)/analytics
mkdir app/\(marketing\)/about
mkdir app/\(marketing\)/contact
mkdir app/api/health
```

### Step 2: Create root states
- `app/loading.tsx` — animated skeleton
- `app/error.tsx` — error boundary with retry
- `app/not-found.tsx` — custom 404

### Step 3: Create shared layouts
- `app/(app)/layout.tsx` — navbar + footer + children
- `app/(marketing)/layout.tsx` — minimal header + footer

### Step 4: Create page routes
- `app/(app)/detect/page.tsx` — detection page
- `app/(app)/chat/page.tsx` — chat page
- `app/(app)/analytics/page.tsx` — analytics page
- `app/(marketing)/page.tsx` — landing page
- `app/(marketing)/about/page.tsx` — about page
- `app/(marketing)/contact/page.tsx` — contact page

### Step 5: Create API route
- `app/api/health/route.ts` — health check

### Step 6: Move existing components
- Move `DetectPanel` usage to detect page
- Move `QAPanel` usage to chat page
- Keep components in `components/` (they're reusable)

### Step 7: Update root page
- `app/page.tsx` → redirect to `/detect` or show landing

### Step 8: Create footer component
- `components/layout/footer.tsx` — proper footer with links

### Step 9: Update navbar
- Integrate with new layout
- Add active route highlighting
- Add mobile menu

### Step 10: Test all routes
- Verify each route loads
- Verify loading states
- Verify error states
- Verify 404

## Component Organization

### New Components to Create
| Component | Location | Purpose |
|---|---|---|
| Footer | `components/layout/footer.tsx` | App footer with links |
| PageHeader | `components/layout/page-header.tsx` | Consistent page headers |
| FeatureCard | `components/shared/feature-card.tsx` | Landing page features |
| StatCard | `components/shared/stat-card.tsx` | Analytics stats |
| EmptyState | `components/shared/empty-state.tsx` | Empty state placeholder |

### Existing Components to Keep
| Component | Location | Purpose |
|---|---|---|
| Navbar | `components/navbar.tsx` | Top navigation |
| DetectPanel | `components/detect-panel.tsx` | Detection UI |
| QAPanel | `components/qa-panel.tsx` | Chat UI |
| AgentTrace | `components/agent-trace.tsx` | Pipeline visualization |

## Styling Approach

### Loading Skeleton
```tsx
export default function Loading() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-8 bg-gray-200 rounded w-1/3" />
      <div className="h-64 bg-gray-200 rounded" />
    </div>
  );
}
```

### Error Boundary
```tsx
"use client";
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="text-center py-12">
      <h2>কিছু একটা ঠিক নেই</h2>
      <p>{error.message}</p>
      <button onClick={reset}>আবার চেষ্টা করুন</button>
    </div>
  );
}
```

### Not Found
```tsx
export default function NotFound() {
  return (
    <div className="text-center py-12">
      <h2>৪০৪ — পাতা পাওয়া যায়নি</h2>
      <Link href="/detect">হোমে ফিরে যান</Link>
    </div>
  );
}
```

## Verification Checklist

- [ ] All routes load without errors
- [ ] Loading states show on slow pages
- [ ] Error boundary catches errors
- [ ] 404 page shows for unknown routes
- [ ] Navbar shows active route
- [ ] Footer appears on all app pages
- [ ] Mobile responsive
- [ ] Bengali text renders correctly
- [ ] TypeScript compiles
- [ ] Build passes

## Post-Phase Next Steps
- Phase 2: Custom hooks (useChat, useDetect, useSession)
- Phase 3: Constants + Types centralization
- Phase 4: Landing page redesign with hero + features
- Phase 5: Analytics page with real data
- Phase 6: Middleware (logging, rate limiting)
- Phase 7: About/Contact pages
- Phase 8: SEO + metadata + Open Graph
- Phase 9: Accessibility audit
- Phase 10: Performance optimization
