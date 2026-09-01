#!/usr/bin/env python3
"""V36 — 7-day free trial paywall, shareable report link, med reminder nudges."""
from pathlib import Path

APP = Path("app.html")
text = APP.read_text(encoding="utf-8")

text = text.replace("<!-- THEME_BUILD_V35 -->", "<!-- THEME_BUILD_V36 -->", 1)
text = text.replace("<!-- THEME_BUILD_V33 -->", "<!-- THEME_BUILD_V36 -->", 1)

CSS = """
/* ===== V36 trial / share / meds ===== */
.trial-chip{
  min-width:168px; max-width:220px; background:#fff; border:1.5px solid #E6E8EC; border-radius:16px;
  padding:10px 12px; box-shadow:0 1px 2px rgba(15,23,42,.04);
}
.trial-chip .trial-label{ font-size:10px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:#FF8A2B; }
.trial-chip .trial-val{ font-size:15px; font-weight:800; color:#0E131F; margin-top:2px; }
.trial-chip .trial-hint{ font-size:11px; color:#6B7280; margin-top:2px; line-height:1.3; }
.trial-bar{ height:4px; background:#F3F4F6; border-radius:99px; margin-top:8px; overflow:hidden; }
.trial-bar > span{ display:block; height:100%; background:#FF8A2B; border-radius:99px; }
.report-teaser{ margin-top:10px; padding:10px 12px; background:#FFF8F2; border:1px solid #FFE0C7; border-radius:14px; }
.report-teaser .tk{ font-size:10px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:#FF8A2B; }
.report-teaser p{ margin:4px 0 0; font-size:13px; color:#0E131F; line-height:1.4; }
.med-banner{
  display:flex; gap:10px; align-items:flex-start; background:#FFF4EB; border:1.5px solid #FFD0A8;
  border-radius:16px; padding:12px 14px; margin:0 0 14px;
}
.med-banner strong{ display:block; font-size:14px; color:#0E131F; }
.med-banner span{ font-size:12.5px; color:#6B7280; }
.med-banner button{ margin-left:auto; border:0; background:#fff; border-radius:10px; padding:6px 10px; font-weight:700; cursor:pointer; }
.share-bar{ display:flex; flex-wrap:wrap; gap:8px; margin:10px 0 14px; }
.share-view{ max-width:640px; margin:24px auto; padding:0 16px 40px; }
.share-view .sv-brand{ font-weight:800; letter-spacing:.04em; color:#0E131F; margin-bottom:8px; }
@media print{
  .trial-chip,.med-banner,.share-bar,.report-teaser{ display:none !important; }
}
"""

if "V36 trial / share / meds" not in text:
    text = text.replace("</style>", CSS + "\n</style>", 1)

