import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

/**
 * Session refresh at the request edge (Next 16 `proxy.ts`).
 *
 * Refreshes the Supabase session cookie when one exists and is close to
 * expiry, and applies the cache-control headers the library requires when
 * auth cookies are set. NEVER gates routes — anonymous visitors pass through
 * untouched (anonymous-first rule, AGENTS.md §2 rule 1). Future route gating,
 * if any, must target only user-data surfaces.
 *
 * IMPORTANT: do not run code between createServerClient and getUser().
 */
export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet, headers) {
          // write to the request so the upstream render sees the session
          cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
          supabaseResponse = NextResponse.next({ request });
          // write to the response so the browser stores refreshed tokens
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options),
          );
          // @supabase/ssr requires these on any response that sets auth cookies
          Object.entries(headers).forEach(([key, value]) =>
            supabaseResponse.headers.set(key, value),
          );
        },
      },
    },
  );

  // Network-verified session check (refreshes tokens when needed).
  const {
    data: { user },
  } = await supabase.auth.getUser();

  // P1: refresh only, no gating. The user object is read so token refresh
  // happens; anonymous requests simply carry no session.
  void user;

  // Probe hook for verifying proxy execution in dev/verification:
  // PROXY_PROBE=true <start command> adds an x-proxy-ran response header.
  if (process.env.PROXY_PROBE === "true") {
    supabaseResponse.headers.set("x-proxy-ran", "1");
  }

  return supabaseResponse;
}
