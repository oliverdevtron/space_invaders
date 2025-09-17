from __future__ import annotations
import random
import pygame
from pygame import Rect
from typing import List, Optional
import src.settings as S
from src.player import Player
from src.bullet import Bullet
from src.alien import AlienGrid, Alien

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Invaders (Pygame)")
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Consolas", 22)
        self.big_font = pygame.font.SysFont("Consolas", 38)

        self.state = S.STATE_MENU
        self.score = 0
        self.lives = S.PLAYER_START_LIVES

        self.player = Player()
        self.grid = AlienGrid()

        self.player_bullets: List[Bullet] = []
        self.alien_bullets: List[Bullet] = []

        # Control repeat fire (enforce at most one bullet)
        self.can_shoot = True

        # Simple respawn invulnerability (optional enhancement)
        self.invuln_timer = 0.0

    def reset_game(self) -> None:
        self.score = 0
        self.lives = S.PLAYER_START_LIVES
        self.player.reset()
        self.player.alive = True
        self.grid = AlienGrid()
        self.player_bullets.clear()
        self.alien_bullets.clear()
        self.can_shoot = True
        self.invuln_timer = 0.0

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.state == S.STATE_MENU:
                        self.reset_game()
                        self.state = S.STATE_PLAYING
                    elif self.state in (S.STATE_GAMEOVER, S.STATE_VICTORY):
                        self.reset_game()
                        self.state = S.STATE_PLAYING
                elif event.key == pygame.K_SPACE:
                    if self.state == S.STATE_PLAYING and self.can_shoot:
                        self.shoot_player()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.can_shoot = True
        return True

    def shoot_player(self) -> None:
        # Only allow one bullet on screen
        if len(self.player_bullets) < S.MAX_PLAYER_BULLETS:
            bullet_x = self.player.rect.centerx - S.BULLET_WIDTH // 2
            bullet_y = self.player.rect.top
            bullet = Bullet(bullet_x, bullet_y, S.BULLET_SPEED_PLAYER, S.WHITE, "player")
            self.player_bullets.append(bullet)
            self.can_shoot = False

    def shoot_alien(self, alien: Alien) -> None:
        if len(self.alien_bullets) < S.MAX_ALIEN_BULLETS:
            bullet_x = alien.rect.centerx - S.BULLET_WIDTH // 2
            bullet_y = alien.rect.bottom
            bullet = Bullet(bullet_x, bullet_y, S.BULLET_SPEED_ALIEN, S.YELLOW, "alien")
            self.alien_bullets.append(bullet)

    def update_bullets(self, dt: float) -> None:
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet.update(dt)
            if bullet.offscreen():
                self.player_bullets.remove(bullet)

        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.update(dt)
            if bullet.offscreen():
                self.alien_bullets.remove(bullet)

    def check_collisions(self) -> None:
        # Player bullets vs aliens
        for bullet in self.player_bullets[:]:
            for alien in self.grid.living_aliens():
                if bullet.rect.colliderect(alien.rect):
                    self.score += alien.points
                    alien.alive = False
                    self.player_bullets.remove(bullet)
                    break

        # Alien bullets vs player
        if self.player.alive and self.invuln_timer <= 0:
            for bullet in self.alien_bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    self.lives -= 1
                    self.alien_bullets.remove(bullet)
                    self.invuln_timer = 1.0  # 1 second invulnerability
                    if self.lives <= 0:
                        self.player.alive = False
                    break

    def update_playing(self, dt: float, keys) -> None:
        if self.invuln_timer > 0:
            self.invuln_timer -= dt

        # Update player
        if self.player.alive:
            self.player.update(dt, keys)

        # Update alien grid
        self.grid.update(dt)

        # Alien shooting
        if self.grid.update_shooting(dt):
            shooter = self.grid.choose_shooter()
            if shooter:
                self.shoot_alien(shooter)

        # Update bullets
        self.update_bullets(dt)

        # Check collisions
        self.check_collisions()

        # Check win/lose conditions
        if not self.grid.living_aliens():
            self.state = S.STATE_VICTORY
        elif not self.player.alive or self.grid.reached_bottom():
            self.state = S.STATE_GAMEOVER

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        
        if self.state == S.STATE_PLAYING:
            self.update_playing(dt, keys)

    def draw_text(self, text: str, x: int, y: int, font=None, color=S.WHITE) -> None:
        if font is None:
            font = self.font
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def draw_menu(self) -> None:
        self.draw_text("SPACE INVADERS", S.WIDTH // 2 - 120, S.HEIGHT // 2 - 60, self.big_font, S.GREEN)
        self.draw_text("Press ENTER to Start", S.WIDTH // 2 - 100, S.HEIGHT // 2, self.font, S.WHITE)
        self.draw_text("Controls: A/D or Arrow Keys to Move, SPACE to Fire", S.WIDTH // 2 - 200, S.HEIGHT // 2 + 40, self.font, S.GRAY)

    def draw_playing(self) -> None:
        # Draw player (with invulnerability flashing)
        if self.player.alive:
            if self.invuln_timer <= 0 or int(self.invuln_timer * 10) % 2:
                self.player.draw(self.screen)

        # Draw aliens
        for alien in self.grid.living_aliens():
            alien.draw(self.screen)

        # Draw bullets
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        for bullet in self.alien_bullets:
            bullet.draw(self.screen)

        # Draw UI
        self.draw_text(f"Score: {self.score}", 10, 10)
        self.draw_text(f"Lives: {self.lives}", 10, 40)

    def draw_gameover(self) -> None:
        self.draw_text("GAME OVER", S.WIDTH // 2 - 80, S.HEIGHT // 2 - 40, self.big_font, S.RED)
        self.draw_text(f"Final Score: {self.score}", S.WIDTH // 2 - 80, S.HEIGHT // 2, self.font, S.WHITE)
        self.draw_text("Press ENTER to Restart", S.WIDTH // 2 - 100, S.HEIGHT // 2 + 40, self.font, S.GRAY)

    def draw_victory(self) -> None:
        self.draw_text("VICTORY!", S.WIDTH // 2 - 70, S.HEIGHT // 2 - 40, self.big_font, S.GREEN)
        self.draw_text(f"Final Score: {self.score}", S.WIDTH // 2 - 80, S.HEIGHT // 2, self.font, S.WHITE)
        self.draw_text("Press ENTER to Restart", S.WIDTH // 2 - 100, S.HEIGHT // 2 + 40, self.font, S.GRAY)

    def draw(self) -> None:
        self.screen.fill(S.BLACK)
        
        if self.state == S.STATE_MENU:
            self.draw_menu()
        elif self.state == S.STATE_PLAYING:
            self.draw_playing()
        elif self.state == S.STATE_GAMEOVER:
            self.draw_gameover()
        elif self.state == S.STATE_VICTORY:
            self.draw_victory()
        
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(S.FPS) / 1000.0  # Convert to seconds
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()