import Link from "next/link";
import { motion } from "framer-motion";

const features = [
  { icon: "🔬", title: "রোগ নির্ণয়", desc: "পাতার ছবি আপলোড করে ফসল ও রোগ শনাক্ত করুন" },
  { icon: "🛡️", title: "নিরাপত্তা যাচাই", desc: "প্রতিটি প্রশ্ন প্রথমে নিরাপত্তা যাচাই করা হয়" },
  { icon: "📚", title: "তথ্যভিত্তিক", desc: "নির্ভরযোগ্য উৎস থেকে উত্তর দেওয়া হয়" },
  { icon: "💬", title: "বাংলায় কথা বলুন", desc: "বহু প্রশ্নের কথোপকথন সমর্থন করে" },
];

export default function LandingPage() {
  return (
    <div className="space-y-12 py-8">
      <motion.section
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <h1 className="text-4xl sm:text-5xl font-bold text-gray-900">
          বাংলাদেশ কৃষি-এআই
        </h1>
        <p className="text-lg text-gray-500 max-w-2xl mx-auto">
          ফসলের রোগ শনাক্ত করুন, বাংলায় পরামর্শ নিন — নিরাপদ, তথ্যভিত্তিক, সহজে।
        </p>
        <Link
          href="/detect"
          className="inline-block bg-[#1a5632] text-white px-8 py-3 rounded-xl font-semibold hover:bg-[#143d22] transition-colors shadow-lg"
        >
          শুরু করুন
        </Link>
      </motion.section>

      <section className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-3xl mx-auto">
        {features.map((f, i) => (
          <motion.div
            key={f.title}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + i * 0.05 }}
            className="bg-white rounded-xl border border-gray-100 p-5 flex gap-4"
          >
            <span className="text-3xl">{f.icon}</span>
            <div>
              <h3 className="font-bold text-gray-900">{f.title}</h3>
              <p className="text-sm text-gray-500">{f.desc}</p>
            </div>
          </motion.div>
        ))}
      </section>

      <section className="text-center text-sm text-gray-400">
        কৃষক কল সেন্টার: <a href="tel:16123" className="text-green-700 font-semibold">১৬১২৩</a>
      </section>
    </div>
  );
}
