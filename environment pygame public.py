# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 16:51:38 2025

@author: josep
"""

import pygame
import sys
import random

def draw_character(screen, x, y, shirt_color, pants_color):
    # Tête
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 10)  # Tête

    # Corps (chemise)
    pygame.draw.line(screen, shirt_color, (x, y + 10), (x, y + 40), 5)  # Corps

    # Bras (noirs)
    pygame.draw.line(screen, (0, 0, 0), (x, y + 15), (x - 10, y + 30), 3)  # Bras gauche
    pygame.draw.line(screen, (0, 0, 0), (x, y + 15), (x + 10, y + 30), 3)  # Bras droit

    # Jambes (pantalon coloré)
    pygame.draw.line(screen, pants_color, (x, y + 40), (x - 10, y + 60), 3)  # Jambe gauche
    pygame.draw.line(screen, pants_color, (x, y + 40), (x + 10, y + 60), 3)  # Jambe droite

def draw_audience(screen, start_x, start_y, rows, cols, spacing, animations, colors):
    # Dessine un public en plusieurs rangées avec des déplacements animés.
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            x_animation = animations[index][0]
            y_animation = animations[index][1]
            x = start_x + col * spacing + x_animation
            y = start_y - row * spacing + y_animation
            shirt_color, pants_color = colors[index]
            draw_character(screen, x, y, shirt_color, pants_color)

def update_animations(animations, max_movement):
    # Met à jour les déplacements aléatoires
    for i in range(len(animations)):
        animations[i][0] += random.uniform(-0.5, 0.5)  # Mouvement horizontal
        animations[i][1] += random.uniform(-0.5, 0.5)  # Mouvement vertical

        # Limite les déplacements
        animations[i][0] = max(-max_movement, min(max_movement, animations[i][0]))
        animations[i][1] = max(-max_movement, min(max_movement, animations[i][1]))

def execution():
    
    pygame.init()
    pygame.mixer.init()

    # Dimensions de la fenêtre
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("l'echafaud")

    # Charge le background
    background = pygame.image.load("pendaison.jpg")
    background = pygame.transform.scale(background, (width, height))
    # Charge la musique d'ambiance
    pygame.mixer.music.load('ost.mp3')
    pygame.mixer.music.play(-1)

    # Couleurs
    BLACK = (0, 0, 0)
    BROWN = (139, 69, 19)
    GRAY = (169, 169, 169)

    # framerate
    clock = pygame.time.Clock()

    # Position de base du public
    audience_base_x = 10
    audience_base_y = 550
    rows, cols = 2, 20
    spacing = 38
    max_movement = 3

    # Initialise les animations du public
    animations = [[0, 0] for _ in range(rows * cols)]

    # Couleurs perso
    colors = [
        ((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),  # Chemise
         (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))   # Pantalon
        for _ in range(rows * cols)
    ]

    # Boucle principale
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Met à jour les animations du public
        update_animations(animations, max_movement)

        # Arrière-plan vierge
        screen.blit(background, (0, 0))

        # L'echafaud
        # Base
        pygame.draw.rect(screen, BROWN, (200, 400, 400, 20))  # Plateforme
        # Poteaux
        pygame.draw.rect(screen, BROWN, (220, 200, 20, 200))  # Poteau gauche
        pygame.draw.rect(screen, BROWN, (220, 180, 200, 20))  # Poutre horizontale
        # Pieds
        pygame.draw.rect(screen, BROWN, (200, 420, 20, 80))  # Pied gauche avant
        pygame.draw.rect(screen, BROWN, (580, 420, 20, 80))  # Pied droit avant
        pygame.draw.rect(screen, BROWN, (220, 420, 20, 80))  # Pied gauche arrière
        pygame.draw.rect(screen, BROWN, (560, 420, 20, 80))  # Pied droit arrière
        # Escalier
        for i in range(5):
            pygame.draw.rect(screen, BROWN, (180, 420 + i * 20, 80, 10))
        # Corde
        pygame.draw.line(screen, GRAY, (400, 200), (400, 280), 5)  # Ligne de la corde
        pygame.draw.circle(screen, BLACK, (400, 290), 10)  # Noeud de la corde

        # Ajouts du public 
        draw_audience(screen, audience_base_x, audience_base_y, rows, cols, spacing, animations, colors)

        # Rafraîchir l'écran
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    execution()
