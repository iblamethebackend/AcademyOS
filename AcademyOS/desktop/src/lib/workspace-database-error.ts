export function workspaceDatabaseError(code?:string){
 if(['PGRST000','PGRST001','PGRST002','PGRST003'].includes(code||''))return {status:503,error:'School storage is temporarily unavailable. Your details are still on this page. Please retry once the database connection has recovered.',code};
 if(code==='PGRST205'||code==='42P01')return {status:503,error:'School storage has not been set up. The AcademyOS workspace table needs to be created in Supabase.',code};
 if(code==='42501')return {status:403,error:'School storage permissions are preventing this action. Check the workspace table grants and owner policies in Supabase.',code};
 if(code==='23505')return {status:409,error:'This school workspace address is already taken. Choose another address.',code};
 if(code==='23514'||code==='23502')return {status:400,error:'The school details do not match the database requirements. Check the workspace schema and your school details.',code};
 return {status:503,error:'School storage could not complete this request. Please try again.',code:code||'DATABASE_UNAVAILABLE'};
}
