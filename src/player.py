from __future__ import annotations
import pygame
from pygame import Rect
import src.settings as S

class Player:
    def __init__(self):
        self.width = S.PLAYER_WIDTH
        self.height = S.PLAYER_HEIGHT
        self.x = (S.WIDTH - self.width) / 2
        self.y = S.HEIGHT - S.PLAYER_Y_OFFSET
        self.speed = S.PLAYER_SPEED
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)
        self.alive = True

    def reset(self):
        self.x = (S.WIDTH - self.width) / 2
        self.y = S.HEIGHT - S.PLAYER_Y_OFFSET
        self.rect.topleft = (int(self.x), int(self.y))

    def update(self, dt: float, keys) -> None:
        vx = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx += self.speed
        self.x += vx * dt
        # clamp
        if self.x < 0:
            self.x = 0
        if self.x + self.width > S.WIDTH:
            self.x = S.WIDTH - self.width
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, S.CYAN, self.rect)
        # Optional: draw a small "cannon" barrel
        barrel = pygame.Rect(self.rect.centerx - 2, self.rect.top - 6, 4, 6)
        pygame.draw.rect(surface, S.CYAN, barrel)