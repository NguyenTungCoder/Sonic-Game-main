"""Utility functions"""
from time import time
from typing import Tuple
import pygame


def animate_gif(
    delay: float, nb_images: int, time_gif: float, state: int
) -> Tuple[float, int]:
    delay_gif = time() - time_gif
    if delay_gif > delay:
        state += 1
        time_gif = time()
    if state >= nb_images:
        state = 0
    return time_gif, state


def play_sound(path: str, volume: float = 0.1) -> None:
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play()
    except pygame.error:
        pass
