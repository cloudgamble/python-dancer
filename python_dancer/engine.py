from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, List, Sequence

from blessed import Terminal

from .themes import Theme


@dataclass
class Pos:
    x: int
    y: int


MovementFn = Callable[[int, int, Pos, Pos], Pos]


def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


def move_bounce_box(cols: int, rows: int, pos: Pos, vel: Pos) -> Pos:
    nx, ny = pos.x + vel.x, pos.y + vel.y
    if nx <= 0 or nx >= cols - 1:
        vel.x *= -1
        nx = pos.x + vel.x
    if ny <= 1 or ny >= rows - 2:
        vel.y *= -1
        ny = pos.y + vel.y
    return Pos(nx, ny)


def move_slide_lr(cols: int, rows: int, pos: Pos, vel: Pos) -> Pos:
    nx = pos.x + vel.x
    if nx >= cols:
        nx = 0
    if nx < 0:
        nx = cols - 1
    ny = pos.y
    return Pos(nx, ny)


def move_jitter(cols: int, rows: int, pos: Pos, vel: Pos) -> Pos:
    jx = random.choice([-1, 0, 1])
    jy = random.choice([-1, 0, 1])
    nx = _clamp(pos.x + jx, 0, cols - 1)
    ny = _clamp(pos.y + jy, 1, rows - 2)
    return Pos(nx, ny)


MOVEMENTS: dict[str, MovementFn] = {
    "bounce": move_bounce_box,
    "slide": move_slide_lr,
    "jitter": move_jitter,
}


class AnimationEngine:
    def __init__(
        self,
        themes: Sequence[Theme],
        start_theme: Theme,
        fps: int = 6,
        scale: int = 2,
        move_every: int = 2,
    ) -> None:
        self.term = Terminal()
        self.themes: List[Theme] = list(themes)
        self.theme_index = self.themes.index(start_theme)
        self.fps = fps
        self.scale = max(1, scale)
        self.move_every = max(1, move_every)
        self.paused = False
        self.pos = Pos(5, 5)
        self.vel = Pos(1, 1)

    def _next_theme(self) -> None:
        self.theme_index = (self.theme_index + 1) % len(self.themes)

    def _prev_theme(self) -> None:
        self.theme_index = (self.theme_index - 1) % len(self.themes)

    def run(self) -> None:
        t = self.term
        with t.fullscreen(), t.hidden_cursor(), t.cbreak(), t.location():
            print(t.clear)
            last_time = time.monotonic()
            frame_index = 0
            while True:
                # Input handling (non-blocking)
                key = t.inkey(timeout=0)
                if key:
                    if key.lower() == "q":
                        break
                    if key == " " or key.lower() == "s":
                        self.paused = not self.paused
                    elif key.name == "KEY_RIGHT":
                        self._next_theme()
                        frame_index = 0
                    elif key.name == "KEY_LEFT":
                        self._prev_theme()
                        frame_index = 0
                    elif key.lower() == "r":
                        self.theme_index = random.randrange(len(self.themes))
                        frame_index = 0

                # Timing
                now = time.monotonic()
                elapsed = now - last_time
                need_draw = elapsed >= 1.0 / max(1, self.fps)
                if not need_draw:
                    time.sleep(0.001)
                    continue
                last_time = now

                # Draw frame
                theme = self.themes[self.theme_index]
                print(t.home + t.clear)

                # Status bar
                status = f"{theme.name}  |  fps={self.fps}  |  controls: q quit, space/s pause, ←/→ theme, r random"
                print(t.bold_white_on_blue(status[: t.width - 1]).ljust(t.width - 1))

                if not self.paused:
                    # Move sprite, but only every N frames to slow down motion
                    if frame_index % self.move_every == 0:
                        mv = MOVEMENTS[theme.movement]
                        self.pos = mv(t.width, t.height, self.pos, self.vel)

                # Render sprite
                frame = theme.frames[frame_index % len(theme.frames)]
                frame_index += 1
                scaled_h = max(1, len(frame) * self.scale)
                cx = _clamp(self.pos.x, 0, max(0, t.width - 1))
                cy = _clamp(self.pos.y, 1, max(1, t.height - scaled_h - 1))
                colorize = theme.colorize
                for i, line in enumerate(frame):
                    y0 = cy + i * self.scale
                    x = cx
                    tiled = (line * self.scale)
                    for vrep in range(self.scale):
                        y = y0 + vrep
                        if y < t.height - 1:
                            print(t.move(y, x) + colorize(tiled))
