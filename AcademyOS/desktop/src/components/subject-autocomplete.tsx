'use client';
import {useEffect,useId,useRef,useState} from 'react';
import {suggestSubjects} from '@/lib/subject-suggestions';
import {Icon} from './icons';
import './subject-autocomplete.css';

export function SubjectAutocomplete({value,subjects,disabled,error,onChange,onAdd}:{value:string;subjects:string[];disabled:boolean;error:boolean;onChange:(value:string)=>void;onAdd:(value:string)=>void}){
 const input=useRef<HTMLInputElement>(null),listId=useId();
 const [open,setOpen]=useState(false),[active,setActive]=useState(-1);
 const suggestions=suggestSubjects(value,subjects),expanded=open&&suggestions.length>0;
 useEffect(()=>{if(expanded&&active>=0)document.getElementById(listId+'-'+active)?.scrollIntoView({block:'nearest'})},[active,expanded,listId]);
 function choose(name:string){if(disabled)return;onAdd(name);setOpen(false);setActive(-1);input.current?.focus()}
 function move(direction:number){const available=suggestions.map((item,index)=>item.alreadyAdded?-1:index).filter(index=>index>=0);if(!available.length)return;const current=available.indexOf(active),next=current<0?(direction>0?0:available.length-1):(current+direction+available.length)%available.length;setActive(available[next]);setOpen(true)}
 return <div className="subject-autocomplete"><div className="inline-input"><input ref={input} role="combobox" aria-label="New subject" aria-autocomplete="list" aria-haspopup="listbox" aria-expanded={expanded} aria-controls={expanded?listId:undefined} aria-activedescendant={expanded&&active>=0?listId+'-'+active:undefined} aria-invalid={error} aria-describedby={error?'subject-error':'subject-help'} placeholder="Add a subject, e.g. Art" value={value} maxLength={40} autoComplete="off" spellCheck={false} disabled={disabled} onFocus={()=>setOpen(true)} onBlur={()=>{setOpen(false);setActive(-1)}} onChange={event=>{onChange(event.target.value);setActive(-1);setOpen(true)}} onKeyDown={event=>{if(event.nativeEvent.isComposing)return;if(event.key==='ArrowDown'||event.key==='ArrowUp'){event.preventDefault();move(event.key==='ArrowDown'?1:-1)}else if(event.key==='Escape'){event.preventDefault();setOpen(false);setActive(-1)}else if(event.key==='Enter'){event.preventDefault();if(expanded&&active>=0&&!suggestions[active]?.alreadyAdded)choose(suggestions[active].name);else choose(value)}}}/><button type="button" className="button" disabled={!value.trim()||disabled} onClick={()=>choose(value)}><Icon name="plus" size={16}/>Add subject</button></div>
  {expanded&&<div className="subject-suggestions-panel"><p>Suggested subjects</p><ul id={listId} data-lenis-prevent role="listbox" aria-label="Subject suggestions">{suggestions.map((item,index)=><li id={listId+'-'+index} key={item.name} role="option" aria-selected={active===index} aria-disabled={item.alreadyAdded} className={(active===index?'is-active ':'')+(item.alreadyAdded?'is-added':'')} onMouseDown={event=>event.preventDefault()} onMouseEnter={()=>{if(!item.alreadyAdded)setActive(index)}} onClick={()=>{if(!item.alreadyAdded)choose(item.name)}}><span>{item.name}</span>{item.alreadyAdded?<small>Already added</small>:<Icon name="plus" size={14}/>}</li>)}</ul><small>Choose the correct spelling, or add your own subject.</small></div>}
 </div>;
}
