# game/utils/sound.py

import pygame
import numpy as np
import array


def _generate_beep(frequency=440, duration=0.08, volume=0.3):
    """Genera un beep de onda cuadrada estilo 8-bit."""
    sample_rate = 44100
    n_samples   = int(sample_rate * duration)
    buf         = array.array('h', [0] * n_samples)
    for i in range(n_samples):
        t      = i / sample_rate
        val    = volume * 32767
        buf[i] = int(val if (t * frequency % 1) < 0.5 else -val)
    stereo = np.array(buf, dtype='int16').reshape(-1, 1).repeat(2, axis=1)
    return pygame.sndarray.make_sound(stereo)


class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._sounds = {}
        self._build()

    def _build(self):
        try:
            self._sounds['shoot']    = _generate_beep(880,  0.06, 0.2)
            self._sounds['explode']  = _generate_beep(110,  0.18, 0.4)
            self._sounds['select']   = _generate_beep(660,  0.08, 0.25)
            self._sounds['levelup']  = _generate_beep(1320, 0.15, 0.3)
            self._sounds['gameover'] = _generate_beep(165,  0.4,  0.4)
        except Exception:
            pass

    def play(self, name: str):
        s = self._sounds.get(name)
        if s:
            s.play()