HELPERS = r'''
/* ===== V36 helpers: trial days, share link, med reminders ===== */
const FREE_LOG_DAYS = 7;

function countLoggedDays(dataStore) {
  const keys = ["daily-log-entries", "behavior-log-entries", "sleep-food-entries"];
  const dates = new Set();
  keys.forEach((k) => {
    (dataStore[k] || []).forEach((e) => { if (e && e.date) dates.add(String(e.date).slice(0, 10)); });
  });
  return dates.size;
}

function shiftISODate(iso, days) {
  const d = new Date(iso + "T12:00:00");
  if (isNaN(d.getTime())) return iso;
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

function reminderDueDate(entry) {
  if (!entry) return null;
  const ticks = Array.isArray(entry._reminder) ? entry._reminder : (entry._reminder ? [entry._reminder] : []);
  const base = (entry.date || todayISO()).slice(0, 10);
  if (ticks.indexOf("Remind me tomorrow") !== -1) return shiftISODate(base, 1);
  if (ticks.indexOf("Remind me in 2 days") !== -1) return shiftISODate(base, 2);
  return null;
}

function collectDueMedReminders(dataStore) {
  const today = todayISO();
  let dismissed = [];
  try { dismissed = JSON.parse(localStorage.getItem("playbook:med-dismissed") || "[]"); } catch (e) { dismissed = []; }
  if (!Array.isArray(dismissed)) dismissed = [];
  const out = [];
  (dataStore["medication-entries"] || []).forEach((e) => {
    const due = reminderDueDate(e);
    if (!due || due > today) return;
    if (dismissed.indexOf(e.id) !== -1) return;
    out.push({ id: e.id, name: e.name || "Medication", dose: e.dose || "", due: due });
  });
  return out;
}

function dismissMedReminder(id) {
  let dismissed = [];
  try { dismissed = JSON.parse(localStorage.getItem("playbook:med-dismissed") || "[]"); } catch (e) { dismissed = []; }
  if (!Array.isArray(dismissed)) dismissed = [];
  if (dismissed.indexOf(id) === -1) dismissed.push(id);
  try { localStorage.setItem("playbook:med-dismissed", JSON.stringify(dismissed)); } catch (e) {}
}

function encodeSharePayload(obj) {
  const json = JSON.stringify(obj);
  return btoa(unescape(encodeURIComponent(json))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function decodeShareParam() {
  try {
    const q = new URLSearchParams(window.location.search).get("share");
    if (!q) return null;
    let b64 = q.replace(/-/g, "+").replace(/_/g, "/");
    while (b64.length % 4) b64 += "=";
    const obj = JSON.parse(decodeURIComponent(escape(atob(b64))));
    if (!obj || obj.v !== 1) return null;
    return obj;
  } catch (e) { return null; }
}

function buildSharePayload(dataStore, profile, range) {
  const analysis = buildStories(dataStore, range || 14);
  const extra = (typeof detectPatterns === "function") ? detectPatterns(dataStore) : [];
  const stories = (analysis.stories || []).concat(extra).slice(0, 5).map((s) => ({
    kicker: s.kicker || "Note",
    text: String(s.text || "").slice(0, 220)
  }));
  const points = buildTalkingPoints(analysis).slice(0, 5);
  const child = String((profile && (profile.nameAge || profile.name)) || "Child").split(" ")[0] || "Child";
  return {
    v: 1,
    app: "THE PLAYBOOK",
    child: child.slice(0, 24),
    range: range === "all" ? "All logged data" : ("Last " + (range || 14) + " days"),
    made: todayISO(),
    stories: stories,
    points: points,
    helped: (analysis.helped || []).slice(0, 4).map((h) => String(h).slice(0, 120)),
    avgE: analysis.avgE,
    logs: (analysis.daily || []).length + (analysis.behavior || []).length
  };
}

function TrialOrPaywall({ dataStore, unlocked, onUnlock }) {
  if (unlocked) return <PaywallCard compact unlocked={true} onUnlock={onUnlock} />;
  const days = countLoggedDays(dataStore);
  const left = Math.max(0, FREE_LOG_DAYS - days);
  if (days < FREE_LOG_DAYS) {
    const pct = Math.min(100, Math.round((days / FREE_LOG_DAYS) * 100));
    return (
      <div className="trial-chip" title="Log seven different days, then preview your report">
        <div className="trial-label">Free week</div>
        <div className="trial-val">{days} / {FREE_LOG_DAYS} days logged</div>
        <div className="trial-hint">{left} more day{left === 1 ? "" : "s"} then a report preview</div>
        <div className="trial-bar" aria-hidden="true"><span style={{ width: pct + "%" }} /></div>
      </div>
    );
  }
  const analysis = buildStories(dataStore, 14);
  const preview = (analysis.stories || []).filter((s) => s.kicker !== "Getting started").slice(0, 2);
  return (
    <div>
      <PaywallCard compact unlocked={false} onUnlock={onUnlock} />
      {preview.length > 0 && (
        <div className="report-teaser">
          <div className="tk">Preview after your free week</div>
          {preview.map((s, i) => <p key={i}><strong>{s.kicker}.</strong> {s.text}</p>)}
        </div>
      )}
    </div>
  );
}

function MedReminderBanner({ dataStore, onDismiss }) {
  const due = collectDueMedReminders(dataStore);
  if (!due.length) return null;
  return (
    <div>
      {due.map((m) => (
        <div className="med-banner" key={m.id} role="status">
          <div>
            <strong>Med reminder</strong>
            <span>{m.name}{m.dose ? " · " + m.dose : ""} · due {m.due}</span>
          </div>
          <button type="button" onClick={() => onDismiss(m.id)}>Done</button>
        </div>
      ))}
    </div>
  );
}

function ShareReportView({ data }) {
  return (
    <div className="share-view">
      <div className="sv-brand">THE PLAYBOOK</div>
      <PageHeader kicker="Shared summary" title={(data.child || "Child") + " — care snapshot"} subtitle={(data.range || "") + " · made " + (data.made || "")} />
      <p style={{ fontSize: 13, color: "#6B7280" }}>This is a short summary a parent chose to share. It is not a diagnosis and does not include the full diary.</p>
      {data.avgE != null && <p style={{ fontWeight: 700 }}>Average energy: {Number(data.avgE).toFixed(1)} / 5 · {data.logs || 0} logs</p>}
      {(data.stories || []).map((s, i) => (
        <div className="card" key={i} style={{ marginTop: 10 }}>
          <div className="stat-label">{s.kicker}</div>
          <p style={{ margin: "6px 0 0" }}>{s.text}</p>
        </div>
      ))}
      {(data.points || []).length > 0 && (
        <div className="card" style={{ marginTop: 12 }}>
          <h3 style={{ marginTop: 0 }}>Talking points</h3>
          <ol>{data.points.map((p, i) => <li key={i}>{p}</li>)}</ol>
        </div>
      )}
      {(data.helped || []).length > 0 && (
        <div className="card" style={{ marginTop: 12 }}>
          <h3 style={{ marginTop: 0 }}>What already helps</h3>
          <ul>{data.helped.map((h, i) => <li key={i}>{h}</li>)}</ul>
        </div>
      )}
      <p style={{ marginTop: 24, fontSize: 12, color: "#9CA3AF" }}>Shared from theplaybook.cloud · parent-made summary</p>
    </div>
  );
}

'''

