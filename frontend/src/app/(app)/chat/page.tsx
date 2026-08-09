import { QAPanel } from "@/components/qa-panel";

export default function ChatPage() {
  return (
    <div className="space-y-5">
      <div>
        <h1 className="font-display text-3xl text-ink">কৃষি পরামর্শ</h1>
        <p className="mt-1 text-sm text-ink-soft">
          বাংলায় যেকোনো কৃষি প্রশ্ন করুন — নিরাপত্তা যাচাই, তথ্য সংগ্রহ, উত্তর তৈরি ও
          যাচাইকরণের ধাপগুলো সরাসরি দেখুন।
        </p>
      </div>
      <div
        className="flex flex-col rounded-xl border rule bg-paper p-5"
        style={{ minHeight: "65vh" }}
      >
        <QAPanel />
      </div>
    </div>
  );
}
