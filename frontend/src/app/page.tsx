"use client";
import { useState } from "react";
import { DetectPanel } from "@/components/detect-panel";
import { QAPanel } from "@/components/qa-panel";

export default function Home() {
  const [detectedContext, setDetectedContext] = useState<{
    crop: string;
    disease: string;
  } | null>(null);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-gradient-to-r from-[#1a5632] to-[#2d7d46] text-white py-4 px-6 shadow">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🌾</span>
            <div>
              <h1 className="text-xl font-bold">কৃষক চ্যাট</h1>
              <p className="text-xs text-green-200">KrishokChat — বাংলাদেশ কৃষি-এআই পরামর্ষদাতা</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs text-green-100">
            <span className="hidden sm:inline px-2 py-0.5 bg-white/10 rounded-full">Safety-aware</span>
            <span className="hidden sm:inline px-2 py-0.5 bg-white/10 rounded-full">RAG-powered</span>
            <span className="px-2 py-0.5 bg-white/10 rounded-full">🇧🇩 বাংলা</span>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-6xl mx-auto w-full px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Detection Panel */}
          <section className="space-y-4">
            <div>
              <h2 className="text-lg font-bold text-gray-900">🔬 ফসলের রোগ নির্ণয়</h2>
              <p className="text-sm text-gray-500">
                পাতার ছবি আপলোড করুন — ফসল শনাক্ত করে নির্দিষ্ট রোগ মডেল দিয়ে বিশ্লেষণ করা হবে।
              </p>
            </div>
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <DetectPanel
                onDetected={(crop, disease) => setDetectedContext({ crop, disease })}
              />
            </div>

            {detectedContext && (
              <div className="bg-green-50 border border-green-200 rounded-2xl p-4">
                <div className="text-xs font-semibold text-green-800 mb-1">সনাক্ত ফসল</div>
                <div className="text-sm text-green-700">
                  <strong>{detectedContext.crop}</strong> — <strong>{detectedContext.disease}</strong>
                </div>
              </div>
            )}
          </section>

          {/* Chat Panel */}
          <section className="space-y-4">
            <div>
              <h2 className="text-lg font-bold text-gray-900">💬 কৃষি পরামর্শ</h2>
              <p className="text-sm text-gray-500">
                বাংলায় যেকোনো কৃষি প্রশ্ন করুন — নিরাপত্তা যাচাই, তথ্য সংগ্রহ, উত্তর তৈরি, যাচাইকরণের ধাপগুলো দেখুন।
              </p>
            </div>
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 min-h-[60vh]">
              <QAPanel detectedCrop={detectedContext?.crop} detectedDisease={detectedContext?.disease} />
            </div>
          </section>
        </div>
      </main>

      <footer className="border-t border-gray-100 py-4 text-center text-xs text-gray-400">
        KrishokChat Advisory System v0.1 — Safety-aware Bengali Agri-AI • কৃষক কল সেন্টার: ১৬১২৩
      </footer>
    </div>
  );
}
