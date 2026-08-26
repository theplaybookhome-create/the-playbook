#!/usr/bin/env python3
"""V32: official brand social tiles + orange borders on connect and quick-link cards."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")

NEW_ICON = r'''/* V32 brand icons */
function SocialIcon({ id }) {
  if (id === "tiktok") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect width="48" height="48" rx="12" fill="#000"/>
        <path fill="#25F4EE" d="M31.1 12.4c1.1 2.6 3.4 4.6 6.2 5.3v4.4c-2.1-.05-4.1-.7-5.8-1.8v11.5c0 5.4-4.4 9.8-9.8 9.8-2.1 0-4-.7-5.6-1.8 1.8 1.8 4.2 2.9 6.9 2.9 5.4 0 9.8-4.4 9.8-9.8V20.5c1.8 1.2 3.9 1.9 6.2 2v-4.6c-2.9-.3-5.3-1.9-6.7-4.5h-1.2v-1z"/>
        <path fill="#FE2C55" d="M29.9 10.8c1.1 2.6 3.4 4.6 6.2 5.3v4.4c-2.1-.05-4.1-.7-5.8-1.8v11.5c0 5.4-4.4 9.8-9.8 9.8-2.1 0-4-.7-5.6-1.8 1.8 1.8 4.2 2.9 6.9 2.9 5.4 0 9.8-4.4 9.8-9.8V18.9c1.8 1.2 3.9 1.9 6.2 2v-4.6c-2.9-.3-5.3-1.9-6.7-4.5h-1.2V10.8z"/>
        <path fill="#fff" d="M29.3 11.6c1.05 2.5 3.2 4.45 5.85 5.2v3.55c-1.95-.04-3.8-.64-5.4-1.65V29.8c0 5.05-4.1 9.15-9.15 9.15-1.95 0-3.75-.6-5.2-1.65 1.65 1.7 3.95 2.75 6.5 2.75 5.05 0 9.15-4.1 9.15-9.15V19.1c1.65 1.1 3.65 1.75 5.8 1.85v-3.7c-2.7-.35-5-1.85-6.3-4.3V11.6h-.25z"/>
      </svg>
    );
  }
  if (id === "x") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect width="48" height="48" rx="12" fill="#000"/>
        <path fill="#fff" d="M26.7 22.3L36.4 11h-2.3l-8.4 9.8L18.9 11H11l10.2 14.8L11 37h2.3l8.9-10.4L29.1 37H37L26.7 22.3zm-3.2 3.7l-1-1.5-8.2-11.7h3.5l6.6 9.5 1 1.5 8.6 12.2h-3.5l-7-10z"/>
      </svg>
    );
  }
  if (id === "facebook") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect width="48" height="48" rx="12" fill="#1877F2"/>
        <path fill="#fff" d="M29.4 24.8h-4.1v14.7h-6.1V24.8h-2.9v-5.2h2.9v-3.4c0-2.9 1.4-7.4 7.4-7.4h4.3v4.8h-3.1c-.5 0-1.3.3-1.3 1.4v4.6h4.5l-.6 5.2z"/>
      </svg>
    );
  }
  if (id === "email") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect width="48" height="48" rx="12" fill="#34C759"/>
        <path fill="#fff" d="M10 16.2h28c1.2 0 2.2 1 2.2 2.2v11.2c0 1.2-1 2.2-2.2 2.2H10c-1.2 0-2.2-1-2.2-2.2V18.4c0-1.2 1-2.2 2.2-2.2zm1.2 2.4v.4l12.8 8.4 12.8-8.4v-.4H11.2zm25.6 12.2V21.4L24 30.2 11.2 21.4v9.4h25.6z"/>
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <rect width="48" height="48" rx="12" fill="#111"/>
    </svg>
  );
}

'''

WIN_CSS = r"""
/* ===== V32 WINNING brand tiles + orange card borders ===== */
.connect-links {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 14px !important;
  justify-items: stretch !important;
}
.connect-btn {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  gap: 8px !important;
  width: 100% !important;
  max-width: none !important;
  min-height: 0 !important;
  background: #FFFFFF !important;
  border: 2px solid #FF6B00 !important;
  border-radius: 16px !important;
  padding: 16px 8px 14px !important;
  text-align: center !important;
  box-shadow: none !important;
  position: relative !important;
}
.connect-btn::after,
.connect-btn .cb-chev {
  display: none !important;
  content: none !important;
}
.connect-btn .cb-text {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  gap: 2px !important;
}
.connect-btn .cb-text strong {
  font-size: 13px !important;
  font-weight: 800 !important;
  color: #111827 !important;
}
.connect-btn .cb-text span {
  font-size: 12px !important;
  font-weight: 500 !important;
  color: #6B7280 !important;
  max-width: none !important;
}
.connect-btn .cb-ico {
  width: 56px !important;
  height: 56px !important;
  min-width: 56px !important;
  border-radius: 14px !important;
  border: none !important;
  background: transparent !important;
  box-shadow: 0 8px 18px rgba(0,0,0,.16) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
  padding: 0 !important;
}
.connect-btn .cb-ico svg {
  width: 56px !important;
  height: 56px !important;
  display: block !important;
  fill: none !important;
  stroke: none !important;
  color: inherit !important;
}
.connect-btn.tt .cb-ico,
.connect-btn.xx .cb-ico,
.connect-btn.fb .cb-ico,
.connect-btn.em .cb-ico,
.connect-btn.ig .cb-ico,
.connect-btn.yt .cb-ico {
  background: transparent !important;
  border: none !important;
}
.quick-link {
  border: 2px solid #FF6B00 !important;
  border-radius: 16px !important;
  background: #FFFFFF !important;
  box-shadow: 0 4px 20px rgba(0,0,0,.04) !important;
}
@media (max-width: 859px) {
  .connect-links { grid-template-columns: 1fr 1fr !important; }
}
"""

ok = True

if "THEME_BUILD_V32" in t:
    print("skip theme")
elif "THEME_BUILD_V31" in t:
    t = t.replace("THEME_BUILD_V31", "THEME_BUILD_V32", 1)
    print("ok theme")
elif "THEME_BUILD_V30" in t:
    t = t.replace("THEME_BUILD_V30", "THEME_BUILD_V32", 1)
    print("ok theme-from-v30")
else:
    print("MISSING theme")
    ok = False

t = t.replace("./sw.js?v=31", "./sw.js?v=32")
t = t.replace("./sw.js?v=30", "./sw.js?v=32")

if '{ id: "x", label: "X (Twitter)",' in t:
    print("skip x-label")
elif '{ id: "x", label: "X",' in t:
    t = t.replace('{ id: "x", label: "X",', '{ id: "x", label: "X (Twitter)",', 1)
    print("ok x-label")

a = t.find("function SocialIcon")
if a < 0:
    a = t.find("/* V31 line icons */")
if a < 0:
    a = t.find("/* V32 brand icons */")
b = t.find("function ConnectCard")
if a >= 0 and b > a:
    if "V32 brand icons" in t[a:b] and 'rect width="48"' in t[a:b]:
        print("skip icons")
    else:
        t = t[:a] + NEW_ICON + t[b:]
        print("ok icons")
else:
    print("MISSING SocialIcon", a, b)
    ok = False

if "/* ===== V32 WINNING brand tiles + orange card borders ===== */" in t:
    print("skip css")
else:
    needle = "@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }\n`;"
    if needle in t:
        t = t.replace(needle, needle.replace("\n`;", WIN_CSS + "\n`;"), 1)
        print("ok css-end")
    elif "/* ===== V31 social + bottom nav ===== */" in t:
        t = t.replace("/* ===== V31 social + bottom nav ===== */", WIN_CSS + "\n/* ===== V31 social + bottom nav ===== */", 1)
        print("ok css-v31")
    else:
        print("MISSING css")
        ok = False

if not ok:
    sys.exit(1)

ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT, len(t))
