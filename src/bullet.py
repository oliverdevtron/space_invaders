from __future__ import annotations
import pygame
from pygame import Rect
from typing import Tuple
import src.settings as S

class Bullet:
    def __init__(self, x: float, y: float, vy: float, color: Tuple[int, int, int], owner: str):
        self.x = x
        self.y = y
        self.vy = vy
        self.color = color
        self.owner = owner  # "player" or "alien"
        self.rect = Rect(int(self.x), int(self.y), S.BULLET_WIDTH, S.BULLET_HEIGHT)

    def update(self, dt: float) -> None:
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x), int(self.y))

    def offscreen(self) -> bool:
        return self.y + self.rect.height < 0 or self.y > S.HEIGHT

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)