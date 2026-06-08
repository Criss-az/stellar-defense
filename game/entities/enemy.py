# game/entities/enemy.py

import pygame
import random
from game.settings import (
    ENEMY_SPEED_INIT, ENEMY_SPEED_INC, ENEMY_DROP,
    ENEMY_SHOOT_CHANCE, RED, YELLOW, GREEN,
    SCREEN_WIDTH, POINTS_PER_ENEMY
)
from game.utils.pixel_art import draw_sprite, ENEMY_A, ENEMY_B

ROW_COLORS = [
    (RED,    YELLOW),
    (YELLOW, GREEN),
    (GREEN,  RED),
    (RED,    YELLOW),
]

SPRITE_SIZE   = 11
SPRITE_HEIGHT = 8
PIXEL_SCALE   = 3


def speed_for_level(level: int) -> float:
    """Velocidad base del grupo enemigo según el nivel."""
    return ENEMY_SPEED_INIT + ENEMY_SPEED_INC * (level - 1)


class Enemy(pygame.sprite.Sprite):
    W = SPRITE_SIZE   * PIXEL_SCALE
    H = SPRITE_HEIGHT * PIXEL_SCALE

    def __init__(self, col: int, row: int, x: int, y: int):
        super().__init__()
        self.col    = col
        self.row    = row
        self.points = POINTS_PER_ENEMY

        color, accent = ROW_COLORS[row % len(ROW_COLORS)]
        matrix        = ENEMY_A if row % 2 == 0 else ENEMY_B

        self.image = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        draw_sprite(self.image, matrix, color, accent, 0, 0, PIXEL_SCALE)
        self.rect  = self.image.get_rect(topleft=(x, y))

    def try_shoot(self) -> bool:
        return random.random() < ENEMY_SHOOT_CHANCE


class EnemyGroup:
    PAD_X = 55
    PAD_Y = 60
    GAP_X = 18
    GAP_Y = 14

    def __init__(self, rows: int, cols: int, level: int = 1):
        self.group     = pygame.sprite.Group()
        self.direction = 1
        self.speed     = speed_for_level(level)
        self._populate(rows, cols)

    def _populate(self, rows: int, cols: int):
        for row in range(rows):
            for col in range(cols):
                x = self.PAD_X + col * (Enemy.W + self.GAP_X)
                y = self.PAD_Y + row * (Enemy.H + self.GAP_Y)
                self.group.add(Enemy(col, row, x, y))

    def update(self) -> list:
        sprites = self.group.sprites()
        if not sprites:
            return []

        leftmost  = min(e.rect.left  for e in sprites)
        rightmost = max(e.rect.right for e in sprites)

        if rightmost >= SCREEN_WIDTH - 10 and self.direction == 1:
            self._drop_and_reverse()
        elif leftmost <= 10 and self.direction == -1:
            self._drop_and_reverse()
        else:
            for e in sprites:
                e.rect.x += self.direction * self.speed

        self.group.update()
        return [e for e in sprites if e.try_shoot()]

    def _drop_and_reverse(self):
        for e in self.group.sprites():
            e.rect.y += ENEMY_DROP
        self.direction *= -1

    def reached_bottom(self, limit_y: int) -> bool:
        return any(e.rect.bottom >= limit_y for e in self.group.sprites())