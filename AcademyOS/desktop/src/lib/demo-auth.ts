/** UI-only navigation state. This is not authentication or an authorization boundary. */
import {findRegisteredSchool,type RegisteredSchool} from './school-registration';
export const DEMO_LOGIN={school:'greenfield',email:'ananya@greenfield.example',password:'Academy@2026'} as const;
export const SESSION_KEY='academyos.demo-session.v1';
export type DemoSession={version:1;email:string;role:'school-admin';school:string;expiresAt:number;source?:'registration'};
let memorySession:DemoSession|null=null;
export function getDemoSession():DemoSession|null{
 if(typeof window==='undefined')return null;
 for(const storage of ['sessionStorage','localStorage'] as const){try{const raw=window[storage].getItem(SESSION_KEY);if(!raw)continue;const value=JSON.parse(raw);const known=value.source==='registration'?!!findRegisteredSchool(value.school,value.email):value.email===DEMO_LOGIN.email&&value.school===DEMO_LOGIN.school;if(value.version===1&&known&&value.role==='school-admin'&&typeof value.expiresAt==='number'&&value.expiresAt>Date.now()){memorySession=value;return value}window[storage].removeItem(SESSION_KEY)}catch{/* Storage may be disabled; use this tab's in-memory preview. */}}
 return memorySession&&memorySession.expiresAt>Date.now()?memorySession:null;
}
export function startDemoSession(remember:boolean,owner?:RegisteredSchool){
 const session:DemoSession={version:1,email:owner?.email||DEMO_LOGIN.email,role:'school-admin',school:owner?.slug||DEMO_LOGIN.school,expiresAt:Date.now()+(remember?7*24:8)*60*60*1000,...(owner?{source:'registration' as const}:{})};
 clearDemoSession();memorySession=session;
 try{(remember?localStorage:sessionStorage).setItem(SESSION_KEY,JSON.stringify(session));return true}catch{return false}
}
export function clearDemoSession(){memorySession=null;for(const storage of ['sessionStorage','localStorage'] as const){try{window[storage].removeItem(SESSION_KEY)}catch{/* No persistent data is available. */}}}
export function safeDestination(value:unknown){if(value==='/dashboard')return '/workspace';return typeof value==='string'&&(value==='/register-school'||value==='/dashboard'||/^\/workspace(?:\/(school|campuses|academics|people|departments|branding|launch|settings))?$/.test(value)||/^\/setup(?:\/(school|academics|people|branding|launch|lifecycle))?$/.test(value))?value:'/workspace'}
