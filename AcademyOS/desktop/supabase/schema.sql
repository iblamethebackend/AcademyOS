-- AcademyOS foundation. Run once on the intended project using its SQL editor.
-- This script is additive. It does not import local demo data or create users.
begin;
create table if not exists public.academyos_workspaces (
 id uuid primary key default gen_random_uuid(),
 owner_id uuid not null references auth.users(id) on delete restrict,
 slug text not null unique check (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$' and length(slug) between 3 and 40),
 school_name text not null check (length(trim(school_name)) between 3 and 100),
 configuration jsonb not null check (jsonb_typeof(configuration)='object' and configuration->>'version'='1'),
 revision integer not null default 1 check (revision>0),
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 constraint workspace_slug_matches_configuration check (configuration->'school'->>'slug'=slug)
);
create index if not exists academyos_workspaces_owner_idx on public.academyos_workspaces(owner_id);
alter table public.academyos_workspaces enable row level security;
revoke all on public.academyos_workspaces from anon;
revoke all on public.academyos_workspaces from authenticated;
grant select,insert on public.academyos_workspaces to authenticated;
grant update (school_name,configuration,revision,updated_at) on public.academyos_workspaces to authenticated;
-- Owners can create and edit their own school only. No role comes from user_metadata.
drop policy if exists "owner_read" on public.academyos_workspaces;
create policy "owner_read" on public.academyos_workspaces for select to authenticated using ((select auth.uid())=owner_id);
drop policy if exists "owner_create" on public.academyos_workspaces;
create policy "owner_create" on public.academyos_workspaces for insert to authenticated with check ((select auth.uid())=owner_id);
drop policy if exists "owner_update" on public.academyos_workspaces;
create policy "owner_update" on public.academyos_workspaces for update to authenticated using ((select auth.uid())=owner_id) with check ((select auth.uid())=owner_id);
-- Actual deletion is deliberately unavailable. Lifecycle screens change settings only.
commit;
