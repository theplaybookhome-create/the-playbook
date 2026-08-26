#!/usr/bin/env python3
"""V31: matching line social icons + 5-item navy bar with orange active border."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
t = ROOT.read_text(encoding="utf-8")

NEW_ICON = r'''function SocialIcon({ id }) {
  const common = { viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.8", strokeLinecap: "round", strokeLinejoin: "round", "aria-hidden": "true" };
  if (id === "tiktok") {
    return (
      <svg {...common}>
        <path d="M14.2 3.5v10.2a3.7 3.7 0 1 1-3.2-3.66"/>
        <path d="M14.2 7.2c1.15.9 2.55 1.45 4.05 1.55"/>
      </svg>
    );
  }
  if (id === "x") {
    return (
      <svg {...common}>
        <path d="M5 5l14 14M19 5L5 19"/>
      </svg>
    );
  }
  if (id === "facebook") {
    return (
      <svg {...common}>
        <path d="M15 8h2.2V5.2H15c-2.6 0-4.3 1.6-4.3 4.4v1.7H8.4v2.9h2.3V20h3.2v-5.8h2.4l.5-2.9h-2.9V9.7c0-.9.4-1.7 1.5-1.7z"/>
      </svg>
    );
  }
  if (id === "email") {
    return (
      <svg {...common}>
        <rect x="3.5" y="5.5" width="17" height="13" rx="2.2"/>
        <path d="M4.2 7.2L12 13.1l7.8-5.9"/>
      </svg>
    );
  }
  if (id === "instagram") {
    return (
      <svg {...common}>
        <rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/>
        <circle cx="12" cy="12" r="3.6"/>
        <circle cx="17.2" cy="6.8" r="0.8" fill="currentColor" stroke="none"/>
      </svg>
    );
  }
  if (id === "youtube") {
    return (
      <svg {...common}>
        <rect x="2.8" y="6" width="18.4" height="12" rx="3"/>
        <path d="M10.4 9.2v5.6L15.6 12z" fill="currentColor" stroke="none"/>
      </svg>
    );
  }
  if (id === "whatsapp") {
    return (
      <svg {...common}>
        <path d="M5.2 18.6l.6-2.2A8 8 0 1 1 7.6 19l-2.4.4z"/>
        <path d="M9.2 9.4c.2-.4.4-.4.6-.4h.5c.2 0 .4.1.5.4l.4 1c.1.2 0 .4-.1.5l-.5.5c.6 1.1 1.5 2 2.6 2.6l.5-.5c.2-.2.4-.2.6-.1l1 .4c.2.1.3.3.3.5v.5c0 .2 0 .4-.4.6A4.8 4.8 0 0 1 12 16.6 4.8 4.8 0 0 1 9.2 9.4z"/>
      </svg>
    );
  }
  return (
    <svg {...common}>
      <circle cx="12" cy="12" r="8"/>
    </svg>
  );
}

'''

ok = True
if "THEME_BUILD_V30" in t:
    t = t.replace("THEME_BUILD_V30", "THEME_BUILD_V31", 1)
    print("ok theme")
elif "THEME_BUILD_V31" in t:
    print("skip theme")
else:
    print("MISSING theme"); ok = False

t = t.replace("./sw.js?v=30", "./sw.js?v=31")
t = t.replace("./sw.js?v=29", "./sw.js?v=31")

a = t.find("function SocialIcon")
b = t.find("function ConnectCard")
if "V31 line icons" in t:
    print("skip icons")
elif a >= 0 and b > a:
    t = t[:a] + "/* V31 line icons */\n" + NEW_ICON + t[b:]
    print("ok icons")
else:
    print("MISSING SocialIcon"); ok = False

CSS = r"""
/* ===== V31 social + bottom nav ===== */
.bottom-nav {
  position: fixed !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100% !important;
  max-width: none !important;
  transform: none !important;
  display: flex !important;
  justify-content: space-evenly !important;
  align-items: center !important;
  gap: 4px !important;
  background: #0E131F !important;
  border: none !important;
  border-radius: 0 !important;
  padding: 8px 10px calc(8px + env(safe-area-inset-bottom)) !important;
  z-index: 50 !important;
  box-shadow: 0 -8px 24px rgba(0,0,0,.18) !important;
}
.bottom-btn {
  flex: 1 1 0 !important;
  max-width: 132px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 3px !important;
  background: transparent !important;
  color: rgba(255,255,255,.55) !important;
  border: 2px solid transparent !important;
  border-radius: 12px !important;
  padding: 7px 6px !important;
  min-height: 54px !important;
  box-sizing: border-box !important;
}
.bottom-btn .ico svg {
  width: 20px !important;
  height: 20px !important;
  stroke: currentColor !important;
  fill: none !important;
}
.bottom-btn.active,
.bottom-btn:focus-visible {
  border: 2px solid #FF6B00 !important;
  color: #FF6B00 !important;
  background: rgba(255,107,0,.08) !important;
  outline: none !important;
}
.bottom-btn.active .lbl,
.bottom-btn.active .ico svg {
  color: #FF6B00 !important;
  stroke: #FF6B00 !important;
}
.connect-btn .cb-ico {
  width: 42px !important;
  height: 42px !important;
  min-width: 42px !important;
  border-radius: 50% !important;
  background: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  box-shadow: 0 4px 20px rgba(0,0,0,.04) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.connect-btn.fb .cb-ico,
.connect-btn.tt .cb-ico,
.connect-btn.xx .cb-ico,
.connect-btn.em .cb-ico,
.connect-btn.ig .cb-ico,
.connect-btn.yt .cb-ico {
  background: #FFFFFF !important;
}
.connect-btn .cb-ico svg {
  width: 20px !important;
  height: 20px !important;
  stroke: #0E131F !important;
  fill: none !important;
  color: #0E131F !important;
}
.connect-card {
  background: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 20px !important;
  box-shadow: 0 4px 20px rgba(0,0,0,.04) !important;
}
"""

if "/* ===== V31 social + bottom nav ===== */" in t:
    print("skip css")
elif "/* ===== V30 tablet spec ===== */" in t:
    t = t.replace("/* ===== V30 tablet spec ===== */", CSS + "\n/* ===== V30 tablet spec ===== */", 1)
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
