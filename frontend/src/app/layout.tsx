import type { Metadata, Viewport } from "next";
import { Noto_Sans_Bengali, Tiro_Bangla } from "next/font/google";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/layout/footer";
import { OfflineIndicator } from "@/components/offline-indicator";
import { PwaRegister } from "@/components/pwa-register";
import { LanguageProvider } from "@/context/language-context";
import "./globals.css";

// F4: two families only. Noto Serif Bengali was dropped — it sat behind Tiro
// Bangla in the display fallback chain and never rendered, but its three
// weight files were still shipped (3 wasted font downloads on rural 3G).
// adjustFontFallback:false — the automatic Times/Arial metric adjustment is
// meaningless for Bengali and only adds layout shift during swap.
const notoSansBn = Noto_Sans_Bengali({
  subsets: ["bengali", "latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-bengali-sans",
  display: "swap",
  adjustFontFallback: false,
});

const tiroBangla = Tiro_Bangla({
  subsets: ["bengali", "latin"],
  weight: ["400"],
  variable: "--font-tiro-bangla",
  display: "swap",
  adjustFontFallback: false,
});

export const viewport: Viewport = {
  themeColor: "#2F5D3A",
};

export const metadata: Metadata = {
  title: "কৃষক চ্যাট — KrishokChat | প্রমাণভিত্তিক ও নিরাপদ কৃষি এআই পরামর্শদাতা",
  description:
    "বাংলাদেশের কৃষকদের জন্য নির্ভরযোগ্য এআই কৃষি পরামর্শদাতা — পাতার ছবি থেকে রোগ নির্ণয়, সার ও সেচ ব্যবস্থাপনা এবং সরকারি কৃষি নির্দেশিকাভিত্তিক তথ্য।",
  manifest: "/manifest.webmanifest",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="bn"
      className={`${notoSansBn.variable} ${tiroBangla.variable}`}
    >
      <body className="font-bengali-sans antialiased">
        <LanguageProvider>
          <PwaRegister />
          <OfflineIndicator />
          <div className="min-h-screen flex flex-col">
            <Navbar />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </LanguageProvider>
      </body>
    </html>
  );
}
