import type { NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/update-session";

/**
 * Next.js 16 renamed `middleware.ts` -> `proxy.ts` (export named `proxy`,
 * Node.js runtime by default). Runs before matching routes are served.
 *
 * Scope: session refresh only (see updateSession). Matcher is deliberately
 * narrow: app tool routes + auth surfaces. `/api/*` is excluded — those are
 * rewrites to the FastAPI backend and must not incur proxy overhead.
 */
export async function proxy(request: NextRequest) {
  return await updateSession(request);
}

export const config = {
  matcher: ["/chat/:path*", "/detect/:path*", "/soil/:path*", "/analytics/:path*", "/auth/:path*"],
};
