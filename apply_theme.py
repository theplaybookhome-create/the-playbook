#!/usr/bin/env python3
"""Apply visual remodel to THE PLAYBOOK app.html. Safe to re-run."""
from pathlib import Path

p = Path("app.html")
s = p.read_text(encoding="utf-8")

THEME_CSS = r"""
/* ===== Remodel theme overlay ===== */
:root {
  --peach: #F4C7A8;
  --sky: #7EB6D9;
  --mint: #7BC4A8;
  --lilac: #B9A7E0;
  --coral: #E07A6A;
}
.app-root { background:
  radial-gradient(1200px 420px at 10% -10%, rgba(193,117,46,0.10), transparent 55%),
  radial-gradient(900px 380px at 110% 8%, rgba(126,182,217,0.16), transparent 50%),
  var(--paper);
}
.app-header {
  background: linear-gradient(180deg, #ffffff 0%, #fffaf5 100%);
  border-bottom: 1px solid rgba(44,62,80,0.08);
}
.header-actions { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }
.header-btn, .header-pill {
  background: #fff;
  border: 1.5px solid var(--line);
  color: var(--navy);
  border-radius: 999px;
  padding: 7px 12px;
  font-weight: 700;
  font-size: 12px;
  cursor: pointer;
  box-shadow: 0 1px 0 rgba(44,62,80,0.04);
}
.header-btn:hover, .header-pill:hover { border-color: var(--amber); background: var(--amber-tint); }
.btn-primary, .btn-amber, .auth-submit {
  border-radius: 999px !important;
  box-shadow: 0 6px 16px rgba(44,62,80,0.16);
}
.btn-primary { background: linear-gradient(180deg, #34495E, #2C3E50); }
.quick-link, .scale-btn, .tick-chip, .range-pill, .child-chip, .connect-btn, .print-pack, .story-card, .stat-card, .insight-metric {
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.quick-link:hover, .print-pack:hover, .connect-btn:hover, .stat-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 22px rgba(44,62,80,0.10);
}
.home-greet { margin: 4px 0 16px; }
.home-greet .hi {
  font-size: 26px; line-height: 1.15; margin: 0 0 6px;
  color: var(--navy); letter-spacing: -0.03em; font-weight: 800;
}
.home-greet .hi em { font-style: normal; color: var(--amber); }
.home-greet .sub { margin: 0; color: var(--soft); font-size: 14px; line-height: 1.45; }
.energy-spark {
  background: #fff; border: 1.5px solid #E8D5C0; border-radius: 16px;
  padding: 14px 14px 10px; margin-bottom: 14px;
}
.energy-spark .es-top { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }
.energy-spark h3 { margin: 0; font-size: 14px; color: var(--navy); }
.energy-spark .es-avg { font-size: 12px; color: var(--soft); font-weight: 700; }
.energy-spark svg { width: 100%; height: 72px; display: block; margin-top: 6px; }
.energy-spark .es-empty { margin: 8px 0 0; font-size: 13px; color: var(--muted); }
.dash-kpis { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.dash-kpis .stat-card { border: 1.5px solid var(--line); border-radius: 16px; background: #fff; padding: 14px; }
.owned-chip-card { border: 1.5px solid #C9E8D6 !important; background: linear-gradient(135deg, #F3FBF6, #fff); }
.quick-log-card {
  position: relative; overflow: hidden;
  border-radius: 18px !important; border: 1.5px solid #E8D5C0 !important;
  box-shadow: 0 10px 28px rgba(193,117,46,0.10);
}
.quick-log-card .ql-bolt {
  position: absolute; top: 12px; right: 14px;
  width: 34px; height: 34px; border-radius: 12px;
  display: grid; place-items: center;
  background: #fff; border: 1.5px solid #E8D5C0; font-size: 16px;
}
.scale-btn { width: 40px; height: 40px; border-radius: 12px; border: 1.5px solid var(--line); background: #fff; font-weight: 800; }
.scale-btn.active { background: linear-gradient(180deg, #D48A45, #C1752E); border-color: #C1752E; color: #fff; }
.quick-links { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 4px 0 16px; }
.quick-link {
  text-align: left; background: #fff; border: 1.5px solid var(--line);
  border-radius: 16px; padding: 12px 12px 13px; cursor: pointer; font-family: inherit;
}
.quick-link .ql-ico {
  width: 34px; height: 34px; border-radius: 11px; display: grid; place-items: center;
  background: var(--amber-tint); border: 1.5px solid #E8D5C0; margin-bottom: 8px; font-size: 16px;
}
.quick-link strong { display: block; color: var(--navy); font-size: 14px; }
.quick-link span:last-child { display: block; color: var(--soft); font-size: 12px; margin-top: 2px; }
.connect-links { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.connect-btn {
  display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit;
  background: #fff; border: 1.5px solid var(--line); border-radius: 16px; padding: 10px 12px; min-height: 64px;
}
.connect-btn .cb-ico { width: 40px; height: 40px; border-radius: 12px; display: grid; place-items: center; flex: 0 0 40px; }
.connect-btn .cb-ico svg { width: 20px; height: 20px; fill: #fff; }
.connect-btn.fb .cb-ico { background: #1877F2; }
.connect-btn.tt .cb-ico { background: #111; }
.connect-btn.xx .cb-ico { background: #0F1419; }
.connect-btn.em .cb-ico { background: #C1752E; }
.connect-btn .cb-text { display: flex; flex-direction: column; min-width: 0; }
.connect-btn .cb-text strong { font-size: 13px; color: var(--navy); }
.connect-btn .cb-text span { font-size: 11px; color: var(--soft); }
.printables-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
@media (min-width: 560px) { .printables-grid { grid-template-columns: 1fr 1fr; } }
.print-pack { background: #fff; border: 1.5px solid var(--line); border-radius: 18px; padding: 16px; display: flex; flex-direction: column; gap: 6px; }
.print-pack .pp-emoji {
  width: 44px; height: 44px; border-radius: 14px; display: grid; place-items: center;
  background: var(--amber-tint); border: 1.5px solid #E8D5C0; font-size: 22px;
}
.print-pack button { width: 100%; margin-top: 8px; }
.insight-dash { display: flex; flex-direction: column; gap: 12px; }
.dash-charts { display: grid; grid-template-columns: 1fr; gap: 12px; }
@media (min-width: 560px) { .dash-charts { grid-template-columns: 1fr 1fr; } }
.chart-card { background: #fff; border: 1.5px solid var(--line); border-radius: 16px; padding: 14px; }
.chart-card h3 { margin: 0 0 8px; font-size: 13px; color: var(--navy); }
.insight-metric { background: #fff; border: 1.5px solid var(--line); border-radius: 16px; padding: 14px; }
.insight-metric .im-val { font-size: 26px; font-weight: 800; color: var(--navy); letter-spacing: -0.03em; }
.insight-metric .im-label { font-size: 12px; color: var(--soft); font-weight: 600; }
.auth-features { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 16px 0 4px; }
.auth-features span {
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.14);
  border-radius: 12px; padding: 10px; font-size: 12px; font-weight: 700; color: #F6E6D4; text-align: center;
}
.auth-card { border-radius: 20px !important; box-shadow: 0 20px 50px rgba(0,0,0,0.28); }
.auth-submit { width: 100%; }
.bottom-nav {
  background: #1A252F !important; border-top: none !important;
  border-radius: 22px 22px 0 0; max-width: 680px; margin: 0 auto;
  padding: 8px 8px calc(10px + env(safe-area-inset-bottom)) !important;
  box-shadow: 0 -10px 30px rgba(26,37,47,0.25);
}
.bottom-btn { color: rgba(255,255,255,0.55); }
.bottom-btn .lbl { font-size: 10px; font-weight: 700; }
.bottom-btn.active { background: rgba(255,255,255,0.1); border-radius: 14px; color: #fff; }
.bottom-btn.active .lbl { color: #F4C7A8 !important; }
.app-main { padding-bottom: 92px; }
"""

