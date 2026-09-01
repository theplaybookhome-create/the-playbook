#!/usr/bin/env python3
"""v44 — teacher form copy feedback, Teacher log section, report cleanup."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"


def main() -> None:
    html = APP.read_text(encoding="utf-8")

    old_css = ".school-card{ background:#fff; border:1.5px solid #E2E8F0; border-radius:18px; padding:16px; margin-bottom:14px; }"
    new_css = (
        ".school-section{ background:#fff; border:1.5px solid #E2E8F0; border-radius:20px; padding:16px 16px 8px; margin:0 0 16px; }\n"
        ".school-section-head{ margin-bottom:12px; }\n"
        ".school-section-head h2{ margin:0 0 4px; font-size:18px; color:#0E131F; }\n"
        ".school-section-head p{ margin:0; font-size:13px; color:#6B7280; line-height:1.45; }\n"
        ".school-section .school-card{ border:1.5px solid #E2E8F0; box-shadow:none; }\n"
        ".school-copied.ok{ background:#ECFDF5; border:1px solid #A7F3D0; color:#065F46; }\n"
        ".btn-navy-copy{ background:var(--navy) !important; color:#fff !important; border:none !important; }\n"
        + old_css
    )
    if old_css in html and ".school-section{" not in html:
        html = html.replace(old_css, new_css, 1)

    dup = (
        '      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>\n'
        '      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>\n'
    )
    one = (
        '      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link in Teacher log on Today and says <code>school.html</code>.</p>\n'
    )
    if dup in html:
        html = html.replace(dup, one, 1)
    elif html.count("This button copies a") > 1:
        html = html.replace(
            '      <p className="no-print" style={{ fontSize: 13, color: "#6B7280", margin: "0 0 10px", lineHeight: 1.45 }}>This button copies a <b>read-only meeting summary</b>. It will contain <code>share=</code>. The teacher daily form is a different link on the Today tab and says <code>school.html</code>.</p>\n',
            one,
            1,
        )

    old_btn = """        <button type="button" className="btn-secondary" onClick={async () => {
          try {
            const payload = buildSharePayload(dataStore, profileSafe, range);
            const url = window.location.origin + window.location.pathname + "?share=" + encodeSharePayload(payload);
            if (navigator.clipboard && navigator.clipboard.writeText) await navigator.clipboard.writeText(url);
            const st = document.getElementById("share-status");
            if (st) st.textContent = "Copied a view-only meeting summary. This is NOT the teacher form (that one says school.html).";
          } catch (e) {
            const st = document.getElementById("share-status");
            if (st) st.textContent = "Could not copy. Long-press and copy the address bar after tapping Share again.";
          }
        }}>Copy meeting-summary link</button>"""
    new_btn = """        <button type="button" className="btn-primary btn-navy-copy" onClick={async () => {
          try {
            const payload = buildSharePayload(dataStore, profileSafe, range);
            const url = window.location.origin + window.location.pathname + "?share=" + encodeSharePayload(payload);
            const ok = await copyTextFallback(url);
            const st = document.getElementById("share-status");
            if (st) st.textContent = ok ? "Copied successfully — this is a view-only meeting summary, not the teacher form." : "Could not auto-copy. Long-press the status line if a link appears, or try again.";
            if (ok && showToast) showToast("Copied successfully", "success");
          } catch (e) {
            const st = document.getElementById("share-status");
            if (st) st.textContent = "Could not copy. Long-press and copy the address bar after tapping again.";
          }
        }}>Copy meeting-summary link</button>"""
    if old_btn in html:
        html = html.replace(old_btn, new_btn, 1)

    old_home = "      <SchoolLinkCard showToast={showToast} />\n      <SchoolInbox showToast={showToast} />\n"
    new_home = (
        '      <section className="school-section" aria-labelledby="teacher-log-heading">\n'
        '        <div className="school-section-head">\n'
        '          <h2 id="teacher-log-heading">Teacher log</h2>\n'
        "          <p>Keep school notes in one place. Teachers only get a short form — they never see your diary.</p>\n"
        "        </div>\n"
        "        <SchoolLinkCard showToast={showToast} />\n"
        "        <SchoolInbox showToast={showToast} />\n"
        "      </section>\n"
    )
    if old_home in html and "id=\"teacher-log-heading\"" not in html:
        html = html.replace(old_home, new_home, 1)

    if "async function copyTextFallback(text)" not in html:
        html = html.replace(
            "function schoolToken() {",
            """async function copyTextFallback(text) {
  if (!text) return false;
  try {
    if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch (e) {}
  try {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "0";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    ta.setSelectionRange(0, text.length);
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);
    return !!ok;
  } catch (e) {
    return false;
  }
}
function schoolToken() {""",
            1,
        )

    old_copyurl = """  async function copyUrl(url) {
    let ok = false;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(url);
        ok = true;
      }
    } catch (e) {}
    setCopied(url);
    setCopyState(ok ? "copied" : "manual");
    return ok;
  }"""
    new_copyurl = """  async function copyUrl(url) {
    const ok = await copyTextFallback(url);
    setCopied(url);
    setCopyState(ok ? "copied" : "manual");
    if (ok && showToast) showToast("Copied successfully", "success");
    else if (!ok && showToast) showToast("Link ready — copy it from the green box");
    return ok;
  }"""
    if old_copyurl in html:
        html = html.replace(old_copyurl, new_copyurl, 1)

    old_make = """  async function makeLink() {
    const token = schoolToken();
    const entry = { token: token, created: todayISO(), label: "Teacher form " + (links.length + 1) };
    const published = await publishSchoolLink(entry);
    if (!published.ok) {
      setSetupHint("Link is ready, but teacher send may fail until cloud tables exist.");
    } else {
      setSetupHint("");
    }
    const next = [entry, ...links].slice(0, 20);
    setLinks(next);
    saveSchoolLinks(next);
    const url = schoolLinkFor(token);
    const ok = await copyUrl(url);
    if (showToast) showToast(ok ? "Teacher form link copied" : "Link created — copy it from the green box");
  }

  async function copyExisting(token) {
    const url = schoolLinkFor(token);
    const ok = await copyUrl(url);
    if (showToast) showToast(ok ? "Teacher link copied" : "Copy the link from the green box");
  }"""
    new_make = """  async function makeLink() {
    const token = schoolToken();
    const entry = { token: token, created: todayISO(), label: "Teacher form " + (links.length + 1) };
    const next = [entry, ...links].slice(0, 20);
    setLinks(next);
    saveSchoolLinks(next);
    const url = schoolLinkFor(token);
    await copyUrl(url);
    try {
      const published = await Promise.race([
        publishSchoolLink(entry),
        new Promise(function (resolve) { setTimeout(function () { resolve({ ok: false, reason: "timeout" }); }, 5000); })
      ]);
      if (!published || !published.ok) {
        setSetupHint("Link is copied. If the teacher cannot send, cloud tables may still need setup.");
      } else {
        setSetupHint("");
      }
    } catch (e) {
      setSetupHint("Link is copied. Teacher send needs an internet connection.");
    }
  }

  async function copyExisting(token) {
    const url = schoolLinkFor(token);
    await copyUrl(url);
  }"""
    if old_make in html:
        html = html.replace(old_make, new_make, 1)

    html = html.replace(
        '<strong>{copyState === "copied" ? "Copied to clipboard" : "Link created — copy it below"}</strong>',
        '<strong>{copyState === "copied" ? "Copied successfully" : "Link created — copy it below"}</strong>',
        1,
    )
    html = html.replace(
        '<button type="button" className="btn-primary" style={{ width: "100%" }} onClick={makeLink}>Create teacher form link</button>',
        '<button type="button" className="btn-primary" style={{ width: "100%" }} onClick={makeLink}>{copyState === "copied" ? "Copied successfully — create another" : "Create teacher form link"}</button>',
        1,
    )
    html = html.replace(
        '<h3 style={{ fontSize: 15, margin: "0 0 8px" }}>Notes from teacher</h3>',
        '<h3 style={{ fontSize: 15, margin: "8px 0 8px" }}>Incoming teacher notes</h3>',
        1,
    )
    html = html.replace(
        'navigator.serviceWorker.register("./sw.js?v=43")',
        'navigator.serviceWorker.register("./sw.js?v=44")',
        1,
    )

    APP.write_text(html, encoding="utf-8")
    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = sw.replace("playbook-v43", "playbook-v44")
        SW.write_text(sw, encoding="utf-8")
    print("v44 applied")


if __name__ == "__main__":
    main()
