-- 004_farm_profiles.sql — P1 farm profile (spine step 4, 2026-08-25)
-- Applies to the hosted Supabase project. Idempotent: safe to re-run.
--
-- HOW TO APPLY: Supabase Dashboard -> SQL Editor -> New query -> paste -> Run.
--
-- Scope (P1): one optional farm-profile row per user — primary crop, sowing
-- date, upazila, note. Feeds the P2 stage-aware advice lane. STRICTLY
-- additive on the already-approved non-gating auth lane:
--   * Nothing is gated by profile presence (anonymous demo unchanged).
--   * No multi-tenancy / per-tenant isolation / billing (unchanged rules).
--   * The backend writes/reads with the service-role key; RLS below still
--     enforces owner-only direct client access as defense in depth.
--   * The backend PII-redacts free-text fields (note) before writing.

-- 1. farm_profiles ----------------------------------------------------------

create table if not exists public.farm_profiles (
  user_uuid uuid primary key references auth.users (id) on delete cascade,
  primary_crop text not null,
  sowing_date date,
  upazila text,
  note text,
  updated_at timestamptz not null default now()
);

comment on table public.farm_profiles is
  'P1 optional farm profile (crop, sowing date, upazila, note) — powers stage-aware advice; never gates anything.';

-- 2. RLS: owner-only --------------------------------------------------------

alter table public.farm_profiles enable row level security;

drop policy if exists "farm_profiles owner select" on public.farm_profiles;
create policy "farm_profiles owner select" on public.farm_profiles
  for select to authenticated using (auth.uid() = user_uuid);

drop policy if exists "farm_profiles owner upsert" on public.farm_profiles;
create policy "farm_profiles owner upsert" on public.farm_profiles
  for insert to authenticated with check (auth.uid() = user_uuid);

drop policy if exists "farm_profiles owner update" on public.farm_profiles;
create policy "farm_profiles owner update" on public.farm_profiles
  for update to authenticated using (auth.uid() = user_uuid);
