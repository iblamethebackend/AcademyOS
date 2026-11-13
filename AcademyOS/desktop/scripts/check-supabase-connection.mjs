import fs from 'node:fs';
const env=Object.fromEntries(fs.readFileSync(new URL('../.env.local',import.meta.url),'utf8').split(/\r?\n/).filter(l=>l&&!l.startsWith('#')).map(l=>{const i=l.indexOf('=');return [l.slice(0,i),l.slice(i+1)]}));
const url=env.NEXT_PUBLIC_SUPABASE_URL,key=env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;
for(const path of ['/auth/v1/settings','/rest/v1/academyos_workspaces?select=id&limit=0']){
 try{const r=await fetch(url+path,{headers:{apikey:key,Authorization:'Bearer '+key},signal:AbortSignal.timeout(15000)});const data=await r.json();console.log(JSON.stringify({endpoint:path,status:r.status,...(path.includes('settings')?{emailEnabled:data.external?.email,autoConfirm:data.mailer_autoconfirm}: {code:data.code,message:data.message})}))}catch(e){console.log(JSON.stringify({endpoint:path,error:e.message,cause:e.cause?.code}))}
}
