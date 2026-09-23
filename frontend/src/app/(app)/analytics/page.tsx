"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { Shield, TrendingUp, AlertTriangle, CheckCircle2, Activity, Download, Filter, RefreshCw, Search, ShieldCheck } from "lucide-react";
import { getSafetyMetrics, type SafetyMetrics } from "@/lib/api";
import { RESEARCH_STATS } from "@/lib/constants";
import { statLocale, numLocale } from "@/lib/bn";
import { toLocaleCount, useCountUp } from "@/lib/use-count-up";
import { safetyLabel, TONE_BADGE, TONE_DOT, TONE_BAR_SOFT, refusalRuleLabel } from "@/lib/safety-labels";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   Analytics Page — enhanced safety metrics dashboard.
   Live data from /api/safety/metrics + research benchmark context.
   ========================================================================= */

function formatQueryForAnalyticsDisplay(rawQuery: string | null | undefined, en: boolean): string {
  if (!rawQuery || !rawQuery.trim() || rawQuery === "(খালি)") {
    return en ? "📷 Image-based disease diagnosis and pest analysis scan" : "📷 চিত্রভিত্তিক রোগ নির্ণয় ও বালাই বিশ্লেষণ স্ক্যান";
  }
  let q = rawQuery;
  q = q.replace(/Corn[_\s]*Northern[_\s]*Leaf[_\s]*Blight/gi, en ? "Corn — Northern Leaf Blight" : "ভুট্টা — উত্তরীয় পাতা পোড়া (Northern Leaf Blight)");
  q = q.replace(/আলুর\s*দেরি\s*ব্লাইট/g, en ? "Potato late blight" : "আলুর লেট ব্লাইট (নাবি ধসা)");
  q = q.replace(/paraquat/gi, en ? "Paraquat (banned chemical)" : "প্যারাকোয়াট (Paraquat — নিষিদ্ধ রাসায়নিক)");
  return q;
}