if "Remodel theme overlay" not in s:
    css_close = "\n@media print {"
    if css_close not in s:
        raise SystemExit("css print block not found")
    s = s.replace(css_close, THEME_CSS + "\n@media print {", 1)

ENERGY_FN = '''
function greetingForNow() {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 17) return "Good afternoon";
  return "Good evening";
}
function EnergySpark({ values, avg }) {
  const pts = (values || []).filter((n) => n != null && !isNaN(n));
  const w = 280, h = 72, pad = 8;
  let path = "";
  if (pts.length) {
    const max = 5, min = 1;
    pts.forEach((v, i) => {
      const x = pad + (pts.length === 1 ? (w - pad * 2) / 2 : i * ((w - pad * 2) / Math.max(pts.length - 1, 1)));
      const y = h - pad - ((v - min) / (max - min)) * (h - pad * 2);
      path += (i === 0 ? "M" : "L") + x.toFixed(1) + " " + y.toFixed(1) + " ";
    });
  }
  return (
    <div className="energy-spark">
      <div className="es-top">
        <h3>Energy spark</h3>
        <div className="es-avg">{avg !== "—" ? ("avg " + avg + "/5") : "log a few days"}</div>
      </div>
      {pts.length < 2 ? (
        <p className="es-empty">A tiny sparkline appears after two energy logs.</p>
      ) : (
        <svg viewBox={"0 0 " + w + " " + h} aria-hidden="true">
          <path d={path} fill="none" stroke="#C1752E" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
    </div>
  );
}
'''

