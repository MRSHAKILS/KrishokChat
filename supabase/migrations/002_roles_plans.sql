-- 002_roles_plans.sql — Admin console + user tiers (amendment 02, 2026-08-22)
-- Applies to the hosted Supabase project. Idempotent: safe to re-run.
--
-- HOW TO APPLY: Supabase Dashboard -> SQL Editor -> New query -> paste -> Run.
--
-- Scope (amendment 02):
--   profiles.role  : 'user' | 'admin'  — authorization source of truth.
--                    Checked SERVER-SIDE by the backend on every /api/v1/admin/*
--                    request via the service-role key. UI guards are cosmetic only.
--   profiles.plan  : 'free' | 'premium' — tier label. NOTHING is gated by plan
--                    (researcher decision 2026-08-22: "no gating now").
--   admin_actions  : audit of every admin mutation (actor, action, target, payload).
--
-- Still forbidden and NOT introduced here: multi-tenancy, per-tenant isolation,
-- billing. The backend writes profile rows with the service-role key (bypasses
-- RLS); RLS below protects direct client access only.

-- 1. profiles: role + plan (+ updated_at) --------------------------------

alter table public.profiles
  add column if not exists role text not null default 'user';
alter table public.profiles
  add column if not exists plan text not null default 'free';
alter table public.profiles
  add column if not exists updated_at timestamptz not null default now();

do $$ begin
  alter table public.profiles
    add constraint profiles_role_check check (role in ('user', 'admin'));
exception when duplicate_object then null; end $$;

do $$ begin
  alter table public.profiles
    add constraint profiles_plan_check check (plan in ('free', 'premium'));
exception when duplicate_object then null; end $$;

-- 2. is_admin(): SECURITY DEFINER helper for RLS policies ------------------
-- A policy on profiles that subqueries profiles would recurse; a security
-- definer function owned by postgres avoids that (standard Supabase pattern).

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'admin'
  );
$$;

-- 2b. keep updated_at fresh on any profile row change (service-role patches
--      cannot call SQL functions through PostgREST JSON bodies, so a trigger
--      owns this column).

create or replace function public.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists profiles_touch_updated_at on public.profiles;
create trigger profiles_touch_updated_at
  before update on public.profiles
  for each row execute function public.touch_updated_at();

-- 3. profiles RLS: admins may read all rows (owners already can, 001) ------
-- Writes stay service-role only: the owner policy from 001 keeps `for all`
-- scoped to id = auth.uid(); no client role/plan escalation path exists.

drop policy if exists profiles_admin_select on public.profiles;
create policy profiles_admin_select on public.profiles
  for select to authenticated
  using (public.is_admin());

-- 4. admin_actions table ---------------------------------------------------

create table if not exists public.admin_actions (
  id          uuid primary key default gen_random_uuid(),
  actor_id    uuid not null references auth.users(id) on delete cascade,
  action      text not null,
  target_type text not null default '',
  target_id   text not null default '',
  payload     jsonb not null default '{}'::jsonb,
  created_at  timestamptz not null default now()
);

create index if not exists admin_actions_created_idx
  on public.admin_actions (created_at desc);

alter table public.admin_actions enable row level security;

-- Reads: admins only. Writes: service-role only (no insert/update/delete
-- policies means authenticated/anon clients can never touch this table).

drop policy if exists admin_actions_admin_select on public.admin_actions;
create policy admin_actions_admin_select on public.admin_actions
  for select to authenticated
  using (public.is_admin());
