import {NextResponse} from 'next/server';
import {workspaceDatabaseError} from '@/lib/workspace-database-error';
import {supabaseConfig} from '@/lib/supabase/config';
export async function GET(){
 const checks:{auth:boolean;workspaceTable:boolean;anonymousAccessBlocked:boolean}={auth:false,workspaceTable:false,anonymousAccessBlocked:false};
 try{
  const {url,key}=supabaseConfig();const headers={apikey:key,Authorization:'Bearer '+key};
  const auth=await fetch(url+'/auth/v1/settings',{headers,cache:'no-store',signal:AbortSignal.timeout(10000)});
  if(!auth.ok)return NextResponse.json({connected:false,checks,error:'Supabase rejected the public connection. Check the project URL and public key.'},{status:503,headers:{'Cache-Control':'no-store'}});
  checks.auth=true;
  const table=await fetch(url+'/rest/v1/academyos_workspaces?select=id&limit=0',{headers,cache:'no-store',signal:AbortSignal.timeout(10000)});const data=await table.json();
  // The schema deliberately gives the anonymous role no table access.
  // A Postgres permission-denied response confirms the table is exposed but protected.
  checks.workspaceTable=data.code==='42501';checks.anonymousAccessBlocked=data.code==='42501';
  const connected=checks.auth&&checks.workspaceTable&&checks.anonymousAccessBlocked;
  return NextResponse.json({connected,checks,databaseStatus:table.status,databaseCode:typeof data.code==='string'?data.code:null,...(!connected?{error:table.ok?'Anonymous table access is unexpectedly permitted. Reapply the schema grants.':workspaceDatabaseError(data.code).error}:{})},{status:connected?200:503,headers:{'Cache-Control':'no-store'}});
 }catch(e){const code=(e as Error&{cause?:{code?:string}}).cause?.code;return NextResponse.json({connected:false,checks,error:code==='EACCES'?'This server is blocked from reaching Supabase. Start the development server from an unrestricted local terminal.':'The server could not reach Supabase. Check network access and project availability.'},{status:503,headers:{'Cache-Control':'no-store'}})}
}