if "function EnergySpark" not in s:
    needle = "function QuickLog({ setDataStore, showToast, activeChildId }) {"
    if needle not in s:
        raise SystemExit("QuickLog not found")
    s = s.replace(needle, ENERGY_FN + "\n" + needle, 1)

if "ql-bolt" not in s:
    old_ql = '<div className="quick-log-card">\n      <h3>Quick log</h3>'
    new_ql = '<div className="quick-log-card">\n      <span className="ql-bolt" aria-hidden="true">⚡</span>\n      <h3>Quick log</h3>'
    if old_ql not in s:
        raise SystemExit("quick log card header not found")
    s = s.replace(old_ql, new_ql, 1)

if 'className="home-greet"' not in s:
    old_home = '''  const lastWin = wins[0];
  return (
    <div>
      <PageHeader kicker="Your companion" title="Today" subtitle={activeChildName ? ("Logging for " + activeChildName + " · track what matters.") : "Track what matters. Spot patterns. Look after yourself too."} />
      <PaywallCard onUnlock={onUnlock} unlocked={unlocked} />
      <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />
      <ConnectCard />
      <div className="dash-grid">
        <div className="stat-card"><div className="stat-label">Energy (7 logs)</div><div className="stat-value">{avgEnergy}{avgEnergy !== "—" ? "/5" : ""}</div><div className="stat-hint">Your average lately</div></div>
        <div className="stat-card"><div className="stat-label">Logs this device</div><div className="stat-value">{daily.length + behavior.length}</div><div className="stat-hint">Daily + behaviour</div></div>
      </div>'''
    new_home = '''  const lastWin = wins[0];
  const hello = greetingForNow();
  return (
    <div>
      <div className="home-greet">
        <p className="hi">{hello}{activeChildName ? <em> · {activeChildName}</em> : null}</p>
        <p className="sub">{activeChildName ? ("Logging for " + activeChildName + " · track what matters today.") : "Track what matters. Spot patterns. Look after yourself too."}</p>
      </div>
      <PaywallCard onUnlock={onUnlock} unlocked={unlocked} />
      <QuickLog setDataStore={setDataStore} showToast={showToast} activeChildId={activeChildId} />
      <EnergySpark values={recentEnergy} avg={avgEnergy} />
      <div className="dash-kpis">
        <div className="stat-card"><div className="stat-label">Energy (7 logs)</div><div className="stat-value">{avgEnergy}{avgEnergy !== "—" ? "/5" : ""}</div><div className="stat-hint">Your average lately</div></div>
        <div className="stat-card"><div className="stat-label">Logs this device</div><div className="stat-value">{daily.length + behavior.length}</div><div className="stat-hint">Daily + behaviour</div></div>
      </div>
      <ConnectCard />'''
    if old_home not in s:
        raise SystemExit("HomePage return block not found")
    s = s.replace(old_home, new_home, 1)

if "owned-chip-card" not in s:
    s = s.replace(
        '<div className="card" style={{ borderColor: "var(--amber)" }}>',
        '<div className="card owned-chip-card" style={{ borderColor: "var(--amber)" }}>',
        1,
    )

if 'className="auth-features"' not in s:
    old_auth_trust = '''        <div className="auth-trust">
          <span>Private logs</span>
          <span>·</span>
          <span>No subscription required</span>
          <span>·</span>
          <span>£2.99 unlock</span>
        </div>'''
    new_auth_trust = '''        <div className="auth-features">
          <span>Private logs</span>
          <span>No subscription</span>
          <span>Track free first</span>
          <span>£2.99 unlock</span>
        </div>
        <div className="auth-trust">
          <span>Private logs</span>
          <span>·</span>
          <span>No subscription required</span>
          <span>·</span>
          <span>£2.99 unlock</span>
        </div>'''
    if old_auth_trust not in s:
        raise SystemExit("auth-trust not found")
    s = s.replace(old_auth_trust, new_auth_trust, 1)

