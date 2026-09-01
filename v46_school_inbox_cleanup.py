#!/usr/bin/env python3
"""v46 - drop leftover inbox fragment; Today shows only the latest note."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"


def main() -> None:
    html = APP.read_text(encoding="utf-8")

    idx = html.find("function SchoolNotesPage")
    if idx != -1:
        orphan = html.find("\n) {", idx)
        root = html.find("\nfunction Root()", idx)
        if orphan != -1 and root != -1 and orphan < root:
            html = html[:orphan] + "\n\n" + html[root:]

    html = html.replace(
        "<SchoolInbox showToast={showToast} />",
        "<SchoolInbox showToast={showToast} latestOnly={true} onSeeAll={function () { onNavigate(\"school\"); }} />",
    )

    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=46")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V46 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")

    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v46"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")

    print("v46 cleanup")
    print("latestOnly usages", html.count("latestOnly={true}"))
    print("SchoolNotesPage", "function SchoolNotesPage" in html)
    print("function Root", "function Root()" in html)


if __name__ == "__main__":
    main()
