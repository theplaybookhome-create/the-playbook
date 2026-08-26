#!/usr/bin/env python3
"""Social tiles + cache-bust so the installed iPad PWA actually loads the theme."""
from pathlib import Path
import sys

p = Path(sys.argv[1] if len(sys.argv) > 1 else "app.html")
s = p.read_text(encoding="utf-8")

# Remove unstyled duplicate chips that overlap the login trust row
old_feat = '''        <div className="auth-features">
          <span>Private logs</span>
          <span>No subscription</span>
          <span>Track free first</span>
          <span>£2.99 unlock</span>
        </div>
        <div className="auth-trust">'''
if old_feat in s:
    s = s.replace(old_feat, "        <div className=\"auth-trust\">", 1)
    print("removed auth-features overlap")

# Circled platforms first: TikTok, Facebook, X — keep IG/WA after
for old_social, label in [
    ('''const SOCIAL_LINKS = [
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "instagram", label: "Instagram", href: "https://www.instagram.com/theplaybookhome/", hint: "Photos" },
  { id: "whatsapp", label: "WhatsApp", href: "https://wa.me/?text=" + encodeURIComponent("Hi — I found THE PLAYBOOK (theplaybook.cloud)"), hint: "Chat" }
];''', "v1"),
    ('''const SOCIAL_LINKS = [
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "x", label: "X", href: "https://x.com/theplaybookhome", hint: "Updates" }
];''', "v0"),
]:
    if old_social in s:
        s = s.replace(old_social, '''const SOCIAL_LINKS = [
  { id: "tiktok", label: "TikTok", href: "https://www.tiktok.com/@the.playbook311", hint: "Videos" },
  { id: "facebook", label: "Facebook", href: "https://www.facebook.com/groups/2217693205459716/", hint: "Group" },
  { id: "x", label: "X", href: "https://x.com/theplaybookhome", hint: "Updates" },
  { id: "instagram", label: "Instagram", href: "https://www.instagram.com/theplaybookhome/", hint: "Photos" },
  { id: "whatsapp", label: "WhatsApp", href: "https://wa.me/?text=" + encodeURIComponent("Hi — I found THE PLAYBOOK (theplaybook.cloud)"), hint: "Chat" }
];''', 1)
        print("social links", label)
        break
else:
    if 'id: "instagram"' in s:
        print("social already")
    else:
        raise SystemExit("SOCIAL_LINKS mismatch")

s = s.replace(
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx" };',
    'const cls = { facebook: "fb", tiktok: "tt", x: "xx", instagram: "ig", whatsapp: "wa" };',
    1,
)

if 'id === "instagram"' not in s:
    needle = '''  if (id === "x") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.9 1.15h3.67l-8.02 9.16L24 22.85h-7.4l-5.8-7.58-6.63 7.58H.49l8.58-9.8L0 1.15h7.59l5.24 6.93L18.9 1.15zm-1.29 19.53h2.03L6.53 3.24H4.35l13.26 17.44z"/></svg>
    );
  }
  return ('''
    insert = '''  if (id === "x") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.9 1.15h3.67l-8.02 9.16L24 22.85h-7.4l-5.8-7.58-6.63 7.58H.49l8.58-9.8L0 1.15h7.59l5.24 6.93L18.9 1.15zm-1.29 19.53h2.03L6.53 3.24H4.35l13.26 17.44z"/></svg>
    );
  }
  if (id === "instagram") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.2A4.8 4.8 0 1 0 16.8 12 4.8 4.8 0 0 0 12 7.2zm0 7.9A3.1 3.1 0 1 1 15.1 12 3.1 3.1 0 0 1 12 15.1z"/><circle cx="17.3" cy="6.7" r="1.15"/><path d="M12 2.2c-2.7 0-3 .01-4.1.06-2.7.12-4.1 1.5-4.2 4.2C3.21 9 3.2 9.3 3.2 12s.01 3 .06 4.1c.12 2.7 1.5 4.1 4.2 4.2 1.1.05 1.4.06 4.1.06s3-.01 4.1-.06c2.7-.12 4.1-1.5 4.2-4.2.05-1.1.06-1.4.06-4.1s-.01-3-.06-4.1c-.12-2.7-1.5-4.1-4.2-4.2-1.1-.05-1.4-.06-4.1-.06zm0 1.8c2.6 0 2.9.01 4 .06 1.9.09 2.9 1.05 3 3 .05 1.1.06 1.3.06 4s-.01 2.9-.06 4c-.09 1.9-1.06 2.9-3 3-1.1.05-1.3.06-4 .06s-2.9-.01-4-.06c-1.9-.09-2.9-1.06-3-3-.05-1.1-.06-1.3-.06-4s.01-2.9.06-4c.09-1.9 1.06-2.9 3-3 1.1-.05 1.4-.06 4-.06z"/></svg>
    );
  }
  if (id === "whatsapp") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2.1A9.9 9.9 0 0 0 2.1 12c0 1.74.46 3.44 1.33 4.94L2 22l5.2-1.36A9.9 9.9 0 0 0 12.04 22 9.9 9.9 0 0 0 22 12.04 9.9 9.9 0 0 0 12.04 2.1zm5.77 14.13c-.24.68-1.4 1.25-1.93 1.33-.5.07-1.12.1-1.81-.11-.42-.13-.95-.31-1.64-.6-2.89-1.25-4.77-4.16-4.92-4.35-.14-.2-1.18-1.57-1.18-3 0-1.42.75-2.12 1.01-2.41.26-.29.57-.36.76-.36h.55c.18 0 .41 0 .63.48.24.52.81 2 .88 2.14.07.14.12.31.02.5-.1.2-.14.31-.28.48-.14.16-.3.37-.42.5-.14.14-.29.29-.12.56.16.27.73 1.2 1.57 1.95 1.08.96 1.99 1.26 2.26 1.4.27.14.43.12.59-.07.16-.2.68-.79.86-1.06.18-.27.36-.22.61-.13.24.09 1.55.73 1.81.86.27.14.44.2.51.31.07.11.07.64-.17 1.32z"/></svg>
    );
  }
  return ('''
    if needle not in s:
        raise SystemExit("SocialIcon mismatch")
    s = s.replace(needle, insert, 1)
    print("social icons")
