"use client";
import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { DetectPanel } from "@/components/detect-panel";
import { QAPanel } from "@/components/qa-panel";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"detect" | "chat">("detect");
  const [detectedContext, setDetectedContext] = useState<{ crop: string; disease: string } | null>(null);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-8">
        {/* Hero */}
        <section className="text-center mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
            বাংলাদেশ কৃষি-এআই পরামর্শদাতা
          </h1>
          <p className="text-sm text-gray-500 mt-2">
            পাতার ছবি আপলোড করুন — ফসল ও রোগ শনাক্ত করুন — বাংলায় পরামর্শ নিন
          </p>
        </section>

        {/* Tab buttons */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab("detect")}
            className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all ${
              activeTab === "detect"
                ? "bg-[#1a5632] text-white shadow-md"
                : "bg-white text-gray-600 border border-gray-200 hover:border-[#1a5632]/30"
            }`}
          >
            🔬 রোগ নির্ণয়
          </button>
          <button
            onClick={() => setActiveTab("chat")}
            className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all ${
              activeTab === "chat"
                ? "bg-[#1a5632] text-white shadow-md"
                : "bg-white text-gray-600 border border-gray-200 hover:border-[#1a5632]/30"
            }`}
          >
            💬 প্রশ্ন করুন
          </button>
        </div>

        {/* Tab content */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          {activeTab === "detect" ? (
            <div>
              <h2 className="text-lg font-bold text-gray-800 mb-1">ফসলের রোগ নির্ণয়</h2>
              <p className="text-sm text-gray-500 mb-5">
                পাতার ছবি আপলোড করুন — ফসল শনাক্ত করে নির্দিষ্ট রোগ মডেল দিয়ে বিশ্লেষণ করা হবে।
              </p>
              <DetectPanel
                onDetected={(crop, disease) => {
                  setDetectedContext({ crop, disease });
                  setActiveTab("chat");
                }}
              />
            </div>
          ) : (
            <div>
              <h2 className="text-lg font-bold text-gray-800 mb-1">কৃষি পরামর্শ</h2>
              {detectedContext ? (
                <div className="mb-3 px-3 py-2 bg-green-50 border border-green-200 rounded-lg text-xs text-green-700">
                  সনাক্ত: <strong>{detectedContext.crop}</strong> — <strong>{detectedContext.disease}</strong>
                </div>
              ) : null}
              <p className="text-sm text-gray-500 mb-5">
                বাংলায় যেকোনো কৃষি প্রশ্ন করুন — নিরাপত্তা যাচাই, তথ্য সংগ্রহ, উত্তর তৈরি, এবং যাচাইকরণের ধাপগুলো দেখুন।
              </p>
              <QAPanel detectedCrop={detectedContext?.crop} detectedDisease={detectedContext?.disease} />
            </div>
          )}
        </div>
      </main>

      <footer className="text-center text-xs text-gray-400 py-6 border-t border-gray-100">
        KrishokChat Advisory System v0.1 — Safety-aware Bengali Agri-AI • কৃষক কল সেন্টার: ১৬১২৩
      </footer>
    </div>
  );
}
