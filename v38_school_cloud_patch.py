#!/usr/bin/env python3
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent
APP = ROOT / 'app.html'
SW = ROOT / 'sw.js'
CSS = '''\n/* ===== V38 school cloud ===== */\n.school-card{ background:#fff; border:1.5px solid #E2E8F0; border-radius:18px; padding:16px; margin-bottom:14px; }\n.school-card h3{ margin:0 0 4px; font-size:15px; color:#0E131F; }\n.school-card p{ margin:0 0 12px; font-size:13px; color:#6B7280; line-height:1.45; }\n.school-entry{ background:#FFF8F2; border:1px solid #FFE0C7; border-radius:14px; padding:12px 14px; margin-bottom:10px; }\n.school-entry .se-head{ display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }\n.school-entry .se-date{ font-size:11px; font-weight:700; color:#FF8A2B; text-transform:uppercase; letter-spacing:.06em; }\n.school-entry .se-del{ border:0; background:none; color:#9CA3AF; cursor:pointer; font-size:14px; }\n.school-entry .se-line{ font-size:13px; color:#374151; line-height:1.4; margin-top:4px; }\n.school-entry .se-tag{ display:inline-block; font-size:11px; font-weight:700; background:#fff; border:1px solid #F3D7B3; color:#C1752E; border-radius:999px; padding:2px 8px; margin-right:6px; margin-top:4px; }\n.school-setup{ font-size:12px; color:#92400E; background:#FFFBEB; border:1px solid #FDE68A; border-radius:10px; padding:8px 10px; margin-top:10px; }\n'''
JS = r'''
function schoolToken(){const b=new Uint8Array(12);if(window.crypto&&window.crypto.getRandomValues)window.crypto.getRandomValues(b);else for(let i=0;i<b.length;i++)b[i]=Math.floor(Math.random()*256);return "s"+Array.from(b,function(x){return x.toString(16).padStart(2,"0")}).join("")}
function loadSchoolLinks(){try{const a=JSON.parse(localStorage.getItem("playbook:school-links")||"[]");return Array.isArray(a)?a:[]}catch(e){return []}}
function saveSchoolLinks(list){try{localStorage.setItem("playbook:school-links",JSON.stringify(list))}catch(e){}}
function loadSavedSchoolNotes(){try{const a=JSON.parse(localStorage.getItem("playbook:school-notes")||"[]");return Array.isArray(a)?a:[]}catch(e){return []}}
function saveSavedSchoolNotes(list){try{localStorage.setItem("playbook:school-notes",JSON.stringify(list.slice(0,40)))}catch(e){}}
function schoolLinkFor(token){const base=(window.location.origin+window.location.pathname).replace(/app\.html.*$/,"");return base+"school.html?t="+encodeURIComponent(token)}
function mapSchoolRow(row){return {id:row.id||row.sentAt||String(row.created_at||Date.now()),token:row.token,child:row.child||"Child",date:row.note_date||row.date||"",mood:row.mood||"",energy:row.energy||"",incidents:row.incidents||"",wins:row.wins||"",note:row.body||row.note||"",author:row.author_name||row.author||"Teacher",sentAt:row.created_at||row.sentAt||""}}
async function publishSchoolLink(entry){const sb=getSupabase();if(!sb)return {ok:false};const {error}=await sb.from("playbook_share_links").upsert({token:entry.token,label:entry.label,active:true});return {ok:!error}}
async function revokeSchoolLinkCloud(token){const sb=getSupabase();if(!sb)return;await sb.from("playbook_share_links").update({active:false}).eq("token",token)}
async function fetchSchoolNotesForTokens(tokens){const sb=getSupabase();if(!sb||!tokens.length)return {notes:loadSavedSchoolNotes(),error:null};const {data,error}=await sb.from("playbook_school_notes").select("*").in("token",tokens).order("created_at",{ascending:false}).limit(40);if(error)return {notes:loadSavedSchoolNotes(),error:error};const mapped=(data||[]).map(mapSchoolRow);saveSavedSchoolNotes(mapped);return {notes:mapped,error:null}}
function SchoolLinkCard({showToast}){const [links,setLinks]=useState(()=>loadSchoolLinks());const [copied,setCopied]=useState("");const [setupHint,setSetupHint]=useState("");async function makeLink(){const token=schoolToken();const entry={token:token,created:todayISO(),label:"School link "+(links.length+1)};const published=await publishSchoolLink(entry);setSetupHint(published.ok?"":"Link copied, but teacher send needs the one-time cloud setup.");const next=[entry,...links].slice(0,20);setLinks(next);saveSchoolLinks(next);const url=schoolLinkFor(token);try{if(navigator.clipboard&&navigator.clipboard.writeText)await navigator.clipboard.writeText(url)}catch(e){}setCopied(url);if(showToast)showToast(published.ok?"School link copied — send to the teacher":"Link copied — cloud setup still needed")}async function copyExisting(token){const url=schoolLinkFor(token);try{if(navigator.clipboard&&navigator.clipboard.writeText)await navigator.clipboard.writeText(url)}catch(e){}setCopied(url);if(showToast)showToast("Link copied")}async function revoke(token){const next=links.filter(function(l){return l.token!==token});setLinks(next);saveSchoolLinks(next);await revokeSchoolLinkCloud(token);if(showToast)showToast("Link revoked")}return (<div className="school-card"><h3>School link</h3><p>Give the teacher this link. They add today's note and it lands in your Playbook. They never see the full diary.</p><button type="button" className="btn-primary" style={{width:"100%"}} onClick={makeLink}>Create & copy school link</button>{links.map(function(l){return (<div key={l.token} style={{display:"flex",gap:8,alignItems:"center",marginTop:8,flexWrap:"wrap"}}><span style={{fontSize:12,color:"#6B7280",flex:"1 1 160px"}}>{l.label} · {l.created}</span><button type="button" className="btn-secondary" style={{padding:"6px 10px",fontSize:12}} onClick={function(){copyExisting(l.token)}}>Copy</button><button type="button" className="btn-secondary" style={{padding:"6px 10px",fontSize:12,color:"#B03A2E"}} onClick={function(){revoke(l.token)}}>Revoke</button></div>)})}{copied?<p style={{fontSize:11,color:"#9CA3AF",margin:"8px 0 0",wordBreak:"break-all"}}>Last copied: {copied}</p>:null}{setupHint?<div className="school-setup">{setupHint}</div>:null}</div>)}
function SchoolInbox({showToast}){const [inbox,setInbox]=useState(()=>loadSavedSchoolNotes());const [status,setStatus]=useState("");async function refresh(){const tokens=loadSchoolLinks().map(function(l){return l.token});const result=await fetchSchoolNotesForTokens(tokens);setInbox(result.notes||[]);if(result.error)setStatus("Could not reach school inbox yet.");else setStatus(result.notes&&result.notes.length?"":"No school notes yet.")}useEffect(function(){refresh();const id=setInterval(refresh,20000);return function(){clearInterval(id)}},[]);function dismiss(id){const next=inbox.filter(function(x){return x.id!==id});setInbox(next);saveSavedSchoolNotes(next)}return (<div style={{marginBottom:14}}>{inbox.map(function(s){return (<div className="school-entry" key={s.id}><div className="se-head"><span className="se-date">School · {s.date||""} · {s.author||"Teacher"}</span><button type="button" className="se-del" onClick={function(){dismiss(s.id)}}>✕</button></div><div><span className="se-tag">{s.child||"Child"}</span>{s.mood?<span className="se-tag">{s.mood}</span>:null}{s.energy?<span className="se-tag">Energy: {s.energy}</span>:null}{s.incidents?<span className="se-tag">Incidents: {s.incidents}</span>:null}</div>{s.wins?<div className="se-line"><b>Wins:</b> {s.wins}</div>:null}{s.note?<div className="se-line"><b>Note:</b> {s.note}</div>:null}</div>)})}<button type="button" className="btn-secondary" style={{padding:"6px 10px",fontSize:12}} onClick={refresh}>Refresh school notes</button>{status?<p style={{fontSize:12,color:"#6B7280",margin:"6px 0 0"}}>{status}</p>:null}</div>)}
'''

