#!/usr/bin/env python3
"""Decode Canva app assets and wire them into app.html / sw.js. Idempotent."""
from pathlib import Path
import base64
import json

ROOT = Path(".")
ASSETS_PATH = Path(__file__).with_name("canva_assets.json")

CSS = """
.brand-mark-img { width:28px; height:28px; border-radius:8px; object-fit:cover; flex-shrink:0; box-shadow:0 4px 10px rgba(11,18,25,.28); }
.print-pack .pp-cover { width:100%; aspect-ratio:16/10; object-fit:cover; border-radius:14px; margin:0 0 10px; background:#1A252F; display:block; }
.print-pack .pp-emoji { display:none; }
"""


def write_assets(root: Path) -> None:
    assets = json.loads(ASSETS_PATH.read_text(encoding="utf-8"))
    for name, blob in assets.items():
        dest = root / name
        data = base64.b64decode(blob)
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)
            print("wrote", dest, len(data))
        else:
            print("ok", dest)


def patch_app(root: Path) -> None:
    p = root / "app.html"
    s = p.read_text(encoding="utf-8")
    s = s.replace("<!-- THEME_BUILD_V18 -->", "<!-- THEME_BUILD_V19 -->")
    if "pp-cover" not in s:
        s = s.replace("\n@media print {", CSS + "\n@media print {", 1)
        print("injected cover css")
    old_span = '<span className="brand-mark" />'
    new_span = '<img className="brand-mark-img" src="icon-192.png" width="28" height="28" alt="" />'
    if old_span in s:
        s = s.replace(old_span, new_span)
        print("header mark images")
    covers = {
        'id: "complete"': 'cover: "cover-complete.jpg"',
        'id: "visual"': 'cover: "cover-visual.jpg"',
        'id: "colouring"': 'cover: "cover-colouring.jpg"',
        'id: "learning"': 'cover: "cover-learning.jpg"',
        'id: "aac"': 'cover: "cover-aac.jpg"',
    }
    for id_line, cover in covers.items():
        token = id_line + ","
        if cover not in s and token in s:
            s = s.replace(token, token + "\n    " + cover + ",", 1)
            print("cover field", cover)
    old_emoji = '<div className="pp-emoji" aria-hidden="true">{p.emoji || "📄"}</div>'
    new_cover = '{p.cover ? <img className="pp-cover" src={p.cover} alt="" /> : <div className="pp-emoji" aria-hidden="true">{p.emoji || "📄"}</div>}'
    if old_emoji in s:
        s = s.replace(old_emoji, new_cover, 1)
        print("print pack covers")
    p.write_text(s, encoding="utf-8")
    print("app.html", p.stat().st_size)


def patch_sw(root: Path) -> None:
    p = root / "sw.js"
    s = p.read_text(encoding="utf-8")
    s = s.replace('const CACHE = "playbook-v18";', 'const CACHE = "playbook-v19";')
    if "cover-complete.jpg" not in s:
        s = s.replace(
            '  "./favicon.png"\n];',
            '  "./favicon.png",\n'
            '  "./cover-complete.jpg",\n'
            '  "./cover-visual.jpg",\n'
            '  "./cover-colouring.jpg",\n'
            '  "./cover-learning.jpg",\n'
            '  "./cover-aac.jpg",\n'
            '  "./icon-maskable-512.png"\n];',
        )
        print("sw precache covers")
    p.write_text(s, encoding="utf-8")
    print("sw.js cache bumped")


if __name__ == "__main__":
    write_assets(ROOT)
    patch_app(ROOT)
    patch_sw(ROOT)
