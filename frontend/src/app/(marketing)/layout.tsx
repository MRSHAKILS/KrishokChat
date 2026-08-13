import CommandMenu from "@/components/command-menu";

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto w-full max-w-6xl px-5">
      {children}
      <CommandMenu />
    </div>
  );
}
