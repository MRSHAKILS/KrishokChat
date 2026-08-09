export default function AppLayout({ children }: { children: React.ReactNode }) {
  return <div className="mx-auto w-full max-w-6xl px-5 py-8">{children}</div>;
}
