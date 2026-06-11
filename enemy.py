"""Enemy class"""
from random import randint, choice
from typing import Tuple
import pygame
from entity import Entity


class Enemy(Entity):
    def __init__(
        self, rect: pygame.Rect, surface: pygame.Surface, category: str
    ):
        super().__init__(rect)
        self.category: str = category
        self.surface: pygame.Surface = surface
        self.speed: Tuple[float, float] = (0.0, 0.0)
        self.position: Tuple[float, float] = rect.topleft

    def enemy_restriction(self) -> bool:
        px, _ = self.position
        width = self.rect.size[0]
        return px + width < 0

    def display(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)

    def moving(self) -> bool:
        return self.speed != (0.0, 0.0)

    def run(self, speed: float) -> None:
        if self.category == "flyingMob":
            vy = choice([
                randint(int(-400 + speed * 0.3), int(-300 + speed * 0.3)),
                randint(int(-120 + speed * 0.1), int(100 + speed * 0.1)),
            ])
            self.change_speed((speed + speed * 0.05, vy))
        elif self.category == "heart":
            self.change_speed((speed + randint(0, 500), 0.0))
        elif self.category == "mediumMob":
            self.change_speed((speed + speed * 0.05, 0.0))
        else:
            self.change_speed((speed, 0.0))
