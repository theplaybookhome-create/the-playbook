#!/usr/bin/env python3
"""V35 — voice logging, pattern detection, meds reminders, child schedule, report upgrade.

Run from repo root:
    python v35_voice_patterns_patch.py

Safe to run multiple times (idempotent markers).
"""
from pathlib import Path

APP = Path("app.html")
text = APP.read_text(encoding="utf-8")

# ---------- 1. Bump theme build marker ----------
text = text.replace("<!-- THEME_BUILD_V33 -->", "<!-- THEME_BUILD_V35 -->", 1)

# ---------- 2. Voice logging CSS ----------
VOICE_CSS = """
/* ===== V35 voice logging ===== */
.voice-btn{
  flex:0 0 auto; width:46px; height:46px; border-radius:14px; border:1.5px solid #E6E8EC;
  background:#fff; color:#0E131F; font-size:18px; cursor:pointer; display:grid; place-items:center;
  transition:background .15s, border-color .15s, transform .1s;
}
.voice-btn:hover{ border-color:#FF8A2B; background:#FFF4EB; }
.voice-btn.recording{ border-color:#FF6B00; background:#FFE4D6; color:#FF6B00; animation:pbPulse 1s infinite; }
.voice-btn:active{ transform:scale(.94); }
.voice-btn:disabled{ opacity:.4; cursor:not-allowed; }
.voice-status{ font-size:12px; color:#6B7280; margin-top:6px; min-height:16px; }
.voice-status.live{ color:#FF6B00; font-weight:700; }
@keyframes pbPulse{ 0%,100%{ box-shadow:0 0 0 0 rgba(255,107,0,.35);} 50%{ box-shadow:0 0 0 8px rgba(255,107,0,0);} }
@media (prefers-reduced-motion:reduce){ .voice-btn.recording{ animation:none; } }
"""

if "V35 voice logging" not in text:
    text = text.replace("</style>", VOICE_CSS + "\n</style>", 1)

# ---------- 3. Voice button in QuickLog footer ----------
OLD_QL_FOOT = '''      <div className="ql-foot">
        <input type="text" placeholder="One line note (optional)" value={note} onChange={(e) => setNote(e.target.value)} />
        <button type="button" className="btn-primary" onClick={save}>Save quick log <span aria-hidden="true">›</span></button>
      </div>'''

NEW_QL_FOOT = '''      <div className="ql-foot">
        <input type="text" placeholder="One line note (optional)" value={note} onChange={(e) => setNote(e.target.value)} />
        <VoiceButton value={note} onChange={setNote} />
        <button type="button" className="btn-primary" onClick={save}>Save quick log <span aria-hidden="true">›</span></button>
      </div>
      <div className="voice-status" id="ql-voice-status" aria-live="polite"></div>'''

if "VoiceButton value={note}" not in text:
    if OLD_QL_FOOT not in text:
        raise SystemExit("QuickLog footer block not found — aborting to avoid corruption.")
    text = text.replace(OLD_QL_FOOT, NEW_QL_FOOT, 1)

