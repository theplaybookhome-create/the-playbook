#!/usr/bin/env python3
"""Bring Today page to the mockup. Idempotent-ish."""
from pathlib import Path
import sys

p = Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
s = p.read_text(encoding="utf-8")

POLISH_CSS = r"""
/* ===== Mockup polish ===== */
@media (min-width: 720px) {
  .app-header, .app-main { padding-left: 22px; padding-right: 22px; }
  .home-top { grid-template-columns: 1fr 300px !important; }
  .home-hero { grid-template-columns: minmax(0, 1.55fr) minmax(250px, 0.9fr) !important; }
  .connect-links { grid-template-columns: repeat(4, 1fr) !important; }
  .quick-links { grid-template-columns: repeat(3, 1fr) !important; }
}
.quick-log-card { min-height: 280px; }
.ql-sun { position: absolute; right: 8px; top: 8px; width: 168px; height: 128px; pointer-events: none; opacity: 0.95; }
.ql-head { display: flex; align-items: center; gap: 8px; margin-bottom: 2px; position: relative; z-index: 1; }
.ql-head h3 { margin: 0; }
.ql-foot { display: flex; gap: 10px; align-items: center; margin-top: 12px; position: relative; z-index: 1; }
.ql-foot input { flex: 1; min-width: 0; margin: 0 !important; border: 1.5px solid #E6E8EC; border-radius: 14px; padding: 12px 14px; font-family: inherit; }
.ql-foot .btn-primary { width: auto !important; white-space: nowrap; padding: 12px 16px !important; }
.tick-chip .tick-box { display: none; }
.tick-chip { display: inline-flex; align-items: center; gap: 6px; }
.owned-card { display: flex; gap: 12px; align-items: flex-start; background: #FFF8F0 !important; border: 1px solid #F0E0CC !important; border-radius: 18px; padding: 14px 16px; }
.owned-crown { width: 40px; height: 40px; border-radius: 50%; flex: 0 0 40px; display: grid; place-items: center; background: #FFE4C4; font-size: 18px; }
.owned-card .price-pill { background: #16A34A !important; color: #fff; margin-left: auto; }
.quick-link { position: relative; padding-right: 28px; }
.quick-link::after { content: "›"; position: absolute; right: 14px; top: 16px; color: #C4CAD1; font-size: 20px; }
.connect-btn { position: relative; padding-right: 28px; }
.connect-btn::after { content: "›"; position: absolute; right: 12px; top: 50%; transform: translateY(-50%); color: #C4CAD1; font-size: 18px; }
.header-btn.ico-btn { display: inline-flex; align-items: center; gap: 6px; }
.header-btn.ico-btn svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2; }
.why-card { grid-column: auto; }
.bottom-btn .ico svg { width: 18px; height: 18px; display: block; margin: 0 auto 3px; }
.bottom-btn.active .ico svg { stroke: #F08A2A; fill: none; }
.signout-quiet { opacity: 0.7; font-size: 11px !important; padding: 8px 10px !important; }
"""

if "Mockup polish" not in s:
    s = s.replace("\n@media print {", POLISH_CSS + "\n@media print {", 1)
    print("injected polish css")

old_es = '''  return (
    <div className="energy-spark">
      <div className="es-top">
        <h3>Energy spark</h3>
        <div className="es-avg">{avg !== "—" ? ("avg " + avg + "/5") : "log a few days"}</div>
      </div>
      {pts.length < 2 ? (
        <p className="es-empty">A tiny sparkline appears after two energy logs.</p>
      ) : (
        <svg viewBox={"0 0 " + w + " " + h} aria-hidden="true">
          <path d={path} fill="none" stroke="#C1752E" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
    </div>
  );'''
new_es = '''  return (
    <div className="energy-spark">
      <div className="es-top">
        <h3>Energy ({pts.length} logs)</h3>
        <div className="es-avg">›</div>
      </div>
      {pts.length < 2 ? (
        <p className="es-empty">A sparkline appears after two energy logs.</p>
      ) : (
        <svg viewBox={"0 0 " + w + " " + h} aria-hidden="true">
          <path d={path} fill="none" stroke="#E07A1A" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
      <div className="es-big">{avg}</div>
      <div className="es-hint">Your average lately</div>
    </div>
  );'''
if old_es in s:
    s = s.replace(old_es, new_es, 1)
    print("energy spark restyled")

