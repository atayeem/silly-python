import cmath as cm
import numpy as np
import sounddevice as sd
from time import sleep

import random

def apply_fade(wave: np.ndarray, sample_rate=44100, fade_time=0.01):  # 10ms fade
    n = len(wave)
    fade_samples = int(sample_rate * fade_time)
    
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    wave[:fade_samples] *= fade_in
    wave[-fade_samples:] *= fade_out
    return wave

def play_note(frequency: complex, duration=0.5, sample_rate=44100):
    left_fundamental = abs(frequency.real)
    right_fundamental = abs(frequency.imag)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Relative amplitudes of harmonics
    amplitudes = [1.0, 0.6, 0.4, 0.3, 0.2, 0.15, 0.1, 0.07, 0.05, 0.03]
    
    # How fast each harmonic decays
    decay_rates = [2, 3, 4, 5, 6, 7, 9, 11, 13, 15]

    left_wave = np.zeros_like(t)
    right_wave = np.zeros_like(t)

    for i, (amp, decay_rate) in enumerate(zip(amplitudes, decay_rates)):
        n = i + 1  # nth harmonic
        envelope = np.exp(-decay_rate * t)
        left_wave += amp * envelope * np.sin(2 * np.pi * left_fundamental * n * t)
        right_wave += amp * envelope * np.sin(2 * np.pi * right_fundamental * n * t)

    # Normalize
    if left_fundamental > 0:
        left_wave *= 0.3 / np.max(np.abs(left_wave))
    if right_fundamental > 0:
        right_wave *= 0.3 / np.max(np.abs(right_wave))

    left_wave = apply_fade(left_wave)
    right_wave = apply_fade(right_wave)
    stereo = np.column_stack((left_wave, right_wave))
    sd.play(stereo, samplerate=sample_rate)
    sd.wait()

class Scale:
    def __init__(self, edo: int, start: float):
        self.edo = edo
        self.start = start
    
    def __call__(self, mag: int, rot: int):
        """
        Returns magnitude\\edo rotated by rotation * tau / edo
        """
        return self.start * 2 ** (mag / self.edo) * cm.exp(1j * rot * (cm.tau / self.edo))

freq = Scale(edo=5, start=220.0)

music = [
    (0, 5, 0.25),
    (1, 4, 0.25),
    (2, 3, 0.25),
    (3, 2, 0.25),
    (4, 1, 0.50),
    (5, 0, 1.00),
    (4, 1, 0.25),
    (3, 1, 0.25),
    (2, 1, 0.25),
    (1, 1, 0.25),
    (0, 1, 0.75),
    (2, 1, 0.25),
    (3, 2, 0.50),
    (2, 2, 0.25),
    (1, 2, 0.25),
    (0, 3, 0.25),
    (1, 3, 0.50),
    (0, 3, 1.25),
]

for note, rotation, duration in music:
    play_note(freq(note, rotation), duration)