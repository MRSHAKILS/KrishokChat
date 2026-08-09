import { getSafetyMetrics, SafetyMetrics } from "@/lib/api";
import { motion } from "framer-motion";

export const dynamic = "force-dynamic";

export default async function AnalyticsPage() {
  let metrics: SafetyMetrics | null = null;
  try {
    metrics = await getSafetyMetrics();
  } catch {
    metrics = { total_queries: 0, by_category: {}, flagged_count: 0, recent: [] };
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">পরিসংখ্যান</h1>
        <p className="text-sm text-gray-500 mt-1">
          নিরাপত্তা যাচাই ও প্রশ্নের বিশ্লেষণ।
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="bg-white rounded-xl border border-gray-100 p-5">
          <div className="text-3xl font-bold text-[#1a5632]">{metrics.total_queries}</div>
          <div className="text-sm text-gray-500">মোট প্রশ্ন</div>
        </motion.div>
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }} className="bg-white rounded-xl border border-gray-100 p-5">
          <div className="text-3xl font-bold text-green-600">{metrics.by_category?.safe_agri ?? 0}</div>
          <div className="text-sm text-gray-500">কৃষি প্রশ্ন</div>
        </motion.div>
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="bg-white rounded-xl border border-gray-100 p-5">
          <div className="text-3xl font-bold text-red-500">{metrics.flagged_count}</div>
          <div className="text-sm text-gray-500">অবরুদ্ধ</div>
        </motion.div>
      </div>

      {metrics.recent?.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-100 p-5">
          <h2 className="font-bold text-gray-900 mb-3">সাম্প্রতিক প্রশ্ন</h2>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {metrics.recent.map((r, i) => (
              <div key={i} className="flex items-center justify-between text-sm border-b border-gray-50 py-2">
                <span className="text-gray-700 truncate max-w-[60%]">{r.query}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${r.category === "safe_agri" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
                  {r.category}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
