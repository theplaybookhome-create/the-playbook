#!/usr/bin/env python3
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")

def sub(old, new, name):
    global t
    if old not in t:
        if new in t or name in ("owned-copy", "owned-copy2"):
            print("skip", name)
            return True
        print("MISSING", name)
        return False
    t = t.replace(old, new, 1)
    print("ok", name)
    return True

sub("THEME_BUILD_V24", "THEME_BUILD_V25", "theme")
sub('content="#0B1219"', 'content="#F4F6F8"', "theme-color")
sub('content="black-translucent"', 'content="default"', "status-bar")
sub("./sw.js?v=24", "./sw.js?v=25", "swq")

sub(
'''const SOCIAL_LINKS = [
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "email", label: "Email", href: "mailto:Theplaybookhome@gmail.com", hint: "Support" }
];''',
'''const SOCIAL_LINKS = [
  { id: "instagram", label: "Instagram", href: "https://www.instagram.com/theplaybookhome", hint: "Community" },
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X (Twitter)", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "youtube", label: "YouTube", href: "https://www.youtube.com/@theplaybookhome", hint: "Videos" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "email", label: "Email", href: "mailto:Theplaybookhome@gmail.com", hint: "Support" }
];''',
"social")

sub('const cls = { facebook: "fb", tiktok: "tt", x: "xx", email: "em" };',
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx", email: "em", instagram: "ig", youtube: "yt" };',
    "cls")

sub("Insights, report, Discover, Printables<br/>& more unlocked.", "Insights, reports, printables & more", "owned-copy")
sub("Insights, report, Discover, Printables & more unlocked.", "Insights, reports, printables & more", "owned-copy2")

old_g = '{activeChildName ? (<span>Logging for <b>{activeChildName}</b> · track what matters.</span>) : "Track what matters. Spot patterns. Look after yourself too."}'
if old_g in t:
    t = t.replace(old_g, '"Track what matters. Build what lasts."', 1)
    print("ok greet")
elif "Track what matters. Build what lasts." in t:
    print("skip greet")
else:
    print("MISSING greet")

if 'id === "instagram"' not in t:
    needle = 'function SocialIcon({ id }) {\n  if (id === "facebook") {'
    insert = '''function SocialIcon({ id }) {
  if (id === "instagram") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm10 1.8H7A2.2 2.2 0 0 0 4.8 7v10A2.2 2.2 0 0 0 7 19.2h10A2.2 2.2 0 0 0 19.2 17V7A2.2 2.2 0 0 0 17 4.8zM12 8.2A3.8 3.8 0 1 1 8.2 12 3.8 3.8 0 0 1 12 8.2zm0 1.6A2.2 2.2 0 1 0 14.2 12 2.2 2.2 0 0 0 12 9.8zM17.35 6.4a1 1 0 1 1-1 1 1 1 0 0 1 1-1z"/></svg>
    );
  }
  if (id === "youtube") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M23 12.2s0-3.2-.4-4.6c-.2-.9-.9-1.6-1.8-1.8C18.9 5.4 12 5.4 12 5.4s-6.9 0-8.8.4c-.9.2-1.6.9-1.8 1.8C1 9 1 12.2 1 12.2s0 3.2.4 4.6c.2.9.9 1.6 1.8 1.8 1.9.4 8.8.4 8.8.4s6.9 0 8.8-.4c.9-.2 1.6-.9 1.8-1.8.4-1.4.4-4.6.4-4.6zM9.8 15.5v-6.6l6.3 3.3-6.3 3.3z"/></svg>
    );
  }
  if (id === "facebook") {'''
    if needle in t:
        t = t.replace(needle, insert, 1)
        print("ok icons")
    else:
        print("MISSING icons")
else:
    print("skip icons")

old_b = '''    { id: "community", label: "Community", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="9" cy="8" r="3"/><circle cx="16" cy="9" r="2.4"/><path d="M3.5 19c.6-3 2.8-5 5.5-5s4.9 2 5.5 5"/></svg> },
    { id: "discover", label: "Discover", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="9"/><path d="M14.5 9.5l-1.2 4.3-4.3 1.2 1.2-4.3z"/></svg> },'''
