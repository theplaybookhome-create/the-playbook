#!/usr/bin/env python3
"""v50 — fix blank-screen boot crash from 'async async function'."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"


def main() -> None:
    html = APP.read_text(encoding="utf-8")
    before = html
    html = html.replace("async async function", "async function")
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V50 -->", html, count=1)
    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=50")', html, count=1)
    if html != before:
        APP.write_text(html, encoding="utf-8")

    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw2 = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v50"', sw, count=1)
        if sw2 != sw:
            SW.write_text(sw2, encoding="utf-8")

    html = APP.read_text(encoding="utf-8")
    print("v50")
    print("async async", html.count("async async"))
    print("THEME", "THEME_BUILD_V50" in html)
    print("sw register", 'register("./sw.js?v=50")' in html)
    print("fetchSchoolNotes", "async function fetchSchoolNotesForTokens" in html)
    if "async async" in html:
        raise SystemExit("still has async async")


if __name__ == "__main__":
    main()
