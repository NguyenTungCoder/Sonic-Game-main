"""Asset loading and game state initialization"""
from dataclasses import dataclass, field
from typing import Dict, List
import pygame

from constants import (
    SONIC_FRAMES,
    SONIC_STANDING_FRAMES,
    DUCK_FRAMES,
    SPIKE_IMAGE,
    BIRD_IMAGE,
    ROCK_IMAGE,
    SONIC_JUMP_IMAGE,
    HEART_IMAGE,
    GRASS_IMAGE,
    CLOUD_IMAGE,
    PALM_IMAGE,
    PALM2_IMAGE,
    FONT_PATH,
    GROUND_OFFSET,
    JUMP_PATH,
    DAMAGE_PATH,
    HEALING_PATH,
    LOST_PATH,
    SCORE_PATH,
    SCORE1000_PATH,
)
from environment import Environment, set_screen_dimensions
from sonic import Sonic


@dataclass
class Assets:
    # Surfaces
    sonic_frames: List[pygame.Surface]
    sonic_standing_frames: List[pygame.Surface]
    duck_frames: List[pygame.Surface]
    enemy_spike: pygame.Surface
    enemy_bird: pygame.Surface
    rock: pygame.Surface
    sonic_jump: pygame.Surface
    heart: pygame.Surface
    grass: pygame.Surface
    cloud: pygame.Surface
    palm: pygame.Surface
    palm2: pygame.Surface

    # Environment entities
    grass_rect: Environment
    grass_2_rect: Environment
    grass_3_rect: Environment
    cloud_rect: Environment
    cloud_2_rect: Environment
    palm_rect: Environment
    palm_2_rect: Environment

    # Player
    sonic_jump_rect: Sonic
    sonic_1_rect: Sonic
    sonic_zone: pygame.Rect

    # Fonts
    score_font: pygame.font.Font
    big_font: pygame.font.Font
    score_live_font: pygame.font.Font
    end_font: pygame.font.Font

    # UI surfaces
    heart_rect: pygame.Rect

    # Sounds
    jump_sound: pygame.mixer.Sound = field(repr=False)
    damage_sound: pygame.mixer.Sound = field(repr=False)
    healing_sound: pygame.mixer.Sound = field(repr=False)
    lost_sound: pygame.mixer.Sound = field(repr=False)
    score_sound: pygame.mixer.Sound = field(repr=False)
    best_score_sound: pygame.mixer.Sound = field(repr=False)

    def set_volume(self, vol: float = 0.1) -> None:
        for s in [self.jump_sound, self.damage_sound, self.healing_sound,
                  self.lost_sound, self.score_sound, self.best_score_sound]:
            s.set_volume(vol)


def load_assets(width: int, height: int) -> Assets:
    set_screen_dimensions(width, height)
    ground_y = height - GROUND_OFFSET

    def load_img(path: str) -> pygame.Surface:
        return pygame.image.load(path).convert_alpha()

    # ---- Surfaces ----
    sonic_frames = [load_img(p) for p in SONIC_FRAMES]
    sonic_standing_frames = [load_img(p) for p in SONIC_STANDING_FRAMES]
    duck_frames = [load_img(p) for p in DUCK_FRAMES]

    spike_surf = load_img(SPIKE_IMAGE)
    bird_surf = load_img(BIRD_IMAGE)
    rock_surf = load_img(ROCK_IMAGE)
    jump_surf = load_img(SONIC_JUMP_IMAGE)
    heart_surf = load_img(HEART_IMAGE)
    grass_surf = load_img(GRASS_IMAGE)
    cloud_surf = load_img(CLOUD_IMAGE)
    palm_surf = load_img(PALM_IMAGE)
    palm2_surf = load_img(PALM2_IMAGE)

    # ---- Environment ----
    grass_rect = Environment(
        grass_surf.get_rect(topleft=(0, height)), grass_surf, "grass"
    )
    grass_2_rect = Environment(
        grass_surf.get_rect(topleft=(width, height)), grass_surf, "grass"
    )
    grass_3_rect = Environment(
        grass_surf.get_rect(topleft=(width // 2, height)), grass_surf, "grass"
    )
    from random import randint
    cloud_rect = Environment(
        cloud_surf.get_rect(topleft=(width + randint(0, 500), randint(200, height // 2))),
        cloud_surf, "cloud1",
    )
    cloud_rect.speed = (620, 0)
    cloud_2_rect = Environment(
        cloud_surf.get_rect(topleft=(width + randint(0, 500), randint(200, height // 2))),
        cloud_surf, "cloud2",
    )
    cloud_2_rect.speed = (550, 0)
    palm_rect = Environment(
        palm_surf.get_rect(topleft=(width + randint(0, 500), ground_y)),
        palm_surf, "palm1",
    )
    palm_rect.speed = (475, 0)
    palm_2_rect = Environment(
        palm2_surf.get_rect(topleft=(width + randint(1000, 2500), ground_y)),
        palm2_surf, "palm2",
    )
    palm_2_rect.speed = (475, 0)

    # ---- Player ----
    sonic_jump_rect = Sonic(
        jump_surf.get_rect(topleft=(100, ground_y - 144 * 4))
    )
    sonic_1_rect = Sonic(
        sonic_frames[0].get_rect(topleft=(100, ground_y - 144))
    )
    sonic_zone = pygame.Rect((100, 200), (128, height - 400))

    # ---- Fonts ----
    score_font = pygame.font.Font(FONT_PATH, 40)
    big_font = pygame.font.Font(FONT_PATH, width // 30)
    score_live_font = pygame.font.Font(FONT_PATH, 150)
    end_font = pygame.font.Font(FONT_PATH, 50)

    # ---- UI Rects ----
    heart_rect = heart_surf.get_rect(topleft=(65, 65))

    # ---- Sounds ----
    pygame.mixer.init()
    jump_sound = pygame.mixer.Sound(JUMP_PATH)
    damage_sound = pygame.mixer.Sound(DAMAGE_PATH)
    healing_sound = pygame.mixer.Sound(HEALING_PATH)
    lost_sound = pygame.mixer.Sound(LOST_PATH)
    score_sound = pygame.mixer.Sound(SCORE_PATH)
    best_score_sound = pygame.mixer.Sound(SCORE1000_PATH)

    return Assets(
        sonic_frames=sonic_frames,
        sonic_standing_frames=sonic_standing_frames,
        duck_frames=duck_frames,
        enemy_spike=spike_surf,
        enemy_bird=bird_surf,
        rock=rock_surf,
        sonic_jump=jump_surf,
        heart=heart_surf,
        grass=grass_surf,
        cloud=cloud_surf,
        palm=palm_surf,
        palm2=palm2_surf,
        grass_rect=grass_rect,
        grass_2_rect=grass_2_rect,
        grass_3_rect=grass_3_rect,
        cloud_rect=cloud_rect,
        cloud_2_rect=cloud_2_rect,
        palm_rect=palm_rect,
        palm_2_rect=palm_2_rect,
        sonic_jump_rect=sonic_jump_rect,
        sonic_1_rect=sonic_1_rect,
        sonic_zone=sonic_zone,
        score_font=score_font,
        big_font=big_font,
        score_live_font=score_live_font,
        end_font=end_font,
        heart_rect=heart_rect,
        jump_sound=jump_sound,
        damage_sound=damage_sound,
        healing_sound=healing_sound,
        lost_sound=lost_sound,
        score_sound=score_sound,
        best_score_sound=best_score_sound,
    )
