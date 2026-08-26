#!/usr/bin/env python3
"""Match Today mockup: 4 social tiles only + Android/tablet layout."""
from pathlib import Path
import sys
import re

p = Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
s = p.read_text(encoding="utf-8")

FOUR = '''const SOCIAL_LINKS = [
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" }
];'''

s2, n = re.subn(r"const SOCIAL_LINKS = \[[\s\S]*?\];", FOUR, s, count=1)
if n:
    s = s2
    print("social links -> 4 mockup tiles")
else:
    raise SystemExit("SOCIAL_LINKS not found")

s = s.replace(
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx", instagram: "ig", whatsapp: "wa" };',
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx" };',
    1,
)

old_why = '''      </div>
      <div className="why-card">
        <div className="stat-label">Why unlock helps</div>'''
new_why = '''        <div className="why-card">
          <div className="stat-label">Why unlock helps</div>'''
if old_why in s:
    s = s.replace(old_why, new_why, 1)
    old_close = '''        {!unlocked && (
          <button type="button" className="btn-ghost" style={{ marginTop: 8 }} onClick={onOpenPaywall}>See what's included →</button>
        )}
      </div>
    </div>
  );
}'''
    new_close = '''        {!unlocked && (
          <button type="button" className="btn-ghost" style={{ marginTop: 8 }} onClick={onOpenPaywall}>See what's included →</button>
        )}
        </div>
      </div>
    </div>
  );
}'''
    if old_close in s:
        s = s.replace(old_close, new_close, 1)
        print("why-card moved into quick-links grid")
    else:
        print("WARN why-card close mismatch")
else:
    print("why-card block not found or already moved")

LAYOUT = r"""
/* ===== Android + mockup layout lock ===== */
.app-main { max-width: 1120px !important; width: 100%; }
.home-today { max-width: 1120px; margin: 0 auto; }
.connect-links { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 10px !important; }
.connect-btn { display: flex !important; flex-direction: row !important; align-items: center !important; gap: 10px !important; width: 100% !important; max-width: none !important; background: #fff !important; border: 1.5px solid #E8ECF0 !important; border-radius: 16px !important; padding: 10px 12px !important; min-height: 62px !important; text-align: left !important; }
.connect-btn .cb-ico { width: 42px !important; height: 42px !important; border-radius: 50% !important; flex: 0 0 42px !important; }
.connect-btn .cb-text { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
.connect-btn::after { content: "›"; margin-left: auto; color: #C4CAD1; font-size: 18px; }
.quick-links { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 12px !important; }
.why-card { background: #FFF8F0 !important; border: 1px solid #F0E0CC !important; border-radius: 18px !important; padding: 14px 16px !important; margin: 0 !important; }
@media (max-width: 559px) {
  .connect-links { grid-template-columns: 1fr 1fr !important; }
  .quick-links { grid-template-columns: 1fr 1fr !important; }
  .home-greet .hi { font-size: 26px; }
}
@media (min-width: 640px) {
  .connect-links { grid-template-columns: repeat(4, 1fr) !important; }
  .home-top { grid-template-columns: 1fr 280px !important; }
  .home-hero { grid-template-columns: minmax(0, 1.55fr) minmax(240px, 0.9fr) !important; }
}
@media (min-width: 720px) {
  .quick-links { grid-template-columns: repeat(3, 1fr) !important; }
  .header-chips { flex-wrap: nowrap; overflow-x: auto; }
}
"""

if "Android + mockup layout lock" in s:
    s = re.sub(
        r"/\* ===== Android \+ mockup layout lock ===== \*/[\s\S]*?(?=\n@media print \{|\n</style>)",
        LAYOUT.rstrip() + "\n",
        s,
        count=1,
    )
    print("replaced android layout css")
elif "\n@media print {" in s:
    s = s.replace("\n@media print {", LAYOUT + "\n@media print {", 1)
    print("injected android layout css")
else:
    print("WARN no print media anchor")

s = s.replace(
    ".connect-links { grid-template-columns: repeat(3, 1fr) !important; }",
    ".connect-links { grid-template-columns: repeat(4, 1fr) !important; }",
)

s = s.replace("./sw.js?v=15", "./sw.js?v=16")
s = s.replace("./sw.js?v=14", "./sw.js?v=16")
if "sw.js?v=16" not in s and 'register("./sw.js")' in s:
    s = s.replace('register("./sw.js")', 'register("./sw.js?v=16")', 1)

s = s.replace("THEME_BUILD_V15", "THEME_BUILD_V16")
if "THEME_BUILD_V16" not in s:
    s = s.replace("<head>", "<head>\n  <!-- THEME_BUILD_V16 -->", 1)

if 'id: "instagram"' in s or 'id: "whatsapp"' in s:
    raise SystemExit("instagram/whatsapp still in SOCIAL_LINKS")
for must in ["tiktok", "facebook", "THEME_BUILD_V16", "Android + mockup layout lock"]:
    if must not in s:
        raise SystemExit("missing " + must)

p.write_text(s, encoding="utf-8")
print("wrote", p, p.stat().st_size)
