"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { Shield, TrendingUp, AlertTriangle, CheckCircle2, Activity } from "lucide-react";
import { getSafetyMetrics, type SafetyMetrics } from "@/lib/api";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";

/* =========================================================================
   Analytics Page — enhanced safety metrics dashboard.
   Live data from /api/safety/metrics + research benchmark context.
   ========================================================================= */

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<SafetyMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSafetyMetrics()
      .then(setMetrics)
      .catch(() => setMetrics({ total_queries: 0, by_category: {}, flagged_count: 0, recent: [] }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="h-8 w-48 animate-pulse rounded bg-bone" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-28 animate-pulse rounded-xl bg-bone" />
          ))}
        </div>
      </div>
    );
  }

  const data: SafetyMetrics = metrics ?? { total_queries: 0, by_category: {}, flagged_count: 0, recent: [] };
  const safe = data.by_category?.safe_agri ?? 0;
  const total = data.total_queries || 0;
  const blocked = total - safe;
  const safePct = total > 0 ? Math.round((safe / total) * 100) : 0;

  // Sort categories by count
  const categories = Object.entries(data.by_category || {})
    .filter(([key]) => key !== "unknown")
    .sort(([, a], [, b]) => b - a)
    .slice(0, 8);

  const maxCat = categories.length > 0 ? Math.max(...categories.map(([, v]) => v)) : 1;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="font-display text-3xl text-ink">পরিসংখ্যান</h1>
        <p className="mt-1 text-sm text-ink-soft">
          নিরাপত্তা যাচাই ও প্রশ্নের বিশ্লেষণ — স্থানীয় অডিট লগ থেকে।
        </p>
      </div>

      {/* Stat cards */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone lg:grid-cols-4"
      >
        <StatCard variants={enter} icon={Activity} value={total} label="মোট প্রশ্ন" tone="ink" />
        <StatCard variants={enter} icon={CheckCircle2} value={safe} label="নিরাপদ কৃষি" tone="leaf" />
        <StatCard variants={enter} icon={AlertTriangle} value={blocked} label="অবরুদ্ধ" tone="clay" />
        <StatCard variants={enter} icon={Shield} value={`${safePct}%`} label="নিরাপদ হার" tone="leaf" />
      </motion.section>

      {/* Donut + category breakdown */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Safe vs Blocked donut */}
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
          className="rounded-xl border rule bg-paper p-6"
        >
          <motion.h2 variants={enter} className="mb-4 font-display text-lg text-ink">
            নিরাপদ vs অবরুদ্ধ
          </motion.h2>
          <motion.div variants={enter} className="flex items-center gap-6">
            {/* CSS donut */}
            <div className="relative h-32 w-32 shrink-0">
              <div
                className="h-full w-full rounded-full"
                style={{
                  background: `conic-gradient(var(--color-leaf) ${safePct * 3.6}deg, var(--color-clay-soft) 0deg)`,
                }}
              />
              <div className="absolute inset-3 flex flex-col items-center justify-center rounded-full bg-paper">
                <span className="font-display text-2xl tabular text-ink">{safePct}%</span>
                <span className="text-[10px] text-ink-faint">নিরাপদ</span>
              </div>
            </div>
            {/* Legend */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-leaf" />
                <span className="text-sm text-ink">নিরাপদ: {safe}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-clay-soft" />
                <span className="text-sm text-ink">অবরুদ্ধ: {blocked}</span>
              </div>
              <div className="pt-1 text-xs text-ink-faint">
                মোট: {total} প্রশ্ন
              </div>
            </div>
          </motion.div>
        </motion.section>

        {/* Category breakdown bars */}
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
          className="rounded-xl border rule bg-paper p-6"
        >
          <motion.h2 variants={enter} className="mb-4 font-display text-lg text-ink">
            শ্রেণী অনুযায়ী প্রশ্ন
          </motion.h2>
          {categories.length === 0 ? (
            <motion.p variants={enter} className="text-sm text-ink-faint">
              কোনো তথ্য নেই।
            </motion.p>
          ) : (
            <motion.div variants={enter} className="space-y-2.5">
              {categories.map(([cat, count], i) => {
                const isSafe = cat === "safe_agri";
                const pct = Math.round((count / maxCat) * 100);
                return (
                  <div key={cat} className="flex items-center gap-3">
                    <div className="w-28 shrink-0 truncate font-mono text-[11px] text-ink-soft">
                      {cat}
                    </div>
                    <div className="relative h-6 flex-1 overflow-hidden rounded-md bg-bone">
                      <motion.div
                        className={`absolute inset-y-0 left-0 rounded-md ${isSafe ? "bg-leaf" : "bg-clay"}`}
                        initial={{ width: 0 }}
                        whileInView={{ width: `${pct}%` }}
                        viewport={{ once: true }}
                        transition={{ delay: i * 0.08, duration: dur.slow, ease: ease.smooth }}
                      />
                      <span className="relative flex items-center px-2 text-xs font-medium tabular text-ink">
                        {count}
                      </span>
                    </div>
                  </div>
                );
              })}
            </motion.div>
          )}
        </motion.section>
      </div>

      {/* Research context strip */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
        className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4"
      >
        {[
          { value: RESEARCH_STATS.safetyCategories, label: "নিরাপত্তা শ্রেণী" },
          { value: RESEARCH_STATS.hallucinationFloor, label: "হ্যালুসিনেশন ফ্লোর" },
          { value: RESEARCH_STATS.fieldInterviews, label: "মাঠ সাক্ষাৎকার" },
          { value: RESEARCH_STATS.interAnnotatorKappa, label: "নির্দেশক κ" },
        ].map((stat) => (
          <motion.div key={stat.label} variants={enter} className="bg-paper-2/30 px-4 py-4 text-center">
            <div className="font-display text-lg tabular text-ochre">{stat.value}</div>
            <div className="mt-1 text-[10px] uppercase tracking-[0.1em] text-ink-faint">
              {stat.label}
            </div>
          </motion.div>
        ))}
      </motion.section>

      {/* Recent queries */}
      {data.recent && data.recent.length > 0 && (
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
          className="rounded-xl border rule bg-paper"
        >
          <motion.div variants={enter} className="flex items-center justify-between border-b rule px-5 py-4">
            <h2 className="font-display text-lg text-ink">সাম্প্রতিক প্রশ্ন</h2>
            <TrendingUp className="h-4 w-4 text-ink-faint" />
          </motion.div>
          <motion.ul variants={enter} className="divide-y divide-bone">
            {data.recent.slice(0, 12).map((r, i) => {
              const isBlocked = r.category !== "safe_agri";
              return (
                <li key={i} className="flex items-center justify-between gap-4 px-5 py-3">
                  <div className="flex min-w-0 items-center gap-3">
                    <div className={`h-2 w-2 shrink-0 rounded-full ${isBlocked ? "bg-clay" : "bg-leaf"}`} />
                    <span className="truncate text-sm text-ink-soft">{r.query || "(খালি)"}</span>
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    <span className="text-[10px] text-ink-faint tabular">
                      {r.timestamp ? new Date(r.timestamp).toLocaleTimeString("bn-BD", { hour: "2-digit", minute: "2-digit" }) : ""}
                    </span>
                    <span
                      className={`rounded-md px-2 py-0.5 text-[10px] font-medium ${
                        isBlocked ? "bg-clay-soft/40 text-clay" : "bg-leaf/10 text-leaf"
                      }`}
                    >
                      {r.category}
                    </span>
                  </div>
                </li>
              );
            })}
          </motion.ul>
        </motion.section>
      )}

      {/* Link to safety design */}
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
        className="rounded-xl border rule bg-paper-2/30 p-5 text-center"
      >
        <motion.p variants={enter} className="text-sm text-ink-soft">
          নিরাপত্তা ডিজাইন কীভাবে কাজ করে দেখুন —
        </motion.p>
        <motion.a
          variants={enter}
          href="/research/safety"
          className="mt-2 inline-block rounded-lg border rule px-5 py-2 text-sm font-medium text-leaf transition-colors hover:border-leaf"
        >
          নিরাপত্তা নকশা দেখুন →
        </motion.a>
      </motion.div>
    </div>
  );
}

/* === Stat card === */
function StatCard({
  value,
  label,
  tone,
  icon: Icon,
  variants,
}: {
  value: number | string;
  label: string;
  tone: "leaf" | "ink" | "clay";
  icon: React.ComponentType<{ className?: string }>;
  variants: typeof enter;
}) {
  const color = tone === "leaf" ? "text-leaf" : tone === "clay" ? "text-clay" : "text-ink";
  return (
    <motion.div variants={variants} className="bg-paper p-5">
      <Icon className={`h-5 w-5 ${color}`} />
      <div className={`mt-3 font-display text-3xl tabular ${color}`}>{value}</div>
      <div className="mt-1 text-xs text-ink-soft">{label}</div>
    </motion.div>
  );
}
