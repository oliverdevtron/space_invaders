# Space Invaders (Pygame)

A Python-based recreation of the classic Space Invaders using Pygame.

## Features (MVP)
- Player movement (left/right), screen bounds clamped
- Single-shot firing (one player bullet at a time)
- Alien formation (5x11): horizontal movement, descend on edge, speeds up over time
- Enemy projectiles
- Collision detection (rect-based)
- Score (top=30, middle=20, bottom=10), lives (3)
- Game states: Menu → Playing → Victory/Game Over → Restart

## Requirements
- Python 3.11+
- Pygame 2.5+
- (Optional) Pillow for future asset processing

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
python -m src.main
```

## Controls
- Left/Right or A/D: Move
- Space: Fire (one bullet on screen)
- Enter: Start / Restart

## Notes
- Uses simple rectangles for sprites (placeholders). Swap with PNGs later.
- Fixed timestep via delta-time scaled movement at 60 FPS target.

## Packaging (optional)
- Use PyInstaller after MVP is complete:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole -n SpaceInvaders src/main.py
```

## License
MIT (personal/portfolio project)