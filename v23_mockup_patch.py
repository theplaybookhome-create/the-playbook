#!/usr/bin/env python3
"""Match THE PLAYBOOK home screen to the tablet mockup (V23)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
text = ROOT.read_text(encoding="utf-8")
orig = text

def swap(old, new, label):
    global text
    if old in text:
        text = text.replace(old, new, 1)
        print("ok", label)
        return True
    if new in text:
        print("skip", label)
        return True
    print("MISSING", label)
    return False

swap("THEME_BUILD_V22", "THEME_BUILD_V23", "theme")
swap("THEME_BUILD_V21", "THEME_BUILD_V23", "theme21")
swap("./sw.js?v=21", "./sw.js?v=23", "swq21")
swap("./sw.js?v=22", "./sw.js?v=23", "swq22")

swap(
    '{!compact && <p style={{ margin: "4px 0 0", fontSize: 12.5, color: "var(--soft)" }}>Insights, report, Discover, Printables & more unlocked.</p>}',
    '<p style={{ margin: "4px 0 0", fontSize: 12.5, color: "var(--soft)", lineHeight: 1.35 }}>Insights, report, Discover, Printables & more unlocked.</p>',
    "owned-copy",
)

swap(
    """          <div className=\"stat-card\">\n            <div className=\"stat-label\">Logs this device</div>\n            <div className=\"stat-value\">{daily.length + behavior.length}</div>\n            <div className=\"stat-hint\">Daily + behaviour</div>\n          </div>""",
    """          <div className=\"stat-card\">\n            <div className=\"es-top\">\n              <div className=\"stat-label\">Logs this device</div>\n              <div className=\"es-avg\" aria-hidden=\"true\">›</div>\n            </div>\n            <div className=\"stat-value\">{daily.length + behavior.length}</div>\n            <div className=\"stat-hint\">Daily + behaviour</div>\n          </div>""",
    "stat-head",
)

swap(
    '<div className="stat-label">Why unlock helps</div>',
    '<div className="stat-label">✓ Why unlock helps</div>',
    "why-label",
)

V23_CSS = """
/* ===== V23 mockup match ===== */
.header-chips { display: flex !important; }
.bottom-nav { display: flex !important; max-width: 860px !important; }
.app-root { padding-bottom: 108px !important; }
.es-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 4px; }
.owned-card p { display: block !important; }
.home-top {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(240px, 320px) !important;
  align-items: start !important;
  gap: 16px !important;
  margin-bottom: 16px !important;
}
.home-top .paywall-card,
.home-top .owned-card { width: 100%; max-width: 320px; margin: 0 0 0 auto !important; }
.home-hero {
  display: grid !important;
  grid-template-columns: minmax(0, 1.7fr) minmax(220px, 0.78fr) !important;
  gap: 14px !important;
  align-items: stretch !important;
}
.quick-log-card { min-height: 268px; padding-right: 196px !important; }
.ql-sun {
  width: 210px !important;
  height: 152px !important;
  right: 4px !important;
  top: 8px !important;
  opacity: 1 !important;
}
.connect-btn .cb-ico { border-radius: 50% !important; }
.connect-btn.em .cb-ico { background: #E8892C !important; border: none !important; }
.quick-links { grid-template-columns: repeat(3, 1fr) !important; }
.why-card { position: relative; padding-right: 28px !important; }
.why-card::after { content: "›"; position: absolute; right: 14px; top: 16px; color: #C4CAD1; font-size: 20px; }
.energy-spark svg { height: 78px; }
.bottom-btn.active .ico svg { stroke: #F08A2A; fill: #F08A2A; }
@media (max-width: 759px) {
  .home-top { grid-template-columns: 1fr !important; }
  .home-top .paywall-card,
  .home-top .owned-card { max-width: none; margin: 0 !important; }
  .home-hero { grid-template-columns: 1fr !important; }
  .quick-log-card { padding-right: 18px !important; min-height: 0; }
  .ql-sun { width: 120px !important; height: 88px !important; opacity: 0.8 !important; }
  .quick-links { grid-template-columns: 1fr 1fr !important; }
  .connect-links { grid-template-columns: 1fr 1fr !important; }
}
"""

if "V23 mockup match" not in text:
    if "/* ===== V22 desktop + empty-state polish ===== */" in text:
        start = text.find("/* ===== V22 desktop + empty-state polish ===== */")
        end = text.find("@media print {", start)
        if start >= 0 and end > start:
            text = text[:start] + V23_CSS + "\n" + text[end:]
            print("ok replace-v22-css")
        else:
            print("MISSING v22-css-end")
    elif ".brand-mark-img { width:28px;" in text:
        mark = ".brand-mark-img { width:28px; height:28px; border-radius:8px; object-fit:cover; flex-shrink:0; box-shadow:0 4px 10px rgba(11,18,25,.28); }"
        text = text.replace(mark, mark + "\n" + V23_CSS, 1)
        print("ok append-v23-css")
    else:
        print("MISSING css-anchor")
else:
    print("skip css")

if text != orig:
    ROOT.write_text(text, encoding="utf-8")
    print("patched", ROOT, "bytes", len(text.encode()))
else:
    print("no-op", ROOT)

print("markers", {
    "V23": "THEME_BUILD_V23" in text,
    "css": "V23 mockup match" in text,
    "chipsShown": ".header-chips { display: flex !important; }" in text,
    "navShown": ".bottom-nav { display: flex !important;" in text,
})
