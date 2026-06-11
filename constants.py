"""Game constants and configuration"""
from typing import Final

# Game states
STATE_REGISTER: Final = 0
STATE_PLAYING: Final = 1
STATE_PAUSED: Final = 2
STATE_GAME_OVER: Final = 3
STATE_HIGH_SCORES: Final = 4

# Gameplay
INITIAL_HEALTH: Final = 3
MAX_HEALTH: Final = 6
JUMP_DURATION: Final = 0.4
GRAVITY_BASE: Final = 1300.0

# Positions (relative to ground line at height - 200)
GROUND_OFFSET: Final = 200
SONIC_X: Final = 100

# Spawning & speed
BASE_MOB_SPEED: Final = 850
MAX_ACCELERATION: Final = 666

# Timing
FPS_LIMIT: Final = 200

# Visual effects
DAMAGE_FLASH: Final = 0.25
HEAL_FLASH: Final = 0.25
GAME_OVER_WAIT: Final = 3.0
SHAKE_INTENSITY: Final = 10
SHAKE_DURATION: Final = 0.15

# Scoring thresholds
SCORE_SOUND_INTERVAL: Final = 100
SCORE_BIG_SOUND_INTERVAL: Final = 1000

# Paths
FONT_PATH: Final = "font/BACKTO1982.TTF"
SCORES_FILE: Final = "best_score.pickle"

# Sound paths
HEALING_PATH: Final = "sounds/healing.wav"
JUMP_PATH: Final = "sounds/jump.mp3"
DAMAGE_PATH: Final = "sounds/damage.wav"
LOST_PATH: Final = "sounds/lost.wav"
SCORE_PATH: Final = "sounds/score.wav"
SCORE1000_PATH: Final = "sounds/best_score.wav"
BESTSCORE_PATH: Final = "sounds/best_score.wav"
MAIN_MUSIC_PATH: Final = "sounds/mainMusic.wav"

# Image paths
SONIC_FRAMES: Final = [
    "images/sonic1.gif",
    "images/sonic2.gif",
    "images/sonic3.gif",
    "images/sonic4.gif",
]
SONIC_STANDING_FRAMES: Final = [
    "images/sonicStanding1.gif",
    "images/sonicStanding2.gif",
]
DUCK_FRAMES: Final = [
    "images/duck1.png",
    "images/duck2.png",
]
SPIKE_IMAGE: Final = "images/spike.png"
BIRD_IMAGE: Final = "images/bird.png"
ROCK_IMAGE: Final = "images/rock.png"
SONIC_JUMP_IMAGE: Final = "images/sonicJump.png"
HEART_IMAGE: Final = "images/heart.png"
GRASS_IMAGE: Final = "images/grass.png"
CLOUD_IMAGE: Final = "images/cloud.png"
PALM_IMAGE: Final = "images/palm-min.png"
PALM2_IMAGE: Final = "images/palm2-min.png"
