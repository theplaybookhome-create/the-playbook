#!/usr/bin/env python3
"""Apply V22 desktop + landing + empty-state fixes to app.html."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
text = ROOT.read_text(encoding="utf-8")
orig = text

subs = [
    ("<!-- THEME_BUILD_V21 -->", "<!-- THEME_BUILD_V22 -->"),
    (".quick-log-card { min-height: 280px; }", ".quick-log-card { min-height: 0; }"),
    (
        ".ql-sun { position: absolute; right: 8px; top: 8px; width: 168px; height: 128px; pointer-events: none; opacity: 0.95; }",
        ".ql-sun { position: absolute; right: 8px; top: 8px; width: 132px; height: 100px; pointer-events: none; opacity: 0.88; }",
    ),
    (
        '        <PaywallCard onUnlock={onUnlock} unlocked={unlocked} />',
        '        <PaywallCard compact onUnlock={onUnlock} unlocked={unlocked} />',
    ),
    (
        """      {pts.length < 2 ? (
        <p className=\"es-empty\">A sparkline appears after two energy logs.</p>
      ) : (""",
        """      {pts.length < 2 ? (
        <div>
          <div className=\"es-dots\" aria-hidden=\"true\"><i /><i /><i /><i /><i /></div>
          <p className=\"es-empty\">Tap energy on the left — a trend line shows after two logs.</p>
        </div>
      ) : (""",
    ),
    (
        """  if (CLOUD_ENABLED && !authReady) {
    return <div className=\"app-root\" style={{ padding: 40, textAlign: \"center\", color: \"var(--soft)\" }}>Starting THE PLAYBOOK…</div>;
  }
  if (CLOUD_ENABLED && (recoveryMode || (forceLogin && !session))) {""",
        """  if (CLOUD_ENABLED && (recoveryMode || (forceLogin && !session && authReady))) {""",
    ),
    (
        '{!loaded ? <div className=\"loading\">Loading your playbook…</div>',
        '{!loaded ? <div className=\"home-today\"><div className=\"home-greet\"><p className=\"hi\">THE PLAYBOOK</p><p className=\"sub\">Opening your tracker…</p></div></div>',
    ),
]

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
.paywall-card.compact .btn-amber { padding: 10px 14px; font-size: 14px; }
.owned-card.compact { padding: 10px 12px; align-items: center; }
.owned-card.compact p { display: none; }
.energy-spark { min-height: 0; }
.es-empty { margin: 8px 0 4px; font-size: 13px; color: #6B7280; line-height: 1.35; }
.es-dots { display: flex; gap: 6px; margin: 10px 0 8px; }
.es-dots i { width: 10px; height: 10px; border-radius: 50%; background: #E8ECF0; display: block; }
.app-main { min-height: auto; }
@media (max-width: 859px) {
  .header-chips { display: none !important; }
  .home-top { flex-direction: column !important; }
  .home-top .paywall-card,
  .home-top .owned-card { width: 100%; max-width: none; }
  .ql-sun { width: 110px; height: 84px; opacity: 0.7; }
}
@media (min-width: 860px) {
  .bottom-nav { display: none !important; }
  .app-root { padding-bottom: 28px !important; }
  .header-chips { display: flex !important; }
  .home-hero {
    grid-template-columns: minmax(0, 1.7fr) minmax(220px, 0.75fr) !important;
    align-items: start;
  }
  .ql-sun { width: 120px; height: 92px; }
}
"""

changed = []
for old, new in subs:
    if old in text:
        text = text.replace(old, new, 1)
        changed.append(old[:48])
    elif new in text:
        changed.append("already:" + old[:40])
    else:
        print("MISSING snippet:", old[:80].replace("\n", " / "))

if "THEME_BUILD_V22" in text and "V22 desktop + empty-state polish" not in text:
    if CSS_MARK in text:
        text = text.replace(CSS_MARK, CSS_MARK + "\n" + CSS_ADD, 1)
        changed.append("css-v22")
    else:
        print("MISSING css mark")

OLD_PW = """function PaywallCard({ onUnlock, unlocked }) {
  if (unlocked) {
    return (
      <div className=\"owned-card\">
        <div className=\"owned-crown\" aria-hidden=\"true\">\U0001f451</div>
        <div>
          <div className=\"stat-label\" style={{ textTransform: \"none\", letterSpacing: 0, fontSize: 14, color: \"#111827\" }}>Full access on this device</div>
          <p style={{ margin: \"4px 0 0\", fontSize: 12.5, color: \"var(--soft)\" }}>Insights, report, Discover, Printables & more unlocked.</p>
        </div>
        <span className=\"price-pill\">Owned</span>
      </div>
    );
  }
  return (
    <div className=\"paywall-card\">"""

NEW_PW = """function PaywallCard({ onUnlock, unlocked, compact }) {
  if (unlocked) {
    return (
      <div className={\"owned-card\" + (compact ? \" compact\" : \"\")}>
        <div className=\"owned-crown\" aria-hidden=\"true\">\U0001f451</div>
        <div>
          <div className=\"stat-label\" style={{ textTransform: \"none\", letterSpacing: 0, fontSize: 14, color: \"#111827\" }}>Full access on this device</div>
          {!compact && <p style={{ margin: \"4px 0 0\", fontSize: 12.5, color: \"var(--soft)\" }}>Insights, report, Discover, Printables & more unlocked.</p>}
        </div>
        <span className=\"price-pill\">Owned</span>
      </div>
    );
  }
  if (compact) {
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

if OLD_PW in text:
    text = text.replace(OLD_PW, NEW_PW, 1)
    changed.append("paywall-fn")
elif "function PaywallCard({ onUnlock, unlocked, compact })" in text:
    changed.append("already:paywall-fn")
else:
    print("MISSING PaywallCard function start")

if text != orig:
    ROOT.write_text(text, encoding="utf-8")
    print("patched", ROOT, "bytes", len(text.encode()), "ops", len(changed))
else:
    print("no-op", ROOT, "ops-noted", changed)

print("markers", {
    "V22": "THEME_BUILD_V22" in text,
    "compact": "PaywallCard compact" in text,
    "authReadyGate": "forceLogin && !session && authReady" in text,
    "css": "V22 desktop + empty-state polish" in text,
})
