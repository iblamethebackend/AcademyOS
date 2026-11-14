import {validSchoolTimezone,validSchoolAddress} from '@/lib/school-timezones';
import {NextResponse,type NextRequest} from 'next/server';
import {cookies} from 'next/headers';
import {workspaceDatabaseError} from '@/lib/workspace-database-error';
import {serverSupabase} from '@/lib/supabase/server';
import {liveSupabase} from '@/lib/supabase/config';
import {validDepartmentConfiguration} from '@/lib/departments';
import {validStaffTaskConfiguration} from '@/lib/staff-tasks';
import {validAchievementConfiguration} from '@/lib/school-achievements';
import {validCampusConfiguration} from '@/lib/campuses';
import {initialState,slugValid,type State} from '@/lib/model';
import {makeRegisteredState,type Registration} from '@/lib/school-registration';
const selectedCookie='academyos-workspace';
function databaseFailure(code?:string){const {status,...body}=workspaceDatabaseError(code);return reply(body,status)}
const reply=(body:unknown,status=200)=>NextResponse.json(body,{status,headers:{'Cache-Control':'private, no-store'}});
function sameOrigin(request:NextRequest){return request.headers.get('origin')===new URL(request.url).origin}
function compatible(sample:unknown,value:unknown):boolean{if(Array.isArray(sample))return Array.isArray(value)&&value.length<=2000&&(sample.length?value.every(v=>compatible(sample[0],v)):value.every(v=>typeof v==='string'));if(sample&&typeof sample==='object')return !!value&&typeof value==='object'&&Object.entries(sample).every(([k,v])=>compatible(v,(value as Record<string,unknown>)[k]));return typeof sample===typeof value}
class AuthUnavailable extends Error {}
function failure(error:unknown,message:string){return error instanceof AuthUnavailable?reply({error:'The server cannot reach Supabase to verify your session. Your school details are still on this page. Start the dev server from your local terminal, then retry.',code:'AUTH_UNAVAILABLE'},503):reply({error:message},503)}
async function identity(){
 if(!liveSupabase)throw new Error('Live Supabase mode is not enabled.');
 const client=await serverSupabase();
 let result:Awaited<ReturnType<typeof client.auth.getUser>>;
 try{result=await client.auth.getUser()}catch{throw new AuthUnavailable()}
 const {data,error}=result;
 if(error&&(error.name==='AuthRetryableFetchError'||error.status===0||(error.status??0)>=500))throw new AuthUnavailable();
 if(error||!data.user)return null;
 return {client,user:data.user};
}
async function selectWorkspace(id:string){const store=await cookies();store.set(selectedCookie,id,{httpOnly:true,sameSite:'lax',secure:process.env.NODE_ENV==='production',path:'/',maxAge:60*60*24*7})}
export async function GET(){try{const identityValue=await identity();if(!identityValue)return reply({error:'Sign in to continue.'},401);const {client}=identityValue;const selected=(await cookies()).get(selectedCookie)?.value;let query=client.from('academyos_workspaces').select('id,slug,school_name,configuration,revision').order('created_at',{ascending:true}).limit(1);if(selected)query=query.eq('id',selected);let {data,error}=await query.maybeSingle();if(!error&&!data&&selected){const fallback=await client.from('academyos_workspaces').select('id,slug,school_name,configuration,revision').order('created_at',{ascending:true}).limit(1).maybeSingle();data=fallback.data;error=fallback.error}if(error)return databaseFailure(error.code);if(!data)return reply({error:'No school workspace is linked to this account.',code:'NO_WORKSPACE'},404);return reply({workspace:data})}catch(error){return failure(error,'Unable to connect to school storage.')}}
export async function POST(request:NextRequest){if(!sameOrigin(request))return reply({error:'Invalid request origin.'},403);try{const value=await identity();if(!value)return reply({error:'Sign in to continue.'},401);const {client,user}=value;const body=await request.json();if(body.action==='select'){if(!slugValid(body.slug||''))return reply({error:'Enter your school workspace code.'},400);const {data,error}=await client.from('academyos_workspaces').select('id').eq('slug',body.slug).maybeSingle();if(error)return databaseFailure(error.code);if(!data)return reply({error:'This account does not have access to that school.'},403);await selectWorkspace(data.id);return reply({ok:true})}
 if(!user.email_confirmed_at)return reply({error:'Verify your owner email before creating a school.'},403);const input=body.school as Registration;if(!input||!['ownerName','name','slug','board','city','phone','address'].every(k=>typeof (input as unknown as Record<string,unknown>)[k]==='string'))return reply({error:'Complete your school details.'},400);if(!slugValid(input.slug)||input.name.trim().length<3||input.ownerName.trim().length<2||!input.city.trim()||!/^[+0-9 ()-]{7,20}$/.test(input.phone))return reply({error:'Check the school name, city, contact number and workspace code.'},400);if((!!input.timezone&&!validSchoolTimezone(input.timezone))||!validSchoolAddress(input.address))return reply({error:'Enter your school address (5-500 characters).'},400);const school={...input,address:input.address.trim(),email:user.email!};const configuration=makeRegisteredState(school);const {data,error}=await client.from('academyos_workspaces').insert({owner_id:user.id,slug:school.slug,school_name:school.name,configuration}).select('id').single();if(error)return databaseFailure(error.code);await selectWorkspace(data.id);return reply({ok:true,id:data.id},201)
 }catch(error){return failure(error,'School creation could not be completed. Please try again.')}}
export async function PATCH(request:NextRequest){if(!sameOrigin(request))return reply({error:'Invalid request origin.'},403);try{const value=await identity();if(!value)return reply({error:'Sign in to continue.'},401);const body=await request.json(),state=body.state as State;if(!compatible(initialState,state)||!validDepartmentConfiguration(state)||!validStaffTaskConfiguration(state)||!validAchievementConfiguration(state)||!validCampusConfiguration(state)||!state.campuses.length||!state.members.length||!state.academic.grades.length||JSON.stringify(state).length>1500000||!Number.isInteger(body.revision))return reply({error:'The school update is incomplete or too large.'},400);const selected=(await cookies()).get(selectedCookie)?.value;if(!selected)return reply({error:'Select your school workspace first.'},400);const {data,error}=await value.client.from('academyos_workspaces').update({configuration:state,school_name:state.school.name,revision:body.revision+1,updated_at:new Date().toISOString()}).eq('id',selected).eq('revision',body.revision).select('revision').maybeSingle();if(error)return databaseFailure(error.code);if(!data)return reply({error:'This workspace changed in another tab. Reload before saving further changes.'},409);return reply({revision:data.revision})}catch(error){return failure(error,'Unable to save school changes.')}}
