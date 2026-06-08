# game/scenes/gameplay.py
# Escena principal: lógica de juego completa.

import pygame
import random
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    BLACK, WHITE, CYAN, YELLOW, RED, GRAY, GREEN,
    ENEMY_ROWS, ENEMY_COLS, POINTS_PER_LEVEL, SHIPS
)
from game.entities.player    import Player
from game.entities.enemy     import EnemyGroup
from game.entities.bullet    import Bullet
from game.entities.explosion import Explosion
from game.utils.pixel_art    import draw_sprite, ALL_SHIPS


class HUD:
    """Dibuja puntaje, vidas y nivel en pantalla."""

    def __init__(self, screen):
        self.screen = screen
        self.font   = pygame.font.SysFont('Courier New', 15, bold=True)

    def draw(self, score: int, lives: int, level: int,
             ship_color, ship_index: int):
        # Puntaje
        t = self.font.render(f"SCORE  {score:06d}", True, WHITE)
        self.screen.blit(t, (10, 8))

        # Nivel
        t2 = self.font.render(f"LVL {level}", True, CYAN)
        self.screen.blit(t2, (SCREEN_WIDTH // 2 - 25, 8))

        # Vidas (miniaturas de la nave)
        matrix = ALL_SHIPS[ship_index]
        x = SCREEN_WIDTH - 14 - lives * 22
        for _ in range(lives):
            draw_sprite(self.screen, matrix,
                        ship_color, WHITE, x, 4, scale=2)
            x += 22

        # Línea separadora
        pygame.draw.line(self.screen, GRAY,
                         (0, 30), (SCREEN_WIDTH, 30), 1)


class GameplayScene:
    """
    Escena de juego principal.
    Recibe ship_index y level (para niveles sucesivos).
    """

    def __init__(self, screen: pygame.Surface,
                 ship_index: int, level: int = 1):
        self.screen     = screen
        self.level      = level
        self.ship_data  = SHIPS[ship_index]

        # Entidades
        self.player     = Player(ship_index, self.ship_data)
        self.enemies    = EnemyGroup(ENEMY_ROWS, ENEMY_COLS, level)
        self.hud        = HUD(screen)

        # Grupos de sprites
        self.player_group    = pygame.sprite.GroupSingle(self.player)
        self.player_bullets  = pygame.sprite.Group()
        self.enemy_bullets   = pygame.sprite.Group()
        self.explosions      = pygame.sprite.Group()

        # Estrellas de fondo (reutilizamos la misma lógica simple)
        self.stars = [
            [random.randint(0, SCREEN_WIDTH),
             random.randint(0, SCREEN_HEIGHT),
             random.uniform(0.3, 1.2),
             random.choice([1, 1, 2])]
            for _ in range(70)
        ]

    # ── Loop principal ──────────────────────────────────────────

    def update(self, sound) -> str | None:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'intro'

        keys = pygame.key.get_pressed()

        # Jugador
        self.player.update(keys)
        if keys[pygame.K_SPACE] and self.player.can_shoot():
            cx, ty = self.player.shoot()
            self.player_bullets.add(
                Bullet(cx, ty, color=CYAN, direction=-1)
            )
            sound.play('shoot')

        # Enemigos
        shot_enemies = self.enemies.update()
        for e in shot_enemies:
            self.enemy_bullets.add(
                Bullet(e.rect.centerx, e.rect.bottom,
                       color=RED, direction=1)
            )

        # Balas
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.explosions.update()

        # ── Colisiones bala jugador → enemigo ──
        hits = pygame.sprite.groupcollide(
            self.enemies.group, self.player_bullets,
            True, True
        )
        for enemy, _ in hits.items():
            self.player.score += enemy.points
            self.explosions.add(
                Explosion(enemy.rect.centerx, enemy.rect.centery)
            )
            sound.play('explode')

        # ── Colisiones bala enemiga → jugador ──
        if pygame.sprite.spritecollide(
                self.player, self.enemy_bullets, True):
            self.explosions.add(
                Explosion(self.player.rect.centerx,
                          self.player.rect.centery, size=36)
            )
            sound.play('explode')
            if not self.player.hit():
                return ('game_over', self.player.score)

        # ── Enemigos llegan al fondo ──
        if self.enemies.reached_bottom(SCREEN_HEIGHT - 40):
            return ('game_over', self.player.score)

        # ── Victoria: todos los enemigos eliminados ──
        if not self.enemies.group:
            self.player.score += POINTS_PER_LEVEL
            sound.play('levelup')
            return ('victory',
                    self.player.score,
                    self.level,
                    self.player.ship_index)

        return None

    # ── Dibujo ──────────────────────────────────────────────────

    def draw(self):
        self.screen.fill(BLACK)
        self._draw_stars()

        self.enemies.group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.explosions.draw(self.screen)

        self.hud.draw(
            self.player.score,
            self.player.lives,
            self.level,
            self.ship_data['color'],
            self.player.ship_index
        )

    def _draw_stars(self):
        for star in self.stars:
            star[1] += star[2]
            if star[1] > SCREEN_HEIGHT:
                star[0] = random.randint(0, SCREEN_WIDTH)
                star[1] = 0
            pygame.draw.rect(
                self.screen, WHITE,
                (int(star[0]), int(star[1]), star[3], star[3])
            )