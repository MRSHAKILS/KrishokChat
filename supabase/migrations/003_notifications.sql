-- 003_notifications.sql — Broadcast announcements & disease alerts (amendment 02)
-- Applies to the hosted Supabase project. Idempotent: safe to re-run.
--
-- HOW TO APPLY: Supabase Dashboard -> SQL Editor -> New query -> paste -> Run.
--
-- Design:
--   announcements       — admin-composed Bengali notifications. kind:
--                          announcement | disease_alert | maintenance
--                          severity: info | warning | urgent
--                          audience: all (incl. anonymous visitors — a farmer
--                          who never signs up still gets disease alerts; this
--                          is additive content, not gating) | free | premium
--   announcement_reads  — per-user read state. Anonymous visitors keep read
--                          state in localStorage on their device.
--
-- RLS: everyone (anon + authenticated) can READ published, unexpired rows.
-- Writes are service-role only (backend admin API, which itself verifies the
-- caller's profiles.role='admin' on every request — amendment 02 §4).

create extension if not exists pgcrypto;

create table if not exists public.announcements (
  id            uuid primary key default gen_random_uuid(),
  kind          text not null default 'announcement',
  severity      text not null default 'info',
  title_bn      text not null,
  body_bn       text not null,
  crop          text not null default '',
  audience      text not null default 'all',
  cta_url       text not null default '',
  published     boolean not null default false,
  published_at  timestamptz,
  expires_at    timestamptz,
  created_by    uuid references auth.users(id) on delete set null,
  created_at    timestamptz not null default now()
);

do $$ begin
  alter table public.announcements
    add constraint announcements_kind_check check (kind in ('announcement', 'disease_alert', 'maintenance'));
exception when duplicate_object then null; end $$;

do $$ begin
  alter table public.announcements
    add constraint announcements_severity_check check (severity in ('info', 'warning', 'urgent'));
exception when duplicate_object then null; end $$;

do $$ begin
  alter table public.announcements
    add constraint announcements_audience_check check (audience in ('all', 'free', 'premium'));
exception when duplicate_object then null; end $$;

create index if not exists announcements_live_idx
  on public.announcements (published, published_at desc)
  where published;

alter table public.announcements enable row level security;

-- Everyone (including anon) reads published rows. Expiry and audience
-- filtering happen in the backend query (audience needs the caller's plan).
drop policy if exists announcements_public_select on public.announcements;
create policy announcements_public_select on public.announcements
  for select
  using (published);

create table if not exists public.announcement_reads (
  user_id         uuid not null references auth.users(id) on delete cascade,
  announcement_id uuid not null references public.announcements(id) on delete cascade,
  read_at         timestamptz not null default now(),
  primary key (user_id, announcement_id)
);

alter table public.announcement_reads enable row level security;

-- Owners manage their own read state; no client writes anywhere else.
drop policy if exists announcement_reads_owner_all on public.announcement_reads;
create policy announcement_reads_owner_all on public.announcement_reads
  for all to authenticated
  using (user_id = auth.uid())
  with check (user_id = auth.uid());
