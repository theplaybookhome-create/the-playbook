#!/usr/bin/env python3
"""V30: implement the vanilla-CSS tablet spec (orange active rule + premium cards)."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")

def sub(old, new, name, required=True):
    global t
    if old not in t:
        print("skip" if new[:36] in t else "MISSING", name)
        return (new[:36] in t) or (not required)
    t = t.replace(old, new, 1)
    print("ok", name)
    return True

ok = True
ok &= sub("THEME_BUILD_V29", "THEME_BUILD_V30", "theme")
ok &= sub("./sw.js?v=29", "./sw.js?v=30", "swq", required=False)
ok &= sub("./sw.js?v=28", "./sw.js?v=30", "swq28", required=False)
ok &= sub("<h3>Quick log</h3>", "<h3>QUICK LOG</h3>", "ql-title", required=False)

CSS = r"""
/* ===== V30 tablet spec ===== */
:root {
  --spec-bg: #F4F6F8;
  --spec-navy: #0E131F;
  --spec-orange: #FF6B00;
  --spec-card: #FFFFFF;
  --spec-line: #E2E8F0;
  --spec-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}
html, body, #root, .app-root {
  background: var(--spec-bg) !important;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}
.app-header {
  background: #0E131F !important;
  color: #FFFFFF !important;
  border-bottom: none !important;
}
.brand, .brand-sub, .app-header, .header-top {
  color: #FFFFFF !important;
}
.brand-sub { color: rgba(255,255,255,.62) !important; }
.card, .quick-log-card, .energy-spark, .stat-card, .connect-card,
.quick-link, .why-card, .paywall-card, .home-side .energy-spark,
.home-side .stat-card, .energy-spark-wrap, .side-card {
  background: #FFFFFF !important;
  border-radius: 20px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
  border: 1px solid #E8ECF0 !important;
}
.quick-log-card,
.energy-spark,
.stat-card,
.quick-link,
.connect-card,
.why-card {
  padding: 24px !important;
}
.scale-btn,
.tick-chip,
.hchip,
.header-chips .hchip,
.header-chips span,
.bottom-btn {
  border: 1px solid #E2E8F0 !important;
  box-sizing: border-box !important;
}
.hchip, .header-chips .hchip, .header-chips span, .bottom-btn {
  border-color: transparent !important;
}
.scale-btn.active,
.scale-btn:focus-visible,
.tick-chip.active,
.tick-chip:focus-visible,
.hchip.active,
.hchip:focus-visible,
.header-chips .hchip.active,
.header-chips .hchip:focus-visible,
.header-chips span.active,
.header-chips span:focus-visible,
.bottom-btn.active,
.bottom-btn:focus-visible {
  border: 2px solid #FF6B00 !important;
  outline: none !important;
}
.scale-btn {
  width: 48px !important;
  height: 48px !important;
  border-radius: 14px !important;
  background: #fff !important;
  color: #4B5563 !important;
  font-weight: 800 !important;
}
.scale-btn.active {
  background: linear-gradient(180deg, #FF8A2B, #FF6B00) !important;
  color: #fff !important;
}
.tick-chip {
  background: #fff !important;
  border-radius: 999px !important;
}
.tick-chip.active {
  background: #FFF4EB !important;
  color: #0E131F !important;
}
.bottom-nav {
  background: #0E131F !important;
}
.bottom-btn { color: rgba(255,255,255,.55) !important; }
.bottom-btn.active,
.bottom-btn.active .lbl {
  color: #FF6B00 !important;
}
.ql-head h3 {
  text-transform: uppercase !important;
  letter-spacing: .08em !important;
  font-size: 13px !important;
  font-weight: 800 !important;
}
.btn-primary {
  background: #0E131F !important;
  color: #fff !important;
  border-radius: 12px !important;
}
"""

if "/* ===== V30 tablet spec ===== */" in t:
    print("skip css")
elif "/* ===== V29 mockup home ===== */" in t:
    t = t.replace("/* ===== V29 mockup home ===== */", CSS + "\n/* ===== V29 mockup home ===== */", 1)
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
