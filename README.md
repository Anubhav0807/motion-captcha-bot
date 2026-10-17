# Modular Selenium mouse bot

The original script is split into modules by responsibility. The existing logic and constants are preserved.

## Files

- `config.py` — ChromeDriver path, credentials, debug flag, mode, and attempt count.
- `geometry.py` — viewport geometry, element rectangles, scrolling, hit testing, and target-point selection.
- `debug_visuals.py` — red movement trail and circle around the final point.
- `mouse_movement.py` — Bézier movement and initial cursor placement.
- `interactions.py` — clicking and human-like typing.
- `main.py` — browser setup and login flow.

## Run

Install Selenium if needed:

```bash
pip install selenium
```

Then run from this folder:

```bash
python main.py
```

Update the values in `config.py` for your environment.
