# game/entities/player.py

import pygame
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_SPEED, PLAYER_LIVES,
    SHOOT_COOLDOWN, CYAN, WHITE
)
from game.utils.pixel_art import draw_sprite, ALL_SHIPS

PIXEL_SCALE   = 3
SPRITE_COLS   = 11
SPRITE_ROWS   = 11


class Player(pygame.sprite.Sprite):
    """
    Nave del jugador.
    ship_index: índice en settings.SHIPS (0-4)
    ship_data:  dict con speed_bonus, fire_bonus, color, accent
    """

    W = SPRITE_COLS * PIXEL_SCALE   # 33 px
    H = SPRITE_ROWS * PIXEL_SCALE   # 33 px

    def __init__(self, ship_index: int, ship_data: dict):
        super().__init__()

        self.ship_index = ship_index
        self.speed      = PLAYER_SPEED + ship_data.get("speed_bonus", 0)
        self.cooldown   = SHOOT_COOLDOWN + ship_data.get("fire_bonus", 0)
        self.lives      = PLAYER_LIVES
        self.score      = 0
        self._shoot_timer = 0

        color  = ship_data.get("color",  CYAN)
        accent = ship_data.get("accent", WHITE)
        matrix = ALL_SHIPS[ship_index]

        self.image = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        draw_sprite(self.image, matrix, color, accent, 0, 0, PIXEL_SCALE)

        self.rect = self.image.get_rect(
            midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)
        )

    # ── Movimiento ──────────────────────────────────────────────

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Límites de pantalla
        self.rect.left  = max(self.rect.left,  4)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH - 4)

        # Cooldown de disparo
        if self._shoot_timer > 0:
            self._shoot_timer -= 1

    # ── Disparo ─────────────────────────────────────────────────

    def can_shoot(self) -> bool:
        return self._shoot_timer == 0

    def shoot(self):
        """Registra el disparo. Devuelve la posición del cañón."""
        self._shoot_timer = self.cooldown
        return self.rect.centerx, self.rect.top

    # ── Daño ────────────────────────────────────────────────────

    def hit(self):
        """Resta una vida. Devuelve True si el jugador sigue vivo."""
        self.lives -= 1
        return self.lives > 0