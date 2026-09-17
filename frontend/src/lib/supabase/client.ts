import { createBrowserClient } from "@supabase/ssr";

/**
 * Browser Supabase client (client components, event handlers).
 * Falls back to `document.cookie` storage — no cookie methods needed.
 * Create once per component render (cached by React), not per event.
 */
export function createClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL || "https://placeholder.supabase.co";
  const key = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY || "placeholder-key";
  return createBrowserClient(url, key);
}
