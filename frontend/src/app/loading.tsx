import { motion } from "framer-motion";

export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <motion.div
        className="w-12 h-12 border-4 border-green-200 border-t-green-600 rounded-full"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      />
      <div className="text-sm text-gray-500 animate-pulse">লোড হচ্ছে...</div>
    </div>
  );
}
