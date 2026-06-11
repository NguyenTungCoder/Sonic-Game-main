"""Sonic player class"""
import pygame
from entity import Entity
import environment


class Sonic(Entity):
    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)
        self.health: int = 3
        self.speed: tuple[float, float] = (0.0, 0.0)
        self.position: tuple[float, float] = rect.topleft

    def sonic_pos_restriction(self, zone: pygame.Rect) -> None:
        px, py = self.position
        h = self.rect.size[1]
        if py + h > zone.bottom:
            py = zone.bottom - h
            self.speed = (0.0, 0.0)
        if py < zone.top:
            py = zone.top
        self.position = (px, py)
        self.rect.topleft = self.position

    def on_floor(self) -> bool:
        return abs(self.position[1] - (environment.height - 200 - 144)) < 2
