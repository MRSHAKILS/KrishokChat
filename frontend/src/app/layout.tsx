import type { Metadata } from "next";
import { Noto_Sans_Bengali, Noto_Serif_Bengali } from "next/font/google";
import "./globals.css";

const bengaliSans = Noto_Sans_Bengali({
  subsets: ["bengali", "latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-bengali-sans",
  display: "swap",
});

const bengaliSerif = Noto_Serif_Bengali({
  subsets: ["bengali"],
  weight: ["400", "600", "700"],
  variable: "--font-bengali-serif",
  display: "swap",
});

export const metadata: Metadata = {
  title: "কৃষক চ্যাট — KrishokChat | Bangladesh Agri-AI Advisory",
  description: "Safety-aware Bengali agricultural AI assistant. Detect crop diseases from leaf images, get grounded treatment advice in Bangla.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="bn" className={`${bengaliSans.variable} ${bengaliSerif.variable}`}>
      <body className="font-bengali-sans antialiased bg-gray-50 text-gray-900">{children}</body>
    </html>
  );
}
