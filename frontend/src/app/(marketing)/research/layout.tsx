import { ResearchSubnav } from "@/components/layout/research-subnav";

export default function ResearchLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ResearchSubnav />
      {children}
    </>
  );
}
