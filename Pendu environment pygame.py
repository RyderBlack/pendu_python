import pygame
import sys


def execution():
    # Initialisation de Pygame
    pygame.init()

    # Dimensions de la fenêtre
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Échafaud")

    # Charge le background
    background = pygame.image.load("pendaison.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Couleurs
    BLACK = (0, 0, 0)
    BROWN = (139, 69, 19)
    GRAY = (169, 169, 169)

    # Boucle principale
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # arrière-plan vierge
        screen.blit(background, (0, 0))

        # L'échafaud
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

        # Ajoute le public en bas de la carte
        for i in range(21):
            x = 10 + i * 38
            y = 550
            pygame.draw.circle(screen, BLACK, (x, y), 10)  # Tête
            pygame.draw.line(screen, BLACK, (x, y + 10), (x, y + 40), 5)  # Corps
            pygame.draw.line(screen, BLACK, (x, y + 15), (x - 10, y + 30), 3)  # Bras gauche
            pygame.draw.line(screen, BLACK, (x, y + 15), (x + 10, y + 30), 3)  # Bras droit
            pygame.draw.line(screen, BLACK, (x, y + 40), (x - 10, y + 60), 3)  # Jambe gauche
            pygame.draw.line(screen, BLACK, (x, y + 40), (x + 10, y + 60), 3)  # Jambe droite

        # Ajoute une deuxième rangée de public au-dessus de la première
        for i in range(20):
            x = 29 + i * 38
            y = 520
            pygame.draw.circle(screen, BLACK, (x, y), 10)  # Tête
            pygame.draw.line(screen, BLACK, (x, y + 10), (x, y + 40), 5)  # Corps
            pygame.draw.line(screen, BLACK, (x, y + 15), (x - 10, y + 30), 3)  # Bras gauche
            pygame.draw.line(screen, BLACK, (x, y + 15), (x + 10, y + 30), 3)  # Bras droit
            pygame.draw.line(screen, BLACK, (x, y + 40), (x - 10, y + 60), 3)  # Jambe gauche
            pygame.draw.line(screen, BLACK, (x, y + 40), (x + 10, y + 60), 3)  # Jambe droite

        # Ajouter 1 mob sur le côté gauche
        for i in range(1):
            x = 10
            y = 480 - i * 38
            pygame.draw.circle(screen, BLACK, (x, y), 10)  # Tête
            pygame.draw.line(screen, BLACK, (x, y + 10), (x, y + 40), 5)  # Corps
            pygame.draw.line(screen, BLACK, (x, y + 15), (x - 10, y + 30), 3)  # Bras gauche
            pygame.draw.line(screen, BLACK, (x, y + 15), (x + 10, y + 30), 3)  # Bras droit
            pygame.draw.line(screen, BLACK, (x, y + 40), (x - 10, y + 60), 3)  # Jambe gauche
            pygame.draw.line(screen, BLACK, (x, y + 40), (x + 10, y + 60), 3)  # Jambe droite

        # Ajouter 1 mob au-dessus de ceux de gauche
        for i in range(1):
            x = 35
            y = 475 - i * 38
            pygame.draw.circle(screen, BLACK, (x, y), 10)  # Tête
            pygame.draw.line(screen, BLACK, (x, y + 10), (x, y + 40), 5)  # Corps
            pygame.draw.line(screen, BLACK, (x, y + 15), (x - 10, y + 30), 3)  # Bras gauche
            pygame.draw.line(screen, BLACK, (x, y + 15), (x + 10, y + 30), 3)  # Bras droit
            pygame.draw.line(screen, BLACK, (x, y + 40), (x - 10, y + 60), 3)  # Jambe gauche
            pygame.draw.line(screen, BLACK, (x, y + 40), (x + 10, y + 60), 3)  # Jambe droite
            
       

        # Rafraîchir l'écran
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    execution()
