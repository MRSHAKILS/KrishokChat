-- 001_saved_history.sql — Premium lane (P4 design doc, decision 1: saved history)
-- Applies to the hosted Supabase project (or any future project at deployment).
--
-- HOW TO APPLY: Supabase Dashboard -> SQL Editor -> New query -> paste -> Run.
-- Idempotent: safe to re-run.
--
-- NOTE: the backend uses the service-role key (bypasses RLS) and enforces
-- ownership in application code; RLS below additionally protects the data
-- from direct client access. This is per-user isolation, not multi-tenancy.

-- gen_random_uuid() (built into PostgreSQL 13+; extension call kept for older hosts)
create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  email       text not null default '',
  display_name text,
  created_at  timestamptz not null default now()
);

create table if not exists public.saved_queries (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  query_text  text not null,
  answer_text text not null,
  sources     jsonb not null default '[]'::jsonb,
  category    text not null default '',
  created_at  timestamptz not null default now()
);

create index if not exists saved_queries_user_created_idx
  on public.saved_queries (user_id, created_at desc);

alter table public.profiles enable row level security;
alter table public.saved_queries enable row level security;

drop policy if exists profiles_owner_all on public.profiles;
create policy profiles_owner_all on public.profiles
  for all to authenticated
  using (id = auth.uid())
  with check (id = auth.uid());

drop policy if exists saved_queries_owner_select on public.saved_queries;
create policy saved_queries_owner_select on public.saved_queries
  for select to authenticated
  using (user_id = auth.uid());

drop policy if exists saved_queries_owner_insert on public.saved_queries;
create policy saved_queries_owner_insert on public.saved_queries
  for insert to authenticated
  with check (user_id = auth.uid());

drop policy if exists saved_queries_owner_delete on public.saved_queries;
create policy saved_queries_owner_delete on public.saved_queries
  for delete to authenticated
  using (user_id = auth.uid());