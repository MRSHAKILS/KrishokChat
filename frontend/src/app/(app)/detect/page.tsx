"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { DetectPanel } from "@/components/detect-panel";

export default function DetectPage() {
  const router = useRouter();
  const [detectedContext, setDetectedContext] = useState<{ crop: string; disease: string } | null>(null);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">ফসলের রোগ নির্ণয়</h1>
        <p className="text-sm text-gray-500 mt-1">
          পাতার ছবি আপলোড করুন — ফসল শনাক্ত করে নির্দিষ্ট রোগ মডেল দিয়ে বিশ্লেষণ করা হবে।
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <DetectPanel
          onDetected={(crop, disease) => {
            setDetectedContext({ crop, disease });
          }}
        />
      </div>

      {detectedContext && (
        <div className="bg-green-50 border border-green-200 rounded-2xl p-5">
          <h3 className="font-bold text-green-800 mb-2">সনাক্ত ফসল</h3>
          <p className="text-sm text-green-700 mb-3">
            <strong>{detectedContext.crop}</strong> — <strong>{detectedContext.disease}</strong>
          </p>
          <button
            onClick={() => router.push("/chat")}
            className="bg-[#1a5632] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-[#143d22] transition-colors"
          >
            💬 এই ফসল সম্পর্কে জিজ্ঞাসা করুন
          </button>
        </div>
      )}
    </div>
  );
}
