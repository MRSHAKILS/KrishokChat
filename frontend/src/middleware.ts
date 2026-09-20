/**
 * Vercel compatibility shim: Vercel's edge routing infrastructure still
 * expects the classic `middleware.ts` export shape (function named `middleware`
 * + `config.matcher`). Next.js 16 introduced `proxy.ts` as the new canonical
 * name, but Vercel's CDN layer reads the compiled output looking for
 * `middleware.js` — without it, every request returns Vercel's own 404.
 *
 * This file re-exports the session-refresh logic from proxy.ts under the
 * `middleware` name so both Next.js 16 (proxy.ts) and Vercel (middleware.ts)
 * are satisfied simultaneously.
 */
export { proxy as middleware, config } from "./proxy";
