# game/entities/explosion.py
# Explosión pixel art animada por frames.
# Sin imágenes externas: dibuja círculos concéntricos que se expanden.

import pygame
from game.settings import YELLOW, ORANGE, RED, WHITE

class Explosion(pygame.sprite.Sprite):
    """
    Animación de explosión retro en 6 frames.
    Se elimina sola al terminar.
    """

    FRAMES     = 6
    FRAME_DUR  = 4   # frames de juego por frame de animación

    def __init__(self, cx: int, cy: int, size: int = 28):
        super().__init__()
        self.frames  = self._build_frames(size)
        self.index   = 0
        self.timer   = 0
        self.image   = self.frames[0]
        self.rect    = self.image.get_rect(center=(cx, cy))

    # ── Construcción de frames ──────────────────────────────────

    def _build_frames(self, size: int):
        colors   = [WHITE, YELLOW, YELLOW, ORANGE, RED, (80, 0, 0)]
        frames   = []
        for i, color in enumerate(colors):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            r    = int(size / 2 * (i + 1) / self.FRAMES)
            pygame.draw.circle(surf, color, (size // 2, size // 2), r)
            # Anillo interior más brillante
            if r > 4:
                pygame.draw.circle(surf, WHITE, (size // 2, size // 2), r // 3)
            frames.append(surf)
        return frames

    # ── Loop de animación ───────────────────────────────────────

    def update(self):
        self.timer += 1
        if self.timer >= self.FRAME_DUR:
            self.timer  = 0
            self.index += 1
            if self.index >= self.FRAMES:
                self.kill()
                return
            self.image = self.frames[self.index]