#!/usr/bin/env python3
"""V29: match the Lewis tablet mockup — real sunrise crop, side cards, hide leftovers."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
URI = (HERE / "sunrise.b64").read_text(encoding="utf-8").strip()

def sub(old, new, name, required=True):
    global t
    if old not in t:
        print("skip" if new[:40] in t else "MISSING", name)
        return (new[:40] in t) or (not required)
    t = t.replace(old, new, 1)
    print("ok", name)
    return True

ok = True
ok &= sub("THEME_BUILD_V28", "THEME_BUILD_V29", "theme")
ok &= sub("./sw.js?v=28", "./sw.js?v=29", "swq", required=False)
ok &= sub("./sw.js?v=27", "./sw.js?v=29", "swq27", required=False)

si = t.find('<svg className="ql-sun')
if "ql-sun-photo" in t:
    print("skip sun")
elif si >= 0:
    se = t.find("</svg>", si)
    t = t[:si] + '<img className="ql-sun ql-sun-photo" alt="" aria-hidden="true" src="' + URI + '" />' + t[se+6:]
    print("ok sun")
else:
    print("MISSING sun"); ok = False

OLD_A = '''            <button type="button" className="header-btn header-ico" title="Import backup" onClick={() => fileInputRef.current?.click()}>
              <svg viewBox="0 0 24 24"><path d="M6 18h12M12 4v10M8 10l4 4 4-4"/></svg>
            </button>
            <button type="button" className="header-btn header-ico" title="Export backup" onClick={handleExport}>
              <svg viewBox="0 0 24 24"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 21h14"/></svg>
            </button>
            <button type="button" className="header-btn header-ico" title="Alerts" onClick={() => showToast("You're all caught up")}>
              <svg viewBox="0 0 24 24"><path d="M6 17h12l-1.2-2.2a6 6 0 0 1-.8-3.1V10a5 5 0 0 0-10 0v1.7c0 1.1-.3 2.1-.8 3.1L6 17z"/><path d="M10 17v1a2 2 0 0 0 4 0v-1"/></svg>
            </button>'''
NEW_A = '''            <button type="button" className="header-btn header-pill hdr-exim" title="Export backup" onClick={handleExport}>
              <svg viewBox="0 0 24 24" width="16" height="16"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 21h14"/></svg>
              Export
            </button>
            <button type="button" className="header-btn header-pill hdr-exim" title="Import backup" onClick={() => fileInputRef.current?.click()}>
              <svg viewBox="0 0 24 24" width="16" height="16"><path d="M6 18h12M12 4v10M8 10l4 4 4-4"/></svg>
              Import
            </button>'''
ok &= sub(OLD_A, NEW_A, "header")

ok &= sub(
    '<div className="progress-row">',
    '<div className="progress-row" style={{ display: "none" }}>',
    "hide-progress",
)

CSS = r"""
/* ===== V29 mockup home ===== */
.app-main { max-width: 1100px !important; padding-bottom: 120px !important; }
.app-root { padding-bottom: 120px !important; }
.menu-btn { display: none !important; }
.header-actions .signout-quiet { display: none !important; }
.hdr-exim { display: inline-flex !important; align-items: center !important; gap: 7px !important; padding: 8px 14px !important; }
.hdr-exim svg { stroke: currentColor; fill: none; stroke-width: 2; }
.home-hero {
  display: grid !important;
  grid-template-columns: minmax(0, 1.75fr) minmax(250px, 0.72fr) !important;
  gap: 14px !important;
  align-items: stretch !important;
  margin-bottom: 16px !important;
}
.home-side { display: flex !important; flex-direction: column !important; gap: 12px !important; }
.energy-spark-wrap, .home-side .stat-card, .home-side .energy-spark {
  display: block !important;
  background: #fff !important;
  border: 1px solid #E8ECF0 !important;
  border-radius: 20px !important;
  box-shadow: 0 8px 24px rgba(15,24,34,.04) !important;
}
.home-side .energy-spark { padding: 16px !important; }
.home-side .es-top, .home-side .es-big, .home-side .es-hint { display: block !important; }
.home-side .es-dots, .home-side .es-empty { display: block !important; }
.quick-log-card {
  position: relative !important;
  overflow: hidden !important;
  min-height: 300px !important;
  padding: 18px 210px 16px 18px !important;
  background: #fff !important;
  border: 1px solid #E8ECF0 !important;
}
.ql-sun, .ql-sun-art, .ql-sun-photo {
  position: absolute !important;
  right: 0 !important;
  top: 8px !important;
  width: 210px !important;
  height: 240px !important;
  object-fit: contain !important;
  object-position: top right !important;
  pointer-events: none !important;
  opacity: 1 !important;
  border: none !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}
.ql-body { position: relative; z-index: 1; }
.ql-head h3 {
  text-transform: uppercase !important;
  letter-spacing: .08em !important;
  font-size: 13px !important;
  font-weight: 800 !important;
}
.progress-row, .inside-card { display: none !important; }
.connect-links {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 12px !important;
}
.connect-btn {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 10px !important;
  background: #fff !important;
  border: 1.5px solid #E8ECF0 !important;
  border-radius: 16px !important;
  padding: 10px 12px !important;
  min-height: 64px !important;
  text-align: left !important;
}
.connect-btn .cb-text { align-items: flex-start !important; text-align: left !important; }
.connect-btn .cb-text strong { font-size: 13px !important; }
.connect-btn .cb-chev, .connect-btn::after { margin-left: auto; color: #C4CAD1; font-size: 20px; }
.connect-btn.em .cb-ico { background: #E8892C !important; }
.quick-links {
  display: grid !important;
  grid-template-columns: 1fr 1fr 1fr minmax(200px, 0.85fr) !important;
  gap: 12px !important;
  align-items: stretch !important;
}
.quick-link.t-disc { display: none !important; }
.quick-links .why-card, .quick-links .why-banner {
  grid-column: 4 !important;
  grid-row: 1 / span 2 !important;
  background: #fff !important;
  border: 1px solid #E8ECF0 !important;
}
.bottom-nav {
  background: #15202B !important;
  border: none !important;
  max-width: 980px !important;
  z-index: 40 !important;
}
@media (max-width: 859px) {
  .home-hero { grid-template-columns: 1fr !important; }
  .quick-log-card { padding: 16px !important; min-height: 0 !important; }
  .ql-sun, .ql-sun-art, .ql-sun-photo { width: 140px !important; height: 160px !important; }
  .connect-links { grid-template-columns: 1fr 1fr !important; }
  .quick-links { grid-template-columns: 1fr 1fr !important; }
  .quick-link.t-disc { display: flex !important; }
  .quick-links .why-card { grid-column: auto !important; grid-row: auto !important; }
}
"""

if "/* ===== V29 mockup home ===== */" in t:
    print("skip css")
elif "/* ===== V28 like-for-like mockup ===== */" in t:
    t = t.replace("/* ===== V28 like-for-like mockup ===== */", CSS + "\n/* ===== V28 like-for-like mockup ===== */", 1)
    print("ok css")
elif "@media print {" in t:
    t = t.replace("@media print {", CSS + "\n@media print {", 1)
    print("ok css-print")
else:
    print("MISSING css"); ok = False

if not ok:
    sys.exit(1)
ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT, len(t))