else:
    print("social icons already")

old_cb = '''.connect-btn .cb-ico { width:40px; height:40px; border-radius:12px; display:grid; place-items:center; flex:0 0 40px; }
.connect-btn .cb-ico svg { width:18px; height:18px; fill:#fff; }
.connect-btn.tt .cb-ico { background:#111; }
.connect-btn.xx .cb-ico { background:#0F1419; }
.connect-btn.fb .cb-ico { background:#1877F2; }
.connect-btn.em .cb-ico { background:#E8892C; }'''
new_cb = '''.connect-btn .cb-ico { width:42px; height:42px; border-radius:50%; display:grid; place-items:center; flex:0 0 42px; box-shadow:0 3px 8px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.28); }
.connect-btn .cb-ico svg { width:20px; height:20px; fill:#fff; }
.connect-btn.tt .cb-ico { background:#111; }
.connect-btn.xx .cb-ico { background:#0F1419; }
.connect-btn.fb .cb-ico { background:#1877F2; }
.connect-btn.ig .cb-ico { background:radial-gradient(circle at 30% 30%, #f9ce34, #ee2a7b 55%, #6228d7); }
.connect-btn.wa .cb-ico { background:#25D366; }
.connect-btn.em .cb-ico { background:#E8892C; }'''
if old_cb in s:
    s = s.replace(old_cb, new_cb, 1)
    print("social css")
elif "connect-btn.ig .cb-ico" in s:
    print("social css already")
else:
    print("WARN social css mismatch — continuing")

s = s.replace(
    ".connect-links { grid-template-columns: repeat(4, 1fr) !important; }",
    ".connect-links { grid-template-columns: repeat(3, 1fr) !important; }",
    1,
)

extra = """
.connect-btn .cb-ico { border-radius: 50% !important; box-shadow: 0 3px 8px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.28); }
.connect-btn.ig .cb-ico { background: radial-gradient(circle at 30% 30%, #f9ce34, #ee2a7b 55%, #6228d7) !important; }
.connect-btn.wa .cb-ico { background: #25D366 !important; }
"""
if "connect-btn.wa .cb-ico { background: #25D366 !important; }" not in s:
    s = s.replace("\n@media print {", extra + "\n@media print {", 1)

# Force installed PWAs to pick up the new theme
old_sw = '''    if ("serviceWorker" in navigator) {
      window.addEventListener("load", function () {
        navigator.serviceWorker.register("./sw.js").catch(function (e) {
          console.warn("SW register failed", e);
        });
      });
    }'''
new_sw = '''    if ("serviceWorker" in navigator) {
      window.addEventListener("load", function () {
        navigator.serviceWorker.register("./sw.js?v=15").then(function (reg) {
          if (reg && reg.update) try { reg.update(); } catch (e) {}
        }).catch(function (e) {
          console.warn("SW register failed", e);
        });
        navigator.serviceWorker.addEventListener("controllerchange", function () {
          if (window.__pbReloaded) return;
          window.__pbReloaded = true;
          window.location.reload();
        });
      });
    }'''
if old_sw in s:
    s = s.replace(old_sw, new_sw, 1)
    print("sw register v15")
elif "sw.js?v=15" in s:
    print("sw register already")
else:
    print("WARN sw register mismatch")

if "THEME_BUILD_V15" not in s:
    s = s.replace("<head>", "<head>\n  <!-- THEME_BUILD_V15 -->", 1)
    print("build stamp")

for must in ["instagram", "whatsapp", "connect-btn.ig", "THEME_BUILD_V15"]:
    if must not in s:
        raise SystemExit("missing " + must)

p.write_text(s, encoding="utf-8")
print("wrote", p, p.stat().st_size)
