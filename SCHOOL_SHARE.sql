-- THE PLAYBOOK — one-time SQL for teacher → parent school notes
-- Open https://supabase.com → your project → SQL Editor → New query → paste this → Run
-- Needed so a teacher on a different phone can send a note into your app.

create table if not exists public.playbook_share_links (
  token text primary key,
  user_id uuid,
  label text,
  child_label text,
  created_at timestamptz not null default now(),
  active boolean not null default true
);

create table if not exists public.playbook_school_notes (
  id uuid primary key default gen_random_uuid(),
  token text not null,
  child text,
  note_date date,
  mood text,
  energy text,
  incidents text,
  wins text,
  body text,
  author_name text default 'Teacher',
  role text default 'Teacher',
  created_at timestamptz not null default now()
);

create index if not exists playbook_school_notes_token_idx
  on public.playbook_school_notes (token, created_at desc);

alter table public.playbook_share_links enable row level security;
alter table public.playbook_school_notes enable row level security;

drop policy if exists "share_links_select" on public.playbook_share_links;
create policy "share_links_select" on public.playbook_share_links
  for select using (true);

drop policy if exists "share_links_insert" on public.playbook_share_links;
create policy "share_links_insert" on public.playbook_share_links
  for insert with check (true);

drop policy if exists "share_links_update" on public.playbook_share_links;
create policy "share_links_update" on public.playbook_share_links
  for update using (true);

drop policy if exists "school_notes_select" on public.playbook_school_notes;
create policy "school_notes_select" on public.playbook_school_notes
  for select using (true);

drop policy if exists "school_notes_insert" on public.playbook_school_notes;
create policy "school_notes_insert" on public.playbook_school_notes
  for insert with check (
    exists (
      select 1 from public.playbook_share_links s
      where s.token = playbook_school_notes.token
        and s.active = true
    )
  );

grant select, insert, update on public.playbook_share_links to anon, authenticated;
grant select, insert on public.playbook_school_notes to anon, authenticated;
