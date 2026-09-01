#!/usr/bin/env python3
"""v47 — School tab owns links; Today shows only the latest note; fetch per token."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

NEW_FETCH = r"""async function fetchSchoolNotesForTokens(tokens) {
  const local = loadSavedSchoolNotes();
  const uniq = [];
  (tokens || []).forEach(function (t) {
    const s = String(t || "").trim();
    if (s && uniq.indexOf(s) === -1) uniq.push(s);
  });
  if (!SUPABASE_URL || !SUPABASE_ANON_KEY || !uniq.length) return { notes: local, error: null };
  try {
    const collected = [];
    let lastErr = null;
    for (let i = 0; i < uniq.length; i++) {
      const res = await fetch(
        SUPABASE_URL + "/rest/v1/playbook_school_notes?token=eq." + encodeURIComponent(uniq[i]) + "&select=*&order=created_at.desc&limit=40",
        { headers: { apikey: SUPABASE_ANON_KEY, Authorization: "Bearer " + SUPABASE_ANON_KEY } }
      );
      if (!res.ok) {
        lastErr = { message: await res.text() };
        continue;
      }
      const data = await res.json();
      (data || []).forEach(function (row) { collected.push(mapSchoolRow(row)); });
    }
    const byId = {};
    local.forEach(function (n) { if (n && n.id) byId[n.id] = n; });
    collected.forEach(function (n) { if (n && n.id) byId[n.id] = n; });
    const merged = Object.keys(byId).map(function (k) { return byId[k]; });
    merged.sort(function (a, b) { return String(b.sentAt || "").localeCompare(String(a.sentAt || "")); });
    saveSavedSchoolNotes(merged);
    return { notes: merged, error: collected.length ? null : lastErr };
  } catch (e) {
    return { notes: local, error: e };
  }
}"""

NEW_INBOX = r"""function SchoolInbox({ showToast, latestOnly, onSeeAll, title }) {
  const [inbox, setInbox] = useState(() => loadSavedSchoolNotes());
  const [status, setStatus] = useState("");
  const [checkedAt, setCheckedAt] = useState("");
  const [busy, setBusy] = useState(false);
  const linkCount = loadSchoolLinks().length;

  async function refresh() {
    setBusy(true);
    const tokens = loadSchoolLinks().map(function (l) { return l.token; });
    if (!tokens.length) {
      setInbox([]);
      setStatus("Create a teacher form link first, then send it to school.");
      setCheckedAt(new Date().toLocaleTimeString());
      setBusy(false);
      return;
    }
    const result = await fetchSchoolNotesForTokens(tokens);
    const notes = result.notes || [];
    setInbox(notes);
    setCheckedAt(new Date().toLocaleTimeString());
    if (result.error && !notes.length) setStatus("Could not reach the school inbox. Check you are online, then tap Check again.");
    else if (!notes.length) setStatus("No teacher notes yet. Open the form on another phone, tap Send to parent, then tap Check again.");
    else setStatus("");
    setBusy(false);
  }

  useEffect(function () {
    refresh();
    const id = setInterval(refresh, 12000);
    return function () { clearInterval(id); };
  }, []);

  function dismiss(id) {
    const next = inbox.filter(function (x) { return x.id !== id; });
    setInbox(next);
    saveSavedSchoolNotes(next);
    if (showToast) showToast("School update hidden on this device");
  }

  const shown = latestOnly ? inbox.slice(0, 1) : inbox;

  return (
    <div className="school-inbox" style={{ marginBottom: 14 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8, marginBottom: 8, flexWrap: "wrap" }}>
        <h3 style={{ fontSize: 15, margin: 0 }}>{title || (latestOnly ? "Latest teacher note" : "All teacher notes")}</h3>
        {latestOnly && onSeeAll ? (
          <button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={onSeeAll}>See all</button>
        ) : null}
      </div>
      {shown.map(function (s) {
        return (
          <div className="school-entry" key={s.id} role="status">
            <div className="se-head">
              <span className="se-date">Received · {s.date || ""} · {s.author || "Teacher"}</span>
              {latestOnly ? null : (
                <button type="button" className="se-del" aria-label="Dismiss" onClick={function () { dismiss(s.id); }}>✕</button>
              )}
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
      {!shown.length ? <p style={{ fontSize: 13, color: "#6B7280", margin: "0 0 8px" }}>{status || "No teacher notes yet."}</p> : null}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
        <button type="button" className="btn-secondary" style={{ padding: "8px 12px", fontSize: 13 }} onClick={refresh} disabled={busy}>{busy ? "Checking…" : "Check for notes"}</button>
        {latestOnly && onSeeAll ? <button type="button" className="btn-secondary" style={{ padding: "8px 12px", fontSize: 13 }} onClick={onSeeAll}>School tab</button> : null}
      </div>
      <p style={{ fontSize: 11, color: "#9CA3AF", margin: "6px 0 0" }}>
        {linkCount ? (linkCount + " teacher link" + (linkCount === 1 ? "" : "s") + " on this phone") : "No teacher link on this phone yet"}
        {checkedAt ? " · last check " + checkedAt : ""}
      </p>
    </div>
  );
}

function SchoolNotesPage({ showToast }) {
  return (
    <div>
      <PageHeader kicker="From school" title="Teacher notes" subtitle="Create the teacher form here. After they send it, tap Check for notes. Today only keeps the most recent one." />
      <SchoolLinkCard showToast={showToast} />
      <SchoolInbox showToast={showToast} title="All teacher notes" />
    </div>
  );
}"""


def replace_function(html: str, name: str, new_src: str) -> str:
    start = html.find("function " + name + "(")
    if start == -1:
        start = html.find("function " + name + "({")
    if start == -1:
        return html
    i = html.find("{", start)
    if i == -1:
        return html
    depth = 0
    for j in range(i, len(html)):
        if html[j] == "{":
            depth += 1
        elif html[j] == "}":
            depth -= 1
            if depth == 0:
                return html[:start] + new_src.rstrip() + "\n\n" + html[j + 1 :].lstrip("\n")
    return html


def dedupe_lines(html: str, needle: str) -> str:
    parts = html.split(needle)
    if len(parts) <= 2:
        return html
    return needle.join([parts[0], parts[1]]) + "".join(parts[2:])


def main() -> None:
    html = APP.read_text(encoding="utf-8")

    if "Check for notes" not in html or "token=eq." not in html.split("async function fetchSchoolNotesForTokens")[1][:800]:
        html = replace_function(html, "fetchSchoolNotesForTokens", NEW_FETCH)
        html = replace_function(html, "SchoolInbox", NEW_INBOX)
        orphan = html.find("\n) {\n  const [inbox, setInbox]")
        root = html.find("\nfunction Root()")
        if orphan != -1 and root != -1 and orphan < root:
            html = html[:orphan] + "\n\n" + html[root:]

    html = html.replace(
        "      <SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />\n",
        "      <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />\n",
    )
    html = html.replace(
        "      <SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} />\n",
        "      <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />\n",
    )

    html = html.replace(
        "They never see your diary. Notes come back here on Today.",
        "They never see your diary. Sent notes land on this School tab. Today only shows the latest one.",
    )

    if "Open form to test" not in html:
        html = html.replace(
            '<button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={function () { copyExisting(l.token); }}>Copy teacher form</button>',
            '<button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={function () { copyExisting(l.token); }}>Copy</button>\n                <button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={function () { window.open(schoolLinkFor(l.token), "_blank"); }}>Open form to test</button>',
        )

    html = dedupe_lines(
        html,
        '<button type="button" className={"hchip" + (mainTab === "school" ? " active" : "")} onClick={() => navigate("school")}>🏫 Teacher notes</button>\n',
    )
    html = dedupe_lines(
        html,
        '          : mainTab === "school" ? <SchoolNotesPage showToast={showToast} />\n',
    )

    html = re.sub(
        r'\n    \{ id: "community", label: "Community", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="9" cy="8" r="3"/><circle cx="16" cy="9" r="2\.4"/><path d="M3\.5 19c\.6-3 2\.8-5 5\.5-5s4\.9 2 5\.5 5"/></svg> \},',
        "",
        html,
        count=1,
    )

    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=47")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V47 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")

    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v47"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")

    print("v47 school verify")
    print("theme", "THEME_BUILD_V47" in html)
    print("open to test", "Open form to test" in html)
    print("SchoolNotesPage", html.count("function SchoolNotesPage"))
    print("orphan", ") {\n  const [inbox, setInbox]" in html and html.find(") {\n  const [inbox, setInbox]") < html.find("function SchoolInbox"))


if __name__ == "__main__":
    main()
