'use client';
import {browserSupabase} from './supabase/browser';
import {loadCloudWorkspace} from './supabase/workspace';
import {validSubmissionFile,type TaskAttachment} from './staff-tasks';

const bucket='staff-task-submissions';
function localFiles():Promise<IDBDatabase>{return new Promise((resolve,reject)=>{
 const request=indexedDB.open('academyos.staff-task-files.v1',1);
 request.onupgradeneeded=()=>request.result.createObjectStore('files');
 request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(new Error('File storage is unavailable in this browser.'));
})}
async function saveLocal(path:string,file:File){const db=await localFiles();try{await new Promise<void>((resolve,reject)=>{const tx=db.transaction('files','readwrite');tx.objectStore('files').put(file,path);tx.oncomplete=()=>resolve();tx.onerror=()=>reject(new Error('The file could not be saved. Check available browser storage.'));tx.onabort=()=>reject(new Error('The file could not be saved.'))})}finally{db.close()}}
export async function uploadTaskFile(file:File,taskId:string,schoolSlug:string,cloud:boolean):Promise<TaskAttachment>{
 if(!validSubmissionFile(file))throw new Error('Choose a PDF, CSV, TXT, DOCX, XLSX or image file, up to 10 MB.');
 const fileId=crypto.randomUUID(),extension=file.name.split('.').pop()!.toLowerCase();
 let path=schoolSlug+'/'+taskId+'/'+fileId+'.'+extension;
 if(cloud){const workspace=await loadCloudWorkspace();path=workspace.id+'/'+taskId+'/'+fileId+'.'+extension;const {error}=await browserSupabase().storage.from(bucket).upload(path,file,{upsert:false,contentType:file.type||'application/octet-stream'});if(error)throw new Error('The file was not uploaded. Check your connection and ask your administrator to configure school file storage.');}
 else await saveLocal(path,file);
 return {id:fileId,name:file.name,size:file.size,type:file.type,path,storage:cloud?'cloud':'local'};
}
export async function readSchoolFile(attachment:TaskAttachment){
 let blob:Blob;
 if(attachment.storage==='cloud'){const {data,error}=await browserSupabase().storage.from(bucket).download(attachment.path);if(error||!data)throw new Error('The file could not be downloaded. Check your school access and connection.');blob=data;}
 else {const db=await localFiles();try{blob=await new Promise<Blob>((resolve,reject)=>{const request=db.transaction('files').objectStore('files').get(attachment.path);request.onsuccess=()=>request.result?resolve(request.result):reject(new Error('This file is not available in this browser. Ask for a new upload.'));request.onerror=()=>reject(new Error('The file could not be read.'))})}finally{db.close()}}
 return blob;
}
export async function downloadTaskFile(attachment:TaskAttachment){
 const blob=await readSchoolFile(attachment);
 const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=attachment.name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