if "function countLoggedDays" not in text:
    anchor = "function PaywallCard({ onUnlock, unlocked, compact }) {"
    if anchor not in text:
        raise SystemExit("PaywallCard not found")
    text = text.replace(anchor, HELPERS + anchor, 1)

OLD_HOME_TOP = '''        <PaywallCard compact onUnlock={onUnlock} unlocked={unlocked} />
      </div>
      <div className="home-hero">'''

NEW_HOME_TOP = '''        <TrialOrPaywall dataStore={dataStore} unlocked={unlocked} onUnlock={onUnlock} />
      </div>
      <MedReminderBanner dataStore={dataStore} onDismiss={(id) => { dismissMedReminder(id); if (typeof showToast === "function") showToast("Reminder cleared"); }} />
      <div className="home-hero">'''

if "TrialOrPaywall dataStore={dataStore}" not in text:
    if OLD_HOME_TOP not in text:
        raise SystemExit("Home paywall block not found")
    text = text.replace(OLD_HOME_TOP, NEW_HOME_TOP, 1)

OLD_INS = '''  if (!unlocked) {
    return (
      <div>
        <PageHeader kicker="Patterns, not perfection" title="Insights" subtitle="Plain English from what you've actually logged." />
        <div className="locked-overlay">
          <p style={{ margin: "0 0 8px", fontWeight: 700, color: "var(--navy)" }}>See what your week is really saying</p>
          <p style={{ margin: "0 0 14px" }}>Story cards, energy trends, top triggers, and links between sleep and hard days — private on this device.</p>
          <button type="button" className="btn-primary" onClick={onRequestUnlock}>Unlock Insights · {PREMIUM_PRICE}</button>
        </div>
      </div>
    );
  }'''

