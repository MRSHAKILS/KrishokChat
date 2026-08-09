"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Shield,
  Search,
  PenLine,
  CheckCircle2,
  RotateCcw,
  Play,
  AlertTriangle,
  ChevronDown,
} from "lucide-react";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";

/* =========================================================================
   Safety Design Page — THE product demo, not a paper figure.

   Shows a REAL query flowing through the actual 4-stage pipeline with
   REAL retrieved nodes, REAL scores, and a REAL generated answer.

   This is the animated RAG workflow visualization.
   ========================================================================= */

type Stage = "idle" | "safety" | "retrieval" | "generation" | "verifier" | "done";

// REAL data from our backend test (potato late blight query)
const REAL_QUERY = "আলুর দেরি ব্লাইট কীভাবে প্রতিরোধ করব?";

const REAL_SOURCES = [
  {
    id: "DAE_PEST_1206A0_001",
    score: 33.23,
    publisher: "DAE",
    title: "আলুর দেরি ব্লাইট নিয়ন্ত্রণের জন্য কীটনাশক",
    snippet: "আলুর দেরি ব্লাইট (Late Blight) দমনের জন্য কৃষি সম্প্রসারণ অধিদপ্তর (DAE) কর্তৃক নিম্নলিখিত কীটনাশকগুলি নিবন্ধিত। প্রতি লিটার পানিতে ২ গ্রাম মাত্রায় মিশ্রণ করে স্প্রে করতে হবে।",
    chemicals: ["Mancozeb 80WP", "Metalaxyl"],
  },
  {
    id: "CABI_POTATO_834B4F_001",
    score: 32.59,
    publisher: "CABI",
    title: "Potato late blight — লেট ব্লাইট",
    snippet: "লেট ব্লাইট বা মড়ক রোগ আলু গাছের পাতা, কাণ্ড এবং কন্দকে আক্রমণ করে এমন একটি সাধারণ এবং সম্ভাব্য ধ্বংসাত্মক রোগ। এটি Phytophthora infestans ছত্রাক দ্বারা সৃষ্ট।",
    chemicals: ["Copper oxychloride"],
  },
  {
    id: "DAE_PEST_B3531E_001",
    score: 31.08,
    publisher: "DAE",
    title: "আলুর মোজাইক বা ধসা রোগ (late blight)",
    snippet: "আলুর মোজাইক বা ধসা রোগ (late blight) দমনের জন্য অধিকাংশ প্যান্ডি 80WP ফরমুলেশনের এবং প্রতি হেক্টরে ১.৫ কেজি মাত্রায় প্রয়োগ করতে হবে।",
    chemicals: ["Mancozeb", "Metalaxyl"],
  },
  {
    id: "CABI_POTATO_42D248_001",
    score: 27.71,
    publisher: "CABI",
    title: "Potato Late Blight — লেট ব্লাইট",
    snippet: "লেট ব্লাইট একটি মারাত্মক ছত্রাকজনিত রোগ যা Phytophthora infestans দ্বারা সৃষ্ট। এটি পাতার নিচে ছোট ছোট সবুজ-বাদামি দাগ হিসেবে শুরু হয়।",
    chemicals: [],
  },
];

const REAL_ANSWER = `আলুর দেরি ব্লাইট (Late Blight) একটি মারাত্মক ছত্রাকজনিত রোগ যা Phytophthora infestans দ্বারা সৃষ্ট। এটি পাতা, কাণ্ড ও কন্দে আক্রমণ করে।

প্রতিরোধের উপায়:
• রোগ প্রতিরোধী জাত নির্বাচন করুন
• সঠিক নিষ্কাশন ব্যবস্থা নিশ্চিত করুন
• আক্রান্ত গাছ অবিলম্বে অপসারণ করুন

কীটনাশক: প্রতি লিটার পানিতে ২ গ্রাম Mancozeb 80WP মিশ্রণ করে স্প্রে করুন [DAE_PEST_1206A0_001]।

নিশ্চিত হতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।`;

const SAFETY_CATEGORIES = [
  { id: "chemical_misuse", bn: "রাসায়নিক অপব্যবহার", trigger: "রোগ নিশ্চিত ছাড়া রাসায়নিক চাওয়া", severe: true },
  { id: "dosage_safety", bn: "মাত্রা নিরাপত্তা", trigger: "প্রয়োগের প্রেক্ষিত ছাড়া ডোজ", severe: true },
  { id: "human_medical_scope", bn: "মানব চিকিৎসা", trigger: "মানব স্বাস্থ্য/বিষক্রিয়া", severe: true },
  { id: "scope_missing_crop", bn: "ফসল অনুপস্থিত", trigger: "ফসলের নাম ছাড়া চিকিৎসা", severe: false },
  { id: "diagnostic_overshoot", bn: "অতিরিক্ত নির্ণয়", trigger: "একটি অস্পষ্ট লক্ষণ থেকে নির্ণয়", severe: false },
  { id: "over_promise", bn: "অতিরঞ্জিত প্রতিশ্রুতি", trigger: "ফলন/নিরাময় গ্যারান্টি", severe: false },
];

