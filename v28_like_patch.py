#!/usr/bin/env python3
"""V28 like-for-like mockup: mountain sunrise + 4 social cards + dark header."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")

NEW_SUN = '''<svg className="ql-sun ql-sun-art" viewBox="0 0 280 320" aria-hidden="true">
        <defs>
          <linearGradient id="v28sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#FFF7EC"/>
            <stop offset="0.45" stopColor="#F8E4C4"/>
            <stop offset="1" stopColor="#FFFFFF" stopOpacity="0"/>
          </linearGradient>
          <radialGradient id="v28glow" cx="58%" cy="30%" r="38%">
            <stop offset="0" stopColor="#FFE09A"/>
            <stop offset="0.45" stopColor="#F2B03A" stopOpacity="0.55"/>
            <stop offset="1" stopColor="#F2B03A" stopOpacity="0"/>
          </radialGradient>
          <linearGradient id="v28far" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#F6E6CF"/>
            <stop offset="1" stopColor="#EED9B8"/>
          </linearGradient>
          <linearGradient id="v28mid" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#E8D0B0"/>
            <stop offset="1" stopColor="#D9B992"/>
          </linearGradient>
          <linearGradient id="v28near" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#C5D3E0"/>
            <stop offset="1" stopColor="#8FA6BB"/>
          </linearGradient>
        </defs>
        <rect width="280" height="320" fill="url(#v28sky)"/>
        <circle cx="162" cy="96" r="78" fill="url(#v28glow)"/>
        <circle cx="162" cy="96" r="40" fill="#F3B445"/>
        <circle cx="162" cy="96" r="34" fill="#F6C25A"/>
        <path d="M8 86 q18-10 34 2" fill="none" stroke="#D7A56A" strokeWidth="1.6" strokeLinecap="round"/>
        <path d="M210 72 q16-8 30 1" fill="none" stroke="#D7A56A" strokeWidth="1.5" strokeLinecap="round"/>
        <path d="M0 168 L38 128 L62 148 L96 108 L128 138 L162 98 L198 132 L228 112 L280 150 L280 220 L0 220 Z" fill="url(#v28far)" opacity="0.95"/>
        <path d="M0 188 L48 150 L78 168 L118 132 L158 162 L198 140 L248 166 L280 152 L280 240 L0 240 Z" fill="url(#v28mid)"/>
        <path d="M0 230 L42 188 L86 214 L132 176 L176 208 L230 184 L280 206 L280 320 L0 320 Z" fill="url(#v28near)" opacity="0.92"/>
        <path d="M48 84 q8-7 16 0" fill="none" stroke="#C48A4A" strokeWidth="1.5" strokeLinecap="round"/>
        <path d="M220 78 q7-6 14 0" fill="none" stroke="#C48A4A" strokeWidth="1.4" strokeLinecap="round"/>
        <path d="M246 92 q6-5 12 0" fill="none" stroke="#C48A4A" strokeWidth="1.3" strokeLinecap="round"/>
      </svg>'''

def sub(old, new, name, required=True):
    global t
    if old not in t:
        print("skip" if (new[:50] in t) else "MISSING", name)
        return (new[:50] in t) or (not required)
    t = t.replace(old, new, 1)
    print("ok", name)
    return True

ok = True
ok &= sub("THEME_BUILD_V27", "THEME_BUILD_V28", "theme")
ok &= sub("./sw.js?v=27", "./sw.js?v=28", "swq", required=False)

si = t.find('<svg className="ql-sun"')
if "v28sky" in t:
    print("skip sun")
elif si >= 0:
    se = t.find("</svg>", si)
    t = t[:si] + NEW_SUN + t[se+6:]
    print("ok sun-svg")
else:
    print("MISSING sun"); ok = False

ok &= sub(
    '<p className="sub">Track what matters. Build what lasts.</p>',
    '<p className="sub">Logging for <strong>{activeChildName || "My child"}</strong> · track what matters.</p>',
    "greet", required=False)

ok &= sub(">Save quick log</button>",
          ">Save quick log <span aria-hidden=\"true\">›</span></button>",
          "save", required=False)

OLD_H = """      <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />\n      <ConnectCard />\n      <div className=\"progress-row\">"""
NEW_H = """      <div className=\"home-mid\">\n        <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />\n        <div className=\"home-side\">\n          <div className=\"side-card energy-side\" role=\"button\" tabIndex={0} onClick={() => onNavigate(\"insights\")}>\n            <div className=\"side-card-h\">ENERGY ({recentEnergy.length} LOGS) <span>›</span></div>\n            <div className=\"spark-embed\"><EnergySpark values={recentEnergy} avg={avgEnergy} /></div>\n            <div className=\"side-avg\">{avgEnergy || \"—\"}</div>\n            <div className=\"side-hint\">Your average lately</div>\n          </div>\n          <div className=\"side-card logs-side\" role=\"button\" tabIndex={0} onClick={() => onNavigate(\"track\", \"daily\")}>\n            <div className=\"side-card-h\">LOGS THIS DEVICE <span>›</span></div>\n            <div className=\"side-avg\">{daily.length + behavior.length}</div>\n            <div className=\"side-hint\">Daily + behaviour</div>\n          </div>\n        </div>\n      </div>\n      <ConnectCard />\n      <div className=\"progress-row\" style={{ display: \"none\" }}>"""
ok &= sub(OLD_H, NEW_H, "layout", required=False)

