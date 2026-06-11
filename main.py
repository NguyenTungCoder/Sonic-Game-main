"""Sonic Runner - Main Game"""
from random import randint, uniform
from time import time
from typing import Dict, List, Tuple

import pygame

from constants import (
    STATE_REGISTER, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER,
    STATE_HIGH_SCORES,
    INITIAL_HEALTH, MAX_HEALTH, JUMP_DURATION, GRAVITY_BASE,
    GROUND_OFFSET, SONIC_X,
    BASE_MOB_SPEED, MAX_ACCELERATION,
    FPS_LIMIT,
    DAMAGE_FLASH, HEAL_FLASH, GAME_OVER_WAIT,
    SHAKE_INTENSITY, SHAKE_DURATION,
    SCORE_SOUND_INTERVAL, SCORE_BIG_SOUND_INTERVAL,
    SCORE_PATH, SCORE1000_PATH, BESTSCORE_PATH, MAIN_MUSIC_PATH,
    JUMP_PATH, DAMAGE_PATH, HEALING_PATH, LOST_PATH,
)

from register import show_register_screen, save_scores
from variables import load_assets, Assets
from enemy import Enemy
from high_scores_screen import screen_scores
from functions import animate_gif, play_sound


class Game:
    def __init__(self) -> None:
        pygame.display.init()
        pygame.font.init()

        window_size = pygame.display.get_desktop_sizes()[0]
        self.screen: pygame.Surface = pygame.display.set_mode(window_size)
        self.width: int = window_size[0]
        self.height: int = window_size[1]
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.state: int = STATE_REGISTER
        self.running: bool = True

        # Player data
        self.player_name: str = ""
        self.scores: Dict[str, int] = {}
        self.best_score: int = 0

        # Game state
        self.score: int = 0
        self.last_score: int = 0
        self.best_score_beaten: bool = False
        self.lost: bool = True
        self.jumping: bool = False
        self.damage: bool = False
        self.healing: bool = False

        # Timers
        self.score_timer: float = time()
        self.start_jump: float = time()
        self.time_spawn: float = time()
        self.effect_time: float = time()
        self.time_score_sound: float = time()
        self.end_time: float = time() - GAME_OVER_WAIT
        self.best_score_time: float = time()

        # GIF state
        self.sonic_state: int = 0
        self.sonic_standing_state: int = 0
        self.duck_state: int = 0
        self.time_gif: float = time()
        self.time_gif_duck: float = time()

        # Entities
        self.enemies: List[Enemy] = []
        self.assets: Assets | None = None

        # Screen shake
        self.shake_time: float = 0.0
        self.shake_offset: Tuple[float, float] = (0.0, 0.0)

        # Mouse tracking for hover effects
        self.mouse_pos: Tuple[int, int] = (0, 0)

        # Register
        self._register()

    def _register(self) -> None:
        self.player_name, self.scores = show_register_screen(self.screen)
        if not self.player_name:
            self.running = False
            return

        if self.player_name in self.scores:
            self.best_score = self.scores[self.player_name]
        else:
            self.best_score = 0

        self.state = STATE_GAME_OVER
        self.lost = True
        self.end_time = time() - GAME_OVER_WAIT
        self.assets = load_assets(self.width, self.height)
        self.assets.set_volume(0.08)

        try:
            pygame.mixer.music.load(MAIN_MUSIC_PATH)
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    # ─── Event Handling ───────────────────────────────────────

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.running = False
            return

        if self.state == STATE_PLAYING and event.key == pygame.K_p:
            self.state = STATE_PAUSED
            return
        if self.state == STATE_PAUSED and event.key == pygame.K_p:
            self.state = STATE_PLAYING
            return

        if self.state in (STATE_PLAYING, STATE_GAME_OVER):
            if event.key == pygame.K_SPACE:
                can_jump = time() - self.end_time > GAME_OVER_WAIT
                if self.state == STATE_PLAYING and can_jump:
                    if self.assets and self.assets.sonic_jump_rect.on_floor():
                        self.start_jump = time()
                        self.jumping = True
                        acceleration = min(self.score / 2, MAX_ACCELERATION)
                        self.assets.sonic_jump_rect.change_speed(
                            (0, GRAVITY_BASE - acceleration / 2.5)
                        )
                        if time() - self.best_score_time > 0.5:
                            play_sound(JUMP_PATH, 0.02)
                elif self.state == STATE_GAME_OVER and can_jump:
                    self._restart_game()

    def _handle_keyup(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_SPACE and self.jumping:
            if self.assets:
                acceleration = min(self.score / 2, MAX_ACCELERATION)
                fall = 500 if acceleration > 500 else acceleration
                self.assets.sonic_jump_rect.change_speed(
                    (0, -500 - fall / 1.3)
                )

    def _handle_click(self, pos: Tuple[int, int]) -> None:
        if self.state == STATE_GAME_OVER:
            w = self.width
            end_surf = self.assets.end_font.render("CLOSE", True, (0, 0, 0)) if self.assets else None
            if end_surf:
                end_rect = end_surf.get_rect(topright=(w - 10, 10))
                scores_surf = self.assets.end_font.render("HIGHSCORES", True, (0, 0, 0))
                scores_rect = scores_surf.get_rect(topright=(w - 10, 75))

                if end_rect.collidepoint(pos):
                    self.running = False
                elif scores_rect.collidepoint(pos):
                    self.state = STATE_HIGH_SCORES

        elif self.state == STATE_HIGH_SCORES:
            self.state = STATE_GAME_OVER

    # ─── Game Logic ───────────────────────────────────────────

    def _restart_game(self) -> None:
        self.lost = False
        self.score = 0
        self.best_score_beaten = False
        self.enemies.clear()
        self.jumping = False
        self.score_timer = time()
        self.time_spawn = time()
        self.effect_time = time()
        if self.assets:
            self.assets.sonic_1_rect.health = INITIAL_HEALTH
        self.end_time = time() - GAME_OVER_WAIT
        self.state = STATE_PLAYING

    def _update_score(self) -> None:
        if not self.lost and self.state == STATE_PLAYING:
            self.score = int(round((time() - self.score_timer) * 10, 0))
            if self.score > self.best_score:
                self.best_score = self.score
                if not self.best_score_beaten:
                    play_sound(BESTSCORE_PATH, 0.05)
                    self.best_score_time = time()
                self.best_score_beaten = True

    def _spawn_enemies(self) -> None:
        if self.lost or self.state != STATE_PLAYING:
            return

        acceleration = min(self.score / 2, MAX_ACCELERATION)
        mobs_speed = BASE_MOB_SPEED + acceleration
        delay = 150 * 4.8 / mobs_speed

        if time() < self.time_spawn + delay + uniform(-0.05, 0.7):
            return

        if not self.assets:
            return

        self.time_spawn = time()
        a = self.assets
        w, h = self.width, self.height

        rand = randint(1, 10)
        ground = h - GROUND_OFFSET

        if rand <= 7:
            if rand <= 2:
                self.enemies.append(Enemy(
                    a.rock.get_rect(topleft=(w, ground)),
                    a.rock, "littleMob",
                ))
            elif rand <= 4:
                self.enemies.append(Enemy(
                    a.duck_frames[self.duck_state].get_rect(topleft=(w, ground)),
                    a.duck_frames[self.duck_state], "mediumMob",
                ))
            else:
                self.enemies.append(Enemy(
                    a.enemy_spike.get_rect(topleft=(w, ground)),
                    a.enemy_spike, "bigMob",
                ))
        else:
            self.enemies.append(Enemy(
                a.enemy_bird.get_rect(topleft=(w, 300)),
                a.enemy_bird, "flyingMob",
            ))

        # Heart spawning
        if a.sonic_1_rect.health < MAX_HEALTH:
            check_hearts = sum(1 for e in self.enemies if e.category == "heart")
            if check_hearts < 2:
                heart_chance = {
                    1: 25, 2: 55, 3: 100, 4: 200,
                }.get(a.sonic_1_rect.health, 200)
                if randint(1, heart_chance) == 1:
                    self.enemies.append(Enemy(
                        a.heart.get_rect(topleft=(w, h - randint(200, 700))),
                        a.heart, "heart",
                    ))

    def _update_enemies(self, dt: float) -> None:
        if not self.assets:
            return

        a = self.assets
        acceleration = min(self.score / 2, MAX_ACCELERATION)
        mobs_speed = BASE_MOB_SPEED + acceleration
        to_remove: List[int] = []

        for i, enemy in enumerate(self.enemies):
            if not enemy.moving():
                enemy.run(mobs_speed)
            enemy.change_position(dt)

            if enemy.rect.colliderect(a.sonic_jump_rect.rect):
                if enemy.category == "heart":
                    if a.sonic_1_rect.health < MAX_HEALTH:
                        a.sonic_1_rect.health += 1
                    self.healing = True
                    self.effect_time = time()
                    play_sound(HEALING_PATH, 0.1)
                    to_remove.append(i)
                elif enemy.category != "heart":
                    a.sonic_1_rect.health -= 1
                    self.damage = True
                    self.effect_time = time()
                    self.shake_time = time()
                    play_sound(DAMAGE_PATH, 0.1)
                    to_remove.append(i)
            elif enemy.enemy_restriction():
                to_remove.append(i)

        for i in reversed(to_remove):
            if i < len(self.enemies):
                self.enemies.pop(i)

    def _check_game_over(self) -> None:
        if not self.assets:
            return
        if self.assets.sonic_1_rect.health <= 0:
            self.enemies.clear()
            self.lost = True
            self.best_score_beaten = False
            self.last_score = self.score
            self.assets.sonic_1_rect.health = INITIAL_HEALTH
            play_sound(LOST_PATH, 0.06)
            self.end_time = time()
            self.scores[self.player_name] = self.best_score
            save_scores(self.scores)
            self.state = STATE_GAME_OVER

    # ─── Rendering ────────────────────────────────────────────

    def _update_shake(self) -> None:
        if time() - self.shake_time < SHAKE_DURATION:
            self.shake_offset = (
                randint(-SHAKE_INTENSITY, SHAKE_INTENSITY),
                randint(-SHAKE_INTENSITY, SHAKE_INTENSITY),
            )
        else:
            self.shake_offset = (0.0, 0.0)

    def _render(self, dt: float) -> None:
        if not self.assets:
            return

        a = self.assets
        w, h = self.width, self.height
        ground = h - GROUND_OFFSET
        acceleration = min(self.score / 2, MAX_ACCELERATION)
        mobs_speed = BASE_MOB_SPEED + acceleration

        if not self.lost:
            self._update_shake()
            offset_x, offset_y = self.shake_offset
        else:
            offset_x, offset_y = 0.0, 0.0

        # Background
        effect_delay = time() - self.effect_time
        if self.damage and effect_delay < DAMAGE_FLASH:
            self.screen.fill((255, 100, 100))
        elif self.healing and effect_delay < HEAL_FLASH:
            self.screen.fill((100, 255, 100))
        else:
            self.screen.fill((135, 206, 235))
            self.effect_time = time()
            self.damage = False
            self.healing = False

        # Environment
        if not self.lost:
            a.grass_rect.animate(mobs_speed, 0, dt, self.screen)
            a.grass_2_rect.animate(mobs_speed, 0, dt, self.screen)
            a.grass_3_rect.animate(mobs_speed, 0, dt, self.screen)
            a.cloud_rect.animate(620, 0, dt, self.screen)
            a.cloud_2_rect.animate(550, 0, dt, self.screen)
            a.palm_rect.animate(475, 0, dt, self.screen)
            a.palm_2_rect.animate(475, 0, dt, self.screen)
        else:
            a.cloud_rect.animate(160, 0, dt, self.screen)
            a.cloud_2_rect.animate(70, 0, dt, self.screen)
            a.palm_rect.position = (w // 4, ground)
            a.palm_2_rect.position = (int(w / 1.3), ground)
            a.palm_rect.animate(0, 0, dt, self.screen)
            a.palm_2_rect.animate(0, 0, dt, self.screen)

        # Enemies
        if not self.lost:
            for enemy in self.enemies:
                if enemy.category != "mediumMob":
                    enemy.display(self.screen)
                else:
                    self.screen.blit(a.duck_frames[self.duck_state], enemy.rect)
                    self.time_gif_duck, self.duck_state = animate_gif(
                        0.08, 2, self.time_gif_duck, self.duck_state
                    )

        # Score text
        if not self.lost:
            color = (255, 195, 36) if self.best_score_beaten else (0, 0, 0)
            score_surface = a.score_live_font.render(str(self.score), True, color)
            score_rect = score_surface.get_rect(topright=(w, 10))
            self.screen.blit(score_surface, score_rect)

        # Game over UI
        elapsed_end = time() - self.end_time
        if self.lost and elapsed_end >= GAME_OVER_WAIT:
            mx, my = self.mouse_pos
            end_surface = a.end_font.render("CLOSE", True, (0, 0, 0))
            end_rect = end_surface.get_rect(topright=(w - 10, 10))
            scores_surface = a.end_font.render("HIGHSCORES", True, (0, 0, 0))
            scores_rect = scores_surface.get_rect(topright=(w - 10, 75))
            end_hover = end_rect.collidepoint(mx, my)
            scores_hover = scores_rect.collidepoint(mx, my)
            if end_hover:
                end_surface = a.end_font.render("CLOSE", True, (255, 60, 60))
            if scores_hover:
                scores_surface = a.end_font.render("HIGHSCORES", True, (255, 60, 60))
            last_surface = a.score_font.render(
                f"Last score : {self.last_score}", True, (0, 0, 0)
            )
            last_rect = last_surface.get_rect(midtop=(w // 2, 100))
            best_surface = a.score_font.render(
                f"Best score : {self.best_score}", True, (0, 0, 0)
            )
            best_rect = best_surface.get_rect(midtop=(w // 2, 25))
            pseudo_surface = a.score_font.render(self.player_name, True, (0, 0, 0))
            pseudo_rect = pseudo_surface.get_rect(topleft=(30, 30))

            self.screen.blit(end_surface, end_rect)
            self.screen.blit(scores_surface, scores_rect)
            self.screen.blit(last_surface, last_rect)
            self.screen.blit(best_surface, best_rect)
            self.screen.blit(pseudo_surface, pseudo_rect)

        # Health hearts
        if not self.lost:
            for i in range(a.sonic_1_rect.health):
                pos = (a.heart_rect[0] + i * 100 + offset_x,
                       a.heart_rect[1] + offset_y)
                self.screen.blit(a.heart, pos)

        # Sonic rendering
        self._render_sonic(dt, mobs_speed)

        # Score sounds
        if not self.lost and self.score > 0:
            if self.score % SCORE_SOUND_INTERVAL == 0 and self.score % SCORE_BIG_SOUND_INTERVAL != 0:
                if time() - self.time_score_sound > 0.2:
                    play_sound(SCORE_PATH, 0.03)
                    self.time_score_sound = time()
            elif self.score % SCORE_BIG_SOUND_INTERVAL == 0:
                if time() - self.time_score_sound > 0.2:
                    play_sound(SCORE1000_PATH, 0.05)
                    self.time_score_sound = time()

        # Pause overlay
        if self.state == STATE_PAUSED:
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            pause_surf = a.big_font.render("PAUSED", True, (255, 255, 255))
            pause_rect = pause_surf.get_rect(center=(w // 2, h // 2))
            self.screen.blit(pause_surf, pause_rect)
            hint_surf = a.score_font.render("Press P to resume", True, (200, 200, 200))
            hint_rect = hint_surf.get_rect(center=(w // 2, h // 2 + 80))
            self.screen.blit(hint_surf, hint_rect)

        pygame.display.flip()

    def _render_sonic(self, dt: float, mobs_speed: float) -> None:
        if not self.assets:
            return
        a = self.assets
        ground = self.height - GROUND_OFFSET

        # Jump logic
        if time() - self.start_jump < JUMP_DURATION:
            a.sonic_jump_rect.change_position(dt)
        else:
            acceleration = min(self.score / 2, MAX_ACCELERATION)
            a.sonic_jump_rect.change_speed((0, -GRAVITY_BASE - acceleration))
            self.start_jump = time()

        a.sonic_jump_rect.sonic_pos_restriction(a.sonic_zone)

        if a.sonic_jump_rect.speed[1] == 0:
            self.jumping = False
        if a.sonic_jump_rect.speed[1] < 0:
            a.sonic_jump_rect.change_speed((0, -50))

        if self.jumping and not self.lost:
            a.sonic_jump_rect.change_speed((0, -3))
            offset_x, offset_y = self.shake_offset if not self.lost else (0, 0)
            self.screen.blit(a.sonic_jump,
                             (a.sonic_jump_rect.rect.x + offset_x,
                              a.sonic_jump_rect.rect.y + offset_y))
        elif not self.lost:
            y_pos = ground - a.sonic_frames[0].get_height()
            self.screen.blit(a.sonic_frames[self.sonic_state], (SONIC_X, y_pos))
            speed_gif = 0.2 - mobs_speed / 2000 if mobs_speed < 300 else 0.07
            self.time_gif, self.sonic_state = animate_gif(
                speed_gif, 4, self.time_gif, self.sonic_state
            )
        elif self.lost:
            if time() - self.end_time < GAME_OVER_WAIT:
                self.screen.fill((255, 255, 255))
                go_surf = a.score_live_font.render("GAME OVER", True, (0, 0, 0))
                go_rect = go_surf.get_rect(
                    center=(self.width // 2, self.height // 2)
                )
                self.screen.blit(go_surf, go_rect)
            else:
                self.screen.blit(
                    a.sonic_standing_frames[self.sonic_standing_state],
                    (SONIC_X, ground - 248),
                )
                restart_surf = a.big_font.render(
                    "PRESS SPACE TO START", True, (255, 10, 10)
                )
                restart_rect = restart_surf.get_rect(
                    midtop=(self.width // 2, self.height // 2)
                )
                self.screen.blit(restart_surf, restart_rect)
                self.time_gif, self.sonic_standing_state = animate_gif(
                    0.3, 2, self.time_gif, self.sonic_standing_state
                )
                self.screen.blit(
                    a.grass,
                    a.grass.get_rect(topright=(self.width, ground)),
                )
                self.screen.blit(
                    a.grass,
                    a.grass.get_rect(topleft=(0, ground)),
                )

    # ─── Game Loop ────────────────────────────────────────────

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS_LIMIT) / 1000.0
            self._handle_events()
            if not self.running:
                break

            if self.state == STATE_HIGH_SCORES:
                if self.assets:
                    result = screen_scores(
                        self.screen, self.scores, self.width, self.height
                    )
                    if not result:
                        self.running = False
                        break
                self.state = STATE_GAME_OVER

            if self.state == STATE_PAUSED:
                self._render(dt)
                continue

            if self.state == STATE_PLAYING:
                self._update_score()
                self._spawn_enemies()
                self._update_enemies(dt)
                self._check_game_over()

            self._render(dt)

        pygame.display.quit()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
