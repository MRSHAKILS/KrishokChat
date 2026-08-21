import Link from "next/link";
import { ShieldCheck, Database, Clock, EyeOff, Phone, FileText } from "lucide-react";

export const metadata = {
  title: "গোপনীয়তা নীতি — KrishokChat",
  description:
    "KrishokChat কী তথ্য সংরক্ষণ করে, কতদিন রাখে এবং কীভাবে স্থানীয়ভাবে প্রক্রিয়া করে — PDP 2025-সম্মত নীতি।",
};

export default function PrivacyPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-10 px-5 py-10 sm:py-14">
      {/* Header */}
      <div>
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-ochre">
          গোপনীয়তা ও ডেটা ব্যবস্থাপনা
        </p>
        <h1 className="mt-3 font-display text-3xl text-ink sm:text-4xl">
          গোপনীয়তা নীতি
        </h1>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
          কৃষক চ্যাট একটি গবেষণা প্রোটোটাইপ। এই পাতায় সত্যভাবে বর্ণনা করা হয়েছে
          সিস্টেম কী তথ্য সংরক্ষণ করে, কতদিন রাখে এবং কোথায় প্রক্রিয়া করে —
          কোনো অতিরঞ্জন ছাড়া। কার্যকর তারিখ: ২১ আগস্ট ২০২৬।
        </p>
        <div className="mt-4 flex flex-wrap gap-2 text-[11px]">
          <span className="rounded-full border rule bg-paper-2/60 px-2.5 py-1 text-ink-soft">
            Local-only · কোনো বাহ্যিক ট্র্যাকিং নেই
          </span>
          <span className="rounded-full border rule bg-paper-2/60 px-2.5 py-1 text-ink-soft">
            PDP Ordinance 2025 (No. 61) সচেতন
          </span>
        </div>
      </div>

      {/* What we store */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <Database className="h-4 w-4 text-leaf" />
          কী তথ্য সংরক্ষিত হয়
        </div>
        <div className="mt-4 grid gap-4 text-sm leading-relaxed text-ink-soft sm:grid-cols-3">
          <div className="rounded-xl border rule bg-paper-2/30 p-4">
            <div className="text-xs font-semibold text-ink">অডিট লগ</div>
            <p className="mt-1 text-xs">
              প্রতিটি প্রশ্নের শ্রেণি (<code className="rounded bg-bone px-1 py-0.5 text-[10px]">category</code>),
              ক্রিয়া, ভেরিফায়ার ফ্ল্যাগ, মডেল, request ID ও সময় —{" "}
              <code className="text-[10px]">backend/app/logs/safety_audit.jsonl</code> ও{" "}
              <code className="text-[10px]">backend/data/krishokchat.db</code> (audit_records) এ।
            </p>
          </div>
          <div className="rounded-xl border rule bg-paper-2/30 p-4">
            <div className="text-xs font-semibold text-ink">সেশন ইতিহাস</div>
            <p className="mt-1 text-xs">
              একই কথোপকথনের ধারাবাহিক প্রশ্নোত্তর (role/content) — মেমোরি বা একই
              SQLite-এ <code className="text-[10px]">sessions</code> টেবিলে, TTL ও
              max-turns দ্বারা সীমিত।
            </p>
          </div>
          <div className="rounded-xl border rule bg-paper-2/30 p-4">
            <div className="text-xs font-semibold text-ink">হেল্পলাইন নিবন্ধন</div>
            <p className="mt-1 text-xs">
              আপনি স্বেচ্ছায় ফর্ম পূরণ করলে — নাম, ফোন, জেলা, ফসল, নোট —{" "}
              <code className="text-[10px]">helpline_registrations.jsonl</code> এ।
            </p>
          </div>
        </div>
        <p className="mt-4 text-xs leading-relaxed text-ink-faint">
          কোনো বাহ্যিক অ্যানালিটিক্স, বিজ্ঞাপন ট্র্যাকার বা তৃতীয় পক্ষের PII
          প্রসেসর ব্যবহার করা হয় না। সমস্ত সংরক্ষণ হোস্টে স্থানীয়ভাবে হয়।
        </p>
      </section>

      {/* Retention */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <Clock className="h-4 w-4 text-leaf" />
          কতদিন রাখা হয়
        </div>
        <div className="mt-3 overflow-hidden rounded-xl border rule text-sm">
          <table className="w-full text-left text-xs sm:text-sm">
            <thead className="bg-paper-2/60 text-ink-faint">
              <tr>
                <th className="px-4 py-2 font-medium">তথ্য</th>
                <th className="px-4 py-2 font-medium">ডিফল্ট</th>
                <th className="px-4 py-2 font-medium">সক্রিয় হলে</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bone bg-paper text-ink-soft">
              <tr>
                <td className="px-4 py-3">অডিট</td>
                <td className="px-4 py-3">
                  <code>AUDIT_RETENTION_DAYS=0</code> — চিরকাল (আজকের আচরণ)
                </td>
                <td className="px-4 py-3">
                  <code>90</code> দিন — startup ও প্রতিটি write-এ{" "}
                  <code>DELETE WHERE timestamp &lt; now() - 90d</code>
                </td>
              </tr>
              <tr>
                <td className="px-4 py-3">সেশন</td>
                <td className="px-4 py-3">
                  <code>SESSION_RETENTION_DAYS=30</code> + TTL 1800s / 10 turns
                </td>
                <td className="px-4 py-3">একই, lazy purge (init + get/append)</td>
              </tr>
              <tr>
                <td className="px-4 py-3">হেল্পলাইন</td>
                <td className="px-4 py-3">স্বয়ংক্রিয় মুছে ফেলা নেই</td>
                <td className="px-4 py-3">প্রস্তাব 365 দিন (অপারেটর সিদ্ধান্ত)</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-xs text-ink-faint">
          ডিফল্ট = ডেমো-অভিন্ন। সক্রিয়করণ একটি এক-লাইন <code>.env</code>{" "}
          পরিবর্তন — <code>AUDIT_RETENTION_DAYS=0</code> বা{" "}
          <code>PII_REDACTION_ENABLED=false</code> দিয়ে তৎক্ষণাৎ পূর্বাবস্থায়
          ফেরা যায়। বিস্তারিত:{" "}
          <code>docs/production_readiness/retention_policy.md</code>.
        </p>
      </section>

      {/* PII Redaction */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <EyeOff className="h-4 w-4 text-leaf" />
          PII রিডাকশন
        </div>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
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
        </p>
        <p className="mt-2 text-xs text-ink-faint">
          বাস্তবায়ন: <code>backend/app/core/redaction.py</code> + পরীক্ষা{" "}
          <code>backend/tests/test_redaction.py</code> (বাংলা ডিজিট সহ)।
        </p>
      </section>

      {/* Local-only */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <ShieldCheck className="h-4 w-4 text-leaf" />
          স্থানীয় প্রক্রিয়াকরণ ও নিরাপত্তা
        </div>
        <ul className="mt-3 list-disc space-y-1.5 pl-5 text-sm leading-relaxed text-ink-soft">
          <li>
            অডিট/সেশন/হেল্পলাইন কখনো বাহ্যিক সেবায় পাঠানো হয় না —{" "}
            <code>backend/app/logs/</code> ও{" "}
            <code>backend/data/krishokchat.db</code> হোস্টে থাকে।
          </li>
          <li>কোনো সাবপ্রসেসর নেই (DPA টেমপ্লেটে “none” ঘোষিত)।</li>
          <li>
            প্রতিটি অনুরোধে <code>X-Request-ID</code> ও JSON লগ — PII রিডাকশন
            চালু থাকলে লগেও একই স্ক্রাব প্রযোজ্য।
          </li>
        </ul>
      </section>

      {/* Rights */}
      <section className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <FileText className="h-4 w-4 text-leaf" />
          আপনার অধিকার ও মুছে ফেলা
        </div>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
          হেল্পলাইন নিবন্ধন মুছতে বা অডিট/সেশন ডেটা সম্পর্কে জানতে অপারেটরের সাথে
          যোগাযোগ করুন। B2B স্থাপনায় নিয়ন্ত্রক (controller) অনুরোধে{" "}
          <code>DELETE WHERE timestamp &lt; …</code> দ্বারা সীমিত, নিশ্চিত
          মুছে ফেলা করা হয় — কোনো ব্যাকগ্রাউন্ড জব ছাড়া, একক প্রসেসে।
        </p>
      </section>

      {/* Contact */}
      <section className="rounded-2xl border rule bg-paper-2/30 p-6 sm:p-8">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <Phone className="h-4 w-4 text-leaf" />
          যোগাযোগ
        </div>
        <p className="mt-3 text-sm text-ink-soft">
          কৃষি জরুরি বা কীটনাশক বিষয়ে সরকারি হেল্পলাইন:
        </p>
        <div className="mt-3 flex flex-wrap gap-3">
          <a
            href="tel:16123"
            className="inline-flex items-center gap-1.5 rounded-lg bg-leaf px-4 py-2 text-sm font-semibold text-paper hover:bg-leaf-2"
          >
            <Phone className="h-4 w-4" /> ১৬১২৩ — কৃষি কল সেন্টার
          </a>
          <a
            href="tel:999"
            className="inline-flex items-center gap-1.5 rounded-lg border rule bg-paper px-4 py-2 text-sm font-medium text-ink hover:border-leaf hover:text-leaf"
          >
            ৯৯৯ — জরুরি
          </a>
        </div>
        <p className="mt-4 text-xs text-ink-faint">
          B2B ডেটা প্রসেসিং শর্তাবলীর টেমপ্লেট:{" "}
          <code>deploy/DPA_template.md</code> · কোড লাইসেন্স: MIT ({" "}
          <code>LICENSE</code>) · ডেটাসেট: CC-BY-4.0 (paper/docs অনুযায়ী)।
        </p>
        <div className="mt-4 flex flex-wrap gap-2 text-xs">
          <Link href="/contact" className="text-leaf hover:underline">
            সাহায্য ও যোগাযোগ →
          </Link>
          <span className="text-ink-faint">·</span>
          <Link href="/research/safety" className="text-leaf hover:underline">
            নিরাপত্তা কাঠামো →
          </Link>
        </div>
      </section>

      <p className="text-center text-[11px] text-ink-faint">
        এই নীতি কোডের প্রকৃত আচরণ বর্ণনা করে; এটি আইনি পরামর্শ নয়। সেটিংস
        পরিবর্তন এক-লাইন <code>.env</code> সুইচ বা{" "}
        <code>git revert</code> দ্বারা প্রত্যাহারযোগ্য।
      </p>
    </div>
  );
}
