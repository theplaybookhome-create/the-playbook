#!/usr/bin/env python3
from pathlib import Path
import sys
p = Path(sys.argv[1] if len(sys.argv) > 1 else 'app.html')
s = p.read_text(encoding='utf-8')
PREMIUM_CSS = r'''
/* ===== Premium dashboard theme (mockup) ===== */
:root { --navy:#0E1822; --navy-mid:#15202B; --navy-dark:#0B1219; --amber:#E8892C; --amber-deep:#C1752E; --amber-tint:#FFF4E8; --paper:#F4F6F8; --sheet:#F7F8FA; }
.app-root { background:var(--navy-dark); padding-bottom:96px; }
.app-header { background:var(--navy) !important; color:#fff !important; padding:16px 20px 18px !important; border-bottom:none !important; }
.header-top { align-items:center; }
.brand { font-weight:800; letter-spacing:1.4px; font-size:15px; display:flex; align-items:center; gap:10px; color:#fff; }
.brand-mark { width:28px; height:28px; border-radius:8px; background:linear-gradient(180deg,#F5A24A,#E07A1A); box-shadow:0 4px 10px rgba(232,137,44,.35); }
.brand-sub { color:rgba(255,255,255,.55) !important; font-size:12px; margin-top:3px; }
.header-btn, .header-pill { background:#1C2A38 !important; border:1px solid rgba(255,255,255,.10) !important; color:#E8EEF4 !important; border-radius:12px !important; padding:8px 14px !important; font-weight:700 !important; font-size:12px !important; box-shadow:none !important; }
.header-avatar { width:38px; height:38px; border-radius:50%; background:#1C2A38; border:1.5px solid rgba(255,255,255,.14); color:#fff; font-weight:800; font-size:12px; display:grid; place-items:center; position:relative; }
.header-avatar .dot { position:absolute; right:1px; bottom:1px; width:8px; height:8px; background:#22C55E; border:2px solid var(--navy); border-radius:50%; }
.header-chips { display:flex; flex-wrap:wrap; gap:6px 4px; margin-top:14px; padding:8px 10px; background:#121C26; border-radius:14px; border:1px solid rgba(255,255,255,.06); }
.header-chips span { display:inline-flex; align-items:center; gap:6px; color:rgba(255,255,255,.72); font-size:12px; font-weight:600; padding:4px 8px; }
.header-chips span:not(:last-child)::after { content:"·"; margin-left:10px; color:rgba(255,255,255,.25); }
.child-bar { display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,.08) !important; }
.child-bar-label { color:rgba(255,255,255,.45); }
.child-chip { border:1px solid rgba(255,255,255,.14) !important; background:#1C2A38 !important; color:#fff !important; }
.child-chip.active { background:var(--amber) !important; border-color:var(--amber) !important; color:#fff !important; }
.child-manage { color:rgba(255,255,255,.7) !important; }
.app-main { background:var(--sheet); border-radius:28px 28px 0 0; margin-top:-2px; padding:22px 18px 28px; min-height:70vh; box-shadow:0 -12px 40px rgba(0,0,0,.18); }
.home-today { max-width:1080px; margin:0 auto; }
.home-top { display:grid; grid-template-columns:1fr; gap:14px; margin-bottom:16px; align-items:start; }
.home-greet { margin:2px 0 0; }
.home-greet .hi { font-size:30px; line-height:1.12; margin:0 0 8px; color:#111827; letter-spacing:-0.035em; font-weight:800; }
.home-greet .sub { margin:0; color:#6B7280; font-size:14.5px; }
.home-greet .sub b { color:var(--amber-deep); font-weight:700; }
.owned-chip-card, .paywall-card { border-radius:18px !important; border:1px solid #EEE4D6 !important; background:#FFF8F0 !important; }
.home-hero { display:grid; grid-template-columns:1fr; gap:14px; margin-bottom:16px; }
.quick-log-card { position:relative; overflow:hidden; border-radius:22px !important; border:1px solid #E8E2DA !important; background:radial-gradient(280px 160px at 92% 8%, rgba(252,211,140,.55), transparent 70%), radial-gradient(220px 140px at 100% 40%, rgba(186,214,232,.35), transparent 65%), #fff !important; box-shadow:0 10px 30px rgba(15,24,34,.06) !important; padding:18px !important; }
.quick-log-card h3 { font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:#111827; display:flex; align-items:center; gap:8px; margin:0 0 4px; }
.ql-bolt { position:static !important; width:28px !important; height:28px !important; border-radius:8px !important; background:#FFF4E8 !important; border:1px solid #F3D7B3 !important; }
.scale-btn { width:48px !important; height:48px !important; border-radius:14px !important; border:1.5px solid #E6E8EC !important; background:#fff !important; font-weight:800 !important; }
.scale-btn.active { background:linear-gradient(180deg,#F08A2A,#E07A1A) !important; border-color:#E07A1A !important; color:#fff !important; box-shadow:0 8px 16px rgba(224,122,26,.28); }
.tick-chip { border-radius:999px !important; border:1.5px solid #E6E8EC !important; background:#fff !important; padding:8px 12px !important; }
.tick-chip.active { background:#FFF4E8 !important; border-color:#F3D7B3 !important; }
.btn-primary, .ql-save { background:#15202B !important; color:#fff !important; border:none !important; border-radius:14px !important; padding:12px 18px !important; font-weight:700 !important; }
.home-side { display:flex; flex-direction:column; gap:12px; }
.energy-spark, .stat-card, .connect-card, .quick-link, .chart-card, .print-pack, .card { background:#fff; border:1px solid #E8ECF0; border-radius:20px; box-shadow:0 8px 24px rgba(15,24,34,.04); }
.energy-spark { padding:16px; }
.energy-spark h3 { margin:0; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#6B7280; }
.energy-spark svg { width:100%; height:84px; display:block; }
.energy-spark .es-big { font-size:32px; font-weight:800; letter-spacing:-.04em; color:#111827; }
.energy-spark .es-hint { font-size:12px; color:#9CA3AF; }
.stat-label { font-size:11px; letter-spacing:.07em; text-transform:uppercase; color:#6B7280; font-weight:700; }
.stat-value { font-size:32px; font-weight:800; letter-spacing:-.04em; color:#111827; margin:6px 0 2px; }
.connect-card { padding:18px; margin-bottom:14px; }
.connect-links { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.connect-btn { display:flex; align-items:center; gap:12px; text-decoration:none; color:inherit; background:#fff; border:1.5px solid #E8ECF0; border-radius:16px; padding:10px 12px; min-height:64px; }
.connect-btn .cb-ico { width:40px; height:40px; border-radius:12px; display:grid; place-items:center; flex:0 0 40px; }
.connect-btn .cb-ico svg { width:18px; height:18px; fill:#fff; }
.connect-btn.tt .cb-ico { background:#111; }
.connect-btn.xx .cb-ico { background:#0F1419; }
.connect-btn.fb .cb-ico { background:#1877F2; }
.connect-btn.em .cb-ico { background:#E8892C; }
.quick-links { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:4px 0 16px; }
.quick-link { text-align:left; padding:16px; cursor:pointer; font-family:inherit; border:1px solid #E8ECF0; }
.quick-link .ql-ico { width:42px; height:42px; border-radius:50%; display:grid; place-items:center; margin-bottom:10px; font-size:18px; border:none; }
.quick-link.t-log .ql-ico { background:#FFE8D2; }
.quick-link.t-ins .ql-ico { background:#EDE4FF; }
.quick-link.t-rep .ql-ico { background:#DCEBFF; }
.quick-link.t-com .ql-ico { background:#D8F5E8; }
.quick-link.t-print .ql-ico { background:#FBD7E8; }
.why-card { background:#FFF8F0; border:1px solid #F0E0CC; border-radius:18px; padding:14px 16px; }
.printables-grid { display:grid; grid-template-columns:1fr; gap:12px; }
.insight-dash { display:flex; flex-direction:column; gap:12px; }
.dash-kpis, .dash-charts { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.auth-shell { background:radial-gradient(900px 500px at 20% -10%, #1E3346, var(--navy-dark)); min-height:100vh; }
.bottom-nav { position:fixed; left:50%; transform:translateX(-50%); bottom:calc(10px + env(safe-area-inset-bottom)); width:calc(100% - 24px); max-width:720px; background:#15202B !important; border:none !important; border-radius:22px !important; padding:8px !important; box-shadow:0 16px 40px rgba(11,18,25,.45); display:flex; justify-content:space-between; z-index:40; }
.bottom-btn { flex:1; color:rgba(255,255,255,.46); background:transparent; border:none; border-radius:14px; padding:8px 4px; font-family:inherit; }
.bottom-btn .lbl { font-size:10px; font-weight:700; }
.bottom-btn.active { background:transparent; color:#F08A2A; }
.bottom-btn.active .lbl { color:#F08A2A !important; }
@media (min-width:860px) {
  .app-main { padding:28px 28px 40px; }
  .home-top { grid-template-columns:1fr 280px; }
  .home-hero { grid-template-columns:minmax(0,1.6fr) minmax(240px,.9fr); }
  .connect-links { grid-template-columns:repeat(4,1fr); }
  .quick-links { grid-template-columns:repeat(3,1fr); }
  .printables-grid { grid-template-columns:1fr 1fr; }
}
@media (max-width:559px) {
  .connect-links, .dash-kpis, .dash-charts { grid-template-columns:1fr; }
  .home-greet .hi { font-size:26px; }
}
'''
START = '/* ===== Remodel theme overlay ===== */'
END = '.app-main { padding-bottom: 92px; }'
if START in s and END in s:
    a = s.find(START); b = s.find(END)+len(END)
    s = s[:a] + PREMIUM_CSS + s[b:]
    print('replaced overlay')
