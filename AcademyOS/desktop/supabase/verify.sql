-- Read-only checks to run after applying schema.sql to the intended project.
select current_database(), current_user;
select schemaname, tablename, rowsecurity
from pg_tables where schemaname='public' and tablename='academyos_workspaces';
select policyname,cmd,roles,qual,with_check
from pg_policies where schemaname='public' and tablename='academyos_workspaces';
select grantee,privilege_type from information_schema.role_table_grants
where table_schema='public' and table_name='academyos_workspaces';
select grantee,column_name,privilege_type from information_schema.role_column_grants
where table_schema='public' and table_name='academyos_workspaces' and privilege_type='UPDATE';
