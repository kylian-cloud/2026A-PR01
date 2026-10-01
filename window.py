# ======================== window.py ========================

import os
import pygame
import random
from config import (
    ASSETS_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORMS,
    PLATFORM_WIDTH, MIN_PLATFORM_GAP, MAX_PLATFORM_GAP,
    doodle_dict, DOODLE_START_X, DOODLE_START_Y, DOODLE_WIDTH
)
from platforms import create_platform, choose_platform_type

# Initialisation de la fenêtre Pygame
GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump - INF1007")

# Chargement de l'arrière-plan avec chemin dynamique
background_img = pygame.image.load(os.path.join(ASSETS_DIR, "background.png"))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


def generate_initial_platforms():
    """
    Génère la disposition initiale des plateformes au début de la partie.
    Place une plateforme verte directement sous le Doodle pour assurer un départ sûr,
    puis remplit l'écran jusqu'en haut avec des plateformes variées.
    """
    PLATFORMS.clear()

    # Plateforme de départ directement sous le Doodle : code fourni
    start_platform = create_platform(
        DOODLE_START_X + (DOODLE_WIDTH - PLATFORM_WIDTH) // 2,
        DOODLE_START_Y + 70,
        "green"
    )
    PLATFORMS.append(start_platform)

    current_y = DOODLE_START_Y + 70 - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)

    # ======================== PARTIE 2.2 ========================
    # TODO : Ajoutez des plateformes jusqu'à ce que la partie supérieure
    # de l'écran soit remplie.
    #
    # À chaque itération, vous devrez notamment déterminer une position
    # horizontale valide, choisir un type avec choose_platform_type(...),
    # ajouter la plateforme à PLATFORMS et calculer la hauteur de la suivante.
    # Les probabilités à utiliser sont données dans le README.=======================

    while current_y > 0:

        # 1. Calcul ou génération des coordonnées x et y
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = current_y

        # 2. Choix aléatoire du type de plateforme
        chosen_type = choose_platform_type(0.65, 0.17, 0.10)

        # 3. Création de la plateforme avec x, y et le type choisi
        platform = create_platform(x, y, chosen_type)

        # 4. Ajout à la liste des plateformes
        PLATFORMS.append(platform)

        # 5. Hauteur de la plateforme suivante (espacement aléatoire)
        current_y -= random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)

def draw_window():
    """
    Affiche tous les éléments graphiques du jeu : arrière-plan, plateformes,
    personnage Doodle et le score.
    """
    GAME_WINDOW.blit(background_img, (0, 0))

    for p in PLATFORMS:
        if p["active"]:
            GAME_WINDOW.blit(p["image"], (int(p["x"]), int(p["y"])))

    GAME_WINDOW.blit(doodle_dict["image"], (int(doodle_dict["x"]), int(doodle_dict["y"])))

    font = pygame.font.SysFont("Arial", 28, bold=True)
    score_text = font.render(f"Score : {int(doodle_dict['score'])}", True, (40, 40, 40))
    GAME_WINDOW.blit(score_text, (20, 20))

    pygame.display.update()


def show_game_over_message():
    """
    Affiche l'écran de Game Over avec un fondu semi-transparent
    et les instructions pour recommencer.
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((20, 20, 30))
    GAME_WINDOW.blit(overlay, (0, 0))

    font_title = pygame.font.SysFont("Arial", 64, bold=True)
    font_sub = pygame.font.SysFont("Arial", 32)
    font_hint = pygame.font.SysFont("Arial", 24)

    title_text = font_title.render("GAME OVER", True, (235, 60, 60))
    score_text = font_sub.render(f"Score Final : {int(doodle_dict['score'])}", True, (255, 255, 255))
    high_score_text = font_sub.render(f"Meilleur Score : {int(doodle_dict['high_score'])}", True, (255, 215, 0))
    hint_text = font_hint.render("Appuyez sur R pour recommencer", True, (200, 200, 200))

    GAME_WINDOW.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90)))
    GAME_WINDOW.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10)))
    GAME_WINDOW.blit(high_score_text, high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 35)))
    GAME_WINDOW.blit(hint_text, hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)))

    pygame.display.update()
