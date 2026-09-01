#!/usr/bin/env python3
"""v51 — one meeting-summary hint on Report, bump cache."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

OLD_BLOCK = '''      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link in Teacher log on Today and says <code>school.html</code>.</p>
      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>
      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>
      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>
      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>'''

NEW_BLOCK = '''      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>Copies a read-only meeting summary (<code>share=</code>). The teacher form is a different link on the School tab (<code>school.html</code>).</p>'''


def main() -> None:
    html = APP.read_text(encoding="utf-8")
    if OLD_BLOCK in html:
        html = html.replace(OLD_BLOCK, NEW_BLOCK, 1)
    else:
        html = re.sub(
            r'(?:\s*<p className="no-print" style=\{\{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 \}\}>This button copies a <b>read-only meeting summary</b>\.[^<]*</p>)+',
            "\n" + NEW_BLOCK,
            html,
            count=1,
        )
    html = html.replace(
        "This is not the teacher daily form — that lives on Today.",
        "This is not the teacher daily form — that lives on the School tab.",
    )
    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=51")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V51 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")
    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v51"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")
    out = APP.read_text(encoding="utf-8")
    print("v51")
    print("hint count", out.count("This button copies a"))
    print("new hint", out.count("Copies a read-only meeting summary"))
    print("theme", "THEME_BUILD_V51" in out)


if __name__ == "__main__":
    main()
