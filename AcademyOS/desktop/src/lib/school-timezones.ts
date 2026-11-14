export const schoolTimezones=Array.from(new Set(['UTC','Asia/Kolkata',...Intl.supportedValuesOf('timeZone')])).sort();

export function validSchoolTimezone(value:unknown):value is string{
 if(typeof value!=='string'||!value.trim()||value.length>100)return false;
 try{new Intl.DateTimeFormat('en',{timeZone:value});return true}catch{return false}
}

export function validSchoolAddress(value:unknown):value is string{
 return typeof value==='string'&&value.trim().length>=5&&value.trim().length<=500;
}
