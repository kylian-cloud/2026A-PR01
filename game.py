# ======================== game.py ========================

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 ========================
def apply_gravity():
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    # TODO : Mettez à jour la vitesse verticale puis la position verticale
    # du Doodle à partir de GRAVITY.

    doodle_dict["vel_y"] += GRAVITY
    doodle_dict["y"] += doodle_dict["vel_y"]
    return

# ===========================================================


# ======================== PARTIE 1.2 ========================
def move_doodle():
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        doodle_dict["direction"] = "left"
        doodle_dict["image"] = doodle_left_img
        doodle_dict["x"] -= DOODLE_SPEED
        
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        doodle_dict["direction"] = "right"
        doodle_dict["image"] = doodle_right_img
        doodle_dict["x"] += DOODLE_SPEED

    
    

    # TODO : Implémentez le Screen Wrap pour qu'une partie du Doodle puisse
    # sortir d'un côté avant de réapparaître de l'autre.
    # N'utilisez pas de dimensions numériques écrites directement.
    if doodle_dict["x"] > SCREEN_WIDTH:
        doodle_dict["x"] = - DOODLE_WIDTH

    if doodle_dict["x"] + DOODLE_WIDTH < 0:
            doodle_dict["x"] = SCREEN_WIDTH


    return

# ===========================================================


