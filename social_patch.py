#!/usr/bin/env python3
"""Today page: active header chips, clickable energy card, 4 official-style socials."""
from pathlib import Path
import sys
import re

p = Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
s = p.read_text(encoding="utf-8")

FOUR = '''const SOCIAL_LINKS = [
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "email", label: "Email", href: "mailto:Theplaybookhome@gmail.com", hint: "Support" }
];'''
s2, n = re.subn(r"const SOCIAL_LINKS = \[[\s\S]*?\];", FOUR, s, count=1)
if n:
    s = s2
    print("social links -> TikTok / X / Facebook / Email")
else:
    print("WARN SOCIAL_LINKS not found")

s = s.replace(
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx", instagram: "ig", whatsapp: "wa" };',
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx", email: "em" };',
    1,
)
s = s.replace(
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx" };',
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx", email: "em" };',
    1,
)

old_extra_email = '''        {SUPPORT_EMAIL ? (
          <a className="connect-btn em" href={"mailto:" + SUPPORT_EMAIL}>
            <span className="cb-ico"><SocialIcon id="email" /></span>
            <span className="cb-text">
              <strong>Email</strong>
              <span>Support</span>
            </span>
          </a>
        ) : null}'''
if old_extra_email in s:
    s = s.replace(old_extra_email, "", 1)
    print("removed duplicate email tile")

NEW_ICON = r'''function SocialIcon({ id }) {
  if (id === "facebook") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M15.1 8.2h2.4V4.7h-2.4c-2.9 0-4.8 1.8-4.8 4.9v2H8v3.6h2.3V22h3.7v-6.8h2.5l.6-3.6h-3.1V9.8c0-1.1.5-1.6 1.6-1.6z"/></svg>
    );
  }
  if (id === "tiktok") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path fill="#25F4EE" d="M16.6 4.3c.55 1.35 1.55 2.45 2.95 2.95V9.7c-1.2-.05-2.35-.35-3.4-.85-.5-.25-1-.55-1.4-.9.0 2.35 0 4.7 0 7.05-.05 1.15-.45 2.3-1.15 3.25-.95 1.3-2.5 2.15-4.15 2.2-1.45.05-2.9-.45-4-1.4-1.55-1.3-2.25-3.4-1.8-5.35.4-1.75 1.7-3.25 3.4-4 .95-.45 2.05-.6 3.1-.45v3.65c-.55-.15-1.15-.1-1.65.15-.55.25-1 .75-1.15 1.35-.2.7.05 1.5.6 1.95.5.45 1.25.55 1.85.35.7-.2 1.2-.8 1.3-1.5.05-2.95.05-5.9.05-8.85h3.05z"/>
        <path fill="#FE2C55" d="M15.35 3.05c.55 1.35 1.55 2.45 2.95 2.95V8.45c-1.2-.05-2.35-.35-3.4-.85-.5-.25-1-.55-1.4-.9.0 2.35 0 4.7 0 7.05-.05 1.15-.45 2.3-1.15 3.25-.95 1.3-2.5 2.15-4.15 2.2-1.45.05-2.9-.45-4-1.4v-3.15c.9.85 2.15 1.3 3.4 1.2 1.15-.05 2.2-.65 2.85-1.6.45-.65.7-1.45.7-2.25 0-2.4 0-4.8 0-7.2h3.2z"/>
        <path fill="#fff" d="M14.7 3.7c.55 1.35 1.55 2.45 2.95 2.95v2.45c-1.2-.05-2.35-.35-3.4-.85-.5-.25-1-.55-1.4-.9v7.05c-.05 1.15-.45 2.3-1.15 3.25-.95 1.3-2.5 2.15-4.15 2.2-1.45.05-2.9-.45-4-1.4-.7-.6-1.2-1.4-1.5-2.25.7.55 1.55.9 2.45.95 1.15.05 2.25-.4 3-1.25.5-.55.8-1.3.85-2.05V6.15c.95-.15 1.95 0 2.8.45.55.25 1.05.65 1.4 1.1V3.7h2.15z"/>
      </svg>
    );
  }
  if (id === "x") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M17.6 3.5h2.9l-6.4 7.3L22 20.5h-5.9l-4.6-6-5.3 6H3.3l6.8-7.8L2 3.5h6.1l4.2 5.5 5.3-5.5zm-1 15.3h1.6L7.5 5.1H5.8l10.8 13.7z"/></svg>
    );
  }
  if (id === "email") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path fill="#4285F4" d="M3 6.2v11.1c0 .6.5 1.1 1.1 1.1h2.2V10.3L12 14.8l5.7-4.5v8.1h2.2c.6 0 1.1-.5 1.1-1.1V6.2L12 13.1 3 6.2z"/>
        <path fill="#EA4335" d="M20.1 4.6H3.9c-.3 0-.6.1-.8.3L12 11.6l8.9-6.7c-.2-.2-.5-.3-.8-.3z"/>
        <path fill="#34A853" d="M3 6.2l9 6.9 9-6.9v1.5L12 14.8 3 7.7z"/>
        <path fill="#FBBC05" d="M3 17.3V7.7l4.3 3.3v7.4H4.1c-.6 0-1.1-.5-1.1-1.1z"/>
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5L4 8V6l8 5 8-5v2z"/></svg>
  );
}
'''

