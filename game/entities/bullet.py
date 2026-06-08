# game/entities/bullet.py

import pygame
from game.settings import BULLET_SPEED, WHITE, YELLOW

class Bullet(pygame.sprite.Sprite):
    """
    Bala del jugador: sube por la pantalla.
    Bala enemiga: baja por la pantalla.
    direction = -1 (jugador, sube) | +1 (enemigo, baja)
    """

    WIDTH  = 3
    HEIGHT = 10

    def __init__(self, x: int, y: int, color=WHITE, direction: int = -1):
        super().__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect      = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed     = BULLET_SPEED

    def update(self):
        self.rect.y += self.speed * self.direction
        # Se elimina sola al salir de pantalla
        if self.rect.bottom < 0 or self.rect.top > 700:
            self.kill()