old_ql = '''  return (
    <div className="quick-log-card">
      <h3>Quick log</h3>
      <p>One-tap energy & mood — full detail later if you want.</p>
      <div className="quick-log-row">
        <span className="quick-log-label">Energy</span>
        <div className="scale-row">
          {[1,2,3,4,5].map((n) => (
            <button type="button" key={n} className={"scale-btn" + (energy === n ? " active" : "")} onClick={() => setEnergy(n)}>{n}</button>
          ))}
        </div>
      </div>
      <div className="quick-log-row" style={{ alignItems: "flex-start" }}>
        <span className="quick-log-label" style={{ marginTop: 8 }}>Mood</span>
        <div className="tick-row">
          {moodOpts.map((m) => (
            <button type="button" key={m} className={"tick-chip" + (mood.includes(m) ? " active" : "")} onClick={() => toggleMood(m)}>
              <span className="tick-box">{mood.includes(m) ? "✓" : ""}</span>{m}
            </button>
          ))}
        </div>
      </div>
      <input type="text" placeholder="One line note (optional)" value={note} onChange={(e) => setNote(e.target.value)} style={{ marginBottom: 10 }} />
      <button type="button" className="btn-primary" style={{ width: "100%" }} onClick={save}>Save quick log</button>
    </div>
  );'''

new_ql = '''  const faces = { Calm: "😌", Happy: "😄", Wobbly: "😕", Overwhelmed: "😣", Shutdown: "😞", "Big feelings": "🤯" };
  return (
    <div className="quick-log-card">
      <svg className="ql-sun" viewBox="0 0 168 128" aria-hidden="true">
        <defs>
          <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#FDE7C7" stopOpacity="0.9"/>
            <stop offset="1" stopColor="#FDE7C7" stopOpacity="0"/>
          </linearGradient>
          <radialGradient id="sun" cx="70%" cy="38%" r="38%">
            <stop offset="0" stopColor="#F8C14A"/>
            <stop offset="1" stopColor="#F3A02A" stopOpacity="0.15"/>
          </radialGradient>
        </defs>
        <rect width="168" height="128" fill="url(#sky)"/>
        <circle cx="118" cy="48" r="26" fill="url(#sun)"/>
        <circle cx="118" cy="48" r="16" fill="#F6B43A"/>
        <path d="M18 118 C40 92 58 88 78 96 C96 104 108 86 128 90 C146 94 158 108 168 118 L168 128 L0 128 Z" fill="#E8D5B5" opacity="0.55"/>
        <path d="M40 128 C58 104 74 100 92 110 C108 118 122 102 148 108 L168 118 L168 128 Z" fill="#D9C4A0" opacity="0.45"/>
      </svg>
      <div className="ql-head">
        <span className="ql-bolt" aria-hidden="true">⚡</span>
        <h3>Quick log</h3>
      </div>
      <p>One-tap energy & mood — full detail later if you want.</p>
      <div className="quick-log-row">
        <span className="quick-log-label">Energy</span>
        <div className="scale-row">
          {[1,2,3,4,5].map((n) => (
            <button type="button" key={n} className={"scale-btn" + (energy === n ? " active" : "")} onClick={() => setEnergy(n)}>{n}</button>
          ))}
        </div>
      </div>
      <div className="quick-log-row" style={{ alignItems: "flex-start" }}>
        <span className="quick-log-label" style={{ marginTop: 8 }}>Mood</span>
        <div className="tick-row">
          {moodOpts.map((m) => (
            <button type="button" key={m} className={"tick-chip" + (mood.includes(m) ? " active" : "")} onClick={() => toggleMood(m)}>
              <span aria-hidden="true">{faces[m] || ""}</span> {m}
            </button>
          ))}
        </div>
      </div>
      <div className="ql-foot">
        <input type="text" placeholder="One line note (optional)" value={note} onChange={(e) => setNote(e.target.value)} />
        <button type="button" className="btn-primary" onClick={save}>Save quick log ›</button>
      </div>
    </div>
  );'''

if old_ql in s:
    s = s.replace(old_ql, new_ql, 1)
    print("quick log mockup")
elif "ql-sun" in s:
    print("quick log already polished")
else:
    print("WARN quick log mismatch")

