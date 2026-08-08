import type { Metadata } from "next";
import { Noto_Sans_Bengali, Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const notoBengali = Noto_Sans_Bengali({
  variable: "--font-bengali",
  subsets: ["bengali"],
  weight: ["400", "500", "600", "700"],
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "KrishokChat — কৃষক চ্যাট | Bangladesh Agri-AI Advisory",
  description:
    "Safety-aware Bengali agricultural AI assistant. Ask questions, detect crop diseases, get grounded treatment advice — in Bangla.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="bn" dir="ltr"
          className={`${notoBengali.variable} ${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col font-sans">{children}</body>
    </html>
  );
}