NEW_INS = '''  const loggedDays = countLoggedDays(dataStore);
  if (!unlocked) {
    const ready = loggedDays >= FREE_LOG_DAYS;
    const preview = ready ? analysis.stories.filter((s) => s.kicker !== "Getting started").slice(0, 2) : [];
    return (
      <div>
        <PageHeader kicker="Patterns, not perfection" title="Insights" subtitle="Plain English from what you've actually logged." />
        {preview.map((s, i) => (
          <div className="card report-teaser" key={i} style={{ marginBottom: 10 }}>
            <div className="tk">{s.kicker}</div>
            <p>{s.text}</p>
          </div>
        ))}
        <div className="locked-overlay">
          <p style={{ margin: "0 0 8px", fontWeight: 700, color: "var(--navy)" }}>{ready ? "Your week has a shape — unlock the full dashboard" : "Log a week first, then this page fills in"}</p>
          <p style={{ margin: "0 0 14px" }}>{ready ? "Full story cards, energy trends and sleep links stay behind the one-time unlock." : (loggedDays + " of " + FREE_LOG_DAYS + " free days logged. Keep going — no payment yet.")}</p>
          {ready
            ? <button type="button" className="btn-primary" onClick={onRequestUnlock}>Unlock Insights · {PREMIUM_PRICE}</button>
            : <p style={{ margin: 0, fontSize: 13 }}>Quick Log on Today still counts.</p>}
        </div>
      </div>
    );
  }'''

if "Log a week first, then this page fills in" not in text:
    if OLD_INS not in text:
        raise SystemExit("Insights lock block not found")
    text = text.replace(OLD_INS, NEW_INS, 1)

OLD_REP_LOCK = '''  if (!unlocked) {
    return (
      <div>
        <PageHeader kicker="For appointments" title="Professional report" subtitle="A clean summary to hand to school, GP, or therapists." />
        <div className="locked-overlay">
          <p style={{ margin: "0 0 8px", fontWeight: 700, color: "var(--navy)" }}>Appointment-ready one-pager</p>
          <p style={{ margin: "0 0 14px" }}>Date range, KPIs, talking points, what already helps, and space for your note — print or Save as PDF.</p>
          <button type="button" className="btn-primary" onClick={onRequestUnlock}>Unlock report · {PREMIUM_PRICE}</button>
        </div>
      </div>
    );
  }'''

NEW_REP_LOCK = '''  const loggedDays = countLoggedDays(dataStore);
  if (!unlocked) {
    const ready = loggedDays >= FREE_LOG_DAYS;
    const sneak = ready ? buildTalkingPoints(buildStories(dataStore, 14)).slice(0, 2) : [];
    return (
      <div>
        <PageHeader kicker="For appointments" title="Professional report" subtitle="A clean summary to hand to school, GP, or therapists." />
        {sneak.length > 0 && (
          <div className="report-teaser" style={{ marginBottom: 12 }}>
            <div className="tk">Preview talking points</div>
            {sneak.map((p, i) => <p key={i}>{i + 1}. {p}</p>)}
          </div>
        )}
        <div className="locked-overlay">
          <p style={{ margin: "0 0 8px", fontWeight: 700, color: "var(--navy)" }}>{ready ? "This is the report you can hand over" : "Appointment-ready one-pager"}</p>
          <p style={{ margin: "0 0 14px" }}>{ready ? "Unlock to print, save as PDF, or send a private link to school or GP." : ("Log " + Math.max(0, FREE_LOG_DAYS - loggedDays) + " more day(s) to preview what your report would say.")}</p>
          {ready && <button type="button" className="btn-primary" onClick={onRequestUnlock}>Unlock report · {PREMIUM_PRICE}</button>}
        </div>
      </div>
    );
  }'''

