import {id,type Department} from './model';
import {departmentInfo} from './workspace';

export const suggestedDepartmentPrefix='suggested:';
export const normalizeDepartmentName=(name:string)=>name.trim().replace(/\s+/g,' ').toLowerCase();
export function invitationDepartment(departments:Department[],selection:string):{departments:Department[];departmentId?:string}{
 if(!selection)return {departments};
 const existing=departments.find(department=>department.id===selection);
 if(existing)return {departments,departmentId:existing.id};
 if(!selection.startsWith(suggestedDepartmentPrefix))throw new Error('This department is no longer available. Choose another department.');
 const name=selection.slice(suggestedDepartmentPrefix.length);
 if(!Object.hasOwn(departmentInfo,name))throw new Error('Choose a department from the list.');
 const matching=departments.find(department=>normalizeDepartmentName(department.name)===normalizeDepartmentName(name));
 if(matching)return {departments,departmentId:matching.id};
 if(departments.length>=100)throw new Error('Your school has reached its 100 department limit. Choose an existing department.');
 const department={id:id(),name,description:departmentInfo[name].description};
 return {departments:[...departments,department],departmentId:department.id};
}
