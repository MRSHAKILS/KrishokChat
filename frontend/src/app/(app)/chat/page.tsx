import { QAPanel } from "@/components/qa-panel";

export default function ChatPage() {
  return (
    <div className="space-y-6">
      <header className="max-w-2xl">
        <p className="mb-2 text-xs font-semibold text-leaf">কৃষকের সহায়তা</p>
        <h1 className="font-display text-2xl text-ink sm:text-3xl">কৃষি পরামর্শ</h1>
        <p className="mt-2 max-w-xl text-sm leading-relaxed text-ink-soft">
          বাংলায় আপনার ফসলের কথা লিখুন বা বলুন। উত্তর দেওয়ার আগে তথ্যসূত্র ও
          নিরাপত্তা যাচাই করা হবে।
        </p>
      </header>
      <div
        className="flex flex-col rounded-2xl border rule bg-paper p-4 shadow-sm sm:p-6"
        style={{ minHeight: "clamp(36rem, 70vh, 48rem)" }}
        aria-label="কৃষি পরামর্শ কথোপকথন"
      >
        <QAPanel />
      </div>
    </div>
  );
}
