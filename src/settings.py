from __future__ import annotations

# Window
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 200, 255)
YELLOW = (255, 240, 0)
RED = (255, 80, 80)
GRAY = (160, 160, 160)
ALIEN_COLORS = {
    30: (140, 220, 255),  # top row(s)
    20: (140, 255, 140),  # middle row(s)
    10: (255, 240, 140),  # bottom row(s)
}

# Player
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 24
PLAYER_SPEED = 360.0  # px/s
PLAYER_START_LIVES = 3
PLAYER_Y_OFFSET = 70  # distance from bottom
PLAYER_BULLET_COOLDOWN = 0.15  # seconds (for future rapid-fire upgrades)

# Bullets
BULLET_WIDTH = 4
BULLET_HEIGHT = 12
BULLET_SPEED_PLAYER = -600.0  # px/s
BULLET_SPEED_ALIEN = 320.0    # px/s
MAX_PLAYER_BULLETS = 1
MAX_ALIEN_BULLETS = 6  # cap to avoid spam

# Alien grid
GRID_ROWS = 5
GRID_COLS = 11
GRID_LEFT_MARGIN = 60
GRID_TOP_MARGIN = 80
GRID_H_SPACING = 48
GRID_V_SPACING = 40
ALIEN_W = 36
ALIEN_H = 24

# Movement
ALIEN_H_SPEED = 60.0          # px/s initial horizontal speed
ALIEN_DESCEND_STEP = 24       # px per descent
ALIEN_SPEEDUP_FACTOR = 1.06   # speed increase on each edge descent
ALIEN_EDGE_MARGIN = 20        # margin to screen edge before descent

# Alien shooting
ALIEN_SHOT_INTERVAL_MIN = 0.6
ALIEN_SHOT_INTERVAL_MAX = 1.8

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"
STATE_VICTORY = "victory"