s2, n = re.subn(r"function SocialIcon\(\{ id \}\) \{[\s\S]*?\n\}\nfunction ConnectCard", NEW_ICON + "function ConnectCard", s, count=1)
if n:
    s = s2
    print("social icons -> official brand marks")
else:
    print("WARN SocialIcon not replaced")

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

old_chips = '''        <div className="header-chips"><span>🔒 Private tracking</span><span>📈 Pattern insights</span><span>📄 Professional report</span><span>👥 Community</span><span>✨ Curated tools</span></div>'''
new_chips = '''        <div className="header-chips" role="navigation" aria-label="Features">
          <button type="button" className={"hchip" + (mainTab === "track" ? " active" : "")} onClick={() => navigate("track", "daily")}>🔒 Private tracking</button>
          <button type="button" className={"hchip" + (mainTab === "insights" ? " active" : "")} onClick={() => navigate("insights")}>📈 Pattern insights</button>
          <button type="button" className={"hchip" + (mainTab === "report" ? " active" : "")} onClick={() => navigate("report")}>📄 Professional report</button>
          <button type="button" className={"hchip" + (mainTab === "community" ? " active" : "")} onClick={() => navigate("community")}>👥 Community</button>
          <button type="button" className={"hchip" + (mainTab === "discover" ? " active" : "")} onClick={() => navigate("discover")}>✨ Curated tools</button>
        </div>'''
if old_chips in s:
    s = s.replace(old_chips, new_chips, 1)
    print("header chips -> active buttons")
elif "className={\"hchip\"" in s or 'className="hchip"' in s:
    print("header chips already buttons")
else:
    print("WARN header chips mismatch")

old_es_avg = '''        <h3>Energy ({pts.length} logs)</h3>
        <div className="es-avg">›</div>'''
new_es_avg = '''        <h3>Energy ({pts.length} logs)</h3>
        <div className="es-avg" aria-hidden="true">›</div>'''
if old_es_avg in s:
    s = s.replace(old_es_avg, new_es_avg, 1)
    print("energy chevron kept as click cue")

if "energy-spark-wrap" not in s:
    s = s.replace(
        "<EnergySpark values={recentEnergy} avg={avgEnergy} />",
        '<div className="energy-spark-wrap" role="button" tabIndex={0} title="Open insights" onClick={() => onNavigate("insights")} onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onNavigate("insights"); } }}><EnergySpark values={recentEnergy} avg={avgEnergy} /></div>',
        1,
    )
    print("energy card opens insights")

