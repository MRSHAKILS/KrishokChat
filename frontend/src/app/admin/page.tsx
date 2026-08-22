"use client";

/* =========================================================================
   /admin — ops overview (amendment 02): safety metrics, user totals by plan,
   live announcements, recent admin actions. Every number comes from a real
   endpoint; unconfigured surfaces show honest empty states, never placeholders.
   ========================================================================= */

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { Activity, Users, Megaphone, ShieldAlert, Loader2, BadgeCheck, ArrowRight } from "lucide-react";
import { getSafetyMetrics, type SafetyMetrics } from "@/lib/api";
import {
  adminListActions,
  adminListAnnouncements,
  adminListUsers,
  type AdminActionRow,
  type AdminAnnouncement,
  type AdminProfileRow,
} from "@/lib/admin-api";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { bn } from "@/lib/bn";

function bnNum(n: number | undefined | null): string {
  return bn(Number(n ?? 0));
}

function StatCard({
  icon: Icon,
  label,
  value,
  hint,
  tone = "leaf",
}: {
  icon: typeof Activity;
  label: string;
  value: string;
  hint?: string;
  tone?: "leaf" | "ochre" | "clay";
}) {
  const toneClass =
    tone === "clay" ? "bg-clay/10 text-clay" : tone === "ochre" ? "bg-ochre/10 text-ochre" : "bg-leaf/10 text-leaf";
  return (
    <div className="rounded-xl border rule bg-paper p-5">
      <div className="flex items-center gap-2.5">
        <span className={`flex h-9 w-9 items-center justify-center rounded-lg ${toneClass}`}>
          <Icon className="h-4.5 w-4.5" aria-hidden />
        </span>
        <span className="text-sm text-ink-soft">{label}</span>
      </div>
      <div className="mt-3 font-display text-3xl tabular text-ink">{value}</div>
      {hint && <div className="mt-1 text-xs text-ink-faint">{hint}</div>}
    </div>
  );
}

