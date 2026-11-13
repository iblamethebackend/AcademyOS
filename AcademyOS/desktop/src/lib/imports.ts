import {roles,type State} from './model';
export type ImportRow={line:number;name:string;key:string;detail:string;errors:string[]};
export function parseCSV(text:string):string[][]{
 const rows:string[][]=[];let row:string[]=[],field='',quoted=false;
 for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){field+='"';i++}else quoted=!quoted}else if(c===','&&!quoted){row.push(field.trim());field=''}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(field.trim());if(row.some(Boolean))rows.push(row);row=[];field=''}else field+=c}
 if(quoted)throw new Error('A quoted field is not closed. Check the CSV and try again.');row.push(field.trim());if(row.some(Boolean))rows.push(row);return rows;
}
export function reviewCSV(text:string,kind:'staff'|'students',state:State):ImportRow[]{
 const rows=parseCSV(text.replace(/^\uFEFF/,''));const headers=kind==='staff'?['name','email','role']:['name','admissionno','grade'];if(!rows.length||headers.some((h,i)=>rows[0][i]?.toLowerCase()!==h)||rows[0].length!==3)throw new Error(`Use these three columns in order: ${headers.join(', ')}.`);
 if(rows.length<2)throw new Error('Add at least one data row below the header.');if(rows.length>501)throw new Error('Preview up to 500 rows at a time. Split this file into smaller batches.');
 const seen=new Set((kind==='staff'?state.members.map(m=>m.email):state.students.map(s=>s.admissionNo)).map(s=>s.toLowerCase()));
 return rows.slice(1).map((r,i)=>{const [name='',key='',detail='']=r;const errors:string[]=[];if(r.length!==3)errors.push('Expected 3 columns');if(!name)errors.push('Name is required');if(!key)errors.push(kind==='staff'?'Email is required':'Admission number is required');if(kind==='staff'&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(key))errors.push('Invalid email');if(kind==='staff'&&!roles.includes(detail))errors.push('Unknown department role');if(kind==='students'&&!state.academic.grades.includes(detail))errors.push('Grade is not configured');if(key&&seen.has(key.toLowerCase()))errors.push('Duplicate record');if(key)seen.add(key.toLowerCase());return {line:i+2,name,key,detail,errors}});
}
