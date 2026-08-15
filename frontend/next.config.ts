import type { NextConfig } from "next";

const backendUrl = process.env.BACKEND_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  // The QA stream can take minutes when the local CPU model is selected
  // (llama-server at ~5 tok/s). The Next proxy defaults to a 30s timeout
  // (proxy-request.js: n || 30000) which kills long generations with a
  // "network error" in the browser; raise it to cover local CPU inference.
  experimental: {
    proxyTimeout: 300_000,
  },
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${backendUrl}/api/:path*` },
      { source: "/health", destination: `${backendUrl}/health` },
    ];
  },
};

export default nextConfig;