export default function AdminOverviewPage() {
  const { session } = useSupabaseSession();
  const token = session?.access_token;

  const [metrics, setMetrics] = useState<SafetyMetrics | null>(null);
  const [users, setUsers] = useState<AdminProfileRow[] | null>(null);
  const [announcements, setAnnouncements] = useState<AdminAnnouncement[] | null>(null);
  const [actions, setActions] = useState<AdminActionRow[] | null>(null);
  const [failed, setFailed] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!token) return;
    setFailed(null);
    getSafetyMetrics()
      .then(setMetrics)
      .catch(() => setMetrics(null));
    try {
      const [usersRes, annRes, actRes] = await Promise.all([
        adminListUsers(token, 1, 100),
        adminListAnnouncements(token, 20),
        adminListActions(token, 10),
      ]);
      setUsers(usersRes.items);
      setAnnouncements(annRes.items);
      setActions(actRes.items);
    } catch (err) {
      setFailed(err instanceof Error ? err.message : "লোড করা যায়নি");
    }
  }, [token]);

  useEffect(() => {
    void load();
  }, [load]);

  if (!token) {
    return (
      <div className="rounded-xl border rule bg-paper p-8 text-center text-sm text-ink-soft">
        অ্যাডমিন হিসেবে লগইন করুন।
      </div>
    );
  }

  const totalUsers = users?.length ?? 0;
  const premiumCount = users?.filter((u) => u.plan === "premium").length ?? 0;
  const adminCount = users?.filter((u) => u.role === "admin").length ?? 0;
  const liveCount = announcements?.filter((a) => a.published).length ?? 0;

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-display text-2xl text-ink">ওভারভিউ</h1>
        <p className="mt-1 text-sm text-ink-soft">
          নিরাপত্তা মেট্রিক্স, ব্যবহারকারী ও সক্রিয় বিজ্ঞপ্তি — সবই লাইভ ডেটা থেকে।
        </p>
      </header>

      {failed && (
        <div role="alert" className="rounded-lg bg-clay/10 px-4 py-3 text-sm text-clay">
          {failed} — ব্যাকএন্ড ও Supabase কনফিগ চালু আছে কিনা দেখুন।
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={Activity}
          label="মোট প্রশ্ন (অডিট)"
          value={metrics ? bnNum(metrics.total_queries) : "—"}
          hint={metrics ? `পাইপলাইন v2 · ${bnNum(metrics.by_category?.safe_agri ?? 0)} নিরাপদ` : "অডিট লগ পাওয়া যায়নি"}
        />
        <StatCard
          icon={ShieldAlert}
          label="প্রত্যাখ্যান হার"
          value={metrics?.router?.refusal_rate != null ? `${bnPercentSafe(metrics.router.refusal_rate)}` : "—"}
          hint="সেফটি রাউটার অনুযায়ী"
          tone="clay"
        />
        <StatCard
          icon={Users}
          label="ব্যবহারকারী"
          value={users ? bnNum(totalUsers) : "—"}
          hint={users ? `${bnNum(premiumCount)} প্রিমিয়াম · ${bnNum(adminCount)} অ্যাডমিন` : undefined}
        />
        <StatCard
          icon={Megaphone}
          label="সক্রিয় বিজ্ঞপ্তি"
          value={announcements ? bnNum(liveCount) : "—"}
          hint={announcements ? `মোট ${bnNum(announcements.length)}টির মধ্যে` : undefined}
          tone="ochre"
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Recent admin actions */}
        <section className="rounded-xl border rule bg-paper p-5">
          <h2 className="font-display text-lg text-ink">সাম্প্রতিক অ্যাডমিন কার্যক্রম</h2>
          {actions === null ? (
            <div className="flex h-24 items-center justify-center">
              <Loader2 className="h-5 w-5 animate-spin text-leaf" />
            </div>
          ) : actions.length === 0 ? (
            <p className="mt-3 text-sm text-ink-faint">এখনো কোনো অ্যাডমিন কার্যক্রম নেই।</p>
          ) : (
            <ul className="mt-3 space-y-2.5">
              {actions.map((a) => (
                <li key={a.id} className="flex items-start justify-between gap-3 border-b rule pb-2.5 last:border-b-0">
                  <div className="min-w-0">
                    <span className="text-sm font-medium text-ink">{actionLabelBn(a.action)}</span>
                    <span className="ml-2 text-xs text-ink-faint">
                      {a.target_type === "profile" ? "ব্যবহারকারী" : "বিজ্ঞপ্তি"} · {a.target_id.slice(0, 8)}…
                    </span>
                    <div className="mt-0.5 text-xs text-ink-faint">
                      {new Date(a.created_at).toLocaleString("bn-BD")}
                    </div>
                  </div>
                  {Object.keys(a.payload ?? {}).length > 0 && (
                    <code className="shrink-0 rounded bg-paper-2/60 px-1.5 py-0.5 text-xs text-ink-soft">
                      {JSON.stringify(a.payload)}
                    </code>
                  )}
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Live announcements quick list */}
        <section className="rounded-xl border rule bg-paper p-5">
          <div className="flex items-center justify-between">
            <h2 className="font-display text-lg text-ink">বিজ্ঞপ্তি</h2>
            <Link href="/admin/announcements" className="inline-flex items-center gap-1 text-sm font-medium text-leaf hover:underline">
              সব দেখুন <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
          {announcements === null ? (
            <div className="flex h-24 items-center justify-center">
              <Loader2 className="h-5 w-5 animate-spin text-leaf" />
            </div>
          ) : announcements.length === 0 ? (
            <p className="mt-3 text-sm text-ink-faint">কোনো বিজ্ঞপ্তি নেই — ঘোষণা ও সতর্কতা বিভাগ থেকে তৈরি করুন।</p>
          ) : (
            <ul className="mt-3 space-y-2.5">
              {announcements.slice(0, 6).map((a) => (
                <li key={a.id} className="flex items-center justify-between gap-3 border-b rule pb-2.5 last:border-b-0">
                  <div className="min-w-0">
                    <div className="flex items-center gap-1.5">
                      <span className="truncate text-sm font-medium text-ink">{a.title_bn}</span>
                      {a.published && <BadgeCheck className="h-3.5 w-3.5 shrink-0 text-leaf" aria-label="প্রকাশিত" />}
                    </div>
                    <div className="mt-0.5 text-xs text-ink-faint">
                      {kindLabelBn(a.kind)} · {audienceLabelBn(a.audience)}
                      {a.crop ? ` · ${a.crop}` : ""}
                    </div>
                  </div>
                  <span
                    className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${
                      a.severity === "urgent"
                        ? "bg-clay/10 text-clay"
                        : a.severity === "warning"
                          ? "bg-ochre/10 text-ochre"
                          : "bg-leaf/10 text-leaf"
                    }`}
                  >
                    {severityLabelBn(a.severity)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}

function bnPercentSafe(rate: number): string {
  // bnPercent exists in lib/bn for this; keep a tiny fallback here if the value is a fraction.
  const pct = rate <= 1 ? rate * 100 : rate;
  return `${bn(Math.round(pct))}%`;
}

export function actionLabelBn(action: string): string {
  if (action === "update_user") return "ব্যবহারকারী পরিবর্তন";
  if (action === "create_announcement") return "বিজ্ঞপ্তি তৈরি";
  return action;
}

export function kindLabelBn(kind: string): string {
  if (kind === "disease_alert") return "রোগ সতর্কতা";
  if (kind === "maintenance") return "রক্ষণাবেক্ষণ";
  return "ঘোষণা";
}

export function severityLabelBn(severity: string): string {
  if (severity === "urgent") return "জরুরি";
  if (severity === "warning") return "সতর্ক";
  return "তথ্য";
}

export function audienceLabelBn(audience: string): string {
  if (audience === "free") return "ফ্রি ব্যবহারকারী";
  if (audience === "premium") return "প্রিমিয়াম";
  return "সবাই";
}
