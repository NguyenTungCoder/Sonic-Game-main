"""Registration screen"""
import pickle
from time import time
from typing import Dict, Tuple
import pygame

from constants import FONT_PATH, SCORES_FILE


def show_register_screen(screen: pygame.Surface) -> Tuple[str, Dict[str, int]]:
    width = screen.get_width()
    height = screen.get_height()

    name_id = ""
    logging = True
    font = pygame.font.Font(FONT_PATH, width // 30)
    big_font = pygame.font.Font(FONT_PATH, 80)

    name_surface = big_font.render(name_id, True, (0, 0, 0))
    name_rect = name_surface.get_rect(midtop=(width // 2, height // 2))
    text_surface = font.render("Press RETURN to continue", True, (0, 0, 0))
    text_rect = text_surface.get_rect(midtop=(width // 2, 50))
    cursor_surface = font.render("-", True, (50, 50, 50))
    cursor_rect = cursor_surface.get_rect(topleft=name_rect.topright)

    while logging:
        cursor_rect = cursor_surface.get_rect(topleft=name_rect.topright)
        screen.fill((150, 150, 150))
        name_surface = font.render(name_id, True, (0, 0, 0))
        name_rect = name_surface.get_rect(midtop=(width // 2, height // 2))
        screen.blit(name_surface, name_rect)

        if int(time() * 2.2) % 2 == 0 and len(name_id) < 20:
            screen.blit(cursor_surface, cursor_rect)

        if name_id:
            screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "", {}
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() or event.unicode.isnumeric():
                    if len(name_id) < 20:
                        name_id += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name_id = name_id[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if name_id:
                        logging = False

        pygame.display.flip()

    try:
        with open(SCORES_FILE, "rb") as f:
            scores: Dict[str, int] = pickle.load(f)
    except (EOFError, FileNotFoundError):
        scores = {}

    return name_id, scores


def save_scores(scores: Dict[str, int]) -> None:
    with open(SCORES_FILE, "wb") as f:
        pickle.dump(scores, f)
