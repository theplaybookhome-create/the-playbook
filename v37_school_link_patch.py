#!/usr/bin/env python3
"""V37 — School link feature.

Adds a 'School' entry point in the parent app (Community tab area) that lets a
parent generate a one-time link for a teacher. The teacher opens /school.html?t=TOKEN,
fills a simple daily form, and the report lands in the parent's Today feed.

Run from repo root:  python v37_school_link_patch.py
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

SCHOOL_CSS = """
/* ===== V37 school link ===== */
.school-card{ background:#fff; border:1.5px solid #E2E8F0; border-radius:18px; padding:16px; margin-bottom:14px; }
.school-card h3{ margin:0 0 4px; font-size:15px; color:#0E131F; }
.school-card p{ margin:0 0 12px; font-size:13px; color:#6B7280; line-height:1.45; }
.school-link-box{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.school-link-box input{ flex:1; min-width:180px; border:1.5px solid #E2E8F0; border-radius:12px; padding:10px 12px; font-size:13px; font-family:inherit; background:#F8FAFC; }
.school-link-box button{ border:0; border-radius:12px; padding:10px 14px; font-weight:700; font-size:13px; cursor:pointer; background:#0E131F; color:#fff; font-family:inherit; }
.school-entry{ background:#FFF8F2; border:1px solid #FFE0C7; border-radius:14px; padding:12px 14px; margin-bottom:10px; }
.school-entry .se-head{ display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
.school-entry .se-date{ font-size:11px; font-weight:700; color:#FF8A2B; text-transform:uppercase; letter-spacing:.06em; }
.school-entry .se-del{ border:0; background:none; color:#9CA3AF; cursor:pointer; font-size:14px; }
.school-entry .se-mood{ font-size:20px; }
.school-entry .se-line{ font-size:13px; color:#374151; line-height:1.4; margin-top:4px; }
.school-entry .se-tag{ display:inline-block; font-size:11px; font-weight:700; background:#fff; border:1px solid #F3D7B3; color:#C1752E; border-radius:999px; padding:2px 8px; margin-right:6px; }
"""

SCHOOL_JS = """
/* ===== V37: School link (parent generates token, teacher sends report) ===== */
const SCHOOL_FORM_URL = "./school.html";

function schoolToken() {
  return "s" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
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
function loadSchoolInbox() {
  try {
    const raw = localStorage.getItem("playbook:school-latest");
    return raw ? JSON.parse(raw) : null;
  } catch (e) { return null; }
}
function clearSchoolLatest() {
  try { localStorage.removeItem("playbook:school-latest"); } catch (e) {}
}
function schoolLinkFor(token) {
  return window.location.origin + window.location.pathname.replace(/app\.html$/, "") + "school.html?t=" + encodeURIComponent(token);
}

function SchoolLinkCard({ showToast }) {
  const [links, setLinks] = useState(() => loadSchoolLinks());
  const [copied, setCopied] = useState("");

  function makeLink() {
    const token = schoolToken();
    const entry = { token: token, created: todayISO(), label: "School link " + (links.length + 1) };
    const next = [entry, ...links].slice(0, 20);
    setLinks(next);
    saveSchoolLinks(next);
    const url = schoolLinkFor(token);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).catch(function () {});
    }
    setCopied(url);
    if (showToast) showToast("School link created & copied");
  }

  async function copyExisting(token) {
    const url = schoolLinkFor(token);
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) await navigator.clipboard.writeText(url);
      setCopied(url);
      if (showToast) showToast("Link copied");
    } catch (e) {
      setCopied(url);
    }
  }

  function revoke(token) {
    const next = links.filter(function (l) { return l.token !== token; });
    setLinks(next);
    saveSchoolLinks(next);
    if (showToast) showToast("Link revoked");
  }

  return (
    <div className="school-card">
      <h3>🏫 School link</h3>
      <p>Give the teacher a one-time link. They fill a short daily form — mood, incidents, one note — and it lands here for you. No login, no chat, no photos.</p>
      <button type="button" className="btn-primary" style={{ width: "100%" }} onClick={makeLink}>Create & copy new link</button>
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
      {copied ? <p style={{ fontSize: 11, color: "#9CA3AF", margin: "8px 0 0", wordBreak: "break-all" }}>Last copied: {copied}</p> : null}
    </div>
  );
}

function SchoolInbox({ dataStore, setDataStore, showToast }) {
  const [inbox, setInbox] = useState(function () {
    const latest = loadSchoolInbox();
    return latest ? [latest] : [];
  });

  useEffect(function () {
    const id = setInterval(function () {
      const latest = loadSchoolInbox();
      if (latest) {
        setInbox(function (cur) {
          if (cur[0] && cur[0].sentAt === latest.sentAt) return cur;
          return [latest];
        });
      }
    }, 4000);
    return function () { clearInterval(id); };
  }, []);

  function dismiss(sentAt) {
    setInbox(function (cur) { return cur.filter(function (x) { return x.sentAt !== sentAt; }); });
    clearSchoolLatest();
    if (showToast) showToast("School update dismissed");
  }

  if (!inbox.length) return null;
  return (
    <div style={{ marginBottom: 14 }}>
      {inbox.map(function (s) {
        return (
          <div className="school-entry" key={s.sentAt} role="status">
            <div className="se-head">
              <span className="se-date">🏫 School · {s.date || ""}</span>
              <button type="button" className="se-del" aria-label="Dismiss" onClick={function () { dismiss(s.sentAt); }}>✕</button>
            </div>
            <div><span className="se-tag">{s.child || "Child"}</span>{s.mood ? <span className="se-mood">{s.mood}</span> : null}</div>
            <div className="se-line">
              {s.energy ? <span className="se-tag">Energy: {s.energy}</span> : null}
              {s.incidents ? <span className="se-tag">Incidents: {s.incidents}</span> : null}
            </div>
            {s.wins ? <div className="se-line"><b>Wins:</b> {s.wins}</div> : null}
            {s.note ? <div className="se-line"><b>Note:</b> {s.note}</div> : null}
          </div>
        );
      })}
    </div>
  );
}
"""


def inject_css(html: str) -> str:
    needle = "/* ===== V36 trial / share / meds ===== */"
    if "V37 school link" in html:
        return html
    idx = html.find(needle)
    if idx == -1:
        # append before </style>
        return html.replace("</style>", SCHOOL_CSS + "\n</style>", 1)
    return html[:idx] + SCHOOL_CSS + "\n" + html[idx:]


def inject_js(html: str) -> str:
    if "V37: School link" in html:
        return html
    marker = "function Root() {"
    idx = html.find(marker)
    if idx == -1:
        raise SystemExit("Could not find Root() to inject school JS")
    return html[:idx] + SCHOOL_JS + "\n" + html[idx:]


def patch_home(html: str) -> str:
    """Insert <SchoolInbox/> into HomePage and a SchoolLinkCard into CommunityPage."""
    if "SchoolInbox" in html and "SchoolLinkCard" in html:
        return html

    # 1) HomePage: add inbox right after <MedReminderBanner ... />
    home_needle = '<MedReminderBanner dataStore={dataStore} onDismiss={(id) => { dismissMedReminder(id); if (typeof showToast === "function") showToast("Reminder cleared"); }} />'
    home_insert = home_needle + "\n      <SchoolInbox dataStore={dataStore} setDataStore={setDataStore} showToast={showToast} />"
    if home_needle in html:
        html = html.replace(home_needle, home_insert, 1)

    # 2) CommunityPage: add SchoolLinkCard after <ConnectCard />
    comm_needle = "<ConnectCard />\n      {cloudMode ? ("
    comm_insert = (
        "<ConnectCard />\n"
        "      <SchoolLinkCard showToast={showToast} />\n"
        "      {cloudMode ? ("
    )
    if "<SchoolLinkCard showToast={showToast} />" not in html and comm_needle in html:
        html = html.replace(comm_needle, comm_insert, 1)
    return html


def bump_sw(text: str) -> str:
    text2 = re.sub(r'const CACHE_NAME = "playbook-v\d+";', 'const CACHE_NAME = "playbook-v37";', text, count=1)
    text2 = re.sub(r'register\("./sw\.js\?v=\d+"\)', 'register("./sw.js?v=37")', text2, count=1)
    if text2 == text:
        print("warning: sw.js bump did not match expected pattern")
    return text2


def main() -> None:
    html = APP.read_text(encoding="utf-8")
    html = inject_css(html)
    html = inject_js(html)
    html = patch_home(html)
    # theme build marker
    html = html.replace("<!-- THEME_BUILD_V36 -->", "<!-- THEME_BUILD_V37 -->", 1)
    APP.write_text(html, encoding="utf-8")
    print("patched", APP, "bytes", APP.stat().st_size)

    sw = SW.read_text(encoding="utf-8")
    sw = bump_sw(sw)
    SW.write_text(sw, encoding="utf-8")
    print("bumped", SW)


if __name__ == "__main__":
    main()
