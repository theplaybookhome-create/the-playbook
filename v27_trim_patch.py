#!/usr/bin/env python3
"""V27: drop extra socials; watercolor sunrise matching Tuesday mockup."""
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
ok &= sub("THEME_BUILD_V26", "THEME_BUILD_V27", "theme")
ok &= sub("THEME_BUILD_V25", "THEME_BUILD_V27", "theme25", required=False)
ok &= sub("./sw.js?v=26", "./sw.js?v=27", "swq")
ok &= sub("./sw.js?v=25", "./sw.js?v=27", "swq25", required=False)

OLD_SOCIAL = '''const SOCIAL_LINKS = [
  { id: "instagram", label: "Instagram", href: "https://www.instagram.com/theplaybookhome", hint: "Community" },
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X (Twitter)", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "youtube", label: "YouTube", href: "https://www.youtube.com/@theplaybookhome", hint: "Videos" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "email", label: "Email", href: "mailto:Theplaybookhome@gmail.com", hint: "Support" }
];'''

NEW_SOCIAL = '''const SOCIAL_LINKS = [
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "email", label: "Email", href: "mailto:Theplaybookhome@gmail.com", hint: "Support" }
];'''
ok &= sub(OLD_SOCIAL, NEW_SOCIAL, "social")

OLD_SUN = '''      <svg className="ql-sun" viewBox="0 0 260 200" aria-hidden="true">
        <defs>
          <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#F8E4C4" stopOpacity="0.95"/>
            <stop offset="0.55" stopColor="#FBEED8" stopOpacity="0.35"/>
            <stop offset="1" stopColor="#FFFFFF" stopOpacity="0"/>
          </linearGradient>
          <radialGradient id="sunGlow" cx="62%" cy="42%" r="42%">
            <stop offset="0" stopColor="#FFE7A8"/>
            <stop offset="0.45" stopColor="#F6B84A"/>
            <stop offset="1" stopColor="#F6B84A" stopOpacity="0"/>
          </radialGradient>
          <linearGradient id="mtFar" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#C5D3E4"/>
            <stop offset="1" stopColor="#E4EDF5"/>
          </linearGradient>
          <linearGradient id="mtMid" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#9FB4CC"/>
            <stop offset="1" stopColor="#D5E2EE"/>
          </linearGradient>
        </defs>
        <rect width="260" height="200" fill="url(#sky)"/>
        <circle cx="168" cy="86" r="70" fill="url(#sunGlow)"/>
        <circle cx="168" cy="86" r="28" fill="#F4B84A"/>
        <ellipse cx="70" cy="58" rx="34" ry="12" fill="#F7D7B8" opacity="0.7"/>
        <ellipse cx="108" cy="48" rx="22" ry="9" fill="#F8E0C6" opacity="0.65"/>
        <ellipse cx="210" cy="40" rx="28" ry="10" fill="#F6D3B4" opacity="0.55"/>
        <path d="M8 200 L48 118 L86 168 L118 96 L156 150 L188 108 L232 162 L260 128 L260 200 Z" fill="url(#mtFar)" opacity="0.9"/>
        <path d="M0 200 L36 142 L72 176 L110 120 L148 168 L186 132 L230 176 L260 150 L260 200 Z" fill="url(#mtMid)" opacity="0.88"/>
        <path d="M0 200 C40 168 78 176 118 186 C160 196 200 170 260 184 L260 200 Z" fill="#E9D7BE" opacity="0.55"/>
      </svg>'''

NEW_SUN = '''      <svg className="ql-sun" viewBox="0 0 280 220" aria-hidden="true">
        <defs>
          <linearGradient id="qlSky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#F6D7A8"/>
            <stop offset="0.42" stopColor="#F8E4C4"/>
            <stop offset="1" stopColor="#FFF6EA"/>
          </linearGradient>
          <radialGradient id="qlSunGlow" cx="62%" cy="36%" r="46%">
            <stop offset="0" stopColor="#FFE7A0"/>
            <stop offset="0.38" stopColor="#F0B03A"/>
            <stop offset="1" stopColor="#F0B03A" stopOpacity="0"/>
          </radialGradient>
          <linearGradient id="qlHill1" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#EED4B0"/>
            <stop offset="1" stopColor="#F6E6CC"/>
          </linearGradient>
          <linearGradient id="qlHill2" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#E0C094"/>
            <stop offset="1" stopColor="#EFD8B4"/>
          </linearGradient>
          <linearGradient id="qlHill3" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#D2AE80"/>
            <stop offset="1" stopColor="#E6C89A"/>
          </linearGradient>
        </defs>
        <rect width="280" height="220" rx="20" fill="url(#qlSky)"/>
        <circle cx="176" cy="78" r="86" fill="url(#qlSunGlow)"/>
        <circle cx="176" cy="78" r="36" fill="#EFA83A"/>
        <circle cx="176" cy="78" r="28" fill="#F6C14A"/>
        <ellipse cx="58" cy="64" rx="40" ry="16" fill="#F3D2AE" opacity="0.55"/>
        <ellipse cx="96" cy="52" rx="24" ry="11" fill="#F7E0C2" opacity="0.5"/>
        <ellipse cx="236" cy="48" rx="30" ry="12" fill="#F4D6B4" opacity="0.4"/>
        <path d="M0 158 C48 136 86 148 128 156 C176 166 214 132 280 150 L280 220 L0 220 Z" fill="url(#qlHill1)"/>
        <path d="M0 178 C56 158 98 172 148 178 C198 184 236 160 280 172 L280 220 L0 220 Z" fill="url(#qlHill2)"/>
        <path d="M0 198 C70 184 128 192 184 196 C228 200 254 188 280 194 L280 220 L0 220 Z" fill="url(#qlHill3)"/>
        <path d="M42 98 q10-9 20 0" fill="none" stroke="#C48A4A" strokeWidth="1.7" strokeLinecap="round"/>
        <path d="M68 88 q8-7 16 0" fill="none" stroke="#C48A4A" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>'''
ok &= sub(OLD_SUN, NEW_SUN, "sun")

CSS_ADD = """
.connect-links { grid-template-columns: repeat(4, 1fr) !important; }
.ql-sun {
  width: 228px !important;
  height: 172px !important;
  right: 14px !important;
  top: 18px !important;
  border-radius: 18px;
  overflow: hidden;
}
@media (max-width: 759px) {
  .connect-links { grid-template-columns: repeat(4, 1fr) !important; }
  .ql-sun { width: 132px !important; height: 108px !important; opacity: .95 !important; }
}
"""
if "grid-template-columns: repeat(4, 1fr) !important;" not in t or "qlHill3" in t:
    if "/* V27 connect + sunrise */" not in t:
        marker = "@media print {"
        if marker in t:
            t = t.replace(marker, "/* V27 connect + sunrise */\n" + CSS_ADD + "\n@media print {", 1)
            print("ok css")
        else:
            print("MISSING css-anchor")
            ok = False
    else:
        print("skip css")
else:
    print("skip css")

ROOT.write_text(t, encoding="utf-8")
print("wrote", ROOT, "ok" if ok else "PARTIAL")
if not ok:
    sys.exit(1)
