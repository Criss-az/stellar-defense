# game/scenes/victory.py

import pygame
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, CYAN, YELLOW, GREEN, GRAY
)


class VictoryScene:
    """
    Pantalla de victoria.
    R → siguiente nivel | ESC → intro
    Recibe nivel completado y puntaje.
    """

    def __init__(self, screen: pygame.Surface, score: int, level: int):
        self.screen = screen
        self.score  = score
        self.level  = level

    def update(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'next_level'
                if event.key == pygame.K_ESCAPE:
                    return 'intro'
        return None

    def draw(self):
        self.screen.fill(BLACK)
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2

        font_big = pygame.font.SysFont('Courier New', 42, bold=True)
        font_med = pygame.font.SysFont('Courier New', 22, bold=True)
        font_sm  = pygame.font.SysFont('Courier New', 15, bold=True)

        t1 = font_big.render("SECTOR CLEARED!", True, GREEN)
        t2 = font_med.render(f"LEVEL {self.level}  COMPLETE", True, CYAN)
        t3 = font_med.render(f"SCORE: {self.score:06d}", True, YELLOW)
        t4 = font_sm.render("[ R ]  NEXT LEVEL     [ ESC ]  MENU", True, GRAY)

        self.screen.blit(t1, t1.get_rect(center=(cx, cy - 80)))
        self.screen.blit(t2, t2.get_rect(center=(cx, cy - 30)))
        self.screen.blit(t3, t3.get_rect(center=(cx, cy + 20)))
        self.screen.blit(t4, t4.get_rect(center=(cx, cy + 90)))