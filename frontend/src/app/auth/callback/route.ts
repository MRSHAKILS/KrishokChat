import { NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

/**
 * PKCE callback route: Supabase redirects here after email confirmation or
 * OAuth. Exchanges the authorization `code` for a session (cookies are set on
 * the response via the server client), then redirects to the allowlisted
 * `next` target. `/auth` is the default landing page.
 */
export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/auth";

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      const forwardedHost = request.headers.get("x-forwarded-host");
      const isLocalEnv = process.env.NODE_ENV === "development";
      const base =
        isLocalEnv && forwardedHost ? `http://${forwardedHost}` : origin;
      // open-redirect guard: relative paths only, reject protocol-relative "//"
      const safeNext =
        next.startsWith("/") && !next.startsWith("//") ? next : "/auth";
      return NextResponse.redirect(`${base}${safeNext}`);
    }
  }

  // code missing or exchange failed — back to /auth with an error marker
  return NextResponse.redirect(`${origin}/auth?error=auth_callback_failed`);
}
