# game/scenes/game_over.py

import pygame
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, RED, GRAY, YELLOW
)


class GameOverScene:
    """
    Pantalla de derrota. Muestra puntaje final.
    R → reiniciar | ESC → intro
    """

    def __init__(self, screen: pygame.Surface, score: int):
        self.screen = screen
        self.score  = score

    def update(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'select'
                if event.key == pygame.K_ESCAPE:
                    return 'intro'
        return None

    def draw(self):
        self.screen.fill(BLACK)
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2

        font_big  = pygame.font.SysFont('Courier New', 52, bold=True)
        font_med  = pygame.font.SysFont('Courier New', 22, bold=True)
        font_sm   = pygame.font.SysFont('Courier New', 15, bold=True)

        t1 = font_big.render("GAME OVER", True, RED)
        t2 = font_med.render(f"SCORE: {self.score:06d}", True, YELLOW)
        t3 = font_sm.render("[ R ]  PLAY AGAIN     [ ESC ]  MENU", True, GRAY)

        self.screen.blit(t1, t1.get_rect(center=(cx, cy - 60)))
        self.screen.blit(t2, t2.get_rect(center=(cx, cy + 10)))
        self.screen.blit(t3, t3.get_rect(center=(cx, cy + 80)))