LAYOUT = r"""
/* ===== Android + mockup layout lock ===== */
.app-main { max-width: 1120px !important; width: 100%; }
.home-today { max-width: 1120px; margin: 0 auto; }
.connect-links { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 10px !important; }
.connect-btn { display: flex !important; flex-direction: row !important; align-items: center !important; gap: 10px !important; width: 100% !important; max-width: none !important; background: #fff !important; border: 1.5px solid #E8ECF0 !important; border-radius: 16px !important; padding: 10px 12px !important; min-height: 62px !important; text-align: left !important; text-decoration: none !important; color: inherit !important; }
.connect-btn .cb-ico { width: 42px !important; height: 42px !important; border-radius: 12px !important; flex: 0 0 42px !important; display: grid !important; place-items: center !important; box-shadow: 0 3px 8px rgba(0,0,0,.16), inset 0 1px 0 rgba(255,255,255,.25) !important; }
.connect-btn .cb-ico svg { width: 22px !important; height: 22px !important; display: block !important; fill: none !important; }
.connect-btn .cb-text { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
.connect-btn::after { content: "›"; margin-left: auto; color: #C4CAD1; font-size: 18px; }
.connect-btn.tt .cb-ico { background: #111 !important; }
.connect-btn.xx .cb-ico { background: #0F1419 !important; }
.connect-btn.fb .cb-ico { background: #1877F2 !important; }
.connect-btn.em .cb-ico { background: #fff !important; border: 1px solid #E6E8EC; }
.connect-btn.em .cb-ico svg { width: 24px !important; height: 24px !important; }
.quick-links { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 12px !important; }
.why-card { background: #FFF8F0 !important; border: 1px solid #F0E0CC !important; border-radius: 18px !important; padding: 14px 16px !important; margin: 0 !important; }
.header-chips button.hchip, .header-chips .hchip {
  background: transparent; border: none; color: rgba(255,255,255,.72);
  font-size: 12px; font-weight: 600; cursor: pointer;
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 10px; border-radius: 10px; font-family: inherit;
}
.header-chips .hchip:hover { background: rgba(255,255,255,.08); color: #fff; }
.header-chips .hchip.active { background: rgba(232,137,44,.18); color: #F3C38A; }
.header-chips span { display: none; }
.energy-spark-wrap { cursor: pointer; border-radius: 18px; }
.energy-spark-wrap:hover .energy-spark { border-color: #E8C9A0; }
.energy-spark-wrap .es-avg { color: #C4CAD1; font-size: 18px; line-height: 1; }
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

s = s.replace(
    ".connect-links { grid-template-columns: repeat(3, 1fr) !important; }",
    ".connect-links { grid-template-columns: repeat(4, 1fr) !important; }",
)

for oldv in ("./sw.js?v=15", "./sw.js?v=16", "./sw.js?v=17", "./sw.js?v=14"):
    s = s.replace(oldv, "./sw.js?v=18")
if "sw.js?v=18" not in s and 'register("./sw.js")' in s:
    s = s.replace('register("./sw.js")', 'register("./sw.js?v=18")', 1)

for oldb in ("THEME_BUILD_V15", "THEME_BUILD_V16", "THEME_BUILD_V17"):
    s = s.replace(oldb, "THEME_BUILD_V18")
if "THEME_BUILD_V18" not in s:
    s = s.replace("<head>", "<head>\n  <!-- THEME_BUILD_V18 -->", 1)

if 'id: "instagram"' in s or 'id: "whatsapp"' in s:
    raise SystemExit("instagram/whatsapp still in SOCIAL_LINKS")
for must in ["tiktok", "facebook", "THEME_BUILD_V18", "hchip", "Android + mockup layout lock", "energy-spark-wrap"]:
    if must not in s:
        raise SystemExit("missing " + must)

p.write_text(s, encoding="utf-8")
print("wrote", p, p.stat().st_size)
