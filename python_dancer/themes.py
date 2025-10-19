from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List

from blessed import Terminal


term = Terminal()


Colorize = Callable[[str], str]


def make_color(color_name: str) -> Colorize:
    def _f(s: str) -> str:
        color_fn = getattr(term, color_name, term.white)
        return color_fn(s)

    return _f


@dataclass(frozen=True)
class Theme:
    name: str
    frames: List[List[str]]
    colorize: Colorize
    movement: str  # one of: bounce, slide, jitter


def simple_frames(*emojis: str) -> List[List[str]]:
    return [[e] for e in emojis]


THEMES: List[Theme] = [
    Theme("Dancer", simple_frames("💃", "🕺"), make_color("magenta"), "bounce"),
    Theme("Breakdance", simple_frames("🤸", "🕺", "🤸"), make_color("yellow"), "jitter"),
    Theme("Robot", simple_frames("🤖", "🦾🤖🦿", "🤖"), make_color("cyan"), "slide"),
    Theme("Moonwalk", simple_frames("🕺", "🕺🏻", "🕺🏼", "🕺🏽"), make_color("white"), "slide"),
    Theme("DJ", simple_frames("🎧", "🎛️", "🎚️"), make_color("green"), "bounce"),
    Theme("Drummer", simple_frames("🥁", "🥁🥁", "🥁"), make_color("red"), "jitter"),
    Theme("Guitarist", simple_frames("🎸", "🎶🎸", "🎸"), make_color("yellow"), "bounce"),
    Theme("Juggler", simple_frames("🤹", "🤹‍♂️", "🤹‍♀️"), make_color("cyan"), "jitter"),
    Theme("Magician", simple_frames("🎩", "✨🎩", "🪄"), make_color("magenta"), "bounce"),
    Theme("Clown", simple_frames("🤡", "🎈🤡", "🤡"), make_color("red"), "jitter"),
    Theme("Bartender", simple_frames("🍸", "🍹", "🍻"), make_color("yellow"), "slide"),
    Theme("Chef", simple_frames("👨‍🍳", "🍳", "🍝"), make_color("white"), "bounce"),
    Theme("Soccer", simple_frames("⚽️", "🤾", "⚽️"), make_color("green"), "slide"),
    Theme("Basketball", simple_frames("🏀", "⛹️", "🏀"), make_color("yellow"), "bounce"),
    Theme("Boxer", simple_frames("🥊", "🤜🤛", "🥊"), make_color("red"), "jitter"),
    Theme("Runner", simple_frames("🏃", "🏃‍♂️", "🏃‍♀️"), make_color("cyan"), "slide"),
    Theme("Skateboard", simple_frames("🛹", "🛹", "🛹"), make_color("white"), "slide"),
    Theme("Surfer", simple_frames("🏄", "🌊🏄", "🏄"), make_color("blue"), "bounce"),
    Theme("Skier", simple_frames("⛷️", "🎿", "⛷️"), make_color("white"), "slide"),
    Theme("Snowboarder", simple_frames("🏂", "🏂", "🏂"), make_color("cyan"), "slide"),
    Theme("Yoga", simple_frames("🧘", "🧘‍♂️", "🧘‍♀️"), make_color("magenta"), "jitter"),
    Theme("Weightlift", simple_frames("🏋️", "🏋️‍♂️", "🏋️‍♀️"), make_color("yellow"), "bounce"),
    Theme("Ninja", simple_frames("🥷", "⚔️", "🥷"), make_color("black" if hasattr(term, "black") else "white"), "jitter"),
    Theme("Pirate", simple_frames("🏴‍☠️", "🦜", "🏴‍☠️"), make_color("red"), "bounce"),
    Theme("Cowboy", simple_frames("🤠", "🐎", "🤠"), make_color("yellow"), "slide"),
]
