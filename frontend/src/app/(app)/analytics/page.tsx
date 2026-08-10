"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { Shield, TrendingUp, AlertTriangle, CheckCircle2, Activity, Download, Filter } from "lucide-react";
import { getSafetyMetrics, type SafetyMetrics } from "@/lib/api";
import { RESEARCH_STATS } from "@/lib/constants";
import { bn } from "@/lib/bn";
import { safetyLabel, TONE_BADGE, TONE_DOT, TONE_BAR } from "@/lib/safety-labels";
import { enter, stagger, dur, ease } from "@/lib/motion";

/* =========================================================================
   Analytics Page — enhanced safety metrics dashboard.
   Live data from /api/safety/metrics + research benchmark context.
   ========================================================================= */

function formatQueryForAnalyticsDisplay(rawQuery?: string | null): string {
  if (!rawQuery || !rawQuery.trim() || rawQuery === "(খালি)") {
    return "📷 চিত্রভিত্তিক রোগ নির্ণয় ও বালাই বিশ্লেষণ স্ক্যান";
  }
  let q = rawQuery;
  q = q.replace(/Corn[_\s]*Northern[_\s]*Leaf[_\s]*Blight/gi, "ভুট্টা — উত্তরীয় পাতা পোড়া (Northern Leaf Blight)");
  q = q.replace(/আলুর\s*দেরি\s*ব্লাইট/g, "আলুর লেট ব্লাইট (নাবি ধসা)");
  q = q.replace(/paraquat/gi, "প্যারাকোয়াট (Paraquat — নিষিদ্ধ রাসায়নিক)");
  return q;
}

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<SafetyMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "safe" | "blocked">("all");

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
  const blocked = Math.max(0, total - safe);
  const safePct = total > 0 ? Math.round((safe / total) * 100) : 0;

  // Sort categories by count
  const categories = Object.entries(data.by_category || {})
    .filter(([key]) => key !== "unknown")
    .sort(([, a], [, b]) => b - a)
    .slice(0, 8);

  const maxCat = categories.length > 0 ? Math.max(...categories.map(([, v]) => v)) : 1;
  const recent = (data.recent ?? []).filter((item) => {
    if (filter === "safe") return item.category === "safe_agri";
    if (filter === "blocked") return item.category !== "safe_agri";
    return true;
  });

  const exportAudit = () => {
    const blob = new Blob([JSON.stringify({ exported_at: new Date().toISOString(), ...data }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "krishokchat-safety-audit.json";
    link.click();
    URL.revokeObjectURL(url);
  };

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
        <StatCard variants={enter} icon={Activity} value={bn(total)} label="মোট প্রশ্ন" tone="ink" />
        <StatCard variants={enter} icon={CheckCircle2} value={bn(safe)} label="নিরাপদ কৃষি" tone="leaf" />
        <StatCard variants={enter} icon={AlertTriangle} value={bn(blocked)} label="অবরুদ্ধ" tone="clay" />
        <StatCard variants={enter} icon={Shield} value={`${bn(safePct)}%`} label="নিরাপদ হার" tone="leaf" />
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
                <span className="font-display text-2xl tabular text-ink">{bn(safePct)}%</span>
                <span className="text-[10px] text-ink-faint">নিরাপদ</span>
              </div>
            </div>
            {/* Legend */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-leaf" />
                <span className="text-sm text-ink">নিরাপদ: {bn(safe)}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-clay-soft" />
                <span className="text-sm text-ink">অবরুদ্ধ: {bn(blocked)}</span>
              </div>
              <div className="pt-1 text-xs text-ink-faint">
                মোট: {bn(total)} প্রশ্ন
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
                const categoryLabel = safetyLabel(cat);
                const pct = Math.round((count / maxCat) * 100);
                return (
                  <div key={cat} className="flex items-center gap-3">
                    <div className="w-36 shrink-0 truncate">
                      <span className={`inline-flex max-w-full items-center gap-1.5 truncate rounded-md px-2 py-1 text-[11px] font-medium ${TONE_BADGE[categoryLabel.tone]}`} title={categoryLabel.label}>
                        <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${TONE_DOT[categoryLabel.tone]}`} />
                        <span className="truncate">{categoryLabel.label}</span>
                      </span>
                    </div>
                    <div className="relative h-6 flex-1 overflow-hidden rounded-md bg-bone">
                      <motion.div
                        className={`absolute inset-y-0 left-0 rounded-md ${TONE_BAR[categoryLabel.tone]}`}
                        initial={{ width: 0 }}
                        whileInView={{ width: `${pct}%` }}
                        viewport={{ once: true }}
                        transition={{ delay: i * 0.08, duration: dur.slow, ease: ease.smooth }}
                      />
                      <span className="relative flex items-center px-2 text-xs font-medium tabular text-ink">
                        {bn(count)}
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
            <div className="mt-1 text-[10px] font-medium text-ink-faint">
              {stat.label}
            </div>
          </motion.div>
        ))}
      </motion.section>

      {/* Local audit controls — no external telemetry; export stays on the
          evaluator's device and uses the already-loaded local audit data. */}
      <div className="flex flex-col gap-3 rounded-xl border rule bg-paper px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2 text-sm text-ink-soft">
          <Filter className="h-4 w-4 text-leaf" />
          <span>অডিট লগ দেখান</span>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as "all" | "safe" | "blocked")}
            className="rounded-md border rule bg-paper-2/40 px-2 py-1.5 text-xs text-ink focus:border-leaf focus:outline-none"
            aria-label="অডিট লগ ফিল্টার"
          >
            <option value="all">সব সিদ্ধান্ত</option>
            <option value="safe">শুধু নিরাপদ</option>
            <option value="blocked">শুধু আটকানো</option>
          </select>
        </div>
        <button type="button" onClick={exportAudit} className="inline-flex min-h-10 items-center justify-center gap-2 rounded-md border rule px-3 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf">
          <Download className="h-3.5 w-3.5" /> অডিট JSON ডাউনলোড
        </button>
      </div>

      {/* Recent queries */}
      {recent.length > 0 && (
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
          className="rounded-xl border rule bg-paper"
        >
          <motion.div variants={enter} className="flex items-center justify-between border-b rule px-5 py-4">
            <h2 className="font-display text-lg text-ink">সাম্প্রতিক প্রশ্ন ও স্ক্যান অডিট</h2>
            <TrendingUp className="h-4 w-4 text-ink-faint" />
          </motion.div>
          <motion.ul variants={enter} className="divide-y divide-bone">
            {recent.slice(0, 12).map((r, i) => {
              const isBlocked = r.category !== "safe_agri" && r.category !== "vision_advisory";
              const categoryLabel = safetyLabel(r.category);
              const displayQuery = formatQueryForAnalyticsDisplay(r.query);
              return (
                <li key={i} className="flex items-center justify-between gap-4 px-5 py-3">
                  <div className="flex min-w-0 items-center gap-3">
                    <div className={`h-2 w-2 shrink-0 rounded-full ${isBlocked ? "bg-clay" : "bg-leaf"}`} />
                    <span className="truncate text-sm text-ink-soft">{displayQuery}</span>
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
                      {categoryLabel.label}
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
