#!/usr/bin/env python3
"""V33: official TikTok glyph, full-width Why Unlock, hover animations."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")

NEW_TIKTOK = r'''  if (id === "tiktok") {
    const note = "M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z";
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect width="48" height="48" rx="12" fill="#010101"/>
        <g transform="translate(12,11) scale(1.05)">
          <path fill="#25F4EE" transform="translate(-1.35,1.2)" d={note}/>
          <path fill="#FE2C55" transform="translate(1.35,-1.2)" d={note}/>
          <path fill="#fff" d={note}/>
        </g>
      </svg>
    );
  }
'''

WIN = r"""
/* ===== V33 polish: TikTok, full-width why, hover ===== */
.quick-links {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 12px !important;
  align-items: stretch !important;
}
.quick-links .why-card,
.why-card,
.why-banner {
  grid-column: 1 / -1 !important;
  grid-row: auto !important;
  width: 100% !important;
  max-width: none !important;
  display: block !important;
  box-sizing: border-box !important;
}
.connect-btn,
.quick-link,
.why-card,
.connect-card {
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease !important;
}
.connect-btn:hover,
.quick-link:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 12px 28px rgba(255,107,0,.20), 0 6px 16px rgba(15,24,34,.08) !important;
  border-color: #FF8A2B !important;
  background: #FFF8F2 !important;
}
.connect-btn:hover .cb-ico {
  transform: scale(1.06) !important;
  box-shadow: 0 10px 22px rgba(0,0,0,.22) !important;
}
.connect-btn .cb-ico {
  transition: transform .18s ease, box-shadow .18s ease !important;
}
.connect-btn:active,
.quick-link:active {
  transform: translateY(-1px) scale(.985) !important;
  box-shadow: 0 6px 16px rgba(255,107,0,.14) !important;
}
.why-card:hover {
  box-shadow: 0 10px 24px rgba(15,24,34,.08) !important;
  border-color: #FF8A2B !important;
}
.bottom-btn {
  transition: transform .16s ease, border-color .16s ease, color .16s ease, background .16s ease !important;
}
.bottom-btn:hover:not(.active) {
  color: rgba(255,255,255,.92) !important;
  background: rgba(255,255,255,.06) !important;
}
.bottom-btn:active {
  transform: scale(.96) !important;
}
@media (max-width: 859px) {
  .quick-links { grid-template-columns: 1fr 1fr !important; }
  .quick-links .why-card, .why-card { grid-column: 1 / -1 !important; }
}
@media (hover: none) {
  .connect-btn:hover,
  .quick-link:hover {
    transform: none !important;
  }
}
@media (prefers-reduced-motion: reduce) {
  .connect-btn, .quick-link, .why-card, .connect-card, .bottom-btn, .connect-btn .cb-ico {
    transition: none !important;
  }
}
"""

ok = True

if "THEME_BUILD_V33" in t:
    print("skip theme")
elif "THEME_BUILD_V32" in t:
    t = t.replace("THEME_BUILD_V32", "THEME_BUILD_V33", 1)
    print("ok theme")
elif "THEME_BUILD_V31" in t:
    t = t.replace("THEME_BUILD_V31", "THEME_BUILD_V33", 1)
    print("ok theme-from-v31")
else:
    print("MISSING theme")
    ok = False

t = t.replace("./sw.js?v=32", "./sw.js?v=33")
t = t.replace("./sw.js?v=31", "./sw.js?v=33")

a = t.find('  if (id === "tiktok") {')
b = t.find('  if (id === "x") {')
if a >= 0 and b > a:
    t = t[:a] + NEW_TIKTOK + t[b:]
    print("ok tiktok")
else:
    print("MISSING tiktok", a, b)
    ok = False

if "/* ===== V33 polish: TikTok, full-width why, hover ===== */" in t:
    print("skip css")
else:
    end = t.rfind("\n`;\n\n// Inject theme CSS")
    if end < 0:
        end = t.find("\n`;\n\n// Inject theme CSS")
    if end >= 0:
        t = t[:end] + WIN + t[end:]
        print("ok css-end")
    else:
        print("MISSING css")
        ok = False

if not ok:
    sys.exit(1)

ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT, len(t))
