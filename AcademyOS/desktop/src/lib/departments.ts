// Departments are school-owned configuration; account roles remain separate.
export function validDepartmentConfiguration(value:unknown):boolean{
 if(!value||typeof value!=='object')return false;
 const state=value as {departments?:unknown;members?:unknown};
 if(state.departments!==undefined&&!Array.isArray(state.departments))return false;
 const departments=(state.departments||[]) as unknown[];
 if(departments.length>100)return false;
 const ids=new Set<string>(),names=new Set<string>();
 for(const item of departments){
  if(!item||typeof item!=='object')return false;
  const department=item as {id?:unknown;name?:unknown;description?:unknown};
  if(typeof department.id!=='string'||!department.id||department.id.length>64||ids.has(department.id))return false;
  if(typeof department.name!=='string'||department.name.trim().length<2||department.name.length>60)return false;
  if(typeof department.description!=='string'||department.description.length>240)return false;
  const name=department.name.trim().replace(/\s+/g,' ').toLowerCase();if(names.has(name))return false;
  ids.add(department.id);names.add(name);
 }
 return Array.isArray(state.members)&&state.members.every(member=>member&&typeof member==='object'&&(!('departmentId' in member)||member.departmentId===undefined||(typeof member.departmentId==='string'&&ids.has(member.departmentId))));
}
