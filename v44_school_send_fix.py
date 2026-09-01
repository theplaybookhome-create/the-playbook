#!/usr/bin/env python3
"""v44 - parent publishes teacher tokens with the anon key so send works."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.html"
SW = ROOT / "sw.js"

OLD_PUBLISH = """async function publishSchoolLink(entry) {
  const sb = getSupabase();
  if (!sb) return { ok: false, reason: "no-cloud" };
  const { error } = await sb.from("playbook_share_links").upsert({
    token: entry.token,
    label: entry.label,
    child_label: entry.child || null,
    active: true
  });
  if (error) return { ok: false, reason: error.message or "cloud" };
  return { ok: true };
}
async function revokeSchoolLinkCloud(token) {
  const sb = getSupabase();
  if (!sb) return;
  await sb.from("playbook_share_links").update({ active: false }).eq("token", token);
}""".replace("error.message or", "error.message ||")

NEW_PUBLISH = (
"async function schoolRestHeaders() {\n"
"  return {\n"
"    apikey: SUPABASE_ANON_KEY,\n"
"    Authorization: \"Bearer \" + SUPABASE_ANON_KEY,\n"
"    \"Content-Type\": \"application/json\"\n"
"  };\n"
"}\n"
"async function publishSchoolLink(entry) {\n"
"  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) return { ok: false, reason: \"no-cloud\" };\n"
"  try {\n"
"    const res = await fetch(SUPABASE_URL + \"/rest/v1/playbook_share_links\", {\n"
"      method: \"POST\",\n"
"      headers: Object.assign(await schoolRestHeaders(), { Prefer: \"resolution=merge-duplicates,return=minimal\" }),\n"
"      body: JSON.stringify({\n"
"        token: entry.token,\n"
"        label: entry.label,\n"
"        child_label: entry.child || null,\n"
"        active: true\n"
"      })\n"
"    });\n"
"    if (!res.ok && res.status !== 409) {\n"
"      const txt = await res.text();\n"
"      return { ok: false, reason: txt || String(res.status) };\n"
"    }\n"
"    return { ok: true };\n"
"  } catch (e) {\n"
"    return { ok: false, reason: (e && e.message) || \"network\" };\n"
"  }\n"
"}\n"
"async function revokeSchoolLinkCloud(token) {\n"
"  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) return;\n"
"  try {\n"
"    await fetch(SUPABASE_URL + \"/rest/v1/playbook_share_links?token=eq.\" + encodeURIComponent(token), {\n"
"      method: \"PATCH\",\n"
"      headers: Object.assign(await schoolRestHeaders(), { Prefer: \"return=minimal\" }),\n"
"      body: JSON.stringify({ active: false })\n"
"    });\n"
"  } catch (e) {}\n"
"}"
)

def main() -> None:
    html = APP.read_text(encoding="utf-8")
    if OLD_PUBLISH in html:
        html = html.replace(OLD_PUBLISH, NEW_PUBLISH, 1)
    elif "resolution=merge-duplicates" not in html:
        html = html.replace(
            "async function publishSchoolLink(entry) {",
            NEW_PUBLISH + "\nasync function publishSchoolLink_UNUSED(entry) {",
            1,
        )
    html = html.replace(
        'setSetupHint("Link is ready, but teacher send may fail until cloud tables exist.");',
        'setSetupHint("Copied locally, but the teacher form is not live yet. Stay online and tap Create teacher form link again.");',
    )
    html = re.sub(r'register\("\./sw\.js\?v=\d+"\)', 'register("./sw.js?v=44")', html, count=1)
    html = re.sub(r"<!-- THEME_BUILD_V\d+ -->", "<!-- THEME_BUILD_V44 -->", html, count=1)
    APP.write_text(html, encoding="utf-8")
    if SW.exists():
        sw = SW.read_text(encoding="utf-8")
        sw = re.sub(r'const CACHE(?:_NAME)? = "playbook-v\d+"', 'const CACHE = "playbook-v44"', sw, count=1)
        SW.write_text(sw, encoding="utf-8")
    print("v44 send fix", "merge-duplicates" in html)

if __name__ == "__main__":
    main()
