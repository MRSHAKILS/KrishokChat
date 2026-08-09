import { DetectPanel } from "@/components/detect-panel";

export default function DetectPage() {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">ফসলের রোগ নির্ণয়</h1>
        <p className="text-sm text-gray-500 mt-1">
          পাতার ছবি আপলোড করুন — ফসল শনাক্ত করে নির্দিষ্ট রোগ মডেল দিয়ে বিশ্লেষণ করা হবে।
        </p>
      </div>
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <DetectPanel />
      </div>
    </div>
  );
}
