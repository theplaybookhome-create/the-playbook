#!/usr/bin/env python3
"""Decode Canva app assets and wire them into app.html / sw.js. Idempotent."""
from pathlib import Path
import base64
import json
import shutil

ROOT = Path(".")
HERE = Path(__file__).resolve().parent
B64_DIR = HERE / "canva_b64"
ASSETS_JSON = HERE / "canva_assets.json"
ASSETS_COMPACT = HERE / "canva_assets_compact.json"

CSS = """
.brand-mark-img { width:28px; height:28px; border-radius:8px; object-fit:cover; flex-shrink:0; box-shadow:0 4px 10px rgba(11,18,25,.28); }
.print-pack .pp-cover { width:100%; aspect-ratio:16/10; object-fit:cover; border-radius:14px; margin:0 0 10px; background:#1A252F; display:block; }
.print-pack .pp-emoji { display:none; }
"""

EXPECTED = [
    "brand-1024.png",
    "icon-512.png",
    "icon-192.png",
    "icon-180.png",
    "icon-maskable-512.png",
    "favicon.png",
    "cover-complete.jpg",
    "cover-visual.jpg",
    "cover-colouring.jpg",
    "cover-learning.jpg",
    "cover-aac.jpg",
]


def _read_clean(path: Path) -> str:
    return "".join(path.read_text(encoding="utf-8").split())


def load_blobs():
    blobs = {}
    if B64_DIR.is_dir():
        for src in sorted(B64_DIR.glob("*.b64")):
            blobs[src.name[:-4]] = _read_clean(src)
            print("b64", src.name[:-4], len(blobs[src.name[:-4]]))
    for candidate in (ASSETS_JSON, ASSETS_COMPACT):
        if candidate.is_file():
            extra = json.loads(candidate.read_text(encoding="utf-8"))
            for name, blob in extra.items():
                blobs.setdefault(name, blob)
            print("json", candidate.name, len(extra))
    if not blobs:
        raise SystemExit("no Canva assets found (canva_b64/*.b64 or canva_assets.json)")
    return blobs


def write_assets(root: Path) -> None:
    blobs = load_blobs()
    for name in EXPECTED:
        if name not in blobs:
            print("missing payload", name)
            continue
        dest = root / name
        try:
            data = base64.b64decode(blobs[name], validate=False)
        except Exception as exc:
            print("skip bad payload", name, exc)
            continue
        if len(data) < 32:
            print("skip tiny payload", name, len(data))
            continue
        if data[:2] != b"\xff\xd8" and data[:8] != b"\x89PNG\r\n\x1a\n":
            print("skip non-image payload", name, data[:8])
            continue
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)
            print("wrote", dest, len(data))
        else:
            print("ok", dest, len(data))
    src = root / "cover-complete.jpg"
    if src.exists() and src.stat().st_size > 32:
        for name in ("cover-visual.jpg", "cover-colouring.jpg", "cover-learning.jpg", "cover-aac.jpg"):
            dest = root / name
            if not dest.exists() or dest.stat().st_size < 32:
                shutil.copyfile(src, dest)
                print("copied fallback", dest)


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
    s = s.replace("./sw.js?v=18", "./sw.js?v=19")
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
