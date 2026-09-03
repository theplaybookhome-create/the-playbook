#!/usr/bin/env python3
"""Insert Daily Communication Boards pack into PRINTABLES_PACKS."""
from pathlib import Path

PACK = '''    samples: ["Core board", "Sentence strip", "Food", "Actions", "Feelings & body", "Toys · school · weather · animals"],
  },
  {
    id: "daily-boards",
    cover: "cover-daily-boards.jpg",
    emoji: "🧩",
    kicker: "Category 5",
    title: "Daily Communication Boards",
    desc: "Full boards plus each group on its own page — toilet, bath, food, feelings, play and more. Print just the section you need.",
    meta: "27 sheets · boy & girl",
    file: "5-daily-communication-boards.pdf",
    samples: ["Full board (boy)", "Full board (girl)", "Toilet · Bath · Food", "Get dressed · Sleep", "School · Play · Feelings", "Quick words · I want / I need"],
  },
];
'''
OLD = '''    samples: ["Core board", "Sentence strip", "Food", "Actions", "Feelings & body", "Toys · school · weather · animals"],
  },
];
'''

def patch(path):
    p = Path(path)
    t = p.read_text()
    if 'id: "daily-boards"' in t:
        print(path, "already patched")
        return
    if OLD not in t:
        raise SystemExit(f"anchor not found in {path}")
    p.write_text(t.replace(OLD, PACK, 1))
    print("patched", path)

if __name__ == "__main__":
    for f in ("app.html", "app-multi-child-printables.html"):
        if Path(f).exists():
            patch(f)