elif 'Premium dashboard theme' not in s:
    s = s.replace('\n@media print {', PREMIUM_CSS + '\n@media print {', 1)
    print('injected css')
if 'function firstNameOf' not in s:
    old = 'function greetingForNow() {\n  const h = new Date().getHours();\n  if (h < 12) return "Good morning";\n  if (h < 17) return "Good afternoon";\n  return "Good evening";\n}'
    new = old + '''\nfunction firstNameOf(user) {\n  if (!user) return "";\n  const md = user.user_metadata || {};\n  const raw = String(md.display_name || md.name || md.full_name || "").trim();\n  if (raw) return raw.split(/\\s+/)[0];\n  const em = String(user.email || "").split("@")[0];\n  const cleaned = em.replace(/[0-9]+/g, " ").replace(/[._-]+/g, " ").trim();\n  const word = (cleaned.split(/\\s+/)[0] || em);\n  return word ? word.charAt(0).toUpperCase() + word.slice(1) : "";\n}\nfunction initialsOf(user) {\n  const n = firstNameOf(user);\n  if (n.length >= 2) return (n[0] + n[1]).toUpperCase();\n  const em = String((user && user.email) || "U");\n  return (em[0] + (em[1] || "P")).toUpperCase();\n}\n'''
    if old not in s: raise SystemExit('greetingForNow missing')
    s = s.replace(old, new, 1)