if "const sleep7" not in s:
    old_last7 = '''  const last7 = useMemo(() => {
    const daily = [...(dataStore["daily-log-entries"] || [])].filter((e) => e.date).sort((a, b) => a.date.localeCompare(b.date));
    return daily.slice(-7);
  }, [dataStore]);

  if (!unlocked) {'''
    new_last7 = '''  const last7 = useMemo(() => {
    const daily = [...(dataStore["daily-log-entries"] || [])].filter((e) => e.date).sort((a, b) => a.date.localeCompare(b.date));
    return daily.slice(-7);
  }, [dataStore]);
  const sleep7 = useMemo(() => {
    const sleep = [...(dataStore["sleep-food-entries"] || [])].filter((e) => e.date).sort((a, b) => a.date.localeCompare(b.date));
    return sleep.slice(-7);
  }, [dataStore]);

  if (!unlocked) {'''
    if old_last7 not in s:
        raise SystemExit("last7 block not found")
    s = s.replace(old_last7, new_last7, 1)

if 'className="insight-dash"' not in s:
    old_ins = '<PageHeader kicker="Patterns, not perfection" title="Insights" subtitle="Built only from what you\'ve logged on this device." />'
    new_ins = '<PageHeader kicker="Patterns, not perfection" title="Insights" subtitle="A dashboard from what you\'ve logged on this device." />'
    if old_ins not in s:
        raise SystemExit("insights header not found")
    s = s.replace(old_ins, new_ins, 1)
    s = s.replace(
        "  return (\n    <div>\n      <PageHeader kicker=\"Patterns, not perfection\" title=\"Insights\" subtitle=\"A dashboard from what you've logged on this device.\" />",
        "  return (\n    <div className=\"insight-dash\">\n      <PageHeader kicker=\"Patterns, not perfection\" title=\"Insights\" subtitle=\"A dashboard from what you've logged on this device.\" />",
        1,
    )

if "Sleep quality" not in s:
    old_bar = '''      <div className="card">
        <div className="stat-label">Energy — last daily scores</div>
        {last7.length === 0 ? <p className="insight-empty">Log daily energy to see a trend.</p> : (
          <div className="insight-bar">
            {last7.map((e) => (
              <div className="insight-col" key={e.id}>
                <div className="insight-fill" style={{ height: e.energy ? (e.energy / 5) * 72 : 4 }} title={e.energy ? `${e.energy}/5` : "—"} />
                <span className="insight-day">{e.date ? e.date.slice(5) : ""}</span>
              </div>
            ))}
          </div>
        )}
      </div>'''
    new_bar = '''      <div className="dash-charts">
      <div className="chart-card">
        <h3>Energy — last daily scores</h3>
        {last7.length === 0 ? <p className="insight-empty">Log daily energy to see a trend.</p> : (
          <div className="insight-bar">
            {last7.map((e) => (
              <div className="insight-col" key={e.id}>
                <div className="insight-fill" style={{ height: e.energy ? (e.energy / 5) * 72 : 4 }} title={e.energy ? `${e.energy}/5` : "—"} />
                <span className="insight-day">{e.date ? e.date.slice(5) : ""}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="chart-card">
        <h3>Sleep quality</h3>
        {sleep7.length === 0 ? <p className="insight-empty">Log sleep to see nights side by side.</p> : (
          <div className="insight-bar">
            {sleep7.map((e) => (
              <div className="insight-col" key={e.id}>
                <div className="insight-fill" style={{ height: e.sleepQuality ? (e.sleepQuality / 5) * 72 : 4, background: "#7EB6D9" }} title={e.sleepQuality ? `${e.sleepQuality}/5` : "—"} />
                <span className="insight-day">{e.date ? e.date.slice(5) : ""}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      </div>'''
    if old_bar not in s:
        raise SystemExit("energy bar card not found")
    s = s.replace(old_bar, new_bar, 1)

s = s.replace('className="header-btn"', 'className="header-btn header-pill"')
s = s.replace('<meta name="theme-color" content="#2C3E50" />', '<meta name="theme-color" content="#1A252F" />', 1)

old_ph = "Browse every pack below. Each card shows example sheets so you know what you're getting — then open or save the PDF without leaving the app."
new_ph = "A grid of packs you can preview, open and save — without leaving the app."
s = s.replace(old_ph, new_ph, 1)

for must in ["home-greet", "EnergySpark", "dash-kpis", "alreadyPaid", "isClockSkewError", "auth-features", "insight-dash", "ql-bolt"]:
    if must not in s:
        raise SystemExit("missing marker " + must)

p.write_text(s, encoding="utf-8")
print("patched", p.stat().st_size)
