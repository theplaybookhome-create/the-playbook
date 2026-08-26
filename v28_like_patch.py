#!/usr/bin/env python3
"""V28 like-for-like mockup patcher."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
HERE = pathlib.Path(__file__).resolve().parent
t = ROOT.read_text(encoding="utf-8")
b64 = (HERE / "sunrise.b64").read_text(encoding="utf-8").strip()

def sub(old, new, name, required=True):
    global t
    if old not in t:
        print("skip" if new[:60] in t or old[:40] not in t else "MISSING", name)
        return (new[:60] in t) or (not required)
    t = t.replace(old, new, 1)
    print("ok", name)
    return True

ok = True
ok &= sub("THEME_BUILD_V27", "THEME_BUILD_V28", "theme")
ok &= sub("./sw.js?v=27", "./sw.js?v=28", "swq", required=False)

si = t.find('<svg className="ql-sun"')
if si >= 0:
    se = t.find("</svg>", si)
    t = t[:si] + '<img className="ql-sun ql-sun-art" alt="" aria-hidden="true" src="' + b64 + '" />' + t[se+6:]
    print("ok sun")
elif "ql-sun-art" in t:
    print("skip sun")
else:
    print("MISSING sun"); ok = False

ok &= sub(
    """            <span className=\"cb-text\">\n              <strong>{s.label}</strong>\n              <span>{s.hint}</span>\n            </span>\n          </a>""",
    """            <span className=\"cb-text\">\n              <strong>{s.label}</strong>\n              <span>{s.hint}</span>\n            </span>\n            <span className=\"cb-chev\" aria-hidden=\"true\">›</span>\n          </a>""",
    "chev", required=False)

ok &= sub(
    '<p className="sub">Track what matters. Build what lasts.</p>',
    '<p className="sub">Logging for <strong>{activeChildName || "My child"}</strong> · track what matters.</p>',
    "greet", required=False)

ok &= sub(">Save quick log</button>", ">Save quick log <span aria-hidden=\"true\">›</span></button>", "save", required=False)

OLD_H = """      <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />\n      <ConnectCard />\n      <div className=\"progress-row\">"""
NEW_H = """      <div className=\"home-mid\">\n        <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />\n        <div className=\"home-side\">\n          <div className=\"side-card energy-side\" role=\"button\" tabIndex={0} onClick={() => onNavigate(\"insights\")}>\n            <div className=\"side-card-h\">ENERGY ({recentEnergy.length} LOGS) <span>›</span></div>\n            <div className=\"spark-embed\"><EnergySpark values={recentEnergy} avg={avgEnergy} /></div>\n            <div className=\"side-avg\">{avgEnergy || \"—\"}</div>\n            <div className=\"side-hint\">Your average lately</div>\n          </div>\n          <div className=\"side-card logs-side\" role=\"button\" tabIndex={0} onClick={() => onNavigate(\"track\", \"daily\")}>\n            <div className=\"side-card-h\">LOGS THIS DEVICE <span>›</span></div>\n            <div className=\"side-avg\">{daily.length + behavior.length}</div>\n            <div className=\"side-hint\">Daily + behaviour</div>\n          </div>\n        </div>\n      </div>\n      <ConnectCard />\n      <div className=\"progress-row\" style={{ display: \"none\" }}>"""
ok &= sub(OLD_H, NEW_H, "layout")

CSS = """\n/* ===== V28 like-for-like mockup ===== */\n.app-header { background:#15202B !important; color:#fff !important; padding:16px 22px 14px !important; border-bottom:none !important; }\n.menu-btn { display:none !important; }\n.brand { color:#fff !important; }\n.brand-sub { color:rgba(255,255,255,.62) !important; }\n.header-btn, .header-pill { background:#1C2A38 !important; border:1px solid rgba(255,255,255,.14) !important; color:#fff !important; border-radius:12px !important; padding:8px 14px !important; display:inline-flex !important; align-items:center !important; gap:8px !important; box-shadow:none !important; }\n.header-chips { display:flex !important; background:#121C26 !important; }\n.header-chips .hchip { display:inline-flex !important; background:transparent !important; border:none !important; color:rgba(255,255,255,.72) !important; }\n.child-bar { display:flex !important; margin-top:12px !important; padding-top:12px !important; border-top:1px solid rgba(255,255,255,.08) !important; }\n.child-chip.active { background:#E8892C !important; border-color:#E8892C !important; }\n.app-main { max-width:1080px !important; }\n.home-greet .sub strong { color:#E07A1A; }\n.home-mid { display:grid; grid-template-columns:minmax(0,1.7fr) minmax(240px,.7fr); gap:14px; margin:0 0 16px; }\n.home-side { display:flex; flex-direction:column; gap:12px; }\n.side-card { background:#fff; border:1px solid #E8ECF0; border-radius:20px; padding:16px; }\n.quick-log-card { position:relative !important; overflow:hidden !important; min-height:280px; padding:18px 220px 18px 18px !important; }\n.ql-sun, .ql-sun-art { position:absolute !important; right:8px !important; top:8px !important; width:210px !important; height:240px !important; object-fit:contain !important; object-position:top right !important; pointer-events:none !important; opacity:1 !important; }\n.ql-body { position:relative; z-index:1; }\n.connect-links { display:grid !important; grid-template-columns:repeat(4,minmax(0,1fr)) !important; gap:12px !important; }\n.connect-btn { display:flex !important; flex-direction:row !important; align-items:center !important; gap:10px !important; background:#fff !important; border:1.5px solid #E8ECF0 !important; border-radius:16px !important; padding:10px 12px !important; min-height:64px !important; text-align:left !important; }\n.connect-btn .cb-text { align-items:flex-start !important; text-align:left !important; }\n.connect-btn .cb-chev { margin-left:auto; color:#C4CAD1; font-size:20px; }\n.connect-btn::after { content:none !important; }\n.connect-btn.em .cb-ico { background:#E8892C !important; }\n.quick-links { grid-template-columns:repeat(3,1fr) !important; }\n.bottom-nav { background:#15202B !important; border:none !important; max-width:920px !important; }\n.bottom-btn { color:rgba(255,255,255,.55) !important; }\n.bottom-btn.active, .bottom-btn.active .lbl { color:#E07A1A !important; }\n@media (max-width:859px) {\n  .home-mid { grid-template-columns:1fr !important; }\n  .quick-log-card { padding:16px !important; }\n  .ql-sun, .ql-sun-art { width:150px !important; height:170px !important; }\n  .connect-links { grid-template-columns:1fr 1fr !important; }\n}\n"""

if "/* ===== V28 like-for-like mockup ===== */" not in t:
    if "/* V27 connect + sunrise */" in t:
        t = t.replace("/* V27 connect + sunrise */", CSS + "\n/* V27 connect + sunrise */", 1)
        print("ok css")
    elif "@media print {" in t:
        t = t.replace("@media print {", CSS + "\n@media print {", 1)
        print("ok css-print")
    else:
        print("MISSING css"); ok = False
else:
    print("skip css")

if not ok:
    sys.exit(1)
ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT, len(t))
