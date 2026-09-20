"use client";

import Link from "next/link";
import { ShieldCheck, Radio, Languages, Camera, LockKeyhole, Database, CheckCircle2 } from "lucide-react";
import { QAPanel } from "@/components/qa-panel";
import { UrgentAlertBanner } from "@/components/notifications/urgent-alert-banner";
import { useLanguage } from "@/context/language-context";

export default function ChatPage() {
  const { t } = useLanguage();

  return (
    <div className="space-y-6">
      <UrgentAlertBanner />
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div className="max-w-2xl">
          <p className="mb-2 text-xs font-semibold text-leaf">{t.chat.farmerSupport}</p>
          <h1 className="font-display text-2xl text-ink sm:text-3xl">{t.chat.title}</h1>
          <p className="mt-2 max-w-xl text-sm leading-relaxed text-ink-soft">
            {t.chat.description}
          </p>
        </div>
        <div className="flex flex-wrap gap-2" aria-label="Features">
          {[
            { icon: ShieldCheck, label: t.chat.safetyVerified },
            { icon: Radio, label: t.chat.liveResponse },
            { icon: Languages, label: t.chat.bilingualSupport },
          ].map(({ icon: Icon, label }) => (
            <span key={label} className="inline-flex min-h-8 items-center gap-1.5 rounded-full border rule bg-paper-2/40 px-2.5 text-xs font-medium text-ink-faint">
              <Icon className="h-3.5 w-3.5 text-leaf" /> {label}
            </span>
          ))}
        </div>
      </header>
      <div
        className="rounded-2xl border rule bg-paper p-3 shadow-[0_12px_36px_rgba(52,39,23,0.07)] sm:p-4"
        style={{ minHeight: "clamp(36rem, 70vh, 48rem)" }}
        aria-label="Conversation"
      >
        <div className="grid h-full min-h-0 gap-3 lg:grid-cols-[minmax(0,1fr)_220px]">
          <div className="min-h-0 rounded-xl border rule bg-paper p-4 sm:p-5">
            <QAPanel />
          </div>
          <aside className="hidden flex-col justify-between rounded-xl border rule bg-paper-2/35 p-4 lg:flex">
            <div>
              <p className="text-xs font-semibold text-ochre">{t.chat.asideGuide}</p>
              <h2 className="mt-2 font-display text-lg text-ink">{t.chat.asideTitle}</h2>
              <div className="mt-5 space-y-3">
                {[
                  { icon: LockKeyhole, label: t.chat.safetyFirst, detail: t.chat.safetyDesc },
                  { icon: Database, label: t.chat.groundedInfo, detail: t.chat.groundedDesc },
                  { icon: CheckCircle2, label: t.chat.verifiedSources, detail: t.chat.verifiedDesc },
                ].map(({ icon: Icon, label, detail }, i) => (
                  <div key={label} className="relative flex gap-2.5">
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-paper text-leaf shadow-sm">
                      <Icon className="h-3.5 w-3.5" />
                    </span>
                    <div>
                      <div className="text-xs font-semibold text-ink">{label}</div>
                      <div className="mt-0.5 text-xs leading-relaxed text-ink-faint">{detail}</div>
                    </div>
                    {i < 2 && <span className="absolute left-3.5 top-8 h-3 border-l border-dashed border-bone" />}
                  </div>
                ))}
              </div>
            </div>
            <Link
              href="/detect"
              className="control-press mt-6 flex min-h-10 items-center justify-between gap-2 rounded-lg border border-leaf/25 bg-leaf/5 px-3 text-xs font-semibold text-leaf hover:bg-leaf/10"
            >
              {t.chat.startWithPhoto} <Camera className="h-3.5 w-3.5" />
            </Link>
          </aside>
        </div>
      </div>
    </div>
  );
}
