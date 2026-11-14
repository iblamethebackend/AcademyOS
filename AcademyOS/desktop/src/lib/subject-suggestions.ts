export const subjectCatalog=[
 'English','English Language','English Literature','Mathematics','Applied Mathematics','Science','Social Studies',
 'Physics','Chemistry','Biology','History','Geography','Civics','Political Science','Economics','Business Studies',
 'Accountancy','Commerce','Computer Science','Computer Applications','Informatics Practices','Information Technology',
 'Artificial Intelligence','Data Science','Robotics','Environmental Studies','Environmental Science','General Knowledge',
 'Physical Education','Health Education','Art','Fine Arts','Visual Arts','Music','Dance','Drama','Theatre',
 'Moral Science','Value Education','Life Skills','Home Science','Design and Technology','Agriculture','Entrepreneurship',
 'Biotechnology','Statistics','Psychology','Sociology','Philosophy','Legal Studies','Financial Literacy','Mass Media Studies',
 'Hindi','Sanskrit','Urdu','Punjabi','Bengali','Marathi','Gujarati','Tamil','Telugu','Kannada','Malayalam','Odia','Assamese',
 'French','German','Spanish','Arabic',
];
export const normalizeSubject=(value:string)=>value.toLowerCase().trim().replace(/[\s._-]+/g,'');
const aliases:Record<string,string>={math:'Mathematics',maths:'Mathematics',sst:'Social Studies',socialscience:'Social Studies',cs:'Computer Science',computers:'Computer Science',it:'Information Technology',ict:'Information Technology',evs:'Environmental Studies',gk:'General Knowledge',pe:'Physical Education',pt:'Physical Education',theater:'Theatre'};
export function canonicalSubject(value:string){
 const cleaned=value.trim().replace(/\s+/g,' '),key=normalizeSubject(cleaned);
 return subjectCatalog.find(name=>normalizeSubject(name)===key)||(Object.hasOwn(aliases,key)?aliases[key]:cleaned);
}
function distance(a:string,b:string){
 const rows=Array.from({length:a.length+1},(_,i)=>Array.from({length:b.length+1},(_,j)=>i===0?j:j===0?i:0));
 for(let i=1;i<=a.length;i++)for(let j=1;j<=b.length;j++){
  rows[i][j]=Math.min(rows[i-1][j]+1,rows[i][j-1]+1,rows[i-1][j-1]+(a[i-1]===b[j-1]?0:1));
  if(i>1&&j>1&&a[i-1]===b[j-2]&&a[i-2]===b[j-1])rows[i][j]=Math.min(rows[i][j],rows[i-2][j-2]+1);
 }
 return rows[a.length][b.length];
}
export function suggestSubjects(value:string,selected:string[]=[],limit=7){
 const key=normalizeSubject(value);if(!key)return [];
 const selectedKeys=new Set(selected.map(name=>normalizeSubject(canonicalSubject(name))));
 return subjectCatalog.map(name=>{
  const target=normalizeSubject(name),names=[target,...Object.keys(aliases).filter(alias=>aliases[alias]===name)];
  let score=Infinity;
  for(const candidate of names){
   if(candidate===key)score=Math.min(score,0);
   else if(candidate.startsWith(key))score=Math.min(score,1+(candidate.length-key.length)/100);
   else if(key.length>=2&&candidate.includes(key))score=Math.min(score,2+candidate.indexOf(key)/100);
   else if(key.length>=3){const difference=distance(key,candidate),threshold=key.length<=4?1:key.length<=8?2:3;if(difference<=threshold)score=Math.min(score,3+difference/Math.max(key.length,candidate.length))}
  }
  return {name,score,alreadyAdded:selectedKeys.has(target)};
 }).filter(item=>Number.isFinite(item.score)).sort((a,b)=>a.score-b.score||a.name.localeCompare(b.name)).slice(0,limit).map(({name,alreadyAdded})=>({name,alreadyAdded}));
}
