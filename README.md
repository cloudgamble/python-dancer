# python-dancer

Animated, colorful CLI character that dances, plays soccer, and generally has a good time — with 25+ themes and keyboard controls.

## Features

- 25 themes (dancer, robot, soccer, surfer, ninja, etc.)
- Color + emoji output (requires a Unicode-capable terminal)
- Smooth animations using `blessed`
- Keyboard controls:
  - `q`: quit
  - `space` or `s`: pause/resume
  - `←`/`→`: previous/next theme
  - `r`: random theme
  - scale via `--scale` (default 2)

## Requirements

- Python 3.13
- macOS Terminal or iTerm2 recommended

## Setup

```bash
cd ~/github/python-dancer
python3.13 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run with defaults:

```bash
python -m python_dancer
```

Pick a theme:

```bash
python -m python_dancer --theme soccer
```

Random theme:

```bash
python -m python_dancer --random
```

List all themes:

```bash
python -m python_dancer --list
```

Adjust size and speed:

```bash
python -m python_dancer --scale 3 --fps 5 --move-every 3
```

## Notes

- Emoji rendering depends on your terminal font.
- Resize the terminal for bigger play area.

## License

MIT