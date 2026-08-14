import { createBrowserClient } from "@supabase/ssr";

/**
 * Browser Supabase client (client components, event handlers).
 * Falls back to `document.cookie` storage — no cookie methods needed.
 * Create once per component render (cached by React), not per event.
 */
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
  );
}
