'use client';
import {createContext,useContext,useEffect,useState,type ReactNode} from 'react';
import {liveSupabase} from '@/lib/supabase/config';
import {LiveSetupProvider} from './live-setup-context';
import {getDemoSession} from '@/lib/demo-auth';
import {registeredSetupKey,findRegisteredSchool,makeRegisteredState} from '@/lib/school-registration';
import {validDepartmentConfiguration} from '@/lib/departments';
import {validStaffTaskConfiguration} from '@/lib/staff-tasks';
import {validAchievementConfiguration} from '@/lib/school-achievements';
import {validCampusConfiguration} from '@/lib/campuses';
import {initialState,type State,id} from '@/lib/model';
const key='academyos.desktop.setup.v1';
export type SetupStore={state:State;ready:boolean;storageError:boolean;toast:string;notify:(message:string)=>void;update:(change:(s:State)=>State,message:string,invalidate?:boolean)=>void;reset:()=>void;cloud?:boolean;saving?:boolean};
export const SetupContext=createContext<SetupStore|null>(null);
const Context=SetupContext;
function compatible(sample:unknown,value:unknown):boolean{
 if(Array.isArray(sample))return Array.isArray(value)&&value.length<2000&&(sample.length?value.every(v=>compatible(sample[0],v)):value.every(v=>typeof v==='string'));
 if(sample&&typeof sample==='object')return !!value&&typeof value==='object'&&Object.entries(sample).every(([k,v])=>compatible(v,(value as Record<string,unknown>)[k]));
 return typeof sample===typeof value;
}
export function SetupProvider({children}:{children:ReactNode}){return liveSupabase?<LiveSetupProvider>{children}</LiveSetupProvider>:<DemoSetupProvider>{children}</DemoSetupProvider>}
function DemoSetupProvider({children}:{children:ReactNode}){
 const [storageKey,setStorageKey]=useState(key);
 const [state,setState]=useState<State>(initialState),[ready,setReady]=useState(false),[storageError,setStorageError]=useState(false),[toast,notify]=useState('');
 useEffect(()=>{try{const session=getDemoSession();const target=session?.source==='registration'?registeredSetupKey(session.school):key;setStorageKey(target);const raw=localStorage.getItem(target);if(raw){const parsed=JSON.parse(raw);if(parsed.version===1&&compatible(initialState,parsed)&&validDepartmentConfiguration(parsed)&&validStaffTaskConfiguration(parsed)&&validAchievementConfiguration(parsed)&&validCampusConfiguration(parsed))setState(parsed);else notify('The saved preview was incompatible. A fresh demo has been loaded.')}}catch{setStorageError(true)}setReady(true)},[]);
 useEffect(()=>{if(ready)try{localStorage.setItem(storageKey,JSON.stringify(state));setStorageError(false)}catch{setStorageError(true)}},[state,ready,storageKey]);
 useEffect(()=>{if(toast){const timer=setTimeout(()=>notify(''),4500);return()=>clearTimeout(timer)}},[toast]);
 function update(change:(s:State)=>State,message:string,invalidate=true){setState(s=>{const next=change(s);return {...next,checks:invalidate?[]:next.checks,activated:invalidate?false:next.activated,activity:[{id:id(),text:message},...s.activity].slice(0,20)}});notify(message)}
 return <Context.Provider value={{state,ready,storageError,toast,notify,update,reset:()=>{const session=getDemoSession();const owner=session?.source==='registration'?findRegisteredSchool(session.school,session.email):undefined;setState(owner?makeRegisteredState(owner):structuredClone(initialState));notify('Demo workspace reset.')}}}>{children}</Context.Provider>
}
export function useSetup(){const value=useContext(Context);if(!value)throw new Error('SetupProvider missing');return value}
