import {getCountryCallingCode,isPossiblePhoneNumber,parsePhoneNumberFromString,validatePhoneNumberLength,type CountryCode} from 'libphonenumber-js/min';

export function sanitizePhoneInput(value:string){
 return value.replace(/[^0-9+ ()-]/g,'').replace(/(?!^)\+/g,'');
}
export function validContactNumber(value:string){
 if(!/^\+?[0-9 ()-]+$/.test(value))return false;
 const parsed=parsePhoneNumberFromString(value,'IN');
 return !!parsed&&isPossiblePhoneNumber(parsed.number)&&(parsed.country!=='IN'||parsed.nationalNumber.length===10);
}

export function nationalNumberLimit(country:CountryCode){return country==='IN'?10:15-getCountryCallingCode(country).length}
export function limitNationalDigits(value:string,country:CountryCode){
 let digits=value.replace(/\D/g,'').slice(0,nationalNumberLimit(country));
 while(digits&&validatePhoneNumberLength(digits,country)==='TOO_LONG')digits=digits.slice(0,-1);
 return digits;
}

// Autofill can supply a complete international number to a national-number field.
// Parse it before applying national limits so the calling code consumes no digits.
export function normalizePhoneInput(value:string,country:CountryCode){
 const raw=sanitizePhoneInput(value.trim());
 const parsed=parsePhoneNumberFromString(raw,country);
 if(parsed?.country&&(raw.startsWith('+')||(parsed.country===country&&parsed.isPossible()))){
  return {country:parsed.country,digits:limitNationalDigits(parsed.nationalNumber,parsed.country)};
 }
 return {country,digits:limitNationalDigits(raw,country)};
}