new_b = '''    { id: "community", label: "Community", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="9" cy="8" r="3"/><circle cx="16" cy="9" r="2.4"/><path d="M3.5 19c.6-3 2.8-5 5.5-5s4.9 2 5.5 5"/></svg> },'''
sub(old_b, new_b, "bottom")

if "V25 light home" not in t:
    css_path = pathlib.Path(__file__).with_name("v25_light.css")
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else "/* ===== V25 light home (Tuesday mockup) ===== */\n.app-root{background:#F3F5F7!important}\n"
    marker = "/* ===== V24 mockup fidelity ===== */"
    endm = "@media print {"
    if marker in t and endm in t:
        i = t.find(marker)
        j = t.find(endm, i)
        t = t[:i] + css + "\n" + t[j:]
        print("ok css-replace")
    elif endm in t:
        j = t.find(endm)
        t = t[:j] + css + "\n" + t[j:]
        print("ok css-insert")
    else:
        print("MISSING css")
else:
    print("skip css")

if "What's inside" not in t:
    mark = "      <ConnectCard />\n      {null}"
    add = """      <ConnectCard />\n      <div className=\"progress-row\">\n        <div className=\"progress-card\" role=\"button\" tabIndex={0} onClick={() => onNavigate(\"insights\")}>\n          <h3>Your progress</h3>\n          <div className=\"progress-energy\">\n            <div>\n              <div className=\"pe-label\">Energy ({recentEnergy.length} logs)</div>\n              <div className=\"spark-embed\"><EnergySpark values={recentEnergy} avg={avgEnergy} /></div>\n            </div>\n            <div className=\"pe-avg\"><b>{avgEnergy}</b><span>Average</span></div>\n          </div>\n          <div className=\"progress-logs\">\n            <div className=\"pl-k\">Logs this device</div>\n            <div className=\"pl-v\"><b>{daily.length + behavior.length}</b><span>Daily + behaviour</span></div>\n          </div>\n        </div>\n        <div className=\"inside-card\">\n          <h3>What's inside</h3>\n          <ul className=\"inside-list\">\n            <li><span className=\"tick-ok\">OK</span> Track energy, mood & habits</li>\n            <li><span className=\"tick-ok\">OK</span> See patterns that matter</li>\n            <li><span className=\"tick-ok\">OK</span> Unlock reports & printables</li>\n            <li><span className=\"tick-ok\">OK</span> Join a support community</li>\n          </ul>\n        </div>\n      </div>"""
    if mark in t:
        t = t.replace(mark, add, 1)
        print("ok progress")
    else:
        print("MISSING connect-null")
else:
    print("skip progress")

if 'className="quick-link t-disc"' not in t:
    old_q = '<button type="button" className="quick-link t-print" onClick={() => onNavigate("discover", null, "printables")}><span className="ql-ico">🖨️</span><strong>Printables</strong><span className="ql-hint">Preview packs · download</span></button>'
    new_q = '''<button type="button" className="quick-link t-print" onClick={() => onNavigate("discover", null, "printables")}><span className="ql-ico">🖨️</span><span><strong>Printables</strong><span className="ql-hint">Preview packs · download</span></span></button>
        <button type="button" className="quick-link t-disc" onClick={() => onNavigate("discover")}><span className="ql-ico">*</span><span><strong>Discover</strong><span className="ql-hint">Tools, guides & more</span></span></button>'''
    if old_q in t:
        t = t.replace(old_q, new_q, 1)
        print("ok discover-card")
    else:
        print("MISSING print-btn")
else:
    print("skip discover-card")

if "why-banner" not in t and "why-card" in t:
    t = t.replace('className="why-card"', 'className="why-banner"', 1)
    t = t.replace('why-check">✓</span> Why unlock helps', 'why-info">i</span> Why unlock helps', 1)
    print("ok why")
else:
    print("skip why")

if "menu-btn" not in t and '<div className="header-top">' in t:
    t = t.replace(
        '<div className="header-top">\n          <div>',
        '''<div className="header-top">
          <button type="button" className="menu-btn" aria-label="Menu" onClick={() => setShowChildModal(true)}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
          </button>
          <div style={{ flex: 1, minWidth: 0 }}>''',
        1
    )
    print("ok menu")
else:
    print("skip menu")

ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT)
if "THEME_BUILD_V25" not in t:
    sys.exit(1)
