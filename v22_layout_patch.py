#!/usr/bin/env python3
"""Apply V22 desktop + empty-state fixes using unique markers."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
text = ROOT.read_text(encoding="utf-8")
orig = text

def swap(old, new, label):
    global text
    if old in text:
        text = text.replace(old, new, 1)
        print("ok", label)
        return True
    if new in text or (label == "theme" and "THEME_BUILD_V22" in text):
        print("skip", label)
        return True
    print("MISSING", label)
    return False

swap("THEME_BUILD_V21", "THEME_BUILD_V22", "theme")
swap(".quick-log-card { min-height: 280px; }", ".quick-log-card { min-height: 0; }", "minheight")
swap("width: 168px; height: 128px; pointer-events: none; opacity: 0.95;", "width: 132px; height: 100px; pointer-events: none; opacity: 0.88;", "qlsun")
swap("A sparkline appears after two energy logs.", "Tap energy on the left - a trend line shows after two logs.", "spark")
swap("Starting THE PLAYBOOK", "Opening", "boot")
swap("Loading your playbook", "Opening your tracker", "load")
swap("<PaywallCard onUnlock={onUnlock} unlocked={unlocked} />", "<PaywallCard compact onUnlock={onUnlock} unlocked={unlocked} />", "compact-use")
swap("function PaywallCard({ onUnlock, unlocked }) {", "function PaywallCard({ onUnlock, unlocked, compact }) {", "pw-sig")
swap('      <div className="owned-card">', '      <div className={"owned-card" + (compact ? " compact" : "")}>', "owned-cls")
swap(
    "  if (CLOUD_ENABLED && !authReady) {",
    "  if (false && CLOUD_ENABLED && !authReady) {",
    "no-blank-boot",
)
swap(
    "if (CLOUD_ENABLED && (recoveryMode || (forceLogin && !session))) {",
    "if (CLOUD_ENABLED && (recoveryMode || (forceLogin && !session && authReady))) {",
    "auth-gate",
)

CSS_MARK = ".brand-mark-img { width:28px; height:28px; border-radius:8px; object-fit:cover; flex-shrink:0; box-shadow:0 4px 10px rgba(11,18,25,.28); }"
CSS_ADD = """
/* ===== V22 desktop + empty-state polish ===== */
.home-top {
  display: flex !important;
  flex-direction: row !important;
  align-items: flex-start !important;
  justify-content: space-between !important;
  gap: 16px !important;
  grid-template-columns: none !important;
  margin-bottom: 14px !important;
}
.home-greet { flex: 1 1 auto; min-width: 0; }
.home-top .paywall-card,
.home-top .owned-card {
  flex: 0 0 auto;
  width: min(300px, 38%);
  max-width: 300px;
  margin: 0 !important;
}
.paywall-card.compact { padding: 14px 16px !important; }
.paywall-card.compact h3 { font-size: 15px; margin: 0 0 4px; color: #111827; }
.paywall-card.compact p { margin: 0 0 10px; font-size: 12.5px; color: #6B7280; }
.paywall-card.compact .paywall-features { display: none; }
.owned-card.compact { padding: 10px 12px; align-items: center; }
.owned-card.compact p { display: none; }
.es-empty { margin: 8px 0 4px; font-size: 13px; color: #6B7280; line-height: 1.35; }
.app-main { min-height: auto; }
@media (max-width: 859px) {
  .header-chips { display: none !important; }
  .home-top { flex-direction: column !important; }
  .home-top .paywall-card,
  .home-top .owned-card { width: 100%; max-width: none; }
}
@media (min-width: 860px) {
  .bottom-nav { display: none !important; }
  .app-root { padding-bottom: 28px !important; }
  .header-chips { display: flex !important; }
  .home-hero {
    grid-template-columns: minmax(0, 1.7fr) minmax(220px, 0.75fr) !important;
    align-items: start;
  }
}
"""

if "V22 desktop + empty-state polish" not in text:
    if CSS_MARK in text:
        text = text.replace(CSS_MARK, CSS_MARK + "\n" + CSS_ADD, 1)
        print("ok css")
    else:
        print("MISSING css mark")
else:
    print("skip css")

NEEDLE = "  return (\n    <div className=\"paywall-card\">"
BRANCH = """  if (compact) {
    return (
      <div className=\"paywall-card compact\">
        <div style={{ display: \"flex\", justifyContent: \"space-between\", alignItems: \"flex-start\", marginBottom: 6 }}>
          <h3>Unlock full access</h3>
          <span className=\"price-pill\">{PREMIUM_PRICE}</span>
        </div>
        <p>Insights, report and printables. One payment, no subscription.</p>
        <button type=\"button\" className=\"btn-amber\" onClick={onUnlock}>Unlock \u00b7 {PREMIUM_PRICE}</button>
      </div>
    );
  }
  return (
    <div className=\"paywall-card\">"""
if "if (compact)" not in text and "<div className=\"paywall-card\">" in text:
    text = text.replace(NEEDLE, BRANCH, 1)
    print("ok compact-branch")
else:
    print("skip compact-branch")

if text != orig:
    ROOT.write_text(text, encoding="utf-8")
    print("patched", ROOT, "bytes", len(text.encode()))
else:
    print("no-op", ROOT)

print("markers", {
    "V22": "THEME_BUILD_V22" in text,
    "css": "V22 desktop + empty-state polish" in text,
    "auth": "forceLogin && !session && authReady" in text,
    "compact": "PaywallCard compact" in text,
})

idx = pathlib.Path("index.html")
if idx.exists():
    it = idx.read_text(encoding="utf-8")
    start = '        if (params.get("stay") === "1" || params.get("landing") === "1") return;'
    end = '        if (returning) window.location.replace("./app.html");'
    if start in it and end in it:
        pre, rest = it.split(start, 1)
        after = rest.split(end, 1)[1]
        it2 = pre + start + "\n        if ((window.location.hash || \"\") === \"#buy\") return;\n        /* Landing stays at / so phones see Open / Log in / Unlock. */\n" + after
        if it2 != it:
            idx.write_text(it2, encoding="utf-8")
            print("ok index-landing")
        else:
            print("skip index-same")
    else:
        print("skip index")
else:
    print("skip index-missing")