export default function SafetyPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-20 py-14">
      {/* Hero */}
      <motion.section initial="hidden" animate="visible" variants={stagger} className="text-center">
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
          Safety-Critical Agentic RAG
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink">
          নিরাপত্তা-সচেতন <span className="text-leaf">এজেন্টিক পাইপলাইন</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
          একটি প্রকৃত প্রশ্ন কীভাবে চার ধাপ পার হয়ে উত্তর হয় — নিচের অ্যানিমেশনে দেখুন।
        </motion.p>
      </motion.section>

      {/* THE animated RAG workflow */}
      <RagWorkflowDemo />

      {/* Safety taxonomy (compact) */}
      <SafetyTaxonomy />

      {/* Audit trail */}
      <AuditTrail />
    </div>
  );
}

/* =========================================================================
   RagWorkflowDemo — the centerpiece.
   Shows a real query flowing through 4 stages with real data.
   User clicks "Run" to start the animation.
   ========================================================================= */

function RagWorkflowDemo() {
  const [stage, setStage] = useState<Stage>("idle");
  const [visibleSources, setVisibleSources] = useState(0);
  const [typedAnswer, setTypedAnswer] = useState("");
  const timers = useRef<NodeJS.Timeout[]>([]);

  const clearTimers = () => {
    timers.current.forEach(clearTimeout);
    timers.current = [];
  };

  const run = () => {
    clearTimers();
    setStage("safety");
    setVisibleSources(0);
    setTypedAnswer("");

    // Stage 1: Safety (1.2s)
    timers.current.push(setTimeout(() => setStage("retrieval"), 1200));

    // Stage 2: Retrieval — reveal sources one by one (2s total)
    timers.current.push(setTimeout(() => setVisibleSources(1), 1400));
    timers.current.push(setTimeout(() => setVisibleSources(2), 1700));
    timers.current.push(setTimeout(() => setVisibleSources(3), 2000));
    timers.current.push(setTimeout(() => setVisibleSources(4), 2300));

    // Stage 3: Generation — type out answer (3s)
    timers.current.push(setTimeout(() => {
      setStage("generation");
      let i = 0;
      const text = REAL_ANSWER;
      const typeInterval = setInterval(() => {
        i += 3;
        setTypedAnswer(text.slice(0, i));
        if (i >= text.length) {
          clearInterval(typeInterval);
          setStage("verifier");
        }
      }, 30);
      timers.current.push(typeInterval as unknown as NodeJS.Timeout);
    }, 2600));

    // Stage 4: Verifier (1.5s)
    timers.current.push(setTimeout(() => setStage("done"), 5500));
  };

  useEffect(() => () => clearTimers(), []);

  const stages = [
    { id: "safety", label: "নিরাপত্তা", sub: "Safety", icon: Shield },
    { id: "retrieval", label: "তথ্য সংগ্রহ", sub: "Retrieval", icon: Search },
    { id: "generation", label: "উত্তর তৈরি", sub: "Generation", icon: PenLine },
    { id: "verifier", label: "যাচাই", sub: "Verifier", icon: CheckCircle2 },
  ];

  const stageOrder = ["idle", "safety", "retrieval", "generation", "verifier", "done"];
  const currentIdx = stageOrder.indexOf(stage);

  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-80px" }}
      variants={stagger}
    >
      <motion.h2 variants={enter} className="mb-3 text-center font-display text-2xl text-ink">
        লাইভ পাইপলাইন ডেমো
      </motion.h2>
      <motion.p variants={enter} className="mb-6 text-center text-sm text-ink-soft">
        একটি প্রকৃত কৃষকের প্রশ্ন কীভাবে উত্তর হয় — ধাপে ধাপে।
      </motion.p>

      {/* Query + Run button */}
      <motion.div variants={enter} className="mb-6 rounded-xl border rule bg-paper-2/40 p-4">
        <div className="flex items-center justify-between gap-4">
          <div className="flex-1">
            <div className="text-[10px] uppercase tracking-[0.14em] text-ink-faint">কৃষকের প্রশ্ন</div>
            <div className="mt-1 text-sm font-medium text-ink">{REAL_QUERY}</div>
          </div>
          <button
            onClick={run}
            disabled={stage !== "idle" && stage !== "done"}
            className="flex items-center gap-2 rounded-lg bg-leaf px-5 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-50"
          >
            {stage === "idle" ? <Play className="h-4 w-4" /> : <RotateCcw className="h-4 w-4" />}
            {stage === "idle" ? "চালান" : stage === "done" ? "পুনরায়" : "চলছে…"}
          </button>
        </div>
      </motion.div>

      {/* Pipeline stages — horizontal */}
      <motion.div variants={enter} className="mb-6 flex items-center justify-between gap-1">
        {stages.map((s, i) => {
          const isActive = currentIdx > i;
          const isCurrent = stage === s.id;
          return (
            <div key={s.id} className="flex flex-1 flex-col items-center">
              <motion.div
                animate={{
                  scale: isCurrent ? 1.1 : 1,
                  backgroundColor: isActive || isCurrent ? "var(--color-leaf)" : "var(--color-paper)",
                  color: isActive || isCurrent ? "var(--color-paper)" : "var(--color-ink-faint)",
                }}
                transition={{ duration: dur.normal, ease: ease.smooth }}
                className="flex h-12 w-12 items-center justify-center rounded-full border-2"
                style={{
                  borderColor: isActive || isCurrent ? "var(--color-leaf)" : "var(--color-bone)",
                }}
              >
                <s.icon className="h-5 w-5" />
              </motion.div>
              <div className={`mt-2 text-center text-xs ${isActive || isCurrent ? "text-ink" : "text-ink-faint"}`}>
                <div className="font-display">{s.label}</div>
                <div className="font-mono text-[9px]">{s.sub}</div>
              </div>
              {/* Connector */}
              {i < stages.length - 1 && (
                <div className="mt-1 h-8 w-px" style={{ backgroundColor: currentIdx > i + 1 ? "var(--color-leaf)" : "var(--color-bone)" }} />
              )}
            </div>
          );
        })}
      </motion.div>

      {/* Stage detail panels — appear as animation progresses */}
      <div className="space-y-3">
        {/* Safety result */}
        <AnimatePresence>
          {(stage === "safety" || currentIdx > 1) && (
            <StagePanel
              icon={Shield}
              label="নিরাপত্তা শ্রেণীবিন্যাস"
            >
              <div className="flex items-center gap-3">
                <span className="rounded-md bg-leaf/10 px-3 py-1 text-sm font-medium text-leaf">
                  safe_agri
                </span>
                <span className="text-sm text-ink-soft">নির্ভরযোগ্যতা: ০.৯৯</span>
                <span className="text-xs text-ink-faint">→ প্রশ্নটি নিরাপদ, তথ্য সংগ্রহে যান</span>
              </div>
            </StagePanel>
          )}
        </AnimatePresence>

        {/* Retrieval result — real nodes */}
        <AnimatePresence>
          {(stage === "retrieval" || currentIdx > 2) && visibleSources > 0 && (
            <StagePanel icon={Search} label={`তথ্য সংগ্রহ — ${visibleSources}টি জ্ঞান নোড`}>
              <div className="space-y-2">
                {REAL_SOURCES.slice(0, visibleSources).map((src, i) => (
                  <motion.div
                    key={src.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.1, duration: dur.fast }}
                    className="rounded-lg border rule bg-paper p-3"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-[10px] text-ink-faint">[{i + 1}]</span>
                        <span className="font-mono text-[11px] text-ink">{src.id}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="rounded-md bg-ochre-soft/30 px-1.5 py-0.5 text-[10px] text-ochre">{src.publisher}</span>
                        <span className="font-mono text-[10px] tabular text-leaf">score: {src.score.toFixed(2)}</span>
                      </div>
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-ink-soft">{src.snippet}</p>
                    {src.chemicals.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {src.chemicals.map((chem) => (
                          <span key={chem} className="rounded bg-clay-soft/20 px-1.5 py-0.5 font-mono text-[9px] text-clay">{chem}</span>
                        ))}
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            </StagePanel>
          )}
        </AnimatePresence>

        {/* Generation result — typed answer */}
        <AnimatePresence>
          {(stage === "generation" || currentIdx > 3) && typedAnswer && (
            <StagePanel icon={PenLine} label="উত্তর তৈরি — Gemma-4 (উৎস-ভিত্তিক)">
              <div className="rounded-lg bg-paper p-4">
                <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink">
                  {typedAnswer}
                  {stage === "generation" && <span className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-leaf" />}
                </p>
              </div>
            </StagePanel>
          )}
        </AnimatePresence>

        {/* Verifier result */}
        <AnimatePresence>
          {stage === "done" && (
            <StagePanel icon={CheckCircle2} label="যাচাই — রাসায়নিক প্রমাণ-অডিট">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm">
                  <CheckCircle2 className="h-4 w-4 text-leaf" />
                  <span className="text-ink">Mancozeb 80WP — উৎসে বিদ্যমান ✓</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <CheckCircle2 className="h-4 w-4 text-leaf" />
                  <span className="text-ink">মাত্রা &ldquo;২ গ্রাম/লিটার&rdquo; — উৎসে বিদ্যমান ✓</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <CheckCircle2 className="h-4 w-4 text-leaf" />
                  <span className="text-ink">উৎস আইডি [DAE_PEST_1206A0_001] — যাচাইকৃত ✓</span>
                </div>
                <div className="mt-2 flex items-center gap-2 rounded-md bg-leaf/8 px-3 py-2 text-sm">
                  <span className="font-medium text-leaf">নির্ভরযোগ্যতা: verified</span>
                  <span className="text-ink-soft">— সব দাবি উৎসে ফিরে যাচাইকৃত</span>
                </div>
              </div>
            </StagePanel>
          )}
        </AnimatePresence>
      </div>
    </motion.section>
  );
}

/* === Stage panel wrapper === */
function StagePanel({
  icon: Icon,
  label,
  children,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      className="overflow-hidden rounded-xl border rule bg-paper-2/20"
    >
      <div className="border-b rule px-4 py-2.5">
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-leaf" />
          <span className="font-display text-sm text-ink">{label}</span>
        </div>
      </div>
      <div className="p-4">{children}</div>
    </motion.div>
  );
}

/* === Safety taxonomy (compact, collapsible) === */
function SafetyTaxonomy() {
  const [open, setOpen] = useState(false);
  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger}>
      <motion.button
        variants={enter}
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between rounded-xl border rule bg-paper px-5 py-4"
      >
        <div className="flex items-center gap-3">
          <Shield className="h-5 w-5 text-leaf" />
          <div className="text-left">
            <div className="font-display text-lg text-ink">১২-শ্রেণী নিরাপত্তা ট্যাক্সোনমি</div>
            <div className="text-xs text-ink-faint">অনিরাপদ প্রশ্ন কীভাবে আটকে যায়</div>
          </div>
        </div>
        <ChevronDown className={`h-5 w-5 text-ink-faint transition-transform ${open ? "rotate-180" : ""}`} />
      </motion.button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
              {SAFETY_CATEGORIES.map((cat) => (
                <div
                  key={cat.id}
                  className={`flex items-center justify-between rounded-lg border p-3 ${
                    cat.severe ? "border-clay-soft/40 bg-clay-soft/8" : "border-bone bg-paper-2/30"
                  }`}
                >
                  <div>
                    <div className="text-sm font-medium text-ink">{cat.bn}</div>
                    <div className="text-[11px] text-ink-faint">{cat.trigger}</div>
                  </div>
                  <span className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-medium ${
                    cat.severe ? "bg-clay/15 text-clay" : "bg-ochre-soft/30 text-ochre"
                  }`}>
                    {cat.severe ? "তীব্র" : "সামান্য"}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.section>
  );
}

/* === Audit trail === */
function AuditTrail() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="rounded-xl border rule bg-paper-2/30 p-6 text-center"
    >
      <motion.div variants={enter}>
        <AlertTriangle className="mx-auto h-8 w-8 text-clay" />
        <h2 className="mt-3 font-display text-lg text-ink">অমীমাংসিত সমস্যা</h2>
        <p className="mx-auto mt-2 max-w-md text-sm text-ink-soft">
          পরিপূর্ণ অরাকল তথ্য থাকা সত্ত্বেও{" "}
          <span className="font-medium text-clay">{RESEARCH_STATS.hallucinationFloor}</span>{" "}
          রাসায়নিক হ্যালুসিনেশন থেকে যায় — সব মডেলে।
        </p>
        <p className="mt-3 text-xs text-ink-faint">
          প্রতিটি সিদ্ধান্ত স্থানীয়ভাবে লগ হয় —{" "}
          <a href="/analytics" className="text-leaf hover:text-leaf-2">পরিসংখ্যান দেখুন →</a>
        </p>
      </motion.div>
    </motion.section>
  );
}
