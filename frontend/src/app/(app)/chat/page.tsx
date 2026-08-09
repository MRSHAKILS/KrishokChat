import { QAPanel } from "@/components/qa-panel";

export default function ChatPage() {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">কৃষি পরামর্শ</h1>
        <p className="text-sm text-gray-500 mt-1">
          বাংলায় যেকোনো কৃষি প্রশ্ন করুন — নিরাপত্তা যাচাই, তথ্য সংগ্রহ, উত্তর তৈরি, যাচাইকরণের ধাপগুলো দেখুন।
        </p>
      </div>
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 min-h-[60vh]">
        <QAPanel />
      </div>
    </div>
  );
}
