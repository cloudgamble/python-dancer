from __future__ import annotations

import argparse
import random
from typing import Optional

from .engine import AnimationEngine
from .themes import THEMES, Theme


def run() -> None:
    parser = argparse.ArgumentParser(
        prog="python-dancer",
        description="Colorful CLI character with 25+ themes and movements",
    )
    parser.add_argument("--theme", type=str, default=None, help="Start with a specific theme by name")
    parser.add_argument("--random", action="store_true", help="Start with a random theme")
    parser.add_argument("--list", action="store_true", help="List themes and exit")
    parser.add_argument("--fps", type=int, default=12, help="Frames per second (default: 12)")

    args = parser.parse_args()

    if args.list:
        for t in THEMES:
            print(t.name)
        return

    theme: Optional[Theme] = None
    if args.random:
        theme = random.choice(THEMES)
    elif args.theme:
        wanted = args.theme.strip().lower()
        theme = next((t for t in THEMES if t.name.lower() == wanted), None)
        if theme is None:
            print(f"Theme not found: {args.theme}\nAvailable: {', '.join(t.name for t in THEMES)}")
            return
    else:
        theme = THEMES[0]

    engine = AnimationEngine(themes=THEMES, start_theme=theme, fps=max(1, args.fps))
    engine.run()