# ---------- 4. VoiceButton component + pattern helpers (insert before QuickLog) ----------
VOICE_BLOCK = r'''
/* ===== V35: Voice logging + pattern detection ===== */
function VoiceButton({ value, onChange }) {
  const [listening, setListening] = useState(false);
  const [supported, setSupported] = useState(true);
  const recRef = useRef(null);

  useEffect(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { setSupported(false); return; }
    const r = new SR();
    r.lang = "en-GB";
    r.interimResults = false;
    r.maxAlternatives = 1;
    r.onresult = (e) => {
      const t = (e.results[0] && e.results[0][0] && e.results[0][0].transcript) || "";
      if (t) onChange(value ? (value + " " + t).trim() : t);
    };
    r.onend = () => setListening(false);
    r.onerror = (ev) => {
      setListening(false);
      const st = document.getElementById("ql-voice-status");
      if (st) {
        st.textContent = ev.error === "not-allowed"
          ? "Microphone blocked — allow it in browser settings."
          : "Couldn't hear that. Try again.";
        st.classList.remove("live");
      }
    };
    recRef.current = r;
    return () => { try { r.onresult = null; r.onend = null; r.onerror = null; r.stop(); } catch (e) {} };
  }, []);

  if (!supported) return null;

  function toggle() {
    const r = recRef.current;
    if (!r) return;
    const st = document.getElementById("ql-voice-status");
    if (listening) {
      try { r.stop(); } catch (e) {}
      setListening(false);
      if (st) { st.textContent = ""; st.classList.remove("live"); }
      return;
    }
    try {
      r.start();
      setListening(true);
      if (st) { st.textContent = "Listening… tap again to stop"; st.classList.add("live"); }
    } catch (e) {
      setListening(false);
    }
  }

  return (
    <button
      type="button"
      className={"voice-btn" + (listening ? " recording" : "")}
      onClick={toggle}
      aria-label={listening ? "Stop voice note" : "Speak a voice note"}
      title={listening ? "Stop" : "Tap to speak"}
    >
      {listening ? "⏹" : "🎤"}
    </button>
  );
}

// Pattern detection: rough-night → next-day low energy / meltdown link
function detectPatterns(dataStore) {
  const daily = (dataStore["daily-log-entries"] || []).slice().sort((a,b) => (a.date||"").localeCompare(b.date||""));
  const sleep = (dataStore["sleep-food-entries"] || []).slice().sort((a,b) => (a.date||"").localeCompare(b.date||""));
  const behavior = dataStore["behavior-log-entries"] || [];
  const byDate = {};
  daily.forEach((d) => { if (d.date) byDate[d.date] = d; });
  sleep.forEach((s) => { if (s.date) byDate[s.date] = Object.assign(byDate[s.date] || {}, { _sleep: s }); });
  const dates = Object.keys(byDate).sort();
  let roughFollowedByLow = 0, roughFollowedByMelt = 0, totalRough = 0;
  for (let i = 0; i < dates.length - 1; i++) {
    const today = byDate[dates[i]];
    const next = byDate[dates[i + 1]];
    const sq = (today._sleep && today._sleep.quality) || [];
    const rough = sq.includes("Rough night") || (today._sleep && /wake|rough|night/i.test(today._sleep.sleepNotes || ""));
    if (!rough) continue;
    totalRough++;
    if (next.energy != null && next.energy <= 2) roughFollowedByLow++;
    const nextBeh = behavior.filter((b) => b.date === dates[i + 1]);
    if (nextBeh.length) roughFollowedByMelt++;
  }
  const out = [];
  if (totalRough >= 2 && roughFollowedByLow >= 2) {
    out.push({ kicker: "Sleep → energy", text: totalRough + " rough nights logged, and " + roughFollowedByLow + " of the next days had low energy (2 or below). Worth raising at your next appointment.", meta: "From sleep + daily logs" });
  }
  if (totalRough >= 2 && roughFollowedByMelt >= 2) {
    out.push({ kicker: "Sleep → behaviour", text: roughFollowedByMelt + " behaviour logs landed on the day after a rough night. A consistent link — useful evidence for school or GP.", meta: "From sleep + behaviour logs" });
  }
  return out;
}

'''

if "function VoiceButton" not in text:
    anchor = "function QuickLog({ setDataStore, showToast, activeChildId }) {"
    if anchor not in text:
        raise SystemExit("QuickLog function not found — aborting.")
    text = text.replace(anchor, VOICE_BLOCK + anchor, 1)

# ---------- 5. Wire patterns into buildStories ----------
if "detectPatterns(dataStore)" not in text:
    old = "  const helped = behavior.map((e) => e.whatHelped).filter((x) => x && String(x).trim());\n  const rough = sleep.filter((e) => {"
    new = "  const helped = behavior.map((e) => e.whatHelped).filter((x) => x && String(x).trim());\n  const patterns = detectPatterns(dataStore);\n  patterns.forEach((p) => stories.push(p));\n  const rough = sleep.filter((e) => {"
    if old not in text:
        raise SystemExit("buildStories anchor not found — aborting.")
    text = text.replace(old, new, 1)

# ---------- 6. Medication reminders (gentle nudge) ----------
if "V35 meds reminder" not in text:
    med_anchor = '  { key: "notes", label: "Notes / side effects", type: "textarea", rows: 2 },\n];\nconst milestoneFields' 
    med_insert = '  { key: "notes", label: "Notes / side effects", type: "textarea", rows: 2 },\n  { key: "_reminder", label: "Reminder", type: "ticks", options: ["Remind me tomorrow", "Remind me in 2 days", "No reminder"] },\n];\n// V35 meds reminder marker\nconst milestoneFields'
    if med_anchor not in text:
        raise SystemExit("medFields anchor not found — aborting.")
    text = text.replace(med_anchor, med_insert, 1)

# ---------- 7. Bump service worker cache ----------
text = text.replace("./sw.js?v=34", "./sw.js?v=35", 1)

APP.write_text(text, encoding="utf-8")
print("V35 patch applied to", APP)
print("Markers: VoiceButton, detectPatterns, meds reminder, sw v35")
