"use client";

/* =========================================================================
   AdminShell — sidebar navigation for the /admin ops console (amendment 02).
   Desktop-first (operators, not farmers). Field Notebook styling.
   ========================================================================= */

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Users, Megaphone, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";

const SECTIONS = [
  { href: "/admin", label: "ওভারভিউ", icon: LayoutDashboard, exact: true },
  { href: "/admin/users", label: "ব্যবহারকারী", icon: Users, exact: false },
  { href: "/admin/announcements", label: "ঘোষণা ও সতর্কতা", icon: Megaphone, exact: false },
] as const;

export function AdminShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="mx-auto flex max-w-7xl gap-6 py-8">
      <aside className="sticky top-24 hidden h-fit w-56 shrink-0 rounded-2xl border rule bg-paper p-3 md:block">
        <div className="px-3 pb-2 pt-1 text-sm font-bold text-ink">অ্যাডমিন কনসোল</div>
        <nav aria-label="অ্যাডমিন বিভাগ" className="space-y-0.5">
          {SECTIONS.map(({ href, label, icon: Icon, exact }) => {
            const active = exact ? pathname === href : pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex items-center gap-2.5 rounded-lg px-3 py-2.5 text-sm transition-colors",
                  active ? "bg-leaf/10 font-semibold text-leaf" : "text-ink-soft hover:bg-paper-2",
                )}
              >
                <Icon className="h-4 w-4" aria-hidden />
                {label}
              </Link>
            );
          })}
        </nav>
        <div className="mt-3 border-t rule pt-3">
          <Link
            href="/"
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-xs text-ink-faint transition-colors hover:bg-paper-2 hover:text-ink"
          >
            <ExternalLink className="h-3.5 w-3.5" aria-hidden />
            মূল সাইটে ফিরুন
          </Link>
        </div>
      </aside>

      <div className="min-w-0 flex-1 space-y-6">
        {/* Mobile section nav */}
        <nav aria-label="অ্যাডমিন বিভাগ" className="flex gap-2 overflow-x-auto scrollbar-thin md:hidden">
          {SECTIONS.map(({ href, label, icon: Icon, exact }) => {
            const active = exact ? pathname === href : pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex shrink-0 items-center gap-1.5 rounded-full border rule px-3 py-2 text-sm",
                  active ? "border-leaf bg-leaf/10 font-semibold text-leaf" : "bg-paper text-ink-soft",
                )}
              >
                <Icon className="h-3.5 w-3.5" aria-hidden />
                {label}
              </Link>
            );
          })}
        </nav>
        {children}
      </div>
    </div>
  );
}
