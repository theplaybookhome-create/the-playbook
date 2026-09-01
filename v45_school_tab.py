#!/usr/bin/env python3
"""v45 - School tab for all teacher notes; Today shows only the latest."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

OLD_FETCH = """async function fetchSchoolNotesForTokens(tokens) {
  const sb = getSupabase();
  if (!sb || !tokens.length) return { notes: loadSavedSchoolNotes(), error: null };
  const { data, error } = await sb.from("playbook_school_notes").select("*").in("token", tokens).order("created_at", { ascending: false }).limit(40);
  if (error) return { notes: loadSavedSchoolNotes(), error: error };
  const mapped = (data || []).map(mapSchoolRow);
  saveSavedSchoolNotes(mapped);
  return { notes: mapped, error: null };
}"""

NEW_FETCH = r"""async function fetchSchoolNotesForTokens(tokens) {
  const local = loadSavedSchoolNotes();
  if (!SUPABASE_URL || !SUPABASE_ANON_KEY || !tokens.length) return { notes: local, error: null };
  try {
    const list = tokens.filter(Boolean).map(function (t) { return encodeURIComponent(String(t)); }).join(",");
    const res = await fetch(
      SUPABASE_URL + "/rest/v1/playbook_school_notes?token=in.(" + list + ")&select=*&order=created_at.desc&limit=40",
      { headers: { apikey: SUPABASE_ANON_KEY, Authorization: "Bearer " + SUPABASE_ANON_KEY } }
    );
    if (!res.ok) return { notes: local, error: { message: await res.text() } };
    const data = await res.json();
    const mapped = (data || []).map(mapSchoolRow);
    saveSavedSchoolNotes(mapped);
    return { notes: mapped, error: null };
  } catch (e) {
    return { notes: local, error: e };
  }
}"""

NEW_INBOX = r"""function SchoolInbox({ showToast, latestOnly, onSeeAll, title }) {
  const [inbox, setInbox] = useState(() => loadSavedSchoolNotes());
  const [status, setStatus] = useState("");

  async function refresh() {
    const tokens = loadSchoolLinks().map(function (l) { return l.token; });
    const result = await fetchSchoolNotesForTokens(tokens);
    const notes = result.notes || [];
    setInbox(notes);
    if (result.error) setStatus("Could not reach school inbox yet.");
    else setStatus(notes.length ? "" : "No teacher notes yet. When the teacher taps Send, it appears here.");
  }

  useEffect(function () {
    refresh();
    const id = setInterval(refresh, 15000);
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
    <div style={{ marginBottom: 14 }}>
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
              <span className="se-date">School · {s.date || ""} · {s.author || "Teacher"}</span>
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
      <button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={refresh}>Refresh notes</button>
      {shown.length && status ? <p style={{ fontSize: 12, color: "#6B7280", margin: "6px 0 0" }}>{status}</p> : null}
    </div>
  );
}

function SchoolNotesPage({ showToast }) {
  return (
    <div>
      <PageHeader kicker="From school" title="Teacher notes" subtitle="Every note sent through your teacher form link. Today only keeps the latest one." />
      <SchoolLinkCard showToast={showToast} />
      <SchoolInbox showToast={showToast} title="All teacher notes" />
    </div>
  );
}
"""


def replace_function(html: str, name: str, new_src: str) -> str:
    start = html.find("function " + name + "(")
    if start == -1:
        start = html.find("function " + name + "({")
    if start == -1:
        return html
    depth = 0
    i = html.find("{", start)
    if i == -1:
        return html
    for j in range(i, len(html)):
        if html[j] == "{":
            depth += 1
        elif html[j] == "}":
            depth -= 1
            if depth == 0:
                return html[:start] + new_src.rstrip() + "\n\n" + html[j + 1 :].lstrip("\n")
    return html


def main() -> None:
    html = APP.read_text(encoding="utf-8")
    if OLD_FETCH in html:
        html = html.replace(OLD_FETCH, NEW_FETCH, 1)
    elif "token=in.(" not in html:
        html = replace_function(html, "fetchSchoolNotesForTokens", NEW_FETCH)
    html = replace_function(html, "SchoolInbox", NEW_INBOX)
    html = html.replace(
        "<SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} />",
        "<SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />",
        1,
    )
    html = html.replace(
        '{ id: "home", label: "Today", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/></svg> },\n    { id: "track", label: "Track",',
        '{ id: "home", label: "Today", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/></svg> },\n    { id: "school", label: "School", ico: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 20V6l8-3 8 3v14"/><path d="M12 3v17M8 20h8"/></svg> },\n    { id: "track", label: "Track",',
        1,
    )
    html = html.replace(
        '          : mainTab === "track" ? (',
        '          : mainTab === "school" ? <SchoolNotesPage showToast={showToast} />\n          : mainTab === "track" ? (',
        1,
    )
    html = html.replace(
        '<button type="button" className={"hchip" + (mainTab === "track" ? " active" : "")} onClick={() => navigate("track", "daily")}>\U0001f512 Private tracking</button>',
        '<button type="button" className={"hchip" + (mainTab === "school" ? " active" : "")} onClick={() => navigate("school")}>\U0001f3eb Teacher notes</button>\n          <button type="button" className={"hchip" + (mainTab === "track" ? " active" : "")} onClick={() => navigate("track", "daily")}>\U0001f512 Private tracking</button>',
        1,
    )
    html = html.replace(
        ".bottom-btn .lbl { font-size: 10px; font-weight: 700; color: var(--muted); }",
        ".bottom-btn .lbl { font-size: 9px; font-weight: 700; color: var(--muted); }",
        1,
    )
    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=45")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V45 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")
    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v45"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")
    print("v45 school tab")
    print("school tab nav", '{ id: "school"' in html)
    print("SchoolNotesPage", "function SchoolNotesPage" in html)
    print("anon in.(", "token=in.(" in html)


if __name__ == "__main__":
    main()