# ======================== PARTIE 2.3 ========================
def move_platforms():
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """
    # TODO : Parcourez les plateformes et gérez le déplacement des plateformes
    # bleues encore actives. Elles doivent rester dans la fenêtre en inversant
    # leur vitesse lorsqu'elles atteignent un bord
    for platform in PLATFORMS:
        if platform["type"] == "blue" and platform["active"]:
            platform["x"] += platform["vx"]
            if platform["x"] + platform["width"] >= SCREEN_WIDTH:
                platform["vx"] = -platform["vx"]
            elif platform["x"] <= 0:
                platform["vx"] = -platform["vx"]
    return 

# ===========================================================


# ======================== PARTIE 3.2 ========================
def check_platform_collisions():
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
    # TODO : Implémentez la détection d'un atterrissage.
    #
    # Contraintes :
    # - aucun rebond pendant la montée ;
    # - ignorer les plateformes inactives ;
    # - utiliser rects_collide(...) pour le chevauchement des rectangles ;
    # - un simple chevauchement ne suffit pas : le Doodle doit arriver par
    #   le dessus de la plateforme. Pour le vérifier, comparez la position
    #   actuelle de ses pieds à leur position approximative à l'image
    #   précédente à l'aide de vel_y. Une tolérance de 14 pixels est permise ;
    # - spring : SPRING_JUMP_VELOCITY ;
    # - brown : JUMP_VELOCITY puis désactivation de la plateforme ;
    # - green/blue : JUMP_VELOCITY.
    doodle_rect = (doodle_dict["x"],doodle_dict["y"],DOODLE_WIDTH,DOODLE_HEIGHT)
    for p in PLATFORMS:
        plateform_rect = (p["x"], p["y"], p["width"], p["height"])
        if doodle_dict["vel_y"] > 0 and p["active"]:
            if rects_collide(plateform_rect,doodle_rect):
                pied_doodle = doodle_dict["y"] + DOODLE_HEIGHT
                pied_doodle_passe = pied_doodle - doodle_dict["vel_y"]
                if pied_doodle_passe <= p["y"] + 14:
                    if p["type"] == "spring":
                        doodle_dict["vel_y"] = SPRING_JUMP_VELOCITY
                    elif p["type"] == "brown":
                        doodle_dict["vel_y"] = JUMP_VELOCITY
                        p["active"] = False
                    elif p["type"] == "green" or p["type"] == "blue":
                        doodle_dict["vel_y"] = JUMP_VELOCITY
                    break
                        



    return

# ===========================================================


# ======================== PARTIE 3.3 ========================
def scroll_camera():
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    # TODO : Lorsque le Doodle dépasse le seuil de caméra, il doit rester
    # visuellement au seuil pendant que les plateformes sont déplacées vers
    # le bas de la même distance.
    #
    # Le score doit représenter la distance verticale ainsi parcourue et le
    # meilleur score doit être mis à jour. Les plateformes sorties sous
    # l'écran doivent être retirées, puis de nouvelles plateformes générées.
    if doodle_dict["y"] < CAMERA_SCROLL_THRESHOLD:
        # Calcule la distance de déplacement vertical
        scroll_distance = CAMERA_SCROLL_THRESHOLD - doodle_dict["y"]

        # 1. Maintient le Doodle au niveau du seuil
        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD

        # 2. Déplace toutes les plateformes vers le bas de la même distance
        for platform in PLATFORMS:
            platform["y"] += scroll_distance

        # 3. Met à jour le score et le meilleur score
        doodle_dict["score"] += scroll_distance
        high_score = doodle_dict.get("high_score", 0)
        if doodle_dict["score"] > high_score:
            doodle_dict["high_score"] = doodle_dict["score"]
        

        # 4. Supprime les plateformes qui sortent par le bas de l'écran
        PLATFORMS[:] = [p for p in PLATFORMS if p["y"] < SCREEN_HEIGHT]

        # 5. Génère de nouvelles plateformes en haut de l'écran
        generate_new_platforms()

    
    return

# ===========================================================


# ======================== PARTIE 3.4 ========================
def generate_new_platforms():
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """
    # TODO : Complétez cette fonction en vous inspirant de la logique de
    # génération initiale, sans la recopier inutilement.
    #
    # Vous devrez partir de la plateforme actuellement la plus haute et
    # continuer à ajouter des plateformes tant que nécessaire. Utilisez
    # choose_platform_type(...) avec les probabilités indiquées dans le README.
    # 1. Point de départ : la plateforme la plus haute (ou le bas de l'écran si la liste est vide)
    if len(PLATFORMS) == 0:
        current_y = SCREEN_HEIGHT
    else:
        highest_platform = min(PLATFORMS, key=lambda p: p['y'])
        current_y = highest_platform['y']

    # 2. Continue d'ajouter des plateformes tant qu'on n'a pas dépassé une marge au-dessus de l'écran
    while current_y > -100:  # Marge au-dessus du haut de l'écran (y = 0)
        # Détermine une distance verticale aléatoire entre les plateformes
        gap_y = random.randint( MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
        current_y -= gap_y

        # Position X aléatoire pour la plateforme
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)

        # Choisit le type de plateforme via la fonction recommandée
        p_type = choose_platform_type(0.55, 0.20, 0.13)

        # Crée et ajoute la nouvelle plateforme
        new_platform = create_platform(x, current_y, p_type)
        PLATFORMS.append(new_platform)

    
    return

# ===========================================================


def check_game_over():
    """
    Vérifie si le Doodle tombe sous le bas de l'écran.
    Si oui, réduit les vies.
    Retourne True si la partie est terminée.
    """
    if doodle_dict["y"] > SCREEN_HEIGHT:
        doodle_dict["lives"] -= 1
        return True
    return False


def restart_game():
    """
    Réinitialise la partie : position du Doodle, vitesse, score et plateformes.
    """
    doodle_dict["x"] = DOODLE_START_X
    doodle_dict["y"] = DOODLE_START_Y
    doodle_dict["vel_y"] = 0.0
    doodle_dict["direction"] = "right"
    doodle_dict["image"] = doodle_right_img
    doodle_dict["score"] = 0
    doodle_dict["lives"] = LIVES

    generate_initial_platforms()


def rects_collide(r1, r2):
    """
    Vérifie si deux rectangles (x, y, largeur, hauteur) se chevauchent.
    Cette fonction est fournie et ne doit pas être modifiée.
    """
    return not (
        r1[0] + r1[2] <= r2[0] or r1[0] >= r2[0] + r2[2] or
        r1[1] + r1[3] <= r2[1] or r1[1] >= r2[1] + r2[3]
    )
