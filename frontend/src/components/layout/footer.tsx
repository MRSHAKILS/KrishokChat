"use client";

import Link from "next/link";
import { Phone, ExternalLink } from "lucide-react";
import { APP, HELPLINE, LINKS } from "@/lib/constants";
import { useLanguage } from "@/context/language-context";

export function Footer() {
  const { t, locale, formatNumber } = useLanguage();

  const NAV_SECTIONS = [
    {
      title: t.footer.services,
      links: [
        { href: "/chat", label: t.nav.chat },
        { href: "/detect", label: t.nav.detect },
        { href: "/soil", label: t.nav.soil },
        { href: "/analytics", label: t.nav.analytics },
      ],
    },
    {
      title: t.footer.research,
      links: [
        { href: "/research", label: t.nav.research },
        { href: "/screencast", label: t.nav.screencast },
        { href: "/library", label: t.nav.library },
      ],
    },
    {
      title: t.footer.organization,
      links: [
        { href: "/data", label: t.nav.data },
        { href: "/business", label: t.nav.business },
        { href: "/about", label: t.nav.about },
        { href: "/team", label: t.nav.team },
        { href: "/contact", label: t.nav.contact },
      ],
    },
  ];

  const RESOURCES = [
    { href: LINKS.huggingface, label: "Hugging Face" },
    { href: LINKS.github, label: "GitHub" },
  ];

  return (
    <footer className="mt-auto border-t rule bg-paper-2/50">
      <div className="mx-auto max-w-6xl px-5 py-6">
        <div className="grid grid-cols-2 gap-6 sm:grid-cols-4 lg:grid-cols-5">
          {/* Identity — compact */}
          <div className="col-span-2 sm:col-span-1">
            <div className="font-display text-base text-ink">
              {locale === "bn" ? APP.name : APP.nameEn}
            </div>
            <p className="mt-1 text-[11px] leading-tight text-ink-soft">{t.footer.tagline}</p>
            <p className="mt-0.5 text-[10px] text-ink-faint">{t.footer.researchPrototype}</p>
          </div>

          {/* Nav + Resources in one row */}
          {NAV_SECTIONS.map((section) => (
            <div key={section.title}>
              <h3 className="text-[10px] font-semibold text-ink-faint">{section.title}</h3>
              <ul className="mt-2 space-y-1.5">
                {section.links.map((link) => (
                  <li key={link.href}>
                    <Link href={link.href} className="text-xs text-ink-soft transition-colors hover:text-leaf">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {/* Resources + Helpline combined */}
          <div>
            <h3 className="text-[10px] font-semibold text-ink-faint">{t.footer.resources}</h3>
            <ul className="mt-2 space-y-1.5">
              {RESOURCES.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1 text-xs text-ink-soft transition-colors hover:text-leaf"
                  >
                    {link.label}
                    <ExternalLink className="h-2.5 w-2.5" />
                  </a>
                </li>
              ))}
            </ul>
            <div className="mt-3 flex flex-col gap-1">
              <a
                href={`tel:${HELPLINE.krishiCallCenter}`}
                className="flex items-center gap-1 text-xs text-leaf"
                title={t.nav.helplineTitle}
              >
                <Phone className="h-3 w-3" />
                <span className="tabular font-medium">{HELPLINE.krishiCallCenter}</span>
                <span className="text-ink-faint">{t.footer.agriHelpline}</span>
              </a>
              <a href={`tel:${HELPLINE.emergency}`} className="flex items-center gap-1 text-xs text-clay">
                <Phone className="h-3 w-3" />
                <span className="tabular font-medium">{HELPLINE.emergency}</span>
                <span className="text-ink-faint">{t.footer.emergency}</span>
              </a>
            </div>
          </div>
        </div>

        <div className="mt-5 flex flex-col items-center justify-between gap-2 border-t rule pt-3 text-[10px] text-ink-faint sm:flex-row">
          <p>
            © {formatNumber(2026)} {APP.nameEn} · v{APP.version} · {t.footer.copyright}
          </p>
          <Link href="/privacy" className="transition-colors hover:text-leaf">
            {t.footer.privacy}
          </Link>
        </div>
      </div>
    </footer>
  );
}
