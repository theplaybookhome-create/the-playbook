#!/usr/bin/env python3
import pathlib,sys
ROOT=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "app.html")
t=ROOT.read_text(encoding="utf-8")
o=t
def s(a,b,n):
    global t
    if a in t:
        t=t.replace(a,b,1); print("ok",n); return
    if b in t: print("skip",n); return
    print("MISSING",n)
s("THEME_BUILD_V23","THEME_BUILD_V24","theme")
s("./sw.js?v=23","./sw.js?v=24","swq")
s('<span className="quick-log-label">Energy</span>','<div className="ql-sec-label">Energy</div>',"e-lab")
s('<span className="quick-log-label" style={{ marginTop: 8 }}>Mood</span>','<div className="ql-sec-label">Mood</div>',"m-lab")
s('      <img className="connect-banner" src="connect-banner.jpg" alt="" width="1080" height="675" onError={(e) => { e.currentTarget.style.display = "none"; }} />\n','',"banner")
s("      {lastWin && <div className=\"card\"><div className=\"stat-label\">Latest win</div><p style={{ margin: \"6px 0 0\", fontSize: 14, lineHeight: 1.45 }}>{lastWin.win}</p></div>}\n","      {null}\n","win")
s('<div className="stat-label">Logs this device</div>','<div className="stat-label"><span className="stat-ico" aria-hidden="true">📊</span> Logs this device</div>',"logs")
s('<div className="stat-label">✓ Why unlock helps</div>','<div className="stat-label why-label"><span className="why-check">✓</span> Why unlock helps</div>',"why")
s('Insights, report, Discover, Printables & more unlocked.','Insights, report, Discover, Printables<br/>& more unlocked.',"owned")
s('<span>Energy, mood, what went well</span>','<span className="ql-hint">Energy, mood, what went well</span>',"h1")
s('<span>Triggers, sleep, energy trends</span>','<span className="ql-hint">Triggers, sleep, energy trends</span>',"h2")
s('<span>Print for school / GP</span>','<span className="ql-hint">Print for school / GP</span>',"h3")
s('<span>Peer notes & support</span>','<span className="ql-hint">Peer notes & support</span>',"h4")
s('<span>Preview packs · download</span>','<span className="ql-hint">Preview packs · download</span>',"h5")
CSS="""
/* ===== V24 mockup fidelity ===== */
.header-chips{display:flex!important;align-items:center}
.header-chips .hchip:not(:last-child)::after{content:"·";margin-left:10px;color:rgba(255,255,255,.28);font-weight:700}
.child-manage{margin-left:auto!important}
.bottom-nav{display:flex!important;max-width:920px!important}
.app-root{padding-bottom:112px!important}
.es-top{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px}
.stat-ico{font-size:13px;margin-right:6px}
.owned-card{display:flex!important;align-items:center!important;gap:12px!important;padding:16px!important;background:#FFF8F0!important;border:1px solid #F0E0CC!important;border-radius:18px!important}
.owned-card p{display:block!important}
.owned-card .price-pill{background:#16A34A!important;color:#fff!important;border-radius:999px!important;padding:4px 10px!important;font-size:12px!important;font-weight:800!important;margin-left:auto;flex:0 0 auto}
.home-top{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(260px,340px)!important;align-items:start!important;gap:16px!important;margin-bottom:18px!important}
.home-top .paywall-card,.home-top .owned-card{width:100%;max-width:340px;margin:0 0 0 auto!important}
.home-hero{display:grid!important;grid-template-columns:minmax(0,1.75fr) minmax(230px,.72fr)!important;gap:14px!important;align-items:stretch!important}
.home-side{display:flex;flex-direction:column;gap:12px;height:100%}
.energy-spark,.stat-card{flex:1}
.quick-log-card{position:relative!important;overflow:hidden!important;min-height:292px;padding:18px 210px 16px 18px!important;background:radial-gradient(280px 170px at 92% 10%,rgba(252,211,140,.5),transparent 70%),radial-gradient(220px 140px at 100% 46%,rgba(186,214,232,.32),transparent 65%),#fff!important}
.ql-sec-label{font-size:13px;font-weight:800;color:#111827;margin:0 0 8px;display:block}
.ql-sun{width:228px!important;height:168px!important;right:0!important;top:6px!important;opacity:1!important}
.scale-row{gap:10px!important}
.scale-btn{width:52px!important;height:52px!important;border-radius:14px!important;font-size:16px!important}
.connect-banner{display:none!important}
.connect-card{position:relative;overflow:hidden;background:#fff!important;border:1px solid #E8ECF0!important}
.connect-card::after{content:"";position:absolute;right:-10px;top:0;bottom:0;width:140px;background-image:radial-gradient(#D7E6F5 1.1px,transparent 1.2px);background-size:10px 10px;opacity:.55;pointer-events:none}
.connect-links{display:grid!important;grid-template-columns:repeat(4,1fr)!important;gap:10px!important}
.connect-btn{display:flex!important;flex-direction:row!important;align-items:center!important;gap:10px!important;width:100%!important;max-width:none!important;background:#fff!important;border:1.5px solid #E8ECF0!important;border-radius:16px!important;padding:10px 28px 10px 12px!important;min-height:64px!important;text-align:left!important}
.connect-btn .cb-ico{width:40px!important;height:40px!important;border-radius:50%!important;flex:0 0 40px!important;display:grid!important;place-items:center!important}
.connect-btn .cb-ico svg{width:18px!important;height:18px!important;fill:#fff!important}
.connect-btn.tt .cb-ico{background:#111!important}
.connect-btn.xx .cb-ico{background:#0F1419!important}
.connect-btn.fb .cb-ico{background:#1877F2!important}
.connect-btn.em .cb-ico{background:#E8892C!important;border:none!important}
.connect-btn.em .cb-ico svg,.connect-btn.em .cb-ico svg path{fill:#fff!important}
.quick-links{display:grid!important;grid-template-columns:repeat(3,1fr)!important;gap:12px!important}
.quick-link{display:flex!important;flex-direction:column!important;align-items:flex-start!important;text-align:left!important;padding:16px 28px 16px 16px!important;min-height:118px}
.quick-link .ql-ico{width:44px!important;height:44px!important;border-radius:50%!important;display:grid!important;place-items:center!important;margin-bottom:10px!important;font-size:18px!important}
.quick-link strong{font-size:15px;color:#111827}
.quick-link .ql-hint{display:block;margin-top:4px;font-size:13px;color:#6B7280;line-height:1.35;font-weight:500}
.why-card{position:relative;padding:16px 28px 16px 16px!important;min-height:118px}
.why-label{text-transform:none!important;letter-spacing:0!important;font-size:14px!important;color:#111827!important;display:flex;align-items:center;gap:6px}
.why-check{color:#E8892C;font-weight:800}
.why-card::after{content:"›";position:absolute;right:14px;bottom:14px;top:auto;color:#C4CAD1;font-size:20px}
.energy-spark svg{height:78px}
.bottom-btn.active .ico svg{stroke:#F08A2A;fill:#F08A2A}
.header-actions .signout-quiet{display:none}
@media (max-width:759px){
.home-top{grid-template-columns:1fr!important}
.home-top .paywall-card,.home-top .owned-card{max-width:none;margin:0!important}
.home-hero{grid-template-columns:1fr!important}
.quick-log-card{padding:18px!important;min-height:0}
.ql-sun{width:128px!important;height:96px!important;opacity:.78!important}
.quick-links{grid-template-columns:1fr 1fr!important}
.connect-links{grid-template-columns:1fr 1fr!important}
.scale-btn{width:46px!important;height:46px!important}
}
"""
if "V24 mockup fidelity" not in t:
    start=t.find("/* ===== V23 mockup match ===== */")
    if start<0: start=t.find("/* ===== V22 desktop + empty-state polish ===== */")
    end=t.find("@media print {", start if start>=0 else 0)
    if start>=0 and end>start:
        t=t[:start]+CSS+"\n"+t[end:]; print("ok css")
    else: print("MISSING css",start,end)
else: print("skip css")
if t!=o:
    ROOT.write_text(t); print("patched",len(t.encode()))
else: print("no-op")
print("V24", "THEME_BUILD_V24" in t, "css", "V24 mockup fidelity" in t, "ql", "ql-sec-label" in t)
