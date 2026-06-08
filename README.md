<div align="center">

# 🚀 Stellar Defense

### A retro pixel-art arcade shooter built entirely in Python

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> Final project for **Stanford Code in Place 2026** — 6-week introductory Python course.

[Gameplay](#-gameplay) • [Features](#-features) • [Installation](#-installation) • [How to Play](#-how-to-play) • [Architecture](#-architecture) • [Author](#-author)

</div>

---

## 🎮 Gameplay

Stellar Defense is a retro arcade space shooter inspired by the classic games of the 80s and 90s.
Choose your ship, survive waves of alien enemies, and defend the galaxy — all rendered in pure pixel art
generated entirely through code, with no external image files.

---

## ✨ Features

- **5 playable ships** — each with unique speed and fire-rate stats
- **Pixel art sprites** drawn programmatically using matrix definitions (no image files)
- **8-bit sound effects** synthesized in pure Python (no audio files)
- **Animated starfield background** with parallax effect
- **Progressive difficulty** — enemies speed up with each level
- **Enemy formations** with classic left-right-drop movement (Space Invaders style)
- **Explosion animations** with multi-frame rendering
- **HUD** showing score, level, and remaining lives
- **Scene-based state machine** architecture (Intro → Select → Play → Victory/Game Over)

---

## 🛠 Installation

### Requirements

- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/stellar-defense.git
cd stellar-defense

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
python main.py
```

> **WSL users (Windows Subsystem for Linux):** make sure you have a display server running.
> The easiest option is to use Windows Terminal and run the game from there — WSL2 with WSLg
> supports GUI applications natively on Windows 11.

---

## 🎯 How to Play

### Controls

| Key | Action |
|-----|--------|
| `A` or `←` | Move left |
| `D` or `→` | Move right |
| `SPACE` | Shoot |
| `ENTER` | Confirm selection |
| `R` | Restart / Next level |
| `ESC` | Return to main menu |

### Game Flow

```
Main Menu  ──►  Ship Select  ──►  Gameplay
                                     │
                          ┌──────────┴──────────┐
                          ▼                     ▼
                       Victory              Game Over
                          │                     │
                    Next Level              Main Menu
```

### Ships

| Ship | Speed | Fire Rate | Description |
|------|-------|-----------|-------------|
| FALCON | ★★★☆☆ | ★★★☆☆ | Balanced. Great for beginners. |
| VIPER | ★★★★☆ | ★★★☆☆ | Faster movement. |
| BLAZE | ★★★☆☆ | ★★★★☆ | Rapid fire. |
| PHANTOM | ★★★★★ | ★★★★☆ | Fast and agile. Hard to control. |
| TITAN | ★★☆☆☆ | ★★★★★ | Slow but devastating firepower. |

### Scoring

| Event | Points |
|-------|--------|
| Destroy an enemy | +100 |
| Clear a level | +500 |

---

## 🏗 Architecture

```
stellar-defense/
│
├── main.py                  # Entry point
│
├── game/
│   ├── engine.py            # Main loop + scene state machine
│   ├── settings.py          # All constants (colors, speeds, ships)
│   │
│   ├── scenes/
│   │   ├── intro.py         # Title screen with animated starfield
│   │   ├── ship_select.py   # Ship selection with pixel art preview
│   │   ├── gameplay.py      # Core game logic + HUD
│   │   ├── game_over.py     # Defeat screen
│   │   └── victory.py       # Victory screen
│   │
│   ├── entities/
│   │   ├── player.py        # Player ship (movement, shooting, lives)
│   │   ├── enemy.py         # Enemy sprite + group movement logic
│   │   ├── bullet.py        # Player and enemy projectiles
│   │   └── explosion.py     # Multi-frame explosion animation
│   │
│   └── utils/
│       ├── pixel_art.py     # Sprite matrices + draw_sprite() function
│       └── sound.py         # Synthesized 8-bit sound effects
│
├── assets/
│   └── fonts/               # (reserved for future font assets)
│
├── requirements.txt
└── README.md
```

### Design Patterns Used

- **State Machine** — `engine.py` manages scene transitions cleanly
- **Single Source of Truth** — all constants centralized in `settings.py`
- **Entity-Component separation** — entities know nothing about scenes
- **Procedural asset generation** — sprites and sounds created in code, not loaded from files

---

## 📦 Dependencies

```
pygame==2.6.1
numpy==2.4.6
```

---

## 👤 Author

**Crisz Alba**
Stanford Code in Place 2026 — Final Project

---

## 📄 License

This project is licensed under the MIT License.
Feel free to use, modify, and distribute it freely.