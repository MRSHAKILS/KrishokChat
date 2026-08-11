import Link from "next/link";
import { ShieldCheck, Radio, Languages, Camera, LockKeyhole, Database, CheckCircle2 } from "lucide-react";
import { QAPanel } from "@/components/qa-panel";

export default function ChatPage() {
  return (
    <div className="space-y-6">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div className="max-w-2xl">
          <p className="mb-2 text-xs font-semibold text-leaf">কৃষকের সহায়তা</p>
          <h1 className="font-display text-2xl text-ink sm:text-3xl">কৃষি পরামর্শ</h1>
          <p className="mt-2 max-w-xl text-sm leading-relaxed text-ink-soft">
            বাংলায় আপনার ফসলের কথা লিখুন বা বলুন। উত্তর দেওয়ার আগে তথ্যসূত্র ও
            নিরাপত্তা যাচাই করা হবে।
          </p>
        </div>
        <div className="flex flex-wrap gap-2" aria-label="কথোপকথনের সুবিধা">
          {[
            { icon: ShieldCheck, label: "নিরাপত্তা যাচাই" },
            { icon: Radio, label: "লাইভ উত্তর" },
            { icon: Languages, label: "বাংলা সহায়তা" },
          ].map(({ icon: Icon, label }) => (
            <span key={label} className="inline-flex min-h-8 items-center gap-1.5 rounded-full border rule bg-paper-2/40 px-2.5 text-[11px] font-medium text-ink-faint">
              <Icon className="h-3.5 w-3.5 text-leaf" /> {label}
            </span>
          ))}
        </div>
      </header>
      <div
        className="rounded-2xl border rule bg-paper p-3 shadow-[0_12px_36px_rgba(52,39,23,0.07)] sm:p-4"
        style={{ minHeight: "clamp(36rem, 70vh, 48rem)" }}
        aria-label="কৃষি পরামর্শ কথোপকথন"
      >
        <div className="grid h-full min-h-0 gap-3 lg:grid-cols-[minmax(0,1fr)_220px]">
          <div className="min-h-0 rounded-xl border rule bg-paper p-4 sm:p-5">
            <QAPanel />
          </div>
          <aside className="hidden flex-col justify-between rounded-xl border rule bg-paper-2/35 p-4 lg:flex">
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-ochre">WORKSPACE</p>
              <h2 className="mt-2 font-display text-lg text-ink">উত্তর কীভাবে তৈরি হয়</h2>
              <div className="mt-5 space-y-3">
                {[{ icon: LockKeyhole, label: "নিরাপত্তা আগে", detail: "প্রশ্নের ঝুঁকি যাচাই" }, { icon: Database, label: "প্রাসঙ্গিক তথ্য", detail: "প্রি-কম্পিউটেড জ্ঞানভাণ্ডার" }, { icon: CheckCircle2, label: "উৎস মিলিয়ে", detail: "দাবি যাচাই করে দেখানো" }].map(({ icon: Icon, label, detail }, i) => (
                  <div key={label} className="relative flex gap-2.5">
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-paper text-leaf shadow-sm"><Icon className="h-3.5 w-3.5" /></span>
                    <div><div className="text-xs font-semibold text-ink">{label}</div><div className="mt-0.5 text-[10px] leading-relaxed text-ink-faint">{detail}</div></div>
                    {i < 2 && <span className="absolute left-3.5 top-8 h-3 border-l border-dashed border-bone" />}
                  </div>
                ))}
              </div>
            </div>
            <Link href="/detect" className="control-press mt-6 flex min-h-10 items-center justify-between gap-2 rounded-lg border border-leaf/25 bg-leaf/5 px-3 text-xs font-semibold text-leaf hover:bg-leaf/10">
              ছবি দিয়ে শুরু করুন <Camera className="h-3.5 w-3.5" />
            </Link>
          </aside>
        </div>
      </div>
    </div>
  );
}
