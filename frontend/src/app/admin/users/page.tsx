"use client";

/* =========================================================================
   /admin/users — plan & role management (amendment 02). Paginated table with
   search; every change requires an explicit confirm step and is audited
   server-side to admin_actions. Nothing here gates any user feature (no
   gating per researcher decision) — these are labels today.
   ========================================================================= */

import { useCallback, useEffect, useState } from "react";
import { Loader2, Search, ChevronLeft, ChevronRight, BadgeCheck } from "lucide-react";
import { adminListUsers, adminPatchUser, type AdminProfileRow } from "@/lib/admin-api";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { cn } from "@/lib/utils";
import { bn } from "@/lib/bn";

const PAGE_SIZE = 20;

export default function AdminUsersPage() {
  const { session } = useSupabaseSession();
  const token = session?.access_token;

  const [rows, setRows] = useState<AdminProfileRow[] | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState<string | null>(null);
  const [confirming, setConfirming] = useState<{ row: AdminProfileRow; changes: { plan?: "free" | "premium"; role?: "user" | "admin" } } | null>(null);

  const load = useCallback(
    async (p: number, q: string) => {
      if (!token) return;
      try {
        setError(null);
        const res = await adminListUsers(token, p, PAGE_SIZE, q);
        setRows(res.items);
        setTotal(res.total);
      } catch (err) {
        setError(err instanceof Error ? err.message : "লোড করা যায়নি");
        setRows([]);
      }
    },
    [token],
  );

  useEffect(() => {
    void load(page, search);
  }, [load, page, search]);

  async function applyChange(row: AdminProfileRow, changes: { plan?: "free" | "premium"; role?: "user" | "admin" }) {
    if (!token) return;
    setPending(row.id);
    try {
      const updated = await adminPatchUser(token, row.id, changes);
      setRows((prev) => prev?.map((r) => (r.id === updated.id ? updated : r)) ?? null);
      setConfirming(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "পরিবর্তন করা যায়নি");
    } finally {
      setPending(null);
    }
  }

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <div className="space-y-5">
      <header className="flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
        <div>
          <h1 className="font-display text-2xl text-ink">ব্যবহারকারী</h1>
          <p className="mt-1 text-sm text-ink-soft">
            প্ল্যান ও ভূমিকা লেবেল — এখন কোনো ফিচার আটকে নেই; পরিবর্তনগুলো অডিট লগে সংরক্ষিত হয়।
          </p>
        </div>
        <div className="relative w-full sm:w-72">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" />
          <input
            type="search"
            value={search}
            onChange={(e) => {
              setPage(1);
              setSearch(e.target.value);
            }}
            placeholder="ইমেইল খুঁজুন…"
            className="w-full rounded-lg border rule bg-paper py-2 pl-9 pr-3 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
          />
        </div>
      </header>

      {error && (
        <div role="alert" className="rounded-lg bg-clay/10 px-4 py-3 text-sm text-clay">
          {error}
        </div>
      )}

      <div className="overflow-x-auto rounded-xl border rule bg-paper scrollbar-thin">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b rule text-xs text-ink-faint">
              <th className="px-4 py-3 font-medium">ব্যবহারকারী</th>
              <th className="px-4 py-3 font-medium">প্ল্যান</th>
              <th className="px-4 py-3 font-medium">ভূমিকা</th>
              <th className="px-4 py-3 font-medium">যোগদান</th>
            </tr>
          </thead>
          <tbody>
            {rows === null ? (
              <tr>
                <td colSpan={4} className="px-4 py-10 text-center">
                  <Loader2 className="mx-auto h-5 w-5 animate-spin text-leaf" />
                </td>
              </tr>
            ) : rows.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-10 text-center text-ink-faint">
                  {search ? "এই খোঁজে কেউ মেলেনি।" : "এখনো কোনো নিবন্ধিত ব্যবহারকারী নেই।"}
                </td>
              </tr>
            ) : (
              rows.map((row) => (
                <tr key={row.id} className="border-b rule last:border-b-0">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <span className="max-w-52 truncate font-medium text-ink">{row.email || row.id.slice(0, 8)}</span>
                      {row.role === "admin" && (
                        <BadgeCheck className="h-4 w-4 shrink-0 text-leaf" aria-label="অ্যাডমিন" />
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <PlanSelect
                      value={row.plan}
                      disabled={pending === row.id}
                      onChange={(plan) => setConfirming({ row, changes: { plan } })}
                    />
                  </td>
                  <td className="px-4 py-3">
                    <RoleSelect
                      value={row.role}
                      disabled={pending === row.id}
                      onChange={(role) => setConfirming({ row, changes: { role } })}
                    />
                  </td>
                  <td className="px-4 py-3 text-xs text-ink-faint">
                    {row.created_at ? new Date(row.created_at).toLocaleDateString("bn-BD") : "—"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between text-sm text-ink-soft">
        <span>
          মোট {bn(total)} জন · পাতা {bn(page)}/{bn(totalPages)}
        </span>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page <= 1}
            className="flex h-9 items-center gap-1 rounded-lg border rule px-3 text-ink-soft transition-colors hover:border-leaf disabled:opacity-40"
          >
            <ChevronLeft className="h-4 w-4" /> আগের
          </button>
          <button
            type="button"
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page >= totalPages}
            className="flex h-9 items-center gap-1 rounded-lg border rule px-3 text-ink-soft transition-colors hover:border-leaf disabled:opacity-40"
          >
            পরের <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Confirm dialog */}
      {confirming && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/30 p-4">
          <div role="alertdialog" aria-modal className="w-full max-w-md rounded-2xl border rule bg-paper p-6 shadow-xl">
            <h2 className="font-display text-lg text-ink">পরিবর্তন নিশ্চিত করুন</h2>
            <p className="mt-2 text-sm leading-relaxed text-ink-soft">
              <span className="font-medium text-ink">{confirming.row.email || confirming.row.id.slice(0, 8)}</span> —{" "}
              {confirming.changes.plan
                ? `প্ল্যান: ${confirming.row.plan === "free" ? "ফ্রি" : "প্রিমিয়াম"} → ${confirming.changes.plan === "free" ? "ফ্রি" : "প্রিমিয়াম"}`
                : `ভূমিকা: ${confirming.row.role === "user" ? "সাধারণ" : "অ্যাডমিন"} → ${confirming.changes.role === "user" ? "সাধারণ ব্যবহারকারী" : "অ্যাডমিন"}`}
            </p>
            <p className="mt-2 text-xs text-ink-faint">এই কাজটি অ্যাডমিন অডিট লগে লেখা হবে।</p>
            <div className="mt-5 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setConfirming(null)}
                className="rounded-lg border rule px-4 py-2 text-sm text-ink-soft hover:border-leaf"
              >
                বাতিল
              </button>
              <button
                type="button"
                onClick={() => void applyChange(confirming.row, confirming.changes)}
                disabled={pending === confirming.row.id}
                className="flex items-center gap-2 rounded-lg bg-leaf px-4 py-2 text-sm font-semibold text-paper hover:bg-leaf-2 disabled:opacity-60"
              >
                {pending === confirming.row.id && <Loader2 className="h-4 w-4 animate-spin" />}
                নিশ্চিত করুন
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const selectClass =
  "rounded-lg border rule bg-paper-2/40 px-2.5 py-1.5 text-sm text-ink focus:border-leaf focus:outline-none disabled:opacity-50 cursor-pointer";

function PlanSelect({
  value,
  onChange,
  disabled,
}: {
  value: "free" | "premium";
  onChange: (plan: "free" | "premium") => void;
  disabled?: boolean;
}) {
  return (
    <select
      value={value}
      disabled={disabled}
      onChange={(e) => onChange(e.target.value as "free" | "premium")}
      className={cn(selectClass, value === "premium" && "border-ochre/40 bg-ochre/10 font-semibold text-ochre")}
      aria-label="প্ল্যান"
    >
      <option value="free">ফ্রি</option>
      <option value="premium">প্রিমিয়াম</option>
    </select>
  );
}

function RoleSelect({
  value,
  onChange,
  disabled,
}: {
  value: "user" | "admin";
  onChange: (role: "user" | "admin") => void;
  disabled?: boolean;
}) {
  return (
    <select
      value={value}
      disabled={disabled}
      onChange={(e) => onChange(e.target.value as "user" | "admin")}
      className={cn(selectClass, value === "admin" && "border-leaf/40 bg-leaf/10 font-semibold text-leaf")}
      aria-label="ভূমিকা"
    >
      <option value="user">সাধারণ</option>
      <option value="admin">অ্যাডমিন</option>
    </select>
  );
}
