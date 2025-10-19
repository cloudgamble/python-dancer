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
    parser.add_argument("--fps", type=int, default=6, help="Frames per second (default: 6)")
    parser.add_argument("--scale", type=int, default=2, help="Tile characters to appear larger (default: 2)")
    parser.add_argument("--move-every", type=int, default=2, help="Move sprite every N frames (default: 2)")
    parser.add_argument("--frame-every", type=int, default=3, help="Advance animation frame every N draws (default: 3)")

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

    engine = AnimationEngine(
        themes=THEMES,
        start_theme=theme,
        fps=max(1, args.fps),
        scale=max(1, args.scale),
        move_every=max(1, args.move_every),
        frame_every=max(1, args.frame_every),
    )
    engine.run()
