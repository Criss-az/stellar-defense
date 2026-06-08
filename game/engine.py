# game/engine.py
# Máquina de estados: conecta todas las escenas.

import pygame
from game.settings        import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from game.utils.sound     import SoundManager
from game.scenes.intro    import IntroScene
from game.scenes.ship_select import ShipSelectScene
from game.scenes.gameplay import GameplayScene
from game.scenes.game_over import GameOverScene
from game.scenes.victory  import VictoryScene


class Engine:
    """
    Controla el loop principal y las transiciones entre escenas.
    Estado inicial: 'intro'
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.sound  = SoundManager()
        self.state  = 'intro'
        self.scene  = IntroScene(self.screen)

        # Persistencia entre escenas
        self.ship_index = 0
        self.level      = 1

    # ── Loop ────────────────────────────────────────────────────

    def run(self):
        while True:
            result = self.scene.update(
            ) if not isinstance(self.scene, GameplayScene) \
              else self.scene.update(self.sound)

            if result:
                self._transition(result)

            self.scene.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── Transiciones ────────────────────────────────────────────

    def _transition(self, result):
        # Normalizar resultado a tupla
        if isinstance(result, str):
            action = result
            args   = ()
        else:
            action = result[0]
            args   = result[1:]

        if action == 'quit':
            pygame.quit()
            raise SystemExit

        elif action == 'intro':
            self.level = 1
            self.scene = IntroScene(self.screen)

        elif action == 'select':
            self.scene = ShipSelectScene(self.screen)

        elif action == 'play':
            self.ship_index = args[0]
            self.scene = GameplayScene(
                self.screen, self.ship_index, self.level
            )

        elif action == 'game_over':
            score = args[0] if args else 0
            self.level = 1
            self.scene = GameOverScene(self.screen, score)

        elif action == 'victory':
            score, level, ship_idx = args
            self.ship_index = ship_idx
            self.scene = VictoryScene(self.screen, score, level)

        elif action == 'next_level':
            self.level += 1
            self.scene = GameplayScene(
                self.screen, self.ship_index, self.level
            )