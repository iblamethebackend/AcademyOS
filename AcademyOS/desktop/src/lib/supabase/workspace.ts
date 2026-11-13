import type {State} from '@/lib/model';
import type {Registration} from '@/lib/school-registration';
export type CloudWorkspace={id:string;slug:string;school_name:string;configuration:State;revision:number};
export async function workspaceRequest<T>(method='GET',body?:unknown,signal?:AbortSignal):Promise<T>{const response=await fetch('/api/workspace',{method,headers:body?{'Content-Type':'application/json'}:undefined,body:body?JSON.stringify(body):undefined,cache:'no-store',signal});const data=await response.json();if(!response.ok)throw new Error(data.error||'Unable to access your school workspace.');return data}
export async function loadCloudWorkspace(signal?:AbortSignal){return (await workspaceRequest<{workspace:CloudWorkspace}>('GET',undefined,signal)).workspace}
export async function createCloudWorkspace(school:Registration){return workspaceRequest<{id:string}>('POST',{school})}
export async function selectCloudWorkspace(slug:string){return workspaceRequest('POST',{action:'select',slug:slug.trim().toLowerCase()})}
