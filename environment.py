"""Environment background elements"""
from random import randint
from typing import Tuple
import pygame
from entity import Entity

height: int = 0
width: int = 0


def set_screen_dimensions(w: int, h: int) -> None:
    global width, height
    width = w
    height = h


class Environment(Entity):
    def __init__(
        self, rect: pygame.Rect, surface: pygame.Surface, category: str
    ):
        super().__init__(rect)
        self.surface: pygame.Surface = surface
        self.category: str = category
        self.speed: Tuple[float, float] = (0.0, 0.0)
        self.position: Tuple[float, float] = rect.topleft

    def loop(self) -> bool:
        px, _ = self.position
        return px + self.rect.size[0] < 0

    def get_rand_pos(self) -> Tuple[int, int]:
        if self.category in ("cloud1", "palm1"):
            rand_x = randint(0, 500)
            rand_y = height - 200 if self.category == "palm1" else randint(200, height // 2)
        elif self.category in ("cloud2", "palm2"):
            rand_x = randint(1000, 2500)
            rand_y = height - 200 if self.category == "palm2" else randint(200, height // 2)
        else:
            rand_x, rand_y = 0, 0
        return rand_x, rand_y

    def animate(
        self, speed_x: float, speed_y: float, dt: float, screen: pygame.Surface
    ) -> None:
        self.speed = (speed_x, speed_y)
        if self.loop():
            if self.category == "grass":
                self.position = (width, height)
            else:
                self.position = (
                    width + self.get_rand_pos()[0],
                    self.get_rand_pos()[1],
                )
        self.change_position(dt)
        screen.blit(self.surface, self.rect)
