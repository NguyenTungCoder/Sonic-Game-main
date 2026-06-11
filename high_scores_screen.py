"""High scores screen"""
from typing import Dict, List, Tuple
import pygame

from constants import FONT_PATH


def draw_scores(
    screen: pygame.Surface,
    scores: Dict[str, int],
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    width: int,
    height: int,
) -> None:
    sorted_scores: List[Tuple[str, int]] = sorted(
        scores.items(), key=lambda x: x[1], reverse=True
    )[:5]

    for ctr, (key, value) in enumerate(sorted_scores):
        gold_colors = [
            (255, 215, 0),
            (192, 192, 192),
            (97, 78, 26),
        ]
        color = gold_colors[ctr] if ctr < 3 else (0, 0, 0)

        ctr_surface = big_font.render(str(ctr + 1), True, color)
        ctr_rect = ctr_surface.get_rect(
            topleft=(15, int(height / 6.5 * ctr + height / 4.5))
        )

        id_surface = big_font.render(key, True, (0, 0, 0))
        id_rect = id_surface.get_rect(
            topleft=(111, int(height / 6.5 * ctr + height / 4.5))
        )

        score_surface = big_font.render(str(value), True, (0, 0, 0))
        score_rect = score_surface.get_rect(
            topright=(width - 15, int(height / 6.5 * ctr + height / 4.5))
        )

        screen.blit(ctr_surface, ctr_rect)
        screen.blit(id_surface, id_rect)
        screen.blit(score_surface, score_rect)


def screen_scores(
    screen: pygame.Surface,
    scores: Dict[str, int],
    width: int,
    height: int,
    looping: bool = True,
) -> bool:
    font = pygame.font.Font(FONT_PATH, width // 30)
    big_font = pygame.font.Font(FONT_PATH, 80)

    exit_surface = big_font.render("EXIT", True, (0, 0, 0))
    exit_rect = exit_surface.get_rect(topleft=(10, 10))

    while looping:
        screen.fill((150, 150, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                hover = exit_rect.collidepoint(event.pos)
                exit_surface = big_font.render(
                    "EXIT", True, (255, 60, 60) if hover else (0, 0, 0)
                )
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_rect.collidepoint(event.pos):
                    looping = False

        screen.blit(exit_surface, exit_rect)
        draw_scores(screen, scores, font, big_font, width, height)
        pygame.display.flip()

    return True
