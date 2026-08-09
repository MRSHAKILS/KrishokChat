import { HELPLINE } from "@/lib/constants";

export default function ContactPage() {
  return (
    <div className="mx-auto max-w-2xl space-y-6 py-12">
      <h1 className="font-display text-3xl text-ink">যোগাযোগ</h1>
      <p className="text-sm text-ink-soft">
        কৃষি সংক্রান্ত যেকোনো প্রশ্নের জন্য নিচের নম্বরে যোগাযোগ করুন:
      </p>

      <div className="space-y-3">
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="flex items-center justify-between rounded-xl border rule bg-paper px-5 py-4 transition-colors hover:border-leaf"
        >
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-ink-faint">
              কৃষক কল সেন্টার
            </div>
            <div className="mt-0.5 text-sm text-ink">বাংলাদেশ সরকার</div>
          </div>
          <span className="tabular text-lg font-semibold text-leaf">
            {HELPLINE.krishiCallCenter}
          </span>
        </a>
        <a
          href={`tel:${HELPLINE.emergency}`}
          className="flex items-center justify-between rounded-xl border rule bg-paper px-5 py-4 transition-colors hover:border-clay"
        >
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-ink-faint">জরুরি</div>
            <div className="mt-0.5 text-sm text-ink">জাতীয় জরুরি সেবা</div>
          </div>
          <span className="tabular text-lg font-semibold text-clay">
            {HELPLINE.emergency}
          </span>
        </a>
      </div>

      <p className="text-xs text-ink-faint">
        এই ব্যবস্থা একটি গবেষণা প্রোটোটাইপ। জরুরি পরিস্থিতিতে সরাসরি কল করুন।
      </p>
    </div>
  );
}
