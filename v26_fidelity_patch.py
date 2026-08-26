#!/usr/bin/env python3
"""V26: closer match to Tuesday tablet mockup header + home copy."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")

def sub(old, new, name, required=True):
    global t
    if old not in t:
        if new in t:
            print("skip", name)
            return True
        print("MISSING", name)
        return not required
    t = t.replace(old, new, 1)
    print("ok", name)
    return True

ok = True
ok &= sub("THEME_BUILD_V25", "THEME_BUILD_V26", "theme")
ok &= sub("THEME_BUILD_V24", "THEME_BUILD_V26", "theme24", required=False)
ok &= sub("./sw.js?v=25", "./sw.js?v=26", "swq")
ok &= sub("./sw.js?v=24", "./sw.js?v=26", "swq24", required=False)

ok &= sub(
    '<p className="sub">"Track what matters. Build what lasts."</p>',
    '<p className="sub">Track what matters. Build what lasts.</p>',
    "tagline-quotes",
)
ok &= sub("Save quick log ›", "Save quick log", "save-label")

OLD_HEADER = '''        <div className="header-top">
          <div>
            <div className="brand"><img className="brand-mark-img" src="icon-192.png" width="28" height="28" alt="" />THE PLAYBOOK</div>
            <div className="brand-sub">{unlocked ? "Full access on this device" : "Track free · unlock once"}{user ? " · " + (user.email || "signed in") : ""}</div>
          </div>
          <div className="header-actions">
            {!unlocked && <button type="button" className="header-btn header-pill" onClick={requestUnlock}>{PREMIUM_PRICE}</button>}
            <button type="button" className="header-btn header-pill ico-btn" onClick={handleExport}><svg viewBox="0 0 24 24"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 21h14"/></svg>Export</button>
            <button type="button" className="header-btn header-pill ico-btn" onClick={() => fileInputRef.current?.click()}><svg viewBox="0 0 24 24"><path d="M12 21V9"/><path d="M7 16l5 5 5-5"/><path d="M5 3h14"/></svg>Import</button>
            {CLOUD_ENABLED && user ? <button type="button" className="header-btn header-pill signout-quiet" onClick={handleSignOut}>Sign out</button> : (
              <a className="header-btn header-pill" href="./app.html?login=1">Log in</a>
            )}
            {user ? <div className="header-avatar" title={user.email || ""}>{initialsOf(user)}<span className="dot" /></div> : null}
            <input ref={fileInputRef} type="file" accept="application/json,.json" className="hidden-file" onChange={(e) => handleImport(e.target.files?.[0])} />
          </div>
        </div>'''

NEW_HEADER = '''        <div className="header-top">
          <button type="button" className="menu-btn" aria-label="Menu" onClick={() => setShowChildModal(true)}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
          </button>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="brand"><img className="brand-mark-img" src="icon-192.png" width="28" height="28" alt="" />THE PLAYBOOK</div>
            <div className="brand-sub">{unlocked ? "Full access on this device" : "Track free · unlock once"}{user ? " · " + (user.email || "signed in") : ""}</div>
          </div>
          <div className="header-actions">
            {!unlocked && <button type="button" className="header-btn header-pill" onClick={requestUnlock}>{PREMIUM_PRICE}</button>}
            <button type="button" className="header-btn header-ico" title="Import backup" onClick={() => fileInputRef.current?.click()}>
              <svg viewBox="0 0 24 24"><path d="M6 18h12M12 4v10M8 10l4 4 4-4"/></svg>
            </button>
            <button type="button" className="header-btn header-ico" title="Export backup" onClick={handleExport}>
              <svg viewBox="0 0 24 24"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 21h14"/></svg>
            </button>
            <button type="button" className="header-btn header-ico" title="Alerts" onClick={() => showToast("You're all caught up")}>
              <svg viewBox="0 0 24 24"><path d="M6 17h12l-1.2-2.2a6 6 0 0 1-.8-3.1V10a5 5 0 0 0-10 0v1.7c0 1.1-.3 2.1-.8 3.1L6 17z"/><path d="M10 17v1a2 2 0 0 0 4 0v-1"/></svg>
            </button>
            {CLOUD_ENABLED && user ? <button type="button" className="header-btn header-pill signout-quiet" onClick={handleSignOut}>Sign out</button> : null}
            {user ? <div className="header-avatar" title={user.email || ""}>{initialsOf(user)}<span className="dot" /></div> : (
              <button type="button" className="header-btn header-pill" onClick={() => {
                try {
                  const url = new URL(window.location.href);
                  url.searchParams.set("login", "1");
                  window.history.replaceState({}, "", url.pathname + url.search + url.hash);
                } catch (e) {}
                window.location.search = (window.location.search ? window.location.search + "&" : "?") + "login=1";
              }}>Log in</button>
            )}
            <input ref={fileInputRef} type="file" accept="application/json,.json" className="hidden-file" onChange={(e) => handleImport(e.target.files?.[0])} />
          </div>
        </div>'''

ok &= sub(OLD_HEADER, NEW_HEADER, "header")

CSS_ADD = """
.child-bar { display: none !important; }
.ql-head h3, .quick-log-card h3 {
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-size: 17px !important;
  font-weight: 800 !important;
  color: #111827 !important;
}
.header-btn.header-ico { font-size: 0 !important; color: transparent !important; }
"""

if ".child-bar { display: none !important; }" not in t:
    marker = "@media print {"
    if marker in t:
        t = t.replace(marker, CSS_ADD + "\n@media print {", 1)
        print("ok css")
    else:
        print("MISSING css-anchor")
        ok = False
else:
    print("skip css")

ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT, "ok" if ok else "PARTIAL")
if not ok:
    sys.exit(1)
