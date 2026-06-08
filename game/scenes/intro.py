# game/scenes/intro.py
# Pantalla de título con estrellas animadas y texto parpadeante.

import pygame
import random
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, CYAN, YELLOW, GRAY,
    TITLE
)


class Star:
    """Estrella de fondo que cae lentamente."""
    def __init__(self):
        self.reset(random.randint(0, SCREEN_HEIGHT))

    def reset(self, y=0):
        self.x     = random.randint(0, SCREEN_WIDTH)
        self.y     = y
        self.speed = random.uniform(0.4, 1.6)
        self.size  = random.choice([1, 1, 1, 2])
        self.color = random.choice([WHITE, CYAN, GRAY])

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         (int(self.x), int(self.y), self.size, self.size))


class IntroScene:
    """
    Pantalla de inicio.
    Devuelve 'select' cuando el jugador presiona ENTER o SPACE.
    """

    N_STARS = 80

    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.stars   = [Star() for _ in range(self.N_STARS)]
        self.blink   = 0          # contador para texto parpadeante
        self.show_prompt = True

    # ── Loop ────────────────────────────────────────────────────

    def update(self) -> str | None:
        for s in self.stars:
            s.update()

        self.blink += 1
        if self.blink >= 40:
            self.blink       = 0
            self.show_prompt = not self.show_prompt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return 'select'
        return None

    def draw(self):
        self.screen.fill(BLACK)

        for s in self.stars:
            s.draw(self.screen)

        self._draw_title()
        self._draw_subtitle()
        if self.show_prompt:
            self._draw_prompt()
        self._draw_controls()

    # ── Helpers de texto ────────────────────────────────────────

    def _font(self, size):
        return pygame.font.SysFont('Courier New', size, bold=True)

    def _draw_title(self):
        font  = self._font(52)
        text  = font.render("STELLAR", True, CYAN)
        text2 = font.render("DEFENSE", True, YELLOW)
        cx    = SCREEN_WIDTH // 2
        self.screen.blit(text,  text.get_rect(center=(cx, 180)))
        self.screen.blit(text2, text2.get_rect(center=(cx, 240)))

        # Línea decorativa
        pygame.draw.line(self.screen, CYAN,
                         (cx - 140, 270), (cx + 140, 270), 2)

    def _draw_subtitle(self):
        font = self._font(14)
        text = font.render("A CODE IN PLACE PROJECT  //  2026", True, GRAY)
        self.screen.blit(text, text.get_rect(
            center=(SCREEN_WIDTH // 2, 295)))

    def _draw_prompt(self):
        font = self._font(18)
        text = font.render("[ PRESS ENTER TO START ]", True, WHITE)
        self.screen.blit(text, text.get_rect(
            center=(SCREEN_WIDTH // 2, 400)))

    def _draw_controls(self):
        font  = self._font(13)
        lines = [
            "A / ← →  MOVE",
            "SPACE    SHOOT",
            "ESC      QUIT",
        ]
        y = SCREEN_HEIGHT - 90
        for line in lines:
            t = font.render(line, True, GRAY)
            self.screen.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 22