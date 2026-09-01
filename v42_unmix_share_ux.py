#!/usr/bin/env python3
"""v42 — stop mixing teacher-form link with professional report snapshot."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"


def strip_compact_duplicate(html: str) -> str:
    """Remove the minified first SchoolLinkCard/SchoolInbox block if a pretty copy follows."""
    if html.count("function SchoolLinkCard") < 2:
        return html
    html = re.sub(
        r"\nfunction SchoolLinkCard\(\{showToast\}\)\{.*?\n\}\n+"
        r"function SchoolInbox\(\{showToast\}\)\{.*?\n\}\n+",
        "\n",
        html,
        count=1,
        flags=re.S,
    )
    return html


def main() -> None:
    html = APP.read_text(encoding="utf-8")
    html = strip_compact_duplicate(html)

    html = html.replace(
        "<ConnectCard />\n      <SchoolLinkCard showToast={showToast} />\n      {cloudMode ? (",
        "<ConnectCard />\n      {cloudMode ? (",
        1,
    )
    html = html.replace(
        "<ConnectCard />\n      <SchoolLinkCard showToast={showToast} />",
        "<ConnectCard />",
        1,
    )

    html = html.replace(
        '<PageHeader kicker="Share with professionals" title="Professional report" subtitle="Print or Save as PDF (browser → Print → Save as PDF)." />\n      <SchoolLinkCard showToast={typeof showToast === "function" ? showToast : undefined} />\n      <SchoolInbox showToast={typeof showToast === "function" ? showToast : undefined} />',
        '<PageHeader kicker="For meetings" title="Professional report" subtitle="Read-only care summary for GP, SENCO, or therapists. This is not the teacher daily form." />',
        1,
    )
    html = html.replace(
        '<PageHeader kicker="For meetings" title="Professional report" subtitle="This page is the care summary for GP, school meetings, or therapists. The teacher daily-note link lives on Today." />',
        '<PageHeader kicker="For meetings" title="Professional report" subtitle="Read-only care summary for GP, SENCO, or therapists. This is not the teacher daily form — that lives on Today." />',
        1,
    )
    html = html.replace(
        '<PageHeader kicker="For appointments" title="Professional report" subtitle="A clean summary to hand to school, GP, or therapists." />',
        '<PageHeader kicker="For meetings" title="Professional report" subtitle="Read-only care summary for GP, SENCO, or therapists." />',
        1,
    )

    if "function HomePage" in html:
        home = html.split("function HomePage")[1][:3500]
        if "<SchoolLinkCard" not in home and "<SchoolInbox showToast={showToast} />" in html.split("function HomePage")[1][:3500]:
            html = html.replace(
                "<SchoolInbox showToast={showToast} />",
                "<SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} />",
                1,
            )

    html = html.replace(
        "<strong>Pro report</strong><span className=\"ql-hint\">Print for school / GP</span>",
        "<strong>Meeting summary</strong><span className=\"ql-hint\">Printable care report — not the teacher form</span>",
        1,
    )

    html = html.replace(">Copy share link</button>", ">Copy meeting-summary link</button>")
    html = html.replace(">Copy this report (view only)</button>", ">Copy meeting-summary link</button>")
    html = html.replace(">Copy report snapshot</button>", ">Copy meeting-summary link</button>")
    html = html.replace(
        '        <button type="button" className="btn-amber" onClick={async () => {\n          try {\n            const payload = buildSharePayload(dataStore, profileSafe, range);',
        '        <button type="button" className="btn-secondary" onClick={async () => {\n          try {\n            const payload = buildSharePayload(dataStore, profileSafe, range);',
        1,
    )
    html = html.replace(
        "Copied this report snapshot. It is view-only — not the teacher daily-note form.",
        "Copied a view-only meeting summary. This is NOT the teacher form (that one says school.html).",
    )
    html = html.replace(
        "Copied: view-only care summary. This is not the teacher form — use School link above for that.",
        "Copied a view-only meeting summary. This is NOT the teacher form (that one says school.html).",
    )
    html = html.replace(
        "Link copied — send only to people you trust.",
        "Copied a view-only meeting summary. This is NOT the teacher form (that one says school.html).",
    )

    if 'id="share-status"' in html and "Need the teacher form" not in html:
        html = html.replace(
            '<p id="share-status" className="no-print" style={{ fontSize: 12, color: "#6B7280", minHeight: 16 }}></p>',
            '<p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>\n      <p id="share-status" className="no-print" style={{ fontSize: 12, color: "#6B7280", minHeight: 16 }}></p>',
            1,
        )

    html = html.replace("<h3>Teacher note link</h3>", "<h3>Teacher form link</h3>")
    html = html.replace("<h3>School link</h3>", "<h3>Teacher form link</h3>")
    html = html.replace(
        "<p>This is only for the teacher. They get a short form (mood, energy, incidents, wins). They never see your diary or the professional report.</p>",
        "<p><b>This is not the professional report.</b> The teacher gets a short form (mood, energy, incidents, wins). They never see your diary. Notes come back here on Today.</p>",
    )
    html = html.replace(
        "<p>Give the teacher this link. They add today's note and it lands in your Playbook. They never see the full diary.</p>",
        "<p><b>This is not the professional report.</b> The teacher gets a short form. Notes come back here on Today.</p>",
    )
    html = html.replace(">Create teacher link</button>", ">Create teacher form link</button>")
    html = html.replace(">Create & copy school link</button>", ">Create teacher form link</button>")
    html = html.replace(
        "Send this to the teacher. It must say school.html — if it says share= it is the wrong button.",
        "Send this to the teacher. The address must include school.html — if it includes share= you copied the meeting summary by mistake.",
    )
    html = html.replace(
        "if (showToast) showToast(ok ? \"Copied — send this to the teacher\" : \"Link created — copy it from the green box\");",
        "if (showToast) showToast(ok ? \"Teacher form link copied\" : \"Link created — copy it from the green box\");",
    )
    html = html.replace(
        '<button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={function () { copyExisting(l.token); }}>Copy</button>',
        '<button type="button" className="btn-secondary" style={{ padding: "6px 10px", fontSize: 12 }} onClick={function () { copyExisting(l.token); }}>Copy teacher form</button>',
    )
    html = html.replace('label: "School link " + (links.length + 1)', 'label: "Teacher form " + (links.length + 1)')

    if "<h3>Notes from teacher</h3>" not in html:
        html = html.replace(
            '  return (\n    <div style={{ marginBottom: 14 }}>\n      {inbox.map(function (s) {',
            '  return (\n    <div style={{ marginBottom: 14 }}>\n      <h3 style={{ fontSize: 15, margin: "0 0 8px" }}>Notes from teacher</h3>\n      {inbox.map(function (s) {',
            1,
        )

    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=42")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V42 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")

    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v42"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")

    def page_has(fn: str, needle: str) -> str:
        if f"function {fn}" not in html:
            return "missing-page"
        body = html.split(f"function {fn}")[1][:4000]
        return str(needle in body)

    print("v42 unmix applied")
    print("compact leftover", html.count("Create & copy school link"), "SchoolLinkCard defs", html.count("function SchoolLinkCard"))
    print("community card", page_has("CommunityPage", "SchoolLinkCard"))
    print("report card", page_has("ReportPage", "SchoolLinkCard"))
    print("home card", page_has("HomePage", "SchoolLinkCard"))
    print("report btn", "Copy meeting-summary link" in html, "Copy report snapshot" in html, "Copy share link" in html)


if __name__ == "__main__":
    main()
