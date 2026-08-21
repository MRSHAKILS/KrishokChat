import Link from "next/link";
import { Phone, ExternalLink } from "lucide-react";
import { APP, HELPLINE, LINKS } from "@/lib/constants";

const NAV_SECTIONS = [
  { title: "সেবাসমূহ", links: [{ href: "/chat", label: "কৃষি পরামর্শ চ্যাট" }, { href: "/detect", label: "ফসলের রোগ নির্ণয়" }, { href: "/soil", label: "মাটি ও সেচ" }, { href: "/analytics", label: "লাইভ পরিসংখ্যান" }] },
  { title: "গবেষণা", links: [{ href: "/research", label: "গবেষণা বিবরণ" }, { href: "/research/safety", label: "নিরাপত্তা কাঠামো" }, { href: "/research/benchmark", label: "বেঞ্চমার্ক ফলাফল" }, { href: "/library", label: "রিসোর্স লাইব্রেরি" }] },
  { title: "প্রতিষ্ঠান ও দল", links: [{ href: "/data", label: "উপাত্ত ও নলেজ গ্রাফ" }, { href: "/business", label: "ব্যবসায়িক মডেল" }, { href: "/about", label: "প্রকল্প পরিচিতি" }, { href: "/team", label: "গবেষক দল" }, { href: "/contact", label: "সাহায্য ও যোগাযোগ" }] },
];

const RESOURCES = [
  { href: LINKS.huggingface, label: "Hugging Face" },
  { href: LINKS.github, label: "GitHub" },
];

export function Footer() {
  return (
    <footer className="mt-auto border-t rule bg-paper-2/50">
      <div className="mx-auto max-w-6xl px-5 py-6">
        <div className="grid grid-cols-2 gap-6 sm:grid-cols-4 lg:grid-cols-5">
          {/* Identity — compact */}
          <div className="col-span-2 sm:col-span-1">
            <div className="font-display text-base text-ink">{APP.name}</div>
            <p className="mt-1 text-[11px] leading-tight text-ink-soft">{APP.tagline}</p>
            <p className="mt-0.5 text-[10px] text-ink-faint">গবেষণা প্রোটোটাইপ — CC-BY-4.0</p>
          </div>

          {/* Nav + Resources in one row */}
          {NAV_SECTIONS.map((section) => (
            <div key={section.title}>
              <h3 className="text-[10px] font-semibold text-ink-faint">{section.title}</h3>
              <ul className="mt-2 space-y-1.5">
                {section.links.map((link) => (
                  <li key={link.href}>
                    <Link href={link.href} className="text-xs text-ink-soft transition-colors hover:text-leaf">{link.label}</Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {/* Resources + Helpline combined */}
          <div>
            <h3 className="text-[10px] font-semibold text-ink-faint">সম্পদ</h3>
            <ul className="mt-2 space-y-1.5">
              {RESOURCES.map((link) => (
                <li key={link.href}>
                  <a href={link.href} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 text-xs text-ink-soft transition-colors hover:text-leaf">
                    {link.label}<ExternalLink className="h-2.5 w-2.5" />
                  </a>
                </li>
              ))}
            </ul>
            <div className="mt-3 flex flex-col gap-1">
              <a href={`tel:${HELPLINE.krishiCallCenter}`} className="flex items-center gap-1 text-xs text-leaf">
                <Phone className="h-3 w-3" /><span className="tabular font-medium">{HELPLINE.krishiCallCenter}</span>
                <span className="text-ink-faint">কৃষি হেল্পলাইন</span>
              </a>
              <a href={`tel:${HELPLINE.emergency}`} className="flex items-center gap-1 text-xs text-clay">
                <Phone className="h-3 w-3" /><span className="tabular font-medium">{HELPLINE.emergency}</span>
                <span className="text-ink-faint">জরুরি</span>
              </a>
            </div>
          </div>
        </div>

        <div className="mt-5 flex flex-col items-center justify-between gap-2 border-t rule pt-3 text-[10px] text-ink-faint sm:flex-row">
          <p>© ২০২৬ {APP.nameEn} · v{APP.version} · North South University</p>
          <Link href="/privacy" className="transition-colors hover:text-leaf">
            গোপনীয়তা নীতি · Privacy
          </Link>
        </div>
      </div>
    </footer>
  );
}
