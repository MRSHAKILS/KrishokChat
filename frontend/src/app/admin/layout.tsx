import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { createClient } from "@/lib/supabase/server";
import { AdminShell } from "@/components/admin/admin-shell";

/* =========================================================================
   /admin layout — the ONLY route-level guard (amendment 02).

   Fail-closed: no session, backend unreachable, or role != admin all render
   the standard Bengali 404 (no redirect, no information leak). Every admin
   API the pages call re-verifies the role server-side regardless — this
   guard is cosmetic; the backend is the enforcement.
   ========================================================================= */

export const dynamic = "force-dynamic";

export default async function AdminLayout({ children }: { children: ReactNode }) {
  const supabase = await createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  let isAdmin = false;
  if (session?.access_token) {
    try {
      const backend = process.env.BACKEND_URL ?? "http://localhost:8000";
      const res = await fetch(`${backend}/api/account`, {
        headers: { Authorization: `Bearer ${session.access_token}` },
        cache: "no-store",
      });
      if (res.ok) {
        const body = (await res.json()) as { role?: string };
        isAdmin = body.role === "admin";
      }
    } catch {
      isAdmin = false;
    }
  }

  if (!isAdmin) notFound();

  return <AdminShell>{children}</AdminShell>;
}
