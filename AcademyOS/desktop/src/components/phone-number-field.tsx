'use client';
import {sanitizePhoneInput,limitNationalDigits,nationalNumberLimit} from '@/lib/phone-input';
import {useState} from 'react';
import {getCountries,getCountryCallingCode,parsePhoneNumberFromString,type CountryCode} from 'libphonenumber-js/min';
import './phone-number-field.css';

const names=new Intl.DisplayNames(['en'],{type:'region'});
const countries=getCountries().sort((a,b)=>(names.of(a)||a).localeCompare(names.of(b)||b));

export function PhoneNumberField({value,onChange,error,disabled=false,label='School contact number',inputId='register-phone',required=false}:{value:string;onChange:(value:string)=>void;error?:string;disabled?:boolean;label?:string;inputId?:string;required?:boolean}){
 const [country,setCountry]=useState<CountryCode>(()=>parsePhoneNumberFromString(value)?.country||'IN');
 const dial='+'+getCountryCallingCode(country);
 const national=(value.startsWith(dial)?value.slice(dial.length):value).replace(/\D/g,'');
 function updateNumber(raw:string){
  raw=sanitizePhoneInput(raw);
  if(raw.startsWith('+')){const parsed=parsePhoneNumberFromString(raw);if(parsed?.country){const digits=limitNationalDigits(parsed.nationalNumber,parsed.country);setCountry(parsed.country);onChange('+'+getCountryCallingCode(parsed.country)+' '+digits);return}}
  const digits=limitNationalDigits(raw,country);onChange(digits?dial+' '+digits:'');
 }
 return <div className="login-field phone-number-field"><label htmlFor={inputId}>{label}</label>
  <div className={'login-input phone-number-input'+(error?' invalid':'')}>
   <div className="phone-country-picker">
    <span className="phone-country-display" aria-hidden="true"><img src={'/country-flags/'+country+'.svg'} alt="" width="22" height="15"/><span>{dial}</span><svg width="10" height="10" viewBox="0 0 12 12" fill="none"><path d="m3 4.5 3 3 3-3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/></svg></span>
    <select aria-label="Phone country and calling code" value={country} disabled={disabled} onChange={e=>{const next=e.target.value as CountryCode;setCountry(next);const digits=limitNationalDigits(national,next);onChange(digits?'+'+getCountryCallingCode(next)+' '+digits:'')}}>
     {countries.map(code=><option value={code} key={code}>{names.of(code)} (+{getCountryCallingCode(code)})</option>)}
    </select>
   </div>
   <input id={inputId} name="phone" type="tel" inputMode="numeric" autoComplete="tel-national" required={required} pattern={country==='IN'?'[0-9]{10}':'[0-9]+'} value={national} onChange={e=>updateNumber(e.target.value)} onPaste={e=>{e.preventDefault();const raw=e.clipboardData.getData('text');const input=e.currentTarget;updateNumber(raw.trim().startsWith('+')?raw:input.value.slice(0,input.selectionStart??0)+raw+input.value.slice(input.selectionEnd??input.value.length))}} placeholder={country==='IN'?'9876543210':'Phone number'} maxLength={nationalNumberLimit(country)} disabled={disabled} aria-invalid={!!error} aria-describedby={error?inputId+'-error':undefined}/>
  </div>
  {error&&<span className="login-field-error" id={inputId+'-error'}>{error}</span>}
 </div>
}
