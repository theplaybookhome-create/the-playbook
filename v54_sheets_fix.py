#!/usr/bin/env python3
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent
app = ROOT / "app.html"
text = app.read_text(encoding="utf-8")
text = text.replace("<!-- THEME_BUILD_V51 -->", "<!-- THEME_BUILD_V54 -->")
text = text.replace("<!-- THEME_BUILD_V52 -->", "<!-- THEME_BUILD_V54 -->")
text = text.replace("<!-- THEME_BUILD_V53 -->", "<!-- THEME_BUILD_V54 -->")
text = text.replace("sw.js?v=51", "sw.js?v=54")
text = text.replace("sw.js?v=52", "sw.js?v=54")
text = text.replace("sw.js?v=53", "sw.js?v=54")
if 'src="./sheets.js"' not in text:
    text = text.replace(
        '<script type="text/babel" data-presets="react">',
        '<script src="./sheets.js"></script>\n  <script type="text/babel" data-presets="react">',
        1,
    )
    print("added sheets.js script")
text2, n = re.subn(
    r'if \("serviceWorker" in navigator\) \{.*?\n    \}',
    '''if ("serviceWorker" in navigator) {
      navigator.serviceWorker.getRegistrations().then(function (regs) {
        regs.forEach(function (r) { r.unregister(); });
      }).catch(function () {});
    }''',
    text,
    count=1,
    flags=re.S,
)
if n:
    text = text2
    print("SW register replaced with unregister")
old_gal_start = "function PrintablesGallery({ unlocked, onRequestUnlock, embedded }) {"
old_page = "function PrintablesPage({ unlocked, onRequestUnlock }) {"
if old_gal_start in text and old_page in text:
    i = text.find(old_gal_start)
    j = text.find(old_page)
    new_gal = '''function PrintablesGallery({ unlocked, onRequestUnlock, embedded }) {
  const sheets = (typeof PRINTABLE_SHEETS !== "undefined" && PRINTABLE_SHEETS) ? PRINTABLE_SHEETS : [];
  const [note, setNote] = useState("");
  async function saveSheet(sheet) {
    if (!unlocked) { onRequestUnlock(); return; }
    setNote("Preparing " + sheet.title + "…");
    try {
      const res = await fetch(sheet.src, { credentials: "same-origin" });
      if (!res.ok) throw new Error("missing");
      const blob = await res.blob();
      const name = (sheet.src.split("/").pop() || "playbook-sheet.jpg");
      if (navigator.share && navigator.canShare) {
        const f = new File([blob], name, { type: blob.type || "image/jpeg" });
        if (navigator.canShare({ files: [f] })) {
          await navigator.share({ files: [f], title: sheet.title, text: "Save to Files or Print" });
          setNote("Share sheet opened — tap Save to Files.");
          return;
        }
      }
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = name;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setNote("Saved. Check Files or Downloads.");
    } catch (e) {
      if (e && e.name === "AbortError") { setNote(""); return; }
      setNote("Could not save that page. Try again on Wi-Fi.");
    }
  }
  return (
    <div>
      {!embedded && (
        <PageHeader kicker="Tap a page · save to this device" title="Printables" subtitle="One scroll of ready sheets. Tap the picture to keep it." />
      )}
      <div className="print-hero">
        <h3>Tap a page to save it</h3>
        <p>No packs to open. Scroll the sheets and tap the image. On iPad choose Save to Files.</p>
      </div>
      {note ? <p className="footer-note">{note}</p> : null}
      <div className="sheets-feed">
        {sheets.map((s) => (
          <button key={s.src} type="button" className="sheet-card" onClick={() => saveSheet(s)}>
            <img src={s.src} alt={s.title} />
            <span className="sheet-cap"><strong>{s.title}</strong><em>Tap to save</em></span>
          </button>
        ))}
      </div>
      {!sheets.length ? <p className="footer-note">Sheets are still publishing — open Discover again in a minute.</p> : null}
    </div>
  );
}

'''
    text = text[:i] + new_gal + text[j:]
    print("replaced PrintablesGallery")
else:
    print("WARN PrintablesGallery not found")
css = """
.sheets-feed { display:flex; flex-direction:column; gap:14px; margin-bottom:18px; }
.sheet-card { border:0; background:#fff; border-radius:16px; padding:0; overflow:hidden; box-shadow:0 8px 24px rgba(18,32,43,.08); text-align:left; cursor:pointer; font-family:inherit; }
.sheet-card img { width:100%; display:block; background:#fff; }
.sheet-cap { display:flex; justify-content:space-between; align-items:center; gap:8px; padding:10px 12px 12px; }
.sheet-cap strong { font-size:14px; color:var(--navy); }
.sheet-cap em { font-style:normal; font-size:12px; font-weight:800; color:#fff; background:var(--amber, #F08A2A); border-radius:999px; padding:5px 10px; }
"""
if ".sheets-feed" not in text:
    text = text.replace(".print-hero {", css + "\n.print-hero {")
    print("added sheets css")
app.write_text(text, encoding="utf-8")
print("wrote", app.name, app.stat().st_size)