s = s.replace('function HomePage({ dataStore, setDataStore, onNavigate, unlocked, onUnlock, onOpenPaywall, showToast, activeChildId, activeChildName }) {', 'function HomePage({ dataStore, setDataStore, onNavigate, unlocked, onUnlock, onOpenPaywall, showToast, activeChildId, activeChildName, firstName }) {', 1)
old_home = '''  const hello = greetingForNow();\n  return (\n    <div>\n      <div className="home-greet">\n        <p className="hi">{hello}{activeChildName ? <em> · {activeChildName}</em> : null}</p>\n        <p className="sub">{activeChildName ? ("Logging for " + activeChildName + " · track what matters today.") : "Track what matters. Spot patterns. Look after yourself too."}</p>\n      </div>\n      <PaywallCard onUnlock={onUnlock} unlocked={unlocked} />\n      <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />\n      <EnergySpark values={recentEnergy} avg={avgEnergy} />\n      <div className="dash-kpis">\n        <div className="stat-card"><div className="stat-label">Energy (7 logs)</div><div className="stat-value">{avgEnergy}{avgEnergy !== "—" ? "/5" : ""}</div><div className="stat-hint">Your average lately</div></div>\n        <div className="stat-card"><div className="stat-label">Logs this device</div><div className="stat-value">{daily.length + behavior.length}</div><div className="stat-hint">Daily + behaviour</div></div>\n      </div>\n      <ConnectCard />'''
new_home = '''  const hello = greetingForNow();\n  const who = firstName || "";\n  return (\n    <div className="home-today">\n      <div className="home-top">\n        <div className="home-greet">\n          <p className="hi">{hello}{who ? ", " + who : ""}{who ? " 👋" : ""}</p>\n          <p className="sub">{activeChildName ? (<span>Logging for <b>{activeChildName}</b> · track what matters.</span>) : "Track what matters. Spot patterns. Look after yourself too."}</p>\n        </div>\n        <PaywallCard onUnlock={onUnlock} unlocked={unlocked} />\n      </div>\n      <div className="home-hero">\n        <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />\n        <div className="home-side">\n          <EnergySpark values={recentEnergy} avg={avgEnergy} />\n          <div className="stat-card">\n            <div className="stat-label">Logs this device</div>\n            <div className="stat-value">{daily.length + behavior.length}</div>\n            <div className="stat-hint">Daily + behaviour</div>\n          </div>\n        </div>\n      </div>\n      <ConnectCard />'''
if old_home in s:
    s = s.replace(old_home, new_home, 1); print('home layout')
