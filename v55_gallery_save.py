#!/usr/bin/env python3
from pathlib import Path
app = Path(__file__).resolve().parent / "app.html"
text = app.read_text(encoding="utf-8")
repls = [
    ('text: "Save to Files or Print"', 'text: "Save Image to put this in your gallery"'),
    ("setNote(\"Share sheet opened \u2014 tap Save to Files.\");", "setNote(\"Share sheet opened \u2014 tap Save Image / Add to Photos.\");"),
    ("setNote(\"Saved. Check Files or Downloads.\");", "setNote(\"Saved. Check your photo gallery or Downloads.\");"),
    ("On iPad choose Save to Files.", "On iPad tap Save Image to add it to your gallery."),
    ("Tap a page \u00b7 save to this device", "Tap a page \u00b7 save to gallery"),
    ("<em>Tap to save</em>", "<em>Save to gallery</em>"),
    ('const f = new File([blob], name, { type: blob.type || "image/jpeg" });',
     'const f = new File([blob], name.replace(/\\.[^.]+$/, ".jpg"), { type: "image/jpeg" });'),
]
n = 0
for a, b in repls:
    if a in text:
        text = text.replace(a, b)
        n += 1
        print("replaced:", a[:50])
    else:
        print("miss:", a[:50])
app.write_text(text, encoding="utf-8")
print("done", n, "replacements", app.stat().st_size)
