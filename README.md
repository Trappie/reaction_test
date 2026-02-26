# Reaction Test

A collection of browser-based reaction time tests, served locally via Flask.

## Setup

```bash
python3 -m venv venv
pip install -r requirements.txt
```

## Run

```bash
venv/bin/python main.py
```

Then open http://localhost:5000 in your browser.

## Tests

| Tab | Name | Input | Description |
|-----|------|-------|-------------|
| 1 | Reaction Test | Click / Space | Square turns green after a random delay — react as fast as possible |
| 2 | Confirmation Test | Left / Right click | Countdown, then blue (left) or yellow (right) |
| 3 | Go / No-Go | Left click / nothing | Countdown, then blue (click) or red (don't click, 1 s window) |
| 4 | Triple Choice | Left / Right click / nothing | Countdown, then blue (left), yellow (right), or red (no-go) |
| 5 | Reflex Triple | Left / Right click / nothing | Same as Tab 4 but random delay, no countdown |
| 6 | Key Test | D / F / J / K / nothing | Countdown, then one of 4 key boxes lights up, or all red (no-go) |
| 7 | Reflex Keys | D / F / J / K / nothing | Same as Tab 6 but random delay, no countdown |

## Key color mapping (Tabs 6 & 7)

| Color | Key |
|-------|-----|
| Green | D |
| Orange | F |
| Purple | J |
| Cyan | K |
| Red (all boxes) | Don't press |

## Timing accuracy

All tests use `performance.now()` for sub-millisecond precision. Reaction timestamps are captured on `pointerdown` / `keydown` (the earliest possible browser events). Color changes are synchronized to `requestAnimationFrame` so the start timestamp is recorded at the same frame the color appears. Results are shown in milliseconds and frames (@ 60 fps).
