import type { NextConfig } from "next";

const backendUrl = process.env.BACKEND_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  // P6: standalone output for Docker when not on Vercel. Vercel natively optimizes output.
  output: process.env.VERCEL ? undefined : "standalone",
  // The QA stream can take minutes when the local CPU model is selected
  // (llama-server at ~5 tok/s). The Next proxy defaults to a 30s timeout
  // (proxy-request.js: n || 30000) which kills long generations with a
  // "network error" in the browser; raise it to cover local CPU inference.
  experimental: {
    proxyTimeout: 300_000,
    optimizePackageImports: ["lucide-react", "motion", "@base-ui/react"],
  },
  // P0-8: baseline security headers on every route. Permissions-Policy
  // deliberately omits microphone/camera — the voice-input demo must keep
  // working. (No custom Cache-Control here: Next 16 already serves
  // /_next/static with its own immutable headers, and overriding them
  // trips the dev-mode warning in next.config validation.)
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "no-referrer" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "Permissions-Policy", value: "geolocation=(), payment=()" },
        ],
      },
    ];
  },
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${backendUrl}/api/:path*` },
      { source: "/health", destination: `${backendUrl}/health` },
    ];
  },
};

export default nextConfig;
