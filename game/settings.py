# game/settings.py
# Todas las constantes del juego en un solo lugar.
# Si quieres cambiar algo, solo tocas este archivo.

# ── Pantalla ──────────────────────────────────────────
SCREEN_WIDTH  = 480
SCREEN_HEIGHT = 640
TITLE         = "Stellar Defense"
FPS           = 60

# ── Colores (paleta retro de 8 bits) ──────────────────
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
CYAN       = (0,   255, 255)
YELLOW     = (255, 255, 0)
RED        = (255, 30,  30)
GREEN      = (0,   255, 80)
ORANGE     = (255, 140, 0)
PURPLE     = (180, 0,   255)
PINK       = (255, 80,  180)
DARK_BLUE  = (5,   5,   30)
GRAY       = (120, 120, 120)
NEON_GREEN = (57,  255, 20)

# ── Jugador ───────────────────────────────────────────
PLAYER_SPEED       = 5
PLAYER_LIVES       = 3
BULLET_SPEED       = 10
SHOOT_COOLDOWN     = 18        # frames entre disparos

# ── Enemigos ──────────────────────────────────────────
ENEMY_ROWS         = 4
ENEMY_COLS         = 8
ENEMY_SPEED_INIT   = 1.2
ENEMY_SPEED_INC    = 0.15      # aumenta por nivel
ENEMY_DROP         = 18        # píxeles que bajan al rebotar
ENEMY_SHOOT_CHANCE = 0.0008    # probabilidad por frame por enemigo

# ── Puntuación ────────────────────────────────────────
POINTS_PER_ENEMY   = 100
POINTS_PER_LEVEL   = 500

# ── Naves disponibles (selector) ──────────────────────
# Cada nave: nombre, color principal, color acento, descripción
SHIPS = [
    {
        "name":        "FALCON",
        "color":       CYAN,
        "accent":      WHITE,
        "description": "Balanceada. Buena para empezar.",
        "speed_bonus": 0,
        "fire_bonus":  0,
    },
    {
        "name":        "VIPER",
        "color":       GREEN,
        "accent":      NEON_GREEN,
        "description": "Más rápida. Disparo normal.",
        "speed_bonus": 2,
        "fire_bonus":  0,
    },
    {
        "name":        "BLAZE",
        "color":       ORANGE,
        "accent":      YELLOW,
        "description": "Disparo más rápido. Velocidad normal.",
        "speed_bonus": 0,
        "fire_bonus":  -6,
    },
    {
        "name":        "PHANTOM",
        "color":       PURPLE,
        "accent":      PINK,
        "description": "Veloz y disparo rápido. Difícil de manejar.",
        "speed_bonus": 3,
        "fire_bonus":  -5,
    },
    {
        "name":        "TITAN",
        "color":       RED,
        "accent":      ORANGE,
        "description": "Lenta pero devastadora.",
        "speed_bonus": -1,
        "fire_bonus":  -10,
    },
]