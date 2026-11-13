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
