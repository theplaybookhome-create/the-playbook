#!/usr/bin/env python3
from pathlib import Path
p = Path("app.html")
s = p.read_text(encoding="utf-8")

if "{showOnboard && !unlocked && (" not in s:
    if "{showOnboard && (" not in s:
        raise SystemExit("onboard gate not found")
    s = s.replace("{showOnboard && (", "{showOnboard && !unlocked && (", 1)

old_load = "      setShowOnboard(ob !== \"1\");\n      setUnlocked(pu === \"1\");"
new_load = (
    "      const alreadyPaid = pu === \"1\";\n"
    "      setShowOnboard(ob !== \"1\" && !alreadyPaid);\n"
    "      setUnlocked(alreadyPaid);\n"
    "      if (alreadyPaid) {\n"
    "        setShowOnboard(false);\n"
    "        try { await storageSet(\"onboard-seen\", \"1\"); } catch (e) {}\n"
    "      }"
)
if "const alreadyPaid" not in s:
    if old_load not in s:
        raise SystemExit("onboard load block not found")
    s = s.replace(old_load, new_load, 1)

old_prem = (
    "        if (userHasPremiumFlag(u)) {\n"
    "          await grantLocalPremium();\n"
    "          setUnlocked(true);\n"
    "          setShowPaywall(false);\n"
    "        }"
)
new_prem = (
    "        if (userHasPremiumFlag(u)) {\n"
    "          await grantLocalPremium();\n"
    "          setUnlocked(true);\n"
    "          setShowPaywall(false);\n"
    "          setShowOnboard(false);\n"
    "          try { localStorage.setItem(\"playbook:onboard-seen\", \"1\"); } catch (e) {}\n"
    "        }"
)
if old_prem in s:
    s = s.replace(old_prem, new_prem, 1)

if "function isClockSkewError" not in s:
    old_client = (
        "function getSupabase() {\n"
        "  if (!CLOUD_ENABLED || !window.supabase) return null;\n"
        "  if (!window.__pb_supabase) {\n"
        "    window.__pb_supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);\n"
        "  }\n"
        "  return window.__pb_supabase;\n"
        "}"
    )
    new_client = (
        "function isClockSkewError(err) {\n"
        "  const m = String((err && err.message) || err || \"\").toLowerCase();\n"
        "  return m.indexOf(\"jwt issued\") >= 0 || m.indexOf(\"issued at future\") >= 0 || m.indexOf(\"future date\") >= 0;\n"
        "}\n"
        "function getSupabase() {\n"
        "  if (!CLOUD_ENABLED || !window.supabase) return null;\n"
        "  if (!window.__pb_supabase) {\n"
        "    window.__pb_supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {\n"
        "      auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }\n"
        "    });\n"
        "  }\n"
        "  return window.__pb_supabase;\n"
        "}\n"
        "async function safeGetSession(sb) {\n"
        "  if (!sb) return { session: null };\n"
        "  try {\n"
        "    const { data, error } = await sb.auth.getSession();\n"
        "    if (error && isClockSkewError(error)) {\n"
        "      console.warn(\"clock skew on getSession\", error.message);\n"
        "      return { session: data && data.session ? data.session : null };\n"
        "    }\n"
        "    if (error) console.warn(\"getSession\", error);\n"
        "    return { session: data && data.session ? data.session : null };\n"
        "  } catch (e) {\n"
        "    console.warn(\"getSession error\", e);\n"
        "    return { session: null };\n"
        "  }\n"
        "}"
    )
    if old_client not in s:
        raise SystemExit("getSupabase block missing")
    s = s.replace(old_client, new_client, 1)

old_show = (
    "  const show = useCallback((message, type = \"default\") => {\n"
    "    if (timer.current) clearTimeout(timer.current);\n"
    "    setToast({ message, type });\n"
    "    timer.current = setTimeout(() => setToast(null), 2400);\n"
    "  }, []);"
)
new_show = (
    "  const show = useCallback((message, type = \"default\") => {\n"
    "    if (typeof isClockSkewError === \"function\" && isClockSkewError(message)) return;\n"
    "    if (timer.current) clearTimeout(timer.current);\n"
    "    setToast({ message, type });\n"
    "    timer.current = setTimeout(() => setToast(null), 2400);\n"
    "  }, []);"
)
if "isClockSkewError(message)" not in s and old_show in s:
    s = s.replace(old_show, new_show, 1)

s = s.replace(
    "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js",
    "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.49.8/dist/umd/supabase.min.js",
    1,
)

old_gs = (
    "    const sessionPromise = sb.auth.getSession().then(({ data }) => data).catch((e) => {\n"
    "      console.warn(\"getSession error\", e);\n"
    "      return { session: null };\n"
    "    });"
)
new_gs = (
    "    const sessionPromise = (typeof safeGetSession === \"function\" ? safeGetSession(sb) : sb.auth.getSession().then(({ data }) => data)).catch((e) => {\n"
    "      console.warn(\"getSession error\", e);\n"
    "      return { session: null };\n"
    "    });"
)
if "safeGetSession(sb)" not in s and old_gs in s:
    s = s.replace(old_gs, new_gs, 1)

p.write_text(s, encoding="utf-8")
print("patched", p.stat().st_size)
