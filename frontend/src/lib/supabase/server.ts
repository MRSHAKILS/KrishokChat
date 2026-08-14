import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

/**
 * Server Supabase client for Server Components, Route Handlers and Server Actions.
 * Always create a NEW client per request — never share across requests.
 *
 * `setAll` may throw in Server Components (cookies can only be set from
 * Route Handlers / Server Actions); the proxy (`src/proxy.ts`) handles session
 * refresh for those cases via `updateSession`.
 */
export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options),
            );
          } catch {
            // Called from a Server Component; ignore — proxy refreshes sessions.
          }
        },
      },
    },
  );
}
