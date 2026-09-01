#!/usr/bin/env python3
"""v43 — app boots again + login does not full-reload."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"


def strip_duplicate_school_helpers(html: str) -> str:
    """Keep the pretty V38 block; drop any earlier minified copy."""
    pretty = html.find("/* ===== V38: School link cloud")
    if pretty == -1:
        pretty = html.find("function schoolToken() {")
    first = html.find("function schoolToken(){")
    if first != -1 and pretty != -1 and first < pretty:
        html = html[:first] + html[pretty:]
    # If two pretty copies remain, keep the last
    marker = "/* ===== V38: School link cloud"
    if html.count(marker) > 1:
        last = html.rfind(marker)
        first = html.find(marker)
        if 0 <= first < last:
            html = html[:first] + html[last:]
    return html


def fix_login_no_reload(html: str) -> str:
    if "const [loginOpen, setLoginOpen]" not in html:
        html = html.replace(
            "  const [recoveryMode, setRecoveryMode] = useState(false);",
            "  const [recoveryMode, setRecoveryMode] = useState(false);\n"
            "  const [loginOpen, setLoginOpen] = useState(function () {\n"
            "    try {\n"
            "      const params = new URLSearchParams(window.location.search);\n"
            "      return params.get(\"login\") === \"1\" || params.get(\"mode\") === \"login\";\n"
            "    } catch (e) { return false; }\n"
            "  });",
            1,
        )

    old_btn = """              <button type=\"button\" className=\"header-btn header-pill\" onClick={() => {
                try {
                  const url = new URL(window.location.href);
                  url.searchParams.set(\"login\", \"1\");
                  window.history.replaceState({}, \"\", url.pathname + url.search + url.hash);
                } catch (e) {}
                window.location.search = (window.location.search ? window.location.search + \"&\" : \"?\") + \"login=1\";
              }}>Log in</button>"""
    new_btn = """              <button type=\"button\" className=\"header-btn header-pill\" onClick={() => setLoginOpen(true)}>Log in</button>"""
    if old_btn in html:
        html = html.replace(old_btn, new_btn, 1)

    html = html.replace(
        "  if (CLOUD_ENABLED && (recoveryMode || (forceLogin && !session && authReady))) {",
        "  if (CLOUD_ENABLED && (recoveryMode || ((forceLogin || loginOpen) && !session && authReady))) {",
        1,
    )

    if "setLoginOpen(false);" not in html:
        html = html.replace(
            "          setRecoveryMode(false);\n          try {\n            const url = new URL(window.location.href);\n            url.searchParams.delete(\"login\");",
            "          setRecoveryMode(false);\n          setLoginOpen(false);\n          try {\n            const url = new URL(window.location.href);\n            url.searchParams.delete(\"login\");",
            1,
        )
        html = html.replace(
            "          } catch (e) {}\n          setRecoveryMode(false);\n        }}",
            "          } catch (e) {}\n          setRecoveryMode(false);\n          setLoginOpen(false);\n        }}",
            1,
        )
    return html


def bump(html: str) -> str:
    html = re.sub(r'register\(\"\./sw\.js\?v=\d+\"\)', 'register(\"./sw.js?v=43\")', html, count=1)
    html = re.sub(r\"<!-- THEME_BUILD_V\d+ -->\", \"<!-- THEME_BUILD_V43 -->\", html, count=1)
    return html


def main() -> None:
    html = APP.read_text(encoding=\"utf-8\")
    html = strip_duplicate_school_helpers(html)
    html = fix_login_no_reload(html)
    html = bump(html)
    APP.write_text(html, encoding=\"utf-8\")

    if SW.exists():
        sw = SW.read_text(encoding=\"utf-8\")
        sw = re.sub(r'const CACHE(?:_NAME)? = \"playbook-v\d+\"', 'const CACHE = \"playbook-v43\"', sw, count=1)
        SW.write_text(sw, encoding=\"utf-8\")

    print(\"v43 boot fix applied\")
    print(\"bytes\", len(html))
    print(\"schoolToken\", html.count(\"function schoolToken\"))
    print(\"SchoolLinkCard\", html.count(\"function SchoolLinkCard\"))
    print(\"loginOpen\", \"setLoginOpen(true)\" in html)
    print(\"theme v43\", \"THEME_BUILD_V43\" in html)


if __name__ == \"__main__\":
    main()
