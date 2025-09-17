from __future__ import annotations
import random
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
import pygame
from pygame import Rect
import src.settings as S

@dataclass
class Alien:
    row: int
    col: int
    x: float
    y: float
    w: int
    h: int
    points: int
    alive: bool = True

    @property
    def rect(self) -> Rect:
        return Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surface: pygame.Surface) -> None:
        color = S.ALIEN_COLORS.get(self.points, S.GREEN)
        pygame.draw.rect(surface, color, self.rect)

class AlienGrid:
    def __init__(self):
        self.aliens: List[Alien] = []
        self.dir = 1  # 1 = right, -1 = left
        self.h_speed = S.ALIEN_H_SPEED
        self._spawn_grid()
        self._shot_timer = self._rand_shot_interval()

    def _spawn_grid(self) -> None:
        self.aliens.clear()
        # Points by row (original: top row 30, next 2 rows 20, last 2 rows 10)
        def points_for_row(r: int) -> int:
            if r == 0:
                return 30
            elif r in (1, 2):
                return 20
            else:
                return 10

        start_x = S.GRID_LEFT_MARGIN
        start_y = S.GRID_TOP_MARGIN
        for r in range(S.GRID_ROWS):
            for c in range(S.GRID_COLS):
                x = start_x + c * S.GRID_H_SPACING
                y = start_y + r * S.GRID_V_SPACING
                self.aliens.append(Alien(
                    row=r, col=c, x=x, y=y, w=S.ALIEN_W, h=S.ALIEN_H, points=points_for_row(r)
                ))

    def living_aliens(self) -> List[Alien]:
        return [a for a in self.aliens if a.alive]

    def bounds(self) -> Optional[Rect]:
        alive = self.living_aliens()
        if not alive:
            return None
        left = min(a.x for a in alive)
        right = max(a.x + a.w for a in alive)
        top = min(a.y for a in alive)
        bottom = max(a.y + a.h for a in alive)
        return Rect(int(left), int(top), int(right - left), int(bottom - top))

    def update(self, dt: float) -> bool:
        # Move horizontally
        moved_down = False
        for a in self.living_aliens():
            a.x += self.dir * self.h_speed * dt

        # Check edges
        b = self.bounds()
        if b:
            if b.left <= S.ALIEN_EDGE_MARGIN or b.right >= S.WIDTH - S.ALIEN_EDGE_MARGIN:
                # Descend and reverse
                for a in self.living_aliens():
                    a.y += S.ALIEN_DESCEND_STEP
                self.dir *= -1
                self.h_speed *= S.ALIEN_SPEEDUP_FACTOR
                moved_down = True

        return moved_down

    def reached_bottom(self) -> bool:
        for a in self.living_aliens():
            if a.y + a.h >= S.HEIGHT - S.PLAYER_Y_OFFSET + 4:
                return True
        return False

    def _rand_shot_interval(self) -> float:
        return random.uniform(S.ALIEN_SHOT_INTERVAL_MIN, S.ALIEN_SHOT_INTERVAL_MAX)

    def choose_shooter(self) -> Optional[Alien]:
        # Bottom-most alive alien in each column can shoot
        shooters: Dict[int, Alien] = {}
        for a in self.living_aliens():
            prev = shooters.get(a.col)
            if prev is None or a.row > prev.row:
                shooters[a.col] = a
        if not shooters:
            return None
        return random.choice(list(shooters.values()))

    def update_shooting(self, dt: float) -> bool:
        # Returns True if a shot should be fired by a chosen alien now
        self._shot_timer -= dt
        if self._shot_timer <= 0:
            self._shot_timer = self._rand_shot_interval()
            return True
        return False