import Link from "next/link";
import { motion } from "framer-motion";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-6 px-4 text-center">
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="text-8xl font-bold text-green-600"
      >
        404
      </motion.div>
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-2">পাতা পাওয়া যায়নি</h2>
        <p className="text-sm text-gray-500">
          আপনি যে পাতাটি খুঁজছেন সেটি পাওয়া যায়নি।
        </p>
      </div>
      <Link
        href="/detect"
        className="bg-[#1a5632] text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-[#143d22] transition-colors"
      >
        হোমে ফিরে যান
      </Link>
    </div>
  );
}
