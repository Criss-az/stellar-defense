# game/scenes/ship_select.py
# Selector de nave con preview pixel art y stats.

import pygame
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, CYAN, YELLOW, GRAY, GREEN, RED,
    SHIPS
)
from game.utils.pixel_art import draw_sprite, ALL_SHIPS

PIXEL_SCALE = 5   # más grande para el preview


class ShipSelectScene:
    """
    El jugador elige entre 5 naves con ← →.
    Devuelve ('play', ship_index) al confirmar con ENTER.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen   = screen
        self.selected = 0          # índice actual

    # ── Loop ────────────────────────────────────────────────────

    def update(self) -> tuple | str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.selected = (self.selected - 1) % len(SHIPS)
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.selected = (self.selected + 1) % len(SHIPS)
                if event.key == pygame.K_RETURN:
                    return ('play', self.selected)
                if event.key == pygame.K_ESCAPE:
                    return 'intro'
        return None

    def draw(self):
        self.screen.fill(BLACK)
        self._draw_header()
        self._draw_ship_preview()
        self._draw_ship_name()
        self._draw_description()
        self._draw_stats()
        self._draw_arrows()
        self._draw_dots()

    # ── Secciones visuales ──────────────────────────────────────

    def _font(self, size):
        return pygame.font.SysFont('Courier New', size, bold=True)

    def _draw_header(self):
        font = self._font(22)
        text = font.render("SELECT YOUR SHIP", True, CYAN)
        self.screen.blit(text, text.get_rect(
            center=(SCREEN_WIDTH // 2, 50)))
        pygame.draw.line(self.screen, CYAN,
                         (60, 72), (SCREEN_WIDTH - 60, 72), 1)

    def _draw_ship_preview(self):
        ship  = SHIPS[self.selected]
        matrix = ALL_SHIPS[self.selected]
        color  = ship['color']
        accent = ship['accent']

        # Tamaño del sprite escalado
        w = 11 * PIXEL_SCALE
        h = 11 * PIXEL_SCALE
        x = SCREEN_WIDTH  // 2 - w // 2
        y = SCREEN_HEIGHT // 2 - h // 2 - 30

        # Fondo con brillo
        glow = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (*color, 30), glow.get_rect())
        self.screen.blit(glow, (x - 10, y - 10))

        draw_sprite(self.screen, matrix, color, accent, x, y, PIXEL_SCALE)

    def _draw_ship_name(self):
        ship = SHIPS[self.selected]
        font = self._font(32)
        text = font.render(ship['name'], True, ship['color'])
        self.screen.blit(text, text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 55)))

    def _draw_description(self):
        ship = SHIPS[self.selected]
        font = self._font(13)
        text = font.render(ship['description'], True, GRAY)
        self.screen.blit(text, text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 85)))

    def _draw_stats(self):
        ship   = SHIPS[self.selected]
        font   = self._font(13)
        spd    = SHIPS[self.selected]['speed_bonus']
        fire   = -SHIPS[self.selected]['fire_bonus']   # negativo = más rápido

        def bar(val, base=5, max_val=8):
            filled = max(1, min(max_val, base + val))
            return '█' * filled + '░' * (max_val - filled)

        lines = [
            f"SPEED  {bar(spd)}",
            f"FIRE   {bar(fire, base=0, max_val=8)}",
        ]
        y = SCREEN_HEIGHT // 2 + 115
        for line in lines:
            t = font.render(line, True, WHITE)
            self.screen.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 22

    def _draw_arrows(self):
        font = self._font(28)
        left  = font.render("◄", True, WHITE)
        right = font.render("►", True, WHITE)
        cy    = SCREEN_HEIGHT // 2 - 10
        self.screen.blit(left,  left.get_rect(midright=(55, cy)))
        self.screen.blit(right, right.get_rect(midleft=(SCREEN_WIDTH - 55, cy)))

    def _draw_dots(self):
        """Indicador de posición — 5 puntos."""
        cx = SCREEN_WIDTH // 2
        y  = SCREEN_HEIGHT - 60
        for i in range(len(SHIPS)):
            color = CYAN if i == self.selected else GRAY
            pygame.draw.circle(self.screen, color,
                               (cx - (len(SHIPS) - 1) * 10 + i * 20, y), 5)

        font = self._font(15)
        hint = font.render("ENTER  TO CONFIRM", True, YELLOW)
        self.screen.blit(hint, hint.get_rect(center=(cx, SCREEN_HEIGHT - 35)))