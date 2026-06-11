"""Base entity class"""
from typing import Tuple
import pygame


class Entity:
    def __init__(self, rect: pygame.Rect):
        self.rect: pygame.Rect = rect
        self.speed: Tuple[float, float] = (0.0, 0.0)
        self.position: Tuple[float, float] = rect.topleft

    def change_speed(self, acceleration: Tuple[float, float]) -> None:
        ax, ay = acceleration
        sx, sy = self.speed
        self.speed = (sx + ax, sy + ay)

    def change_position(self, dt: float) -> None:
        sx, sy = self.speed
        px, py = self.position
        px -= sx * dt
        py -= sy * dt
        self.position = (px, py)
        self.rect.bottomleft = self.position
