import {NextResponse,type NextRequest} from 'next/server';
import {serverSupabase} from '@/lib/supabase/server';
import {liveSupabase} from '@/lib/supabase/config';
import {safeDestination} from '@/lib/demo-auth';
export async function GET(request:NextRequest){
 const url=request.nextUrl;
 const next=url.searchParams.get('next');
 const type=url.searchParams.get('type');
 const destination=next==='/reset-password'||type==='recovery'?'/reset-password':!next||next==='/register-school'?'/register-school':safeDestination(next);
 let success=false;
 if(liveSupabase){
  try{
   const client=await serverSupabase();
   const code=url.searchParams.get('code'),hash=url.searchParams.get('token_hash');
   if(code){const {error}=await client.auth.exchangeCodeForSession(code);success=!error}
   else if(hash&&(type==='signup'||type==='email'||type==='recovery')){const {error}=await client.auth.verifyOtp({token_hash:hash,type});success=!error}
   // A reused link may still have a valid session in this browser.
   if(!success){const {data,error}=await client.auth.getUser();success=!error&&!!data.user?.email_confirmed_at}
  }catch{/* Show an actionable recovery screen without exposing tokens or Auth errors. */}
 }
 const target=new URL(success?destination:'/login',request.url);
 if(!success){target.searchParams.set('confirmation','expired');target.searchParams.set('next',destination)}
 const response=NextResponse.redirect(target);
 response.headers.set('Cache-Control','private, no-store');return response;
}
