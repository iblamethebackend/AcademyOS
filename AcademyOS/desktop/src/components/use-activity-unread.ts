'use client';
import {useEffect,useState} from 'react';

export function useActivityUnread(scope:string,activity:{id:string}[],viewing:boolean){
 const [seen,setSeen]=useState<{scope:string;ids:string[]}|null>(null);
 const key='academyos.activity-seen.v1:'+scope;
 useEffect(()=>{
  let ids:string[]=[];
  try{const stored=JSON.parse(localStorage.getItem(key)||'[]');if(Array.isArray(stored))ids=stored.filter(id=>typeof id==='string').slice(0,100)}catch{/* Use this tab's read state if storage is unavailable. */}
  setSeen({scope,ids});
 },[key,scope]);
 useEffect(()=>{
  if(!viewing||seen?.scope!==scope)return;
  const ids=activity.map(item=>item.id);
  if(ids.every(id=>seen.ids.includes(id)))return;
  setSeen({scope,ids});
  try{localStorage.setItem(key,JSON.stringify(ids))}catch{/* The badge still clears in this tab. */}
 },[activity,viewing,seen,scope,key]);
 return !!seen&&seen.scope===scope&&activity.some(item=>!seen.ids.includes(item.id));
}