else:
    print('WARN home mismatch')
s = s.replace('onClick={() => onNavigate("track", "daily")}><span className="ql-ico">', 'onClick={() => onNavigate("track", "daily")} className="quick-link t-log"><span className="ql-ico">', 1)
s = s.replace('onClick={() => onNavigate("insights")}><span className="ql-ico">', 'onClick={() => onNavigate("insights")} className="quick-link t-ins"><span className="ql-ico">', 1)
s = s.replace('onClick={() => onNavigate("report")}><span className="ql-ico">', 'onClick={() => onNavigate("report")} className="quick-link t-rep"><span className="ql-ico">', 1)
s = s.replace('onClick={() => onNavigate("community")}><span className="ql-ico">', 'onClick={() => onNavigate("community")} className="quick-link t-com"><span className="ql-ico">', 1)
s = s.replace('onClick={() => onNavigate("discover", null, "printables")}><span className="ql-ico">', 'onClick={() => onNavigate("discover", null, "printables")} className="quick-link t-print"><span className="ql-ico">', 1)
s = s.replace('className="quick-link" onClick={() => onNavigate("track", "daily")} className="quick-link t-log"', 'className="quick-link t-log" onClick={() => onNavigate("track", "daily")}')
s = s.replace('className="quick-link" onClick={() => onNavigate("insights")} className="quick-link t-ins"', 'className="quick-link t-ins" onClick={() => onNavigate("insights")}')
s = s.replace('className="quick-link" onClick={() => onNavigate("report")} className="quick-link t-rep"', 'className="quick-link t-rep" onClick={() => onNavigate("report")}')
s = s.replace('className="quick-link" onClick={() => onNavigate("community")} className="quick-link t-com"', 'className="quick-link t-com" onClick={() => onNavigate("community")}')
s = s.replace('className="quick-link" onClick={() => onNavigate("discover", null, "printables")} className="quick-link t-print"', 'className="quick-link t-print" onClick={() => onNavigate("discover", null, "printables")}')
s = s.replace('<div className="card">\n        <div className="stat-label">Why unlock helps</div>', '<div className="why-card">\n        <div className="stat-label">Why unlock helps</div>', 1)
old_hdr = '''        <div className="header-value">Private tracking · pattern insights · professional report · community · curated tools</div>'''
new_hdr = '''        <div className="header-chips"><span>🔒 Private tracking</span><span>📈 Pattern insights</span><span>📄 Professional report</span><span>👥 Community</span><span>✨ Curated tools</span></div>'''
if old_hdr in s:
    s = s.replace(old_hdr, new_hdr, 1)
    print('header chips')
if 'header-avatar' not in s:
    s = s.replace('{CLOUD_ENABLED && user ? <button type="button" className="header-btn header-pill" onClick={handleSignOut}>Sign out</button> : null}', '{CLOUD_ENABLED && user ? <button type="button" className="header-btn header-pill" onClick={handleSignOut}>Sign out</button> : null}\n            {user ? <div className="header-avatar" title={user.email || ""}>{initialsOf(user)}<span className="dot" /></div> : null}', 1)
s = s.replace('activeChildName={(children.find((c) => c.id === activeChildId) || {}).name} />', 'activeChildName={(children.find((c) => c.id === activeChildId) || {}).name} firstName={firstNameOf(user)} />', 1)
s = s.replace('<div className="auth-screen">', '<div className="auth-screen auth-shell">', 1)
s = s.replace('<meta name="theme-color" content="#1A252F" />', '<meta name="theme-color" content="#0B1219" />', 1)
for must in ['Premium dashboard theme','home-hero','header-chips','firstNameOf']:
    if must not in s: raise SystemExit('missing '+must)
p.write_text(s, encoding='utf-8')
print('wrote', p.stat().st_size)
