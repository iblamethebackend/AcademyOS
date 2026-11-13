import {createServerClient} from '@supabase/ssr';
import {NextResponse,type NextRequest} from 'next/server';
import {liveSupabase,supabaseConfig} from '@/lib/supabase/config';
export async function proxy(request:NextRequest){
 if(!liveSupabase)return NextResponse.next();
 let response=NextResponse.next({request});
 const {url,key}=supabaseConfig();
 const client=createServerClient(url,key,{
  cookies:{
   getAll:()=>request.cookies.getAll(),
   setAll:(values,headers)=>{
    values.forEach(({name,value})=>request.cookies.set(name,value));
    response=NextResponse.next({request});
    values.forEach(({name,value,options})=>response.cookies.set(name,value,options));
    Object.entries(headers).forEach(([name,value])=>response.headers.set(name,value));
   }
  }
 });
 let authenticated=false;
 try{const {data,error}=await client.auth.getUser();authenticated=!!data.user&&!error}
 catch{/* Fail closed when the Auth service is unavailable. */}
 const protectedPath=/^\/(workspace|setup|dashboard)(\/|$)/.test(request.nextUrl.pathname);
 if(protectedPath&&!authenticated){
  const target=new URL('/login',request.url);target.searchParams.set('next',request.nextUrl.pathname);
  const redirect=NextResponse.redirect(target);
  response.cookies.getAll().forEach(c=>redirect.cookies.set(c));
  redirect.headers.set('Cache-Control','private, no-store');return redirect;
 }
 response.headers.set('Cache-Control','private, no-store');return response;
}
export const config={matcher:['/workspace/:path*','/setup/:path*','/dashboard/:path*','/login','/register-school','/reset-password','/auth/:path*','/api/workspace/:path*']};
