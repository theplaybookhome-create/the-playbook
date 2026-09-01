#!/usr/bin/env python3
"""V38 — Teacher can add a school note via the parent link (Supabase)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

SCHOOL_CSS = """
/* ===== V38 school cloud ===== */
.school-card{ background:#fff; border:1.5px solid #E2E8F0; border-radius:18px; padding:16px; margin-bottom:14px; }
.school-card h3{ margin:0 0 4px; font-size:15px; color:#0E131F; }
.school-card p{ margin:0 0 12px; font-size:13px; color:#6B7280; line-height:1.45; }
.school-entry{ background:#FFF8F2; border:1px solid #FFE0C7; border-radius:14px; padding:12px 14px; margin-bottom:10px; }
.school-entry .se-head{ display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
.school-entry .se-date{ font-size:11px; font-weight:700; color:#FF8A2B; text-transform:uppercase; letter-spacing:.06em; }
.school-entry .se-del{ border:0; background:none; color:#9CA3AF; cursor:pointer; font-size:14px; }
.school-entry .se-line{ font-size:13px; color:#374151; line-height:1.4; margin-top:4px; }
.school-entry .se-tag{ display:inline-block; font-size:11px; font-weight:700; background:#fff; border:1px solid #F3D7B3; color:#C1752E; border-radius:999px; padding:2px 8px; margin-right:6px; margin-top:4px; }
.school-setup{ font-size:12px; color:#92400E; background:#FFFBEB; border:1px solid #FDE68A; border-radius:10px; padding:8px 10px; margin-top:10px; }
.school-copied{ margin-top:12px; background:#ECFDF5; border:1.5px solid #6EE7B7; color:#065F46; border-radius:14px; padding:12px 14px; }
.school-copied strong{ display:block; font-size:14px; margin-bottom:4px; }
.school-copied .sc-url{ display:block; margin:8px 0; font-size:12px; word-break:break-all; background:#fff; border:1px solid #A7F3D0; border-radius:10px; padding:8px 10px; color:#064E3B; }
.school-copied .sc-hint{ font-size:12px; line-height:1.4; margin:0; }
.school-copied .sc-actions{ display:flex; gap:8px; margin-top:10px; flex-wrap:wrap; }
"""

SCHOOL_JS = r"""
/* ===== V38: School link cloud (teacher adds by link) ===== */
function schoolToken() {
  const bytes = new Uint8Array(12);
  if (window.crypto && window.crypto.getRandomValues) window.crypto.getRandomValues(bytes);
  else for (let i = 0; i < bytes.length; i++) bytes[i] = Math.floor(Math.random() * 256);
  return "s" + Array.from(bytes, function (b) { return b.toString(16).padStart(2, "0"); }).join("");
}
function loadSchoolLinks() {
  try {
    const raw = localStorage.getItem("playbook:school-links");
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch (e) { return []; }
}
function saveSchoolLinks(list) {
  try { localStorage.setItem("playbook:school-links", JSON.stringify(list)); } catch (e) {}
}
function loadSavedSchoolNotes() {
  try {
    const raw = localStorage.getItem("playbook:school-notes");
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch (e) { return []; }
}
function saveSavedSchoolNotes(list) {
  try { localStorage.setItem("playbook:school-notes", JSON.stringify(list.slice(0, 40))); } catch (e) {}
}
function schoolLinkFor(token) {
  const origin = (window.location && window.location.origin) || "https://theplaybook.cloud";
  return origin.replace(/\/$/, "") + "/school.html?t=" + encodeURIComponent(token);
}
function mapSchoolRow(row) {
  return {
    id: row.id || row.sentAt || String(row.created_at || Date.now()),
    token: row.token,
    child: row.child || "Child",
    date: row.note_date || row.date || "",
    mood: row.mood || "",
    energy: row.energy || "",
    incidents: row.incidents || "",
    wins: row.wins || "",
    note: row.body || row.note || "",
    author: row.author_name || row.author || "Teacher",
    sentAt: row.created_at || row.sentAt || ""
  };
}
async function publishSchoolLink(entry) {
  const sb = getSupabase();
  if (!sb) return { ok: false, reason: "no-cloud" };
  const { error } = await sb.from("playbook_share_links").upsert({
    token: entry.token,
    label: entry.label,
    child_label: entry.child || null,
    active: true
  });
  if (error) return { ok: false, reason: error.message || "cloud" };
  return { ok: true };
}
async function revokeSchoolLinkCloud(token) {
  const sb = getSupabase();
  if (!sb) return;
  await sb.from("playbook_share_links").update({ active: false }).eq("token", token);
}
async function fetchSchoolNotesForTokens(tokens) {
  const sb = getSupabase();
  if (!sb || !tokens.length) return { notes: loadSavedSchoolNotes(), error: null };
  const { data, error } = await sb.from("playbook_school_notes").select("*").in("token", tokens).order("created_at", { ascending: false }).limit(40);
  if (error) return { notes: loadSavedSchoolNotes(), error: error };
  const mapped = (data || []).map(mapSchoolRow);
  saveSavedSchoolNotes(mapped);
  return { notes: mapped, error: null };
}

function SchoolLinkCard({ showToast }) {
  const [links, setLinks] = useState(() => loadSchoolLinks());
  const [copied, setCopied] = useState("");
  const [copyState, setCopyState] = useState("");
  const [setupHint, setSetupHint] = useState("");

  async function copyUrl(url) {
    let ok = false;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(url);
        ok = true;
      }
    } catch (e) {}
    setCopied(url);
    setCopyState(ok ? "copied" : "manual");
    return ok;
  }

  async function shareUrl(url) {
    try {
      if (navigator.share) {
        await navigator.share({ title: "Playbook school note", text: "Please add today's note for our child.", url: url });
        return;
      }
    } catch (e) {}
    await copyUrl(url);
  }

  async function makeLink() {
    const token = schoolToken();
    const entry = { token: token, created: todayISO(), label: "School link " + (links.length + 1) };
    const published = await publishSchoolLink(entry);
    if (!published.ok) {
      setSetupHint("Link is ready, but teacher send may fail until cloud tables exist.");
    } else {
      setSetupHint("");
    }
    const next = [entry, ...links].slice(0, 20);
    setLinks(next);
    saveSchoolLinks(next);
    const url = schoolLinkFor(token);
    const ok = await copyUrl(url);
    if (showToast) showToast(ok ? "Copied — send this to the teacher" : "Link created — copy it from the green box");
  }

  async function copyExisting(token) {
    const url = schoolLinkFor(token);
    const ok = await copyUrl(url);
    if (showToast) showToast(ok ? "Teacher link copied" : "Copy the link from the green box");
  }

  async function revoke(token) {
    const next = links.filter(function (l) { return l.token !== token; });
    setLinks(next);
    saveSchoolLinks(next);
    if (copied && copied.indexOf(token) !== -1) { setCopied(""); setCopyState(""); }
    await revokeSchoolLinkCloud(token);
    if (showToast) showToast("Link revoked");
  }

  return (
    <div className="school-card">
      <h3>Teacher note link</h3>
      <p>This is only for the teacher. They get a short form (mood, energy, incidents, wins). They never see your diary or the professional report.</p>
      <button type="button" className="btn-primary" style={{ width: "100%" }} onClick={makeLink}>Create teacher link</button>
      {copied ? (
        <div className="school-copied" role="status">
          <strong>{copyState === "copied" ? "Copied to clipboard" : "Link created — copy it below"}</strong>
          <span className="sc-url">{copied}</span>
          <p className="sc-hint">Send this to the teacher. It must say school.html — if it says share= it is the wrong button.</p>
          <div className="sc-actions">
            <button type="button" className="btn-secondary" style={{ padding: "8px 12px", fontSize: 13 }} onClick={function () { copyUrl(copied); }}>Copy again</button>
            <button type="button" className="btn-amber" style={{ padding: "8px 12px", fontSize: 13 }} onClick={function () { shareUrl(copied); }}>Share with teacher</button>
          </div>
        </div>
      ) : null}
      {links.length > 0 && (
        <div style={{ marginTop: 12 }}>
          {links.map(function (l) {
            return (
              <div key={l.token} style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 8, flexWrap: "wrap" }}>
                <span style={{ fontSize: 12, color: "#6B7280", flex: "1 1 160px" }}>{l.label} · {l.created}</span>
                <button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={function () { copyExisting(l.token); }}>Copy</button>
                <button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12, color: "#B03A2E" }} onClick={function () { revoke(l.token); }}>Revoke</button>
              </div>
            );
          })}
        </div>
      )}
      {setupHint ? <div className="school-setup">{setupHint}</div> : null}
    </div>
  );
}

function SchoolInbox({ showToast }) {
  const [inbox, setInbox] = useState(() => loadSavedSchoolNotes());
  const [status, setStatus] = useState("");

  async function refresh() {
    const tokens = loadSchoolLinks().map(function (l) { return l.token; });
    const result = await fetchSchoolNotesForTokens(tokens);
    setInbox(result.notes || []);
    if (result.error) setStatus("Could not reach school inbox yet.");
    else setStatus(result.notes && result.notes.length ? "" : "No school notes yet.");
  }

  useEffect(function () {
    refresh();
    const id = setInterval(refresh, 20000);
    return function () { clearInterval(id); };
  }, []);

  function dismiss(id) {
    const next = inbox.filter(function (x) { return x.id !== id; });
    setInbox(next);
    saveSavedSchoolNotes(next);
    if (showToast) showToast("School update hidden on this device");
  }

  return (
    <div style={{ marginBottom: 14 }}>
      {inbox.map(function (s) {
        return (
          <div className="school-entry" key={s.id} role="status">
            <div className="se-head">
              <span className="se-date">School · {s.date || ""} · {s.author || "Teacher"}</span>
              <button type="button" className="se-del" aria-label="Dismiss" onClick={function () { dismiss(s.id); }}>✕</button>
            </div>
            <div>
              <span className="se-tag">{s.child || "Child"}</span>
              {s.mood ? <span className="se-tag">{s.mood}</span> : null}
              {s.energy ? <span className="se-tag">Energy: {s.energy}</span> : null}
              {s.incidents ? <span className="se-tag">Incidents: {s.incidents}</span> : null}
            </div>
            {s.wins ? <div className="se-line"><b>Wins:</b> {s.wins}</div> : null}
            {s.note ? <div className="se-line"><b>Note:</b> {s.note}</div> : null}
          </div>
        );
      })}
      <button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={refresh}>Refresh school notes</button>
      {status ? <p style={{ fontSize: 12, color: "#6B7280", margin: "6px 0 0" }}>{status}</p> : null}
    </div>
  );
}
"""


def inject_css(html: str) -> str:
    if "/* ===== V38 school cloud ===== */" in html:
        html = re.sub(
            r"/\* ===== V38 school cloud ===== \*/.*?\.school-setup\{[^}]*\}(?:\n\.school-copied[\s\S]*?\.school-copied \.sc-actions\{[^}]*\})?",
            SCHOOL_CSS.strip(),
            html,
            count=1,
            flags=re.S,
        )
        return html
    needle = "/* ===== V36 trial / share / meds ===== */"
    if needle in html:
        return html.replace(needle, SCHOOL_CSS + "\n" + needle, 1)
    return html.replace("</style>", SCHOOL_CSS + "\n</style>", 1)


def inject_js(html: str) -> str:
    if "V38: School link cloud" in html:
        html = re.sub(
            r"/\* ===== V38: School link cloud ===== \*/.*?^function SchoolInbox\([\s\S]*?^\}\n",
            SCHOOL_JS.lstrip() + "\n",
            html,
            count=1,
            flags=re.M,
        )
        return html
    marker = "function Root() {"
    idx = html.find(marker)
    if idx == -1:
        raise SystemExit("Could not find Root() to inject school JS")
    return html[:idx] + SCHOOL_JS + "\n" + html[idx:]


def patch_pages(html: str) -> str:
    home_needle = '<MedReminderBanner dataStore={dataStore} onDismiss={(id) => { dismissMedReminder(id); if (typeof showToast === "function") showToast("Reminder cleared"); }} />'
    if home_needle in html and "<SchoolInbox" not in html.split("function HomePage")[1][:1800]:
        html = html.replace(home_needle, home_needle + "\n      <SchoolInbox showToast={showToast} />", 1)

    comm_needle = "<ConnectCard />\n      {cloudMode ? ("
    if comm_needle in html and "<SchoolLinkCard showToast={showToast} />" not in html:
        html = html.replace(
            comm_needle,
            "<ConnectCard />\n      <SchoolLinkCard showToast={showToast} />\n      {cloudMode ? (",
            1,
        )

    report_needle = '<PageHeader kicker="Share with professionals" title="Professional report" subtitle="Print or Save as PDF (browser → Print → Save as PDF)." />'
    if report_needle in html and "SchoolLinkCard" not in html.split("function ReportPage")[1][:2500]:
        html = html.replace(
            report_needle,
            report_needle + "\n      <SchoolLinkCard showToast={typeof showToast === \"function\" ? showToast : undefined} />\n      <SchoolInbox showToast={typeof showToast === \"function\" ? showToast : undefined} />",
            1,
        )
    html = html.replace(
        "function ReportPage({ dataStore, profile, unlocked, onRequestUnlock }) {",
        "function ReportPage({ dataStore, profile, unlocked, onRequestUnlock, showToast }) {",
        1,
    )
    html = html.replace(
        "<ReportPage dataStore={dataStore} profile={profile} unlocked={unlocked} onRequestUnlock={requestUnlock} />",
        "<ReportPage dataStore={dataStore} profile={profile} unlocked={unlocked} onRequestUnlock={requestUnlock} showToast={showToast} />",
        1,
    )
    html = html.replace(">Copy share link</button>", ">Copy this report (view only)</button>", 1)
    html = html.replace(
        "Link copied — send only to people you trust.",
        "Copied: view-only care summary. This is not the teacher form — use School link above for that.",
        1,
    )
    return html


def bump_sw(text: str) -> str:
    text = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v40"', text, count=1)
    text = re.sub(r'CACHE_NAME = "playbook-v\d+"', 'CACHE = "playbook-v40"', text)
    return text


def bump_app_sw_register(html: str) -> str:
    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=40")', html, count=1)
    for n in range(36, 40):
        html = html.replace(f"<!-- THEME_BUILD_V{n} -->", "<!-- THEME_BUILD_V40 -->", 1)
    return html


def main() -> None:
    html = APP.read_text(encoding="utf-8")
    html = inject_css(html)
    html = inject_js(html)
    html = patch_pages(html)
    html = bump_app_sw_register(html)
    APP.write_text(html, encoding="utf-8")
    print("patched", APP, "bytes", APP.stat().st_size)
    print("has SchoolLinkCard", "SchoolLinkCard" in html)
    print("has SchoolInbox", "SchoolInbox" in html)
    print("has V38 js", "V38: School link cloud" in html)

    sw = SW.read_text(encoding="utf-8")
    SW.write_text(bump_sw(sw), encoding="utf-8")
    print("bumped", SW)


if __name__ == "__main__":
    main()
