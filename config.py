# ======================== config.py ========================

import os

# Chemin absolu du dossier du projet et du dossier d'assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Dimensions de la fenêtre
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 800

# Dimensions du Doodle
DOODLE_WIDTH = 60
DOODLE_HEIGHT = 60
DOODLE_SIZE = (DOODLE_WIDTH, DOODLE_HEIGHT)
DOODLE_START_X = SCREEN_WIDTH // 2 - DOODLE_WIDTH // 2
DOODLE_START_Y = SCREEN_HEIGHT - 200

# Dimensions des plateformes
PLATFORM_WIDTH = 105
PLATFORM_HEIGHT = 25
PLATFORM_SIZE = (PLATFORM_WIDTH, PLATFORM_HEIGHT)

# Limites de distance verticale entre les plateformes
MIN_PLATFORM_GAP = 70
MAX_PLATFORM_GAP = 140

# Vitesse des plateformes mobiles (bleues)
MOVING_PLATFORM_SPEED = 3

# Physique du jeu
GRAVITY = 0.5
JUMP_VELOCITY = -14.0
SPRING_JUMP_VELOCITY = -21.0
DOODLE_SPEED = 8

# Vies et Seuil de défilement (Camera Scroll)
LIVES = 1
CAMERA_SCROLL_THRESHOLD = 350

# Images par seconde
FPS = 60

# Liste globale des plateformes
PLATFORMS = []

# Dictionnaire global du Doodle
doodle_dict = {}  # Sera rempli dans doodle.py
