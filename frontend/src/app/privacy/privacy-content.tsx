"use client";

import Link from "next/link";
import { ShieldCheck, Database, Clock, EyeOff, Phone, FileText } from "lucide-react";
import { useLanguage } from "@/context/language-context";

export function PrivacyContent() {
  const { locale } = useLanguage();
  const en = locale === "en";
  return (
    <div className="mx-auto max-w-3xl space-y-10 px-5 py-10 sm:py-14">
      {/* Header */}
      <div>
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-ochre">
          {en ? "Privacy and Data Management" : "গোপনীয়তা ও ডেটা ব্যবস্থাপনা"}
        </p>
        <h1 className="mt-3 font-display text-3xl text-ink sm:text-4xl">
          {en ? "Privacy Policy" : "গোপনীয়তা নীতি"}
        </h1>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
          {en
            ? "KrishokTech is a research prototype. This page truthfully describes what data the system stores, how long it is kept, and where it is processed — with no exaggeration. Effective date: August 21, 2026."
            : "কৃষক টেক একটি গবেষণা প্রোটোটাইপ। এই পাতায় সত্যভাবে বর্ণনা করা হয়েছে সিস্টেম কী তথ্য সংরক্ষণ করে, কতদিন রাখে এবং কোথায় প্রক্রিয়া করে — কোনো অতিরঞ্জন ছাড়া। কার্যকর তারিখ: ২১ আগস্ট ২০২৬।"}
        </p>
        <div className="mt-4 flex flex-wrap gap-2 text-[11px]">
          <span className="rounded-full border rule bg-paper-2/60 px-2.5 py-1 text-ink-soft">
            {en ? "Local-only · no external tracking" : "Local-only · কোনো বাহ্যিক ট্র্যাকিং নেই"}
          </span>
          <span className="rounded-full border rule bg-paper-2/60 px-2.5 py-1 text-ink-soft">
            {en ? "Per PDP Ordinance 2025 (No. 61)" : "PDP Ordinance 2025 (No. 61) অনুসারে"}
          </span>
        </div>
      </div>

      {/* What we store */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <Database className="h-4 w-4 text-leaf" />
          {en ? "What data is stored" : "কী তথ্য সংরক্ষিত হয়"}
        </div>
        <div className="mt-4 grid gap-4 text-sm leading-relaxed text-ink-soft sm:grid-cols-3">
          <div className="rounded-xl border rule bg-paper-2/30 p-4">
            <div className="text-xs font-semibold text-ink">{en ? "Audit log" : "অডিট লগ"}</div>
            <p className="mt-1 text-xs">
              {en ? (
                <>
                  Each query&apos;s <code className="rounded bg-bone px-1 py-0.5 text-[10px]">category</code>,
                  action, verifier flags, model, request ID, and timestamp —{" "}
                  <code className="text-[10px]">backend/app/logs/safety_audit.jsonl</code> and{" "}
                  <code className="text-[10px]">backend/data/krishokchat.db</code> (audit_records).
                </>
              ) : (
                <>
                  প্রতিটি প্রশ্নের শ্রেণি (<code className="rounded bg-bone px-1 py-0.5 text-[10px]">category</code>),
                  ক্রিয়া, ভেরিফায়ার ফ্ল্যাগ, মডেল, request ID ও সময় —{" "}
                  <code className="text-[10px]">backend/app/logs/safety_audit.jsonl</code> ও{" "}
                  <code className="text-[10px]">backend/data/krishokchat.db</code> (audit_records) এ।
                </>
              )}
            </p>
          </div>
          <div className="rounded-xl border rule bg-paper-2/30 p-4">
            <div className="text-xs font-semibold text-ink">{en ? "Session history" : "সেশন ইতিহাস"}</div>
            <p className="mt-1 text-xs">
              {en ? (
                <>
                  The back-and-forth (role/content) within one conversation — in memory or the same
                  SQLite&apos;s <code className="text-[10px]">sessions</code> table, bounded by TTL and
                  max-turns.
                </>
              ) : (
                <>
                  একই কথোপকথনের ধারাবাহিক প্রশ্নোত্তর (role/content) — মেমোরি বা একই
                  SQLite-এ <code className="text-[10px]">sessions</code> টেবিলে, TTL ও
                  max-turns দ্বারা সীমিত।
                </>
              )}
            </p>
          </div>
          <div className="rounded-xl border rule bg-paper-2/30 p-4">
            <div className="text-xs font-semibold text-ink">{en ? "Helpline registration" : "হেল্পলাইন নিবন্ধন"}</div>
            <p className="mt-1 text-xs">
              {en ? (
                <>
                  If you voluntarily fill in the form — name, phone, district, crop, notes — into{" "}
                  <code className="text-[10px]">helpline_registrations.jsonl</code>.
                </>
              ) : (
                <>
                  আপনি স্বেচ্ছায় ফর্ম পূরণ করলে — নাম, ফোন, জেলা, ফসল, নোট —{" "}
                  <code className="text-[10px]">helpline_registrations.jsonl</code> এ।
                </>
              )}
            </p>
          </div>
        </div>
        <p className="mt-4 text-xs leading-relaxed text-ink-faint">
          {en
            ? "No external analytics, advertising trackers, or third-party PII processors are used. All storage happens locally on the host."
            : "কোনো বাহ্যিক অ্যানালিটিক্স, বিজ্ঞাপন ট্র্যাকার বা তৃতীয় পক্ষের PII প্রসেসর ব্যবহার করা হয় না। সমস্ত সংরক্ষণ হোস্টে স্থানীয়ভাবে হয়।"}
        </p>
      </section>

      {/* Retention */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <Clock className="h-4 w-4 text-leaf" />
          {en ? "How long data is kept" : "কতদিন রাখা হয়"}
        </div>
        <div className="mt-3 overflow-hidden rounded-xl border rule text-sm">
          <table className="w-full text-left text-xs sm:text-sm">
            <thead className="bg-paper-2/60 text-ink-faint">
              <tr>
                <th className="px-4 py-2 font-medium">{en ? "Data" : "তথ্য"}</th>
                <th className="px-4 py-2 font-medium">{en ? "Default" : "ডিফল্ট"}</th>
                <th className="px-4 py-2 font-medium">{en ? "When enabled" : "সক্রিয় হলে"}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bone bg-paper text-ink-soft">
              <tr>
                <td className="px-4 py-3">{en ? "Audit" : "অডিট"}</td>
                <td className="px-4 py-3">
                  {en ? (
                    <><code>AUDIT_RETENTION_DAYS=0</code> — forever (today&apos;s behavior)</>
                  ) : (
                    <><code>AUDIT_RETENTION_DAYS=0</code> — চিরকাল (আজকের আচরণ)</>
                  )}
                </td>
                <td className="px-4 py-3">
                  {en ? (
                    <>
                      <code>90</code> days — at startup and on every write:{" "}
                      <code>DELETE WHERE timestamp &lt; now() - 90d</code>
                    </>
                  ) : (
                    <>
                      <code>90</code> দিন — startup ও প্রতিটি write-এ{" "}
                      <code>DELETE WHERE timestamp &lt; now() - 90d</code>
                    </>
                  )}
                </td>
              </tr>
              <tr>
                <td className="px-4 py-3">{en ? "Session" : "সেশন"}</td>
                <td className="px-4 py-3">
                  <code>SESSION_RETENTION_DAYS=30</code> + TTL 1800s / 10 turns
                </td>
                <td className="px-4 py-3">{en ? "Same, lazy purge (init + get/append)" : "একই, lazy purge (init + get/append)"}</td>
              </tr>
              <tr>
                <td className="px-4 py-3">{en ? "Helpline" : "হেল্পলাইন"}</td>
                <td className="px-4 py-3">{en ? "No automatic deletion" : "স্বয়ংক্রিয় মুছে ফেলা নেই"}</td>
                <td className="px-4 py-3">{en ? "365 days suggested (operator decision)" : "প্রস্তাব 365 দিন (অপারেটর সিদ্ধান্ত)"}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-xs text-ink-faint">
          {en ? (
            <>
              Defaults = demo-identical. Enabling is a one-line <code>.env</code>{" "}
              change — revertible instantly with <code>AUDIT_RETENTION_DAYS=0</code> or{" "}
              <code>PII_REDACTION_ENABLED=false</code>. Details:{" "}
              <code>docs/production_readiness/retention_policy.md</code>.
            </>
          ) : (
            <>
              ডিফল্ট = ডেমো-অভিন্ন। সক্রিয়করণ একটি এক-লাইন <code>.env</code>{" "}
              পরিবর্তন — <code>AUDIT_RETENTION_DAYS=0</code> বা{" "}
              <code>PII_REDACTION_ENABLED=false</code> দিয়ে তৎক্ষণাৎ পূর্বাবস্থায়
              ফেরা যায়। বিস্তারিত:{" "}
              <code>docs/production_readiness/retention_policy.md</code>.
            </>
          )}
        </p>
      </section>

      {/* PII Redaction */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <EyeOff className="h-4 w-4 text-leaf" />
          {en ? "PII Redaction" : "PII রিডাকশন"}
        </div>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
          {en ? (
            <>
              When <code>PII_REDACTION_ENABLED=true</code>, before storage, phone numbers
              (<code>+880</code>/<code>01</code> and Bengali digits <code>০-৯</code>), emails, and
              names labeled <code>নাম:</code>/<code>name:</code> are replaced by regex with{" "}
              <code>[REDACTED_PHONE]</code> / <code>[REDACTED_EMAIL]</code> /{" "}
              <code>[REDACTED]</code>. This is <strong>best-effort</strong> — no claim of
              perfection is made — and <strong>is never applied to the user-visible answer</strong>,
              only to the stored audit text. Default is{" "}
              <code>PII_REDACTION_ENABLED=false</code> (today&apos;s verbatim).
            </>
          ) : (
            <>
              <code>PII_REDACTION_ENABLED=true</code> হলে সংরক্ষণের আগে প্রশ্নের
              পাঠ্য থেকে ফোন নম্বর (<code>+880</code>/<code>01</code> ও বাংলা
              ডিজিট <code>০-৯</code>), ইমেইল এবং <code>নাম:</code>/
              <code>name:</code> লেবেলযুক্ত নাম regex দ্বারা{" "}
              <code>[REDACTED_PHONE]</code> / <code>[REDACTED_EMAIL]</code> /
              <code>[REDACTED]</code> দিয়ে প্রতিস্থাপন করা হয়। এটি{" "}
              <strong>best-effort</strong> — নিখুঁত দাবি করা হয় না — এবং{" "}
              <strong>ব্যবহারকারীর কাছে দৃশ্যমান উত্তরে কখনো প্রয়োগ হয় না</strong>,
              শুধু সংরক্ষিত অডিট টেক্সটে। ডিফল্ট{" "}
              <code>PII_REDACTION_ENABLED=false</code> (আজকের verbatim)।
            </>
          )}
        </p>
        <p className="mt-2 text-xs text-ink-faint">
          {en ? (
            <>
              Implementation: <code>backend/app/core/redaction.py</code> + tests{" "}
              <code>backend/tests/test_redaction.py</code> (including Bengali digits).
            </>
          ) : (
            <>
              বাস্তবায়ন: <code>backend/app/core/redaction.py</code> + পরীক্ষা{" "}
              <code>backend/tests/test_redaction.py</code> (বাংলা ডিজিট সহ)।
            </>
          )}
        </p>
      </section>

      {/* Local-only */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <ShieldCheck className="h-4 w-4 text-leaf" />
          {en ? "Local Processing and Security" : "স্থানীয় প্রক্রিয়াকরণ ও নিরাপত্তা"}
        </div>
        <ul className="mt-3 list-disc space-y-1.5 pl-5 text-sm leading-relaxed text-ink-soft">
          <li>
            {en ? (
              <>
                Audit/session/helpline data is never sent to an external service —{" "}
                <code>backend/app/logs/</code> and{" "}
                <code>backend/data/krishokchat.db</code> stay on the host.
              </>
            ) : (
              <>
                অডিট/সেশন/হেল্পলাইন কখনো বাহ্যিক সেবায় পাঠানো হয় না —{" "}
                <code>backend/app/logs/</code> ও{" "}
                <code>backend/data/krishokchat.db</code> হোস্টে থাকে।
              </>
            )}
          </li>
          <li>{en ? <>No subprocessors (declared &ldquo;none&rdquo; in the DPA template).</> : <>কোনো সাবপ্রসেসর নেই (DPA টেমপ্লেটে &ldquo;none&rdquo; ঘোষিত)।</>}</li>
          <li>
            {en ? (
              <>
                Every request gets an <code>X-Request-ID</code> and a JSON log entry — when PII
                redaction is enabled, the same scrub applies to logs too.
              </>
            ) : (
              <>
                প্রতিটি অনুরোধে <code>X-Request-ID</code> ও JSON লগ — PII রিডাকশন
                চালু থাকলে লগেও একই স্ক্রাব প্রযোজ্য।
              </>
            )}
          </li>
        </ul>
      </section>

      {/* Rights */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <FileText className="h-4 w-4 text-leaf" />
          {en ? "Your Rights and Deletion" : "আপনার অধিকার ও মুছে ফেলা"}
        </div>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
          {en ? (
            <>
              To delete a helpline registration or ask about audit/session data, contact the
              operator. In a B2B deployment, on the controller&apos;s request, deletion is confirmed
              and bounded by <code>DELETE WHERE timestamp &lt; …</code> — no background job, a
              single process.
            </>
          ) : (
            <>
              হেল্পলাইন নিবন্ধন মুছতে বা অডিট/সেশন ডেটা সম্পর্কে জানতে অপারেটরের সাথে
              যোগাযোগ করুন। B2B স্থাপনায় নিয়ন্ত্রক (controller) অনুরোধে{" "}
              <code>DELETE WHERE timestamp &lt; …</code> দ্বারা সীমিত, নিশ্চিত
              মুছে ফেলা করা হয় — কোনো ব্যাকগ্রাউন্ড জব ছাড়া, একক প্রসেসে।
            </>
          )}
        </p>
      </section>

      {/* Contact */}
      <section className="rounded-2xl border rule bg-paper-2/30 p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <Phone className="h-4 w-4 text-leaf" />
          {en ? "Contact" : "যোগাযোগ"}
        </div>
        <p className="mt-3 text-sm text-ink-soft">
          {en ? "Government helpline for agricultural emergencies or pesticide questions:" : "কৃষি জরুরি বা কীটনাশক বিষয়ে সরকারি হেল্পলাইন:"}
        </p>
        <div className="mt-3 flex flex-wrap gap-3">
          <a
            href="tel:16123"
            className="inline-flex items-center gap-1.5 rounded-lg bg-leaf px-4 py-2 text-sm font-semibold text-paper hover:bg-leaf-2"
          >
            <Phone className="h-4 w-4" /> {en ? "16123 — Agriculture Call Center" : "১৬১২৩ — কৃষি কল সেন্টার"}
          </a>
          <a
            href="tel:999"
            className="inline-flex items-center gap-1.5 rounded-lg border rule bg-paper px-4 py-2 text-sm font-medium text-ink hover:border-leaf hover:text-leaf"
          >
            {en ? "999 — Emergency" : "৯৯৯ — জরুরি"}
          </a>
        </div>
        <p className="mt-4 text-xs text-ink-faint">
          {en ? (
            <>
              B2B data processing terms template: <code>deploy/DPA_template.md</code> · Code
              license: MIT ( <code>LICENSE</code> ) · Dataset: CC-BY-4.0 (per paper/docs).
            </>
          ) : (
            <>
              B2B ডেটা প্রসেসিং শর্তাবলীর টেমপ্লেট:{" "}
              <code>deploy/DPA_template.md</code> · কোড লাইসেন্স: MIT ({" "}
              <code>LICENSE</code>) · ডেটাসেট: CC-BY-4.0 (paper/docs অনুযায়ী)।
            </>
          )}
        </p>
        <div className="mt-4 flex flex-wrap gap-2 text-xs">
          <Link href="/contact" className="text-leaf hover:underline">
            {en ? "Help and Contact →" : "সাহায্য ও যোগাযোগ →"}
          </Link>
          <span className="text-ink-faint">·</span>
          <Link href="/research/safety" className="text-leaf hover:underline">
            {en ? "Safety Framework →" : "নিরাপত্তা কাঠামো →"}
          </Link>
        </div>
      </section>

      <p className="text-center text-[11px] text-ink-faint">
        {en ? (
          <>
            This policy describes the code&apos;s actual behavior; it is not legal advice. Setting
            changes are revertible with a one-line <code>.env</code> switch or{" "}
            <code>git revert</code>.
          </>
        ) : (
          <>
            এই নীতি কোডের প্রকৃত আচরণ বর্ণনা করে; এটি আইনি পরামর্শ নয়। সেটিংস
            পরিবর্তন এক-লাইন <code>.env</code> সুইচ বা{" "}
            <code>git revert</code> দ্বারা প্রত্যাহারযোগ্য।
          </>
        )}
      </p>
    </div>
  );
}
