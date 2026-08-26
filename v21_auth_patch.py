#!/usr/bin/env python3
"""Allow the app to open without a cloud session; login is opt-in."""
from pathlib import Path
import sys

p = Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
s = p.read_text(encoding="utf-8")

for old, new in [
    ("<!-- THEME_BUILD_V19 -->", "<!-- THEME_BUILD_V21 -->"),
    ("<!-- THEME_BUILD_V20 -->", "<!-- THEME_BUILD_V21 -->"),
    ("./sw.js?v=18", "./sw.js?v=21"),
    ("./sw.js?v=19", "./sw.js?v=21"),
    ("./sw.js?v=20", "./sw.js?v=21"),
]:
    s = s.replace(old, new)

old_gate = """  if (CLOUD_ENABLED && authReady && (!session || recoveryMode)) {
    return <AuthScreen recoveryMode={recoveryMode} onAuthed={(s) => { setSession(s); setRecoveryMode(false); }} />;
  }
  if (CLOUD_ENABLED && !authReady) {
    return <div className=\"app-root\" style={{ padding: 40, textAlign: \"center\", color: \"var(--soft)\" }}>Starting secure session…</div>;
  }"""

new_gate = """  const forceLogin = (function () {
    try {
      const params = new URLSearchParams(window.location.search);
      return params.get(\"login\") === \"1\" || params.get(\"mode\") === \"login\";
    } catch (e) { return false; }
  })();
  if (CLOUD_ENABLED && !authReady) {
    return <div className=\"app-root\" style={{ padding: 40, textAlign: \"center\", color: \"var(--soft)\" }}>Starting THE PLAYBOOK…</div>;
  }
  if (CLOUD_ENABLED && (recoveryMode || (forceLogin && !session))) {
    return (
      <AuthScreen
        recoveryMode={recoveryMode}
        onAuthed={(sess) => {
          setSession(sess);
          setRecoveryMode(false);
          try {
            const url = new URL(window.location.href);
            url.searchParams.delete(\"login\");
            url.searchParams.delete(\"mode\");
            window.history.replaceState({}, \"\", url.pathname + url.search + url.hash);
          } catch (e) {}
        }}
        onSkip={() => {
          try {
            const url = new URL(window.location.href);
            url.searchParams.delete(\"login\");
            url.searchParams.delete(\"mode\");
            window.history.replaceState({}, \"\", url.pathname + url.search + url.hash);
          } catch (e) {}
          setRecoveryMode(false);
        }}
      />
    );
  }"""

if old_gate not in s:
    if "forceLogin" in s:
        print("auth gate already patched")
    else:
        raise SystemExit("auth gate block not found")
else:
    s = s.replace(old_gate, new_gate, 1)
    print("auth gate -> optional login")

s = s.replace(
    "function AuthScreen({ onAuthed, recoveryMode }) {",
    "function AuthScreen({ onAuthed, onSkip, recoveryMode }) {",
    1,
)

old_footer = """        <p className=\"auth-footer\">Need help? <a href=\"mailto:Theplaybookhome@gmail.com\">Theplaybookhome@gmail.com</a></p>
      </div>
    </div>
  );
}"""
new_footer = """        {onSkip && !recoveryMode ? (
          <p className=\"auth-footer\">
            <button type=\"button\" onClick={onSkip} style={{ background: \"none\", border: \"none\", color: \"#E8A317\", fontWeight: 700, cursor: \"pointer\", fontSize: 13, fontFamily: \"inherit\", padding: 0 }}>Continue on this device without logging in</button>
          </p>
        ) : null}
        <p className=\"auth-footer\">Need help? <a href=\"mailto:Theplaybookhome@gmail.com\">Theplaybookhome@gmail.com</a></p>
      </div>
    </div>
  );
}"""
if "Continue on this device without logging in" not in s:
    if old_footer not in s:
        raise SystemExit("auth footer not found")
    s = s.replace(old_footer, new_footer, 1)
    print("auth skip added")

old_actions = """            {CLOUD_ENABLED && user ? <button type=\"button\" className=\"header-btn header-pill signout-quiet\" onClick={handleSignOut}>Sign out</button> : null}"""
new_actions = """            {CLOUD_ENABLED && user ? <button type=\"button\" className=\"header-btn header-pill signout-quiet\" onClick={handleSignOut}>Sign out</button> : (
              <a className=\"header-btn header-pill\" href=\"./app.html?login=1\">Log in</a>
            )}"""
if old_actions in s:
    s = s.replace(old_actions, new_actions, 1)
    print("header login link added")
elif 'href="./app.html?login=1"' in s:
    print("header login already present")
else:
    print("WARN header login not patched")

if "THEME_BUILD_V21" not in s:
    s = s.replace("<head>", "<head>\n  <!-- THEME_BUILD_V21 -->", 1)

p.write_text(s, encoding="utf-8")
print("wrote", p, p.stat().st_size)
