# game/utils/sound.py

import pygame
import numpy as np
import array


def _generate_beep(frequency=440, duration=0.08, volume=0.3):
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
        self._muted  = False
        self._build()

    def _build(self):
        try:
            # Volumen reducido a la mitad vs antes
            self._sounds['shoot']    = _generate_beep(880,  0.05, 0.08)
            self._sounds['explode']  = _generate_beep(150,  0.12, 0.15)
            self._sounds['select']   = _generate_beep(660,  0.07, 0.10)
            self._sounds['levelup']  = _generate_beep(1320, 0.12, 0.12)
            self._sounds['gameover'] = _generate_beep(165,  0.35, 0.15)
        except Exception:
            pass

    def toggle_mute(self):
        self._muted = not self._muted
        pygame.mixer.set_num_channels(0 if self._muted else 8)

    def is_muted(self) -> bool:
        return self._muted

    def play(self, name: str):
        if self._muted:
            return
        s = self._sounds.get(name)
        if s:
            # stop evita que se apilen instancias del mismo sonido
            s.stop()
            s.play()