if 'cb-chev' not in t:
    t = t.replace(
        """            <span className=\"cb-text\">\n              <strong>{s.label}</strong>\n              <span>{s.hint}</span>\n            </span>\n          </a>""",
        """            <span className=\"cb-text\">\n              <strong>{s.label}</strong>\n              <span>{s.hint}</span>\n            </span>\n            <span className=\"cb-chev\" aria-hidden=\"true\">›</span>\n          </a>""", 1)
    print("ok chev")

CSS = """\n/* ===== V28 like-for-like mockup ===== */\n.app-header { background:#15202B !important; color:#fff !important; padding:16px 22px 14px !important; border-bottom:none !important; }\n.menu-btn { display:none !important; }\n.brand { color:#fff !important; }\n.brand-sub { color:rgba(255,255,255,.62) !important; }\n.header-btn, .header-pill { background:#1C2A38 !important; border:1px solid rgba(255,255,255,.14) !important; color:#fff !important; border-radius:12px !important; padding:8px 14px !important; display:inline-flex !important; align-items:center !important; gap:8px !important; box-shadow:none !important; }\n.header-chips { display:flex !important; background:#121C26 !important; margin-top:14px !important; padding:8px 12px !important; border-radius:14px !important; }\n.header-chips .hchip { display:inline-flex !important; background:transparent !important; border:none !important; color:rgba(255,255,255,.72) !important; }\n.child-bar { display:flex !important; margin-top:12px !important; padding-top:12px !important; border-top:1px solid rgba(255,255,255,.08) !important; }\n.child-chip.active { background:#E8892C !important; border-color:#E8892C !important; color:#fff !important; }\n.app-main { max-width:1080px !important; }\n.home-greet .sub strong { color:#E07A1A; }\n.home-mid { display:grid; grid-template-columns:minmax(0,1.7fr) minmax(240px,.7fr); gap:14px; margin:0 0 16px; }\n.home-side { display:flex; flex-direction:column; gap:12px; }\n.side-card { background:#fff; border:1px solid #E8ECF0; border-radius:20px; padding:16px; }\n.side-card-h { display:flex; justify-content:space-between; font-size:11px; font-weight:800; letter-spacing:.06em; color:#6B7280; }\n.side-avg { font-size:28px; font-weight:800; color:#111827; margin-top:8px; }\n.side-hint { font-size:12px; color:#9CA3AF; }\n.quick-log-card { position:relative !important; overflow:hidden !important; min-height:280px; padding:18px 220px 18px 18px !important; }\n.ql-sun, .ql-sun-art { position:absolute !important; right:4px !important; top:4px !important; width:220px !important; height:250px !important; opacity:1 !important; pointer-events:none !important; }\n.ql-body { position:relative; z-index:1; }\n.connect-links { display:grid !important; grid-template-columns:repeat(4,minmax(0,1fr)) !important; gap:12px !important; }\n.connect-btn { display:flex !important; flex-direction:row !important; align-items:center !important; gap:10px !important; background:#fff !important; border:1.5px solid #E8ECF0 !important; border-radius:16px !important; padding:10px 12px !important; min-height:64px !important; text-align:left !important; }\n.connect-btn .cb-text { align-items:flex-start !important; text-align:left !important; }\n.connect-btn .cb-chev { margin-left:auto; color:#C4CAD1; font-size:20px; }\n.connect-btn::after { content:none !important; }\n.connect-btn.em .cb-ico { background:#E8892C !important; }\n.quick-links { grid-template-columns:repeat(3,1fr) !important; }\n.bottom-nav { background:#15202B !important; border:none !important; max-width:920px !important; }\n.bottom-btn { color:rgba(255,255,255,.55) !important; }\n.bottom-btn.active, .bottom-btn.active .lbl { color:#E07A1A !important; }\n@media (max-width:859px) {\n  .home-mid { grid-template-columns:1fr !important; }\n  .quick-log-card { padding:16px !important; }\n  .ql-sun, .ql-sun-art { width:150px !important; height:170px !important; }\n  .connect-links { grid-template-columns:1fr 1fr !important; }\n}\n"""

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

if "ql-sun-art" not in t:
    print("MISSING ql-sun-art"); ok = False

if not ok:
    sys.exit(1)
ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT, len(t))