if "Preview talking points" not in text:
    if OLD_REP_LOCK not in text:
        raise SystemExit("Report lock block not found")
    text = text.replace(OLD_REP_LOCK, NEW_REP_LOCK, 1)

OLD_REP_ACTIONS = '''      <div className="report-actions no-print">
        <button type="button" className="btn-primary" onClick={() => window.print()}>Print / Save as PDF</button>
      </div>'''

NEW_REP_ACTIONS = '''      <div className="report-actions no-print share-bar">
        <button type="button" className="btn-primary" onClick={() => window.print()}>Print / Save as PDF</button>
        <button type="button" className="btn-amber" onClick={async () => {
          try {
            const payload = buildSharePayload(dataStore, profileSafe, range);
            const url = window.location.origin + window.location.pathname + "?share=" + encodeSharePayload(payload);
            if (navigator.clipboard && navigator.clipboard.writeText) await navigator.clipboard.writeText(url);
            const st = document.getElementById("share-status");
            if (st) st.textContent = "Link copied — send only to people you trust.";
          } catch (e) {
            const st = document.getElementById("share-status");
            if (st) st.textContent = "Could not copy. Long-press and copy the address bar after tapping Share again.";
          }
        }}>Copy share link</button>
      </div>
      <p id="share-status" className="no-print" style={{ fontSize: 12, color: "#6B7280", minHeight: 16 }}></p>'''

if "Copy share link" not in text:
    if OLD_REP_ACTIONS not in text:
        raise SystemExit("Report actions block not found")
    text = text.replace(OLD_REP_ACTIONS, NEW_REP_ACTIONS, 1)

OLD_ROOT = "const root = ReactDOM.createRoot(document.getElementById(\"root\"));\nroot.render(React.createElement(App));"
NEW_ROOT = """function Root() {
  const shared = decodeShareParam();
  if (shared) return <ShareReportView data={shared} />;
  return <App />;
}
const root = ReactDOM.createRoot(document.getElementById(\"root\"));
root.render(React.createElement(Root));"""
if "function Root()" not in text:
    if OLD_ROOT not in text:
        raise SystemExit("React root render not found")
    text = text.replace(OLD_ROOT, NEW_ROOT, 1)

NOTIFY = '''
  useEffect(() => {
    if (!loaded) return;
    const due = collectDueMedReminders(dataStore);
    if (!due.length) return;
    if (!("Notification" in window)) return;
    const fire = () => {
      try {
        due.slice(0, 3).forEach((m) => {
          new Notification("THE PLAYBOOK", { body: "Med reminder: " + m.name + (m.dose ? " · " + m.dose : ""), tag: "med-" + m.id });
        });
      } catch (e) {}
    };
    if (Notification.permission === "granted") fire();
    else if (Notification.permission !== "denied") {
      Notification.requestPermission().then((p) => { if (p === "granted") fire(); }).catch(() => {});
    }
  }, [loaded, dataStore]);
'''

if "Med reminder:" not in text:
    after = """      setLoaded(true);
    }
    loadAll();
    return () => { cancelled = true; };
  }, []);
"""
    if after not in text:
        raise SystemExit("loadAll effect close not found")
    text = text.replace(after, after + "\n" + NOTIFY, 1)

text = text.replace("./sw.js?v=35", "./sw.js?v=36", 1)
text = text.replace("./sw.js?v=34", "./sw.js?v=36", 1)

APP.write_text(text, encoding="utf-8")
print("V36 patch applied")
for m in ["countLoggedDays", "TrialOrPaywall", "Copy share link", "ShareReportView", "MedReminderBanner", "THEME_BUILD_V36", "sw.js?v=36", "decodeShareParam"]:
    print(("OK " if m in text else "MISSING "), m)
