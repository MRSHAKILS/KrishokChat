"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, FlaskConical, BarChart3, ShieldCheck } from "lucide-react";
import { cn } from "@/lib/utils";

const ITEMS = [
  { href: "/research", label: "গবেষণা সারসংক্ষেপ", icon: BookOpen },
  { href: "/research/methodology", label: "কর্পাস ও পদ্ধতি", icon: FlaskConical },
  { href: "/research/benchmark", label: "বেঞ্চমার্ক ফলাফল", icon: BarChart3 },
  { href: "/research/safety", label: "নিরাপত্তা ও গার্ডরেইল", icon: ShieldCheck },
] as const;

export function ResearchSubnav() {
  const pathname = usePathname();

  return (
    <nav
      aria-label="গবেষণা বিভাগ"
      className="sticky top-16 z-40 -mx-5 border-b rule bg-paper/90 px-5 py-2 backdrop-blur-md"
    >
      <div className="mx-auto flex max-w-4xl items-center gap-1 overflow-x-auto scrollbar-thin">
        {ITEMS.map((item) => {
          const active = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={active ? "page" : undefined}
              className={cn(
                "flex min-h-10 shrink-0 items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-medium transition-colors sm:px-4",
                active ? "bg-leaf text-paper shadow-sm" : "text-ink-soft hover:bg-paper-2 hover:text-ink",
              )}
            >
              <Icon className="h-3.5 w-3.5" />
              {item.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