def main():
    html = APP.read_text(encoding='utf-8')
    if 'V38 school cloud' not in html:
        html = html.replace('/* ===== V36 trial / share / meds ===== */', CSS + '\n/* ===== V36 trial / share / meds ===== */', 1)
    if 'function SchoolLinkCard' not in html:
        idx = html.find('function Root() {')
        if idx == -1:
            raise SystemExit('no Root')
        html = html[:idx] + JS + '\n' + html[idx:]
    needle = '<MedReminderBanner dataStore={dataStore} onDismiss={(id) => { dismissMedReminder(id); if (typeof showToast === "function") showToast("Reminder cleared"); }} />'
    if needle in html and '<SchoolInbox showToast={showToast} />' not in html:
        html = html.replace(needle, needle + '\n      <SchoolInbox showToast={showToast} />', 1)
    comm = '<ConnectCard />\n      {cloudMode ? ('
    if comm in html and '<SchoolLinkCard showToast={showToast} />' not in html:
        html = html.replace(comm, '<ConnectCard />\n      <SchoolLinkCard showToast={showToast} />\n      {cloudMode ? (', 1)
    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=39")', html, count=1)
    APP.write_text(html, encoding='utf-8')
    sw = SW.read_text(encoding='utf-8')
    sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v39"', sw, count=1)
    SW.write_text(sw, encoding='utf-8')
    print('patched')

if __name__ == '__main__':
    main()
