#!/usr/bin/env python3
"""v48 — Today keeps only the latest teacher note; link card stays on School tab."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

OLD = """      <section className=\"school-section\" aria-labelledby=\"teacher-log-heading\">
        <div className=\"school-section-head\">
          <h2 id=\"teacher-log-heading\">Teacher log</h2>
          <p>Keep school notes in one place. Teachers only get a short form — they never see your diary.</p>
        </div>
        <SchoolLinkCard showToast={showToast} />
        <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />
      </section>"""

NEW = """      <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />"""

def main() -> None:
    html = APP.read_text(encoding="utf-8")
    if OLD in html:
        html = html.replace(OLD, NEW, 1)
    html = html.replace(
        "      <SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />",
        "      <SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />",
    )
    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=48")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V48 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")
    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v48"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")
    home = html.split("function HomePage")[1][:3200]
    print("v48")
    print("home link card", "<SchoolLinkCard" in home)
    print("home latestOnly", "latestOnly={true}" in home)
    print("school-section on home", "school-section" in home)

if __name__ == "__main__":
    main()