old_owned = '''    return (
      <div className="card" style={{ borderColor: "var(--amber)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
          <div>
            <div className="stat-label">Full access on this device</div>
            <p style={{ margin: "4px 0 0", fontSize: 13, color: "var(--soft)" }}>Insights, report, Discover, Printables & more unlocked.</p>
          </div>
          <span className="price-pill" style={{ background: "var(--success)" }}>Owned</span>
        </div>
      </div>
    );'''
new_owned = '''    return (
      <div className="owned-card">
        <div className="owned-crown" aria-hidden="true">👑</div>
        <div>
          <div className="stat-label" style={{ textTransform: "none", letterSpacing: 0, fontSize: 14, color: "#111827" }}>Full access on this device</div>
          <p style={{ margin: "4px 0 0", fontSize: 12.5, color: "var(--soft)" }}>Insights, report, Discover, Printables & more unlocked.</p>
        </div>
        <span className="price-pill">Owned</span>
      </div>
    );'''
if old_owned in s:
    s = s.replace(old_owned, new_owned, 1)
    print("owned card")

old_actions = '''            <button type="button" className="header-btn header-pill" onClick={handleExport}>Export</button>
            <button type="button" className="header-btn header-pill" onClick={() => fileInputRef.current?.click()}>Import</button>
            {CLOUD_ENABLED && user ? <button type="button" className="header-btn header-pill" onClick={handleSignOut}>Sign out</button> : null}
            <input ref={fileInputRef} type="file" accept="application/json,.json" className="hidden-file" onChange={(e) => handleImport(e.target.files?.[0])} />'''
new_actions = '''            <button type="button" className="header-btn header-pill ico-btn" onClick={handleExport}><svg viewBox="0 0 24 24"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 21h14"/></svg>Export</button>
            <button type="button" className="header-btn header-pill ico-btn" onClick={() => fileInputRef.current?.click()}><svg viewBox="0 0 24 24"><path d="M12 21V9"/><path d="M7 16l5 5 5-5"/><path d="M5 3h14"/></svg>Import</button>
            {CLOUD_ENABLED && user ? <button type="button" className="header-btn header-pill signout-quiet" onClick={handleSignOut}>Sign out</button> : null}
            {user ? <div className="header-avatar" title={user.email || ""}>{initialsOf(user)}<span className="dot" /></div> : null}
            <input ref={fileInputRef} type="file" accept="application/json,.json" className="hidden-file" onChange={(e) => handleImport(e.target.files?.[0])} />'''
if old_actions in s:
    s = s.replace(old_actions, new_actions, 1)
    print("header actions")

if "function initialsOf" not in s:
    raise SystemExit("initialsOf missing")

old_bottom = '''const bottom = [
    { id: "home", label: "Today", ico: "◎" },
    { id: "track", label: "Track", ico: "☰" },
    { id: "insights", label: "Insights", ico: "◔" },
    { id: "report", label: "Report", ico: "▤" },
    { id: "community", label: "Community", ico: "◉" },
    { id: "discover", label: "Discover", ico: "✦" },
  ];'''
new_bottom = '''const bottom = [
    { id: "home", label: "Today", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/></svg> },
    { id: "track", label: "Track", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4M16 3v4M4 11h16"/></svg> },
    { id: "insights", label: "Insights", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 19V10M12 19V5M19 19v-7"/></svg> },
    { id: "report", label: "Report", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M7 3h8l5 5v13H7z"/><path d="M15 3v5h5"/></svg> },
    { id: "community", label: "Community", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="9" cy="8" r="3"/><circle cx="16" cy="9" r="2.4"/><path d="M3.5 19c.6-3 2.8-5 5.5-5s4.9 2 5.5 5"/></svg> },
    { id: "discover", label: "Discover", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="9"/><path d="M14.5 9.5l-1.2 4.3-4.3 1.2 1.2-4.3z"/></svg> },
  ];'''
if old_bottom in s:
    s = s.replace(old_bottom, new_bottom, 1)
    print("nav icons")

s = s.replace('<span className="child-bar-label">Child</span>', '<span className="child-bar-label">CHILD</span>', 1)
s = s.replace('onClick={() => setShowChildModal(true)}>Manage</button>', 'onClick={() => setShowChildModal(true)}>Manage ›</button>', 1)

for must in ["ql-sun", "owned-card", "Mockup polish", "faces"]:
    if must not in s:
        raise SystemExit("missing " + must)

p.write_text(s, encoding="utf-8")
print("wrote", p, p.stat().st_size)
