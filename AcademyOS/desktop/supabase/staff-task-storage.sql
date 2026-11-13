-- Run in the existing AcademyOS project's SQL editor to enable owner uploads.
-- Shared by staff task submissions and school achievement certificates.
-- Uses the existing school-owner policies; this does not activate staff logins.
begin;
insert into storage.buckets(id,name,public,file_size_limit)
values ('staff-task-submissions','staff-task-submissions',false,10485760)
on conflict(id) do update set public=false,file_size_limit=10485760;

drop policy if exists "school_owner_task_file_insert" on storage.objects;
create policy "school_owner_task_file_insert" on storage.objects for insert to authenticated
with check (bucket_id='staff-task-submissions' and exists (
 select 1 from public.academyos_workspaces w
 where w.id::text=(storage.foldername(name))[1] and w.owner_id=(select auth.uid())
));
drop policy if exists "school_owner_task_file_read" on storage.objects;
create policy "school_owner_task_file_read" on storage.objects for select to authenticated
using (bucket_id='staff-task-submissions' and exists (
 select 1 from public.academyos_workspaces w
 where w.id::text=(storage.foldername(name))[1] and w.owner_id=(select auth.uid())
));
commit;
