#!/usr/bin/env python3
"""Split teacher-note link from professional report / community."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

def main() -> None:
    html = APP.read_text(encoding="utf-8")

    html = html.replace(
        "<ConnectCard />\n      <SchoolLinkCard showToast={showToast} />\n      {cloudMode ? (",
        "<ConnectCard />\n      {cloudMode ? (",
        1,
    )

    html = html.replace(
        '<PageHeader kicker="Share with professionals" title="Professional report" subtitle="Print or Save as PDF (browser → Print → Save as PDF)." />\n      <SchoolLinkCard showToast={typeof showToast === "function" ? showToast : undefined} />\n      <SchoolInbox showToast={typeof showToast === "function" ? showToast : undefined} />',
        '<PageHeader kicker="For meetings" title="Professional report" subtitle="This page is the care summary for GP, school meetings, or therapists. The teacher daily-note link lives on Today." />',
        1,
    )
    html = html.replace(
        '<PageHeader kicker="Share with professionals" title="Professional report" subtitle="Print or Save as PDF (browser → Print → Save as PDF)." />',
        '<PageHeader kicker="For meetings" title="Professional report" subtitle="This page is the care summary for GP, school meetings, or therapists. The teacher daily-note link lives on Today." />',
        1,
    )

    if "function HomePage" in html:
        home = html.split("function HomePage")[1][:3000]
        if "<SchoolLinkCard" not in home and "<SchoolInbox showToast={showToast} />" in home:
            html = html.replace(
                "<SchoolInbox showToast={showToast} />",
                "<SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} />",
                1,
            )

    html = html.replace(">Copy share link</button>", ">Copy report snapshot</button>", 1)
    html = html.replace(">Copy this report (view only)</button>", ">Copy report snapshot</button>", 1)
    html = html.replace(
        "Link copied — send only to people you trust.",
        "Copied this report snapshot. It is view-only — not the teacher daily-note form.",
        1,
    )
    html = html.replace(
        "Copied: view-only care summary. This is not the teacher form — use School link above for that.",
        "Copied this report snapshot. It is view-only — not the teacher daily-note form.",
        1,
    )

    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=41")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V41 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")

    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v41"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")

    print("v41 split applied")


if __name__ == "__main__":
    main()
