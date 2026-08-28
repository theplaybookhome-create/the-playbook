#!/usr/bin/env python3
"""V34 launch: privacy links, delete-my-data, theme-color, SW v34."""
from pathlib import Path

APP = Path("app.html")
t = APP.read_text(encoding="utf-8")
orig = t

t = t.replace('content="#F4F6F8"', 'content="#0B1219"', 1)
t = t.replace('apple-mobile-web-app-status-bar-style" content="default"',
              'apple-mobile-web-app-status-bar-style" content="black-translucent"')
t = t.replace('<style>body { margin: 0; background: #F7F6F4; }</style>',
              '<style>body { margin: 0; background: #0B1219; }</style>')
t = t.replace('./sw.js?v=33', './sw.js?v=34')

old_sig = "function HomePage({ dataStore, setDataStore, onNavigate, unlocked, onUnlock, onOpenPaywall, showToast, activeChildId, activeChildName, firstName }) {"
new_sig = "function HomePage({ dataStore, setDataStore, onNavigate, unlocked, onUnlock, onOpenPaywall, showToast, activeChildId, activeChildName, firstName, onWipeDevice }) {"
if old_sig in t:
    t = t.replace(old_sig, new_sig, 1)

card = '''        {!unlocked && (
          <button type="button" className="btn-ghost" style={{ marginTop: 8 }} onClick={onOpenPaywall}>See what's included →</button>
        )}
        </div>
        <div className="why-card" style={{ marginTop: 12 }}>
          <div className="stat-label why-label">Your data</div>
          <p style={{ margin: "8px 0 10px", fontSize: 13, lineHeight: 1.5, color: "var(--soft)" }}>
            Logs stay on this device. Export a backup anytime. Delete clears notes on this phone or tablet — it does not cancel a Stripe payment.
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            <a href="./privacy.html" style={{ fontSize: 13, fontWeight: 700, color: "var(--amber-deep)" }}>Privacy</a>
            <span style={{ color: "var(--line)" }}>·</span>
            <a href="./terms.html" style={{ fontSize: 13, fontWeight: 700, color: "var(--amber-deep)" }}>Terms</a>
            <span style={{ color: "var(--line)" }}>·</span>
            <button type="button" className="btn-ghost" style={{ margin: 0, padding: "6px 10px", fontSize: 12 }} onClick={onWipeDevice}>Delete my data</button>
          </div>
        </div>
'''
old_card_end = '''        {!unlocked && (
          <button type="button" className="btn-ghost" style={{ marginTop: 8 }} onClick={onOpenPaywall}>See what's included →</button>
        )}
        </div>
'''
if "Delete my data" not in t and old_card_end in t:
    t = t.replace(old_card_end, card, 1)

old_home = '<HomePage setDataStore={setDataStore} showToast={showToast} dataStore={dataStore} onNavigate={navigate} unlocked={unlocked} onUnlock={handleUnlock} onOpenPaywall={requestUnlock} activeChildId={activeChildId} activeChildName={(children.find((c) => c.id === activeChildId) || {}).name} firstName={firstNameOf(user)} />'
new_home = old_home.replace("firstName={firstNameOf(user)} />", "firstName={firstNameOf(user)} onWipeDevice={() => setPendingWipe(true)} />")
if "onWipeDevice={() => setPendingWipe(true)}" not in t and old_home in t:
    t = t.replace(old_home, new_home, 1)

if "const [pendingWipe, setPendingWipe] = useState(false);" not in t:
    t = t.replace(
        "  const [recoveryMode, setRecoveryMode] = useState(false);\n  const fileInputRef = useRef(null);",
        "  const [recoveryMode, setRecoveryMode] = useState(false);\n  const [pendingWipe, setPendingWipe] = useState(false);\n  const fileInputRef = useRef(null);",
        1,
    )

wipe_fn = '''
  async function handleWipeDevice() {
    try {
      const keepUnlock = localStorage.getItem("playbook:premium-unlocked");
      const doomed = [];
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (k && k.indexOf("playbook:") === 0) doomed.push(k);
      }
      doomed.forEach((k) => localStorage.removeItem(k));
      if (keepUnlock === "1") {
        try { localStorage.setItem("playbook:premium-unlocked", "1"); } catch (e) {}
      }
      showToast("Device logs deleted", "success");
    } catch (e) {
      console.error(e);
      showToast("Could not delete everything — clear site data in the browser", "error");
    }
    setPendingWipe(false);
    window.setTimeout(() => window.location.reload(), 400);
  }

'''
if "async function handleWipeDevice()" not in t:
    needle = "    if (fileInputRef.current) fileInputRef.current.value = \"\";\n  }\n\n  const bottom = ["
    if needle in t:
        t = t.replace(needle, "    if (fileInputRef.current) fileInputRef.current.value = \"\";\n  }\n" + wipe_fn + "  const bottom = [", 1)

modal = '''
      {pendingWipe && (
        <ConfirmModal
          title="Delete data on this device?"
          message="This removes logs, child nicknames and notes stored in this browser. Your £2.99 unlock on this device is kept. Community posts on your account stay until you email us. This cannot be undone."
          onConfirm={handleWipeDevice}
          onCancel={() => setPendingWipe(false)}
        />
      )}
'''
close = '''            <button type="button" className="btn-secondary" style={{ width: "100%", marginTop: 10 }} onClick={() => setShowChildModal(false)}>Done</button>
          </div>
        </div>
      )}
    </div>
  );
}
'''
if "pendingWipe &&" not in t and close in t:
    t = t.replace(close, close.replace("    </div>\n  );\n}\n", modal + "    </div>\n  );\n}\n"), 1)

if t == orig:
    print("V34: no changes (already applied?)")
else:
    APP.write_text(t, encoding="utf-8")
    print("V34: patched app.html", len(orig), "->", len(t))