export default function AnalyticsPage() {
  const { locale } = useLanguage();
  const en = locale === "en";
  const [metrics, setMetrics] = useState<SafetyMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState<"all" | "safe" | "blocked">("all");

  useEffect(() => {
    getSafetyMetrics()
      .then(setMetrics)
      .catch(() => setMetrics({ total_queries: 0, by_category: {}, flagged_count: 0, recent: [] }))
      .finally(() => setLoading(false));
  }, []);

  /* Manual refresh: during a live demo the audit log grows as questions are
     asked, so a visible refresh re-counts the stats (and re-plays the
     count-up animations via the key remount below). */
  const refresh = () => {
    setRefreshing(true);
    getSafetyMetrics()
      .then(setMetrics)
      .catch(() => {})
      .finally(() => setRefreshing(false));
  };

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

  /* Two-segment donut: safe vs blocked, drawn from the top (SVG arc animation).
     Blocked uses the light terracotta tint (clay-soft) over a bone track ring so
     the chart stays airy — the alarm color lives in badges, not in large fills. */
  const donutSegments = [
    { name: "safe", frac: safePct / 100, rot: -90, color: "var(--color-leaf)" },
    { name: "blocked", frac: total > 0 ? 1 - safePct / 100 : 1, rot: -90 + (safePct / 100) * 360, color: "var(--color-clay-soft)" },
  ];
  const recent = (data.recent ?? []).filter((item) => {
    if (filter === "safe") return item.category === "safe_agri";
    if (filter === "blocked") return item.category !== "safe_agri";
    return true;
  });

  /* Pipeline stats (dual-view) — aggregated from the same logged decisions
     the chat stepper renders; null means "no evidence yet", shown as —. */
  const verifier = data.verifier;
  const verifierChecked = verifier?.checked ?? 0;
  const verifierGrounded = verifier?.grounded ?? 0;
  const verifierUnsupported = verifier?.unsupported ?? 0;
  const verifierPassPct = verifier?.pass_rate == null ? null : Math.round(verifier.pass_rate * 100);
  const routerBlocked = data.router?.blocked ?? 0;
  const routerRefusalPct = data.router?.refusal_rate == null ? null : Math.round(data.router.refusal_rate * 100);
  const retrievalHitPct = data.retrieval?.hit_rate == null ? null : Math.round(data.retrieval.hit_rate * 100);
  const avgTop1 = data.retrieval?.avg_top1_score == null ? "—" : data.retrieval.avg_top1_score.toFixed(2);
  const avgSources = data.retrieval?.avg_sources == null ? "—" : numLocale(Math.round(data.retrieval.avg_sources), en);

  const exportAudit = () => {
    const blob = new Blob([JSON.stringify({ exported_at: new Date().toISOString(), ...data }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `krishokchat-safety-audit-${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const exportAuditCSV = () => {
    const headers = ["Timestamp", "Query", "Category", "Classification", "Router Status", "Retrieval Hit", "Verifier Passed"];
    const rows = (data.recent ?? []).map((r) => [
      r.timestamp ? `"${new Date(r.timestamp).toLocaleString("en-US")}"` : `""`,
      `"${(r.query || "").replace(/"/g, '""')}"`,
      `"${r.category || ""}"`,
      `"${r.category === "safe_agri" || r.category === "vision_advisory" ? "SAFE" : "BLOCKED"}"`,
      `"${r.action === "refuse" || (r.category !== "safe_agri" && r.category !== "vision_advisory") ? "BLOCKED" : "PASSED"}"`,
      `"${r.retrieval_hit ? "HIT" : "MISS"}"`,
      `"${r.verifier_passed == null ? "N/A" : r.verifier_passed ? "PASSED" : "FAILED"}"`,
    ]);

    const csvContent = "\uFEFF" + [headers.join(","), ...rows.map((row) => row.join(","))].join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `krishokchat-safety-audit-${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
        <div>
          <h1 className="font-display text-3xl text-ink">{en ? "Analytics" : "পরিসংখ্যান"}</h1>
          <p className="mt-1 text-sm text-ink-soft">
            {en ? "Safety verification and query analysis — from the local audit log." : "নিরাপত্তা যাচাই ও প্রশ্নের বিশ্লেষণ — স্থানীয় অডিট লগ থেকে।"}
          </p>
        </div>
        <button
          type="button"
          onClick={refresh}
          disabled={refreshing}
          className="inline-flex min-h-10 items-center justify-center gap-2 self-start rounded-lg border rule bg-paper px-4 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf disabled:cursor-not-allowed disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? "animate-spin" : ""}`} />
          {refreshing ? (en ? "Refreshing…" : "রিফ্রেশ হচ্ছে…") : (en ? "Refresh" : "রিফ্রেশ")}
        </button>
      </div>

      {/* Stat cards — key remount replays the count-up on refresh */}
      <motion.section
        key={`stats-${total}`}
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone lg:grid-cols-4"
      >
        <StatCard variants={enter} icon={Activity} value={total} label={en ? "Total queries" : "মোট প্রশ্ন"} tone="ink" en={en} />
        <StatCard variants={enter} icon={CheckCircle2} value={safe} label={en ? "Safe agri" : "নিরাপদ কৃষি"} tone="leaf" en={en} />
        <StatCard variants={enter} icon={AlertTriangle} value={blocked} label={en ? "Blocked" : "অবরুদ্ধ"} tone="clay" en={en} />
        <StatCard variants={enter} icon={Shield} value={safePct} suffix="%" label={en ? "Safe rate" : "নিরাপদ হার"} tone="leaf" en={en} />
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
            {en ? "Safe vs. Blocked" : "নিরাপদ vs অবরুদ্ধ"}
          </motion.h2>
          <motion.div variants={enter} className="flex items-center gap-6">
            {/* Animated SVG donut — light track ring, arcs draw from the top */}
            <div key={`donut-${total}`} className="relative h-36 w-36 shrink-0">
              <svg viewBox="0 0 240 240" className="h-full w-full">
                <circle cx={120} cy={120} r={92} fill="none" stroke="var(--color-bone)" strokeWidth={30} />
                {donutSegments.map((s, i) => (
                  <motion.circle
                    key={s.name}
                    cx={120}
                    cy={120}
                    r={92}
                    fill="none"
                    stroke={s.color}
                    strokeWidth={26}
                    pathLength={1}
                    strokeDasharray={`${Math.max(s.frac - 0.006, 0)} ${1 - Math.max(s.frac - 0.006, 0)}`}
                    transform={`rotate(${s.rot} 120 120)`}
                    initial={{ opacity: 0, pathLength: 0 }}
                    animate={{ opacity: 1, pathLength: Math.max(s.frac - 0.006, 0) }}
                    transition={{ delay: 0.15 + i * 0.15, duration: dur.slow, ease: ease.smooth }}
                  />
                ))}
                <text x={120} y={118} textAnchor="middle" className="fill-ink font-display" fontSize={34}>
                  {numLocale(safePct, en)}
                </text>
                <text x={120} y={142} textAnchor="middle" className="fill-ink-soft" fontSize={12}>
                  {en ? "% safe" : "% নিরাপদ"}
                </text>
              </svg>
            </div>
            {/* Legend */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-leaf" />
                <span className="text-sm text-ink">{en ? "Safe: " : "নিরাপদ: "}<span className="font-semibold tabular">{numLocale(safe, en)}</span></span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full border border-clay/40 bg-clay-soft" />
                <span className="text-sm text-ink">{en ? "Blocked: " : "অবরুদ্ধ: "}<span className="font-semibold tabular">{numLocale(blocked, en)}</span></span>
              </div>
              <div className="pt-1 text-xs text-ink-faint">
                {en ? `Total: ${numLocale(total, en)} queries` : `মোট: ${numLocale(total, en)} প্রশ্ন`}
              </div>
            </div>
          </motion.div>
        </motion.section>

        {/* Category breakdown bars — label row + light track; the count sits
            OUTSIDE the fill so it is never dark-on-dark. Fills use soft tones
            per group: safe=leaf, uncertain=ochre, stopped=light terracotta,
            off-topic=neutral — color signals the group, not alarm level. */}
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
          className="rounded-xl border rule bg-paper p-6"
        >
          <motion.h2 variants={enter} className="mb-4 font-display text-lg text-ink">
            {en ? "Questions by Category" : "শ্রেণী অনুযায়ী প্রশ্ন"}
          </motion.h2>
          {categories.length === 0 ? (
            <motion.p variants={enter} className="text-sm text-ink-faint">
              {en ? "No data yet." : "কোনো তথ্য নেই।"}
            </motion.p>
          ) : (
            <motion.div variants={enter} key={`cats-${total}`} className="space-y-3.5">
              {categories.map(([cat, count], i) => {
                const categoryLabel = safetyLabel(cat);
                const pct = Math.round((count / maxCat) * 100);
                const share = total > 0 ? Math.round((count / total) * 100) : 0;
                return (
                  <div key={cat}>
                    <div className="mb-1 flex items-center justify-between gap-2">
                      <span className={`inline-flex min-w-0 items-center gap-1.5 rounded-md px-1.5 py-0.5 text-xs font-medium ${TONE_BADGE[categoryLabel.tone]}`} title={en ? categoryLabel.labelEn : categoryLabel.label}>
                        <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${TONE_DOT[categoryLabel.tone]}`} />
                        <span className="truncate">{en ? categoryLabel.labelEn : categoryLabel.label}</span>
                      </span>
                      <span className="shrink-0 text-xs tabular text-ink-soft">
                        <span className="font-display text-sm font-semibold text-ink">{numLocale(count, en)}</span>
                        <span className="ml-1 text-ink-faint">({numLocale(share, en)}%)</span>
                      </span>
                    </div>
                    <div className="h-2.5 overflow-hidden rounded-full bg-paper-2">
                      <motion.div
                        className={`h-full rounded-full ${TONE_BAR_SOFT[categoryLabel.tone]}`}
                        initial={{ width: 0 }}
                        whileInView={{ width: `${Math.max(pct, 3)}%` }}
                        viewport={{ once: true }}
                        transition={{ delay: i * 0.07, duration: dur.slow, ease: ease.smooth }}
                      />
                    </div>
                  </div>
                );
              })}
            </motion.div>
          )}
        </motion.section>
      </div>

      {/* Pipeline stats — dual-view: these are the same decisions the chat
          stepper animates live, aggregated from the local audit log. */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
        className="rounded-xl border rule bg-paper p-6"
      >
        <motion.div variants={enter} className="mb-1 flex items-center gap-2">
          <h2 className="font-display text-lg text-ink">{en ? "Pipeline Statistics" : "পাইপলাইন পরিসংখ্যান"}</h2>
          <span className="rounded-md bg-leaf/10 px-2 py-0.5 text-xs font-medium text-leaf">{en ? "Live stepper data" : "লাইভ স্টেপার ডেটা"}</span>
        </motion.div>
        <motion.p variants={enter} className="mb-5 text-xs text-ink-faint">
          {en ? "Aggregated stats behind the decisions each stage's animation shows in chat." : "চ্যাটে প্রতিটি ধাপের অ্যানিমেশন যে সিদ্ধান্ত দেখায়, এখানে তারই জমা পরিসংখ্যান।"}
        </motion.p>
        <motion.div variants={enter} className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <StageStat
            icon={Shield}
            name={en ? "Safety Router" : "নিরাপত্তা রাউটার"}
            detail={en ? `${numLocale(routerBlocked, en)} queries blocked` : `${numLocale(routerBlocked, en)} টি প্রশ্ন আটকানো`}
            pct={routerRefusalPct}
            pctLabel={en ? "Refusal rate" : "অস্বীকৃতি হার"}
            tone="clay"
            en={en}
          />
          <StageStat
            icon={Search}
            name={en ? "Source Retrieval" : "উৎস অনুসন্ধান"}
            detail={en ? `Avg top score ${avgTop1} · avg ${avgSources} sources` : `গড় শীর্ষ স্কোর ${avgTop1} · গড় ${avgSources} উৎস`}
            pct={retrievalHitPct}
            pctLabel={en ? "Source hit rate" : "উৎস হিট হার"}
            tone="ochre"
            en={en}
          />
          <StageStat
            icon={ShieldCheck}
            name={en ? "Answer Verification" : "উত্তর যাচাই"}
            detail={en ? `${numLocale(verifierGrounded, en)} / ${numLocale(verifierChecked, en)} claims grounded · ${numLocale(verifierUnsupported, en)} unsupported` : `${numLocale(verifierGrounded, en)} / ${numLocale(verifierChecked, en)} দাবি ভিত্তিক · ${numLocale(verifierUnsupported, en)} অপোষিত`}
            pct={verifierPassPct}
            pctLabel={en ? "Verification pass rate" : "যাচাই পাস হার"}
            tone="leaf"
            en={en}
          />
        </motion.div>

        {/* P5: refusal reasons — why blocked queries were blocked (D1a gate
            visibility). Rendered only when the log has rule evidence. */}
        {(() => {
          const rules = Object.entries(data.router?.refusal_rules ?? {})
            .filter(([, count]) => count > 0)
            .sort(([, a], [, b]) => b - a);
          if (rules.length === 0) return null;
          return (
            <motion.div variants={enter} className="mt-4 flex flex-wrap items-center gap-1.5">
              <span className="text-xs text-ink-faint">{en ? "Refusal reasons:" : "অস্বীকৃতির কারণ:"}</span>
              {rules.map(([rule, count]) => (
                <span
                  key={rule}
                  className="inline-flex items-center gap-1 rounded-full bg-clay-soft/15 px-2.5 py-1 text-xs font-medium text-clay ring-1 ring-clay-soft/40"
                >
                  {refusalRuleLabel(rule, en)}
                  <span className="tabular text-clay-soft">{numLocale(count, en)}</span>
                </span>
              ))}
            </motion.div>
          );
        })()}
      </motion.section>

      {/* Research context strip */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
        className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4"
      >
        {[
          { value: RESEARCH_STATS.safetyCategories, label: "নিরাপত্তা শ্রেণী", labelEn: "Safety categories" },
          { value: RESEARCH_STATS.hallucinationFloor, label: "হ্যালুসিনেশন ফ্লোর", labelEn: "Hallucination floor" },
          { value: RESEARCH_STATS.fieldInterviews, label: "মাঠ সাক্ষাৎকার", labelEn: "Field interviews" },
          { value: RESEARCH_STATS.interAnnotatorKappa, label: "নির্দেশক κ", labelEn: "Annotator κ" },
        ].map((stat) => (
          <motion.div key={stat.label} variants={enter} className="bg-paper-2/30 px-4 py-4 text-center">
            <div className="font-display text-lg tabular text-ochre">{statLocale(stat.value, en)}</div>
            <div className="mt-1 text-xs font-medium text-ink-faint">
              {en ? stat.labelEn : stat.label}
            </div>
          </motion.div>
        ))}
      </motion.section>

      {/* Local audit controls — no external telemetry; export stays on the
          evaluator's device and uses the already-loaded local audit data. */}
      <div className="flex flex-col gap-3 rounded-xl border rule bg-paper px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2 text-sm text-ink-soft">
          <Filter className="h-4 w-4 text-leaf" />
          <span>{en ? "Show audit log" : "অডিট লগ দেখান"}</span>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as "all" | "safe" | "blocked")}
            className="rounded-md border rule bg-paper-2/40 px-2 py-1.5 text-xs text-ink focus:border-leaf focus:outline-none"
            aria-label={en ? "Audit log filter" : "অডিট লগ ফিল্টার"}
          >
            <option value="all">{en ? "All decisions" : "সব সিদ্ধান্ত"}</option>
            <option value="safe">{en ? "Safe only" : "শুধু নিরাপদ"}</option>
            <option value="blocked">{en ? "Blocked only" : "শুধু আটকানো"}</option>
          </select>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={exportAuditCSV}
            className="inline-flex min-h-10 items-center justify-center gap-1.5 rounded-md border rule bg-paper px-3 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf cursor-pointer"
          >
            <Download className="h-3.5 w-3.5 text-leaf" />
            {en ? "Export CSV" : "CSV এক্সপোর্ট"}
          </button>
          <button
            type="button"
            onClick={exportAudit}
            className="inline-flex min-h-10 items-center justify-center gap-1.5 rounded-md border rule bg-paper px-3 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf cursor-pointer"
          >
            <Download className="h-3.5 w-3.5 text-ochre" />
            {en ? "Export JSON" : "JSON এক্সপোর্ট"}
          </button>
        </div>
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
            <h2 className="font-display text-lg text-ink">{en ? "Recent Queries & Scan Audit" : "সাম্প্রতিক প্রশ্ন ও স্ক্যান অডিট"}</h2>
            <TrendingUp className="h-4 w-4 text-ink-faint" />
          </motion.div>
          <motion.ul variants={enter} className="divide-y divide-bone">
            {recent.slice(0, 12).map((r, i) => {
              const isBlocked = r.category !== "safe_agri" && r.category !== "vision_advisory";
              const categoryLabel = safetyLabel(r.category);
              const displayQuery = formatQueryForAnalyticsDisplay(r.query, en);
              return (
                <li key={i} className="flex items-center justify-between gap-4 px-5 py-3">
                  <div className="flex min-w-0 items-center gap-3">
                    <div className={`h-2 w-2 shrink-0 rounded-full ${isBlocked ? "bg-clay" : "bg-leaf"}`} />
                    <span className="truncate text-sm text-ink-soft">{displayQuery}</span>
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    {/* Per-step validity dots — router · retrieval · verifier */}
                    <span className="flex items-center gap-1" title={en ? "Steps: Router → Source → Verify" : "ধাপ: রাউটার → উৎস → যাচাই"}>
                      <span className={`h-1.5 w-1.5 rounded-full ${isBlocked ? "bg-clay" : "bg-leaf"}`} title={en ? "Safety Router" : "নিরাপত্তা রাউটার"} />
                      <span className={`h-1.5 w-1.5 rounded-full ${r.retrieval_hit === false ? "bg-clay-soft" : "bg-leaf"}`} title={en ? "Source Retrieval" : "উৎস অনুসন্ধান"} />
                      <span
                        className={`h-1.5 w-1.5 rounded-full ${
                          r.verifier_passed == null ? "bg-bone" : r.verifier_passed ? "bg-leaf" : "bg-clay"
                        }`}
                        title={en ? "Answer Verification" : "উত্তর যাচাই"}
                      />
                    </span>
                    <span className="text-xs text-ink-faint tabular">
                      {r.timestamp ? new Date(r.timestamp).toLocaleTimeString(en ? "en-US" : "bn-BD", { hour: "2-digit", minute: "2-digit" }) : ""}
                    </span>
                    <span
                      className={`rounded-md px-2 py-0.5 text-xs font-medium ${
                        isBlocked ? "bg-clay-soft/40 text-clay" : "bg-leaf/10 text-leaf"
                      }`}
                    >
                      {en ? categoryLabel.labelEn : categoryLabel.label}
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
          {en ? "See how the safety design works —" : "নিরাপত্তা ডিজাইন কীভাবে কাজ করে দেখুন —"}
        </motion.p>
        <motion.a
          variants={enter}
          href="/research/safety"
          className="mt-2 inline-block rounded-lg border rule px-5 py-2 text-sm font-medium text-leaf transition-colors hover:border-leaf"
        >
          {en ? "See the safety design →" : "নিরাপত্তা নকশা দেখুন →"}
        </motion.a>
      </motion.div>
    </div>
  );
}

/* === Pipeline stage stat — progress-bar card. The numeral stays ink-on-paper
   (always legible); the tone color lives only in the small icon + bar fill. === */
function StageStat({
  icon: Icon,
  name,
  detail,
  pct,
  pctLabel,
  tone,
  en,
}: {
  icon: React.ComponentType<{ className?: string }>;
  name: string;
  detail: string;
  pct: number | null;
  pctLabel: string;
  tone: "leaf" | "ochre" | "clay";
  en: boolean;
}) {
  const color = tone === "leaf" ? "text-leaf" : tone === "clay" ? "text-clay" : "text-ochre";
  const barFill = tone === "leaf" ? "bg-leaf/80" : tone === "clay" ? "bg-clay-soft" : "bg-ochre/70";
  const n = useCountUp(pct ?? 0, true);
  return (
    <div className="rounded-xl border rule bg-paper p-5">
      <div className="flex items-center justify-between gap-2">
        <span className="flex items-center gap-2 text-sm font-medium text-ink">
          <Icon className={`h-4 w-4 ${color}`} />
          {name}
        </span>
        <span className="shrink-0 text-xs text-ink-faint">{pctLabel}</span>
      </div>
      <div className="mt-2.5 font-display text-3xl tabular text-ink">
        {pct == null ? "—" : (
          <>
            {toLocaleCount(n, en)}
            <span className="text-xl text-ink-soft">%</span>
          </>
        )}
      </div>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-paper-2">
        {pct != null && (
          <motion.div
            className={`h-full rounded-full ${barFill}`}
            initial={{ width: 0 }}
            whileInView={{ width: `${Math.max(Math.min(pct, 100), 3)}%` }}
            viewport={{ once: true }}
            transition={{ duration: dur.slow, ease: ease.smooth }}
          />
        )}
      </div>
      <div className="mt-2 text-xs text-ink-soft">{detail}</div>
    </div>
  );
}

/* === Stat card === */
function StatCard({  value,
  suffix,
  label,
  tone,
  icon: Icon,
  variants,
  en,
}: {
  value: number;
  suffix?: string;
  label: string;
  tone: "leaf" | "ink" | "clay";
  icon: React.ComponentType<{ className?: string }>;
  variants: typeof enter;
  en: boolean;
}) {
  const color = tone === "leaf" ? "text-leaf" : tone === "clay" ? "text-clay" : "text-ink";
  const n = useCountUp(value, true);
  return (
    <motion.div variants={variants} className="bg-paper p-5">
      <Icon className={`h-5 w-5 ${color}`} />
      <div className="mt-3 font-display text-3xl tabular text-ink">
        {toLocaleCount(n, en)}
        {suffix ? <span className="text-xl text-ink-soft">{suffix}</span> : null}
      </div>
      <div className="mt-1 text-xs text-ink-soft">{label}</div>
    </motion.div>
  );
}
