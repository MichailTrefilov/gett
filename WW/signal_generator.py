import numpy as np
import time


def get_sin_wave_amplitude(freq, time):
    """Синус, сдвинутый вверх и нормированный: значения от 0 до 1."""
    return (np.sin(2 * np.pi * freq * time) + 1) / 2


def get_triangle_wave_amplitude(freq, time):
    """Треугольник: значения от 0 до 1 (0 -> 1 -> 0 за один период)."""
    phase = (freq * time) % 1
    return 1 - abs(2 * phase - 1)


def wait_for_sampling_period(sampling_frequency):
    time.sleep(1 / sampling_frequency)
